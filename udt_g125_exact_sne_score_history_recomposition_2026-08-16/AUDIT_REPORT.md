# G125 audit report — exact conditional SNe score/history recomposition

Date: 2026-08-16

Status: `BLIND_VERIFIED_WITH_REPAIRS__EXACT_CONDITIONAL_SNE_TOTAL_SCORE_DERIVED`

## Result

On the outgoing frozen P1 branch,

\[
R(Z)=R_\infty(1-Z^{-2/n}),
\qquad
\zeta_{\rm P1}(R)=-\frac n2\log(1-R/R_\infty).
\]

Combining this conditional G120 radius-frequency chord with G124's finite-radius live junction
gives

\[
\boxed{
\phi_{\rm pair}(R)+\frac12\log|K(R)|+\chi_s(R)
=\zeta_{\rm P1}(R)
}.
\]

Thus the frozen SNe interface constrains one total score for histories that already realize the
same G119 central-spherical query, G120 imported transfer, processed-release frequency slot, and
frozen P1 functional curve. It does not constrain terminal `phi_pair` alone and is not independent
evidence for G124.

The conditional luminosity prediction `d_L=Z^2R(Z)` is unchanged by identity. Replaying either SNe
likelihood would return the same prediction vector and was therefore stopped as a loop.

## Surviving freedom

The exact family

\[
|K(R)|=\exp(2[\zeta_{\rm P1}-\phi_{\rm pair}-\chi_s])
\]

shows that the terminal reciprocal, screen-rate, and source-clock allocations remain
underdetermined. The explicit `(a,b)` examples are terminal algebra only, not globally integrable
history witnesses. Orientation remains in signed `K`, the branch, and `beta_pair`.

The open inversion domain is `0<R<R_inf`; `R=0,Z=1` is its normalized boundary closure. The formal
`R->R_inf` divergence is outside the evaluated SNe range and remains an extrapolated P1 property,
not `X_max`.

## Evidence gates

1. Preregistered at commit `20ebc809` before executable evaluation.
2. Production symbolic derivation: 16/16 pass.
3. Independent Fraction/direct-float implementation: 13/13 pass, including signed orientation and
   wrong-log-sign catch proofs.
4. Six exact source hashes pass.
5. Package verification reruns both implementations in an isolated temporary directory and requires
   byte-identical regenerated artifacts.
6. Fresh adversarial review returned `PASS_WITH_REPAIRS`. Five repairs passed the first follow-up;
   one residual naming defect failed. After correction, the second follow-up returned `PASS`.

## Maximum conclusion

G125 recovers one exact line of the conditional empirical score and prevents a redundant
observational replay. It does not select a complete history, query, source clock, native transfer,
branch population, `X_max`, CMB/BAO interpretation, action, bootstrap, matter, mass, or signalling
law.
