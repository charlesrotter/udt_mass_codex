# ACI1 initial candidate — finite clock slowing and integrated curvature

UNREVIEWED candidate; no native field equation or physical adoption. Source
snapshot and exposure are frozen separately. This tests a necessary condition
for realizing the working asymptotic target in declared comparisons. It does
not establish which comparisons isolate the additional positional contribution.

## 1. Inputs and distinction from earlier work

Use one smooth time-oriented Lorentz4 metric g, signature(-+++), its Levi-Civita
connection and R(X,Y)=[nabla_X,nabla_Y]-nabla_[X,Y]. Ordinary proper clocks and
the regular free affine-null clock interface retain W4/R6/FSL1's stated grades.
Work in length units for time, c_E=1. No Einstein equation or RG completion is
used. The owner's extreme-distance asymptotic received-slowing statement is a
WORKING physical direction, not a chosen metric, population or finite distance.

R7 already bounds a clock ratio by relative transport rapidity. R8 already gives
an integral of the deformation of an auxiliary clock field. PSW's separate
holonomy check gives a local curvature-area expansion. The proposed increment
is a finite, full4D bound directly on curvature, with explicit preparation and
acceleration contributions and without truncating to small loops or a commuting
boost sector. Standard transport-variation methods are mathematical tools;
this is not a claim of literature novelty or a new law of light.

## 2. Relative transport gives the clock bound

Let gamma run from emission p to reception q on the actual affine null branch,
and let u in T_p and v in T_q be the future unit endpoint clocks. For every
piecewise smooth path alpha from p to q write P_alpha for metric parallel
transport. Normalize the ray so k_p=u+n with n unit spatial. R6 gives

    Z = omega_e/omega_o = 1/[-g(k_p,P_gamma^-1 v)].

For future unit vectors a,b at a point define the hyperbolic distance
rho(a,b)=arcosh[-g(a,b)]. Decompose P_gamma^-1 v=cosh(rho)u+sinh(rho)m.
Since |g(n,m)|<=1, the positive denominator lies in[e^-rho,e^rho]. Thus

    |log Z| <= rho(u,P_gamma^-1 v).                         (1)

This is the existing R7 estimate, written without endpoint spatial tetrads.
No lower bound on redshift follows from large rapidity: direction still matters.

Choose a declared comparison path beta from p to q and put

    B = rho(P_beta u,v),
    H = P_gamma^-1 P_beta.

Metric transport acts isometrically on the unit future hyperboloid. Its triangle
inequality gives rho(u,P_gamma^-1 v)<=rho(u,H u)+B. The split uses specified
paths/preparation, not a decomposition of the spacetime metric or of UDT physics.

## 3. Full4D curvature bound from an actual fixed-endpoint sweep

Suppose gamma and beta admit a C2 fixed-endpoint homotopy F(s,t),0<=s,t<=1,
with F(0,t)=gamma(t), F(1,t)=beta(t), F(s,0)=p, F(s,1)=q. Piecewise smooth
paths and sweeps are allowed with matching differentiable pieces and additive
integrals; no causal character is assigned to the mathematical sweep. It is
not a physical observer population or a spacetime foliation. No existence is
asserted for arbitrary global pairs of paths.

Write T=F_t,S=F_s, P_s(t):T_p->T_F(s,t) for transport along t, and
U(s,t)=P_s(t)u. Define the nonnegative integrated curvature quantity

    C[F,u] = integral_0^1 integral_0^1
       sqrt(g(R(T,S)U,R(T,S)U)) dt ds.                    (2)

Metricity makes R(T,S) skew-adjoint for g, so R(T,S)U is spatial relative to U
and the square root is real. This is the positive spatial norm, not an
indefinite matrix norm or the scalar curvature. It is invariant under coordinate
or tetrad changes with the same g,u,F. Different sweeps and physical initial
clocks can give different values; there is no preferred universal frame.

Here is the direct variation derivation. For any fixed w in T_p set W=P_s(t)w.
Since nabla_T W=0 and[partial_t,partial_s]=0,

    nabla_T nabla_S W = R(T,S)W.

After transport back to p and integration in t, the fixed initial endpoint
and fixed initial vector make the initial derivative zero. At the fixed final
endpoint q this gives

    A_s := P_s(1)^-1 partial_s P_s(1)
         = integral_0^1 P_s(t)^-1 R(T,S)P_s(t) dt.         (3)

Let H_s=P_0(1)^-1 P_s(1), so H_0=I, H_1=H and H_s'=H_s A_s. The curve
h_s=H_s u lies on the future unit hyperboloid. Its Riemannian speed is

    |h_s'| = sqrt(g(A_s u,A_s u))
            <= integral_0^1 sqrt(g(R(T,S)U,R(T,S)U)) dt.

The inequality is the ordinary triangle inequality in the positive-definite
space u-perp after transport back to p. Integrating the curve length bounds
its endpoint distance. With (1),

    rho(u,H u) <= C[F,u],
    |log Z| <= B + C[F,u].                               (4)

The full noncommuting Lorentz transport is retained. No positive Ad-invariant
norm on the noncompact Lorentz algebra, path-independent scalar depth or
two-dimensional reduction has been invoked. Equation(3) uses transported
curvature, so cancellations may make(4) strict.

## 4. Preparation and acceleration can be controlled separately

For a concrete query, let beta be an initial preparation curve c:p->b0 followed
by the actual receiving clock worldline b(tau):b0->q. Let its initial unit
velocity be v0 and define rho0=rho(P_c u,v0). Along b, pull its unit velocity
back into T_b0 by parallel transport. Its hyperbolic speed equals the ordinary
proper acceleration magnitude |a|=sqrt(g(nabla_v v,nabla_v v)). Therefore

    B <= rho0 + integral_b |a| d tau,
    |log Z| <= rho0 + integral_b |a| d tau + C[F,u].       (5)

For a free receiver prepared by parallel transport along c, rho0=0 and a=0.
For bounded initial mismatch and accumulated acceleration they contribute a
uniform finite allowance. Bounded acceleration magnitude alone is insufficient
over an unbounded proper-time interval. Each case is a stated comparison
protocol, not a claim that every physical observer is so prepared. An emission
at a different event uses its own actual u and initial-data correspondence.

## 5. What can be bounded from geometry before evaluating Z

Define the positive metric j_U=g+2 U-flat tensor U-flat on each tangent space
of the sweep. The linear map on bivectors is

    L_U(X wedge Y)=R(X,Y)U.

Let K_U be its operator norm, using the j_U-induced bivector norm on the input
and the positive spatial norm on the output. Then

    C[F,u] <= integral K_U |T wedge S|_(j_U) dt ds
            <= K_max A_j(F)                              (6)

whenever a finite K_max bounds it. The area integral counts the parametrized
sweep with multiplicity, not the area of its image-union. Null or rank-deficient
pieces cause no indefinite-area problem because j_U is positive definite.
K_U and A_j are tied to the explicitly transported u and the chosen sweep.
Neither a bound on scalar curvature nor a bound in an unrelated frame is a
substitute. Their values can be calculated/estimated from g,F and transport
without substituting the observed Z as their definition. They may be expensive
to bound, and this theorem does not supply a uniform bound for free.

For a family realizing Z->infinity, if rho0+integral|a| stays uniformly bounded,
then(5) forces C[F,u]->infinity for EVERY sequence of admissible sweeps, whenever
such sweeps exist for each comparison. In particular, a family admitting
uniformly bounded K_max and A_j cannot realize that asymptote. Large C on one
poorly chosen sweep is not evidence of redshift; an unnecessarily winding sweep
can be replaced when a smaller one exists. The infimum over a nonempty allowed
sweep set also obeys(4); an empty set is a domain failure, not infinite curvature.

This is a necessary geometric restriction relative to a specified realization
of the working target and bounded kinematics. It does not force pointwise
curvature blowup, a preferred curvature sign, conformal completion, a selected
distance or a physical X_max. Failure of the sweep hypotheses is reported as
failure of this test's domain, not a chosen topological explanation.

## 6. Exact analytic controls and adverse distinctions

### Flat inertial motion

For g=-dt^2+dx^2+dy^2+dz^2, source x=0 and receiver x=L+vt, actual arrival
t_o=(s+L)/(1-v) gives Z=1/[gamma_v(1-v)]=exp(rho0), v=tanh(rho0).
Curvature vanishes and every contractible sweep has C=0. Initial mismatch
alone saturates the bound. Allowing rho0->infinity would invalidate an inference
of unbounded curvature from received slowing.

### Flat constant proper acceleration

From rest at x=L, let t=sinh(a tau)/a and
x=L+(cosh(a tau)-1)/a, a>0. The outgoing intersection with t-x=s has
tau=-log[1-a(L+s)]/a on its future reception domain. Hence
Z=1/[1-a(L+s)] and log Z=a tau=integral|a|d tau, with rho0=0 and C=0.
As reception proper time tends to infinity the accumulated acceleration, not
the bounded instantaneous acceleration, supplies the unbounded clock ratio.

### Regular curved geometry with zero scalar curvature

Consider the supplied Lorentz4 product, H>0,

    g_H=-dt^2+exp(2Ht)dx^2+dy^2+exp(2Hy)dz^2.             (7)

It is an exact control, not an admitted UDT cosmology or adopted Hubble model.
The(t,x) factor has curvature H^2 and the(y,z) factor curvature -H^2, so
R_scalar=0, Ric_ab Ric^ab=4H^4 and R_abcd R^abcd=8H^4. Local curvature stays
regular. The parent control program will independently compute these from the
original metric connection rather than merely repeat the product assertion.

Source x=y=z=0 and receiver x=L,y=z=0 have unit free velocity partial_t.
Emission at t=s obeys exp(-Hs)-exp(-Ht_o)=HL. At s=0, for0<HL<1,

    t_o=-log(1-HL)/H,   Z=exp(Ht_o)=1/(1-HL).

The initial curve c is the t=0 x-segment, explicitly not a geodesic
parallel-preparation rule. Parallel transport along it gives initial mismatch
rho0=HL; the receiver is free. In the Lorentz2 plane theta0=dt,
theta1=exp(Ht)dx and varpi=H exp(Ht)dx. The bounded triangle between c,
the receiver and the null leg has integrated curvature

    C = integral_0^t_o integral_( (1-exp(-Ht))/H )^L
            H^2 exp(Ht) dx dt
      = Ht_o-HL.

The planar boost direction has fixed sign and the bound saturates:
log Z=rho0+C. As L tends to1/H, the initial mismatch stays below1 and all
local curvature scalars stay fixed, while t_o and C diverge. The asymptote is
not a local singularity. The initial separation at t=0 is L; identifying it
with a selected physical cosmic distance or X_max would add information.

CCW's RG condition requires positive limiting scalar curvature. Since this
control's scalar is identically zero, its observed asymptote cannot establish
that RG endpoint. This is a supplied geometric control of a mathematical
implication, not a countermodel admitted by all UDT postulates or an alternative
physical law. It also defeats replacing the transported curvature norm in(6)
by the scalar curvature alone.

### No converse and no sign selection

Reversing a nontrivial path deformation and repeating it can increase the
absolute integral C without changing its final paths or holonomy. Thus a large
chosen C does not prove a large clock shift. Even large actual relative
rapidity does not force redshift in all directions, by R7's exact expression.
The norm bound loses orientation and cannot select a positive positional law.

## 7. Physical return and maximum claim

If the working UDT asymptote is realized by a family in the declared domain
with bounded preparation and accumulated acceleration, it cannot arise in a
uniformly controlled curvature/sweep family. This is a necessary global
comparison constraint, obtained without RG, Einstein dynamics, a fitted profile
or assigning DDR's response. It narrows admissible realizations of that target.

It does not identify total redshift with the additional positional contribution,
prove that nature uses this comparison preparation, determine the dependence
on operational distance, or select a metric family. If the physical target is
assigned elsewhere, this conditional exclusion says nothing about that case.
The mathematical proof would hold for the same metric/query in ordinary Lorentz
geometry; UDT's role is the existing physical requirement a candidate realization
must meet. No statement that all UDT postulates are insufficient follows.

This result would be more than assuming the RG endpoint and checking its
consequences: it tests any metric/comparison family in its domain by a finite
curvature bound. Its physical-selection gain is nevertheless limited to that
necessary condition. It supplies no native selector or automatic successor.

## Discovery exposure before this freeze

The parent developed the transport/curvature argument in analysis but had not
frozen a file when /root/aci_math sent an unsolicited pre-seal outline of the
same hyperboloid-speed route. The parent read that message and its correction.
Therefore this candidate is NOT claimed frozen before all reviewer argument
exposure, and parent discovery is NOT independent of that outline. The full
source-first reports and sibling arguments remain unread at this freeze.
The reviewer had not seen a parent or sibling candidate. Record this departure
from the intended exposure order rather than inventing retrospective blindness.
