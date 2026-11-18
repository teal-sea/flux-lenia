# Horizon 300k summary

Source: `outputs/horizon300k_20261117` (scripts/horizon300k_summary.py; JSON only, no simulation). Rules: docs/HORIZON-300K-GPU-2026-11-16.md rules 1-7. Expected per species x cell: 50 treatment, 100 neutral runs. Selection bar scaled to the seeds present: need = ceil(0.8 x treatment seeds present) (= 40 at 50). Any verdict computed on fewer than 50 treatment seeds or 100 neutral runs is labelled PARTIAL.

Runs read: **900**; duplicates of one cell/arm/seed (last kept): 0; unreadable files skipped: 0.

## Counts present vs expected

Expected total 900 (3 species x 2 cells x 50 seeds x 3 arms); present 900.

| species | cell | treat | neutral_plus | neutral_minus | total / expected |
|---|---|---|---|---|---|
| MITOSA | fs0/k3 | 50 / 50 | 50 / 50 | 50 / 50 | 150 / 150 |
| MITOSA | fs10/k3 | 50 / 50 | 50 / 50 | 50 / 50 | 150 / 150 |
| OSCILLIS | fs0/k3 | 50 / 50 | 50 / 50 | 50 / 50 | 150 / 150 |
| OSCILLIS | fs10/k3 | 50 / 50 | 50 / 50 | 50 / 50 | 150 / 150 |
| VAGRANT | fs0/k3 | 50 / 50 | 50 / 50 | 50 / 50 | 150 / 150 |
| VAGRANT | fs10/k3 | 50 / 50 | 50 / 50 | 50 / 50 | 150 / 150 |

Wall seconds per run: min 221, median 375, max 19902 (n=900).

## Rule 1: takeover frequency

Treatment: winner share at the end >= 0.90, exact (Clopper-Pearson) 95% interval. Neutral: either lineage reaches >= 0.90 at any sample. Takeover occurs if the treatment count exceeds the neutral count and two-sided Fisher exact p < 0.05 on the 2x2 of counts.

| species | cell | treat takeover | frequency | exact 95% | neutral >= 0.90 at any sample | neutral frequency | Fisher p | takeover occurs | status |
|---|---|---|---|---|---|---|---|---|---|
| OSCILLIS | fs0/k3 | 38 of 50 | 0.760 | [0.618, 0.869] | 0 of 100 | 0.000 | 0.0000 | YES | full |
| OSCILLIS | fs10/k3 | 50 of 50 | 1.000 | [0.929, 1.000] | 0 of 100 | 0.000 | 0.0000 | YES | full |
| MITOSA | fs0/k3 | 0 of 50 | 0.000 | [0.000, 0.071] | 0 of 100 | 0.000 | 1.0000 | no | full |
| MITOSA | fs10/k3 | 5 of 50 | 0.100 | [0.033, 0.218] | 0 of 100 | 0.000 | 0.0036 | YES | full |
| VAGRANT | fs0/k3 | 14 of 50 | 0.280 | [0.162, 0.425] | 0 of 100 | 0.000 | 0.0000 | YES | full |
| VAGRANT | fs10/k3 | 48 of 50 | 0.960 | [0.863, 0.995] | 0 of 100 | 0.000 | 0.0000 | YES | full |

## Rule 2: selection at the final step (standard rule)

E = largest neutral |delta| over the cell's neutral runs (primary); E95 = 95th percentile (secondary, labelled). Selection: at least `need` treatment seeds outside E with the same winner sign; takeover: selection and the median final share of the winner over the outside seeds >= 0.90; large but inconsistent: `need`+ outside with both signs.

| species | cell | treat seeds | neutral runs | need | E (max) | outside E | +u / -u | winner median final share | verdict | E95 | outside E95 | verdict at E95 (secondary) | status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| OSCILLIS | fs0/k3 | 50 | 100 | 40 | 0.0761 | 50 | 0 / 50 | 0.933 | takeover | 0.0469 | 50 | takeover | full |
| OSCILLIS | fs10/k3 | 50 | 100 | 40 | 0.3578 | 50 | 50 / 0 | 0.977 | takeover | 0.1245 | 50 | takeover | full |
| MITOSA | fs0/k3 | 50 | 100 | 40 | 0.1128 | 12 | 6 / 6 | 0.636 | no selection detected | 0.0661 | 25 | no selection detected | full |
| MITOSA | fs10/k3 | 50 | 100 | 40 | 0.1516 | 20 | 8 / 12 | 0.858 | no selection detected | 0.0980 | 27 | no selection detected | full |
| VAGRANT | fs0/k3 | 50 | 100 | 40 | 0.3324 | 14 | 12 / 2 | 1.000 | no selection detected | 0.0667 | 37 | no selection detected | full |
| VAGRANT | fs10/k3 | 50 | 100 | 40 | 0.1236 | 49 | 3 / 46 | 0.997 | large but inconsistent | 0.0461 | 50 | large but inconsistent | full |

## Rule 3: direction

Winner sign split among treatment seeds outside E (primary), per cell. A cell has a consistent sign only if its rule-2 verdict is selection or takeover (all outside seeds the same sign, at least `need` of them). Sensing off (fs0) vs sensing on (fs10) per species: same sign, opposite sign, or no consistent sign.

| species | cell | +u | -u | consistent sign |
|---|---|---|---|---|
| OSCILLIS | fs0/k3 | 0 | 50 | -u |
| OSCILLIS | fs10/k3 | 50 | 0 | +u |
| MITOSA | fs0/k3 | 6 | 6 | none |
| MITOSA | fs10/k3 | 8 | 12 | none |
| VAGRANT | fs0/k3 | 12 | 2 | none |
| VAGRANT | fs10/k3 | 3 | 46 | none |

| species | kappa | sensing off (fs0) | sensing on (fs10) | comparison | status |
|---|---|---|---|---|---|
| OSCILLIS | 3 | -u | +u | opposite sign | full |
| MITOSA | 3 | none | none | no consistent sign (off and on) | full |
| VAGRANT | 3 | none | none | no consistent sign (off and on) | full |

## Rule 4: share movement, |delta| at 30,000 vs final step

Run lengths present: [300000]. d30 = mean share_A over samples with 27000 < t <= 30000 minus the first sample (campaign_harness_summary.py part 3); d300 = delta_share_A. Classes as in campaign_harness_summary.py: saturated if |d300 - d30| <= 0.05; reverses if opposite sign; grows if |d300| > |d30|; else shrinks.

| species | cell | group | n | saturated | grows | reverses | shrinks | median |d30| | median |d300| | status |
|---|---|---|---|---|---|---|---|---|---|---|
| OSCILLIS | fs0/k3 | treat | 50 | 0 | 28 | 22 | 0 | 0.030 | 0.433 | full |
| OSCILLIS | fs0/k3 | neutral | 100 | 99 | 1 | 0 | 0 | 0.004 | 0.009 | full |
| OSCILLIS | fs10/k3 | treat | 50 | 0 | 49 | 1 | 0 | 0.068 | 0.477 | full |
| OSCILLIS | fs10/k3 | neutral | 100 | 83 | 7 | 10 | 0 | 0.006 | 0.024 | full |
| MITOSA | fs0/k3 | treat | 50 | 10 | 17 | 18 | 5 | 0.032 | 0.066 | full |
| MITOSA | fs0/k3 | neutral | 100 | 100 | 0 | 0 | 0 | 0.011 | 0.010 | full |
| MITOSA | fs10/k3 | treat | 50 | 14 | 13 | 22 | 1 | 0.048 | 0.114 | full |
| MITOSA | fs10/k3 | neutral | 100 | 84 | 9 | 7 | 0 | 0.007 | 0.016 | full |
| VAGRANT | fs0/k3 | treat | 50 | 10 | 20 | 20 | 0 | 0.041 | 0.171 | full |
| VAGRANT | fs0/k3 | neutral | 100 | 94 | 5 | 1 | 0 | 0.005 | 0.006 | full |
| VAGRANT | fs10/k3 | treat | 50 | 0 | 48 | 1 | 1 | 0.209 | 0.496 | full |
| VAGRANT | fs10/k3 | neutral | 100 | 98 | 1 | 1 | 0 | 0.008 | 0.010 | full |

## Rule 5: distinctness at the final step

Per treatment run: end hybrid fraction vs the same run's own hybrid fraction at step 30,000. Verdict (as specified): holds if the median end hybrid fraction over treatment runs is at most half the median of the same runs' 30,000-step values. Secondary (the harness's per-run rule, campaign_harness_summary.py (c)): runs with h_end <= max(0.10, h30 + 0.05).

| species | cell | treat n | median h30 | median h_end | ratio | holds (<= 1/2) | runs holding (harness rule) | status |
|---|---|---|---|---|---|---|---|---|
| OSCILLIS | fs0/k3 | 50 | 0.064 | 0.000 | 0.00 | holds | 46 of 50 | full |
| OSCILLIS | fs10/k3 | 50 | 0.000 | 0.000 | 0.00 | holds | 50 of 50 | full |
| MITOSA | fs0/k3 | 50 | 0.000 | 0.000 | 0.02 | holds | 44 of 50 | full |
| MITOSA | fs10/k3 | 50 | 0.005 | 0.103 | 21.87 | does not hold | 25 of 50 | full |
| VAGRANT | fs0/k3 | 50 | 0.000 | 0.000 | 0.01 | holds | 50 of 50 | full |
| VAGRANT | fs10/k3 | 50 | 0.000 | 0.000 | 0.00 | holds | 50 of 50 | full |

## Rule 6: neutral-arm sanity

Mean neutral delta within 2 SE of zero per cell; outside is flagged as harness asymmetry (reported, not voiding).

| species | cell | neutral runs | mean delta | SE | mean/SE | flag | status |
|---|---|---|---|---|---|---|---|
| OSCILLIS | fs0/k3 | 100 | +0.0003 | 0.0020 | +0.15 | ok | full |
| OSCILLIS | fs10/k3 | 100 | -0.0023 | 0.0062 | -0.37 | ok | full |
| MITOSA | fs0/k3 | 100 | -0.0006 | 0.0027 | -0.23 | ok | full |
| MITOSA | fs10/k3 | 100 | -0.0041 | 0.0042 | -0.98 | ok | full |
| VAGRANT | fs0/k3 | 100 | +0.0063 | 0.0048 | +1.32 | ok | full |
| VAGRANT | fs10/k3 | 100 | -0.0001 | 0.0023 | -0.03 | ok | full |

## Rule 7: conservation (max relative drift of sum(body)+sum(food))

| species | cell | runs | max drift | status |
|---|---|---|---|---|
| OSCILLIS | fs0/k3 | 150 | 2.65e-14 | full |
| OSCILLIS | fs10/k3 | 150 | 2.57e-14 | full |
| MITOSA | fs0/k3 | 150 | 4.18e-14 | full |
| MITOSA | fs10/k3 | 150 | 2.17e-14 | full |
| VAGRANT | fs0/k3 | 150 | 3.82e-14 | full |
| VAGRANT | fs10/k3 | 150 | 1.43e-14 | full |

Max over all 900 runs: **4.18e-14**.

## Per-run table

winner = lineage whose share rose; end/peak = winner's share at the last sample / its maximum over samples. h30/h300 = hybrid fraction at step 30,000 / at the end.

| species | cell | arm | seed | A start | d30 | d300 | class | winner share end | winner share peak | h30 | h300 | blobs end | max drift | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| OSCILLIS | fs0/k3 | treat | 1 | 0.501 | -0.017 | -0.434 | grows | 0.933 | 0.933 | 0.347 | 0.000 | 8 | 1.3e-14 | 15647 |
| OSCILLIS | fs0/k3 | treat | 2 | 0.495 | +0.026 | -0.373 | reverses | 0.878 | 0.887 | 0.000 | 0.000 | 13 | 1.4e-14 | 15452 |
| OSCILLIS | fs0/k3 | treat | 3 | 0.499 | +0.065 | -0.358 | reverses | 0.859 | 0.861 | 0.568 | 1.000 | 35 | 8.4e-15 | 16919 |
| OSCILLIS | fs0/k3 | treat | 4 | 0.498 | +0.015 | -0.400 | reverses | 0.903 | 0.913 | 0.213 | 0.000 | 14 | 1.5e-14 | 16904 |
| OSCILLIS | fs0/k3 | treat | 5 | 0.502 | -0.023 | -0.228 | grows | 0.726 | 0.726 | 1.000 | 1.000 | 3 | 2.4e-14 | 16693 |
| OSCILLIS | fs0/k3 | treat | 6 | 0.493 | -0.072 | -0.466 | grows | 0.973 | 0.973 | 0.000 | 0.000 | 1 | 1.3e-14 | 16492 |
| OSCILLIS | fs0/k3 | treat | 7 | 0.499 | +0.024 | -0.430 | reverses | 0.931 | 0.950 | 0.000 | 0.000 | 30 | 1.8e-14 | 16627 |
| OSCILLIS | fs0/k3 | treat | 8 | 0.499 | -0.124 | -0.423 | grows | 0.924 | 0.925 | 0.130 | 0.000 | 8 | 2.0e-14 | 16527 |
| OSCILLIS | fs0/k3 | treat | 9 | 0.502 | -0.160 | -0.464 | grows | 0.961 | 0.961 | 0.000 | 0.000 | 6 | 6.2e-15 | 288 |
| OSCILLIS | fs0/k3 | treat | 10 | 0.506 | -0.035 | -0.406 | grows | 0.900 | 0.900 | 0.359 | 0.452 | 1 | 3.3e-15 | 288 |
| OSCILLIS | fs0/k3 | treat | 11 | 0.506 | +0.014 | -0.427 | reverses | 0.921 | 0.931 | 0.000 | 0.000 | 33 | 7.3e-15 | 288 |
| OSCILLIS | fs0/k3 | treat | 12 | 0.501 | +0.029 | -0.077 | reverses | 0.575 | 0.575 | 0.977 | 1.000 | 1 | 6.4e-15 | 288 |
| OSCILLIS | fs0/k3 | treat | 13 | 0.504 | -0.094 | -0.446 | grows | 0.942 | 0.943 | 0.161 | 0.000 | 12 | 1.1e-14 | 288 |
| OSCILLIS | fs0/k3 | treat | 14 | 0.500 | -0.032 | -0.447 | grows | 0.947 | 0.959 | 0.030 | 0.000 | 9 | 1.6e-14 | 288 |
| OSCILLIS | fs0/k3 | treat | 15 | 0.503 | +0.027 | -0.396 | reverses | 0.894 | 0.894 | 0.542 | 0.685 | 1 | 2.7e-15 | 288 |
| OSCILLIS | fs0/k3 | treat | 16 | 0.499 | -0.125 | -0.425 | grows | 0.927 | 0.936 | 0.000 | 0.000 | 36 | 1.2e-14 | 288 |
| OSCILLIS | fs0/k3 | treat | 17 | 0.504 | -0.024 | -0.431 | grows | 0.927 | 0.928 | 0.346 | 0.000 | 5 | 5.2e-15 | 288 |
| OSCILLIS | fs0/k3 | treat | 18 | 0.493 | -0.168 | -0.435 | grows | 0.942 | 0.944 | 0.057 | 0.000 | 1 | 5.5e-15 | 283 |
| OSCILLIS | fs0/k3 | treat | 19 | 0.498 | -0.046 | -0.474 | grows | 0.976 | 0.987 | 0.000 | 0.000 | 2 | 1.6e-14 | 283 |
| OSCILLIS | fs0/k3 | treat | 20 | 0.499 | +0.027 | -0.422 | reverses | 0.923 | 0.939 | 0.309 | 0.033 | 19 | 2.4e-15 | 283 |
| OSCILLIS | fs0/k3 | treat | 21 | 0.495 | -0.015 | -0.477 | grows | 0.982 | 0.982 | 0.000 | 0.000 | 2 | 7.2e-15 | 283 |
| OSCILLIS | fs0/k3 | treat | 22 | 0.501 | +0.035 | -0.465 | reverses | 0.964 | 0.979 | 0.052 | 0.000 | 7 | 1.1e-14 | 283 |
| OSCILLIS | fs0/k3 | treat | 23 | 0.504 | -0.049 | -0.474 | grows | 0.970 | 0.982 | 0.000 | 0.000 | 10 | 8.9e-15 | 283 |
| OSCILLIS | fs0/k3 | treat | 24 | 0.505 | -0.018 | -0.413 | grows | 0.908 | 0.909 | 0.417 | 0.361 | 28 | 7.6e-15 | 283 |
| OSCILLIS | fs0/k3 | treat | 25 | 0.500 | -0.174 | -0.438 | grows | 0.938 | 0.938 | 0.096 | 0.000 | 3 | 7.2e-15 | 283 |
| OSCILLIS | fs0/k3 | treat | 26 | 0.499 | +0.031 | -0.479 | reverses | 0.980 | 0.990 | 0.000 | 0.000 | 8 | 9.0e-15 | 283 |
| OSCILLIS | fs0/k3 | treat | 27 | 0.491 | -0.094 | -0.454 | grows | 0.963 | 0.963 | 0.000 | 0.000 | 1 | 1.1e-14 | 283 |
| OSCILLIS | fs0/k3 | treat | 28 | 0.499 | -0.005 | -0.414 | grows | 0.916 | 0.921 | 0.000 | 0.000 | 25 | 7.1e-15 | 279 |
| OSCILLIS | fs0/k3 | treat | 29 | 0.508 | -0.192 | -0.454 | grows | 0.946 | 0.946 | 0.071 | 0.000 | 1 | 1.2e-14 | 279 |
| OSCILLIS | fs0/k3 | treat | 30 | 0.498 | +0.016 | -0.451 | reverses | 0.953 | 0.953 | 0.366 | 0.000 | 11 | 4.5e-15 | 279 |
| OSCILLIS | fs0/k3 | treat | 31 | 0.499 | +0.007 | -0.435 | reverses | 0.936 | 0.946 | 0.075 | 0.000 | 21 | 7.9e-15 | 279 |
| OSCILLIS | fs0/k3 | treat | 32 | 0.504 | +0.005 | -0.454 | reverses | 0.950 | 0.953 | 0.271 | 0.061 | 9 | 3.6e-15 | 279 |
| OSCILLIS | fs0/k3 | treat | 33 | 0.495 | -0.016 | -0.446 | grows | 0.951 | 0.951 | 0.114 | 0.000 | 1 | 5.0e-15 | 279 |
| OSCILLIS | fs0/k3 | treat | 34 | 0.501 | +0.030 | -0.380 | reverses | 0.879 | 0.884 | 0.593 | 0.345 | 33 | 1.3e-15 | 279 |
| OSCILLIS | fs0/k3 | treat | 35 | 0.497 | -0.001 | -0.486 | grows | 0.989 | 0.989 | 0.000 | 0.000 | 1 | 1.2e-14 | 279 |
| OSCILLIS | fs0/k3 | treat | 36 | 0.500 | -0.060 | -0.478 | grows | 0.978 | 0.978 | 0.000 | 0.000 | 1 | 1.2e-14 | 279 |
| OSCILLIS | fs0/k3 | treat | 37 | 0.502 | +0.002 | -0.216 | reverses | 0.713 | 0.731 | 0.991 | 1.000 | 3 | 1.2e-15 | 279 |
| OSCILLIS | fs0/k3 | treat | 38 | 0.507 | +0.037 | -0.388 | reverses | 0.881 | 0.893 | 0.000 | 0.000 | 15 | 4.4e-15 | 281 |
| OSCILLIS | fs0/k3 | treat | 39 | 0.504 | +0.012 | -0.284 | reverses | 0.779 | 0.780 | 0.971 | 1.000 | 1 | 2.6e-15 | 281 |
| OSCILLIS | fs0/k3 | treat | 40 | 0.497 | -0.027 | -0.272 | grows | 0.775 | 0.776 | 0.708 | 1.000 | 12 | 2.8e-15 | 281 |
| OSCILLIS | fs0/k3 | treat | 41 | 0.500 | -0.014 | -0.484 | grows | 0.984 | 0.990 | 0.000 | 0.000 | 4 | 1.2e-14 | 281 |
| OSCILLIS | fs0/k3 | treat | 42 | 0.502 | -0.092 | -0.488 | grows | 0.986 | 0.986 | 0.000 | 0.000 | 7 | 4.9e-15 | 281 |
| OSCILLIS | fs0/k3 | treat | 43 | 0.500 | -0.102 | -0.475 | grows | 0.975 | 0.975 | 0.000 | 0.000 | 9 | 6.9e-15 | 281 |
| OSCILLIS | fs0/k3 | treat | 44 | 0.496 | +0.069 | -0.342 | reverses | 0.846 | 0.860 | 0.000 | 0.000 | 19 | 5.8e-15 | 281 |
| OSCILLIS | fs0/k3 | treat | 45 | 0.498 | +0.027 | -0.425 | reverses | 0.927 | 0.944 | 0.000 | 0.000 | 18 | 1.2e-14 | 281 |
| OSCILLIS | fs0/k3 | treat | 46 | 0.505 | -0.053 | -0.493 | grows | 0.988 | 0.990 | 0.000 | 0.000 | 1 | 9.9e-15 | 281 |
| OSCILLIS | fs0/k3 | treat | 47 | 0.497 | +0.058 | -0.427 | reverses | 0.931 | 0.942 | 0.245 | 0.000 | 10 | 3.1e-15 | 281 |
| OSCILLIS | fs0/k3 | treat | 48 | 0.499 | +0.004 | -0.434 | reverses | 0.936 | 0.946 | 0.000 | 0.000 | 25 | 1.3e-14 | 228 |
| OSCILLIS | fs0/k3 | treat | 49 | 0.499 | +0.050 | -0.432 | reverses | 0.932 | 0.943 | 0.187 | 0.031 | 12 | 5.8e-15 | 228 |
| OSCILLIS | fs0/k3 | treat | 50 | 0.500 | -0.013 | -0.409 | grows | 0.909 | 0.910 | 0.517 | 0.085 | 2 | 5.7e-15 | 228 |
| OSCILLIS | fs0/k3 | neutral_plus | 1 | 0.501 | +0.003 | +0.006 | saturated | 0.507 | 0.508 | 0.977 | 1.000 | 29 | 2.3e-14 | 15271 |
| OSCILLIS | fs0/k3 | neutral_plus | 2 | 0.495 | +0.005 | +0.006 | saturated | 0.501 | 0.501 | 0.749 | 1.000 | 8 | 1.9e-14 | 15309 |
| OSCILLIS | fs0/k3 | neutral_plus | 3 | 0.499 | -0.002 | +0.004 | saturated | 0.504 | 0.510 | 0.754 | 1.000 | 10 | 2.6e-14 | 16955 |
| OSCILLIS | fs0/k3 | neutral_plus | 4 | 0.498 | -0.001 | +0.006 | saturated | 0.504 | 0.505 | 0.919 | 1.000 | 17 | 2.6e-14 | 16893 |
| OSCILLIS | fs0/k3 | neutral_plus | 5 | 0.502 | +0.002 | +0.002 | saturated | 0.504 | 0.505 | 1.000 | 1.000 | 32 | 1.6e-14 | 16529 |
| OSCILLIS | fs0/k3 | neutral_plus | 6 | 0.493 | +0.002 | +0.002 | saturated | 0.495 | 0.496 | 1.000 | 1.000 | 21 | 1.4e-14 | 16518 |
| OSCILLIS | fs0/k3 | neutral_plus | 7 | 0.499 | +0.002 | -0.008 | saturated | 0.509 | 0.509 | 0.851 | 1.000 | 5 | 2.5e-14 | 16723 |
| OSCILLIS | fs0/k3 | neutral_plus | 8 | 0.499 | -0.000 | -0.005 | saturated | 0.506 | 0.506 | 1.000 | 1.000 | 22 | 2.2e-14 | 16722 |
| OSCILLIS | fs0/k3 | neutral_plus | 9 | 0.502 | -0.001 | -0.002 | saturated | 0.499 | 0.500 | 1.000 | 1.000 | 20 | 8.0e-15 | 288 |
| OSCILLIS | fs0/k3 | neutral_plus | 10 | 0.506 | +0.029 | +0.037 | saturated | 0.543 | 0.543 | 1.000 | 1.000 | 10 | 1.8e-14 | 288 |
| OSCILLIS | fs0/k3 | neutral_plus | 11 | 0.506 | +0.002 | +0.001 | saturated | 0.507 | 0.508 | 0.744 | 1.000 | 9 | 1.8e-14 | 288 |
| OSCILLIS | fs0/k3 | neutral_plus | 12 | 0.501 | +0.002 | -0.006 | saturated | 0.504 | 0.504 | 0.939 | 1.000 | 23 | 1.4e-14 | 288 |
| OSCILLIS | fs0/k3 | neutral_plus | 13 | 0.504 | +0.004 | +0.005 | saturated | 0.509 | 0.513 | 1.000 | 1.000 | 23 | 1.0e-14 | 288 |
| OSCILLIS | fs0/k3 | neutral_plus | 14 | 0.500 | +0.004 | +0.018 | saturated | 0.518 | 0.518 | 0.982 | 1.000 | 28 | 1.6e-14 | 288 |
| OSCILLIS | fs0/k3 | neutral_plus | 15 | 0.503 | +0.003 | -0.025 | saturated | 0.523 | 0.524 | 0.866 | 1.000 | 13 | 1.9e-14 | 288 |
| OSCILLIS | fs0/k3 | neutral_plus | 16 | 0.499 | -0.022 | -0.019 | saturated | 0.520 | 0.525 | 1.000 | 1.000 | 23 | 2.0e-14 | 288 |
| OSCILLIS | fs0/k3 | neutral_plus | 17 | 0.504 | -0.007 | -0.027 | saturated | 0.523 | 0.523 | 0.856 | 1.000 | 22 | 1.7e-14 | 288 |
| OSCILLIS | fs0/k3 | neutral_plus | 18 | 0.493 | +0.007 | +0.007 | saturated | 0.500 | 0.501 | 1.000 | 1.000 | 10 | 7.1e-15 | 283 |
| OSCILLIS | fs0/k3 | neutral_plus | 19 | 0.498 | +0.000 | -0.002 | saturated | 0.504 | 0.505 | 0.881 | 1.000 | 21 | 1.9e-14 | 283 |
| OSCILLIS | fs0/k3 | neutral_plus | 20 | 0.499 | +0.001 | -0.000 | saturated | 0.502 | 0.502 | 0.916 | 1.000 | 12 | 1.9e-14 | 283 |
| OSCILLIS | fs0/k3 | neutral_plus | 21 | 0.495 | +0.002 | +0.006 | saturated | 0.501 | 0.501 | 0.993 | 1.000 | 15 | 9.3e-15 | 283 |
| OSCILLIS | fs0/k3 | neutral_plus | 22 | 0.501 | -0.004 | +0.001 | saturated | 0.502 | 0.502 | 0.807 | 1.000 | 36 | 1.7e-14 | 283 |
| OSCILLIS | fs0/k3 | neutral_plus | 23 | 0.504 | -0.005 | -0.016 | saturated | 0.512 | 0.515 | 0.854 | 1.000 | 13 | 1.8e-14 | 283 |
| OSCILLIS | fs0/k3 | neutral_plus | 24 | 0.505 | +0.005 | +0.006 | saturated | 0.512 | 0.512 | 0.980 | 1.000 | 20 | 1.1e-14 | 283 |
| OSCILLIS | fs0/k3 | neutral_plus | 25 | 0.500 | +0.003 | +0.003 | saturated | 0.504 | 0.505 | 1.000 | 1.000 | 7 | 1.4e-14 | 283 |
| OSCILLIS | fs0/k3 | neutral_plus | 26 | 0.499 | +0.004 | -0.010 | saturated | 0.511 | 0.512 | 0.775 | 1.000 | 18 | 1.7e-14 | 283 |
| OSCILLIS | fs0/k3 | neutral_plus | 27 | 0.491 | +0.002 | -0.010 | saturated | 0.519 | 0.519 | 1.000 | 1.000 | 23 | 1.6e-14 | 283 |
| OSCILLIS | fs0/k3 | neutral_plus | 28 | 0.499 | +0.001 | +0.002 | saturated | 0.501 | 0.501 | 0.855 | 1.000 | 11 | 1.8e-14 | 279 |
| OSCILLIS | fs0/k3 | neutral_plus | 29 | 0.508 | -0.002 | +0.003 | saturated | 0.511 | 0.511 | 1.000 | 1.000 | 26 | 1.5e-14 | 279 |
| OSCILLIS | fs0/k3 | neutral_plus | 30 | 0.498 | -0.008 | -0.013 | saturated | 0.516 | 0.516 | 0.851 | 1.000 | 20 | 1.8e-14 | 279 |
| OSCILLIS | fs0/k3 | neutral_plus | 31 | 0.499 | -0.001 | +0.025 | saturated | 0.524 | 0.524 | 0.846 | 1.000 | 37 | 1.9e-14 | 279 |
| OSCILLIS | fs0/k3 | neutral_plus | 32 | 0.504 | +0.001 | +0.001 | saturated | 0.505 | 0.507 | 0.888 | 1.000 | 25 | 1.8e-14 | 279 |
| OSCILLIS | fs0/k3 | neutral_plus | 33 | 0.495 | -0.000 | +0.000 | saturated | 0.495 | 0.498 | 1.000 | 1.000 | 6 | 4.3e-15 | 279 |
| OSCILLIS | fs0/k3 | neutral_plus | 34 | 0.501 | +0.000 | -0.021 | saturated | 0.520 | 0.521 | 0.843 | 1.000 | 20 | 1.9e-14 | 279 |
| OSCILLIS | fs0/k3 | neutral_plus | 35 | 0.497 | +0.003 | -0.011 | saturated | 0.514 | 0.514 | 0.843 | 1.000 | 14 | 1.4e-14 | 279 |
| OSCILLIS | fs0/k3 | neutral_plus | 36 | 0.500 | -0.008 | -0.013 | saturated | 0.513 | 0.513 | 0.985 | 1.000 | 2 | 1.5e-14 | 279 |
| OSCILLIS | fs0/k3 | neutral_plus | 37 | 0.502 | +0.002 | +0.002 | saturated | 0.504 | 0.504 | 1.000 | 1.000 | 34 | 6.1e-15 | 279 |
| OSCILLIS | fs0/k3 | neutral_plus | 38 | 0.507 | +0.001 | +0.001 | saturated | 0.508 | 0.510 | 0.774 | 1.000 | 7 | 1.5e-14 | 281 |
| OSCILLIS | fs0/k3 | neutral_plus | 39 | 0.504 | +0.003 | +0.005 | saturated | 0.509 | 0.509 | 1.000 | 1.000 | 15 | 6.8e-15 | 281 |
| OSCILLIS | fs0/k3 | neutral_plus | 40 | 0.497 | -0.002 | -0.002 | saturated | 0.505 | 0.506 | 1.000 | 1.000 | 17 | 4.5e-15 | 281 |
| OSCILLIS | fs0/k3 | neutral_plus | 41 | 0.500 | -0.004 | -0.006 | saturated | 0.506 | 0.507 | 0.896 | 1.000 | 7 | 1.7e-14 | 281 |
| OSCILLIS | fs0/k3 | neutral_plus | 42 | 0.502 | +0.002 | +0.003 | saturated | 0.505 | 0.506 | 0.967 | 1.000 | 17 | 1.2e-14 | 281 |
| OSCILLIS | fs0/k3 | neutral_plus | 43 | 0.500 | +0.006 | +0.009 | saturated | 0.509 | 0.509 | 1.000 | 1.000 | 18 | 1.2e-14 | 281 |
| OSCILLIS | fs0/k3 | neutral_plus | 44 | 0.496 | +0.001 | +0.002 | saturated | 0.498 | 0.498 | 0.762 | 1.000 | 2 | 1.7e-14 | 281 |
| OSCILLIS | fs0/k3 | neutral_plus | 45 | 0.498 | -0.004 | -0.009 | saturated | 0.512 | 0.514 | 0.867 | 1.000 | 26 | 1.9e-14 | 281 |
| OSCILLIS | fs0/k3 | neutral_plus | 46 | 0.505 | -0.007 | -0.021 | saturated | 0.515 | 0.516 | 0.809 | 1.000 | 28 | 1.6e-14 | 281 |
| OSCILLIS | fs0/k3 | neutral_plus | 47 | 0.497 | -0.004 | +0.033 | saturated | 0.529 | 0.530 | 0.799 | 1.000 | 10 | 2.1e-14 | 281 |
| OSCILLIS | fs0/k3 | neutral_plus | 48 | 0.499 | +0.001 | +0.002 | saturated | 0.501 | 0.501 | 0.907 | 1.000 | 13 | 1.8e-14 | 228 |
| OSCILLIS | fs0/k3 | neutral_plus | 49 | 0.499 | -0.006 | -0.006 | saturated | 0.506 | 0.507 | 0.753 | 1.000 | 20 | 2.0e-14 | 228 |
| OSCILLIS | fs0/k3 | neutral_plus | 50 | 0.500 | +0.005 | +0.008 | saturated | 0.508 | 0.508 | 0.930 | 1.000 | 29 | 1.1e-14 | 228 |
| OSCILLIS | fs0/k3 | neutral_minus | 1 | 0.501 | -0.012 | -0.017 | saturated | 0.515 | 0.516 | 1.000 | 1.000 | 1 | 1.4e-14 | 15311 |
| OSCILLIS | fs0/k3 | neutral_minus | 2 | 0.495 | -0.001 | +0.005 | saturated | 0.500 | 0.528 | 0.776 | 1.000 | 21 | 2.2e-14 | 15310 |
| OSCILLIS | fs0/k3 | neutral_minus | 3 | 0.499 | +0.006 | +0.008 | saturated | 0.507 | 0.507 | 1.000 | 1.000 | 55 | 1.4e-14 | 16937 |
| OSCILLIS | fs0/k3 | neutral_minus | 4 | 0.498 | +0.011 | +0.012 | saturated | 0.510 | 0.521 | 0.963 | 1.000 | 4 | 1.7e-14 | 16674 |
| OSCILLIS | fs0/k3 | neutral_minus | 5 | 0.502 | +0.017 | +0.019 | saturated | 0.522 | 0.523 | 1.000 | 1.000 | 2 | 1.1e-14 | 16629 |
| OSCILLIS | fs0/k3 | neutral_minus | 6 | 0.493 | +0.005 | -0.012 | saturated | 0.519 | 0.520 | 0.999 | 1.000 | 1 | 1.1e-14 | 16775 |
| OSCILLIS | fs0/k3 | neutral_minus | 7 | 0.499 | -0.002 | -0.022 | saturated | 0.523 | 0.526 | 0.983 | 1.000 | 1 | 2.5e-14 | 16609 |
| OSCILLIS | fs0/k3 | neutral_minus | 8 | 0.499 | +0.007 | -0.014 | saturated | 0.515 | 0.516 | 0.605 | 0.766 | 1 | 1.1e-14 | 288 |
| OSCILLIS | fs0/k3 | neutral_minus | 9 | 0.502 | -0.010 | -0.009 | saturated | 0.507 | 0.514 | 0.768 | 1.000 | 1 | 3.5e-15 | 288 |
| OSCILLIS | fs0/k3 | neutral_minus | 10 | 0.506 | -0.003 | -0.001 | saturated | 0.495 | 0.504 | 1.000 | 1.000 | 1 | 7.1e-15 | 288 |
| OSCILLIS | fs0/k3 | neutral_minus | 11 | 0.506 | -0.006 | -0.048 | saturated | 0.542 | 0.544 | 0.359 | 0.956 | 50 | 1.0e-14 | 288 |
| OSCILLIS | fs0/k3 | neutral_minus | 12 | 0.501 | -0.009 | -0.014 | saturated | 0.513 | 0.520 | 1.000 | 1.000 | 4 | 4.0e-15 | 288 |
| OSCILLIS | fs0/k3 | neutral_minus | 13 | 0.504 | -0.002 | +0.023 | saturated | 0.528 | 0.529 | 0.942 | 1.000 | 1 | 5.6e-15 | 288 |
| OSCILLIS | fs0/k3 | neutral_minus | 14 | 0.500 | -0.004 | -0.018 | saturated | 0.518 | 0.521 | 0.775 | 1.000 | 9 | 5.9e-15 | 288 |
| OSCILLIS | fs0/k3 | neutral_minus | 15 | 0.503 | -0.005 | -0.015 | saturated | 0.513 | 0.516 | 0.999 | 1.000 | 1 | 7.6e-15 | 288 |
| OSCILLIS | fs0/k3 | neutral_minus | 16 | 0.499 | -0.022 | -0.067 | saturated | 0.568 | 0.575 | 0.830 | 1.000 | 42 | 1.1e-14 | 288 |
| OSCILLIS | fs0/k3 | neutral_minus | 17 | 0.504 | -0.003 | +0.002 | saturated | 0.506 | 0.508 | 1.000 | 1.000 | 1 | 5.2e-15 | 288 |
| OSCILLIS | fs0/k3 | neutral_minus | 18 | 0.493 | -0.011 | -0.033 | saturated | 0.540 | 0.550 | 0.817 | 1.000 | 1 | 4.0e-15 | 283 |
| OSCILLIS | fs0/k3 | neutral_minus | 19 | 0.498 | -0.000 | -0.004 | saturated | 0.506 | 0.509 | 0.784 | 1.000 | 1 | 5.6e-15 | 283 |
| OSCILLIS | fs0/k3 | neutral_minus | 20 | 0.499 | -0.003 | +0.006 | saturated | 0.505 | 0.505 | 0.965 | 1.000 | 41 | 4.2e-15 | 283 |
| OSCILLIS | fs0/k3 | neutral_minus | 21 | 0.495 | -0.002 | +0.003 | saturated | 0.498 | 0.501 | 1.000 | 1.000 | 1 | 8.7e-15 | 283 |
| OSCILLIS | fs0/k3 | neutral_minus | 22 | 0.501 | +0.014 | +0.076 | grows | 0.577 | 0.587 | 0.930 | 1.000 | 23 | 7.6e-15 | 283 |
| OSCILLIS | fs0/k3 | neutral_minus | 23 | 0.504 | -0.009 | +0.032 | saturated | 0.536 | 0.540 | 0.402 | 1.000 | 8 | 1.1e-14 | 283 |
| OSCILLIS | fs0/k3 | neutral_minus | 24 | 0.505 | -0.003 | -0.051 | saturated | 0.546 | 0.547 | 0.952 | 1.000 | 1 | 7.0e-15 | 283 |
| OSCILLIS | fs0/k3 | neutral_minus | 25 | 0.500 | +0.034 | +0.027 | saturated | 0.528 | 0.547 | 0.866 | 1.000 | 8 | 4.8e-15 | 283 |
| OSCILLIS | fs0/k3 | neutral_minus | 26 | 0.499 | +0.004 | +0.001 | saturated | 0.501 | 0.507 | 0.847 | 1.000 | 1 | 1.1e-14 | 283 |
| OSCILLIS | fs0/k3 | neutral_minus | 27 | 0.491 | +0.011 | +0.024 | saturated | 0.515 | 0.519 | 0.710 | 0.946 | 10 | 5.7e-15 | 283 |
| OSCILLIS | fs0/k3 | neutral_minus | 28 | 0.499 | -0.001 | -0.031 | saturated | 0.532 | 0.534 | 0.657 | 1.000 | 57 | 1.1e-14 | 279 |
| OSCILLIS | fs0/k3 | neutral_minus | 29 | 0.508 | -0.004 | +0.006 | saturated | 0.515 | 0.515 | 0.761 | 1.000 | 1 | 1.1e-14 | 279 |
| OSCILLIS | fs0/k3 | neutral_minus | 30 | 0.498 | +0.011 | +0.020 | saturated | 0.518 | 0.518 | 1.000 | 1.000 | 1 | 4.7e-15 | 279 |
| OSCILLIS | fs0/k3 | neutral_minus | 31 | 0.499 | +0.024 | -0.013 | saturated | 0.515 | 0.518 | 0.764 | 0.903 | 5 | 7.8e-15 | 279 |
| OSCILLIS | fs0/k3 | neutral_minus | 32 | 0.504 | +0.003 | -0.000 | saturated | 0.496 | 0.507 | 1.000 | 1.000 | 1 | 6.5e-15 | 279 |
| OSCILLIS | fs0/k3 | neutral_minus | 33 | 0.495 | +0.004 | +0.007 | saturated | 0.502 | 0.503 | 0.987 | 1.000 | 1 | 5.4e-15 | 279 |
| OSCILLIS | fs0/k3 | neutral_minus | 34 | 0.501 | -0.002 | -0.010 | saturated | 0.509 | 0.510 | 1.000 | 1.000 | 18 | 3.2e-15 | 279 |
| OSCILLIS | fs0/k3 | neutral_minus | 35 | 0.497 | +0.005 | +0.001 | saturated | 0.499 | 0.504 | 0.959 | 1.000 | 4 | 1.9e-15 | 279 |
| OSCILLIS | fs0/k3 | neutral_minus | 36 | 0.500 | +0.008 | -0.018 | saturated | 0.517 | 0.525 | 0.867 | 1.000 | 4 | 3.2e-15 | 279 |
| OSCILLIS | fs0/k3 | neutral_minus | 37 | 0.502 | +0.000 | -0.009 | saturated | 0.506 | 0.508 | 1.000 | 1.000 | 1 | 9.9e-15 | 279 |
| OSCILLIS | fs0/k3 | neutral_minus | 38 | 0.507 | +0.001 | +0.047 | saturated | 0.554 | 0.556 | 0.628 | 1.000 | 17 | 6.9e-15 | 281 |
| OSCILLIS | fs0/k3 | neutral_minus | 39 | 0.504 | -0.011 | -0.009 | saturated | 0.504 | 0.508 | 1.000 | 1.000 | 1 | 4.8e-15 | 281 |
| OSCILLIS | fs0/k3 | neutral_minus | 40 | 0.497 | +0.009 | +0.006 | saturated | 0.503 | 0.507 | 1.000 | 1.000 | 32 | 2.4e-15 | 281 |
| OSCILLIS | fs0/k3 | neutral_minus | 41 | 0.500 | -0.002 | +0.040 | saturated | 0.540 | 0.541 | 0.718 | 1.000 | 9 | 8.9e-15 | 281 |
| OSCILLIS | fs0/k3 | neutral_minus | 42 | 0.502 | -0.003 | -0.020 | saturated | 0.518 | 0.520 | 0.921 | 1.000 | 9 | 4.6e-16 | 281 |
| OSCILLIS | fs0/k3 | neutral_minus | 43 | 0.500 | +0.012 | +0.020 | saturated | 0.519 | 0.519 | 0.851 | 1.000 | 1 | 1.3e-15 | 281 |
| OSCILLIS | fs0/k3 | neutral_minus | 44 | 0.496 | +0.017 | +0.059 | saturated | 0.555 | 0.557 | 0.875 | 1.000 | 29 | 5.4e-15 | 281 |
| OSCILLIS | fs0/k3 | neutral_minus | 45 | 0.498 | -0.002 | -0.007 | saturated | 0.509 | 0.509 | 1.000 | 1.000 | 1 | 4.2e-15 | 281 |
| OSCILLIS | fs0/k3 | neutral_minus | 46 | 0.505 | -0.004 | +0.005 | saturated | 0.510 | 0.510 | 0.680 | 0.981 | 1 | 1.6e-14 | 281 |
| OSCILLIS | fs0/k3 | neutral_minus | 47 | 0.497 | -0.007 | -0.002 | saturated | 0.506 | 0.512 | 0.993 | 1.000 | 9 | 1.2e-14 | 281 |
| OSCILLIS | fs0/k3 | neutral_minus | 48 | 0.499 | +0.011 | +0.019 | saturated | 0.518 | 0.528 | 0.823 | 1.000 | 50 | 1.0e-14 | 228 |
| OSCILLIS | fs0/k3 | neutral_minus | 49 | 0.499 | -0.007 | -0.006 | saturated | 0.507 | 0.513 | 0.915 | 1.000 | 2 | 7.9e-15 | 228 |
| OSCILLIS | fs0/k3 | neutral_minus | 50 | 0.500 | +0.012 | +0.034 | saturated | 0.534 | 0.538 | 0.999 | 1.000 | 5 | 6.3e-15 | 228 |
| OSCILLIS | fs10/k3 | treat | 1 | 0.501 | +0.081 | +0.480 | grows | 0.982 | 0.982 | 0.001 | 0.000 | 5 | 1.6e-14 | 18464 |
| OSCILLIS | fs10/k3 | treat | 2 | 0.495 | +0.066 | +0.489 | grows | 0.984 | 0.985 | 0.000 | 0.000 | 5 | 5.1e-15 | 18281 |
| OSCILLIS | fs10/k3 | treat | 3 | 0.499 | -0.023 | +0.474 | reverses | 0.974 | 0.974 | 0.000 | 0.000 | 6 | 2.5e-14 | 19902 |
| OSCILLIS | fs10/k3 | treat | 4 | 0.498 | +0.045 | +0.476 | grows | 0.974 | 0.974 | 0.000 | 0.000 | 5 | 1.6e-14 | 19474 |
| OSCILLIS | fs10/k3 | treat | 5 | 0.502 | +0.051 | +0.465 | grows | 0.968 | 0.968 | 0.000 | 0.000 | 5 | 1.2e-14 | 19549 |
| OSCILLIS | fs10/k3 | treat | 6 | 0.493 | +0.071 | +0.478 | grows | 0.971 | 0.971 | 0.001 | 0.000 | 9 | 1.4e-14 | 19650 |
| OSCILLIS | fs10/k3 | treat | 7 | 0.499 | +0.027 | +0.479 | grows | 0.978 | 0.979 | 0.000 | 0.000 | 5 | 1.9e-14 | 19401 |
| OSCILLIS | fs10/k3 | treat | 8 | 0.499 | +0.071 | +0.468 | grows | 0.968 | 0.968 | 0.000 | 0.000 | 5 | 7.8e-15 | 386 |
| OSCILLIS | fs10/k3 | treat | 9 | 0.502 | +0.119 | +0.482 | grows | 0.985 | 0.985 | 0.000 | 0.000 | 7 | 3.5e-15 | 386 |
| OSCILLIS | fs10/k3 | treat | 10 | 0.506 | +0.020 | +0.476 | grows | 0.982 | 0.982 | 0.000 | 0.000 | 4 | 6.7e-15 | 386 |
| OSCILLIS | fs10/k3 | treat | 11 | 0.506 | +0.007 | +0.487 | grows | 0.992 | 0.993 | 0.000 | 0.000 | 5 | 1.7e-14 | 386 |
| OSCILLIS | fs10/k3 | treat | 12 | 0.501 | +0.050 | +0.467 | grows | 0.968 | 0.969 | 0.001 | 0.000 | 7 | 4.2e-15 | 386 |
| OSCILLIS | fs10/k3 | treat | 13 | 0.504 | +0.127 | +0.464 | grows | 0.969 | 0.970 | 0.001 | 0.000 | 8 | 3.4e-15 | 386 |
| OSCILLIS | fs10/k3 | treat | 14 | 0.500 | +0.079 | +0.479 | grows | 0.979 | 0.979 | 0.000 | 0.000 | 5 | 1.8e-14 | 386 |
| OSCILLIS | fs10/k3 | treat | 15 | 0.503 | +0.030 | +0.475 | grows | 0.977 | 0.978 | 0.000 | 0.000 | 4 | 7.6e-15 | 386 |
| OSCILLIS | fs10/k3 | treat | 16 | 0.499 | +0.085 | +0.495 | grows | 0.994 | 0.994 | 0.000 | 0.000 | 6 | 1.1e-14 | 386 |
| OSCILLIS | fs10/k3 | treat | 17 | 0.504 | +0.013 | +0.465 | grows | 0.970 | 0.970 | 0.001 | 0.000 | 4 | 6.4e-15 | 386 |
| OSCILLIS | fs10/k3 | treat | 18 | 0.493 | +0.075 | +0.482 | grows | 0.974 | 0.974 | 0.000 | 0.000 | 5 | 6.2e-15 | 385 |
| OSCILLIS | fs10/k3 | treat | 19 | 0.498 | +0.194 | +0.481 | grows | 0.979 | 0.979 | 0.000 | 0.000 | 5 | 1.7e-14 | 385 |
| OSCILLIS | fs10/k3 | treat | 20 | 0.499 | +0.010 | +0.491 | grows | 0.990 | 0.990 | 0.000 | 0.000 | 7 | 6.6e-15 | 385 |
| OSCILLIS | fs10/k3 | treat | 21 | 0.495 | +0.058 | +0.484 | grows | 0.979 | 0.979 | 0.000 | 0.000 | 5 | 1.0e-14 | 385 |
| OSCILLIS | fs10/k3 | treat | 22 | 0.501 | +0.004 | +0.466 | grows | 0.967 | 0.968 | 0.000 | 0.000 | 6 | 3.9e-15 | 385 |
| OSCILLIS | fs10/k3 | treat | 23 | 0.504 | +0.034 | +0.491 | grows | 0.995 | 0.995 | 0.000 | 0.000 | 6 | 7.8e-15 | 385 |
| OSCILLIS | fs10/k3 | treat | 24 | 0.505 | +0.018 | +0.474 | grows | 0.980 | 0.980 | 0.000 | 0.000 | 4 | 6.8e-15 | 385 |
| OSCILLIS | fs10/k3 | treat | 25 | 0.500 | +0.057 | +0.438 | grows | 0.939 | 0.939 | 0.000 | 0.000 | 4 | 5.7e-15 | 385 |
| OSCILLIS | fs10/k3 | treat | 26 | 0.499 | +0.024 | +0.480 | grows | 0.979 | 0.980 | 0.000 | 0.000 | 4 | 8.8e-15 | 385 |
| OSCILLIS | fs10/k3 | treat | 27 | 0.491 | +0.063 | +0.477 | grows | 0.968 | 0.969 | 0.000 | 0.000 | 4 | 2.5e-15 | 385 |
| OSCILLIS | fs10/k3 | treat | 28 | 0.499 | +0.109 | +0.488 | grows | 0.987 | 0.987 | 0.000 | 0.000 | 5 | 1.8e-14 | 379 |
| OSCILLIS | fs10/k3 | treat | 29 | 0.508 | +0.038 | +0.462 | grows | 0.970 | 0.970 | 0.000 | 0.000 | 4 | 4.6e-15 | 379 |
| OSCILLIS | fs10/k3 | treat | 30 | 0.498 | +0.070 | +0.472 | grows | 0.969 | 0.970 | 0.000 | 0.000 | 7 | 1.5e-14 | 379 |
| OSCILLIS | fs10/k3 | treat | 31 | 0.499 | +0.082 | +0.480 | grows | 0.979 | 0.979 | 0.000 | 0.000 | 3 | 6.4e-15 | 379 |
| OSCILLIS | fs10/k3 | treat | 32 | 0.504 | +0.072 | +0.473 | grows | 0.978 | 0.978 | 0.000 | 0.000 | 6 | 5.3e-15 | 379 |
| OSCILLIS | fs10/k3 | treat | 33 | 0.495 | +0.020 | +0.485 | grows | 0.979 | 0.979 | 0.000 | 0.000 | 7 | 6.5e-15 | 379 |
| OSCILLIS | fs10/k3 | treat | 34 | 0.501 | +0.042 | +0.476 | grows | 0.977 | 0.977 | 0.000 | 0.000 | 4 | 6.6e-15 | 379 |
| OSCILLIS | fs10/k3 | treat | 35 | 0.497 | +0.097 | +0.485 | grows | 0.982 | 0.982 | 0.000 | 0.000 | 6 | 5.4e-15 | 379 |
| OSCILLIS | fs10/k3 | treat | 36 | 0.500 | +0.163 | +0.486 | grows | 0.987 | 0.987 | 0.000 | 0.000 | 7 | 1.6e-14 | 379 |
| OSCILLIS | fs10/k3 | treat | 37 | 0.502 | +0.100 | +0.464 | grows | 0.966 | 0.966 | 0.001 | 0.000 | 5 | 2.8e-15 | 379 |
| OSCILLIS | fs10/k3 | treat | 38 | 0.507 | +0.014 | +0.481 | grows | 0.988 | 0.988 | 0.000 | 0.000 | 5 | 2.3e-14 | 378 |
| OSCILLIS | fs10/k3 | treat | 39 | 0.504 | +0.158 | +0.441 | grows | 0.946 | 0.947 | 0.000 | 0.000 | 3 | 5.9e-15 | 378 |
| OSCILLIS | fs10/k3 | treat | 40 | 0.497 | +0.084 | +0.481 | grows | 0.977 | 0.978 | 0.000 | 0.000 | 4 | 6.6e-15 | 378 |
| OSCILLIS | fs10/k3 | treat | 41 | 0.500 | +0.097 | +0.474 | grows | 0.974 | 0.975 | 0.000 | 0.000 | 5 | 1.5e-14 | 378 |
| OSCILLIS | fs10/k3 | treat | 42 | 0.502 | +0.130 | +0.474 | grows | 0.976 | 0.976 | 0.001 | 0.000 | 6 | 5.1e-15 | 378 |
| OSCILLIS | fs10/k3 | treat | 43 | 0.500 | +0.069 | +0.474 | grows | 0.974 | 0.974 | 0.000 | 0.000 | 6 | 9.4e-15 | 378 |
| OSCILLIS | fs10/k3 | treat | 44 | 0.496 | +0.109 | +0.465 | grows | 0.961 | 0.961 | 0.000 | 0.000 | 6 | 6.9e-15 | 378 |
| OSCILLIS | fs10/k3 | treat | 45 | 0.498 | +0.121 | +0.486 | grows | 0.984 | 0.985 | 0.000 | 0.000 | 7 | 4.8e-15 | 378 |
| OSCILLIS | fs10/k3 | treat | 46 | 0.505 | +0.050 | +0.475 | grows | 0.980 | 0.981 | 0.000 | 0.000 | 6 | 1.0e-14 | 378 |
| OSCILLIS | fs10/k3 | treat | 47 | 0.497 | +0.107 | +0.474 | grows | 0.971 | 0.971 | 0.000 | 0.000 | 4 | 5.7e-15 | 378 |
| OSCILLIS | fs10/k3 | treat | 48 | 0.499 | +0.008 | +0.493 | grows | 0.991 | 0.991 | 0.000 | 0.000 | 7 | 1.4e-14 | 385 |
| OSCILLIS | fs10/k3 | treat | 49 | 0.499 | +0.024 | +0.487 | grows | 0.986 | 0.986 | 0.000 | 0.000 | 6 | 1.0e-14 | 385 |
| OSCILLIS | fs10/k3 | treat | 50 | 0.500 | +0.079 | +0.470 | grows | 0.970 | 0.970 | 0.000 | 0.000 | 7 | 1.4e-14 | 385 |
| OSCILLIS | fs10/k3 | neutral_plus | 1 | 0.501 | -0.019 | -0.027 | saturated | 0.526 | 0.526 | 0.841 | 0.857 | 3 | 2.4e-14 | 18418 |
| OSCILLIS | fs10/k3 | neutral_plus | 2 | 0.495 | -0.002 | +0.041 | saturated | 0.536 | 0.544 | 0.116 | 0.575 | 5 | 1.4e-14 | 18278 |
| OSCILLIS | fs10/k3 | neutral_plus | 3 | 0.499 | +0.014 | +0.028 | saturated | 0.527 | 0.528 | 0.061 | 0.504 | 4 | 2.6e-14 | 19681 |
| OSCILLIS | fs10/k3 | neutral_plus | 4 | 0.498 | +0.001 | +0.032 | saturated | 0.530 | 0.531 | 0.000 | 0.647 | 6 | 1.5e-14 | 19726 |
| OSCILLIS | fs10/k3 | neutral_plus | 5 | 0.502 | +0.009 | -0.018 | saturated | 0.515 | 0.516 | 0.071 | 0.881 | 3 | 1.3e-14 | 19481 |
| OSCILLIS | fs10/k3 | neutral_plus | 6 | 0.493 | +0.000 | +0.021 | saturated | 0.513 | 0.516 | 0.902 | 1.000 | 4 | 2.1e-14 | 19515 |
| OSCILLIS | fs10/k3 | neutral_plus | 7 | 0.499 | -0.002 | -0.016 | saturated | 0.516 | 0.523 | 1.000 | 1.000 | 5 | 2.0e-14 | 19585 |
| OSCILLIS | fs10/k3 | neutral_plus | 8 | 0.499 | +0.004 | +0.028 | saturated | 0.527 | 0.528 | 0.261 | 0.690 | 3 | 9.4e-15 | 386 |
| OSCILLIS | fs10/k3 | neutral_plus | 9 | 0.502 | -0.001 | -0.014 | saturated | 0.512 | 0.515 | 0.622 | 0.866 | 3 | 1.2e-14 | 386 |
| OSCILLIS | fs10/k3 | neutral_plus | 10 | 0.506 | +0.010 | +0.009 | saturated | 0.515 | 0.516 | 1.000 | 1.000 | 4 | 2.0e-14 | 386 |
| OSCILLIS | fs10/k3 | neutral_plus | 11 | 0.506 | +0.001 | +0.003 | saturated | 0.509 | 0.510 | 0.000 | 0.000 | 4 | 1.4e-14 | 386 |
| OSCILLIS | fs10/k3 | neutral_plus | 12 | 0.501 | -0.002 | -0.018 | saturated | 0.517 | 0.517 | 0.836 | 0.847 | 5 | 9.9e-15 | 386 |
| OSCILLIS | fs10/k3 | neutral_plus | 13 | 0.504 | +0.007 | +0.014 | saturated | 0.518 | 0.520 | 0.729 | 1.000 | 6 | 7.4e-15 | 386 |
| OSCILLIS | fs10/k3 | neutral_plus | 14 | 0.500 | +0.007 | +0.007 | saturated | 0.507 | 0.508 | 0.734 | 0.689 | 7 | 1.4e-14 | 386 |
| OSCILLIS | fs10/k3 | neutral_plus | 15 | 0.503 | -0.018 | -0.026 | saturated | 0.523 | 0.523 | 0.821 | 0.841 | 4 | 1.6e-14 | 386 |
| OSCILLIS | fs10/k3 | neutral_plus | 16 | 0.499 | -0.008 | -0.079 | grows | 0.580 | 0.584 | 0.547 | 0.720 | 4 | 4.5e-15 | 386 |
| OSCILLIS | fs10/k3 | neutral_plus | 17 | 0.504 | +0.002 | +0.003 | saturated | 0.507 | 0.518 | 0.872 | 1.000 | 6 | 1.4e-14 | 386 |
| OSCILLIS | fs10/k3 | neutral_plus | 18 | 0.493 | -0.008 | +0.032 | saturated | 0.525 | 0.526 | 0.675 | 0.864 | 4 | 1.3e-14 | 385 |
| OSCILLIS | fs10/k3 | neutral_plus | 19 | 0.498 | -0.002 | -0.022 | saturated | 0.524 | 0.527 | 0.000 | 0.481 | 7 | 1.3e-14 | 385 |
| OSCILLIS | fs10/k3 | neutral_plus | 20 | 0.499 | +0.005 | +0.005 | saturated | 0.504 | 0.509 | 1.000 | 1.000 | 6 | 1.2e-14 | 385 |
| OSCILLIS | fs10/k3 | neutral_plus | 21 | 0.495 | -0.001 | +0.004 | saturated | 0.499 | 0.501 | 0.831 | 0.863 | 6 | 1.4e-14 | 385 |
| OSCILLIS | fs10/k3 | neutral_plus | 22 | 0.501 | +0.008 | +0.017 | saturated | 0.518 | 0.519 | 0.000 | 0.563 | 5 | 1.8e-14 | 385 |
| OSCILLIS | fs10/k3 | neutral_plus | 23 | 0.504 | -0.003 | +0.002 | saturated | 0.506 | 0.525 | 0.000 | 0.653 | 5 | 8.0e-15 | 385 |
| OSCILLIS | fs10/k3 | neutral_plus | 24 | 0.505 | -0.005 | -0.009 | saturated | 0.503 | 0.504 | 0.677 | 0.742 | 5 | 7.6e-15 | 385 |
| OSCILLIS | fs10/k3 | neutral_plus | 25 | 0.500 | -0.015 | -0.005 | saturated | 0.505 | 0.517 | 1.000 | 1.000 | 6 | 1.3e-14 | 385 |
| OSCILLIS | fs10/k3 | neutral_plus | 26 | 0.499 | -0.000 | -0.006 | saturated | 0.506 | 0.507 | 0.000 | 0.700 | 3 | 2.1e-14 | 385 |
| OSCILLIS | fs10/k3 | neutral_plus | 27 | 0.491 | -0.007 | -0.048 | saturated | 0.557 | 0.557 | 0.139 | 0.849 | 3 | 1.0e-14 | 385 |
| OSCILLIS | fs10/k3 | neutral_plus | 28 | 0.499 | +0.018 | +0.047 | saturated | 0.546 | 0.548 | 0.608 | 0.708 | 4 | 1.8e-14 | 379 |
| OSCILLIS | fs10/k3 | neutral_plus | 29 | 0.508 | -0.008 | -0.050 | saturated | 0.542 | 0.544 | 0.511 | 0.540 | 6 | 9.3e-15 | 379 |
| OSCILLIS | fs10/k3 | neutral_plus | 30 | 0.498 | +0.005 | -0.036 | saturated | 0.539 | 0.546 | 0.333 | 0.840 | 4 | 1.1e-14 | 379 |
| OSCILLIS | fs10/k3 | neutral_plus | 31 | 0.499 | -0.004 | +0.054 | reverses | 0.553 | 0.553 | 0.463 | 0.480 | 4 | 1.7e-14 | 379 |
| OSCILLIS | fs10/k3 | neutral_plus | 32 | 0.504 | +0.003 | +0.001 | saturated | 0.505 | 0.509 | 1.000 | 1.000 | 5 | 1.2e-14 | 379 |
| OSCILLIS | fs10/k3 | neutral_plus | 33 | 0.495 | -0.011 | -0.045 | saturated | 0.550 | 0.552 | 0.579 | 0.686 | 4 | 1.7e-14 | 379 |
| OSCILLIS | fs10/k3 | neutral_plus | 34 | 0.501 | +0.013 | +0.030 | saturated | 0.531 | 0.533 | 1.000 | 1.000 | 6 | 1.7e-14 | 379 |
| OSCILLIS | fs10/k3 | neutral_plus | 35 | 0.497 | +0.018 | +0.022 | saturated | 0.519 | 0.522 | 0.014 | 0.946 | 5 | 1.5e-14 | 379 |
| OSCILLIS | fs10/k3 | neutral_plus | 36 | 0.500 | -0.003 | -0.032 | saturated | 0.532 | 0.536 | 0.460 | 0.764 | 5 | 2.1e-14 | 379 |
| OSCILLIS | fs10/k3 | neutral_plus | 37 | 0.502 | -0.002 | -0.006 | saturated | 0.504 | 0.507 | 0.963 | 1.000 | 4 | 5.4e-15 | 379 |
| OSCILLIS | fs10/k3 | neutral_plus | 38 | 0.507 | +0.004 | +0.070 | grows | 0.577 | 0.577 | 0.000 | 0.394 | 4 | 1.7e-14 | 378 |
| OSCILLIS | fs10/k3 | neutral_plus | 39 | 0.504 | -0.012 | -0.024 | saturated | 0.519 | 0.520 | 0.423 | 0.869 | 3 | 9.7e-15 | 378 |
| OSCILLIS | fs10/k3 | neutral_plus | 40 | 0.497 | +0.007 | +0.020 | saturated | 0.517 | 0.517 | 0.614 | 0.681 | 4 | 1.4e-14 | 378 |
| OSCILLIS | fs10/k3 | neutral_plus | 41 | 0.500 | +0.002 | +0.034 | saturated | 0.535 | 0.537 | 0.000 | 0.602 | 6 | 1.6e-14 | 378 |
| OSCILLIS | fs10/k3 | neutral_plus | 42 | 0.502 | -0.003 | +0.025 | saturated | 0.526 | 0.530 | 0.502 | 0.527 | 5 | 1.1e-14 | 378 |
| OSCILLIS | fs10/k3 | neutral_plus | 43 | 0.500 | +0.010 | +0.042 | saturated | 0.541 | 0.543 | 0.716 | 0.854 | 6 | 1.3e-14 | 378 |
| OSCILLIS | fs10/k3 | neutral_plus | 44 | 0.496 | -0.006 | -0.029 | saturated | 0.534 | 0.534 | 1.000 | 1.000 | 5 | 1.6e-14 | 378 |
| OSCILLIS | fs10/k3 | neutral_plus | 45 | 0.498 | +0.018 | +0.042 | saturated | 0.540 | 0.540 | 0.529 | 0.914 | 5 | 1.7e-14 | 378 |
| OSCILLIS | fs10/k3 | neutral_plus | 46 | 0.505 | +0.002 | +0.023 | saturated | 0.529 | 0.534 | 0.000 | 0.792 | 5 | 1.7e-14 | 378 |
| OSCILLIS | fs10/k3 | neutral_plus | 47 | 0.497 | +0.005 | +0.084 | grows | 0.581 | 0.595 | 0.013 | 0.766 | 4 | 1.2e-14 | 378 |
| OSCILLIS | fs10/k3 | neutral_plus | 48 | 0.499 | -0.009 | -0.008 | saturated | 0.510 | 0.512 | 1.000 | 1.000 | 6 | 1.2e-14 | 385 |
| OSCILLIS | fs10/k3 | neutral_plus | 49 | 0.499 | -0.002 | +0.095 | reverses | 0.595 | 0.598 | 0.000 | 0.790 | 4 | 9.7e-15 | 385 |
| OSCILLIS | fs10/k3 | neutral_plus | 50 | 0.500 | -0.013 | +0.008 | saturated | 0.507 | 0.509 | 0.000 | 0.677 | 3 | 1.6e-14 | 385 |
| OSCILLIS | fs10/k3 | neutral_minus | 1 | 0.501 | +0.010 | +0.019 | saturated | 0.520 | 0.527 | 0.758 | 1.000 | 6 | 6.3e-15 | 18327 |
| OSCILLIS | fs10/k3 | neutral_minus | 2 | 0.495 | -0.017 | -0.015 | saturated | 0.520 | 0.530 | 0.000 | 0.000 | 6 | 4.8e-15 | 18434 |
| OSCILLIS | fs10/k3 | neutral_minus | 3 | 0.499 | -0.018 | -0.065 | saturated | 0.566 | 0.566 | 0.395 | 0.482 | 10 | 2.1e-15 | 19803 |
| OSCILLIS | fs10/k3 | neutral_minus | 4 | 0.498 | -0.011 | -0.002 | saturated | 0.504 | 0.517 | 1.000 | 1.000 | 5 | 8.1e-15 | 19618 |
| OSCILLIS | fs10/k3 | neutral_minus | 5 | 0.502 | +0.004 | -0.061 | reverses | 0.559 | 0.566 | 0.980 | 1.000 | 4 | 1.0e-14 | 19582 |
| OSCILLIS | fs10/k3 | neutral_minus | 6 | 0.493 | +0.005 | -0.018 | saturated | 0.526 | 0.530 | 1.000 | 1.000 | 24 | 7.2e-15 | 19531 |
| OSCILLIS | fs10/k3 | neutral_minus | 7 | 0.499 | +0.001 | -0.003 | saturated | 0.504 | 0.505 | 1.000 | 1.000 | 7 | 6.2e-15 | 19859 |
| OSCILLIS | fs10/k3 | neutral_minus | 8 | 0.499 | +0.007 | -0.113 | reverses | 0.613 | 0.625 | 0.273 | 1.000 | 4 | 2.6e-15 | 386 |
| OSCILLIS | fs10/k3 | neutral_minus | 9 | 0.502 | +0.023 | -0.168 | reverses | 0.666 | 0.666 | 0.767 | 1.000 | 5 | 4.4e-15 | 386 |
| OSCILLIS | fs10/k3 | neutral_minus | 10 | 0.506 | -0.013 | -0.024 | saturated | 0.518 | 0.532 | 1.000 | 1.000 | 4 | 7.9e-16 | 386 |
| OSCILLIS | fs10/k3 | neutral_minus | 11 | 0.506 | +0.002 | -0.003 | saturated | 0.497 | 0.497 | 0.000 | 0.000 | 8 | 3.5e-15 | 386 |
| OSCILLIS | fs10/k3 | neutral_minus | 12 | 0.501 | -0.016 | +0.041 | reverses | 0.542 | 0.545 | 0.750 | 1.000 | 5 | 1.6e-15 | 386 |
| OSCILLIS | fs10/k3 | neutral_minus | 13 | 0.504 | -0.003 | +0.050 | reverses | 0.554 | 0.555 | 0.890 | 0.886 | 5 | 8.2e-16 | 386 |
| OSCILLIS | fs10/k3 | neutral_minus | 14 | 0.500 | +0.003 | +0.015 | saturated | 0.515 | 0.516 | 0.739 | 0.654 | 6 | 2.0e-15 | 386 |
| OSCILLIS | fs10/k3 | neutral_minus | 15 | 0.503 | -0.022 | -0.027 | saturated | 0.525 | 0.535 | 0.813 | 1.000 | 3 | 3.8e-15 | 386 |
| OSCILLIS | fs10/k3 | neutral_minus | 16 | 0.499 | +0.036 | +0.224 | grows | 0.723 | 0.758 | 0.000 | 1.000 | 3 | 6.9e-15 | 386 |
| OSCILLIS | fs10/k3 | neutral_minus | 17 | 0.504 | +0.007 | +0.013 | saturated | 0.517 | 0.519 | 0.681 | 0.754 | 6 | 2.6e-15 | 386 |
| OSCILLIS | fs10/k3 | neutral_minus | 18 | 0.493 | +0.006 | -0.042 | saturated | 0.550 | 0.553 | 0.898 | 1.000 | 7 | 1.8e-15 | 385 |
| OSCILLIS | fs10/k3 | neutral_minus | 19 | 0.498 | +0.014 | +0.013 | saturated | 0.511 | 0.516 | 0.872 | 0.876 | 8 | 3.2e-15 | 385 |
| OSCILLIS | fs10/k3 | neutral_minus | 20 | 0.499 | -0.002 | -0.034 | saturated | 0.535 | 0.535 | 0.601 | 0.625 | 8 | 2.3e-15 | 385 |
| OSCILLIS | fs10/k3 | neutral_minus | 21 | 0.495 | -0.007 | -0.010 | saturated | 0.515 | 0.523 | 1.000 | 1.000 | 7 | 2.3e-15 | 385 |
| OSCILLIS | fs10/k3 | neutral_minus | 22 | 0.501 | +0.005 | +0.013 | saturated | 0.514 | 0.515 | 0.699 | 0.750 | 8 | 3.2e-15 | 385 |
| OSCILLIS | fs10/k3 | neutral_minus | 23 | 0.504 | +0.000 | -0.005 | saturated | 0.501 | 0.501 | 0.004 | 0.002 | 10 | 2.0e-15 | 385 |
| OSCILLIS | fs10/k3 | neutral_minus | 24 | 0.505 | -0.010 | +0.034 | saturated | 0.539 | 0.559 | 0.840 | 1.000 | 8 | 1.8e-15 | 385 |
| OSCILLIS | fs10/k3 | neutral_minus | 25 | 0.500 | -0.005 | -0.017 | saturated | 0.517 | 0.519 | 0.889 | 0.877 | 5 | 2.7e-15 | 385 |
| OSCILLIS | fs10/k3 | neutral_minus | 26 | 0.499 | -0.011 | +0.136 | reverses | 0.635 | 0.642 | 0.025 | 1.000 | 3 | 2.0e-15 | 385 |
| OSCILLIS | fs10/k3 | neutral_minus | 27 | 0.491 | +0.004 | +0.054 | grows | 0.545 | 0.545 | 0.509 | 0.614 | 5 | 3.2e-15 | 385 |
| OSCILLIS | fs10/k3 | neutral_minus | 28 | 0.499 | -0.002 | -0.003 | saturated | 0.504 | 0.504 | 0.879 | 0.833 | 6 | 2.3e-15 | 379 |
| OSCILLIS | fs10/k3 | neutral_minus | 29 | 0.508 | +0.039 | +0.024 | saturated | 0.533 | 0.559 | 0.097 | 1.000 | 5 | 2.5e-15 | 379 |
| OSCILLIS | fs10/k3 | neutral_minus | 30 | 0.498 | -0.000 | +0.014 | saturated | 0.512 | 0.522 | 0.640 | 0.614 | 8 | 2.6e-15 | 379 |
| OSCILLIS | fs10/k3 | neutral_minus | 31 | 0.499 | -0.002 | +0.104 | reverses | 0.602 | 0.606 | 0.382 | 0.756 | 4 | 1.9e-15 | 379 |
| OSCILLIS | fs10/k3 | neutral_minus | 32 | 0.504 | +0.009 | +0.012 | saturated | 0.516 | 0.517 | 1.000 | 1.000 | 9 | 1.6e-15 | 379 |
| OSCILLIS | fs10/k3 | neutral_minus | 33 | 0.495 | +0.010 | +0.028 | saturated | 0.523 | 0.524 | 0.861 | 1.000 | 6 | 3.9e-15 | 379 |
| OSCILLIS | fs10/k3 | neutral_minus | 34 | 0.501 | -0.012 | -0.035 | saturated | 0.534 | 0.534 | 1.000 | 1.000 | 7 | 2.2e-15 | 379 |
| OSCILLIS | fs10/k3 | neutral_minus | 35 | 0.497 | +0.005 | -0.021 | saturated | 0.523 | 0.550 | 0.908 | 1.000 | 14 | 2.4e-15 | 379 |
| OSCILLIS | fs10/k3 | neutral_minus | 36 | 0.500 | -0.004 | -0.136 | grows | 0.636 | 0.639 | 1.000 | 1.000 | 4 | 3.6e-15 | 379 |
| OSCILLIS | fs10/k3 | neutral_minus | 37 | 0.502 | +0.003 | -0.017 | saturated | 0.515 | 0.516 | 1.000 | 1.000 | 3 | 1.4e-15 | 379 |
| OSCILLIS | fs10/k3 | neutral_minus | 38 | 0.507 | +0.012 | +0.017 | saturated | 0.524 | 0.524 | 0.363 | 0.334 | 6 | 1.8e-15 | 378 |
| OSCILLIS | fs10/k3 | neutral_minus | 39 | 0.504 | +0.016 | -0.033 | saturated | 0.529 | 0.533 | 0.912 | 1.000 | 22 | 6.6e-16 | 378 |
| OSCILLIS | fs10/k3 | neutral_minus | 40 | 0.497 | +0.003 | +0.005 | saturated | 0.501 | 0.512 | 0.902 | 1.000 | 2 | 8.5e-16 | 378 |
| OSCILLIS | fs10/k3 | neutral_minus | 41 | 0.500 | +0.005 | -0.010 | saturated | 0.510 | 0.522 | 0.752 | 0.751 | 8 | 2.7e-15 | 378 |
| OSCILLIS | fs10/k3 | neutral_minus | 42 | 0.502 | +0.025 | +0.066 | saturated | 0.568 | 0.591 | 0.930 | 1.000 | 5 | 2.0e-15 | 378 |
| OSCILLIS | fs10/k3 | neutral_minus | 43 | 0.500 | +0.022 | -0.358 | reverses | 0.858 | 0.869 | 0.561 | 0.644 | 17 | 4.5e-15 | 378 |
| OSCILLIS | fs10/k3 | neutral_minus | 44 | 0.496 | +0.000 | +0.005 | saturated | 0.500 | 0.501 | 0.437 | 0.478 | 7 | 1.2e-14 | 378 |
| OSCILLIS | fs10/k3 | neutral_minus | 45 | 0.498 | -0.005 | -0.021 | saturated | 0.524 | 0.524 | 0.875 | 0.876 | 12 | 2.5e-15 | 378 |
| OSCILLIS | fs10/k3 | neutral_minus | 46 | 0.505 | -0.005 | -0.124 | grows | 0.619 | 0.621 | 0.780 | 1.000 | 7 | 2.8e-15 | 378 |
| OSCILLIS | fs10/k3 | neutral_minus | 47 | 0.497 | +0.000 | +0.011 | saturated | 0.508 | 0.533 | 0.903 | 1.000 | 4 | 4.2e-15 | 378 |
| OSCILLIS | fs10/k3 | neutral_minus | 48 | 0.499 | -0.006 | -0.029 | saturated | 0.530 | 0.530 | 1.000 | 1.000 | 7 | 2.6e-15 | 385 |
| OSCILLIS | fs10/k3 | neutral_minus | 49 | 0.499 | -0.016 | +0.005 | saturated | 0.504 | 0.505 | 0.001 | 0.000 | 6 | 3.3e-15 | 385 |
| OSCILLIS | fs10/k3 | neutral_minus | 50 | 0.500 | -0.021 | -0.059 | saturated | 0.559 | 0.560 | 0.890 | 1.000 | 9 | 1.8e-15 | 385 |
| MITOSA | fs0/k3 | treat | 1 | 0.501 | +0.021 | -0.089 | reverses | 0.587 | 0.597 | 0.000 | 0.000 | 22 | 7.6e-15 | 15615 |
| MITOSA | fs0/k3 | treat | 2 | 0.495 | -0.014 | -0.079 | grows | 0.584 | 0.586 | 0.000 | 0.000 | 11 | 5.1e-15 | 15600 |
| MITOSA | fs0/k3 | treat | 3 | 0.499 | -0.015 | -0.121 | grows | 0.622 | 0.625 | 0.000 | 0.000 | 15 | 8.4e-15 | 17039 |
| MITOSA | fs0/k3 | treat | 4 | 0.498 | -0.006 | -0.114 | grows | 0.616 | 0.624 | 0.000 | 0.000 | 28 | 4.5e-15 | 16981 |
| MITOSA | fs0/k3 | treat | 5 | 0.502 | +0.078 | +0.008 | shrinks | 0.511 | 0.593 | 0.001 | 0.000 | 15 | 1.4e-14 | 16769 |
| MITOSA | fs0/k3 | treat | 6 | 0.493 | +0.011 | -0.062 | reverses | 0.569 | 0.571 | 0.000 | 0.000 | 32 | 9.1e-15 | 16710 |
| MITOSA | fs0/k3 | treat | 7 | 0.499 | +0.076 | +0.009 | shrinks | 0.509 | 0.583 | 0.113 | 0.388 | 12 | 5.7e-15 | 16761 |
| MITOSA | fs0/k3 | treat | 8 | 0.499 | +0.152 | +0.243 | grows | 0.742 | 0.744 | 0.011 | 0.242 | 26 | 5.0e-15 | 289 |
| MITOSA | fs0/k3 | treat | 9 | 0.502 | +0.163 | +0.248 | grows | 0.751 | 0.761 | 0.390 | 0.565 | 34 | 2.9e-15 | 289 |
| MITOSA | fs0/k3 | treat | 10 | 0.506 | +0.030 | -0.057 | reverses | 0.551 | 0.559 | 0.000 | 0.000 | 21 | 4.5e-15 | 289 |
| MITOSA | fs0/k3 | treat | 11 | 0.506 | -0.037 | -0.099 | grows | 0.593 | 0.595 | 0.000 | 0.000 | 12 | 7.5e-15 | 289 |
| MITOSA | fs0/k3 | treat | 12 | 0.501 | -0.009 | -0.094 | grows | 0.593 | 0.596 | 0.000 | 0.000 | 13 | 9.9e-16 | 289 |
| MITOSA | fs0/k3 | treat | 13 | 0.504 | +0.039 | -0.052 | reverses | 0.547 | 0.549 | 0.000 | 0.000 | 32 | 6.7e-15 | 289 |
| MITOSA | fs0/k3 | treat | 14 | 0.500 | +0.104 | +0.024 | shrinks | 0.524 | 0.605 | 0.007 | 0.012 | 26 | 3.1e-15 | 289 |
| MITOSA | fs0/k3 | treat | 15 | 0.503 | -0.004 | -0.090 | grows | 0.588 | 0.596 | 0.000 | 0.000 | 30 | 4.3e-15 | 289 |
| MITOSA | fs0/k3 | treat | 16 | 0.499 | +0.015 | -0.070 | reverses | 0.571 | 0.574 | 0.000 | 0.000 | 16 | 3.2e-15 | 289 |
| MITOSA | fs0/k3 | treat | 17 | 0.504 | +0.048 | -0.018 | reverses | 0.514 | 0.524 | 0.000 | 0.000 | 26 | 4.1e-15 | 289 |
| MITOSA | fs0/k3 | treat | 18 | 0.493 | +0.082 | +0.281 | grows | 0.773 | 0.775 | 0.007 | 0.761 | 30 | 2.7e-15 | 288 |
| MITOSA | fs0/k3 | treat | 19 | 0.498 | +0.033 | +0.109 | grows | 0.608 | 0.620 | 0.000 | 0.000 | 32 | 8.6e-15 | 288 |
| MITOSA | fs0/k3 | treat | 20 | 0.499 | +0.037 | -0.067 | reverses | 0.568 | 0.571 | 0.000 | 0.000 | 21 | 3.2e-15 | 288 |
| MITOSA | fs0/k3 | treat | 21 | 0.495 | -0.005 | -0.026 | saturated | 0.531 | 0.544 | 0.000 | 0.000 | 32 | 4.6e-15 | 288 |
| MITOSA | fs0/k3 | treat | 22 | 0.501 | -0.026 | -0.084 | grows | 0.583 | 0.583 | 0.000 | 0.000 | 23 | 8.0e-15 | 288 |
| MITOSA | fs0/k3 | treat | 23 | 0.504 | +0.042 | -0.001 | saturated | 0.497 | 0.498 | 0.000 | 0.000 | 30 | 4.4e-15 | 288 |
| MITOSA | fs0/k3 | treat | 24 | 0.505 | +0.073 | +0.028 | saturated | 0.533 | 0.583 | 0.001 | 0.000 | 25 | 1.3e-15 | 288 |
| MITOSA | fs0/k3 | treat | 25 | 0.500 | +0.069 | +0.184 | grows | 0.685 | 0.692 | 0.008 | 0.039 | 26 | 5.9e-15 | 288 |
| MITOSA | fs0/k3 | treat | 26 | 0.499 | +0.010 | -0.043 | reverses | 0.544 | 0.547 | 0.000 | 0.000 | 19 | 5.7e-15 | 288 |
| MITOSA | fs0/k3 | treat | 27 | 0.491 | +0.078 | +0.115 | saturated | 0.606 | 0.607 | 0.008 | 0.000 | 30 | 4.5e-15 | 288 |
| MITOSA | fs0/k3 | treat | 28 | 0.499 | +0.025 | -0.030 | reverses | 0.532 | 0.532 | 0.000 | 0.000 | 22 | 8.1e-15 | 287 |
| MITOSA | fs0/k3 | treat | 29 | 0.508 | +0.130 | +0.204 | grows | 0.713 | 0.716 | 0.481 | 0.636 | 30 | 8.0e-15 | 287 |
| MITOSA | fs0/k3 | treat | 30 | 0.498 | +0.011 | -0.093 | reverses | 0.595 | 0.598 | 0.000 | 0.000 | 23 | 3.8e-15 | 287 |
| MITOSA | fs0/k3 | treat | 31 | 0.499 | +0.001 | -0.065 | reverses | 0.567 | 0.568 | 0.000 | 0.000 | 28 | 9.8e-15 | 287 |
| MITOSA | fs0/k3 | treat | 32 | 0.504 | +0.068 | -0.052 | reverses | 0.547 | 0.553 | 0.000 | 0.000 | 33 | 2.6e-15 | 287 |
| MITOSA | fs0/k3 | treat | 33 | 0.495 | +0.112 | +0.061 | shrinks | 0.555 | 0.610 | 0.029 | 0.000 | 44 | 1.5e-15 | 287 |
| MITOSA | fs0/k3 | treat | 34 | 0.501 | -0.023 | -0.125 | grows | 0.624 | 0.629 | 0.000 | 0.000 | 22 | 2.5e-15 | 287 |
| MITOSA | fs0/k3 | treat | 35 | 0.497 | +0.002 | -0.088 | reverses | 0.591 | 0.594 | 0.000 | 0.000 | 30 | 6.5e-15 | 287 |
| MITOSA | fs0/k3 | treat | 36 | 0.500 | +0.040 | +0.087 | saturated | 0.587 | 0.590 | 0.000 | 0.000 | 24 | 4.6e-15 | 287 |
| MITOSA | fs0/k3 | treat | 37 | 0.502 | +0.042 | -0.054 | reverses | 0.552 | 0.563 | 0.000 | 0.000 | 28 | 3.0e-15 | 287 |
| MITOSA | fs0/k3 | treat | 38 | 0.507 | -0.001 | -0.084 | grows | 0.577 | 0.578 | 0.000 | 0.000 | 25 | 6.2e-15 | 284 |
| MITOSA | fs0/k3 | treat | 39 | 0.504 | +0.025 | -0.143 | reverses | 0.639 | 0.646 | 0.000 | 0.000 | 18 | 8.8e-16 | 284 |
| MITOSA | fs0/k3 | treat | 40 | 0.497 | +0.065 | -0.021 | reverses | 0.525 | 0.530 | 0.006 | 0.000 | 35 | 3.6e-15 | 284 |
| MITOSA | fs0/k3 | treat | 41 | 0.500 | +0.052 | +0.005 | saturated | 0.505 | 0.556 | 0.146 | 0.000 | 19 | 3.2e-15 | 284 |
| MITOSA | fs0/k3 | treat | 42 | 0.502 | +0.035 | +0.036 | saturated | 0.538 | 0.543 | 0.003 | 0.330 | 22 | 2.0e-15 | 284 |
| MITOSA | fs0/k3 | treat | 43 | 0.500 | -0.020 | -0.022 | saturated | 0.522 | 0.524 | 0.000 | 0.000 | 20 | 3.6e-15 | 284 |
| MITOSA | fs0/k3 | treat | 44 | 0.496 | -0.012 | -0.115 | grows | 0.620 | 0.623 | 0.000 | 0.000 | 15 | 3.0e-15 | 284 |
| MITOSA | fs0/k3 | treat | 45 | 0.498 | +0.028 | -0.062 | reverses | 0.564 | 0.567 | 0.000 | 0.015 | 24 | 1.2e-15 | 284 |
| MITOSA | fs0/k3 | treat | 46 | 0.505 | +0.039 | +0.020 | saturated | 0.526 | 0.547 | 0.004 | 0.000 | 28 | 4.3e-15 | 284 |
| MITOSA | fs0/k3 | treat | 47 | 0.497 | +0.015 | -0.024 | saturated | 0.528 | 0.539 | 0.000 | 0.000 | 6 | 7.8e-15 | 284 |
| MITOSA | fs0/k3 | treat | 48 | 0.499 | +0.030 | -0.022 | reverses | 0.524 | 0.524 | 0.000 | 0.000 | 19 | 4.4e-15 | 223 |
| MITOSA | fs0/k3 | treat | 49 | 0.499 | -0.012 | -0.134 | grows | 0.634 | 0.638 | 0.000 | 0.000 | 26 | 3.8e-15 | 223 |
| MITOSA | fs0/k3 | treat | 50 | 0.500 | +0.100 | +0.012 | shrinks | 0.512 | 0.604 | 0.004 | 0.000 | 30 | 1.8e-15 | 223 |
| MITOSA | fs0/k3 | neutral_plus | 1 | 0.501 | -0.015 | -0.020 | saturated | 0.519 | 0.519 | 1.000 | 1.000 | 11 | 4.2e-14 | 15566 |
| MITOSA | fs0/k3 | neutral_plus | 2 | 0.495 | -0.005 | -0.004 | saturated | 0.509 | 0.510 | 1.000 | 1.000 | 3 | 3.5e-14 | 15326 |
| MITOSA | fs0/k3 | neutral_plus | 3 | 0.499 | -0.005 | -0.001 | saturated | 0.502 | 0.512 | 1.000 | 1.000 | 17 | 3.8e-14 | 16782 |
| MITOSA | fs0/k3 | neutral_plus | 4 | 0.498 | -0.031 | -0.020 | saturated | 0.522 | 0.534 | 1.000 | 1.000 | 11 | 3.3e-14 | 16808 |
| MITOSA | fs0/k3 | neutral_plus | 5 | 0.502 | +0.003 | +0.007 | saturated | 0.509 | 0.509 | 0.963 | 1.000 | 14 | 3.6e-14 | 16782 |
| MITOSA | fs0/k3 | neutral_plus | 6 | 0.493 | +0.008 | +0.007 | saturated | 0.499 | 0.503 | 1.000 | 1.000 | 22 | 3.6e-14 | 16758 |
| MITOSA | fs0/k3 | neutral_plus | 7 | 0.499 | +0.004 | +0.001 | saturated | 0.500 | 0.507 | 1.000 | 1.000 | 9 | 3.8e-14 | 16613 |
| MITOSA | fs0/k3 | neutral_plus | 8 | 0.499 | -0.001 | -0.002 | saturated | 0.503 | 0.503 | 1.000 | 1.000 | 15 | 3.1e-14 | 289 |
| MITOSA | fs0/k3 | neutral_plus | 9 | 0.502 | -0.009 | -0.004 | saturated | 0.501 | 0.506 | 1.000 | 1.000 | 10 | 2.1e-14 | 289 |
| MITOSA | fs0/k3 | neutral_plus | 10 | 0.506 | +0.005 | +0.009 | saturated | 0.515 | 0.515 | 1.000 | 1.000 | 9 | 3.4e-14 | 289 |
| MITOSA | fs0/k3 | neutral_plus | 11 | 0.506 | +0.002 | +0.005 | saturated | 0.511 | 0.511 | 1.000 | 1.000 | 9 | 3.6e-14 | 289 |
| MITOSA | fs0/k3 | neutral_plus | 12 | 0.501 | -0.005 | +0.001 | saturated | 0.502 | 0.503 | 1.000 | 1.000 | 15 | 2.9e-14 | 289 |
| MITOSA | fs0/k3 | neutral_plus | 13 | 0.504 | -0.013 | -0.009 | saturated | 0.504 | 0.510 | 1.000 | 1.000 | 11 | 3.1e-14 | 289 |
| MITOSA | fs0/k3 | neutral_plus | 14 | 0.500 | -0.006 | -0.009 | saturated | 0.509 | 0.510 | 1.000 | 1.000 | 19 | 3.2e-14 | 289 |
| MITOSA | fs0/k3 | neutral_plus | 15 | 0.503 | -0.001 | -0.000 | saturated | 0.498 | 0.500 | 1.000 | 1.000 | 17 | 2.4e-14 | 289 |
| MITOSA | fs0/k3 | neutral_plus | 16 | 0.499 | -0.009 | -0.007 | saturated | 0.508 | 0.516 | 1.000 | 1.000 | 15 | 4.1e-14 | 289 |
| MITOSA | fs0/k3 | neutral_plus | 17 | 0.504 | +0.004 | -0.002 | saturated | 0.498 | 0.498 | 1.000 | 1.000 | 19 | 3.2e-14 | 289 |
| MITOSA | fs0/k3 | neutral_plus | 18 | 0.493 | +0.017 | +0.012 | saturated | 0.505 | 0.513 | 1.000 | 1.000 | 21 | 1.9e-14 | 288 |
| MITOSA | fs0/k3 | neutral_plus | 19 | 0.498 | +0.015 | +0.012 | saturated | 0.510 | 0.514 | 1.000 | 1.000 | 10 | 3.2e-14 | 288 |
| MITOSA | fs0/k3 | neutral_plus | 20 | 0.499 | +0.005 | +0.003 | saturated | 0.501 | 0.507 | 1.000 | 1.000 | 10 | 2.7e-14 | 288 |
| MITOSA | fs0/k3 | neutral_plus | 21 | 0.495 | +0.006 | -0.003 | saturated | 0.508 | 0.508 | 1.000 | 1.000 | 10 | 3.4e-14 | 288 |
| MITOSA | fs0/k3 | neutral_plus | 22 | 0.501 | -0.004 | -0.002 | saturated | 0.501 | 0.503 | 1.000 | 1.000 | 15 | 3.0e-14 | 288 |
| MITOSA | fs0/k3 | neutral_plus | 23 | 0.504 | +0.015 | +0.012 | saturated | 0.516 | 0.519 | 0.991 | 1.000 | 11 | 3.9e-14 | 288 |
| MITOSA | fs0/k3 | neutral_plus | 24 | 0.505 | -0.007 | -0.003 | saturated | 0.498 | 0.505 | 1.000 | 1.000 | 19 | 3.0e-14 | 288 |
| MITOSA | fs0/k3 | neutral_plus | 25 | 0.500 | +0.012 | +0.005 | saturated | 0.505 | 0.513 | 1.000 | 1.000 | 15 | 2.4e-14 | 288 |
| MITOSA | fs0/k3 | neutral_plus | 26 | 0.499 | -0.003 | +0.007 | saturated | 0.506 | 0.507 | 1.000 | 1.000 | 5 | 3.2e-14 | 288 |
| MITOSA | fs0/k3 | neutral_plus | 27 | 0.491 | -0.004 | -0.002 | saturated | 0.510 | 0.513 | 1.000 | 1.000 | 12 | 3.8e-14 | 288 |
| MITOSA | fs0/k3 | neutral_plus | 28 | 0.499 | +0.004 | +0.003 | saturated | 0.502 | 0.502 | 1.000 | 1.000 | 9 | 3.8e-14 | 287 |
| MITOSA | fs0/k3 | neutral_plus | 29 | 0.508 | -0.010 | -0.013 | saturated | 0.505 | 0.505 | 1.000 | 1.000 | 17 | 2.6e-14 | 287 |
| MITOSA | fs0/k3 | neutral_plus | 30 | 0.498 | +0.009 | +0.010 | saturated | 0.508 | 0.508 | 0.891 | 1.000 | 12 | 3.0e-14 | 287 |
| MITOSA | fs0/k3 | neutral_plus | 31 | 0.499 | +0.017 | +0.034 | saturated | 0.532 | 0.533 | 1.000 | 1.000 | 16 | 3.0e-14 | 287 |
| MITOSA | fs0/k3 | neutral_plus | 32 | 0.504 | -0.006 | +0.010 | saturated | 0.514 | 0.515 | 0.999 | 1.000 | 10 | 3.8e-14 | 287 |
| MITOSA | fs0/k3 | neutral_plus | 33 | 0.495 | -0.007 | -0.007 | saturated | 0.512 | 0.513 | 1.000 | 1.000 | 15 | 3.2e-14 | 287 |
| MITOSA | fs0/k3 | neutral_plus | 34 | 0.501 | -0.000 | -0.004 | saturated | 0.502 | 0.504 | 1.000 | 1.000 | 22 | 2.5e-14 | 287 |
| MITOSA | fs0/k3 | neutral_plus | 35 | 0.497 | +0.004 | +0.002 | saturated | 0.499 | 0.501 | 1.000 | 1.000 | 8 | 3.6e-14 | 287 |
| MITOSA | fs0/k3 | neutral_plus | 36 | 0.500 | +0.000 | +0.001 | saturated | 0.502 | 0.504 | 1.000 | 1.000 | 10 | 3.7e-14 | 287 |
| MITOSA | fs0/k3 | neutral_plus | 37 | 0.502 | +0.001 | +0.006 | saturated | 0.508 | 0.508 | 1.000 | 1.000 | 14 | 3.5e-14 | 287 |
| MITOSA | fs0/k3 | neutral_plus | 38 | 0.507 | -0.017 | -0.008 | saturated | 0.501 | 0.511 | 0.968 | 1.000 | 7 | 3.2e-14 | 284 |
| MITOSA | fs0/k3 | neutral_plus | 39 | 0.504 | -0.002 | -0.004 | saturated | 0.500 | 0.500 | 1.000 | 1.000 | 12 | 3.7e-14 | 284 |
| MITOSA | fs0/k3 | neutral_plus | 40 | 0.497 | +0.016 | +0.004 | saturated | 0.501 | 0.513 | 1.000 | 1.000 | 18 | 2.9e-14 | 284 |
| MITOSA | fs0/k3 | neutral_plus | 41 | 0.500 | -0.015 | -0.009 | saturated | 0.509 | 0.516 | 1.000 | 1.000 | 8 | 2.6e-14 | 284 |
| MITOSA | fs0/k3 | neutral_plus | 42 | 0.502 | -0.001 | -0.005 | saturated | 0.504 | 0.506 | 1.000 | 1.000 | 12 | 3.7e-14 | 284 |
| MITOSA | fs0/k3 | neutral_plus | 43 | 0.500 | +0.014 | +0.006 | saturated | 0.506 | 0.516 | 1.000 | 1.000 | 16 | 3.7e-14 | 284 |
| MITOSA | fs0/k3 | neutral_plus | 44 | 0.496 | -0.004 | -0.007 | saturated | 0.511 | 0.511 | 0.999 | 1.000 | 23 | 2.0e-14 | 284 |
| MITOSA | fs0/k3 | neutral_plus | 45 | 0.498 | +0.006 | +0.004 | saturated | 0.501 | 0.504 | 1.000 | 1.000 | 12 | 3.0e-14 | 284 |
| MITOSA | fs0/k3 | neutral_plus | 46 | 0.505 | +0.031 | +0.045 | saturated | 0.550 | 0.550 | 0.796 | 1.000 | 13 | 2.9e-14 | 284 |
| MITOSA | fs0/k3 | neutral_plus | 47 | 0.497 | -0.001 | +0.004 | saturated | 0.501 | 0.502 | 0.975 | 1.000 | 8 | 3.7e-14 | 284 |
| MITOSA | fs0/k3 | neutral_plus | 48 | 0.499 | -0.024 | -0.021 | saturated | 0.522 | 0.526 | 1.000 | 1.000 | 12 | 3.1e-14 | 223 |
| MITOSA | fs0/k3 | neutral_plus | 49 | 0.499 | +0.000 | +0.004 | saturated | 0.503 | 0.505 | 0.922 | 1.000 | 21 | 1.9e-14 | 223 |
| MITOSA | fs0/k3 | neutral_plus | 50 | 0.500 | -0.007 | -0.005 | saturated | 0.506 | 0.507 | 1.000 | 1.000 | 15 | 3.0e-14 | 223 |
| MITOSA | fs0/k3 | neutral_minus | 1 | 0.501 | -0.026 | -0.026 | saturated | 0.525 | 0.525 | 1.000 | 1.000 | 5 | 1.1e-14 | 15458 |
| MITOSA | fs0/k3 | neutral_minus | 2 | 0.495 | +0.053 | +0.053 | saturated | 0.548 | 0.549 | 1.000 | 1.000 | 2 | 8.9e-15 | 15311 |
| MITOSA | fs0/k3 | neutral_minus | 3 | 0.499 | -0.010 | -0.010 | saturated | 0.511 | 0.512 | 1.000 | 1.000 | 5 | 9.1e-15 | 16714 |
| MITOSA | fs0/k3 | neutral_minus | 4 | 0.498 | +0.030 | +0.030 | saturated | 0.528 | 0.531 | 0.977 | 1.000 | 3 | 8.9e-15 | 16810 |
| MITOSA | fs0/k3 | neutral_minus | 5 | 0.502 | +0.010 | +0.010 | saturated | 0.512 | 0.514 | 1.000 | 1.000 | 6 | 1.0e-14 | 16946 |
| MITOSA | fs0/k3 | neutral_minus | 6 | 0.493 | +0.003 | +0.003 | saturated | 0.495 | 0.511 | 1.000 | 1.000 | 9 | 1.0e-14 | 16651 |
| MITOSA | fs0/k3 | neutral_minus | 7 | 0.499 | -0.067 | -0.067 | saturated | 0.568 | 0.568 | 1.000 | 1.000 | 3 | 1.0e-14 | 16580 |
| MITOSA | fs0/k3 | neutral_minus | 8 | 0.499 | +0.066 | +0.066 | saturated | 0.566 | 0.566 | 0.995 | 1.000 | 7 | 3.0e-15 | 289 |
| MITOSA | fs0/k3 | neutral_minus | 9 | 0.502 | +0.087 | +0.087 | saturated | 0.589 | 0.590 | 0.819 | 1.000 | 17 | 2.5e-15 | 289 |
| MITOSA | fs0/k3 | neutral_minus | 10 | 0.506 | +0.020 | +0.021 | saturated | 0.527 | 0.529 | 1.000 | 1.000 | 5 | 4.1e-15 | 289 |
| MITOSA | fs0/k3 | neutral_minus | 11 | 0.506 | -0.085 | -0.084 | saturated | 0.578 | 0.580 | 0.961 | 1.000 | 4 | 4.3e-15 | 289 |
| MITOSA | fs0/k3 | neutral_minus | 12 | 0.501 | -0.012 | -0.012 | saturated | 0.510 | 0.510 | 1.000 | 1.000 | 4 | 3.6e-15 | 289 |
| MITOSA | fs0/k3 | neutral_minus | 13 | 0.504 | -0.046 | -0.046 | saturated | 0.542 | 0.542 | 1.000 | 1.000 | 6 | 2.6e-15 | 289 |
| MITOSA | fs0/k3 | neutral_minus | 14 | 0.500 | +0.028 | +0.028 | saturated | 0.528 | 0.528 | 0.974 | 1.000 | 4 | 3.5e-15 | 289 |
| MITOSA | fs0/k3 | neutral_minus | 15 | 0.503 | -0.014 | -0.014 | saturated | 0.511 | 0.512 | 1.000 | 1.000 | 7 | 3.4e-15 | 289 |
| MITOSA | fs0/k3 | neutral_minus | 16 | 0.499 | -0.030 | -0.030 | saturated | 0.531 | 0.532 | 1.000 | 1.000 | 4 | 3.8e-15 | 289 |
| MITOSA | fs0/k3 | neutral_minus | 17 | 0.504 | -0.010 | -0.011 | saturated | 0.506 | 0.519 | 1.000 | 1.000 | 3 | 4.6e-15 | 289 |
| MITOSA | fs0/k3 | neutral_minus | 18 | 0.493 | +0.018 | +0.018 | saturated | 0.510 | 0.511 | 1.000 | 1.000 | 5 | 2.7e-15 | 288 |
| MITOSA | fs0/k3 | neutral_minus | 19 | 0.498 | +0.003 | +0.002 | saturated | 0.500 | 0.507 | 0.856 | 1.000 | 2 | 2.4e-15 | 288 |
| MITOSA | fs0/k3 | neutral_minus | 20 | 0.499 | +0.018 | +0.018 | saturated | 0.517 | 0.518 | 1.000 | 1.000 | 7 | 4.4e-15 | 288 |
| MITOSA | fs0/k3 | neutral_minus | 21 | 0.495 | -0.007 | -0.007 | saturated | 0.512 | 0.515 | 1.000 | 1.000 | 3 | 1.5e-15 | 288 |
| MITOSA | fs0/k3 | neutral_minus | 22 | 0.501 | -0.031 | -0.032 | saturated | 0.531 | 0.531 | 0.954 | 1.000 | 6 | 4.5e-15 | 288 |
| MITOSA | fs0/k3 | neutral_minus | 23 | 0.504 | +0.011 | +0.011 | saturated | 0.515 | 0.516 | 1.000 | 1.000 | 5 | 3.2e-15 | 288 |
| MITOSA | fs0/k3 | neutral_minus | 24 | 0.505 | -0.039 | -0.040 | saturated | 0.534 | 0.534 | 1.000 | 1.000 | 6 | 1.6e-15 | 288 |
| MITOSA | fs0/k3 | neutral_minus | 25 | 0.500 | -0.113 | -0.113 | saturated | 0.612 | 0.614 | 1.000 | 1.000 | 5 | 2.3e-15 | 288 |
| MITOSA | fs0/k3 | neutral_minus | 26 | 0.499 | +0.028 | +0.028 | saturated | 0.527 | 0.529 | 0.923 | 1.000 | 7 | 3.6e-15 | 288 |
| MITOSA | fs0/k3 | neutral_minus | 27 | 0.491 | +0.011 | +0.010 | saturated | 0.501 | 0.502 | 1.000 | 1.000 | 6 | 3.0e-15 | 288 |
| MITOSA | fs0/k3 | neutral_minus | 28 | 0.499 | +0.038 | +0.038 | saturated | 0.537 | 0.538 | 0.855 | 1.000 | 6 | 4.2e-15 | 287 |
| MITOSA | fs0/k3 | neutral_minus | 29 | 0.508 | +0.066 | +0.066 | saturated | 0.575 | 0.575 | 1.000 | 1.000 | 5 | 2.6e-15 | 287 |
| MITOSA | fs0/k3 | neutral_minus | 30 | 0.498 | +0.008 | +0.007 | saturated | 0.505 | 0.505 | 1.000 | 1.000 | 7 | 2.3e-15 | 287 |
| MITOSA | fs0/k3 | neutral_minus | 31 | 0.499 | +0.013 | +0.013 | saturated | 0.511 | 0.512 | 1.000 | 1.000 | 7 | 3.2e-15 | 287 |
| MITOSA | fs0/k3 | neutral_minus | 32 | 0.504 | -0.057 | -0.057 | saturated | 0.552 | 0.553 | 1.000 | 1.000 | 4 | 4.4e-15 | 287 |
| MITOSA | fs0/k3 | neutral_minus | 33 | 0.495 | -0.022 | -0.022 | saturated | 0.528 | 0.528 | 1.000 | 1.000 | 6 | 1.1e-15 | 287 |
| MITOSA | fs0/k3 | neutral_minus | 34 | 0.501 | -0.024 | -0.023 | saturated | 0.522 | 0.523 | 1.000 | 1.000 | 6 | 4.6e-15 | 287 |
| MITOSA | fs0/k3 | neutral_minus | 35 | 0.497 | +0.013 | +0.012 | saturated | 0.510 | 0.512 | 0.949 | 1.000 | 13 | 3.2e-15 | 287 |
| MITOSA | fs0/k3 | neutral_minus | 36 | 0.500 | +0.011 | +0.011 | saturated | 0.511 | 0.511 | 1.000 | 1.000 | 5 | 2.8e-15 | 287 |
| MITOSA | fs0/k3 | neutral_minus | 37 | 0.502 | +0.008 | +0.008 | saturated | 0.510 | 0.512 | 1.000 | 1.000 | 8 | 1.2e-15 | 287 |
| MITOSA | fs0/k3 | neutral_minus | 38 | 0.507 | -0.003 | -0.003 | saturated | 0.496 | 0.529 | 0.902 | 1.000 | 4 | 4.4e-15 | 284 |
| MITOSA | fs0/k3 | neutral_minus | 39 | 0.504 | +0.012 | +0.012 | saturated | 0.517 | 0.517 | 1.000 | 1.000 | 12 | 2.9e-15 | 284 |
| MITOSA | fs0/k3 | neutral_minus | 40 | 0.497 | -0.002 | -0.002 | saturated | 0.506 | 0.506 | 1.000 | 1.000 | 11 | 1.7e-15 | 284 |
| MITOSA | fs0/k3 | neutral_minus | 41 | 0.500 | -0.047 | -0.047 | saturated | 0.547 | 0.547 | 1.000 | 1.000 | 5 | 3.1e-15 | 284 |
| MITOSA | fs0/k3 | neutral_minus | 42 | 0.502 | +0.027 | +0.027 | saturated | 0.529 | 0.529 | 1.000 | 1.000 | 5 | 3.7e-15 | 284 |
| MITOSA | fs0/k3 | neutral_minus | 43 | 0.500 | +0.032 | +0.032 | saturated | 0.531 | 0.531 | 1.000 | 1.000 | 4 | 2.9e-15 | 284 |
| MITOSA | fs0/k3 | neutral_minus | 44 | 0.496 | -0.000 | +0.000 | saturated | 0.496 | 0.498 | 0.610 | 1.000 | 3 | 5.1e-15 | 284 |
| MITOSA | fs0/k3 | neutral_minus | 45 | 0.498 | -0.033 | -0.033 | saturated | 0.535 | 0.535 | 1.000 | 1.000 | 7 | 2.5e-15 | 284 |
| MITOSA | fs0/k3 | neutral_minus | 46 | 0.505 | +0.004 | +0.003 | saturated | 0.509 | 0.518 | 1.000 | 1.000 | 5 | 4.3e-15 | 284 |
| MITOSA | fs0/k3 | neutral_minus | 47 | 0.497 | -0.015 | -0.014 | saturated | 0.518 | 0.518 | 0.927 | 1.000 | 6 | 4.2e-15 | 284 |
| MITOSA | fs0/k3 | neutral_minus | 48 | 0.499 | -0.019 | -0.019 | saturated | 0.520 | 0.521 | 0.950 | 1.000 | 4 | 3.3e-15 | 223 |
| MITOSA | fs0/k3 | neutral_minus | 49 | 0.499 | -0.010 | -0.010 | saturated | 0.510 | 0.510 | 0.911 | 1.000 | 6 | 3.0e-15 | 223 |
| MITOSA | fs0/k3 | neutral_minus | 50 | 0.500 | +0.002 | +0.002 | saturated | 0.502 | 0.506 | 1.000 | 1.000 | 3 | 2.3e-15 | 223 |
| MITOSA | fs10/k3 | treat | 1 | 0.501 | -0.002 | +0.111 | reverses | 0.612 | 0.695 | 0.004 | 0.383 | 5 | 1.7e-15 | 18143 |
| MITOSA | fs10/k3 | treat | 2 | 0.495 | +0.018 | +0.088 | grows | 0.583 | 0.625 | 0.000 | 0.000 | 2 | 1.1e-14 | 18155 |
| MITOSA | fs10/k3 | treat | 3 | 0.499 | +0.019 | -0.117 | reverses | 0.618 | 0.634 | 0.001 | 0.000 | 2 | 4.5e-15 | 19615 |
| MITOSA | fs10/k3 | treat | 4 | 0.498 | +0.057 | +0.032 | saturated | 0.530 | 0.694 | 0.001 | 0.517 | 2 | 3.8e-15 | 19391 |
| MITOSA | fs10/k3 | treat | 5 | 0.502 | +0.003 | -0.101 | reverses | 0.599 | 0.600 | 0.014 | 1.000 | 11 | 5.1e-15 | 19473 |
| MITOSA | fs10/k3 | treat | 6 | 0.493 | +0.057 | -0.028 | reverses | 0.535 | 0.540 | 0.007 | 1.000 | 2 | 7.2e-15 | 19260 |
| MITOSA | fs10/k3 | treat | 7 | 0.499 | +0.014 | +0.045 | saturated | 0.544 | 0.598 | 0.011 | 0.527 | 3 | 3.7e-15 | 19478 |
| MITOSA | fs10/k3 | treat | 8 | 0.499 | +0.037 | -0.376 | reverses | 0.876 | 0.888 | 0.002 | 0.000 | 8 | 3.5e-15 | 379 |
| MITOSA | fs10/k3 | treat | 9 | 0.502 | -0.016 | -0.347 | grows | 0.845 | 0.854 | 0.005 | 0.000 | 7 | 5.6e-15 | 379 |
| MITOSA | fs10/k3 | treat | 10 | 0.506 | -0.061 | +0.024 | reverses | 0.530 | 0.663 | 0.009 | 0.535 | 2 | 5.0e-15 | 379 |
| MITOSA | fs10/k3 | treat | 11 | 0.506 | +0.014 | -0.346 | reverses | 0.840 | 0.843 | 0.001 | 0.996 | 1 | 1.5e-14 | 379 |
| MITOSA | fs10/k3 | treat | 12 | 0.501 | +0.005 | +0.142 | grows | 0.643 | 0.713 | 0.003 | 0.348 | 2 | 1.1e-14 | 379 |
| MITOSA | fs10/k3 | treat | 13 | 0.504 | +0.047 | +0.192 | grows | 0.696 | 0.711 | 0.007 | 0.998 | 1 | 6.1e-15 | 379 |
| MITOSA | fs10/k3 | treat | 14 | 0.500 | +0.099 | +0.145 | saturated | 0.645 | 0.700 | 0.007 | 0.984 | 1 | 8.4e-15 | 379 |
| MITOSA | fs10/k3 | treat | 15 | 0.503 | +0.056 | +0.089 | saturated | 0.592 | 0.678 | 0.000 | 0.000 | 3 | 9.4e-15 | 379 |
| MITOSA | fs10/k3 | treat | 16 | 0.499 | +0.087 | +0.394 | grows | 0.893 | 0.901 | 0.000 | 0.000 | 2 | 1.1e-14 | 379 |
| MITOSA | fs10/k3 | treat | 17 | 0.504 | +0.040 | +0.094 | grows | 0.598 | 0.739 | 0.008 | 0.461 | 2 | 1.8e-14 | 379 |
| MITOSA | fs10/k3 | treat | 18 | 0.493 | +0.118 | +0.159 | saturated | 0.652 | 0.654 | 0.010 | 1.000 | 2 | 6.7e-15 | 375 |
| MITOSA | fs10/k3 | treat | 19 | 0.498 | +0.048 | -0.405 | reverses | 0.907 | 0.912 | 0.010 | 0.000 | 1 | 1.1e-14 | 375 |
| MITOSA | fs10/k3 | treat | 20 | 0.499 | -0.041 | +0.000 | saturated | 0.499 | 0.655 | 0.012 | 0.000 | 2 | 7.7e-15 | 375 |
| MITOSA | fs10/k3 | treat | 21 | 0.495 | +0.026 | -0.223 | reverses | 0.728 | 0.747 | 0.020 | 0.938 | 5 | 1.2e-14 | 375 |
| MITOSA | fs10/k3 | treat | 22 | 0.501 | +0.048 | +0.048 | saturated | 0.549 | 0.663 | 0.001 | 0.000 | 4 | 1.1e-14 | 375 |
| MITOSA | fs10/k3 | treat | 23 | 0.504 | +0.093 | +0.118 | saturated | 0.622 | 0.690 | 0.003 | 0.000 | 3 | 1.3e-14 | 375 |
| MITOSA | fs10/k3 | treat | 24 | 0.505 | +0.033 | +0.030 | saturated | 0.535 | 0.634 | 0.007 | 0.000 | 3 | 1.2e-14 | 375 |
| MITOSA | fs10/k3 | treat | 25 | 0.500 | +0.077 | -0.015 | reverses | 0.514 | 0.527 | 0.104 | 1.000 | 16 | 6.7e-15 | 375 |
| MITOSA | fs10/k3 | treat | 26 | 0.499 | +0.077 | +0.196 | grows | 0.695 | 0.752 | 0.001 | 0.000 | 3 | 7.9e-15 | 375 |
| MITOSA | fs10/k3 | treat | 27 | 0.491 | +0.107 | +0.486 | grows | 0.977 | 0.977 | 0.002 | 0.000 | 1 | 7.5e-15 | 375 |
| MITOSA | fs10/k3 | treat | 28 | 0.499 | +0.107 | -0.087 | reverses | 0.589 | 0.605 | 0.026 | 0.776 | 2 | 1.2e-14 | 384 |
| MITOSA | fs10/k3 | treat | 29 | 0.508 | -0.027 | -0.399 | grows | 0.891 | 0.896 | 0.007 | 0.000 | 9 | 3.3e-15 | 384 |
| MITOSA | fs10/k3 | treat | 30 | 0.498 | +0.073 | -0.055 | reverses | 0.557 | 0.568 | 0.057 | 0.702 | 2 | 1.5e-14 | 384 |
| MITOSA | fs10/k3 | treat | 31 | 0.499 | +0.053 | +0.011 | saturated | 0.509 | 0.613 | 0.004 | 0.000 | 4 | 1.3e-14 | 384 |
| MITOSA | fs10/k3 | treat | 32 | 0.504 | -0.006 | +0.013 | saturated | 0.518 | 0.608 | 0.006 | 0.559 | 3 | 1.8e-14 | 384 |
| MITOSA | fs10/k3 | treat | 33 | 0.495 | +0.009 | +0.129 | grows | 0.623 | 0.673 | 0.006 | 1.000 | 2 | 5.8e-15 | 384 |
| MITOSA | fs10/k3 | treat | 34 | 0.501 | -0.071 | -0.004 | shrinks | 0.502 | 0.571 | 0.002 | 0.000 | 2 | 1.2e-14 | 384 |
| MITOSA | fs10/k3 | treat | 35 | 0.497 | +0.055 | -0.369 | reverses | 0.872 | 0.873 | 0.003 | 1.000 | 5 | 1.5e-14 | 384 |
| MITOSA | fs10/k3 | treat | 36 | 0.500 | +0.047 | -0.037 | reverses | 0.537 | 0.537 | 0.012 | 1.000 | 15 | 7.2e-15 | 384 |
| MITOSA | fs10/k3 | treat | 37 | 0.502 | +0.059 | -0.079 | reverses | 0.576 | 0.581 | 0.001 | 1.000 | 12 | 2.6e-15 | 384 |
| MITOSA | fs10/k3 | treat | 38 | 0.507 | +0.029 | -0.064 | reverses | 0.558 | 0.637 | 0.005 | 0.000 | 2 | 1.4e-14 | 381 |
| MITOSA | fs10/k3 | treat | 39 | 0.504 | -0.000 | +0.002 | saturated | 0.506 | 0.563 | 0.041 | 1.000 | 19 | 4.2e-15 | 381 |
| MITOSA | fs10/k3 | treat | 40 | 0.497 | +0.003 | -0.056 | reverses | 0.560 | 0.562 | 0.008 | 1.000 | 17 | 5.3e-15 | 381 |
| MITOSA | fs10/k3 | treat | 41 | 0.500 | +0.096 | -0.208 | reverses | 0.708 | 0.719 | 0.005 | 0.000 | 3 | 1.5e-14 | 381 |
| MITOSA | fs10/k3 | treat | 42 | 0.502 | +0.052 | +0.463 | grows | 0.965 | 0.965 | 0.002 | 0.000 | 1 | 1.1e-14 | 381 |
| MITOSA | fs10/k3 | treat | 43 | 0.500 | +0.102 | +0.214 | grows | 0.714 | 0.769 | 0.002 | 0.000 | 6 | 1.2e-14 | 381 |
| MITOSA | fs10/k3 | treat | 44 | 0.496 | -0.023 | +0.002 | saturated | 0.497 | 0.699 | 0.009 | 0.000 | 2 | 4.4e-15 | 381 |
| MITOSA | fs10/k3 | treat | 45 | 0.498 | +0.064 | -0.396 | reverses | 0.899 | 0.922 | 0.002 | 0.000 | 2 | 1.6e-14 | 381 |
| MITOSA | fs10/k3 | treat | 46 | 0.505 | +0.015 | -0.406 | reverses | 0.901 | 0.903 | 0.000 | 0.000 | 1 | 1.1e-14 | 381 |
| MITOSA | fs10/k3 | treat | 47 | 0.497 | +0.011 | -0.407 | reverses | 0.910 | 0.926 | 0.000 | 0.000 | 14 | 8.9e-15 | 381 |
| MITOSA | fs10/k3 | treat | 48 | 0.499 | +0.053 | -0.257 | reverses | 0.758 | 0.779 | 0.012 | 0.909 | 3 | 1.6e-14 | 295 |
| MITOSA | fs10/k3 | treat | 49 | 0.499 | +0.038 | +0.063 | saturated | 0.562 | 0.731 | 0.000 | 0.000 | 2 | 6.0e-15 | 295 |
| MITOSA | fs10/k3 | treat | 50 | 0.500 | +0.098 | +0.301 | grows | 0.800 | 0.821 | 0.003 | 0.206 | 5 | 1.0e-14 | 295 |
| MITOSA | fs10/k3 | neutral_plus | 1 | 0.501 | -0.033 | -0.023 | saturated | 0.522 | 0.533 | 1.000 | 1.000 | 4 | 3.7e-15 | 18345 |
| MITOSA | fs10/k3 | neutral_plus | 2 | 0.495 | -0.008 | +0.030 | saturated | 0.525 | 0.525 | 0.000 | 1.000 | 1 | 1.6e-14 | 18548 |
| MITOSA | fs10/k3 | neutral_plus | 3 | 0.499 | -0.017 | +0.052 | reverses | 0.551 | 0.562 | 0.001 | 0.000 | 2 | 6.8e-15 | 19752 |
| MITOSA | fs10/k3 | neutral_plus | 4 | 0.498 | -0.003 | -0.019 | saturated | 0.521 | 0.522 | 0.622 | 1.000 | 4 | 4.0e-15 | 19087 |
| MITOSA | fs10/k3 | neutral_plus | 5 | 0.502 | +0.001 | +0.017 | saturated | 0.520 | 0.525 | 0.598 | 1.000 | 12 | 3.9e-15 | 19446 |
| MITOSA | fs10/k3 | neutral_plus | 6 | 0.493 | +0.000 | -0.013 | saturated | 0.520 | 0.526 | 0.565 | 1.000 | 12 | 5.5e-15 | 19269 |
| MITOSA | fs10/k3 | neutral_plus | 7 | 0.499 | +0.001 | -0.035 | saturated | 0.536 | 0.537 | 1.000 | 1.000 | 3 | 2.9e-15 | 19320 |
| MITOSA | fs10/k3 | neutral_plus | 8 | 0.499 | +0.012 | +0.036 | saturated | 0.535 | 0.537 | 0.001 | 0.880 | 3 | 1.0e-14 | 379 |
| MITOSA | fs10/k3 | neutral_plus | 9 | 0.502 | +0.020 | +0.001 | saturated | 0.503 | 0.526 | 0.218 | 0.899 | 3 | 6.9e-15 | 379 |
| MITOSA | fs10/k3 | neutral_plus | 10 | 0.506 | -0.004 | +0.004 | saturated | 0.510 | 0.510 | 0.513 | 1.000 | 1 | 2.2e-14 | 379 |
| MITOSA | fs10/k3 | neutral_plus | 11 | 0.506 | -0.010 | -0.152 | grows | 0.646 | 0.647 | 0.004 | 0.076 | 9 | 1.4e-14 | 379 |
| MITOSA | fs10/k3 | neutral_plus | 12 | 0.501 | +0.007 | -0.008 | saturated | 0.507 | 0.509 | 1.000 | 1.000 | 6 | 1.0e-14 | 379 |
| MITOSA | fs10/k3 | neutral_plus | 13 | 0.504 | -0.005 | -0.023 | saturated | 0.518 | 0.526 | 0.452 | 1.000 | 3 | 8.8e-15 | 379 |
| MITOSA | fs10/k3 | neutral_plus | 14 | 0.500 | -0.002 | +0.008 | saturated | 0.508 | 0.513 | 0.002 | 0.825 | 6 | 8.2e-15 | 379 |
| MITOSA | fs10/k3 | neutral_plus | 15 | 0.503 | -0.004 | +0.047 | reverses | 0.550 | 0.553 | 0.001 | 0.928 | 2 | 1.4e-14 | 379 |
| MITOSA | fs10/k3 | neutral_plus | 16 | 0.499 | +0.006 | -0.014 | saturated | 0.515 | 0.515 | 0.000 | 1.000 | 1 | 1.8e-14 | 379 |
| MITOSA | fs10/k3 | neutral_plus | 17 | 0.504 | +0.015 | +0.059 | saturated | 0.563 | 0.564 | 0.416 | 0.816 | 12 | 7.7e-15 | 379 |
| MITOSA | fs10/k3 | neutral_plus | 18 | 0.493 | -0.005 | +0.002 | saturated | 0.494 | 0.506 | 0.002 | 0.886 | 3 | 1.2e-14 | 375 |
| MITOSA | fs10/k3 | neutral_plus | 19 | 0.498 | +0.008 | -0.052 | reverses | 0.554 | 0.559 | 0.277 | 0.346 | 13 | 5.3e-15 | 375 |
| MITOSA | fs10/k3 | neutral_plus | 20 | 0.499 | -0.011 | +0.002 | saturated | 0.501 | 0.505 | 1.000 | 1.000 | 9 | 5.4e-15 | 375 |
| MITOSA | fs10/k3 | neutral_plus | 21 | 0.495 | +0.029 | +0.080 | grows | 0.575 | 0.583 | 0.215 | 0.580 | 19 | 3.9e-15 | 375 |
| MITOSA | fs10/k3 | neutral_plus | 22 | 0.501 | -0.004 | -0.060 | grows | 0.558 | 0.568 | 0.002 | 1.000 | 3 | 4.0e-15 | 375 |
| MITOSA | fs10/k3 | neutral_plus | 23 | 0.504 | +0.006 | +0.026 | saturated | 0.530 | 0.534 | 0.001 | 0.947 | 4 | 7.2e-15 | 375 |
| MITOSA | fs10/k3 | neutral_plus | 24 | 0.505 | +0.005 | +0.017 | saturated | 0.522 | 0.529 | 0.125 | 0.889 | 3 | 6.1e-15 | 375 |
| MITOSA | fs10/k3 | neutral_plus | 25 | 0.500 | +0.007 | +0.017 | saturated | 0.517 | 0.522 | 0.098 | 0.940 | 2 | 9.9e-15 | 375 |
| MITOSA | fs10/k3 | neutral_plus | 26 | 0.499 | -0.006 | -0.049 | saturated | 0.549 | 0.563 | 0.001 | 0.809 | 6 | 6.6e-15 | 375 |
| MITOSA | fs10/k3 | neutral_plus | 27 | 0.491 | +0.008 | +0.058 | saturated | 0.549 | 0.554 | 0.001 | 0.948 | 3 | 5.4e-15 | 375 |
| MITOSA | fs10/k3 | neutral_plus | 28 | 0.499 | -0.006 | -0.023 | saturated | 0.525 | 0.525 | 0.114 | 0.175 | 13 | 7.1e-15 | 384 |
| MITOSA | fs10/k3 | neutral_plus | 29 | 0.508 | +0.005 | +0.048 | saturated | 0.557 | 0.557 | 0.181 | 0.949 | 2 | 8.8e-15 | 384 |
| MITOSA | fs10/k3 | neutral_plus | 30 | 0.498 | -0.004 | +0.010 | saturated | 0.507 | 0.520 | 0.001 | 0.895 | 4 | 5.9e-15 | 384 |
| MITOSA | fs10/k3 | neutral_plus | 31 | 0.499 | +0.005 | -0.004 | saturated | 0.506 | 0.506 | 0.001 | 0.857 | 3 | 7.2e-15 | 384 |
| MITOSA | fs10/k3 | neutral_plus | 32 | 0.504 | +0.006 | -0.016 | saturated | 0.511 | 0.516 | 1.000 | 1.000 | 3 | 3.7e-15 | 384 |
| MITOSA | fs10/k3 | neutral_plus | 33 | 0.495 | -0.007 | -0.037 | saturated | 0.542 | 0.546 | 0.600 | 1.000 | 2 | 9.9e-15 | 384 |
| MITOSA | fs10/k3 | neutral_plus | 34 | 0.501 | -0.003 | -0.018 | saturated | 0.517 | 0.518 | 1.000 | 1.000 | 1 | 2.1e-14 | 384 |
| MITOSA | fs10/k3 | neutral_plus | 35 | 0.497 | +0.003 | +0.005 | saturated | 0.503 | 0.511 | 0.004 | 0.120 | 18 | 2.5e-15 | 384 |
| MITOSA | fs10/k3 | neutral_plus | 36 | 0.500 | -0.020 | -0.007 | saturated | 0.507 | 0.521 | 0.550 | 0.945 | 3 | 9.1e-15 | 384 |
| MITOSA | fs10/k3 | neutral_plus | 37 | 0.502 | -0.024 | -0.008 | saturated | 0.506 | 0.525 | 0.553 | 1.000 | 3 | 4.6e-15 | 384 |
| MITOSA | fs10/k3 | neutral_plus | 38 | 0.507 | -0.018 | -0.047 | saturated | 0.540 | 0.540 | 0.257 | 0.258 | 11 | 1.1e-14 | 381 |
| MITOSA | fs10/k3 | neutral_plus | 39 | 0.504 | +0.005 | +0.007 | saturated | 0.512 | 0.524 | 0.004 | 0.897 | 3 | 9.7e-15 | 381 |
| MITOSA | fs10/k3 | neutral_plus | 40 | 0.497 | -0.015 | -0.033 | saturated | 0.537 | 0.537 | 0.064 | 0.503 | 16 | 2.6e-15 | 381 |
| MITOSA | fs10/k3 | neutral_plus | 41 | 0.500 | -0.014 | -0.013 | saturated | 0.513 | 0.514 | 0.408 | 0.510 | 14 | 4.7e-15 | 381 |
| MITOSA | fs10/k3 | neutral_plus | 42 | 0.502 | +0.002 | +0.014 | saturated | 0.516 | 0.522 | 0.033 | 1.000 | 3 | 5.4e-15 | 381 |
| MITOSA | fs10/k3 | neutral_plus | 43 | 0.500 | -0.011 | +0.001 | saturated | 0.501 | 0.510 | 0.079 | 0.903 | 3 | 9.8e-15 | 381 |
| MITOSA | fs10/k3 | neutral_plus | 44 | 0.496 | -0.032 | -0.112 | grows | 0.616 | 0.620 | 1.000 | 1.000 | 6 | 2.8e-15 | 381 |
| MITOSA | fs10/k3 | neutral_plus | 45 | 0.498 | +0.025 | +0.097 | grows | 0.594 | 0.603 | 0.256 | 0.340 | 11 | 3.7e-15 | 381 |
| MITOSA | fs10/k3 | neutral_plus | 46 | 0.505 | +0.015 | -0.098 | reverses | 0.592 | 0.596 | 0.268 | 0.458 | 12 | 4.3e-15 | 381 |
| MITOSA | fs10/k3 | neutral_plus | 47 | 0.497 | -0.006 | -0.005 | saturated | 0.509 | 0.510 | 0.001 | 1.000 | 1 | 1.7e-14 | 381 |
| MITOSA | fs10/k3 | neutral_plus | 48 | 0.499 | -0.010 | -0.003 | saturated | 0.505 | 0.519 | 0.724 | 0.822 | 11 | 7.3e-15 | 295 |
| MITOSA | fs10/k3 | neutral_plus | 49 | 0.499 | -0.000 | +0.011 | saturated | 0.511 | 0.511 | 0.000 | 1.000 | 1 | 1.7e-14 | 295 |
| MITOSA | fs10/k3 | neutral_plus | 50 | 0.500 | +0.007 | +0.001 | saturated | 0.501 | 0.508 | 0.097 | 0.889 | 3 | 5.8e-15 | 295 |
| MITOSA | fs10/k3 | neutral_minus | 1 | 0.501 | +0.007 | -0.008 | saturated | 0.507 | 0.507 | 1.000 | 1.000 | 2 | 1.1e-14 | 18096 |
| MITOSA | fs10/k3 | neutral_minus | 2 | 0.495 | -0.018 | -0.036 | saturated | 0.541 | 0.618 | 0.001 | 1.000 | 1 | 1.3e-14 | 18050 |
| MITOSA | fs10/k3 | neutral_minus | 3 | 0.499 | +0.035 | +0.016 | saturated | 0.515 | 0.534 | 1.000 | 1.000 | 1 | 1.1e-14 | 19590 |
| MITOSA | fs10/k3 | neutral_minus | 4 | 0.498 | -0.028 | -0.112 | grows | 0.614 | 0.614 | 0.786 | 1.000 | 1 | 1.3e-14 | 19382 |
| MITOSA | fs10/k3 | neutral_minus | 5 | 0.502 | -0.066 | -0.066 | saturated | 0.564 | 0.577 | 0.385 | 1.000 | 1 | 1.4e-14 | 19525 |
| MITOSA | fs10/k3 | neutral_minus | 6 | 0.493 | -0.007 | +0.001 | saturated | 0.494 | 0.495 | 1.000 | 1.000 | 1 | 8.9e-15 | 19429 |
| MITOSA | fs10/k3 | neutral_minus | 7 | 0.499 | +0.006 | -0.002 | saturated | 0.502 | 0.503 | 1.000 | 1.000 | 1 | 5.6e-15 | 19451 |
| MITOSA | fs10/k3 | neutral_minus | 8 | 0.499 | -0.004 | -0.003 | saturated | 0.503 | 0.506 | 1.000 | 1.000 | 12 | 6.2e-15 | 379 |
| MITOSA | fs10/k3 | neutral_minus | 9 | 0.502 | +0.001 | +0.001 | saturated | 0.503 | 0.504 | 1.000 | 1.000 | 8 | 6.1e-15 | 379 |
| MITOSA | fs10/k3 | neutral_minus | 10 | 0.506 | +0.001 | +0.001 | saturated | 0.507 | 0.508 | 1.000 | 1.000 | 11 | 8.8e-15 | 379 |
| MITOSA | fs10/k3 | neutral_minus | 11 | 0.506 | +0.002 | +0.039 | saturated | 0.545 | 0.545 | 0.001 | 1.000 | 1 | 1.2e-14 | 379 |
| MITOSA | fs10/k3 | neutral_minus | 12 | 0.501 | +0.008 | -0.005 | saturated | 0.503 | 0.507 | 1.000 | 1.000 | 1 | 1.6e-14 | 379 |
| MITOSA | fs10/k3 | neutral_minus | 13 | 0.504 | +0.009 | +0.014 | saturated | 0.519 | 0.520 | 1.000 | 1.000 | 1 | 1.6e-14 | 379 |
| MITOSA | fs10/k3 | neutral_minus | 14 | 0.500 | -0.001 | +0.023 | saturated | 0.523 | 0.523 | 1.000 | 1.000 | 1 | 1.7e-14 | 379 |
| MITOSA | fs10/k3 | neutral_minus | 15 | 0.503 | +0.004 | +0.059 | grows | 0.561 | 0.561 | 1.000 | 1.000 | 1 | 2.0e-14 | 379 |
| MITOSA | fs10/k3 | neutral_minus | 16 | 0.499 | +0.010 | +0.018 | saturated | 0.517 | 0.517 | 1.000 | 1.000 | 1 | 1.4e-14 | 379 |
| MITOSA | fs10/k3 | neutral_minus | 17 | 0.504 | +0.005 | +0.011 | saturated | 0.515 | 0.516 | 1.000 | 1.000 | 1 | 1.1e-14 | 379 |
| MITOSA | fs10/k3 | neutral_minus | 18 | 0.493 | -0.002 | -0.002 | saturated | 0.509 | 0.510 | 1.000 | 1.000 | 9 | 5.5e-15 | 375 |
| MITOSA | fs10/k3 | neutral_minus | 19 | 0.498 | -0.014 | -0.009 | saturated | 0.511 | 0.546 | 0.023 | 1.000 | 1 | 1.1e-14 | 375 |
| MITOSA | fs10/k3 | neutral_minus | 20 | 0.499 | +0.002 | -0.001 | saturated | 0.503 | 0.504 | 1.000 | 1.000 | 1 | 8.5e-15 | 375 |
| MITOSA | fs10/k3 | neutral_minus | 21 | 0.495 | -0.002 | +0.105 | reverses | 0.600 | 0.600 | 0.302 | 1.000 | 1 | 9.8e-15 | 375 |
| MITOSA | fs10/k3 | neutral_minus | 22 | 0.501 | -0.025 | -0.029 | saturated | 0.528 | 0.528 | 0.322 | 1.000 | 1 | 1.8e-14 | 375 |
| MITOSA | fs10/k3 | neutral_minus | 23 | 0.504 | +0.008 | +0.004 | saturated | 0.508 | 0.522 | 0.001 | 0.985 | 1 | 1.6e-14 | 375 |
| MITOSA | fs10/k3 | neutral_minus | 24 | 0.505 | +0.007 | -0.033 | saturated | 0.528 | 0.544 | 0.005 | 1.000 | 1 | 1.6e-14 | 375 |
| MITOSA | fs10/k3 | neutral_minus | 25 | 0.500 | +0.010 | +0.010 | saturated | 0.510 | 0.510 | 1.000 | 1.000 | 16 | 6.2e-15 | 375 |
| MITOSA | fs10/k3 | neutral_minus | 26 | 0.499 | -0.035 | -0.015 | saturated | 0.515 | 0.544 | 0.003 | 1.000 | 1 | 1.3e-14 | 375 |
| MITOSA | fs10/k3 | neutral_minus | 27 | 0.491 | +0.001 | +0.032 | saturated | 0.523 | 0.538 | 0.004 | 1.000 | 1 | 1.6e-14 | 375 |
| MITOSA | fs10/k3 | neutral_minus | 28 | 0.499 | -0.004 | -0.031 | saturated | 0.533 | 0.548 | 0.002 | 1.000 | 1 | 2.0e-14 | 384 |
| MITOSA | fs10/k3 | neutral_minus | 29 | 0.508 | -0.005 | -0.005 | saturated | 0.496 | 0.497 | 1.000 | 1.000 | 23 | 5.2e-15 | 384 |
| MITOSA | fs10/k3 | neutral_minus | 30 | 0.498 | -0.016 | -0.037 | saturated | 0.540 | 0.540 | 1.000 | 1.000 | 1 | 1.8e-14 | 384 |
| MITOSA | fs10/k3 | neutral_minus | 31 | 0.499 | -0.006 | +0.055 | reverses | 0.554 | 0.566 | 0.671 | 1.000 | 1 | 1.8e-14 | 384 |
| MITOSA | fs10/k3 | neutral_minus | 32 | 0.504 | -0.011 | -0.004 | saturated | 0.500 | 0.514 | 1.000 | 1.000 | 1 | 1.9e-14 | 384 |
| MITOSA | fs10/k3 | neutral_minus | 33 | 0.495 | +0.014 | +0.048 | saturated | 0.542 | 0.548 | 0.327 | 1.000 | 2 | 1.1e-14 | 384 |
| MITOSA | fs10/k3 | neutral_minus | 34 | 0.501 | +0.010 | +0.012 | saturated | 0.514 | 0.514 | 1.000 | 1.000 | 1 | 1.4e-14 | 384 |
| MITOSA | fs10/k3 | neutral_minus | 35 | 0.497 | +0.020 | +0.028 | saturated | 0.525 | 0.567 | 0.141 | 1.000 | 1 | 1.9e-14 | 384 |
| MITOSA | fs10/k3 | neutral_minus | 36 | 0.500 | +0.004 | -0.033 | saturated | 0.533 | 0.541 | 1.000 | 1.000 | 2 | 1.1e-14 | 384 |
| MITOSA | fs10/k3 | neutral_minus | 37 | 0.502 | -0.019 | -0.015 | saturated | 0.513 | 0.518 | 1.000 | 1.000 | 1 | 8.9e-15 | 384 |
| MITOSA | fs10/k3 | neutral_minus | 38 | 0.507 | +0.008 | -0.008 | saturated | 0.501 | 0.518 | 0.003 | 1.000 | 1 | 1.9e-14 | 381 |
| MITOSA | fs10/k3 | neutral_minus | 39 | 0.504 | -0.018 | -0.012 | saturated | 0.508 | 0.516 | 0.559 | 1.000 | 1 | 1.4e-14 | 381 |
| MITOSA | fs10/k3 | neutral_minus | 40 | 0.497 | +0.023 | +0.035 | saturated | 0.532 | 0.532 | 1.000 | 1.000 | 1 | 9.0e-15 | 381 |
| MITOSA | fs10/k3 | neutral_minus | 41 | 0.500 | +0.008 | -0.012 | saturated | 0.512 | 0.547 | 0.001 | 1.000 | 1 | 1.3e-14 | 381 |
| MITOSA | fs10/k3 | neutral_minus | 42 | 0.502 | +0.007 | +0.006 | saturated | 0.508 | 0.518 | 1.000 | 1.000 | 1 | 1.5e-14 | 381 |
| MITOSA | fs10/k3 | neutral_minus | 43 | 0.500 | -0.006 | -0.006 | saturated | 0.507 | 0.510 | 1.000 | 1.000 | 1 | 1.4e-14 | 381 |
| MITOSA | fs10/k3 | neutral_minus | 44 | 0.496 | -0.053 | -0.132 | grows | 0.636 | 0.636 | 0.547 | 1.000 | 1 | 1.7e-14 | 381 |
| MITOSA | fs10/k3 | neutral_minus | 45 | 0.498 | -0.007 | -0.014 | saturated | 0.517 | 0.523 | 1.000 | 1.000 | 1 | 1.6e-14 | 381 |
| MITOSA | fs10/k3 | neutral_minus | 46 | 0.505 | +0.027 | -0.028 | reverses | 0.522 | 0.531 | 0.008 | 1.000 | 1 | 1.1e-14 | 381 |
| MITOSA | fs10/k3 | neutral_minus | 47 | 0.497 | -0.025 | -0.088 | grows | 0.592 | 0.594 | 0.999 | 1.000 | 1 | 1.7e-14 | 381 |
| MITOSA | fs10/k3 | neutral_minus | 48 | 0.499 | +0.022 | +0.043 | saturated | 0.541 | 0.553 | 1.000 | 1.000 | 1 | 1.9e-14 | 295 |
| MITOSA | fs10/k3 | neutral_minus | 49 | 0.499 | +0.020 | -0.016 | saturated | 0.517 | 0.544 | 0.008 | 1.000 | 1 | 1.1e-14 | 295 |
| MITOSA | fs10/k3 | neutral_minus | 50 | 0.500 | +0.015 | +0.009 | saturated | 0.509 | 0.519 | 1.000 | 1.000 | 1 | 1.2e-14 | 295 |
| VAGRANT | fs0/k3 | treat | 1 | 0.501 | +0.053 | +0.017 | saturated | 0.519 | 0.754 | 0.000 | 0.000 | 2 | 2.0e-14 | 15455 |
| VAGRANT | fs0/k3 | treat | 2 | 0.495 | +0.072 | -0.495 | reverses | 1.000 | 1.000 | 0.000 | 0.000 | 1 | 6.1e-15 | 15330 |
| VAGRANT | fs0/k3 | treat | 3 | 0.499 | +0.174 | -0.243 | reverses | 0.743 | 0.790 | 0.000 | 0.000 | 5 | 1.1e-14 | 16553 |
| VAGRANT | fs0/k3 | treat | 4 | 0.498 | +0.047 | -0.034 | reverses | 0.536 | 0.537 | 0.000 | 0.000 | 2 | 8.6e-15 | 16731 |
| VAGRANT | fs0/k3 | treat | 5 | 0.502 | +0.006 | -0.075 | reverses | 0.573 | 0.596 | 0.000 | 0.000 | 3 | 6.1e-15 | 16716 |
| VAGRANT | fs0/k3 | treat | 6 | 0.493 | +0.023 | +0.036 | saturated | 0.529 | 0.694 | 0.001 | 0.000 | 9 | 1.5e-14 | 16553 |
| VAGRANT | fs0/k3 | treat | 7 | 0.499 | +0.067 | -0.140 | reverses | 0.641 | 0.642 | 0.000 | 0.000 | 2 | 8.8e-15 | 16733 |
| VAGRANT | fs0/k3 | treat | 8 | 0.499 | +0.021 | -0.184 | reverses | 0.685 | 0.686 | 0.000 | 0.000 | 2 | 6.8e-15 | 282 |
| VAGRANT | fs0/k3 | treat | 9 | 0.502 | +0.024 | -0.223 | reverses | 0.720 | 0.743 | 0.000 | 0.000 | 10 | 5.3e-15 | 282 |
| VAGRANT | fs0/k3 | treat | 10 | 0.506 | -0.009 | -0.058 | saturated | 0.552 | 0.553 | 0.000 | 0.000 | 2 | 7.8e-15 | 282 |
| VAGRANT | fs0/k3 | treat | 11 | 0.506 | +0.078 | +0.494 | grows | 1.000 | 1.000 | 0.000 | 0.000 | 9 | 8.3e-15 | 282 |
| VAGRANT | fs0/k3 | treat | 12 | 0.501 | -0.006 | -0.069 | grows | 0.568 | 0.574 | 0.000 | 0.000 | 2 | 5.8e-15 | 282 |
| VAGRANT | fs0/k3 | treat | 13 | 0.504 | +0.012 | -0.168 | reverses | 0.664 | 0.667 | 0.000 | 0.000 | 4 | 6.7e-15 | 282 |
| VAGRANT | fs0/k3 | treat | 14 | 0.500 | +0.050 | -0.171 | reverses | 0.671 | 0.735 | 0.000 | 0.000 | 5 | 5.0e-15 | 282 |
| VAGRANT | fs0/k3 | treat | 15 | 0.503 | -0.022 | -0.041 | saturated | 0.538 | 0.541 | 0.000 | 0.000 | 2 | 7.1e-15 | 282 |
| VAGRANT | fs0/k3 | treat | 16 | 0.499 | +0.008 | -0.008 | saturated | 0.509 | 0.523 | 0.000 | 0.000 | 2 | 2.1e-14 | 282 |
| VAGRANT | fs0/k3 | treat | 17 | 0.504 | +0.087 | +0.217 | grows | 0.721 | 0.836 | 0.000 | 0.000 | 3 | 6.3e-15 | 282 |
| VAGRANT | fs0/k3 | treat | 18 | 0.493 | +0.021 | +0.020 | saturated | 0.512 | 0.530 | 0.000 | 0.000 | 3 | 6.7e-15 | 283 |
| VAGRANT | fs0/k3 | treat | 19 | 0.498 | +0.063 | -0.149 | reverses | 0.651 | 0.671 | 0.000 | 0.000 | 9 | 1.3e-15 | 283 |
| VAGRANT | fs0/k3 | treat | 20 | 0.499 | +0.174 | +0.501 | grows | 1.000 | 1.000 | 0.000 | 0.000 | 10 | 7.2e-15 | 283 |
| VAGRANT | fs0/k3 | treat | 21 | 0.495 | +0.044 | +0.505 | grows | 1.000 | 1.000 | 0.000 | 0.000 | 1 | 1.8e-15 | 283 |
| VAGRANT | fs0/k3 | treat | 22 | 0.501 | +0.119 | +0.499 | grows | 1.000 | 1.000 | 0.000 | 0.000 | 19 | 4.3e-15 | 283 |
| VAGRANT | fs0/k3 | treat | 23 | 0.504 | -0.014 | -0.501 | grows | 0.997 | 1.000 | 0.000 | 0.000 | 3 | 3.7e-15 | 283 |
| VAGRANT | fs0/k3 | treat | 24 | 0.505 | +0.017 | -0.130 | reverses | 0.625 | 0.645 | 0.000 | 0.000 | 5 | 4.9e-15 | 283 |
| VAGRANT | fs0/k3 | treat | 25 | 0.500 | +0.054 | -0.063 | reverses | 0.562 | 0.599 | 0.000 | 0.000 | 2 | 1.0e-14 | 283 |
| VAGRANT | fs0/k3 | treat | 26 | 0.499 | -0.018 | -0.064 | saturated | 0.564 | 0.567 | 0.000 | 0.000 | 2 | 6.3e-15 | 283 |
| VAGRANT | fs0/k3 | treat | 27 | 0.491 | +0.051 | -0.174 | reverses | 0.683 | 0.690 | 0.000 | 0.000 | 2 | 2.1e-15 | 283 |
| VAGRANT | fs0/k3 | treat | 28 | 0.499 | +0.082 | +0.501 | grows | 1.000 | 1.000 | 0.000 | 0.000 | 14 | 1.1e-14 | 276 |
| VAGRANT | fs0/k3 | treat | 29 | 0.508 | +0.056 | -0.268 | reverses | 0.759 | 0.763 | 0.000 | 0.000 | 4 | 5.1e-15 | 276 |
| VAGRANT | fs0/k3 | treat | 30 | 0.498 | +0.060 | -0.051 | reverses | 0.553 | 0.555 | 0.000 | 0.000 | 2 | 3.1e-15 | 276 |
| VAGRANT | fs0/k3 | treat | 31 | 0.499 | +0.069 | -0.133 | reverses | 0.634 | 0.635 | 0.000 | 0.000 | 2 | 4.8e-15 | 276 |
| VAGRANT | fs0/k3 | treat | 32 | 0.504 | +0.007 | -0.136 | reverses | 0.631 | 0.671 | 0.000 | 0.000 | 5 | 4.5e-15 | 276 |
| VAGRANT | fs0/k3 | treat | 33 | 0.495 | +0.002 | -0.126 | reverses | 0.631 | 0.635 | 0.000 | 0.000 | 2 | 6.9e-15 | 276 |
| VAGRANT | fs0/k3 | treat | 34 | 0.501 | +0.106 | -0.175 | reverses | 0.674 | 0.731 | 0.000 | 0.000 | 10 | 5.4e-15 | 276 |
| VAGRANT | fs0/k3 | treat | 35 | 0.497 | +0.125 | +0.502 | grows | 0.999 | 1.000 | 0.000 | 0.000 | 10 | 5.5e-15 | 276 |
| VAGRANT | fs0/k3 | treat | 36 | 0.500 | +0.010 | +0.015 | saturated | 0.515 | 0.689 | 0.000 | 0.000 | 2 | 1.1e-14 | 276 |
| VAGRANT | fs0/k3 | treat | 37 | 0.502 | -0.009 | -0.108 | grows | 0.605 | 0.614 | 0.000 | 0.001 | 3 | 5.2e-15 | 276 |
| VAGRANT | fs0/k3 | treat | 38 | 0.507 | +0.129 | +0.493 | grows | 1.000 | 1.000 | 0.000 | 0.000 | 11 | 1.5e-14 | 282 |
| VAGRANT | fs0/k3 | treat | 39 | 0.504 | -0.032 | -0.189 | grows | 0.684 | 0.689 | 0.000 | 0.000 | 4 | 5.0e-15 | 282 |
| VAGRANT | fs0/k3 | treat | 40 | 0.497 | -0.035 | -0.171 | grows | 0.674 | 0.687 | 0.000 | 0.000 | 4 | 4.7e-15 | 282 |
| VAGRANT | fs0/k3 | treat | 41 | 0.500 | +0.058 | +0.500 | grows | 1.000 | 1.000 | 0.000 | 0.000 | 12 | 5.2e-15 | 282 |
| VAGRANT | fs0/k3 | treat | 42 | 0.502 | +0.004 | +0.174 | grows | 0.676 | 0.792 | 0.000 | 0.000 | 3 | 8.6e-15 | 282 |
| VAGRANT | fs0/k3 | treat | 43 | 0.500 | +0.022 | -0.216 | reverses | 0.716 | 0.762 | 0.000 | 0.000 | 5 | 3.5e-15 | 282 |
| VAGRANT | fs0/k3 | treat | 44 | 0.496 | +0.294 | +0.504 | grows | 1.000 | 1.000 | 0.000 | 0.000 | 9 | 1.0e-14 | 282 |
| VAGRANT | fs0/k3 | treat | 45 | 0.498 | +0.123 | +0.502 | grows | 1.000 | 1.000 | 0.000 | 0.000 | 26 | 5.5e-15 | 282 |
| VAGRANT | fs0/k3 | treat | 46 | 0.505 | +0.037 | +0.495 | grows | 1.000 | 1.000 | 0.000 | 0.000 | 10 | 5.3e-15 | 282 |
| VAGRANT | fs0/k3 | treat | 47 | 0.497 | -0.025 | -0.033 | saturated | 0.536 | 0.556 | 0.000 | 0.000 | 2 | 4.3e-15 | 282 |
| VAGRANT | fs0/k3 | treat | 48 | 0.499 | +0.088 | +0.501 | grows | 1.000 | 1.000 | 0.000 | 0.000 | 16 | 3.9e-15 | 221 |
| VAGRANT | fs0/k3 | treat | 49 | 0.499 | +0.001 | -0.042 | saturated | 0.543 | 0.543 | 0.000 | 0.000 | 2 | 8.8e-15 | 221 |
| VAGRANT | fs0/k3 | treat | 50 | 0.500 | -0.001 | -0.079 | grows | 0.580 | 0.586 | 0.000 | 0.000 | 2 | 6.0e-15 | 221 |
| VAGRANT | fs0/k3 | neutral_plus | 1 | 0.501 | -0.014 | -0.099 | grows | 0.597 | 0.603 | 0.746 | 0.790 | 10 | 9.7e-15 | 15332 |
| VAGRANT | fs0/k3 | neutral_plus | 2 | 0.495 | +0.042 | +0.332 | grows | 0.827 | 0.845 | 0.498 | 0.212 | 8 | 4.1e-15 | 15312 |
| VAGRANT | fs0/k3 | neutral_plus | 3 | 0.499 | +0.029 | +0.280 | grows | 0.779 | 0.792 | 0.720 | 0.536 | 8 | 1.1e-15 | 16979 |
| VAGRANT | fs0/k3 | neutral_plus | 4 | 0.498 | +0.004 | +0.002 | saturated | 0.500 | 0.504 | 0.587 | 0.000 | 2 | 4.9e-15 | 16658 |
| VAGRANT | fs0/k3 | neutral_plus | 5 | 0.502 | -0.002 | -0.006 | saturated | 0.504 | 0.506 | 0.584 | 0.128 | 10 | 6.1e-15 | 16333 |
| VAGRANT | fs0/k3 | neutral_plus | 6 | 0.493 | +0.009 | +0.056 | saturated | 0.549 | 0.550 | 0.888 | 0.820 | 13 | 7.6e-15 | 16713 |
| VAGRANT | fs0/k3 | neutral_plus | 7 | 0.499 | +0.011 | +0.009 | saturated | 0.508 | 0.516 | 0.888 | 1.000 | 7 | 9.9e-15 | 16718 |
| VAGRANT | fs0/k3 | neutral_plus | 8 | 0.499 | +0.003 | +0.010 | saturated | 0.509 | 0.509 | 0.974 | 1.000 | 8 | 1.9e-15 | 282 |
| VAGRANT | fs0/k3 | neutral_plus | 9 | 0.502 | -0.004 | -0.008 | saturated | 0.505 | 0.506 | 0.997 | 1.000 | 2 | 1.5e-15 | 282 |
| VAGRANT | fs0/k3 | neutral_plus | 10 | 0.506 | +0.014 | -0.006 | saturated | 0.500 | 0.500 | 0.252 | 0.000 | 2 | 9.6e-15 | 282 |
| VAGRANT | fs0/k3 | neutral_plus | 11 | 0.506 | -0.001 | -0.000 | saturated | 0.494 | 0.499 | 0.859 | 1.000 | 7 | 1.3e-14 | 282 |
| VAGRANT | fs0/k3 | neutral_plus | 12 | 0.501 | -0.005 | -0.000 | saturated | 0.499 | 0.505 | 0.478 | 0.002 | 2 | 6.9e-15 | 282 |
| VAGRANT | fs0/k3 | neutral_plus | 13 | 0.504 | -0.001 | -0.006 | saturated | 0.501 | 0.521 | 0.581 | 0.147 | 6 | 2.0e-15 | 282 |
| VAGRANT | fs0/k3 | neutral_plus | 14 | 0.500 | -0.011 | -0.090 | grows | 0.590 | 0.594 | 0.810 | 0.794 | 10 | 5.7e-15 | 282 |
| VAGRANT | fs0/k3 | neutral_plus | 15 | 0.503 | -0.014 | -0.002 | saturated | 0.500 | 0.512 | 0.311 | 0.000 | 2 | 9.4e-15 | 282 |
| VAGRANT | fs0/k3 | neutral_plus | 16 | 0.499 | -0.013 | +0.001 | saturated | 0.500 | 0.500 | 0.235 | 0.000 | 2 | 1.2e-14 | 282 |
| VAGRANT | fs0/k3 | neutral_plus | 17 | 0.504 | +0.018 | -0.000 | saturated | 0.496 | 0.498 | 0.851 | 1.000 | 3 | 5.4e-15 | 282 |
| VAGRANT | fs0/k3 | neutral_plus | 18 | 0.493 | -0.005 | -0.028 | saturated | 0.535 | 0.558 | 0.705 | 0.044 | 9 | 3.3e-15 | 283 |
| VAGRANT | fs0/k3 | neutral_plus | 19 | 0.498 | -0.002 | -0.005 | saturated | 0.507 | 0.507 | 0.866 | 1.000 | 8 | 1.3e-15 | 283 |
| VAGRANT | fs0/k3 | neutral_plus | 20 | 0.499 | +0.003 | +0.013 | saturated | 0.512 | 0.512 | 0.692 | 1.000 | 9 | 5.4e-15 | 283 |
| VAGRANT | fs0/k3 | neutral_plus | 21 | 0.495 | +0.003 | +0.006 | saturated | 0.501 | 0.501 | 0.986 | 1.000 | 5 | 8.0e-16 | 283 |
| VAGRANT | fs0/k3 | neutral_plus | 22 | 0.501 | +0.002 | -0.000 | saturated | 0.499 | 0.499 | 0.814 | 1.000 | 5 | 2.1e-15 | 283 |
| VAGRANT | fs0/k3 | neutral_plus | 23 | 0.504 | +0.012 | +0.010 | saturated | 0.514 | 0.517 | 0.965 | 1.000 | 7 | 2.0e-15 | 283 |
| VAGRANT | fs0/k3 | neutral_plus | 24 | 0.505 | +0.012 | -0.002 | saturated | 0.497 | 0.498 | 0.535 | 0.004 | 2 | 4.2e-15 | 283 |
| VAGRANT | fs0/k3 | neutral_plus | 25 | 0.500 | -0.004 | +0.007 | saturated | 0.507 | 0.508 | 0.979 | 1.000 | 8 | 3.9e-15 | 283 |
| VAGRANT | fs0/k3 | neutral_plus | 26 | 0.499 | +0.019 | +0.000 | saturated | 0.500 | 0.519 | 0.314 | 0.000 | 2 | 7.5e-15 | 283 |
| VAGRANT | fs0/k3 | neutral_plus | 27 | 0.491 | -0.001 | -0.010 | saturated | 0.519 | 0.519 | 0.992 | 1.000 | 8 | 4.5e-15 | 283 |
| VAGRANT | fs0/k3 | neutral_plus | 28 | 0.499 | +0.001 | +0.002 | saturated | 0.501 | 0.503 | 0.856 | 1.000 | 11 | 3.0e-15 | 276 |
| VAGRANT | fs0/k3 | neutral_plus | 29 | 0.508 | +0.025 | +0.088 | grows | 0.597 | 0.599 | 0.813 | 0.791 | 19 | 3.1e-15 | 276 |
| VAGRANT | fs0/k3 | neutral_plus | 30 | 0.498 | -0.013 | -0.001 | saturated | 0.503 | 0.518 | 0.611 | 0.000 | 2 | 9.4e-15 | 276 |
| VAGRANT | fs0/k3 | neutral_plus | 31 | 0.499 | -0.009 | -0.011 | saturated | 0.513 | 0.514 | 0.831 | 1.000 | 7 | 4.2e-15 | 276 |
| VAGRANT | fs0/k3 | neutral_plus | 32 | 0.504 | +0.005 | +0.006 | saturated | 0.510 | 0.534 | 0.673 | 0.000 | 2 | 7.0e-15 | 276 |
| VAGRANT | fs0/k3 | neutral_plus | 33 | 0.495 | +0.006 | +0.007 | saturated | 0.502 | 0.504 | 0.612 | 0.017 | 7 | 5.2e-15 | 276 |
| VAGRANT | fs0/k3 | neutral_plus | 34 | 0.501 | -0.010 | -0.007 | saturated | 0.506 | 0.513 | 0.949 | 1.000 | 2 | 3.7e-15 | 276 |
| VAGRANT | fs0/k3 | neutral_plus | 35 | 0.497 | -0.000 | -0.001 | saturated | 0.504 | 0.504 | 0.943 | 1.000 | 6 | 2.7e-15 | 276 |
| VAGRANT | fs0/k3 | neutral_plus | 36 | 0.500 | -0.001 | -0.007 | saturated | 0.507 | 0.507 | 0.973 | 1.000 | 5 | 4.9e-15 | 276 |
| VAGRANT | fs0/k3 | neutral_plus | 37 | 0.502 | +0.007 | +0.009 | saturated | 0.511 | 0.516 | 0.643 | 0.150 | 4 | 6.1e-15 | 276 |
| VAGRANT | fs0/k3 | neutral_plus | 38 | 0.507 | +0.007 | +0.014 | saturated | 0.521 | 0.525 | 0.751 | 1.000 | 10 | 4.3e-15 | 282 |
| VAGRANT | fs0/k3 | neutral_plus | 39 | 0.504 | -0.000 | -0.003 | saturated | 0.499 | 0.501 | 0.440 | 0.005 | 5 | 6.4e-15 | 282 |
| VAGRANT | fs0/k3 | neutral_plus | 40 | 0.497 | +0.005 | +0.004 | saturated | 0.501 | 0.505 | 0.511 | 0.061 | 9 | 7.1e-15 | 282 |
| VAGRANT | fs0/k3 | neutral_plus | 41 | 0.500 | -0.005 | -0.011 | saturated | 0.511 | 0.511 | 0.883 | 1.000 | 9 | 2.0e-15 | 282 |
| VAGRANT | fs0/k3 | neutral_plus | 42 | 0.502 | -0.003 | -0.012 | saturated | 0.510 | 0.511 | 0.989 | 1.000 | 9 | 5.4e-15 | 282 |
| VAGRANT | fs0/k3 | neutral_plus | 43 | 0.500 | +0.003 | +0.004 | saturated | 0.504 | 0.504 | 0.990 | 1.000 | 3 | 8.0e-15 | 282 |
| VAGRANT | fs0/k3 | neutral_plus | 44 | 0.496 | -0.001 | -0.013 | saturated | 0.517 | 0.518 | 0.739 | 1.000 | 8 | 4.8e-15 | 282 |
| VAGRANT | fs0/k3 | neutral_plus | 45 | 0.498 | +0.002 | -0.000 | saturated | 0.503 | 0.503 | 0.894 | 1.000 | 5 | 1.6e-15 | 282 |
| VAGRANT | fs0/k3 | neutral_plus | 46 | 0.505 | +0.001 | -0.001 | saturated | 0.495 | 0.496 | 0.828 | 1.000 | 7 | 4.8e-15 | 282 |
| VAGRANT | fs0/k3 | neutral_plus | 47 | 0.497 | +0.000 | +0.004 | saturated | 0.500 | 0.500 | 0.289 | 0.000 | 2 | 9.0e-15 | 282 |
| VAGRANT | fs0/k3 | neutral_plus | 48 | 0.499 | -0.008 | -0.002 | saturated | 0.504 | 0.514 | 0.788 | 1.000 | 10 | 6.5e-15 | 221 |
| VAGRANT | fs0/k3 | neutral_plus | 49 | 0.499 | -0.000 | +0.001 | saturated | 0.500 | 0.502 | 0.163 | 0.000 | 2 | 1.2e-14 | 221 |
| VAGRANT | fs0/k3 | neutral_plus | 50 | 0.500 | +0.004 | +0.002 | saturated | 0.502 | 0.511 | 0.473 | 0.002 | 2 | 5.8e-15 | 221 |
| VAGRANT | fs0/k3 | neutral_minus | 1 | 0.501 | +0.005 | -0.016 | saturated | 0.515 | 0.515 | 1.000 | 1.000 | 1 | 3.7e-15 | 15414 |
| VAGRANT | fs0/k3 | neutral_minus | 2 | 0.495 | +0.007 | -0.004 | saturated | 0.509 | 0.509 | 0.331 | 0.000 | 2 | 1.8e-14 | 16688 |
| VAGRANT | fs0/k3 | neutral_minus | 3 | 0.499 | +0.010 | +0.014 | saturated | 0.514 | 0.514 | 1.000 | 1.000 | 1 | 6.4e-15 | 16738 |
| VAGRANT | fs0/k3 | neutral_minus | 4 | 0.498 | +0.002 | +0.006 | saturated | 0.504 | 0.510 | 0.978 | 1.000 | 4 | 1.5e-14 | 16595 |
| VAGRANT | fs0/k3 | neutral_minus | 5 | 0.502 | -0.001 | -0.001 | saturated | 0.499 | 0.499 | 1.000 | 1.000 | 4 | 6.7e-15 | 16656 |
| VAGRANT | fs0/k3 | neutral_minus | 6 | 0.493 | +0.001 | -0.000 | saturated | 0.508 | 0.508 | 1.000 | 1.000 | 1 | 8.3e-15 | 16882 |
| VAGRANT | fs0/k3 | neutral_minus | 7 | 0.499 | -0.001 | +0.004 | saturated | 0.503 | 0.503 | 1.000 | 1.000 | 1 | 1.3e-14 | 16796 |
| VAGRANT | fs0/k3 | neutral_minus | 8 | 0.499 | -0.004 | -0.003 | saturated | 0.503 | 0.507 | 0.448 | 1.000 | 4 | 9.5e-15 | 282 |
| VAGRANT | fs0/k3 | neutral_minus | 9 | 0.502 | -0.005 | -0.010 | saturated | 0.507 | 0.508 | 0.881 | 1.000 | 4 | 2.7e-15 | 282 |
| VAGRANT | fs0/k3 | neutral_minus | 10 | 0.506 | +0.009 | +0.005 | saturated | 0.511 | 0.518 | 0.189 | 1.000 | 3 | 3.7e-15 | 282 |
| VAGRANT | fs0/k3 | neutral_minus | 11 | 0.506 | -0.004 | -0.007 | saturated | 0.501 | 0.502 | 0.529 | 0.521 | 20 | 1.5e-14 | 282 |
| VAGRANT | fs0/k3 | neutral_minus | 12 | 0.501 | -0.002 | +0.007 | saturated | 0.509 | 0.509 | 0.939 | 1.000 | 1 | 9.1e-15 | 282 |
| VAGRANT | fs0/k3 | neutral_minus | 13 | 0.504 | -0.000 | -0.007 | saturated | 0.503 | 0.503 | 0.933 | 1.000 | 4 | 7.9e-15 | 282 |
| VAGRANT | fs0/k3 | neutral_minus | 14 | 0.500 | -0.005 | +0.016 | saturated | 0.516 | 0.517 | 0.965 | 1.000 | 4 | 1.4e-14 | 282 |
| VAGRANT | fs0/k3 | neutral_minus | 15 | 0.503 | -0.007 | -0.015 | saturated | 0.512 | 0.513 | 0.339 | 0.000 | 4 | 1.3e-14 | 282 |
| VAGRANT | fs0/k3 | neutral_minus | 16 | 0.499 | +0.028 | -0.000 | saturated | 0.501 | 0.501 | 0.164 | 0.000 | 2 | 5.3e-15 | 282 |
| VAGRANT | fs0/k3 | neutral_minus | 17 | 0.504 | +0.003 | +0.028 | saturated | 0.532 | 0.532 | 1.000 | 1.000 | 4 | 5.2e-15 | 282 |
| VAGRANT | fs0/k3 | neutral_minus | 18 | 0.493 | +0.005 | -0.018 | saturated | 0.525 | 0.525 | 1.000 | 1.000 | 4 | 6.2e-15 | 283 |
| VAGRANT | fs0/k3 | neutral_minus | 19 | 0.498 | +0.008 | +0.008 | saturated | 0.506 | 0.507 | 0.947 | 1.000 | 20 | 1.7e-15 | 283 |
| VAGRANT | fs0/k3 | neutral_minus | 20 | 0.499 | -0.014 | -0.010 | saturated | 0.511 | 0.520 | 1.000 | 1.000 | 16 | 3.8e-14 | 283 |
| VAGRANT | fs0/k3 | neutral_minus | 21 | 0.495 | +0.002 | +0.002 | saturated | 0.498 | 0.498 | 1.000 | 1.000 | 1 | 4.0e-15 | 283 |
| VAGRANT | fs0/k3 | neutral_minus | 22 | 0.501 | +0.005 | +0.004 | saturated | 0.505 | 0.507 | 0.937 | 1.000 | 15 | 3.2e-15 | 283 |
| VAGRANT | fs0/k3 | neutral_minus | 23 | 0.504 | +0.003 | -0.010 | saturated | 0.506 | 0.506 | 0.730 | 1.000 | 4 | 9.7e-15 | 283 |
| VAGRANT | fs0/k3 | neutral_minus | 24 | 0.505 | +0.001 | -0.006 | saturated | 0.501 | 0.505 | 0.898 | 1.000 | 4 | 4.6e-15 | 283 |
| VAGRANT | fs0/k3 | neutral_minus | 25 | 0.500 | +0.002 | -0.003 | saturated | 0.502 | 0.507 | 0.917 | 1.000 | 4 | 6.4e-15 | 283 |
| VAGRANT | fs0/k3 | neutral_minus | 26 | 0.499 | +0.006 | +0.006 | saturated | 0.505 | 0.516 | 0.566 | 1.000 | 4 | 1.1e-14 | 283 |
| VAGRANT | fs0/k3 | neutral_minus | 27 | 0.491 | -0.001 | +0.005 | saturated | 0.496 | 0.497 | 0.651 | 1.000 | 4 | 8.7e-15 | 283 |
| VAGRANT | fs0/k3 | neutral_minus | 28 | 0.499 | +0.007 | +0.010 | saturated | 0.509 | 0.509 | 0.529 | 0.533 | 15 | 2.3e-14 | 276 |
| VAGRANT | fs0/k3 | neutral_minus | 29 | 0.508 | -0.001 | -0.010 | saturated | 0.501 | 0.502 | 0.744 | 1.000 | 4 | 5.4e-15 | 276 |
| VAGRANT | fs0/k3 | neutral_minus | 30 | 0.498 | +0.010 | -0.012 | saturated | 0.515 | 0.515 | 0.931 | 1.000 | 3 | 3.9e-15 | 276 |
| VAGRANT | fs0/k3 | neutral_minus | 31 | 0.499 | +0.003 | +0.013 | saturated | 0.511 | 0.512 | 0.526 | 0.723 | 4 | 5.4e-15 | 276 |
| VAGRANT | fs0/k3 | neutral_minus | 32 | 0.504 | -0.018 | +0.066 | reverses | 0.570 | 0.570 | 0.946 | 1.000 | 1 | 9.4e-15 | 276 |
| VAGRANT | fs0/k3 | neutral_minus | 33 | 0.495 | +0.004 | +0.005 | saturated | 0.500 | 0.503 | 1.000 | 1.000 | 4 | 3.0e-15 | 276 |
| VAGRANT | fs0/k3 | neutral_minus | 34 | 0.501 | -0.022 | -0.024 | saturated | 0.523 | 0.523 | 1.000 | 1.000 | 1 | 2.3e-14 | 276 |
| VAGRANT | fs0/k3 | neutral_minus | 35 | 0.497 | +0.000 | -0.000 | saturated | 0.503 | 0.503 | 1.000 | 1.000 | 4 | 2.9e-15 | 276 |
| VAGRANT | fs0/k3 | neutral_minus | 36 | 0.500 | +0.010 | -0.000 | saturated | 0.500 | 0.500 | 0.934 | 1.000 | 1 | 7.5e-15 | 276 |
| VAGRANT | fs0/k3 | neutral_minus | 37 | 0.502 | -0.016 | -0.016 | saturated | 0.514 | 0.515 | 1.000 | 1.000 | 2 | 1.2e-15 | 276 |
| VAGRANT | fs0/k3 | neutral_minus | 38 | 0.507 | -0.018 | +0.003 | saturated | 0.510 | 0.513 | 0.836 | 0.927 | 33 | 1.1e-14 | 282 |
| VAGRANT | fs0/k3 | neutral_minus | 39 | 0.504 | +0.003 | +0.012 | saturated | 0.517 | 0.517 | 1.000 | 1.000 | 4 | 4.4e-15 | 282 |
| VAGRANT | fs0/k3 | neutral_minus | 40 | 0.497 | +0.000 | +0.007 | saturated | 0.504 | 0.504 | 1.000 | 1.000 | 4 | 1.7e-15 | 282 |
| VAGRANT | fs0/k3 | neutral_minus | 41 | 0.500 | +0.000 | +0.001 | saturated | 0.501 | 0.503 | 0.770 | 1.000 | 16 | 2.2e-15 | 282 |
| VAGRANT | fs0/k3 | neutral_minus | 42 | 0.502 | +0.003 | +0.003 | saturated | 0.505 | 0.508 | 0.901 | 1.000 | 4 | 3.0e-15 | 282 |
| VAGRANT | fs0/k3 | neutral_minus | 43 | 0.500 | +0.001 | +0.010 | saturated | 0.510 | 0.510 | 0.882 | 1.000 | 4 | 7.3e-15 | 282 |
| VAGRANT | fs0/k3 | neutral_minus | 44 | 0.496 | +0.017 | +0.020 | saturated | 0.515 | 0.516 | 0.985 | 1.000 | 31 | 7.4e-15 | 282 |
| VAGRANT | fs0/k3 | neutral_minus | 45 | 0.498 | +0.005 | +0.005 | saturated | 0.502 | 0.504 | 1.000 | 1.000 | 15 | 2.6e-15 | 282 |
| VAGRANT | fs0/k3 | neutral_minus | 46 | 0.505 | -0.001 | -0.001 | saturated | 0.496 | 0.496 | 0.767 | 1.000 | 4 | 3.9e-15 | 282 |
| VAGRANT | fs0/k3 | neutral_minus | 47 | 0.497 | -0.001 | +0.003 | saturated | 0.500 | 0.500 | 0.307 | 1.000 | 3 | 6.9e-15 | 282 |
| VAGRANT | fs0/k3 | neutral_minus | 48 | 0.499 | -0.008 | -0.004 | saturated | 0.506 | 0.511 | 0.793 | 0.795 | 19 | 2.4e-14 | 221 |
| VAGRANT | fs0/k3 | neutral_minus | 49 | 0.499 | +0.005 | -0.002 | saturated | 0.503 | 0.503 | 0.237 | 1.000 | 3 | 7.9e-15 | 221 |
| VAGRANT | fs0/k3 | neutral_minus | 50 | 0.500 | -0.009 | +0.009 | saturated | 0.508 | 0.509 | 0.849 | 1.000 | 4 | 6.1e-15 | 221 |
| VAGRANT | fs10/k3 | treat | 1 | 0.501 | -0.219 | -0.500 | grows | 0.999 | 0.999 | 0.001 | 0.000 | 1 | 2.2e-15 | 18101 |
| VAGRANT | fs10/k3 | treat | 2 | 0.495 | -0.114 | +0.501 | reverses | 0.996 | 0.996 | 0.001 | 0.000 | 1 | 8.4e-15 | 19293 |
| VAGRANT | fs10/k3 | treat | 3 | 0.499 | -0.295 | -0.496 | grows | 0.997 | 0.997 | 0.000 | 0.000 | 1 | 2.5e-15 | 19745 |
| VAGRANT | fs10/k3 | treat | 4 | 0.498 | -0.317 | -0.496 | grows | 0.998 | 0.998 | 0.000 | 0.000 | 1 | 1.6e-15 | 19468 |
| VAGRANT | fs10/k3 | treat | 5 | 0.502 | -0.023 | -0.499 | grows | 0.997 | 0.997 | 0.000 | 0.000 | 1 | 8.0e-15 | 19755 |
| VAGRANT | fs10/k3 | treat | 6 | 0.493 | -0.086 | -0.488 | grows | 0.995 | 0.995 | 0.000 | 0.000 | 1 | 8.3e-15 | 19380 |
| VAGRANT | fs10/k3 | treat | 7 | 0.499 | -0.295 | -0.494 | grows | 0.995 | 0.995 | 0.000 | 0.000 | 1 | 2.9e-15 | 19295 |
| VAGRANT | fs10/k3 | treat | 8 | 0.499 | -0.170 | -0.495 | grows | 0.995 | 0.995 | 0.001 | 0.000 | 1 | 9.0e-15 | 385 |
| VAGRANT | fs10/k3 | treat | 9 | 0.502 | -0.121 | -0.499 | grows | 0.996 | 0.996 | 0.000 | 0.000 | 1 | 4.2e-15 | 385 |
| VAGRANT | fs10/k3 | treat | 10 | 0.506 | -0.229 | -0.501 | grows | 0.995 | 0.995 | 0.000 | 0.000 | 1 | 1.0e-14 | 385 |
| VAGRANT | fs10/k3 | treat | 11 | 0.506 | +0.024 | +0.307 | grows | 0.813 | 0.821 | 0.000 | 0.000 | 34 | 3.3e-15 | 385 |
| VAGRANT | fs10/k3 | treat | 12 | 0.501 | -0.134 | -0.499 | grows | 0.997 | 0.997 | 0.000 | 0.000 | 1 | 9.1e-15 | 385 |
| VAGRANT | fs10/k3 | treat | 13 | 0.504 | -0.110 | -0.502 | grows | 0.997 | 0.997 | 0.000 | 0.000 | 1 | 6.6e-15 | 385 |
| VAGRANT | fs10/k3 | treat | 14 | 0.500 | -0.217 | -0.498 | grows | 0.998 | 0.998 | 0.000 | 0.000 | 1 | 8.8e-15 | 385 |
| VAGRANT | fs10/k3 | treat | 15 | 0.503 | -0.228 | -0.499 | grows | 0.997 | 0.997 | 0.000 | 0.000 | 1 | 9.4e-15 | 385 |
| VAGRANT | fs10/k3 | treat | 16 | 0.499 | -0.270 | -0.491 | grows | 0.992 | 0.992 | 0.000 | 0.000 | 1 | 1.0e-14 | 385 |
| VAGRANT | fs10/k3 | treat | 17 | 0.504 | -0.237 | -0.502 | grows | 0.998 | 0.998 | 0.001 | 0.000 | 1 | 9.3e-15 | 385 |
| VAGRANT | fs10/k3 | treat | 18 | 0.493 | -0.070 | -0.487 | grows | 0.994 | 0.994 | 0.000 | 0.000 | 1 | 3.6e-15 | 378 |
| VAGRANT | fs10/k3 | treat | 19 | 0.498 | -0.265 | -0.493 | grows | 0.995 | 0.995 | 0.001 | 0.000 | 1 | 5.2e-15 | 378 |
| VAGRANT | fs10/k3 | treat | 20 | 0.499 | -0.224 | -0.497 | grows | 0.998 | 0.998 | 0.000 | 0.000 | 2 | 1.3e-14 | 378 |
| VAGRANT | fs10/k3 | treat | 21 | 0.495 | -0.125 | -0.489 | grows | 0.994 | 0.994 | 0.001 | 0.000 | 1 | 5.5e-15 | 378 |
| VAGRANT | fs10/k3 | treat | 22 | 0.501 | -0.306 | -0.499 | grows | 0.998 | 0.998 | 0.000 | 0.000 | 1 | 5.7e-15 | 378 |
| VAGRANT | fs10/k3 | treat | 23 | 0.504 | -0.208 | -0.502 | grows | 0.998 | 0.998 | 0.000 | 0.000 | 1 | 1.0e-14 | 378 |
| VAGRANT | fs10/k3 | treat | 24 | 0.505 | -0.070 | -0.501 | grows | 0.996 | 0.996 | 0.001 | 0.000 | 1 | 2.6e-15 | 378 |
| VAGRANT | fs10/k3 | treat | 25 | 0.500 | -0.135 | -0.496 | grows | 0.995 | 0.995 | 0.000 | 0.000 | 1 | 8.2e-15 | 378 |
| VAGRANT | fs10/k3 | treat | 26 | 0.499 | -0.255 | -0.497 | grows | 0.998 | 0.998 | 0.000 | 0.000 | 1 | 6.3e-15 | 378 |
| VAGRANT | fs10/k3 | treat | 27 | 0.491 | -0.162 | -0.482 | grows | 0.991 | 0.991 | 0.000 | 0.000 | 1 | 7.0e-15 | 378 |
| VAGRANT | fs10/k3 | treat | 28 | 0.499 | -0.225 | -0.484 | grows | 0.985 | 0.985 | 0.000 | 0.000 | 1 | 1.4e-14 | 374 |
| VAGRANT | fs10/k3 | treat | 29 | 0.508 | -0.145 | -0.503 | grows | 0.995 | 0.995 | 0.000 | 0.000 | 1 | 7.9e-15 | 374 |
| VAGRANT | fs10/k3 | treat | 30 | 0.498 | -0.258 | -0.495 | grows | 0.997 | 0.997 | 0.000 | 0.000 | 1 | 9.8e-15 | 374 |
| VAGRANT | fs10/k3 | treat | 31 | 0.499 | -0.259 | -0.495 | grows | 0.997 | 0.997 | 0.000 | 0.000 | 1 | 1.2e-14 | 374 |
| VAGRANT | fs10/k3 | treat | 32 | 0.504 | -0.270 | -0.501 | grows | 0.997 | 0.997 | 0.000 | 0.000 | 1 | 6.8e-15 | 374 |
| VAGRANT | fs10/k3 | treat | 33 | 0.495 | -0.074 | -0.491 | grows | 0.997 | 0.997 | 0.000 | 0.000 | 1 | 4.7e-15 | 374 |
| VAGRANT | fs10/k3 | treat | 34 | 0.501 | -0.291 | -0.498 | grows | 0.996 | 0.996 | 0.000 | 0.000 | 1 | 1.2e-14 | 374 |
| VAGRANT | fs10/k3 | treat | 35 | 0.497 | -0.210 | -0.496 | grows | 0.998 | 0.998 | 0.001 | 0.000 | 1 | 9.1e-15 | 374 |
| VAGRANT | fs10/k3 | treat | 36 | 0.500 | -0.207 | -0.496 | grows | 0.996 | 0.996 | 0.000 | 0.000 | 1 | 8.0e-15 | 374 |
| VAGRANT | fs10/k3 | treat | 37 | 0.502 | -0.016 | -0.500 | grows | 0.997 | 0.997 | 0.003 | 0.000 | 1 | 1.8e-15 | 374 |
| VAGRANT | fs10/k3 | treat | 38 | 0.507 | +0.000 | +0.458 | grows | 0.965 | 0.982 | 0.002 | 0.000 | 10 | 8.4e-15 | 377 |
| VAGRANT | fs10/k3 | treat | 39 | 0.504 | -0.016 | -0.504 | grows | 0.999 | 0.999 | 0.000 | 0.000 | 1 | 3.7e-15 | 377 |
| VAGRANT | fs10/k3 | treat | 40 | 0.497 | -0.045 | -0.495 | grows | 0.998 | 0.998 | 0.000 | 0.000 | 2 | 3.0e-15 | 377 |
| VAGRANT | fs10/k3 | treat | 41 | 0.500 | -0.225 | -0.496 | grows | 0.996 | 0.996 | 0.000 | 0.000 | 1 | 9.0e-15 | 377 |
| VAGRANT | fs10/k3 | treat | 42 | 0.502 | -0.170 | -0.499 | grows | 0.997 | 0.997 | 0.000 | 0.000 | 1 | 5.6e-15 | 377 |
| VAGRANT | fs10/k3 | treat | 43 | 0.500 | -0.170 | -0.495 | grows | 0.995 | 0.995 | 0.000 | 0.000 | 1 | 5.9e-15 | 377 |
| VAGRANT | fs10/k3 | treat | 44 | 0.496 | -0.223 | -0.093 | shrinks | 0.597 | 0.729 | 0.001 | 0.000 | 28 | 4.1e-15 | 377 |
| VAGRANT | fs10/k3 | treat | 45 | 0.498 | -0.268 | -0.494 | grows | 0.997 | 0.997 | 0.000 | 0.000 | 1 | 9.2e-15 | 377 |
| VAGRANT | fs10/k3 | treat | 46 | 0.505 | -0.244 | -0.503 | grows | 0.997 | 0.997 | 0.000 | 0.000 | 1 | 8.1e-15 | 377 |
| VAGRANT | fs10/k3 | treat | 47 | 0.497 | -0.244 | -0.491 | grows | 0.995 | 0.995 | 0.000 | 0.000 | 1 | 8.2e-15 | 377 |
| VAGRANT | fs10/k3 | treat | 48 | 0.499 | -0.213 | -0.491 | grows | 0.993 | 0.993 | 0.000 | 0.000 | 1 | 1.0e-14 | 294 |
| VAGRANT | fs10/k3 | treat | 49 | 0.499 | -0.183 | -0.498 | grows | 0.999 | 0.999 | 0.000 | 0.000 | 1 | 9.9e-15 | 294 |
| VAGRANT | fs10/k3 | treat | 50 | 0.500 | -0.138 | -0.498 | grows | 0.998 | 0.998 | 0.000 | 0.000 | 1 | 7.6e-15 | 294 |
| VAGRANT | fs10/k3 | neutral_plus | 1 | 0.501 | -0.021 | -0.016 | saturated | 0.515 | 0.520 | 1.000 | 1.000 | 50 | 5.8e-15 | 18500 |
| VAGRANT | fs10/k3 | neutral_plus | 2 | 0.495 | +0.010 | +0.010 | saturated | 0.505 | 0.518 | 0.949 | 1.000 | 8 | 9.3e-15 | 19243 |
| VAGRANT | fs10/k3 | neutral_plus | 3 | 0.499 | -0.020 | -0.038 | saturated | 0.539 | 0.546 | 0.879 | 1.000 | 18 | 4.3e-15 | 19607 |
| VAGRANT | fs10/k3 | neutral_plus | 4 | 0.498 | +0.024 | +0.038 | saturated | 0.536 | 0.536 | 1.000 | 1.000 | 12 | 4.3e-15 | 19478 |
| VAGRANT | fs10/k3 | neutral_plus | 5 | 0.502 | -0.006 | -0.006 | saturated | 0.503 | 0.507 | 1.000 | 1.000 | 1 | 8.0e-15 | 19570 |
| VAGRANT | fs10/k3 | neutral_plus | 6 | 0.493 | +0.000 | -0.000 | saturated | 0.508 | 0.509 | 1.000 | 1.000 | 1 | 8.5e-15 | 19474 |
| VAGRANT | fs10/k3 | neutral_plus | 7 | 0.499 | +0.023 | +0.028 | saturated | 0.528 | 0.531 | 1.000 | 1.000 | 21 | 4.3e-15 | 19057 |
| VAGRANT | fs10/k3 | neutral_plus | 8 | 0.499 | +0.001 | +0.002 | saturated | 0.501 | 0.506 | 1.000 | 1.000 | 35 | 3.5e-15 | 385 |
| VAGRANT | fs10/k3 | neutral_plus | 9 | 0.502 | +0.018 | +0.015 | saturated | 0.518 | 0.521 | 1.000 | 1.000 | 8 | 1.0e-15 | 385 |
| VAGRANT | fs10/k3 | neutral_plus | 10 | 0.506 | +0.002 | +0.024 | saturated | 0.530 | 0.531 | 1.000 | 1.000 | 15 | 2.1e-15 | 385 |
| VAGRANT | fs10/k3 | neutral_plus | 11 | 0.506 | -0.012 | -0.023 | saturated | 0.517 | 0.517 | 0.985 | 1.000 | 1 | 5.7e-15 | 385 |
| VAGRANT | fs10/k3 | neutral_plus | 12 | 0.501 | +0.015 | +0.016 | saturated | 0.517 | 0.521 | 1.000 | 1.000 | 47 | 3.7e-15 | 385 |
| VAGRANT | fs10/k3 | neutral_plus | 13 | 0.504 | +0.011 | +0.014 | saturated | 0.518 | 0.518 | 1.000 | 1.000 | 1 | 3.6e-15 | 385 |
| VAGRANT | fs10/k3 | neutral_plus | 14 | 0.500 | -0.007 | -0.009 | saturated | 0.509 | 0.509 | 1.000 | 1.000 | 62 | 3.4e-15 | 385 |
| VAGRANT | fs10/k3 | neutral_plus | 15 | 0.503 | -0.039 | -0.041 | saturated | 0.538 | 0.539 | 1.000 | 1.000 | 14 | 2.3e-15 | 385 |
| VAGRANT | fs10/k3 | neutral_plus | 16 | 0.499 | +0.001 | -0.006 | saturated | 0.508 | 0.521 | 1.000 | 1.000 | 11 | 6.9e-15 | 385 |
| VAGRANT | fs10/k3 | neutral_plus | 17 | 0.504 | -0.003 | +0.002 | saturated | 0.506 | 0.508 | 1.000 | 1.000 | 43 | 4.1e-15 | 385 |
| VAGRANT | fs10/k3 | neutral_plus | 18 | 0.493 | -0.009 | -0.011 | saturated | 0.518 | 0.519 | 1.000 | 1.000 | 1 | 1.1e-15 | 378 |
| VAGRANT | fs10/k3 | neutral_plus | 19 | 0.498 | -0.026 | -0.032 | saturated | 0.534 | 0.534 | 1.000 | 1.000 | 13 | 4.6e-15 | 378 |
| VAGRANT | fs10/k3 | neutral_plus | 20 | 0.499 | -0.006 | -0.021 | saturated | 0.522 | 0.524 | 1.000 | 1.000 | 7 | 3.9e-15 | 378 |
| VAGRANT | fs10/k3 | neutral_plus | 21 | 0.495 | +0.004 | +0.003 | saturated | 0.498 | 0.502 | 1.000 | 1.000 | 1 | 3.1e-15 | 378 |
| VAGRANT | fs10/k3 | neutral_plus | 22 | 0.501 | -0.007 | -0.022 | saturated | 0.521 | 0.528 | 0.861 | 1.000 | 26 | 4.0e-15 | 378 |
| VAGRANT | fs10/k3 | neutral_plus | 23 | 0.504 | +0.001 | +0.003 | saturated | 0.507 | 0.513 | 1.000 | 1.000 | 9 | 4.8e-15 | 378 |
| VAGRANT | fs10/k3 | neutral_plus | 24 | 0.505 | -0.008 | -0.009 | saturated | 0.504 | 0.505 | 1.000 | 1.000 | 1 | 2.2e-15 | 378 |
| VAGRANT | fs10/k3 | neutral_plus | 25 | 0.500 | +0.016 | +0.010 | saturated | 0.510 | 0.518 | 1.000 | 1.000 | 20 | 2.4e-15 | 378 |
| VAGRANT | fs10/k3 | neutral_plus | 26 | 0.499 | +0.009 | +0.004 | saturated | 0.504 | 0.511 | 0.920 | 1.000 | 27 | 5.8e-15 | 378 |
| VAGRANT | fs10/k3 | neutral_plus | 27 | 0.491 | -0.006 | -0.006 | saturated | 0.515 | 0.526 | 1.000 | 1.000 | 44 | 2.6e-15 | 378 |
| VAGRANT | fs10/k3 | neutral_plus | 28 | 0.499 | -0.016 | +0.001 | saturated | 0.500 | 0.524 | 1.000 | 1.000 | 1 | 5.4e-15 | 374 |
| VAGRANT | fs10/k3 | neutral_plus | 29 | 0.508 | -0.012 | -0.013 | saturated | 0.504 | 0.505 | 1.000 | 1.000 | 62 | 3.3e-15 | 374 |
| VAGRANT | fs10/k3 | neutral_plus | 30 | 0.498 | -0.008 | -0.028 | saturated | 0.531 | 0.531 | 1.000 | 1.000 | 45 | 4.7e-15 | 374 |
| VAGRANT | fs10/k3 | neutral_plus | 31 | 0.499 | +0.031 | +0.061 | saturated | 0.560 | 0.560 | 0.988 | 1.000 | 1 | 3.1e-15 | 374 |
| VAGRANT | fs10/k3 | neutral_plus | 32 | 0.504 | -0.017 | -0.017 | saturated | 0.512 | 0.525 | 1.000 | 1.000 | 30 | 6.6e-15 | 374 |
| VAGRANT | fs10/k3 | neutral_plus | 33 | 0.495 | -0.033 | -0.035 | saturated | 0.541 | 0.541 | 1.000 | 1.000 | 2 | 2.4e-15 | 374 |
| VAGRANT | fs10/k3 | neutral_plus | 34 | 0.501 | -0.019 | -0.010 | saturated | 0.509 | 0.519 | 0.993 | 1.000 | 2 | 6.5e-15 | 374 |
| VAGRANT | fs10/k3 | neutral_plus | 35 | 0.497 | +0.001 | +0.007 | saturated | 0.504 | 0.505 | 1.000 | 1.000 | 1 | 2.8e-15 | 374 |
| VAGRANT | fs10/k3 | neutral_plus | 36 | 0.500 | +0.011 | +0.011 | saturated | 0.511 | 0.511 | 1.000 | 1.000 | 41 | 2.8e-15 | 374 |
| VAGRANT | fs10/k3 | neutral_plus | 37 | 0.502 | -0.009 | -0.017 | saturated | 0.515 | 0.515 | 1.000 | 1.000 | 3 | 1.2e-15 | 374 |
| VAGRANT | fs10/k3 | neutral_plus | 38 | 0.507 | -0.004 | +0.010 | saturated | 0.517 | 0.526 | 0.296 | 1.000 | 12 | 5.4e-15 | 377 |
| VAGRANT | fs10/k3 | neutral_plus | 39 | 0.504 | +0.015 | +0.016 | saturated | 0.520 | 0.521 | 1.000 | 1.000 | 36 | 5.9e-15 | 377 |
| VAGRANT | fs10/k3 | neutral_plus | 40 | 0.497 | -0.011 | -0.010 | saturated | 0.513 | 0.521 | 1.000 | 1.000 | 1 | 1.7e-15 | 377 |
| VAGRANT | fs10/k3 | neutral_plus | 41 | 0.500 | +0.002 | +0.008 | saturated | 0.508 | 0.516 | 1.000 | 1.000 | 19 | 2.8e-15 | 377 |
| VAGRANT | fs10/k3 | neutral_plus | 42 | 0.502 | +0.006 | +0.014 | saturated | 0.516 | 0.516 | 1.000 | 1.000 | 2 | 3.8e-15 | 377 |
| VAGRANT | fs10/k3 | neutral_plus | 43 | 0.500 | +0.001 | -0.001 | saturated | 0.501 | 0.503 | 1.000 | 1.000 | 63 | 3.1e-15 | 377 |
| VAGRANT | fs10/k3 | neutral_plus | 44 | 0.496 | -0.011 | -0.018 | saturated | 0.522 | 0.523 | 0.817 | 1.000 | 12 | 5.9e-15 | 377 |
| VAGRANT | fs10/k3 | neutral_plus | 45 | 0.498 | +0.014 | +0.016 | saturated | 0.514 | 0.514 | 1.000 | 1.000 | 27 | 5.6e-15 | 377 |
| VAGRANT | fs10/k3 | neutral_plus | 46 | 0.505 | +0.014 | +0.025 | saturated | 0.530 | 0.531 | 0.998 | 1.000 | 49 | 2.5e-15 | 377 |
| VAGRANT | fs10/k3 | neutral_plus | 47 | 0.497 | +0.020 | +0.051 | saturated | 0.547 | 0.548 | 0.919 | 1.000 | 3 | 3.3e-15 | 377 |
| VAGRANT | fs10/k3 | neutral_plus | 48 | 0.499 | +0.003 | +0.010 | saturated | 0.508 | 0.518 | 1.000 | 1.000 | 11 | 4.5e-15 | 294 |
| VAGRANT | fs10/k3 | neutral_plus | 49 | 0.499 | -0.022 | -0.124 | grows | 0.624 | 0.630 | 0.675 | 1.000 | 6 | 4.1e-15 | 294 |
| VAGRANT | fs10/k3 | neutral_plus | 50 | 0.500 | -0.007 | -0.013 | saturated | 0.514 | 0.514 | 1.000 | 1.000 | 59 | 4.1e-15 | 294 |
| VAGRANT | fs10/k3 | neutral_minus | 1 | 0.501 | -0.005 | -0.004 | saturated | 0.503 | 0.507 | 1.000 | 1.000 | 1 | 8.6e-16 | 18254 |
| VAGRANT | fs10/k3 | neutral_minus | 2 | 0.495 | +0.018 | -0.021 | saturated | 0.526 | 0.527 | 0.740 | 1.000 | 46 | 2.0e-15 | 19407 |
| VAGRANT | fs10/k3 | neutral_minus | 3 | 0.499 | -0.001 | -0.004 | saturated | 0.505 | 0.505 | 1.000 | 1.000 | 2 | 5.6e-16 | 19476 |
| VAGRANT | fs10/k3 | neutral_minus | 4 | 0.498 | -0.010 | -0.013 | saturated | 0.515 | 0.515 | 1.000 | 1.000 | 1 | 1.1e-15 | 19651 |
| VAGRANT | fs10/k3 | neutral_minus | 5 | 0.502 | -0.000 | -0.000 | saturated | 0.498 | 0.499 | 1.000 | 1.000 | 1 | 3.7e-15 | 19736 |
| VAGRANT | fs10/k3 | neutral_minus | 6 | 0.493 | -0.002 | -0.000 | saturated | 0.508 | 0.509 | 1.000 | 1.000 | 1 | 4.2e-15 | 19399 |
| VAGRANT | fs10/k3 | neutral_minus | 7 | 0.499 | -0.019 | +0.001 | saturated | 0.500 | 0.506 | 0.769 | 1.000 | 45 | 2.2e-15 | 19437 |
| VAGRANT | fs10/k3 | neutral_minus | 8 | 0.499 | -0.004 | +0.006 | saturated | 0.505 | 0.505 | 1.000 | 1.000 | 1 | 8.7e-15 | 385 |
| VAGRANT | fs10/k3 | neutral_minus | 9 | 0.502 | +0.012 | +0.025 | saturated | 0.527 | 0.527 | 0.946 | 1.000 | 1 | 8.3e-15 | 385 |
| VAGRANT | fs10/k3 | neutral_minus | 10 | 0.506 | -0.011 | -0.013 | saturated | 0.507 | 0.507 | 1.000 | 1.000 | 1 | 8.2e-15 | 385 |
| VAGRANT | fs10/k3 | neutral_minus | 11 | 0.506 | +0.002 | -0.020 | saturated | 0.514 | 0.520 | 0.520 | 1.000 | 34 | 8.1e-15 | 385 |
| VAGRANT | fs10/k3 | neutral_minus | 12 | 0.501 | +0.012 | +0.012 | saturated | 0.514 | 0.514 | 1.000 | 1.000 | 1 | 1.2e-14 | 385 |
| VAGRANT | fs10/k3 | neutral_minus | 13 | 0.504 | +0.003 | +0.005 | saturated | 0.509 | 0.509 | 1.000 | 1.000 | 1 | 1.0e-14 | 385 |
| VAGRANT | fs10/k3 | neutral_minus | 14 | 0.500 | +0.007 | +0.008 | saturated | 0.508 | 0.508 | 1.000 | 1.000 | 1 | 1.2e-14 | 385 |
| VAGRANT | fs10/k3 | neutral_minus | 15 | 0.503 | +0.013 | +0.013 | saturated | 0.515 | 0.517 | 1.000 | 1.000 | 1 | 8.0e-15 | 385 |
| VAGRANT | fs10/k3 | neutral_minus | 16 | 0.499 | -0.024 | +0.035 | reverses | 0.534 | 0.535 | 0.761 | 1.000 | 5 | 8.6e-15 | 385 |
| VAGRANT | fs10/k3 | neutral_minus | 17 | 0.504 | -0.008 | -0.012 | saturated | 0.508 | 0.508 | 1.000 | 1.000 | 1 | 9.6e-15 | 385 |
| VAGRANT | fs10/k3 | neutral_minus | 18 | 0.493 | +0.001 | -0.004 | saturated | 0.511 | 0.511 | 1.000 | 1.000 | 1 | 7.1e-15 | 378 |
| VAGRANT | fs10/k3 | neutral_minus | 19 | 0.498 | -0.002 | -0.009 | saturated | 0.511 | 0.511 | 0.978 | 1.000 | 1 | 7.8e-15 | 378 |
| VAGRANT | fs10/k3 | neutral_minus | 20 | 0.499 | -0.024 | -0.025 | saturated | 0.527 | 0.535 | 0.670 | 1.000 | 76 | 1.1e-14 | 378 |
| VAGRANT | fs10/k3 | neutral_minus | 21 | 0.495 | -0.006 | -0.003 | saturated | 0.508 | 0.511 | 0.998 | 1.000 | 1 | 9.8e-15 | 378 |
| VAGRANT | fs10/k3 | neutral_minus | 22 | 0.501 | +0.004 | +0.004 | saturated | 0.505 | 0.506 | 0.937 | 1.000 | 1 | 1.0e-14 | 378 |
| VAGRANT | fs10/k3 | neutral_minus | 23 | 0.504 | +0.029 | +0.030 | saturated | 0.534 | 0.539 | 0.904 | 1.000 | 1 | 9.2e-15 | 378 |
| VAGRANT | fs10/k3 | neutral_minus | 24 | 0.505 | -0.012 | -0.009 | saturated | 0.504 | 0.508 | 1.000 | 1.000 | 1 | 7.5e-15 | 378 |
| VAGRANT | fs10/k3 | neutral_minus | 25 | 0.500 | -0.006 | -0.002 | saturated | 0.502 | 0.508 | 0.996 | 1.000 | 1 | 9.3e-15 | 378 |
| VAGRANT | fs10/k3 | neutral_minus | 26 | 0.499 | +0.002 | +0.000 | saturated | 0.499 | 0.502 | 0.986 | 1.000 | 1 | 1.0e-14 | 378 |
| VAGRANT | fs10/k3 | neutral_minus | 27 | 0.491 | -0.001 | -0.004 | saturated | 0.512 | 0.513 | 0.953 | 1.000 | 1 | 9.0e-15 | 378 |
| VAGRANT | fs10/k3 | neutral_minus | 28 | 0.499 | +0.024 | +0.046 | saturated | 0.545 | 0.545 | 0.726 | 1.000 | 40 | 1.1e-14 | 374 |
| VAGRANT | fs10/k3 | neutral_minus | 29 | 0.508 | -0.014 | -0.015 | saturated | 0.507 | 0.507 | 0.970 | 1.000 | 1 | 8.7e-15 | 374 |
| VAGRANT | fs10/k3 | neutral_minus | 30 | 0.498 | +0.001 | +0.001 | saturated | 0.498 | 0.501 | 1.000 | 1.000 | 1 | 1.1e-14 | 374 |
| VAGRANT | fs10/k3 | neutral_minus | 31 | 0.499 | -0.008 | +0.022 | saturated | 0.521 | 0.522 | 0.944 | 1.000 | 9 | 6.9e-15 | 374 |
| VAGRANT | fs10/k3 | neutral_minus | 32 | 0.504 | +0.017 | +0.016 | saturated | 0.521 | 0.522 | 1.000 | 1.000 | 2 | 9.1e-15 | 374 |
| VAGRANT | fs10/k3 | neutral_minus | 33 | 0.495 | -0.007 | -0.011 | saturated | 0.517 | 0.518 | 0.991 | 1.000 | 1 | 6.7e-15 | 374 |
| VAGRANT | fs10/k3 | neutral_minus | 34 | 0.501 | +0.001 | +0.009 | saturated | 0.510 | 0.512 | 0.968 | 1.000 | 1 | 1.1e-14 | 374 |
| VAGRANT | fs10/k3 | neutral_minus | 35 | 0.497 | -0.002 | -0.001 | saturated | 0.504 | 0.509 | 1.000 | 1.000 | 1 | 1.0e-14 | 374 |
| VAGRANT | fs10/k3 | neutral_minus | 36 | 0.500 | -0.010 | -0.011 | saturated | 0.511 | 0.511 | 1.000 | 1.000 | 1 | 1.1e-14 | 374 |
| VAGRANT | fs10/k3 | neutral_minus | 37 | 0.502 | -0.004 | -0.004 | saturated | 0.502 | 0.503 | 1.000 | 1.000 | 1 | 6.5e-15 | 374 |
| VAGRANT | fs10/k3 | neutral_minus | 38 | 0.507 | -0.029 | -0.020 | saturated | 0.513 | 0.522 | 0.736 | 1.000 | 58 | 1.1e-14 | 377 |
| VAGRANT | fs10/k3 | neutral_minus | 39 | 0.504 | -0.012 | -0.013 | saturated | 0.508 | 0.509 | 1.000 | 1.000 | 1 | 8.6e-15 | 377 |
| VAGRANT | fs10/k3 | neutral_minus | 40 | 0.497 | -0.008 | -0.001 | saturated | 0.504 | 0.514 | 1.000 | 1.000 | 2 | 7.3e-15 | 377 |
| VAGRANT | fs10/k3 | neutral_minus | 41 | 0.500 | +0.001 | +0.001 | saturated | 0.501 | 0.503 | 1.000 | 1.000 | 1 | 6.2e-15 | 377 |
| VAGRANT | fs10/k3 | neutral_minus | 42 | 0.502 | +0.001 | +0.003 | saturated | 0.505 | 0.506 | 1.000 | 1.000 | 1 | 7.9e-15 | 377 |
| VAGRANT | fs10/k3 | neutral_minus | 43 | 0.500 | -0.001 | +0.001 | saturated | 0.500 | 0.502 | 1.000 | 1.000 | 1 | 8.9e-15 | 377 |
| VAGRANT | fs10/k3 | neutral_minus | 44 | 0.496 | +0.002 | +0.050 | saturated | 0.546 | 0.547 | 0.564 | 1.000 | 45 | 8.9e-15 | 377 |
| VAGRANT | fs10/k3 | neutral_minus | 45 | 0.498 | -0.000 | -0.002 | saturated | 0.504 | 0.505 | 1.000 | 1.000 | 1 | 9.4e-15 | 377 |
| VAGRANT | fs10/k3 | neutral_minus | 46 | 0.505 | -0.009 | -0.007 | saturated | 0.502 | 0.508 | 0.993 | 1.000 | 1 | 9.9e-15 | 377 |
| VAGRANT | fs10/k3 | neutral_minus | 47 | 0.497 | -0.009 | -0.006 | saturated | 0.509 | 0.513 | 0.979 | 1.000 | 1 | 7.6e-15 | 377 |
| VAGRANT | fs10/k3 | neutral_minus | 48 | 0.499 | +0.064 | +0.053 | saturated | 0.552 | 0.573 | 0.898 | 1.000 | 50 | 8.7e-15 | 294 |
| VAGRANT | fs10/k3 | neutral_minus | 49 | 0.499 | +0.006 | +0.007 | saturated | 0.506 | 0.507 | 1.000 | 1.000 | 1 | 1.0e-14 | 294 |
| VAGRANT | fs10/k3 | neutral_minus | 50 | 0.500 | +0.008 | +0.004 | saturated | 0.503 | 0.507 | 0.996 | 1.000 | 1 | 1.0e-14 | 294 |

