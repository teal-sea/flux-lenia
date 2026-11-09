"""Checks for engine/nutrient.py. Small: a few hundred steps on one core.

1. Food off and an unread tag: identical to neural_field.step (tag rows are zero).
2. Food on: sum(A) + sum(F) conserved to 1e-12 relative over 300 steps; F and A stay >= 0.
3. The tag really is unread: flipping its sign changes no body cell.
4. react() moves mass in both directions: uptake on fresh food, decay on empty food.

Usage: python scripts/test_nutrient.py
"""

from __future__ import annotations

import dataclasses
import json
import sys
from pathlib import Path

import jax.numpy as jnp
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine import neural_field as nf  # noqa: E402
from engine import nutrient as nu  # noqa: E402


def world(species="SPECIES_002_MITOSA"):
    data = json.loads((ROOT / "outputs" / "species" / f"{species}_genome.json").read_text())
    w = nf.World.from_json(data, seed=1)
    w.cfg = dataclasses.replace(w.cfg, advect_genome=True)
    g = np.random.default_rng(7).normal(size=w.cfg.genome_dim)
    w.spawn(40, 40, g, radius=16, peak=0.9, seed=3)
    w.spawn(90, 100, -g, radius=16, peak=0.9, seed=3)
    return data, w


def main():
    data, w = world()
    cfg0 = w.cfg
    params0 = {k: np.asarray(v) for k, v in w.params.items()}
    cfgT, pT = nu.tagged(cfg0, params0)
    pT = nf.params_to_jax(pT)
    tag = jnp.where(jnp.sum(w.A, 0) > 0, 1.0, 0.0)[None]
    GfT = jnp.concatenate([w.Gf, tag], axis=0)
    F0 = jnp.zeros((cfg0.size, cfg0.size))

    # 1. food off + tag == plain engine
    A, G = w.A, w.Gf
    At, Gt, Ft = w.A, GfT, F0
    off = nu.Food(enabled=False)
    for _ in range(50):
        A, G, _, _ = nf.step(A, G, w.light, w.params, w.bank, cfg0)
        At, Gt, Ft = nu.step(At, Gt, Ft, w.light, pT, w.bank, cfgT, off)
    dA = float(jnp.max(jnp.abs(A - At)))
    dG = float(jnp.max(jnp.abs(G - Gt[:-1])))
    print(f"1. food off + tag vs plain engine, 50 steps: max |dA| = {dA:.2e}, max |dG| = {dG:.2e}")
    assert dA < 1e-12 and dG < 1e-12

    # 2. conservation with food on
    food = nu.Food()
    M = float(jnp.sum(w.A))
    F = jnp.full((cfg0.size, cfg0.size), M / cfg0.size ** 2)
    total0 = float(jnp.sum(w.A) + jnp.sum(F))
    A2, G2, F2 = nu.rollout(w.A, GfT, F, w.light, pT, w.bank, cfgT, food, 300)
    total1 = float(jnp.sum(A2) + jnp.sum(F2))
    rel = abs(total1 - total0) / total0
    print(f"2. food on, 300 steps: total {total0:.6f} -> {total1:.6f}, relative drift {rel:.1e}; "
          f"body {float(jnp.sum(w.A)):.1f} -> {float(jnp.sum(A2)):.1f}; "
          f"min A {float(jnp.min(A2)):.1e}, min F {float(jnp.min(F2)):.1e}")
    assert rel < 1e-12
    assert float(jnp.min(F2)) >= -1e-12 and float(jnp.min(A2)) >= -1e-12

    # 3. tag sign does not reach the body
    A3, _, _ = nu.rollout(w.A, GfT.at[-1].multiply(-1.0), F, w.light, pT, w.bank, cfgT, food, 300)
    d3 = float(jnp.max(jnp.abs(A3 - A2)))
    print(f"3. tag flipped, 300 steps with food: max |dA| = {d3:.2e}")
    assert d3 == 0.0

    # 4. react() directions
    A4 = jnp.ones((3, 4, 4)) * 0.5
    Ar, Fr = nu.react(A4, jnp.ones((4, 4)), food)
    Ad, Fd = nu.react(A4, jnp.zeros((4, 4)), food)
    print(f"4. react: body on food gains {float(jnp.sum(Ar - A4)):.4f}, "
          f"body without food loses {float(jnp.sum(A4 - Ad)):.4f}")
    assert float(jnp.sum(Ar - A4)) > 0 and float(jnp.sum(A4 - Ad)) > 0
    print("ALL OK")


if __name__ == "__main__":
    main()
