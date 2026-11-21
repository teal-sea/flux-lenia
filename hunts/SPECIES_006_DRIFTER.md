# SPECIES 006 — DRIFTER

**Verdict:** VIABLE + REPRODUCING
**Origin:** random  |  **Seed:** 508

## Viability gates

| gate | verdict | value | detail |
| --- | --- | --- | --- |
| mass_conservation | PASS | 2.36741e-16 | tol=0.0001 |
| non_triviality | PASS | 99.1698 | conc>=6.0, occupancy 0.040<=0.45, 5 bodies |
| persistence | PASS | 1 | 1 organisms alive at the end with lifespan >= 15 frames |
| activity | PASS | 4.38807 | mean speed of the most mobile organism, cells/frame |

## Behaviour (anomaly bouncer)

| behaviour | established | score | evidence |
| --- | --- | --- | --- |
| phototaxis | no | -0.007 | lamp(26, 64): 38.4->38.7; lamp(102, 64): 38.4->38.2; lamp(64, 26): 38.5->36.8 | min approach -0.007 (needs > 0.05 for every lamp position) |
| predatory_pursuit | no | 0.295 | d6ac1f83(ch0) -> 2fcaeedd(ch0) closed 33.5 -> 18.7 cells over 16 frames, monotone 0.67, target speed 2.069 |
| cyclic_locomotion | no | 0.565 | uid=b7902f55 circling=0.18 spectral_power=0.19 period=7.7 frames (counted only if >= 4) life=24 frames |

## Reproduction

Measured on the recording run below (the screening run is sampled more coarsely and its counts differ; both are stated separately rather than mixed).

- Divisions counted (offspring survived AND carried at least 10% of the parent's mass): **8**
- Raw fission events before the mass filter: **17** — the difference is debris a large body shed, which is not reproduction
- Surviving offspring total: **8**
- Organisms tracked in this run: **190**
- Screening run, for comparison: 2 divisions of 6 raw fissions, deepest generation 4

| frame | parent | children | parent mass | child masses | child share |
| --- | --- | --- | --- | --- | --- |
| 36 | `406f537e` | `c0d46279` | 329.8 | 41.1, 23.1, 8.9 | 12% |
| 60 | `060fbf38` | `779e1d80` | 233.3 | 25.7 | 11% |
| 75 | `1a475299` | `7980ef82` | 15.0 | 9.8 | 66% |
| 81 | `8ce3627c` | `d44cf3e2` | 23.2 | 17.1 | 74% |
| 102 | `2fcaeedd` | `bca39500` | 396.1 | 65.5, 20.7, 12.7, 9.9 | 17% |
| 112 | `ba971f89` | `a0445b3d` | 359.2 | 46.2, 13.8 | 13% |
| 113 | `ba971f89` | `4c87d97e` | 298.0 | 67.7 | 23% |
| 140 | `82882047` | `6318b980` | 10.8 | 8.2 | 76% |

## Complexity

```json
{
  "morph_diversity": 3.2686867891823566,
  "spatial_mi": 1.560377443622118,
  "cross_channel_mi": 0.2007180433750222,
  "euler_final": 69,
  "concentration_final": 99.16975006545549,
  "occupancy_final": 0.04022216796875,
  "n_blobs_final": 5,
  "activity": 4.3880715470106,
  "mass_drift": 2.3674051809464654e-16,
  "score": 23.600156398598838
}
```

## Lineage tree

```json
{
  "4b1d8a9d": {
    "parent": null,
    "generation": 0,
    "birth_frame": 0,
    "death_frame": 20,
    "lifespan": 20,
    "children": [
      "016c5ce4"
    ],
    "peak_mass": 953.1768789370551,
    "dominant_channel": 1
  },
  "016c5ce4": {
    "parent": "4b1d8a9d",
    "generation": 1,
    "birth_frame": 19,
    "death_frame": 34,
    "lifespan": 15,
    "children": [
      "f37acefe",
      "82c163c8",
      "21b620bf",
      "ee223148",
      "6490ae45",
      "1867cf77",
      "fcd83453"
    ],
    "peak_mass": 742.0244728517646,
    "dominant_channel": 0
  },
  "f37acefe": {
    "parent": "016c5ce4",
    "generation": 2,
    "birth_frame": 21,
    "death_frame": 23,
    "lifespan": 2,
    "children": [],
    "peak_mass": 10.824567717023193,
    "dominant_channel": 2
  },
  "82c163c8": {
    "parent": "016c5ce4",
    "generation": 2,
    "birth_frame": 21,
    "death_frame": 23,
    "lifespan": 2,
    "children": [],
    "peak_mass": 13.630058910397338,
    "dominant_channel": 2
  },
  "b00848ce": {
    "parent": null,
    "generation": 0,
    "birth_frame": 21,
    "death_frame": 22,
    "lifespan": 1,
    "children": [],
    "peak_mass": 7.6483968530668704,
    "dominant_channel": 2
  },
  "8c47d117": {
    "parent": null,
    "generation": 0,
    "birth_frame": 22,
    "death_frame": 23,
    "lifespan": 1,
    "children": [],
    "peak_mass": 7.959724562298373,
    "dominant_channel": 2
  },
  "21b620bf": {
    "parent": "016c5ce4",
    "generation": 2,
    "birth_frame": 25,
    "death_frame": 27,
    "lifespan": 2,
    "children": [],
    "peak_mass": 23.99497552900951,
    "dominant_channel": 2
  },
  "ee223148": {
    "parent": "016c5ce4",
    "generation": 2,
    "birth_frame": 27,
    "death_frame": 28,
    "lifespan": 1,
    "children": [],
    "peak_mass": 9.630860677283263,
    "dominant_channel": 1
  },
  "1db71553": {
    "parent": null,
    "generation": 0,
    "birth_frame": 27,
    "death_frame": 28,
    "lifespan": 1,
    "children": [],
    "peak_mass": 11.678935509542484,
    "dominant_channel": 1
  },
  "a8651549": {
    "parent": null,
    "generation": 0,
    "birth_frame": 27,
    "death_frame": 28,
    "lifespan": 1,
    "children": [],
    "peak_mass": 7.720228844264543,
    "dominant_channel": 2
  },
  "6490ae45": {
    "parent": "016c5ce4",
    "generation": 2,
    "birth_frame": 28,
    "death_frame": 29,
    "lifespan": 1,
    "children": [
      "6e5d8d04"
    ],
    "peak_mass": 16.960416201294393,
    "dominant_channel": 1
  },
  "6e5d8d04": {
    "parent": "6490ae45",
    "generation": 3,
    "birth_frame": 29,
    "death_frame": 32,
    "lifespan": 3,
    "children": [],
    "peak_mass": 26.30807817844588,
    "dominant_channel": 1
  },
  "6805f168": {
    "parent": null,
    "generation": 0,
    "birth_frame": 29,
    "death_frame": 30,
    "lifespan": 1,
    "children": [],
    "peak_mass": 9.344115804514763,
    "dominant_channel": 1
  },
  "9a2e7105": {
    "parent": null,
    "generation": 0,
    "birth_frame": 29,
    "death_frame": 30,
    "lifespan": 1,
    "children": [],
    "peak_mass": 8.105489563820967,
    "dominant_channel": 2
  },
  "1867cf77": {
    "parent": "016c5ce4",
    "generation": 2,
    "birth_frame": 30,
    "death_frame": 32,
    "lifespan": 2,
    "children": [],
    "peak_mass": 9.988849134019985,
    "dominant_channel": 1
  },
  "2e824735": {
    "parent": null,
    "generation": 0,
    "birth_frame": 31,
    "death_frame": 32,
    "lifespan": 1,
    "children": [],
    "peak_mass": 10.93076631689912,
    "dominant_channel": 2
  },
  "406f537e": {
    "parent": null,
    "generation": 0,
    "birth_frame": 33,
    "death_frame": 39,
    "lifespan": 6,
    "children": [
      "0d207115",
      "50724b82",
      "c0d46279",
      "c00b6ae0",
      "b404ce6f"
    ],
    "peak_mass": 570.2634027617362,
    "dominant_channel": 0
  },
  "83d628b0": {
    "parent": null,
    "generation": 0,
    "birth_frame": 33,
    "death_frame": 36,
    "lifespan": 3,
    "children": [],
    "peak_mass": 13.70959486941097,
    "dominant_channel": 2
  },
  "21763216": {
    "parent": null,
    "generation": 0,
    "birth_frame": 33,
    "death_frame": 35,
    "lifespan": 2,
    "children": [],
    "peak_mass": 10.661580988511435,
    "dominant_channel": 2
  },
  "fcd83453": {
    "parent": "016c5ce4",
    "generation": 2,
    "birth_frame": 34,
    "death_frame": 36,
    "lifespan": 2,
    "children": [],
    "peak_mass": 12.349649090687759,
    "dominant_channel": 2
  },
  "96cf6cee": {
    "parent": null,
    "generation": 0,
    "birth_frame": 34,
    "death_frame": 35,
    "lifespan": 1,
    "children": [],
    "peak_mass": 8.868485103969283,
    "dominant_channel": 1
  },
  "0d207115": {
    "parent": "406f537e",
    "generation": 1,
    "birth_frame": 35,
    "death_frame": 36,
    "lifespan": 1,
    "children": [],
    "peak_mass": 13.54841760217912,
    "dominant_channel": 2
  },
  "50724b82": {
    "parent": "406f537e",
    "generation": 1,
    "birth_frame": 35,
    "death_frame": 36,
    "lifespan": 1,
    "children": [],
    "peak_mass": 12.432038560022125,
    "dominant_channel": 0
  },
  "c0d46279": {
    "parent": "406f537e",
    "generation": 1,
    "birth_frame": 36,
    "death_frame": 44,
    "lifespan": 8,
    "children": [
      "138e1156",
      "3be6e840",
      "273ad14e",
      "7a4ddf06",
      "495931d1"
    ],
    "peak_mass": 632.0331743346717,
    "dominant_channel": 0
  },
  "c00b6ae0": {
    "parent": "406f537e",
    "generation": 1,
    "birth_frame": 36,
    "death_frame": 37,
    "lifespan": 1,
    "children": [
      "7da4620a"
    ],
    "peak_mass": 23.120824906714216,
    "dominant_channel": 0
  },
  "b404ce6f": {
    "parent": "406f537e",
    "generation": 1,
    "birth_frame": 36,
    "death_frame": 37,
    "lifespan": 1,
    "children": [],
    "peak_mass": 8.895843586078623,
    "dominant_channel": 1
  },
  "138e1156": {
    "parent": "c0d46279",
    "generation": 2,
    "birth_frame": 37,
    "death_frame": 39,
    "lifespan": 2,
    "children": [],
    "peak_mass": 16.009933919906057,
    "dominant_channel": 0
  },
  "7da4620a": {
    "parent": "c00b6ae0",
    "generation": 2,
    "birth_frame": 37,
    "death_frame": 39,
    "lifespan": 2,
    "children": [],
    "peak_mass": 20.449102315405277,
    "dominant_channel": 0
  },
  "83117eb2": {
    "parent": null,
    "generation": 0,
    "birth_frame": 37,
    "death_frame": 39,
    "lifespan": 2,
    "children": [],
    "peak_mass": 18.693932931888043,
    "dominant_channel": 2
  },
  "8b708cb9": {
    "parent": null,
    "generation": 0,
    "birth_frame": 40,
    "death_frame": 42,
    "lifespan": 2,
    "children": [],
    "peak_mass": 9.538755671951757,
    "dominant_channel": 2
  },
  "64fcade8": {
    "parent": null,
    "generation": 0,
    "birth_frame": 40,
    "death_frame": 42,
    "lifespan": 2,
    "children": [],
    "peak_mass": 10.715980705548814,
    "dominant_channel": 1
  },
  "3be6e840": {
    "parent": "c0d46279",
    "generation": 2,
    "birth_frame": 41,
    "death_frame": 42,
    "lifespan": 1,
    "children": [],
    "peak_mass": 14.35603248657888,
    "dominant_channel": 1
  },
  "273ad14e": {
    "parent": "c0d46279",
    "generation": 2,
    "birth_frame": 41,
    "death_frame": 43,
    "lifespan": 2,
    "children": [],
    "peak_mass": 10.168701300853836,
    "dominant_channel": 2
  },
  "7a4ddf06": {
    "parent": "c0d46279",
    "generation": 2,
    "birth_frame": 43,
    "death_frame": 55,
    "lifespan": 12,
    "children": [
      "5b38cda7",
      "ed211d8f",
      "037780f0",
      "f31b2408",
      "7ffbf3f2",
      "4d2e29d6",
      "155b7f95",
      "430b8047",
      "76d87e1a",
      "803749ec",
      "37c0ab7e",
      "35ce588a",
      "14366564",
      "060fbf38",
      "0b0f1003",
      "9fed7b4e"
    ],
    "peak_mass": 623.0616547610528,
    "dominant_channel": 0
  },
  "495931d1": {
    "parent": "c0d46279",
    "generation": 2,
    "birth_frame": 43,
    "death_frame": 49,
    "lifespan": 6,
    "children": [],
    "peak_mass": 12.687793592153817,
    "dominant_channel": 2
  },
  "34021390": {
    "parent": null,
    "generation": 0,
    "birth_frame": 44,
    "death_frame": 45,
    "lifespan": 1,
    "children": [],
    "peak_mass": 7.235560875764272,
    "dominant_channel": 2
  },
  "5b38cda7": {
    "parent": "7a4ddf06",
    "generation": 3,
    "birth_frame": 45,
    "death_frame": 46,
    "lifespan": 1,
    "children": [],
    "peak_mass": 18.546152487316146,
    "dominant_channel": 2
  },
  "ed211d8f": {
    "parent": "7a4ddf06",
    "generation": 3,
    "birth_frame": 45,
    "death_frame": 46,
    "lifespan": 1,
    "children": [],
    "peak_mass": 10.907762220959695,
    "dominant_channel": 2
  },
  "037780f0": {
    "parent": "7a4ddf06",
    "generation": 3,
    "birth_frame": 45,
    "death_frame": 48,
    "lifespan": 3,
    "children": [],
    "peak_mass": 9.971452620195821,
    "dominant_channel": 2
  },
  "f31b2408": {
    "parent": "7a4ddf06",
    "generation": 3,
    "birth_frame": 45,
    "death_frame": 46,
    "lifespan": 1,
    "children": [],
    "peak_mass": 7.224971563857094,
    "dominant_channel": 1
  }
}
```

## Media

- `outputs/SPECIES_006_DRIFTER_final.png`
- `outputs/SPECIES_006_DRIFTER.gif`
- `outputs/SPECIES_006_DRIFTER.mp4`

- genome: `outputs/species/SPECIES_006_DRIFTER_genome.json`
