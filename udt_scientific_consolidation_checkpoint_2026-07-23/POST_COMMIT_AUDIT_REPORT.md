# Post-commit adversarial audit report

Date: 2026-07-23

Preregistration commit: `67d5b1dee23e471cadc2cbbfd7244165edb96b6e`

Maximum conclusion:
`POST_COMMIT_CHECKPOINT_CORRECTION_VERIFIED_WITH_NO_NEW_PHYSICS`

## Result

The checkpoint's underlying scientific evidence remains intact. The audit
found and corrected four navigation/verification defects and one wording
ambiguity:

1. The repository gate passed but rewrote its own scope list on a clean
   replay. Its generated output is now excluded from its input-scope report,
   making repeated clean replays byte-deterministic.
2. The independent verifier previously checked source hashes and path
   existence without resolving every current identity to an exact parent
   status row. `SOURCE_STATUS_BINDINGS.tsv` now provides 29 exact bindings
   covering all 24 current identities, and the verifier checks every source
   row, field, and value.
3. The particle result now retains its exact parent grade,
   `SETTLED_STATIC_FINITE_BOX_CONDITIONAL`, including the carrier, action,
   coefficient, boundary, box, staticity, and operator limits. This is not a
   promotion to time-live or unconditional matter.
4. The `phi`/observer-rapidity join now reproduces the exact parent grade
   `OPEN_NOT_JOINED`; no identity is derived.
5. The zero-`dphi` prose now separates the exact negative result—`dphi`
   supplies no intrinsic line or split there—from the still-open possibility
   of a replacement requiring additional structure.
6. `MEMORY.md`'s top pointer now routes to the July 23 consolidation
   checkpoint while preserving its durable historical content.

The historical preregistered status table remains unchanged. The two current
status corrections are append-only in
`POST_COMMIT_STATUS_CORRECTIONS.tsv`.

## Independent checks

The strengthened verifier requires:

- exactly 24 current status identities;
- exactly two registered post-commit status corrections;
- 29 unique source bindings covering all 24 identities;
- unique resolution of every bound parent row and exact equality of every
  bound field value;
- exact source-lineage hashes;
- the 12-family by 5-causal-class finite-cell count with zero supplied
  complete on-shell `(g,phi)` branches;
- 1,114 fixed-base path and classification identities;
- the bounded zero-context startup route.

Its 20 exercised catches include status omission/duplication, scientific
promotion, scoped-stability promotion, `phi`/rapidity identity promotion,
missing or duplicate source bindings, altered parent status, an unbound
current identity, stale startup pointers, and non-lean current blocks.

## Scope statement

No prior scientific package, frozen evidence, equation, script, data file,
manifest, current registry, or canonical file was edited. No derivation,
solve, GPU work, artifact move, or repository reorganization occurred.
