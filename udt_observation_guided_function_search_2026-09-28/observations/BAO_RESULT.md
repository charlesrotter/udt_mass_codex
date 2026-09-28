# Conditional galaxy-clustering comparison

Construction result, pending the campaign's fresh adversarial review. These are
consistency checks of supplied metric and measurement interfaces, not UDT
predictions or a calibration of physical separation.

The six supernova-only functions were compared with the public DESI DR2
anisotropic BAO ratios without fitting any parameter to BAO. In a spatially flat
homogeneous metric with the supplied comoving observers and conventional
optical/ruler interpretation,

    x = ln(1+z), F = h0 D_M, H/h0 = exp(x)/F',
    D_M/D_H = exp(x) F/F'.

Here T=c_E tau has length units, H=d ln(a)/dT, h0=H(today), and D_H=1/H.
This derivation uses null incidence and beam geometry, not an Einstein or
Friedmann equation. It still supplies an expanding observer congruence, the
shape F, and a conventional comoving ruler. It therefore does not establish
UDT's intended native positional explanation without required Hubble expansion.
The geometry lane independently derived the relation before BAO-target
exposure; its curved counterpart has an extra sqrt(1-kappa F^2) factor on the
increasing-distance branch. Only the declared flat comparison was calculated.

## Data and estimator

The [official product description](https://data.desi.lbl.gov/public/papers/y3/bao-cosmo-params/README.html)
links the [released likelihood files](https://github.com/CobayaSampler/bao_data/tree/bb0c1c9009dc76d1391300e169e8df38fd1096db/desi_bao_dr2).
The pinned combined mean/covariance files contain 13 entries. The isotropic
BGS D_V datum is excluded; it cannot independently supply D_M/D_H. Six
anisotropic pairs occur at z=.510,.706,.934,1.321,1.484,2.33. The last is above
the SNe maximum 2.26137 and is excluded from the headline diagnostic.
The [DESI analysis](https://arxiv.org/html/2503.14738v3) describes the fiducial
templates and reconstruction behind these compressed measurements. The ratio
cancels the numerical sound-horizon size; it does not cancel that interface.

Use the full ratio Jacobian on the released covariance, and the full SNe
coefficient covariance on the prediction Jacobian. Sum the resulting matrices
under an explicit, unverified zero cross-probe covariance assumption. The
reported residual quadratic forms use five points and are approximate
consistency diagnostics, not calibrated chi-square significances or a ranking
of UDT against other physical theories.

| SNe-only family | Five-point quadratic diagnostic | Interpretation |
|---|---:|---|
| F0, log-redshift baseline | 9.2384 | Exact shape, supplied interface |
| F1, one shape coefficient | 31.3535 | Greater discrepancy in this comparison |
| F2, two shape coefficients | 4.5186 | Useful finite-range empirical lead |
| F3, three shape coefficients | 4.3117 | Similar finite-range agreement |
| F4, natural spline | withheld | Prediction linearization failed its frozen diagnostic |
| F5, external flat-Lambda-CDM shape | 7.1114 | Conventional comparison, not native UDT |

For F2 the observed ratios are .62149,.89182,1.22301,1.94701,2.38058;
the unchanged SNe fit predicts .59448,.87635,1.24717,1.99374,2.35691.
Covariance, residuals and all six predictions are in
[RESULT.json](comparison_checked/RESULT.json). No BAO outcome was used to
retune the SNe families or choose a replacement coefficient.

## Approximation checks and retained limitations

The frozen correlated Gaussian ratio diagnostic used 100,000 draws, seed
9282026. All denominators were positive; variance ratios to the linear result
were 1.001–1.017, with mean shifts below .045 linear standard deviations.
The SNe coefficient diagnostic used 20,000 draws, seed 9282027, without
discarding invalid or extreme draws. At the five included points, F0/F1/F2/F3/F5
passed the predeclared positivity, variance and bias diagnostics. F4's variance
ratio was 1.24686 at z=1.484, exceeding the 20% tolerance, so its statistic is
withheld. These finite Monte Carlo checks assess local approximations; they do
not certify a Gaussian ratio law or its far tails.

At the excluded z=2.33 point F3/F4 have severe nonlinear uncertainty; F3's
sample variance ratio is about 7,767. Their extrapolated local covariance bands
are not reliable uncertainty statements. The saved comparison figure shows
point estimates and local linear bands; its F4 shading is diagnostic only,
including inside the fitted range where the above check failed. Read it with
this limitation; the square beyond the vertical domain marker is extrapolation.

The first implementation run stopped on a finite-difference check of the
analytic F4 parameter Jacobian. The step-convergence diagnostic supported a
smaller step, with the original 2e-7 tolerance unchanged. The checked step gives
3.29e-9 relative discrepancy. INITIAL_compare_bao.py, both run captures and
F4_JACOBIAN_DIAGNOSTIC.json preserve the failure and bounded correction. No
observational model, fit or residual changed. The checked run exited zero in
0.737 seconds under the 2-thread / 2-GiB / 600-second limits.

[BAO_COMPARISON_FREEZE.md](BAO_COMPARISON_FREEZE.md) records exposure: public
paper summaries were already known; the covariance-quality refinement was
made after BAO means were read but before SNe coefficients or comparison
residuals. This is an exposed cross-probe consistency check, not blind
confirmation. Quasar variability was assessed at the methods/interface level
only; [INTERFACE_MAP.md](INTERFACE_MAP.md) explains why no independent quasar
distance or duration fit is claimed.

The result contributes an additional shape-and-slope constraint under a named
geometry. It neither selects that geometry natively nor proves local GR
correspondence or a global unreachable asymptote.
