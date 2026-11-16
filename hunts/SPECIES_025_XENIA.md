# SPECIES 025 — XENIA

**Verdict:** VIABLE + REPRODUCING
**Origin:** random  |  **Seed:** 882

## Viability gates

| gate | verdict | value | detail |
| --- | --- | --- | --- |
| mass_conservation | PASS | 1.45264e-16 | tol=0.0001 |
| non_triviality | PASS | 19.4853 | conc>=6.0, occupancy 0.200<=0.45, 6 bodies |
| persistence | PASS | 3 | 3 organisms alive at the end with lifespan >= 15 frames |
| activity | PASS | 0.839322 | mean speed of the most mobile organism, cells/frame |

## Behaviour (anomaly bouncer)

| behaviour | established | score | evidence |
| --- | --- | --- | --- |
| phototaxis | no | 0.003 | lamp(26, 64): 38.5->38.4; lamp(102, 64): 38.3->38.1; lamp(64, 26): 38.4->37.9 | min approach +0.003 (needs > 0.05 for every lamp position) |
| predatory_pursuit | no | 0.233 | b29ff489(ch0) -> e5a0a726(ch1) closed 47.5 -> 29.4 cells over 19 frames, monotone 0.61, target speed 2.139 |
| cyclic_locomotion | no | 0.311 | uid=395d8718 circling=0.08 spectral_power=0.10 period=20.0 frames (counted only if >= 4) life=41 frames |

## Reproduction

Measured on the recording run below (the screening run is sampled more coarsely and its counts differ; both are stated separately rather than mixed).

- Divisions counted (offspring survived AND carried at least 10% of the parent's mass): **2**
- Raw fission events before the mass filter: **11** — the difference is debris a large body shed, which is not reproduction
- Surviving offspring total: **2**
- Organisms tracked in this run: **56**
- Screening run, for comparison: 1 divisions of 6 raw fissions, deepest generation 2

| frame | parent | children | parent mass | child masses | child share |
| --- | --- | --- | --- | --- | --- |
| 108 | `a91ab42f` | `d481a237` | 76.9 | 19.2 | 25% |
| 116 | `d10494ad` | `e5a0a726` | 708.6 | 143.2, 58.9, 47.5 | 20% |

## Complexity

```json
{
  "morph_diversity": 2.6368564313745426,
  "spatial_mi": 1.3500094482508893,
  "cross_channel_mi": 0.7805798916188663,
  "euler_final": -19,
  "concentration_final": 19.485329570329597,
  "occupancy_final": 0.19976806640625,
  "n_blobs_final": 6,
  "activity": 0.8393219519865206,
  "mass_drift": 1.4526447150552763e-16,
  "score": 15.24306284353822
}
```

## Lineage tree

```json
{
  "d10494ad": {
    "parent": null,
    "generation": 0,
    "birth_frame": 0,
    "death_frame": 119,
    "lifespan": 119,
    "children": [
      "a4a84f7f",
      "8d05b24e",
      "b29ff489",
      "b7d78ec8",
      "770e2331",
      "1b8573e4",
      "6c2e75e2",
      "a91ab42f",
      "0689e50e",
      "2e4be878",
      "fe101b01",
      "c773fbdb",
      "2fb6882d",
      "d3a1b94e",
      "1b5282b2",
      "645430a9",
      "cb0b392e",
      "4cb92a4e",
      "61744e35",
      "ffb2cbf4",
      "5f72c6c7",
      "35abf685",
      "395d8718",
      "dd1fd6b1",
      "c2396d83",
      "b1b54d58",
      "75daa815",
      "e5a0a726",
      "b817c378",
      "2acb7d81"
    ],
    "peak_mass": 1550.2174020571913,
    "dominant_channel": 1
  },
  "a4a84f7f": {
    "parent": "d10494ad",
    "generation": 1,
    "birth_frame": 29,
    "death_frame": 31,
    "lifespan": 2,
    "children": [],
    "peak_mass": 4.793670955118458,
    "dominant_channel": 1
  },
  "2cfe0e60": {
    "parent": null,
    "generation": 0,
    "birth_frame": 70,
    "death_frame": 71,
    "lifespan": 1,
    "children": [],
    "peak_mass": 3.6541429123428926,
    "dominant_channel": 2
  },
  "8d05b24e": {
    "parent": "d10494ad",
    "generation": 1,
    "birth_frame": 72,
    "death_frame": 73,
    "lifespan": 1,
    "children": [],
    "peak_mass": 4.788243198469092,
    "dominant_channel": 2
  },
  "b29ff489": {
    "parent": "d10494ad",
    "generation": 1,
    "birth_frame": 75,
    "death_frame": 135,
    "lifespan": 60,
    "children": [
      "9881f49a"
    ],
    "peak_mass": 26.66600127517264,
    "dominant_channel": 0
  },
  "636303a1": {
    "parent": null,
    "generation": 0,
    "birth_frame": 77,
    "death_frame": 82,
    "lifespan": 5,
    "children": [],
    "peak_mass": 3.167334130976232,
    "dominant_channel": 2
  },
  "b7d78ec8": {
    "parent": "d10494ad",
    "generation": 1,
    "birth_frame": 80,
    "death_frame": 81,
    "lifespan": 1,
    "children": [],
    "peak_mass": 25.85996891936769,
    "dominant_channel": 0
  },
  "770e2331": {
    "parent": "d10494ad",
    "generation": 1,
    "birth_frame": 82,
    "death_frame": 88,
    "lifespan": 6,
    "children": [],
    "peak_mass": 49.38948850063445,
    "dominant_channel": 1
  },
  "1b8573e4": {
    "parent": "d10494ad",
    "generation": 1,
    "birth_frame": 82,
    "death_frame": 134,
    "lifespan": 52,
    "children": [],
    "peak_mass": 26.632079853720942,
    "dominant_channel": 0
  },
  "f1815e92": {
    "parent": null,
    "generation": 0,
    "birth_frame": 83,
    "death_frame": 85,
    "lifespan": 2,
    "children": [],
    "peak_mass": 2.9752273501685043,
    "dominant_channel": 2
  },
  "6c2e75e2": {
    "parent": "d10494ad",
    "generation": 1,
    "birth_frame": 88,
    "death_frame": 105,
    "lifespan": 17,
    "children": [],
    "peak_mass": 27.337255441995705,
    "dominant_channel": 0
  },
  "a91ab42f": {
    "parent": "d10494ad",
    "generation": 1,
    "birth_frame": 88,
    "death_frame": 116,
    "lifespan": 28,
    "children": [
      "d481a237",
      "a1bc0f40"
    ],
    "peak_mass": 98.15629081535143,
    "dominant_channel": 1
  },
  "0689e50e": {
    "parent": "d10494ad",
    "generation": 1,
    "birth_frame": 91,
    "death_frame": 105,
    "lifespan": 14,
    "children": [],
    "peak_mass": 76.36022062996082,
    "dominant_channel": 1
  },
  "2e4be878": {
    "parent": "d10494ad",
    "generation": 1,
    "birth_frame": 91,
    "death_frame": 92,
    "lifespan": 1,
    "children": [],
    "peak_mass": 14.801258402868243,
    "dominant_channel": 2
  },
  "fe101b01": {
    "parent": "d10494ad",
    "generation": 1,
    "birth_frame": 91,
    "death_frame": 143,
    "lifespan": 52,
    "children": [],
    "peak_mass": 14.240115749386408,
    "dominant_channel": 0
  },
  "c773fbdb": {
    "parent": "d10494ad",
    "generation": 1,
    "birth_frame": 92,
    "death_frame": 96,
    "lifespan": 4,
    "children": [],
    "peak_mass": 86.52586348787989,
    "dominant_channel": 1
  },
  "2fb6882d": {
    "parent": "d10494ad",
    "generation": 1,
    "birth_frame": 94,
    "death_frame": 96,
    "lifespan": 2,
    "children": [],
    "peak_mass": 39.823051649306436,
    "dominant_channel": 1
  },
  "d3a1b94e": {
    "parent": "d10494ad",
    "generation": 1,
    "birth_frame": 94,
    "death_frame": 96,
    "lifespan": 2,
    "children": [],
    "peak_mass": 11.895733770805158,
    "dominant_channel": 0
  },
  "1b5282b2": {
    "parent": "d10494ad",
    "generation": 1,
    "birth_frame": 94,
    "death_frame": 95,
    "lifespan": 1,
    "children": [],
    "peak_mass": 11.337064122189439,
    "dominant_channel": 2
  },
  "645430a9": {
    "parent": "d10494ad",
    "generation": 1,
    "birth_frame": 94,
    "death_frame": 96,
    "lifespan": 2,
    "children": [],
    "peak_mass": 8.79687573805754,
    "dominant_channel": 2
  },
  "cb0b392e": {
    "parent": "d10494ad",
    "generation": 1,
    "birth_frame": 94,
    "death_frame": 96,
    "lifespan": 2,
    "children": [],
    "peak_mass": 11.790625333933557,
    "dominant_channel": 2
  },
  "4cb92a4e": {
    "parent": "d10494ad",
    "generation": 1,
    "birth_frame": 98,
    "death_frame": 99,
    "lifespan": 1,
    "children": [],
    "peak_mass": 85.97861171909342,
    "dominant_channel": 1
  },
  "61744e35": {
    "parent": "d10494ad",
    "generation": 1,
    "birth_frame": 101,
    "death_frame": 102,
    "lifespan": 1,
    "children": [],
    "peak_mass": 39.93499426837314,
    "dominant_channel": 1
  },
  "ffb2cbf4": {
    "parent": "d10494ad",
    "generation": 1,
    "birth_frame": 101,
    "death_frame": 104,
    "lifespan": 3,
    "children": [],
    "peak_mass": 13.047167701156484,
    "dominant_channel": 0
  },
  "5f72c6c7": {
    "parent": "d10494ad",
    "generation": 1,
    "birth_frame": 106,
    "death_frame": 119,
    "lifespan": 13,
    "children": [],
    "peak_mass": 27.702828732088133,
    "dominant_channel": 0
  },
  "d481a237": {
    "parent": "a91ab42f",
    "generation": 2,
    "birth_frame": 108,
    "death_frame": null,
    "lifespan": 43,
    "children": [],
    "peak_mass": 19.636720589277893,
    "dominant_channel": 0
  },
  "35abf685": {
    "parent": "d10494ad",
    "generation": 1,
    "birth_frame": 110,
    "death_frame": 118,
    "lifespan": 8,
    "children": [],
    "peak_mass": 57.77831084236299,
    "dominant_channel": 1
  },
  "395d8718": {
    "parent": "d10494ad",
    "generation": 1,
    "birth_frame": 110,
    "death_frame": null,
    "lifespan": 41,
    "children": [],
    "peak_mass": 12.468286272255584,
    "dominant_channel": 0
  },
  "dd1fd6b1": {
    "parent": "d10494ad",
    "generation": 1,
    "birth_frame": 113,
    "death_frame": 115,
    "lifespan": 2,
    "children": [],
    "peak_mass": 81.54418473638131,
    "dominant_channel": 1
  },
  "c2396d83": {
    "parent": "d10494ad",
    "generation": 1,
    "birth_frame": 114,
    "death_frame": 117,
    "lifespan": 3,
    "children": [
      "05805f22"
    ],
    "peak_mass": 90.47810205009927,
    "dominant_channel": 1
  },
  "b1b54d58": {
    "parent": "d10494ad",
    "generation": 1,
    "birth_frame": 115,
    "death_frame": 117,
    "lifespan": 2,
    "children": [],
    "peak_mass": 30.94193586894835,
    "dominant_channel": 0
  },
  "75daa815": {
    "parent": "d10494ad",
    "generation": 1,
    "birth_frame": 115,
    "death_frame": 117,
    "lifespan": 2,
    "children": [],
    "peak_mass": 14.61198916873738,
    "dominant_channel": 2
  },
  "a1bc0f40": {
    "parent": "a91ab42f",
    "generation": 2,
    "birth_frame": 115,
    "death_frame": 119,
    "lifespan": 4,
    "children": [],
    "peak_mass": 75.54169181295575,
    "dominant_channel": 1
  },
  "e5a0a726": {
    "parent": "d10494ad",
    "generation": 1,
    "birth_frame": 116,
    "death_frame": null,
    "lifespan": 35,
    "children": [
      "9f3a9459",
      "c803b5ba",
      "8bb6b92f",
      "749c74ec",
      "71efe5ed",
      "eecccd7e",
      "59829d18",
      "866a8965",
      "1fea19e9",
      "83c9b947",
      "8d1f2f10",
      "d296ea6b",
      "21c32da1",
      "cffd9cfb",
      "191c00bd",
      "22eab7e3",
      "6199cf1f"
    ],
    "peak_mass": 1410.3225747798308,
    "dominant_channel": 1
  },
  "b817c378": {
    "parent": "d10494ad",
    "generation": 1,
    "birth_frame": 116,
    "death_frame": 117,
    "lifespan": 1,
    "children": [
      "ad4a82f8"
    ],
    "peak_mass": 58.87743293356927,
    "dominant_channel": 1
  },
  "2acb7d81": {
    "parent": "d10494ad",
    "generation": 1,
    "birth_frame": 116,
    "death_frame": 119,
    "lifespan": 3,
    "children": [],
    "peak_mass": 48.0284058522882,
    "dominant_channel": 1
  },
  "9881f49a": {
    "parent": "b29ff489",
    "generation": 2,
    "birth_frame": 116,
    "death_frame": 119,
    "lifespan": 3,
    "children": [],
    "peak_mass": 6.883872697830092,
    "dominant_channel": 0
  },
  "05805f22": {
    "parent": "c2396d83",
    "generation": 2,
    "birth_frame": 117,
    "death_frame": 119,
    "lifespan": 2,
    "children": [],
    "peak_mass": 16.955067426775713,
    "dominant_channel": 0
  },
  "ad4a82f8": {
    "parent": "b817c378",
    "generation": 2,
    "birth_frame": 117,
    "death_frame": 118,
    "lifespan": 1,
    "children": [],
    "peak_mass": 39.55877927412798,
    "dominant_channel": 1
  },
  "9f3a9459": {
    "parent": "e5a0a726",
    "generation": 2,
    "birth_frame": 125,
    "death_frame": 126,
    "lifespan": 1,
    "children": [],
    "peak_mass": 17.820302754900272,
    "dominant_channel": 0
  }
}
```

## Media

- `outputs/SPECIES_025_XENIA_final.png`
- `outputs/SPECIES_025_XENIA.gif`
- note: ffmpeg not on PATH; GIF written instead

- genome: `outputs/species/SPECIES_025_XENIA_genome.json`
