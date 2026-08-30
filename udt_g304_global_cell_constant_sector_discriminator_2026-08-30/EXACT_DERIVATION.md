# G304 exact derivation

Date: 2026-08-30

## Landing

`FOUNDED_RELATION_LAYERS_NONSELECTIVE__WORKING_FINITE_CEILING_CONDITIONALLY_SELECTS_POSITIVE_CONSTANT_IN_PRIMARY_STATIC_SMOOTH_CENTER_BRANCH__X_EMERGES__FULL_WRL_ARCHITECTURE_INCOMPATIBLE`

This is a bounded conditional architecture result. It does **not** adopt a UDT field equation,
select a complete physical history, fix a mass or source, use an observation, determine a numerical
scale, identify the derived radius with physical `X_max`, or modify the metric or reciprocal kernel.

## 1. Frozen conditional family

G301 and G303 leave the trace-free candidate class

\[
R_{ab}=\Lambda g_{ab},\qquad d\Lambda=0.
\]

In the G302 primary static diagonal areal-spherical chart,

\[
ds^2=-f(r)c_E^2dt^2+\frac{dr^2}{f(r)}+r^2d\Omega^2,
\]

the trace-free residual is exactly

\[
r^2f''-2f+2=0,
\]

with complete solution family

\[
f(r)=1+\frac br-\frac{R_0}{12}r^2.
\]

A direct Christoffel-to-Ricci computation, rather than a familiar-vacuum import, gives

\[
R_{ab}=\frac{R_0}{4}g_{ab},\qquad R=R_0.
\]

Thus `Lambda=R0/4`. The constants `b` and `R0` remain free solution data at this stage.

## 2. The smooth center removes `b`, not `R0`

The exact curvature invariants are

\[
R_{ab}R^{ab}=\frac{R_0^2}{4},
\]

\[
R_{abcd}R^{abcd}=\frac{R_0^2}{6}+\frac{12b^2}{r^6},
\]

and

\[
C_{abcd}C^{abcd}=\frac{12b^2}{r^6}.
\]

Therefore a smooth areal center at `r=0` forces

\[
b=0.
\]

This is a derived regularity restriction on the explicitly tested centered stratum. It is not a
universal preferred-center premise. The surviving family is

\[
f(r)=1-\frac{R_0}{12}r^2.
\]

## 3. Exact three-sign census

### Positive constant

For `R0>0`, define only after the sign census

\[
X=\sqrt{\frac{12}{R_0}}.
\]

Then

\[
f(r)=1-\frac{r^2}{X^2}.
\]

The static region `0<=r<X` ends at a simple zero:

\[
f(X)=0,\qquad f'(X)=-\frac2X.
\]

The proper radial reach is finite,

\[
\int_0^X\frac{dr}{\sqrt{f}}
=X\left[\arcsin\frac rX\right]_0^X
=\frac{\pi X}{2},
\]

whereas the optical reach is infinite,

\[
\int_0^X\frac{dr}{f}
=X\left[\operatorname{artanh}\frac rX\right]_0^X
=\infty.
\]

All registered invariants are finite at the zero:

\[
R=R_0,
\quad
R_{ab}R^{ab}=\frac{R_0^2}{4},
\quad
R_{abcd}R^{abcd}=\frac{R_0^2}{6},
\quad
C_{abcd}C^{abcd}=0.
\]

With the native reciprocal presentation

\[
\phi=-\frac12\log f,
\qquad
\chi=\tanh\phi=\frac{1-f}{1+f},
\]

the static endpoint has

\[
\phi\to+\infty,
\qquad
\chi\to1.
\]

The bounded static chart therefore develops a finite regular causal-ceiling radius and the already
derived dimensionless projective endpoint. `X` is here an algebraic radius of this conditional
solution. Calling it the physical all-frame `X_max`, or assigning it a value, remains open.

### Zero constant

For `R0=0`,

\[
f=1.
\]

Both proper and optical radial reaches are infinite. There is no finite outer causal ceiling.

### Negative constant

For `R0<0`, write `L=sqrt(-12/R0)` after the sign choice. Then

\[
f(r)=1+\frac{r^2}{L^2}>0
\]

for every finite positive `r`. There is no finite zero. Moreover,

\[
\int_0^\infty\frac{dr}{\sqrt{f}}
=L\,\operatorname{arsinh}(r/L)\big|_0^\infty
=\infty,
\]

while

\[
\int_0^\infty\frac{dr}{f}
=L\,\arctan(r/L)\big|_0^\infty
=\frac{\pi L}{2}.
\]

Although `phi->-infinity` and `chi->-1` at coordinate infinity, this is not G17's finite regular
outer horizon. It is a different completion problem with a finite optical boundary and infinite
proper reach.

## 4. The non-centered controls do not change the sign result

For `r>0`, roots of `f` are roots of

\[
P(r)=r+b-\frac{R_0}{12}r^3.
\]

For `R0>0`, `P` has one positive maximum. Depending on `b`, the chart has one outer root, two roots,
a double root, or no static interval. Whenever a nondegenerate static interval has a finite outer
root, the constant sign is positive. For `R0=0` and `R0<0`, any positive root is an inner boundary
of an exterior interval extending to infinity; neither has a finite outer causal ceiling. The exact
domain census is preserved in `DOMAIN_CLASSIFICATION.tsv`.

The `b!=0` controls are center-singular. They prevent the sign result from being an artifact of
examining only the attractive smooth-centered profile, but they are not promoted to physical mass
or source solutions.

## 5. What selects, and at what grade

Endpoint reversal, triangle closure, and projective composition are identities for arbitrary
vertex potentials:

\[
\delta_{AC}=\delta_{AB}+\delta_{BC},
\qquad
\chi_{AC}=\frac{\chi_{AB}+\chi_{BC}}{1+\chi_{AB}\chi_{BC}}.
\]

They contain no residual in `R0`. The current W5 and W6 rows explicitly leave the metric history
open. G235's rank-complete network is reconstructive, G292's Euler sector does not select a
continuous history, and G294's co-presence existence condition admits a regular metric
nonselection family. Therefore the founded/working relation layers do not select the sign.

G17 is different: it is an active `WORKING` program condition whose sharp registered form is a
finite causal horizon with a region beyond. Inside the exact static smooth-center family above,
that condition accepts only `R0>0`. Hence

\[
\boxed{
\text{G17 conditionally selects the positive sign in this bounded family, but not its magnitude.}
}
\]

This is not yet a derivation of G17 from F1--F4 or W1--W6. It is also not a proof that every
physical observer relation globally realizes this static patch.

## 6. G17 finiteness is not the full WR-L profile

The stronger historical WR-L architecture selects

\[
f_{\mathrm{WRL}}=1-\frac rX
\]

after affine residual recentering and wall-regularity assumptions. Substitution into the G302
trace-free ODE gives

\[
r^2f_{\mathrm{WRL}}''-2f_{\mathrm{WRL}}+2
=\frac{2r}{X}\ne0.
\]

Therefore the full WR-L profile and the G301 trace-free candidate cannot both be exact global laws
on this branch. Their shared finite-proper/infinite-optical regular horizon behavior does not make
their profiles identical. G304 preserves this as an architecture fork rather than averaging or
fitting between them.

## 7. Historical negative scope

The older “de Sitter native-forbidden” calculation asked whether a fixed-sign supplied source in a
particular `phi` equation could generate the quadratic profile. `NEGATIVES_REGISTRY.md` now marks
the relevant physical-field/action/source premises conditions-changed. G301's trace-free residual
does not contain that source equation. Consequently the old negative is neither erased nor
automatically applicable:

- if the old source equation is reimposed, its scoped negative still matters;
- in the present source-free candidate-residual comparison, importing it would change the premise;
- a point-of-use regrade is required before combining the architectures.

## 8. Exact boundary of the result

What is newly narrowed:

- founded relation/network structure alone remains nonselective;
- one already active working global condition distinguishes the sign in one exact primary branch;
- the endpoint radius follows from the surviving constant rather than being inserted into the
  kernel;
- the stronger WR-L profile is exposed as a separate incompatible closure, not hidden scaffolding.

What remains open:

- whether G17 is the correct physical global-completion condition;
- whether the positive static patch has the required all-frame observer-pair realization;
- the magnitude of `R0`, the numerical radius, and their relation to physical `X_max`;
- nonspherical and time-live completion, lawful data, branch/path population, and one realized
  history;
- mass, source, action, matter, radiative transfer, observations, and both loud regimes.
