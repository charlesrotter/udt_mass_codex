# GRS1 initial candidate — reciprocal balance versus response selection

UNPROMOTED conditional mathematics and explicitly unadopted comparisons.
This initial candidate is retained for review history; final verdict and limits
will belong to REVIEWED_RESULT.md. Baseline and source versions: LAUNCH.json.
No new UDT premise, action, source, scale, field equation or canon is adopted.

## 1. Ownership before calculation

The founding interpretation is preserved: observed c_E is the clock/ruler
calibration of positional-dilation geometry, including causal cones. It does not
by itself specify a functional derivative or a response's scaling weight.
G176's determinant-one calibrated pair is a two-dimensional pair statement;
it is not a fixed four-volume condition on arbitrary spacetime variations.

Current G312 authority is the 2026-09-09 AUTHORITY_RECORD, not the stronger
historical GR-principal overlap. DDR and Local Metric Sufficiency are
OWNER_ADOPTED_PROVISIONAL_POSTULATE, not derived/canon. The latter supplies
finite local metric-jet dependence without a separate hidden history label;
it does not establish the full response architecture below. GR is FILTER ONLY.

On the regular full all-pair domain with the specified symmetric covariant
response E, the reviewed G310 algebra gives

    <E,H(u,n)>_g=0 for every orthonormal pair  <=>  TF_g(E)=0.
    TF_g(E)_ab = E_ab - (tr_g E)/4 g_ab.

The pair tangents span the nine trace-free symmetric directions. This identifies
the balance test, not E itself. Raising the indices of H to use inverse-metric
variations changes an overall sign, which does not change stationarity.

## 2. Action route: exactly where an equation is chosen

All actions in this section are UNADOPTED COMPARISON FUNCTIONALS. Let
S_f[g]=integral sqrt(-g) f(R) d^4x, with Levi-Civita curvature and compactly
supported inverse-metric variation h^{ab}=delta g^{ab}. Then

    delta sqrt(-g) = -1/2 sqrt(-g) g_ab h^{ab},
    delta R = Ric_ab h^{ab} + g_ab box h^{ab} - nabla_a nabla_b h^{ab}.

In the second line metric compatibility allows the box term to be written
box(g_ab h^{ab}); the double divergence is understood with the displayed
contracted indices. Twice integrating by parts transfers derivatives to f'(R):

    delta S_f = integral sqrt(-g) E^f_ab h^{ab} d^4x,
    E^f_ab = f'(R) Ric_ab - (1/2)f(R)g_ab
             + (g_ab box - nabla_a nabla_b) f'(R).

There is no physical boundary contribution in this local compact-support test;
this is not a prescription for UDT boundaries or X_max. Arbitrary stationarity
gives E^f=0. Stationarity against all trace-free shape variations instead gives
TF(E^f)=0. G310 explains why testing all reciprocal planes gives this same
algebraic condition if E is this variational derivative; it does not identify E
as a variational derivative in the first place.

For f(R)=R-2 Lambda, E^f=G+Lambda g. Thus unrestricted stationarity yields the
usual vacuum Einstein equation with the chosen constant. Trace-free stationarity
discards that explicit trace term and gives Ric-(R/4)g=0; Bianchi makes R constant
on a connected regular solution. Its constant is not selected by this test.
Matter coupling and its normalization would be additional choices, absent here.

For f(R)=R^2,

    E^2_ab = 2R Ric_ab - (1/2)R^2 g_ab
             + 2(g_ab box R - nabla_a nabla_b R),
    tr_g E^2 = 6 box R.

Both actions permit exactly the same reciprocal-variation test, applied to
different responses. A concrete distinction is the smooth local metric

    g = -dt^2 + t(dx^2+dy^2+dz^2),  t>0.
    Ric_00 = 3/(4t^2),  Ric_ii=1/(4t),  R=0.

Here E^2=0 identically, whereas TF(Ric)=Ric is nonzero. In particular the
orthonormal pair u=partial_t, n=t^(-1/2)partial_x gives <Ric,H>=2/t^2 !=0.
Thus reciprocal stationarity plus locality/covariance does not uniquely select
the Einstein response or its trace-free equation in this broad action arena.

Limits of the witness matter: E^2 is generally fourth order, has metric homothety
weight -2, and lacks the full Einstein spin-two principal response at flat space.
It is outside the full G301 arena. It is not a model satisfying all UDT premises,
not an admitted UDT cosmology, and not claimed to pass the current empirical GR
filter (whose full implementation is not supplied here). Its vanishing at R=0
is deliberately a degeneracy witness. No viability, source, causal-evolution or
stability assertion follows. The nonconstant-R control prevents this degeneracy
from concealing a wrong derivative term in our calculation.

## 3. A conditional route that does not begin with an action or jet order two

Consider the following mathematical arena, not an adoption packet:

* E is a symmetric covariant rank-two, metric-only natural differential operator
  of finite order r, equivariant under local diffeomorphisms and unoriented
  orthonormal changes of frame, with no additional background fields/data.
* In normal metric jets at a fixed Lorentz metric value, E is continuously
  differentiable at the flat jet. Its domain includes the flattening rays used
  below. These requirements exclude singular curvature-ratio constructions.
* E has exact constant-homothety weight zero: E[lambda^2 g]=E[g], lambda>0,
  wherever used. This is a condition on the typed response, not merely on its
  zero set, and not merely a change of coordinates.

At a point use normal coordinates with g(0)=eta, first derivatives zero, and
normal derivative tensors J_2,...,J_r. Put D_s(x)=s x and
g_s=s^(-2) D_s^*g. In these coordinates g_s(x)=g(sx), hence

    J_k[g_s]=s^k J_k[g],
    E[g_s](0)=s^2 E[g](0).

The second equality uses weight zero and the two covariant output indices under
pullback. Write E(0)=F(J_2,...,J_r). It follows that

    F(s^2 J_2,s^3 J_3,...,s^r J_r)=s^2 F(J_2,...,J_r).

At the zero jet this also gives F(0)=0. Differentiability there gives

    s^2 F(J) = D F_0(s^2 J_2,s^3 J_3,...,s^r J_r) + o(s^2).

Divide by s^2 and take s down to zero on a fixed jet ray. Terms of order k>2
vanish. Thus F(J)=D_2 F_0(J_2) exactly, not just to leading order. No finite
truncation or small-curvature approximation has been made. For r<2 the result
is zero. The argument requires the whole flattening ray and its regular endpoint;
it does not extrapolate from a derivative at one nonflat physical metric.

The second normal metric jet is linearly equivalent to algebraic Riemann
curvature. The Lorentz-equivariant linear contraction classification used in
G301 then leaves just Ric_ab and R g_ab. Therefore, in this arena,

    E_ab = a Ric_ab + b R g_ab,  with constant a,b.

This uses the reviewed G301 invariant-basis argument as attributed mathematics;
we are not claiming to repeat its entire exact rank certificate. It is also a
special case of the standard natural-tensor classification (Navarro/Sancho,
Theorem5.1; see REFERENCES.md). The explicit flattening argument here makes the
load-bearing smoothness and homothety hypotheses visible. This is a conditional
alternative way to obtain the algebraic response class, not a proof of every
G301 principal/causal gate or of native UDT membership.

If additionally a!=0, the existing DDR balance becomes

    TF(E)=a(Ric-(R/4)g)=0,
    nabla^a(Ric_ab-(R/4)g_ab)=(1/4)partial_b R,
    Ric=Lambda g,  Lambda constant on each connected regular solution.

Neither an action nor the off-shell identity div E=0 is needed for this last
conditional trace-free result. If one separately requires div E=0 identically
for every metric, then (a/2+b)dR=0 forces b=-a/2, selecting a multiple of the
Einstein tensor within this class. That conservation identity is additional to
DDR. Pure-trace a=0 gives automatic balance for every metric and no shape law.

## 4. Why the hypotheses cannot be hidden in familiar words

Finite locality is already owner-provisional. Exact response type, its full
naturality/flat regularity, weight zero and nonzero Ricci coefficient have not
been established by this campaign from current UDT premises. This list is an
audit of this route, not a theorem that every possible derivation must adopt
these as independent new physical premises.

General covariance is not homothety weight zero. Absence of an explicit length
constant does not choose that weight: integral sqrt(-g) R^2 is scale invariant
in four dimensions but its covariant Euler response has weight -2. EH's action
has weight +2 while its response has weight zero. A fixed Lambda g term has
weight +2 and is excluded from the exact homogeneous weight-zero arena, although
DDR is blind to it and may leave an integration constant in its solutions.

Constant rescaling of a mathematical metric, changing numerical units with all
dimensional quantities transformed, and identifying rescaled geometries as a
physical symmetry are different claims. No physical scale symmetry, Weyl gauge
freedom or strong common-scale neutrality is adopted here. Measured c_E and
G_obs remain anchors. The source paper's dimensional argument for stress-energy
cannot become a UDT source/response identification by analogy.

Likewise an equation's zero set may be unchanged on a domain after multiplication
by a nonvanishing natural scalar while the response's weight changes. Without
a physically owned normalization, choosing a convenient representative is not
identifying the full response. Singular or vanishing multipliers can also change
regularity or add solutions. The witness above explicitly exposes that issue.

## 5. Bounded landing

There is a concrete conditional derivation here: a smooth natural finite-jet
weight-zero response collapses to curvature order two, and DDR with nonzero
shape sensitivity gives the trace-free Einstein vacuum equation. Derivative
order two need not be an independent starting assumption in this mathematical
route. Native ownership of the route's other hypotheses remains OPEN.

Reciprocity alone does not choose an action. GR specifies a response through
its action or through additional typed geometric/conservation assumptions;
using either requires exposing those choices. The positional-dilation premise
is retained front and center, but no new response term or sourced extension
follows from the completed derivation. No fitted profile or familiar equation
is imported to fill that open identification. This is not an impossibility
theorem for UDT or a demand for a new premise.
