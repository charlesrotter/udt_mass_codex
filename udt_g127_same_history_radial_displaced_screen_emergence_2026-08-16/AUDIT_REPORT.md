# G127 same-history radial/tilted screen-emergence audit

Date: 2026-08-16

Status:
`BLIND_VERIFIED__LOCAL_SAME_HISTORY_RADIAL_TILTED_SCREEN_EMERGENCE_DERIVED__GENERIC_TIDAL_CONTRAST_AND_OPTICAL_SHEAR_METRIC_OWNED_CONDITIONALLY__PHYSICAL_HISTORY_GLOBAL_QUERY_AND_OBSERVATIONS_OPEN`

## Result

For one supplied nonlinear reciprocal spherical metric

\[
ds^2=-e^{-2\phi(r)}dt^2+e^{2\phi(r)}dr^2+r^2d\Omega^2,
\]

the same curvature tensor at the same regular finite-radius event gives:

- an isotropic, in this reciprocal-areal subfamily exactly zero, optical tidal matrix for the
  symmetry-radial null query; and
- a generally nonisotropic optical tidal matrix for a tilted null query.

The generic adapted tidal eigenvalue contrast is

\[
(\mathcal R_{\perp,\alpha})_{11}-(\mathcal R_{\perp,\alpha})_{22}
=\sin^2\alpha\,\Xi,
\]

with the spherically adapted curvature contrast

\[
\Xi=e^{-2\phi}\left(2\phi'^2-\phi''+\frac{2\phi'}r\right)
-\frac{1-e^{-2\phi}}{r^2}.
\]

The point-observer Jacobi data then give

\[
\mathcal D_{11}-\mathcal D_{22}
=-\frac{\lambda^3}{6}\sin^2\alpha\,\Xi+O(\lambda^4),
\]

while the actual optical shear follows from

\[
\mathcal B=\mathcal D'\mathcal D^{-1}
=\frac I\lambda-\frac\lambda3\mathcal R_\perp(0)+O(\lambda^2).
\]

Thus the leading optical-shear eigenvalue contrast is

\[
-\frac\lambda3\sin^2\alpha\,\Xi+O(\lambda^2).
\]

## What this removes

Inside this bounded local class, radial and angular screen behavior do not require:

- a separately appended angular-response law;
- an independently selected angular amplitude;
- a scalar `mu` added after the pair relation;
- a second metric history; or
- SNe or R5 data as inputs.

They are different null-query projections of one metric's curvature and one Jacobi construction.

## Exact scope correction

The executable strict comparison is at one shared finite-radius event. Its radial query is the
symmetry-radial control; it is not literally G119's center-vertex observer. It is consistent with
G119's broader radial-isotropy theorem, and the same metric family separately admits the central
query.

## Certification

- preregistered in commit `bc5f90dc` before executable evaluation;
- direct coordinate Christoffel/Riemann and symbolic generic-angle implementation: `26/26`;
- independent standard-library Fraction and Cartan/warped-curvature implementation: `17/17`;
- six exact source hashes verified;
- isolated replay of both implementations: byte-identical;
- first blind review: `PASS_WITH_REPAIRS`;
- all five repairs registered and implemented;
- blind follow-up: `PASS` with fresh byte-identical replays.

## Maximum justified conclusion

`DERIVED`, conditionally on one supplied reciprocal spherical metric history and the declared
point-observer queries: the local radial and tilted screen responses emerge from one metric rather
than from separately fitted radial and angular sectors.

Still `OPEN`: selection of the physical metric history, ownership or universality of the observer
query, finite/time-live propagation, nonspherical histories, caustics and branch populations,
global completion, source/transfer laws, `X_max`, and all SNe/R5/CMB/BAO predictions.
