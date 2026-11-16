# SPECIES 020 — RADIATA

**Verdict:** VIABLE + REPRODUCING
**Origin:** random  |  **Seed:** 787

## Viability gates

| gate | verdict | value | detail |
| --- | --- | --- | --- |
| mass_conservation | PASS | 1.80642e-16 | tol=0.0001 |
| non_triviality | PASS | 24.6504 | conc>=6.0, occupancy 0.164<=0.45, 2 bodies |
| persistence | PASS | 1 | 1 organisms alive at the end with lifespan >= 15 frames |
| activity | PASS | 8.95003 | mean speed of the most mobile organism, cells/frame |

## Behaviour (anomaly bouncer)

| behaviour | established | score | evidence |
| --- | --- | --- | --- |
| phototaxis | no | -0.005 | lamp(26, 64): 38.5->38.1; lamp(102, 64): 38.3->38.0; lamp(64, 26): 38.4->38.6 | min approach -0.005 (needs > 0.05 for every lamp position) |
| predatory_pursuit | no | 0.189 | ccb59c30(ch2) -> 2b0d8da6(ch1) closed 68.8 -> 40.2 cells over 23 frames, monotone 0.45, target speed 2.660 |
| cyclic_locomotion | no | 0.312 | uid=07398ad7 circling=0.18 spectral_power=0.10 period=4.6 frames (counted only if >= 4) life=24 frames |

## Reproduction

Measured on the recording run below (the screening run is sampled more coarsely and its counts differ; both are stated separately rather than mixed).

- Divisions counted (offspring survived AND carried at least 10% of the parent's mass): **5**
- Raw fission events before the mass filter: **14** — the difference is debris a large body shed, which is not reproduction
- Surviving offspring total: **5**
- Organisms tracked in this run: **167**
- Screening run, for comparison: 3 divisions of 9 raw fissions, deepest generation 8

| frame | parent | children | parent mass | child masses | child share |
| --- | --- | --- | --- | --- | --- |
| 68 | `7520c042` | `ab99ea43` | 6.6 | 5.5 | 83% |
| 71 | `ab99ea43` | `868398ca` | 4.8 | 3.4 | 72% |
| 81 | `6617f876` | `9a37b89c` | 12.5 | 6.7 | 53% |
| 86 | `51f7fd6a` | `2b0d8da6` | 8.7 | 6.9 | 80% |
| 91 | `e48121f0` | `004c0d8f` | 12.5 | 7.3 | 58% |

## Complexity

```json
{
  "morph_diversity": 2.9835218328687794,
  "spatial_mi": 1.4350407510751615,
  "cross_channel_mi": 0.8706057380384942,
  "euler_final": 16,
  "concentration_final": 24.650398764435746,
  "occupancy_final": 0.16412353515625,
  "n_blobs_final": 2,
  "activity": 8.950029837986447,
  "mass_drift": 1.806418001592212e-16,
  "score": 32.709745217473355
}
```

## Lineage tree

```json
{
  "5c4f3cba": {
    "parent": null,
    "generation": 0,
    "birth_frame": 0,
    "death_frame": 48,
    "lifespan": 48,
    "children": [
      "a225010c",
      "c9755ecb",
      "69cf116e",
      "df9099cf"
    ],
    "peak_mass": 2502.4262973493624,
    "dominant_channel": 1
  },
  "a225010c": {
    "parent": "5c4f3cba",
    "generation": 1,
    "birth_frame": 38,
    "death_frame": 40,
    "lifespan": 2,
    "children": [],
    "peak_mass": 3.6127020225497763,
    "dominant_channel": 2
  },
  "c9755ecb": {
    "parent": "5c4f3cba",
    "generation": 1,
    "birth_frame": 41,
    "death_frame": 42,
    "lifespan": 1,
    "children": [],
    "peak_mass": 6.323457781724873,
    "dominant_channel": 2
  },
  "280fe5fe": {
    "parent": null,
    "generation": 0,
    "birth_frame": 43,
    "death_frame": 44,
    "lifespan": 1,
    "children": [],
    "peak_mass": 2.332676625197506,
    "dominant_channel": 2
  },
  "69cf116e": {
    "parent": "5c4f3cba",
    "generation": 1,
    "birth_frame": 44,
    "death_frame": 45,
    "lifespan": 1,
    "children": [],
    "peak_mass": 5.304962500287731,
    "dominant_channel": 2
  },
  "df9099cf": {
    "parent": "5c4f3cba",
    "generation": 1,
    "birth_frame": 46,
    "death_frame": 55,
    "lifespan": 9,
    "children": [
      "ff07f5e2",
      "ce2d2939",
      "c039cacc"
    ],
    "peak_mass": 2387.994572077361,
    "dominant_channel": 1
  },
  "5c303e75": {
    "parent": null,
    "generation": 0,
    "birth_frame": 47,
    "death_frame": 49,
    "lifespan": 2,
    "children": [],
    "peak_mass": 5.650393928703453,
    "dominant_channel": 2
  },
  "90a8af74": {
    "parent": null,
    "generation": 0,
    "birth_frame": 48,
    "death_frame": 52,
    "lifespan": 4,
    "children": [],
    "peak_mass": 3.050456135683629,
    "dominant_channel": 2
  },
  "cdd414d8": {
    "parent": null,
    "generation": 0,
    "birth_frame": 49,
    "death_frame": 50,
    "lifespan": 1,
    "children": [],
    "peak_mass": 2.4204740121170887,
    "dominant_channel": 2
  },
  "ff07f5e2": {
    "parent": "df9099cf",
    "generation": 2,
    "birth_frame": 50,
    "death_frame": 51,
    "lifespan": 1,
    "children": [],
    "peak_mass": 4.20427044800279,
    "dominant_channel": 2
  },
  "27112ebf": {
    "parent": null,
    "generation": 0,
    "birth_frame": 51,
    "death_frame": 56,
    "lifespan": 5,
    "children": [],
    "peak_mass": 7.475915390034279,
    "dominant_channel": 2
  },
  "ce2d2939": {
    "parent": "df9099cf",
    "generation": 2,
    "birth_frame": 52,
    "death_frame": 65,
    "lifespan": 13,
    "children": [
      "192a83f2",
      "72da03c8",
      "17b5334d",
      "58187fb5",
      "5beac7b1",
      "6e902331"
    ],
    "peak_mass": 2399.4545096130933,
    "dominant_channel": 1
  },
  "c039cacc": {
    "parent": "df9099cf",
    "generation": 2,
    "birth_frame": 52,
    "death_frame": 61,
    "lifespan": 9,
    "children": [],
    "peak_mass": 8.377772507329585,
    "dominant_channel": 2
  },
  "06d5d75f": {
    "parent": null,
    "generation": 0,
    "birth_frame": 55,
    "death_frame": 64,
    "lifespan": 9,
    "children": [],
    "peak_mass": 4.736854103294061,
    "dominant_channel": 2
  },
  "ccb59c30": {
    "parent": null,
    "generation": 0,
    "birth_frame": 56,
    "death_frame": 109,
    "lifespan": 53,
    "children": [],
    "peak_mass": 10.427398582416428,
    "dominant_channel": 2
  },
  "192a83f2": {
    "parent": "ce2d2939",
    "generation": 3,
    "birth_frame": 57,
    "death_frame": 59,
    "lifespan": 2,
    "children": [],
    "peak_mass": 4.291425462741772,
    "dominant_channel": 2
  },
  "72da03c8": {
    "parent": "ce2d2939",
    "generation": 3,
    "birth_frame": 58,
    "death_frame": 60,
    "lifespan": 2,
    "children": [],
    "peak_mass": 9.331972448205763,
    "dominant_channel": 2
  },
  "17b5334d": {
    "parent": "ce2d2939",
    "generation": 3,
    "birth_frame": 58,
    "death_frame": 60,
    "lifespan": 2,
    "children": [],
    "peak_mass": 6.4025601369244844,
    "dominant_channel": 2
  },
  "58187fb5": {
    "parent": "ce2d2939",
    "generation": 3,
    "birth_frame": 62,
    "death_frame": 77,
    "lifespan": 15,
    "children": [
      "ee16a238",
      "82c9429f"
    ],
    "peak_mass": 23.692507643168657,
    "dominant_channel": 2
  },
  "5beac7b1": {
    "parent": "ce2d2939",
    "generation": 3,
    "birth_frame": 63,
    "death_frame": 67,
    "lifespan": 4,
    "children": [
      "3f882330",
      "07398ad7",
      "3d1be5f7",
      "7520c042"
    ],
    "peak_mass": 2350.8564877168765,
    "dominant_channel": 1
  },
  "6e902331": {
    "parent": "ce2d2939",
    "generation": 3,
    "birth_frame": 63,
    "death_frame": 78,
    "lifespan": 15,
    "children": [
      "34fada35"
    ],
    "peak_mass": 17.220608379790253,
    "dominant_channel": 2
  },
  "3f882330": {
    "parent": "5beac7b1",
    "generation": 4,
    "birth_frame": 64,
    "death_frame": 65,
    "lifespan": 1,
    "children": [],
    "peak_mass": 5.113348954624977,
    "dominant_channel": 2
  },
  "11d27d26": {
    "parent": null,
    "generation": 0,
    "birth_frame": 65,
    "death_frame": 68,
    "lifespan": 3,
    "children": [],
    "peak_mass": 4.376872134588144,
    "dominant_channel": 2
  },
  "07398ad7": {
    "parent": "5beac7b1",
    "generation": 4,
    "birth_frame": 66,
    "death_frame": 90,
    "lifespan": 24,
    "children": [
      "fa3a4950",
      "6617f876",
      "51f7fd6a",
      "f1f048e8",
      "3d984a39",
      "ac5d47d2",
      "56a2ce45",
      "7979d5e1",
      "4643b61b"
    ],
    "peak_mass": 2365.829238926546,
    "dominant_channel": 1
  },
  "3d1be5f7": {
    "parent": "5beac7b1",
    "generation": 4,
    "birth_frame": 66,
    "death_frame": 70,
    "lifespan": 4,
    "children": [
      "2ee53068",
      "6a736dfd"
    ],
    "peak_mass": 2278.203291149413,
    "dominant_channel": 1
  },
  "7520c042": {
    "parent": "5beac7b1",
    "generation": 4,
    "birth_frame": 67,
    "death_frame": 70,
    "lifespan": 3,
    "children": [
      "ab99ea43"
    ],
    "peak_mass": 14.300226640215232,
    "dominant_channel": 2
  },
  "2ee53068": {
    "parent": "3d1be5f7",
    "generation": 5,
    "birth_frame": 68,
    "death_frame": 70,
    "lifespan": 2,
    "children": [],
    "peak_mass": 11.084282133795394,
    "dominant_channel": 2
  },
  "6a736dfd": {
    "parent": "3d1be5f7",
    "generation": 5,
    "birth_frame": 68,
    "death_frame": 73,
    "lifespan": 5,
    "children": [
      "9125daa4",
      "11fd94c5"
    ],
    "peak_mass": 2273.4459756821807,
    "dominant_channel": 1
  },
  "ab99ea43": {
    "parent": "7520c042",
    "generation": 5,
    "birth_frame": 68,
    "death_frame": 78,
    "lifespan": 10,
    "children": [
      "868398ca"
    ],
    "peak_mass": 14.56601834126821,
    "dominant_channel": 2
  },
  "30762358": {
    "parent": null,
    "generation": 0,
    "birth_frame": 70,
    "death_frame": 71,
    "lifespan": 1,
    "children": [],
    "peak_mass": 4.717047769727749,
    "dominant_channel": 2
  },
  "fa3a4950": {
    "parent": "07398ad7",
    "generation": 5,
    "birth_frame": 71,
    "death_frame": 73,
    "lifespan": 2,
    "children": [],
    "peak_mass": 10.240207191738344,
    "dominant_channel": 2
  },
  "9125daa4": {
    "parent": "6a736dfd",
    "generation": 6,
    "birth_frame": 71,
    "death_frame": 75,
    "lifespan": 4,
    "children": [],
    "peak_mass": 12.487533534583882,
    "dominant_channel": 2
  },
  "11fd94c5": {
    "parent": "6a736dfd",
    "generation": 6,
    "birth_frame": 71,
    "death_frame": 78,
    "lifespan": 7,
    "children": [
      "daa76313"
    ],
    "peak_mass": 2243.5610440719374,
    "dominant_channel": 1
  },
  "868398ca": {
    "parent": "ab99ea43",
    "generation": 6,
    "birth_frame": 71,
    "death_frame": 78,
    "lifespan": 7,
    "children": [],
    "peak_mass": 6.4941433246564,
    "dominant_channel": 2
  },
  "66648a0b": {
    "parent": null,
    "generation": 0,
    "birth_frame": 74,
    "death_frame": 75,
    "lifespan": 1,
    "children": [],
    "peak_mass": 3.6612544420291657,
    "dominant_channel": 2
  },
  "3bbf9eb5": {
    "parent": null,
    "generation": 0,
    "birth_frame": 74,
    "death_frame": 75,
    "lifespan": 1,
    "children": [],
    "peak_mass": 4.617014430493277,
    "dominant_channel": 2
  },
  "daa76313": {
    "parent": "11fd94c5",
    "generation": 7,
    "birth_frame": 76,
    "death_frame": 78,
    "lifespan": 2,
    "children": [],
    "peak_mass": 4.252982872649176,
    "dominant_channel": 0
  },
  "ee16a238": {
    "parent": "58187fb5",
    "generation": 4,
    "birth_frame": 76,
    "death_frame": 78,
    "lifespan": 2,
    "children": [],
    "peak_mass": 21.31293925202719,
    "dominant_channel": 2
  },
  "82c9429f": {
    "parent": "58187fb5",
    "generation": 4,
    "birth_frame": 76,
    "death_frame": 77,
    "lifespan": 1,
    "children": [],
    "peak_mass": 4.728868441700301,
    "dominant_channel": 2
  },
  "34fada35": {
    "parent": "6e902331",
    "generation": 4,
    "birth_frame": 76,
    "death_frame": 78,
    "lifespan": 2,
    "children": [],
    "peak_mass": 5.830031114834674,
    "dominant_channel": 2
  }
}
```

## Media

- `outputs/SPECIES_020_RADIATA_final.png`
- `outputs/SPECIES_020_RADIATA.gif`
- `outputs/SPECIES_020_RADIATA.mp4`

- genome: `outputs/species/SPECIES_020_RADIATA_genome.json`
