import numpy as np, json, glob
for sp in ["OSCILLIS", "MITOSA", "VAGRANT"]:
    for food in (1, 0):
        p = glob.glob("pilot/SPECIES_*%s_s1_neutral_plus_food%d.json" % (sp, food))[0]
        r = json.load(open(p)); f = r["final"]
        d = np.load(p.replace(".json", "_frames.npz"))
        b = d["body_10000"]; M = b.sum()
        print("%-8s food=%d  mass in cells<0.3 %.2f  area>0.01 %.2f  max density %.2f  blobs %2d  largest blob %.3f  body/total %.2f  food min/max %.3f/%.3f" % (
            sp, food, b[b < 0.3].sum() / M, (b > 0.01).mean(), b.max(), f["n_blobs"], f["largest_blob_frac"],
            f["body"] / (f["body"] + f["food"]) if f["food"] > 0 else 1.0, d["food_10000"].min(), d["food_10000"].max()))
