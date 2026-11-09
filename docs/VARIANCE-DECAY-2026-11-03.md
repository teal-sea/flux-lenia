# ROADMAP step 1: genome variance decay

Status: **design fixed before any run.** Results are appended below the line once the runs finish; this section is not edited afterwards.

Date: 2026-11-03 (UTC). Run by Vizier (Hermes, Claude Opus 5.5) at Thomas's request, as the kill test for "The Dish" idea: a conserved-mass world where lineages compete for territory. If genome blending homogenizes the world faster than lineages interact, the Dish as written is a lava lamp.

## Question

How fast does between-lineage genome variation decay when the genome field advects with mass (`advect_genome=True`), compared with the frozen-field control (`advect_genome=False`)?

## Design

- Engine: `engine/neural_field.py` at `origin/main` `7983d06`, unchanged.
- Worlds: the three curated species (`outputs/species/SPECIES_00{1,2,3}_*_genome.json`): OSCILLIS, MITOSA, VAGRANT. Brain, kernels and config from the JSON; only `advect_genome` is changed.
- Seeding: two blobs of the species at the species' own spawn radius and peak, centres drawn from the placement seed with periodic separation of at least 40 cells. Blob A carries genome `+u`, blob B carries `-u`, with `u` a fixed unit vector (seed 20261103) in the 8-dimensional genome space.
- Placement seeds 1, 2, 3. Arms: advect on, advect off. 3 species x 3 seeds x 2 arms = 18 runs, 20,000 steps each, sampled every 100 steps.
- Software: Python 3.13, jax 0.11.1, numpy 2.5.2, scipy 1.18.1 (the pinned set in `requirements.txt`), CPU, float64, one thread per run.

## Measures

`s = G . u` per cell (+1 pure lineage A, -1 pure lineage B). All statistics are mass-weighted.

- `var_s`: variance of `s` over cells. Primary measure.
- `var_between`: variance of per-organism mean `s`, organisms segmented with `novelty_oracle.extract_blobs` defaults.
- `hybrid_frac` (`|s| < 0.5`), `pure_frac` (`|s| > 0.9`).
- First contact: first sample with `hybrid_frac > 0.01`.
- Half-life: first sampled step at which a measure is at most half its step-0 value; "> 20,000" if never.

## Decision rule (fixed now)

Using the median `var_s` half-life of the 9 advect-on runs:

- **under 1,000 steps: short.** Blending is fatal for the Dish as written; ROADMAP step 2 (conditional blending) has to come first.
- **over 10,000 steps, or never within 20,000: long.** Blending is not the bottleneck; ROADMAP step 3 can proceed.
- **in between: intermediate.** Report it and compare with the first-contact time.

Runs where the two lineages never touch say nothing about blending and are reported separately, not counted as "long".

## Known caveat in the control

With `advect_genome=False` the genome field stays in place, so mass moving onto empty background takes the background genome, zero, which reads as a hybrid. The control measures that frozen map sampled by moving mass. It is not a conserved lineage label. This is the control ROADMAP step 1 names, and it is reported with this caveat rather than treated as clean.

---

## Results

Appended 2026-11-09. All 18 runs finished all 20,000 steps; mass drift stayed below 1e-15 in every run. Full table: `outputs/variance_decay_20261103/SUMMARY.md` (from `scripts/variance_decay_summary.py`); per-run series and frames are in the same folder.

**Verdict by the fixed rule: long.** Median `var_s` half-life over the 9 advect-on runs is 19,400 steps (7,200, 7,300, 10,600, 15,900, 19,400, and four runs that never halved within 20,000). Every advect-on run had contact, so none was excluded. Blending is not the bottleneck for the Dish; ROADMAP step 3 can proceed.

What the median hides: the three species behave very differently.

| species | advect-on `var_s` half-lives | mass that is hybrid at step 20,000 | lineage A's share at step 20,000 |
|---|---|---|---|
| OSCILLIS | 7,200 / 15,900 / 10,600 | 63% / 39% / 53% | 48% / 56% / 53% |
| MITOSA | 7,300 / 19,400 / never | 67% / 29% / 8% | 35% / 51% / 44% |
| VAGRANT | never / never / never | 12% / 6% / 14% | 41% / 56% / 52% |

(seeds 1 / 2 / 3)

- VAGRANT keeps its lineages almost pure for the whole run. OSCILLIS ends with about half its mass hybrid. MITOSA depends on the seed.
- Lineage A's share stays between 35% and 56% in every run, so the variance that is lost comes from blending, not from one lineage taking over.
- `var_between` (per-organism means) falls much faster than `var_s` in some runs (VAGRANT seeds 1 and 3: 300 and 600 steps) while the cells stay pure. It is sensitive to how many small fragments the segmentation finds, and is not used for the verdict.
- Advect-off control: half-lives 400 to 5,500 steps, faster than advect-on in all 9 pairs. Its caveat (above) applies: moving mass reads the empty background's zero genome as hybrid, so this is not evidence that advection slows blending, only that the frozen field is a poor lineage label.

Deviations from the design: none in the recipe. Execution was split. The first batch ran on citadel (9 runs finished: all 6 OSCILLIS runs and MITOSA seed 1 both arms, MITOSA seed 2 advect on); the other 9 were cut off when citadel ran out of memory on 2026-11-08 and were rerun from scratch on an InstaBox machine (8 vCPU, Debian 13) on 2026-11-09 with the same script, the same pinned jax 0.11.1 / numpy 2.5.2 / scipy 1.18.1 and Python 3.13. Each run is self-contained, so no run mixes the two machines. Cloud run log: `outputs/variance_decay_20261103/runs.cloud-20261109.log`.
