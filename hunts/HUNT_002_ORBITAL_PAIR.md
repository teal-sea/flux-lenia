# HUNT 002 — ORBITAL_PAIR

**Status:** VERIFIED
**Steps:** 400  |  **Wall clock:** 0.7s

## Gates

| gate | verdict | value | detail |
| --- | --- | --- | --- |
| mass_conservation | PASS | 0 | tol=0.0001, m0=800.000000 |
| non_triviality | PASS | 10.0747 | peak/mean, need >= 2.0 |
| dynamic_activity | PASS | 0.00280644 | v_cm=0.00281 (>0.001), S_dot=8.810e-04 (>0) |
| attractor_self_heal | PASS | 1.08122 | conc 10.07 -> blast 11.61 -> healed 10.89 in 200 steps; clean self-heal |

## Metrics

```json
{
  "steps": 400,
  "mass_0": 800.0,
  "mass_final": 800.0,
  "mass_drift": 0.0,
  "concentration_final": 10.074722612984914,
  "entropy_final": 8.759191180251534,
  "v_cm": 0.00280644116215895,
  "s_dot": 0.0008809541687258005,
  "com_final": [
    89.22110257537432,
    102.96322491618604
  ],
  "attractor_conc_before": 10.074722612984914,
  "attractor_conc_after_blast": 11.610537806772578,
  "attractor_conc_healed": 10.892995290177094,
  "attractor_disruption": 0.15244242971098898,
  "attractor_recovery": 1.081220367907454,
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
    10.02278712079722,
    17.994050765766616
  ],
  "kernel_sigma": [
    2.3744368033291616,
    3.2991309475921966
  ],
  "K": [
    [
      -1.347612317068191,
      -2.2093138551729856
    ],
    [
      1.4429408078077046,
      -0.9894919191049115
    ]
  ],
  "self_repulsion": 0.9882448772095005,
  "repulsion_sigma": 2.104050086197955,
  "v_max": 0.35,
  "seed": 2
}
```

## Snapshots

- `outputs/HUNT_002_ORBITAL_PAIR_init.png`
- `outputs/HUNT_002_ORBITAL_PAIR_final.png`
