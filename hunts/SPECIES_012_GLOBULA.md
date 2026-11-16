# SPECIES 012 — GLOBULA

**Verdict:** VIABLE + REPRODUCING
**Origin:** random  |  **Seed:** 638

## Viability gates

| gate | verdict | value | detail |
| --- | --- | --- | --- |
| mass_conservation | PASS | 2.14239e-16 | tol=0.0001 |
| non_triviality | PASS | 11.3435 | conc>=6.0, occupancy 0.334<=0.45, 1 bodies |
| persistence | PASS | 1 | 1 organisms alive at the end with lifespan >= 15 frames |
| activity | PASS | 2.34498 | mean speed of the most mobile organism, cells/frame |

## Behaviour (anomaly bouncer)

| behaviour | established | score | evidence |
| --- | --- | --- | --- |
| phototaxis | no | 0.004 | lamp(26, 64): 38.3->38.2; lamp(102, 64): 38.5->37.8; lamp(64, 26): 38.4->36.7 | min approach +0.004 (needs > 0.05 for every lamp position) |
| predatory_pursuit | no | 0.000 | no closing pair found |
| cyclic_locomotion | no | 0.007 | uid=69ecfcbc circling=0.01 spectral_power=0.02 period=2.7 frames (counted only if >= 4) life=141 frames |

## Reproduction

Measured on the recording run below (the screening run is sampled more coarsely and its counts differ; both are stated separately rather than mixed).

- Divisions counted (offspring survived AND carried at least 10% of the parent's mass): **1**
- Raw fission events before the mass filter: **1** — the difference is debris a large body shed, which is not reproduction
- Surviving offspring total: **1**
- Organisms tracked in this run: **17**
- Screening run, for comparison: 1 divisions of 1 raw fissions, deepest generation 2

| frame | parent | children | parent mass | child masses | child share |
| --- | --- | --- | --- | --- | --- |
| 10 | `11123ae5` | `69ecfcbc` | 131.8 | 130.6, 64.9, 52.9, 47.5, 32.1, 26.8, 21.9 | 20% |

## Complexity

```json
{
  "morph_diversity": 0.14426244990926557,
  "spatial_mi": 1.5867267425083378,
  "cross_channel_mi": 1.0767512476592733,
  "euler_final": -6,
  "concentration_final": 11.343483580699676,
  "occupancy_final": 0.3338623046875,
  "n_blobs_final": 1,
  "activity": 2.344980867991842,
  "mass_drift": 2.1423933709259587e-16,
  "score": 12.577253776307902
}
```

## Lineage tree

```json
{
  "11123ae5": {
    "parent": null,
    "generation": 0,
    "birth_frame": 0,
    "death_frame": 11,
    "lifespan": 11,
    "children": [
      "7c6666ee",
      "59c7d6f3",
      "fb276d7e",
      "d8ca3247",
      "45a431c5",
      "89ea669e",
      "3a2b3c3d",
      "54e2ef4d",
      "67536d9c",
      "69ecfcbc",
      "fd5b8eab"
    ],
    "peak_mass": 2102.83339976786,
    "dominant_channel": 1
  },
  "7c6666ee": {
    "parent": "11123ae5",
    "generation": 1,
    "birth_frame": 5,
    "death_frame": 6,
    "lifespan": 1,
    "children": [],
    "peak_mass": 35.8809724058535,
    "dominant_channel": 1
  },
  "1ad15488": {
    "parent": null,
    "generation": 0,
    "birth_frame": 6,
    "death_frame": 7,
    "lifespan": 1,
    "children": [],
    "peak_mass": 18.78621447693434,
    "dominant_channel": 1
  },
  "4f38b032": {
    "parent": null,
    "generation": 0,
    "birth_frame": 6,
    "death_frame": 7,
    "lifespan": 1,
    "children": [],
    "peak_mass": 33.75836882628344,
    "dominant_channel": 1
  },
  "59c7d6f3": {
    "parent": "11123ae5",
    "generation": 1,
    "birth_frame": 7,
    "death_frame": 8,
    "lifespan": 1,
    "children": [],
    "peak_mass": 23.63586723004031,
    "dominant_channel": 1
  },
  "fb276d7e": {
    "parent": "11123ae5",
    "generation": 1,
    "birth_frame": 8,
    "death_frame": 9,
    "lifespan": 1,
    "children": [],
    "peak_mass": 247.80294227117122,
    "dominant_channel": 1
  },
  "d8ca3247": {
    "parent": "11123ae5",
    "generation": 1,
    "birth_frame": 9,
    "death_frame": 10,
    "lifespan": 1,
    "children": [],
    "peak_mass": 24.07579288389241,
    "dominant_channel": 1
  },
  "45a431c5": {
    "parent": "11123ae5",
    "generation": 1,
    "birth_frame": 10,
    "death_frame": 11,
    "lifespan": 1,
    "children": [],
    "peak_mass": 130.64637508669307,
    "dominant_channel": 0
  },
  "89ea669e": {
    "parent": "11123ae5",
    "generation": 1,
    "birth_frame": 10,
    "death_frame": 11,
    "lifespan": 1,
    "children": [],
    "peak_mass": 64.87581270884395,
    "dominant_channel": 0
  },
  "3a2b3c3d": {
    "parent": "11123ae5",
    "generation": 1,
    "birth_frame": 10,
    "death_frame": 11,
    "lifespan": 1,
    "children": [],
    "peak_mass": 52.8639586147765,
    "dominant_channel": 1
  },
  "54e2ef4d": {
    "parent": "11123ae5",
    "generation": 1,
    "birth_frame": 10,
    "death_frame": 11,
    "lifespan": 1,
    "children": [],
    "peak_mass": 47.547121757599854,
    "dominant_channel": 1
  },
  "67536d9c": {
    "parent": "11123ae5",
    "generation": 1,
    "birth_frame": 10,
    "death_frame": 11,
    "lifespan": 1,
    "children": [],
    "peak_mass": 32.088520385806966,
    "dominant_channel": 1
  },
  "69ecfcbc": {
    "parent": "11123ae5",
    "generation": 1,
    "birth_frame": 10,
    "death_frame": null,
    "lifespan": 141,
    "children": [],
    "peak_mass": 2033.7215439186637,
    "dominant_channel": 0
  },
  "fd5b8eab": {
    "parent": "11123ae5",
    "generation": 1,
    "birth_frame": 10,
    "death_frame": 11,
    "lifespan": 1,
    "children": [],
    "peak_mass": 21.871722419650084,
    "dominant_channel": 1
  },
  "7ffc4d91": {
    "parent": null,
    "generation": 0,
    "birth_frame": 38,
    "death_frame": 42,
    "lifespan": 4,
    "children": [],
    "peak_mass": 3.502467041913694,
    "dominant_channel": 1
  },
  "e58275c2": {
    "parent": null,
    "generation": 0,
    "birth_frame": 105,
    "death_frame": 107,
    "lifespan": 2,
    "children": [],
    "peak_mass": 1.9123486007921604,
    "dominant_channel": 1
  },
  "b17a9617": {
    "parent": null,
    "generation": 0,
    "birth_frame": 109,
    "death_frame": 110,
    "lifespan": 1,
    "children": [],
    "peak_mass": 2.3795718507468,
    "dominant_channel": 1
  }
}
```

## Media

- `outputs/SPECIES_012_GLOBULA_final.png`
- `outputs/SPECIES_012_GLOBULA.gif`
- `outputs/SPECIES_012_GLOBULA.mp4`

- genome: `outputs/species/SPECIES_012_GLOBULA_genome.json`
