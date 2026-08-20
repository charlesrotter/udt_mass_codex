# G192 preregistration — smooth time-live mixing family classification

Date: 2026-08-20

## Whole question and exact bounded regime

Which parts of the externally accepted G191 frequency/screen result are identities of its complete
coframe architecture, and which parts depend on the special constant choices
`a(eta)=exp(H eta)` and `mu(eta)=constant`?

The bounded arena is one smooth coordinate neighborhood with coordinates `(eta,z,x,y)`, an interval
`I` containing `eta=0`, and the complete coframe

\[
\begin{aligned}
\theta^0&=a(\eta)\,d\eta,\\
\theta^1&=a(\eta)\,dz,\\
\theta^2&=a(\eta)\left[dx+\frac{\mu(\eta)}{\sqrt2}(x+y)(d\eta+dz)\right],\\
\theta^3&=a(\eta)\left[dy+\frac{\mu(\eta)}{\sqrt2}(x+y)(d\eta+dz)\right],\\
g&=-(\theta^0)^2+(\theta^1)^2+(\theta^2)^2+(\theta^3)^2,
\end{aligned}
\]

where `a` is an arbitrary positive `C^3` function on `I`, normalized by `a(0)=1`, and `mu` is an
arbitrary real `C^2` function on `I`. No monotonicity, sign, asymptote, or observational profile is
imposed.

The supplied completed pair remains

\[
F(\tau,\sigma)=(\eta=\tau,z=\sigma,x=0,y=0),
\]

with source vertex at the origin and the `+z` ruler orientation selecting the outgoing germ. The
classification is local on every regular subinterval of `I`; it does not select an endpoint or a
global observer population.

## Metric-led versus template-led

This is metric-led. The connection, affine ray, frequency, parallel screen, curvature tide, and
matrix Jacobi initial-value problem must be recomputed from the displayed complete metric with
unevaluated functions and independently checked on nonconstant function families. G191 is a required
specialization, not a formula source.

## Premise and choice ledger

| Item | Status | Role |
|---|---|---|
| `c_E` | `OBSERVED`, set to one in dimensionless control units | clock/ruler calibration only |
| completed-pair Dual Reciprocity | `WORKING_FOUNDATIONAL_CLARIFICATION` | applies after the full pullback |
| displayed coframe architecture | `CHOSE_MATHEMATICAL_FUNCTION_FAMILY` | bounded smooth sector extending G191, not the complete ten-function arena |
| `a(eta)>0`, `a(0)=1` | `free-and-explored` plus source-unit calibration | arbitrary common-scale history on the interval |
| real `mu(eta)` | `free-and-explored` | arbitrary signed mixing history on the interval |
| `C^3`/`C^2` regularity | `pinned-by-MATHEMATICAL_OPERATOR_ORDER` | enough derivatives for curvature and certified residuals |
| central pair and `+z` ruler orientation | `CHOSE_QUERY` | fixes one completed pair and local outgoing germ |
| affine parameter and frequency | `DERIVED_CONDITIONAL` | must follow from the same metric and source normalization |
| full rank-two Jacobi screen | `DERIVED_CONDITIONAL` | no scalarization or fitted angular coefficient |
| P1, G116, G189, static `phi(R)`, `R(Z)` | `OMITTED` | forbidden construction inputs |
| transfer, luminosity, source state, observations | `OMITTED` | no radiative or SNe claim |
| `X_max` | `OMITTED` | possible later global consequence only |

## Whole-space and omitted-sector ledger

This push explores the full function space of `a(eta)>0` and real `mu(eta)` within the displayed
coframe architecture. It does not explore arbitrary dependence on `(z,x,y)`, the other independent
complete-coframe mixing channels, general screen anisotropy or rotation, different pair surfaces,
both ruler orientations at once, singular metrics, global cut loci, endpoint populations, topology,
emission, transfer, source physics, action, dynamics, matter, bootstrap, or global completion.

Those omissions may host other behavior. Therefore every conclusion is scoped to this two-function
complete-coframe family.

## Preregistered derivation gates

1. Reconstruct `g=E^T eta_4 E`; prove `det E=a^4` and Lorentzian regularity for every `a>0`.
2. Pull back `g` to the supplied pair and reconstruct its completed orthonormal clock, ruler, and
   two normalized null germs.
3. Derive the selected central affine ray, the exact `lambda(eta)` relation, frequency, and
   differential contraction law with arbitrary `a` and `mu`.
4. Derive a parallel orthonormal screen and the full self-adjoint `2 x 2` tidal matrix including all
   `a'`, `a''`, `mu`, and `mu'` terms that actually survive.
5. Rotate only as an analysis device into fixed symmetric/antisymmetric screen modes; retain the
   original-screen matrix response in the reported result.
6. Solve the vertex-normalized matrix Jacobi IVP exactly when possible, or give an exact quadrature
   and certified ODE characterization. Require `D(0)=0`, `D'(0)=I` in affine parameter.
7. Classify frequency turns without imposing monotonicity. A claimed `d_A(Z)` is permitted only on
   locally one-to-one, noncaustic pieces.
8. Classify every determinant zero/caustic allowed by this function family. Do not discard a
   caustic or force one to exist.
9. Recover G191 for `a=exp(H eta)`, constant positive `mu`; recover the G190 conformal screen for
   `mu=0`; recover the G188 static-mixing normalization for `a=1`, constant `mu`.
10. Independently replay multiple nonconstant analytic and numerical function families without
    importing production code or reading its outputs. Include monotone, turning, signed-mixing,
    zero-crossing-mixing, and near-singular-but-regular controls.

## Preregistered certification and falsification contract

The proposed classification fails if any of the following occurs:

- the coframe or pair pullback loses the claimed regularity for allowed `a>0`;
- the central tangent is not an affine null geodesic;
- the frequency contraction identity fails;
- the screen is not parallel/orthonormal or the tide is not self-adjoint;
- any derivative term is dropped by specializing before curvature is computed;
- the matrix Jacobi residual or vertex normalization fails;
- any one of the three exact regression limits fails;
- a numerical control contradicts the symbolic/quadrature classification beyond the registered
  tolerance;
- the result filters out turns, caustics, or signs because they are physically inconvenient.

Certification requires exact symbolic residuals where tractable, independent numerical errors below
`2e-9` on a preregistered bounded function census, hostile mutation catches, the current premise
verifier, full repository tests, and `git diff --check`.

## Maximum conclusion

At most G192 may classify frequency turns, screen mixing, and caustics for this supplied smooth
two-function complete-coframe family and identify which G191 statements are family identities versus
constant-control specializations. It cannot select the physical UDT history, claim the family is the
general complete metric, derive transfer or luminosity, predict observations, establish `X_max`, or
derive dynamics, action, source, matter, mass, bootstrap, or signalling.
