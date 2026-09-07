# PC1 source-first independent reconstruction

Stage A completed before reading any PC1 author candidate, code, results or
verdict. Reviewer `/root/persistence_pc1_review`, 2026-09-07 UTC. Exact runtime
model UNKNOWN; different-model/human specialist axes UNTESTED. Findings must
not be disclosed to the author until its candidate is frozen.

The broad spatially parallel null seed does NOT itself force Lambda=0 or
full ambient curvature annihilation. A nonempty Ricci-flat subclass does
provide the desired initial full-root interface. These conclusions concern
the CHOSEN recipe and owner-provisional Einstein arena; no promotion follows.

## 1. Full tangential initial equations

Let n be future unit normal, K(X,Z)=-g(nabla_X n,Z), gamma positive, and
ell=f n+Y, with f>0 and gamma(Y,Y)=f^2. The Gauss decomposition, with this
particular K sign, is

    nabla_X n=-K#X,
    nabla_X Y=D_X Y-K(X,Y)n.

Therefore nabla_X ell=0 for every tangent X is exactly

    X(f)=K(X,Y),       D_X Y=f K#X.                       (A1)

This is a sufficient-class restriction on supplied full initial data. It
does not add an independently evolving physical field or select f,Y. Since
the relation holds on the whole smooth initial patch, commuting tangential
covariant derivatives gives R(X,Z)ell=0 for tangent X,Z. A condition imposed
only at a single event would not justify this differentiated conclusion.

## 2. Algebraic conclusion, including the scalar branch

Use G358's explicit Q_abcd=g(R(e_a,e_b)e_c,e_d), signature (-+++), and
adapt a frame at one point so e0=n, e3=Y/f, L=ell/f=e0+e3. Distinguish
the mixed-curvature matrix M below from the old quadratic tensor B.

G358's algebraic Einstein converse yields

    Q_i00j=E_ij,
    Q_i0jk=epsilon_jkl M_li,
    Q_ijkl=epsilon_ijm epsilon_kln E_mn,
    E=E^T, M=M^T, tr M=0, Lambda=-tr E.                 (A2)

The last spatial formula is its C/K formula after substituting
C=E-(tr E)I/3 and K=-(tr E)/3. It retains the scalar curvature.

Impose Q_ij0d+Q_ij3d=0 for all tangent i,j and all d. The d=3 relations
give M_3i=0; the (i,j)=(1,2) equations give E_13=E_23=0. The remaining
(3,1)/(3,2) equations give M_12=-E_11=E_22,
M_11=E_12=-M_22. Thus the complete algebraic survivor is

    E = [[p,r,0],[r,-p,0],[0,0,-Lambda]],
    M = [[r,-p,0],[-p,-r,0],[0,0,0]].                    (A3)

All three real parameters p,r,Lambda remain. Direct substitution proves
the converse for algebraic tensors, with no PDE realization claim. In
particular R(n,e3)L=Lambda L. Full R(A,B)ell=0 holds on this class exactly
when Lambda=0. Tangential annihilation alone does not justify it.

This is also an actual-data obstruction, not merely a formal tensor.
G313 section3 already admits the Einstein product

    g=Lambda^-1[-dt^2+cosh(t)^2 dz^2+dOmega_2^2],
    Lambda>0.

At t=0 its complete spacelike data are

    gamma=Lambda^-1[dz^2+dOmega_2^2], K=0,
    n=sqrt(Lambda)partial_t,
    f=1, Y=sqrt(Lambda)partial_z.

Y is gamma-parallel and unit, so (A1) holds on the slice. The original
Hamiltonian constraint is R3=2Lambda, and momentum is zero. The actual
Einstein product has the nonzero R(n,Y)(n+Y)=Lambda(n+Y) above. The source
uses periodic z, but the counterexample already works on a local patch;
no new compact embedding result is needed. This refutes any universal
spatial-seed => Lambda0/full-annihilation assertion in the admitted arena.

## 3. The full old quadratic tensor and derivative boundary

On the Lambda=0 subclass, (A3) has the two transverse curvature components
p,r. The curvature and its first dual have the same two-screen component
support as G355; equivalently expand (A2)-(A3) in the unchanged recipe.
The complete four-index identity is

    B=4(p^2+r^2) L-flat tensor4.                         (A4)

This coefficient is tied to L=n+e3, not an arbitrary free rescaling of ell.
With ell=fL the coefficient of ell-flat tensor4 is
4(p^2+r^2)/f^4. On its positive branch the time orientation picks

    beta=[4(p^2+r^2)]^(1/4)L-flat = c ell-flat, c>0.

The real fourth-root uniqueness proof uses mixed components and retains the
full covector; evaluating one timelike contraction is insufficient. At
p=r=0 the full Ricci-flat curvature and B vanish; the only real root is zero.
No nonzero root or smooth continuation through such zeros is supplied.

The nonzero-Lambda spatial seed cannot be assumed to have a root. Already
the actual product example p=r=0 has, for the same Weyl/first-dual recipe,
B0000=B1111=2Lambda^2/3 and B0011=4Lambda^2/9. A fourth power eta tensor4
would require B0000*B1111=B0011^2, whereas their difference is
20Lambda^4/81. Thus no real covector fourth root exists there, null or
otherwise. This is a concrete recipe-domain failure, not a claim that a
new prescription has been selected for that branch.

Along the nonzero-root Ricci-flat initial patch, (A1) and beta=c ell-flat
give tangential recurrence nabla_X beta=X(log c) beta. This is NOT full
recurrence. A beta known only along Sigma has no defined normal derivative;
one must first establish a smooth ambient recipe domain and then control
nabla_n beta. Complete Einstein initial data determine a local metric only
at the inherited development scope, but a normal-derivative/type-propagation
argument must still be supplied. No alpha for all ambient directions,
q_rec, D, phase closure or phase-independent product persistence follows
solely from (A1)-(A4). A failed proof of propagation would leave it open,
not refute every possible Ricci-flat propagation theorem.

## 4. A complete spacelike interface in an actual harmonic development

Take the already admitted smooth harmonic metric with partial_v future,

    g=-2du dv+dx^2+dy^2+H(u,x,y)du^2, Delta_xy H=0.

For a supplied constant a, use the spacelike graph v=-a u, on an open
patch where F=H+2a>0. Its tangent basis is Z=partial_u-a partial_v,
partial_x,partial_y. With graph coordinates (u,x,y), its FULL data are

    gamma=diag(F,1,1),
    n=F^-1/2[partial_u+(H+a)partial_v],
    K_uu=H_u/(2sqrt(F)), K_ui=H_i/(2sqrt(F)), K_ij=0,
    f=F^-1/2, Y=-F^-1 Z, ell=partial_v.                (A5)

Here i,j=x,y. The normal is future because g(n,partial_v)<0, and has
norm -1. One direct K sign check uses n-flat=-d(v+a u)/sqrt(F):
K equals the tangential Hessian of v+a u divided by sqrt(F), and
Gamma^v_uu=-H_u/2, Gamma^v_ui=-H_i/2 give (A5).

Intrinsic differentiation gives

    R3=-Delta_xy H/F+(H_x^2+H_y^2)/(2F^2),
    (tr K)^2-|K|^2=-(H_x^2+H_y^2)/(2F^2),
    M_u=Delta_xy H/(2sqrt(F)), M_x=M_y=0.             (A6)

Consequently the ORIGINAL Hamiltonian and momentum constraints are zero,
as required for this Lambda0 metric. Also gamma(Y,Y)=f^2 and direct
differentiation verifies both equations (A1). This is not data on a null
u cut: u is one of the three spacelike coordinates and every gamma/K
component is supplied. No theorem identifying this open graph with the
registered compact G321/G335 families is used or claimed.

For a concrete nonempty nonzero-root/positive-q patch, choose a=1 and
H=x^3-3xy^2 near (u,x,y)=(0,1,0). At that point F=3 and
N=Hxx^2+Hxy^2=36(x^2+y^2)>0. Continuity permits an open regular spacelike
patch with F,N>0. G355 gives b=sqrt(6)(x^2+y^2)^(1/4),
q_rec=1/[4(x^2+y^2)]>0 there; the old root is nonclosed. These particular
ambient quantities are available from the actual admitted harmonic metric,
not inferred for all data satisfying (A1). This supplies a full local
initial-data interface without compact/global/physical occupancy claims.

## 5. Independent checks, exposure, and limits

source_first_check.py builds a generic symmetric6x6 bivector curvature
matrix, imposes Bianchi, all Einstein contractions and all spatial-seed
integrability equations, and solves the exact22-variable homogeneous
linear system. Rank19 leaves exactly3 parameters, with E as (A3) and
full-annihilation defects +/-Lambda. This is independent of the author's
unseen code. It computes the entire256-entry old Weyl/first-dual B and
verifies (A4) on Lambda0, and independently differentiates the induced
cubic gamma for R3, Hamiltonian, momentum, both seed equations and null norm.
The analytic classification and identities above bear the continuous
quantifiers. Finite computation is exact algebra/implementation support,
not PDE existence, propagation or physical confirmation.

The initial child reached JSON serialization after the scientific assertions
but exited1 because SymPy Zero lacked a JSON encoder. Original code and
streams remain in diagnostics/ and source_first.*. The only correction
was default=str in json.dumps; the full corrected run exited0 in
0.640886415 seconds, max RSS53888KiB, under512MiB/60s. Python3.10.12,
SymPy1.13.1. No author repair was used. Exact commands, timestamps and
streams are the capture JSON/stdout/stderr; source_first_corrected.stdout
records25 source/method/work-order hashes. No new PC1 author payload has
been read, and no findings have been sent before candidate freeze.

Omitted: full parent premise audit replay; historical production/review
suite reruns; compact embedding; general Einstein development construction;
normal-derivative or parallel-vector propagation proof; generic recurrence,
product persistence, global regularity/caustics, physical measurements,
different-model/human review, protected payloads and external research.
These are not marked passed. Stage A has no verdict on the unseen candidate.
