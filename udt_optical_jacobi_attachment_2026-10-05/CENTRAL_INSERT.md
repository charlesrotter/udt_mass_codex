<a id="r13ojm"></a>

#### The actual two-dimensional optical map — OJM1

OAA1's affine endpoint does not by definition give apparent source size. OJM1
calculates that missing map on the same CONDITIONAL metric and actual histories.
Keep m>0,H>0,a>3m,Omega=sqrt(m/a³-H²)>0, strict outward s>0 and one fixed
finite-E escaping receiver from CPR1. No metric, population or field-law
selection is added. Every central ray has its own conserved b; the actual
emission sequence still has varying b(R).

Declare the infinitesimal source rest-screen orthogonal to u_e and k_e. For a
quotient vector X the representative X_u=X+g(X,u)k/omega_u is orthogonal to
u and k and has the same quotient inner products. Thus source and receiver
screen lengths are explicitly tied to their proper frames without an extra
source-frequency stretch. A finite material disk or known ruler is not supplied.

In outgoing EF coordinates, along the equatorial ray, choose

    e_parallel=(b partial_u+partial_phi)/(r s), e_perp=partial_theta/r.

They form a regular orthonormal quotient frame through f=0. e_perp is parallel;
metric compatibility, planarity and null orthogonality imply that the derivative
of e_parallel is a multiple of k. It therefore is parallel in the quotient.
Let P=integral_a^r b d rho/(rho²s), I=integral_a^r d rho/(rho²s³), s_a=s(a,b).
Varying b from the same source event gives at fixed r the connecting vector
(delta u,delta r,delta phi)=(b I,0,I)delta b. Fixing affine parameter changes
it only along k. Its screen length component is r s I delta b and initial
affine derivative delta b/(a s_a). Rotating the ray plane about the source
radial axis instead gives r sin(P) times the rotation, with initial slope b/a.
The complete forward vertex block in this parallel basis is therefore

    B_parallel=a s_a r s(r) I, B_perp=a r sin(P)/b.

Both continue to r-a at b=0 and have B(a)=0,B'(a)=1. Differentiating with
d/dlambda=s d/dr gives B_parallel''-q B_parallel=0 and B_perp''+q B_perp=0,
where q=3mb²/r^5. This derives the null tide diag(-q,+q) from actual metric
geodesic variations. H still enters s, affine length, incidence and frequency;
its absence as an explicit term in q does not remove those effects.

G348 reversal now supplies the map from observed sky angle to source size:

    delta x_e=J delta theta_o,
    J=-A B_eo=A diag(B_parallel,B_perp),
    D_A²=|det J|, D_A=A a R sqrt(|s_a s_R I sin(P)/b|).

The source-size-to-sky map is J^{-1} only where det J!=0. D_A is an angular-
area distance; it does not convert both directional lengths by one scalar when
the image is sheared. The corresponding forward area distance is Z D_A by
geometric reciprocity, without a flux or luminosity law. Positive affine
rescaling leaves J invariant; changing the physical receiver has the existing
G348 frequency/screen effect. Endpoint basis changes must also rotate the
source coordinates. These statements apply to the infinitesimal rest-screen.

B_parallel>0 on every stated outward segment. For b!=0, conjugate points
occur exactly at P=n pi, n a nonzero integer. P grows monotonically in magnitude;
the perpendicular zero has affine derivative a cos(P)/r, so it is simple.
The full phase map remains invertible there, whereas the sky-position inverse
fails. Strict outgoing ray regularity therefore is not a no-caustic theorem.
Global multiple images remain separately labeled branches.

Before the first caustic both B factors are positive. For d=sqrt(B_parallel B_perp),

    d''/d=-(1/4)(B_parallel'/B_parallel-B_perp'/B_perp)²<=0.

The vertex data d(0)=0,d'(0)=1 imply D_A<=D_o. With m>0,b!=0 the nonzero
tide generates unequal logarithmic derivatives and the inequality is strict
at positive separation before the first caustic. It cannot be extended through
a conjugate crossing by inserting absolute values. Independent finite original-
metric checks include strongly focused branches with negative B_perp; those
valid rays and initially failed finite-angle approximations are preserved.

For a strict limiting incidence b(R)=b_*+O(1/R), S_*=sqrt(1+H²b_*²), the
two signed limiting length factors are

    j_parallel,*=a s_a,* S_*² I_infinity(b_*)/H,
    j_perp,*=a S_* sin(P_infinity(b_*))/(H b_*),
    D_A,*=sqrt(|j_parallel,* j_perp,*|).

Use the continuous b_*=0 limit. Generic endpoints depend on source/ray data;
they are not automatically1/H. If P_infinity is a nonzero multiple of pi,
the area limit vanishes and the next order must be studied separately. No
general approach sign, universal ceiling or all-history claim follows.

On the already supplied b_*=0 preparation, b(R)=O(1/R) rather than identically
zero. Uniform small-b expansion gives L=R-a+O(b²R) and each B=R-a+O(b²R).
For example1/s=1+O(b²), I=1/a-1/R+O(b²), P/b=1/a-1/R+O(b²) uniformly;
the strict source margin and smooth x=1/R integral tails control the remainders.
Since A=O(1/R), each eigenvalue of J is D_o+O(R^-2). Eventually |P|<pi,
so the whole connecting segment is caustic-free. The smooth tail consequently has

    D_A=1/H-(a/H+E/H²)/R+O(R^-2),
    Z(1/H-D_A)->(a+E/H)/sqrt(h).

Thus the specific pole survives the full angular-area calculation and each
principal length factor at this order. The eventual approach is from below
and monotone; finite-time nonattainment is asserted only on that tail. Exact
finite-ray equality D_A=D_o is not asserted, nor are earlier crossings excluded.

The [initial derivation](udt_optical_jacobi_attachment_2026-10-05/INITIAL_CANDIDATE.md)
and [map/error clarification](udt_optical_jacobi_attachment_2026-10-05/CLARIFICATIONS.md)
retain full hypotheses. Parent exact and40/70digit controls pass; two fresh
contexts reconstruct the argument and replay saved quantities with distinct
implementations, including an original four-dimensional metric/Jacobi check.
Their [work record](udt_optical_jacobi_attachment_2026-10-05/WORK_RECORD.md)
preserves finite-angle failure/repair and same-model/library limits. Numerical
agreement and regression are not interval certification or native selection.

A finite map x(theta) with a supplied Hessian bound M has the usual forward
remainder M|delta theta|²/2; inverse angular error needs its own control. No such
numeric bound, finite source/disk, known astronomical ruler or flux law is
provided. The conditional optical calculation is now explicit; native metric/
comparison selection, independent physical source/scale calibration and data
remain open. H is not an identified observed Hubble constant or X_max.
Physically matched GR queries still give the same records. No additional UDT
prediction or need for a new postulate has been established by this calculation.
