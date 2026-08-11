# Independent-verifier preregistration

Date: 2026-08-11

Production status when frozen: corrected production outputs exist; no independent implementation
has been written or run.

## Independent method

- duplicate the two metric/coframe formulas without importing `solve_common_query.py`;
- centered real finite differences rather than production complex-step metric derivatives;
- fixed-step classical RK4 rather than adaptive DOP853 for the time-live observer and exponential
  rulings;
- independent surface-jet scales;
- recompute ambient and normal curvature generators and compare them to the saved production finite
  loop returns, rather than importing production curvature;
- rerun the exact plane/cylinder equal-metric unequal-extrinsic control.

## Frozen gates

1. Both pair metrics are Lorentzian and rank two.
2. Pair-metric reconstruction residual `<1e-7`.
3. R17 terminal `phi_pair=phi` defect `<1e-7`.
4. R17 declared leaf `s`-ruling acceleration norm `>1e-4`; it must remain
   `NOT_OWNED_BY_QUERY` for the geodesic Jacobi channel.
5. Time-live Fermi `s`-ruling acceleration norm `<1e-5`.
6. Independent Gauss residual `<5e-4` on both queries.
7. Time-live Jacobi balance residual divided by the larger nonzero term `<5e-3`.
8. Independent ambient/normal curvature-generator norms agree with the smallest production
   finite-loop return divided by area to relative error `<0.15`.
9. Plane/cylinder control has equal first fundamental form and unequal second fundamental form.
10. No production evaluator import and no physical-selection promotion.

Codazzi is deliberately not certified by this reduced independent verifier. The production Q2
Codazzi refinement is nonmonotone and remains `NUMERICALLY_UNRESOLVED` unless a later independent
higher-jet implementation closes it. Ricci is checked through the independently rebuilt normal
curvature generator but not claimed as a full exhaustive tensor replay.

Maximum verifier verdict: `VERIFIED_WITH_CAVEATS` for the bounded channel-ownership and common-
immersion compatibility result.
