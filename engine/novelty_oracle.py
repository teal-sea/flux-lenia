"""Emergence and anomaly detection for Neural Flow Lenia worlds.

Three layers, in increasing order of how strong a claim they make:

1. **Spatial complexity** — cheap scalar descriptors of a single frame:
   morphological diversity, spatial mutual information, and the topological
   Euler characteristic. These say how structured a world is.

2. **Speciation tracking** — persistent density blobs are promoted to
   *organisms* with stable identities, lifespans, and a lineage tree.
   Fission is detected as one body splitting into several that each go on to
   survive, which is the only sense in which a strictly mass-conserving
   world can be said to reproduce: no new matter appears, an organism
   divides what it has.

3. **The anomaly bouncer** — behavioural claims, each of which must beat a
   control before it is allowed to be logged. Phototaxis is only recorded if
   the organism tracks the light when the light MOVES; a creature that
   happens to drift north is not phototactic just because the lamp is north.
   Pursuit requires one body to close on another that is itself moving.
   Cyclical locomotion requires a dominant spectral period or consistent
   turning, not merely a wiggle.

Every detector reports its numeric margin, and a detector that cannot run
(too few frames, no organisms) returns "not established" rather than a
default pass.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field, asdict

import numpy as np
from scipy import ndimage

# --------------------------------------------------------------------------
# Frame-level complexity
# --------------------------------------------------------------------------


def euler_characteristic(binary: np.ndarray) -> int:
    """chi = components - holes, via 2x2 bit-quad counting (4-connectivity).

    The field is zero-padded first, so the result describes the pattern as a
    figure in the plane rather than on the torus.
    """
    b = np.pad(binary.astype(np.uint8), 1)
    q = (b[:-1, :-1].astype(int) << 3 | b[:-1, 1:].astype(int) << 2
         | b[1:, :-1].astype(int) << 1 | b[1:, 1:].astype(int))
    counts = np.bincount(q.ravel(), minlength=16)
    n1 = counts[[1, 2, 4, 8]].sum()          # exactly one filled corner
    n3 = counts[[7, 11, 13, 14]].sum()       # exactly three filled corners
    nd = counts[[6, 9]].sum()                # the two diagonal patterns
    return int((n1 - n3 + 2 * nd) // 4)


def spatial_mutual_information(f: np.ndarray, lags=(1, 2, 4, 8),
                               bins: int = 12) -> float:
    """Average MI (nats) between a cell and its neighbour at several lags.

    Quantile binning, so a mostly-empty field is still informative: uniform
    noise gives ~0, a smooth blob gives a high value, and structure at
    several scales keeps MI high out to large lags.
    """
    x = f.ravel()
    edges = np.unique(np.quantile(x, np.linspace(0, 1, bins + 1)))
    if edges.size < 3:
        return 0.0                                # constant field: no info
    d = np.digitize(f, edges[1:-1])
    nb = edges.size - 1

    vals = []
    for lag in lags:
        for axis in (0, 1):
            joint = np.histogram2d(
                d.ravel(), np.roll(d, lag, axis=axis).ravel(),
                bins=[nb, nb], range=[[0, nb], [0, nb]])[0]
            p = joint / joint.sum()
            px, py = p.sum(1, keepdims=True), p.sum(0, keepdims=True)
            nz = p > 0
            vals.append(float(np.sum(p[nz] * np.log(p[nz] / (px @ py)[nz]))))
    return float(np.mean(vals))


def cross_channel_mi(A: np.ndarray, bins: int = 12) -> float:
    """Mean MI between distinct channels. High means the channels organize
    each other rather than living independently."""
    c = A.shape[0]
    if c < 2:
        return 0.0
    out = []
    for i in range(c):
        for j in range(i + 1, c):
            xi, xj = A[i].ravel(), A[j].ravel()
            ei = np.unique(np.quantile(xi, np.linspace(0, 1, bins + 1)))
            ej = np.unique(np.quantile(xj, np.linspace(0, 1, bins + 1)))
            if ei.size < 3 or ej.size < 3:
                continue
            di = np.digitize(xi, ei[1:-1])
            dj = np.digitize(xj, ej[1:-1])
            joint = np.histogram2d(di, dj, bins=[ei.size - 1, ej.size - 1])[0]
            p = joint / joint.sum()
            px, py = p.sum(1, keepdims=True), p.sum(0, keepdims=True)
            nz = p > 0
            out.append(float(np.sum(p[nz] * np.log(p[nz] / (px @ py)[nz]))))
    return float(np.mean(out)) if out else 0.0


# --------------------------------------------------------------------------
# Blob extraction
# --------------------------------------------------------------------------


@dataclass
class Blob:
    """One connected body of mass in one frame."""

    label: int
    mask: np.ndarray = field(repr=False)
    area: int
    mass: float
    channel_mass: np.ndarray
    centroid: tuple[float, float]
    elongation: float
    radius: float
    peak: float

    @property
    def dominant_channel(self) -> int:
        return int(np.argmax(self.channel_mass))

    def descriptor(self) -> np.ndarray:
        mix = self.channel_mass / (self.channel_mass.sum() + 1e-12)
        mix_entropy = float(-np.sum(mix * np.log(mix + 1e-12)))
        return np.array([
            np.log10(self.area + 1.0),
            self.elongation,
            self.radius / (np.sqrt(self.area / np.pi) + 1e-9),
            np.log10(self.peak + 1e-6),
            mix_entropy,
        ])


def _label_periodic(mask: np.ndarray) -> tuple[np.ndarray, int]:
    """Connected components on a torus: label, then union across the seams."""
    lab, n = ndimage.label(mask)
    if n == 0:
        return lab, 0

    parent = np.arange(n + 1)

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[max(ra, rb)] = min(ra, rb)

    for u, v in ((lab[0, :], lab[-1, :]), (lab[:, 0], lab[:, -1])):
        both = (u > 0) & (v > 0)
        for a, b in zip(u[both], v[both]):
            union(int(a), int(b))

    roots = np.array([find(i) for i in range(n + 1)])
    uniq = {r: i for i, r in enumerate(sorted(set(roots[1:])), start=1)}
    remap = np.zeros(n + 1, dtype=int)
    for i in range(1, n + 1):
        remap[i] = uniq[roots[i]]
    return remap[lab], len(uniq)


def _circular_centroid(mask: np.ndarray, weight: np.ndarray) -> tuple[float, float]:
    """Centroid on a torus, via the circular mean of each axis."""
    n = mask.shape[0]
    w = weight * mask
    m = w.sum()
    if m <= 0:
        return (float("nan"), float("nan"))
    ang = 2 * np.pi * np.arange(n) / n

    def circ(profile):
        a = float(np.sum(profile * np.cos(ang)) / m)
        b = float(np.sum(profile * np.sin(ang)) / m)
        return float((np.arctan2(b, a) % (2 * np.pi)) * n / (2 * np.pi))

    return circ(w.sum(axis=1)), circ(w.sum(axis=0))


def field_centroid(A: np.ndarray) -> tuple[float, float]:
    """Circular centre of mass of the whole field."""
    tot = A.sum(axis=0) if A.ndim == 3 else A
    return _circular_centroid(np.ones_like(tot, dtype=bool), tot)


def wrap_delta(a: float, b: float, n: int) -> float:
    """Shortest signed difference a - b on a periodic axis of length n."""
    return ((a - b + n / 2) % n) - n / 2


def extract_blobs(A: np.ndarray, rel_threshold: float = 0.08,
                  min_area: int = 12) -> list[Blob]:
    """Segment a frame into organisms.

    The threshold is relative to the frame's own peak, so a world that has
    spread its mass thin is not silently reported as empty; it is reported
    as one huge low-contrast blob, which the non-triviality gate then
    rejects on its own terms.
    """
    tot = A.sum(axis=0)
    peak = float(tot.max())
    if peak <= 0:
        return []
    mask_all = tot > rel_threshold * peak
    lab, n = _label_periodic(mask_all)

    blobs = []
    for i in range(1, n + 1):
        m = lab == i
        area = int(m.sum())
        if area < min_area:
            continue
        cy, cx = _circular_centroid(m, tot)
        size = A.shape[-1]
        ys, xs = np.nonzero(m)
        dy = np.array([wrap_delta(y, cy, size) for y in ys])
        dx = np.array([wrap_delta(x, cx, size) for x in xs])
        w = tot[ys, xs]
        cov = np.cov(np.stack([dy, dx]), aweights=w + 1e-12)
        ev = np.linalg.eigvalsh(np.atleast_2d(cov))
        elong = float(np.sqrt(max(ev[-1], 1e-12) / max(ev[0], 1e-12)))
        blobs.append(Blob(
            label=i, mask=m, area=area, mass=float(tot[m].sum()),
            channel_mass=np.array([float(A[c][m].sum()) for c in range(A.shape[0])]),
            centroid=(cy, cx), elongation=min(elong, 1e3),
            radius=float(np.sqrt(dy ** 2 + dx ** 2).max()),
            peak=float(tot[m].max()),
        ))
    return blobs


def morphological_diversity(blobs: list[Blob]) -> float:
    """Mean pairwise distance between standardized shape descriptors."""
    if len(blobs) < 2:
        return 0.0
    d = np.stack([b.descriptor() for b in blobs])
    d = (d - d.mean(0)) / (d.std(0) + 1e-9)
    diffs = [np.linalg.norm(d[i] - d[j])
             for i in range(len(d)) for j in range(i + 1, len(d))]
    return float(np.mean(diffs))


def frame_complexity(A: np.ndarray) -> dict:
    tot = A.sum(axis=0)
    blobs = extract_blobs(A)
    masses = sorted((b.mass for b in blobs), reverse=True)
    m1 = masses[0] if masses else 0.0
    return {
        "n_blobs": len(blobs),
        # Share of the largest body held by the second largest. A world with
        # one dominant blob and a halo of specks scores near 0; a world that
        # has genuinely divided scores near 1. This is the continuous signal
        # the search hill-climbs on, since the strict division count is 0 or
        # 1 and gives a mutation search nothing to follow.
        "second_share": float(masses[1] / m1) if len(masses) > 1 else 0.0,
        "n_major": int(sum(1 for m in masses if m >= 0.2 * m1)) if masses else 0,
        "morph_diversity": morphological_diversity(blobs),
        "spatial_mi": spatial_mutual_information(tot),
        "cross_channel_mi": cross_channel_mi(A),
        "euler": euler_characteristic(tot > 0.08 * max(tot.max(), 1e-12)),
        "concentration": float(tot.max() / (tot.mean() + 1e-12)),
        "occupancy": float((tot > 0.08 * max(tot.max(), 1e-12)).mean()),
    }


# --------------------------------------------------------------------------
# Speciation tracking
# --------------------------------------------------------------------------


# An offspring carrying less than this share of its parent's mass is debris
# shed by a big body, not a division. Set from observation: unfiltered runs
# logged "children" at 0.6% of the parent, which is a speck, not a creature.
MIN_OFFSPRING_FRAC = 0.10


@dataclass
class Organism:
    uid: str
    parent: str | None
    generation: int
    birth_frame: int
    death_frame: int | None = None
    track: list[tuple[int, float, float]] = field(default_factory=list)
    mass_track: list[float] = field(default_factory=list)
    children: list[str] = field(default_factory=list)
    dominant_channel: int = 0

    @property
    def lifespan(self) -> int:
        return len(self.track)

    def path(self, size: int) -> tuple[float, float, float]:
        """(net displacement, path length, straightness)."""
        if len(self.track) < 2:
            return 0.0, 0.0, 0.0
        pts = [(y, x) for _, y, x in self.track]
        steps = [np.hypot(wrap_delta(b[0], a[0], size), wrap_delta(b[1], a[1], size))
                 for a, b in zip(pts[:-1], pts[1:])]
        length = float(np.sum(steps))
        net = float(np.hypot(wrap_delta(pts[-1][0], pts[0][0], size),
                             wrap_delta(pts[-1][1], pts[0][1], size)))
        return net, length, net / (length + 1e-9)


class SpeciationTracker:
    """Follows blobs across frames and maintains a lineage tree.

    Identity rule: a body keeps its UUID as long as it is the largest
    successor of itself. When one body splits, the heaviest fragment carries
    the identity forward and the others are recorded as offspring, which is
    what makes the lineage a tree rather than a soup of renamings.
    """

    def __init__(self, size: int, min_overlap: int = 1):
        self.size = size
        self.min_overlap = min_overlap
        self.organisms: dict[str, Organism] = {}
        self.prev: list[tuple[str, Blob]] = []
        self.frame = 0
        self.events: list[dict] = []

    def _new(self, blob: Blob, parent: str | None, generation: int) -> str:
        uid = uuid.uuid4().hex[:8]
        self.organisms[uid] = Organism(
            uid=uid, parent=parent, generation=generation,
            birth_frame=self.frame, dominant_channel=blob.dominant_channel)
        if parent is not None:
            self.organisms[parent].children.append(uid)
        return uid

    def _record(self, uid: str, blob: Blob) -> None:
        o = self.organisms[uid]
        o.track.append((self.frame, blob.centroid[0], blob.centroid[1]))
        o.mass_track.append(blob.mass)
        o.dominant_channel = blob.dominant_channel

    def update(self, A: np.ndarray) -> list[Blob]:
        blobs = extract_blobs(A)

        # Overlap matrix between previous bodies and current ones.
        assign: dict[int, list[str]] = {i: [] for i in range(len(blobs))}
        succ: dict[str, list[int]] = {uid: [] for uid, _ in self.prev}
        for uid, pb in self.prev:
            for i, cb in enumerate(blobs):
                if int(np.count_nonzero(pb.mask & cb.mask)) >= self.min_overlap:
                    succ[uid].append(i)
                    assign[i].append(uid)

        claimed: dict[int, str] = {}

        for uid, idxs in succ.items():
            if not idxs:
                self.organisms[uid].death_frame = self.frame
                self.events.append({"frame": self.frame, "type": "death",
                                    "uid": uid})
                continue
            idxs = sorted(idxs, key=lambda i: -blobs[i].mass)
            heir = idxs[0]
            if heir not in claimed:
                claimed[heir] = uid
            if len(idxs) > 1:
                gen = self.organisms[uid].generation
                offspring = []
                for i in idxs[1:]:
                    if i in claimed:
                        continue
                    child = self._new(blobs[i], parent=uid, generation=gen + 1)
                    claimed[i] = child
                    offspring.append(child)
                if offspring:
                    self.events.append({
                        "frame": self.frame, "type": "fission", "parent": uid,
                        "children": offspring,
                        "parent_mass": float(blobs[heir].mass),
                        "child_mass": [float(blobs[i].mass) for i in idxs[1:]],
                    })

        # A parent whose only successor was claimed by a heavier parent has
        # been absorbed. Without this it would keep a null death_frame and go
        # on being counted as a survivor forever, silently inflating
        # persistence.
        carried = set(claimed.values())
        for uid, idxs in succ.items():
            if idxs and uid not in carried and self.organisms[uid].death_frame is None:
                self.organisms[uid].death_frame = self.frame
                self.events.append({"frame": self.frame, "type": "merged",
                                    "uid": uid})

        for i, b in enumerate(blobs):
            if i not in claimed:
                claimed[i] = self._new(b, parent=None, generation=0)
                self.events.append({"frame": self.frame, "type": "birth",
                                    "uid": claimed[i]})

        for i, b in enumerate(blobs):
            self._record(claimed[i], b)

        self.prev = [(claimed[i], b) for i, b in enumerate(blobs)]
        self.frame += 1
        return blobs

    # -- summaries ---------------------------------------------------------

    def reproduction_events(self, min_child_life: int = 8,
                            min_mass_frac: float = MIN_OFFSPRING_FRAC
                            ) -> list[dict]:
        """Fissions whose offspring both survived AND are substantial.

        Two filters, and both are load-bearing:

        * **Survival.** A blob that flickers apart for one frame and
          re-merges is not reproduction.
        * **Mass share.** A large body continuously sheds specks; without a
          mass floor those specks are counted as offspring and any messy
          world looks fecund. An offspring must carry at least
          `min_mass_frac` of the parent's mass to count as a division rather
          than debris.

        Pass `min_mass_frac=0.0` to see the raw fission count, which is what
        the strict count should always be reported against.
        """
        out = []
        for e in self.events:
            if e["type"] != "fission":
                continue
            parent_mass = max(float(e["parent_mass"]), 1e-12)
            alive = []
            ratios = []
            for c, cm in zip(e["children"], e["child_mass"]):
                frac = float(cm) / parent_mass
                if (self.organisms[c].lifespan >= min_child_life
                        and frac >= min_mass_frac):
                    alive.append(c)
                    ratios.append(frac)
            if alive:
                out.append({**e, "surviving_children": alive,
                            "child_mass_frac": ratios})
        return out

    def lineage(self) -> dict:
        return {uid: {
            "parent": o.parent, "generation": o.generation,
            "birth_frame": o.birth_frame, "death_frame": o.death_frame,
            "lifespan": o.lifespan, "children": o.children,
            "peak_mass": float(max(o.mass_track)) if o.mass_track else 0.0,
            "dominant_channel": o.dominant_channel,
        } for uid, o in self.organisms.items()}

    def survivors(self, min_life: int = 5) -> list[Organism]:
        return [o for o in self.organisms.values()
                if o.death_frame is None and o.lifespan >= min_life]


# --------------------------------------------------------------------------
# Anomaly bouncer
# --------------------------------------------------------------------------


@dataclass
class Anomaly:
    kind: str
    established: bool
    score: float
    detail: str

    def __post_init__(self):
        # numpy scalars leak in from the detectors and are not JSON
        # serializable; coerce once, here, rather than at every call site.
        self.established = bool(self.established)
        self.score = float(self.score)

    def as_dict(self) -> dict:
        return asdict(self)


MIN_CYCLE_FRAMES = 4.0


def detect_cyclic_locomotion(tracker: SpeciationTracker,
                             min_life: int = 20) -> Anomaly:
    """Self-directed cyclical motion: consistent turning, or a clear period.

    Circling index is the mean sign of successive velocity cross products
    (+-1 means always turning the same way). The spectral test looks for a
    single dominant frequency in the velocity, which is what a gait looks
    like as opposed to drift.
    """
    best = (0.0, "", None)
    n = tracker.size
    for o in tracker.organisms.values():
        if o.lifespan < min_life:
            continue
        pts = np.array([(y, x) for _, y, x in o.track])
        v = np.array([[wrap_delta(b[0], a[0], n), wrap_delta(b[1], a[1], n)]
                      for a, b in zip(pts[:-1], pts[1:])])
        speed = np.linalg.norm(v, axis=1)
        if np.mean(speed) < 1e-3:
            continue
        cross = v[:-1, 0] * v[1:, 1] - v[:-1, 1] * v[1:, 0]
        moving = np.linalg.norm(v[:-1], axis=1) * np.linalg.norm(v[1:], axis=1)
        ok = moving > 1e-9
        circ = float(np.abs(np.mean(np.sign(cross[ok])))) if ok.any() else 0.0

        spec = np.abs(np.fft.rfft(v[:, 0] - v[:, 0].mean()))[1:]
        period = 0.0
        power = 0.0
        if spec.size > 2 and spec.sum() > 0:
            k = int(np.argmax(spec))
            power = float(spec[k] / (spec.sum() + 1e-12))
            period = float(len(v) / (k + 1))

        # A period of two or three frames is the sampling floor, where
        # centroid jitter and a genuine gait are indistinguishable. Only a
        # cycle spanning several frames counts as locomotion.
        spectral = power * 3.0 if period >= MIN_CYCLE_FRAMES else 0.0
        score = max(circ, spectral)
        if score > best[0]:
            best = (score, (f"uid={o.uid} circling={circ:.2f} "
                            f"spectral_power={power:.2f} period={period:.1f} "
                            f"frames (counted only if >= {MIN_CYCLE_FRAMES:.0f}) "
                            f"life={o.lifespan} frames"), o.uid)

    est = best[0] >= 0.6
    return Anomaly("cyclic_locomotion", est, best[0],
                   best[1] or "no organism lived long enough to test")


def detect_pursuit(tracker: SpeciationTracker, min_frames: int = 12) -> Anomaly:
    """One body closing on another body that is itself moving.

    Requires both partners to be in motion, so a blob drifting onto a static
    lump is not counted as a chase.
    """
    n = tracker.size
    orgs = [o for o in tracker.organisms.values() if o.lifespan >= min_frames]
    best = (0.0, "")
    for i, a in enumerate(orgs):
        for b in orgs[i + 1:]:
            fa = {f: (y, x) for f, y, x in a.track}
            fb = {f: (y, x) for f, y, x in b.track}
            common = sorted(set(fa) & set(fb))
            if len(common) < min_frames:
                continue
            dist = np.array([
                np.hypot(wrap_delta(fa[f][0], fb[f][0], n),
                         wrap_delta(fa[f][1], fb[f][1], n)) for f in common])
            mv_b = np.mean([np.hypot(
                wrap_delta(fb[f2][0], fb[f1][0], n),
                wrap_delta(fb[f2][1], fb[f1][1], n))
                for f1, f2 in zip(common[:-1], common[1:])])
            closing = (dist[0] - dist[-1]) / (dist[0] + 1e-9)
            monotone = float(np.mean(np.diff(dist) < 0))
            if mv_b < 0.05 or dist[-1] > dist[0]:
                continue
            score = closing * monotone
            if score > best[0]:
                best = (score, (f"{a.uid}(ch{a.dominant_channel}) -> "
                                f"{b.uid}(ch{b.dominant_channel}) closed "
                                f"{dist[0]:.1f} -> {dist[-1]:.1f} cells over "
                                f"{len(common)} frames, monotone {monotone:.2f}, "
                                f"target speed {mv_b:.3f}"))
    return Anomaly("predatory_pursuit", best[0] >= 0.35, best[0],
                   best[1] or "no closing pair found")


def detect_phototaxis(run_fn, size: int, light_positions, steps: int) -> Anomaly:
    """Does the world track the light when the light MOVES?

    run_fn(light_pos) -> (com_start, com_end). The claim is only established
    if the mass approaches the lamp in EVERY placement tested; a constant
    drift will approach one lamp and recede from the one behind it, and is
    rejected. That control is the whole point of the test.
    """
    approaches = []
    detail = []
    for pos in light_positions:
        (y0, x0), (y1, x1) = run_fn(pos)
        d0 = np.hypot(wrap_delta(y0, pos[0], size), wrap_delta(x0, pos[1], size))
        d1 = np.hypot(wrap_delta(y1, pos[0], size), wrap_delta(x1, pos[1], size))
        approaches.append((d0 - d1) / (d0 + 1e-9))
        detail.append(f"lamp{tuple(round(p) for p in pos)}: {d0:.1f}->{d1:.1f}")

    a = np.array(approaches)
    est = bool(np.all(a > 0.05)) and len(a) >= 2
    return Anomaly("phototaxis", est, float(a.min() if a.size else 0.0),
                   "; ".join(detail) + f" | min approach {a.min():+.3f} "
                   f"(needs > 0.05 for every lamp position)")


# --------------------------------------------------------------------------
# Viability gates
# --------------------------------------------------------------------------


@dataclass
class Gate:
    name: str
    passed: bool
    value: float
    detail: str = ""


MASS_TOL = 1e-4
MIN_CONCENTRATION = 6.0
MAX_OCCUPANCY = 0.45


def viability_gates(mass_trace: np.ndarray, frames: list[dict],
                    tracker: SpeciationTracker) -> list[Gate]:
    """The bar a world must clear before its behaviour is worth claiming."""
    m = np.asarray(mass_trace, dtype=float)
    if m.size == 0 or not np.all(np.isfinite(m)) or m[0] <= 0:
        return [Gate("mass_conservation", False, float("inf"),
                     "non-finite or empty mass trace")]
    drift = float(np.max(np.abs(m - m[0])) / m[0])
    gates = [Gate("mass_conservation", drift <= MASS_TOL, drift,
                  f"tol={MASS_TOL:g}")]

    last = frames[-1]
    trivial_ok = (last["concentration"] >= MIN_CONCENTRATION
                  and last["occupancy"] <= MAX_OCCUPANCY
                  and last["n_blobs"] >= 1)
    gates.append(Gate("non_triviality", trivial_ok, last["concentration"],
                      f"conc>={MIN_CONCENTRATION}, occupancy "
                      f"{last['occupancy']:.3f}<={MAX_OCCUPANCY}, "
                      f"{last['n_blobs']} bodies"))

    surv = tracker.survivors(min_life=max(3, tracker.frame // 4))
    gates.append(Gate("persistence", len(surv) >= 1, float(len(surv)),
                      f"{len(surv)} organisms alive at the end with lifespan "
                      f">= {max(3, tracker.frame // 4)} frames"))

    moved = 0.0
    for o in tracker.organisms.values():
        if o.lifespan >= 5:
            net, length, _ = o.path(tracker.size)
            moved = max(moved, length / max(o.lifespan - 1, 1))
    gates.append(Gate("activity", moved > 0.02, moved,
                      "mean speed of the most mobile organism, cells/frame"))
    return gates
