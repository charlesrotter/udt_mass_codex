# Candidate-exposed, author-code-unexposed direct stage

Read INITIAL_CANDIDATE.md and CANDIDATE_FREEZE.json after the source-first seal.
Expected candidate SHA256:
431610fc8e8d7672447b879f327272c257de74635e902e76c120de2f041dbf79.
No `check_machian.py` or `checks/analytic.*` has yet been opened.

Before computation: independently verify the candidate's scale criterion and
external static-dust GR control, exact and conditional only. The static product
curvature is reconstructed from the Gauss tensor of round S3 in an orthonormal
frame, followed by explicit contraction and solving Einstein+Lambda for dust.
This differs from the candidate's described direct coordinate Ricci route.
Spatial volume is integrated separately; vacuum energy is deliberately added
as a wrong mass-definition control. The observer scope of no redshift is
stationary dust-rest clocks, not all possible observers in that metric.
Homothety checks use both affine tangent and phase-covector normalization and
a nonlinear arrival map to expose event-matching errors. First-derivative
criterion is one-dimensional local root isolation, not global uniqueness.

Same declared resources and existing capture helper as source-first: one CPU
process, no GPU, exact SymPy/Fraction methods,60s/512MiB/threads1. Freeze these
checks/output before author-code exposure. No physical field equation is
introduced into UDT. The field equation applies only to the named imported
GR comparison. Native admission, physical viability/stability and independent
observations remain outside scope. SOURCE_MAP.md was requested but did not yet
exist when its read was attempted; citation fidelity is pending.
