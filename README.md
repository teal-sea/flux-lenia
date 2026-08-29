# fun-dots — Neural Flow Lenia discovery engine

An open-ended artificial-life workbench in JAX. Continuous multi-channel
fields, a neural sensory-motor map, strict mass conservation, and an oracle
that decides what counts as an organism, a division, and a behaviour.

```
engine/neural_field.py    the core: perception, brain, flow, transport
engine/novelty_oracle.py  complexity metrics, speciation tracking, anomalies
engine/render.py          shader-style compositing, GIF/MP4 recording
scripts/discover.py       the search loop (screen -> curate)
scripts/selftest.py       verification; run this before trusting a result
app/viewer.py             interactive viewport
```

## Run it

```bash
.venv/bin/python scripts/selftest.py                 # verify the core
.venv/bin/python scripts/discover.py screen --n 15   # sample candidates
.venv/bin/python scripts/discover.py curate --target 3
.venv/bin/streamlit run app/viewer.py                # explore interactively
```

`screen` is shardable: pass `--shard i --nshards n` and run several
processes in parallel. Results land in `hunts/_screen/shard_*.jsonl`, one
JSON line per candidate whether it passed or failed.

## How the dynamics work

Each step, for every cell:

```
U_k   = A[src_k] (*) ring_k            multi-scale perception (radii 3..45 px)
B_k   = bell(U_k)                      Lenia-style growth features
h     = tanh(FiLM_G(W1 [U, B, A, light]))    MLP conditioned on the LOCAL genome
E,g,t = W2 h                           growth potential, flux gain, drift angle
v_c   = g_c R(t_c) grad(E_c) - alpha grad(A_total)
A     = reintegrate(A, dt v)           mass-conserving transport
```

Three properties matter:

**Mass is conserved by construction.** Transport is reintegration tracking:
each cell's mass moves to a sub-cell position and is split bilinearly among
its neighbours, and those weights are a partition of unity. Measured drift
over 600 steps is ~1e-16 relative, i.e. float rounding, not tolerance.
Nothing is created, nothing decays, and "growth" only reshapes the potential
that mass flows along.

**Nothing blurs.** Donor-cell upwinding (what the legacy engine used) is
strongly diffusive and smears structure into mush. Reintegration tracking is
not: the selftest measures edge density before and after 600 steps and it
rises rather than collapsing.

**The flow is not a gradient.** `R(t_c)` rotates the velocity away from
`grad(E)`. A pure gradient flow relaxes into a minimum and stops; a rotated
one need not, which is where self-propulsion and circulation come from. Set
the orientation-drift ceiling to 0 in the viewer and the world visibly dies
down.

The genome is a per-cell vector field that rides along with the mass, so
different regions run different species, and where two organisms merge their
genomes blend in proportion to the mass each contributed. That is what makes
the viewer's spawner and mutation brush real edits to the world rather than
decoration.

## What the oracle will and will not claim

The point of this repo is not to generate pretty fields; it is to avoid
believing things about them that are not true. Concretely:

- **Division, not shedding.** A large body continuously sheds specks. An
  early version counted those as reproduction and reported 22 of 40
  candidates as "reproducing"; the offspring were ~0.6% of the parent's
  mass. Reproduction now requires an offspring to survive *and* to carry at
  least 10% of the parent's mass. Both the strict and the raw fission counts
  are reported, so the gap stays visible.
- **Phototaxis must track a moving lamp.** The probe runs the same world
  under three lamp positions and requires approach in every one. A creature
  that happens to drift north is not phototactic because the lamp is north.
- **A gait is not jitter.** Cyclical locomotion needs a period of at least 4
  frames; at 2 frames the sampling floor and a real cycle are
  indistinguishable.
- **Pursuit needs a moving target.** Drifting onto a stationary lump does
  not count.
- **Presets are seeds, not phenotypes.** `PREDATOR`, `SWARMER`, `PLANT` and
  `AMOEBA` are four distinct points in genome space with distinct channel
  mixes. They are handles for spawning, and nothing in the code claims a
  `PREDATOR` predates; the anomaly bouncer is what earns or refuses a
  behavioural label.
- **Zero is reported.** A search that finds nothing prints the count, the
  best score, and why, and exits non-zero.

One caveat worth knowing before quoting a behavioural verdict: the
detectors read organism *tracks*, so they inherit the tracker's sampling
cadence. Screening samples every 12 steps and the recording pass every 6,
and a borderline case can flip between them (this was observed: a pursuit
that scored 0.27 at the coarse cadence scored above threshold at the fine
one). The verdicts published in `hunts/SPECIES_*.md` come from the fine
cadence, and every verdict carries its raw numbers so a borderline call is
visible as borderline rather than as a bare yes.

## Verification

`scripts/selftest.py` checks the claims above rather than that the code
runs: exact partition of unity in the transport weights, mass conservation
under real dynamics, non-negativity, edge sharpness over 600 steps,
gradients flowing through a `lax.scan` rollout, Euler characteristic against
known shapes (disk 1, annulus 0, two disks 2), periodic connected components
across the wrap seam, fission detected on a synthetic split *and* rejected
on a one-frame flicker, spatial MI ranking structure above noise, every
canvas tool actually changing the world, the genome field tracking moving
mass, GIF/MP4 round-trips, and a headless render of the Streamlit app.

## Discovery run of 2026-08-28

120 candidates screened (two batches of 60, four and three shards in
parallel), 96 viable, **6 dividing under the strict criterion**, 3 curated
into species with reports, genomes and media. Mass drift across every run
stayed at ~1e-16 relative.

Division counts differ between the screening run (720 steps, tracked every
12) and the longer recording run (900 steps, tracked every 6). Both are
listed rather than blended, and each species' report states both.

| species | seed | alpha | divisions (screen / recording) | largest offspring | behaviours established |
| --- | --- | --- | --- | --- | --- |
| OSCILLIS | 442 | 0.35 | 4 of 4 raw / 3 of 4 | 41% of parent | none |
| MITOSA | 350 | 0.20 | 5 of 7 raw / 13 of 22 | 56% of parent | predatory pursuit |
| VAGRANT | 458 | 0.35 | 3 of 6 raw / 5 of 9 | 88% of parent | none |

All three rebuild exactly from their seed. The anomaly bouncer flagged 3
runs across the screen for cyclical locomotion and auto-recorded the two
best that did not win on score (`outputs/ANOMALY_*`).

Phototaxis was **not** established for any species, which is the expected
result: these are randomly initialized brains that were never selected for
light response, and the lamp-moving control rejects the drift that would
otherwise be mistaken for it. Reporting it as absent is the point of having
the control.

Two things this run corrected about itself, both worth knowing:

1. An earlier pass reported 22 of 40 candidates as reproducing. Those
   "offspring" were 0.3-2.6% of the parent's mass — debris shed by a big
   body. Adding the offspring-mass floor dropped the true rate to ~3-5%,
   and widening the search (concentration avoidance and seeded mass, not
   just brain weights) plus a shaped objective is what then found genuine
   dividers at 41-88% offspring share.
2. The hill-climb backstop works and was exercised: mutating a
   non-dividing lineage found a viable divider at 89.7% offspring share in
   4 generations. The final three species came from screening alone, so
   they are all seed-reproducible; the hill-climb path is kept for pools
   too thin to fill the target.

## The viewport

`streamlit run app/viewer.py`. Arm a tool, click the canvas:

- **Spawn** drops one of the four preset genomes where you click.
- **Mutate** is the radioactive brush; it perturbs the genome of the
  organism under the cursor and reports how many live cells it hit (zero if
  you hit vacuum).
- **Scalpel** excises mass. This intentionally breaks conservation, so it
  rebaselines the counter and says so.
- **Light** moves the lamp the creatures sense.

The recorder writes GIF and, when ffmpeg is present, MP4 into `outputs/`,
through the same render path shown on screen.

## Legacy engine

`engine/physics.py`, `engine/oracle.py` and `scripts/run_hunt.py` are the
earlier linear non-reciprocal model (asymmetric coupling matrix, upwind
advection) that produced `hunts/HUNT_*.md`. They still run and are left
intact so those results stay reproducible, but the neural engine above
supersedes them.
