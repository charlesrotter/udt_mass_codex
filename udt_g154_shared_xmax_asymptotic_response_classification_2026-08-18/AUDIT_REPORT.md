# G154 shared-Xmax asymptotic response classification

Date: 2026-08-18
Status: `VERIFIED_WITH_CAVEATS__FRESH_ADVERSARIAL_REPAIR_FOLLOWUP_PASS`

## Result first

The adopted **normalized** Mobius law does not derive a fixed dimensionful `X_max`. A fresh
adversarial review caught the circular step: the first derivation inserted one fixed \(X_*\) into
the dimensionful Mobius law before proving it. The strongest valid limited theorem is only this:
if a leaf is additionally supplied with that one-scale law, consistency forces
\(x=X_*\tanh\phi\) and hence \(X=X_*\) inside that leaf.

More importantly, even a conditionally supplied fixed leaf scale does not select the asymptotic
metric-frame response. With

\[
\rho=X_*\tanh\phi,
\qquad
V(\rho)=X_*\operatorname{sech}^2\phi\,V(\phi),
\]

the full product may tend to zero, a finite nonzero limit, infinity, or no limit. Exact regular
interior pair metrics realize all four classes with the same `phi(q)`, the same `rho(q)`, and the
same `X_*`; only the retained metric common scale changes.

The live-`dX` term therefore remains generally intrinsic. It is excluded only after a fixed-scale
leaf premise is independently supplied or derived. A finite common endpoint for `X` still does not
control `dX`.

## Strongest implication

The persistent gap is now exactly typed. The endpoint asymptote is a working relational frame, but
neither its fixed scale realization nor the relation between additive depth and normalized metric
clock/ruler rate is selected. The missing object is the common-scale/history law that would own
both the scale carry and the manner of approach.

## Evidence

- preregistration committed at `f5946fa0` before execution;
- production SymPy derivation: all registered checks pass;
- independent stdlib numerical/source-hash replay: all registered checks pass;
- both asymptotic orientations and temporal/spatial duals checked;
- same-profile common-scale witnesses separate all four response classes;
- live-scale endpoint, oscillation, and exact-cancellation witnesses checked;
- fresh adversarial review required repairs; its four-class replay passed, the registered type
  correction plus stronger independent checks were applied, and repair-only follow-up passed.

## Bounded landing

```text
EVEN_FIXED_LEAF_SCALE_NOT_DERIVED__RESPONSE_CLASS_NOT_SELECTED__
COMMON_SCALE_CONTROLS_NORMALIZED_APPROACH_RATE_WITHOUT_CHANGING_TERMINAL_RECIPROCAL_POSITION__
LIVE_DXMAX_REMAINS_INTRINSIC_UNTIL_FIXED_SCALE_DESCENT_IS_INDEPENDENTLY_SUPPLIED_OR_DERIVED__
GLOBAL_SHARED_XMAX_PHYSICAL_HISTORY_PROPER_LENGTH_VALUE_DYNAMICS_AND_COMPLETION_OPEN
```
