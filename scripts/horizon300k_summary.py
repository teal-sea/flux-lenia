"""Apply rules 1-7 of docs/HORIZON-300K-GPU-2026-11-16.md to run JSON (no simulation, standard library only).

Usage: python scripts/horizon300k_summary.py OUTROOT [-o SUMMARY.md] [--n-seeds 50]

OUTROOT holds `*_food1.json` written by scripts/food_selection.py (via scripts/run_batch.py). Any layout works: all
files under OUTROOT are read recursively (flat, or `<SPECIES>_fs<G>_k<kappa>_per_channel/` subdirectories as the
CPU campaign writes them). Cell identity comes from the JSON fields (species, seed, arm, food_sense (absent = 0),
repulsion_kappa), never from file names. Design: 3 species x cells food_sense {0,10} x kappa 3 x seeds 1-50 x 3 arms
= 900 runs. Partial data is fine: every verdict computed on fewer than the expected seeds is labelled PARTIAL.

Scaling to the seeds present: the bars are 40 of 50 (4/5). With n treatment seeds present, need = ceil(0.8 n)
(40 at 50, 4 at 5). The neutral envelope E uses the neutral runs present (100 at full design).
Winner = the lineage whose share rose (sign of delta_share_A); winner share = share_A_end if delta > 0 else 1 - share_A_end.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import statistics as st
import sys
from pathlib import Path

ARMS = ("treat", "neutral_plus", "neutral_minus")
NEUT = ARMS[1:]
TAU = 0.05  # saturation tolerance of campaign_harness_summary.py part 3


# ---------------------------------------------------------------- statistics (stdlib)
def binom_cdf(k, n, p):
    return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(0, k + 1))


def clopper_pearson(k, n, alpha=0.05):
    """Exact binomial interval by bisection on the cdf."""
    if n == 0:
        return float("nan"), float("nan")

    def solve(f):
        lo, hi = 0.0, 1.0
        for _ in range(100):
            mid = (lo + hi) / 2
            if f(mid):
                hi = mid
            else:
                lo = mid
        return (lo + hi) / 2
    lower = 0.0 if k == 0 else solve(lambda p: 1 - binom_cdf(k - 1, n, p) >= alpha / 2)
    upper = 1.0 if k == n else solve(lambda p: binom_cdf(k, n, p) <= alpha / 2)
    return lower, upper


def fisher_exact_two_sided(a, n1, c, n2):
    """Two-sided Fisher exact on [[a, n1-a], [c, n2-c]]: sum of hypergeometric probabilities <= the observed one."""
    n, K = n1 + n2, a + c
    if n == 0:
        return 1.0
    den = math.comb(n, K)
    pmf = lambda x: math.comb(n1, x) * math.comb(n2, K - x) / den
    lo, hi = max(0, K - n2), min(K, n1)
    p0 = pmf(a)
    return min(1.0, sum(p for p in (pmf(x) for x in range(lo, hi + 1)) if p <= p0 * (1 + 1e-9)))


def pct(xs, q):
    xs = sorted(xs)
    k = (len(xs) - 1) * q
    lo, hi = math.floor(k), math.ceil(k)
    return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)


def med(xs):
    return st.median(xs) if xs else float("nan")


def fg(x):
    return f"{x:g}"


# ---------------------------------------------------------------- loading and per-run measures
def find_json(root: Path):
    """All *_food1.json under root, recursive, following symlinked directories."""
    return sorted(Path(d) / n for d, _, ns in os.walk(root, followlinks=True) for n in ns if n.endswith("_food1.json"))


def load(root: Path):
    runs, dup, bad = {}, 0, []
    for f in find_json(root):
        try:
            r = json.loads(f.read_text())
            key = (r["species"], float(r.get("food_sense") or 0.0), float(r["repulsion_kappa"]), r["arm"], int(r["seed"]))
            r["delta_share_A"], r["share_A_end"], r["series"]["share_A"], r["t"]  # presence check
        except Exception as e:  # noqa: BLE001 - partial or foreign file: report, never crash
            bad.append(f"{f.name}: {type(e).__name__} {e}")
            continue
        dup += key in runs
        runs[key] = r
    return runs, dup, bad


def winner_side(r, x):
    return x if r["delta_share_A"] > 0 else 1 - x


def d30(r):
    """Copied verbatim from scripts/campaign_harness_summary.py (part 3): mean share_A over samples with
    27000 < t <= 30000 minus the first sample."""
    s = r["series"]["share_A"]
    xs = [x for t, x in zip(r["t"], s) if 27000 < t <= 30000]
    return st.mean(xs) - s[0]


def classify(x30, x300):
    """Same definitions as campaign_harness_summary.py part 3 (b)."""
    if abs(x300 - x30) <= TAU:
        return "saturated"
    if x300 * x30 < 0:
        return "reverses"
    if abs(x300) > abs(x30):
        return "grows"
    return "shrinks"


def h_at(r, step):
    return r["series"]["hybrid_frac"][r["t"].index(step)] if step in r["t"] else float("nan")


def sel_verdict(treat, E, need):
    out = [r for r in treat if abs(r["delta_share_A"]) > E]
    winners = {"+u" if r["delta_share_A"] > 0 else "-u" for r in out}
    ws = [winner_side(r, r["share_A_end"]) for r in out]
    if len(out) >= need and len(winners) == 1:
        v = "takeover" if med(ws) >= 0.90 else "selection"
    elif len(out) >= need:
        v = "large but inconsistent"
    else:
        v = "no selection detected"
    npos = sum(r["delta_share_A"] > 0 for r in out)
    return {"verdict": v, "n_out": len(out), "plus": npos, "minus": len(out) - npos, "winners": sorted(winners),
            "ws_med": med(ws)}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("outroot")
    ap.add_argument("--n-seeds", type=int, default=50, help="expected seeds per species x cell x arm (default 50)")
    ap.add_argument("-o", "--out")
    a = ap.parse_args()
    n_exp = a.n_seeds
    runs, dup, bad = load(Path(a.outroot))
    out = []
    P = out.append
    species = sorted({k[0] for k in runs})
    cells = sorted({(k[1], k[2]) for k in runs})
    lab = lambda c: f"fs{fg(c[0])}/k{fg(c[1])}"
    short = lambda sp: sp[12:] if sp.startswith("SPECIES_") else sp

    def grp(sp, c, arms):
        return [r for k, r in sorted(runs.items(), key=lambda kv: kv[0][4]) if k[0] == sp and (k[1], k[2]) == c and k[3] in arms]

    P("# Horizon 300k summary\n")
    P(f"Source: `{a.outroot}` (scripts/horizon300k_summary.py; JSON only, no simulation). Rules: docs/HORIZON-300K-GPU-2026-11-16.md "
      f"rules 1-7. Expected per species x cell: {n_exp} treatment, {2 * n_exp} neutral runs. Selection bar scaled to the seeds present: "
      f"need = ceil(0.8 x treatment seeds present) (= {math.ceil(0.8 * n_exp)} at {n_exp}). Any verdict computed on fewer than "
      f"{n_exp} treatment seeds or {2 * n_exp} neutral runs is labelled PARTIAL.\n")
    if not runs:
        P(f"**No `*_food1.json` runs found under `{a.outroot}` (0 of {3 * 2 * 3 * n_exp} expected).**\n")
    P(f"Runs read: **{len(runs)}**; duplicates of one cell/arm/seed (last kept): {dup}; unreadable files skipped: {len(bad)}."
      + ("".join(f"\n- skipped {b}" for b in bad[:5])) + "\n")

    # ---- counts and wall
    P("## Counts present vs expected\n")
    P(f"Expected total 900 (3 species x 2 cells x {n_exp} seeds x 3 arms); present {len(runs)}.\n")
    P("| species | cell | treat | neutral_plus | neutral_minus | total / expected |")
    P("|---|---|---|---|---|---|")
    exp_sp, exp_cells = ["OSCILLIS", "MITOSA", "VAGRANT"], [(0.0, 3.0), (10.0, 3.0)]
    seen_pairs = {(short(sp), c) for sp in species for c in cells}
    rows = sorted(seen_pairs | {(s, c) for s in exp_sp for c in exp_cells}, key=lambda x: (x[0], x[1]))
    full_name = {short(sp): sp for sp in species}
    for sps, c in rows:
        sp = full_name.get(sps)
        ns = [len(grp(sp, c, (arm,))) if sp else 0 for arm in ARMS]
        P(f"| {sps} | {lab(c)} | {ns[0]} / {n_exp} | {ns[1]} / {n_exp} | {ns[2]} / {n_exp} | {sum(ns)} / {3 * n_exp} |")
    w = [r["wall_seconds"] for r in runs.values() if "wall_seconds" in r]
    if w:
        P(f"\nWall seconds per run: min {min(w):.0f}, median {med(w):.0f}, max {max(w):.0f} (n={len(w)}).\n")

    # ---- per-cell analysis
    info = {}
    for sp in species:
        for c in cells:
            tr, ne = grp(sp, c, ("treat",)), grp(sp, c, NEUT)
            if not tr and not ne:
                continue
            info[(sp, c)] = (tr, ne)
    partial = lambda tr, ne: len(tr) < n_exp or len(ne) < 2 * n_exp
    ptag = lambda tr, ne: " **PARTIAL**" if partial(tr, ne) else ""

    P("## Rule 1: takeover frequency\n")
    P("Treatment: winner share at the end >= 0.90, exact (Clopper-Pearson) 95% interval. Neutral: either lineage reaches >= 0.90 at any "
      "sample. Takeover occurs if the treatment count exceeds the neutral count and two-sided Fisher exact p < 0.05 on the 2x2 of counts.\n")
    P("| species | cell | treat takeover | frequency | exact 95% | neutral >= 0.90 at any sample | neutral frequency | Fisher p | takeover occurs | status |")
    P("|---|---|---|---|---|---|---|---|---|---|")
    for (sp, c), (tr, ne) in info.items():
        k = sum(winner_side(r, r["share_A_end"]) >= 0.90 for r in tr)
        m = sum(max(max(x, 1 - x) for x in r["series"]["share_A"]) >= 0.90 for r in ne)
        lo, hi = clopper_pearson(k, len(tr))
        p = fisher_exact_two_sided(k, len(tr), m, len(ne)) if tr and ne else float("nan")
        occ = "YES" if (tr and ne and k > m and p < 0.05) else "no"
        fr = lambda x, n: f"{x / n:.3f}" if n else "n/a"
        P(f"| {short(sp)} | {lab(c)} | {k} of {len(tr)} | {fr(k, len(tr))} | [{lo:.3f}, {hi:.3f}] | {m} of {len(ne)} | {fr(m, len(ne))} "
          f"| {p:.4f} | {occ} | {'PARTIAL' if partial(tr, ne) else 'full'} |")
    P("")

    P("## Rule 2: selection at the final step (standard rule)\n")
    P("E = largest neutral |delta| over the cell's neutral runs (primary); E95 = 95th percentile (secondary, labelled). Selection: at least "
      "`need` treatment seeds outside E with the same winner sign; takeover: selection and the median final share of the winner over the "
      "outside seeds >= 0.90; large but inconsistent: `need`+ outside with both signs.\n")
    P("| species | cell | treat seeds | neutral runs | need | E (max) | outside E | +u / -u | winner median final share | verdict | E95 | outside E95 | verdict at E95 (secondary) | status |")
    P("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    res = {}
    for (sp, c), (tr, ne) in info.items():
        if not tr or not ne:
            P(f"| {short(sp)} | {lab(c)} | {len(tr)} | {len(ne)} | | | | | | cannot compute (treatment or neutral runs missing) | | | | PARTIAL |")
            continue
        need = math.ceil(0.8 * len(tr))
        ad = [abs(r["delta_share_A"]) for r in ne]
        E, E95 = max(ad), pct(ad, 0.95)
        v, v2 = sel_verdict(tr, E, need), sel_verdict(tr, E95, need)
        res[(sp, c)] = v
        wsm = f"{v['ws_med']:.3f}" if v["n_out"] else "-"
        P(f"| {short(sp)} | {lab(c)} | {len(tr)} | {len(ne)} | {need} | {E:.4f} | {v['n_out']} | {v['plus']} / {v['minus']} | {wsm} "
          f"| {v['verdict']} | {E95:.4f} | {v2['n_out']} | {v2['verdict']} | {'PARTIAL' if partial(tr, ne) else 'full'} |")
    P("")

    P("## Rule 3: direction\n")
    P("Winner sign split among treatment seeds outside E (primary), per cell. A cell has a consistent sign only if its rule-2 verdict is "
      "selection or takeover (all outside seeds the same sign, at least `need` of them). Sensing off (fs0) vs sensing on (fs10) per species: "
      "same sign, opposite sign, or no consistent sign.\n")
    P("| species | cell | +u | -u | consistent sign |")
    P("|---|---|---|---|---|")
    sign = {}
    for (sp, c), v in res.items():
        s = v["winners"][0] if v["verdict"] in ("selection", "takeover") else None
        sign[(sp, c)] = s
        P(f"| {short(sp)} | {lab(c)} | {v['plus']} | {v['minus']} | {s or 'none'} |")
    P("\n| species | kappa | sensing off (fs0) | sensing on (fs10) | comparison | status |")
    P("|---|---|---|---|---|---|")
    for sp in species:
        for kap in sorted({c[1] for c in cells}):
            c0, c1 = (0.0, kap), (10.0, kap)
            if (sp, c0) not in info or (sp, c1) not in info:
                if any((sp, c) in info for c in (c0, c1)):
                    P(f"| {short(sp)} | {fg(kap)} | {sign.get((sp, c0)) or "none"} | {sign.get((sp, c1)) or "none"} | cannot compare (one cell has no runs) | PARTIAL |")
                continue
            s0, s1 = sign.get((sp, c0)), sign.get((sp, c1))
            comp = ("same sign" if s0 == s1 else "opposite sign") if (s0 and s1) else "no consistent sign (" + \
                ("off" if not s0 else "") + (" and " if not s0 and not s1 else "") + ("on" if not s1 else "") + ")"
            pp = partial(*info[(sp, c0)]) or partial(*info[(sp, c1)])
            P(f"| {short(sp)} | {fg(kap)} | {s0 or 'none'} | {s1 or 'none'} | {comp} | {'PARTIAL' if pp else 'full'} |")
    P("")

    # ---- rule 4 and 5 per-run measures
    meas = {}
    for k, r in runs.items():
        try:
            x30, x300 = d30(r), r["delta_share_A"]
            meas[k] = {"d30": x30, "d300": x300, "cls": classify(x30, x300), "h30": h_at(r, 30000),
                       "h300": r["final"]["hybrid_frac"]}
        except Exception as e:  # noqa: BLE001
            meas[k] = {"err": f"{type(e).__name__} {e}"}
    steps = sorted({r.get("steps") for r in runs.values()})
    P("## Rule 4: share movement, |delta| at 30,000 vs final step\n")
    P(f"Run lengths present: {steps}. d30 = mean share_A over samples with 27000 < t <= 30000 minus the first sample (campaign_harness_summary.py part 3); "
      f"d300 = delta_share_A. Classes as in campaign_harness_summary.py: saturated if |d300 - d30| <= {TAU}; reverses if opposite sign; grows if |d300| > |d30|; else shrinks.\n")
    P("| species | cell | group | n | saturated | grows | reverses | shrinks | median |d30| | median |d300| | status |")
    P("|---|---|---|---|---|---|---|---|---|---|---|")
    for (sp, c), (tr, ne) in info.items():
        for g, rs in (("treat", tr), ("neutral", ne)):
            ms = [meas[(r["species"], float(r.get("food_sense") or 0.0), float(r["repulsion_kappa"]), r["arm"], int(r["seed"]))] for r in rs]
            ms = [m for m in ms if "cls" in m]
            if not ms:
                continue
            cnt = {k2: sum(m["cls"] == k2 for m in ms) for k2 in ("saturated", "grows", "reverses", "shrinks")}
            P(f"| {short(sp)} | {lab(c)} | {g} | {len(ms)} | {cnt['saturated']} | {cnt['grows']} | {cnt['reverses']} | {cnt['shrinks']} "
              f"| {med([abs(m['d30']) for m in ms]):.3f} | {med([abs(m['d300']) for m in ms]):.3f} "
              f"| {'PARTIAL' if (len(tr) < n_exp if g == 'treat' else len(ne) < 2 * n_exp) else 'full'} |")
    P("")

    P("## Rule 5: distinctness at the final step\n")
    P("Per treatment run: end hybrid fraction vs the same run's own hybrid fraction at step 30,000. Verdict (as specified): holds if the median "
      "end hybrid fraction over treatment runs is at most half the median of the same runs' 30,000-step values. Secondary (the harness's per-run "
      "rule, campaign_harness_summary.py (c)): runs with h_end <= max(0.10, h30 + 0.05).\n")
    P("| species | cell | treat n | median h30 | median h_end | ratio | holds (<= 1/2) | runs holding (harness rule) | status |")
    P("|---|---|---|---|---|---|---|---|---|")
    for (sp, c), (tr, ne) in info.items():
        ms = [meas[(r["species"], float(r.get("food_sense") or 0.0), float(r["repulsion_kappa"]), r["arm"], int(r["seed"]))] for r in tr]
        ms = [m for m in ms if "cls" in m and not math.isnan(m["h30"])]
        if not ms:
            continue
        m30, m3 = med([m["h30"] for m in ms]), med([m["h300"] for m in ms])
        ratio = f"{m3 / m30:.2f}" if m30 > 0 else "n/a"
        hold = sum(m["h300"] <= max(0.10, m["h30"] + 0.05) for m in ms)
        P(f"| {short(sp)} | {lab(c)} | {len(ms)} | {m30:.3f} | {m3:.3f} | {ratio} | {'holds' if m3 <= m30 / 2 else 'does not hold'} | {hold} of {len(ms)} "
          f"| {'PARTIAL' if len(tr) < n_exp else 'full'} |")
    P("")

    P("## Rule 6: neutral-arm sanity\n")
    P("Mean neutral delta within 2 SE of zero per cell; outside is flagged as harness asymmetry (reported, not voiding).\n")
    P("| species | cell | neutral runs | mean delta | SE | mean/SE | flag | status |")
    P("|---|---|---|---|---|---|---|---|")
    for (sp, c), (tr, ne) in info.items():
        d = [r["delta_share_A"] for r in ne]
        if len(d) < 2:
            P(f"| {short(sp)} | {lab(c)} | {len(d)} | | | | too few | PARTIAL |")
            continue
        m, se = st.mean(d), st.stdev(d) / math.sqrt(len(d))
        z = m / se if se > 0 else (0.0 if m == 0 else float("inf"))
        P(f"| {short(sp)} | {lab(c)} | {len(d)} | {m:+.4f} | {se:.4f} | {z:+.2f} | {'FLAGGED (outside 2 SE)' if abs(z) > 2 else 'ok'} "
          f"| {'PARTIAL' if len(ne) < 2 * n_exp else 'full'} |")
    P("")

    P("## Rule 7: conservation (max relative drift of sum(body)+sum(food))\n")
    P("| species | cell | runs | max drift | status |")
    P("|---|---|---|---|---|")
    alld = []
    for (sp, c), (tr, ne) in info.items():
        d = [r["max_rel_total_drift"] for r in tr + ne if "max_rel_total_drift" in r]
        alld += d
        if d:
            P(f"| {short(sp)} | {lab(c)} | {len(d)} | {max(d):.2e} | {'PARTIAL' if partial(tr, ne) else 'full'} |")
    if alld:
        P(f"\nMax over all {len(alld)} runs: **{max(alld):.2e}**.\n")

    # ---- per-run table
    P("## Per-run table\n")
    P("winner = lineage whose share rose; end/peak = winner's share at the last sample / its maximum over samples. h30/h300 = hybrid fraction at step 30,000 / at the end.\n")
    P("| species | cell | arm | seed | A start | d30 | d300 | class | winner share end | winner share peak | h30 | h300 | blobs end | max drift | wall s |")
    P("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for k in sorted(runs, key=lambda k: (k[0], k[1], k[2], ARMS.index(k[3]) if k[3] in ARMS else 9, k[4])):
        r, m = runs[k], meas[k]
        if "cls" not in m:
            P(f"| {short(k[0])} | fs{fg(k[1])}/k{fg(k[2])} | {k[3]} | {k[4]} | unreadable: {m['err']} |")
            continue
        pk = max(winner_side(r, x) for x in r["series"]["share_A"])
        P(f"| {short(k[0])} | fs{fg(k[1])}/k{fg(k[2])} | {k[3]} | {k[4]} | {r['share_A_start']:.3f} | {m['d30']:+.3f} | {m['d300']:+.3f} | {m['cls']} "
          f"| {winner_side(r, r['share_A_end']):.3f} | {pk:.3f} | {m['h30']:.3f} | {m['h300']:.3f} | {r['final'].get('n_blobs', 'n/a')} "
          f"| {r['max_rel_total_drift']:.1e} | {r['wall_seconds']:.0f} |")
    P("")
    text = "\n".join(out)
    if a.out:
        Path(a.out).write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
