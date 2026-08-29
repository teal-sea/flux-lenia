#!/usr/bin/env python3
"""Autonomous hunt runner: sweep non-reciprocal genomes, gate them, log them.

Usage:
    python scripts/run_hunt.py            # HUNT 001..005
    python scripts/run_hunt.py 3 9        # HUNT 003..009

Every hunt writes a report to hunts/, verified or not. A rejected candidate
is recorded with the gate that rejected it and by how much: a hunt that finds
nothing must say so out loud, with numbers, not fall silent.
"""

from __future__ import annotations

import json
import sys
import time
from dataclasses import asdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt          # noqa: E402
import numpy as np                        # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from engine.oracle import evaluate         # noqa: E402
from engine.physics import Genome, Simulator  # noqa: E402

HUNTS = ROOT / "hunts"
OUTPUTS = ROOT / "outputs"
STEPS = 400

SPECIES_NAMES = {
    1: "CHASER_DYAD",
    2: "ORBITAL_PAIR",
    3: "FLEEING_SHELL",
    4: "PULSE_WANDERER",
    5: "TWIN_VORTEX",
    6: "SLOW_CRAWLER",
    7: "SHEAR_RIBBON",
    8: "CORE_HALO",
    9: "DRIFT_LATTICE",
}


def genome_for(hunt_id: int) -> Genome:
    """Deterministic sweep over the non-reciprocal parameter space.

    The asymmetry is the point: K[0][1] (how 0 responds to 1) and K[1][0]
    (how 1 responds to 0) are drawn independently and with opposite sign,
    so channel 0 pursues while channel 1 retreats.
    """
    rng = np.random.default_rng(1000 + hunt_id)

    chase = -float(rng.uniform(1.6, 3.2))     # 0 attracted to 1
    flee = float(rng.uniform(0.8, 2.6))       # 1 repelled by 0
    self0 = -float(rng.uniform(0.6, 1.6))
    self1 = -float(rng.uniform(0.6, 1.6))

    r0 = float(rng.uniform(8.0, 14.0))
    r1 = float(rng.uniform(13.0, 22.0))

    return Genome(
        n_channels=2,
        size=128,
        dx=1.0,
        dt=0.05,
        kernel_radius=[r0, r1],
        kernel_sigma=[float(rng.uniform(2.0, 4.0)),
                      float(rng.uniform(3.0, 5.5))],
        K=[[self0, chase], [flee, self1]],
        self_repulsion=float(rng.uniform(0.4, 1.1)),
        repulsion_sigma=float(rng.uniform(1.5, 3.0)),
        v_max=0.35,
        seed=hunt_id,
    )


def save_snapshot(rho, path: Path, title: str) -> None:
    """Two-channel view: Magma for channel 0, Viridis for channel 1."""
    arr = np.asarray(rho)
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.4))
    for ax, data, cmap, name in (
        (axes[0], arr[0], "magma", "channel 0 (chaser)"),
        (axes[1], arr[1], "viridis", "channel 1 (fleer)"),
    ):
        ax.imshow(data, cmap=cmap, interpolation="bilinear")
        ax.set_title(name, fontsize=10)
        ax.axis("off")

    rgb = np.zeros(arr.shape[1:] + (3,))
    a = arr[0] / (arr[0].max() + 1e-12)
    b = arr[1] / (arr[1].max() + 1e-12)
    rgb[..., 0] = a
    rgb[..., 1] = b
    rgb[..., 2] = 0.35 * (a + b)
    axes[2].imshow(np.clip(rgb, 0, 1), interpolation="bilinear")
    axes[2].set_title("composite", fontsize=10)
    axes[2].axis("off")

    fig.suptitle(title, fontsize=11)
    fig.tight_layout()
    fig.savefig(path, dpi=110)
    plt.close(fig)


def write_report(hunt_id: int, species: str, genome: Genome, report,
                 snapshots: list[Path], elapsed: float) -> Path:
    status = "VERIFIED" if report.passed else "REJECTED"
    name = species if report.passed else "REJECTED"
    path = HUNTS / f"HUNT_{hunt_id:03d}_{name}.md"

    lines = [
        f"# HUNT {hunt_id:03d} — {species}",
        "",
        f"**Status:** {status}",
        f"**Steps:** {STEPS}  |  **Wall clock:** {elapsed:.1f}s",
        "",
        "## Gates",
        "",
        "| gate | verdict | value | detail |",
        "| --- | --- | --- | --- |",
    ]
    for g in report.gates:
        lines.append(
            f"| {g.name} | {'PASS' if g.passed else 'FAIL'} | "
            f"{g.value:.6g} | {g.detail} |"
        )

    lines += ["", "## Metrics", "", "```json",
              json.dumps(report.metrics, indent=2, default=float), "```",
              "", "## Genome", "", "```json", genome.to_json(), "```",
              "", "## Snapshots", ""]
    for s in snapshots:
        lines.append(f"- `outputs/{s.name}`")
    lines.append("")

    path.write_text("\n".join(lines))
    return path


def run_one(hunt_id: int) -> dict:
    species = SPECIES_NAMES.get(hunt_id, f"SPECIES_{hunt_id:03d}")
    genome = genome_for(hunt_id)
    print(f"\n=== HUNT {hunt_id:03d} ({species}) ===")

    t0 = time.time()
    report, sim = evaluate(genome, steps=STEPS)
    elapsed = time.time() - t0

    snaps = []
    tag = f"HUNT_{hunt_id:03d}_{species}"
    p_final = OUTPUTS / f"{tag}_final.png"
    save_snapshot(sim.rho, p_final, f"{tag} — t={STEPS}")
    snaps.append(p_final)

    # An initial-condition snapshot makes the sweep visually comparable.
    p_init = OUTPUTS / f"{tag}_init.png"
    save_snapshot(Simulator(genome).rho, p_init, f"{tag} — t=0")
    snaps.insert(0, p_init)

    (OUTPUTS / f"{tag}_genome.json").write_text(genome.to_json())

    print(report.summary())
    print(f"  -> {'VERIFIED' if report.passed else 'REJECTED'} "
          f"in {elapsed:.1f}s")

    path = write_report(hunt_id, species, genome, report, snaps, elapsed)
    return {
        "hunt": hunt_id,
        "species": species,
        "verified": report.passed,
        "report": str(path.relative_to(ROOT)),
        "failed_gates": [g.name for g in report.gates if not g.passed],
        "metrics": report.metrics,
        "genome": asdict(genome),
        "elapsed_s": elapsed,
    }


def main() -> int:
    HUNTS.mkdir(exist_ok=True)
    OUTPUTS.mkdir(exist_ok=True)

    lo = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    hi = int(sys.argv[2]) if len(sys.argv) > 2 else 5

    results = [run_one(i) for i in range(lo, hi + 1)]
    verified = [r for r in results if r["verified"]]

    index = HUNTS / "INDEX.json"
    index.write_text(json.dumps(
        {"generated": time.strftime("%Y-%m-%dT%H:%M:%S"),
         "range": [lo, hi], "runs": results}, indent=2, default=float))

    print("\n" + "=" * 60)
    print(f"HUNT SWEEP {lo:03d}-{hi:03d}: {len(results)} candidates run, "
          f"{len(verified)} VERIFIED, {len(results) - len(verified)} rejected")
    if not verified:
        # Zero is reported, never swallowed.
        print("ZERO verified species this sweep. Rejection reasons:")
        for r in results:
            print(f"  HUNT {r['hunt']:03d}: {', '.join(r['failed_gates'])}")
    else:
        for r in verified:
            m = r["metrics"]
            print(f"  HUNT {r['hunt']:03d} {r['species']}: "
                  f"drift={m['mass_drift']:.2e} conc={m['concentration_final']:.2f} "
                  f"v_cm={m['v_cm']:.4f}")
    print(f"Index: {index.relative_to(ROOT)}")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
