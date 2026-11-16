# SPECIES 018 — PULSARA

**Verdict:** VIABLE + REPRODUCING
**Origin:** random  |  **Seed:** 776

## Viability gates

| gate | verdict | value | detail |
| --- | --- | --- | --- |
| mass_conservation | PASS | 1.54711e-16 | tol=0.0001 |
| non_triviality | PASS | 12.0229 | conc>=6.0, occupancy 0.276<=0.45, 1 bodies |
| persistence | PASS | 1 | 1 organisms alive at the end with lifespan >= 15 frames |
| activity | PASS | 3.03658 | mean speed of the most mobile organism, cells/frame |

## Behaviour (anomaly bouncer)

| behaviour | established | score | evidence |
| --- | --- | --- | --- |
| phototaxis | no | -0.009 | lamp(26, 64): 38.3->38.7; lamp(102, 64): 38.5->38.7; lamp(64, 26): 38.4->38.6 | min approach -0.009 (needs > 0.05 for every lamp position) |
| predatory_pursuit | no | 0.175 | 03581381(ch2) -> a5a9839f(ch2) closed 47.6 -> 28.8 cells over 19 frames, monotone 0.44, target speed 0.289 |
| cyclic_locomotion | no | 0.548 | uid=d377a5d0 circling=0.16 spectral_power=0.18 period=6.7 frames (counted only if >= 4) life=21 frames |

## Reproduction

Measured on the recording run below (the screening run is sampled more coarsely and its counts differ; both are stated separately rather than mixed).

- Divisions counted (offspring survived AND carried at least 10% of the parent's mass): **2**
- Raw fission events before the mass filter: **11** — the difference is debris a large body shed, which is not reproduction
- Surviving offspring total: **2**
- Organisms tracked in this run: **42**
- Screening run, for comparison: 1 divisions of 5 raw fissions, deepest generation 2

| frame | parent | children | parent mass | child masses | child share |
| --- | --- | --- | --- | --- | --- |
| 65 | `03581381` | `83a1acb4` | 3.7 | 2.4 | 66% |
| 72 | `03581381` | `946ad33a` | 1.8 | 1.5 | 82% |

## Complexity

```json
{
  "morph_diversity": 1.677576807064229,
  "spatial_mi": 1.525281191506684,
  "cross_channel_mi": 0.5641009324721222,
  "euler_final": -12,
  "concentration_final": 12.022874645851482,
  "occupancy_final": 0.27593994140625,
  "n_blobs_final": 1,
  "activity": 3.0365790364191696,
  "mass_drift": 1.5471139298114594e-16,
  "score": 15.242648403816586
}
```

## Lineage tree

```json
{
  "f0255b4b": {
    "parent": null,
    "generation": 0,
    "birth_frame": 0,
    "death_frame": 74,
    "lifespan": 74,
    "children": [
      "5c5772e8",
      "a089b3dc",
      "73a354cb",
      "2f5215bb",
      "bf9b1bed",
      "b1d8759c",
      "0551605d",
      "b6cce854",
      "afc8f225",
      "e4506684"
    ],
    "peak_mass": 1454.6577981179803,
    "dominant_channel": 2
  },
  "5c5772e8": {
    "parent": "f0255b4b",
    "generation": 1,
    "birth_frame": 40,
    "death_frame": 41,
    "lifespan": 1,
    "children": [],
    "peak_mass": 1.2031535722668436,
    "dominant_channel": 2
  },
  "a089b3dc": {
    "parent": "f0255b4b",
    "generation": 1,
    "birth_frame": 42,
    "death_frame": 43,
    "lifespan": 1,
    "children": [],
    "peak_mass": 1.6265738768329063,
    "dominant_channel": 2
  },
  "73a354cb": {
    "parent": "f0255b4b",
    "generation": 1,
    "birth_frame": 42,
    "death_frame": 43,
    "lifespan": 1,
    "children": [],
    "peak_mass": 1.297929025448958,
    "dominant_channel": 2
  },
  "2f5215bb": {
    "parent": "f0255b4b",
    "generation": 1,
    "birth_frame": 44,
    "death_frame": 45,
    "lifespan": 1,
    "children": [],
    "peak_mass": 1.1938688452028998,
    "dominant_channel": 2
  },
  "1dfe428b": {
    "parent": null,
    "generation": 0,
    "birth_frame": 47,
    "death_frame": 53,
    "lifespan": 6,
    "children": [],
    "peak_mass": 2.369611165649178,
    "dominant_channel": 2
  },
  "8fdee0ae": {
    "parent": null,
    "generation": 0,
    "birth_frame": 47,
    "death_frame": 63,
    "lifespan": 16,
    "children": [
      "8aadc31e"
    ],
    "peak_mass": 3.680892274787097,
    "dominant_channel": 2
  },
  "b04293c0": {
    "parent": null,
    "generation": 0,
    "birth_frame": 47,
    "death_frame": 48,
    "lifespan": 1,
    "children": [],
    "peak_mass": 1.4187565641564113,
    "dominant_channel": 2
  },
  "5e9824bc": {
    "parent": null,
    "generation": 0,
    "birth_frame": 47,
    "death_frame": 48,
    "lifespan": 1,
    "children": [],
    "peak_mass": 2.223692194997802,
    "dominant_channel": 2
  },
  "76e0cd73": {
    "parent": null,
    "generation": 0,
    "birth_frame": 47,
    "death_frame": 51,
    "lifespan": 4,
    "children": [],
    "peak_mass": 1.4762703549689915,
    "dominant_channel": 2
  },
  "0acc3c6e": {
    "parent": null,
    "generation": 0,
    "birth_frame": 48,
    "death_frame": 50,
    "lifespan": 2,
    "children": [],
    "peak_mass": 1.2925055512194794,
    "dominant_channel": 2
  },
  "bf9b1bed": {
    "parent": "f0255b4b",
    "generation": 1,
    "birth_frame": 49,
    "death_frame": 64,
    "lifespan": 15,
    "children": [],
    "peak_mass": 2.8328376351193163,
    "dominant_channel": 2
  },
  "b1d8759c": {
    "parent": "f0255b4b",
    "generation": 1,
    "birth_frame": 53,
    "death_frame": 55,
    "lifespan": 2,
    "children": [],
    "peak_mass": 1.6889581434241452,
    "dominant_channel": 2
  },
  "03581381": {
    "parent": null,
    "generation": 0,
    "birth_frame": 54,
    "death_frame": 82,
    "lifespan": 28,
    "children": [
      "83a1acb4",
      "946ad33a"
    ],
    "peak_mass": 6.437740308261203,
    "dominant_channel": 2
  },
  "ec8fae21": {
    "parent": null,
    "generation": 0,
    "birth_frame": 55,
    "death_frame": 56,
    "lifespan": 1,
    "children": [],
    "peak_mass": 1.1079385567912023,
    "dominant_channel": 2
  },
  "a5a9839f": {
    "parent": null,
    "generation": 0,
    "birth_frame": 55,
    "death_frame": 74,
    "lifespan": 19,
    "children": [
      "6ec676fc"
    ],
    "peak_mass": 2.1243272341771333,
    "dominant_channel": 2
  },
  "0551605d": {
    "parent": "f0255b4b",
    "generation": 1,
    "birth_frame": 58,
    "death_frame": 65,
    "lifespan": 7,
    "children": [],
    "peak_mass": 2.9073554297434336,
    "dominant_channel": 2
  },
  "ea2ced56": {
    "parent": null,
    "generation": 0,
    "birth_frame": 60,
    "death_frame": 62,
    "lifespan": 2,
    "children": [],
    "peak_mass": 1.6028126079648186,
    "dominant_channel": 2
  },
  "eb4db618": {
    "parent": null,
    "generation": 0,
    "birth_frame": 61,
    "death_frame": 62,
    "lifespan": 1,
    "children": [],
    "peak_mass": 0.9951656708404129,
    "dominant_channel": 2
  },
  "8aadc31e": {
    "parent": "8fdee0ae",
    "generation": 1,
    "birth_frame": 62,
    "death_frame": 64,
    "lifespan": 2,
    "children": [],
    "peak_mass": 4.0287250387640485,
    "dominant_channel": 2
  },
  "d1df7c2a": {
    "parent": null,
    "generation": 0,
    "birth_frame": 63,
    "death_frame": 76,
    "lifespan": 13,
    "children": [],
    "peak_mass": 2.641196621952758,
    "dominant_channel": 2
  },
  "978b3817": {
    "parent": null,
    "generation": 0,
    "birth_frame": 63,
    "death_frame": 66,
    "lifespan": 3,
    "children": [],
    "peak_mass": 1.349500697905157,
    "dominant_channel": 2
  },
  "cdb8c607": {
    "parent": null,
    "generation": 0,
    "birth_frame": 64,
    "death_frame": 65,
    "lifespan": 1,
    "children": [],
    "peak_mass": 1.0229543878292437,
    "dominant_channel": 2
  },
  "b6cce854": {
    "parent": "f0255b4b",
    "generation": 1,
    "birth_frame": 65,
    "death_frame": 88,
    "lifespan": 23,
    "children": [],
    "peak_mass": 3.1115072614885,
    "dominant_channel": 2
  },
  "afc8f225": {
    "parent": "f0255b4b",
    "generation": 1,
    "birth_frame": 65,
    "death_frame": 91,
    "lifespan": 26,
    "children": [
      "4ebad85d",
      "14bdc62c"
    ],
    "peak_mass": 1391.0486657724573,
    "dominant_channel": 1
  },
  "83a1acb4": {
    "parent": "03581381",
    "generation": 1,
    "birth_frame": 65,
    "death_frame": 86,
    "lifespan": 21,
    "children": [],
    "peak_mass": 2.4332919028085236,
    "dominant_channel": 2
  },
  "e4506684": {
    "parent": "f0255b4b",
    "generation": 1,
    "birth_frame": 66,
    "death_frame": 72,
    "lifespan": 6,
    "children": [],
    "peak_mass": 3.293937556913989,
    "dominant_channel": 2
  },
  "a93e9a17": {
    "parent": null,
    "generation": 0,
    "birth_frame": 68,
    "death_frame": 71,
    "lifespan": 3,
    "children": [],
    "peak_mass": 1.165380987451812,
    "dominant_channel": 2
  },
  "946ad33a": {
    "parent": "03581381",
    "generation": 1,
    "birth_frame": 72,
    "death_frame": 81,
    "lifespan": 9,
    "children": [],
    "peak_mass": 1.516064785022997,
    "dominant_channel": 2
  },
  "6ec676fc": {
    "parent": "a5a9839f",
    "generation": 1,
    "birth_frame": 74,
    "death_frame": 77,
    "lifespan": 3,
    "children": [],
    "peak_mass": 1.6096058715783237,
    "dominant_channel": 2
  },
  "6b7484ee": {
    "parent": null,
    "generation": 0,
    "birth_frame": 78,
    "death_frame": 79,
    "lifespan": 1,
    "children": [],
    "peak_mass": 1.0293441305657338,
    "dominant_channel": 2
  },
  "4ebad85d": {
    "parent": "afc8f225",
    "generation": 2,
    "birth_frame": 83,
    "death_frame": null,
    "lifespan": 68,
    "children": [
      "fdfe3dae",
      "5ef083b1",
      "d377a5d0",
      "b63dc08e",
      "1014bff0"
    ],
    "peak_mass": 1380.7661031963053,
    "dominant_channel": 1
  },
  "14bdc62c": {
    "parent": "afc8f225",
    "generation": 2,
    "birth_frame": 88,
    "death_frame": 89,
    "lifespan": 1,
    "children": [],
    "peak_mass": 1.5118772186682052,
    "dominant_channel": 2
  },
  "5eb84017": {
    "parent": null,
    "generation": 0,
    "birth_frame": 89,
    "death_frame": 92,
    "lifespan": 3,
    "children": [],
    "peak_mass": 1.464154024759684,
    "dominant_channel": 2
  },
  "43b82017": {
    "parent": null,
    "generation": 0,
    "birth_frame": 93,
    "death_frame": 96,
    "lifespan": 3,
    "children": [],
    "peak_mass": 1.4216906478228077,
    "dominant_channel": 2
  },
  "fdfe3dae": {
    "parent": "4ebad85d",
    "generation": 3,
    "birth_frame": 125,
    "death_frame": 145,
    "lifespan": 20,
    "children": [],
    "peak_mass": 1.7811170694992111,
    "dominant_channel": 2
  },
  "5ef083b1": {
    "parent": "4ebad85d",
    "generation": 3,
    "birth_frame": 128,
    "death_frame": null,
    "lifespan": 23,
    "children": [],
    "peak_mass": 2.431893876547492,
    "dominant_channel": 2
  },
  "d377a5d0": {
    "parent": "4ebad85d",
    "generation": 3,
    "birth_frame": 130,
    "death_frame": null,
    "lifespan": 21,
    "children": [],
    "peak_mass": 3.9190800058615602,
    "dominant_channel": 2
  },
  "b63dc08e": {
    "parent": "4ebad85d",
    "generation": 3,
    "birth_frame": 141,
    "death_frame": null,
    "lifespan": 10,
    "children": [],
    "peak_mass": 2.442961530316543,
    "dominant_channel": 2
  },
  "262fc9b0": {
    "parent": null,
    "generation": 0,
    "birth_frame": 142,
    "death_frame": 143,
    "lifespan": 1,
    "children": [],
    "peak_mass": 1.3059252714986531,
    "dominant_channel": 2
  }
}
```

## Media

- `outputs/SPECIES_018_PULSARA_final.png`
- `outputs/SPECIES_018_PULSARA.gif`
- `outputs/SPECIES_018_PULSARA.mp4`

- genome: `outputs/species/SPECIES_018_PULSARA_genome.json`
