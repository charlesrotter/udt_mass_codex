# G72 metric screen-response join — preregistration

Date: 2026-08-11

Base commit: `074e8939eb24ee2644f1472b4ce9ef6d42c8dbb8`

## Whole question

Once a regular ordered observer-sky query, path, endpoint screens, and complete metric branch are
supplied, does the metric itself determine a source-free orientation-sensitive response object, or
does every orientation-sensitive CMB readout still require an independently supplied source or
detector law?

This is a metric-led type and invariant-classification problem. It is not a CMB fit, a search for a
desired peak pattern, or a source model.

## Exact bounded arena

Let `S_s` and `S_o` be oriented positive-definite two-dimensional screen spaces at the supplied
source and observer endpoints. On a regular no-caustic branch, the supplied query provides:

- an invertible Jacobi/image map `D:S_s->S_o`;
- an oriented metric screen isometry `U:S_s->S_o` from the supplied path transport;
- endpoint screen metrics and their independent oriented orthonormal-frame gauges.

The relative response is provisionally typed as

```text
M = U^-1 D : S_s -> S_s.
```

The audit will classify algebraic/order-zero response data from `(D,U)` under independent endpoint
screen-frame changes. It will separately test area/focusing, shear magnitude and tensor, relative
polar rotation, open-path gauge dependence, and action on scalar and orientation-sensitive source
states.

## Premise ledger

| Object | Status | Ownership in this audit |
| --- | --- | --- |
| complete Lorentzian metric/coframe | `DERIVED` / current banked geometry | supplies screen metrics and connection conditionally on a branch |
| ordered physical CMB query | `OPEN` | not selected here |
| regular pair/path realization | `CONDITIONAL` | supplied bounded query |
| `D` | `DERIVED_CONDITIONAL` | Jacobi/image map on the supplied regular query |
| `U` | `DERIVED_CONDITIONAL` | metric screen transport on the supplied path |
| screen orientations | `CHOSE_QUERY` unless the branch supplies them | reflection quotient audited separately |
| source field/covariance/polarization | `OPEN` | absent from the source-free classification |
| detector/radiation response | `OPEN` | not imported |
| `c_E` | `OBSERVED` calibration | fixes clock-length units; not a response selector |
| global size / `X_max` / profile | `WORKING` / `OPEN` | retained symbolically; no value or surface selected |
| SNe P1 | `CONDITIONAL` low-redshift anchor | inactive except as a future compatibility bracket |

No action, source law, bootstrap selector, last-scattering surface, local signal law, or physical
CMB spectrum is supplied.

## Registered claims to test

1. A single open-path `U` has no orientation scalar invariant under independent endpoint frame
   rotations.
2. Because `D` and `U` have the same source and target, `M=U^-1 D` transforms only by source
   conjugation. Its polar rotation angle is invariant under oriented `SO(2)` source gauge and flips
   sign under reflection.
3. The singular values of `D`, equivalently the positive polar factor of `M`, own source-free area
   and shear-magnitude response. A shear axis is gauge-covariant rather than an absolute scalar.
4. A complete source-free geometric response operator can therefore exist without becoming a
   physical TT/TE/EE/BB observable.
5. Zero or constant scalar source data remain zero or constant under a purely geometric pullback;
   metric transport reshapes supplied structure but does not populate a nontrivial sky state.
6. An orientation-sensitive source tensor is transported covariantly, but its observed value is
   not fixed until that source tensor and a measurement contraction are supplied.
7. The endpoint Jacobi block `D` alone is not a composable observer-network functor; composition
   belongs to the full Jacobi transfer state. No false groupoid law may be assigned to `D`.

## Falsification and certification contract

The strongest positive landing is allowed only if all of the following pass:

- exact symbolic gauge transformation of `D`, `U`, and `M`;
- exact two-dimensional polar/decomposition identities on a declared positive-determinant stratum;
- independent numerical `SO(2)xSO(2)` gauge trials;
- reflection-sign and degeneracy tests;
- explicit zero-source and constant-scalar counterchecks;
- full-source-freedom consistency with G71;
- a catch-proof rejecting promotion of a geometric response operator to a physical CMB observable;
- a catch-proof rejecting multiplication of endpoint Jacobi blocks as the full transfer law.

Failure at a caustic, negative/zero determinant, missing orientation, or absent common source/target
typing must be reported as a domain boundary, not repaired by a fitted convention.

## Registered landings

Exactly one primary landing will be used:

1. `METRIC_OWNS_SOURCE_FREE_SCREEN_RESPONSE__PHYSICAL_OBSERVABLE_OPEN`;
2. `ONLY_SCALAR_FOCUS_SHEAR_OWNED__RELATIVE_ROTATION_NOT_OWNED`;
3. `NO_NEW_RESPONSE_JOIN__G71_BOUNDARY_UNCHANGED`;
4. `TYPE_OR_REGULARITY_FAILURE`.

Even landing 1 may claim only a conditional geometric response operator. It may not claim CMB
temperature or polarization power, a source, a physical endpoint/profile, a global scale, or an
observed spectrum.

## No-go / success interpretation

A positive response classification would support the possibility that distance dilation and the
angular sector geometrically distort a supplied remote pattern as an observer-frame effect. It
would not prove that geometry creates the initial pattern. A negative response classification
would route the missing joint directly to source/observation ownership rather than another inverse
rank scan.
