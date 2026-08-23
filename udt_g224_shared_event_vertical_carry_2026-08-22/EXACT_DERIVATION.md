# G224 exact derivation — metric-normalized vertical carry at a shared observer event

Date: 2026-08-22

## Bounded landing

```text
SHARED_MIDDLE_EVENT_AND_METRIC_UNIT_CLOCK_CANONICALLY_IDENTIFY_INCIDENT_FUTURE_NULL_VERTICAL_LINES
__VERTICAL_SCALAR_CARRY_IS_THE_INVERSE_REPRESENTATION_OF_THE_ACTUAL_CLOCK_RATE_CHAIN
__DISTINCT_EVENT_NORMALIZATION_IS_ABSTRACTLY_AVAILABLE_BUT_NOT_A_COMPOSABLE_VERTEX_RELATION
__NO_SCREEN_MAP_OR_INDEPENDENT_DIRECT_RELATION_IS_DERIVED
```

Status: `DERIVED_CONDITIONAL__INTERNALLY_VERIFIED__FRESH_EXTERNAL_REVIEW_PENDING`.

The condition is important: the metric, observer germs, marked incidences, and regular future-null
ribbons are supplied. This package does not derive a universal null observer protocol or populate
a physical history.

## 1. Exact type ledger

Let `b` be one marked event of a supplied future-timelike observer `B`, with metric-unit tangent

\[
U_B\in T_bM,
\qquad
g(U_B,U_B)=-1.
\]

Let two supplied regular future-null ribbons meet `B` at `b`. Their vertical tangent lines are

\[
V_-\subset T_bM,
\qquad
V_+\subset T_bM.
\]

They may be different null directions. Each is time-oriented by its future ray. The required carry
is a linear map between the **one-dimensional vector spaces** `V_-` and `V_+`; it is not an ambient
Lorentz transformation of `T_bM`.

## 2. The metric clock functional is nondegenerate

For either incident line define

\[
\mu_\pm:V_\pm\longrightarrow\mathbb R,
\qquad
\mu_\pm(v)=-g(U_B,v).
\]

If `v` is nonzero and future null, then `-g(U_B,v)>0`. To see this, choose an orthonormal frame at
`b` in which `U_B=(1,0,0,0)`. A future-null vector has `v^0=|\vec v|>0`, so

\[
-g(U_B,v)=v^0>0.
\]

Therefore each restriction `mu_+` and `mu_-` is a nonzero linear functional on a one-dimensional
space, hence a linear isomorphism to `R`.

This uses more data than G216's clock derivative alone. It uses the actual ambient metric, the
actual observer clock at the incidence, and both incident null lines.

## 3. Unique shared-event switch

Define

\[
\boxed{
S_{+\leftarrow-}=\mu_+^{-1}\circ\mu_-:
V_-\longrightarrow V_+ .}
\]

It obeys

\[
\mu_+\!\left(S_{+\leftarrow-}v\right)=\mu_-(v).
\]

It is the unique map with this property: if another linear map `R:V_- -> V_+` preserves the same
pairing, then `mu_+ R=mu_-`; applying `mu_+^{-1}` gives `R=S`.

Choose arbitrary positive affine generators `K_-` and `K_+` and set

\[
\omega_-=-g(U_B,K_-)>0,
\qquad
\omega_+=-g(U_B,K_+)>0.
\]

Then

\[
\boxed{
S_{+\leftarrow-}(K_-)=\frac{\omega_-}{\omega_+}K_+.}
\]

Under independent positive rescalings

\[
K_-\mapsto\gamma_-K_-,
\qquad
K_+\mapsto\gamma_+K_+,
\]

the displayed coordinate coefficient changes to

\[
\frac{\gamma_-\omega_-}{\gamma_+\omega_+},
\]

which represents exactly the same abstract linear map. Hence no affine-generator scale has been
smuggled in.

The metric-unit condition already fixes the normalization of `U_B`. If one temporarily uses the
same positive nonunit representative `u_B=zeta U_B` on both incidences, both functionals acquire
the factor `zeta`, which cancels from `S`. Using two independently rescaled middle clocks would no
longer describe one calibrated shared observer event.

## 4. Vertex cocycle

For any collection of future-null lines `V_i` incident at the same calibrated observer event, set

\[
S_{j\leftarrow i}=\mu_j^{-1}\mu_i.
\]

Then

\[
S_{k\leftarrow j}S_{j\leftarrow i}
=\mu_k^{-1}\mu_j\mu_j^{-1}\mu_i
=S_{k\leftarrow i},
\]

and

\[
S_{i\leftarrow i}=1,
\qquad
S_{i\leftarrow j}=S_{j\leftarrow i}^{-1}.
\]

Thus the vertex switches form a thin pair-groupoid on the incident **line amplitudes**. No extra
positive scale torsor remains.

## 5. Edge transport and inverse clock carry

Now consider one supplied affinely ruled future-null edge `e:A->B`. Let its affine generator be
parallel along the ray,

\[
P_eK_{e,A}=K_{e,B},
\]

and define the observer frequencies

\[
\omega_{e,A}=-g(U_A,K_{e,A}),
\qquad
\omega_{e,B}=-g(U_B,K_{e,B}).
\]

The G220 proper-clock arrow on this same null incidence is

\[
r_e=\frac{d\tau_B}{d\tau_A}
=\frac{\omega_{e,A}}{\omega_{e,B}}.
\]

Normalize the endpoint line generators by the metric clocks:

\[
N_{e,A}=\frac{K_{e,A}}{\omega_{e,A}},
\qquad
N_{e,B}=\frac{K_{e,B}}{\omega_{e,B}}.
\]

Both satisfy `-g(U,N)=1`. Affine transport gives

\[
P_eN_{e,A}
=\frac{K_{e,B}}{\omega_{e,A}}
=\frac{\omega_{e,B}}{\omega_{e,A}}N_{e,B}
=\boxed{r_e^{-1}N_{e,B}}.
\]

Since G216 uses

\[
\delta_e=-\log r_e,
\]

the vertical coefficient is

\[
r_e^{-1}=e^{\delta_e}.
\]

This is the reciprocal ruler representation of the proper-clock arrow, derived here from the same
metric null relation rather than attached as a post-readout modifier.

## 6. Actual three-observer composition

For supplied composable relations `A->B` and `B->C`, the incoming edge ends and the outgoing edge
begins at the same calibrated event of `B`. The vertex switch maps the incoming frequency-one
generator exactly to the outgoing frequency-one generator:

\[
S_BN_{AB,B}=N_{BC,B}.
\]

Therefore

\[
P_{BC}S_BP_{AB}N_{AB,A}
=r_{AB}^{-1}r_{BC}^{-1}N_{BC,C}.
\]

G216 gives, for the actual composed event relation,

\[
r_{AC}=r_{BC}r_{AB}.
\]

Hence

\[
\boxed{
q_{AC}=q_{BC}q_{AB}
=(r_{BC}r_{AB})^{-1}
=r_{AC}^{-1}.}
\]

The middle switch contributes no fitted scalar. It only converts between the two metric-normalized
null line bases at the shared observer event.

An independently supplied direct `A->C` ribbon need not be this composite. If its clock ratio is
`r_AC^ind`, present identities do not force

\[
r_{AC}^{\rm ind}=r_{BC}r_{AB}.
\]

This retains the exact G214 boundary.

## 7. Different directions and the screen ceiling

In Minkowski space let

\[
U=(1,0,0,0),
\]

\[
K_- = \alpha(1,1,0,0),
\qquad
K_+ = \beta\left(1,\frac35,\frac45,0\right),
\]

with `alpha,beta>0`. Both vectors are future null and

\[
-g(U,K_-)=\alpha,
\qquad
-g(U,K_+)=\beta.
\]

The unique switch is

\[
S(K_-)=\frac\alpha\beta K_+.
\]

It preserves the clock pairing but does not make the two ambient vectors equal; their spatial
directions differ. Thus the theorem does not supply:

- an ambient Lorentz transformation;
- an identification of screen planes;
- an `SO(2)` screen rotation;
- a Jacobi map; or
- angular holonomy.

Those remain separate complete-metric channels.

## 8. Distinct-event scope correction

The preregistration said that the construction is unavailable at distinct middle events without
transport. That sentence was too broad.

Given any two observer-calibrated future-null lines, even at different events, the two metric clock
functionals still define the abstract line isomorphism

\[
\mu_2^{-1}\mu_1.
\]

No ambient transport is required merely to match their one-dimensional normalized amplitudes.
What is unavailable at distinct events is the **shared physical vertex** required to compose the
two supplied event relations pointwise. The abstract normalization does not create event incidence,
a path, or ambient direction transport.

Accordingly the preregistered outcome is graded

```text
A_WITH_DISTINCT_EVENT_SCOPE_CORRECTION
```

rather than an unqualified `A`.

## 9. Relation to G223

G223 proved that the clock derivative by itself does not identify distinct vertical bundles. G224
does not contradict that statement. It adds the data G223 deliberately did not use in that step:

- the observer metric-unit clock at each incidence; and
- the restriction of the ambient metric to each clock--null pair.

Those data turn every incident null line into a canonically normalized real line. At a real shared
event, their unique comparison is the required vertex switch.

This closes the local one-dimensional carry question on the declared null network. It does not
select null ribbons as the universal UDT pair protocol, choose a complete metric history, or derive
global screen and branch carry.

## 10. Verification

The SymPy derivation checks 24 exact identities. An independent standard-library implementation
uses exact rational arithmetic on 20,000 seeded cases and performs 220,003 assertions, including
affine-basis covariance, common-clock cancellation, vertex cocycles, two- and three-edge inverse
clock products, independent-direct counterexamples, and unequal null-direction controls.
