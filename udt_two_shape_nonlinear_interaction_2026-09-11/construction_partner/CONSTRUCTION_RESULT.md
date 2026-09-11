# Exact two-rate curvature distinction — construction result, unreviewed

This is a conditional construction contribution, not a fresh adversarial review,
scientific promotion, a native dynamics claim or physical adoption. The permitted
result is a mixed curvature distinction already present in the complete initial
geometry and locally retained in an actual analytic development. It does not
demonstrate newly generated mode coupling, energy transfer or a long-time effect.

The data, conventions, exposure, choice tags and comparison controls were frozen
in CONSTRUCTION_FREEZE.md before scientific confirmation. Source versions and
selected current registry rows are in inputs_serial.stdout. Current banking
G388/G389/G394 and G312 GR FILTER ONLY override their sources' historical status
headings. Parent owns the actual launch full395 audit; this partner did not rerun
that audit or use historical PASS/FAIL text as a current execution result.

## 1. Whole exact data and their NR1/NR2 interface

On the supplied rectangular split T3 with X period 2*pi and fixed positive y,z
periods, use T0=1, gamma=I, signature -+++, K=-gamma_T/2 and Lambda=0. Put

    p=A cos X, r=B cos(X+theta), H=[[p,r],[r,-p]],
    d=p^2+r^2, s=-2/3+c,
    K=diag(kappa,s I-H), kappa=(d-s^2)/(2s), K_xA=0.       (1)

Both independent quantities are transverse shape RATES of an initially flat
metric. They are not two additional physical fields or an initial nonflat metric.
The family is jointly real analytic in X,A,B,c,theta whenever s!=0 and periodic
in X and theta. gamma is positive definite for every member.

The frozen safe box |A|<1/4, |B|<1/4, |c|<1/6 has

    -5/6<s<-1/2, d<1/8<s^2,
    kappa=(|s|-d/|s|)/2>1/8.                            (2)

The last bound follows because u-d/u increases with u>0 and decreases with d;
its infimum on u>=1/2,d<=1/8 is 1/4 before division by two. These restrictions
are disclosed comparison choices. No physical scale or selected amplitude follows.

Since the initial metric is constant, R3=0 and every spatial Christoffel vanishes.
With tau=kappa+2s, direct full constraints give

    M_x=kappa'-(kappa'+2s')=0, M_y=M_z=0,
    H_constraint=tau^2-tr(K^2)=4s*kappa+2s^2-2d=0.        (3)

There is no missing momentum component, integrated-only cancellation or suppressed
higher-order axial field. K_xx includes both quadratic shape rates and the full
homogeneous completion. Omitting its d/(2s) term gives H_constraint=-2d, except
at zero rates; the actual mutant capture rejects it for this reason.

NR2 equations (2)--(5) specialize to exactly (1): initial shape coordinates f=w=0,
transverse velocity matrix H, zero periodic primitive Psi, constant mean s0+c
and Lambda=0. Thus NR1 Q=0 because both displacement vectors u_c,u_s vanish,
with no phase or separate-polarization condition on the velocity vectors.

For a radial family A=epsilon*a, B=epsilon*b and analytic c(epsilon)=O(epsilon^2),
the complete first variation is delta gamma=0, delta K_xx=0 and
delta K_AB=-[[a cos X,b cos(X+theta)],[b cos(X+theta),-a cos X]].
The normal metric derivative is therefore the exact G327 two-component initial
velocity. NR2 owns the single-parameter existence scope. An independent c tangent
is homogeneous and is NOT within that G327 tensor sector. The joint parameter
existence needed here is checked directly next, rather than attributed to a
stronger quantifier in NR2's statement.

## 2. Actual jointly analytic common local developments

Supply Ric(g)=0 as the conditional equation; no G312 filter implication is used.
In Gaussian coordinates g=-dT^2+gamma(T,x), the six spatial equations are equivalent
to the complete system

    gamma_T=-2K,
    K_T=Ric3(gamma)+tau K-2K gamma^-1 K.                 (4)

Introduce A_lij=partial_l gamma_ij and its equation
A_lij,T=-2 partial_l K_ij. Ric3 is then analytic in positive gamma, its inverse,
A and first spatial derivatives of A. The enlarged system is first order in T
and the spatial variables, with identity coefficient of the highest time
derivative. Its initial A=0 is the actual initial spatial derivative. The defect
A-partial gamma has zero time derivative and zero initial value, so the reduction
does not create an auxiliary-field solution unrelated to a metric.

Treat A_amplitude,B_amplitude,c,theta as additional mathematical variables whose
derivatives do not appear in the equations; distinguish A_amplitude from the
auxiliary tensor. The initial data and coefficients are jointly analytic on an
open neighborhood of any compact parameter box with s away from zero. The
noncharacteristic analytic Cauchy--Kovalevskaya theorem used and reviewed in NR2
therefore supplies an actual locally unique analytic solution jointly in time,
spatial coordinates and all four parameters. It is an imported mathematical
method with its hypotheses checked here, not a new physical premise or a proof
of smooth/Sobolev well-posedness.

Cover the entire supplied compact initial slice and a fixed compact closed
parameter box strictly inside the safe box (theta on its circle) by finitely many
such analytic neighborhoods. Shrink to a common positive time interval. Analytic
uniqueness identifies overlapping solutions, spatial deck translates and theta
periodicity. The coefficients of (4) retain all six metric components and all
spatial directions. Compactness and continuity preserve positive gamma and
Lorentzian signature on a smaller common slab. This common slab depends on the
chosen finite parameter box; no numeric lifetime, arbitrary-amplitude uniformity,
singular-endpoint or long-time claim is made.

For completeness, put E_ab^res=Ric_ab and assume (4), so E_ij^res=0.
The direct Gaussian identities give E_00^res=H_constraint and E_0i^res=-M_i
initially. Contracted Bianchi for F_ab=E_ab^res-(tr_g E^res)g_ab/2 gives, writing
C=E_00^res and D_i=E_0i^res,

    C_T=2 div_gamma(D^sharp)+2 tau C,
    D_i,T=(1/2)partial_i C+tau D_i.                     (5)

This homogeneous analytic noncharacteristic system has zero initial data by
(3), so analytic uniqueness forces C=D=0 throughout the slab. All ten original
Ricci equations hold. This is the full NR2 CK/auxiliary/Bianchi method with joint
parameter hypotheses checked; exact initial constraints or finite formal jets
alone would not establish this conclusion.

At A=B=c=0, (4) has the complete Taub data, hence its analytic solution is the
unit-normalized Taub background by uniqueness. Differentiating (4) along a radial
G327 direction above and using linearized analytic uniqueness identifies the
whole spacetime tangent with the matching G327 first variation. No new exact
realizability theorem is claimed beyond this explicit family.

## 3. Raw curvature result and the invariant being compared

Fix volume epsilon_0123=+1 and
R^a_bcd=partial_c Gamma^a_db-partial_d Gamma^a_cb
+Gamma^a_ce Gamma^e_db-Gamma^a_de Gamma^e_cb. The first-pair dual is
(*C)_ab cd=(1/2)epsilon_ab^ef C_efcd. Define the geometric pseudoscalar

    J=(1/16) C_abcd (*C)^abcd.                          (6)

For the initial Gaussian normal n=partial_T let
E_ij=C_i0j0 and Bmag_ij=(*C)_i0j0. These are curvature tensors, not observer
vorticity or an imported physical electromagnetic field. At gamma=I the result is

    E=diag(2s*kappa, -kappa*(s I+H)),
    Bmag=[[0,0,0],[0,r',-p'],[0,-p',-r']],
    J=tr(E Bmag)=-2kappa*(p*r'-r*p').                    (7)

raw_geometry.py reconstructs all 4D connection/Riemann components using
gamma=I, gamma_T=-2K, gamma_TT=-2tau K+4K^2 and mixed metric derivatives
gamma_TX=-2K_X. It then forms all Ricci components and the FIRST-pair dual,
without importing source/candidate check code or a preset curl formula. Before
substituting the Hamiltonian completion it finds Ric00=4s*kappa+2s^2-2d;
all other Ricci entries are zero. After completion, Riemann equals Weyl. The
direct contraction gives C_abcd(*C)^abcd=-32kappa*(p*r'-r*p'), fixing (6)--(7)
including the Lorentzian orientation sign. Independent sign conventions may flip
the magnetic tensor and its reported J sign; nonvanishing and J^2 are unaffected.

The same result has a short geometric derivation: Gauss/Ricci give
E=tau K-K^2 on this flat vacuum slice, and Codazzi plus the stated dual convention
give Bmag_ij=epsilon_i^kl partial_k K_lj. Since H^2=d I and 2s*kappa=d-s^2,
the transverse electric block is -kappa(s I+H), the magnetic block is the one
shown, and their contraction is (7). This derivation is the same context's
argument, not a separate-context review. The raw constructor checks signs and
all components by a different implementation route from this reduced formula.

Equation (6) is an oriented spacetime scalar independent of a coordinate chart or
observer. Changing orientation reverses its sign; J^2 is orientation independent.
The equality to tr(E Bmag) is evaluated with the supplied normal, not used to
postulate an observer-independent decomposition. Coordinate changes cannot turn
J^2>0 into zero. No physical observer, handedness or comparison marking is selected.

For the phased data,

    p*r'-r*p'=-A B sin(theta),
    J=2kappa A B sin(theta)
     =A B sin(theta)*(d/s-s).                          (8)

Thus within the safe box J is nonzero on the ENTIRE initial slice exactly when
A B sin(theta)!=0; its sign is sign(A B sin(theta)) in the stated convention.
Quadrature theta=-pi/2 gives r=B sin X and

    J=A B*(s^2-A^2 cos^2 X-B^2 sin^2 X)/s.              (9)

For each fixed member with A B sin(theta)!=0, compactness gives a positive lower
bound on |J| on the initial slice. Continuity of the actual analytic development
therefore preserves nonzero J on a datum-dependent smaller common neighborhood
of that whole slice. This is a local retention argument, not an evolved finite-time
trajectory, a computed persistence time or a statement uniform as A B sin(theta)
approaches zero.

Moreover, (7) is REQUIRED on the initial slice of every sufficiently regular
Ric=0 development of these same COMPLETE data: Gauss, Codazzi and Ricci determine
that curvature there. The CK argument proves that at least one actual analytic
development exists. No arbitrary-completion or physical-data necessity follows.

## 4. Constant-basis and one-component controls throughout the local slab

At X=0 and X=pi/2, direct commutation gives

    [H(0),H(pi/2)]
       =[[0,-2AB sin(theta)],[2AB sin(theta),0]].        (10)

If a fixed transverse basis diagonalized the complete data for every X, the
mixed K matrices would be simultaneously similar to diagonal matrices and would
commute. Equation (10) forbids this when AB sin(theta)!=0. This argument excludes
even arbitrary constant GL(2,R) similarities, hence the smaller set of legal
constant basis/lattice changes. It is not a claim classifying all spacetime
coordinate changes or every possible different transverse action.

When A=0, B=0, or sin(theta)=0, H(X)=f(X)H0 for a constant real symmetric
trace-free matrix H0. A constant orthogonal basis diagonalizes H0 on the local
transverse universal cover. Both gamma and K then have diagonal transverse
blocks and are independent of both transverse coordinates. Reflection of one
of these transverse coordinates preserves the complete initial data and reverses
spacetime orientation. Equation (4), its analytic uniqueness and translation
invariance extend this reflection to an isometry of the local lifted development.
The pseudoscalar is independent of transverse position. The reflection therefore
requires J=-J at each fixed (T,X), so J=0 throughout that control's local slab.
Equivalently one may reflect about a given transverse point in a local chart.

A rotated reflection need NOT descend to an automorphism of an arbitrarily
periodized transverse torus. None is asserted: the argument is local on the cover,
which is sufficient for the local scalar to vanish on the quotient. The identity
of local curvature does descend. At B=c=0 the complete data coincide exactly with
NE1; its longer areal-time development and distinct normal remain its own scope.
Other one-component/phase-aligned controls are locally polarized in the above
sense, without a claimed global rotated-lattice equivalence to NE1.

Consequently the joint nonzero-parity local neighborhood is not locally isometric
to any of these zero-parity control neighborhoods: J^2 is positive in the former
and identically zero in the latter. This limited non-isometry follows from the
scalar itself, including for orientation-reversing coordinate maps; it is not a
complete invariant classification of arbitrary metrics.

The Gaussian congruence has covector n_flat=-dT. Frobenius gives zero vorticity
identically, including in the joint family. Nonzero J describes curvature parity,
not rotating Gaussian observers. No shift, physical rotation or coupling is inserted.

## 5. Completion freedom, leading amplitude order and exact cancellation limits

Equation (8) displays the complete homogeneous freedom. Holding A,B,theta,X fixed,

    partial_c J= -A B sin(theta)*(1+d/s^2).             (11)

For a nonzero joint phase this is nonzero: finite curvature parity is not fixed
by the transverse first-order tangent alone. This statement explores the one
declared homogeneous family, not all possible completions.

For analytic c(A,B)=O((|A|+|B|)^2), set rho=|A|+|B|. Uniformly in X, with fixed
theta and on a sufficiently small compact amplitude neighborhood,

    J=(2/3) A B sin(theta)+O(rho^4).                    (12)

Indeed s=-2/3+O(rho^2), d=O(rho^2), 1/s is bounded and analytic, and the exact
formula is AB sin(theta)*(-s+d/s). Those facts supply the remainder bound; it
is not a fitted or numerically extrapolated expansion. Thus the leading mixed
coefficient in this declared completion class is insensitive to those homogeneous
tails, while the exact value is not. For A=epsilon*a, B=epsilon*b and analytic
c(epsilon)=O(epsilon^2), this becomes

    J=(2/3)epsilon^2 a b sin(theta)+O(epsilon^4).         (13)

The raw script checks the epsilon^2 coefficient with a general c2*epsilon^2
representative; the all-analytic-tail assertion follows from (8), not that finite
test. Quadrature has leading -(2/3)epsilon^2 a b. The expansion statements here
are initial-slice statements. Analytic spacetime dependence gives legitimate
Taylor expansions on smaller compact slabs, but no uncomputed later-time
coefficient is asserted.

Outside the safe box, J can cancel for nonzero joint data: take theta=-pi/2,
A=B=s!=0, so d=s^2, kappa=0 and E=0 while Bmag need not vanish. Every exact
constraint still holds and the same analytic method gives a local development
near each such fixed finite datum. This exact initial-scalar cancellation is a
limit control of the formula, not an extension of the safe-box result or a
claim that J stays zero during that development. Such data are outside the
frozen near-Taub safe box. They do not refute the asymptotic near-zero statement
for any fixed analytic O(epsilon^2) homogeneous tail.
For unequal |A| and |B| in quadrature, d is not constant; choosing constant s
cannot make J vanish on the whole initial slice, although it may vanish at some
points outside the safe box. All other completions and metrics remain unclassified.

## 6. Meaning, evidence and omissions

Added reach relative to the inspected NR1/NR2/NE1 arguments is this explicit
mixed curvature diagnostic, its local non-isometry/control proof and completion
dependence. Existence of compatible two-component local developments is already
owned by NR2. No literature-wide novelty claim is made. In particular the leading
mixed parity can arise by contracting first-order curvature pieces; a first-order
scalar truncation discards it. It should not be described as a newly discovered
nonlinear interaction mechanism. The exact nonlinear data and existence argument
make the invariant an actual metric property rather than a coordinate artifact
or an unintegrated formal perturbation.

PERMITTED: the analytic witness family with two independent out-of-phase shape
rates and nonzero local curvature parity. REQUIRED: (3)--(9) for those fixed full
data in the supplied Ric=0 branch, plus zero Gaussian twist. OPEN: arbitrary
completions, any physical occupation or field law, sustained evolution/transfer,
stability, other mode sectors, Lambda!=0, selected scales/observers/histories and
native pair population. Parent separately owns the lawful retained-record join;
this result does not establish it merely from a scalar curvature calculation.

Actual raw_geometry_initial capture: exit 0, 2.273228881 seconds, 51,192 KiB max
RSS, Python 3.10.12, SymPy 1.13.1, 2 GiB/180-second limits and one library thread.
Its 18 named predicate groups include structural/symmetric zeros and a trivial
orientation-square algebra check; they are not 18 independent proofs. The raw
full metric/Ricci/Hodge calculation, analytic constraint/development argument and
non-isometry proof supply the substantive support. No floating tolerance is used.

Actual mutants: omit_axial_completion exits 1 at all_original_initial_constraints
with residual -2(p^2+r^2); freeze_second_time exits 1 at the raw full spatial Ricci
equations with the saved nonzero residuals. These are matched scientific failures,
not dependency errors/timeouts. Initial failed metadata input capture is separate:
Git could not create threaded lstat under the 256 MiB metadata limit; a command-only
serial-index retry passed. The old script and all streams remain preserved.

Not repeated: upstream full-package scientific programs, general CK theorem proof,
NR1 arbitrary-correction necessity proof from scratch, source reviews' entire
historical correction chains or any full registry audit. No new GPU/PDE solve,
external correspondence, protected-payload access or accepted-source edit occurred.
The construction was source/candidate-hypothesis exposed and is not the planned
fresh adversarial review. Different-model, different-library, human-specialist and
formal-proof independence remain unestablished. A separate review of the argument,
constraint interface, orientation convention, completion and records is still due.
