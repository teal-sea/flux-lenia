# Pilot 2 gain ladder: verdicts

pilot root `outputs/pilot2_gain_ladder`, reference root `outputs/food_sensing_2x2_gpu` (food_sense 0, kappa 3, treat, read at step 10,000)

| species | gain | n | median Q(g) | IQR Q(g) | median Q(0) | IQR Q(0) | R(0) | n ref | max sat | max drift | changes foraging | clean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SPECIES_001_OSCILLIS | 30 | 64 | 1374.56 | [1189.40, 1626.72] | 1469.08 | [1343.72, 1632.58] | 893.74 | 50 | 0.00e+00 | 1.1e-15 | no | yes |
| SPECIES_001_OSCILLIS | 100 | 64 | 1362.43 | [1218.96, 1598.37] | 1469.08 | [1343.72, 1632.58] | 893.74 | 50 | 0.00e+00 | 1.9e-15 | no | yes |
| SPECIES_001_OSCILLIS | 300 | 64 | 1272.84 | [967.27, 1549.85] | 1469.08 | [1343.72, 1632.58] | 893.74 | 50 | 0.00e+00 | 1.2e-15 | no | yes |
| SPECIES_001_OSCILLIS | 1000 | 64 | 1113.64 | [952.76, 1536.47] | 1469.08 | [1343.72, 1632.58] | 893.74 | 50 | 0.00e+00 | 1.8e-15 | no | yes |
| SPECIES_002_MITOSA | 30 | 64 | 1209.56 | [1040.90, 1351.78] | 1428.20 | [1336.88, 1623.16] | 976.07 | 50 | 0.00e+00 | 3.5e-15 | no | yes |
| SPECIES_002_MITOSA | 100 | 64 | 1111.07 | [934.35, 1339.39] | 1428.20 | [1336.88, 1623.16] | 976.07 | 50 | 0.00e+00 | 5.7e-15 | no | yes |
| SPECIES_002_MITOSA | 300 | 64 | 1076.07 | [889.28, 1264.81] | 1428.20 | [1336.88, 1623.16] | 976.07 | 50 | 2.82e-04 | 7.5e-15 | no | yes |
| SPECIES_002_MITOSA | 1000 | 64 | 1136.85 | [906.99, 1327.14] | 1428.20 | [1336.88, 1623.16] | 976.07 | 50 | 0.00e+00 | 5.3e-15 | no | yes |
| SPECIES_003_VAGRANT | 30 | 64 | 1334.38 | [1127.19, 1577.66] | 1402.03 | [1213.35, 1589.41] | 1026.40 | 50 | 0.00e+00 | 1.1e-15 | no | yes |
| SPECIES_003_VAGRANT | 100 | 64 | 1176.58 | [995.69, 1475.54] | 1402.03 | [1213.35, 1589.41] | 1026.40 | 50 | 0.00e+00 | 7.4e-16 | no | yes |
| SPECIES_003_VAGRANT | 300 | 64 | 1314.51 | [1096.93, 1538.90] | 1402.03 | [1213.35, 1589.41] | 1026.40 | 50 | 0.00e+00 | 5.7e-16 | no | yes |
| SPECIES_003_VAGRANT | 1000 | 64 | 1399.23 | [1252.26, 1574.92] | 1402.03 | [1213.35, 1589.41] | 1026.40 | 50 | 5.45e-04 | 7.1e-16 | no | yes |

| gain | species measured | changes foraging in | clean in | qualifies |
|---|---|---|---|---|
| 30 | 3 | 0 of 3 | 3 of 3 | no |
| 100 | 3 | 0 of 3 | 3 of 3 | no |
| 300 | 3 | 0 of 3 | 3 of 3 | no |
| 1000 | 3 | 0 of 3 | 3 of 3 | no |

**No gain qualifies: nothing changes foraging at any gain (prediction iii, no coupling).** Next design per the doc: a food-coupled hunt gate.
