"""Job lists for the CPU campaign (docs/HORIZON-300K-GPU-2026-11-16.md, docs/SPECIES-SCAN-2026-11-16.md, execution notes).

  python scripts/make_cpu_jobs.py OUTDIR [--G 10]

Job line for scripts/run_batch.py: SPECIES SEED ARM FOOD KAPPA SUBDIR FOOD_SENSE, SUBDIR = the id gpu/manifest.py
gives the (species, cell): <species>_fs<food_sense>_k<kappa>_per_channel (what scripts/species_scan_summary.py reads).
Jobs are ordered seed by seed. Writes horizon_jobs.txt (900), scan_vultr2_jobs.txt, scan_ib_jobs.txt, scan_all_jobs.txt.
Scan split: InstaBox gets the even seeds 2..16 (8 seeds, 2,880 runs), Vultr box 2 the other 12 seeds (4,320 runs):
the InstaBox side is sized by the 170 box-hour cap, not 50/50.
"""
import argparse
from pathlib import Path

ARMS = ["treat", "neutral_plus", "neutral_minus"]
ROOT = Path(__file__).resolve().parents[1]


def sid(sp, fs, k):
    return f"{sp}_fs{fs}_k{k}_per_channel"


def line(sp, seed, arm, k, fs):
    return f"{sp} {seed} {arm} 1 {k} {sid(sp, fs, k)} {fs}"


ap = argparse.ArgumentParser()
ap.add_argument("out"); ap.add_argument("--G", type=int, default=10)
a = ap.parse_args()
out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
horizon_species = ["SPECIES_001_OSCILLIS", "SPECIES_002_MITOSA", "SPECIES_003_VAGRANT"]
H = [line(sp, s, arm, 3, fs) for s in range(1, 51) for sp in horizon_species for fs in (0, 10) for arm in ARMS]
species = sorted(p.name[:-len("_genome.json")] for p in (ROOT / "outputs/species").glob("*_genome.json"))
cells = [(0, 0), (3, 0), (0, a.G), (3, a.G)]           # (kappa, food_sense)
S = {s: [line(sp, s, arm, k, fs) for sp in species for (k, fs) in cells for arm in ARMS] for s in range(1, 21)}
ib_seeds = [2, 4, 6, 8, 10, 12, 14, 16]
ib = [j for s in ib_seeds for j in S[s]]
v2 = [j for s in range(1, 21) if s not in ib_seeds for j in S[s]]
assert len(H) == 900 and len(species) == 30 and len(ib) == 2880 and len(v2) == 4320 and len(set(ib + v2)) == 7200 and len(set(H)) == 900
import random
NIB = 30                         # InstaBox shards: per seed, shuffle (fixed RNG) then deal round robin, so each box gets 12 jobs
rng = random.Random(20261117)    # per seed in a random mix of species/cells/arms, still ordered seed by seed
shards = [[] for _ in range(NIB)]
for s_ in ib_seeds:
    js = list(S[s_]); rng.shuffle(js)
    for i, j in enumerate(js):
        shards[i % NIB].append(j)
assert sorted(sum(shards, [])) == sorted(ib) and all(len(x) == 96 for x in shards)
for i, x in enumerate(shards):
    (out / f"scan_ib_shard_{i + 1:02d}.txt").write_text("\n".join(x) + "\n")
print(NIB, "InstaBox shards of", len(shards[0]))
for name, js in [("horizon_jobs.txt", H), ("scan_vultr2_jobs.txt", v2), ("scan_ib_jobs.txt", ib), ("scan_all_jobs.txt", [j for s in range(1, 21) for j in S[s]])]:
    (out / name).write_text("\n".join(js) + "\n")
    print(name, len(js))
