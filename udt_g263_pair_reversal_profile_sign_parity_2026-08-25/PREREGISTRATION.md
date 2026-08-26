# G263 preregistration

Date: 2026-08-25
Status: `PREREGISTERED_BEFORE_OUTCOME_ALGEBRA`

## Frozen objects

Use only:

\[
D(\delta)=\operatorname{diag}(e^{-\delta},e^{+\delta}),
\quad f=e^{-2\phi}>0,
\quad N=e^{-\phi},
\]

\[
p=r\phi',\qquad z=r^2\phi'',\qquad
\mu=\frac r2(1-f),
\]

and the already-derived G201/G260/G262 channel formulas. The symbol `z` replaces G201's jet symbol
`q` here so it cannot be confused with the endpoint clock factor `q_pair=e^{-delta}`.

## Operations

- `R_pair`: `delta -> -delta`, fixed ambient `phi(r)` and fixed complete metric.
- `C_phi`: `(phi,p,z) -> (-phi,-p,-z)`, equivalently `f -> 1/f`, fixed endpoint order.
- Even/odd parts of any channel `F` under an involution `I` are
  `F_even=(F+I(F))/2` and `F_odd=(F-I(F))/2`.

## Candidate outcomes

1. `FULL_EQUIVALENCE`: both involutions agree on every registered channel.
2. `SCALAR_EQUIVALENCE_ONLY`: they agree on reciprocal scalar inversion but differ on at least one
   complete-metric channel.
3. `NO_STABLE_PARITY`: even the reciprocal scalar does not admit a lawful involutive split.

No candidate is preferred before calculation.

## Tests

1. Exact symbolic involution and parity closure for `D`, endpoint clock factor, `N`, `f`, `mu`,
   signed static acceleration, `E0`, `E1`, `A_parallel`, and `A_perp`.
2. Exact proof that `R_pair` leaves the ambient metric fixed.
3. Exact comparison of `g_phi` and `g_-phi`, including the unchanged areal sphere.
4. At least 10,000 implementation-distinct rational substitutions spanning both signs of `phi`
   through a positive rational proxy for `exp(2 phi)`.
5. Applied mutation catches for confusing endpoint reversal with profile conjugation, forcing mass
   aspect oddness, deleting the sphere distinction, and asserting lockstep angular loudness.

## Certification and falsification

The result fails if any displayed parity identity fails exact substitution, either map is not an
involution, the two operations are called identical despite a separating channel, or the evidence
promotes a diagnostic parity split into a profile-selection, mass, source, or dynamics law.

## Maximum conclusion

An exact local parity classification on arbitrary real primary `phi` with `f>0`. No physical
history, pair population, universal orchestra score, mass law, or asymptotic completion may be
claimed.
