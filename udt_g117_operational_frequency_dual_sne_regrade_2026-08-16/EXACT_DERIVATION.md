# G117 exact derivation — operational frequency coordinate and SNe regrade

Date: 2026-08-16

## 1. The type correction

For the declared observational protocol, let

\[
Z_{\rm obs}=1+z_{\rm release},\qquad \zeta_{\rm obs}=\log Z_{\rm obs}.
\]

Pantheon+ `zCMB` and DES `zHD` are processed release coordinates rooted in spectroscopic redshift.
They are conditionally adopted for G94's frequency slot. They are neither Lambda-CDM/UDT distances,
untouched one-ray ratios, nor G116-derived global coordinates.

G116 gives, locally on its regular central spherical time-live two-jet,

\[
\zeta=\phi_{\rm pair}+v_{\rm rel}R+
\left(\dot v_{\rm rel}-\frac{\mathcal A_{\rm opt}}4\right)R^2+O(R^3).
\]

Therefore the catalog identification `phi_pair=log(1+z)` is not universal. It is exact on the pure
stationary reciprocal reduction, where the correction vanishes. More generally,

\[
\phi_{\rm pair}=\zeta-v_{\rm rel}R-
\left(\dot v_{\rm rel}-\frac{\mathcal A_{\rm opt}}4\right)R^2+O(R^3).
\]

The same restriction applies to `c_eff/c_E=Z_obs^-2`: it follows from
`c_eff/c_E=exp(-2 phi_pair)` only when `phi_pair=zeta_obs`.

## 2. Why the frozen SNe curve does not change

G94's regular-branch geometric factorization uses the frequency ratio itself:

\[
Z=\omega_s/\omega_o,\qquad d_G=Z d_A.
\]

Under the still-conditional transparent null-momentum transfer, the luminosity relation is

\[
d_L=Z^2d_A.
\]

The frozen P1 SNe chord can therefore be typed directly by the observed frequency coordinate:

\[
\lambda_A(\zeta)=n\left(1-e^{-2\zeta/n}\right),
\qquad D_{\rm sky}=\lambda_A I_2,
\]

\[
d_{L,\rm shape}
=e^{2\zeta}\sqrt{\det D_{\rm sky}}
=nZ^2\left(1-Z^{-2/n}\right).
\]

This explicitly supersedes only G94's old conditional identification `Z=exp(phi_pair)`. G94's
independent Wronskian result, endpoint-clock algebra, and conditional transfer factorization remain
intact. The result is algebraically the old P1 formula, but it no longer requires an unsupported universal
identification between terminal depth and observed frequency. No G116 correction is appended to
the curve: the correction belongs inside the relation between `zeta` and `phi_pair`.

## 3. Exact non-identifiability from SNe alone

The preregistered rational local witness takes

\[
\zeta=\frac3{100},\quad R=\frac1{100},\quad
v_{\rm rel}=\frac1{50},\quad \dot v_{\rm rel}=\frac1{70},\quad
\mathcal A_{\rm opt}=\frac1{30}.
\]

The live correction is

\[
\Delta=\frac{337}{1680000},
\]

so two distinct terminal depths survive:

\[
\phi_{\rm pure}=\frac3{100},\qquad
\phi_{\rm live}=\frac{50063}{1680000}.
\]

Both return the same formal local frequency depth because `phi_live+Delta=zeta`. The G116 witness
is not extrapolated across the SNe range. The frozen likelihood is a function of its release
coordinate and supplied screen chord and omits `phi_pair` and the G116 coefficients by construction.
It therefore proves structural non-identifiability only inside this conditional interface—not two
global physical histories with one metric-derived screen. An independently derived screen history
or terminal-depth observable could break it.

## 4. Numerical replay

No optimizer was called and `n=1.0559332414320268` remained bit-identical.

| Reduction | Rows | chi-square / nominal dof | Status |
|---|---:|---:|---|
| Pantheon+ `zCMB` | 1367 | `1260.8480887274925 / 1366` | compatible fixed-`n` replay; calibration sample |
| DES `zHD` | 1623 | `1444.1864417504900 / 1622` | no large-residual rejection; low-chi-square warning |

The maximum retyped-versus-legacy magnitude disagreement was `1.07e-14` for Pantheon+ and
`3.11e-15` for DES. An implementation-distinct precision-domain replay agrees with production to
`6.83e-13` in Pantheon+ chi-square and `1.59e-12` in DES chi-square.

Pantheon+ remains the calibration source. The conditional fixed-`n` replay has one profiled offset,
so its replay dof is 1366; its goodness-of-fit provenance remains the original G99 calibration,
which fitted `n` on the same data and recorded 1365.
DES retains its previously banked covariance/effective-dof warning.

## 5. What was removed and what remains

Removed from the active interface:

- universal `phi_pair=log(1+z_release)`;
- universal `c_eff/c_E=(1+z_release)^-2`;
- any need to append an angular/orchestra correction after P1;
- the claim that SNe separately measures terminal depth, sky area, or G116 jet coefficients.

Still conditional/open:

- the P1 screen chord as the output of one physical complete history;
- transparent null-momentum transfer and source population;
- values and finite-radius evolution of `v_rel`, `dot(v_rel)`, and `A_opt`;
- global history, regime evolution, `X_max`, BAO/CMB, bootstrap, action, matter, mass, and signalling.

## 6. Landing

```text
RETYPE_PRESERVES_DUAL_SNE_ANCHOR
__OBSERVED_FREQUENCY_COORDINATE_REPLACES_UNIVERSAL_TERMINAL_DEPTH_IDENTIFICATION
__G116_TERMINAL_DECOMPOSITION_NOT_IDENTIFIED_BY_CURRENT_SNE_INTERFACE
__P1_SCREEN_CHORD_TRANSFER_AND_PHYSICAL_HISTORY_REMAIN_CONDITIONAL
```
