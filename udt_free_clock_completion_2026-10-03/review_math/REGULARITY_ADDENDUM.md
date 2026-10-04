# FCL1 mathematical review — finite regularity clarification

This responds to the parent's explicit follow-up after the exposed review was
sealed. It changes neither candidate nor verdict: ACCEPT_WITH_LIMITS, no
mathematical repair required. Candidate SHA-256 remains
`9563063c01c69ffef69654915e522d0019192d7470fb41d2c88fbf438a3c8371`.

The normal-collar regularity is already checked in EXPOSED_REVIEW.md: C3 data
give a C2 normal vector field and C2 local flow chart. The transformed metric
has at least C1 coefficients, enough for the lowered geodesic equation, bounded
first derivatives and the Dini estimate. No argument invokes a general C1-metric
geodesic uniqueness theorem. The receiver is supplied and exists in the original
regular geometry; the C2 change of coordinates transports its equation.

R6's historical word "smooth" is stronger than the derivatives used by its
clock-variation identity. In original interior charts the physical metric
g=Omega^-2 gbar is C3 wherever Omega>0, so its connection is C2. A C2 regular
two-parameter ray map q(lambda,s) is enough: k=partial_lambda q and
J=partial_s q then have the mixed derivatives needed for
nabla_k J=nabla_J k. Metric compatibility, affine geodesicity and nullness give

    d/dlambda g(k,J)
      = g(k,nabla_k J)
      = g(k,nabla_J k)
      = (1/2) partial_s g(k,k) = 0.

This needs first derivatives of the metric and second derivatives of the ray
map, not C-infinity data. FCL1 supplies a smooth regular unique null family and
regular affine-data extension; its C3 geometry and family premises therefore
cover the required derivatives. The identity is used at actual interior
events, not as a differentiation of the singular physical metric at Omega=0.
Continuity of the conformal endpoint data then suffices for the endpoint limit.

If the affine parameter values at emission or reception depend on s, the
endpoint variation acquires a multiple lambda_i'(s)k_i. Contracting it with
k_i gives zero because k_i is null. Thus per-ray physical emission-frequency
normalization need not preserve a common fixed affine-parameter interval for
R6's ratio to hold. This also shows that the candidate has not hidden an
incompatible parameter convention when normalizing omega_e=1.

Suggested optional central clarification: say "the required differentiability
is covered by C3 geometry and the supplied regular ray family" if retaining
R6's historical smooth terminology could be read as a C-infinity premise.
This is an explanatory clarification, not an extra physical assumption,
scientific repair or expanded quantifier.
