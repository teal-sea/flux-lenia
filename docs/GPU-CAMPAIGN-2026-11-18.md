# GPU campaign, 2026-11-18

## Questions

- Food-sensing pilot: which tested gain changes foraging without saturation or loss of conservation?
- Food-sensing factorial: does sensing cause rule-grade lineage selection, and does that require repulsion?
- Species scan: across the fixed species set, does sensing increase the frequency of selection and does repulsion preserve distinct lineages?
- Long horizon: does more time produce takeover or consistent selection, with sensing off versus on?

## Decision criteria fixed before the runs

The following are verbatim quotations from the retained design documents at base commit
`7404b8ab3e05ef30b2c83987babf551571c16c3d`. The GPU 2x2 document says it adds no rule.
Its later results are not substituted for the original criteria. `FINDINGS.md` supplies
measurement discipline, not an additional selection criterion for this campaign.

### `docs/FOOD-SENSING-2026-11-16.md:65-65`

> - **Pre-registered selection rule.** A candidate *changes foraging in a species* if `|Q_candidate - Q_ref| > R` for that species. A candidate **qualifies** if it changes foraging in **at least 2 of 3 species**, AND in all three of its runs the velocity saturation fraction `sat_frac` (fraction of body (channel, cell) velocities at the soft bound `|d| >= 0.9 max_step`, as defined on 2026-11-15) is below `1e-2` at every one of the 100 samples, AND in all three runs the max relative drift of `sum(body) + sum(food)` is at most `1e-12`. **Chosen `food_sense` = the smallest candidate that qualifies.** If none qualifies, the **largest candidate whose three runs are all non-saturating (every sample below `1e-2`) and conserve** is taken and this is said; if even none of those exists, the smallest candidate is taken. The main experiment runs either way.

### `docs/FOOD-SENSING-2026-11-16.md:84-97`

> **Rule 1: selection per cell per species.** Neutral envelope `E` = the largest `|delta|` among that cell's 100 neutral runs (50 seeds x `neutral_plus`, `neutral_minus`); this is primary. The 95th percentile of the 100 neutral `|delta|` (numpy linear interpolation) is reported as a **secondary**, less conservative envelope `E95` and labelled as such. A treatment seed is *outside* the envelope if `|delta| > E`. Let `n_out` be the number of treatment seeds outside `E` and `n_win` the larger of the numbers of outside seeds with `delta > 0` and with `delta < 0` (the winner is the genome of the larger group). Verdict:
> - **selection** if at least 40 of 50 treatment seeds are outside `E` and agree on the winner (`n_win >= 40`);
> - **takeover** if selection and the winner's median final share (over the seeds that are outside and agree) is at least 0.90;
> - **large but inconsistent** if `n_out >= 40` and `n_win < 40`;
> - **no selection detected** otherwise.
> Report `E`, `E95`, `n_out`, the winner split (outside seeds `+u` / `-u`), and the winner-side final-share distribution (min, median, max, over the agreeing seeds). The same counts are reported against `E95` as a secondary.
>
> **Rule 2: cause (the factorial question).** Food sensing is the **cause** of selection in a species, at a given `kappa`, if **selection or takeover** holds in the sensing-on cell and **no selection detected** holds in the matched sensing-off cell with the same `kappa`. Stated separately for `kappa = 0` and `kappa = 3`. Any other combination is reported as it is: *no cause shown* (sensing-on cell shows no selection), *selection also without sensing* (the off cell is not null), or *inconclusive* (a `large but inconsistent` cell). **Repulsion is a necessary condition** in a species if selection appears in the sensing-on cell at `kappa = 3` and not at `kappa = 0`.
>
> **Rule 3: distinctness (step 2 replicated at 50 seeds).** Per species and per `food_sense` value, treatment arm, end hybrid fraction, `kappa = 3` against `kappa = 0` of the same `food_sense`: **distinct** if the median hybrid fraction at `kappa = 3` is at most half the median at `kappa = 0` AND at least 40 of 50 seeds are below the matched `kappa = 0` seed; **no effect** if fewer than 30 of 50 are below; **partial** otherwise.
>
> **Rule 4: neutral-arm sanity.** In the neutral arms both lineages share `G8`, so food sensing and repulsion act identically on both; their share deltas should be centred on zero in every cell. Report, per cell and species, the mean and standard error of the 100 neutral deltas (and per arm). A cell whose neutral mean exceeds 2 SE from zero is **flagged as a harness asymmetry** (for example `+u` always placed first) and said plainly; this does not void the result but is reported next to it. With 12 cell-species combinations about 0.6 flags are expected by chance at the 2 SE level; this is stated in the results with the observed count.
>
> **Rule 5: conservation.** Max relative drift of `sum(body) + sum(food)` per run, expected about `1e-15`; the maximum over all 1,800 runs is reported, with the count of runs above `1e-12`. The mean fraction of body velocities at the soft bound per cell is reported (`sat_frac`).

### `docs/FOOD-SENSING-2x2-GPU-2026-11-16.md:3-11`

> GPU copy of the 2x2 in `docs/FOOD-SENSING-2026-11-16.md` (branch `vizier/food-sensing-brain-20261116`,
> design, rules and predictions fixed there before any run; this file adds no rule). Same engine
> (`Config.food_sense` input, `repulsion_kappa`), same species files, same seeds 1-50, same arms, same
> food parameters, 30,000 steps sampled every 100, `per_channel` transport, `food_sense` = 10 (B's pilot
> value, chosen by the fallback clause), run as `jax.vmap` batches of 150 by `scripts/gpu_batch.py` on
> Modal A100-80GB containers (`gpu/modal_campaign.py`, manifest `gpu/campaign_manifest.json --pilot 10`,
> launched 03:07 UTC). Worker B runs the identical design one process per run on InstaBox CPU boxes;
> B's result is the independent replication of everything below and was not available when this was
> written.

### `docs/SPECIES-SCAN-2026-11-16.md:39-62`

> Thresholds are the earlier rules scaled from 5 to 20 seeds (4 of 5 -> 16 of 20; 3 of 5 -> 12 of 20). `delta` = A's share averaged over the last 10% of samples minus A's share at step 0 (`delta_share_A` in the run JSON).
>
> **Rule 1: selection, per species x cell.** `E` = largest `|delta|` among that cell's 40 neutral runs (primary); the 95th percentile of those 40 `|delta|` (linear interpolation) is reported as a **secondary, labelled** variant and never replaces the primary. A treatment seed is outside `E` if `|delta| > E`; its winner is `+u` if `delta > 0`, else `-u`; its winner share is A's final share (`+u`) or 1 minus it (`-u`).
> - **selection**: at least 16 of 20 treatment seeds outside `E` and all agree on the winner;
> - **takeover**: selection and the median of those seeds' winner share is at least 0.90;
> - **large but inconsistent**: at least 16 outside `E` with disagreeing winners;
> - **no selection detected**: otherwise.
>
> **Rule 2: lineage distinctness, per species**, at the same `food_sense`: treatment arm, end hybrid fraction (`final.hybrid_frac`: mass with ancestry between 0.1 and 0.9), `kappa 3` vs `kappa 0`, seeds matched.
> - **distinct**: median hybrid fraction at `kappa 3` at most half that at `kappa 0`, AND at least 16 of 20 seeds strictly below their matched `kappa 0` seed;
> - **no effect**: fewer than 12 of 20 below;
> - **partial**: otherwise.
>
> **Rule 3: neutral-arm sanity, per cell and species.** Mean of the 40 neutral `delta` within 2 standard errors of zero. A species-cell outside is **flagged as harness asymmetry**: reported, not voiding. About 5% of tests are expected to flag by chance (120 tests), so flags are read as a count against that.
>
> **Rule 4: conservation.** Max relative drift of `sum(body) + sum(food)` per cell, expected about 1e-15.
>
> **Rule 5: species-level aggregate (new).**
> - For each cell: the number of species (of those with a complete cell) with `selection` or `takeover`, with an exact (Clopper-Pearson) binomial 95% interval.
> - Food sensing **changes the frequency of selection** at a given `kappa` if the count in the sensing-on cell exceeds the count in the sensing-off cell AND an exact two-sided McNemar test on the paired per-species outcomes (selection-or-takeover vs not) gives p < 0.05. (If off exceeds on, the test is still printed; it does not count as "changes" in the sense of the question, and is reported as a decrease.) Two cells, `kappa 0` and `kappa 3`, are two tests; each is read at 0.05 and the pair is reported without correction, with that stated in the results.
> - The distinctness frequency is treated the same way: number of species `distinct` at `kappa 3 vs 0`, exact interval, McNemar on `food_sense` 0 vs G.
> - Per cell, the distribution across species (min, quartiles, median, max) of the winner's median final share (per species, the larger lineage's median final share over its 20 treatment seeds; descriptive, defined whatever the verdict) and of the end hybrid fraction (per-species median over treatment seeds).
>
> Run `python scripts/species_scan_summary.py OUTROOT -o SUMMARY.md`; it computes all five rules over `OUTROOT/<id>/*_food1.json` and reports present vs expected runs (7,200). A cell is analysed only if all its 60 runs are present for that species; species missing from a cell are listed `incomplete` and dropped from that cell's denominators and from the pairs.

### `docs/SPECIES-SCAN-2026-11-16.md:88-88`

> The owner's Dish project defaults to **physics as renderer plus crossover topology**. That default changes only if selection appears when, and only when, the genome can touch food: i.e. a count of selection-or-takeover species that is higher with `food_sense = G` than with `0` by the Rule 5 test. If selection is absent or equally frequent in both, the default stands.

### `docs/HORIZON-300K-GPU-2026-11-16.md:29-45`

> 1. Takeover frequency per species and cell: treatment runs with winner share at the end >= 0.90, out
>    of 50, with an exact binomial 95% interval; neutral runs reaching 0.90 at any sample, out of 100
>    (expected 0). "Takeover occurs" if the treatment count exceeds the neutral count with a two-sided
>    exact test p < 0.05.
> 2. Selection at 300,000 steps by the standard rule: E = largest neutral |delta| among the cell's 100
>    neutral runs (primary) and the 95th percentile (secondary, labelled); selection if at least 40 of 50
>    treatment seeds are outside E with the same winner; takeover if selection and the winner's median
>    final share >= 0.90; large but inconsistent if 40+ outside with disagreeing winners.
> 3. Direction: the sign split of winners among treatment seeds outside E, per cell; the sensing-off and
>    sensing-on cells compared per species (same sign, opposite sign, or no consistent sign).
> 4. Share movement: per treatment run, |delta| at 30,000 vs 300,000 classified grows / saturated /
>    reverses (part A's classes); counts per cell against the neutral runs' counts.
> 5. Distinctness at 300,000 steps: end hybrid fraction per run; "holds" if the median over treatment
>    runs stays below half the matched 30,000-step median of the same runs' own series.
> 6. Neutral-arm sanity: mean neutral delta within 2 SE of zero per cell; a cell outside is flagged as
>    harness asymmetry and reported, not voiding.
> 7. Conservation: max relative drift of sum(body)+sum(food) per run (expect ~1e-14 at 300k steps).

### `docs/FINDINGS.md:111-118`

> Strict counts cannot exceed raw counts; the filter only removes.
>
> **Cause.** The strict count came from the recording run (900 steps, tracked
> every 6) and the raw count from the screening run (720 steps, tracked every
> 12). Two different runs presented as one comparison.
>
> **Fix.** Both figures now come from the same tracker, and the screening
> run's numbers appear on a separate labelled line.

### `docs/FINDINGS.md:234-239`

> Threshold is 0.35. Nothing about the world changed.
>
> This is a real limitation, not a bug to be papered over. Published verdicts
> come from the fine cadence, and every verdict carries its raw numbers so a
> borderline call reads as borderline. The proper fix is to track at native
> step resolution for the final verification pass, which is on the roadmap.

## Results against the criteria

**Scientific verdict:** the retained long-horizon data support OSCILLIS takeover in both
sensing conditions, with opposite winning directions. The species scan does not meet
the pre-registered test for a sensing-induced increase in selection frequency. It is
partial. Neither observation establishes that sensing is necessary for selection in general.

All fresh execution in this package was JSON summarisation, archive verification, log recovery,
and mock-runner testing. No simulation ran. The summary scripts and their thresholds were
not edited. Final-campaign results are the retained unique result files, not the sum of
machine run counts. Hardware qualifications below apply to every pooled verdict.

### Pilot and earlier factorial

The original CPU pilot selected gain 10 by fallback, not by a successful foraging gate.
At each gain 0.1, 0.3, 1, 3, and 10, the foraging criterion passed in 0 of 3 species;
all candidate runs met the saturation and conservation clauses. Source:
`campaign_gpu/evidence/food-sensing-cpu-pilot.md`, recovered unchanged from
`25b722a5:outputs/food_sensing_20261116/pilot/PILOT.md`.
The later GPU ladder also reports 0 of 3 at gains 30, 100, 300, and 1000
(`outputs/pilot2_gain_ladder/SUMMARY.md`). That is failure of the specified foraging
criterion, not proof that food has no neural or trajectory effect. The scan used 10,
not a gain selected by a successful pilot-2 gate.

The earlier factorial results below are from
`outputs/food_sensing_2x2_gpu/SUMMARY.md` and the unchanged CPU summary recovered from
`25b722a5:outputs/food_sensing_20261116/SUMMARY.md` into
`campaign_gpu/evidence/food-sensing-cpu-summary.md`.
These are historical results, not a newly rerun replication.

| species and hardware | fs0/k0 outside E (+u/-u) | fs0/k3 | fs10/k0 | fs10/k3 |
|---|---|---|---|---|
| OSCILLIS A100 | 7 (1/6) | 24 (7/17) | 28 (28/0) | 40 (40/0), selection |
| OSCILLIS rented CPU | 12 (4/8) | 26 (9/17) | 21 (21/0) | 35 (35/0), no selection detected |
| MITOSA A100 | 1 (1/0) | 9 (9/0) | 5 (4/1) | 19 (19/0) |
| MITOSA rented CPU | 0 (0/0) | 1 (1/0) | 8 (6/2) | 6 (6/0) |
| VAGRANT A100 | 19 (10/9) | 25 (24/1) | missing | missing |
| VAGRANT rented CPU | 16 (10/6) | 28 (26/2) | 12 (12/0) | 43 (0/43), selection |

Each measured entry has 50 treatment and 100 neutral runs. Unlabelled verdicts are
no selection detected. **OSCILLIS is 40 of 50 on GPU and 35 of 50 on CPU against a
threshold of 40. The GPU meets the primary rule; the CPU does not.** The CPU's secondary
E95 count of 40 does not rescue its primary verdict. These data neither establish
cross-hardware replication of the threshold verdict nor justify discarding the GPU result.
The causal rule passes for OSCILLIS at k3 on A100 and VAGRANT at k3 on CPU. Repulsion
is necessary in those measured species/hardware comparisons by the factorial rule.
It is not established as necessary for all genomes or all horizons. No factorial
cell meets the takeover criterion. The two VAGRANT sensing-on A100 cells remain absent.

Distinctness meets Rule 3 in all 5 measurable A100 comparisons and all 6 CPU comparisons.
Matched-seed counts for OSCILLIS fs0/fs10, MITOSA fs0/fs10, VAGRANT fs0/fs10 are
48/42, 50/44, 50/missing on A100 and 50/41, 50/48, 50/50 on CPU, each out of 50.
The respective median hybrid fractions and ratios are in the cited summaries.
CPU neutral sanity flags 0 of 12 combinations. A100 flags MITOSA fs0/k3; the GPU doc
says 11 of 12 unflagged, but only 10 cells were measured, so that denominator is
not a valid measured-cell count. Read it as 1 flag among 10 measured cells, not a
measurement of the 2 missing cells. Conservation maxima are 6.16e-15 on A100 and
6.76e-15 on CPU, with 0 CPU runs above 1e-12. The A100 maximum also lies below 1e-12.
CPU mean saturation fractions by F0K0/F0K3/F1K0/F1K3 are 8.78e-7, 1.00e-6,
1.17e-8, and 5.64e-9. A100 mean saturation fractions in the same cell order are
8.37e-7, 1.06e-6, 4.06e-9, and 1.37e-8
(`outputs/food_sensing_2x2_gpu/SUMMARY.md:68-72`). These diagnostics do not change the selection rule.

### Long horizon: all rules, full retained design

Source: `docs/HORIZON-300K-SUMMARY-2026-11-18.md`, regenerated from
`outputs/horizon300k_20261117`. All 900 unique runs are readable, with no duplicate
cell/arm/seed keys: 6 cells, each 50 treatment and 100 neutral runs. The following
tables are the exact script output before its per-run appendix.

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

#### Rule 2: selection at the final step (standard rule)

E = largest neutral |delta| over the cell's neutral runs (primary); E95 = 95th percentile (secondary, labelled). Selection: at least `need` treatment seeds outside E with the same winner sign; takeover: selection and the median final share of the winner over the outside seeds >= 0.90; large but inconsistent: `need`+ outside with both signs.

| species | cell | treat seeds | neutral runs | need | E (max) | outside E | +u / -u | winner median final share | verdict | E95 | outside E95 | verdict at E95 (secondary) | status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| OSCILLIS | fs0/k3 | 50 | 100 | 40 | 0.0761 | 50 | 0 / 50 | 0.933 | takeover | 0.0469 | 50 | takeover | full |
| OSCILLIS | fs10/k3 | 50 | 100 | 40 | 0.3578 | 50 | 50 / 0 | 0.977 | takeover | 0.1245 | 50 | takeover | full |
| MITOSA | fs0/k3 | 50 | 100 | 40 | 0.1128 | 12 | 6 / 6 | 0.636 | no selection detected | 0.0661 | 25 | no selection detected | full |
| MITOSA | fs10/k3 | 50 | 100 | 40 | 0.1516 | 20 | 8 / 12 | 0.858 | no selection detected | 0.0980 | 27 | no selection detected | full |
| VAGRANT | fs0/k3 | 50 | 100 | 40 | 0.3324 | 14 | 12 / 2 | 1.000 | no selection detected | 0.0667 | 37 | no selection detected | full |
| VAGRANT | fs10/k3 | 50 | 100 | 40 | 0.1236 | 49 | 3 / 46 | 0.997 | large but inconsistent | 0.0461 | 50 | large but inconsistent | full |

#### Rule 3: direction

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

#### Rule 4: share movement, |delta| at 30,000 vs final step

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

#### Rule 5: distinctness at the final step

Per treatment run: end hybrid fraction vs the same run's own hybrid fraction at step 30,000. Verdict (as specified): holds if the median end hybrid fraction over treatment runs is at most half the median of the same runs' 30,000-step values. Secondary (the harness's per-run rule, campaign_harness_summary.py (c)): runs with h_end <= max(0.10, h30 + 0.05).

| species | cell | treat n | median h30 | median h_end | ratio | holds (<= 1/2) | runs holding (harness rule) | status |
|---|---|---|---|---|---|---|---|---|
| OSCILLIS | fs0/k3 | 50 | 0.064 | 0.000 | 0.00 | holds | 46 of 50 | full |
| OSCILLIS | fs10/k3 | 50 | 0.000 | 0.000 | 0.00 | holds | 50 of 50 | full |
| MITOSA | fs0/k3 | 50 | 0.000 | 0.000 | 0.02 | holds | 44 of 50 | full |
| MITOSA | fs10/k3 | 50 | 0.005 | 0.103 | 21.87 | does not hold | 25 of 50 | full |
| VAGRANT | fs0/k3 | 50 | 0.000 | 0.000 | 0.01 | holds | 50 of 50 | full |
| VAGRANT | fs10/k3 | 50 | 0.000 | 0.000 | 0.00 | holds | 50 of 50 | full |

#### Rule 6: neutral-arm sanity

Mean neutral delta within 2 SE of zero per cell; outside is flagged as harness asymmetry (reported, not voiding).

| species | cell | neutral runs | mean delta | SE | mean/SE | flag | status |
|---|---|---|---|---|---|---|---|
| OSCILLIS | fs0/k3 | 100 | +0.0003 | 0.0020 | +0.15 | ok | full |
| OSCILLIS | fs10/k3 | 100 | -0.0023 | 0.0062 | -0.37 | ok | full |
| MITOSA | fs0/k3 | 100 | -0.0006 | 0.0027 | -0.23 | ok | full |
| MITOSA | fs10/k3 | 100 | -0.0041 | 0.0042 | -0.98 | ok | full |
| VAGRANT | fs0/k3 | 100 | +0.0063 | 0.0048 | +1.32 | ok | full |
| VAGRANT | fs10/k3 | 100 | -0.0001 | 0.0023 | -0.03 | ok | full |

#### Rule 7: conservation (max relative drift of sum(body)+sum(food))

| species | cell | runs | max drift | status |
|---|---|---|---|---|
| OSCILLIS | fs0/k3 | 150 | 2.65e-14 | full |
| OSCILLIS | fs10/k3 | 150 | 2.57e-14 | full |
| MITOSA | fs0/k3 | 150 | 4.18e-14 | full |
| MITOSA | fs10/k3 | 150 | 2.17e-14 | full |
| VAGRANT | fs0/k3 | 150 | 3.82e-14 | full |
| VAGRANT | fs10/k3 | 150 | 1.43e-14 | full |

Max over all 900 runs: **4.18e-14**.


Rule 1's takeover-frequency test and Rule 2's consistent-selection test answer different
questions. In particular, VAGRANT fs10 has 48 of 50 end-share takeovers but both winner
signs among its 49 outside-envelope seeds, so it is large but inconsistent under Rule 2.
MITOSA fs10 has 5 of 50 takeovers and passes the frequency test, yet does not meet the
40-seed selection bar. The sensing-off OSCILLIS and VAGRANT takeover counts, 38 and 14
of 50, exceed the pre-run prediction of at least a fifth; their neutral counts are
0 of 100. Only OSCILLIS has consistent selection, and sensing reverses its sign.
Conservation is a measured float64 diagnostic, not an exact-real arithmetic proof.
The runners' `share_A_end` field is the mean over the final 10% of samples, not the
last instantaneous sample (`scripts/gpu_batch.py:224-226`); the unchanged summary uses
that field for its reported final-share counts. Neutral peak counts instead read the
sampled series. These are the retained instruments, not a new endpoint definition.
The distinctness comparison uses each long run's own 30k series, not a separate
short-run dataset. Rounded zeroes in the table are not claims of exact zero.

### Species scan: all rules, partial retained design

Source: `docs/SPECIES-SCAN-SUMMARY-2026-11-18.md`, regenerated from
`outputs/species_scan_20261117`. There are 7,173 design runs, not 7,174. The extra
recursive file counted in the collector is a 300-step smoke run under `smoke/smoke_fs0/`.
It is not a scan run. Every complete cell has 20 seeds in each arm. VAGRANT fs0/k3
has only 33 of 60 runs, 11 per arm. It is incomplete and excluded, never judged with
a lower selection threshold. All missing pairs are in `campaign_gpu/evidence/audit.json`.

| criterion | exact result | decision |
|---|---|---|
| Rule 1 and Rule 5, fs0/k0 | selection 4/30; takeover 0/30; large but inconsistent 3/30 | selection exists without sensing |
| Rule 1 and Rule 5, fs0/k3 | selection 5/29; takeover 0/29; large but inconsistent 2/29 | partial, VAGRANT excluded |
| Rule 1 and Rule 5, fs10/k0 | selection 11/30; takeover 0/30; large but inconsistent 7/30 | not a takeover result |
| Rule 1 and Rule 5, fs10/k3 | selection 12/30; takeover 0/30; large but inconsistent 6/30 | not a takeover result |
| Rule 5, sensing frequency at k0 | 30 pairs; on-only 11, off-only 4; p=0.1185 | no change by the rule |
| Rule 5, sensing frequency at k3 | 29 pairs; on-only 11, off-only 4; p=0.1185 | no change by the rule; partial |
| Rule 2, distinctness fs0 | distinct 18/29; partial 4/29; no effect 7/29 | common, not universal |
| Rule 2, distinctness fs10 | distinct 17/30; partial 5/30; no effect 8/30 | common, not universal |
| Rule 5, distinctness frequency | 29 pairs; on-only 3, off-only 5; off 18, on 16; p=0.7266 | no change by the rule |
| Rule 3, neutral sanity | 5 flags among 119 complete species-cells | reported, not voiding |
| Rule 4, conservation k0/fs0, k3/fs0, k0/fs10, k3/fs10 | maxima 6.75e-15, 6.75e-15, 6.61e-15, 6.76e-15 | small measured drift |

The script reports exact binomial intervals and the full per-species rule decisions,
matched distinctness counts, and winner-share/hybrid distributions. Those tables are
part of this report by reference, not omitted measurements. Neutral flags are GLOBULA
at k0/fs0, k3/fs0 and k0/fs10; HELIX at k0/fs0; PULSARA at k3/fs10.
The two aggregate selection tests use 0.05 without multiplicity correction, as planned.
Neither passes even before correction. A non-significant result does not establish equal
frequencies. Sensing-on counts are numerically higher. The pre-registered Dish default
therefore stands under this decision rule, with missing-data and hardware caveats.

Pre-registered subgroups do not replace the primary result. Excluding the five
cadence-dependent species gives selection counts 3/25, 5/24, 8/25, 8/25 in cell order
k0/fs0, k3/fs0, k0/fs10, k3/fs10, with sensing p=0.2266 and 0.5488.
The original three give 0/3, 0/2, 0/3, 0/3, with p=1 in both tests.
Distinctness paired tests give off/on 17/13 over 24 pairs (p=0.2188) in the
cadence-excluded subgroup and 2/2 over 2 pairs (p=1) in the original three.
A random food coupling and the fixed lineage axis are the tested mechanism, not all
possible food-sensing policies. No new phototaxis or division claim follows from a
lineage-share experiment. The sampling and detector warnings in `FINDINGS.md` still apply.

## Hardware and provenance

`campaign_gpu/evidence/run-hardware.tsv` labels every retained design run used above
with its hardware, source and SHA-256: 9,573 rows covering the final horizon, final
scan and retained A100 factorial. `hardware-cells.md` lists every cell and exact
hardware counts; its table is reproduced below. The historical CPU factorial is a
separate 1,800-run rented-CPU experiment at `25b722a5`, not another source of final
horizon or scan files. Its recovered summary is historical evidence, not a fresh
per-run audit here. The original pilot used rented CPU; pilot 2 used A100 as recorded
in `docs/GPU-PILOT2-GAIN-LADDER-2026-11-16.md`.

| retained experiment | rented CPU | A100 | L4 |
|---|---|---|---|
| horizon300k_20261117 | 128 | 0 | 772 |
| species_scan_20261117 | 3,886 | 0 | 3,287 |
| food_sensing_2x2_gpu | 0 | 1,500 | 0 |

CPU assignment requires exact `wall_seconds` equality with that run's retained stdout
JSON, not merely a seed allocation or a successful scheduler line. L4 assignment
requires an exact result SHA-256 match inside a checksum-verified fleet archive and
membership in a planned L4 shard. Each L4 row identifies its machine log. This catches
two XENIA seed-5 neutral results whose retained files came from L4 despite CPU completion
logs. The CPU source includes both Vultr and InstaBox CPU; their scheduler logs and the
execution notes in the design docs identify those venues. The labels are hardware
categories, not an assertion that all rented CPUs are identical.

All 6 horizon cells and 119 of the 120 scan cells mix rented CPU and L4: 125 mixed
cells. The incomplete VAGRANT scan fs0/k3 cell is CPU-only. No retained cell mixes A100
with L4 or CPU. Pooling therefore answers a mixed-hardware campaign question, not a
clean L4 replication. Common seed sets and a common engine do not remove trajectory
or backend confounding. Do not call pooled sensing comparisons an isolated hardware-controlled
causal replication or treat CPU and GPU twins as bit-identical.

The explicit earlier cross-check, `docs/FOOD-SENSING-2x2-GPU-2026-11-16.md:76-79`, says:

> Median per-run |difference| between a GPU run and its CPU twin: 0.002 to 0.016. End hybrid fraction
> medians agree except OSCILLIS k3 (CPU 0.313, GPU 0.065; both "distinct"). **0 of 90 GPU runs
> reproduce their CPU twin to 1e-6**: the trajectories are chaotic and the hardware differs, as
> expected; the distributions and every verdict agree.

### Every retained cell, including every mixed cell

| cell | rented CPU | A100 | L4 | mixed |
|---|---|---|---|---|
| outputs/food_sensing_2x2_gpu/SPECIES_001_OSCILLIS_fs0_k0_per_channel | 0 | 150 | 0 | no |
| outputs/food_sensing_2x2_gpu/SPECIES_001_OSCILLIS_fs0_k3_per_channel | 0 | 150 | 0 | no |
| outputs/food_sensing_2x2_gpu/SPECIES_001_OSCILLIS_fs10_k0_per_channel | 0 | 150 | 0 | no |
| outputs/food_sensing_2x2_gpu/SPECIES_001_OSCILLIS_fs10_k3_per_channel | 0 | 150 | 0 | no |
| outputs/food_sensing_2x2_gpu/SPECIES_002_MITOSA_fs0_k0_per_channel | 0 | 150 | 0 | no |
| outputs/food_sensing_2x2_gpu/SPECIES_002_MITOSA_fs0_k3_per_channel | 0 | 150 | 0 | no |
| outputs/food_sensing_2x2_gpu/SPECIES_002_MITOSA_fs10_k0_per_channel | 0 | 150 | 0 | no |
| outputs/food_sensing_2x2_gpu/SPECIES_002_MITOSA_fs10_k3_per_channel | 0 | 150 | 0 | no |
| outputs/food_sensing_2x2_gpu/SPECIES_003_VAGRANT_fs0_k0_per_channel | 0 | 150 | 0 | no |
| outputs/food_sensing_2x2_gpu/SPECIES_003_VAGRANT_fs0_k3_per_channel | 0 | 150 | 0 | no |
| outputs/horizon300k_20261117/SPECIES_001_OSCILLIS_fs0_k3_per_channel | 23 | 0 | 127 | yes |
| outputs/horizon300k_20261117/SPECIES_001_OSCILLIS_fs10_k3_per_channel | 21 | 0 | 129 | yes |
| outputs/horizon300k_20261117/SPECIES_002_MITOSA_fs0_k3_per_channel | 21 | 0 | 129 | yes |
| outputs/horizon300k_20261117/SPECIES_002_MITOSA_fs10_k3_per_channel | 21 | 0 | 129 | yes |
| outputs/horizon300k_20261117/SPECIES_003_VAGRANT_fs0_k3_per_channel | 21 | 0 | 129 | yes |
| outputs/horizon300k_20261117/SPECIES_003_VAGRANT_fs10_k3_per_channel | 21 | 0 | 129 | yes |
| outputs/species_scan_20261117/SPECIES_001_OSCILLIS_fs0_k0_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_001_OSCILLIS_fs0_k3_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_001_OSCILLIS_fs10_k0_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_001_OSCILLIS_fs10_k3_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_002_MITOSA_fs0_k0_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_002_MITOSA_fs0_k3_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_002_MITOSA_fs10_k0_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_002_MITOSA_fs10_k3_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_003_VAGRANT_fs0_k0_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_003_VAGRANT_fs0_k3_per_channel | 33 | 0 | 0 | no |
| outputs/species_scan_20261117/SPECIES_003_VAGRANT_fs10_k0_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_003_VAGRANT_fs10_k3_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_004_CORONA_fs0_k0_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_004_CORONA_fs0_k3_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_004_CORONA_fs10_k0_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_004_CORONA_fs10_k3_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_005_SPLITTER_fs0_k0_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_005_SPLITTER_fs0_k3_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_005_SPLITTER_fs10_k0_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_005_SPLITTER_fs10_k3_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_006_DRIFTER_fs0_k0_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_006_DRIFTER_fs0_k3_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_006_DRIFTER_fs10_k0_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_006_DRIFTER_fs10_k3_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_007_NUCLEUS_fs0_k0_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_007_NUCLEUS_fs0_k3_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_007_NUCLEUS_fs10_k0_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_007_NUCLEUS_fs10_k3_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_008_TENDRIL_fs0_k0_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_008_TENDRIL_fs0_k3_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_008_TENDRIL_fs10_k0_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_008_TENDRIL_fs10_k3_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_009_ARBORIS_fs0_k0_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_009_ARBORIS_fs0_k3_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_009_ARBORIS_fs10_k0_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_009_ARBORIS_fs10_k3_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_010_CILIATA_fs0_k0_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_010_CILIATA_fs0_k3_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_010_CILIATA_fs10_k0_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_010_CILIATA_fs10_k3_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_011_FLAGELLA_fs0_k0_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_011_FLAGELLA_fs0_k3_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_011_FLAGELLA_fs10_k0_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_011_FLAGELLA_fs10_k3_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_012_GLOBULA_fs0_k0_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_012_GLOBULA_fs0_k3_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_012_GLOBULA_fs10_k0_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_012_GLOBULA_fs10_k3_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_013_HELIX_fs0_k0_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_013_HELIX_fs0_k3_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_013_HELIX_fs10_k0_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_013_HELIX_fs10_k3_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_014_LUMINA_fs0_k0_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_014_LUMINA_fs0_k3_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_014_LUMINA_fs10_k0_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_014_LUMINA_fs10_k3_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_015_MEDUSA_fs0_k0_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_015_MEDUSA_fs0_k3_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_015_MEDUSA_fs10_k0_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_015_MEDUSA_fs10_k3_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_016_NODULUS_fs0_k0_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_016_NODULUS_fs0_k3_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_016_NODULUS_fs10_k0_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_016_NODULUS_fs10_k3_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_017_ORBITA_fs0_k0_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_017_ORBITA_fs0_k3_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_017_ORBITA_fs10_k0_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_017_ORBITA_fs10_k3_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_018_PULSARA_fs0_k0_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_018_PULSARA_fs0_k3_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_018_PULSARA_fs10_k0_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_018_PULSARA_fs10_k3_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_019_QUASARIA_fs0_k0_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_019_QUASARIA_fs0_k3_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_019_QUASARIA_fs10_k0_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_019_QUASARIA_fs10_k3_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_020_RADIATA_fs0_k0_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_020_RADIATA_fs0_k3_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_020_RADIATA_fs10_k0_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_020_RADIATA_fs10_k3_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_021_SPIRALIS_fs0_k0_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_021_SPIRALIS_fs0_k3_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_021_SPIRALIS_fs10_k0_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_021_SPIRALIS_fs10_k3_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_022_TORQUATA_fs0_k0_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_022_TORQUATA_fs0_k3_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_022_TORQUATA_fs10_k0_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_022_TORQUATA_fs10_k3_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_023_UNDULA_fs0_k0_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_023_UNDULA_fs0_k3_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_023_UNDULA_fs10_k0_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_023_UNDULA_fs10_k3_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_024_VESICA_fs0_k0_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_024_VESICA_fs0_k3_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_024_VESICA_fs10_k0_per_channel | 33 | 0 | 27 | yes |
| outputs/species_scan_20261117/SPECIES_024_VESICA_fs10_k3_per_channel | 30 | 0 | 30 | yes |
| outputs/species_scan_20261117/SPECIES_025_XENIA_fs0_k0_per_channel | 31 | 0 | 29 | yes |
| outputs/species_scan_20261117/SPECIES_025_XENIA_fs0_k3_per_channel | 30 | 0 | 30 | yes |
| outputs/species_scan_20261117/SPECIES_025_XENIA_fs10_k0_per_channel | 30 | 0 | 30 | yes |
| outputs/species_scan_20261117/SPECIES_025_XENIA_fs10_k3_per_channel | 30 | 0 | 30 | yes |
| outputs/species_scan_20261117/SPECIES_026_YGGRA_fs0_k0_per_channel | 30 | 0 | 30 | yes |
| outputs/species_scan_20261117/SPECIES_026_YGGRA_fs0_k3_per_channel | 30 | 0 | 30 | yes |
| outputs/species_scan_20261117/SPECIES_026_YGGRA_fs10_k0_per_channel | 30 | 0 | 30 | yes |
| outputs/species_scan_20261117/SPECIES_026_YGGRA_fs10_k3_per_channel | 30 | 0 | 30 | yes |
| outputs/species_scan_20261117/SPECIES_027_ZONATA_fs0_k0_per_channel | 30 | 0 | 30 | yes |
| outputs/species_scan_20261117/SPECIES_027_ZONATA_fs0_k3_per_channel | 30 | 0 | 30 | yes |
| outputs/species_scan_20261117/SPECIES_027_ZONATA_fs10_k0_per_channel | 30 | 0 | 30 | yes |
| outputs/species_scan_20261117/SPECIES_027_ZONATA_fs10_k3_per_channel | 30 | 0 | 30 | yes |
| outputs/species_scan_20261117/SPECIES_028_ANTENNA_fs0_k0_per_channel | 30 | 0 | 30 | yes |
| outputs/species_scan_20261117/SPECIES_028_ANTENNA_fs0_k3_per_channel | 30 | 0 | 30 | yes |
| outputs/species_scan_20261117/SPECIES_028_ANTENNA_fs10_k0_per_channel | 30 | 0 | 30 | yes |
| outputs/species_scan_20261117/SPECIES_028_ANTENNA_fs10_k3_per_channel | 30 | 0 | 30 | yes |
| outputs/species_scan_20261117/SPECIES_029_BIFIDA_fs0_k0_per_channel | 30 | 0 | 30 | yes |
| outputs/species_scan_20261117/SPECIES_029_BIFIDA_fs0_k3_per_channel | 30 | 0 | 30 | yes |
| outputs/species_scan_20261117/SPECIES_029_BIFIDA_fs10_k0_per_channel | 30 | 0 | 30 | yes |
| outputs/species_scan_20261117/SPECIES_029_BIFIDA_fs10_k3_per_channel | 30 | 0 | 30 | yes |
| outputs/species_scan_20261117/SPECIES_030_CATENA_fs0_k0_per_channel | 30 | 0 | 30 | yes |
| outputs/species_scan_20261117/SPECIES_030_CATENA_fs0_k3_per_channel | 30 | 0 | 30 | yes |
| outputs/species_scan_20261117/SPECIES_030_CATENA_fs10_k0_per_channel | 30 | 0 | 30 | yes |
| outputs/species_scan_20261117/SPECIES_030_CATENA_fs10_k3_per_channel | 30 | 0 | 30 | yes |

## Deviations and missing work

- Venue changed from the pre-run Modal A100 plan to rented CPU and then an InstaBox L4
  tail. The design docs' CPU execution notes are not descriptions of the final hardware
  mix. Use the per-run table above instead.
- The first fleet launch is recorded as 2026-11-18T00:49:31Z in
  `campaign_gpu/gpu_boxes.json`. The work-package brief records a corrected relaunch at
  01:07 UTC. Per-machine logs establish restart execution, for example
  `outputs/gpu_machine_logs/flux-l4-20/campaign.log` starts the old shard at 00:55:14Z
  and the corrected shard at 01:13:40Z. The 01:07 control-action time is supplied context,
  not an independently recovered launch receipt. The typo was MITOSIS for MITOSA;
  `outputs/logs/SPECIES_002_MITOSIS_fs0_k3_per_channel.log` preserves the missing-genome
  traceback. The misspelled species is not a new species or a completed result.
- Duplicate batch IDs and duplicate executions are different faults. In corrected
  `campaign_gpu/shards/box20.tsv:1,3`, the horizon VAGRANT fs0/k3 batch and scan VAGRANT
  fs0/k3 batch have the same id but different output trees. Old `run_shard.sh` searched
  `DONE <id> runs=` only. The horizon DONE at 03:34:51Z in that box's log therefore
  suppressed the scan batch, while the box still ended ALL_DONE. Missing seeds are
  7, 9, 11, 13, 15, 17, 18, 19, 20 in all 3 arms: exactly 27 missing design runs.
- Checksum-verified archives contain 4,170 JSON run members but only 4,062 unique
  output paths. There are 108 duplicated L4 output paths, 27 each in CORONA fs10/k0
  (boxes 09 and 11), SPLITTER fs0/k0 (11 and 13), SPLITTER fs0/k3 (12 and 14), and
  SPLITTER fs10/k0 (13 and 15). The final shards do not explain every historical
  duplicate; the restart history and per-machine logs must be kept, not inferred away.
  `campaign_gpu/evidence/l4-result-hashes.tsv` records every machine copy. There are
  also 3 L4 archive paths whose retained result is CPU: OSCILLIS horizon fs0/k3 seed 8
  treat and neutral_plus, and XENIA scan fs0/k0 seed 5 treat. Conversely, the 2 XENIA
  seed-5 neutrals retain L4 results despite CPU stdout. These are duplicate computations,
  not additional independent seeds. All 111 alternate archived JSON copies that differ
  from retained results are preserved under `outputs/gpu_machine_logs/*/alternate_results/`.
- The supplied merged-log copy has 123 files, including only one `outputs/campaign.log`;
  identical log names on different machines had been merged or overwritten. It is
  unpacked unchanged as requested. In addition, all 20 original pulled tar archives
  were checked against the hashes in `gpu_boxes.json`, and 188 distinct machine log
  files were recovered under `outputs/gpu_machine_logs/`. This retains the actual
  machine histories rather than treating the merged log as a fleet-wide trace.
- The collector's final 7,174 count includes the smoke JSON. The summary's 7,173 count
  is the design count. ALL_DONE in all 20 boxes does not certify design coverage.

## Cost and timing

Source: `campaign_gpu/gpu_boxes.json` and the retained
`campaign_gpu/evidence/gpu_collector.log`. All 20 boxes have `terminal=ALL_DONE`,
`status=pulled`, a SHA-256 receipt and `deleted=true`. Archive checks were replayed here;
provider deletion was reported by the parent and was not independently queried here.
The final box deletion is 2026-11-18T07:32:14Z; the final collector line is 07:32:36Z.
First launch to last deletion is 6 h 42 min 43 s. Billing exposure starts at creation,
not at launch: summed creation-to-deletion time is 115.387778 GPU-hours at
0.765 USD/GPU-hour, giving 88.27165 USD, rounded to 88.27 USD, below the 98 USD cap.
This is a collector estimate using recorded timestamps and a rate, not an invoice.
The collector initially printed a 95 USD cap, changing to 98 USD by 01:42:01Z.
Earlier CPU, A100, pilot and failed Modal expenditure is not included in that 88.27 USD;
it must not be presented as the cost of the entire research program.
The earlier cost notes remain in their design docs and are not reconciled to provider
invoices by this package. No money was spent on this write-up.

`wall_seconds` is not comparable wall-clock latency across runners: GPU values are
batch loop time divided by batch size, excluding compilation
(`scripts/gpu_batch.py:22-25,240`); CPU values are individual run wall time.
Horizon summary reports minimum/median/maximum 221/375/19,902 seconds over its 900
records. Do not multiply these mixed values into an additional billed-cost estimate.

## Reproduction

Run from this branch's repository root. These commands read results and do not simulate:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python scripts/horizon300k_summary.py \
  outputs/horizon300k_20261117 -o docs/HORIZON-300K-SUMMARY-2026-11-18.md
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python scripts/species_scan_summary.py \
  outputs/species_scan_20261117 -o docs/SPECIES-SCAN-SUMMARY-2026-11-18.md
python scripts/gpu_campaign_audit.py
python scripts/scan_campaign_logs.py
python scripts/test_run_shard.py
bash -n scripts/run_shard.sh
```

`recover_gpu_logs.py PULLED_ARCHIVE_DIRECTORY` optionally replays original archive
checks and log/alternate-result recovery when the retained tar files are available.
The committed manifests allow routine audit without those machine-local archives.
The CPU historical summaries were recovered with `git show 25b722a5:<original path>`;
they were not regenerated from simulations here. Sources and exact validation receipts
are retained in `campaign_gpu/evidence/verification.json`.

The runner fix hashes id, output tree, expected count and full argument string. It
uses fixed-string DONE lookup and separate per-batch log names. Different output trees
and seed ranges no longer collide. Old id-only markers are deliberately not trusted;
`gpu_batch.py` still skips existing result JSON. The mock integration test covers old
marker rejection, identical ids across two experiments, different batches in one output
tree, exact resume, unique logs and failure retry. It never imports or runs JAX.

The prepared `campaign_gpu/shards/missing-vagrant-fs0-k3.tsv` requests exactly the
27 missing pairs and no completed pair. With code, species files and the existing
output tree placed at the standard `/data/fl` layout on a future authorised L4,
finishing is one command:

```sh
FL=/data/fl bash /data/fl/code/scripts/run_shard.sh \
  /data/fl/code/campaign_gpu/shards/missing-vagrant-fs0-k3.tsv
```

That is a future simulation command, not executed by this package. Expected count 27
is the number in this shard, not the eventual 60-file cell size. After collection,
rerun both summary/audit scripts and verify all 60 design keys, not only ALL_DONE.

## Open items

1. Authorise and execute the prepared 27-run completion only as a separate package;
   then regenerate the scan report with complete denominators. Nothing was launched here.
2. For hardware-specific conclusions, use the committed per-run labels to pre-register
   a hardware-stratified check or an independent uniform-hardware replication. Do not
   silently recalculate a new primary threshold after seeing these results.
3. Recover a control-action launch receipt if the precise 01:07 relaunch time matters.
   Reconcile the earlier CPU/A100 charges against invoices if a whole-program total
   is needed. Neither is required to read the present numerical results.
4. The earlier missing VAGRANT A100 sensing cells remain an open replication gap, not
   something filled by the mixed CPU/L4 scan or the longer horizon.
5. The regression test verifies the repaired runner's bookkeeping, not the historical
   completeness of ALL_DONE or the simulation engine. No independent engine replay,
   independent statistical implementation, provider invoice audit or new GPU/CPU
   numerical-equivalence test was performed.

Secret scanning covered the merged logs, per-machine logs, alternate JSON results and
collector log. `campaign_gpu/evidence/secret-scan.json` lists file hashes, patterns and
zero detected credential matches. This is a pattern scan, not a proof against arbitrary
secret formats. Operational machine IDs, paths, IP addresses and checksums are retained.
