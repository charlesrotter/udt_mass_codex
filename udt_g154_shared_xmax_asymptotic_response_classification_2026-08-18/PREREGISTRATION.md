# G154 preregistration — shared-Xmax asymptotic response classification

Date: 2026-08-18
Status: `PREREGISTERED_BEFORE_DERIVATION`

## Whole question

For the G153 exact differential

\[
\rho=X\tanh\phi,
\qquad
V(\rho)=\tanh\phi\,V(X)+X\operatorname{sech}^2\phi\,V(\phi),
\]

determine what a supplied composition-compatible observer-relation network actually forces as
\(\phi\to\epsilon\infty\), \(\epsilon=\pm1\). In particular:

1. Does the adopted native Mobius position law force one fixed `X` along a connected compositional
   leaf, or can `dX` remain intrinsic to that same leaf?
2. Does a shared finite endpoint `X_*` force the metric-frame response `V(rho)` to vanish?
3. Do Reciprocity, reversal, and matched-depth composition select a quiet, finite-live, divergent,
   or nonconvergent response class?

If the current premises do not select a class, the negative must be scoped and the next deliverable
is a cold metric-first external-consultation problem statement rather than another local census.

## Bounded regime

- one supplied smooth regular calibrated relation family or network branch;
- finite interior pair metrics with `X>0` and signed additive depth;
- full nonlinear `tanh`/`sech^2` law; no linearization;
- both asymptotic signs and arbitrary normalized metric-frame derivative `V`;
- exact distinction between a compositional leaf and transverse family/modulation directions;
- asymptotic approach only; the endpoint itself need not belong to the manifold.

Null, degenerate, cut-locus, branch-junction, material, radiative, action, source, bootstrap,
observational, numerical-value, proper-length, and global-completion strata are omitted.

## Premise and choice ledger

| object | status | role |
|---|---|---|
| complete pair pullback and terminal `phi_pair` | `DERIVED_ON_SUPPLIED_PAIR` | upstream metric readout |
| `rho=X tanh(phi_pair)` | `CHOSE / DERIVED_DOWNSTREAM` | working finite relational position |
| additive depth and native Mobius composition | `DERIVED_ON_MATCHED_COMPOSABLE_DEPTHS` | compositional-leaf law |
| one fixed dimensionful Mobius scale on a leaf | `OWNER_UNDER_TEST` | possible consequence of the adopted same-law constitution |
| `X` varying transversely or between families | `OPEN / FREE_AND_EXPLORED` | live-modulation class |
| `V=u` or `V=n` | `DERIVED_FROM_SUPPLIED_PAIR_METRIC` | normalized frame response direction |
| asymptotic sign `epsilon=+/-1` | `FREE_AND_EXPLORED` | both orientations tested |
| positive witness exponent `p` | `FREE_AND_EXPLORED` | spans response-rate classes; not physics |
| simple diagonal witness metric | `FREE_AND_EXPLORED_COUNTERFAMILY` | disproves only a universal selector if all gates pass |
| proper length, history, `X` value, completion | `OPEN` | prohibited inference |

## Preregistered classes

For each normalized frame direction define the exact two contributions

\[
A_V=\tanh\phi\,V(X),
\qquad
B_V=X\operatorname{sech}^2\phi\,V(\phi),
\qquad
R_V=A_V+B_V.
\]

Classify `R_V` without filtering:

1. `QUIET`: `R_V -> 0`;
2. `FINITE_LIVE`: `R_V -> r`, finite and nonzero;
3. `DIVERGENT`: `|R_V| -> infinity`;
4. `NONCONVERGENT`: none of the preceding limits exists.

Within `QUIET`, distinguish termwise quieting from finite or divergent cancellation. A finite
zero-order endpoint is not allowed to stand in for a first-derivative conclusion.

## Preregistered tests

1. Re-derive the continuous same-scale Mobius homomorphism by applying `artanh(x/X_*)`; determine
   whether `x(phi)=X(phi)tanh(phi)` permits nonconstant `X` on one unit-slope compositional leaf.
2. Prove the exact zero-order equivalence between `phi -> epsilon infinity`, `X -> X_*`, and
   `rho -> epsilon X_*` under the stated positive finite hypotheses.
3. Derive the exact `A_V+B_V` response classification without replacing `tanh(phi)` by `epsilon`
   when `V(X)` may diverge.
4. Construct exact smooth regular pair-metric counterfamilies that obey the terminal definition,
   reversal, and additive-depth composition while realizing quiet, finite-live, and divergent
   fixed-scale responses.
5. Construct live-`X` witnesses with the same finite endpoint but quiet, finite/nonconvergent, and
   divergent `V(X)` behavior; test cancellation explicitly.
6. Check both asymptotic signs, common-scale covariance, positivity, finite-interior regularity,
   and the distinction between within-leaf and transverse derivatives.
7. Use a separate exact/symbolic implementation for the load-bearing limits and mutation-style
   catch proofs for any verifier.
8. Run the premise verifier and a fresh adversarial review before banking.

## Certification and falsification contract

`NETWORK_FORCES_FIXED_LEAF_SCALE` requires an exact theorem from the already adopted same-law,
unit-slope composition premises, not a fitted or chosen constant. `NETWORK_SELECTS_RESPONSE_CLASS`
requires all other preregistered classes to contradict an active premise. One regular counterfamily
per surviving class falsifies universal selection in this bounded arena.

No finite `X_*`, no vanishing response, and no proper-ruler calibration may be inferred solely from
`sech^2(phi)->0`. Any result based on `V(phi)` being bounded, `dX=0`, or `V(rho)=1` must be explicitly
conditional.

## Maximum conclusions allowed

Exactly one primary landing:

- `FIXED_LEAF_SCALE_AND_UNIQUE_ASYMPTOTIC_RESPONSE_DERIVED`;
- `FIXED_LEAF_SCALE_DERIVED__RESPONSE_CLASS_NOT_SELECTED`;
- `EVEN_FIXED_LEAF_SCALE_NOT_DERIVED__RESPONSE_CLASS_NOT_SELECTED`;
- `TYPE_OR_EXISTENCE_FAILURE`.

All landings leave numerical `X_max`, proper length, physical history, dynamics, observations,
matter/bootstrap, and global completion open.
