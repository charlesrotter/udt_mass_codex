# G339 exact derivation — finite-time pair-carry type classification

Date: 2026-09-03
Grade: `EXTERNALLY_ACCEPTED_DERIVED_CONDITIONAL_BOUNDED`

## Bounded landing

```text
FINITE_TIME_PAIR_COMPONENTS_DEPEND_ON_SUPPLIED_CARRY
__G338_LIE_CARRY_IS_THE_COMOVING_OBSERVER_SEPARATION_QUERY
__PARALLEL_AND_FERMI_LOCAL_RULERS_ARE_QUIET_CONTROLS
__METRIC_DEFORMATION_IS_RECOVERED_FROM_TYPED_PAIR_PLUS_CARRY
__NO_PHYSICAL_CARRY_SELECTED
```

This classifies several exact ways of carrying a pair on one supplied lawful spacetime. It changes
neither the metric, kernel, angular sector, nor provisional field equation, and it does not select
which observer worldlines or local frames are physically populated.

## 1. Fixed metric and normal deformation

Use the G323/G324/G338 spacetime

\[
 g=-dT^2+a_X(T)^2dX^2+a_\perp(T)^2(dy^2+dz^2),
\]

with

\[
 \frac{a_X(T)}{a_X(T_0)}=u^{-1/3},\qquad
 \frac{a_\perp(T)}{a_\perp(T_0)}=u^{2/3},\qquad u=T/T_0>0.
\]

For the supplied geodesic normal congruence `n=partial_T`, define

\[
 H=\frac12\gamma^{-1}{\cal L}_n\gamma.
\]

In the orthonormal principal frame,

\[
 \boxed{H=\frac1{3T}\operatorname{diag}(-1,2,2)}.
\tag{1}
\]

Thus the fixed-normal metric shape has

\[
 \operatorname{tr}H=\frac1T,\quad
 \operatorname{tr}(H^2)=\frac1{T^2},\quad
 \det H=-\frac4{27T^3}.
\tag{2}
\]

The ratios `tr(H^2)/(tr H)^2=1` and `det(H)/(tr H)^3=-4/27` are independent of pair carry.
They characterize this supplied normal slicing; they do not select it or attach an absolute scale.

## 2. The transport identity

For any spatial vector extension `V(T)`, the definition of the Lie derivative gives

\[
 \boxed{
 \frac12 n[g(V,V)]
 =\frac12({\cal L}_n g)(V,V)+g([n,V],V).
 }
\tag{3}
\]

Equivalently, the observed logarithmic length rate is the sum of metric deformation and declared
carry:

\[
 n\log\sqrt{g(V,V)}
 =\frac{g(HV,V)}{g(V,V)}+\frac{g([n,V],V)}{g(V,V)}.
\tag{4}
\]

Equation (3) is the finite-time version of G334's first-jet accounting. It proves that raw component
change is not meaningful without saying how the compared vector is identified at neighboring
events. Conversely, if the carry is supplied, subtracting its bracket term recovers the restriction
of the metric tensor `L_n g`.

## 3. Connecting, parallel, and interpolating carries

Let `J_0` be unit at `T0`, with squared longitudinal fraction `rho`. Define the diagnostic family

\[
 J_\lambda^i(T)=J_0^i\left[\frac{a_i(T_0)}{a_i(T)}\right]^\lambda,
 \qquad 0\le\lambda\le1.
\tag{5}
\]

Direct connection evaluation gives

\[
 [n,J_\lambda]=-\lambda HJ_\lambda,
 \qquad
 \nabla_nJ_\lambda=(1-\lambda)HJ_\lambda.
\tag{6}
\]

- `lambda=0`: `[n,J_0]=0`. It is the connecting field between fixed labels of the supplied normal
  observer congruence. Because `n` is geodesic, it also satisfies the exact Jacobi equation.
- `lambda=1`: `nabla_n J_1=0`. It is a parallel local ruler along one normal observer. It is not the
  connecting field between the same fixed comoving labels.
- intermediate `lambda`: a declared diagnostic homotopy, not a proposed physical field or law.

The exact squared length is

\[
 \boxed{
 G_\lambda(u,\rho)=
 \rho u^{-2(1-\lambda)/3}+(1-\rho)u^{4(1-\lambda)/3}.
 }
\tag{7}
\]

G338 is the endpoint `lambda=0`; parallel carry is `G_1=1` identically.

## 4. Complete pair pullback

Keep the initial finite boost coefficients `c=cosh z`, `s=sinh z` in the carried normal-spatial
pair. For every member of (5), the unchanged complete pullback is

\[
 h_{00}=-c^2+G_\lambda s^2,\qquad
 h_{01}=(G_\lambda-1)sc,
\]

\[
 h_{11}=-s^2+G_\lambda c^2,\qquad
 \boxed{\det h=-G_\lambda}.
\tag{8}
\]

On the declared clock-timelike stratum

\[
 \Delta_\lambda=c^2-G_\lambda s^2>0,
\tag{9}
\]

the G176/W1 outputs are exactly the G338 formulas with `G` replaced by `G_lambda`:

\[
 m=\sqrt{G_\lambda},\quad
 \beta=-\frac{(G_\lambda-1)sc}{\Delta_\lambda},\quad
 \Phi=-\frac12\log\Delta_\lambda,\quad
 \chi=\frac{1-\Delta_\lambda}{1+\Delta_\lambda}.
\tag{10}
\]

For parallel carry, `G_1=Delta_1=1` and the entire boosted pair is `diag(-1,1)` for all `T`.
Accordingly `m=1`, `beta=Phi=chi=0`. This is exact local-ruler quietness, not zero curvature.

For `0<=lambda<1` and nonzero boost, the complete clock-timelike intervals are:

- `rho=1`: `u>tanh(|z|)^[3/(1-lambda)]`;
- `rho=0`: `u<coth(|z|)^[3/(2(1-lambda))]`;
- `0<rho<1`: exactly two clock-null boundaries enclose `u=1`.

At `lambda=1`, the interval is all `u>0`. These boundaries belong to the declared clock vector and
carry; the pair plane itself remains Lorentzian because `det h=-G_lambda<0`.

## 5. Silent-direction classification

At `u=1`,

\[
 \left.\frac{d\sqrt{G_\lambda}}{dT}\right|_{T_0}
 =\frac{(1-\lambda)(2-3\rho)}{3T_0}.
\tag{11}
\]

For every `lambda<1`, the unique initially first-order-silent direction remains `rho=2/3`. Put

\[
 y=u^{2(1-\lambda)/3}>0.
\]

Then

\[
 \boxed{G_\lambda-1=\frac{(y-1)^2(y+2)}{3y}\ge0}.
\tag{12}
\]

For `lambda<1`, equality occurs only at `u=1`, so the direction turns on on both sides. At
`lambda=1`, `y=1` for every `u` and the local ruler remains quiet. The apparent difference is
exactly the distinction between connecting separation and parallel ruler.

## 6. Fermi and rotating local rulers

Because `n` is geodesic, Fermi-Walker transport along a normal observer is identical to parallel
transport. More generally, let a spatial orthonormal carry obey

\[
 \nabla_nV=\Omega V,\qquad \Omega^T=-\Omega.
\tag{13}
\]

Then `[n,V]=Omega V-HV`. Since `g(Omega V,V)=0`, equation (3) gives `n[g(V,V)]=0` even though
`g(HV,V)` need not vanish. Rotation changes orientation and the directional projection of `H`, but
the local ruler's Gram matrix stays normalized.

Thus a continuously orthonormalized frame moves the geometric response into its connection/carry
coefficients. It does not remove the response from the metric.

## 7. Explicit accelerated Fermi controls

Let `e_i` be any principal orthonormal direction with `H e_i=H_i e_i`. For constant finite rapidity,

\[
 U=c n+s e_i,\qquad S=s n+c e_i.
\tag{14}
\]

Direct evaluation gives

\[
 \boxed{\nabla_UU=H_i s S},\qquad
 \boxed{\nabla_US=H_i s U}.
\tag{15}
\]

The first equation is nonzero proper acceleration when `H_i s` is nonzero. The second is exactly
Fermi-Walker transport of `S`; consequently

\[
 g(U,U)=-1,\qquad g(U,S)=0,\qquad g(S,S)=1
\tag{16}
\]

throughout the regular curve. Acceleration is recorded by the connection, not by a changing Gram
matrix of the observer's own orthonormal frame. G339 supplies these three principal-axis controls;
it does not classify all accelerated congruences or select their population.

## 8. What survives arbitrary pair-frame congruence

At one regular event, any Lorentzian `2x2` pair matrix can be transformed by an invertible basis
change `A` as `h -> A^T h A` to `diag(-1,1)`. Hence no nonconstant numerical scalar of the raw pair
components alone is invariant under arbitrary smooth `GL(2)` frame carry; only the inertia class
survives pointwise. In particular, terminal `Phi` and the clock-timelike boundary require the
declared clock/ruler calibration.

This does not make G338 a frame artifact. The complete typed object includes the pair metric and
its carry. Equation (3) removes the carry contribution and recovers the metric deformation tensor.
For the supplied normal congruence its eigenvalues and ratios are (1)--(2), independent of whether
the local components were kept commuting, parallel, Fermi, or rotating.

## 9. Scientific meaning and limits

G338's commuting field is not merely an arbitrary ruler convention: `[n,J]=0` is the connecting
condition for the infinitesimal separation of the selected comoving normal observers. Parallel and
Fermi frames answer a different question—how one observer carries a local ruler. Accelerated
congruences choose different observer worldlines and bring additional acceleration gradients into
their connecting-field evolution.

The metric therefore determines the response once the observer worldlines and their connecting
relation are supplied. It does not, from this calculation alone, populate a preferred congruence.

Production passed `2182/2182` exact and analytic-control checks. A separate direct four-dimensional
implementation imported no production code and read no production result; it passed
`16155/16155` checks across 1,200 deterministic random cases. Twelve hostile mutations were caught.
A fresh sealed external `gpt-5.4` review independently rederived the bounded chain, replayed all
registered checks, and returned `ACCEPT_G339_BOUNDED_CARRY_TYPE_CLASSIFICATION` with no required
mathematical or scientific repair.

The bounded landing is Candidate B. This is not a physical carry, population, occupancy, stability,
matter/mass, scale, `X_max`, or canon result.
