# G349 exact derivation — finite null-wavefront patch area

Date: 2026-09-04
Grade: `PREREGISTERED_LOCALLY_REPAIRED_PENDING_EXTERNAL_FOLLOWUP`

## Bounded landing

```text
FINITE_METRIC_NULL_PATCH_AREA_CLOSES_WITH_MULTIPLICITY
__UNION_AREA_REQUIRES_GLOBAL_PREIMAGE_IDENTIFICATION
__CAUSTICS_ORIENTATION_OBSERVER_AND_LABEL_BRANCHES_RETAINED
__NO_LIGHT_DISTANCE_POPULATION_HISTORY_SCALE_OR_XMAX_SELECTED
```

G349 selects preregistered alternatives `A`, `T1`, `J1`, `M1`, `U1`, `E1`, `C1`, `S1`,
`O1`, `L1`, and `P1`. The result is conditional on a supplied smooth Lorentzian metric, source,
compact celestial patch, regular null-geodesic family, affine cut, observer, and path labels. It
does not use a field equation and selects no metric or physical ray population.

## 1. The supplied finite null map

Let `(M,g)` be a smooth time-oriented four-dimensional Lorentzian manifold, `p in M`, and `u` a
future unit timelike vector at `p`. The celestial sphere of `u` consists of unit spacelike
directions `n in u^perp`; the corresponding normalized future null tangent is

\[
 k_u(n)=u+n,\qquad -g(k_u,u)=1.
\tag{1}
\]

Let `U` be a compact piecewise-smooth celestial patch. For every `n in U`, let `gamma_n` be the
geodesic with source `p` and tangent (1). Supply a positive smooth cut `tau(n)` such that every ray
exists regularly through that affine value and the family depends smoothly on `n`. Define

\[
 F:U\longrightarrow M,\qquad F(n)=\gamma_n(\tau(n)).
\tag{2}
\]

Equation (2), including its repetitions and critical points, is the complete finite object in this
tile. No injectivity or pre-caustic restriction is made.

## 2. A variable cut adds no transverse area term

For `v in T_nU`, vary `n` through a curve with tangent `v`. At fixed affine parameter the variation
field `J_v` is a source-vertex Jacobi field. Differentiating (2) gives

\[
 dF_n(v)=J_v(\tau(n))+d\tau_n(v)\,k_n(\tau(n)).
\tag{3}
\]

The initial conditions are `J_v(0)=0` and `D J_v(0)=d k_u(v)`. Variation of
`g(k_u,k_u)=0` gives `g(DJ_v(0),k_u)=0`. The Jacobi equation and curvature symmetries then give

\[
 {d^2\over d\lambda^2}g(J_v,k)=0,
\tag{4}
\]

with both initial value and first derivative zero. Hence `g(J_v,k)=0` all along the ray. Since
`g(k,k)=0`, equations (3)--(4) imply

\[
 g(dF(v),dF(w))=g(J_v,J_w).
\tag{5}
\]

Thus a direction-dependent affine cut changes the endpoint and therefore the value of the Jacobi
map there, but its **gradient** contributes only a null-longitudinal term and adds no transverse
area. This proves `T1`.

The right side of (5) is the pullback of the positive quotient-screen metric from G348. The
correct rank for physical transverse area is therefore

\[
 r_s(n)=\operatorname{rank}\left(T_nU\xrightarrow{dF_n}k^\perp
 \longrightarrow Q_k\right)=\operatorname{rank}[J(\tau(n))],
\tag{6}
\]

not necessarily the ordinary map rank `r_F=rank(dF)`. The two ranks obey

\[
 r_s=2\Rightarrow r_F=2,\qquad
 r_s=1\Rightarrow r_F\in\{1,2\},\qquad
 r_s=0\Rightarrow r_F\leq1.
\tag{7}
\]

In the exceptional `r_s=1,r_F=2` case, the extra ordinary direction is the null generator and the
image plane is null-degenerate, not spacelike. Relative to the source celestial metric `s_u`,
define everywhere

\[
 J_gF(n)=\sqrt{{\det(F^*g)_n\over\det(s_u)_n}}
\tag{8}
\]

using the nonnegative semidefinite Gram determinant. It is positive exactly when `r_s=2` and zero
when `r_s<2`, including an ordinary-rank-two null plane. Coordinate determinants in (8) pair with
their metric area densities and therefore define a scalar density. G348 identifies (8) pointwise
with its source-to-target directional metric-area Jacobian. This proves the repaired `J1`.

## 3. Coordinate-free finite sheet area

The ordinary area formula for a `C^1` map from a compact two-manifold to a manifold is a category-A
analysis theorem. To apply it without pretending that Lorentzian spacetime is Riemannian, choose
any auxiliary positive Riemannian metric `h` only inside the proof. At every ordinary rank-two
point the plane `P=dF(T_nU)` is either spacelike or null-degenerate by (5). Define

\[
 w_g(P)={\sqrt{\det(g|_P)}\over\sqrt{\det(h|_P)}}\geq0.
\tag{9}
\]

The weight is positive on spacelike planes and zero on null planes. If `J_hF` is the ordinary
Riemannian two-Jacobian, then

\[
 J_gF=w_g(dF(TU))J_hF.
\tag{10}
\]

Apply the standard area formula to (10):

\[
 \int_U J_gF\,d\Omega_u
 =\int_M\sum_{n\in F^{-1}(y),\,\operatorname{rank}dF_n=2}
 w_g(dF_nT_nU)\,d\mathcal H_h^2(y).
\tag{11}
\]

Where smooth sheets overlap on a set of positive two-area, their approximate tangent planes agree
almost everywhere; transverse sheet intersections occupy zero two-area. Consequently the weight
in (9) defines an intrinsic density `dA_g` on the rectifiable spacelike image, independent of `h`.
Null portions have zero metric density. With

\[
 N_s(F,U;y)=\#\{n\in U:F(n)=y,\ r_s(n)=2\},
\tag{12}
\]

equation (11) becomes

\[
 \boxed{\mathcal A_{\rm mult}(F,U)
 =\int_U J_gF\,d\Omega_u
 =\int_{F(U)_{\rm sp}}N_s(F,U;y)\,dA_g(y)}.
\tag{13}
\]

This is the exact finite sheet area, counted once for every supplied preimage. The auxiliary `h`
has cancelled and is not physical structure. The ordinary critical set `r_F<2` has zero auxiliary
two-dimensional image measure. The screen-critical set `r_s<2` can additionally contain
ordinary-rank-two null sheets of positive auxiliary area; their Lorentzian metric two-area is zero
because `w_g=0`. This proves the repaired `M1`.

## 4. Multiplicity-weighted area is not union area

Define the geometric image-union area by counting each regular image point once:

\[
 \mathcal A_{\rm union}(F,U)=\int_{F(U)_{\rm sp}}1\,dA_g.
\tag{14}
\]

Because `N_s>=1` almost everywhere on the spacelike regular image,

\[
 \boxed{\mathcal A_{\rm union}\leq\mathcal A_{\rm mult}},\qquad
 \mathcal A_{\rm mult}-\mathcal A_{\rm union}
 =\int_{F(U)_{\rm sp}}(N_s-1)\,dA_g.
\tag{15}
\]

Equality holds exactly when `N_s=1` for `dA_g`-almost every spacelike regular image point. Strict
injectivity is stronger than necessary: isolated self-intersections have zero target two-area and
do not change either integral. Thus `U1` and `E1` hold. The local field `J_gF(n)` determines (13);
it cannot by itself determine (14), because (14) requires the global equivalence relation
`F(n)=F(n')`.

The complete supplied map (2) does contain that relation. Therefore this is a need for global map
information, not a missing light, matter, or transfer law.

## 5. Critical points, folds, cusps, and orientations

At transverse screen rank one or zero, (8) vanishes. This includes every ordinary-rank-one or
rank-zero point and the mixed `r_s=1,r_F=2` null stratum. These points remain part of `F`; they can
bound or join regular sheets and alter global topology and limiting multiplicity. The ordinary
rank-losing image has zero auxiliary two-area; an ordinary-rank-two null sheet can have positive
auxiliary area while its metric two-area is zero. A caustic is not a singular spacetime or a
singular full G348 phase flow.

The mixed stratum occurs explicitly in a Lorentz frame with

\[
 k=(1,0,0,1),\qquad J_v=0,\qquad J_w=(0,0,1,0),
 \qquad d\tau(v)=1,\quad d\tau(w)=0.
\tag{16}
\]

Then `dF(v)=k` and `dF(w)=J_w` are ordinarily independent, so `r_F=2`, but `r_s=1`; their image
plane is null and its Lorentzian Gram determinant is zero. Any positive auxiliary Riemannian metric
assigns that ordinary plane positive area, which is exactly cancelled by `w_g=0`.

G348 classifies rank loss while moving along one ray. G349 does **not** equate that classification
with a complete singularity classification across the two-dimensional sky patch. A rank-one map
point need not be a fold. For example

\[
 (x,y)\longmapsto(x,y^3+xy)
\tag{17}
\]

has rank one at the origin, but the differential kernel is tangent to the critical curve there,
which is the cusp rather than fold condition. No genericity assumption was supplied.

If endpoint orientations are supplied, one may integrate a signed determinant sheet by sheet. It
can flip across a fold and cancel even when absolute sheet area is positive. It is neither (13) nor
(14). Without orientations only the nonnegative density (8) is intrinsic. This proves `C1` and
`S1`.

## 6. Exact witness maps

The preregistered witnesses separate all three finite notions.

For the fold

\[
 F(x,y)=(x^2,y),\qquad (x,y)\in[-1,1]\times[0,1],
\tag{18}
\]

`|det dF|=2|x|`, so

\[
 \mathcal A_{\rm mult}=2,\qquad
 \mathcal A_{\rm union}=1,\qquad
 \mathcal A_{\rm signed}=0.
\tag{19}
\]

For the rank-zero complex-square map on the unit disk,

\[
 F(x,y)=(x^2-y^2,2xy),
\tag{20}
\]

`det dF=4(x^2+y^2)>=0`. Hence

\[
 \mathcal A_{\rm mult}=2\pi,\qquad
 \mathcal A_{\rm union}=\pi,
\tag{21}
\]

without signed cancellation. Two transverse unit sheets meeting only at one point give both areas
equal to two despite noninjectivity. Two identically overlapping labelled unit sheets give per-label
area one, declared disjoint-union census two, and geometric union one.

These smooth-map normal forms are category-A controls for (11)--(15). They are not claims that a
particular UDT spacetime realizes those exact coordinate polynomials.

## 7. Finite observer covariance

Let a second finite timelike source observer present the **same intrinsic ray set and endpoint
assignment**. If `D(n)=omega_v(n)/omega_u(n)`, G348 gives pointwise

\[
 J'_gF(n')=D(n)^2J_gF(n),\qquad
 d\Omega_v(n')=D(n)^{-2}d\Omega_u(n).
\tag{22}
\]

Therefore

\[
 \boxed{J'_gF\,d\Omega_v=J_gF\,d\Omega_u},
\qquad
 \boxed{\mathcal A'_{\rm mult}=\mathcal A_{\rm mult}}.
\tag{23}
\]

If each observer normalizes its ray tangent to unit measured frequency, the numerical affine cut
must transform reciprocally so that the endpoints in (2) remain fixed; holding the same numerical
cut while changing tangent normalization defines a different map and is not an observer-covariance
test. Target observer changes are quotient-screen isometries. Null observers remain excluded.

Equation (23) proves `O1`; it is covariance of one supplied geometric ray map, not selection of a
preferred observer.

## 8. Path labels

For labels `ell`, each supplied map `F_ell:U_ell->M` satisfies (13)--(23) separately. A declared
disjoint union has multiplicity

\[
 N_s(y)=\sum_\ell N_s(F_\ell,U_\ell;y)
\tag{24}
\]

and is a mathematical label-counted census. Equation (24) does not say that Nature populates all
labels, with equal weights or otherwise. No label is summed, weighted, or selected physically.
This proves `L1`.

## 9. Computational evidence

The repaired production implementation passed `44321/44321` checks. It covered arbitrary passive
two-coordinate changes, 5,200 variable-cut null-cone samples, the mixed screen-rank-one/
ordinary-rank-two null witness (16), the maps (18) and (20), isolated and identically overlapping
sheets, label counts, and 5,200 finite/near-null observer changes. The
largest coordinate-invariance error was `7.285283487590277e-13`; other algebraic errors were at or
below `7.105427357601002e-15`.

The implementation-distinct route passed `14321/14321`. It used central finite differences of the
full variable-cut Minkowski map, an independent Gaussian-elimination reconstruction of (16),
mapped-cell fold areas, polar rank-zero quadrature, explicit root counts, and rapidity observers
without importing production code or reading its result. Its cut Jacobian error was
`6.64484023360501e-11`. Rank-zero quadrature errors decreased by factors greater than three on `16`,
`32`, and `64` radial refinements; the finest error was
`0.0007669903937594924`, below its registered numerical tolerance.

The first hostile run returned `20/21` solely because one prose hook searched for different wording.
The recorded repair replaced that hook with the explicit cusp (17), after which all `21/21` original
hostile mutations were caught. The external review then exposed (16); the preregistered repair adds
a twenty-second behavioral mutation forbidding ordinary-rank-two from being equated with positive
metric area. The repaired hostile route passes `22/22`. No tolerance was loosened.

## 10. Ownership and remaining boundary

This is general differential and measure geometry of a supplied Lorentzian metric. It extends the
metric-derived G348 density but is not uniquely diagnostic of UDT. The standard area formula is an
analysis tool, not a field equation or imported physical mechanism.

Every metric, source, patch, cut, geodesic family, endpoint, observer, orientation, and path label
remains supplied. The result does not provide emission, absorption, intensity, brightness, flux,
luminosity, probability, detection, or observational distance. It selects no physical ray or
observer population, metric history, occupancy, topology, stability, matter/mass, scale, `X_max`,
or canon. This proves only `P1`.
