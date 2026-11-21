# SPECIES 004 — CORONA

**Verdict:** VIABLE + REPRODUCING
**Origin:** random  |  **Seed:** 476

## Viability gates

| gate | verdict | value | detail |
| --- | --- | --- | --- |
| mass_conservation | PASS | 1.59271e-16 | tol=0.0001 |
| non_triviality | PASS | 18.552 | conc>=6.0, occupancy 0.201<=0.45, 5 bodies |
| persistence | PASS | 2 | 2 organisms alive at the end with lifespan >= 15 frames |
| activity | PASS | 1.21598 | mean speed of the most mobile organism, cells/frame |

## Behaviour (anomaly bouncer)

| behaviour | established | score | evidence |
| --- | --- | --- | --- |
| phototaxis | no | 0.002 | lamp(26, 64): 38.4->38.0; lamp(102, 64): 38.4->37.3; lamp(64, 26): 38.3->38.2 | min approach +0.002 (needs > 0.05 for every lamp position) |
| predatory_pursuit | no | 0.166 | 7c0391ba(ch1) -> 800cbca4(ch1) closed 66.7 -> 41.7 cells over 19 frames, monotone 0.44, target speed 2.001 |
| cyclic_locomotion | no | 0.400 | uid=7e168882 circling=0.40 spectral_power=0.04 period=2.1 frames (counted only if >= 4) life=62 frames |

## Reproduction

Measured on the recording run below (the screening run is sampled more coarsely and its counts differ; both are stated separately rather than mixed).

- Divisions counted (offspring survived AND carried at least 10% of the parent's mass): **1**
- Raw fission events before the mass filter: **8** — the difference is debris a large body shed, which is not reproduction
- Surviving offspring total: **1**
- Organisms tracked in this run: **109**
- Screening run, for comparison: 1 divisions of 2 raw fissions, deepest generation 6

| frame | parent | children | parent mass | child masses | child share |
| --- | --- | --- | --- | --- | --- |
| 96 | `ccf83eca` | `dd6ec91a` | 16.0 | 4.8 | 30% |

## Complexity

```json
{
  "morph_diversity": 3.2652857865412654,
  "spatial_mi": 1.3844726110336771,
  "cross_channel_mi": 0.6169240223141821,
  "euler_final": 112,
  "concentration_final": 18.5520232313689,
  "occupancy_final": 0.20135498046875,
  "n_blobs_final": 5,
  "activity": 1.2159810451864472,
  "mass_drift": 1.5927074963884647e-16,
  "score": 15.780216917423454
}
```

## Lineage tree

```json
{
  "e9664757": {
    "parent": null,
    "generation": 0,
    "birth_frame": 0,
    "death_frame": 73,
    "lifespan": 73,
    "children": [
      "7b5fcb8d",
      "aaca8805",
      "ff7020c1",
      "7f137b7c",
      "93e75c01",
      "59e68df8",
      "7e168882",
      "ceff7fdc",
      "c575f552"
    ],
    "peak_mass": 2834.820726114881,
    "dominant_channel": 0
  },
  "1484b087": {
    "parent": null,
    "generation": 0,
    "birth_frame": 48,
    "death_frame": 49,
    "lifespan": 1,
    "children": [],
    "peak_mass": 5.363147068189936,
    "dominant_channel": 0
  },
  "7b5fcb8d": {
    "parent": "e9664757",
    "generation": 1,
    "birth_frame": 62,
    "death_frame": 63,
    "lifespan": 1,
    "children": [],
    "peak_mass": 5.610436051915985,
    "dominant_channel": 0
  },
  "aaca8805": {
    "parent": "e9664757",
    "generation": 1,
    "birth_frame": 66,
    "death_frame": 67,
    "lifespan": 1,
    "children": [
      "2ca4088b"
    ],
    "peak_mass": 7.0556585770158735,
    "dominant_channel": 0
  },
  "ff7020c1": {
    "parent": "e9664757",
    "generation": 1,
    "birth_frame": 66,
    "death_frame": 67,
    "lifespan": 1,
    "children": [],
    "peak_mass": 5.879769283092004,
    "dominant_channel": 0
  },
  "2ca4088b": {
    "parent": "aaca8805",
    "generation": 2,
    "birth_frame": 67,
    "death_frame": 68,
    "lifespan": 1,
    "children": [],
    "peak_mass": 6.340520283395246,
    "dominant_channel": 0
  },
  "7f137b7c": {
    "parent": "e9664757",
    "generation": 1,
    "birth_frame": 68,
    "death_frame": 70,
    "lifespan": 2,
    "children": [],
    "peak_mass": 5.9861657660846666,
    "dominant_channel": 0
  },
  "93e75c01": {
    "parent": "e9664757",
    "generation": 1,
    "birth_frame": 69,
    "death_frame": 70,
    "lifespan": 1,
    "children": [],
    "peak_mass": 7.505070934926883,
    "dominant_channel": 0
  },
  "59e68df8": {
    "parent": "e9664757",
    "generation": 1,
    "birth_frame": 69,
    "death_frame": 70,
    "lifespan": 1,
    "children": [],
    "peak_mass": 6.939045814125323,
    "dominant_channel": 0
  },
  "7e168882": {
    "parent": "e9664757",
    "generation": 1,
    "birth_frame": 71,
    "death_frame": 133,
    "lifespan": 62,
    "children": [
      "0c54b610",
      "2acd1bc7",
      "34d10ec7",
      "54fcea33",
      "e76eafce",
      "b1252299",
      "9927750d",
      "909560c2",
      "f42d5e97",
      "ccf83eca",
      "0b2d84ff",
      "191cf7bf",
      "a3cc173a",
      "e1777437",
      "29f53a8a",
      "03bc69c1",
      "0f618ead",
      "4a21bd26",
      "a08fdeb1",
      "380b2b2f",
      "d6f79883",
      "4ce5207f",
      "ddf013a8",
      "33bb260c",
      "730033ea",
      "9e05f1f0",
      "ae5e4a41",
      "29ddf1ff",
      "7b69b74a",
      "3d62b115",
      "ba52d655",
      "912b513f",
      "f0e137a1",
      "d0fc8f21",
      "998e819b",
      "4c270957",
      "ac9d648c",
      "f2dc87fe",
      "b57594f8",
      "38c6fcb1",
      "2319515f",
      "800cbca4",
      "0896a083"
    ],
    "peak_mass": 2546.18050660903,
    "dominant_channel": 0
  },
  "c6bdadde": {
    "parent": null,
    "generation": 0,
    "birth_frame": 72,
    "death_frame": 73,
    "lifespan": 1,
    "children": [],
    "peak_mass": 6.098107052101359,
    "dominant_channel": 0
  },
  "0c54b610": {
    "parent": "7e168882",
    "generation": 2,
    "birth_frame": 73,
    "death_frame": 74,
    "lifespan": 1,
    "children": [],
    "peak_mass": 7.625278523745018,
    "dominant_channel": 0
  },
  "ceff7fdc": {
    "parent": "e9664757",
    "generation": 1,
    "birth_frame": 73,
    "death_frame": 77,
    "lifespan": 4,
    "children": [],
    "peak_mass": 7.787902046493903,
    "dominant_channel": 0
  },
  "c575f552": {
    "parent": "e9664757",
    "generation": 1,
    "birth_frame": 73,
    "death_frame": 75,
    "lifespan": 2,
    "children": [],
    "peak_mass": 6.129828439056447,
    "dominant_channel": 0
  },
  "8b80fc8b": {
    "parent": null,
    "generation": 0,
    "birth_frame": 74,
    "death_frame": 75,
    "lifespan": 1,
    "children": [],
    "peak_mass": 8.908374107238966,
    "dominant_channel": 0
  },
  "2acd1bc7": {
    "parent": "7e168882",
    "generation": 2,
    "birth_frame": 75,
    "death_frame": 76,
    "lifespan": 1,
    "children": [],
    "peak_mass": 35.65278940600973,
    "dominant_channel": 1
  },
  "34d10ec7": {
    "parent": "7e168882",
    "generation": 2,
    "birth_frame": 75,
    "death_frame": 77,
    "lifespan": 2,
    "children": [],
    "peak_mass": 33.57907902304114,
    "dominant_channel": 1
  },
  "54fcea33": {
    "parent": "7e168882",
    "generation": 2,
    "birth_frame": 78,
    "death_frame": 79,
    "lifespan": 1,
    "children": [
      "084f958b",
      "282fe0c4"
    ],
    "peak_mass": 30.3420384686779,
    "dominant_channel": 1
  },
  "e76eafce": {
    "parent": "7e168882",
    "generation": 2,
    "birth_frame": 78,
    "death_frame": 79,
    "lifespan": 1,
    "children": [],
    "peak_mass": 27.895484676649318,
    "dominant_channel": 1
  },
  "084f958b": {
    "parent": "54fcea33",
    "generation": 3,
    "birth_frame": 79,
    "death_frame": 85,
    "lifespan": 6,
    "children": [
      "9d85a2a5"
    ],
    "peak_mass": 16.06580958094365,
    "dominant_channel": 1
  },
  "282fe0c4": {
    "parent": "54fcea33",
    "generation": 3,
    "birth_frame": 79,
    "death_frame": 82,
    "lifespan": 3,
    "children": [],
    "peak_mass": 10.603545224226975,
    "dominant_channel": 1
  },
  "b1252299": {
    "parent": "7e168882",
    "generation": 2,
    "birth_frame": 80,
    "death_frame": 83,
    "lifespan": 3,
    "children": [
      "16f6828b"
    ],
    "peak_mass": 34.82368923688774,
    "dominant_channel": 1
  },
  "9927750d": {
    "parent": "7e168882",
    "generation": 2,
    "birth_frame": 80,
    "death_frame": 81,
    "lifespan": 1,
    "children": [],
    "peak_mass": 26.71191642074002,
    "dominant_channel": 1
  },
  "b70ca8dc": {
    "parent": null,
    "generation": 0,
    "birth_frame": 81,
    "death_frame": 82,
    "lifespan": 1,
    "children": [],
    "peak_mass": 5.824946537147242,
    "dominant_channel": 0
  },
  "4b4e24f2": {
    "parent": null,
    "generation": 0,
    "birth_frame": 81,
    "death_frame": 82,
    "lifespan": 1,
    "children": [],
    "peak_mass": 7.175771115039163,
    "dominant_channel": 0
  },
  "909560c2": {
    "parent": "7e168882",
    "generation": 2,
    "birth_frame": 82,
    "death_frame": 83,
    "lifespan": 1,
    "children": [],
    "peak_mass": 6.913635774837813,
    "dominant_channel": 0
  },
  "16f6828b": {
    "parent": "b1252299",
    "generation": 3,
    "birth_frame": 82,
    "death_frame": 85,
    "lifespan": 3,
    "children": [
      "189549c1"
    ],
    "peak_mass": 22.602869433662068,
    "dominant_channel": 1
  },
  "189549c1": {
    "parent": "16f6828b",
    "generation": 4,
    "birth_frame": 83,
    "death_frame": 84,
    "lifespan": 1,
    "children": [],
    "peak_mass": 4.982674268117351,
    "dominant_channel": 0
  },
  "1928c973": {
    "parent": null,
    "generation": 0,
    "birth_frame": 83,
    "death_frame": 85,
    "lifespan": 2,
    "children": [],
    "peak_mass": 7.6570577333288865,
    "dominant_channel": 0
  },
  "7eeb574e": {
    "parent": null,
    "generation": 0,
    "birth_frame": 84,
    "death_frame": 85,
    "lifespan": 1,
    "children": [],
    "peak_mass": 4.729652878427909,
    "dominant_channel": 0
  },
  "f42d5e97": {
    "parent": "7e168882",
    "generation": 2,
    "birth_frame": 85,
    "death_frame": 86,
    "lifespan": 1,
    "children": [],
    "peak_mass": 6.243197445224351,
    "dominant_channel": 0
  },
  "9d85a2a5": {
    "parent": "084f958b",
    "generation": 4,
    "birth_frame": 85,
    "death_frame": 89,
    "lifespan": 4,
    "children": [
      "7dcf0948"
    ],
    "peak_mass": 23.10871206312073,
    "dominant_channel": 1
  },
  "ccf83eca": {
    "parent": "7e168882",
    "generation": 2,
    "birth_frame": 86,
    "death_frame": 98,
    "lifespan": 12,
    "children": [
      "dd6ec91a"
    ],
    "peak_mass": 26.23192812614957,
    "dominant_channel": 1
  },
  "0b2d84ff": {
    "parent": "7e168882",
    "generation": 2,
    "birth_frame": 87,
    "death_frame": 88,
    "lifespan": 1,
    "children": [],
    "peak_mass": 6.360095416321992,
    "dominant_channel": 0
  },
  "7dcf0948": {
    "parent": "9d85a2a5",
    "generation": 5,
    "birth_frame": 89,
    "death_frame": 90,
    "lifespan": 1,
    "children": [],
    "peak_mass": 7.286890206697725,
    "dominant_channel": 1
  },
  "191cf7bf": {
    "parent": "7e168882",
    "generation": 2,
    "birth_frame": 90,
    "death_frame": 95,
    "lifespan": 5,
    "children": [
      "c61f71ed"
    ],
    "peak_mass": 29.289000537430123,
    "dominant_channel": 1
  },
  "4be6a520": {
    "parent": null,
    "generation": 0,
    "birth_frame": 90,
    "death_frame": 91,
    "lifespan": 1,
    "children": [],
    "peak_mass": 7.975161181122428,
    "dominant_channel": 0
  },
  "a3cc173a": {
    "parent": "7e168882",
    "generation": 2,
    "birth_frame": 91,
    "death_frame": 92,
    "lifespan": 1,
    "children": [],
    "peak_mass": 25.14589176257877,
    "dominant_channel": 1
  },
  "e1777437": {
    "parent": "7e168882",
    "generation": 2,
    "birth_frame": 91,
    "death_frame": 92,
    "lifespan": 1,
    "children": [],
    "peak_mass": 6.532917513463694,
    "dominant_channel": 0
  },
  "29f53a8a": {
    "parent": "7e168882",
    "generation": 2,
    "birth_frame": 91,
    "death_frame": 92,
    "lifespan": 1,
    "children": [],
    "peak_mass": 6.030878758424081,
    "dominant_channel": 0
  }
}
```

## Media

- `outputs/SPECIES_004_CORONA_final.png`
- `outputs/SPECIES_004_CORONA.gif`
- `outputs/SPECIES_004_CORONA.mp4`

- genome: `outputs/species/SPECIES_004_CORONA_genome.json`
