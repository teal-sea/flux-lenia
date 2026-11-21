# GPU campaign kit (staged, not run)

Runs the food-selection campaign as `jax.vmap` batches of (seed, arm) on one A100/H100 instead of one
process per run. **Nothing here has been run on a GPU.** The owner's explicit yes is required before any
GPU is created or any Modal function is run. Validation so far: `docs/GPU-BATCH-RUNNER-2026-11-16.md`
(CPU, 300 steps, batch <= 8).

Files: `scripts/gpu_batch.py` (the runner), `scripts/test_gpu_batch.py` (validation), `gpu/manifest.py`
(manifest expansion), `gpu/campaign_manifest.json` (1,800 runs), `gpu/campaign_manifest_species_scan.template.json`
(about 30 species x seeds 1-20 x 4 cells), `gpu/vultr_setup.sh`, `gpu/run_campaign.sh`, `gpu/modal_campaign.py`.

## FP64 requirement: A100 / H100 only

The conservation claim (sum body + sum food at rounding, ~2.5e-16) needs float64 (`jax_enable_x64`).
NVIDIA's L40S, A40 and A16 run FP64 at 1/64 of their FP32 rate, so they are slower than the CPU boxes for this
job. Use A100 (40 or 80 GB; 9.7 TFLOPS FP64, 19.5 with tensor cores) or H100 (34 / 67 TFLOPS). `vultr_setup.sh`
refuses any other card unless `ALLOW_ANY_GPU=1`; `gpu_batch.py --device gpu` refuses to run on a CPU backend.

## Throughput formula

    seconds per run-equivalent = ms_per_batched_step x steps / batch / 1000
    CPU reference: 27.9 ms per step per run  ->  30,000 steps = 836 s per run on one core
    campaign wall seconds     = n_batches x (ms_per_batched_step x steps / 1000 + ~60 s compile/IO)
    speed-up vs one CPU core  = 27.9 x batch / ms_per_batched_step

`gpu_batch.py` prints `ms per batched step` and `ms per run-step` per batch and stores them in `batch_log.json`.
Example only (made-up number, NOT a measurement): if a batch of 150 took 300 ms per batched step, a 30,000-step
batch would take 9,000 s = 2.5 h for 150 runs = 60 s per run-equivalent, 14x one CPU core. The first smoke gives the real number.

## What the first 10 minutes must measure before committing the campaign

`vultr_setup.sh` runs a 1,000-step batch-64 smoke. Then, by hand (each is 1,000 steps, `--seeds 1-N --arms treat`):

    cd /root/fl/code && source /root/fl/venv/bin/activate
    for B in 64 128 256; do
      python scripts/gpu_batch.py --device gpu --species SPECIES_001_OSCILLIS --arms treat --seeds 1-$B \
        --steps 1000 --sample-every 100 --frame-every 1000 --transport per_channel --kappa 3 --food-sense 0 \
        --food 1 --batch $B --outdir /root/fl/smoke_$B
    done
    nvidia-smi --query-gpu=memory.used,memory.total --format=csv

Record: (1) ms per batched step at 64 / 128 / 256 (does it scale ~linearly? if ms per run-step stops falling the card
is saturated, pick that batch); (2) `max_rel_total_drift` (expect ~2.5e-16; anything above 1e-12 means a float32
fallback or a bad kernel, stop); (3) peak memory (the runner prints the XLA estimate; compare with nvidia-smi);
(4) the host-side blob statistics are not the bottleneck: loop time per 100-step chunk vs. time the GPU is busy
(`nvidia-smi dmon`, GPU utilisation should stay above ~90%; if not, raise `--threads`); (5) that the campaign
estimate (formula above) fits the budget. Only then start `run_campaign.sh`.

## Vultr route

1. **Create** (owner's yes first): a Vultr cloud-GPU instance with an A100 or H100, an Ubuntu 22.04/24.04 image that
   ships the NVIDIA driver, SSH key attached. Note the IP and the hourly price; the cost is stated before launch.
2. **Tarball and copy** (on citadel, committed state only):

       git -C /home/thomas/worktrees/flux-lenia-gpu-20261116 archive --format=tar.gz HEAD engine scripts gpu outputs/species requirements.txt -o /tmp/flux-lenia-gpu.tar.gz
       scp /tmp/flux-lenia-gpu.tar.gz root@IP:/root/flux-lenia-gpu.tar.gz
       scp gpu/vultr_setup.sh root@IP:/root/vultr_setup.sh    # the script is also inside the tarball

3. **Setup + smoke**: `ssh root@IP 'bash /root/vultr_setup.sh'` (log: `/root/fl/setup.log`; the last lines print
   `SMOKE batch=64: ... ms per batched step`). Re-running is safe.
4. **Measure** as above. Decide batch size and expected hours.
5. **Run** (survives disconnect):

       ssh root@IP 'cd /root/fl/code && FOOD_SENSE_PILOT=<pilot value> nohup gpu/run_campaign.sh gpu/campaign_manifest.json > /root/fl/out/run.out 2>&1 &'
       ssh root@IP 'cat /root/fl/out/campaign.log'     # START / DONE <id> runs=150 / FAIL / ALL_DONE

   `--species A,B` limits the entries; re-running the same command resumes (DONE batches skipped, partial
   batches redo only the runs without a JSON). `run_campaign.sh` refuses to start if the manifest holds `@PILOT` and no value is given.
6. **Pull**: `rsync -a --partial root@IP:/root/fl/out/food_sensing_2x2/ /home/thomas/flux-lenia-results/food_sensing_2x2/`
   (JSON + frames + per-batch `batch_log.json`). Check `ALL_DONE` and the run count first
   (`find ... -name '*_food1.json' | wc -l` = 1,800).
7. **Destroy** the instance in the Vultr console/API as soon as the rsync is verified. Billing runs until it is destroyed.

## Modal route

1. Owner's yes first. On a machine with Modal credentials (`modal token` set) and `pip install modal`.
2. Look before billing: `python gpu/manifest.py summary gpu/campaign_manifest.json --pilot <v>` (12 batches, 1,800 runs).
3. **Run**: `modal run gpu/modal_campaign.py --manifest gpu/campaign_manifest.json --pilot <pilot value>`
   (`--only SPECIES_001_OSCILLIS` for one species; `--dry-run` expands without calling Modal functions, but it still starts
   an app, so treat it as a `modal run`). One A100-80GB container per (species, cell), mapped in parallel, timeout 3 h
   per container (a 30,000-step batch must finish inside it: check that the smoke's ms per batched step x 30,000 is
   under 10,800 s at the chosen batch; if not, split the seeds range into several manifest entries or raise the timeout in
   `modal_campaign.py`). Results are written to the Modal Volume
   `flux-lenia-gpu-out`, and re-running the same command resumes.
4. **Pull**: `modal volume get flux-lenia-gpu-out /food_sensing_2x2 ./out/`.
5. Nothing to destroy; stop billing by letting the run finish (`modal app list`, `modal app stop` if aborting).
   Delete the volume when pulled: `modal volume delete flux-lenia-gpu-out`.

## Memory and batch size

`gpu_batch.py` prints the per-element state (1.70 MB: A 3 + G 9 + F 1 channels of 128x128 float64) and the XLA
compiled argument+output+temp size for the chosen batch, and shrinks `--batch` automatically when that exceeds 85% of
the device memory. See the doc for the measured per-element figure. `--estimate-only` compiles and prints without running.

## Changing the campaign

Edit the manifest (species, cells, seeds, arms, steps); `food_sense: "@PILOT"` is the owner's pilot value, supplied at
launch (`--pilot` or `FOOD_SENSE_PILOT`) and never defaulted. Every invocation is one (species, cell): all static jit
arguments (kappa, food_sense, transport, food, steps) are constant inside it, the batch axis is (seed, arm).
