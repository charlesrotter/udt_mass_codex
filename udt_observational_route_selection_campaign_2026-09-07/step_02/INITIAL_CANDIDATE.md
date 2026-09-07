# ORS2 — metric-to-clock comparison and limits

Candidate frozen after exploratory source inspection; no empirical fit or
outcome-blind claim. Depends on reviewed ORS1, not an accepted grade. No new
physical adoption. Method algebra below is conditional on stated hypotheses;
its checks are not an independent certification of the experiment.

## 1. What geometry supplies

G261 W4 is WORKING/POSIT_NOT_CANON: the completed physical metric governs
proper clocks/rulers/free fall/null propagation. It does not derive strontium,
Ramsey spectroscopy, a gravimeter, laser transfer or their corrections.
G276 distinguishes a dimensionful same-segment proper-clock anchor from a
dimensionless ratio; the ratio here does not attach a global homothety scale.
G312/G313 do not uniquely supply an Earth metric, matter model or laboratory
history. We use a supplied stationary local laboratory geometry, not a new
solution of its source problem or a vacuum equation inside the apparatus.

Let K be a timelike Killing field, parameterized by a common stationary time t,
g(K,K)=-c_E^2 N^2, N>0. Laboratory observers have u=K/N and g(u,u)=-c_E^2.
This includes the static form -N^2 c_E^2 dt^2+gamma_ij dx^i dx^j, but does
not require vanishing stationary shift. K(N)=0 and the Killing identity give

    a_mu = u^nu nabla_nu u_mu
         = N^-2 K^nu nabla_nu K_mu
         = -(2N^2)^-1 partial_mu g(K,K)
         = c_E^2 partial_mu ln N.

Hence for a proper spatial path between stationary observers, with unit
tangent e and proper length h,

    ln(N2/N1) = (1/c_E^2) integral_1^2 a_mu e^mu dh.

For rotation the spatial path can be understood locally in the stationary
observer quotient; N is constant along K, so the projected gradient suffices.
This is an exact stationary-geometric identity, not a new force law. Identical
corrected clocks counting proper time give the ratio R=N2/N1 when their rates
are compared against the same stationary time convention. Photon emission/
reception frequencies have a different endpoint ratio; the actual laser/
Ramsey comparison convention must implement the stated rate readout.

Write z upward. A supported laboratory's proper acceleration is upward, while
a released test body's measured initial gravitational acceleration is downward.
The identification of gravimeter magnitude with the supported congruence's
|a_z| uses the supplied conventional local free-fall/metrology model, including
stationarity, alignment and nongravitational corrections. With that bridge,

    R-1 = exp(integral a_z dz/c_E^2)-1 ~= g_mag Delta z/c_E^2.

The paper indexes ensembles downward; its positive tabulated separation has
negative rate difference, so its predicted signed gradient is -g_mag/c_E^2.
Neither an arbitrary function N nor one universal Earth source law is selected.

Error support: if |a_z(z)-a_z(0)|<=B|z| on a height H, replacing the integral
by a_z(0)H has absolute log-rate error <=B H^2/(2c_E^2). For s=g_mag H/c_E^2,
|exp(s)-1-s|<=exp(|s|)s^2/2. At H=.01m and the supplied g magnitude the latter
bound is <6e-37. B is a supplied bound, not measured in this campaign; the
source's local-height/gradient model is used only at its reported uncertainty.
Finite cloud averaging is likewise conditional on its local-gradient model.

## 2. What the 2023 experiment supplies

Primary source: Zheng et al., Nature Communications14,4886 (2023),
https://www.nature.com/articles/s41467-023-40629-8 and its Supplementary Note3.
Five strontium ensembles span roughly1cm; ten simultaneous pair comparisons,
14 normal-operation runs, published differential systematic budget. It supplies
an actual measurement, not a proposed ideal tidal protocol.

Supplement3H supplies independent LaCoste–Romberg gravimetry, cross-checked
against survey points, g=-9.803m/s^2 (rounded). DDS lattice transport gives
array extent1.00(.01)cm; tilt correction gives height.99(.01)cm, consistent
with camera imaging. This is conventional atom/lattice/imaging metrology,
not a native UDT derivation. Use the geometric-height calibration, NOT the
clock-inferred heights in Fig4/Supplementary Table1. The source reports
expected signed gradient -10.9e-19/cm with uncertainty<.1e-19/cm.

Source Table1 gives statistical uncertainty.7 and systematic2.5 in units
1e-19/cm; reported total2.6 (1sigma). The large corrections are not omitted:
weighted mean total correction+122.8 versus expected magnitude10.9. This
campaign does not certify that budget afresh. Documentation supports using
the authors' published summary conditionally rather than demanding raw shots.

Controls and dependencies, not a claim of statistical independence:

| Effect | Supplied control/assumption | Relevant limitation |
|---|---|---|
| Second-order Zeeman | Vary B and gradient to obtain coefficient; independent sensitive transition measures B; opposite-spin splitting gives differential B | Vector light-shift correction shared with lattice evaluation; source coefficient/error model retained |
| Density | Vary atom number separately for each pair; measure numbers each shot | Pair-dependent, not one height-linear correction; source fluctuation bound |
| Blackbody | Vary viewport temperatures, measure response slopes; thermistors cross-calibrated in ice bath | Thermal geometry/monitoring model and transfer of controlled response to operating condition |
| Lattice light | Vary intensity/detuning and spatial differences; fit response and monitor daily | Residual light-gradient mechanism hypothesized, not definitively identified; measured response model and separation from delta-u component supplied |
| Probe/DC Stark | Vary intensity/misalignment or applied electrode voltage to bound responses | DC bound includes specified charge-asymmetry/field-geometry assumption, not assumption-free |
| Ellipse extraction | Quantum-projection-noise model and Monte Carlo bias correction from atom number/contrast | Supplied atomic/noise estimator model, not raw theory-free data |

The documented control-variable slopes/splittings need not set the gravitational
intercept: a height-only rate offset survives. Authors added an unknown gradient
to target AND systematic-evaluation data, finalized corrections/uncertainties
before unblinding, and report no post-unblinding changes. These facts support
an unused target contrast in their procedure; blinding alone cannot certify
all nuisances, covariance or physical assumptions. Our source selection and
published results are already exposed. There is no new blind data holdout here.

In particular it would be circular to infer g or heights from this clock
gradient and then use them to predict the same gradient. It would also be
circular to force a gravitational-gradient subtraction during corrections.
The inspected procedure instead measures response to controlled variations
and reports the gravity-dependent residual as its target. This supports a
published-summary comparison under its correction model, not an independently
reprocessed or model-free certification. Calibration and target share apparatus
and some records; they are not asserted to be independent random variables.

## 3. Actual records and non-independence

Authors' processed data: https://zenodo.org/records/8184043 (DOI
10.5281/zenodo.8184043; CC-BY4.0; metadata revision2, modified2023-07-26).
Four files total29,753bytes; Fig3.csv958bytes and Fig4.csv369bytes retrieved
for schema only and MD5 checked against official metadata. No fitting done.

Fig3 has two header rows and14 data rows: four height-binned comparisons
for panel3b, plus14 runwise gradients for3a with uncertainties. These are
not ten raw pair records and not independent replications: both panels use
the same experiment. Fig4 is ten **clock-inferred heights**, unusable as
independent geometric calibration. Fig1/Fig2 are listed figure data; not
retrieved or assumed to contain raw covariance. Full raw-shot covariance and
author analysis code are not in this inspected deposit; paper says code on
request. No request/contact is authorized or needed for the summary-level
route. A new correlated pairwise fit is NOT established as executable here.

Noiseless geometry clarifies information count. For five node values
q_i=ln N_i, ten edge contrasts y_ij=q_j-q_i form y=Dq. The complete connected
graph incidence D has rank4: common q shift is invisible; six cycle relations
are identities, not six independent gravity tests. Restricting q_i=q0+k h_i
uses one contrast direction, leaving three possible non-linear node-shape
directions in an ideal resolved network. This is not a claim that the released
four binned points or correlated pair estimators supply three certified tests.
With arbitrary node biases b_i, y=D(q+b) cannot separate q from b. Documented
nuisance constraints, not unique selection of every input, make the published
gradient meaningful. Geometry between sampled points remains functionally free.

## 4. Sensitivity, interpretation and surviving route

analytic_checks.py uses only published error/expected-gradient summaries,
standard SI c_E and exact finite graph algebra. It never reads observed
gradients. The decimal forecast sqrt(.7^2+2.5^2+.1^2)/10.9 is approximately
.2384: roughly24% relative 1sigma sensitivity to the local predicted gradient,
conditional on the published error combination (not a new covariance audit).
This is consistent with using reported total2.6/10.9. Equivalent potential
difference uncertainty at1cm is about.0234m^2/s^2, or2.38mm of height using
the supplied g. Do not confuse this gradient sensitivity with the paper's
different intercept/height-resolution statistic. No new alpha fit or residual
significance is calculated. The printed alpha result, if later cited, is the
authors' result, not ours and not a new UDT law.

After independently calibrating g, geometry, frequency scale and controlled
systematics, the gravitational clock-rate gradient remains a consequence to
compare without retuning those inputs. Conversely if the clock gradient is
used to calibrate a potential difference, that same gradient is not its test.
An allowed diagnostic departure coefficient may summarize tension, but does
not become an adopted coupling. Existing exposure limits the claim to a
retrospective quantitative benchmark/conditional parameter constraint.

What remains free: absolute lapse normalization and constant metric homothety;
spatial geometry, Weyl curvature, lapse away from sampled path, initial data
and time dependence beyond local stationarity. The measurements constrain
one local combination, not the complete metric, source content or stability.
They do not select the chosen phase/current/product recipe. Local failure
would test the combined stationary-geometric/readout/correction model, not
refute all UDT or uniquely establish a competing mechanism. Agreement would
be shared metric consistency (including GR), not distinctive confirmation.

ORS1's R and W remain alternatives. Cassini offers a published model-conditioned
gamma constraint with joint orbit/force calibration and a source discrepancy
in quoted uncertainties; a held-out arc is not documented here. GWOSC offers
actual strain arrays but an arbitrary-waveform test needs sky/response and
release-matched calibration bounds; existing pure-polarization evidence assumes
GR phase and is not an arbitrary-mixture test. Neither is rejected merely for
using conventional physics. C now has the shorter documented path to a modest
published-summary metric constraint. No observational fitting or follow-on
execution is authorized by this candidate.

## Source/verification limits

Source hashes, commands and schema observations are recorded in SOURCE_LEDGER.md
at campaign root and the fetch records. Supplement3H's printed sideband relation
uses an energy/frequency convention not independently reconstructed here; the
route uses the reported DDS/camera geometric height and its stated uncertainty,
not a new calculation of tilt from that equation. No flight/instrument defect
is alleged. Full source-theorem proofs, experiment raw processing, all atomic
coefficients, per-pair covariance and future-release eligibility were not replayed.
These omissions restrict the claim; they do not require a documentation campaign
before using a trustworthy published measurement at its reported scope.
