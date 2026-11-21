"""Apply the decision rule in docs/FOOD-ON-EXACT-TRANSPORT-2026-11-10.md (verbatim from the food report).

Usage: python scripts/food_on_exact_summary.py [NEWDIR] [OLDDIR]
NEWDIR defaults to outputs/food_on_exact_20261110 (per_channel, food on);
OLDDIR to outputs/food_selection_20261109 (mean transport; only its food-on runs are used).
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from food_selection_summary import SPECIES, load, verdict  # noqa: E402


def main() -> None:
    new = load(Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "outputs/food_on_exact_20261110")
    old = load(Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "outputs/food_selection_20261109")
    new = {k: v for k, v in new.items() if k[1]}
    print(f"{len(new)} new-mode (per_channel) food-on runs\n")
    print("### Per run (per_channel, food on)\n")
    print("| species | arm | seed | A start | A end | delta | hybrid at end | body / total | blobs at end "
          "| largest blob | total drift | wall s |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for sp in SPECIES:
        for arm in ("treat", "neutral_plus", "neutral_minus"):
            for s in range(1, 6):
                r = new.get((sp, True, arm, s))
                if r is None:
                    continue
                f = r["final"]
                bt = f["body"] / (f["body"] + f["food"])
                print(f"| {sp[12:]} | {arm} | {s} | {r['share_A_start']:.3f} | {r['share_A_end']:.3f} "
                      f"| {r['delta_share_A']:+.4f} | {f['hybrid_frac']:.2f} | {bt:.2f} | {f['n_blobs']} "
                      f"| {f['largest_blob_frac']:.3f} | {r['max_rel_total_drift']:.1e} | {r['wall_seconds']:.0f} |")
    print("\n### Verdicts, new (per_channel) beside old (mean, 2026-11-09), food on\n")
    print("| species | mode | n neutral / treat | E | seeds outside E | winner | winner's final share "
          "| treat deltas (seeds 1-5) | verdict |")
    print("|---|---|---|---|---|---|---|---|---|")
    for sp in SPECIES:
        for name, runs in (("new per_channel", new), ("old mean", old)):
            if not any(k[0] == sp and k[1] for k in runs):
                continue
            v = verdict(runs, sp, True)
            d = ", ".join(f"{runs[(sp, True, 'treat', s)]['delta_share_A']:+.3f}"
                          for s in range(1, 6) if (sp, True, "treat", s) in runs)
            note = " (E < 1e-6)" if v["envelope"] < 1e-6 else ""
            print(f"| {sp[12:]} | {name} | {v['n_neutral']} / {v['n_treat']} | {v['envelope']:.4f}{note} "
                  f"| {v['out_of_envelope']} of {v['n_treat']} | {', '.join(v['winners']) or '-'} "
                  f"| {v['winner_final_shares'] or '-'} | {d} | {v['verdict']} |")
    print("\n### Conservation (new mode)\n")
    d = [r["max_rel_total_drift"] for r in new.values()]
    print(f"- max relative drift of sum(body)+sum(food) over all {len(d)} runs: {max(d):.2e}")
    for sp in SPECIES:
        d = [r["max_rel_total_drift"] for k, r in new.items() if k[0] == sp]
        if d:
            print(f"  - {sp[12:]}: {max(d):.2e}")


if __name__ == "__main__":
    main()
