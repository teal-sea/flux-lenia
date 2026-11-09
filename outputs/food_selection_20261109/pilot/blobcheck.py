import numpy as np, sys
sys.path.insert(0, ".")
from scipy import ndimage
from engine import novelty_oracle as no
d = np.load("pilot/SPECIES_001_OSCILLIS_s1_neutral_plus_food1_frames.npz")
b = d["body_10000"]; M = b.sum(); peak = b.max()
mask = b > 0.08 * peak
lab, n = ndimage.label(mask)
sizes = ndimage.sum(b, lab, range(1, n + 1))
print("peak %.2f thr %.3f  mask area %.2f  mass in mask %.2f  plain components %d  largest component mass frac %.3f" % (peak, 0.08 * peak, mask.mean(), b[mask].sum() / M, n, sizes.max() / M))
lp, npl = no._label_periodic(mask)
print("periodic labels", npl, "max label", lp.max())
bl = no.extract_blobs(b[None])
print("extract_blobs:", len(bl), "masses frac", sorted([round(x.mass / M, 3) for x in bl])[-5:], "areas", sorted([x.area for x in bl])[-5:])
