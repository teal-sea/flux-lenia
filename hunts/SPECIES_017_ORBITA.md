# SPECIES 017 — ORBITA

**Verdict:** VIABLE + REPRODUCING
**Origin:** random  |  **Seed:** 739

## Viability gates

| gate | verdict | value | detail |
| --- | --- | --- | --- |
| mass_conservation | PASS | 4.12545e-16 | tol=0.0001 |
| non_triviality | PASS | 35.0463 | conc>=6.0, occupancy 0.111<=0.45, 5 bodies |
| persistence | PASS | 2 | 2 organisms alive at the end with lifespan >= 15 frames |
| activity | PASS | 3.13403 | mean speed of the most mobile organism, cells/frame |

## Behaviour (anomaly bouncer)

| behaviour | established | score | evidence |
| --- | --- | --- | --- |
| phototaxis | no | -0.008 | lamp(26, 64): 38.3->38.5; lamp(102, 64): 38.5->38.3; lamp(64, 26): 38.5->38.8 | min approach -0.008 (needs > 0.05 for every lamp position) |
| predatory_pursuit | no | 0.042 | 2184ff76(ch2) -> 40d46ffa(ch2) closed 36.9 -> 34.8 cells over 23 frames, monotone 0.73, target speed 0.340 |
| cyclic_locomotion | no | 0.333 | uid=40d46ffa circling=0.33 spectral_power=0.14 period=3.1 frames (counted only if >= 4) life=23 frames |

## Reproduction

Measured on the recording run below (the screening run is sampled more coarsely and its counts differ; both are stated separately rather than mixed).

- Divisions counted (offspring survived AND carried at least 10% of the parent's mass): **4**
- Raw fission events before the mass filter: **9** — the difference is debris a large body shed, which is not reproduction
- Surviving offspring total: **4**
- Organisms tracked in this run: **63**
- Screening run, for comparison: 3 divisions of 4 raw fissions, deepest generation 2

| frame | parent | children | parent mass | child masses | child share |
| --- | --- | --- | --- | --- | --- |
| 100 | `f109d8c8` | `d6513f18` | 2.4 | 2.1 | 88% |
| 105 | `5e115299` | `2184ff76` | 5.2 | 3.9 | 76% |
| 116 | `a394cff9` | `0f3f2674` | 3.5 | 1.7 | 49% |
| 128 | `987d0d85` | `40d46ffa` | 4.6 | 3.4 | 73% |

## Complexity

```json
{
  "morph_diversity": 3.125164712332134,
  "spatial_mi": 1.6082406456551606,
  "cross_channel_mi": 1.3239132767420478,
  "euler_final": 23,
  "concentration_final": 35.04627035546484,
  "occupancy_final": 0.11138916015625,
  "n_blobs_final": 5,
  "activity": 3.134034029376505,
  "mass_drift": 4.12545132826521e-16,
  "score": 33.27837139698758
}
```

## Lineage tree

```json
{
  "6eeddb15": {
    "parent": null,
    "generation": 0,
    "birth_frame": 0,
    "death_frame": null,
    "lifespan": 151,
    "children": [
      "a68ef4ff",
      "264c85b0",
      "83bdebbb",
      "2e1206ba",
      "3435062f",
      "2aea9f73",
      "f5bc590b",
      "e1eaddf7",
      "b44747ef",
      "2c24962c",
      "91d21edf",
      "6508128e",
      "12e6fd13",
      "4a0450bb",
      "6a8eabef",
      "f2160fb1",
      "69c63b53",
      "b4814036",
      "5eecb781",
      "5e115299",
      "3d57444d"
    ],
    "peak_mass": 545.0295171963623,
    "dominant_channel": 0
  },
  "b57f8fd0": {
    "parent": null,
    "generation": 0,
    "birth_frame": 38,
    "death_frame": 40,
    "lifespan": 2,
    "children": [],
    "peak_mass": 1.7572907475926305,
    "dominant_channel": 2
  },
  "b4ee0f0d": {
    "parent": null,
    "generation": 0,
    "birth_frame": 40,
    "death_frame": 41,
    "lifespan": 1,
    "children": [],
    "peak_mass": 1.7574367634179333,
    "dominant_channel": 2
  },
  "0d9dae64": {
    "parent": null,
    "generation": 0,
    "birth_frame": 45,
    "death_frame": 46,
    "lifespan": 1,
    "children": [],
    "peak_mass": 1.6319724940906188,
    "dominant_channel": 2
  },
  "a68ef4ff": {
    "parent": "6eeddb15",
    "generation": 1,
    "birth_frame": 48,
    "death_frame": 49,
    "lifespan": 1,
    "children": [],
    "peak_mass": 2.5138073715965237,
    "dominant_channel": 2
  },
  "907b0724": {
    "parent": null,
    "generation": 0,
    "birth_frame": 50,
    "death_frame": 51,
    "lifespan": 1,
    "children": [],
    "peak_mass": 1.502034550263117,
    "dominant_channel": 2
  },
  "264c85b0": {
    "parent": "6eeddb15",
    "generation": 1,
    "birth_frame": 53,
    "death_frame": 55,
    "lifespan": 2,
    "children": [],
    "peak_mass": 2.888859687602318,
    "dominant_channel": 2
  },
  "83bdebbb": {
    "parent": "6eeddb15",
    "generation": 1,
    "birth_frame": 53,
    "death_frame": 54,
    "lifespan": 1,
    "children": [],
    "peak_mass": 1.559702864952478,
    "dominant_channel": 2
  },
  "60de6456": {
    "parent": null,
    "generation": 0,
    "birth_frame": 55,
    "death_frame": 56,
    "lifespan": 1,
    "children": [],
    "peak_mass": 3.2885815306176926,
    "dominant_channel": 2
  },
  "2e1206ba": {
    "parent": "6eeddb15",
    "generation": 1,
    "birth_frame": 57,
    "death_frame": 58,
    "lifespan": 1,
    "children": [],
    "peak_mass": 2.7570316214518185,
    "dominant_channel": 2
  },
  "815bcdf5": {
    "parent": null,
    "generation": 0,
    "birth_frame": 58,
    "death_frame": 59,
    "lifespan": 1,
    "children": [],
    "peak_mass": 1.6405134354708213,
    "dominant_channel": 2
  },
  "b95b545c": {
    "parent": null,
    "generation": 0,
    "birth_frame": 60,
    "death_frame": 63,
    "lifespan": 3,
    "children": [],
    "peak_mass": 2.4699297106924343,
    "dominant_channel": 2
  },
  "3435062f": {
    "parent": "6eeddb15",
    "generation": 1,
    "birth_frame": 64,
    "death_frame": 65,
    "lifespan": 1,
    "children": [],
    "peak_mass": 2.0762451294873245,
    "dominant_channel": 2
  },
  "2aea9f73": {
    "parent": "6eeddb15",
    "generation": 1,
    "birth_frame": 64,
    "death_frame": 65,
    "lifespan": 1,
    "children": [],
    "peak_mass": 1.995999323534693,
    "dominant_channel": 2
  },
  "1c20e39b": {
    "parent": null,
    "generation": 0,
    "birth_frame": 67,
    "death_frame": 72,
    "lifespan": 5,
    "children": [],
    "peak_mass": 2.1608682024820975,
    "dominant_channel": 2
  },
  "f5bc590b": {
    "parent": "6eeddb15",
    "generation": 1,
    "birth_frame": 68,
    "death_frame": 69,
    "lifespan": 1,
    "children": [],
    "peak_mass": 2.757828728936048,
    "dominant_channel": 2
  },
  "e1eaddf7": {
    "parent": "6eeddb15",
    "generation": 1,
    "birth_frame": 68,
    "death_frame": 69,
    "lifespan": 1,
    "children": [],
    "peak_mass": 1.9759236430753813,
    "dominant_channel": 2
  },
  "b44747ef": {
    "parent": "6eeddb15",
    "generation": 1,
    "birth_frame": 68,
    "death_frame": 77,
    "lifespan": 9,
    "children": [],
    "peak_mass": 3.5456756374691016,
    "dominant_channel": 2
  },
  "2c24962c": {
    "parent": "6eeddb15",
    "generation": 1,
    "birth_frame": 70,
    "death_frame": 75,
    "lifespan": 5,
    "children": [],
    "peak_mass": 5.844153480495014,
    "dominant_channel": 2
  },
  "cfa3ac80": {
    "parent": null,
    "generation": 0,
    "birth_frame": 70,
    "death_frame": 71,
    "lifespan": 1,
    "children": [],
    "peak_mass": 1.4184191114699434,
    "dominant_channel": 2
  },
  "91d21edf": {
    "parent": "6eeddb15",
    "generation": 1,
    "birth_frame": 71,
    "death_frame": 77,
    "lifespan": 6,
    "children": [],
    "peak_mass": 4.767939029174461,
    "dominant_channel": 2
  },
  "a23e5af5": {
    "parent": null,
    "generation": 0,
    "birth_frame": 75,
    "death_frame": 76,
    "lifespan": 1,
    "children": [],
    "peak_mass": 2.1088681199089447,
    "dominant_channel": 2
  },
  "6508128e": {
    "parent": "6eeddb15",
    "generation": 1,
    "birth_frame": 77,
    "death_frame": null,
    "lifespan": 74,
    "children": [
      "0e5e89aa"
    ],
    "peak_mass": 9.11548977994139,
    "dominant_channel": 2
  },
  "12e6fd13": {
    "parent": "6eeddb15",
    "generation": 1,
    "birth_frame": 78,
    "death_frame": 79,
    "lifespan": 1,
    "children": [],
    "peak_mass": 2.4294972504597934,
    "dominant_channel": 1
  },
  "a0400406": {
    "parent": null,
    "generation": 0,
    "birth_frame": 79,
    "death_frame": 81,
    "lifespan": 2,
    "children": [],
    "peak_mass": 6.038552204615464,
    "dominant_channel": 2
  },
  "2b77d619": {
    "parent": null,
    "generation": 0,
    "birth_frame": 79,
    "death_frame": 82,
    "lifespan": 3,
    "children": [
      "530bfb27"
    ],
    "peak_mass": 4.618694952887446,
    "dominant_channel": 2
  },
  "530bfb27": {
    "parent": "2b77d619",
    "generation": 1,
    "birth_frame": 81,
    "death_frame": 84,
    "lifespan": 3,
    "children": [
      "ca23132f"
    ],
    "peak_mass": 5.97756195610717,
    "dominant_channel": 2
  },
  "5d722aff": {
    "parent": null,
    "generation": 0,
    "birth_frame": 81,
    "death_frame": 82,
    "lifespan": 1,
    "children": [],
    "peak_mass": 2.340349589981929,
    "dominant_channel": 2
  },
  "ca23132f": {
    "parent": "530bfb27",
    "generation": 2,
    "birth_frame": 83,
    "death_frame": 84,
    "lifespan": 1,
    "children": [],
    "peak_mass": 2.1577013768443973,
    "dominant_channel": 2
  },
  "4a0450bb": {
    "parent": "6eeddb15",
    "generation": 1,
    "birth_frame": 83,
    "death_frame": 85,
    "lifespan": 2,
    "children": [],
    "peak_mass": 3.122721692580522,
    "dominant_channel": 1
  },
  "6a8eabef": {
    "parent": "6eeddb15",
    "generation": 1,
    "birth_frame": 83,
    "death_frame": 85,
    "lifespan": 2,
    "children": [],
    "peak_mass": 3.0148443299479277,
    "dominant_channel": 2
  },
  "f2160fb1": {
    "parent": "6eeddb15",
    "generation": 1,
    "birth_frame": 85,
    "death_frame": 86,
    "lifespan": 1,
    "children": [],
    "peak_mass": 3.721102695793081,
    "dominant_channel": 2
  },
  "f109d8c8": {
    "parent": null,
    "generation": 0,
    "birth_frame": 86,
    "death_frame": 102,
    "lifespan": 16,
    "children": [
      "d9357c63",
      "d6513f18"
    ],
    "peak_mass": 6.865640936176231,
    "dominant_channel": 2
  },
  "2bb2a0f2": {
    "parent": null,
    "generation": 0,
    "birth_frame": 87,
    "death_frame": 88,
    "lifespan": 1,
    "children": [],
    "peak_mass": 5.937483849033143,
    "dominant_channel": 2
  },
  "6f37e781": {
    "parent": null,
    "generation": 0,
    "birth_frame": 87,
    "death_frame": 88,
    "lifespan": 1,
    "children": [],
    "peak_mass": 1.739354141383933,
    "dominant_channel": 2
  },
  "9f68ec70": {
    "parent": null,
    "generation": 0,
    "birth_frame": 89,
    "death_frame": 90,
    "lifespan": 1,
    "children": [],
    "peak_mass": 2.15652413116856,
    "dominant_channel": 2
  },
  "69c63b53": {
    "parent": "6eeddb15",
    "generation": 1,
    "birth_frame": 90,
    "death_frame": 92,
    "lifespan": 2,
    "children": [],
    "peak_mass": 5.279503776084836,
    "dominant_channel": 2
  },
  "b4814036": {
    "parent": "6eeddb15",
    "generation": 1,
    "birth_frame": 90,
    "death_frame": 96,
    "lifespan": 6,
    "children": [],
    "peak_mass": 4.614015347522702,
    "dominant_channel": 2
  },
  "d9357c63": {
    "parent": "f109d8c8",
    "generation": 1,
    "birth_frame": 91,
    "death_frame": 92,
    "lifespan": 1,
    "children": [],
    "peak_mass": 1.5880699031609842,
    "dominant_channel": 2
  },
  "5eecb781": {
    "parent": "6eeddb15",
    "generation": 1,
    "birth_frame": 91,
    "death_frame": 93,
    "lifespan": 2,
    "children": [],
    "peak_mass": 1.8665659036423006,
    "dominant_channel": 1
  }
}
```

## Media

- `outputs/SPECIES_017_ORBITA_final.png`
- `outputs/SPECIES_017_ORBITA.gif`
- `outputs/SPECIES_017_ORBITA.mp4`

- genome: `outputs/species/SPECIES_017_ORBITA_genome.json`
