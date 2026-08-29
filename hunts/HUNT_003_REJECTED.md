# HUNT 003 — FLEEING_SHELL

**Status:** REJECTED
**Steps:** 400  |  **Wall clock:** 0.6s

## Gates

| gate | verdict | value | detail |
| --- | --- | --- | --- |
| mass_conservation | PASS | 0 | tol=0.0001, m0=800.000000 |
| non_triviality | PASS | 13.2295 | peak/mean, need >= 2.0 |
| dynamic_activity | PASS | 0.00254267 | v_cm=0.00254 (>0.001), S_dot=1.431e-03 (>0) |
| attractor_self_heal | FAIL | 1.26168 | conc 13.23 -> blast 17.81 -> healed 16.69 in 200 steps; recovery 1.262 outside [0.8, 1.25] |

## Metrics

```json
{
  "steps": 400,
  "mass_0": 800.0,
  "mass_final": 800.0,
  "mass_drift": 0.0,
  "concentration_final": 13.229511850704641,
  "entropy_final": 8.646355462916361,
  "v_cm": 0.0025426722087853897,
  "s_dot": 0.0014309982325960036,
  "com_final": [
    39.82112131305046,
    19.402012911333436
  ],
  "attractor_conc_before": 13.229511850704641,
  "attractor_conc_after_blast": 17.806353718130026,
  "attractor_conc_healed": 16.691446527498638,
  "attractor_disruption": 0.3459569724926479,
  "attractor_recovery": 1.2616827223757014,
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
    12.512677170056461,
    19.507880813257092
  ],
  "kernel_sigma": [
    2.68087439900816,
    4.4938514712453905
  ],
  "K": [
    [
      -1.0946793271888513,
      -1.9004117892298136
    ],
    [
      1.2620704583938798,
      -1.2607915574841853
    ]
  ],
  "self_repulsion": 1.0794039787584508,
  "repulsion_sigma": 2.5600562107000635,
  "v_max": 0.35,
  "seed": 3
}
```

## Snapshots

- `outputs/HUNT_003_FLEEING_SHELL_init.png`
- `outputs/HUNT_003_FLEEING_SHELL_final.png`
