# G275 external-review repair preregistration

Date: 2026-08-26

Trigger: fresh external Codex `gpt-5.4` verdict `ACCEPT_WITH_REPAIRS` on the sealed 34-file G275
intake. The bounded scientific landing is frozen and must not change during these repairs.

## R1 — nonrecursive manifest semantics and exact containment

Repair `build_review_intake.py` so `REVIEW_SCOPE.json` explicitly distinguishes:

- physical files including `REVIEW_MANIFEST.tsv`;
- manifest entries, which enumerate every other physical file;
- the deliberate exclusion of the manifest from its own hash table to avoid recursive self-hash.

Add a sealed-scope verifier which proves exact physical count, exact listed-payload count, no
missing or extra files, path containment, and every listed SHA-256 and byte count. A mutation that
adds an unlisted file or changes a listed payload must fail.

## R2 — sealed verifier fails closed

When `verify_package.py` detects a sealed review root, it may resolve frozen sources only from exact
files inside that root. Missing or mismatched sealed source bytes must fail; no Git or outside-path
fallback may execute. Repository-mode historical Git resolution may remain only outside a sealed
review root so the fixed preregistration snapshot remains replayable after startup documents move.

## R3 — real mutation and scope catches

Replace pre-baked or tautological predicates with executable functions and hostile alternatives.
At minimum test:

- homothety leakage into the full/projective state;
- screen deletion;
- vector-only composition with hidden spatial carry;
- an invalid `c_E`-only length attachment;
- per-anchor scale proliferation;
- automatic `X_max=ell` on a finite populated domain;
- an empty population passed to a supremum operator;
- a zero-weight datum passed to scale recovery.

The empty-population control in the independent verifier must exercise the actual rejection
contract rather than test list length. Self-reported counts must be derived from an explicit
machine-readable mutation ledger.

## Acceptance contract

1. all original production and independent scientific checks still pass;
2. the exact original landing is byte-identical wherever registered;
3. the corrected sealed intake is self-contained and its registered no-write replay passes;
4. targeted tamper tests prove R1 and R2 fail closed;
5. all eight R3 mutations/scope violations are genuinely exercised and caught;
6. no observation, anchor value, history, population, or `X_max` is introduced;
7. a fresh external repair-only reviewer accepts R1--R3.

Maximum conclusion before item 7: `SCIENTIFIC_LANDING_RETAINED__REPAIRS_IMPLEMENTED__PENDING_EXTERNAL_FOLLOWUP`.
