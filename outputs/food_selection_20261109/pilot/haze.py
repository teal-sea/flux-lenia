import numpy as np, glob
for p in sorted(glob.glob("pilot/*_frames.npz")):
    d = np.load(p); print(p.split("/")[-1][12:20])
    for t in [0, 2500, 5000, 10000]:
        b = d["body_%d" % t]; f = d["food_%d" % t]; M = b.sum()
        print("  t=%5d area>0.01 %.2f  area>0.3 %.2f  mass in cells<0.1 %.2f  <0.3 %.2f  food min/max %.3f/%.3f"
              % (t, (b > 0.01).mean(), (b > 0.3).mean(), b[b < 0.1].sum() / M, b[b < 0.3].sum() / M, f.min(), f.max()))
