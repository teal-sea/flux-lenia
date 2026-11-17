# Campaign part A summary (scripts/campaign_harness_summary.py; JSON only, no simulation)

## Part 1: same-host control and determinism

45 box-control runs, 3 repeats, 45 citadel-control runs, 45 step 2 repulsion runs.

### (a) Determinism (repeat on the same box minus first run)

| run | |d final share_A| | |d final hybrid_frac| | first sample with |d share_A| > 1e-12 (step) | wall s first / repeat |
|---|---|---|---|---|
| OSCILLIS s1 treat | 0.000e+00 | 0.000e+00 | none | 2750 / 1347 |
| MITOSA s1 treat | 0.000e+00 | 0.000e+00 | none | 2739 / 1348 |
| VAGRANT s1 treat | 0.000e+00 | 0.000e+00 | none | 2777 / 1355 |

**Verdict (a): deterministic** (3 repeats compared).

### (b) Host effect: |box - citadel| per run, 45 runs

| set | measure | n | median | max | agree 1e-12 | agree 1e-6 | agree 1e-2 |
|---|---|---|---|---|---|---|---|
| all | final share_A | 45 | 6.568e-03 | 5.304e-02 | 0 | 0 | 31 |
| all | final hybrid_frac | 45 | 1.416e-02 | 3.223e-01 | 11 | 11 | 19 |
| OSCILLIS | final share_A | 15 | 5.985e-03 | 2.007e-02 | 0 | 0 | 12 |
| OSCILLIS | final hybrid_frac | 15 | 1.875e-03 | 5.539e-02 | 5 | 5 | 8 |
| MITOSA | final share_A | 15 | 8.300e-03 | 3.477e-02 | 0 | 0 | 8 |
| MITOSA | final hybrid_frac | 15 | 1.482e-02 | 3.223e-01 | 5 | 5 | 6 |
| VAGRANT | final share_A | 15 | 5.107e-03 | 5.304e-02 | 0 | 0 | 11 |
| VAGRANT | final hybrid_frac | 15 | 1.792e-02 | 3.221e-01 | 1 | 1 | 5 |

At step 300 (series index 3): median |d share_A| 6.79e-11, max 6.87e-05.
First sample at which box and citadel differ by more than 1e-12 in share_A: median 300 steps (min 100, max 800); never: 0 of 45.

### (c) Step 2 neutral-arm check: repulsion (kappa 3) minus control, final hybrid fraction, 10 pairs per species

| species | control used | n | mean diff | SE | mean/SE | flag |
|---|---|---|---|---|---|---|
| OSCILLIS | box control (this campaign) | 10 | +0.0017 | 0.0165 | +0.10 | ok |
| MITOSA | box control (this campaign) | 10 | -0.0426 | 0.0426 | -1.00 | ok |
| VAGRANT | box control (this campaign) | 10 | +0.0267 | 0.0374 | +0.71 | ok |
| OSCILLIS | citadel control (repeats step 2) | 10 | +0.0021 | 0.0196 | +0.10 | ok |
| MITOSA | citadel control (repeats step 2) | 10 | -0.0313 | 0.0250 | -1.25 | ok |
| VAGRANT | citadel control (repeats step 2) | 10 | +0.0133 | 0.0062 | +2.15 | exceeds 2 SE |
| OSCILLIS | box minus citadel, same runs | 10 | -0.0003 | 0.0062 | -0.05 | ok |
| MITOSA | box minus citadel, same runs | 10 | -0.0113 | 0.0191 | -0.59 | ok |
| VAGRANT | box minus citadel, same runs | 10 | +0.0134 | 0.0395 | +0.34 | ok |

**Verdict (c), step 2 flag: cleared (all species within 2 SE).** (Three species were tested, so about 14% chance of one exceedance by chance with no leak.)

## Part 2: kappa robustness (kappa 1 and 10, seeds 1 to 20)

- kappa 1: 180 of 180 runs present
- kappa 10: 180 of 180 runs present

### kappa 1

**Distinctness (rule 1 matched for seeds 1-5; descriptive for seeds 6-20)**

| species | seeds 1-5 control median | treat median (seeds 1-5) | seeds below matched control | rule 1 verdict | seeds 6-20 treat hybrid: min / q1 / median / q3 / max | seeds 6-20 below control median | distinct (unmatched) | all 20: median | box-control verdict (secondary) |
|---|---|---|---|---|---|---|---|---|---|
| OSCILLIS | 0.939 | 0.915 | 3 of 5 | partial | 0.263 / 0.834 / 0.965 / 1.000 / 1.000 (n=15) | 7 of 15 | no | 0.940 | no effect |
| MITOSA | 0.921 | 0.448 | 4 of 5 | distinct | 0.020 / 0.278 / 0.758 / 0.996 / 1.000 (n=15) | 9 of 15 | no | 0.699 | distinct |
| VAGRANT | 0.502 | 0.035 | 5 of 5 | distinct | 0.000 / 0.001 / 0.046 / 0.074 / 0.318 (n=15) | 15 of 15 | yes | 0.041 | distinct |

**Selection (rule 2 scaled to 20 seeds: 16 of 20 outside E)**

| species | E (max of 40 neutral) | treat out of E | winners | max winner share | verdict | E95 (secondary) | out of E95 | verdict at E95 (secondary) | treat deltas (20 seeds) |
|---|---|---|---|---|---|---|---|---|---|
| OSCILLIS | 0.0459 | 4 of 20 | +u 0 / -u 4 | 0.591 | no selection detected | 0.0173 | 12 of 20 | no selection detected (+u 2 / -u 10) | -0.02 -0.01 +0.02 -0.00 -0.00 -0.03 -0.01 -0.09 -0.09 -0.04 -0.03 +0.04 -0.00 -0.04 +0.03 -0.06 -0.01 -0.07 -0.05 -0.00 |
| MITOSA | 0.0604 | 2 of 20 | +u 2 / -u 0 | 0.588 | no selection detected | 0.0507 | 4 of 20 | no selection detected (+u 3 / -u 1) | +0.04 +0.02 -0.00 +0.02 +0.08 +0.01 +0.04 +0.01 +0.09 -0.03 -0.05 +0.03 +0.05 +0.06 -0.00 +0.05 +0.04 +0.05 +0.03 -0.01 |
| VAGRANT | 0.0477 | 8 of 20 | +u 8 / -u 0 | 0.703 | no selection detected | 0.0259 | 12 of 20 | no selection detected (+u 12 / -u 0) | +0.05 +0.06 +0.20 +0.05 +0.01 +0.04 +0.03 +0.01 +0.03 -0.01 +0.09 +0.01 -0.00 +0.04 -0.01 +0.03 +0.12 +0.01 +0.06 +0.20 |

**Saturation and conservation**

| species | runs | runs with max-over-samples sat_frac > 1e-2 | runs with mean sat_frac > 1e-2 | largest sat_frac in any sample | mean of per-run means | max drift sum(body)+sum(food) | wall s median / max |
|---|---|---|---|---|---|---|---|
| OSCILLIS | 60 | 0 | 0 | 1.05e-03 | 1.89e-06 | 3.02e-15 | 1914 / 3100 |
| MITOSA | 60 | 0 | 0 | 3.57e-04 | 3.53e-07 | 2.12e-15 | 1896 / 3090 |
| VAGRANT | 60 | 0 | 0 | 0.00e+00 | 0.00e+00 | 1.80e-15 | 1904 / 3111 |

**Saturation flag for kappa 1: not flagged.**

### kappa 10

**Distinctness (rule 1 matched for seeds 1-5; descriptive for seeds 6-20)**

| species | seeds 1-5 control median | treat median (seeds 1-5) | seeds below matched control | rule 1 verdict | seeds 6-20 treat hybrid: min / q1 / median / q3 / max | seeds 6-20 below control median | distinct (unmatched) | all 20: median | box-control verdict (secondary) |
|---|---|---|---|---|---|---|---|---|---|
| OSCILLIS | 0.939 | 0.000 | 5 of 5 | distinct | 0.000 / 0.000 / 0.000 / 0.000 / 0.000 (n=15) | 15 of 15 | yes | 0.000 | distinct |
| MITOSA | 0.921 | 0.000 | 5 of 5 | distinct | 0.000 / 0.000 / 0.000 / 0.000 / 0.001 (n=15) | 15 of 15 | yes | 0.000 | distinct |
| VAGRANT | 0.502 | 0.000 | 5 of 5 | distinct | 0.000 / 0.000 / 0.000 / 0.000 / 0.000 (n=15) | 15 of 15 | yes | 0.000 | distinct |

**Selection (rule 2 scaled to 20 seeds: 16 of 20 outside E)**

| species | E (max of 40 neutral) | treat out of E | winners | max winner share | verdict | E95 (secondary) | out of E95 | verdict at E95 (secondary) | treat deltas (20 seeds) |
|---|---|---|---|---|---|---|---|---|---|
| OSCILLIS | 0.0363 | 11 of 20 | +u 5 / -u 6 | 0.640 | no selection detected | 0.0212 | 15 of 20 | no selection detected (+u 7 / -u 8) | +0.01 +0.03 +0.12 +0.04 +0.01 -0.03 +0.03 -0.12 -0.14 -0.05 +0.01 +0.07 -0.05 -0.01 +0.07 -0.12 +0.01 -0.12 -0.03 +0.05 |
| MITOSA | 0.0778 | 3 of 20 | +u 3 / -u 0 | 0.641 | no selection detected | 0.0501 | 5 of 20 | no selection detected (+u 5 / -u 0) | +0.05 +0.05 +0.00 -0.01 +0.08 -0.01 +0.07 +0.14 +0.04 -0.03 -0.02 -0.04 +0.06 +0.02 +0.02 +0.03 +0.02 +0.08 +0.02 +0.02 |
| VAGRANT | 0.0376 | 9 of 20 | +u 9 / -u 0 | 0.685 | no selection detected | 0.0242 | 9 of 20 | no selection detected (+u 9 / -u 0) | +0.01 +0.05 +0.19 +0.02 +0.01 +0.06 +0.07 -0.00 +0.02 -0.02 +0.07 -0.01 +0.00 +0.05 -0.01 +0.01 +0.07 +0.02 +0.04 +0.14 |

**Saturation and conservation**

| species | runs | runs with max-over-samples sat_frac > 1e-2 | runs with mean sat_frac > 1e-2 | largest sat_frac in any sample | mean of per-run means | max drift sum(body)+sum(food) | wall s median / max |
|---|---|---|---|---|---|---|---|
| OSCILLIS | 60 | 0 | 0 | 1.05e-03 | 1.82e-06 | 3.04e-15 | 1888 / 3078 |
| MITOSA | 60 | 0 | 0 | 1.05e-03 | 4.87e-06 | 2.05e-15 | 1892 / 3085 |
| VAGRANT | 60 | 0 | 0 | 3.54e-04 | 1.76e-07 | 2.10e-15 | 1896 / 3099 |

**Saturation flag for kappa 10: not flagged.**

### Dose-response, seeds 1-5, treatment, median final hybrid fraction (per species)

| species | kappa 0 (citadel control) | kappa 0 (box control) | kappa 1 | kappa 3 (step 2) | kappa 10 |
|---|---|---|---|---|---|
| OSCILLIS | 0.939 | 0.940 | 0.915 | 0.313 | 0.000 |
| MITOSA | 0.921 | 1.000 | 0.448 | 0.000 | 0.000 |
| VAGRANT | 0.502 | 0.571 | 0.035 | 0.000 | 0.000 |

## Part 3: horizon, 300,000 steps, kappa 3

45 of 45 runs present.

### Per run

| species | arm | seed | A start | d30 | d300 | class (b) | winner share end | winner share peak | h30 | h300 | (c) | blobs end | max drift | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| OSCILLIS | treat | 1 | 0.501 | -0.018 | -0.456 | grows | 0.955 | 0.955 | 0.313 | 0.000 | holds | 1 | 1.4e-14 | 6415 |
| OSCILLIS | treat | 2 | 0.495 | +0.003 | -0.428 | reverses | 0.933 | 0.940 | 0.000 | 0.000 | holds | 26 | 1.9e-14 | 13600 |
| OSCILLIS | treat | 3 | 0.499 | +0.073 | -0.343 | reverses | 0.843 | 0.852 | 0.466 | 0.870 | erodes | 24 | 6.7e-15 | 6486 |
| OSCILLIS | treat | 4 | 0.498 | +0.021 | -0.386 | reverses | 0.888 | 0.898 | 0.103 | 0.000 | holds | 18 | 2.1e-14 | 13601 |
| OSCILLIS | treat | 5 | 0.502 | -0.016 | -0.200 | grows | 0.698 | 0.724 | 0.955 | 1.000 | holds | 4 | 9.2e-15 | 6089 |
| OSCILLIS | neutral_plus | 1 | 0.501 | -0.000 | -0.007 | saturated | 0.506 | 0.506 | 0.949 | 1.000 | erodes | 15 | 2.1e-14 | 11433 |
| OSCILLIS | neutral_plus | 2 | 0.495 | -0.005 | -0.010 | saturated | 0.515 | 0.516 | 0.740 | 1.000 | erodes | 8 | 2.0e-14 | 13535 |
| OSCILLIS | neutral_plus | 3 | 0.499 | +0.003 | +0.018 | saturated | 0.517 | 0.518 | 0.762 | 1.000 | erodes | 17 | 2.6e-14 | 11464 |
| OSCILLIS | neutral_plus | 4 | 0.498 | +0.007 | +0.026 | saturated | 0.524 | 0.524 | 0.959 | 1.000 | holds | 37 | 2.6e-14 | 13545 |
| OSCILLIS | neutral_plus | 5 | 0.502 | -0.001 | -0.001 | saturated | 0.499 | 0.500 | 1.000 | 1.000 | holds | 17 | 1.7e-14 | 11368 |
| OSCILLIS | neutral_minus | 1 | 0.501 | -0.006 | +0.005 | saturated | 0.506 | 0.507 | 1.000 | 1.000 | holds | 1 | 1.1e-14 | 11392 |
| OSCILLIS | neutral_minus | 2 | 0.495 | -0.014 | -0.003 | saturated | 0.508 | 0.526 | 0.763 | 0.998 | erodes | 60 | 2.1e-14 | 13569 |
| OSCILLIS | neutral_minus | 3 | 0.499 | +0.006 | +0.005 | saturated | 0.505 | 0.506 | 1.000 | 1.000 | holds | 74 | 1.6e-14 | 11419 |
| OSCILLIS | neutral_minus | 4 | 0.498 | +0.006 | -0.012 | saturated | 0.514 | 0.514 | 0.899 | 1.000 | erodes | 2 | 1.7e-14 | 13571 |
| OSCILLIS | neutral_minus | 5 | 0.502 | +0.004 | +0.037 | saturated | 0.540 | 0.544 | 1.000 | 1.000 | holds | 1 | 1.1e-14 | 11427 |
| MITOSA | treat | 1 | 0.501 | +0.025 | -0.067 | reverses | 0.566 | 0.568 | 0.000 | 0.000 | holds | 18 | 4.7e-15 | 13600 |
| MITOSA | treat | 2 | 0.495 | +0.045 | -0.032 | reverses | 0.537 | 0.539 | 0.000 | 0.000 | holds | 25 | 3.6e-15 | 6416 |
| MITOSA | treat | 3 | 0.499 | +0.005 | -0.115 | reverses | 0.616 | 0.620 | 0.000 | 0.000 | holds | 32 | 9.1e-15 | 13611 |
| MITOSA | treat | 4 | 0.498 | -0.019 | -0.086 | grows | 0.588 | 0.592 | 0.000 | 0.000 | holds | 21 | 6.7e-15 | 6328 |
| MITOSA | treat | 5 | 0.502 | +0.089 | -0.048 | reverses | 0.546 | 0.549 | 0.001 | 0.000 | holds | 22 | 1.4e-14 | 13616 |
| MITOSA | neutral_plus | 1 | 0.501 | -0.023 | -0.026 | saturated | 0.525 | 0.525 | 1.000 | 1.000 | holds | 21 | 3.8e-14 | 13545 |
| MITOSA | neutral_plus | 2 | 0.495 | -0.018 | -0.020 | saturated | 0.525 | 0.530 | 1.000 | 1.000 | holds | 11 | 3.6e-14 | 11460 |
| MITOSA | neutral_plus | 3 | 0.499 | +0.010 | +0.005 | saturated | 0.505 | 0.511 | 1.000 | 1.000 | holds | 27 | 4.6e-14 | 13530 |
| MITOSA | neutral_plus | 4 | 0.498 | -0.008 | +0.005 | saturated | 0.503 | 0.503 | 1.000 | 1.000 | holds | 23 | 3.3e-14 | 11406 |
| MITOSA | neutral_plus | 5 | 0.502 | -0.000 | -0.001 | saturated | 0.499 | 0.501 | 0.956 | 1.000 | holds | 21 | 4.0e-14 | 13527 |
| MITOSA | neutral_minus | 1 | 0.501 | -0.030 | -0.030 | saturated | 0.529 | 0.529 | 1.000 | 1.000 | holds | 13 | 1.0e-14 | 13569 |
| MITOSA | neutral_minus | 2 | 0.495 | +0.075 | +0.074 | saturated | 0.568 | 0.570 | 0.611 | 1.000 | erodes | 7 | 1.3e-14 | 11456 |
| MITOSA | neutral_minus | 3 | 0.499 | -0.024 | -0.025 | saturated | 0.525 | 0.526 | 0.648 | 1.000 | erodes | 7 | 1.0e-14 | 13568 |
| MITOSA | neutral_minus | 4 | 0.498 | -0.000 | -0.000 | saturated | 0.502 | 0.502 | 0.912 | 1.000 | erodes | 4 | 6.7e-15 | 11458 |
| MITOSA | neutral_minus | 5 | 0.502 | +0.030 | +0.030 | saturated | 0.533 | 0.533 | 1.000 | 1.000 | holds | 4 | 1.2e-14 | 13562 |
| VAGRANT | treat | 1 | 0.501 | +0.050 | -0.024 | reverses | 0.523 | 0.551 | 0.000 | 0.000 | holds | 3 | 2.3e-14 | 6410 |
| VAGRANT | treat | 2 | 0.495 | +0.074 | -0.495 | reverses | 1.000 | 1.000 | 0.000 | 0.000 | holds | 1 | 7.6e-15 | 13574 |
| VAGRANT | treat | 3 | 0.499 | +0.198 | -0.245 | reverses | 0.746 | 0.816 | 0.000 | 0.000 | holds | 4 | 1.2e-14 | 6357 |
| VAGRANT | treat | 4 | 0.498 | +0.026 | -0.035 | reverses | 0.537 | 0.549 | 0.000 | 0.000 | holds | 2 | 5.2e-15 | 13575 |
| VAGRANT | treat | 5 | 0.502 | +0.008 | -0.098 | reverses | 0.596 | 0.610 | 0.000 | 0.000 | holds | 3 | 4.3e-15 | 6338 |
| VAGRANT | neutral_plus | 1 | 0.501 | -0.015 | -0.080 | grows | 0.579 | 0.580 | 0.762 | 0.802 | holds | 22 | 9.1e-15 | 11405 |
| VAGRANT | neutral_plus | 2 | 0.495 | +0.033 | +0.354 | grows | 0.849 | 0.865 | 0.520 | 0.248 | holds | 5 | 3.6e-15 | 13475 |
| VAGRANT | neutral_plus | 3 | 0.499 | +0.022 | +0.264 | grows | 0.763 | 0.777 | 0.705 | 0.541 | holds | 5 | 1.1e-15 | 11391 |
| VAGRANT | neutral_plus | 4 | 0.498 | +0.002 | +0.002 | saturated | 0.500 | 0.503 | 0.577 | 0.000 | holds | 2 | 7.5e-15 | 13473 |
| VAGRANT | neutral_plus | 5 | 0.502 | -0.007 | -0.005 | saturated | 0.503 | 0.510 | 0.609 | 0.130 | holds | 7 | 6.1e-15 | 11408 |
| VAGRANT | neutral_minus | 1 | 0.501 | +0.009 | +0.007 | saturated | 0.508 | 0.510 | 1.000 | 1.000 | holds | 1 | 2.0e-15 | 11434 |
| VAGRANT | neutral_minus | 2 | 0.495 | +0.001 | -0.002 | saturated | 0.507 | 0.508 | 0.346 | 0.000 | holds | 2 | 1.9e-14 | 13547 |
| VAGRANT | neutral_minus | 3 | 0.499 | +0.020 | +0.009 | saturated | 0.508 | 0.521 | 1.000 | 1.000 | holds | 1 | 6.6e-15 | 11395 |
| VAGRANT | neutral_minus | 4 | 0.498 | +0.012 | +0.020 | saturated | 0.518 | 0.518 | 0.818 | 1.000 | erodes | 4 | 1.6e-14 | 13573 |
| VAGRANT | neutral_minus | 5 | 0.502 | -0.004 | -0.005 | saturated | 0.503 | 0.504 | 1.000 | 1.000 | holds | 4 | 9.2e-15 | 11459 |

### (a) Takeover

| species | treat runs with winner share end >= 0.90 | treat runs with winner share >= 0.90 at any sample | neutral runs (of 10) with >= 0.90 at any sample | max winner share end (treat) |
|---|---|---|---|---|
| OSCILLIS | 2 of 5 | 2 of 5 | 0 of 10 | 0.955 |
| MITOSA | 0 of 5 | 0 of 5 | 0 of 10 | 0.616 |
| VAGRANT | 1 of 5 | 1 of 5 | 0 of 10 | 1.000 |

**Verdict (a): takeover appears** (any treatment run with winner share >= 0.90 at step 300,000).

### (b) Does the share keep moving (|d300 - d30| <= 0.05 saturated)

| species | arm | saturated | grows | reverses | shrinks | median |d300| - |d30| | median |d30| | median |d300| |
|---|---|---|---|---|---|---|---|---|
| OSCILLIS | treat | 0 | 2 | 3 | 0 | +0.365 | 0.018 | 0.386 |
| OSCILLIS | neutral (10) | 10 | 0 | 0 | 0 | +0.006 | 0.006 | 0.009 |
| MITOSA | treat | 0 | 1 | 4 | 0 | +0.042 | 0.025 | 0.067 |
| MITOSA | neutral (10) | 10 | 0 | 0 | 0 | +0.000 | 0.021 | 0.022 |
| VAGRANT | treat | 0 | 0 | 5 | 0 | +0.047 | 0.050 | 0.098 |
| VAGRANT | neutral (10) | 7 | 3 | 0 | 0 | +0.001 | 0.011 | 0.008 |

### (c) Distinctness at 300,000 steps

| species | arm | median h30 | median h300 | holds | erodes | rule 1 at 300k vs 30k citadel control (treat) |
|---|---|---|---|---|---|---|
| OSCILLIS | treat | 0.313 | 0.000 | 4 | 1 | distinct (median 0.000 vs control 0.939, 5 of 5 seeds below) |
| OSCILLIS | neutral (10) | 0.954 | 1.000 | 5 | 5 |  |
| MITOSA | treat | 0.000 | 0.000 | 5 | 0 | distinct (median 0.000 vs control 0.921, 5 of 5 seeds below) |
| MITOSA | neutral (10) | 1.000 | 1.000 | 7 | 3 |  |
| VAGRANT | treat | 0.000 | 0.000 | 5 | 0 | distinct (median 0.000 vs control 0.502, 5 of 5 seeds below) |
| VAGRANT | neutral (10) | 0.733 | 0.672 | 9 | 1 |  |

### (d) Selection at 300,000 steps (rule 2, 4 of 5 bar, E from 10 neutral runs)

| species | E (max |d300| of 10 neutral) | treat out of E | winners | max winner share | verdict | treat d300 (seeds 1-5) | E at 30k (same neutral runs, d30) |
|---|---|---|---|---|---|---|---|
| OSCILLIS | 0.0375 | 5 of 5 | +u 0 / -u 5 | 0.955 | selection | -0.456 -0.428 -0.343 -0.386 -0.200 | 0.0138 |
| MITOSA | 0.0735 | 2 of 5 | +u 0 / -u 2 | 0.616 | no selection detected | -0.067 -0.032 -0.115 -0.086 -0.048 | 0.0752 |
| VAGRANT | 0.3543 | 1 of 5 | +u 0 / -u 1 | 1.000 | no selection detected | -0.024 -0.495 -0.245 -0.035 -0.098 | 0.0329 |

### (e) Conservation, saturation, wall time

- max relative drift of sum(body)+sum(food), 45 runs: 4.61e-14 (median 1.16e-14)
- wall seconds per run: median 11460, min 6089, max 13616
- saturation (max over samples), largest over runs 5.36e-04; runs above 1e-2: 0

### Trajectories (treatment runs): A share and hybrid fraction at steps 0, 30k, 100k, 200k, 300k

| species | seed | share_A | hybrid |
|---|---|---|---|
| OSCILLIS | 1 | 0.501 / 0.481 / 0.338 / 0.130 / 0.045 | 0.000 / 0.313 / 0.353 / 0.106 / 0.000 |
| OSCILLIS | 2 | 0.495 / 0.497 / 0.295 / 0.142 / 0.060 | 0.000 / 0.000 / 0.000 / 0.000 / 0.000 |
| OSCILLIS | 3 | 0.499 / 0.573 / 0.471 / 0.244 / 0.148 | 0.000 / 0.466 / 0.699 / 0.581 / 0.870 |
| OSCILLIS | 4 | 0.498 / 0.518 / 0.385 / 0.207 / 0.102 | 0.000 / 0.103 / 0.000 / 0.000 / 0.000 |
| OSCILLIS | 5 | 0.502 / 0.483 / 0.294 / 0.288 / 0.306 | 0.000 / 0.955 / 1.000 / 1.000 / 1.000 |
| MITOSA | 1 | 0.501 / 0.526 / 0.502 / 0.456 / 0.432 | 0.000 / 0.000 / 0.000 / 0.000 / 0.000 |
| MITOSA | 2 | 0.495 / 0.540 / 0.524 / 0.481 / 0.461 | 0.000 / 0.000 / 0.000 / 0.000 / 0.000 |
| MITOSA | 3 | 0.499 / 0.504 / 0.477 / 0.430 / 0.380 | 0.000 / 0.000 / 0.000 / 0.000 / 0.000 |
| MITOSA | 4 | 0.498 / 0.477 / 0.449 / 0.421 / 0.408 | 0.000 / 0.000 / 0.000 / 0.000 / 0.000 |
| MITOSA | 5 | 0.502 / 0.592 / 0.547 / 0.496 / 0.451 | 0.000 / 0.001 / 0.000 / 0.000 / 0.000 |
| VAGRANT | 1 | 0.501 / 0.553 / 0.742 / 0.611 / 0.449 | 0.000 / 0.000 / 0.000 / 0.000 / 0.000 |
| VAGRANT | 2 | 0.495 / 0.572 / 0.443 / 0.031 / 0.000 | 0.000 / 0.000 / 0.000 / 0.000 / 0.000 |
| VAGRANT | 3 | 0.499 / 0.703 / 0.673 / 0.485 / 0.184 | 0.000 / 0.000 / 0.000 / 0.000 / 0.000 |
| VAGRANT | 4 | 0.498 / 0.523 / 0.473 / 0.466 / 0.462 | 0.000 / 0.000 / 0.000 / 0.000 / 0.000 |
| VAGRANT | 5 | 0.502 / 0.511 / 0.584 / 0.533 / 0.390 | 0.000 / 0.000 / 0.000 / 0.000 / 0.000 |

