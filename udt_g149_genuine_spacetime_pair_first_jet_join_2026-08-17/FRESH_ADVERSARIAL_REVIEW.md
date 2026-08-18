# G149 fresh adversarial review

Date: 2026-08-17

Initial landing: `REPAIR_REQUIRED`

The reviewer found the core differential geometry sound:

- pullback and chain rules were correct;
- the Christoffel construction was torsion-free and metric-compatible;
- `u,n` normalization and screen-projection signs were correct;
- `dot(phi_pair)`, `a_n`, and `Omega` came from the same supplied metric/query history;
- the G148 identity vanished exactly;
- the independent replay agreed at approximately `1e-18`;
- source-manifest hashes matched.

Required repairs:

1. Replace the initial `lambda` surrogate with G148's exact registered combined `h_dot/phi_dot`
   fixture, or withdraw the catch; describe it only as fixture-specific misuse evidence.
2. Independently replay the five `B,Q,S,Y,Z` removal controls because liveness appears in the
   maximum conclusion.
3. Narrow `Y,Z` liveness to the pair-clock (`tau`) direction; `F_sigma_sigma` was not exercised.
4. Correct the geometry wording: `B,Q,S` are affine, while assembled `E` is smooth and generally
   quadratic through `Q(x)S(x)`.
5. Attribute `dot(phi_pair)` to the normalized pair-clock derivative and reserve the explicit
   Levi-Civita dependence for `a_n,Omega`.

No repair requested a new physical premise, parameter, solve, or desired outcome.

