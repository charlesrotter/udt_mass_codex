# RT1 initial candidate — local curvature reconstruction and its fibre

Explored then frozen2026-09-08 for fresh separate-context adversarial review.
CONDITIONAL CANDIDATE, NOT BANKED. Question/regime/discovery: ../WORK_ORDER.md
and DISCOVERY_RECORD.md. General arguments below, not finite checks, own the
quantifiers. Sources: G313's Bianchi/curvature convention, banked G367--G369
and their ENTIRE original SM1/SM3 proofs/reviews. No old curvature recipe.

## 1. Exact question and comparison status

Let g be a supplied smooth time-oriented4D Lorentz metric, signature(-+++),
on a sufficiently small connected regular patch. Write

    S_ab=Ric_ab-(R/4)g_ab,       A^a_b=g^ac S_cb.

Fix a NONZERO real constant beta as an OPTIONAL comparison parameter. Ask
whether locally there exist smooth n>0 and phi such that

    q=dphi !=0, q^2=0, q-sharp future,
    S=beta n q tensor q,       div[j]=0, j=n q-sharp.              (RT1.1)

This is a mathematical representability question, not a sourced UDT law.
G312/G313's currently admitted bounded VACUUM arena has S=0, excluded from
this nonzero class. A nonzero example below is NOT an admitted vacuum history
or a new scientific solve. No claim is made that this comparison must be
physically adopted, or that carried content must gravitate in this form.

The G352 CHOSEN phase-independent label product is NOT included in(RT1.1).
G367 distinguishes it from mere conservation. Full product matching with
supplied labels/measure is a separate RT2 gate, not an inferred converse.
Delta>0 may later be supplied and Theta=Delta phi; no physical phase unit is
selected. Global exactness, zeros/rank changes, singular/atomic measures,
caustics, coupled evolution, genericity and stability are excluded.

## 2. Local characterization

Near any point with S!=0, (RT1.1) exists if and only if the following hold
throughout a sufficiently small neighborhood:

1. The FULL endomorphism satisfies A^2=0. Equivalently S has rank one
   (S is already symmetric and trace-free in Lorentz signature).
2. The nonzero rank-one sign epsilon equals sign(beta). Equivalently
   sign[S(U,U)]=sign(beta) for any future unit timelike auxiliary U.
3. A smooth future-raised representative b of the resulting null covector
   line satisfies b wedge db=0. This is independent of nonzero rescaling.
4. dR=0.

These form a sufficient AND necessary list, not a proved minimal independent
list. In particular this step does not exhibit a constant-scalar null-Ricci
METRIC with twisting line; independence of condition3 from the other metric
conditions is NOT claimed. The equivalence itself does not require it.
For an externally prescribed Lambda_*, additionally require R=4Lambda_*;
otherwise Lambda_*=R/4 is simply the constant of this supplied metric.

### Algebra and smooth line extraction

A is g-self-adjoint. If A^2=0, g(Au,Av)=g(u,A^2v)=0 for all u,v.
Its image is totally null. A Lorentz vector space has maximal totally null
dimension one: in an orthonormal frame, equality in the Euclidean Cauchy
inequality for two orthogonal null vectors makes them collinear. Since A!=0,
rank(A)=1. A symmetric real rank-one bilinear form is epsilon b tensor b,
epsilon=+1 or-1; trace-free then gives b^2=0. Conversely such a null rank-one
tensor has A^2=0. Testing only tr(A^2)=0 is strictly weaker.

On the retained constant-rank patch choose ANY smooth future unit timelike U
as a proof device. The sign epsilon is locally constant and S(U,U) never zero.
The formula

    b_a=-epsilon S_ab U^b / sqrt(|S(U,U)|)

is smooth, future-raised and gives S=epsilon b tensor b. This particular
representative is auxiliary; no observer, phase scale or physical current is
selected by it. Another U gives the same future b when S=epsilon b^2 and the
square-root convention is fixed; the formula does not add physical data.
That square-root representative itself need NOT be exact or affinely geodesic.

### Differential sufficiency

Nonvanishing b and b wedge db=0 imply, by the LOCAL codimension-one Frobenius
theorem, b=f dpsi on a sufficiently small chart with f nowhere zero. Choose
psi's sign so f>0. Set q=dpsi=h b with h=1/f>0 and

    n=1/(|beta| h^2).

Then q is nonzero, exact and future-null, and beta n q q=epsilon b b=S.
Exact null q implies affinity:

    q^a nabla_a q_b=(1/2)nabla_b(q^2)=0.

The actual metric's contracted Bianchi identity gives

    (1/4)d_b R=nabla^a S_ab
             =beta {div(n q-sharp) q_b+n q^a nabla_a q_b}
             =beta div(j) q_b.                                  (RT1.2)

Condition4 and beta!=0,q!=0 force div(j)=0. No additional PDE is solved or
assumed for g, and no vacuum existence theorem is imported into this class.
The local Frobenius theorem is a mathematical method with its hypotheses
checked, not a new physical premise.

### Necessity

If(RT1.1) holds, S=epsilon b^2 with b=sqrt(|beta|n) q, hence rank one,
the stated sign and b wedge db=0. Exact-null affinity and conservation in
(RT1.2) give dR=0. Thus all four conditions follow. This proof neither
upgrades the optional relation to physics nor derives the chosen product.

## 3. ALL local decompositions at fixed g and beta

Shrink to a common submersion chart with connected phi-level fibres. Given
one solution (q=dphi,n), any other future-null exact solution of the same
nonzero tensor factorization has

    q'=a q, a>0,       n'=n/a^2.

This follows from equality of the rank-one lines and their full tensors, not
from one contraction. Exactness gives da wedge dphi=0. In a submersion chart
all derivatives of a tangent to a phi-level vanish, so a=A(phi)>0. Therefore

    phi'=F(phi)+constant, F'>0,
    n'=n/[F'(phi)]^2,       j'=j/F'(phi).                         (RT1.3)

Conversely EVERY such smooth local F yields the same full S, exact-null
affinity and a conserved j': j(phi)=0 makes div(j/F')=0. These statements
are local; disconnected fibres/global monodromy need separate treatment.
Phase origin is free unless supplied. No other local freedom in q,n remains
at fixed g,beta,orientation in this nonzero one-direction class.

For any FIXED supplied future unit observer U,

    Gamma=-g(U,j),      Gamma'=Gamma/F'(phi),
    S(U,U)=beta Gamma[-U(phi)].                                  (RT1.4)

Thus the metric determines the null line and full signed amplitude tensor,
but not the phase/density split or conserved-current/readout normalization.
Even a positive CONSTANT F'!=1 changes j when beta is fixed. This is not
G352's simultaneous affine Theta/Delta gauge, which leaves d(Theta/Delta)
and j unchanged. Arbitrary nonlinear F is likewise not that admitted gauge.
Distinct data need not be forbidden or uniquely selected to be legitimate.

If beta is ALSO varied to a nonzero constant beta' of the same sign, equality
of S instead gives n'=beta n/[beta' (F')^2], j'=beta j/[beta' F'].
Opposite signs cannot keep n,n'>0. Parameter and data freedom are separate
from physical law adoption. The degenerate beta=0 or S=0 case is not covered;
S=0 alone supplies no nonzero rank-one line to reconstruct.

## 4. Exact diagnostics and alternative shortcuts

These examples support or falsify specific algebra/implementation shortcuts;
they are not substitutes for sections2--3 or genericity evidence.

**Trace invariants do not fix the full algebraic type.** In a Minkowski frame,
take q=-dt+dz and e=dx, and T=q tensor e+e tensor q. T is symmetric and
trace-free, rank2. For B=g^-1 T, B^2=q-sharp tensor q!=0 and B^3=0.
All positive-power traces vanish, but no rank-one null factorization exists.
This is a pointwise algebraic diagnostic, not a claimed twisting/global metric.
It is Ricci-algebraically admissible: in4D the curvature tensor
K_abcd=(g_ac T_bd+g_bd T_ac-g_ad T_bc-g_bc T_ad)/2 has Ricci T.
No global development assertion is needed for this pointwise screen.

**Constant scalar/conservation cannot simply be omitted.** On r>0 let

    g=2du dr+u r^2 du^2+r^2(dx^2+dy^2).

Direct full-metric computation gives Ric=3u g+r du^2, R=12u, S=r du^2.
The null line is exact, rank one and positive. With beta=1,q=du,n=r,
J=r^2 and div(r partial_r)=3, so there is NO conserved factorization of the
required type (RT1.2 already proves impossibility for any alternative exact
phase). This actual local comparison metric is NOT an admitted vacuum metric
or failure of UDT. It only defeats dropping condition4 from this test.

**Full metric held fixed while current changes.** On a regular small patch,

    g=2du dr+dx^2+dy^2-(x^2+y^2)du^2/2

has Ric=S=du^2, R=0. Choose partial_r future and beta=1. Then q=du,n=1
and F(u)=u+u^3/3, F'=1+u^2 give another exact representation with
q'=(1+u^2)du, n'=1/(1+u^2)^2 and j'=partial_r/(1+u^2).
The full curvature and optional tensor are unchanged; current/readout differ.
G352's stronger product with ORIGINAL labels/measure is not asserted for the
second data choice. Whether and how product constraints change this freedom
is RT2, not an assumption hidden in this example.

## 5. What this establishes and does not establish

Candidate outcome: exact local conditional reconstruction criteria, full
algebraic rather than scalar-invariant screening, and an ALL-decompositions
phase function freedom within the stated class. Metric curvature supplies
more than a freely named quantity, but does not alone fix the linear carried
current. Existence does not identify any physical content or measurement.
The line-square-root b is metric/time-orientation determined on this nonzero
class; converting it to an exact phase and separately normalized density is
where residual freedom enters. It is not legitimate to call b an exact phase
without testing its differential properties or to choose F silently.

These comparison restrictions are additional to specifying ordinary data in
the admitted VACUUM equation; they are not new owner-adopted physical laws.
The result does not prove every UDT connection needs a new premise, eliminate
geometric effects carried by vacuum Weyl data, or make emergence a prerequisite.
No existence of an independent twisting null-Ricci metric was established here;
no minimality, global reconstruction, stability or physical coupling is claimed.
Fresh source-first/direct mathematical review remains required before use.
