# Independent review-check repair

2026-09-10, before any RF1 author candidate/code/output exposure.
Initial source preserved literally as `independent_normal_metric_check.initial.py`,
SHA-256 `bb6ca932a3fea3981d1ac3d23dd319ec8f6ea11fa46f8683b33ae702741e6c19`.
Initial capture stem `independent_normal_metric_check` returned rc=1 before any
assertion executed: Python 3.10 does not accept starred tuple expansion directly
inside `r2[d, e, *s]`. No initial mathematical check passed or failed.

One bounded verification repair contains three changes:

1. Write the tensor key as `r2[(d, e) + s]`, compatible with Python 3.10.
2. Extend the radial identity multiplication to degree five. A quartic metric
   coefficient contracted with x has degree five, which the original default
   degree-four multiplication would silently discard. This closes a potential
   false pass; it does not alter geometry construction or an expected tensor.
3. Remove the arithmetic-only literal-sign wrong-claim probe. It would provide
   no substantive evidence about the implementation and is not counted.

Metric formulas, curvature construction, covariant-derivative slot corrections,
expected geometrical quantities and resource limits remain unchanged. The failed
initial source/stdout/stderr/metadata are retained. Parent was notified before
repair; this is disclosed against the campaign's one-repair budget. No author
candidate/proof or physical premise is changed.
