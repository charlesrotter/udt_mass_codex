# LC1 — frozen published-summary comparison contract

Candidate for fresh review; not scientific promotion or an outcome-blind
preregistration. Authority, two-step/two-hour budget and exclusions are in the
campaign log and the approved work order. No new numerical benchmark run yet.
The authors' reported result and agreement, and the prior route review, are
already exposed. Subsequent review must not be described as empirical blindness.

## Object, scope and precise map

G261 W4 supplies the working physical-metric role, not an atomic/laser/gravimeter
law. On a supplied smooth stationary laboratory patch, let K be timelike Killing,
g(K,K)=-c_E²N², u=K/N. The reviewed geometric identity is a=c_E² d ln N and
Δln N=∫a·e dh/c_E² on a proper spatial path. Supported observers, identical
corrected clock-rate readout and conventional gravity/geometry metrology remain
explicitly supplied. Do not use a photon emitted/received ratio with reversed
endpoint convention. No Earth source solve or vacuum equation inside matter.

The target is the source's EFFECTIVE LINEAR gradient over its approximately1cm
array and sampled runs, within its local constant-gradient, stationary and
finite-cloud/readout approximations. It is not an unrestricted pointwise metric
jet. If those restrictions fail, the reported slope is a source-specific weighted
summary, not enough to infer a general local lapse derivative. The prior ORS2
bound B H²/(2c_E²) for bounded acceleration variation and exponential remainder
bound remain conditional methods; B is not measured here. No generic spatial
or temporal uniformity is derived from UDT.

Use downward ordered ensemble separation as in the paper. Let one displayed
gradient unit be U=10^-19 per cm. The numerical measured coefficient is y.
The independent geometric prediction in these same units is

    mu = -g_mag * L_cm / (c_E² * 10^-19),    L_cm = 0.01m.

L_cm is a UNIT conversion, not another measured array length. Supplied g_mag
is the positive magnitude of downward free-fall acceleration identified with
upward support acceleration by the source's conventional local metrology.
The published expected coefficient -10.9 is a rounding consistency check, not
a second prediction to combine with mu or a value tuned to the clock result.
The independently calibrated array height is already part of the source's
normalization; do not multiply a per-centimetre result by0.99 and still call
it a per-centimetre result. Do not add that same height uncertainty twice.

The clock-only local metric constraint in this declared linear model is

    kappa_up = -(y * 10^-19)/L_cm   [m^-1],
    a_clock = c_E² kappa_up        [m/s²].

a_clock is an inferred equivalent support-acceleration component, not an
independent gravimeter measurement. A rate change over a stated query segment
can be obtained by kappa_up H; that segment/history is supplied, not selected.
Clock ratios alone are homothety-invariant. Fixed dimensional metrology may fix
scale in an identified family/segment (G276/ORS2 caveat), but this calculation
does not infer the complete family/history or a global scale. Spatial metric,
unsampled lapse shape, curvature, time dependence and physical content remain free.

## Frozen source inputs and dependency roles

Zheng et al., Nature Communications14,4886 (2023), main Table1 and Methods;
Supplementary Note3A–H; DOI10.1038/s41467-023-40629-8. Exact bytes and source
identifiers are in INPUTS.json. No new broad search, fetch or data acquisition.

| Input | Value | Role and qualification |
|---|---:|---|
| y | -12.4 U | ONE corrected gradient, first/runwise analysis; supplied published summary, not newly fitted |
| u_y | 2.6 U | Reported TOTAL1σ standard uncertainty; primary marginal scale, not merely the0.7 statistical error |
| u_stat, u_sys | 0.7,2.5 U | Source decomposition for documentation/sensitivity only; do not replace rounded total2.6 with a newly assembled budget |
| g_mag | 9.803m/s² | Source independent LaCoste–Romberg/survey metrology, rounded value |
| c_E | 299792458m/s | Supplied observed/SI clock-ruler calibration convention, not UDT-derived scale |
| L_cm | 0.01m | Exact SI unit conversion |
| Printed reference | -10.9 U | Rounding check only |
| u_ref cap | 0.1 U | Conservative use of source's reported <0.1 standard uncertainty for g/height reference; NOT a maximum actual error |
| Total correction | +122.8 U | Source disclosure only; no reapplication to already corrected y |

These empirical values are source-pinned observations/measurement assumptions,
not `pinned-by-THEORY`. Under the skill's three-way choice audit they are
justified observational/query pins rather than unexamined `pinned-by-HABIT`:
each fixed value has its source and role above. The conditional metric identity
is `pinned-by-THEORY` with G261 and reviewed ORS2 hypotheses; correlation and
bias scenarios below are `free-and-explored` controls, not physical laws.

The source's total correction exceeds its target. Its Zeeman/lattice responses
share controls; density/ellipse terms are pair-specific; DC shift bounds use a
field-geometry/charge assumption; estimator correction uses an atomic/noise
model. These are inherited measurement assumptions, not independently recertified.
Author-reported finalization before unblinding supports separation of target
from controlled-response calibration, not zero covariance or complete validity.

## Error models: explicit conditional second-moment statements

Define D=y-mu. Interpret the reported u_y and reference uncertainty as marginal
standard deviations of zero-mean comparison errors e_y,e_ref within the source
measurement model. This centering/marginal interpretation is a stated statistical
assumption, not established by our arithmetic. If those are not adequate marginal
uncertainties, neither model below independently certifies the actual experiment.
The reference may share controls with the clock analysis. No raw covariance is
reconstructed, and no physical law is added by either statistical scenario.

**Q: zero cross-covariance comparator.** Inherit the source total u_y; assume
Cov(e_y,e_ref)=0 only for this comparator, with0<=u_ref<=0.1. Display the upper
standard-uncertainty value

    U_Q = sqrt(u_y² + 0.1²).

This is not a claim that the paper established cross-covariance zero. Within
u_y, the authors' full total-error model is inherited, not decomposed anew.

**C: unknown cross-correlation envelope.** For any admissible covariance,
Var(e_y-e_ref)=u_y²+u_ref²-2Cov(e_y,e_ref). Cauchy–Schwarz gives

    |u_y-u_ref| <= SD(e_y-e_ref) <= u_y+u_ref <= U_C=u_y+0.1.

The upper bound is sharp given only these two marginal error scales (oppositely
correlated errors). This is a bound on STANDARD UNCERTAINTY, not on realized
error and not a raw covariance certificate. It preserves arbitrary shared-input
correlation between these two summaries, not arbitrary unbounded omitted bias
or an incorrectly reported marginal u_y. Do not demand every raw sample to use
a conditional published-summary measurement at this scope.

Report D, U_Q, U_C and their one-standard-uncertainty bands. Classify whether
zero lies inside each displayed band, merely as a descriptive consistency
comparison; no p-value, rejection/acceptance of UDT, Gaussian assumption or
automatic68%/95% coverage. The clock-only kappa/a summaries use u_y alone;
do not insert u_ref into a constraint inferred solely from the clock summary.
No confidence interval with validated coverage is claimed by this contract.

## Frozen robustness controls and decision rules

Keep nominal calibration and y unchanged. Define a diagnostic signed additive
correction displacement b, D(b)=D+b. Use only the predeclared scenarios
b=t*u_sys, t in {-1,-1/2,0,1/2,1}. These are counterfactual sensitivity controls
in source-error units, NOT fitted changes, hard bounds on actual biases, added
independent uncertainties, or evidence that such displacements occurred. Do not
add them in quadrature to u_y or count the same systematic budget twice.

Report: (i) zero-mismatch displacement b0=-D; (ii) each scenario D(b) and its
membership in the fixed Q/C displayed bands; (iii) thresholds U-|D| for every
displacement |b|<=B to remain inside that same one-standard-uncertainty band
(only if B<=U-|D| and this is nonnegative); and (iv) the unidentifiability if
an unconstrained additive height-gradient bias is allowed. Thresholds are
conditional algebra, not newly measured bias bounds. Useful outcome can be
loss of descriptive overlap under a scenario, with no wholesale UDT verdict.

Source/rounding controls: independently calculate mu from g and c_E and require
agreement with printed -10.9 within0.05 U (half its last displayed decimal
place). This checks numeric correspondence, not extra experimental precision.
Keep rounded source inputs explicit; do not claim meaningful extra digits.
Only source-error arithmetic and declared local geometric conversion are new.

Implementation plan: standard-library Decimal at60digits and separate-context
independent argument/implementation. Check cm-to-m/sign/uncertainty mapping,
dimensional round trip, and covariance envelope. Catch-proof any new guards
against sign reversal, missing cm conversion, use of statistical-only error,
double counting the same experiment and target-based reference substitution.
No large grid, simulation, raw-pair fit or observational tuning.

## Exclusions and return

Do not use the second same-data gradient as another observation, Fig4's
clock-inverted heights as external calibration, or Fig3 bins as independent
raw pairs. The existing deposit metadata is a provenance pointer; no arrays
are needed for this scalar-summary calculation. No new physical premise,
recipe adoption, source solve, grade/canon or fixed-manuscript change follows.
Fresh LC1 review must close any load-bearing objection before LC2 execution;
one same-premise repair/focused re-review, within the campaign hard stop.
