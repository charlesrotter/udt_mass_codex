# Reciprocal–transverse-twist C2 Jacobi audit — preregistration

Date: 2026-07-20

Base: `ee5690c49f27d230e5b802d08af9e36b5213f5ae`

Branch: `codex/c2-reciprocal-transverse-twist-jacobi-2026-07-20`

Mode: CPU-only exact symbolic/automatic-differentiation metric audit

## Whole question

The banked static finite-box Hopfion is a full three-dimensional nonround/toroidal texture, while
the latest bounded conditional metric-only `C2` solution-space search observed only the round metric
orbit. Earlier null-section, projective-transport, transverse-realization, and Cartan/holonomy audits
already show that simply relabeling a winding frame or celestial direction as the carrier is not
gauge invariant. The Cartan audit explicitly left one local calculation undone: embedding its
transverse twist inside a nontrivial reciprocal coframe.

This audit asks:

> In the conditional pre-scale metric-only `C2` branch, what exact quadratic operator does the full
> curvature action assign to a genuine off-diagonal transverse twist when it is coupled to an
> arbitrary nontrivial reciprocal dilation profile? Does background reciprocal curvature generate a
> definite lower-derivative twist term alongside the higher-derivative term, or does the complete
> calculation leave, cancel, or destabilize that structure?

This is `METRIC_LED` and `OBSERVING`. It does not target a particle, Hopf charge, mass, stable lump,
or desired coefficient ratio. Every sign and zero mode is retained and characterized.

## Exact bounded frame

Use the four-dimensional coframe

```text
e0 = exp[-p(r)] dt
e1 = exp[+p(r)] dr
e2 = dx
e3 = dy + epsilon*u(r) dx
g  = -e0^2 + e1^2 + e2^2 + e3^2.
```

The twist-free member has the reciprocal clock/parallel product exactly. `u(r)` is a transverse
off-diagonal metric degree of freedom. Constant `u` is a coordinate/frame shear and must be an exact
zero mode; only invariant derivatives may survive. The calculation retains arbitrary local jets of
`p(r)` and `u(r)` and expands the full scalar density `sqrt(-g) C_abcd C^abcd` through order
`epsilon^2` before varying `u`.

The local radial interval is unspecified. No physical finite-cell boundary condition is installed.
When integration by parts is displayed, both the bulk Jacobi operator and the complete boundary
variation are retained separately. Polynomial or analytic profiles used for independent numeric
checks are test witnesses only, not physical solutions.

## Premise ledger

| Object | Status |
|---|---|
| The metric is the theory | `pinned-by-THEORY` |
| Reciprocal exponential clock/parallel character | `DERIVED-CONDITIONAL` under the frozen sign, unit, representative, and slot premises |
| Four-dimensional conformal-Lorentzian readout | `INHERITED / CONDITIONAL` |
| Metric-only local `C2` bulk action | `UNIQUE-CONDITIONAL` inside the frozen pre-scale action class; not the complete UDT action |
| Static cohomogeneity-one block and flat local transverse base at zero twist | `pinned-by-HABIT / BOUNDED SLICE` |
| Off-diagonal twist `u(r)` | `free-and-varied` through quadratic order; no shape or sign selected |
| Reciprocal profile `p(r)` | `free symbolic background` in the twist Jacobi calculation; not varied to solve its own equation here |
| Small parameter `epsilon` | category-A bookkeeping for the exact Hessian/Jacobi operator, not a small-physical-field claim |
| Constant-twist coordinate zero mode | `pinned-by` diffeomorphism covariance and independently checked |
| Local interval and chart `(t,r,x,y)` | `pinned-by-HABIT / LOCAL TILE`; global periods/topology absent |
| Boundary values of `u,p` | `OPEN`; none imposed |
| Physical representative, scale, finite-cell wall/caps | `OPEN / EXCLUDED` |
| Carrier, round `S2`, Hopf section, `L2+L4`, source, mass | `OPEN / EXCLUDED` |
| Symbolic simplification, finite differences, AD, rational witnesses | category-A methods |

The background is not required to solve the full Bach equation. Therefore a background-dependent
twist Jacobi density is an off-shell metric Hessian result unless the background is separately shown
on shell. No stability conclusion may be drawn from it.

## Frozen calculations

1. Construct the full metric, inverse, determinant, connection, Riemann, Ricci, scalar, Weyl, and
   `C2` density directly from the coframe with no reduced GR equation.
2. Expand the exact density through `epsilon^2`; verify the linear coefficient vanishes.
3. Prove that the quadratic density contains no undifferentiated `u` and vanishes for constant `u`.
4. Derive the higher-derivative Euler/Jacobi operator and the complete endpoint variation from that
   quadratic density without choosing boundary data.
5. Classify independently the coefficients of `u''^2`, `u'u''`, and `u'^2`, including their signs
   and dependence on `p,p',p''` after removal only of exact total derivatives.
6. Independently reconstruct the curvature density with a separate coordinate-tensor
   implementation at preregistered analytic profiles and compare the `epsilon^2` coefficient.
7. Compare the action-derived Jacobi operator with the direct linearized full metric Euler/Bach
   projection at selected local jets. If a fully independent direct Bach implementation is not
   completed, the result must remain `LEAD` rather than a promoted field-equation statement.
8. Check the limits `p=constant`, `u=constant`, flat reciprocal background, and reversal `u -> -u`.
9. Exercise mutation catches for a missing `epsilon^2 u^2` metric backreaction term, Euclidean time
   sign, frozen `p` derivatives, discarded boundary variation, action-only circular verification,
   constant-twist false stiffness, and promotion to a carrier or Hopf conclusion.

## Frozen outcome classes

1. `BACKGROUND_CURVATURE_GENERATES_BOTH_DERIVATIVE_ORDERS` — the one conditional metric invariant
   yields a nonzero background-dependent lower-derivative twist term plus a higher-derivative term.
2. `PURE_HIGHER_DERIVATIVE_TWIST_OPERATOR` — all lower-derivative terms cancel after exact boundary
   separation.
3. `TWIST_QUADRATIC_OPERATOR_DEGENERATE_OR_TOTAL_BOUNDARY` — no nontrivial local twist Hessian
   remains in this tile.
4. `TWIST_OPERATOR_SIGN_OR_BRANCH_DEPENDENT` — coefficients change sign or vanish across allowed
   reciprocal jets; characterize the strata rather than selecting one.
5. `CALCULATION_OR_VERIFICATION_INCONCLUSIVE` — independent tensor/Bach disagreement or resource
   limits prevent classification.

No outcome may be renamed a Hopfion, carrier, matter action, stability theorem, or native UDT action.

## Completeness limits

This is one local Jacobi tile. It omits unrestricted ten-component metrics, angular dependence,
global linking, nontoric topology, nonperturbative twist amplitudes, genuine time dependence,
variation of `p` and every metric component together, physical boundary/corner action, bootstrap
closure, scale, matter, source, and stability. Any omitted sector can change the result.

## Falsification and certification contract

- Exact symbolic identities must simplify to zero and be independently checked numerically at
  multiple rational/profile witnesses.
- Logged and independently recomputed quadratic density/Jacobi values must agree to relative
  `1e-8` in float64 or exactly in symbolic arithmetic.
- A nonzero constant-`u` density or Jacobi residual fails the audit.
- A claimed lower-derivative bulk coefficient that can be removed completely into the recorded
  boundary variation fails the corresponding outcome.
- Any direct Bach comparison exceeding relative `1e-7` is a verification failure.
- No retuning of profiles, signs, or outcome wording after inspection.

Maximum positive conclusion:

`CONDITIONAL_LOCAL_C2_RECIPROCAL_TRANSVERSE_TWIST_JACOBI_STRUCTURE_CHARACTERIZED`.

Even a successful two-order structure would remain a metric-shape Hessian, not the historical
carrier `L2+L4`, and would not derive the carrier, topology, physical scale, complete action, source,
boundary charge, stability, or mass.
