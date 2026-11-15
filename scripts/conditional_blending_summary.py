"""Apply the pilot rule and decision rules of docs/CONDITIONAL-BLENDING-2026-11-15.md to run JSON.

Usage:
  python scripts/conditional_blending_summary.py pilot [PILOTDIR] [CONTROLDIR]
  python scripts/conditional_blending_summary.py main  [NEWDIR]   [CONTROLDIR]
PILOTDIR defaults to outputs/conditional_blending_20261115/pilot (subdirs k<kappa>/), NEWDIR to
outputs/conditional_blending_20261115, CONTROLDIR to outputs/food_on_exact_20261110 (repulsion off).
Runs only over JSON; no simulation.
"""

from __future__ import annotations

import json
import math
import statistics as st
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from food_selection_summary import SPECIES, load, verdict  # noqa: E402

PILOT_SPECIES = SPECIES[:2]
PILOT_STEP = 10000
DRIFT_MAX = 1e-12
SAT_EXCESS_MAX = 0.05
ARMS = ("treat", "neutral_plus", "neutral_minus")


def idx(r: dict, step: int) -> int:
    return r["t"].index(step)


def pilot(pdir: Path, cdir: Path) -> None:
    ctrl = load(cdir)
    runs = {}
    for f in sorted(pdir.glob("k*/SPECIES_*_food1.json")):
        r = json.loads(f.read_text())
        runs[(r["repulsion_kappa"], r["species"])] = r
    kappas = sorted({k for k, _ in runs})
    ch = {sp: ctrl[(sp, True, "treat", 1)]["series"]["hybrid_frac"][idx(ctrl[(sp, True, "treat", 1)], PILOT_STEP)]
          for sp in PILOT_SPECIES}
    print("## Pilot runs (seed 1, treat, food on, per_channel, 10,000 steps)\n")
    print("Control (repulsion off, 2026-11-10) hybrid fraction at step 10,000: "
          + ", ".join(f"{sp[12:]} {ch[sp]:.3f} (half {ch[sp] / 2:.3f})" for sp in PILOT_SPECIES) + "\n")
    print("| kappa | species | hybrid | pure | blobs | largest blob | max drift | sat with (mean over samples) "
          "| sat without | excess | wall s | hybrid <= half control | drift ok | sat ok |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    qual = {}
    for k in kappas:
        ok_all = True
        for sp in PILOT_SPECIES:
            r = runs.get((k, sp))
            if r is None:
                print(f"| {k:g} | {sp[12:]} | missing |" + " |" * 12)
                ok_all = False
                continue
            i = idx(r, PILOT_STEP)
            s = r["series"]
            sw = st.mean(s["sat_frac"][1:i + 1]); so = st.mean(s["sat_frac_without_repulsion"][1:i + 1])
            a = s["hybrid_frac"][i] <= ch[sp] / 2
            b = max(abs(x - (s["body"][0] + s["food"][0])) / (s["body"][0] + s["food"][0])
                    for x in [bb + ff for bb, ff in zip(s["body"][:i + 1], s["food"][:i + 1])]) <= DRIFT_MAX
            c = sw - so <= SAT_EXCESS_MAX
            ok_all &= a and b and c
            print(f"| {k:g} | {sp[12:]} | {s['hybrid_frac'][i]:.3f} | {s['pure_frac'][i]:.3f} | {s['n_blobs'][i]} "
                  f"| {s['largest_blob_frac'][i]:.3f} | {r['max_rel_total_drift']:.1e} | {sw:.4f} | {so:.4f} "
                  f"| {sw - so:+.4f} | {r['wall_seconds']:.0f} | {'yes' if a else 'no'} | {'yes' if b else 'no'} "
                  f"| {'yes' if c else 'no'} |")
        qual[k] = ok_all
    q = [k for k in kappas if qual[k]]
    if q:
        print(f"\n**Chosen kappa = {min(q):g}** (smallest candidate that qualifies for both species; qualifying: "
              + ", ".join(f"{k:g}" for k in q) + ").")
    else:
        print(f"\n**No candidate qualifies; the largest candidate, kappa = {max(kappas):g}, is taken** (pre-registered fallback).")


def main_summary(ndir: Path, cdir: Path) -> None:
    new = {k: v for k, v in load(ndir).items() if k[1]}
    ctrl = {k: v for k, v in load(cdir).items() if k[1]}
    kap = sorted({r["repulsion_kappa"] for r in new.values()})
    print(f"{len(new)} repulsion-on food-on runs, kappa = {kap}; control {len(ctrl)} runs from {cdir.name}\n")
    print("### Per run (repulsion on)\n")
    print("| species | arm | seed | A start | A end | delta | hybrid end | control hybrid | pure end | blobs | largest blob "
          "| sat end | sat end w/o term | total drift | wall s |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for sp in SPECIES:
        for arm in ARMS:
            for s in range(1, 6):
                r, c = new.get((sp, True, arm, s)), ctrl.get((sp, True, arm, s))
                if r is None or c is None:
                    print(f"| {sp[12:]} | {arm} | {s} | missing |" + " |" * 11)
                    continue
                f = r["final"]
                print(f"| {sp[12:]} | {arm} | {s} | {r['share_A_start']:.3f} | {r['share_A_end']:.3f} "
                      f"| {r['delta_share_A']:+.4f} | {f['hybrid_frac']:.3f} "
                      f"| {c['final']['hybrid_frac']:.3f} | {f['pure_frac']:.3f} | {f['n_blobs']} "
                      f"| {f['largest_blob_frac']:.3f} | {f.get('sat_frac', float('nan')):.4f} "
                      f"| {f.get('sat_frac_without_repulsion', float('nan')):.4f} "
                      f"| {r['max_rel_total_drift']:.1e} | {r['wall_seconds']:.0f} |")

    print("\n### Step 2 verdict (rule 1: lineage distinctness, treatment arm)\n")
    print("| species | control median hybrid | repulsion median hybrid | ratio | seeds below control (of 5) "
          "| per-seed hybrid (repulsion / control) | verdict |")
    print("|---|---|---|---|---|---|---|")
    for sp in SPECIES:
        seeds = [s for s in range(1, 6) if (sp, True, "treat", s) in new and (sp, True, "treat", s) in ctrl]
        h = [new[(sp, True, "treat", s)]["final"]["hybrid_frac"] for s in seeds]
        c = [ctrl[(sp, True, "treat", s)]["final"]["hybrid_frac"] for s in seeds]
        mh, mc = st.median(h), st.median(c)
        below = sum(a < b for a, b in zip(h, c))
        if mh <= mc / 2 and below >= 4:
            v = "distinct"
        elif below < 3:
            v = "no effect"
        else:
            v = "partial"
        per = ", ".join(f"{a:.2f}/{b:.2f}" for a, b in zip(h, c))
        print(f"| {sp[12:]} | {mc:.3f} | {mh:.3f} | {mh / mc:.2f} | {below} of {len(seeds)} | {per} | {v} |")

    print("\n### Neutral-arm sanity check (repulsion minus control, hybrid fraction at the end)\n")
    print("| species | n pairs | mean diff | SE | mean/SE | max abs diff | final share equal to control (1e-12) | flag |")
    print("|---|---|---|---|---|---|---|---|")
    for sp in SPECIES:
        d, same = [], 0
        for arm in ("neutral_plus", "neutral_minus"):
            for s in range(1, 6):
                r, c = new.get((sp, True, arm, s)), ctrl.get((sp, True, arm, s))
                if r and c:
                    d.append(r["final"]["hybrid_frac"] - c["final"]["hybrid_frac"])
                    same += abs(r["share_A_end"] - c["share_A_end"]) < 1e-12
        if len(d) < 2:
            print(f"| {sp[12:]} | {len(d)} | | | | | | |")
            continue
        m, se = st.mean(d), st.stdev(d) / math.sqrt(len(d))
        z = m / se if se > 0 else (0.0 if m == 0 else float("inf"))
        print(f"| {sp[12:]} | {len(d)} | {m:+.4f} | {se:.4f} | {z:+.2f} | {max(abs(x) for x in d):.4f} "
              f"| {same} of {len(d)} | {'LEAK (|mean| > 2 SE)' if abs(z) > 2 else 'ok'} |")
    print("\nPer-seed differences, neutral_plus then neutral_minus, seeds 1 to 5:\n")
    for sp in SPECIES:
        for arm in ("neutral_plus", "neutral_minus"):
            row = [(new[(sp, True, arm, s)]["final"]["hybrid_frac"] - ctrl[(sp, True, arm, s)]["final"]["hybrid_frac"])
                   for s in range(1, 6) if (sp, True, arm, s) in new and (sp, True, arm, s) in ctrl]
            print(f"- {sp[12:]} {arm}: " + ", ".join(f"{x:+.4f}" for x in row))

    print("\n### Selection (rule 2), repulsion on beside the food-on exact control\n")
    print("| species | run set | E | treatment seeds outside E | winner | winner's final share | treat deltas (seeds 1-5) | verdict |")
    print("|---|---|---|---|---|---|---|---|")
    for sp in SPECIES:
        for name, runs in ((f"repulsion kappa={kap[0]:g} (this run)" if kap else "repulsion", new),
                           ("control, repulsion off (2026-11-10)", ctrl)):
            if not any(k[0] == sp for k in runs):
                continue
            v = verdict(runs, sp, True)
            dl = ", ".join(f"{runs[(sp, True, 'treat', s)]['delta_share_A']:+.3f}" for s in range(1, 6)
                           if (sp, True, "treat", s) in runs)
            print(f"| {sp[12:]} | {name} | {v['envelope']:.4f} | {v['out_of_envelope']} of {v['n_treat']} "
                  f"| {', '.join(v['winners']) or '-'} | {v['winner_final_shares'] or '-'} | {dl} | {v['verdict']} |")
    big = max((r["final"]["share_A"] if r["delta_share_A"] > 0 else 1 - r["final"]["share_A"], k)
              for k, r in new.items() if k[2] == "treat")
    print(f"\nLargest winner-side final share in a treatment run: {big[0]:.3f} ({big[1][0][12:]}, seed {big[1][3]}).")

    print("\n### Conservation (rule 3) and velocity bound\n")
    d = [r["max_rel_total_drift"] for r in new.values()]
    print(f"- max relative drift of sum(body)+sum(food), all {len(d)} runs: {max(d):.2e}")
    for sp in SPECIES:
        dd = [r["max_rel_total_drift"] for k, r in new.items() if k[0] == sp]
        if dd:
            print(f"  - {sp[12:]}: {max(dd):.2e}")
    for sp in SPECIES:
        ss = [(st.mean(r["series"]["sat_frac"][1:]), st.mean(r["series"]["sat_frac_without_repulsion"][1:]))
              for k, r in new.items() if k[0] == sp and k[2] == "treat" and "sat_frac" in r["series"]]
        if ss:
            print(f"- {sp[12:]} treat: mean fraction of body velocities at the soft bound, with term "
                  f"{st.mean(a for a, _ in ss):.4f}, same states without it {st.mean(b for _, b in ss):.4f}")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "main"
    cd = Path(sys.argv[3]) if len(sys.argv) > 3 else ROOT / "outputs/food_on_exact_20261110"
    if mode == "pilot":
        pilot(Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "outputs/conditional_blending_20261115/pilot", cd)
    else:
        main_summary(Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "outputs/conditional_blending_20261115", cd)
