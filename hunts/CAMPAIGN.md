# Campaign report

*Generated 2026-08-29 15:27 UTC from 120 screening records and `hunts/SPECIES_INDEX.json`. Regenerate with `python scripts/report.py`.*

## Objective

Determine how often a randomly parameterized Neural Flow Lenia world
produces an organism that **divides**: a body that splits into parts
which survive independently and each carry a substantial share of the
parent's mass. Secondary: characterize the behaviour of whatever is
found, and confirm that mass conservation holds across every run
regardless of outcome.

Division rather than growth is the operative question because mass is
conserved: no world here can manufacture a second organism, so the
only reproduction available is partition of what already exists.

**Seed batches:** 300, 400. **Records:** 120.

## Method

**Apparatus.** `engine/neural_field.py`. 128x128 periodic grid, 3 mass
channels, 16 multi-scale concentric ring kernels (radii 3-45 cells),
an 8-dimensional genome vector conditioning a shared 36-24-9 MLP via
FiLM modulation, flux-form reintegration transport. float64
throughout.

**Procedure per candidate.** Sample a kernel bank and brain from the
seed. Seed one blob at the centre. Run 720 steps, sampling invariants
and segmenting organisms every 12 steps. Apply the viability gates,
count divisions, and run the two track-based anomaly detectors.
Records are appended to JSONL whether the candidate passes or fails.

**Independent variables**, sampled per seed:

- concentration avoidance `alpha`: [0.2, 0.35, 0.55, 0.8]
- spawn radius: [16.0, 20.0, 26.0]
- spawn peak density: [0.9, 1.2, 1.4]
- kernel bank and MLP weights: drawn from the seed

**Viability gates** (all four must pass):

| gate | criterion |
| --- | --- |
| mass_conservation | max relative drift <= 1e-4 |
| non_triviality | peak/mean >= 6, occupancy <= 0.45, >= 1 body |
| persistence | >= 1 organism alive at the end, lifespan >= 25% of run |
| activity | most mobile organism > 0.02 cells/frame |

**Division criterion.** A fission event counts only if an offspring
both survives >= 6 frames and carries >= 10% of the parent's mass.
The raw fission count is retained alongside it. Without the mass
floor, debris shed by a large body is indistinguishable from
division; see `docs/FINDINGS.md` section 2.1.

**Curation.** The highest-scoring dividers are re-run for 900 steps
with finer tracking (every 6 steps), probed for phototaxis with a
lamp moved to three positions, recorded to PNG/GIF/MP4, and written
up individually as `hunts/SPECIES_*.md`.

## Results

### Yield

| outcome | count | rate |
| --- | --- | --- |
| screened | 120 | 100% |
| viable (all four gates) | 96 | 80% |
| any raw fission | 36 | 30% |
| **dividing (strict)** | **7** | **6%** |
| flagged by anomaly bouncer | 3 | 2% |
| errored | 0 | 0% |

The gap between viability and division is the headline number.
Producing *interesting dynamics* at random is easy; producing a
*specific capability* at random is roughly an order of magnitude
harder. That ratio is the argument for optimizing rather than
sampling (`docs/ROADMAP.md` step 6).

### Why candidates were rejected

| gate | failures |
| --- | --- |
| mass_conservation | 0 |
| non_triviality | 7 |
| persistence | 10 |
| activity | 7 |

Mass conservation never failed in 120 runs. The gate is not idle, it is simply never the binding constraint: conservation is structural in the transport scheme rather than something the dynamics can violate.

### Measured distributions

Median [min, max] over all screened candidates.

| quantity | value |
| --- | --- |
| mass drift (relative) | 2.18e-16 [0.000, 4.43e-16] |
| final concentration (peak/mean) | 18.330 [3.889, 86.626] |
| final occupancy | 0.201 [0.033, 0.572] |
| spatial MI (nats) | 1.497 [0.910, 1.650] |
| cross-channel MI (nats) | 0.848 [0.199, 1.384] |
| morphological diversity | 0.289 [0.000, 3.948] |
| organisms tracked | 5.000 [1, 143] |
| activity (cells/frame) | 0.104 [0.011, 9.947] |
| second-body mass share | 1.46e-04 [0.000, 0.619] |
| score | 2.240 [-1.000, 46.369] |

### Division rate by parameter

Small cells throughout; these are descriptive, not tests.

| parameter | value | n | dividers | rate |
| --- | --- | --- | --- | --- |
| alpha | 0.2 | 38 | 4 | 11% |
| alpha | 0.35 | 33 | 2 | 6% |
| alpha | 0.55 | 20 | 0 | 0% |
| alpha | 0.8 | 29 | 1 | 3% |
| spawn radius | 16.0 | 33 | 3 | 9% |
| spawn radius | 20.0 | 43 | 1 | 2% |
| spawn radius | 26.0 | 44 | 3 | 7% |

No parameter value is necessary or sufficient. An earlier reading of this table at n=2 suggested low alpha mattered; it did not survive n=7 (`docs/FINDINGS.md` section 3).

### Every divider found

| seed | batch | alpha | spawn r | divisions | raw | largest offspring | score | viable |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 442 | 400 | 0.35 | 16.0 | 4 | 4 | 41.2% | 46.4 | yes |
| 350 | 300 | 0.2 | 16.0 | 5 | 7 | 56.2% | 42.8 | yes |
| 458 | 400 | 0.35 | 16.0 | 3 | 6 | 88.5% | 31.7 | yes |
| 427 | 400 | 0.2 | 26.0 | 2 | 6 | 52.4% | 23.6 | yes |
| 302 | 300 | 0.2 | 26.0 | 1 | 5 | 21.4% | 15.6 | yes |
| 446 | 400 | 0.8 | 20.0 | 1 | 1 | 10.5% | 11.0 | yes |
| 425 | 400 | 0.2 | 26.0 | 1 | 4 | 12.7% | -1.0 | NO |

1 candidate(s) divided but failed a viability gate and were therefore not eligible for curation. Division alone is not sufficient.

### Anomaly bouncer

| behaviour | flagged |
| --- | --- |
| cyclic_locomotion | 3 |

Phototaxis is not screened for: it requires its own controlled runs with the lamp moved between positions, so it is evaluated only during curation.

## Curated species

3 species promoted from the screen, re-run at finer tracking, probed, recorded and written up individually.

| species | divisions | behaviours established | report |
| --- | --- | --- | --- |
| OSCILLIS | 4 | none | [`SPECIES_001_OSCILLIS.md`](SPECIES_001_OSCILLIS.md) |
| MITOSA | 5 | predatory_pursuit | [`SPECIES_002_MITOSA.md`](SPECIES_002_MITOSA.md) |
| VAGRANT | 3 | none | [`SPECIES_003_VAGRANT.md`](SPECIES_003_VAGRANT.md) |

### Behavioural outcomes

| behaviour | established | of |
| --- | --- | --- |
| cyclic_locomotion | 0 | 3 |
| phototaxis | 0 | 3 |
| predatory_pursuit | 1 | 3 |

**Phototaxis absent is a result, not a gap.** These brains were randomly initialized and never selected for light response, and the probe requires the mass to approach the lamp at every one of three lamp positions, so a creature drifting in a fixed direction cannot pass by being lucky about where the lamp is.

## Threats to validity

1. **Single seeding per candidate.** Each world is run from one
   initial condition. A candidate that divides may have done so for
   that layout rather than in general. Curated species were re-run
   with a different step budget and tracking cadence and continued to
   divide, which is weak replication, not strong.
2. **Detector cadence affects behavioural verdicts.** Detectors read
   organism tracks and inherit the sampling rate. One pursuit call
   flipped between the 12-step and 6-step cadences (0.27 vs 0.47
   against a 0.35 threshold). Published verdicts use the fine
   cadence and carry their raw numbers.
3. **Thresholds are chosen, not derived.** The 10% offspring mass
   floor, the 6-frame survival requirement, the 4-frame minimum
   cycle, and every gate bound are judgement calls. The 10% floor in
   particular moved the headline yield from 55% to 5% on identical
   runs. Raw counts are reported alongside filtered ones so the
   effect of each choice stays inspectable.
4. **Score-ranked curation.** The three written-up species are the
   top scorers, and the score weights division heavily. They are not
   a random sample of dividers.
5. **Cell counts are small.** The per-parameter breakdown above has
   a handful of dividers per cell. Treat it as description, not
   inference.

## Reproducing this campaign

```bash
python scripts/selftest.py            # 27 checks, run this first
# batch 300: 60 candidates over 4 shards
for i in $(seq 0 3); do \
  python scripts/discover.py screen --n 15 --shard $i --nshards 4 --base 300 & done; wait
# batch 400: 60 candidates over 3 shards
for i in $(seq 0 2); do \
  python scripts/discover.py screen --n 20 --shard $i --nshards 3 --base 400 & done; wait
python scripts/discover.py curate --target 3
python scripts/report.py
```

Seeds fully determine the kernel bank, the brain, `alpha` and the
spawn geometry, so a rerun reproduces the same candidates. Curated
species additionally store their full genome in
`outputs/species/*.json`; the selftest verifies that two independent
loads of a saved genome agree bitwise after 240 steps.

Raw records: `hunts/_screen/shard_*.jsonl`, one JSON object per
candidate. Console transcripts: `hunts/_screen/*.log`, `*.txt`.

## Conclusions

1. Randomly parameterized worlds are viable 80% of the time and divide 6% of the time. Structure is cheap; a named capability is not.
2. Mass conservation held in 120/120 runs, worst observed relative drift 4.4e-16, against a gate of 1e-4. Conservation is a property of the discretization, not of the parameters, and no candidate could violate it.
3. Division is governed by the mass budget, not by the controller. Searching brain weights alone at fixed physical parameters produced no dividers; adding concentration avoidance and seeded mass to the search produced them immediately. A body handed several times its preferred size must either split or go amorphous.
4. Rare binary targets need shaped objectives. The strict division count is 0 for nearly every candidate, so mutation search on it is flat. Adding continuous proxies (second-body mass share, largest offspring fraction) let a hill-climb reach an 89.7% offspring share in 4 generations from a non-dividing lineage.
5. Behaviours established across curated species: predatory_pursuit. Phototaxis was tested under a moving lamp and not established for any species, as expected for brains never selected for it.

Next steps and their ordering are in `docs/ROADMAP.md`. The first is
measuring how fast genome variance decays under the blending rule,
because that decides whether multi-species experiments are possible
at all.
