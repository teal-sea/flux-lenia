# Species scan: how often does selection appear across 30 species, and does food sensing change that?

Status: **design fixed before any run.** Results, a launch note and any deviation are appended below the horizontal rule at the end; this section is not edited afterwards.

Date: 2026-11-16 (UTC). Branch `vizier/species-scan-20261116` = `vizier/gpu-batch-runner-20261116` (GPU runner, food-sensing engine, `repulsion_kappa`) merged with `vizier/species-breadth-20261116` (27 new species; no engine changes). Follows `docs/FOOD-SELECTION-2026-11-09.md`, `docs/GENOME-TRANSPORT-2026-11-10.md`, `docs/FOOD-ON-EXACT-TRANSPORT-2026-11-10.md`, `docs/CONDITIONAL-BLENDING-2026-11-15.md`, `docs/FOOD-SENSING-2026-11-16.md`, `docs/GPU-BATCH-RUNNER-2026-11-16.md`, `docs/GPU-PILOT2-GAIN-LADDER-2026-11-16.md`.

## What is known

Four CPU experiments on three species (OSCILLIS, MITOSA, VAGRANT):

- No selection: no lineage wins under the neutral-envelope rule (largest winner share 0.70).
- Contact repulsion `kappa = 3` keeps lineages distinct: median end hybrid fraction 0.94 -> 0.31 (OSCILLIS), 0.92 -> 0.00 (MITOSA), 0.50 -> 0.00 (VAGRANT).
- The food-sensing brain (`Config.food_sense`: food features enter through the same ring bank with a per-species random `W1f` block scaled by `food_sense`) was calibrated by B's pilot, which found gains 0.1 to 10 change foraging in 0 of 3 species; 10 was chosen by fallback. A 2x2 at `food_sense = 10` x `kappa` {0, 3} x 3 species x 50 seeds and a GPU pilot 2 (gains 30, 100, 300, 1000, 64 seeds) are running; the scan's gain **G** is whatever the pilot-2 rule picks, or 10 if none qualifies, and is supplied at launch (`--pilot G`), not written here.
- Everything so far is three species. Whether any of it holds across genomes is untested. This scan tests it on 30.

## Question

Across 30 species, in each of four cells, in how many species does selection appear, and does food sensing (gain G) change that count? Secondary: in how many species does repulsion keep lineages distinct?

## Cells and runs

- **Cells (4):** `kappa` {0, 3} x `food_sense` {0, G}. `per_channel` transport, food on with the parameters of the earlier docs (`uptake 0.05`, `decay 5e-4`, `diffusion 0.1`, `threshold 0.3`, initial food uniform with total equal to the body mass), `advect_genome = True`, same placements, lineage axis (seed 20261103) and tag as the earlier experiments.
- **Species (30):** `@ALL` = every `outputs/species/*_genome.json`: SPECIES_001..030 (verified in the worktree: 30 files).
- **Seeds 1-20**, arms `treat` (A has `+u`, B has `-u`), `neutral_plus`, `neutral_minus`; **30,000 steps**, `sample_every = 100`; **`frame_every = 15000`** (frames at steps 0, 15,000 and 30,000 only; the value 0 is not valid in `gpu_batch.py`, and sparse frames keep the 7,200 `*_frames.npz` small; no rule below reads frames).
- **Batch = 60** (20 seeds x 3 arms): one (species, cell) per Modal A100-80GB container. **120 containers, 7,200 runs** (30 x 4 x 20 x 3).
- Manifest `gpu/species_scan_manifest.json` (experiment `species_scan_20261116`); `food_sense: "@PILOT"` is filled at launch. `gpu/manifest.py` dry expansion (`--pilot 10`, placeholder only) gives 120 batches / 7,200 runs; the first three ids, in order:

```
SPECIES_001_OSCILLIS_fs0_k0_per_channel    ... --kappa 0 --food-sense 0  --food 1 --batch 60
SPECIES_001_OSCILLIS_fs0_k3_per_channel    ... --kappa 3 --food-sense 0  --food 1 --batch 60
SPECIES_001_OSCILLIS_fs10_k0_per_channel   ... --kappa 0 --food-sense 10 --food 1 --batch 60   (fs10 only because the dry run used --pilot 10)
```

- `gpu/modal_campaign.py` adds `outputs/species` of the checkout it is launched from to the image (`add_local_dir(REPO/"outputs"/"species", "/app/outputs/species")`), so the 30 genomes are present at launch if it is launched from this branch.
- Hardware: GPU float64 (jax 0.11.1), validated bit-identical against the CPU runner on a single batch, drift about 2e-15. Trajectories are chaotic and differ per run between CPU and GPU; statistics and verdicts are what carry over (the 50-seed sense-off cells, `gpu/manifest_sense_off_50.json`, are the cross-check).

## Decision rules (fixed before the runs)

Thresholds are the earlier rules scaled from 5 to 20 seeds (4 of 5 -> 16 of 20; 3 of 5 -> 12 of 20). `delta` = A's share averaged over the last 10% of samples minus A's share at step 0 (`delta_share_A` in the run JSON).

**Rule 1: selection, per species x cell.** `E` = largest `|delta|` among that cell's 40 neutral runs (primary); the 95th percentile of those 40 `|delta|` (linear interpolation) is reported as a **secondary, labelled** variant and never replaces the primary. A treatment seed is outside `E` if `|delta| > E`; its winner is `+u` if `delta > 0`, else `-u`; its winner share is A's final share (`+u`) or 1 minus it (`-u`).
- **selection**: at least 16 of 20 treatment seeds outside `E` and all agree on the winner;
- **takeover**: selection and the median of those seeds' winner share is at least 0.90;
- **large but inconsistent**: at least 16 outside `E` with disagreeing winners;
- **no selection detected**: otherwise.

**Rule 2: lineage distinctness, per species**, at the same `food_sense`: treatment arm, end hybrid fraction (`final.hybrid_frac`: mass with ancestry between 0.1 and 0.9), `kappa 3` vs `kappa 0`, seeds matched.
- **distinct**: median hybrid fraction at `kappa 3` at most half that at `kappa 0`, AND at least 16 of 20 seeds strictly below their matched `kappa 0` seed;
- **no effect**: fewer than 12 of 20 below;
- **partial**: otherwise.

**Rule 3: neutral-arm sanity, per cell and species.** Mean of the 40 neutral `delta` within 2 standard errors of zero. A species-cell outside is **flagged as harness asymmetry**: reported, not voiding. About 5% of tests are expected to flag by chance (120 tests), so flags are read as a count against that.

**Rule 4: conservation.** Max relative drift of `sum(body) + sum(food)` per cell, expected about 1e-15.

**Rule 5: species-level aggregate (new).**
- For each cell: the number of species (of those with a complete cell) with `selection` or `takeover`, with an exact (Clopper-Pearson) binomial 95% interval.
- Food sensing **changes the frequency of selection** at a given `kappa` if the count in the sensing-on cell exceeds the count in the sensing-off cell AND an exact two-sided McNemar test on the paired per-species outcomes (selection-or-takeover vs not) gives p < 0.05. (If off exceeds on, the test is still printed; it does not count as "changes" in the sense of the question, and is reported as a decrease.) Two cells, `kappa 0` and `kappa 3`, are two tests; each is read at 0.05 and the pair is reported without correction, with that stated in the results.
- The distinctness frequency is treated the same way: number of species `distinct` at `kappa 3 vs 0`, exact interval, McNemar on `food_sense` 0 vs G.
- Per cell, the distribution across species (min, quartiles, median, max) of the winner's median final share (per species, the larger lineage's median final share over its 20 treatment seeds; descriptive, defined whatever the verdict) and of the end hybrid fraction (per-species median over treatment seeds).

Run `python scripts/species_scan_summary.py OUTROOT -o SUMMARY.md`; it computes all five rules over `OUTROOT/<id>/*_food1.json` and reports present vs expected runs (7,200). A cell is analysed only if all its 60 runs are present for that species; species missing from a cell are listed `incomplete` and dropped from that cell's denominators and from the pairs.

## Species caveats and the pre-registered subgroups

All 27 new species passed the existing hunt gates unchanged and a 3,000-step food-on smoke (54 of 54 runs, drift at most 4.9e-16; `hunts/CAMPAIGN-2026-11-16.md`). Flags there are the campaign's own, labelled not filtered:

| flag | species |
|---|---|
| none | ORBITA (017) |
| single qualifying division in the screen | CORONA 004, TENDRIL 008, ARBORIS 009, CILIATA 010, FLAGELLA 011, GLOBULA 012, HELIX 013, MEDUSA 015, NODULUS 016, PULSARA 018, QUASARIA 019, SPIRALIS 021, TORQUATA 022, VESICA 024, XENIA 025, ANTENNA 028 (16) |
| **no division in the 6-frame recording run** (gate verdict depends on tracker cadence) | TENDRIL 008, ARBORIS 009, MEDUSA 015, SPIRALIS 021, TORQUATA 022 |
| debris-dominated (>= 5 raw fissions per division) | SPLITTER 005, CILIATA 010, HELIX 013, PULSARA 018, SPIRALIS 021, VESICA 024, XENIA 025, ANTENNA 028 |
| fragmenting (>= 60 organisms tracked) | SPLITTER 005, DRIFTER 006, CILIATA 010, HELIX 013, RADIATA 020, UNDULA 023, VESICA 024, YGGRA 026, ZONATA 027, BIFIDA 029 |
| many bodies at the end (>= 6) | SPLITTER 005, NUCLEUS 007, HELIX 013, LUMINA 014, SPIRALIS 021, UNDULA 023, XENIA 025, YGGRA 026, ZONATA 027, CATENA 030 |
| cyclic locomotion flagged | LUMINA 014, UNDULA 023 |

Predatory pursuit was detected in VESICA 024 only; no new species establishes phototaxis. SPECIES_001..003 come from `discover.py curate` and carry no flags from this campaign.

**Primary analysis: all 30 species.** Pre-registered labelled subgroups, each reported with the same rules beside the primary and never in its place:
1. **Excluding the five cadence-dependent species** (TENDRIL, ARBORIS, MEDUSA, SPIRALIS, TORQUATA): 25 species.
2. **The original three** (001-003): the cross-check against the earlier CPU experiments.

No other post-hoc subgroup is declared. Any further split by flag (fragmenting, many bodies and so on) is exploratory and will be named as such.

## What consumes the result

The owner's Dish project defaults to **physics as renderer plus crossover topology**. That default changes only if selection appears when, and only when, the genome can touch food: i.e. a count of selection-or-takeover species that is higher with `food_sense = G` than with `0` by the Rule 5 test. If selection is absent or equally frequent in both, the default stands.

## Predictions

Three outcomes; I do not know which will occur.
1. **Food sensing creates selection** (Rule 5 changes the frequency, at least at `kappa 3`, where lineages stay distinct). The brain route works for a minority of genomes; the Dish default is reconsidered.
2. **Selection is rare or absent in every cell** and sensing does not change it (counts near 0 of 30 in all four, McNemar p large). The three-species result generalises; B's pilot found no foraging change at gains up to 10, and the shared random `W1f` need not couple to movement.
3. **Selection appears in some species in the sensing-off cells too** (a genome-dependent effect, with or without food sensing). Then the earlier "no selection" was a property of the three species, and the question becomes which genomes.

My guess, not a measurement: outcome 2, with a few `large but inconsistent` cells from fragmenting species where `E` is wide, and `distinct` in most species at `kappa 3` (the three-species result was 3 of 3).

Known limits, stated now: 20 seeds per species-cell and an `E` set by 40 runs, so a per-species verdict is weaker than the three-species 50-seed run and the strength is in the species count; one gain G for all 30 species (the pilot-2 species are three); `W1f` is random per species, so "food sensing" here means one random food coupling per species, not a designed one; 120 species-cell verdicts and two aggregate tests are not corrected for multiplicity; the distinctness verdict depends on the threshold-based hybrid measure (`0.1 < a < 0.9`); the 5 flagged-cadence species are in the primary analysis.

## Cost, stated before launch

Measured on Modal A100-80GB: about 19 ms per batched step at batch 60, so about 570 s per container; 120 containers x 570 s x $2.50/h = **about $47** (GPU time; container start-up and image build extra). The owner's total Modal cap for this program is $60, of which about $13 is already committed to the 2x2 and pilot 2: **the $47 estimate leaves no margin under the remaining $47, so 20 seeds fits only if the measured time holds; a running tally is needed and the launch can be stopped (`modal app stop`) and resumed**. 50 seeds (150-run batches, about 1,300 s each, 120 containers) would cost about $108 to $112 and **does not fit without a new cap**. Runs are resumable (`gpu_batch.py` skips existing JSON), so a partial launch is not lost.

## Launch and pull (owner)

```
modal run gpu/modal_campaign.py --manifest gpu/species_scan_manifest.json --pilot <G>
modal volume get flux-lenia-gpu-out /species_scan_20261116 ./out/
python scripts/species_scan_summary.py ./out/species_scan_20261116 -o SUMMARY.md
```


---

## Execution note (2026-11-17): CPU on Vultr + InstaBox instead of GPU on Modal (deviation, recorded)

Authorised by the owner after Modal burned real money. Design, cells, rules 1-5 and predictions above are **unchanged**; the venue differs from "Launch and pull". The runs are the CPU scheme of `scripts/food_selection.py` (float64, one thread per run), not the batched GPU runner, so float-level trajectories need not match GPU outputs.

- **Branch** `vizier/cpu-campaign-20261117` (merge of the species-scan, gpu-batch-runner and campaign-harness branches; engine/* clean; see the horizon doc for the two resolved script conflicts).
- **G = 10** (B's pilot fallback value, and the gain at which the 50-seed 2x2 found rule-grade selection in OSCILLIS (GPU, 40/50) and VAGRANT (CPU, 43/50)); not chosen by the pilot-2 rule.
- **Frames: `FRAME_EVERY = 15000`** for every cell (frames at 0, 15,000 and 30,000, as the GPU manifest); `SAMPLE_EVERY = 100`, `STEPS = 30000`. The food_sense argument is passed in all four cells (value 0 in the off cells), so the JSON of every cell carries the food-flow logs and float32 frames, as in the GPU runs. Output subdirectory `<species>_fs<G>_k<kappa>_per_channel` (what `scripts/species_scan_summary.py` reads).
- **Jobs:** 7,200 runs = 30 species x 4 cells x 20 seeds x 3 arms (`campaign_cpu/scan_all_jobs.txt`, `scripts/make_cpu_jobs.py`), split by seed so each side has every species and cell: **InstaBox: even seeds 2, 4, ..., 16 (2,880 runs)**, **Vultr box 2: the other 12 seeds, 1, 3, 5, ..., 19 and 18, 20 (4,320 runs)**. The InstaBox half is 8 seeds rather than 10 because of the 170 box-hour cap (2,880 runs x about 1,200 s / 8 concurrent is about 120 box-hours; 3,600 runs would be about 152 plus overhead, too close to the cap).
- **Vultr box 2:** `vizier-flux-cpu-20261116-2` (id `f9c1e6f3-fc17-47e8-a8c8-6b8db3924c36`, ip 209.250.255.87, 16 dedicated vCPU, 32 GiB), same software as box 1 (Python 3.13.18, jax 0.11.1, numpy 2.5.2, scipy 1.18.1). `scripts/run_batch.py /root/fl/out per_channel 16 /root/fl/scan_vultr2_jobs.txt` with `STEPS=30000 SAMPLE_EVERY=100 FRAME_EVERY=15000 SHARD=_v2`; log `runs_v2.log` ends with `ALL_DONE`. Started 2026-11-17T02:29:40Z.
- **InstaBox:** 30 fresh boxes `flux-scan-01` ... `flux-scan-30`, `create --vcpus 8 --mem-mib 16384 --auto-suspend 30m --max-run-minutes -1 --no-vault --secrets none --meta owner=vizier --meta task=flux-scan` (created 02:21Z (01) and 02:32-02:36Z (02-30), all launched by 02:36:22Z; list, shards and times in `outputs/species_scan_20261117/instabox_boxes.json`). Each box: venv with the same pins (jax 0.11.1, numpy 2.5.2, scipy 1.18.1, Python 3.13.5), the same tarball (engine+scripts sha256 equal to citadel's before launch), shard `campaign_cpu/scan_ib_shard_NN.txt` (96 runs: per seed 12 jobs dealt from a fixed-RNG shuffle, ordered seed by seed), 8 concurrent, `SHARD=_ibNN`, log `/data/out/runs_ibNN.log` ending `ALL_DONE`, outputs in `/data/out/`. Steal at launch: 0-1% (`vmstat`).
- **Cost accounting:** InstaBox against the hard cap of 170 box-hours (about $0.068 per 8/16 box-hour, remaining allowance about $11.5): box-hours are counted from creation to deletion for all 30 boxes (final figure in the Results section). Vultr: $1.32 per hour for both boxes, prepaid credit. Deadman on citadel deletes both Vultr boxes at 2026-11-23T06:00Z. No Modal.
- **Collection:** `/home/thomas/worktrees/flux-lenia-cpu-20261117/scripts/collect_cpu_campaign.sh`: rsyncs box 2's `/root/fl/out/` into `outputs/species_scan_20261117/`, pulls each finished InstaBox box (tar, sha256, `instabox-run pull`, compare, extract, `rm --yes`), records it in `instabox_boxes.json`, commits and pushes. Summary: `python scripts/species_scan_summary.py outputs/species_scan_20261117 -o SUMMARY.md` once all 7,200 runs are present.

- **InstaBox half complete (2026-11-17T06:11Z):** all 30 boxes finished (96 runs each, 2,880 JSON, none failed), pulled with sha256 verified against the box, extracted into `outputs/species_scan_20261117/` and deleted (`rm --yes`) in the same collector pass. **Box-hours (creation to deletion): 82.7 of the 170 cap**, about $5.6 at $0.068. Steal at launch 0-1%. Runs took about 10-17 min each at 8 concurrent. The Vultr box 2 half (4,320 runs) was still running.
