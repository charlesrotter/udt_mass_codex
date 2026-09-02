# G325 audit report — homogeneous diagonal first variations of G324

Date: 2026-09-02

Grade: `EXTERNALLY_ACCEPTED_AFTER_R1_EVIDENCE_REPAIR`

## Bounded landing

```text
HOMOGENEOUS_DIAGONAL_MODES_CLOSE_AS_TIME_GAUGE__THREE_QUOTIENT_LATTICE_MODULI
__ONE_LOCAL_KASNER_SHEAR__ONE_CONNECTED_SCALAR_MODE__NO_FULL_STABILITY_CLAIM
```

For the complete spatially homogeneous diagonal synchronous first-variation sector around every
registered G324 compact Taub quotient, the adopted trace-free Ricci equation has exactly six
constants:

- one residual time-origin gauge mode;
- three fixed-quotient lattice moduli;
- one genuine local Kasner shear;
- one connected scalar-curvature variation.

The general solution, exact residuals, quotient classification, curvature witnesses, and parameter
count were derived by production algebra, reconstructed by an implementation-distinct direct
Christoffel/Riemann engine, and independently rederived by the fresh external reviewer. Repair R1
removed one non-load-bearing tautological production assertion. The repair-only reviewer then ran
all registered commands and obtained byte-identical artifacts.

This is not full linear stability: off-diagonal homogeneous modes and every nonzero Fourier mode
remain unclassified. It is not nonlinear stability, singularity avoidance, physical occupancy,
topology or universe selection, scale calibration, or `X_max`. No metric, reciprocal kernel,
angular-sector formula, source, action, matter model, observation, or new equation was introduced.

## Four evidence gates

1. Preregistered: `PASS`, commit `3875663f`.
2. Full bounded space: `PASS`, complete ODE solution in the declared diagonal homogeneous sector.
3. Independently verified: `PASS`, direct tensor engine plus fresh external derivation and repair
   replay.
4. Premise audited: `PASS`, owner-provisional Universal Reciprocity/DDR and G312 premises remain
   explicit; trace-free Ricci is active only in its bounded declared arena.
