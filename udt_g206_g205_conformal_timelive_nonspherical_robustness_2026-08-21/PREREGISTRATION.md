# G206 preregistration

Date: 2026-08-21

## Exact tests

For `g_tilde=exp(2 Omega) g0`:

1. Derive the connection difference directly and prove that every `g0`-affine null tangent `k`
   obeys `nabla_tilde_k k=2 k(Omega) k`.
2. Prove that `k_tilde=exp(-2 Omega) k` is affine and
   `d lambda_tilde/d lambda=exp(2 Omega)`.
3. Prove conformal equality of causal curves and hence preservation of G205 Cauchy slices and
   global hyperbolicity for every smooth finite `Omega`.
4. Prove the exact null-completeness criterion: every inextendible base null geodesic must have
   divergent `integral exp(2 Omega) d lambda` at both affine ends.
5. Prove the sufficient global lower-bound class `Omega>=C` is null complete.
6. Test the smooth bounded genuine time-live/nonspherical witness
   `Omega_B=epsilon sin(t)(3 z^2-r^2)/(1+r^2)`.
7. Test the smooth failing witness `Omega_F=-r^2+Omega_B`; use an exact outgoing G205 radial null
   ray to prove finite transformed affine length despite retained global hyperbolicity.
8. Derive the complete pair-pullback scaling and completed readouts:
   `h_tilde=exp(2 Omega)h`, `T_tilde=exp(Omega)T`,
   `Lsigma_tilde=exp(Omega)Lsigma`, `m_tilde=exp(2 Omega)m`, and
   `Phi_tilde=Phi-Omega`. Confirm that the arbitrary-calibration reciprocal control remains
   conformally invariant while completed `Phi` is scale-sensitive.

## Verification contract

- Production: exact symbolic connection/pullback algebra and analytic integral bounds.
- Independent: separately written direct radial Euler-Lagrange/parameter transformation plus at
  least 10,000 distinct exact or high-precision witness cases.
- At least 12 hostile catches, including causal-cone, affine-power, lower-bound, bounded-witness,
  finite-integral, completed-readout, mechanization-scope, history-selection, and `X_max` errors.
- Saved outputs replay byte-identically under `UDT_NO_WRITE=1`.
- Fresh adversarial review before final banking.

## Falsification

The strongest landing fails if a positive smooth conformal factor changes the causal curve set or
Cauchy property, if the affine factor is not `exp(2 Omega)`, if the integral criterion is not both
necessary and sufficient, or if either registered witness has the wrong completeness class.

## Scope lock

Global hyperbolicity is not null completeness. Neither implies timelike/spacelike completeness of
the conformal family. The deformation class is supplied configuration space, not a selected UDT
history or new mechanism.

