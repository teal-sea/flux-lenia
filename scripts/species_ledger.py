#!/usr/bin/env python3
"""Summaries over JSON for campaign 2026-11-16 (light; no simulation).

  ledger  SCREEN_DIR                 per-seed pass/reject table, reject histogram, passes (ascending seed)
  validate                           load every new species JSON with nf.World.from_json (the loader food_selection uses)
"""
from __future__ import annotations

import glob
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(d):
    recs = {}
    for f in sorted(glob.glob(str(Path(d) / "shard_*.jsonl"))):
        for line in open(f):
            if line.strip():
                r = json.loads(line)
                recs[r["seed"]] = r
    return dict(sorted(recs.items()))


def verdict(r):
    """('PASS'|'REJECT', [reasons]); reasons are the failing gates, 'no_division', or 'error'."""
    if "error" in r:
        return "REJECT", ["error"]
    fails = [g["name"] for g in r["gates"] if not g["passed"]]
    if fails:
        return "REJECT", fails
    if r["n_reproduction"] <= 0:
        return "REJECT", ["no_division"]
    return "PASS", []


def margins(r):
    if "error" in r:
        return r["error"][:60]
    g = {x["name"]: x for x in r["gates"]}
    return (f"drift={g['mass_conservation']['value']:.2e} conc={g['non_triviality']['value']:.1f} "
            f"surv={g['persistence']['value']:.0f} act={g['activity']['value']:.3f} "
            f"div={r['n_reproduction']}/{r['n_fission_raw']}raw best_child={r['best_child_mass_frac']:.2f}")


def cmd_ledger(d):
    recs = load(d)
    hist = Counter()
    rows, passes = [], []
    for s, r in recs.items():
        v, why = verdict(r)
        for w in why:
            hist[w] += 1
        if v == "PASS":
            passes.append(s)
        rows.append(f"| {s} | {v} | {', '.join(why) or '-'} | {margins(r)} | {r.get('wall_s', 0):.1f} |")
    print(f"ids run: {len(recs)} (seeds {min(recs)}..{max(recs)}, contiguous={len(recs) == max(recs) - min(recs) + 1})")
    print(f"passes: {len(passes)}  seeds {passes}")
    print("reject reasons (a seed can fail several gates):", dict(hist))
    print(f"mean wall per seed: {sum(r.get('wall_s', 0) for r in recs.values()) / len(recs):.1f}s")
    print("\n| seed | verdict | failed gate(s) | margins | wall s |\n| --- | --- | --- | --- | --- |")
    print("\n".join(rows))
    return 0


def cmd_validate():
    import numpy as np
    from engine import neural_field as nf
    bad = 0
    for f in sorted(glob.glob(str(ROOT / "outputs/species/SPECIES_*_genome.json"))):
        data = json.loads(Path(f).read_text())
        try:
            w = nf.World.from_json(data, seed=1)
            ok = np.isfinite(np.asarray(w.A)).all()
            print(f"OK   {Path(f).name} keys={sorted(data)}" if ok else f"BAD {f}")
        except Exception as e:
            bad += 1
            print(f"FAIL {Path(f).name}: {e!r}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT))
    if sys.argv[1] == "ledger":
        raise SystemExit(cmd_ledger(sys.argv[2]))
    raise SystemExit(cmd_validate())
