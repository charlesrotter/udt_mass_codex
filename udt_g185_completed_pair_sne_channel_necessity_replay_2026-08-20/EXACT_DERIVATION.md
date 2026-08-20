# G185 exact derivation — completed-pair SNe channel necessity replay

Date: 2026-08-20

## 1. Scope

This audit asks one bounded non-regression question. For the supplied central, spherical, outgoing,
regular SNe query, does the accepted completed-pair construction retain every metric channel that
is relevant to that query and reproduce the frozen Pantheon+ and DES-SN5YR conditional interface?

The audit does not derive a radiative-transfer law, a redshift history, a metric profile, a branch
population, or a value of `X_max`.

## 2. One metric, two different angular objects

The primary metric is

\[
g=-c_E^2e^{-2\phi(r)}dt^2+e^{2\phi(r)}dr^2
  +r^2d\theta^2+r^2\sin^2\theta\,d\varphi^2.
\]

For a supplied pair immersion with base tangent matrix \(Y\) and angular tangent matrix \(Z\),
the exact pullback is

\[
h=Y^TB^T\eta_2BY+Z^TQ^TQZ,
\]

where

\[
B=\begin{pmatrix}c_Ee^{-\phi}&0\\0&e^\phi\end{pmatrix},
\qquad
Q=\begin{pmatrix}r&0\\0&r\sin\theta\end{pmatrix}.
\]

The pair-plane angular Gram is therefore

\[
P_{\rm pair}=Z^TQ^TQZ.
\]

For the declared radial pair tangent, \(Z=0\), and hence

\[
\boxed{P_{\rm pair}=0.}
\]

This is not an instruction to turn off an angular sector. It is the value of the angular pullback
on that particular tangent plane. A nonradial tangent immediately restores the term. In the simple
one-spatial-parameter notation used by G180,

\[
\boxed{m^2=v^2+e^{-2\phi}r^2b^2,}
\]

so \(b^2=0\) gives \(m=|v|\), whereas every regular \(b^2>0\) contributes positively.

The observer-sky screen is a different object. The exact central-spherical screen theorem gives

\[
\boxed{\mathcal D_{\rm sky}=R O,\qquad O\in O(2),\qquad
|\det\mathcal D_{\rm sky}|=R^2.}
\]

Thus the same central radial query can consistently have

\[
P_{\rm pair}=0
\quad\text{and}\quad
|\det\mathcal D_{\rm sky}|=R^2>0.
\]

The first statement concerns angular motion of the pair plane. The second concerns the transverse
area of the observed beam. Conflating them is the category error tested by G185.

## 3. Completed reciprocal readout

On the regular calibrated pair stratum, the completed density and reciprocal readout are

\[
m=\sqrt{-\det h},
\qquad
\Phi=-\frac12\log(-h_{00}).
\]

For the primary radial pair in dimension-matched coordinates,

\[
h=\operatorname{diag}(-e^{-2\phi},e^{2\phi}),
\qquad
m=1,
\qquad
\Phi=\phi.
\]

Angular, screen, and mixing contributions are not appended after this readout. Whenever they are
present in the supplied pair realization, they enter \(h\) first. The bounded central radial result
does not claim that they vanish for other queries.

## 4. Conditional observational interface

G185 retains the G120 radiative bridge as an explicit imported conditional:

\[
F_o=\frac{L_\Omega\,\mathcal T}{Z^3R^2},
\qquad
\eta\epsilon=\frac1Z.
\]

With the conventional definition of luminosity distance inside that imported bridge,

\[
d_L^2=\frac{Z^3R^2}{\eta\epsilon}=Z^4R^2,
\]

and therefore

\[
\boxed{d_L=Z^2R.}
\]

This formula retains the metric-derived areal screen exactly once. Removing \(R\), inserting it a
second time, or replacing the imported transfer by \(\eta\epsilon=1\) changes the observable curve.
No terminal \(\Phi\) factor is inserted. Outside the pure reciprocal reduction, release-frequency
depth \(\log Z\) and terminal completed depth \(\Phi\) remain separately typed.

The radius-frequency curve is not rederived in G185. It remains the frozen historical calibration

\[
R_{\rm P1}(Z)=nX_{\rm eff}\left(1-Z^{-2/n}\right),
\qquad
n=1.0559332414320268.
\]

After profiling only the already-declared catalog magnitude offset, the shape used in the replay is

\[
5\log_{10}\!\left[Z^2n\left(1-Z^{-2/n}\right)\right],
\]

with the overall \(X_{\rm eff}\) scale absorbed by that offset exactly as in the frozen interface.

## 5. Production outcome

The production route used Cholesky whitening for both covariances. It returned

| catalog | rows | \(\chi^2\) | profiled offset |
|---|---:|---:|---:|
| Pantheon+ | 1367 | 1260.8480887274907 | 22.343528501617094 |
| DES-SN5YR | 1623 | 1444.1864417504896 | 41.708956602969536 |

Against the frozen G120 result, both chi-squares and both offsets agree exactly at the stored
floating-point precision. Maximum curve residuals are \(3.55\times10^{-15}\) mag for Pantheon+ and
\(1.17\times10^{-15}\) mag for DES.

The hostile controls were not near-degenerate alternatives:

| control | Pantheon+ \(\chi^2\) | DES \(\chi^2\) |
|---|---:|---:|
| delete the areal screen | 117950.09281570319 | 16406.38783447045 |
| duplicate the areal screen | 115567.50270059548 | 16539.659239727313 |
| replace transfer by \(\eta\epsilon=1\) | 2279.7628244181906 | 2135.4666044415126 |

## 6. Independent outcome

The independent route inverted the Pantheon+ covariance in the precision domain and reconstructed
the retained DES covariance precision by a Schur complement. Relative to production it found

\[
|\Delta\chi^2_{\rm P+}|=9.09\times10^{-13},
\qquad
|\Delta\chi^2_{\rm DES}|=2.27\times10^{-12}.
\]

It separately evaluated the radial angular Gram, the nonradial completed-density increment, the
sky determinant, and the imported transfer reduction using direct numerical matrices rather than
the production symbolic path. Every check passed.

## 7. Exact landing ceiling

The result establishes only

```text
CENTRAL_SPHERICAL_SNE_QUERY_RETAINS_THE_FULL_RELEVANT_METRIC_RESPONSE
__RADIAL_PAIR_ANGULAR_TANGENT_ZERO_IS_QUERY_DERIVED
__AREAL_SKY_RESPONSE_R2_REMAINS_ACTIVE
__FROZEN_DUAL_SNE_REPLAY_IS_CONDITIONALLY_PRESERVED
```

It does not convert the imported transfer into native UDT light physics, derive the frozen
radius-frequency history, validate nonspherical or multiple-image queries, or select a global
metric history.
