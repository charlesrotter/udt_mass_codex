# G146 exact derivation — multidirectional relational-position composition

Date: 2026-08-17

## 1. Active input and exact scope

G137 provisionally owns, on every regular oriented reciprocal ray,

\[
\xi=\frac{x}{X_{\max}}=\tanh\phi,
\qquad
\xi\oplus\eta=\frac{\xi+\eta}{1+\xi\eta}.
\]

G139 keeps residual angular transport in a different, path-labelled channel. The present question
is whether the scalar law already determines its own non-collinear extension on a supplied positive
three-screen.

The positive three-space and its Euclidean inner product are conditional input, additional to the
no-privileged-center requirement. The July directional audit already proved that centerlessness is
compatible with angular anisotropy, so centerlessness does not supply this isotropic control.

## 2. General rotation-covariant form is function-valued

For non-collinear vectors `u,v` in an oriented three-dimensional inner-product space, every
`SO(3)`-equivariant vector-valued algebraic function has the local form

\[
F(u,v)=A(a,b,c)u+B(a,b,c)v+C(a,b,c)(u\times v),
\]

where

\[
a=\|u\|^2,\qquad b=\|v\|^2,\qquad c=u\cdot v.
\]

This follows because `u,v,u cross v` form an equivariant basis on the regular non-collinear
stratum, while the coefficients must be rotation scalars. If reflection covariance is additionally
required, the cross-product term is excluded unless its coefficient is a pseudoscalar. The
one-dimensional G137 law constrains only the degenerate collinear locus `c^2=ab`. It cannot, by
itself, determine the coefficient functions away from that locus.

The next sections give two explicit global counterexamples even in the parity-even subclass
`C=0`.

## 3. Two smooth open-ball extensions

Let `B^3={u: |u|<1}`. Define the two registered controls

\[
u\oplus_M v=
\frac{(1+2u\cdot v+\|v\|^2)u+(1-\|u\|^2)v}
     {1+2u\cdot v+\|u\|^2\|v\|^2}
\]

and

\[
u\oplus_E v=
\frac{u+\gamma_u^{-1}v+
      \frac{\gamma_u}{1+\gamma_u}(u\cdot v)u}
     {1+u\cdot v},
\qquad
\gamma_u=(1-\|u\|^2)^{-1/2}.
\]

They are algebraic controls, not proposed UDT laws.

Both denominators are positive throughout the open ball. Writing
`a=|u|^2`, `b=|v|^2`, and `c=u dot v`, Cauchy--Schwarz gives

\[
1+2c+ab\geq(1-\sqrt{ab})^2>0,
\qquad
1+c\geq1-\sqrt{ab}>0.
\]

Direct algebra gives the exact closure identities

\[
1-\|u\oplus_Mv\|^2
=\frac{(1-a)(1-b)}{1+2c+ab}>0,
\]

\[
1-\|u\oplus_Ev\|^2
=\frac{(1-a)(1-b)}{(1+c)^2}>0.
\]

Both operations are therefore smooth maps `B^3 times B^3 -> B^3`. Their formulas use only vectors,
inner products, and scalar functions, so both are `SO(3)`-covariant. Both have zero identity and
two-sided **element inverse** `-u`.

For collinear signed inputs `u=a n`, `v=b n`, both reduce exactly to

\[
(a n)\oplus(b n)=\frac{a+b}{1+ab}n,
\]

which is the G137 composition law.

## 4. Exact non-collinear separation

On the preregistered witness

\[
u=(1/2,0,0),\qquad v=(0,1/3,0),
\]

the two results are

\[
u\oplus_Mv=(20/37,9/37,0),
\qquad
\|u\oplus_Mv\|^2=13/37,
\]

and

\[
u\oplus_Ev=(1/2,\sqrt3/6,0),
\qquad
\|u\oplus_Ev\|^2=1/3.
\]

They are unequal and both remain inside the ball. Thus the one-dimensional law, inverse, closure,
and rotational covariance do not uniquely determine non-collinear observer-position composition.

This is a theorem about the position projection, not a complete observer-arrow groupoid. On the
same witness both controls fail the stronger reverse-order identity

\[
-(u\oplus v)=(-v)\oplus(-u).
\]

Thus element inverse `-u` is not enough to implement reversal of a composed non-collinear physical
arrow. An additional rotation/frame state or a different full lift is required before groupoid
reversal can be tested.

For the registered third vector `w=(0,0,1/4)`, both controls happen to associate exactly. That one
triple is parallel to `u cross v`, the natural rotation axis, so it is an axis-blind associativity
control. It supplies no general associativity ruling and was retained rather than replaced after
inspection. The position-projection nonuniqueness conclusion does not depend on associativity.

## 5. Angular companion in the boost control

For a ball vector `u`, the standard symmetric boost-control matrix is

\[
B(u)=
\begin{pmatrix}
\gamma_u&-\gamma_u u^T\\
-\gamma_u u&I+\frac{\gamma_u-1}{\|u\|^2}uu^T
\end{pmatrix}.
\]

Each registered `B(u)` is symmetric. For the non-collinear `u,v` above, exact multiplication gives

\[
B(v)B(u)\ne[B(v)B(u)]^T.
\]

The antisymmetric part contains, among other entries, `sqrt(6)/12`. Consequently the product is not
a pure symmetric boost control. In the standard boost/rotation factorization it contains an
additional rotation factor.

This is only an algebraic demonstration of the familiar `3+3` translation/rotation architecture.
It does **not** prove that UDT reciprocal depth is Lorentz rapidity, that the Einstein control is the
physical composition law, or that this algebraic rotation equals UDT screen transport.

## 6. The sharpened metric-native joint

G139 already owns a conditional typed pair

\[
J(\gamma)=(\xi_{AB},U_\gamma),
\]

where endpoint position and path-labelled angular transport compose in their separate homes. G142
likewise shows that a supplied physical carry belongs inside the total calibrated comparison.

G146 therefore changes the next question. It is not “which scalar profile should be selected?” The
three-dimensional position ball and G139's path screen are not yet the same carrier: the latter can
be the rank-two angular screen of a pair relation. A future test must first derive, from one complete
metric and one typed composed query, a solder

\[
\sigma_{AB}:T_{\xi_{AB}}S^2_{|\xi|}\longrightarrow H_{AB},
\]

or its correct complete-coframe analogue. Only then can it ask whether the multidirectional
position lift's angular defect is the metric-owned transport. Schematically, the comparison would
have the conjugated form

\[
\sigma\,\operatorname{gyr}_{\rm pos}(u,v)\,\sigma^{-1}
\stackrel{?}{=}
U_{\rm metric}(\gamma_u,\gamma_v)
\]

on one common rank-two carrier and one fully specified composed observer query. The exact endpoint
indices, path order, and screen homes depend on that query. No current source owns `sigma` or this
equality.

## Maximum conclusion

The active scalar position law does not uniquely determine the non-collinear **position
projection**, even after adding a supplied isotropic positive three-space and rotational covariance.
Two explicit smooth parity-even open-ball extensions survive and differ exactly. They do not yet
define complete observer arrows: reverse-order composition already exposes missing frame carry. A
non-collinear boost control shows how an angular factor can accompany position composition, but the
rank-two carrier solder and identification with metric path transport remain `OPEN`.

This is not a history law, proper-distance join, global topology, physical Lorentz solder, or
selection of either registered control.
