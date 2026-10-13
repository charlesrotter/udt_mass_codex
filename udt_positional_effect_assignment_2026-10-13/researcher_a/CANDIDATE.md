# PEA1 A — finite echo and tidal-standard discriminator

**Frozen explorer candidate; UNADOPTED physical assignment, awaiting separate
review.** This proof supports a finite operational test of B's conformal vacuum
assignment (CVA), and distinguishes that test from native positional attribution.
It also identifies a weaker conformal-Killing interpretation of the same test.
No source, field equation, observer population or physical scale is adopted.

## 1. Sources, discovery and scope

My initial TMR proposal was saved before cross-exposure. Subsequent inspection
of UDT_DEVELOPMENT R8GRL showed that GRL1 T1 already proves the exact strict
light/free-fall matching rigidity, including its two-direction minimum and
one-congruence exception. I reuse it without novelty claim. R8GRC's conformal
S+F obstruction has different hypotheses: the present comparison does not
equate the full Weyl tensor under that tangent isometry or impose S+F.

The owner statements in udt_positional_geometry_clock_connection_2026-09-28,
udt_shared_geometry_extension_2026-09-29 and the universal-law clarification
preserve ordinary proper clocks, one geometry and circumstance-dependent
universality. They supply neither CVA nor the echo preparation below. The
current native supplied-pair kernel remains chi=tanh(Phi), with physical
event/path/depth assignment and extra positional attribution OPEN.

After my initial proposal, coordinator's interest in relational comparison and
then B's CVA proposal were disclosed. The following operational development is
cross-exposed collaboration, not independent discovery/review of B. B owns
the existence and uniqueness argument for a Ricci-flat conformal representative;
that theorem is conditional input here, not re-certified by my echo checks.

Nearest prior mathematics: SGE1's stationary-clock result and actual echo
composition; NCI1/CGW1's endpoint-redshift/conformal-Killing class; GRL1's rich
trajectory rigidity. The original Hasse–Perlick paper and Dirmeier–Plaue–Scherfner
discussion credit the existing conformal-Killing interpretation:
https://doi.org/10.1063/1.527863 and https://arxiv.org/abs/0802.3642.
The finite echo/tidal-invariant combination below is derived here, not claimed
new across the literature. Only these targeted sources and current central
chapters were searched; no exhaustive novelty survey was performed.

All statements concern a smooth Lorentz4 region, signature (-,+,+,+), consistent
time orientation, positive conformal factor and regular chosen null branches.
Units c_E=1 do not select a physical scale. The metric, domain and query clocks
are supplied, free-and-explored. No claim covers horizons, global completion,
caustics, X_max, noisy reconstruction or instrument availability.

## 2. Same-history clock contrast is exact, but free fall changes

Supply g=Omega^2 g0, with psi=log Omega, on the same identified region.
This is a conformal comparison hypothesis. In CVA, g0 would additionally be
the uniquely determined Ricci-flat representative up to constant calibration.
The identities in this section do not require Ric(g0)=0.

Take the same unparameterized observer histories, endpoint events and regular
null branch for both metrics. If U0 and k0 are respectively a g0-unit endpoint
clock tangent and g0-affine null tangent, then

    U=Omega^-1 U0,     k=Omega^-2 k0

are the g-unit clock tangent and a g-affine tangent along that ray. The second
identity follows by inserting the conformal connection difference

    D(X,Y)=X(psi)Y+Y(psi)X-g0(X,Y)grad0 psi

into nabla_k k; the two derivative terms cancel and g0(k0,k0)=0. A constant
affine rescaling would cancel in every endpoint ratio. Therefore

    omega_g = -g(k,U) = Omega^-1 omega_0,
    Z_g/Z_0 = Omega_o/Omega_e.                         (A1)

Endpoint velocities need not be static or identical to each other. Their
dimensionless local Lorentz angles are preserved by the conformal identification.
The factor in (A1) is independent of which endpoint timelike tangents are used
for the fixed events/ray and their corresponding normalization. Absolute
constant normalization of g0 cancels. This is a well-defined whole-metric
comparison once the identity map and conformal representative are fixed.

It does **not** preserve acceleration or the same free-fall preparation. Direct
substitution gives, with P0(V)=V+g0(U0,V)U0,

    a_g=Omega^-2 [a_0+P0(grad0 psi)].                  (A2)

Two g0-geodesic directions at one point remain geodesic in g only if grad0 psi
is parallel to both; nonparallel directions force dpsi=0 there. This is the
existing GRL1 obstruction, not a new exclusion. A physical experiment using
separately released clocks in each metric generally moves the endpoint events
and ray, so (A1) alone is not that experiment's contrast.

## 3. An actual finite-range echo eliminates a stationary lapse

Assume g0 has a specified future timelike Killing field xi on the query tube.
Set N0=sqrt(-g0(xi,xi)). Prepare actual g-proper clocks A and B on two of its
orbits, with U=xi/(Omega N0). They can be accelerated; these are query clocks,
not an adopted universal observer population. Choose an outgoing null branch
from event e on A to b on B and an immediate return branch from b to r on A.
Both future branches and their nearby tick correspondence must be regular.

Since xi is conformal Killing for g,

    L_xi g=2 xi(psi)g,
    k^a nabla_a[g(k,xi)]=k^a k^b nabla_(a xi_b)=0

on each affine null leg. The physical frequency at a clock is proportional to
1/(Omega N0). Thus

    Z_out=(Omega_b N0_B)/(Omega_e N0_A),
    Z_back=(Omega_r N0_A)/(Omega_b N0_B),
    Q := d tau_A(return)/d tau_A(emit)
       = Z_out Z_back = Omega_r/Omega_e.              (A3)

N0 is constant along each Killing orbit, so its cancellation is exact even
with stationary shift, unequal outbound/return travel times or reference Weyl
tides. The relay event is the same b in both formulas. A finite waiting time
requires its actual transfer map and replaces b by distinct receive/send events;
the simple cancellation cannot silently be retained.

Here Q is the derivative of the actual echo map at finite spatial/radar range:
neighboring emitted ticks are sent through the same regular branch. It is not
generally a ratio for arbitrarily large inter-tick intervals. In a flow parameter
t of xi, stationarity of g0 gives t_r=t_e+T for the fixed branches, and the
conformal metric has the same null incidences. Directly differentiating
d tau_A=Omega(t,A)N0_A dt gives the same (A3), independently of the conserved
frequency argument. A finite-range experiment still needs ordinary derivative
and clock-error control; no precision has been certified.

The comparison has operational substance: the echo intervals are measured on
one physical clock, and the stationary reference's gravitational lapse cancels
without estimating its value from redshift. Nevertheless, stationarity, the
correct orbit preparation and the conformal comparison are substantive inputs.

## 4. A finite joint echo/tide relation

Let I_g=C_abcd[g] C^abcd[g] be the signed real quadratic Weyl invariant. Under
g=Omega^2 g0, the connection formula in section2 changes curvature by Hessian
and gradient terms of the form g0 Kulkarni–Nomizu a symmetric tensor. Those are
precisely trace pieces removed by Weyl projection. Thus the (1,3) Weyl tensor
is unchanged and the all-lowered tensor obeys C[g]=Omega^2 C[g0]. Four inverse
metrics contribute Omega^-8 to its square, giving

    I_g=Omega^-4 I_0.                                 (A4)

Because a Killing flow preserves its metric and curvature, xi(I0)=0. At e,r
on the same orbit, I0(e)=I0(r). Combining (A3) and (A4) gives the exact finite
consistency condition

    Q^4 I_g(r)=I_g(e).                                (A5)

If I is nonzero, this predicts Q=[I_g(e)/I_g(r)]^(1/4), with positive root and
positive ratio. Negative I of fixed sign is allowed. At I=0 the un-divided
identity can be vacuous and does not recover Q. Nonzero Weyl does not ensure
I!=0; radiative/algebraically special sectors can have vanishing scalar
invariants. No continuity or conditioning claim across I=0 is made.

The two record sets have distinct physical meaning: actual echo interval
derivatives and a local tidal compass sufficient to reconstruct the required
Weyl invariant. Their ideal availability is assumed. Inferring I from Q and
then checking (A5) would be circular. A source-independent local curvature
measurement is a method; an instrument's ability to perform it is unverified.

This is a useful operational test of the assigned clock preparation and scale
evolution. It is not another estimate of total scalar curvature R, does not
set R's sign and does not force Weyl to vanish. It measures a relation between
finite timing and tidal change. Passing it alone proves neither stationarity
nor a Ricci-flat conformal anchor; no converse classification is asserted.

## 5. The weaker tidal-shape criterion is the known CKV class

On I!=0, define the diagnostic tensor h=|I_g|^(1/2)g. It is unchanged under
conformal rescaling and can be viewed as expressing geometry in local tidal
units. It is not a second physical metric or modified proper-time law.

If xi is conformal Killing for g, L_xi g=2 sigma g, the same conformal-weight
argument along its local flow gives xi(I)=-4sigma I. Therefore L_xi h=0.
Conversely L_xi h=0 implies L_xi g=-xi(log |I|)g/2. Timelike Killing fields of
h are precisely timelike conformal-Killing fields of g on this domain.

Consequently the proposed TIDAL-SHAPE-STATIONARITY route does not discover a
new class beyond NCI1/CGW1. It gives an invariant way to express that existing
class and the finite echo test (A5), under less restrictive hypotheses than CVA.
This is a deliberate narrowing of the exploratory proposal. It cannot by
itself justify choosing a vacuum anchor or assigning the conformal factor to
the positional contribution.

There may be several timelike Killing directions; selecting a query is not
selecting a preferred physical population. Formula (A5) holds for any one
validly prepared direction and its echo. Arbitrary moving clocks do not inherit
it from covariance. If no such timelike direction exists, this echo preparation
is unavailable even if B's conformal vacuum assignment exists; dynamical
Ricci-flat references need the more general same-history comparison (A1).

## 6. Exact Schwarzschild controls and a false positive

Take the supplied exterior reference

    g0=-f dt^2+f^-1 dr^2+r^2 dOmega_2^2,
    f=1-2m/r,  r>2m>0,
    x=r+2m log(r/(2m)-1),  dx/dr=1/f.

Its radial null branches satisfy dt=+/-dx. For
Omega=exp(Ht+beta x), hold A at x_A and B at x_A+L, L>0. Their events have
t_b=t_e+L and t_r=t_e+2L. Direct actual clock lapses give

    Z_out=sqrt(f_B/f_A) exp[(H+beta)L],
    Z_back=sqrt(f_A/f_B) exp[(H-beta)L],
    Q=exp(2HL).                                       (A6)

The factors after the square roots are the two same-history CVA contrasts.
For H>0 and beta>H, Q>1 but the return contrast is less than one. Hence positive
echo is not equivalent to mutual positive contrast, even with nonzero Weyl
and a conformally Schwarzschild reference. The beta dependence cancels because
the emitter returns to its same reference orbit. All-null nonnegative contrast
would require H>=|beta| in this restricted family, a strictly stronger condition.
This is a supplied exact counterexample to an inference, not an admitted UDT
history or rejection of B's stronger monotonicity conjecture.

For general Omega(t,r), held-clock acceleration computed directly from the
physical metric has only radial component

    a_g^r=m/(Omega^2 r^2)+f Omega_r/Omega^3.

For the displayed Omega it becomes Omega^-2[m/r^2+beta]. Its magnitude is
Omega^-1 |m/r^2+beta|/sqrt(f). Even beta=0 retains a changing physical holding
acceleration through Omega. The query cannot be described as the same free-fall
or the same physical acceleration as the reference. It is realizable only as
an ideal controlled-clock query at its stated scope.

At fixed r, I0=48m^2/r^6 and I_g=48m^2/(Omega^4 r^6), so (A5) agrees with
Q=exp(2HL). As H,beta approach zero on a fixed compact regular exterior with
fixed finite t range and bounded derivatives, Omega and its first two derivatives
approach their reference values, giving C2 convergence to Schwarzschild.
This is mathematical recovery on that compact domain, not a measured solar
system bound or global extension through r=2m.

## 7. Ordinary GR does not disappear from this comparison

Time-only conformal Schwarzschild is the known nonrotating Thakurta class,
not a new geometry: Mello–Maciel–Zanchin, arXiv:1611.05077, equation(2),
https://arxiv.org/pdf/1611.05077. Their equations(5)–(9) analyze its GR
stress tensor as an imperfect fluid with radial heat flow. Their cosmological
source and global assumptions are not adopted as UDT and are not needed for
the proofs above. This inspected comparison suffices to show that the same
metric pattern already has an ordinary GR source interpretation.

An even simpler comparison is a regular expanding spatially flat FLRW region
g=a(eta)^2[-deta^2+dmathbf{x}^2]. Comoving held coordinates are geodesic, and
a separation L gives Q=a(eta+2L)/a(eta)>1 when a grows. This is familiar
cosmological clock evolution, not a diagnostic unique to an added UDT effect.
Its Weyl invariant vanishes, so the tidal-ratio test is unavailable; it is
not a counterexample to an I!=0 premise or a certified unique-CVA reference.

For two candidate interpretations producing exactly the same physical g and
same actual query, the metric clock/optical interface returns the same records.
Thus even a unique Ricci-flat conformal anchor and positive factor do not show
that the factor is absent ordinary GR matter evolution. A physically justified
vacuum-sector designation, new metric dynamics or another independent test
would be needed for that stronger causal label. This is a concrete confounder,
not a theorem that UDT needs a new postulate or cannot make progress.

## 8. Decision and evidence

The useful return is a conditional physical comparison, not native geometry
selection: a reference fixed independently of the echo can yield a definite
same-history factor (A1), and a stationary-reference preparation makes its
temporal change accessible through an actual echo plus independent tide test
(A3)–(A5). This removes the need to insert an arbitrary stationary gravitational
lapse into that echo observable. It does not derive CVA, an all-null sign, a
positional distance curve, an asymptotic scale or a vacuum-sector identification.

Retain CVA-ECHO as a concrete discriminator if B's anchor argument survives
review. Reject the claim that Q>1 alone isolates mutual positional slowing.
Do not promote tidal-shape stationarity as a new geometric class. Require
the reference/preparation and GR-source confounding to remain in every brief.
A useful subsequent decision concerns the physical reason to assign the
conformal vacuum comparison to the extra effect, not another larger survey of
positive echoes. No successor work is authorized by this recommendation.

The frozen COMPUTE_PLAN and check_echo.py were executed once after coordinator
slot authorization using the existing TPS1 capture. CHECK_RESULT.json records
22 exact symbolic identities passing, including direct four-metric Christoffels,
two original affine-geodesic residuals, actual frequency/acceleration readouts
and an independently differentiated proper-clock echo. Capture took about
0.712 seconds, peak RSS52724KiB, one thread and 2GiB virtual memory; no killing
timeout and no stderr. These are same-researcher symbolic checks, not fresh
review or independent evidence of physical attribution. Full Weyl contraction
and B's anchor existence/uniqueness were not recomputed by this script.

Researcher A is a separate explorer context with the inherited model, exposed
to parent and B as recorded. Initial proposal, rejected TMR novelty and TSS
strengthening, fixed plans, source credits, proof, code and outputs are retained.
