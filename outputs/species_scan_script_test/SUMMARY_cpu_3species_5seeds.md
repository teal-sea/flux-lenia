# Species scan summary

Source: `/home/thomas/.hermes/profiles/forge/cache/scratch/scanflat`. Rules: docs/SPECIES-SCAN-2026-11-16.md. Seeds per arm: 5; selection needs 4 of 5 treatment seeds outside E; distinct needs median ratio <= 1/2 and 4 of 5 seeds below control; no effect is fewer than 3.

## Run counts

Expected under the design: 3 species x 4 cells x 5 seeds x 3 arms = 180. Present: **90**.

| cell | species with any run | complete species (all arms, all seeds) | runs |
|---|---|---|---|
| k0/fs0 | 3 | 3 | 45 |
| k3/fs0 | 3 | 3 | 45 |

## Per species x cell: selection (primary E = max |delta| over the cell's neutral runs)

Cell entry: verdict (treatment seeds outside E of 5; E; winner(s); median final share of the winner over the outside seeds). `incomplete` = the cell lacks runs.

| species | k0/fs0 | k3/fs0 |
|---|---|---|
| OSCILLIS | no selection detected (0/5; E 0.014; -; -) | large but inconsistent (4/5; E 0.014; +u,-u; 0.52) |
| MITOSA | no selection detected (0/5; E 0.058; -; -) | no selection detected (1/5; E 0.075; +u; 0.59) |
| VAGRANT | no selection detected (1/5; E 0.038; +u; 0.66) | no selection detected (3/5; E 0.032; +u; 0.57) |

Secondary (labelled): same rule with E = 95th percentile of the neutral |delta| (linear interpolation).

| species | k0/fs0 | k3/fs0 |
|---|---|---|
| OSCILLIS | no selection detected (2/5; E 0.013) | large but inconsistent (4/5; E 0.010) |
| MITOSA | no selection detected (0/5; E 0.044) | no selection detected (1/5; E 0.055) |
| VAGRANT | no selection detected (1/5; E 0.035) | no selection detected (3/5; E 0.027) |

## Species-level aggregate: frequency of selection or takeover (primary E)

### all species

| cell | species complete | selection or takeover | frequency | exact 95% interval | takeover only | large but inconsistent |
|---|---|---|---|---|---|---|
| k0/fs0 | 3 | 0 | 0.000 | [0.000, 0.708] | 0 | 0 |
| k3/fs0 | 3 | 0 | 0.000 | [0.000, 0.708] | 0 | 1 |

Paired test, food sensing on vs off at the same kappa (McNemar exact, two-sided, on species complete in both cells): the frequency counts as changed if on > off and p < 0.05.

| kappa | fs off -> fs on | pairs | on only | off only | count off | count on | p | frequency of selection changes |
|---|---|---|---|---|---|---|---|---|

### excluding the five cadence-dependent species

| cell | species complete | selection or takeover | frequency | exact 95% interval | takeover only | large but inconsistent |
|---|---|---|---|---|---|---|
| k0/fs0 | 3 | 0 | 0.000 | [0.000, 0.708] | 0 | 0 |
| k3/fs0 | 3 | 0 | 0.000 | [0.000, 0.708] | 0 | 1 |

Paired test, food sensing on vs off at the same kappa (McNemar exact, two-sided, on species complete in both cells): the frequency counts as changed if on > off and p < 0.05.

| kappa | fs off -> fs on | pairs | on only | off only | count off | count on | p | frequency of selection changes |
|---|---|---|---|---|---|---|---|---|

### original three (001-003)

| cell | species complete | selection or takeover | frequency | exact 95% interval | takeover only | large but inconsistent |
|---|---|---|---|---|---|---|
| k0/fs0 | 3 | 0 | 0.000 | [0.000, 0.708] | 0 | 0 |
| k3/fs0 | 3 | 0 | 0.000 | [0.000, 0.708] | 0 | 1 |

Paired test, food sensing on vs off at the same kappa (McNemar exact, two-sided, on species complete in both cells): the frequency counts as changed if on > off and p < 0.05.

| kappa | fs off -> fs on | pairs | on only | off only | count off | count on | p | frequency of selection changes |
|---|---|---|---|---|---|---|---|---|

## Distribution across species (all complete species per cell)

Winner's median final share = for each species, the larger lineage's median final share over its treatment seeds (descriptive, defined whatever the verdict). End hybrid fraction = per-species median over treatment seeds.

| cell | species | winner's median final share | end hybrid fraction |
|---|---|---|---|
| k0/fs0 | 3 | min 0.500, Q1 0.501, median 0.501, Q3 0.507, max 0.512 | min 0.502, Q1 0.712, median 0.921, Q3 0.930, max 0.939 |
| k3/fs0 | 3 | min 0.501, Q1 0.514, median 0.526, Q3 0.538, max 0.551 | min 0.000, Q1 0.000, median 0.000, Q3 0.157, max 0.313 |

## Lineage distinctness: kappa 3 vs kappa 0, same food sensing, treatment arm

### fs 0

| species | median hybrid k0 | median hybrid k3 | ratio | seeds k3 < k0 | verdict |
|---|---|---|---|---|---|
| OSCILLIS | 0.939 | 0.313 | 0.33 | 5 of 5 | distinct |
| MITOSA | 0.921 | 0.000 | 0.00 | 5 of 5 | distinct |
| VAGRANT | 0.502 | 0.000 | 0.00 | 5 of 5 | distinct |

Distinct in 3 of 3 species (1.000, exact 95% [0.292, 1.000]); partial 0; no effect 0.

## Neutral-arm sanity (mean neutral delta within 2 SE of zero; else flagged as harness asymmetry, not voiding)

| cell | species | neutral runs | species flagged | max |mean/SE| over species | pooled mean delta | pooled SE |
|---|---|---|---|---|---|---|---|
| k0/fs0 | 3 | 30 | 0 | 1.59 | +0.00412 | 0.00290 |
| k3/fs0 | 3 | 30 | 0 | 1.62 | +0.00278 | 0.00365 |

Flagged species-cells (about 5% of tests are expected by chance): none

## Conservation: max relative drift of sum(body)+sum(food)

| cell | max drift over runs |
|---|---|
| k0/fs0 | 2.75e-15 |
| k3/fs0 | 2.65e-15 |

