"""Multi-channel continuous-field simulator with strict mass conservation.

Physics
-------
Each channel c carries a mass density rho_c(x, y) >= 0 on a periodic grid.
Channels perceive each other non-locally through ring kernels:

    U_j   = rho_j (*) ring_j                 (FFT convolution)
    Phi_i = sum_j K[i, j] * U_j              (asymmetric coupling matrix)
    v_i   = -grad Phi_i                      (advective velocity)
    d rho_i / dt = -div (rho_i v_i)          (continuity equation)

K is NOT required to be symmetric. K[0,1] != K[1,0] breaks Newton's third
law: channel 0 can chase channel 1 while channel 1 flees channel 0. That
non-reciprocity is the engine of the chaser/fleer dynamics we hunt for.

Mass conservation
-----------------
The update is written in flux form on a staggered grid. The change of a cell
is the difference of the two face fluxes that bound it, and every face flux
appears exactly twice with opposite sign across the periodic domain. The sum
of all updates is therefore an exactly telescoping sum: total mass is
conserved to floating-point rounding, not merely approximately. We run in
float64 so that rounding is ~1e-15 per step rather than ~1e-7.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict, field

import jax
import jax.numpy as jnp

jax.config.update("jax_enable_x64", True)


# --------------------------------------------------------------------------
# Genome
# --------------------------------------------------------------------------


@dataclass
class Genome:
    """The full parameter set that defines one candidate species."""

    n_channels: int = 2
    size: int = 128
    dx: float = 1.0
    dt: float = 0.05

    # Ring kernel per channel: radius (cells) and shell thickness.
    kernel_radius: list[float] = field(default_factory=lambda: [12.0, 18.0])
    kernel_sigma: list[float] = field(default_factory=lambda: [3.0, 4.5])

    # Asymmetric coupling, row-major [n_channels][n_channels].
    # K[i][j] < 0 -> channel i is attracted to the perceived field of j.
    K: list[list[float]] = field(
        default_factory=lambda: [[-1.0, -2.2], [1.6, -1.0]]
    )

    # Short-range repulsion keeping mass from collapsing to a delta.
    self_repulsion: float = 0.6
    repulsion_sigma: float = 2.0

    # Velocity magnitude cap, in cells per step (CFL guard).
    v_max: float = 0.35

    seed: int = 0

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)

    @staticmethod
    def from_dict(d: dict) -> "Genome":
        return Genome(**d)


# --------------------------------------------------------------------------
# Kernels
# --------------------------------------------------------------------------


def _radial_distance(size: int) -> jnp.ndarray:
    """Distance from the origin cell, wrapped periodically (FFT-aligned)."""
    idx = jnp.arange(size)
    d = jnp.minimum(idx, size - idx)
    return jnp.sqrt(d[:, None] ** 2 + d[None, :] ** 2)


def ring_kernel(size: int, radius: float, sigma: float) -> jnp.ndarray:
    """Normalized annular perception kernel, origin-centred for FFT use."""
    r = _radial_distance(size)
    k = jnp.exp(-0.5 * ((r - radius) / sigma) ** 2)
    return k / jnp.sum(k)


def gaussian_kernel(size: int, sigma: float) -> jnp.ndarray:
    r = _radial_distance(size)
    k = jnp.exp(-0.5 * (r / sigma) ** 2)
    return k / jnp.sum(k)


def build_kernels(g: Genome) -> tuple[jnp.ndarray, jnp.ndarray]:
    """Return (perception kernel FFTs [C,H,W], repulsion kernel FFT [H,W])."""
    ks = jnp.stack(
        [
            ring_kernel(g.size, g.kernel_radius[c], g.kernel_sigma[c])
            for c in range(g.n_channels)
        ]
    )
    rep = gaussian_kernel(g.size, g.repulsion_sigma)
    return jnp.fft.rfft2(ks, axes=(-2, -1)), jnp.fft.rfft2(rep)


def _convolve(field_: jnp.ndarray, kernel_ft: jnp.ndarray) -> jnp.ndarray:
    """Periodic convolution via FFT. Batched over leading axes."""
    return jnp.fft.irfft2(
        jnp.fft.rfft2(field_, axes=(-2, -1)) * kernel_ft,
        s=field_.shape[-2:],
        axes=(-2, -1),
    )


# --------------------------------------------------------------------------
# Dynamics
# --------------------------------------------------------------------------


def potential(
    rho: jnp.ndarray, K: jnp.ndarray, kern_ft: jnp.ndarray,
    rep_ft: jnp.ndarray, self_repulsion: float,
) -> jnp.ndarray:
    """Per-channel potential Phi_i = sum_j K_ij U_j + repulsion."""
    perceived = _convolve(rho, kern_ft)              # [C, H, W]
    phi = jnp.einsum("ij,jhw->ihw", K, perceived)
    phi = phi + self_repulsion * _convolve(jnp.sum(rho, axis=0), rep_ft)
    return phi


def _grad(phi: jnp.ndarray, dx: float) -> tuple[jnp.ndarray, jnp.ndarray]:
    """Centred periodic gradient."""
    gx = (jnp.roll(phi, -1, axis=-1) - jnp.roll(phi, 1, axis=-1)) / (2 * dx)
    gy = (jnp.roll(phi, -1, axis=-2) - jnp.roll(phi, 1, axis=-2)) / (2 * dx)
    return gx, gy


def velocity(
    rho: jnp.ndarray, K: jnp.ndarray, kern_ft: jnp.ndarray,
    rep_ft: jnp.ndarray, self_repulsion: float, dx: float, v_max: float,
) -> tuple[jnp.ndarray, jnp.ndarray]:
    """v = -grad Phi, magnitude-limited to v_max for CFL stability."""
    phi = potential(rho, K, kern_ft, rep_ft, self_repulsion)
    gx, gy = _grad(phi, dx)
    vx, vy = -gx, -gy
    mag = jnp.sqrt(vx**2 + vy**2)
    scale = jnp.minimum(1.0, v_max / (mag + 1e-12))
    return vx * scale, vy * scale


def _upwind_flux(rho: jnp.ndarray, v_face: jnp.ndarray, axis: int) -> jnp.ndarray:
    """Donor-cell flux through the face between cell i and cell i+1.

    Upwinding (take the density from whichever cell the flow leaves) is what
    keeps rho >= 0; the flux-difference form is what keeps mass exact.
    """
    rho_up = jnp.where(v_face > 0, rho, jnp.roll(rho, -1, axis=axis))
    return rho_up * v_face


def step(
    rho: jnp.ndarray, K: jnp.ndarray, kern_ft: jnp.ndarray, rep_ft: jnp.ndarray,
    self_repulsion: float, dx: float, dt: float, v_max: float,
) -> jnp.ndarray:
    """One conservative advection step of the continuity equation."""
    vx, vy = velocity(rho, K, kern_ft, rep_ft, self_repulsion, dx, v_max)

    # Face-centred velocities (arithmetic average of the two adjacent cells).
    vx_face = 0.5 * (vx + jnp.roll(vx, -1, axis=-1))
    vy_face = 0.5 * (vy + jnp.roll(vy, -1, axis=-2))

    fx = _upwind_flux(rho, vx_face, axis=-1)
    fy = _upwind_flux(rho, vy_face, axis=-2)

    # Divergence as a difference of the bounding face fluxes: the global sum
    # of this array telescopes to exactly zero on a periodic grid.
    div = (fx - jnp.roll(fx, 1, axis=-1)) / dx + (fy - jnp.roll(fy, 1, axis=-2)) / dx

    return jnp.maximum(rho - dt * div, 0.0)


@jax.jit
def _step_jit(rho, K, kern_ft, rep_ft, self_repulsion, dx, dt, v_max):
    return step(rho, K, kern_ft, rep_ft, self_repulsion, dx, dt, v_max)


class Simulator:
    """Stateful convenience wrapper around the pure step function."""

    def __init__(self, genome: Genome, rho: jnp.ndarray | None = None):
        self.g = genome
        self.K = jnp.asarray(genome.K, dtype=jnp.float64)
        self.kern_ft, self.rep_ft = build_kernels(genome)
        self.rho = seed_field(genome) if rho is None else jnp.asarray(rho)
        self.mass_0 = float(jnp.sum(self.rho))
        self.t = 0

    def step(self, n: int = 1) -> jnp.ndarray:
        for _ in range(n):
            self.rho = _step_jit(
                self.rho, self.K, self.kern_ft, self.rep_ft,
                self.g.self_repulsion, self.g.dx, self.g.dt, self.g.v_max,
            )
            self.t += 1
        return self.rho

    # -- mass bookkeeping ---------------------------------------------------

    def mass(self) -> float:
        return float(jnp.sum(self.rho))

    def mass_drift(self) -> float:
        return abs(self.mass() - self.mass_0) / max(self.mass_0, 1e-30)

    # -- perturbation operators (used by the oracle and the viewer) ---------

    def inject_noise(self, amplitude: float = 0.5, key_seed: int = 1234,
                     radius_frac: float = 0.18) -> None:
        """Localized Gaussian noise pulse aimed at the soliton.

        The pulse is scaled to the field's own mean density and confined to a
        patch, so it is a perturbation of the structure rather than a flood
        that buries it. Rebaselines mass_0: this ADDS mass on purpose, so the
        conservation gate must not read the addition as a leak.
        """
        key = jax.random.PRNGKey(key_seed)
        n = self.g.size
        # Aim at the current centre of mass so the blast actually hits.
        total = jnp.sum(self.rho, axis=0)
        m = jnp.sum(total)
        ang = 2 * jnp.pi * jnp.arange(n) / n

        def circ(w):
            a = jnp.sum(w * jnp.cos(ang)) / m
            b = jnp.sum(w * jnp.sin(ang)) / m
            return (jnp.arctan2(b, a) % (2 * jnp.pi)) * n / (2 * jnp.pi)

        px, py = circ(jnp.sum(total, axis=0)), circ(jnp.sum(total, axis=1))
        yy, xx = jnp.meshgrid(jnp.arange(n), jnp.arange(n), indexing="ij")
        dx_ = jnp.abs(((xx - px + n / 2) % n) - n / 2)
        dy_ = jnp.abs(((yy - py + n / 2) % n) - n / 2)
        envelope = jnp.exp(-(dx_**2 + dy_**2) / (2 * (radius_frac * n) ** 2))

        scale = amplitude * jnp.mean(self.rho)
        noise = scale * jax.random.normal(key, self.rho.shape) * envelope
        self.rho = jnp.maximum(self.rho + noise, 0.0)
        self.mass_0 = self.mass()

    def scalpel(self, axis: int = 0, position: float = 0.5, width: int = 4) -> None:
        """Cut a slice of mass out of the field. Removes mass on purpose."""
        n = self.g.size
        p = int(position * n)
        idx = (jnp.arange(n)[:, None] if axis == 0 else jnp.arange(n)[None, :])
        cut = jnp.abs(((idx - p + n // 2) % n) - n // 2) < width
        self.rho = jnp.where(cut, 0.0, self.rho)
        self.mass_0 = self.mass()


# --------------------------------------------------------------------------
# Initial conditions
# --------------------------------------------------------------------------


def seed_field(g: Genome, blobs: int = 3, mass_per_channel: float = 400.0):
    """Random smooth blobs, normalized so every channel starts equal-mass."""
    key = jax.random.PRNGKey(g.seed)
    n = g.size
    yy, xx = jnp.meshgrid(jnp.arange(n), jnp.arange(n), indexing="ij")

    channels = []
    for c in range(g.n_channels):
        key, k1, k2 = jax.random.split(key, 3)
        cx = jax.random.uniform(k1, (blobs,)) * n
        cy = jax.random.uniform(k2, (blobs,)) * n
        acc = jnp.zeros((n, n))
        for b in range(blobs):
            dx_ = jnp.abs(((xx - cx[b] + n / 2) % n) - n / 2)
            dy_ = jnp.abs(((yy - cy[b] + n / 2) % n) - n / 2)
            acc = acc + jnp.exp(-(dx_**2 + dy_**2) / (2 * (n / 14.0) ** 2))
        channels.append(acc * (mass_per_channel / jnp.sum(acc)))

    return jnp.stack(channels)
