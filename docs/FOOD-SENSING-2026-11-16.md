# Food sensing (campaign B): does selection appear when, and only when, the genome can touch the resource?

Status: **design fixed before the pilot and before the main runs.** The pilot results, a launch progress note and the results are appended below horizontal rules; this section is not edited afterwards.

Date: 2026-11-16 (UTC). Branch `vizier/food-sensing-brain-20261116`, based on `vizier/conditional-blending-20261115` @ `ce00383`. Follows `docs/VARIANCE-DECAY-2026-11-03.md`, `docs/FOOD-SELECTION-2026-11-09.md`, `docs/GENOME-TRANSPORT-2026-11-10.md`, `docs/FOOD-ON-EXACT-TRANSPORT-2026-11-10.md` and `docs/CONDITIONAL-BLENDING-2026-11-15.md`.

## Question

Four experiments on this engine found no selection once the heredity bias was removed (exact transport) and, with contact repulsion `kappa = 3` (2026-11-15), the two lineages stay distinct in all three species and still nobody wins (largest winner-side final share 0.703; OSCILLIS large but inconsistent, VAGRANT 3 of 5 seeds `+u`). The reports name the remaining obstacle: **the brain is food-blind.** `perceive` sees only the body field `A` (and light); food `F` enters only through `react` (growth where food is). A genome can change movement and shape but cannot change the *response to food*, and the genome changes nothing that food rewards.

This experiment removes that obstacle and asks, with the conserved budget and no fitness function anywhere (ROADMAP step 0):

1. **Cause (the factorial question).** When the genome can touch the resource (the brain senses food), does one lineage win consistently, and does it fail to win when the same dish is run with the brain food-blind?
2. **Repulsion as a condition.** If selection appears, does it need lineages to stay apart (`kappa = 3`)?
3. **Distinctness at scale.** Does the step 2 result (repulsion keeps lineages apart) replicate with 50 seeds instead of 5, with and without food sensing?

What consumes the result: the owner's Dish project reads this as its measurement #4, *is movement a heritable problem-selection policy*. A null is a result, not a failure.

## Mechanism (food perception as brain input)

Stays inside the architecture genome -> brain -> behaviour. There is no chemotaxis term: food enters the shared brain's first layer through the same ring bank and bell machinery as the body, and the genome acts on it through the FiLM modulation it already has.

Notation as in `engine/neural_field.py`: bank `(khat_k, src_k)`, `k = 1..K`, `K = 16`; bell parameters `m_k, s_k`; hidden width `H = 24`; body features `X = [U_1..U_K, B_1..B_K, A_1..A_C, light]` (`F_body = 2K + C + 1 = 36`); `bell_k(u) = 2 exp(-0.5 ((u - m_k) / (|s_k| + 1e-3))^2) - 1`.

```
Uf_k(x)  = (ring_k * F)(x)                       k = 1..K      (perceive(F[None], khat, zeros) : every kernel reads the one food field)
Bf_k(x)  = bell_k(Uf_k(x)) - bell_k(0)                          (offset: exactly 0 where there is no food)
Xf       = [Uf_1..Uf_K, Bf_1..Bf_K]                              n_food_features = 2K = 32

pre(x)   = W1^T X(x) + b1  +  food_sense * W1f^T Xf(x)           (old pre-activation + the new block)
gamma(x) = 1 + Wg1^T G(x),   beta(x) = Wg2^T G(x)                (unchanged: FiLM from the local genome field)
h(x)     = tanh(pre(x) * gamma(x) + beta(x))                     (unchanged; gamma and beta now modulate the food term as well)
```

then `E, gain, theta = W2 h + b2` and the flow, transport, uptake and decay are unchanged. `W1f` (32 x 24, in the brain parameter dict as `"W1f"`) is drawn once per species: `W1f ~ N(0, 1/32)` i.i.d., from `numpy.random.default_rng(seed)` with `seed = crc32("W1f|<species id>")` (OSCILLIS 610146212, MITOSA 2535044062, VAGRANT 1543556059). It is identical across arms, seeds, kappa and `food_sense` within a species, so lineages differ only by genome. `Config.food_sense` (float, default `0.0`) scales the block; at `0.0` the branch is a Python-level `if` that is not traced, so the compiled step is the pre-change one and every earlier result reproduces (tested by state hash, below).

Why this is food perception and not a hand-wired policy: the brain's response to food is `W1f` (random, shared, not tuned), read through the bell nonlinearity, then through `tanh`, then `W2`. The genome decides the response through `gamma` and `beta`. Whether a lineage's response to food is *helpful* is not specified anywhere; it is whatever the random `W1f`, `W2` and the genome axis happen to give. That is the point (prediction ii below).

The perception function: the existing `perceive` is reused unchanged (`perceive(F[None], khat, zeros_like(ksrc))`); the new function `food_features` wraps it with the bell and the offset, and does not touch the body's path (`perceive` for `A`, `sensorimotor`'s `X`, and the repulsion term are the same code as before). `sensorimotor` gained the optional arguments `Ff=None, return_hidden=False`; `engine.nutrient.step` passes `Ff` only when `food_sense != 0`.

**The tag never enters.** The lineage tag is the last genome row; `engine.nutrient.tagged` gives it zero rows in `Wg1` and `Wg2`. `Xf` is a function of `F`, the bank and the bell parameters only, and `W1f` has no genome rows. So the tag reaches the brain nowhere.

**Mass conservation is untouched.** Only the velocity changes. `reintegrate`, `react`, and `diffuse` are unchanged, so `sum(body) + sum(food)` is conserved by `react`/`diffuse` as before, and `sum(A_tot * G)` is conserved by `per_channel` transport as before (both asserted with `food_sense` on).

**Food logging** (new, not used by dynamics): `engine.nutrient.rollout_logged` returns, with the state, the sum of food eaten (`gain`) and body decayed (`loss`) over the chunk; `react_stats` is `react` plus those two scalars (`react` calls it). The cumulative sums are recorded every 100 steps (`food_eaten_cum`, `body_decayed_cum`).

CLI (backward compatible): `scripts/food_selection.py SPECIES SEED ARM FOOD STEPS OUTDIR [TRANSPORT [KAPPA [FOOD_SENSE]]]`; `scripts/run_batch.py` job lines may carry a 7th field `FOOD_SENSE` (`-` as the 6th field means no subdirectory). When the `FOOD_SENSE` argument is present (even as `0`) the run logs the food measures, `sat_frac` at every sample, `food_sense` and the `W1f` seed, and saves **three float32 frames** (steps 0, 15,000, 30,000) instead of five float64 ones. Without it, behaviour is as before.

## Tests (`scripts/test_food_sense.py`)

- `quick` (single field evaluations, seconds): (1) `food_features` has shape `(32, 128, 128)`, is exactly 0 for `F = 0`, and responds to the food field; (2) **tag unreadable**: with `food_sense = 3` and a non-uniform food field, replacing the tag by noise, or flipping it, gives bit-identical hidden activations `h` and bit-identical velocities; positive controls: changing a functional genome row, or the food field, changes `h`; (3) **the genome shapes the response to food**: the food-induced change of `h` (food on minus food off, same state) differs between a uniform genome `+u` and `-u`; (4) `food_sense = 0` ignores `Ff` and does not need `W1f` (bit-identical).
- `full` (rolls the engine; **only on InstaBox machines**), 300 steps, three species: (5) **no-op**: with `food_sense = 0` the sha256 of `(A, G, F)` (food on, `per_channel`) equals the hash from the pre-change engine (base commit `ce00383`, extracted with `git archive`) for `kappa = 0` and `kappa = 3`, and equals the hash through `rollout_logged` with `food_sense = 0.0` passed explicitly; (6) conservation with `food_sense = 3` on: (a) max relative drift of `sum(A) + sum(F)` over the full food step below `1e-12`; (b) transport alone under a prescribed fixed food field: max `|d sum(A_tot G_row)| / M` for every genome row (tag included) and `|dM|/M` below `1e-12`; (c) the food logger: `|(body gain) - (eaten - decayed)| / M` below `1e-12`; (7) the term acts: max `|A(on) - A(off)| > 1e-6`; (8) the tag stays unread over the rollout: `A` after 300 steps with the tag sign flipped is bit-identical.

## Where the compute runs

No simulation of any kind runs on citadel (it carries the Hermes gateway and bots and ran out of memory under a batch on 2026-11-08; the owner ordered that heavy compute never run there again). Pilot, `full` tests and all 1,800 main runs run on InstaBox machines (Pro workspace; 8 vCPU / 16 GiB, Debian 13, Python 3.13, CPU, float64). On citadel only editing, git, box control, file transfer, the `quick` test (single field evaluations) and summary scripts over JSON run. Software versions are recorded from the boxes (previous batches: Python 3.13.5, jax 0.11.1, numpy 2.5.2, scipy 1.18.1). Each box runs 8 concurrent single-thread runs with `XLA_FLAGS="--xla_cpu_multi_thread_eigen=false intra_op_parallelism_threads=1"`. One box (`flux-lenia-campB-w1`) is built, tested and used for the pilot; it is then forked to at most 40 boxes in total.

**Cost estimate (stated before launch).** The brief's reference rate is about $0.07 per 8/16 box-hour (the InstaBox skill's $0.034/h for 4/8, doubled); the 2026-11-15 doc used $0.136/h, which would be four times the 4/8 rate. Expected wall time: 1,800 runs / (40 boxes x 8 concurrent) = 5.6 waves of 30,000 steps, about 836 s each in the earlier batches (sensing-on runs cost one extra FFT bank per step, so somewhat more): about 1.5 to 2 h on 40 boxes, 60 to 80 box-hours plus about 1 h on the proof box: **about $5 at $0.068/h, at most about $11 at $0.136/h**. Both are estimates, not bills. Boxes are deleted after the verified pull.

## Pilot (calibrate `food_sense` once, never change it)

- **Runs.** For each candidate and each of the three species: seed 1, arm `treat`, food on (same food parameters), `per_channel`, `advect_genome`, `kappa = 3`, **10,000 steps**, sampled every 100. Candidates, a geometric ladder: `food_sense` in {0.1, 0.3, 1, 3, 10} (15 runs). Plus three `food_sense = 0` runs on the box (same species, seed, arm, `kappa = 3`) to compare with the stored reference; 18 runs. The scale: in the `quick` test `food_sense = 3` changes the hidden activations by up to 1.8 for a 1.7x change of the food level, so the top of the ladder is expected to saturate and the bottom to be a small perturbation.
- **Quantity.** `Q` = net food drawn into the body by step 10,000 = `body(10,000) - body(0)` = `food(0) - food(10,000)` (exact, because `sum(body) + sum(food)` is conserved). It is computable from the existing runs, which did not log gross uptake. The gross `food_eaten_cum` of the new runs is recorded too but is not used in the rule.
- **Reference.** `food_sense = 0` values from `outputs/conditional_blending_20261115` (`kappa = 3`, arm `treat`, food on, seeds 1 to 5, series sampled every 100 steps, index 10,000): `Q_ref` = seed 1's `Q`; the species' **seed-to-seed spread** `R` = max minus min of `Q` over seeds 1 to 5.
- **Pre-registered selection rule.** A candidate *changes foraging in a species* if `|Q_candidate - Q_ref| > R` for that species. A candidate **qualifies** if it changes foraging in **at least 2 of 3 species**, AND in all three of its runs the velocity saturation fraction `sat_frac` (fraction of body (channel, cell) velocities at the soft bound `|d| >= 0.9 max_step`, as defined on 2026-11-15) is below `1e-2` at every one of the 100 samples, AND in all three runs the max relative drift of `sum(body) + sum(food)` is at most `1e-12`. **Chosen `food_sense` = the smallest candidate that qualifies.** If none qualifies, the **largest candidate whose three runs are all non-saturating (every sample below `1e-2`) and conserve** is taken and this is said; if even none of those exists, the smallest candidate is taken. The main experiment runs either way.
- Every pilot run is listed in `outputs/food_sensing_20261116/pilot/PILOT.md` (Q, Q_ref, R, difference, gross eaten, end body, hybrid fraction, max sat over samples, drift, wall time) by `python scripts/food_sensing_summary.py pilot`. The three box `food_sense = 0` runs are reported next to the stored reference (whether the box reproduces the stored `Q` within `R`) but the rule uses the stored reference as written.
- One pilot only. A change of any pilot parameter (ladder, steps, species) is a new pilot with its own recorded criteria.
- Limits stated now: one seed per candidate and species; `Q` is a mass-total, so it can change with no change in how the two lineages differ; the criterion shows that sensing changes foraging, not that it changes it differently for the two lineages. The pilot criterion and the main verdict are separate questions.

## Main experiment: the 2 x 2 factorial (1,800 runs)

`food_sense` in {0, chosen} x `kappa` in {0, 3} x species {OSCILLIS, MITOSA, VAGRANT} x seeds 1 to 50 x arms {`treat` (A has `+u`, B has `-u`), `neutral_plus`, `neutral_minus`} = 4 x 3 x 50 x 3 = **1,800 runs**. Food on, same food parameters (`k = 0.05`, `d = 5e-4`, `D = 0.1`, `theta = 0.3`, initial food uniform with total equal to the body mass), `per_channel`, `advect_genome = True`, 30,000 steps, sampled every 100; same placements (`placements(seed)`), lineage axis (seed 20261103) and tag as every earlier experiment. `food_sense`, `kappa` and the `W1f` seed are recorded in each run's JSON. The `kappa = 0, food_sense = 0` cell is rerun here on the boxes (not taken from the earlier 5-seed set), so that all four cells share hardware and engine revision.

Cells: **F0K0** (blind, no repulsion), **F0K3** (blind, repulsion: the 2026-11-15 condition at 50 seeds), **F1K0** (sensing, no repulsion), **F1K3** (sensing, repulsion). Output directories `main/<cell>/` (file names repeat across cells).

Job order: a job list `jobs.txt` ordered seed by seed (1 to 50), within a seed species by species, within a species cell by cell, within a cell arm by arm (`treat`, `neutral_plus`, `neutral_minus`). It is split by remainder over the boxes (`awk (NR-1)%N==i`), so every box receives a mix of cells and seeds. Each shard is run by `scripts/run_batch.py` with its own log ending in `ALL_DONE`.

## Measures

Per run: A's share from the tag (`a = (1 + tag) / 2`, share `= sum(A_tot a) / sum(A_tot)`); `delta` = mean of the last 10% of samples minus the step-0 share; the winner of a treatment run is `+u` if `delta > 0`, `-u` otherwise, and the winner-side final share is `share_A_end` (`+u`) or `1 - share_A_end` (`-u`); end hybrid fraction (mass with `0.1 < a < 0.9`); end pure fraction; blob count; largest blob fraction; max relative drift of `sum(body) + sum(food)`; `sat_frac` at every sample (with the repulsion term; `sat_frac_without_repulsion` as in the earlier doc); wall time; **food consumed** = cumulative gross uptake over the run (`food_eaten_total`) and, comparably with the earlier sets, `Q_30000 = body(30,000) - body(0)`; **end body mass**.

## Decision rules (fixed before the runs)

**Rule 1: selection per cell per species.** Neutral envelope `E` = the largest `|delta|` among that cell's 100 neutral runs (50 seeds x `neutral_plus`, `neutral_minus`); this is primary. The 95th percentile of the 100 neutral `|delta|` (numpy linear interpolation) is reported as a **secondary**, less conservative envelope `E95` and labelled as such. A treatment seed is *outside* the envelope if `|delta| > E`. Let `n_out` be the number of treatment seeds outside `E` and `n_win` the larger of the numbers of outside seeds with `delta > 0` and with `delta < 0` (the winner is the genome of the larger group). Verdict:
- **selection** if at least 40 of 50 treatment seeds are outside `E` and agree on the winner (`n_win >= 40`);
- **takeover** if selection and the winner's median final share (over the seeds that are outside and agree) is at least 0.90;
- **large but inconsistent** if `n_out >= 40` and `n_win < 40`;
- **no selection detected** otherwise.
Report `E`, `E95`, `n_out`, the winner split (outside seeds `+u` / `-u`), and the winner-side final-share distribution (min, median, max, over the agreeing seeds). The same counts are reported against `E95` as a secondary.

**Rule 2: cause (the factorial question).** Food sensing is the **cause** of selection in a species, at a given `kappa`, if **selection or takeover** holds in the sensing-on cell and **no selection detected** holds in the matched sensing-off cell with the same `kappa`. Stated separately for `kappa = 0` and `kappa = 3`. Any other combination is reported as it is: *no cause shown* (sensing-on cell shows no selection), *selection also without sensing* (the off cell is not null), or *inconclusive* (a `large but inconsistent` cell). **Repulsion is a necessary condition** in a species if selection appears in the sensing-on cell at `kappa = 3` and not at `kappa = 0`.

**Rule 3: distinctness (step 2 replicated at 50 seeds).** Per species and per `food_sense` value, treatment arm, end hybrid fraction, `kappa = 3` against `kappa = 0` of the same `food_sense`: **distinct** if the median hybrid fraction at `kappa = 3` is at most half the median at `kappa = 0` AND at least 40 of 50 seeds are below the matched `kappa = 0` seed; **no effect** if fewer than 30 of 50 are below; **partial** otherwise.

**Rule 4: neutral-arm sanity.** In the neutral arms both lineages share `G8`, so food sensing and repulsion act identically on both; their share deltas should be centred on zero in every cell. Report, per cell and species, the mean and standard error of the 100 neutral deltas (and per arm). A cell whose neutral mean exceeds 2 SE from zero is **flagged as a harness asymmetry** (for example `+u` always placed first) and said plainly; this does not void the result but is reported next to it. With 12 cell-species combinations about 0.6 flags are expected by chance at the 2 SE level; this is stated in the results with the observed count.

**Rule 5: conservation.** Max relative drift of `sum(body) + sum(food)` per run, expected about `1e-15`; the maximum over all 1,800 runs is reported, with the count of runs above `1e-12`. The mean fraction of body velocities at the soft bound per cell is reported (`sat_frac`).

## Predictions (written before the runs)

(i) **Selection appears with sensing on and not off**, possibly only with repulsion: a heritable trait that touches the resource is selected, and the 2026-11-09 claim survives (ROADMAP step 0).

(ii) **Sensing changes foraging but no lineage wins consistently.** The lineage axis `u` is random (seed 20261103): the difference between `+u` and `-u` is not aligned with a food-response gradient in most species, and `W1f` is random. The two lineages then differ in how they react to food but not in whether the reaction pays. Then the next experiment is a genome axis chosen along the food-response gradient.

(iii) **Sensing changes nothing measurable** (the mechanism is too weak at a non-saturating gain); then `food eaten` and the shares are indistinguishable from the sensing-off cells.

My expectation, a guess and not a measurement: (ii), with a chance of a species-specific selection under (i) given 50 seeds (a consistent sign over 40 of 50 seeds is a strict bar, and the envelope is set by 100 neutral runs, so 1-in-100 excursions make `E` large). Outcomes can mix across species.

Known limits, stated now: `W1f` is one random draw per species (a different draw could give a different answer; the experiment cannot separate "sensing does not select" from "this `W1f` does not select"); the genome axis is the one fixed random axis of the earlier experiments; the food field is uniform at the start so the first steps give no gradient; one calibrated gain for three species; `E` is a maximum over 100 runs and is sensitive to a single outlier (hence the secondary `E95`); the neutral arms differ from the treatment arm only by the sign of the functional genome of lineage A; a `delta` threshold relative to a neutral envelope is a significance-like criterion, not an effect size.

---
