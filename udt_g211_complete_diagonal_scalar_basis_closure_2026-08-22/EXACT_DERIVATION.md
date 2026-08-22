# G211 exact derivation — complete diagonal-scalar basis closure

Date: 2026-08-22

## Bounded landing

```text
COMPLETE_LOCAL_DIAGONAL_SCALAR_SECTOR_HAS_RANK_TWO_AFTER_SUPPLIED_1PLUS3_REFERENCE
__COMMON_SCALE_AND_RELATIVE_SPATIAL_VOLUME_FORM_AN_EXACT_BASIS
__LAPSE_ONLY_IS_NOT_A_THIRD_TILE
__CAUSAL_CONES_DEPEND_ONLY_ON_RELATIVE_MODE_WHILE_NULL_AFFINE_AND_COMPLETED_DEPTH_HEAR_COMMON_SCALE
__NO_PHYSICAL_SCALAR_HISTORY_OR_XMAX_SELECTION
```

This is a metric decomposition and conditional response theorem. It selects no scalar function or
physical history.

## 1. Supplied split and unique scalar coordinates

Fix a supplied time foliation, positive reference lapse square `f`, positive spatial reference
metric `H`, and supplied shift `b`. Let another metric in the same calibrated split have positive
lapse square `F` and positive spatial metric `K`. Define

\[
\boxed{
\ell=\frac12\log\frac Ff,
\qquad
\sigma=\frac16\log\frac{\det K}{\det H},
\qquad
\overline K=e^{-2\sigma}K.
}
\]

Then `det(K_bar)=det(H)`. Positivity makes both logarithms real. Ratios of the lapse coefficients
and determinants prove uniqueness exactly as in G210. Thus, after the split and references are
supplied, the diagonal scalar sector has two coordinates: lapse scale `ell` and spatial-volume
scale `sigma`. The determinant-one spatial remainder and shift are separate supplied sectors.

These variables are calibrated-split quantities. This theorem does not derive the foliation.

## 2. Common/relative basis and closure of the lapse tile

Write the metric on `X=alpha partial_t+v` as

\[
g_{\ell,\sigma,b}(X,X)
=-e^{2\ell}f\alpha^2
+e^{2\sigma}h_A(v+\alpha b,v+\alpha b),
\]

where `h_A` is any supplied positive determinant-normalized spatial metric. Define

\[
\boxed{\Omega=\ell,\qquad q=\sigma-\ell.}
\]

Then

\[
\boxed{
g_{\ell,\sigma,b}
=e^{2\Omega}
\left[-fdt^2+e^{2q}h_A(dx+b\,dt,dx+b\,dt)\right]
=e^{2\Omega}g_{q,b}.
}
\]

The inverse map is

\[
\ell=\Omega,
\qquad
\sigma=\Omega+q.
\]

The linear transformation has determinant one. Therefore the G206 common scale and the G210
relative spatial-volume mode form a basis of the complete local diagonal scalar plane.

A lapse-only deformation has `sigma=0`, hence

\[
\boxed{\Omega=\ell,\qquad q=-\ell.}
\]

It is a particular mixture of the two basis modes, not a third independent local scalar.

## 3. Volume/cone coordinates

Two other exact linear combinations expose what different instruments hear:

\[
\boxed{
V=\ell+3\sigma,
\qquad
W=\ell-\sigma=-q.
}
\]

Their inverse is

\[
\boxed{
\ell=\frac{V+3W}{4},
\qquad
\sigma=\frac{V-W}{4}.
}
\]

The transformation determinant is `-4`, so it also has rank two. The absolute four-volume density
relative to the supplied reference scales as

\[
\frac{\sqrt{|\det g_{\ell,\sigma,b}|}}
{\sqrt{f\det H}}
=e^{\ell+3\sigma}=e^V,
\]

while every causal-ellipsoid radius acquires the common factor

\[
e^{\ell-\sigma}=e^W=e^{-q}.
\]

Volume and causal width therefore provide two independent readouts of the same two-scalar plane.

## 4. Complete local ADM algebra

Put `u=e^(2 ell)` and `z=e^(2 sigma)`. In a spatial basis,

\[
g_{\ell,\sigma,b}=
\begin{pmatrix}
-uf+zb^THb&(zHb)^T\\
zHb&zH
\end{pmatrix}.
\]

The unit-determinant shift congruence gives

\[
\operatorname{inertia}(g_{\ell,\sigma,b})=(-,+,+,+),
\]

\[
\boxed{\det g_{\ell,\sigma,b}=-ufz^3\det H.}
\]

The inverse is

\[
\boxed{
g_{\ell,\sigma,b}^{-1}=
\begin{pmatrix}
-1/(uf)&b^T/(uf)\\
b/(uf)&z^{-1}H^{-1}-bb^T/(uf)
\end{pmatrix}.
}
\]

Hence `g^{-1}(dt,dt)=-1/(uf)<0`: the supplied time function remains temporal for every smooth
finite pair of scalar modes.

## 5. Exact causal separation

For a causal tangent `partial_t+v`,

\[
\boxed{
e^{2\sigma}h_A(v+b,v+b)\le e^{2\ell}f.
}
\]

The center remains `v=-b`. For any spatial covector `xi`,

\[
\boxed{
|\xi(v)+\xi(b)|
\le \sqrt f\,e^{\ell-\sigma}|\xi|_{h_A^{-1}}
=\sqrt f\,e^{-q}|\xi|_{h_A^{-1}}.
}
\]

The common scale `Omega` cancels. On G205,

\[
\boxed{
\left|\frac{dr}{dt}+b^r\right|\le f e^{-q}.
}
\]

Because `g=e^(2 Omega)g_q`, the metrics have exactly the same unparametrized timelike, null, and
causal curves. Thus global hyperbolicity depends on the supplied relative metric `g_q`, not on
`Omega`. If `g_q` has Cauchy `t`-slices, so does every smooth positive common rescaling. This is a
conditional transfer theorem, not a universal theorem for arbitrary `q`.

## 6. Null-affine composition

For a `g_q`-null affine tangent `k`, the conformal connection formula gives an affine
`g`-tangent `exp(-2 Omega)k`. Corresponding affine parameters obey

\[
\boxed{d\lambda_g=e^{2\Omega}d\lambda_q.}
\]

Consequently, at every end of every maximal unparametrized `g_q` null geodesic,

\[
g\text{ has infinite null affine reach}
\iff
\int e^{2\Omega}\,d\lambda_q=\infty.
\]

The base affine interval need not itself be infinite; the weighted integral is the exact joint
criterion.

For static radial unshifted G205, stationarity gives

\[
E=e^{2\ell}f\dot t.
\]

The null equation yields

\[
\boxed{
\dot r=\pm E e^{-(\ell+\sigma)},
\qquad
\frac{d\lambda}{dr}=\frac{e^{\ell+\sigma}}{E}
=\frac{e^{2\Omega+q}}{E}.
}
\]

Thus causal width hears only `q`, while affine reach hears the joint density `2 Omega+q`.

## 7. Exact G205 radial controls

Let `phi` be any registered G205 profile.

1. **Base:** `Omega=0,q=0` is the complete G205 metric.
2. **Common-only failure:** `Omega=-phi,q=0` has exactly the base causal curves and Cauchy slices,
   but radial affine density `exp(-2phi)` is integrable. It is radial-null incomplete.
3. **Relative-only failure:** `Omega=0,q=-phi` is the G210 control. Its causal width scales as
   `exp(phi)` and radial affine density `exp(-phi)` is integrable.
4. **Affine compensation:** `Omega=phi/2,q=-phi` has exactly the same causal curves as the
   relative-only control, but radial affine density is identically one. The outgoing radial ray has
   infinite affine reach.

The fourth control proves only radial restoration, not full null completeness. Together the
controls show that equal cones do not determine affine reach and equal relative mode does not
determine completed depth.

## 8. Completed observer-pair response

For supplied pair tangents `J_i=alpha_i partial_t+v_i`, set `w_i=v_i+alpha_i b`. Then

\[
\boxed{
h_{ij}
=-e^{2\ell}f\alpha_i\alpha_j
+e^{2\sigma}h_A(w_i,w_j)
=e^{2\Omega}\left[-f\alpha_i\alpha_j+e^{2q}h_A(w_i,w_j)\right].
}
\]

On the regular clock stratum,

\[
T^2=e^{2\Omega}
\left[f\alpha_0^2-e^{2q}h_A(w_0,w_0)\right],
\]

and completed-pair Dual Reciprocity gives

\[
\boxed{
\Phi
=-\Omega
-\frac12\log\left[f\alpha_0^2-e^{2q}h_A(w_0,w_0)\right].
}
\]

Therefore:

- every regular completed clock hears common scale through `-Omega`;
- a generic spatially bearing clock also hears `q` before readout;
- an Eulerian-normal clock `w_0=0` is exactly `q`-blind but still hears `Omega`;
- an unshifted coordinate-static clock is the same `q`-blind stratum;
- ambient determinant or causal response alone does not determine completed depth.

The arbitrary-calibration conformal control remains a control and is not substituted for `Phi`.

## 9. What is and is not closed

G211 closes the complete two-dimensional local diagonal scalar plane after the calibrated `1+3`
reference is supplied. There is no third independent lapse scalar in that plane. This is a basis
closure, not a physical-function closure.

The theorem does not select `ell`, `sigma`, `Omega`, `q`, the lapse, the foliation, a determinant-one
spatial history, a complete metric history, transfer, observations, action/source/matter, or
`X_max`. Arbitrary live null completeness beyond the integral criterion, timelike/spacelike
completeness, maximal extension, and global realization remain open.

## Evidence precision

The production algebra, independent exact-Fraction census, and high-precision radial controls
certify the finite identities and boundary anchors. Global causal transfer and the all-null affine
criterion are analytic theorems; finite scripts do not mechanize their universal quantifiers.
