# SPECIES 010 — CILIATA

**Verdict:** VIABLE + REPRODUCING
**Origin:** random  |  **Seed:** 602

## Viability gates

| gate | verdict | value | detail |
| --- | --- | --- | --- |
| mass_conservation | PASS | 2.41908e-16 | tol=0.0001 |
| non_triviality | PASS | 18.3832 | conc>=6.0, occupancy 0.177<=0.45, 3 bodies |
| persistence | PASS | 1 | 1 organisms alive at the end with lifespan >= 15 frames |
| activity | PASS | 6.76931 | mean speed of the most mobile organism, cells/frame |

## Behaviour (anomaly bouncer)

| behaviour | established | score | evidence |
| --- | --- | --- | --- |
| phototaxis | no | 0.010 | lamp(26, 64): 38.4->37.7; lamp(102, 64): 38.4->38.0; lamp(64, 26): 38.5->38.1 | min approach +0.010 (needs > 0.05 for every lamp position) |
| predatory_pursuit | no | 0.173 | d872336c(ch0) -> c7d22493(ch1) closed 55.8 -> 31.6 cells over 16 frames, monotone 0.40, target speed 2.624 |
| cyclic_locomotion | no | 0.327 | uid=c7d22493 circling=0.10 spectral_power=0.11 period=21.0 frames (counted only if >= 4) life=22 frames |

## Reproduction

Measured on the recording run below (the screening run is sampled more coarsely and its counts differ; both are stated separately rather than mixed).

- Divisions counted (offspring survived AND carried at least 10% of the parent's mass): **1**
- Raw fission events before the mass filter: **31** — the difference is debris a large body shed, which is not reproduction
- Surviving offspring total: **1**
- Organisms tracked in this run: **196**
- Screening run, for comparison: 1 divisions of 11 raw fissions, deepest generation 9

| frame | parent | children | parent mass | child masses | child share |
| --- | --- | --- | --- | --- | --- |
| 96 | `5d5bfc61` | `2ed90836` | 20.1 | 6.7 | 33% |

## Complexity

```json
{
  "morph_diversity": 3.1957041147086285,
  "spatial_mi": 1.3870386033513944,
  "cross_channel_mi": 0.5723639376442058,
  "euler_final": 92,
  "concentration_final": 18.38324029377664,
  "occupancy_final": 0.177001953125,
  "n_blobs_final": 3,
  "activity": 6.7693085904096595,
  "mass_drift": 2.4190807558101343e-16,
  "score": 16.099239577291254
}
```

## Lineage tree

```json
{
  "fad74384": {
    "parent": null,
    "generation": 0,
    "birth_frame": 0,
    "death_frame": 15,
    "lifespan": 15,
    "children": [
      "a0d00a5c",
      "94242df3",
      "63afd85e",
      "29c8ca40",
      "167c4a83",
      "f356fbb8",
      "3c42f1d8",
      "2a6bdb15"
    ],
    "peak_mass": 3736.1893623028072,
    "dominant_channel": 1
  },
  "a0d00a5c": {
    "parent": "fad74384",
    "generation": 1,
    "birth_frame": 8,
    "death_frame": 9,
    "lifespan": 1,
    "children": [],
    "peak_mass": 20.27532787529402,
    "dominant_channel": 0
  },
  "94242df3": {
    "parent": "fad74384",
    "generation": 1,
    "birth_frame": 9,
    "death_frame": 11,
    "lifespan": 2,
    "children": [],
    "peak_mass": 28.505076151424745,
    "dominant_channel": 0
  },
  "63afd85e": {
    "parent": "fad74384",
    "generation": 1,
    "birth_frame": 10,
    "death_frame": 11,
    "lifespan": 1,
    "children": [],
    "peak_mass": 6.533502577919756,
    "dominant_channel": 0
  },
  "29c8ca40": {
    "parent": "fad74384",
    "generation": 1,
    "birth_frame": 12,
    "death_frame": 14,
    "lifespan": 2,
    "children": [],
    "peak_mass": 22.906125796596545,
    "dominant_channel": 0
  },
  "167c4a83": {
    "parent": "fad74384",
    "generation": 1,
    "birth_frame": 12,
    "death_frame": 13,
    "lifespan": 1,
    "children": [],
    "peak_mass": 8.11402484136584,
    "dominant_channel": 0
  },
  "f356fbb8": {
    "parent": "fad74384",
    "generation": 1,
    "birth_frame": 12,
    "death_frame": 13,
    "lifespan": 1,
    "children": [],
    "peak_mass": 5.596127137210148,
    "dominant_channel": 0
  },
  "3c42f1d8": {
    "parent": "fad74384",
    "generation": 1,
    "birth_frame": 13,
    "death_frame": 24,
    "lifespan": 11,
    "children": [
      "5446e676",
      "8a3a76fd"
    ],
    "peak_mass": 3624.3293374122986,
    "dominant_channel": 1
  },
  "2a6bdb15": {
    "parent": "fad74384",
    "generation": 1,
    "birth_frame": 13,
    "death_frame": 15,
    "lifespan": 2,
    "children": [],
    "peak_mass": 6.96629157110317,
    "dominant_channel": 0
  },
  "5446e676": {
    "parent": "3c42f1d8",
    "generation": 2,
    "birth_frame": 18,
    "death_frame": 19,
    "lifespan": 1,
    "children": [],
    "peak_mass": 23.14849353200438,
    "dominant_channel": 0
  },
  "8a3a76fd": {
    "parent": "3c42f1d8",
    "generation": 2,
    "birth_frame": 22,
    "death_frame": 30,
    "lifespan": 8,
    "children": [
      "0146528d",
      "44ba9841",
      "3a0bf10b",
      "9a91fe77"
    ],
    "peak_mass": 3592.4542562650013,
    "dominant_channel": 1
  },
  "0146528d": {
    "parent": "8a3a76fd",
    "generation": 3,
    "birth_frame": 25,
    "death_frame": 27,
    "lifespan": 2,
    "children": [],
    "peak_mass": 12.649044530408256,
    "dominant_channel": 0
  },
  "9dd1a663": {
    "parent": null,
    "generation": 0,
    "birth_frame": 26,
    "death_frame": 27,
    "lifespan": 1,
    "children": [],
    "peak_mass": 5.311940031831975,
    "dominant_channel": 0
  },
  "44ba9841": {
    "parent": "8a3a76fd",
    "generation": 3,
    "birth_frame": 27,
    "death_frame": 68,
    "lifespan": 41,
    "children": [],
    "peak_mass": 21.146838394563396,
    "dominant_channel": 0
  },
  "3a0bf10b": {
    "parent": "8a3a76fd",
    "generation": 3,
    "birth_frame": 29,
    "death_frame": 62,
    "lifespan": 33,
    "children": [
      "bd29cfbb",
      "09bb65d7",
      "10f35ff5",
      "31062fd2",
      "5a05657c",
      "c110313c",
      "98569cb2",
      "65af57f4",
      "025d917d",
      "5f8e0eb9",
      "e4a43d74",
      "cdb46369",
      "43a87e93",
      "8bb95e54",
      "655205a2",
      "45b983f7",
      "bcec0243",
      "1e947201",
      "efd567a0",
      "47773217",
      "5b1a2041",
      "897d952b",
      "348adcf3",
      "93306d02",
      "1543440f",
      "24fbc919",
      "9a4883bb",
      "658e12e7",
      "ff5e2c3a"
    ],
    "peak_mass": 3451.9826440958454,
    "dominant_channel": 1
  },
  "9a91fe77": {
    "parent": "8a3a76fd",
    "generation": 3,
    "birth_frame": 29,
    "death_frame": 30,
    "lifespan": 1,
    "children": [],
    "peak_mass": 8.970087945597847,
    "dominant_channel": 0
  },
  "bd29cfbb": {
    "parent": "3a0bf10b",
    "generation": 4,
    "birth_frame": 31,
    "death_frame": 32,
    "lifespan": 1,
    "children": [],
    "peak_mass": 22.37030928950178,
    "dominant_channel": 0
  },
  "09bb65d7": {
    "parent": "3a0bf10b",
    "generation": 4,
    "birth_frame": 31,
    "death_frame": 32,
    "lifespan": 1,
    "children": [],
    "peak_mass": 18.0720925993144,
    "dominant_channel": 0
  },
  "10f35ff5": {
    "parent": "3a0bf10b",
    "generation": 4,
    "birth_frame": 31,
    "death_frame": 32,
    "lifespan": 1,
    "children": [],
    "peak_mass": 11.21723421087911,
    "dominant_channel": 0
  },
  "31062fd2": {
    "parent": "3a0bf10b",
    "generation": 4,
    "birth_frame": 31,
    "death_frame": 39,
    "lifespan": 8,
    "children": [],
    "peak_mass": 28.874116049260355,
    "dominant_channel": 0
  },
  "5a05657c": {
    "parent": "3a0bf10b",
    "generation": 4,
    "birth_frame": 33,
    "death_frame": 34,
    "lifespan": 1,
    "children": [],
    "peak_mass": 8.117709842517462,
    "dominant_channel": 0
  },
  "c110313c": {
    "parent": "3a0bf10b",
    "generation": 4,
    "birth_frame": 34,
    "death_frame": 35,
    "lifespan": 1,
    "children": [],
    "peak_mass": 22.35312392333461,
    "dominant_channel": 0
  },
  "98569cb2": {
    "parent": "3a0bf10b",
    "generation": 4,
    "birth_frame": 34,
    "death_frame": 81,
    "lifespan": 47,
    "children": [],
    "peak_mass": 22.135942822302216,
    "dominant_channel": 0
  },
  "65af57f4": {
    "parent": "3a0bf10b",
    "generation": 4,
    "birth_frame": 35,
    "death_frame": 38,
    "lifespan": 3,
    "children": [],
    "peak_mass": 12.395385643200232,
    "dominant_channel": 0
  },
  "025d917d": {
    "parent": "3a0bf10b",
    "generation": 4,
    "birth_frame": 36,
    "death_frame": 37,
    "lifespan": 1,
    "children": [],
    "peak_mass": 56.79884950155544,
    "dominant_channel": 0
  },
  "5f8e0eb9": {
    "parent": "3a0bf10b",
    "generation": 4,
    "birth_frame": 36,
    "death_frame": 103,
    "lifespan": 67,
    "children": [
      "594fc73e",
      "ddd7c9ed"
    ],
    "peak_mass": 39.928749254048455,
    "dominant_channel": 0
  },
  "8151964b": {
    "parent": null,
    "generation": 0,
    "birth_frame": 37,
    "death_frame": 41,
    "lifespan": 4,
    "children": [],
    "peak_mass": 7.749327863207109,
    "dominant_channel": 0
  },
  "e4a43d74": {
    "parent": "3a0bf10b",
    "generation": 4,
    "birth_frame": 40,
    "death_frame": 42,
    "lifespan": 2,
    "children": [],
    "peak_mass": 29.45749168947834,
    "dominant_channel": 0
  },
  "cdb46369": {
    "parent": "3a0bf10b",
    "generation": 4,
    "birth_frame": 40,
    "death_frame": 49,
    "lifespan": 9,
    "children": [],
    "peak_mass": 12.762137035352698,
    "dominant_channel": 0
  },
  "fed5bc9a": {
    "parent": null,
    "generation": 0,
    "birth_frame": 42,
    "death_frame": 47,
    "lifespan": 5,
    "children": [],
    "peak_mass": 8.041492518707672,
    "dominant_channel": 0
  },
  "43a87e93": {
    "parent": "3a0bf10b",
    "generation": 4,
    "birth_frame": 43,
    "death_frame": 51,
    "lifespan": 8,
    "children": [
      "4453599a",
      "86ed5461"
    ],
    "peak_mass": 45.11128506699856,
    "dominant_channel": 0
  },
  "8bb95e54": {
    "parent": "3a0bf10b",
    "generation": 4,
    "birth_frame": 46,
    "death_frame": 70,
    "lifespan": 24,
    "children": [
      "d786b04e",
      "0798ef38",
      "3de4716b",
      "55d64bb1",
      "52e2c27f",
      "4f4654de",
      "a22d061f",
      "4f542e3b",
      "756416ff",
      "3c72804d",
      "755a2525",
      "d0966fb5",
      "b72aaff8",
      "38fd8248"
    ],
    "peak_mass": 3234.452815167545,
    "dominant_channel": 1
  },
  "655205a2": {
    "parent": "3a0bf10b",
    "generation": 4,
    "birth_frame": 48,
    "death_frame": 49,
    "lifespan": 1,
    "children": [],
    "peak_mass": 78.9669577321559,
    "dominant_channel": 0
  },
  "45b983f7": {
    "parent": "3a0bf10b",
    "generation": 4,
    "birth_frame": 48,
    "death_frame": 51,
    "lifespan": 3,
    "children": [],
    "peak_mass": 61.16960525702975,
    "dominant_channel": 0
  },
  "bcec0243": {
    "parent": "3a0bf10b",
    "generation": 4,
    "birth_frame": 49,
    "death_frame": 55,
    "lifespan": 6,
    "children": [],
    "peak_mass": 57.94963986670231,
    "dominant_channel": 0
  },
  "4453599a": {
    "parent": "43a87e93",
    "generation": 5,
    "birth_frame": 49,
    "death_frame": 51,
    "lifespan": 2,
    "children": [],
    "peak_mass": 11.929339557968827,
    "dominant_channel": 0
  },
  "594fc73e": {
    "parent": "5f8e0eb9",
    "generation": 5,
    "birth_frame": 50,
    "death_frame": 51,
    "lifespan": 1,
    "children": [],
    "peak_mass": 8.158642009131126,
    "dominant_channel": 0
  },
  "86ed5461": {
    "parent": "43a87e93",
    "generation": 5,
    "birth_frame": 50,
    "death_frame": 52,
    "lifespan": 2,
    "children": [],
    "peak_mass": 8.064866295587317,
    "dominant_channel": 0
  },
  "3a150e27": {
    "parent": null,
    "generation": 0,
    "birth_frame": 50,
    "death_frame": 51,
    "lifespan": 1,
    "children": [],
    "peak_mass": 8.106053810808381,
    "dominant_channel": 0
  },
  "1e947201": {
    "parent": "3a0bf10b",
    "generation": 4,
    "birth_frame": 51,
    "death_frame": 52,
    "lifespan": 1,
    "children": [],
    "peak_mass": 76.3962667891741,
    "dominant_channel": 0
  }
}
```

## Media

- `outputs/SPECIES_010_CILIATA_final.png`
- `outputs/SPECIES_010_CILIATA.gif`
- `outputs/SPECIES_010_CILIATA.mp4`

- genome: `outputs/species/SPECIES_010_CILIATA_genome.json`
