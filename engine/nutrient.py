"""Food and a neutral lineage tag for the neural field (ROADMAP step 4, plus a marker).

This module adds two things on top of `engine.neural_field`, without changing that file:

Food
----
A food field F(x) lives beside the body channels A. After the usual sense -> flow ->
transport step, three local updates run:

    uptake   U    = F * (1 - exp(-k * A_tot))     a cell eats from the food it sits on;
                    * A_tot^2/(A_tot^2+theta^2)   never more than the food there, crowded
                                                  cells eat less per unit of mass, and
                                                  faint tails (density << theta) barely eat
    decay    L_c  = d * A_c                       body slowly breaks back down into food
    A_c     <- A_c - L_c + U * A_c / A_tot        new mass keeps the cell's channel mix
    F       <- F + sum_c L_c - sum_c (U * A_c / A_tot)
    F       <- F + D * laplacian(F)               food spreads (periodic 5-point stencil)

What leaves food enters body and the other way round, written so that the two sides are
the same numbers with opposite signs, and the periodic Laplacian sums to zero. So
sum(A) + sum(F) is conserved to float rounding, which is the invariant the engine is built
on. The brain does not see food: the curated species were found with three body channels,
and giving them a food sense would mean new brains. Organisms forage blind, so anything
food selects for acts through movement and shape.

Mass that appears through uptake is added to a cell that already has mass, so it takes the
genome already there; decay removes mass without changing the genome. Lineages therefore
grow and shrink only through how much food their bodies take in.

Neutral tag
-----------
`tagged()` appends one extra genome dimension whose FiLM weights (rows of Wg1 and Wg2) are
zero. The brain cannot read it, but it is carried and blended with the mass exactly like
the functional genome. Two lineages with the same functional genome and opposite tags are
a neutral competition: any change in their mass shares is position, chance or numerics,
never genetics. This is the marker-swap control that microbial competition assays use.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from functools import partial

import jax
import jax.numpy as jnp
import numpy as np

from engine import neural_field as nf


@dataclass(frozen=True)
class Food:
    """Food parameters. Frozen so it can be a jit static argument."""

    enabled: bool = True
    uptake: float = 0.05        # k: per-step uptake rate constant
    decay: float = 5e-4         # d: fraction of body that returns to food each step
    diffusion: float = 0.1      # D: food diffusion coefficient (stable for D <= 0.25)
    # theta: body density at which a cell eats at half its full rate. Uptake is scaled by
    # A_tot^2 / (A_tot^2 + theta^2), so organism tissue (density 1 to 5) eats normally and the
    # faint tails that bilinear transport leaves everywhere (density ~0.01) cannot grow.
    # Without it (theta = 0) the first pilot turned every species into a lawn covering the
    # whole dish within 5,000 steps.
    threshold: float = 0.3


def tagged(cfg: nf.Config, params: dict) -> tuple[nf.Config, dict]:
    """Config and brain with one extra, unread genome dimension (the lineage tag)."""
    p = {k: np.asarray(v, dtype=np.float64).copy() for k, v in params.items()}
    hd = p["Wg1"].shape[1]
    p["Wg1"] = np.vstack([p["Wg1"], np.zeros((1, hd))])
    p["Wg2"] = np.vstack([p["Wg2"], np.zeros((1, hd))])
    return replace(cfg, genome_dim=cfg.genome_dim + 1), p


def react(A, F, food: Food):
    """Uptake and decay. Returns (A, F) with sum(A) + sum(F) unchanged up to rounding."""
    Atot = jnp.sum(A, axis=0)
    U = F * (1.0 - jnp.exp(-food.uptake * Atot))
    if food.threshold > 0.0:
        U = U * Atot ** 2 / (Atot ** 2 + food.threshold ** 2)
    frac = jnp.where(Atot > 0.0, A / jnp.where(Atot > 0.0, Atot, 1.0), 0.0)
    gain = U[None] * frac                       # per channel, sums to U where body exists
    loss = food.decay * A
    A_new = A - loss + gain
    F_new = F + jnp.sum(loss, axis=0) - jnp.sum(gain, axis=0)
    return A_new, F_new


def diffuse(F, D: float):
    lap = (jnp.roll(F, 1, axis=0) + jnp.roll(F, -1, axis=0)
           + jnp.roll(F, 1, axis=1) + jnp.roll(F, -1, axis=1) - 4.0 * F)
    return F + D * lap


@partial(jax.jit, static_argnums=(6, 7))
def step(A, Gf, F, light, p, bank, cfg: nf.Config, food: Food):
    """One neural_field step, then food uptake, decay and diffusion."""
    khat, ksrc = bank
    U = nf.perceive(A, khat, ksrc)
    E, gain, theta = nf.sensorimotor(U, A, Gf, light, p, cfg)
    dy, dx = nf.flow_field(E, gain, theta, A, cfg)
    A, Gf = nf.reintegrate(A, Gf, dy, dx, cfg)
    if food.enabled:
        A, F = react(A, F, food)
        F = diffuse(F, food.diffusion)
    return A, Gf, F


@partial(jax.jit, static_argnums=(6, 7, 8))
def rollout(A, Gf, F, light, p, bank, cfg: nf.Config, food: Food, n_steps: int):
    def body(carry, _):
        a, g, f = carry
        a, g, f = step(a, g, f, light, p, bank, cfg, food)
        return (a, g, f), None

    (A, Gf, F), _ = jax.lax.scan(body, (A, Gf, F), None, length=n_steps)
    return A, Gf, F
