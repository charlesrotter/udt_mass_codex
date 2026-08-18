# G153 relational-position / ruler differential join audit

Date: 2026-08-17
Status: `VERIFIED_WITH_CAVEATS` after fresh adversarial repair and follow-up

## Result

The finite G137 observer-pair position

\[
\rho=X_{\max}\tanh\phi_{\rm pair}
\]

is not automatically a proper metric length. G147's vector `rho n` is a conditional rest-space
picture, and G152's metric ruler is `r=L n`. Their finite equality is destroyed by an exact common-
scale counterexample, so it is not the premise-owned join.

On one supplied smooth regular calibrated pair family, the correctly typed native join is instead
the exact first differential

\[
\boxed{d\rho=u(\rho)\theta^0+n(\rho)\theta^1.}
\]

For a possibly varying asymptotic-scale realization,

\[
\boxed{u(\rho)=\tanh\phi\,u(X_{\max})
+X_{\max}\operatorname{sech}^2\phi\,u(\phi),}
\]

\[
\boxed{n(\rho)=\tanh\phi\,n(X_{\max})
+X_{\max}\operatorname{sech}^2\phi\,n(\phi).}
\]

These coefficients are derived once the smooth complete pair history and `X_max` realization are
supplied. The pair metric keeps `T`, `L`, shift `beta`, time dependence, and the complete upstream
orchestra inside this response. Fixed `X_max` is only a conditional subcase.

The squared-gradient diagnostic

\[
h^{-1}(d\rho,d\rho)=-u(\rho)^2+n(\rho)^2
\]

is exact, but its causal type depends on the supplied history. The optional conditions
`n(rho)=+/-1` or `d rho=+/-theta1` would add a local proper-ruler calibration and are not adopted.

## Evidence gates

1. Preregistered in commit `18060cba`: `PASS`.
2. Bounded scope justified: `PASS`; this is a first-differential/type audit, not a global solve.
3. Independently verified: `PASS`; symbolic production and separate exact-Fraction replay.
4. Premises audited: `PASS`; proper length, history, value, and completion remain open.
5. Fresh adversarial gate: initial `REPAIR_REQUIRED`, repaired, then `FOLLOWUP_PASS`.

## Maximum conclusion

```text
G137_OWNS_FINITE_RELATIONAL_POSITION_NOT_METRIC_PROPER_RULER_LENGTH__
G147_REST_SPACE_VECTOR_LIFT_REMAINS_CONDITIONAL__
FINITE_CHORD_EQUALS_LOCAL_RULER_IS_NOT_THE_NATIVE_JOIN__
ON_A_SUPPLIED_SMOOTH_PAIR_FAMILY_D_RHO_HAS_AN_EXACT_METRIC_FRAME_DECOMPOSITION_WITH_DERIVED_TEMPORAL_AND_SPATIAL_RESPONSE_COEFFICIENTS__
UNIT_RULER_IDENTIFICATION_PROPER_LENGTH_HISTORY_XMAX_VALUE_AND_GLOBAL_COMPLETION_OPEN
```
