#!/usr/bin/env python3
"""Collector + spend-cap enforcer for the InstaBox L4 GPU flux-lenia campaign (2026-11-18).
Idempotent, safe from cron. Each tick:
  1. Query each live box (ALL_DONE / FINISHED_WITH_FAILURES / running, JSON count).
  2. Terminal boxes: tar /data/fl/out -> sha256 -> instabox-run pull -> verify -> extract into
     outputs/ (never overwrite an existing result JSON) -> rm the box. Record deleted_at.
  3. Compute real spend from per-box created_at/deleted_at at $0.765/GPU-h. If >= cap, pull and
     delete every remaining box (stop the burn) and mark the campaign stopped.
  4. git add/commit/push results.
  5. When horizon>=900 and scan>=7200 and all boxes pulled: run the two summary scripts, commit,
     print GPU_CAMPAIGN_ALL_DONE.
State: campaign_gpu/gpu_boxes.json. Log: /home/thomas/work/flux-gpu-20261116/live/gpu_collector.log
"""
from __future__ import annotations
import json, os, subprocess, sys, tarfile, hashlib, time
from pathlib import Path

ROOT = Path("/home/thomas/worktrees/flux-lenia-cpu-20261117")
IBR = "/home/thomas/bin/instabox-run"
LIVE = Path("/home/thomas/work/flux-gpu-20261116/live")
STATE = ROOT / "campaign_gpu" / "gpu_boxes.json"
LOG = LIVE / "gpu_collector.log"
H = ROOT / "outputs" / "horizon300k_20261117"
S = ROOT / "outputs" / "species_scan_20261117"
RATE = 0.765


def say(m):
    line = time.strftime("%FT%TZ", time.gmtime()) + " " + m
    print(line)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def run(args, timeout):
    return subprocess.run(args, capture_output=True, text=True, timeout=timeout)


def now():
    return time.time()


def iso(ts):
    return time.strftime("%FT%TZ", time.gmtime(ts))


def parse_iso(s):
    return time.mktime(time.strptime(s, "%Y-%m-%dT%H:%M:%SZ")) - time.timezone


def box_state(name):
    try:
        r = run([IBR, "exec", name, "--timeout", "60", "--",
                 "grep -c ALL_DONE /data/fl/out/campaign.log 2>/dev/null; "
                 "grep -c FINISHED_WITH_FAILURES /data/fl/out/campaign.log 2>/dev/null; "
                 "find /data/fl/out -name '*_food1.json' 2>/dev/null | wc -l"], 90)
    except Exception as e:
        return None
    nums = [x for x in r.stdout.split() if x.isdigit()]
    if r.returncode != 0 or len(nums) < 3:
        return None
    return {"all_done": int(nums[0]) > 0, "failed": int(nums[1]) > 0, "json": int(nums[2])}


def pull_box(name, b):
    r = run([IBR, "exec", name, "--timeout", "300", "--",
             "cd /data/fl && rm -f out.tar && tar cf out.tar out && sha256sum out.tar"], 360)
    if r.returncode != 0 or not r.stdout.strip():
        say(f"{name}: tar failed {r.stderr.strip()[:160]}"); return False
    box_sha = r.stdout.split()[0]
    dst = LIVE / "pulled" / f"{name}.tar"
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        dst.unlink()
    r = run([IBR, "pull", name, "/data/fl/out.tar", str(dst)], 1200)
    if r.returncode != 0 or not dst.exists():
        say(f"{name}: pull failed rc={r.returncode} {r.stderr.strip()[:160]}"); return False
    h = hashlib.sha256()
    with open(dst, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    if h.hexdigest() != box_sha:
        say(f"{name}: sha256 MISMATCH; box kept"); return False
    outroot = ROOT / "outputs"
    with tarfile.open(dst) as t:
        for m in t.getmembers():
            if m.name.startswith("out/") and ".." not in m.name:
                m.name = m.name[4:]
                if not m.name:
                    continue
                tgt = outroot / m.name
                if m.isfile() and tgt.exists() and not m.name.endswith(".log"):
                    continue
                t.extract(m, outroot, filter="data")
    r = run([IBR, "rm", "--yes", name], 120)
    b["status"] = "pulled"
    b["sha256"] = box_sha
    b["deleted_at"] = iso(now())
    b["deleted"] = r.returncode == 0
    say(f"{name}: pulled {b.get('json_on_box', '?')} runs, sha {box_sha[:12]} verified, rm rc={r.returncode}")
    return True


def spend(st):
    total = 0.0
    for name, b in st["boxes"].items():
        c = parse_iso(b["created_at"])
        d = parse_iso(b["deleted_at"]) if b.get("deleted_at") else now()
        total += max(0.0, (d - c)) / 3600 * RATE
    return total


def main():
    st = json.load(open(STATE))
    cap = st.get("cap_usd", 95)
    # 1+2: query and pull terminal boxes
    for name, b in st["boxes"].items():
        if b.get("status") in ("pulled", "deleted"):
            continue
        qs = box_state(name)
        if qs is None:
            say(f"{name}: not queryable"); continue
        b["json_on_box"] = qs["json"]
        if qs["all_done"] or qs["failed"]:
            b["terminal"] = "ALL_DONE" if qs["all_done"] else "FINISHED_WITH_FAILURES"
            pull_box(name, b)
    # 3: spend cap
    sp = spend(st)
    st["spend_usd"] = round(sp, 2)
    if sp >= cap and not st.get("stopped"):
        say(f"SPEND CAP ${sp:.2f} >= ${cap}: pulling+deleting all remaining boxes")
        for name, b in st["boxes"].items():
            if b.get("status") not in ("pulled", "deleted"):
                pull_box(name, b)
                if b.get("status") != "pulled":
                    run([IBR, "rm", "--yes", name], 120)
                    b["status"] = "deleted"; b["deleted_at"] = iso(now())
        st["stopped"] = True
        st["spend_usd"] = round(spend(st), 2)
    json.dump(st, open(STATE, "w"), indent=1)
    # 4: git
    subprocess.run(["git", "add", "outputs/horizon300k_20261117", "outputs/species_scan_20261117",
                    "campaign_gpu"], cwd=ROOT, capture_output=True)
    diff = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT)
    n_h = len(list(H.rglob("*_food1.json")))
    n_s = len(list(S.rglob("*_food1.json")))
    if diff.returncode != 0:
        subprocess.run(["git", "commit", "-q", "-m",
                        f"GPU campaign results: horizon {n_h}/900, species scan {n_s}/7200"],
                       cwd=ROOT, capture_output=True)
        subprocess.run(["git", "push", "-q", "origin", "vizier/cpu-campaign-20261117"],
                       cwd=ROOT, capture_output=True)
    # 5: completion
    pulled = sum(b.get("status") in ("pulled", "deleted") for b in st["boxes"].values())
    total = len(st["boxes"])
    say(f"horizon {n_h}/900 scan {n_s}/7200 | boxes pulled {pulled}/{total} | spend ${st['spend_usd']:.2f}/${cap}")
    if n_h >= 900 and n_s >= 7200 and pulled == total and not st.get("summarized"):
        for script in ("horizon300k_summary.py", "species_scan_summary.py"):
            r = subprocess.run([sys.executable, str(ROOT / "scripts" / script)], cwd=ROOT,
                               capture_output=True, text=True, timeout=600)
            say(f"{script} rc={r.returncode} {r.stdout.strip()[-200:]}")
        subprocess.run(["git", "add", "-A", "outputs"], cwd=ROOT, capture_output=True)
        subprocess.run(["git", "commit", "-q", "-m", "GPU campaign summaries: horizon + species scan complete"],
                       cwd=ROOT, capture_output=True)
        subprocess.run(["git", "push", "-q", "origin", "vizier/cpu-campaign-20261117"],
                       cwd=ROOT, capture_output=True)
        st["summarized"] = True
        json.dump(st, open(STATE, "w"), indent=1)
        say("GPU_CAMPAIGN_ALL_DONE")
    return 0


if __name__ == "__main__":
    sys.exit(main())