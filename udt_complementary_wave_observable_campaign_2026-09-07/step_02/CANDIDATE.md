# CO2 — actual fixed-query network design

Conditional finite-design candidate; pending fresh adversarial review. Dependency
is the reviewed CO1 at c5dd7945, review31c578ab, preserved in commit9da534d3.
This result is not an empirical residual, product eligibility, physical-content
identification, source solution or promotion. All CO1 measurement/arena caveats
are inherited. Scope/controls were frozen in CAMPAIGN_LOG before execution.

## Query, conventions and what was computed

`design_inputs.json` freezes official H1/L1/V1 arm/location decimals and source
SHA, GCN21529 nominal sky and GWOSC time. The code actually re-parsed and matched
every frozen constant against the fetched official header. No renormalization
or forced arm orthogonality was applied; maximum squared-norm departure is
9.31e-12 and largest arm dot product1.91e-7. Published decimals are not exact
metrology. Arm lengths are twice the explicitly named midpoint constants.

Nominal query: RA197.450370833deg, Dec-23.381486111deg, GPS1187008882.43,
UTC2017-08-17T12:41:04.430. Interpret the optical coordinates as an ICRS-like
distant-source direction and identify it with GCRS for this static design.
This is supplied query/conventional astrometry, not a precision counterpart
position or a derivation of photon/GW observation. The circular alone does
not supply the coordinate covariance/frame. No source distance or inclination
is needed for this rank calculation; source association remains conditional.

For celestial unit n toward the source, p=(-sinRA,cosRA,0), q=n cross p,
rotate all three by ERFA c2t06a (IAU2006/2000A GCRS-to-ITRS). Offline IERS-B
gives historical, not extrapolated, UT1-UTC0.340825231s and polar motion;
full two-part dates, rotation/basis, file hash and versions are saved in output.
This includes precession/nutation/rotation/polar motion, not a complete
barycentric/geocentric aberration or instrument-transfer model. More precise
astrometry and response belong to any eventual precision test. Finite offsets
below are diagnostic queries, not measured uncertainty bounds.

Plane phase t+n.r/c_E fixes arrival offset tau_I=-n.r_I/c_E, with calibrated
c_E=299792458m/s. For aligned channels d_I(t)=d_local,I(t+tau_I), construct
F from D_I:eplus/ecross. Our convention yields offsets H1+18.826632ms,
L1+15.560841ms,V1-6.330544ms relative to geocenter. These are design delays,
not measured arrivals. A convention-consistent polarization rotation changes
the displayed columns but not their span or the unused contrast.

## Result and sensitivity meaning

The real long-wavelength matrix, rounded for display, is

    F = [ 0.076377   0.887150 ]  H1
        [ 0.132950  -0.741236 ]  L1
        [-0.157401   0.257365 ]  V1.

At full saved precision its singular values are1.185937 and0.211048,
rank2 and unweighted condition number5.61929. Thus there is ONE algebraic
unused contrast for two free tensor functions. A unit null vector is
q=(0.329437,0.636443,0.697433), original max|q^T F|=2.78e-17.
This tiny floating residual verifies arithmetic, not the real instrument.

Using H1/L1 to infer the two unrestricted waveform values gives the held-out
Virgo signal prediction

    d_V,signal = -0.472356 d_H,signal -0.912551 d_L,signal,
    r_V = d_V +0.472356 d_H +0.912551 d_L.

All channels here are consistently aligned and calibrated. H/L training
condition number7.66035 and inverse operator norm6.62449 quantify geometric
noise amplification. The other two possible holdouts are rescalings of this
SAME relation, not two additional independent tests. Their coefficients and
original residuals are saved, not selected by looking at strain outcomes.

For a declared comparator with centered, uncorrelated noise and equal H/L
standard deviation sigma, the residual standard deviation is

    sd(r_V) = sqrt(sigma_V² + (0.472356²+0.912551²) sigma²).

At sigma_V/sigma=1,3,10 it is1.43383,3.17110,10.05265 times sigma. These
are NOT measured PSD ratios. Actual correlated/complex errors use CO1's
centered b C b^dagger, plus a separately propagated bias. The noise-weighted
response-matrix condition numbers5.619,7.288,7.624 do not by themselves give
a test's power. A response component lying in col(F) remains invisible; an
alternative outside it is tested only in its q-projection and only above
justified error. No source inclination/ellipse, distance or binary phase was
selected to improve the contrast. Published weak Virgo signal motivates
caution but is not used as a substitute for a measured error calculation.

In27 frozen sky/time diagnostic cases (RA/Dec offsets0,+/-0.01degree;
time0,-10,-100s), rank remains2 and conditions range5.61413–5.77817.
At fixed nominal sky, ||F(t-10s)-F(t)||_2=0.001074 and the100s change is
0.010743. Same-time sampled sky change reaches0.0003223. These finite values
show why a frozen merger matrix is not automatically a precision100s-window
response; they are not supremum bounds. At100Hz the arm parameter2pi fL/c
is~0.00837 for LIGO and~0.00629 for Virgo; at500Hz~0.04187/~0.03144.
Compute/bound actual response error before an empirical null comparison.

## Data route and what processing does NOT yet establish

Use the [official O2 archive](https://gwosc.org/o2_details/) as the proposed
next route: H/L C02 and Virgo Repro2A, with matched
[O2 calibration uncertainty documentation](https://dcc.ligo.org/public/0177/T2100313/003/README).
The special original cleaned GW170817 C00/Repro1A files are a different
product and are not silently assigned those uncertainties. The
[GWTC-1 v3 event page](https://gwosc.org/eventapi/html/GWTC-1-confident/GW170817/v3/)
explicitly retains the L1 glitch. Public metadata is sufficient to nominate
the archival route, not certify an unexamined file or reject all processing.

A pre-glitch window with explicit filter support can avoid dependence on the
special glitch-subtraction model. Off-source error estimation, witness-noise
subtraction's signal-transfer effects, quality/injection masks, timing and
release headers still require a bounded check. Hourly median/+/-1sigma
calibration records are not deterministic bounds or a full joint covariance.
The archive's use of established calibration physics is permissible as a
supplied measurement model, not a reason for automatic rejection. Conversely,
neither the archive nor the published template-based polarization odds prove
that this particular free-waveform statistic survives preprocessing unchanged.

No new external reply is needed to begin that finite check. Do not demand every
servo sample: matched documentation, signal-injection transfer checks and a
justified residual/error model can suffice. Stop/narrow if those do not support
the intended claim; do not turn a GOCE-like exhaustive hunt into a prerequisite.

## Limits and proposed return

This supplies a practical additional curvature channel and an explicit unused
relation in a declared tensor plane-wave measurement class. It does not join
the laboratory clock datum and this wave to reconstruct one global metric.
Weyl histories/source data and unmeasured components remain free. It is a
consistency test shared with established metric physics, not a distinctively
UDT prediction or generic all-UDT polarization theorem. No additional physical
premise has been adopted or shown necessary; supplied instrument laws remain
visible. Emergence is neither solved nor made a prerequisite.

Recommended continuation is the separately proposed matched-release,
fixed-window conditional strain test in NEXT_WORK_ORDER.md, with an early
error/power gate and an untouched reserved contrast until its frozen analysis
and checks receive fresh review. Current authorization stops at this reviewed
design/recommendation; no arrays or empirical fitting have been undertaken.
