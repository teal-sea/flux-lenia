"""Validation of scripts/gpu_batch.py (kept tiny: <= 300 steps, batch <= 8, so it can run on citadel).

  python scripts/test_gpu_batch.py cli-compare CLI_DIR BATCH_DIR TAG      JSON + frames, CLI vs gpu_batch
  python scripts/test_gpu_batch.py arrays [--steps 300]                   1. batch of 1 vs the single-run path: A, G, F, metrics
  python scripts/test_gpu_batch.py batch4 [--steps 300]                   2. batch of 4 vs four batches of 1
  python scripts/test_gpu_batch.py species [--steps 300]                  3. conservation, three species, three arms
  python scripts/test_gpu_batch.py hash REF_ENGINE_ROOT [--steps 300]     4. kappa 0 / food_sense 0 batch vs the pre-change engine

Run with JAX_PLATFORMS=cpu and XLA_FLAGS="--xla_cpu_multi_thread_eigen=false intra_op_parallelism_threads=1".
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

os.environ.setdefault("JAX_PLATFORMS", "cpu")
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402

import gpu_batch as gb  # noqa: E402
import food_selection as fs  # noqa: E402
from engine import nutrient as nu  # noqa: E402

SPECIES = ["SPECIES_001_OSCILLIS", "SPECIES_002_MITOSA", "SPECIES_003_VAGRANT"]
ARMS = ["treat", "neutral_plus", "neutral_minus"]
KW = dict(food_on=True, transport="per_channel", kappa=3.0, food_sense=0.0, fs_present=True,
          sample_every=100, threads=1, log=lambda m: None)


def sim(species, pairs, steps, **over):
    kw = {**KW, **over}
    return gb.simulate(species, pairs, steps=steps, frame_every=steps, **kw)


def flat(d, prefix=""):
    for k, v in d.items():
        if isinstance(v, dict):
            yield from flat(v, f"{prefix}{k}.")
        elif isinstance(v, list):
            if v and isinstance(v[0], list):
                for i, x in enumerate(v):
                    yield f"{prefix}{k}[{i}]", np.asarray(x, dtype=float)
            else:
                try:
                    yield f"{prefix}{k}", np.asarray(v, dtype=float)
                except (TypeError, ValueError):
                    yield f"{prefix}{k}", v
        else:
            yield f"{prefix}{k}", v


def compare_results(a: dict, b: dict, label: str, skip=("wall_seconds",)) -> dict:
    """Max abs difference per leaf (numbers), exact equality for the rest."""
    fa, fb = dict(flat(a)), dict(flat(b))
    assert fa.keys() == fb.keys(), (sorted(set(fa) ^ set(fb)))
    worst, bad = {}, []
    for k in fa:
        if k in skip:
            continue
        x, y = fa[k], fb[k]
        if isinstance(x, np.ndarray):
            d = float(np.max(np.abs(x - y))) if x.size else 0.0
        elif isinstance(x, (int, float)) and not isinstance(x, bool):
            d = abs(x - y)
        else:
            d = 0.0 if x == y else float("inf")
        worst[k] = d
        if d != 0.0:
            bad.append((k, d))
    top = {}
    for k, d in worst.items():                      # group by series name
        g = k.split(".")[-1] if k.startswith("series.") else k
        top[g] = max(top.get(g, 0.0), d)
    nz = {k: v for k, v in top.items() if v != 0.0}
    print(f"{label}: {len(worst)} leaves compared; {'BIT-IDENTICAL' if not nz else 'max abs diffs ' + json.dumps(nz)}")
    return nz


def cli_compare(cli_dir, batch_dir, tag):
    a = json.loads((Path(cli_dir) / f"{tag}.json").read_text())
    b = json.loads((Path(batch_dir) / f"{tag}.json").read_text())
    assert list(a.keys()) == list(b.keys()), "key order/set differs"
    compare_results(a, b, "CLI vs gpu_batch JSON")
    fa, fb = np.load(Path(cli_dir) / f"{tag}_frames.npz"), np.load(Path(batch_dir) / f"{tag}_frames.npz")
    for k in sorted(fa.files):
        if k not in fb.files:
            print(f"  frame {k}: not in batch file (frame set differs)")
            continue
        same = fa[k].dtype == fb[k].dtype and np.array_equal(fa[k], fb[k])
        d = 0.0 if same else float(np.max(np.abs(fa[k].astype(float) - fb[k].astype(float))))
        print(f"  frame {k}: dtype {fa[k].dtype}, {'identical' if same else f'max abs diff {d:.3e}'}")


def single_path(species, seed, arm, steps, kappa=3.0, food_sense=0.0):
    """What food_selection.main does, in-process, returning the final arrays."""
    r = fs.build_run(species, seed, arm, True, "per_channel", kappa, food_sense)
    A, G, F = r.A, r.G, r.F
    for _ in range(steps // 100):
        A, G, F, _, _ = nu.rollout_logged(A, G, F, r.w.light, r.p, r.w.bank, r.cfg, r.food, 100)
    return np.asarray(A), np.asarray(G), np.asarray(F), r


def arrays(steps):
    sp = SPECIES[0]
    A1, G1, F1, r = single_path(sp, 1, "treat", steps)
    s = sim(sp, [(1, "treat")], steps)
    for name, x, y in (("A", A1, s.final[0][0]), ("G", G1, s.final[1][0]), ("F", F1, s.final[2][0])):
        d = float(np.max(np.abs(x - y)))
        print(f"final {name}: {'bit-identical' if np.array_equal(x, y) else f'max abs diff {d:.3e} (max |x| {np.max(np.abs(x)):.3e})'}")
    A_h, G_h, F_h = (np.asarray(t) for t in (r.A, r.G, r.F))
    # metrics at the end: measure() on the single path's final arrays vs the batch's final row
    m1 = fs.measure(A1, G1, F1, r.u)
    mb = s.results[0][0]["final"]
    for k in m1:
        d = abs(m1[k] - mb[k])
        print(f"metric {k:18s} single {m1[k]!r:>24}  batch {mb[k]!r:>24}  {'identical' if d == 0 else f'diff {d:.3e}'}")


def batch4(steps):
    sp = SPECIES[0]
    pairs = [(s, "treat") for s in (1, 2, 3, 4)]
    big = sim(sp, pairs, steps)
    all_ok = True
    for i, pr in enumerate(pairs):
        one = sim(sp, [pr], steps)
        for name, j in (("A", 0), ("G", 1), ("F", 2)):
            x, y = big.final[j][i], one.final[j][0]
            same = np.array_equal(x, y)
            all_ok &= same
            if not same:
                print(f"  seed {pr[0]} {name}: max abs diff {float(np.max(np.abs(x - y))):.3e}")
        nz = compare_results(big.results[i][0], one.results[0][0], f"seed {pr[0]} JSON batch4 vs batch1")
        all_ok &= not nz
    print("batch4 vs 4x batch1:", "ALL IDENTICAL" if all_ok else "DIFFERENCES (listed above)")


def species_conservation(steps):
    for sp in SPECIES:
        pairs = [(1, a) for a in ARMS]
        on = sim(sp, pairs, steps)
        drifts = [r["max_rel_total_drift"] for r, _ in on.results]
        # food off: sum(A_tot * G) per genome row (incl. tag) and sum(A) must not move
        off = sim(sp, pairs, steps, food_on=False, fs_present=False, kappa=0.0)
        out = []
        for i, (s_, arm) in enumerate(pairs):
            r = off.runs[i]
            S0 = np.asarray(jnp.sum(r.G * jnp.sum(r.A, 0)[None], axis=(1, 2)))
            A, G = off.final[0][i], off.final[1][i]
            S = np.asarray(jnp.sum(jnp.asarray(G) * jnp.sum(jnp.asarray(A), 0)[None], axis=(1, 2)))
            M0 = float(jnp.sum(r.A))
            d = np.abs(S - S0) / M0
            out.append((float(d[:-1].max()), float(d[-1]), abs(float(np.sum(A)) - M0) / M0))
        print(f"{sp[12:]:9s} food on, kappa 3: max_rel_total_drift per arm {['%.2e' % d for d in drifts]}")
        print(f"{'':9s} food off: max|dS_row|/M functional {['%.2e' % o[0] for o in out]}, "
              f"tag {['%.2e' % o[1] for o in out]}, |dM|/M {['%.2e' % o[2] for o in out]}")


def pos_state(species):
    sys.path.insert(0, str(ROOT / "scripts"))
    import test_repulsion as tr
    w, cfg, p, G, _ = tr.setup(ROOT, species)
    n = cfg.size
    F = jnp.full((n, n), float(jnp.sum(w.A)) / n ** 2)
    return w, cfg, p, G, F


def hash_of(A, G, F):
    h = hashlib.sha256()
    for x in (A, G, F):
        h.update(np.asarray(x).tobytes())
    return h.hexdigest()


def hash_check(ref_root, steps):
    """kappa 0, food_sense 0 (cfg defaults): batch-of-1 and batch-of-3 element vs the pre-change engine hash."""
    for sp in SPECIES:
        ref = subprocess.run([sys.executable, str(ROOT / "scripts" / "test_repulsion.py"), "hash", str(ref_root), sp, str(steps)],
                             capture_output=True, text=True, check=True).stdout.strip()
        w, cfg, p, G, F = pos_state(sp)
        food = nu.Food()
        # same-process unbatched, current engine
        A, G1, F1 = w.A, G, F
        for _ in range(steps // 100):
            A, G1, F1 = nu.rollout(A, G1, F1, w.light, p, w.bank, cfg, food, 100)
        h_single = hash_of(A, G1, F1)
        # batch of 1 and a batch of 3 (same state three times) through the vmapped rollout
        res = {}
        for B in (1, 3):
            Ab, Gb, Fb = (jnp.stack([x] * B) for x in (w.A, G, F))
            for _ in range(steps // 100):
                Ab, Gb, Fb = gb.brollout(Ab, Gb, Fb, w.light, p, w.bank, cfg, food, 100)
            res[B] = [hash_of(Ab[i], Gb[i], Fb[i]) for i in range(B)]
        ok1 = res[1][0] == ref
        print(f"{sp[12:]:9s} pre-change engine {ref[:16]}  current unbatched {h_single[:16]} ({'==' if h_single == ref else '!='})  "
              f"batch1 {res[1][0][:16]} ({'==' if ok1 else '!='})  batch3 {[h[:16] for h in res[3]]} ({'all ==' if all(h == ref for h in res[3]) else '!='})")
        if not ok1:
            Ar = A
            Ab1, Gb1, Fb1 = (jnp.stack([x]) for x in (w.A, G, F))
            for _ in range(steps // 100):
                Ab1, Gb1, Fb1 = gb.brollout(Ab1, Gb1, Fb1, w.light, p, w.bank, cfg, food, 100)
            for n_, x, y in (("A", A, Ab1[0]), ("G", G1, Gb1[0]), ("F", F1, Fb1[0])):
                print(f"{'':9s}   batch1 vs unbatched {n_}: max abs diff {float(jnp.max(jnp.abs(x - y))):.3e}")


def main():
    mode = sys.argv[1]
    a = sys.argv[2:]
    get = lambda k, d: int(a[a.index(k) + 1]) if k in a else d
    steps = get("--steps", 300)
    if mode == "cli-compare":
        cli_compare(*a[:3])
    elif mode == "arrays":
        arrays(steps)
    elif mode == "batch4":
        batch4(steps)
    elif mode == "species":
        species_conservation(steps)
    elif mode == "hash":
        hash_check(Path(a[0]), steps)
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
