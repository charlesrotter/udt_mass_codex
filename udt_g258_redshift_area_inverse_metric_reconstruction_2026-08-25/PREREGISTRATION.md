# G258 preregistration — redshift/area inverse metric reconstruction

Date: 2026-08-25

The current 240-row premise verifier passed before this preregistration was written. The G237 knot
values were already known from prior work; this is not a blinded observational test. The theorem,
formulas, classifications, and conclusion ceiling below are frozen before running the G258 scripts.

## Exact inputs

1. `CURRENT_SCIENTIFIC_PREMISES.tsv` for current ownership and guards.
2. G119 central-spherical finite-radius screen theorem.
3. G237 frozen `K=12` state and covariance, without refit.
4. G249/G252 one-scale homothety and attachment results.
5. G253 minimal native-kernel dependency spine.
6. G257 bounded GR quiet-limit embedding and its external acceptance.

No protected package or observational outcome outside the already frozen G237 state may be read.

## Pinned algebra

For each frozen knot, with observer depth calibrated to zero,

\[
Z_i=1+z_i=e^{\phi_i},\qquad
f_i=e^{-2\phi_i}=Z_i^{-2},\qquad
T_i=Z_i^{-1},\qquad L_i=Z_i.
\]

With the G237 relative state

\[
\theta_i=5\log_{10}\frac{R_i}{R_0},
\]

the scale-free areal ratios are

\[
\bar R_i:=\frac{R_i}{R_0}=10^{\theta_i/5}.
\]

Thus, after one still-open positive attachment `ell=R_0`, the sampled primary metric is

\[
g_i=-Z_i^{-2}c_E^2dt^2+Z_i^2dR^2+(\ell\bar R_i)^2d\Omega^2.
\]

The theorem is pointwise and sampled. It does not define derivatives, interpolation, dynamics, or
a field equation.

## Registered checks

1. Reconstruct every saved G237 relative-radius knot from `theta`.
2. Verify `T_i L_i=1`, `f_i=T_i^2`, and `Z_i=T_i^{-1}=L_i` at all twelve knots.
3. Verify the radial clock/ruler block has determinant `-1` in `x0=c_E t` units.
4. Recompute the saved delta-method relative-radius covariance from the frozen theta covariance.
5. Classify every adjacent sampled radius change with its full-covariance standard error; report
   signs and standardized values without imposing monotonicity.
6. Verify positive homothety changes only `ell`, leaving every `Z_i`, `f_i`, clock/ruler ratio, and
   relative radius unchanged.
7. A separate implementation must read the frozen source directly and reproduce the node table and
   every load-bearing classification without importing production code or output.
8. Hostile controls must catch: wrong redshift sign, post-readout angular insertion, `Z^-1` instead
   of `Z^-2` for `f`, logarithm-base error, absolute-scale self-selection, covariance
   diagonalization, forced monotonicity, and use of the static GR exterior as the SNe profile.

## Falsification and certification

- Outcome 1 requires all algebraic, covariance, independent, and hostile gates to pass.
- Outcome 2 applies if any primary metric component remains free at a sampled knot after `ell` is
  supplied.
- Outcome 3 applies if the frozen source fails a declared identity beyond the recorded covariance.
- Raw algebraic/covariance residual tolerance: `2e-12`; Decimal independent tolerance: `2e-11`.
- No observational goodness-of-fit threshold is used because the input state is already frozen.

## Maximum conclusion

G258 may establish that redshift plus relative central-spherical area reconstructs the sampled
primary metric state up to one positive absolute scale under the declared imported transfer. It may
not call that state a continuous physical history, derive radiative transfer, infer derivatives or
curvature between knots, select a UDT parent law, identify `X_max`, validate UDT, or generalize to
nonspherical/time-live/global physics.
