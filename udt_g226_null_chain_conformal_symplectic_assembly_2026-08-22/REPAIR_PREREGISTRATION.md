# G226 external-review repair preregistration

Date: 2026-08-22

Trigger: fresh external `gpt-5.4` verdict `G226_ACCEPTED_WITH_REPAIRS`.

## Frozen repair scope

### R1 — strict-read-only aggregate replay

Replace the aggregate verifier's unconditional temporary-directory output with component replay to
`/dev/null`. Parse each component's stdout as JSON, compare it exactly with the sealed saved JSON,
and retain before/after SHA-256 comparison of all package and source bytes.

Pass condition: `verify_package.py` completes from a sealed read-only intake without creating a
temporary output directory, and the saved evidence tree remains byte-identical.

### R2 — verifier-coverage wording

Replace the overbroad `fail-closed` label with a bounded mechanical description. State explicitly
that the verifier checks enumerated algebraic counters, exact replay equality, required evidence
presence, selected scope tokens, manifest hashes, and no evidence-byte drift; it is not a general
semantic proof of every narrative sentence.

Pass condition: no package file describes this bounded mechanical verifier as universally
`fail-closed`.

## Frozen scientific boundary

No formula, scientific claim, alternative, source, counter, tolerance, ownership grade, or bounded
landing may change under these repairs.

## Required verification

1. ordinary repository replay passes;
2. sealed strict-read-only intake replay passes;
3. production, independent, and hostile-catch JSON remain exactly unchanged;
4. package/source hashes remain unchanged during each replay;
5. fresh repair-only external review verifies R1 and R2 before banking.

