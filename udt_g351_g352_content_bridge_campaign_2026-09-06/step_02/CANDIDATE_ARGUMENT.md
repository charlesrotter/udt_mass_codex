# Step2 candidate — symmetry constrains a geometric rule, not its physical identity

UNPROMOTED; direct review pending. IDs CB2-SHAPE, CB2-FINITE, CB2-CONVERSION.
Work order frozen at9fb783cb, accepted-source snapshot c19b5fb1. Step1's fresh
VERIFIED-WITH-CAVEATS query result is used only conditionally, with its limits.
No physical requirement of metric-only content naturality is adopted here.

## 1. Objects and exact construction class

G313 section5 admits the constant-real-A!=0 plane wave in the owner-provisional
G312/UR vacuum arena. It does not select a physical history or population.
Condition on the earlier unpromoted CHOSEN Weyl/dual recipe, with

    g=-2 du dv+dx^2+dy^2+A(x^2-y^2)du^2,
    beta=-b du=dTheta, b=sqrt(2|A|), C0=beta#=b partial_v.

Supply time orientation, positive dimensionless spacing Delta and the same
smooth local phase/product framework as Step1. Consider aligned smooth
nonnegative current representatives C=f C0, with f independent of v and phase,
so their label measure is mu=Delta f dxdy. Step1 proves these are reduced-query
completions, NOT fully coupled physical solutions.

Now restrict this construction class: f is a natural scalar assignment from
g,beta,Delta (and orientation), with no supplied observer, preferred point,
coordinate labels, boundary, population profile or material length. In precise
form, for every allowed local diffeomorphism psi,

    f[psi* g,psi* beta,Delta] = psi* f[g,beta,Delta].       (N)

The rule is local/restriction-compatible on the metric germs under discussion.
This is an explicit mathematical hypothesis under test, not an enlargement of
G312's Local Metric Sufficiency beyond its accepted vacuum-response scope.
The chosen geometric recipe already has this naturality; its physical adoption
does not follow. Phase/Delta are fixed for the following comparisons.

## 2. Full symmetries and the surviving constant (CB2-SHAPE)

Let p(u),q(u) solve p''=A p, q''=-A q. Define

    T(u,v,x,y)=(u, v+p'x+q'y+(pp'+qq')/2, x+p, y+q).      (1)

Expanding T* g, the du dx and du dy terms cancel. The extra du^2 term is

    2(Ap-p'')x + 2(-Aq-q'')y
    + A(p^2-q^2)-pp''-qq'',

which vanishes by those ODEs. Thus T* g=g, T* beta=beta, and T_* C0=C0.
Its Jacobian determinant is1. The maps are continuously connected to identity
by scaling p,q and therefore preserve the supplied time/volume orientations.
They also preserve |dTheta| dxdy, since the added p'du,q'du vanish in its wedge.
Constant v translations preserve the same data.

At any fixed u0 the ODEs permit arbitrary p(u0),q(u0),p'(u0),q'(u0). This follows
from their constant-coefficient linear equations: exponential/hyperbolic bases
for a positive coefficient, sine/cosine bases for a negative coefficient, each
with nonzero fundamental Wronskian. Both signs of nonzero A are covered. In
particular p',q' can be zero at u0 while p,q are arbitrary, giving arbitrary
transverse translations at that phase. Small versions suffice on a local chart.

By(N), f is invariant under these symmetries. Their local orbits span each
fixed-phase slice, hence f is transverse- and v-independent. The already
declared phase-independent product condition then makes f a spacetime constant
k>=0 on the connected product region. Conversely every CHOSEN dimensionless
constant k gives a natural C=k C0 and mu=Delta k dxdy.

Therefore naturality removes nonuniform f in this aligned smooth construction
class; it does NOT distinguish k=1 from k=2 or choose a physical magnitude.
The original fixed-B root remains unique for its recipe. C=k C0 for k!=1 is
not another root of that fixed B, and a separately chosen coefficient is not
metric-selected merely because it is covariant. This conclusion does not
classify currents outside the stated aligned smooth class.

## 3. Local finite patches versus intrinsic finite population (CB2-FINITE)

On any SUPPLIED finite-area patch V, mu(V)=Delta k Area(V) is finite. This
is exactly the type G351/G352 allow. Choosing V restricts the query and can
break the symmetries; no theorem here forbids that use or selects its edge.

Separately add the global mathematical hypotheses: the transverse quotient at
one phase is the complete R^2 plane, the measure is Borel, nonnegative, finite
on the whole plane, and invariant under ALL its translations. These are NOT
extra hypotheses of G351. Let Q=[0,1)^2 and m=mu(Q). Its integer translates
are disjoint and cover R^2. Translation invariance gives every square mass m.
Finiteness bounds N m for every positive integer N, forcing m=0. Countable
additivity on the covering then gives mu(R^2)=0. This proof needs no smooth
density and does not conclude anything about a merely locally finite measure.

For k>0, the natural area measure is locally finite with infinite whole-plane
amount; its supplied finite-patch restriction is nonzero and finite. A subset
of the complete plane invariant under every translation is empty or the whole
plane (translate any point to any other point), so an intrinsic nonempty bounded
populated support cannot be chosen by those symmetries alone. A finite query
window, actual boundary, additional structure or different global geometry
changes these hypotheses; it is not a refutation. No global completion of UDT,
X_max boundary, physical cutoff or universal absence of finite content follows.

## 4. A precise optional count-conversion obstruction (CB2-CONVERSION)

The geometric mu has homothety weight+2. IF one seeks to convert it to a
homothety-invariant dimensionless count by multiplying by a scalar q, a specific
candidate route would require a natural smooth real scalar q[g,beta,Delta]
with

    q[h^2 g,beta,Delta]=h^-2 q[g,beta,Delta], h>0.         (2)

Its rule must be defined on this branch and its constant homotheties, local/
restriction-compatible, observer-neutral and free of extra dimensional data.
These are OPTIONAL construction-class hypotheses, not a claim that all physical
amount must be a dimensionless count or that every possible conversion is here.

Use the explicit proper homothety

    F_h(u,v,x,y)=(u,h^2 v,h x,h y).                       (3)

Direct pullback gives F_h* g=h^2 g, F_h* beta=beta. Every point P=(u0,0,0,0)
is fixed. Scalar naturality and(2) at that point give

    q[g,beta,Delta](P)
      = (F_h* q[g,beta,Delta])(P)
      = q[h^2 g,beta,Delta](P)
      = h^-2 q[g,beta,Delta](P).

Taking h=2 forces q(P)=0. The isometries in section2 and constant v translations
carry each point at u0 to its axis point; naturality therefore gives q=0
everywhere on the region. This argument does not need phase-independence of q,
polynomial curvature invariants, dimensional guessing, or a finite search.
For strictly local germs one may instead take h arbitrarily close to1 and
restrict its domain; restriction-compatibility is essential. A domain boundary
or nonlocal supplied structure would be different data.

Thus no nonzero scalar in THIS class converts this branch's geometric area
amount to an invariant count. This does not reject its original area-valued
measure, which has a different weight and survives with any k>=0. It does not
show that physical content is impossible or that a new premise is necessary.

The tempting replacement q=|A| is not a scalar: under passive u'=a u,v'=v/a,
A'=A/a^2, whereas beta=-sqrt(2|A|)du remains the same covector. A preferred
null-coordinate normalization would add data. Likewise q=(-beta(U_*))^2 for
a SUPPLIED unit future observer field has the desired homothety weight when
U_* rescales as U_*/h, but uses an extra field. Recomputing it from each
measuring observer changes mu and fails Step1's fixed-measure query. A supplied
material length can also change the input/scaling assumptions. No such field,
length, count interpretation or physical choice is selected or adopted here.

## 5. Landing, counterevidence and review limits

The useful surviving geometric structure is a locally finite uniform area
measure times an unselected constant, with compatible product/readout on a
supplied finite patch. Symmetry does not turn it into physical content. The
stronger proposed routes fail under their stated hypotheses: nonuniform
metric-only profile in this class; nonzero globally finite fully translation-
invariant whole-plane amount; natural scalar weight-2 count conversion without
extra input. Neither the uniform area measure nor supplied finite content is
refuted. The chosen cross-phase labels still are not a physical identity law.

What would count against this result: a full pullback/sign defect; failure of
the stated local symmetry reach; a nonzero measure satisfying the exact global
hypotheses; or a natural scalar satisfying(2) on the same metric/phase germs.
A different geometry, supplied boundary/observer/scale or non-natural rule is
an alternative route, not that counterexample. No general completeness claim.

The analytic symmetry/measure/fixed-point arguments carry the quantifiers.
The exact checker verifies full4x4 metric/covector identities, both-sign
rational witnesses, current/amount scaling and a null-coordinate boost; small
arithmetic controls supplement the proof. Sixteen guard groups passed in two
author runs. Five deliberately faulty variants failed at the intended checks.
No unexpected mathematical failure or pre-freeze correction occurred in Step2.
Sources and Step1's review are dependencies, not new evidence for adoption.
The fresh Step2 reviewer has not received this argument/code/results at freeze.
