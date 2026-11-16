# SPECIES 030 — CATENA

**Verdict:** VIABLE + REPRODUCING
**Origin:** random  |  **Seed:** 976

## Viability gates

| gate | verdict | value | detail |
| --- | --- | --- | --- |
| mass_conservation | PASS | 1.24255e-16 | tol=0.0001 |
| non_triviality | PASS | 76.5143 | conc>=6.0, occupancy 0.031<=0.45, 10 bodies |
| persistence | PASS | 6 | 6 organisms alive at the end with lifespan >= 15 frames |
| activity | PASS | 2.42839 | mean speed of the most mobile organism, cells/frame |

## Behaviour (anomaly bouncer)

| behaviour | established | score | evidence |
| --- | --- | --- | --- |
| phototaxis | no | -0.025 | lamp(26, 64): 38.4->38.7; lamp(102, 64): 38.4->38.2; lamp(64, 26): 38.5->39.4 | min approach -0.025 (needs > 0.05 for every lamp position) |
| predatory_pursuit | no | 0.334 | fedbb9e4(ch0) -> 0ea59d4d(ch0) closed 26.4 -> 12.7 cells over 15 frames, monotone 0.64, target speed 1.952 |
| cyclic_locomotion | no | 0.564 | uid=993be70a circling=0.08 spectral_power=0.19 period=5.0 frames (counted only if >= 4) life=26 frames |

## Reproduction

Measured on the recording run below (the screening run is sampled more coarsely and its counts differ; both are stated separately rather than mixed).

- Divisions counted (offspring survived AND carried at least 10% of the parent's mass): **11**
- Raw fission events before the mass filter: **12** — the difference is debris a large body shed, which is not reproduction
- Surviving offspring total: **12**
- Organisms tracked in this run: **72**
- Screening run, for comparison: 7 divisions of 8 raw fissions, deepest generation 3

| frame | parent | children | parent mass | child masses | child share |
| --- | --- | --- | --- | --- | --- |
| 65 | `8d06654c` | `fedbb9e4` | 409.1 | 81.6 | 20% |
| 69 | `8b4a37ae` | `95278742` | 279.0 | 107.2 | 38% |
| 71 | `8b4a37ae` | `b65b01b9` | 95.9 | 95.2, 81.5 | 99% |
| 74 | `b65b01b9` | `c857058e` | 185.0 | 96.7 | 52% |
| 78 | `c857058e` | `c4b00f8f` | 281.6 | 109.7 | 39% |
| 80 | `c857058e` | `82e5264b` | 178.4 | 91.6 | 51% |
| 92 | `692046e0` | `0ea59d4d` | 181.0 | 107.5 | 59% |
| 96 | `0ea59d4d` | `63140a0b`, `185e997f` | 184.8 | 93.9, 19.4 | 51%, 10% |
| 101 | `0ea59d4d` | `d5a05744` | 85.6 | 79.4 | 93% |
| 108 | `63140a0b` | `61b879d0` | 92.6 | 83.0 | 90% |
| 123 | `fedbb9e4` | `baead1bb` | 82.9 | 79.8 | 96% |

## Complexity

```json
{
  "morph_diversity": 3.160575153653113,
  "spatial_mi": 1.4726012031306281,
  "cross_channel_mi": 0.8120298623701789,
  "euler_final": 33,
  "concentration_final": 76.51429280930076,
  "occupancy_final": 0.03070068359375,
  "n_blobs_final": 10,
  "activity": 2.42839282836326,
  "mass_drift": 1.242553662756311e-16,
  "score": 47.539086257536184
}
```

## Lineage tree

```json
{
  "8b4a37ae": {
    "parent": null,
    "generation": 0,
    "birth_frame": 0,
    "death_frame": 72,
    "lifespan": 72,
    "children": [
      "8385182f",
      "32e1bcfb",
      "908cd46b",
      "9f6003d4",
      "6325cfaf",
      "727f5b82",
      "993be70a",
      "e0347efd",
      "e8e28d7c",
      "8d06654c",
      "95278742",
      "b65b01b9",
      "e3e9f8dd"
    ],
    "peak_mass": 904.7968205743589,
    "dominant_channel": 0
  },
  "8385182f": {
    "parent": "8b4a37ae",
    "generation": 1,
    "birth_frame": 19,
    "death_frame": 20,
    "lifespan": 1,
    "children": [],
    "peak_mass": 6.852684842171429,
    "dominant_channel": 2
  },
  "ccd67063": {
    "parent": null,
    "generation": 0,
    "birth_frame": 32,
    "death_frame": 33,
    "lifespan": 1,
    "children": [],
    "peak_mass": 5.757965687967509,
    "dominant_channel": 2
  },
  "02915bfc": {
    "parent": null,
    "generation": 0,
    "birth_frame": 32,
    "death_frame": 33,
    "lifespan": 1,
    "children": [],
    "peak_mass": 4.469789693455529,
    "dominant_channel": 2
  },
  "32e1bcfb": {
    "parent": "8b4a37ae",
    "generation": 1,
    "birth_frame": 33,
    "death_frame": 34,
    "lifespan": 1,
    "children": [],
    "peak_mass": 11.185363241189147,
    "dominant_channel": 0
  },
  "cff8f74a": {
    "parent": null,
    "generation": 0,
    "birth_frame": 35,
    "death_frame": 69,
    "lifespan": 34,
    "children": [],
    "peak_mass": 14.966580043376672,
    "dominant_channel": 0
  },
  "bb9374b7": {
    "parent": null,
    "generation": 0,
    "birth_frame": 38,
    "death_frame": 39,
    "lifespan": 1,
    "children": [],
    "peak_mass": 7.018460538836333,
    "dominant_channel": 0
  },
  "a5fa0ff1": {
    "parent": null,
    "generation": 0,
    "birth_frame": 38,
    "death_frame": 39,
    "lifespan": 1,
    "children": [],
    "peak_mass": 5.602614877989203,
    "dominant_channel": 2
  },
  "cd94a308": {
    "parent": null,
    "generation": 0,
    "birth_frame": 38,
    "death_frame": 39,
    "lifespan": 1,
    "children": [],
    "peak_mass": 6.096632611621116,
    "dominant_channel": 2
  },
  "e7073d35": {
    "parent": null,
    "generation": 0,
    "birth_frame": 40,
    "death_frame": 41,
    "lifespan": 1,
    "children": [],
    "peak_mass": 5.0417122300352775,
    "dominant_channel": 0
  },
  "0ace5585": {
    "parent": null,
    "generation": 0,
    "birth_frame": 40,
    "death_frame": 41,
    "lifespan": 1,
    "children": [],
    "peak_mass": 6.2284174640044005,
    "dominant_channel": 0
  },
  "908cd46b": {
    "parent": "8b4a37ae",
    "generation": 1,
    "birth_frame": 42,
    "death_frame": 43,
    "lifespan": 1,
    "children": [],
    "peak_mass": 20.030235734336156,
    "dominant_channel": 0
  },
  "cbcb3eeb": {
    "parent": null,
    "generation": 0,
    "birth_frame": 43,
    "death_frame": 44,
    "lifespan": 1,
    "children": [],
    "peak_mass": 5.34116883560347,
    "dominant_channel": 2
  },
  "145e8d53": {
    "parent": null,
    "generation": 0,
    "birth_frame": 43,
    "death_frame": 44,
    "lifespan": 1,
    "children": [],
    "peak_mass": 4.5335573875148025,
    "dominant_channel": 2
  },
  "9f6003d4": {
    "parent": "8b4a37ae",
    "generation": 1,
    "birth_frame": 44,
    "death_frame": 45,
    "lifespan": 1,
    "children": [],
    "peak_mass": 20.166457285971845,
    "dominant_channel": 0
  },
  "a169f276": {
    "parent": null,
    "generation": 0,
    "birth_frame": 46,
    "death_frame": 47,
    "lifespan": 1,
    "children": [],
    "peak_mass": 6.637084991672204,
    "dominant_channel": 2
  },
  "33aa8766": {
    "parent": null,
    "generation": 0,
    "birth_frame": 46,
    "death_frame": 47,
    "lifespan": 1,
    "children": [],
    "peak_mass": 3.8860113612979412,
    "dominant_channel": 2
  },
  "4d497aa2": {
    "parent": null,
    "generation": 0,
    "birth_frame": 46,
    "death_frame": 47,
    "lifespan": 1,
    "children": [],
    "peak_mass": 5.547329764768348,
    "dominant_channel": 0
  },
  "6325cfaf": {
    "parent": "8b4a37ae",
    "generation": 1,
    "birth_frame": 54,
    "death_frame": 55,
    "lifespan": 1,
    "children": [],
    "peak_mass": 34.44369392440485,
    "dominant_channel": 0
  },
  "727f5b82": {
    "parent": "8b4a37ae",
    "generation": 1,
    "birth_frame": 55,
    "death_frame": null,
    "lifespan": 96,
    "children": [],
    "peak_mass": 38.18368246527274,
    "dominant_channel": 0
  },
  "993be70a": {
    "parent": "8b4a37ae",
    "generation": 1,
    "birth_frame": 55,
    "death_frame": 81,
    "lifespan": 26,
    "children": [],
    "peak_mass": 20.50523121236689,
    "dominant_channel": 0
  },
  "e0347efd": {
    "parent": "8b4a37ae",
    "generation": 1,
    "birth_frame": 60,
    "death_frame": 61,
    "lifespan": 1,
    "children": [],
    "peak_mass": 83.98616500851632,
    "dominant_channel": 0
  },
  "e8e28d7c": {
    "parent": "8b4a37ae",
    "generation": 1,
    "birth_frame": 62,
    "death_frame": 64,
    "lifespan": 2,
    "children": [],
    "peak_mass": 81.60325083220158,
    "dominant_channel": 0
  },
  "8d06654c": {
    "parent": "8b4a37ae",
    "generation": 1,
    "birth_frame": 64,
    "death_frame": 65,
    "lifespan": 1,
    "children": [
      "fedbb9e4"
    ],
    "peak_mass": 81.83976376014712,
    "dominant_channel": 0
  },
  "fedbb9e4": {
    "parent": "8d06654c",
    "generation": 2,
    "birth_frame": 65,
    "death_frame": 123,
    "lifespan": 58,
    "children": [
      "baead1bb"
    ],
    "peak_mass": 82.01141910881628,
    "dominant_channel": 0
  },
  "95278742": {
    "parent": "8b4a37ae",
    "generation": 1,
    "birth_frame": 69,
    "death_frame": 77,
    "lifespan": 8,
    "children": [],
    "peak_mass": 110.01226350320813,
    "dominant_channel": 0
  },
  "b65b01b9": {
    "parent": "8b4a37ae",
    "generation": 1,
    "birth_frame": 71,
    "death_frame": 77,
    "lifespan": 6,
    "children": [
      "c857058e"
    ],
    "peak_mass": 280.542036923083,
    "dominant_channel": 0
  },
  "e3e9f8dd": {
    "parent": "8b4a37ae",
    "generation": 1,
    "birth_frame": 71,
    "death_frame": 72,
    "lifespan": 1,
    "children": [],
    "peak_mass": 81.4989369270988,
    "dominant_channel": 0
  },
  "8b1ce0b5": {
    "parent": null,
    "generation": 0,
    "birth_frame": 73,
    "death_frame": 81,
    "lifespan": 8,
    "children": [],
    "peak_mass": 9.459231897600581,
    "dominant_channel": 0
  },
  "c857058e": {
    "parent": "b65b01b9",
    "generation": 2,
    "birth_frame": 74,
    "death_frame": 87,
    "lifespan": 13,
    "children": [
      "c4b00f8f",
      "82e5264b"
    ],
    "peak_mass": 404.6714471946162,
    "dominant_channel": 0
  },
  "ef7623e2": {
    "parent": null,
    "generation": 0,
    "birth_frame": 76,
    "death_frame": 78,
    "lifespan": 2,
    "children": [],
    "peak_mass": 4.900367600403249,
    "dominant_channel": 2
  },
  "c4b00f8f": {
    "parent": "c857058e",
    "generation": 3,
    "birth_frame": 78,
    "death_frame": 91,
    "lifespan": 13,
    "children": [
      "692046e0"
    ],
    "peak_mass": 303.3157817398092,
    "dominant_channel": 0
  },
  "82e5264b": {
    "parent": "c857058e",
    "generation": 3,
    "birth_frame": 80,
    "death_frame": null,
    "lifespan": 71,
    "children": [],
    "peak_mass": 98.27820128321106,
    "dominant_channel": 0
  },
  "b68f149e": {
    "parent": null,
    "generation": 0,
    "birth_frame": 83,
    "death_frame": 117,
    "lifespan": 34,
    "children": [],
    "peak_mass": 12.856260980660545,
    "dominant_channel": 0
  },
  "5d93bb1a": {
    "parent": null,
    "generation": 0,
    "birth_frame": 84,
    "death_frame": null,
    "lifespan": 67,
    "children": [],
    "peak_mass": 20.536740359206313,
    "dominant_channel": 0
  },
  "070f74e2": {
    "parent": null,
    "generation": 0,
    "birth_frame": 87,
    "death_frame": 89,
    "lifespan": 2,
    "children": [],
    "peak_mass": 5.720587143457071,
    "dominant_channel": 0
  },
  "6d5bc51b": {
    "parent": null,
    "generation": 0,
    "birth_frame": 87,
    "death_frame": 88,
    "lifespan": 1,
    "children": [],
    "peak_mass": 6.692507521947247,
    "dominant_channel": 0
  },
  "692046e0": {
    "parent": "c4b00f8f",
    "generation": 4,
    "birth_frame": 89,
    "death_frame": 94,
    "lifespan": 5,
    "children": [
      "0ea59d4d"
    ],
    "peak_mass": 303.39341266340244,
    "dominant_channel": 0
  },
  "17797035": {
    "parent": null,
    "generation": 0,
    "birth_frame": 90,
    "death_frame": 92,
    "lifespan": 2,
    "children": [],
    "peak_mass": 8.508510140578364,
    "dominant_channel": 0
  },
  "78634304": {
    "parent": null,
    "generation": 0,
    "birth_frame": 90,
    "death_frame": 92,
    "lifespan": 2,
    "children": [],
    "peak_mass": 8.798582653115492,
    "dominant_channel": 0
  }
}
```

## Media

- `outputs/SPECIES_030_CATENA_final.png`
- `outputs/SPECIES_030_CATENA.gif`
- note: ffmpeg not on PATH; GIF written instead

- genome: `outputs/species/SPECIES_030_CATENA_genome.json`
