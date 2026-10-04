# FCL1 mathematical adversarial review — exposed stage

Verdict: **ACCEPT_WITH_LIMITS** for the exact conditional theorem in
INITIAL_CANDIDATE.md, SHA-256
`9563063c01c69ffef69654915e522d0019192d7470fb41d2c88fbf438a3c8371`.
No substantive mathematical defect or required repair was found. This verdict
does not adopt RG, promote a registry source, or establish a physical prediction.

Reviewer: fresh separate inherited-model context `/root/fcl_math`. No human or
different-model review is claimed. SOURCE_FIRST.md was independently constructed
from the work order and existing source arguments, then sealed at SHA-256
`24dfbb35624d4521ba34bd0972850107cbf595b613a9367f4713c8ec7fe0365c` before
candidate exposure. That seal remains intact. The parent reported reading the
source-first reconstruction only after freezing its candidate. I subsequently
read the initial candidate, CANDIDATE_FREEZE.json, CHECK_PLAN.md, check_controls.py,
and checks/parent_controls.{json,stdout,stderr}. I did not open the sibling
review. The frozen candidate, control, plan and work-order hashes match their
saved pins. Parent baseline/startup audits remain attributed, not independently
rerun here. All my written artifacts are inside review_math/.

## Independent argument and the candidate's stronger estimate

The sealed source-first argument is distinct from the parent's spatial-covector
proof. It uses the scalar conformal boost E=-gbar(u/Omega,n), derives

    dE/dr=(E^2-1)/(r E)+T/(alpha E),
    T=gbar(v,nabla_bar_v n), |T|<=C E^2,

and integrates in the decreasing-r direction to bound E. It then solves the
forced equation for Q=E^2-1 to obtain Q=O(r). This independently establishes
v->n_p without assuming a rescaled-velocity bound. Its weaker sufficient rate
does not independently imply the candidate's sharper rate; I checked that rate
separately after exposure as follows.

The candidate uses the physical spatial momentum P_i=w_i/x. In the normal
collar, lowering the ordinary geodesic equation gives exactly

    dP_i/dtau = -(partial_i N) gamma^2/N
               +(1/2)(partial_i h_jk) T^j T^k.

Because dx/dtau=-x gamma/N,

    dw_i/dx = w_i/x + (partial_i N) gamma
               - N(partial_i h_jk) T^j T^k/(2 gamma).

The signs and x factors agree with independent substitution. There is no
suppressed derivative of h in x: lowering first puts those derivatives into
the derivative of P_i; they cancel correctly in this exact covector equation.
The spatial derivatives of N and h remain explicit, so the construction is not
a disguised homogeneous calculation.

Uniform positive bounds for h and h^-1 give
gamma<=1+c|w|, gamma>=sqrt(1+c'|w|^2), and |T_spatial|<=c''|w|.
Thus the force is at most C(1+|w|), without first bounding w. With
s=log(x0/x), the upper Dini derivative of r=|w| obeys

    D+ r <= (-1+C x0 e^-s)r + C x0 e^-s.

This inequality also holds at w=0, where D+|w|<=|dw/ds|=x|F|.
The integrating factor is

    mu(s)=exp[s-C x0(1-e^-s)].

Its forcing integral is C x0 integral_0^s exp[-C x0(1-e^-t)] dt,
at most C x0 s. Consequently

    r(s)<=exp(C x0)e^-s[r(0)+C x0 s],

which is exactly candidate (1). Applying comparison on each finite s interval
does not assume late boundedness or require a new existence theorem for the
already supplied receiver. The general O(x log(1/x)) rate is justified.

The sealed variable-lapse example N=1+b y has
Y'=Y/x+b sqrt(1+Y^2) and hence Y=b x log x+O(x) when b!=0. This independently
shows why an O(x) tangential-rate claim would be too strong. The actual candidate
retains the logarithm and is consistent with that diagnostic.

## Collar regularity, endpoint and proper time

The vector field V=grad_bar x/gbar(grad_bar x,grad_bar x) is C2 with nonzero
denominator near p. The C3 defining function supplies a C3 boundary chart.
Flowing that chart inward gives a local C2 coordinate map with invertible
Jacobian. Pulling back the C3 metric through this map gives at least C1 metric
coefficients, which is sufficient for the lowered geodesic equation and all
first-derivative bounds used here. The coordinates need not be C3, and the
candidate correctly claims only the regularity it uses.

Orthogonality follows because the transported y-coordinate vectors are tangent
to the level sets of x while V is proportional to its gradient. Hence
gbar=-N^2 dx^2+h_ij dy^i dy^j with arbitrary positive spatial h and arbitrary
positive lapse N. This is an available local coordinate choice, not an added
metric ansatz. A compact smaller chart around p contains a final receiver tail
because convergence to p was explicitly supplied. All local coefficient and
inverse bounds therefore follow from existing hypotheses.

Candidate (1) gives dy/dx=O(x[1+log(x0/x)]), whose integral from zero to x is
O(x^2[1+log(x0/x)]). Using the already supplied endpoint and C1 metric
coefficients then gives N(q(x))=N(p)+O(x) and
gamma-1=O(x^2[1+log(x0/x)]^2). The correction in

    d tau/dx=-N/(x gamma)

relative to -N(p)/x is O(1)+O(x log^2(x0/x)), which is integrable at zero.
Both the logarithmic proper-time divergence and the stated finite additive
limit are valid. This checks the actual physical proper-time parameter; the
conformal parameter is not silently substituted for it.

## Actual emitter/null preparation and gauge

The candidate uses the actual regular interior emitter and the supplied
regular affine-data extension of the actual ray family. Its unnormalized
emission frequency has a positive finite limit because a nonzero future null
vector has a strictly negative contraction with a regular future timelike
vector. Consistently scaling each complete ray by the reciprocal preserves
finite nonzero limiting data at both endpoints. This is permitted normalization,
not independent endpoint tuning.

The independently derived receiver limit gives
B*=-gbar_p(K,n_p) finite and positive. The exact frequency relation therefore
gives xZ=1/B ->1/B*. A bounded set of directions alone would not suffice, but
the work order explicitly supplies a regular limiting family/affine data.
The conclusion is conditional on those supplied data and does not prove
global branch availability, uniqueness or caustic avoidance.

For x'=a x and gbar'=a^2 gbar with smooth finite positive a, the same physical
ray has kbar'=a^-2 kbar and T'=T/a. Thus B'=B/a, the normal limit transforms
consistently, and x'Z->a(p)/B*. Physical Z is unchanged. The candidate correctly
preserves a gauge-dependent residue and avoids any measured-distance or X_max
identification. Its future orientation has x decreasing and n=-N^-1 partial_x;
the signs used in both proper time and frequency are consistent with it.

## Independent checks of the saved finite controls

The general proof is analytic. I inspected the actual direct-Christoffel control
implementation and its saved exact output; I did not rerun the parent's code
or call it an independent implementation. The diagonal physical-Christoffel
formula is correct for the supplied diagonal metric, and its independently
computed acceleration differentiates w=h u/x before comparison. This is a
useful formula check, not coverage of all h or proof of the general asymptote.
Its intentional force omission is nonzero for each of the six saved cases.

As independent hand arithmetic, at the first saved point and spatial velocity
(3/4,0,0), gamma=5/4, a1=107/90 and N=13697/12012. Equation (7) gives

    F1=5/28-3N/(50 a1)=9259/76505,
    F2=5/44, F3=5/52.

These match the saved omitted-force residuals, showing a nonzero lapse/spatial
force rather than a vacuous zero assertion. The other five rational output
triples were inspected but not independently re-evaluated by hand.

For the exact free-clock control, set x=t and G=sqrt(1+x^2). The reported
u=(-xG,x^2,0,0) has g(u,u)=-1 and spatial physical momentum u^y/x^2=1.
Its curve y=2-G obeys dy/dx=-x/G. The actual ray incidence is
x_e=x+y=2-G+x, and emission proper time satisfies d tau_e=-dx_e/x_e.
Thus direct differentiation gives

    Z = x_e/[x(G-x)],  xZ->1.

This agrees with direct contraction with kbar=(-1,1,0,0)/x_e. The two
nontrivial original geodesic components cancel: the x acceleration derivative
is x+2x^3 and its connection term is -x-2x^3; the y terms are -2x^2G and
2x^2G. This independently checks the free receiver rather than trusting the
script's zero residual array. For 0<x<1/4, 1<x_e<1+x<5/4, within the supplied
compact interior emission interval.

For the accelerated control,
u=(-(1+x^2)/2,(x^2-1)/2,0,0) is unit, with
y=1-x+2 atan x and x_e=1+2 atan x. Direct contraction gives omega_o=1/x_e
and Z=x_e->1. Differentiating the actual event correspondence independently
gives the same ratio. Direct physical acceleration is
((x^2-1)/(2x),-(1+x^2)/(2x),0,0), with g(a,a)=x^-2. Hence it is not a
counterexample to the free-geodesic theorem, but an explicit check that merely
requiring a unit clock is insufficient. Its emissions satisfy
1<x_e<1+2x<3/2, away from the boundary.

The saved capture reports returncode 0, duration 0.4172915399540216 seconds,
maximum RSS 49364 KiB, 2 GiB virtual-address limit, and no wall or CPU timeout.
Actual stdout parses as PASS with six nonuniform cases and the two clock
families; stderr is empty. I independently verified stdout/stderr hashes and
the capture utility hash against the receipt. These are checks of the saved
artifacts and correspondence; they do not independently authenticate runtime
history or turn exact finite controls into a general theorem. No optional
reviewer control was executed, so the scientific check count here is zero
additional scripts and the independent proof/hand recomputations above.

## Limits, survivor and repair disposition

The strongest survivor is the complete stated conditional single-receiver
theorem, including its local O(x[1+log(x0/x)]) spatial-covector bound,
future-normal tangent limit, infinite physical proper time, and positive finite
xZ limit under the supplied interior-emitter/regular-null-family hypotheses.
There is no mathematical repair to request for this frozen version.

Keep these limits in central integration: RG remains UNADOPTED; the existence
and physical admission of the completion and branch remain supplied; initial
data are finite but not uniformly controlled across populations; the residue
depends on gauge and ray data; no global full-history monotonicity, fixed-
emission distance curve, field/action/source law, X_max value/realization or
physical clock anomaly follows. FCW1's zero-gradient and interior-deformation
limits remain intact. The accelerated example must remain explicitly outside
the geodesic quantifier.

Checks omitted: no reviewer numerical/symbolic script, no second independent
evaluation of all six parent rational cases, no full registry/maintenance test
rerun, no upstream source-package replay, no global receiver/null existence
theorem, no different-model or human review. Source-first and exposed-stage
arguments are independent reasoning axes; parent controls share their author's
code and library and are described accordingly. Final central integration has
not yet been inspected in this stage.
