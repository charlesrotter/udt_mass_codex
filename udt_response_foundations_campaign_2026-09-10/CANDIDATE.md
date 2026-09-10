# RF1 — intrinsic normal-metric-jet response estimate

Initial frozen candidate, CONDITIONAL / UNREVIEWED / UNPROMOTED,2026-09-10.
One result with representation, estimate and ownership parts. No second step.
The work-order question preceded the argument; analytical exploration preceded
this freeze. The current G312 authority governs, not historical stronger W3.

## 1. Exact question and conditional domain

GL1 supplied an equivariant differentiable response on an ambient product of
curvature derivative tensors, including unrealizable arrays. RF1 asks whether
the estimate needs that response extension when working with genuine metric
jets. It does NOT assume or prove that UDT has a particular response formula.

Fix dimension4, signature(-+++), a Lorentz vector space(V,eta), a reporting
orthonormal frame and units, and one finite metric-jet order N>=2. Consider a
symmetric covariant rank-two metric response E of order at most N: at an event
its value depends only on j^N g, not on higher derivatives or an extra field,
orientation, chosen vector, position-dependent external coefficient or hidden
history label. It is natural under local diffeomorphisms, in the FULL
unoriented convention. Its normalized domain contains an open neighborhood
of the flat normal metric N-jet, consisting of all realizable normal jets
in that neighborhood. One fixed E/domain/units is used throughout.

These typing, fixed-order and full-neighborhood hypotheses are CONDITIONAL.
Explained Local Metric Sufficiency supports finite local dependence without
hidden history, but does not by itself supply this full architecture, a common
order bound on a neighborhood, response regularity, or an off-equation domain.
If E is known only on a restricted solution set, the full-neighborhood premise
cannot be silently inferred. Realizable as a metric is not admitted as a
particular field-law solution. G311 identifies DDR with TF(E)=0 only for its
specified symmetric-response domain, and does not identify E's formula.

Fix arbitrary positive finite-dimensional component norms, not an invariant
positive Lorentz norm. Uniformities below are in controlled frames, not under
unbounded boosts. No preferred physical frame, numerical scale, boundary,
source, carrier, action or empirical criterion is added. Mixed-weight response
coefficients would need appropriate dimensions; this result neither supplies
nor physically adopts them. N, units and comparison parameters are supplied.

## 2. A linear space of genuine normal metric jets

For each s=2,...,N let H_s be the vector space of homogeneous degree-s
polynomials h_s:V->Sym2(V*) satisfying

    h_s(x)(x,v)=0 for all x,v in V.                       (1)

Use homogeneous Taylor polynomials WITHOUT factorials. Put H=direct_sum H_s.
For any tuple h=(h2,...,hN), the polynomial tensor

    g_h(x)=eta+sum_(s=2)^N h_s(x)                         (2)

is a smooth Lorentz metric on a sufficiently small neighborhood of0: its value
at0 is eta and nondegeneracy/signature are open. No common global domain or
global completeness is claimed. It satisfies g_h(x)(x,v)=eta(x,v).

To verify that these coordinates really are geodesic normal, write
g_ij(x)x^j=eta_ij x^j and differentiate:

    (partial_k g_ij)x^j=eta_ik-g_ik.

Contract with another x. Both (partial_j g_ik)x^j x^k and
(partial_i g_jk)x^j x^k vanish. Consequently the first-kind Christoffel
symbols obey Gamma_i,jk x^j x^k=0. Invertibility gives Gamma^i_jk x^j x^k=0,
so coordinate rays t->tx are affinely parametrized geodesics. Their initial
velocities are x, hence the coordinates are the exponential normal coordinates
of g_h near0. This argument uses no positive-definite metric assumption.

Conversely, the pseudo-Riemannian Gauss identity in exponential coordinates
g(x)(x,v)=eta(x,v), together with zero first derivatives at0, implies (1) for
each homogeneous Taylor coefficient of every smooth metric normalized at0.
Thus ALL tuples in H are realizable normal metric N-jets, and every normalized
normal jet lies here. This is a finite-jet fact, not a curvature-array extension
or an existence theorem for DDR solutions. Higher Taylor coefficients of a
general metric do not affect an order-N response.

Changing the chosen orthonormal frame acts linearly on each H_s by the usual
rank-(s+2) covariant tensor representation. Normal coordinates of a fixed
metric with different orthonormal frames differ by that linear Lorentz change.
Naturality and finite-jet dependence therefore define an intrinsic germ

    Fhat:H -> Sym2(V*),   Fhat(h)=E[g_h](0),              (3)

on the declared neighborhood, equivariant under O(1,3) whenever both sides
are defined. No values of E on unrealizable metric data have been requested.
This is not a classification or proof of existence of every possible E.

## 3. The curvature block and its exact normalization

At0 the connection vanishes. With the curvature convention in the repository,

    R_abcd = (g_ad,bc+g_bc,ad-g_ac,bd-g_bd,ac)/2.         (4)

Only h2 enters. The linear map h2->R is an equivariant bijection from H_2 to
the20-dimensional algebraic curvature space K. Its inverse is

    h2_ij(x)=-(1/3) R_i a j b x^a x^b.                 (5)

The curvature pair symmetries/Bianchi identity give symmetry in i,j and (1).
Substitution in (4) recovers R. Conversely polarization of (1) at degree2,
inserted in (4), gives (5), so the map has no extra normal-coordinate kernel.
Both directions are algebraic identities, not a dimension count inferred
from a finite sample. Author checks independently test a full algebraic
curvature basis and the linear normal-condition rank as finite certificates.

## 4. Intrinsic regularity and the leading estimate

Assume Fhat is Frechet differentiable at h=0 on H. This is smooth dependence
of response on REALIZABLE local metric variations, not an assumption that a
smooth metric automatically has a differentiable response. It is a separate
sufficient hypothesis, not derived or physically adopted here. A differentiable
natural map on the full metric-jet bundle would suffice by restriction, but
is not needed as an extra ambient extension.

Let P(X)=X-(tr_eta X/4)eta and That=P Fhat. Equivariance gives
Fhat(0)=beta eta, hence That(0)=0, without assuming beta=0. Let L_s denote
the derivative block DThat_0 restricted to H_s. From (4)-(5) and the ENTIRE
reviewed G301 linear-equivariant basis,

    L_2(h2)=a S(R),  S(R)=Ric(R)-(tr_eta Ric(R)/4)eta.    (6)

The fixed coefficient a can be zero. The -I element of the specified full
Lorentz group acts on H_s by(-1)^s and on the rank-two output by+1. Thus

    L_s=0 for odd s.                                    (7)

This uses the stated group; no differently oriented/typed class is covered
by an unproved extension of the parity argument.

In the sum norm on H define the sufficiently-small-ball modulus

    omega(t)=sup_(0<||h||<=t)
        ||That(h)-DThat_0[h]||/||h||,  omega(t)->0.        (8)

Suppose the SUPPLIED family/set of normal tuples has

    ||h_s||<=M_s epsilon^s, 0<epsilon<=epsilon0<=1,       (9)
    M=sum_s M_s,   D=sum_(even s>=4) ||L_s|| M_s,

where M epsilon0^2 is within the germ ball. All-zero M is trivial. Then

    ||That(h)-a S(R(h2))||
       <= D epsilon^4 + M epsilon^2 omega(M epsilon^2). (10)

Proof: ||h||<=M epsilon^2; apply (8), remove odd linear blocks by (7),
and bound every remaining s>=4 linear term by epsilon^4. This is exactly
a GL1-type uniform estimate on genuine metric jets, without an assumed
response extension to the ambient curvature derivative product.

If, optionally, That is C1 and
||DThat(h)-DThat(0)||<=C||h||^alpha, 0<alpha<=1, on the ball, integrating
along [0,h] bounds the nonlinear term by C||h||^(1+alpha)/(1+alpha).
Replace the second term of(10) by
C M^(1+alpha) epsilon^(2+2alpha)/(1+alpha). Bare differentiability supplies
no power rate. This is sufficient regularity, not an optimality theorem.

For exact DDR and a!=0 only, (10) gives ||S||/epsilon^2->0; an approximate
balance ||That||<=rho(epsilon)epsilon^2 adds rho/|a| and requires rho->0.
These are conditional consequences, not replacement physical equations.
Normalization by actual ||Rm|| additionally needs its epsilon^2 lower bound.
Uniformity across different responses additionally needs uniform coefficients,
moduli and a nonzero lower bound on |a|. None is inferred from fixing one E.

## 5. Does the intrinsic regime correspond to actual curvature control?

Yes at finite-order weighted scope, with constants changed, not as a statement
that arbitrary curvature arrays are realizable. Write J_j=nabla^j Rm(0),
0<=j<=N-2. For actual normal metrics, h_s is a universal finite polynomial
in J_0,...,J_(s-2), of total weight s when J_j has weight j+2.
Here is a direct finite-order derivation that works in Lorentz signature.

Fix x in V and the geodesic gamma(t)=exp_0(tx). Parallel transport back to0.
The Jacobi variation of initial velocity y has transported matrix A(t,x)y,
where A(0)=0, A'(0)=I and

    A''(t,x)+K(t,x)A(t,x)=0,
    K_j(x)y=(nabla_x^j R)(y,x)x,
    K(t,x)=sum_j t^j K_j(x)/j!    (finite Taylor data).   (11)

Each K_j is a homogeneous degree-(j+2) polynomial in x and linear in J_j.
Use coefficients A(t,x)=sum_n t^n A_n(x), A_0=0,A_1=I. Equating finite
Taylor coefficients gives

    A_(n+2)=-sum_(j=0)^n (K_j/j!) A_(n-j)
                  /[(n+2)(n+1)].                       (12)

Terms with A_0 vanish. Induction makes A_n a finite polynomial of weight
n-1 for n>=1, with A_2=0. The pulled-back normal metric is
g(x)(y,z)=eta(A(1,x)y,A(1,x)z), so its degree-s part is

    h_s(x)(y,z)=sum_(p+q=s+2) eta(A_p(x)y,A_q(x)z).      (13)

No infinite Taylor convergence is asserted: only finitely many coefficients
of smooth geodesic/Jacobi solutions are used. Equivalently one can replace
x by ux, expand at u=0, and retain degree<=N before setting u=1 formally.
The weight statement follows. In particular, with eta-adjoint notation,

    h2 = -eta K0/3,
    h3 = -eta K1/6,
    h4 = eta(2 K0^2/45-K2/20).                         (14)

The K0^2 term is retained: treating all higher normal coefficients as merely
linear curvature derivatives would give a false pass here.

Consequently ||J_j||<=B_j epsilon^(j+2) implies (9), with finite M_s
depending on the finite coefficient polynomials, the B_j, N and chosen norms.
Finite-dimensional polarization passes from the polynomial-in-x coefficients
to coefficient norms; all constants are fixed in the declared frames.

Conversely coordinate curvature/covariant-derivative formulas at0 express
J_j as finite polynomials in h2,...,h_(j+2), since g(0)^-1=eta^-1 and the
finite derivatives of g^-1 are recursively polynomial in metric derivatives.
For the normal metric g_t(x)=g(tx)=t^-2 delta_t^*g with delta_t(x)=tx,
constant scaling and tensor pullback give exactly

    h_s(g_t)=t^s h_s(g),  J_j(g_t)=t^(j+2)J_j(g).       (15)

Thus those coordinate polynomials are weighted-homogeneous of weight j+2,
and (9) implies corresponding weighted J_j bounds. This proves equivalence
of the two FINITE-ORDER bounded regimes up to constants on realizable jets.
It does not make the regime automatic from curvature smallness alone.

The cited primary mathematical corroboration is Jentsch, arXiv1509.08269v2,
Theorem1 and AppendixB. The introduction explicitly permits indefinite
metrics. We do NOT import the Euclidean-qualified Theorem3(a) as a Lorentz
realization theorem. Equations(1)-(15) supply the needed finite-order argument
directly. This is standard geometric machinery applied to the response question,
not a newly discovered jet-isomorphism theorem or a UDT physical premise.

## 6. What has genuinely changed and what has not

The response need not be specified on non-realizable ambient curvature arrays
to obtain (10). A differentiable natural response on a full neighborhood of
realizable NORMAL METRIC jets suffices, and its weighted regime corresponds
to actual finite curvature-jet control. Nonlinear curvature compatibility
relations are automatically respected by evaluating actual metrics; no
arbitrary array is promoted to a metric or a field-law solution.

This removes a representation assumption at the stated conditional scope.
It does NOT derive response regularity, a full response neighborhood, a
selected finite order, a!=0, an invariant quietness law, physical small scale,
balanced-family existence/convergence, stability or empirical GR recovery.
Metric realization is kinematic, not a new development of the field equations.
Local dependence alone does not provide the other hypotheses; the source's
known degenerate alternatives remain controls, not rediscoveries here.

Initial data, query/frame/marking choices and domain controls are not additional
physical laws. Conversely the response-domain/regularity/type assumptions
cannot be hidden as initial data. No unique metric history is demanded. The
new result remains CONDITIONAL and UNPROMOTED, with the entire review controlling
use. No claim is made that these are necessary conditions for every GR limit,
that no other native route exists, or that a new physical premise is necessary.
