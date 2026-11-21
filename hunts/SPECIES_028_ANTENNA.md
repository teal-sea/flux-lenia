# SPECIES 028 — ANTENNA

**Verdict:** VIABLE + REPRODUCING
**Origin:** random  |  **Seed:** 929

## Viability gates

| gate | verdict | value | detail |
| --- | --- | --- | --- |
| mass_conservation | PASS | 2.21203e-16 | tol=0.0001 |
| non_triviality | PASS | 34.5237 | conc>=6.0, occupancy 0.098<=0.45, 4 bodies |
| persistence | PASS | 1 | 1 organisms alive at the end with lifespan >= 15 frames |
| activity | PASS | 4.29035 | mean speed of the most mobile organism, cells/frame |

## Behaviour (anomaly bouncer)

| behaviour | established | score | evidence |
| --- | --- | --- | --- |
| phototaxis | no | -0.004 | lamp(26, 64): 38.4->38.1; lamp(102, 64): 38.4->38.6; lamp(64, 26): 38.4->38.2 | min approach -0.004 (needs > 0.05 for every lamp position) |
| predatory_pursuit | no | 0.223 | aefb4c3f(ch2) -> b7595571(ch1) closed 49.8 -> 24.9 cells over 19 frames, monotone 0.44, target speed 1.790 |
| cyclic_locomotion | no | 0.359 | uid=b7595571 circling=0.22 spectral_power=0.12 period=6.3 frames (counted only if >= 4) life=20 frames |

## Reproduction

Measured on the recording run below (the screening run is sampled more coarsely and its counts differ; both are stated separately rather than mixed).

- Divisions counted (offspring survived AND carried at least 10% of the parent's mass): **4**
- Raw fission events before the mass filter: **17** — the difference is debris a large body shed, which is not reproduction
- Surviving offspring total: **4**
- Organisms tracked in this run: **94**
- Screening run, for comparison: 1 divisions of 6 raw fissions, deepest generation 5

| frame | parent | children | parent mass | child masses | child share |
| --- | --- | --- | --- | --- | --- |
| 88 | `cf02c8ba` | `2a21f9c9` | 30.3 | 8.0 | 26% |
| 105 | `a744196a` | `5829e0fd` | 12.7 | 6.3 | 50% |
| 116 | `d753aa51` | `913cb5b5` | 7.7 | 7.6 | 98% |
| 138 | `11a5de9a` | `ebb1ceff` | 8.7 | 4.9 | 57% |

## Complexity

```json
{
  "morph_diversity": 3.202049071399505,
  "spatial_mi": 1.5182933754570729,
  "cross_channel_mi": 1.059778419672023,
  "euler_final": 18,
  "concentration_final": 34.52367881357827,
  "occupancy_final": 0.09832763671875,
  "n_blobs_final": 4,
  "activity": 4.290353562532534,
  "mass_drift": 2.2120265042043332e-16,
  "score": 15.92574683024068
}
```

## Lineage tree

```json
{
  "816c74f9": {
    "parent": null,
    "generation": 0,
    "birth_frame": 0,
    "death_frame": 77,
    "lifespan": 77,
    "children": [
      "ab8a175e",
      "a61e1deb",
      "168a61d1",
      "bde23b92",
      "f3a05321",
      "4f003444",
      "737ab305",
      "f6e04954",
      "ae957c47",
      "23c4ac72",
      "62803143",
      "9545e699"
    ],
    "peak_mass": 2041.6914574487105,
    "dominant_channel": 1
  },
  "0b90d2f0": {
    "parent": null,
    "generation": 0,
    "birth_frame": 26,
    "death_frame": 27,
    "lifespan": 1,
    "children": [],
    "peak_mass": 8.92178406950447,
    "dominant_channel": 1
  },
  "ab8a175e": {
    "parent": "816c74f9",
    "generation": 1,
    "birth_frame": 34,
    "death_frame": 35,
    "lifespan": 1,
    "children": [],
    "peak_mass": 6.474418222539295,
    "dominant_channel": 2
  },
  "a61e1deb": {
    "parent": "816c74f9",
    "generation": 1,
    "birth_frame": 46,
    "death_frame": 47,
    "lifespan": 1,
    "children": [
      "f7b40c1e"
    ],
    "peak_mass": 11.160957133183437,
    "dominant_channel": 0
  },
  "35e596a0": {
    "parent": null,
    "generation": 0,
    "birth_frame": 46,
    "death_frame": 47,
    "lifespan": 1,
    "children": [],
    "peak_mass": 8.841543839915362,
    "dominant_channel": 2
  },
  "f7b40c1e": {
    "parent": "a61e1deb",
    "generation": 2,
    "birth_frame": 47,
    "death_frame": 48,
    "lifespan": 1,
    "children": [],
    "peak_mass": 8.708802141380179,
    "dominant_channel": 0
  },
  "168a61d1": {
    "parent": "816c74f9",
    "generation": 1,
    "birth_frame": 55,
    "death_frame": 56,
    "lifespan": 1,
    "children": [],
    "peak_mass": 6.688510568693344,
    "dominant_channel": 0
  },
  "bde23b92": {
    "parent": "816c74f9",
    "generation": 1,
    "birth_frame": 59,
    "death_frame": 63,
    "lifespan": 4,
    "children": [],
    "peak_mass": 14.210450309473405,
    "dominant_channel": 2
  },
  "d85d8c5a": {
    "parent": null,
    "generation": 0,
    "birth_frame": 60,
    "death_frame": 61,
    "lifespan": 1,
    "children": [],
    "peak_mass": 4.858964103452973,
    "dominant_channel": 2
  },
  "f3a05321": {
    "parent": "816c74f9",
    "generation": 1,
    "birth_frame": 61,
    "death_frame": 62,
    "lifespan": 1,
    "children": [],
    "peak_mass": 6.448854914534353,
    "dominant_channel": 2
  },
  "4f003444": {
    "parent": "816c74f9",
    "generation": 1,
    "birth_frame": 64,
    "death_frame": 66,
    "lifespan": 2,
    "children": [],
    "peak_mass": 8.30852306738349,
    "dominant_channel": 2
  },
  "5acb2cc7": {
    "parent": null,
    "generation": 0,
    "birth_frame": 64,
    "death_frame": 65,
    "lifespan": 1,
    "children": [],
    "peak_mass": 5.948215790075114,
    "dominant_channel": 2
  },
  "737ab305": {
    "parent": "816c74f9",
    "generation": 1,
    "birth_frame": 65,
    "death_frame": 66,
    "lifespan": 1,
    "children": [],
    "peak_mass": 9.159236623837911,
    "dominant_channel": 2
  },
  "f6e04954": {
    "parent": "816c74f9",
    "generation": 1,
    "birth_frame": 67,
    "death_frame": 68,
    "lifespan": 1,
    "children": [],
    "peak_mass": 7.3580087169494295,
    "dominant_channel": 2
  },
  "ae957c47": {
    "parent": "816c74f9",
    "generation": 1,
    "birth_frame": 67,
    "death_frame": 71,
    "lifespan": 4,
    "children": [],
    "peak_mass": 8.067196979099595,
    "dominant_channel": 2
  },
  "23c4ac72": {
    "parent": "816c74f9",
    "generation": 1,
    "birth_frame": 70,
    "death_frame": 84,
    "lifespan": 14,
    "children": [],
    "peak_mass": 9.157488745554991,
    "dominant_channel": 2
  },
  "62803143": {
    "parent": "816c74f9",
    "generation": 1,
    "birth_frame": 72,
    "death_frame": 75,
    "lifespan": 3,
    "children": [
      "eb17c16d"
    ],
    "peak_mass": 11.724375612652933,
    "dominant_channel": 2
  },
  "9545e699": {
    "parent": "816c74f9",
    "generation": 1,
    "birth_frame": 75,
    "death_frame": 89,
    "lifespan": 14,
    "children": [
      "bc5b6d50",
      "fc40e06d",
      "de62047c",
      "0eea8721",
      "cf02c8ba",
      "c497fd91",
      "28323478",
      "76b9b966",
      "1875f0e7",
      "2aadba5c"
    ],
    "peak_mass": 1856.6057383149282,
    "dominant_channel": 1
  },
  "eb17c16d": {
    "parent": "62803143",
    "generation": 2,
    "birth_frame": 75,
    "death_frame": 76,
    "lifespan": 1,
    "children": [],
    "peak_mass": 5.578845945852552,
    "dominant_channel": 2
  },
  "17858835": {
    "parent": null,
    "generation": 0,
    "birth_frame": 77,
    "death_frame": 79,
    "lifespan": 2,
    "children": [],
    "peak_mass": 10.757877006955177,
    "dominant_channel": 2
  },
  "bc5b6d50": {
    "parent": "9545e699",
    "generation": 2,
    "birth_frame": 78,
    "death_frame": 79,
    "lifespan": 1,
    "children": [],
    "peak_mass": 7.893205376653882,
    "dominant_channel": 2
  },
  "b8a56841": {
    "parent": null,
    "generation": 0,
    "birth_frame": 78,
    "death_frame": 79,
    "lifespan": 1,
    "children": [],
    "peak_mass": 4.8923927560898335,
    "dominant_channel": 2
  },
  "fc40e06d": {
    "parent": "9545e699",
    "generation": 2,
    "birth_frame": 79,
    "death_frame": 81,
    "lifespan": 2,
    "children": [
      "bca6fc48"
    ],
    "peak_mass": 36.797156729080356,
    "dominant_channel": 2
  },
  "de62047c": {
    "parent": "9545e699",
    "generation": 2,
    "birth_frame": 80,
    "death_frame": 83,
    "lifespan": 3,
    "children": [],
    "peak_mass": 8.47956971172591,
    "dominant_channel": 0
  },
  "bca6fc48": {
    "parent": "fc40e06d",
    "generation": 3,
    "birth_frame": 80,
    "death_frame": 82,
    "lifespan": 2,
    "children": [],
    "peak_mass": 5.578442714178543,
    "dominant_channel": 2
  },
  "0eea8721": {
    "parent": "9545e699",
    "generation": 2,
    "birth_frame": 85,
    "death_frame": 87,
    "lifespan": 2,
    "children": [],
    "peak_mass": 8.667231855446563,
    "dominant_channel": 1
  },
  "cf02c8ba": {
    "parent": "9545e699",
    "generation": 2,
    "birth_frame": 86,
    "death_frame": 89,
    "lifespan": 3,
    "children": [
      "01fec0f8",
      "2a21f9c9"
    ],
    "peak_mass": 51.33084373507441,
    "dominant_channel": 2
  },
  "c497fd91": {
    "parent": "9545e699",
    "generation": 2,
    "birth_frame": 86,
    "death_frame": 99,
    "lifespan": 13,
    "children": [
      "8689303c"
    ],
    "peak_mass": 21.54696255546276,
    "dominant_channel": 2
  },
  "01fec0f8": {
    "parent": "cf02c8ba",
    "generation": 3,
    "birth_frame": 87,
    "death_frame": 88,
    "lifespan": 1,
    "children": [],
    "peak_mass": 6.2608953558399785,
    "dominant_channel": 2
  },
  "8689303c": {
    "parent": "c497fd91",
    "generation": 3,
    "birth_frame": 87,
    "death_frame": 92,
    "lifespan": 5,
    "children": [],
    "peak_mass": 7.586636412817699,
    "dominant_channel": 2
  },
  "2a21f9c9": {
    "parent": "cf02c8ba",
    "generation": 3,
    "birth_frame": 88,
    "death_frame": 99,
    "lifespan": 11,
    "children": [],
    "peak_mass": 10.88712251140609,
    "dominant_channel": 2
  },
  "28323478": {
    "parent": "9545e699",
    "generation": 2,
    "birth_frame": 88,
    "death_frame": 112,
    "lifespan": 24,
    "children": [
      "5d048e1e",
      "ed5b4d5c",
      "ef46a2a7",
      "d7ef549f",
      "93f5f5e5",
      "67816df8",
      "349c44d5",
      "6498a752",
      "a744196a",
      "0a55fb82",
      "d753aa51",
      "2d056661",
      "443fbf42",
      "81780dc5",
      "fa662be5",
      "a1d49123"
    ],
    "peak_mass": 1798.9519398344862,
    "dominant_channel": 1
  },
  "76b9b966": {
    "parent": "9545e699",
    "generation": 2,
    "birth_frame": 88,
    "death_frame": 96,
    "lifespan": 8,
    "children": [
      "6d5a6e04"
    ],
    "peak_mass": 23.730037078112712,
    "dominant_channel": 2
  },
  "1875f0e7": {
    "parent": "9545e699",
    "generation": 2,
    "birth_frame": 88,
    "death_frame": 89,
    "lifespan": 1,
    "children": [],
    "peak_mass": 6.410075922875102,
    "dominant_channel": 2
  },
  "2aadba5c": {
    "parent": "9545e699",
    "generation": 2,
    "birth_frame": 89,
    "death_frame": 90,
    "lifespan": 1,
    "children": [],
    "peak_mass": 9.569541773327595,
    "dominant_channel": 1
  },
  "241403d4": {
    "parent": null,
    "generation": 0,
    "birth_frame": 89,
    "death_frame": 91,
    "lifespan": 2,
    "children": [],
    "peak_mass": 6.173639629273814,
    "dominant_channel": 2
  },
  "6d5a6e04": {
    "parent": "76b9b966",
    "generation": 3,
    "birth_frame": 90,
    "death_frame": 92,
    "lifespan": 2,
    "children": [],
    "peak_mass": 6.640991552369177,
    "dominant_channel": 2
  },
  "5d048e1e": {
    "parent": "28323478",
    "generation": 3,
    "birth_frame": 91,
    "death_frame": 92,
    "lifespan": 1,
    "children": [],
    "peak_mass": 10.707517897644564,
    "dominant_channel": 2
  },
  "ed5b4d5c": {
    "parent": "28323478",
    "generation": 3,
    "birth_frame": 91,
    "death_frame": 92,
    "lifespan": 1,
    "children": [],
    "peak_mass": 7.484245469068783,
    "dominant_channel": 2
  },
  "ef46a2a7": {
    "parent": "28323478",
    "generation": 3,
    "birth_frame": 95,
    "death_frame": 96,
    "lifespan": 1,
    "children": [],
    "peak_mass": 11.177592628493768,
    "dominant_channel": 2
  }
}
```

## Media

- `outputs/SPECIES_028_ANTENNA_final.png`
- `outputs/SPECIES_028_ANTENNA.gif`
- note: ffmpeg not on PATH; GIF written instead

- genome: `outputs/species/SPECIES_028_ANTENNA_genome.json`
