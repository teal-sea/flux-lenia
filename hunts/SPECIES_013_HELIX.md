# SPECIES 013 — HELIX

**Verdict:** VIABLE + REPRODUCING
**Origin:** random  |  **Seed:** 661

## Viability gates

| gate | verdict | value | detail |
| --- | --- | --- | --- |
| mass_conservation | PASS | 1.354e-16 | tol=0.0001 |
| non_triviality | PASS | 33.4909 | conc>=6.0, occupancy 0.129<=0.45, 6 bodies |
| persistence | PASS | 1 | 1 organisms alive at the end with lifespan >= 15 frames |
| activity | PASS | 7.98209 | mean speed of the most mobile organism, cells/frame |

## Behaviour (anomaly bouncer)

| behaviour | established | score | evidence |
| --- | --- | --- | --- |
| phototaxis | no | -0.013 | lamp(26, 64): 38.4->38.8; lamp(102, 64): 38.4->38.9; lamp(64, 26): 38.4->38.6 | min approach -0.013 (needs > 0.05 for every lamp position) |
| predatory_pursuit | no | 0.057 | e76f2b12(ch0) -> c6210185(ch1) closed 39.1 -> 34.6 cells over 17 frames, monotone 0.50, target speed 2.406 |
| cyclic_locomotion | no | 0.441 | uid=eba3f440 circling=0.00 spectral_power=0.15 period=12.5 frames (counted only if >= 4) life=26 frames |

## Reproduction

Measured on the recording run below (the screening run is sampled more coarsely and its counts differ; both are stated separately rather than mixed).

- Divisions counted (offspring survived AND carried at least 10% of the parent's mass): **1**
- Raw fission events before the mass filter: **20** — the difference is debris a large body shed, which is not reproduction
- Surviving offspring total: **1**
- Organisms tracked in this run: **179**
- Screening run, for comparison: 1 divisions of 7 raw fissions, deepest generation 6

| frame | parent | children | parent mass | child masses | child share |
| --- | --- | --- | --- | --- | --- |
| 76 | `473b5566` | `03c5f72b` | 1069.3 | 114.7, 31.3, 17.4, 16.2 | 11% |

## Complexity

```json
{
  "morph_diversity": 3.16131100133113,
  "spatial_mi": 1.5025424879681053,
  "cross_channel_mi": 1.3536855558234044,
  "euler_final": 43,
  "concentration_final": 33.49086214753117,
  "occupancy_final": 0.12908935546875,
  "n_blobs_final": 6,
  "activity": 7.98209302304734,
  "mass_drift": 1.3540049853802243e-16,
  "score": 15.36870737573419
}
```

## Lineage tree

```json
{
  "83f786e3": {
    "parent": null,
    "generation": 0,
    "birth_frame": 0,
    "death_frame": 55,
    "lifespan": 55,
    "children": [
      "4554d665",
      "ccadfb76",
      "7da43677",
      "cf5db8ca",
      "265e9038",
      "0f365c0b",
      "8fc6848e",
      "5b4176f2",
      "6c6f2c2d",
      "bd8eb9b5",
      "b4a9e63d",
      "681447bd",
      "7f5cabbd",
      "93ed9e03",
      "83eb398c",
      "738d40a9",
      "7d1143af",
      "4c715de7"
    ],
    "peak_mass": 1668.5145509711704,
    "dominant_channel": 2
  },
  "4554d665": {
    "parent": "83f786e3",
    "generation": 1,
    "birth_frame": 32,
    "death_frame": 33,
    "lifespan": 1,
    "children": [],
    "peak_mass": 13.417829629346256,
    "dominant_channel": 0
  },
  "ccadfb76": {
    "parent": "83f786e3",
    "generation": 1,
    "birth_frame": 37,
    "death_frame": 38,
    "lifespan": 1,
    "children": [],
    "peak_mass": 17.927094534290358,
    "dominant_channel": 0
  },
  "7da43677": {
    "parent": "83f786e3",
    "generation": 1,
    "birth_frame": 37,
    "death_frame": 41,
    "lifespan": 4,
    "children": [],
    "peak_mass": 14.347545515639824,
    "dominant_channel": 0
  },
  "cf5db8ca": {
    "parent": "83f786e3",
    "generation": 1,
    "birth_frame": 42,
    "death_frame": 43,
    "lifespan": 1,
    "children": [],
    "peak_mass": 10.93368696438582,
    "dominant_channel": 0
  },
  "265e9038": {
    "parent": "83f786e3",
    "generation": 1,
    "birth_frame": 43,
    "death_frame": 45,
    "lifespan": 2,
    "children": [],
    "peak_mass": 27.82218387962442,
    "dominant_channel": 0
  },
  "0f365c0b": {
    "parent": "83f786e3",
    "generation": 1,
    "birth_frame": 43,
    "death_frame": 44,
    "lifespan": 1,
    "children": [],
    "peak_mass": 10.680579471392548,
    "dominant_channel": 0
  },
  "ff64c937": {
    "parent": null,
    "generation": 0,
    "birth_frame": 43,
    "death_frame": 44,
    "lifespan": 1,
    "children": [],
    "peak_mass": 9.218013610241945,
    "dominant_channel": 0
  },
  "8fc6848e": {
    "parent": "83f786e3",
    "generation": 1,
    "birth_frame": 45,
    "death_frame": 47,
    "lifespan": 2,
    "children": [],
    "peak_mass": 16.816897515519308,
    "dominant_channel": 0
  },
  "5b4176f2": {
    "parent": "83f786e3",
    "generation": 1,
    "birth_frame": 46,
    "death_frame": 47,
    "lifespan": 1,
    "children": [],
    "peak_mass": 21.36496902546979,
    "dominant_channel": 0
  },
  "6c6f2c2d": {
    "parent": "83f786e3",
    "generation": 1,
    "birth_frame": 46,
    "death_frame": 47,
    "lifespan": 1,
    "children": [],
    "peak_mass": 12.570544943315198,
    "dominant_channel": 0
  },
  "bd8eb9b5": {
    "parent": "83f786e3",
    "generation": 1,
    "birth_frame": 47,
    "death_frame": 48,
    "lifespan": 1,
    "children": [],
    "peak_mass": 6.547660294049763,
    "dominant_channel": 2
  },
  "74ac3770": {
    "parent": null,
    "generation": 0,
    "birth_frame": 47,
    "death_frame": 48,
    "lifespan": 1,
    "children": [],
    "peak_mass": 12.245484920153658,
    "dominant_channel": 0
  },
  "b4a9e63d": {
    "parent": "83f786e3",
    "generation": 1,
    "birth_frame": 48,
    "death_frame": 54,
    "lifespan": 6,
    "children": [],
    "peak_mass": 25.046585671566795,
    "dominant_channel": 0
  },
  "681447bd": {
    "parent": "83f786e3",
    "generation": 1,
    "birth_frame": 48,
    "death_frame": 62,
    "lifespan": 14,
    "children": [],
    "peak_mass": 17.734521295703477,
    "dominant_channel": 0
  },
  "7f5cabbd": {
    "parent": "83f786e3",
    "generation": 1,
    "birth_frame": 48,
    "death_frame": 49,
    "lifespan": 1,
    "children": [],
    "peak_mass": 16.234833545085845,
    "dominant_channel": 0
  },
  "1e9e22ea": {
    "parent": null,
    "generation": 0,
    "birth_frame": 49,
    "death_frame": 51,
    "lifespan": 2,
    "children": [],
    "peak_mass": 9.13009324700447,
    "dominant_channel": 0
  },
  "93ed9e03": {
    "parent": "83f786e3",
    "generation": 1,
    "birth_frame": 52,
    "death_frame": 54,
    "lifespan": 2,
    "children": [],
    "peak_mass": 7.479998935249839,
    "dominant_channel": 0
  },
  "07ded4d1": {
    "parent": null,
    "generation": 0,
    "birth_frame": 53,
    "death_frame": 55,
    "lifespan": 2,
    "children": [],
    "peak_mass": 15.798244318228146,
    "dominant_channel": 0
  },
  "83eb398c": {
    "parent": "83f786e3",
    "generation": 1,
    "birth_frame": 54,
    "death_frame": 75,
    "lifespan": 21,
    "children": [
      "5e805df5",
      "17702c82",
      "4babbf46",
      "61f78a4e",
      "3b68820b",
      "5ca52ce5",
      "befca47a",
      "5e77837e",
      "768f5b6b",
      "7685f203",
      "c0b02828",
      "b4219e4b",
      "6a592908",
      "0e9755c4",
      "6ba45f1c",
      "3d769d91",
      "32d1afda",
      "6c8df17e",
      "b70960ae",
      "473b5566"
    ],
    "peak_mass": 1519.790214613783,
    "dominant_channel": 2
  },
  "738d40a9": {
    "parent": "83f786e3",
    "generation": 1,
    "birth_frame": 55,
    "death_frame": 62,
    "lifespan": 7,
    "children": [],
    "peak_mass": 17.462241751448037,
    "dominant_channel": 0
  },
  "7d1143af": {
    "parent": "83f786e3",
    "generation": 1,
    "birth_frame": 55,
    "death_frame": 56,
    "lifespan": 1,
    "children": [],
    "peak_mass": 14.467313527923809,
    "dominant_channel": 0
  },
  "4c715de7": {
    "parent": "83f786e3",
    "generation": 1,
    "birth_frame": 55,
    "death_frame": 56,
    "lifespan": 1,
    "children": [],
    "peak_mass": 9.562596221674209,
    "dominant_channel": 2
  },
  "5e805df5": {
    "parent": "83eb398c",
    "generation": 2,
    "birth_frame": 56,
    "death_frame": 57,
    "lifespan": 1,
    "children": [],
    "peak_mass": 22.03469389120098,
    "dominant_channel": 0
  },
  "17702c82": {
    "parent": "83eb398c",
    "generation": 2,
    "birth_frame": 57,
    "death_frame": 58,
    "lifespan": 1,
    "children": [],
    "peak_mass": 15.8708892806454,
    "dominant_channel": 0
  },
  "4babbf46": {
    "parent": "83eb398c",
    "generation": 2,
    "birth_frame": 58,
    "death_frame": 62,
    "lifespan": 4,
    "children": [],
    "peak_mass": 22.143539921416618,
    "dominant_channel": 0
  },
  "61f78a4e": {
    "parent": "83eb398c",
    "generation": 2,
    "birth_frame": 58,
    "death_frame": 60,
    "lifespan": 2,
    "children": [],
    "peak_mass": 12.387194454849949,
    "dominant_channel": 0
  },
  "3b68820b": {
    "parent": "83eb398c",
    "generation": 2,
    "birth_frame": 58,
    "death_frame": 65,
    "lifespan": 7,
    "children": [],
    "peak_mass": 28.39421687897384,
    "dominant_channel": 0
  },
  "5ca52ce5": {
    "parent": "83eb398c",
    "generation": 2,
    "birth_frame": 59,
    "death_frame": 61,
    "lifespan": 2,
    "children": [],
    "peak_mass": 8.62146362115183,
    "dominant_channel": 0
  },
  "070bcc47": {
    "parent": null,
    "generation": 0,
    "birth_frame": 61,
    "death_frame": 62,
    "lifespan": 1,
    "children": [],
    "peak_mass": 8.131468791790184,
    "dominant_channel": 0
  },
  "74c7cce4": {
    "parent": null,
    "generation": 0,
    "birth_frame": 61,
    "death_frame": 62,
    "lifespan": 1,
    "children": [],
    "peak_mass": 7.609715110715869,
    "dominant_channel": 0
  },
  "b9ece891": {
    "parent": null,
    "generation": 0,
    "birth_frame": 62,
    "death_frame": 63,
    "lifespan": 1,
    "children": [],
    "peak_mass": 14.865283449287178,
    "dominant_channel": 0
  },
  "befca47a": {
    "parent": "83eb398c",
    "generation": 2,
    "birth_frame": 63,
    "death_frame": 66,
    "lifespan": 3,
    "children": [],
    "peak_mass": 20.336804939455003,
    "dominant_channel": 0
  },
  "5e77837e": {
    "parent": "83eb398c",
    "generation": 2,
    "birth_frame": 63,
    "death_frame": 65,
    "lifespan": 2,
    "children": [],
    "peak_mass": 14.87645585765421,
    "dominant_channel": 0
  },
  "768f5b6b": {
    "parent": "83eb398c",
    "generation": 2,
    "birth_frame": 63,
    "death_frame": 65,
    "lifespan": 2,
    "children": [],
    "peak_mass": 14.471186515895873,
    "dominant_channel": 0
  },
  "7685f203": {
    "parent": "83eb398c",
    "generation": 2,
    "birth_frame": 64,
    "death_frame": 65,
    "lifespan": 1,
    "children": [],
    "peak_mass": 19.600494631186752,
    "dominant_channel": 0
  },
  "c0b02828": {
    "parent": "83eb398c",
    "generation": 2,
    "birth_frame": 67,
    "death_frame": 69,
    "lifespan": 2,
    "children": [],
    "peak_mass": 16.239358420846617,
    "dominant_channel": 0
  },
  "b4219e4b": {
    "parent": "83eb398c",
    "generation": 2,
    "birth_frame": 67,
    "death_frame": 71,
    "lifespan": 4,
    "children": [],
    "peak_mass": 13.006383888583532,
    "dominant_channel": 0
  },
  "6a592908": {
    "parent": "83eb398c",
    "generation": 2,
    "birth_frame": 67,
    "death_frame": 68,
    "lifespan": 1,
    "children": [],
    "peak_mass": 11.140519376576702,
    "dominant_channel": 0
  },
  "d60c20bd": {
    "parent": null,
    "generation": 0,
    "birth_frame": 68,
    "death_frame": 69,
    "lifespan": 1,
    "children": [],
    "peak_mass": 9.843521221071281,
    "dominant_channel": 0
  }
}
```

## Media

- `outputs/SPECIES_013_HELIX_final.png`
- `outputs/SPECIES_013_HELIX.gif`
- `outputs/SPECIES_013_HELIX.mp4`

- genome: `outputs/species/SPECIES_013_HELIX_genome.json`
