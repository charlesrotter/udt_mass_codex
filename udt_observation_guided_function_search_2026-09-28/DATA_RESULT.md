# FDATA1 — empirical brightness functions

Status: DRAFT, construction checks complete, awaiting the campaign's fresh
separate-context review. All fitted functions remain empirical and unselected.
No native UDT law, absolute length, physical separation, local GR bound or
asymptotic completion is established.

## What the data lane learned

The public Pantheon+ processed magnitudes support a smooth finite-range
brightness–redshift curve. A useful compact description is

\[
x=\log(1+z_{HD}),\quad
F_2(x)=x\exp(0.24480409x-0.15933069x^2),
\]
\[
m_{\rm pred}=23.80411734+5\log_{10}[(1+z_{HEL})F_2(x)].
\]

The shape coefficients have conditional 1-sigma uncertainties 0.03404020 and
0.05003719, correlation -0.89257. The magnitude offset has uncertainty
0.00942870. Original full-covariance chi-square is 1209.588124 for 1368 degrees
of freedom. This is a compact empirical lead, not a selected model: the flexible
spline has almost the same AICc, and the conventional external comparison has
slightly lower AICc. A cubic term adds little. The repaired same-release
validation score for F2 is 294.804660 for 304 validation rows, conditional on
training data and covariance. This is an exposed consistency check, not blind
confirmation or an independent survey.

The fitted shape does not establish physical separation as a function of
redshift. Under the declared conventional optical interpretation it supplies a
relative brightness distance and a conditional relative angular-distance curve.
Native event/path assignment and the physical optical interface remain open.
The F2 formula must not be extended to an asymptotic law: its negative quadratic
log term eventually turns even its extrapolated luminosity distance over.
No such extrapolation is admitted by this result.

## Measurement contract and preserved history

[FREEZE.md](data/FREEZE.md) was sealed at 2026-09-28 11:51:54 UTC before this
campaign downloaded observational rows. Published summaries, historical fits and
schema were already exposed. Download completed at 11:52:01 UTC. Parent startup
is attributed to LAUNCH.json; this context independently verified grok at
2dcec4fc and read the assigned instructions and source caveats. The actual
source hashes read here are in [SOURCE_MANIFEST.json](data/SOURCE_MANIFEST.json).
Current program status was being updated by the parent during launch; the
manifest records the bytes present at download, without changing source grades.

The pinned public [Pantheon+ release](https://github.com/PantheonPlusSH0ES/DataRelease/tree/c447f0fea703fcd0fff57de5000947b5ca81286b)
provides standardized `m_b_corr`, `zHD`, `zHEL`, and full STAT+SYS covariance.
Primary selection is `IS_CALIBRATOR==0` and `zHD>0.023`, without clipping or
brightness-based cuts: 1,371 light-curve rows, 1,309 CID keys, spanning
0.02303–2.26137. These are processed quantities dependent on source
standardization, selection simulations, calibration and velocity corrections;
some covariance redshift terms use a fiducial cosmology. The measurement-method
dependencies are described by the [Pantheon+ analysis](https://arxiv.org/html/2202.04077v2).

No Cepheid distance, `MU_SH0ES`, H0, BAO target or quasar outcome entered these
fits. Write the conventional amplitude relation as

\[
D_{L,obs}=L(1+z_{HEL})F(x),\qquad
A=M_B+25+5\log_{10}(L/{\rm Mpc}).
\]

The fitted A cannot separate intrinsic standardized brightness from length L.
No absolute distance follows from c_E alone. The public likelihood's frame
convention is `D_L,obs=(1+zHEL)(1+zHD)D_A,HD`, giving
`D_A,HD=L F(x)/(1+zHD)`. Invoking distance duality with actual heliocentric
redshift instead gives `D_A,obs=D_L,obs/(1+zHEL)^2`; these frame objects must not
be equated silently. A reported curve with `z=zHD` uses
`D_L,HD/L=(1+z)F(x)` and `D_A,HD/L=F(x)/(1+z)`.
Neither distance is automatically physical radial separation or projective chi.
x is observed log redshift, not isolated positional depth for a general query.

G277/G279/G281's distinctions survive: scale calibration and empirical area
reconstruction do not select a native kernel/history. ZDR1's conventional
light-transfer and source/duration requirements survive. No duration was
independently remeasured, and deriving angular distance from these same
brightness data supplies no independent duality test.

## Six frozen families and coefficients

For F0–F3, `F=x exp(sum a_j*x^j)` with free magnitude offset A. All coefficients
are dimensionless except A, expressed in magnitudes. Errors are 1-sigma under
the supplied Gaussian covariance, without chi-square rescaling.

| Family | A | a1 | a2 | a3 |
|---|---:|---:|---:|---:|
| F0 | 23.882193 ± 0.004327 | fixed 0 | fixed 0 | fixed 0 |
| F1 | 23.821863 ± 0.007606 | 0.148056 ± 0.015349 | fixed 0 | fixed 0 |
| F2 | 23.804117 ± 0.009429 | 0.244804 ± 0.034040 | -0.159331 ± 0.050037 | fixed 0 |
| F3 | 23.801896 ± 0.011527 | 0.263113 ± 0.064378 | -0.220517 ± 0.189337 | 0.049168 ± 0.146737 |

F4 is a natural cubic spline of `q(x)=A+(5/ln10)ln(F/x)`. The entire correction
is represented by the following cardinal magnitudes; no separate intercept is
fitted. Its normalization is arbitrary, so compare relative F values. The
natural boundary condition is imposed, not measured.

| z knot | q | 1-sigma |
|---:|---:|---:|
| 0.001 | 23.818151 | 0.015212 |
| 0.1 | 23.840463 | 0.008504 |
| 0.3 | 23.930046 | 0.008121 |
| 0.6 | 23.952080 | 0.015358 |
| 1.0 | 24.057305 | 0.037932 |
| 2.3 | 23.904893 | 0.139772 |

F5 is the explicitly **external** flat-Lambda-CDM comparison,

\[
F_5(x)=\int_0^{e^x-1}\frac{dt}{\sqrt{\Omega(1+t)^3+1-\Omega}},
\quad \Omega=0.32797750\pm0.01859266,
\]

with `A=23.80211622±0.00750991`. It is not imported as UDT dynamics. Its error
uses a local Jacobian approximation. Full parameter covariance/correlation for
all six families is preserved in [full_fits.json](data/results/full_fits.json).
For F2 specifically, the covariance in `[A,a1,a2]` order is

```text
[[ 8.8900417495e-5, -2.6531904215e-4,  2.7884968369e-4],
 [-2.6531904215e-4,  1.1587351740e-3, -1.5202992065e-3],
 [ 2.7884968369e-4, -1.5202992065e-3,  2.5037206478e-3]]
```

## Original residuals, complexity and validation

The common covariance likelihood constant is omitted from AICc/BIC; rows and
covariance are identical across this table. Repaired validation fits use only
development rows and do not retune on validation outcomes.

| Family | Parameters | Original chi-square / dof | AICc | BIC | Repaired conditional validation chi-square / rows |
|---|---:|---:|---:|---:|---:|
| F0 | 1 | 1312.775 / 1370 | 1314.778 | 1319.998 | 307.423 / 304 |
| F1 | 2 | 1219.728 / 1369 | 1223.736 | 1234.174 | 293.953 / 304 |
| F2 | 3 | 1209.588 / 1368 | 1215.606 | 1231.258 | 294.805 / 304 |
| F3 | 4 | 1209.476 / 1367 | 1217.505 | 1238.369 | 294.828 / 304 |
| F4 | 6 | 1203.588 / 1365 | 1215.649 | 1246.928 | 291.422 / 304 |
| F5 external | 2 | 1209.696 / 1369 | 1213.704 | 1224.142 | 294.982 / 304 |

F0 is strongly disfavored relative to F1 inside the supplied nested Gaussian
models (delta chi-square 93.047 for one parameter), but its absolute chi-square
does not fail an upper-tail test. This does not reject a UDT class. F1→F2 gains
10.139; F2→F3 gains only 0.112. These exposed exploratory comparisons are not
pristine discovery significances. More flexible families have unusually small
full-data chi-square: F2's lower-tail probability is 0.000841. That warning
about likelihood/covariance calibration is retained, not recast as exceptionally
strong confirmation. No errors were rescaled to make reduced chi-square one.

The original split grouped identical CID using `SHA256(CID) mod5`; it had
1,070 development and 301 validation rows. A finite post-fit identity diagnostic
found five possible primary alias pairs with different CID but matching sky,
peak date and redshift. The source-grouping repair was separately frozen in
[ALIAS_REPAIR_FREEZE.md](data/ALIAS_REPAIR_FREEZE.md) before its scores were
computed. It unions those possible aliases conservatively, hashes each group's
lexicographically smallest CID, and moves three rows. The repaired split has
1,067 development / 304 validation rows in 1,304 conservative groups overall.
All primary fit results remain unchanged. This finite grouping check is not a
complete physical-source identity census.

Both original and repaired checks include cross-partition covariance and
training-parameter uncertainty:

```text
e = rV - CVT CTT^-1 rT
S = CVV - CVT CTT^-1 CTV
B = XV - CVT CTT^-1 XT
Vpred = S + B Cov(betaT) B.T
score = e.T solve(Vpred,e)
```

This is exact for these linear Gaussian families F0–F4; F5 uses the declared
local-Jacobian approximation. Repaired upper-tail probabilities range from
0.434 to 0.688. Original checks are preserved in
[validation.json](data/results/validation.json); repaired checks and old/new
comparison are in [alias_validation](data/alias_validation/summary.json).
No external DES fit was added; no blind, independent-survey claim is made.
The parent separately owns any added DESI/quasar comparisons.

## Shape, derivatives, and representation limits

Under the conventional frame-corrected optical interface, normalized at z=.1:

| z | F2 D_L(z)/D_L(.1) | F2 D_A(z)/D_A(.1) | 1-sigma log-ratio error | F4 D_L ratio | F4 log-ratio error |
|---:|---:|---:|---:|---:|---:|
| .05 | .483624 | .530780 | .001293 | .485500 | .003602 |
| .3 | 3.356929 | 2.403482 | .003305 | 3.390258 | .005658 |
| .6 | 7.600959 | 3.592641 | .005804 | 7.551143 | .007568 |
| 1 | 14.199292 | 4.295286 | .010658 | 14.611404 | .018616 |
| 2 | 33.205795 | 4.464335 | .033237 | 33.284429 | .046936 |

These are family-conditional pointwise errors, not total uncertainty over
arbitrary functions. The apparently precise F2 derivative comes from restricting
the family. In F2,
`d ln F/dx=1/x+a1+2a2*x` and `d² ln F/dx²=-1/x²+2a2`.
For F4 use the spline derivative of q divided by `5/ln10`. Full derivatives and
errors are saved in [anchor_curves.tsv](data/results/anchor_curves.tsv) and
[curves.tsv](data/results/curves.tsv). In particular, at z=2 F2 gives
`d ln F/dx=.80496±.08103`, whereas F4 gives `.63335±.20446`.
No total-shape precision claim follows from either single representation.

Predeclared cuts and spline resolutions were all retained. On the exact common
sample domain .05018–.97423, normalized at z=.1, changing the lower cut to .01
or .05 moves F2 relative shape by at most 0.162% or 0.359%; removing all z>=1
moves it by up to 2.414%. Coarse/fine splines move the primary F4 relative shape
by up to 2.914% / 0.682%; derivative variation is larger. Coarse/primary/fine
spline AICc values are 1216.803 / 1215.649 / 1219.973. No finer-resolution
convergence claim or resolution-independent scale is made. The original
sensitivity anchor table contains z=.05 or1 just outside some cut samples;
[sensitivity_summary.json](data/results/sensitivity_summary.json) explicitly
flags that and supplies comparisons strictly inside the common data range.

The main standalone figure is
[empirical_curves_residuals.png](data/results/empirical_curves_residuals.png)
([PDF](data/results/empirical_curves_residuals.pdf)). The
[spline derivative figure](data/results/spline_derivative_sensitivity.png)
([PDF](data/results/spline_derivative_sensitivity.pdf)) displays the loss of
derivative precision and the imposed endpoint condition. Plots use at most
400 points; the fit itself uses all selected rows and covariance, not binned
points or plotted error bars.

## Verification and release caveats

The covariance is positive definite on primary rows: eigenvalues
0.0052029221–2.1493223381, condition number 413.10. Whitened design condition
numbers are modest (largest primary value 62.22 for F3). Original quadratic
residuals and whitened norms agree within 4.6e-13. The full release's maximum
asymmetry is 3e-8; the primary submatrix is exactly symmetric in the downloaded
precision, so upper/lower/symmetric sensitivity gives identical primary fits.

[independent_anchor.py](data/independent_anchor.py) re-parses saved release bytes
and uses direct symmetric linear solves, separately constructed piecewise
polynomial splines, and adaptive quadrature. It does not import fitter routines.
All six original chi-square values agree within 3.2e-12; original F2 validation
agrees within 5.7e-12. A second direct anchor reproduces repaired F2 validation
within 3.5e-13. These are **same-context, different-implementation anchors**,
not a fresh-context reviewer or different-model claim. Results are in
[independent_anchor.json](data/results/independent_anchor.json).

The schema check found two real release-description caveats. First, the
`m_b_corr_err_DIAG` column is not numerically the square root of the covariance
diagonal: the primary maximum difference is .21147 mag, with median signed
`sqrt(Cii)-table` difference -.05639 mag. The release owner instructs users to
fit the full covariance; the discrepancy's complete explanation remains
unresolved in the saved [issue 6](https://github.com/PantheonPlusSH0ES/DataRelease/issues/6)
and [issue 13](https://github.com/PantheonPlusSH0ES/DataRelease/issues/13) material.
The table errors were never used in fitting or substituted for C. Second,
the file has 1,543 CID keys versus the paper's 1,550-source headline, also raised
in [issue 10](https://github.com/PantheonPlusSH0ES/DataRelease/issues/10).
This report gives observed row/key counts and the limited alias diagnostic,
without asserting a repaired physical-source census. These checks do not
validate raw photometry, calibration, covariance truth or source/optical physics.

CPU only, float64, two threads and a 3 GiB address-space cap; the principal
fit/sensitivity/plot run took 2.53 seconds and peaked at 393,080 KiB RSS. Every
fit/check subprocess had a 600-second timeout. Downloads were about 33.9 MB plus
small issue metadata; compressed covariance preserves exact original bytes.
All fitted and diagnostic outcomes, including the initial grouping limitation,
are retained. Exact commands and runtime notes are in [COMMANDS.md](data/COMMANDS.md).

## Return to the geometry lane

The empirical clue is a modest curved correction to the positive reduced
brightness shape over a measured finite range, with explicit covariance and
derivative limitations. A native construction must supply a complete physical
clock/beam query and its relation to these observables before it can inherit
these constraints. Substituting F2/F4 into a free metric function leaves that
function observationally supplied. No whole-theory rejection, asymptotic
selection, independent physical separation or native derivation follows here.
