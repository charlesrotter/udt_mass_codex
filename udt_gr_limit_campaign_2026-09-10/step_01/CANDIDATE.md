# GL1 — weighted quiet-jet leading response

INITIAL CANDIDATE / UNREVIEWED / UNPROMOTED.2026-09-10.
This is a conditional theorem for an explicitly presented response germ,
NOT a derivation of UDT response-class membership or a field law.

## 1. Question, objects and ownership

At a regular event fix a four-dimensional Lorentz vector space(V,eta),
signature(-+++), an orthonormal frame and fixed calibrated component units.
Let K be the20-dimensional algebraic curvature space. For a fixed finite
integer m>=0 use the finite-dimensional ambient space

    J = K direct_sum J1 direct_sum ... direct_sum Jm,
    Jj = (V*)^tensor(j) tensor K.

Actual inputs are the full covariant tensors Riem, nabla Riem,...,nabla^m Riem
in an orthonormal frame, expressed in the fixed units. The product space also
contains tensors not realizable as a metric jet. The present theorem assumes
a response presentation EXTENDING to a neighborhood of0 in this product.
It does NOT prove that every local finite-jet metric response admits that
extension. Differential Bianchi/commutator constraints are not discarded when
claiming anything about actual metrics; here estimates on the larger space
are merely sufficient for its realizable subset. No arbitrary jet is called
an actual metric development.

Fix a single map F:J->Sym2(V*) near0, with Lorentz-equivariant germ under the
FULL unoriented O(1,3) action. Equivariance is required whenever both arguments
are in its domain; differentiating the overlapping germs makes DF_0 equivariant.
There are no auxiliary vectors, orientation tensors, position-dependent
external coefficients or hidden history arguments. These are CONDITIONAL
typing hypotheses, not consequences asserted of Local Metric Sufficiency.
The map is held FIXED as the limit parameter changes.

Put P(X)=X-(tr_eta X/4)eta and T=P F, the trace-free response. Assume F is
Fréchet differentiable at0, not merely differentiable along individual rays.
No exact weighted homogeneity is required. No nonzero curvature derivative
coefficient is presumed. DDR, when imposed on an actual supplied response,
means T=0 by G311; identifying the physical response with this class remains
unclosed under current G312 authority.

Choose ANY fixed positive component norms on each input slot and on the
output trace-free symmetric space, and the sum norm on J. They are mathematical
controls associated with the supplied frame, not positive Lorentz-invariant
norms or a preferred physical observer. Constants are not uniform over
unbounded boosts. Coefficients/units are fixed through the limit. No numerical
length or physical value is selected. A mixed-weight physical response would
require dimensionally appropriate coefficients; this theorem does not supply,
adopt or bypass ownership of them. The parameter below controls a family of
inputs, not a new operator scale, X_max input, time variable or empirical fit.

G301's reviewed linear curvature-to-symmetric-tensor basis is reused with
its exact naturality/type hypotheses. The present novelty is a finite-jet
weighted remainder estimate WITHOUT exact response homogeneity, not another
proof that the G301 basis consists of Ricci and scalar-times-metric.

## 2. What the derivative actually permits

Lorentz equivariance implies F(0)=beta eta: the only invariant symmetric
covariant two-tensor is the metric line. Hence T(0)=0, even when beta is
not zero. No flat-quiet F(0)=0 assumption is needed for the SHAPE equation.
This observation does not make beta an adopted physical coefficient.

Let Aj be the restriction of DT_0 to slot Jj (with J0=K). G301's basis gives

    A0(K0)=a S(K0),  S(K0)=Ric(K0)-(R(K0)/4)eta.          (1)

The real constant a is fixed by F; it can be zero. There is no GR-principal
overlap assumption determining it.

The element -I belongs to the declared O(1,3) group. It acts by(-1)^j on
the rank(4+j) input Jj and by+1 on a rank-two output. Thus equivariance and
linearity give Aj((-1)^j Z)=Aj(Z), proving

    Aj=0 for every ODD j.                              (2)

No classification of the even higher-derivative maps is needed for the bound.
This proof uses the stated unoriented group; it is not an undisclosed
assertion about every differently typed response architecture.

By Fréchet differentiability define, on a sufficiently small ball,

    omega(t)=sup_{0<||J||<=t} ||T(J)-DT_0[J]||/||J||,
    omega(t)->0 as t->0+.                              (3)

This finite supremum/modulus follows directly from differentiability. The
ball is contained in the domain; no global or boost-uniform bound is assumed.
Consequently

    T(J)=a S(J0)+sum_{even j>=2} Aj Jj+N(J),
    ||N(J)||<=||J|| omega(||J||).                       (4)

The displayed expansion is derived from the declared class, not an adopted
Einstein-plus-corrections equation.

## 3. GL1-BOUND — uniform estimate on a supplied weighted regime

For0<epsilon<=epsilon0<=1 suppose a family/set of inputs satisfies

    ||Jj||<=Mj epsilon^(j+2), j=0,...,m,                (5)

with fixed finite Mj>=0. At least one Mj may be positive; if all are zero,
the zero-input conclusion is immediate. Require M epsilon0² small enough
for the domain of(3), where

    M=sum_j Mj,
    D=sum_{even 2<=j<=m} ||Aj|| Mj.                    (6)

Both constants depend on the declared fixed map/norms/order/bounds, not on
epsilon or the individual input. Since ||J||<=M epsilon² and, for even
j>=2, epsilon^(j+2)<=epsilon^4, (4) proves uniformly

    ||T(J)-a S(J0)||
      <= D epsilon^4 + M epsilon² omega(M epsilon²).   (7)

Thus the normalized response difference divided by epsilon² tends to zero.
For exact DDR inputs T(J)=0, IF a!=0,

    ||S(J0)||/epsilon²
      <= [D epsilon²+M omega(M epsilon²)]/|a| ->0.     (8)

For approximate response balance ||T(J)||<=rho(epsilon) epsilon²,
add rho(epsilon)/|a| to(8); convergence needs rho->0. This is mathematical
residual control, not an observational tolerance or a replacement for DDR.

Crucial quantifiers: the normalization is the DECLARED epsilon² scale, not
automatically ||J0||. If actual curvature decays faster, (8) alone does not
prove ||S||/||J0||->0. Such a relative claim follows only with an additional
lower bound ||J0||>=c epsilon²,c>0. No such lower bound is assumed generally.
Uniformity over a class of response maps additionally needs uniform moduli,
derivative bounds and |a|>=a_min>0; fixing F does not establish that stronger
claim. No conclusion dividing by a is available on a=0.

## 4. GL1-RATE — optional stronger regularity, explicit rate

If T is C1 near0 and

    ||DT(J)-DT(0)||<=H ||J||^alpha, 0<alpha<=1,         (9)

on a ball containing each segment[0,J], the fundamental theorem of calculus
on that segment gives

    ||N(J)||<=H/(1+alpha) ||J||^(1+alpha).

Equation(7) therefore strengthens to

    ||T(J)-aS(J0)||
      <=D epsilon^4 + H M^(1+alpha)/(1+alpha)
                                      *epsilon^(2+2alpha).  (10)

In particular, a Lipschitz derivative(alpha=1) gives the O(epsilon^4)
absolute remainder and, for fixed nonzero a and exact balance, O(epsilon²)
normalized trace-free-Ricci bound. Bare differentiability does NOT give
this polynomial rate. The stronger regularity and its constants stay optional
mathematical conditions, not supplied physical laws or empirical numbers.

## 5. Limits and no-new-scale control

The a=0 loophole is not a new discovery: G312 and ND1/ND2 already preserve
regular curvature-quadratic and scalar-only counterresponses. They remain
valid controls; DDR and locality alone do not remove them. This candidate
does not repeat their nonselection result as a new achievement.

Curvature smallness by itself does not state (5). A higher-derivative slot
can be as large as the leading curvature, or larger; then it cannot be
discarded by the estimate. Nor does a pointwise response estimate establish
existence of a balanced metric family, compactness/convergence, stability,
nonspherical global dynamics, a quiet physical scale or measured GR recovery.

If one separately imposes EXACT weighted degree-two homogeneity on T,

    T(t² J0,t³ J1,...,t^(m+2) Jm)=t² T(J),

then evaluating(4), dividing by t² and sending t->0 gives exactly
T(J)=a S(J0) wherever the dilation ray/domain hypotheses hold. This is a
consistency control extending the old homogeneity argument, not the campaign's
new physical premise or headline discovery. Dimensionally scale-free exact
classes cannot secretly retain arbitrary mixed-weight corrections. Conversely,
allowing a mathematical nonhomogeneous germ here does not license a new
physical operator scale in UDT. That constitutive question remains OPEN.

## 6. Discovery and maximum conclusion

After the question/conditional slot class was recorded, the parent combined
G301's linear basis with a weighted Taylor estimate; the -I parity argument
removes odd-derivative linear terms. The normalized-curvature versus actual-
curvature distinction and fixed-map dependence are explicit safeguards.
Candidate frozen before small CPU checks and before direct review exposure.
The fresh reviewer is reconstructing the source-first argument independently.

Maximum claim: a controlled conditional leading-response estimate, with
optional quantified rate, over the declared response-germ/jet-input class.
It does not show UDT satisfies the hypotheses, select a response or physical
scale, establish full GR dynamics, supply content, change grades/canon, or
turn the G312 unclosed join into a theorem. New results remain UNPROMOTED.
