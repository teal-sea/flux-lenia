# SPECIES 026 — YGGRA

**Verdict:** VIABLE + REPRODUCING
**Origin:** random  |  **Seed:** 896

## Viability gates

| gate | verdict | value | detail |
| --- | --- | --- | --- |
| mass_conservation | PASS | 1.31754e-16 | tol=0.0001 |
| non_triviality | PASS | 29.1209 | conc>=6.0, occupancy 0.138<=0.45, 12 bodies |
| persistence | PASS | 1 | 1 organisms alive at the end with lifespan >= 15 frames |
| activity | PASS | 2.61601 | mean speed of the most mobile organism, cells/frame |

## Behaviour (anomaly bouncer)

| behaviour | established | score | evidence |
| --- | --- | --- | --- |
| phototaxis | no | 0.001 | lamp(26, 64): 38.4->38.3; lamp(102, 64): 38.4->38.1; lamp(64, 26): 38.5->38.1 | min approach +0.001 (needs > 0.05 for every lamp position) |
| predatory_pursuit | no | 0.334 | 416ea458(ch1) -> b54d2f85(ch0) closed 59.2 -> 25.8 cells over 23 frames, monotone 0.59, target speed 1.648 |
| cyclic_locomotion | no | 0.492 | uid=691a8164 circling=0.09 spectral_power=0.16 period=5.8 frames (counted only if >= 4) life=24 frames |

## Reproduction

Measured on the recording run below (the screening run is sampled more coarsely and its counts differ; both are stated separately rather than mixed).

- Divisions counted (offspring survived AND carried at least 10% of the parent's mass): **8**
- Raw fission events before the mass filter: **17** — the difference is debris a large body shed, which is not reproduction
- Surviving offspring total: **8**
- Organisms tracked in this run: **166**
- Screening run, for comparison: 2 divisions of 6 raw fissions, deepest generation 3

| frame | parent | children | parent mass | child masses | child share |
| --- | --- | --- | --- | --- | --- |
| 80 | `74c1dd82` | `9cda6657` | 18.2 | 10.4 | 57% |
| 81 | `d71d32b1` | `4814a9d6` | 51.7 | 10.9 | 21% |
| 83 | `d71d32b1` | `4c8f384f` | 33.9 | 19.1 | 56% |
| 90 | `31eb0894` | `2f7683ef` | 54.1 | 23.7 | 44% |
| 93 | `785ff579` | `c264acd6` | 48.1 | 23.0 | 48% |
| 102 | `464c25cb` | `19f4d900` | 18.6 | 10.4 | 56% |
| 117 | `1b52c045` | `acfc4c30` | 10.0 | 9.0 | 90% |
| 128 | `acfc4c30` | `b54d2f85` | 22.5 | 19.0 | 84% |

## Complexity

```json
{
  "morph_diversity": 2.9491864577521,
  "spatial_mi": 1.4595106339976565,
  "cross_channel_mi": 0.907653858865965,
  "euler_final": 173,
  "concentration_final": 29.12093562212188,
  "occupancy_final": 0.1380615234375,
  "n_blobs_final": 12,
  "activity": 2.616006318393727,
  "mass_drift": 1.3175355846687336e-16,
  "score": 24.77655281654052
}
```

## Lineage tree

```json
{
  "2adf827f": {
    "parent": null,
    "generation": 0,
    "birth_frame": 0,
    "death_frame": 60,
    "lifespan": 60,
    "children": [
      "3aa48e9e",
      "7ed91e72",
      "27feb32d",
      "5238167d",
      "e0f4f0a0",
      "428720c0",
      "47428492"
    ],
    "peak_mass": 3428.702951263402,
    "dominant_channel": 0
  },
  "3aa48e9e": {
    "parent": "2adf827f",
    "generation": 1,
    "birth_frame": 56,
    "death_frame": 58,
    "lifespan": 2,
    "children": [
      "aeb42e5b"
    ],
    "peak_mass": 25.07491983202627,
    "dominant_channel": 0
  },
  "7ed91e72": {
    "parent": "2adf827f",
    "generation": 1,
    "birth_frame": 57,
    "death_frame": 58,
    "lifespan": 1,
    "children": [],
    "peak_mass": 7.995516258679864,
    "dominant_channel": 0
  },
  "aeb42e5b": {
    "parent": "3aa48e9e",
    "generation": 2,
    "birth_frame": 57,
    "death_frame": 58,
    "lifespan": 1,
    "children": [],
    "peak_mass": 8.853833449265014,
    "dominant_channel": 0
  },
  "ba75ca42": {
    "parent": null,
    "generation": 0,
    "birth_frame": 58,
    "death_frame": 59,
    "lifespan": 1,
    "children": [],
    "peak_mass": 6.044145854609398,
    "dominant_channel": 1
  },
  "27feb32d": {
    "parent": "2adf827f",
    "generation": 1,
    "birth_frame": 59,
    "death_frame": 62,
    "lifespan": 3,
    "children": [
      "179756a7",
      "d8eec7bf",
      "eb6aa97f",
      "64e90abc"
    ],
    "peak_mass": 2751.2141821117193,
    "dominant_channel": 0
  },
  "5238167d": {
    "parent": "2adf827f",
    "generation": 1,
    "birth_frame": 59,
    "death_frame": 60,
    "lifespan": 1,
    "children": [],
    "peak_mass": 63.856678927282516,
    "dominant_channel": 1
  },
  "e0f4f0a0": {
    "parent": "2adf827f",
    "generation": 1,
    "birth_frame": 59,
    "death_frame": 60,
    "lifespan": 1,
    "children": [],
    "peak_mass": 47.198380869468295,
    "dominant_channel": 1
  },
  "428720c0": {
    "parent": "2adf827f",
    "generation": 1,
    "birth_frame": 59,
    "death_frame": 60,
    "lifespan": 1,
    "children": [],
    "peak_mass": 27.867001254950125,
    "dominant_channel": 0
  },
  "47428492": {
    "parent": "2adf827f",
    "generation": 1,
    "birth_frame": 59,
    "death_frame": 60,
    "lifespan": 1,
    "children": [],
    "peak_mass": 13.986513437180356,
    "dominant_channel": 1
  },
  "e5ca03e3": {
    "parent": null,
    "generation": 0,
    "birth_frame": 60,
    "death_frame": 61,
    "lifespan": 1,
    "children": [],
    "peak_mass": 7.713640985414267,
    "dominant_channel": 0
  },
  "4681bf04": {
    "parent": null,
    "generation": 0,
    "birth_frame": 60,
    "death_frame": 61,
    "lifespan": 1,
    "children": [],
    "peak_mass": 11.33401244589285,
    "dominant_channel": 1
  },
  "57d164df": {
    "parent": null,
    "generation": 0,
    "birth_frame": 60,
    "death_frame": 61,
    "lifespan": 1,
    "children": [],
    "peak_mass": 7.092368540580248,
    "dominant_channel": 1
  },
  "179756a7": {
    "parent": "27feb32d",
    "generation": 2,
    "birth_frame": 61,
    "death_frame": 67,
    "lifespan": 6,
    "children": [
      "ab961cd1",
      "d37d04af",
      "43e7f74b",
      "88797cff"
    ],
    "peak_mass": 3114.5950301129797,
    "dominant_channel": 0
  },
  "d8eec7bf": {
    "parent": "27feb32d",
    "generation": 2,
    "birth_frame": 61,
    "death_frame": 62,
    "lifespan": 1,
    "children": [],
    "peak_mass": 29.1521447075588,
    "dominant_channel": 0
  },
  "eb6aa97f": {
    "parent": "27feb32d",
    "generation": 2,
    "birth_frame": 61,
    "death_frame": 62,
    "lifespan": 1,
    "children": [],
    "peak_mass": 19.791659515438603,
    "dominant_channel": 1
  },
  "64e90abc": {
    "parent": "27feb32d",
    "generation": 2,
    "birth_frame": 61,
    "death_frame": 62,
    "lifespan": 1,
    "children": [],
    "peak_mass": 15.231086999488303,
    "dominant_channel": 1
  },
  "3dc42b53": {
    "parent": null,
    "generation": 0,
    "birth_frame": 62,
    "death_frame": 64,
    "lifespan": 2,
    "children": [],
    "peak_mass": 12.86143081626387,
    "dominant_channel": 1
  },
  "ab961cd1": {
    "parent": "179756a7",
    "generation": 3,
    "birth_frame": 63,
    "death_frame": 64,
    "lifespan": 1,
    "children": [],
    "peak_mass": 14.576438346463355,
    "dominant_channel": 1
  },
  "d37d04af": {
    "parent": "179756a7",
    "generation": 3,
    "birth_frame": 63,
    "death_frame": 64,
    "lifespan": 1,
    "children": [],
    "peak_mass": 8.462604737993356,
    "dominant_channel": 1
  },
  "43e7f74b": {
    "parent": "179756a7",
    "generation": 3,
    "birth_frame": 64,
    "death_frame": 65,
    "lifespan": 1,
    "children": [],
    "peak_mass": 12.907455765599735,
    "dominant_channel": 0
  },
  "88797cff": {
    "parent": "179756a7",
    "generation": 3,
    "birth_frame": 64,
    "death_frame": 65,
    "lifespan": 1,
    "children": [],
    "peak_mass": 11.492488917701571,
    "dominant_channel": 1
  },
  "8a5a1590": {
    "parent": null,
    "generation": 0,
    "birth_frame": 65,
    "death_frame": 70,
    "lifespan": 5,
    "children": [
      "a06f4edb",
      "d6690b4f"
    ],
    "peak_mass": 3242.9043957965746,
    "dominant_channel": 0
  },
  "98eef966": {
    "parent": null,
    "generation": 0,
    "birth_frame": 66,
    "death_frame": 67,
    "lifespan": 1,
    "children": [],
    "peak_mass": 7.173790623027399,
    "dominant_channel": 1
  },
  "a06f4edb": {
    "parent": "8a5a1590",
    "generation": 1,
    "birth_frame": 69,
    "death_frame": 74,
    "lifespan": 5,
    "children": [
      "7b1c5fcd"
    ],
    "peak_mass": 3323.11144159404,
    "dominant_channel": 0
  },
  "d6690b4f": {
    "parent": "8a5a1590",
    "generation": 1,
    "birth_frame": 69,
    "death_frame": 70,
    "lifespan": 1,
    "children": [],
    "peak_mass": 7.653418497548618,
    "dominant_channel": 1
  },
  "7b1c5fcd": {
    "parent": "a06f4edb",
    "generation": 2,
    "birth_frame": 72,
    "death_frame": 78,
    "lifespan": 6,
    "children": [
      "43a59f18",
      "96a4171b",
      "ed7d6284",
      "123929df",
      "d6810121",
      "bbc25497",
      "4a2c5710",
      "25fa79cd",
      "3974a656",
      "373c875b",
      "339320b4",
      "73c6ba85",
      "860a4a44"
    ],
    "peak_mass": 3105.1599798697616,
    "dominant_channel": 0
  },
  "43a59f18": {
    "parent": "7b1c5fcd",
    "generation": 3,
    "birth_frame": 75,
    "death_frame": 77,
    "lifespan": 2,
    "children": [],
    "peak_mass": 20.541552928000097,
    "dominant_channel": 1
  },
  "96a4171b": {
    "parent": "7b1c5fcd",
    "generation": 3,
    "birth_frame": 77,
    "death_frame": 78,
    "lifespan": 1,
    "children": [],
    "peak_mass": 75.6352814432125,
    "dominant_channel": 1
  },
  "ed7d6284": {
    "parent": "7b1c5fcd",
    "generation": 3,
    "birth_frame": 77,
    "death_frame": 78,
    "lifespan": 1,
    "children": [],
    "peak_mass": 59.96050042597632,
    "dominant_channel": 1
  },
  "123929df": {
    "parent": "7b1c5fcd",
    "generation": 3,
    "birth_frame": 77,
    "death_frame": 84,
    "lifespan": 7,
    "children": [
      "fdfdbe7e",
      "74c1dd82",
      "42305daf",
      "cae993a6",
      "0c6bcd1c",
      "52bd18b6",
      "028c0b89",
      "8a1c00df",
      "74552b0a",
      "255e2b0d",
      "98ba6944",
      "d71d32b1",
      "31eb0894",
      "47563f61",
      "ca961b63",
      "c39cf239",
      "e3e93d8e",
      "b1f8e752"
    ],
    "peak_mass": 3001.377787801302,
    "dominant_channel": 0
  },
  "d6810121": {
    "parent": "7b1c5fcd",
    "generation": 3,
    "birth_frame": 77,
    "death_frame": 78,
    "lifespan": 1,
    "children": [],
    "peak_mass": 22.89883617581694,
    "dominant_channel": 1
  },
  "bbc25497": {
    "parent": "7b1c5fcd",
    "generation": 3,
    "birth_frame": 77,
    "death_frame": 78,
    "lifespan": 1,
    "children": [],
    "peak_mass": 19.801433849983734,
    "dominant_channel": 1
  },
  "4a2c5710": {
    "parent": "7b1c5fcd",
    "generation": 3,
    "birth_frame": 77,
    "death_frame": 78,
    "lifespan": 1,
    "children": [],
    "peak_mass": 18.959095924919826,
    "dominant_channel": 1
  },
  "25fa79cd": {
    "parent": "7b1c5fcd",
    "generation": 3,
    "birth_frame": 77,
    "death_frame": 78,
    "lifespan": 1,
    "children": [],
    "peak_mass": 18.450654881570376,
    "dominant_channel": 0
  },
  "3974a656": {
    "parent": "7b1c5fcd",
    "generation": 3,
    "birth_frame": 77,
    "death_frame": 78,
    "lifespan": 1,
    "children": [],
    "peak_mass": 16.117333702266297,
    "dominant_channel": 1
  },
  "373c875b": {
    "parent": "7b1c5fcd",
    "generation": 3,
    "birth_frame": 77,
    "death_frame": 78,
    "lifespan": 1,
    "children": [],
    "peak_mass": 11.533346872452082,
    "dominant_channel": 1
  },
  "339320b4": {
    "parent": "7b1c5fcd",
    "generation": 3,
    "birth_frame": 77,
    "death_frame": 78,
    "lifespan": 1,
    "children": [],
    "peak_mass": 11.323300950558808,
    "dominant_channel": 1
  },
  "73c6ba85": {
    "parent": "7b1c5fcd",
    "generation": 3,
    "birth_frame": 77,
    "death_frame": 78,
    "lifespan": 1,
    "children": [],
    "peak_mass": 8.94937912701808,
    "dominant_channel": 0
  },
  "860a4a44": {
    "parent": "7b1c5fcd",
    "generation": 3,
    "birth_frame": 77,
    "death_frame": 78,
    "lifespan": 1,
    "children": [],
    "peak_mass": 8.568267419845242,
    "dominant_channel": 1
  }
}
```

## Media

- `outputs/SPECIES_026_YGGRA_final.png`
- `outputs/SPECIES_026_YGGRA.gif`
- note: ffmpeg not on PATH; GIF written instead

- genome: `outputs/species/SPECIES_026_YGGRA_genome.json`
