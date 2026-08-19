# G176 exact derivation — completed-pair Dual Reciprocity

Date: 2026-08-19

## 1. Declared domain

Charles provisionally clarifies the physical scalar-kernel domain as the **completed UDT reciprocal
observer pair**. Angular, screen, and mixing data enter its metric pullback first. An arbitrary
metric-length or otherwise calibrated curve is a different query type and remains useful as a
control, but it is not a rival reciprocal kernel.

This clarification is `WORKING_FOUNDATIONAL_CLARIFICATION`, not canon. The derivation below is
conditional on it.

## 2. Generic completed pair

Write any regular time-oriented auxiliary pair metric as

\[
h_\sigma=-T^2(dy^0+\beta\,d\sigma)^2+L_\sigma^2d\sigma^2,
\qquad T>0,\quad L_\sigma>0.
\]

Its matrix and determinant are

\[
h_\sigma=
\begin{pmatrix}
-T^2&-T^2\beta\\
-T^2\beta&L_\sigma^2-T^2\beta^2
\end{pmatrix},
\qquad
\det h_\sigma=-T^2L_\sigma^2.
\]

All complete-metric contributions are already contained in \(T,L_\sigma,\beta\) at this stage.

Let the physical ruler coordinate satisfy

\[
ds=m\,d\sigma,\qquad m>0.
\]

Then

\[
h_s=-T^2\left(dy^0+\frac{\beta}{m}ds\right)^2
+\frac{L_\sigma^2}{m^2}ds^2.
\]

Therefore

\[
T_s=T,\qquad L_s=\frac{L_\sigma}{m},\qquad
\beta_s=\frac{\beta}{m},
\]

and

\[
\det h_s=-\frac{T^2L_\sigma^2}{m^2}.
\]

The shift is retained. It cancels from the determinant because the completed clock/ruler
decomposition is triangular, not because it has been turned off.

## 3. Reciprocal normalization theorem

Dual Reciprocity on the completed pair requires the clock and ruler factors to be contragredient:

\[
T_sL_s=1.
\]

Since all three quantities are positive,

\[
T\frac{L_\sigma}{m}=1
\quad\Longleftrightarrow\quad
\boxed{m=T L_\sigma}
\quad\Longleftrightarrow\quad
\boxed{m=\sqrt{-\det h_\sigma}}.
\]

Equivalently,

\[
\boxed{\det h_s=-1}.
\]

The positive solution is unique. Thus no nonconstant family of physical ruler densities survives
inside the completed reciprocal-pair type. The terminal scalar is

\[
\Phi=\frac12\log\frac{L_s}{T_s}=-\log T.
\]

This does not say that every calibrated curve has determinant one. It says that a completed pair
called the UDT reciprocal pair has the founded reciprocal normalization.

## 4. Covariance

For an orientation-preserving auxiliary reparameterization
\(\sigma=k\widetilde\sigma\), \(k>0\),

\[
L_{\widetilde\sigma}=kL_\sigma,\qquad
\beta_{\widetilde\sigma}=k\beta,\qquad
m_{\widetilde\sigma}=km.
\]

The calibrated metric, \(L_s\), \(\beta_s\), determinant, and \(\Phi\) are unchanged. Orientation
reversal flips the directed shift and ruler orientation while preserving the determinant and scalar
magnitude. The normalization is therefore a density law, not a privileged auxiliary chart.

## 5. Static spherical turning family

For G173,

\[
T=e^{-\phi},qquad
L_\sigma^2=H=e^{2\phi}v^2+r^2b^2.
\]

The theorem gives

\[
\boxed{m^2=e^{-2\phi}H
=v^2+e^{-2\phi}r^2b^2}.
\]

Consequently,

\[
L_s^2=\frac{H}{m^2}=e^{2\phi},qquad
\det h_s=-1,qquad
\boxed{\Phi=\phi}.
\]

For a pure radial segment \(b=0\), \(m=|v|\), recovering the founded radial tape. At an angular
radial turn \(v=0\), \(b\ne0\), \(r>0\),

\[
m^2=e^{-2\phi}r^2b^2>0,
\]

so the reciprocal calibration remains regular whenever the complete spatial tangent remains
nonzero.

## 6. Where the orchestra remains

The normalization does not bolt an angular correction onto an already computed scalar. Complete
metric data first determine \(T,L_\sigma,\beta\). Reciprocity then grades the ruler.

- Contributions entering only \(L_\sigma\) change the physical ruler map
  \(ds=T L_\sigma d\sigma\).
- Contributions changing the clock scale \(T\) change \(\Phi=-\log T\).
- Shift remains \(\beta_s=\beta/(T L_\sigma)\).
- Screen orientation, Jacobi data, and holonomy remain separately typed non-scalar outputs.

Thus the orchestra changes the completed relation without becoming a post-processing scalar score.

## 7. Regrading G173--G175

G173--G175 remain correct classifications of the broader arena of arbitrary calibrated curves.
Their \(m_A\), metric-arclength, and other densities are lawful control queries. They are not
alternative physical reciprocal kernels under the G176 clarification.

G175's exact recalibration law also remains true. It shows why position-dependent regrading changes
the query; it no longer represents residual ambiguity inside one completed reciprocal pair.

## 8. Status and ceiling

- `WORKING_FOUNDATIONAL_CLARIFICATION`: Dual Reciprocity applies after the complete pair pullback.
- `DERIVED_CONDITIONAL`: unique positive reciprocal density
  \(m=T L_\sigma=\sqrt{-\det h_\sigma}\), determinant one, and \(\Phi=-\log T\).
- `DERIVED_BOUNDED`: static angular-turn specialization and radial recovery.
- `RECLASSIFIED_CONTROLS`: arbitrary calibrated curves are other query observables, not rival
  reciprocal kernels.
- `OPEN`: which observer events and pair germs are physically realized; singular/global strata;
  non-scalar transport; distance, `X_max`, observations, radiative transfer, dynamics, action,
  source, matter, bootstrap, mass, and signalling.

The maximum conclusion is scalar-kernel normalization closure on supplied regular completed
physical UDT reciprocal pairs. It is not a global relation-selection theorem.
