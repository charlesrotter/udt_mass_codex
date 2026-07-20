# Conditional C2 Nonlinear Stationary Solution-Space Exploration

Date: 2026-07-20

Base: `786d00a05a4475fcd8495645d39ee2897f5185b3`

Preregistration commit: `111c56a`

Mode: CPU float64 tensor construction and bounded spectral/Galerkin root census

## Result

`ONLY_ROUND_COORDINATE_CSN_ORBIT_OBSERVED_AMONG_147_CERTIFIED_ROOTS_IN_BOUNDED_SEARCH`

with the load-bearing caveat

`51_PREREGISTERED_ATTEMPT_BASINS_UNRESOLVED; NO_BRANCH_EXCLUSION`.

The conditional stationary toric metric varied all four retained functions `N(eta)`, `H(eta)`,
`S(eta)`, and `W(eta)` together, including the nonlinear `W^2` backreaction. The census ran every
preregistered seed at polynomial orders two and four in the unrestricted, seal-even, and
seal-odd-shift sectors: 198 attempts total.

Of those, 147 reached raw stationarity residual at or below `1e-9`. Every one passed a separate
projection using twice the quadrature and two additional polynomial degrees; the largest validation
residual was `6.626992185076909e-9`, below the registered `1e-7` gate. Their largest gauge-fixed
coefficient norm was `1.3830808433406037e-10`. They form six bookkeeping clusters—one per
order/sector—but all six represent the same round, untwisted metric.

The other 51 attempts did not admit a residual-decreasing step under the frozen Newton/Broyden
solver. They were preserved as unresolved basins. Forty-eight use the larger `0.20` seed norm; only
three use `0.05`. Their failure is not classified as an absent solution. It may reflect
conditioning, a fold, a basin boundary, a runaway, or an additional branch.

## Exact and independent anchors

- The round cylinder has maximum computed Weyl-squared magnitude about `1.7e-23` and raw
  stationarity error about `1e-13`.
- A constant nonround squashing reproduces the previously derived pointwise Weyl density to about
  `1.1e-9` and its integrated action to about `7.1e-15`.
- The package verifier separately reconstructs the metric and curvature with NumPy and finite
  coordinate differences at nonconstant, shifted test profiles rather than calling the primary
  tensor routine.
- Every source is replayed by blob and SHA-256 from the frozen base. Mutation catches reject missing
  attempts, hidden validation failures, merit filtering, coframe-copy promotion, and UDT-wide
  overstatement. The independent tensor reconstruction separately checks the full shifted metric,
  determinant, scalar curvature, and Weyl-squared contraction.

## Interpretation

The conditional round conformally flat geometry is more than a linearized accident: it has a broad
observed nonlinear basin in this smooth-cap toric stationary tile when lapse, radial shape,
squashing, and shift backreact together. This strengthens the earlier Jacobi and angular rigidity
lead within their shared premises.

It does not establish uniqueness. The unresolved large-amplitude directions lie inside the tested
ansatz, and major completeness layers lie outside it. The result also cannot select between seal
coframe lifts that induce the same metric: a metric-only `C^2` action is exactly blind to a sign
choice erased by `g=e^T eta e`.

## Scope and evidence grade

The result is `VERIFIED-WITH-CAVEATS`: preregistered; complete for the exact 198-attempt finite
census; independently reconstructed on the tensor and raw-count premises; every physical and
numerical premise audited. No fresh different-model review was authorized.

This is one bounded completeness tile. It does not cover a physical finite-cell boundary,
endpoint-singular branches, nontoric or alternative topology, unrestricted ten-component metrics,
genuine time dependence, another action, carrier/source emergence, scale, `X_max`, total mass, or
particle mass. It supplies neither a UDT rigidity theorem nor the missing complete-coframe selector.
