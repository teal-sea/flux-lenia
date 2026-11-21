"""Apply the decision rules of docs/CAMPAIGN-HARNESS-2026-11-16.md to run JSON (no simulation).

Usage: python scripts/campaign_harness_summary.py [control|kappa|horizon|all] [HARNESSDIR]
HARNESSDIR defaults to outputs/campaign_harness_20261116 (subdirs control_box, control_box_repeat,
kappa_1, kappa_10, horizon_300k). Reference sets: outputs/food_on_exact_20261110 (citadel control, repulsion
off) and outputs/conditional_blending_20261115 (repulsion on, kappa 3, 30,000 steps).
"""

from __future__ import annotations

import json
import math
import statistics as st
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from food_selection_summary import SPECIES, load  # noqa: E402

CIT = ROOT / "outputs/food_on_exact_20261110"
STEP2 = ROOT / "outputs/conditional_blending_20261115"
ARMS = ("treat", "neutral_plus", "neutral_minus")
NEUT = ARMS[1:]


def pct(xs, q):
    xs = sorted(xs)
    k = (len(xs) - 1) * q
    lo, hi = math.floor(k), math.ceil(k)
    return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)


def med(xs):
    return st.median(xs) if xs else float("nan")


def food(runs):
    return {k: v for k, v in runs.items() if k[1]}


def short(sp):
    return sp[12:]


# ---------------------------------------------------------------- part 1
def control(h: Path) -> None:
    box, rep, cit, s2 = (food(load(p)) for p in (h / "control_box", h / "control_box_repeat", CIT, STEP2))
    print(f"## Part 1: same-host control and determinism\n\n{len(box)} box-control runs, {len(rep)} repeats, "
          f"{len(cit)} citadel-control runs, {len(s2)} step 2 repulsion runs.\n")
    print("### (a) Determinism (repeat on the same box minus first run)\n")
    print("| run | |d final share_A| | |d final hybrid_frac| | first sample with |d share_A| > 1e-12 (step) | wall s first / repeat |")
    print("|---|---|---|---|---|")
    ok, n = True, 0
    for k, r in sorted(rep.items()):
        b = box.get(k)
        if b is None:
            print(f"| {short(k[0])} s{k[3]} {k[2]} | box run missing | | | |")
            continue
        ds = abs(r["final"]["share_A"] - b["final"]["share_A"]); dh = abs(r["final"]["hybrid_frac"] - b["final"]["hybrid_frac"])
        div = next((t for t, x, y in zip(b["t"], b["series"]["share_A"], r["series"]["share_A"]) if abs(x - y) > 1e-12), None)
        ok &= ds <= 1e-12 and dh <= 1e-12; n += 1
        print(f"| {short(k[0])} s{k[3]} {k[2]} | {ds:.3e} | {dh:.3e} | {div if div is not None else 'none'} "
              f"| {b['wall_seconds']:.0f} / {r['wall_seconds']:.0f} |")
    print(f"\n**Verdict (a): {'deterministic' if ok and n == 3 else ('nondeterministic on one host' if n else 'incomplete')}** "
          f"({n} repeats compared).\n")

    print("### (b) Host effect: |box - citadel| per run, 45 runs\n")
    print("| set | measure | n | median | max | agree 1e-12 | agree 1e-6 | agree 1e-2 |")
    print("|---|---|---|---|---|---|---|---|")
    for name, sel in [("all", lambda k: True)] + [(short(sp), (lambda k, sp=sp: k[0] == sp)) for sp in SPECIES]:
        ks = [k for k in box if k in cit and sel(k)]
        for meas in ("share_A", "hybrid_frac"):
            d = [abs(box[k]["final"][meas] - cit[k]["final"][meas]) for k in ks]
            if not d:
                continue
            print(f"| {name} | final {meas} | {len(d)} | {med(d):.3e} | {max(d):.3e} | {sum(x <= 1e-12 for x in d)} "
                  f"| {sum(x <= 1e-6 for x in d)} | {sum(x <= 1e-2 for x in d)} |")
    ks = [k for k in box if k in cit]
    if ks:
        d = [abs(box[k]["series"]["share_A"][i] - cit[k]["series"]["share_A"][i]) for k in ks
             for i in [min(3, len(box[k]["t"]) - 1)]]
        print(f"\nAt step {box[ks[0]]['t'][min(3, len(box[ks[0]]['t']) - 1)]} (series index 3): median |d share_A| {med(d):.2e}, max {max(d):.2e}.")
        firsts = []
        for k in ks:
            firsts.append(next((t for t, x, y in zip(box[k]["t"], box[k]["series"]["share_A"], cit[k]["series"]["share_A"])
                                if abs(x - y) > 1e-12), None))
        fv = [f for f in firsts if f is not None]
        print(f"First sample at which box and citadel differ by more than 1e-12 in share_A: median {med(fv):.0f} steps "
              f"(min {min(fv) if fv else 'n/a'}, max {max(fv) if fv else 'n/a'}); never: {sum(f is None for f in firsts)} of {len(firsts)}.")

    print("\n### (c) Step 2 neutral-arm check: repulsion (kappa 3) minus control, final hybrid fraction, 10 pairs per species\n")
    print("| species | control used | n | mean diff | SE | mean/SE | flag |")
    print("|---|---|---|---|---|---|---|")
    flags = {}
    for label, ctrl, other in (("box control (this campaign)", box, s2), ("citadel control (repeats step 2)", cit, s2),
                               ("box minus citadel, same runs", box, cit)):
        for sp in SPECIES:
            d = [other[(sp, True, a, s)]["final"]["hybrid_frac"] - ctrl[(sp, True, a, s)]["final"]["hybrid_frac"]
                 for a in NEUT for s in range(1, 6) if (sp, True, a, s) in other and (sp, True, a, s) in ctrl]
            if len(d) < 2:
                print(f"| {short(sp)} | {label} | {len(d)} | | | | |")
                continue
            m, se = st.mean(d), st.stdev(d) / math.sqrt(len(d))
            z = m / se if se > 0 else (0.0 if m == 0 else float("inf"))
            flags[(label, sp)] = abs(z) > 2
            print(f"| {short(sp)} | {label} | {len(d)} | {m:+.4f} | {se:.4f} | {z:+.2f} | {'exceeds 2 SE' if abs(z) > 2 else 'ok'} |")
    lab = "box control (this campaign)"
    got = [flags.get((lab, sp)) for sp in SPECIES]
    if None in got:
        v = "incomplete"
    else:
        v = "confirmed (at least one species still exceeds 2 SE with the same-host control)" if any(got) else "cleared (all species within 2 SE)"
    print(f"\n**Verdict (c), step 2 flag: {v}.** (Three species were tested, so about 14% chance of one exceedance by chance with no leak.)\n")


# ---------------------------------------------------------------- shared selection logic
def sat_stats(r):
    s = r["series"].get("sat_frac")
    if not s:
        return float("nan"), float("nan")
    return max(s[1:]), st.mean(s[1:])


def sel_verdict(treat, neutral, E, min_out):
    out = [r for r in treat if abs(r["delta_share_A"]) > E]
    winners = {"+u" if r["delta_share_A"] > 0 else "-u" for r in out}
    ws = [r["share_A_end"] if r["delta_share_A"] > 0 else 1 - r["share_A_end"] for r in out]
    if len(out) >= min_out and len(winners) == 1:
        v = "takeover" if all(x >= 0.9 for x in ws) else "selection"
    elif len(out) >= min_out:
        v = "large but inconsistent"
    else:
        v = "no selection detected"
    npos = sum(r["delta_share_A"] > 0 for r in out)
    return v, len(out), f"+u {npos} / -u {len(out) - npos}", (max(ws) if ws else float("nan"))


def rule1(h, c):
    mh, mc = med(h), med(c)
    below = sum(a < b for a, b in zip(h, c))
    v = "distinct" if (mh <= mc / 2 and below >= 4) else ("no effect" if below < 3 else "partial")
    return v, mh, mc, below


# ---------------------------------------------------------------- part 2
def kappa(h: Path) -> None:
    box = food(load(h / "control_box"))
    s2 = food(load(STEP2))
    cit = food(load(CIT))
    print("## Part 2: kappa robustness (kappa 1 and 10, seeds 1 to 20)\n")
    ds = {k: food(load(h / f"kappa_{k}")) for k in (1, 10)}
    for k, runs in ds.items():
        print(f"- kappa {k}: {len(runs)} of 180 runs present")
    for k, runs in ds.items():
        if not runs:
            continue
        print(f"\n### kappa {k}\n")
        print("**Distinctness (rule 1 matched for seeds 1-5; descriptive for seeds 6-20)**\n")
        print("| species | seeds 1-5 control median | treat median (seeds 1-5) | seeds below matched control | rule 1 verdict "
              "| seeds 6-20 treat hybrid: min / q1 / median / q3 / max | seeds 6-20 below control median | distinct (unmatched) "
              "| all 20: median | box-control verdict (secondary) |")
        print("|---|---|---|---|---|---|---|---|---|---|")
        for sp in SPECIES:
            t = {s: runs.get((sp, True, "treat", s)) for s in range(1, 21)}
            h15 = [t[s]["final"]["hybrid_frac"] for s in range(1, 6) if t[s]]
            c15 = [cit[(sp, True, "treat", s)]["final"]["hybrid_frac"] for s in range(1, 6) if t[s]]
            late = [t[s]["final"]["hybrid_frac"] for s in range(6, 21) if t[s]]
            if len(h15) < 5:
                print(f"| {short(sp)} | incomplete |")
                continue
            v, mh, mc, below = rule1(h15, c15)
            cm = med([cit[(sp, True, "treat", s)]["final"]["hybrid_frac"] for s in range(1, 6)])
            lb = sum(x < cm for x in late)
            un = (len(late) == 15 and med(late) <= cm / 2 and lb >= 12)
            bx = [box[(sp, True, "treat", s)]["final"]["hybrid_frac"] for s in range(1, 6) if (sp, True, "treat", s) in box]
            bv = rule1(h15, bx)[0] if len(bx) == 5 else "n/a"
            q = (f"{min(late):.3f} / {pct(late, .25):.3f} / {med(late):.3f} / {pct(late, .75):.3f} / {max(late):.3f}"
                 if late else "n/a")
            print(f"| {short(sp)} | {mc:.3f} | {mh:.3f} | {below} of 5 | {v} | {q} (n={len(late)}) | {lb} of {len(late)} "
                  f"| {'yes' if un else 'no'} | {med(h15 + late):.3f} | {bv} |")
        print("\n**Selection (rule 2 scaled to 20 seeds: 16 of 20 outside E)**\n")
        print("| species | E (max of 40 neutral) | treat out of E | winners | max winner share | verdict | E95 (secondary) "
              "| out of E95 | verdict at E95 (secondary) | treat deltas (20 seeds) |")
        print("|---|---|---|---|---|---|---|---|---|---|")
        for sp in SPECIES:
            tr = [runs[(sp, True, "treat", s)] for s in range(1, 21) if (sp, True, "treat", s) in runs]
            ne = [runs[(sp, True, a, s)] for a in NEUT for s in range(1, 21) if (sp, True, a, s) in runs]
            if len(tr) < 20 or len(ne) < 40:
                print(f"| {short(sp)} | incomplete ({len(tr)} treat, {len(ne)} neutral) |")
                continue
            E = max(abs(r["delta_share_A"]) for r in ne)
            E95 = pct([abs(r["delta_share_A"]) for r in ne], 0.95)
            v, n_out, w, mx = sel_verdict(tr, ne, E, 16)
            v2, n2, w2, _ = sel_verdict(tr, ne, E95, 16)
            dl = " ".join(f"{r['delta_share_A']:+.2f}" for r in tr)
            print(f"| {short(sp)} | {E:.4f} | {n_out} of 20 | {w} | {mx:.3f} | {v} | {E95:.4f} | {n2} of 20 | {v2} ({w2}) | {dl} |")
        print("\n**Saturation and conservation**\n")
        print("| species | runs | runs with max-over-samples sat_frac > 1e-2 | runs with mean sat_frac > 1e-2 | largest sat_frac in any sample "
              "| mean of per-run means | max drift sum(body)+sum(food) | wall s median / max |")
        print("|---|---|---|---|---|---|---|---|")
        flag = False
        for sp in SPECIES:
            rs = [r for kk, r in runs.items() if kk[0] == sp]
            if not rs:
                continue
            ss = [sat_stats(r) for r in rs]
            over = sum(a > 1e-2 for a, _ in ss)
            flag |= over > 0
            w = [r["wall_seconds"] for r in rs]
            print(f"| {short(sp)} | {len(rs)} | {over} | {sum(b > 1e-2 for _, b in ss)} | {max(a for a, _ in ss):.2e} "
                  f"| {st.mean(b for _, b in ss):.2e} | {max(r['max_rel_total_drift'] for r in rs):.2e} | {med(w):.0f} / {max(w):.0f} |")
        print(f"\n**Saturation flag for kappa {k}: {'FLAGGED (a run exceeds 1e-2)' if flag else 'not flagged'}.**")
    print("\n### Dose-response, seeds 1-5, treatment, median final hybrid fraction (per species)\n")
    print("| species | kappa 0 (citadel control) | kappa 0 (box control) | kappa 1 | kappa 3 (step 2) | kappa 10 |")
    print("|---|---|---|---|---|---|")
    for sp in SPECIES:
        def m5(runs):
            xs = [runs[(sp, True, "treat", s)]["final"]["hybrid_frac"] for s in range(1, 6) if (sp, True, "treat", s) in runs]
            return f"{med(xs):.3f}" if len(xs) == 5 else "n/a"
        print(f"| {short(sp)} | {m5(cit)} | {m5(box)} | {m5(ds[1])} | {m5(s2)} | {m5(ds[10])} |")
    print()


# ---------------------------------------------------------------- part 3
def d30(r):
    s = r["series"]["share_A"]
    xs = [x for t, x in zip(r["t"], s) if 27000 < t <= 30000]
    return st.mean(xs) - s[0]


def winner_side(r, x):
    return x if r["delta_share_A"] > 0 else 1 - x


def horizon(h: Path) -> None:
    runs = food(load(h / "horizon_300k"))
    cit = food(load(CIT))
    print(f"## Part 3: horizon, 300,000 steps, kappa 3\n\n{len(runs)} of 45 runs present.\n")
    if not runs:
        return
    tau = 0.05
    print("### Per run\n")
    print("| species | arm | seed | A start | d30 | d300 | class (b) | winner share end | winner share peak | h30 | h300 | (c) | blobs end | max drift | wall s |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    cls, hold = {}, {}
    for sp in SPECIES:
        for a in ARMS:
            for s in range(1, 6):
                r = runs.get((sp, True, a, s))
                if r is None:
                    print(f"| {short(sp)} | {a} | {s} | missing |")
                    continue
                x30, x300 = d30(r), r["delta_share_A"]
                if abs(x300 - x30) <= tau:
                    c = "saturated"
                elif x300 * x30 < 0:
                    c = "reverses"
                elif abs(x300) > abs(x30):
                    c = "grows"
                else:
                    c = "shrinks"
                i30 = r["t"].index(30000)
                h30, h300 = r["series"]["hybrid_frac"][i30], r["final"]["hybrid_frac"]
                hd = "holds" if h300 <= max(0.10, h30 + 0.05) else "erodes"
                cls[(sp, a, s)], hold[(sp, a, s)] = c, hd
                ws = winner_side(r, r["share_A_end"])
                pk = max(winner_side(r, x) for x in r["series"]["share_A"])
                print(f"| {short(sp)} | {a} | {s} | {r['share_A_start']:.3f} | {x30:+.3f} | {x300:+.3f} | {c} | {ws:.3f} | {pk:.3f} "
                      f"| {h30:.3f} | {h300:.3f} | {hd} | {r['final']['n_blobs']} | {r['max_rel_total_drift']:.1e} | {r['wall_seconds']:.0f} |")
    print("\n### (a) Takeover\n")
    print("| species | treat runs with winner share end >= 0.90 | treat runs with winner share >= 0.90 at any sample | neutral runs (of 10) with >= 0.90 at any sample | max winner share end (treat) |")
    print("|---|---|---|---|---|")
    anyto = False
    for sp in SPECIES:
        tr = [runs[(sp, True, "treat", s)] for s in range(1, 6) if (sp, True, "treat", s) in runs]
        ne = [runs[(sp, True, a, s)] for a in NEUT for s in range(1, 6) if (sp, True, a, s) in runs]
        e = sum(winner_side(r, r["share_A_end"]) >= 0.9 for r in tr)
        anyto |= e > 0
        pk = sum(max(winner_side(r, x) for x in r["series"]["share_A"]) >= 0.9 for r in tr)
        npk = sum(max(max(x, 1 - x) for x in r["series"]["share_A"]) >= 0.9 for r in ne)
        mx = max((winner_side(r, r["share_A_end"]) for r in tr), default=float("nan"))
        print(f"| {short(sp)} | {e} of {len(tr)} | {pk} of {len(tr)} | {npk} of {len(ne)} | {mx:.3f} |")
    print(f"\n**Verdict (a): {'takeover appears' if anyto else 'no takeover'}** (any treatment run with winner share >= 0.90 at step 300,000).")
    print("\n### (b) Does the share keep moving (|d300 - d30| <= 0.05 saturated)\n")
    print("| species | arm | saturated | grows | reverses | shrinks | median |d300| - |d30| | median |d30| | median |d300| |")
    print("|---|---|---|---|---|---|---|---|---|")
    for sp in SPECIES:
        for grp, arms in (("treat", ("treat",)), ("neutral (10)", NEUT)):
            rs = [(runs[(sp, True, a, s)], cls[(sp, a, s)]) for a in arms for s in range(1, 6) if (sp, True, a, s) in runs]
            if not rs:
                continue
            cnt = {c: sum(x == c for _, x in rs) for c in ("saturated", "grows", "reverses", "shrinks")}
            dd = [abs(r["delta_share_A"]) - abs(d30(r)) for r, _ in rs]
            print(f"| {short(sp)} | {grp} | {cnt['saturated']} | {cnt['grows']} | {cnt['reverses']} | {cnt['shrinks']} "
                  f"| {med(dd):+.3f} | {med([abs(d30(r)) for r, _ in rs]):.3f} | {med([abs(r['delta_share_A']) for r, _ in rs]):.3f} |")
    print("\n### (c) Distinctness at 300,000 steps\n")
    print("| species | arm | median h30 | median h300 | holds | erodes | rule 1 at 300k vs 30k citadel control (treat) |")
    print("|---|---|---|---|---|---|---|")
    for sp in SPECIES:
        for grp, arms in (("treat", ("treat",)), ("neutral (10)", NEUT)):
            ks = [(a, s) for a in arms for s in range(1, 6) if (sp, True, a, s) in runs]
            if not ks:
                continue
            h30s = [runs[(sp, True, a, s)]["series"]["hybrid_frac"][runs[(sp, True, a, s)]["t"].index(30000)] for a, s in ks]
            h300s = [runs[(sp, True, a, s)]["final"]["hybrid_frac"] for a, s in ks]
            ho = sum(hold[(sp, a, s)] == "holds" for a, s in ks)
            r1 = ""
            if grp == "treat" and len(ks) == 5:
                v, mh, mc, below = rule1(h300s, [cit[(sp, True, "treat", s)]["final"]["hybrid_frac"] for s in range(1, 6)])
                r1 = f"{v} (median {mh:.3f} vs control {mc:.3f}, {below} of 5 seeds below)"
            print(f"| {short(sp)} | {grp} | {med(h30s):.3f} | {med(h300s):.3f} | {ho} | {len(ks) - ho} | {r1} |")
    print("\n### (d) Selection at 300,000 steps (rule 2, 4 of 5 bar, E from 10 neutral runs)\n")
    print("| species | E (max |d300| of 10 neutral) | treat out of E | winners | max winner share | verdict | treat d300 (seeds 1-5) | E at 30k (same neutral runs, d30) |")
    print("|---|---|---|---|---|---|---|---|")
    for sp in SPECIES:
        tr = [runs[(sp, True, "treat", s)] for s in range(1, 6) if (sp, True, "treat", s) in runs]
        ne = [runs[(sp, True, a, s)] for a in NEUT for s in range(1, 6) if (sp, True, a, s) in runs]
        if len(tr) < 5 or len(ne) < 10:
            print(f"| {short(sp)} | incomplete |")
            continue
        E = max(abs(r["delta_share_A"]) for r in ne)
        v, n_out, w, mx = sel_verdict(tr, ne, E, 4)
        print(f"| {short(sp)} | {E:.4f} | {n_out} of 5 | {w} | {mx:.3f} | {v} | "
              + " ".join(f"{r['delta_share_A']:+.3f}" for r in tr) + f" | {max(abs(d30(r)) for r in ne):.4f} |")
    print("\n### (e) Conservation, saturation, wall time\n")
    d = [r["max_rel_total_drift"] for r in runs.values()]
    w = [r["wall_seconds"] for r in runs.values()]
    ss = [sat_stats(r) for r in runs.values()]
    print(f"- max relative drift of sum(body)+sum(food), {len(d)} runs: {max(d):.2e} (median {med(d):.2e})")
    print(f"- wall seconds per run: median {med(w):.0f}, min {min(w):.0f}, max {max(w):.0f}")
    print(f"- saturation (max over samples), largest over runs {max(a for a, _ in ss):.2e}; runs above 1e-2: {sum(a > 1e-2 for a, _ in ss)}")
    print("\n### Trajectories (treatment runs): A share and hybrid fraction at steps 0, 30k, 100k, 200k, 300k\n")
    print("| species | seed | share_A | hybrid |")
    print("|---|---|---|---|")
    for sp in SPECIES:
        for s in range(1, 6):
            r = runs.get((sp, True, "treat", s))
            if r is None:
                continue
            ix = [r["t"].index(t) for t in (0, 30000, 100000, 200000, 300000)]
            print(f"| {short(sp)} | {s} | " + " / ".join(f"{r['series']['share_A'][i]:.3f}" for i in ix)
                  + " | " + " / ".join(f"{r['series']['hybrid_frac'][i]:.3f}" for i in ix) + " |")
    print()


def main() -> None:
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    h = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "outputs/campaign_harness_20261116"
    print("# Campaign part A summary (scripts/campaign_harness_summary.py; JSON only, no simulation)\n")
    if mode in ("control", "all"):
        control(h)
    if mode in ("kappa", "all"):
        kappa(h)
    if mode in ("horizon", "all"):
        horizon(h)


if __name__ == "__main__":
    main()
