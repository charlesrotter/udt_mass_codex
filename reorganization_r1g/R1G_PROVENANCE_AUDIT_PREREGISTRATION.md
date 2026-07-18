# R1G provenance-classification audit preregistration

Date: 2026-07-18

Branch: `codex/reorg-r1g-provenance-audit-2026-07-18`

Base: `8015342a81b2d27cc310dde95ab7f386c6441a77` (`origin/grok` after a fresh fetch)

## Question and frozen scope

This audit tests whether filename-prefix logic incorrectly classified post-2026-07-01
`cascade_*` artifacts as pre-native and consequently proposed invalid
`archive/pre_2026-07-01/` destinations. It authorizes no move and makes no scientific verdict.

The 32-file candidate universe will be frozen mechanically from the B02 and B03 rows in
`reorganization_r1e/PROPOSED_BATCH_FILE_PLAN.tsv`, resolved through the current-path registry. The
expected planning counts are 18 B02 and 14 B03. No candidate content will be inspected until this
preregistration is committed.

The wider affected universe will be reconstructed independently from tracked repository history:
all `cascade_*` paths carrying the R1C pre-native classification despite being first committed after
the July-1 boundary. The reported expected finding—121 files first committed July 2–3—is a claim to
test, not an input classification.

## Independent concepts and labels

Every candidate will receive three separate determinations:

1. operator provenance: `PRE_NATIVE`, `NATIVE_2026-07-01`, `MIXED`, or `OPEN`;
2. scientific lifecycle: `ACTIVE`, `SUPERSEDED`, `HISTORICAL`, or `FROZEN`;
3. path-migration safety, including justified owner and destination or a fail-closed blocked state.

Commit date and filename are evidence locators only. Neither may establish operator provenance.
`NATIVE_2026-07-01` requires explicit ancestry/content evidence tying the artifact to the native
field-equation line. `PRE_NATIVE` requires explicit evidence that the operator predates that line.
Mixed or unresolved lineage is `MIXED` or `OPEN`, never inferred into either endpoint class.

## Method

1. Reproduce the R1C prefix assignment directly from the classifier source and independently census
   affected tracked paths using Git history.
2. Locate the exact July-1 native-field-equation boundary by commit ancestry, primary dispatch/result
   records, and operator-bearing source—not by filename or calendar date alone.
3. For each B02/B03 file record current path, proposed destination, introducing/first/last commit and
   dates, family/commit ancestry, operator evidence, lifecycle evidence, owner, destination ruling,
   and evidence paths/commits.
4. Group the remaining affected cascade files only where coherent introducing commits and shared
   family evidence justify it. Preserve a one-row-per-file census behind the family summary.
5. Propose additions-only correction logic and destination taxonomy without rewriting R0–R1F fixed
   records or current registries.

## Fail-closed contract

The audit must fail if:

- any B02/B03 candidate is missing or duplicated;
- the reproduced counts disagree without a documented, evidence-backed correction;
- a post-July cascade artifact becomes `PRE_NATIVE` without an explicit lineage-evidence field;
- deleting that evidence still permits verification;
- an `archive/pre_2026-07-01/` destination lacks proven `PRE_NATIVE` operator provenance;
- provenance, lifecycle, and migration safety are collapsed into one field;
- a research artifact, current registry, or fixed R0–R1F record changes;
- frozen manifests, navigation/frontier checks, tests, or the 54-path dirty-checkout metadata gate
  drift.

Catch-proofs will inject each load-bearing classification defect and require the matching verifier
gate to reject it. A second, independently implemented census will cross-check candidate membership,
dates, and aggregate counts without consuming the first census output.

## Authorized additions and maximum conclusion

Only new audit records, scripts, tables, and retained verification output under
`reorganization_r1g/` may be added. No existing file may be modified. In particular, no research
artifact, current registry, equation, scientific label, manifest, R0–R1F record, or startup/control
file may change.

The maximum conclusion is a verified correction proposal/overlay and a migration hold. B02/B03,
application of the correction, physics work, canonization, and GPU work remain unauthorized.

This organization audit is one provenance tile. It does not sample or close any of the ten physics
solver-completeness criteria; all remain outside this audit's regime.
