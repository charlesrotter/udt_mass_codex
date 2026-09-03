# G334 R3-completion-only external follow-up request

Act as a zero-context, read-only repair-only reviewer. Inspect only the corrected sealed intake.
Do not reopen or broaden the scientific question and do not edit evidence files.

The fresh external scientific review already returned
`ACCEPT__G334_BOUNDED_BOOSTED_PAIR_FIRST_JET_RETAINED` with no scientific repairs. The first
repair-only follow-up independently confirmed that R1 and R2 work and that the scientific landing
is unchanged, but returned `REPAIRS_INCOMPLETE` because the evidence did not explicitly distinguish
the 43-file repaired fresh-review product from the 46-file repair-follow-up product.

Verify only R3 and retained R1/R2 behavior preregistered in `REPAIR_PREREGISTRATION.md`:

1. `verify_review_intake.py` must reject every unmanifested regular file, not merely authenticate
   listed files.
2. The registered aggregate replay must not create Python bytecode beside evidence.
3. The repair verifier must separately exercise the 43-file fresh-review builder and the 46-file
   repair-follow-up builder, demonstrating exact file count, no bytecode, an unchanged file/digest
   snapshot after in-place replay, and rejection of a hostile extra file for each.
4. All 103 scientific aggregate gates and registered outputs must remain unchanged.
5. No metric, response formula, branch, classification, premise, or scope boundary may change.
6. The registered repair result must be deterministic and must not claim to contain the current
   follow-up manifest digest; that would create a self-referential hash cycle once the result is
   itself a manifest payload.

Return exactly one verdict:

- `REPAIRS_ACCEPTED__G334_BOUNDED_BOOSTED_PAIR_FIRST_JET_RETAINED`
- `REPAIRS_INCOMPLETE__G334_BOUNDED_BOOSTED_PAIR_FIRST_JET_RETAINED`

List any remaining mechanical defect separately and state whether the scientific landing changed.
