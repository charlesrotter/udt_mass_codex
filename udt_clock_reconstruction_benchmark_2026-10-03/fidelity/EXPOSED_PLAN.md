# CBR1 exposed replay freeze

Source-first seal completed before new implementation exposure. Now read:
RUN_PLAN.md, forward.py, inverse.py, SMOKE_PLAN.md, smoke.py and smoke outputs.
No main records/outcomes yet. The source-first scientific disposition is unchanged;
the Python version typo is controlled by SOURCE_FIRST_METADATA_CORRECTION.md.

Independent implementation: derive direct linear coefficients for each raw log
record and apply 50-digit Decimal arithmetic, independently from parent's
frame-contraction/summation stages. No parent scientific module imports. General
v weights per raw log are +2(1+3/v²) for frame0 and -(1-v²)/v² for the six boosts,
all divided by L². Richardson weights are -1 at large L and+2 at half L.
Geodesic-stencil weights are -4 center,-1 each temporal,+1 each spatial, divided
by h². The single raw-weight composition also recomputes the deterministic noise
bounds directly rather than copying a parent bound formula.

Read the public clock-only file. Enforce exact row schema and complete21-record
groups, nine sites and two halving pairs. Replay epsilon0,1e-14,1e-12,1e-10 with
the frozen seed1729 in saved row order using standard-library Random: this shares
the PRNG method to reproduce the specified perturbations, not independent noise.
Convert actual perturbed float values to Decimal before reconstruction. Calibration
v,L,h decimal strings represent the frozen nominal settings. Recompute endpoint
fit, all interior held-out residuals, alpha/Lambda when identifiable. Compare
reported scalar/Box results with independent results, tolerance1e-10 in R and
1e-7 in Q (floating implementation agreement only, not continuum accuracy).
Compare informative statuses and parameter results with scale-aware1e-7 relative/
absolute tolerance. Smaller discrepancies will be reported, not hidden by gates.

Independently compare noisy-minus-clean changes against direct absolute-weight
bounds, including the shared center. An adversarial epsilon1e-12 perturbation on
A/center0/h=.04/L pair .01/.005 will align raw signs with combined Box weights;
check attained bound to1e-6 relative, exceeding the parent's0.1% requirement.
This is a deliberate guard challenge, not a physical noise distribution.

Catch tests: changing one raw record by1e-6 must alter reconstructed R/Q by the
predicted linear weight; the adversarial sign pattern must attain the bound.
These exercise the independently implemented estimator and are not evidence
for geometry. Parent schema/input guards may be challenged separately via
subprocess and clearly labeled regression, not independently reimplemented proof.

Main oracle comparison occurs only after independent inverse records are saved.
Do not use oracle values to set any estimator, exclusions or threshold. Inspect
actual saved geodesic placement/clock mapping and main finite-error tables. The
math reviewer separately handles original tensor reconstruction; this reviewer
will inspect false-pass/full-tensor scope and record if that numerical replay
is not duplicated here. A new physical law, empirical experiment, generic4D
claim, rigorous finite remainder bound and hardware capability remain excluded.

Resource limits: CPU2GiB, one BLAS thread through existing capture, no timeout;
bounded serialized main dataset, four noise levels and fixed finite linear
combinations. Output at most a few MiB. Preserve every failed replay/report;
no parent source changes or scientific tuning in this directory.
