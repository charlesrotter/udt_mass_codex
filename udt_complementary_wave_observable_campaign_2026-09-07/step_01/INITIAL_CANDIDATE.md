# CO1 — wave tidal geometry and an unused network contrast

Conditional candidate, not promotion. Source-first separate-context review
controls its eventual status. Scope and two-step/two-hour limits are in the
campaign log. No new observations or waveform/source parameters are fitted.

## What is complementary

LC1/LC2 constrain an effective local stationary d ln N/dh under supplied
laboratory metrology, not a full metric or curvature tensor. G261 W4 supplies
the working physical-metric role; later owner-provisional G312/G313 admits
Ric=Lambda g in its bounded vacuum arena, leaving Weyl/initial-data freedom.
Time-dependent tidal curvature is therefore an additional geometric channel,
not a relabeling of that clock gradient. Neither observation is used to calibrate
the other. No same-global-history/metric joining of the laboratory and a distant
event is constructed, and no stationary-Killing formula is applied to a wave.

One exact admitted local zero-Lambda wave construction makes the retained
freedom explicit, with length coordinates (u,v,x,y):

    ds² = -2 du dv + dx²+dy² + H du²,
    H=A(u)(x²-y²)+2B(u)xy.

For arbitrary smooth A,B, the only possible Ricci component is
Ric_uu=-(H_xx+H_yy)/2=0; R_uiuj=-H_ij/2 has transverse matrix
[[-A,-B],[-B,A]]. This is an exact local geometry statement, not a binary
source, a measured amplitude, a global completion or a stability claim.
It generalizes the explicit G313 constant-A witness by a same-equation check.

For the MEASUREMENT approximation, use a weak locally plane tensor wave in a
nearly flat detector patch, with x0=c_E t, propagation direction supplied, and
transverse trace-free perturbation h_ij=h_plus eplus_ij+h_cross ecross_ij.
At linear order, linearized Riemann gives

    E_ij = R_hat0 i hat0 j = -(1/(2c_E²)) d²h_ij/dt².

This is first-order curvature, not an exact nonlinear TT metric or a theorem
that every admitted UDT metric has only this local signal form. Higher orders,
background curvature, near-zone variation and source evolution are outside
the examined detector approximation. A local tetrad/observer must be specified;
the curvature projection, rather than h00 in a chosen gauge, owns the meaning.

## What the instruments supply

For arm unit vectors a_I,b_I the long-wavelength differential response is
D_I=(a_I a_I^T-b_I b_I^T)/2. Conventional calibrated interferometer response
supplies the comparison

    d_I = D_I:h + e_I = F_Iplus h_plus + F_Icross h_cross + e_I.

Geocentric delays are applied consistently. This readout, laser transfer,
actuation, clocks and noise model are explicit supplied measurement assumptions,
not G352 content or a UDT instrument derivation. The official LAL detector
construction documents this tensor. The two waveform functions remain FREE;
neither a binary inspiral phase nor a fixed polarization ellipse is imposed.

For frozen D and consistent delays, the Fourier tidal projection is
D_I:E(f)=(2pi f)² d_I(signal,f)/(2c_E²). It constrains a band-limited projection,
not DC curvature or every spatial metric component. The f=0 integrations and
unobserved channels stay free. For time-dependent D, differentiating D:h also
introduces D-dot and D-double-dot terms; the displayed derivative map then
requires those known response terms, not naive differentiation of d alone.

Controlled regime: |h|<<1; wavefront approximately planar across the network;
arm light-travel parameter epsilon_L=2pi f L/c_E<<1 and detector rotation
epsilon_rot=Omega*T<<1 for a frozen-frame window. These are method controls,
not measured error bounds. No precision null test may discard corrections
merely because epsilon is small: either calculate the frequency/time-dependent
response or bound its matrix error DeltaF and propagate the leakage below.
CO2's static matrix calculation can establish design conditioning, not precision
release eligibility. This preserves an informative calculation without silently
granting the approximation experimental accuracy.

## Information and unused contrast

At a fixed aligned time or resolved frequency, let F be the supplied N-by-2
response and rank(F)=r. Exactly N-r independent linear contrasts annihilate
both free tensor functions: rows of Z span ker(F^dagger), so z=Z^dagger d
contains only the combined error under the response model. For N=3,r=2 there
is one such combination. In a real long-wavelength convention, a nonzero
q=Fplus cross Fcross gives q^T F=0; normalize only when q!=0. Complex
frequency response uses the Hermitian null space, not a naive real cross product.

This follows by rank-nullity; finite examples do not own the quantifier.
With only two rank-two detectors there is no unused channel for two arbitrary
waveforms. Rank-one response instead leaves N-1 null directions but identifies
only ONE tensor combination. Rank deficiency is not an extra reconstructed
polarization. Small singular values amplify waveform-inference noise even when
the algebraic null direction exists. All singular values depend on response
and noise weighting; unweighted condition numbers are geometric design only.

If a chosen two-detector training submatrix F_T is invertible, its wave estimate
is F_T^-1 d_T, and a third response has the unused residual

    r_J = d_J - F_J F_T^-1 d_T.

No waveform restriction is needed. But this subtraction also transports noise;
its variance is w^dagger C w for the full supplied error covariance C and
w=(-F_J F_T^-1,1). Diagonal independent-noise formulas are only declared
comparators. The null and reconstructed signal views are not automatically
statistically independent; whitening with a correct covariance produces
orthogonal uncorrelated views, and independence additionally needs a suitable
distribution (for example joint Gaussian). No such distribution is adopted here.

For normalized q with q^dagger F=0 and actual response F+DeltaF,

    |q^dagger d| <= ||DeltaF||_2 ||h||_2 + |q^dagger e|.

Separate this deterministic conditional bound from standard uncertainties and
coverage probabilities. A supplied bound on errors/wave amplitude makes it
useful; an arbitrary error function per detector can explain every d and erases
the test. Common amplitude calibration leaves the null relation unchanged but
not absolute inferred curvature; differential gain/phase/timing can leak signal.
An arbitrary alternative component inside col(F) is invisible to the null test;
three instruments cannot identify/exclude all arbitrary extra polarizations.

Sky/delays/calibration/noise/window/band/regularization must not be chosen using
the reserved contrast without accounting for that exposure. A fixed optical
counterpart position can supply sky query data, conditional on association and
astrometry; the follow-up was triggered by GW localization, so it is not wholly
independent event selection or a new blind test. Fitting sky using all three
GW amplitudes and then claiming the same null was untouched is not allowed.

## Primary documentation and precise survivor

The earlier GW170814 source screen left sky/conditioning unresolved. GW170817
has a concrete optical-coordinate route (GCN21529) and H1/L1/V1 strain releases.
The LVC GW170817 tests paper explicitly uses GR phase templates and compares
pure mode families. Its published odds are NOT a waveform-free null test and
will not be reused as one. Official product/uncertainty documentation can
support a later conditional analysis without every raw servo sample, but data
and calibration versions must match. No release has yet been certified here.

Survivor: a precise additional curvature readout and an algebraically unused
network relation are available in this declared measurement class. CO2 should
check the actual geometry and a viable release/calibration route. Positive
design rank does not imply useful statistical power; poor conditioning, a
response mismatch or nuisance degeneracy is an informative negative result,
not a verdict against UDT. Geometry/calibration and emergence stay parallel.

Sources: G261 EXACT_DERIVATION; G276 AUDIT_REPORT; later G312 ADOPTION_RECORD;
G313 EXACT_DERIVATION/AUDIT_REPORT; reviewed ORS1 and LC2 limits.
Primary measurement references:
https://lscsoft.docs.ligo.org/lalsuite/lal/group___create_detector__c.html
https://dcc.ligo.org/public/0150/P1800059/008/main.pdf
https://gwosc.org/events/GW170817/
https://gcn.nasa.gov/circulars/21529
Exact fetched source hashes, source limitations and failed retrievals belong
in the campaign source ledger. No adopted premises or accepted grades changed.
