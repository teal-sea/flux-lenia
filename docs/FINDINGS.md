# Findings

What the discovery run produced, and, at greater length, what it got wrong
first. The errors are the more useful half of this document: every one of
them was a case where the numbers looked healthy and the system was doing
something else.

Run date: 2026-08-28. Engine: `engine/neural_field.py` at commit `2f3ebe5`.

---

## 1. Results

120 candidates screened in two batches of 60. 96 viable. 6 dividing under
the strict criterion. 3 curated into species with reports, genomes and
media.

| species | seed | alpha | divisions (screen / recording) | largest offspring | behaviours established |
| --- | --- | --- | --- | --- | --- |
| OSCILLIS | 442 | 0.35 | 4 of 4 raw / 3 of 4 | 41% of parent | none |
| MITOSA | 350 | 0.20 | 5 of 7 raw / 13 of 22 | 56% of parent | predatory pursuit |
| VAGRANT | 458 | 0.35 | 3 of 6 raw / 5 of 9 | 88% of parent | none |

Mass drift across every run in the campaign stayed at approximately `1e-16`
relative. Not one run out of roughly 180 breached the `1e-4` gate, including
the ones that failed every other gate.

All three species rebuild exactly from their seed, verified by the selftest:
two independent loads of a saved genome agree bitwise after 240 steps.

**Hit rates.** Viability is cheap and division is expensive:

| property | rate |
| --- | --- |
| viable (persistent, localized, active, conserving) | 96/120 = 80% |
| dividing, strict criterion | 6/120 = 5% |
| flagged by the anomaly bouncer | 3/120 = 2.5% |

That gap is itself a finding. Random search over "produces interesting
dynamics" succeeds most of the time. Random search over "produces a specific
capability" is twenty times harder, and this is the argument for training
rather than searching.

**Phototaxis was not established for any species.** This is the expected
result and it is reported as a result rather than as a gap. These are
randomly initialized brains that were never selected for light response. The
probe moves the lamp to three positions and requires approach in all three,
so a creature that merely drifts cannot pass by being lucky about the lamp's
location. Best margin observed was `+0.02` against a `+0.05` threshold.

---

## 2. The four measurement failures

### 2.1 Debris counted as offspring

**Symptom.** The first pass reported 22 of 40 candidates as reproducing, a
55% rate.

**Reality.** A large body continuously sheds specks. The tracker saw one
blob become two, logged a fission, and the "offspring" survived long enough
to qualify. Their mass was 0.3% to 2.6% of the parent's. Rendering a single
frame showed it immediately: one fat central blob ringed by fourteen tiny
satellites, each faithfully circled by an organism marker.

**What made it invisible in the numbers.** Every gate passed. Mass
conservation was perfect at `1.1e-16`. Concentration was 33.7, well above
the threshold. Nine fission events with surviving offspring, deepest lineage
generation 3, 64 organisms tracked. Nothing in that report is false. It is
all consistent with a healthy dividing population and it is also all
consistent with a blob dropping crumbs, and the summary statistics cannot
tell those apart.

**Fix.** An offspring must survive *and* carry at least 10% of the parent's
mass (`MIN_OFFSPRING_FRAC`). Both the strict and the raw count are reported
side by side in every species report so the gap stays visible.

**Effect.** The rate fell from 55% to 0% on the same candidates. Widening
the search space and reshaping the objective then recovered it to 5%, with
offspring at 41-88% of parent mass rather than 0.6%.

**The general lesson.** Same runs, same physics, two answers an order of
magnitude apart, and the only thing that changed was a threshold I picked
casually. In emergence work the detector *is* the experiment.

### 2.2 A 2.1-frame "gait"

**Symptom.** The cyclic locomotion detector reported a confirmed periodic
gait with `period = 2.1 frames`.

**Reality.** Two frames is the Nyquist floor of the sampling. At that period
a real cycle and centroid jitter are mathematically indistinguishable.

**Fix.** `MIN_CYCLE_FRAMES = 4`. Anything faster scores zero on the spectral
route. After the fix the detector selected a different organism in the same
world with a genuine 23-frame period.

### 2.3 A report claiming more divisions than fissions

**Symptom.** A species report stated 13 divisions out of 7 raw fissions.
Strict counts cannot exceed raw counts; the filter only removes.

**Cause.** The strict count came from the recording run (900 steps, tracked
every 6) and the raw count from the screening run (720 steps, tracked every
12). Two different runs presented as one comparison.

**Fix.** Both figures now come from the same tracker, and the screening
run's numbers appear on a separate labelled line.

**Why it matters beyond the typo.** This is the failure that is hardest to
catch in general, because both numbers were correct measurements. Only the
juxtaposition was false, and it was caught by an internal consistency check
(strict must be <= raw), not by any test.

### 2.4 Merged organisms that never died

**Symptom.** Found by reading the tracker, not by a failing test.

**Cause.** When two bodies merge, the heavier parent carries the identity
forward. The lighter one had successors, so it was not marked dead by the
no-successor branch, but its successor was claimed by the other parent, so
it silently vanished from the active set with `death_frame = None`.

**Effect.** Absorbed organisms counted as survivors forever, inflating the
persistence gate.

**Fix.** A parent whose successors were all claimed elsewhere is recorded as
`merged`, with a death frame. Covered by a test.

---

## 3. A hypothesis that did not survive

At n=2, both dividers had the lowest concentration avoidance setting
(`alpha = 0.2`), and this was noted mid-run as a possible pattern: weaker
anti-clumping might make bodies more willing to split.

At n=7 the dividers spanned the whole range: `0.35, 0.20, 0.35, 0.20, 0.20,
0.80, 0.20`. Three of four alpha values are represented. The pattern
dissolved.

Recorded here because the alternative is quietly dropping it, and a
disappearing hypothesis is worth as much as a confirmed one when the sample
was that small to begin with.

---

## 4. What actually made division happen

Forty random brains at fixed settings produced zero true dividers. The brain
was not the lever.

What produced dividers was widening the search beyond the neural parameters
to two physical ones:

- **`alpha`**, concentration avoidance, quantized to `{0.20, 0.35, 0.55,
  0.80}`.
- **Seeded mass**, via spawn radius and peak, over three combinations.

The mechanism is a mass budget argument and in hindsight it is obvious. In a
world where mass cannot be created, a species has a preferred body size set
by its kernel radii and growth response. Hand it three times that mass and
it has exactly two options: split, or become amorphous. Division is a
mass-budget phenomenon, not a control-policy one.

### 4.1 The objective had to be shaped

The strict division count is 0 for about 95% of candidates and 1 for most of
the rest. A mutation search hill-climbing on that is climbing a flat plane.

Two continuous proxies were added to the score, both of which rise smoothly
as a lineage approaches genuine division:

- `second_share`: the mass of the second largest body over the largest. Near
  0 for one blob plus specks, near 1 for a world that has actually divided.
- `best_child_mass_frac`: the largest offspring any fission produced,
  regardless of whether it cleared the 10% bar.

With those in the objective, the hill-climb found a viable divider with an
89.7% offspring share in 4 generations from a non-dividing lineage. Without
them there was nothing to follow.

The final three species came from screening alone and are all
seed-reproducible; the hill-climb path is retained for pools too thin to
fill the target.

---

## 5. Sampling cadence changes verdicts

Behavioural detectors read organism *tracks*, so they inherit the tracker's
sampling rate. The same world produced:

| cadence | pursuit score | verdict |
| --- | --- | --- |
| every 12 steps (screening) | 0.27 | not established |
| every 6 steps (recording) | 0.47 | established |

Threshold is 0.35. Nothing about the world changed.

This is a real limitation, not a bug to be papered over. Published verdicts
come from the fine cadence, and every verdict carries its raw numbers so a
borderline call reads as borderline. The proper fix is to track at native
step resolution for the final verification pass, which is on the roadmap.

---

## 6. The tests that earned their keep

Twenty-seven checks pass. They were not equally useful.

**Confirmed the math, caught nothing:** partition of unity, Euler
characteristic against known shapes, spatial MI ranking, gradient flow. The
math was never the problem.

**Caught real defects, all of them negative cases:**

- a one-frame flicker that must *not* count as reproduction
- a shed speck that must register as a raw fission and must *not* survive
  the mass filter
- a merged body that must be marked dead
- the genome-tracking test that *failed* because its premise was not met

That last one is worth dwelling on. The test asserted that a mutated genome
follows its organism, and it required the mass to have travelled more than 3
cells for the comparison to mean anything. It failed, reporting 0.2 cells of
travel. That looked like a broken test and was the test working exactly as
intended: the discovered species keep a nearly stationary main body, and
without the premise check the assertion would have passed while
demonstrating nothing. It was rewritten to drive the transport operator
directly with a known constant displacement, where the answer is exact: mass
and carried genome both land at x=34.00 as predicted, genome undiluted at
1.000.

**Rule of thumb from this campaign:** a test that can only confirm the happy
path would have passed on the debris. Write the case that must fail.

---

## 7. Open weaknesses

1. **Genome blending is a diffusion operator.** Masses that touch average
   their genomes, weighted by mass, everywhere, every step, including inside
   a single organism wherever the flow varies. It may homogenize the world
   faster than any selection can amplify a difference. The decay rate has
   not been measured, and it gates every multi-species experiment.
2. **Nothing trains.** The engine is differentiable end to end and no
   gradient is ever taken outside the selftest.
3. **The organism definition is topological.** One connected blob, one
   identity. A clonal individual occupying disconnected patches, which the
   genome field makes perfectly possible, is counted as many organisms.
4. **No consumable resource.** The only external field is static and
   inexhaustible, so there is no depletion gradient and therefore no tip
   instability, and therefore every morphology found is a compact blob.
5. **Behavioural verdicts are cadence-dependent**, per section 5.
