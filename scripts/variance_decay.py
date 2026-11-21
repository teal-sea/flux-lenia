"""ROADMAP step 1: genome variance decay, advect_genome on vs off.

Two lineages of one curated species are spawned as two blobs carrying
opposite genome vectors (+u and -u for a fixed unit vector u). The run
records, every SAMPLE steps, how much genome variation the world still
holds. Variation is measured mass-weighted, so empty cells do not count.

Quantities per sample:
  s            lineage coordinate of a cell, G . u  (+1 pure A, -1 pure B)
  var_s        mass-weighted variance of s over all cells
  var_between  mass-weighted variance of per-organism mean s
               (organisms segmented with novelty_oracle.extract_blobs)
  hybrid_frac  mass fraction with |s| < 0.5
  pure_frac    mass fraction with |s| > 0.9

Half-life = first sampled step at which the quantity falls to half its
step-0 value. If it never does, the half-life is reported as "> T".

With advect_genome=False the genome field is frozen in place, so mass that
moves onto empty background picks up the background genome (zero). The
control therefore measures the frozen map sampled by moving mass, not a
conserved lineage label. This is the control ROADMAP step 1 specifies; the
caveat is reported with the numbers.

Usage:
  python scripts/variance_decay.py SPECIES PLACEMENT_SEED ADVECT(0|1) STEPS OUTDIR
"""

from __future__ import annotations

import dataclasses
import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine import neural_field as nf  # noqa: E402
from engine import novelty_oracle as no  # noqa: E402

SAMPLE = 100
U_SEED = 20261103
MIN_SEP = 40.0  # minimum periodic distance between the two spawn centres


def lineage_axis(dim: int) -> np.ndarray:
    u = np.random.default_rng(U_SEED).normal(size=dim)
    return u / np.linalg.norm(u)


def placements(seed: int, size: int) -> list[tuple[float, float]]:
    rng = np.random.default_rng(seed)
    while True:
        a = rng.uniform(0, size, size=2)
        b = rng.uniform(0, size, size=2)
        d = np.abs(a - b)
        d = np.minimum(d, size - d)
        if np.hypot(*d) >= MIN_SEP:
            return [tuple(map(float, a)), tuple(map(float, b))]


def measure(A: np.ndarray, G: np.ndarray, u: np.ndarray) -> dict:
    m = A.sum(axis=0)
    M = float(m.sum())
    s = np.tensordot(u, G, axes=(0, 0))
    w = m / M
    mean_s = float((w * s).sum())
    var_s = float((w * (s - mean_s) ** 2).sum())
    gbar = (G * w[None]).sum(axis=(1, 2))
    var_tot = float((w[None] * (G - gbar[:, None, None]) ** 2).sum())

    blobs = no.extract_blobs(A)
    if blobs:
        bm = np.array([b.mass for b in blobs])
        bs = np.array([float((m[b.mask] * s[b.mask]).sum() / m[b.mask].sum())
                       for b in blobs])
        bw = bm / bm.sum()
        bmean = float((bw * bs).sum())
        var_between = float((bw * (bs - bmean) ** 2).sum())
        n_a = int((bs > 0.5).sum())
        n_b = int((bs < -0.5).sum())
        n_h = int((np.abs(bs) <= 0.5).sum())
    else:
        var_between, n_a, n_b, n_h = 0.0, 0, 0, 0

    return {
        "mass": M,
        "mean_s": mean_s,
        "var_s": var_s,
        "var_total": var_tot,
        "var_between": var_between,
        "hybrid_frac": float(w[np.abs(s) < 0.5].sum()),
        "pure_frac": float(w[np.abs(s) > 0.9].sum()),
        "share_A": float(w[s > 0].sum()),
        "n_blobs": len(blobs),
        "n_blobs_A": n_a,
        "n_blobs_B": n_b,
        "n_blobs_hybrid": n_h,
    }


def half_life(ts: list[int], xs: list[float]) -> int | None:
    x0 = xs[0]
    if x0 <= 0:
        return None
    for t, x in zip(ts, xs):
        if x <= 0.5 * x0:
            return t
    return None


def main() -> None:
    species, pseed, advect, steps, outdir = sys.argv[1:6]
    pseed, advect, steps = int(pseed), bool(int(advect)), int(steps)
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)

    gpath = ROOT / "outputs" / "species" / f"{species}_genome.json"
    data = json.loads(gpath.read_text())
    w = nf.World.from_json(data, seed=pseed)
    w.cfg = dataclasses.replace(w.cfg, advect_genome=advect)
    w.light_pos = None
    cfg = w.cfg

    u = lineage_axis(cfg.genome_dim)
    (ya, xa), (yb, xb) = placements(pseed, cfg.size)
    r, peak = float(data["spawn_radius"]), float(data["spawn_peak"])
    w.spawn(ya, xa, +u, radius=r, peak=peak, seed=pseed * 2 + 1)
    w.spawn(yb, xb, -u, radius=r, peak=peak, seed=pseed * 2 + 2)

    ts, rows = [0], [measure(np.asarray(w.A), np.asarray(w.Gf), u)]
    frames = {0: (np.asarray(w.A).sum(0), np.tensordot(u, np.asarray(w.Gf), axes=(0, 0)))}
    keep = {steps // 4, steps // 2, steps}
    t0 = time.time()
    while w.t < steps:
        w.run(SAMPLE)
        A, G = np.asarray(w.A), np.asarray(w.Gf)
        ts.append(w.t)
        rows.append(measure(A, G, u))
        if w.t in keep:
            frames[w.t] = (A.sum(0), np.tensordot(u, G, axes=(0, 0)))
    wall = time.time() - t0

    series = {k: [r_[k] for r_ in rows] for k in rows[0]}
    m0 = series["mass"][0]
    contact = next((t for t, h in zip(ts, series["hybrid_frac"]) if h > 0.01), None)
    result = {
        "species": species,
        "placement_seed": pseed,
        "advect_genome": advect,
        "steps": steps,
        "sample_every": SAMPLE,
        "spawn_centres": [[ya, xa], [yb, xb]],
        "lineage_axis_seed": U_SEED,
        "wall_seconds": wall,
        "max_rel_mass_drift": float(max(abs(m - m0) / m0 for m in series["mass"])),
        "first_contact_step": contact,
        "half_life": {
            k: half_life(ts, series[k])
            for k in ("var_s", "var_total", "var_between", "pure_frac")
        },
        "final": rows[-1],
        "t": ts,
        "series": series,
    }
    tag = f"{species}_p{pseed}_adv{int(advect)}"
    (out / f"{tag}.json").write_text(json.dumps(result))
    np.savez_compressed(out / f"{tag}_frames.npz",
                        **{f"mass_{k}": v[0] for k, v in frames.items()},
                        **{f"s_{k}": v[1] for k, v in frames.items()})
    print(json.dumps({k: result[k] for k in
                      ("species", "placement_seed", "advect_genome", "wall_seconds",
                       "max_rel_mass_drift", "first_contact_step", "half_life")}))


if __name__ == "__main__":
    main()
