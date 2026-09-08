# HB2 initial candidate — curvature-line drift from admitted initial data

Explored then frozen for fresh review; UNREVIEWED, UNPROMOTED. Not a claim
of a new general differential-geometric theorem or of physical carried content.
QUESTION.md and the entire reviewed HB1/source scopes control. No new law.

## 1. Domain and claim

Supply any G331 unscaled weighted-contact metric gamma_w on compact S3,
w1,w2>0. Put eta=gamma(xi,.), xi=w1*d_phi1+w2*d_phi2, and

    R=scalar(gamma), lambda_h=(R-2)/2, Delta=2-lambda_h=(6-R)/2,
    P=xi tensor eta, Pi=I-P, A(X)=D_X xi.

Here A is a spatial covariant derivative of an ALREADY metric-defined unit
Killing field, not an extra connection or physical carrier. The accepted metric
satisfies Ric^sharp=lambda_h*I+Delta*P and Ric^sharp xi=2xi. Require Delta
nowhere zero for the global line statement; local statements need a nonzero
gap on their supporting domain. The xi sign is immaterial for P.

Choose fixed finite Lambda, a free constant C and either sign so that

    D0:=b+C=+/-sqrt[2*(R+2*C^2-2*Lambda)]

is strictly nonzero everywhere, and take EXACT G332 data

    K=((C-b)/2)*gamma+b*eta tensor eta.

The symbol D0 here is a scalar root, not the connection D. G332 proves both
original vacuum constraints. Conditional on the imported standard smooth local
marked Einstein-Cauchy theorem, these smooth compact data have an actual local
development in the admitted owner-provisional G310/G312 arena. Choose its
Gaussian normal presentation, lapse1/shift0, with negative-K convention
gamma_dot=-2K. Pull tensors back by this normal flow to compare the slices.
This is specified query/foliation data, not an additional physical evolution law.

Let P(t) be the continued simple spatial Ricci projector. Smooth development
and the uniform gap give it for some datum-dependent interval, as in G331.
The candidate's exact initial variation is

    Y := (5/(2*Delta))*A(grad b)
       = (5/(2*Delta*D0))*A(grad R),
    P_dot = Y tensor eta + xi tensor Y_flat.                       (1)

All derivatives/contractions in (1) use the supplied initial gamma. In
particular, first-order FIXED-LINE preservation is equivalent to dR=0 at
that event, within this precise strict/simple-gap class. For unequal weights
the drift is nonzero on0<x<1 and zero at the two axis circles. For equal weights
it vanishes everywhere (excluding the round gap-zero case w1=w2=1). The
global zero-first-drift condition within this family is exactly w1=w2.
Zero first drift alone is not an all-time preservation theorem.

## 2. Identities of the initial metric, not new premises

Unit Killing implies A is skew-adjoint, A(xi)=0, div(xi)=0 and D_xi xi=0.
The scalar b depends on R,C,Lambda; xi(b)=0 because isometries preserve R.
Consequently grad b is horizontal and

    Hess(b)(X,xi)=-db(A X).                                      (2)

Two more identities follow from the same metric. The Killing/commutator
identity gives div A, in components D_k A_i^k=Ric_i j xi^j=2eta_i.
The constant-norm Killing identity gives |D xi|^2=Ric(xi,xi)=2.
A is a skew operator on the two-dimensional horizontal plane, so its rotation
magnitude has square1; hence

    A^2=-Pi,       |A Z|^2=|Z|^2 for horizontal Z.                (3)

These identities can equivalently be checked from G331's Sasaki metric. No
new target orientation or extra almost-complex structure is selected. The
uniform simple-gap condition and positive radicand, not a finite box, own the
regularity domain. Both can fail at an excluded boundary.

## 3. Covariant Ricci variation with all spatial terms retained

G337 supplies the uncommuted Ricci variation. For h=gamma_dot=-2K,

    Ric_dot_ij = -D^k D_i K_kj -D^k D_j K_ki
                 +D^k D_k K_ij +D_i D_j tr(K).                  (4)

It follows directly from the connection variation and is not restricted to
G337's later double-silent contraction. The connection formula for an arbitrary
symmetric h is

    C^k_ij=(1/2)gamma^kl(D_i h_jl+D_j h_il-D_l h_ij),
    Ric_dot_ij=D_k C^k_ij-D_j C^k_ik.                           (5)

We evaluate the mixed part using h=(b-C)gamma-2b eta^2. For h=f gamma in
three dimensions, (5) yields Ric_dot=-(1/2)Hess f-(1/2)(Delta_g f)gamma.
The constant C contributes no covariant Ricci change. Its mixed contribution
at a horizontal X and xi is therefore +(1/2)db(A X), by (2).

For the remaining rank-one variation h=q eta^2, with xi(q)=0, (5) gives

    C^k_ij=(1/2)[(q_i eta_j+q_j eta_i)xi^k-q^k eta_i eta_j]
             +q[eta_j A_i^k+eta_i A_j^k],
    C^k_ik=(1/2)q_i.

At (X,xi), differentiating the first term in brackets contributes
(1/2)Hess(q)(xi,X). The negative q^k term contributes +(1/2)dq(A X).
The A terms contribute dq(A X)+q(div A)(X). The last divergence is zero
for horizontal X by div A=2eta. Finally -D_j C^k_ik cancels the Hessian term.
Thus the complete mixed variation is

    Ric_dot[q eta^2](X,xi)=(3/2)dq(A X).

Set q=-2b and add the conformal part to obtain

    Ric_dot(X,xi)=-(5/2)db(A X),
    Pi gamma^-1 Ric_dot(xi,.)=(5/2)A(grad b).                   (6)

Connection terms and spatial b derivatives were essential. In particular,
momentum conservation has NOT been used to commute derivatives or remove them.
This argument covers the entire declared family, not just coordinate samples.

## 4. Raising indices and differentiating the actual eigenprojector

Write B=gamma^-1 Ric. Since gamma_dot=-2K,

    B_dot=gamma^-1 Ric_dot+2 K^sharp B.                         (7)

The second term must not be dropped. In this initial family K^sharp preserves
P and Pi, so its contribution to Pi B_dot xi vanishes, but its full/vertical
contribution generally does not. Equations (6)--(7) give

    Pi B_dot xi=(5/2)A(grad b).                                (8)

Choose a smooth initial-sign-compatible unit eigenvector V(t) of P(t), with
V(0)=xi, on a local chart. Differentiating B V=lambda_v V and projecting to Pi
gives Delta*Pi V_dot=Pi B_dot xi. This proves the transverse part Y in (1).
The evolving unit norm fixes the parallel part:

    V_dot=Y+((C+b)/2)xi,
    (V_flat)_dot=Y_flat-((C+b)/2)eta.

Their parallel contributions cancel in P(t)=V(t) tensor V(t)_flat, yielding
the full tensor formula (1). It is independent of the sign choice V->-V.
No physical line orientation is selected. This also verifies that the result
is about a projector, not merely changing components in an arbitrary frame.

Normal-flow pullback is a declared comparison of slices. At the initial slice,
K^sharp commutes with P, so replacing that comparison by Levi-Civita transport
along the same unit normals does not change the initial transverse/projector
derivative (their difference is the corresponding shape-operator commutator).
This does not assert foliation independence or a physical flow of matter.

## 5. Exact family discrimination and domain boundaries

The accepted coordinate metric gives, with F=w1*x+w2*(1-x),

    R(x)=16*w1-8*w2-2-24*w1*(w1-w2)*x/F,
    R'(x)=-24*w1*w2*(w1-w2)/F^2,
    |grad R|^2=4*x*(1-x)*F*[R'(x)]^2.                          (9)

The chart singularities at x=0,1 do not make R or P singular: these are smooth
global tensors on S3, and dx vanishes at those two axis circles. For unequal
positive weights, (9) has nonzero gradient at EVERY interior torus and zero
gradient on the axes. Together with (3), strict D0 and nonzero Delta this proves
the first-drift alternatives in Section1. More quantitatively,

    |Y|^2=25*|grad R|^2/[4*Delta^2*D0^2],
    |P_dot|_HS^2=2|Y|^2.                                     (10)

The endpoints are R(0)=16w1-8w2-2 and R(1)=-8w1+16w2-2. For this monotone
family, a global simple gap means their Delta values have the same strict
sign; a strict global radicand is decided by the minimum endpoint R. These
criteria are convenient exact domain checks, not added physical restrictions.
If the gap closes, no particular continued simple projector is selected by
this proof. If D0 reaches zero, the smooth G332 root method can fail. Such
boundary cases do not refute the admitted field equation.

Nonzero P_dot at an interior point means P(t) differs from its normally carried
initial line for all sufficiently small nonzero t at that point, by smooth
Taylor expansion with nonzero first derivative. It does NOT establish that
all leaves become nonclosed, that an irrational orbit type persists, that a
different foliation is absent, or that a topological class changes. The smooth
gap-open line still exists. Zero axis drift likewise proves no axis persistence.

## 6. Supplied choices, checks and honest ceiling

The scalar Lambda, compatible C/root, positive weights and marked initial
slice are ordinary supplied data in the examined class. Formula (1) constrains
their resulting line behavior without selecting those inputs. No new carrier,
action, coupling, boundary, conventional physical mechanism or observation law
was used. This is an additional consequence of the admitted metric development,
not adoption of the weighted-contact family as physical content.

Author discovery: covariant calculation suggested coefficient5/2, then the
inspected shared G337 time-dual Ricci engine tested12 exact local fixtures.
All mixed residuals vanished; vertical index-raising terms were nonzero.
One exploratory weight pair (2,3/2) is gap-open only in the interior and closes
at an axis; it is NOT evidence for the global simple-gap statement. Keep it
as a boundary control. Frozen positive checks use separately declared global
gap/radicand checks. This pre-freeze exploration is disclosed, not a hidden
data restriction, physical fit or theorem repair.

Finite checks corroborate original tensors, signs, derivative factors and
actual hostile residual rejection; they cannot prove the universal argument.
Fresh separate-context review must assess (1)--(10), actual smooth-domain
hypotheses and the first-order inference before downstream use. The old
carrier's energy/stability question remains distinct. No finite-time numerical
solution, arbitrary-data stability, particle, localization, size, absolute
scale, matter identification, global completion, new premise, grade or canon.
