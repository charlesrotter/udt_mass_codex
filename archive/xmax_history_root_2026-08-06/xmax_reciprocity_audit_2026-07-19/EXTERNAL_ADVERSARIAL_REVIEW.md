# Fresh adversarial review

Date: 2026-07-19

Context supplied to the reviewer: the preregistration, candidate/status ledgers, exact derivation,
report, and saved machine-readable result. The review was conducted without authority to change the
metric, adopt a premise, or strengthen the conclusion.

## Initial disposition: `REVISE_AND_REVERIFY`

The reviewer identified one load-bearing overstatement and two scope weaknesses:

1. Finite `X_max` plus smooth bounded composition and reversal do not force the fractional-linear
   XR1 law. The exact countermodel
   `f(u)=u/sqrt(1+u^2)`, with composition transported from additive `u`, retains those generic
   properties but does not make `A` multiplicative.
2. The Lorentz-like commutator `[Kx,Ky]=-Jz` is a result inside a chosen negative-curvature group,
   not a consequence of one-dimensional XR1, isotropy, and homogeneity. A radially compactified
   additive `R^3` supplies an isotropic homogeneous bounded-ball counterextension with commuting
   translations.
3. The endpoints `+-1` must be described as limits rather than group elements, and the simple CSN
   line-average example must not be generalized into a no-go theorem for every bootstrap functional.

The reviewer also found presentation-level control characters in early report formulas. They were
removed without changing scientific content.

## Corrections applied

- The result is now conditional on the working `X_max` posit, historical named `P2`
  fractional-linear law, signed oriented domain, and additive-coordinate-to-metric-phi join.
- The smooth alternative bounded group and the flat isotropic three-dimensional counterextension
  are load-bearing saved artifacts and exercised catch-proofs.
- The Lorentz/negative-curvature extension is stamped `CHOSE / CONDITIONAL`.
- Endpoint and CSN claims are explicitly scoped.
- The original preregistration remains unchanged; `POST_PREREG_PREMISE_REFINEMENT.md` records the
  tightened maximum conclusion.

## Corrected disposition

`PASS_AS_VERIFIED_WITH_CAVEATS` for the bounded audit:

- exact: `A` is a multiplicative character of the chosen XR1 law and reversal sends `A` to `A^-1`;
- refuted implication: a finite bound and generic smooth group properties select XR1;
- refuted in tested class: natural XR1 re-centering preserves the pinned reciprocal metric/CSN
  representative;
- open: derivation of P2 from UDT, the full coframe action, angular selection, scale selection,
  finite-cell join, and action.

This review does not canonize `X_max`, P2, a position group, or a new UDT principle.
