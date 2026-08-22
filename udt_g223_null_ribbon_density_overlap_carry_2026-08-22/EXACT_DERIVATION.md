# G223 exact derivation — null-ribbon density overlap and calibration carry

Date: 2026-08-22

## Primary bounded result

On one supplied regular affine null ribbon, the metric canonically owns a nondegenerate pairing
between the quotient clock line and the null vertical ruler line. The G222 expression

\[
\vartheta=a[d\lambda]
\]

is the clock-trivialized representation of that pairing, not an unqualified global one-form.
It carries with inverse clock weight on overlaps. Local integration along an interval fiber is
automatic. A canonically shared global scalar across independently calibrated ribbons is not.

## 1. Chart-free metric object

Let

\[
V\subset T\Sigma
\]

be the null vertical line of a regular Lorentzian pair surface and let

\[
Q=T\Sigma/V.
\]

For a class `[X]` in `Q` and `v` in `V`, define

\[
\boxed{\mathcal A([X],v)=-h(X,v).}
\]

This is independent of the lift of `[X]`: replacing `X` by `X+cK` adds `-c h(K,v)=0` because
`V` is one-dimensional and null. Since `h` is Lorentzian and nondegenerate, `mathcal A` is a
nondegenerate line pairing

\[
\boxed{\mathcal A\in Q^*\otimes V^*.}
\]

In an adapted chart `(y_i,lambda_i)`,

\[
J_i=\partial_{y_i},\qquad K_i=\partial_{\lambda_i},\qquad
a_i=-h(J_i,K_i)>0,
\]

and

\[
\boxed{\mathcal A=a_i\,dy_i\otimes[d\lambda_i].}
\]

This mixed pairing is the invariant metric object beneath the local G222 ruler density.

## 2. Exact affine-null overlap law

Let two adapted charts be related by

\[
y_j=f(y_i),
\qquad
\lambda_j=\alpha(y_i)\lambda_i+b(y_i),
\qquad f'>0,\quad\alpha>0.
\]

Put

\[
q=\alpha'\lambda_i+b'.
\]

Direct differentiation gives

\[
\boxed{
K_j=\alpha^{-1}K_i,
\qquad
J_j=(f')^{-1}\left(J_i-\frac q\alpha K_i\right).}
\]

Therefore

\[
\boxed{a_j=\frac{a_i}{f'\alpha}.}
\]

If

\[
h_i=\begin{pmatrix}H_i&-a_i\\-a_i&0\end{pmatrix},
\]

the basis Jacobian from chart `j` to chart `i` is

\[
P_{ij}=
\begin{pmatrix}
(f')^{-1}&0\\
-q/(\alpha f')&\alpha^{-1}
\end{pmatrix},
\]

and exact congruence gives

\[
h_j=P_{ij}^{T}h_iP_{ij}
=
\begin{pmatrix}
\dfrac{H_i+2a_iq/\alpha}{(f')^2}&-\dfrac{a_i}{f'\alpha}\\
-\dfrac{a_i}{f'\alpha}&0
\end{pmatrix}.
\]

In particular,

\[
\det h_j=-a_j^2.
\]

On the vertical cotangent line,

\[
[d\lambda_j]=\alpha[d\lambda_i],
\]

so the clock-trivialized ruler density obeys

\[
\boxed{\vartheta_j=a_j[d\lambda_j]=(f')^{-1}\vartheta_i.}
\]

At the same time,

\[
dy_j=f' dy_i,
\]

and hence

\[
dy_j\otimes\vartheta_j=dy_i\otimes\vartheta_i=\mathcal A.
\]

Thus `vartheta` has exact inverse clock weight. It becomes an ordinary global element of `V*` only
after a compatible clock coframe has been fixed.

## 3. Area form and triple overlaps

With the supplied positive orientations, the metric area form is

\[
\boxed{\epsilon_h=a_i\,dy_i\wedge d\lambda_i.}
\]

Because

\[
dy_j\wedge d\lambda_j=f'\alpha\,dy_i\wedge d\lambda_i,
\]

the coefficient law for `a_j` makes `epsilon_h` invariant.

For successive overlaps with derivative data `(F_1,A_1,Q_1)` and `(F_2,A_2,Q_2)`, the composite
data are

\[
F_{12}=F_1F_2,
\qquad
A_{12}=A_1A_2,
\qquad
Q_{12}=A_2Q_1+F_1Q_2.
\]

The exact matrices obey

\[
P_1P_2=P_{12},
\]

while both the density factor `(FA)^{-1}` and the clock weight `F^{-1}` compose
multiplicatively. The metric pairing therefore descends on the supplied affine-null atlas.

## 4. Local fiber coordinate versus a chosen full one-form

After fixing a clock coframe, the vertical covector `vartheta` asks only for a function whose
vertical derivative agrees with it. Since G222 gives `K(a)=0`, on an interval-fiber chart

\[
\boxed{s_i=a_i(y_i)\lambda_i+s_0(y_i)}
\]

satisfies

\[
\boxed{[ds_i]=a_i[d\lambda_i]=\vartheta_i.}
\]

So a local ruler coordinate along each regular interval fiber always exists. No new field equation
or closedness condition is needed for that bounded statement.

The stronger demand

\[
ds_i=a_i d\lambda_i
\]

in the same chosen horizontal chart sets the horizontal coefficient of `ds_i` to zero. It requires

\[
\partial_{y_i}a_i=0
\]

and a constant `s_0`. This is exactly the G222 condition

\[
d(a_i d\lambda_i)=0.
\]

It is valid, but it applies to one chosen full representative, not to the vertical density class
alone.

## 5. Exact closedness counterexample on the same geometry

Hold the clock chart fixed and start with `a=1` and affine coordinate `lambda_i`. The full
representative

\[
\rho_i=d\lambda_i
\]

is closed. Now make the allowed raywise affine change

\[
\lambda_j=e^{y}\lambda_i.
\]

Then `a_j=e^{-y}` and

\[
\rho_j=a_jd\lambda_j
=d\lambda_i+\lambda_i dy.
\]

The vertical restrictions agree:

\[
[\rho_j]=[\rho_i].
\]

But

\[
d\rho_i=0,
\qquad
d\rho_j=-dy\wedge d\lambda_i\ne0.
\]

The pair metric and invariant mixed pairing have not changed. Hence closedness of the selected full
representative is not an invariant of the metric-owned vertical density.

Equivalently, choosing `lambda_j=a(y)lambda_i` turns the local fiber potential
`s=a(y)lambda_i` into an affine coordinate with exact representative `ds=d lambda_j`. What changes
is the horizontal extension, not the vertical metric pairing.

## 6. Global scalar classification

Fix first a global clock trivialization so that the inverse clock weight has been removed and
`vartheta` is a global vertical covector.

- On each interval fiber it integrates locally.
- If a global source section is supplied, then

  \[
  s(p)=\int_{\text{source}}^{p}\vartheta
  \]

  gives a global scalar on that interval ribbon, unique after choosing the source value.
- On a closed fiber, a necessary condition is zero period. A positive `vartheta` has strictly
  positive period and therefore cannot be the vertical differential of a single-valued real
  scalar.
- For local potentials `s_i`, overlap differences are constant along fibers and form an additive
  Cech cocycle on the base. A global scalar exists exactly when the period conditions hold and this
  mismatch can be removed by base functions. On ordinary smooth paracompact interval bundles this
  additive cocycle is normally removable, but the resulting trivialization is not selected by the
  local metric pairing alone.

Thus mathematical existence on a supplied interval ribbon is much less restrictive than canonical
ownership across a network of independently calibrated ribbons.

## 7. Compatibility with G214

The affine-null overlap preserves the null vertical line and has lower-triangular basis matrix.
G214's calibrated pair-chart overlap preserves its declared clock line and has upper-triangular
basis matrix. Their intersection is the positive diagonal subgroup:

\[
P=\operatorname{diag}((f')^{-1},\alpha^{-1}).
\]

On that common subgroup, G214 gives

\[
m_j=(\det P)m_i=\frac{m_i}{f'\alpha}.
\]

With G222's `m_i=a_i`, this is exactly the G223 coefficient law. There is no conflict. The two
larger triangular groups preserve different supplied line choices, so their shear parameters must
not be silently identified.

## 8. Compatibility with G216 and three observers

For an actual proper-clock incidence map

\[
\tau_B=f(\tau_A),
\qquad
r_{AB}=f'>0,
\]

the same mixed pairing written in the `B` clock coframe has ruler density

\[
\vartheta_B=r_{AB}^{-1}\vartheta_A.
\]

For an actual composite, G216 gives

\[
r_{AC}=r_{BC}r_{AB},
\]

and the inverse ruler weights compose in the opposite order exactly.

This does not identify the vertical bundles of distinct `AB` and `BC` pair surfaces. Such a carry
requires an explicit orientation-preserving vertical gluing map at the shared incidence. If those
maps are supplied and satisfy a cocycle, pullback of `mathcal A` and `vartheta` is functorial. The
clock derivative alone leaves an arbitrary positive vertical scaling untouched, so it cannot
select that gluing.

This retains G214's exact boundary: an actual composite relation carries; three independently
supplied pair surfaces sharing observer names do not acquire a tensor product automatically.

## 9. Landing and ceiling

```text
METRIC_OWNS_NONDEGENERATE_CLOCK_RULER_LINE_PAIRING_ON_SUPPLIED_NULL_RIBBON
__RULER_DENSITY_HAS_EXACT_INVERSE_CLOCK_OVERLAP_WEIGHT
__LOCAL_FIBER_COORDINATE_EXISTS_BUT_GLOBAL_SCALAR_NEEDS_TRIVIALIZATION_AND_CECH_PERIOD_GATES
__G216_CLOCK_COMPOSITION_DOES_NOT_BY_ITSELF_SUPPLY_CROSS_RIBBON_VERTICAL_CARRY
```

The result improves the local ownership statement and corrects the type of the provisional
closedness gate. It does not select a null protocol, identify vertical bundles of distinct pair
surfaces, populate observer events or branches, choose a physical history, or derive `X_max`,
transfer, observations, action, source, matter, bootstrap, mass, or signalling.
