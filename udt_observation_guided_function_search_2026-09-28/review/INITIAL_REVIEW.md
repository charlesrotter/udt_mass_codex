# Initial adversarial review — OFS1

2026-09-28. Reviewer `/root/function_adversarial_review`. Scientific content
survives as a conditional/empirical checkpoint, with two required precision
repairs before final `VERIFIED-WITH-CAVEATS` closeout. No native function,
physical premise, asymptotic law, source response or scientific promotion is
established. The initial integrated candidate and numerical evidence are not
refuted. This is a fresh separate-context review, not different-model review.

## Snapshot and independence

Independently verified branch grok and HEAD
`2dcec4fcf54c418543cc41c464432cb6028aa697`; dirt preserved in START_STATUS.txt.
Parent startup/fetch/pull attributed, not independently rerun by this scoped
reviewer. The source-first frame was sealed at 12:10:43 UTC before current
candidate, proofs, code or numerical outputs. Prior source formulas/verdicts,
current freezes and the task's high-level construction description were exposed.
The raw F2 implementation was written before reading construction fitting code
or numerical fit outputs. Source-first frame/pins record exact exposure.

CONSTRUCTION_MANIFEST.json SHA-256
`930e1c4fe82c14d9dba5920285fdc97809ad22ae87828fb056ec17d3025aa176`
was independently checked: 132 files, no hash/size mismatch. Initial candidate
hash `129b01123871ca4f896d0ae2c2ddbf571fd084d3af2a7120bc49e2728663d1d2`.
Runtime exact model identity is unattested; inherited model with no override.
Independent implementation and analytic argument are present; different-model
independence is UNTESTED. Checksums establish correspondence, not chronology
or truth. Parent audit run is attributed; its saved capture was inspected and
records exit 0, 406.503 seconds, empty stderr and PASS stdout. No full audit
was duplicated here.

## Required repairs

**R1 — model-comparison qualification.** DATA_RESULT and the initial candidate
use the conventional AICc formula without identifying that the extra
`2k(k+1)/(n-k-1)` term is not an exact finite-sample correction for this fixed,
known-covariance linear Gaussian problem. Whitening reduces it to ordinary
known-variance Gaussian regression; the fitted-mean optimism correction is
exactly `2k` for F0–F4. BIC likewise remains a convention/asymptotic diagnostic,
not a supplied model probability. Defect: precision of score interpretation,
not computation or fit. Survivor: all coefficients, chi-squares, residuals,
covariance, validation and qualitative near-equivalence of the compact curves.
Smallest repair: label AICc/BIC as conventional heuristic complexity summaries
here, add ordinary AIC if useful, and avoid exact finite-sample/evidence claims.
No refit, sample change, formula retuning or new model is warranted.

**R2 — standalone BAO figure uncertainty.** The initial standalone PNG/PDF
shades F4 although its in-domain Gaussian approximation failed. The figure
does not label that failure or the level/local meaning of either shaded band.
BAO_RESULT's prose caveat is correct but does not travel with the standalone
figure. Defect: uncertainty presentation, not the already-withheld F4 statistic.
Survivor: point predictions and the valid reported five-point diagnostics.
Smallest repair: retain the initial artifact and provide a corrected standalone
plot with unsupported F4 uncertainty removed or conspicuously marked diagnostic;
label any F2 local error indication and restrict it to checked scope. Preserve
the extrapolation distinction and no-family/systematic-uncertainty limitation.
No new data or recomputed fit is needed.

## Independent numerical results

The independent raw parser used the saved 1701-row release and full covariance,
not supplied fit coefficients or construction functions. Direct dense solves
replace the fitter's Cholesky-whitened SVD/QR estimator. The spherical alias
search independently recovered ten possible pairs, with five in the primary
sample, and the conservative hash grouping reproduced 1067 training/304
validation rows. The exact linear Gaussian prediction argument includes both
cross-block conditioning and training-coefficient uncertainty. It is not blind
or independent-survey confirmation, and the finite alias search is not a
complete physical-source identity census.

| Quantity | Independent value | Absolute difference from saved result |
|---|---:|---:|
| F2 full original chi-square | 1209.58812420269 | 1.14e-12 |
| F2 repaired validation score | 294.80466026209 | 7.11e-12 |
| F2 five-point AP quadratic | 4.51857159878 | 1.96e-12 |
| F2 coefficient vector | [23.80411733917, .244804092368, -.159330687084] | max 1.57e-13 |
| F2 parameter covariance | full saved 3x3 reproduced | max 3.04e-18 |

The independent AP calculation parses the original 13 BAO entries by quantity
label, forms ratio Jacobians, excludes z=2.33 using the independently selected
SNe range, and propagates F2 covariance analytically. A 40000-draw diagnostic
with a different seed gives all included denominators positive and marginal
variance ratios 1.010–1.037, consistent with a local approximation. A finite
Gaussian-ratio diagnostic does not prove existence of exact ratio moments or
global Gaussianity: a denominator with nonzero Gaussian variance has a pole
in its unrestricted distribution. The candidate expressly claims only local
linearized diagnostics, not a certified ratio distribution or significance.
That limitation remains material, especially for F3/F4 extrapolation.

I inspected fitting/validation/alias and all-family AP implementations, their
finite-difference repair, selection and saved summaries. No fitting or covariance
defect was found. The all-six tables and sensitivity calculations were reviewed
against saved artifacts/code but not all independently refitted in this context.
F5 has its declared nonlinear/Jacobian approximation. F4's statistic remains
withheld. Published processing, covariance calibration, zero cross-probe
covariance and optical/ruler assumptions are supplied, not independently proved.

## Analytic conclusions

ANALYTIC_REVIEW.md contains the direct argument. Independent rational root
counts, high-precision integration and direct metric-to-Ricci calculation
confirm the F2 singular flat continuation and the exact saved F3 point-estimate
past-completeness statement. The flat inverse, curved regular turning example,
clock-parametrized Jacobi equation, actual return distinction and smooth
identical-in-range/different-tail witnesses survive at their written hypotheses.
The C2 spline qualification is necessary and retained. The inverse leaves F,
metric/query choices and interfaces supplied; no unique whole universe is
required to state this limited result or its remaining freedom.

The F3 supplied flat geometry with complete spatial slices is past null/timelike
complete, not future complete or an identified physical UDT completion. Its
coefficient uncertainty and sample sensitivity prevent empirical tail selection.
The expanding examples remain expanding controls after reciprocal-coordinate
rewriting. The founding positional geometry behind c_E, ordinary local clocks,
one geometry including velocity/gravity and no preferred physical observer is
preserved; it is neither replaced by these controls nor proved observationally.
Local GR readout consistency is not sourced-field recovery or measured
terrestrial/solar correspondence. No protected input was used.

## Actual omissions and review limits

No raw photometry, DES independent fit, quasar light-curve refit, BAO catalog/
template reanalysis, survey covariance validation, physical transfer proof,
native response law, nonlinear dynamical solve, source/matter theory, all-history
classification or X_max identification was attempted. Source papers were checked
at the method/interface statements used in the map; their full analyses were
not replicated. The historical source audits and author's complete ODE sweep
were not rerun. The reviewer did not perform new mutation/catch tests because
no new regression guard is proposed. No GPU, external message, subdelegation,
commit, live/registry/CANON mutation or protected payload access occurred.

Review code stayed within two threads/two GiB/600 seconds per command. Reviewer
symbolic failures and their same-equation implementation repairs are preserved
and explained in ANALYTIC_REVIEW.md. No unfavorable scientific result was removed.
After R1/R2, a bounded fidelity re-review should check repaired wording/figure,
unchanged scientific bytes and final current-status claims. Review does not
change registry grades, adopt premises or authorize a successor campaign.
