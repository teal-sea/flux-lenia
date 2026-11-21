"""Checks for Config.repulsion_kappa (docs/CONDITIONAL-BLENDING-2026-11-15.md).

Modes
  quick   a few seconds, one field evaluation per check, no rollouts:
          1. the neutral tag never enters F: two blobs that differ only in the tag give F == 0
             (to rounding) and F is bit-identical when the tag is replaced by noise. With G8
             exactly constant F < 1e-25; with the state as spawned F < 1e-10 (World.spawn's 1e-9
             regulariser leaves G8 a fraction 1e-3 off u in cells holding about 1e-6 of mass);
          2. the test can fail: two blobs that differ in the functional genome give F > 1e-3;
          3. in the tag-only state the repulsion term adds nothing to the velocity (|dv| < 1e-12).
  full    rolls the engine for hundreds of steps. RUN ON AN INSTABOX MACHINE, NOT ON CITADEL.
          4. kappa = 0 is a no-op: the sha256 of (A, G, F) after STEPS steps (food on, per_channel,
             three species) equals the hash from the pre-change engine at --ref-root
             (git archive of the base commit's engine/), and equals the hash with the new code and
             repulsion_kappa passed explicitly as 0.0;
          5. conservation with repulsion on (kappa = KAPPA, food off, STEPS steps, three species):
             sum(A_tot * G) for every genome row incl. the tag, and sum(A), stay at their initial
             values to rounding (< 1e-12 of M; the expectation is about 1e-16);
          6. the term acts: the treatment trajectory differs from kappa = 0.

Usage: python scripts/test_repulsion.py quick
       python scripts/test_repulsion.py full [--ref-root DIR] [--steps 300] [--kappa 3]
       python scripts/test_repulsion.py hash ENGINE_ROOT SPECIES      (prints a state hash; used by `full`)
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SPECIES = ["SPECIES_001_OSCILLIS", "SPECIES_002_MITOSA", "SPECIES_003_VAGRANT"]
POS = ((30, 40), (90, 100))
TOUCH = ((60, 50), (60, 72))     # blobs of radius 16 overlap: the tag-only and G8-differs checks need contact


def load(root: Path):
    sys.path.insert(0, str(root))
    import jax.numpy as jnp
    from engine import neural_field as nf
    from engine import nutrient as nu
    return jnp, nf, nu


def setup(root: Path, species: str, arm: str = "treat", seed: int = 1, mods=None, pos=POS):
    """Two blobs as in scripts/food_selection.py; returns (world, cfg, params, G, mods)."""
    jnp, nf, nu = mods or load(root)
    data = json.loads((ROOT / "outputs" / "species" / f"{species}_genome.json").read_text())
    w = nf.World.from_json(data, seed=seed)
    w.cfg = dataclasses.replace(w.cfg, advect_genome=True, genome_transport="per_channel")
    cfg, params = nu.tagged(w.cfg, {k: np.asarray(v) for k, v in w.params.items()})
    p = nf.params_to_jax(params)
    u = np.random.default_rng(20261103).normal(size=w.cfg.genome_dim)
    u /= np.linalg.norm(u)
    sa, sb = {"treat": (1, -1), "neutral_plus": (1, 1)}[arm]
    r, peak = float(data["spawn_radius"]), float(data["spawn_peak"])
    w.spawn(*pos[0], sa * u, radius=r, peak=peak, seed=1000 + seed)
    m_a = np.asarray(jnp.sum(w.A, axis=0))
    w.spawn(*pos[1], sb * u, radius=r, peak=peak, seed=1000 + seed)
    m_b = np.asarray(jnp.sum(w.A, axis=0)) - m_a
    tag = (m_a - m_b) / np.maximum(m_a + m_b, 1e-300)
    G = jnp.concatenate([w.Gf, jnp.asarray(tag)[None]], axis=0)
    return w, cfg, p, G, (jnp, nf, nu)


def state_hash(root: Path, species: str, steps: int = 300) -> str:
    w, cfg, p, G, (jnp, nf, nu) = setup(root, species)
    n = cfg.size
    F = jnp.full((n, n), float(jnp.sum(w.A)) / n ** 2)
    A, food = w.A, nu.Food()
    for _ in range(steps // 100):
        A, G, F = nu.rollout(A, G, F, w.light, p, w.bank, cfg, food, 100)
    h = hashlib.sha256()
    for x in (A, G, F):
        h.update(np.asarray(x).tobytes())
    return h.hexdigest()


def quick() -> None:
    for sp in SPECIES[:2]:
        w, cfg, p, G, (jnp, nf, nu) = setup(ROOT, sp, arm="neutral_plus", pos=TOUCH)
        cfg_r = dataclasses.replace(cfg, repulsion_kappa=3.0)
        F0 = np.asarray(nf.foreign_mass_field(w.A, G, cfg_r))
        rng = np.random.default_rng(0)
        G_noise = G.at[-1].set(jnp.asarray(rng.uniform(-1, 1, size=G.shape[1:])))
        F1 = np.asarray(nf.foreign_mass_field(w.A, G_noise, cfg_r))
        assert np.array_equal(F0, F1), "F changed when only the tag changed"
        assert F0.max() < 1e-10, F0.max()
        # strict version: G8 exactly the same constant everywhere, tag untouched
        G8c = G.at[:-1].set(jnp.asarray(np.asarray(G[:-1, 0, 0]) * 0 + np.asarray(
            jnp.sum(G[:-1] * jnp.sum(w.A, 0)[None], axis=(1, 2)) / jnp.sum(w.A)))[:, None, None])
        Fc = np.asarray(nf.foreign_mass_field(w.A, G8c, cfg_r))
        assert Fc.max() < 1e-25, Fc.max()
        # the tag really differs between the blobs in this state
        tag = np.asarray(G[-1]); m = np.asarray(jnp.sum(w.A, 0))
        assert tag[m > 0.5].max() > 0.9 and tag[m > 0.5].min() < -0.9
        # velocity: with and without the term, same state
        khat, ksrc = w.bank
        U = nf.perceive(w.A, khat, ksrc)
        E, gain, theta = nf.sensorimotor(U, w.A, G, w.light, p, cfg)
        d1 = nf.flow_field(E, gain, theta, w.A, cfg_r, G)
        d0 = nf.flow_field(E, gain, theta, w.A, cfg, G)
        dd = max(float(jnp.max(jnp.abs(a - b))) for a, b in zip(d1, d0))
        assert dd < 1e-12, dd
        # positive control: treatment arm, same positions
        wt, cfg_t, pt, Gt, _ = setup(ROOT, sp, arm="treat", pos=TOUCH)
        Ft = np.asarray(nf.foreign_mass_field(wt.A, Gt, dataclasses.replace(cfg_t, repulsion_kappa=3.0)))
        assert Ft.max() > 1e-3, Ft.max()  # the check can fail
        print(f"{sp[12:]:9s} tag-only: max F = {F0.max():.1e} (G8 exactly constant: {Fc.max():.1e}), F(tag noise) == F bitwise, max|dv| = {dd:.1e}; "
              f"treat (G8 differs): max F = {Ft.max():.3f}")
    print("quick OK")


def full(ref_root: Path | None, steps: int, kappa: float) -> None:
    jnp, nf, nu = mods = load(ROOT)
    for sp in SPECIES:
        # 4. kappa = 0 no-op
        h_new = state_hash(ROOT, sp, steps)
        if ref_root is not None:
            out = subprocess.run([sys.executable, __file__, "hash", str(ref_root), sp, str(steps)],
                                 capture_output=True, text=True, check=True).stdout.strip()
            assert out == h_new, f"{sp}: kappa=0 hash {h_new} != pre-change {out}"
            print(f"{sp[12:]:9s} 4. kappa=0 hash == pre-change engine ({steps} steps): {h_new[:16]}")
        else:
            print(f"{sp[12:]:9s} 4. (no --ref-root: pre-change comparison skipped) hash {h_new[:16]}")
        # 5. conservation with repulsion on, food off
        w, cfg, p, G0, _ = setup(ROOT, sp, mods=mods)
        cfg_r = dataclasses.replace(cfg, repulsion_kappa=kappa)

        def run(cfg_):
            A, G = w.A, G0
            S0 = np.asarray(jnp.sum(G0 * jnp.sum(w.A, 0)[None], axis=(1, 2)))
            M0 = float(jnp.sum(w.A)); worst = np.zeros(2); mdrift = 0.0
            for _ in range(steps):
                A, G, _, _ = nf.step(A, G, w.light, p, w.bank, cfg_)
                S = np.asarray(jnp.sum(G * jnp.sum(A, 0)[None], axis=(1, 2)))
                d = np.abs(S - S0)
                worst = np.maximum(worst, [d[-1], d[:-1].max()])
                mdrift = max(mdrift, abs(float(jnp.sum(A)) - M0))
            return worst / M0, mdrift / M0, A
        (tag_d, fn_d), m_d, A_r = run(cfg_r)
        print(f"{sp[12:]:9s} 5. repulsion kappa={kappa}, food off, {steps} steps: max|dS_tag|/M = {tag_d:.2e}, "
              f"functional rows = {fn_d:.2e}, |dM|/M = {m_d:.2e}")
        assert tag_d < 1e-12 and fn_d < 1e-12 and m_d < 1e-12
        _, _, A_0 = run(cfg)
        diff = float(jnp.max(jnp.abs(A_r - A_0)))
        print(f"{sp[12:]:9s} 6. repulsion changes the trajectory: max|A(kappa) - A(0)| = {diff:.2e}")
        assert diff > 1e-6
    print("full OK")


def main() -> None:
    mode = sys.argv[1] if len(sys.argv) > 1 else "quick"
    if mode == "hash":
        root, sp = Path(sys.argv[2]), sys.argv[3]
        print(state_hash(root, sp, int(sys.argv[4]) if len(sys.argv) > 4 else 300))
    elif mode == "quick":
        quick()
    elif mode == "full":
        a = sys.argv[2:]
        get = lambda k, d: a[a.index(k) + 1] if k in a else d
        ref = get("--ref-root", None)
        full(Path(ref) if ref else None, int(get("--steps", 300)), float(get("--kappa", 3.0)))
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
