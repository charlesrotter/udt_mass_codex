# G345 exact derivation — observer-calibrated endpoint screen scalar

Date: 2026-09-04
Status: `EXTERNALLY_ACCEPTED_DERIVED_CONDITIONAL_BOUNDED`

## 1. Inputs and exact type problem

On one supplied G340--G344 labelled null ray, let

\[
 \omega_i=-g(k,n_i)>0
\tag{1}
\]

be the ray frequency measured by the supplied normal observer at endpoint `i`. Let `q_i` be the
positive metric induced on that endpoint's quotient screen. G344 gives

\[
 K_{10}=B_{10}^{-T},\qquad \Delta_{10}=|\det K_{10}|.
\tag{2}
\]

Here `K_10` is a bilinear covector on the two endpoint screens. Its determinant is a screen
bidensity. Under one common affine rescaling `k -> a k`,

\[
 \omega_i\mapsto a\omega_i,\qquad K_{10}\mapsto aK_{10},
 \qquad\Delta_{10}\mapsto a^2\Delta_{10}.
\tag{3}
\]

Thus neither `K` nor `Delta` alone is independent of the arbitrary affine unit.

## 2. Endpoint clocks remove the affine weight

Define the observer-normalized mixed tensor

\[
 \boxed{\widehat K_{10}={K_{10}\over\sqrt{\omega_1\omega_0}}.}
\tag{4}
\]

Both numerator and denominator acquire the same factor `a` in (3), so `Khat` is common-affine
invariant. Taking its two-dimensional determinant gives, in orthonormal endpoint screens,

\[
 \boxed{\widehat\Delta_{10}
 =|\det\widehat K_{10}|
 ={\Delta_{10}\over\omega_1\omega_0}.}
\tag{5}
\]

This product, rather than a frequency ratio, is forced by the bidensity's affine weight two.

There is also a limited uniqueness result. In the frozen first-power monomial class

\[
 \Delta\,\omega_0^a\omega_1^b,
\tag{6}
\]

affine invariance requires `2+a+b=0`, while endpoint-reversal symmetry requires `a=b`. Hence

\[
 \boxed{a=b=-1.}
\tag{7}
\]

This does **not** select a unique physical observable. Arbitrary functions of `Deltahat`, other
metric invariants, different determinant powers, and operational attachments lie outside the
classified monomial class.

## 3. Metric screen areas make the determinant a coordinate scalar

Let endpoint screen components change passively by arbitrary invertible matrices

\[
 x_i'=R_i x_i,\qquad p_i'=R_i^{-T}p_i.
\tag{8}
\]

The canonical endpoint blocks and screen metrics transform as

\[
 B_{10}'=R_1B_{10}R_0^T,\qquad
 K_{10}'=R_1^{-T}K_{10}R_0^{-1},
\tag{9}
\]

\[
 q_i'=R_i^{-T}q_iR_i^{-1}.
\tag{10}
\]

Therefore the intrinsic, orientation-free scalar is

\[
 \boxed{
 \widehat\Delta_{10}=
 { |\det K_{10}| 
  \over
  \omega_1\omega_0\sqrt{\det q_1\det q_0}}.}
\tag{11}
\]

Indeed, both `abs(det K)` and the product of metric screen-area coefficients acquire
`1/abs(det R_1 det R_0)`. Their ratio is unchanged. Equation (11) reduces to (5) in orthonormal
screens. The oriented determinant retains the expected endpoint orientation sign; the absolute
scalar does not.

The metric screen forms are not an imported detector measure. They are the local area structures
already induced by the supplied spacetime metric on the G341/G342 quotient screens.

## 4. Reversal and independent endpoint frequency conventions

In one common affine gauge G343/G344 gives

\[
 B_{01}=-B_{10}^T,
 \qquad
 \boxed{\widehat K_{01}=-\widehat K_{10}^T},
 \qquad
 \boxed{\widehat\Delta_{01}=\widehat\Delta_{10}}.
\tag{12}
\]

This is scalar reversal symmetry, not equality of the oriented mixed tensor.

Now normalize the forward ray to unit normal-observer frequency at endpoint zero. Put

\[
 \alpha_{01}={\omega_1\over\omega_0},\qquad \omega_0=1.
\tag{13}
\]

G343's exact separately normalized reverse block is

\[
 B_{01}^{[1]}=-\alpha_{01}\,[B_{10}^{[0]}]^T.
\tag{14}
\]

Consequently

\[
 \Delta_{01}^{[1]}={\Delta_{10}^{[0]}\over\alpha_{01}^2},
\tag{15}
\]

while the reverse-gauge endpoint frequency product is `1/alpha_01`. Thus

\[
 \boxed{
 \widehat\Delta_{10}^{[0]}={\Delta_{10}^{[0]}\over\alpha_{01}}
 ={\Delta_{01}^{[1]}\over1/\alpha_{01}}
 =\widehat\Delta_{01}^{[1]}.}
\tag{16}
\]

The apparent mismatch between separately source-normalized maps was exactly their missing clock
weight; no new transfer law was needed.

## 5. Typed stationary composition

For three endpoints on the same labelled ray in one common affine gauge, G344 gives

\[
 H_1=B_{21}^{-1}B_{20}B_{10}^{-1},\qquad
 \Delta_{20}={\Delta_{21}\Delta_{10}\over|\det H_1|}.
\tag{17}
\]

`H_1` is a covariant Hessian on the joined screen. Its normalized scalar determinant is

\[
 \boxed{
 \widehat h_1={|\det(H_1/\omega_1)|\over\det q_1}
 ={|\det H_1|\over\omega_1^2\det q_1}.}
\tag{18}
\]

Substitution into (11) proves

\[
 \boxed{
 \widehat\Delta_{20}=
 {\widehat\Delta_{21}\widehat\Delta_{10}\over\widehat h_1}.}
\tag{19}
\]

This held for all six endpoint orderings. Bare multiplication is false in general because the
stationary intermediate screen must still be eliminated. If different segments are separately
unit-normalized, G343's clock-ratio conversion must first place them in one typed common-ray chart.
At `T_2=T_0`, the total map is the identity and the type-I chart and `H_1` are singular, exactly as
in G344.

## 6. Reference-free mixed-direction formula

Use G343's invariant projective direction `lambda` and define

\[
 h(T)=\sqrt{T^2+\lambda^2},
\tag{20}
\]

\[
 J_\parallel=\int_{T_0}^{T_1}
 {u^{4/3}\over(u^2+\lambda^2)^{3/2}}\,du,
 \qquad
 J_Z=\int_{T_0}^{T_1}
 {u^{-2/3}\over\sqrt{u^2+\lambda^2}}\,du.
\tag{21}
\]

Writing the common affine normalization as `gamma>0`, the two G343 position blocks and endpoint
frequencies become

\[
 B_\parallel={h_1h_0(T_1T_0)^{-1/3}J_\parallel\over\gamma},
 \qquad
 B_Z={(T_1T_0)^{2/3}J_Z\over\gamma},
\tag{22}
\]

\[
 \omega_i=\gamma T_i^{-2/3}h_i.
\tag{23}
\]

Both the marked event and `gamma` cancel from (5):

\[
 \boxed{
 \widehat\Delta_{10}=
 {(T_0T_1)^{1/3}
  \over
  (T_0^2+\lambda^2)(T_1^2+\lambda^2)
  |J_\parallel J_Z|}.}
\tag{24}
\]

The integrands are positive on `T>0`; for reversed endpoints both integrals change sign together.
Thus (24) is positive and regular for every noncoincident positive endpoint pair and finite
projective direction.

## 7. Principal directions and coincidence

For `lambda=0`, both integrals reduce to the same power integral and

\[
 \boxed{
 \widehat\Delta_X={4\over
  9(T_0T_1)^{1/3}(T_1^{2/3}-T_0^{2/3})^2}.}
\tag{25}
\]

For the transverse projective limit `lambda -> infinity`, all powers of `lambda` cancel and

\[
 \boxed{
 \widehat\Delta_\perp=
 {7(T_0T_1)^{1/3}\over
  9\left|(T_1^{7/3}-T_0^{7/3})(T_1^{1/3}-T_0^{1/3})\right|}.}
\tag{26}
\]

Both are finite and positive away from coincidence. For `epsilon=T_1-T_0 -> 0`, (21) gives

\[
 J_\parallel J_Z=
 {T_0^{2/3}\over h(T_0)^4}\epsilon^2(1+O(\epsilon)),
\tag{27}
\]

and hence

\[
 \boxed{\widehat\Delta_{10}=|T_1-T_0|^{-2}(1+O(T_1-T_0)).}
\tag{28}
\]

The pole remains the ordinary identity boundary of the endpoint generating chart; clock
normalization does not erase it.

## 8. Compact labels and exact remaining dependence

Every supplied compact lift `L` retains its own

\[
 \widehat K_L,\qquad\widehat\Delta_L.
\tag{29}
\]

No sum, interference rule, weighting, preferred lift, or physical route follows. The scalar still
depends on the supplied spacetime, normal-observer congruence, two endpoints, projective ray
direction, and path label. It is invariant under affine, marked-event, and screen-coordinate
bookkeeping; it is not independent of physical observer or ray choice.

## 9. Evidence and ownership

The repaired production route passed `9824/9824` checks. The preserved execution note records the
first `9822/9824` result: two supplemental strict numerical convergence-order checks compared
values already at the `1e-11` quadrature floor. Replacing only that over-strong diagnostic with the
recorded two-scale consistency check changed no candidate formula or scientific gate. Production
maxima were `6.951093173576455e-14` or smaller; the reference-covariance maximum was
`4.7375971271501307e-14`.

An implementation-distinct verifier rebuilt the scalar fundamental bases in the reference-free
`(lambda,gamma)` variables, used direct-`T` composite Simpson integration, and independently
reconstructed the screen metrics and stationary sewing. It imported neither production nor
G343/G344 code and passed `4360/4360`; its largest error was the independently integrated block
composition error `3.2360683022147896e-09`. Seventeen hostile mutations were all caught.

This is a metric-native geometric scalar **conditional on** the supplied exact spacetime, supplied
normal observers, supplied fixed labelled ray, and provisional adopted vacuum premises underlying
that arena. “Scalar” here means invariant under the declared affine/reference/screen-coordinate
bookkeeping. It does not mean dimensionless, universally observer-independent, or physically
selected.

No luminosity, flux, probability, amplitude, observational distance, emission, detection,
electromagnetic transfer, path population, matter/mass, physical scale, `X_max`, or canon follows.
Fresh external `gpt-5.4` review authenticated all 29 sealed payloads, reproduced the registered
`17/17` aggregate and all three underlying replays, independently reconstructed the load-bearing
formulas, and accepted the bounded result. Its three non-blocking caveats concern documentary or
tautological verifier assertions and text-token integrity guards; none is mathematical evidence,
and none changes the scientific landing.
