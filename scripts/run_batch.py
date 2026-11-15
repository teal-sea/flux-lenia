"""Run jobs.txt lines (SPECIES SEED ARM FOOD) with N concurrent single-thread processes.
Pauses launching if MemAvailable < 6 GiB; drops concurrency to 6 if any run's RSS > 2.5 GiB.
Usage: run_batch.py OUTDIR TRANSPORT [N] [JOBS_FILE]; logs to OUTDIR/runs.log, RSS peaks to OUTDIR/rss.log.
JOBS_FILE defaults to OUTDIR/jobs.txt; a resume after a killed batch passes the unfinished subset.
Optional extras (defaults leave the behaviour above unchanged):
  STEPS env (default 30000); SHARD env (suffix for runs/rss log names, e.g. _w2; the sentinel is
  written to runs{SHARD}.log); a job line may carry a 5th field KAPPA (repulsion, default 0) and
  a 6th field SUBDIR (outputs go to OUTDIR/SUBDIR; used by the pilot).
"""
import os, subprocess, sys, time
from pathlib import Path
out, transport = Path(sys.argv[1]), sys.argv[2]
n = int(sys.argv[3]) if len(sys.argv) > 3 else 8
jobs_file = Path(sys.argv[4]) if len(sys.argv) > 4 else out / "jobs.txt"
root = Path(__file__).resolve().parents[1]
py = os.environ.get("PY", str(Path.home() / "venvs/flux-lenia-20261103/bin/python"))
env = dict(os.environ, XLA_FLAGS="--xla_cpu_multi_thread_eigen=false intra_op_parallelism_threads=1")
jobs = [l.split() for l in jobs_file.read_text().splitlines() if l.strip()]
steps = os.environ.get("STEPS", "30000"); shard = os.environ.get("SHARD", "")
log = open(out / f"runs{shard}.log", "a"); rss = open(out / f"rss{shard}.log", "a")
def say(m): log.write(time.strftime("%F %T ") + m + "\n"); log.flush()
def avail_gib():
    for l in open("/proc/meminfo"):
        if l.startswith("MemAvailable"): return int(l.split()[1]) / 2**20
def rss_gib(pid):
    try:
        for l in open(f"/proc/{pid}/status"):
            if l.startswith("VmRSS"): return int(l.split()[1]) / 2**20
    except OSError: pass
    return 0.0
running, peak, cap = {}, {}, n
say(f"batch start: {len(jobs)} jobs, {n} concurrent, transport={transport}, pid={os.getpid()}")
todo = list(jobs)
while todo or running:
    for j, pr in list(running.items()):
        r = rss_gib(pr.pid); peak[j] = max(peak.get(j, 0), r)
        if r > 2.5 and cap > 6: cap = 6; say(f"RSS {r:.2f} GiB in {j}: concurrency cut to 6")
        if pr.poll() is not None:
            say(f"done {j} rc={pr.returncode} peak_rss_gib={peak[j]:.2f}")
            rss.write(f"{j} {peak[j]:.3f}\n"); rss.flush(); del running[j]
    while todo and len(running) < cap and avail_gib() >= 6:
        sp, seed, arm, food, *extra = todo.pop(0); j = " ".join((sp, seed, arm, food, *extra))
        kappa = extra[0] if extra else "0"; sub = extra[1] if len(extra) > 1 else ""
        odir = out / sub; odir.mkdir(parents=True, exist_ok=True)
        lf = open(odir / f"run_{sp}_s{seed}_{arm}.log", "a")
        running[j] = subprocess.Popen(["nice", "-n", "10", py, str(root / "scripts/food_selection.py"),
            sp, seed, arm, food, steps, str(odir), transport, kappa], stdout=lf, stderr=subprocess.STDOUT, env=env, cwd=root)
        say(f"launch {j} pid={running[j].pid} avail_gib={avail_gib():.1f}")
    if todo and avail_gib() < 6: say(f"paused: avail {avail_gib():.1f} GiB")
    time.sleep(15)
say("ALL_DONE")
