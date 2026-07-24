# User framing addendum: directional separation and `X_max`

Recorded after preregistration and after the first exact cap calculation.
It does not change the frozen solder-family test or its certification
contract.

Charles clarified that `X_max` should remain a consequence sought from the
complete UDT metric, not be treated as an optional postulate. He also raised
the possibility that angular structure could produce tiny directional
variations, potentially visible later in CMB observations.

The noncircular geometric definitions to test next are:

```text
X(p,n) = limiting/cut distance from observer p in allowed direction n,

X_max  = sup over allowed observer pairs (p,q) of d_h(p,q).
```

A round completion has constant `X(p,n)`. A nonround completion can have a
narrow directional distribution while retaining one scalar supremum
`X_max`. If one instead uses the name `X_max(n)` for the directional
quantity, the absolute maximum must still be distinguished from it.

Status:

- complete-metric two-point distance: `DERIVED` once a physical observer-rest
  metric and observer pairing are supplied;
- direction-dependent endpoint distribution: `OPEN`;
- scalar global diameter/supremum: `OPEN_NOT_EVALUABLE` in the current
  branch census;
- CMB relation: `OBSERVATIONAL_COMPARISON_OPEN`, not an input to this audit.

This clarification supports rather than weakens the current cap result. The
failure of one smooth global scalar to cover both caps makes a relational
two-observer definition more natural, but does not yet select it.
