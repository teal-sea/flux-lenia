"""Summarize outputs/variance_decay_20261103/*.json against the decision rule in
docs/VARIANCE-DECAY-2026-11-03.md. Prints a markdown table and the verdict.

Usage: python scripts/variance_decay_summary.py [OUTDIR]
"""

from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def fmt(x, steps):
    return f"> {steps:,}" if x is None else f"{x:,}"


def main() -> None:
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "outputs" / "variance_decay_20261103"
    runs = [json.loads(p.read_text()) for p in sorted(out.glob("SPECIES_*.json"))]
    runs.sort(key=lambda r: (r["species"], not r["advect_genome"], r["placement_seed"]))
    print(f"{len(runs)} runs\n")
    print("| species | seed | advect | first contact | var_s half-life | var_between half-life "
          "| pure_frac half-life | final var_s / start | final hybrid_frac | final blobs A/B/hybrid | mass drift |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for r in runs:
        s, hl, f = r["series"], r["half_life"], r["final"]
        print(f"| {r['species'].split('_', 2)[2]} | {r['placement_seed']} | {'on' if r['advect_genome'] else 'off'} "
              f"| {fmt(r['first_contact_step'], r['steps'])} | {fmt(hl['var_s'], r['steps'])} "
              f"| {fmt(hl['var_between'], r['steps'])} | {fmt(hl['pure_frac'], r['steps'])} "
              f"| {s['var_s'][-1] / s['var_s'][0]:.3f} | {f['hybrid_frac']:.3f} "
              f"| {f['n_blobs_A']}/{f['n_blobs_B']}/{f['n_blobs_hybrid']} | {r['max_rel_mass_drift']:.1e} |")

    on = [r for r in runs if r["advect_genome"]]
    touched = [r for r in on if r["first_contact_step"] is not None]
    untouched = [r for r in on if r["first_contact_step"] is None]
    # a half-life that never happened counts as the run length plus one sample (it is "> steps")
    hl = [r["half_life"]["var_s"] if r["half_life"]["var_s"] is not None else r["steps"] + r["sample_every"]
          for r in touched]
    print()
    print(f"advect on: {len(on)} runs, {len(touched)} with contact, {len(untouched)} never touched")
    if hl:
        med = statistics.median(hl)
        verdict = "short" if med < 1000 else ("long" if med > 10000 else "intermediate")
        print(f"median var_s half-life over runs with contact: {med:,} steps "
              f"(values: {sorted(hl)}; {sum(1 for r in touched if r['half_life']['var_s'] is None)} never halved, "
              f"counted as > {on[0]['steps']:,})")
        print(f"verdict by the fixed rule: {verdict}")


if __name__ == "__main__":
    main()
