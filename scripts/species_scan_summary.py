"""Apply the pre-registered rules of docs/SPECIES-SCAN-2026-11-16.md to GPU-batch run JSON. Prints SUMMARY.md.

Usage: python scripts/species_scan_summary.py OUTROOT [--n-seeds 20] [--expected-species 30] [-o SUMMARY.md]

OUTROOT/<id>/*_food1.json, id = <SPECIES>_fs<G>_k<kappa>_per_channel (as written by scripts/gpu_batch.py through
gpu/manifest.py; run schema = scripts/food_selection.py). Cell (kappa, food_sense) is read from the directory name.
Thresholds scale with n seeds as 4/5 (selection, distinct) and 3/5 (no effect): 16 and 12 of 20 (4 of 5 and 3 of 5 at
5 seeds, which is how the CPU outputs of earlier experiments are used to test this script). Runs only over JSON, no
simulation, pure standard library (no numpy/scipy).
"""
from __future__ import annotations

import argparse
import json
import math
import re
import statistics as st
import sys
from pathlib import Path

ID_RE = re.compile(r"^(SPECIES_\d{3}_[A-Z0-9]+)_fs([0-9.]+)_k([0-9.]+)_per_channel$")
ARMS = ("treat", "neutral_plus", "neutral_minus")
# Pre-registered labelled subgroups (docs/SPECIES-SCAN-2026-11-16.md, "Species caveats")
CADENCE_FIVE = {"SPECIES_008_TENDRIL", "SPECIES_009_ARBORIS", "SPECIES_015_MEDUSA",
                "SPECIES_021_SPIRALIS", "SPECIES_022_TORQUATA"}
ORIGINAL = {"SPECIES_001_OSCILLIS", "SPECIES_002_MITOSA", "SPECIES_003_VAGRANT"}
SUBGROUPS = {"all species": lambda s: True,
             "excluding the five cadence-dependent species": lambda s: s not in CADENCE_FIVE,
             "original three (001-003)": lambda s: s in ORIGINAL}


# ---------- statistics (stdlib) ----------
def binom_cdf(k: int, n: int, p: float) -> float:
    return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(0, k + 1))


def clopper_pearson(k: int, n: int, alpha: float = 0.05) -> tuple[float, float]:
    """Exact binomial interval by bisection on the cdf."""
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


def mcnemar_exact(b: int, c: int) -> float:
    """Two-sided exact p on the discordant pairs (b: on-only, c: off-only), H0 p=1/2."""
    n = b + c
    if n == 0:
        return 1.0
    return min(1.0, 2 * binom_cdf(min(b, c), n, 0.5))


def pct(xs: list[float], q: float) -> float:
    """Linear-interpolation percentile (numpy default)."""
    xs = sorted(xs)
    h = (len(xs) - 1) * q
    lo = int(math.floor(h))
    hi = min(lo + 1, len(xs) - 1)
    return xs[lo] + (xs[hi] - xs[lo]) * (h - lo)


def fmt_g(x: float) -> str:
    return f"{x:g}"


# ---------- loading ----------
def load(root: Path):
    cells: dict[tuple[float, float], dict[str, dict[tuple[str, int], dict]]] = {}
    n_files = 0
    for d in sorted(p for p in root.iterdir() if p.is_dir()):
        m = ID_RE.match(d.name)
        if not m:
            continue
        sp, fs, k = m.group(1), float(m.group(2)), float(m.group(3))
        for f in sorted(d.glob("*_food1.json")):
            r = json.loads(f.read_text())
            cells.setdefault((k, fs), {}).setdefault(sp, {})[(r["arm"], r["seed"])] = r
            n_files += 1
    return cells, n_files


# ---------- per species x cell rules ----------
def share_win(r: dict) -> float:
    return r["share_A_end"] if r["delta_share_A"] > 0 else 1 - r["share_A_end"]


def selection_verdict(runs: dict, n_seeds: int, E: float) -> dict:
    need = -(-4 * n_seeds // 5)
    treat = [runs[("treat", s)] for s in range(1, n_seeds + 1)]
    out = [r for r in treat if abs(r["delta_share_A"]) > E]
    winners = {"+u" if r["delta_share_A"] > 0 else "-u" for r in out}
    ws = [share_win(r) for r in out]
    if len(out) >= need and len(winners) == 1:
        v = "takeover" if st.median(ws) >= 0.90 else "selection"
    elif len(out) >= need:
        v = "large but inconsistent"
    else:
        v = "no selection detected"
    return {"E": E, "n_out": len(out), "winners": sorted(winners), "win_share_median": st.median(ws) if ws else None,
            "verdict": v}


def cell_species(runs: dict, n_seeds: int) -> dict | None:
    need = {(a, s) for a in ARMS for s in range(1, n_seeds + 1)}
    if not need <= set(runs):
        return None
    neutral = [runs[(a, s)] for a in ARMS[1:] for s in range(1, n_seeds + 1)]
    ad = [abs(r["delta_share_A"]) for r in neutral]
    prim = selection_verdict(runs, n_seeds, max(ad))
    sec = selection_verdict(runs, n_seeds, pct(ad, 0.95))
    treat = [runs[("treat", s)] for s in range(1, n_seeds + 1)]
    med_share = st.median(r["share_A_end"] for r in treat)
    return {"prim": prim, "sec": sec,
            "hybrid": [r["final"]["hybrid_frac"] for r in treat],            # by seed
            "hybrid_med": st.median(r["final"]["hybrid_frac"] for r in treat),
            "lineage_win_share": max(med_share, 1 - med_share),                # descriptive, any verdict
            "neutral_delta": [r["delta_share_A"] for r in neutral],
            "drift": max(r["max_rel_total_drift"] for r in runs.values())}


def distinct_verdict(h3: list[float], h0: list[float]) -> dict:
    n = len(h3)
    need, low = -(-4 * n // 5), -(-3 * n // 5)
    below = sum(a < b for a, b in zip(h3, h0))
    m3, m0 = st.median(h3), st.median(h0)
    if m3 <= m0 / 2 and below >= need:
        v = "distinct"
    elif below < low:
        v = "no effect"
    else:
        v = "partial"
    return {"m3": m3, "m0": m0, "below": below, "verdict": v}


def dist(xs: list[float]) -> str:
    if not xs:
        return "n/a"
    return f"min {min(xs):.3f}, Q1 {pct(xs, .25):.3f}, median {pct(xs, .5):.3f}, Q3 {pct(xs, .75):.3f}, max {max(xs):.3f}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("outroot")
    ap.add_argument("--n-seeds", type=int, default=20)
    ap.add_argument("--expected-species", type=int, default=30)
    ap.add_argument("-o", "--out")
    a = ap.parse_args()
    n = a.n_seeds
    cells, n_files = load(Path(a.outroot))
    out: list[str] = []
    P = out.append
    kappas = sorted({k for k, _ in cells})
    fss = sorted({f for _, f in cells})
    cell_keys = [(k, f) for f in fss for k in kappas if (k, f) in cells]
    lab = lambda c: f"k{fmt_g(c[0])}/fs{fmt_g(c[1])}"
    expected_cells = 4
    expected = a.expected_species * expected_cells * n * 3
    need_out, need_dist, low = -(-4 * n // 5), -(-4 * n // 5), -(-3 * n // 5)

    P("# Species scan summary\n")
    P(f"Source: `{a.outroot}`. Rules: docs/SPECIES-SCAN-2026-11-16.md. Seeds per arm: {n}; selection needs "
      f"{need_out} of {n} treatment seeds outside E; distinct needs median ratio <= 1/2 and {need_dist} of {n} seeds below control; "
      f"no effect is fewer than {low}.\n")

    # run counts
    P("## Run counts\n")
    P(f"Expected under the design: {a.expected_species} species x {expected_cells} cells x {n} seeds x 3 arms = {expected}. "
      f"Present: **{n_files}**.\n")
    P("| cell | species with any run | complete species (all arms, all seeds) | runs |")
    P("|---|---|---|---|")
    full: dict[tuple, dict[str, dict]] = {}
    for c in cell_keys:
        full[c] = {}
        for sp, runs in sorted(cells[c].items()):
            r = cell_species(runs, n)
            if r is not None:
                full[c][sp] = r
        P(f"| {lab(c)} | {len(cells[c])} | {len(full[c])} | {sum(len(v) for v in cells[c].values())} |")
    P("")

    # per species x cell verdict table
    P("## Per species x cell: selection (primary E = max |delta| over the cell's neutral runs)\n")
    P("Cell entry: verdict (treatment seeds outside E of " + str(n) + "; E; winner(s); median final share of the winner "
      "over the outside seeds). `incomplete` = the cell lacks runs.\n")
    species = sorted({sp for c in cell_keys for sp in cells[c]})
    P("| species | " + " | ".join(lab(c) for c in cell_keys) + " |")
    P("|---|" + "---|" * len(cell_keys))
    for sp in species:
        row = []
        for c in cell_keys:
            r = full[c].get(sp)
            if r is None:
                row.append("incomplete")
                continue
            p = r["prim"]
            ws = f"{p['win_share_median']:.2f}" if p["win_share_median"] is not None else "-"
            row.append(f"{p['verdict']} ({p['n_out']}/{n}; E {p['E']:.3f}; {','.join(p['winners']) or '-'}; {ws})")
        P(f"| {sp[12:]} | " + " | ".join(row) + " |")
    P("\nSecondary (labelled): same rule with E = 95th percentile of the neutral |delta| (linear interpolation).\n")
    P("| species | " + " | ".join(lab(c) for c in cell_keys) + " |")
    P("|---|" + "---|" * len(cell_keys))
    for sp in species:
        row = []
        for c in cell_keys:
            r = full[c].get(sp)
            row.append("incomplete" if r is None else f"{r['sec']['verdict']} ({r['sec']['n_out']}/{n}; E {r['sec']['E']:.3f})")
        P(f"| {sp[12:]} | " + " | ".join(row) + " |")
    P("")

    # aggregates
    P("## Species-level aggregate: frequency of selection or takeover (primary E)\n")
    sel = lambda c, sp: full[c][sp]["prim"]["verdict"] in ("selection", "takeover")
    for gname, gf in SUBGROUPS.items():
        P(f"### {gname}\n")
        P("| cell | species complete | selection or takeover | frequency | exact 95% interval | takeover only | large but inconsistent |")
        P("|---|---|---|---|---|---|---|")
        for c in cell_keys:
            sps = [s for s in full[c] if gf(s)]
            k = sum(sel(c, s) for s in sps)
            lo, hi = clopper_pearson(k, len(sps)) if sps else (float("nan"),) * 2
            tk = sum(full[c][s]["prim"]["verdict"] == "takeover" for s in sps)
            li = sum(full[c][s]["prim"]["verdict"] == "large but inconsistent" for s in sps)
            P(f"| {lab(c)} | {len(sps)} | {k} | {k / len(sps) if sps else float('nan'):.3f} | [{lo:.3f}, {hi:.3f}] | {tk} | {li} |")
        P("")
        P("Paired test, food sensing on vs off at the same kappa (McNemar exact, two-sided, on species complete in both cells): "
          "the frequency counts as changed if on > off and p < 0.05.\n")
        P("| kappa | fs off -> fs on | pairs | on only | off only | count off | count on | p | frequency of selection changes |")
        P("|---|---|---|---|---|---|---|---|---|")
        for k in kappas:
            for f0 in fss:
                for f1 in fss:
                    if not (f0 == 0 and f1 > 0 and (k, f0) in full and (k, f1) in full):
                        continue
                    sps = [s for s in full[(k, f0)] if s in full[(k, f1)] and gf(s)]
                    b = sum(sel((k, f1), s) and not sel((k, f0), s) for s in sps)
                    cc = sum(sel((k, f0), s) and not sel((k, f1), s) for s in sps)
                    p = mcnemar_exact(b, cc)
                    c0, c1 = sum(sel((k, f0), s) for s in sps), sum(sel((k, f1), s) for s in sps)
                    P(f"| {fmt_g(k)} | {fmt_g(f0)} -> {fmt_g(f1)} | {len(sps)} | {b} | {cc} | {c0} | {c1} | {p:.4f} "
                      f"| {'YES' if (c1 > c0 and p < 0.05) else 'no'} |")
        P("")

    # distribution of winner share and hybrid fraction
    P("## Distribution across species (all complete species per cell)\n")
    P("Winner's median final share = for each species, the larger lineage's median final share over its treatment seeds "
      "(descriptive, defined whatever the verdict). End hybrid fraction = per-species median over treatment seeds.\n")
    P("| cell | species | winner's median final share | end hybrid fraction |")
    P("|---|---|---|---|")
    for c in cell_keys:
        P(f"| {lab(c)} | {len(full[c])} | {dist([r['lineage_win_share'] for r in full[c].values()])} "
          f"| {dist([r['hybrid_med'] for r in full[c].values()])} |")
    P("")

    # distinctness
    P("## Lineage distinctness: kappa 3 vs kappa 0, same food sensing, treatment arm\n")
    k0s, k3s = 0.0, 3.0
    for f in fss:
        if (k0s, f) not in full or (k3s, f) not in full:
            continue
        P(f"### fs {fmt_g(f)}\n")
        P("| species | median hybrid k0 | median hybrid k3 | ratio | seeds k3 < k0 | verdict |")
        P("|---|---|---|---|---|---|")
        res = {}
        for sp in sorted(s for s in full[(k0s, f)] if s in full[(k3s, f)]):
            d = distinct_verdict(full[(k3s, f)][sp]["hybrid"], full[(k0s, f)][sp]["hybrid"])
            res[sp] = d["verdict"]
            ratio = f"{d['m3'] / d['m0']:.2f}" if d["m0"] > 0 else "n/a"
            P(f"| {sp[12:]} | {d['m0']:.3f} | {d['m3']:.3f} | {ratio} | {d['below']} of {n} | {d['verdict']} |")
        cnt = {v: sum(x == v for x in res.values()) for v in ("distinct", "partial", "no effect")}
        k = cnt["distinct"]
        lo, hi = clopper_pearson(k, len(res)) if res else (float("nan"),) * 2
        P(f"\nDistinct in {k} of {len(res)} species ({k / len(res) if res else float('nan'):.3f}, exact 95% [{lo:.3f}, {hi:.3f}]); "
          f"partial {cnt['partial']}; no effect {cnt['no effect']}.\n")
        globals().setdefault("_DIST", {})[f] = res
    dres = globals().get("_DIST", {})
    for f1 in fss:
        if f1 > 0 and 0.0 in dres and f1 in dres:
            P(f"### Distinctness frequency, fs 0 vs fs {fmt_g(f1)} (McNemar exact, species with a verdict at both)\n")
            P("| subgroup | pairs | distinct fs on only | distinct fs off only | distinct off | distinct on | p | changes |")
            P("|---|---|---|---|---|---|---|---|")
            for gname, gf in SUBGROUPS.items():
                sps = [s for s in dres[0.0] if s in dres[f1] and gf(s)]
                d0 = lambda s: dres[0.0][s] == "distinct"
                d1 = lambda s: dres[f1][s] == "distinct"
                b = sum(d1(s) and not d0(s) for s in sps)
                cc = sum(d0(s) and not d1(s) for s in sps)
                p = mcnemar_exact(b, cc)
                c0, c1 = sum(d0(s) for s in sps), sum(d1(s) for s in sps)
                P(f"| {gname} | {len(sps)} | {b} | {cc} | {c0} | {c1} | {p:.4f} | {'YES' if (c1 > c0 and p < 0.05) else 'no'} |")
            P("")

    # neutral sanity
    P("## Neutral-arm sanity (mean neutral delta within 2 SE of zero; else flagged as harness asymmetry, not voiding)\n")
    P("| cell | species | neutral runs | species flagged | max |mean/SE| over species | pooled mean delta | pooled SE |")
    P("|---|---|---|---|---|---|---|---|")
    flagged_list = []
    for c in cell_keys:
        flagged, zmax, pooled = 0, 0.0, []
        for sp, r in sorted(full[c].items()):
            d = r["neutral_delta"]
            m, se = st.mean(d), st.stdev(d) / math.sqrt(len(d))
            z = m / se if se > 0 else (0.0 if m == 0 else float("inf"))
            zmax = max(zmax, abs(z))
            if abs(z) > 2:
                flagged += 1
                flagged_list.append(f"{lab(c)} {sp[12:]} (mean {m:+.4f}, z {z:+.2f})")
            pooled += d
        if pooled:
            pm, pse = st.mean(pooled), st.stdev(pooled) / math.sqrt(len(pooled))
            P(f"| {lab(c)} | {len(full[c])} | {len(pooled)} | {flagged} | {zmax:.2f} | {pm:+.5f} | {pse:.5f} |")
    P("\nFlagged species-cells (about 5% of tests are expected by chance): " + ("; ".join(flagged_list) if flagged_list else "none") + "\n")

    # conservation
    P("## Conservation: max relative drift of sum(body)+sum(food)\n")
    P("| cell | max drift over runs |")
    P("|---|---|")
    for c in cell_keys:
        d = max(r["max_rel_total_drift"] for v in cells[c].values() for r in v.values())
        P(f"| {lab(c)} | {d:.2e} |")
    P("")
    text = "\n".join(out)
    if a.out:
        Path(a.out).write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
