# HUNT 001 — CHASER_DYAD

**Status:** VERIFIED
**Steps:** 400  |  **Wall clock:** 2.7s

## Gates

| gate | verdict | value | detail |
| --- | --- | --- | --- |
| mass_conservation | PASS | 1.42109e-16 | tol=0.0001, m0=800.000000 |
| non_triviality | PASS | 10.1183 | peak/mean, need >= 2.0 |
| dynamic_activity | PASS | 0.00343845 | v_cm=0.00344 (>0.001), S_dot=4.802e-04 (>0) |
| attractor_self_heal | PASS | 1.14363 | conc 10.12 -> blast 12.17 -> healed 11.57 in 200 steps; clean self-heal |

## Metrics

```json
{
  "steps": 400,
  "mass_0": 799.9999999999999,
  "mass_final": 799.9999999999999,
  "mass_drift": 1.4210854715202006e-16,
  "concentration_final": 10.118281103394786,
  "entropy_final": 8.697696007606844,
  "v_cm": 0.003438445054523094,
  "s_dot": 0.00048016927348433215,
  "com_final": [
    78.0064836140405,
    71.91746867551142
  ],
  "attractor_conc_before": 10.118281103394786,
  "attractor_conc_after_blast": 12.174555273256592,
  "attractor_conc_healed": 11.571532239686153,
  "attractor_disruption": 0.20322366505234823,
  "attractor_recovery": 1.143626286069853,
  "attractor_heal_mass_ok": true
}
```

## Genome

```json
{
  "n_channels": 2,
  "size": 128,
  "dx": 1.0,
  "dt": 0.05,
  "kernel_radius": [
    8.457191805606886,
    14.809812200008817
  ],
  "kernel_sigma": [
    3.2602019987461333,
    3.2464053338024357
  ],
  "K": [
    [
      -0.7876895768819296,
      -2.5801518857119214
    ],
    [
      0.8282608420765968,
      -1.4578900645411248
    ]
  ],
  "self_repulsion": 0.5065430831572099,
  "repulsion_sigma": 1.7703675111190635,
  "v_max": 0.35,
  "seed": 1
}
```

## Snapshots

- `outputs/HUNT_001_CHASER_DYAD_init.png`
- `outputs/HUNT_001_CHASER_DYAD_final.png`
