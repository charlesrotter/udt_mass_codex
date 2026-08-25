# G252 banking replay record

Date: 2026-08-24

The preregistered 235-row integration checks were executed without persistent script outputs.

- Production: 4,096 cases; fresh JSON byte-identical to `DERIVATION_RESULT.json`.
- Independent: 12,000 cases; fresh JSON byte-identical to `INDEPENDENT_VERIFICATION.json`.
- Hostile controls: 20/20; fresh JSON byte-identical to `CATCH_PROOF_RESULT.json`.
- Package verifier: all checks passed, including single-G252 historical registry reconstruction,
  duplicate-G252 rejection, unrelated-mutation rejection, and external repair acceptance.
- The first post-banking intake exposed one integration-only package check that read the registry
  from the repository root instead of the lawful sealed `sources/` location. Under preregistered
  banking item 4, the check was changed to use the exact resolver. No science or saved output changed.
- Fresh post-banking sealed intake: `/tmp/udt_g252_review_gqfbjcza`; 46 files including scope;
  scope SHA-256 `5797eeecdf0c09755b7802bfba38c69792d9f794efd6fc4666f9bdb3376ad596`;
  all package checks passed from the intake root.
- Full current-premise verifier: `PASS: 235-row premise registry`.
- Repository suite: `PASS: 157 passed, 1 xfailed.`

No observational value, fitted coefficient, new kernel mechanism, protected payload, or unrelated
work entered these checks.
