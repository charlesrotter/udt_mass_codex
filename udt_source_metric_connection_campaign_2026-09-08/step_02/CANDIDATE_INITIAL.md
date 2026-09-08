# SM2 initial candidate — a constrained optional tensor class

Explored then frozen2026-09-08 for fresh review. CONDITIONAL CANDIDATE only.
Prerecorded class: ../SM2_PLANNED_CLASS.md; reviewed conditional dependency:
SM1 ../step_01/REVIEWED_RESULT.md and its pinned candidate/review. All source,
regularity, positive AC density, supplied phase/spacing/product/label and
orientation caveats carry forward. No curvature recipe or physical adoption.

## Exact class and quantifier

Let q_a=d(Theta/Delta)_a, ell=q-sharp and j=n ell with n>0. We consider a
single smooth natural algebraic prescription P_ab(g,q,n), symmetric covariant
rank two, at each event. Natural means equivariant under proper orthochronous
Lorentz frame changes (and hence coordinate-independent tensor construction).
There are no additional input vectors, label values, phase VALUE, curvature,
derivatives of n/q/g, nonlocal data or prescribed functions of position.
q itself already contains one phase derivative. Fixed constants/parameters
in the prescription may remain unselected. No linearity, sign condition,
energy meaning, cross-family addition, dimensional coupling law or metric
source equation is imposed. This OPTIONAL mathematical class is not an
exhaustive set of UDT source possibilities or an adopted physical class.

Require div(P)=0 for EVERY regular SM1 product tube and every locally smooth
positive finite label density, in particular for parallel and expanding
null tubes in the admitted flat metric. This universal identity is an optional
Bianchi-compatibility screen. It is stronger than compatibility on one chosen
physical history and is not claimed to be a native UDT requirement.

## Algebraic naturality without assuming a source form

At a point choose an auxiliary null frame (ell,k,e1,e2), with g(ell,k)=-1,
positive orthonormal eA, and all other pairings zero. k and eA are only proof
tools, not added inputs. Rotations of the e1/e2 plane fix (g,q,n). An invariant
symmetric bilinear P therefore has frame matrix

    [[u,v,0,0], [v,w,0,0], [0,0,z,0], [0,0,0,z]].

Null rotations also fix ell and q. Use

    ell'=ell,  e1'=e1+t ell,
    k'=k+t e1+(t^2/2)ell,  e2'=e2.

Invariance of P(ell,e1') requires t*u=0 for all t, hence u=0.
Invariance of P(e1',k') then requires t*(z+v)=0, hence v=-z.
Thus the invariant space is exactly span{g,q tensor q}, with z and w free.
Conversely both tensors are invariant under the full stabilizer. Nonzero
future null covectors form one Lorentz orbit, so there is no further scalar
invariant of q at fixed g. Only n (and fixed parameters) can enter coefficients:

    P_ab = A(n) g_ab + B(n) q_a q_b.                              (SM2.1)

Orientation/time orientation supply no extra symmetric rank-two tensor from
one null direction. Smoothness yields smooth A,B on the connected n>0 domain.
This classification does not include derivative/curvature constructions or
independent label/phase-value fields, even though those could define other
explicitly enlarged mathematical classes.

## General divergence and necessity of the density dependence

SM1 gives nabla_ell q=0 and ell(n)+n theta=0, where theta=div(ell).
Metric compatibility and the product rule give, for EVERY tube in the class,

    nabla^a P_ab = A'(n) d_b n + [B(n)-n B'(n)] theta q_b.          (SM2.2)

Necessity is not inferred from a finite numerical sample. The following
analytic families belong to the required quantifier and allow arbitrary n0>0:

1. Flat parallel phase: g=2 dr dphi+dx^2+dy^2, q=dphi, J=1,
   n=s(x,y). Near any point take s=n0+epsilon*x on a small bounded label
   patch, epsilon!=0 and s>0. The product is phase independent, theta=0,
   and dn has a nonzero screen component. Equation(SM2.2) implies A'(n0)=0.
   Since n0 was arbitrary, A=A0 is constant on n>0.
2. Flat outgoing phase: g=2 dr dphi-dphi^2+r^2(dvartheta^2+
   sin(vartheta)^2 dpsi^2), r>0, away from angular poles. Here phi=r-t,
   ell=partial_r, J=r^2 sin(vartheta), theta=2/r!=0. Choose any smooth
   positive finite s(vartheta,psi); its value can realize any chosen n0
   at the event. Thus (SM2.2) forces B(n0)-n0 B'(n0)=0 for every n0>0.
   The ordinary differential identity (B/n)'=0 gives B=C n.

Both are local coordinate forms of the same flat Lorentzian geometry, not
new metric solves or assumptions that arbitrary adapted metrics are vacuum.
The selected examples serve as analytic necessity probes within a universal
class, not evidence that flat geometry or a populated phase is selected.

Conversely for arbitrary constants A0,C,

    P_ab = A0 g_ab + C n q_a q_b                                 (SM2.3)

has zero divergence on EVERY SM1 tube, since nabla(g)=0, div(j)=0 and
nabla_ell q=0. This sufficiency needs no vacuum equation, and even holds for
the broader conserved aligned currents with phase-dependent quotient density.
No physical source-sector UDT equation is inferred from this geometric fact.

Therefore(SM2.3) is necessary AND sufficient for the stated universal identity
WITHIN the declared algebraic natural class. Positivity of C, nonzero C,
physical normalization, scale or interpretation is not fixed. The A0 term
is metric proportional and can be absorbed into a constant scalar term only
in a separately declared constant-coefficient metric-equation comparison.

## Alternatives tested, data freedom and scope boundary

A nonlinear density function is not automatically inconsistent on one chosen
tube: on a flat parallel congruence theta=0 and ell(n)=0, any B(n) is conserved.
It fails the UNIVERSAL screen when B-nB' is nonzero and expansion is nonzero.
For example B=n^2 gives residual -n^2 theta q. A varying A(n) similarly fails
the transverse-density probe. This constrains a class of prescriptions, not
the legitimacy of all initial data or the admitted UDT metric equations.

If the available data are EXPLICITLY enlarged by a supplied scalar w with
ell(w)=0, then P=A0 g+n w q tensor q is conserved as well. In a local flow
box w=W(phi,y) is freely supplied initial transverse data transported along
the rays. It need not be a constant, and need not preserve a phase-independent
product if folded into mu. This is a sufficient enlarged-class construction,
not a complete enlarged-class classification. The choice to add w as a
physical quantity or adopt this formula is NOT made. Merely specifying values
of a scalar already present in a chosen mathematical model is data selection;
declaring its physical status or its coupling is a separate issue.

The finite symbolic checker tests stabilizer algebra, the displayed divergence
identity and defect residuals. The analytic family argument supplies necessity
for all n>0; test counts do not. A conserved tensor is not yet a metric source,
stress-energy, physical carried content, source evolution or a closed coupled
system. SM3 may assess that missing interface only after fresh review.
