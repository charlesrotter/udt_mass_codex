# PC1 candidate — initial recipe eligibility and complete spacelike data

UNPROMOTED CONDITIONAL CANDIDATE; fresh direct review pending.
PC1-SEED, PC1-CURVATURE, PC1-CAUCHY. No propagation result is used or claimed.
Source baseline94b1141119894f4ad75f3d338f0ec8d41df0bc42.
This is a declared sufficient route on ACTUAL smooth4D time-oriented Einstein
developments Ric=Lambda g in G312/G313's owner-provisional bounded arena.
It is not all lawful initial data, a selected scalar sector, a new physical
field, physical recipe adoption, or a compact G321/G335 embedding theorem.

## 1. Complete initial-data condition (PC1-SEED)

Let Sigma be a smooth spacelike local slice, n its future unit normal,
gamma its induced Riemannian metric, and K(X,Z)=-g(nabla_X n,Z).
Supply a smooth nonzero future-null section ell of TM restricted to Sigma.
Write ell=f n+Y, Y tangent, f>0, gamma(Y,Y)=f^2. The Gauss/Weingarten formulas give

    nabla_X ell = (X(f)-K(X,Y)) n + D_X Y-f K-sharp(X).

Thus spatial parallelism is EXACTLY the full data condition

    df(X)=K(X,Y),   D_XY=f K-sharp(X),   |Y|_gamma^2=f^2,   f>0.       (1)

The scalar and vector equations are both needed. Gamma and K must still obey
the original Hamiltonian/momentum constraints and come from the ACTUAL smooth
development under discussion. Pointwise arbitrary curvature is not a substitute.
Equation(1) restricts supplied initial data; it is not a new evolution law or
an asserted necessary condition on every possible recipe-compatible geometry.
Rescaling ell by a positive spatial CONSTANT preserves(1); a nonconstant
spatial rescaling generally does not. Ell's auxiliary scale will not select
the fixed recipe's root.

The pullback connection commutator applied to(1) implies R(X,Z)ell=0 for
every tangent X,Z. This uses an open patch, not parallelism at one point alone.

## 2. Algebraic curvature and the exact root gate (PC1-CURVATURE)

At each initial event choose e0=n, e3=Y/f, and oriented orthonormal e1,e2.
Then ell=f(e0+e3). Use precisely G358's convention

    Q_abcd=g(R(e_a,e_b)e_c,e_d), Ric_bc=sum_a eta_aa Q_abca,
    E_ij=Q_i00j, Q_i0jk=epsilon_jkl M_li,
    Q_ijkl=epsilon_ijm epsilon_kln E_mn, Lambda=-tr E,                (2)

where E is symmetric and M symmetric trace-free. M is G358's mixed curvature
matrix, NOT the four-index quadratic recipe B and not a separate field.

Spatial integrability is Q_ij0d+Q_ij3d=0, all spatial i,j and all d.
Substitution of(2) is equivalent to the eight independent linear conditions

    E22=-E11, E13=E23=M13=M23=0,
    M11=E12, M22=-E12, M12=-E11.

Consequently the full solution, with arbitrary real p,q,rho, is

    E=[[-p,-q,0],[-q,p,0],[0,0,rho]],
    M=[[-q,p,0],[p,q,0],[0,0,0]],     Lambda=-rho.                   (3)

This equivalence follows by substitution of the displayed eight conditions
into ALL spatial commutator components and reading those conditions back
from them; G358's full eleven-dimensional representation owns the ambient
algebraic quantifier. Exact rank8/elimination checks supplement this argument.
It is not an Einstein PDE-realization converse for arbitrary p,q,rho.

Importantly, spatial integrability alone does NOT algebraically erase rho.
The only possibly nonzero full contraction Q_ab0d+Q_ab3d has
(03,0)=rho, (03,3)=-rho and the skew partners. Hence FULL R(A,B)ell=0
is equivalent to rho=0 within this algebraic family.

For the CHOSEN old recipe use WEYL, not R, at nonzero Lambda:

    W_abcd=Q_abcd-(Lambda/3)(eta_bc eta_ad-eta_ac eta_bd),
    (*W)_aech=(1/2) epsilon_ae{}^{mn} W_mnch,
    B_abcd=eta^ef eta^hi
      (W_aech W_bfdi+(*W)_aech (*W)_bfdi).                           (4)

The possible overall sign translation from the older coordinate curvature
convention cancels in both quadratic terms; the antisymmetric pair slots
and FIRST-pair dual are unchanged. Inserting(3) into the full expression gives

    B0000=2rho^2/3+4(p^2+q^2), B1000=B2000=0,
    B1111=2rho^2/3.                                                (5)

If B=beta tensor4 for any nonzero REAL covector, B0000>0 implies beta0!=0.
Then B1000=0 forces beta1=0, while B1111=beta1^4 forces rho=0.
Thus nonzero rho fails the actual full-root domain; it cannot be rescued
by a different timelike extractor or by renaming a component as the root.

Conversely, when rho=0 the ENTIRE tensor is

    B=4(p^2+q^2) L-flat tensor4,   L=e0+e3.                        (6)

This follows by multiplying the transverse two-by-two trace-free block
[[p,q],[q,-p]], whose square is (p^2+q^2)I, in the two terms of(4);
the first dual contributes the same transverse norm. All256 component
identities in(6) are also checked exactly, including the coefficient.
If p=q=0, curvature and B vanish and the NONZERO-root recipe is undefined.
Otherwise the unique future-raised real fourth root is

    beta=b ell-flat, b=[4(p^2+q^2)]^(1/4)/f >0.                    (7)

The two real signs of a fourth root are separated by the supplied time
orientation. B and beta do not depend on the auxiliary positive seed scale.

Therefore, for this spatially parallel seed class, the initial nonzero
real-root domain exists precisely when Lambda=0 and p^2+q^2>0.
This is a restriction imposed jointly by the chosen recipe and this sufficient
class, NOT UDT-wide metric selection of Lambda or physical adoption.
The connected scalar is constant by the admitted equation; zero at one such
event fixes that connected Einstein sector, not the whole UDT arena.

On a smooth nonzero patch of Sigma, the FULL covector beta is specified by(7).
Tangential derivatives obey nabla_X beta=X(log b) beta. This does NOT yet
supply the normal derivative or full ambient recurrence alpha, q_rec or D:
a root defined only on Sigma is not yet a root on an ambient neighborhood.
No extension is manufactured by the extractor formula outside its type domain.

## 3. Nonempty lawful spacelike-data interface (PC1-CAUCHY)

Use the already reviewed G355 actual local harmonic metrics

    g=-2du dv+dx^2+dy^2+H(u,x,y)du^2, Hxx+Hyy=0,
    ell=partial_v future and parallel.

Take t=v+c u and a local graph Sigma={t=0}, with c a supplied chart/query
constant and L=H+2c>0 on the retained patch. Restrict around any finite event
as necessary. The graph is genuinely spacelike: g^-1(dt,dt)=-L<0.
Tangent frame is (X_u=partial_u-c partial_v,partial_x,partial_y), and

    gamma=L du^2+dx^2+dy^2,
    n=[partial_u+(H+c)partial_v]/sqrt L,
    K=(1/(2sqrt L)) [[Hu,Hx,Hy],[Hx,0,0],[Hy,0,0]],
    f=1/sqrt L, Y=-X_u/L.                                        (8)

These are induced data of an already ACTUAL smooth solution, not initial
values chosen independently of the constraints. Direct ambient differentiation
gives K with the admitted minus sign. It also gives (1), |Y|^2=f^2 and f n+Y=ell.

The ORIGINAL (unpreconditioned) Hamiltonian and momentum residuals of(8) are

    R3+(tr K)^2-|K|^2 = -(Hxx+Hyy)/L,
    D^j(K_ij-gamma_ij tr K) = ((Hxx+Hyy)/(2sqrt L),0,0).            (9)

Thus both vanish by harmonicity. Their full symbolic general-H expressions,
not only a flat example, are checked. No lapse/shift or normal derivative is
discarded to make a null cut look like spacelike Cauchy data.

For nonemptiness with nonzero recipe, H=x^3-3xy^2 at u=0,x=1,y=0,c=2
has L=5 and N=Hxx^2+Hxy^2=36; a small regular open patch has L,N>0.
This is a coordinate/complete-data interface witness, not a new chosen profile
law, physical populated history, compact embedding, or production solve.
It lies in the old positive-q family, but no general q propagation is inferred.

A full spacelike graph here contains an open set of ALL (u,x,y) ray labels.
An equality at a single u-null cut is much weaker than compatibility on such
a Sigma. The old cubic/quartic fixed-label failure at varying u is not,
without complete initially compatible data, a dynamical-departure example.

## 4. Discovery, checks and limits

The preliminary tentative idea that spatial integrability alone erased
Lambda was NOT retained. explore_algebra.py exposed a three-parameter rank8
space. Its exploratory R-quadratic output is not the Weyl recipe at nonzero
Lambda and is explicitly excluded from all recipe conclusions.
DIAGNOSTIC_PLAN.md froze the finite correction/check. The first diagnostic
hit a Python/SymPy bool-multiplication TypeError before a scientific assertion;
the initial code/stderr are retained, and int(bool) corrected only typing.
The corrected full Weyl calculation establishes(5)-(6); no premise changed.

The frozen author checker passes17 grouped exact checks, with no floating
tolerance. Actual drop-dual, wrong-K-sign and erase-scalar mutations all fail
their intended guards. The scripts reuse author assembly, so these are author
checks/regression, NOT independent review. Analytic formulas above carry the
general algebraic and smooth-data claims. Counts do not certify propagation,
physical truth or completeness outside the declared class.

Next useful question, only if this survives fresh review: on an ACTUAL
Ricci-flat development, does the spatially parallel seed extend as a parallel
null field and preserve the original nonzero-root/recurrence recipe locally?
That is not answered here. Generic recipe-compatible data without(1), global
phase/cauchy topology, quantitative durations, zero crossings, physical
content identity, detector laws, population, scale, manuscript and canon remain
outside the result. All G312/G351/G352 stamps and old recipe caveats survive.
