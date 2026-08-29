"""Interactive viewport for the non-reciprocal field simulator.

Run:  .venv/bin/streamlit run app/viewer.py

Live controls for the asymmetric cross-weights K_01 and K_10, plus the two
perturbation operators the oracle uses: a Gaussian noise blast and a digital
scalpel that slices mass out of the soliton so you can watch it heal.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt          # noqa: E402
import numpy as np                        # noqa: E402
import streamlit as st                    # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from engine.oracle import (               # noqa: E402
    center_of_mass, concentration, spatial_entropy,
)
from engine.physics import Genome, Simulator  # noqa: E402

st.set_page_config(page_title="fun-dots viewport", layout="wide")


# --------------------------------------------------------------------------
# State
# --------------------------------------------------------------------------


def build(genome: Genome) -> None:
    st.session_state.genome = genome
    st.session_state.sim = Simulator(genome)
    st.session_state.history = []


def load_genome(path: Path) -> Genome:
    data = json.loads(path.read_text())
    return Genome.from_dict(data)


if "sim" not in st.session_state:
    build(Genome())


sim: Simulator = st.session_state.sim
genome: Genome = st.session_state.genome


# --------------------------------------------------------------------------
# Sidebar
# --------------------------------------------------------------------------

with st.sidebar:
    st.header("Non-reciprocal coupling")
    st.caption("K_01 is how channel 0 responds to 1. K_10 is the reverse. "
               "Equal magnitudes with equal sign = reciprocal, and nothing "
               "self-propels. Break the symmetry to get chasers.")

    k01 = st.slider("K_01  (chaser gain)", -4.0, 4.0,
                    float(genome.K[0][1]), 0.05)
    k10 = st.slider("K_10  (fleer gain)", -4.0, 4.0,
                    float(genome.K[1][0]), 0.05)
    k00 = st.slider("K_00  (self 0)", -3.0, 3.0, float(genome.K[0][0]), 0.05)
    k11 = st.slider("K_11  (self 1)", -3.0, 3.0, float(genome.K[1][1]), 0.05)

    asym = abs(k01 - k10)
    st.metric("asymmetry |K_01 - K_10|", f"{asym:.2f}")

    sim.K = np.array([[k00, k01], [k10, k11]], dtype=np.float64)
    genome.K = [[k00, k01], [k10, k11]]

    st.divider()
    st.header("Kernels")
    r0 = st.slider("ring radius ch0", 3.0, 30.0, float(genome.kernel_radius[0]), 0.5)
    r1 = st.slider("ring radius ch1", 3.0, 30.0, float(genome.kernel_radius[1]), 0.5)
    s0 = st.slider("ring sigma ch0", 0.5, 8.0, float(genome.kernel_sigma[0]), 0.1)
    s1 = st.slider("ring sigma ch1", 0.5, 8.0, float(genome.kernel_sigma[1]), 0.1)
    if [r0, r1] != list(genome.kernel_radius) or [s0, s1] != list(genome.kernel_sigma):
        genome.kernel_radius = [r0, r1]
        genome.kernel_sigma = [s0, s1]
        from engine.physics import build_kernels
        sim.kern_ft, sim.rep_ft = build_kernels(genome)

    st.divider()
    st.header("Load a hunted species")
    hunts = sorted((ROOT / "hunts").glob("HUNT_*.md"))
    st.caption(f"{len(hunts)} hunt reports on disk")
    genome_files = sorted((ROOT / "outputs").glob("*_genome.json"))
    if genome_files:
        pick = st.selectbox("genome", [p.name for p in genome_files])
        if st.button("Load genome"):
            build(load_genome(ROOT / "outputs" / pick))
            st.rerun()
    else:
        st.caption("No genome JSON in outputs/ yet. Run scripts/run_hunt.py.")


# --------------------------------------------------------------------------
# Controls
# --------------------------------------------------------------------------

st.title("fun-dots — non-reciprocal active matter viewport")

c1, c2, c3, c4, c5, c6 = st.columns(6)
n_steps = c1.number_input("steps / advance", 1, 500, 25)
if c2.button("▶ Advance", use_container_width=True):
    sim.step(int(n_steps))
if c3.button("💥 Noise blast", use_container_width=True):
    sim.inject_noise(amplitude=0.5, key_seed=int(np.random.randint(1 << 30)))
    st.toast("Gaussian pulse injected. Mass baseline re-anchored.")
if c4.button("🔪 Scalpel", use_container_width=True):
    sim.scalpel(axis=0, position=0.5, width=5)
    st.toast("Sliced. Advance to watch it heal.")
if c5.button("↺ Reset", use_container_width=True):
    build(genome)
    st.rerun()
auto = c6.checkbox("auto-run")

st.session_state.history.append({
    "t": sim.t,
    "mass": sim.mass(),
    "drift": sim.mass_drift(),
    "conc": concentration(sim.rho),
    "entropy": spatial_entropy(sim.rho),
})
st.session_state.history = st.session_state.history[-400:]


# --------------------------------------------------------------------------
# Canvas
# --------------------------------------------------------------------------

rho = np.asarray(sim.rho)
left, right = st.columns([3, 1])

with left:
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.8))
    axes[0].imshow(rho[0], cmap="magma", interpolation="bilinear")
    axes[0].set_title("channel 0 — magma")
    axes[1].imshow(rho[1], cmap="viridis", interpolation="bilinear")
    axes[1].set_title("channel 1 — viridis")

    rgb = np.zeros(rho.shape[1:] + (3,))
    a = rho[0] / (rho[0].max() + 1e-12)
    b = rho[1] / (rho[1].max() + 1e-12)
    rgb[..., 0], rgb[..., 1], rgb[..., 2] = a, b, 0.35 * (a + b)
    axes[2].imshow(np.clip(rgb, 0, 1), interpolation="bilinear")
    axes[2].set_title("composite")
    for ax in axes:
        ax.axis("off")
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

with right:
    st.subheader("Invariants")
    drift = sim.mass_drift()
    st.metric("step", sim.t)
    st.metric("total mass", f"{sim.mass():.6f}")
    st.metric("mass drift", f"{drift:.2e}",
              delta="within 1e-4 gate" if drift <= 1e-4 else "GATE BREACH",
              delta_color="normal" if drift <= 1e-4 else "inverse")
    st.metric("concentration (peak/mean)", f"{concentration(sim.rho):.2f}")
    st.metric("spatial entropy", f"{spatial_entropy(sim.rho):.4f}")
    cx, cy = center_of_mass(sim.rho)
    st.metric("centre of mass", f"({cx:.1f}, {cy:.1f})")

hist = st.session_state.history
if len(hist) > 2:
    st.line_chart(
        {"concentration": [h["conc"] for h in hist],
         "entropy x10": [h["entropy"] * 10 for h in hist]},
        height=180,
    )

if auto:
    sim.step(int(n_steps))
    st.rerun()
