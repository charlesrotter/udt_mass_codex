# G264 registered repair result

Date: 2026-08-25
Status: `REPAIR_IMPLEMENTED_AWAITING_EXTERNAL_FOLLOWUP`

The scientific landing is unchanged.

## R1 — metric-first verifier

`verify_metric_first.py` now derives the curvature evidence without importing the production script,
SymPy, or saved results. At a regular equatorial point it constructs the inverse metric and its
derivative, Christoffels and their derivatives, Riemann, Ricci, scalar curvature, Kretschmann
scalar, and both registered mixed Einstein channels directly from exact metric component jets.

Observed result: 250 arbitrary regular rational jets, 1,000/1,000 exact assertions passed.

## R2 — honest role labels

`verify_independent.py` is now explicitly a result-blind, implementation-distinct consistency
replay. Reports and gates cite `verify_metric_first.py` as the independent metric-first derivation.

## R3 — fail-closed repair checks

Package and altered-copy checks require the metric-first construction, dependency-free provenance,
full coverage, honest consistency-replay label, unchanged scientific landing, and unchanged
ownership ceiling.

No physics premise, profile, threshold, source, history, or `X_max` statement changed.

Post-repair gates: package verification passed; the 245-row premise audit passed; repository tests
returned 167 passed and one expected xfail.
