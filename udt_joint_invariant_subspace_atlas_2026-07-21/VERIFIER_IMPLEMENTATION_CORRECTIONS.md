# Independent-Verifier Implementation Corrections

Date: 2026-07-21

The independent verifier was implemented only after the main atlas had completed. Two execution
defects stopped its first attempts before a verification result was written:

1. A diagnostic-only Riemann bivector construction supplied one inverse metric to an `einsum` that
   explicitly required two. The corrected call raises both leading curvature indices, matching the
   independently implemented production bivector check.
2. The omitted-nonlinear-jet catch initially selected the first transformed anchor, whose phi
   gradient was zero. The omitted gradient-times-map-second-jet term was therefore exactly zero and
   made the negative control vacuous. The catch now selects the first preregistered anchor for which
   that contraction is nonzero and tests the raw scalar second-partial transformation directly.

Neither defect changed an atlas candidate, family, tolerance, saved row, scientific classifier, or
maximum conclusion. The completed pre-review verifier produced its result only after both
corrections and its then-registered catches passed.

A later fresh review exposed three substantive certification defects, now preserved in
`FRESH_ADVERSARIAL_CORRECTION_REVIEW.md`:

3. Product and CRT primary projectors did not first establish semisimplicity. Both implementations
   therefore called an exact Lorentzian self-adjoint nilpotent Jordan operator classified. They now
   use separately written algebraic-versus-geometric multiplicity gates and fail closed on defective
   or rank-ambiguous clusters.
4. Projector residual and stability acceptance used `1e-7`; both now enforce the registered `1e-9`.
5. Several negative controls used catch-only predicates. Saved registries, full row coverage,
   bivector summaries, uncertainty identities, and the result contract now pass through reusable
   validators, and their mutations pass through those same validators. The exact Jordan example is
   a tenth end-to-end catch.

The post-correction full builder and independent verifier reproduce the same census and pass all ten
catches. Fresh external review and repository-wide banking remain separate final gates.

A third fresh review found one final production-only tolerance leak:

6. The builder's curvature-eigenbivector complementary-pair test still used a literal `1e-7` even
   though all central projectors and the independent bivector test used `1e-9`. The saved ensemble
   has zero candidate bivector planes, so no row changed. The gate now uses `RANK_TOL`, and the full
   replay again reproduces the census and all ten catches.
