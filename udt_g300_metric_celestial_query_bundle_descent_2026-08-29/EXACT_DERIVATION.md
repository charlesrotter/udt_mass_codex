# G300 exact derivation — exact celestial control geometry without lawful query-family ownership

Date: 2026-08-29

## Landing

```text
NO_PROPER_LAWFUL_RANK_TWO_QUERY_FAMILY_IS_DERIVED
__THE_QUERY_DOMAIN_REMAINS_WHOLLY_OPERATIONAL
```

Status after fresh external review and registered repair:
`EXTERNALLY_REFUTED_AND_REPAIRED_WITH_CAVEATS`.

The original internal landing 1 was refuted on premise ownership. The exact algebra below derives
the full-relation action on an algebraically available celestial control fiber together with its
positive clock cocycle. It does **not** derive that every direction is a lawful physical UDT query.
Bare pair planes and W1 scalars do not compose by themselves; G274's full path-labelled frame
morphism remains the composition owner.

## 1. The metric canonically supplies the celestial control fiber

Let `(V,g)` be a time-oriented Lorentzian four-space and let `U` be a metric-unit future clock.
Its oriented celestial direction fiber is

\[
\mathbb S_U
=\{n\in V:g(U,n)=0,\ g(n,n)=1\}.
\]

The rest space `U^perp` is positive definite and three-dimensional, so `S_U` is intrinsically a
two-sphere. It is defined without a chart, screen basis, radial axis, scale, or selected direction.

Let `Gr^U_2(V)` be the Lorentzian two-planes containing the clock line `R U`. Given an oriented
plane, its positive ruler orientation selects one unit vector `n in S_U`, and

\[
n\longmapsto \operatorname{span}(U,n)
\]

is a bijection from `S_U` to the oriented clock-containing plane family. Indeed, for any vector
`v` spanning such a plane with `U`,

\[
s=v+g(v,U)U
\]

is nonzero, lies in `U^perp`, and has positive norm. Normalizing `s` gives the unique oriented
representative. If ruler orientation is forgotten, `n` and `-n` define the same plane, so

\[
\boxed{\operatorname{Gr}^U_2(V)_{\rm unoriented}\cong\mathbb{RP}^2.}
\]

Thus the metric and clock derive the complete local clock-containing plane **control family**. This
is a geometric classification, not a premise-owned physical query domain, and it does not choose a
member.

## 2. A full relation transports the entire fiber

Let

\[
P_\gamma:T_XM\longrightarrow T_YM
\]

be the metric isometry carried by one supplied regular path-labelled relation, with unit future
clocks `U_X,U_Y`. For every `n in S_{U_X}`, define the future-null vector

\[
K_X(n)=U_X+n
\]

and

\[
\Omega_\gamma(n)
=-g_Y(P_\gamma K_X(n),U_Y).
\]

Because a proper time-oriented metric isometry sends future-null vectors to future-null vectors,
`Omega_gamma(n)>0`. Set

\[
\mathcal A_\gamma(n)
=\frac{P_\gamma K_X(n)}{\Omega_\gamma(n)}-U_Y,
\qquad
r_\gamma(n)=\Omega_\gamma(n)^{-1}.
\]

The normalized transported vector is null:

\[
0=g_Y(U_Y+\mathcal A_\gamma,U_Y+\mathcal A_\gamma).
\]

Its normalization gives

\[
g_Y(U_Y,\mathcal A_\gamma)=0,
\qquad
g_Y(\mathcal A_\gamma,\mathcal A_\gamma)=1.
\]

Therefore

\[
\boxed{\mathcal A_\gamma:\mathbb S_{U_X}\to\mathbb S_{U_Y}}
\]

is an exact all-direction celestial map of the supplied complete relation. It acts on every
algebraically available null direction; no new carrier or propagation law has been inserted. For a
non-route direction, however, this alone supplies only a possible evaluator input, not a lawful
physical query germ.

## 3. Reversal and concatenation are exact

For mathematical reversal, use `P_{gamma^{-1}}=P_gamma^{-1}`. If

\[
P_\gamma(U_X+n)=\Omega_\gamma(n)(U_Y+n_Y),
\]

then

\[
P_\gamma^{-1}(U_Y+n_Y)=\Omega_\gamma(n)^{-1}(U_X+n).
\]

Hence

\[
\boxed{\mathcal A_{\gamma^{-1}}=\mathcal A_\gamma^{-1}},
\qquad
\boxed{r_{\gamma^{-1}}(n_Y)=r_\gamma(n)^{-1}}.
\]

This is inverse transport of the same relation, not a later physical return leg.

For composable full relations `P_AC=P_BC P_AB`, write

\[
P_{AB}(U_A+n)=\Omega_{AB}(n)(U_B+n_B)
\]

and

\[
P_{BC}(U_B+n_B)=\Omega_{BC}(n_B)(U_C+n_C).
\]

Then

\[
P_{AC}(U_A+n)
=\Omega_{AB}(n)\Omega_{BC}(n_B)(U_C+n_C).
\]

Therefore

\[
\boxed{\mathcal A_{AC}=\mathcal A_{BC}\circ\mathcal A_{AB}},
\]

\[
\boxed{\Omega_{AC}(n)=\Omega_{AB}(n)\Omega_{BC}(\mathcal A_{AB}n)},
\]

and

\[
\boxed{r_{AC}(n)=r_{AB}(n)r_{BC}(\mathcal A_{AB}n)}.
\]

This is the precise algebraic structure: celestial control fibers are acted on by the supplied full
relation groupoid, and `r` is a positive multiplicative cocycle over that action. The full
morphisms still compose; neither the plane nor `r` alone replaces them. Calling the arbitrary
direction-indexed pair germs a premise-owned composable functor would exceed the active premises.

## 4. Every supplied direction gives a regular evaluator input

For each supplied direction `n`, define at the target

\[
J_{\gamma,n}
=\bigl(r_\gamma(n)U_Y,\ \mathcal A_\gamma(n)\bigr).
\]

Its complete pullback is

\[
\boxed{
h_{\gamma,n}=J_{\gamma,n}^{T}g_YJ_{\gamma,n}
=\begin{pmatrix}-r_\gamma(n)^2&0\\0&1\end{pmatrix}.
}
\]

It is regular and Lorentzian for every direction. Algebraically applying the W1 readout to this
supplied input gives

\[
\boxed{\Phi_{\gamma,n}=-\log r_\gamma(n)}.
\]

This calculation demonstrates evaluator compatibility. It does not establish lawful query-family
ownership for arbitrary non-route directions. For the actual G298 null-leg direction

\[
n_X=k_X/\omega_X-U_X,
\]

one has `Omega=omega_Y/omega_X`, so `r=omega_X/omega_Y` and

\[
\mathcal A_\gamma(n_X)=n_Y.
\]

Thus the target-local G298 germ `J_L` occurs exactly as the actual supplied-leg member. G220's clock
arrow and W1 depth are recovered there without using depth as an input.

## 5. The transported-source plane is not discarded

G298 also supplies the transported-source ruler `n_tilde_X=P_gamma n_X`. Let

\[
a=g_Y(U_Y,\widetilde n_X),
\qquad
s_T=\widetilde n_X+aU_Y.
\]

Then

\[
g_Y(U_Y,s_T)=0,
\qquad
g_Y(s_T,s_T)=1+a^2>0,
\]

and

\[
\operatorname{span}(U_Y,\widetilde n_X)
=\operatorname{span}(U_Y,s_T).
\]

Therefore the G298 transported-source plane is contained in the complete clock-containing plane
control family after lawful pair-domain orthogonalization and ruler normalization. Because
`A_gamma` is bijective, its normalized direction has one inverse source-sky query. G300 does not
identify that query with the actual route tangent or assert that its direction-dependent clock
weight equals the actual-leg weight. It proves inclusion of the plane class, exactly as
preregistered. `J_T` and `J_L` remain distinct when screen carry is active.

## 6. Naturality controls the geometry but cannot choose a section

The construction uses only contractions, metric normalization, and the full isometry. It is
covariant under diffeomorphisms and endpoint Lorentz-frame changes. Positive rescaling of an
affine null representative cancels between its frequency and normalization. Pair-domain shift and
positive ruler rescaling change a representative, not its plane class.

There is also an exact obstruction to a unique metric-plus-clock section. Consider the identity
relation with equal clocks. Every simultaneous spatial rotation `R in SO(3)` is a gauge
automorphism of that relation. A natural selected unit direction `n_*` would have to obey

\[
Rn_*=n_*
\quad\text{for every }R\in SO(3).
\]

The only spatial vector fixed by all rotations is zero, which is not on the unit sphere. Hence

\[
\boxed{\text{metric naturality cannot select one global query section.}}
\]

A supplied route tangent or operational question may select a member on a narrower domain. That is
query data, not a universal selector derived by naturality. The obstruction only rules out a
universal metric-plus-clock section; it does not rule out route-conditioned sections.

## 7. Exact repaired ownership statement

Within the preregistered regular local regime:

1. the metric and each unit observer clock derive the full oriented `S^2` celestial control fiber;
2. forgetting ruler orientation gives the `RP^2` plane quotient;
3. the complete path-labelled metric morphism acts bijectively and compositionally on the fibers;
4. its frequency factor is a positive multiplicative cocycle;
5. each supplied direction yields a regular rank-two evaluator input, but lawful query-family
   ownership is not derived;
6. the actual target-local G298 germ and the transported-source G298 plane class are retained;
7. no universal gauge-natural individual direction is selected;
8. lawful query-family ownership, route-conditioned sections, route and query population, singular
   strata, higher surface/Jacobi data, metric history,
   dynamics, scale, observations, matter, source, action, and `X_max` remain open.

This does not close G299's lawful query-family/subfunctor gap. It sharply characterizes the
metric-defined control arena in which any supplied lawful query is evaluated. No metric component
or reciprocal-kernel formula changed.

## Exact evidence

- preregistered and pushed at `2ddba8a2`; G244 source-scope repair pushed at `dc6cbde4` before the
  fresh evidence rerun;
- nine frozen source hashes and phrase checks;
- 10,524 exact production cases and 26,992 assertions;
- 9,891 implementation-distinct exact cases and 22,050 assertions;
- noncollinear reversal, composition, clock cocycle, endpoint gauge covariance, affine scaling,
  plane quotient, G298 plane retention, and isotropy checks;
- nine hostile mutation catches;
- fresh external review replayed all checks, accepted the algebra, and refuted the ownership jump;
- no observation, fit, action, source, matter, field equation, scale, profile, distance, `X_max`,
  or protected input.
