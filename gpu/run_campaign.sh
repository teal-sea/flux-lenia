#!/usr/bin/env bash
# Run every (species, cell) batch of a campaign manifest, one gpu_batch.py call each.
#   gpu/run_campaign.sh [MANIFEST] [--pilot X] [--species A,B]      (FOOD_SENSE_PILOT=X also works)
# DEVICE=cpu is for dry rehearsals only (default gpu; gpu_batch refuses a CPU backend when asked for gpu).
# Output: /root/fl/out/<experiment>/<species>_fs<f>_k<k>_<transport>/ (JSON + frames + batch_log.json);
# sentinels in /root/fl/out/campaign.log (timestamp first):  START id / DONE id runs=N / FAIL id rc=R / ALL_DONE.
# Resumable: DONE batches are skipped; a half-finished batch redoes only runs without a JSON.
set -uo pipefail
FL=${FL:-/root/fl}
MANIFEST=${1:-gpu/campaign_manifest.json}; shift || true
cd "$FL/code"
PY="$FL/venv/bin/python"
OUT="$FL/out"; LOG="$OUT/campaign.log"; mkdir -p "$OUT/logs"
export PYTHONUNBUFFERED=1
# expand first so a missing pilot value fails before anything runs
"$PY" -I gpu/manifest.py expand "$MANIFEST" "$@" > "$OUT/expanded.tsv" || { echo "manifest expansion failed" | tee -a "$LOG"; exit 2; }
n=$(wc -l < "$OUT/expanded.tsv"); echo "$(date -u +%FT%TZ) CAMPAIGN $MANIFEST: $n batches" | tee -a "$LOG"
fail=0
while IFS=$'\t' read -r id outrel runs args; do
  if grep -q " DONE $id runs=" "$LOG" 2>/dev/null; then echo "skip $id (DONE)"; continue; fi
  echo "$(date -u +%FT%TZ) START $id" | tee -a "$LOG"
  # shellcheck disable=SC2086
  "$PY" scripts/gpu_batch.py --device "${DEVICE:-gpu}" $args --outdir "$OUT/$outrel" >> "$OUT/logs/$id.log" 2>&1
  rc=$?
  have=$(ls "$OUT/$outrel"/*_food[01].json 2>/dev/null | wc -l)
  if [ "$rc" = 0 ] && [ "$have" = "$runs" ]; then
    echo "$(date -u +%FT%TZ) DONE $id runs=$have" | tee -a "$LOG"
  else
    echo "$(date -u +%FT%TZ) FAIL $id rc=$rc have=$have want=$runs (see logs/$id.log)" | tee -a "$LOG"; fail=1
  fi
done < "$OUT/expanded.tsv"
if [ "$fail" = 0 ]; then echo "$(date -u +%FT%TZ) ALL_DONE" | tee -a "$LOG"; else echo "$(date -u +%FT%TZ) FINISHED_WITH_FAILURES (no ALL_DONE)" | tee -a "$LOG"; exit 1; fi
