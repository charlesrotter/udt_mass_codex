# CF1 independent reconstruction — before author exposure

Review-only fresh context, 2026-09-08. Initial HEAD and both local grok/origin-grok
refs: `32d23fb47dc4e440acc8c721aef6cb8201796ded`. The user explicitly replaces
startup synchronization and duplicate audit with reuse. No checkout/fetch/pull,
Git mutation, agent, resume, fork or model override was performed. This context
has received the dispatch, allowed startup sources, WORK_ORDER and QUESTION;
it has not received the author candidate, checker, results, campaign log, other
reviews or advisory material. This document is an independently constructed
argument from the declared definitions, not an assessment of an unseen proof.

## Frame, hypotheses, coverage and stop

This is exact mathematics on the supplied compact smooth S3, with
`s=|z2|^2`, `V1=(iz1,0)`, `V2=(0,iz2)`, and
`X=V1+r(s)V2`, where r is smooth and strictly positive on [0,1]. The test sector,
torus action, sign, coordinate conventions and supplied Hopf map are
`pinned-by-THEORY` only relative to step_01/QUESTION.md, not derived physical
choices. r is `free-and-explored` within that sector. The frame is the supplied
mathematical template; there is no metric evolution computation or physical
choice here. Both axes are included. Equivalence permits every smooth ambient
diffeomorphism and unparametrized leaves, not just equivariant maps.

The exact questions are all-leaf closure, regular smooth circle-fibre
submersion, Hopf equivalence, and smooth time-family equivalence from identity.
Maximum conclusion is an iff classification in this specified positive sector.
No lawful K, Einstein evolution, genericity, metric-selected structure,
physical stability or topology change is inferred. CF2 must supply its own
actual global-data/development join. There is no obligation for CF1 to do so.

Checks are finite exact arithmetic/algebra supporting the proof below. They do
not decide irrationality numerically or prove the universal quantifiers.
CPU only; no GPU/grid; one library thread; existing run_capture.py with 512 MiB
address-space and 60 CPU/wall seconds per check. Total review budget 45 minutes
from approximately 20:29:52 UTC, with unresolved objection as the return point
if a load-bearing issue cannot be settled. No physical equations are imported.

## 1. Global vector field and individual leaves

V1,V2 are globally smooth rotations. r(|z2|^2) is smooth at both axes as well
as in the torus charts. X is tangent to S3 and nonzero: its Euclidean norm
squared is `|z1|^2+r(s)^2 |z2|^2=(1-s)+r(s)^2 s>0`. Also Xs=0.
Consequently its complete flow is exactly

    (z1,z2) -> (exp(i u) z1, exp(i r(s) u) z2).

For 0<s<1 a return requires `u=2*pi*q` and `q*r(s)=p` with integers p,q,
q>0. It exists iff r(s) is rational. For r(s)=p/q in positive lowest terms,
the least positive period for this representative is 2*pi*q. These are
unparametrized-circle statements independent of positive changes of speed.
For irrational r(s), any supposed period gives the contradictory rational
formula above. Nonclosure alone suffices; no density theorem is needed.

At s=0 the leaf is the z1-axis circle with period 2*pi. At s=1 it is the
z2-axis circle with period 2*pi/r(1). Both are closed whatever the interior
slopes do. An irrational orbit can approach itself but cannot be a compact
embedded circle: a nonvanishing smooth vector field tangent to a compact
circle has a finite traversal time (its speed has a positive minimum).

## 2. All leaves closed

All leaves close iff r is a constant positive rational.

Necessity: on the connected interval (0,1) closure makes every value rational.
A continuous nonconstant real function has an interval in its image by the
intermediate-value theorem; any nondegenerate interval contains an irrational.
Thus r is constant in the interior; continuity fixes the same endpoint values.
Sufficiency follows directly from the flow, including both axes.

This does not assert that every member has either all closed or all nonclosed
leaves. A varying r can have rational tori, irrational tori and rational
plateaus at the same time. Both axes always close.

## 3. Axis return germs and regularity of a fibration

Take transverse disk D0: z1 positive real, z2=w near 0. One traversal of the
central axis follows phi1 through 2*pi. Its transverse return germ is

    P0(w) = exp(2*pi*i*r(|w|^2)) w.

At the other axis use D1: z2 positive real, z1=w. Following phi2 through
2*pi requires the variable time 2*pi/r(1-|w|^2). Its return germ is

    P1(w) = exp(2*pi*i/r(1-|w|^2)) w.

These are foliation holonomy germs, not just periods or chart identifications.
For constant r=p/q reduced, P0 is rotation by 2*pi*p/q and has order q;
P1 is rotation by 2*pi*q/p and has order p. In the case p or q equals 1,
that axis has trivial holonomy; the other can still be exceptional. Interior
leaf holonomy is trivial for constant rational r: its primitive q-fold return
has exactly the identity transverse germ.

A regular circle-fibre submersion to a smooth surface has trivial holonomy
along each fibre: local transverse disks map diffeomorphically to the same
base disk, and continuing within a fibre preserves that base point, so the
return germ is the identity. Compact connected circle fibres supply closure,
which by section 2 has already forced constant rational r. The axis orders
therefore force p=q=1. Conversely r=1 is exactly the standard Hopf kernel;
for example `(2 z1 conjugate(z2), |z1|^2-|z2|^2)` gives its submersion to S2.
Local coordinates w=z2/z1 (or its reciprocal) show its rank is two at the
axes as well as elsewhere. Thus:

    regular circle fibration <=> r identically 1.

All-closed weighted flows with a nonunit primitive weight are not regular
circle-fibre submersions; the exceptional-axis return germ is the obstruction.
An underlying topological leaf space, or an orbifold quotient, is a weaker
object and does not meet this definition. Calling all their leaves circles
does not remove their nontrivial holonomy.

## 4. Full diffeomorphism equivalence, not only equivariance

An ambient smooth diffeomorphism carrying line distributions carries their
maximal leaves to maximal leaves. It preserves compactness and conjugates
holonomy germs (a reversal of leaf orientation replaces a generator by its
inverse, which does not change whether it is trivial or its finite order).
The Hopf foliation has compact leaves and trivial leaf holonomy. A nonconstant
r, or a constant irrational r, fails compact-leaf closure. A constant rational
r=p/q other than 1 has nontrivial axis holonomy. No smooth ambient diffeomorphism,
including a non-equivariant one, can carry Hopf to any of these fields.
For r=1 the identity works. Hence in this precise sector:

    Hopf equivalence by an arbitrary smooth diffeomorphism
    <=> regular circle fibration <=> r identically 1.

This proof does not rely on a census of all circle fibrations on S3, theorems
about all Seifert actions, or an extension of a torus coordinate map to axes.

## 5. Smooth families and exact obstructions

For a jointly smooth positive r(t,s) on an interval containing t=0, initially
r(0,s)=1, a smooth isotopy F_t from identity carrying Hopf to L_t exists on
the whole interval iff r(t,s)=1 throughout it. Necessity holds at each t by
section 4 even without smoothness of F_t; sufficiency uses F_t=id. No extra
time-regularity theorem is hidden here because the surviving member is fixed.

If only all-orbits-closed is required at every t in a connected interval,
section 2 first gives r(t,s)=rho(t) rational. Continuity of rho forces it
constant; the initial condition makes it 1. At isolated times constant
rational slopes different from 1 can have all leaves closed without Hopf
equivalence. Constant irrational slopes fail closure even arbitrarily close
to 1. Constant slopes (N+1)/N approach 1 while all leaves close but have
exceptional-axis orders N and N+1. The distinction is not numerical tolerance.

More generally failure of a local persistence interval means every sufficiently
small interval contains some time with r(t,.) not identically 1. It need not
mean every nonzero time fails. A nonzero derivative can establish such
departure inside this actual family; a vanishing derivative cannot establish
persistence. Smooth flat time functions can leave r=1 with all initial time
jets zero. These are mathematical examples only, not vacuum developments.

The homotopy r_v=(1-v)+v*r stays positive and gives nonvanishing smooth line
fields. Thus line-field homotopy to Hopf supplies neither closure nor
fibration equivalence. Neither drift nor homotopy alone supplies CF2.

## Evidence and review independence

Context: fresh review-only conversation as dispatched; no author turn history,
resume, fork or child agent. Model: backend identity UNKNOWN. The dispatch's
configured CLI label gpt-6-astra/xhigh is not backend authentication; different-
model review UNTESTED. Argument: source-first reconstruction from QUESTION.
Implementation: new small checker, sharing Python and the required capture
utility only; shared elementary formulas are mathematically unavoidable.
Human specialist/formal proof-assistant review UNTESTED. No theorem is promoted.

Parent synchronization is reused, not freshly network-verified. At receipt
inspection HEAD/grok/origin-grok all matched the dispatched hash. The parent
prebank_358.json reports returncode 0, timeout false and PASS for 358 rows;
its stdout/stderr strings match the separate files byte-for-byte. The on-disk
registry and verifier matched `git show` at the parent hash. This authenticates
correspondence at inspection, not a new run, remote freshness after parent
sync, or atomic provenance of every dependency during the parent's audit.
Concurrent parent banking can change later HEAD/status; it cannot strengthen
this review or alter the sealed mathematical definitions.
