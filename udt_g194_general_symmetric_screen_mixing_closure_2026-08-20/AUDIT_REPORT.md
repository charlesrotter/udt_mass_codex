# G194 audit report — arbitrary symmetric screen mixing closure

Date: 2026-08-20

## Current grade

`EXTERNALLY_REVIEWED_VERIFIED_WITH_CAVEATS__R5_REPAIRS_ACCEPTED`

## Bounded result

For the displayed coframe

\[
\theta^0=a\,d\eta,\quad \theta^1=a\,dz,\quad
\theta_{\rm screen}=a[dX+M(\eta)X(d\eta+dz)],
\]

with arbitrary positive `C3 a`, arbitrary real `C2` symmetric

\[
M=\begin{pmatrix}A&N\\N&B\end{pmatrix},
\]

and the supplied central `+z` pair germ, direct metric reconstruction gives

\[
\frac{d\lambda}{d\eta}=a^2,\qquad Z=\frac1a,
\]

\[
\mathcal T=\tau_0I_2+\frac{2M'-4M^2}{a^4},
\]

and

\[
\mathcal D=aLK,\qquad
L'=-2ML,\qquad
K=\int_0^\eta L^{-1}L^{-T}ds.
\]

The Gram integrand is definite, so `det D>0` for every nonvertex point on the declared connected
regular interval.  This closes the arbitrary smooth symmetric `2 x 2` matrix tile.  It does not
cover antisymmetric rotation or arbitrary complete coframes.

## Evidence

- preregistered and committed before computation at `90057d83`;
- 19 exact symbolic production assertions;
- independent Torch metric-jet/Riemann spot checks plus separately implemented formula-driven
  SciPy matrix-IVPs;
- 267 histories, including 11 named classes and 256 seeded random histories;
- 4,007 independent assertions;
- maximum tide error `5.329070518200751e-15`;
- maximum factorization error `1.4583445562266206e-11`;
- maximum Wronskian residual `7.860850859131574e-12`;
- minimum sampled nonvertex determinant `0.0002100108472233669`;
- 22 of 22 hostile structural mutations caught.

The numerical evidence is a two-leg spot-check plus formula-driven IVP replay, not full
metric-derived curvature evaluation at every adaptive IVP call.  The no-caustic statement is
instead supported by the exact positive-Gram proof.

## Four banking gates

1. `PREREGISTERED`: yes, commit `90057d83`.
2. `FULL SPACE OR BOUNDED SCOPE`: full arbitrary-function space inside the declared symmetric
   family; wider complete-coframe arena explicitly omitted.
3. `INDEPENDENTLY VERIFIED`: internal independent implementation passes.  After the first external
   review exposed a write-triggering autodiff dependency, the preregistered R5 replacement passed
   384/384 forward-versus-reverse autodiff comparisons and a fresh sealed external no-write replay.
   The evidence grade remains metric-jet/Riemann spot checks plus formula-driven matrix IVPs.
4. `PREMISE AUDITED`: construction inputs and omissions are ledgered; the final 179-row G194
   premise verifier and full repository suite pass.

## Maximum conclusion

G194 may establish only that the displayed arbitrary smooth symmetric screen-mixing family and one
supplied central pair possess the stated frequency, tide, ordered Jacobi representation, and no
nonvertex caustic theorem.  It does not select functions as a physical history, choose physical
pair germs, derive transfer or observations, or establish global completion, `X_max`, dynamics,
action, source, matter, mass, bootstrap, or signalling.
