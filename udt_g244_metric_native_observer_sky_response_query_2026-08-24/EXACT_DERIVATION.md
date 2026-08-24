# G244 exact derivation — metric-native observer-sky response query

Date: 2026-08-24

## 1. Supplied geometric query

Supply a smooth time-oriented Lorentz metric, one metric-unit observer at an event, and one smooth
regular affine null observation sheet over a patch (U) of the observer celestial sphere. Let

\[
\mathcal D_n:\mathcal S_{o,n}\longrightarrow\mathcal S_{s,n}
\]

be the G188 vertex-normalized Jacobi map at the regular source endpoint on direction (n\). The
observer screen is canonically (T_nS^2). The source screen carries its positive quotient metric.

The history, observation sheet, endpoint incidence, and branch are supplied. The complete metric
determines \(\mathcal D\) on that query through

\[
g\longrightarrow\nabla^g\longrightarrow R^g
\longrightarrow\mathcal T
\longrightarrow\mathcal D.
\]

No post-readout angular coefficient enters this chain.

## 2. Intrinsic observer-sky tensor

Define, without choosing a source-screen basis,

\[
\boxed{
H_n(v,w)=\langle\mathcal D_nv,\mathcal D_nw\rangle_{\mathcal S_s}.
}
\]

Equivalently, \(H=\mathcal D^\dagger\mathcal D\). On a regular branch it is a positive symmetric
bilinear form on the observer sky tangent plane.

In passive orthonormal endpoint bases,

\[
\mathcal D\mapsto Q_s^T\mathcal DQ_o,
\qquad Q_s,Q_o\in O(2),
\]

and hence

\[
\boxed{H\mapsto Q_o^THQ_o.}
\]

The source basis cancels. Therefore (H) is an intrinsic tensor on the observer celestial sphere,
not a scalar created by selecting the G225 least-turning comparison. No cross-direction screen
transport is needed to define it pointwise.

## 3. Exact area/shape decomposition

For a regular two-dimensional map define

\[
\boxed{A=\sqrt{\det H}=|\det\mathcal D|>0,}
\]

\[
\boxed{C=\frac{H}{A},\qquad\det C=1,}
\]

and

\[
\boxed{
\mathfrak s
=\frac{(\operatorname{tr}H)^2}{4\det H}-1.
}
\]

If \(\sigma_1,\sigma_2>0\) are the singular values of \(\mathcal D\), then

\[
A=\sigma_1\sigma_2,
\]

\[
\operatorname{spec}(C)
=\left\{\frac{\sigma_1}{\sigma_2},\frac{\sigma_2}{\sigma_1}\right\},
\]

and

\[
\boxed{
\mathfrak s
=\frac{(\sigma_1^2-\sigma_2^2)^2}
       {4\sigma_1^2\sigma_2^2}\ge0.
}
\]

Thus \(\mathfrak s=0\) exactly when the screen map is conformal: \(\mathcal D=cQ\) for some
positive \(c\) and (Q\in O(2)). The complete response has not been scalarized: (C) remains the
full local determinant-one shape tensor, while \(\mathfrak s\) is its unique scalar singular-value
contrast in two dimensions.

Under a positive common scaling \(\mathcal D\mapsto c\mathcal D\),

\[
A\mapsto c^2A,
\qquad C\mapsto C,
\qquad\mathfrak s\mapsto\mathfrak s.
\]

Area and shape are therefore distinct native channels.

## 4. Parity is orientation-line-valued

The regular determinant sign obeys

\[
\operatorname{sgn}\det(Q_s^T\mathcal DQ_o)
=\det(Q_s)\det(Q_o)\operatorname{sgn}\det\mathcal D.
\]

It is an ordinary invariant sign only after compatible endpoint screen orientations are supplied,
or under (SO(2)) basis changes. Without that extra orientation data it is naturally valued in the
tensor product of the two endpoint orientation lines. The pre-outcome G244 parity correction
records this exact type.

## 5. Geometric area measure

Let the regular null sheet define a local endpoint map

\[
\Psi:U\subset S_o^2\longrightarrow\Sigma_s
\]

to a source screen cross-section. With the observer solid-angle form (d\Omega_o) and source
screen area form (dA_s), the Jacobi definition gives

\[
\boxed{
\Psi^*(dA_s)=A(n)\,d\Omega_o.
}
\]

This is the direct geometric meaning of (A=|\det\mathcal D|): source-screen area per observer
solid angle. It is not yet flux, luminosity, or a catalogue count. Those require a source density
and detector/transfer contract.

## 6. Coefficient-free angular projection

For a separately supplied normalized positive sky reference measure (Q), define the explicit
geometric-area query

\[
\boxed{
dP_A=\frac{A\,dQ}{\int A\,dQ}.
}

If (f_A=dP_A/dQ) and (K) is a bounded symmetric angular-bin kernel with positive reference
mass, the factorized reference-projected response is

\[
\boxed{
w_K^{\rm area}
=\frac{\int K(n,m)[f_A(n)-1][f_A(m)-1],dQ(n)dQ(m)}
       {\int K(n,m),dQ(n)dQ(m)}.
}

This is the G239 intensity term with the response fixed to the metric area field. There is no
angular amplitude coefficient.

If (A) is constant over the declared sky shell, normalization gives (P_A=Q) and

\[
w_K^{\rm area}=0
\]

for every bin. A nonconstant positive (A) can survive. The exact four-cell algebra witness uses

\[
Q=(1/10,1/5,3/10,2/5),
\qquad A=(1,2,1,3),
\]

and the frozen G239 control kernel, obtaining

\[
\boxed{w_K^{\rm area}=-1/6.}
\]

The four Jacobi matrices \(\operatorname{diag}(A_i,1)\) realize these determinants exactly as a
finite operator witness. They are not asserted to be samples of one physical metric history.

The step from this geometric-area query to a galaxy catalogue is still conditional. A supplied
source measure, incidence relation, branch/detection protocol, and transfer semantics decide
whether the catalogue measure is (P_A), another metric pushforward, or contains a separate G239
connected term.

## 7. Correct composition object

The Jacobi position map does not multiply under subdivision. Write the G226 full phase transfer as

\[
M_{ij}=\begin{pmatrix}A_{ij}&B_{ij}\\C_{ij}&D_{ij}\end{pmatrix},
\]

where the vertex Jacobi map is the upper-right block (B). From

\[
M_{20}=M_{21}M_{10}
\]

one obtains

\[
\boxed{
B_{20}=A_{21}B_{10}+B_{21}D_{10},
}

not (B_{21}B_{10}) in general. G244 therefore retains the full G226 phase for composition and
extracts (H,A,C,\mathfrak s) only at the requested regular endpoint.

## 8. Degenerate strata

At a caustic, \(\det\mathcal D=0\). Then (H\) remains a positive semidefinite tensor, but

\[
A=0
\]

and (C=H/A), \(\mathfrak s\), and regular inverse-density formulas leave their declared scope.
No inverse of \(\mathcal D\) is taken. The full phase remains invertible and composable as in G226.

Branch merger, nonproper or infinite fibers, coherent waves, and detector aggregation remain open.

## 9. Separation from reciprocal redshift

The SNe endpoint relation remains

\[
\boxed{\phi=\log(1+z).}
\]

The angular tensor (H) is a separately typed screen/Jacobi output. It neither generates nor
modifies the direct reciprocal redshift in this derivation. G242's rejection of exact zero tide
motivates keeping the native response live; it does not calibrate its amplitude.

## 10. Bounded landing

```text
METRIC_NATIVE_OBSERVER_SKY_AREA_SHAPE_QUERY_DERIVED_CONDITIONALLY
__NO_FITTED_ANGULAR_COEFFICIENT
__CATALOG_IDENTIFICATION_AND_HISTORY_OPEN
```

The complete metric supplies the angular area/shape response once a regular null observation sheet
is supplied. G244 derives no physical metric history, observer/source population, detector law,
catalogue map, feature scale, BAO/CMB origin, `X_max`, or global completion.

