# Genome transport: does the no-food share shift vanish when the genome is conserved exactly?

Status: **design fixed before the main runs.** Results are appended below the final horizontal rule; this section is not edited afterwards.

Date: 2026-11-10 (UTC). Follows `docs/FOOD-SELECTION-2026-11-09.md`, whose last paragraphs name this experiment. Branch `vizier/genome-transport-conservation-20261110`, based on `vizier/food-selection-20261109`.

## Question

The food report found that without food every species showed a consistent small shift of lineage A's mass share toward one genome (OSCILLIS +u, MITOSA -u, VAGRANT +u; 5 of 5 treatment seeds outside the neutral envelope each), and it derived from the code that this is a bookkeeping effect: body channels each move on their own displacement, but the genome (and the neutral tag) moves on the cell's mass-weighted mean displacement, so `sum(A_tot * G)` is not conserved by transport. That explanation was derived, not measured. If it is right, a transport that conserves `sum(A_tot * G)` exactly must make the shift vanish. If the shift survives, the explanation was wrong.

## Change

New config flag `Config.genome_transport` in `engine/neural_field.py`:

- `"mean"` (default): the existing scheme. Every earlier result reproduces bit-for-bit with it.
- `"per_channel"`: new.

Notation. Cell `s` holds channel masses `A_c(s)` (c = 1..3) and genome vector `G(s)` (functional dimensions plus the tag). Channel `c` has displacement `d_c(s)`. `W_c(s -> x)` is the bilinear weight (partition of unity over the 3x3 stencil: `sum_x W_c(s -> x) = 1`) with which channel c's mass at `s` lands in cell `x`.

Mass (unchanged, same code path and same operation order):

    A_c'(x) = sum_s W_c(s -> x) A_c(s)           A_tot'(x) = sum_c A_c'(x)

Genome, `"per_channel"`: each channel carries its own copy of the pair `(A_c, A_c G)` along `d_c`, so the genome-weighted mass arriving from channel c is `W_c(s -> x) A_c(s) G(s)`:

    N(x)  = sum_c sum_s W_c(s -> x) A_c(s) G(s)
    G'(x) = N(x) / A_tot'(x)         where A_tot'(x) > 1e-30,   else G'(x) = G(x)

Conservation, exact in arithmetic: `sum_x A_tot'(x) G'(x) = sum_x N(x) = sum_c sum_s A_c(s) G(s) sum_x W_c(s -> x) = sum_s A_tot(s) G(s)`. This holds for every genome dimension, including the tag. (In `"mean"` the arriving genome weight uses `W_t(s -> x) A_tot(s)` with the mean displacement `d_t`, which differs from the per-channel weights, so the identity fails. Also `"mean"` uses a 1e-9 mass threshold below which a cell keeps its old genome; `"per_channel"` uses 1e-30, so that the sum of the discarded terms is negligible against rounding.) Cells with `A_tot' <= 1e-30` carry no mass, so they contribute nothing to `sum(A_tot G)`.

Stencil, window and clipping are identical to `"mean"`. Nothing else in the engine changes. In a full run the genome feeds the brain, so trajectories under the two modes differ over time; that is expected and is part of what is measured. The mass update itself is identical at every step given the same state.

## Tests (`scripts/test_transport.py`), written and run before any main run

For OSCILLIS, MITOSA, VAGRANT in the food-selection two-blob setup (food off, unread tag), 400 steps:

- (a) from the same state, one step in `"mean"` and `"per_channel"` gives identical `A` (max difference exactly 0), checked on every one of the 400 states of a `"mean"` trajectory;
- (b) under `"per_channel"`, `S = sum(A_tot * tag)` and `sum(A_tot * G_functional)` are conserved: max over steps of `|S_t - S_0| / M < 1e-12`;
- (c) under `"mean"` the same quantity drifts by more than 1e-6 of `M`, so the test discriminates.

## Experiment

Only the no-food arms of the food-selection design, new transport:

- Species OSCILLIS, MITOSA, VAGRANT (`outputs/species/`), seeds 1 to 5 (same spawn positions as before), arms `treat` (+u / -u), `neutral_plus`, `neutral_minus`, same tag, same `u` (seed 20261103).
- Food off. `advect_genome = True`, `genome_transport = "per_channel"`. 30,000 steps, sampled every 100.
- 3 x 5 x 3 = 45 runs. Python 3.13.5, jax 0.11.1, numpy 2.5.2, scipy 1.18.1, CPU float64, one thread per run (`XLA_FLAGS="--xla_cpu_multi_thread_eigen=false intra_op_parallelism_threads=1"`), 8 concurrent, on citadel (16 cores, 31 GiB), `nice -n 10`.
- Scheduling guards: pause launching when `free -g` available memory is under 6 GiB; drop to 6 concurrent if any run's RSS exceeds 2.5 GiB. If projected wall time exceeds 7 hours, reduce to seeds 1 to 3 and say so.

## Measures

As in the food report: `delta` = lineage A's mass share averaged over the last 10% of samples minus its share at step 0. Neutral envelope `E` per species = the largest `|delta|` among its 10 neutral runs (5 seeds x 2 neutral arms), now in the new mode. A treatment seed is outside the envelope if `|delta| > E`; its winner is `+u` if `delta > 0`, else `-u`. Also reported: the neutral-arm `|delta|` range under the new mode next to the old mode's (food-off runs in `outputs/food_selection_20261109/`), the median `delta` of the treatment seeds, and the max conservation drift of `sum(A_tot * tag)` along each run's series (the series records `share_A`, which is that quantity divided by total mass).

## Prediction and decision rule (fixed now)

Prediction: under exact conservation the consistent no-food shift vanishes, and the identical-lineage runs drift near zero.

Per species:

- **Vanished**: fewer than 4 of 5 treatment seeds are outside the envelope.
- **Persists**: 4 or more of 5 outside. Then the food report's explanation (that the shift comes from the genome/mass transport mismatch) was wrong, or at least incomplete, and the results say so with the numbers.

Caveats stated now. The envelope is set by the neutral runs themselves, so if exact conservation makes the neutral drift very small the envelope shrinks and the rule becomes stricter; the verdict is still computed by the rule as written, and the actual sizes are always reported. A `persists` verdict for a species cannot by itself say what causes the shift (for example genuine genome-dependent dynamics acting through the brain); it only says that the transport mismatch is not the whole explanation. A `vanished` verdict is evidence for the explanation, from 5 seeds per species. Runs from different modes are not paired one-to-one because trajectories diverge.

---

## Progress note (batch launched)

2026-11-10 14:03 UTC: 45 jobs (3 species x seeds 1-5 x 3 arms, food off, `per_channel`) launched on citadel by `outputs/genome_transport_20261110/run_all.sh` (scheduler `scripts/run_batch.py`, pid 1147960; 8 concurrent single-thread runs, nice 10). Jobs are ordered seed by seed, so seeds 1-3 finish first. Logs: `runs.log`, `rss.log` (peak RSS per run), `run_*.log`. Early RSS about 0.5 GiB per run; available memory 17-20 GiB. Test results before launch: `outputs/genome_transport_20261110/test_transport_output.txt` (A identical to exactly 0.0; per-channel tag drift at most 1.2e-16 of M over 400 steps; old mode 5.9e-5 to 2.1e-3). No deviation from the design so far.

---

## Results

Appended 2026-11-10 after the batch finished (18:18 UTC; started 14:03 UTC, 4 h 15 min wall). All 45 runs (3 species x seeds 1 to 5 x 3 arms, food off, `per_channel`, 30,000 steps) finished with exit code 0; no reduction of seeds was needed. Machine: citadel (16 vCPU, 31 GiB; the brief's "32 cores / 115 GiB" was wrong, corrected by the user), 8 concurrent single-thread runs under `nice -n 10`, no pause or concurrency cut triggered, peak RSS per run at most 0.51 GiB, each run 1,566 to 3,038 s wall (host load was about 36 to 39 from other work, so wall times are not comparable to the InstaBox runs). Python 3.13.5, jax 0.11.1, numpy 2.5.2, scipy 1.18.1, float64 CPU. Commits: design `f6c43a1` (before any main run), launch note `faf4900`. Per-run table and verdicts: `outputs/genome_transport_20261110/SUMMARY.md` (from `scripts/genome_transport_summary.py`), raw series and frames in the same folder.

**Tests** (`scripts/test_transport.py`, 400 steps per species, output in `outputs/genome_transport_20261110/test_transport_output.txt`): `A` is bit-identical between modes (max difference exactly 0.0) on every one of 400 states for each species. Under `per_channel`, max |S_t - S_0| / M for S = sum(A_tot * tag) was 1.23e-16 (OSCILLIS), 7.9e-17 (MITOSA), 1.21e-16 (VAGRANT); for the functional genome rows at most 8.8e-17. Under the old `mean` mode the same quantity drifted 2.05e-3, 4.26e-4 and 5.86e-5 of M, so the test discriminates. The `mean` path is textually unchanged and gives the same state hash as the pre-change code in a 300-step MITOSA rollout; `scripts/test_nutrient.py` still passes. In the 45 runs, `sum(body)` drift was at most 3.5e-15 relative.

**Result by the rule as written** (neutral envelope E from the 10 neutral runs of the new mode):

| species | neutral envelope E (share) | treatment seeds outside E | winner of those | verdict by the rule |
|---|---|---|---|---|
| OSCILLIS | 8.9e-16 | 5 of 5 | +u | persists |
| MITOSA | 8.3e-16 | 3 of 5 | -u | vanished |
| VAGRANT | 1.8e-15 | 2 of 5 | -u (mixed) | vanished |

**What those numbers are.** The rule's envelope is set by the neutral runs, and under exact conservation the neutral runs drift by rounding error only (largest |delta| over all 30 neutral runs 1.8e-13 in share points, i.e. about 1e-15 as a fraction), so E is at rounding scale and the rule fires on rounding noise. The design flagged this case in advance ("the envelope shrinks and the rule becomes stricter; the actual sizes are always reported"). The sizes: the largest |delta| of any treatment run is 3.4e-15 of the share (treatment deltas: OSCILLIS +2.0e-15 to +3.2e-15, MITOSA -6.7e-16 to -1.7e-15, VAGRANT -3.3e-16 to -3.4e-15), and the largest excursion of `share_A` from its starting value at any sampled step in any of the 45 runs is 3.7e-15. The old mode's no-food treatment shifts were 5.5 to 10 points (0.055 to 0.10 of the share), consistent winners in all 15 runs. So the shift is smaller by about 12 orders of magnitude and its sign is not tied to a genome in MITOSA and VAGRANT (and in OSCILLIS the +3e-15 is a rounding-level offset, not a share change anyone could see). By the letter of the rule OSCILLIS is "persists"; by the size of the effect it is gone. I report both and do not change the rule after the fact. A rerun that fixes a rounding-scale floor on E would give "vanished" for all three species, but that is a different rule from the one written here.

**Neutral-arm drift, new vs old** (|delta|, share points; old = food-off runs of 2026-11-09, all 5 seeds):

| species | old mode, min to max | new mode, min to max |
|---|---|---|
| OSCILLIS | 0.24 to 1.93 | 0 to 8.9e-14 |
| MITOSA | 0.41 to 3.89 | 5.6e-15 to 8.3e-14 |
| VAGRANT | 0.02 to 0.66 | 0 to 1.8e-13 |

The old range across species, 0.02 to 3.9 points, matches the food report's "0.7 to 3.9" at its upper end (that figure was the per-species maximum).

**Conclusion.** The food report's explanation holds: the consistent no-food share shift came from the genome and tag travelling on the mass-weighted mean displacement instead of each channel's own. With exact conservation, the treatment and neutral arms differ in share by at most 3.4e-15 in all 15 treatment runs, 12 orders of magnitude below the old effect. What it does not show: the lineages still mix and still build and lose blobs under the new transport (hybrid fraction and blob counts in SUMMARY.md); only the share bookkeeping became exact. Selection in this engine now means a gain in matter, not a relabelling. Limits: 5 seeds per species, one set of species, food off only, tag-based measure.

Deviations from the design: none in the recipe. The host had 16 cores and 31 GiB, not the brief's 32 and 115; the memory guards were set to 6 GiB available and 2.5 GiB RSS per the user's correction (the brief had said 20 GiB). The scheduler `scripts/run_batch.py` and the optional TRANSPORT argument on `scripts/food_selection.py` were added; with the argument omitted that script behaves as before. During test development the first per-channel implementation changed `A` by 1.8e-15 (XLA fused the genome numerator into the mass loop); the fix was an `optimization_barrier` so the mass loop is compiled as in the other branches, and A identity is then exactly 0 (this was done before the design commit and before any main run).
