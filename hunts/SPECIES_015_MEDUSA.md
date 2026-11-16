# SPECIES 015 — MEDUSA

**Verdict:** VIABLE + REPRODUCING
**Origin:** random  |  **Seed:** 709

## Viability gates

| gate | verdict | value | detail |
| --- | --- | --- | --- |
| mass_conservation | PASS | 1.50649e-16 | tol=0.0001 |
| non_triviality | PASS | 30.9555 | conc>=6.0, occupancy 0.124<=0.45, 1 bodies |
| persistence | PASS | 1 | 1 organisms alive at the end with lifespan >= 15 frames |
| activity | PASS | 0.379541 | mean speed of the most mobile organism, cells/frame |

## Behaviour (anomaly bouncer)

| behaviour | established | score | evidence |
| --- | --- | --- | --- |
| phototaxis | no | -0.017 | lamp(26, 64): 38.4->37.3; lamp(102, 64): 38.4->39.0; lamp(64, 26): 38.3->38.5 | min approach -0.017 (needs > 0.05 for every lamp position) |
| predatory_pursuit | no | 0.000 | no closing pair found |
| cyclic_locomotion | no | 0.098 | uid=87261b7a circling=0.10 spectral_power=0.02 period=3.6 frames (counted only if >= 4) life=124 frames |

## Reproduction

Measured on the recording run below (the screening run is sampled more coarsely and its counts differ; both are stated separately rather than mixed).

- Divisions counted (offspring survived AND carried at least 10% of the parent's mass): **0**
- Raw fission events before the mass filter: **2** — the difference is debris a large body shed, which is not reproduction
- Surviving offspring total: **0**
- Organisms tracked in this run: **30**
- Screening run, for comparison: 1 divisions of 1 raw fissions, deepest generation 2

## Complexity

```json
{
  "morph_diversity": 0.43278734976150857,
  "spatial_mi": 1.4245807507383774,
  "cross_channel_mi": 0.6264630385106238,
  "euler_final": -13,
  "concentration_final": 30.955535678489714,
  "occupancy_final": 0.1243896484375,
  "n_blobs_final": 1,
  "activity": 0.37954124269447526,
  "mass_drift": 1.5064922560425245e-16,
  "score": 13.59153694719149
}
```

## Lineage tree

```json
{
  "a44cb02a": {
    "parent": null,
    "generation": 0,
    "birth_frame": 0,
    "death_frame": 17,
    "lifespan": 17,
    "children": [
      "97b3c102",
      "36a3ca2b",
      "6d8d68b7",
      "bf4c4a27",
      "24b042f2",
      "69fa1b46",
      "25ef886c"
    ],
    "peak_mass": 746.0929468332721,
    "dominant_channel": 1
  },
  "97b3c102": {
    "parent": "a44cb02a",
    "generation": 1,
    "birth_frame": 7,
    "death_frame": 8,
    "lifespan": 1,
    "children": [],
    "peak_mass": 7.590891425447918,
    "dominant_channel": 2
  },
  "36a3ca2b": {
    "parent": "a44cb02a",
    "generation": 1,
    "birth_frame": 9,
    "death_frame": 12,
    "lifespan": 3,
    "children": [],
    "peak_mass": 16.168723907210442,
    "dominant_channel": 2
  },
  "6d8d68b7": {
    "parent": "a44cb02a",
    "generation": 1,
    "birth_frame": 9,
    "death_frame": 10,
    "lifespan": 1,
    "children": [],
    "peak_mass": 6.642191349469104,
    "dominant_channel": 2
  },
  "bf4c4a27": {
    "parent": "a44cb02a",
    "generation": 1,
    "birth_frame": 9,
    "death_frame": 10,
    "lifespan": 1,
    "children": [],
    "peak_mass": 6.626913376567798,
    "dominant_channel": 2
  },
  "24b042f2": {
    "parent": "a44cb02a",
    "generation": 1,
    "birth_frame": 9,
    "death_frame": 10,
    "lifespan": 1,
    "children": [],
    "peak_mass": 6.269800531339815,
    "dominant_channel": 2
  },
  "69fa1b46": {
    "parent": "a44cb02a",
    "generation": 1,
    "birth_frame": 9,
    "death_frame": 10,
    "lifespan": 1,
    "children": [],
    "peak_mass": 5.823046075523291,
    "dominant_channel": 2
  },
  "0ed9e0a4": {
    "parent": null,
    "generation": 0,
    "birth_frame": 13,
    "death_frame": 18,
    "lifespan": 5,
    "children": [
      "8d982ad9",
      "83dacdac"
    ],
    "peak_mass": 532.8190281685103,
    "dominant_channel": 1
  },
  "ba7f5845": {
    "parent": null,
    "generation": 0,
    "birth_frame": 13,
    "death_frame": 14,
    "lifespan": 1,
    "children": [],
    "peak_mass": 6.571685942502219,
    "dominant_channel": 2
  },
  "9b27650e": {
    "parent": null,
    "generation": 0,
    "birth_frame": 14,
    "death_frame": 20,
    "lifespan": 6,
    "children": [
      "2d6c1f3f",
      "2e973069",
      "88126a7c"
    ],
    "peak_mass": 508.5197814855445,
    "dominant_channel": 1
  },
  "7a63ff5f": {
    "parent": null,
    "generation": 0,
    "birth_frame": 14,
    "death_frame": 17,
    "lifespan": 3,
    "children": [],
    "peak_mass": 13.465825773441122,
    "dominant_channel": 2
  },
  "fe0cbf95": {
    "parent": null,
    "generation": 0,
    "birth_frame": 15,
    "death_frame": 17,
    "lifespan": 2,
    "children": [],
    "peak_mass": 8.083844846387228,
    "dominant_channel": 2
  },
  "fee57b46": {
    "parent": null,
    "generation": 0,
    "birth_frame": 15,
    "death_frame": 16,
    "lifespan": 1,
    "children": [],
    "peak_mass": 8.595130432048014,
    "dominant_channel": 2
  },
  "25ef886c": {
    "parent": "a44cb02a",
    "generation": 1,
    "birth_frame": 16,
    "death_frame": 17,
    "lifespan": 1,
    "children": [],
    "peak_mass": 22.470315669093676,
    "dominant_channel": 2
  },
  "2d6c1f3f": {
    "parent": "9b27650e",
    "generation": 1,
    "birth_frame": 18,
    "death_frame": 19,
    "lifespan": 1,
    "children": [],
    "peak_mass": 15.472146708085162,
    "dominant_channel": 2
  },
  "2e973069": {
    "parent": "9b27650e",
    "generation": 1,
    "birth_frame": 18,
    "death_frame": 20,
    "lifespan": 2,
    "children": [],
    "peak_mass": 12.130627516539207,
    "dominant_channel": 2
  },
  "88126a7c": {
    "parent": "9b27650e",
    "generation": 1,
    "birth_frame": 18,
    "death_frame": 28,
    "lifespan": 10,
    "children": [
      "17c3c3a9",
      "87261b7a",
      "b35b5040",
      "c20782ed",
      "c23c8eb8"
    ],
    "peak_mass": 619.5093505694279,
    "dominant_channel": 1
  },
  "8d982ad9": {
    "parent": "0ed9e0a4",
    "generation": 1,
    "birth_frame": 18,
    "death_frame": 20,
    "lifespan": 2,
    "children": [],
    "peak_mass": 22.016278384916653,
    "dominant_channel": 2
  },
  "83dacdac": {
    "parent": "0ed9e0a4",
    "generation": 1,
    "birth_frame": 18,
    "death_frame": 19,
    "lifespan": 1,
    "children": [],
    "peak_mass": 8.19090271694965,
    "dominant_channel": 2
  },
  "9a776fca": {
    "parent": null,
    "generation": 0,
    "birth_frame": 19,
    "death_frame": 20,
    "lifespan": 1,
    "children": [],
    "peak_mass": 9.418060695198365,
    "dominant_channel": 2
  },
  "17c3c3a9": {
    "parent": "88126a7c",
    "generation": 2,
    "birth_frame": 22,
    "death_frame": 23,
    "lifespan": 1,
    "children": [],
    "peak_mass": 12.511150019043342,
    "dominant_channel": 0
  },
  "87261b7a": {
    "parent": "88126a7c",
    "generation": 2,
    "birth_frame": 27,
    "death_frame": null,
    "lifespan": 124,
    "children": [
      "379239d2",
      "7d3eecea",
      "e5cd53dd",
      "3588999d"
    ],
    "peak_mass": 728.1978667892788,
    "dominant_channel": 1
  },
  "b35b5040": {
    "parent": "88126a7c",
    "generation": 2,
    "birth_frame": 27,
    "death_frame": 28,
    "lifespan": 1,
    "children": [],
    "peak_mass": 8.280890575684971,
    "dominant_channel": 2
  },
  "c20782ed": {
    "parent": "88126a7c",
    "generation": 2,
    "birth_frame": 27,
    "death_frame": 29,
    "lifespan": 2,
    "children": [],
    "peak_mass": 7.9703777780842,
    "dominant_channel": 0
  },
  "c23c8eb8": {
    "parent": "88126a7c",
    "generation": 2,
    "birth_frame": 27,
    "death_frame": 31,
    "lifespan": 4,
    "children": [],
    "peak_mass": 6.476827654335872,
    "dominant_channel": 0
  },
  "6bed36d4": {
    "parent": null,
    "generation": 0,
    "birth_frame": 31,
    "death_frame": 32,
    "lifespan": 1,
    "children": [],
    "peak_mass": 3.9238335542335507,
    "dominant_channel": 0
  },
  "379239d2": {
    "parent": "87261b7a",
    "generation": 3,
    "birth_frame": 34,
    "death_frame": 35,
    "lifespan": 1,
    "children": [],
    "peak_mass": 6.545085417486945,
    "dominant_channel": 0
  },
  "7d3eecea": {
    "parent": "87261b7a",
    "generation": 3,
    "birth_frame": 54,
    "death_frame": 55,
    "lifespan": 1,
    "children": [],
    "peak_mass": 8.65509761417955,
    "dominant_channel": 0
  },
  "e5cd53dd": {
    "parent": "87261b7a",
    "generation": 3,
    "birth_frame": 98,
    "death_frame": 103,
    "lifespan": 5,
    "children": [],
    "peak_mass": 5.641664755476375,
    "dominant_channel": 0
  },
  "3588999d": {
    "parent": "87261b7a",
    "generation": 3,
    "birth_frame": 126,
    "death_frame": 129,
    "lifespan": 3,
    "children": [],
    "peak_mass": 4.514457324467577,
    "dominant_channel": 0
  }
}
```

## Media

- `outputs/SPECIES_015_MEDUSA_final.png`
- `outputs/SPECIES_015_MEDUSA.gif`
- `outputs/SPECIES_015_MEDUSA.mp4`

- genome: `outputs/species/SPECIES_015_MEDUSA_genome.json`
