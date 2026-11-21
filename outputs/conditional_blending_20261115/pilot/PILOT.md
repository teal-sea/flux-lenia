# Pilot: choose kappa (2026-11-15)

Rule and candidates: docs/CONDITIONAL-BLENDING-2026-11-15.md (Pilot). 12 runs, 10,000 steps each, run on InstaBox box flux-lenia-step2-w1 (m_agq6dc6cqnfwkrte3cd4jrpyb4, 8 vCPU / 16 GiB), 8 concurrent single-thread runs, batch 23:33:59 to 23:38:14 UTC. Python 3.13.5, jax 0.11.1, numpy 2.5.2, scipy 1.18.1, CPU, float64. Nothing ran on citadel. Per-run JSON and frames are in k<kappa>/. Table from `python scripts/conditional_blending_summary.py pilot`.

## Pilot runs (seed 1, treat, food on, per_channel, 10,000 steps)

Control (repulsion off, 2026-11-10) hybrid fraction at step 10,000: OSCILLIS 0.857 (half 0.429), MITOSA 0.927 (half 0.463)

| kappa | species | hybrid | pure | blobs | largest blob | max drift | sat with (mean over samples) | sat without | excess | wall s | hybrid <= half control | drift ok | sat ok |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.1 | OSCILLIS | 0.831 | 0.169 | 73 | 0.093 | 4.9e-16 | 0.0000 | 0.0000 | +0.0000 | 118 | no | yes | yes |
| 0.1 | MITOSA | 0.899 | 0.101 | 43 | 0.085 | 4.9e-16 | 0.0000 | 0.0000 | +0.0000 | 119 | no | yes | yes |
| 0.3 | OSCILLIS | 0.835 | 0.165 | 54 | 0.177 | 6.1e-16 | 0.0000 | 0.0000 | +0.0000 | 116 | no | yes | yes |
| 0.3 | MITOSA | 0.943 | 0.057 | 36 | 0.150 | 3.7e-16 | 0.0000 | 0.0000 | +0.0000 | 117 | no | yes | yes |
| 1 | OSCILLIS | 0.826 | 0.174 | 56 | 0.054 | 3.7e-16 | 0.0000 | 0.0000 | +0.0000 | 119 | no | yes | yes |
| 1 | MITOSA | 0.312 | 0.688 | 32 | 0.189 | 3.7e-16 | 0.0000 | 0.0000 | +0.0000 | 116 | yes | yes | yes |
| 3 | OSCILLIS | 0.139 | 0.861 | 50 | 0.064 | 4.9e-16 | 0.0000 | 0.0000 | +0.0000 | 118 | yes | yes | yes |
| 3 | MITOSA | 0.002 | 0.998 | 33 | 0.143 | 3.7e-16 | 0.0000 | 0.0000 | +0.0000 | 120 | yes | yes | yes |
| 10 | OSCILLIS | 0.000 | 1.000 | 47 | 0.092 | 7.4e-16 | 0.0000 | 0.0000 | +0.0000 | 108 | yes | yes | yes |
| 10 | MITOSA | 0.000 | 1.000 | 37 | 0.115 | 2.5e-16 | 0.0000 | 0.0000 | +0.0000 | 107 | yes | yes | yes |
| 30 | OSCILLIS | 0.000 | 1.000 | 45 | 0.047 | 8.6e-16 | 0.0000 | 0.0000 | +0.0000 | 107 | yes | yes | yes |
| 30 | MITOSA | 0.000 | 1.000 | 15 | 0.172 | 4.9e-16 | 0.0000 | 0.0000 | +0.0000 | 107 | yes | yes | yes |

**Chosen kappa = 3** (smallest candidate that qualifies for both species; qualifying: 3, 10, 30).

Saturation: the largest single-sample fraction of body velocities at the soft bound over all pilot runs was 4.0e-4 (kappa 30, MITOSA); 0 for every other candidate; without the term 0 everywhere.
