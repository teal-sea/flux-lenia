# Food pilot (calibration only), 2026-11-09

Written before the pilot runs. The pilot checks only that the food parameters give a living dish. It uses the neutral arm (both lineages genetically identical), so it shows nothing about whether one genome beats the other.

Parameters under test: `Food(uptake=0.05, decay=5e-4, diffusion=0.1)`, initial food uniform and equal in total to the body mass.

Runs: SPECIES_001_OSCILLIS, SPECIES_002_MITOSA, SPECIES_003_VAGRANT; seed 1; arm neutral_plus; food on; 10,000 steps.

Viability, all three must hold for every species at step 10,000:
1. `sum(body) + sum(food)` drift below 1e-10 relative.
2. Body holds more than 50% of the total, so bodies are not starved into food.
3. Structure persists: the largest blob holds at least 5% of body mass, and the maximum cell density is at least 0.2.

If a species fails, the parameters change and the pilot reruns. Every try is recorded in the experiment write-up.
