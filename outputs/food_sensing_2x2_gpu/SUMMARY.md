1500 runs in food_sensing_2x2_gpu; cells (food_sense, kappa): F0K0=(0, 0), F0K3=(0, 3), F1K0=(10, 0), F1K3=(10, 3)

Runs per species and cell (expected 150): OSCILLIS F0K0 150; OSCILLIS F0K3 150; OSCILLIS F1K0 150; OSCILLIS F1K3 150; MITOSA F0K0 150; MITOSA F0K3 150; MITOSA F1K0 150; MITOSA F1K3 150; VAGRANT F0K0 150; VAGRANT F0K3 150; VAGRANT F1K0 0; VAGRANT F1K3 0

### Rule 1: selection per cell per species (E = largest neutral |delta| of the cell's 100 neutral runs)

| species | cell | E | n out | winner split (+u / -u) | winner-side final share min / median / max | verdict | E95 (secondary) | n out E95 | split E95 | verdict E95 (secondary) |
|---|---|---|---|---|---|---|---|---|---|---|
| OSCILLIS | F0K0 | 0.0381 | 7 of 50 | 1 / 6 | 0.538 / 0.546 / 0.574 | no selection detected | 0.0184 | 29 | 8 / 21 | no selection detected |
| OSCILLIS | F0K3 | 0.0326 | 24 of 50 | 7 / 17 | 0.534 / 0.587 / 0.655 | no selection detected | 0.0202 | 32 | 11 / 21 | no selection detected |
| OSCILLIS | F1K0 | 0.0331 | 28 of 50 | 28 / 0 | 0.534 / 0.550 / 0.591 | no selection detected | 0.0263 | 36 | 36 / 0 | no selection detected |
| OSCILLIS | F1K3 | 0.0342 | 40 of 50 | 40 / 0 | 0.538 / 0.568 / 0.619 | selection | 0.0238 | 44 | 43 / 1 | selection |
| MITOSA | F0K0 | 0.0641 | 1 of 50 | 1 / 0 | 0.588 / 0.588 / 0.588 | no selection detected | 0.0415 | 6 | 5 / 1 | no selection detected |
| MITOSA | F0K3 | 0.0763 | 9 of 50 | 9 / 0 | 0.582 / 0.600 / 0.651 | no selection detected | 0.0442 | 18 | 18 / 0 | no selection detected |
| MITOSA | F1K0 | 0.0597 | 5 of 50 | 4 / 1 | 0.555 / 0.569 / 0.600 | no selection detected | 0.0322 | 14 | 8 / 6 | no selection detected |
| MITOSA | F1K3 | 0.0523 | 19 of 50 | 19 / 0 | 0.555 / 0.576 / 0.635 | no selection detected | 0.0308 | 30 | 28 / 2 | no selection detected |
| VAGRANT | F0K0 | 0.0393 | 19 of 50 | 10 / 9 | 0.543 / 0.596 / 0.741 | no selection detected | 0.0179 | 36 | 12 / 24 | no selection detected |
| VAGRANT | F0K3 | 0.0388 | 25 of 50 | 24 / 1 | 0.537 / 0.574 / 0.766 | no selection detected | 0.0181 | 35 | 30 / 5 | no selection detected |
| VAGRANT | F1K0 | nan | 0 of 0 | 0 / 0 | - | no selection detected | nan | 0 | 0 / 0 | no selection detected |
| VAGRANT | F1K3 | nan | 0 of 0 | 0 / 0 | - | no selection detected | nan | 0 | 0 / 0 | no selection detected |

### Rule 2: cause (sensing-on selection, matched sensing-off null)

| species | kappa | sensing off | sensing on | cause shown |
|---|---|---|---|---|
| OSCILLIS | 0 | no selection detected | no selection detected | no (no selection with sensing) |
| OSCILLIS | 3 | no selection detected | selection | yes |
| MITOSA | 0 | no selection detected | no selection detected | no (no selection with sensing) |
| MITOSA | 3 | no selection detected | no selection detected | no (no selection with sensing) |
| VAGRANT | 0 | no selection detected | no selection detected | no (no selection with sensing) |
| VAGRANT | 3 | no selection detected | no selection detected | no (no selection with sensing) |

- OSCILLIS: repulsion necessary (sensing-on selection at kappa 3 and not at kappa 0): yes

- MITOSA: repulsion necessary (sensing-on selection at kappa 3 and not at kappa 0): no

- VAGRANT: repulsion necessary (sensing-on selection at kappa 3 and not at kappa 0): no

### Rule 3: distinctness, kappa 3 vs kappa 0 at the same food_sense (treatment arm, end hybrid fraction)

| species | food_sense | median hybrid kappa 0 | median hybrid kappa 3 | ratio | seeds below matched kappa-0 seed | verdict |
|---|---|---|---|---|---|---|
| OSCILLIS | 0 | 1.000 | 0.021 | 0.02 | 48 of 50 | distinct |
| OSCILLIS | 10 | 0.434 | 0.000 | 0.00 | 42 of 50 | distinct |
| MITOSA | 0 | 1.000 | 0.000 | 0.00 | 50 of 50 | distinct |
| MITOSA | 10 | 0.325 | 0.003 | 0.01 | 44 of 50 | distinct |
| VAGRANT | 0 | 0.743 | 0.000 | 0.00 | 50 of 50 | distinct |

### Rule 4: neutral-arm sanity (mean and SE of neutral delta; flag if |mean| > 2 SE)

| species | cell | n | mean | SE | mean/SE | neutral_plus mean | neutral_minus mean | flag |
|---|---|---|---|---|---|---|---|---|
| OSCILLIS | F0K0 | 100 | +0.0008 | 0.0009 | +0.83 | +0.0003 | +0.0012 | ok |
| OSCILLIS | F0K3 | 100 | +0.0008 | 0.0010 | +0.87 | +0.0006 | +0.0010 | ok |
| OSCILLIS | F1K0 | 100 | +0.0015 | 0.0012 | +1.25 | +0.0012 | +0.0018 | ok |
| OSCILLIS | F1K3 | 100 | +0.0005 | 0.0011 | +0.40 | +0.0013 | -0.0004 | ok |
| MITOSA | F0K0 | 100 | +0.0023 | 0.0020 | +1.14 | +0.0003 | +0.0044 | ok |
| MITOSA | F0K3 | 100 | -0.0046 | 0.0021 | -2.19 | -0.0022 | -0.0070 | FLAG |
| MITOSA | F1K0 | 100 | -0.0006 | 0.0017 | -0.38 | -0.0020 | +0.0007 | ok |
| MITOSA | F1K3 | 100 | -0.0009 | 0.0016 | -0.55 | -0.0001 | -0.0017 | ok |
| VAGRANT | F0K0 | 100 | -0.0002 | 0.0009 | -0.17 | +0.0013 | -0.0016 | ok |
| VAGRANT | F0K3 | 100 | +0.0005 | 0.0010 | +0.49 | +0.0013 | -0.0003 | ok |

Flags: 1 of 12 cell-species combinations (about 0.6 expected by chance at 2 SE).

### Rule 5: conservation and velocity bound

- max relative drift of sum(body)+sum(food), all 1500 runs: 6.16e-15; runs above 1e-12: 0
  - F0K0: max drift 2.31e-15; mean sat_frac 8.37e-07; max single-sample sat_frac 1.37e-03
  - F0K3: max drift 2.64e-15; mean sat_frac 1.06e-06; max single-sample sat_frac 1.37e-03
  - F1K0: max drift 6.16e-15; mean sat_frac 4.06e-09; max single-sample sat_frac 1.31e-04
  - F1K3: max drift 5.54e-15; mean sat_frac 1.37e-08; max single-sample sat_frac 1.33e-04

### Foraging (descriptive): gross food eaten over 30,000 steps and end body mass, median (min-max) over seeds

| species | cell | arm | food eaten | end body | Q_30000 = body(end) - body(0) | end blobs |
|---|---|---|---|---|---|---|
| OSCILLIS | F0K0 | treat | 48680.5 (36802.4-63780.1) | 3236.8 (2476.8-4186.6) | 1472.5 (1101.5-1933.4) | 43 |
| OSCILLIS | F0K0 | neutral_plus | 49223.7 (36955.8-64787.3) | 3298.0 (2485.5-4277.5) | 1533.7 (1110.2-2024.3) | 19 |
| OSCILLIS | F0K0 | neutral_minus | 48682.9 (36372.5-63510.9) | 3241.0 (2477.1-4265.0) | 1474.2 (1099.5-2011.8) | 6 |
| OSCILLIS | F0K3 | treat | 48928.1 (36773.0-63955.0) | 3276.5 (2484.0-4206.2) | 1512.2 (1103.9-1953.0) | 31 |
| OSCILLIS | F0K3 | neutral_plus | 49229.3 (36960.7-64765.8) | 3298.2 (2486.5-4280.3) | 1533.8 (1111.2-2027.1) | 20 |
| OSCILLIS | F0K3 | neutral_minus | 48701.9 (36243.5-63485.1) | 3234.8 (2472.2-4255.2) | 1468.0 (1096.9-2002.0) | 7 |
| OSCILLIS | F1K0 | treat | 45800.0 (32660.4-61876.7) | 3204.0 (2406.3-4190.7) | 1440.3 (1026.3-1937.4) | 5 |
| OSCILLIS | F1K0 | neutral_plus | 45259.2 (31924.5-60991.6) | 3267.6 (2472.3-4255.2) | 1503.2 (1092.3-2001.9) | 5 |
| OSCILLIS | F1K0 | neutral_minus | 45756.6 (33231.2-61666.4) | 3086.8 (2360.5-4090.5) | 1330.0 (985.2-1837.2) | 6 |
| OSCILLIS | F1K3 | treat | 46180.0 (32465.6-62031.8) | 3185.5 (2384.6-4152.6) | 1421.2 (1004.5-1899.3) | 8 |
| OSCILLIS | F1K3 | neutral_plus | 45046.1 (31988.6-60809.7) | 3259.2 (2480.7-4253.3) | 1494.9 (1100.6-2000.1) | 5 |
| OSCILLIS | F1K3 | neutral_minus | 45773.8 (33180.8-61722.0) | 3091.5 (2377.1-4096.5) | 1340.1 (994.3-1843.3) | 6 |
| MITOSA | F0K0 | treat | 48565.5 (36807.9-63953.8) | 3312.3 (2532.2-4272.4) | 1546.1 (1156.9-2019.2) | 29 |
| MITOSA | F0K0 | neutral_plus | 48773.1 (36551.5-64241.4) | 3303.1 (2520.8-4289.0) | 1538.8 (1145.5-2035.7) | 17 |
| MITOSA | F0K0 | neutral_minus | 47970.0 (36518.3-62874.3) | 3284.1 (2535.3-4275.4) | 1532.6 (1160.0-2022.2) | 5 |
| MITOSA | F0K3 | treat | 48417.4 (36834.7-63810.5) | 3286.0 (2526.5-4282.9) | 1521.7 (1147.6-2029.7) | 29 |
| MITOSA | F0K3 | neutral_plus | 48908.5 (36819.9-64116.5) | 3306.6 (2521.7-4287.5) | 1542.3 (1146.4-2034.3) | 15 |
| MITOSA | F0K3 | neutral_minus | 47785.3 (36794.5-62770.2) | 3303.2 (2536.0-4275.6) | 1538.9 (1160.7-2022.4) | 5 |
| MITOSA | F1K0 | treat | 44572.8 (32029.2-59768.5) | 3126.9 (2134.4-4096.0) | 1373.8 (759.1-1872.3) | 8 |
| MITOSA | F1K0 | neutral_plus | 44846.4 (31997.0-60150.3) | 3150.2 (2329.5-4152.0) | 1385.9 (954.2-1898.8) | 8 |
| MITOSA | F1K0 | neutral_minus | 44242.4 (32084.0-59394.5) | 3108.4 (2266.7-4096.8) | 1350.1 (891.4-1873.1) | 9 |
| MITOSA | F1K3 | treat | 44680.5 (32399.7-60549.2) | 3110.9 (2292.6-4168.7) | 1357.8 (912.6-1915.4) | 12 |
| MITOSA | F1K3 | neutral_plus | 44776.8 (31923.4-59965.3) | 3156.2 (2317.7-4113.8) | 1389.4 (942.4-1860.5) | 8 |
| MITOSA | F1K3 | neutral_minus | 43919.1 (32269.2-59404.1) | 3083.1 (2351.8-4107.1) | 1343.2 (971.8-1883.4) | 8 |
| VAGRANT | F0K0 | treat | 47713.3 (34453.2-63598.1) | 3166.1 (2332.3-4192.1) | 1409.6 (952.8-1938.8) | 31 |
| VAGRANT | F0K0 | neutral_plus | 47349.9 (35004.6-62842.1) | 3123.7 (2356.3-4169.7) | 1374.5 (981.0-1916.5) | 5 |
| VAGRANT | F0K0 | neutral_minus | 47853.4 (34442.9-63217.8) | 3176.8 (2339.4-4158.1) | 1394.7 (964.1-1904.8) | 22 |
| VAGRANT | F0K3 | treat | 48008.1 (34690.2-63736.6) | 3187.9 (2318.5-4193.5) | 1423.6 (943.2-1940.3) | 33 |
| VAGRANT | F0K3 | neutral_plus | 47343.9 (34958.2-62877.0) | 3125.9 (2362.5-4169.1) | 1373.4 (987.2-1915.8) | 6 |
| VAGRANT | F0K3 | neutral_minus | 47883.3 (34305.5-63069.4) | 3187.7 (2321.6-4141.6) | 1406.1 (946.3-1888.4) | 19 |

Sensing effect on foraging (treat arm, median food eaten, sensing on minus off, same kappa):

- OSCILLIS kappa 0: 45800.0 vs 48680.5 (-2880.5)
- OSCILLIS kappa 3: 46180.0 vs 48928.1 (-2748.1)
- MITOSA kappa 0: 44572.8 vs 48565.5 (-3992.7)
- MITOSA kappa 3: 44680.5 vs 48417.4 (-3736.8)

### Per-run table (treatment arm)

| species | cell | seed | delta | winner | winner-side final share | hybrid end | blobs | food eaten | end body | drift | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| OSCILLIS | F0K0 | 1 | +0.0064 | +u | 0.508 | 1.000 | 52 | 51555.8 | 3397.8 | 2.5e-16 | 16 |
| OSCILLIS | F0K0 | 2 | -0.0231 | -u | 0.528 | 0.568 | 31 | 36802.4 | 2476.8 | 1.7e-15 | 16 |
| OSCILLIS | F0K0 | 3 | +0.0111 | +u | 0.510 | 0.915 | 56 | 45064.8 | 2995.6 | 4.2e-16 | 16 |
| OSCILLIS | F0K0 | 4 | +0.0060 | +u | 0.504 | 0.957 | 52 | 45725.0 | 3046.3 | 5.5e-16 | 16 |
| OSCILLIS | F0K0 | 5 | +0.0045 | +u | 0.507 | 1.000 | 37 | 63055.4 | 4127.1 | 6.1e-16 | 16 |
| OSCILLIS | F0K0 | 6 | -0.0311 | -u | 0.538 | 1.000 | 37 | 60545.0 | 3958.1 | 4.2e-16 | 16 |
| OSCILLIS | F0K0 | 7 | +0.0169 | +u | 0.516 | 1.000 | 36 | 43429.0 | 2899.2 | 4.3e-16 | 16 |
| OSCILLIS | F0K0 | 8 | -0.0235 | -u | 0.524 | 1.000 | 23 | 48247.0 | 3232.4 | 5.1e-16 | 16 |
| OSCILLIS | F0K0 | 9 | -0.0759 | -u | 0.574 | 0.990 | 27 | 56178.3 | 3695.4 | 4.5e-16 | 16 |
| OSCILLIS | F0K0 | 10 | +0.0164 | +u | 0.522 | 1.000 | 40 | 47190.7 | 3173.2 | 6.6e-16 | 16 |
| OSCILLIS | F0K0 | 11 | -0.0354 | -u | 0.530 | 0.462 | 32 | 38929.5 | 2589.7 | 8.0e-16 | 16 |
| OSCILLIS | F0K0 | 12 | +0.0479 | +u | 0.549 | 1.000 | 43 | 50896.0 | 3388.2 | 5.0e-16 | 16 |
| OSCILLIS | F0K0 | 13 | -0.0189 | -u | 0.515 | 1.000 | 36 | 53579.8 | 3570.8 | 5.9e-16 | 16 |
| OSCILLIS | F0K0 | 14 | -0.0265 | -u | 0.526 | 1.000 | 50 | 50354.4 | 3326.0 | 3.8e-16 | 16 |
| OSCILLIS | F0K0 | 15 | +0.0248 | +u | 0.527 | 0.956 | 62 | 46053.2 | 3091.2 | 5.4e-16 | 16 |
| OSCILLIS | F0K0 | 16 | -0.0486 | -u | 0.550 | 0.968 | 37 | 40187.0 | 2746.6 | 1.2e-15 | 16 |
| OSCILLIS | F0K0 | 17 | -0.0096 | -u | 0.506 | 1.000 | 65 | 49507.6 | 3274.5 | 7.7e-16 | 16 |
| OSCILLIS | F0K0 | 18 | -0.0358 | -u | 0.543 | 1.000 | 25 | 56833.0 | 3757.7 | 4.4e-16 | 16 |
| OSCILLIS | F0K0 | 19 | -0.0287 | -u | 0.531 | 0.937 | 21 | 47815.9 | 3162.4 | 7.9e-16 | 16 |
| OSCILLIS | F0K0 | 20 | +0.0154 | +u | 0.514 | 0.968 | 46 | 41064.1 | 2745.4 | 7.5e-16 | 16 |
| OSCILLIS | F0K0 | 21 | -0.0181 | -u | 0.523 | 1.000 | 41 | 55908.1 | 3675.1 | 3.4e-16 | 16 |
| OSCILLIS | F0K0 | 22 | -0.0118 | -u | 0.511 | 0.887 | 47 | 47345.2 | 3118.1 | 4.0e-16 | 16 |
| OSCILLIS | F0K0 | 23 | -0.0555 | -u | 0.552 | 0.751 | 32 | 47409.9 | 3148.1 | 5.3e-16 | 16 |
| OSCILLIS | F0K0 | 24 | -0.0067 | -u | 0.502 | 1.000 | 66 | 57163.6 | 3751.7 | 2.2e-16 | 16 |
| OSCILLIS | F0K0 | 25 | -0.0201 | -u | 0.520 | 1.000 | 40 | 51500.2 | 3458.5 | 3.6e-16 | 16 |
| OSCILLIS | F0K0 | 26 | -0.0225 | -u | 0.523 | 0.829 | 38 | 47931.6 | 3177.5 | 5.3e-16 | 16 |
| OSCILLIS | F0K0 | 27 | -0.0223 | -u | 0.531 | 1.000 | 30 | 50495.3 | 3358.3 | 5.0e-16 | 16 |
| OSCILLIS | F0K0 | 28 | -0.0377 | -u | 0.539 | 0.684 | 34 | 39935.5 | 2666.8 | 4.7e-16 | 16 |
| OSCILLIS | F0K0 | 29 | -0.0467 | -u | 0.538 | 1.000 | 43 | 50142.9 | 3378.2 | 7.4e-16 | 16 |
| OSCILLIS | F0K0 | 30 | -0.0074 | -u | 0.510 | 0.951 | 63 | 48984.1 | 3241.3 | 6.5e-16 | 16 |
| OSCILLIS | F0K0 | 31 | -0.0400 | -u | 0.541 | 0.752 | 49 | 42642.5 | 2835.7 | 1.0e-15 | 16 |
| OSCILLIS | F0K0 | 32 | +0.0007 | +u | 0.505 | 1.000 | 59 | 47578.5 | 3152.6 | 5.3e-16 | 16 |
| OSCILLIS | F0K0 | 33 | -0.0121 | -u | 0.517 | 1.000 | 63 | 59346.4 | 3891.7 | 4.3e-16 | 16 |
| OSCILLIS | F0K0 | 34 | +0.0143 | +u | 0.516 | 0.891 | 57 | 42345.7 | 2830.9 | 4.4e-16 | 16 |
| OSCILLIS | F0K0 | 35 | -0.0195 | -u | 0.522 | 1.000 | 39 | 54441.1 | 3581.9 | 3.5e-16 | 16 |
| OSCILLIS | F0K0 | 36 | -0.0128 | -u | 0.513 | 1.000 | 54 | 52280.9 | 3455.4 | 2.4e-16 | 16 |
| OSCILLIS | F0K0 | 37 | +0.0375 | +u | 0.540 | 1.000 | 58 | 63780.1 | 4186.6 | 8.1e-16 | 16 |
| OSCILLIS | F0K0 | 38 | -0.0166 | -u | 0.510 | 0.663 | 30 | 37573.9 | 2510.8 | 6.5e-16 | 16 |
| OSCILLIS | F0K0 | 39 | +0.0339 | +u | 0.538 | 1.000 | 58 | 58355.9 | 3851.7 | 2.2e-16 | 16 |
| OSCILLIS | F0K0 | 40 | +0.0216 | +u | 0.518 | 1.000 | 51 | 59992.5 | 3954.5 | 4.3e-16 | 16 |
| OSCILLIS | F0K0 | 41 | -0.0323 | -u | 0.532 | 0.981 | 33 | 47053.8 | 3113.3 | 6.7e-16 | 16 |
| OSCILLIS | F0K0 | 42 | -0.0126 | -u | 0.511 | 1.000 | 45 | 54805.6 | 3631.5 | 3.5e-16 | 16 |
| OSCILLIS | F0K0 | 43 | -0.0424 | -u | 0.543 | 1.000 | 44 | 53624.8 | 3559.6 | 3.5e-16 | 16 |
| OSCILLIS | F0K0 | 44 | +0.0251 | +u | 0.521 | 0.820 | 66 | 37212.9 | 2493.0 | 4.9e-16 | 16 |
| OSCILLIS | F0K0 | 45 | -0.0164 | -u | 0.519 | 1.000 | 63 | 48377.0 | 3193.4 | 5.2e-16 | 16 |
| OSCILLIS | F0K0 | 46 | -0.0310 | -u | 0.526 | 0.830 | 56 | 50921.2 | 3357.5 | 3.8e-16 | 16 |
| OSCILLIS | F0K0 | 47 | +0.0108 | +u | 0.507 | 0.930 | 38 | 44984.5 | 3009.7 | 5.5e-16 | 16 |
| OSCILLIS | F0K0 | 48 | -0.0018 | -u | 0.503 | 0.885 | 34 | 39629.0 | 2654.2 | 1.1e-15 | 16 |
| OSCILLIS | F0K0 | 49 | +0.0212 | +u | 0.520 | 0.798 | 43 | 45952.6 | 3082.9 | 4.1e-16 | 16 |
| OSCILLIS | F0K0 | 50 | +0.0210 | +u | 0.521 | 1.000 | 53 | 52633.0 | 3494.5 | 6.0e-16 | 16 |
| OSCILLIS | F0K3 | 1 | -0.0097 | -u | 0.509 | 0.000 | 24 | 51959.2 | 3448.6 | 6.1e-16 | 18 |
| OSCILLIS | F0K3 | 2 | +0.0225 | +u | 0.517 | 0.000 | 29 | 36773.0 | 2488.5 | 1.2e-15 | 18 |
| OSCILLIS | F0K3 | 3 | +0.0687 | +u | 0.568 | 0.492 | 77 | 45126.7 | 2994.2 | 8.4e-16 | 18 |
| OSCILLIS | F0K3 | 4 | +0.0162 | +u | 0.514 | 0.065 | 28 | 45829.0 | 3059.3 | 5.5e-16 | 18 |
| OSCILLIS | F0K3 | 5 | -0.0171 | -u | 0.515 | 1.000 | 42 | 63274.6 | 4161.9 | 4.1e-16 | 18 |
| OSCILLIS | F0K3 | 6 | -0.0379 | -u | 0.545 | 0.026 | 26 | 61017.6 | 4016.8 | 6.4e-16 | 18 |
| OSCILLIS | F0K3 | 7 | +0.0151 | +u | 0.514 | 0.000 | 42 | 43501.4 | 2906.6 | 7.2e-16 | 18 |
| OSCILLIS | F0K3 | 8 | -0.1237 | -u | 0.624 | 0.000 | 17 | 48730.3 | 3289.0 | 5.1e-16 | 18 |
| OSCILLIS | F0K3 | 9 | -0.1304 | -u | 0.628 | 0.000 | 18 | 56587.9 | 3784.2 | 6.8e-16 | 18 |
| OSCILLIS | F0K3 | 10 | -0.0563 | -u | 0.550 | 0.372 | 37 | 47059.4 | 3188.8 | 5.3e-16 | 18 |
| OSCILLIS | F0K3 | 11 | -0.0031 | -u | 0.497 | 0.000 | 38 | 38870.9 | 2588.7 | 4.8e-16 | 18 |
| OSCILLIS | F0K3 | 12 | +0.0059 | +u | 0.507 | 0.890 | 64 | 50993.4 | 3402.3 | 2.5e-16 | 18 |
| OSCILLIS | F0K3 | 13 | -0.0469 | -u | 0.543 | 0.000 | 22 | 54175.5 | 3620.4 | 4.7e-16 | 18 |
| OSCILLIS | F0K3 | 14 | -0.0350 | -u | 0.535 | 0.019 | 27 | 50752.0 | 3374.1 | 7.5e-16 | 18 |
| OSCILLIS | F0K3 | 15 | +0.0191 | +u | 0.522 | 0.362 | 48 | 46092.3 | 3092.1 | 4.1e-16 | 18 |
| OSCILLIS | F0K3 | 16 | -0.0858 | -u | 0.587 | 0.000 | 27 | 39987.7 | 2752.6 | 1.4e-15 | 18 |
| OSCILLIS | F0K3 | 17 | -0.0163 | -u | 0.512 | 0.288 | 46 | 49694.5 | 3295.7 | 6.4e-16 | 18 |
| OSCILLIS | F0K3 | 18 | -0.1409 | -u | 0.648 | 0.023 | 26 | 57302.4 | 3827.2 | 4.4e-16 | 18 |
| OSCILLIS | F0K3 | 19 | -0.0315 | -u | 0.533 | 0.000 | 21 | 47906.2 | 3183.7 | 6.6e-16 | 18 |
| OSCILLIS | F0K3 | 20 | +0.0122 | +u | 0.511 | 0.339 | 42 | 41140.9 | 2745.9 | 3.0e-16 | 18 |
| OSCILLIS | F0K3 | 21 | -0.0344 | -u | 0.539 | 0.000 | 25 | 56186.1 | 3707.8 | 4.6e-16 | 18 |
| OSCILLIS | F0K3 | 22 | +0.0365 | +u | 0.538 | 0.000 | 33 | 47460.7 | 3145.9 | 5.3e-16 | 18 |
| OSCILLIS | F0K3 | 23 | -0.0611 | -u | 0.557 | 0.000 | 34 | 47517.3 | 3158.2 | 5.3e-16 | 18 |