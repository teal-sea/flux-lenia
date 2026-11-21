#!/usr/bin/env python3
"""Push each box's shard + runner to the InstaBox L4 fleet and launch it detached.
Reads live/gpu_fleet.txt (name<TAB>id, line i -> box{i:02d}.tsv) and campaign_gpu/shards/.
Idempotent-ish: re-running re-pushes and relaunches; run_shard.sh skips DONE batches and
gpu_batch skips existing JSONs, so a relaunch never duplicates completed runs.
"""
from __future__ import annotations
import subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IBR = "/home/thomas/bin/instabox-run"
FLEET = Path("/home/thomas/work/flux-gpu-20261116/live/gpu_fleet.txt")
SHARDS = ROOT / "campaign_gpu" / "shards"
RUNNER = ROOT / "scripts" / "run_shard.sh"


def run(args, timeout):
    return subprocess.run(args, capture_output=True, text=True, timeout=timeout)


def main():
    boxes = [l.split("\t")[0] for l in FLEET.read_text().splitlines() if l.strip()]
    print(f"fleet: {len(boxes)} boxes")
    ok = 0
    for i, name in enumerate(boxes, 1):
        tsv = SHARDS / f"box{i:02d}.tsv"
        if not tsv.exists():
            print(f"  {name}: MISSING {tsv}"); continue
        r = run([IBR, "cp", str(RUNNER), f"{name}:/data/fl/code/scripts/run_shard.sh"], 120)
        if r.returncode != 0:
            print(f"  {name}: cp runner failed {r.stderr.strip()[:120]}"); continue
        r = run([IBR, "cp", str(tsv), f"{name}:/data/fl/shard.tsv"], 120)
        if r.returncode != 0:
            print(f"  {name}: cp shard failed {r.stderr.strip()[:120]}"); continue
        cmd = ("chmod +x /data/fl/code/scripts/run_shard.sh; cd /data/fl && "
               "setsid nohup bash code/scripts/run_shard.sh /data/fl/shard.tsv "
               "> /data/fl/shard.nohup 2>&1 < /dev/null & sleep 3; "
               "head -1 /data/fl/out/campaign.log 2>/dev/null; echo LAUNCHED")
        r = run([IBR, "exec", name, "--timeout", "60", "--", cmd], 90)
        launched = "LAUNCHED" in r.stdout
        print(f"  {name}: {'LAUNCHED' if launched else 'CHECK'} {r.stdout.strip()[:80]} {r.stderr.strip()[:80]}")
        ok += launched
    print(f"launched {ok}/{len(boxes)}")


if __name__ == "__main__":
    main()