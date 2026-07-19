# Post-preregistration premise refinement

Date: 2026-07-19

The original preregistration at commit `1883254` is preserved unchanged. Its XR1 candidate explicitly
specified the fractional-linear law, but its maximum-conclusion wording could be read as attributing
the resulting reciprocity to finite `X_max` alone.

The adversarial check supplied an exact smooth bounded countergroup,

\[
 \xi=f(u)=\frac{u}{\sqrt{1+u^2}},\qquad
 \xi\boxplus\eta=f\!\left(f^{-1}(\xi)+f^{-1}(\eta)\right),
\]

which retains a finite bound, identity, reversal, associativity, commutativity, order, and regularity
but does not make `A=(1-xi)/(1+xi)` multiplicative. The audit grade is therefore tightened:

- finite `X_max` plus generic smooth group properties do not derive XR1;
- the historical named `P2` fractional-linear/projective law is load-bearing and remains `CHOSE`;
- the exact result is conditional also on the signed oriented domain and on identifying the XR1
  additive coordinate with metric `phi/A`.

No registered calculation, tolerance, candidate, or falsification gate is changed. This layer only
narrows the maximum allowed conclusion in response to the registered countermodel.
