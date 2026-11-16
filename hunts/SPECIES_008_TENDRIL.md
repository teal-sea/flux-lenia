# SPECIES 008 — TENDRIL

**Verdict:** VIABLE + REPRODUCING
**Origin:** random  |  **Seed:** 544

## Viability gates

| gate | verdict | value | detail |
| --- | --- | --- | --- |
| mass_conservation | PASS | 2.53739e-16 | tol=0.0001 |
| non_triviality | PASS | 25.5507 | conc>=6.0, occupancy 0.183<=0.45, 1 bodies |
| persistence | PASS | 1 | 1 organisms alive at the end with lifespan >= 15 frames |
| activity | PASS | 1.31917 | mean speed of the most mobile organism, cells/frame |

## Behaviour (anomaly bouncer)

| behaviour | established | score | evidence |
| --- | --- | --- | --- |
| phototaxis | no | -0.002 | lamp(26, 64): 38.4->38.5; lamp(102, 64): 38.4->38.4; lamp(64, 26): 38.5->38.3 | min approach -0.002 (needs > 0.05 for every lamp position) |
| predatory_pursuit | no | 0.000 | no closing pair found |
| cyclic_locomotion | no | 0.191 | uid=a043ba00 circling=0.19 spectral_power=0.04 period=2.3 frames (counted only if >= 4) life=49 frames |

## Reproduction

Measured on the recording run below (the screening run is sampled more coarsely and its counts differ; both are stated separately rather than mixed).

- Divisions counted (offspring survived AND carried at least 10% of the parent's mass): **0**
- Raw fission events before the mass filter: **1** — the difference is debris a large body shed, which is not reproduction
- Surviving offspring total: **0**
- Organisms tracked in this run: **36**
- Screening run, for comparison: 1 divisions of 2 raw fissions, deepest generation 4

## Complexity

```json
{
  "morph_diversity": 0.41570367042612105,
  "spatial_mi": 1.4437659351635885,
  "cross_channel_mi": 1.1934093750716952,
  "euler_final": -49,
  "concentration_final": 25.55065016385469,
  "occupancy_final": 0.1827392578125,
  "n_blobs_final": 1,
  "activity": 1.3191713924175412,
  "mass_drift": 2.5373870793293687e-16,
  "score": 12.99200619715459
}
```

## Lineage tree

```json
{
  "d2c9b1e3": {
    "parent": null,
    "generation": 0,
    "birth_frame": 0,
    "death_frame": 17,
    "lifespan": 17,
    "children": [
      "3d490034",
      "8378bc11",
      "a043ba00"
    ],
    "peak_mass": 3560.02239654152,
    "dominant_channel": 0
  },
  "3d490034": {
    "parent": "d2c9b1e3",
    "generation": 1,
    "birth_frame": 15,
    "death_frame": 16,
    "lifespan": 1,
    "children": [],
    "peak_mass": 23.042595068192604,
    "dominant_channel": 1
  },
  "8378bc11": {
    "parent": "d2c9b1e3",
    "generation": 1,
    "birth_frame": 16,
    "death_frame": 17,
    "lifespan": 1,
    "children": [],
    "peak_mass": 57.150411910896125,
    "dominant_channel": 1
  },
  "a043ba00": {
    "parent": "d2c9b1e3",
    "generation": 1,
    "birth_frame": 16,
    "death_frame": 65,
    "lifespan": 49,
    "children": [
      "6831f6a7",
      "09ab8eb0",
      "4dc55f58",
      "e04c48d2",
      "5b8d662b",
      "3a5c1ed3",
      "2770ad55",
      "45a2e4cf",
      "2f89a860",
      "fb6bf186",
      "1cf525d6"
    ],
    "peak_mass": 3475.525603109772,
    "dominant_channel": 0
  },
  "6831f6a7": {
    "parent": "a043ba00",
    "generation": 2,
    "birth_frame": 27,
    "death_frame": 28,
    "lifespan": 1,
    "children": [],
    "peak_mass": 12.742655100439828,
    "dominant_channel": 1
  },
  "09ab8eb0": {
    "parent": "a043ba00",
    "generation": 2,
    "birth_frame": 30,
    "death_frame": 31,
    "lifespan": 1,
    "children": [],
    "peak_mass": 51.1013410394853,
    "dominant_channel": 1
  },
  "4dc55f58": {
    "parent": "a043ba00",
    "generation": 2,
    "birth_frame": 30,
    "death_frame": 31,
    "lifespan": 1,
    "children": [],
    "peak_mass": 9.934515982806916,
    "dominant_channel": 1
  },
  "e04c48d2": {
    "parent": "a043ba00",
    "generation": 2,
    "birth_frame": 31,
    "death_frame": 32,
    "lifespan": 1,
    "children": [],
    "peak_mass": 63.92044492954607,
    "dominant_channel": 1
  },
  "5b8d662b": {
    "parent": "a043ba00",
    "generation": 2,
    "birth_frame": 35,
    "death_frame": 36,
    "lifespan": 1,
    "children": [],
    "peak_mass": 8.819804612576995,
    "dominant_channel": 1
  },
  "3a5c1ed3": {
    "parent": "a043ba00",
    "generation": 2,
    "birth_frame": 38,
    "death_frame": 39,
    "lifespan": 1,
    "children": [],
    "peak_mass": 11.808839082181859,
    "dominant_channel": 1
  },
  "2770ad55": {
    "parent": "a043ba00",
    "generation": 2,
    "birth_frame": 41,
    "death_frame": 42,
    "lifespan": 1,
    "children": [],
    "peak_mass": 22.41407870143895,
    "dominant_channel": 1
  },
  "45a2e4cf": {
    "parent": "a043ba00",
    "generation": 2,
    "birth_frame": 43,
    "death_frame": 44,
    "lifespan": 1,
    "children": [],
    "peak_mass": 81.84388376483453,
    "dominant_channel": 1
  },
  "2f89a860": {
    "parent": "a043ba00",
    "generation": 2,
    "birth_frame": 43,
    "death_frame": 44,
    "lifespan": 1,
    "children": [],
    "peak_mass": 29.266852788869304,
    "dominant_channel": 1
  },
  "fb6bf186": {
    "parent": "a043ba00",
    "generation": 2,
    "birth_frame": 51,
    "death_frame": 52,
    "lifespan": 1,
    "children": [],
    "peak_mass": 15.028021555160946,
    "dominant_channel": 1
  },
  "1cf525d6": {
    "parent": "a043ba00",
    "generation": 2,
    "birth_frame": 59,
    "death_frame": 63,
    "lifespan": 4,
    "children": [
      "6ff0e86c",
      "5a8c004a",
      "a3820753",
      "e52def70",
      "345fc696"
    ],
    "peak_mass": 451.63480699228506,
    "dominant_channel": 1
  },
  "6ff0e86c": {
    "parent": "1cf525d6",
    "generation": 3,
    "birth_frame": 60,
    "death_frame": 64,
    "lifespan": 4,
    "children": [
      "68d4c962",
      "beb7155c"
    ],
    "peak_mass": 105.87521195098451,
    "dominant_channel": 1
  },
  "5a8c004a": {
    "parent": "1cf525d6",
    "generation": 3,
    "birth_frame": 60,
    "death_frame": 63,
    "lifespan": 3,
    "children": [
      "c54b71b8"
    ],
    "peak_mass": 84.16081672846697,
    "dominant_channel": 1
  },
  "a3820753": {
    "parent": "1cf525d6",
    "generation": 3,
    "birth_frame": 60,
    "death_frame": 64,
    "lifespan": 4,
    "children": [
      "5bb829f4"
    ],
    "peak_mass": 76.14207257137494,
    "dominant_channel": 1
  },
  "68d4c962": {
    "parent": "6ff0e86c",
    "generation": 4,
    "birth_frame": 61,
    "death_frame": 65,
    "lifespan": 4,
    "children": [],
    "peak_mass": 46.27886372192674,
    "dominant_channel": 1
  },
  "beb7155c": {
    "parent": "6ff0e86c",
    "generation": 4,
    "birth_frame": 61,
    "death_frame": 64,
    "lifespan": 3,
    "children": [],
    "peak_mass": 19.10009221224076,
    "dominant_channel": 1
  },
  "5bb829f4": {
    "parent": "a3820753",
    "generation": 4,
    "birth_frame": 62,
    "death_frame": 64,
    "lifespan": 2,
    "children": [],
    "peak_mass": 61.01407440123697,
    "dominant_channel": 1
  },
  "e52def70": {
    "parent": "1cf525d6",
    "generation": 3,
    "birth_frame": 62,
    "death_frame": 63,
    "lifespan": 1,
    "children": [],
    "peak_mass": 39.163037689310514,
    "dominant_channel": 1
  },
  "345fc696": {
    "parent": "1cf525d6",
    "generation": 3,
    "birth_frame": 62,
    "death_frame": 64,
    "lifespan": 2,
    "children": [],
    "peak_mass": 107.40797979259898,
    "dominant_channel": 1
  },
  "e8fcd9b8": {
    "parent": null,
    "generation": 0,
    "birth_frame": 62,
    "death_frame": null,
    "lifespan": 89,
    "children": [
      "65b23735",
      "65783397",
      "a12c1175",
      "edc71955",
      "ae5a8172",
      "4183b583",
      "fbb9d964",
      "f439df34",
      "61f9b617",
      "f9316008",
      "8647342a"
    ],
    "peak_mass": 3408.2125862333987,
    "dominant_channel": 0
  },
  "c54b71b8": {
    "parent": "5a8c004a",
    "generation": 4,
    "birth_frame": 63,
    "death_frame": 64,
    "lifespan": 1,
    "children": [],
    "peak_mass": 17.61900084055243,
    "dominant_channel": 1
  },
  "65b23735": {
    "parent": "e8fcd9b8",
    "generation": 1,
    "birth_frame": 99,
    "death_frame": 100,
    "lifespan": 1,
    "children": [],
    "peak_mass": 10.88776597719418,
    "dominant_channel": 1
  },
  "65783397": {
    "parent": "e8fcd9b8",
    "generation": 1,
    "birth_frame": 105,
    "death_frame": 106,
    "lifespan": 1,
    "children": [],
    "peak_mass": 11.43264776331677,
    "dominant_channel": 1
  },
  "a12c1175": {
    "parent": "e8fcd9b8",
    "generation": 1,
    "birth_frame": 108,
    "death_frame": 109,
    "lifespan": 1,
    "children": [],
    "peak_mass": 11.520425588769934,
    "dominant_channel": 1
  },
  "edc71955": {
    "parent": "e8fcd9b8",
    "generation": 1,
    "birth_frame": 108,
    "death_frame": 109,
    "lifespan": 1,
    "children": [],
    "peak_mass": 11.419265584704712,
    "dominant_channel": 1
  },
  "ae5a8172": {
    "parent": "e8fcd9b8",
    "generation": 1,
    "birth_frame": 140,
    "death_frame": 141,
    "lifespan": 1,
    "children": [],
    "peak_mass": 12.28337567044674,
    "dominant_channel": 1
  },
  "4183b583": {
    "parent": "e8fcd9b8",
    "generation": 1,
    "birth_frame": 142,
    "death_frame": 143,
    "lifespan": 1,
    "children": [],
    "peak_mass": 12.443761436359797,
    "dominant_channel": 1
  },
  "fbb9d964": {
    "parent": "e8fcd9b8",
    "generation": 1,
    "birth_frame": 147,
    "death_frame": 148,
    "lifespan": 1,
    "children": [],
    "peak_mass": 28.728763175852364,
    "dominant_channel": 1
  },
  "f439df34": {
    "parent": "e8fcd9b8",
    "generation": 1,
    "birth_frame": 147,
    "death_frame": 148,
    "lifespan": 1,
    "children": [],
    "peak_mass": 18.666992874206194,
    "dominant_channel": 1
  },
  "61f9b617": {
    "parent": "e8fcd9b8",
    "generation": 1,
    "birth_frame": 147,
    "death_frame": 148,
    "lifespan": 1,
    "children": [],
    "peak_mass": 13.711226163406648,
    "dominant_channel": 1
  },
  "f9316008": {
    "parent": "e8fcd9b8",
    "generation": 1,
    "birth_frame": 147,
    "death_frame": 149,
    "lifespan": 2,
    "children": [],
    "peak_mass": 13.202101570450294,
    "dominant_channel": 0
  },
  "8647342a": {
    "parent": "e8fcd9b8",
    "generation": 1,
    "birth_frame": 147,
    "death_frame": 149,
    "lifespan": 2,
    "children": [],
    "peak_mass": 12.413368527279093,
    "dominant_channel": 1
  }
}
```

## Media

- `outputs/SPECIES_008_TENDRIL_final.png`
- `outputs/SPECIES_008_TENDRIL.gif`
- `outputs/SPECIES_008_TENDRIL.mp4`

- genome: `outputs/species/SPECIES_008_TENDRIL_genome.json`
