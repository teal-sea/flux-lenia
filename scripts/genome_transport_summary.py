"""Apply the decision rule in docs/GENOME-TRANSPORT-2026-11-10.md.

Usage: python scripts/genome_transport_summary.py [NEWDIR] [OLDDIR]
NEWDIR defaults to outputs/genome_transport_20261110 (per_channel, food off);
OLDDIR to outputs/food_selection_20261109 (mean transport, food-off runs only).
"""

from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPECIES = ["SPECIES_001_OSCILLIS", "SPECIES_002_MITOSA", "SPECIES_003_VAGRANT"]


def load(d: Path) -> dict:
    runs = {}
    for p in sorted(d.glob("SPECIES_*_food0.json")):
        r = json.loads(p.read_text())
        runs[(r["species"], r["arm"], r["seed"])] = r
    return runs


def stats(runs, sp):
    neu = [r for (s, a, _), r in runs.items() if s == sp and a != "treat"]
    tr = sorted((r for (s, a, _), r in runs.items() if s == sp and a == "treat"),
                key=lambda r: r["seed"])
    E = max((abs(r["delta_share_A"]) for r in neu), default=0.0)
    out = [r for r in tr if abs(r["delta_share_A"]) > E]
    return neu, tr, E, out


def main() -> None:
    new = load(Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "outputs/genome_transport_20261110")
    old = load(Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "outputs/food_selection_20261109")
    print(f"{len(new)} new-mode runs, {len(old)} old-mode food-off runs\n")
    print("### Per run (new mode, per_channel)\n")
    print("| species | arm | seed | A start | A end | delta | hybrid at end | blobs | max abs(share_A - start) over run | wall s |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for sp in SPECIES:
        for arm in ("treat", "neutral_plus", "neutral_minus"):
            for s in range(1, 6):
                r = new.get((sp, arm, s))
                if r is None:
                    continue
                sh = r["series"]["share_A"]
                f = r["final"]
                print(f"| {sp[12:]} | {arm} | {s} | {r['share_A_start']:.3f} | {r['share_A_end']:.3f} "
                      f"| {r['delta_share_A']:+.2e} | {f['hybrid_frac']:.2f} | {f['n_blobs']} "
                      f"| {max(abs(x - sh[0]) for x in sh):.2e} | {r['wall_seconds']:.0f} |")
    print("\n### Verdicts (new mode)\n")
    print("| species | n neutral | neutral envelope E | treat seeds outside E | winner(s) | treat deltas (seeds in order) | median treat delta | verdict |")
    print("|---|---|---|---|---|---|---|---|")
    for sp in SPECIES:
        neu, tr, E, out = stats(new, sp)
        if not tr:
            continue
        winners = sorted({"+u" if r["delta_share_A"] > 0 else "-u" for r in out})
        v = "persists" if len(out) >= 4 else "vanished"
        print(f"| {sp[12:]} | {len(neu)} | {E:.2e} | {len(out)} of {len(tr)} | {', '.join(winners) or '-'} "
              f"| {', '.join(f'{r['delta_share_A']:+.2e}' for r in tr)} "
              f"| {statistics.median(r['delta_share_A'] for r in tr):+.2e} | {v} |")
    print("\n### Neutral-arm drift, new vs old mode (|delta|, share points; old = food-off runs of 2026-11-09)\n")
    print("| species | old min | old max (=E_old) | new min | new max (=E_new) | old treat outside E_old | new treat outside E_new |")
    print("|---|---|---|---|---|---|---|")
    for sp in SPECIES:
        on, ot, oE, oo = stats(old, sp)
        nn, nt, nE, no_ = stats(new, sp)
        if not nt:
            continue
        od = [abs(r["delta_share_A"]) * 100 for r in on]
        nd = [abs(r["delta_share_A"]) * 100 for r in nn]
        print(f"| {sp[12:]} | {min(od):.2f} | {max(od):.2f} | {min(nd):.1e} | {max(nd):.1e} "
              f"| {len(oo)} of {len(ot)} | {len(no_)} of {len(nt)} |")


if __name__ == "__main__":
    main()
