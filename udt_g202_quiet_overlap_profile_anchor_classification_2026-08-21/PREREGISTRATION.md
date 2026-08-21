# G202 preregistration — quiet-overlap profile and anchor classification

Date: 2026-08-21

Status: `PREREGISTERED_BEFORE_CONFIRMATORY_IMPLEMENTATION`

## Predicted landing

```text
QUIET_OVERLAP_FORCES_SECOND_ORDER_FLATNESS
__TWO_SIDED_GROWTH_HAS_INFINITE_NATIVE_PROFILES
__ANCHORS_CALIBRATE_BUT_DO_NOT_DERIVE_HISTORY
```

## Exact variables

Let

```text
s=log(r/r0)
P=d phi/ds
Q=d^2 phi/ds^2.
```

Then G201's jets satisfy `p=P` and `q=Q-P`.  Preregister the transformed amplitudes

```text
A_parallel=exp(-2phi)(2P^2+2P-Q)
A_perp=1-exp(-2phi)(1+P).
```

## Required theorems and controls

1. At a zero-depth overlap, both angular modes vanish iff `phi=P=Q=0`.
2. If an analytic profile changes sign there and is not identically zero, its first nonzero Taylor
   order is odd and at least three.
3. The minimal nondegenerate control is `phi=a s^3`, `a>0`; it is monotone, reaches both signed
   depth extremes, and remains a supplied control rather than a selected law.
4. The infinite family `phi=a s^3 + sum b_k s^(2k+1)` with nonnegative coefficients supplies
   distinct lawful monotone examples sharing the quiet second jet.
5. For the cubic control, derive the exact angular amplitudes and their leading quiet-middle orders.
6. Finite smooth point/jet anchors do not select a unique global profile: compactly supported
   perturbations away from the anchors preserve them, and sufficiently small perturbations preserve
   monotonicity on their support.
7. Dimensional basis: `c_E` alone cannot form a length; `c_E` and `G_obs` alone still retain mass
   dimension.  A mass anchor permits `G_obs M/c_E^2`; a density anchor permits
   `c_E/sqrt(G_obs rho)`.  These are dimensional candidates, not derived physical scale laws.
8. No finite anchor set or dimensional candidate is to be promoted to a global history selector.

## Independent verification

Use no SymPy and import no production code.  Require at least 20,000 exact-rational polynomial
crossing cases checking the transformed amplitudes, quiet jets, monotonicity for nonnegative odd
coefficients, and equality of finite anchor jets under explicit polynomial perturbations.  Verify
the dimensional exponent systems independently using exact linear algebra.

## Falsification

The predicted landing fails if quietness does not require the full zero second jet, if two-sided
growth is incompatible with a smooth positive primary metric at every finite `s`, if the lawful
profile class collapses to one member, or if `c_E,G_obs` alone determine a length without importing
a mass-dimension anchor.

## Maximum conclusion

Classify necessary local profile conditions and the information content of anchors.  Do not select
the physical history, fit data, derive `X_max`, import P1/G116/G189, or add transfer, source, action,
matter, mass dynamics, bootstrap, or signalling.
