# GRL1 initial synthesis and two analytic tests

UNREVIEWED candidate, frozen after three sealed research reports and before
reading either new reviewer's source-first argument. This is a literature-led
connection audit, not a newly selected physical theory. Existing UDT meanings
are retained. Ten substantive primary papers were inspected across the lanes;
one additional mistaken clock-paper identifier was opened as title metadata and
discarded. The finite review is not a census of all GR or a novelty theorem.

## 1. What the sources actually supply

The three lane reports and SOURCES ledgers own exact versions, inspected
sections, local pins and access omissions. EPS's smooth operational axioms
recover conformal/projective/Weyl structure and, with a further clock condition,
local metric structure. Matveev–Scholz prove the stated light-cone compatibility
step, not Weyl integrability by itself. Avalos–Dahia–Romero's standard-clock
definition and no-second-clock-effect argument retain their local/global
hypotheses. In the admitted R6/R7 Levi-Civita metric interface, norm preservation
is already present. It is not path-independent Lorentz transport or equality
of accumulated readings of clocks that reunite. This route does not fix curvature.

Clock-compass papers infer curvature from sufficiently rich, known local
positions, velocities and reference-frame motion. Their Fermi-coordinate rate
quotients must be converted to the actual null-arrival protocol before use as
UDT received ticking. PSW/J1 and CMF/CBR already separate ideal curvature
reconstruction from physical response identification. For the exact PSW
preparation, Jacobi deviation gives A_J=-T(n,n), hence

    lim 2 log p_L/L^2 = lim 2 log q_L/(3L^2) = A_J.

This is the existing leading-order theorem's shared-metric consistency, not a
new finite equality or curvature sign law. The source's remainder/protocol
hypotheses survive. Reconstructing Ricci does not prove that DDR balances it.

Joint cosmography can infer additional combinations of kinematics and curvature
from specified observer/source records. It requires its congruence, frame,
regularity and local-series conditions. Where luminosity distance is used,
photon/energy-flux identifications are further assumptions; R13/R14 do not
supply them automatically. Angular-area geometry is retained separately.
Heinesen–Korzyński2406.06167v1 §VII corrects older spatial-Ricci/vorticity signs;
its (26)/IX retain an apparent internal quadrupole tension. We quarantine that
quadrupole and do not claim to resolve the external paper. No current UDT
formula is declared wrong on that basis. T2 below is reconstructed directly.

These methods can restrict candidate metrics when independent physical records
or a justified physical condition are supplied. Generating every record from
one arbitrary metric and checking agreement verifies representation consistency;
it does not explain why that metric is physically selected.

## 2. T1 — exact operational agreement determines the scale field

On an identified connected regular domain, let g0 and g be smooth Lorentz4
metrics with the same null cones, same time/sign convention and the same
unparameterized timelike geodesics in every timelike direction. Cone equality
implies g=exp(2f)g0. One direct algebraic proof chooses a g0-orthonormal basis:
g(1,n;1,n)=0 for every unit n makes the mixed time-space entries vanish and
the spatial quadratic form a multiple of the identity. Lorentz signature fixes
the positive multiplier. Smoothness gives smooth f.

The conformal connection difference is

    C(X,Y)=X(f)Y+Y(f)X-g0(X,Y)grad0 f.

For an affinely g0-geodesic tangent v, equality of its unparameterized path
requires C(v,v) parallel to v. Since v is timelike, this forces grad0 f parallel
to v. It holds for every timelike direction, so grad0 f=0. Thus g=C0^2 g0 with
one positive constant C0 on the connected domain. A shared absolute proper-time
calibration fixes C0; constancy alone already suffices for the next statement.

For identical endpoint curves, matched events and the same regular null
correspondence, both proper intervals scale by C0. Therefore Z_g=Z_g0. An
additional matched clock ratio cannot coexist with exact agreement of all
these light-cone and free-fall data. No Einstein equation has entered.

**The all-direction clause is essential.** In coordinates (eta,x,y,z), take

    g0=-deta^2+dx^2+dy^2+dz^2,
    g=exp(2H eta)g0, H>0.

They share null cones and unparameterized null paths. Coordinate-rest curves
are unparameterized timelike geodesics of both metrics; their normalized
g-velocity is exp(-H eta)partial_eta and has zero proper acceleration.
For rest emitter x=0 and receiver x=L>0, the actual outgoing incidence is
eta_o=eta_e+L. Proper rates are1 for g0 and exp(H eta) for g, giving

    Z_g0=1,                  Z_g=exp(HL).

There is no violation of the rigidity result. For v=partial_eta+b partial_x,
0<|b|<1, the connection difference gives
C(v,v)=H(1+b^2)partial_eta+2Hb partial_x, which is not parallel to v.
Thus a single free-clock congruence cannot replace all free-fall directions.
The clocks are query data; no parallel-preparation identity between metrics,
native UDT admission, physical distance law or X_max is claimed.

**Physical implication test.** W4 assigns one geometry to its own light and
free-fall readouts. It does not assert that all those readouts equal those of
a reference GR metric. GR FILTER ONLY supplies restricted empirical recovery,
not exact complete global agreement. Consequently T1 is a useful rigidity
guard, but its reference-matching premise is not the missing UDT assignment.
It does not forbid tiny deviations outside or within finite experimental errors,
nor does it identify where or how any allowed additional effect appears.

## 3. T2 — local drift separates tides from changing line of sight

Take a smooth unit geodesic congruence U in a normal tube, an observer integral
curve, and a parallel nonrotating orthonormal spatial frame along it. No
curvature equation is assumed. All source clocks are other integral curves.
At an observer event define

    B_ij=g(nabla_(e_j)U,e_i)=H delta_ij+sigma_ij+W_ij,
    H=tr B/3,       sigma^T=sigma, tr sigma=0,       W^T=-W,
    T_ij=g(R(e_j,U)U,e_i),       tr T=Ric(U,U).

Here W is the spatial antisymmetric velocity gradient (its squared norm equals
the usual vorticity norm regardless of index sign convention). Distinct sources
approach the observer on its Fermi simultaneity slice with separation rn,
|n|=1. When differentiating one source's observed z, keep that actual source
worldline fixed; do not reset its preparation at each tick. Use the unique
regular short null branch and ordinary proper clocks. Dots mean reception
proper-time derivatives. Set P_n=I-nn^T.

The direct local relation is

    z = r n.Bn + O(r^2),
    dot z = r[-T(n,n)+|P_n Bn|^2] + O(r^2).              (T2)

To see the terms, Fermi coordinates give source position X=rn and velocity
V=BX+O(r^2). Both clocks are geodesic, so relative coordinate acceleration is
-TX+O(r^2). The lapse/clock-rate corrections are quadratic; the light-flight
curvature correction is cubic. The leading received shift is therefore the
radial relative velocity n.V. Its derivative is n.A+|P_n V|^2/r: one tidal
acceleration term and one changing-direction term. Retardation changes X and V
only at the orders already placed in the remainders. On the scaled normal-tube
family with r tending to zero, smooth geodesic dependence and regular incidence
give C1 control in reception time. Thus differentiating the remainder is
justified locally for this fixed smooth congruence; no finite-r numerical error
constant, survey convergence radius or global extension is asserted.

Define J(n)=lim_(r->0) dot z/r. With the exact uniform rest-sphere average,

    <n_i n_j>=delta_ij/3,
    <n_i n_j n_k n_l>=(delta_ij delta_kl+delta_ik delta_jl
                       +delta_il delta_jk)/15,
    <|P_n Bn|^2>=sigma_ij sigma_ij/5+W_ij W_ij/3.

The last line follows by subtracting <(n.Bn)^2> from <|Bn|^2>;
the isotropic H part cancels and n.Wn=0. Hence the corrected scalar is

    M=<J>-sigma^2/5-W^2/3 = -Ric(U,U)/3.                (T2M)

Where H(n)=n.Bn is nonzero, the redshift-coordinate slope
s(n)=lim_(z->0) dot z/z obeys J(n)=H(n)s(n). This is the carefully scoped
monopole connection from the joint-drift literature. Our r-coordinate form
does not require division by a vanishing H(n). Its Fermi distance is declared
query data, not automatically a measured luminosity or cosmic distance.
The average of the product is not the product of separately averaged data.

**Independent original-incidence flat control.** In Minkowski space take
X(t,q)=q+tBq with B=diag(2h,h,h), h>0, and observer q=0. The source lines are
inertial; restrict to a small tube with |Bq|<1 and det(I+tB)>0. For a source
seen at reception (0,0) from emission (t_e,X_e)=(-r,rn), let
q=(I-rB)^(-1)rn and constant v=Bq. For0<hr<1/8 all these directions are
regular and |v|<1/3. Exact null incidence for each fixed q gives

    Z=gamma_v(1+n.v),
    dot n=P_n v/[r(1+n.v)],
    dot Z=gamma_v|P_n v|^2/[r(1+n.v)].

Thus J(n)=h^2 n_1^2(1-n_1^2) and <J>=2h^2/15>0. At the observer,
sigma=diag(2h/3,-h/3,-h/3), W=0 and Ric=0, so T2M gives M=0. This check
uses the actual flat arrival derivative rather than inserting curvature into
the target formula. Positive raw drift is not sufficient for negative Ricci,
even for geodesic clocks. These supplied query controls are not UDT histories.

**Protocol check.** If r_i=d tau_i/dt and arrival t_o=F(t_e), then
Z=[r_o(F(t_e))/r_e(t_e)]F'(t_e). For flat emitter x=0, receiver x=L+vt,
v=3/5, the same-coordinate proper-rate quotient is4/5 but actual Z=2.
At v=-3/5 that quotient remains4/5 while Z=1/2 on its regular outgoing domain.
This is the clock lane's chain-rule counterexample, not a criticism of the
compass paper's acknowledged need for time-transfer modeling.

**Physical implication test.** T2M permits a geometric conclusion if the
corrected measured or physically required M is supplied. Neither ordinary
clocks, W4, universality nor the working far-separation asymptote establishes
M>0 or identifies it as the positional contribution. Temporal drift, variation
of source separation and a global asymptotic family are different questions.
This leaves the same type of physical join as PSW/J1. T2 is a complementary
diagnostic for a different preparation, not a selected field law or response.

## 4. Survivor, novelty and next decision

T1 specifies a stringent operational agreement sufficient to fix the metric
scale field. T2 gives a corrected joint-observable curvature diagnostic and an
exact adverse control for the raw-sign inference. Standard GR geometric methods
produce both without importing Einstein dynamics. They are useful tools, not
newly derived native conditions on UDT's positional geometry.

The bounded search found no completed physical connection from the inspected
existing commitments. This is not proof that the complete postulates are
insufficient or that a new one is required. The one-geometry interpretation and
ordinary clocks remain intact. EPS norm closure, clock/tidal agreement and
screen reciprocity mostly recover already accepted structure; imposing their
identities again cannot supply the missing assignment. No historical grade or
mathematical result is automatically retracted.

The research decision should now distinguish an independent physical condition
from another inverse measurement method. A proposed next derivation must name
the additional positional requirement as applied to an actual comparison and
show why it constrains the corrected quantity or another geometric object.
Alternatively independent observations could constrain candidates, with their
own assumptions and authorized work order. This review has not chosen such an
observation, physical population, response, new postulate or successor campaign.

All primary/source versions, omissions and discovery history are preserved.
Two fresh source-first/exposed reviewers must still challenge this candidate,
especially the T2 C1 expansion and metric-versus-observable distinction.
No scientific CPU, GPU, empirical fit, formal proof or human review ran here.
