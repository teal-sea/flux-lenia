# Roadmap

What this project is aimed at, in order, with the reasoning. Written so that
picking it up cold does not require reconstructing the argument.

---

## 0. The claim worth chasing

Most artificial life systems have a fitness function. Someone writes down
what winning means, the search finds things that win, and the result is
bounded by whatever that function could express. It is shopping, not
discovery.

This engine was built so that it does not need one. Mass is conserved, so
the total is fixed. The genome is a field carried by the mass, so it is
inherited by whatever matter an organism holds and blended where matter
merges. Put those together and a genome configuration that is better at
acquiring and holding mass mechanically increases its own share of the
world. No score, no selection loop, no generations, no resets.

**The target claim:** heritable variation plus a conserved budget is
sufficient for selection, with no fitness function anywhere, demonstrated by
a measured shift in the genome distribution against a control where the
genome does not advect.

That is a small claim. It is also sharp, falsifiable with the instruments
already built, and it is aimed at the actual open question in this field
rather than at producing more creatures. Nobody has a system that keeps
generating novelty the way the biosphere does, and the two leading
explanations are that in nature the environment for each organism is mostly
other organisms, and that nobody wrote a fitness function. This engine can
speak to the second.

Precedent for taking a toy seriously: Conway's Game of Life demonstrated
universal computation in a trivial substrate, and Boids was three rules that
changed how flocking was understood. Both were hobbies. They mattered
because each isolated one mechanism so cleanly that it could not be argued
with, not because they were large or pretty. That is the bar. It is not
"find more species."

---

## 1. Measure genome variance decay `[gates everything, ~1 hour]`

**Why first.** The mixing rule in `reintegrate` averages genomes wherever
mass merges, weighted by mass. That is a diffusion operator, and it runs
everywhere, every step, including inside a single organism wherever the flow
field varies. If it homogenizes the world faster than selection can amplify
any difference, then every experiment below is dead and the system is a
single-species pattern generator wearing a costume.

This has not been measured. It should be measured before anything is built
on top of the assumption that it is fine.

**Experiment.** Seed one world with two clearly distinct genome patches.
Track between-organism genome variance over time. Compare against a control
with `advect_genome = False` where the field is frozen. Report the decay
half-life in steps.

**Decision rule.** If variance half-life is short relative to the timescale
on which organisms interact (hundreds rather than tens of thousands of
steps), go to step 2 before attempting step 3. If it is long, step 3 can
proceed directly.

---

## 2. Conditional genome blending, i.e. self/non-self recognition `[~1 hour]`

**Why.** Fungi already solved the problem in step 1. Hyphae fuse when they
meet a genetically compatible neighbour and reject it, often killing the
contact zone, when they do not. This is vegetative incompatibility and it is
exactly a mechanism for stopping genetic variation from washing out on
contact.

Current blending is unconditional: any two masses that touch average. Making
the blend conditional on genome similarity gives:

- variation that stops leaking, so distinct lineages can coexist
- competition without averaging into grey
- self/non-self recognition as a free side effect
- a mechanism biology actually uses, rather than one invented for
  convenience

**Change.** One rule in `reintegrate`. Where the incoming genome is similar
to the resident genome, blend as now. Where it is dissimilar, resist: keep
the resident genome and optionally add a repulsive contribution to the
velocity at the contact zone.

**Risk.** A hard threshold will produce artefacts at boundaries. Prefer a
smooth similarity weight. Conservation must not be touched: this changes
only how `Gf` mixes, never how `A` moves.

---

## 3. Selection with no fitness function `[the actual experiment, ~half a day]`

**Setup.** One world. N distinct genome patches, say 20, seeded at random
positions with a shared brain. Fixed total mass. `advect_genome = True`.
Long run, of order 50k steps. No scoring anywhere in the loop.

**Measure.**

- mass share held by each genome cluster over time
- entropy of the genome cluster distribution
- whether specific clusters expand monotonically
- lineage trees from `SpeciationTracker`

**Control.** Identical run with the genome field frozen. If the distribution
shifts in both, the shift is not selection.

**What would count as a result.** Cluster mass shares diverge in the live
run and do not in the control, with entropy falling. Reported with the
number of independent seeds it held for, because one run proves nothing.

**Follow-ons if it works.**

- *Does division get selected for on its own?* A body that splits colonizes
  more of a fixed budget, so dividers should displace non-dividers with
  nobody rewarding them. Measure the divider fraction over time.
- *Error threshold.* Add a per-step mutation rate to the genome field and
  sweep it. Eigen's error threshold predicts a sharp transition between
  lineages that dissolve and lineages that freeze. A sharp transition is the
  kind of result that is hard to fool yourself about.

---

## 4. Consumable nutrient channel `[~1 hour, changes morphology completely]`

**Why.** Every morphology found so far is a compact blob, and that is
correct for the regime built rather than bad luck. Branching, foraging,
mycelial growth needs a tip instability: a front advancing into empty space,
fed by a resource that depletes, so a bump that sticks out reaches fresh
food first and grows faster. Positive feedback gives fingers. Same physics
family as viscous fingering and dendritic crystals.

This world has neither half. Mass is conserved, so there is no growth front.
The only external field is static and inexhaustible, so there is no
depletion gradient to chase.

**Change that preserves the invariant.** Add a nutrient channel to the same
conserved field: body channels 0-2, food at channel 3. A local reaction
moves mass from food to body wherever body is present, written
antisymmetrically so what leaves food enters body. Total mass is still
exactly conserved and the gate still means what it meant.

**Expected effect.** Chemotrophic growth, depletion, a reason to explore,
and a shift from the compact-soliton regime into the branching-network
regime. Morphology should change completely. This is the single most
visually dramatic change available.

---

## 5. Genotype-based individuation `[~1 hour]`

**Why.** The current organism definition is topological: one connected
blob, one UUID. *Armillaria ostoyae* in the Malheur forest is a single
genetic individual spread over roughly ten square kilometres, thousands of
years old, much of it not contiguous tissue, linked by rhizomorph cords.
Under the current tracker that is thousands of separate organisms.

The genome field makes clonal, spatially disconnected individuals perfectly
possible here, and the tracker cannot see them.

**Change.** Cluster live cells by genome vector and report clonal identity
alongside topological identity. Both are useful: connected bodies for
counting fissions, genotype clusters for counting individuals.

---

## 6. Train instead of search `[~a couple of hours]`

**Why.** Random search gets a specific capability 5% of the time. The engine
is differentiable end to end and no gradient is ever taken. BPTT through
`rollout` with Adam would be far more efficient, and it directly closes the
weakest claim in the current results: phototaxis is absent because nothing
ever selected for it, which is not the same as it being impossible.

**Objectives.** Navigate to a moving target. Maximize centre-of-mass speed.
Follow the lamp.

**Caveat that keeps this below the experiments above.** Training answers
"can this architecture be optimized," which is engineering, and the answer
is very likely yes. The experiments in steps 1 to 3 answer "does this
substrate do something on its own," which is the research question. Do not
let the easier one crowd out the harder one.

---

## 7. Conduit memory, for persistent networks `[speculative]`

Physarum-style adaptive network models thicken a tube with flux and decay it
without: `dD/dt = f(|Q|) - D`. That memory is what turns exploratory tips
into a persistent optimized network, and it is what produced the results
where slime mould networks compare respectably to real rail systems on
cost, efficiency and fault tolerance.

This engine's transport has flux but no memory, so channels never reinforce.
Adding a conductance field that gates the flux gain would be the third
ingredient for genuine foraging networks, on top of step 4's nutrient.

Speculative because it is a real addition to the dynamics rather than a
change to a mixing rule, and because steps 1 to 4 should come first.

---

## Ordering

```
1. variance decay          gates everything, do it first
2. incompatibility         fixes the fatal flaw, if step 1 says it is fatal
3. selection experiment    the actual claim
4. nutrient channel        biggest visual change, independent of 1-3
5. genotype individuation  small, makes 3 measurable properly
6. training                engineering, high success probability, lower value
7. conduit memory          speculative, after 4
```

Steps 1 and 2 together are roughly two hours and decide whether the
interesting version of this project exists at all. If the answer is no, it
ends with a working engine, a conservation technique worth reusing, and some
good GIFs. That is an acceptable floor.
