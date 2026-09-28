# First bounded review repair

2026-09-28, parent construction context. Pending fresh reviewer's re-review.
The review messages identified two precision/presentation defects. This record
preserves their initial evidence and states the controlling corrections; no
data, fit coefficient, covariance, residual, metric equation or physical premise
has changed. INITIAL_CANDIDATE.md, DATA_RESULT.md, GEOMETRY_RESULT.md and the
original figures remain the construction snapshot pinned by
CONSTRUCTION_MANIFEST.json. INITIAL_DECISION_BRIEF.md and INITIAL_WORK_ORDER.md
preserve those mutable files' initial bytes.

## R1 — qualify the complexity scores

The construction reported the conventional expressions
`AICc=chi2+2k+2k(k+1)/(n-k-1)` and `BIC=chi2+k ln(n)` without sufficiently
qualifying their scope for a fixed supplied covariance. They are retained as
reported complexity conventions/heuristics, not established exact finite-sample
corrections or log evidences for this release. Under the fixed-known-covariance
Gaussian linear-mean model, the optimism correction for an independent
same-design replicate is exactly `2k`. Thus the ordinary AIC scores are:

| Family | k | chi-square + 2k |
|---|---:|---:|
| F0 | 1 | 1314.774837 |
| F1 | 2 | 1223.727541 |
| F2 | 3 | 1215.588124 |
| F3 | 4 | 1217.475848 |
| F4 | 6 | 1215.587836 |
| F5 external | 2 | 1213.695637 |

The exact linear-model statement applies to F0–F4 under their declared
Gaussian likelihood. F5's nonlinear-mean use is an asymptotic approximation.
None verifies the observational covariance or gives a posterior probability
that a physical theory is true. F2 and F4 remain effectively tied on this
score; there is no established UDT preference over the conventional control.
The original numerical AICc/BIC columns are not silently recalculated or erased.

## R2 — repair the standalone plot's uncertainty presentation

The original BAO figure drew local linear F2/F4 bands without on-figure labels
for their level and limitations. In particular F4 had failed the declared
variance-approximation diagnostic at an included point. The prose caveat did
not travel with the image when shared.

`observations/plot_reviewed_bao.py` reads only saved comparison and fit results;
it does no fitting or statistical retuning. The corrected standalone
[PNG](observations/comparison_reviewed/bao_shape_comparison.png) and
[PDF](observations/comparison_reviewed/bao_shape_comparison.pdf) remove those
bands. They show F2's local coefficient 1-sigma bars only at the five checked
points, include release-modeled STAT+SYS and explicitly exclude family and
additional unmodeled/interface uncertainty, label the withheld
F4 uncertainty, and shade the extrapolation region. Measurement bars are also
labeled as local 1-sigma. The complete covariance still lives in the saved
result, since pointwise bars cannot display cross-redshift correlations.

Original plots remain in observations/comparison_checked/. The presentation
run exited zero in 1.359 seconds; input hashes, ordinary AIC and the unchanged
conventional score values are in comparison_reviewed/PRECISION_REPAIR.json.
Parent visually checked the corrected image. Fresh reviewer must confirm the
repair before the campaign is described as reviewed.

The same-cycle reviewer caught that the first repaired caption's shorthand
"exclude systematic uncertainty" was too broad: the parameter covariance
already includes the release's modeled STAT+SYS. The caption now makes that
distinction. The first repair image/table/script are preserved under
observations/presentation_initial/ and INITIAL_plot_reviewed_bao.py; relocation
hashes are in PRESENTATION_REPAIR_HISTORY.json. The rerun is caption-only and
leaves the scientific input files and reported numbers unchanged.
