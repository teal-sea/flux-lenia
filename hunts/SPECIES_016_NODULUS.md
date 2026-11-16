# SPECIES 016 — NODULUS

**Verdict:** VIABLE + REPRODUCING
**Origin:** random  |  **Seed:** 729

## Viability gates

| gate | verdict | value | detail |
| --- | --- | --- | --- |
| mass_conservation | PASS | 1.28092e-16 | tol=0.0001 |
| non_triviality | PASS | 7.05282 | conc>=6.0, occupancy 0.450<=0.45, 1 bodies |
| persistence | PASS | 1 | 1 organisms alive at the end with lifespan >= 15 frames |
| activity | PASS | 4.16546 | mean speed of the most mobile organism, cells/frame |

## Behaviour (anomaly bouncer)

| behaviour | established | score | evidence |
| --- | --- | --- | --- |
| phototaxis | no | -0.013 | lamp(26, 64): 38.3->38.7; lamp(102, 64): 38.5->38.8; lamp(64, 26): 38.4->39.0 | min approach -0.013 (needs > 0.05 for every lamp position) |
| predatory_pursuit | no | 0.000 | no closing pair found |
| cyclic_locomotion | no | 0.066 | uid=ddd2722d circling=0.07 spectral_power=0.02 period=2.1 frames (counted only if >= 4) life=139 frames |

## Reproduction

Measured on the recording run below (the screening run is sampled more coarsely and its counts differ; both are stated separately rather than mixed).

- Divisions counted (offspring survived AND carried at least 10% of the parent's mass): **2**
- Raw fission events before the mass filter: **2** — the difference is debris a large body shed, which is not reproduction
- Surviving offspring total: **2**
- Organisms tracked in this run: **37**
- Screening run, for comparison: 1 divisions of 1 raw fissions, deepest generation 2

| frame | parent | children | parent mass | child masses | child share |
| --- | --- | --- | --- | --- | --- |
| 4 | `fd6f4435` | `9575a417` | 499.3 | 105.0, 66.3, 54.6, 41.5 | 21% |
| 12 | `9a49dc28` | `ddd2722d` | 61.5 | 48.8, 33.5, 17.5 | 79% |

## Complexity

```json
{
  "morph_diversity": 0.0,
  "spatial_mi": 1.3531281943300149,
  "cross_channel_mi": 0.8784130093349143,
  "euler_final": -3,
  "concentration_final": 7.05282192446793,
  "occupancy_final": 0.449951171875,
  "n_blobs_final": 1,
  "activity": 4.165455380866259,
  "mass_drift": 1.2809221765111634e-16,
  "score": 12.80634391576513
}
```

## Lineage tree

```json
{
  "fd6f4435": {
    "parent": null,
    "generation": 0,
    "birth_frame": 0,
    "death_frame": 5,
    "lifespan": 5,
    "children": [
      "9575a417",
      "8eb3233b",
      "81499f5a",
      "62d06d01"
    ],
    "peak_mass": 3515.5978956098625,
    "dominant_channel": 2
  },
  "9575a417": {
    "parent": "fd6f4435",
    "generation": 1,
    "birth_frame": 4,
    "death_frame": 14,
    "lifespan": 10,
    "children": [
      "085c5d95",
      "029f5b93",
      "d6830ce2",
      "4f95c4a7",
      "9a49dc28",
      "a5619565",
      "b3abdb30",
      "9d3fddad",
      "33a32b10",
      "4b5c3c7f",
      "ace3edab",
      "98b51cd2",
      "da619948",
      "cf38c21e",
      "2ae6d927",
      "c0e3c9ce"
    ],
    "peak_mass": 2891.1793596791003,
    "dominant_channel": 2
  },
  "8eb3233b": {
    "parent": "fd6f4435",
    "generation": 1,
    "birth_frame": 4,
    "death_frame": 5,
    "lifespan": 1,
    "children": [],
    "peak_mass": 66.27235797541789,
    "dominant_channel": 2
  },
  "81499f5a": {
    "parent": "fd6f4435",
    "generation": 1,
    "birth_frame": 4,
    "death_frame": 5,
    "lifespan": 1,
    "children": [],
    "peak_mass": 54.578484589218306,
    "dominant_channel": 2
  },
  "62d06d01": {
    "parent": "fd6f4435",
    "generation": 1,
    "birth_frame": 4,
    "death_frame": 5,
    "lifespan": 1,
    "children": [],
    "peak_mass": 41.536849847322735,
    "dominant_channel": 2
  },
  "085c5d95": {
    "parent": "9575a417",
    "generation": 2,
    "birth_frame": 9,
    "death_frame": 10,
    "lifespan": 1,
    "children": [],
    "peak_mass": 44.18819152128355,
    "dominant_channel": 2
  },
  "029f5b93": {
    "parent": "9575a417",
    "generation": 2,
    "birth_frame": 10,
    "death_frame": 11,
    "lifespan": 1,
    "children": [],
    "peak_mass": 69.67186408724527,
    "dominant_channel": 2
  },
  "d6830ce2": {
    "parent": "9575a417",
    "generation": 2,
    "birth_frame": 10,
    "death_frame": 11,
    "lifespan": 1,
    "children": [],
    "peak_mass": 54.88211676704098,
    "dominant_channel": 2
  },
  "4f95c4a7": {
    "parent": "9575a417",
    "generation": 2,
    "birth_frame": 10,
    "death_frame": 11,
    "lifespan": 1,
    "children": [],
    "peak_mass": 14.042775960688486,
    "dominant_channel": 0
  },
  "9a49dc28": {
    "parent": "9575a417",
    "generation": 2,
    "birth_frame": 11,
    "death_frame": 14,
    "lifespan": 3,
    "children": [
      "ddd2722d",
      "b697de8e",
      "e0c7bdb7"
    ],
    "peak_mass": 433.27352065235846,
    "dominant_channel": 0
  },
  "a5619565": {
    "parent": "9575a417",
    "generation": 2,
    "birth_frame": 11,
    "death_frame": 14,
    "lifespan": 3,
    "children": [
      "dec15b74",
      "668f6bbc"
    ],
    "peak_mass": 392.5780842462258,
    "dominant_channel": 1
  },
  "b3abdb30": {
    "parent": "9575a417",
    "generation": 2,
    "birth_frame": 11,
    "death_frame": 12,
    "lifespan": 1,
    "children": [],
    "peak_mass": 64.17107827605153,
    "dominant_channel": 2
  },
  "9d3fddad": {
    "parent": "9575a417",
    "generation": 2,
    "birth_frame": 11,
    "death_frame": 12,
    "lifespan": 1,
    "children": [],
    "peak_mass": 40.95256631423295,
    "dominant_channel": 2
  },
  "33a32b10": {
    "parent": "9575a417",
    "generation": 2,
    "birth_frame": 11,
    "death_frame": 14,
    "lifespan": 3,
    "children": [],
    "peak_mass": 64.99740083172318,
    "dominant_channel": 0
  },
  "4b5c3c7f": {
    "parent": "9575a417",
    "generation": 2,
    "birth_frame": 11,
    "death_frame": 12,
    "lifespan": 1,
    "children": [],
    "peak_mass": 25.116203407835236,
    "dominant_channel": 2
  },
  "ace3edab": {
    "parent": "9575a417",
    "generation": 2,
    "birth_frame": 11,
    "death_frame": 12,
    "lifespan": 1,
    "children": [],
    "peak_mass": 23.238894481985973,
    "dominant_channel": 2
  },
  "98b51cd2": {
    "parent": "9575a417",
    "generation": 2,
    "birth_frame": 11,
    "death_frame": 12,
    "lifespan": 1,
    "children": [],
    "peak_mass": 20.28944448121579,
    "dominant_channel": 2
  },
  "da619948": {
    "parent": "9575a417",
    "generation": 2,
    "birth_frame": 11,
    "death_frame": 12,
    "lifespan": 1,
    "children": [],
    "peak_mass": 12.96978976245427,
    "dominant_channel": 2
  },
  "ddd2722d": {
    "parent": "9a49dc28",
    "generation": 3,
    "birth_frame": 12,
    "death_frame": null,
    "lifespan": 139,
    "children": [
      "ea217307",
      "1e57a19e",
      "9fd0ab6d",
      "7c6c7701"
    ],
    "peak_mass": 3495.3544393656057,
    "dominant_channel": 2
  },
  "b697de8e": {
    "parent": "9a49dc28",
    "generation": 3,
    "birth_frame": 12,
    "death_frame": 13,
    "lifespan": 1,
    "children": [],
    "peak_mass": 33.477859395329965,
    "dominant_channel": 2
  },
  "e0c7bdb7": {
    "parent": "9a49dc28",
    "generation": 3,
    "birth_frame": 12,
    "death_frame": 13,
    "lifespan": 1,
    "children": [],
    "peak_mass": 17.524910860008074,
    "dominant_channel": 1
  },
  "cf38c21e": {
    "parent": "9575a417",
    "generation": 2,
    "birth_frame": 12,
    "death_frame": 14,
    "lifespan": 2,
    "children": [],
    "peak_mass": 41.109676882625614,
    "dominant_channel": 1
  },
  "2ae6d927": {
    "parent": "9575a417",
    "generation": 2,
    "birth_frame": 12,
    "death_frame": 13,
    "lifespan": 1,
    "children": [],
    "peak_mass": 27.959839540309755,
    "dominant_channel": 1
  },
  "c0e3c9ce": {
    "parent": "9575a417",
    "generation": 2,
    "birth_frame": 12,
    "death_frame": 13,
    "lifespan": 1,
    "children": [],
    "peak_mass": 20.653568250643627,
    "dominant_channel": 1
  },
  "dec15b74": {
    "parent": "a5619565",
    "generation": 3,
    "birth_frame": 12,
    "death_frame": 14,
    "lifespan": 2,
    "children": [],
    "peak_mass": 58.250663761307564,
    "dominant_channel": 2
  },
  "668f6bbc": {
    "parent": "a5619565",
    "generation": 3,
    "birth_frame": 13,
    "death_frame": 14,
    "lifespan": 1,
    "children": [],
    "peak_mass": 17.66767238458722,
    "dominant_channel": 2
  },
  "ec273978": {
    "parent": null,
    "generation": 0,
    "birth_frame": 13,
    "death_frame": 14,
    "lifespan": 1,
    "children": [],
    "peak_mass": 21.430196619899693,
    "dominant_channel": 1
  },
  "71b8a360": {
    "parent": null,
    "generation": 0,
    "birth_frame": 13,
    "death_frame": 14,
    "lifespan": 1,
    "children": [],
    "peak_mass": 58.135992255711,
    "dominant_channel": 2
  },
  "f68934d6": {
    "parent": null,
    "generation": 0,
    "birth_frame": 131,
    "death_frame": 132,
    "lifespan": 1,
    "children": [],
    "peak_mass": 1.7811468777028299,
    "dominant_channel": 1
  },
  "ea217307": {
    "parent": "ddd2722d",
    "generation": 4,
    "birth_frame": 132,
    "death_frame": 133,
    "lifespan": 1,
    "children": [],
    "peak_mass": 4.307545006947841,
    "dominant_channel": 0
  },
  "1e57a19e": {
    "parent": "ddd2722d",
    "generation": 4,
    "birth_frame": 134,
    "death_frame": 139,
    "lifespan": 5,
    "children": [],
    "peak_mass": 7.182010942749902,
    "dominant_channel": 0
  },
  "43d46481": {
    "parent": null,
    "generation": 0,
    "birth_frame": 141,
    "death_frame": 142,
    "lifespan": 1,
    "children": [],
    "peak_mass": 2.1289244934232703,
    "dominant_channel": 1
  },
  "77f5705e": {
    "parent": null,
    "generation": 0,
    "birth_frame": 141,
    "death_frame": 142,
    "lifespan": 1,
    "children": [],
    "peak_mass": 1.69897163857836,
    "dominant_channel": 0
  },
  "a1de70a5": {
    "parent": null,
    "generation": 0,
    "birth_frame": 141,
    "death_frame": 142,
    "lifespan": 1,
    "children": [],
    "peak_mass": 4.295298877885703,
    "dominant_channel": 0
  },
  "89570fbe": {
    "parent": null,
    "generation": 0,
    "birth_frame": 143,
    "death_frame": 144,
    "lifespan": 1,
    "children": [],
    "peak_mass": 1.445723510929109,
    "dominant_channel": 0
  },
  "9fd0ab6d": {
    "parent": "ddd2722d",
    "generation": 4,
    "birth_frame": 144,
    "death_frame": 146,
    "lifespan": 2,
    "children": [],
    "peak_mass": 3.6758508607837204,
    "dominant_channel": 0
  },
  "7c6c7701": {
    "parent": "ddd2722d",
    "generation": 4,
    "birth_frame": 146,
    "death_frame": 147,
    "lifespan": 1,
    "children": [],
    "peak_mass": 2.2236671048903887,
    "dominant_channel": 1
  }
}
```

## Media

- `outputs/SPECIES_016_NODULUS_final.png`
- `outputs/SPECIES_016_NODULUS.gif`
- `outputs/SPECIES_016_NODULUS.mp4`

- genome: `outputs/species/SPECIES_016_NODULUS_genome.json`
