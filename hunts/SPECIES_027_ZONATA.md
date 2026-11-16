# SPECIES 027 — ZONATA

**Verdict:** VIABLE + REPRODUCING
**Origin:** random  |  **Seed:** 926

## Viability gates

| gate | verdict | value | detail |
| --- | --- | --- | --- |
| mass_conservation | PASS | 1.21789e-16 | tol=0.0001 |
| non_triviality | PASS | 51.3127 | conc>=6.0, occupancy 0.089<=0.45, 20 bodies |
| persistence | PASS | 13 | 13 organisms alive at the end with lifespan >= 15 frames |
| activity | PASS | 6.69939 | mean speed of the most mobile organism, cells/frame |

## Behaviour (anomaly bouncer)

| behaviour | established | score | evidence |
| --- | --- | --- | --- |
| phototaxis | no | -0.022 | lamp(26, 64): 38.5->38.5; lamp(102, 64): 38.3->39.2; lamp(64, 26): 38.4->39.1 | min approach -0.022 (needs > 0.05 for every lamp position) |
| predatory_pursuit | no | 0.252 | 951ac8d8(ch2) -> 7fd76c43(ch1) closed 48.2 -> 31.6 cells over 16 frames, monotone 0.73, target speed 2.559 |
| cyclic_locomotion | no | 0.468 | uid=7f01f62b circling=0.30 spectral_power=0.16 period=5.2 frames (counted only if >= 4) life=22 frames |

## Reproduction

Measured on the recording run below (the screening run is sampled more coarsely and its counts differ; both are stated separately rather than mixed).

- Divisions counted (offspring survived AND carried at least 10% of the parent's mass): **2**
- Raw fission events before the mass filter: **22** — the difference is debris a large body shed, which is not reproduction
- Surviving offspring total: **2**
- Organisms tracked in this run: **305**
- Screening run, for comparison: 3 divisions of 13 raw fissions, deepest generation 8

| frame | parent | children | parent mass | child masses | child share |
| --- | --- | --- | --- | --- | --- |
| 65 | `b03cc29e` | `72791c48` | 17.5 | 12.5 | 72% |
| 145 | `fae18a68` | `43e5de33` | 114.4 | 54.7, 47.9, 32.4, 31.4, 29.5, 15.3 | 42% |

## Complexity

```json
{
  "morph_diversity": 2.6706503273614706,
  "spatial_mi": 1.374764701120845,
  "cross_channel_mi": 0.6927363637696871,
  "euler_final": 68,
  "concentration_final": 51.31272178745616,
  "occupancy_final": 0.0885009765625,
  "n_blobs_final": 20,
  "activity": 6.699386874426502,
  "mass_drift": 1.217889926227267e-16,
  "score": 32.463721474172516
}
```

## Lineage tree

```json
{
  "7f01f62b": {
    "parent": null,
    "generation": 0,
    "birth_frame": 0,
    "death_frame": 22,
    "lifespan": 22,
    "children": [
      "b3e501aa",
      "bb496da1",
      "cd92353f",
      "66dc5950",
      "cb3eb2fb",
      "ac1b5355",
      "f402c2ac",
      "9f72b737",
      "8ef1590f",
      "32d31eb3",
      "acbfc791",
      "26a25895",
      "5ac9ea7f",
      "59c3cda2",
      "88d93231",
      "16e7b3ed",
      "c48c35a4",
      "3f8206c9",
      "5e6e1781",
      "559638ef",
      "03c1f21f",
      "44c11e7c"
    ],
    "peak_mass": 1851.9696700307659,
    "dominant_channel": 1
  },
  "b3e501aa": {
    "parent": "7f01f62b",
    "generation": 1,
    "birth_frame": 9,
    "death_frame": 10,
    "lifespan": 1,
    "children": [],
    "peak_mass": 13.259052010323778,
    "dominant_channel": 2
  },
  "bb496da1": {
    "parent": "7f01f62b",
    "generation": 1,
    "birth_frame": 12,
    "death_frame": 13,
    "lifespan": 1,
    "children": [],
    "peak_mass": 15.373929655057234,
    "dominant_channel": 2
  },
  "cd92353f": {
    "parent": "7f01f62b",
    "generation": 1,
    "birth_frame": 13,
    "death_frame": 24,
    "lifespan": 11,
    "children": [],
    "peak_mass": 25.630492096904,
    "dominant_channel": 2
  },
  "66dc5950": {
    "parent": "7f01f62b",
    "generation": 1,
    "birth_frame": 14,
    "death_frame": 15,
    "lifespan": 1,
    "children": [],
    "peak_mass": 24.128612482779484,
    "dominant_channel": 2
  },
  "cb3eb2fb": {
    "parent": "7f01f62b",
    "generation": 1,
    "birth_frame": 16,
    "death_frame": 17,
    "lifespan": 1,
    "children": [],
    "peak_mass": 22.694363302513104,
    "dominant_channel": 2
  },
  "ac1b5355": {
    "parent": "7f01f62b",
    "generation": 1,
    "birth_frame": 16,
    "death_frame": 17,
    "lifespan": 1,
    "children": [],
    "peak_mass": 20.82981534618528,
    "dominant_channel": 2
  },
  "f402c2ac": {
    "parent": "7f01f62b",
    "generation": 1,
    "birth_frame": 16,
    "death_frame": 17,
    "lifespan": 1,
    "children": [],
    "peak_mass": 19.516084683283957,
    "dominant_channel": 2
  },
  "9f72b737": {
    "parent": "7f01f62b",
    "generation": 1,
    "birth_frame": 16,
    "death_frame": 17,
    "lifespan": 1,
    "children": [],
    "peak_mass": 17.811279999692534,
    "dominant_channel": 2
  },
  "8ef1590f": {
    "parent": "7f01f62b",
    "generation": 1,
    "birth_frame": 16,
    "death_frame": 17,
    "lifespan": 1,
    "children": [
      "2617a3e2"
    ],
    "peak_mass": 17.145830847885634,
    "dominant_channel": 2
  },
  "32d31eb3": {
    "parent": "7f01f62b",
    "generation": 1,
    "birth_frame": 16,
    "death_frame": 17,
    "lifespan": 1,
    "children": [],
    "peak_mass": 15.029699765487408,
    "dominant_channel": 2
  },
  "acbfc791": {
    "parent": "7f01f62b",
    "generation": 1,
    "birth_frame": 17,
    "death_frame": 18,
    "lifespan": 1,
    "children": [],
    "peak_mass": 36.9139618927705,
    "dominant_channel": 2
  },
  "26a25895": {
    "parent": "7f01f62b",
    "generation": 1,
    "birth_frame": 17,
    "death_frame": 18,
    "lifespan": 1,
    "children": [],
    "peak_mass": 25.155843068936726,
    "dominant_channel": 2
  },
  "5ac9ea7f": {
    "parent": "7f01f62b",
    "generation": 1,
    "birth_frame": 17,
    "death_frame": 18,
    "lifespan": 1,
    "children": [],
    "peak_mass": 22.64342687110412,
    "dominant_channel": 2
  },
  "2617a3e2": {
    "parent": "8ef1590f",
    "generation": 2,
    "birth_frame": 17,
    "death_frame": 37,
    "lifespan": 20,
    "children": [
      "21e4f4bf"
    ],
    "peak_mass": 27.241835908551256,
    "dominant_channel": 2
  },
  "59c3cda2": {
    "parent": "7f01f62b",
    "generation": 1,
    "birth_frame": 18,
    "death_frame": 20,
    "lifespan": 2,
    "children": [],
    "peak_mass": 22.076865852346195,
    "dominant_channel": 2
  },
  "88d93231": {
    "parent": "7f01f62b",
    "generation": 1,
    "birth_frame": 20,
    "death_frame": 24,
    "lifespan": 4,
    "children": [],
    "peak_mass": 30.193621664159778,
    "dominant_channel": 2
  },
  "16e7b3ed": {
    "parent": "7f01f62b",
    "generation": 1,
    "birth_frame": 20,
    "death_frame": 21,
    "lifespan": 1,
    "children": [],
    "peak_mass": 21.064117041557182,
    "dominant_channel": 2
  },
  "c48c35a4": {
    "parent": "7f01f62b",
    "generation": 1,
    "birth_frame": 20,
    "death_frame": null,
    "lifespan": 131,
    "children": [],
    "peak_mass": 28.679438593257245,
    "dominant_channel": 2
  },
  "3f8206c9": {
    "parent": "7f01f62b",
    "generation": 1,
    "birth_frame": 21,
    "death_frame": 87,
    "lifespan": 66,
    "children": [],
    "peak_mass": 27.04040694254649,
    "dominant_channel": 2
  },
  "5e6e1781": {
    "parent": "7f01f62b",
    "generation": 1,
    "birth_frame": 21,
    "death_frame": 24,
    "lifespan": 3,
    "children": [
      "0604abc1",
      "86450365",
      "31634933"
    ],
    "peak_mass": 1447.4617825739208,
    "dominant_channel": 1
  },
  "559638ef": {
    "parent": "7f01f62b",
    "generation": 1,
    "birth_frame": 21,
    "death_frame": 31,
    "lifespan": 10,
    "children": [],
    "peak_mass": 22.366787400683833,
    "dominant_channel": 2
  },
  "03c1f21f": {
    "parent": "7f01f62b",
    "generation": 1,
    "birth_frame": 21,
    "death_frame": 23,
    "lifespan": 2,
    "children": [],
    "peak_mass": 12.134831251254967,
    "dominant_channel": 1
  },
  "44c11e7c": {
    "parent": "7f01f62b",
    "generation": 1,
    "birth_frame": 22,
    "death_frame": 29,
    "lifespan": 7,
    "children": [],
    "peak_mass": 21.997883792271285,
    "dominant_channel": 2
  },
  "0604abc1": {
    "parent": "5e6e1781",
    "generation": 2,
    "birth_frame": 23,
    "death_frame": 24,
    "lifespan": 1,
    "children": [],
    "peak_mass": 16.51749527663095,
    "dominant_channel": 2
  },
  "86450365": {
    "parent": "5e6e1781",
    "generation": 2,
    "birth_frame": 23,
    "death_frame": 28,
    "lifespan": 5,
    "children": [
      "e4cc2e14",
      "6b8076b2",
      "514ae701",
      "f97db934"
    ],
    "peak_mass": 1486.8540268986887,
    "dominant_channel": 1
  },
  "31634933": {
    "parent": "5e6e1781",
    "generation": 2,
    "birth_frame": 24,
    "death_frame": 25,
    "lifespan": 1,
    "children": [],
    "peak_mass": 21.077274229142972,
    "dominant_channel": 0
  },
  "e4cc2e14": {
    "parent": "86450365",
    "generation": 3,
    "birth_frame": 25,
    "death_frame": 27,
    "lifespan": 2,
    "children": [],
    "peak_mass": 24.78419306514928,
    "dominant_channel": 2
  },
  "6b8076b2": {
    "parent": "86450365",
    "generation": 3,
    "birth_frame": 25,
    "death_frame": 26,
    "lifespan": 1,
    "children": [],
    "peak_mass": 22.81935857793153,
    "dominant_channel": 2
  },
  "da3cd012": {
    "parent": null,
    "generation": 0,
    "birth_frame": 26,
    "death_frame": 27,
    "lifespan": 1,
    "children": [],
    "peak_mass": 6.7982554748140345,
    "dominant_channel": 2
  },
  "514ae701": {
    "parent": "86450365",
    "generation": 3,
    "birth_frame": 27,
    "death_frame": 40,
    "lifespan": 13,
    "children": [
      "8045ca87",
      "9b7f702c",
      "bfd698a3",
      "8fff8d4a",
      "60a91586",
      "77adb14d",
      "0a91ea4e",
      "108d5973",
      "4865fc05",
      "ae041f6b",
      "8396a9c2",
      "c8f6c69e",
      "a384b27f",
      "79dffe68",
      "77fc74f0",
      "2d03b0e4",
      "5ca407dd"
    ],
    "peak_mass": 1524.6310019913606,
    "dominant_channel": 1
  },
  "f97db934": {
    "parent": "86450365",
    "generation": 3,
    "birth_frame": 28,
    "death_frame": 29,
    "lifespan": 1,
    "children": [],
    "peak_mass": 9.573925122033973,
    "dominant_channel": 2
  },
  "6d730ac0": {
    "parent": null,
    "generation": 0,
    "birth_frame": 28,
    "death_frame": 30,
    "lifespan": 2,
    "children": [],
    "peak_mass": 6.9369772636205855,
    "dominant_channel": 2
  },
  "8045ca87": {
    "parent": "514ae701",
    "generation": 4,
    "birth_frame": 29,
    "death_frame": 30,
    "lifespan": 1,
    "children": [],
    "peak_mass": 33.38806518395419,
    "dominant_channel": 2
  },
  "9b7f702c": {
    "parent": "514ae701",
    "generation": 4,
    "birth_frame": 29,
    "death_frame": 30,
    "lifespan": 1,
    "children": [],
    "peak_mass": 23.04084434874454,
    "dominant_channel": 2
  },
  "bfd698a3": {
    "parent": "514ae701",
    "generation": 4,
    "birth_frame": 31,
    "death_frame": 59,
    "lifespan": 28,
    "children": [
      "6f06259f",
      "4d28ee7e"
    ],
    "peak_mass": 35.47443232280389,
    "dominant_channel": 2
  },
  "8fff8d4a": {
    "parent": "514ae701",
    "generation": 4,
    "birth_frame": 31,
    "death_frame": 32,
    "lifespan": 1,
    "children": [
      "14038c60"
    ],
    "peak_mass": 24.806232690401515,
    "dominant_channel": 2
  },
  "60a91586": {
    "parent": "514ae701",
    "generation": 4,
    "birth_frame": 31,
    "death_frame": 32,
    "lifespan": 1,
    "children": [],
    "peak_mass": 20.400588818503316,
    "dominant_channel": 2
  },
  "6f06259f": {
    "parent": "bfd698a3",
    "generation": 5,
    "birth_frame": 32,
    "death_frame": 33,
    "lifespan": 1,
    "children": [],
    "peak_mass": 13.364727533608999,
    "dominant_channel": 2
  },
  "14038c60": {
    "parent": "8fff8d4a",
    "generation": 5,
    "birth_frame": 32,
    "death_frame": 35,
    "lifespan": 3,
    "children": [],
    "peak_mass": 23.620768928083308,
    "dominant_channel": 2
  }
}
```

## Media

- `outputs/SPECIES_027_ZONATA_final.png`
- `outputs/SPECIES_027_ZONATA.gif`
- note: ffmpeg not on PATH; GIF written instead

- genome: `outputs/species/SPECIES_027_ZONATA_genome.json`
