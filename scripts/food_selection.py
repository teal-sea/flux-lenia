"""Does food make one lineage take over? (ROADMAP steps 3 and 4, two lineages.)

Two blobs of one species, identical in shape and mass, at the same seeded positions as the
variance-decay experiment. Each carries a neutral tag (+1 for lineage A, -1 for B) that the
brain cannot read, so ancestry is measured by the tag, independent of the functional genome.

Arms:
  treat          A has functional genome +u, B has -u           (genetic difference)
  neutral_plus   both +u                                         (no genetic difference)
  neutral_minus  both -u                                         (no genetic difference)
Food: 1 = food field at the start equal in total to the body mass, uniform; 0 = no food
(the plain conserved-mass dish).

Per cell, a = (1 + tag) / 2 is the fraction of lineage-A ancestry. Lineage A's share of the
dish is sum(A_tot * a) / sum(A_tot), mass-weighted over body only.

Usage:
  python scripts/food_selection.py SPECIES SEED ARM FOOD STEPS OUTDIR [TRANSPORT [KAPPA [FOOD_SENSE]]]
TRANSPORT is 'mean' (default, the original scheme) or 'per_channel' (docs/GENOME-TRANSPORT-2026-11-10.md).
KAPPA (default 0 = off, behaviour unchanged) is Config.repulsion_kappa, the self/non-self contact
repulsion of docs/CONDITIONAL-BLENDING-2026-11-15.md. With KAPPA > 0 each sample also records the
fraction of (channel, cell) velocities at the soft bound, with and without the repulsion term.
FOOD_SENSE (default absent = 0 = off, behaviour unchanged) is Config.food_sense, the food field as brain
input (docs/FOOD-SENSING-2026-11-16.md). When the argument is present (even as 0) the run also logs
cumulative food eaten and body decayed, sat_frac every sample, and records food_sense and the W1f seed.
"""

from __future__ import annotations

import dataclasses
import json
import sys
import time
from pathlib import Path
from types import SimpleNamespace

import jax
import jax.numpy as jnp
import numpy as np
from functools import partial

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine import neural_field as nf  # noqa: E402
from engine import novelty_oracle as no  # noqa: E402
from engine import nutrient as nu  # noqa: E402

SAMPLE = 100
U_SEED = 20261103          # same lineage axis as scripts/variance_decay.py
MIN_SEP = 40.0
ARMS = {"treat": (+1, -1), "neutral_plus": (+1, +1), "neutral_minus": (-1, -1)}
FOOD = nu.Food()           # the parameters fixed in docs/FOOD-SELECTION-2026-11-09.md


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


BOUND_FRAC = 0.9           # a velocity is 'at the soft bound' if |d| >= 0.9 * max_step
BODY_MIN = 0.05            # ... counted over (channel, cell) pairs holding at least this much of that channel


@partial(jax.jit, static_argnums=(6,))
def _sat(A, G, F, light, p, bank, cfg):
    """Fractions of body (channel, cell) velocities at the soft bound: (with repulsion, without)."""
    khat, ksrc = bank
    U = nf.perceive(A, khat, ksrc)
    Ff = nf.food_features(F, p, bank, cfg) if cfg.food_sense != 0.0 else None
    E, gain, theta = nf.sensorimotor(U, A, G, light, p, cfg, Ff)
    body = A >= BODY_MIN
    n = jnp.maximum(jnp.sum(body), 1)
    out = []
    for c in (cfg, dataclasses.replace(cfg, repulsion_kappa=0.0)):
        dy, dx = nf.flow_field(E, gain, theta, A, c, G)
        hit = jnp.sqrt(dy ** 2 + dx ** 2) >= BOUND_FRAC * cfg.max_step
        out.append(jnp.sum(hit & body) / n)
    return out[0], out[1]


def measure(A, G, F, u) -> dict:
    m = A.sum(axis=0)
    M = float(m.sum())
    w = m / M
    a = np.clip((1.0 + G[-1]) / 2.0, 0.0, 1.0)
    s = np.tensordot(u, G[:-1], axes=(0, 0))
    blobs = no.extract_blobs(A)
    ba = [float((m[b.mask] * a[b.mask]).sum() / m[b.mask].sum()) for b in blobs]
    bm = [float(b.mass) for b in blobs]
    big = max(bm) / M if bm else 0.0
    return {
        "body": M,
        "food": float(F.sum()),
        "share_A": float((w * a).sum()),
        "hybrid_frac": float(w[(a > 0.1) & (a < 0.9)].sum()),
        "pure_frac": float(w[np.abs(G[-1]) > 0.8].sum()),
        "mean_s": float((w * s).sum()),
        "n_blobs": len(blobs),
        "n_blobs_A": sum(1 for x in ba if x > 0.9),
        "n_blobs_B": sum(1 for x in ba if x < 0.1),
        "n_blobs_mixed": sum(1 for x in ba if 0.1 <= x <= 0.9),
        "largest_blob_frac": big,
        "max_density": float(m.max()),
    }


def build_run(species: str, seed: int, arm: str, food_on: bool, transport: str = "mean",
              kappa: float = 0.0, food_sense: float = 0.0) -> SimpleNamespace:
    """Everything one run needs before its first step (shared by scripts/gpu_batch.py).

    Returns a namespace with: data, w (World), cfg, params (numpy, tagged), p (jax), food, u,
    A, G, F (initial state), M0, total0, centres ((ya, xa), (yb, xb))."""
    data = json.loads((ROOT / "outputs" / "species" / f"{species}_genome.json").read_text())
    w = nf.World.from_json(data, seed=seed)
    w.cfg = dataclasses.replace(w.cfg, advect_genome=True, genome_transport=transport)
    cfg, params = nu.tagged(w.cfg, {k: np.asarray(v) for k, v in w.params.items()})
    if kappa != 0.0:
        cfg = dataclasses.replace(cfg, repulsion_kappa=kappa)
    if food_sense != 0.0:
        cfg = dataclasses.replace(cfg, food_sense=food_sense)
        params = dict(params, W1f=nf.sample_food_weights(species, cfg))
    p = nf.params_to_jax(params)
    food = FOOD if food_on else nu.Food(enabled=False)

    u = lineage_axis(w.cfg.genome_dim)
    (ya, xa), (yb, xb) = placements(seed, w.cfg.size)
    r, peak = float(data["spawn_radius"]), float(data["spawn_peak"])
    ga, gb = (sgn * u for sgn in ARMS[arm])
    # same noise seed for both blobs: identical shape, channel mix and mass
    w.spawn(ya, xa, ga, radius=r, peak=peak, seed=1000 + seed)
    m_a = np.asarray(jnp.sum(w.A, axis=0))
    w.spawn(yb, xb, gb, radius=r, peak=peak, seed=1000 + seed)
    m_b = np.asarray(jnp.sum(w.A, axis=0)) - m_a
    tag = np.where(m_a + m_b > 0, (m_a - m_b) / np.maximum(m_a + m_b, 1e-300), 0.0)
    A = w.A
    G = jnp.concatenate([w.Gf, jnp.asarray(tag)[None]], axis=0)
    M0 = float(jnp.sum(A))
    n = w.cfg.size
    F = jnp.full((n, n), M0 / n ** 2) if food_on else jnp.zeros((n, n))
    total0 = M0 + float(jnp.sum(F))
    return SimpleNamespace(data=data, w=w, cfg=cfg, params=params, p=p, food=food, u=u, A=A, G=G,
                           F=F, M0=M0, total0=total0, centres=((ya, xa), (yb, xb)))


def main() -> None:
    species, seed, arm, food_on, steps, outdir = sys.argv[1:7]
    transport = sys.argv[7] if len(sys.argv) > 7 else "mean"
    kappa = float(sys.argv[8]) if len(sys.argv) > 8 else 0.0
    food_sense_arg = len(sys.argv) > 9
    food_sense = float(sys.argv[9]) if food_sense_arg else 0.0
    seed, food_on, steps = int(seed), bool(int(food_on)), int(steps)
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)

    run = build_run(species, seed, arm, food_on, transport, kappa, food_sense)
    w, cfg, p, food, u = run.w, run.cfg, run.p, run.food, run.u
    A, G, F, total0 = run.A, run.G, run.F, run.total0
    (ya, xa), (yb, xb) = run.centres

    t, ts = 0, [0]
    def sat(A, G, F):
        if kappa == 0.0 and not food_sense_arg:
            return {}
        a, b = _sat(A, G, F, w.light, p, w.bank, cfg)
        return {"sat_frac": float(a), "sat_frac_without_repulsion": float(b)}

    rows = [measure(np.asarray(A), np.asarray(G), np.asarray(F), u) | sat(A, G, F)]
    keep = {0, steps // 4, steps // 2, 3 * steps // 4, steps}
    if food_sense_arg:           # 1,800-run campaign: 3 float32 frames per run keep the npz total near 1 GB
        keep = {0, steps // 2, steps}
    frames = {}

    def snap(t, A, G, F):
        A_, G_ = np.asarray(A), np.asarray(G)
        ty = np.float32 if food_sense_arg else np.float64
        frames[f"body_{t}"] = A_.sum(0).astype(ty)
        frames[f"ancestry_{t}"] = np.clip((1.0 + G_[-1]) / 2.0, 0.0, 1.0).astype(ty)
        frames[f"food_{t}"] = np.asarray(F).astype(ty)

    snap(0, A, G, F)
    eaten_cum, decayed_cum, eaten_s, decayed_s = 0.0, 0.0, [0.0], [0.0]
    t0 = time.time()
    while t < steps:
        if food_sense_arg:
            A, G, F, e_, d_ = nu.rollout_logged(A, G, F, w.light, p, w.bank, cfg, food, SAMPLE)
            eaten_cum += float(e_); decayed_cum += float(d_)
            eaten_s.append(eaten_cum); decayed_s.append(decayed_cum)
        else:
            A, G, F = nu.rollout(A, G, F, w.light, p, w.bank, cfg, food, SAMPLE)
        t += SAMPLE
        ts.append(t)
        rows.append(measure(np.asarray(A), np.asarray(G), np.asarray(F), u) | sat(A, G, F))
        if t in keep:
            snap(t, A, G, F)
    wall = time.time() - t0

    series = {k: [r_[k] for r_ in rows] for k in rows[0]}
    if food_sense_arg:
        series["food_eaten_cum"], series["body_decayed_cum"] = eaten_s, decayed_s
    tail = max(1, len(ts) // 10)
    totals = [b + f for b, f in zip(series["body"], series["food"])]
    share_end = float(np.mean(series["share_A"][-tail:]))
    result = {
        "species": species, "seed": seed, "arm": arm, "food": food_on, "steps": steps,
        "sample_every": SAMPLE, "genome_transport": transport,
        "repulsion_kappa": kappa, "repulsion_radius": cfg.repulsion_radius,
        "repulsion_genome_dims": cfg.repulsion_genome_dims,
        **({"food_sense": food_sense, "W1f_seed": nf.food_weight_seed(species),
            "W1f_seed_rule": "crc32('W1f|<species id>')",
            "food_eaten_total": eaten_cum, "body_decayed_total": decayed_cum} if food_sense_arg else {}),
        "food_params": dataclasses.asdict(food),
        "genome_A_sign": ARMS[arm][0], "genome_B_sign": ARMS[arm][1],
        "spawn_centres": [[ya, xa], [yb, xb]], "lineage_axis_seed": U_SEED,
        "wall_seconds": wall,
        "max_rel_total_drift": float(max(abs(x - total0) / total0 for x in totals)),
        "share_A_start": series["share_A"][0],
        "share_A_end": share_end,
        "delta_share_A": share_end - series["share_A"][0],
        "final": rows[-1], "t": ts, "series": series,
    }
    tag_ = f"{species}_s{seed}_{arm}_food{int(food_on)}"
    (out / f"{tag_}.json").write_text(json.dumps(result))
    np.savez_compressed(out / f"{tag_}_frames.npz", **frames)
    print(json.dumps({k: result[k] for k in ("species", "seed", "arm", "food", "wall_seconds",
                                             "max_rel_total_drift", "share_A_start",
                                             "share_A_end")}
                     | {"body_end": rows[-1]["body"], "food_end": rows[-1]["food"],
                        "n_blobs_end": rows[-1]["n_blobs"],
                        "largest_blob_frac": rows[-1]["largest_blob_frac"]}))


if __name__ == "__main__":
    main()
