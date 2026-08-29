"""Canvas tools, kept free of Streamlit so they can be tested directly.

The viewport's whole interaction model is "arm a tool, click the world".
Each tool is a pure function of (world, position) that returns the line it
wants written to the log, including when it did nothing: a brush stroke on
vacuum reports zero mutated cells rather than implying an edit happened.
"""

from __future__ import annotations

import numpy as np

from engine import neural_field as nf

# Channel mixes give each preset a visual identity on top of its genome.
PRESET_MIX = {
    "PREDATOR": np.array([1.0, 0.15, 0.15]),
    "SWARMER":  np.array([0.15, 1.0, 0.3]),
    "PLANT":    np.array([0.2, 0.35, 1.0]),
    "AMOEBA":   np.array([0.7, 0.7, 0.7]),
}

TOOLS = ("Spawn", "Mutate", "Scalpel", "Light")


def apply_click(world: nf.World, tool: str, cy: float, cx: float,
                preset: str = "AMOEBA", brush: float = 14.0) -> str:
    """Act on the world at a clicked cell. Returns a log line."""
    if tool not in TOOLS:
        raise ValueError(f"unknown tool {tool!r}; expected one of {TOOLS}")

    if tool == "Spawn":
        mix = PRESET_MIX.get(preset)
        if mix is not None and mix.size != world.cfg.channels:
            mix = np.resize(mix, world.cfg.channels)
        world.spawn(cy, cx, nf.preset_genome(preset, world.cfg),
                    radius=brush, peak=1.2, channel_mix=mix)
        return f"spawned {preset} at ({cy:.0f}, {cx:.0f}), r={brush:.0f}"

    if tool == "Mutate":
        hit = world.mutation_brush(cy, cx, radius=brush, strength=0.6)
        return (f"radioactive brush at ({cy:.0f}, {cx:.0f}): {hit} live cells "
                f"mutated" + ("" if hit else " — hit vacuum, genome unchanged"))

    if tool == "Scalpel":
        removed = world.scalpel(cy, cx, radius=brush)
        return (f"scalpel at ({cy:.0f}, {cx:.0f}) removed {removed:.1f} mass; "
                f"baseline reset")

    world.set_light(cy, cx)
    return f"lamp moved to ({cy:.0f}, {cx:.0f})"
