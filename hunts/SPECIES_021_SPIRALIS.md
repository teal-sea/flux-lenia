# SPECIES 021 — SPIRALIS

**Verdict:** VIABLE + REPRODUCING
**Origin:** random  |  **Seed:** 792

## Viability gates

| gate | verdict | value | detail |
| --- | --- | --- | --- |
| mass_conservation | PASS | 2.30768e-16 | tol=0.0001 |
| non_triviality | PASS | 12.5361 | conc>=6.0, occupancy 0.231<=0.45, 7 bodies |
| persistence | PASS | 2 | 2 organisms alive at the end with lifespan >= 15 frames |
| activity | PASS | 6.08663 | mean speed of the most mobile organism, cells/frame |

## Behaviour (anomaly bouncer)

| behaviour | established | score | evidence |
| --- | --- | --- | --- |
| phototaxis | no | 0.001 | lamp(26, 64): 38.3->38.1; lamp(102, 64): 38.5->38.4; lamp(64, 26): 38.3->38.3 | min approach +0.001 (needs > 0.05 for every lamp position) |
| predatory_pursuit | no | 0.069 | 8fb9c96a(ch2) -> f7502195(ch2) closed 9.0 -> 7.8 cells over 22 frames, monotone 0.52, target speed 0.224 |
| cyclic_locomotion | no | 0.372 | uid=ed917769 circling=0.14 spectral_power=0.12 period=22.5 frames (counted only if >= 4) life=46 frames |

## Reproduction

Measured on the recording run below (the screening run is sampled more coarsely and its counts differ; both are stated separately rather than mixed).

- Divisions counted (offspring survived AND carried at least 10% of the parent's mass): **0**
- Raw fission events before the mass filter: **7** — the difference is debris a large body shed, which is not reproduction
- Surviving offspring total: **0**
- Organisms tracked in this run: **116**
- Screening run, for comparison: 1 divisions of 6 raw fissions, deepest generation 3

## Complexity

```json
{
  "morph_diversity": 3.284799137187589,
  "spatial_mi": 1.3953882272960503,
  "cross_channel_mi": 0.755681335396808,
  "euler_final": 30,
  "concentration_final": 12.536084140326865,
  "occupancy_final": 0.2305908203125,
  "n_blobs_final": 7,
  "activity": 6.08663374993182,
  "mass_drift": 2.307679873259348e-16,
  "score": 16.872569661242288
}
```

## Lineage tree

```json
{
  "e9d97b53": {
    "parent": null,
    "generation": 0,
    "birth_frame": 0,
    "death_frame": 56,
    "lifespan": 56,
    "children": [
      "76091cec",
      "2cec3c29",
      "2b4abf4e",
      "e8fe3bb8",
      "e756321a",
      "dac93fda",
      "304e7074",
      "fade4063",
      "a8b2a1a1",
      "97835162",
      "a2ec2fe7",
      "6473721b"
    ],
    "peak_mass": 3898.558290703176,
    "dominant_channel": 1
  },
  "fd40274f": {
    "parent": null,
    "generation": 0,
    "birth_frame": 21,
    "death_frame": 22,
    "lifespan": 1,
    "children": [],
    "peak_mass": 6.279278934170687,
    "dominant_channel": 0
  },
  "76091cec": {
    "parent": "e9d97b53",
    "generation": 1,
    "birth_frame": 24,
    "death_frame": 25,
    "lifespan": 1,
    "children": [],
    "peak_mass": 7.86175577935843,
    "dominant_channel": 2
  },
  "98882ae7": {
    "parent": null,
    "generation": 0,
    "birth_frame": 24,
    "death_frame": 25,
    "lifespan": 1,
    "children": [],
    "peak_mass": 4.040838774080252,
    "dominant_channel": 2
  },
  "2cec3c29": {
    "parent": "e9d97b53",
    "generation": 1,
    "birth_frame": 46,
    "death_frame": 47,
    "lifespan": 1,
    "children": [],
    "peak_mass": 6.435990226366854,
    "dominant_channel": 2
  },
  "2b4abf4e": {
    "parent": "e9d97b53",
    "generation": 1,
    "birth_frame": 47,
    "death_frame": 50,
    "lifespan": 3,
    "children": [],
    "peak_mass": 8.611086069571494,
    "dominant_channel": 2
  },
  "e8fe3bb8": {
    "parent": "e9d97b53",
    "generation": 1,
    "birth_frame": 49,
    "death_frame": 50,
    "lifespan": 1,
    "children": [],
    "peak_mass": 5.973339422087072,
    "dominant_channel": 2
  },
  "d9494cfd": {
    "parent": null,
    "generation": 0,
    "birth_frame": 50,
    "death_frame": 52,
    "lifespan": 2,
    "children": [],
    "peak_mass": 5.754793927080356,
    "dominant_channel": 2
  },
  "e756321a": {
    "parent": "e9d97b53",
    "generation": 1,
    "birth_frame": 51,
    "death_frame": 53,
    "lifespan": 2,
    "children": [],
    "peak_mass": 13.17147428991845,
    "dominant_channel": 2
  },
  "dac93fda": {
    "parent": "e9d97b53",
    "generation": 1,
    "birth_frame": 51,
    "death_frame": 54,
    "lifespan": 3,
    "children": [],
    "peak_mass": 12.763009047304324,
    "dominant_channel": 2
  },
  "304e7074": {
    "parent": "e9d97b53",
    "generation": 1,
    "birth_frame": 51,
    "death_frame": 53,
    "lifespan": 2,
    "children": [],
    "peak_mass": 4.970658709521368,
    "dominant_channel": 2
  },
  "86d10ca2": {
    "parent": null,
    "generation": 0,
    "birth_frame": 52,
    "death_frame": 53,
    "lifespan": 1,
    "children": [],
    "peak_mass": 5.132007552375562,
    "dominant_channel": 2
  },
  "fade4063": {
    "parent": "e9d97b53",
    "generation": 1,
    "birth_frame": 53,
    "death_frame": 54,
    "lifespan": 1,
    "children": [],
    "peak_mass": 8.291340879929681,
    "dominant_channel": 2
  },
  "a8b2a1a1": {
    "parent": "e9d97b53",
    "generation": 1,
    "birth_frame": 53,
    "death_frame": 61,
    "lifespan": 8,
    "children": [],
    "peak_mass": 11.67247147622456,
    "dominant_channel": 2
  },
  "97835162": {
    "parent": "e9d97b53",
    "generation": 1,
    "birth_frame": 53,
    "death_frame": 56,
    "lifespan": 3,
    "children": [],
    "peak_mass": 6.345116560090823,
    "dominant_channel": 2
  },
  "a2ec2fe7": {
    "parent": "e9d97b53",
    "generation": 1,
    "birth_frame": 53,
    "death_frame": 56,
    "lifespan": 3,
    "children": [],
    "peak_mass": 6.65088914915128,
    "dominant_channel": 2
  },
  "6473721b": {
    "parent": "e9d97b53",
    "generation": 1,
    "birth_frame": 53,
    "death_frame": 54,
    "lifespan": 1,
    "children": [],
    "peak_mass": 5.59458770345345,
    "dominant_channel": 2
  },
  "ac87b55f": {
    "parent": null,
    "generation": 0,
    "birth_frame": 54,
    "death_frame": 64,
    "lifespan": 10,
    "children": [],
    "peak_mass": 13.288400106778907,
    "dominant_channel": 2
  },
  "697aa632": {
    "parent": null,
    "generation": 0,
    "birth_frame": 54,
    "death_frame": 55,
    "lifespan": 1,
    "children": [],
    "peak_mass": 6.377934982400324,
    "dominant_channel": 2
  },
  "078f3160": {
    "parent": null,
    "generation": 0,
    "birth_frame": 54,
    "death_frame": 71,
    "lifespan": 17,
    "children": [
      "a113227d",
      "e3f3d218",
      "b0331070",
      "39bcc372",
      "9b1a1f04",
      "779838e0",
      "8d07451b",
      "bf1e31e2",
      "6aa2c127",
      "49c9e49b",
      "14d7da65",
      "18d040ae"
    ],
    "peak_mass": 3628.1982621814195,
    "dominant_channel": 1
  },
  "95a582da": {
    "parent": null,
    "generation": 0,
    "birth_frame": 55,
    "death_frame": 62,
    "lifespan": 7,
    "children": [
      "11df2bc6"
    ],
    "peak_mass": 12.76623454722785,
    "dominant_channel": 2
  },
  "11df2bc6": {
    "parent": "95a582da",
    "generation": 1,
    "birth_frame": 57,
    "death_frame": 58,
    "lifespan": 1,
    "children": [],
    "peak_mass": 5.331678604164177,
    "dominant_channel": 2
  },
  "2cfc7c3d": {
    "parent": null,
    "generation": 0,
    "birth_frame": 57,
    "death_frame": 58,
    "lifespan": 1,
    "children": [],
    "peak_mass": 5.078330448649171,
    "dominant_channel": 2
  },
  "a113227d": {
    "parent": "078f3160",
    "generation": 1,
    "birth_frame": 58,
    "death_frame": 59,
    "lifespan": 1,
    "children": [],
    "peak_mass": 16.916708176425168,
    "dominant_channel": 2
  },
  "e3f3d218": {
    "parent": "078f3160",
    "generation": 1,
    "birth_frame": 58,
    "death_frame": 59,
    "lifespan": 1,
    "children": [],
    "peak_mass": 5.419038005368005,
    "dominant_channel": 2
  },
  "5c851aa0": {
    "parent": null,
    "generation": 0,
    "birth_frame": 59,
    "death_frame": 62,
    "lifespan": 3,
    "children": [],
    "peak_mass": 5.25801253080256,
    "dominant_channel": 2
  },
  "a0cf11c7": {
    "parent": null,
    "generation": 0,
    "birth_frame": 59,
    "death_frame": 63,
    "lifespan": 4,
    "children": [],
    "peak_mass": 7.478906318262806,
    "dominant_channel": 2
  },
  "b0331070": {
    "parent": "078f3160",
    "generation": 1,
    "birth_frame": 61,
    "death_frame": 63,
    "lifespan": 2,
    "children": [
      "6771306f"
    ],
    "peak_mass": 35.603076379192665,
    "dominant_channel": 2
  },
  "6771306f": {
    "parent": "b0331070",
    "generation": 2,
    "birth_frame": 62,
    "death_frame": 65,
    "lifespan": 3,
    "children": [],
    "peak_mass": 33.88238893669824,
    "dominant_channel": 2
  },
  "39bcc372": {
    "parent": "078f3160",
    "generation": 1,
    "birth_frame": 63,
    "death_frame": 66,
    "lifespan": 3,
    "children": [
      "b970e92d"
    ],
    "peak_mass": 35.261085671715975,
    "dominant_channel": 2
  },
  "9b1a1f04": {
    "parent": "078f3160",
    "generation": 1,
    "birth_frame": 64,
    "death_frame": 66,
    "lifespan": 2,
    "children": [],
    "peak_mass": 9.641448555677467,
    "dominant_channel": 2
  },
  "779838e0": {
    "parent": "078f3160",
    "generation": 1,
    "birth_frame": 64,
    "death_frame": 66,
    "lifespan": 2,
    "children": [],
    "peak_mass": 9.089462059694904,
    "dominant_channel": 2
  },
  "8d07451b": {
    "parent": "078f3160",
    "generation": 1,
    "birth_frame": 64,
    "death_frame": 66,
    "lifespan": 2,
    "children": [],
    "peak_mass": 8.220295649306266,
    "dominant_channel": 2
  },
  "bf1e31e2": {
    "parent": "078f3160",
    "generation": 1,
    "birth_frame": 64,
    "death_frame": 66,
    "lifespan": 2,
    "children": [],
    "peak_mass": 7.1134505851996375,
    "dominant_channel": 2
  },
  "6aa2c127": {
    "parent": "078f3160",
    "generation": 1,
    "birth_frame": 64,
    "death_frame": 65,
    "lifespan": 1,
    "children": [],
    "peak_mass": 6.705834621014558,
    "dominant_channel": 2
  },
  "49c9e49b": {
    "parent": "078f3160",
    "generation": 1,
    "birth_frame": 65,
    "death_frame": 66,
    "lifespan": 1,
    "children": [],
    "peak_mass": 14.211221881462407,
    "dominant_channel": 2
  },
  "b970e92d": {
    "parent": "39bcc372",
    "generation": 2,
    "birth_frame": 65,
    "death_frame": 66,
    "lifespan": 1,
    "children": [],
    "peak_mass": 10.68114802918367,
    "dominant_channel": 2
  },
  "84486f80": {
    "parent": null,
    "generation": 0,
    "birth_frame": 66,
    "death_frame": 67,
    "lifespan": 1,
    "children": [],
    "peak_mass": 6.140199755535565,
    "dominant_channel": 2
  },
  "47ceda4b": {
    "parent": null,
    "generation": 0,
    "birth_frame": 66,
    "death_frame": 67,
    "lifespan": 1,
    "children": [],
    "peak_mass": 5.769161242250398,
    "dominant_channel": 2
  },
  "a550a602": {
    "parent": null,
    "generation": 0,
    "birth_frame": 66,
    "death_frame": 68,
    "lifespan": 2,
    "children": [],
    "peak_mass": 7.255602270040521,
    "dominant_channel": 2
  }
}
```

## Media

- `outputs/SPECIES_021_SPIRALIS_final.png`
- `outputs/SPECIES_021_SPIRALIS.gif`
- `outputs/SPECIES_021_SPIRALIS.mp4`

- genome: `outputs/species/SPECIES_021_SPIRALIS_genome.json`
