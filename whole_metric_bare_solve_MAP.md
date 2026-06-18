# Bare Whole-Metric Solve — SETUP MAP (no compute)

Date: 2026-06-18. Driver: Claude (Opus 4.8, 1M). MODE = MAP (frame + premise
ledger, NO computation). Frame: CRITICAL_UNIVERSE_FRAME.md (governing) + CANON
C-2026-06-18-1 (the relativistically-derived bare metric form) + CANON C-2026-06-10-2
(finite-cell). DATA-BLIND. Brought to Charles for check BEFORE any solve runs.

## Purpose
Re-anchor on the actual program (Charles, restated 2026-06-18): solve the METRIC on its
own, with NOTHING imposed, and analyze the solution space for what it PRODUCES. UDT is an
EXTENSION OF GR and MUST REMAIN RELATIVISTIC; borrow GR numerical methods for TRACTABILITY
ONLY, never to impose approximations or assumptions. Let structure (charge, particles,
EM, ...) EMERGE; name nothing in advance.

## The governing setup (what we solve)
- LAW: Einstein's equations (GR — the framing UDT extends). The metric is primary; energy
  curves it; Misner-Sharp energy is READ OFF the solved metric (emergent diagnostic, not
  an input).
- STRUCTURE HELD (DERIVED, C-2026-06-18-1): the relativistic dilation form — exponential
  clock law + the reciprocal tie B=1/A along the dilation-gradient direction. phi defined
  up to an additive constant.
- DOMAIN: the finite mirrored cell with the seal (same-minus / time-reversal mirror fold)
  (CANON C-2026-06-10-2) — the only boundary/regularity, derived.
- MATTER SLOT: EMPTY of anything external. The only energy allowed is the metric's OWN
  content. No posited field, no chosen action, no ansatz.
- DELIVERABLE: a map of the solution space — which self-consistent geometries exist on the
  cell, what (if any) structure appears, each with a regime stamp. OBSERVE.

## What is HELD vs FREE (the C-2026-06-18-1 split — binding)
HELD (derived, not chosen):
- Einstein's equations (GR).
- Exponential dilation law + B=1/A along grad phi (C-2026-06-18-1).
- Finite mirrored cell + seal (C-2026-06-10-2).

FREE (the solution space — MUST NOT be smuggled; these are CHOICES per C-2026-06-18-1):
- the angular / transverse metric block (including whether r^2 dOmega^2 is the right form),
- all off-diagonal / shift terms (rotation, shear, frame-dragging),
- the TIME-dependence of phi / the metric (non-stationary allowed),
- the chart (areal r is a choice),
- the topology.

## THE CENTRAL HONEST QUESTION (must be confronted, not assumed)
With Einstein + NO external matter, WHERE does non-trivial structure come from? Pure vacuum
GR with nothing in it is trivial (flat / Schwarzschild) — the "empty-room problem." Three
candidates, to be DECIDED BY THE SOLVE, not pre-chosen:
  (a) CLOSURE pins it: the finite MIRRORED cell + seal closing consistently on itself may
      force a non-trivial self-consistent geometry with no source (the critical-universe
      "the whole closes only one way" idea). Structure from the global boundary condition.
  (b) SELF-GRAVITATING / GEON: the metric's own DYNAMICAL content (time-dependent
      angular/off-diagonal fields) carries energy that self-traps (geon literature, charter
      mine, principle 4). REQUIRES time to be LIVE.
  (c) TRIVIAL: no non-trivial structure — itself an informative result (would say static
      geometry holds nothing; structure must be dynamical or non-existent).

*** SMUGGLE-WATCH (the load-bearing warning) ***: imposing STATIC is the suspected past
smuggle. Static vacuum tends to trivial; and the program's static failures (the winding
catalog's import-held multiplicity, the box-controlled single-cell spectrum) may ALL stem
from freezing time — which C-2026-06-18-1 now shows is a CHOICE, not a consequence. So time
should be treated as LIVE unless we explicitly TEST that freezing it does not kill structure.
This is the key fork for the first pass (see Tractability) — Charles's call.

## PREMISE / CHOICE LEDGER (chose or derived?)
| Item | tag |
|---|---|
| Einstein's equations govern | HELD (UDT extends GR — owner principle) |
| Exponential dilation law + B=1/A along grad phi | DERIVED (C-2026-06-18-1) |
| Finite mirrored cell + seal | DERIVED/CANON (C-2026-06-10-2) |
| Nothing external in the matter slot | HELD (owner: solve the metric on its own) |
| phi up to a constant (gauge) | DERIVED (C-2026-06-18-1, R1) |
| Static (d/dt = 0) | CHOICE — suspected wrong smuggle; default LIVE unless tested |
| Spherical symmetry | CHOICE — must be tested, not assumed |
| Diagonal metric (no off-diagonals) | CHOICE — must be tested |
| Areal radius (rho = r) | CHOICE (a chart); was a theorem only under macro-data anchoring |
| Any grid/spectral/solver method | category-A conditioning only (tractability), never physics |

## TRACTABILITY PLAN (build up; every reduction STATED + TESTED)
- The fully-free solve (all 10 components, time-dependent, no symmetry) is NR-grade. We
  build toward it; we do NOT pretend a reduced slice is the whole (the slice-not-whole scar).
- THE FIRST-PASS FORK (Charles's call): given the empty-room logic + the static-smuggle
  warning, do we (i) keep TIME LIVE from the start (a dynamical / geon-type solve — harder,
  but the honest place structure may live), or (ii) run the closed-cell VACUUM-static solve
  first to test candidate (a) (closure pins it) cheaply, KNOWING static may be trivial and
  treating a null as "structure is dynamical," not "no structure"?
- Whichever: borrow GR numerics (spectral, Newton, continuation, NR evolution, SCF) for
  TRACTABILITY ONLY; every symmetry reduction tagged CHOICE + a relax-and-test plan.

## WHAT COUNTS AS "OBSERVING THE SOLUTION SPACE"
Report which self-consistent geometries exist; any localized curvature / energy
concentrations (candidate structure, read via Misner-Sharp); regime stamps; verifier pass.
Name nothing ("particle", "charge", "EM") in advance — read features off the solution.

## STATUS
MAP only. No compute run. Awaiting Charles's check + the first-pass fork decision
(time-live vs closed-cell-static-first).
