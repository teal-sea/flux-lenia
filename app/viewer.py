"""Neural Flow Lenia discovery viewport.

    streamlit run app/viewer.py

Click the canvas to act on the world. The tool selector decides what a click
does: drop a creature, irradiate its genome, cut it, or move the lamp. All
four act at the clicked cell, so the world is edited by pointing at it rather
than by typing coordinates.

Rendering goes through `engine.render`, the same code path the recorder uses,
so a saved clip is exactly what was on screen.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
import streamlit as st
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.tools import PRESET_MIX, TOOLS, apply_click   # noqa: E402
from engine import neural_field as nf          # noqa: E402
from engine import novelty_oracle as no        # noqa: E402
from engine import render as rd                # noqa: E402

st.set_page_config(page_title="fun-dots · Neural Flow Lenia", layout="wide")

SPECIES_DIR = ROOT / "outputs" / "species"
OUTPUTS = ROOT / "outputs"
SCALE = 3                       # canvas upscale factor
CLICK_STRIDE = 2                # cell spacing of the invisible click grid


# --------------------------------------------------------------------------
# World lifecycle
# --------------------------------------------------------------------------


def new_world(seed: int, genome_file: str | None = None) -> nf.World:
    if genome_file:
        data = json.loads((SPECIES_DIR / genome_file).read_text())
        data["config"]["advect_genome"] = True     # brush needs a live genome
        w = nf.World.from_json(data, seed=seed)
    else:
        cfg = nf.Config(advect_genome=True)
        w = nf.World.random(cfg, seed=seed)
    w.light_pos = None
    return w


def reset(seed: int, genome_file: str | None, spawn_preset: str = "AMOEBA"):
    w = new_world(seed, genome_file)
    w.spawn(w.cfg.size / 2, w.cfg.size / 2,
            nf.preset_genome(spawn_preset, w.cfg),
            radius=20.0, peak=1.2,
            channel_mix=PRESET_MIX.get(spawn_preset), seed=seed)
    st.session_state.world = w
    st.session_state.frames = []
    st.session_state.log = [f"world reset (seed {seed}, {spawn_preset} seeded)"]
    st.session_state.tracker = no.SpeciationTracker(size=w.cfg.size)
    st.session_state.tracker.update(np.asarray(w.A))
    st.session_state.last_click = None


if "world" not in st.session_state:
    reset(7, None)

world: nf.World = st.session_state.world
cfg = world.cfg


def log(msg: str) -> None:
    st.session_state.log.insert(0, f"[t={world.t}] {msg}")
    del st.session_state.log[24:]


# --------------------------------------------------------------------------
# Sidebar
# --------------------------------------------------------------------------

with st.sidebar:
    st.header("World")
    genomes = sorted(p.name for p in SPECIES_DIR.glob("*_genome.json")) \
        if SPECIES_DIR.exists() else []
    choice = st.selectbox("brain", ["random"] + genomes)
    seed = st.number_input("seed", 0, 10_000, 7)
    if st.button("Reset world", width='stretch'):
        reset(int(seed), None if choice == "random" else choice)
        st.rerun()

    st.divider()
    st.header("Physics")
    alpha = st.slider("concentration avoidance α", 0.0, 1.5, float(cfg.alpha), 0.01)
    gain_max = st.slider("flux gain ceiling", 0.2, 6.0, float(cfg.gain_max), 0.1)
    theta_max = st.slider("orientation drift ceiling (rad)", 0.0, float(np.pi),
                          float(cfg.theta_max), 0.05,
                          help="0 makes the flow a pure gradient descent and "
                               "the world relaxes; larger values make it "
                               "active and it can move forever.")
    e_scale = st.slider("growth amplitude", 0.1, 3.0, float(cfg.e_scale), 0.05)
    max_step = st.slider("max displacement / step", 0.1, 0.95,
                         float(cfg.max_step), 0.05)
    if (alpha, gain_max, theta_max, e_scale, max_step) != (
            cfg.alpha, cfg.gain_max, cfg.theta_max, cfg.e_scale, cfg.max_step):
        import dataclasses
        world.cfg = dataclasses.replace(
            cfg, alpha=alpha, gain_max=gain_max, theta_max=theta_max,
            e_scale=e_scale, max_step=max_step)
        cfg = world.cfg

    st.divider()
    st.header("Display")
    show_flow = st.checkbox("vector flow overlay", True)
    show_markers = st.checkbox("organism markers", True)
    exposure = st.slider("exposure", 0.4, 4.0, 1.6, 0.1)
    bloom = st.slider("bloom", 0.0, 1.2, 0.45, 0.05)

    st.divider()
    st.header("Auto-recorder")
    recording = st.checkbox("record frames", False)
    clip_len = st.number_input("auto-save every N frames", 20, 600, 120)
    st.caption(f"buffer: {len(st.session_state.frames)} frames · "
               f"{'ffmpeg found (MP4+GIF)' if rd.ffmpeg_available() else 'no ffmpeg (GIF only)'}")


# --------------------------------------------------------------------------
# Toolbar
# --------------------------------------------------------------------------

st.title("Neural Flow Lenia — discovery viewport")

c = st.columns([1.3, 1, 1, 1, 1, 1.2])
tool = c[0].radio("click tool", list(TOOLS),
                  horizontal=False, label_visibility="collapsed")
preset = c[1].selectbox("creature", list(PRESET_MIX), label_visibility="collapsed")
n_steps = c[2].number_input("steps/advance", 1, 200, 12,
                            label_visibility="collapsed")
advance = c[3].button("▶ Advance", width='stretch')
auto = c[4].checkbox("auto-run")
brush = c[5].slider("brush radius", 4.0, 40.0, 14.0, 1.0)

st.caption(f"**{tool}** tool armed — click the canvas. "
           + {"Spawn": f"Drops a {preset} genome seed where you click.",
              "Mutate": "Radioactive brush: perturbs the local genome of "
                        "whatever organism is under the cursor.",
              "Scalpel": "Excises mass (this intentionally breaks "
                         "conservation and rebaselines the counter).",
              "Light": "Moves the lamp; organisms sense it as an input "
                       "channel."}[tool])


# --------------------------------------------------------------------------
# Simulation advance
# --------------------------------------------------------------------------

if advance or auto:
    world.step(int(n_steps))
    st.session_state.tracker.update(np.asarray(world.A))

A = np.asarray(world.A)
blobs = no.extract_blobs(A)

img = rd.upscale(rd.composite(A, exposure=exposure, bloom=bloom), SCALE)
if show_flow:
    img = rd.draw_flow(img, np.asarray(world.dy), np.asarray(world.dx),
                       scale_up=SCALE, stride=6, gain=9.0)
if show_markers:
    img = rd.draw_markers(img, [b.centroid for b in blobs], scale_up=SCALE)
if world.light_pos is not None:
    img = rd.draw_markers(img, [world.light_pos], scale_up=SCALE, radius=16,
                          color=(1.0, 1.0, 0.6), alpha=0.5)

if recording:
    st.session_state.frames.append(img)


def save_clip(reason: str) -> None:
    frames = st.session_state.frames
    if not frames:
        log("recorder: nothing buffered, nothing written")
        return
    OUTPUTS.mkdir(exist_ok=True)
    tag = f"CLIP_{time.strftime('%Y%m%d_%H%M%S')}"
    gif = rd.save_gif(frames[::2], OUTPUTS / f"{tag}.gif", fps=18)
    mp4 = rd.save_mp4(frames, OUTPUTS / f"{tag}.mp4", fps=30)
    log(f"recorder ({reason}): {len(frames)} frames -> {gif.name}"
        + (f" + {mp4.name}" if mp4 else " (no ffmpeg, GIF only)"))
    st.session_state.frames = []


if recording and len(st.session_state.frames) >= int(clip_len):
    save_clip("auto")


# --------------------------------------------------------------------------
# Canvas with click capture
# --------------------------------------------------------------------------

left, right = st.columns([3, 1.15])

with left:
    n = cfg.size
    gy, gx = np.meshgrid(np.arange(0, n, CLICK_STRIDE),
                         np.arange(0, n, CLICK_STRIDE), indexing="ij")
    fig = go.Figure()
    fig.add_layout_image(dict(
        source=Image.fromarray(rd.to_uint8(img)), xref="x", yref="y",
        x=0, y=0, sizex=n, sizey=n, sizing="stretch", layer="below"))
    # Invisible pick targets: plotly reports the clicked marker's coordinates,
    # which is what turns the rendered field into a clickable canvas.
    fig.add_trace(go.Scattergl(
        x=gx.ravel(), y=gy.ravel(), mode="markers",
        marker=dict(size=9, color="rgba(255,255,255,0.02)"),
        hoverinfo="x+y", name="", showlegend=False))
    fig.update_xaxes(range=[0, n], visible=False, constrain="domain")
    fig.update_yaxes(range=[n, 0], visible=False, scaleanchor="x")
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=640,
                      dragmode="pan", plot_bgcolor="#05060a",
                      paper_bgcolor="#05060a")

    ev = st.plotly_chart(fig, width='stretch', key="canvas",
                         on_select="rerun", selection_mode="points")

    pts = (ev.get("selection", {}) or {}).get("points", []) if ev else []
    if pts:
        cx, cy = float(pts[0]["x"]), float(pts[0]["y"])
        stamp = (round(cx, 2), round(cy, 2), tool, world.t)
        if st.session_state.get("last_click") != stamp:
            st.session_state.last_click = stamp
            log(apply_click(world, tool, cy, cx, preset, brush))
            st.rerun()

# --------------------------------------------------------------------------
# Instrument panel
# --------------------------------------------------------------------------

with right:
    st.subheader("Invariants")
    drift = world.mass_drift()
    m1, m2 = st.columns(2)
    m1.metric("step", world.t)
    m2.metric("mass", f"{world.mass():.1f}")
    st.metric("mass drift", f"{drift:.2e}",
              delta="within 1e-4" if drift <= 1e-4 else "GATE BREACH",
              delta_color="normal" if drift <= 1e-4 else "inverse")

    fc = no.frame_complexity(A)
    st.subheader("Emergence")
    g1, g2 = st.columns(2)
    g1.metric("organisms", fc["n_blobs"])
    g2.metric("Euler χ", fc["euler"])
    g1.metric("spatial MI", f"{fc['spatial_mi']:.2f}")
    g2.metric("cross-ch MI", f"{fc['cross_channel_mi']:.2f}")
    g1.metric("morph diversity", f"{fc['morph_diversity']:.2f}")
    g2.metric("peak/mean", f"{fc['concentration']:.1f}")

    tr: no.SpeciationTracker = st.session_state.tracker
    reps = tr.reproduction_events(min_child_life=3)
    st.metric("fission events (surviving)", len(reps))
    if tr.organisms:
        gens = max(o.generation for o in tr.organisms.values())
        st.caption(f"{len(tr.organisms)} organisms tracked · deepest "
                   f"generation {gens}")

    st.subheader("Genome field")
    Gf = np.asarray(world.Gf)
    tot = A.sum(axis=0)
    live = tot > 0.08 * max(tot.max(), 1e-9)
    if live.any():
        gm = Gf[:, live]
        st.caption(f"live-cell genome spread (std across cells): "
                   f"{float(gm.std(axis=1).mean()):.3f} — rises when the "
                   f"brush or hybridization creates variation")
    else:
        st.caption("no live cells")

    if st.button("Save clip now", width='stretch'):
        save_clip("manual")
        st.rerun()

    st.subheader("Log")
    st.code("\n".join(st.session_state.log[:12]) or "—", language="text")

if auto:
    st.rerun()
