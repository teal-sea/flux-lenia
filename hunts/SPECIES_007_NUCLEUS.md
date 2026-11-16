# SPECIES 007 — NUCLEUS

**Verdict:** VIABLE + REPRODUCING
**Origin:** random  |  **Seed:** 543

## Viability gates

| gate | verdict | value | detail |
| --- | --- | --- | --- |
| mass_conservation | PASS | 3.81693e-16 | tol=0.0001 |
| non_triviality | PASS | 33.4761 | conc>=6.0, occupancy 0.131<=0.45, 9 bodies |
| persistence | PASS | 4 | 4 organisms alive at the end with lifespan >= 15 frames |
| activity | PASS | 0.43958 | mean speed of the most mobile organism, cells/frame |

## Behaviour (anomaly bouncer)

| behaviour | established | score | evidence |
| --- | --- | --- | --- |
| phototaxis | no | -0.002 | lamp(26, 64): 38.4->38.5; lamp(102, 64): 38.4->38.3; lamp(64, 26): 38.3->37.6 | min approach -0.002 (needs > 0.05 for every lamp position) |
| predatory_pursuit | no | 0.005 | 6648c1f2(ch0) -> 1ca7bf30(ch0) closed 27.6 -> 27.3 cells over 34 frames, monotone 0.39, target speed 0.072 |
| cyclic_locomotion | no | 0.458 | uid=84d2d290 circling=0.09 spectral_power=0.15 period=7.7 frames (counted only if >= 4) life=24 frames |

## Reproduction

Measured on the recording run below (the screening run is sampled more coarsely and its counts differ; both are stated separately rather than mixed).

- Divisions counted (offspring survived AND carried at least 10% of the parent's mass): **2**
- Raw fission events before the mass filter: **15** — the difference is debris a large body shed, which is not reproduction
- Surviving offspring total: **2**
- Organisms tracked in this run: **31**
- Screening run, for comparison: 2 divisions of 7 raw fissions, deepest generation 2

| frame | parent | children | parent mass | child masses | child share |
| --- | --- | --- | --- | --- | --- |
| 80 | `e41b6304` | `10aa6b57` | 43.2 | 35.1 | 81% |
| 108 | `6648c1f2` | `a2e45539` | 1124.3 | 119.0, 35.3 | 11% |

## Complexity

```json
{
  "morph_diversity": 2.684428171113097,
  "spatial_mi": 1.3836440305460702,
  "cross_channel_mi": 0.6818552683317257,
  "euler_final": 9,
  "concentration_final": 33.476119538222754,
  "occupancy_final": 0.13092041015625,
  "n_blobs_final": 9,
  "activity": 0.43958024042009136,
  "mass_drift": 3.816934238182364e-16,
  "score": 24.38907864742946
}
```

## Lineage tree

```json
{
  "6648c1f2": {
    "parent": null,
    "generation": 0,
    "birth_frame": 0,
    "death_frame": null,
    "lifespan": 151,
    "children": [
      "ebc5b284",
      "aed8f07b",
      "5ea8f425",
      "e41b6304",
      "f7bd8f5d",
      "72d81280",
      "117649db",
      "81d9a7d9",
      "e62e2b00",
      "2f5dac12",
      "4dd83c1d",
      "1ca7bf30",
      "b096c411",
      "19f95434",
      "2e04de43",
      "04567e4f",
      "a2e45539",
      "84d2d290",
      "db024113",
      "5843c283",
      "c64d9f32",
      "b57a8995",
      "509cb32d",
      "2a9ab95b",
      "707c64a4",
      "f4fe93ff",
      "886a568a",
      "a4505e6f"
    ],
    "peak_mass": 1774.6417484750134,
    "dominant_channel": 0
  },
  "ebc5b284": {
    "parent": "6648c1f2",
    "generation": 1,
    "birth_frame": 54,
    "death_frame": 55,
    "lifespan": 1,
    "children": [],
    "peak_mass": 33.670515773623784,
    "dominant_channel": 0
  },
  "aed8f07b": {
    "parent": "6648c1f2",
    "generation": 1,
    "birth_frame": 56,
    "death_frame": 58,
    "lifespan": 2,
    "children": [],
    "peak_mass": 37.80048480868105,
    "dominant_channel": 0
  },
  "5ea8f425": {
    "parent": "6648c1f2",
    "generation": 1,
    "birth_frame": 65,
    "death_frame": 66,
    "lifespan": 1,
    "children": [],
    "peak_mass": 47.50313433138964,
    "dominant_channel": 0
  },
  "e41b6304": {
    "parent": "6648c1f2",
    "generation": 1,
    "birth_frame": 68,
    "death_frame": 97,
    "lifespan": 29,
    "children": [
      "10aa6b57"
    ],
    "peak_mass": 85.17689398105348,
    "dominant_channel": 0
  },
  "f7bd8f5d": {
    "parent": "6648c1f2",
    "generation": 1,
    "birth_frame": 68,
    "death_frame": 71,
    "lifespan": 3,
    "children": [],
    "peak_mass": 41.04929062811934,
    "dominant_channel": 0
  },
  "72d81280": {
    "parent": "6648c1f2",
    "generation": 1,
    "birth_frame": 69,
    "death_frame": 78,
    "lifespan": 9,
    "children": [],
    "peak_mass": 49.51085050190383,
    "dominant_channel": 0
  },
  "117649db": {
    "parent": "6648c1f2",
    "generation": 1,
    "birth_frame": 71,
    "death_frame": 115,
    "lifespan": 44,
    "children": [],
    "peak_mass": 84.7570778277697,
    "dominant_channel": 0
  },
  "81d9a7d9": {
    "parent": "6648c1f2",
    "generation": 1,
    "birth_frame": 72,
    "death_frame": 77,
    "lifespan": 5,
    "children": [],
    "peak_mass": 42.12334988890456,
    "dominant_channel": 0
  },
  "e62e2b00": {
    "parent": "6648c1f2",
    "generation": 1,
    "birth_frame": 77,
    "death_frame": 78,
    "lifespan": 1,
    "children": [],
    "peak_mass": 27.471182575487347,
    "dominant_channel": 0
  },
  "2f5dac12": {
    "parent": "6648c1f2",
    "generation": 1,
    "birth_frame": 79,
    "death_frame": 83,
    "lifespan": 4,
    "children": [],
    "peak_mass": 49.227299522849435,
    "dominant_channel": 0
  },
  "4dd83c1d": {
    "parent": "6648c1f2",
    "generation": 1,
    "birth_frame": 79,
    "death_frame": 82,
    "lifespan": 3,
    "children": [],
    "peak_mass": 29.381717627517396,
    "dominant_channel": 0
  },
  "10aa6b57": {
    "parent": "e41b6304",
    "generation": 2,
    "birth_frame": 80,
    "death_frame": 105,
    "lifespan": 25,
    "children": [],
    "peak_mass": 38.1626433393695,
    "dominant_channel": 0
  },
  "1ca7bf30": {
    "parent": "6648c1f2",
    "generation": 1,
    "birth_frame": 83,
    "death_frame": 117,
    "lifespan": 34,
    "children": [],
    "peak_mass": 30.97571131509943,
    "dominant_channel": 0
  },
  "b096c411": {
    "parent": "6648c1f2",
    "generation": 1,
    "birth_frame": 84,
    "death_frame": 133,
    "lifespan": 49,
    "children": [],
    "peak_mass": 72.11386895604296,
    "dominant_channel": 0
  },
  "19f95434": {
    "parent": "6648c1f2",
    "generation": 1,
    "birth_frame": 97,
    "death_frame": null,
    "lifespan": 54,
    "children": [],
    "peak_mass": 48.02469423019917,
    "dominant_channel": 0
  },
  "2e04de43": {
    "parent": "6648c1f2",
    "generation": 1,
    "birth_frame": 98,
    "death_frame": 111,
    "lifespan": 13,
    "children": [],
    "peak_mass": 46.763911894921854,
    "dominant_channel": 0
  },
  "04567e4f": {
    "parent": "6648c1f2",
    "generation": 1,
    "birth_frame": 104,
    "death_frame": null,
    "lifespan": 47,
    "children": [],
    "peak_mass": 46.640381514703236,
    "dominant_channel": 0
  },
  "a2e45539": {
    "parent": "6648c1f2",
    "generation": 1,
    "birth_frame": 108,
    "death_frame": null,
    "lifespan": 43,
    "children": [],
    "peak_mass": 125.11172148888687,
    "dominant_channel": 0
  },
  "84d2d290": {
    "parent": "6648c1f2",
    "generation": 1,
    "birth_frame": 108,
    "death_frame": 132,
    "lifespan": 24,
    "children": [],
    "peak_mass": 38.35269693810971,
    "dominant_channel": 0
  },
  "db024113": {
    "parent": "6648c1f2",
    "generation": 1,
    "birth_frame": 114,
    "death_frame": 115,
    "lifespan": 1,
    "children": [],
    "peak_mass": 42.83952540605139,
    "dominant_channel": 0
  },
  "5843c283": {
    "parent": "6648c1f2",
    "generation": 1,
    "birth_frame": 116,
    "death_frame": 123,
    "lifespan": 7,
    "children": [],
    "peak_mass": 76.49928179076251,
    "dominant_channel": 0
  },
  "c64d9f32": {
    "parent": "6648c1f2",
    "generation": 1,
    "birth_frame": 116,
    "death_frame": 117,
    "lifespan": 1,
    "children": [],
    "peak_mass": 45.75316079086321,
    "dominant_channel": 0
  },
  "b57a8995": {
    "parent": "6648c1f2",
    "generation": 1,
    "birth_frame": 118,
    "death_frame": null,
    "lifespan": 33,
    "children": [],
    "peak_mass": 46.84188941525064,
    "dominant_channel": 0
  },
  "509cb32d": {
    "parent": "6648c1f2",
    "generation": 1,
    "birth_frame": 118,
    "death_frame": 123,
    "lifespan": 5,
    "children": [],
    "peak_mass": 30.1187555421778,
    "dominant_channel": 0
  },
  "2a9ab95b": {
    "parent": "6648c1f2",
    "generation": 1,
    "birth_frame": 128,
    "death_frame": 138,
    "lifespan": 10,
    "children": [],
    "peak_mass": 77.70076987395525,
    "dominant_channel": 0
  },
  "707c64a4": {
    "parent": "6648c1f2",
    "generation": 1,
    "birth_frame": 136,
    "death_frame": null,
    "lifespan": 15,
    "children": [],
    "peak_mass": 41.6861039039723,
    "dominant_channel": 0
  },
  "f4fe93ff": {
    "parent": "6648c1f2",
    "generation": 1,
    "birth_frame": 137,
    "death_frame": 147,
    "lifespan": 10,
    "children": [],
    "peak_mass": 39.38792375771682,
    "dominant_channel": 0
  },
  "886a568a": {
    "parent": "6648c1f2",
    "generation": 1,
    "birth_frame": 144,
    "death_frame": 145,
    "lifespan": 1,
    "children": [],
    "peak_mass": 42.69564701758931,
    "dominant_channel": 0
  },
  "5602ed90": {
    "parent": null,
    "generation": 0,
    "birth_frame": 147,
    "death_frame": 150,
    "lifespan": 3,
    "children": [],
    "peak_mass": 4.971289465526445,
    "dominant_channel": 2
  },
  "a4505e6f": {
    "parent": "6648c1f2",
    "generation": 1,
    "birth_frame": 150,
    "death_frame": null,
    "lifespan": 1,
    "children": [],
    "peak_mass": 44.49487140395642,
    "dominant_channel": 0
  }
}
```

## Media

- `outputs/SPECIES_007_NUCLEUS_final.png`
- `outputs/SPECIES_007_NUCLEUS.gif`
- `outputs/SPECIES_007_NUCLEUS.mp4`

- genome: `outputs/species/SPECIES_007_NUCLEUS_genome.json`
