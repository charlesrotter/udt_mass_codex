# G262 exact derivation

Date: 2026-08-25

## 1. Bounded metric and types

On the positive primary static-spherical branch write

\[
ds^2=-f(r)c_E^2dt^2+f(r)^{-1}dr^2+r^2d\Omega^2,
\qquad
f=e^{-2\phi}>0,
\qquad
N=\sqrt f=e^{-\phi}.
\]

Here `N` is the static lapse/clock factor. The calculation keeps four different mass-related
objects separate:

1. a local invariant rest mass of a supplied massive object;
2. an endpoint observer's energy or mass-equivalent readout of a supplied covector;
3. the spherical geometric mass aspect `mu`, which is only a change of metric variables;
4. a normalized total physical UDT mass, which remains open.

No field equation is used below.

## 2. Clock, redshift, and conditional covector energy

For a static worldline,

\[
d\tau=N\,dt.
\]

On an endpoint-exact matched observer/source branch,

\[
\delta_{os}=\phi_s-\phi_o,
\qquad
q_{os}=\frac{d\tau_s}{d\tau_o}
=\frac{N_s}{N_o}
=e^{-\delta_{os}}.
\]

The direct reciprocal redshift is

\[
Z_{so}=1+z=e^{\delta_{os}}=\frac1{q_{os}}.
\]

G95 supplies a distinct conditional theorem. If one physical carried covector is identified with
the affinely transported null-query covector and endpoint energy is read as `E_u=-p(u)`, then

\[
\epsilon_{so}=\frac{E_o}{E_s}=\frac1{Z_{so}}=q_{os}.
\]

The numerical factor is the same, but the arrow types are opposite: `q_os` maps observer clock to
source clock; `epsilon_so` describes energy carried from source to observer. This is not yet a
massive-particle or physical-carrier theorem.

## 3. Acceleration is the first clock derivative

Using `x^0=c_E t`, the nonzero static radial connection term needed here is

\[
\Gamma^r{}_{00}=\frac12 f f'.
\]

The unit static tangent has `u^0=N^{-1}`, so the radial coordinate component of geometric
four-acceleration is

\[
a^r=\frac12f'.
\]

Projecting onto the outward unit radial frame `n=N partial_r` gives

\[
\boxed{a_{\hat r}=\frac{f'}{2\sqrt f}=N'.}
\]

This has inverse-length units in the `x^0` convention. The corresponding dimensional proper
acceleration is `c_E^2 N'`. Thus the static acceleration is not an independent instrument: it is
the first radial derivative of the metric clock factor.

## 4. The metric's spherical mass aspect

Define

\[
\boxed{\mu(r)=\frac r2\left(1-f(r)\right).}
\]

This is algebraically equivalent to

\[
\boxed{f=1-\frac{2\mu}{r}},
\qquad
\boxed{\frac{\mu}{r}=\frac{1-N^2}{2}}.
\]

Therefore, after the areal radius and clock normalization are supplied, the same lapse that gives
time dilation also fixes the dimensionless compactness aspect. No Einstein equation or matter
source is required for this change of variables.

Attaching dimensions through

\[
M_{\rm ref}=\frac{c_E^2}{G_{\rm obs}}\mu
\]

is the existing conditional GR/Misner--Sharp comparison attachment. It is not a native UDT mass
law and does not identify local rest mass, matter substance, or normalized total mass.

## 5. Gravity and the angular orchestra are mass-aspect derivatives

The bounded G257/G259 full-metric residuals are

\[
\mathcal E_0=rf'+f-1,
\qquad
\mathcal E_1=rf'+\frac{r^2}{2}f''.
\]

Direct differentiation of `mu` gives

\[
\boxed{\mathcal E_0=-2\mu',}
\qquad
\boxed{\mathcal E_1=-r\mu''.}
\]

The native G201 angular modes become

\[
A_\parallel
=\frac{r^2f''-rf'}2
=-r\mu''+3\mu'-\frac{3\mu}{r},
\]

\[
A_\perp
=1-f+\frac{rf'}2
=\frac{3\mu}{r}-\mu'.
\]

Consequently,

\[
\boxed{
A_\parallel+A_\perp
=2\mu'-r\mu''
=\mathcal E_1-\mathcal E_0.
}
\]

The complete bounded hierarchy is therefore

\[
N
\longrightarrow
\left\{
\begin{array}{l}
\text{clock/redshift level},\\
N'\text{ static acceleration},\\
\mu=r(1-N^2)/2\text{ geometric mass aspect},\\
\mu',\mu''\text{ curvature and angular response}.
\end{array}
\right.
\]

These are interlocking descriptions of one supplied metric, not independently adjustable
post-processing sectors.

## 6. Exact pair-position asymptotics

For the current working normalized pair coordinate

\[
\chi=\tanh\delta,
\]

the clock and conditional carried-energy factor is

\[
\boxed{
q=e^{-\delta}
=\sqrt{\frac{1-\chi}{1+\chi}}.
}
\]

Hence

\[
\chi\to+1
\quad\Longrightarrow\quad
q\to0,
\qquad q_{\rm reverse}=q^{-1}\to\infty.
\]

At the opposite signed end the roles reverse. The invariant conclusion is reciprocal asymptotic
separation of the pair readouts, not that a local object acquires infinite invariant rest mass.

If the same static primary chart also has `N->0` at finite areal radius, then

\[
\frac\mu r\to\frac12.
\]

Thus the geometric compactness aspect saturates while one directional pair-energy ratio vanishes
and its reverse diverges. These are different mass notions and must not be conflated. No numerical
`X_max`, physical distance profile, boundary, or global completion is derived.

### Pre-existing WR-L boundary-side relation

The sealed asymptotic-boundary audit already derives one nonidentity metric limit on the separately
supplied WR-L representative

\[
f(r)=1-\frac rX,
\qquad 0<r<X.
\]

On a static slice the outward unit radial component is \(n^r=\sqrt f\), the lapse is
\(N=\sqrt f\), and the raw spherical lapse flux is

\[
\Phi_N(r)
=\int_{S_r}n^i\nabla_iN\,dA
=4\pi r^2\sqrt f\,N'
=-\frac{2\pi r^2}{X}.
\]

Therefore

\[
\boxed{\Phi_{\rm wall}=-2\pi X.}
\]

This relation is `DERIVED_METRIC_LIMIT` on that supplied representative. It is not a normalized
physical mass or charge and does not identify \(X\) with global \(X_{\max}\). Such a promotion
would still require a complete action or generator, normalization, reference, orientation, and
boundary prescription. G262 did not newly derive this relation; it retains it so the bounded
mass/Xmax ledger is complete.

## 7. What “mass is a function of time dilation” can force

Let a positive mass-related factor depend only on the clock ratio `q`. If one additionally posits
that it composes on observer chains,

\[
F(q_1q_2)=F(q_1)F(q_2),
\qquad F(1)=1,
\]

and assumes continuity or measurability, then the ordinary character theorem gives

\[
\boxed{F(q)=q^w}
\]

for one dimensionless weight `w`.

The founding pair-depth composition law does not automatically apply to a new physical mass
object. Therefore generic mass composition, the object being transformed, and `w` would be new
premises. The conditional G95 transported-covector energy theorem realizes the `w=1` numerical
factor for its declared endpoint roles; it does not derive a local rest-mass law.

## 8. Nonselection counterfamily

The identities above were derived for arbitrary positive `f`. In particular, both

\[
f_0(r)=1
\]

and

\[
f_a(r)=1+\frac{a r^2}{1+r^2},
\qquad 0<a<1,
\]

are positive and smooth-centered on `r>=0`. The first has zero acceleration, mass aspect, and
curvature residuals. The second has nonzero values. Both satisfy every clock--acceleration--mass-
aspect--angular identity exactly.

Therefore the hierarchy is not a nonidentity history law. It translates any supplied primary
metric into mutually consistent instruments but does not select the numerical function `f(r)` or
`phi(r)`.

## 9. Exact landing

```text
ONE_METRIC_STATE_HIERARCHY_DERIVED
__COVECTOR_ENERGY_PAIRING_CONDITIONAL
__LOCAL_REST_MASS_PHYSICAL_TOTAL_MASS_XMAX_VALUE_AND_HISTORY_LAW_OPEN
```

This narrows the missing bridge: a future physical source/mass statement must connect the
geometric mass aspect or its derivatives to a genuinely owned matter/global response. Merely
renaming `mu`, applying the reciprocal energy factor, promoting the unnormalized wall lapse flux,
or taking the `X_max` limit cannot supply that nonidentity relation.
