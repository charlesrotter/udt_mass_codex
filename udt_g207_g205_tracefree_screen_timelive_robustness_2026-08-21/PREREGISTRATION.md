# G207 preregistration

Date: 2026-08-21

## Exact tests

1. Prove `A=exp(S)` is positive, preserves the radial direction, and has determinant one on the
   screen. Derive `det g_S=det g_0` and Lorentz signature without treating common volume as gauge.
2. Prove that radial causal motion obeys the unchanged inequality `|dr/dt|<=f`. Use the complete
   G205 optical radial distance and compact-slab smoothness to decide whether every smooth supplied
   `S` preserves the G205 Cauchy slices and global hyperbolicity.
3. For every smooth static `S`, prove or refute null completeness by using
   `g_S=f[-dt^2+H_S]`, completeness of `H_S`, and the exact affine relation back to `g_S`.
4. Construct a smooth, center-regular, nonspherical screen tensor without choosing a singular
   global screen frame. With fixed unit axis `a`, define

   \[
   u=a\times x,
   \qquad
   v=x\times u,
   \qquad
   K=v\otimes v-r^2u\otimes u.
   \]

   Verify `Kx=0`, `tr K=0`, and screen eigenvalues `+/- r^2|u|^2`.
5. Use a compact-time smooth coefficient multiplying `K/(r_0^4+r^4)` to test a genuine
   time-live/nonspherical null-complete survivor. The proof must control affine energy through the
   finite live slab and reduce to G205 outside it.
6. On a supercritical G205 member, choose an exact circular-null radius `r_c`. Test the smooth
   time-live shear

   \[
   S_F=\left(\frac{t}{t_0}\right)^2
   e^{2(1-r^2/r_c^2)}\frac{K}{r_c^4}.
   \]

   At the equatorial circular orbit verify the azimuthal screen eigenvalue is `-(t/t0)^2`, all
   radial and polar geodesic residuals vanish, and the affine future is proportional to
   `integral exp[-(t/t0)^2]dt`, hence finite.
7. Derive the complete pair pullback for `J_i=alpha_i partial_t+v_i`:

   \[
   (h_S)_{ij}=-f\alpha_i\alpha_j+h_0(Av_i,Av_j).
   \]

   Prove ambient determinant-one shear does not imply pair-area or completed-scalar blindness.
   Derive the exact completed `Phi` shift and the static-clock kernel stratum.

## Certification contract

- Production: exact symbolic tensor, eigenvalue, determinant, orbit-geodesic, affine-integral, and
  pair-pullback algebra.
- Independent: separately written direct-coordinate orbit derivation plus at least 10,000 distinct
  exact-rational determinant-one local pair cases.
- At least 15 hostile catches covering trace, radial kernel, ambient volume, causal radial bound,
  static versus time-live scope, compact-time survivor, orbit residuals, affine compression,
  pair-area blindness, completed scalar, mechanization scope, history selection, and `X_max`.
- Saved artifacts replay byte-identically under `UDT_NO_WRITE=1`.
- Fresh cold adversarial review before final banking.

## Falsification

The strongest landing fails if a registered smooth `S` changes ambient volume, if the radial causal
bound is not retained, if a finite-time inextendible causal curve survives the extension argument,
if any static member is null incomplete, if the compact-time witness is incomplete, or if the
time-live circular-orbit failure does not solve every geodesic equation with finite affine length.

## Scope lock

This does not classify timelike/spacelike completeness, arbitrary radial-screen mixing, shifts,
combined common scale plus shear, trace-changing screen modes, maximal extension, observations, or
physical history ownership.
