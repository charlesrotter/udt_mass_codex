# Audit report — recovered `mu_lock` crosswalk

## Result

The August 6 result was neither lost physics nor already a complete modern scalar. It has an exact,
restricted home inside the modern geometry:

```text
M_pq=Q_q(S_q-S_p)B_p^-1,
mu_lock=-[M_pq]_(screen,clock)
```

on the supplied one-screen, reference-calibrated endpoint transition. The minus sign comes from the
fact that the August upper arrow is the metric adjoint of the lower coframe transition.

The complete release replaces that one coefficient by a `2x2` transition matrix. The old
rank-one slice cannot select a unique scalar on this four-component space. Moreover, the terminal
pair metric depends on `SY+Z`, so an exact `S/Z` fiber changes the ambient mixing transition while
leaving the pair readout fixed. The August invariant is therefore a full-arrow channel, not a
universal synonym for terminal `phi_pair` or `c_eff/c_E`.

## Evidence

- Primary SymPy route: 14/14 exact checks pass.
- Independent no-SymPy Fraction route: 9/9 exact checks pass.
- Hostile mutations: 4/4 caught.
- The original `s!=r` scope and `s=r` gauge carve-out are retained.

## Four gates

1. Preregistered: **PASS** — question, candidate landings, falsifiers, and conclusion ceiling were
   written before the derivation scripts ran.
2. Full space or bounded scope: **PASS FOR DECLARED SCOPE** — full algebraic `2x2` modern mixing was
   released; the endpoint carry is explicitly limited to a supplied block-preserving identity carry.
3. Independently verified: **PARTIAL PASS** — an implementation-independent exact Fraction replay
   verifies the load-bearing algebra; a fresh-context semantic adversary remains owed.
4. Premises audited: **PASS** — arrow, coframe, pair pullback, carry, and physical ownership are kept
   type-distinct.

## Grade

`INTERNALLY_VERIFIED_WITH_CAVEATS`. This is not canon and does not select a scalar, history, regime
score, action, source, matter law, bootstrap relation, or observational prediction.

## Smallest justified next action

A fresh semantic adversary should try to break the variance convention, the endpoint-transition
formula, the rank-one extension theorem, and the pullback non-recovery witness. No further solve is
needed unless that review identifies a mathematical error.
