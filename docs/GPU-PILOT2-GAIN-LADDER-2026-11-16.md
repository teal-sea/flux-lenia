# Pilot 2: food_sense gain ladder, upward, on GPU (2026-11-16)

Written before the runs. Launched from citadel as Modal A100 containers (gpu/modal_campaign.py,
manifest gpu/pilot2_gain_ladder.json); nothing heavy runs on citadel.

## Why

B's pilot (branch vizier/food-sensing-brain-20261116, commit eb36b7a, PILOT.md) tested food_sense in
{0.1, 0.3, 1, 3, 10} on seed 1 of each species at 10,000 steps and found that none changed foraging in
at least 2 of 3 species by the pre-registered rule; 10 was chosen by the fallback clause. The 2x2 at
food_sense 10 is running (InstaBox, B; Modal, Vizier). If 10 does nothing, the open question is whether
any non-saturating gain does. This pilot extends the ladder upward with 64 seeds per gain so the
foraging change is measured against a seed distribution, not one seed.

## Design

Gains: 30, 100, 300, 1000. Species: OSCILLIS, MITOSA, VAGRANT. Seeds 1-64, arm treat, food on,
per_channel, kappa 3, 10,000 steps, sampled every 100. 12 batches of 64 runs, one A100 container each.
Reference food_sense = 0: the fs0, kappa 3 cells of the 2x2 (seeds 1-50, read at step 10,000).

## Rule, fixed before the runs (B's rule, applied per gain with distributions)

Q = body(10,000) - body(0) per run (food consumed into body). For a gain g and species s:
- `changes foraging` if |median Q(g) - median Q(0)| > R(0), where R(0) = max - min of Q(0) over the
  reference seeds (B's spread statistic), AND the two distributions' interquartile ranges do not overlap.
- `clean` if the velocity saturation fraction stays below 1e-2 in every sample of every run and the
  relative drift of sum(body)+sum(food) stays below 1e-12.
- A gain `qualifies` if it changes foraging in at least 2 of 3 species and is clean in all 3.
- Recommendation = the smallest qualifying gain. If none qualifies: if the failures are saturation,
  the brain route to food sensing is capped by the soft velocity bound and the next design is a
  normalised food input; if the failures are "no change", the shared brain's random food weights do
  not couple to movement in these species and the next design is a food-coupled hunt gate.

## Predictions

(i) a gain in 30..300 qualifies (then the 2x2 is rerun at that gain); (ii) every gain that changes
foraging also saturates (route capped); (iii) nothing changes foraging at any gain (no coupling).

## Cost, stated before launch

12 containers x about 10,000 steps x ~20 ms per batched step = ~200 s each plus start-up; about
$1.70 at $2.50 per A100-hour. Containers queue behind the running 2x2 (workspace concurrency ~9).

---

## Results (appended 2026-11-16 04:30 UTC)

All 12 batches finished on Modal A100-80GB containers (launched 03:33 UTC, last done ~03:58 UTC),
768 runs, 64 per (species, gain), no failures. Per-run JSON in `outputs/pilot2_gain_ladder/`, verdict
table from `scripts/pilot2_gain_ladder_summary.py` in `outputs/pilot2_gain_ladder/SUMMARY.md`.
Reference Q(0): the fs0, kappa 3 treat runs of the GPU 2x2 (`outputs/food_sensing_2x2_gpu/`,
seeds 1-50, read at step 10,000), as pre-registered.

**No gain qualifies: nothing changes foraging at any gain, in any species (prediction iii).**

| species | median Q(0), IQR, R(0) | median Q at gain 30 / 100 / 300 / 1000 |
|---|---|---|
| OSCILLIS | 1469, [1344, 1633], 894 | 1375 / 1362 / 1273 / 1114 |
| MITOSA | 1428, [1337, 1623], 976 | 1210 / 1111 / 1076 / 1137 |
| VAGRANT | 1402, [1213, 1589], 1026 | 1334 / 1177 / 1315 / 1399 |

Every gain's IQR overlaps the reference IQR and every median shift is inside R(0). All gains are
clean: the largest single-sample saturation fraction was 5.45e-4 (VAGRANT, gain 1000), drift at
most 7.5e-15. The medians drift down with gain in OSCILLIS and MITOSA (food input perturbs the
hidden layer and the organisms forage slightly worse), which is a change in the wrong direction
and still inside the spread.

**Reading, with the 2x2 beside it.** By this rule the food input through the shared brain does not
make a lineage forage more at the population level, at any non-saturating gain. The GPU 2x2 at
gain 10 (`docs/FOOD-SENSING-2x2-GPU-2026-11-16.md`) nevertheless shows selection in OSCILLIS at
kappa 3 (40 of 50 treatment seeds outside the neutral envelope, all for +u). The two are
compatible: selection by the share rule needs a consistent small difference between the two
lineages' responses, not a measurable change in total food eaten. The pilot rule measures the
latter and therefore cannot be the gate for the former. Deviation from the doc's "next design"
clause: the clause assumed no change in foraging implied no coupling to movement; the 2x2 shows
coupling to the lineage share without a foraging change, so the hunt-gate redesign is not the
next step. The next step is replication of the OSCILLIS result on the CPU 2x2 (worker B) and the
species scan at gain 10.

Cost: 12 containers, 4,115 container-seconds, $3.58 at the corrected $3.13 per container-hour
(A100 + 8 cores + 32 GiB), against the $1.70 estimate: fs > 0 steps cost about 2x (food features
through the ring bank) and OSCILLIS/VAGRANT run about 2x slower than MITOSA.
