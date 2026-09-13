# Exact saved-artifact cross-check

After the independent source-first implementation passed and before this run,
the parent's frozen code and all ten saved cases were read. This check is
explicitly outcome-exposed. Its purpose is correspondence at those exact
published parameter values and the stated calibration inversion, rather than
another general sampling claim.

Read the saved JSON parameter records; import no parent scientific function.
At the circle point (R,0), construct the full metric coefficients on the
spatial unit tangent. Integrate its future quadratic root in actual time by
adaptive Gauss-Kronrod quadrature, then solve angle=2pi by Brent on [e,15].
This is separate from both the parent's dt/dell integration and the reviewer's
earlier actual-time ODE. R=1, L/c_E=1.7, t_*=1 are the parent's frozen controls.
Quad epsabs/epsrel=2e-12; Brent xtol=2e-12/rtol=2e-14. Emission derivatives
use h=1e-4. Accept duration error<=3e-9, slope error<=3e-8, and recovered
kappa/initial b error<=3e-8. The entire fixed bracket is strictly positive
slice in these cases; test that before evaluating quadrature.

The candidate's exact calibration formulas are comparison-side operations on
the independently recomputed records. This is noiseless algebra validation,
not independently acquired data, an observational identifiability theorem,
or a claimed unused prediction after outcome exposure.

Existing capture wrapper, 180s/2048MiB, CPU one thread, no author import,
PYTHONDONTWRITEBYTECODE=1. Preserve any failure without overwriting.
