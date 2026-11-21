# Species scan summary

Source: `outputs/species_scan_20261117`. Rules: docs/SPECIES-SCAN-2026-11-16.md. Seeds per arm: 20; selection needs 16 of 20 treatment seeds outside E; distinct needs median ratio <= 1/2 and 16 of 20 seeds below control; no effect is fewer than 12.

## Run counts

Expected under the design: 30 species x 4 cells x 20 seeds x 3 arms = 7200. Present: **7173**.

**PARTIAL: 7173 of 7200 runs present. Every verdict below is computed only on species x cell with all arms and all 20 seeds present; the rest print `incomplete`, and the aggregates are over the complete species only (PARTIAL until all are present).**

| cell | species with any run | complete species (all arms, all seeds) | runs |
|---|---|---|---|
| k0/fs0 | 30 | 30 | 1800 |
| k3/fs0 | 30 | 29 | 1773 |
| k0/fs10 | 30 | 30 | 1800 |
| k3/fs10 | 30 | 30 | 1800 |

## Per species x cell: selection (primary E = max |delta| over the cell's neutral runs)

Cell entry: verdict (treatment seeds outside E of 20; E; winner(s); median final share of the winner over the outside seeds). `incomplete` = the cell lacks runs.

| species | k0/fs0 | k3/fs0 | k0/fs10 | k3/fs10 |
|---|---|---|---|---|
| OSCILLIS | no selection detected (9/20; E 0.022; +u,-u; 0.54) | no selection detected (12/20; E 0.031; +u,-u; 0.56) | no selection detected (6/20; E 0.056; +u; 0.56) | no selection detected (15/20; E 0.033; +u; 0.58) |
| MITOSA | no selection detected (1/20; E 0.064; +u; 0.58) | no selection detected (2/20; E 0.087; +u; 0.61) | no selection detected (3/20; E 0.040; +u,-u; 0.58) | no selection detected (3/20; E 0.065; +u; 0.58) |
| VAGRANT | no selection detected (5/20; E 0.045; +u,-u; 0.59) | incomplete | no selection detected (6/20; E 0.031; +u,-u; 0.56) | large but inconsistent (18/20; E 0.039; +u,-u; 0.73) |
| CORONA | large but inconsistent (20/20; E 0.009; +u,-u; 0.54) | large but inconsistent (19/20; E 0.010; +u,-u; 0.55) | selection (20/20; E 0.002; +u; 0.51) | selection (20/20; E 0.002; +u; 0.51) |
| SPLITTER | no selection detected (8/20; E 0.009; +u,-u; 0.52) | no selection detected (12/20; E 0.008; -u; 0.51) | no selection detected (2/20; E 0.007; +u; 0.51) | no selection detected (2/20; E 0.007; +u,-u; 0.50) |
| DRIFTER | selection (17/20; E 0.057; +u; 0.59) | selection (18/20; E 0.071; +u; 0.67) | no selection detected (1/20; E 0.092; -u; 0.60) | no selection detected (11/20; E 0.095; -u; 0.63) |
| NUCLEUS | selection (18/20; E 0.017; -u; 0.54) | selection (18/20; E 0.010; -u; 0.53) | large but inconsistent (17/20; E 0.002; +u,-u; 0.52) | large but inconsistent (19/20; E 0.003; +u,-u; 0.53) |
| TENDRIL | no selection detected (9/20; E 0.010; +u; 0.51) | no selection detected (1/20; E 0.012; -u; 0.52) | selection (20/20; E 0.003; -u; 0.53) | selection (20/20; E 0.002; -u; 0.53) |
| ARBORIS | no selection detected (12/20; E 0.007; +u,-u; 0.51) | no selection detected (13/20; E 0.008; +u,-u; 0.51) | selection (17/20; E 0.005; -u; 0.51) | selection (17/20; E 0.005; -u; 0.51) |
| CILIATA | no selection detected (13/20; E 0.017; -u; 0.55) | no selection detected (15/20; E 0.016; -u; 0.55) | no selection detected (13/20; E 0.005; +u,-u; 0.51) | no selection detected (11/20; E 0.004; +u; 0.51) |
| FLAGELLA | no selection detected (13/20; E 0.064; +u,-u; 0.63) | large but inconsistent (20/20; E 0.048; +u,-u; 0.61) | selection (20/20; E 0.045; +u; 0.61) | selection (20/20; E 0.028; +u; 0.58) |
| GLOBULA | selection (18/20; E 0.010; +u; 0.53) | no selection detected (15/20; E 0.011; +u,-u; 0.53) | no selection detected (15/20; E 0.012; -u; 0.52) | no selection detected (7/20; E 0.018; -u; 0.52) |
| HELIX | no selection detected (3/20; E 0.016; +u,-u; 0.52) | no selection detected (1/20; E 0.018; +u; 0.52) | large but inconsistent (19/20; E 0.005; +u,-u; 0.53) | large but inconsistent (16/20; E 0.008; +u,-u; 0.54) |
| LUMINA | no selection detected (10/20; E 0.016; +u,-u; 0.53) | selection (20/20; E 0.019; +u; 0.59) | no selection detected (14/20; E 0.026; +u,-u; 0.55) | large but inconsistent (18/20; E 0.014; +u,-u; 0.56) |
| MEDUSA | no selection detected (10/20; E 0.026; +u,-u; 0.54) | no selection detected (11/20; E 0.026; +u,-u; 0.54) | no selection detected (13/20; E 0.036; +u,-u; 0.55) | selection (20/20; E 0.016; -u; 0.63) |
| NODULUS | no selection detected (12/20; E 0.007; +u,-u; 0.53) | no selection detected (11/20; E 0.007; +u,-u; 0.53) | selection (16/20; E 0.002; -u; 0.51) | large but inconsistent (17/20; E 0.002; +u,-u; 0.51) |
| ORBITA | no selection detected (3/20; E 0.081; +u; 0.61) | no selection detected (5/20; E 0.067; +u; 0.60) | large but inconsistent (19/20; E 0.018; +u,-u; 0.57) | selection (16/20; E 0.018; +u; 0.58) |
| PULSARA | no selection detected (11/20; E 0.007; +u,-u; 0.51) | no selection detected (10/20; E 0.006; +u,-u; 0.51) | selection (20/20; E 0.002; -u; 0.53) | selection (19/20; E 0.002; -u; 0.52) |
| QUASARIA | no selection detected (6/20; E 0.006; +u,-u; 0.51) | no selection detected (8/20; E 0.005; +u,-u; 0.51) | selection (20/20; E 0.005; -u; 0.51) | no selection detected (12/20; E 0.006; -u; 0.51) |
| RADIATA | no selection detected (9/20; E 0.008; +u,-u; 0.52) | no selection detected (11/20; E 0.008; +u,-u; 0.51) | large but inconsistent (17/20; E 0.003; +u,-u; 0.51) | no selection detected (15/20; E 0.003; +u,-u; 0.51) |
| SPIRALIS | large but inconsistent (17/20; E 0.009; +u,-u; 0.52) | no selection detected (14/20; E 0.011; +u,-u; 0.52) | selection (18/20; E 0.003; +u; 0.51) | selection (17/20; E 0.003; +u; 0.51) |
| TORQUATA | selection (17/20; E 0.019; +u; 0.54) | no selection detected (15/20; E 0.018; +u; 0.54) | large but inconsistent (16/20; E 0.009; +u,-u; 0.51) | no selection detected (15/20; E 0.009; +u,-u; 0.52) |
| UNDULA | no selection detected (14/20; E 0.008; +u,-u; 0.52) | selection (16/20; E 0.007; -u; 0.52) | selection (20/20; E 0.002; +u; 0.51) | selection (20/20; E 0.002; +u; 0.51) |
| VESICA | no selection detected (7/20; E 0.037; +u,-u; 0.55) | no selection detected (5/20; E 0.073; -u; 0.59) | selection (20/20; E 0.037; +u; 0.63) | no selection detected (3/20; E 0.090; +u; 0.60) |
| XENIA | no selection detected (9/20; E 0.012; +u,-u; 0.52) | no selection detected (12/20; E 0.013; +u,-u; 0.52) | selection (20/20; E 0.007; -u; 0.52) | selection (16/20; E 0.007; -u; 0.52) |
| YGGRA | no selection detected (15/20; E 0.016; +u; 0.54) | selection (17/20; E 0.016; +u; 0.54) | no selection detected (9/20; E 0.003; +u,-u; 0.50) | no selection detected (12/20; E 0.003; +u; 0.50) |
| ZONATA | large but inconsistent (17/20; E 0.018; +u,-u; 0.54) | no selection detected (14/20; E 0.015; +u,-u; 0.53) | large but inconsistent (20/20; E 0.006; +u,-u; 0.54) | large but inconsistent (16/20; E 0.005; +u,-u; 0.53) |
| ANTENNA | no selection detected (7/20; E 0.042; +u; 0.57) | no selection detected (7/20; E 0.026; +u,-u; 0.54) | no selection detected (7/20; E 0.016; -u; 0.53) | selection (17/20; E 0.012; -u; 0.54) |
| BIFIDA | no selection detected (14/20; E 0.004; +u,-u; 0.51) | no selection detected (14/20; E 0.004; +u,-u; 0.51) | large but inconsistent (19/20; E 0.004; +u,-u; 0.51) | selection (17/20; E 0.004; -u; 0.51) |
| CATENA | no selection detected (11/20; E 0.070; +u,-u; 0.60) | no selection detected (5/20; E 0.086; +u,-u; 0.65) | no selection detected (13/20; E 0.047; -u; 0.57) | no selection detected (2/20; E 0.062; -u; 0.66) |

Secondary (labelled): same rule with E = 95th percentile of the neutral |delta| (linear interpolation).

| species | k0/fs0 | k3/fs0 | k0/fs10 | k3/fs10 |
|---|---|---|---|---|
| OSCILLIS | no selection detected (11/20; E 0.017) | no selection detected (15/20; E 0.017) | no selection detected (14/20; E 0.025) | large but inconsistent (17/20; E 0.021) |
| MITOSA | no selection detected (4/20; E 0.034) | no selection detected (4/20; E 0.076) | no selection detected (7/20; E 0.027) | no selection detected (10/20; E 0.033) |
| VAGRANT | no selection detected (11/20; E 0.023) | incomplete | no selection detected (9/20; E 0.024) | large but inconsistent (19/20; E 0.025) |
| CORONA | large but inconsistent (20/20; E 0.007) | large but inconsistent (19/20; E 0.007) | selection (20/20; E 0.002) | selection (20/20; E 0.002) |
| SPLITTER | no selection detected (8/20; E 0.007) | no selection detected (12/20; E 0.008) | no selection detected (3/20; E 0.006) | no selection detected (2/20; E 0.006) |
| DRIFTER | selection (19/20; E 0.034) | selection (18/20; E 0.061) | no selection detected (6/20; E 0.053) | selection (18/20; E 0.055) |
| NUCLEUS | selection (19/20; E 0.009) | selection (19/20; E 0.009) | large but inconsistent (17/20; E 0.002) | large but inconsistent (20/20; E 0.003) |
| TENDRIL | no selection detected (12/20; E 0.008) | no selection detected (3/20; E 0.009) | selection (20/20; E 0.002) | selection (20/20; E 0.002) |
| ARBORIS | no selection detected (13/20; E 0.006) | no selection detected (14/20; E 0.006) | selection (19/20; E 0.003) | selection (20/20; E 0.003) |
| CILIATA | no selection detected (13/20; E 0.016) | no selection detected (15/20; E 0.015) | large but inconsistent (17/20; E 0.002) | selection (16/20; E 0.002) |
| FLAGELLA | no selection detected (14/20; E 0.053) | large but inconsistent (20/20; E 0.031) | selection (20/20; E 0.017) | selection (20/20; E 0.025) |
| GLOBULA | selection (18/20; E 0.009) | large but inconsistent (17/20; E 0.009) | selection (19/20; E 0.008) | selection (18/20; E 0.009) |
| HELIX | no selection detected (4/20; E 0.016) | no selection detected (2/20; E 0.014) | large but inconsistent (19/20; E 0.004) | large but inconsistent (17/20; E 0.006) |
| LUMINA | no selection detected (13/20; E 0.014) | selection (20/20; E 0.014) | large but inconsistent (20/20; E 0.015) | large but inconsistent (19/20; E 0.011) |
| MEDUSA | no selection detected (13/20; E 0.023) | no selection detected (11/20; E 0.022) | large but inconsistent (18/20; E 0.016) | selection (20/20; E 0.011) |
| NODULUS | no selection detected (12/20; E 0.004) | no selection detected (12/20; E 0.005) | selection (16/20; E 0.002) | large but inconsistent (17/20; E 0.002) |
| ORBITA | no selection detected (14/20; E 0.045) | no selection detected (9/20; E 0.046) | large but inconsistent (20/20; E 0.011) | selection (16/20; E 0.016) |
| PULSARA | no selection detected (12/20; E 0.005) | no selection detected (13/20; E 0.005) | selection (20/20; E 0.002) | selection (19/20; E 0.001) |
| QUASARIA | no selection detected (9/20; E 0.005) | no selection detected (11/20; E 0.003) | selection (20/20; E 0.004) | no selection detected (15/20; E 0.004) |
| RADIATA | no selection detected (10/20; E 0.007) | no selection detected (11/20; E 0.007) | large but inconsistent (19/20; E 0.002) | large but inconsistent (16/20; E 0.002) |
| SPIRALIS | large but inconsistent (19/20; E 0.006) | large but inconsistent (17/20; E 0.006) | selection (18/20; E 0.002) | selection (19/20; E 0.002) |
| TORQUATA | selection (18/20; E 0.011) | selection (16/20; E 0.012) | large but inconsistent (19/20; E 0.004) | large but inconsistent (19/20; E 0.004) |
| UNDULA | large but inconsistent (16/20; E 0.006) | large but inconsistent (17/20; E 0.006) | selection (20/20; E 0.002) | selection (20/20; E 0.002) |
| VESICA | no selection detected (8/20; E 0.032) | no selection detected (8/20; E 0.047) | selection (20/20; E 0.025) | no selection detected (13/20; E 0.027) |
| XENIA | no selection detected (12/20; E 0.006) | large but inconsistent (16/20; E 0.006) | selection (20/20; E 0.003) | selection (17/20; E 0.003) |
| YGGRA | selection (18/20; E 0.008) | selection (18/20; E 0.007) | no selection detected (12/20; E 0.002) | selection (16/20; E 0.002) |
| ZONATA | large but inconsistent (18/20; E 0.010) | no selection detected (15/20; E 0.012) | large but inconsistent (20/20; E 0.004) | large but inconsistent (16/20; E 0.003) |
| ANTENNA | no selection detected (10/20; E 0.027) | no selection detected (8/20; E 0.026) | no selection detected (11/20; E 0.010) | selection (17/20; E 0.010) |
| BIFIDA | large but inconsistent (16/20; E 0.003) | no selection detected (14/20; E 0.003) | large but inconsistent (19/20; E 0.003) | selection (17/20; E 0.003) |
| CATENA | no selection detected (11/20; E 0.065) | no selection detected (5/20; E 0.079) | selection (17/20; E 0.025) | no selection detected (10/20; E 0.026) |

## Species-level aggregate: frequency of selection or takeover (primary E)

### all species

| cell | species complete | selection or takeover | frequency | exact 95% interval | takeover only | large but inconsistent |
|---|---|---|---|---|---|---|
| k0/fs0 | 30 | 4 | 0.133 | [0.038, 0.307] | 0 | 3 |
| k3/fs0 | 29 | 5 | 0.172 | [0.058, 0.358] | 0 | 2 |
| k0/fs10 | 30 | 11 | 0.367 | [0.199, 0.561] | 0 | 7 |
| k3/fs10 | 30 | 12 | 0.400 | [0.227, 0.594] | 0 | 6 |

Paired test, food sensing on vs off at the same kappa (McNemar exact, two-sided, on species complete in both cells): the frequency counts as changed if on > off and p < 0.05.

| kappa | fs off -> fs on | pairs | on only | off only | count off | count on | p | frequency of selection changes |
|---|---|---|---|---|---|---|---|---|
| 0 | 0 -> 10 | 30 | 11 | 4 | 4 | 11 | 0.1185 | no |
| 3 | 0 -> 10 | 29 | 11 | 4 | 5 | 12 | 0.1185 | no |

### excluding the five cadence-dependent species

| cell | species complete | selection or takeover | frequency | exact 95% interval | takeover only | large but inconsistent |
|---|---|---|---|---|---|---|
| k0/fs0 | 25 | 3 | 0.120 | [0.025, 0.312] | 0 | 2 |
| k3/fs0 | 24 | 5 | 0.208 | [0.071, 0.422] | 0 | 2 |
| k0/fs10 | 25 | 8 | 0.320 | [0.149, 0.535] | 0 | 6 |
| k3/fs10 | 25 | 8 | 0.320 | [0.149, 0.535] | 0 | 6 |

Paired test, food sensing on vs off at the same kappa (McNemar exact, two-sided, on species complete in both cells): the frequency counts as changed if on > off and p < 0.05.

| kappa | fs off -> fs on | pairs | on only | off only | count off | count on | p | frequency of selection changes |
|---|---|---|---|---|---|---|---|---|
| 0 | 0 -> 10 | 25 | 8 | 3 | 3 | 8 | 0.2266 | no |
| 3 | 0 -> 10 | 24 | 7 | 4 | 5 | 8 | 0.5488 | no |

### original three (001-003)

| cell | species complete | selection or takeover | frequency | exact 95% interval | takeover only | large but inconsistent |
|---|---|---|---|---|---|---|
| k0/fs0 | 3 | 0 | 0.000 | [0.000, 0.708] | 0 | 0 |
| k3/fs0 | 2 | 0 | 0.000 | [0.000, 0.842] | 0 | 0 |
| k0/fs10 | 3 | 0 | 0.000 | [0.000, 0.708] | 0 | 0 |
| k3/fs10 | 3 | 0 | 0.000 | [0.000, 0.708] | 0 | 1 |

Paired test, food sensing on vs off at the same kappa (McNemar exact, two-sided, on species complete in both cells): the frequency counts as changed if on > off and p < 0.05.

| kappa | fs off -> fs on | pairs | on only | off only | count off | count on | p | frequency of selection changes |
|---|---|---|---|---|---|---|---|---|
| 0 | 0 -> 10 | 3 | 0 | 0 | 0 | 0 | 1.0000 | no |
| 3 | 0 -> 10 | 2 | 0 | 0 | 0 | 0 | 1.0000 | no |

## Distribution across species (all complete species per cell)

Winner's median final share = for each species, the larger lineage's median final share over its treatment seeds (descriptive, defined whatever the verdict). End hybrid fraction = per-species median over treatment seeds.

| cell | species | winner's median final share | end hybrid fraction |
|---|---|---|---|
| k0/fs0 | 30 | min 0.501, Q1 0.506, median 0.511, Q3 0.537, max 0.601 | min 0.524, Q1 1.000, median 1.000, Q3 1.000, max 1.000 |
| k3/fs0 | 29 | min 0.500, Q1 0.508, median 0.518, Q3 0.534, max 0.666 | min 0.000, Q1 0.001, median 0.055, Q3 1.000, max 1.000 |
| k0/fs10 | 30 | min 0.501, Q1 0.506, median 0.512, Q3 0.532, max 0.628 | min 0.481, Q1 0.982, median 1.000, Q3 1.000, max 1.000 |
| k3/fs10 | 30 | min 0.500, Q1 0.509, median 0.517, Q3 0.538, max 0.720 | min 0.000, Q1 0.000, median 0.026, Q3 1.000, max 1.000 |

## Lineage distinctness: kappa 3 vs kappa 0, same food sensing, treatment arm

### fs 0

| species | median hybrid k0 | median hybrid k3 | ratio | seeds k3 < k0 | verdict |
|---|---|---|---|---|---|
| OSCILLIS | 1.000 | 0.099 | 0.10 | 19 of 20 | distinct |
| MITOSA | 1.000 | 0.000 | 0.00 | 20 of 20 | distinct |
| CORONA | 1.000 | 1.000 | 1.00 | 6 of 20 | no effect |
| SPLITTER | 1.000 | 1.000 | 1.00 | 12 of 20 | partial |
| DRIFTER | 0.996 | 0.640 | 0.64 | 20 of 20 | partial |
| NUCLEUS | 1.000 | 0.000 | 0.00 | 20 of 20 | distinct |
| TENDRIL | 1.000 | 0.000 | 0.00 | 20 of 20 | distinct |
| ARBORIS | 1.000 | 1.000 | 1.00 | 11 of 20 | no effect |
| CILIATA | 1.000 | 0.006 | 0.01 | 19 of 20 | distinct |
| FLAGELLA | 0.524 | 0.055 | 0.10 | 20 of 20 | distinct |
| GLOBULA | 1.000 | 1.000 | 1.00 | 5 of 20 | no effect |
| HELIX | 1.000 | 0.232 | 0.23 | 20 of 20 | distinct |
| LUMINA | 1.000 | 0.098 | 0.10 | 20 of 20 | distinct |
| MEDUSA | 1.000 | 0.698 | 0.70 | 16 of 20 | partial |
| NODULUS | 1.000 | 1.000 | 1.00 | 7 of 20 | no effect |
| ORBITA | 0.843 | 0.000 | 0.00 | 20 of 20 | distinct |
| PULSARA | 1.000 | 0.471 | 0.47 | 17 of 20 | distinct |
| QUASARIA | 1.000 | 0.001 | 0.00 | 19 of 20 | distinct |
| RADIATA | 1.000 | 0.041 | 0.04 | 18 of 20 | distinct |
| SPIRALIS | 1.000 | 1.000 | 1.00 | 5 of 20 | no effect |
| TORQUATA | 1.000 | 1.000 | 1.00 | 10 of 20 | no effect |
| UNDULA | 1.000 | 0.002 | 0.00 | 20 of 20 | distinct |
| VESICA | 0.893 | 0.052 | 0.06 | 20 of 20 | distinct |
| XENIA | 1.000 | 1.000 | 1.00 | 8 of 20 | no effect |
| YGGRA | 1.000 | 0.000 | 0.00 | 16 of 20 | distinct |
| ZONATA | 1.000 | 0.000 | 0.00 | 20 of 20 | distinct |
| ANTENNA | 1.000 | 0.001 | 0.00 | 20 of 20 | distinct |
| BIFIDA | 1.000 | 0.000 | 0.00 | 15 of 20 | partial |
| CATENA | 0.803 | 0.001 | 0.00 | 20 of 20 | distinct |

Distinct in 18 of 29 species (0.621, exact 95% [0.423, 0.793]); partial 4; no effect 7.

### fs 10

| species | median hybrid k0 | median hybrid k3 | ratio | seeds k3 < k0 | verdict |
|---|---|---|---|---|---|
| OSCILLIS | 0.481 | 0.000 | 0.00 | 16 of 20 | distinct |
| MITOSA | 0.673 | 0.004 | 0.01 | 18 of 20 | distinct |
| VAGRANT | 0.987 | 0.000 | 0.00 | 20 of 20 | distinct |
| CORONA | 1.000 | 1.000 | 1.00 | 5 of 20 | no effect |
| SPLITTER | 1.000 | 1.000 | 1.00 | 3 of 20 | no effect |
| DRIFTER | 0.892 | 0.000 | 0.00 | 20 of 20 | distinct |
| NUCLEUS | 0.968 | 0.000 | 0.00 | 20 of 20 | distinct |
| TENDRIL | 1.000 | 0.000 | 0.00 | 20 of 20 | distinct |
| ARBORIS | 1.000 | 1.000 | 1.00 | 7 of 20 | no effect |
| CILIATA | 1.000 | 0.000 | 0.00 | 20 of 20 | distinct |
| FLAGELLA | 0.867 | 0.030 | 0.03 | 20 of 20 | distinct |
| GLOBULA | 1.000 | 0.979 | 0.98 | 13 of 20 | partial |
| HELIX | 1.000 | 0.658 | 0.66 | 18 of 20 | partial |
| LUMINA | 1.000 | 0.004 | 0.00 | 20 of 20 | distinct |
| MEDUSA | 0.964 | 0.000 | 0.00 | 20 of 20 | distinct |
| NODULUS | 1.000 | 1.000 | 1.00 | 1 of 20 | no effect |
| ORBITA | 0.980 | 0.000 | 0.00 | 20 of 20 | distinct |
| PULSARA | 1.000 | 0.000 | 0.00 | 20 of 20 | distinct |
| QUASARIA | 1.000 | 1.000 | 1.00 | 4 of 20 | no effect |
| RADIATA | 1.000 | 0.000 | 0.00 | 20 of 20 | distinct |
| SPIRALIS | 1.000 | 0.000 | 0.00 | 20 of 20 | distinct |
| TORQUATA | 1.000 | 1.000 | 1.00 | 5 of 20 | no effect |
| UNDULA | 1.000 | 0.022 | 0.02 | 19 of 20 | distinct |
| VESICA | 1.000 | 0.998 | 1.00 | 13 of 20 | partial |
| XENIA | 1.000 | 0.403 | 0.40 | 15 of 20 | partial |
| YGGRA | 1.000 | 1.000 | 1.00 | 10 of 20 | no effect |
| ZONATA | 1.000 | 0.186 | 0.19 | 19 of 20 | distinct |
| ANTENNA | 1.000 | 0.612 | 0.61 | 17 of 20 | partial |
| BIFIDA | 1.000 | 1.000 | 1.00 | 5 of 20 | no effect |
| CATENA | 0.880 | 0.000 | 0.00 | 20 of 20 | distinct |

Distinct in 17 of 30 species (0.567, exact 95% [0.374, 0.745]); partial 5; no effect 8.

### Distinctness frequency, fs 0 vs fs 10 (McNemar exact, species with a verdict at both)

| subgroup | pairs | distinct fs on only | distinct fs off only | distinct off | distinct on | p | changes |
|---|---|---|---|---|---|---|---|
| all species | 29 | 3 | 5 | 18 | 16 | 0.7266 | no |
| excluding the five cadence-dependent species | 24 | 1 | 5 | 17 | 13 | 0.2188 | no |
| original three (001-003) | 2 | 0 | 0 | 2 | 2 | 1.0000 | no |

## Neutral-arm sanity (mean neutral delta within 2 SE of zero; else flagged as harness asymmetry, not voiding)

| cell | species | neutral runs | species flagged | max |mean/SE| over species | pooled mean delta | pooled SE |
|---|---|---|---|---|---|---|---|
| k0/fs0 | 30 | 1200 | 2 | 4.28 | +0.00003 | 0.00032 |
| k3/fs0 | 29 | 1160 | 1 | 2.34 | -0.00025 | 0.00037 |
| k0/fs10 | 30 | 1200 | 1 | 2.40 | -0.00019 | 0.00023 |
| k3/fs10 | 30 | 1200 | 1 | 2.24 | -0.00022 | 0.00024 |

Flagged species-cells (about 5% of tests are expected by chance): k0/fs0 GLOBULA (mean -0.0016, z -2.27); k0/fs0 HELIX (mean +0.0043, z +4.28); k3/fs0 GLOBULA (mean -0.0018, z -2.34); k0/fs10 GLOBULA (mean -0.0014, z -2.40); k3/fs10 PULSARA (mean -0.0003, z -2.24)

## Conservation: max relative drift of sum(body)+sum(food)

| cell | max drift over runs |
|---|---|
| k0/fs0 | 6.75e-15 |
| k3/fs0 | 6.75e-15 |
| k0/fs10 | 6.61e-15 |
| k3/fs10 | 6.76e-15 |

