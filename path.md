# UDT observer-relation and path-selection problem

Cold external review brief — 2026-08-11

Status: **OPEN REVIEW QUESTION, NOT A UDT RESULT**

## 0. Why this document exists

UDT has recently eliminated several category errors and has derived a substantial amount of
coherent metric structure. Yet one question keeps returning in different clothing:

> Given two observers in the complete UDT geometry, what determines their physical comparison?

This has often been phrased as a request for a **preferred path**, a physical non-isometric arrow,
or a universal scalar observer-pair law. That phrasing may be correct. It may also be the remaining
category error.

The latest solved-geometry atlas shows that endpoint reciprocal depth, timelike/spacelike ambient
geodesic and numerical differential-of-exponential-map data, full-frame path holonomy, and angular
normal-bundle holonomy can all survive simultaneously. They need not be rival definitions of one
number. A serious alternative is that they are different parts of one complete observer-pair
relation, perhaps organized by one pair immersion or correspondence.

This brief asks a cold reviewer to reconstruct the problem from the beginning and determine the
correct mathematical object. It must not assume that UDT needs one preferred path, one scalar, one
physical branch, or one universal route policy.

## 1. Epistemic rules

1. The metric is the theory. Do not import GR field equations, an Einstein-Hilbert action,
   Standard Model dynamics, quantum mechanics, fluids, statistical weights, or a preferred
   congruence as affirmative UDT physics.
2. Standard differential geometry, topology, groupoids, submanifold theory, causal geometry, and
   exact algebra may be used to analyze what the supplied structures imply.
3. External mathematical theorems may identify a proof, obstruction, or counterexample. They do
   not become UDT postulates merely because they are familiar.
4. Keep `DERIVED`, `CONDITIONAL`, `OBSERVED`, `WORKING`, `POSIT`, `CHOSE`, and `OPEN` separate.
5. Do not select a branch because it resembles GR, a particle, a cosmology, or a desired answer.
6. Co-presence is not material signalling. A metric null cone is not automatically the
   characteristic cone of a field equation that has not been derived.
7. `c_E` is an observed clock-length calibration anchor, not a path, branch, simultaneity, or
   dynamical selector.
8. `X_max` is presently a working observer-pair positional-dilation asymptote. It is not a material
   wall, preferred center, route selector, or known numerical constant.
9. Strong local Common-Scale Neutrality is inactive. The physical metric is not currently treated
   as scale-free; `c_E` and observed `G` remain anchors.
10. Bootstrap is a working global/local self-consistency hypothesis. Do not activate it to select
    a relation in this review.

## 2. Founding premises and the first metric

### 2.1 Reciprocal-`c_E` identity

The first physical proposal is:

> The measured constant `c_E` is the reversible identity between temporal and spatial measure.
> Its directions `L=c_E T` and `T=L/c_E` are equally fundamental. It is not conceptually primary
> as a one-way material signal speed.

Use the dimension-matched clock/ruler coframe pair

```text
q=(c_E dt, dr)^T.
```

### 2.2 Two meanings that must be distinguished

The project also uses **observer-frame Reciprocity**: no admissible observer is a preferred frame;
the same comparison law applies covariantly under exchange of observer roles. This requires
neutral self-comparison, reversal covariance, and matched composition. By itself, it is not
obviously identical to the clock/ruler duality below.

The founding metric derivation interprets **dual clock/ruler Reciprocity** as a contragredient
action on the two directions of the `c_E` conversion pair. The banked premise ledger calls this a
`FOUNDATIONAL_INTERPRETATION`:

Positional comparison acts contragrediently on the two directions of that clock/ruler pair. If

```text
P(Delta)=diag(u(Delta),v(Delta)),  u,v>0,
K=[[0,1],[1,0]],
```

then dual Reciprocity is represented by

```text
P(Delta)^T K P(Delta)=K.
```

Therefore

```text
u(Delta)v(Delta)=1.
```

This inverse relation is not derived from the arithmetic existence of `1/c_E` alone. If reversible
conversion were interpreted only as ordinary intertwining covariance, it would give `u=v`, not
`uv=1`. Dual/contragredient Reciprocity is doing independent foundational work.

An external reviewer must decide whether no-preferred-observer/frame Reciprocity actually implies
this contragredient clock/ruler action, whether both are two faces of one precise postulate, or
whether the metric derivation presently contains a third interpretive premise. Do not silently
merge them merely because both use the word “Reciprocity.”

### 2.3 Positional relativity and composition

Only relative positional depth matters. Regular comparisons compose and reverse:

```text
P(Delta_2)P(Delta_1)=P(Delta_1+Delta_2),
P(-Delta)=P(Delta)^-1.
```

Continuity or measurability and nontriviality give, after choosing the sign and unit of the
additive coordinate `phi`,

```text
D(phi)=diag(exp(-phi),exp(+phi)),
D(phi_2)D(phi_1)=D(phi_1+phi_2),
D(-phi)=D(phi)^-1.
```

The trivial `phi=0` representation remains mathematically allowed; nonzero realized dilation is
observational input.

### 2.4 Declared local metric readout

With a local Lorentzian quadratic interval and spherical areal angular sector supplied as inherited
local metric structure,

```text
ds^2=-(u c_E dt)^2+(v dr)^2+r^2 dOmega^2,
```

the reciprocal character gives

```text
ds^2=-exp(-2phi)c_E^2 dt^2+exp(+2phi)dr^2+r^2 dOmega^2.       (1)
```

Equation (1) is the founding static/spherical reciprocal metric family. The Lorentzian quadratic
readout, spherical areal sector, continuity, and nontriviality are explicit premises; it is
inaccurate to claim that the number `c_E` alone derives the entire metric.

Direct consequences include

```text
det D=1,
det g_(t,r)=-c_E^2,
sqrt(-g)=c_E r^2 sin(theta),
J=D^-1 dD=diag(-dphi,+dphi),
(1/2)Tr(J^2)=dphi^2.
```

The one-dimensional reciprocal group has a canonical quadratic tangent norm up to normalization.
This does not select a physical action or field equation.

## 3. What the founding derivation actually owns

The derivation begins with an **already supplied ordered relative depth** `Delta`. Its exact logical
type is

```text
supplied ordered signed depth delta
    -> D(delta)=diag(exp(-delta),exp(+delta))
    -> exact composition, reversal, and reciprocal exchange.
```

It is not yet

```text
bare observers/events
    -> event pairing, pair surface, path, branch, or relation
    -> delta.
```

Thus the foundation owns the reciprocal character and its relational type. It does not yet own the
map from complete observer/query data to a numerical depth.

Pointwise `phi(x)` is not automatically a universal physical scalar. On branches where a complete
relation descends endpoint-exactly, it can be a potential representation and

```text
delta_AB=phi(B)-phi(A).
```

On a supplied factorized coframe, reciprocal refactorizations can change pointwise `phi` while
leaving the complete coframe fixed. The invariant founding object is the ordered relational
character, not a preferred global zero or arbitrary pointwise representative.

The signed arrow coordinate and physical separation magnitude are also different types:

```text
delta(B,A)=-delta(A,B),
rho(B,A)=rho(A,B)>=0.
```

One nonzero scalar cannot obey both rules. A complete observer relation may therefore need a
nonnegative magnitude together with an oriented reciprocal lift. Neither their join nor a
universal pointwise potential has yet been derived.

The phrase **positional dilation** should be taken seriously: UDT may be saying that physical
distance is operationally constituted by the clock/ruler comparison rather than that dilation is
attached after an independently known distance has been supplied.

## 4. The complete regular metric arena

The static spherical form (1) is not the complete local metric chart used in the recent work. On a
regular pair-adapted reciprocal/angular split, write the full coframe matrix as

```text
E=[[B,   0],
   [Q S, Q]],                                                (2)

B=[[T,T beta],
   [0,L]],

T=exp(kappa-phi),
L=exp(kappa+phi).
```

Here

- `kappa` is common clock/ruler scale;
- `phi` is reciprocal clock/ruler imbalance;
- `beta` is the clock-ruler shift/query-state coordinate; event pairing can affect it, but it does
  not encode the full pairing;
- `Q` is a general invertible two-dimensional angular coframe;
- `S` is a general `2 x 2` reciprocal-angular mixing field.

The induced metric blocks are

```text
g_base   =B^T eta_(1,1) B+S^T Q^T Q S,
g_cross  =S^T Q^T Q,
g_screen =Q^T Q.                                      (3)
```

Conditional on the regular split and positive screen, this covers all ten independent local metric
components after the one angular frame-presentation freedom is removed. It does not freeze the
angular sector or append an angular correction to `phi` afterward. Angular and mixing geometry are
already inside the complete metric.

Every entry of `B,Q,S` may depend on time and all spatial coordinates. Define

```text
K=dE E^-1=[[P,0],[C,R]],
P=dB B^-1,
R=dQ Q^-1,
C=Q dS B^-1,

P=[[d kappa-d phi, exp(-2phi)d beta],
   [0,               d kappa+d phi]].                (4)
```

The exact compatibility identities are

```text
dP-P wedge P=0,
dR-R wedge R=0,
dC-C wedge P-R wedge C=0.                            (5)
```

They show that the reciprocal, angular, and mixing instruments are coupled parts of one smooth
coframe. But (5) is a Maurer-Cartan identity obeyed by every smooth regular coframe movie. It is not
an equation of motion and selects no frequency, trajectory, characteristic, or physical regime.

## 5. The terminal observer-pair readout

The strongest current local geometric object is a regular calibrated pair immersion

```text
F:Sigma -> (M,g),
h=F^*g.                                                (6)
```

The immersion is the two-dimensional tape/congruence, not yet one A-to-B comparison. An actual
comparison also identifies the relevant curves, sections, or paired points in `Sigma`. At caustics
or cut loci a single immersion may need replacement by a correspondence or branch atlas. These
types must not be silently interchanged.

Use A-calibrated coordinates

```text
y^0=c_E tau_A,
y^1=s_A,
```

where `tau_A` is A's proper clock parameter and `s_A` is A's calibrated ruler parameter. For pair
tangents `J_i=F_*(partial_i)` and complete coframe `theta^a`,

```text
V_i^a=theta^a(J_i),
h_ij=eta_ab V_i^a V_j^b.                              (7)
```

Equation (7) makes the full angular and mixing orchestra act **before** the scalar readout.

On the regular Lorentzian pair stratum

```text
h_00<0,
det h<0,
```

there is a unique positive clock/ruler/shift decomposition

```text
h=-T^2(dy^0+beta dy^1)^2+L^2(dy^1)^2,

T^2=-h_00,
beta=h_01/h_00,
L^2=h_11-h_01^2/h_00,
TL=sqrt(-det h).                                      (8)
```

Writing

```text
T=sigma exp(-phi_pair),
L=sigma exp(+phi_pair),
```

gives the exact readouts

```text
kappa_pair=log sigma=(1/4)log(-det h),

phi_pair=(1/2)log(L/T)
        =(1/4)log[(-det h)/h_00^2],

beta_pair=h_01/h_00.                                 (9)
```

The conditional terminal calibration is

```text
c_eff^(pair)/c_E=T/L=exp(-2phi_pair).                 (10)
```

Equation (10) does not redefine `c_E` and is not a material signalling law. It is the completed
clock/ruler ratio on a supplied A-calibrated pair metric. `c_E` is the end of this computation, not
the beginning: it calibrates the tape but does not select its event pairing, direction, embedding,
path, branch, or global continuation.

## 6. Why the pair relation is still not owned

An ordered pair `(A,B)` fixes source and target. In groupoid language it identifies

```text
Hom(A,B),
```

but does not generally select one member of that set. Reciprocity maps the family to
`Hom(B,A)` by reversal; it does not prove that the groupoid is thin.

The metric supplies a strong local conditional construction after a complete observer query is
given. If the query supplies A's worldline `z_A(y)`, proper clock, A-orthogonal unit ruler field
`n(y)`, its evolution, event-intersection rule, and a regular exponential branch, then

```text
F(y,s)=Exp_{z_A(y)}[s n(y)]                            (11)
```

is metric-natural locally. Its Jacobian columns are Jacobi fields. At a conjugate point the
Jacobian loses rank; at a cut locus several branches may reach the same endpoint. The metric
naturally supplies the branch atlas, not necessarily a preferred member.

The choices are not merely coordinate gauge. In flat `1+1` geometry, fixed worldlines

```text
z_A(y)=(y,0),
z_B(v)=(v,L)
```

admit the calibrated family

```text
F_k(y,s)=(y+k s/L,s),

h_k=[[-1,-k/L],[-k/L,1-k^2/L^2]],
det h_k=-1.                                           (12)
```

Different `k` values pair different events while all return `phi_pair=0`. Neither `c_E` nor the
terminal depth reconstructs the event pairing.

Likewise, two distinct rotating ruler embeddings can induce the same pair metric. Thus even `h`
does not in general reconstruct the complete embedding or observer protocol.

## 7. Transport is not reciprocal depth

Levi-Civita and other metric-compatible transports preserve the endpoint Lorentz Gram data:

```text
P_gamma^dagger P_gamma=I.
```

Therefore their reciprocal-root clock/ruler density character is zero. They can still carry
nontrivial Lorentz/frame holonomy. What they cannot do is manufacture the nonzero reciprocal
density imbalance of a supplied pair relation by norm change under isometric transport.

This is one reason earlier searches for a universal non-isometric tangent-bundle connection
stagnated. The required object may not be a connection on the ambient tangent bundle at all.

A related no-go applies to an overlarge arrow arena. Let

```text
S_t=diag(exp(-t),1,1,1),
J=[[0,-1],[1,0]] direct_sum I_2.
```

Direct multiplication gives

```text
S_t J S_t^-1 J^-1=diag(exp(-t),exp(+t),1,1)=D_t.
```

Thus the pure reciprocal matrix is a commutator in `GL^+(4)`. Every real additive group character
vanishes on commutators, so no arrow-only character on the full general-linear group can assign
`D_t -> t` universally. This does not refute the UDT character on correctly typed supplied depths.
It refutes treating every invertible four-dimensional linear map as one physical comparison
group.

## 8. The R17 global branch: a concrete complete example

On the supplied regular stationary R17 completion `R x S^3`, use

```text
theta0=u^-1(dt+a sigma3),
theta1=u sigma3,
theta2=v sigma1,
theta3=v sigma2,

u=exp(phi),
v=exp(lambda phi).                                   (13)
```

Here `phi` is a smooth stationary field, `a` is the supplied nonzero twist coefficient, and
`lambda` labels the supplied screen-scaling family. The left-invariant `SU(2)` coframe convention
is

```text
d sigma1=-2 sigma2 wedge sigma3,
d sigma2=-2 sigma3 wedge sigma1,
d sigma3=-2 sigma1 wedge sigma2,
```

with dual fields `(Z,X,Y)` satisfying

```text
[X,Y]=2Z,  [Y,Z]=2X,  [Z,X]=2Y,
```

and `T` dual to `dt`. The orthonormal frame is

```text
e0=u T,
e1=u^-1(Z-aT),
e2=v^-1 X,
e3=v^-1 Y.
```

The intrinsic clock/twist-ruler distribution is

```text
E_pair=span(T,Z),
```

and is globally integrable. Its leaves are Hopf cylinders

```text
R x S^1,
```

foliating the spacetime over `S^2`. The angular screen

```text
H=span(X,Y)
```

is a positive rank-two normal bundle and is nonintegrable; on each spatial `S^3` it is the Hopf
contact plane.

Every reciprocal leaf has induced metric

```text
h=-u^-2(dt+a dpsi)^2+u^2 dpsi^2,
det h=-1.                                             (14)
```

The terminal evaluator gives

```text
phi_pair=phi,
delta_K(p,q)=phi(q)-phi(p).                           (15)
```

Thus R17 conditionally owns a global endpoint scalar. It also owns a metric-projected normal
connection

```text
D_W s=P_H(nabla^LC_W s),
```

and hence path-labelled normal transport

```text
U_gamma:H_p->H_q.                                    (16)
```

In the oriented local normal frame `(e2,e3)`, writing

```text
p1=Z(phi), p2=X(phi), p3=Y(phi),
```

the projected normal connection has representative

```text
A(e0)=a/(u v^2),
A(e1)=2/u-u/v^2,
A(e2)=-lambda p3/v,
A(e3)=+lambda p2/v,                                  (16a)
```

for the displayed Maurer-Cartan sign convention. The full verified curvature has leafwise,
mixed, and horizontal components and is generically nonzero. Its detailed second-jet formulas are
in the attached R17 connection source; do not claim to have independently recomputed them from
this brief alone.

The exact joint supplied-path object is

```text
J_gamma=(delta_K(p,q),U_gamma).                       (17)
```

Endpoint depth is exact while normal transport can retain loop holonomy. For two endpoints on the
same Hopf fiber, the intrinsic reciprocal leaf is available. Cross-leaf comparisons must leave
that leaf; the branch does not select one cross-leaf path. Different windings can share the same
endpoint scalar and differ in holonomy.

This is not a defect in composition. It is ordinary coexistence of endpoint and path-labelled
data.

## 9. The minimal multichannel assembly currently known

On one supplied regular calibrated pair relation, the banked data separate by type into

```text
kappa      common-scale endpoint density,
phi        reciprocal endpoint density,
beta       pair-metric shift/query-state coordinate,
U_gamma    angular normal transport on a supplied path.          (18)
```

Matched endpoint density differences compose additively:

```text
Delta_kappa_20=Delta_kappa_21+Delta_kappa_10,
Delta_phi_20=Delta_phi_21+Delta_phi_10.               (19)
```

`beta` is a state coordinate, not a free additive character. `U_gamma` composes in the normal
isometry groupoid, not in the real numbers:

```text
U_(gamma2 o gamma1)=U_gamma2 U_gamma1.                (20)
```

Before reciprocal projection, the matched endpoint-density factor is two-dimensional:
`(Delta_kappa,Delta_phi)`. Among its continuous real characters that are odd under the founded
clock/ruler exchange and normalized by a pure reciprocal comparison, `Delta_phi` is unique.
Separately, compact `SO(2)` contributes no nontrivial continuous real additive character. These
limited theorems neither erase `Delta_kappa` from the complete pair state nor erase the angular
channel.

## 10. Complete observer networks

There are two exact network homes.

### 10.1 Endpoint-descended atlas

For supplied object potentials,

```text
delta_ij=phi_j-phi_i
```

and every matched triangle closes identically.

### 10.2 Path-labelled family

For genuinely path-labelled antisymmetric edge data `e_ij`, face periods and angular/full-frame
holonomy may be nonzero while composition and reversal remain exact. The four-face identity is
boundary-of-boundary/Bianchi bookkeeping; it does not force each face return to vanish.

Requiring every direct relation to equal every composite route is a genuine flat-descent
restriction. No current UDT premise owns that condition universally. Imposing it merely to obtain
a simple scalar would delete geometric curvature information.

Therefore route policy cannot be selected before the physical relation/query is correctly typed.
A clock-depth question may be endpoint-descended while an orientation-memory question remains
path-labelled.

## 11. Latest solved-geometry observation

The preregistered numerical G63 atlas integrated Levi-Civita geodesics, parallel transport,
numerical differential-of-exponential-map/Jacobi data, and R17 normal transport on fourteen
bounded metric witnesses. It retained all signs and zero controls.

Observed results:

```text
14/14 endpoint pair constructions regular;
28/28 timelike/spacelike numerical differential-of-exponential-map propagators regular at affine endpoint 0.4;
28/28 declared loops with nonidentity Levi-Civita holonomy;
18/18 R17 normal-holonomy evaluations nonzero;
56/56 independent numerical comparisons passed.
```

The stationary R17 samples cover

```text
lambda=-1,0,+1,
epsilon=-0.12,0,+0.12.
```

The complete local time-live samples cover

```text
epsilon=-0.15,-0.075,0,+0.075,+0.15,
```

with `kappa,phi,beta,Q,S`, all four coordinates, and time dependence active. The time-live family is
explicitly local and off-shell; no native evolution equation was supplied.

The correct landing was

```text
MULTIPLE_GEOMETRIC_SURVIVOR_FAMILIES.
```

This is bounded geometric persistence, not physical selection or dynamical stability.

The counts above are supplied verified evidence. A browser-only reviewer receiving `path.md` alone
does not have the fourteen witness definitions, initial data, loops, tolerances, or saved arrays
needed for an independent numerical replay. Do not claim such a replay unless the complete G63
package is also attached.

## 12. A possible hidden-in-plain-sight joint

The four G63 channels were computed on common metric witnesses, but not all of the declared
geodesics and loops were generated as parts of one common observer-pair immersion. Correlating
their numerical values prematurely could therefore correlate different questions.

A sharper hypothesis to test is:

> Endpoint reciprocal depth, timelike/spacelike ambient geodesic and numerical
> differential-of-exponential-map data, ambient holonomy, and angular normal
> holonomy are not instruments awaiting arbitrary mixing coefficients. Once a complete calibrated
> pair immersion `F:Sigma->M` is supplied, they may be related pieces of its intrinsic metric,
> variation/Jacobi geometry, tangent or ambient connection, and normal connection.

This is a **lead only**. In particular, a Jacobi propagator is not automatically a second
fundamental form, and an arbitrary ambient loop is not automatically a loop in or canonically
associated with `F(Sigma)`. The exact relationship must be constructed and type-checked.

Use a declared sign convention beginning with

```text
nabla^M_X Y = nabla^Sigma_X Y + II(X,Y),
nabla^M_X xi = -A_xi X + nabla^perp_X xi.             (21)
```

The Gauss equation should then be checked in the form

```text
<R^M(X,Y)Z,W>
 =<R^Sigma(X,Y)Z,W>
  +<II(X,W),II(Y,Z)>-<II(X,Z),II(Y,W)>,               (22)
```

with the corresponding Codazzi identity for `nabla II` and Ricci identity relating normal
curvature to ambient curvature and the commutator of shape operators. Intrinsic Jacobi evolution
depends on `R^Sigma`; ambient Jacobi evolution depends on `R^M`; tangent and normal holonomies are
generated by their respective curvature blocks; `II` links those blocks. Global finite-loop
holonomy can still retain topology and path ordering not exhausted by the local identities.

The first move must be adversarial. Try to construct two fully typed immersions with the same
induced pair metric and endpoint depth but inequivalent second fundamental form, normal connection,
or holonomy. Do not infer that one immersion uniquely fixes every channel merely because all
channels can be represented on it. Gauss-Codazzi-Ricci can relate correctly co-typed channels; it
cannot select the immersion, observer query, or route.

The question is whether applying (21)--(22) and the companion identities to one fully specified UDT
pair query turns the apparently loose channel pile into one coherent machine—or proves that
genuinely independent data remain.

## 13. Competing interpretations to adjudicate

Do not assume one in advance.

### A. Preferred path is derived

The complete metric plus founding ordered observer semantics canonically selects one path or pair
surface, including at global branch points.

### B. Relation-first, query-conditional

The founding word “comparison” presupposes an operational query. A complete query supplies the
observer germ, event pairing, ruler evolution, requested output, and branch policy; the metric then
constructs the geometry. No path is expected from bare endpoints.

### C. Branch-valued metric relation

The metric naturally returns all admissible regular branches. A physical answer is a
branch-labelled relation or set, not one selected member.

### D. Multichannel path groupoid

Endpoint depth and path memory are both physical, correctly typed components. Different questions
have different route policies; no universal preferred path exists.

### E. Global/on-shell completion is logically prior

Local kinematics cannot decide the relation. A still-missing native global or on-shell rule selects
the physical observer family and only then determines its route semantics.

### F. Genuine underdetermination requiring one small premise

The current foundations are insufficient, and UDT needs an explicit operational observer-query
postulate. If so, identify the smallest statement and prove that it is not already implicit.

These possibilities can coexist by branch or regime only if the metric or query typing actually
derives that stratification. Do not assign micro, terrestrial, or cosmological labels by intuition.

## 14. Required cold-review tasks

### Task 1 — reconstruct and type-check

Reconstruct the implication chain from Reciprocal-`c_E`, dual Reciprocity, composition, and local
metric readout. List every premise. State precisely what is a point, observer, event, ordered query,
pair relation, pair immersion, path, branch, endpoint state, and output channel.

Independently adjudicate whether observer-frame/no-preferred-frame Reciprocity implies the
contragredient clock/ruler law, or whether the latter is a distinct foundational interpretation.
Give the strongest proof and strongest counterexample.

### Task 2 — adjudicate the preferred-path question

Determine whether the physical UDT problem mathematically requires a unique path from bare
observer endpoints. Prove your answer. Separate:

- existence of a comparison;
- selection of a member of `Hom(A,B)`;
- covariance under observer exchange;
- event pairing;
- causal admissibility;
- local normal-neighborhood uniqueness;
- cut-locus and global branch multiplicity;
- route-dependent holonomy;
- measurement/output-channel choice.

Do not infer uniqueness from the word “ordered,” Reciprocity, `c_E`, or local exponential-map
uniqueness.

Also test for circularity: if reciprocal positional depth operationally constitutes physical
distance, would deriving it from a pre-existing geodesic distance or preferred path assume the
object being derived? Determine whether the metric can instead return a causally admissible set of
event pairings without selecting a curve, and whether that is already a complete answer for some
queries.

### Task 3 — test whether the complete query is implicit

The founding source says “a positional comparison at relative depth.” Decide whether this already
means that a full operational comparison protocol is primitive, or only that an abstract depth has
been supplied. Determine which, if any, of these are contained in the two physical postulates:

```text
observer worldline,
proper clock,
ruler germ and its evolution,
event pairing,
causal relation,
pair surface or correspondence,
path/path class,
cut-locus branch policy,
requested measurement channel,
middle-observer calibration carry.
```

If the source does not own them, state the smallest operational premise needed. A pair-relative
query must not be turned into a global preferred congruence.

After declaring a supposedly complete protocol, attempt to construct two inequivalent pair
relations that satisfy it. If both survive, identify the exact datum still omitted. Prove that
A-calibrated query coordinates reverse covariantly under `A <-> B` rather than creating a preferred
observer.

### Task 4 — common pair-immersion reconstruction

Starting from one fully typed regular calibrated immersion `F:Sigma->(M,g)`, derive:

1. its first fundamental form and the exact `(kappa,phi,beta)` decomposition;
2. its tangent and normal bundles;
3. second fundamental form and normal connection;
4. Gauss, Codazzi, and Ricci equations;
5. Jacobi/geodesic-deviation data associated with a declared congruence inside the same query;
6. ambient and normal holonomy for loops actually associated with the same query.

Then determine which G63 channels are identities, linked free data, or genuinely independent.
Explicitly identify any G63 quantities that cannot be placed in this common object without new
query data.

Before attempting unification, construct or rule out two immersions with identical `h` and
`phi_pair` but inequivalent `II`, normal connection, or holonomy. Use equations (21)--(22) and state
the Codazzi/Ricci sign conventions. Treat a calibrated correspondence or span as a separate
possible primitive object; tangent transport may be only one representation attached to it.

### Task 5 — naturality or no-go

Audit whether a Lorentz metric and bare ordered endpoints can functorially select a curve or
surface on generic metrics. Address isometries, multiple geodesics, conjugate points, cut loci,
topology, and diffeomorphism covariance. If a no-go requires hypotheses, state them precisely.

Audit at least:

- unique geodesic in a convex normal neighborhood;
- orthogonal exponential/Fermi tube from a complete observer germ;
- causal diamond, boundary, or extremal constructions;
- stationary Killing-flow surfaces;
- intrinsic reciprocal-plane integral leaves;
- path groupoid with no quotient;
- homotopy/holonomy classes;
- branch-labelled multirelations.

For every candidate distinguish metric-derived data from query-supplied data.
For every output channel also classify the route as one of: query input, metric-derived output,
retained branch label, or quotiented presentation data.

### Task 6 — R17 exact test

Use equations (13)--(17) to determine whether the R17 foliation and normal connection already
provide the correct complete relation architecture:

- same-leaf endpoints;
- cross-leaf endpoints;
- multiple windings;
- endpoint scalar versus relative holonomy;
- dependence on `lambda`;
- global Hopf-base topology.

Do not promote R17 to the universal UDT branch. Determine what it proves as a constructive model
of the object type.

### Task 7 — causality and co-presence

Determine whether causal accessibility canonically supplies an admissible relation or branch set
without selecting a unique route. State whether co-presence adds any mathematical structure beyond
whole-solution membership. Do not infer instantaneous signalling.

Determine the precise integrability, overlap, and holonomy conditions under which relational
`phi_AB` descends to one pointwise potential `phi(x)`.

### Task 8 — identify the smallest remaining joint

Return the smallest genuine missing item, choosing among or refining:

- no item: preferred path was a category error;
- no universal route selector: the complete query protocol determines which relation type is
  requested;
- complete observer-query semantics;
- a common pair-immersion/correspondence;
- branch/path quotient policy;
- global overlap and middle-state carry;
- native on-shell/global completion;
- one explicit new postulate.

If a new postulate is required, phrase only the minimal statement and construct at least one
countermodel showing why current premises do not imply it.

## 15. Required landing

Return exactly one primary landing, with qualifications:

```text
PREFERRED_PATH_DERIVED
PREFERRED_PATH_IS_A_CATEGORY_ERROR__RELATION_FIRST
NO_UNIVERSAL_ROUTE_SELECTOR_REQUIRED__QUERY_PROTOCOL_DETERMINES_RELATION_TYPE
COMMON_PAIR_IMMERSION_UNIFIES_CHANNELS_CONDITIONALLY
COMPLETE_QUERY_PROTOCOL_IS_THE_SMALLEST_MISSING_PREMISE
BRANCH_LABELLED_MULTIRELATION_IS_METRIC_NATURAL
GLOBAL_ONSHELL_COMPLETION_IS_LOGICALLY_PRIOR
GENUINE_NONUNIQUENESS_REMAINS
```

or a more precise replacement.

Also return:

1. a premise/type ledger;
2. the strongest proof or no-go;
3. the strongest counterexample;
4. a channel-ownership table;
5. exact equations for the common pair-immersion test;
6. runnable symbolic or numerical checks for every finite-dimensional load-bearing claim;
7. the smallest next calculation, if any;
8. a short lay explanation.

Do not derive an action, source, matter law, mass spectrum, `X_max` value, CMB spectrum, bootstrap
optimizer, or signalling theory in this review.

## 16. Controlling source map

The brief is self-contained, but these repository sources control its statements:

```text
UDT_RECIPROCAL_C_FOUNDING_POSTULATE_MAP.md
UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md

udt_founding_phi_ownership_morphism_audit_2026-08-05/
  AUDIT_REPORT.md
  EXACT_DERIVATION.md

udt_complete_pair_phi_orchestra_audit_2026-08-05/
  AUDIT_REPORT.md
  EXACT_DERIVATION.md

udt_terminal_reciprocal_ce_positional_derivation_2026-08-09/
  AUDIT_REPORT.md
  EXACT_DERIVATION.md

udt_reciprocal_flag_foundation_ownership_audit_2026-08-09/
  AUDIT_REPORT.md
  EXACT_DERIVATION.md

udt_reciprocal_calibration_state_solder_audit_2026-08-09/
  AUDIT_REPORT.md
  EXACT_DERIVATION.md

udt_calibrated_pair_map_owner_atlas_2026-08-09/
  AUDIT_REPORT.md
  EXACT_DERIVATION.md

udt_founding_pair_relation_functor_ownership_audit_2026-08-09/
  AUDIT_REPORT.md
  EXACT_DERIVATION.md

udt_r17_intrinsic_pair_foliation_integrability_audit_2026-08-10/
  AUDIT_REPORT.md
  EXACT_DERIVATION.md

udt_r17_path_labelled_connection_decomposition_audit_2026-08-10/
  AUDIT_REPORT.md
  EXACT_DERIVATION.md

udt_r17_depth_holonomy_joint_invariant_audit_2026-08-10/
  AUDIT_REPORT.md
  EXACT_DERIVATION.md

udt_multichannel_observer_relation_assembly_audit_2026-08-10/
  AUDIT_REPORT.md
  EXACT_DERIVATION.md

udt_pair_instrument_mixing_solution_space_audit_2026-08-10/
  AUDIT_REPORT.md
  EXACT_DERIVATION.md

udt_complete_timelive_orchestra_compatibility_audit_2026-08-10/
  AUDIT_REPORT.md
  EXACT_DERIVATION.md

udt_complete_observer_network_assembly_from_scratch_2026-08-11/
  AUDIT_REPORT.md
  EXACT_DERIVATION.md

udt_solved_geometry_relation_family_survivor_atlas_2026-08-11/
  AUDIT_REPORT.md
  EXACT_METHOD_AND_LIMITS.md
  SURVIVOR_CLASSIFICATION.tsv
  EXTERNAL_REVIEW_ADJUDICATION.md
```

`LIVE.md` and `CURRENT_SCIENTIFIC_PREMISES.tsv` control current status and forbid promotion of the
conditional structures above.
