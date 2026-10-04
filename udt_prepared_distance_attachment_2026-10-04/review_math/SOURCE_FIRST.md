# PDA1 mathematical reviewer — sealed source-first argument

Status: independent analytic construction/attack before exposure to PDA1's
parent candidate, tests or the other reviewer's files. Conditional mathematics,
not a scientific promotion. Reviewer context `/root/pda_math`; runtime identity
Codex based on GPT-6 (no more specific model identity supplied; no model
independence claim). The parent dispatch, WORK_ORDER and BASELINE are exposed.
FCL/CCW candidate and reviewed-source verdicts are exposed as required sources;
PDA1 candidate/verdict is not. Parent's startup full406 PASS411.800s,
normal verification and57 maintenance tests are attributed, not independently
rerun here. Independent branch/HEAD/status inspection found grok at
976f860dcbb4dc382152d540e604e18e8874f0ce with existing untracked work and this
new package. No protected payload was read, hashed, staged or changed.

Applied on-disk AGENTS/CLAUDE and no-shortcuts, completeness-map,
solution-space-not-imposition, verifier-before-record protocols. The source
snapshot hashes are in SOURCE_FIRST_SEAL.json. No scientific program ran.
The following hand derivation checks the load-bearing equations and gives
adverse as well as positive exact controls. It does not independently replay
all old FCL/CCW scripts or their full packages.

## 1. Scope and main finding

RG and the ordinary proper-clock/null interface remain supplied, conditional
and UNADOPTED at their existing source scope. I find a source-preserving
conditional route to a distance pole. It requires actual fixed-emission
incidence, a regular ray branch and a chosen initial-distance path transverse
to the limiting light front. Compact smooth bounded initial data alone do not
supply remote source access, a common regular future collar, a nonsingular
receiver endpoint map, transverse incidence or a scalar law common to all
angles/population labels.

The endpoint map need not be assumed C1 if a common compact collar and bounded
smooth crossing data have actually been obtained: a shifted x-adapted chart
retains enough of the stipulated C3 regularity to prove C1 dependence. This
avoids differentiating FCL's normal chart beyond its guaranteed C1 coefficients.
Endpoint-map nonsingularity does not follow and is not by itself enough for a
simple distance pole. An explicit nonsingular, noncrossing counterexample
below has a quadratic attachment and a double distance pole.

Choice ledger: RG/geodesic/null equations are pinned-by-THEORY only at their
existing conditional source scope, not native adoption. Initial slice, origin,
label path, constant momentum and examples are free-and-explored query data.
Time uses c_E=1 length units. No field/source law, physical population,
preferred observer, fitted metric, Omega=distance definition, native scale,
X_max, extra UDT attribution or complete-postulate insufficiency is introduced.

## 2. Uniform estimates and endpoint regularity

First obtain a common x=Omega collar: all selected trajectories cross x=x0,
their crossing positions and finite velocities depend C1 on compact labels,
and the entire future tails stay in a common relatively compact regular patch.
A compact finite-time geodesic-flow tube can establish the crossing-data bound;
compact initial data alone, without that existence/tube check, cannot.
Alternatively prepare directly on a sufficiently small interior collar slice
with a margin exceeding the finite coordinate-speed displacement bound.
These are checkable supplied/local hypotheses, not a global existence theorem.

There is a useful C3-regularity route. Use x=Omega plus ordinary transverse
coordinates, without flowing them to eliminate shift. The C3 coordinate
inverse gives at least C2 pulled-back metric coefficients. Write

    b=-N^2 dx^2+h_ij(dy^i+beta^i dx)(dy^j+beta^j dx),
    n=-(partial_x-beta^i partial_i)/N,
    T=u/x=gamma n+v, w_i=h_ij v^j,
    gamma=sqrt(1+h^ij w_i w_j).

N,h,beta and their first two derivatives have finite compact bounds and h,N
have positive lower bounds. Future orientation gives

    dx/dtau=-x gamma/N,
    dy^i/dx=-beta^i-N h^ij w_j/gamma = G^i(x,y,w).

Since P_i=g_ia u^a=w_i/x, the lowered geodesic equation gives exactly

    dP_i/dtau=-(partial_i N)gamma^2/N
        +(partial_i h_jk)v^j v^k/2
        -(gamma/N) w_k partial_i beta^k,
    dw_i/dx=w_i/x+F_i,
    F_i=(partial_i N)gamma
        -N(partial_i h_jk)v^j v^k/(2gamma)
        +w_k partial_i beta^k.

I recomputed the shift term and its sign directly by differentiating b(T,T)
at fixed coordinate T. All spatial dependence remains. On the common compact
metric patch |F|<=C(1+|w|). For s=log(x0/x), FCL's same norm comparison yields

    |w(x,a)| <= exp(C x0)(x/x0)[W+C x0 log(x0/x)]

uniformly in labels a, where W bounds the actual crossing data. Thus w->0
uniformly; |dy/dx| is uniformly bounded and the endpoint Y(a)=lim y(x,a)
exists, with y-Y=O(x) in this shifted chart. In the normal chart the source's
sharper spatial remainder is O(x^2[1+log(x0/x)]). These are compatible chart
statements. Uniform limits of the continuous interior flow first give Y
continuous; this alone is not a differentiability argument.

For differentiability put V=D_a y, W1=D_a w. Bounded w and C2 metric data bound
G_y,G_w,F_y,F_w uniformly. In decreasing-x time the exact linearized equations
are

    V_s=-x(G_y V+G_w W1),
    (W1)_s=-W1-x(F_y V+F_w W1).

The upper norm derivative of |V|+|W1| is at most C x(|V|+|W1|), after discarding
the helpful -|W1| term. Since integral_0^infinity x ds=x0, Gronwall bounds both
uniformly. Substitution into the second equation and the same integrating
factor as FCL gives W1=O(x[1+log(x0/x)]), uniformly. The first equation in x
then has a bounded right side, so V has a uniform limit. Uniform convergence
of interior first derivatives on compact label charts gives Y C1. Also

    r(x,a)=(x,y(x,a)),
    r_x(0,a)=(1,-beta(0,Y(a)))=-N_* n_*,
    D_a r(0,a)=(0,D_a Y).

Hence r extends jointly C1. This proof supplies neither det D_aY!=0 nor
injectivity. Physical phase-space geodesic-flow invertibility does not imply
invertibility of its endpoint-position projection. Interior crossing and a
singular endpoint projection are separate issues. For a labelled one-parameter
family a simple pole needs only the appropriate directional derivative below;
full three-dimensional endpoint-map nonsingularity is a convenient stronger
congruence condition, not a necessary hypothesis for every one-dimensional
query.

## 3. Actual fixed-emission incidence and operational distance

Fix the actual emission event e and its ordinary unit velocity u_e. Supply a
regular null wavefront branch to p=r(0,a*), with a C2 local defining function
f(q), f(p)=0 and df_p=b(K,.) for a future nonzero conformal-null tangent K
(the irrelevant positive normalization may be absorbed). For example, the
CCW local C3 extension plus a convex normal neighborhood gives
f(q)=sigma_b(e,q). A remote prescribed source needs its own regular branch;
RG alone supplies no such access. Supply the future orientation of this branch.

Set F(x,a)=f(r(x,a)). Endpoint regularity above gives

    F_x(0,a*)=b(K,-N_* n_*)=N_* B0>0,
    B0=-b(K,n_*)>0,
    F_a(0,a*)=df_p(0,Y'(a*)).

Thus the incidence equation F=0 determines a unique local x=x(a) with

    x'(a*)=-F_a/F_x.

For a one-sided domain the same result follows from a C1 extension of F (or
one-sided inverse argument); only x>0 receptions count. No physical extension
beyond x=0 or boundary reception is inferred.

Let L(a) be the induced physical-metric proper distance on the stated initial
spacelike slice from the stated origin, in a smooth cut-locus-free domain.
If L'(a*)!=0, use L as local parameter. For approach from L<L*, require

    c=F_a/(F_x L') >0.

Then actual incidence, rather than definition of Omega, proves

    x_o(L)=c(L*-L)+o(L*-L).

Let E=-b(K_e,u_e)>0 be the physical emission frequency of the same conformal-
affine normalization (k=x^2 K); normalize the whole ray by E. Regularity gives
B_o=-b(K_o/E,T_o)->B0/E>0. R6 then gives

    Z=1/(x_o B_o),
    (L*-L) Z -> 1/[c(B0/E)] = N_* E L'/F_a >0.

This residue is independent of a regular positive conformal gauge because c
and B transform oppositely. It depends on geometry, emitter normalization,
initial ruler and preparation; it is not a universal scale. Uniform convergence
and the incidence derivative prove the limit, not full-history monotonicity.

Equivalent source-clock form, when an actual timelike emitter family is
available, is s_*(a)=s(0,a), s_*'=-F_a/E. Therefore
(L*-L)Z -> -N_*/(ds_*/dL), with ds_*/dL<0 on this orientation. This is a useful
cross-check against CCW's emitter-gap residue; it must not replace deriving
s_*(a) from the geometry and preparation.

For a multidimensional population, a chosen one-dimensional path/section or
additional factorization is essential. Different receivers with the same
initial L can have different endpoints and shifts. A nonsingular endpoint
map and a nonzero distance gradient do not by themselves define a common
Z(L) or a common L*. In a three-label chart the limiting light-front pullback
F(0,a)=0 is generally a surface; compare it to distance levels explicitly.
Tangential intersections may give higher powers, absence of reception, or
noninvertibility of the distance label. C1 alone gives the simple-pole result
under nonzero first derivative; higher-order classifications require their own
extra differentiability/order calculation.

## 4. Exact supplied positive and adverse controls

All controls use the supplied flat conformal geometry

    g=x^-2(-dx^2+d y_vec^2), 0<x<=1,

with initial slice x=1, Euclidean physical initial distance, origin/source
(e,u_e)=((1,0),-partial_x), and ordinary free receivers. This slice's coordinate-
comoving unit normals are generally not the parallel-transport preparation of
PSW1 on its spacelike preparation geodesic. The following constant-momentum
initial velocities are explicit query choices, not PSW by relabeling.

### A. Positive moving free family

For q=(L,0,0), fixed P=3/4 in the first spatial direction,

    gamma(x)=sqrt(1+P^2 x^2),
    y(x,L)=L+[sqrt(1+P^2)-sqrt(1+P^2 x^2)]/P,
    Y(L)=L+d, d=(sqrt(1+P^2)-1)/P=1/3.

These solve the constant physical spatial momentum geodesic equations and
have uniform finite initial data, noncrossing spatial maps and Y'=1.
Outgoing actual null incidence is y=1-x. The derivative of x+y-1 is
1-Px/gamma>0, so there is exactly one interior future reception for
0<L<L*=2/3, with x=0 only at the limiting label. Squaring the actual incidence
while preserving its positive-root sign gives

    x_o(L)=[16-(2+3L)^2]/[6(2+3L)],
    Z=1/[x_o(gamma(x_o)-P x_o)],
    x_o/(2/3-L)->1, (2/3-L)Z->1.

The formula gives x=1 at L=0 and x=0 at L=2/3; the derivative at the endpoint
is -1. This is a moving free positive control, not merely a comoving clock.

An immediate radial return to the same comoving emitter arrives at
x_return=2x_o-1. The echo exists only for x_o>1/2, equivalently

    0<L<(sqrt(73)-7)/6 < L*.

At equality return occurs only at x=0, not at a physical clock event. Near
the one-way distance pole there is no such echo.

### B. Smooth bounded noncrossing family with a nonsingular endpoint map,
###    but tangential distance attachment and a double pole

Keep the SAME fixed P=3/4 for every receiver and all nearby 3D initial
positions q. The spatial flow is translation, so it is noncrossing for every
x, and its endpoint map Y(q)=q+(1/3,0,0) has Jacobian identity. Select the
smooth one-parameter subfamily

    q(a)=(-1/3+a, 1-a^2, 0),
    Y(a)=(a,1-a^2,0),  a near0.

Initial distance is actual Euclidean L(a)=|q(a)| on the initial slice. At a=0,

    L*=sqrt(10)/3, L'(0)=-1/sqrt(10)!=0,
    |Y(a)|=sqrt(1-a^2+a^4)=1-a^2/2+O(a^4).

Outgoing incidence from e is |y(x,a)|=1-x. Its x derivative in
x+|y|-1 is >=1-|P|x/gamma>0. For every small nonzero a, F(0,a)<0 and
F(1,a)=|q(a)|>0; hence the unique actual future reception exists. At a=0 it
is only the boundary endpoint. Since y(x,a)=Y(a)-(P/2)x^2 e1+O(x^4),

    x_o(a)=a^2/2+O(a^4),
    x_o/(L*-L)^2 ->5  as a->0+,
    B_o=gamma-P x_o n1 ->1,
    (L*-L)^2 Z ->1/5.

Here n is the actual outgoing unit ray direction y/|y|. All physical initial
velocities are identical and bounded. The endpoint map is a diffeomorphism;
initial proper distance is a valid local parameter; the only failed simple-
pole gate is transversality to the limiting null wavefront. This explicitly
refutes the tempting inference “uniform bounded preparation plus nonsingular
endpoint map gives a simple distance pole.” It does not refute the conditional
transverse theorem or establish a generic higher-order law. The deliberate
curve shape constructs a mathematical counterexample, not a native or fitted
physical preparation.

For the same comoving source, any such reception has |y_o|=1-x_o, so the
future straight return again requires x_return=2x_o-1>0. It fails near this
one-way limit too.

### C. Endpoint Jacobian degeneration is also possible

For initial positions q=(L,0,0) near L*=1 choose a smooth bounded momentum
through d(L)=-(L-1)-(L-1)^2 and P(L)=2d/(1-d^2). The identity
(sqrt(1+P^2)-1)/P=d gives Y(L)=1-(L-1)^2 exactly. Thus Y'(1)=0 although
initial data are smooth and bounded. Actual incidence gives
x_o=(L-1)^2+o((L-1)^2), B_o->1. This is a distinct endpoint-projection
failure, not needed for control B. It shows compact smooth preparation alone
cannot assert a nonsingular endpoint map. Interior y_L at L=1 equals x^2>0;
no contradiction with regular interior phase-space evolution occurs.

### D. CCW's unbounded-boost population fails the stated gate

CCW gives P_a=(1-a^-2)/2 at its fixed-emission receptions. On x=1,
w=P_a and gamma=sqrt(1+P_a^2) diverge as a->0. It admits no continuous finite
extension of its initial velocities to a compact label set containing the
limit and no uniform W in the estimate. Its exact Z=1 therefore remains a
valid warning against pointwise-to-population quantifier exchange, while
being excluded by the bounded-preparation hypothesis without a new mechanism.

## 5. Review ceilings and omissions

The hand checks above recompute the shifted geodesic equation, uniform
variational estimates, null-incidence sign/implicit derivative, distance
residue, all displayed control limits and echo domains. They are analytic
checks, not numerical certification or finite-sample proof of the generic
statement. No independent scientific program, all-source replay, remote
caustic/global-existence classification, common angular distance law,
whole-history monotonicity or native RG admission was attempted.

For the upcoming exposed review, high-priority attacks are: differentiating
normal-chart coefficients without sufficient regularity; replacing compact
initial data by an unproved common collar; conflating endpoint-map regularity
with nonsingularity; claiming transversality merely from timelikeness (it
supplies F_x, not F_a); silently changing a multidimensional population into
one scalar distance curve; and assuming the echo survives the one-way limit.

No parent candidate objection or acceptance is asserted at this source-first
stage. This sealed route should be compared against the eventual candidate,
with any source-preserving repair and final integration reviewed separately.
