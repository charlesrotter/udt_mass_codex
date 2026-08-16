# G124 audit report — finite-radius live observer-transition junction

Date: 2026-08-16

Status:
`BLIND_VERIFIED_WITH_REPAIRS__EXACT_FINITE_RADIUS_KAPPA_PHI_SOURCE_CLOCK_JUNCTION_DERIVED_CONDITIONALLY`

## Result

For one supplied normalized radial-null point-observer query on a regular central-spherical branch,
the complete pullback gives

\[
h_\parallel=
\begin{pmatrix}-A^2&-s\\-s&0\end{pmatrix},
\qquad
\kappa_{\rm pair}=\frac12\log|s|,
\qquad
\phi_{\rm pair}=\frac12\log|s|-\log A.
\]

For a supplied endpoint/source clock,

\[
\boxed{\zeta=\phi_{\rm pair}-\kappa_{\rm pair}+\chi_s},
\qquad
\chi_s=\log\frac{-g(K,U_s)}{-g(K,U_T)}.
\]

The finite-radius spherical screen theorem gives

\[
\kappa_{\rm pair}=-\frac12\log|K(R)|
=-\frac12\log\left|\frac{R\theta_{\rm sky}}2\right|.
\]

Thus G116's local optical term is the two-jet reduction of the already present pair common-scale
magnitude `-kappa_pair`, not a separately appended correction. On this null-ruler subclass,
`beta_pair=sgn(s) exp(2 phi_pair)` and is not independent.

Active fixed-label sky drift remains upstream in both `phi_pair` and `chi_s`; it cancels in the
scalar frequency identity only when the two readouts use the same terminal clock convention.

## Scope and strata

- `kappa_pair` is an expansion magnitude. Orientation remains in `K(R)`, the branch label, and
  `beta_pair`.
- At an areal turning point only the shared logarithmic chart term is guaranteed to cancel. The
  turning point alone establishes neither frequency finiteness nor divergence.
- The normalized initial observer vertex and a later spherical caustic both have `R=0` but are
  different strata. The later caustic can retain nontrivial full Jacobi-phase data.
- Every regular branch is evaluated separately. No branch population, occupancy, or aggregation
  rule follows.

## Evidence gates

1. Preregistered at commit `5fca1cea` before executable evaluation.
2. Production symbolic implementation: 22/22 checks pass.
3. Independent standard-library Fraction implementation: 15/15 checks pass without importing
   production code.
4. Eight exact source hashes verify.
5. Blind review returned `PASS_WITH_REPAIRS`; all three repairs were applied. The bounded follow-up
   returned `PASS` and reproduced both JSON artifacts byte-for-byte.

## Maximum conclusion

This is an exact conditional evaluator theorem. It removes an unnecessary independent optical
correction slot and closes the finite-radius junction for the declared query class. It does not
select a physical metric history, observer query, endpoint clock, transfer law, global branch,
`X_max`, bootstrap condition, action, matter model, observation, or signalling law.
