# SD1 initial conditional candidate — clocks and labelled beams

UNREVIEWED, CONDITIONAL, UNPROMOTED. BE1's complete reviewed metric WITH its
calibration clarification is an explicitly conditional UNPROMOTED dependency.
This candidate follows exploratory hand algebra, before SD1 numerical/reviewer
outcomes. G421/G423 and current G312 FILTER ONLY authority retain their limits.

## Calibrated family and exact records

Use WORK_ORDER's fixed marked two-mode protocol. Write
 Q(xi)=a1 cos(k xi)+eta cos(2k xi), a1=(Q-c2 eta)/c1,
 theta=k xi_A=21/40, k=3/4, c1=cos(theta), c2=cos(2theta).
The constant Q is the common source value Q(xi_A); it does not fix the whole
function. Initial H_y,H_z fix L,Q at the supplied epoch and labelled axes.
They also fix initial K_XX at the source, but not spatial derivatives nearby.
Let
 v=partial_eta partial_xi Q(xi_A)
   =k[(c2/c1)sin(theta)-2sin(2theta)]
   =-k tan(theta)[1+2cos(theta)^2] !=0.                  (1)
The last inequality follows from 0<theta<pi/2, without a floating-point gate.
Let q=P_t(1,xi_A)=3Q/2 and r=P_txi(1,xi_A)=3Q_xi(xi_A)/2.
Thus q is fixed and r_eta=3v/2. This is a real amplitude direction in the
supplied marked family; no proof of nonisometry of all unmarked members is made.

The positive axial ray is exactly xi=xi_A+t-1, with t_o=1+d, d>0.
R(d)=N(1+d,xi_A+d)/N(1,xi_A) is its dimensionless proper-clock slope.
It compares nearby source emissions to the SAME fixed receiver; it is not
dt_o/dt_e, which equals1 on this axial branch. The full lapse constraints give
 log R(d)=-log(1+d)/4
          +(1/4) integral_0^d (1+u)[P_t+P_xi]^2(1+u,xi_A+u)du.     (2)
Along the ray d lambda/dt=t(P_t+P_xi)^2. This includes the quadratic mixed
metric terms; no linearized or frozen lapse is used.

Define positive labelled infinitesimal screen widths, inherited from G421:
 D_y=b_y(o)/N_e integral_0^d N^2 exp(-P)/(1+u)du,
 D_z=b_z(o)/N_e integral_0^d N^2 exp(+P)/(1+u)du.         (3)
All functions in the integrands are evaluated on the full axial ray; b_y(e)=
b_z(e)=1 and N_e=3/4. Physical widths multiply by the same L. Set
 H(d)=log(D_y/D_z)=P_o+log I_minus-log I_plus,
 I_plus/minus=integral_0^d W exp(+/-P)du, W=N^2/(1+u).  (4)
H is a SIGNED labelled y/z shape record. The ordinary unordered aspect ratio
is exp(|H|), and does not carry that sign. No finite beam envelope or flux law.
The positive widths also give the inherited local endpoint rank on this branch.

## Controlled short-distance rank

At t=1, P=P_xi=P_xixi=0 and P_tt=-P_t, so along the ray
 P=q u+(-q/2+r)u^2+O(u^3),
 P_t+P_xi=q+(-q+2r)u+O(u^2),
 W/W(0)=1+(q^2-3)u/2+O(u^2).
Substitute these into (2)-(4); the logarithms of I/d are regular at d=0:
 log R=(q^2-1)d/4+[1/8-q^2/8+qr/2]d^2+O(d^3),
 H=[r/3+q(1-q^2)/12]d^2+O(d^3).                       (5)
For the second equation, the weighted mean of P is
 qd/2+[(-q/2+r)/3+q(q^2-3)/24]d^2+O(d^3);
log I_minus-log I_plus is minus twice this through second order. Endpoint
rulers cancel the entire order-d shape term. Dropping them changes the result.

The finite-mode Bessel functions and positive lapse are real analytic for t>0
and finite parameters. On a compact parameter neighborhood and 0<=d<=d_* with
1+d in a fixed positive slab, the normalized positive integrals I/d extend
analytically across d=0. Taylor's theorem gives bounded third-order remainder,
including one eta derivative. This justifies differentiation of (5), not merely
formal series. Constants depend on that neighborhood; no global amplitude,
infinite-mode or finite experimental error bound is asserted.

At fixed Q,L, phases and layout,
 partial_eta log R=(9/8)Qv d^2+O(d^3),
 partial_eta H=(v/2)d^2+O(d^3).                         (6)
For EACH fixed finite (Q,eta), the beam derivative is nonzero for all sufficiently
small positive d; a finite d_0 exists but is not numerically certified here.
For Q!=0 the clock derivative is also nonzero for sufficiently small positive d.
The one-dimensional inverse function theorem therefore gives LOCAL recovery of
eta from the labelled beam record, or from clocks when Q!=0, after calibration.
Equivalently the supplied initial-rate calibration plus the new record has full
local parameter rank at the stated positive-d regime. This is not global
one-to-one inversion, uniform sensitivity or an acquisition/noise theorem.
Sensitivity vanishes like d^2 as separation tends to zero: smaller d is not
claimed better for an actual instrument. Unknown modes/phases/epoch add freedoms.

## Exact blind case and the role of marking

At Q=0, all amplitudes are linear in eta: P=eta P_* and
lambda-lambda0=eta^2 lambda_*. Therefore for EVERY finite positive axial segment
 R(eta)=R(-eta), D_y(eta)=D_z(-eta), H(eta)=-H(-eta).    (7)
Clocks alone have an exact sign ambiguity; at eta=0 their first eta derivative
vanishes. Area D_y D_z and the unordered aspect ratio are also even in eta.
The labelled shape retains the local rank from (6), including eta=0, for small
positive d. If the y,z labels are discarded, that sign discrimination disappears.
With the supplied equal transverse periods, eta reversal is the coordinate
exchange y<->z at Q=0. No physically distinct unmarked spacetime pair or preferred
frame is inferred. The result distinguishes members of a supplied marked query.
At Q!=0 this axis exchange also changes Q's sign and is outside the fixed signed
calibration comparison. No global classification in that case is attempted.

This one conditional result identifies complementary information and a precise
blind case within a known family. It does not select a UDT metric, restore the
open event/path-to-pair assignment, identify physical light, test observations,
or force the theory toward an existing physical interpretation.
