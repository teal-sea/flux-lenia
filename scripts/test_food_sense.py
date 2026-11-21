"""Checks for Config.food_sense (docs/FOOD-SENSING-2026-11-16.md).

Modes
  quick   seconds, single field evaluations, no rollouts (allowed on citadel):
          1. food_features is exactly 0 where there is no food, has shape (2 n_kernels, H, W), and
             responds to the food field;
          2. the lineage tag is unreadable: with food_sense on and a non-uniform food field, replacing
             the tag by noise or flipping it leaves the hidden activations and the velocities
             BIT-identical (positive controls: changing a functional genome row, or the food
             field, changes them);
          3. the genome shapes the response to food: the food-induced change of the hidden
             activations differs between genome +u and genome -u on the same food field;
          4. food_sense = 0 leaves sensorimotor untouched (Ff ignored, W1f not needed).
  full    rolls the engine for hundreds of steps. RUN ON AN INSTABOX MACHINE, NOT ON CITADEL.
          5. no-op: with food_sense = 0 the sha256 of (A, G, F) after STEPS steps (food on, per_channel,
             three species, kappa 0 and kappa 3) equals the hash from the pre-change engine at
             --ref-root (git archive of the base commit), and equals the hash through rollout_logged;
          6. conservation with food_sense on: (a) sum(A) + sum(F) over the full food step;
             (b) transport alone under a prescribed food field: sum(A_tot * G) for every genome row incl.
             the tag, and sum(A); (c) eaten - decayed equals the body gain from the food logger;
          7. the term acts: the trajectory with food_sense on differs from food_sense = 0;
          8. the tag stays unread over the rollout: flipping the tag sign gives bit-identical A.
  hash    prints a state hash (used by `full` for the reference engine).

Usage: python scripts/test_food_sense.py quick
       python scripts/test_food_sense.py full [--ref-root DIR] [--steps 300] [--food-sense 3]
       python scripts/test_food_sense.py hash ENGINE_ROOT SPECIES KAPPA STEPS
"""

from __future__ import annotations

import dataclasses
import hashlib
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from test_repulsion import SPECIES, POS, TOUCH, load, setup  # noqa: E402


def food_field(jnp, n, level):
    y, x = np.mgrid[0:n, 0:n] * (2 * np.pi / n)
    return jnp.asarray(level * (1.0 + 0.5 * np.sin(y) * np.cos(2 * x) + 0.2 * np.cos(3 * y + x)))


def with_food(cfg, p, species, fs):
    nf = sys.modules["engine.neural_field"]
    cfg = dataclasses.replace(cfg, food_sense=fs)
    p = dict(p)
    import jax.numpy as jnp
    p["W1f"] = jnp.asarray(nf.sample_food_weights(species, cfg))
    return cfg, p


def quick() -> None:
    for sp in SPECIES:
        w, cfg0, p0, G, (jnp, nf, nu) = setup(ROOT, sp, arm="treat", pos=TOUCH)
        n = cfg0.size
        cfg, p = with_food(cfg0, p0, sp, 3.0)
        level = float(jnp.sum(w.A)) / n ** 2
        F = food_field(jnp, n, level)
        # 1. food features
        Z = nf.food_features(jnp.zeros((n, n)), p, w.bank, cfg)
        assert Z.shape == (cfg.n_food_features, n, n) and float(jnp.max(jnp.abs(Z))) == 0.0
        Ff = nf.food_features(F, p, w.bank, cfg)
        assert float(jnp.max(jnp.abs(Ff))) > 1e-3
        Ff2 = nf.food_features(F * 1.7, p, w.bank, cfg)
        assert float(jnp.max(jnp.abs(Ff2 - Ff))) > 1e-4

        khat, ksrc = w.bank
        U = nf.perceive(w.A, khat, ksrc)

        def run(Gx, Fx, c=cfg):
            Fe = nf.food_features(Fx, p, w.bank, c) if c.food_sense != 0.0 else None
            E, g, th, h = nf.sensorimotor(U, w.A, Gx, w.light, p, c, Fe, return_hidden=True)
            return h, nf.flow_field(E, g, th, w.A, c, Gx)

        h0, v0 = run(G, F)
        # 2. tag unreadable
        rng = np.random.default_rng(0)
        for name, Gt in (("noise", G.at[-1].set(jnp.asarray(rng.uniform(-1, 1, size=G.shape[1:])))),
                         ("flipped", G.at[-1].set(-G[-1]))):
            h1, v1 = run(Gt, F)
            assert np.array_equal(np.asarray(h0), np.asarray(h1)), f"hidden changed with tag {name}"
            assert all(np.array_equal(np.asarray(a), np.asarray(b)) for a, b in zip(v0, v1)), f"velocity changed with tag {name}"
        # positive controls: the check can fail
        Gf = G.at[0].set(G[0] + 0.5)
        h2, _ = run(Gf, F)
        assert float(jnp.max(jnp.abs(h2 - h0))) > 1e-3
        h3, _ = run(G, F * 1.7)
        assert float(jnp.max(jnp.abs(h3 - h0))) > 1e-6
        # 3. the genome shapes the response to food: food-induced change of h differs between +u and -u
        u = np.random.default_rng(20261103).normal(size=cfg0.genome_dim - 1)
        u /= np.linalg.norm(u)

        def uniform_genome(sign):
            g = jnp.concatenate([jnp.asarray(sign * u)[:, None, None] * jnp.ones((1, n, n)),
                                 jnp.zeros((1, n, n))], axis=0)
            return g

        d = {}
        for sign in (+1, -1):
            Gs = uniform_genome(sign)
            h_on, _ = run(Gs, F)
            h_off, _ = run(Gs, F, dataclasses.replace(cfg, food_sense=0.0))
            d[sign] = np.asarray(h_on - h_off)
        gap = float(np.max(np.abs(d[+1] - d[-1])))
        assert gap > 1e-4, gap
        # 4. food_sense = 0: Ff ignored, no W1f needed
        c0 = dataclasses.replace(cfg, food_sense=0.0)
        pw = {k: v for k, v in p.items() if k != "W1f"}
        out_a = nf.sensorimotor(U, w.A, G, w.light, pw, c0)
        out_b = nf.sensorimotor(U, w.A, G, w.light, p, c0, Ff)
        assert all(np.array_equal(np.asarray(a), np.asarray(b)) for a, b in zip(out_a, out_b))
        print(f"{sp[12:]:9s} Wf seed {nf.food_weight_seed(sp)}: features {tuple(Ff.shape)} max {float(jnp.max(jnp.abs(Ff))):.3g}, 0 at F=0; "
              f"tag noise/flip -> hidden and velocity bit-identical; max|dh| for genome change {float(jnp.max(jnp.abs(h2 - h0))):.2g}, "
              f"food change {float(jnp.max(jnp.abs(h3 - h0))):.2g}; food-induced dh differs +u vs -u by {gap:.2g}")
    print("quick OK")


def state_hash(root: Path, species: str, kappa: float, steps: int = 300, logged: bool = False,
               explicit_zero: bool = False) -> str:
    w, cfg, p, G, (jnp, nf, nu) = setup(root, species)
    if kappa != 0.0:
        cfg = dataclasses.replace(cfg, repulsion_kappa=kappa)
    if explicit_zero:
        cfg = dataclasses.replace(cfg, food_sense=0.0)
    n = cfg.size
    F = jnp.full((n, n), float(jnp.sum(w.A)) / n ** 2)
    A, food = w.A, nu.Food()
    for _ in range(steps // 100):
        if logged:
            A, G, F, _, _ = nu.rollout_logged(A, G, F, w.light, p, w.bank, cfg, food, 100)
        else:
            A, G, F = nu.rollout(A, G, F, w.light, p, w.bank, cfg, food, 100)
    h = hashlib.sha256()
    for x in (A, G, F):
        h.update(np.asarray(x).tobytes())
    return h.hexdigest()


def full(ref_root, steps: int, fs: float) -> None:
    import subprocess
    jnp, nf, nu = mods = load(ROOT)
    for sp in SPECIES:
        for kappa in (0.0, 3.0):
            h_new = state_hash(ROOT, sp, kappa, steps)
            h_log = state_hash(ROOT, sp, kappa, steps, logged=True, explicit_zero=True)
            assert h_new == h_log, f"{sp} kappa={kappa}: rollout_logged / explicit food_sense=0 hash differs"
            if ref_root is not None:
                out = subprocess.run([sys.executable, __file__, "hash", str(ref_root), sp, str(kappa), str(steps)],
                                     capture_output=True, text=True, check=True).stdout.strip()
                assert out == h_new, f"{sp} kappa={kappa}: food_sense=0 hash {h_new} != pre-change {out}"
                print(f"{sp[12:]:9s} 5. kappa={kappa:g} food_sense=0 hash == pre-change engine == rollout_logged ({steps} steps): {h_new[:16]}")
            else:
                print(f"{sp[12:]:9s} 5. (no --ref-root) kappa={kappa:g} hash {h_new[:16]} == rollout_logged")
        # 6, 7, 8 with food_sense on
        w, cfg0, p0, G0, _ = setup(ROOT, sp, mods=mods)
        n = cfg0.size
        cfg, p = with_food(cfg0, p0, sp, fs)
        M0 = float(jnp.sum(w.A))
        F0 = jnp.full((n, n), M0 / n ** 2)
        food = nu.Food()
        # (a) full food step: sum(A) + sum(F); (c) food logger vs body gain
        A, G, F = w.A, G0, F0
        T0, worst, eaten, decayed = M0 + float(jnp.sum(F0)), 0.0, 0.0, 0.0
        for _ in range(steps // 100):
            A, G, F, e, d = nu.rollout_logged(A, G, F, w.light, p, w.bank, cfg, food, 100)
            eaten += float(e); decayed += float(d)
            worst = max(worst, abs(float(jnp.sum(A)) + float(jnp.sum(F)) - T0) / T0)
        gain_err = abs((float(jnp.sum(A)) - M0) - (eaten - decayed)) / M0
        print(f"{sp[12:]:9s} 6a. food_sense={fs:g}, food on, {steps} steps: max |d(sum A + sum F)|/T = {worst:.2e}; "
              f"6c. |(body gain) - (eaten - decayed)|/M = {gain_err:.2e} (eaten {eaten:.3f}, decayed {decayed:.3f})")
        assert worst < 1e-12 and gain_err < 1e-12 and eaten > 0
        # (b) transport alone under a prescribed, fixed food field
        Fx = food_field(jnp, n, M0 / n ** 2)
        A, G = w.A, G0
        S0 = np.asarray(jnp.sum(G0 * jnp.sum(w.A, 0)[None], axis=(1, 2)))
        wt = np.zeros(2); mdr = 0.0
        khat, ksrc = w.bank
        for _ in range(steps):
            U = nf.perceive(A, khat, ksrc)
            Ff = nf.food_features(Fx, p, w.bank, cfg)
            E, g, th = nf.sensorimotor(U, A, G, w.light, p, cfg, Ff)
            dy, dx = nf.flow_field(E, g, th, A, cfg, G)
            A, G = nf.reintegrate(A, G, dy, dx, cfg)
            S = np.asarray(jnp.sum(G * jnp.sum(A, 0)[None], axis=(1, 2)))
            dd = np.abs(S - S0)
            wt = np.maximum(wt, [dd[-1], dd[:-1].max()])
            mdr = max(mdr, abs(float(jnp.sum(A)) - M0))
        print(f"{sp[12:]:9s} 6b. transport under food_sense={fs:g}, {steps} steps: max|dS_tag|/M = {wt[0] / M0:.2e}, "
              f"functional rows = {wt[1] / M0:.2e}, |dM|/M = {mdr / M0:.2e}")
        assert wt.max() / M0 < 1e-12 and mdr / M0 < 1e-12
        # 7. acts; 8. tag unread over the rollout
        def roll(c, G_):
            A, G, F = w.A, G_, F0
            for _ in range(steps // 100):
                A, G, F = nu.rollout(A, G, F, w.light, p, w.bank, c, food, 100)
            return A
        A_on = roll(cfg, G0)
        A_off = roll(dataclasses.replace(cfg, food_sense=0.0), G0)
        diff = float(jnp.max(jnp.abs(A_on - A_off)))
        A_flip = roll(cfg, G0.at[-1].set(-G0[-1]))
        same = bool(np.array_equal(np.asarray(A_on), np.asarray(A_flip)))
        print(f"{sp[12:]:9s} 7. food sensing changes the trajectory: max|A(on) - A(off)| = {diff:.2e}; "
              f"8. tag flipped: body bit-identical = {same}")
        assert diff > 1e-6 and same
    print("full OK")


def main() -> None:
    mode = sys.argv[1] if len(sys.argv) > 1 else "quick"
    if mode == "hash":
        root, sp, kappa = Path(sys.argv[2]), sys.argv[3], float(sys.argv[4])
        print(state_hash(root, sp, kappa, int(sys.argv[5]) if len(sys.argv) > 5 else 300))
    elif mode == "quick":
        sys.path.insert(0, str(ROOT))
        quick()
    elif mode == "full":
        a = sys.argv[2:]
        get = lambda k, d: a[a.index(k) + 1] if k in a else d
        ref = get("--ref-root", None)
        full(Path(ref) if ref else None, int(get("--steps", 300)), float(get("--food-sense", 3.0)))
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
