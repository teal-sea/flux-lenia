"""Many food-selection runs as ONE jax.vmap-batched computation (same engine, same metrics,
same per-run JSON as scripts/food_selection.py).

One invocation = one (species, cell) batch. Everything that is a jit static argument (Config
incl. kappa and food_sense, Food, transport, steps per chunk) is constant within the invocation;
the batch dimension is (seed, arm) only. The initial state of every element comes from
food_selection.build_run, the function the single-run CLI uses.

  python scripts/gpu_batch.py --species SPECIES_001_OSCILLIS --arms treat,neutral_plus,neutral_minus \\
      --seeds 1-50 --steps 30000 --sample-every 100 --frame-every 1000 --transport per_channel \\
      --kappa 3 --food-sense 0 --food 1 --batch 150 --outdir OUT [--device cpu|gpu]

Output in OUT: <species>_s<seed>_<arm>_food<0|1>.json and ..._frames.npz per run (schema of
food_selection.py), plus batch_log.json (one entry appended per invocation). Resume: a (seed, arm)
pair whose JSON exists is skipped, so re-running the same command after an interruption only does
the missing pairs (granularity: a whole batch, since JSONs are written when a batch finishes).

--food-sense absent  = food_selection.py without its 9th argument (no logged food flows, 5 float64
                       frames in the original; here frames come from --frame-every).
--food-sense X       = with the argument (X may be 0): logs food_eaten_cum / body_decayed_cum and
                       sat_frac every sample, float32 frames, adds food_sense/W1f keys.
JSON differences from food_selection.py: wall_seconds is the batch's device-loop wall time divided
by the batch size (a run-equivalent figure; compile time excluded); frames are written at every
multiple of --frame-every plus t=0 and the final step (food_selection.py uses a fixed quarter /
half set), so use --frame-every steps/2 for its food-sense frame set.
Blob statistics need scipy labelling, so each sample is copied to the host and measured there with
the very same food_selection.measure() (thread pool), while the device already runs the next chunk.
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from pathlib import Path
from types import SimpleNamespace


def _device_from_argv(argv):
    for i, a in enumerate(argv):
        if a == "--device" and i + 1 < len(argv):
            return argv[i + 1]
        if a.startswith("--device="):
            return a.split("=", 1)[1]
    return "gpu"


if _device_from_argv(sys.argv) == "cpu":          # must be decided before jax is imported
    os.environ["JAX_PLATFORMS"] = "cpu"

import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from engine import neural_field as nf  # noqa: E402
from engine import nutrient as nu  # noqa: E402
import food_selection as fs  # noqa: E402

assert jax.config.jax_enable_x64, "float64 is required (the conservation claim depends on it)"


# --------------------------------------------------------------------------- batched kernels


@partial(jax.jit, static_argnums=(6, 7, 8))
def brollout(A, G, F, light, p, bank, cfg, food, n_steps):
    """vmap of nu.rollout over the leading (seed, arm) axis; light, brain, bank shared."""
    return jax.vmap(lambda a, g, f: nu.rollout(a, g, f, light, p, bank, cfg, food, n_steps))(A, G, F)


@partial(jax.jit, static_argnums=(6, 7, 8))
def brollout_logged(A, G, F, light, p, bank, cfg, food, n_steps):
    return jax.vmap(lambda a, g, f: nu.rollout_logged(a, g, f, light, p, bank, cfg, food, n_steps))(A, G, F)


@partial(jax.jit, static_argnums=(6,))
def bsat(A, G, F, light, p, bank, cfg):
    return jax.vmap(lambda a, g, f: fs._sat(a, g, f, light, p, bank, cfg))(A, G, F)


def state_bytes_per_element(cfg) -> int:
    n = cfg.size
    return (cfg.channels + cfg.genome_dim + 1) * n * n * 8


def parse_seeds(text: str) -> list[int]:
    out = []
    for part in text.split(","):
        if "-" in part:
            a, b = part.split("-")
            out += list(range(int(a), int(b) + 1))
        else:
            out.append(int(part))
    return out


def _mem(compiled):
    try:
        m = compiled.memory_analysis()
        return {"argument": int(m.argument_size_in_bytes), "output": int(m.output_size_in_bytes),
                "temp": int(m.temp_size_in_bytes)}
    except Exception:       # backend without memory analysis
        return None


def device_memory_limit():
    try:
        return int(jax.devices()[0].memory_stats()["bytes_limit"])
    except Exception:
        return None


# --------------------------------------------------------------------------- the batch


def simulate(species, pairs, *, food_on, transport, kappa, food_sense, fs_present, steps,
             sample_every, frame_every, threads=8, log=print):
    """Run len(pairs) (seed, arm) elements as one batch. Returns SimpleNamespace(results, final,
    timing, mem). results[i] = (result_dict, frames_dict) in the food_selection.py schema."""
    assert steps % sample_every == 0, "steps must be a multiple of sample_every"
    assert frame_every % sample_every == 0, "frame_every must be a multiple of sample_every"
    B = len(pairs)
    t_build = time.time()
    runs = [fs.build_run(species, s, a, food_on, transport, kappa, food_sense) for s, a in pairs]
    r0 = runs[0]
    for r in runs[1:]:              # light, brain and kernel bank must be shared by the whole batch
        assert r.cfg == r0.cfg and r.food == r0.food
        assert np.array_equal(np.asarray(r.w.light), np.asarray(r0.w.light))
        assert all(np.array_equal(np.asarray(r.p[k]), np.asarray(r0.p[k])) for k in r0.p)
        assert all(np.array_equal(np.asarray(x), np.asarray(y)) for x, y in zip(r.w.bank, r0.w.bank))
    cfg, p, food, light, bank, u = r0.cfg, r0.p, r0.food, r0.w.light, r0.w.bank, r0.u
    A_h = np.stack([np.asarray(r.A) for r in runs])
    G_h = np.stack([np.asarray(r.G) for r in runs])
    F_h = np.stack([np.asarray(r.F) for r in runs])
    total0 = [r.total0 for r in runs]
    build_s = time.time() - t_build
    A, G, F = jnp.asarray(A_h), jnp.asarray(G_h), jnp.asarray(F_h)
    assert A.dtype == jnp.float64

    roll = brollout_logged if fs_present else brollout
    t_c = time.time()
    exe = roll.lower(A, G, F, light, p, bank, cfg, food, sample_every).compile()
    compile_s = time.time() - t_c
    mem = _mem(exe)
    sat_on = kappa != 0.0 or fs_present

    pool = ThreadPoolExecutor(max_workers=threads)

    def measure_all(Ah, Gh, Fh):
        return list(pool.map(lambda i: fs.measure(Ah[i], Gh[i], Fh[i], u), range(B)))

    def sat_rows():
        if not sat_on:
            return [{} for _ in range(B)]
        a, b = bsat(A, G, F, light, p, bank, cfg)
        a, b = np.asarray(a), np.asarray(b)
        return [{"sat_frac": float(a[i]), "sat_frac_without_repulsion": float(b[i])} for i in range(B)]

    keep = {t for t in range(0, steps + 1, frame_every)} | {0, steps}
    frames = [dict() for _ in range(B)]
    ty = np.float32 if fs_present else np.float64

    def snap(t, Ah, Gh, Fh):
        for i in range(B):
            frames[i][f"body_{t}"] = Ah[i].sum(0).astype(ty)
            frames[i][f"ancestry_{t}"] = np.clip((1.0 + Gh[i][-1]) / 2.0, 0.0, 1.0).astype(ty)
            frames[i][f"food_{t}"] = Fh[i].astype(ty)

    # t = 0
    sat0 = sat_rows()
    meas0 = measure_all(A_h, G_h, F_h)
    rows = [[m | s] for m, s in zip(meas0, sat0)]
    snap(0, A_h, G_h, F_h)
    ts = [0]
    eaten_cum, decayed_cum = np.zeros(B), np.zeros(B)
    eaten_s, decayed_s = [[0.0] for _ in range(B)], [[0.0] for _ in range(B)]

    n_chunks = steps // sample_every
    t0 = time.time()
    nxt = exe(A, G, F, light, p, bank)                       # dispatched, runs asynchronously
    t_first = None
    for k in range(1, n_chunks + 1):
        if fs_present:
            A, G, F, e_, d_ = nxt
        else:
            A, G, F = nxt
        t = k * sample_every
        A_h, G_h, F_h = np.asarray(A), np.asarray(G), np.asarray(F)   # blocks until chunk k is done
        if t_first is None:
            t_first = time.time() - t0
        sat_k = sat_rows()                                   # queued before chunk k+1
        if k < n_chunks:
            nxt = exe(A, G, F, light, p, bank)               # device works on k+1 while host measures k
        if fs_present:
            e_h, d_h = np.asarray(e_), np.asarray(d_)
            for i in range(B):
                eaten_cum[i] += float(e_h[i]); decayed_cum[i] += float(d_h[i])
                eaten_s[i].append(float(eaten_cum[i])); decayed_s[i].append(float(decayed_cum[i]))
        meas = measure_all(A_h, G_h, F_h)
        for i in range(B):
            rows[i].append(meas[i] | sat_k[i])
        ts.append(t)
        if t in keep:
            snap(t, A_h, G_h, F_h)
        if k % max(1, n_chunks // 10) == 0 or k == n_chunks:
            log(f"  t={t}/{steps}  {time.time() - t0:.0f}s elapsed")
    wall = time.time() - t0
    pool.shutdown()

    results = []
    for i, (seed, arm) in enumerate(pairs):
        series = {k: [r_[k] for r_ in rows[i]] for k in rows[i][0]}
        if fs_present:
            series["food_eaten_cum"], series["body_decayed_cum"] = eaten_s[i], decayed_s[i]
        tail = max(1, len(ts) // 10)
        totals = [b + f for b, f in zip(series["body"], series["food"])]
        share_end = float(np.mean(series["share_A"][-tail:]))
        (ya, xa), (yb, xb) = runs[i].centres
        result = {
            "species": species, "seed": seed, "arm": arm, "food": food_on, "steps": steps,
            "sample_every": sample_every, "genome_transport": transport,
            "repulsion_kappa": kappa, "repulsion_radius": cfg.repulsion_radius,
            "repulsion_genome_dims": cfg.repulsion_genome_dims,
            **({"food_sense": food_sense,
                "W1f_seed": None if "W1f" in runs[i].data["params"] else nf.food_weight_seed(species),
                "W1f_seed_rule": "params['W1f']" if "W1f" in runs[i].data["params"] else "crc32('W1f|<species id>')",
                "food_eaten_total": float(eaten_cum[i]), "body_decayed_total": float(decayed_cum[i])}
               if fs_present else {}),
            "food_params": dataclasses.asdict(food),
            "genome_A_sign": fs.ARMS[arm][0], "genome_B_sign": fs.ARMS[arm][1],
            "spawn_centres": [[ya, xa], [yb, xb]], "lineage_axis_seed": fs.U_SEED,
            "wall_seconds": wall / B,
            "max_rel_total_drift": float(max(abs(x - total0[i]) / total0[i] for x in totals)),
            "share_A_start": series["share_A"][0],
            "share_A_end": share_end,
            "delta_share_A": share_end - series["share_A"][0],
            "final": rows[i][-1], "t": ts, "series": series,
        }
        results.append((result, frames[i]))
    return SimpleNamespace(
        results=results, final=(A_h, G_h, F_h), runs=runs, cfg=cfg, p=p, light=light, bank=bank,
        timing={"batch": B, "build_seconds": build_s, "compile_seconds": compile_s,
                "loop_seconds": wall, "first_chunk_seconds": t_first,
                "ms_per_batched_step": 1000.0 * wall / steps,
                "ms_per_run_step": 1000.0 * wall / steps / B},
        mem=mem, exe=exe)


def estimate(species, pairs, args, cfg_probe=None):
    """Compile (no execution) for the given pairs and report the memory the device would need."""
    r = fs.build_run(species, pairs[0][0], pairs[0][1], bool(args.food), args.transport, args.kappa,
                     args.food_sense or 0.0)
    B = len(pairs)
    mk = lambda *s: jnp.zeros((B,) + s)
    n = r.cfg.size
    A, G, F = mk(r.cfg.channels, n, n), mk(r.cfg.genome_dim, n, n), mk(n, n)
    roll = brollout_logged if args.food_sense is not None else brollout
    exe = roll.lower(A, G, F, r.w.light, r.p, r.w.bank, r.cfg, r.food, args.sample_every).compile()
    return r.cfg, _mem(exe)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--species", required=True)
    ap.add_argument("--arms", default="treat,neutral_plus,neutral_minus")
    ap.add_argument("--seeds", required=True, help="e.g. 1-50 or 1,3,5-7")
    ap.add_argument("--steps", type=int, default=30000)
    ap.add_argument("--sample-every", type=int, default=100)
    ap.add_argument("--frame-every", type=int, default=1000)
    ap.add_argument("--transport", default="per_channel")
    ap.add_argument("--kappa", type=float, default=0.0)
    ap.add_argument("--food-sense", type=float, default=None, help="absent = off and not logged; 0 = off but logged")
    ap.add_argument("--food", type=int, default=1)
    ap.add_argument("--batch", type=int, default=150, help="max (seed, arm) elements per vmap batch")
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--device", default="gpu", choices=["cpu", "gpu"])
    ap.add_argument("--threads", type=int, default=min(16, os.cpu_count() or 4), help="host threads for blob statistics")
    ap.add_argument("--estimate-only", action="store_true", help="compile, print the memory estimate, exit")
    ap.add_argument("--mem-fraction", type=float, default=0.85, help="auto-shrink --batch to fit this fraction of device memory")
    a = ap.parse_args(argv)

    plat = jax.devices()[0].platform
    if a.device == "gpu" and plat not in ("gpu", "cuda", "rocm"):
        raise SystemExit(f"--device gpu but jax sees {jax.devices()}; refusing to run a GPU campaign on {plat}")
    out = Path(a.outdir)
    out.mkdir(parents=True, exist_ok=True)
    fs_present = a.food_sense is not None
    food_sense = a.food_sense or 0.0
    arms = a.arms.split(",")
    seeds = parse_seeds(a.seeds)
    food_on = bool(a.food)
    tagname = lambda s, arm: f"{a.species}_s{s}_{arm}_food{int(food_on)}"
    todo = [(s, arm) for s in seeds for arm in arms if not (out / f"{tagname(s, arm)}.json").exists()]
    print(f"{a.species}: {len(seeds) * len(arms)} runs requested, {len(todo)} to do "
          f"({len(seeds) * len(arms) - len(todo)} already present); devices {jax.devices()}; jax {jax.__version__}", flush=True)
    if not todo and not a.estimate_only:
        return

    B = min(a.batch, len(todo)) if todo else a.batch
    probe = todo[:B] if todo else [(seeds[0], arms[0])] * B
    cfg, mem = estimate(a.species, probe, a)
    per_state = state_bytes_per_element(cfg)
    print(f"memory estimate per element: state (A,G,F float64) {per_state / 1e6:.2f} MB", flush=True)
    limit = device_memory_limit()
    if mem:
        need = mem["argument"] + mem["output"] + mem["temp"]
        print(f"compiled batch {B}: arguments {mem['argument'] / 1e9:.2f} GB + outputs {mem['output'] / 1e9:.2f} GB + "
              f"temp {mem['temp'] / 1e9:.2f} GB = {need / 1e9:.2f} GB ({need / B / 1e6:.2f} MB per element)"
              + (f"; device limit {limit / 1e9:.1f} GB" if limit else "; device limit unknown"), flush=True)
        if limit and need > a.mem_fraction * limit:
            B2 = max(1, int(B * a.mem_fraction * limit / need))
            print(f"  batch {B} needs {need / limit:.0%} of device memory; shrinking to {B2}", flush=True)
            B = B2
    else:
        print("memory analysis unavailable on this backend; state size only", flush=True)
    if a.estimate_only:
        return

    log_path = out / "batch_log.json"
    t_all = time.time()
    entries = []
    for i in range(0, len(todo), B):
        chunk = todo[i:i + B]
        print(f"batch {i // B + 1}/{-(-len(todo) // B)}: {len(chunk)} runs, seeds {chunk[0][0]}..{chunk[-1][0]}", flush=True)
        sim = simulate(a.species, chunk, food_on=food_on, transport=a.transport, kappa=a.kappa,
                       food_sense=food_sense, fs_present=fs_present, steps=a.steps,
                       sample_every=a.sample_every, frame_every=a.frame_every, threads=a.threads,
                       log=lambda m: print(m, flush=True))
        for (result, frames), (s, arm) in zip(sim.results, chunk):
            tg = tagname(s, arm)
            np.savez_compressed(out / f"{tg}_frames.npz", **frames)
            (out / f"{tg}.json.tmp").write_text(json.dumps(result))
            os.replace(out / f"{tg}.json.tmp", out / f"{tg}.json")      # JSON last: its presence = run complete
        drift = max(r["max_rel_total_drift"] for r, _ in sim.results)
        entries.append({**sim.timing, "max_rel_total_drift": drift, "memory_analysis": sim.mem})
        print(f"  done: {sim.timing['ms_per_batched_step']:.2f} ms per batched step "
              f"({sim.timing['ms_per_run_step']:.3f} ms per run-step; CPU reference 27.9), "
              f"max total drift {drift:.2e}", flush=True)
    entry = {
        "species": a.species, "device": str(jax.devices()[0]), "platform": plat, "jax": jax.__version__,
        "argv": sys.argv[1:], "started_unix": t_all, "total_wall_seconds": time.time() - t_all,
        "runs_done": len(todo), "batch_size": B, "state_bytes_per_element": per_state,
        "kappa": a.kappa, "food_sense": a.food_sense, "transport": a.transport, "steps": a.steps,
        "max_rel_total_drift": max(e["max_rel_total_drift"] for e in entries),
        "ms_per_batched_step": float(np.mean([e["ms_per_batched_step"] for e in entries])),
        "batches": entries,
    }
    log = json.loads(log_path.read_text()) if log_path.exists() else []
    log.append(entry)
    log_path.write_text(json.dumps(log, indent=1))
    print(json.dumps({k: entry[k] for k in ("runs_done", "total_wall_seconds", "ms_per_batched_step",
                                            "max_rel_total_drift")}), flush=True)


if __name__ == "__main__":
    main()
