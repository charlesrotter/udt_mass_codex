# IEC1 local geometric justification and coefficient verification

This source-preserving completion supplies the local indefinite-signature proof
requested by the initial candidate and reviewers. It changes no physical premise
or coefficient. The original candidate stays fixed. Actual exact reconstruction
and control receipts, rather than this prose, own their pass/fail status.

## Local symmetry without a positive-definite/global assumption

At o let J_X(Y)=R(Y,X)X. Along t↦exp_o(tX), parallel-frame Jacobi variation
satisfies j''+J_X j=0, j(0)=0,j'(0)=Y because ∇R=0. Hence

 (d exp_o)_X Y=P_X S_X Y,
 S_X=sum_{r>=0}(-J_X)^r/(2r+1)!.

P_X is metric parallel transport. The power series is entire in the finite
matrix J_X; no diagonalizability or non-null X is needed. In a normal chart,

 (exp_o^*g)_X(Y,Z)=g_o(S_XY,S_XZ).

Because J_X is quadratic in X, this metric is analytic and even in X. Therefore
X↦−X is a local isometry; the same construction works at each nearby point.
All statements are local on a nondegenerate normal neighborhood. No positive-
definite spectral theorem, global completeness or global decomposition is used.

For a geodesic γ, its point reflection about γ(t/2) sends γ(s) toγ(t−s).
Its differential is minus parallel transport along γ: it is −Id at the midpoint,
and an isometry carries parallel fields to parallel fields. Compose it with the
reflection atγ(0). The resulting τ_t sendsγ(s) toγ(s+t) and its differential is
parallel transport. τ_t τ_s=τ_(t+s), since both sides have the same value and
first derivative atγ(0), and a local isometry is determined by that one-jet via
its action on nearby exponential geodesics. These are the needed transvections.

Infinitesimal transvections K_X have K_X(o)=X and ∇K_X(o)=0. Isotropy fields
vanish at o and their derivatives are skew metric endomorphisms. Killing fields
are determined locally by these jets (restrict to Jacobi fields along radial
geodesics), giving a finite-dimensional local Lie algebra. The point reflection
splits it into h+p, with p identified with T_oM and h with infinitesimal isotropy.
For an infinitesimal isometric flow, the Killing identity reads
(∇_Z∇K_X)(Y)=R(Z,K_X)Y with the present curvature convention. It follows
from differentiating the Killing equation and commuting covariant derivatives;
it is signature independent. At o this gives

 ∇_Z[K_X,K_Y]=R(Z,Y)X−R(Z,X)Y=R(X,Y)Z.

The fundamental fields of a left group action reverse the group Lie bracket.
Consequently, in the group algebra [X,Y] acts on p as −R(X,Y), and
[H,X]=HX, or R(X,Y)Z=−[[X,Y],Z]. This fixes the sign rather than borrowing
a possibly opposite convention. The original space-form controls separately
check this normalization.

The local group involution σ induced by the point reflection is −1 on p and
+1 on h. Near identity, (Z,H)↦exp(Z)exp(H) is a local diffeomorphism because
its derivative is the direct sum p+h. Thus G=exp(Z)k locally, with k isotropy
and σ(k)=k. Direct multiplication gives G σ(G)^-1=exp(2Z). This uses only a
local split, not a global polar/Cartan decomposition or Killing-form metric.
Flat central directions are not discarded.

## The actual interval and the actual return

τ_(Ln) carries o toB(0) and U to its parallel preparation. It therefore carries
the whole geodesic A(b) toB(b). Translate A(s) back to o by exp(-sU). The relative
point is G.o with G=exp(-sU)exp(Ln)exp(bU). The radial vector just established is

 Z=1/2 log[exp(-sU)exp(Ln)exp(2bU)exp(Ln)exp(-sU)].

The radial geodesic has constant squared speed g_o(Z,Z), which is its squared
geodesic interval F, including null intervals. In a small convex chronological
tube, the specified outgoing and later return null branches are regular and
unique. Solve F(0,b)=0 near b=L, then F(a,b)=0 near a=2L. Endpoint derivatives
are p=-F_s/F_b at(0,b) and q=-F_b/F_s at(a,b). No future exchange symmetry is
assumed. The inverse branch of the first signal is not used as the return.

Under s=Lx,b=Ly the palindromic product at−L is its inverse. Its local logarithm
is odd and F/L² is analytic in L². Its leading term1−(y−x)² has nonzero
partial derivatives at(0,1) and(2,1). The analytic implicit-function theorem
therefore controls both arrival derivatives and the O(L⁸) remainder in D for
each fixed geometry/frame. There is no supplied finite error constant, uniform
boost bound or global arrival theorem. Evenness in signed L does not assert
invariance under n↦−n for physical future clocks: the analytic branch at negative
L is past-directed, and the physical future branch would have to be changed.

## Exact algebra, not a fit of invariants

The construction multiplies the five free associative exponentials through
degree7 and forms the finite logarithm. Left-nested commutators recover the
homogeneous Lie terms; the saved Z representation has2 degree1,2 degree3,
8 degree5 and32 degree7 terms. The parent check independently re-expands each
saved commutator into words and compares every coefficient against the original
associative product/log, so it need not accept a remembered Dynkin projection
formula unchecked. This is exact finite symbolic correspondence, not independent
physical evidence or a floating matrix test.

Pairings use only metric skew-adjointness and curvature pair symmetry. For
C=R(n,U), A=CU,B=Cn, g(U,A)=g(n,B)=0, g(n,A)=T and g(U,B)=−T.
For e,z,w in {U,n},

 g(e,R(V,z)w)=−g(V,R(w,e)z).

This reduces degree1×5 to pairings of A/B and degree1×7 to degree3×5.
The remaining degree3×5 terms are the Kij contractions in INITIAL_CANDIDATE.
The relation index1=index2 is not a fitted simplification: ∇R=0 implies the
curvature endomorphism acts as a derivation of R,
[C,R(X,Y)]=R(CX,Y)+R(X,CY). Put X=n,Y=U to get
0=R(B,U)+R(n,A), hence R(A,n)=R(B,U).

All resulting interval coefficients through degree8 are retained, as are the
successive original-incidence roots and derivatives. Their exact expansion gives
the stated d4,d6. The full interval/tensor derivation owns universality in this
locally symmetric sector; finite original metric controls challenge signs,
normalization, preparation and return handling but cannot prove that universality.
The cubic expression is not inferred by fitting a list of numerical examples.

The V=0 corollary follows by the explicit K substitutions in the original
candidate. A general clock plane has both V and W, and its quartic term can have
either sign. Curvature invariance of the plane would require V=W=0; no converse
from vanishing one or two measured coefficients is claimed. Physical FC adoption,
UDT geometry/field selection, local-scale calibration and positional attribution
remain outside the conclusion.
