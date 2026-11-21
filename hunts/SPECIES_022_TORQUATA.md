# SPECIES 022 — TORQUATA

**Verdict:** VIABLE + REPRODUCING
**Origin:** random  |  **Seed:** 800

## Viability gates

| gate | verdict | value | detail |
| --- | --- | --- | --- |
| mass_conservation | PASS | 2.02708e-16 | tol=0.0001 |
| non_triviality | PASS | 11.2565 | conc>=6.0, occupancy 0.334<=0.45, 2 bodies |
| persistence | PASS | 1 | 1 organisms alive at the end with lifespan >= 15 frames |
| activity | PASS | 0.421645 | mean speed of the most mobile organism, cells/frame |

## Behaviour (anomaly bouncer)

| behaviour | established | score | evidence |
| --- | --- | --- | --- |
| phototaxis | no | -0.008 | lamp(26, 64): 38.4->38.4; lamp(102, 64): 38.4->38.7; lamp(64, 26): 38.4->38.6 | min approach -0.008 (needs > 0.05 for every lamp position) |
| predatory_pursuit | no | 0.000 | no closing pair found |
| cyclic_locomotion | no | 0.031 | uid=69802926 circling=0.03 spectral_power=0.02 period=2.3 frames (counted only if >= 4) life=132 frames |

## Reproduction

Measured on the recording run below (the screening run is sampled more coarsely and its counts differ; both are stated separately rather than mixed).

- Divisions counted (offspring survived AND carried at least 10% of the parent's mass): **0**
- Raw fission events before the mass filter: **1** — the difference is debris a large body shed, which is not reproduction
- Surviving offspring total: **0**
- Organisms tracked in this run: **66**
- Screening run, for comparison: 1 divisions of 1 raw fissions, deepest generation 3

## Complexity

```json
{
  "morph_diversity": 1.8112730735542897,
  "spatial_mi": 1.5042986681621193,
  "cross_channel_mi": 0.9688891441260403,
  "euler_final": 18,
  "concentration_final": 11.256465409768852,
  "occupancy_final": 0.333984375,
  "n_blobs_final": 2,
  "activity": 0.42164510605432676,
  "mass_drift": 2.0270839741037632e-16,
  "score": 15.365481758092749
}
```

## Lineage tree

```json
{
  "a07cbaa6": {
    "parent": null,
    "generation": 0,
    "birth_frame": 0,
    "death_frame": 4,
    "lifespan": 4,
    "children": [
      "73c60929",
      "9622d7d2",
      "efcea654",
      "06999146",
      "edf07157"
    ],
    "peak_mass": 2224.356992820512,
    "dominant_channel": 0
  },
  "73c60929": {
    "parent": "a07cbaa6",
    "generation": 1,
    "birth_frame": 1,
    "death_frame": 2,
    "lifespan": 1,
    "children": [],
    "peak_mass": 33.56483390761954,
    "dominant_channel": 0
  },
  "9622d7d2": {
    "parent": "a07cbaa6",
    "generation": 1,
    "birth_frame": 3,
    "death_frame": 5,
    "lifespan": 2,
    "children": [
      "03025f30",
      "c2edf392",
      "28e11511",
      "1e733b91"
    ],
    "peak_mass": 538.5928191444041,
    "dominant_channel": 0
  },
  "efcea654": {
    "parent": "a07cbaa6",
    "generation": 1,
    "birth_frame": 3,
    "death_frame": 4,
    "lifespan": 1,
    "children": [],
    "peak_mass": 48.27252050779793,
    "dominant_channel": 0
  },
  "06999146": {
    "parent": "a07cbaa6",
    "generation": 1,
    "birth_frame": 3,
    "death_frame": 4,
    "lifespan": 1,
    "children": [],
    "peak_mass": 38.66715935661313,
    "dominant_channel": 0
  },
  "03025f30": {
    "parent": "9622d7d2",
    "generation": 2,
    "birth_frame": 4,
    "death_frame": 7,
    "lifespan": 3,
    "children": [
      "2d35f3dc",
      "1512dd91",
      "f1ea390a"
    ],
    "peak_mass": 212.27462391238575,
    "dominant_channel": 0
  },
  "c2edf392": {
    "parent": "9622d7d2",
    "generation": 2,
    "birth_frame": 4,
    "death_frame": 7,
    "lifespan": 3,
    "children": [
      "af2c2347",
      "ae5290f2",
      "92cee16d"
    ],
    "peak_mass": 313.69889708680824,
    "dominant_channel": 1
  },
  "28e11511": {
    "parent": "9622d7d2",
    "generation": 2,
    "birth_frame": 4,
    "death_frame": 5,
    "lifespan": 1,
    "children": [],
    "peak_mass": 33.998028640652976,
    "dominant_channel": 0
  },
  "1e733b91": {
    "parent": "9622d7d2",
    "generation": 2,
    "birth_frame": 4,
    "death_frame": 5,
    "lifespan": 1,
    "children": [],
    "peak_mass": 33.41001679414998,
    "dominant_channel": 0
  },
  "edf07157": {
    "parent": "a07cbaa6",
    "generation": 1,
    "birth_frame": 4,
    "death_frame": 5,
    "lifespan": 1,
    "children": [],
    "peak_mass": 44.18801477774084,
    "dominant_channel": 0
  },
  "2d35f3dc": {
    "parent": "03025f30",
    "generation": 3,
    "birth_frame": 5,
    "death_frame": 6,
    "lifespan": 1,
    "children": [],
    "peak_mass": 53.40180951668507,
    "dominant_channel": 0
  },
  "db491663": {
    "parent": null,
    "generation": 0,
    "birth_frame": 5,
    "death_frame": 8,
    "lifespan": 3,
    "children": [
      "2dbd03a5"
    ],
    "peak_mass": 56.46937092679515,
    "dominant_channel": 0
  },
  "af2c2347": {
    "parent": "c2edf392",
    "generation": 3,
    "birth_frame": 6,
    "death_frame": 7,
    "lifespan": 1,
    "children": [],
    "peak_mass": 28.502849691103286,
    "dominant_channel": 0
  },
  "1512dd91": {
    "parent": "03025f30",
    "generation": 3,
    "birth_frame": 6,
    "death_frame": 10,
    "lifespan": 4,
    "children": [
      "381b7c13",
      "f2a52465"
    ],
    "peak_mass": 302.00193388821623,
    "dominant_channel": 0
  },
  "ae5290f2": {
    "parent": "c2edf392",
    "generation": 3,
    "birth_frame": 7,
    "death_frame": 8,
    "lifespan": 1,
    "children": [],
    "peak_mass": 39.540013472598886,
    "dominant_channel": 1
  },
  "92cee16d": {
    "parent": "c2edf392",
    "generation": 3,
    "birth_frame": 7,
    "death_frame": 8,
    "lifespan": 1,
    "children": [],
    "peak_mass": 21.718261767040993,
    "dominant_channel": 0
  },
  "f1ea390a": {
    "parent": "03025f30",
    "generation": 3,
    "birth_frame": 7,
    "death_frame": 8,
    "lifespan": 1,
    "children": [],
    "peak_mass": 144.11017752967678,
    "dominant_channel": 0
  },
  "94388c52": {
    "parent": null,
    "generation": 0,
    "birth_frame": 7,
    "death_frame": 9,
    "lifespan": 2,
    "children": [
      "be2e5a36"
    ],
    "peak_mass": 97.05015180165528,
    "dominant_channel": 1
  },
  "5fa8ba24": {
    "parent": null,
    "generation": 0,
    "birth_frame": 7,
    "death_frame": 8,
    "lifespan": 1,
    "children": [],
    "peak_mass": 31.0475957097687,
    "dominant_channel": 1
  },
  "be2e5a36": {
    "parent": "94388c52",
    "generation": 1,
    "birth_frame": 8,
    "death_frame": 12,
    "lifespan": 4,
    "children": [
      "8a8fa6ae",
      "e7f9edb1"
    ],
    "peak_mass": 101.08749262378973,
    "dominant_channel": 0
  },
  "2dbd03a5": {
    "parent": "db491663",
    "generation": 1,
    "birth_frame": 8,
    "death_frame": 12,
    "lifespan": 4,
    "children": [
      "7a8b1f0f",
      "4c033205"
    ],
    "peak_mass": 264.886579164256,
    "dominant_channel": 0
  },
  "381b7c13": {
    "parent": "1512dd91",
    "generation": 4,
    "birth_frame": 9,
    "death_frame": 11,
    "lifespan": 2,
    "children": [],
    "peak_mass": 122.98700219757646,
    "dominant_channel": 0
  },
  "f2a52465": {
    "parent": "1512dd91",
    "generation": 4,
    "birth_frame": 9,
    "death_frame": 10,
    "lifespan": 1,
    "children": [],
    "peak_mass": 57.553311100710594,
    "dominant_channel": 0
  },
  "4d140996": {
    "parent": null,
    "generation": 0,
    "birth_frame": 9,
    "death_frame": 11,
    "lifespan": 2,
    "children": [],
    "peak_mass": 22.56633725809759,
    "dominant_channel": 0
  },
  "282deceb": {
    "parent": null,
    "generation": 0,
    "birth_frame": 9,
    "death_frame": 10,
    "lifespan": 1,
    "children": [],
    "peak_mass": 29.07124373487411,
    "dominant_channel": 0
  },
  "7a8b1f0f": {
    "parent": "2dbd03a5",
    "generation": 2,
    "birth_frame": 10,
    "death_frame": 12,
    "lifespan": 2,
    "children": [],
    "peak_mass": 30.416870666993283,
    "dominant_channel": 0
  },
  "4c033205": {
    "parent": "2dbd03a5",
    "generation": 2,
    "birth_frame": 10,
    "death_frame": 13,
    "lifespan": 3,
    "children": [],
    "peak_mass": 809.6907597205324,
    "dominant_channel": 0
  },
  "8a8fa6ae": {
    "parent": "be2e5a36",
    "generation": 2,
    "birth_frame": 10,
    "death_frame": 11,
    "lifespan": 1,
    "children": [],
    "peak_mass": 70.59372229739185,
    "dominant_channel": 0
  },
  "e7f9edb1": {
    "parent": "be2e5a36",
    "generation": 2,
    "birth_frame": 10,
    "death_frame": 11,
    "lifespan": 1,
    "children": [],
    "peak_mass": 48.83656894735837,
    "dominant_channel": 1
  },
  "3b2d9a92": {
    "parent": null,
    "generation": 0,
    "birth_frame": 10,
    "death_frame": 12,
    "lifespan": 2,
    "children": [],
    "peak_mass": 67.251575039597,
    "dominant_channel": 0
  },
  "13d6b912": {
    "parent": null,
    "generation": 0,
    "birth_frame": 10,
    "death_frame": 12,
    "lifespan": 2,
    "children": [],
    "peak_mass": 33.791709138979,
    "dominant_channel": 1
  },
  "2b11c33b": {
    "parent": null,
    "generation": 0,
    "birth_frame": 12,
    "death_frame": 20,
    "lifespan": 8,
    "children": [
      "69802926",
      "d6f7e4a6"
    ],
    "peak_mass": 2019.8216076218168,
    "dominant_channel": 0
  },
  "d0194696": {
    "parent": null,
    "generation": 0,
    "birth_frame": 15,
    "death_frame": 16,
    "lifespan": 1,
    "children": [],
    "peak_mass": 8.192576018880962,
    "dominant_channel": 2
  },
  "238100ed": {
    "parent": null,
    "generation": 0,
    "birth_frame": 16,
    "death_frame": 17,
    "lifespan": 1,
    "children": [],
    "peak_mass": 7.095989103892653,
    "dominant_channel": 2
  },
  "1de30af3": {
    "parent": null,
    "generation": 0,
    "birth_frame": 17,
    "death_frame": 18,
    "lifespan": 1,
    "children": [],
    "peak_mass": 5.5379060794789625,
    "dominant_channel": 1
  },
  "69802926": {
    "parent": "2b11c33b",
    "generation": 1,
    "birth_frame": 19,
    "death_frame": null,
    "lifespan": 132,
    "children": [
      "39eb34f9",
      "b89498bf",
      "aec8def2",
      "c9f1e76c",
      "b9eae1f1",
      "166a8729",
      "7c14b15f",
      "11d0b59f",
      "229326a3",
      "88fb10aa",
      "d7e019af"
    ],
    "peak_mass": 2172.258078284186,
    "dominant_channel": 0
  },
  "d6f7e4a6": {
    "parent": "2b11c33b",
    "generation": 1,
    "birth_frame": 19,
    "death_frame": 20,
    "lifespan": 1,
    "children": [],
    "peak_mass": 6.005750171378498,
    "dominant_channel": 1
  },
  "39eb34f9": {
    "parent": "69802926",
    "generation": 2,
    "birth_frame": 22,
    "death_frame": 23,
    "lifespan": 1,
    "children": [],
    "peak_mass": 7.897443610482389,
    "dominant_channel": 1
  },
  "b5f20366": {
    "parent": null,
    "generation": 0,
    "birth_frame": 76,
    "death_frame": 78,
    "lifespan": 2,
    "children": [],
    "peak_mass": 1.9173369277095882,
    "dominant_channel": 1
  },
  "75b4a02a": {
    "parent": null,
    "generation": 0,
    "birth_frame": 80,
    "death_frame": 83,
    "lifespan": 3,
    "children": [],
    "peak_mass": 3.557563717499783,
    "dominant_channel": 1
  }
}
```

## Media

- `outputs/SPECIES_022_TORQUATA_final.png`
- `outputs/SPECIES_022_TORQUATA.gif`
- `outputs/SPECIES_022_TORQUATA.mp4`

- genome: `outputs/species/SPECIES_022_TORQUATA_genome.json`
