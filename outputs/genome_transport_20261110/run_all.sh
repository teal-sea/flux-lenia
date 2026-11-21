#!/bin/bash
# 45 no-food runs, per-channel genome transport, 8 concurrent, one thread each.
cd "$(dirname "$0")/../.."
exec python3 scripts/run_batch.py outputs/genome_transport_20261110 per_channel 8
