"""Neural Flow Lenia: mass-conserving neural sensory-motor field dynamics.

What this is
------------
A continuous multi-channel field where *nothing is created or destroyed*.
Every cell of mass is transported; growth never adds material, it only
reshapes the potential that the mass flows along. Concretely:

    U_k   = A[src_k] (*) ring_k             multi-scale concentric perception
    B_k   = bell(U_k; m_k, s_k)             Lenia-style growth features
    h     = tanh(FiLM_G(W1 [U,B,A,light]))  per-cell MLP, conditioned on the
    E,g,t = W2 h                            LOCAL genome vector at that cell
    v_c   = g_c * R(t_c) grad(E_c) - alpha * grad(A_total)
    A     <- reintegrate(A, dt * v)         mass-conserving transport

Three things distinguish this from the passive linear engine it replaces
(`engine/physics.py`):

1. **No blurring.** Transport is reintegration tracking (Flow Lenia's
   scheme): each cell's mass is displaced to a sub-cell position and split
   bilinearly among its neighbours. The bilinear weights are a partition of
   unity, so mass is conserved to float rounding, and unlike donor-cell
   upwinding it adds almost no numerical diffusion. Structures stay sharp
   for thousands of steps instead of smearing into mush.

2. **A neural sensory-motor map.** The mapping from local neighbourhood
   composition to (growth, flux gain, orientation drift) is a differentiable
   MLP, not a fixed bell curve. Classic Lenia is the special case where the
   MLP is one linear layer over the bell features, so this architecture
   strictly contains it.

3. **Orientation drift makes it active.** R(t_c) rotates the flow away from
   the potential gradient. A pure gradient flow relaxes; a rotated one does
   not, so the field can sustain locomotion and circulation forever without
   any energy bookkeeping. This is the source of self-propulsion.

Localized genomes
-----------------
The genome is not a global constant. A genome field Gf(x) rides along with
the mass (advected as a mass-weighted mixture), so different regions of the
same world run different species, they interact, and mixtures blend where
they touch. That is what makes the creature spawner and the mutation brush
meaningful rather than cosmetic: dropping a creature drops its genome into
the substrate, and painting mutation edits the genome of whatever organism
is under the brush.

The perception bank (ring kernels) and the MLP weights are shared across the
world; the per-cell genome vector conditions that shared brain through FiLM
modulation. So "species" means a point in genome space, and speciation is a
measurable clustering of the genome field, not a label we assign by hand.
"""

from __future__ import annotations

import json
import math
import zlib
from dataclasses import dataclass, asdict, field
from functools import partial

import jax
import jax.numpy as jnp
import numpy as np

jax.config.update("jax_enable_x64", True)

EPS = 1e-12


# ==========================================================================
# Configuration
# ==========================================================================


@dataclass(frozen=True)
class Config:
    """Static world configuration. Frozen so it can be a jit static arg."""

    size: int = 128
    channels: int = 3
    genome_dim: int = 8
    n_kernels: int = 16
    hidden: int = 24

    dt: float = 1.0
    alpha: float = 0.35           # concentration avoidance strength
    max_step: float = 0.85        # hard bound on displacement, in cells
    e_scale: float = 1.0          # growth potential amplitude
    gain_max: float = 2.5         # flux gain ceiling
    theta_max: float = math.pi    # orientation drift ceiling (radians)

    r_min: float = 3.0            # multi-scale perception range, in cells
    r_max: float = 45.0

    # Transporting the genome field costs as much as transporting the mass.
    # For a spatially uniform genome the mass-weighted blend returns that
    # same uniform value, so skipping it is exact, not an approximation.
    # Single-species searches run with this off; multi-species worlds and the
    # viewer's spawner and mutation brush need it on.
    advect_genome: bool = True

    @property
    def window(self) -> int:
        """Transport stencil radius. Bilinear splitting of a displacement
        bounded by max_step < 1 never reaches beyond one cell, so a 3x3
        window carries the full partition of unity."""
        return int(math.ceil(self.max_step))

    @property
    def n_features(self) -> int:
        return 2 * self.n_kernels + self.channels + 1


# ==========================================================================
# Perception bank: multi-scale concentric ring kernels
# ==========================================================================


@dataclass
class KernelSpec:
    """Shape of the perception bank. Small enough to serialize verbatim."""

    radius: list[float]
    betas: list[list[float]]     # concentric shell weights, inner -> outer
    src: list[int]               # which channel each kernel reads

    @staticmethod
    def sample(rng: np.random.Generator, cfg: Config) -> "KernelSpec":
        k = cfg.n_kernels
        # Log-spaced radii so the bank covers 3px detail and 45px context
        # with equal resolution per octave, then jittered.
        base = np.geomspace(cfg.r_min, cfg.r_max, k)
        radius = base * rng.uniform(0.85, 1.15, size=k)
        radius = np.clip(radius, cfg.r_min, cfg.r_max)

        n_shell = 3
        betas = rng.uniform(0.0, 1.0, size=(k, n_shell))
        # Guarantee every kernel has a dominant shell (avoids all-zero rings).
        betas[np.arange(k), rng.integers(0, n_shell, size=k)] = 1.0
        betas[betas < 0.15] = 0.0

        src = rng.integers(0, cfg.channels, size=k)
        return KernelSpec(radius.tolist(), betas.tolist(), src.tolist())


def _radial_grid(size: int) -> np.ndarray:
    """Distance from the origin cell with periodic wrap, FFT-aligned."""
    idx = np.arange(size)
    d = np.minimum(idx, size - idx)
    return np.sqrt(d[:, None] ** 2 + d[None, :] ** 2)


def _bump(x: np.ndarray) -> np.ndarray:
    """Lenia's smooth compact bump on (0, 1), zero outside."""
    inside = (x > 0.0) & (x < 1.0)
    safe = np.where(inside, x, 0.5)
    return np.where(inside, np.exp(4.0 - 1.0 / (safe * (1.0 - safe))), 0.0)


def build_kernel(size: int, radius: float, betas: np.ndarray) -> np.ndarray:
    """One multi-shell concentric ring kernel, normalized to unit sum."""
    r = _radial_grid(size) / max(radius, 1e-6)
    n = len(betas)
    idx = np.minimum((r * n).astype(int), n - 1)
    k = np.asarray(betas)[idx] * _bump(r * n - idx)
    k = np.where(r < 1.0, k, 0.0)
    total = k.sum()
    if total <= 0:                      # degenerate spec: refuse silently? no.
        raise ValueError(f"empty kernel (radius={radius}, betas={betas})")
    return k / total


def build_bank(spec: KernelSpec, cfg: Config) -> tuple[jnp.ndarray, jnp.ndarray]:
    """Precompute kernel FFTs and the source-channel index vector."""
    ks = np.stack([
        build_kernel(cfg.size, r, np.asarray(b))
        for r, b in zip(spec.radius, spec.betas)
    ])
    return jnp.fft.rfft2(jnp.asarray(ks)), jnp.asarray(spec.src, dtype=jnp.int32)


# ==========================================================================
# Brain parameters
# ==========================================================================


def sample_params(rng: np.random.Generator, cfg: Config) -> dict:
    """Random sensory-motor brain. Scaled so the field is neither dead nor
    saturated at initialization."""
    f, hd, c, gd = cfg.n_features, cfg.hidden, cfg.channels, cfg.genome_dim
    return {
        # Bell features: centres spread across the density range a ring
        # kernel actually reports, widths narrow enough to be selective.
        "bell_m": rng.uniform(0.02, 0.60, size=cfg.n_kernels),
        "bell_s": rng.uniform(0.02, 0.20, size=cfg.n_kernels),
        "W1": rng.normal(0, 1.0 / math.sqrt(f), size=(f, hd)),
        "b1": rng.normal(0, 0.10, size=hd),
        "Wg1": rng.normal(0, 0.60 / math.sqrt(gd), size=(gd, hd)),
        "Wg2": rng.normal(0, 0.60 / math.sqrt(gd), size=(gd, hd)),
        "W2": rng.normal(0, 1.0 / math.sqrt(hd), size=(hd, 3 * c)),
        "b2": rng.normal(0, 0.10, size=3 * c),
    }


def params_to_jax(p: dict) -> dict:
    return {k: jnp.asarray(v, dtype=jnp.float64) for k, v in p.items()}


def params_to_json(p: dict) -> dict:
    return {k: np.asarray(v).tolist() for k, v in p.items()}


def params_from_json(d: dict) -> dict:
    return {k: jnp.asarray(np.asarray(v, dtype=np.float64)) for k, v in d.items()}


def mutate_params(p: dict, rng: np.random.Generator, sigma: float = 0.08) -> dict:
    """Gaussian drift on the shared brain. Bell widths stay positive."""
    out = {}
    for k, v in p.items():
        a = np.asarray(v, dtype=np.float64)
        out[k] = a + rng.normal(0, sigma * (np.std(a) + 1e-3), size=a.shape)
    out["bell_s"] = np.clip(out["bell_s"], 0.01, 0.5)
    out["bell_m"] = np.clip(out["bell_m"], 0.0, 1.2)
    return out


# ==========================================================================
# Genome vectors and presets
# ==========================================================================

PRESET_NAMES = ("PREDATOR", "SWARMER", "PLANT", "AMOEBA")


def preset_genome(name: str, cfg: Config, scale: float = 1.0) -> np.ndarray:
    """A deterministic point in genome space per preset name.

    These are seeds, not verified phenotypes. What a preset actually does is
    whatever the oracle measures it doing; the name is a handle, and
    `engine.novelty_oracle` is what earns or refuses the label.
    """
    seed = zlib.crc32(name.encode()) & 0xFFFFFFFF
    rng = np.random.default_rng(seed)
    return rng.normal(0.0, scale, size=cfg.genome_dim)


# ==========================================================================
# Dynamics
# ==========================================================================


def perceive(A: jnp.ndarray, khat: jnp.ndarray, ksrc: jnp.ndarray) -> jnp.ndarray:
    """Non-local perception: U_k = A[src_k] convolved with ring kernel k."""
    Ahat = jnp.fft.rfft2(A)
    return jnp.fft.irfft2(Ahat[ksrc] * khat, s=A.shape[-2:])


def sensorimotor(U, A, Gf, light, p, cfg: Config):
    """Per-cell MLP: neighbourhood composition -> (growth, flux, drift).

    The genome field enters as FiLM modulation (multiplicative gain and
    additive bias on the hidden pre-activation), which lets two cells with
    the same neighbourhood but different genomes behave differently. That is
    what allows several species to share one world.
    """
    m = p["bell_m"][:, None, None]
    s = jnp.abs(p["bell_s"][:, None, None]) + 1e-3
    B = 2.0 * jnp.exp(-0.5 * ((U - m) / s) ** 2) - 1.0

    X = jnp.concatenate([U, B, A, light[None]], axis=0)     # (F, H, W)

    pre = jnp.einsum("fh,fyx->hyx", p["W1"], X) + p["b1"][:, None, None]
    gamma = 1.0 + jnp.einsum("gh,gyx->hyx", p["Wg1"], Gf)
    beta = jnp.einsum("gh,gyx->hyx", p["Wg2"], Gf)
    h = jnp.tanh(pre * gamma + beta)

    out = jnp.einsum("ho,hyx->oyx", p["W2"], h) + p["b2"][:, None, None]
    c = cfg.channels
    E = cfg.e_scale * jnp.tanh(out[:c])
    gain = cfg.gain_max * jax.nn.sigmoid(out[c:2 * c])
    theta = cfg.theta_max * jnp.tanh(out[2 * c:])
    return E, gain, theta


def _grad2(f: jnp.ndarray) -> tuple[jnp.ndarray, jnp.ndarray]:
    """Centred periodic gradient, (d/dy, d/dx)."""
    gy = 0.5 * (jnp.roll(f, -1, axis=-2) - jnp.roll(f, 1, axis=-2))
    gx = 0.5 * (jnp.roll(f, -1, axis=-1) - jnp.roll(f, 1, axis=-1))
    return gy, gx


def flow_field(E, gain, theta, A, cfg: Config):
    """v = gain * R(theta) grad(E) - alpha grad(A_total), softly bounded.

    The rotation is the active term: it makes the flow non-gradient, so the
    dynamics need not relax to a potential minimum. The alpha term is the
    only thing stopping mass from collapsing to a delta.
    """
    gEy, gEx = _grad2(E)
    ct, st = jnp.cos(theta), jnp.sin(theta)
    ry = ct * gEy - st * gEx
    rx = st * gEy + ct * gEx

    gAy, gAx = _grad2(jnp.sum(A, axis=0))
    vy = gain * ry - cfg.alpha * gAy
    vx = gain * rx - cfg.alpha * gAx

    dy, dx = cfg.dt * vy, cfg.dt * vx
    mag = jnp.sqrt(dy ** 2 + dx ** 2) + EPS
    # Smooth saturation keeps |d| < max_step strictly (bang-bang clipping
    # would make every cell move at the ceiling and destroy the gradients).
    scale = cfg.max_step * jnp.tanh(mag / cfg.max_step) / mag
    return dy * scale, dx * scale


def reintegrate(A, Gf, dy, dx, cfg: Config):
    """Mass-conserving transport by reintegration tracking.

    Each source cell's mass is moved to a sub-cell target position and split
    bilinearly over the neighbouring cells. The bilinear weights of one
    source sum to exactly 1 over the stencil (partition of unity), so the
    total is preserved by construction rather than by correction, and the
    scheme is far less diffusive than donor-cell upwinding.

    The genome field rides along as a mass-weighted mixture: where two
    organisms' mass merges into one cell, their genomes blend in proportion
    to the mass each contributed.
    """
    w = cfg.window
    ax = (-2, -1)
    A_new = jnp.zeros_like(A)

    if cfg.advect_genome:
        Atot = jnp.sum(A, axis=0)
        # The genome is a property of matter, not of a channel, so it travels
        # on the mass-weighted mean displacement of all channels present.
        dy_t = jnp.sum(A * dy, axis=0) / (Atot + EPS)
        dx_t = jnp.sum(A * dx, axis=0) / (Atot + EPS)
        g_num = jnp.zeros_like(Gf)
        g_den = jnp.zeros_like(Atot)

    for oi in range(-w, w + 1):
        for oj in range(-w, w + 1):
            sh = (oi, oj)
            wy = jnp.clip(1.0 - jnp.abs(oi - jnp.roll(dy, sh, axis=ax)), 0.0, 1.0)
            wx = jnp.clip(1.0 - jnp.abs(oj - jnp.roll(dx, sh, axis=ax)), 0.0, 1.0)
            A_new = A_new + wy * wx * jnp.roll(A, sh, axis=ax)

            if cfg.advect_genome:
                ty = jnp.clip(1.0 - jnp.abs(oi - jnp.roll(dy_t, sh, axis=ax)),
                              0.0, 1.0)
                tx = jnp.clip(1.0 - jnp.abs(oj - jnp.roll(dx_t, sh, axis=ax)),
                              0.0, 1.0)
                wt = ty * tx * jnp.roll(Atot, sh, axis=ax)
                g_num = g_num + wt * jnp.roll(Gf, sh, axis=ax)
                g_den = g_den + wt

    if not cfg.advect_genome:
        return A_new, Gf
    return A_new, jnp.where(g_den > 1e-9, g_num / (g_den + EPS), Gf)


@partial(jax.jit, static_argnums=(5,))
def step(A, Gf, light, p, bank, cfg: Config):
    """One full sense -> decide -> flow -> transport update."""
    khat, ksrc = bank
    U = perceive(A, khat, ksrc)
    E, gain, theta = sensorimotor(U, A, Gf, light, p, cfg)
    dy, dx = flow_field(E, gain, theta, A, cfg)
    A_new, Gf_new = reintegrate(A, Gf, dy, dx, cfg)
    return A_new, Gf_new, dy, dx


@partial(jax.jit, static_argnums=(5, 6))
def rollout(A, Gf, light, p, bank, cfg: Config, n_steps: int):
    """Run n_steps under lax.scan. Returns final state and the mass trace."""

    def body(carry, _):
        a, g = carry
        a, g, _, _ = step(a, g, light, p, bank, cfg)
        return (a, g), jnp.sum(a)

    (A_out, G_out), mass = jax.lax.scan(body, (A, Gf), None, length=n_steps)
    return A_out, G_out, mass


# ==========================================================================
# World: stateful wrapper
# ==========================================================================


class World:
    """A living world: fields, brain, perception bank, and the seeding and
    perturbation operators the viewer and the discovery loop both use."""

    def __init__(self, cfg: Config, spec: KernelSpec, params: dict,
                 seed: int = 0):
        self.cfg = cfg
        self.spec = spec
        self.params = params_to_jax(params)
        self.bank = build_bank(spec, cfg)
        self.rng = np.random.default_rng(seed)

        n = cfg.size
        self.A = jnp.zeros((cfg.channels, n, n))
        self.Gf = jnp.zeros((cfg.genome_dim, n, n))
        self.light = jnp.zeros((n, n))
        self.dy = jnp.zeros((cfg.channels, n, n))
        self.dx = jnp.zeros((cfg.channels, n, n))
        self.t = 0
        self.mass_0 = 0.0

    # -- construction ------------------------------------------------------

    @staticmethod
    def random(cfg: Config, seed: int) -> "World":
        rng = np.random.default_rng(seed)
        return World(cfg, KernelSpec.sample(rng, cfg), sample_params(rng, cfg),
                     seed=seed)

    # -- seeding -----------------------------------------------------------

    def spawn(self, cy: float, cx: float, genome: np.ndarray,
              radius: float = 14.0, peak: float = 1.0,
              channel_mix: np.ndarray | None = None,
              noise: float = 0.25, seed: int | None = None) -> None:
        """Drop a creature: a soft blob of mass plus its genome, written into
        the genome field wherever the new mass dominates."""
        cfg = self.cfg
        n = cfg.size
        rng = np.random.default_rng(seed) if seed is not None else self.rng

        yy, xx = np.meshgrid(np.arange(n), np.arange(n), indexing="ij")
        dy = np.abs(((yy - cy + n / 2) % n) - n / 2)
        dx = np.abs(((xx - cx + n / 2) % n) - n / 2)
        r = np.sqrt(dy ** 2 + dx ** 2)
        body = np.clip(1.0 - (r / radius) ** 2, 0.0, 1.0) ** 0.75
        body = body * (1.0 + noise * rng.normal(size=body.shape))
        body = np.clip(body, 0.0, None)

        if channel_mix is None:
            channel_mix = rng.uniform(0.4, 1.0, size=cfg.channels)
        add = peak * np.asarray(channel_mix)[:, None, None] * body[None]

        A = np.asarray(self.A) + add
        # Genome of a cell is the mass-weighted blend of what was already
        # there and what we just dropped: spawning into empty space gives a
        # pure genome, spawning onto an organism gives a hybrid.
        old_tot = np.asarray(jnp.sum(self.A, axis=0))
        new_tot = add.sum(axis=0)
        g_old = np.asarray(self.Gf)
        g_new = np.asarray(genome)[:, None, None] * np.ones_like(new_tot)[None]
        denom = old_tot + new_tot + 1e-9
        Gf = (g_old * old_tot[None] + g_new * new_tot[None]) / denom[None]
        Gf = np.where((old_tot + new_tot)[None] > 1e-6, Gf, g_old)

        self.A = jnp.asarray(A)
        self.Gf = jnp.asarray(Gf)
        self.mass_0 = float(jnp.sum(self.A))

    def set_light(self, cy: float, cx: float, sigma: float = 26.0,
                  amp: float = 1.0) -> None:
        n = self.cfg.size
        yy, xx = np.meshgrid(np.arange(n), np.arange(n), indexing="ij")
        dy = ((yy - cy + n / 2) % n) - n / 2
        dx = ((xx - cx + n / 2) % n) - n / 2
        self.light = jnp.asarray(amp * np.exp(-(dy ** 2 + dx ** 2) /
                                              (2 * sigma ** 2)))
        self.light_pos = (float(cy), float(cx))

    def clear_light(self) -> None:
        self.light = jnp.zeros((self.cfg.size, self.cfg.size))
        self.light_pos = None

    # -- evolution ---------------------------------------------------------

    def step(self, n: int = 1):
        for _ in range(n):
            self.A, self.Gf, self.dy, self.dx = step(
                self.A, self.Gf, self.light, self.params, self.bank, self.cfg)
            self.t += 1
        return self.A

    def run(self, n: int):
        """Fast path: compiled scan, no per-step Python."""
        self.A, self.Gf, mass = rollout(
            self.A, self.Gf, self.light, self.params, self.bank, self.cfg, n)
        self.t += n
        return np.asarray(mass)

    # -- diagnostics -------------------------------------------------------

    def mass(self) -> float:
        return float(jnp.sum(self.A))

    def mass_drift(self) -> float:
        if self.mass_0 <= 0:
            return 0.0
        return abs(self.mass() - self.mass_0) / self.mass_0

    def speed_field(self) -> np.ndarray:
        return np.asarray(jnp.sqrt(jnp.sum(self.dy ** 2 + self.dx ** 2, axis=0)))

    # -- perturbation operators -------------------------------------------

    def mutation_brush(self, cy: float, cx: float, radius: float = 12.0,
                       strength: float = 0.5, seed: int | None = None) -> int:
        """Radioactive brush: stochastic perturbation of the LOCAL genome.

        Only cells carrying mass are mutated (mutating vacuum would be
        washed away on the next transport step and would silently do
        nothing). Returns the number of cells actually altered, so a brush
        stroke that hit empty space reports zero instead of pretending.
        """
        n = self.cfg.size
        rng = np.random.default_rng(seed) if seed is not None else self.rng
        yy, xx = np.meshgrid(np.arange(n), np.arange(n), indexing="ij")
        dy = ((yy - cy + n / 2) % n) - n / 2
        dx = ((xx - cx + n / 2) % n) - n / 2
        env = np.exp(-(dy ** 2 + dx ** 2) / (2 * (radius / 2) ** 2))

        tot = np.asarray(jnp.sum(self.A, axis=0))
        live = tot > (0.02 * max(tot.max(), 1e-9))
        mask = env * live
        hit = int(np.count_nonzero(mask > 0.05))

        noise = rng.normal(0, strength, size=(self.cfg.genome_dim, n, n))
        self.Gf = jnp.asarray(np.asarray(self.Gf) + noise * mask[None])
        return hit

    def scalpel(self, cy: float, cx: float, radius: float = 10.0) -> float:
        """Excise mass. Returns the mass removed (this intentionally breaks
        conservation, so the caller must rebaseline)."""
        n = self.cfg.size
        yy, xx = np.meshgrid(np.arange(n), np.arange(n), indexing="ij")
        dy = ((yy - cy + n / 2) % n) - n / 2
        dx = ((xx - cx + n / 2) % n) - n / 2
        keep = ((dy ** 2 + dx ** 2) > radius ** 2).astype(float)
        before = self.mass()
        self.A = self.A * jnp.asarray(keep)[None]
        removed = before - self.mass()
        self.mass_0 = self.mass()
        return removed

    # -- serialization -----------------------------------------------------

    def genome_json(self, name: str, extra: dict | None = None) -> str:
        return json.dumps({
            "name": name,
            "config": asdict(self.cfg),
            "kernels": asdict(self.spec),
            "params": params_to_json(self.params),
            **(extra or {}),
        }, indent=2)

    @staticmethod
    def from_json(data: dict, seed: int = 0) -> "World":
        cfg = Config(**data["config"])
        spec = KernelSpec(**data["kernels"])
        return World(cfg, spec, {k: np.asarray(v)
                                 for k, v in data["params"].items()}, seed=seed)
