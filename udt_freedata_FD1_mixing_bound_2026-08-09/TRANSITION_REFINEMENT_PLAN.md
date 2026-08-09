# FD1 transition-refinement freeze

Date: 2026-08-09
Status: frozen before transition calculation

The first pass exposed four sampled joint neighborhoods and eight entry/exit brackets. This bounded
step refines those brackets without changing any physical or observational rule.

## Frozen brackets

| `q/qcrit` | wall | edge | original bracket |
|---:|:---:|:---:|:---|
| 0.75 | D | entry | 0.001–0.002 |
| 0.75 | D | exit | 0.02–0.05 |
| 0.75 | N | entry | 0.002–0.005 |
| 0.75 | N | exit | 0.02–0.05 |
| 0.95 | D | entry | 0.1–0.2 |
| 0.95 | D | exit | 0.5–1.0 |
| 0.95 | N | entry | 0.1–0.2 |
| 0.95 | N | exit | 0.5–1.0 |

Each bracket has one outside and one inside witness across all three SNe-conditioned `n` values.

## Contract

- Bisect every bracket for eight log-midpoint steps at grids 180 and 240.
- Define the joint sign from both registered conditions: full centered multiplet containment and the
  report-only historical RA2 3.1% comparison line. Record which condition controls each edge.
- Require the two boundary estimates to differ by less than `0.10` in absolute log ratio. This is a
  convergence diagnostic, not a physical precision claim.
- Recompute both original endpoints at grid 320 and at grid 240 with asymptotic joins 10x and 100x
  deeper. Every variant must preserve the original inside/outside orientation.
- Require every recomputed raw backward residual below `1e-8`.
- Preserve every spectral/readout row used by the refinement.
- Do not add intermediate `q`, wall, profile, source, or observational choices.

The 3.1% line remains report-only. These boundaries describe where the preregistered historical
comparison label turns on/off; they do not derive a selector, CMB phase, or physical exclusion.

Maximum conclusion: numerically converged transition brackets for the first-pass affine-comparison
window, still pending an independent solver and semantic/premise audit.
