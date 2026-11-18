#!/usr/bin/env python3
"""Shard the remaining flux-lenia horizon + species-scan work across the InstaBox L4 GPU fleet.

Reads the CPU-collected JSONs already in outputs/ (the done-set), computes the remaining
(species, cell, seed) units, and greedily assigns them to N boxes balanced by run-steps
(horizon runs are 10x longer than scan runs). Scan (species,cell) batches are kept whole so
the vmap batch stays near 60; horizon batches are split into ~10-seed chunks. Emits one
shard TSV per box (id<TAB>outrel<TAB>runs<TAB>gpu_batch-args) for scripts/run_shard.sh.

Run AFTER stopping the CPU boxes and collecting their latest JSONs, so the done-set is frozen.
  python scripts/shard_gpu_campaign.py --boxes 20 --outdir campaign_gpu/shards
"""
from __future__ import annotations
import argparse, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARMS = "treat,neutral_plus,neutral_minus"
NARM = 3

HORIZON = dict(exp="horizon300k_20261117", steps=300000, sample=1000, frame=50000,
               seeds=list(range(1, 51)),
               species=["SPECIES_001_OSCILLIS", "SPECIES_002_MITOSA", "SPECIES_003_VAGRANT"],
               cells=[(3, 0), (3, 10)])
SCAN = dict(exp="species_scan_20261117", steps=30000, sample=100, frame=15000,
            seeds=list(range(1, 21)), cells=[(0, 0), (3, 0), (0, 10), (3, 10)])


def scan_species():
    sp = sorted({p.name[:-len("_genome.json")] for p in (ROOT / "outputs" / "species").glob("*_genome.json")})
    return sp


def cid(species, kappa, fs):
    return f"{species}_fs{fs}_k{kappa}_per_channel"


def done_seeds(exp, species, kappa, fs):
    # A seed is done only when ALL arms have a JSON; a partial seed stays in the shard and
    # gpu_batch's per-(seed,arm) skip-existing fills only the missing arms.
    d = ROOT / "outputs" / exp / cid(species, kappa, fs)
    arms = {}
    if d.exists():
        for p in d.glob(f"{species}_s*_food1.json"):
            m = re.match(rf"{re.escape(species)}_s(\d+)_(.+)_food1\.json$", p.name)
            if m:
                arms.setdefault(int(m.group(1)), set()).add(m.group(2))
    return {s for s, a in arms.items() if len(a) >= NARM}


def fmt(x):
    return str(int(x)) if float(x) == int(float(x)) else repr(float(x))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--boxes", type=int, default=20)
    ap.add_argument("--outdir", default="campaign_gpu/shards")
    ap.add_argument("--horizon-chunk", type=int, default=10)
    a = ap.parse_args()
    outdir = ROOT / a.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    # Build units: (weight_run_steps, exp, species, kappa, fs, [seeds])
    units = []
    # horizon: split remaining seeds into chunks
    for sp in HORIZON["species"]:
        for (k, f) in HORIZON["cells"]:
            rem = [s for s in HORIZON["seeds"] if s not in done_seeds(HORIZON["exp"], sp, k, f)]
            for i in range(0, len(rem), a.horizon_chunk):
                chunk = rem[i:i + a.horizon_chunk]
                units.append((len(chunk) * NARM * HORIZON["steps"], HORIZON["exp"], sp, k, f, chunk))
    # scan: whole (species,cell) batches of remaining seeds
    for sp in scan_species():
        for (k, f) in SCAN["cells"]:
            rem = [s for s in SCAN["seeds"] if s not in done_seeds(SCAN["exp"], sp, k, f)]
            if rem:
                units.append((len(rem) * NARM * SCAN["steps"], SCAN["exp"], sp, k, f, rem))

    # greedy least-loaded assignment by run-steps
    load = [0] * a.boxes
    box_units = [[] for _ in range(a.boxes)]
    for u in sorted(units, key=lambda x: -x[0]):
        b = min(range(a.boxes), key=lambda i: load[i])
        box_units[b].append(u)
        load[b] += u[0]

    total_runs = 0
    for b in range(a.boxes):
        lines = []
        # group by (exp,species,k,f) to merge seed lists into one call
        groups = {}
        for (w, exp, sp, k, f, seeds) in box_units[b]:
            groups.setdefault((exp, sp, k, f), []).extend(seeds)
        for (exp, sp, k, f), seeds in sorted(groups.items()):
            seeds = sorted(set(seeds))
            c = cid(sp, k, f)
            runs = len(seeds) * NARM
            total_runs += runs
            seedstr = ",".join(map(str, seeds))
            steps = HORIZON["steps"] if exp == HORIZON["exp"] else SCAN["steps"]
            sample = HORIZON["sample"] if exp == HORIZON["exp"] else SCAN["sample"]
            frame = HORIZON["frame"] if exp == HORIZON["exp"] else SCAN["frame"]
            args = (f"--species {sp} --arms {ARMS} --seeds {seedstr} --steps {steps} "
                    f"--sample-every {sample} --frame-every {frame} --transport per_channel "
                    f"--kappa {fmt(k)} --food-sense {fmt(f)} --food 1 --batch 64")
            lines.append(f"{c}\t{exp}/{c}\t{runs}\t{args}")
        (outdir / f"box{b+1:02d}.tsv").write_text("\n".join(lines) + "\n")

    tot_steps = sum(load)
    print(f"units={len(units)} total_remaining_runs={total_runs} total_run_steps={tot_steps:,}")
    print(f"boxes={a.boxes} min_load={min(load):,} max_load={max(load):,} "
          f"projected_wall_h_at_1.311ms={max(load)*1.311/1000/3600:.2f}")
    for b in range(a.boxes):
        nr = sum(len(s) for (_, _, _, _, _, s) in box_units[b]) * NARM
        print(f"  box{b+1:02d}: {len(box_units[b])} batches, {nr} runs, {load[b]:,} run-steps")


if __name__ == "__main__":
    main()