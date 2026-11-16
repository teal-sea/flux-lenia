# Pilot: choose food_sense (2026-11-16)

Rule and candidates: `docs/FOOD-SENSING-2026-11-16.md` (Pilot). 18 pilot runs, 10,000 steps each (15 candidates-by-species runs plus three `food_sense = 0` box runs), seed 1, treat, food on, `per_channel`, `kappa = 3`. Run on InstaBox. Runs 1 to 16 (all candidates and `fs0` OSCILLIS) on box `flux-campb-w1` (8 vCPU / 16 GiB), 02:00:34 to about 02:45 UTC, **under 33 to 63% CPU steal** (wall 1,000 to 1,320 s per run); the last two jobs (`fs0` MITOSA and VAGRANT, directory `fs0_t2/`) on the freshly created box `flux-campb-t2` (0% steal), because the w1 scheduler was stopped to move them (the scheduler process was killed deliberately; its 8 running children finished normally). `timing/` holds six extra 10,000-step sensing-on runs (seeds 2 and 3, `food_sense = 1`) used only to time a healthy box; they are not pilot runs and not part of the rule. Python 3.13.5, jax 0.11.1, numpy 2.5.2, scipy 1.18.1, CPU, float64. Nothing ran on citadel. Table from `python scripts/food_sensing_summary.py pilot`.

Note: the three box `food_sense = 0` runs reproduce the stored 2026-11-15 reference `Q` exactly (difference +0.00, 2-decimal print), so the engine with the new code at `food_sense = 0` reproduces the stored seed-1 run on a different host.

## Pilot runs (seed 1, treat, food on, per_channel, kappa 3, 10,000 steps)

Reference (food_sense = 0, 2026-11-15, kappa 3, treat, seeds 1-5, step 10,000): Q = body(10,000) - body(0); Q_ref = seed 1; R = max - min over seeds 1-5

| species | Q_ref (seed 1) | R (seed spread) | Q seeds 1-5 |
|---|---|---|---|
| OSCILLIS | 1564.21 | 856.31 | 1564.2, 1067.0, 1344.0, 1369.4, 1923.3 |
| MITOSA | 1560.73 | 827.20 | 1560.7, 1073.0, 1385.0, 1373.8, 1900.2 |
| VAGRANT | 1506.19 | 981.54 | 1506.2, 923.1, 1226.0, 1250.6, 1904.6 |

| food_sense | species | Q | Q - Q_ref | R | changes foraging (|dQ| > R) | gross eaten | body end | hybrid end | max sat_frac (100 samples) | max drift | wall s | sat ok | drift ok |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | OSCILLIS | 1564.21 | +0.00 | 856.31 | no | 17504.7 | 3415.2 | 0.139 | 3.71e-04 | 7.4e-16 | 796 | yes | yes |
| 0 | MITOSA | 1560.73 | +0.00 | 827.20 | no | 16974.1 | 3411.7 | 0.002 | 0.00e+00 | 6.1e-16 | 378 | yes | yes |
| 0 | VAGRANT | 1506.19 | +0.00 | 981.54 | no | 17330.9 | 3357.2 | 0.000 | 0.00e+00 | 9.8e-16 | 370 | yes | yes |
| 0.1 | OSCILLIS | 1560.77 | -3.44 | 856.31 | no | 17512.3 | 3411.8 | 0.032 | 3.57e-04 | 8.6e-16 | 1292 | yes | yes |
| 0.1 | MITOSA | 1515.53 | -45.20 | 827.20 | no | 16910.5 | 3366.5 | 0.003 | 0.00e+00 | 6.1e-16 | 1289 | yes | yes |
| 0.1 | VAGRANT | 1507.71 | +1.52 | 981.54 | no | 17262.4 | 3358.7 | 0.000 | 0.00e+00 | 9.8e-16 | 1300 | yes | yes |
|  | candidate 0.1: changes foraging in 0 of 3 species; clean (sat, drift) = True; qualifies = False | | | | | | | | | | | | |
| 0.3 | OSCILLIS | 1553.58 | -10.63 | 856.31 | no | 17409.3 | 3404.6 | 0.220 | 4.22e-04 | 7.4e-16 | 1316 | yes | yes |
| 0.3 | MITOSA | 1513.46 | -47.27 | 827.20 | no | 17071.1 | 3364.4 | 0.003 | 0.00e+00 | 8.6e-16 | 1272 | yes | yes |
| 0.3 | VAGRANT | 1507.75 | +1.56 | 981.54 | no | 17280.1 | 3358.7 | 0.000 | 0.00e+00 | 7.4e-16 | 1319 | yes | yes |
|  | candidate 0.3: changes foraging in 0 of 3 species; clean (sat, drift) = True; qualifies = False | | | | | | | | | | | | |
| 1 | OSCILLIS | 1512.15 | -52.06 | 856.31 | no | 17112.8 | 3363.1 | 0.000 | 0.00e+00 | 6.1e-16 | 1305 | yes | yes |
| 1 | MITOSA | 1545.25 | -15.48 | 827.20 | no | 16720.0 | 3396.2 | 0.001 | 1.51e-04 | 7.4e-16 | 1287 | yes | yes |
| 1 | VAGRANT | 1487.33 | -18.86 | 981.54 | no | 17292.2 | 3338.3 | 0.000 | 0.00e+00 | 7.4e-16 | 1001 | yes | yes |
|  | candidate 1: changes foraging in 0 of 3 species; clean (sat, drift) = True; qualifies = False | | | | | | | | | | | | |
| 3 | OSCILLIS | 1372.77 | -191.44 | 856.31 | no | 15736.7 | 3223.8 | 0.003 | 1.55e-04 | 4.9e-16 | 1037 | yes | yes |
| 3 | MITOSA | 1542.13 | -18.60 | 827.20 | no | 16513.4 | 3393.1 | 0.000 | 0.00e+00 | 8.6e-16 | 1015 | yes | yes |
| 3 | VAGRANT | 1469.72 | -36.48 | 981.54 | no | 17415.6 | 3320.7 | 0.000 | 0.00e+00 | 6.1e-16 | 1032 | yes | yes |
|  | candidate 3: changes foraging in 0 of 3 species; clean (sat, drift) = True; qualifies = False | | | | | | | | | | | | |
| 10 | OSCILLIS | 1351.47 | -212.74 | 856.31 | no | 16166.1 | 3202.5 | 0.001 | 0.00e+00 | 9.8e-16 | 1025 | yes | yes |
| 10 | MITOSA | 1233.94 | -326.79 | 827.20 | no | 14800.5 | 3084.9 | 0.000 | 0.00e+00 | 4.9e-16 | 1037 | yes | yes |
| 10 | VAGRANT | 1468.18 | -38.01 | 981.54 | no | 17450.8 | 3319.2 | 0.000 | 0.00e+00 | 8.6e-16 | 1021 | yes | yes |
|  | candidate 10: changes foraging in 0 of 3 species; clean (sat, drift) = True; qualifies = False | | | | | | | | | | | | |

**No candidate qualifies; the largest non-saturating, conserving candidate, food_sense = 10, is taken** (pre-registered fallback).
