# G207 audit report — trace-free angular-screen time-live robustness

Date: 2026-08-21

## Bounded landing

```text
TRACEFREE_SCREEN_SHEAR_PRESERVES_AMBIENT_VOLUME_SIGNATURE_RADIAL_CAUSAL_BOUND_AND_G205_GLOBAL_HYPERBOLICITY
__ALL_SMOOTH_STATIC_MEMBERS_AND_COMPACT_TIME_LIVE_WITNESSES_RETAIN_NULL_COMPLETENESS
__UNRESTRICTED_SMOOTH_TIME_LIVE_SHEAR_CAN_AFFINELY_COMPRESS_A_G205_CIRCULAR_NULL_ORBIT_TO_FINITE_LENGTH
__COMPLETED_PAIR_KERNEL_HEARS_SHEAR_EXACTLY_WHEN_THE_SUPPLIED_CLOCK_GERM_HAS_SCREEN_CONTENT
__NO_PHYSICAL_S_HISTORY_OR_XMAX_SELECTION
```

Grade:
`EXTERNALLY_VERIFIED_WITH_CAVEATS__ANALYTIC_GLOBAL_THEOREMS__INDEPENDENT_ALGEBRAIC_CORE`.

## What was turned on

For every exact G205 base, G207 supplies a smooth self-adjoint spatial endomorphism `S` which
kills the radial direction and is trace-free on the angular screen. The complete metric is changed
before any observer-pair pullback:

\[
A=e^S,
\qquad
g_S=-fdt^2+h_0(A\cdot,A\cdot).
\]

This is the smallest nonconformal angular-shape tile. Common scale, shift, and radial-screen mixing
remain outside this audit.

## Exact result

The exponential is positive and determinant one on the screen. Hence the Lorentz signature and
ambient four-volume are preserved. The radial metric is exactly unchanged, and every causal curve
still obeys

\[
|dr/dt|\le f.
\]

Together with the complete G205 optical radial distance and smooth compact-slab control, this
proves that every smooth member retains the G205 `t=constant` Cauchy slices and is globally
hyperbolic. Its angular causal cones need not equal those of G205.

Every smooth static member is null complete. A center-regular nonspherical compact-time-live
witness is also null complete by an exact energy/Gronwall crossing argument.

The unrestricted live class is broader. On a supercritical G205 member, the supplied smooth shear

\[
S_F=\left(\frac{t}{t_0}\right)^2e^{2(1-r^2/r_c^2)}\frac{K}{r_c^4}
\]

preserves an exact circular null geodesic while changing its affine density to a Gaussian. Its
remaining future affine length is

\[
\frac{\sqrt\pi\,r_c\sqrt{f(r_c)}\,t_0}{2|J|}<\infty.
\]

Thus global hyperbolicity, ambient determinant one, and radial causal control do not by themselves
guarantee null completeness under arbitrary time-live angular shear.

## Completed pair response

For a supplied pair germ `J_i=alpha_i partial_t+v_i`,

\[
(h_S)_{ij}=-f\alpha_i\alpha_j+h_0(Av_i,Av_j).
\]

After the full pullback, completed-pair Dual Reciprocity gives

\[
\Phi_S=-\frac12\log\left[f\alpha_0^2-h_0(Av_0,Av_0)\right].
\]

A static clock tangent is exactly blind to pure screen shear. A clock tangent with screen content
generically hears it. The pair area and shift can also change, even though the ambient determinant
does not. No angular score is pasted onto the endpoint afterward.

## Evidence

- 36/36 production symbolic assertions pass.
- A separately written Euler-Lagrange orbit proof and 10,000 distinct exact-rational pair cases
  pass 110,009 assertions without importing production code or artifacts.
- All 10,000 generic rational cases change completed clock depth, pair area, and shift while
  preserving ambient determinant and completed reciprocal identity.
- 100-digit finite boundary controls pass.
- 24 hostile mutations are caught.
- Seven preregistered source hashes match in live repository context.
- No-write replay is byte stable.
- A fresh sealed gpt-5.4 reviewer returned `VERIFIED_WITH_CAVEATS`, found no mathematical error or
  hidden material overclaim, and retained the complete bounded landing.

The reviewer correctly retained three evidence boundaries: the global-hyperbolicity, universal
static null-completeness, and compact-live survivor results are analytic proofs rather than finite
mechanizations; live source provenance is a separate repository-context gate; and the failure
witness is conditional on G205's preregistered supercritical circular-null stratum.

## Ceiling

`S`, its axis, amplitude, and time profile are controls, not a selected UDT history. G207 does not
classify timelike/spacelike completeness, combined common scale plus shear, radial-screen mixing,
shift, trace-changing modes, maximal extension, observations, an action/source/transfer law, or
`X_max`.
