# G119 external-review adjudication

Date: 2026-08-16

Sealed intake: `/tmp/udt_g119_screen_review_sqtu5kqn`

Scope SHA-256: `2f922a37212b0c214adf208d7c777c93bcdb867da37b67e942c4edc0f495e0dd`

Reviewer: external Codex `gpt-5.4`, fresh ephemeral read-only context

## Accepted landing

`VERIFIED_WITH_CAVEATS__DECLARED_CENTRAL_SPHERICAL_BRANCHWISE_THEOREM_STANDS`

The reviewer found no mandatory theorem, algebra, type, or ownership defect. It independently
accepted the rotational-Jacobi normalization, warped-curvature sign, branchwise determinant,
rank-zero/phase-surviving caustic, G94 transfer boundary, and scoped SNe regrade. Both executable
outputs reproduced byte-for-byte, and all 23 scoped file hashes matched.

## Optional improvements adopted

1. `verify_offdiagonal_orbit_witness.py` adds an exact shifted-coordinate time-live witness with
   nonzero orbit cross term. This is additive hardening; the arbitrary-`h_ab` result still rests on
   the covariant warped-product proof reviewed in the sealed intake.
2. `EXACT_DERIVATION.md` now explicitly types passage through another regular center as the same
   `R=0` spherical-caustic stratum followed by signed-amplitude branch continuation.

These improvements do not alter the reviewed theorem or its maximum conclusion.
