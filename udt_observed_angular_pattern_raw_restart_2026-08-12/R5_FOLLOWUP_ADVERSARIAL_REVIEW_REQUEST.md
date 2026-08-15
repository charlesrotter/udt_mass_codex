# R5 repaired-package follow-up adversarial review

Date: 2026-08-14
Mode: read-only, source-bounded, no continuation of research

The first external review returned `COVARIANCE_CAVEAT_INSUFFICIENT` while accepting the spectral
conclusions. Audit only whether its two blocking repairs and optional minimum-rank clarification are
now satisfied.

Required checks:

1. Confirm every covariance atlas row now carries the covariance threshold gap plus global,
   covariance-range, and joint range-overlap ownership flags.
2. Reconcile the row labels to exactly 91,568 owned and 184,300 unresolved range-overlap rows.
3. Confirm every summary row carries an ownership status and reconcile exactly 2,369 `OWNED`, 475
   `UNRESOLVED_NUMERICAL`, and six `NUMERICAL_BOOKKEEPING` rows.
4. Confirm the independent verifier reconstructs every new ownership field and summary label.
5. Confirm the outcome prose no longer promotes unresolved range-overlap values or summaries.
6. Confirm the proper-rank minimum table now discloses the postselected minimizer ranks.
7. State whether the already accepted dominant-direction and control-dependent-subspace conclusions
   can now be banked as `VERIFIED_WITH_CAVEATS`.

Return exactly one primary landing:

- `VERIFIED_WITH_CAVEATS`
- `REPAIR_INCOMPLETE`
- `COVARIANCE_CAVEAT_REMAINS`
- `REFUTED`

Separate blocking repairs from optional clarifications. Do not infer any feature, oscillation,
significance, physical scale, BAO interpretation, cosmology, UDT response, CMB relation, or
`X_max`. Do not edit files or continue the research.
