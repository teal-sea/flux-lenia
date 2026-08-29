# SPECIES 003 — VAGRANT

**Verdict:** VIABLE + REPRODUCING
**Origin:** random  |  **Seed:** 458

## Viability gates

| gate | verdict | value | detail |
| --- | --- | --- | --- |
| mass_conservation | PASS | 3.15819e-16 | tol=0.0001 |
| non_triviality | PASS | 33.6271 | conc>=6.0, occupancy 0.110<=0.45, 10 bodies |
| persistence | PASS | 1 | 1 organisms alive at the end with lifespan >= 15 frames |
| activity | PASS | 9.48492 | mean speed of the most mobile organism, cells/frame |

## Behaviour (anomaly bouncer)

| behaviour | established | score | evidence |
| --- | --- | --- | --- |
| phototaxis | no | -0.013 | lamp(26, 64): 38.5->38.6; lamp(102, 64): 38.3->38.8; lamp(64, 26): 38.4->38.7 | min approach -0.013 (needs > 0.05 for every lamp position) |
| predatory_pursuit | no | 0.197 | 3c117e13(ch1) -> 274bf5ec(ch1) closed 42.2 -> 26.9 cells over 12 frames, monotone 0.55, target speed 2.908 |
| cyclic_locomotion | no | 0.499 | uid=e4eea9b9 circling=0.04 spectral_power=0.17 period=6.0 frames (counted only if >= 4) life=25 frames |

## Reproduction

Measured on the recording run below (the screening run is sampled more coarsely and its counts differ; both are stated separately rather than mixed).

- Divisions counted (offspring survived AND carried at least 10% of the parent's mass): **5**
- Raw fission events before the mass filter: **9** — the difference is debris a large body shed, which is not reproduction
- Surviving offspring total: **5**
- Organisms tracked in this run: **134**
- Screening run, for comparison: 3 divisions of 6 raw fissions, deepest generation 6

| frame | parent | children | parent mass | child masses | child share |
| --- | --- | --- | --- | --- | --- |
| 48 | `97ec9c5a` | `3c117e13` | 2.5 | 2.2 | 88% |
| 56 | `befa0635` | `7d5d4480` | 5.2 | 2.5 | 48% |
| 63 | `274bf5ec` | `24310859` | 3.9 | 2.7 | 71% |
| 117 | `cafd0c43` | `ea75d2a8` | 6.4 | 2.4 | 38% |
| 119 | `cafd0c43` | `e4eea9b9` | 3.6 | 2.6 | 73% |

## Complexity

```json
{
  "morph_diversity": 2.057681364240886,
  "spatial_mi": 1.5570788769910864,
  "cross_channel_mi": 0.5226206437228443,
  "euler_final": 8,
  "concentration_final": 33.627136656417875,
  "occupancy_final": 0.11016845703125,
  "n_blobs_final": 10,
  "activity": 9.484923065153584,
  "mass_drift": 3.158186707845354e-16,
  "score": 31.65153711758065
}
```

## Lineage tree

```json
{
  "4582f6ff": {
    "parent": null,
    "generation": 0,
    "birth_frame": 0,
    "death_frame": 32,
    "lifespan": 32,
    "children": [
      "163ddfde",
      "47d62c42",
      "a4df0367",
      "61831236",
      "b21c4cb7",
      "3692661d"
    ],
    "peak_mass": 714.4348999671452,
    "dominant_channel": 2
  },
  "163ddfde": {
    "parent": "4582f6ff",
    "generation": 1,
    "birth_frame": 26,
    "death_frame": 38,
    "lifespan": 12,
    "children": [
      "ed56acb1",
      "017726b1",
      "995c2ec3"
    ],
    "peak_mass": 16.03386084283691,
    "dominant_channel": 1
  },
  "47d62c42": {
    "parent": "4582f6ff",
    "generation": 1,
    "birth_frame": 26,
    "death_frame": 27,
    "lifespan": 1,
    "children": [
      "38e10013"
    ],
    "peak_mass": 3.8240941816820344,
    "dominant_channel": 1
  },
  "e84b8988": {
    "parent": null,
    "generation": 0,
    "birth_frame": 26,
    "death_frame": 31,
    "lifespan": 5,
    "children": [
      "6f68ce00"
    ],
    "peak_mass": 7.0902667837500095,
    "dominant_channel": 1
  },
  "a4df0367": {
    "parent": "4582f6ff",
    "generation": 1,
    "birth_frame": 27,
    "death_frame": 31,
    "lifespan": 4,
    "children": [],
    "peak_mass": 7.090742180937726,
    "dominant_channel": 1
  },
  "61831236": {
    "parent": "4582f6ff",
    "generation": 1,
    "birth_frame": 27,
    "death_frame": 28,
    "lifespan": 1,
    "children": [],
    "peak_mass": 3.395494854359238,
    "dominant_channel": 1
  },
  "38e10013": {
    "parent": "47d62c42",
    "generation": 2,
    "birth_frame": 27,
    "death_frame": 29,
    "lifespan": 2,
    "children": [],
    "peak_mass": 3.5374337266155864,
    "dominant_channel": 1
  },
  "b21c4cb7": {
    "parent": "4582f6ff",
    "generation": 1,
    "birth_frame": 28,
    "death_frame": 31,
    "lifespan": 3,
    "children": [
      "45137244"
    ],
    "peak_mass": 5.491967606113972,
    "dominant_channel": 1
  },
  "8eba54f0": {
    "parent": null,
    "generation": 0,
    "birth_frame": 29,
    "death_frame": 30,
    "lifespan": 1,
    "children": [],
    "peak_mass": 3.0886364680251734,
    "dominant_channel": 1
  },
  "6f68ce00": {
    "parent": "e84b8988",
    "generation": 1,
    "birth_frame": 30,
    "death_frame": 35,
    "lifespan": 5,
    "children": [
      "4bfb00cb",
      "ba7fc8e2",
      "f938dba2"
    ],
    "peak_mass": 638.8441813280629,
    "dominant_channel": 2
  },
  "435daf0a": {
    "parent": null,
    "generation": 0,
    "birth_frame": 30,
    "death_frame": 31,
    "lifespan": 1,
    "children": [],
    "peak_mass": 2.914492361783882,
    "dominant_channel": 1
  },
  "45137244": {
    "parent": "b21c4cb7",
    "generation": 2,
    "birth_frame": 31,
    "death_frame": 32,
    "lifespan": 1,
    "children": [],
    "peak_mass": 3.1115332869942938,
    "dominant_channel": 1
  },
  "50a3fd2e": {
    "parent": null,
    "generation": 0,
    "birth_frame": 31,
    "death_frame": 32,
    "lifespan": 1,
    "children": [],
    "peak_mass": 6.454545424287893,
    "dominant_channel": 1
  },
  "4bfb00cb": {
    "parent": "6f68ce00",
    "generation": 2,
    "birth_frame": 32,
    "death_frame": 34,
    "lifespan": 2,
    "children": [],
    "peak_mass": 6.780657361501119,
    "dominant_channel": 1
  },
  "3692661d": {
    "parent": "4582f6ff",
    "generation": 1,
    "birth_frame": 32,
    "death_frame": 35,
    "lifespan": 3,
    "children": [],
    "peak_mass": 8.026087460615928,
    "dominant_channel": 1
  },
  "ed56acb1": {
    "parent": "163ddfde",
    "generation": 2,
    "birth_frame": 33,
    "death_frame": 34,
    "lifespan": 1,
    "children": [],
    "peak_mass": 3.3974778490531565,
    "dominant_channel": 1
  },
  "017726b1": {
    "parent": "163ddfde",
    "generation": 2,
    "birth_frame": 33,
    "death_frame": 36,
    "lifespan": 3,
    "children": [
      "063ee550",
      "e06442d1"
    ],
    "peak_mass": 632.8618357703087,
    "dominant_channel": 2
  },
  "ba7fc8e2": {
    "parent": "6f68ce00",
    "generation": 2,
    "birth_frame": 33,
    "death_frame": 35,
    "lifespan": 2,
    "children": [],
    "peak_mass": 3.66163306650022,
    "dominant_channel": 1
  },
  "f938dba2": {
    "parent": "6f68ce00",
    "generation": 2,
    "birth_frame": 33,
    "death_frame": 37,
    "lifespan": 4,
    "children": [],
    "peak_mass": 9.966074048251176,
    "dominant_channel": 1
  },
  "995c2ec3": {
    "parent": "163ddfde",
    "generation": 2,
    "birth_frame": 34,
    "death_frame": 36,
    "lifespan": 2,
    "children": [],
    "peak_mass": 3.473953832090893,
    "dominant_channel": 1
  },
  "063ee550": {
    "parent": "017726b1",
    "generation": 3,
    "birth_frame": 35,
    "death_frame": 39,
    "lifespan": 4,
    "children": [
      "872cc1e6",
      "0f6489c3",
      "93aea649"
    ],
    "peak_mass": 643.4541841399591,
    "dominant_channel": 2
  },
  "cabda0b2": {
    "parent": null,
    "generation": 0,
    "birth_frame": 35,
    "death_frame": 36,
    "lifespan": 1,
    "children": [],
    "peak_mass": 2.259126531642828,
    "dominant_channel": 1
  },
  "59a7adec": {
    "parent": null,
    "generation": 0,
    "birth_frame": 35,
    "death_frame": 37,
    "lifespan": 2,
    "children": [
      "0dd02101",
      "ce5ae1db"
    ],
    "peak_mass": 5.491720968094209,
    "dominant_channel": 1
  },
  "e06442d1": {
    "parent": "017726b1",
    "generation": 3,
    "birth_frame": 36,
    "death_frame": 37,
    "lifespan": 1,
    "children": [],
    "peak_mass": 3.1102973876650397,
    "dominant_channel": 1
  },
  "0dd02101": {
    "parent": "59a7adec",
    "generation": 1,
    "birth_frame": 36,
    "death_frame": 39,
    "lifespan": 3,
    "children": [
      "bd397794"
    ],
    "peak_mass": 6.398362100334737,
    "dominant_channel": 1
  },
  "872cc1e6": {
    "parent": "063ee550",
    "generation": 4,
    "birth_frame": 37,
    "death_frame": 43,
    "lifespan": 6,
    "children": [
      "8bb30899",
      "3558add2",
      "bb66fcc3",
      "751d8615"
    ],
    "peak_mass": 646.1749009526595,
    "dominant_channel": 2
  },
  "0f6489c3": {
    "parent": "063ee550",
    "generation": 4,
    "birth_frame": 37,
    "death_frame": 44,
    "lifespan": 7,
    "children": [
      "c1f8cdcc",
      "ab244574",
      "030f78fb"
    ],
    "peak_mass": 665.5187470499993,
    "dominant_channel": 2
  },
  "ce5ae1db": {
    "parent": "59a7adec",
    "generation": 1,
    "birth_frame": 37,
    "death_frame": 38,
    "lifespan": 1,
    "children": [
      "0668b144"
    ],
    "peak_mass": 3.850794081750868,
    "dominant_channel": 1
  },
  "c9844274": {
    "parent": null,
    "generation": 0,
    "birth_frame": 37,
    "death_frame": 42,
    "lifespan": 5,
    "children": [
      "850d18d7",
      "3b864d6f"
    ],
    "peak_mass": 3.5453411748144767,
    "dominant_channel": 1
  },
  "8bb30899": {
    "parent": "872cc1e6",
    "generation": 5,
    "birth_frame": 38,
    "death_frame": 39,
    "lifespan": 1,
    "children": [],
    "peak_mass": 2.7144368309273768,
    "dominant_channel": 1
  },
  "93aea649": {
    "parent": "063ee550",
    "generation": 4,
    "birth_frame": 38,
    "death_frame": 40,
    "lifespan": 2,
    "children": [],
    "peak_mass": 3.8962954558086236,
    "dominant_channel": 1
  },
  "0668b144": {
    "parent": "ce5ae1db",
    "generation": 2,
    "birth_frame": 38,
    "death_frame": 43,
    "lifespan": 5,
    "children": [],
    "peak_mass": 3.4898233040398847,
    "dominant_channel": 1
  },
  "850d18d7": {
    "parent": "c9844274",
    "generation": 1,
    "birth_frame": 39,
    "death_frame": 40,
    "lifespan": 1,
    "children": [],
    "peak_mass": 2.2694909745047402,
    "dominant_channel": 1
  },
  "bd397794": {
    "parent": "0dd02101",
    "generation": 2,
    "birth_frame": 39,
    "death_frame": 42,
    "lifespan": 3,
    "children": [],
    "peak_mass": 2.4706337817578974,
    "dominant_channel": 1
  },
  "3558add2": {
    "parent": "872cc1e6",
    "generation": 5,
    "birth_frame": 40,
    "death_frame": 43,
    "lifespan": 3,
    "children": [
      "4e7b6f6b"
    ],
    "peak_mass": 5.11726218453415,
    "dominant_channel": 1
  },
  "bb66fcc3": {
    "parent": "872cc1e6",
    "generation": 5,
    "birth_frame": 40,
    "death_frame": 43,
    "lifespan": 3,
    "children": [],
    "peak_mass": 5.104546008743372,
    "dominant_channel": 1
  },
  "3b864d6f": {
    "parent": "c9844274",
    "generation": 1,
    "birth_frame": 41,
    "death_frame": 43,
    "lifespan": 2,
    "children": [],
    "peak_mass": 2.4612491132959264,
    "dominant_channel": 1
  },
  "a81ef90a": {
    "parent": null,
    "generation": 0,
    "birth_frame": 41,
    "death_frame": 43,
    "lifespan": 2,
    "children": [],
    "peak_mass": 2.338443235773167,
    "dominant_channel": 1
  },
  "94a33132": {
    "parent": null,
    "generation": 0,
    "birth_frame": 41,
    "death_frame": 43,
    "lifespan": 2,
    "children": [],
    "peak_mass": 2.2962632195037926,
    "dominant_channel": 1
  },
  "751d8615": {
    "parent": "872cc1e6",
    "generation": 5,
    "birth_frame": 42,
    "death_frame": 43,
    "lifespan": 1,
    "children": [],
    "peak_mass": 4.515408200675758,
    "dominant_channel": 1
  }
}
```

## Media

- `outputs/SPECIES_003_VAGRANT_final.png`
- `outputs/SPECIES_003_VAGRANT.gif`
- `outputs/SPECIES_003_VAGRANT.mp4`

- genome: `outputs/species/SPECIES_003_VAGRANT_genome.json`
