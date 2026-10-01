# PSW1 initial synthesis — a prepared-clock curvature discriminator

CONDITIONAL MATHEMATICAL CANDIDATE; UNREVIEWED integration; no physical adoption.
Fixed after three source-first specialist notes and their small algebraic checks.
Parent saw all three notes and prior TPS1 outcomes. Same inherited model in
separate contexts; no claim of different-model or human review. The final central
argument will remain in UDT_DEVELOPMENT.md, not this fixed evidence edition.

## 1. What the previous survey did not impose

R6 supplies Z[g,Q] once geometry and an actual clock/null comparison Q are given.
SGE1 already shows that the additional positional consequence must constrain the
physical geometry or comparison assignment; appending a second clock multiplier
to unchanged (g,Q) is not an implementation. TPS1 supplied Ric=0 and supplied Q.
It tested those consequences, not a positional admissibility condition on (g,Q).

The whiteboard's strongest route specifies an ordinary diagnostic laboratory so
that a clock coefficient becomes a test of curvature. Its physical identification
with the positional contribution is a separate OPEN join. This is a calculable
restriction of one proposed implementation, not an inference that UDT requires
new premises or that every valid initial state must be uniquely selected.

## 2. Route A — a supplied preparation and a derived local coefficient

Choose a smooth Lorentz4 geometry, event o, future unit U and spatial unit n.
Let A be the geodesic through (o,U). At B0=exp_o(L n) prepare another geodesic
clock B with initial velocity obtained by parallel transport of U along the
spacelike preparation geodesic. L is initial proper separation specified without
redshift. Reset B's proper label at preparation, and vary emissions on these
same worldlines near A's proper time s=0. Use a unique regular outgoing null
branch and an ideal immediate return in a small chronological normal tube.
No re-preparation at each tick, fixed receiver, physical population, preferred
observer or globally preferred center is assumed. These are supplied query data.

Use length units for proper time, c_E=1. Let p_L=d tau_B/d tau_A at emission0,
and q_L=d tau_A,return/d tau_B at the matched relay. With the repository curvature
convention R(X,Y)=[nabla_X,nabla_Y]-nabla_[X,Y], define

    T_ij=g(R(e_i,U)U,e_j),    tr T=Ric(U,U).

T is electric tidal curvature, not DDR's unidentified response E. The candidate
local received-clock formulas are

    log p_L(n) = -(1/2) T(n,n) L^2 + O(L^3),
    log q_L(n) = -(3/2) T(n,n) L^2 + O(L^3).             (1)

The second is an actual later future leg, not the inverse of the first map.
Both clocks are ordinary local clocks. On the matched clock leg R6 supplies
Phi=-log Z and chi=tanh(Phi); that algebra does not select T or attach a global
distance law.

### Derivation to be challenged

Fermi coordinates along A give, on the radial direction and to the required
order, g00=-(1+e r^2), g0n=0 and gnn=1, plus cubic jet remainders, where
e=T(n,n) at o. The radial mixed/spatial quadratic terms vanish by Riemann
antisymmetry. Frame-transport effects transverse to n enter beyond the displayed
radial coefficient; no totally geodesic two-surface is presumed in the general
claim. At |s|,|t|,r=O(L), the needed jets are

    r_B(t)=L-e L t^2/2+O(L^4),
    t_b=s+L-e L(s+L)^2/2-e L^3/6+O(L^4),
    tau_B(t)=t+e L^2 t/2+O(L^4).

Differentiating the proper arrival map gives p=1-eL^2/2+O(L^3).
The return relation is t_a=t_b+r_B(t_b)-e r_B(t_b)^3/6+O(L^4).
Its derivative divided by d tau_B/dt_b gives q=1-3eL^2/2+O(L^3).
Smooth fixed geometry, bounded jets on a compact normal neighborhood and
transverse arrival give C1 Taylor control. The remainders are local and
metric-dependent; no numeric solar/cosmic bound or global extension is claimed.
An expansion of one flight time alone would not prove the received-tick ratio.

Standard Fermi-coordinate methods and prior clock-curvature work are credited
in PRIMARY_METHOD_REFERENCES.md and the specialists' source ledgers. Neither
those references nor the polynomial checks validate new UDT physical premises.

### Trace, sign and what vacuum excludes

For an orthonormal triad of identically prepared experiments, the outgoing mean
and return mean obey

    (1/3) sum_i log p_i = -Ric(U,U)L^2/6 + O(L^3),
    (1/3) sum_i log q_i = -Ric(U,U)L^2/2 + O(L^3).       (2)

At leading quadratic order this equals the spherical mean; no equality of all
finite-angle records or higher-order spherical averages is claimed. A triad
recovers a trace, not the entire tidal form or an all-direction sign theorem.
Six independent quadratic-form directions could determine T's six components;
testing its eigenvalues is separate from sampling a few signs.

Ric=0 fixes these leading means to zero. If T is nonzero and trace-free, the
leading directional form has both signs; T=0 leaves higher orders undecided.
Positive leading mean requires Ric(U,U)<0, whereas positive leading shifts in
every direction require negative-definite T. Those are different requirements.
In the conditional Einstein family Ric=Lambda g the outgoing mean coefficient
is Lambda/6. This identifies a mathematical sector; it does not select Lambda.

For an operationally matched comparator g0, match initial frames, proper L,
units, velocities and relay rule, not coordinate worldlines. Then (1)–(2) hold
for differences with Delta T and Delta Ric. This is a diagnostic contrast, not
an already isolated positional contribution. In particular, two Ricci-flat
candidates have zero leading mean contrast under this preparation.

**OPEN physical join J1:** nothing inspected identifies this particular net
coefficient or matched contrast with UDT's positional contribution, or demands
a nonzero positive L^2 term. Such a statement would be UNADOPTED physical input.
An effect beginning at higher order, finite separation or different physical
comparisons is not excluded. The result does not reject Ric=0 as universally
UDT-incompatible. No observer population, matter law or new clock physics is
needed to *evaluate* the supplied diagnostic.

## 3. Controls already available within this whiteboard

The geometry context directly reconstructs curvature in the supplied exact
local product g=-(1+e x^2)dt^2+dx^2+dy^2+dz^2, checks receiver/null/proper-clock
jets and independently checks endpoint frequency. Holding B fixed instead
gives +eL^2/2: a physical preparation error reverses the leading sign.

The tests context supplies an independent time-dependent analytic family

    g=-dt^2+sum_i (1+kappa_i t^2)^2 (dx^i)^2.

At t=0 the spatial metric is Euclidean and its first time derivative vanishes,
so coordinate-comoving free clocks realize the same zero-relative-motion
preparation there. Along axis i let kappa=kappa_i. Null travel integrates
dt/(1+kappa t^2); neighboring-pulse differentiation gives
p=1+kappa t_b^2 and pq=1+kappa t_a^2, with integral limits L and2L.
For kappa=k^2>0, t_b=tan(kL)/k and t_a=tan(2kL)/k on2kL<pi/2.
For kappa=-k^2<0 use tanh instead, before the metric degeneracy.
Thus log p=kappa L^2+O(L^4) and log q=3kappa L^2+O(L^4), consistent with
T_ii=-2kappa_i and Ric(U,U)=-2sum kappa_i at preparation. Both signs survive
the same initial-separation/motion matching. These are off-equation controls,
not new Ricci-flat solutions or native-admitted UDT countermodels.

Ordinary inertial recession in flat spacetime gives both future-leg ratios
p=q=exp(rapidity)>1 under a different initial-velocity preparation. Therefore
mutual net redshift alone cannot supply positional attribution. None of these
controls selects a desired sign, constant, scale or asymptote.

## 4. Route B — endpoint factorization is testable but unadopted

For a separately specified physical clock congruence U, a stronger proposed
property is -log Z_AB=Psi(B)-Psi(A) for every short regular null segment.
G402/NCI1 already proves its conformal-Killing criterion for exp(-Psi)U, or
vanishing shear plus exact alpha=a_flat-H U_flat (local closedness and global
periods distinguished). This is a nonidentity condition that TPS1 did not impose.
It is not implied simply by F3's ordered reciprocal algebra or W4.

The supplied controls with all kappa_i equal satisfy that criterion with
Psi=-log(1+kappa t^2); both signs of kappa survive. Unequal kappa_i develop
shear and fail on a time neighborhood even though their initial shear vanishes.
Thus it tests a proposed compression and physical clock assignment, but does
not supply the intended additional sign, selected geometry or asymptote.
The related pointwise inequality B(n,n)>|a.n| for opposite infinitesimal net
directions likewise retains a supplied U; flat Milne clocks can satisfy it.
It cannot be promoted to an additional positional law from net signs alone.

This route is retained as a precisely labeled alternative and control. Repeating
NCI1's theorem is not a new solution-selection program. No radiation population,
clock-score stationarity or action is revived by this placement.

## 5. Provisional research decision

Prefer Route A's prepared comparison as a diagnostic vocabulary for a proposed
native connection. It gives a leading coefficient and controlled challenge that
were absent from TPS1's amplitude plots. Do not rerun a larger Ric=0 survey to
discover a nonzero Ricci coefficient it has already fixed to zero.

The next substantive question is whether an accepted positional premise yields
an actual restriction on this prepared observable, its higher-order terms or a
different specified finite comparison. Require the explicit implication before
using a positivity rule to select histories. A signed L^2 rule may be proposed,
but should not be adopted just to make the calculation close. No full native
field equation, scale, X_max realization or all-postulates nonselection theorem
has been derived in this whiteboard.

Cross-review must examine general4D preparation and C1 remainder, both future
legs, trace versus all-direction claims, exact control domains, source ownership
and the J1 gap. One bounded correction/re-review is available; preserve this
edition and each objection. Return a reviewed diagnostic and decision brief,
with actual new physical commitments visibly unadopted.
