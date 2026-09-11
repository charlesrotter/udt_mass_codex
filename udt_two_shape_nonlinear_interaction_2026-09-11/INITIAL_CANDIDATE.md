# TI1 — mixed curvature and retained pair information on actual local developments

CONDITIONAL CANDIDATE, UNPROMOTED; fresh adversarial review pending.
Baseline grok b318072a9403d6acdd3a6d5749e1b366d76d29c5. The authorized WORK_ORDER.md,
DISCOVERY_AND_DATA_FREEZE.md, launch receipt and source pins govern scope and discovery history.
This initial candidate must be preserved if review requires repair.

## Result and ceiling

Within the supplied Ric(g)=0 equation and the compact analytic family below, two transverse
components with a nonaligned relative phase produce a nonzero curvature pseudoscalar on the
initial slice. Its nonzero value is independent of observer and survives on a data-dependent
local time interval. It vanishes in the one-component/aligned polarized controls. This establishes
a geometric distinction beyond constant-basis rotation of those controls. It does not establish
new dynamical generation, energy transfer, growth, long-time persistence, stability or genericity.

All normalized directional pair-germ matrices agree throughout the common Gaussian chart,
even though the joint and polarized solutions have different curvature. Original ruler densities
and suitable common derivatives recover the diagnostic on the initial slice. These are actual
smooth records of the same local solutions, not unrelated arbitrarily specified jets.

The exact value depends on the chosen higher-order completion. A leading mixed coefficient
survives the displayed tangent-preserving homogeneous freedom; other completions remain
unclassified. Nonzero behavior is not universal outside the chosen neighborhood.

G388/G389 supply the reviewed constraint/local-development method; G394 supplies the polarized
comparison; G405 supplies the exact common-record interface. Their full original arguments and
reviews, qualified by the later BANKING_RECORD.md, own accepted scope. G312 is GR FILTER ONLY:
Ric=0 is expressly supplied here, not UDT's derived or adopted native dynamics. G176 remains
WORKING; G166 does not admit the unrestricted metric envelope as derived native UDT solutions.
The event/history-to-depth assignment and physical acquisition remain OPEN. No promotion or canon.

## 1. Complete chosen data, phase and exact constraints

Use the supplied split T3 with X-period2pi, fixed positive y,z periods, T0=1 and the calibrated
background normalization gamma0=I. Let A,B,c be real and theta a real phase. On the initial slice:

    s=-2/3+c, p=A cos X, r=B cos(X+theta), d=p^2+r^2,
    H=[[p,r],[r,-p]], kappa=(d-s^2)/(2s),
    gamma=I, K=diag-block(kappa, s I2-H), K_XA=0.

Here K=-partial_T gamma/2. Neither H nor K introduces a physical field, polarization identity,
action or momentum. The supplied quotient/background/equation/Gaussian comparison are
pinned-by-HABIT for the declared comparison; amplitudes, phase and completion are
free-and-explored. Standard geometric implications are pinned-by-THEORY only under the exact
source hypotheses, not by method prose. Calibrated c_E=1 selects no absolute size.

The declared near-background domain is

    |A|<1/4, |B|<1/4, |c|<1/6, theta arbitrary modulo2pi.             (1)

Thus -5/6<s<-1/2, d<1/8, and kappa>1/8. To see the last bound, put x=-s>1/2;
kappa=x/2-d/(2x)>x/2-1/(16x)>1/8. This is a sufficient chosen domain, not a sharp,
physical or uniquely selected boundary.

The initial spatial connection/curvature vanish. With tau=trK=kappa+2s,

    R3+tau^2-tr(K^2)=4s kappa+2s^2-2d=0,
    D_j K^j_i-partial_i tau=0 for i=X,y,z.                           (2)

For i=X the two kappa derivatives cancel and s'=0; transverse components vanish because
the fields depend only on X and K_XA=0. No constraint was dropped. Dropping the quadratic
longitudinal correction by taking kappa=-s/2 instead gives Hamiltonian residual -2d.
The quadratic correction and generated higher harmonics are part of the exact data.

In NR2's coordinates this is the velocity-only f=w=0 sector; V=-H and M=I. NR1's quadratic
phase-balance condition is zero because the initial shape displacement is zero. It does not
forbid relative phase between the two initial shape velocities.

For A=epsilon a, B=epsilon b and analytic c(epsilon)=O(epsilon^2), the complete first-order
data are exactly the two velocity components of the G327 sector. Holding a nonzero c fixed
instead changes the zero-amplitude background. Both are permitted data, but only the first
asserts the original radial tangent. No general two-parameter theorem is inferred solely
from NR2's single-parameter statement; the following interface is checked directly.

## 2. Actual jointly analytic local solutions

In Gaussian coordinates g=-dT^2+gamma_ij dx^i dx^j solve all six spatial equations using

    partial_T gamma=-2K,
    partial_T K=Ric3+tau K-2K gamma^-1 K.                            (3)

This is solved for all six pure second normal derivatives of gamma. The right-hand side
is analytic on positive gamma and contains spatial derivatives of order at most two, with
invertible highest normal coefficient. The data are jointly real analytic in X,A,B,c,theta
where s!=0. Treat A,B,c,theta as additional mathematical independent variables with zero
parameter derivatives in the operator. The same noncharacteristic analytic CK method used
and reviewed in NR2 then supplies joint analytic local solutions; these parameter variables
are not physical dimensions. Finite covering and uniqueness on the compact slice and any
fixed compact parameter subbox inside(1), with the phase circle covered by finitely many
charts, give a common local time slab after shrinking. No uniform prescribed duration over
unbounded parameters or a global Gaussian chart is claimed.

Periodicity and overlapping chart solutions agree by analytic uniqueness; positivity and
Lorentzian signature persist on a smaller slab. To recover the original equations rather
than only their spatial part, put E_ab=Ric_ab, C=E_00, D_i=E_0i. Spatial equations give E_ij=0.
The full contracted Bianchi identity in this convention yields the homogeneous propagation
system used in NR2:

    partial_T C=2 div_gamma(D^sharp)+2tau C,
    partial_T D_i=(partial_i C)/2+tau D_i.

The exact constraints set C=D_i=0 initially. Analytic uniqueness makes all of them zero on
the local slab. Thus these are actual local Ric=0 developments, not only compatible finite
jets or a formal power series. The standard CK theorem is an explicitly credited method,
not re-proved or machine-certified here. This application claims no new existence theorem,
smooth Sobolev well-posedness or long-time stability. The raw metric-jet calculation below
independently checks all16 initial Ricci entries but does not substitute for this argument.

## 3. Geometric comparison with signs fixed

Use signature(-+++), R^a_bcd=partial_c Gamma^a_db-partial_d Gamma^a_cb
+Gamma^a_ce Gamma^e_db-Gamma^a_de Gamma^e_cb, and epsilon_0123=+1 on the initial orthonormal
frame (partial_T,partial_X,partial_y,partial_z). Star acts on the FIRST antisymmetric pair:
(*C)_ab cd=(1/2)epsilon_ab^ef C_ef cd. Define

    E_ij=C_i0j0, Bmag_ij=(*C)_i0j0,
    J=E_ij Bmag^ij, P=C_abcd(*C)^abcd=16J.                          (4)

E and Bmag are standard electric/magnetic names for Weyl tensors, not electromagnetic
fields or physical identifications. P is a spacetime pseudoscalar; its sign uses the supplied
orientation, while nonvanishing and P^2 do not. It is independent of a different choice of
unit observer. Initial Ric=0 makes C=Riemann.

Gauss/Codazzi, or direct four-dimensional metric reconstruction using (3), gives

    E=diag-block(2s kappa, -kappa(s I2+H)),
    Bmag=diag-block(0, [[r',-p'],[-p',-r']]),
    J=-2kappa(p r'-r p')=2kappa A B sin(theta).                     (5)

The partner's separate raw metric-jet implementation constructs Christoffels, all Riemann
entries, all Ricci entries and the Lorentzian Hodge star; it checks *^2=-1 and the full
contraction factor16. Parent reconstructs E and curl K from actual record jets by Gauss/Codazzi.
Their prior formula exposure is disclosed; neither is the later fresh adversarial review.

If AB sin(theta)!=0, (1) gives |J|>|AB sin(theta)|/4 at every initial X. Compactness and
continuity of the actual analytic solution therefore preserve nonvanishing, and its sign
under the chosen orientation, on some data-dependent positive time interval about T0.
There is no claimed positive bound uniform as AB sin(theta) tends to zero, and no computed
finite-time trajectory or growth law.

For quadrature theta=-pi/2:

    J=AB(s^2-A^2 cos^2X-B^2 sin^2X)/s.                             (6)

Setting either component to zero or aligning their phases makes J=0. These controls are
locally polarized: their transverse H is one scalar function times a fixed symmetric matrix,
diagonalizable in a constant local transverse basis. The initial data then have transverse
reflection symmetry, which (3) preserves by analytic uniqueness. At each local point a
reflection fixing that point reverses orientation, so P=-P and P=0 throughout the local
development. A rotated transverse basis need not be a legal automorphism of the supplied
torus lattice; only this local symmetry conclusion is used.

For the joint case,

    [H(0),H(pi/2)]=[[0,-2AB sin(theta)],[2AB sin(theta),0]]!=0.       (7)

Simultaneous constant diagonalization of gamma=I and all K_AB would diagonalize the
endomorphisms gamma^-1 K and force commutation. Equation(7) rules this out even before
restricting to lattice-preserving changes. An X-dependent basis can change component
appearance; it cannot remove the nonzero pseudoscalar. No classification of all metrics,
or invariant preferred decomposition of a general metric into two shapes, follows.

## 4. Completion dependence, expansion and cancellation

For complete chosen data, (5) is required by the supplied equation; the full data themselves
are permitted choices. Changing c changes s and kappa and hence the exact J. For fixed
a,b,theta and analytic c(epsilon)=O(epsilon^2), on the compact initial circle,

    J(epsilon,X)=(2/3)epsilon^2 a b sin(theta)+O(epsilon^4).         (8)

The remainder is uniform in X for this fixed analytic c and sufficiently small epsilon:
s stays bounded away from zero, c=O(epsilon^2), and d=epsilon^2 times a bounded trigonometric
function. Thus the displayed homogeneous completion cannot remove that leading coefficient.
This is not a statement that arbitrary other exact completions have been classified.

The coefficient in(8) can already be obtained by multiplying the first-order Weyl pieces.
A first-order expansion of J itself loses it, but linearized curvature contains that information
when used to compute the quadratic diagnostic. The exact family establishes realizability,
completion dependence and controlled local persistence; scalar multiplication alone is not
evidence for a new nonlinear dynamical coupling law.

Outside(1), choose any s!=0 and p=s cosX,r=s sinX. Then d=s^2,kappa=0 and J=0 despite
noncommuting transverse shapes and generally nonzero Bmag. These complete analytic data
still satisfy(2), and the same local method applies. This is an initial-slice cancellation
control only: no persistence of its zero J is asserted. It refutes a proposed universal
claim that two nonaligned shapes always give this invariant. It does not erase the scoped
nonzero result within(1) or classify all cancellations.

## 5. Lawful pair-record join and exact information loss

For each fixed nonzero v, use the actual rank-two surface
F_(a,v)(T,sigma)=(T,a+sigma v), restricted to the common local patch. Its commuting columns
and original clock Kclock=partial_T share one geometry and marking. Gaussian g gives

    h_v=diag(-1,gamma(v,v)), det h_v=-gamma(v,v)<0,
    T_v=1, m_v=sqrt(gamma(v,v)), B_v=0, Phi_v=0,
    H_v=diag(-1,1), det H_v=-1.                                   (9)

These are precisely G405's completed-pair formulas at N=1,beta=0. H is a pointwise normalized
Gram matrix. Consequently all such normalized H fields, including the chosen six, agree
for the joint and polarized actual solutions throughout their common Gaussian domains,
despite the invariant distinction. Their scalar Phi readouts also agree. This conclusion
does not identify native physical pair populations or fill in G166's event/path assignment.
The hypersurface-normal observer has zero rotation W, a consistent control distinct from P.

Retain the original directions D={eX,ey,ez,eX+ey,eX+ez,ey+ez}, common chart and densities.
Put q_v=m_v^2. Standard polarization reconstructs

    gamma_ii=q_i, gamma_ij=(q_(i+j)-q_i-q_j)/2.

At T0 all q are 1 or2 regardless of amplitudes. Even the unnormalized instantaneous pair
values therefore fail to distinguish this initial family. In contrast,

    qdot_v=-2K(v,v), partial_X qdot_v=-2(partial_X K)(v,v).          (10)

The same polarization reconstructs all K and K_X from those common derivatives. With the
supplied initial gamma=I, its vanishing spatial curvature/connection, orientation and the
conditional Ric=0 equation, E=tau K-K^2 and Bmag_ij=epsilon_i^kl partial_k K_lj recover J.
This sufficient data set is not claimed minimal. Only X derivatives are needed because
the stated family is transversely translation invariant. A general metric would require
its full appropriate spatial derivatives and curvature; no general reduced-jet inverse
theorem is claimed. Actual smooth solution records supply all compatibility hypotheses.

Dropping mixed directions loses off-diagonal K; dropping density or its time/spatial
derivatives loses relevant information. No instrument transfer or observation is proved.
Nor are full time-live tape metrics identical: s_tape(T,sigma)=integral_0^sigma m(T,u)du
has alpha=partial_T s_tape, so its coordinate metric is

    -dT^2+(ds_tape-alpha dT)^2.

The fixed-tape clock differs from the original tangent partial_T|s+alpha partial_s. For
the G405 control m=exp(T), alpha=s_tape and the fixed-tape clock rate is sqrt(1-s_tape^2)
where timelike. Confusing this with(9) changes the query and cannot establish a native
depth/history law. G405's full marking/density limits are retained.

## 6. Evidence and return

Actual launch full395 premise audit: PASS, exit0,407.580seconds, saved streams,2GiB/900s.
Parent record script:23 exact named identity checks and6 explicit invalid-control witnesses,
PASS,4.859seconds, Python3.10.12/SymPy1.13.1. Construction raw-geometry check:18 grouped checks,
including all16 Ricci entries, PASS,2.27seconds; component counts include structural identities
and are not independent proofs. Deliberately invalid equation controls must fail and are kept.
Metadata capture failures/repairs are recorded separately; no failed science is silently upgraded.

The return is a conditional mixed-curvature/readout result on actual local solutions. Roadmap
stage4 gains a controlled two-shape comparison; it does not complete nonlinear dynamics or
stage5 global reach. Fresh adversarial review is required before a reviewed disposition.
Any later acceptance must be separately authorized at the exact reviewed scope. An unresolved
physical identification is not a prerequisite to accepting a valid conditional mathematical
result, but this research authorization itself does not promote it.
