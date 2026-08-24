# G243 exact derivation and numerical representation

Date: 2026-08-24

## Direct reciprocal redshift

For the active bounded SNe observer query,

\[
1+z=\exp(\phi_s-\phi_o).
\]

Taking the observer calibration as the zero of depth gives

\[
\phi=\log(1+z).
\]

No angular or screen response is needed to generate this redshift. The angular sector is closed in
G243.

## Temporary transfer interface

The processed release magnitude is used only through the explicitly imported temporary radiative
transfer interface

\[
d_L=(1+z)^2R.
\]

After one additive calibration per release is removed, the relative radial observable is

\[
\theta(\phi)=5\log_{10}\frac{R(\phi)}{R(\phi_{\min})}.
\]

Equivalently,

\[
s(\phi)=\log\frac{R(\phi)}{R(\phi_{\min})}
       =\frac{\log 10}{5}\,\theta(\phi).
\]

This is a processed observational representation, not a native UDT light law.

## Registered spline representation

For each registered basis count, write

\[
\theta(\phi)=\sum_{j=0}^{K-2}c_j
\left[B_j(\phi)-B_j(\phi_{\min})\right].
\]

The last B-spline column is removed because the anchored columns retain one exact
partition-of-unity redundancy. Two further unpenalized coefficients are the Pantheon and DES
release offsets.

The observational roughness penalty is

\[
P_{ij}=\int_{\phi_{\min}}^{\phi_{\max}}B_i''(\phi)B_j''(\phi)\,d\phi.
\]

It is a numerical regularizer only. It is not an action, field equation, or physical smoothness
postulate.

For whitened design matrix \(X\), data vector \(y\), and dimensionless registered multiplier
\(\alpha\),

\[
\lambda=\alpha\frac{\operatorname{tr}(X_s^TX_s)}{\operatorname{tr}P_s},
\]

and the penalized coefficients solve

\[
(X^TX+\lambda P)c=X^Ty.
\]

The selected numerical representation minimizes

\[
\operatorname{GCV}
=\frac{N\chi^2_{\rm raw}}{(N-\operatorname{edf})^2}
\]

over the complete preregistered \((K,\alpha)\) census.

## Exact nullspace repair

The second-derivative penalty has exactly three zero modes: the two release offsets and the
anchored affine spline. The affine coefficient vector is obtained from the B-spline Greville
abscissae. The certified implementations split these three modes from the positive penalty block,
eliminate the unpenalized block by a Schur complement, and diagonalize only the positive block.

This is a numerical stability repair for extreme \(\alpha\); it does not change the represented
family or its physical interpretation.

## Observed local candidate

Both implementations independently select

```text
K = 48
alpha = 0.1
raw chi-square = 2089.791198559...
edf = 34.0920176769...
GCV = 0.899491818195...
```

The selected coefficients agree to `1.33e-12`. Its derivative is not globally positive:

```text
min s' = -1.01870213505...
max s' = 12.916873313...
```

Four positive-derivative intervals survive on the 4,097-point characterization grid. The turns
are reported and retained; they are not repaired.

## Certification landing

The exact-nullspace repair leaves 29 of 485 extreme census rows above the preregistered absolute
`1e-7` raw-chi-square cross-route tolerance. The worst difference is `9.17e-6`; every GCV row and
the selected coefficients pass their registered gates.

The controlling landing is therefore

```text
CROSS_ROUTE_OR_FULL_COVARIANCE_FAILURE__NO_FREEZE
```

The selected turning curve remains an observed, strongly reproduced local candidate. It is not a
frozen radial history and cannot be used as the unique input to later angular inversion.
