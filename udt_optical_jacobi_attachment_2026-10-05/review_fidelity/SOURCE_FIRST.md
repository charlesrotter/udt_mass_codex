# OJM1 fidelity review — sealed source-first assessment

Reviewer: `/root/ojm_fidelity`, fresh separate agent context, inherited GPT-6
model identity (no different-model/human claim), 2026-10-05. This context has
read no OJM1 parent candidate, code, result or peer derivation. The only OJM1
scientific input read is WORK_ORDER.md. Parent continuing-session startup and
premise checks are attributed to parent, not independently rerun here. Direct
`git branch --show-current`, `git rev-parse HEAD`, `git rev-parse origin/grok`
gave grok and 278a8f126dc7a1283c0c2dcdb074c183fce7cdde twice. `git status` showed no
tracked dirt; package and existing untracked names were visible and untouched.
Protected payloads were neither read nor hashed. Review writes stay here.

Read AGENTS, CLAUDE How we work/DRIVER TRIGGERS/Repo discipline, LIVE current
block, no-shortcuts/completeness-map/verifier-before-record/solver-first skill
protocols. Parent startup owns the other bounded orientation reads and verifier.
Load-bearing sources: central R8ACP/R8CGE/R8CPR/R8OAA, R13, R16, current R18
comparison/attachment paragraphs; original G348 exact derivation and its exact
registry row; original CPR1/OAA1 INITIAL_CANDIDATE and CLARIFICATIONS. The
conditional equation class remains conditional and source history supplied.
G348's registered status remains externally accepted derived conditional bounded.

## Independent reconstruction before exposure

Use the supplied outward equatorial future null geodesic, Killing energy one,
s(r)=sqrt(1-f(r)b²/r²), P=integral_a^R b dr/(r²s), and
I=integral_a^R dr/(r²s³). The source bound gives s>0 uniformly near a strict
limiting b. Vary b at a fixed source event, evaluate the connecting field at
fixed r=R, and work in the quotient to remove the difference from fixed affine
parameter. Then delta t=b I delta b, delta phi=I delta b and
|delta x|=R s(R) I |delta b|. Its source quotient initial derivative has norm
|delta b|/[a s(a)]. Independently rotating the orbit plane about the source
radial axis gives displacement R sin(P) delta i and source slope
(b/a) delta i. In parallel, reflection-adapted orthonormal quotient frames:

    B_parallel=a s(a) R s(R) I,
    B_perp=a R sin(P)/b.

At b=0 both continue to R-a. The signed perpendicular factor is needed;
discarding its sign before locating caustics loses parity information. Constant
endpoint screen rotations only rotate the diagonal map. G348's reversal gives
B_eo=-B_oe^T, hence the source-size-from-sky differential is
J=-omega_o B_eo=omega_o B_oe^T. The actual angular-from-size map is J^{-1}
only off caustics. A quoted source-to-sky map must distinguish these directions.

The circular source rest screen consists of quotient representatives shifted
by g(X,u_e) k/omega_e. This is an isometry; it does not add an independent
Doppler stretch to its lengths. A supplied material disk plane need not be this
screen and its projection is additional source geometry. Likewise a new
receiving observer changes omega_o and angular scale physically; positive affine
rescaling changes B inversely and leaves J invariant. G348 proves metric-area
reciprocity only; no flux or material emitter is supplied.

The ray family variations are geodesic Jacobi fields. Direct differentiation
of the plane-rotation solution gives B_perp''=-3mb² B_perp/r^5 in affine
parameter. Null Ricci contraction vanishes, so the other eigenvalue is opposite:
B_parallel''=+3mb² B_parallel/r^5. This is a consequence of this conditional
metric, not an added propagation law. The two factors generally differ when
mb is nonzero. Ric(k,k)=0 does not suppress Weyl shear.

B_parallel>0 for R>a. Other endpoint conjugacies occur when P=n pi, n nonzero;
the full phase transport survives, while J loses rank and its inverse fails.
For small b the entire segment has |P|<pi and is nonconjugate. A proof for this
domain must not become a universal no-caustic assertion. Outgoing source
regularity alone does not obviously bound P below pi near a=3m and near-tangent
launch; frozen numerical controls below test that potential counterexample.

Writing S=sqrt(1+H²b²), the generic strict limiting branch has

    D_A,infinity = (a/H) sqrt(abs(s(a) S^3 I_infinity sin(P_infinity)/b)).

It need not equal the affine endpoint 1/H. When sin(P_infinity)=0 the leading
limit vanishes and the next term matters. On the b_*=0 preparation, incidence
gives b(R)=Omega a/(H² R)+O(R^-2), not b identically zero. Smooth even dependence
of the optical factors implies D_A-D_o=O(R^-2) or smaller; this suffices to
retain D_A=1/H-(a/H+E/H²)/R+O(R^-2) and
Z(1/H-D_A)->(a+E/H)/sqrt(h). This is a late-tail assertion, with all fixed
history, regularity and conditional-metric hypotheses preserved. No full-history
maximum, universally selected distance or global X_max follows. Physical source
size is supplied for this geometric conversion; known astronomical ruler, disk,+luminosity, observations and metric admission remain separate.

## Review tests frozen before execution

CPU only, at most 2 GiB virtual memory, one BLAS thread, no GPU, no wall/CPU
timeout. Every failure and rerun is retained. Hard implementation cap: 100
named finite cases including reruns; initial suite has 16 cases. Stop on a
resource error or unresolved substantive defect and report the survivor rather
than add a new premise. No parameter tuning to rescue expected outcomes.

Numerical controls are free-and-explored, not physical population choices.
Nine fixed-ray cases: m=1,a=8,H=.01,E=1.2, b=0,1,4 and R=10,100,1000.
For each compare quadrature/closed-variation B with direct DOP853 integration
of the second-order affine Jacobi equations expressed in r. Use float64,
rtol=2e-11, atol=2e-12, acceptance |difference|/(1+|B|)<2e-8 for each component.
Three caustic-domain controls: m=1,a=3.001,H=.01,E=1.2,R=1000,
b=a/sqrt(f(a)) times .99,.9999,.999999. Report P and signed B_perp; no assumed
sign is a passing condition. Four actual-incidence cases: first parameter set,
R=10^3,10^4,10^5,10^6; high-precision quadrature and root solve of
P-Omega U=Omega d, with d=integral_R^infinity dr/[v(E+v)]. At 50 decimal digits
require original incidence residual<1e-35 and strict source regularity. Report
the pole product, expected residue and discrepancy without treating finite
asymptotic error as a failed exact equality. Freeze saved source and script
hashes before running. These finite checks do not certify the whole domain.

At exposure, independently replay selected parent saved quantities with this
implementation, audit source-rest-screen definitions and actual incidences,
then review the final central claim scope. Shared Python/numerical libraries
and same-model limitations remain explicit; distinct implementation and fresh
context do not provide premise independence or empirical confirmation.
