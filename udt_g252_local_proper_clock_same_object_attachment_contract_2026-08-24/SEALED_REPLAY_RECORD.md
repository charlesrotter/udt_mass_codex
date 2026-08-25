# G252 repaired sealed replay record

Date: 2026-08-24

- fresh repair test intake: `/tmp/udt_g252_review_nlhcr0y2`;
- file count: 33 including `REVIEW_SCOPE.json`;
- scope SHA-256: `a3369e7a0ea568e2e26280f17dd6cdff4dc04ff5cf71a505499a82e47050d145`;
- production 4,096-case replay: PASS;
- independent 12,000-case replay: PASS;
- 20-hostile replay: PASS;
- package verifier: PASS, including repository/relocated controls and missing, ambiguous, and
  hash-mismatch rejection;
- evidence writes: none;
- scientific landing: unchanged.

This intake is the internal repair proof. A later fresh intake containing the complete repair record
will be used for external repair-only follow-up.
