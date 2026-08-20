# G189 exact derivation — P1-free metric/flux interface

Date: 2026-08-20

## 1. Bounded question and answer

For a supplied regular static-spherical metric history, static source/observer query, and regular
central radial null branch, the metric fixes both the frequency ratio and angular screen. With the
already authorized temporary transparent-transfer bridge, the luminosity curve is therefore fixed
by the supplied metric profile alone:

\[
\boxed{d_L(Z)=Z^2\,\phi^{-1}(\log Z+\phi_o)}
\]

on every monotone branch. This formula contains no P1 screen tensor and no post-readout angular
factor. It does not choose the function \(\phi(R)\).

The coefficient-free control \(R=R_0\tanh\phi\) is not the missing profile. It violates regular
central smoothness and, when retained only as a formal outgoing annular/catalog curve, is strongly
rejected by both frozen SNe interfaces.

## 2. Static-query frequency ratio

The primary metric is

\[
ds^2=-c_E^2e^{-2\phi(R)}dt^2+e^{2\phi(R)}dR^2+R^2d\Omega^2.
\]

A static unit observer has

\[
u=\frac{e^\phi}{c_E}\,\partial_t.
\]

For a null geodesic, stationarity conserves \(E=-k_t\). Its measured frequency is

\[
\omega=-k\cdot u=\frac{E}{c_E}e^\phi.
\]

Consequently, for source and observer on the same regular branch,

\[
\boxed{Z:=\frac{\omega_s}{\omega_o}=e^{\phi_s-\phi_o}.}
\]

This is derived for the declared static query. It is not a universal identification of every
catalog redshift with every completed terminal depth.

## 3. Metric screen and imported cargo

G188 supplies the finite Jacobi map on any supplied regular affine null query. G119 specializes it
for the central spherical branch:

\[
\mathcal D_{\rm sky}=R O,\qquad O\in O(2),\qquad
d_A^2=|\det\mathcal D_{\rm sky}|=R^2.
\]

The accepted regular-branch flux factorization is

\[
d_L^2=\frac{Z^3d_A^2}{\eta\epsilon}.
\]

The temporary transparent null-cargo bridge remains explicitly imported:

\[
\eta=1,\qquad \epsilon=Z^{-1}.
\]

It gives

\[
\boxed{d_L=Z^2d_A=Z^2R.}
\]

Thus G188 removes a separately prescribed angular screen response, but it cannot manufacture a
physical carrier or choose the radius reached at a given frequency.

## 4. What P1 actually supplied

On the outgoing static branch, set \(\phi_o=0\), so \(Z=e^\phi\). The frozen P1 curve is

\[
R_{\rm P1}(Z)=nX_{\rm eff}\left(1-Z^{-2/n}\right).
\]

It is exactly equivalent to the profile

\[
\boxed{
\phi_{\rm P1}(R)
=-\frac n2\log\left(1-\frac{R}{nX_{\rm eff}}\right).
}
\]

Therefore P1 no longer owns an independent screen or reciprocal kernel. Its remaining role is one
empirical radius-frequency, equivalently static \(\phi(R)\), profile under the imported transfer.
The SNe domain is annular and does not prove this profile is a smooth central metric history.

## 5. Why the metric form alone does not select the curve

Two smooth monotone profiles can share the same coincidence value and first derivative:

\[
\phi_1(R)=R,\qquad \phi_2(R)=R+aR^2,\qquad a>0,
\]

yet their inverse radius functions are

\[
R_1(y)=y,
\qquad
R_2(y)=\frac{\sqrt{1+4ay}-1}{2a}.
\]

They differ at every generic finite \(y\). Substituting \(y=\log Z+\phi_o\) gives different SNe
curves while preserving the same local normalization. The declared metric form and reciprocal
character therefore evaluate a supplied profile; they do not algebraically select one.

This statement concerns the configuration family, not a claim that UDT needs a foreign mechanism.
A later metric-native global or time-live condition may reduce the family.

## 6. The direct \(R\propto\chi\) control fails its type check

The currently adopted normalized pair position is

\[
\chi=\tanh\phi.
\]

The simplest scale-only screen join would be

\[
R=R_0\chi,
\qquad
\phi(R)=\operatorname{artanh}(R/R_0).
\]

But a smooth rotationally invariant scalar at a regular center has an even radial expansion,

\[
\phi(R)=\phi(0)+aR^2+O(R^4),
\qquad \phi'(0)=0.
\]

The proposed join instead gives

\[
\left.\frac{d\phi}{dR}\right|_{R=0}=\frac1{R_0}\ne0.
\]

It is therefore not a globally regular central-static metric realization. A smooth-even control
\(\phi=aR^2\) gives

\[
R=\sqrt{\log Z/a},
\]

showing that regular-center static scaling has a different low-depth structure. The computed
\(R=R_0\chi\) catalog curve is retained only as a formal outgoing annular control.

## 7. Frozen no-shape-fit result

The formal control has

\[
\frac{d_L}{R_0}
=Z^2\tanh(\log Z)
=Z^2\frac{Z^2-1}{Z^2+1}.
\]

No shape parameter was fitted. Only the existing additive magnitude zero point was analytically
profiled per catalog.

| catalog | rows | P1 \(\chi^2\) | control \(\chi^2\) | preregistered ceiling |
|---|---:|---:|---:|---:|
| Pantheon+ | 1367 | 1260.848088727491 | 3204.950963265004 | 1627.342686907440 |
| DES-SN5YR | 1623 | 1444.186441750489 | 2685.911034093437 | 1906.780617317963 |

The preregistered landing is therefore

```text
R_PROPORTIONAL_CHI_JOIN_REJECTED_IN_DECLARED_SNE_INTERFACE
```

The implementation-distinct precision replay agrees within \(1.1\times10^{-11}\) in chi-square
and \(2.2\times10^{-14}\) in the profiled offsets.

An alternate transfer-product control changes the scores substantially. Because the physical
transfer product remains open and the temporary bridge was pinned before this test, that control
is diagnostic only; it is not used to select a transfer exponent from SNe.

## 8. Exact landing

```text
STATIC_CHI_SCREEN_JOIN_TYPE_FAILS_REGULAR_CENTER
__AND_IS_DATA_REJECTED_AS_A_FORMAL_ANNULAR_CONTROL
__METRIC_TO_FLUX_FACTORIZATION_CLOSES_CONDITIONALLY
__P1_ROLE_LOCALIZED_TO_UNOWNED_PHI_OF_R_OR_TIMELIVE_FREQUENCY_HISTORY
```

The reciprocal kernel, G188 screen propagation, time-live histories, displaced queries, and native
radiative transfer are outside this negative. The next metric-led question is not another fitted
radial profile. It is whether the complete time-live pair/ray geometry produces a frequency-screen
relation without identifying areal radius directly with dimensionless \(\chi\).
