# SPECIES 029 — BIFIDA

**Verdict:** VIABLE + REPRODUCING
**Origin:** random  |  **Seed:** 951

## Viability gates

| gate | verdict | value | detail |
| --- | --- | --- | --- |
| mass_conservation | PASS | 4.0325e-16 | tol=0.0001 |
| non_triviality | PASS | 11.3954 | conc>=6.0, occupancy 0.436<=0.45, 1 bodies |
| persistence | PASS | 1 | 1 organisms alive at the end with lifespan >= 15 frames |
| activity | PASS | 3.67396 | mean speed of the most mobile organism, cells/frame |

## Behaviour (anomaly bouncer)

| behaviour | established | score | evidence |
| --- | --- | --- | --- |
| phototaxis | no | -0.015 | lamp(26, 64): 38.3->38.9; lamp(102, 64): 38.5->38.8; lamp(64, 26): 38.5->38.7 | min approach -0.015 (needs > 0.05 for every lamp position) |
| predatory_pursuit | no | 0.000 | no closing pair found |
| cyclic_locomotion | no | 0.096 | uid=f2d5108e circling=0.10 spectral_power=0.02 period=23.2 frames (counted only if >= 4) life=117 frames |

## Reproduction

Measured on the recording run below (the screening run is sampled more coarsely and its counts differ; both are stated separately rather than mixed).

- Divisions counted (offspring survived AND carried at least 10% of the parent's mass): **1**
- Raw fission events before the mass filter: **2** — the difference is debris a large body shed, which is not reproduction
- Surviving offspring total: **1**
- Organisms tracked in this run: **190**
- Screening run, for comparison: 2 divisions of 2 raw fissions, deepest generation 3

| frame | parent | children | parent mass | child masses | child share |
| --- | --- | --- | --- | --- | --- |
| 34 | `bb44ad35` | `f2d5108e` | 121.6 | 26.8 | 22% |

## Complexity

```json
{
  "morph_diversity": 0.0,
  "spatial_mi": 1.490036188700788,
  "cross_channel_mi": 0.8517624183366331,
  "euler_final": 9,
  "concentration_final": 11.395417361173251,
  "occupancy_final": 0.435546875,
  "n_blobs_final": 1,
  "activity": 3.673955890021571,
  "mass_drift": 4.032497168960531e-16,
  "score": 20.358617761807714
}
```

## Lineage tree

```json
{
  "779cbcd4": {
    "parent": null,
    "generation": 0,
    "birth_frame": 0,
    "death_frame": 4,
    "lifespan": 4,
    "children": [
      "9dd8e3a9",
      "ba680023",
      "05d8b901",
      "25a19574",
      "cf017fcc",
      "e8f00efa",
      "b8a14d0c"
    ],
    "peak_mass": 4477.195785532783,
    "dominant_channel": 1
  },
  "9dd8e3a9": {
    "parent": "779cbcd4",
    "generation": 1,
    "birth_frame": 1,
    "death_frame": 2,
    "lifespan": 1,
    "children": [],
    "peak_mass": 79.5900969911687,
    "dominant_channel": 1
  },
  "ba680023": {
    "parent": "779cbcd4",
    "generation": 1,
    "birth_frame": 1,
    "death_frame": 2,
    "lifespan": 1,
    "children": [],
    "peak_mass": 34.48449592562669,
    "dominant_channel": 1
  },
  "05d8b901": {
    "parent": "779cbcd4",
    "generation": 1,
    "birth_frame": 3,
    "death_frame": 8,
    "lifespan": 5,
    "children": [
      "15c27031",
      "49ab7afc",
      "88689195",
      "47fbd0a9",
      "4ea735bf",
      "0a4e28bc",
      "947f8726",
      "9ce13d96",
      "cb791387",
      "e33761e4",
      "ba3a2f0c",
      "4e978ab8",
      "c74a8692",
      "1b247b12",
      "ff4e97e4",
      "043678a9",
      "ed34b6a3"
    ],
    "peak_mass": 2745.8641882479583,
    "dominant_channel": 1
  },
  "25a19574": {
    "parent": "779cbcd4",
    "generation": 1,
    "birth_frame": 4,
    "death_frame": 6,
    "lifespan": 2,
    "children": [],
    "peak_mass": 40.17311882993831,
    "dominant_channel": 1
  },
  "cf017fcc": {
    "parent": "779cbcd4",
    "generation": 1,
    "birth_frame": 4,
    "death_frame": 6,
    "lifespan": 2,
    "children": [],
    "peak_mass": 37.19243319030421,
    "dominant_channel": 1
  },
  "e8f00efa": {
    "parent": "779cbcd4",
    "generation": 1,
    "birth_frame": 4,
    "death_frame": 5,
    "lifespan": 1,
    "children": [],
    "peak_mass": 36.84970598418975,
    "dominant_channel": 1
  },
  "b8a14d0c": {
    "parent": "779cbcd4",
    "generation": 1,
    "birth_frame": 4,
    "death_frame": 5,
    "lifespan": 1,
    "children": [
      "0111bf94"
    ],
    "peak_mass": 31.482700826053204,
    "dominant_channel": 1
  },
  "15c27031": {
    "parent": "05d8b901",
    "generation": 2,
    "birth_frame": 5,
    "death_frame": 6,
    "lifespan": 1,
    "children": [],
    "peak_mass": 27.180208073908844,
    "dominant_channel": 1
  },
  "49ab7afc": {
    "parent": "05d8b901",
    "generation": 2,
    "birth_frame": 5,
    "death_frame": 6,
    "lifespan": 1,
    "children": [],
    "peak_mass": 19.362689197482048,
    "dominant_channel": 2
  },
  "0111bf94": {
    "parent": "b8a14d0c",
    "generation": 2,
    "birth_frame": 5,
    "death_frame": 6,
    "lifespan": 1,
    "children": [],
    "peak_mass": 28.97140828624059,
    "dominant_channel": 1
  },
  "88689195": {
    "parent": "05d8b901",
    "generation": 2,
    "birth_frame": 6,
    "death_frame": 7,
    "lifespan": 1,
    "children": [],
    "peak_mass": 45.24939597146353,
    "dominant_channel": 1
  },
  "47fbd0a9": {
    "parent": "05d8b901",
    "generation": 2,
    "birth_frame": 6,
    "death_frame": 7,
    "lifespan": 1,
    "children": [],
    "peak_mass": 30.939926076996677,
    "dominant_channel": 1
  },
  "4ea735bf": {
    "parent": "05d8b901",
    "generation": 2,
    "birth_frame": 6,
    "death_frame": 7,
    "lifespan": 1,
    "children": [],
    "peak_mass": 16.301152018937533,
    "dominant_channel": 2
  },
  "0a4e28bc": {
    "parent": "05d8b901",
    "generation": 2,
    "birth_frame": 7,
    "death_frame": 8,
    "lifespan": 1,
    "children": [],
    "peak_mass": 106.16661891669867,
    "dominant_channel": 1
  },
  "947f8726": {
    "parent": "05d8b901",
    "generation": 2,
    "birth_frame": 7,
    "death_frame": 8,
    "lifespan": 1,
    "children": [],
    "peak_mass": 81.59078318038988,
    "dominant_channel": 1
  },
  "9ce13d96": {
    "parent": "05d8b901",
    "generation": 2,
    "birth_frame": 7,
    "death_frame": 10,
    "lifespan": 3,
    "children": [],
    "peak_mass": 871.0699579933398,
    "dominant_channel": 2
  },
  "cb791387": {
    "parent": "05d8b901",
    "generation": 2,
    "birth_frame": 7,
    "death_frame": 14,
    "lifespan": 7,
    "children": [
      "2a74ad87",
      "fe08a2cb",
      "d730eec0",
      "f5617c9e",
      "bb699a1c"
    ],
    "peak_mass": 1094.2511058747589,
    "dominant_channel": 2
  },
  "e33761e4": {
    "parent": "05d8b901",
    "generation": 2,
    "birth_frame": 7,
    "death_frame": 8,
    "lifespan": 1,
    "children": [],
    "peak_mass": 46.235276064079606,
    "dominant_channel": 2
  },
  "ba3a2f0c": {
    "parent": "05d8b901",
    "generation": 2,
    "birth_frame": 7,
    "death_frame": 10,
    "lifespan": 3,
    "children": [],
    "peak_mass": 387.2026693120729,
    "dominant_channel": 1
  },
  "4e978ab8": {
    "parent": "05d8b901",
    "generation": 2,
    "birth_frame": 7,
    "death_frame": 8,
    "lifespan": 1,
    "children": [],
    "peak_mass": 38.10065582173692,
    "dominant_channel": 1
  },
  "c74a8692": {
    "parent": "05d8b901",
    "generation": 2,
    "birth_frame": 7,
    "death_frame": 8,
    "lifespan": 1,
    "children": [],
    "peak_mass": 27.649625425391147,
    "dominant_channel": 1
  },
  "1b247b12": {
    "parent": "05d8b901",
    "generation": 2,
    "birth_frame": 7,
    "death_frame": 8,
    "lifespan": 1,
    "children": [],
    "peak_mass": 26.209143985032092,
    "dominant_channel": 2
  },
  "ff4e97e4": {
    "parent": "05d8b901",
    "generation": 2,
    "birth_frame": 8,
    "death_frame": 9,
    "lifespan": 1,
    "children": [],
    "peak_mass": 327.7666578503941,
    "dominant_channel": 1
  },
  "043678a9": {
    "parent": "05d8b901",
    "generation": 2,
    "birth_frame": 8,
    "death_frame": 9,
    "lifespan": 1,
    "children": [
      "1183791c"
    ],
    "peak_mass": 321.6807573665928,
    "dominant_channel": 1
  },
  "ed34b6a3": {
    "parent": "05d8b901",
    "generation": 2,
    "birth_frame": 8,
    "death_frame": 9,
    "lifespan": 1,
    "children": [
      "77a9a30f"
    ],
    "peak_mass": 188.37305889952788,
    "dominant_channel": 1
  },
  "af6b78be": {
    "parent": null,
    "generation": 0,
    "birth_frame": 8,
    "death_frame": 9,
    "lifespan": 1,
    "children": [],
    "peak_mass": 30.48819259099311,
    "dominant_channel": 1
  },
  "9e6ea40e": {
    "parent": null,
    "generation": 0,
    "birth_frame": 8,
    "death_frame": 9,
    "lifespan": 1,
    "children": [],
    "peak_mass": 16.65850330356544,
    "dominant_channel": 1
  },
  "736b8f2a": {
    "parent": null,
    "generation": 0,
    "birth_frame": 8,
    "death_frame": 9,
    "lifespan": 1,
    "children": [],
    "peak_mass": 47.0843184693746,
    "dominant_channel": 1
  },
  "38c1d66e": {
    "parent": null,
    "generation": 0,
    "birth_frame": 8,
    "death_frame": 10,
    "lifespan": 2,
    "children": [],
    "peak_mass": 32.150338410453884,
    "dominant_channel": 1
  },
  "e299d3f7": {
    "parent": null,
    "generation": 0,
    "birth_frame": 8,
    "death_frame": 10,
    "lifespan": 2,
    "children": [],
    "peak_mass": 34.07551386874435,
    "dominant_channel": 1
  },
  "c94d9464": {
    "parent": null,
    "generation": 0,
    "birth_frame": 8,
    "death_frame": 9,
    "lifespan": 1,
    "children": [],
    "peak_mass": 17.452308025589424,
    "dominant_channel": 2
  },
  "77a9a30f": {
    "parent": "ed34b6a3",
    "generation": 3,
    "birth_frame": 9,
    "death_frame": 10,
    "lifespan": 1,
    "children": [],
    "peak_mass": 55.22134612790225,
    "dominant_channel": 1
  },
  "1183791c": {
    "parent": "043678a9",
    "generation": 3,
    "birth_frame": 9,
    "death_frame": 12,
    "lifespan": 3,
    "children": [
      "255f882b",
      "df8741b3"
    ],
    "peak_mass": 450.1670620982352,
    "dominant_channel": 1
  },
  "a5577242": {
    "parent": null,
    "generation": 0,
    "birth_frame": 9,
    "death_frame": 10,
    "lifespan": 1,
    "children": [],
    "peak_mass": 38.737511372064105,
    "dominant_channel": 1
  },
  "b6ce01e8": {
    "parent": null,
    "generation": 0,
    "birth_frame": 9,
    "death_frame": 10,
    "lifespan": 1,
    "children": [],
    "peak_mass": 19.417713490491792,
    "dominant_channel": 1
  },
  "b3a0451e": {
    "parent": null,
    "generation": 0,
    "birth_frame": 9,
    "death_frame": 10,
    "lifespan": 1,
    "children": [],
    "peak_mass": 18.801981365164206,
    "dominant_channel": 2
  },
  "e2d7a4dd": {
    "parent": null,
    "generation": 0,
    "birth_frame": 9,
    "death_frame": 11,
    "lifespan": 2,
    "children": [],
    "peak_mass": 31.641751238270334,
    "dominant_channel": 0
  },
  "255f882b": {
    "parent": "1183791c",
    "generation": 4,
    "birth_frame": 10,
    "death_frame": 11,
    "lifespan": 1,
    "children": [
      "ef1f3d57"
    ],
    "peak_mass": 63.711021639018,
    "dominant_channel": 1
  },
  "df8741b3": {
    "parent": "1183791c",
    "generation": 4,
    "birth_frame": 10,
    "death_frame": 12,
    "lifespan": 2,
    "children": [],
    "peak_mass": 53.70386634411046,
    "dominant_channel": 1
  }
}
```

## Media

- `outputs/SPECIES_029_BIFIDA_final.png`
- `outputs/SPECIES_029_BIFIDA.gif`
- note: ffmpeg not on PATH; GIF written instead

- genome: `outputs/species/SPECIES_029_BIFIDA_genome.json`
