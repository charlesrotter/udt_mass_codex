# ND2 — exact tangent constraints behind a vacuous linear test

Status: INITIAL CANDIDATE / UNREVIEWED / UNPROMOTED, 2026-09-09.
Conditional dependency: reviewed UNPROMOTED ND1, in full at its exact source/
candidate/review hashes. This does not bank that dependency or adopt Q, S,
angular cancellation, GR dynamics or a physical superposition principle.

## Question and assumptions

G312 already establishes that the quadratic response has zero first variation
at flat curvature. The new question is which infinitesimal deformations of
a common Ricci-flat background actually integrate to exact solutions, rather
than merely passing that known degenerate first-order test.

Definitions from G312/ND1: M=g^-1 Ric, S=g[M-(tr M/4)I], and
Q=g[M²-(tr(M²)/4)I]. The corresponding all-pair response balances are S=0
and Q=0. Q is the existing UNADOPTED curvature-weight-two counterresponse,
not a full G301 response. Current G312 authority controls historical wording.

For the exact profile classification, fix a compact interval K=[r_-,r_+]
with 0<r_-<r_+<infinity. Profiles belong to X=C2(K); equations hold on its
interior. Choose supplied b0 with f0=1+b0/r strictly positive on K. Continuity
gives a positive lower bound. This is a local comparison window and function-
space norm, not a reflecting/material boundary or selected physical size.
The complete metric is the SAME one-function 4D spherical metric as ND1.
Dimensionful profile coefficients carry their appropriate units; no operator
length, preferred scale, source interpretation or physical initial population
is introduced by choosing data or units.

A realizable velocity means h=d f_epsilon/d epsilon at zero for a two-sided
C1 map epsilon -> f_epsilon in X, with f_epsilon>0 and the specified exact
response equation holding for every sufficiently small epsilon. No time
evolution or dynamical stability is meant by this parameter.

## ND2-NECESSARY — general quadratic leading-order obstruction

This paragraph has a wider but NECESSITY-ONLY scope. Let g_epsilon be a C1
curve in the local C2 metric topology, all nondegenerate Lorentzian near
epsilon=0, with Ric(g0)=0 and Q(g_epsilon)=0. Use the supplied identification
of the local manifolds/charts. The Ricci map is differentiable at this
regular metric, so for N=dM_epsilon/d epsilon at zero,

    M_epsilon = epsilon N + o(epsilon),
    g_epsilon^-1 Q(g_epsilon)
      = epsilon² [N²-(tr(N²)/4)I] + o(epsilon²).

Divide the exact zero equation by epsilon² and take the limit. Necessarily

    N²-(tr(N²)/4)I = 0.

Only C1 parameter regularity is needed; there is no assertion of a second
parameter derivative. The ordinary first variation DQ at a Ricci-flat
background is zero, so it misses this constraint. Higher-order corrections
to a curve with this same velocity cannot cancel a nonzero leading tensor.

This is tensorial algebra for a specified Q. It is NOT sufficient for an
arbitrary N to be a metric variation, an integrable solution or a lawful UDT
development. No general Lorentz-self-adjoint classification, positivity
argument, causal/PDE assertion or nonzero-curvature principal condition is
inferred. Ricci-flat need not mean the full Riemann curvature vanishes.

## ND2-TANGENT — exact realizable velocities in the supplied profile class

Define the two finite-dimensional linear subspaces of X

    V_E = span{r², r^-1},
    V_Z = span{r^-1, r^-2}.

Claim: the set of realizable Q-solution velocities at f0 is exactly

    T_Q(f0) = V_E union V_Z,

while T_S(f0)=V_E. In particular T_Q is not a linear vector space.

Proof. By the reviewed connected-interval ND1 classification, each positive
exact Q profile on K is in (f0+V_E) union (f0+V_Z); continuity extends its
interior formula to endpoints. Thus for every epsilon!=0 the difference
quotient (f_epsilon-f0)/epsilon lies in V_E union V_Z. Finite-dimensional
subspaces are closed in X, and a finite union of closed sets is closed.
The C1 limit h therefore belongs to that union. This handles curves which
change branches as epsilon changes, including infinitely many changes;
branch choice is not assumed continuous in advance.

Conversely, for any h in either subspace, f_epsilon=f0+epsilon h lies in
the corresponding exact family. If h!=0, choose |epsilon| < m/(2||h||_infty),
where m=min_K f0>0. Positivity is then retained; h=0 is immediate. This
constructs a two-sided smooth exact curve with velocity h. The S statement
is the same argument on its one affine plane, already supplied by G260/ND1.

The common direction is span{r^-1}. Nothing here restricts the supplied b0
or selects a sign/value of the family constants. Exhaustion comes from the
reviewed analytic classification and this closed-set argument, not samples.

## ND2-OBSTRUCTION — individually integrable directions need not add

Take nonzero supplied constants alpha and delta with appropriate units and

    h_E=alpha r²,      h_Z=delta/r²,      h_*=h_E+h_Z.

Each summand is an exact Q-solution velocity, but their sum belongs to
neither plane, so no C1 curve of exact Q solutions has velocity h_*.
There is also a direct leading-order check, independent of the closed-set
argument. On any profile f0+epsilon h, the mixed Ricci blocks are exactly
epsilon A_h, epsilon B_h, with

    A_h=-h''/2-h'/r,      B_h=-h/r²-h'/r.

For h_*, A_h=-3alpha-delta/r⁴ and B_h=-3alpha+delta/r⁴. Therefore exactly

    g_epsilon^-1 Q(g_epsilon)
      = (6 alpha delta epsilon²/r⁴) diag(1,1,-1,-1).

It is nonzero for epsilon!=0. For any other C1 curve with the same velocity,
ND2-NECESSARY has the same nonzero leading coefficient, so higher-order
profile corrections cannot repair it. The exact quadratic formula above
is for the MIXED tensor; the covariant tensor also contains the varying g.

This demonstrates a false inference from a vacuous linearized residual,
not a failure of a physical superposition postulate or a verdict against UDT.
Q is an explicitly optional comparison, and the curve parameter is not time.

## ND2-FILTER — a constraint without response-law selection

The geometric angular sum is C_ang[f]=r² f''/2-f+1. At f0 its first
variation is Lh=r²h''/2-h. The Euler equation gives ker L=V_E.
On V_Z, h=beta/r+delta/r² has Lh=2delta/r². Consequently

    T_Q(f0) intersect ker L = V_E = T_S(f0).

More strongly, the exact Q AND C_ang=0 solution set is f0+V_E wherever
positive, so the same statement holds for actual filtered-curve velocities.
The first linearization of Q ALONE admits every h in X, but its exact
solution velocities form only the union above. Within this profile class,
S's ordinary linearized zero set is V_E and is integrable by the straight
families; this is not a general linearization-stability theorem.

The angular readout can distinguish the extra Z direction if that direction
is allowed in the comparison. If cancellation is imposed throughout the
comparison class, S and Q still have the SAME filtered solution metrics
and velocities. Thus the chosen filter has real discriminatory effect on
metrics without choosing the response formula. No spacetime principal-symbol
test, propagation measurement, empirical tolerance or universal quiet-law
adoption has been smuggled into this static argument.

## Scope, discovery and review ceiling

ND1's common-background ambiguity motivated this question AFTER its separate
review completed. Parent explored the tangent/leading-order argument and then
froze this candidate before CPU checks. A new reviewer begins source-first
with definitions and ND1 dependency, before this proof and outputs are supplied.
Finite exact checks will support the algebra; they cannot prove function-space
closure, general metric sufficiency or the absence of every alternate route.

New candidate contribution is the exact realizable-velocity union, nonlinear
sum obstruction and filter intersection in this fixed class, plus the stated
general necessity-only expansion. G312's zero flat first variation and ND1's
exact solution classification are dependencies, not rediscoveries.

No Q law adoption, physical source/content, stability, cosmological prediction,
native response-class closure, required-new-premise conclusion or banking.
The actual full verifier remains failed at G325. Entire original assumptions
and fresh review must accompany any conditional downstream use.
