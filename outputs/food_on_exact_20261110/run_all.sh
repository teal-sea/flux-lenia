#!/bin/bash
# 45 food-on runs, per-channel genome transport, 8 concurrent, one thread each.
cd "$(dirname "$0")/../.."
exec python3 scripts/run_batch.py outputs/food_on_exact_20261110 per_channel 8
