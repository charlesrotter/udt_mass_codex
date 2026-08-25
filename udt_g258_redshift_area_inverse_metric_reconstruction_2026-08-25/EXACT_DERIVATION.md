# G258 exact derivation — redshift/area inverse metric reconstruction

Date: 2026-08-25

## 1. Direct sampled reconstruction

On the supplied calibrated source-observer frequency query, the active conditional attachment is

\[
Z:=1+z=e^\phi.
\]

The primary determinant-one radial metric uses

\[
f=e^{-2\phi},\qquad T=e^{-\phi},\qquad L=e^{+\phi}.
\]

Therefore every sampled redshift fixes the reciprocal radial block pointwise:

\[
\boxed{T=Z^{-1},\qquad L=Z,\qquad f=Z^{-2},\qquad TL=1.}
\]

No angular amplitude or profile coefficient enters this map.

G119 proves `d_A=R` on a supplied regular central-spherical radial null branch. The frozen G237
state uses the explicitly imported temporary transfer interface and records

\[
\theta_i=5\log_{10}\frac{R_i}{R_0}.
\]

Hence

\[
\boxed{\bar R_i:=\frac{R_i}{R_0}=10^{\theta_i/5}.}
\]

Writing the still-open positive absolute attachment as `ell=R_0`, the sampled metric values are

\[
\boxed{
g_i=-Z_i^{-2}c_E^2dt^2+Z_i^2dR^2+(\ell\bar R_i)^2d\Omega^2.
}
\]

This is an inverse value map at the frozen state knots. It is not interpolation or an equation of
motion.

## 2. Exact scale separation

The transformation

\[
R_i\mapsto aR_i,\qquad a>0,
\]

changes `ell` but leaves every `bar R_i`, `Z_i`, `f_i`, `T_i`, and `L_i` unchanged. Thus the frozen
state plus reciprocal redshift fixes the complete dimensionless sampled radial history, while one
positive absolute scale remains. This is exactly the G249/G252 attachment type; it is not a new
kernel coefficient.

## 3. Covariance transport and the upper-edge turn

For the eleven non-anchor state coordinates,

\[
\frac{\partial\bar R_i}{\partial\theta_i}
=\frac{\log 10}{5}\bar R_i.
\]

Therefore the frozen covariance transports as

\[
C_R=J C_\theta J^T,
\qquad
J_{ij}=\delta_{ij}\frac{\log10}{5}\bar R_i.
\]

The production reconstruction reproduces the saved delta-method covariance exactly at binary
precision, and the independent 60-digit Decimal route agrees within the preregistered tolerance.

Ten of eleven adjacent sampled changes are positive. The last is

\[
\Delta\bar R_{10\to11}=-0.0737469542,
\qquad
\sigma_\Delta=0.2379746641,
\qquad
\frac{\Delta\bar R}{\sigma_\Delta}=-0.309894.
\]

Thus the displayed final downturn is retained, but it is only a `0.31 sigma` sampled fluctuation
under the frozen covariance. G258 neither repairs it nor promotes it to a physical turning point.
The two preceding positive changes are also below `2 sigma`, which explains why derivative-based
smooth inversions were unstable near the upper edge even though the value-level state is coherent.

## 4. What W3 contributes—and does not

G257 proves that the primary metric contains an exact bounded static-spherical GR vacuum exterior.
W3 requires the eventual UDT parent law to reduce to GR in the quiet regime and to depart through
the same metric machinery at extremes.

G258 does **not** impose the static vacuum formula `f=1+C/R` on the cosmological SNe branch. That
would confuse one exact GR comparison solution with a different observer relation and would turn
W3 into an unsupported global history prescription. Instead:

- G257 supplies an exact low-regime comparison rail;
- reciprocal redshift fixes the directional clock/ruler state at every SNe knot;
- the conditional area/transfer chain locates those states at relative areal radii;
- a future parent law must join these constraints covariantly.

## 5. Exact remaining freedom

G258 removes the claim that every macro radial value remains wholly unknown. On the declared
processed query, twelve sampled relative metric states are already observationally anchored.

It leaves open:

1. the radiative-transfer law that made `R` observable;
2. the one positive absolute scale `ell`;
3. interpolation and derivatives between the twelve knots;
4. metric values outside the sampled interval;
5. the time-live and nonspherical fields;
6. observer/null-branch population and global completion;
7. the covariant UDT parent law joining the exact GR regime to the macro state.

## 6. Landing

```text
POINTWISE_RELATIVE_METRIC_STATE_RECONSTRUCTS
__ZERO_UDT_SHAPE_FIT_COEFFICIENTS
__ONE_ABSOLUTE_SCALE_REMAINS
__FINAL_SAMPLED_DOWNTURN_IS_ONLY_MINUS_0P31_SIGMA
__CONTINUOUS_AND_COVARIANT_PARENT_LAW_REMAINS_OPEN
```
