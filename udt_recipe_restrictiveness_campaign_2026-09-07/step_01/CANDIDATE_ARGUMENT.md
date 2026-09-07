# RC1 — a constrained tangent can pass the full algebraic root test yet leave the seed class

UNPROMOTED CONDITIONAL CANDIDATE; fresh direct review pending.
Sources pinned at5e022dff; G312/G313 arena and G355/G358/G361 recipe/data
definitions only. Lambda0 is the examined sector, not a selected UDT law.
The chosen recipe and physical-identification limits are unchanged.

## 1. Question and exact tangent

On a neighborhood of p=(u,v,x,y)=(0,0,1,0), put H0=x^3-3xy^2 and

    g_e=-2du dv+dx^2+dy^2+(H0-2e v y)du^2+2e x^2du dy.       (1)

e is a formal variation parameter. g0 is the admitted harmonic metric.
All g_e are smooth Lorentzian metrics (det=-1 with positive transverse
block), but (1) is NOT an exact vacuum family at e!=0:

    Ric(g_e)=4e^2x^2 du tensor2,  scalar R=0.                (2)

Thus delta Ric=0 exactly and the first variation is lawful LINEARIZED
vacuum data, not a finite-epsilon solution or nonlinear stability claim.
The coefficient -2 in(1) is equation-derived: replacing it by kappa gives
Ric_uy=-(kappa+2)e/2, while Ric_uu=(2-kappa)e^2x^2.
No coefficient was chosen to make the recipe pass.

All component identities use the ordinary Levi-Civita formula and
Q_abcd=g(R(partial_a,partial_b)partial_c,partial_d), as in G358/G361.
The exact tensor implementation and saved nonzero entries supplement the
displayed smooth rational identities, not a finite numerical sample.

## 2. COMPLETE spacelike data and original constraints

Use the fixed graph t=v+2u=0 with tangent columns X=(partial_u-2partial_v,
partial_x,partial_y). Set S=H0-2e v y+4-e^2x^4, dt=2du+dv. Then

    n=-g_e^-1(dt)/sqrt(S),  gamma=X^T g_e X,
    K_ij=-X_i^a X_j^b(2 Gamma^u_ab+Gamma^v_ab)/sqrt(S).       (3)

K has exactly the admitted minus-Weingarten sign. At p,e=0, S=5;
shrink to a fixed small neighborhood and small e to keep S>0. Define
L=H0+4 on Sigma. The full variations are

    gamma0=diag(L,1,1),
    delta gamma=[[4uy,0,x^2],[0,0,0],[x^2,0,0]],
    K0=(1/(2sqrt L))[[0,H0x,H0y],[H0x,0,0],[H0y,0,0]],
    delta K=[[ y(-2x^3-3xy^2+6)/sqrt L,
               -uy H0x/L^(3/2), 2u(x^3+4)/L^(3/2)],
             [-uy H0x/L^(3/2),0,x/sqrt L],
             [2u(x^3+4)/L^(3/2),x/sqrt L,0]].              (4)

No lapse/shift/normal contribution is dropped. For every actual smooth
metric the ORIGINAL Gauss/Codazzi constraints equal

    H=R3+(tr K)^2-|K|^2=2 G(n,n),
    M_i=D^j(K_ij-gamma_ij tr K)=-G(n,X_i).                 (5)

Here G=Ric because R=0, hence on Sigma
H=8e^2x^2/S, M=(-4e^2x^2/sqrt(S),0,0). Differentiating gives
delta H=delta M=0. This uses exact geometric identities and all components
of(2)-(3), not a different constraint equation or preconditioned residual.
The checker uses the right-hand projections; it is NOT claimed to be an
independent intrinsic recomputation of the left sides. Fresh review must
scrutinize this distinction and the sign/data formulas.

## 3. Full algebraic fourth-root test through first order

Write r2=x^2+y^2>0, N=36r2, b=N^(1/4)>0. At e=0 the FULL chosen Weyl/
FIRST-dual quadratic is B0=N du tensor4 and future root beta0=-b du.
Ric=O(e^2), so replacing Weyl by Q changes neither B0 nor delta B.
This replacement is used ONLY through first order, never at finite e.
Direct differentiation of the complete quadratic yields

    delta B_uuux=12y, delta B_uuuy=12x                     (6)

and all permutations of those entries; EVERY other entry is zero.
Consequently all256 first-order component equations are solved by

    beta_e=-b[du+e{y dx+x dy}/(3r2)]+O(e^2),              (7)
    delta B=delta(beta tensor4).

The full null condition holds through first order, and the future sign is
continuous from beta0. No O(e^2) completion of a root is asserted. The
transverse covector terms are indispensable; checking only B_uuuu misses
the change. This is a formal tangent to the full algebraic root domain,
not an existing exact recipe or a current on g_e at e!=0.

## 4. No smooth first-order spatially parallel seed near this seed

Seek ANY smooth ell_e=partial_v+e a+O(e^2) along Sigma, not merely a
rescaling of partial_v, with nabla_X ell_e=O(e^2) for ALL spatial X.
Spatial curvature integrability necessarily gives

    Q0(X_i,X_j,a,.)+delta Q(X_i,X_j,partial_v,.)=0.        (8)

Substituting the curvature of(1) on an open patch with x near1 yields,
equivalently for every component of(8),

    a^u=0, a^x=-y/(3r2), a^y=-x/(3r2), a^v arbitrary.    (9)

These are spatial, not just full ambient assumptions. The displayed
relations substituted back annihilate every spatial component; elimination
of their coefficients gives the converse. The 4D tensor checker records
the complete linear system and its symbolic solution without sampling.

The y-component of the remaining differential equation with X=partial_x
is partial_x a^y=0: Gamma0^y_xc=0 for every c and delta Gamma^y_xv=0.
But(9) forces

    partial_x a^y=(x^2-y^2)/(3r2^2), equal to1/3 at p.     (10)

Thus no such smooth first-order seed exists on a neighborhood of p.
Arbitrary a^v, seed scaling, or a different candidate transverse correction
cannot remove this obstruction. Baseline nonzero curvature forces every
parallel null seed to be a constant multiple of partial_v; normalize that
constant before the argument. This is not failure of ONE poorly rescaled
section. A pure infinitesimal coordinate variation would carry a parallel
seed and satisfy its linearized equations, so the demonstrated direction
is not pure diffeomorphism gauge. It leaves this sufficient seed class.

## 5. Evidence, alternative outcomes and ceiling

Exploration first derived the v-term by Ric_uy, discovered an O(e^2)
Ricci residual, and found that an allowed quadratic metric completion may
remove it. Exact realization is reserved for RC2 after this review. No
finite-epsilon vacuum claim is used in RC1. The algebraic root tangent
surviving while the seed tangent fails was not discarded or called a pass
for the full recipe. No new physical assumption was required.

Author check_tangent.py passes12 groups on full rational-function tensors.
Two ACTUAL mutations fail: omitting the v-term violates linearized Ricci;
omitting a transverse root variation violates full256 root matching.
These are same-author/shared-geometry regression, not separate-context proof.
No unexpected failure or post-freeze repair has occurred. Exact arithmetic
has no floating tolerance; one event in(10) refutes an open-neighborhood
equation, while the constraints and tensor identities hold as expressions.

Strongest claim: the declared constrained infinitesimal direction is not
gauge, lies in the full algebraic root tangent, but cannot lie in the
spatially parallel-seed tangent. This separates necessary pointwise checks
from differential initial-data compatibility. No codimension, genericity,
exact nearby admitted family, generic recipe necessity, stability, physical
identification, product theorem, scientific promotion or canon follows.
