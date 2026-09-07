# FW1 — matched release; narrowed off-source screen

Candidate frozen23:04UTC2026-09-07, before any strain sample/PSD/contrast
inspection. Baseline b11fcea; scope/premise/exposure stamps in CAMPAIGN_LOG.
Status CANDIDATE, awaiting actual fresh-context review. This is a narrowing
under the approved error/power gate, not a completed event-analysis contract.
FREEZE.json controls the next calculation. No event unseal is licensed here.

## What is established by the metadata check

The three official O2_4KHZ_R1 files cover GPS[1187008512,1187012608),
16777216 float64 samples at4096Hz. Each matches the official published MD5;
local SHA256 identifies exact bytes. H/L source C02 and Virgo Repro2A agree
with the official release map, not the special C00/Repro1A event product.
The full98s proposed event support passes DQ127 and no-transient-injection
bits23. H/L have ongoing CW injections(mask23), Virgo has none(mask31).
Therefore no all-injection-free or astrophysical-residual claim is available.

The fixed100s background grid, excluding every98s support intersecting
GPS[1187008680,1187008980), gave36 candidates. Strict metadata screening
removes starts1187009316,1187010516,1187011916. The33 survivors are frozen
in metadata_filtered_run.stdout: first12 train the noise PSD, remaining21
are reference records. This selection used metadata only. Initial assertion
failure and its source-preserving pre-candidate repair remain in history.

T2100313v3 supplies event-epoch C02 estimates at1187008882 and run-wide Virgo
estimates; LIGO bracketing hourly records were independently inspected by the
reviewer. These are discrete-time estimates, not continuous error certificates.
In41 sampled30–500Hz rows, median |R_model/R_true-1| maxima are0.006057(H)
and0.013017(L); Virgo median is1. The sampled pointwise intervals include
H magnitude[0.9848004,1.0212786], L[0.98557623,1.0312196], V[0.949,1.051].
They are NOT deterministic full-band bounds or a joint probability statement.
The release response to true strain is the INVERSE of documented true/model
ratio if no correction is applied. Bias and centered uncertainty are distinct.

The public noise-subtraction source documents independently measured witness
channels, safety/hardware/software tests and finite calibration-line checks.
Those support its intended use, not exact retention of every unrestricted
waveform. Narrow spurious-line and finite-test caveats remain. Downstream
injection cannot certify upstream cleaning or decimation. Swope's primary
paper gives J2000 coordinates and centroid/WCS errors, resolving the missing
frame label; a full frame/timing/finite-arm response error contract is still
needed for a precise event-null interpretation. No further documentation
search is needed merely to perform the following off-source screen.

## Exact mathematical scope of the next calculation

Let x_i be a98s sampled vector, N=98*4096. P removes its DC and Nyquist
Fourier coefficients. A_i is the real cyclic shift with multiplier
exp(+2pi i f tau_i) on P's image. C crops four seconds from each end.
Use the fixed CO2 F and delays, and b=(-F_V F_HL^{-1},1), so bF=0.
The finite residual is r=C sum_i b_i A_i P x_i. Apply a COMMON periodic
Hann window w on the90s core, then DFT. For positive retained frequencies,
I_k=2|DFT(w r)_k|^2/(fs sum w^2), Q=mean_k I_k/S_train(f_k).
S_train is the frozen mean Welch estimator in FREEZE.json; no event input.

On the expressly declared DISCRETE CYCLIC STATIC surrogate
x_i=A_i^{-1}(F_i h), h=(h_plus,h_cross) arbitrary in P's image, r=0.
That algebra is exact; Fourier/crop/taper implementations have numerical
checks. It is NOT the continuum rotating finite-arm release response theorem.
A cyclic extension is numerical boundary data, not a physical periodic source.
DC/Nyquist removal and the band projection are analysis choices, not new UDT
laws. Window leakage, variable response and calibration can break a physical
null; an exact claim would require N A R=0 or a supported error bound on the
actual domain. The old static-matrix rank check does not supply that join.

The off-source calculation remains meaningful as the sensitivity of this
fixed linear/quadratic functional of actual released channels, including CW
and instrumental background. It does not require guessing the true event h.
It does not establish a lower/upper power bound on a DIFFERENT improved
complete operator. Neglecting extra nuisance penalties is not proof of such
domination. A failed screen stops this chosen procedure, not the instrument,
all free-waveform tests, or UDT. An alternative in col(F) is invisible here.

## Frozen decision and statistical limitations

The supplied resolution query is residual h_rss=1e-21 strain sqrt(second)
on90s BEFORE Hann weighting, equivalently1.0541e-22 unweighted RMS. This is
an explicit analysis target, not a claimed source amplitude, law or physical
content. Report the entire1e-23 through1e-19 grid, not just this threshold.
Use three spectral families and eight fixed independent phase draws each,
all explicitly synthetic. Their finite fractions crossing max(reference Q)
are descriptive REINJECTION fractions, not90% population detection power.
The same21 backgrounds define the threshold and receive injections, so the
fractions are not independent binomial trials or a held-out coverage proof.
Require >=90% crossings in EACH family at the target to survive the screen.

Were a separately reserved noise-only statistic exchangeable with those21
references conditional on training, its rank could attain1/22=0.04545.
No unconditional significance or selection-corrected GW claim follows:
stationarity/exchangeability, upstream retention and response/calibration
error are not proved. Report chronological diagnostics without altering
windows, weights, thresholds or rejecting inconvenient samples. Estimate
the residual PSD directly, retaining actual training-channel contributions
and cross terms; never substitute Virgo noise alone or assert stochastic
independence from algebraic bF=0. There is one detector contrast, not three.

If screen fails: reviewed finite-procedure sensitivity limitation, event
UNEXAMINED. If screen survives: full physical operator and nuisance gates
remain OPEN; do not unseal merely because a software injection passed.
The approved campaign may narrow or stop honestly within its remaining
budget; no new premise or physical identification is needed for this screen.

## Sources and evidence type

Official release: https://gwosc.org/o2_details/ and matching checksum catalogue
https://gwosc.org/archive/md5/O2_4KHZ_R1/strain-hdf.txt .
Injection semantics: https://gwosc.org/o2_inj/ .
Calibration: https://dcc.ligo.org/T2100313/public (v3 archives/README).
Upstream tests: https://arxiv.org/abs/1809.05348 (v2).
Astrometry: https://arxiv.org/abs/1710.05452 .
CO1/CO2 remain reviewed conditional dependencies, not scientific promotion.
Metadata arithmetic/checksums support correspondence; source statements and
analytic finite-model identities have separate roles. No observation fitted,
event strain inspected, canon/manuscript/accepted grade changed at this stage.
