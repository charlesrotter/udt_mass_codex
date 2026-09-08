# CD2 initial candidate — analytic joint local development

2026-09-08. Explored then frozen for fresh separate-context review.
CONDITIONAL CANDIDATE, NOT BANKED, NOT_PHYSICAL_ADOPTION, NOT_CANON.
Prior question ../CD2_QUESTION.md; entire reviewed CD1 scope/caveats inherited.

## 1. Exact positive claim and method restriction

For EVERY CD1 seed choice with rho and Phi REAL ANALYTIC near x0, its reviewed
local constrained data admit an analytic local joint development satisfying

    Ric_ab=Lambda_* g_ab+beta n q_a q_b,
    q=dphi,   g^-1(q,q)=0,   div(n q-sharp)=0.                (1)

Here beta!=0 and Lambda_* are supplied real constants, n>0, q nonzero and
future-raised. Original phase, cross-phase labels and mu=s0|dy dz| have their
prescribed initial values; the fixed product propagates without retuning.
The claim is local near an interior initial event, after shrinking before
zeros/caustics. No common time interval over all seeds or global result.

The source relation is OPTIONAL and UNADOPTED, outside G312's bounded vacuum
theorem. G351/G352 owner-provisional interface and CHOSEN product do not derive
it or identify its mathematical density as physical matter. Analyticity is an
explicit restriction of this proof method/data, not a proposed physical law
or an established necessary condition. Smooth nonanalytic CD1 seeds remain
unresolved HERE.

Method: analytic first-order normal-form Cauchy--Kovalevskaya(CK), with actual
hypotheses below. METHOD_SOURCE_SCREEN.md identifies Leon Simon's Stanford
Lecture3 normal-form theorem/proof and the bounded null-dust literature screen.
Existing smooth results are not denied; their full hypotheses are not silently
imported for this data/product/sign/scalar class.

## 2. Full initial metric jet and gauge, not extra physics

Use coordinates(t,x^i), i=1,2,3, Sigma={t=0}. Starting with the CD1 analytic
gamma,K,phi_0=Phi(x),n_0=rho(x), set

    g_00=-1,  g_0i=0,  g_ij=gamma_ij,
    v_ij:=partial_t g_ij=-2K_ij,
    v_00=2 tr_gamma K,
    v_0i=gamma_ij gamma^kl (3)Gamma^j_kl.                   (2)

Choose a flat reference connection with zero coefficients in this chart and
define H^a=g^bc[Gamma(g)^a_bc-Gamma(ref)^a_bc], H_b=g_ba H^a. H is a vector
relative to the specified reference connection, not bare Christoffel symbols
claimed tensorial in arbitrary charts. Initial direct evaluation gives

    H^0=(v_00+gamma^ij v_ij)/2=0,
    H^i=-gamma^ij v_0j+gamma^kl (3)Gamma^i_kl=0.             (3)

Initial lapse1/shift0 and their rates fixed by(3) are gauge data, not a physical
observer/source/rate selector. The induced metric AND full second fundamental
form are exactly gamma,K with negative-K convention. Later coordinates need
not be Gaussian normal.

## 3. Exact-null phase and an invertible density variable

Let p_i be auxiliary spatial phase derivatives. On the open domain g^00<0 and

    b=g^0i p_i,        D=b^2-g^00 g^ij p_i p_j>0,
    Q(g,p)=(-b+sqrt(D))/g^00,
    q=(Q,p_i),        ell^a=g^ab q_b,    ell^0=sqrt(D)>0,
    V^i=ell^i/ell^0,   W=sqrt(-det g)>0,                    (4)

Q is the null root with future-raised q. On Sigma Q=-E, ell^0=E,
E=|Dphi_0|_gamma=Phi'>0. Inverse metric, roots and denominators are analytic
and regular near each initial event. Differentiating the null quadratic gives
Q_{p_i}=-V^i. No weaker pullback identity is used to fix normalization.

Evolve the coordinate flux density m, defined invertibly by

    m=W n ell^0,          n=m/(W ell^0).                    (5)

This variable change is NOT a physical mass or extra constitutive law.
Initial m_0=sqrt(det gamma) rho E=s0 E: it is neither n_0 nor s0.
Continuity becomes EXACTLY

    partial_t m+partial_i(m V^i)=0.                         (6)

For phase use

    partial_t phi=Q(g,p),
    partial_t p_i=partial_i Q
                =Q_g w_i+Q_{p_j} partial_i p_j,             (7)

where Q_g w_i contracts symmetric metric variables and w_i=partial_i g.
Initial p_i=partial_i phi_0. Equation(7) preserves p_i-partial_i phi=0.
Thus q=dphi throughout the neighborhood and(4) enforces nullness there.

## 4. The ACTUAL joint first-order analytic system

Define the reduced Ricci tensor in the fixed reference chart by

    Ric^H_ab=Ric_ab-nabla_(a H_b)
             =-(1/2)g^cd partial_c partial_d g_ab+P_ab(g,partial g). (8)

Parentheses include1/2. P is analytic rational in nondegenerate g and its
first derivatives. The second-derivative part of Ric is

    (1/2)g^cd[partial_c partial_a g_bd+partial_c partial_b g_ad
              -partial_c partial_d g_ab-partial_a partial_b g_cd],

and H_b=g^cd[partial_c g_bd-(1/2)partial_b g_cd]. Subtract its symmetrized
derivative to obtain the displayed wave principal part. All remaining terms
are first-derivative products; the differential order is actually checked.

Introduce v_ab,w_iab and solve the following NORMAL-FORM system:

    partial_t g_ab=v_ab,
    partial_t w_iab=partial_i v_ab,
    partial_t v_ab=(1/g^00){2[P_ab-Lambda_* g_ab-beta n q_a q_b]
                      -2g^0i partial_i v_ab-g^ij partial_i w_jab},
    partial_t phi=Q,
    partial_t p_i=Q_g w_i+Q_{p_j} partial_i p_j,
    partial_t m=-V^i partial_i m-m partial_i V^i.            (9)

Here partial_i V^i=V^i_g w_i+V^i_{p_j} partial_i p_j. P uses(g,v,w);
n,q,V are algebraic(4)--(5). Every right side is analytic in finitely many
unknowns and their FIRST spatial derivatives. No time derivative is hidden
on the right and no unsolved second phase derivative is treated as independent
data. There are55 scalar unknowns(10+10+30+1+3+1), bookkeeping NOT physical DOF.

Initial w_iab=partial_i g_ab. Its difference from partial_i g_ab has zero
time derivative by(9). The p constraint propagates by(7). Thus the metric
equation is really Ric^H=Lambda_*g+beta n q q, with exact phase/current equations.
All initial fields are analytic by reviewed CD1's analytic ODE subcase and
(2),(4),(5). Sigma is noncharacteristic: coefficient of partial_t U is identity
after division by verified nonzero g^00. CK supplies a unique local analytic
solution of this JOINT system, not a metric first followed by reconstructed
content. Restrict so g stays Lorentzian, g^00<0,D>0,m>0; then n>0 and ell
is nonzero future-null. CK supplies actual solutions, not only formal series.

## 5. Original metric equations and propagated gauge constraints

Write T_ab=beta n q_a q_b, j=n ell. On the evolved exact-null phase/current:

    ell^a nabla_a q_b=(1/2)nabla_b(q^2)=0,
    nabla^a T_ab=beta[(div j)q_b+n ell^a nabla_a q_b]=0.     (10)

These are not off-shell identities for arbitrary supplied q,n. Put
E_ab=G_ab+Lambda_*g_ab-T_ab. On the reduced solution, trace(T)=0 gives

    E_ab=nabla_(a H_b)-(1/2)g_ab nabla_c H^c,
    nabla^a E_ab=(1/2)[Box_g H_b+Ric_bc H^c]=0.              (11)

Bianchi supplies this homogeneous subsidiary equation only AFTER a joint
reduced solution exists and(10) holds; it is not an existence theorem.
On Sigma H=0, so its tangential covariant derivatives vanish. In the initial
unit-lapse/zero-shift frame, with a_b=nabla_N H_b,

    E_00=a_0/2,             E_0i=a_i/2.                    (12)

Reviewed CD1 scalar/momentum constraints set these projections to zero by
Gauss--Codazzi. Hence H and its normal derivative vanish initially.
Equation(11) is linear homogeneous wave with the now known analytic g and
noncharacteristic Sigma. CK uniqueness, or zero-data Taylor recursion, gives
H=0 locally. Thus ALL original metric equations(1) hold. No vacuum existence
or propagation theorem is exported from G315.

## 6. Propagation of the ORIGINAL product

Transport original labels by ell(Y)=ell(Z)=0, Y|Sigma=y,Z|Sigma=z.
Since ell^0>0, local flow/transport existence and uniqueness give them on a
smaller tube. Also ell(phi)=0. Initial(Phi,y,z) are independent, so
(r,phi,Y,Z) form a local adapted chart, with affine parameter r of ell;
exact nullness supplies affinity. No new labels, weight or phase normalization.

Let epsilon_g be the consistently oriented metric volume and eta=i_j epsilon_g.
Continuity gives d eta=0; i_ell eta=0. Cartan's identity implies L_ell eta=0.
The form

    eta_product=s0 dphi wedge dY wedge dZ                    (13)

also annihilates ell and is Lie-transported. CD1's FULL initial match is
eta|Sigma=s0 dPhi wedge dy wedge dz. Two horizontal transported forms with
the same initial pullback coincide on the entire local tube: pull back along
the flow, where both are constant and have no ray component.
Therefore eta=eta_product in the FULL neighborhood. In SM1 adapted coordinates
this is nJ=s0 with the ORIGINAL phase/label measure at all cuts.
Only now does every supplied observer's -g(U,j)=n[-U(phi)] equal G352's chosen
continuous readout. This supplies no detector, physical counting or source identity.

## 7. Uniqueness axes and the unproved smooth/stability claims

At gauge data(2), CK gives uniqueness among ANALYTIC reduced solutions,
hence among analytic full solutions in that wave gauge. There is also local
geometric uniqueness WITHIN THE ANALYTIC CATEGORY: on any analytic full
development with the same geometric/phase/density data, solve Box_g X^a=0
with X^0|Sigma=0,N X^0=1 and X^i|Sigma=x^i,N X^i=0. This linear analytic
wave problem is noncharacteristic, so CK gives analytic coordinates with
invertible initial Jacobian. In them lapse1/shift0 and H=0 determine exactly
the first jet(2). Initial fields in(9) coincide; analytic uniqueness then
identifies the developments, giving a local analytic diffeomorphism fixing
the identified initial data. Labels have unique transport. Nonanalytic
competitors, maximal developments or global gauge uniqueness are not covered.

Continuous dependence in a declared Sobolev norm, smooth-data existence,
nonlinear stability and uniform lifespans are NOT established. CK alone does
not supply them. The naive unrestricted first-order reduction is not
automatically strongly hyperbolic: freeze a Lorentz-frame principal symbol
at q=(-E,E,0,0),m=m0>0. For the curl-compatible transverse perturbation with
wave covector dy, the fixed-metric phase/current block reads

    partial_t delta p_y=0,
    partial_t delta m+(m0/E)partial_y delta p_y=0.             (14)

Its symbol [[0,0],[m0/E,0]] is nonzero nilpotent with one eigenvector.
The metric source in(9) is algebraic in(p,m), so no missing principal derivative
diagonalizes this invariant zero-metric-perturbation sector. Equal-derivative
smooth harmonic-wave estimates cannot simply be assumed for these variables.
This is a frozen-symbol/method diagnostic, not a flat nonvacuum solution or
nonexistence/instability theorem. Different reductions, derivative hierarchies
or the CD1 symmetry restriction may avoid it; these transverse perturbations
are outside the restricted CD1 family. No universal smooth impossibility follows.

## 8. Ceiling and verification boundary

The candidate milestone is DYNAMICAL COHERENCE at an analytic local conditional
scope for genuinely independently seeded data. It is not only Bianchi
compatibility, an isolated exact spacetime or metric factorization.
The response, constant coupling and single exact-null direction remain
optional model assumptions. Two analytic initial profiles, measure amplitude,
metric-rate datum and scalar/coupling values remain supplied with CD1
compatibilities; they need not be uniquely selected.

The general argument owns existence/propagation/uniqueness quantifiers.
Null-root, gauge-jet, principal-symbol and original-residual recomputations
and wrong-substitution checks are finite diagnostics, not a CK proof.
Fresh direct adversarial review is required before use. Retain analytic/local/
positive/regular, method-chart, chosen-product, optional-source and review limits.
Stop after this second reviewed step: no physical adoption, promotion,
observation or successor research is authorized.
