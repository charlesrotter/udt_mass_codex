# ACI1 source-first mathematical reconstruction

Status: CONDITIONAL CANDIDATE, UNPROMOTED. Analytic reconstruction, not a native
metric-selection result. This note was completed without reading the parent's
new candidate or sibling source-first arguments. See EXPOSURE.json for the
pre-seal message defect affecting the parent's independence chronology.

## 1. Sources, frame and ceiling

Assigned snapshot: grok dfe6ba373f8a7ecf1c55a3b58d8fd727976362e6, independently
checked. Top-level synchronization and CPA1 normal/57-maintenance/full406
PASS412.1847066390328s are attributed to the parent, not rerun here and not
scientific evidence for this argument. Exact source SHA-256 pins are in
SOURCE_PINS.json. I read AGENTS.md, the relevant CLAUDE.md method/trigger/repo
sections, the no-shortcuts and completeness-map protocols, and ACI1 WORK_ORDER.
Scientific exposure was bounded to central R6/R7, R8 through PSW1, FSL1's
INITIAL_CANDIDATE, REPAIR and REVIEWED_RESULT, SGE1's REVIEWED_RESULT, PSW1 geometry
CROSS_REVIEW, and the roadmap's current extreme-separation direction. Existing
results and old review verdicts were therefore exposed; the new ACI1 candidate
and other source-first reconstructions were not.

R6/FSL1 supply the CONDITIONAL ordinary-clock/free-affine-null interface;
R7/FSL1 already own |log Z| <= relative transported rapidity. R8/SGE already
own log Z = integral K d ell on its compatible-extension domain. PSW's
cross-review already gives the infinitesimal curvature-loop interpretation.
The roadmap target is working asymptotic slowing toward an unreachable limit,
with its physical realization and comparison assignment unselected. No premise
grade is changed. No RG, Einstein equation, physical population, scalar-potential
exactness, isotropy, new response, topology or completion law is introduced.

This is metric-led general Lorentz4. The connection/clock convention is
pinned-by-THEORY only at the cited working/conditional scope. Actual paths,
preparations, sweep and the flat quotient control below are free-and-explored
query/control data. Signature (-+++), c_E=1 and curvature sign are mathematical
conventions. No numerical approximation or frozen physical parameter occurs.
The requested quantifier is every comparison and every sweep satisfying the
stated domain, not every physically realized UDT comparison.

## 2. Conditional finite bound

Let (M,g) be smooth and time-oriented, with its torsion-free metric-compatible
connection, R(X,Y)=[nabla_X,nabla_Y]-nabla_[X,Y]. Let gamma connect emission e to
reception o as one member of a regular smooth future affine-null clock branch,
with endpoint future unit clock vectors u_e,u_o. Thus

    Z = omega_e/omega_o, omega_i=-g(k_i,u_i)>0.

Choose earlier clock events e0,o0, timelike proper-clock histories A:e0->e and
B:o0->o, and any regular piecewise smooth preparation path c:e0->o0. Its
parallel transport is geometric bookkeeping; c need not be a physical signal.
Let u_A0,u_B0 be the clocks at those events and define

    rho0 = arcosh[-g(P_c u_A0,u_B0)],
    a_A = nabla_uA uA, a_B = nabla_uB uB,
    alpha_A = integral_A sqrt(g(a_A,a_A)) d tau,
    alpha_B = integral_B sqrt(g(a_B,a_B)) d tau,
    L_prep = rho0 + alpha_A + alpha_B.

Construct beta:e->o by reversing A, traversing c, then traversing B, with
parallel map Q=P_B P_c P_A^{-1}. Supply a fixed-endpoint sweep H:[0,1]^2->M
from beta to gamma:

    H(s,0)=e, H(s,1)=o, H(0,t)=beta(t), H(1,t)=gamma(t).

A finite stripwise C2 sweep with smooth seam matching suffices for the broken
reference path; parallel transport and its s derivative are continuous at
seams and the integrated identities below telescope. A smooth sweep is the
simpler special case. No homotopy existence or embedding is asserted. It need
not be a causal surface or totally geodesic. Rank degeneracy is harmless when
smooth; no inverse surface metric is used.

Write X=partial_t H, Y=partial_s H, P_s(t) for transport from e along the
s-path through parameter t, and define the future unit field

    U(s,t)=P_s(t)u_e.

For W=R(X,Y)U, metricity gives g(W,U)=0. Hence g(W,W)>=0, and the nonnegative
comparison-dependent curvature-action budget is unambiguous:

    C[H;u_e] = integral_0^1 integral_0^1
               sqrt(g(R(X,Y)U,R(X,Y)U)) dt ds.

The candidate inequality is

    |log Z| <= rho_gamma <= L_prep + C[H;u_e],
    rho_gamma = arcosh[-g(P_gamma u_e,u_o)].                 (ACI-M1)

It is exact, finite and fully four-dimensional. There is no sign or dimensional
reduction assumption on R. It holds for every admissible fixed-endpoint sweep.
For a nonempty set of such sweeps, C can also be replaced by their infimum;
no minimizer or finite-area preferred sweep is guaranteed. Treating an empty
set as infinite is only an extended-value convention, not a geometric result.

## 3. Proof, including the Lorentz-group issue

A. Along a unit timelike clock history, pull its velocity back by parallel
transport to the fixed initial tangent space. Its derivative is the pulled-back
proper acceleration and its speed in the future unit hyperboloid is |a|.
The induced metric on that hyperboloid is positive and its distance is
arcosh[-g(v,w)]. To verify the distance estimate directly, write
w0=cosh(rho)w+sinh(rho)n at any rho>0, with n a spatial unit at w.
Differentiating -g(w0,w)=cosh(rho) and using Cauchy--Schwarz in w-perp gives
|rho'|<=sqrt(g(w',w')); continuity handles rho=0. Integrate and use the triangle
inequality, preserved by Lorentz parallel transport, to obtain

    d_H(u_o,Q u_e) <= alpha_B + rho0 + alpha_A.             (1)

This is why both the initial velocity preparation and integrated acceleration
must be controlled. A pointwise acceleration bound alone does not control a
family with unbounded proper histories.

B. For V(s,t)=P_s(t)v with v fixed at e, nabla_t V=0. Commuting derivatives gives

    nabla_t nabla_s V = R(X,Y)V.

The initial variation is zero because the initial point/vector are fixed. Since
the endpoint o is also fixed, integrate after pulling back by P_s(t):

    B_s := P_s(1)^{-1} d_s P_s(1)
         = integral_0^1 P_s(t)^{-1} R(X,Y) P_s(t) dt.        (2)

This is a linear-map identity on T_eM. If the opposite R convention were used,
the right side changes sign; the estimate does not. All maps are the full4D
maps. On finitely many smooth strips, the intermediate variation boundary terms
cancel because the transported vector has the same value on both sides.

Set v_s=P_s(1)u_e in the fixed reception tangent space. Equation(2) gives

    d_s v_s = P_s(1) integral_0^1 P_s(t)^{-1}R(X,Y)U dt.

Each pulled-back integrand lies in the SAME positive-definite subspace
u_e-perp. Therefore its ordinary triangle inequality, followed by the isometry
P_s(1), gives

    sqrt(g(d_s v_s,d_s v_s))
      <= integral_0^1 sqrt(g(R(X,Y)U,R(X,Y)U)) dt.

Integrating hyperboloid speed now yields

    d_H(P_gamma u_e,Q u_e) <= C[H;u_e].                    (3)

No matrix norm was asserted to be invariant under a noncompact group, and no
Euclidean norm of an arbitrarily conjugated Lorentz matrix was used.

C. Combine(1),(3) by the hyperboloid triangle inequality. R7 already proves
|log Z|<=rho_gamma from the ACTUAL received ray direction. This proves ACI-M1.
The proof controls the time column enough to bound any null readout; it does
not identify a time-column norm with the signed clock depth. No spin/spatial
rotation has been discarded by a planar approximation.

## 4. What this budget means, and what it does not mean

C is a coordinate scalar of the supplied metric, source clock, paths and sweep.
It is unchanged by simultaneous frame changes and orientation-preserving
regular reparametrizations of the surface parameters that preserve the path
foliation. It depends on the sweep and its path ordering. A different source
clock or sweep is different comparison data, not a gauge-free curvature number.
The U field is determined by full parallel transport on that sweep. It is NOT
an independently selected observer population.

For a positive pointwise control introduce

    h_U(V,W)=g(V,W)+2g(U,V)g(U,W).

Let R_U:Lambda^2(TM)->U-perp send X wedge Y to R(X,Y)U, and use the h_U exterior
norm in its domain and h_U=g in its range. Then

    C <= integral ||R_U||_op,hU |X wedge Y|_hU dt ds.        (4)

Thus a uniform bound on this observer-relative curvature norm together with
uniform swept h_U area gives a finite budget. Both controls are substantive
hypotheses. An indefinite Lorentzian "area" is unsuitable: it can vanish on
a nonzero null tangent bivector. Bounded pointwise curvature does not control
an arbitrarily large sweep, and even bounded curvature in some supplied frame
does not bound the transported-frame curvature without boost/distortion control.

There is no positive norm on the relevant Lorentz representation invariant
under all boosts: a nonzero null bivector (e0+e1) wedge e2 scales by exp(r) under
a boost in the 01 plane. Invariance plus homogeneity would force its norm to
vanish. The same null structure makes polynomial curvature scalars insufficient:
an algebraic curvature tensor proportional to F tensor F for the decomposable
null bivector F=l wedge e (l null, e spatial unit, g(l,e)=0) satisfies the
curvature symmetries/Bianchi identity, has vanishing complete scalar
contractions, but R(X,Y)U is generally nonzero and can be scaled arbitrarily.
Therefore a bound expressed only in such scalars cannot replace(4) in general.

The budget is not the unknown redshift relabeled: it never uses k's direction,
u_o or an observed Z. In particular changing the receiver clock changes Z and
L_prep while leaving C fixed. Nevertheless C is a nonlocal, transport-weighted
functional and evaluating it requires more geometric data than R at a point.
It cannot be advertised as a cheap independent scalar-curvature test or a
curvature-only field equation. Any claimed independent uniform bound on C must
be checked for circular use of an already bounded endpoint rapidity; for example,
assuming uniformly bounded transported boosts to prove such a bound can hide
the very conclusion sought. Naming this functional supplies no physical bound.
In a specially aligned sector, inequalities can
saturate; that does not establish an independently selected physical control.

## 5. Exact analytic scope controls

No scientific CPU slot was used. These are explicit analytic controls, not a
finite numeric certificate or a native-admitted UDT model.

1. Contractible Minkowski comparisons: R=0 implies C=0. Parallel-prepared
inertial clocks give rho0=alpha_A=alpha_B=0 and Z=1. Giving the receiving clock
an initial collinear receding rapidity r instead gives Z=exp(r), accounted for
by rho0=r. Thus flat geometry does not make arbitrary observers equal.

2. Acceleration: pulling velocity back along a flat timelike history gives
|Delta rapidity|<=integral |a|d tau; a collinear monotone acceleration saturates.
A fixed nonzero proper acceleration maintained over growing proper duration
escapes the uniform L_prep hypothesis while R remains zero.

3. Topology obstruction with actual signals: let

    M=(0,infinity)_t x S1_x x R2,
    g=-dt^2+t^2 dx^2+dy^2+dz^2, x~x+L, L>0.

The local map T=t cosh x, X=t sinh x exhibits flatness; the identification is a
Lorentz boost. The future unit comoving clock u=partial_t is geodesic. Take
emitter and receiver to be that same clock at x=0. A future null branch with
m positive windings has dx/dt=1/t on the cover, hence

    t_o=exp(mL)t_e, Z=d t_o/d t_e=exp(mL).

Every finite m is a regular smooth branch, R=0, and its reference clock-history
path has rho0=alpha_A=alpha_B=0. The null path and the reference clock path have
different winding and no fixed-endpoint homotopy. Thus deleting the sweep
hypothesis would make ACI-M1 false, even in smooth time-oriented flat Lorentz4
and with actual regular affine-null signals. The theorem supplies no topology
selection or global access theorem. The quotient is a supplied off-equation
control, not an admitted UDT completion.

4. Direction and cancellations: R7's fixed-Z=1 family with diverging transported
rapidity already disproves any converse from large rapidity to redshift. Large C
likewise provides no positive sign, monotonicity or lower bound on Z: C is
unsigned and upper-bounds an integrated vector before further directional
readout. Curvature contributions may cancel, and boosts can be aligned to
produce blueshift instead. No finite-sample test can remove that logical gap.

## 6. Increment and physical join

For a family on the exact stated domain, if L_prep is uniformly bounded and
Z tends to infinity, then for EVERY admissible choice of sweeps

    C[H;u_e] >= log Z - L_prep -> infinity.                 (ACI-M2)

Equivalently, a uniformly bounded preparation/acceleration AND uniformly
bounded transported-curvature budget exclude unbounded received slowing.
Taking the infimum over all existing admissible sweeps retains this necessary
condition, but establishes neither a preferred sweep nor a global comparison.
The actual directional R7 criterion still must hold for sufficiency. If C grows,
that may reflect long or highly stretched sweeps, large transported boosts, or
curvature accumulation; it need not imply a pointwise curvature singularity,
nonzero scalar invariant, finite physical endpoint, or X_max realization.

The increment beyond old work is a finite4D estimate comparing the actual null
path to a controlled preparation/history path through an explicitly curved
sweep. R7 bounds readout by an already supplied endpoint rapidity; this estimate
bounds that rapidity by separate preparation/acceleration and a surface
curvature-action budget. R8's K identity integrates auxiliary first derivatives
along one ray; this controls path-to-path transport with curvature over a sweep.
PSW's small-loop proof supplies leading local coefficients; this supplies a
nonperturbative unsigned finite bound, not new local coefficients. General
parallel-transport variation is ordinary differential geometry, not a newly
native dynamical law and not a full-corpus novelty claim.

Physical join J_ACI remains OPEN: no inspected implication assigns UDT's working
asymptotic positional effect to a family of these actual regular null comparisons
with uniformly controlled preparation/acceleration and an admitted sweep class.
Without that assignment, ACI-M2 is conditional machinery. With that assignment,
the target would exclude the bounded-C subclass, but would still select no
metric, sign, scale, curvature component, field equation, physical observer
population or topology. Existing commitments could have further consequences;
this scoped reconstruction does not prove their insufficiency or that a new
postulate is necessary. No canon, registry grade or central file is changed.

## 7. Checks, omissions and reviewer identity

Analytic checks: explicit curvature commutator/sign derivation; positive-space
triangle inequalities after common-fiber transport; timelike acceleration
bound; observer/frame and path-order dependence; flat initial-motion and
acceleration controls; explicit flat quotient winding control; null-bivector
obstruction to scalar/norm shortcuts; direction/converse analysis. Mathematical
computation budget used: zero of the one allowed short CPU exact controls.
No GPU, production solve, timeout, fitted profile, external literature browse,
source-wide reproof, empirical validation, formal proof assistant or new premise
audit was run. Parent closure owns required repository regressions and full406.
No claim of different-model or human review is made.

Reviewer: /root/aci_math, actual fresh separate context; Codex/GPT-6 family,
inherited model (no more specific deployment identifier exposed in this context).
No other subagent was spawned. Protected atlas/owner-audit/pair-response/G88
payloads were not read, hashed or cited. A resolved-path deny-prefix guard ran
before hashing the exact listed scientific sources; only baseline path metadata
was visible in git status. SOURCE_PINS records complete-file hashes as byte
correspondence, while only named bounded excerpts entered model context.
