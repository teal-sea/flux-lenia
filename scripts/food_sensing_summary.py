"""Apply the pilot rule and decision rules of docs/FOOD-SENSING-2026-11-16.md to run JSON.

Usage:
  python scripts/food_sensing_summary.py pilot [PILOTDIR] [REFDIR]
  python scripts/food_sensing_summary.py main  [MAINDIR]
PILOTDIR defaults to outputs/food_sensing_20261116/pilot (subdirs fs<value>/), REFDIR to
outputs/conditional_blending_20261115 (food_sense = 0 reference, kappa = 3), MAINDIR to
outputs/food_sensing_20261116/main (subdirs per cell). Runs only over JSON; no simulation.
"""

from __future__ import annotations

import json
import math
import statistics as st
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SPECIES = ["SPECIES_001_OSCILLIS", "SPECIES_002_MITOSA", "SPECIES_003_VAGRANT"]
ARMS = ("treat", "neutral_plus", "neutral_minus")
PILOT_STEP = 10000
DRIFT_MAX = 1e-12
SAT_MAX = 1e-2
N_OUT = 40            # rule 1: outside E and agreeing
NSEED = 50


def load_dir(d: Path, pattern: str = "SPECIES_*_food1.json", recursive: bool = True) -> list[dict]:
    return [json.loads(p.read_text()) for p in sorted((d.rglob if recursive else d.glob)(pattern))]


def q_at(r: dict, step: int) -> float:
    """Q = body(step) - body(0): net food drawn into the body."""
    i = r["t"].index(step)
    return r["series"]["body"][i] - r["series"]["body"][0]


def drift(r: dict, step: int | None = None) -> float:
    s = r["series"]
    i = len(s["body"]) if step is None else r["t"].index(step) + 1
    tot = [b + f for b, f in zip(s["body"][:i], s["food"][:i])]
    return max(abs(x - tot[0]) / tot[0] for x in tot)


# ---------------------------------------------------------------------------------------- pilot


def pilot(pdir: Path, rdir: Path) -> None:
    ref = {}
    for r in load_dir(rdir, recursive=False):
        if r["arm"] == "treat" and r["repulsion_kappa"] == 3.0 and r["food"]:
            ref[(r["species"], r["seed"])] = r
    Qref, R = {}, {}
    for sp in SPECIES:
        qs = [q_at(ref[(sp, s)], PILOT_STEP) for s in range(1, 6)]
        Qref[sp], R[sp] = q_at(ref[(sp, 1)], PILOT_STEP), max(qs) - min(qs)
    runs = {}
    for r in load_dir(pdir):
        runs[(r["food_sense"], r["species"])] = r
    cands = sorted({k for k, _ in runs if k != 0.0})
    print("## Pilot runs (seed 1, treat, food on, per_channel, kappa 3, 10,000 steps)\n")
    print("Reference (food_sense = 0, 2026-11-15, kappa 3, treat, seeds 1-5, step 10,000): "
          "Q = body(10,000) - body(0); Q_ref = seed 1; R = max - min over seeds 1-5\n")
    print("| species | Q_ref (seed 1) | R (seed spread) | Q seeds 1-5 |")
    print("|---|---|---|---|")
    for sp in SPECIES:
        print(f"| {sp[12:]} | {Qref[sp]:.2f} | {R[sp]:.2f} | "
              + ", ".join(f"{q_at(ref[(sp, s)], PILOT_STEP):.1f}" for s in range(1, 6)) + " |")
    print("\n| food_sense | species | Q | Q - Q_ref | R | changes foraging (|dQ| > R) | gross eaten | body end "
          "| hybrid end | max sat_frac (100 samples) | max drift | wall s | sat ok | drift ok |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    qual, nonsat = {}, {}
    for k in [0.0] + cands:
        flags = []
        for sp in SPECIES:
            r = runs.get((k, sp))
            if r is None:
                print(f"| {k:g} | {sp[12:]} | missing |" + " |" * 11)
                flags.append((False, False, False)); continue
            i = r["t"].index(PILOT_STEP)
            s = r["series"]
            q = q_at(r, PILOT_STEP)
            ch = abs(q - Qref[sp]) > R[sp]
            ms = max(s["sat_frac"][1:i + 1])
            dr = drift(r, PILOT_STEP)
            sat_ok, dr_ok = ms < SAT_MAX, dr <= DRIFT_MAX
            print(f"| {k:g} | {sp[12:]} | {q:.2f} | {q - Qref[sp]:+.2f} | {R[sp]:.2f} | {'yes' if ch else 'no'} "
                  f"| {s['food_eaten_cum'][i]:.1f} | {s['body'][i]:.1f} | {s['hybrid_frac'][i]:.3f} | {ms:.2e} "
                  f"| {dr:.1e} | {r['wall_seconds']:.0f} | {'yes' if sat_ok else 'no'} | {'yes' if dr_ok else 'no'} |")
            flags.append((ch, sat_ok, dr_ok))
        if k != 0.0:
            n_ch = sum(f[0] for f in flags)
            clean = all(f[1] and f[2] for f in flags) and len(flags) == 3
            qual[k] = n_ch >= 2 and clean
            nonsat[k] = clean
            print(f"|  | candidate {k:g}: changes foraging in {n_ch} of 3 species; clean (sat, drift) = {clean}; qualifies = {qual[k]} |" + " |" * 12)
    q = [k for k in cands if qual[k]]
    if q:
        print(f"\n**Chosen food_sense = {min(q):g}** (smallest candidate that qualifies; qualifying: "
              + ", ".join(f"{k:g}" for k in q) + ").")
    else:
        ns = [k for k in cands if nonsat[k]]
        if ns:
            print(f"\n**No candidate qualifies; the largest non-saturating, conserving candidate, food_sense = {max(ns):g}, is taken** (pre-registered fallback).")
        else:
            print(f"\n**No candidate qualifies and none is clean; the smallest candidate, food_sense = {min(cands):g}, is taken** (pre-registered fallback).")


# ---------------------------------------------------------------------------------------- main


def verdicts(runs: dict, sp: str, cell: tuple) -> dict:
    """runs[(sp, cell, arm, seed)]; cell = (food_sense, kappa)."""
    neu = [r["delta_share_A"] for arm in ("neutral_plus", "neutral_minus") for s in range(1, NSEED + 1)
           if (r := runs.get((sp, cell, arm, s))) is not None]
    tr = [(s, runs[(sp, cell, "treat", s)]) for s in range(1, NSEED + 1) if (sp, cell, "treat", s) in runs]
    E = max(abs(x) for x in neu) if neu else float("nan")
    E95 = float(np.percentile(np.abs(neu), 95)) if neu else float("nan")
    out = {"n_neutral": len(neu), "n_treat": len(tr), "E": E, "E95": E95}
    for name, thr in (("", E), ("95", E95)):
        o = [(s, r) for s, r in tr if abs(r["delta_share_A"]) > thr]
        pos = [x for x in o if x[1]["delta_share_A"] > 0]
        neg = [x for x in o if x[1]["delta_share_A"] < 0]
        win = pos if len(pos) >= len(neg) else neg
        wsign = "+u" if win is pos else "-u"
        ws = [r["share_A_end"] if wsign == "+u" else 1 - r["share_A_end"] for _, r in win]
        if len(o) >= N_OUT and len(win) >= N_OUT:
            v = "takeover" if st.median(ws) >= 0.9 else "selection"
        elif len(o) >= N_OUT:
            v = "large but inconsistent"
        else:
            v = "no selection detected"
        out[name] = {"n_out": len(o), "n_pos": len(pos), "n_neg": len(neg), "winner": wsign if o else "-",
                     "wshare": (min(ws), st.median(ws), max(ws)) if ws else None, "verdict": v}
    return out


def main_summary(mdir: Path) -> None:
    runs, cells = {}, set()
    for r in load_dir(mdir):
        cell = (r["food_sense"], r["repulsion_kappa"])
        runs[(r["species"], cell, r["arm"], r["seed"])] = r
        cells.add(cell)
    cells = sorted(cells)
    fsv = sorted({c[0] for c in cells}); kv = sorted({c[1] for c in cells})
    name = lambda c: f"F{'1' if c[0] != 0 else '0'}K{int(c[1])}"
    print(f"{len(runs)} runs in {mdir.name}; cells (food_sense, kappa): " + ", ".join(f"{name(c)}=({c[0]:g}, {c[1]:g})" for c in cells) + "\n")
    cnt = {(sp, c): sum(1 for k in runs if k[0] == sp and k[1] == c) for sp in SPECIES for c in cells}
    print("Runs per species and cell (expected 150): " + "; ".join(f"{sp[12:]} {name(c)} {cnt[(sp, c)]}" for sp in SPECIES for c in cells) + "\n")

    V = {(sp, c): verdicts(runs, sp, c) for sp in SPECIES for c in cells}
    print("### Rule 1: selection per cell per species (E = largest neutral |delta| of the cell's 100 neutral runs)\n")
    print("| species | cell | E | n out | winner split (+u / -u) | winner-side final share min / median / max | verdict | "
          "E95 (secondary) | n out E95 | split E95 | verdict E95 (secondary) |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for sp in SPECIES:
        for c in cells:
            v = V[(sp, c)]; p, q = v[""], v["95"]
            ws = "-" if p["wshare"] is None else "%.3f / %.3f / %.3f" % p["wshare"]
            print(f"| {sp[12:]} | {name(c)} | {v['E']:.4f} | {p['n_out']} of {v['n_treat']} | {p['n_pos']} / {p['n_neg']} | {ws} "
                  f"| {p['verdict']} | {v['E95']:.4f} | {q['n_out']} | {q['n_pos']} / {q['n_neg']} | {q['verdict']} |")

    print("\n### Rule 2: cause (sensing-on selection, matched sensing-off null)\n")
    print("| species | kappa | sensing off | sensing on | cause shown |")
    print("|---|---|---|---|---|")
    sel = lambda v: v in ("selection", "takeover")
    nec = {}
    for sp in SPECIES:
        for k in kv:
            off = V[(sp, (0.0, k))][""]["verdict"] if (sp, (0.0, k)) in V else None
            on = next((V[(sp, c)][""]["verdict"] for c in cells if c[0] != 0 and c[1] == k), None)
            if off is None or on is None:
                continue
            if sel(on) and off == "no selection detected":
                res = "yes"
            elif not sel(on) and on != "large but inconsistent":
                res = "no (no selection with sensing)"
            elif on == "large but inconsistent" or off == "large but inconsistent":
                res = "inconclusive (large but inconsistent cell)"
            else:
                res = "no (selection also without sensing)"
            nec[(sp, k)] = on
            print(f"| {sp[12:]} | {k:g} | {off} | {on} | {res} |")
    for sp in SPECIES:
        on0 = nec.get((sp, 0.0)); on3 = nec.get((sp, 3.0))
        if on0 and on3:
            print(f"\n- {sp[12:]}: repulsion necessary (sensing-on selection at kappa 3 and not at kappa 0): {'yes' if sel(on3) and not sel(on0) else 'no'}")

    print("\n### Rule 3: distinctness, kappa 3 vs kappa 0 at the same food_sense (treatment arm, end hybrid fraction)\n")
    print("| species | food_sense | median hybrid kappa 0 | median hybrid kappa 3 | ratio | seeds below matched kappa-0 seed | verdict |")
    print("|---|---|---|---|---|---|---|")
    for sp in SPECIES:
        for f in fsv:
            a = {s: runs[(sp, (f, 0.0), "treat", s)]["final"]["hybrid_frac"] for s in range(1, NSEED + 1) if (sp, (f, 0.0), "treat", s) in runs}
            b = {s: runs[(sp, (f, 3.0), "treat", s)]["final"]["hybrid_frac"] for s in range(1, NSEED + 1) if (sp, (f, 3.0), "treat", s) in runs}
            seeds = sorted(set(a) & set(b))
            if not seeds:
                continue
            m0, m3 = st.median(a[s] for s in seeds), st.median(b[s] for s in seeds)
            below = sum(b[s] < a[s] for s in seeds)
            v = "distinct" if (m3 <= m0 / 2 and below >= 40) else ("no effect" if below < 30 else "partial")
            print(f"| {sp[12:]} | {f:g} | {m0:.3f} | {m3:.3f} | {m3 / m0 if m0 else float('nan'):.2f} | {below} of {len(seeds)} | {v} |")

    print("\n### Rule 4: neutral-arm sanity (mean and SE of neutral delta; flag if |mean| > 2 SE)\n")
    print("| species | cell | n | mean | SE | mean/SE | neutral_plus mean | neutral_minus mean | flag |")
    print("|---|---|---|---|---|---|---|---|---|")
    nflag = 0
    for sp in SPECIES:
        for c in cells:
            per = {arm: [runs[(sp, c, arm, s)]["delta_share_A"] for s in range(1, NSEED + 1) if (sp, c, arm, s) in runs]
                   for arm in ("neutral_plus", "neutral_minus")}
            d = per["neutral_plus"] + per["neutral_minus"]
            if len(d) < 2:
                continue
            m, se = st.mean(d), st.stdev(d) / math.sqrt(len(d))
            z = m / se if se > 0 else 0.0
            fl = abs(z) > 2; nflag += fl
            print(f"| {sp[12:]} | {name(c)} | {len(d)} | {m:+.4f} | {se:.4f} | {z:+.2f} | {st.mean(per['neutral_plus']):+.4f} "
                  f"| {st.mean(per['neutral_minus']):+.4f} | {'FLAG' if fl else 'ok'} |")
    print(f"\nFlags: {nflag} of {len(SPECIES) * len(cells)} cell-species combinations (about {0.05 * len(SPECIES) * len(cells):.1f} expected by chance at 2 SE).")

    print("\n### Rule 5: conservation and velocity bound\n")
    d = [r["max_rel_total_drift"] for r in runs.values()]
    print(f"- max relative drift of sum(body)+sum(food), all {len(d)} runs: {max(d):.2e}; runs above 1e-12: {sum(x > 1e-12 for x in d)}")
    for c in cells:
        dd = [r["max_rel_total_drift"] for k, r in runs.items() if k[1] == c]
        ss = [st.mean(r["series"]["sat_frac"][1:]) for k, r in runs.items() if k[1] == c]
        sm = [max(r["series"]["sat_frac"][1:]) for k, r in runs.items() if k[1] == c]
        print(f"  - {name(c)}: max drift {max(dd):.2e}; mean sat_frac {st.mean(ss):.2e}; max single-sample sat_frac {max(sm):.2e}")

    print("\n### Foraging (descriptive): gross food eaten over 30,000 steps and end body mass, median (min-max) over seeds\n")
    print("| species | cell | arm | food eaten | end body | Q_30000 = body(end) - body(0) | end blobs |")
    print("|---|---|---|---|---|---|---|")
    for sp in SPECIES:
        for c in cells:
            for arm in ARMS:
                rs = [runs[(sp, c, arm, s)] for s in range(1, NSEED + 1) if (sp, c, arm, s) in runs]
                if not rs:
                    continue
                fe = [r["food_eaten_total"] for r in rs]; bd = [r["final"]["body"] for r in rs]
                q = [r["final"]["body"] - r["series"]["body"][0] for r in rs]
                nb = [r["final"]["n_blobs"] for r in rs]
                f3 = lambda x: f"{st.median(x):.1f} ({min(x):.1f}-{max(x):.1f})"
                print(f"| {sp[12:]} | {name(c)} | {arm} | {f3(fe)} | {f3(bd)} | {f3(q)} | {st.median(nb):.0f} |")
    print("\nSensing effect on foraging (treat arm, median food eaten, sensing on minus off, same kappa):\n")
    for sp in SPECIES:
        for k in kv:
            on = [r["food_eaten_total"] for kk, r in runs.items() if kk[0] == sp and kk[2] == "treat" and kk[1] == (fsv[-1], k)]
            off = [r["food_eaten_total"] for kk, r in runs.items() if kk[0] == sp and kk[2] == "treat" and kk[1] == (0.0, k)]
            if on and off:
                print(f"- {sp[12:]} kappa {k:g}: {st.median(on):.1f} vs {st.median(off):.1f} ({st.median(on) - st.median(off):+.1f})")

    print("\n### Per-run table (treatment arm)\n")
    print("| species | cell | seed | delta | winner | winner-side final share | hybrid end | blobs | food eaten | end body | drift | wall s |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for sp in SPECIES:
        for c in cells:
            for s in range(1, NSEED + 1):
                r = runs.get((sp, c, "treat", s))
                if r is None:
                    print(f"| {sp[12:]} | {name(c)} | {s} | missing |" + " |" * 8); continue
                dlt = r["delta_share_A"]; w = "+u" if dlt > 0 else "-u"
                sh = r["share_A_end"] if dlt > 0 else 1 - r["share_A_end"]
                f = r["final"]
                print(f"| {sp[12:]} | {name(c)} | {s} | {dlt:+.4f} | {w} | {sh:.3f} | {f['hybrid_frac']:.3f} | {f['n_blobs']} "
                      f"| {r['food_eaten_total']:.1f} | {f['body']:.1f} | {r['max_rel_total_drift']:.1e} | {r['wall_seconds']:.0f} |")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "main"
    if mode == "pilot":
        pilot(Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "outputs/food_sensing_20261116/pilot",
              Path(sys.argv[3]) if len(sys.argv) > 3 else ROOT / "outputs/conditional_blending_20261115")
    else:
        main_summary(Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "outputs/food_sensing_20261116/main")
