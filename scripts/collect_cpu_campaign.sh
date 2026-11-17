#!/bin/bash
# Collector for the CPU campaign (docs/HORIZON-300K-GPU-2026-11-16.md and docs/SPECIES-SCAN-2026-11-16.md, execution notes).
# Idempotent, never deletes results; safe from cron (absolute paths only). Exit 0 on a quiet tick.
#   /home/thomas/worktrees/flux-lenia-cpu-20261117/scripts/collect_cpu_campaign.sh
# 1. rsync /root/fl/out/ from Vultr box 1 (horizon) and box 2 (scan) into outputs/horizon300k_20261117/ and
#    outputs/species_scan_20261117/ (result files only once 2 min old, never overwritten; logs refreshed).
# 2. For each InstaBox box in outputs/species_scan_20261117/instabox_boxes.json that shows ALL_DONE and is not
#    pulled: tar on the box, sha256, instabox-run pull, compare, extract, rm --yes the box, record it.
# 3. git add / commit / push if anything changed.  4. One status line per source; CAMPAIGN_ALL_DONE when both complete.
export HOME=/home/thomas
export PATH=/home/thomas/bin:/home/thomas/.local/bin:/usr/local/bin:/usr/bin:/bin
WT=/home/thomas/worktrees/flux-lenia-cpu-20261117
LIVE=/home/thomas/work/flux-gpu-20261116/live
H=$WT/outputs/horizon300k_20261117
S=$WT/outputs/species_scan_20261117
BOXES=$S/instabox_boxes.json
IBR=/home/thomas/bin/instabox-run
LOG=/home/thomas/work/flux-cpu-20261117/collector.log
exec 9>/home/thomas/work/flux-cpu-20261117/collector.lock
flock -n 9 || { echo "collector already running"; exit 0; }
mkdir -p "$H" "$S" "$(dirname "$LOG")"
say() { echo "$(date -u +%FT%TZ) $*" | tee -a "$LOG"; }
SSH=(ssh -i "$LIVE/gpu_key" -o BatchMode=yes -o StrictHostKeyChecking=accept-new -o UserKnownHostsFile="$LIVE/known_hosts_cpu" -o ConnectTimeout=20 -o ServerAliveInterval=15 -o LogLevel=ERROR)

vultr_pull() {   # N destdir
  local n=$1 dest=$2 ip
  ip=$(python3 -c "import json;print(json.load(open('$LIVE/instance-cpu-$n.json'))['main_ip'])")
  # result files: only those not modified in the last 2 minutes, never overwritten
  timeout 120 "${SSH[@]}" "root@$ip" "cd /root/fl/out && find . -type f \( -name '*.json' -o -name '*.npz' \) -mmin +2" 2>/dev/null > "$dest/.files_$n.txt" \
    || { say "box $n: ssh failed (file list)"; return 1; }
  timeout 1500 rsync -a --partial --ignore-existing --files-from="$dest/.files_$n.txt" -e "${SSH[*]}" "root@$ip:/root/fl/out/" "$dest/" 2>>"$LOG" \
    || say "box $n: rsync results rc=$?"
  # run and shard logs: refreshed every tick
  timeout 600 rsync -a --partial -m --include='*/' --include='*.log' --exclude='*' -e "${SSH[*]}" "root@$ip:/root/fl/out/" "$dest/" 2>>"$LOG" \
    || say "box $n: rsync logs rc=$?"
  rm -f "$dest/.files_$n.txt"
}

vultr_pull 1 "$H"
vultr_pull 2 "$S"

# --- InstaBox boxes: pull finished, verify, delete ---
if [ -f "$BOXES" ]; then
python3 - "$BOXES" "$S" "$IBR" "$LOG" <<'PYEOF'
import json, subprocess, sys, tarfile, hashlib, os, time
boxes_f, S, IBR, LOG = sys.argv[1:5]
def say(m):
    line = time.strftime("%FT%TZ", time.gmtime()) + " " + m
    print(line); open(LOG, "a").write(line + "\n")
def run(args, timeout):
    return subprocess.run(args, capture_output=True, text=True, timeout=timeout)
st = json.load(open(boxes_f))
changed = False
for name, b in st["boxes"].items():
    if b.get("status") == "pulled":
        continue
    try:
        r = run([IBR, "exec", name, "--timeout", "60", "--", f"ls /data/out/runs_{b['shard']}.log >/dev/null 2>&1 && grep -c ALL_DONE /data/out/runs_{b['shard']}.log; ls /data/out/*/*_food1.json 2>/dev/null | wc -l"], 90)
    except Exception as e:
        say(f"{name}: exec failed {e}"); continue
    out = [x for x in r.stdout.split() if x.isdigit()]
    if r.returncode != 0 or len(out) < 2:
        say(f"{name}: not queryable rc={r.returncode} {r.stderr.strip()[:120]}"); continue
    done, n_json = int(out[0]), int(out[1])
    b["json_on_box"] = n_json
    if done < 1:
        continue
    if n_json != b["expected"]:
        say(f"{name}: ALL_DONE but {n_json} json != expected {b['expected']}; not pulling"); b["status"] = "anomaly"; changed = True; continue
    r = run([IBR, "exec", name, "--timeout", "300", "--", "cd /data && rm -f out.tar && tar cf out.tar out && sha256sum out.tar && ls -l out.tar"], 360)
    if r.returncode != 0 or not r.stdout.strip():
        say(f"{name}: tar failed {r.stderr.strip()[:200]}"); continue
    box_sha = r.stdout.split()[0]
    dst = f"/home/thomas/work/flux-cpu-20261117/pulled/{name}.tar"
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.exists(dst): os.remove(dst)
    r = run([IBR, "pull", name, "/data/out.tar", dst], 1200)   # not piped: a closed pipe truncates the transfer
    if r.returncode != 0 or not os.path.exists(dst):
        say(f"{name}: pull failed rc={r.returncode} {r.stderr.strip()[:200]}"); continue
    h = hashlib.sha256()
    with open(dst, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""): h.update(chunk)
    if h.hexdigest() != box_sha:
        say(f"{name}: sha256 MISMATCH box={box_sha[:12]} local={h.hexdigest()[:12]}; box kept"); continue
    with tarfile.open(dst) as t:
        for m in t.getmembers():       # extract into species_scan_20261117, keeping subdirs, never overwriting
            if m.name.startswith("out/") and ".." not in m.name:
                m.name = m.name[4:]
                if not m.name: continue
                tgt = os.path.join(S, m.name)
                if m.isfile() and os.path.exists(tgt) and not m.name.endswith(".log"): continue
                t.extract(m, S, filter="data")
    r = run([IBR, "rm", "--yes", name], 120)
    if r.returncode != 0:
        say(f"{name}: pulled and verified but rm failed rc={r.returncode} {r.stderr.strip()[:200]}")
        b["rm_failed"] = True
    b.update(status="pulled", sha256=box_sha, pulled_at=time.strftime("%FT%TZ", time.gmtime()), deleted=(r.returncode == 0))
    say(f"{name}: pulled {n_json} runs, sha256 {box_sha[:12]} verified, rm rc={r.returncode}")
    changed = True
if changed:
    json.dump(st, open(boxes_f, "w"), indent=1)
PYEOF
fi

# --- git ---
cd "$WT" || exit 0
git add outputs/horizon300k_20261117 outputs/species_scan_20261117 >>"$LOG" 2>&1
if ! git diff --cached --quiet; then
  n_h=$(find "$H" -name '*_food1.json' | wc -l); n_s=$(find "$S" -name '*_food1.json' | wc -l)
  git commit -q -m "CPU campaign results: horizon $n_h/900, species scan $n_s/7200" >>"$LOG" 2>&1 && say "committed horizon $n_h/900 scan $n_s/7200"
  git push -q origin vizier/cpu-campaign-20261117 >>"$LOG" 2>&1 || say "git push failed (will retry next tick)"
fi

# --- status ---
n_h=$(find "$H" -name '*_food1.json' | wc -l); n_s=$(find "$S" -name '*_food1.json' | wc -l)
h_done=no; grep -qs ALL_DONE "$H"/runs_h1.log && h_done=yes
v_done=no; grep -qs ALL_DONE "$S"/runs_v2.log && v_done=yes
ib_pulled=$(python3 -c "import json;d=json.load(open('$BOXES'))['boxes'];print(sum(b.get('status')=='pulled' for b in d.values()),len(d))" 2>/dev/null || echo "0 0")
echo "horizon (Vultr box 1): json $n_h / 900, ALL_DONE $h_done"
echo "scan (Vultr box 2 + InstaBox): json $n_s / 7200, Vultr box 2 ALL_DONE $v_done, InstaBox boxes pulled/total: ${ib_pulled% *}/${ib_pulled#* }"
if [ "$n_h" -ge 900 ] && [ "$n_s" -ge 7200 ] && [ "$h_done" = yes ] && [ "$v_done" = yes ]; then echo CAMPAIGN_ALL_DONE; fi
exit 0
