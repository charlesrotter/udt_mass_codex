# TSI1 source-first fidelity and identifiability review

**Status: source-first completed; candidate and integration not yet reviewed.**
`CONTROL_FREEZE.md` records startup attribution, exposure, scope and controls.
This is a fresh separate context with an independent mathematical argument and
implementation; it is not different-model, different-library, human, formal-proof
or empirical independence. The parent disclosed its proposed logarithmic timing
slope before this review; no TSI1 candidate, producer code or output was opened.

## What survives source inspection

CPR1 supplies a strict smooth actual incidence branch in x=1/R, with fixed
source/receiver histories, b varying between rays, Z=R C(x), C smooth and C(0)>0,
and receiver radial proper velocity v/R -> H. Therefore

    d log Z / d tau_o = (v/R)[1-x C'(x)/C(x)] -> H.

Here tau_o is proper length; receiver seconds multiply the derivative by c_E.
The derivative control is essential: the bare statement Z~CR would not suffice
for differentiated asymptotics. The CPR1 smooth tail and nonzero limiting
incidence Jacobian supply that control. This is conditional recovery of the
supplied H from an ideal record with an independently calibrated receiver clock.
It is not a physical field-law selector, native metric admission or empirical
measurement. No source size appears in this timing formula.

The exact homothety is

    (m,a,R,b,tau) -> lambda(m,a,R,b,tau),
    H -> H/lambda, Omega -> Omega/lambda, E -> E.

At corresponding events Z and angular quantities remain unchanged; J and source
screen sizes both scale by lambda. Thus redshift values and uncalibrated angle
records, with a co-scaled unknown source size, do not break this degeneracy.
A calibrated duration changes under it and can attach the scale. An unknown
multiplicative receiver-clock calibration leaves only that clock's H product.
ICN1/MGC1 and central R16 already own calibration versus selection and the
constants-only obstruction. c_E and G_obs alone remain insufficient to select a
nonzero length/time. A geometric m is not independently measured physical mass;
writing M=c_E^2 m/G_obs alone would define a readout, not supply an extra datum.

## Records and obstructions the candidate must state

1. Z is a ratio of actual proper intervals on matched source/reception events.
   Arbitrary unlabelled brightness variations or an unknown drifting oscillator
   are not automatically that record. An unknown constant rate multiplier
   cancels the logarithmic slope, which should not be rejected unnecessarily.
2. CPR1 has finite tau_e,* but infinite tau_o. Any fixed positive emitter tick
   spacing gives finitely many ticks in a bounded neighborhood before tau_e,*.
   Such a record cannot approach the asymptotic slope through infinitely many
   received pulses. An ideal continuous/differential record, or accumulating
   known emissions, is an extra record hypothesis, not an attained observation.
3. Source variability must be classified. If source rate q(tau_e)>0 extends
   smoothly with bounded logarithmic derivative to tau_e,*, then
   d log q/d tau_o=(d log q/d tau_e)/Z ->0, and the asymptotic received-frequency
   exponent survives. Unrestricted variability does not: in the ideal endpoint
   law delta=tau_e,*-tau_e proportional to exp(-H tau_o), q proportional to
   delta^p gives received frequency q/Z proportional to exp(-(p+1)H tau_o).
   A source nuisance can then mimic a different H. This is a diagnostic timing
   construction, not a new source-emission premise or a finite-data inference.
4. A finite observation window does not certify that the asymptotic regime has
   been reached or bound its bias. A parameter fit might identify H in some
   specified finite experiment, but that needs its own model, nuisance and
   uniqueness/error analysis. The asymptotic proof neither supplies nor forbids it.
5. A source image angle gives a physical scale only after its size/shape/orientation
   and the applicable map are known. OJM1's D_A is an area distance, not a universal
   scalar ruler in a sheared image, and inversion fails at caustics. Apparent
   angular motion needs an actual reference tetrad: arbitrary time-dependent
   frame rotation can create or remove angular drift.

## Independent angular lead, offered before candidate exposure

For the radial receiver let N=(-1/(E+v),E,0,0), an outward unit spatial vector
orthogonal to u_o in the regular outgoing chart. With signed equatorial photon
propagation angle theta measured from N,

    sin theta = b/(R A),
    cos theta = [s/(E+v)-v b^2/(R^2(1+s))]/A.

Thus sin theta_* = H b_*/sqrt(1+H^2 b_*^2), cos theta_*=1/sqrt(1+H^2 b_*^2),
and tan theta_*=H b_*. The sky arrival direction is opposite photon propagation;
its displacement from the corresponding opposite radial reference is equivalent.
Endpoint angle alone determines a dimensionless combination, not H separately.

There is a conditional angle-versus-calibrated-time possibility. In the supplied
b_*=0 preparation, implicit incidence differentiation gives
b=(Omega a/H^2)/R+O(R^-2). Consequently
theta=(Omega a/H)/R+O(R^-2), with nonzero leading coefficient, and smooth tail
control yields -d log|theta|/d tau_o -> H. This needs calibrated receiver time,
a physically specified stable radial/parallel tetrad and ideal unbounded angular
tracking, but no known source size or source cadence. A fixed nonzero physical
source angular resolution may still obstruct attainable late samples.

For generic b_* the 1/R coefficient of theta-theta_* can vanish; a universal
angular exponential index cannot be inferred without nondegeneracy. This lead
is independently derived here, not an adopted physical law or a claim of
complete inverse-problem coverage. The parent may include it only with its
own candidate review and a precise measurement protocol.

## Checks actually performed

`independent_checks.py` imports no TSI1 producer functions. It transforms CPR1
incidence integrals to x=1/r, independently solves b(R), and differentiates the
actual incidence equation to obtain db/dR. Its drift includes both A_R and A_b db/dR.
Twelve40-digit cases passed: b_*=0,2, R=10^3,10^5,10^7 and their lambda=3
companions. Homothety agreement was checked at1e-25, actual incidence residuals
below1e-28. At R=10^7 the relative timing-slope errors were3.06387508e-6 and
2.83068662e-6; error decreased across the frozen radii. The largest displayed
angular residual magnitude was5.74e-42. Eight exact/control groups passed.
The capture ran1.292s, peak52,560KiB, CPU-only,2GiB virtual limit, one BLAS
thread, no timeout. stdout/stderr/receipt retain command, versions and hashes.
No failures or repairs occurred. This is finite floating-point support for an
analytic limit, not numerical certification of all branches.

Not repeated: underlying full4D curvature/Jacobi integration, all OJM1/CPR1
producer tests, full406 premise audit, normal/maintenance closure, empirical
inference, finite-source inverse bounds, finite-window parameter identifiability.
Parent owns final audit and maintenance; they must be actually run and recorded.

**Review ceiling:** the timing lead survives under explicit smooth-branch and
record/calibration hypotheses. The strongest tempting overclaims are unattainable
fixed-cadence asymptotic measurement, constants-only scale selection, and angular
scale recovery without a dimensional record or calibrated geometric object.
