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


---

## Collection note (takeover), 2026-11-16 05:15 UTC

Worker sa-0-d8be21d7 was interrupted at about 03:22 UTC (after relaunching the horizon shards on fresh boxes). A second worker (FORGE subagent) took over at about 05:05 UTC with the job: wait for the shards, launch the one pre-registered `_c2` repeat shard on `flux-campa-fc` after `_c1` finishes, pull every box with sha256 comparison, delete each `flux-campa-*` box only after its verified pull, run `scripts/campaign_harness_summary.py`, append Results. No new experiments, no other relaunch, nothing simulated on citadel.

Box states at takeover (measured by Vizier at 05:08 UTC): `flux-campa-t1` (`_h1`) 8 of 8 json, ALL_DONE at 04:04 UTC; `g2` to `g6` (`_h2` to `_h6`) 0 json, 7 to 8 processes each; `fb-1` to `fb-5` (`_k1` to `_k5`) 40 of 72 json each; `fc` (`_c1`) 44 of 45 json, 1 process left. All 12 boxes listed Running at 05:04.


---

## Results (collected 2026-11-16 05:06 to 06:45 UTC)

All numbers below are copied from `outputs/campaign_harness_20261116/SUMMARY.md`, produced by `scripts/campaign_harness_summary.py` (unchanged, ran without error on the real layout; every rule as written in the design). **Execution** (the runs finishing: 45 + 3 + 360 + 45 = 453 run JSONs, all `rc=0`, per-shard `ALL_DONE`) is separated from **verification** (the summary script, and the sha256 of every pulled tarball on citadel equal to the box's, below). Raw outputs are under `outputs/campaign_harness_20261116/{control_box,control_box_repeat,kappa_1,kappa_10,horizon_300k,shard_logs}/`; per-box tarball sha256 are in the box table.

### Part 1: same-host control and determinism

**(a) Determinism: deterministic.** The three repeats (seed 1, `treat`, same box `flux-campa-fc`, 3 concurrent instead of 8) reproduce the first runs exactly: |d final share_A| and |d final hybrid_frac| are 0.000e+00 for OSCILLIS, MITOSA and VAGRANT (all six differences at most 1e-12); no sample of `share_A` differs by more than 1e-12 (first divergence: none). Wall time first / repeat: 2750 / 1347, 2739 / 1348, 2777 / 1355 s (the first runs shared the host with the other 42, the repeat ran 3 at a time).

**(b) Host effect, box vs citadel, 45 runs** (box `flux-campa-fc` against `outputs/food_on_exact_20261110`; `|box - citadel|`):

| set | measure | median | max | agree 1e-12 | agree 1e-6 | agree 1e-2 |
|---|---|---|---|---|---|---|
| all (45) | final share_A | 6.568e-03 | 5.304e-02 | 0 | 0 | 31 |
| all (45) | final hybrid_frac | 1.416e-02 | 3.223e-01 | 11 | 11 | 19 |
| OSCILLIS (15) | share_A / hybrid | 5.985e-03 / 1.875e-03 | 2.007e-02 / 5.539e-02 | 0 / 5 | 0 / 5 | 12 / 8 |
| MITOSA (15) | share_A / hybrid | 8.300e-03 / 1.482e-02 | 3.477e-02 / 3.223e-01 | 0 / 5 | 0 / 5 | 8 / 6 |
| VAGRANT (15) | share_A / hybrid | 5.107e-03 / 1.792e-02 | 5.304e-02 / 3.221e-01 | 0 / 1 | 0 / 1 | 11 / 5 |

No run agrees in final `share_A` to 1e-12 or 1e-6. At step 300 the median |d share_A| is 6.79e-11 (max 6.87e-05). The first sample where box and citadel differ by more than 1e-12 in `share_A`: median step 300 (min 100, max 800), and 45 of 45 runs diverge. The host effect is order 1e-2 in final share and, for hybrid fraction, up to 0.32 in a single run. This is the prediction's first outcome (deterministic on one host, differing by order 1e-2 or more across hosts). Not shown by the script: which 11 runs agree in hybrid_frac to 1e-12 (the count is the same at 1e-12 and 1e-6).

**(c) Step 2 flag re-test: cleared.** Final `hybrid_frac`, repulsion (kappa 3, step 2 neutral runs) minus control, 10 neutral pairs per species:

| species | control | mean diff | SE | mean/SE | flag |
|---|---|---|---|---|---|
| OSCILLIS | box (this campaign) | +0.0017 | 0.0165 | +0.10 | ok |
| MITOSA | box | -0.0426 | 0.0426 | -1.00 | ok |
| VAGRANT | box | +0.0267 | 0.0374 | +0.71 | ok |
| OSCILLIS | citadel (repeats step 2) | +0.0021 | 0.0196 | +0.10 | ok |
| MITOSA | citadel | -0.0313 | 0.0250 | -1.25 | ok |
| VAGRANT | citadel | +0.0133 | 0.0062 | **+2.15** | exceeds 2 SE |
| OSCILLIS / MITOSA / VAGRANT | box minus citadel, same runs | -0.0003 / -0.0113 / +0.0134 | 0.0062 / 0.0191 / 0.0395 | -0.05 / -0.59 / +0.34 | ok |

Against the same-host box control every species is within 2 SE (largest |mean/SE| 1.00), so by the pre-registered rule the flag is **cleared**. The citadel-control row reproduces the step 2 number (+2.15 SE) exactly. With the box control VAGRANT's difference has a larger mean (+0.0267) and a six times larger SE (0.0374 vs 0.0062): the citadel control's tight spread was what made 0.0133 look significant, and the host change moves the control values by more than that. Multiplicity: three species were tested (about 14% chance of one exceedance with no leak). Context, not evidence for this part: worker B's 50-seed 2x2 on fresh boxes found 0 of 12 neutral flags, Vizier's GPU run 1 of 12 (MITOSA, -2.19 SE); both are consistent with chance.

### Part 2: kappa robustness (kappa 1 and 10, 20 seeds, 180 runs each, all present)

**Distinctness** (rule 1 matched for seeds 1-5 against the citadel control; unmatched descriptive for seeds 6-20, n = 15, control seeds 1-5 median in brackets):

| kappa | species | median hybrid seeds 1-5 [control median] | below matched control | rule 1 | seeds 6-20 hybrid min / q1 / med / q3 / max | seeds 6-20 below control median | distinct (unmatched) | median of all 20 |
|---|---|---|---|---|---|---|---|---|
| 1 | OSCILLIS | 0.915 [0.939] | 3 of 5 | **partial** | 0.263 / 0.834 / 0.965 / 1.000 / 1.000 | 7 of 15 | no | 0.940 |
| 1 | MITOSA | 0.448 [0.921] | 4 of 5 | **distinct** | 0.020 / 0.278 / 0.758 / 0.996 / 1.000 | 9 of 15 | no | 0.699 |
| 1 | VAGRANT | 0.035 [0.502] | 5 of 5 | **distinct** | 0.000 / 0.001 / 0.046 / 0.074 / 0.318 | 15 of 15 | yes | 0.041 |
| 10 | OSCILLIS | 0.000 [0.939] | 5 of 5 | **distinct** | 0.000 / 0.000 / 0.000 / 0.000 / 0.000 | 15 of 15 | yes | 0.000 |
| 10 | MITOSA | 0.000 [0.921] | 5 of 5 | **distinct** | 0.000 / 0.000 / 0.000 / 0.000 / 0.001 | 15 of 15 | yes | 0.000 |
| 10 | VAGRANT | 0.000 [0.502] | 5 of 5 | **distinct** | 0.000 / 0.000 / 0.000 / 0.000 / 0.000 | 15 of 15 | yes | 0.000 |

Seeds 1-5 medians by kappa (OSCILLIS / MITOSA / VAGRANT): kappa 0 citadel 0.939 / 0.921 / 0.502; kappa 1 0.915 / 0.448 / 0.035; kappa 3 (step 2) 0.313 / 0.000 / 0.000; kappa 10 0.000 / 0.000 / 0.000. Distinctness is robust at kappa 10 for all species and at kappa 1 for VAGRANT; at kappa 1 OSCILLIS gives no distinctness (the unmatched seeds 6-20 median 0.965 is above its control median) and MITOSA is mixed (matched seeds distinct, unmatched seeds 6-20 median 0.758, only 9 of 15 below the control median, so the unmatched label is "no"). The box control as secondary control gives the same verdicts except OSCILLIS kappa 1 "no effect" and MITOSA, VAGRANT "distinct" (see SUMMARY.md).

**Selection** (rule 2 at 16 of 20; `E` = largest |delta| of the 40 neutral runs):

| kappa | species | E | treat out of E | winners | max winner share | verdict | E95 | out of E95 (winners) | verdict at E95 (secondary) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | OSCILLIS | 0.0459 | 4 of 20 | +u 0 / -u 4 | 0.591 | no selection detected | 0.0173 | 12 (+u 2 / -u 10) | no selection detected |
| 1 | MITOSA | 0.0604 | 2 of 20 | +u 2 / -u 0 | 0.588 | no selection detected | 0.0507 | 4 (+u 3 / -u 1) | no selection detected |
| 1 | VAGRANT | 0.0477 | 8 of 20 | +u 8 / -u 0 | 0.703 | no selection detected | 0.0259 | 12 (+u 12) | no selection detected |
| 10 | OSCILLIS | 0.0363 | 11 of 20 | +u 5 / -u 6 | 0.640 | no selection detected | 0.0212 | 15 (+u 7 / -u 8) | no selection detected |
| 10 | MITOSA | 0.0778 | 3 of 20 | +u 3 / -u 0 | 0.641 | no selection detected | 0.0501 | 5 (+u 5) | no selection detected |
| 10 | VAGRANT | 0.0376 | 9 of 20 | +u 9 / -u 0 | 0.685 | no selection detected | 0.0242 | 9 (+u 9) | no selection detected |

No selection at either kappa, primary or secondary rule. VAGRANT's one-sided lean persists: all of its out-of-envelope seeds favour `+u` (8 of 20 at kappa 1, 9 of 20 at kappa 10, and 12 of 20 at kappa 1 with E95), below the 16-of-20 bar at both; so the question whether VAGRANT reaches the bar is answered: it does not, at either kappa, and the lean is real in sign but weak in size (max winner share 0.70).

**Saturation flag: not flagged at either kappa.** Runs with max-over-samples `sat_frac` above 1e-2: 0 of 180 at kappa 1, 0 of 180 at kappa 10 (by the mean over samples also 0). Largest `sat_frac` in any sample 1.05e-03 (kappa 1 OSCILLIS, kappa 10 OSCILLIS and MITOSA). The prediction that kappa 10 might saturate velocity is not borne out. **Conservation:** max relative drift of `sum(body)+sum(food)` 3.04e-15 (kappa 1: 3.02e-15, kappa 10: 3.04e-15). Wall time per run, median / max: kappa 1 1896 to 1914 / 3111 s, kappa 10 1888 to 1896 / 3099 s (steal-affected, see deviations).

### Part 3: horizon, 300,000 steps at kappa 3 (45 runs, all present)

**(a) Takeover: takeover appears.** Treatment runs with winner share at least 0.90 at step 300,000: OSCILLIS 2 of 5 (seed 1: 0.955, seed 2: 0.933), MITOSA 0 of 5 (max 0.616), VAGRANT 1 of 5 (seed 2: 1.000; A's share reaches 0.000, i.e. lineage B fixes). The same counts at any sampled step are identical (2, 0, 1). Neutral runs reaching 0.90 at any sample: 0 of 10 for each species (no drift to fixation in the neutral arms). In every one of the 15 treatment runs the winner is `-u` (`d300` is negative in 15 of 15); this is a measured count from the per-run table, not a rule.

**(b) Share keeps moving, tau = 0.05:**

| species | arm | saturated | grows | reverses | shrinks | median |d300| - |d30| | median |d30| | median |d300| |
|---|---|---|---|---|---|---|---|---|
| OSCILLIS | treat | 0 | 2 | 3 | 0 | +0.365 | 0.018 | 0.386 |
| OSCILLIS | neutral (10) | 10 | 0 | 0 | 0 | +0.006 | 0.006 | 0.009 |
| MITOSA | treat | 0 | 1 | 4 | 0 | +0.042 | 0.025 | 0.067 |
| MITOSA | neutral (10) | 10 | 0 | 0 | 0 | +0.000 | 0.021 | 0.022 |
| VAGRANT | treat | 0 | 0 | 5 | 0 | +0.047 | 0.050 | 0.098 |
| VAGRANT | neutral (10) | 7 | 3 | 0 | 0 | +0.001 | 0.011 | 0.008 |

Treatment: 0 of 15 saturated (3 grows, 12 reverses: the 30,000-step sign is wrong in 12 of 15 for the 300,000-step winner). Neutral: 27 of 30 saturated; the 3 that grow are VAGRANT `neutral_plus` seeds 1-3 (d300 -0.080, +0.354, +0.264), so VAGRANT's neutral arm has large late drift too. Outcome 3 of the prediction ("nothing changes") is rejected for all three species.

**(c) Distinctness at 300,000 steps:** rule 1 against the 30,000-step citadel control (limitation: early control, late state): OSCILLIS **distinct** (median 0.000 vs control 0.939, 5 of 5 below), MITOSA **distinct** (0.000 vs 0.921, 5 of 5), VAGRANT **distinct** (0.000 vs 0.502, 5 of 5). Holds / erodes per treatment run: OSCILLIS 4 / 1, MITOSA 5 / 0, VAGRANT 5 / 0 (neutral, 10 runs: 5 / 5, 7 / 3, 9 / 1). Median hybrid at 30k to 300k, treatment: OSCILLIS 0.313 to 0.000, MITOSA 0.000 to 0.000, VAGRANT 0.000 to 0.000. Exceptions in OSCILLIS: seed 3 erodes (0.466 to 0.870), seed 5 has hybrid 0.955 to 1.000, which the "holds" rule (`h300 <= max(0.10, h30 + 0.05)`) classes as holds; so for OSCILLIS the 300,000-step distinctness is 3 to 4 of 5 by eye and the rule's count of 4 includes seed 5. The medians say distinct, two runs say not.

**(d) Selection at 300,000 steps** (rule 2, bar 4 of 5, `E` = largest |d300| of 10 neutral runs):

| species | E | treat out of E | winners | max winner share | verdict | treat d300 seeds 1-5 |
|---|---|---|---|---|---|---|
| OSCILLIS | 0.0375 | 5 of 5 | +u 0 / -u 5 | 0.955 | **selection** | -0.456 -0.428 -0.343 -0.386 -0.200 |
| MITOSA | 0.0735 | 2 of 5 | +u 0 / -u 2 | 0.616 | no selection detected | -0.067 -0.032 -0.115 -0.086 -0.048 |
| VAGRANT | 0.3543 | 1 of 5 | +u 0 / -u 1 | 1.000 | no selection detected | -0.024 -0.495 -0.245 -0.035 -0.098 |

OSCILLIS is "selection", not "takeover" under the rule (takeover requires every out-of-envelope winner at 0.90; seeds 3 and 5 are 0.843 and 0.698, seeds 1, 2, 4: 0.955, 0.933, 0.888). MITOSA: 5 of 5 treatment seeds drift to `-u` with |d300| 0.032 to 0.115, but only 2 exceed E = 0.0735 (the largest neutral |d300|, a `neutral_minus` seed at +0.074). VAGRANT: E is inflated to 0.354 by one neutral run (`neutral_plus` seed 2, +0.354, winner share 0.849), so the rule cannot detect selection there although treatment seed 2 reaches 1.000; at 30,000 steps the same neutral runs had E 0.033. The VAGRANT "no selection detected" is a property of the envelope, as the rule is written, and not evidence of absence.

**Prediction check (design written before the run):** I expected outcome 2 (drift, no takeover) for OSCILLIS and VAGRANT and outcome 3 for MITOSA, with any takeover "well below one half". Measured: takeover in 3 of 15 treatment runs (OSCILLIS 2, VAGRANT 1) and 0 of 30 neutral; OSCILLIS gets selection with a consistent `-u` winner; MITOSA is not at rest (|d300| 0.03 to 0.12, 4 of 5 reverse sign). The prediction was wrong for OSCILLIS and for MITOSA's "nothing changes".

**(e) Conservation, saturation, wall time:** max relative drift of `sum(body)+sum(food)` over the 45 runs 4.61e-14 (median 1.16e-14); largest `sat_frac` 5.36e-04, 0 runs above 1e-2; wall seconds per run median 11,460, min 6,089, max 13,616.

### Conservation (all parts)

Max relative drift of `sum(body)+sum(food)`: kappa runs 3.04e-15, horizon runs 4.61e-14, control runs: see SUMMARY.md (not part of its tables; the control JSONs carry `max_rel_total_drift`).

### Wall times

Control (45 runs, 8 concurrent under steal) 2750 s typical, repeat (3 concurrent) 1347 to 1355 s; kappa runs median about 1900 s; horizon runs median 11,460 s (3.2 h). None is comparable to the 836 s reference for an uncontended box (steal measured in progress note 2).

### Box facts, versions, cost

Instabox Pro workspace, 8 vCPU / 16 GiB, template `agent-browser`, `AMD EPYC`, Python 3.13.5, jax 0.11.1, jaxlib 0.11.1, numpy 2.5.2, scipy 1.18.1, float64, CPU, code revision as in the progress notes (sha256 of the engine and script listing compared with citadel before dispatch). Ids are in the two progress notes. Tarball sha256 (box `/data/fl/out_<box>.tgz` equal to citadel `sha256sum` in every case) and deletion time (UTC, 2026-11-16, `instabox-run rm --yes` in the same step as the verified pull):

| box | shard | tarball sha256 | deleted |
|---|---|---|---|
| flux-campa-t1 | `_h1` | 80f0a9874e6dbc6aee442e7516bccb7af4fb6fa38491ef7929eef24302bcd0a6 | 05:06 |
| flux-campa-fc | `_c1`, `_c2` | b9cda4dcb87c2823e209bb90b6cc43bf93d651c9ebabb57a11ae1b6924cff1b7 | 05:27 |
| flux-campa-g2 | `_h2` | 1d78815832e12fac60e2a13a9996f202889eaca38d0cc2abbe33a671f3453efb | 05:28 |
| flux-campa-g3 | `_h3` | d5fe78ebfb0ceae9afd44b3756dfc86539019d3d4131bf40376021edc9031920 | 05:29 |
| flux-campa-g4 | `_h4` | 250c78268d8ab83341ea6a9a57506db5dbca1c9a794d5da079f25ffe67dc011e | 06:06 |
| flux-campa-g5 | `_h5` | edebdf1918d9f8ec6602624a1fe37a1b89a0b4316d3601e251d62f85e42151fd | 06:06 |
| flux-campa-g6 | `_h6` | d29399f7bbb4e7874fa062f5e40ce606e298b24791c2da50e4a56e2234702e3f | 06:06 |
| flux-campa-fb-1 | `_k1` | a68bf4cb979c58ac91368673df29459941451cb209e60006cd6b25a57a91046d | 06:43 |
| flux-campa-fb-2 | `_k2` | cac13d9bd3f1feff9242e1c2e13197e7548e1fd4cec17c5e52367417367c89be | 06:44 |
| flux-campa-fb-3 | `_k3` | c42baa28863d0dd4abd30e89076a944cfb8d389b002f683e9f9ec85586bd12c6 | 06:44 |
| flux-campa-fb-4 | `_k4` | a27fff3f74d8e7a614c2047a067802de7591e67136d02137950c733165c27a36 | 06:45 |
| flux-campa-fb-5 | `_k5` | cf9c52a49bf03507eb90987a0e20ecdbf805dea0e5ea9749bb6f21c1805e53b7 | 06:45 |

`instabox-run ls` after the last deletion shows 0 `flux-campa-*` boxes. Created: fb-1..5 01:48, fc 01:49, t1 02:07, g2..g6 02:10 to 02:11 (progress notes; ls clock to the minute). Box-hours of the surviving 12 boxes, created to deleted: about 24.7 (fb) + 3.6 (fc) + 3.0 (t1) + 3.3 + 3.3 + 3.9 x 3 (g2..g6) = about 49.6, plus the six first-launch horizon forks (`w1`, `fa-1..5`, 01:4x to about 02:1x, deletion times not recorded by me) about 2 to 3: **about 52 box-hours, about $3.6 at $0.07 per 8/16 box-hour: an estimate, not a bill.**

### Deviations

1. Worker sa-0-d8be21d7 was interrupted at about 03:22 UTC; this results block, the collection and the deletions were done by a second worker (Collection note above).
2. Horizon shards moved from forks to fresh boxes at 02:15 to 02:17 after measured 59 to 71% steal; t1 was a 13th box for about 4 minutes; the first-launch tarball overwrite incident (progress note 2).
3. **`_c2` was not launched by me.** At takeover (05:04) `flux-campa-fc` had already started `SHARD=_c2` (3 jobs, `runs_c2.log` line `batch start` at 05:03:03, the same second as the `_c1` `ALL_DONE`), i.e. chained after `_c1` on the box. I verified the processes and let it finish (all three runs `rc=0`, 05:26 ALL_DONE); I launched nothing on any box and no shard other than the pre-registered `_c2` ran.
4. Horizon shards are 8, 8, 8, 7, 7, 7 jobs, not 8, 8, 8, 8, 8, 5 (progress note 1).
5. Kappa and control wall times are steal-affected; the kappa and control shards were not relaunched.
6. `t1` was resumed from Paused by Vizier at 05:07 per the handoff; I did not need to resume it myself. Citadel's clock and the box clocks agreed to the minute.
7. I wrote the "Conservation (all parts)" line for the control runs without a number: the summary script prints no drift for part 1.
8. Nothing heavy ran on citadel: only git, box control, `pull`, sha256 and `tar -x`, and the JSON-only summary script.
