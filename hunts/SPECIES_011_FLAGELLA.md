# SPECIES 011 — FLAGELLA

**Verdict:** VIABLE + REPRODUCING
**Origin:** random  |  **Seed:** 606

## Viability gates

| gate | verdict | value | detail |
| --- | --- | --- | --- |
| mass_conservation | PASS | 1.48203e-16 | tol=0.0001 |
| non_triviality | PASS | 87.1602 | conc>=6.0, occupancy 0.034<=0.45, 3 bodies |
| persistence | PASS | 1 | 1 organisms alive at the end with lifespan >= 15 frames |
| activity | PASS | 4.41958 | mean speed of the most mobile organism, cells/frame |

## Behaviour (anomaly bouncer)

| behaviour | established | score | evidence |
| --- | --- | --- | --- |
| phototaxis | no | -0.020 | lamp(26, 64): 38.4->38.2; lamp(102, 64): 38.4->39.2; lamp(64, 26): 38.3->37.8 | min approach -0.020 (needs > 0.05 for every lamp position) |
| predatory_pursuit | no | 0.242 | 4d70b88e(ch2) -> 75c80bff(ch2) closed 29.2 -> 19.0 cells over 14 frames, monotone 0.69, target speed 1.481 |
| cyclic_locomotion | no | 0.424 | uid=08abc20d circling=0.10 spectral_power=0.14 period=6.0 frames (counted only if >= 4) life=31 frames |

## Reproduction

Measured on the recording run below (the screening run is sampled more coarsely and its counts differ; both are stated separately rather than mixed).

- Divisions counted (offspring survived AND carried at least 10% of the parent's mass): **6**
- Raw fission events before the mass filter: **10** — the difference is debris a large body shed, which is not reproduction
- Surviving offspring total: **6**
- Organisms tracked in this run: **125**
- Screening run, for comparison: 1 divisions of 2 raw fissions, deepest generation 4

| frame | parent | children | parent mass | child masses | child share |
| --- | --- | --- | --- | --- | --- |
| 106 | `4d70b88e` | `c89067f8` | 341.7 | 38.0, 11.2 | 11% |
| 116 | `c89067f8` | `28f094d4` | 144.8 | 40.7 | 28% |
| 122 | `c89067f8` | `75c80bff` | 105.9 | 12.3 | 12% |
| 128 | `75c80bff` | `7c2b68c7` | 158.8 | 52.8 | 33% |
| 130 | `75c80bff` | `ebfc0a61` | 92.4 | 25.1 | 27% |
| 139 | `823d8ebf` | `24474077` | 66.7 | 26.5, 13.8, 11.1, 9.0 | 14% |

## Complexity

```json
{
  "morph_diversity": 3.223543374451114,
  "spatial_mi": 1.541525585159964,
  "cross_channel_mi": 0.8450948988973992,
  "euler_final": 88,
  "concentration_final": 87.16016757865683,
  "occupancy_final": 0.034423828125,
  "n_blobs_final": 3,
  "activity": 4.419581173395414,
  "mass_drift": 1.482026674505084e-16,
  "score": 16.475693047491664
}
```

## Lineage tree

```json
{
  "08abc20d": {
    "parent": null,
    "generation": 0,
    "birth_frame": 0,
    "death_frame": 31,
    "lifespan": 31,
    "children": [
      "7c52477f",
      "7584908c",
      "b7922cd0"
    ],
    "peak_mass": 760.8249368425695,
    "dominant_channel": 1
  },
  "7c52477f": {
    "parent": "08abc20d",
    "generation": 1,
    "birth_frame": 4,
    "death_frame": 5,
    "lifespan": 1,
    "children": [],
    "peak_mass": 5.632167722603744,
    "dominant_channel": 1
  },
  "daf77ecf": {
    "parent": null,
    "generation": 0,
    "birth_frame": 5,
    "death_frame": 6,
    "lifespan": 1,
    "children": [],
    "peak_mass": 5.382311808818599,
    "dominant_channel": 1
  },
  "e9b7e885": {
    "parent": null,
    "generation": 0,
    "birth_frame": 15,
    "death_frame": 16,
    "lifespan": 1,
    "children": [],
    "peak_mass": 4.599781986453496,
    "dominant_channel": 2
  },
  "8748af1e": {
    "parent": null,
    "generation": 0,
    "birth_frame": 16,
    "death_frame": 17,
    "lifespan": 1,
    "children": [],
    "peak_mass": 7.394595276049195,
    "dominant_channel": 1
  },
  "7584908c": {
    "parent": "08abc20d",
    "generation": 1,
    "birth_frame": 23,
    "death_frame": 24,
    "lifespan": 1,
    "children": [],
    "peak_mass": 8.18077300418062,
    "dominant_channel": 1
  },
  "315cce96": {
    "parent": null,
    "generation": 0,
    "birth_frame": 25,
    "death_frame": 26,
    "lifespan": 1,
    "children": [],
    "peak_mass": 6.6283989554877625,
    "dominant_channel": 1
  },
  "bef70b1e": {
    "parent": null,
    "generation": 0,
    "birth_frame": 27,
    "death_frame": 28,
    "lifespan": 1,
    "children": [],
    "peak_mass": 5.193066324776529,
    "dominant_channel": 1
  },
  "b7922cd0": {
    "parent": "08abc20d",
    "generation": 1,
    "birth_frame": 30,
    "death_frame": 37,
    "lifespan": 7,
    "children": [
      "443e7ed5",
      "ba18ddcc"
    ],
    "peak_mass": 545.3660384925961,
    "dominant_channel": 1
  },
  "264f2f26": {
    "parent": null,
    "generation": 0,
    "birth_frame": 31,
    "death_frame": 32,
    "lifespan": 1,
    "children": [],
    "peak_mass": 7.188110434334562,
    "dominant_channel": 1
  },
  "443e7ed5": {
    "parent": "b7922cd0",
    "generation": 2,
    "birth_frame": 32,
    "death_frame": 34,
    "lifespan": 2,
    "children": [],
    "peak_mass": 16.450206032652183,
    "dominant_channel": 1
  },
  "ba18ddcc": {
    "parent": "b7922cd0",
    "generation": 2,
    "birth_frame": 33,
    "death_frame": 35,
    "lifespan": 2,
    "children": [],
    "peak_mass": 8.769906872396747,
    "dominant_channel": 1
  },
  "df9d0240": {
    "parent": null,
    "generation": 0,
    "birth_frame": 35,
    "death_frame": 39,
    "lifespan": 4,
    "children": [
      "a0b0b643",
      "6bc92440"
    ],
    "peak_mass": 552.2745331640358,
    "dominant_channel": 1
  },
  "a0b0b643": {
    "parent": "df9d0240",
    "generation": 1,
    "birth_frame": 38,
    "death_frame": 62,
    "lifespan": 24,
    "children": [
      "03c0c680",
      "3e057b63",
      "4e777b66",
      "8a7414d8",
      "8c213552",
      "39cbb705",
      "1198f650",
      "de109700"
    ],
    "peak_mass": 515.8334063668788,
    "dominant_channel": 1
  },
  "6bc92440": {
    "parent": "df9d0240",
    "generation": 1,
    "birth_frame": 38,
    "death_frame": 39,
    "lifespan": 1,
    "children": [],
    "peak_mass": 14.84380129618339,
    "dominant_channel": 1
  },
  "03c0c680": {
    "parent": "a0b0b643",
    "generation": 2,
    "birth_frame": 40,
    "death_frame": 45,
    "lifespan": 5,
    "children": [
      "cc7d1c70"
    ],
    "peak_mass": 37.01564672757846,
    "dominant_channel": 1
  },
  "8de52846": {
    "parent": null,
    "generation": 0,
    "birth_frame": 40,
    "death_frame": 44,
    "lifespan": 4,
    "children": [],
    "peak_mass": 9.841500443203811,
    "dominant_channel": 1
  },
  "3e057b63": {
    "parent": "a0b0b643",
    "generation": 2,
    "birth_frame": 42,
    "death_frame": 43,
    "lifespan": 1,
    "children": [],
    "peak_mass": 7.325058189238092,
    "dominant_channel": 1
  },
  "eee2f10a": {
    "parent": null,
    "generation": 0,
    "birth_frame": 43,
    "death_frame": 44,
    "lifespan": 1,
    "children": [],
    "peak_mass": 5.469198644128747,
    "dominant_channel": 1
  },
  "cc7d1c70": {
    "parent": "03c0c680",
    "generation": 3,
    "birth_frame": 44,
    "death_frame": 45,
    "lifespan": 1,
    "children": [],
    "peak_mass": 6.439203818472148,
    "dominant_channel": 1
  },
  "4e777b66": {
    "parent": "a0b0b643",
    "generation": 2,
    "birth_frame": 44,
    "death_frame": 45,
    "lifespan": 1,
    "children": [],
    "peak_mass": 6.525984683608086,
    "dominant_channel": 1
  },
  "a02777c7": {
    "parent": null,
    "generation": 0,
    "birth_frame": 46,
    "death_frame": 59,
    "lifespan": 13,
    "children": [],
    "peak_mass": 13.798085400763137,
    "dominant_channel": 1
  },
  "e1043e84": {
    "parent": null,
    "generation": 0,
    "birth_frame": 46,
    "death_frame": 51,
    "lifespan": 5,
    "children": [],
    "peak_mass": 7.264348831507705,
    "dominant_channel": 1
  },
  "af38bba2": {
    "parent": null,
    "generation": 0,
    "birth_frame": 46,
    "death_frame": 49,
    "lifespan": 3,
    "children": [],
    "peak_mass": 7.004012172296029,
    "dominant_channel": 1
  },
  "87a6efa8": {
    "parent": null,
    "generation": 0,
    "birth_frame": 51,
    "death_frame": 52,
    "lifespan": 1,
    "children": [],
    "peak_mass": 8.721662468859948,
    "dominant_channel": 0
  },
  "638cc481": {
    "parent": null,
    "generation": 0,
    "birth_frame": 51,
    "death_frame": 56,
    "lifespan": 5,
    "children": [],
    "peak_mass": 8.173693159092867,
    "dominant_channel": 1
  },
  "8a7414d8": {
    "parent": "a0b0b643",
    "generation": 2,
    "birth_frame": 55,
    "death_frame": 56,
    "lifespan": 1,
    "children": [
      "a2122768"
    ],
    "peak_mass": 15.659181836110399,
    "dominant_channel": 1
  },
  "8c213552": {
    "parent": "a0b0b643",
    "generation": 2,
    "birth_frame": 55,
    "death_frame": 56,
    "lifespan": 1,
    "children": [],
    "peak_mass": 5.867305288685757,
    "dominant_channel": 1
  },
  "a2122768": {
    "parent": "8a7414d8",
    "generation": 3,
    "birth_frame": 56,
    "death_frame": 57,
    "lifespan": 1,
    "children": [],
    "peak_mass": 5.561788517862228,
    "dominant_channel": 1
  },
  "39cbb705": {
    "parent": "a0b0b643",
    "generation": 2,
    "birth_frame": 57,
    "death_frame": 60,
    "lifespan": 3,
    "children": [],
    "peak_mass": 10.089407545585907,
    "dominant_channel": 0
  },
  "955e701e": {
    "parent": null,
    "generation": 0,
    "birth_frame": 57,
    "death_frame": 59,
    "lifespan": 2,
    "children": [],
    "peak_mass": 7.446711332630775,
    "dominant_channel": 1
  },
  "1198f650": {
    "parent": "a0b0b643",
    "generation": 2,
    "birth_frame": 58,
    "death_frame": 60,
    "lifespan": 2,
    "children": [
      "5db657b6"
    ],
    "peak_mass": 21.159243982056974,
    "dominant_channel": 0
  },
  "de109700": {
    "parent": "a0b0b643",
    "generation": 2,
    "birth_frame": 59,
    "death_frame": 62,
    "lifespan": 3,
    "children": [],
    "peak_mass": 12.744264422399386,
    "dominant_channel": 1
  },
  "5db657b6": {
    "parent": "1198f650",
    "generation": 3,
    "birth_frame": 59,
    "death_frame": 60,
    "lifespan": 1,
    "children": [],
    "peak_mass": 7.662237861354052,
    "dominant_channel": 1
  },
  "7c709999": {
    "parent": null,
    "generation": 0,
    "birth_frame": 60,
    "death_frame": 64,
    "lifespan": 4,
    "children": [
      "aeaf5539",
      "457a20b9"
    ],
    "peak_mass": 538.9650578699625,
    "dominant_channel": 1
  },
  "56c6cdf5": {
    "parent": null,
    "generation": 0,
    "birth_frame": 60,
    "death_frame": 66,
    "lifespan": 6,
    "children": [],
    "peak_mass": 10.116780127873017,
    "dominant_channel": 1
  },
  "89a8d95b": {
    "parent": null,
    "generation": 0,
    "birth_frame": 62,
    "death_frame": 64,
    "lifespan": 2,
    "children": [],
    "peak_mass": 5.6843459317719605,
    "dominant_channel": 1
  },
  "aeaf5539": {
    "parent": "7c709999",
    "generation": 1,
    "birth_frame": 63,
    "death_frame": 64,
    "lifespan": 1,
    "children": [],
    "peak_mass": 23.49627270870923,
    "dominant_channel": 1
  },
  "457a20b9": {
    "parent": "7c709999",
    "generation": 1,
    "birth_frame": 63,
    "death_frame": 66,
    "lifespan": 3,
    "children": [
      "033f47c5",
      "ffcb7f0c"
    ],
    "peak_mass": 521.1826621007101,
    "dominant_channel": 1
  },
  "033f47c5": {
    "parent": "457a20b9",
    "generation": 2,
    "birth_frame": 65,
    "death_frame": 91,
    "lifespan": 26,
    "children": [
      "c5e327fc",
      "acb34404",
      "6dcd61b9",
      "b93d38c2",
      "11d1827c",
      "35e44ec9",
      "d4bae05f",
      "c553ef48",
      "4d70b88e"
    ],
    "peak_mass": 536.1391292321089,
    "dominant_channel": 1
  }
}
```

## Media

- `outputs/SPECIES_011_FLAGELLA_final.png`
- `outputs/SPECIES_011_FLAGELLA.gif`
- `outputs/SPECIES_011_FLAGELLA.mp4`

- genome: `outputs/species/SPECIES_011_FLAGELLA_genome.json`
