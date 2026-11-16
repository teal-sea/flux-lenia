# SPECIES 009 — ARBORIS

**Verdict:** VIABLE + REPRODUCING
**Origin:** random  |  **Seed:** 592

## Viability gates

| gate | verdict | value | detail |
| --- | --- | --- | --- |
| mass_conservation | PASS | 4.13789e-16 | tol=0.0001 |
| non_triviality | PASS | 7.58157 | conc>=6.0, occupancy 0.399<=0.45, 2 bodies |
| persistence | PASS | 1 | 1 organisms alive at the end with lifespan >= 15 frames |
| activity | PASS | 2.32034 | mean speed of the most mobile organism, cells/frame |

## Behaviour (anomaly bouncer)

| behaviour | established | score | evidence |
| --- | --- | --- | --- |
| phototaxis | no | -0.031 | lamp(26, 64): 38.4->39.6; lamp(102, 64): 38.4->39.2; lamp(64, 26): 38.3->38.5 | min approach -0.031 (needs > 0.05 for every lamp position) |
| predatory_pursuit | no | 0.000 | no closing pair found |
| cyclic_locomotion | no | 0.118 | uid=d56e2c30 circling=0.12 spectral_power=0.06 period=2.1 frames (counted only if >= 4) life=36 frames |

## Reproduction

Measured on the recording run below (the screening run is sampled more coarsely and its counts differ; both are stated separately rather than mixed).

- Divisions counted (offspring survived AND carried at least 10% of the parent's mass): **0**
- Raw fission events before the mass filter: **4** — the difference is debris a large body shed, which is not reproduction
- Surviving offspring total: **0**
- Organisms tracked in this run: **76**
- Screening run, for comparison: 1 divisions of 4 raw fissions, deepest generation 4

## Complexity

```json
{
  "morph_diversity": 2.3884223383410133,
  "spatial_mi": 1.4276535350841428,
  "cross_channel_mi": 0.8655105275111944,
  "euler_final": 50,
  "concentration_final": 7.581568712728391,
  "occupancy_final": 0.39892578125,
  "n_blobs_final": 2,
  "activity": 2.320344606398047,
  "mass_drift": 4.137891641430899e-16,
  "score": 14.913292711504214
}
```

## Lineage tree

```json
{
  "1aa6518f": {
    "parent": null,
    "generation": 0,
    "birth_frame": 0,
    "death_frame": 7,
    "lifespan": 7,
    "children": [
      "a4d3fda7",
      "494eb564",
      "9a41722c",
      "4a40211e",
      "11cf295d",
      "c8f2fba1",
      "f5e9b59f",
      "938c82cc",
      "50bc7e79",
      "677efbbb",
      "dd151bf1"
    ],
    "peak_mass": 4341.702555900252,
    "dominant_channel": 1
  },
  "a4d3fda7": {
    "parent": "1aa6518f",
    "generation": 1,
    "birth_frame": 4,
    "death_frame": 6,
    "lifespan": 2,
    "children": [],
    "peak_mass": 47.72257623172662,
    "dominant_channel": 0
  },
  "494eb564": {
    "parent": "1aa6518f",
    "generation": 1,
    "birth_frame": 5,
    "death_frame": 6,
    "lifespan": 1,
    "children": [
      "f9f44872"
    ],
    "peak_mass": 187.261938310301,
    "dominant_channel": 0
  },
  "9a41722c": {
    "parent": "1aa6518f",
    "generation": 1,
    "birth_frame": 5,
    "death_frame": 6,
    "lifespan": 1,
    "children": [],
    "peak_mass": 39.01038244911483,
    "dominant_channel": 0
  },
  "4a40211e": {
    "parent": "1aa6518f",
    "generation": 1,
    "birth_frame": 6,
    "death_frame": 7,
    "lifespan": 1,
    "children": [],
    "peak_mass": 274.51870488222005,
    "dominant_channel": 0
  },
  "11cf295d": {
    "parent": "1aa6518f",
    "generation": 1,
    "birth_frame": 6,
    "death_frame": 7,
    "lifespan": 1,
    "children": [],
    "peak_mass": 203.06301885392415,
    "dominant_channel": 0
  },
  "c8f2fba1": {
    "parent": "1aa6518f",
    "generation": 1,
    "birth_frame": 6,
    "death_frame": 10,
    "lifespan": 4,
    "children": [
      "f6ef60b0",
      "c19ca294",
      "00e5b51d",
      "d56e2c30"
    ],
    "peak_mass": 3091.370901996711,
    "dominant_channel": 0
  },
  "f5e9b59f": {
    "parent": "1aa6518f",
    "generation": 1,
    "birth_frame": 6,
    "death_frame": 7,
    "lifespan": 1,
    "children": [],
    "peak_mass": 42.55162185928755,
    "dominant_channel": 0
  },
  "938c82cc": {
    "parent": "1aa6518f",
    "generation": 1,
    "birth_frame": 6,
    "death_frame": 7,
    "lifespan": 1,
    "children": [],
    "peak_mass": 41.436649072462444,
    "dominant_channel": 0
  },
  "50bc7e79": {
    "parent": "1aa6518f",
    "generation": 1,
    "birth_frame": 6,
    "death_frame": 7,
    "lifespan": 1,
    "children": [],
    "peak_mass": 39.663605825999106,
    "dominant_channel": 0
  },
  "677efbbb": {
    "parent": "1aa6518f",
    "generation": 1,
    "birth_frame": 6,
    "death_frame": 7,
    "lifespan": 1,
    "children": [],
    "peak_mass": 37.89192506085221,
    "dominant_channel": 0
  },
  "dd151bf1": {
    "parent": "1aa6518f",
    "generation": 1,
    "birth_frame": 6,
    "death_frame": 7,
    "lifespan": 1,
    "children": [],
    "peak_mass": 36.925393520267974,
    "dominant_channel": 0
  },
  "f9f44872": {
    "parent": "494eb564",
    "generation": 2,
    "birth_frame": 6,
    "death_frame": 7,
    "lifespan": 1,
    "children": [],
    "peak_mass": 26.144162771230313,
    "dominant_channel": 0
  },
  "e0c3ab2c": {
    "parent": null,
    "generation": 0,
    "birth_frame": 7,
    "death_frame": 8,
    "lifespan": 1,
    "children": [],
    "peak_mass": 32.175597250644294,
    "dominant_channel": 0
  },
  "f6ef60b0": {
    "parent": "c8f2fba1",
    "generation": 2,
    "birth_frame": 8,
    "death_frame": 9,
    "lifespan": 1,
    "children": [],
    "peak_mass": 47.21281948561906,
    "dominant_channel": 0
  },
  "c19ca294": {
    "parent": "c8f2fba1",
    "generation": 2,
    "birth_frame": 8,
    "death_frame": 9,
    "lifespan": 1,
    "children": [],
    "peak_mass": 30.843338552317217,
    "dominant_channel": 0
  },
  "00e5b51d": {
    "parent": "c8f2fba1",
    "generation": 2,
    "birth_frame": 9,
    "death_frame": 10,
    "lifespan": 1,
    "children": [],
    "peak_mass": 85.22124062140105,
    "dominant_channel": 1
  },
  "d56e2c30": {
    "parent": "c8f2fba1",
    "generation": 2,
    "birth_frame": 9,
    "death_frame": 45,
    "lifespan": 36,
    "children": [
      "207d4fab",
      "62682353",
      "53a108de",
      "fcc99ca5",
      "44703ab4",
      "a2820fb6"
    ],
    "peak_mass": 4214.964501844293,
    "dominant_channel": 0
  },
  "207d4fab": {
    "parent": "d56e2c30",
    "generation": 3,
    "birth_frame": 12,
    "death_frame": 13,
    "lifespan": 1,
    "children": [],
    "peak_mass": 22.579056070613376,
    "dominant_channel": 1
  },
  "7f97c115": {
    "parent": null,
    "generation": 0,
    "birth_frame": 35,
    "death_frame": 36,
    "lifespan": 1,
    "children": [],
    "peak_mass": 4.435069634664107,
    "dominant_channel": 1
  },
  "62682353": {
    "parent": "d56e2c30",
    "generation": 3,
    "birth_frame": 38,
    "death_frame": 42,
    "lifespan": 4,
    "children": [],
    "peak_mass": 9.223239901431274,
    "dominant_channel": 1
  },
  "53a108de": {
    "parent": "d56e2c30",
    "generation": 3,
    "birth_frame": 43,
    "death_frame": 79,
    "lifespan": 36,
    "children": [
      "7658af79",
      "8d841043",
      "8f0817de",
      "85ccc027"
    ],
    "peak_mass": 4246.433271975765,
    "dominant_channel": 0
  },
  "fcc99ca5": {
    "parent": "d56e2c30",
    "generation": 3,
    "birth_frame": 43,
    "death_frame": 44,
    "lifespan": 1,
    "children": [],
    "peak_mass": 4.661259880322792,
    "dominant_channel": 1
  },
  "44703ab4": {
    "parent": "d56e2c30",
    "generation": 3,
    "birth_frame": 43,
    "death_frame": 44,
    "lifespan": 1,
    "children": [],
    "peak_mass": 3.4340480801986977,
    "dominant_channel": 0
  },
  "a2820fb6": {
    "parent": "d56e2c30",
    "generation": 3,
    "birth_frame": 44,
    "death_frame": 46,
    "lifespan": 2,
    "children": [
      "12a03541"
    ],
    "peak_mass": 4116.363143210869,
    "dominant_channel": 0
  },
  "12a03541": {
    "parent": "a2820fb6",
    "generation": 4,
    "birth_frame": 46,
    "death_frame": 47,
    "lifespan": 1,
    "children": [],
    "peak_mass": 3.342046385981044,
    "dominant_channel": 1
  },
  "b564cb4b": {
    "parent": null,
    "generation": 0,
    "birth_frame": 46,
    "death_frame": 47,
    "lifespan": 1,
    "children": [],
    "peak_mass": 5.788454247529658,
    "dominant_channel": 0
  },
  "7658af79": {
    "parent": "53a108de",
    "generation": 4,
    "birth_frame": 52,
    "death_frame": 53,
    "lifespan": 1,
    "children": [],
    "peak_mass": 3.2246355445491126,
    "dominant_channel": 1
  },
  "2c91dad0": {
    "parent": null,
    "generation": 0,
    "birth_frame": 66,
    "death_frame": 67,
    "lifespan": 1,
    "children": [],
    "peak_mass": 3.0737049955014824,
    "dominant_channel": 1
  },
  "8d841043": {
    "parent": "53a108de",
    "generation": 4,
    "birth_frame": 73,
    "death_frame": 75,
    "lifespan": 2,
    "children": [],
    "peak_mass": 4.003586106060656,
    "dominant_channel": 1
  },
  "8f0817de": {
    "parent": "53a108de",
    "generation": 4,
    "birth_frame": 76,
    "death_frame": 79,
    "lifespan": 3,
    "children": [],
    "peak_mass": 4.236414373650451,
    "dominant_channel": 1
  },
  "85ccc027": {
    "parent": "53a108de",
    "generation": 4,
    "birth_frame": 78,
    "death_frame": null,
    "lifespan": 73,
    "children": [
      "61fd6e22",
      "bed8e49b",
      "82ce0c53",
      "0d7f5a44",
      "64699799",
      "5fd81972",
      "10d2bfd3",
      "cc7d399c",
      "aafd740a",
      "a7a5cb75",
      "1248976b",
      "ba4ac163",
      "6ed3abdd",
      "f77ffca2",
      "ac3b69fd",
      "56a32361",
      "e568024a",
      "de3f016e",
      "c4d52eae",
      "c3eea0da",
      "5accc700",
      "72de129e",
      "095ea880",
      "665c4784"
    ],
    "peak_mass": 4165.936926257553,
    "dominant_channel": 0
  },
  "61fd6e22": {
    "parent": "85ccc027",
    "generation": 5,
    "birth_frame": 80,
    "death_frame": 81,
    "lifespan": 1,
    "children": [],
    "peak_mass": 4.265167215729607,
    "dominant_channel": 1
  },
  "bed8e49b": {
    "parent": "85ccc027",
    "generation": 5,
    "birth_frame": 81,
    "death_frame": 85,
    "lifespan": 4,
    "children": [],
    "peak_mass": 23.522211791311307,
    "dominant_channel": 1
  },
  "82ce0c53": {
    "parent": "85ccc027",
    "generation": 5,
    "birth_frame": 81,
    "death_frame": 82,
    "lifespan": 1,
    "children": [],
    "peak_mass": 3.9976646670842486,
    "dominant_channel": 1
  },
  "0d7f5a44": {
    "parent": "85ccc027",
    "generation": 5,
    "birth_frame": 82,
    "death_frame": 83,
    "lifespan": 1,
    "children": [],
    "peak_mass": 4.490641892190334,
    "dominant_channel": 1
  },
  "e0e2a82b": {
    "parent": null,
    "generation": 0,
    "birth_frame": 83,
    "death_frame": 92,
    "lifespan": 9,
    "children": [
      "60c76c5b"
    ],
    "peak_mass": 8.109093195049963,
    "dominant_channel": 1
  },
  "3df4537e": {
    "parent": null,
    "generation": 0,
    "birth_frame": 86,
    "death_frame": 87,
    "lifespan": 1,
    "children": [],
    "peak_mass": 2.4257402610983174,
    "dominant_channel": 1
  },
  "60c76c5b": {
    "parent": "e0e2a82b",
    "generation": 1,
    "birth_frame": 87,
    "death_frame": 89,
    "lifespan": 2,
    "children": [],
    "peak_mass": 4.163831850186994,
    "dominant_channel": 1
  },
  "64699799": {
    "parent": "85ccc027",
    "generation": 5,
    "birth_frame": 94,
    "death_frame": 96,
    "lifespan": 2,
    "children": [],
    "peak_mass": 3.404674313320967,
    "dominant_channel": 1
  }
}
```

## Media

- `outputs/SPECIES_009_ARBORIS_final.png`
- `outputs/SPECIES_009_ARBORIS.gif`
- `outputs/SPECIES_009_ARBORIS.mp4`

- genome: `outputs/species/SPECIES_009_ARBORIS_genome.json`
