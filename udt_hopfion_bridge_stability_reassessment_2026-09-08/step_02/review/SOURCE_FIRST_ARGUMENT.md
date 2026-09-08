# Independent source-first HB2 argument

Constructed before author HB2 candidate exposure. This is a review argument,
conditional on the exact sources and their imported local Cauchy theorem.

Write g=gamma_w, eta=xi-flat, H=g-eta^2, JX=nabla_X xi. The Sasaki metric has
Jxi=0, J^2=-I on horizontal vectors, d eta(X,Y)=2g(JX,Y). Let
k_h=(C-b)/2, k_v=(C+b)/2 and h=-2K=(b-C)H-(b+C)eta^2.
The curve g_t=a H+c eta^2, a=1+t(b-C), c=1-t(b+C), is a globally smooth
positive metric for sufficiently small t, with the required first jet.
It is used only to compute the derivative. xi remains Killing for this curve
because xi(b)=0. Its squared norm is c, its dual is alpha_t=c eta.

In0<x<1 the metric is A dx^2+H_ab dphi^a dphi^b. Write A0=g_xx,
H0 for its angular matrix, W0=sqrt(det g), Z=H0^{-1}eta', and E=W0/A0.
eta'(xi)=0. Therefore

    sqrt(det g_t) A_t^{-1} H_t^{-1}(c eta)'
       = E[(c'/sqrt(c))xi + (c^(3/2)/a)Z].

For a Killing field the covariant identity delta d alpha_t=2Ric_t(xi,.)
follows by expanding d alpha and commuting the covariant derivatives of the
Killing equation. In these coordinates, its angular components are

    2Ric_t(xi,.)_a
      = -H_t,ab / sqrt(det g_t) * partial_x[
           sqrt(det g_t) A_t^{-1} H_t^{bc}(c eta_c)'].

For a fixed horizontal angular Y, the xi term contracts to zero. The old
mixed Ricci is zero, so g(Y,(EZ)')=0. It follows exactly on the auxiliary curve

    Ric_t(Y,xi) = -1/(2sqrt(c)A0) * (c^(3/2)/a)' * eta'(Y).

Since partial_t(c^(3/2)/a)'|0=-(5/2)b', differentiation gives

    dot Ric(Y,xi) = (5/(4A0)) b' eta'(Y)
                  = (5/2)g(J grad b,Y).

The radial mixed component vanishes by the block/angle-independent coordinate
curvature formula, as does g(J grad b,partial_x). Thus the covector identity
holds for all horizontal Y. Both sides are globally smooth intrinsic tensors;
equality on the dense interior extends to both axes. No angular-coordinate
singularity is promoted to a physical singularity.

Now A=g^{-1}Ric=lambda_h I+D P, P=xi tensor eta, lambda_h=(R-2)/2,
D=2-lambda_h=(6-R)/2. The actual derivative is

    dot A = g^{-1}dot Ric - g^{-1}h A.

The second term is retained. h-sharp commutes with P and is diagonal in this
splitting, so its horizontal-vertical block is zero (its diagonal part is not
zero). Differentiating the eigenvalue equation therefore gives

    V=Q dot P xi = (5/(2D))J grad b = 5/(6-R) J grad b,
    dot P = V tensor eta + xi tensor V-flat.

The second block follows by differentiating metric self-adjointness and using
[h-sharp,P]=0. P^2=P excludes diagonal projector blocks. A positive-sign unit
representative with initial value xi has derivative V+(C+b)xi/2, since its
normalization is with g_t. Reversing representative sign does not alter P.

G332 gives db=dR/(b+C), b+C=epsilon sqrt(2(R+2C^2-2Lambda)). Consequently

    V = 5/[(6-R)(b+C)] J grad R.

On the strict simple-gap domain, drift vanishes at exactly the critical points
of R: J is invertible horizontally and xi(R)=0. Reversing epsilon at fixed
gamma,C,Lambda reverses V. It does not generally negate the complete K unless
C also reverses. Equal weights give constant R and zero first drift. The
scalar-gradient critical set for unequal weights is to be checked directly
from the source metric; no orbit conclusion is inferred from it.

Global domain: on compact S3 strict radicand and simple gap give positive
uniform margins. Smooth lawful G332 data meet the imported smooth Einstein
Cauchy interface (boundary-free compact manifold, gamma>0, smooth K, four
constraints, connected constant Lambda, harmonic reduction/Bianchi propagation).
Conditional smooth local development and a sufficiently small Gaussian-normal
tubular neighborhood exist; C2 continuity preserves the gap locally. No new
proof of the imported PDE theorem is claimed. First nonzero P-dot prevents
P(t) being identically P(0) near zero under this specified pullback; it says
nothing by itself about periodic orbits, topology, stability or physical matter.

At D=0 the spectral-line derivative is not defined by this formula. At zero
radicand the assumed smooth square-root branch is unavailable. Neither limit
is assigned the nondegenerate conclusion. The unscaled family is the target;
no physical scale or homothety selection is introduced.
