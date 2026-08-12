# UDT from reciprocal clock/ruler postulates to the current Xmax/CMB frontier

## Cold-start consultation brief

Date: 2026-08-12  
Repository authority: `LIVE.md`, then `CURRENT_SCIENTIFIC_PREMISES.tsv`, then the frozen source
spine in `SOURCE_MANIFEST.tsv`  
Purpose: expose the whole dependency chain and ask whether the present obstacle is mathematical,
conceptual, or a missing premise  
Maximum conclusion: diagnosis and next-question design only

This document is intentionally self-contained. It asks a cold reviewer to challenge the framing,
not to make UDT work and not to choose a geometry because it resembles a desired universe.

## 1. The physical picture being attempted

UDT begins from a relational view of clock and ruler calibration. The observed Einsteinian
constant `c_E` is treated as the reversible conversion between temporal and spatial measure,

```text
L = c_E T,
T = L/c_E,
```

rather than being used here as a material signalling law. The second founding idea is UDT
Reciprocity: positional comparison acts dually on the clock and ruler sides of that conversion.

The project also uses a working co-present interpretation. Co-presence means membership in one
complete geometric solution. It does not mean instantaneous access, zero travel time, or a
material signalling theorem. All present cosmological calculations concern relations between
observational frames, not changes to ordinary local physics.

The hoped-for global picture is that ordinary terrestrial/solar observations recover the usual
`c_E` calibration, while extreme observer separation may approach a frame-shared positional
dilation asymptote `X_max`. The angular and mixing sectors of the complete metric may modulate the
observer relation, so the result need not be a radial solo. That physical picture remains partly
working hypothesis. The exact owned mathematics is narrower and is listed below.

## 2. Founding implication chain

Use the dimension-matched coframe pair

\[
q=\begin{pmatrix}c_E\,dt\\dr\end{pmatrix}.
\]

For an already supplied ordered positional depth `Delta`, take a positive diagonal comparison

\[
P(\Delta)=\operatorname{diag}(u(\Delta),v(\Delta)).
\]

Let

\[
K=\begin{pmatrix}0&1\\1&0\end{pmatrix}
\]

encode the dual clock/ruler evaluation pairing. UDT Reciprocity is represented by

\[
P(\Delta)^T K P(\Delta)=K,
\]

which gives exactly

\[
u(\Delta)v(\Delta)=1.
\]

Continuous positional composition and reversal are additionally posited:

\[
P(\Delta_2)P(\Delta_1)=P(\Delta_1+\Delta_2),
\qquad P(-\Delta)=P(\Delta)^{-1}.
\]

After excluding the trivial representation and choosing the sign and unit of depth, this derives

\[
D(\delta)=\operatorname{diag}(e^{-\delta},e^{+\delta}).
\]

When the character is represented by a supplied local pointwise presentation `phi`, and with the
declared Lorentzian quadratic and inherited spherical-areal readouts, one obtains the conditional
founding metric chart

\[
ds^2=-e^{-2\phi}c_E^2dt^2+e^{2\phi}dr^2+r^2d\Omega^2.
\]

### Premise precision

The arithmetic existence of `c_E^{-1}` does not derive this metric. The chain also requires:

- dual rather than ordinary covariant action on the conversion pair;
- continuous additive comparison depth;
- a nontrivial realized comparison;
- the local Lorentzian quadratic readout; and
- the spherical areal angular readout in this chart.

The first exact product is therefore:

```text
supplied ordered depth delta -> reciprocal character D(delta).
```

The founding does not yet supply:

```text
(complete geometry, observers, paired events, route/branch) -> delta.
```

This distinction is central to the present consultation.

## 3. What phi is, and what it is not

Three related uses must not be collapsed.

### 3.1 Founded reciprocal coordinate

`phi` is the additive logarithmic coordinate of the derived reciprocal representation. It is not
an undefined random placeholder. Once a depth is supplied, its action, addition, reversal, and
clock/ruler exchange parity are exact.

### 3.2 Pointwise presentation potential

In a complete factorized coframe, a local split can be written schematically as

```text
theta = D(phi) bar_theta,
D(phi)=diag(exp(-phi),exp(+phi)).
```

Local reciprocal refactorizations can change the displayed pointwise `phi` while leaving the
complete coframe unchanged. Thus the complete metric does not universally recover one preferred
pointwise representative without a reference, pair relation, stationary structure, or other
owner. A global pointwise `phi` is a potential representation on branches where the physical
relation is endpoint exact; it is not the primitive universal observable.

### 3.3 Terminal reciprocal coordinate of a supplied pair metric

When a calibrated observer-pair realization is supplied, the complete metric returns a unique
terminal reciprocal coordinate. This is the most important later correction and is derived in
Section 5.

## 4. The complete-coframe broadening

The founding two-channel character does not uniquely determine its complete four-dimensional
extension. In a positive triangular chart, fixing the founded base generator still leaves three
angular-generator parameters and four base-angular mixing parameters. Direct-sum spectator,
reciprocal-angular, and shift-mixing extensions all exist.

Later work therefore introduced a complete pair-adapted coframe configuration of the form

\[
E=\begin{pmatrix}B&0\\QS&Q\end{pmatrix},
\qquad g=E^T\eta E,
\]

Here `B` and `Q` are regular `2 x 2` base and positive-screen blocks, `S` is a real `2 x 2`
mixing matrix, and `eta=diag(-1,+1,+1,+1)`. `B` carries common scale, reciprocal depth, and
shift; `Q` carries angular scale, shear, and frame presentation; and `S` carries four mixing
channels. The exact ten-variable Jacobian uses a fixed positive lower-triangular representative
for `Q` after removing local left-`O(2)` presentation freedom.

This block form is conditional on a supplied regular reciprocal/angular `2+2` split. No universal
split, screen, or global coframe section is founded. On the declared positive-screen,
time-oriented regular component, it is a coordinate chart on all ten independent Lorentzian
metric components. Its point-map Jacobian is nonzero, and the same remains true at every finite
jet order.

This yields two exact conclusions:

1. the complete chart does not secretly omit a metric degree of freedom on its declared stratum;
2. it cannot select a proper subset of metric histories by being expanded more deeply.

The Maurer--Cartan, Cartan, and Bianchi equations organize compatibility and curvature of supplied
histories. They are not equations of motion. With time turned fully on, arbitrary smooth complete
coframe movies remain kinematically admissible.

This broadening was scientifically useful: it allowed the angular orchestra and mixing to act.
It was not a derivation that one particular complete extension or history is physical. The
project moved from a founded reciprocal subgroup to a local configuration arena of all metrics
admitting that supplied split on the declared positive-screen, time-oriented regular component.

## 5. The corrected observer-pair object

Let an ordered observer query supply a regular calibrated pair immersion

\[
F:\Sigma^2\to(M,g).
\]

Use A-calibrated coordinates

```text
y^0 = c_E tau_A,
y^1 = s_A,
```

and form the complete induced pair metric

\[
h=F^*g.
\]

Every reciprocal, angular, shift, and mixing contribution enters through the complete pullback.
On the regular Lorentzian stratum `h_00<0`, `det(h)<0`, there is a unique decomposition

\[
h=-T^2(dy^0+\beta\,dy^1)^2+L^2(dy^1)^2,
\]

with

\[
T^2=-h_{00},\qquad
\beta=\frac{h_{01}}{h_{00}},\qquad
L^2=h_{11}-\frac{h_{01}^2}{h_{00}}.
\]

Write

\[
T=\sigma e^{-\phi_{\rm pair}},
\qquad
L=\sigma e^{+\phi_{\rm pair}}.
\]

Then exactly

\[
\phi_{\rm pair}
=\frac12\log\frac{L}{T}
=\frac14\log\frac{-\det h}{h_{00}^2},
\]

while `sigma=(-det h)^(1/4)` is common scale and `beta` is retained as a separate pairing/shift
state.

`phi_pair` is a state coordinate on one supplied calibrated pair family. On one coherent family,
the signed arrow depth between matched states is

\[
\Delta\phi_{\rm pair}=\phi_{\rm pair}(B)-\phi_{\rm pair}(A),
\]

which telescopes. Independently rebuilt pair tapes may carry calibration offsets and do not
compose without a lawful middle transition. The founded `delta` is therefore not automatically
identical to every locally reconstructed `phi_pair`.

The null slopes of `h` yield an orientation-balanced terminal ratio

\[
\frac{c_{\rm eff}^{(\rm pair)}}{c_E}
=\frac{T}{L}
=e^{-2\phi_{\rm pair}}.
\]

This is the sense in which reciprocal `c_E` is at the end of the calculation. The complete metric,
angular sector, mixing, global geometry, and query first determine `h`; `c_E` then calibrates the
clock/ruler readout. It does not select the pair immersion, event pairing, route, branch, history,
or global topology.

`c_eff^(pair)` is a conditional geometric pair-calibration readout. It is not silently a local signal velocity
or a universal mixed-geometry propagation law.

## 6. Query, route, and channel typing

Bare endpoints do not generically determine one preferred curve or pair surface. A physical query
may contain observer germs, event incidence, ruler evolution, calibration carry, admissible branch
rules, and requested outputs. Once supplied, the complete metric may return several distinct
channels:

| channel | natural home | present status |
|---|---|---|
| common scale / `kappa` | endpoint state on a supplied pair metric | derived conditionally |
| reciprocal depth / `phi_pair` | endpoint state or endpoint difference where exact | derived conditionally |
| shift / `beta` | calibrated pair-state variable | derived conditionally, not additive |
| Jacobi response | supplied geodesic variation/query | derived conditionally |
| screen/normal/ambient transport | path-labelled groupoid channel | derived conditionally |
| physical branch weights or source covariance | physical state/readout law | open |

The first fundamental form, second fundamental form, normal connection, Jacobi data, and holonomy
can be compatibility-linked when they arise from the same pair immersion. They do not collapse to
one scalar. Returning a branch-labelled family may be the correct geometric answer when the query
does not prove uniqueness.

## 7. Xmax: controlling meaning and current gap

`X_max` is currently a `WORKING_FOUNDATIONAL_FRAME`: the frame-shared positional-dilation
asymptote for observer pairs. A physical realization must have a nonnegative separation `s(p,q)`
and signed ordered depth `delta` such that

\[
0\le s(p,q)<X_{\max},
\]

for finite comparisons and

\[
s(p,q)\to X_{\max}^{-}
\quad\Longrightarrow\quad
|\delta(p,q)|\to\infty.
\]

This is structurally analogous to a limiting relation, but it is not yet a derived separation operator,
numerical value, tanh law, lapse zero, radial edge, finite-cell seal, causal horizon,
manifold boundary, spatial diameter, or variational boundary.

The notation `s(p,q)` and `delta(p,q)` is schematic. Until route descent is owned, realizations may
instead be `s_Q(p,q;gamma)` and `delta_Q(p,q;gamma)`. The physical law must determine whether route
labels survive or descend. No universal equality `delta=phi_pair` is assumed before a coherent
relation family and calibration carry are selected.

The whiteboard suggests a cleaner mathematical home: `X_max` may be an ideal boundary condition
on calibrated observer-relation space. That is a conceptual proposal, not yet a theorem. It avoids
pre-identifying a spacetime seam before the physical relation exists.

## 8. The SNe compatibility anchor

The corrected observer-query replay leaves the best frozen SNe fit numerically unchanged. For the
registered conditional identification

\[
1+z=e^{\phi_{\rm pair}},
\]

the leading P1 family is

\[
r(\phi_{\rm pair})
=R_w\left[1-e^{-2\phi_{\rm pair}/n}\right]
\]

or equivalently

\[
r(z)=R_w\left[1-(1+z)^{-2/n}\right].
\]

With the separately supplied area/flux readout `d_A=r` and
`d_L=(1+z)^2d_A`, the frozen primary fit gives approximately

```text
n   = 1.0559332414,
R_w = 2202.6331 Mpc,
```

with the frozen external absolute-magnitude anchor retained. Independent replay reproduces the
shape. The native retyping changes interpretation, not fitted numbers.

This is an `OBSERVED` conditional low-redshift compatibility anchor. It does not derive P1 from
the complete metric, select the SNe pair immersion, own the screen-area/flux law, determine
`X_max`, or select a CMB profile. The complete orchestra can in principle alter the pair metric
and area response upstream, but no coefficient-free native correction is presently owned.

## 9. The CMB arc before the current AM excavation

The modern CMB work was deliberately reframed away from fitting peaks. It asked what a supplied
complete metric and observer-sky query can geometrically return.

### 9.1 Query and response architecture

The complete query map separated:

- observer and source/end surfaces;
- null or other admitted routes;
- Jacobi/image response;
- screen and normal transport;
- source/state covariance;
- scalar versus orientation-sensitive observables; and
- global endpoint/scale ownership.

The metric can derive a finite Jacobi map `D` and screen isometry `U` along the same supplied
query. The relative map

\[
M=U^{-1}D
\]

has three generic oriented invariants: common response scale, shear magnitude, and relative polar
rotation. These are source-free geometric responses. They are not automatically temperature or
polarization power.

After matching source and observer screen types, covariance transports as

\[
C_{\rm obs}=M C_{\rm src}M^T.
\]

For invertible `M`,

\[
C_{\rm src}=M^{-1}C_{\rm obs}M^{-T}.
\]

Thus unrestricted source covariance can absorb any invertible local response. This is the exact
bounded non-identifiability statement; it is not a full-CMB no-go.

### 9.2 Source/response boundary

For a regular one-to-one sky map with invertible local response, arbitrary source structure is in
principle recoverable. Geometry may rearrange, magnify, shear, and rotate it strongly, but does not
erase all source freedom or create a nonconstant scalar field from zero or constant data.

A robust kaleidoscope in the stronger sense requires global branching, noninjectivity, critical or
fold behavior, singular response, or a restriction on source/state data. Multiple route branches
also require an owned rule for combination, weighting, or measurement.

### 9.3 Conditional family maps

A new center-regular stationary axial control family was constructed with

\[
\begin{aligned}
ds^2={}&-A(x)c_E^2dt^2+\frac{R^2}{A(x)}dx^2
+R^2x^2(d\theta^2+\sin^2\theta\,d\psi^2)\\
&+2Rc_E h_{\rm mix}(x)\sin^2\theta\,dt\,d\psi,\\
A(x)={}&1+a x^2,\qquad
h_{\rm mix}(x)=x^2q(x^2),\qquad x=r/R\in[0,1].
\end{aligned}
\]

using 49 exact primitive profile shapes, four amplitudes, three lapse controls, and three zero-
mixing controls: 591 geometries total. These are `CHOSE_CONTROL`, not physical profiles.

The whole-sky atlas and a direct-Christoffel replay evaluated roughly 1.5 million sampled rays.
All 591 controls survived the registered finite-mesh regularity/topology gates and were sampled
degree one. That is a strong evaluator/solution-space result, not continuum injectivity or physical
selection.

An ownership audit found no current native owner of the profile, endpoint/global scale, or source
state. A same-geometry control subsequently returned both a stationary redshift and angular
distance before comparison to SNe, and reverse-pair/nonradial/integrator controls verified the
geometric reciprocity and screen covariance. Those calculations show the machinery coheres on
chosen controls. They do not choose the controls.

## 10. G83--G86: the current conditional excavation

### G83 — stationary endpoint-asymptote candidates

All 591 controls have finite depth on their owned `0<=x<=1` domain. Under a transparent
`FREE_AND_EXPLORED` continuation, only

\[
A_-(x)=1-x^2/4
\]

has a positive lapse zero, at `x=2`. The repository label `AM` below refers only to this chosen
`A_-` control. It is not a derived universal model class. For stationary Killing observers,

\[
\phi_{\rm pair}=\frac12\log\frac{A_r}{A_s}\to+\infty
\]

as `x_s->2^-`. This is a stationary asymptote candidate, not physical `X_max`. The one-sided radial
proper length is finite but receiver dependent.

With every AM angular/mixing profile active, the registered path census was `516` endpoint-
regular/no-sampled-caustic, `18` turning, and `57` affine-cap rows. The latter two are bounded
statuses, not physical exclusions. The common lapse behavior therefore does not erase
orchestra-dependent path accessibility.

### G84 — conditional global completion

With `x=2 sin(chi)`, the AM spatial metric becomes a round three-sphere metric of radius `2R` on a
minimal doubled simply connected completion candidate. The zero-mixing spacetime extends to a
smooth constant-curvature Lorentzian hyperboloid. Recentered central geodesic stationary observers
share the conditional patch law

\[
\phi(s)=-\log\cos\frac{s}{2R},
\qquad
\frac{c_{\rm eff}}{c_E}=\cos^2\frac{s}{2R},
\]

with divergence at `s->pi R`. This covers a conditional observer class, not arbitrary observers,
and `pi R` is not the completed spatial diameter. The 196 nonzero-mixing stationary doubled
extensions are degenerate on the axial fixed subset in that restricted extension class.

### G85 — mixed time-live completion classes

Allowing other complete metric channels repairs the restricted obstruction. Near the candidate
seam the declared block is

\[
\begin{aligned}
ds^2/R^2={}&u\,d\tau^2+2b\,d\tau d\chi+4d\chi^2
+D\,d\theta^2+C\,d\psi^2+2H\,d\tau d\psi,\\
D={}&4\sin^2\chi,\qquad C=D\sin^2\theta,\qquad
H=h_{\rm mix}\sin^2\theta.
\end{aligned}
\]

The axial clock-radial determinant and induced-seam determinant are

\[
\det G_H=4u_H-b_H^2,
\qquad
\det(g_{\rm seam}/R^2)=D(u_H C-H^2).
\]

These equations, not a merit criterion, distinguish the seam types. The exact axial regularity
gate is

\[
4u_H-b_H^2<0.
\]

Retaining the stationary germ or making only the mixing time-dependent leaves `392`
profile/archetype rows pointwise degenerate. All `196` mixed profiles nevertheless admit several
constructed smooth witnesses when other complete metric channels are allowed:

- clock-radial shift support preserves the lapse-zero candidate but gives a seam timelike off axis
  and null on the axial subset;
- negative clock-norm lift gives a timelike seam and removes the lapse-zero candidate there;
- sufficient mixing taper can give a uniformly null seam, subject to regular completion-chart
  conditions.

These are kinematic completion classes. They are not on-shell solutions or selected regimes.
Here completion means smooth, nondegenerate complete-tensor witnesses on the declared candidate;
geodesic and global causal completeness were not proved.

### G86 — ownership result

Across 21 frozen sources, 14 current conditions, three regular G85 classes, and 42 condition-family
cells, two conditions distinguish geometric properties but zero own a physical exclusion or
nonidentity selector. Current `X_max` semantics do not identify this seam with physical `X_max` or
require uniform nullness.

The exact landing is:

```text
NO_EXISTING_OWNED_CONDITION_DISTINGUISHES_THE_THREE_G85_REGULAR_FAMILIES.
```

G86 is an internally verified, source-bounded ownership result with fresh external semantic review
still pending. G83--G85 are externally reviewed with their stated caveats.

## 11. Current premise inventory

| object | grade | exact boundary |
|---|---|---|
| reciprocal `c_E` conversion identity | foundational proposal / observed calibration | not a route or dynamics |
| dual reciprocal character on supplied depth | `DERIVED` | physical depth assignment open |
| local spherical founding metric readout | `CONDITIONAL/DECLARED` | complete extension not unique |
| complete ten-component coframe chart | `DEFINED_CONDITIONAL_CONFIGURATION_CHART` | finite-jet open on the supplied regular split; not on-shell |
| `phi_pair` from a supplied calibrated pair metric | `DERIVED_CONDITIONAL` | query/immersion owner open |
| terminal `c_eff^(pair)/c_E=e^{-2phi_pair}` | `DERIVED_CONDITIONAL` | not local signal speed |
| co-presence | `WORKING_SEMANTICS` | no signalling or selector |
| `X_max` asymptotic frame | `WORKING` | realization, value, and all-frame theorem open |
| SNe P1 fit | `OBSERVED_CONDITIONAL_COMPATIBILITY` | not a metric derivation or selector |
| CMB Jacobi/screen response | `DERIVED_CONDITIONAL_ON_QUERY` | observable/source law open |
| 591-profile stationary axial atlas | `CHOSE_CONTROL` | not physical cosmology |
| AM continuation and doubled S3 | `FREE_AND_EXPLORED/CONDITIONAL` | not universal completion |
| G85 regular completion classes | `DERIVED_KINEMATIC_WITNESSES` | no native history selection |
| action, source, matter, mass, bootstrap return | `OPEN` or `WORKING_HYPOTHESIS` | inactive as selectors here |

## 12. Is the work linear or circular?

### The strongest linear reading

The arc is linear as a type-correction and conditional-geometry program. It has successively:

1. placed `phi` in a relational rather than arbitrary-pointwise role;
2. made `c_E` the terminal calibration rather than a path selector;
3. included the complete angular/mixing orchestra;
4. distinguished endpoint, shift, Jacobi, and holonomy channels;
5. separated geometric response from source population;
6. built center-safe global-sky controls;
7. joined redshift and area response on one geometry;
8. separated `X_max`, chart horizon, seam, and spatial diameter; and
9. proved that existing premises do not select among three regular continuation classes.

Those are cumulative results and remove category errors.

### The strongest rabbit-hole reading

The G83--G86 subprogram is ansatz-conditioned. AM was entered because it was the sole explored
stationary lapse continuation with the desired positive zero. Its formula was extended beyond the
owned domain; a doubled topology was then considered; completion repairs were constructed; and
existing principles were asked to select among them.

That is legitimate characterization of a witness. It is not a deduction that the physical
relation realizes `X_max` at this lapse zero. Further seam drilling would repeatedly rediscover
underdetermination because the founding does not select either the ambient history or the complete
observer relation.

### Adjudication

Both readings are true at their stated levels:

```text
LINEAR_TYPE_CORRECTION_AND_CONDITIONAL_GEOMETRY
BUT
EXHAUSTED_AM_SEAM_SELECTION_PROGRAM.
```

## 13. The whiteboard's proposed object

Let `H` denote candidate complete metric histories. For each history `g`, let `Q_g` be the
class/category of admissible ordered observer/event queries. For `Q` in `Q_g`, let `R_g(Q)` be the
possibly set-valued family of regular realizations, including branch and route labels. The neutral
typed total space is

\[
\mathcal C=\{(g,Q,F):g\in\mathcal H,\ Q\in\mathcal Q_g,\ F\in\mathcal R_g(Q)\}.
\]

The metric evaluates a typed member of this total space:

\[
(g,Q,F)\mapsto h_F=F^*g
\mapsto
(\kappa,\phi_{\rm pair},\beta,
\{\text{channels defined for the query class of }F\}).
\]

A history owner selects or restricts `H`. A relation owner supplies a natural, possibly set-valued
assignment `Q -> R_g^phys(Q)`. A joint selector may constrain both, but their ownership obligations
remain distinct. Current evidence derives the evaluation arrows. It does not derive a physical
subspace of `C`, a natural choice `g -> F_g in R_g(Q)`, a natural physical subfamily
`R_g^phys(Q)`, or a unique physical history subset of `H`.

Three architectures remain open:

1. **factorized history-first:** a native law selects `g`, then query semantics returns the lawful
   relation family for each admissible query on that history;
2. **joint relational:** one nonidentity global condition selects compatible `(g,Q,R_g(Q))`
   families;
3. **kinematic framework plus added physics:** the current structure is a relation/evaluation
   framework and requires an explicitly new action, global law, or postulate for physical
   selection.

The tempting claim that history ownership and query ownership are one object is not derived. The
equally tempting strict order `select g, then F` is also not derived. A joint constraint may or may
not factorize.

The registered G85 seam properties differ invariantly under seam-preserving identifications. Full
equivalence under all allowed global diffeomorphisms, query relabellings, and completion-chart
changes has not been classified. They may nevertheless be connected strata in one larger off-shell
completion arena. Connectedness would weaken discrete-branch rhetoric but would not confer
physical equivalence or selection.

## 14. Mutually exclusive next programs

### Program A — object-type/factorization audit (recommended first)

Without a solve, define `H`, `Q_g`, `R_g(Q)`, and all relevant equivalences. Ask whether current
foundations own a natural relation family for every history/query, any nonidentity restriction on
histories, or any joint condition on `(g,Q,F)`.

**Yes return:** an existing premise yields a real, nonidentity restriction rather than an identity
or definition.  
**No return:** all proposed restrictions reduce to supplied query data, coordinate/gauge choice,
regularity, or an unowned condition.

### Program B — query-first invariant Xmax test

Define the `X_max` gate directly on pair metrics and relation sequences, including reversal,
re-centering, route labels, and multiple observers. Only afterward test whether any manifold seam
represents it.

**Yes return:** an invariant classification, including a possible proof of nonselection, is
obtained without presupposing AM.  
**No return:** the conditions merely restate divergence or require a supplied separation law.

### Program C — one same-history SNe/CMB commuting diagram

Supply one global control history and one explicitly declared common calibrated relation
architecture—or one actually owned by Program A—then evaluate its low-redshift and observer-sky
projections before comparison with P1 or CMB data.

**Yes return:** a definite cross-query compatibility or independence relation is derived.  
**No return:** independent query/profile/source inputs survive, showing that the control does not
close the global relation.

### Program D — justified owner-source scope expansion

If Program A finds no owner in the current source spine, determine whether that is a result about
the theory or only about the bounded corpus. Expand authority only through an explicit,
outcome-independent source rule.

**Yes return:** a wider controlling source supplies an already-owned restriction.  
**No return:** no owner is found in the justified expanded scope.

### Program E — explicitly add and test one new selection premise

Only if Programs A and D find no owned implication, state the smallest new postulate explicitly
and derive its consequences. Possible *types* include a global relational consistency law, an
action-first law, or a bootstrap-style mutual admissibility return. No formula is proposed here.

**Yes return:** the postulate cuts the open history/relation arena, survives observer covariance,
and has independent falsifiers.  
**No return:** it merely names the desired branch, inserts a fit, or restates regularity.

Programs B--D should not start before Program A establishes which object is actually missing.
Program E additionally requires Program D.

## 15. Cold external-review task

Starting only from the mathematics and status ledger above, perform a hostile reconstruction.
Do not assume UDT is correct and do not import GR field equations, Lambda-CDM dynamics, standard
CMB source physics, an action, a preferred congruence, or bootstrap as an affirmative law.

Return exactly one primary landing, or define a sharper one:

```text
LINEAR_PROGRAM__FACTORISATION_AUDIT_NEXT
CONDITIONAL_AM_WITNESS_PROGRAM_EXHAUSTED__GENERAL_OWNER_UNRESOLVED
DECLARED_SOURCE_UNIVERSE_HAS_NO_OWNER__WIDER_SOURCE_OR_NEW_PREMISE_DECISION_OPEN
FOUNDING_ALREADY_IMPLIES_A_MISSING_RELATION_RULE
UNIVERSAL_SELECTION_IS_A_CATEGORY_ERROR__RETURN_RELATION_FAMILIES
EVIDENCE_UNDERDETERMINES_THE_PROGRAM_ARCHITECTURE
INCONSISTENT_FOUNDATION_OR_TYPE_CHAIN
OTHER_PRECISE_LANDING
```

Required tasks:

1. Reconstruct every implication from the reciprocal `c_E` identity to `D(delta)` and the founding
   metric. Identify every premise beyond the two named postulates.
2. Decide whether the move from the founded two-channel/spherical metric to the ten-component
   complete coframe is a lawful configuration-space completion, an unowned enlargement, or both.
3. Identify the earliest open arrow that prevents physical prediction.
4. Determine whether history ownership and observer-relation ownership must factorize, may be
   selected jointly, or are category-distinct forever.
5. Determine whether physical coverage requires all admissible ordered queries, one operational
   query class, a set-valued family, or another structure.
6. Determine whether current evidence selects a mathematical home for `X_max`; if not, state the
   exact nonselection among spacetime, relation-space, and global-admissibility interpretations.
7. Adjudicate whether G83--G86 is a productive witness program or target-led drift, and identify the
   exact step where its conclusion ceiling became fixed.
8. Determine whether the SNe and CMB channels can constrain a joint history/relation law without
   being promoted from compatibility/readout to derivation.
9. If an additional premise is necessary, give its smallest mathematical type and falsification
   criterion. Do not invent a convenient formula unless it follows uniquely.
10. Give one bounded next calculation or no-solve audit that can return a genuine negative as well
    as a positive.

A finding of an existing implication, no owner in the declared scope, a category error, an
inconsistent chain, or genuine underdetermination is equally valuable. The review is not graded by
closure or by requiring a new premise.

## 16. Hard guards for reviewers

- `c_E` is an observed clock/ruler calibration, not a route or history selector.
- `c_eff^(pair)` is a conditional terminal readout, not automatically local signal speed.
- Co-presence is whole-solution membership, not instantaneous communication.
- `X_max` is not already a material wall, seam, horizon, spatial diameter, or numerical constant.
- The SNe P1 fit is a conditional compatibility anchor, not the physical profile owner.
- The 591 G75 geometries and AM continuation are chosen controls.
- G85 time-live completions are kinematic witnesses, not on-shell histories.
- Regular invertible CMB response does not by itself populate TT/TE/EE/BB power.
- The round `S^2` matter carrier, complete action, source, mass law, and bootstrap return remain open
  and are outside this consultation.
- Do not revive strong local CSN or claim the active physical metric is scale-free.
