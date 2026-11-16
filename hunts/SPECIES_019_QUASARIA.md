# SPECIES 019 — QUASARIA

**Verdict:** VIABLE + REPRODUCING
**Origin:** random  |  **Seed:** 780

## Viability gates

| gate | verdict | value | detail |
| --- | --- | --- | --- |
| mass_conservation | PASS | 2.20307e-16 | tol=0.0001 |
| non_triviality | PASS | 9.88523 | conc>=6.0, occupancy 0.323<=0.45, 1 bodies |
| persistence | PASS | 1 | 1 organisms alive at the end with lifespan >= 15 frames |
| activity | PASS | 3.61163 | mean speed of the most mobile organism, cells/frame |

## Behaviour (anomaly bouncer)

| behaviour | established | score | evidence |
| --- | --- | --- | --- |
| phototaxis | no | 0.008 | lamp(26, 64): 38.4->37.9; lamp(102, 64): 38.4->38.1; lamp(64, 26): 38.4->38.1 | min approach +0.008 (needs > 0.05 for every lamp position) |
| predatory_pursuit | no | 0.000 | no closing pair found |
| cyclic_locomotion | no | 0.015 | uid=11279b44 circling=0.01 spectral_power=0.02 period=2.6 frames (counted only if >= 4) life=136 frames |

## Reproduction

Measured on the recording run below (the screening run is sampled more coarsely and its counts differ; both are stated separately rather than mixed).

- Divisions counted (offspring survived AND carried at least 10% of the parent's mass): **2**
- Raw fission events before the mass filter: **2** — the difference is debris a large body shed, which is not reproduction
- Surviving offspring total: **3**
- Organisms tracked in this run: **46**
- Screening run, for comparison: 1 divisions of 1 raw fissions, deepest generation 2

| frame | parent | children | parent mass | child masses | child share |
| --- | --- | --- | --- | --- | --- |
| 8 | `e75ebe90` | `33386d8f`, `b611107b` | 273.9 | 126.9, 90.1, 86.4 | 46%, 32% |
| 15 | `c50f9c94` | `11279b44` | 38.6 | 24.5 | 63% |

## Complexity

```json
{
  "morph_diversity": 0.0,
  "spatial_mi": 1.5037190557630788,
  "cross_channel_mi": 0.7899100137802343,
  "euler_final": 37,
  "concentration_final": 9.885231429385376,
  "occupancy_final": 0.323486328125,
  "n_blobs_final": 1,
  "activity": 3.6116345435647057,
  "mass_drift": 2.2030726243372084e-16,
  "score": 11.761696225576765
}
```

## Lineage tree

```json
{
  "e75ebe90": {
    "parent": null,
    "generation": 0,
    "birth_frame": 0,
    "death_frame": 9,
    "lifespan": 9,
    "children": [
      "086f1d36",
      "e70edcb5",
      "457ef002",
      "e23dac64",
      "bd650aa2",
      "5b05b509",
      "85b8f75f",
      "601ed303",
      "ebd13f45",
      "5572a79d",
      "d4143ca9",
      "62ac368d",
      "33386d8f",
      "d4b3f59e",
      "b611107b",
      "0ab65745",
      "1731ca39"
    ],
    "peak_mass": 2043.1600902223397,
    "dominant_channel": 1
  },
  "086f1d36": {
    "parent": "e75ebe90",
    "generation": 1,
    "birth_frame": 3,
    "death_frame": 4,
    "lifespan": 1,
    "children": [],
    "peak_mass": 47.179618241026404,
    "dominant_channel": 1
  },
  "e70edcb5": {
    "parent": "e75ebe90",
    "generation": 1,
    "birth_frame": 4,
    "death_frame": 5,
    "lifespan": 1,
    "children": [
      "cdc1245c"
    ],
    "peak_mass": 44.95253605067494,
    "dominant_channel": 1
  },
  "457ef002": {
    "parent": "e75ebe90",
    "generation": 1,
    "birth_frame": 4,
    "death_frame": 5,
    "lifespan": 1,
    "children": [],
    "peak_mass": 32.54574722130518,
    "dominant_channel": 1
  },
  "e23dac64": {
    "parent": "e75ebe90",
    "generation": 1,
    "birth_frame": 4,
    "death_frame": 5,
    "lifespan": 1,
    "children": [],
    "peak_mass": 25.758097889445764,
    "dominant_channel": 1
  },
  "bd650aa2": {
    "parent": "e75ebe90",
    "generation": 1,
    "birth_frame": 4,
    "death_frame": 5,
    "lifespan": 1,
    "children": [],
    "peak_mass": 25.482560869043617,
    "dominant_channel": 1
  },
  "5b05b509": {
    "parent": "e75ebe90",
    "generation": 1,
    "birth_frame": 4,
    "death_frame": 5,
    "lifespan": 1,
    "children": [],
    "peak_mass": 23.693578778652558,
    "dominant_channel": 2
  },
  "cdc1245c": {
    "parent": "e70edcb5",
    "generation": 2,
    "birth_frame": 5,
    "death_frame": 6,
    "lifespan": 1,
    "children": [],
    "peak_mass": 31.28944711224569,
    "dominant_channel": 1
  },
  "5bf6e669": {
    "parent": null,
    "generation": 0,
    "birth_frame": 5,
    "death_frame": 6,
    "lifespan": 1,
    "children": [],
    "peak_mass": 17.686306771075955,
    "dominant_channel": 1
  },
  "85b8f75f": {
    "parent": "e75ebe90",
    "generation": 1,
    "birth_frame": 6,
    "death_frame": 9,
    "lifespan": 3,
    "children": [
      "269c4b24",
      "c2b6b8d7"
    ],
    "peak_mass": 297.1333634356847,
    "dominant_channel": 1
  },
  "601ed303": {
    "parent": "e75ebe90",
    "generation": 1,
    "birth_frame": 6,
    "death_frame": 7,
    "lifespan": 1,
    "children": [],
    "peak_mass": 23.920999967152465,
    "dominant_channel": 2
  },
  "ebd13f45": {
    "parent": "e75ebe90",
    "generation": 1,
    "birth_frame": 6,
    "death_frame": 7,
    "lifespan": 1,
    "children": [],
    "peak_mass": 17.07902005760257,
    "dominant_channel": 1
  },
  "5572a79d": {
    "parent": "e75ebe90",
    "generation": 1,
    "birth_frame": 7,
    "death_frame": 12,
    "lifespan": 5,
    "children": [],
    "peak_mass": 97.43615039410689,
    "dominant_channel": 2
  },
  "d4143ca9": {
    "parent": "e75ebe90",
    "generation": 1,
    "birth_frame": 7,
    "death_frame": 10,
    "lifespan": 3,
    "children": [],
    "peak_mass": 24.243214327119304,
    "dominant_channel": 2
  },
  "62ac368d": {
    "parent": "e75ebe90",
    "generation": 1,
    "birth_frame": 7,
    "death_frame": 9,
    "lifespan": 2,
    "children": [],
    "peak_mass": 22.570814779703298,
    "dominant_channel": 1
  },
  "269c4b24": {
    "parent": "85b8f75f",
    "generation": 2,
    "birth_frame": 7,
    "death_frame": 8,
    "lifespan": 1,
    "children": [],
    "peak_mass": 42.621691839861654,
    "dominant_channel": 1
  },
  "33386d8f": {
    "parent": "e75ebe90",
    "generation": 1,
    "birth_frame": 8,
    "death_frame": 14,
    "lifespan": 6,
    "children": [
      "079b31e9",
      "1fe773ad",
      "d9e041b2"
    ],
    "peak_mass": 375.58126178337653,
    "dominant_channel": 1
  },
  "d4b3f59e": {
    "parent": "e75ebe90",
    "generation": 1,
    "birth_frame": 8,
    "death_frame": 12,
    "lifespan": 4,
    "children": [],
    "peak_mass": 109.93754291224184,
    "dominant_channel": 2
  },
  "b611107b": {
    "parent": "e75ebe90",
    "generation": 1,
    "birth_frame": 8,
    "death_frame": 14,
    "lifespan": 6,
    "children": [],
    "peak_mass": 97.99317976017366,
    "dominant_channel": 2
  },
  "c2b6b8d7": {
    "parent": "85b8f75f",
    "generation": 2,
    "birth_frame": 8,
    "death_frame": 10,
    "lifespan": 2,
    "children": [],
    "peak_mass": 27.545237579881327,
    "dominant_channel": 1
  },
  "20084b27": {
    "parent": null,
    "generation": 0,
    "birth_frame": 8,
    "death_frame": 12,
    "lifespan": 4,
    "children": [
      "aff93046",
      "a36e512a"
    ],
    "peak_mass": 166.2037340603263,
    "dominant_channel": 1
  },
  "079b31e9": {
    "parent": "33386d8f",
    "generation": 2,
    "birth_frame": 9,
    "death_frame": 10,
    "lifespan": 1,
    "children": [],
    "peak_mass": 20.432137386471563,
    "dominant_channel": 2
  },
  "0ab65745": {
    "parent": "e75ebe90",
    "generation": 1,
    "birth_frame": 9,
    "death_frame": 10,
    "lifespan": 1,
    "children": [],
    "peak_mass": 95.27410517797361,
    "dominant_channel": 1
  },
  "1731ca39": {
    "parent": "e75ebe90",
    "generation": 1,
    "birth_frame": 9,
    "death_frame": 10,
    "lifespan": 1,
    "children": [],
    "peak_mass": 15.287254832372042,
    "dominant_channel": 1
  },
  "1fe773ad": {
    "parent": "33386d8f",
    "generation": 2,
    "birth_frame": 10,
    "death_frame": 11,
    "lifespan": 1,
    "children": [
      "658e037c"
    ],
    "peak_mass": 49.86045162483593,
    "dominant_channel": 1
  },
  "f279ca45": {
    "parent": null,
    "generation": 0,
    "birth_frame": 10,
    "death_frame": 11,
    "lifespan": 1,
    "children": [],
    "peak_mass": 39.02439609005309,
    "dominant_channel": 2
  },
  "3d453844": {
    "parent": null,
    "generation": 0,
    "birth_frame": 10,
    "death_frame": 11,
    "lifespan": 1,
    "children": [],
    "peak_mass": 29.38311829536996,
    "dominant_channel": 2
  },
  "aff93046": {
    "parent": "20084b27",
    "generation": 1,
    "birth_frame": 11,
    "death_frame": 14,
    "lifespan": 3,
    "children": [
      "9af15577"
    ],
    "peak_mass": 261.0996075420085,
    "dominant_channel": 2
  },
  "658e037c": {
    "parent": "1fe773ad",
    "generation": 3,
    "birth_frame": 11,
    "death_frame": 13,
    "lifespan": 2,
    "children": [],
    "peak_mass": 18.186880128756567,
    "dominant_channel": 2
  },
  "c68d748f": {
    "parent": null,
    "generation": 0,
    "birth_frame": 11,
    "death_frame": 12,
    "lifespan": 1,
    "children": [],
    "peak_mass": 23.23108309634724,
    "dominant_channel": 1
  },
  "5eaac897": {
    "parent": null,
    "generation": 0,
    "birth_frame": 11,
    "death_frame": 12,
    "lifespan": 1,
    "children": [],
    "peak_mass": 24.061835980177428,
    "dominant_channel": 1
  },
  "44c90f68": {
    "parent": null,
    "generation": 0,
    "birth_frame": 11,
    "death_frame": 12,
    "lifespan": 1,
    "children": [],
    "peak_mass": 17.27608921455561,
    "dominant_channel": 1
  },
  "9af15577": {
    "parent": "aff93046",
    "generation": 2,
    "birth_frame": 12,
    "death_frame": 13,
    "lifespan": 1,
    "children": [],
    "peak_mass": 21.286277233975326,
    "dominant_channel": 1
  },
  "a36e512a": {
    "parent": "20084b27",
    "generation": 1,
    "birth_frame": 12,
    "death_frame": 13,
    "lifespan": 1,
    "children": [],
    "peak_mass": 32.797769836951495,
    "dominant_channel": 1
  },
  "a2fef896": {
    "parent": null,
    "generation": 0,
    "birth_frame": 12,
    "death_frame": 13,
    "lifespan": 1,
    "children": [],
    "peak_mass": 23.692359134751197,
    "dominant_channel": 1
  },
  "d9e041b2": {
    "parent": "33386d8f",
    "generation": 2,
    "birth_frame": 13,
    "death_frame": 15,
    "lifespan": 2,
    "children": [
      "cd5b8e1d"
    ],
    "peak_mass": 478.4789888621103,
    "dominant_channel": 1
  },
  "cd5b8e1d": {
    "parent": "d9e041b2",
    "generation": 3,
    "birth_frame": 14,
    "death_frame": 16,
    "lifespan": 2,
    "children": [],
    "peak_mass": 784.8833153952661,
    "dominant_channel": 1
  },
  "c50f9c94": {
    "parent": null,
    "generation": 0,
    "birth_frame": 14,
    "death_frame": 16,
    "lifespan": 2,
    "children": [
      "11279b44"
    ],
    "peak_mass": 38.59785398964835,
    "dominant_channel": 2
  },
  "5eff8eed": {
    "parent": null,
    "generation": 0,
    "birth_frame": 14,
    "death_frame": 16,
    "lifespan": 2,
    "children": [],
    "peak_mass": 25.918938212748557,
    "dominant_channel": 2
  },
  "317ee030": {
    "parent": null,
    "generation": 0,
    "birth_frame": 14,
    "death_frame": 15,
    "lifespan": 1,
    "children": [
      "c6863b84"
    ],
    "peak_mass": 20.846701817217628,
    "dominant_channel": 1
  }
}
```

## Media

- `outputs/SPECIES_019_QUASARIA_final.png`
- `outputs/SPECIES_019_QUASARIA.gif`
- `outputs/SPECIES_019_QUASARIA.mp4`

- genome: `outputs/species/SPECIES_019_QUASARIA_genome.json`
