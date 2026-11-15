# Conditional blending (ROADMAP step 2): does self/non-self contact repulsion keep lineages distinct, and does any lineage then win?

Status: **design fixed before the pilot and before the main runs.** The pilot results, a launch progress note and the results are appended below horizontal rules; this section is not edited afterwards.

Date: 2026-11-15 (UTC). Branch `vizier/conditional-blending-20261115`, based on `vizier/food-on-exact-transport-20261110`. Follows `docs/VARIANCE-DECAY-2026-11-03.md`, `docs/FOOD-SELECTION-2026-11-09.md`, `docs/GENOME-TRANSPORT-2026-11-10.md` and `docs/FOOD-ON-EXACT-TRANSPORT-2026-11-10.md`.

## Question

With exact genome transport and food on, no species shows selection (largest final share 0.662), and lineages still merge on contact: the end hybrid fraction (mass whose ancestry is between 0.1 and 0.9) is 0.30 to 1.00. The 2026-11-10 report named two obstacles: unconditional blending on contact, and a food-blind brain. This experiment removes the first. Two questions, in this order:

1. **Lineage distinctness (the step 2 question).** Does a contact repulsion between mass of different functional genome keep the two lineages apart, i.e. lower the end hybrid fraction?
2. **Selection.** If they stay apart, does one lineage now win under the unchanged decision rule?

## Mechanism

ROADMAP step 2 offers two routes. Only the **velocity route** is built here.

**Rejected: "keep the resident genome on contact".** Where arriving mass meets a dissimilar resident, overwriting the arriving genome with the resident's relabels matter. That is a heredity bias of exactly the kind `docs/GENOME-TRANSPORT-2026-11-10.md` removed (under `mean` transport it alone moved a lineage's share by 1.6 to 10 points), and it would make the neutral-tag share unreliable again, since matter would change lineage without anyone growing. It also breaks `sum(A_tot * G)` conservation, which `per_channel` transport guarantees. The velocity route changes only where mass goes; every unit of mass still carries the genome it had.

**Foreign-mass field.** Let `G8` be the 8-dimensional *functional* genome (the first `repulsion_genome_dims = 8` rows of the genome field; the ninth row is the neutral lineage tag appended last by `engine.nutrient.tagged` and is never read), `A_tot = sum_c A_c`, and `K` a unit-sum smooth ring kernel of radius `R` cells (the existing `build_kernel` with a single shell, so the same ring machinery as the perception bank; `R = 8`, fixed, not tuned). The first form considered was `F(x) = sum_y K(x-y) A_tot(y) |G8(x) - G8(y)|^2`. It reads the genome stored in `x` even where `x` is empty, and empty cells hold stale genome values (zero where the matter never reached), which would make `F` nonzero next to a blob in the neutral arms, where no genetic difference exists. The final formula replaces `G8(x)` by the neighbourhood's own mass-weighted mean genome `Gbar(x)`:

```
F(x)  = sum_y K(x-y) A_tot(y) |Gbar(x) - G8(y)|^2 ,   Gbar(x) = (K * (A_tot G8))(x) / (K * A_tot)(x)
      = (K*(A_tot |G8|^2))(x) - |(K*(A_tot G8))(x)|^2 / (K*A_tot)(x)
      = (K * A_tot)(x) * Var_K(G8)(x)          (mass-weighted genome variance over the neighbourhood)
```

`F` is the amount of mass in the neighbourhood of `x` times how unlike one another the genomes of that mass are. It is zero wherever the neighbourhood's mass shares one genome, and it is 0 (set explicitly) where `K * A_tot <= 1e-12`. In a two-lineage contact zone it is largest at the interface and zero deep inside either lineage. Implementation: three groups of FFT convolutions (`A_tot`, `A_tot |G8|^2`, `A_tot G8`), with `G8` first centred on its global mass-weighted mean (`F` is invariant to that shift; it removes cancellation), and the variance clipped at 0 against rounding. Code: `engine.neural_field.foreign_mass_field`. (This is a refinement of the starting definition, made on paper before any run; the starting form was never run.)

**Velocity term.** In `flow_field`, before the soft bound:

```
v_c  <-  gain_c R(theta_c) grad E_c  -  alpha grad A_tot  -  kappa grad F        (same term for every channel c)
```

`kappa = Config.repulsion_kappa`, default `0.0`. At `0.0` the branch is a Python-level `if` that is not traced, so the compiled step is the one that existed before and every earlier result reproduces (tested by state hash, below). The soft bound `max_step * tanh(|d| / max_step)` is applied after, unchanged, so displacements stay below `max_step`. `Config.repulsion_radius = 8.0` and `Config.repulsion_genome_dims = 8` are exposed, not tuned.

**What is untouched.** Only the velocity changes. `reintegrate` is unchanged, so mass is conserved by the partition of unity as before and `sum(A_tot * G)` (every genome row, tag included) is conserved by `per_channel` transport exactly as before; food uptake and decay are unchanged. Neutral arms: both blobs have the same `G8`, so `F` is zero up to rounding (about `1e-32` after centring) and the repulsion adds nothing; the neutral envelope still means "no genetic difference". This is a prediction about the neutral arms and is checked (rule 1, sanity check).

## Tests (`scripts/test_repulsion.py`)

- `quick` (single field evaluations, seconds): (1) two blobs differing only in the tag: `F` is bit-identical when the tag is replaced by noise, `F < 1e-10` for the state as spawned (the spawn operator's `1e-9` regulariser leaves `G8` slightly off its constant in cells holding about `1e-6` of mass) and `F < 1e-25` with `G8` exactly constant; (2) blobs differing in `G8`, in contact: `F > 1e-3` (the check can fail); (3) the velocity with and without the term differs by `< 1e-12` in the tag-only state.
- `full` (rolls the engine; **only on InstaBox machines**): (4) with `kappa = 0` the sha256 of `(A, G, F)` after 300 steps (food on, `per_channel`, three species) equals the hash computed by the pre-change `engine/` (the base commit, extracted with `git archive`); (5) conservation with repulsion on (`kappa = 3`, food off, 300 steps, three species): max drift of `sum(A_tot * G_row)` for every row including the tag, and of `sum(A)`, below `1e-12` of `M` (expected about `1e-16`, as in `scripts/test_transport.py`); (6) the term acts: with `kappa = 3` the trajectory differs from `kappa = 0`.

## Where the compute runs

No simulation of any kind runs on citadel (the host carries the Hermes gateway and bots and ran out of memory under a batch on 2026-11-08). Pilot, the `full` tests and the 45 main runs run on InstaBox machines (Pro workspace, 8 vCPU / 16 GiB, Debian 13, Python 3.13, CPU, float64). On citadel only editing, git, box control, file transfer, the summary script over JSON and the `quick` tests (single field evaluations) run. Software versions are recorded from the boxes and match the earlier batches if the resolver allows (jax 0.11.1, numpy 2.5.2, scipy 1.18.1). Each box runs 8 concurrent single-thread runs with `XLA_FLAGS="--xla_cpu_multi_thread_eigen=false intra_op_parallelism_threads=1"`.

## Pilot (calibrate `kappa` once, never change it)

- **Runs.** OSCILLIS and MITOSA, seed 1, arm `treat`, food on (same food parameters), `per_channel`, `advect_genome`, **10,000 steps**, sampled every 100, one run per candidate. Candidates, a geometric ladder of six: `kappa` in {0.1, 0.3, 1, 3, 10, 30} (12 runs). `repulsion_radius = 8` for all. The ladder is chosen from scale only: `F` is at most about 1 and its gradient at most a few tenths per cell, so `kappa grad F` is of order `0.03` to `10` cells per step across the ladder against `max_step = 0.85`; the top candidates are expected to saturate the bound.
- **Control values**, read from the existing 2026-11-10 series (`outputs/food_on_exact_20261110`, same species, seed 1, arm `treat`, step 10,000): hybrid fraction 0.857 (OSCILLIS) and 0.927 (MITOSA). Half of each is 0.43 and 0.46.
- **Pre-registered selection rule.** A candidate *qualifies* if, for BOTH species, (a) its end hybrid fraction at step 10,000 is at most half the control's at the same step; (b) the max relative drift of `sum(body) + sum(food)` over the run is at most `1e-12`; (c) velocity saturation is not caused by the term: the fraction of body velocities (channel-cell pairs with at least 0.05 of that channel) at the soft bound (`|d| >= 0.9 max_step`), averaged over the 100 samples, is at most 0.05 above the same fraction computed on the same states with the term removed (both recorded in the run). **Chosen `kappa` = the smallest candidate that qualifies.** If none does, the **largest** candidate is taken and this is said in the results; the main experiment runs either way.
- Every pilot run is listed in `outputs/conditional_blending_20261115/pilot/PILOT.md` (hybrid fraction, pure fraction, blob count, largest blob, drift, saturation with and without the term, wall time).
- Limits, stated now: one seed per candidate; the criterion is built on the outcome measure of question 1, so a distinct verdict in the main runs is partly by construction at the seed-1 pair and must be read through the other four seeds, which the pilot never saw; seed 1 treat is itself one of the 15 treatment runs of the main experiment (the pilot runs are 10,000 steps, the main runs 30,000, and the main runs are fresh runs, not the pilot's).

## Main experiment (45 runs)

Same design as `docs/FOOD-ON-EXACT-TRANSPORT-2026-11-10.md` with repulsion on at the chosen `kappa`: species OSCILLIS, MITOSA, VAGRANT; seeds 1 to 5; arms `treat` (A has `+u`, B has `-u`), `neutral_plus`, `neutral_minus`; food on with the same parameters (`k = 0.05`, `d = 5e-4`, `D = 0.1`, `theta = 0.3`, initial food uniform, total equal to the body mass); `per_channel`; `advect_genome = True`; 30,000 steps sampled every 100; same placements, lineage axis (seed 20261103) and tag. Jobs ordered seed by seed. `kappa` is recorded in each run's JSON. **The control is the existing 45 runs in `outputs/food_on_exact_20261110` (repulsion off); they are not rerun.** Same engine revision apart from the new term; hardware differs from the control (citadel, then InstaBox) so trajectories are paired by seed and placement but not bit for bit.

Sharding: the 45 jobs are split by remainder over up to four boxes (`awk (NR-1)%N==i`), each shard run by `scripts/run_batch.py` with its own log ending in `ALL_DONE`.

## Measures

Per run: A's share from the tag (`a = (1 + tag) / 2`, share `= sum(A_tot a) / sum(A_tot)`), `delta` = mean of the last 10% of samples minus the step-0 share; end hybrid fraction (mass with `0.1 < a < 0.9`, i.e. `|tag| < 0.8`); end pure fraction (mass with `|tag| > 0.8`; this equals `1 - hybrid` up to the boundary, reported because it was asked for); blob count; largest blob fraction; max relative drift of `sum(body) + sum(food)`; fraction of velocity cells at the soft bound with and without the term (as defined in the pilot); wall time.

## Decision rules (fixed before the runs)

**Rule 1: lineage distinctness.** Per species, take the five treatment runs' end hybrid fractions and the control's five (same seeds, `outputs/food_on_exact_20261110`).
- **Distinct** if the median hybrid fraction under repulsion is at most half the control's median AND at least 4 of 5 seeds are below their matched control seed.
- **No effect** if fewer than 3 of 5 seeds are below their matched control seed.
- **Partial** otherwise.

*Neutral-arm sanity check (prediction).* In the neutral arms `F` is zero up to rounding, so their hybrid fractions should match the control's neutral arms up to run-to-run variation. Report the per-seed differences (repulsion minus control, 10 neutral runs per species). The implementation is declared to **leak** (result void) if for any species the mean of the 10 paired differences differs from zero by more than 2 standard errors of those differences. The number of neutral runs whose final share equals the control's to `1e-12` is also reported.

**Rule 2: selection (verbatim from `docs/FOOD-SELECTION-2026-11-09.md`).** `delta` = A's share averaged over the last 10% of samples, minus A's share at step 0. Per species: neutral envelope `E` = largest `|delta|` among the 10 neutral runs; a treatment seed is out of the envelope if `|delta| > E`, its winner the genome whose lineage gained (`+u` if `delta > 0`); **selection** if at least 4 of 5 treatment seeds are out of the envelope and agree on the winner; **takeover** if selection and the winner's final share is at least 0.90 in those seeds; **large but inconsistent** if at least 4 are out but the winners disagree; **no selection detected** otherwise. `E`'s size is reported per species, next to the food-on exact control.

**Rule 3: conservation.** `sum(body) + sum(food)` max relative drift per run, expected about `1e-15`.

## Prediction

Three outcomes are possible and I do not know which will occur:

1. **Repulsion keeps lineages distinct and one wins** (rule 1 distinct, rule 2 selection or takeover for some species). Then unconditional blending was the obstacle.
2. **Repulsion keeps lineages distinct and nobody wins** (rule 1 distinct, rule 2 no selection detected). Then the remaining obstacle is the food-blind brain.
3. **Repulsion does not keep them distinct at the calibrated `kappa`** (rule 1 no effect or partial). Then either the pilot's single-seed calibration did not transfer, or a velocity term cannot hold lineages apart against transport and the tail spreading that bilinear reintegration leaves everywhere.

My expectation, a guess and not a measurement: outcome 2 at least for OSCILLIS and MITOSA (the functional genome does not change anything food rewards; the brain cannot see food), with a real chance of outcome 3 for VAGRANT (its control hybrid fraction is already the lowest, median 0.50, so "half of the control" is the hardest bar there). Outcomes can mix across species.

Known limits, stated now: 5 seeds per species; the envelope is set by 10 runs; the radius is fixed at 8 and only `kappa` is calibrated; hybrid fraction is a threshold measure (`0.1 < a < 0.9`) and a thin interface of mixed mass counts as hybrid however narrow; `F` uses the 8 functional dimensions with equal weights, so genomes that differ in dimensions the brain barely reads repel as strongly as ones that differ in dimensions it reads strongly.

---

## Pilot results and tests (appended 2026-11-15, before the main runs)

Compute: all on InstaBox, box `flux-lenia-step2-w1` (`m_agq6dc6cqnfwkrte3cd4jrpyb4`, 8 vCPU / 16 GiB, Debian 13, Python 3.13.5, jax 0.11.1, numpy 2.5.2, scipy 1.18.1, CPU, float64). Nothing heavy ran on citadel; there only the `quick` test (single field evaluations) ran.

**Tests.** `quick` passed on citadel and on the box: tag-only state `F` is bit-identical when the tag is replaced by noise, max `F` 2.5e-18 as spawned and 5.3e-46 with `G8` exactly constant, max velocity difference with and without the term 1.4e-17; treatment state in contact has max `F` = 0.697. `full` passed on the box (300 steps, three species; log `outputs/conditional_blending_20261115/logs/test_repulsion_full_w1.log`): with `kappa = 0` the state hash equals the hash from the pre-change engine (base commit `b2cdd8b`) for OSCILLIS, MITOSA and VAGRANT; with `kappa = 3`, food off, `max |dS_tag| / M` is 1.2e-16, 6.9e-17, 1.1e-16, the functional rows 4.0e-17, 6.2e-17, 6.9e-17, and `|dM| / M` 2.5e-16 in all three; the repulsion changes the trajectory (max `|A(kappa) - A(0)|` 1.19, 9.7e-5, 1.9e-4).

**Pilot** (12 runs, seed 1, treat, food on, 10,000 steps; per-run table `outputs/conditional_blending_20261115/pilot/PILOT.md`). Control hybrid fraction at step 10,000: OSCILLIS 0.857, MITOSA 0.927. End hybrid fraction by candidate:

| kappa | OSCILLIS hybrid | MITOSA hybrid | both at most half the control |
|---|---|---|---|
| 0.1 | 0.831 | 0.899 | no |
| 0.3 | 0.835 | 0.943 | no |
| 1 | 0.826 | 0.312 | no (OSCILLIS) |
| 3 | 0.139 | 0.002 | yes |
| 10 | 0.000 | 0.000 | yes |
| 30 | 0.000 | 0.000 | yes |

Every candidate had total drift of `sum(body) + sum(food)` at most 8.6e-16 and no velocity saturation attributable to the term (largest single-sample fraction at the bound 4.0e-4, kappa 30). **Chosen `kappa = 3`** (the smallest qualifying candidate). `kappa` is not changed after this point.
