#!/usr/bin/env python3
"""Pilot 2 (GPU gain ladder) verdicts by the rule in docs/GPU-PILOT2-GAIN-LADDER-2026-11-16.md.

  python scripts/pilot2_gain_ladder_summary.py [PILOT_ROOT] [REF_ROOT] [-o SUMMARY.md]

PILOT_ROOT: outputs/pilot2_gain_ladder/<SPECIES>_fs<G>_k3_per_channel/*_food1.json (10,000-step runs).
REF_ROOT:   outputs/food_sensing_2x2_gpu/<SPECIES>_fs0_k3_per_channel/*_food1.json (30,000-step runs,
            read at step 10,000; treat arm only, as in the pilot).

Q = body(10,000) - body(0) per run. Per species and gain:
  changes foraging: |median Q(g) - median Q(0)| > R(0) (= max - min of Q(0) over the reference seeds)
                    AND the interquartile ranges of Q(g) and Q(0) do not overlap
  clean:            every sample's velocity saturation fraction < 1e-2 in every run
                    AND max relative drift of sum(body)+sum(food) < 1e-12 in every run
  qualifies:        changes foraging in >= 2 of 3 species AND clean in all 3
Recommendation = smallest qualifying gain; otherwise the failure mode (saturation vs no change).
Standard library only.
"""
import glob
import json
import os
import re
import statistics as st
import sys

STEP = 10_000
SAT_LIMIT = 1e-2
DRIFT_LIMIT = 1e-12


def q_at(d, step):
    s = d["series"]["body"]
    se = int(d["sample_every"])
    n_expected = int(d["steps"]) // se + 1
    if len(s) == n_expected:          # series[0] is step 0
        i = step // se
    elif len(s) == n_expected - 1:    # series[0] is step sample_every
        i = step // se - 1
    else:
        raise SystemExit(f"unexpected series length {len(s)} for steps {d['steps']} every {se}")
    return s[i] - s[0], len(s), i


def load_runs(root, arm="treat"):
    out = {}
    for cell in sorted(glob.glob(os.path.join(root, "*_per_channel"))):
        m = re.search(r"(SPECIES_\d+_[A-Z]+)_fs([0-9.]+)_k([0-9.]+)_per_channel$", cell)
        if not m:
            continue
        sp, fs, k = m.group(1), float(m.group(2)), float(m.group(3))
        runs = []
        for f in sorted(glob.glob(os.path.join(cell, "*_food1.json"))):
            d = json.load(open(f))
            if d["arm"] != arm:
                continue
            q, n, i = q_at(d, STEP)
            runs.append({"seed": d["seed"], "Q": q, "max_sat": max(d["series"]["sat_frac"]),
                         "drift": d["max_rel_total_drift"], "series_len": n, "idx": i})
        if runs:
            out[(sp, fs, k)] = runs
    return out


def iqr(xs):
    s = sorted(xs)
    n = len(s)
    return s[n // 4], s[(3 * n) // 4]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    out_path = sys.argv[sys.argv.index("-o") + 1] if "-o" in sys.argv else None
    pilot_root = args[0] if len(args) > 0 else "outputs/pilot2_gain_ladder"
    ref_root = args[1] if len(args) > 1 else "outputs/food_sensing_2x2_gpu"
    pilot = load_runs(pilot_root)
    ref = load_runs(ref_root)
    species = sorted({k[0] for k in pilot})
    gains = sorted({k[1] for k in pilot})
    lines = ["# Pilot 2 gain ladder: verdicts", "",
             f"pilot root `{pilot_root}`, reference root `{ref_root}` (food_sense 0, kappa 3, treat, read at step {STEP:,})", "",
             "| species | gain | n | median Q(g) | IQR Q(g) | median Q(0) | IQR Q(0) | R(0) | n ref | max sat | max drift | changes foraging | clean |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    per_gain = {g: {"changes": 0, "clean": 0, "species": 0, "sat_fail": 0} for g in gains}
    for sp in species:
        r = ref.get((sp, 0.0, 3.0))
        if not r:
            lines.append(f"| {sp} | - | - | - | - | - | - | - | 0 | - | - | NO REFERENCE PULLED | - |")
            continue
        q0 = [x["Q"] for x in r]
        m0, (lo0, hi0), R0 = st.median(q0), iqr(q0), max(q0) - min(q0)
        for g in gains:
            p = pilot.get((sp, g, 3.0))
            if not p:
                continue
            qg = [x["Q"] for x in p]
            mg, (log_, hig) = st.median(qg), iqr(qg)
            changes = abs(mg - m0) > R0 and (hig < lo0 or log_ > hi0)
            max_sat = max(x["max_sat"] for x in p)
            max_drift = max(x["drift"] for x in p)
            clean = max_sat < SAT_LIMIT and max_drift < DRIFT_LIMIT
            per_gain[g]["species"] += 1
            per_gain[g]["changes"] += int(changes)
            per_gain[g]["clean"] += int(clean)
            per_gain[g]["sat_fail"] += int(max_sat >= SAT_LIMIT)
            lines.append(f"| {sp} | {g:g} | {len(qg)} | {mg:.2f} | [{log_:.2f}, {hig:.2f}] | {m0:.2f} | [{lo0:.2f}, {hi0:.2f}] | {R0:.2f} | {len(q0)} | {max_sat:.2e} | {max_drift:.1e} | {'YES' if changes else 'no'} | {'yes' if clean else 'NO'} |")
    lines += ["", "| gain | species measured | changes foraging in | clean in | qualifies |", "|---|---|---|---|---|"]
    qualifying = []
    for g in gains:
        pg = per_gain[g]
        q = pg["species"] == 3 and pg["changes"] >= 2 and pg["clean"] == 3
        if q:
            qualifying.append(g)
        lines.append(f"| {g:g} | {pg['species']} | {pg['changes']} of {pg['species']} | {pg['clean']} of {pg['species']} | {'YES' if q else 'no'} |")
    lines.append("")
    if qualifying:
        lines.append(f"**Recommendation: food_sense = {min(qualifying):g}** (smallest qualifying gain; qualifying: {', '.join(f'{g:g}' for g in qualifying)}).")
    else:
        sat_any = any(per_gain[g]["sat_fail"] for g in gains)
        change_any = any(per_gain[g]["changes"] for g in gains)
        if not change_any:
            lines.append("**No gain qualifies: nothing changes foraging at any gain (prediction iii, no coupling).** Next design per the doc: a food-coupled hunt gate.")
        elif sat_any:
            lines.append("**No gain qualifies: the gains that change foraging also saturate (prediction ii, route capped).** Next design per the doc: a normalised food input.")
        else:
            lines.append("**No gain qualifies** (changes in fewer than 2 of 3 species at every clean gain).")
    text = "\n".join(lines) + "\n"
    print(text)
    if out_path:
        with open(out_path, "w") as f:
            f.write(text)


if __name__ == "__main__":
    main()
