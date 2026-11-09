#!/bin/bash
# Run one shard of jobs.txt (lines where (line_number - 1) % NSHARDS == SHARD), 8 at a time,
# one thread each. Usage: run_shard.sh SHARD NSHARDS
set -u
cd "$(dirname "$0")/../.."
export XLA_FLAGS="--xla_cpu_multi_thread_eigen=false intra_op_parallelism_threads=1"
OUT=outputs/food_selection_20261109
PY=${PY:-.venv/bin/python}
awk -v s="$1" -v n="$2" '(NR-1)%n==s' $OUT/jobs.txt > $OUT/shard_$1.txt
xargs -P 8 -L 1 bash -c "\$0 scripts/food_selection.py \$1 \$2 \$3 \$4 30000 $OUT >> $OUT/runs_shard_$1.log 2>&1 || echo FAIL \$1 \$2 \$3 \$4 >> $OUT/runs_shard_$1.log" "$PY" < $OUT/shard_$1.txt
echo ALL_DONE >> $OUT/runs_shard_$1.log
