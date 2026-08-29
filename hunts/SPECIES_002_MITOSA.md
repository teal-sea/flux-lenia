# SPECIES 002 — MITOSA

**Verdict:** VIABLE + REPRODUCING
**Origin:** random  |  **Seed:** 350

## Viability gates

| gate | verdict | value | detail |
| --- | --- | --- | --- |
| mass_conservation | PASS | 1.53412e-16 | tol=0.0001 |
| non_triviality | PASS | 82.6074 | conc>=6.0, occupancy 0.051<=0.45, 2 bodies |
| persistence | PASS | 2 | 2 organisms alive at the end with lifespan >= 15 frames |
| activity | PASS | 3.89917 | mean speed of the most mobile organism, cells/frame |

## Behaviour (anomaly bouncer)

| behaviour | established | score | evidence |
| --- | --- | --- | --- |
| phototaxis | no | -0.015 | lamp(26, 64): 38.4->38.4; lamp(102, 64): 38.4->39.0; lamp(64, 26): 38.5->38.4 | min approach -0.015 (needs > 0.05 for every lamp position) |
| predatory_pursuit | YES | 0.475 | 9997bf69(ch2) -> e7e9752b(ch0) closed 41.3 -> 18.2 cells over 14 frames, monotone 0.85, target speed 2.876 |
| cyclic_locomotion | no | 0.420 | uid=3ca8911f circling=0.05 spectral_power=0.14 period=22.0 frames (counted only if >= 4) life=23 frames |

## Reproduction

Measured on the recording run below (the screening run is sampled more coarsely and its counts differ; both are stated separately rather than mixed).

- Divisions counted (offspring survived AND carried at least 10% of the parent's mass): **13**
- Raw fission events before the mass filter: **22** — the difference is debris a large body shed, which is not reproduction
- Surviving offspring total: **13**
- Organisms tracked in this run: **54**
- Screening run, for comparison: 5 divisions of 7 raw fissions, deepest generation 6

| frame | parent | children | parent mass | child masses | child share |
| --- | --- | --- | --- | --- | --- |
| 58 | `6282dae9` | `f630caf4` | 415.4 | 73.2 | 18% |
| 58 | `526fc9c6` | `ccab51fa` | 72.3 | 18.6 | 26% |
| 63 | `ccab51fa` | `d2a02337` | 50.7 | 45.1 | 89% |
| 66 | `d2a02337` | `c9f4996f` | 72.3 | 17.1 | 24% |
| 83 | `f630caf4` | `e3cf1c8f` | 50.9 | 28.8 | 56% |
| 90 | `e3cf1c8f` | `248c38e8` | 46.4 | 26.0 | 56% |
| 91 | `6282dae9` | `02944611` | 357.8 | 64.0 | 18% |
| 95 | `248c38e8` | `4c33c82a` | 52.9 | 26.6 | 50% |
| 101 | `248c38e8` | `789923e8` | 404.9 | 83.1 | 21% |
| 104 | `eba06356` | `8979a3b6` | 42.8 | 37.6 | 88% |
| 121 | `e7e9752b` | `92650a09` | 481.3 | 129.5 | 27% |
| 130 | `92650a09` | `505fe4ec` | 95.0 | 22.1 | 23% |

## Complexity

```json
{
  "morph_diversity": 3.498344605367639,
  "spatial_mi": 1.511073570032554,
  "cross_channel_mi": 0.8555789810858123,
  "euler_final": -8,
  "concentration_final": 82.60744545138077,
  "occupancy_final": 0.05084228515625,
  "n_blobs_final": 2,
  "activity": 3.8991671715211846,
  "mass_drift": 1.534123862260774e-16,
  "score": 42.815069738016646
}
```

## Lineage tree

```json
{
  "abab94cb": {
    "parent": null,
    "generation": 0,
    "birth_frame": 0,
    "death_frame": 44,
    "lifespan": 44,
    "children": [
      "702b5c02"
    ],
    "peak_mass": 734.1915270502641,
    "dominant_channel": 2
  },
  "702b5c02": {
    "parent": "abab94cb",
    "generation": 1,
    "birth_frame": 43,
    "death_frame": 50,
    "lifespan": 7,
    "children": [
      "6282dae9",
      "00267905"
    ],
    "peak_mass": 686.2581861314347,
    "dominant_channel": 2
  },
  "6282dae9": {
    "parent": "702b5c02",
    "generation": 2,
    "birth_frame": 48,
    "death_frame": 98,
    "lifespan": 50,
    "children": [
      "fa1e8652",
      "5de631de",
      "526fc9c6",
      "3ccdea6a",
      "f630caf4",
      "42cfd7c0",
      "0605e465",
      "3fe3d4a1",
      "f26255ce",
      "2ffcb55c",
      "24f54592",
      "db42f2b5",
      "ed27898e",
      "064670cd",
      "3ca8911f",
      "52d475b1",
      "02944611"
    ],
    "peak_mass": 698.9545185381214,
    "dominant_channel": 0
  },
  "00267905": {
    "parent": "702b5c02",
    "generation": 2,
    "birth_frame": 49,
    "death_frame": 51,
    "lifespan": 2,
    "children": [],
    "peak_mass": 69.54887765691916,
    "dominant_channel": 2
  },
  "fa1e8652": {
    "parent": "6282dae9",
    "generation": 3,
    "birth_frame": 52,
    "death_frame": 55,
    "lifespan": 3,
    "children": [],
    "peak_mass": 75.18628773687504,
    "dominant_channel": 2
  },
  "5de631de": {
    "parent": "6282dae9",
    "generation": 3,
    "birth_frame": 55,
    "death_frame": 56,
    "lifespan": 1,
    "children": [],
    "peak_mass": 52.90736978839383,
    "dominant_channel": 2
  },
  "526fc9c6": {
    "parent": "6282dae9",
    "generation": 3,
    "birth_frame": 55,
    "death_frame": 61,
    "lifespan": 6,
    "children": [
      "ccab51fa",
      "66ee53b4"
    ],
    "peak_mass": 98.48033583017705,
    "dominant_channel": 1
  },
  "3ccdea6a": {
    "parent": "6282dae9",
    "generation": 3,
    "birth_frame": 57,
    "death_frame": 59,
    "lifespan": 2,
    "children": [],
    "peak_mass": 75.33102732934289,
    "dominant_channel": 2
  },
  "f630caf4": {
    "parent": "6282dae9",
    "generation": 3,
    "birth_frame": 58,
    "death_frame": 85,
    "lifespan": 27,
    "children": [
      "e3cf1c8f"
    ],
    "peak_mass": 80.0968947862689,
    "dominant_channel": 2
  },
  "ccab51fa": {
    "parent": "526fc9c6",
    "generation": 4,
    "birth_frame": 58,
    "death_frame": 65,
    "lifespan": 7,
    "children": [
      "d2a02337"
    ],
    "peak_mass": 97.6384205114509,
    "dominant_channel": 1
  },
  "66ee53b4": {
    "parent": "526fc9c6",
    "generation": 4,
    "birth_frame": 60,
    "death_frame": 61,
    "lifespan": 1,
    "children": [],
    "peak_mass": 23.035854046275496,
    "dominant_channel": 2
  },
  "d2a02337": {
    "parent": "ccab51fa",
    "generation": 5,
    "birth_frame": 63,
    "death_frame": 70,
    "lifespan": 7,
    "children": [
      "c9f4996f"
    ],
    "peak_mass": 92.75820707372941,
    "dominant_channel": 2
  },
  "42cfd7c0": {
    "parent": "6282dae9",
    "generation": 3,
    "birth_frame": 64,
    "death_frame": 68,
    "lifespan": 4,
    "children": [],
    "peak_mass": 71.91862965626274,
    "dominant_channel": 2
  },
  "c9f4996f": {
    "parent": "d2a02337",
    "generation": 6,
    "birth_frame": 66,
    "death_frame": 77,
    "lifespan": 11,
    "children": [],
    "peak_mass": 96.6501571546122,
    "dominant_channel": 2
  },
  "0605e465": {
    "parent": "6282dae9",
    "generation": 3,
    "birth_frame": 67,
    "death_frame": 68,
    "lifespan": 1,
    "children": [],
    "peak_mass": 60.030521010680346,
    "dominant_channel": 2
  },
  "3fe3d4a1": {
    "parent": "6282dae9",
    "generation": 3,
    "birth_frame": 71,
    "death_frame": 73,
    "lifespan": 2,
    "children": [
      "18147bb4"
    ],
    "peak_mass": 75.68934159934886,
    "dominant_channel": 2
  },
  "18147bb4": {
    "parent": "3fe3d4a1",
    "generation": 4,
    "birth_frame": 73,
    "death_frame": 74,
    "lifespan": 1,
    "children": [],
    "peak_mass": 35.538474449060146,
    "dominant_channel": 2
  },
  "f26255ce": {
    "parent": "6282dae9",
    "generation": 3,
    "birth_frame": 75,
    "death_frame": 77,
    "lifespan": 2,
    "children": [],
    "peak_mass": 40.174376269874635,
    "dominant_channel": 2
  },
  "2ffcb55c": {
    "parent": "6282dae9",
    "generation": 3,
    "birth_frame": 76,
    "death_frame": 77,
    "lifespan": 1,
    "children": [],
    "peak_mass": 25.09531550895354,
    "dominant_channel": 2
  },
  "24f54592": {
    "parent": "6282dae9",
    "generation": 3,
    "birth_frame": 78,
    "death_frame": 79,
    "lifespan": 1,
    "children": [],
    "peak_mass": 92.8386489436009,
    "dominant_channel": 2
  },
  "db42f2b5": {
    "parent": "6282dae9",
    "generation": 3,
    "birth_frame": 80,
    "death_frame": 82,
    "lifespan": 2,
    "children": [],
    "peak_mass": 39.84163559548555,
    "dominant_channel": 2
  },
  "e3cf1c8f": {
    "parent": "f630caf4",
    "generation": 4,
    "birth_frame": 83,
    "death_frame": 94,
    "lifespan": 11,
    "children": [
      "248c38e8"
    ],
    "peak_mass": 82.97484598511122,
    "dominant_channel": 2
  },
  "ed27898e": {
    "parent": "6282dae9",
    "generation": 3,
    "birth_frame": 84,
    "death_frame": 85,
    "lifespan": 1,
    "children": [],
    "peak_mass": 92.19589978915944,
    "dominant_channel": 2
  },
  "064670cd": {
    "parent": "6282dae9",
    "generation": 3,
    "birth_frame": 89,
    "death_frame": 90,
    "lifespan": 1,
    "children": [],
    "peak_mass": 58.718580339859976,
    "dominant_channel": 2
  },
  "3ca8911f": {
    "parent": "6282dae9",
    "generation": 3,
    "birth_frame": 89,
    "death_frame": 112,
    "lifespan": 23,
    "children": [
      "c4299fc3"
    ],
    "peak_mass": 109.7887700409569,
    "dominant_channel": 2
  },
  "52d475b1": {
    "parent": "6282dae9",
    "generation": 3,
    "birth_frame": 89,
    "death_frame": 95,
    "lifespan": 6,
    "children": [],
    "peak_mass": 87.13741891510529,
    "dominant_channel": 2
  },
  "248c38e8": {
    "parent": "e3cf1c8f",
    "generation": 5,
    "birth_frame": 90,
    "death_frame": 107,
    "lifespan": 17,
    "children": [
      "4c33c82a",
      "789923e8",
      "eba06356"
    ],
    "peak_mass": 519.0479291147869,
    "dominant_channel": 0
  },
  "02944611": {
    "parent": "6282dae9",
    "generation": 3,
    "birth_frame": 91,
    "death_frame": 108,
    "lifespan": 17,
    "children": [],
    "peak_mass": 67.74265867091147,
    "dominant_channel": 2
  },
  "4c33c82a": {
    "parent": "248c38e8",
    "generation": 6,
    "birth_frame": 95,
    "death_frame": 117,
    "lifespan": 22,
    "children": [
      "9997bf69",
      "e7e9752b"
    ],
    "peak_mass": 680.4596274691655,
    "dominant_channel": 2
  },
  "789923e8": {
    "parent": "248c38e8",
    "generation": 6,
    "birth_frame": 101,
    "death_frame": 108,
    "lifespan": 7,
    "children": [],
    "peak_mass": 85.26083269950355,
    "dominant_channel": 2
  },
  "eba06356": {
    "parent": "248c38e8",
    "generation": 6,
    "birth_frame": 102,
    "death_frame": 105,
    "lifespan": 3,
    "children": [
      "8979a3b6"
    ],
    "peak_mass": 81.18215259593501,
    "dominant_channel": 1
  },
  "8979a3b6": {
    "parent": "eba06356",
    "generation": 7,
    "birth_frame": 104,
    "death_frame": 112,
    "lifespan": 8,
    "children": [],
    "peak_mass": 92.14091515879227,
    "dominant_channel": 2
  },
  "c4299fc3": {
    "parent": "3ca8911f",
    "generation": 4,
    "birth_frame": 109,
    "death_frame": 113,
    "lifespan": 4,
    "children": [],
    "peak_mass": 107.73095176686198,
    "dominant_channel": 2
  },
  "9997bf69": {
    "parent": "4c33c82a",
    "generation": 7,
    "birth_frame": 116,
    "death_frame": 131,
    "lifespan": 15,
    "children": [],
    "peak_mass": 51.23880324362876,
    "dominant_channel": 2
  },
  "e7e9752b": {
    "parent": "4c33c82a",
    "generation": 7,
    "birth_frame": 116,
    "death_frame": 130,
    "lifespan": 14,
    "children": [
      "550548a8",
      "92650a09",
      "c249c152"
    ],
    "peak_mass": 626.2217876847558,
    "dominant_channel": 0
  },
  "550548a8": {
    "parent": "e7e9752b",
    "generation": 8,
    "birth_frame": 118,
    "death_frame": 119,
    "lifespan": 1,
    "children": [],
    "peak_mass": 113.09415124773952,
    "dominant_channel": 2
  },
  "92650a09": {
    "parent": "e7e9752b",
    "generation": 8,
    "birth_frame": 121,
    "death_frame": 131,
    "lifespan": 10,
    "children": [
      "505fe4ec"
    ],
    "peak_mass": 132.4108890573885,
    "dominant_channel": 2
  },
  "c249c152": {
    "parent": "e7e9752b",
    "generation": 8,
    "birth_frame": 129,
    "death_frame": 133,
    "lifespan": 4,
    "children": [
      "047c786d",
      "388313ac",
      "c22d2adc"
    ],
    "peak_mass": 461.6638149375955,
    "dominant_channel": 2
  },
  "505fe4ec": {
    "parent": "92650a09",
    "generation": 9,
    "birth_frame": 130,
    "death_frame": 147,
    "lifespan": 17,
    "children": [
      "f5120198",
      "620ab438"
    ],
    "peak_mass": 129.95657813041598,
    "dominant_channel": 2
  },
  "047c786d": {
    "parent": "c249c152",
    "generation": 9,
    "birth_frame": 131,
    "death_frame": 132,
    "lifespan": 1,
    "children": [
      "31c88ab9"
    ],
    "peak_mass": 38.932002613079646,
    "dominant_channel": 1
  }
}
```

## Media

- `outputs/SPECIES_002_MITOSA_final.png`
- `outputs/SPECIES_002_MITOSA.gif`
- `outputs/SPECIES_002_MITOSA.mp4`

- genome: `outputs/species/SPECIES_002_MITOSA_genome.json`
