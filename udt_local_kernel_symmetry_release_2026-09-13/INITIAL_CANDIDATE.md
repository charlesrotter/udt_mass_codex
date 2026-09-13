# LSR1 — symmetry-release candidate

UNPROMOTED MATHEMATICAL CANDIDATE; computation/review pending at freeze.
This is a sufficiency test of retained geometric hypotheses, not an admitted
native nonspherical UDT solution or a new physical premise. G166's native
assembly join remains OPEN. G179's supplied-pair evaluator and G176's WORKING
completed reciprocity apply at their existing scopes. No field equation enters.

## Question, comparison class and quantifier

G288 proves a leading quiet center in its static, analytic-even, round-spherical
reciprocal areal metric. Keep staticity, analyticity/evenness at a calibrated
Cartesian center, the entire original radial clock/ruler block, vanishing
radial-angular mixing, and the area 4 pi r^2 of centered spheres. Remove their
round intrinsic geometry. Do these retained conditions force G288's leading
zero null-screen tide? A regular counterexample suffices to refute that geometric
implication. It cannot refute G288's actual theorem or establish a physical UDT
counterexample before native admission is supplied.

The center, radial congruence and common coordinate marking are supplied
comparison data, not a preferred physical center/frame. Staticity, analytic
evenness and the radial profile are inherited restrictions, not purported
universal postulates. The construction below is free-and-explored within this
declared class. No desired observational behavior is an acceptance criterion.

## Exact local construction

Use dimension-matched x0=c_E t, Euclidean auxiliary coordinates x in R^3,
r=|x|, n=x/r and P=I-n n^T. The auxiliary Euclidean form defines this construction
and comparison marking, not an additional physical background field. Let c be
real and S a constant real symmetric tracefree 3 by 3 matrix (five free
components). Let C(x)v=x cross v and define

    f=1+c r^2, D(x)=C(x)^T S C(x),
    M(r)=average_{n in S^2} sqrt(det_{n-perp}(I+D(r n))), q(r)=1/M(r),
    gamma=f^-1 n n^T + q(r)[P+D(x)],
    g=-f (dx0)^2 + gamma_ij dx^i dx^j.

Here the determinant is on the auxiliary orthonormal tangent plane. The
normalizing q is fixed by the retained areal condition; it is not a fitted
profile or a physical law. Restrict to |c|r^2<1/2 and r^2||S||op<1/2. Then f>0,
I+D is positive on the tangent plane, M,q>0, and g is Lorentzian. These are
parameter-dependent existence bounds, not a selected radius or cutoff.

D is a quadratic polynomial, D x=0. The tangent determinant is

    1-r^2 n^T S n+r^4 n^T adj(S)n.

Its positive square root is uniformly analytic in r^2 in a small neighborhood.
Sphere averaging therefore gives an analytic M and q. With tr S=0,

    <n^T S n>=0,
    <n^T adj(S)n>=-tr(S^2)/6,
    <(n^T S n)^2>=2 tr(S^2)/15,
    M=1-tr(S^2)r^4/10+O(r^6), q=1+tr(S^2)r^4/10+O(r^6).

In Cartesian form gamma=I+(f^-1-1)xx^T/r^2+(q-1)P+qD. The first
nonconstant term here is -c xx^T/(1+c r^2); (q-1)P is analytic because q-1
is divisible by r^4. Thus the metric extends analytically and evenly through
x=0, with g(0)=diag(-1,1,1,1) and all first derivatives zero.

For r>0, gamma(n,n)=f^-1 and gamma(n,w)=0 for every w perpendicular to n.
The angular area is r^2 q integral sqrt(det(I+D))dOmega=4 pi r^2 exactly.
At S=0, q=1 and g is exactly G288's f=1+c r^2 family. For S nonzero,
the radial raw pair is still diag(-f,1/f) with m=1. The construction changes
the angular shape, with the inherited total area and radial block held fixed.

## Original-metric leading curvature

The exact Cartesian second jet is

    g00=-1-c r^2, g0i=0,
    gij=delta_ij-c x_i x_j+D_ij(x)+O(r^4).

The analytic remainder has zero derivatives through order three at the center;
it does not contribute to the curvature there. With G288's convention
R^a_bcd=partial_c Gamma^a_db-partial_d Gamma^a_cb
          +Gamma^a_ce Gamma^e_db-Gamma^a_de Gamma^e_cb,
direct differentiation at this zero-connection point gives

    R_0i0j=c delta_ij, R_0ijk=0,
    R_ijkl=-c(delta_ik delta_jl-delta_il delta_jk)
             -3 epsilon_ijp epsilon_klq S_pq,
    Ric_00=3c, Ric_ij=-3c delta_ij+3S_ij, R=-12c,
    C_0i0j=3S_ij/2,
    Riemann^2=24c^2+36 tr(S^2), Ricci^2=36c^2+9 tr(S^2),
    Weyl^2=18 tr(S^2).

These formulas are candidate analytical identities, to be checked from original
metric derivatives rather than used to manufacture their own verification.
For S nonzero, positive Weyl^2 distinguishes the center from the quadratic
spherical family; this is not merely a coordinate relabeling of that family.
No stress tensor, field law, physical mass or content is inferred from Ricci.

For a clock-normalized metric-null vector k=U+n at the center, with U=partial_0
and unit n, and any Euclidean orthonormal screen v,w perpendicular to n,

    T(v,w)=R(v,k,w,k)=-3(v cross n)^T S(w cross n).

The constant-curvature c contribution cancels, but independent angular second
derivatives survive. This is a geometric contraction, not a model of light or
an instrument. Within this exact five-parameter angular family, all central
null-screen tides vanish for all n,v,w if and only if S=0. Indeed choosing
n perpendicular to any unit a realizes a=v cross n, so vanishing implies
a^T S a=0 for every a and hence S=0 by polarization. This is only a
family-scoped equivalence, not a completeness theorem for UDT or all metrics.

## A sign-sensitive witness and G288 comparison

Take S=diag(s,2s,-3s), s nonzero. Approach the center along x=r e1 and use
the exact normalized null direction k=f^-1/2 partial_0+gamma_33^-1/2 partial_3
and screens v=gamma_11^-1/2 partial_1, w=gamma_22^-1/2 partial_2. Gamma is
diagonal on this ray, so these are actual metric-null/orthonormal vectors.
Incidence relative to the radial direction is pi/2 throughout. Their limits give

    T(v,v)=-6s+O(r^2), T(w,w)=-3s+O(r^2), T(v,w)=O(r^2).

Even analyticity gives the stated local remainder for fixed parameters.
The comparison-scaled quantities r^2 T start at order r^2, with coefficients
-6s and -3s. G288's scaled A start at order r^4 when c4 is nonzero, while
its raw T start at order r^2; in its quadratic c4=0 subclass both vanish
identically. Do not confuse these normalizations. The witness's 2:1 leading
ratio is an example, not a universal nonspherical ratio or a transplanted
definition of G288's channels. All central limits use the explicit screen above.

## Kernel, full records and what survives

The complete radial record, lapse N=sqrt(f), Phi=-log(N), chi=tanh(Phi),
proper radial ruler dr/sqrt(f), and static proper radial acceleration f'/(2sqrt(f))
are identical throughout this comparison family. The acceleration follows from
a_i=partial_i log N and the exact radial inverse metric, not a field equation.

For any fixed nonzero coordinate direction v, the actual local pair surface
F_(a,v)(x0,sigma)=(x0,a+sigma v) has

    h_v=diag(-f,gamma(v,v)), m_v^2=f gamma(v,v),
    H_v=diag(-f,1/f), Phi_v=-log(sqrt(f)).

These supplied regular pairs coexist in the same metric; no independent pair
metrics are glued. All normalized H and Phi fields are the same for all S,
but the original ruler densities differ off the radial direction:

    m_v^2=|v|^2+c[r^2|v|^2-(x dot v)^2]+v^T D(x)v+O(r^4).

Keeping m and the common marking retains that information. ER1/G213's existing
six-direction polarization recovers gamma from these full records. This is a
reuse of record sufficiency, not a new inverse theorem; curvature requires the
corresponding common second derivatives, not six isolated values. No measurement
protocol or physical pair-selection rule is supplied. The scalar's unchanged
value is not evidence that the complete metric/kernel record is unchanged.

## Maximum conclusion and open join

The retained radial reciprocity, regularity, staticity and areal normalization
alone do not force G288's leading quiet center in this explicitly supplied
geometric comparison class. Round angular geometry supplies a load-bearing
restriction. Radial clock/ruler relations survive exactly in the example;
leading null-screen quietness and quartic scaled onset do not extend generally.
G288 remains valid at its reviewed spherical scope.

This does not show that UDT admits S nonzero, predicts a new effect, selects
any c or S, or needs an extra physical postulate. Native complete nonspherical
assembly is still the unresolved join. The next useful question is what the
existing native premises actually constrain about this angular metric second
jet. That question is a return-point proposal, not authorized continuation.
