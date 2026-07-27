# Complete non-ultrastatic reciprocal-branch audit — preregistration

Date: 2026-07-27

Base: `e912c09`

## Whole question

Without adopting an action or choosing endpoint-versus-path semantics globally, does the complete
finite-cell metric configuration space contain a globally regular non-ultrastatic clock/angular
branch in which intrinsic metric data supply:

1. a timelike observer line;
2. a nontrivial signed reciprocal depth;
3. a spatial ruler line; and
4. the founded local clock/ruler weights?

This is a law-neutral existence, regularity, and intrinsic-structure audit. Its objects are metric
configurations, not on-shell solutions.

## Why this class

Existing complete `S3` controls have angular structure but trivial clocks. WR-L has a nontrivial
local clock profile but no complete all-observer geometry. Static diagonal same-scalar reciprocal
toric soldering is obstructed at a primitive cap. Shifted, twisted, nonintegrable, and time-live
complete coframes remain open. Cross-branch splicing is forbidden.

The audit therefore tests stationary twisted coframes directly. It does not attach the WR-L profile
to an existing complete branch.

## General bounded configuration frame

On a complete finite spatial cell `Sigma`, a stationary metric with supplied time orientation is
written law-neutrally as

```text
g=-N^2 dt^2+h_ij(dx^i+beta^i dt)(dx^j+beta^j dt),
```

or in a globally supplied coframe. `N`, `h`, and `beta` are free configuration data. Stationarity,
the finite-cell class, any global coframe, and any isometry stratum are recorded rather than called
derived universal UDT laws.

The exact twisted `S3` witness family uses global Maurer-Cartan forms with

```text
d sigma_3 = kappa sigma_1 wedge sigma_2,
tau = c_E dt + a sigma_3,
theta_0 = exp(-phi) tau,
theta_1 = R exp(+phi) sigma_3,
theta_2 = R exp(lambda phi) sigma_1,
theta_3 = R exp(lambda phi) sigma_2,
g = -theta_0^2+theta_1^2+theta_2^2+theta_3^2.
```

Here `phi` is any registered smooth profile on `S3`, `lambda` is free, and `a`, `R`, and `kappa`
remain explicit. The family must not select a profile, `lambda`, orientation, scale, or dynamics.

## Frozen strata and witnesses

- `CONFIGURATION_STRATUM_UNIVERSE.tsv`
- `WITNESS_UNIVERSE.tsv`
- `PROPERTY_GATE_UNIVERSE.tsv`
- `FALSIFICATION_CONTRACT.tsv`
- `PREMISE_LEDGER.tsv`
- `SOURCE_SCOPE.tsv` and `SOURCE_MANIFEST.tsv`

Generated records may not modify these universes.

## Required exact tests

1. Check global coframe invertibility, Lorentz signature, stationary Killing norm, and positive
   induced spatial slice condition.
2. Derive the normalized Killing-norm depth and test normalization independence, reversal,
   composition, self-depth, and nontriviality.
3. Compute the twist one-form from `star(K_flat wedge dK_flat)` and determine its spatial line.
4. Separate a supplied stationary line from an intrinsic unique timelike Killing line.
5. Test an explicit generic-lapse round-`S3` control: for
   `f(x)=sum_i d_i x_i^2` with distinct `d_i`, prove no nonzero round spatial Killing generator
   preserves `f`.
6. Audit static/twist-free, twisted, multiple-Killing, causal-degenerate, boundary, quotient, and
   time-live strata without deleting any.
7. Determine whether the branch supplies only depth or also the full observer/ruler pair.
8. Keep endpoint depth in this stationary stratum separate from the globally open physical
   endpoint-versus-path semantics.

## Certification contract

`CONDITIONAL_INTRINSIC_STATIONARY_DEPTH` requires a metric-intrinsic timelike Killing **line**, a
positive nonconstant norm, a normalization-independent scalar difference, and exact founded clock
alignment. A merely supplied coordinate `t` is insufficient.

`CONDITIONAL_INTRINSIC_STATIONARY_PAIR` additionally requires a nonzero metric-derived spatial line,
such as the Killing twist line, with exact causal orthogonality and the recorded reciprocal ruler
weight. It must disclose any sign/orientation ambiguity and every global regularity condition.

No result may call the configuration on shell, selected, stable, unique across all UDT metrics, or a
complete observer law.

## Maximum conclusion and stop

At most:

```text
LAW_NEUTRAL_COMPLETE_NONULTRASTATIC_CONFIGURATION_CLASS_CLASSIFIED;
CONDITIONAL_STATIONARY_INTRINSIC_DEPTH_OR_PAIR_STRATA_EXPLICIT;
NO_ACTION_DYNAMICS_PROFILE_LAMBDA_OR_GLOBAL_SEMANTICS_SELECTED.
```

Stop before equations of motion, action adoption, density/bootstrap solves, empirical comparison,
carrier/source work, GPU work, canonization, or startup-control edits.
