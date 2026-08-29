# HUNT 005 — TWIN_VORTEX

**Status:** VERIFIED
**Steps:** 400  |  **Wall clock:** 0.5s

## Gates

| gate | verdict | value | detail |
| --- | --- | --- | --- |
| mass_conservation | PASS | 1.42109e-16 | tol=0.0001, m0=800.000000 |
| non_triviality | PASS | 9.73495 | peak/mean, need >= 2.0 |
| dynamic_activity | PASS | 0.011067 | v_cm=0.01107 (>0.001), S_dot=1.195e-03 (>0) |
| attractor_self_heal | PASS | 1.20027 | conc 9.73 -> blast 12.15 -> healed 11.68 in 200 steps; clean self-heal |

## Metrics

```json
{
  "steps": 400,
  "mass_0": 800.0,
  "mass_final": 800.0,
  "mass_drift": 1.4210854715202004e-16,
  "concentration_final": 9.734948044833429,
  "entropy_final": 8.941213976463454,
  "v_cm": 0.011067033139368267,
  "s_dot": 0.0011954956717273647,
  "com_final": [
    64.7671430624603,
    20.748894231521316
  ],
  "attractor_conc_before": 9.734948044833429,
  "attractor_conc_after_blast": 12.149870605367052,
  "attractor_conc_healed": 11.684571680058642,
  "attractor_disruption": 0.24806732911279195,
  "attractor_recovery": 1.2002705742492303,
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
    13.008756347264518,
    21.790498031077362
  ],
  "kernel_sigma": [
    2.324469408180316,
    4.242011636946779
  ],
  "K": [
    [
      -0.8872840283677704,
      -1.73155067690863
    ],
    [
      2.4750116762994865,
      -1.2385580486204986
    ]
  ],
  "self_repulsion": 0.9017789945010947,
  "repulsion_sigma": 2.0100055348498813,
  "v_max": 0.35,
  "seed": 5
}
```

## Snapshots

- `outputs/HUNT_005_TWIN_VORTEX_init.png`
- `outputs/HUNT_005_TWIN_VORTEX_final.png`
