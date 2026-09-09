# SE1 — local curvature-pattern response to neighboring initial data

Frozen initial candidate 2026-09-09; UNPROMOTED, direct review PENDING.
One local criterion with a lawful matched-data discriminator. Not a new
fundamental equation, complete invariant, conservation law or physical object.

## Premises, methods and exact ceiling

G310/G312 supply the OWNER-PROVISIONAL bounded metric-only vacuum equation
Ric(g)=Lambda g on a connected domain, with spacetime-constant Lambda by
Bianchi. This is not derived from the bare metric or made canon. G303/G315
own the full constraints and conditional metric-development interface.
LE1's full-Weyl diagnostic and NR2's analytic local development argument are
reviewed UNPROMOTED dependencies, used only conditionally at their stated
scopes. NR2's first-harmonic tangent classification is not needed here.

For any actual sufficiently regular oriented local Einstein development,
choose a supplied smooth spacelike slice and future unit normal n. Work on
its local Gaussian neighborhood, before failure of that coordinate method;
use a Fermi-transported orthonormal spatial frame. Smoothness suffices for
the displayed differential identities; all explicit witnesses are analytic.
The directional derivative n(A) refers to this specified geometric normal.
It is not a derivative along an unspecified physically selected observer.

The general statement is an exact instantaneous identity wherever I2!=0.
The examples prove existence of differing local rates on lawful data and
nonclosure by the pointwise tuple (gamma,K,Q). They do not prove genericity,
long-time monotonicity, stability, radiation, carried content, or behavior of
LG2's unspecified gluing collar. No physical premise is added.

## 1. Conventions and the load-bearing identity

Signature (-+++); R^a_bcd=partial_c Gamma^a_db-partial_d Gamma^a_cb plus
the usual quadratic terms. K_ij=-(1/2)partial_t gamma_ij, tau=tr K,
epsilon_123=+1 in the spatial orthonormal frame. D is the spatial metric
connection and curl S_ij=epsilon_(i^kl D_k S_j)l. Define

    E_ij=C_i0j0,
    B_ij=(1/2)epsilon_i^kl C_klj0=-curl K_ij,
    Q=E+iB,
    I2=tr Q², I3=tr Q³, A=1-6 I3²/I2³.                 (1)

Here Q represents the FULL complex self-dual Weyl operator, not merely the
electric tensor. The opposite dual/index convention conjugates Q and A;
one must also reverse the curl sign in its evolution. The frame/observer
representation changes by complex orthogonal similarity, preserving the
traces; orientation reversal conjugates them. A is dimensionless and
invariant under nonzero common Weyl multiplication. It can be complex,
can lie outside [0,1], and is undefined at I2=0, including some nonflat Weyl
tensors. It does not classify all geometries or all Weyl operators.

Ric=Lambda g and dLambda=0 imply divergence-free Weyl. Expanding differential
Bianchi in the Gaussian/Fermi frame, or equivalently using its projected
form with theta=-tau, sigma=-K+tau I/3 and zero acceleration/vorticity, gives

    W := projected nabla_n Q
       = 2 tau Q -3 (KQ)_(sym,TF) -i curl Q,           (2)
    (KQ)_(sym,TF)=(KQ+QK)/2-tr(KQ)I/3.

The electric and magnetic parts are respectively local(E)+curl B and
local(B)-curl E. Lambda contributes no separate Weyl source term; this
does not make Lambda irrelevant to the initial data or evolved geometry.
METHOD_REFERENCES.md records the primary mathematical convention check.
No electromagnetic/energy interpretation from that source is imported.

Differentiating the traces, nI2=2tr(QW) and nI3=3tr(Q²W), gives

    nA = L_Q(W)
       = 36 I3 [I3 tr(QW)-I2 tr(Q²W)] / I2^4.         (3)

Trace cyclicity shows L_Q(alpha Q)=0 and L_Q([Omega,Q])=0, for any scalar
alpha and any infinitesimal frame generator Omega. Consequently the exact
instantaneous scalar criterion is

    nA = L_Q(-3(KQ)_(sym,TF)-i curl Q).                (4)

The right side equals zero if and only if THIS scalar is stationary at
THIS event in THIS direction. It is not a completeness theorem about the
geometry. In particular I3=0 makes nA=0 for every W at that event; a zero
first derivative there need not persist. Nor does stationarity imply that
W is only multiplication plus a frame commutator. Preservation on an
interval requires this criterion throughout that interval with I2 nonzero.
The split into spatial and local terms depends on the supplied normal;
the scalar and its derivative along that fixed normal do not depend on
the spatial frame. Spatial variation alone does not force nA!=0.

This identity is not a closed differential equation for A alone. More
strongly, the next construction shows that even knowing full Q and K at
one point cannot remove the needed neighboring initial data.

## 2. Lawful matched-point comparison, not freely invented curvature

On the same supplied split translation T³ quotient, let x have period2pi
and choose unit initial spatial metric and T0=1. Transverse periods are
arbitrary positive supplied constants. All units, quotient, marking and
profiles here are free-and-explored initial/query data, not UDT selections.
Fix e=1/6 and compare m=0 with m=1 in

    q=e cos(mx), gamma=I,
    K=diag(1/3-3q²/4, -2/3-q, -2/3+q), Lambda=0.      (5)

The m=1 datum was first reconstructed independently by the reviewer from
NR2's f=w=r=0,p=cos x chart; the author subsequently derived the matched
homogeneous comparator and recomputed it by a distinct method. The m=0
datum is not attributed to NR2's first-harmonic tangent theorem. Its full
constraints and analytic existence hypotheses are checked directly here.

Both metrics are positive, globally periodic and analytic. R3=0 and the
sum of pairwise eigenvalue products of K vanishes identically in q, so

    H=R3+tau²-tr K²=0,
    M_x=-partial_x(K22+K33)=0, M_y=M_z=0.             (6)

All original constraints hold pointwise on the entire compact slice.
Apply the explicitly conditional analytic method already assessed in NR2:
solve all six Gaussian spatial equations

    gamma_dot=-2K_cov,
    (K_cov)_dot=Ric3+tau K_cov-2K_cov K_mixed.         (7)

The positive metric makes the analytic system solved for all six pure
second time derivatives noncharacteristic. Analytic CK gives local
solutions, not merely formal jets. A finite compact cover, analytic
uniqueness and the fixed translation transitions glue them to a common
positive local slab for each supplied datum. For this finite pair one may
take the smaller interval; no uniform interval over arbitrary profiles,
frequencies or amplitudes is claimed. In the reduced solutions the residual
C=Ric00 and D_i=Ric0i satisfies

    C_dot=2 div_gamma(D^sharp)+2tau C,
    (D_i)_dot=(1/2)partial_i C+tau D_i.

Zero constraint data and analytic uniqueness give C=D_i=0. Thus these are
actual local solutions of the FULL admitted vacuum equation. The analytic
existence theorem and Bianchi propagation, not the finite checks below,
justify this passage. No smooth Sobolev stability or global time claim.

At corresponding marked points x=0, both data have the same gamma,K,
full E and B=0 (and the same first spatial derivatives of gamma,K):

    E=diag(-5/12,5/32,25/96),
    I2=1225/4608, I3=-625/12288, A=20449/117649.      (8)

But B being zero at a point does not make its spatial curl zero. Direct
variation of spatial Ricci at the flat initial metric gives

    (Ric3_mixed)_dot=diag(0,-q'',q''),
    E_dot=2tau E+diag(0,m² e,-m² e) at x=0,
    B_dot=0 there.                                  (9)

For clarity this follows from the full flat-metric first variation
delta Ric_ij=(partial_k partial_i h_kj+partial_k partial_j h_ki
-Delta h_ij-partial_i partial_j tr h)/2 with h=-2K, and from
K_mixed_dot=Ric3_mixed+tau K_mixed. It does not substitute the proposed
Bianchi equation into its own check. KE is pure trace in (5), so at this
event the local contribution is common multiplication only. The rate is

    nA=2592 m² e²(e-2)(e+2)/(3e²+4)^4,
    nA|m=0=0,
    nA|m=1=-5930496/5764801 !=0.                    (10)

The simplified formula is used only on the ORIGINAL domain I2!=0;
e=+-2/3 gives I2=0 and is excluded even though cancellation leaves a
finite expression in (10). The chosen e=1/6 is safely in the domain.

Thus there is no universal pointwise function of (gamma,K,Q) that returns
nA for all these lawful developments with the stated normal. Neighboring
Cauchy data genuinely matter. This does not exhibit different futures for
the same complete initial data: the two full K fields differ away from
the point. The admitted equation already supplies the conditional local
evolution once legitimate complete initial data are supplied; this result
does not require an additional physical law selecting those data.

## 3. Independent author geometry check and surviving controls

Before seeing the reviewer witness, the author used NR2's distinct member
u=e cos x, v=0, V=0, s=-2/3, Lambda=0 with

    gamma=diag(1,exp(2u),exp(-2u)),
    K_mixed=diag(1/3-3(u')²/4,-2/3,-2/3).            (11)

The full spatial connection computation yields R3=-2(u')², zero full
constraints, and actual local analytic developments by the same explicit
method. At x=0, B=0, curl E=0 and

    E=diag(-4/9,2/9+e,2/9-e),
    E_dot=diag(8/9,-4/9+e,-4/9-e),
    curl B=diag(0,e,-e).

With d=9e/2, A=d²(d²-9)²/(d²+3)³ and
nA=162d²(d²-1)(d²-9)/(d²+3)^4>0 for0<|d|<1.
Both the local trace-free term and spatial curl contribute here: respectively
2d partial_d A and d partial_d A. This corroboration refutes neither
preserving examples nor the relevance of local deformation; it also prevents
reading (10)'s negative sign as a universal decreasing-pattern law.

The LE1 Kasner controls survive. K_i=-p_i/T and E_i=-p_jp_k/T² give KE pure
trace, curl Q=0 and Q_dot=2tau Q. A is constant, including nonzero constant
A in nonflat non-Taub examples. Changing overall curvature strength is not
automatically changing this shape diagnostic. No finite-time result for
the unspecified LG2 collar is inferred from either family here.

## 4. Evidence logic and omissions

check_geometry.py was written before exposure to reviewer SF3. It reconstructs
all spatial Christoffels/Ricci/momenta and independently varies those tensors
under ADM for (11), checks full electric propagation, exact invariant rates
and Kasner controls. It detects omitting curl B or the inverse-metric
derivative. check_matched_data.py was written after reviewer SF3 exposure,
but before reading reviewer code; it uses the independent flat Ricci
variation for (5), not the reviewer's 4D tensor-jet engine. It detects the
cancelled-denominator false pass explicitly. Both initial runs passed.

The fresh source-first review independently found (5), obtained the full
4D curvature and normal derivative from metric third jets at two events,
checked every Ricci and normal-Ricci component, and independently expanded
the general Bianchi projection including noncommuting tensors. Source-first
does not mean hypothesis-blind; same-model/different-model provenance is
UNKNOWN and different-library independence is not claimed. The author's
matched comparison intentionally uses that disclosed review finding.

Direct adversarial review of THIS frozen candidate is still required.
Exact checks support the displayed algebra; they do not prove the general
analytic existence theorem, infinite-time persistence, completeness,+genericity or any physical identification. No numerical integration,
observations, calibration, protected payload or new physical law is involved.

The full365 premise audit actually fails at pre-existing G325 replay; later
gates were unreached. This blocks promotion/full integration, not saving
this explicitly UNPROMOTED result. Registry, premises, canon and fixed
manuscript remain unchanged. No successor campaign is authorized.
