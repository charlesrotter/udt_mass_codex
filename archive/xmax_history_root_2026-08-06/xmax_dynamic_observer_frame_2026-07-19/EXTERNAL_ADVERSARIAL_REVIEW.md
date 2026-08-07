# Fresh-context adversarial review

Date: 2026-07-19

Review mode: fresh isolated read-only context, supplied the preregistration and completed draft
package after the primary and independent algebra had run.

Initial verdict: `REVISE`, not refuted.

Final disposition: both load-bearing review findings were accepted and corrected before banking.
The tensor results survived.

## Finding 1 — connection signs were conflated

The draft combined two distinct conventions. With

\[
D\phi=d\phi+a,\qquad \phi'=\phi-\beta,
\]

active invariance requires

\[
a'=a+d\beta.
\]

Thus an active transformation from `a=0` gives `a'=+d beta`. The negative sign belongs instead to
the absorbed pullback shift in fixed unprimed coordinates:

\[
d\phi'=d\phi-d\beta=d\phi+a_{shift},\qquad a_{shift}=-d\beta.
\]

Both are exact and both have zero exterior curvature, but they must not be identified. The derivation
result, report, ledgers, and verifier now keep them separate. New catch-proofs reverse each sign and
conflate the conventions; all are rejected.

## Finding 2 — global group language was too strong

The exact compatible-chart composition law survived:

\[
\beta_{12}(t)=\beta_1(t)+\beta_2(T_{\beta_1}(t)),\qquad
\frac{dT_2}{dt}=e^{-2\beta_{12}(t)}.
\]

But `beta=-one_half log(T')`, so `T` and `beta` are not independent semidirect-product factors. In
addition, strict monotonicity guarantees an inverse only on the time map's image. The audit now grades
this as the lifted local composition law of orientation-preserving time diffeomorphisms: a
pseudogroup/groupoid on compatible chart intervals.

The review supplied the decisive counterexample `beta(t)=t^2` on the real line:

\[
T(t)=\int_0^t e^{-2s^2}ds,
\]

whose image is `(-sqrt(pi/8),sqrt(pi/8))`. It is not a global real-line-to-real-line frame. A global
group therefore requires additional common-domain and surjectivity premises. The primary derivation
and independent verifier now recompute this finite-image witness, and catch-proofs reject global-group
promotion or deletion of the witness.

## Finding 3 — frame paths versus physical observers

The draft's phrase “arbitrary observer trajectories” was too broad. The exact pullback accepts
arbitrary smooth re-centerings/frame paths. Only the subset satisfying

\[
L|\dot\beta|<ce^{-2\beta}
\]

is timelike and eligible for the conditional observer interpretation. The report and ledgers now use
that distinction.

## Results that survived independent attack

- The fixed-F3/common-CSN requirement uniquely gives `dT=exp(-2 beta)dt` on the positive branch.
- The full stationary depth-translation-invariant seed closes only when every forced off-diagonal
  descendant is retained.
- The conditional depth-trajectory causal bound is exact.
- An independent connection-transformation calculation reproduces the `beta_dot` and
  `beta_double_dot` terms.
- The exact scalar curvature is the base scalar evaluated at shifted depth; all frame-path derivatives
  cancel.
- This is metric covariance, not a derived equivalence principle, physical force, or action symmetry.

## Gate reassessment

1. Preregistered: `PASS`.
2. Full space or bounded scope: `PASS` for the declared one-depth, stationary-seed, fixed-F3 frame
   family after the chart-local and timelike-observer qualifications.
3. Independently verified: `PASS`; the adversary also used a connection-transformation route distinct
   from direct differentiation of the pulled-back metric.
4. Every premise audited: `PASS` after the sign, global-domain, and observer-eligibility corrections.

Final evidence grade: `VERIFIED-WITH-CAVEATS` in the declared bounded regime.
