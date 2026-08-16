# G120 exact derivation — derived spherical screen with imported radiative transfer

Date: 2026-08-16

## 1. Typed inputs

Supply one smooth time-oriented spherically symmetric history

\[
g=h_{ab}(x)dx^a dx^b+R(x)^2d\Omega^2,
\]

one regular central radial point-observer query, and one finite regular branch. G119 derives on this
class

\[
D_{\rm sky}=R O,\qquad O\in O(2),\qquad d_A^2=|\det D_{\rm sky}|=R^2.
\tag{1}
\]

For one supplied source/observer frequency query define `Z=omega_s/omega_o>0`. G117 conditionally
places the processed Pantheon+ `1+zCMB` and DES `1+zHD` coordinates in this frequency slot. This
does not identify `Z` universally with `exp(phi_pair)` or derive either catalog coordinate from the
metric.

G94 derives, after a standardized-source/isotropy readout is supplied,

\[
d_L^2=\frac{Z^3d_A^2}{\eta\epsilon},
\tag{2}
\]

where `eta` is the surviving carried amount and `epsilon` is the received-to-emitted energy per
carried unit. Neither factor is metric-derived.

## 2. Explicit temporary light bridge

Charles authorized importing radiative transfer until UDT has a native light theory. G120 adopts
the minimal historical transparent null-momentum bridge

\[
\eta=1,\qquad \epsilon=\frac1Z,
\qquad \mathcal T:=\eta\epsilon=\frac1Z.
\tag{3}
\]

This is `IMPORTED_CONDITIONAL`, not `DERIVED`. Substituting (1) and (3) into (2) gives exactly

\[
d_L^2=\frac{Z^3R^2}{1/Z}=Z^4R^2,
\qquad
\boxed{d_L=Z^2R}.
\tag{4}
\]

The positive root follows from `Z,R,d_L>0` on the regular branch. The tempting assignment
`T=1` would instead give `d_L=Z^(3/2)R`; it is a different transfer theory, not transparent
null-frequency energy propagation in G94's notation.

## 3. Exact P1 retyping

The frozen observational P1 luminosity shape is

\[
d_L^{\rm P1}(Z)=nX_{\rm eff}Z^2\left(1-Z^{-2/n}\right),
\tag{5}
\]

with

\[
n=1.0559332414320268,
\qquad
X_{\rm eff}=2085.9586748597476\ {\rm Mpc}
\]

under the G99 absolute-calibration convention. Equating (4) and (5), without refitting, yields

\[
\boxed{R_{\rm P1}(Z)=nX_{\rm eff}\left(1-Z^{-2/n}\right).}
\tag{6}
\]

Thus G119 removes the independently prescribed tensor-valued P1 screen inside the declared class.
The remaining P1 object is one scalar, empirical radius-versus-processed-frequency curve under the
imported transfer and query pins.

The physical interpretation of (6) is restricted to the outgoing catalog orientation `Z>=1`;
every evaluated SNe row has `Z>1`. For `0<Z<1` the same algebraic expression is negative and cannot
be a nonnegative areal radius. Reverse or blueshifted observer queries require their own correctly
oriented branch and must not be represented by extrapolating (6) below `Z=1`.

Equation (6) has the exact family properties

\[
R(1)=0,
\qquad
\frac{dR}{dZ}=2X_{\rm eff}Z^{-2/n-1}>0,
\qquad
\left.\frac{dR}{dz}\right|_{z=0}=2X_{\rm eff},
\tag{7}
\]

and

\[
\lim_{Z\to\infty}R(Z)=nX_{\rm eff}
=2202.6331050379085\ {\rm Mpc}.
\tag{8}
\]

Equation (8) is a formal property of the extrapolated P1 family. The SNe data stop at `z=2.2613`,
where the curve reaches about `0.89344` of that formal limit. It is not a measured asymptote and is
not `X_max`, which is an observer-pair positional-dilation asymptote of a different type.

## 4. Frozen likelihood replay

No optimizer was called and `n` remained bit-identical. One additive magnitude zero point was
analytically profiled in each already-defined likelihood.

| Dataset | Rows | Processed frequency slot | chi-square / nominal dof | Result |
|---|---:|---|---:|---|
| Pantheon+ | 1367 | `Z=1+zCMB` | `1260.8480887274907 / 1366` | calibration-sample fixed-`n` replay |
| DES-SN5YR | 1623 | `Z=1+zHD` | `1444.1864417504896 / 1622` | same low-chi-square warning |

The maximum magnitude disagreement between the recomposed curve and the frozen G117 curve is
`3.55e-15` for Pantheon+ and `1.17e-15` for DES. Chi-square disagreements are below `2e-12`.
An implementation-distinct precision-domain replay, including a DES Schur complement, agrees to
the same scale.

The DES result remains a no-large-residual rejection with an anomalously low literal chi-square.
Nothing in G120 repairs or reinterprets that released-covariance warning.
Pantheon+ is the calibration sample, not a holdout; its original joint `n` calibration used 1365
degrees of freedom. The displayed 1366 is only the fixed-`n`, one-offset replay count.

## 5. Hostile transfer check

Replacing (3) by `T=1` changes the model by the nonconstant magnitude term

\[
\Delta m=-2.5\log_{10}Z.
\]

Its range is `1.2587` magnitudes over Pantheon+ and `0.7513` over DES, so one additive offset cannot
absorb it. The profiled chi-squares rise to approximately `2279.76` and `2135.47`, respectively.
This is a catch proof for the transfer typing, not a derivation of the adopted light bridge.

## 6. What “history” is now constrained

G120 upgrades the interpretation of the frozen SNe chord: conditional on (3), the data constrain
one areal-radius-versus-processed-frequency curve in the G119 query class. They still do not supply
the complete two-dimensional orbit metric `h_ab`, a map from frequency to affine parameter or
co-present positional separation, the terminal reciprocal depth, source evolution, global branch
population, or a law selecting this curve from the metric solution space.

Consequently (6) is a conditional empirical history component, not the complete physical metric
history. A later co-present network-consistency theorem may test whether global Reciprocity,
composition, and causal/light-cone compatibility restrict complete histories, but no such condition
is used here.

## 7. Landing

```text
BLIND_VERIFIED_WITH_CAVEATS
__G119_EXACT_SCREEN_PLUS_IMPORTED_TRANSPARENT_TRANSFER_GIVES_DL_EQUALS_Z2R
__FROZEN_P1_BECOMES_ONE_CONDITIONAL_EMPIRICAL_RADIUS_FREQUENCY_CURVE
__PANTHEON_AND_DES_LIKELIHOODS_PRESERVED_WITHOUT_REFIT
__NATIVE_LIGHT_COMPLETE_HISTORY_TERMINAL_DEPTH_XMAX_AND_DOWNSTREAM_PHYSICS_OPEN
```
