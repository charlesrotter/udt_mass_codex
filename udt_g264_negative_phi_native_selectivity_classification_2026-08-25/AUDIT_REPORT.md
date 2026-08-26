# G264 audit report — negative-phi native selectivity

Date: 2026-08-25
Grade: `EXTERNAL_ACCEPT_PACKAGING_REPAIR__PRODUCTION_SYMPY_REPLAY_NOT_RERUN_EXTERNALLY`

## Primary landing

```text
NEGATIVE_PHI_SIGN_ALONE_DOES_NOT_SELECT
__FINITE_ARBITRARILY_DEEP_SMOOTH_ASYMPTOTICALLY_FLAT_SLICE_COMPLETE_COUNTERFAMILY_EXISTS
__UNBOUNDED_NEGATIVE_ENDS_HAVE_AN_ALPHA_TWO_CURVATURE_ACCELERATION_AND_SLICE_COMPLETENESS_THRESHOLD
__THE_ALPHA_TWO_CRITICAL_REPRESENTATIVE_IS_THE_G201_ZERO_TIDE_FAMILY
```

## What was learned

Negative `phi` is not automatically more selective: sign alone rejects nothing. An explicit two-parameter family remains
strictly negative away from the center, can reach arbitrarily large finite negative depth, is
smooth-centered and asymptotically flat, has bounded scalar and Kretschmann curvature for every
finite member, and has a complete static spatial slice.

Unbounded negative ends are more structured. Under the conditional asymptotic assumption
`f~C(r/L)^alpha`, `alpha=2` is the exact common threshold for curvature, normalized static
acceleration, and radial static-slice completeness. The exact critical representative
`f=1+C(r/L)^2` is also the G201 zero-angular-tide family: both native angular channels vanish while
curvature and acceleration approach finite nonzero values.

That coincidence is derived but not a physical selection law. No source, physical mass positivity,
field equation, energy condition, observational outcome, or `X_max` profile was used.

## Evidence

- direct four-dimensional symbolic Christoffel/Ricci/Riemann replay: 27/27 checks;
- independent dependency-free metric-first tensor derivation: 250 arbitrary exact jets, constructing
  the connection and curvature before comparison, with 1,000 assertions;
- result-blind implementation-distinct consistency replay: 12,000 exact rational assertions and
  6,025 high-precision Decimal assertions;
- exact independent alpha-two/G201 intersection: 1,000 cases;
- mutation checks: 18/18 caught; fail-closed package verification: pass;
- repository regression suite: 167 passed, 1 expected xfail;
- 245-row current-premise registry audit: pass;
- fresh external adversarial review: `ACCEPT_WITH_REPAIRS`; bounded landing accepted unchanged;
- registered replay-independence repair: R1--R3 accepted;
- final packaging-repair follow-up: `ACCEPT_PACKAGING_REPAIR`; seven sealed sources resolved without
  Git and 3/3 packaging mutations caught;
- qualification: the final external runtime lacked SymPy, so the locally certified 27-check
  production script was not rerun there; the dependency-free metric-first derivation did rerun.

## Maximum conclusion

Within the primary static-spherical metric, sign alone does not select negative profiles. Growth
and radial jets produce invariant conditional classes, and the alpha-two critical class has an
already-owned zero-angular-tide representative. Physical population, history, dynamics, and
`X_max` remain open.
