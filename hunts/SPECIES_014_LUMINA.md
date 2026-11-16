# SPECIES 014 — LUMINA

**Verdict:** VIABLE + REPRODUCING
**Origin:** random  |  **Seed:** 679

## Viability gates

| gate | verdict | value | detail |
| --- | --- | --- | --- |
| mass_conservation | PASS | 1.64275e-16 | tol=0.0001 |
| non_triviality | PASS | 76.0995 | conc>=6.0, occupancy 0.045<=0.45, 8 bodies |
| persistence | PASS | 1 | 1 organisms alive at the end with lifespan >= 15 frames |
| activity | PASS | 3.64355 | mean speed of the most mobile organism, cells/frame |

## Behaviour (anomaly bouncer)

| behaviour | established | score | evidence |
| --- | --- | --- | --- |
| phototaxis | no | 0.010 | lamp(26, 64): 38.3->37.4; lamp(102, 64): 38.5->38.1; lamp(64, 26): 38.5->37.3 | min approach +0.010 (needs > 0.05 for every lamp position) |
| predatory_pursuit | no | 0.277 | edc3e7fe(ch1) -> 3ace516c(ch1) closed 20.3 -> 12.8 cells over 56 frames, monotone 0.75, target speed 0.275 |
| cyclic_locomotion | YES | 0.666 | uid=99e00679 circling=0.45 spectral_power=0.22 period=23.0 frames (counted only if >= 4) life=24 frames |

## Reproduction

Measured on the recording run below (the screening run is sampled more coarsely and its counts differ; both are stated separately rather than mixed).

- Divisions counted (offspring survived AND carried at least 10% of the parent's mass): **9**
- Raw fission events before the mass filter: **21** — the difference is debris a large body shed, which is not reproduction
- Surviving offspring total: **9**
- Organisms tracked in this run: **74**
- Screening run, for comparison: 3 divisions of 12 raw fissions, deepest generation 3

| frame | parent | children | parent mass | child masses | child share |
| --- | --- | --- | --- | --- | --- |
| 60 | `830e85e2` | `99e00679` | 22.6 | 11.3, 10.5 | 50% |
| 62 | `830e85e2` | `d52b7577` | 10.9 | 10.3, 7.9 | 73% |
| 72 | `7b7be170` | `7c4711ae` | 14.4 | 14.1 | 98% |
| 92 | `391fdd37` | `b29720d2` | 12.9 | 7.0 | 54% |
| 108 | `391fdd37` | `3ca7d1f5` | 9.5 | 6.0 | 63% |
| 117 | `3ca7d1f5` | `5dab7d19` | 11.6 | 7.4 | 64% |
| 122 | `83e050fb` | `f52148b4` | 374.6 | 56.2 | 15% |
| 128 | `83e050fb` | `15d554a2` | 315.8 | 51.4 | 16% |
| 144 | `3ca7d1f5` | `3bfb01d3` | 15.2 | 10.9 | 72% |

## Complexity

```json
{
  "morph_diversity": 3.1970468480965777,
  "spatial_mi": 1.5123730817278334,
  "cross_channel_mi": 0.8722153129835218,
  "euler_final": 57,
  "concentration_final": 76.09946636113463,
  "occupancy_final": 0.0452880859375,
  "n_blobs_final": 8,
  "activity": 3.643548367652221,
  "mass_drift": 1.6427482949530466e-16,
  "score": 33.16050365153089
}
```

## Lineage tree

```json
{
  "cf3d4a23": {
    "parent": null,
    "generation": 0,
    "birth_frame": 0,
    "death_frame": 55,
    "lifespan": 55,
    "children": [
      "2b2ff438",
      "e6d689b3",
      "270d483a",
      "98382a76",
      "b2acb59c",
      "fc59cf40",
      "879b1eb4",
      "8a182796",
      "fe5eaed7",
      "830e85e2",
      "af35c9b4",
      "1c4ce68a",
      "9d407be7"
    ],
    "peak_mass": 686.9119576350997,
    "dominant_channel": 2
  },
  "2b2ff438": {
    "parent": "cf3d4a23",
    "generation": 1,
    "birth_frame": 24,
    "death_frame": 28,
    "lifespan": 4,
    "children": [],
    "peak_mass": 19.98599677151175,
    "dominant_channel": 2
  },
  "e6d689b3": {
    "parent": "cf3d4a23",
    "generation": 1,
    "birth_frame": 27,
    "death_frame": 28,
    "lifespan": 1,
    "children": [],
    "peak_mass": 4.442073744352383,
    "dominant_channel": 1
  },
  "270d483a": {
    "parent": "cf3d4a23",
    "generation": 1,
    "birth_frame": 29,
    "death_frame": 31,
    "lifespan": 2,
    "children": [],
    "peak_mass": 18.63675188052726,
    "dominant_channel": 2
  },
  "98382a76": {
    "parent": "cf3d4a23",
    "generation": 1,
    "birth_frame": 32,
    "death_frame": 33,
    "lifespan": 1,
    "children": [],
    "peak_mass": 22.082712448685957,
    "dominant_channel": 2
  },
  "b2acb59c": {
    "parent": "cf3d4a23",
    "generation": 1,
    "birth_frame": 32,
    "death_frame": 34,
    "lifespan": 2,
    "children": [],
    "peak_mass": 20.656846628600906,
    "dominant_channel": 2
  },
  "fc59cf40": {
    "parent": "cf3d4a23",
    "generation": 1,
    "birth_frame": 34,
    "death_frame": 35,
    "lifespan": 1,
    "children": [],
    "peak_mass": 21.201655107993002,
    "dominant_channel": 2
  },
  "879b1eb4": {
    "parent": "cf3d4a23",
    "generation": 1,
    "birth_frame": 35,
    "death_frame": 45,
    "lifespan": 10,
    "children": [],
    "peak_mass": 28.579204344439084,
    "dominant_channel": 2
  },
  "8a182796": {
    "parent": "cf3d4a23",
    "generation": 1,
    "birth_frame": 35,
    "death_frame": 38,
    "lifespan": 3,
    "children": [],
    "peak_mass": 21.09526507611596,
    "dominant_channel": 2
  },
  "5d66b0fa": {
    "parent": null,
    "generation": 0,
    "birth_frame": 37,
    "death_frame": 39,
    "lifespan": 2,
    "children": [],
    "peak_mass": 4.011076351708112,
    "dominant_channel": 1
  },
  "fe5eaed7": {
    "parent": "cf3d4a23",
    "generation": 1,
    "birth_frame": 38,
    "death_frame": 40,
    "lifespan": 2,
    "children": [],
    "peak_mass": 15.229833442291477,
    "dominant_channel": 2
  },
  "9990b997": {
    "parent": null,
    "generation": 0,
    "birth_frame": 40,
    "death_frame": 42,
    "lifespan": 2,
    "children": [],
    "peak_mass": 4.357002231221682,
    "dominant_channel": 1
  },
  "830e85e2": {
    "parent": "cf3d4a23",
    "generation": 1,
    "birth_frame": 41,
    "death_frame": 63,
    "lifespan": 22,
    "children": [
      "b3c874e7",
      "99e00679",
      "8201bb8b",
      "dd96e6ed",
      "d52b7577"
    ],
    "peak_mass": 47.76034227927285,
    "dominant_channel": 2
  },
  "af35c9b4": {
    "parent": "cf3d4a23",
    "generation": 1,
    "birth_frame": 45,
    "death_frame": 56,
    "lifespan": 11,
    "children": [],
    "peak_mass": 30.088737510282574,
    "dominant_channel": 2
  },
  "1c4ce68a": {
    "parent": "cf3d4a23",
    "generation": 1,
    "birth_frame": 46,
    "death_frame": 49,
    "lifespan": 3,
    "children": [],
    "peak_mass": 16.787503037523937,
    "dominant_channel": 2
  },
  "9d407be7": {
    "parent": "cf3d4a23",
    "generation": 1,
    "birth_frame": 47,
    "death_frame": 70,
    "lifespan": 23,
    "children": [
      "22bbd532",
      "2df6fea5",
      "811fb5df",
      "db0838c9",
      "ad30926f",
      "513753c8",
      "9857b8f4"
    ],
    "peak_mass": 549.2419007332695,
    "dominant_channel": 2
  },
  "b3c874e7": {
    "parent": "830e85e2",
    "generation": 2,
    "birth_frame": 50,
    "death_frame": 52,
    "lifespan": 2,
    "children": [],
    "peak_mass": 12.035474532055659,
    "dominant_channel": 2
  },
  "a7680c3d": {
    "parent": null,
    "generation": 0,
    "birth_frame": 54,
    "death_frame": 62,
    "lifespan": 8,
    "children": [],
    "peak_mass": 7.139428870317179,
    "dominant_channel": 1
  },
  "2b295a60": {
    "parent": null,
    "generation": 0,
    "birth_frame": 55,
    "death_frame": 56,
    "lifespan": 1,
    "children": [],
    "peak_mass": 3.8185627924771,
    "dominant_channel": 1
  },
  "6124d674": {
    "parent": null,
    "generation": 0,
    "birth_frame": 55,
    "death_frame": 59,
    "lifespan": 4,
    "children": [],
    "peak_mass": 6.229303711712708,
    "dominant_channel": 1
  },
  "22bbd532": {
    "parent": "9d407be7",
    "generation": 2,
    "birth_frame": 57,
    "death_frame": 77,
    "lifespan": 20,
    "children": [
      "8fa357e2",
      "28585ae3"
    ],
    "peak_mass": 31.28487333113506,
    "dominant_channel": 2
  },
  "99e00679": {
    "parent": "830e85e2",
    "generation": 2,
    "birth_frame": 60,
    "death_frame": 84,
    "lifespan": 24,
    "children": [],
    "peak_mass": 11.294659231050575,
    "dominant_channel": 2
  },
  "8201bb8b": {
    "parent": "830e85e2",
    "generation": 2,
    "birth_frame": 60,
    "death_frame": 62,
    "lifespan": 2,
    "children": [],
    "peak_mass": 10.496579254572577,
    "dominant_channel": 2
  },
  "2df6fea5": {
    "parent": "9d407be7",
    "generation": 2,
    "birth_frame": 61,
    "death_frame": 63,
    "lifespan": 2,
    "children": [],
    "peak_mass": 7.6513465210638465,
    "dominant_channel": 1
  },
  "8fa357e2": {
    "parent": "22bbd532",
    "generation": 3,
    "birth_frame": 62,
    "death_frame": 65,
    "lifespan": 3,
    "children": [],
    "peak_mass": 8.133164239694244,
    "dominant_channel": 1
  },
  "28585ae3": {
    "parent": "22bbd532",
    "generation": 3,
    "birth_frame": 62,
    "death_frame": 65,
    "lifespan": 3,
    "children": [],
    "peak_mass": 6.5793281612133345,
    "dominant_channel": 1
  },
  "dd96e6ed": {
    "parent": "830e85e2",
    "generation": 2,
    "birth_frame": 62,
    "death_frame": 63,
    "lifespan": 1,
    "children": [],
    "peak_mass": 10.346624489100442,
    "dominant_channel": 2
  },
  "d52b7577": {
    "parent": "830e85e2",
    "generation": 2,
    "birth_frame": 62,
    "death_frame": 71,
    "lifespan": 9,
    "children": [],
    "peak_mass": 12.599255009522038,
    "dominant_channel": 1
  },
  "811fb5df": {
    "parent": "9d407be7",
    "generation": 2,
    "birth_frame": 63,
    "death_frame": 64,
    "lifespan": 1,
    "children": [],
    "peak_mass": 5.963064490688332,
    "dominant_channel": 2
  },
  "cdb01b0e": {
    "parent": null,
    "generation": 0,
    "birth_frame": 63,
    "death_frame": 66,
    "lifespan": 3,
    "children": [],
    "peak_mass": 5.42977003859169,
    "dominant_channel": 1
  },
  "db0838c9": {
    "parent": "9d407be7",
    "generation": 2,
    "birth_frame": 64,
    "death_frame": 65,
    "lifespan": 1,
    "children": [],
    "peak_mass": 18.05282548568351,
    "dominant_channel": 2
  },
  "ad30926f": {
    "parent": "9d407be7",
    "generation": 2,
    "birth_frame": 65,
    "death_frame": 67,
    "lifespan": 2,
    "children": [],
    "peak_mass": 6.5128539908955325,
    "dominant_channel": 1
  },
  "513753c8": {
    "parent": "9d407be7",
    "generation": 2,
    "birth_frame": 66,
    "death_frame": 68,
    "lifespan": 2,
    "children": [],
    "peak_mass": 13.59753983123155,
    "dominant_channel": 1
  },
  "eadd6c19": {
    "parent": null,
    "generation": 0,
    "birth_frame": 68,
    "death_frame": 71,
    "lifespan": 3,
    "children": [],
    "peak_mass": 5.38800982584954,
    "dominant_channel": 1
  },
  "9857b8f4": {
    "parent": "9d407be7",
    "generation": 2,
    "birth_frame": 69,
    "death_frame": 71,
    "lifespan": 2,
    "children": [
      "7b7be170"
    ],
    "peak_mass": 507.4863831009758,
    "dominant_channel": 2
  },
  "276a73a2": {
    "parent": null,
    "generation": 0,
    "birth_frame": 69,
    "death_frame": 89,
    "lifespan": 20,
    "children": [
      "09a0215c",
      "194bc74c",
      "e16db9c2",
      "8716e096",
      "ce7f3efb",
      "8e7b1b91",
      "a0fff7b5",
      "135a8564"
    ],
    "peak_mass": 521.1330413823206,
    "dominant_channel": 2
  },
  "7b7be170": {
    "parent": "9857b8f4",
    "generation": 3,
    "birth_frame": 71,
    "death_frame": 74,
    "lifespan": 3,
    "children": [
      "7c4711ae",
      "cb4fa436"
    ],
    "peak_mass": 29.34235065164424,
    "dominant_channel": 1
  },
  "f0df1f90": {
    "parent": null,
    "generation": 0,
    "birth_frame": 71,
    "death_frame": 73,
    "lifespan": 2,
    "children": [],
    "peak_mass": 6.810463849373117,
    "dominant_channel": 1
  },
  "09a0215c": {
    "parent": "276a73a2",
    "generation": 1,
    "birth_frame": 72,
    "death_frame": 74,
    "lifespan": 2,
    "children": [],
    "peak_mass": 7.30795830401377,
    "dominant_channel": 1
  },
  "7c4711ae": {
    "parent": "7b7be170",
    "generation": 4,
    "birth_frame": 72,
    "death_frame": 84,
    "lifespan": 12,
    "children": [],
    "peak_mass": 19.157105042505503,
    "dominant_channel": 1
  }
}
```

## Media

- `outputs/SPECIES_014_LUMINA_final.png`
- `outputs/SPECIES_014_LUMINA.gif`
- `outputs/SPECIES_014_LUMINA.mp4`

- genome: `outputs/species/SPECIES_014_LUMINA_genome.json`
