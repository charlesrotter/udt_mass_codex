# Empirical reconstruction freeze — FDATA1

Status: frozen before this campaign downloads or reads observational rows or fits
fresh outcomes. DRAFT, empirical controls only, not a native UDT law. Parent
startup is attributed to LAUNCH.json. This scoped context independently read
AGENTS, WORK_ORDER, LAUNCH, CAMPAIGN_LOG, CURRENT_RESEARCH_PROGRAM, the required
CLAUDE sections, no-shortcuts/completeness-map/solver-first skills, exact
G277/G279/G281 rows and their LAY_REPORTs, and ZDR1 DECISION_BRIEF. It independently
verified branch grok and HEAD 2dcec4fcf54c418543cc41c464432cb6028aa697;
parent-owned WORK_ORDER edits and preexisting untracked work are preserved.

## Scope, exposure, and sources

Question: which of six explicitly supplied positive brightness-distance shapes
describes processed Pantheon+ standardized magnitudes on the declared redshift
range, with the release's full covariance? This estimates shape, slope/curvature,
and an arbitrary magnitude offset. It cannot identify physical separation,
isolated positional depth, native dynamics, local GR correspondence, or an
asymptotic completion. All family and smoothness restrictions are
`free-and-explored`. Conventional optical interpretation is `IMPORTED`,
conditionally used, not UDT-derived. Standardization/calibration are external
observational input. No value is claimed `pinned-by-THEORY` from UDT.

Historical fits and G277/G279/G281 outcomes, public paper summaries and schema
have been exposed. This campaign has not yet seen raw target rows. The
predeclared split below is a reproducibility/consistency test, not pristine
blind confirmation; full-sample estimates follow it. No DES independence claim.

Release repository: https://github.com/PantheonPlusSH0ES/DataRelease
Pinned public commit: c447f0fea703fcd0fff57de5000947b5ca81286b (queried by GitHub
API before rows). Paths under Pantheon+_Data/4_DISTANCES_AND_COVAR:
Pantheon+SH0ES.dat and Pantheon+SH0ES_STAT+SYS.cov. Save README and the public
5_COSMOLOGY/cosmosis_likelihoods/Pantheon+SH0ES_cosmosis_likelihood.py.
Methods source: https://arxiv.org/html/2202.04077v2 . Its outcomes are exposed.
Metadata-only network read initially failed sandbox DNS; allowed public network
escalation succeeded. README.md gave 404; actual README was retrieved. No fit
failed or new data row was seen during these checks.

## Measurement contract and sample

Use m_b_corr, zHD (CMB/peculiar-velocity corrected), zHEL and IS_CALIBRATOR.
Primary: all release rows with IS_CALIBRATOR==0 and zHD>0.023, finite required
values; retain all duplicate light curves with their full covariance. No
outlier clipping, brightness-driven exclusions, weighting adjustments, or
uncertainty rescaling. Stop on malformed rows, dimension mismatch or nonpositive
covariance; record rather than repair silently. The zHD cut is methodological,
not a physical onset. No upper cut for primary.

Dependence retained: SALT2/Tripp standardization, source populations and dust,
selection simulations, photometric cross-calibration, peculiar velocities,
redshift frames, intrinsic scatter and the release's systematic model. Some
redshift covariance components use a fiducial cosmology. Do not re-add redshift
errors already propagated into that covariance. This is a conditional fit to
processed products, not raw redshift/flux geometry free of those assumptions.
Do not use MU_SH0ES, CEPH_DIST or an assumed H0 in this run. An apparent-magnitude
offset does not establish an absolute length; c_E alone supplies none.

Set x=ln(1+zHD), k=5/ln(10). Fit

    m_pred = A + k ln[(1+zHEL) F(x)].

F is a positive dimensionless reduced brightness-distance shape; A absorbs
absolute standardized luminosity and scale. In conventional units this would
mean D_L,obs = L (1+zHEL) F(x), A=M_B+25+5log10(L/Mpc), so M_B and L cannot be
separated here. The public likelihood uses
D_L,obs=(1+zHEL)(1+zHD) D_A,HD; hence its corrected D_A,HD=L F(x)/(1+zHD).
If separately invoking transparent metric light propagation and distance
duality with actual heliocentric redshift, D_A,obs=D_L,obs/(1+zHEL)^2 instead.
These frame objects must not be silently equated. Neither angular distance is
physical radial separation or projective chi. For a frame-corrected curve at
z=zHD, use D_L,HD/L=(1+z)F(ln(1+z)), D_A,HD/L=F/(1+z).

This lane does not measure durations independently, validate transparent
transfer, or isolate positional from Doppler/gravitational redshift. x is an
observed log redshift, not the general query's native pair depth.

## Exactly six families

F0: F(x)=x, with A free (one parameter).
F1: F(x)=x exp(a1*x), with A,a1 free (two).
F2: F(x)=x exp(a1*x+a2*x^2), with A,a1,a2 free (three).
F3: F(x)=x exp(a1*x+a2*x^2+a3*x^3), with A,a1,a2,a3 free (four).
F4: natural cubic spline for the entire additive magnitude correction
q(x)=A+k ln[F(x)/x], with cardinal values at z=[.001,.1,.3,.6,1,2.3]
(x=ln(1+z)); six free cardinal magnitudes, natural end conditions, no smoothing
penalty, no other intercept. Only relative F shape is identifiable. F4 is the
flexible baseline, not a selected family. Do not extrapolate it outside sampled
redshifts or treat natural endpoint curvature as evidence.
F5: external flat-Lambda-CDM benchmark,
F(x)=integral_0^(exp(x)-1) [Omega*(1+t)^3+1-Omega]^-1/2 dt,
with A free and 0<=Omega<=1 (two). This equation is an imported comparison,
not UDT dynamics, not an interpretation adopted for F0--F4.

No candidate imposes the desired extreme-separation asymptote. F0--F3's
normalization F/x->1 is a coordinate choice absorbed by A and extrapolative
outside data; it does not supply a physical local Hubble law. The finite list
does not classify all shapes.

## Covariance, estimators, checks and comparison

Read raw NxN covariance in release row order; use C=(Craw+Craw.T)/2 and retain
raw asymmetry diagnostics. Fit F0--F4 by Cholesky whitening plus QR/SVD least
squares, float64. Report original r.T solve(C,r), residuals, n, k, rank,
condition numbers, score/normal-equation residual, chi-square survival and lower
tail, reduced chi-square, AICc and BIC. Complexity scores compare primary rows
and covariance only. Gaussian likelihood/covariance are taken as supplied;
goodness of fit is conditional and low chi-square must not be advertised as
model confirmation. Parameter covariance is the inverse GLS information, no
reduced-chi-square scaling. Confidence bands are pointwise 68/95% Gaussian
bands on log distance; no simultaneous-band claim. F1--F3 report covariance and
correlation, relative D_L and D_A anchored at z=.1, and analytic slope/curvature
uncertainties. F4 uses its analytic spline derivatives and exact linear error
propagation. Endpoint derivatives are particularly representation-sensitive.

F5: bounded scalar minimize of profiled original chi-square, atol in Omega
1e-10, Gaussian-Legendre 64 point integration; re-evaluate at 128 points and
independent adaptive quadrature at z=.1,.5,1,2. Parameter errors from full
local Jacobian GLS information; mark approximation and any bound contact.

For each family, development rows satisfy
int(SHA256(UTF8(CID)).hexdigest(),16) mod 5 !=0; validation rows use ==0.
All repeated CID rows remain in one partition. Preserve row indices/split.
Fit development only, then no-retune validation with covariance cross-blocks:
e = r_V - C_VT C_TT^-1 r_T;
S = C_VV-C_VT C_TT^-1 C_TV;
B = X_V-C_VT C_TT^-1 X_T;
Vpred=S+B Cov(beta_T) B.T.
Report e.T Vpred^-1 e, validation count and conditional predictive log score;
linear-family predictive Gaussian errors are exact under this statistical
model. F5 uses the local-Jacobian parameter-uncertainty approximation and says
so. Never call rows independent merely because CID grouping is enforced.
After this consistency comparison, refit each frozen family to all primary
rows; give full-data estimates separately.

Predeclared sensitivity: all six families at zHD>.01 and zHD>.05, and primary
zHD<1; F0--F4 at primary covariance built from raw upper or lower triangles;
F4 coarser knots [.001,.3,.6,2.3] and finer knots
[.001,.05,.1,.2,.3,.45,.6,1,2.3]. These are same-family representation checks,
not new families. Report them all without choosing preferred cut/resolution
after outcomes. Curve comparisons use common overlap [.05,1] or actual common
sample range as appropriate, all relative to z=.1. No sensitive absolute scale
is attached. Independent anchor: load saved artifacts in separate code using
direct dense symmetric linear solves for GLS and original chi-square, plus
independent quadrature for F5; same-context different implementation, not fresh
review. Parent's actual fresh reviewer is a separate later stage.

Mismatch diagnostic is finite: verify release shapes, row selection and
covariance ordering; compare original quadratic and whitened scores; check
rank/conditioning and independent solves; evaluate declared cut and spline
sensitivity. Do not invent mechanism or fit rescue after failed family.

## Resources and artifacts

CPU only, maximum two BLAS/OpenMP threads, maximum 3 GiB per process, no GPU.
Each fit/check subprocess has 600 s limit; download limit 512 MiB. Use the
1701-row release rather than a new grid solve; plot grids are at most 500 points.
Save scripts, exact commands, stdout/stderr, package versions, source/data
SHA-256, selected indices, parameter covariances, residual and curve tables,
original scores, validation diagnostics and standalone PNG/PDF figures.
Do not overwrite historical artifacts. All outputs DRAFT pending review.
The campaign hard stop is 2026-09-28 17:45:32 UTC; this lane targets an early
checkpoint and yields before that. No commit or live/registry/CANON edits here.
