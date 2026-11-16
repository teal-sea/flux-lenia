#!/usr/bin/env python3
"""Drop the four Config keys added after SPECIES_001..003 were written, when they hold their defaults.

engine/neural_field.py at ce00383 serialises genome_transport, repulsion_kappa, repulsion_radius and
repulsion_genome_dims; SPECIES_001..003 predate them. Config(**data["config"]) fills the defaults, so removing
default-valued keys keeps the loaded world identical and the file schema identical to the existing three.
Refuses to drop a key that is not at its default. Usage: species_strip_defaults.py FILE...
"""
import json, sys
DEFAULTS = {"genome_transport": "mean", "repulsion_kappa": 0.0, "repulsion_radius": 8.0, "repulsion_genome_dims": 8}
for f in sys.argv[1:]:
    d = json.load(open(f))
    for k, v in DEFAULTS.items():
        if k in d["config"]:
            assert d["config"][k] == v, (f, k, d["config"][k])
            del d["config"][k]
    open(f, "w").write(json.dumps(d, indent=2))
