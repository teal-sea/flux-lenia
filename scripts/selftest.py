#!/usr/bin/env python3
"""Verification for the Neural Flow Lenia core. Run before trusting a hunt.

Each check either prints PASS with the measured number, or fails loudly.
Nothing here is a smoke test that passes by not crashing.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import jax                                     # noqa: E402
import jax.numpy as jnp                        # noqa: E402

from engine import neural_field as nf          # noqa: E402
from engine import novelty_oracle as no        # noqa: E402

FAILS: list[str] = []


def check(name: str, ok: bool, detail: str) -> None:
    print(f"  [{'PASS' if ok else 'FAIL'}] {name:<34} {detail}")
    if not ok:
        FAILS.append(name)


# --------------------------------------------------------------------------


def test_euler():
    """chi must be 1 for a disk, 0 for an annulus, 2 for two disks."""
    n = 64
    yy, xx = np.meshgrid(np.arange(n), np.arange(n), indexing="ij")

    def disk(cy, cx, r):
        return ((yy - cy) ** 2 + (xx - cx) ** 2) < r ** 2

    d = disk(32, 32, 12)
    ann = disk(32, 32, 14) & ~disk(32, 32, 6)
    two = disk(16, 16, 8) | disk(48, 48, 8)
    vals = (no.euler_characteristic(d), no.euler_characteristic(ann),
            no.euler_characteristic(two))
    check("euler_characteristic", vals == (1, 0, 2),
          f"disk={vals[0]} (want 1), annulus={vals[1]} (want 0), "
          f"two disks={vals[2]} (want 2)")


def test_kernel_always_has_support():
    """No sampled kernel may come out empty.

    At small radii the shells are narrower than the grid can resolve and the
    naive profile is identically zero, which killed 2 of 120 candidates in
    the first campaign. Every radius in the configured range must yield a
    usable kernel for every shell pattern.
    """
    cfg = nf.Config()
    bad = []
    for radius in np.linspace(cfg.r_min, cfg.r_max, 24):
        for betas in ([1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0],
                      [1.0, 0.5, 0.2]):
            k = nf.build_kernel(cfg.size, float(radius), np.array(betas))
            if not (np.isfinite(k).all() and abs(k.sum() - 1.0) < 1e-9
                    and (k > 0).any()):
                bad.append((round(float(radius), 2), betas))
    check("every kernel in range has support", not bad,
          f"96 (radius, shell) combinations across {cfg.r_min}-{cfg.r_max} "
          f"cells, all normalized and non-empty"
          if not bad else f"empty or malformed: {bad[:4]}")


def test_partition_of_unity():
    """The weights of ONE source cell must sum to exactly 1 over the stencil.

    Note this is a per-source property: with a varying displacement field,
    neighbouring cells legitimately push mass into the same target, so the
    transported field is not pointwise unchanged. What must hold is that
    every source hands on all of its mass and no more.
    """
    cfg = nf.Config(size=32, channels=1, advect_genome=False)
    rng = np.random.default_rng(0)
    zero = jnp.zeros((1, 32, 32))

    worst_single = 0.0
    for _ in range(64):
        d = rng.uniform(-cfg.max_step, cfg.max_step, size=2)
        A = np.zeros((1, 32, 32))
        A[0, 16, 16] = 1.0                       # a single grain of mass
        dy = jnp.full((1, 32, 32), d[0])
        dx = jnp.full((1, 32, 32), d[1])
        out, _ = nf.reintegrate(jnp.asarray(A), zero, dy, dx, cfg)
        worst_single = max(worst_single, abs(float(jnp.sum(out)) - 1.0))
    check("single-source weights sum to 1", worst_single < 1e-15,
          f"max |sum(w) - 1| = {worst_single:.3e} over 64 random "
          f"displacements at |d| <= {cfg.max_step}")

    # And globally, with a fully random displacement field on random mass.
    A = jnp.asarray(rng.uniform(0, 3, size=(1, 32, 32)))
    dy = jnp.asarray(rng.uniform(-cfg.max_step, cfg.max_step, size=(1, 32, 32)))
    dx = jnp.asarray(rng.uniform(-cfg.max_step, cfg.max_step, size=(1, 32, 32)))
    out, _ = nf.reintegrate(A, zero, dy, dx, cfg)
    rel = abs(float(jnp.sum(out) - jnp.sum(A))) / float(jnp.sum(A))
    check("transport conserves total mass", rel < 1e-14,
          f"relative change {rel:.3e} under a random displacement field")


def test_mass_conservation():
    """Long run, real dynamics, drift must stay at rounding level."""
    cfg = nf.Config(advect_genome=True)
    w = nf.World.random(cfg, seed=5)
    w.spawn(64, 64, nf.preset_genome("AMOEBA", cfg), radius=16, seed=1)
    m0 = w.mass()
    trace = w.run(600)
    drift = abs(float(trace[-1]) - m0) / m0
    worst = float(np.max(np.abs(np.asarray(trace) - m0)) / m0)
    neg = float(jnp.min(w.A))
    check("mass conservation (600 steps)", worst < 1e-12,
          f"final drift {drift:.2e}, worst {worst:.2e} (gate is 1e-4)")
    check("density stays non-negative", neg >= 0.0, f"min rho = {neg:.3e}")


def test_no_blurring():
    """The old engine's failure mode: structure smeared into mush.

    Reintegration tracking should hold a sharp interface. We measure the
    field's total-variation-per-unit-mass, which collapses under diffusion.
    """
    cfg = nf.Config(advect_genome=False)
    w = nf.World.random(cfg, seed=5)
    w.spawn(64, 64, nf.preset_genome("AMOEBA", cfg), radius=16, seed=1)

    def sharpness(A):
        a = np.asarray(A).sum(0)
        gy = np.abs(np.diff(a, axis=0)).sum()
        gx = np.abs(np.diff(a, axis=1)).sum()
        return float((gy + gx) / a.sum())

    s0 = sharpness(w.A)
    w.run(600)
    s1 = sharpness(w.A)
    check("interfaces stay sharp", s1 > 0.5 * s0,
          f"edge density {s0:.4f} -> {s1:.4f} after 600 steps "
          f"(diffusion would drive this toward 0)")


def test_differentiable():
    """The sensory-motor map must be differentiable end to end: an MLP we
    cannot take gradients through is not a differentiable MLP."""
    cfg = nf.Config(size=32, advect_genome=False)
    w = nf.World.random(cfg, seed=2)
    w.spawn(16, 16, nf.preset_genome("PLANT", cfg), radius=6, seed=1)

    def loss(p):
        a, g, _ = nf.rollout(w.A, w.Gf, w.light, p, w.bank, cfg, 5)
        return jnp.sum(a * jnp.arange(cfg.size)[None, :, None])

    grads = jax.grad(loss)(w.params)
    flat = np.concatenate([np.asarray(g).ravel() for g in grads.values()])
    finite = bool(np.all(np.isfinite(flat)))
    nz = float(np.max(np.abs(flat)))
    check("gradients flow through rollout", finite and nz > 0,
          f"{flat.size} params, max |grad| = {nz:.3e}, all finite={finite}")


def test_periodic_labelling():
    """A body straddling the wrap seam is ONE organism, not two."""
    n = 48
    A = np.zeros((1, n, n))
    yy, xx = np.meshgrid(np.arange(n), np.arange(n), indexing="ij")
    dy = np.minimum(np.abs(yy - 0), n - np.abs(yy - 0))
    dx = np.minimum(np.abs(xx - 0), n - np.abs(xx - 0))
    A[0] = np.exp(-(dy ** 2 + dx ** 2) / (2 * 5.0 ** 2))
    blobs = no.extract_blobs(A)
    check("periodic connected components", len(blobs) == 1,
          f"blob spanning the seam segmented into {len(blobs)} body(ies), "
          f"want 1")


def test_fission_detection():
    """A synthetic split must be logged as fission with surviving children,
    and a one-frame flicker must NOT be."""
    n = 64
    tr = no.SpeciationTracker(size=n)

    def frame(centres, r=3.5):
        A = np.zeros((1, n, n))
        yy, xx = np.meshgrid(np.arange(n), np.arange(n), indexing="ij")
        for cy, cx in centres:
            dy = ((yy - cy + n / 2) % n) - n / 2
            dx = ((xx - cx + n / 2) % n) - n / 2
            A[0] += np.exp(-(dy ** 2 + dx ** 2) / (2 * r ** 2))
        return A

    for _ in range(5):
        tr.update(frame([(32, 32)]))
    # Drift apart slowly enough that consecutive masks still overlap (so the
    # link to the parent survives), then hold so the children can live.
    for k in np.arange(1.5, 13.0, 1.5):
        tr.update(frame([(32, 32 - k), (32, 32 + k)]))
    for _ in range(15):
        tr.update(frame([(32, 20), (32, 44)]))

    reps = tr.reproduction_events(min_child_life=8)
    check("fission detected with lineage", len(reps) == 1,
          f"{len(reps)} reproduction event(s); "
          f"{len(tr.organisms)} organisms tracked")
    if reps:
        child = reps[0]["surviving_children"][0]
        o = tr.organisms[child]
        check("child inherits lineage", o.parent is not None and o.generation == 1,
              f"child {child}: parent={o.parent}, generation={o.generation}, "
              f"lifespan={o.lifespan}")

    tr2 = no.SpeciationTracker(size=n)
    for _ in range(4):
        tr2.update(frame([(32, 32)]))
    tr2.update(frame([(32, 26), (32, 38)]))     # one-frame flicker
    for _ in range(6):
        tr2.update(frame([(32, 32)]))
    check("flicker is not reproduction",
          len(tr2.reproduction_events(min_child_life=8)) == 0,
          f"{len(tr2.reproduction_events(min_child_life=8))} events from a "
          f"single-frame split (want 0)")
    # The body that merged away must be recorded dead, not left as an
    # immortal survivor.
    alive2 = [o for o in tr2.organisms.values() if o.death_frame is None]
    check("merged body is marked dead", len(alive2) == 1,
          f"{len(alive2)} organism(s) still alive after the two bodies "
          f"re-merged (want 1)")

    # A speck shed by a large body is not an offspring: it must register as
    # a raw fission and then be filtered out by the offspring-mass floor.
    def blob(cy, cx, r, amp):
        yy, xx = np.meshgrid(np.arange(n), np.arange(n), indexing="ij")
        dy = ((yy - cy + n / 2) % n) - n / 2
        dx = ((xx - cx + n / 2) % n) - n / 2
        return amp * np.exp(-(dy ** 2 + dx ** 2) / (2 * r ** 2))

    def shed(dist):
        return (blob(32, 32, 6.0, 1.0) + blob(32, 32 + dist, 2.5, 0.2))[None]

    tr3 = no.SpeciationTracker(size=n)
    for _ in range(4):
        tr3.update(shed(8))
    for k in range(1, 10):                     # drifts out and detaches
        tr3.update(shed(8 + 2.0 * k))
    for _ in range(10):                        # and then survives out there
        tr3.update(shed(26))
    strict = tr3.reproduction_events(min_child_life=6)
    raw = tr3.reproduction_events(min_child_life=6, min_mass_frac=0.0)
    check("shed speck is not counted as reproduction",
          len(strict) == 0 and len(raw) >= 1,
          f"{len(raw)} raw fission event(s), {len(strict)} after the "
          f"{no.MIN_OFFSPRING_FRAC:.0%} offspring-mass filter (want 0)")


def test_mi_ordering():
    """Spatial MI must rank structure above noise."""
    rng = np.random.default_rng(0)
    n = 96
    noise = rng.uniform(size=(n, n))
    yy, xx = np.meshgrid(np.arange(n), np.arange(n), indexing="ij")
    smooth = np.exp(-(((yy - 48) ** 2 + (xx - 48) ** 2) / (2 * 14.0 ** 2)))
    mi_n = no.spatial_mutual_information(noise)
    mi_s = no.spatial_mutual_information(smooth)
    check("spatial MI ranks structure > noise", mi_s > mi_n + 0.5,
          f"noise {mi_n:.3f} nats vs blob {mi_s:.3f} nats")


def test_mutation_brush_reports_zero():
    """A brush stroke on empty space must report 0 cells, not pretend."""
    cfg = nf.Config(size=64)
    w = nf.World.random(cfg, seed=1)
    w.spawn(16, 16, nf.preset_genome("PLANT", cfg), radius=6, seed=1)
    empty = w.mutation_brush(50, 50, radius=6, strength=0.5, seed=0)
    onto = w.mutation_brush(16, 16, radius=8, strength=0.5, seed=0)
    check("mutation brush reports its hits", empty == 0 and onto > 0,
          f"{empty} cells on vacuum, {onto} cells on the organism")


def test_click_tools():
    """Every canvas tool must actually change the world it claims to change."""
    from app.tools import apply_click

    cfg = nf.Config(size=64, advect_genome=True)
    w = nf.World.random(cfg, seed=4)
    w.light_pos = None

    before = w.mass()
    msg = apply_click(w, "Spawn", 32, 32, preset="PREDATOR", brush=10)
    spawned = w.mass() > before
    dominant = int(np.argmax(np.asarray(w.A).sum(axis=(1, 2))))
    check("Spawn tool adds a creature", spawned and dominant == 0,
          f"mass {before:.1f} -> {w.mass():.1f}, dominant channel "
          f"{dominant} (PREDATOR mix is channel 0) | {msg}")

    g0 = np.asarray(w.Gf).copy()
    msg = apply_click(w, "Mutate", 32, 32, brush=12)
    changed = float(np.abs(np.asarray(w.Gf) - g0).max())
    check("Mutate tool edits the local genome", changed > 0,
          f"max genome delta {changed:.3f} | {msg}")

    m0 = w.mass()
    msg = apply_click(w, "Scalpel", 32, 32, brush=8)
    check("Scalpel removes mass and rebaselines",
          w.mass() < m0 and abs(w.mass_drift()) < 1e-12,
          f"mass {m0:.1f} -> {w.mass():.1f}, drift after rebaseline "
          f"{w.mass_drift():.1e} | {msg}")

    msg = apply_click(w, "Light", 10, 50)
    check("Light tool moves the lamp", float(np.asarray(w.light).max()) > 0.9,
          f"peak illumination {float(np.asarray(w.light).max()):.2f} | {msg}")


def test_genome_rides_with_mass():
    """The localized genome must travel with the mass, not stay put.

    This is what makes the brush and the spawner meaningful: if the genome
    field were static, a creature would swim out of its own mutation.

    Tested against the transport operator directly under a known constant
    displacement, so there is an exact expected answer. Driving it with
    emergent motion instead would make the test hostage to whether the
    particular species happens to travel — the discovered species keep a
    nearly stationary main body, which would let the check pass without
    demonstrating anything.
    """
    n = 64
    cfg = nf.Config(size=n, channels=1, genome_dim=2, advect_genome=True)
    yy, xx = np.meshgrid(np.arange(n), np.arange(n), indexing="ij")

    A = np.exp(-((yy - 32.0) ** 2 + (xx - 24.0) ** 2) / (2 * 5.0 ** 2))[None]
    Gf = np.zeros((2, n, n))
    Gf[0] = (((yy - 32.0) ** 2 + (xx - 24.0) ** 2) < 8.0 ** 2).astype(float)

    A, Gf = jnp.asarray(A), jnp.asarray(Gf)
    steps, vx = 20, 0.5
    dy = jnp.zeros((1, n, n))
    dx = jnp.full((1, n, n), vx)
    for _ in range(steps):
        A, Gf = nf.reintegrate(A, Gf, dy, dx, cfg)

    a = np.asarray(A)[0]
    g = np.asarray(Gf)[0]
    mass_x = float((a.sum(0) * np.arange(n)).sum() / a.sum())
    gw = g * a                                   # genome carried by the mass
    gen_x = float((gw.sum(0) * np.arange(n)).sum() / gw.sum())
    expected = 24.0 + steps * vx

    ok = (abs(mass_x - expected) < 0.3 and abs(gen_x - expected) < 0.5
          and float(g.max()) > 0.9)
    check("genome field rides with the mass",
          ok,
          f"after {steps} steps at {vx} cells/step the mass centre is at "
          f"x={mass_x:.2f} and the carried genome at x={gen_x:.2f} "
          f"(both expected {expected:.1f}); genome peak held at "
          f"{float(g.max()):.3f} (a static field would leave the genome at "
          f"x=24)")


def test_recording_roundtrip():
    """The recorder must write files that actually decode."""
    from PIL import Image
    from engine import render as rd

    out = ROOT / "outputs" / "_selftest"
    out.mkdir(parents=True, exist_ok=True)
    cfg = nf.Config(size=48, advect_genome=False)
    w = nf.World.random(cfg, seed=3)
    w.light_pos = None
    w.spawn(24, 24, np.zeros(cfg.genome_dim), radius=8, seed=1)

    frames = []
    for _ in range(12):
        w.run(4)
        frames.append(rd.upscale(rd.composite(np.asarray(w.A)), 4))

    gif = rd.save_gif(frames, out / "t.gif", fps=12)
    with Image.open(gif) as im:
        n_gif = getattr(im, "n_frames", 1)
    mp4 = rd.save_mp4(frames, out / "t.mp4", fps=12)
    mp4_ok = mp4 is not None and mp4.stat().st_size > 1000
    check("GIF written and decodable", gif.exists() and n_gif == len(frames),
          f"{gif.name}: {n_gif} frames, {gif.stat().st_size // 1024} KB")
    check("MP4 written via ffmpeg", mp4_ok,
          f"{mp4.name}: {mp4.stat().st_size // 1024} KB" if mp4
          else "ffmpeg unavailable — recorder falls back to GIF")


def test_saved_genome_reproduces():
    """A saved species must reload into the exact world that was tested.

    Skipped with a note if no species has been curated yet — reported as a
    skip, not as a pass.
    """
    import json
    from scripts.discover import sample_candidate

    files = sorted((ROOT / "outputs" / "species").glob("*_genome.json"))
    if not files:
        print("  [SKIP] saved genome reproduces          no curated species "
              "on disk yet (run scripts/discover.py curate)")
        return

    data = json.loads(files[-1].read_text())
    seed = int(data["seed"])
    radius = float(data.get("spawn_radius", 20.0))
    peak = float(data.get("spawn_peak", 1.2))

    def run_from_json():
        w = nf.World.from_json(data, seed=seed)
        w.light_pos = None
        w.spawn(w.cfg.size / 2, w.cfg.size / 2, np.zeros(w.cfg.genome_dim),
                radius=radius, peak=peak, seed=seed)
        w.run(240)
        return float(jnp.sum(w.A)), float(jnp.max(w.A))

    a, b = run_from_json(), run_from_json()
    check("saved genome reproduces its world bitwise", a == b,
          f"{files[-1].name}: two independent loads agree exactly after 240 "
          f"steps (mass {a[0]:.9f}, peak {a[1]:.9f})")

    # A species that came straight from the screen must also be
    # reconstructible from its seed alone. A hill-climbed mutant cannot be,
    # by definition, so that case is reported rather than failed.
    origin = data.get("origin") or "random"
    if origin == "random":
        fresh = sample_candidate(seed)
        same = (fresh.cfg == nf.World.from_json(data, seed=seed).cfg and all(
            np.allclose(np.asarray(data["params"][k]), np.asarray(v))
            for k, v in fresh.params.items()))
        check("screened species rebuilds from its seed", same,
              f"sample_candidate({seed}) reproduces the saved brain and config")
    else:
        print(f"  [INFO] species origin is '{origin}' — a mutant, so it is "
              f"reproducible from its stored genome, not from a seed")


def test_viewer_renders():
    """Run the actual Streamlit script headlessly and require no exception."""
    try:
        from streamlit.testing.v1 import AppTest
    except Exception as e:                      # pragma: no cover
        check("viewer renders headlessly", False, f"AppTest unavailable: {e}")
        return

    at = AppTest.from_file(str(ROOT / "app" / "viewer.py"), default_timeout=180)
    at.run()
    ok = not at.exception
    detail = "clean first render"
    if not ok:
        detail = str(at.exception)[:220]
    check("viewer renders headlessly", ok, detail)
    if not ok:
        return

    advance = [b for b in at.button if "Advance" in (b.label or "")]
    if advance:
        advance[0].click().run()
        check("viewer advances the simulation", not at.exception,
              "clicked Advance, no exception"
              if not at.exception else str(at.exception)[:220])
    toggles = [c for c in at.checkbox if "record" in (c.label or "").lower()]
    if toggles:
        toggles[0].set_value(True).run()
        check("viewer arms the recorder", not at.exception,
              "recorder toggled, no exception"
              if not at.exception else str(at.exception)[:220])


def main() -> int:
    print("Neural Flow Lenia selftest\n")
    for t in (test_euler, test_kernel_always_has_support,
              test_partition_of_unity, test_mass_conservation,
              test_no_blurring, test_differentiable, test_periodic_labelling,
              test_fission_detection, test_mi_ordering,
              test_mutation_brush_reports_zero, test_click_tools,
              test_genome_rides_with_mass, test_recording_roundtrip,
              test_saved_genome_reproduces, test_viewer_renders):
        t()
    print()
    if FAILS:
        print(f"FAILED: {len(FAILS)} check(s): {', '.join(FAILS)}")
        return 1
    print("All checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
