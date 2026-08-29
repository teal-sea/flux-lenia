# Architecture

How the Neural Flow Lenia engine is built and why each piece is the way it
is. For how to run it, see the README. For what the discovery run found and
what went wrong on the way, see `FINDINGS.md`.

---

## 1. The state

A world is two fields on a periodic `size x size` grid, plus one static
input field.

| symbol | shape | meaning |
| --- | --- | --- |
| `A` | `(C, H, W)` | mass density per channel, always `>= 0` |
| `Gf` | `(G, H, W)` | genome vector per cell, advected with the mass |
| `light` | `(H, W)` | external stimulus, read by the brain as an input |

Defaults: `C = 3` channels, `G = 8` genome dimensions, `H = W = 128`,
float64 throughout.

`A` is the only conserved quantity. `Gf` is a property *of* the matter, not
a field in its own right: it is carried by mass and it blends where mass
blends. `light` is fixed by the operator and never changes on its own.

Everything runs in float64. This is not optional. In float32 the per-step
rounding is around `1e-7` relative, so a 700-step rollout could accumulate
drift near the `1e-4` conservation gate and the gate would stop meaning
anything. In float64 the per-step rounding is around `1e-16` and measured
drift over 600 steps is `2.1e-16`, which is rounding and nothing else.

---

## 2. One step

```
U_k   = A[src_k] (*) ring_k                 perception   (FFT convolution)
B_k   = 2*exp(-((U_k - m_k)/s_k)^2 / 2) - 1 growth features
X     = [U, B, A, light]                    feature stack, (2K + C + 1, H, W)
h     = tanh(FiLM_Gf(W1 X + b1))            hidden, conditioned on the genome
E,g,t = W2 h + b2                           three outputs per channel
v_c   = g_c R(t_c) grad(E_c) - alpha grad(sum A)
A,Gf  = reintegrate(A, Gf, dt * v)          conservative transport
```

Each line is a design decision, taken in turn.

### 2.1 Perception: multi-scale concentric rings

`K = 16` kernels. Radii are log-spaced from 3 to 45 cells and then jittered
by +-15%, so the bank has roughly equal resolution per octave rather than
crowding the large scales. Each kernel is a Lenia shell kernel: the radial
profile is divided into 3 concentric shells with independent weights, each
shell shaped by the smooth compact bump `exp(4 - 1/(x(1-x)))` on `(0,1)`.
Every kernel is normalized to unit sum, so `U_k` is a weighted local average
of density and lives on the same scale as `A` itself.

Each kernel reads exactly one source channel (`src_k`), sampled at random.
That is what lets channels perceive each other asymmetrically: channel 0 can
watch channel 1 at radius 5 while channel 1 watches channel 0 at radius 40.

Convolution is done by FFT because a 45-cell radius kernel is 91x91 dense,
and 16 of those per step in direct form would dominate the runtime. The FFTs
are precomputed once per world in `build_bank`.

### 2.2 Growth features: why bells feed the MLP

The MLP does not read `U` alone. It also reads a bell-curve transform of it,
`B_k`, with a learnable centre and width per kernel.

The reason is bluntly practical. Classic Lenia's growth is a linear
combination of bell functions of the perceptions, `E = sum_k h_k G_k(U_k)`.
That is exactly a linear layer on top of bell features. Feeding both `U` and
`B` means this architecture strictly *contains* classic Lenia rather than
merely resembling it, and a randomly initialized network starts near the
regime that is already known to produce solitons. A raw MLP on `U` alone is
close to monotone in its useful range and mostly produces blobs that
collapse or spread.

That single choice is the difference between a random brain being viable
around 80% of the time and being viable almost never.

### 2.3 The genome conditions the brain (FiLM)

```
gamma = 1 + Wg1 . Gf        beta = Wg2 . Gf
h     = tanh((W1 X + b1) * gamma + beta)
```

The MLP weights are global. What varies from cell to cell is the genome
vector, which modulates the hidden pre-activation multiplicatively and
additively. So "species" means a point in genome space, and two cells with
identical neighbourhoods but different genomes behave differently.

Multiplicative gating rather than plain concatenation is deliberate: a
concatenated genome only shifts the hidden units, while a gain term can
change which features a cell responds to at all. Stronger differentiation
per genome dimension, which matters when the whole species identity has to
fit in 8 numbers.

Storing a whole MLP per cell was the alternative and was rejected on cost.
The shared brain is 1,529 parameters (36 input features, 24 hidden, 9
outputs, plus the two FiLM matrices and the bell centres and widths). Even
the non-FiLM core is 1,113 numbers, so a per-cell brain would mean advecting
on the order of a thousand fields instead of 8, well over a hundred times
the transport work. Eight numbers conditioning a shared brain buys most of
the expressiveness for well under 1% of the cost.

### 2.4 Three outputs, and why one of them is a rotation

Per channel the network emits:

| output | squashing | role |
| --- | --- | --- |
| `E` | `e_scale * tanh` | growth potential; mass flows up its gradient |
| `g` | `gain_max * sigmoid` | flux gain, how hard this cell pushes |
| `t` | `theta_max * tanh` | orientation drift, in radians |

`E` plays the role of Flow Lenia's affinity field. Nothing about `E` creates
mass; it only says which way mass should go.

`t` is the important one. Without it, `v = g grad(E)` is a gradient flow,
and gradient flows relax. They run downhill, find a minimum, and stop. A
world built only from `E` would be a world where everything eventually sits
still. Rotating the velocity by `R(t)` makes the field non-gradient, so
there is no potential for it to sit at the bottom of, and locomotion and
circulation can persist indefinitely. Setting `theta_max = 0` in the viewer
visibly kills the world, which is the cheapest demonstration available that
this term is doing the work.

The `-alpha grad(sum A)` term is the only thing preventing every world from
collapsing into a single delta spike. It is deliberately kept outside the
rotation so it always points away from density rather than being spun into
something else.

### 2.5 Transport: reintegration tracking

This is the heart of the engine and the piece that most distinguishes it
from the legacy `engine/physics.py`.

Displacement is `d = dt * v`, smoothly saturated so `|d| < max_step` with
`max_step = 0.85` cells:

```
scale = max_step * tanh(|d| / max_step) / |d|
```

Smooth saturation rather than a hard clip, because a hard clip sets every
fast cell to exactly the ceiling and destroys the velocity gradients that
the structure depends on.

Then each cell's mass is moved to its sub-cell target position and split
bilinearly over the neighbours:

```
for each offset o in the 3x3 stencil:
    w = clamp(1 - |o_y - d_y(x-o)|) * clamp(1 - |o_x - d_x(x-o)|)
    A_new += w * A(x-o)
```

Two properties follow, and both are tested:

**Conservation is structural.** The bilinear weights of a single source cell
sum to exactly 1 over the stencil (measured worst case `2.2e-16` over 64
random displacements). Because `max_step < 1`, all nonzero weights fall
inside the 3x3 window, so nothing is silently truncated at the stencil edge.
Mass is not corrected, rescaled, or clipped back into line. It simply cannot
leave.

**Nothing blurs.** This is the reason for choosing this scheme over
donor-cell upwinding, which the legacy engine used. Upwinding also conserves
mass exactly, and it *also* smears every structure into mush within a few
hundred steps, because it is first-order and strongly diffusive. Exact
conservation and faithful dynamics are different properties, and only one of
them was ever in doubt. The selftest measures edge density per unit mass,
which collapses toward zero under diffusion; here it goes from 0.657 to
0.902 over 600 steps.

Because `A >= 0`, `w >= 0`, and nothing is subtracted, density can never go
negative and no clipping is required anywhere.

### 2.6 Genome transport

The genome rides on the mass as a mass-weighted mixture:

```
Gf_new = sum_o w_o A_tot(x-o) Gf(x-o)  /  sum_o w_o A_tot(x-o)
```

Where two organisms' mass merges into one cell, their genomes average in
proportion to the mass each contributed. Spawning into empty space gives a
pure genome; spawning onto an existing organism gives a hybrid.

The genome travels on the mass-weighted mean displacement across channels,
since it belongs to matter rather than to any one channel. That is an
approximation when channels move differently, and it is documented as one in
the code.

**`advect_genome = False` is an exact optimization, not a shortcut.** For a
spatially uniform genome the weighted average returns that same uniform
value, so skipping the pass changes nothing. Single-species searches run
with it off (63 steps/s versus 47), and the viewer and any multi-species
world run with it on.

### 2.7 What the transport does not have

There is no conduit memory. Flux does not thicken a channel and absence does
not decay one. That is the one ingredient in Physarum-style adaptive network
models (`dD/dt = f(|Q|) - D`) that would give persistent foraging networks,
and it is deliberately absent. See `ROADMAP.md`.

---

## 3. Performance

Measured on an M-series Mac, 10 cores, CPU only, at 128x128 with 3 channels
and 16 kernels:

| configuration | steps/s |
| --- | --- |
| `advect_genome = False` | 63 |
| `advect_genome = True` | 47 |

One screening candidate is 720 steps, roughly 12s alone. Four parallel
shards give roughly 1.6x total throughput rather than 4x, because JAX
already threads the FFTs across cores, so the shards contend. Sixty
candidates across four shards took about 8 minutes wall clock.

`rollout` uses `lax.scan` over a fixed step count, so a chunked run compiles
once and reuses. Changing any static `Config` field (including `alpha`)
triggers a recompile, which is why the search quantizes `alpha` to four
values instead of sampling it continuously.

---

## 4. Differentiability

The whole step is pure JAX with no data-dependent control flow, so gradients
flow through arbitrarily long `lax.scan` rollouts. The selftest confirms it
directly: `jax.grad` of a loss over a 5-step rollout with respect to all
1,529 brain parameters gives finite gradients with max magnitude 13.0.

Nothing currently trains. The machinery is there for it and unused. That is
the single largest piece of unrealized capability in the repo.

---

## 5. Module map

```
engine/neural_field.py    Config, KernelSpec, params, step, rollout, World
engine/novelty_oracle.py  complexity metrics, SpeciationTracker, detectors
engine/render.py          composite, overlays, GIF/MP4 writers
scripts/discover.py       Candidate sampling, screen, hill-climb, curate
scripts/selftest.py       27 checks
app/tools.py              click tools, Streamlit-free so they are testable
app/viewer.py             the viewport
engine/physics.py         LEGACY linear engine, superseded
engine/oracle.py          LEGACY gates, superseded
scripts/run_hunt.py       LEGACY hunt runner, superseded
```

The legacy trio still runs and still produces `hunts/HUNT_*.md`. It is kept
so those results stay reproducible, not because it is recommended.

---

## 6. Invariants the code must never break

1. **Total mass is conserved to float rounding.** Any change to transport
   must keep the per-source weights a partition of unity. If you add a term
   that creates or destroys mass, the conservation gate will catch it, and
   the correct response is to write it as a transfer between channels rather
   than to widen the tolerance.
2. **Density is non-negative.** Guaranteed structurally by non-negative
   weights and no subtraction. Do not introduce a subtractive term.
3. **Detectors report their margins.** Every gate and every anomaly returns
   the number it judged on, not just a verdict, so a borderline call is
   visible as borderline.
4. **A detector that cannot evaluate fails.** Never default to pass. An
   empty field, a missing track, a blast that did not disturb anything: all
   of these are failures, not silent successes.
5. **Zero is reported.** A search that finds nothing prints the count, the
   best score seen, the reason, and exits non-zero.

---

## 7. Extension points

- **New channel semantics.** Adding a consumable nutrient channel is the
  most promising extension and does not break conservation, provided the
  reaction is written as an antisymmetric transfer between channels.
- **Conditional genome blending.** The mixing rule in `reintegrate` is the
  single place to change to get self/non-self recognition.
- **New detectors.** Follow the `Anomaly` contract: a verdict, a numeric
  score, and a detail string carrying the raw evidence.
- **Training.** Write a loss over `rollout` output and use `jax.grad`. The
  hard part is already done.
