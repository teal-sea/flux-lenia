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

(appended after the runs)
