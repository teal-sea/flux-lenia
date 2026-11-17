# Food-sensing 2x2 on GPU: replicate of worker B's design at 50 seeds (2026-11-16)

GPU copy of the 2x2 in `docs/FOOD-SENSING-2026-11-16.md` (branch `vizier/food-sensing-brain-20261116`,
design, rules and predictions fixed there before any run; this file adds no rule). Same engine
(`Config.food_sense` input, `repulsion_kappa`), same species files, same seeds 1-50, same arms, same
food parameters, 30,000 steps sampled every 100, `per_channel` transport, `food_sense` = 10 (B's pilot
value, chosen by the fallback clause), run as `jax.vmap` batches of 150 by `scripts/gpu_batch.py` on
Modal A100-80GB containers (`gpu/modal_campaign.py`, manifest `gpu/campaign_manifest.json --pilot 10`,
launched 03:07 UTC). Worker B runs the identical design one process per run on InstaBox CPU boxes;
B's result is the independent replication of everything below and was not available when this was
written.

## What ran

12 cells (3 species x food_sense {0, 10} x kappa {0, 3}) of 150 runs each. **10 cells completed**
(1,500 runs). The two VAGRANT sensing-on cells (fs10 k0, fs10 k3) were lost when Modal disabled the
workspace at 04:05 UTC (`ConflictError: workspace ... is disabled`; about $30-35 of spend, which
matches the Starter plan's included compute running out). Per-run JSON (same schema as
`scripts/food_selection.py`) in `outputs/food_sensing_2x2_gpu/<SPECIES>_fs<v>_k<kappa>_per_channel/`;
frames stayed on the Modal Volume `flux-lenia-gpu-out` (26 MB per run, not pulled). Verdicts from B's
`scripts/food_sensing_summary.py main outputs/food_sensing_2x2_gpu` in
`outputs/food_sensing_2x2_gpu/SUMMARY.md`.

The lineage axis `u` is fixed for every seed (`lineage_axis_seed` 20261103, lineage A = +u, B = -u),
so "+u wins" names one genome direction, not a placement.

## Results

**Rule 1, selection** (E = largest neutral |delta| among the cell's 100 neutral runs; selection needs
40 of 50 treatment seeds outside E with the same winner; takeover needs the winner's median final
share >= 0.90):

| species | cell | E | seeds outside E | winners +u / -u | winner share min / median / max | verdict |
|---|---|---|---|---|---|---|
| OSCILLIS | fs0 k0 | 0.0381 | 7 of 50 | 1 / 6 | 0.538 / 0.546 / 0.574 | no selection detected |
| OSCILLIS | fs0 k3 | 0.0326 | 24 of 50 | 7 / 17 | 0.534 / 0.587 / 0.655 | no selection detected |
| OSCILLIS | fs10 k0 | 0.0331 | 28 of 50 | 28 / 0 | 0.534 / 0.550 / 0.591 | no selection detected |
| **OSCILLIS** | **fs10 k3** | 0.0342 | **40 of 50** | **40 / 0** | 0.538 / **0.568** / 0.619 | **selection** |
| MITOSA | fs0 k0 | 0.0641 | 1 of 50 | 1 / 0 | 0.588 | no selection detected |
| MITOSA | fs0 k3 | 0.0763 | 9 of 50 | 9 / 0 | 0.582 / 0.600 / 0.651 | no selection detected |
| MITOSA | fs10 k0 | 0.0597 | 5 of 50 | 4 / 1 | 0.555 / 0.569 / 0.600 | no selection detected |
| MITOSA | fs10 k3 | 0.0523 | 19 of 50 | 19 / 0 | 0.555 / 0.576 / 0.635 | no selection detected |
| VAGRANT | fs0 k0 | 0.0393 | 19 of 50 | 10 / 9 | 0.543 / 0.596 / 0.741 | no selection detected |
| VAGRANT | fs0 k3 | 0.0388 | 25 of 50 | 24 / 1 | 0.537 / 0.574 / 0.766 | no selection detected |
| VAGRANT | fs10 k0, fs10 k3 | lost | | | | not measured |

Secondary envelope (95th percentile of neutral |delta|) gives the same verdicts; OSCILLIS fs10 k3 is
44 of 50 outside, 43 / 1.

**Rule 2, cause.** OSCILLIS at kappa 3: sensing off = no selection, sensing on = selection: **cause
shown**. OSCILLIS at kappa 0: no selection with sensing on (28 of 50, all +u, under the 40 bar), so by
the rule repulsion is necessary for this species. MITOSA: no selection in any cell (fs10 k3 is 19 of
50, all +u, under the bar). VAGRANT: not measurable (sensing cells lost).

**Rule 3, distinctness** (kappa 3 vs kappa 0 at the same food_sense, treatment arm, end hybrid
fraction): OSCILLIS fs0 1.000 -> 0.021 (48 of 50 seeds below matched control), fs10 0.434 -> 0.000
(42 of 50); MITOSA fs0 1.000 -> 0.000 (50 of 50), fs10 0.325 -> 0.003 (44 of 50); VAGRANT fs0
0.743 -> 0.000 (50 of 50). **Distinct in every measurable species and cell.**

**Rule 4, neutral-arm sanity:** mean neutral delta within 2 SE of zero in 11 of 12 cell-species
combinations; the one flag is MITOSA fs0 k3 at -2.19 SE (0.6 flags expected by chance at 2 SE).
The OSCILLIS fs10 k3 cell that shows selection has neutral mean +0.0005 (0.40 SE): no placement
asymmetry behind the +u wins.

**Rule 5, conservation and velocity bound:** max relative drift of sum(body)+sum(food) over all
1,500 runs 6.16e-15; largest single-sample saturation fraction 1.37e-3 (fs0 cells), 1.33e-4 (fs10).

## Cross-check against the CPU runs (same seeds 1-5, food_sense 0)

CPU: `outputs/food_on_exact_20261110` (kappa 0) and `outputs/conditional_blending_20261115` (kappa 3),
one process per run on citadel/InstaBox. GPU: this experiment's fs0 cells, seeds 1-5. Final share of
lineage A, median (min-max), treat arm: OSCILLIS k0 CPU 0.499 (0.481-0.514) vs GPU 0.507
(0.472-0.510); MITOSA k0 0.512 (0.484-0.546) vs 0.517 (0.488-0.556); VAGRANT k0 0.500 (0.464-0.662)
vs 0.499 (0.444-0.594); OSCILLIS k3 0.499 (0.484-0.571) vs 0.514 (0.485-0.568); MITOSA k3 0.526
(0.479-0.590) vs 0.530 (0.485-0.578); VAGRANT k3 0.551 (0.510-0.695) vs 0.542 (0.513-0.704).
Median per-run |difference| between a GPU run and its CPU twin: 0.002 to 0.016. End hybrid fraction
medians agree except OSCILLIS k3 (CPU 0.313, GPU 0.065; both "distinct"). **0 of 90 GPU runs
reproduce their CPU twin to 1e-6**: the trajectories are chaotic and the hardware differs, as
expected; the distributions and every verdict agree.

## Reading

With the food input the lineages do not eat measurably more at the population level (B's pilot,
GPU pilot 2), yet in OSCILLIS the +u lineage gains a small, consistent edge in 40 of 50 seeds, only
when repulsion keeps the lineages apart. By the pre-registered rules that is selection, caused by
food sensing, with repulsion necessary, in one species of the two measured; not takeover (shares
0.54-0.62). The design's prediction (i) ("selection appears with sensing on and not off, possibly
only with repulsion") holds for OSCILLIS; prediction (ii) ("sensing changes foraging but no lineage
wins consistently") holds for MITOSA so far. Pending: B's CPU replication of the same cells; VAGRANT's
sensing cells; the 30-species scan at gain 10 (`docs/SPECIES-SCAN-2026-11-16.md`).

## Replication: worker B's CPU run of the same design (appended 2026-11-16 05:05 UTC)

B's 1,800 runs (branch `vizier/food-sensing-brain-20261116` @ `25b722a`, 60 InstaBox CPU boxes, one
process per run, same seeds, same rules, `outputs/food_sensing_20261116/SUMMARY.md`) finished at
04:55 UTC. Seeds outside E of 50, winners +u / -u, verdict; GPU first, CPU second:

| species | fs0 k0 | fs0 k3 | fs10 k0 | fs10 k3 |
|---|---|---|---|---|
| OSCILLIS GPU | 7 (1/6) none | 24 (7/17) none | 28 (28/0) none | **40 (40/0) selection** |
| OSCILLIS CPU | 12 (4/8) none | 26 (9/17) none | 21 (21/0) none | 35 (35/0) none (40 under the secondary envelope) |
| MITOSA GPU | 1 (1/0) none | 9 (9/0) none | 5 (4/1) none | 19 (19/0) none |
| MITOSA CPU | 0 none | 1 none | 8 (6/2) none | 6 (6/0) none |
| VAGRANT GPU | 19 (10/9) none | 25 (24/1) none | lost | lost |
| VAGRANT CPU | 16 (10/6) none | 28 (26/2) none | 12 (12/0) none | **43 (0/43) selection** (winner share median 0.707, max 0.827) |

Reading across hardware. OSCILLIS: the sensing + repulsion cell carries the same +u edge on both
(40 of 50 and 35 of 50, every outside seed +u on both, and the same +u-only pattern without
repulsion: 28 and 21); the pre-registered bar of 40 is met on the GPU and missed by five seeds on
the CPU, so the honest statement is a real, borderline effect in this species. VAGRANT: rule-grade
selection on the CPU with the opposite winner (-u, as expected: each species has its own random brain
and `W1f`, so the favoured genome direction is species-specific), the GPU cells that would replicate
it were lost with the Modal disable. MITOSA: nothing on either. Every sensing-off cell on both
hardware: no selection. Every sensing-on, repulsion-off cell: no selection. Distinctness, neutral
sanity (B: 0 of 12 flags) and conservation agree on both.

**Across the two hardware runs of the one design: 2 of 3 species reach rule-grade selection in the
sensing + repulsion cell, none without sensing, none without repulsion.** Open: the two lost VAGRANT
GPU cells (one `modal run`, about $6, once Modal is restored) and the 30-species scan.

## Cost and deviations

Ten completed containers, 20,231 container-seconds, $17.60 at $3.13 per container-hour (A100-80GB
$0.000694/s plus cpu=8 cores and 32 GiB memory, from modal.com/pricing on 2026-11-16); the two killed
VAGRANT containers add about $2.80. The estimate stated before launch ($11 at a GPU-only $2.50/h)
was low: fs10 cells run about 1.5x slower than fs0 cells and OSCILLIS/VAGRANT about 2x slower than
MITOSA. Deviations: two cells missing (workspace disabled); `wall_seconds` per run is batch time
divided by batch size; frames not pulled. No simulation ran on citadel; the summary script ran over
JSON only.
