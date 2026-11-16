# SPECIES 023 — UNDULA

**Verdict:** VIABLE + REPRODUCING
**Origin:** random  |  **Seed:** 807

## Viability gates

| gate | verdict | value | detail |
| --- | --- | --- | --- |
| mass_conservation | PASS | 2.19572e-16 | tol=0.0001 |
| non_triviality | PASS | 23.5108 | conc>=6.0, occupancy 0.181<=0.45, 32 bodies |
| persistence | PASS | 6 | 6 organisms alive at the end with lifespan >= 15 frames |
| activity | PASS | 6.20207 | mean speed of the most mobile organism, cells/frame |

## Behaviour (anomaly bouncer)

| behaviour | established | score | evidence |
| --- | --- | --- | --- |
| phototaxis | no | -0.031 | lamp(26, 64): 38.5->39.1; lamp(102, 64): 38.3->38.6; lamp(64, 26): 38.4->39.6 | min approach -0.031 (needs > 0.05 for every lamp position) |
| predatory_pursuit | no | 0.344 | 68d3775e(ch2) -> 3c77252a(ch1) closed 75.6 -> 37.8 cells over 17 frames, monotone 0.69, target speed 3.767 |
| cyclic_locomotion | YES | 0.630 | uid=d7eae613 circling=0.26 spectral_power=0.21 period=10.0 frames (counted only if >= 4) life=21 frames |

## Reproduction

Measured on the recording run below (the screening run is sampled more coarsely and its counts differ; both are stated separately rather than mixed).

- Divisions counted (offspring survived AND carried at least 10% of the parent's mass): **19**
- Raw fission events before the mass filter: **58** — the difference is debris a large body shed, which is not reproduction
- Surviving offspring total: **19**
- Organisms tracked in this run: **408**
- Screening run, for comparison: 8 divisions of 20 raw fissions, deepest generation 5

| frame | parent | children | parent mass | child masses | child share |
| --- | --- | --- | --- | --- | --- |
| 61 | `2358d3fd` | `763f1051` | 27.9 | 20.7 | 74% |
| 65 | `1d98c70c` | `a70c6c5a` | 24.1 | 11.6 | 48% |
| 73 | `336c50b5` | `7b794c3e` | 24.8 | 17.0, 11.8 | 69% |
| 84 | `eee2db24` | `06d5093b` | 138.5 | 15.2 | 11% |
| 86 | `eee2db24` | `0cfc5805` | 143.4 | 22.2 | 15% |
| 87 | `eee2db24` | `f5fe4307` | 81.7 | 47.7 | 58% |
| 91 | `482bb6a0` | `f90eac19` | 12.5 | 10.3 | 82% |
| 93 | `22bb36eb` | `d264dec8` | 24.5 | 17.5 | 71% |
| 97 | `8a8a4b75` | `98da4394` | 16.6 | 12.9 | 77% |
| 101 | `d264dec8` | `0f195506` | 24.3 | 19.2 | 79% |
| 109 | `f05241fb` | `63e87db1` | 11.3 | 10.8 | 96% |
| 110 | `66eb4565` | `d7eae613` | 24.0 | 13.7 | 57% |

## Complexity

```json
{
  "morph_diversity": 2.8076284530632796,
  "spatial_mi": 1.1397334483447856,
  "cross_channel_mi": 0.6685752712130381,
  "euler_final": 89,
  "concentration_final": 23.51076878860559,
  "occupancy_final": 0.18145751953125,
  "n_blobs_final": 32,
  "activity": 6.202071470425191,
  "mass_drift": 2.1957169265476371e-16,
  "score": 40.24262418050153
}
```

## Lineage tree

```json
{
  "15e53507": {
    "parent": null,
    "generation": 0,
    "birth_frame": 0,
    "death_frame": 72,
    "lifespan": 72,
    "children": [
      "8ff739fb",
      "bd01233c",
      "87c1a09c",
      "0be64ced",
      "7b6c41d3",
      "3d80bff3",
      "f43726d5",
      "6b541bb7",
      "03c676c2",
      "7430f341",
      "9cecaf02",
      "1bd14533",
      "df628a45",
      "2e8498b5",
      "2a091441",
      "0d21fb19",
      "b86e4065",
      "7d4ddc81",
      "1514fd78",
      "cb90677a",
      "846a3ee8",
      "1d98c70c",
      "cd64ce97",
      "30d640e9",
      "3854e0cf",
      "6a16bf12",
      "9f522491",
      "d5999e50",
      "ccdcf004",
      "94c1d0a8",
      "283aeb05",
      "1da64014",
      "9c3db5e2",
      "df4abfee"
    ],
    "peak_mass": 4099.460042777132,
    "dominant_channel": 1
  },
  "8ff739fb": {
    "parent": "15e53507",
    "generation": 1,
    "birth_frame": 11,
    "death_frame": 12,
    "lifespan": 1,
    "children": [],
    "peak_mass": 6.195998956518691,
    "dominant_channel": 2
  },
  "1b387bb5": {
    "parent": null,
    "generation": 0,
    "birth_frame": 19,
    "death_frame": 20,
    "lifespan": 1,
    "children": [],
    "peak_mass": 7.53565401842789,
    "dominant_channel": 2
  },
  "bd01233c": {
    "parent": "15e53507",
    "generation": 1,
    "birth_frame": 26,
    "death_frame": 27,
    "lifespan": 1,
    "children": [],
    "peak_mass": 10.117299632720572,
    "dominant_channel": 2
  },
  "32e0fabc": {
    "parent": null,
    "generation": 0,
    "birth_frame": 32,
    "death_frame": 33,
    "lifespan": 1,
    "children": [],
    "peak_mass": 13.282726872550377,
    "dominant_channel": 2
  },
  "dc1dbbde": {
    "parent": null,
    "generation": 0,
    "birth_frame": 34,
    "death_frame": 35,
    "lifespan": 1,
    "children": [],
    "peak_mass": 8.421034186955925,
    "dominant_channel": 2
  },
  "87c1a09c": {
    "parent": "15e53507",
    "generation": 1,
    "birth_frame": 37,
    "death_frame": 39,
    "lifespan": 2,
    "children": [],
    "peak_mass": 11.809213269580177,
    "dominant_channel": 2
  },
  "0be64ced": {
    "parent": "15e53507",
    "generation": 1,
    "birth_frame": 38,
    "death_frame": 40,
    "lifespan": 2,
    "children": [],
    "peak_mass": 18.983505458684203,
    "dominant_channel": 2
  },
  "7b6c41d3": {
    "parent": "15e53507",
    "generation": 1,
    "birth_frame": 41,
    "death_frame": 44,
    "lifespan": 3,
    "children": [],
    "peak_mass": 17.675507152597444,
    "dominant_channel": 2
  },
  "3b8606a5": {
    "parent": null,
    "generation": 0,
    "birth_frame": 42,
    "death_frame": 43,
    "lifespan": 1,
    "children": [],
    "peak_mass": 9.039933292630469,
    "dominant_channel": 2
  },
  "97b1d247": {
    "parent": null,
    "generation": 0,
    "birth_frame": 42,
    "death_frame": 43,
    "lifespan": 1,
    "children": [],
    "peak_mass": 9.002089147037688,
    "dominant_channel": 2
  },
  "8219f7a0": {
    "parent": null,
    "generation": 0,
    "birth_frame": 44,
    "death_frame": 45,
    "lifespan": 1,
    "children": [],
    "peak_mass": 9.132530874079407,
    "dominant_channel": 2
  },
  "0f6b9995": {
    "parent": null,
    "generation": 0,
    "birth_frame": 44,
    "death_frame": 51,
    "lifespan": 7,
    "children": [],
    "peak_mass": 16.00820512331925,
    "dominant_channel": 2
  },
  "d65c67c0": {
    "parent": null,
    "generation": 0,
    "birth_frame": 46,
    "death_frame": 47,
    "lifespan": 1,
    "children": [],
    "peak_mass": 12.37195548012408,
    "dominant_channel": 2
  },
  "3d80bff3": {
    "parent": "15e53507",
    "generation": 1,
    "birth_frame": 47,
    "death_frame": 48,
    "lifespan": 1,
    "children": [],
    "peak_mass": 20.7180986849634,
    "dominant_channel": 2
  },
  "836aafdc": {
    "parent": null,
    "generation": 0,
    "birth_frame": 48,
    "death_frame": 49,
    "lifespan": 1,
    "children": [],
    "peak_mass": 8.586600357757082,
    "dominant_channel": 2
  },
  "148d3744": {
    "parent": null,
    "generation": 0,
    "birth_frame": 48,
    "death_frame": 50,
    "lifespan": 2,
    "children": [],
    "peak_mass": 12.27977246420566,
    "dominant_channel": 2
  },
  "27958229": {
    "parent": null,
    "generation": 0,
    "birth_frame": 50,
    "death_frame": 52,
    "lifespan": 2,
    "children": [],
    "peak_mass": 9.76506423120652,
    "dominant_channel": 2
  },
  "f43726d5": {
    "parent": "15e53507",
    "generation": 1,
    "birth_frame": 51,
    "death_frame": 52,
    "lifespan": 1,
    "children": [],
    "peak_mass": 34.031336039892025,
    "dominant_channel": 1
  },
  "6b541bb7": {
    "parent": "15e53507",
    "generation": 1,
    "birth_frame": 51,
    "death_frame": 52,
    "lifespan": 1,
    "children": [],
    "peak_mass": 12.738001869477147,
    "dominant_channel": 2
  },
  "b0deeeda": {
    "parent": null,
    "generation": 0,
    "birth_frame": 52,
    "death_frame": 59,
    "lifespan": 7,
    "children": [],
    "peak_mass": 11.883274654157802,
    "dominant_channel": 2
  },
  "b063787b": {
    "parent": null,
    "generation": 0,
    "birth_frame": 52,
    "death_frame": 59,
    "lifespan": 7,
    "children": [
      "245ca792"
    ],
    "peak_mass": 18.49894177911513,
    "dominant_channel": 2
  },
  "be98e667": {
    "parent": null,
    "generation": 0,
    "birth_frame": 52,
    "death_frame": 65,
    "lifespan": 13,
    "children": [],
    "peak_mass": 17.621317930354603,
    "dominant_channel": 2
  },
  "03c676c2": {
    "parent": "15e53507",
    "generation": 1,
    "birth_frame": 53,
    "death_frame": 54,
    "lifespan": 1,
    "children": [],
    "peak_mass": 14.043705336544896,
    "dominant_channel": 2
  },
  "133703de": {
    "parent": null,
    "generation": 0,
    "birth_frame": 53,
    "death_frame": 54,
    "lifespan": 1,
    "children": [],
    "peak_mass": 8.85026055270389,
    "dominant_channel": 2
  },
  "e5293589": {
    "parent": null,
    "generation": 0,
    "birth_frame": 53,
    "death_frame": 60,
    "lifespan": 7,
    "children": [],
    "peak_mass": 13.574467825909558,
    "dominant_channel": 2
  },
  "3c93a072": {
    "parent": null,
    "generation": 0,
    "birth_frame": 54,
    "death_frame": 55,
    "lifespan": 1,
    "children": [],
    "peak_mass": 13.629014871093865,
    "dominant_channel": 2
  },
  "7430f341": {
    "parent": "15e53507",
    "generation": 1,
    "birth_frame": 55,
    "death_frame": 81,
    "lifespan": 26,
    "children": [],
    "peak_mass": 18.77382166637688,
    "dominant_channel": 2
  },
  "c8ffac42": {
    "parent": null,
    "generation": 0,
    "birth_frame": 56,
    "death_frame": 57,
    "lifespan": 1,
    "children": [],
    "peak_mass": 8.167875893745544,
    "dominant_channel": 2
  },
  "949def68": {
    "parent": null,
    "generation": 0,
    "birth_frame": 56,
    "death_frame": 69,
    "lifespan": 13,
    "children": [
      "70e2524e"
    ],
    "peak_mass": 26.975199033271622,
    "dominant_channel": 2
  },
  "2358d3fd": {
    "parent": null,
    "generation": 0,
    "birth_frame": 56,
    "death_frame": 61,
    "lifespan": 5,
    "children": [
      "763f1051"
    ],
    "peak_mass": 20.91978839307668,
    "dominant_channel": 2
  },
  "c3ee7d04": {
    "parent": null,
    "generation": 0,
    "birth_frame": 56,
    "death_frame": 57,
    "lifespan": 1,
    "children": [],
    "peak_mass": 11.24759256499543,
    "dominant_channel": 2
  },
  "9cecaf02": {
    "parent": "15e53507",
    "generation": 1,
    "birth_frame": 57,
    "death_frame": 58,
    "lifespan": 1,
    "children": [],
    "peak_mass": 87.5071857274495,
    "dominant_channel": 2
  },
  "1bd14533": {
    "parent": "15e53507",
    "generation": 1,
    "birth_frame": 57,
    "death_frame": 59,
    "lifespan": 2,
    "children": [],
    "peak_mass": 28.56342994986199,
    "dominant_channel": 2
  },
  "df628a45": {
    "parent": "15e53507",
    "generation": 1,
    "birth_frame": 57,
    "death_frame": 58,
    "lifespan": 1,
    "children": [],
    "peak_mass": 18.35714899230581,
    "dominant_channel": 2
  },
  "3c59d829": {
    "parent": null,
    "generation": 0,
    "birth_frame": 57,
    "death_frame": 63,
    "lifespan": 6,
    "children": [
      "f1561396"
    ],
    "peak_mass": 26.00988459555249,
    "dominant_channel": 2
  },
  "2e8498b5": {
    "parent": "15e53507",
    "generation": 1,
    "birth_frame": 58,
    "death_frame": 59,
    "lifespan": 1,
    "children": [],
    "peak_mass": 15.790164990284218,
    "dominant_channel": 2
  },
  "245ca792": {
    "parent": "b063787b",
    "generation": 1,
    "birth_frame": 58,
    "death_frame": 60,
    "lifespan": 2,
    "children": [],
    "peak_mass": 19.21229514335667,
    "dominant_channel": 2
  },
  "87bb2042": {
    "parent": null,
    "generation": 0,
    "birth_frame": 58,
    "death_frame": 61,
    "lifespan": 3,
    "children": [],
    "peak_mass": 11.335996194574303,
    "dominant_channel": 2
  },
  "ddfafded": {
    "parent": null,
    "generation": 0,
    "birth_frame": 58,
    "death_frame": 59,
    "lifespan": 1,
    "children": [],
    "peak_mass": 11.47849283315463,
    "dominant_channel": 2
  }
}
```

## Media

- `outputs/SPECIES_023_UNDULA_final.png`
- `outputs/SPECIES_023_UNDULA.gif`
- `outputs/SPECIES_023_UNDULA.mp4`

- genome: `outputs/species/SPECIES_023_UNDULA_genome.json`
