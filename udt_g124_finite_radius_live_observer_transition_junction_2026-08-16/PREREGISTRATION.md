# G124 preregistration — finite-radius live observer-transition junction

Date: 2026-08-16

Status: preregistered after design-stage symbolic reduction and before executable witness evaluation

## Whole question and bounded regime

Let one supplied smooth time-oriented central-spherical metric and one supplied normalized radial
null point-observer query define

\[
F(\tau,\lambda,n)=\operatorname{Exp}_{z(\tau)}[\lambda k(\tau,n)],
\qquad -g(k,u_o)=1.
\]

On one regular outgoing branch, use areal radius `R` as the calibrated ruler label wherever
`K(R)=dR/dlambda` is nonzero. Derive the exact finite-radius relation among:

- terminal `kappa_pair`, `phi_pair`, `beta_pair`, and `c_eff/c_E`;
- the carried endpoint frequency depth `zeta=log(omega_s/omega_o)`;
- the source clock relative to the normalized observer-time variation;
- the exact central-spherical screen area and expansion;
- the G123 common-event chart transition and G114 phase-matching boundary.

No metric history, source clock, branch, transfer law, observation, or profile is selected.

## Design-stage candidate, frozen before executable evaluation

Write the areal-ruler longitudinal pullback as

\[
h_\parallel=\begin{pmatrix}-A^2&-s\\-s&0\end{pmatrix},
\qquad s=\frac{d\lambda}{dR}\ne0,
\]

where `A=sqrt(-g(T,T))` and `T=F_*(partial_tau)|_R`. The design-stage reduction suggests

\[
\kappa_{\rm pair}=\frac12\log|s|,
\qquad
\phi_{\rm pair}=\frac12\log|s|-\log A,
\qquad
\beta_{\rm pair}=\operatorname{sgn}(s)e^{2\phi_{\rm pair}},
\]

and, with `U_T=T/A` and

\[
\chi_s=\log\frac{-g(k,U_s)}{-g(k,U_T)},
\]

the candidate exact junction

\[
\boxed{\zeta=\phi_{\rm pair}-\kappa_{\rm pair}+\chi_s.}
\]

This disclosed pilot algebra is not evidence. The package must reconstruct it from the metric/query
normalization and independently verify the frozen witnesses below.

## Frozen outcome classes

1. `EXACT_FINITE_RADIUS_KAPPA_PHI_SOURCE_RAPIDITY_JUNCTION_DERIVED`;
2. `LOCAL_G116_SERIES_ONLY__NO_FINITE_RADIUS_UPGRADE`;
3. `IDENTITY_ONLY__NO_NEW_DEPENDENCY_REDUCTION`;
4. `TYPE_FAILURE_BETWEEN_PAIR_AND_FREQUENCY_CARRIERS`;
5. `BOUNDED_INCONCLUSIVE`.

## Frozen exact witnesses

1. Flat normalized control: `A=1`, `s=1`, source ratio `1`.
2. Rational finite control: `A=3/4`, `s=25/16`, source ratio `6/5`.
3. Orientation-reversed ruler control: `A=3/4`, `s=-25/16`.
4. Areal-turning chart limit: `K(R)->0`, hence `|s|->infinity`; test cancellation of
   `phi_pair-kappa_pair` while retaining the affine chart.
5. G116 two-jet reduction:
   `phi_pair=p2 R^2`, `kappa_pair=A_opt R^2/4`,
   `chi_s=v_rel R+dot(v_rel)R^2`.
6. G119 screen link on `R>0`:
   `theta_sky=2K(R)/R` and
   `kappa_pair=-log|K(R)|/2=-log|R theta_sky/2|/2`.

## Certification and falsification contract

The exact landing requires:

- derivation of `g(T,k)=-1` from affine normalization, commuting variations, and nullness;
- exact terminal decomposition from the raw `2x2` Gram block;
- exact endpoint frequency factorization through `U_T`;
- reproduction of G116 through `O(R^2)` with no new coefficient;
- preservation of G119 `D_sky=R O` and its regular/turning/caustic strata;
- preservation of G123 direct-chart composition and the query-tangent/Jacobi-phase distinction;
- independent exact implementation and a fresh blind review.

It is falsified if the claimed equality requires setting `kappa_pair=0`, imposing source comotion,
equating query tangents with phase, choosing a history after evaluation, or hiding an imported
transfer/profile.

## Loop stop rule

Stop as `IDENTITY_ONLY__NO_NEW_DEPENDENCY_REDUCTION` if the work merely rewrites definitions without
eliminating a previously independent input or upgrading G116 from local series to an exact
finite-radius relation.

## Maximum conclusion

G124 may derive the exact score of one supplied regular central-spherical null observer query. It
cannot select the physical history, observer/source query, branch occupancy, radiation transfer,
`X_max`, bootstrap closure, action, matter, mass, or an observation.
