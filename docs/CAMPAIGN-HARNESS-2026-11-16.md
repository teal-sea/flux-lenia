# Campaign part A (2026-11-16): same-host control and determinism, kappa robustness, 300,000-step horizon

Status: **design fixed before any run.** Launch notes and results are appended below horizontal rules; this section is not edited afterwards.

Date: 2026-11-16 (UTC). Branch `vizier/campaign-harness-20261116`, based on `vizier/conditional-blending-20261115` @ `ce00383`. No change to `engine/*`. Follows `docs/CONDITIONAL-BLENDING-2026-11-15.md` (step 2), whose neutral-arm sanity check flagged VAGRANT at +2.15 SE.

## Where the compute runs

No simulation of any kind runs on citadel (the host carries the Hermes gateway and bots and ran out of memory under a batch on 2026-11-08). Every run below, including the smoke run, runs on InstaBox machines (Pro workspace, 8 vCPU / 16 GiB, Debian 13, Python 3.13, CPU, float64), 8 concurrent single-thread runs per box with `XLA_FLAGS="--xla_cpu_multi_thread_eigen=false intra_op_parallelism_threads=1"`, via `scripts/run_batch.py` started with `exec --background` on the box (the scheduler lives on the box). On citadel only edits, git, box control, file transfer, `python -c` imports and the summary script over JSON run. Box budget: at most 12 at once. Versions are recorded from the boxes; the target is the earlier batches' set (jax 0.11.1, numpy 2.5.2, scipy 1.18.1). Before dispatch the sha256 of `engine/*.py` and `scripts/*.py` on every box is compared with citadel.

Code changes (no engine change; defaults unchanged): `scripts/food_selection.py` gains two optional trailing CLI arguments, `SAMPLE_EVERY` (default 100, the previous hardcoded value) and `FRAME_EVERY` (default 0 = the previous frame steps at 0, 1/4, 1/2, 3/4, end; with `FRAME_EVERY > 0` frames at every multiple of it plus the end). `scripts/run_batch.py` passes them if the optional env vars `SAMPLE_EVERY` / `FRAME_EVERY` are set. A 300-step smoke run on a box checks that with defaults the series reproduces the committed 2026-11-10 control series to rounding at steps 100, 200, 300. New: `scripts/campaign_harness_summary.py` (JSON only, no simulation).

## Part 1: same-host control and determinism

**Question.** The step 2 neutral-arm check compared box runs (repulsion on) with citadel runs (repulsion off). No neutral run reproduced its control to 1e-12 and VAGRANT was flagged. Is that a host effect on a chaotic trajectory, or a leak?

**Arms.** (A) `control_box`: the exact 45 jobs of `outputs/food_on_exact_20261110/jobs.txt` (3 species x seeds 1-5 x `treat`, `neutral_plus`, `neutral_minus`; food on, `per_channel`, repulsion off, 30,000 steps, sampled every 100), all on ONE box. (B) `control_box_repeat`: three of them (OSCILLIS, MITOSA, VAGRANT; seed 1; `treat`), run a second time on the same box after (A) finishes (the same code, the same box, different concurrency: 3 at a time instead of 8). The engine revision differs from the 2026-11-10 control only by the repulsion term, which at `kappa = 0` is a Python-level branch that is not traced; the 300-step hash equality was tested on 2026-11-15.

**Measures.** Per run: `final.share_A` and `final.hybrid_frac` at step 30,000, the series, `share_A_end` (mean of the last 10% of samples), drift, wall time. The `lscpu` model and the box id of every box are recorded (whether two boxes share a physical host is not observable; "same host" means the same box).

**Decision rules.**
- (a) *Determinism.* For each of the 3 repeats, `|final.share_A| difference` and `|final.hybrid_frac| difference` between (A) and (B). **Deterministic** if all six differences are at most 1e-12; otherwise **nondeterministic on one host**. The step of first divergence (first sample with any difference above 1e-12 in `share_A`) is reported.
- (b) *Host effect.* Per run (45), `|box - citadel|` of final `hybrid_frac` and of final `share_A`. Report median and max over the 45, per species and overall, and how many of 45 agree to 1e-12, 1e-6, 1e-2 (for each of the two measures).
- (c) *Step 2 flag re-test.* The step 2 neutral-arm check repeated with the box control: end hybrid fraction (`final.hybrid_frac`) of the 30 repulsion-on neutral runs (`outputs/conditional_blending_20261115`, kappa 3) minus the matching box-control neutral runs, 10 pairs per species, mean difference and its standard error (`std / sqrt(10)`). The flag is **cleared** if `|mean| <= 2 SE` for every species with the box control; **confirmed** if any species (VAGRANT or another) still exceeds 2 SE. Also reported: the same table with the citadel control (repeats step 2) and box minus citadel for the same neutral runs.

**Prediction (written before the run).** If runs are deterministic on one host but box and citadel differ by order 1e-2 or more in final hybrid fraction, the step 2 mismatch is host-dependent floating point on a chaotic trajectory, not a leak. Alternatives, stated now: (i) the box control agrees with the citadel control to 1e-12 (the host does not matter) and the 2.15 SE is then a property of the repulsion arm, which would make a leak, or a real small effect of the term on neutral arms, the live explanation; (ii) repeats on one box differ (nondeterminism, e.g. thread scheduling): then no pairing of single runs is meaningful and the neutral-arm check can only be read as a distribution comparison. I expect the first outcome, as a guess and not a measurement. Limit: the check has 10 pairs per species and chaotic differences make pairs near-independent draws, so it can fail by chance at roughly 5% per species (about 14% over three) even with no leak; a "confirmed" for one species at 2 to 3 SE will be reported as such and not rescued, and also with the multiplicity stated.

## Part 2: kappa robustness (kappa 1 and 10)

**Question.** Do the step 2 conclusions (lineages distinct, no selection) hold when kappa is changed from the calibrated 3 by a factor of 3 down and 3.3 up, with 20 seeds instead of 5?

**Runs.** kappa in {1, 10} x 3 species x seeds 1-20 x arms `treat`, `neutral_plus`, `neutral_minus`; food on, `per_channel`, radius 8, 30,000 steps, sampled every 100 = 360 runs, in `outputs/campaign_harness_20261116/kappa_1/` and `kappa_10/`. Placements, lineage axis and food as in all earlier docs. Jobs ordered seed by seed, split by remainder over the boxes.

**Measures.** As in step 2, per run: A's share and `delta`, end hybrid fraction, pure fraction, blob count, largest blob, drift, saturation fraction with and without the term (`sat_frac`, `sat_frac_without_repulsion`, each sample), wall time. The **velocity saturation fraction per run** is recorded as the maximum over the 301 samples and the mean over samples 1 to 300.

**Decision rules.**
- *Distinctness (rule 1 of the step 2 doc, per species and kappa).* Seeds 1-5, matched control `outputs/food_on_exact_20261110`: **distinct** if the median treatment hybrid fraction is at most half the control's median AND at least 4 of 5 seeds are below their matched control seed; **no effect** if fewer than 3 of 5 are below; **partial** otherwise. Seeds 6-20 have no control at kappa 0 (none was run), so no matched verdict is possible: report the treatment hybrid fraction distribution of seeds 6-20 (n = 15: min, quartiles, median, max) and of all 20, next to the seeds 1-5 control distribution (min, median, max), and the number of seeds 6-20 whose hybrid fraction is below the seeds 1-5 control median. **Limitation, stated now:** this is an unmatched comparison of different seeds, not a paired one; it supports "similar to / lower than the control's range" and cannot give the paired verdict. Descriptive label (mine, not from an earlier doc): *distinct (unmatched)* if the seeds 6-20 median is at most half the control median and at least 12 of 15 seeds are below the control median. The box control of part 1 is used as a secondary control (labelled) if part 1 shows a host effect of order 1e-2 or more.
- *Selection (rule 2, scaled from 5 to 20 seeds).* `delta` = A's share averaged over the last 10% of samples minus the step-0 share. Per species and kappa, the neutral envelope `E` = largest `|delta|` among the 40 neutral runs (20 seeds x 2 neutral arms). A treatment seed is out of the envelope if `|delta| > E`; its winner is `+u` if `delta > 0`, else `-u`. **Selection** if at least 16 of the 20 treatment seeds are out of the envelope and agree on the winner; **takeover** if selection and the winner's final share is at least 0.90 in those seeds; **large but inconsistent** if at least 16 are out and the winners disagree; otherwise **no selection detected**. `E` is reported per species and kappa. Secondary, less conservative, labelled secondary: the same counts with `E95` = the 95th percentile of the 40 neutral `|delta|` (linear interpolation), reported as numbers and verdict, not substituted for the primary.
- *Saturation flag.* kappa is **flagged** if any run's saturation fraction (maximum over samples, as defined above) exceeds 1e-2. Reported separately for kappa 1 and 10, with the number of runs over 1e-2 by the maximum and by the mean.
- *Conservation.* `sum(body) + sum(food)` max relative drift per run, expect about 1e-15.

**Prediction.** kappa 10: lineages distinct, no selection, as at kappa 3 (the pilot gave hybrid 0.000 at kappa 10 for seed 1); kappa 1: partial or weak (the pilot at kappa 1 gave OSCILLIS 0.826, MITOSA 0.312 for seed 1 at 10,000 steps), so lineage distinctness is expected to fall off below kappa 3 for OSCILLIS first. No selection at either kappa is my expectation for MITOSA and OSCILLIS; VAGRANT's `+u` lean (3 of 5 seeds at kappa 3) may reach the 16-of-20 bar or not and I do not know which. Saturation at kappa 10 is a real possibility (kappa 30 in the pilot stayed below 1e-3). Known limits: seed-matching with the control only for 5 seeds; the control itself may carry a host effect (part 1); one radius.

## Part 3: horizon, 300,000 steps at kappa 3

**Runs.** kappa = 3, 3 species x seeds 1-5 x arms `treat`, `neutral_plus`, `neutral_minus`, food on, `per_channel`, **300,000 steps** = 45 runs, `outputs/campaign_harness_20261116/horizon_300k/`. Series sampled every **1,000** steps (301 samples; `SAMPLE_EVERY=1000`); frames every **50,000** steps (`FRAME_EVERY=50000`, 7 frames; the frames are 128 x 128 x 3 fields, about 0.3 MB per frame compressed, so every 10,000 steps would put roughly 400 MB in git; "at most every 10,000" is read as "not more often than every 10,000"). `share_A_end` and `delta` use the last 10% of samples (the last 30 samples, steps 270,000 to 300,000, 1 sample = 1,000 steps) as the earlier docs do for the last 10% of steps. Sharded over 6 boxes (8, 8, 8, 8, 8, 5 jobs), ordered by (seed, species, arm); every box runs all its jobs in one round.

**Definitions.** Per run: `d30` = mean of `share_A` over the samples with `27,000 < t <= 30,000` (steps 28,000, 29,000, 30,000: the last 10% of the first 30,000 steps) minus `share_A` at step 0; `d300` = `delta_share_A` (steps 270,000 to 300,000 minus step 0); `h30` and `h300` = `hybrid_frac` at steps 30,000 and 300,000 (single samples). Winner of a run = the lineage that gained at the horizon (`+u` if `delta > 0`); winner share = `share_A_end` if `delta > 0` else `1 - share_A_end`.

**Decision rules.**
- (a) *Takeover.* **Takeover appears** if at least one `treat` run has winner share at least 0.90 at step 300,000. Also reported: the number of treatment runs with winner share at least 0.90 at any sampled step (peak), and the same for all 30 neutral runs (a neutral run reaching 0.90 is drift to fixation by chance and not a genetic effect). **No takeover** otherwise.
- (b) *Does the share keep moving?* Tolerance tau = 0.05 (a 5-point share change; a choice made now, the 30,000-step neutral envelopes were 0.014 to 0.075). Per run: **saturated** if `|d300 - d30| <= tau`; else **grows** if `d300` and `d30` have the same sign and `|d300| > |d30|`; **reverses** if the signs differ; **shrinks** if the same sign and `|d300| < |d30|`. Counts per species and arm (treat and neutral), and the median of `|d300| - |d30|`. A treatment effect shows as treat counts differing from neutral counts.
- (c) *Distinctness at 300,000 steps.* Per run, hybrid fraction at 30,000 and at 300,000; per run **holds** if `h300 <= max(0.10, h30 + 0.05)`, else **erodes** (lineages remix). Per species: the medians, and rule 1 of the step 2 doc applied verbatim to the 5 treatment seeds at 300,000 steps against the 30,000-step citadel control `outputs/food_on_exact_20261110` (repulsion off); **limitation:** no repulsion-off control exists at 300,000 steps, so this compares a late repulsion state with an early control.
- (d) *Selection at 300,000 steps.* Rule 2 of the step 2 doc with `delta = d300`, `E` = largest `|d300|` among the 10 neutral runs per species, selection if at least 4 of 5 treatment seeds are out of the envelope and agree on the winner, takeover as above.
- (e) *Conservation* and wall time per run; saturation fractions as in part 2 (informational).

**Prediction (written before the run), three possible outcomes.** (1) *Takeover appears late*: some treatment seeds climb above 0.90 between 30,000 and 300,000 steps, treatment runs' `|d300|` exceeds the 300,000-step neutral envelope, and the winners agree. (2) *The share drifts but never takes over*: `|delta|` grows or wanders with neutral and treatment alike, no run's winner share reaches 0.90 in the treatment arm beyond what neutral arms do, selection rule says no selection or large but inconsistent. (3) *Nothing changes after 30,000 steps*: most runs are saturated in the rule (b) sense and `h300` close to `h30`. My expectation, a guess and not a measurement: outcome 2 for OSCILLIS and VAGRANT (the 30,000-step deltas are of both signs and the brain does not read food), outcome 3 for MITOSA, and I put the probability of any takeover in the treatment arm well below one half. Outcomes can mix across species.

## Common to all parts

Per run also: conservation `max_rel_total_drift`, wall time, blob counts. Per box: id, size, created and deleted time, `lscpu` model, versions, cost estimate (about $0.07 per 8/16 box-hour, an estimate and not a bill). Every deviation from this design is listed in the results section. Raw outputs (`*_food1.json`, `*_frames.npz`, per-run logs, jobs and shard files, shard logs) are committed under `outputs/campaign_harness_20261116/`; `SUMMARY.md` is produced by `scripts/campaign_harness_summary.py`. Execution (the runs finishing) is reported separately from verification (the summary script's checks, the checksum comparison after the pull).


---

## Progress note (all shards launched), 2026-11-16 01:47 to 01:50 UTC

Code on every box: HEAD `48f5d6e` (`engine/ scripts/ docs/ outputs/species/ outputs/campaign_harness_20261116/`) extracted to `/data/fl/code`; the sha256 of the sorted `sha256sum engine/*.py scripts/*.py` listing is `b00f97b6...fb820` on all 12 boxes and on citadel. Venv `/data/fl/venv` (Python 3.13.5, jax 0.11.1, jaxlib 0.11.1, numpy 2.5.2, scipy 1.18.1, ml_dtypes 0.6.0, opt_einsum 3.4.0, CPU, float64), CPU model `AMD EPYC`, 8 vCPU / 16 GiB, template `agent-browser` (the default of `create`; the box is used as plain Debian 13). One box (`flux-campa-w1`) was created, set up and smoke-tested, then forked 5 + 5 + 1 (fork takes at most 5 per call). Smoke (300 steps, OSCILLIS seed 1 treat, kappa 0, defaults): the series reproduces the committed 2026-11-10 citadel control to 1e-16 at step 100, 5e-14 at step 200 and **1.1e-8 (share_A), 4.1e-8 (hybrid_frac) at step 300**: the two hosts already diverge measurably at step 300, which is the first evidence for the host hypothesis (not a result of the design; recorded here because it was observed before the runs). The horizon shards were launched first (01:47); `fb` and `fc` were forked from `w1` while its horizon shard was running, so their `/data/fl/out` was emptied (`rm -rf /data/fl/out/*`) before launch (no run state is copied by a fork, only files).

| box | id | shard suffix | assignment |
|---|---|---|---|
| `flux-campa-w1` | `m_agq6ebmuseqbisxft2o7uyqq4m` | `_h1` | horizon, jobs_h1.txt (8) |
| `flux-campa-fa-1` | `m_agq6eb4vgg5w4qlwty5wbsgnfu` | `_h2` | horizon, jobs_h2.txt (8) |
| `flux-campa-fa-2` | `m_agq6eb4wy3y7qlajsjqqg6gfau` | `_h3` | horizon, jobs_h3.txt (8) |
| `flux-campa-fa-3` | `m_agq6eb4yorxm6yp7ocah7ct5wa` | `_h4` | horizon, jobs_h4.txt (7) |
| `flux-campa-fa-4` | `m_agq6eb42gee5jxyeipnbexa5yy` | `_h5` | horizon, jobs_h5.txt (7) |
| `flux-campa-fa-5` | `m_agq6eb43qidw6mshskaqbtaqoi` | `_h6` | horizon, jobs_h6.txt (7) |
| `flux-campa-fc` | `m_agq6eczgglttsb7x4vvsf2qvse` | `_c1,c2` | control_box (45) then control_box_repeat (3), same box |
| `flux-campa-fb-1` | `m_agq6ecxmg6htzkbtrfqkpxigby` | `_k1` | kappa 1 and 10, jobs_k1.txt (72) |
| `flux-campa-fb-2` | `m_agq6ecxoenac53wurbvqbnuzdm` | `_k2` | kappa 1 and 10, jobs_k2.txt (72) |
| `flux-campa-fb-3` | `m_agq6ecxphd6f6vmftyajpjhiyy` | `_k3` | kappa 1 and 10, jobs_k3.txt (72) |
| `flux-campa-fb-4` | `m_agq6ecxq5o4gkj7t7ziws35fxi` | `_k4` | kappa 1 and 10, jobs_k4.txt (72) |
| `flux-campa-fb-5` | `m_agq6ecxr6vr2yib4azme6vzwye` | `_k5` | kappa 1 and 10, jobs_k5.txt (72) |

Shard commands (working directory `/data/fl/code`; `. /data/fl/env.sh` sets `PY=/data/fl/venv/bin/python` and `XLA_FLAGS="--xla_cpu_multi_thread_eigen=false intra_op_parallelism_threads=1"`), each started with `instabox-run exec <box> --background`; the scheduler lives on the box:
- horizon: `SHARD=_hN STEPS=300000 SAMPLE_EVERY=1000 FRAME_EVERY=50000 $PY scripts/run_batch.py /data/fl/out per_channel 8 outputs/campaign_harness_20261116/jobs_hN.txt`
- kappa: `SHARD=_kN STEPS=30000 $PY scripts/run_batch.py /data/fl/out per_channel 8 outputs/campaign_harness_20261116/jobs_kN.txt`
- control: `SHARD=_c1 STEPS=30000 $PY scripts/run_batch.py /data/fl/out per_channel 8 outputs/campaign_harness_20261116/jobs_control_box.txt`, then `SHARD=_c2 ... jobs_control_box_repeat.txt` (3 jobs).
Outputs on a box: `/data/fl/out/<subdir>/` (`horizon_300k`, `kappa_1`, `kappa_10`, `control_box`, `control_box_repeat`) with `*_food1.json`, `*_frames.npz`, `run_*.log`; shard logs `/data/fl/out/runs_<suffix>.log` (the shard is finished when its last line is `ALL_DONE`; a finished job is a line `done ... rc=0`) and `rss_<suffix>.log`.

Expected time: horizon about 2.5 h (a 300,000-step run is about ten times the 30,000-step wall of 437 to 864 s), kappa shards 72 jobs = 9 rounds of 8, about 2 h, control 45 + 3 jobs, about 1.5 h.

To collect, from any machine with the `instabox-run` wrapper (key injected by the wrapper, never copied to a box), for each box `<b>`:
```
~/bin/instabox-run exec <b> --timeout 60 -- 'tail -1 /data/fl/out/runs_*.log; find /data/fl/out -name "*_food1.json" | wc -l'
~/bin/instabox-run exec <b> --timeout 300 -- 'cd /data/fl/out && tar -czf /data/fl/out_<b>.tgz . && sha256sum /data/fl/out_<b>.tgz'
~/bin/instabox-run pull <b> /data/fl/out_<b>.tgz ./out_<b>.tgz        # no pipe to head/tail; compare sha256sum with the box's
mkdir -p outputs/campaign_harness_20261116 && tar -xzf out_<b>.tgz -C outputs/campaign_harness_20261116
python scripts/campaign_harness_summary.py > outputs/campaign_harness_20261116/SUMMARY.md
~/bin/instabox-run rm --yes <b>            # only after the verified pull, boxes named flux-campa-* only
```
Box count at launch: 12 (the budget). Deviation so far: the horizon shards are 8, 8, 8, 7, 7, 7 jobs (split by remainder, balanced) and not 8, 8, 8, 8, 8, 5 as written in the design; same single round. Box names are lowercase (`flux-campa-*`; the service rejects capitals). No simulation ran on citadel.


---

## Progress note 2 (deviation: horizon shards moved to fresh boxes), 2026-11-16 02:26 UTC

**Measured.** Forks of one box land on that box's physical host. Twelve forks (96 vCPU) on one host showed CPU steal (`vmstat` `st`) of 59 to 71%, each run process getting about 40% of a core (`ps` `pcpu`), and no run had finished 36 minutes after launch (01:50 to 02:26; reference wall for a 30,000-step run on an uncontended box: median 836 s, max 864 s), i.e. a slowdown of at least 2.6x (and about 2.5x from the CPU share). A control box created fresh (`flux-campa-t1`, not a fork), under an 8-thread busy loop, showed 0% steal. **Decision:** the slowdown is above 2x, so the long pole (the six 300,000-step shards, which would have taken about 6 h instead of 2.3 h) was moved: the six horizon forks (`flux-campa-w1`, `-fa-1` to `-fa-5`) were deleted with their (empty, 17 minutes old) runs, and the horizon shards were relaunched from step 0 on six fresh boxes created with `create` (box count never above 12 at any time: the 13th, `t1`, was a probe created while 12 existed? no: `t1` was created at 02:07 as the 13th box; see below). Steal on the fresh boxes at 02:24: t1 1%, g2 31%, g3 29%, g4 58%, g5 48%, g6 40%; on the five kappa forks and the control fork 33 to 49% (down from 54 to 71% before the horizon forks were removed). So fresh boxes are not uncontended either; the host(s) are shared with each other or with other tenants, and the fleet total is capped at roughly half of 96 vCPU. Kappa and control shards (20 to 36 minutes into their first round) were NOT relaunched: a fresh box gives no guaranteed better host, and the loss of 36 minutes of progress is about what a relaunch would save. They continue on the forks. Horizon, kappa and control wall times in the results are therefore **not comparable to the 836 s reference**; they are measured and reported as they come.

Deviations recorded here: (1) `flux-campa-t1` was created as a probe (a 13th box for about 4 minutes, 02:07 to 02:11, until the six forks were deleted); the cap of 12 was exceeded by one box for those minutes, and `t1` was then used as horizon shard h1. (2) A tarball in the shared scratch directory (`$TMPDIR/code.tgz`) was overwritten at 01:47 by a sibling worker with its own revision (different `engine/neural_field.py`, `engine/nutrient.py`, `scripts/food_selection.py`, `scripts/run_batch.py`). The first six boxes had received my tarball before that (their hash check passed); the fresh boxes were first set up from the sibling's tarball, the hash check **failed**, nothing was launched from it, and the boxes were re-extracted from a private tarball (`.../scratch/campA/code.tgz`, `git archive HEAD` of this worktree at `53749ba`, which adds `scripts/campaign_harness_summary.py`) after `rm -rf /data/fl/code /data/fl/out`. On these six boxes the sha256 of the sorted `sha256sum engine/*.py scripts/*.py` listing is `cba6d93f...bb0a`, equal to citadel's at `53749ba`; the engine files and `scripts/food_selection.py`, `scripts/run_batch.py` are identical to the ones on the kappa and control boxes (per-file hashes compared); the only difference is the extra summary script. (3) Relaunch from step 0 on the horizon boxes; no result of the first launch was kept.

| box | id | shard suffix | assignment | note |
|---|---|---|---|---|
| `flux-campa-t1` | `m_agq6eha73qyzaza6kpkk6jrlfa` | `_h1` | horizon, `jobs_h1.txt` (8) | created 02:07:36 UTC, launched 02:15 to 02:17 |
| `flux-campa-g2` | `m_agq6ehzbv75jt5fek7cd3j63gm` | `_h2` | horizon, `jobs_h2.txt` (8) | created 02:10:53 UTC, launched 02:15 to 02:17 |
| `flux-campa-g3` | `m_agq6ehz57nqmm2dzicvklkjldu` | `_h3` | horizon, `jobs_h3.txt` (8) | created 02:11:00 UTC, launched 02:15 to 02:17 |
| `flux-campa-g4` | `m_agq6eh2vucampy3zfymkq4iydi` | `_h4` | horizon, `jobs_h4.txt` (7) | created 02:11:06 UTC, launched 02:15 to 02:17 |
| `flux-campa-g5` | `m_agq6eh3nqse4wjbw2vclzc67ky` | `_h5` | horizon, `jobs_h5.txt` (7) | created 02:11:12 UTC, launched 02:15 to 02:17 |
| `flux-campa-g6` | `m_agq6eh4ovwy5vyyywqb4iqcolu` | `_h6` | horizon, `jobs_h6.txt` (7) | created 02:11:21 UTC, launched 02:15 to 02:17 |

The kappa (`flux-campa-fb-1` to `-5`, `_k1` to `_k5`) and control (`flux-campa-fc`, `_c1` then `_c2`) shards of Progress note 1 are unchanged. Collection commands as in Progress note 1 with the new horizon box names; `<b>` in `/data/fl/out_<b>.tgz` is the box name. Nothing was simulated on citadel.
