# G267 exact derivation — provisional `sech(delta)` mutual-clock projection

Date: 2026-08-26

## Primary landing

```text
SECH_PROVISIONALLY_CLOSES_A_COEFFICIENT_FREE_BOUNDED_PAIR_STATE
__SIGNED_COMPANION_REQUIRED_FOR_COMPOSITION
__MUTUAL_EFFECT_IS_QUADRATIC_AT_QUIET_AND_SYMMETRIC_AT_LOUD_ENDS
__DISTANCE_SCALE_QUERY_POPULATION_AND_HISTORY_REMAIN_OPEN
```

This is preregistered alternative C. The physical reading

\[
M_{AB}=\operatorname{sech}\delta_{AB}
\]

is a `SUPPLIED_PROVISIONAL_CANDIDATE`. It is not regraded as derived uniqueness or canon by the
consequences below.

## 1. The native compactified pair state

G266 already derives, on one supplied regular G220 same-correspondence relation,

\[
\Gamma=\cosh\delta,
\qquad
\Xi=\sinh\delta,
\qquad
\Gamma^2-\Xi^2=1.
\]

The provisional projection and the existing normalized pair position are

\[
\boxed{M=\frac1\Gamma=\operatorname{sech}\delta},
\qquad
\boxed{\chi=\frac\Xi\Gamma=\tanh\delta}.
\]

Therefore

\[
\boxed{M^2+\chi^2=1},
\qquad
M>0,
\qquad
-1<\chi<1.
\]

Thus additive depth maps bijectively to the open right unit semicircle; its two infinite-depth
endpoints occur only in the compact closure. This is the central normalization of the reciprocal
hyperbola by its even trace coordinate. No coefficient, profile, or observational scale enters.

The complete kernel state is recovered exactly:

\[
\Gamma=\frac1M,
\qquad
\Xi=\frac\chi M,
\]

\[
r=e^{-\delta}=\Gamma-\Xi=\frac{1-\chi}{M},
\qquad
r^{-1}=\frac{1+\chi}{M}.
\]

The mutual projection does not replace the signed one-way clock/frequency arrow. It joins it in a
bounded presentation of the same reciprocal kernel.

## 2. Reversal and the original mutual-slowdown statement

Mathematical reversal of the same event correspondence gives

\[
\delta\mapsto-\delta,
\qquad
M\mapsto M,
\qquad
\chi\mapsto-\chi.
\]

Consequently

\[
\boxed{M_{AB}=M_{BA}}.
\]

This realizes the proposed statement “A sees B slowed and B sees A slowed” as a symmetric magnitude,
while `r_AB` and `r_BA=r_AB^-1` retain the orientation needed by the exact correspondence. A later
causal return remains a different query.

## 3. Exact composition requires the complete pair

For two composable supplied relations, additive depth gives

\[
\boxed{
\chi_{AC}
=
\frac{\chi_{AB}+\chi_{BC}}
     {1+\chi_{AB}\chi_{BC}}
},
\]

\[
\boxed{
M_{AC}
=
\frac{M_{AB}M_{BC}}
     {1+\chi_{AB}\chi_{BC}}
}.
\]

The denominator is positive on the regular state space. The identity is `(M,chi)=(1,0)`, reversal
is `(M,chi)->(M,-chi)`, and associativity is inherited exactly from addition of `delta`. The unit-
semicircle constraint is preserved.

`M` alone cannot compose. Take two inputs with

\[
M_1=M_2=\frac45,
\qquad
|\chi_1|=|\chi_2|=\frac35.
\]

For equal signs,

\[
(M_{12},\chi_{12})
=
\left(\frac8{17},\frac{15}{17}\right),
\]

whereas opposite signs give

\[
(M_{12},\chi_{12})=(1,0).
\]

The same two mutual magnitudes therefore have different composites. The signed companion is not an
optional correction; it is part of the complete reciprocal state.

## 4. Quiet middle and two loud ends

The exact differential interlock is

\[
\boxed{
\frac{dM}{d\delta}=-M\chi,
\qquad
\frac{d\chi}{d\delta}=M^2
}.
\]

At the quiet point,

\[
M(0)=1,
\qquad
M'(0)=0,
\qquad
M''(0)=-1,
\]

and

\[
\boxed{
M
=
1-\frac{\delta^2}{2}
+\frac{5\delta^4}{24}
+O(\delta^6)
}.
\]

So the mutual effect `1-M` begins quadratically. By contrast, the signed directional arrow remains

\[
r=e^{-\delta}=1-\delta+O(\delta^2).
\]

Direct redshift can therefore remain first order in depth while the symmetric mutual sector is much
quieter near zero.

At the two ends,

\[
M\sim2e^{-\delta}\quad(\delta\to+\infty),
\qquad
M\sim2e^{\delta}\quad(\delta\to-\infty).
\]

Thus `M->0` and the mutual-effect magnitude `1-M->1` symmetrically at both extremes. The exact
quiet/loud/loud envelope is a consequence of the provisional projection, not a fitted regime
function.

## 5. Why the projection remains a premise

Existing premises distinguish `Gamma`, but do not select which positive normalized smooth function
of `Gamma` is the physical mutual clock. For example,

\[
F_1(\Gamma)=\frac1\Gamma,
\qquad
F_2(\Gamma)=\frac1{\Gamma^2},
\qquad
F_3(\Gamma)=\frac2{\Gamma+1}
\]

are all coefficient-free, positive, reversal-even, and normalized to one at `Gamma=1`. At
`Gamma=5/4` they give, respectively,

\[
\frac45,
\qquad
\frac{16}{25},
\qquad
\frac89.
\]

Therefore evenness, normalization, positivity, and absence of a fitted coefficient do not derive
`1/Gamma`. The additional unit-semicircle physical interpretation selects it provisionally; that
interpretation is precisely the new content.

## 6. What separation it owns

Once the candidate is supplied,

\[
|\delta|=\operatorname{arcosh}\frac1M.
\]

With `chi` retaining orientation,

\[
\delta=\operatorname{artanh}\chi.
\]

These are dimensionless reciprocal depths. Neither equation provides a length unit, chooses areal,
slice, optical, radar, or pair-surface separation, or populates a query branch. A dimensionful
distance still requires an independently owned protocol and scale.

## 7. Why no metric history is selected

For every admitted smooth valued depth history `delta(q)`, the formulas

\[
M(q)=\operatorname{sech}\delta(q),
\qquad
\chi(q)=\tanh\delta(q)
\]

define a valid state pointwise. The candidate therefore rejects zero currently admitted histories.
It is a new physical readout premise, not a propagation equation for `delta`, a source law, or a
complete metric history.

## Exact status

- `DERIVED_CONDITIONAL`: the right-semicircle algebra, reconstruction, reversal, composition,
  differential interlock, and limits after the candidate is supplied.
- `SUPPLIED_PROVISIONAL_CANDIDATE`: `M=1/Gamma` is the physical mutual-clock projection.
- `OPEN`: independent derivation or canonization of that projection; operational distance and
  scale; query population; physical valued history; source/matter; global completion.
