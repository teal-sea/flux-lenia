"""Invariant oracle: the gates a candidate must pass to be called a species.

Four gates, all hard. A candidate is verified only if every one passes.

1. Mass Conservation   -- |m_t - m_0| / m_0 <= 1e-4 at every checkpoint.
2. Non-Triviality      -- neither vacuum collapse nor diffusion into mush.
3. Attractor           -- after a noise blast, re-localize within 200 steps.
4. Dynamic Activity    -- centre-of-mass actually moves, and entropy is
                          being produced (S_dot > 0 in the observed window).

Every gate returns a numeric margin alongside its verdict, so a rejection
says how far off it was rather than just "no". A gate that cannot be
evaluated (e.g. the field is empty) FAILS; it never silently passes.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import jax.numpy as jnp
import numpy as np

from engine.physics import Genome, Simulator

MASS_TOL = 1e-4
VACUUM_MASS_FRAC = 1e-3      # below this fraction of m_0, it's vacuum
MIN_CONCENTRATION = 2.0      # peak/mean ratio below this is uniform mush
MIN_VCM = 1e-3               # cells/step
HEAL_STEPS = 200


@dataclass
class GateResult:
    name: str
    passed: bool
    value: float
    detail: str = ""


@dataclass
class OracleReport:
    passed: bool
    gates: list[GateResult] = field(default_factory=list)
    metrics: dict = field(default_factory=dict)

    def summary(self) -> str:
        lines = []
        for g in self.gates:
            mark = "PASS" if g.passed else "FAIL"
            lines.append(f"  [{mark}] {g.name:<22} value={g.value:.6g}  {g.detail}")
        return "\n".join(lines)


# --------------------------------------------------------------------------
# Field statistics
# --------------------------------------------------------------------------


def concentration(rho: jnp.ndarray) -> float:
    """Peak-to-mean ratio. 1.0 means perfectly uniform; high means localized."""
    mean = float(jnp.mean(rho))
    if mean <= 0:
        return 0.0
    return float(jnp.max(rho)) / mean


def center_of_mass(rho: jnp.ndarray) -> tuple[float, float]:
    """Periodic (circular) centre of mass of the summed density, in cells."""
    total = jnp.sum(rho, axis=0) if rho.ndim == 3 else rho
    n = total.shape[0]
    m = float(jnp.sum(total))
    if m <= 0:
        return (float("nan"), float("nan"))
    ang = 2 * jnp.pi * jnp.arange(n) / n
    cx = jnp.sum(total, axis=0)
    cy = jnp.sum(total, axis=1)

    def circ(w):
        a = jnp.sum(w * jnp.cos(ang)) / m
        b = jnp.sum(w * jnp.sin(ang)) / m
        return float((jnp.arctan2(b, a) % (2 * jnp.pi)) * n / (2 * jnp.pi))

    return circ(cx), circ(cy)


def _wrap_delta(a: float, b: float, n: int) -> float:
    return ((a - b + n / 2) % n) - n / 2


def spatial_entropy(rho: jnp.ndarray) -> float:
    """Shannon entropy of the normalized density. Rises as mass spreads."""
    p = jnp.sum(rho, axis=0) if rho.ndim == 3 else rho
    tot = jnp.sum(p)
    if float(tot) <= 0:
        return 0.0
    p = (p / tot).ravel()
    p = jnp.where(p > 0, p, 1.0)
    return float(-jnp.sum(p * jnp.log(p)))


# --------------------------------------------------------------------------
# Trajectory recording
# --------------------------------------------------------------------------


def run_trajectory(sim: Simulator, steps: int, sample_every: int = 10) -> dict:
    """Advance the simulator, sampling invariants along the way."""
    rec = {"step": [], "mass": [], "conc": [], "entropy": [], "com": []}

    def sample():
        rec["step"].append(sim.t)
        rec["mass"].append(sim.mass())
        rec["conc"].append(concentration(sim.rho))
        rec["entropy"].append(spatial_entropy(sim.rho))
        rec["com"].append(center_of_mass(sim.rho))

    sample()
    for _ in range(steps // sample_every):
        sim.step(sample_every)
        sample()
        if not np.isfinite(sim.mass()):
            break
    return rec


# --------------------------------------------------------------------------
# Gates
# --------------------------------------------------------------------------


def gate_mass(rec: dict) -> GateResult:
    m = np.asarray(rec["mass"], dtype=float)
    if m.size == 0 or not np.all(np.isfinite(m)) or m[0] <= 0:
        return GateResult("mass_conservation", False, float("inf"),
                          "non-finite or empty mass record")
    drift = float(np.max(np.abs(m - m[0])) / m[0])
    return GateResult("mass_conservation", drift <= MASS_TOL, drift,
                      f"tol={MASS_TOL:g}, m0={m[0]:.6f}")


def gate_nontrivial(rec: dict) -> GateResult:
    m = np.asarray(rec["mass"], dtype=float)
    conc = np.asarray(rec["conc"], dtype=float)
    if conc.size == 0 or not np.all(np.isfinite(conc)):
        return GateResult("non_triviality", False, 0.0, "no concentration data")
    if m[-1] < VACUUM_MASS_FRAC * m[0]:
        return GateResult("non_triviality", False, float(conc[-1]),
                          "collapsed to vacuum")
    final = float(conc[-1])
    return GateResult("non_triviality", final >= MIN_CONCENTRATION, final,
                      f"peak/mean, need >= {MIN_CONCENTRATION}")


def dynamic_activity(rec: dict, size: int, dt: float, sample_every: int
                     ) -> tuple[GateResult, float, float]:
    """v_cm (cells/time) and entropy production rate S_dot."""
    coms = rec["com"]
    ent = np.asarray(rec["entropy"], dtype=float)
    if len(coms) < 3 or any(not np.isfinite(c[0]) for c in coms):
        return (GateResult("dynamic_activity", False, 0.0, "no COM track"),
                0.0, 0.0)

    interval = sample_every * dt
    speeds = [
        np.hypot(_wrap_delta(x1, x0, size), _wrap_delta(y1, y0, size)) / interval
        for (x0, y0), (x1, y1) in zip(coms[:-1], coms[1:])
    ]
    v_cm = float(np.mean(speeds))

    # Entropy production rate: mean absolute rate of change of spatial entropy.
    # A live soliton continually reshapes mass; a frozen one does not.
    s_dot = float(np.mean(np.abs(np.diff(ent))) / interval)

    ok = v_cm > MIN_VCM and s_dot > 0.0
    detail = f"v_cm={v_cm:.5f} (>{MIN_VCM:g}), S_dot={s_dot:.3e} (>0)"
    return GateResult("dynamic_activity", ok, v_cm, detail), v_cm, s_dot


MIN_DISRUPTION = 0.05        # a blast that moves nothing proves nothing
RECOVERY_BAND = (0.80, 1.25)


def gate_attractor(genome: Genome, rho_final: jnp.ndarray,
                   noise_amplitude: float = 1.5) -> tuple[GateResult, dict]:
    """Blast the settled state with a localized noise pulse; does it re-form?

    Concentration is measured before the blast, right after it, and after
    HEAL_STEPS of relaxation. Note the blast RAISES peak/mean (noise spikes
    lift the peak), so recovery is judged as a two-sided return to the
    pre-blast value, not as an increase from the post-blast value.

    The gate also refuses to pass on a blast that barely perturbed the field:
    a perturbation test that did not perturb is not evidence of an attractor,
    so it fails loudly rather than passing by default.
    """
    conc_before = concentration(rho_final)
    if conc_before <= 0:
        return (GateResult("attractor_self_heal", False, 0.0,
                           "degenerate pre-blast state"), {})

    sim = Simulator(genome, rho=rho_final)
    sim.inject_noise(amplitude=noise_amplitude, key_seed=genome.seed + 77)
    conc_after_blast = concentration(sim.rho)

    rec = run_trajectory(sim, HEAL_STEPS, sample_every=20)
    conc_healed = concentration(sim.rho)

    mass_ok = gate_mass(rec).passed
    disruption = abs(conc_after_blast / conc_before - 1.0)
    recovery = conc_healed / conc_before
    lo, hi = RECOVERY_BAND

    disrupted = disruption >= MIN_DISRUPTION
    recovered = lo <= recovery <= hi
    coherent = conc_healed >= MIN_CONCENTRATION
    ok = disrupted and recovered and coherent and mass_ok

    reasons = []
    if not disrupted:
        reasons.append(f"blast too weak (disruption {disruption:.3f} < "
                       f"{MIN_DISRUPTION})")
    if not recovered:
        reasons.append(f"recovery {recovery:.3f} outside [{lo}, {hi}]")
    if not coherent:
        reasons.append("healed state not localized")
    if not mass_ok:
        reasons.append("mass drifted while healing")

    detail = (f"conc {conc_before:.2f} -> blast {conc_after_blast:.2f} -> "
              f"healed {conc_healed:.2f} in {HEAL_STEPS} steps"
              + ("; " + "; ".join(reasons) if reasons else "; clean self-heal"))
    info = {
        "conc_before": conc_before,
        "conc_after_blast": conc_after_blast,
        "conc_healed": conc_healed,
        "disruption": disruption,
        "recovery": recovery,
        "heal_mass_ok": mass_ok,
    }
    return GateResult("attractor_self_heal", ok, recovery, detail), info


# --------------------------------------------------------------------------
# Full evaluation
# --------------------------------------------------------------------------


def evaluate(genome: Genome, steps: int = 400, sample_every: int = 10
             ) -> tuple[OracleReport, Simulator]:
    """Run a candidate and put it through every gate. Never swallows failure."""
    sim = Simulator(genome)
    rec = run_trajectory(sim, steps, sample_every)

    gates = [gate_mass(rec), gate_nontrivial(rec)]
    act, v_cm, s_dot = dynamic_activity(rec, genome.size, genome.dt, sample_every)
    gates.append(act)

    # Only worth blasting a candidate that is still coherent.
    if gates[1].passed:
        att, att_info = gate_attractor(genome, sim.rho)
    else:
        att, att_info = GateResult(
            "attractor_self_heal", False, 0.0,
            "skipped: candidate failed non-triviality"), {}
    gates.append(att)

    metrics = {
        "steps": steps,
        "mass_0": rec["mass"][0],
        "mass_final": rec["mass"][-1],
        "mass_drift": gates[0].value,
        "concentration_final": rec["conc"][-1],
        "entropy_final": rec["entropy"][-1],
        "v_cm": v_cm,
        "s_dot": s_dot,
        "com_final": rec["com"][-1],
        **{f"attractor_{k}": v for k, v in att_info.items()},
    }

    return OracleReport(all(g.passed for g in gates), gates, metrics), sim
