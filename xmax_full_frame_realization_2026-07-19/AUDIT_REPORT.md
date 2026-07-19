# Xmax full-frame realization audit

Date: 2026-07-19

Base: `07f397607c2ca784630034a97fb7f24cf08d378d`

Status: `VERIFIED-WITH-CAVEATS`; exact conditional realization, not canon or complete UDT closure

## Result first

A complete four-dimensional positional frame action **does exist** in a sharply defined reciprocal
CSN coframe family. It preserves the same symbolic `X_max`, composes exactly, preserves the conditional
metric null cones, and changes the entire metric by only one common positive scale:

\[
 \boxed{\phi'=\phi-\beta},\qquad
 \boxed{t'=e^{-2\beta}t},\qquad
 \boxed{y'^A=y^A},
\]

for

\[
 \boxed{
 g=-e^{-2\phi}c^2dt^2+e^{2\phi}h_{ij}dz^i dz^j,
 \qquad h_{ij}=h_{ij}(y)
 }
\]

gives

\[
 \boxed{F_\beta^*g=e^{-2\beta}g}.
\]

Because Common-Scale Neutrality identifies the two sides, this is an exact frame equivalence in the
declared family. It is a CSN homothety, not generally an isometry.

The crucial structural finding is that, under the registered time action, the reciprocal spatial
coframe must be based on **additive positional depth**, `L dphi`, rather than the differential `dx` of
the bounded reach chart. The latter contains `sech(phi)^2` and fails full-frame covariance exactly.
The earlier mismatch was therefore not a failure of every full-frame realization; it was a
discriminator between two spatial coframe identifications.

There is also a principled reduction of the historical fractional-linear premise. The reciprocal
coframe pair after quotienting common scale is the positive projective ray

\[
 [u:v]=[e^{-\phi}:e^{+\phi}].
\]

The unique fractional-linear coordinate sending the reciprocal axes to `-1,+1` and the neutral ray
to `0` is

\[
 \boxed{\xi=\frac{v-u}{v+u}=\tanh\phi}.
\]

Multiplication of the reciprocal projective ratios then gives

\[
 \boxed{\xi_1\oplus\xi_2
 =\frac{\xi_1+\xi_2}{1+\xi_1\xi_2}}.
\]

Thus historical `P2` is no longer an arbitrary standalone formula **if** positional separation is
identified with this anchored projective coordinate of the reciprocal CSN coframe ray. That
`PROJECTIVE_POSITION_JOIN` is the smallest remaining premise. It is highly native-looking, but it is
not yet owner-locked and this audit does not promote it.

The result does not close the absolute finite-cell field: an observer shift of relational depth is
not compatible with treating the same quantity as an absolute scalar fixed to `phi=0` on one physical
seal. Relational depth and the absolute static field therefore remain distinct unless their map or
boundary action is derived.

## Lay interpretation

The old picture treated the bounded distance `x` as though its tiny ruler marks `dx` were the thing
that receives reciprocal spatial dilation. That does not transform consistently when an observer
moves their positional origin.

The consistent object is instead the unbounded depth coordinate `phi`. It behaves like a running
count of relational layers. Every observer may subtract their own depth `beta`, while their time unit
rescales in exactly the amount needed to make all four metric sectors change together. CSN declares
that common change of units physically neutral.

The bounded distance is then not the fundamental ruler. It is a projective display of the reciprocal
clock/ruler pair:

\[
 x=X_{\max}\tanh\phi.
\]

All observers retain the same `X_max`; shifting `phi` merely changes where they place zero. The
fractional-linear position law is what that projective display does when reciprocal dilations
compose.

This is close to the SR analogy Charles proposed, with an important qualification. We now have a
complete conditional frame representation, but we have not yet proved that UDT identifies physical
position with the projective coframe ray, nor reconciled relational depth with the absolute
finite-cell field.

## Why the projective coordinate appears

UDT Reciprocity supplies positive dual weights, in the current representation,

\[
 u=e^{-\phi},\qquad v=e^{+\phi},\qquad uv=1.
\]

CSN removes their common scale. What remains is their projective ratio

\[
 r=\frac vu=e^{2\phi}.
\]

Consider a fractional-linear coordinate `(ar+b)/(cr+d)` with three relational anchors:

- the pure `u` axis `r=0` is `xi=-1`;
- the neutral ray `u=v`, `r=1`, is `xi=0`;
- the pure `v` axis `r=infinity` is `xi=+1`.

Those conditions uniquely give

\[
 \xi=\frac{r-1}{r+1}=\frac{v-u}{v+u}=\tanh\phi.
\]

Common scaling `(u,v)->(su,sv)` leaves `xi` unchanged, and reversal `u<->v` sends `xi->-xi`.
Composition multiplies `r`, so the XR1 addition formula follows exactly.

The previous smooth bounded countergroup is still decisive against a larger claim: a finite bound,
identity, reversal, associativity, and smoothness do not force this chart. It is excluded only after
requiring position to be an anchored **projective** coordinate of the reciprocal coframe ray.

Status:

- reciprocal ray after CSN: `DERIVED_IN_DECLARED_DUAL_REPRESENTATION`;
- anchored chart given projective positional interpretation: `DERIVED_CONDITIONAL`;
- physical join `x=X_max xi`: `PROJECTIVE_POSITION_JOIN / CANDIDATE`;
- XR1 after that join: `DERIVED_CONDITIONAL_ON_PROJECTIVE_POSITION_JOIN`.

## Exact full-frame action

Let `z^i=(phi,y^1,y^2)` and let `h_ij=h_ij(y)` be a stationary positive spatial seed invariant under
the frame map. More generally the exact requirement is `F_beta^*h=h`. The seed may contain transverse
structure and invariant depth-transverse cross terms. Merely imposing `partial_phi h=0` would be
insufficient if time-dependent spatial seeds were admitted. Apply

\[
 F_\beta:(t,\phi,y^A)
 \longmapsto(e^{-2\beta}t,\phi-\beta,y^A).
\]

The temporal term pulls back as

\[
 -e^{-2(\phi-\beta)}c^2d(e^{-2\beta}t)^2
 =e^{-2\beta}\left(-e^{-2\phi}c^2dt^2\right).
\]

The complete spatial term pulls back as

\[
 e^{2(\phi-\beta)}h_{ij}dz^i dz^j
 =e^{-2\beta}\left(e^{2\phi}h_{ij}dz^i dz^j\right).
\]

Therefore every component, including allowed cross terms in `h`, receives the same factor. Also,

\[
 F_{\beta_2}\circ F_{\beta_1}=F_{\beta_1+\beta_2}.
\]

With `xi=tanh(phi)` and `alpha=tanh(beta)`, the bounded display is

\[
 \xi'=\tanh(\phi-\beta)
 =\frac{\xi-\alpha}{1-\alpha\xi}.
\]

The limiting endpoints `xi=+-1` remain fixed, while every finite interior position may be recentered.
`X_max` and `c` are unchanged symbolic parameters. The common factor is positive, so this conditional
metric's null cone is preserved.

This supplies the requested all-sector frame realization in the declared family. It does not prove
that this is the unique complete UDT metric or that all physically allowed field and boundary data
transform this way.

## Why bounded `dx` failed and additive `dphi` works

Suppose a pure depth coframe is `k(phi)dphi` and retain the preregistered F3 time action
`t'=exp(-2beta)t`. After the explicit reciprocal factor `e^phi`, full-frame CSN covariance requires

\[
 k(\phi-\beta)=k(\phi)
\]

for every `beta`. Hence `k` is constant:

\[
 \boxed{k(\phi)=L}.
\]

Choosing `L=X_max` uses the working universal reach as one global ruler; it does not calculate
`X_max` or prove that normalization.

This selection is scoped to the fixed F3 time action. If its exponent is freed, the exact family

\[
 k(\phi)=e^{a\phi},\qquad
 t'=e^{-(a+2)\beta}t
\]

gives the common factor `exp(-2(a+1)beta)`. Covariance alone therefore does not uniquely select
`a=0`. The registered F3 transformation does. Bounded `dx` still fails every constant time rescaling
in this class because its defect depends on position.

By contrast,

\[
 dx=X_{\max}\operatorname{sech}^2\phi\,d\phi.
\]

The `sech^2(phi)` seed is not translation invariant. For
`alpha=1/3`, `beta=atanh(1/3)`, the temporal ratio is `1/2`, while the exact bounded-`dx` spatial
ratios include

\[
 \frac{32}{81}\quad\hbox{and}\quad\frac{512}{625}
\]

at the registered sample positions. They cannot be one CSN factor.

This regrades the choice of radial variable:

> Under the fixed F3 time action, `x` is a bounded projective reach display, while `phi` is the
> additive frame/depth coordinate whose differential supplies the covariant reciprocal spatial
> coframe.

That statement is exact inside the projective-position/full-frame premises. It is not yet canon.

## Angular and transverse sector

In the restricted warped family

\[
 g=-e^{-2\phi}c^2dt^2
  +e^{2\phi}L^2d\phi^2
  +R(\phi)^2q_{AB}(y)dy^A dy^B,
\]

the common frame factor requires

\[
 R(\phi-\beta)=e^{-\beta}R(\phi).
\]

The positive solutions are

\[
 \boxed{R(\phi)=C e^\phi}.
\]

Thus the frame requirement selects the same reciprocal `e^phi` weight for transverse coframes. This
is a genuine radial-angular constraint.

It does **not** select the intrinsic two-metric `q_AB`. A round local sphere, a flat local transverse
metric, and arbitrary `phi`-independent intrinsic geometry all pass the frame equation. The general
matrix proof also permits invariant depth-transverse cross terms. Consequently topology, roundness,
curvature sign, connection/twist, section, and boundary completion remain open.

The result is `PHI_DEPENDENCE_SELECTED_IN_RESTRICTED_WARP_CLASS`, not a derived `S^2` or unique
holonomy.

## Why 1+1 conformal covariance is not enough

Every two-dimensional Lorentzian metric is locally conformally flat. In optical null coordinates
`u=t-y`, `v=t+y`, write

\[
 g_2=-A(y)du\,dv.
\]

For any smooth monotone one-parameter re-centering `h_beta(y)`, the extension

\[
 u'=-h_\beta(-u),\qquad v'=h_\beta(v)
\]

is locally conformal, with a positive factor proportional to
`h_beta'(-u)h_beta'(v)`. At `t=0` it realizes `y'=h_beta(y)`.

Therefore neither local 1+1 conformal freedom nor CSN alone selects XR1. The selection enters through
the reciprocal projective coframe interpretation and the complete spatial-frame requirement.

## The finite-cell seam remains real

The frame construction treats `phi_rel` as relational depth:

\[
 \phi_{rel}'=\phi_{rel}-\beta.
\]

Each observer can place their own relational origin at zero. But the current absolute static field
convention fixes `Phi_abs=0` at one physical mirrored-cell seal. If the same scalar is shifted
internally, its seal value becomes `-beta`, not zero.

There are at least three logically possible resolutions:

1. `phi_rel` is a coordinate/projective parameter distinct from the absolute field `Phi_abs`;
2. the full boundary and field frame action supplies a compensating map;
3. one of the current global-frame or absolute-seal interpretations must be revised.

The audit selects none. It only rejects silently using the same symbol as though the join were
already derived.

## Xmax, total mass, and c

The exact frame map leaves `X_max` fixed. It is therefore mathematically consistent for all observers
to share one `X_max` inside this representation.

If bootstrap later gives

\[
 X_{\max}=F(c,M_{\rm total},G),
\]

then observer invariance additionally requires `M_total` and every other argument to be native global
scalars of the complete solution. Ordinary frame-dependent energy cannot simply be inserted. UDT's
complete action, source, and native mass definition remain open, so this is only a compatibility
condition.

The symbol `c` is also unchanged by the frame map, and the positive conformal factor preserves the
conditional metric null cone. The construction does not determine the value or cosmic origin of `c`
and does not yet turn the null cone into a native propagation theorem.

## Does this select the action or matter?

No. The frame realization constrains an admissible metric/coframe family, but it does not decide:

- the complete varying fields;
- pre-scale versus post-scale variation;
- derivative order or invariant inventory;
- a native source or coupling;
- the differentiable finite-cell boundary action;
- carrier emergence, mass, or stability outside existing premises.

It is potentially valuable input to the action problem because an eventual action should respect or
explain this frame structure. It is not itself that action.

## Verdict and evidence gates

- `EXACT_CONDITIONAL`: a four-dimensional one-parameter frame group with fixed `X_max` and
  `F_beta^*g=e^-2beta g` exists in the reciprocal additive-depth coframe family.
- `DERIVED_CONDITIONAL_ON_PROJECTIVE_POSITION_JOIN`: the anchored projective coframe coordinate gives
  `xi=tanh(phi)` and XR1.
- `SELECTED_IN_FIXED_F3_CLASS`: with the registered time action, full-frame covariance selects
  constant depth seed `L dphi` over bounded `dx`; it also selects reciprocal `e^phi` transverse
  dependence in the restricted warp family. A freed time exponent admits the recorded exponential
  depth-seed counterfamily.
- `REFUTED_IMPLICATION`: finite `X_max` or local 1+1 CSN covariance alone selects XR1.
- `NOT_DERIVED`: intrinsic angular geometry, topology, global boundary/field action, `X_max` value,
  action, source, matter, or physical signal law.
- `OPEN_ROLE_DISTINCTION`: relational projective depth versus the absolute static seal field.

Evidence gates:

1. **Preregistered:** yes, commit `c8fc885` before algebra.
2. **Full space or bounded scope:** complete four metric sectors in the declared reciprocal CSN
   coframe family, exact restricted-warp and 1+1 counterfamilies; not all diffeomorphisms, fields,
   angular geometries, or boundaries.
3. **Independent verification:** recorded separately in this package.
4. **Every premise audited:** recorded in `FRAME_COMPONENT_LEDGER.tsv` and `STATUS_LEDGER.tsv`.

The package grade is `VERIFIED-WITH-CAVEATS`. The smallest genuinely missing premise is the
`PROJECTIVE_POSITION_JOIN`, followed by the map between relational depth and the absolute static
field/seal. Charles retains the physics verdict.
