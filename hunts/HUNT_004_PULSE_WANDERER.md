# HUNT 004 — PULSE_WANDERER

**Status:** VERIFIED
**Steps:** 400  |  **Wall clock:** 0.5s

## Gates

| gate | verdict | value | detail |
| --- | --- | --- | --- |
| mass_conservation | PASS | 0 | tol=0.0001, m0=800.000000 |
| non_triviality | PASS | 18.2651 | peak/mean, need >= 2.0 |
| dynamic_activity | PASS | 0.00277932 | v_cm=0.00278 (>0.001), S_dot=8.732e-04 (>0) |
| attractor_self_heal | PASS | 1.04798 | conc 18.27 -> blast 20.30 -> healed 19.14 in 200 steps; clean self-heal |

## Metrics

```json
{
  "steps": 400,
  "mass_0": 800.0,
  "mass_final": 800.0,
  "mass_drift": 0.0,
  "concentration_final": 18.265133672762488,
  "entropy_final": 8.713784121160492,
  "v_cm": 0.002779320486117631,
  "s_dot": 0.0008731635779795965,
  "com_final": [
    16.834416955154754,
    82.56148437245776
  ],
  "attractor_conc_before": 18.265133672762488,
  "attractor_conc_after_blast": 20.295891967045595,
  "attractor_conc_healed": 19.141485075935382,
  "attractor_disruption": 0.11118223007102501,
  "attractor_recovery": 1.0479794683616104,
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
    11.724042829147926,
    20.533834911243865
  ],
  "kernel_sigma": [
    2.250984680119146,
    4.401191668596105
  ],
  "K": [
    [
      -0.7384773652985913,
      -1.601408724385144
    ],
    [
      1.0342723618297367,
      -0.9806546369472374
    ]
  ],
  "self_repulsion": 0.5919747024599642,
  "repulsion_sigma": 2.737480492245595,
  "v_max": 0.35,
  "seed": 4
}
```

## Snapshots

- `outputs/HUNT_004_PULSE_WANDERER_init.png`
- `outputs/HUNT_004_PULSE_WANDERER_final.png`
