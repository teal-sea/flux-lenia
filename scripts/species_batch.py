#!/usr/bin/env python3
"""Batch species hunt (campaign 2026-11-16, part C). Thin wrapper over scripts/discover.py.

discover.py's `curate` renumbers species from 001 and overwrites hunts/SPECIES_INDEX.json, so it cannot
add species to an existing repo. This script reuses its functions unchanged (sample_candidate, evaluate,
phototaxis_probe, record_species, write_report): no gate, threshold or engine file is touched.

  screen  --base B --n N --shard I --nshards K --outdir D
      seeds B..B+N-1 with seed % K == I; one JSON line per seed (record + wall_s) in D/shard_B_I.jsonl.
  promote --seed S --idx I --name NAME [--caveat-dir D]
      re-run seed S as discover's curate does (phototaxis probe, 900-step recording, report, genome JSON),
      write hunts/SPECIES_III_NAME.md, outputs/species/SPECIES_III_NAME_genome.json, outputs/ media,
      and D/SPECIES_III_NAME_caveats.json (measured flags for the ledger).
Passing rule (exactly discover.py curate's): all four viability gates pass AND n_reproduction > 0.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import discover as dc                     # noqa: E402
from engine import neural_field as nf     # noqa: E402
from engine import novelty_oracle as no   # noqa: E402


def cmd_screen(a) -> int:
    out = Path(a.outdir)
    out.mkdir(parents=True, exist_ok=True)
    cfg = nf.Config(advect_genome=False)
    seeds = [s for s in range(a.base, a.base + a.n) if s % a.nshards == a.shard]
    f = out / f"shard_{a.base}_{a.shard}.jsonl"
    with f.open("a") as fh:
        for s in seeds:
            t0 = time.time()
            try:
                rec, *_ = dc.evaluate(dc.sample_candidate(s, cfg))
            except Exception as e:                       # logged, never swallowed
                rec = {"seed": s, "viable": False, "error": repr(e), "score": -1.0, "n_reproduction": 0}
            rec["wall_s"] = time.time() - t0
            fh.write(json.dumps(rec, default=float) + "\n")
            fh.flush()
            print(f"seed={s} viable={rec.get('viable')} repro={rec.get('n_reproduction')}"
                  f"/{rec.get('n_fission_raw')} wall={rec['wall_s']:.1f}s", flush=True)
    print(f"SHARD_DONE {a.shard}", flush=True)
    return 0


def cmd_promote(a) -> int:
    cfg = nf.Config(advect_genome=False)
    c = dc.sample_candidate(a.seed, cfg)
    rec, *_ = dc.evaluate(c)
    if not (rec["viable"] and rec["n_reproduction"] > 0):
        print(f"seed {a.seed} no longer passes on re-evaluation: viable={rec['viable']} "
              f"repro={rec['n_reproduction']}")
        return 2
    rec["origin"] = "random"
    tag = f"SPECIES_{a.idx:03d}_{a.name}"
    photo = dc.phototaxis_probe(c)
    out = dc.record_species(c, tag)
    tracker = out["tracker"]
    anomalies = [photo, no.detect_pursuit(tracker), no.detect_cyclic_locomotion(tracker)]
    world = nf.World(c.cfg, c.spec, c.params, seed=c.seed)
    gpath = dc.SPECIES_DIR / f"{tag}_genome.json"
    gpath.write_text(world.genome_json(a.name, {
        "seed": c.seed, "origin": rec["origin"], "spawn_radius": c.spawn_radius,
        "spawn_peak": c.spawn_peak, "verified": {x.kind: x.established for x in anomalies}}))
    rpath = dc.write_report(a.idx, a.name, rec, anomalies, tracker, out["media"], gpath)

    strict = tracker.reproduction_events(min_child_life=6)
    raw = tracker.reproduction_events(min_child_life=6, min_mass_frac=0.0)
    fracs = [f for e in strict for f in e.get("child_mass_frac", [])]
    cyc = next(x for x in anomalies if x.kind == "cyclic_locomotion")
    cav = {
        "species": a.name, "idx": a.idx, "seed": a.seed,
        "screen": {"n_reproduction": rec["n_reproduction"], "n_fission_raw": rec["n_fission_raw"],
                   "best_child_mass_frac": rec["best_child_mass_frac"], "n_blobs_final": rec["n_blobs_final"],
                   "concentration_final": rec["concentration_final"], "occupancy_final": rec["occupancy_final"],
                   "activity": rec["activity"], "max_generation": rec["max_generation"],
                   "n_organisms": rec["n_organisms"], "n_survivors": rec["n_survivors"]},
        "recording": {"divisions": len(strict), "raw_fissions": len(raw),
                      "strict_le_raw": len(strict) <= len(raw), "child_frac_min": min(fracs, default=None),
                      "child_frac_median": float(np.median(fracs)) if fracs else None},
        "flags": [],
    }
    fl = cav["flags"]
    if rec["n_reproduction"] == 1:
        fl.append("single_division_in_screen: one qualifying fission carries the whole verdict")
    if len(strict) == 0:
        fl.append("no_division_in_recording_run: screen verdict (12-frame cadence) did not reproduce at 6-frame cadence (FINDINGS 5)")
    if len(strict) > len(raw):
        fl.append("strict_gt_raw: impossible count, tracker inconsistency (FINDINGS 2.3)")
    if rec["n_fission_raw"] >= 5 * max(rec["n_reproduction"], 1):
        fl.append(f"debris_dominated: {rec['n_reproduction']} divisions among {rec['n_fission_raw']} raw fissions (FINDINGS 2.1)")
    if rec["n_organisms"] >= 60:
        fl.append(f"fragmenting: {rec['n_organisms']} organisms tracked (shedding/merging churn, FINDINGS 2.1/2.5)")
    if rec["n_blobs_final"] >= 6:
        fl.append(f"many_bodies_final: {rec['n_blobs_final']} bodies at end of screen run")
    if cyc.established:
        fl.append(f"cyclic_locomotion_flagged: {cyc.detail}")
    (Path(a.caveat_dir)).mkdir(parents=True, exist_ok=True)
    (Path(a.caveat_dir) / f"{tag}_caveats.json").write_text(json.dumps(cav, indent=2, default=float))
    print(f"PROMOTED {tag} seed={a.seed} report={rpath.name} flags={len(fl)}")
    return 0


def main() -> int:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("screen")
    s.add_argument("--base", type=int, required=True)
    s.add_argument("--n", type=int, required=True)
    s.add_argument("--shard", type=int, default=0)
    s.add_argument("--nshards", type=int, default=1)
    s.add_argument("--outdir", required=True)
    s.set_defaults(func=cmd_screen)
    q = sub.add_parser("promote")
    q.add_argument("--seed", type=int, required=True)
    q.add_argument("--idx", type=int, required=True)
    q.add_argument("--name", required=True)
    q.add_argument("--caveat-dir", default=str(ROOT / "hunts" / "_screen_campC"))
    q.set_defaults(func=cmd_promote)
    a = p.parse_args()
    return a.func(a)


if __name__ == "__main__":
    raise SystemExit(main())
