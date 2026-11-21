# SPECIES 005 — SPLITTER

**Verdict:** VIABLE + REPRODUCING
**Origin:** random  |  **Seed:** 506

## Viability gates

| gate | verdict | value | detail |
| --- | --- | --- | --- |
| mass_conservation | PASS | 1.3661e-16 | tol=0.0001 |
| non_triviality | PASS | 10.3392 | conc>=6.0, occupancy 0.278<=0.45, 17 bodies |
| persistence | PASS | 4 | 4 organisms alive at the end with lifespan >= 15 frames |
| activity | PASS | 8.29934 | mean speed of the most mobile organism, cells/frame |

## Behaviour (anomaly bouncer)

| behaviour | established | score | evidence |
| --- | --- | --- | --- |
| phototaxis | no | -0.003 | lamp(26, 64): 38.4->37.9; lamp(102, 64): 38.4->38.5; lamp(64, 26): 38.3->38.2 | min approach -0.003 (needs > 0.05 for every lamp position) |
| predatory_pursuit | no | 0.247 | f86496dd(ch0) -> a357a82c(ch0) closed 64.4 -> 42.5 cells over 12 frames, monotone 0.73, target speed 0.411 |
| cyclic_locomotion | no | 0.419 | uid=0b42c3f7 circling=0.42 spectral_power=0.13 period=4.6 frames (counted only if >= 4) life=33 frames |

## Reproduction

Measured on the recording run below (the screening run is sampled more coarsely and its counts differ; both are stated separately rather than mixed).

- Divisions counted (offspring survived AND carried at least 10% of the parent's mass): **1**
- Raw fission events before the mass filter: **25** — the difference is debris a large body shed, which is not reproduction
- Surviving offspring total: **1**
- Organisms tracked in this run: **297**
- Screening run, for comparison: 2 divisions of 17 raw fissions, deepest generation 6

| frame | parent | children | parent mass | child masses | child share |
| --- | --- | --- | --- | --- | --- |
| 144 | `c702391e` | `040c391c` | 6.0 | 4.0 | 67% |

## Complexity

```json
{
  "morph_diversity": 2.895640869852788,
  "spatial_mi": 1.3140438388997349,
  "cross_channel_mi": 0.7606880594124715,
  "euler_final": 173,
  "concentration_final": 10.339189929186194,
  "occupancy_final": 0.2779541015625,
  "n_blobs_final": 17,
  "activity": 8.299335536578141,
  "mass_drift": 1.3661014988793904e-16,
  "score": 24.42968760697068
}
```

## Lineage tree

```json
{
  "0b42c3f7": {
    "parent": null,
    "generation": 0,
    "birth_frame": 0,
    "death_frame": 33,
    "lifespan": 33,
    "children": [
      "76412cc0",
      "246f6ab5",
      "c0b12704",
      "15599c94"
    ],
    "peak_mass": 3293.684894531879,
    "dominant_channel": 0
  },
  "76412cc0": {
    "parent": "0b42c3f7",
    "generation": 1,
    "birth_frame": 6,
    "death_frame": 7,
    "lifespan": 1,
    "children": [],
    "peak_mass": 98.90260875102288,
    "dominant_channel": 0
  },
  "246f6ab5": {
    "parent": "0b42c3f7",
    "generation": 1,
    "birth_frame": 7,
    "death_frame": 8,
    "lifespan": 1,
    "children": [],
    "peak_mass": 81.49042247814134,
    "dominant_channel": 0
  },
  "c0b12704": {
    "parent": "0b42c3f7",
    "generation": 1,
    "birth_frame": 7,
    "death_frame": 8,
    "lifespan": 1,
    "children": [],
    "peak_mass": 48.80133129927066,
    "dominant_channel": 0
  },
  "15599c94": {
    "parent": "0b42c3f7",
    "generation": 1,
    "birth_frame": 32,
    "death_frame": 36,
    "lifespan": 4,
    "children": [
      "7654c7d2"
    ],
    "peak_mass": 3041.923593710477,
    "dominant_channel": 0
  },
  "7654c7d2": {
    "parent": "15599c94",
    "generation": 2,
    "birth_frame": 35,
    "death_frame": 36,
    "lifespan": 1,
    "children": [],
    "peak_mass": 8.407859474703518,
    "dominant_channel": 0
  },
  "e0a95503": {
    "parent": null,
    "generation": 0,
    "birth_frame": 35,
    "death_frame": 39,
    "lifespan": 4,
    "children": [
      "23b246f7",
      "c828fc26"
    ],
    "peak_mass": 3144.0949256806816,
    "dominant_channel": 0
  },
  "709f3a73": {
    "parent": null,
    "generation": 0,
    "birth_frame": 36,
    "death_frame": 38,
    "lifespan": 2,
    "children": [],
    "peak_mass": 8.202460536591785,
    "dominant_channel": 0
  },
  "21aa1fa1": {
    "parent": null,
    "generation": 0,
    "birth_frame": 36,
    "death_frame": 38,
    "lifespan": 2,
    "children": [],
    "peak_mass": 8.786399229994718,
    "dominant_channel": 0
  },
  "23b246f7": {
    "parent": "e0a95503",
    "generation": 1,
    "birth_frame": 37,
    "death_frame": 38,
    "lifespan": 1,
    "children": [],
    "peak_mass": 8.74766264095305,
    "dominant_channel": 0
  },
  "c828fc26": {
    "parent": "e0a95503",
    "generation": 1,
    "birth_frame": 38,
    "death_frame": 44,
    "lifespan": 6,
    "children": [
      "ca9e8900",
      "23dcc14e"
    ],
    "peak_mass": 3070.104286395824,
    "dominant_channel": 0
  },
  "ca9e8900": {
    "parent": "c828fc26",
    "generation": 2,
    "birth_frame": 39,
    "death_frame": 81,
    "lifespan": 42,
    "children": [
      "ad9b00d6",
      "e1a5c487",
      "af0cbaf5"
    ],
    "peak_mass": 2985.822925270939,
    "dominant_channel": 0
  },
  "551cb6f2": {
    "parent": null,
    "generation": 0,
    "birth_frame": 39,
    "death_frame": 40,
    "lifespan": 1,
    "children": [],
    "peak_mass": 6.361162308886376,
    "dominant_channel": 0
  },
  "f221152c": {
    "parent": null,
    "generation": 0,
    "birth_frame": 39,
    "death_frame": 40,
    "lifespan": 1,
    "children": [],
    "peak_mass": 5.717338634121374,
    "dominant_channel": 0
  },
  "9d744f88": {
    "parent": null,
    "generation": 0,
    "birth_frame": 39,
    "death_frame": 40,
    "lifespan": 1,
    "children": [],
    "peak_mass": 4.388049117606233,
    "dominant_channel": 0
  },
  "ef966d39": {
    "parent": null,
    "generation": 0,
    "birth_frame": 41,
    "death_frame": 46,
    "lifespan": 5,
    "children": [],
    "peak_mass": 7.832461744588259,
    "dominant_channel": 0
  },
  "a09960bd": {
    "parent": null,
    "generation": 0,
    "birth_frame": 41,
    "death_frame": 53,
    "lifespan": 12,
    "children": [],
    "peak_mass": 8.426014313330223,
    "dominant_channel": 0
  },
  "23dcc14e": {
    "parent": "c828fc26",
    "generation": 2,
    "birth_frame": 42,
    "death_frame": 76,
    "lifespan": 34,
    "children": [
      "c2479f8e",
      "7843366d",
      "e44430c8",
      "6992972c",
      "de999db7",
      "af21bad0",
      "3f90e687",
      "10cfb49b",
      "f7ee8913",
      "36fbfe32",
      "3c351cce",
      "b7654454",
      "afd3e04c",
      "306565bc",
      "fcf3d2d0"
    ],
    "peak_mass": 3123.1696662922814,
    "dominant_channel": 0
  },
  "22b057b2": {
    "parent": null,
    "generation": 0,
    "birth_frame": 43,
    "death_frame": 60,
    "lifespan": 17,
    "children": [],
    "peak_mass": 5.488142046619275,
    "dominant_channel": 0
  },
  "fe00937d": {
    "parent": null,
    "generation": 0,
    "birth_frame": 48,
    "death_frame": 49,
    "lifespan": 1,
    "children": [],
    "peak_mass": 3.092561630164812,
    "dominant_channel": 2
  },
  "c2479f8e": {
    "parent": "23dcc14e",
    "generation": 3,
    "birth_frame": 49,
    "death_frame": 52,
    "lifespan": 3,
    "children": [],
    "peak_mass": 13.538429795055626,
    "dominant_channel": 0
  },
  "20dafb6c": {
    "parent": null,
    "generation": 0,
    "birth_frame": 51,
    "death_frame": 52,
    "lifespan": 1,
    "children": [],
    "peak_mass": 3.2189274496700073,
    "dominant_channel": 2
  },
  "1ecefe45": {
    "parent": null,
    "generation": 0,
    "birth_frame": 54,
    "death_frame": 58,
    "lifespan": 4,
    "children": [],
    "peak_mass": 5.198298779323089,
    "dominant_channel": 2
  },
  "7843366d": {
    "parent": "23dcc14e",
    "generation": 3,
    "birth_frame": 55,
    "death_frame": 60,
    "lifespan": 5,
    "children": [],
    "peak_mass": 13.697742578914264,
    "dominant_channel": 0
  },
  "b5a35175": {
    "parent": null,
    "generation": 0,
    "birth_frame": 55,
    "death_frame": 56,
    "lifespan": 1,
    "children": [],
    "peak_mass": 2.829271163082231,
    "dominant_channel": 2
  },
  "e44430c8": {
    "parent": "23dcc14e",
    "generation": 3,
    "birth_frame": 56,
    "death_frame": 58,
    "lifespan": 2,
    "children": [],
    "peak_mass": 3.498693734389668,
    "dominant_channel": 2
  },
  "6992972c": {
    "parent": "23dcc14e",
    "generation": 3,
    "birth_frame": 58,
    "death_frame": 59,
    "lifespan": 1,
    "children": [],
    "peak_mass": 8.910102578550205,
    "dominant_channel": 0
  },
  "e5a3a468": {
    "parent": null,
    "generation": 0,
    "birth_frame": 59,
    "death_frame": 70,
    "lifespan": 11,
    "children": [],
    "peak_mass": 6.788883230851336,
    "dominant_channel": 2
  },
  "776e9a4d": {
    "parent": null,
    "generation": 0,
    "birth_frame": 60,
    "death_frame": 61,
    "lifespan": 1,
    "children": [],
    "peak_mass": 2.8844473304936034,
    "dominant_channel": 2
  },
  "de999db7": {
    "parent": "23dcc14e",
    "generation": 3,
    "birth_frame": 61,
    "death_frame": 62,
    "lifespan": 1,
    "children": [],
    "peak_mass": 12.573511204469707,
    "dominant_channel": 0
  },
  "af21bad0": {
    "parent": "23dcc14e",
    "generation": 3,
    "birth_frame": 61,
    "death_frame": 75,
    "lifespan": 14,
    "children": [],
    "peak_mass": 7.232004014229754,
    "dominant_channel": 0
  },
  "3f90e687": {
    "parent": "23dcc14e",
    "generation": 3,
    "birth_frame": 63,
    "death_frame": 64,
    "lifespan": 1,
    "children": [],
    "peak_mass": 12.070689890069216,
    "dominant_channel": 0
  },
  "10cfb49b": {
    "parent": "23dcc14e",
    "generation": 3,
    "birth_frame": 65,
    "death_frame": 82,
    "lifespan": 17,
    "children": [
      "291ae587"
    ],
    "peak_mass": 3011.0565908252843,
    "dominant_channel": 0
  },
  "f7ee8913": {
    "parent": "23dcc14e",
    "generation": 3,
    "birth_frame": 65,
    "death_frame": 67,
    "lifespan": 2,
    "children": [],
    "peak_mass": 10.301095492192292,
    "dominant_channel": 0
  },
  "36fbfe32": {
    "parent": "23dcc14e",
    "generation": 3,
    "birth_frame": 66,
    "death_frame": 67,
    "lifespan": 1,
    "children": [],
    "peak_mass": 7.283210463093737,
    "dominant_channel": 0
  },
  "e633a457": {
    "parent": null,
    "generation": 0,
    "birth_frame": 67,
    "death_frame": 68,
    "lifespan": 1,
    "children": [],
    "peak_mass": 2.5104566711148095,
    "dominant_channel": 0
  },
  "f509d230": {
    "parent": null,
    "generation": 0,
    "birth_frame": 67,
    "death_frame": 70,
    "lifespan": 3,
    "children": [],
    "peak_mass": 3.53939820621631,
    "dominant_channel": 2
  },
  "3c351cce": {
    "parent": "23dcc14e",
    "generation": 3,
    "birth_frame": 68,
    "death_frame": 69,
    "lifespan": 1,
    "children": [],
    "peak_mass": 10.41465482225989,
    "dominant_channel": 0
  },
  "b7654454": {
    "parent": "23dcc14e",
    "generation": 3,
    "birth_frame": 68,
    "death_frame": 71,
    "lifespan": 3,
    "children": [],
    "peak_mass": 8.617033095444608,
    "dominant_channel": 0
  },
  "96bc19c4": {
    "parent": null,
    "generation": 0,
    "birth_frame": 68,
    "death_frame": 69,
    "lifespan": 1,
    "children": [],
    "peak_mass": 2.9313120460207718,
    "dominant_channel": 2
  }
}
```

## Media

- `outputs/SPECIES_005_SPLITTER_final.png`
- `outputs/SPECIES_005_SPLITTER.gif`
- `outputs/SPECIES_005_SPLITTER.mp4`

- genome: `outputs/species/SPECIES_005_SPLITTER_genome.json`
