"""Modal route for the GPU campaign: one A100-80GB container per (species, cell) batch.

NOT RUN by whoever wrote it: `modal run` bills. The owner's explicit yes comes first
(gpu/README.md, "Modal route").

  modal run gpu/modal_campaign.py --manifest gpu/campaign_manifest.json --pilot 0.5 [--only SPECIES_001_OSCILLIS] [--dry-run]
  modal volume get flux-lenia-gpu-out /food_sensing_2x2 ./out/        # pull results to citadel

Each map item runs scripts/gpu_batch.py for one manifest entry and writes into the Modal Volume
under /out/<experiment>/<id>/. The function is resumable: gpu_batch skips runs whose JSON exists
in the volume, so re-running the same command after a failure only does the missing runs.
Nothing here imports jax locally; the local entrypoint only expands the manifest.
"""
from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

import modal

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
for p in (str(HERE), "/app/gpu"):
    if p not in sys.path:
        sys.path.insert(0, p)
from manifest import expand  # noqa: E402

VOLUME = "flux-lenia-gpu-out"
vol = modal.Volume.from_name(VOLUME, create_if_missing=True)

# same pins as gpu/vultr_setup.sh: jax[cuda12]==0.11.1 (the version of the CPU results), numpy 2.5.2, scipy 1.18.1
image = (
    modal.Image.debian_slim(python_version="3.13")
    .pip_install("jax[cuda12]==0.11.1", "numpy==2.5.2", "scipy==1.18.1")
    .env({"JAX_ENABLE_X64": "1", "PYTHONUNBUFFERED": "1"})
    .add_local_dir(str(REPO / "engine"), "/app/engine", ignore=["__pycache__"])
    .add_local_dir(str(REPO / "scripts"), "/app/scripts", ignore=["__pycache__"])
    .add_local_dir(str(REPO / "outputs" / "species"), "/app/outputs/species")
    .add_local_dir(str(REPO / "gpu"), "/app/gpu", ignore=["__pycache__"])
)

app = modal.App("flux-lenia-gpu-campaign", image=image)


@app.function(gpu="A100-80GB", timeout=6 * 3600, volumes={"/out": vol}, cpu=8, memory=32768)
def run_entry(entry: dict) -> dict:
    """One (species, cell) batch. entry: an element of manifest.expand()."""
    vol.reload()
    outdir = f"/out/{entry['outdir']}"
    cmd = f"{sys.executable} /app/scripts/gpu_batch.py --device gpu {entry['args']} --outdir {outdir}"
    t0 = time.time()
    print(f"START {entry['id']}: {cmd}", flush=True)
    rc = subprocess.run(cmd.split(), cwd="/app").returncode
    vol.commit()
    have = len(list(Path(outdir).glob("*_food[01].json")))
    res = {"id": entry["id"], "rc": rc, "have": have, "want": entry["runs"], "seconds": time.time() - t0,
           "ok": rc == 0 and have == entry["runs"]}
    print(("DONE " if res["ok"] else "FAIL ") + str(res), flush=True)
    return res


@app.local_entrypoint()
def main(manifest: str = "gpu/campaign_manifest.json", pilot: str = "", only: str = "", dry_run: bool = False):
    entries = expand(manifest, pilot or None, only.split(",") if only else None)
    print(f"{len(entries)} batches, {sum(e['runs'] for e in entries)} runs, one A100-80GB container each")
    if dry_run:
        for e in entries:
            print(" ", e["id"], e["args"])
        return
    results = list(run_entry.map(entries, order_outputs=False, return_exceptions=True))
    bad = [r for r in results if not (isinstance(r, dict) and r.get("ok"))]
    for r in results:
        print(r)
    exp = entries[0]["experiment"] if entries else "EXPERIMENT"
    print("ALL_DONE" if not bad else f"{len(bad)} batches failed (re-run the same command to resume)")
    print(f"pull: modal volume get {VOLUME} /{exp} ./out/")
