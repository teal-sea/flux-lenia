"""Apply the decision rule in docs/FOOD-SELECTION-2026-11-09.md to the run files.

Usage: python scripts/food_selection_summary.py [OUTDIR]
Prints markdown: one table per food setting, then the verdict per species.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPECIES = ["SPECIES_001_OSCILLIS", "SPECIES_002_MITOSA", "SPECIES_003_VAGRANT"]


def load(out: Path) -> dict:
    runs = {}
    for p in sorted(out.glob("SPECIES_*_food[01].json")):
        r = json.loads(p.read_text())
        runs[(r["species"], r["food"], r["arm"], r["seed"])] = r
    return runs


def verdict(runs: dict, sp: str, food: bool) -> dict:
    neutral = [runs[(sp, food, arm, s)] for arm in ("neutral_plus", "neutral_minus")
               for s in range(1, 6) if (sp, food, arm, s) in runs]
    treat = [runs[(sp, food, "treat", s)] for s in range(1, 6) if (sp, food, "treat", s) in runs]
    E = max(abs(r["delta_share_A"]) for r in neutral)
    out = [r for r in treat if abs(r["delta_share_A"]) > E]
    winners = {"+u" if r["delta_share_A"] > 0 else "-u" for r in out}
    win_share = [r["share_A_end"] if r["delta_share_A"] > 0 else 1 - r["share_A_end"] for r in out]
    if len(out) >= 4 and len(winners) == 1:
        v = "takeover" if all(x >= 0.9 for x in win_share) else "selection"
    elif len(out) >= 4:
        v = "large but inconsistent"
    else:
        v = "no selection detected"
    return {"n_neutral": len(neutral), "n_treat": len(treat), "envelope": E,
            "out_of_envelope": len(out), "winners": sorted(winners),
            "winner_final_shares": [round(x, 3) for x in win_share], "verdict": v}


def main() -> None:
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "outputs" / "food_selection_20261109"
    runs = load(out)
    print(f"{len(runs)} runs\n")
    for food in (True, False):
        print(f"### Food {'on' if food else 'off'}\n")
        print("| species | arm | seed | A start | A end | delta | hybrid at end | body / total | blobs at end | total drift |")
        print("|---|---|---|---|---|---|---|---|---|---|")
        for sp in SPECIES:
            for arm in ("treat", "neutral_plus", "neutral_minus"):
                for s in range(1, 6):
                    r = runs.get((sp, food, arm, s))
                    if r is None:
                        print(f"| {sp[12:]} | {arm} | {s} | missing | | | | | | |")
                        continue
                    f = r["final"]
                    bt = f["body"] / (f["body"] + f["food"]) if f["food"] > 0 else 1.0
                    print(f"| {sp[12:]} | {arm} | {s} | {r['share_A_start']:.3f} | {r['share_A_end']:.3f} "
                          f"| {r['delta_share_A']:+.3f} | {f['hybrid_frac']:.2f} | {bt:.2f} | {f['n_blobs']} "
                          f"| {r['max_rel_total_drift']:.0e} |")
        print()
    print("### Verdicts\n")
    print("| species | food | neutral envelope E | treat seeds outside E | winner(s) | winner's final share | verdict |")
    print("|---|---|---|---|---|---|---|")
    res = {}
    for sp in SPECIES:
        for food in (True, False):
            v = verdict(runs, sp, food)
            res[(sp, food)] = v
            print(f"| {sp[12:]} | {'on' if food else 'off'} | {v['envelope']:.3f} | {v['out_of_envelope']} of {v['n_treat']} "
                  f"| {', '.join(v['winners']) or '-'} | {v['winner_final_shares'] or '-'} | {v['verdict']} |")
    print()
    for sp in SPECIES:
        on, off = res[(sp, True)]["verdict"], res[(sp, False)]["verdict"]
        cause = on in ("selection", "takeover") and off not in ("selection", "takeover")
        print(f"- {sp[12:]}: food on: {on}; food off: {off}; food is the cause: {'yes' if cause else 'no'}")


if __name__ == "__main__":
    main()
