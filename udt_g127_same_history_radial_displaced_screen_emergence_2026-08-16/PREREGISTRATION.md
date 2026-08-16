# G127 preregistration — same-history radial/displaced screen emergence

Date: 2026-08-16

## Whole bounded question

Can one supplied nonlinear reciprocal spherical metric history produce both:

1. the isotropic G119 central-radial screen; and
2. a nonisotropic angular screen for a tilted/displaced null observer query,

through the metric curvature and one observer-exponential/Jacobi construction alone—without an
appended angular response, fitted amplitude, separate `mu`, second history, SNe input, or R5 input?

This is a local finite-radius same-history theorem test. It is not a physical-history selector,
time-live global solve, observational comparison, source model, or prediction.

## Exact declared arena

Use the static spherical reciprocal subfamily

\[
ds^2=-e^{-2\phi(r)}c_E^2dt^2+e^{2\phi(r)}dr^2+r^2d\Omega^2
\]

at a regular finite-radius event. Set `c_E=1` only inside dimensionless curvature algebra. Let the
orthonormal-frame spherical curvature scalars be

```text
T = R(e_r,e_t,e_t,e_r),
U = R(e_theta,e_t,e_t,e_theta)=R(e_phi,e_t,e_t,e_phi),
V = R(e_theta,e_r,e_r,e_theta)=R(e_phi,e_r,e_r,e_phi),
W = R(e_phi,e_theta,e_theta,e_phi).
```

For a null direction with spatial part
`v=cos(alpha)e_r+sin(alpha)e_theta`, choose screen
`s1=-sin(alpha)e_r+cos(alpha)e_theta`, `s2=e_phi`.

## Preregistered exact targets

Subject to one declared Riemann-sign convention, test:

```text
Rperp_radial = (U+V) I2,
Rperp_tilted_11 = sin(alpha)^2 T + cos(alpha)^2 U + V,
Rperp_tilted_22 = U + cos(alpha)^2 V + sin(alpha)^2 W,
Rperp_tilted_12 = 0,
Rperp_tilted_11-Rperp_tilted_22
  = sin(alpha)^2 (T-U+V-W).
```

The point-observer Jacobi data are fixed by `D(0)=0`, `D'(0)=I`, hence

\[
D(\lambda)=\lambda I-\frac{\lambda^3}{6}R_\perp(0)+O(\lambda^4).
\]

Thus a nonzero invariant combination `Xi=T-U+V-W` should produce query-relative screen shear at
order `lambda^3` for `sin(alpha) != 0`, while the radial query remains isotropic.

## Candidate landings

1. `SAME_HISTORY_EMERGENCE_DERIVED_LOCALLY`: both projections follow from one metric and one
   observer-exponential law; no independent angular amplitude or response is present.
2. `ONLY_SPECIAL_WITNESS_EMERGENCE`: the effect occurs for one chosen profile but does not survive
   the exact spherical curvature classification.
3. `SPHERICAL_HISTORY_FORCES_ALL_QUERY_ISOTROPY`: the tilted screen remains isotropic and the
   proposed bridge fails.
4. `TYPE_OR_ALGEBRA_FAILURE`: the screen/query contractions or normalization are not lawful.

## Certification and falsification

- derive the curvature and screen contractions directly from the coordinate metric;
- independently reconstruct the load-bearing curvature combination by a separate method;
- prove the radial and tilted outputs use the identical metric functions at the identical event;
- include a regular nonlinear `phi(r)` witness only after the generic formula is established;
- test radial limit, zero-curvature limit, tilt reversal, screen-basis covariance, and Jacobi-jet
  coefficient;
- reject landing 1 if any angular coefficient is independently inserted or if the two queries use
  different metric histories.

## Explicit omissions and maximum conclusion

Omitted: time dependence, nonspherical metric histories, finite-beam/extended sources, global
integration, caustics, cut loci, source and branch populations, radiative transfer, SNe, R5/BAO,
CMB, `X_max`, bootstrap, action, matter, mass, and signalling.

At most G127 can derive a local kinematic same-history bridge. It cannot show that the supplied
history is physical, that the response matches an observed angular pattern, or that UDT predicts a
cosmology.
