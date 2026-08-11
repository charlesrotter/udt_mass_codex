# First-production implementation correction preregistration

Date: 2026-08-11

Parent performance-refinement commit: `b1797af0`

The complete first production return is preserved as `FIRST_PRODUCTION_*`. No physical conclusion
was drawn from it.

## Reproduced defects

1. **Gauss sign:** with the registered convention
   `R(X,Y)Z=nabla_X nabla_Y Z-nabla_Y nabla_X Z-nabla_[X,Y]Z`, the implementation compared
   `ambient-intrinsic-extrinsic`. The correct rearrangement for the implemented component is
   `ambient-intrinsic+extrinsic`. The R17 first return exposes the exact doubled-extrinsic signature:
   its nonconvergent residual is approximately twice the separately reported extrinsic term.
2. **Jacobi slot typing:** the implementation contracted the ambient tensor as `R(v,v)J`, which
   vanishes by antisymmetry, instead of `R(J,v)v`. The printed Q2 residual was therefore only the
   second covariant derivative term and cannot certify or refute Jacobi compatibility.
3. **Nested finite-difference conditioning:** the unregistered internal surface-jet step
   `2e-5` is too close to the adaptive ODE error floor for second and third query derivatives.
   The Q2 Gauss/Codazzi rows worsen under the outer registered refinement while the algebraic,
   Ricci, transport-metric, and loop-quadrature controls remain small. This is classified as a
   numerical-conditioning defect, not a geometric result.

## Frozen repairs

- Change only the Gauss rearrangement sign.
- Change only the Jacobi curvature contraction to `R(J,v)v` under the declared tensor indexing.
- Set the internal surface-jet difference to `2e-4`; retain the registered outer scales
  `0.004,0.002,0.001`, DOP853 tolerances, witnesses, query definitions, and all channels.
- Add explicit raw terms for the Jacobi balance and convergence ratios to the output.
- Preserve the first implementation and outputs in git history.

No result value or landing is predicted. Failure of the corrected residuals to converge remains a
preregistered `NUMERICALLY_UNRESOLVED_COMMON_IMMERSION_TEST`.
