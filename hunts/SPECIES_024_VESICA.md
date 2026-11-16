# SPECIES 024 — VESICA

**Verdict:** VIABLE + REPRODUCING
**Origin:** random  |  **Seed:** 811

## Viability gates

| gate | verdict | value | detail |
| --- | --- | --- | --- |
| mass_conservation | PASS | 2.74785e-16 | tol=0.0001 |
| non_triviality | PASS | 122.073 | conc>=6.0, occupancy 0.034<=0.45, 4 bodies |
| persistence | PASS | 1 | 1 organisms alive at the end with lifespan >= 15 frames |
| activity | PASS | 5.25655 | mean speed of the most mobile organism, cells/frame |

## Behaviour (anomaly bouncer)

| behaviour | established | score | evidence |
| --- | --- | --- | --- |
| phototaxis | no | -0.003 | lamp(26, 64): 38.3->37.9; lamp(102, 64): 38.5->38.2; lamp(64, 26): 38.4->38.6 | min approach -0.003 (needs > 0.05 for every lamp position) |
| predatory_pursuit | YES | 0.399 | f8fbba83(ch0) -> 1e39ed5e(ch0) closed 43.4 -> 18.4 cells over 27 frames, monotone 0.69, target speed 1.490 |
| cyclic_locomotion | no | 0.549 | uid=a609aeb9 circling=0.11 spectral_power=0.18 period=6.3 frames (counted only if >= 4) life=20 frames |

## Reproduction

Measured on the recording run below (the screening run is sampled more coarsely and its counts differ; both are stated separately rather than mixed).

- Divisions counted (offspring survived AND carried at least 10% of the parent's mass): **11**
- Raw fission events before the mass filter: **29** — the difference is debris a large body shed, which is not reproduction
- Surviving offspring total: **11**
- Organisms tracked in this run: **147**
- Screening run, for comparison: 1 divisions of 7 raw fissions, deepest generation 5

| frame | parent | children | parent mass | child masses | child share |
| --- | --- | --- | --- | --- | --- |
| 41 | `1c75469e` | `e9a9875d` | 38.0 | 8.0 | 21% |
| 51 | `92c6c97b` | `9fb1f41b` | 15.5 | 10.1 | 65% |
| 56 | `9fb1f41b` | `895752b3` | 12.8 | 12.8 | 100% |
| 81 | `902d9b0d` | `4ae080f2` | 12.8 | 9.9 | 77% |
| 108 | `28328d93` | `730e83d7` | 28.4 | 9.2 | 33% |
| 109 | `208903b0` | `4f74fb96` | 402.6 | 52.2, 49.6 | 12% |
| 114 | `730e83d7` | `58b3eac0` | 12.6 | 11.7 | 93% |
| 127 | `1e39ed5e` | `a3ee87b7` | 23.5 | 15.3 | 65% |
| 137 | `b2883b4e` | `e97078aa` | 9.8 | 9.1 | 93% |
| 140 | `77f9b325` | `5fd57cf5` | 25.5 | 6.7 | 26% |
| 141 | `2cfa4e9f` | `e262c4f7` | 34.4 | 17.5 | 51% |

## Complexity

```json
{
  "morph_diversity": 3.3272022649243462,
  "spatial_mi": 1.488415316055936,
  "cross_channel_mi": 0.23768801035356973,
  "euler_final": 74,
  "concentration_final": 122.07301375461638,
  "occupancy_final": 0.03387451171875,
  "n_blobs_final": 4,
  "activity": 5.256549408981715,
  "mass_drift": 2.747849930200554e-16,
  "score": 15.158454131822156
}
```

## Lineage tree

```json
{
  "da02b5c7": {
    "parent": null,
    "generation": 0,
    "birth_frame": 0,
    "death_frame": 27,
    "lifespan": 27,
    "children": [
      "4fbe32be",
      "fd0f5ba5",
      "9eb07a4c",
      "0b00481f"
    ],
    "peak_mass": 819.286509081134,
    "dominant_channel": 0
  },
  "65d8ec45": {
    "parent": null,
    "generation": 0,
    "birth_frame": 10,
    "death_frame": 12,
    "lifespan": 2,
    "children": [],
    "peak_mass": 5.012141016096307,
    "dominant_channel": 1
  },
  "8e07c543": {
    "parent": null,
    "generation": 0,
    "birth_frame": 12,
    "death_frame": 13,
    "lifespan": 1,
    "children": [],
    "peak_mass": 4.558537064066312,
    "dominant_channel": 1
  },
  "4fbe32be": {
    "parent": "da02b5c7",
    "generation": 1,
    "birth_frame": 15,
    "death_frame": 22,
    "lifespan": 7,
    "children": [],
    "peak_mass": 12.615530320617806,
    "dominant_channel": 0
  },
  "574e6632": {
    "parent": null,
    "generation": 0,
    "birth_frame": 15,
    "death_frame": 16,
    "lifespan": 1,
    "children": [],
    "peak_mass": 5.192450796138075,
    "dominant_channel": 1
  },
  "0949448b": {
    "parent": null,
    "generation": 0,
    "birth_frame": 18,
    "death_frame": 19,
    "lifespan": 1,
    "children": [],
    "peak_mass": 6.613129593781513,
    "dominant_channel": 0
  },
  "fd0f5ba5": {
    "parent": "da02b5c7",
    "generation": 1,
    "birth_frame": 20,
    "death_frame": 24,
    "lifespan": 4,
    "children": [],
    "peak_mass": 13.360796442614419,
    "dominant_channel": 0
  },
  "5ec9f0ae": {
    "parent": null,
    "generation": 0,
    "birth_frame": 20,
    "death_frame": 21,
    "lifespan": 1,
    "children": [],
    "peak_mass": 5.521921657829279,
    "dominant_channel": 0
  },
  "8178eae3": {
    "parent": null,
    "generation": 0,
    "birth_frame": 21,
    "death_frame": 22,
    "lifespan": 1,
    "children": [],
    "peak_mass": 7.4927072040792275,
    "dominant_channel": 0
  },
  "3778bf17": {
    "parent": null,
    "generation": 0,
    "birth_frame": 23,
    "death_frame": 24,
    "lifespan": 1,
    "children": [],
    "peak_mass": 13.73280597338419,
    "dominant_channel": 0
  },
  "9eb07a4c": {
    "parent": "da02b5c7",
    "generation": 1,
    "birth_frame": 25,
    "death_frame": 44,
    "lifespan": 19,
    "children": [
      "47a8f647",
      "dce83403"
    ],
    "peak_mass": 29.718019333598985,
    "dominant_channel": 0
  },
  "0b00481f": {
    "parent": "da02b5c7",
    "generation": 1,
    "birth_frame": 26,
    "death_frame": 50,
    "lifespan": 24,
    "children": [
      "347e98fe",
      "032577d9",
      "d79e320f",
      "7f8f1a8e",
      "1c75469e",
      "f76897ba"
    ],
    "peak_mass": 700.2887053636123,
    "dominant_channel": 2
  },
  "347e98fe": {
    "parent": "0b00481f",
    "generation": 2,
    "birth_frame": 28,
    "death_frame": 37,
    "lifespan": 9,
    "children": [],
    "peak_mass": 33.31572242467611,
    "dominant_channel": 0
  },
  "032577d9": {
    "parent": "0b00481f",
    "generation": 2,
    "birth_frame": 28,
    "death_frame": 33,
    "lifespan": 5,
    "children": [],
    "peak_mass": 17.512341124235093,
    "dominant_channel": 0
  },
  "47a8f647": {
    "parent": "9eb07a4c",
    "generation": 2,
    "birth_frame": 28,
    "death_frame": 29,
    "lifespan": 1,
    "children": [],
    "peak_mass": 6.766481518803849,
    "dominant_channel": 0
  },
  "b9a2a712": {
    "parent": null,
    "generation": 0,
    "birth_frame": 32,
    "death_frame": 33,
    "lifespan": 1,
    "children": [],
    "peak_mass": 7.094594092402823,
    "dominant_channel": 0
  },
  "d79e320f": {
    "parent": "0b00481f",
    "generation": 2,
    "birth_frame": 37,
    "death_frame": 38,
    "lifespan": 1,
    "children": [],
    "peak_mass": 19.47108031203378,
    "dominant_channel": 0
  },
  "acab13f5": {
    "parent": null,
    "generation": 0,
    "birth_frame": 37,
    "death_frame": 43,
    "lifespan": 6,
    "children": [],
    "peak_mass": 14.298125816212025,
    "dominant_channel": 0
  },
  "dce83403": {
    "parent": "9eb07a4c",
    "generation": 2,
    "birth_frame": 39,
    "death_frame": 40,
    "lifespan": 1,
    "children": [],
    "peak_mass": 5.388959768729005,
    "dominant_channel": 1
  },
  "7f8f1a8e": {
    "parent": "0b00481f",
    "generation": 2,
    "birth_frame": 40,
    "death_frame": 41,
    "lifespan": 1,
    "children": [],
    "peak_mass": 36.62076225821936,
    "dominant_channel": 0
  },
  "1c75469e": {
    "parent": "0b00481f",
    "generation": 2,
    "birth_frame": 40,
    "death_frame": 43,
    "lifespan": 3,
    "children": [
      "e9a9875d"
    ],
    "peak_mass": 39.08524089890935,
    "dominant_channel": 0
  },
  "e9a9875d": {
    "parent": "1c75469e",
    "generation": 3,
    "birth_frame": 41,
    "death_frame": 49,
    "lifespan": 8,
    "children": [
      "89b5be94",
      "59d7b8fb"
    ],
    "peak_mass": 44.17338486397809,
    "dominant_channel": 0
  },
  "bfd065ec": {
    "parent": null,
    "generation": 0,
    "birth_frame": 41,
    "death_frame": 42,
    "lifespan": 1,
    "children": [],
    "peak_mass": 6.086656441155712,
    "dominant_channel": 0
  },
  "89b5be94": {
    "parent": "e9a9875d",
    "generation": 4,
    "birth_frame": 44,
    "death_frame": 47,
    "lifespan": 3,
    "children": [],
    "peak_mass": 14.121829701614926,
    "dominant_channel": 0
  },
  "2cfb13d1": {
    "parent": null,
    "generation": 0,
    "birth_frame": 45,
    "death_frame": 47,
    "lifespan": 2,
    "children": [],
    "peak_mass": 9.567669827397774,
    "dominant_channel": 0
  },
  "92c6c97b": {
    "parent": null,
    "generation": 0,
    "birth_frame": 46,
    "death_frame": 52,
    "lifespan": 6,
    "children": [
      "9fb1f41b"
    ],
    "peak_mass": 30.079534495494077,
    "dominant_channel": 0
  },
  "f76897ba": {
    "parent": "0b00481f",
    "generation": 2,
    "birth_frame": 47,
    "death_frame": 49,
    "lifespan": 2,
    "children": [],
    "peak_mass": 23.912013786010093,
    "dominant_channel": 0
  },
  "3742c193": {
    "parent": null,
    "generation": 0,
    "birth_frame": 48,
    "death_frame": 49,
    "lifespan": 1,
    "children": [],
    "peak_mass": 10.365960512284605,
    "dominant_channel": 0
  },
  "61406751": {
    "parent": null,
    "generation": 0,
    "birth_frame": 48,
    "death_frame": 50,
    "lifespan": 2,
    "children": [],
    "peak_mass": 14.27000586556057,
    "dominant_channel": 0
  },
  "59d7b8fb": {
    "parent": "e9a9875d",
    "generation": 4,
    "birth_frame": 49,
    "death_frame": 66,
    "lifespan": 17,
    "children": [
      "9b4a6714",
      "0e9b296e",
      "508fe83b",
      "210035f3",
      "e5743c19",
      "29d63d6e",
      "65f536ff",
      "62a5e753",
      "e534427e"
    ],
    "peak_mass": 689.8078281378371,
    "dominant_channel": 2
  },
  "9fb1f41b": {
    "parent": "92c6c97b",
    "generation": 1,
    "birth_frame": 51,
    "death_frame": 57,
    "lifespan": 6,
    "children": [
      "895752b3"
    ],
    "peak_mass": 24.11072938214222,
    "dominant_channel": 0
  },
  "9b4a6714": {
    "parent": "59d7b8fb",
    "generation": 5,
    "birth_frame": 51,
    "death_frame": 62,
    "lifespan": 11,
    "children": [],
    "peak_mass": 18.363834847183803,
    "dominant_channel": 0
  },
  "0e9b296e": {
    "parent": "59d7b8fb",
    "generation": 5,
    "birth_frame": 51,
    "death_frame": 53,
    "lifespan": 2,
    "children": [],
    "peak_mass": 8.527118895179147,
    "dominant_channel": 0
  },
  "508fe83b": {
    "parent": "59d7b8fb",
    "generation": 5,
    "birth_frame": 52,
    "death_frame": 55,
    "lifespan": 3,
    "children": [],
    "peak_mass": 22.78158255525644,
    "dominant_channel": 0
  },
  "210035f3": {
    "parent": "59d7b8fb",
    "generation": 5,
    "birth_frame": 53,
    "death_frame": 56,
    "lifespan": 3,
    "children": [],
    "peak_mass": 44.06856388592252,
    "dominant_channel": 0
  },
  "e5743c19": {
    "parent": "59d7b8fb",
    "generation": 5,
    "birth_frame": 53,
    "death_frame": 54,
    "lifespan": 1,
    "children": [],
    "peak_mass": 5.859393274182656,
    "dominant_channel": 0
  },
  "86ec2bb4": {
    "parent": null,
    "generation": 0,
    "birth_frame": 55,
    "death_frame": 60,
    "lifespan": 5,
    "children": [],
    "peak_mass": 11.109310096879843,
    "dominant_channel": 0
  },
  "895752b3": {
    "parent": "9fb1f41b",
    "generation": 2,
    "birth_frame": 56,
    "death_frame": 73,
    "lifespan": 17,
    "children": [],
    "peak_mass": 15.724955657605273,
    "dominant_channel": 0
  },
  "0a6d366f": {
    "parent": null,
    "generation": 0,
    "birth_frame": 56,
    "death_frame": 57,
    "lifespan": 1,
    "children": [],
    "peak_mass": 4.468957219620535,
    "dominant_channel": 0
  },
  "29d63d6e": {
    "parent": "59d7b8fb",
    "generation": 5,
    "birth_frame": 57,
    "death_frame": 65,
    "lifespan": 8,
    "children": [
      "9c3e1da0"
    ],
    "peak_mass": 46.9881869308756,
    "dominant_channel": 0
  }
}
```

## Media

- `outputs/SPECIES_024_VESICA_final.png`
- `outputs/SPECIES_024_VESICA.gif`
- `outputs/SPECIES_024_VESICA.mp4`

- genome: `outputs/species/SPECIES_024_VESICA_genome.json`
