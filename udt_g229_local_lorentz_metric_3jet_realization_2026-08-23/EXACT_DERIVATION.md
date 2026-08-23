# G229 exact derivation — local Lorentz-metric 3-jet realization

Date: 2026-08-23
Status: `DERIVED_CONDITIONAL__ONE_SUPPLIED_EVENT__FIXED_TANGENT_FRAME`

## 1. Question and ceiling

G227 and G228 classify the admissible curvature value and first curvature derivative at one event.
G229 asks whether those tensors are genuinely the jets of a Lorentz metric. It does **not** ask what
their values are or which history Nature realizes.

Fix a four-dimensional tangent frame with

\[
\eta=\operatorname{diag}(-1,1,1,1),\qquad
g_{ab}(0)=\eta_{ab},\qquad g_{ab,c}(0)=0.
\]

Let

\[
H_{ab,cd}=g_{ab,cd}(0),\qquad
K_{ab,cde}=g_{ab,cde}(0),
\]

with symmetry in \((ab)\), \((cd)\), and \((cde)\). Their full dimensions are

\[
\dim H=10\cdot10=100,\qquad
\dim K=10\cdot20=200.
\]

## 2. Direct curvature maps

For the frozen convention

\[
R^\rho{}_{\sigma\mu\nu}
=\partial_\mu\Gamma^\rho{}_{\nu\sigma}
-\partial_\nu\Gamma^\rho{}_{\mu\sigma}
+\Gamma^\rho{}_{\mu\lambda}\Gamma^\lambda{}_{\nu\sigma}
-\Gamma^\rho{}_{\nu\lambda}\Gamma^\lambda{}_{\mu\sigma},
\]

direct differentiation at the locally inertial origin gives

\[
\boxed{
C_2(H)_{abcd}
=\frac12\left(
H_{ad,bc}+H_{bc,ad}-H_{bd,ac}-H_{ac,bd}
\right)
}
\]

and

\[
\boxed{
C_3(K)_{eabcd}
=\frac12\left(
K_{ad,bce}+K_{bc,ade}-K_{bd,ace}-K_{ac,bde}
\right).
}
\]

Since the connection vanishes at the origin,

\[
C_3(K)=\partial_eR_{abcd}=\nabla_eR_{abcd}.
\]

Exact elimination returns

\[
\operatorname{rank}C_2=20,
\qquad
\operatorname{rank}C_3=60.
\]

The second number is not a dimension guess. The full independent replay keeps all 84 symmetric
bivector derivative slots, imposes four algebraic-Bianchi rows and 24 generated differential rows,
and finds combined constraint rank 24. Hence the compatible target has dimension \(84-24=60\),
and the metric 3-jet map reaches all of it.

## 3. Coordinate kernels

Consider identity-linear coordinate changes

\[
x^a=y^a+\frac16A^a{}_{bcd}y^by^cy^d,
\]

where the lower three indices are symmetric. Pulling back the constant metric gives

\[
\partial_i x^a
=\delta_i^a+\frac12A^a{}_{icd}y^cy^d,
\]

so the induced quadratic metric jet is

\[
\Delta H_{ij,cd}=A_{jicd}+A_{ijcd},
\qquad A_{abcd}=\eta_{ae}A^e{}_{bcd}.
\]

The cubic-coordinate domain has dimension

\[
4\binom{6}{3}=80.
\]

Its image has rank 80 and \(C_2\Delta H=0\). Since \(\dim\ker C_2=100-20=80\),

\[
\boxed{\ker C_2=\operatorname{im}G_2.}
\]

Likewise, for

\[
x^a=y^a+\frac1{24}B^a{}_{bcde}y^by^cy^dy^e,
\]

one gets

\[
\Delta K_{ij,cde}=B_{jicde}+B_{ijcde}.
\]

The quartic-coordinate domain and image both have dimension

\[
4\binom{7}{4}=140,
\]

and \(C_3\Delta K=0\). Since \(\dim\ker C_3=200-60=140\),

\[
\boxed{\ker C_3=\operatorname{im}G_3.}
\]

These are fixed-tangent-frame statements. A linear Lorentz change would alter tensor components but
not the geometric jet; it is deliberately outside the identity-linear kernel test.

## 4. Geodesic normal slices

The radial normal-coordinate constraints are

\[
H_{i(j,kl)}=0,
\qquad
K_{i(j,klm)}=0.
\]

Generating every row without deletion gives ranks

\[
\operatorname{rank}N_2=80,
\qquad
\operatorname{rank}N_3=140.
\]

Thus their null spaces have dimensions 20 and 60. The restricted curvature maps have ranks 20 and
60, respectively, so both are isomorphisms. Moreover,

\[
\operatorname{rank}(N_2G_2)=80,
\qquad
\operatorname{rank}(N_3G_3)=140,
\]

which proves that the normal conditions uniquely fix these higher-coordinate gauges.

The exact inverse tensors are

\[
\boxed{
H^R_{ab,cd}=-\frac13\left(R_{acbd}+R_{adbc}\right)
}
\]

and

\[
\boxed{
K^D_{ab,cde}=-\operatorname{Sym}_{cde}D_{e,acbd}.
}
\]

On complete exact target bases,

\[
C_2(H^R)=R,
\qquad
C_3(K^D)=D,
\qquad
N_2H^R=0,
\qquad
N_3K^D=0.
\]

## 5. Smooth local representative

For any supplied compatible \((R,D)\), insert the normal tensors above into

\[
\boxed{
g_{ab}(x)=\eta_{ab}
+\frac12H^R_{ab,cd}x^cx^d
+\frac16K^D_{ab,cde}x^cx^dx^e.
}
\]

This is a smooth polynomial metric. The normal constraints imply the exact radial identity

\[
g_{ab}(x)x^b=\eta_{ab}x^b,
\]

so the radial coordinate lines are affinely parametrized geodesics. Since \(g(0)=\eta\), openness
of Lorentz signature supplies a sufficiently small, data-dependent neighborhood for every finite
coefficient set. No uniform radius is claimed.

Therefore

\[
\boxed{
\text{every algebraically compatible supplied }(R,\nabla R)\text{ at one event}
\text{ has a smooth local Lorentz-metric representative.}
}
\]

## 6. Recovery of G188/G227/G228 channels

Because \(C_2H^R=I_{20}\) and \(C_3K^D\) is the complete compatible 60-dimensional basis, every
linear null-screen, tidal, derivative-tidal, and Jacobi-generator contraction used in G188, G227,
and G228 factors through a realized metric jet.

The exact regression reproduces:

- G227 null-tide rank 19;
- G227 rank 20 after the timelike sectional datum;
- every one-direction G228 projection at rank 20;
- every two-direction projection at rank 40;
- every three-direction projection at rank 54, codimension 6;
- the four-direction projection at rank 60, codimension 20.

For the nonzero sign witness \(R\) given by the first G227 basis element, with
\(k=(1,0,0,1)\) and screen \((s_1,s_2)\),

\[
\mathcal T_{AB}=R(s_A,k,s_B,k)
=\begin{pmatrix}1&0\\0&0\end{pmatrix}.
\]

The G188 Jacobi equation remains

\[
\mathcal D''+\mathcal T\mathcal D=0,
\]

so its first-order generator has lower-left block \(-\mathcal T\), and
\(\mathcal D'''(0)=-\mathcal T\). This prevents an overall curvature-sign ambiguity from being
silently absorbed in the projection bridge.

## 7. What this theorem does not do

The theorem realizes **supplied point data**. It does not generate curvature values, prescribe a
curvature field across a finite region, prove overlap compatibility of independently supplied
neighboring jets, select observers or null relations, derive dynamics, or select a metric history.
Those are later questions of different type.
