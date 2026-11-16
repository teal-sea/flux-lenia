"""Expand a campaign manifest into one gpu_batch.py invocation per (species, cell).

  python gpu/manifest.py expand MANIFEST [--pilot X] [--species A,B]   TSV: id <TAB> outdir-relative <TAB> expected-runs <TAB> gpu_batch args
  python gpu/manifest.py summary MANIFEST [--pilot X]                  counts

Manifest keys: experiment; defaults {steps, sample_every, frame_every, arms, seeds, food, batch};
species: list or "@ALL" (every outputs/species/*_genome.json); cells: list of
{kappa, food_sense, transport}. A food_sense of "@PILOT" is replaced by --pilot / $FOOD_SENSE_PILOT and
the expansion fails if that is unset: the pilot value is the owner's to choose, never defaulted.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if not (ROOT / "outputs" / "species").exists():          # Modal container: code sits in /app
    ROOT = Path("/app")


def count_seeds(text: str) -> int:
    n = 0
    for part in str(text).split(","):
        if "-" in part:
            a, b = part.split("-")
            n += int(b) - int(a) + 1
        else:
            n += 1
    return n


def fmt(x) -> str:
    return repr(float(x)).rstrip("0").rstrip(".") if float(x) != int(float(x)) else str(int(float(x)))


def expand(path, pilot=None, only=None) -> list[dict]:
    m = json.loads(Path(path).read_text())
    d = {"steps": 30000, "sample_every": 100, "frame_every": 1000, "arms": "treat,neutral_plus,neutral_minus",
         "seeds": "1-50", "food": 1, "batch": 150, **m.get("defaults", {})}
    sp = m["species"]
    if sp == "@ALL":
        sp = sorted(p.name[:-len("_genome.json")] for p in (ROOT / "outputs" / "species").glob("*_genome.json"))
    if only:
        sp = [s for s in sp if s in only]
    pilot = pilot if pilot is not None else os.environ.get("FOOD_SENSE_PILOT")
    out = []
    for s in sp:
        for c in m["cells"]:
            fsv = c["food_sense"]
            if fsv == "@PILOT":
                if pilot in (None, ""):
                    raise SystemExit("manifest has food_sense '@PILOT': pass --pilot X or set FOOD_SENSE_PILOT (the owner's pilot value)")
                fsv = float(pilot)
            kappa = float(c["kappa"])
            transport = c.get("transport", "per_channel")
            cid = f"{s}_fs{fmt(fsv)}_k{fmt(kappa)}_{transport}"
            nruns = count_seeds(d["seeds"]) * len(d["arms"].split(","))
            args = (f"--species {s} --arms {d['arms']} --seeds {d['seeds']} --steps {d['steps']} "
                    f"--sample-every {d['sample_every']} --frame-every {d['frame_every']} --transport {transport} "
                    f"--kappa {fmt(kappa)} --food-sense {fmt(fsv)} --food {d['food']} --batch {d['batch']}")
            out.append({"id": cid, "experiment": m["experiment"], "outdir": f"{m['experiment']}/{cid}",
                        "runs": nruns, "args": args})
    return out


def main():
    mode, path, rest = sys.argv[1], sys.argv[2], sys.argv[3:]
    get = lambda k: rest[rest.index(k) + 1] if k in rest else None
    only = get("--species").split(",") if get("--species") else None
    es = expand(path, get("--pilot"), only)
    if mode == "expand":
        for e in es:
            print(f"{e['id']}\t{e['outdir']}\t{e['runs']}\t{e['args']}")
    elif mode == "summary":
        print(f"{len(es)} batches, {sum(e['runs'] for e in es)} runs")
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
