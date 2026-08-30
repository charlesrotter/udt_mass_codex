# G302 exact derivation — reciprocal trace span and curvature-channel separation

Date: 2026-08-30

## 1. Internal bounded landing

```text
RECIPROCAL_SHAPE_SPANS_NINE_AND_COMPLETE_SCALE_RESTORES_TEN
__NO_G301_CLASS_SELECTED__TRACEFREE_BRANCH_HAS_EXACT_CHANNEL_SEPARATION
```

Status: `INTERNALLY_VERIFIED_BOUNDED_CLASSIFICATION_PENDING_FRESH_EXTERNAL_REVIEW`.

This is a two-gate conditional classification.  Gate A is a full four-dimensional local
metric-tangent result over the algebraically available pair-plane control family.  Gate B is an
exact static, diagonal, areal-spherical response result conditional on the G301 trace-free Ricci
class.  Neither gate adopts a field equation, selects a physical history/query population, changes
the UDT metric or reciprocal kernel, or derives mass.

## 2. Gate A: the exact reciprocal metric tangent

On one orthonormal timelike-spacelike pair plane, let

\[
D(s)=\operatorname{diag}(e^{-s},e^s),\qquad
h(s)=D(s)^T\operatorname{diag}(-1,1)D(s).
\]

Then

\[
h(s)=\operatorname{diag}(-e^{-2s},e^{2s}),
\qquad
\dot h(0)=2\operatorname{diag}(1,1).
\]

The metric trace of this tangent is zero:

\[
\operatorname{tr}_{\eta}\dot h(0)=-2+2=0.
\]

Embed half this tangent as

\[
Q=\operatorname{diag}(1,1,0,0)
\]

in a four-dimensional Lorentz frame.  Every Lorentz transform gives another exact traceless
symmetric tensor.  The production certificate constructs 133 distinct rational transforms from
exact `5-4-3` boosts, `3-4-5` rotations, and their pairwise products.  The resulting orbit has

\[
\boxed{\operatorname{rank}\operatorname{span}\{\Lambda^TQ\Lambda\}=9.}
\]

Nine is the full dimension of the four-dimensional traceless symmetric tensor space.  A greedy
exact basis occurs at registered orbit indices

```text
0, 1, 3, 4, 5, 6, 7, 9, 38.
```

The uncomposed generators span only rank eight; the compound transform at index 38 supplies the
missing mixed direction.  This is caught by the hostile replay.

### The retained common scale restores ten

The conformal metric direction `eta_ab` is not in that traceless span.  Adding it raises the exact
rank to ten:

\[
\boxed{S^2(V^*)=S^2_0(V^*)\oplus\mathbb R g,\qquad 9+1=10.}
\]

The same separation is visible on every supplied regular pair metric.  For

\[
\widehat h=e^{2\omega}h,
\qquad m=\sqrt{-\det h},
\]

one has

\[
\widehat m=e^{2\omega}m,
\qquad
\frac{\widehat h}{\widehat m}=\frac h m.
\]

Thus determinant-normalized reciprocal shape is blind to the common scale, while the complete pair
metric and its normalization scalar detect it.  This reproduces G154's conformal distinction by a
different finite-dimensional tangent calculation.

### Exact ownership consequence

Dual Reciprocity naturally identifies the nine-dimensional shape sector.  It does **not** erase
the tenth metric direction or require a trace-free curvature residual.  Therefore it does not
select either G301 class.

This statement uses every algebraically available pair plane only as a control family.  G300 leaves
physical query/plane population open.  A smaller populated family could span less, but cannot turn
the retained common metric scale into a derived trace-free field equation.

## 3. Gate B: direct primary-metric derivation

Now conditionally test the exceptional G301 class on the exact primary static spherical metric

\[
ds^2=-f(r)(dx^0)^2+\frac{dr^2}{f(r)}+r^2d\Omega^2,
\qquad x^0=c_Et.
\]

This chart is tested only where `r>0` and `f>0`.  The nonzero mixed Ricci eigenvalues derived from
the metric are

\[
R^t{}_t=R^r{}_r=-\left(\frac{f''}{2}+\frac{f'}r\right),
\qquad
R^\theta{}_\theta=R^\varphi{}_\varphi=
\frac{1-f-rf'}{r^2}.
\]

Consequently `S_ab=0` is exactly

\[
\boxed{r^2f''-2f+2=0.}
\]

The homogeneous indicial polynomial is

\[
(m-2)(m+1)=0.
\]

Therefore the complete twice-differentiable solution on a connected radial interval is

\[
\boxed{f(r)=1+\frac b r-\frac{R_0}{12}r^2.}
\]

No named external solution was imported.  Direct substitution gives

\[
R=R_0,
\qquad
R_{ab}=\frac{R_0}{4}g_{ab}.
\]

This agrees with the contracted-Bianchi consequence of G301: `R0` is constant on each connected
smooth solution region.  Both `b` and `R0` remain free conditional solution data.

## 4. Exact curvature split

The independent full Christoffel/Riemann recomputation gives

\[
R_{ab}R^{ab}=\frac{R_0^2}{4},
\]

\[
R_{abcd}R^{abcd}=\frac{R_0^2}{6}+\frac{12b^2}{r^6},
\]

and

\[
\boxed{C_{abcd}C^{abcd}=\frac{12b^2}{r^6}.}
\]

Equivalently,

\[
R_{abcd}=C_{abcd}+\frac{R_0}{12}
(g_{ac}g_{bd}-g_{ad}g_{bc}).
\]

The data separate cleanly:

- `R0` occupies the Ricci/constant-sectional-curvature channel;
- `b` occupies the Weyl channel in this exact family.

This is a geometric separation, not a matter/source interpretation.

## 5. Reciprocal and angular channels

The primary reciprocal outputs are

\[
\phi(r)=-\frac12\log f(r),
\qquad
\chi(r)=\tanh\phi(r)=\frac{1-f(r)}{1+f(r)}.
\]

They see the complete `f`, hence both `b/r` and `R0 r^2`.

The registered G201/G288 angular channels are

\[
A_\parallel=\frac r2(rf''-f'),
\qquad
A_\perp=\frac12(rf'-2f+2).
\]

Exact substitution yields

\[
\boxed{A_\parallel=\frac{3b}{2r},\qquad
A_\perp=-\frac{3b}{2r}.}
\]

The `R0 r^2` term cancels from both channels.  Therefore this family has a native channel
separation:

- completed reciprocal clock/position readout sees `b` and `R0`;
- the registered null-angular tide sees `b` but not `R0`.

For `b=0`, this is exactly G288's family

\[
f=1+c_2r^2,
\qquad c_2=-\frac{R_0}{12},
\]

with zero registered angular tide and constant sectional curvature.  For `R0=0`, the family lies in
G301's generic Ricci-flat solution class.  These are regression correspondences, not imported laws.

## 6. Null versus non-null response

For the pure scalar-curvature Riemann part with sectional curvature `K=R0/12`, an orthogonal null
screen contraction is

\[
K\big[(e\cdot e)(k\cdot k)-(e\cdot k)^2\big]=0.
\]

Likewise `R_ab k^a k^b=0`.  Thus `R0` supplies neither Ricci focusing nor an isotropic screen tide
for a null carrier.  A unit timelike-spacelike sectional contraction has magnitude `|R0|/12` and is
nonzero when `R0` is nonzero.  Finite pair position and non-null deviation can therefore detect the
scalar datum even when the registered null-angular channels cancel it.

## 7. Static-chart domains and center gate

For `r>0`, `f>0` is equivalent to

\[
P(r)=r+b-\frac{R_0}{12}r^3>0.
\]

All eight exact sign/repeated-root strata are recorded in `DOMAIN_CLASSIFICATION.tsv`.  In summary:

- `R0<0`: `P` is strictly increasing; negative `b` produces one inner root, while nonnegative `b`
  gives a positive static chart for every `r>0`;
- `R0=0`: negative `b` gives the root `r=-b`; nonnegative `b` has no positive root;
- `R0>0`: an outer root always limits the `b>=0` chart; for negative `b`, two positive roots exist
  only when

  \[
  -\frac{4}{3\sqrt{R_0}}<b<0.
  \]

  Equality gives a double root at `2/sqrt(R0)` but no open positive-`f` interval; more negative `b`
  gives none.

Zeros of `f` are boundaries of this static chart.  G302 does not classify their global extension.

An ordinary smooth areal center requires

\[
f=1+O(r^2).
\]

Hence

\[
\boxed{b=0}
\]

is necessary.  For nonzero `b`, the invariant witness `C^2=12b^2/r^6` diverges.  The two-term family
is therefore an exterior relation family when `b` is nonzero; it is not a smooth micro-core or a
derived mass object.

## 8. Conditional scale separation

When both data are nonzero, their magnitudes cross at

\[
r_\times=\left(\frac{12|b|}{|R_0|}\right)^{1/3}.
\]

For an `epsilon`-quiet middle to exist with

\[
\frac{|b|}{r}<\epsilon,
\qquad
\frac{|R_0|r^2}{12}<\epsilon,
\]

the exact separation condition is

\[
\boxed{|b|\sqrt{\frac{|R_0|}{12}}<\epsilon^{3/2}.}
\]

Thus a small-end/quiet-middle/large-end pattern is available for separated solution data, but is
not guaranteed for arbitrary `b,R0` and is not selected by current premises.  `R0` alone grows only
with the large-distance dimensionless combination `|R0|r^2`; it cannot create both loud ends.

## 9. What G302 does and does not establish

G302 derives:

1. reciprocal shape spans the exact nine-dimensional traceless metric tangent;
2. the retained common scale restores the tenth metric direction;
3. completed-pair structure therefore does not select either G301 residual class;
4. conditional on the exceptional class, the primary metric has one exact two-datum family;
5. `R0` and `b` enter distinct reciprocal, Ricci, Weyl, angular, null, and center channels;
6. separated data can produce a native two-end pattern without switching terms by hand.

G302 does not derive or adopt:

- a UDT field equation or physical history;
- a physical observer/query population;
- a value or sign for `b` or `R0`;
- a source, mass, matter sector, action, boundary completion, or `X_max`;
- a nonspherical or time-live continuation;
- an observational prediction or calibration.

The trace-free class remains a serious conditional class because it exposes an exact, testable
channel separation.  It is not privileged by Dual Reciprocity alone.
