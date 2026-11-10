"""Checks for Config.genome_transport = "per_channel" (docs/GENOME-TRANSPORT-2026-11-10.md).

For each of the three species, in the food-selection setup (two blobs, treatment arm, unread
tag as ninth genome dimension, food off), STEPS steps:

 a. Mass: from the same state, one step in either mode gives bit-identical A (max |dA| == 0).
    The state is advanced with the "mean" mode, so this is checked on 400 different states.
 b. Conservation: under "per_channel" run on its own, S = sum(A_tot * tag) stays at its
    initial value. Reported as max_t |S_t - S_0| / M and also relative to the tag-weighted
    absolute mass sum(A_tot |tag|). Also checked for the functional genome rows.
 c. Discrimination: under "mean" the same quantity drifts by more than 1e6 times the
    per_channel drift (printed); the assert is that it is > 1e-6 and per_channel < 1e-12.

Usage: python scripts/test_transport.py [STEPS]
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

SPECIES = ["SPECIES_001_OSCILLIS", "SPECIES_002_MITOSA", "SPECIES_003_VAGRANT"]


def setup(species, seed=1):
    data = json.loads((ROOT / "outputs" / "species" / f"{species}_genome.json").read_text())
    w = nf.World.from_json(data, seed=seed)
    w.cfg = dataclasses.replace(w.cfg, advect_genome=True)
    cfg, params = nu.tagged(w.cfg, {k: np.asarray(v) for k, v in w.params.items()})
    p = nf.params_to_jax(params)
    u = np.random.default_rng(20261103).normal(size=w.cfg.genome_dim)
    u /= np.linalg.norm(u)
    r, peak = float(data["spawn_radius"]), float(data["spawn_peak"])
    w.spawn(30, 40, u, radius=r, peak=peak, seed=1000 + seed)
    m_a = np.asarray(jnp.sum(w.A, axis=0))
    w.spawn(90, 100, -u, radius=r, peak=peak, seed=1000 + seed)
    m_b = np.asarray(jnp.sum(w.A, axis=0)) - m_a
    tag = (m_a - m_b) / np.maximum(m_a + m_b, 1e-300)
    G = jnp.concatenate([w.Gf, jnp.asarray(tag)[None]], axis=0)
    return w, cfg, p, G


def invariants(A, G):
    m = jnp.sum(A, axis=0)
    return np.asarray(jnp.sum(G * m[None], axis=(1, 2))), float(jnp.sum(m)), \
        float(jnp.sum(m * jnp.abs(G[-1])))


def run(w, cfg, p, G, steps):
    A = w.A
    S0, M, Mabs = invariants(A, G)
    worst = np.zeros(2)
    for _ in range(steps):
        A, G, _, _ = nf.step(A, G, w.light, p, w.bank, cfg)
        S, _, _ = invariants(A, G)
        d = np.abs(S - S0)
        worst = np.maximum(worst, [d[-1], d[:-1].max()])
    return worst / M, worst[0] / Mabs, M


def main():
    steps = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    summary = []
    for sp in SPECIES:
        w, cfg_m, p, G0 = setup(sp)
        cfg_c = dataclasses.replace(cfg_m, genome_transport="per_channel")
        assert cfg_m.genome_transport == "mean"

        # a. identical A from identical states, every step, trajectory driven by "mean"
        A, G = w.A, G0
        dA_max = 0.0
        for _ in range(steps):
            A1, G1, _, _ = nf.step(A, G, w.light, p, w.bank, cfg_m)
            A2, G2, _, _ = nf.step(A, G, w.light, p, w.bank, cfg_c)
            dA_max = max(dA_max, float(jnp.max(jnp.abs(A1 - A2))))
            A, G = A1, G1
        print(f"{sp[12:]:9s} a. max |A_mean - A_per_channel| over {steps} states: {dA_max:.1e}")
        assert dA_max == 0.0

        # b. / c. conservation
        (tag_c, fn_c), tag_c_abs, M = run(w, cfg_c, p, G0, steps)
        (tag_m, fn_m), tag_m_abs, _ = run(w, cfg_m, p, G0, steps)
        print(f"{sp[12:]:9s} b. per_channel: max|dS_tag|/M = {tag_c:.2e} "
              f"(/sum A|tag| = {tag_c_abs:.2e}), functional genome rows max = {fn_c:.2e}")
        print(f"{sp[12:]:9s} c. mean (old):   max|dS_tag|/M = {tag_m:.2e} "
              f"(/sum A|tag| = {tag_m_abs:.2e}), functional genome rows max = {fn_m:.2e}")
        assert tag_c < 1e-12 and fn_c < 1e-12, "per_channel must conserve to rounding"
        assert tag_m > 1e-6, "old mode must show the drift, or the test does not discriminate"
        summary.append((sp[12:], dA_max, tag_c_abs, tag_c, fn_c, tag_m, tag_m_abs))
    print("\nsummary (steps=%d):" % steps)
    print("species | max dA | per_channel tag drift /M | /A|tag| | fn rows | old tag drift /M | /A|tag|")
    for s, d, tca, tc, fc, tm, tma in summary:
        print(f"{s} | {d:.0e} | {tc:.2e} | {tca:.2e} | {fc:.2e} | {tm:.2e} | {tma:.2e}")
    print("ALL OK")


if __name__ == "__main__":
    main()
