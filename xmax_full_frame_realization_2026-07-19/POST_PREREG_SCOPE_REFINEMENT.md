# Post-preregistration scope refinement

Date: 2026-07-19

The preregistration at commit `c8fc885` is preserved unchanged. Fresh adversarial review confirmed
the registered F3/F4 realization and identified two necessary wording refinements.

First, the complete spatial seed must be stationary and invariant under the frame map. The safe
condition is `h=h(y)` in the registered coordinates, or more generally `F_beta^*h=h`. The condition
`partial_phi h=0` alone would admit time-dependent counterexamples such as `h_11=1+t^2`, which are not
invariant under `t'=exp(-2beta)t`.

Second, the selection of constant pure-depth seed `k(phi)=L` is conditional on the preregistered F3
time action. If the time exponent is freed, the exact family

\[
 k(\phi)=e^{a\phi},\qquad
 t'=e^{-(a+2)\beta}t
\]

gives the common CSN factor `exp(-2(a+1)beta)`. Therefore the audit may say that fixed F3 selects
`L dphi` and rejects bounded `dx`; it may not say covariance alone uniquely selects `a=0`.

The bounded `dx` branch remains refuted for every constant time rescaling in the tested class because
its spatial defect is position-dependent. No registered candidate, test, or result is removed. The
maximum conclusion is narrowed to make the fixed time action and stationary seed explicit.
