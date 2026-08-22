# G213 exact derivation — determinant-one spatial remainder and completed rank closure

Date: 2026-08-22

## Bounded landing

```text
DETERMINANT_ONE_SPATIAL_REMAINDER_HAS_EXACTLY_FIVE_POINTWISE_MODES
__G207_AND_G208_COVER_FOUR_LOGARITHMIC_MODE_COORDINATES
__THE_MISSING_COORDINATE_IS_RADIAL_VERSUS_SCREEN_GRADING_NOT_A_NEW_PHYSICAL_LAW
__G176_COMPLETED_PAIR_PLUS_RULER_DENSITY_IS_INFORMATION_EQUIVALENT_TO_THE_FULL_PULLBACK
__THE_G129_SIX_PAIR_DESIGN_THEREFORE_RETAINS_EXACT_RANK_TEN
__COMPLETED_METRICS_WITHOUT_RULER_DENSITIES_ARE_NOT_METRIC_FAITHFUL
__NO_NETWORK_VALUE_PROFILE_OR_PHYSICAL_PAIR_POPULATION_IS_DERIVED
```

Status: `DERIVED_CONDITIONAL__INDEPENDENTLY_VERIFIED__EXTERNAL_REVIEW_REPAIR_PENDING`.

## 1. Unique five-mode logarithmic coordinates

Fix the supplied G211 calibrated `1+3` split, positive spatial reference metric `H`, and positive
spatial metric `K`. Remove the spatial-volume scalar by

\[
\sigma=\frac16\log\frac{\det K}{\det H},
\qquad
\overline K=e^{-2\sigma}K,
\qquad
\det\overline K=\det H.
\]

The relative endomorphism

\[
R=H^{-1}\overline K
\]

is positive, `H`-self-adjoint, and has determinant one. It therefore has a unique `H`-self-adjoint
logarithm. Put

\[
\boxed{X=\frac12\log R.}
\]

Then `tr X=0`, `R=e^{2X}`, and

\[
\overline K(v,w)=H(e^Xv,e^Xw).
\]

Now supply an `H`-unit radial vector `r` and its two-dimensional orthogonal screen with projector
`P`. Define

\[
\gamma=\frac12H(r,Xr),
\qquad
w=PXr,
\qquad
S=PXP+\gamma P.
\]

The screen endomorphism `S` is self-adjoint and screen-trace-free. Direct substitution gives the
unique decomposition

\[
\boxed{
X=\gamma(2r\otimes r^\flat-P)
 +(r\otimes w^\flat+w\otimes r^\flat)
 +S.
}
\]

The three direct summands have dimensions

\[
\boxed{1+2+2=5.}
\]

In an adapted `H`-orthonormal basis this is

\[
X=
\begin{pmatrix}
2\gamma&w_1&w_2\\
w_1&-\gamma+s_1&s_2\\
w_2&s_2&-\gamma-s_1
\end{pmatrix}.
\]

The five displayed entries have a constant rank-five Jacobian with respect to
`(gamma,w1,w2,s1,s2)`. This is the complete local determinant-one spatial census after the split.

The grading mode changes the radial scale against the two screen scales while preserving total
spatial determinant. In its pure form the coframe eigenvalues are

\[
(e^{2\gamma},e^{-\gamma},e^{-\gamma}),
\]

and the relative metric eigenvalues are

\[
(e^{4\gamma},e^{-2\gamma},e^{-2\gamma}).
\]

It is distinct from the G211 relative scalar `q`, which changes all three spatial directions
together relative to the clock channel.

## 2. Global count without a logarithm

The same count follows from a Schur factorization. In an adapted orthonormal basis write any
positive determinant-one relative metric as

\[
R=\begin{pmatrix}a&c^T\\c&D\end{pmatrix},\qquad a>0.
\]

Put

\[
u=\frac ca,
\qquad
C=D-\frac{cc^T}{a},
\qquad
B=\sqrt a\,C.
\]

Positivity gives `C>0`, while `det R=a det C=1` gives `det B=1`. Therefore uniquely

\[
\boxed{
R=
\begin{pmatrix}1&0\\u&I_2\end{pmatrix}
\begin{pmatrix}a&0\\0&a^{-1/2}B\end{pmatrix}
\begin{pmatrix}1&u^T\\0&I_2\end{pmatrix}.
}
\]

Here `a` supplies one coordinate, `u` two, and the positive determinant-one screen metric `B` two.
This confirms the global pointwise `1+2+2` count on the positive stratum. These Schur coordinates
are not asserted to be the same finite factor ordering as the logarithmic summands.

## 3. What G207 and G208 covered

G207 declared an arbitrary self-adjoint screen endomorphism that kills the radial direction and is
trace-free on the screen. In the coordinates above it is exactly

\[
\gamma=0,\qquad w=0,\qquad S\in\operatorname{Sym}_0(2),
\]

so its configuration class contains the two screen-shape coordinates.

G208 declared

\[
C_W(v)=H(W,v)r+H(r,v)W
\]

for an arbitrary screen vector `W`. It is exactly

\[
\gamma=0,\qquad S=0,\qquad w=W,
\]

so its configuration class contains the two logarithmic radial-screen mixing coordinates.

Their declared logarithmic coordinate directions span rank four. Neither supplied the independent
grading coordinate `gamma`. This is a coverage result, not a claim that the four modes commute or
that their amplitudes form one selected history. G207 and G208 remain conditional configuration
tiles.

## 4. Completed pair plus density recovers the full pullback

Write a regular auxiliary pair metric as

\[
h_\sigma=-T^2(dy^0+\beta\,d\sigma)^2+L_\sigma^2d\sigma^2.
\]

Under the G176 working clarification,

\[
m=TL_\sigma=\sqrt{-\det h_\sigma},
\qquad ds=m\,d\sigma.
\]

Let `J=diag(1,m)` be the Jacobian from `(dy0,d sigma)` to `(dy0,ds)`. Then

\[
\boxed{h_s=J^{-T}h_\sigma J^{-1}},
\qquad
\boxed{h_\sigma=J^Th_sJ}.
\]

Also `det h_s=-1`. Thus, on the regular positive-density stratum,

\[
\boxed{h_\sigma\ \longleftrightarrow\ (m,h_s)}
\]

is an exact bijection once the calibrated germ and auxiliary ruler orientation are retained.
G176 completion normalizes the physical tape; it does not discard the scale because the tape
density is part of the typed completed relation.

## 5. Rank-ten reconstruction survives completion

G129's six supplied ruler directions

\[
e_1,\ e_2,\ e_3,\ e_1+e_2,\ e_1+e_3,\ e_2+e_3
\]

give a full-pullback restriction design of exact rank ten. For every one of those known pair germs,
Section 4 reconstructs its full pullback from `(m,h_s)`. The G129 component reconstruction then
recovers the ten ambient metric components exactly.

Equivalently, composing the G129 restriction map with six invertible completed-tuple coordinate
maps preserves injectivity and local differential rank. Therefore

\[
\boxed{
\text{a rank-complete valued network of typed G176 completed relations is locally metric-faithful.}
}
\]

The six-plane design remains only a sufficiency witness. G213 does not prove that Nature supplies
those six germs or that six is globally minimal.

## 6. Why the density cannot be dropped

In one calibrated ambient basis write

\[
g=\begin{pmatrix}a&b^T\\b&K\end{pmatrix}.
\]

For any positive `lambda`, define the distinct congruent metric

\[
g_\lambda=
\begin{pmatrix}1&0\\0&\lambda I_3\end{pmatrix}^{T}
g
\begin{pmatrix}1&0\\0&\lambda I_3\end{pmatrix}
=\begin{pmatrix}a&\lambda b^T\\\lambda b&\lambda^2K\end{pmatrix}.
\]

Lorentz signature is preserved. On every clock-ruler plane using the same fixed clock and any
spatial ruler `v`, the auxiliary pullback and density obey

\[
h_{\sigma,\lambda}=j_\lambda^Th_\sigma j_\lambda,
\qquad
m_\lambda=\lambda m,
\qquad
j_\lambda=\operatorname{diag}(1,\lambda).
\]

Consequently

\[
h_{s,\lambda}
=(Jj_\lambda)^{-T}h_{\sigma,\lambda}(Jj_\lambda)^{-1}
=h_s.
\]

Thus every completed normalized metric is identical while the ambient metric changes. The ruler
density carries precisely the otherwise invisible spatial calibration scale. A network of `h_s`
values without the densities is not metric-faithful, even on the G129 six-plane design.

## 7. What closes and what remains open

G213 closes the local information question left by G212:

- a typed completed relation retains its auxiliary full-pullback information;
- a rank-complete valued completed network can reconstruct the Lorentz metric;
- no second object is needed to choose a metric after that valued network is given.

It does not generate the values of the network from a few anchors, select the physical pair germs,
derive a foliation, or turn the five spatial coordinates into physical profiles. Those are separate
global/population or finite-data questions. No source, action, `X_max`, transfer law, or observation
enters this theorem.
