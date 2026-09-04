# G338 exact derivation — finite-time completed-pair readout on an explicit lawful spacetime

Date: 2026-09-03
Grade: `EXTERNALLY_ACCEPTED_DERIVED_CONDITIONAL_BOUNDED`

## Bounded landing

```text
EXPLICIT_LAWFUL_TAUB_DEVELOPMENT_CARRIES_NATIVE_COMPLETED_PAIR_RESPONSE_FOR_FINITE_TIME
__ZERO_BOOST_TERMINAL_BLINDNESS_COEXISTS_WITH_NONTRIVIAL_RULER_DENSITY
__INITIAL_SILENCE_CAN_TURN_ON_EXACTLY
__NO_OCCUPANCY_OR_SCALE_SELECTION
```

This is one exact dynamic-evaluation tile. It does not select the G323/G324 spacetime as the
physical universe, establish stability, evolve the generic G332 data used in G333--G337, or fix an
absolute scale or physical `X_max`.

## 1. Supplied lawful spacetime

Under the owner-adopted provisional G310/G312 vacuum dynamics, G323/G324 derived the exact compact
Taub/Kasner quotient

\[
 g=-dT^2+C_X^2T^{-2/3}dX^2
   +C_\perp^2T^{4/3}(dy^2+dz^2),\qquad T>0.
\tag{1}
\]

Its Kasner exponents are `(-1/3,2/3,2/3)`, whose sum and sum of squares are both one, so `Ric(g)=0`.
The compact quotient and its maximal-development status are inherited from G323/G324; they are not
rederived or strengthened here.

Fix a reference time `T0>0` and write `u=T/T0`. At `T0`, choose a unit spatial direction whose
squared longitudinal fraction is

\[
 \rho\in[0,1].
\]

The transverse plane is rotationally equivalent in (1). Carry the corresponding constant linear
combination of the three commuting spatial translation fields. Its squared length relative to its
unit length at `T0` is

\[
 \boxed{G(u,\rho)=\rho u^{-2/3}+(1-\rho)u^{4/3}}.
\tag{2}
\]

This commuting-field carry is a declared query family. G338 does not claim it is the unique
physical observer carry.

## 2. Complete raw pair pullback

At `T0`, boost the orthonormal clock/ruler pair by any finite rapidity `z`:

\[
 e_0=\cosh z\,\partial_T+\sinh z\,e,
 \qquad
 e_1=\sinh z\,\partial_T+\cosh z\,e.
\tag{3}
\]

Keeping these coefficients while carrying `e` by the declared translation-field rule gives the
complete two-dimensional pullback

\[
 h_{00}=-\cosh^2z+G\sinh^2z,
\]

\[
 h_{01}=(G-1)\sinh z\cosh z,
\]

\[
 h_{11}=-\sinh^2z+G\cosh^2z.
\tag{4}
\]

Direct expansion, using `cosh^2(z)-sinh^2(z)=1`, gives

\[
 \boxed{\det h=-G}.
\tag{5}
\]

The off-diagonal term is part of the completed pair. Deleting it destroys (5) away from the quiet
or unboosted cases.

Define

\[
 \Delta=-h_{00}=\cosh^2z-G\sinh^2z.
\tag{6}
\]

The regular timelike-pair stratum is exactly `Delta>0`. There,

\[
 T_{\rm pair}=\sqrt\Delta,
 \qquad
 L_\sigma=\sqrt{G/\Delta},
 \qquad
 \beta=\frac{h_{01}}{h_{00}}
 =-\frac{(G-1)\sinh z\cosh z}{\Delta}.
\tag{7}
\]

## 3. Native completed-pair normalization

Apply the existing G176/W1 ruler calibration after the full pullback has been formed:

\[
 m=T_{\rm pair}L_\sigma=\sqrt G.
\tag{8}
\]

Then

\[
 L_s=\frac1{\sqrt\Delta},
 \qquad
 \beta_s=\frac\beta{\sqrt G},
 \qquad
 \det h_s=-1.
\tag{9}
\]

The terminal reciprocal and projective readouts are

\[
 \boxed{\Phi=-\frac12\log\Delta},
 \qquad
 \boxed{\chi=\tanh\Phi=\frac{1-\Delta}{1+\Delta}}.
\tag{10}
\]

Thus W1 normalizes the determinant but does not erase the raw evolution: `m=sqrt(G)` and the shift
remain separate completed-pair channels. The conditional ratio `c_eff/c_E=Delta` is an
inter-observer readout in this query; it is not promoted to a local signal speed.

## 4. Exact zero-boost blindness

For `z=0`, equations (4)--(10) reduce to

\[
 h=\operatorname{diag}(-1,G),\qquad
 \Phi=\chi=\beta=0,\qquad m=\sqrt G.
\tag{11}
\]

Therefore the terminal scalar alone does not faithfully encode the full pair history. It can remain
quiet while the ruler-density channel changes. This is not a failure of the completed kernel; it is
why its non-scalar channels must be retained.

## 5. Initial jets and an exactly silent direction

At `u=1`, every direction has `G=1`, and

\[
 G_u(1)=\frac{4-6\rho}{3},
 \qquad
 G_{uu}(1)=\frac{4+6\rho}{9}.
\tag{12}
\]

For the carried spatial length `sqrt(G)`, with physical derivative `d/dT=T0^{-1}d/du`,

\[
 \left.\frac{d\sqrt G}{dT}\right|_{T_0}
 =\frac{2-3\rho}{3T_0}.
\tag{13}
\]

The unique first-order silent direction is

\[
 \boxed{\rho=\frac23}.
\tag{14}
\]

It is not silent at the next order:

\[
 \left.\frac{d^2\sqrt G}{dT^2}\right|_{T_0,\rho=2/3}
 =\frac4{9T_0^2}>0.
\tag{15}
\]

More strongly, set `y=u^(2/3)>0`. Then for `rho=2/3`,

\[
 \boxed{G-1=\frac{(y-1)^2(y+2)}{3y}\ge0},
\tag{16}
\]

with equality only at `u=1`. Hence an initially first-order-silent pair direction turns on exactly
on both finite-time sides. This is not an inference from a truncated Taylor series.

## 6. Entire regular interval

For `z=0`, the carried pair is regular for every `u>0`. For nonzero finite `z`, regularity is

\[
 G(u,\rho)<\coth^2 z.
\tag{17}
\]

The complete classification is:

- `rho=1`: the interval is `u>tanh^3|z|`; the pair boundary lies to the past.
- `rho=0`: the interval is `0<u<coth^(3/2)|z|`; the pair boundary lies to the future.
- `0<rho<1`: `G` diverges at both ends and has one minimum at
  `u_*=sqrt(rho/[2(1-rho)])`. Since `G(1,rho)=1<coth^2(z)`, exactly two pair boundaries enclose
  `u=1`.

At `Delta=0`, the carried clock vector becomes null. This is a boundary of this declared pair germ,
not automatically a horizon, singularity, or boundary of spacetime. Indeed each such boundary is
at positive finite `T`, where the ambient Kretschmann scalar `64/(27T^4)` is finite.

On the regular stratum and for nonzero `z`, `Delta=1-(G-1)sinh^2(z)`, so the sign of `Phi` is the
sign of `G-1`. Both signs occur in the admitted directional family; pair reversal is not being
confused with negative physical distance.

## 7. What was learned

The preregistered Candidate A survives:

```text
EXPLICIT_LAWFUL_TAUB_DEVELOPMENT_CARRIES_NATIVE_COMPLETED_PAIR_RESPONSE_FOR_FINITE_TIME
__ZERO_BOOST_TERMINAL_BLINDNESS_COEXISTS_WITH_NONTRIVIAL_RULER_DENSITY
__INITIAL_SILENCE_CAN_TURN_ON_EXACTLY
__NO_OCCUPANCY_OR_SCALE_SELECTION
```

Production passed `169/169` exact checks. A separate implementation that imports neither the
production module nor its output passed `16/16` reconstruction checks across 500 deterministic
random cases. Nine hostile mutations were caught. A fresh sealed `gpt-5.4` review independently
rederived the bounded chain and returned `ACCEPT_G338_BOUNDED_FINITE_TIME_PAIR_READOUT` with no
required scientific repair.

This establishes that, on one already lawful exact spacetime and one declared complete pair-carry
family, the native kernel has a coherent finite-time response. It does not answer which lawful
spacetime, pair population, topology, or scale Nature occupies.
