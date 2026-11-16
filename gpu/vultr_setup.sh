#!/usr/bin/env bash
# Fresh Vultr GPU instance (Ubuntu 22.04/24.04, NVIDIA driver image, A100 or H100) -> ready to run.
# Idempotent: safe to re-run. Log: /root/fl/setup.log.
# Operator has already scp'd the code tarball (default /root/flux-lenia-gpu.tar.gz, see gpu/README.md).
set -euo pipefail
FL=${FL:-/root/fl}
TARBALL=${TARBALL:-/root/flux-lenia-gpu.tar.gz}
mkdir -p "$FL" "$FL/out"
exec > >(tee -a "$FL/setup.log") 2>&1
echo "=== vultr_setup $(date -u +%FT%TZ) ==="

# 0. the GPU must do float64 at full rate: A100 / H100 only (L40S, A40, A16 run FP64 at 1/64 rate)
command -v nvidia-smi >/dev/null || { echo "FATAL: no nvidia-smi: this is not a GPU image with the driver"; exit 1; }
GPU=$(nvidia-smi --query-gpu=name,memory.total --format=csv,noheader | head -1)
echo "GPU: $GPU"
if ! echo "$GPU" | grep -Eqi 'A100|H100|H200|B200|GH200' && [ "${ALLOW_ANY_GPU:-0}" != 1 ]; then
  echo "FATAL: '$GPU' is not an FP64-class card (A100/H100). Destroy this instance, or set ALLOW_ANY_GPU=1 to override."; exit 1
fi

# 1. uv
export PATH="$HOME/.local/bin:$PATH"
command -v uv >/dev/null || { apt-get update -qq && apt-get install -y -qq curl ca-certificates tar rsync >/dev/null; curl -LsSf https://astral.sh/uv/install.sh | sh; }
uv --version

# 2. python 3.13 venv
[ -x "$FL/venv/bin/python" ] || uv venv --python 3.13 "$FL/venv"
PY="$FL/venv/bin/python"

# 3. jax[cuda12] as close to 0.11.1 as the CUDA wheels allow, with the repo's numpy/scipy pins
if ! "$PY" -c 'import jax, jaxlib' 2>/dev/null; then
  ok=0
  for v in 0.11.1 0.11.0 0.10.2 0.10.1; do
    echo "trying jax[cuda12]==$v"
    if uv pip install --python "$PY" "jax[cuda12]==$v" "numpy==2.5.2" "scipy==1.18.1"; then ok=1; break; fi
  done
  [ "$ok" = 1 ] || { echo "FATAL: no jax[cuda12] wheel installed"; exit 1; }
fi
"$PY" -c 'import jax, numpy, scipy; print("jax", jax.__version__, "numpy", numpy.__version__, "scipy", scipy.__version__)'
[ "$("$PY" -c 'import jax; print(jax.__version__)')" = "0.11.1" ] || echo "NOTE: jax is not 0.11.1; record this in the results (summary tables were produced with 0.11.1 on CPU)"

# 4. code
if [ ! -d "$FL/code/engine" ]; then
  [ -f "$TARBALL" ] || { echo "FATAL: $TARBALL missing: scp the tarball first (gpu/README.md step 2)"; exit 1; }
  mkdir -p "$FL/code" && tar -xzf "$TARBALL" -C "$FL/code"
fi
cd "$FL/code"
ls engine/neural_field.py scripts/gpu_batch.py gpu/manifest.py outputs/species >/dev/null

# 5. device check
JAX_ENABLE_X64=1 "$PY" -c 'import jax; d=jax.devices(); print(d); assert d[0].platform in ("gpu","cuda"), d'

# 6. smoke: 1,000 steps, batch 64, prints ms per batched step (the number the campaign is sized from)
rm -rf "$FL/smoke"
"$PY" scripts/gpu_batch.py --device gpu --species SPECIES_001_OSCILLIS --arms treat --seeds 1-64 \
  --steps 1000 --sample-every 100 --frame-every 1000 --transport per_channel --kappa 3 --food-sense 0 \
  --food 1 --batch 64 --outdir "$FL/smoke"
"$PY" - <<PYEOF
import json
e = json.load(open("$FL/smoke/batch_log.json"))[-1]
print(f"SMOKE batch=64: {e['ms_per_batched_step']:.2f} ms per batched step, "
      f"{e['ms_per_batched_step']/64:.3f} ms per run-step (CPU reference 27.9), max total drift {e['max_rel_total_drift']:.2e}")
PYEOF
nvidia-smi --query-gpu=memory.used,memory.total --format=csv
echo "=== setup OK $(date -u +%FT%TZ) ==="
