# G320 preregistration — physical versus representational G319 freedom

Date: 2026-09-01
Status: `PREREGISTERED_BEFORE_OUTCOME_SCRIPTS_OR_RESULTS`

## 1. Frozen bounded frame

Retain G319's exact flat marked-`T^3`, one-coordinate, diagonal-TT, smooth positive periodic,
sign-definite `B!=0` diagnostic slice. Reconstruct

\[
\gamma_{ij}=\psi^4\delta_{ij}
\]

and `K^i_j` by G319 equations (6)--(8). Do not modify the active conditional equation, metric, or
reciprocal kernel.

## 2. Physical equivalence relation

Two conformal tuples count as the same physical initial datum when they reconstruct pairs related
by a spatial diffeomorphism,

\[
(\widehat\gamma,\widehat K)=(f^*\gamma,f^*K).
\]

Raw seed fields, raw `psi`, coordinate phase, and auxiliary `W` are not comparison criteria.
Conformal seed changes satisfying

\[
\widehat{\bar\gamma}=\vartheta^4\bar\gamma,
\qquad
\widehat\psi=\psi/\vartheta,
\qquad \vartheta>0,
\]

reconstruct the same intrinsic metric and must be accepted as representation controls. A complete
seed transformation is equivalent only when it reconstructs the same `K` as well.

## 3. Exact intrinsic invariants

For `gamma=psi^4 delta` in three dimensions and `psi=psi(x)`, preregister

\[
{}^{(3)}R=-8\psi^{-5}\psi'',
\qquad
d\mu_\gamma=\psi^6\,dx\,dy\,dz.
\]

On the periodic torus,

\[
\int {}^{(3)}R\,d\mu_\gamma
=-8\int\psi\psi''\,d^3x
=8\int(\psi')^2\,d^3x.
\]

Use the dimensionless homothety-neutral invariant

\[
Q_R=\frac{\int{}^{(3)}R\,d\mu_\gamma}
{\operatorname{Vol}(\gamma)^{1/3}}.
\]

Both volume and total scalar curvature are diffeomorphism invariants, and `Q_R` is also unchanged
by a common constant rescaling of the physical metric.

## 4. Preregistered separating family

Set

\[
\psi_n(x)=p+a\cos(nx),
\qquad p=\frac32,
\qquad a=\frac15,
\qquad n\in\{1,2,3,4\}.
\]

All profiles are positive and have the same value distribution, hence the same physical volume.
Preregister the exact prediction

\[
\int(\psi_n')^2\,d^3x=(2\pi)^2\pi a^2n^2,
\]

so

\[
Q_R(\psi_n)=n^2 Q_R(\psi_1).
\]

If this identity and direct tensor reconstruction hold, no spatial diffeomorphism or conformal-seed
rewriting can identify `n=1` with any `n>1`, because it would have to preserve `Q_R`. This proves at
least a countably infinite genuine physical direction in the bounded G319 family. It does not prove
that every distinct profile is inequivalent.

## 5. Lawful-data reconstruction controls

Use `d=0`, `Lambda=0`, and `J0=100` only as diagnostic controls. For `n<=4`, preregister the analytic
bounds

\[
Z=36(\psi')^2+J_0>0,
\]

and

\[
Z+\psi^6F=36(\psi')^2+J_0+12\psi\psi''
\ge J_0-12an^2(p+a)>0.
\]

Therefore both `epsilon=+1` and `epsilon=-1` must reconstruct smooth sign-definite data. Direct
physical Hamiltonian and momentum residuals must pass independently.

## 6. Required equivalence controls

1. Phase shifts `psi_n(x-theta)` and reflections `psi_n(-x)` must preserve all invariant outputs.
2. An explicit positive nonconstant `vartheta(x)` seed rewrite must reconstruct the same `gamma`
   pointwise and preserve intrinsic invariants.
3. A deliberate raw-array comparison must be rejected as a physical discriminator.
4. Constant profiles must give zero total scalar curvature; nonconstant periodic profiles must give
   strictly positive total scalar curvature.

## 7. Auxiliary extrinsic/tidal characterization

For each reconstructed branch, compute the scalar fields

\[
\tau=\operatorname{tr}K,
\qquad
K_2=\operatorname{tr}(K^2),
\qquad
K_3=\operatorname{tr}(K^3),
\]

and their volume-weighted summaries. These are physical characterizers and phase/reflection controls,
not load-bearing selectors. No extrinsic difference may override a failed intrinsic invariant proof.

## 8. Possible landings

1. `G319_FREEDOM_NOT_PURE_REPRESENTATION` if at least one fully lawful pair differs in a registered
   invariant after all declared quotient controls pass;
2. `REGISTERED_CONTROLS_EQUIVALENT_AFTER_QUOTIENT` if no invariant separator survives;
3. `ONLY_INTRINSIC_METRIC_SEPARATED__FULL_DATA_RECONSTRUCTION_FAILED` if curvature separates but the
   G319 constraint replay fails;
4. `QUOTIENT_AUDIT_INCONCLUSIVE` if the controls or independent implementation disagree.

## 9. Certification contract and maximum conclusion

- Production derives exact formulas and bounded numerical summaries using only standard-library
  mathematical methods.
- An implementation-distinct verifier rebuilds Christoffels/Ricci and physical constraints without
  importing production functions or reading production results.
- Hostile mutations must catch wrong conformal powers, omitted volume weight, coordinate-array
  comparison, phase-dependent false distinctions, loss of homothety normalization, wrong mode
  scaling, failed constraint reconstruction, and any selection/kernel/scale overclaim.
- Run the exact premise verifier and full repository purity harness.
- Require fresh external adversarial review before an externally accepted grade.

Maximum conclusion: the G319 bounded family contains genuine inequivalent physical initial
geometries, if the invariant separator passes. No complete quotient, physical occupancy, evolution,
history, topology, scale, observation, source, matter/mass, `X_max`, metric change, or kernel change
may be claimed.
