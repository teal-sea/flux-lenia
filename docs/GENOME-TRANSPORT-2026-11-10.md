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
