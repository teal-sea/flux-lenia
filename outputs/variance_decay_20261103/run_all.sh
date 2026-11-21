#!/bin/bash
# Runs all 18 jobs, 9 at a time, one thread each.
cd "$(dirname "$0")/../.."
export XLA_FLAGS="--xla_cpu_multi_thread_eigen=false intra_op_parallelism_threads=1"
OUT=outputs/variance_decay_20261103
PY=${PY:-$HOME/venvs/flux-lenia-20261103/bin/python}
xargs -P 9 -L 1 bash -c "\$0 scripts/variance_decay.py \$1 \$2 \$3 20000 $OUT >> $OUT/runs.log 2>&1 || echo FAIL \$1 \$2 \$3 >> $OUT/runs.log" "$PY" < $OUT/jobs.txt
echo ALL_DONE >> $OUT/runs.log
