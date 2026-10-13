# GRC1 mathematical direct review — initial findings

Reviewer `/root/grc_review_math`; source-first record predates candidate exposure.
This initial report is saved without reading the sibling review. Exact runtime
model is unexposed; separate context, independently authored argument and check
implementation are supplied, but different-model/human/formal/empirical review is
not. Parent startup is attributed as recorded in SOURCE_FIRST. This report is not
the later integration attestation and cannot confer physical adoption.

**Initial verdict: VERIFIED-WITH-CAVEATS for the inspected conditional mathematics.**
No blocking defect found in A's initial candidate, B's candidate or coordinator
C1/C2. A's forthcoming supplement and actual central integration are not yet
covered. The physical sign/neutrality rules remain unadopted; the finite witnesses
are supplied examples, not native geometry selection.

## 1. A: spherical clock relation and failed recurrence route

I independently followed the argument from E=sqrt(F)omega=sigma k(r), hence
log Z-(1/2)log(F_o/F_e)=log(E_e/E_o)=-integral r''/r'. Because dr is spacelike
on F>0, a radial null vector cannot annihilate r, and sigma cannot change on
a regular branch. There is no missing zero denominator or affine normalization.
Warped-product Ric(k,k)=-2 Hess r(k,k)/r gives the discrepancy with the stated
sign. Both null directions are necessary to force the two-dimensional Hessian
to be pure trace. Its Hodge dual is Killing, and K(r)=0 lifts that symmetry to
the angular warped factor. dF=(Box r)dr and [K,grad r/F]=0 give the normalized
local coordinates and reciprocal static metric; no vacuum equation was used.

Adverse test: directly constructing the connection of h=diag(-q,1/q) gives
Hess r(k_+,k_+)=q_t/q and Hess r(k_-,k_-)=-q_t/q. Thus reciprocal determinant
alone cannot impose NAR. Independently differentiating the null incidence for
q=1+t gives dt_o/dt_e=q_e/q_o and proper interval ratio sqrt(q_e/q_o), opposite
to the proposed endpoint factor sqrt(q_o/q_e). The EF control similarly yields
Gamma^r_vv=(FF_r-F_v)/2, Gamma^r_vr=-F_r/2 and Hess r(n,n)=F_v/2. A single
null direction is insufficient. These are analytic checks, with the diagonal
calculation additionally independently executed.

The recurrence rejection survives: a nonzero radial Lorentz boost has two null
eigenlines and a spacelike kernel; the transverse boost preserves neither null
line. This obstructs a common invariant null line for Schwarzschild curvature
when mu is nonzero. For C² convergence on a common regular patch, normalized
future null directions have a compact unit-sphere limit; curvature invariance
is a closed algebraic condition, so the obstruction passes to the limit.
This conclusion requires the declared C² quiet recovery and says nothing about
weaker convergence, a single ray, or the absence of redshift.

NAR uses generally accelerated areal-radius clocks. They are not PSW1 clocks.
The areal foliation is supplied; covariance does not make it a universal observer
population or a preferred physical center. Radial shear vanishes by symmetry,
but 2r'/r expansion generally remains. Neither all-null Ricci neutrality nor a
finite matched optical contrast follows. r=0, F=0, global extensions and absence
of trapping are not established by this local equivalence.

## 2. B: all-frame sign, optical implication and rigidity

The boost limit is sound with the order of quantifiers stated: first compute
the fixed-laboratory L→0 coefficient, then take eta→infinity in the finite
algebraic tensor. Multiplying by exp(-2eta) leaves Q_k/4. It supplies neither a
uniform physical laboratory size nor a finite-distance bound at arbitrarily
large boost. For every screen vector this gives Q_k<=0. Its two eigenvalues
have mean Delta Ric(k,k)/2, so their trace-free absolute eigenvalue is at most
-Delta Ric(k,k)/2. No energy equation is required or licensed.

The converse fails: D=-B has zero null screen but C=-1. The stronger conjunction
with F forces each screen eigenvalue to vanish. I checked the proposed rigidity
argument: adding the k=u±e1 equations makes the e2 electric sectional contraction
the negative of the e1/e2 spatial contraction; interchange e1/e2 and use pair
symmetry to equate electric diagonals. A common spatial perpendicular compares
arbitrary directions in one rest space. A common two-dimensional spacelike plane
for any two timelike observers identifies their scalar. Polynomial extension and
curvature polarization then give D=kappa B; S imposes kappa>=0. This is a proof
of all-frame scope, not the author's finite null-system rank calculation.

The vertex statistic follows directly by inserting J=lambda I+a lambda³+... into
J''+T J=0, which gives a=-T(0)/6. In two screen dimensions the determinant's
quadratic normalized coefficient is -tr T/6. The subtraction compares matched
source normalizations and affine cuts; its Q is not a propagated difference-beam
equation. Neither unchanged cones nor ordinary clocks imply F.

I recomputed the finite adverse boost at w=1,kappa=2: C=-11/16 while the original
frame has (4,1,1). Thus zero null Ricci trace and one-frame positivity do not
suffice. The cosh control has temporal sectional magnitude1 and spatial magnitude
tanh²t; its C=1+sech²t|m|² is positive while Q=-sech²t I. S does not force the
space-form branch or preserve optical focusing. No counterexample to the stated
conjunction was found.

## 3. Spherical cone, limits and actual quartic clocks

Starting from g=diag(-f,1/f,r²,r²sin²theta), my code reconstructed Christoffels
and curvature without importing producer routines. It recovered all six stated
orthonormal components. The curvature contraction gives
C=beta+(alpha-beta)b1²+(beta-gamma)m1² because |b|²-|m|²=1. The unboosted
transverse plane tests beta; boosts in the two adverse planes in the candidate
make each remaining coefficient necessary. Together with the displayed identity
they prove the exact sign cone, not a finite-plane sampling approximation.

For delta f=-r²q, alpha-beta=(r³q')'/(2r) and beta-gamma=rq'/2. Integration
of q'(r)>=r0³q'(r0)/r³ gives the stated lower bound. A positive derivative
cannot become exactly zero at a later finite radius under these conditions,
yet an integrable r^-3 tail is allowed. The center and infinite-domain caveats
are essential. The quartic difference has Q_radial=(0,0),
Q_tangential=(-4lambda r²,-lambda r²), so it separates radial from all-null
neutrality as claimed.

The finite quartic proof also survives direct examination. The preparation is
parallel along the spatial radial geodesic, and E=sqrt(f(r0)) follows from rest.
The original radial equations give dr/dtau=v, dv/dtau=2lambda r³,
dt/dtau=E/f. Outgoing null incidence defines F=t_B-rstar. Since
dF/dr=1/[v(E+v)]>0, there is at most one intercept. Changing to v removes the
initial square-root singularity. The bound at the lapse zero is positive using
log2>2/3 and rstar(r0)<=64rh/255, whereas F at v=1-E is negative by
E>1/2 and the given 1/[2E(1+E)] bound (here E=sqrt255/16). The intercept is
strictly inside the regular static patch and after p=1. Thus p=E+v>1 and
q=1/(E-v)>1 describe two finite future legs. The latter is not the inverse map.

My independent method integrated the original first integrals in v, rather than
the producer coordinate-time trajectory, then differentiated neighboring proper
arrival maps. At 60 decimal working arithmetic it gives
p=1.0059098196166655731160116455023 and
q=1.0099172783832545544387475644456. Difference from the producer fine finite
differences is about2.46e-12 and1.03e-12. My finite differences at h=2e-6 differ
from endpoint expressions by2.68e-15 and5.49e-15; h=1e-5 gives errors25 times
larger, consistent with the expected centered-difference order. This is a
floating diagnostic, not an interval certification; the analytic sign proof
does not rely on those digits. Raw neighboring emission, proper arrival and
return records and incidence residuals are saved in check_01.stdout.

The held-clock adverse comparison at that arrival radius gives
p_static=0.9980139748745118457<1. The preparation is consequently load-bearing.
Small epsilon gives E=1-epsilon/2, v_arr=2epsilon+O(epsilon²), hence log p's
coefficient3/2 and log q's coefficient5/2; L=r0+lambda r0^5/10+... changes
no leading quartic term. This zero-central-curvature witness does not imply that
S itself controls all finite clocks, that local quadratic signs determine zero
cases, or that the metric is native/stable/typical.

## 4. Mean variant, coordinator tests and physical return

With a declared Ricci-flat reference the leading angular mean depends only on
Ric_g(U,U), independent of reference Weyl and matching. Its all-timelike
nonpositive contraction plus null nonnegative contraction force zero on the null
cone. A symmetric tensor vanishing there is Lambda g; contracted Bianchi on
a connected smooth four-dimensional region then fixes Lambda constant. The
mean sign fixes Lambda>=0. Weyl remains unrestricted. This does not establish a
physical vacuum comparison sector or an ordinary matter equation.

C1: direct null separation gives the positive quadratic root for sigma(tau).
At tau=0 its three derivatives are gamma,(gamma²-1)/b,0, yielding the stated
nonzero negative Schwarzian. The conclusion rejects that naive invariant,
not projective methods in general.

C2: I=Omega Id is indeed the tangent isometry from g to g0. One-raised-index
Weyl is conformally invariant; lowering gives Omega², while pullback on four
covariant slots gives Omega^4. Their difference is therefore
Omega²(1-Omega²)W0, and a nonzero W0 at a point forces Omega=1 there.
Only an open region of such equality fixes derivatives and D=0. This result
belongs to S+F with its canonical matching, not S alone or the mean variant.

The continuation recommendation is physically meaningful insofar as it asks
whether the postulated positional effect entails this clock comparison and what
optical defocusing is allowed. Another arbitrary supplied profile would not
answer that join. The campaign has conditional restrictions and decision-relevant
counterexamples; it has not derived its new inequalities from founding words.
No need to manufacture a mathematical defect or impose another premise to mark
that physical incompleteness honestly.

## Evidence, exposure, caveats and unperformed checks

check_01 was one CPU worker through the unchanged TPS1 capture wrapper, 2GiB
virtual limit, one BLAS thread, no killing timeout, duration1.00s, maxRSS57036KiB,
empty stderr, exit0. CHECK_PLAN was saved before parent clearance and execution.
The implementation uses Python3.10.12/SymPy1.13.1/mpmath1.3.0; no producer script
was read/imported/executed before this check. Saved producer outputs and freezes
were read for direct result comparison. Producer counts remain author regression,
not independent proof. No failure or excluded assertion occurred in this check.

After source-first I read both full initial candidates/freezes, A SOURCES and
spherical/clock-map outputs, B algebra/spherical/arrival outputs, central
INITIAL_CANDIDATE, NOTEBOOK C1/C2/mean-proposal sections, C1 saved output and the
capture implementation. I have not read the sibling review. The author historical
note files and all producer scripts were not substantively read; their contents
are not certified here. Pins bind exact reviewed bytes and captures separately.

Primary references independently inspected online: Abreu–Visser
https://arxiv.org/html/1004.1456 §§II–III for the spherical Ricci/Hodge definitions;
Schmidt https://arxiv.org/pdf/gr-qc/9709071 §4 eqs4.3–4.4 for the pure-Hessian
Killing argument; Galaev https://arxiv.org/pdf/1611.01551 §4.2 for the Walker
recurrence definition. They support mathematical methods; no source equation,
energy interpretation or general holonomy classification is adopted. C2's
Gover–Nurowski conformal weight is being checked directly against its cited page;
the weight above was also independently derived by tensor lowering/pullback.

Not done: global metric classification/realization, PDE evolution/stability,
empirical measurements or native premise adoption; full historical PSW1/PCC1/LKT1
reproof; independent full406 regression (parent owns it); finite-instrument error
certification; source-only independent discovery of the candidates. These are
limits of this review, not reasons to widen or refute its conditional claims.
