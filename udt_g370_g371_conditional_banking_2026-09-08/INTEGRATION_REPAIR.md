# One bounded integration repair — no scientific change

Initial banking_checks_initial captured exit1 at12:11:11UTC with diagnostic
`current route lacks 352-row: CURRENT_RESEARCH_PROGRAM.md`. This is a stale
current-count expectation in the integration verifier, not a source/result
failure. All six banking guards reached before startup validation passed;
the later eight mutant tests had not yet run and are not claimed passed.

Finite diagnostic: inspect ONLY current registry-count expectations, compare
with the actual two-row additive change and correctly updated current mirrors.
No physics, fields, numerical controls, source data or boundary changes.
Stop after locating/fixing the mismatch and a focused replay; retain failure.
No broad source or scientific solve is required by this implementation error.

Cause: the patch builder deduplicated identical `352-row` source lines, then
apply_patch changed only the first matching repeated line. Two dictionary
entries still demanded352: CURRENT_RESEARCH_PROGRAM.md and
CURRENT_SCIENTIFIC_PREMISES.md. Scope/history counts elsewhere must remain352.
Repair changes exactly these two CURRENT expectations to354. It changes no
scientific banked source, registry row, candidate, test claim or resource cap.

Exact initial verifier source is recoverable from baseline
6eea4b90c59e5fd873d793c073b55ecab67d1992 plus INITIAL_VERIFIER_DIFF.patch.
The initial checker remains unchanged; its stdout/stderr/json remain saved.
This uses the one grouped integration/editorial repair in the work order,
not an author RT scientific repair. Fresh review must check this difference
and the successful replay. Failed checks are never relabeled as passing.
