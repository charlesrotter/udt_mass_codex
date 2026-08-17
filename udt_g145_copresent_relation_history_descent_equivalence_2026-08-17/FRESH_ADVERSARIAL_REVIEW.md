# G145 fresh adversarial review

Date: 2026-08-17

## Initial return

Initial verdict: `REPAIR`.

The reviewer reproduced production 43/43, independent 23/23, and package 27/27, and accepted the
bounded mathematical landing. It required three evidence repairs:

1. independently reconstruct curvature rather than substituting the production formula;
2. use fixed nonzero amplitudes and independently prove all nine non-`Phi` coframe fields are live
   while the complete perturbation preserves the marked metric two-jet; and
3. load saved evidence before recomputation and prevent the package verifier from rewriting it.

It also required the four-dimensional base-atlas/two-dimensional pair-sheet distinction and the
supplied/open ownership ceiling to remain explicit.

## Repairs

- Production now uses fixed nonzero rational amplitudes for `kappa`, `beta`, all three `Q` fields,
  and all four `S` fields.
- The independent stdlib/Fraction route directly contracts Christoffel and Ricci tensors from the
  metric first and second derivatives. Its separate exact bivariate three-jet algebra proves each
  of the nine fields changes the metric at cubic order while their combined perturbation preserves
  the marked zero-, first-, and second-order metric jets.
- The fail-closed package verifier loads the saved JSON first and invokes both recomputations with
  `--no-write`. Before/after SHA-256 digests were identical.
- The theorem wording now says that full-pullback valuation determines the metric component on the
  supplied four-dimensional base atlas; the query atlas, calibrations, numerical valuation, and
  physical realization remain supplied or open.

## Follow-up

Verdict: `PASS`.

The reviewer reran production 43/43, independent 23/23, and package 29/29. It found the independent
curvature and nine-field jet checks substantive, the 4D/2D type boundary correct, the ownership
ceiling preserved, and the saved evidence unchanged by package verification.
