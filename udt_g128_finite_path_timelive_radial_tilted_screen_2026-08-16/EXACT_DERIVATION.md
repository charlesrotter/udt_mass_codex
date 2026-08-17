# G128 exact finite-path construction

Date: 2026-08-16

## Metric arena

The bounded calculation uses the complete smooth spherical base

\[
ds^2=-N^2dT^2+L^2(dR+\beta dT)^2+R^2d\Omega^2,
\qquad N=e^{\kappa-\phi},\quad L=e^{\kappa+\phi},
\]

with all three functions `kappa(T,R)`, `phi(T,R)`, and `beta(T,R)` retained. This is not the
complete nonspherical coframe. The four histories and four initial tilt angles are exactly those
frozen in `PREREGISTRATION.md`; they are free certification witnesses, not selected cosmologies.

## Metric-owned propagation

The implementation constructs the full coordinate Levi-Civita connection and Riemann tensor from
the metric without linearization. For an affinely parameterized null ray,

\[
\frac{dx^a}{d\lambda}=k^a,
\qquad
\frac{dk^a}{d\lambda}=-\Gamma^a{}_{bc}k^bk^c.
\]

Two initially orthonormal screen vectors are parallel transported:

\[
\frac{ds_A^a}{d\lambda}=-\Gamma^a{}_{bc}k^bs_A^c.
\]

The screen tidal matrix and point-observer Jacobi phase are

\[
({\cal R}_\perp)_{AB}=R(s_A,k,k,s_B),
\]

\[
{\cal D}'={\cal P},\qquad
{\cal P}'=-{\cal R}_\perp{\cal D},\qquad
{\cal D}(0)=0,\quad {\cal P}(0)=I.
\]

Where `det D` is nonzero, the optical deformation and shear are read from

\[
{\cal B}={\cal P}{\cal D}^{-1},
\qquad
\sigma={\rm sym}({\cal B})-\tfrac12\operatorname{tr}({\cal B})I.
\]

Nothing angular is appended after this propagation. The different radial and tilted responses are
the projections of the same metric curvature onto different null queries.

## Exact symbolic gates

The production implementation verifies, with all metric jets independent:

- `g g^{-1}=I`;
- lower-index symmetry of the Levi-Civita connection;
- both Riemann pair antisymmetries and pair exchange;
- null and screen normalization including nonzero `beta`;
- exact recovery of all four G127 static adapted curvature scalars.

Spherical-coordinate trigonometric identities are certified through the exact rational
half-angle substitution, avoiding numerical sampling and avoiding a fragile general-purpose
factorization path.

## Independent method

`verify_finite_path_independent.py` does not import the production module, symbolic connection,
Riemann tensor, or Jacobi equation. It separately codes the metric and its first derivatives,
reconstructs the Levi-Civita connection, propagates central and neighboring nonlinear rays, and
estimates each endpoint Jacobi column from the five-point formula

\[
J_A(\lambda_f)=
\frac{-x(2h)+8x(h)-8x(-h)+x(-2h)}{12h},
\qquad h=2\times10^{-4},
\]

then projects onto its independently transported central screen.

Both implementations enforce the preregistered terminal events at `R=0.08` and
`|sin(theta)|=0.2`, and reject nonfinite states or nonfinite/nonpositive `N,L`. None of those guards
fires in the saved atlas.

## Bounded result

All 16 production branches reach `lambda=0.8`. The three nonflat history families each retain
nonzero tilted tidal contrast and finite optical shear, while every radial control remains
isotropic. At `alpha=pi/4`, the maximum shear norms are approximately

| history | maximum shear norm | maximum tidal contrast |
|---|---:|---:|
| H1 static reciprocal | 1.4858e-3 | 1.3157e-2 |
| H2 time-live reciprocal | 2.4392e-3 | 1.4339e-2 |
| H3 time-live full spherical base | 5.4712e-4 | 1.7908e-2 |

These differing magnitudes demonstrate dependence on the supplied history; they do not select one
history or define a universal angular curve.

## Status

The differential-geometric construction is `DERIVED_CONDITIONALLY` from each supplied metric and
query. The all-family finite-path persistence is `OBSERVED` in this bounded atlas. Physical
history, universal query ownership, nonspherical completion, observations, transfer, and global
completion remain `OPEN`.
