# Food and selection: does a lineage take over when there is something to eat?

Status: **design fixed before the main runs.** Results are appended below the line once the runs finish; this section is not edited afterwards.

Date: 2026-11-09 (UTC). Run by Vizier (Hermes, Claude Opus 5.5) at Thomas's request. It follows `docs/VARIANCE-DECAY-2026-11-03.md`. That experiment found that two lineages stay distinct for most of a 20,000-step run, but that neither one ever wins: lineage A's share stayed between 35% and 56% in every run. ROADMAP step 0's target claim needs a lineage that grows at another's expense. This experiment adds ROADMAP step 4, a consumable food channel, and measures ROADMAP step 3's quantity (mass share by lineage) for two lineages.

## Question

With food in the dish, does one genome take mass from the other, consistently enough across seeds to be selection rather than position or luck? And is food what makes the difference?

## Food (engine/nutrient.py, new; engine/neural_field.py unchanged)

After each neural_field step, per cell:

- uptake `U = F (1 - exp(-k A_tot)) A_tot^2 / (A_tot^2 + theta^2)`, added to the body in proportion to its channel mix and taken from food
- decay: a fraction `d` of the body returns to food
- food diffuses with coefficient `D` (periodic 5-point stencil)

`sum(body) + sum(food)` is conserved to float rounding: about 1e-15 relative in every pilot run. The brain does not see food, because the curated species were found with three body channels. Organisms forage blind, so anything food selects for acts through movement and shape.

Fixed parameters: `k = 0.05`, `d = 5e-4` (body turns over about every 2,000 steps), `D = 0.1`, `theta = 0.3`. Initial food is uniform and equal in total to the initial body mass.

## Neutral tag

`nutrient.tagged()` adds a ninth genome dimension whose FiLM weights are zero. The brain cannot read it, but it is carried and blended with the mass like the functional genome. Lineage A starts with tag +1 and B with -1. Per cell, `a = (1 + tag) / 2` is the fraction of A ancestry, and A's share of the dish is `sum(A_tot a) / sum(A_tot)`. Checked in `scripts/test_nutrient.py`: with an unread tag and food off, the engine is identical to `neural_field.step` (difference exactly 0), and flipping the tag changes no body cell over 300 steps with food.

This replaces ROADMAP step 3's frozen-genome control. The variance-decay experiment showed that the frozen field reads empty background as hybrid, so it is a poor lineage label.

## Design

- Species: OSCILLIS, MITOSA, VAGRANT (`outputs/species/`). Seeds 1 to 5 set the two spawn positions (the same placement rule as the variance-decay experiment). Both blobs use the same noise seed, so they have identical shape, channel mix and mass.
- Arms, per species and seed:
  - `treat`: A has functional genome `+u`, B has `-u` (`u` is the unit vector from seed 20261103, as before).
  - `neutral_plus`: both have `+u`.
  - `neutral_minus`: both have `-u`.
- Food on and food off.
- 3 species x 5 seeds x 3 arms x 2 food settings = 90 runs, 30,000 steps each, sampled every 100 steps. `advect_genome = True`.
- Software: Python 3.13, jax 0.11.1, numpy 2.5.2, scipy 1.18.1, CPU, float64, one thread per run, on InstaBox machines (8 vCPU, 16 GiB, Debian 13).

## Decision rule (fixed now)

`delta` = A's share averaged over the last 10% of samples, minus A's share at step 0. The step-0 share is close to 0.5 (0.501 for seed 1; the two identical blobs differ only by where their centres fall on the grid) and is recorded per run.

For each species and food setting:

- Neutral envelope `E` = the largest `|delta|` among its 10 neutral runs (5 seeds x 2 neutral arms).
- A treatment seed is **out of the envelope** if its `|delta| > E`. Its winner is the genome whose lineage gained (`+u` if `delta > 0`).
- **Selection**: at least 4 of the 5 treatment seeds are out of the envelope, and all of those agree on the winner.
- **Takeover**: selection, and the winner's final share is at least 0.90 in those seeds.
- **Large but inconsistent**: at least 4 out of the envelope, but the winners disagree (position or chance decides).
- **No selection detected**: otherwise.

Food is **the cause** for a species if it shows selection with food on and not with food off.

## Pilot (calibration only; neutral arm, seed 1, 10,000 steps)

The pilot used only `neutral_plus`, where the two lineages are genetically identical, so it says nothing about which genome wins. Its criteria were written before it ran (`outputs/food_selection_20261109/pilot/PILOT.md`).

- **Try 1, no density threshold (theta = 0):** rejected. Total mass was conserved (drift at most 7.4e-16) and food was eaten down to about 0.010 per cell. But food ended uniform at that level everywhere: body mass covered 92 to 100% of the dish at density above 0.01, because the faint tails that transport leaves around every organism could eat and grew exponentially. A dish where food is equally depleted everywhere has nothing left to forage for.
- **Try 2, theta = 0.3:** kept. Food stays patchy (0.011 to 0.039 per cell at step 10,000). Body reaches 90 to 93% of the total.
- **Matched no-food runs** (same seed and arm) show that thin film is these species' normal state in a two-blob dish, not something food causes. The share of mass in cells below density 0.3 was, with food against without: OSCILLIS 16% against 76%, MITOSA 11% against 30%, VAGRANT 48% against 55%. So try 2's food makes the dish denser, not thinner. The pilot's "at least 70% in dense cells" criterion fails the no-food dish itself, so it was the wrong bar and is replaced by this comparison.
- **Known deviation:** with food, OSCILLIS breaks into about 1,400 dense specks of 1 to 20 cells (91% of its mass above the blob threshold, the largest connected piece 0.3% of the mass). Without food it forms 28 blobs, the largest 45%. It fails the pilot's "largest blob at least 5%" criterion, and it is kept in the experiment with that label: food turns OSCILLIS into dust. Its share measurement is unaffected, because the tag is defined per cell.

## Caveats known before the runs

- Transport moves the genome (and tag) on each cell's mass-weighted mean displacement, while the body channels each move on their own. So `sum(A_tot * tag)` is not exactly conserved by transport alone, and some share drift happens with no selection at all. The neutral arms measure that drift together with position effects. That is what the envelope is for.
- In `treat`, the `+u` lineage always starts at the seed's first position. The neutral arms use the same positions, so position effects show up in the envelope.
- Five seeds is a small sample. The rule needs 4 of 5, and every run is reported, not just the verdicts.
- Blind foraging: selection can only act through movement and shape, since the brain cannot sense food.

---

## Results

Appended 2026-11-09. All 90 runs finished all 30,000 steps on four InstaBox machines (one calibrated machine and three copies of it, with identical `engine/nutrient.py` and `scripts/food_selection.py` hashes), with no failures. `sum(body) + sum(food)` drifted at most 3e-15 relative in any run. Full per-run table and verdicts: `outputs/food_selection_20261109/SUMMARY.md` (from `scripts/food_selection_summary.py`); series and frames for every run are in the same folder.

**Food did not make any lineage take over, and food is not the cause of selection for any species.** No winner reached a 90% share in any run; the highest final share was 0.648.

| species | food | neutral envelope E | treatment seeds outside E | winner | winner's final share | verdict by the rule |
|---|---|---|---|---|---|---|
| OSCILLIS | on | 0.014 | 4 of 5 | +u | 0.54 to 0.60 | selection |
| OSCILLIS | off | 0.019 | 5 of 5 | +u | 0.56 to 0.60 | selection |
| MITOSA | on | 0.019 | 2 of 5 | -u | 0.53, 0.54 | no selection detected |
| MITOSA | off | 0.039 | 5 of 5 | -u | 0.55 to 0.59 | selection |
| VAGRANT | on | 0.023 | 2 of 5 | +u | 0.54, 0.65 | no selection detected |
| VAGRANT | off | 0.007 | 5 of 5 | +u | 0.52 to 0.57 | selection |

What the table says:

- **Without food, every species shows a small, consistent shift toward one genome.** All 15 no-food treatment runs move the same way within each species, outside every identical-lineage run: +u gains 6.5 to 10 points in OSCILLIS, -u gains 5.5 to 9 points in MITOSA, and +u gains 1.6 to 6.4 points in VAGRANT. The identical-lineage runs move at most 0.7 to 3.9 points.
- **Food weakens it.** With food, MITOSA and VAGRANT no longer have a consistent winner, and OSCILLIS keeps the same winner (+u) at about the same size as without food. So in OSCILLIS the shift that survives is the no-food one, not something food adds.
- **By the end most mass carries ancestry from both lineages.** The share of mass whose ancestry is between 10% and 90% lineage A ranged from 0.18 to 1.00 in the treatment runs. "Lineage A holds 60%" therefore mostly means the average cell is 60% A, not that A's organisms hold 60% of the dish.

**Where the no-food shift comes from (derived from the code, not separately measured).** With no food there is no growth, and blending at a merge is a mass-weighted average, so the mass-weighted ancestry `sum(A_tot * a)` would be exactly conserved if the genome travelled exactly with the matter. In `reintegrate` it does not quite: each body channel moves on its own displacement, while the genome (and the tag with it) moves on the cell's mass-weighted mean displacement (`dy_t`, `engine/neural_field.py` lines 355 to 382). Without food, a change in A's share can only come from that mismatch. The shifts above are real and consistent for this engine. But they are the inheritance rule handing one genome's label to matter that did not come from it, wherever the two genomes' channels move differently. They are not one lineage acquiring or holding more mass. Calling that ROADMAP step 0's selection would overstate it: it is a heredity bias of this transport scheme.

**What this means for the Dish.** Food as built here (blind foraging, the same uptake and decay constants for every genome) does not give a lineage a way to win, and it washes out the small bias the engine already had. Two things stand in the way: the inheritance rule itself picks a direction, and lineages mostly merge on contact. The next measurement should remove the first. Carry the genome on each channel's own displacement, so that `sum(A_tot * genome)` is conserved exactly by transport. Then rerun the no-food arms, where the shift should vanish; if it does not, the explanation above is wrong. Only after that does a selection result in this engine mean what ROADMAP step 0 says.

Deviations from the design: none in the recipe. Calibration history is above and in `outputs/food_selection_20261109/pilot/`. The machines ran about 2.7 machine-hours in total and were deleted after the results were copied back with matching checksums.
