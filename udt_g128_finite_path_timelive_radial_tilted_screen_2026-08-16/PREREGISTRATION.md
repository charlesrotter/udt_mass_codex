# G128 preregistration — finite-path time-live radial/tilted screen propagation

Date: 2026-08-16

## Whole question

Does the local G127 result survive exact finite affine propagation when the complete smooth
spherical base is time-live, or was the radial/tilted bridge only a vertex-jet fact?

The test is metric-led. It will not fit an angular curve, import an observational target, append an
angular response, or select a physical history.

## Exact bounded metric arena

Use dimension-matched `T=c_E t`, areal radius `R`, and

\[
ds^2=-N^2dT^2+L^2(dR+\beta dT)^2+R^2d\Omega^2,
\qquad
N=e^{\kappa-\phi},\quad L=e^{\kappa+\phi}.
\]

All three smooth spherical-base instruments `kappa(T,R)`, `phi(T,R)`, and `beta(T,R)` are retained.
This is the complete spherical base, not the complete nonspherical four-dimensional coframe.

At the shared regular event

\[
p=(T,R,\theta,\psi)=(0,2/5,\pi/2,0),
\]

use the Eulerian observer and orthonormal frame

\[
e_0=N^{-1}(\partial_T-\beta\partial_R),\quad
e_1=L^{-1}\partial_R,\quad e_2=R^{-1}\partial_\theta,\quad
e_3=(R\sin\theta)^{-1}\partial_\psi.
\]

For each declared angle,

\[
k=e_0+\cos\alpha\,e_1+\sin\alpha\,e_2,
\quad s_1=-\sin\alpha\,e_1+\cos\alpha\,e_2,
\quad s_2=e_3.
\]

The metric must verify `g(k,k)=0`, `g(k,e0)=-1`, and screen orthonormality before integration.

## Free-and-explored certification histories

These dimensionless profiles are witnesses, not cosmologies:

1. `H0`: `kappa=phi=beta=0`.
2. `H1`: `kappa=beta=0`, `phi=log(1+R^2/4)/2` (the static G127 class).
3. `H2`: `kappa=beta=0`,
   `phi=log(1+q(T)R^2)/2`, `q(T)=(1+2 sin(T)/5)/4`.
4. `H3`: the same `phi`, with
   `kappa=R^2 cos(T/2)/(20(1+R^2))` and
   `beta=R exp(-R^2)(1+sin(T/2))/12`.

Angles are `alpha in {0, pi/12, pi/6, pi/4}`. No value is observationally anchored.

## Exact propagation

For each history and angle, integrate simultaneously on `0 <= lambda <= 4/5`:

- the full nonlinear affinely parameterized null geodesic;
- two parallel-transported screen vectors;
- the exact `2x2` Jacobi map `D` and derivative `P=D_lambda D`;
- the optical tidal matrix `Rperp_AB=R(s_A,k,k,s_B)`; and
- where `det D != 0`, `B=P D^-1` and its trace-free shear.

Initial point-observer data are `D(0)=0`, `P(0)=I` in the declared matched basis. No weak-field,
small-angle, frozen-curvature, post-processing, or Riccati-only approximation is permitted.

Stop a branch before the target endpoint if the solver fails, `R<=0.08`, `|sin(theta)|<=0.2`, the
metric ceases to be finite/positive in `N,L`, or a nonfinite state appears. A Jacobi caustic is not
a solver failure: retain `(D,P)` and suspend only `D^-1`.

## Numerical controls

- CPU, float64, SciPy DOP853;
- production `rtol=1e-10`, `atol=1e-12`, maximum step `0.01`;
- convergence replay `rtol=2.5e-12`, `atol=2.5e-14`, maximum step `0.005`;
- 161 saved affine samples per completed branch;
- estimated memory below 2 GiB; no background process or checkpoint required;
- outputs overwrite only this new package's declared JSON/TSV artifacts.

## Independent route

Independently reconstruct each Jacobi endpoint column by a five-point centered finite difference of
four neighboring full nonlinear geodesics whose initial unit spatial direction is rotated by
`delta in {-2h,-h,h,2h}`, `h=2e-4`, along each initial screen direction. Project the endpoint
variation onto the production branch's parallel screen. This route does not integrate the Jacobi
or Riemann equations.

## Preregistered gates

1. Exact symbolic metric, inverse, connection, Riemann symmetries, null/screen normalization, and
   G127 static vertex limit must pass.
2. Along every completed branch: null drift `<2e-9`, affine residual `<2e-9`, screen metric drift
   `<2e-9`, and screen-ray orthogonality drift `<2e-9`.
3. Production versus stricter replay endpoint differences: geodesic/screen `<2e-8`, Jacobi phase
   `<5e-8` in max norm.
4. Five-point neighboring-ray endpoint Jacobi comparison: max absolute difference `<2e-5` and max
   relative Frobenius difference `<2e-5` wherever the reference norm exceeds `1e-8`.
5. `H0` must reproduce `D=lambda I` and zero shear to `<2e-9`.
6. Every radial branch must retain equal Jacobi singular values and zero trace-free optical matrix
   to `<2e-8`; failure rejects the implementation.
7. At least one nonflat tilted branch must exhibit nonzero pathwise tidal contrast and nonzero
   finite optical shear above `1e-7`, or the G127 finite-emergence lead is not observed in this
   bounded atlas.
8. Reversing the initial tilt sign on one nonflat control must preserve scalar singular values and
   shear norm to `<2e-8`.

Raw residuals, not scaled solver residuals, control certification.

## Candidate landings

- `FINITE_PATH_SAME_HISTORY_EMERGENCE_OBSERVED`: every completed nonflat family contains a tilted
  nonzero response while the radial control stays isotropic.
- `FINITE_PATH_EMERGENCE_HISTORY_DEPENDENT`: at least one but not every completed nonflat family
  carries a tilted nonzero response.
- `LOCAL_ONLY_IN_DECLARED_ATLAS`: the G127 vertex contrast does not survive as finite pathwise
  response in the declared controls.
- `NUMERICAL_OR_TYPE_FAILURE`: any certification gate fails.

## Maximum conclusion

At most: branchwise finite-path persistence or nonpersistence of the metric-owned radial/tilted
screen response on these supplied spherical histories. No physical history, query universality,
nonspherical completion, observational curve, source law, transfer, `X_max`, bootstrap, action,
matter, mass, or signalling claim can follow.

