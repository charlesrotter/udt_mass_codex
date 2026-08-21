# G205 preregistration

Date: 2026-08-21

## Exact tests

1. Derive the geodesic first integrals directly from the full metric. After spherical reduction to
   an equatorial plane, independently establish

   \[
   E=f\dot t,\qquad L=r^2\dot\varphi,
   \qquad
   \dot r^2=E^2+\epsilon f-\frac{fL^2}{r^2},
   \]

   for `epsilon=-1,0,+1` (timelike, null, spacelike).
2. Treat all outer cases separately: `E!=0`; causal `E=0`; and spacelike `E=0`. No radial-only
   argument may certify the nonradial family.
3. Prove center extension in smooth Cartesian coordinates. A coordinate pole in spherical
   variables is not a physical boundary.
4. Prove or refute that every geodesic trapped in a finite radial interval extends for all affine
   parameter.
5. Form the conformal ultrastatic representative

   \[
   f^{-1}g=-dt^2+\frac{dr^2}{f^2}+\frac{r^2}{f}d\Omega^2
   \]

   and prove or refute completeness of its optical spatial metric. Derive the causal-hierarchy
   verdict rather than inferring it from curvature decay.
6. Classify finite-radius Killing horizons separately from event/conformal-boundary language.
7. Register null circular orbits through the exact condition `r f'-2f=0`, equivalently
   `p=r phi'=-1`; determine whether their count depends on `a,n`.

## Verification contract

- Production route: direct Christoffel/Euler-Lagrange reconstruction plus exact symbolic limits.
- Independent route: Hamiltonian first integrals and exact-rational profile-jet/trapping census;
  it may not import production code or read production artifacts.
- Minimum independent census: 10,000 distinct exact parameter/initial-data cases.
- At least 12 hostile catches, including sign, `E=0`, nonradial, center-chart, optical/affine,
  trapping, horizon, parameter-selection, and `X_max` confusions.
- Saved JSON artifacts must replay byte-identically under `UDT_NO_WRITE=1`.
- Fresh adversarial review is required before final banking.

## Falsification

The strongest landing fails if any allowed geodesic reaches the center or outer end at finite
affine parameter without smooth extension, if an imprisoned finite-radius geodesic has an ODE
extension obstruction, or if the optical spatial metric is incomplete. One counterexample is
decisive.

## Scope locks

Geodesic completeness is not physical-history selection, a field equation, maximal analytic
extension, observational validation, or `X_max`. Global hyperbolicity is evaluated as a property of
the supplied history; it is not promoted to a founding UDT postulate.
