#!/bin/bash
# Offload the tail of the 300k-step horizon from Vultr box 1 to the idle Vultr box 2 (docs/HORIZON-300K-GPU-2026-11-16.md,
# "Offload plan"). Cron-safe (absolute paths). Quiet no-op (exit 0) unless every precondition holds.
#   /home/thomas/worktrees/flux-lenia-cpu-20261117/scripts/offload_horizon_tail.sh [--dry-run]
# Rules: box 1 is never touched (read-only ssh). Box 2 writes to its OWN output dir /root/fl/out_h2, never /root/fl/out,
# because the scan there has the same <species>_fs<fs>_k3_per_channel subdirs and the same <species>_s<seed>_<arm>_food1.json
# names (30k steps) and would be overwritten / have its logs appended to. The collector maps out_h2 into the horizon dir.
# run_batch.py has no per-job output-exists skip (jobs are read once at start), so the share given to box 2 is bounded:
# ceil(remaining * 16/48) jobs from the END of the remaining list, launched in reverse order.
export HOME=/home/thomas
export PATH=/home/thomas/bin:/home/thomas/.local/bin:/usr/local/bin:/usr/bin:/bin
WT=/home/thomas/worktrees/flux-lenia-cpu-20261117
CB=/home/thomas/work/flux-gpu-20261116/live/cpubox.sh
JOBS_LOCAL=$WT/campaign_cpu/horizon_jobs.txt
JOBS_BOX1=/root/fl/horizon_jobs.txt          # the file box 1's scheduler was started with (code/ has no campaign_cpu/)
JOBS_BOX2=/root/fl/horizon_tail_h2.txt
OUT2=/root/fl/out_h2
MARK_BOX2=/root/fl/out/OFFLOAD_LAUNCHED
MARK_LOCAL=$WT/.OFFLOAD_LAUNCHED
LOG=/home/thomas/work/flux-cpu-20261117/offload.log
DRY=no; [ "${1:-}" = "--dry-run" ] && DRY=yes
mkdir -p "$(dirname "$LOG")"
say() { echo "$(date -u +%FT%TZ) offload: $*" | tee -a "$LOG"; }
noop() { say "NO-OP: $*"; exit 0; }
# pre(): a failed precondition. DRY_FORCE=1 with --dry-run reports it and continues, to exercise steps 2-3 before the scan ends.
pre() { if [ "$DRY" = yes ] && [ "${DRY_FORCE:-0}" = 1 ]; then say "PRECONDITION FAILED (ignored, DRY_FORCE): $*"; else noop "$*"; fi; }
rb() { local n=$1; shift; timeout 60 "$CB" "$n" "$@"; }

say "start dry_run=$DRY"
# --- 1. preconditions ---
[ -e "$MARK_LOCAL" ] && pre "local marker $MARK_LOCAL exists (already launched)"
say "ok: no local marker"
m=$(rb 2 "test -e $MARK_BOX2 && echo yes || echo no") || noop "ssh to box 2 failed"
[ "$m" = no ] || pre "box 2 marker $MARK_BOX2 exists (already launched)"
say "ok: no box 2 marker"
r2=$(rb 2 "grep -c ALL_DONE /root/fl/out/runs_v2.log; ps -eo args | grep -c '[f]ood_selection.py'; true") || noop "ssh to box 2 failed"
a2=$(echo "$r2" | sed -n 1p); p2=$(echo "$r2" | sed -n 2p)
[ "${a2:-0}" -ge 1 ] 2>/dev/null || pre "box 2 runs_v2.log has no ALL_DONE (scan still running)"
[ "${p2:-1}" -eq 0 ] 2>/dev/null || pre "box 2 still has $p2 food_selection.py process(es)"
[ "${a2:-0}" -ge 1 ] 2>/dev/null && [ "${p2:-1}" -eq 0 ] 2>/dev/null && say "ok: box 2 scan ALL_DONE and no food_selection.py running"
LOG1=$(mktemp -p "${TMPDIR:-/tmp}" h1log.XXXXXX) || exit 0
trap 'rm -f "$LOG1"' EXIT
rb 1 "cat /root/fl/out/runs_h1.log" > "$LOG1" || noop "ssh to box 1 failed or log unreadable"
n_done=$(grep -c ' done ' "$LOG1"); a1=$(grep -c ALL_DONE "$LOG1")
[ "$a1" -eq 0 ] || pre "box 1 horizon already ALL_DONE"
[ "$n_done" -lt 900 ] || pre "box 1 has $n_done done lines (>= 900)"
say "ok: box 1 horizon not finished ($n_done done lines, no ALL_DONE)"
# same code on both boxes (the result must not depend on which box ran a job)
sh1=$(rb 1 "cd /root/fl/code && cat engine/*.py scripts/*.py | sha256sum | cut -c1-64") || noop "ssh to box 1 failed (sha)"
sh2=$(rb 2 "cd /root/fl/code && cat engine/*.py scripts/*.py | sha256sum | cut -c1-64") || noop "ssh to box 2 failed (sha)"
[ "$sh1" = "$sh2" ] || pre "code differs between boxes (box1 $sh1 box2 $sh2)"
say "ok: engine/scripts sha256 equal on both boxes (${sh1:0:16})"

# --- 2. remaining list: full - done(rc=0) - in flight; reversed; bounded share ---
LIST=$(mktemp -p "${TMPDIR:-/tmp}" h2jobs.XXXXXX); trap 'rm -f "$LOG1" "$LIST"' EXIT
python3 -I - "$JOBS_LOCAL" "$LOG1" "$LIST" <<'PYEOF' || noop "job list computation failed"
import sys, re, math
jobs_f, log_f, out_f = sys.argv[1:4]
norm = lambda s: " ".join(s.split())
jobs = [norm(l) for l in open(jobs_f) if l.strip()]
assert len(jobs) == len(set(jobs)), "duplicate job lines"
launched, done_ok, done_bad = set(), set(), set()
for l in open(log_f):
    m = re.match(r"\S+ \S+ launch (.*) pid=\d+ avail_gib=\S+$", l.rstrip("\n"))
    if m: launched.add(norm(m.group(1))); continue
    m = re.match(r"\S+ \S+ done (.*) rc=(-?\d+) peak_rss_gib=\S+$", l.rstrip("\n"))
    if m: (done_ok if m.group(2) == "0" else done_bad).add(norm(m.group(1)))
unk = (launched | done_ok | done_bad) - set(jobs)
assert not unk, f"{len(unk)} logged jobs not in job file, e.g. {sorted(unk)[:2]}"
inflight = launched - done_ok - done_bad
remaining = [j for j in jobs if j not in done_ok and j not in inflight]   # failed (rc!=0) jobs stay in the list
k = math.ceil(len(remaining) * 16 / 48)
tail = remaining[len(remaining) - k:][::-1]                               # box 2 takes the END, last job first
open(out_f, "w").write("".join(j + "\n" for j in tail))
print(f"jobs {len(jobs)}  done_ok {len(done_ok)}  done_failed {len(done_bad)}  in_flight {len(inflight)}  remaining {len(remaining)}")
print(f"box 2 share ceil({len(remaining)}*16/48) = {k} jobs (reverse order)")
if tail: print("first (launched first):", tail[0]); print("last:", tail[-1])
sys.exit(0 if tail else 3)
PYEOF
[ -s "$LIST" ] || noop "nothing remaining for box 2"
N=$(wc -l < "$LIST")

RUNCMD="source /root/fl/env.sh; cd /root/fl/code && mkdir -p $OUT2 && STEPS=300000 SAMPLE_EVERY=1000 FRAME_EVERY=50000 SHARD=_h2 setsid nohup \$PY scripts/run_batch.py $OUT2 per_channel 16 $JOBS_BOX2 > /root/fl/out_h2.stdout 2>&1 < /dev/null & disown; date -u +%FT%TZ > $MARK_BOX2; echo launched"
if [ "$DRY" = yes ]; then
  say "DRY RUN: would copy $N jobs to box 2:$JOBS_BOX2, then run on box 2:"
  say "  bash -c '$RUNCMD'"
  say "  then write local marker $MARK_LOCAL"
  exit 0
fi

# --- 4. launch ---
rb 2 "test ! -e $JOBS_BOX2 && test ! -d $OUT2 && cat > $JOBS_BOX2" < "$LIST" || noop "could not stage job list on box 2 (exists already?)"
c=$(rb 2 "wc -l < $JOBS_BOX2"); [ "$c" = "$N" ] || { say "ERROR staged $c lines != $N; not launching"; exit 0; }
T=$(date -u +%FT%TZ)
rb 2 "bash -c '$RUNCMD'" || { say "ERROR launch command failed"; exit 0; }
date -u +%FT%TZ > "$MARK_LOCAL"
say "LAUNCHED $N jobs on box 2 at $T; first: $(head -1 "$LIST"); last: $(tail -1 "$LIST")"
