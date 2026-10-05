# OJM1 initial two-dimensional optical attachment candidate

Conditional extension of the supplied CGE1/CPR1/OAA1 geometry and histories.
Mathematical exploration preceded this freeze. Parent derived the quotient
basis, both Jacobi factors, limiting map and b_*=0 pole before reading matching
preliminary formulas from the two source-first reviewers. That later exposure
is disclosed; no different-model or blind-after-exposure claim is made.

## 1. The same geometry and an explicit size/angle query

Keep the source, receiver, orientations and strict regular outward ray domain
in WORK_ORDER and CPR1/OAA1 with their clarifications. In outgoing coordinates,

    g=-f du^2-2du dr+r^2(dtheta^2+sin^2(theta)dphi^2),
    f=1-2m/r-H^2 r^2, s=sqrt(1-f b^2/r^2)>0,
    k=(b^2/[r^2(1+s)],s,0,b/r^2), theta=pi/2.

Each ray has Killing energy1 and fixed signed b; different emissions have the
actual b(R) determined by incidence. At reception omega_o=A>0 and at emission
omega_e=(1-Omega b)/sqrt(h). Ordinary proper clocks give Z=omega_e/A.

Declare the infinitesimal source plane orthogonal to its proper velocity u_e
and to the received ray k_e. This is a physical rest-screen at the specified
source event, not a model of a disk, finite material surface or known standard
ruler. For a quotient-screen representative X, the actual rest-screen vector is

    X_u=X+[g(X,u)/omega_u] k.

It is orthogonal to u and k, and preserves inner products. Thus the source and
receiver use explicit isometric representatives of G348's quotient screen.
Finite source shape, orientation and ray-branch selection still require data.

## 2. Derive the complete Jacobi map from neighboring rays

On the equatorial central ray choose the orthonormal quotient representatives

    e_parallel=(b partial_u+partial_phi)/(r s),
    e_perp=partial_theta/r.

They are orthogonal to k and each other, have norm1, and are parallel in the
quotient. In fact e_perp is parallel as a spacetime vector. Metric compatibility,
planarity and null orthogonality then force nabla_k e_parallel to be a multiple
of k. The frame is regular at f=0 because s>0.

Write P(r,b)=integral_a^r b d rho/(rho^2 s),
I(r,b)=integral_a^r d rho/(rho^2 s^3), and s_a=s(a,b).
A variation of impact b through the same source event has, at fixed r,
delta u=b I delta b and delta phi=I delta b. Passing to fixed affine parameter
only adds a multiple of k, so its quotient component is r s I delta b.
Its initial affine derivative is delta b/(a s_a). A rotation of the orbital
plane about the source radial axis gives perpendicular component r sin(P)
times the rotation angle, with initial derivative b/a times that angle.
Therefore the forward vertex Jacobi block is diagonal in this parallel frame:

    B_parallel(a,r)=a s_a r s(r) I(r,b),
    B_perp(a,r)=a r sin(P(r,b))/b.                  (1)

At b=0 both are r-a, the continuous limit; this limit is not imposed on actual
nonradial incidences. Both satisfy B(a)=0, DB/dlambda(a)=1. Differentiation gives

    D^2 B_parallel/dlambda^2-q B_parallel=0,
    D^2 B_perp/dlambda^2+q B_perp=0,
    q=3m b^2/r^5.                                 (2)

These are original metric geodesic variations, with G348 curvature convention.
The null tide is diag(-q,+q). H has no explicit term in q, but enters the ray,
affine interval, b(R), clock frequencies and map. No disappearance of H's
observable influence or imported thin-lens equation follows.

G348 reciprocity gives B_eo=-B_oe^T. With matching parallel orthonormal endpoint
bases and the observed sky direction opposite future k, the size/angle map is

    delta x_e=J delta theta_o,
    J=-A B_eo=A diag(B_parallel,B_perp).            (3)

This is the full infinitesimal map, up to consistently applied endpoint rotations.
Define its area distance D_A by D_A^2=|det J|, not by declaring all lengths equal:

    D_A=A a R sqrt(|s_a s_R I sin(P)/b|).           (4)

A projected source circle maps to a generally anisotropic image. A single D_A
reproduces its area, not both directional sizes, unless the two singular values
coincide. The forward area distance is Z D_A; this is geometric reciprocity,
not a luminosity/flux law. Affine rescaling multiplies A and divides B, leaving
J unchanged. Physical endpoint observer changes retain G348's screen/sky rules.

## 3. Focusing, caustics and exact scope

B_parallel>0 for r>a on every stated outward ray. For b!=0 the only conjugate
points in this segment occur at P(r,b)=n pi with nonzero integer n. P has the
sign of b and increases in magnitude along the ray. At such an endpoint the
perpendicular factor crosses zero simply: its derivative is a cos(P)/r.
The full Jacobi phase propagator remains invertible, while the sky-position map
loses rank and cannot be inverted there. No caustic is discarded as an invalid
ray. Multiple global images are separate branches, not resolved by this formula.

Before the first conjugate point both forward factors are positive. Put
d=sqrt(B_parallel B_perp), l=lambda-lambda_e. Their equations imply

    d''/d=-(1/4)(B_parallel'/B_parallel-B_perp'/B_perp)^2 <=0.

Together with d(0)=0,d'(0)=1 this proves 0<d<=l, hence D_A<=D_o=A l.
For m>0 and b!=0, q>0 splits the logarithmic derivatives and the inequality
is strict at every positive pre-caustic interval. This is a geometric statement
on the declared branch; it is not extended through caustics with an absolute-
determinant substitution. No energy/matter or physical photon premise is added.

## 4. Actual late histories and the finite optical endpoint

Put S(b)=sqrt(1+H^2 b^2) and use the actual strict regular b(R)=b_*+O(R^-1).
I_infinity and P_infinity converge smoothly. Equations(1)-(3) and A~S/(HR) give

    j_parallel,*=a s_a,* S_*^2 I_infinity(b_*)/H >0,
    j_perp,*=a S_* sin(P_infinity(b_*))/(H b_*),
    D_A,*=sqrt(|j_parallel,* j_perp,*|).            (5)

The perpendicular expression uses its continuous b_*=0 limit. For nonzero
b_* this optical endpoint generally depends on the ray/source preparation;
it need not equal1/H. If P_infinity is a nonzero multiple of pi, its determinant
limit vanishes and no positive-endpoint/simple-pole claim is inferred. Away
from this limiting degeneracy the map is smooth in x=1/R; the next coefficient
also depends on actual b'(0). No universal approach sign or full-history ceiling
is established. H is supplied, not an observed Hubble parameter or selected scale.

Now take the existing u_infinity=phi_0=0 preparation, with b_*=0 but b(R)!=0
in general. Source uniform regularity bounds give, for small b and all large R,

    L=(R-a)+O(b^2 R),
    B_parallel=(R-a)+O(b^2 R), B_perp=(R-a)+O(b^2 R).

For example s and1/s are uniformly1+O(b^2), I=(1/a-1/R)+O(b^2),
and P/b=(1/a-1/R)+O(b^2), with smooth parameter derivatives. The finite
x-integrals, after the same tail subtraction as OAA1, justify smooth asymptotic
remainders. Since b(R)=O(1/R) and A=O(1/R), each eigenvalue of J differs from
D_o by O(R^-2). Eventually |P|<pi, so the whole connecting segment has no
conjugate point and both eigenvalues are positive. Consequently

    D_A=1/H-(a/H+E/H^2)/R+O(R^-2),
    Z(1/H-D_A) -> (a+E/H)/sqrt(h).                 (6)

The same leading pole is now attached to the actual infinitesimal angular-area
distance, and to each principal length factor at this order. The smooth tail
gives eventual monotone approach from below and nonattainment on that tail at
finite receiver proper time. No statement rules out earlier crossings or
identifies a universal X_max. Formula(6) is not a radial-only substitution and
does not assert exact D_A=D_o at finite nonradial incidence.

## 5. What this supplies and what remains open

For a supplied sufficiently small rest-screen ruler on a regular inverse branch,
J now predicts geometric apparent size/shape and Z predicts the same central
clock cadence. If a smooth finite map has a Hessian bound M on a regular patch,
its linear remainder is bounded by M|delta theta|^2/2. No numerical M, finite
disk/population model, emission physics or independent source size is supplied.
The infinitesimal result alone cannot be used as an unbounded finite-source fit.

The OAA1 optical-interface gap is narrowed: the full conditional map is explicit
and its specified late pole survives an angular-area readout. Native metric and
physical comparison selection, a calibrated length scale, astronomical source
model and empirical test remain open. The same physically matched GR geometry
and query give the same records. This does not establish an extra UDT effect,
X_max, canon, a whole-UDT obstruction or the necessity of a new premise.
