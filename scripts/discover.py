#!/usr/bin/env python3
"""Open-ended discovery loop for reproducing Neural Flow Lenia species.

Two phases:

    screen   Sample random brains, run each world, gate it, and log every
             candidate with its numbers. Shardable across processes.
    curate   Read the screening log; if fewer than --target reproducers were
             found, hill-climb by mutating the most promising viable brains;
             then deeply verify the winners (phototaxis with a moving lamp,
             pursuit, cyclical locomotion), record media, and write reports.

Usage:
    python scripts/discover.py screen --n 24 --shard 0 --nshards 4
    python scripts/discover.py curate --target 3

Reproduction here means fission: a mass-conserving world cannot manufacture
a second organism, so an organism reproduces by dividing what it has into
bodies that then survive on their own. Every candidate is logged whether it
passes or not, and a run that finds nothing says so with the reason.
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from engine import neural_field as nf          # noqa: E402
from engine import novelty_oracle as no        # noqa: E402
from engine import render as rd                # noqa: E402

HUNTS = ROOT / "hunts"
OUTPUTS = ROOT / "outputs"
SCREEN_DIR = HUNTS / "_screen"
SPECIES_DIR = OUTPUTS / "species"

STEPS = 720
SAMPLE_EVERY = 12

# The brain alone does not decide whether a body divides: how hard mass
# resists piling up (alpha) and how much mass the world starts with relative
# to the species' preferred body size matter just as much. Both are searched.
# Alpha is quantized because it is a static jit argument, so each distinct
# value costs one compilation.
ALPHA_CHOICES = (0.20, 0.35, 0.55, 0.80)
SPAWN_CHOICES = ((16.0, 0.9), (20.0, 1.2), (26.0, 1.4))


@dataclass
class Candidate:
    """Everything needed to reproduce one world exactly."""

    seed: int
    cfg: nf.Config
    spec: nf.KernelSpec
    params: dict
    spawn_radius: float
    spawn_peak: float


def sample_candidate(seed: int, base: nf.Config | None = None) -> Candidate:
    base = base or nf.Config(advect_genome=False)
    rng = np.random.default_rng(seed)
    spec = nf.KernelSpec.sample(rng, base)
    params = nf.sample_params(rng, base)
    alpha = float(ALPHA_CHOICES[int(rng.integers(len(ALPHA_CHOICES)))])
    radius, peak = SPAWN_CHOICES[int(rng.integers(len(SPAWN_CHOICES)))]
    return Candidate(seed, dataclasses.replace(base, alpha=alpha), spec,
                     params, radius, peak)


# --------------------------------------------------------------------------
# One candidate
# --------------------------------------------------------------------------


def build_world(c: Candidate, light=None) -> nf.World:
    w = nf.World(c.cfg, c.spec, c.params, seed=c.seed)
    w.light_pos = None
    w.spawn(c.cfg.size / 2, c.cfg.size / 2, np.zeros(c.cfg.genome_dim),
            radius=c.spawn_radius, peak=c.spawn_peak, seed=c.seed)
    if light is not None:
        w.set_light(*light)
    return w


def evaluate(c: Candidate, steps: int = STEPS,
             sample_every: int = SAMPLE_EVERY, keep_frames: bool = False):
    """Run one world and put it through the oracle. Returns (record, world,
    tracker, frames)."""
    cfg, seed = c.cfg, c.seed
    w = build_world(c)
    tracker = no.SpeciationTracker(size=cfg.size)
    frames, mass, images = [], [float(w.mass())], []

    A0 = np.asarray(w.A)
    tracker.update(A0)
    frames.append(no.frame_complexity(A0))
    if keep_frames:
        images.append(A0)

    for _ in range(steps // sample_every):
        m = w.run(sample_every)
        mass.extend(np.asarray(m).tolist())
        A = np.asarray(w.A)
        if not np.all(np.isfinite(A)):
            break
        tracker.update(A)
        frames.append(no.frame_complexity(A))
        if keep_frames:
            images.append(A)

    gates = no.viability_gates(np.asarray(mass), frames, tracker)
    # Strict count is what "reproducing" means here; the raw count is kept
    # alongside it so the gap between "it split off something" and "it
    # divided" stays visible instead of being quietly collapsed.
    repro = tracker.reproduction_events(min_child_life=6)
    raw = tracker.reproduction_events(min_child_life=6, min_mass_frac=0.0)
    best_frac = max((max(e["child_mass_frac"]) for e in raw
                     if e.get("child_mass_frac")), default=0.0)

    # The bouncer watches every candidate, not just the finalists: these two
    # detectors read the track record we already have, so screening every
    # world for them costs nothing extra. Phototaxis needs its own controlled
    # runs with a moving lamp, so it is deferred to curation.
    bouncer = [no.detect_pursuit(tracker), no.detect_cyclic_locomotion(tracker)]

    fin = frames[-1]
    span = frames[len(frames) // 2:]
    record = {
        "seed": seed,
        "alpha": float(cfg.alpha),
        "spawn_radius": float(c.spawn_radius),
        "spawn_peak": float(c.spawn_peak),
        "viable": all(g.passed for g in gates),
        "gates": [asdict(g) for g in gates],
        "n_reproduction": len(repro),
        "n_fission_raw": len(raw),
        "best_child_mass_frac": float(best_frac),
        "n_organisms": len(tracker.organisms),
        "n_survivors": len(tracker.survivors(min_life=5)),
        "max_generation": max((o.generation for o in tracker.organisms.values()),
                              default=0),
        "second_share": float(np.mean([f["second_share"] for f in span])),
        "n_major": float(np.mean([f["n_major"] for f in span])),
        "morph_diversity": float(np.mean([f["morph_diversity"] for f in span])),
        "spatial_mi": float(np.mean([f["spatial_mi"] for f in span])),
        "cross_channel_mi": float(np.mean([f["cross_channel_mi"] for f in span])),
        "euler_final": int(fin["euler"]),
        "concentration_final": float(fin["concentration"]),
        "occupancy_final": float(fin["occupancy"]),
        "n_blobs_final": int(fin["n_blobs"]),
        "anomalies": {a.kind: a.as_dict() for a in bouncer},
        "flagged": [a.kind for a in bouncer if a.established],
        "mass_drift": float([g for g in gates if g.name == "mass_conservation"][0].value),
        "activity": float([g for g in gates if g.name == "activity"][0].value)
        if any(g.name == "activity" for g in gates) else 0.0,
    }
    record["score"] = score_of(record)
    return record, w, tracker, images


def score_of(r: dict) -> float:
    """Division dominates; the rest shapes the climb toward it.

    The strict division count is nearly always 0, which gives a mutation
    search no direction. `second_share` (how big the second body is relative
    to the first) and `best_child_mass_frac` (the largest offspring a fission
    ever produced) are continuous stand-ins that rise smoothly as a lineage
    approaches genuine division, so the hill-climb has something to follow.
    """
    if not r["viable"]:
        return -1.0
    return (8.0 * min(r["n_reproduction"], 4)
            + 6.0 * min(r.get("second_share", 0.0), 1.0)
            + 5.0 * min(r.get("best_child_mass_frac", 0.0), 0.5)
            + 1.0 * max(r.get("n_major", 1.0) - 1.0, 0.0)
            + 1.0 * r["morph_diversity"]
            + 0.8 * r["spatial_mi"]
            + 0.6 * r["cross_channel_mi"]
            + 3.0 * min(r["activity"], 0.5))


# --------------------------------------------------------------------------
# Screen phase
# --------------------------------------------------------------------------


def cmd_screen(args) -> int:
    SCREEN_DIR.mkdir(parents=True, exist_ok=True)
    cfg = nf.Config(advect_genome=False)
    # Filename carries the seed base so a second batch adds to the pool
    # instead of overwriting the first one's results.
    out = SCREEN_DIR / f"shard_{args.base}_{args.shard}.jsonl"
    seeds = [s for s in range(args.base, args.base + args.n * args.nshards)
             if s % args.nshards == args.shard]

    t0 = time.time()
    n_viable = n_repro = 0
    with out.open("w") as fh:
        for i, seed in enumerate(seeds):
            try:
                rec, *_ = evaluate(sample_candidate(seed, cfg))
            except Exception as e:                    # log, never swallow
                rec = {"seed": seed, "viable": False, "error": repr(e),
                       "score": -1.0, "n_reproduction": 0}
            rec["origin"] = "random"
            fh.write(json.dumps(rec, default=float) + "\n")
            fh.flush()
            n_viable += bool(rec.get("viable"))
            n_repro += bool(rec.get("n_reproduction", 0))
            flags = rec.get("flagged") or []
            print(f"[shard {args.shard}] {i+1}/{len(seeds)} seed={seed} "
                  f"viable={rec.get('viable')} "
                  f"repro={rec.get('n_reproduction')}"
                  f"/{rec.get('n_fission_raw')} raw "
                  f"(best child {rec.get('best_child_mass_frac', 0):.1%}) "
                  f"score={rec.get('score', -1):.2f} "
                  f"flagged={','.join(flags) if flags else '-'} "
                  f"({time.time() - t0:.0f}s)", flush=True)

    print(f"[shard {args.shard}] done: {len(seeds)} screened, {n_viable} viable, "
          f"{n_repro} with reproduction, {time.time() - t0:.0f}s", flush=True)
    return 0


# --------------------------------------------------------------------------
# Hill-climb phase
# --------------------------------------------------------------------------


def hill_climb(cfg, seeds: list[int], target: int, budget: int,
               already: list[dict], generations: int = 10) -> list[dict]:
    """Mutate promising brains looking for reproduction.

    Novelty pressure: a mutant only replaces its parent if it scores higher,
    and each lineage is abandoned once it has yielded a reproducer so the
    search does not return three copies of one species.
    """
    found = list(already)
    evaluated = 0
    rng_master = np.random.default_rng(90210)

    for base_seed in seeds:
        if len(found) >= target or evaluated >= budget:
            break
        base = sample_candidate(base_seed, cfg)
        best_rec, *_ = evaluate(base)
        best = base

        print(f"  lineage from seed {base_seed} (alpha={base.cfg.alpha}, "
              f"spawn r={base.spawn_radius}): start score "
              f"{best_rec['score']:.2f} second_share="
              f"{best_rec.get('second_share', 0):.2f}", flush=True)

        for gen in range(generations):
            if len(found) >= target or evaluated >= budget:
                break
            sigma = 0.15 if gen < generations // 2 else 0.06
            mrng = np.random.default_rng(int(rng_master.integers(1 << 30)))
            cand = dataclasses.replace(
                best, params=nf.mutate_params(best.params, mrng, sigma=sigma))
            rec, *_ = evaluate(cand)
            evaluated += 1
            rec["origin"] = f"mutant:{base_seed}:g{gen}"
            print(f"    gen {gen}: score {rec['score']:.2f} "
                  f"repro={rec['n_reproduction']} "
                  f"second_share={rec.get('second_share', 0):.2f} "
                  f"best_child={rec.get('best_child_mass_frac', 0):.1%} "
                  f"viable={rec['viable']}", flush=True)
            if rec["score"] > best_rec["score"]:
                best_rec, best = rec, cand
            if rec["viable"] and rec["n_reproduction"] > 0:
                found.append({"record": rec, "candidate": cand})
                print(f"    -> DIVIDER found in lineage {base_seed}",
                      flush=True)
                break
    return found


# --------------------------------------------------------------------------
# Deep verification and reporting
# --------------------------------------------------------------------------


def phototaxis_probe(c: Candidate, steps: int = 400) -> no.Anomaly:
    """Move the lamp and see whether the organism follows it."""
    n = c.cfg.size

    def run_fn(pos):
        w = build_world(c, light=(pos[0], pos[1]))
        start = no.field_centroid(np.asarray(w.A))
        w.run(steps)
        return start, no.field_centroid(np.asarray(w.A))

    lamps = [(n * 0.20, n * 0.5), (n * 0.80, n * 0.5), (n * 0.5, n * 0.20)]
    return no.detect_phototaxis(run_fn, n, lamps, steps)


def record_species(c: Candidate, tag: str) -> dict:
    """Re-run with frame capture, then write PNG, GIF and MP4."""
    OUTPUTS.mkdir(exist_ok=True)
    cfg = c.cfg
    w = build_world(c)
    tracker = no.SpeciationTracker(size=cfg.size)

    frames_rgb, centroid_frames = [], []
    n_frames, every = 150, 6
    tracker.update(np.asarray(w.A))
    for _ in range(n_frames):
        w.run(every)
        A = np.asarray(w.A)
        blobs = tracker.update(A)
        img = rd.upscale(rd.composite(A), 4)
        img = rd.draw_flow(img, np.asarray(w.dy), np.asarray(w.dx), scale_up=4,
                           stride=8, gain=9.0)
        img = rd.draw_markers(img, [b.centroid for b in blobs], scale_up=4)
        frames_rgb.append(img)
        centroid_frames.append([b.centroid for b in blobs])

    from PIL import Image
    png = OUTPUTS / f"{tag}_final.png"
    Image.fromarray(rd.to_uint8(frames_rgb[-1])).save(png)

    gif = rd.save_gif(frames_rgb[::2], OUTPUTS / f"{tag}.gif", fps=18)
    mp4 = rd.save_mp4(frames_rgb, OUTPUTS / f"{tag}.mp4", fps=30)

    media = {"png": png.name, "gif": gif.name,
             "mp4": mp4.name if mp4 else None,
             "frames": len(frames_rgb), "steps_recorded": n_frames * every}
    if mp4 is None:
        media["mp4_note"] = "ffmpeg not on PATH; GIF written instead"
    return {"media": media, "tracker": tracker}


def write_report(idx: int, name: str, rec: dict, anomalies: list[no.Anomaly],
                 tracker: no.SpeciationTracker, media: dict,
                 genome_path: Path) -> Path:
    HUNTS.mkdir(exist_ok=True)
    path = HUNTS / f"SPECIES_{idx:03d}_{name}.md"
    # Both counts must come from the SAME tracker. Mixing the recording
    # run's strict count with the screening run's raw count produced a report
    # claiming more divisions than fissions, which is impossible.
    repro = tracker.reproduction_events(min_child_life=6)
    raw = tracker.reproduction_events(min_child_life=6, min_mass_frac=0.0)
    lineage = tracker.lineage()

    lines = [
        f"# SPECIES {idx:03d} — {name}",
        "",
        f"**Verdict:** {'VIABLE + REPRODUCING' if rec['n_reproduction'] else 'VIABLE'}",
        f"**Origin:** {rec.get('origin', 'random')}  |  **Seed:** {rec['seed']}",
        "",
        "## Viability gates",
        "",
        "| gate | verdict | value | detail |",
        "| --- | --- | --- | --- |",
    ]
    for g in rec["gates"]:
        lines.append(f"| {g['name']} | {'PASS' if g['passed'] else 'FAIL'} | "
                     f"{g['value']:.6g} | {g['detail']} |")

    lines += ["", "## Behaviour (anomaly bouncer)", "",
              "| behaviour | established | score | evidence |",
              "| --- | --- | --- | --- |"]
    for a in anomalies:
        lines.append(f"| {a.kind} | {'YES' if a.established else 'no'} | "
                     f"{a.score:.3f} | {a.detail} |")

    surviving = sum(len(e["surviving_children"]) for e in repro)
    lines += [
        "", "## Reproduction", "",
        "Measured on the recording run below (the screening run is sampled "
        "more coarsely and its counts differ; both are stated separately "
        "rather than mixed).",
        "",
        f"- Divisions counted (offspring survived AND carried at least "
        f"{no.MIN_OFFSPRING_FRAC:.0%} of the parent's mass): **{len(repro)}**",
        f"- Raw fission events before the mass filter: **{len(raw)}** — the "
        f"difference is debris a large body shed, which is not reproduction",
        f"- Surviving offspring total: **{surviving}**",
        f"- Organisms tracked in this run: **{len(lineage)}**",
        f"- Screening run, for comparison: {rec['n_reproduction']} divisions "
        f"of {rec.get('n_fission_raw', 'n/a')} raw fissions, deepest "
        f"generation {rec['max_generation']}",
        "",
    ]
    if repro:
        lines += ["| frame | parent | children | parent mass | child masses | "
                  "child share |",
                  "| --- | --- | --- | --- | --- | --- |"]
        for e in repro[:12]:
            lines.append(
                f"| {e['frame']} | `{e['parent']}` | "
                f"{', '.join('`%s`' % c for c in e['surviving_children'])} | "
                f"{e['parent_mass']:.1f} | "
                f"{', '.join('%.1f' % m for m in e['child_mass'])} | "
                f"{', '.join('%.0f%%' % (f * 100) for f in e.get('child_mass_frac', []))} |")
        lines.append("")

    lines += ["## Complexity", "", "```json",
              json.dumps({k: rec[k] for k in (
                  "morph_diversity", "spatial_mi", "cross_channel_mi",
                  "euler_final", "concentration_final", "occupancy_final",
                  "n_blobs_final", "activity", "mass_drift", "score")},
                  indent=2, default=float), "```", ""]

    lines += ["## Lineage tree", "", "```json",
              json.dumps(dict(list(lineage.items())[:40]), indent=2,
                         default=float), "```", ""]

    lines += ["## Media", ""]
    for k in ("png", "gif", "mp4"):
        if media.get(k):
            lines.append(f"- `outputs/{media[k]}`")
    if media.get("mp4_note"):
        lines.append(f"- note: {media['mp4_note']}")
    lines += ["", f"- genome: `{genome_path.relative_to(ROOT)}`", ""]

    path.write_text("\n".join(lines))
    return path


SPECIES_NAMES = ["OSCILLIS", "MITOSA", "VAGRANT", "CORONA", "SPLITTER",
                 "DRIFTER", "NUCLEUS", "TENDRIL"]


def cmd_curate(args) -> int:
    cfg = nf.Config(advect_genome=False)
    SPECIES_DIR.mkdir(parents=True, exist_ok=True)

    records = []
    for f in sorted(SCREEN_DIR.glob("shard_*.jsonl")):
        for line in f.read_text().splitlines():
            if line.strip():
                records.append(json.loads(line))
    if not records:
        print("failed: no screening records found. Run `screen` first.")
        return 1

    viable = [r for r in records if r.get("viable")]
    repro = [r for r in viable if r.get("n_reproduction", 0) > 0]
    print(f"Screened {len(records)} candidates: {len(viable)} viable, "
          f"{len(repro)} reproducing.")

    flagged: dict[str, int] = {}
    for r in records:
        for k in r.get("flagged", []):
            flagged[k] = flagged.get(k, 0) + 1
    print("Anomaly bouncer over the whole screen: "
          + (", ".join(f"{k}={v}" for k, v in sorted(flagged.items()))
             if flagged else "nothing flagged"))

    winners = [{"record": r, "candidate": sample_candidate(r["seed"], cfg)}
               for r in sorted(repro, key=lambda r: -r["score"])[:args.target]]

    if len(winners) < args.target:
        need = args.target - len(winners)
        print(f"\n{need} more reproducer(s) needed. Hill-climbing from the "
              f"best viable non-reproducers.")
        pool = [r["seed"] for r in sorted(viable, key=lambda r: -r["score"])
                if r.get("n_reproduction", 0) == 0][:args.lineages]
        winners = hill_climb(cfg, pool, args.target, args.budget, winners)

    if not winners:
        print("\n" + "=" * 68)
        print("ZERO reproducing species found. This is a real result, not a "
              "crash.")
        print(f"  candidates screened : {len(records)}")
        print(f"  viable              : {len(viable)}")
        best = max(records, key=lambda r: r.get("score", -1))
        print(f"  best score          : {best.get('score', -1):.2f} "
              f"(seed {best.get('seed')})")
        print("=" * 68)
        return 1

    print(f"\nVerifying and recording {len(winners)} species.")
    summary = []
    for i, wdef in enumerate(winners[:args.target], start=1):
        name = SPECIES_NAMES[(i - 1) % len(SPECIES_NAMES)]
        tag = f"SPECIES_{i:03d}_{name}"
        cand: Candidate = wdef["candidate"]
        print(f"\n=== {tag} (seed {cand.seed}, alpha={cand.cfg.alpha}) ===",
              flush=True)

        photo = phototaxis_probe(cand)
        print(f"  phototaxis: {photo.established} ({photo.detail})", flush=True)

        out = record_species(cand, tag)
        tracker = out["tracker"]
        anomalies = [photo, no.detect_pursuit(tracker),
                     no.detect_cyclic_locomotion(tracker)]
        for a in anomalies[1:]:
            print(f"  {a.kind}: {a.established} ({a.detail})", flush=True)

        world = nf.World(cand.cfg, cand.spec, cand.params, seed=cand.seed)
        gpath = SPECIES_DIR / f"{tag}_genome.json"
        gpath.write_text(world.genome_json(name, {
            "seed": cand.seed, "origin": wdef["record"].get("origin"),
            "spawn_radius": cand.spawn_radius, "spawn_peak": cand.spawn_peak,
            "verified": {a.kind: a.established for a in anomalies},
        }))

        rpath = write_report(i, name, wdef["record"], anomalies, tracker,
                             out["media"], gpath)
        summary.append({
            "species": name, "report": str(rpath.relative_to(ROOT)),
            "genome": str(gpath.relative_to(ROOT)),
            "reproduction_events": wdef["record"]["n_reproduction"],
            "behaviours": {a.kind: {"established": a.established,
                                    "score": a.score} for a in anomalies},
            "media": out["media"],
        })
        print(f"  wrote {rpath.relative_to(ROOT)}", flush=True)

    # The bouncer auto-records what it flags, not only what wins on score:
    # a candidate that scored poorly but showed pursuit or a gait is exactly
    # the run worth keeping a clip of.
    chosen = {w["candidate"].seed for w in winners[:args.target]}
    extra = [r for r in records if r.get("flagged") and r["seed"] not in chosen]
    extra.sort(key=lambda r: -r.get("score", 0))
    anomaly_clips = []
    for r in extra[:args.record_flagged]:
        kinds = "_".join(k.split("_")[0].upper() for k in r["flagged"])
        tag = f"ANOMALY_{r['seed']}_{kinds}"
        print(f"\n=== auto-recording flagged run {tag} ===", flush=True)
        out = record_species(sample_candidate(r["seed"], cfg), tag)
        anomaly_clips.append({"seed": r["seed"], "flagged": r["flagged"],
                              "media": out["media"]})
        print(f"  wrote outputs/{out['media']['gif']}", flush=True)

    (HUNTS / "SPECIES_INDEX.json").write_text(json.dumps({
        "generated": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "screened": len(records), "viable": len(viable),
        "reproducing_found": len(summary), "species": summary,
        "flagged_by_bouncer": flagged,
        "anomaly_clips": anomaly_clips,
    }, indent=2, default=float))

    # A campaign that does not write up its results is not finished. This is
    # generated from the raw records, so it cannot drift from the data.
    try:
        import subprocess
        subprocess.run([sys.executable, str(ROOT / "scripts" / "report.py")],
                       check=True)
    except Exception as e:                     # report, never swallow
        print(f"WARNING: campaign report generation failed: {e!r}")

    print("\n" + "=" * 68)
    print(f"DISCOVERY COMPLETE: {len(summary)} reproducing species "
          f"from {len(records)} screened candidates")
    for s in summary:
        beh = [k for k, v in s["behaviours"].items() if v["established"]]
        print(f"  {s['species']:<10} repro={s['reproduction_events']}  "
              f"behaviours={beh or 'none established'}")
    print("=" * 68)
    return 0


def main() -> int:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("screen")
    s.add_argument("--n", type=int, default=12, help="candidates per shard")
    s.add_argument("--shard", type=int, default=0)
    s.add_argument("--nshards", type=int, default=1)
    s.add_argument("--base", type=int, default=0)
    s.set_defaults(func=cmd_screen)

    c = sub.add_parser("curate")
    c.add_argument("--target", type=int, default=3)
    c.add_argument("--lineages", type=int, default=6)
    c.add_argument("--budget", type=int, default=40, help="mutant evaluations")
    c.add_argument("--record-flagged", type=int, default=2,
                   help="also record this many flagged non-winning runs")
    c.set_defaults(func=cmd_curate)

    a = p.parse_args()
    return a.func(a)


if __name__ == "__main__":
    raise SystemExit(main())
