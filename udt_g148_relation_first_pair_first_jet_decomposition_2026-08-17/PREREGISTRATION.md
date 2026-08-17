# G148 preregistration — relation-first complete-pair first jet

Date: 2026-08-17

## Question

On one supplied regular time-oriented calibrated complete observer-pair realization, adopt only the
already owned working relation-first position constitution

\[
\boldsymbol\xi=X_{\max}\tanh(\phi_{\rm pair})\,n
\]

inside the query clock's rest space. What exact covariant first-jet decomposition follows from the
complete metric? In particular, do radial position change, rotation into the metric pair screen,
and change of the query rest space appear as pieces of one coefficient-free identity?

This is an observing calculation. It does not target a loud--quiet--loud pattern or an observational
fit.

## Exact bounded regime

- one supplied smooth regular pair immersion on a time-oriented Lorentzian four-metric;
- `h00<0`, `det(h)<0`, finite real `phi_pair`, and symbolic `X_max>0`;
- query-owned unit clock `u`, orthogonal unit ruler `n`, and metric screen
  `H_pair=span(u,n)^perp`;
- local first jet along `u` only;
- every `B,Q,S,Y,Z` block retained and independently time-live in the registered witness;
- coincidence is treated only by a limit; null, degenerate, cut, singular, and global strata are
  outside the theorem.

## Premise and choice ledger

| Item | Status | Ownership |
|---|---|---|
| complete coframe and pair pullback | `DERIVED` evaluator on supplied `B,Q,S,Y,Z` | frozen sources |
| `phi_pair=(1/4)log((-det h)/h00^2)` | `DERIVED` on the regular calibrated pair | frozen sources |
| `x/X_max=tanh(phi_pair)` | `CHOSE / WORKING_FOUNDATIONAL_CLARIFICATION`, then `DERIVED` | G136--G137 |
| `xi=X_max tanh(phi_pair)n` | `WORKING_RELATION_FIRST_REPRESENTATION` | this bounded test; not spacetime displacement |
| Levi-Civita derivative and metric orthogonal projectors | `DERIVED` from supplied metric | no GR field equations |
| `X_max` | `WORKING_FOUNDATIONAL_FRAME`, symbolic and unfixed | no numerical value |
| histories and first jets | `free-and-explored` symbolically; one rational witness for liveness | not selected as physical |
| action, source, matter, bootstrap, radiative law, observations | omitted | not load-bearing |

## Preregistered identities

Let `dot` mean `nabla_u`. Define

\[
\rho=X_{\max}\tanh\phi,\qquad
a_n=g(\nabla_u u,n),\qquad
\Omega=P_H\nabla_u n.
\]

The proposed exact identities are

\[
\dot\rho=X_{\max}\operatorname{sech}^2\phi\,\dot\phi,
\]

\[
\nabla_u\boldsymbol\xi
=\dot\rho\,n+\rho a_n u+\rho\Omega,
\]

and, after projection into the instantaneous rest space,

\[
P_{u^\perp}\nabla_u\boldsymbol\xi
=\dot\rho\,n+\rho\Omega,
\qquad
\|P_{u^\perp}\nabla_u\boldsymbol\xi\|^2
=\dot\rho^2+\rho^2\|\Omega\|^2.
\]

The terminal scalar derivative must also agree with

\[
\dot\phi
=\frac14\operatorname{tr}(h^{-1}\dot h)
-\frac12\frac{\dot h_{00}}{h_{00}},
\]

with `dot h` built from all five live blocks before readout.

## Regime characterization to report, not impose

The calculation will characterize the exact coefficient functions

\[
w_r(\phi)=\operatorname{sech}^2\phi,
\qquad
w_s(\phi)=\tanh\phi,
\]

and their neutral and asymptotic limits. It must not call those coefficients alone a physical
quiet-middle/loud-ends law, because actual amplitudes also contain `dot phi`, `Omega`, `a_n`, and the
unselected complete history.

## Certification and falsification contract

The bounded landing fails if any of the following occurs:

1. the covariant decomposition or norm split has a nonzero exact residual;
2. an extra solder coefficient, force, source, or evolution equation is required;
3. any of `B,Q,S,Y,Z` is frozen or cannot affect at least one registered first-jet output;
4. the claimed screen piece does not lie in `H_pair`;
5. an independent implementation using a different algebraic route disagrees;
6. a catch proof removing the screen or rest-space term still passes;
7. the result requires identifying `phi` with Lorentz rapidity or `xi` with proper/spacetime
   displacement.

## Maximum conclusion

At most:

```text
EXACT_RELATION_FIRST_COMPLETE_PAIR_FIRST_JET_DECOMPOSITION__
NATIVE_RADIAL_SCREEN_AND_REST_SPACE_WEIGHTS__
PHYSICAL_HISTORY_DYNAMICS_AND_OBSERVATIONAL_REGIME_PATTERN_OPEN
```

No action, source, field equation, selected history, numerical `X_max`, proper length, signal law,
bootstrap closure, matter, mass, SNe, BAO, CMB, or canon follows.
