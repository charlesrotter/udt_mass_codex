# One geometry, time per separation, and automatic redshift

Initial candidate: CONSTRUCTION / REVIEW PENDING / UNPROMOTED.
Baseline, authorization and exclusions: WORK_ORDER.md. Exact owner intent:
OWNER_STATEMENT.md. No new field equation or physical history is adopted.

## 1. What is already automatic

Consider G220's supplied smooth metric, two future timelike clock curves, and
one regular future-null incidence branch. Write its arrival map as

    tau_B = F_AB(tau_A),   r_AB = F'_AB > 0.

With clock pulses as the observable,

    q_AB = frequency_received / frequency_emitted = 1/r_AB,
    1+z_AB = r_AB,    delta_AB = -log r_AB.

Longer received tick spacing IS redshift. There is no second redshift mechanism
or independently fitted response curve to derive. Finite pulse intervals give
the corresponding interval-average slope; the formula above is differential.
G220 already owns this result. The algebraic conversion chi=tanh(delta) does
not choose the physical incidence map or the separation assigned to its events.

The owner gives time per separation the fundamental interpretation. In local
clock/ruler calibration, 1/c_E = 1/299792458 s/m, about 3.33564095 ns/m.
This dimensionful calibration and the dimensionless ratio r_AB are distinct
objects in the SAME geometry. One must connect them, not add a second mechanism.

## 2. Exact connection in a declared longitudinal chart

For an explicit construction attempt take a supplied smooth diagonal 1+1 metric

    g = -N(t,x)^2 c_E^2 dt^2 + A(t,x)^2 dx^2,   N,A>0,
    p(t,x) = A/(c_E N).

N,A are dimensionless if t and x use time and length units. This is a declared
longitudinal diagnostic class, not the whole UDT metric. Flat transverse factors
could be appended for a local 4D control, but would not prove native admission
or supply the actual angular/screen/mixing sectors. Work on a compact regular
ray tube with monotone x, sign epsilon=+1 or -1, and one transverse intersection
with each supplied observer curve x_i(t). No caustic/global claim is made.

Null incidence is dt/dx=epsilon p. Supply endpoint coordinate velocities v_i
and define beta_i=p_i v_i, |beta_i|<1, eta_i=atanh(beta_i). These are velocities
relative to the static-coordinate orthonormal frame at each endpoint. Their
proper-clock rates are d tau_i/dt=N_i sqrt(1-beta_i^2).

Let t(x;t_A) be the ray emitted from x_A(t_A). Its variation at fixed x obeys

    dJ/dx = epsilon (partial_t p) J,
    J_A = 1-epsilon p_A v_A,
    J_B = (1-epsilon p_B v_B) dt_B/dt_A.

The initial and terminal factors follow by differentiating the moving-boundary
conditions. Hence, with s the positive coordinate distance along this monotone
ray (ds=epsilon dx),

    I_AB = integral_ray partial_t p ds,
    dt_B/dt_A = [(1-epsilon beta_A)/(1-epsilon beta_B)] exp(I_AB),

    log(1+z_AB)
      = log(N_B/N_A) + epsilon(eta_B-eta_A) + I_AB.             (1)

All endpoint values are evaluated at their actual emission/reception events.
This follows by multiplying the coordinate arrival slope by the proper-clock
normalizations, not by postulating independent physical dilation factors.
The integral is dimensionless: partial_t p has units inverse length.

Equation (1) is a coordinate representation of G220 on this restricted tube.
It combines endpoint clock normalization, observer motion and changing null
time-per-distance in one metric. The split depends on the chart and observer
convention; it does NOT identify a coordinate-invariant 'UDT part', prove
three independent causes, or license fitting I_AB after the fact. In particular
changing p by changing coordinates does not change the total r_AB.

For fixed-coordinate clocks, the same expression can be written

    log r_AB = integral_ray [epsilon partial_x log N
                             + p partial_t log A] ds.         (2)

The total derivative of log N along the ray proves equivalence of (1) and (2).
This explicitly avoids treating every time derivative of coordinate slowness
as physical redshift; the endpoint lapse can cancel it.

For the supplied reciprocal longitudinal specialization N=e^-phi, A=e^phi,
equation (2) becomes

    log r_AB = integral_ray [(e^(2phi)/c_E) partial_t phi
                              - epsilon partial_x phi] ds.  (2R)

This is an exact constraint on the readout of that supplied geometry. Allowing
phi(t,x) here is a diagnostic specialization, not a derivation extending F4's
static areal branch. The founding reciprocal block alone has not selected these
derivatives or the physical ray/observer assignment. Identifying the first term
as 'the UDT effect' would add an unproved physical interpretation.

## 3. Independent covariant expression and nearby limit

NCI1/G402 (INITIAL_CANDIDATE plus REPAIR) and DCI1/G403 already establish the general local
identity for supplied smooth unit observer field U, k=omega(U+n), c_E=1 units:

    d log omega / (omega d lambda) = -H - a.n - sigma(n,n),
    log r_AB = integral_ray [H+a.n+sigma(n,n)] d ell_U,
    d ell_U = omega d lambda > 0.                            (3)

Here H=div(U)/3, a=nabla_U U and sigma is shear. ell_U is the accumulated local
rest-length along that ray, not an asserted unique finite proper/radar/areal
separation. The endpoints must use this supplied observer field. Its extension
is not selected by UDT in this calculation. The integral is independent of
constant affine rescaling. No GR field equation appears.
Current G402/G403 grades are BANKED_DERIVED_CONDITIONAL / VERIFIED_WITH_CAVEATS;
the old candidate headers remain historical. SCOPED_REGISTRY.json preserves the
exact current fields and controlling banking reference; this packet does not
upgrade those sources or replay their full historical verification.

For a matched smooth congruence and a regular tube with
|H+a.n+sigma(n,n)|<=K along a ray of rest-length S,

    |log r_AB|<=KS,    |z_AB|<=exp(KS)-1.                   (4)

This is a conditional small-separation bound, not a measured tolerance or a law
selecting K. It says the rate contrast can approach zero while the local
time-per-distance calibration and light cones persist. Fixed, nonvanishing
relative endpoint rapidity need not have this limit; a uniform bound on the
interpolating congruence must not be silently assumed in that case.

At one event the even and odd directional integrands are respectively
H+sigma(n,n) and a.n. Positive total logarithmic redshift slope for both n and
-n is equivalent AT THAT EVENT to H+sigma(n,n)>|a.n|. That is a conditional
diagnostic, not an owner-adopted requirement on all directions, identification
of the even part with positional physics, or a claim about a finite outbound
and later return pair. The owner allows the combined observation to contain
other effects; a positional contribution is not determined by this algebraic split.

## 4. Controls, construction attempt and ownership stop

1. **Flat motion:** N=A=1, so r_AB=exp[epsilon(eta_B-eta_A)]. This is the
   existing SR null-clock readout, not the transported sech comparison.
2. **Static primary:** N=e^-phi(x), A=e^phi(x), fixed-coordinate observers.
   I=0 and r_AB=N_B/N_A. Stationary opposite future exchange gives inverse
   r, as in G265. This still does not settle the full nested positional premise.
3. **Time-coordinate control:** N=N(t), A=1, fixed-coordinate endpoints.
   With T=integral N dt the metric is flat. I=-log(N_B/N_A), so r=1 exactly,
   although the coordinate slowness varies. This catches a false attribution of
   coordinate p to physical positional redshift.
4. **Existing time-live family:** use G220's affine-ruler control with shift zero,
   rename its proper time tau, and keep the symbolic parameter b free:

       g=-c_E^2 d tau^2 + (a0+b tau)^2 dx^2,
       a0>0, a0+b tau>0.

   For fixed-coordinate clocks separated by coordinate L>0,

       tau_B=[(a0+b tau_A) exp(bL/c_E)-a0]/b,
       r_AB=exp(bL/c_E),    z_AB=exp(bL/c_E)-1.             (5)

   The continuous b=0 limit is tau_B=tau_A+a0 L/c_E and r=1.
   Both distinct FUTURE-directed exchange experiments have r=exp(bL/c_E).
   A later echo has slope exp(2bL/c_E). This is not mathematical inversion
   of the first event correspondence. b>0 gives mutual received redshift;
   b<0 on its positive domain gives the corresponding blueshift control.

   Change only time coordinate, dt=(a0+b tau)d tau. Then

       g=-(a0+b tau(t))^-2 c_E^2 dt^2
          +(a0+b tau(t))^2 dx^2.

   Thus a reciprocal longitudinal block can accommodate the example. This
   changes neither the observations nor the supplied history. It is G220's
   already-known control expressed in reciprocal coordinates, NOT a selected
   UDT history, full F4 areal metric, new cosmology or derived physical mechanism.
   In 1+1 this affine-scale geometry is locally flat; mutual redshift here can
   be ordinary relative recession. The construction therefore FAILS the gate
   of deriving a distinct positional effect from the current postulates.

   Write h=bL/c_E. For |h|<=h0, |exp(h)-1-h|<=exp(h0) h^2/2 by Taylor's
   integral remainder. Neither L nor b is equated to an observed distance or
   Hubble scale. Physical separation on this chosen slice is D_A=(a0+b tau_A)L;
   no solar-system threshold or scale follows. A hypothetical measurement
   sensitivity epsilon would constrain a chosen b and specified protocol;
   this is not a prediction or eligibility claim for an actual instrument.

The affine example was known from G220 before this attempt; its re-expression
is disclosed, not discovery presented as an independent breakthrough. Equations
(1)–(4) are known geometrical consequences/application, not new physical laws.
The new value of this packet is the explicit connection and fidelity to the
clarified interpretation, plus a precise stop before an unowned construction.

## 5. Exactly what remains open

The chain is now explicit:

    positional geometry and physical observer/path assignment
      -> actual null incidence F_AB
      -> r_AB=F'_AB
      -> automatic redshift 1+z_AB=r_AB.

The last arrow is settled, not an additional research gate. For the supplied
geometries the middle arrow is also settled by G220/(1)/(3). The first arrow is
not established as a complete native construction by the sources examined here.
The bare reciprocal calibration 1/c_E supplies neither the required variation
of the incidence map nor a dimensional detection scale. This does not prove
that the full UDT postulates cannot supply it, that a new physical premise is
necessary, or that the positional interpretation is merely units.

For a declared physical distance convention D and a justified observer/path
family, a native claim must determine r_AB(D;geometry,query data) from admitted
relations. It cannot use the desired redshift to choose a profile or treat a
generic even directional channel as a uniquely identified positional contribution.
An extension of GR requires a demonstrated appropriate correspondence and any
distinct predictions; the controls here test readout consistency, not empirical
GR recovery or a native response equation. Response-class membership, physical
history and interpretation of signal content remain at their current grades.

Return: explicit conditional connection, preserved founding interpretation,
and a failed native selection attempt with its precise ownership gap. No all-UDT
no-go, registry promotion, new physical premise or automatic successor.
