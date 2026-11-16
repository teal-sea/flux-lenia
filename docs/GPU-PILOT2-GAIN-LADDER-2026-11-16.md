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
