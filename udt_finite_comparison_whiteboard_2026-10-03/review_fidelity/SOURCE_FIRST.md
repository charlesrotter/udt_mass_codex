# FCW1 source-first fidelity and physical-scope audit

Verdict at source-first seal: conditional results below are VERIFIED-WITH-CAVEATS.
They do not establish a native UDT law or admit a supplied metric physically.
Review context, exposure, frame, resources and omitted work are in the sealed
SOURCE_FIRST_PLAN. Parent's continuing startup is attributed, not independently
repeated. Exact source bytes are in SOURCE_FIRST_DESIGN_SEAL.json. This report
precedes access to all FCW1 proposer/parent proofs, code and results.

## 1. Existing authority does not supply scalar closure

ECS1 gives q=p/(2-p^2) for its space-form clock sheet and prepared direct echo,
with positive p,q and 0<p<sqrt(2). Its general transverse H witness preserves
only clocks/rays/preparation in that sheet. Its reviewed source explicitly
leaves all-observer/all-direction inference open. RCD1's different comoving
protocol has q(L)=p(2L)/p(L) for every positive scale history: even there this
uses two p values, not a universal single-argument scalar function of p(L).

ULC1 says one governing law applies to all observers while comparisons may
depend on circumstances. It neither supplies nor excludes an additional
single-valued q=Q(p). W4 supplies a common metric clock/null interface; W5 does
not reduce all observer data to the scalar pair depth. GR FILTER ONLY neither
selects the product example nor imposes Einstein dynamics to exclude it.
The product has non-Einstein Ricci at nonzero curvature and is not a native-
admitted UDT countermodel. The result below tests scalar sufficiency in this
supplied kinematic family, not complete UDT consistency or insufficiency.

## 2. Independently reconstructed tilted echo

Take the supplied product metric, in curvature units k=1,

    g=-dt^2+cosh(t)^2 dx^2+dy^2+dz^2.

At t=0, A(s)=(gamma s,0,u s,0) and B(b)=(gamma b,L,u b,0),
gamma^2-u^2=1, are unit geodesics. The x-directed initial segment has proper
length L and its connection vanishes along t=0, so transporting A's velocity
produces exactly B's initial velocity. This is the PSW preparation in the
product, not a freely chosen Doppler mismatch. Set v=u^2>=0.

The dS2 embedding invariant between base endpoints is

    Z=cosh(gamma x)cosh(gamma y)cos L-sinh(gamma x)sinh(gamma y).

For the local selected product null geodesic the timelike base proper separation
equals the Euclidean transverse displacement |u(y-x)|. Thus Z=cosh(u(y-x)),
or the exact incidence function is

    F(x,y;L)=cosh(gamma(y-x))-cosh(u(y-x))
             +(cos L-1)cosh(gamma x)cosh(gamma y)=0.

The first arrival solves F(0,b;L)=0; the actual return solves F(b,a;L)=0 on
the future roots b~L,a~2L. Nearby emissions keep the worldlines fixed, giving
p=-F_x/F_y at (0,b), q=-F_x/F_y at (b,a). The null invariant is an independent
geometric derivation, not ECS1's scalar relation inserted as propagation.

The independent script constructs the degree-eight Taylor polynomial directly
from those cosh products, solves the arrivals and differentiates F. It obtains

    p=1+(v+1)L^2/2+(v+1)(4v+5)L^4/24
        +(v+1)(24v^2+82v+61)L^6/720+O(L^8),
    q=1+3(v+1)L^2/2+(v+1)(18v+19)L^4/8
        +(v+1)(734v^2+1652v+921)L^6/240+O(L^8),
    (2-p^2)q-p=-v(v+1)^2 L^6/3+O(L^8).

The analytic remainder follows locally from F: dividing F by L^2 after writing
b=L B and a=L A yields a regular analytic implicit problem at B=1,A=2, with
nonzero future-root derivatives. Parity makes clock-ratio expansions even.
These are small-separation conclusions, with no explicit finite-L bound.

For u=0, p=sec L spans an interval above 1 and enforces Q(p)=p/(2-p^2) there.
For each fixed u!=0, p also spans such an interval monotonically at small L,
but the nonzero sixth-order coefficient violates that same Q. Hence no single
scalar Q fits all these laboratories at matched p in the supplied product.
Restoring units multiplies the displayed residual coefficient by k^6.

This is stronger than failure for one aligned sheet and narrower than general
metric reconstruction. The nonzero tilt is an operational way to reach hidden
geometry. The initial clock plane is not curvature-invariant: R(U,e_x)e_x is
proportional to gamma e_t, outside span{U,e_x} when u!=0. A totally geodesic
surface containing that plane is therefore unavailable. A single tidal vector
R(U,e_x)U lying along e_x would not establish full plane closure. This geometric
observation alone does not predict the first failing order: the fourth-order
scalar discriminator cancels, as the preserved first failed run demonstrates.

## 3. Conditional regular conformal endpoint

Retain RCD1's supplied flat homogeneous/comoving sector only, without its
UNADOPTED response equation. Write g=Omega(eta)^-2(-deta^2+dmathbf{x}^2),
Omega(0)=1, Omega>0 for 0<=eta<L*. First emission eta=0 and initial proper
separation L give arrival eta=L. Ordinary proper time and endpoint frequency give

    t(L)=integral_0^L ds/Omega(s), p(L)=1/Omega(L),
    q(L)=Omega(L)/Omega(2L), provided 2L<L*,
    H=-Omega', R=6(2Omega'^2-Omega Omega'').

Assume additionally smooth extension to eta=L* with Omega(L*)=0 and
Omega'(L*)=-h<0. This is a regular simple defining-function zero and is an
UNADOPTED condition, not supplied by the open working meaning of X_max.
For Delta=L*-L,

    Omega=h Delta+O(Delta^2), Delta p -> 1/h,
    t=-(1/h)log Delta+constant+O(Delta), H -> h, R -> 12h^2.

Thus the conformal endpoint occurs at infinite comoving proper time with a
simple-pole first tick ratio. The boundary is spacelike in the regular flat
conformal metric because dOmega is timelike there. These are sector-specific
asymptotics, not an exact de Sitter metric, a globally selected history or a
physical distance law for general observers.

The actual echo ceases at L=L*/2 in this domain: q diverges there while the
first p(L*/2) is finite. The first reception limit is instead L=L*. These are
distinct operational domain statements. Neither is an identification with
physical X_max, a material wall, preferred center, cutoff or selected scale.

Controls Omega=(1-L/L*)^beta, normalized by L*=1 for the symbolic check:
beta=1 has a regular simple zero, logarithmic infinite proper time and H=1.
beta=2 also has p->infinity and infinite proper time, but Omega'=0 at the
endpoint and H,R->0; it violates the nondegenerate endpoint assumption.
The optional beta=1/2 reaches p->infinity at finite proper time with singular
Omega', H and R, violating smooth completion. Merely asking for divergent
received slowing selects none of these rates or proper-time conclusions.

Moreover Omega_epsilon=Omega exp(epsilon B), for any smooth compact interior
bump B supported away from eta=0 and eta=L*, stays positive and retains the
complete endpoint germ and normalization while p changes by exp(-epsilon B).
Echoes change when their arrival arguments meet the support. All real epsilon
are allowed kinematically. This explicit family disproves uniqueness from this
endpoint condition within the supplied sector; it does not prove arbitrary
histories satisfy UDT or that no stronger native connection exists.

## 4. Exterior network ambiguity is prior ICN1 evidence

ICN1 REVIEWED_RESULT already states the smooth compact conformal rescaling
supported away from every clock, and its INITIAL_CANDIDATE section 6 is the
historical derivation target. Null curves retain their unparameterized paths;
if g_tilde=e^(2psi)g then k_tilde=e^(-2psi)k is affine along the same null ray.
Proper observer vectors scale as U_tilde=e^(-psi)U, so endpoint frequency scales
as e^(-psi). With psi zero on clock neighborhoods, their proper clocks, geodesic
motion and all selected null-incidence timing maps are unchanged. Sequential
relay timings made solely from those maps are likewise unchanged.

This is the existing ICN1 supplied-geometry ambiguity, not a novel FCW theorem.
It does not establish full optical-screen, pair-data or tidal blindness, nor
preservation of any selected physical field equation or native admissibility.
Positive conformal factors preserve causal curves but interior curvature can
change; no claim of general all-observer record equality follows.

## 5. Evidence and independence limits

Independent implementation uses Python 3.10.12 / SymPy 1.13.1, four symbolic
families and 17 passing finite checks, captured in 11.36 seconds at about
61 MiB max RSS with 2 GiB virtual-address limit, one BLAS thread and no timeout.
The initial fourth-order assertion failed in 10.29 seconds; unchanged initial
code, stdout/stderr/receipt and ORDER_CHECK_REPAIR preserve the cancellation.
This is one same-premise extraction repair, not a removed adverse metric.

Fresh context is real; inherited model is shared, exact backend not exposed.
Code/argument were independently arranged from source geometry. Existing source
proofs, definitions and target trajectories were exposed; FCW new candidate,
peer proofs/results and parent new code were not. Different-model/library,
formal proof and human-review axes are UNTESTED. General geodesic solves,
all-metric classification, empirical data, full prior-package replay, physical
adoption, source/carrier/matter work and registry regrading were not performed.
