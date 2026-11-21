# GPU batch runner: design and CPU validation (2026-11-16)

Status: runner and launch kits written and validated on CPU at <= 300 steps, batch <= 8. **No GPU was created,
no Modal function was run, and nothing on a GPU has been measured.** Launch needs the owner's explicit yes
(`gpu/README.md`).

## What it is

`scripts/gpu_batch.py` runs many (seed, arm) food-selection runs of one (species, cell) as one `jax.vmap` over
`nu.rollout` (`nu.rollout_logged` when `--food-sense` is given), chunked by `--sample-every` steps. Initial states
come from `food_selection.build_run`, a function extracted from `food_selection.main()` (the only change to
that script). Metrics are the unchanged `food_selection.measure()` on host copies of each sample, in a thread pool
while the device already runs the next chunk; `sat_frac` pairs are vmapped on device. Per-run JSON has the same
keys in the same order as `food_selection.py`; `wall_seconds` = batch loop wall / batch size. No engine file was edited:
`vmap` over `nu.rollout` works as is (static `Config`, `Food`, `n_steps` stay static; only `A, G, F` are mapped; light, brain
and kernel bank are shared and asserted identical across the batch).

## Validation (citadel CPU, 1 core via taskset, `jax 0.11.1`, float64, `XLA_FLAGS` as instructed)

Everything below: 300 steps, sample every 100, batch <= 8.

0. **Refactor unchanged.** `food_selection.py OSCILLIS 1 treat 1 300 DIR per_channel 3 0` and the 7-argument form
   (`... per_channel`) before and after the refactor: JSON identical except `wall_seconds`, frames npz identical (values, dtypes, keys).
1. **Batch of 1 vs `food_selection.py`** (OSCILLIS, seed 1, treat, food on, per_channel, kappa 3, food_sense 0): JSON
   (60 leaves, every series of every metric, `t`, `final`, `max_rel_total_drift`, `share_A_*`, params) **bit-identical**;
   frames (float32 body/ancestry/food at t=0 and 300) identical. In-process final **A, G, F arrays: bit-identical**; all 12 `measure()` metrics identical.
   Same for the 7-argument form (food_sense absent, 49 leaves, float64 frames): bit-identical.
2. **Batch of 4 (seeds 1-4, treat) vs four batches of 1:** per element A, G, F and the whole JSON **bit-identical**.
   So here vmap changed no reduction order on CPU. (On GPU, batched `dot_general`/FFT kernels may differ in the last bits;
   per-element drift stays the check there, `test_gpu_batch.py arrays/batch4` can be run on the GPU box at the same sizes.)
3. **Conservation, three species, batch 3 (the three arms), kappa 3:**

   | species | food on: max_rel_total_drift (sum body + sum food) per arm | food off: max rel dS of sum(A_tot*G), functional rows / tag | rel dM |
   |---|---|---|---|
   | OSCILLIS | 2.46e-16 x3 | 6.1e-17, 1.2e-16, 6.1e-17 / 9.5e-17, 3.3e-17, 2.2e-17 | <= 1.2e-16 |
   | MITOSA | 2.46e-16 x3 | 2.9e-17, 6.1e-17, 1.2e-16 / 6.3e-17, 1.2e-17, 3.6e-17 | <= 1.2e-16 |
   | VAGRANT | 2.46e-16 x3 | 3.4e-17, 1.2e-16, 3.1e-17 / 5.5e-17, 3.4e-17, 1.7e-17 | 0 |

   (sum(A_tot*G) is conserved only with food off, since uptake adds mass to a cell without changing its genome; measured at the end state.)
4. **kappa 0 / food_sense 0 equals the pre-change engine** (hash approach of `scripts/test_repulsion.py`: sha256 of (A, G, F) after 300 steps,
   food on, per_channel; pre-change engine = `git archive b2cdd8b engine`, the commit before `repulsion_kappa` was added): for all three species the hash of
   the current unbatched path, the batch-of-1 and each element of a batch of 3 equals the pre-change hash
   (OSCILLIS 928fb7d7..., MITOSA 17e67633..., VAGRANT 0388d93c...).
5. **Resume:** a 4-run invocation at batch 2, then deleting 2 JSONs and re-running the same command, redid only the 2 missing runs
   (`batch_log.json` has both entries).

Reproduce: `JAX_PLATFORMS=cpu XLA_FLAGS="--xla_cpu_multi_thread_eigen=false intra_op_parallelism_threads=1" python scripts/test_gpu_batch.py {arrays|batch4|species|hash REF_ENGINE_ROOT|cli-compare A B TAG}`.

## Memory estimate

Per element state (A 3 + G 9 + F 1 channels, 128x128, float64): **1.70 MB**. XLA compiled argument + output + temp size
(CPU backend, one 100-step chunk, `memory_analysis`): batch 2: 26.57 MB/element, 4: 26.00, 8: 25.71, i.e. linear, about **26 MB per element**
(about 3.9 GB at batch 150, about 40 GB at batch 1,500 by extrapolation). The GPU backend's buffer assignment and cuFFT workspaces differ, so
this is an estimate; `gpu_batch.py` recomputes it from the actual device compile, prints it, and shrinks `--batch` to fit 85% of device memory.
An 80 GB card is nowhere near the limit at batch 150; the batch is limited by throughput saturation, not memory. The smoke measures it.

## CPU timing (not a GPU prediction)

On one core, batched CPU: 51-56 ms per run-step (the single-run CLI measured 14.1 s / 300 steps = 47 ms incl. the 5 measure calls, on a loaded host
at the time). The CPU has no vmap gain; the claim to be tested on the GPU is the throughput formula in `gpu/README.md`.

## Deviations and notes

- The `modal` and `gpu-rental-runs` skills named in the brief do not exist on this profile; the Modal syntax was taken from the installed Modal 1.6.3
  API plus the `modal-browser-suites` skill, and the module was import-checked (no network, no app run). Vultr conventions come from the brief only.
- Frames: `--frame-every` (default 1000) writes frames at every multiple plus t=0 and the last step; `food_selection.py` uses a fixed set, so
  frame sets differ unless `--frame-every` is chosen to match (done in the comparisons above).
- Blob statistics are computed at every sample for every element (same as the CLI), on the host. Throughput on the GPU box must show the host side keeps up.
- Remaining batch of a resumed invocation can have a different size, which recompiles once.
- The `@PILOT` food_sense placeholder must be supplied by the owner at launch.

## run_campaign.sh rehearsal (CPU, `DEVICE=cpu`, 1 manifest entry, 2 runs, 100 steps)
Sentinels `START`, `DONE <id> runs=2`, `ALL_DONE` written; a second invocation printed `skip ... (DONE)` and `ALL_DONE`. A first attempt with a broken
interpreter wrote `FAIL ... rc=1` and `FINISHED_WITH_FAILURES` with no `ALL_DONE` (the failure path works). `vultr_setup.sh` and `modal_campaign.py` could only
be syntax-checked (`bash -n`, import of the Modal module with its image definition): they need the GPU box / Modal account.
