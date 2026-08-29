# SPECIES 001 — OSCILLIS

**Verdict:** VIABLE + REPRODUCING
**Origin:** random  |  **Seed:** 442

## Viability gates

| gate | verdict | value | detail |
| --- | --- | --- | --- |
| mass_conservation | PASS | 1.57479e-16 | tol=0.0001 |
| non_triviality | PASS | 76.5655 | conc>=6.0, occupancy 0.033<=0.45, 4 bodies |
| persistence | PASS | 3 | 3 organisms alive at the end with lifespan >= 15 frames |
| activity | PASS | 0.90135 | mean speed of the most mobile organism, cells/frame |

## Behaviour (anomaly bouncer)

| behaviour | established | score | evidence |
| --- | --- | --- | --- |
| phototaxis | no | 0.020 | lamp(26, 64): 38.4->37.6; lamp(102, 64): 38.4->37.6; lamp(64, 26): 38.4->37.6 | min approach +0.020 (needs > 0.05 for every lamp position) |
| predatory_pursuit | no | 0.038 | 76556492(ch1) -> b8e93b72(ch2) closed 12.0 -> 11.2 cells over 25 frames, monotone 0.58, target speed 0.169 |
| cyclic_locomotion | no | 0.167 | uid=623b149c circling=0.17 spectral_power=0.17 period=3.1 frames (counted only if >= 4) life=26 frames |

## Reproduction

Measured on the recording run below (the screening run is sampled more coarsely and its counts differ; both are stated separately rather than mixed).

- Divisions counted (offspring survived AND carried at least 10% of the parent's mass): **3**
- Raw fission events before the mass filter: **4** — the difference is debris a large body shed, which is not reproduction
- Surviving offspring total: **4**
- Organisms tracked in this run: **31**
- Screening run, for comparison: 4 divisions of 4 raw fissions, deepest generation 2

| frame | parent | children | parent mass | child masses | child share |
| --- | --- | --- | --- | --- | --- |
| 62 | `95d64b2f` | `76556492`, `623b149c` | 194.1 | 74.6, 23.9, 7.8, 7.5 | 38%, 12% |
| 66 | `95d64b2f` | `71aa3472` | 110.3 | 45.0 | 41% |
| 117 | `76556492` | `b8e93b72` | 80.7 | 14.0 | 17% |

## Complexity

```json
{
  "morph_diversity": 3.512243030593141,
  "spatial_mi": 1.4240871135866322,
  "cross_channel_mi": 0.9028062290842259,
  "euler_final": 183,
  "concentration_final": 76.56547811833622,
  "occupancy_final": 0.03314208984375,
  "n_blobs_final": 4,
  "activity": 0.9013499301467098,
  "mass_drift": 1.5747930191317263e-16,
  "score": 46.36881947038091
}
```

## Lineage tree

```json
{
  "72973540": {
    "parent": null,
    "generation": 0,
    "birth_frame": 0,
    "death_frame": 59,
    "lifespan": 59,
    "children": [
      "5d188bb4",
      "970010d0",
      "a59f76df",
      "fefc7791",
      "2e38fa49",
      "7f2b02b5",
      "95d64b2f"
    ],
    "peak_mass": 715.6062902072166,
    "dominant_channel": 1
  },
  "42f175df": {
    "parent": null,
    "generation": 0,
    "birth_frame": 23,
    "death_frame": 24,
    "lifespan": 1,
    "children": [],
    "peak_mass": 4.334000458187203,
    "dominant_channel": 2
  },
  "0259f757": {
    "parent": null,
    "generation": 0,
    "birth_frame": 36,
    "death_frame": 37,
    "lifespan": 1,
    "children": [],
    "peak_mass": 8.996540368180904,
    "dominant_channel": 2
  },
  "5d188bb4": {
    "parent": "72973540",
    "generation": 1,
    "birth_frame": 45,
    "death_frame": 46,
    "lifespan": 1,
    "children": [],
    "peak_mass": 11.603909122082364,
    "dominant_channel": 2
  },
  "d4ba1d05": {
    "parent": null,
    "generation": 0,
    "birth_frame": 46,
    "death_frame": 47,
    "lifespan": 1,
    "children": [],
    "peak_mass": 12.010353312806622,
    "dominant_channel": 2
  },
  "970010d0": {
    "parent": "72973540",
    "generation": 1,
    "birth_frame": 47,
    "death_frame": 48,
    "lifespan": 1,
    "children": [],
    "peak_mass": 12.17794768579915,
    "dominant_channel": 2
  },
  "a59f76df": {
    "parent": "72973540",
    "generation": 1,
    "birth_frame": 51,
    "death_frame": 52,
    "lifespan": 1,
    "children": [],
    "peak_mass": 46.46323150726366,
    "dominant_channel": 1
  },
  "fefc7791": {
    "parent": "72973540",
    "generation": 1,
    "birth_frame": 53,
    "death_frame": 55,
    "lifespan": 2,
    "children": [
      "fa55f293"
    ],
    "peak_mass": 52.45832235527282,
    "dominant_channel": 1
  },
  "d28318c5": {
    "parent": null,
    "generation": 0,
    "birth_frame": 54,
    "death_frame": 57,
    "lifespan": 3,
    "children": [],
    "peak_mass": 14.734458843082184,
    "dominant_channel": 2
  },
  "fa55f293": {
    "parent": "fefc7791",
    "generation": 2,
    "birth_frame": 55,
    "death_frame": 57,
    "lifespan": 2,
    "children": [],
    "peak_mass": 46.73984227735005,
    "dominant_channel": 1
  },
  "2e38fa49": {
    "parent": "72973540",
    "generation": 1,
    "birth_frame": 58,
    "death_frame": 60,
    "lifespan": 2,
    "children": [],
    "peak_mass": 298.58613623127076,
    "dominant_channel": 1
  },
  "7f2b02b5": {
    "parent": "72973540",
    "generation": 1,
    "birth_frame": 58,
    "death_frame": 60,
    "lifespan": 2,
    "children": [],
    "peak_mass": 8.913398971609888,
    "dominant_channel": 2
  },
  "95d64b2f": {
    "parent": "72973540",
    "generation": 1,
    "birth_frame": 58,
    "death_frame": null,
    "lifespan": 93,
    "children": [
      "fe802152",
      "76556492",
      "623b149c",
      "147e8968",
      "43c27100",
      "8888464c",
      "71aa3472",
      "659ea425"
    ],
    "peak_mass": 364.2738916169146,
    "dominant_channel": 1
  },
  "fe802152": {
    "parent": "95d64b2f",
    "generation": 2,
    "birth_frame": 60,
    "death_frame": 61,
    "lifespan": 1,
    "children": [],
    "peak_mass": 5.186282941464435,
    "dominant_channel": 0
  },
  "76556492": {
    "parent": "95d64b2f",
    "generation": 2,
    "birth_frame": 62,
    "death_frame": null,
    "lifespan": 89,
    "children": [
      "fc93ba4f",
      "b8e93b72",
      "3a8dd693"
    ],
    "peak_mass": 97.709832348623,
    "dominant_channel": 1
  },
  "623b149c": {
    "parent": "95d64b2f",
    "generation": 2,
    "birth_frame": 62,
    "death_frame": 88,
    "lifespan": 26,
    "children": [
      "bc198708"
    ],
    "peak_mass": 23.89158826415382,
    "dominant_channel": 2
  },
  "147e8968": {
    "parent": "95d64b2f",
    "generation": 2,
    "birth_frame": 62,
    "death_frame": 63,
    "lifespan": 1,
    "children": [],
    "peak_mass": 7.752746121753021,
    "dominant_channel": 2
  },
  "43c27100": {
    "parent": "95d64b2f",
    "generation": 2,
    "birth_frame": 62,
    "death_frame": 63,
    "lifespan": 1,
    "children": [],
    "peak_mass": 7.519932678290499,
    "dominant_channel": 2
  },
  "8888464c": {
    "parent": "95d64b2f",
    "generation": 2,
    "birth_frame": 63,
    "death_frame": 65,
    "lifespan": 2,
    "children": [],
    "peak_mass": 44.99046706864087,
    "dominant_channel": 1
  },
  "ce89f76e": {
    "parent": null,
    "generation": 0,
    "birth_frame": 65,
    "death_frame": 66,
    "lifespan": 1,
    "children": [],
    "peak_mass": 7.697660216787335,
    "dominant_channel": 2
  },
  "caa2839a": {
    "parent": null,
    "generation": 0,
    "birth_frame": 65,
    "death_frame": 66,
    "lifespan": 1,
    "children": [],
    "peak_mass": 8.192483460072676,
    "dominant_channel": 2
  },
  "fc93ba4f": {
    "parent": "76556492",
    "generation": 3,
    "birth_frame": 66,
    "death_frame": 71,
    "lifespan": 5,
    "children": [],
    "peak_mass": 10.374746413895556,
    "dominant_channel": 2
  },
  "71aa3472": {
    "parent": "95d64b2f",
    "generation": 2,
    "birth_frame": 66,
    "death_frame": null,
    "lifespan": 85,
    "children": [],
    "peak_mass": 59.42923668110353,
    "dominant_channel": 1
  },
  "bc198708": {
    "parent": "623b149c",
    "generation": 3,
    "birth_frame": 66,
    "death_frame": 67,
    "lifespan": 1,
    "children": [],
    "peak_mass": 6.466530973085939,
    "dominant_channel": 2
  },
  "bee290cb": {
    "parent": null,
    "generation": 0,
    "birth_frame": 69,
    "death_frame": 70,
    "lifespan": 1,
    "children": [],
    "peak_mass": 6.512006456177612,
    "dominant_channel": 2
  },
  "9dce8149": {
    "parent": null,
    "generation": 0,
    "birth_frame": 71,
    "death_frame": 72,
    "lifespan": 1,
    "children": [],
    "peak_mass": 6.478604766179579,
    "dominant_channel": 2
  },
  "659ea425": {
    "parent": "95d64b2f",
    "generation": 2,
    "birth_frame": 74,
    "death_frame": 75,
    "lifespan": 1,
    "children": [],
    "peak_mass": 8.652045924532166,
    "dominant_channel": 2
  },
  "af79e31a": {
    "parent": null,
    "generation": 0,
    "birth_frame": 91,
    "death_frame": 92,
    "lifespan": 1,
    "children": [],
    "peak_mass": 9.240252802483083,
    "dominant_channel": 2
  },
  "1c558fa1": {
    "parent": null,
    "generation": 0,
    "birth_frame": 95,
    "death_frame": 116,
    "lifespan": 21,
    "children": [],
    "peak_mass": 17.001926579626993,
    "dominant_channel": 2
  },
  "b8e93b72": {
    "parent": "76556492",
    "generation": 3,
    "birth_frame": 117,
    "death_frame": 142,
    "lifespan": 25,
    "children": [],
    "peak_mass": 14.397079209832091,
    "dominant_channel": 2
  },
  "3a8dd693": {
    "parent": "76556492",
    "generation": 3,
    "birth_frame": 149,
    "death_frame": null,
    "lifespan": 2,
    "children": [],
    "peak_mass": 12.217139725793423,
    "dominant_channel": 2
  }
}
```

## Media

- `outputs/SPECIES_001_OSCILLIS_final.png`
- `outputs/SPECIES_001_OSCILLIS.gif`
- `outputs/SPECIES_001_OSCILLIS.mp4`

- genome: `outputs/species/SPECIES_001_OSCILLIS_genome.json`
