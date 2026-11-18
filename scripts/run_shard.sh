#!/usr/bin/env bash
# Run a pre-sharded campaign TSV (id<TAB>outrel<TAB>runs<TAB>gpu_batch-args), one gpu_batch.py call per line.
# Resumable: exact batch keys are skipped; old id-only DONE lines are not trusted.
# A half-finished batch redoes only runs without a JSON (gpu_batch skip-existing).
# Used by the InstaBox L4 GPU fleet (2026-11-18) to run disjoint shards of the horizon + species scan.
set -uo pipefail
FL=${FL:-/data/fl}
TSV=${1:?usage: run_shard.sh SHARD.tsv}
cd "$FL/code"
PY="$FL/venv/bin/python"
OUT="$FL/out"; LOG="$OUT/campaign.log"; mkdir -p "$OUT/logs"
export PYTHONUNBUFFERED=1
export XLA_FLAGS="--xla_gpu_enable_triton_gemm=false ${XLA_FLAGS:-}"
n=$(wc -l < "$TSV"); echo "$(date -u +%FT%TZ) SHARD $TSV: $n batches" | tee -a "$LOG"
fail=0
while IFS=$'\t' read -r id outrel runs args; do
  [ -z "$id" ] && continue
  # Include output tree and arguments, not just the species-cell id. Different
  # experiments and seed ranges may share an id on the same machine.
  key=$(printf '%s\t%s\t%s\t%s' "$id" "$outrel" "$runs" "$args" | sha256sum)
  key=${key%% *}
  if grep -Fq " DONE batch=$key " "$LOG" 2>/dev/null; then echo "skip $id batch=$key (DONE)"; continue; fi
  echo "$(date -u +%FT%TZ) START batch=$key id=$id out=$outrel" | tee -a "$LOG"
  # shellcheck disable=SC2086
  "$PY" scripts/gpu_batch.py --device gpu $args --outdir "$OUT/$outrel" >> "$OUT/logs/$id-$key.log" 2>&1
  rc=$?
  have=$(ls "$OUT/$outrel"/*_food[01].json 2>/dev/null | wc -l)
  if [ "$rc" = 0 ] && [ "$have" -ge "$runs" ]; then
    echo "$(date -u +%FT%TZ) DONE batch=$key id=$id out=$outrel runs=$have" | tee -a "$LOG"
  else
    echo "$(date -u +%FT%TZ) FAIL batch=$key id=$id out=$outrel rc=$rc have=$have want=$runs (see logs/$id-$key.log)" | tee -a "$LOG"; fail=1
  fi
done < "$TSV"
if [ "$fail" = 0 ]; then echo "$(date -u +%FT%TZ) ALL_DONE" | tee -a "$LOG"; else echo "$(date -u +%FT%TZ) FINISHED_WITH_FAILURES (no ALL_DONE)" | tee -a "$LOG"; exit 1; fi