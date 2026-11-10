# Food on, exact genome transport: does food give a lineage a consistent win once the heredity bias is gone?

Status: **design fixed before the main runs.** A progress note and the results are appended below horizontal rules; this section is not edited afterwards.

Date: 2026-11-10 (UTC). Branch `vizier/food-on-exact-transport-20261110`, based on `vizier/genome-transport-conservation-20261110`. Follows `docs/FOOD-SELECTION-2026-11-09.md` (food model, neutral tag, decision rule) and `docs/GENOME-TRANSPORT-2026-11-10.md` (the `per_channel` transport, under which the no-food share shift vanished: treatment |delta| <= 3.4e-15).

## Question

The 2026-11-09 food-on runs used `genome_transport = "mean"`, which has a heredity bias: with no food it alone moved lineage A's share by 1.6 to 10 points, consistently in one direction per species. Food-on verdicts were OSCILLIS selection (+u), MITOSA and VAGRANT no selection detected. Those verdicts were measured with that bias present. With exact per-channel transport, does food now give any lineage a consistent win by the same decision rule?

## What differs from 2026-11-09

Only the transport mode: `genome_transport = "per_channel"` instead of `"mean"`. Everything else is the same: species, seeds, arms, spawn placement, lineage axis `u` (seed 20261103), neutral tag, `advect_genome = True`, food parameters (`k = 0.05`, `d = 5e-4`, `D = 0.1`, `theta = 0.3`, initial food uniform and equal in total to the initial body mass), 30,000 steps, sampled every 100, `scripts/food_selection.py` unchanged (its optional transport argument exists already). Also the same code revision of `engine/` as the transport experiment. Hardware differs (citadel instead of InstaBox) and trajectories under the two modes diverge, so old and new runs are not paired one to one.

## Design

- Species OSCILLIS, MITOSA, VAGRANT (`outputs/species/`); seeds 1 to 5; arms `treat` (A has `+u`, B has `-u`), `neutral_plus` (both `+u`), `neutral_minus` (both `-u`). Food on. 3 x 5 x 3 = 45 runs.
- citadel (16 cores, 31 GiB), 8 concurrent single-thread runs, `nice -n 10`, `XLA_FLAGS="--xla_cpu_multi_thread_eigen=false intra_op_parallelism_threads=1"`; Python 3.13.5, jax 0.11.1, numpy 2.5.2, scipy 1.18.1, float64 CPU. Jobs are ordered seed by seed.
- Guards: no new launches while available memory < 6 GiB; concurrency drops to 6 if any run's RSS > 2.5 GiB. If projected wall time exceeds 7 hours, cut to seeds 1 to 3 per species and say so.

## Measures

- A's share from the neutral tag: per cell `a = (1 + tag) / 2`, share = `sum(A_tot a) / sum(A_tot)` over body. `delta` = mean of the last 10% of samples minus the step-0 share. Also the hybrid fraction (mass with ancestry between 0.1 and 0.9) and blob count at the end, and per-run wall time.
- Conservation, stated before the runs:
  - **Expected conserved**: `sum(body) + sum(food)`, to float rounding (about 1e-15 relative, as in the 2026-11-09 runs). Reported as max relative drift over the samples of each run.
  - **Not expected conserved**: `sum(A_tot * tag)` (and `sum(A_tot * G)`). Under `per_channel` transport alone it is conserved to rounding (shown with food off, 1.2e-16 of M). With food, uptake adds mass to a cell that keeps the genome already there and decay removes mass at the cell's genome, so the tag-weighted sum changes by `sum((U - d A_tot) tag)` each step, legitimately: this is growth of a lineage. What is expected is that transport adds no change of its own, and that the tag stays within [-1, 1] (it is a mass-weighted average of values in [-1, 1]); frames record the ancestry field, so the range is checked there. The series records `share_A`, the tag-weighted sum divided by total body, so a change in `share_A` with food has two legitimate sources, differential growth and neutral position effects, and the neutral arms are what separate them from genetics.
- Envelope size is reported per species. If E is below 1e-6 of the share for any species, that is stated next to its verdict.

## Prediction

Three outcomes are possible and I do not know which will occur:

1. **A consistent winner now appears where none was before** (MITOSA or VAGRANT, food on). Then removing the bias unmasks a food-mediated genome effect that the bias was hiding or cancelling.
2. **The old OSCILLIS +u "selection" disappears.** Then it was the transport bias (OSCILLIS had the largest no-food shift, +6.5 to +10 points, and the food-on shift was of the same size).
3. **Nothing changes**: the same verdict per species as 2026-11-09.

My expectation, from the no-food bias being the only consistent effect found before, is outcome 2 for OSCILLIS and no selection for MITOSA and VAGRANT; this is a guess, not a measurement. Outcomes can mix across species.

## Decision rule (verbatim from `docs/FOOD-SELECTION-2026-11-09.md`)

`delta` = A's share averaged over the last 10% of samples, minus A's share at step 0.

For each species:

- Neutral envelope `E` = the largest `|delta|` among its 10 neutral runs (5 seeds x 2 neutral arms).
- A treatment seed is **out of the envelope** if its `|delta| > E`. Its winner is the genome whose lineage gained (`+u` if `delta > 0`).
- **Selection**: at least 4 of the 5 treatment seeds are out of the envelope, and all of those agree on the winner.
- **Takeover**: selection, and the winner's final share is at least 0.90 in those seeds.
- **Large but inconsistent**: at least 4 out of the envelope, but the winners disagree.
- **No selection detected**: otherwise.

Known limits, stated now: 5 seeds per species; the envelope is set by 10 runs; with food on, neutral drift is real, so E is meaningful again; blind foraging means selection can act only through movement and shape.
