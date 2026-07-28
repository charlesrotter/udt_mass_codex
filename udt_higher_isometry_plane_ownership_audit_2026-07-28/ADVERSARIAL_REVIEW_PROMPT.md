# Fresh adversarial review prompt

You are a fresh, zero-context adversarial mathematical reviewer. Work read-only in
`/home/udt-admin/udt_mass_codex` on branch `grok`. Do not edit any file, do not use conversation
history, and do not trust the candidate report.

Review the uncommitted result package
`udt_higher_isometry_plane_ownership_audit_2026-07-28/` against its committed preregistration
`3e3eecc` and frozen sources. Rerun the production and independent scripts directly. You may run
read-only symbolic or standard-library scratch calculations.

Attack these load-bearing points especially hard:

1. Does the `3 x 3` orbit Gram matrix really cover the stated descended `R x T2` family, with
   correct determinant, inertia, response, characteristic polynomial, and leakage?
2. Does the scan `span(K+rV+sY,mV+nY)` exhaust every `R x S1` subgroup containing a compact ruler
   line? Is constancy of the induced Gram determinant basis invariant? Does the jet-generic proof
   actually force `n=0,s=0`, or hide fixed values or dependent jets?
3. Is the smooth nonconstant-depth `alpha=0`, `q_B=u^-1 q_round_base` countercontrol genuinely a
   complete regular `S3` metric with two distinct free Hopf/anti-Hopf reciprocal planes? Check cap
   smoothness, periods, Killing properties, and whether an equivalence weakens or strengthens the
   nonselection conclusion.
4. Is the theorem of exactly two unoriented primitive free circle lines for unimodular two-cap
   `S3` correct? Hunt orientation, exceptional-orbit, and enumeration-bound errors.
5. Is the distinction between the full `D3` eigenspace problem and restricted plane-by-plane Gram
   response mathematically honest? Is either being mislabeled as a complete metric-only selector?
6. Does the use of `A`, `V`, `f=A(Y)`, or founded `phi` make the positive generic statement
   circular? The conclusion must remain conditional on the registered descended Hopf family.
7. Are the Berger/round enhanced-isometry controls correct and sufficiently scoped? Downgrade or
   remove them if they are asserted without evidence.
8. Are generic, exceptional, constant-depth, and outside-family strata kept separate? Does any
   language silently select nonzero `alpha`, Hopf topology, a physical branch, macro/micro regimes,
   carrier, action, source, density/bootstrap law, or dynamics?
9. Hunt false passes, tautological checks, shared-code dependence, stale counts, missing source
   identities, and violations of the preregistered maximum conclusion.

Return one of `PASS`, `PASS_WITH_CAVEATS`, or `REFUTED` as the first line, followed by concrete
findings, exact rerun results, required corrections, and residual caveats. The outer runner will
save your response as `FRESH_ADVERSARIAL_REVIEW.md`; do not require that file to exist while you
review.
