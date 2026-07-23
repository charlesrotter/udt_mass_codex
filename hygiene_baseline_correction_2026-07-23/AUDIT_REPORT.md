# Hygiene-Baseline Correction Audit

Date: 2026-07-23

Status: `VERIFIED_WITH_EXACT_LEGACY_BACKLOG_AND_CODE_REVIEW_CAVEAT`

Maximum conclusion:

`CURRENT_TEST_BASELINE_GREEN_WITH_EXACT_HASHED_LEGACY_HYGIENE_BACKLOG`

## Result

The repository test suite is green without rewriting historical scientific evidence:

```text
70 passed, 1 expected xfail, 0 failed
```

The former expected failure was real rather than obsolete. The hygiene guard was committed at
`b5622bd847a3f37f134125a0bf734eeb57133159`; all 37 currently noncompliant documents were introduced
later on 2026-07-09. They contain 88 exact missing requirements.

Retrospectively adding grades, premises, or verifier claims would alter evidence meaning, and 23 of
the 37 paths are classified immutable in the fixed R1C snapshot. This correction therefore leaves
all 37 files byte-identical and records their exact paths, SHA-256 values, omissions, introducing
commits, and fixed classifications in `HYGIENE_LEGACY_BACKLOG.tsv`.

## Corrected guard behavior

`tests/test_hygiene_header.py` now:

- verifies the complete backlog-file SHA-256;
- requires exactly 37 unique rows and 88 omissions;
- checks every registered document's bytes and exact omission list;
- requires every other covered document to be fully compliant; and
- fails when a registered path is no longer covered.

The backlog is not a general waiver. A new omission cannot enter by merely adding a row: the
backlog hash and counts are separately frozen in the test and the final test hash is frozen by this
package's repository gate.

## Independent and adversarial verification

The independent verifier separately implements the glob census, marker checks, allowed-grade check,
document hashes, introducing-commit ancestry, and fixed-classification comparison. It reproduces:

```text
covered documents:                70
fully compliant:                  33
registered backlog:               37
registered omissions:             88
post-test introductions:          37
fixed classifications reproduced: 37
```

It then copies the test controls and all 70 documents into disposable directories and runs the
actual pytest test after four mutations. New unregistered omissions, changed registered bytes,
duplicate rows, and an enlarged backlog all turn the test red.

A fresh zero-context reviewer independently reproduced the census, hashes, unchanged artifacts,
green suite, and mutation behavior. Its verdict is `VERIFIED-WITH-CAVEATS`.

## Caveat

No editable test can prevent a deliberate commit that weakens both the test and all its guard
constants. The final test and control hashes are therefore recorded and gate-checked, and future
policy changes require ordinary preregistration and code review. The fail-closed claim applies to
data/backlog mutations under the banked guard code.

Coverage remains the declared root globs. Scientific immutability, frozen packages, and unrelated
scope are enforced by separate repository gates rather than this metadata-presence test.

## Repository gates

- six hard-frozen packages: 127 manifest entries and 133 tracked paths, unchanged;
- 85 prior scientific-package manifests: 2,418 entries, all replayed;
- latest bank-simplex package: 41 entries, unchanged;
- current navigation: 1,114 artifact paths, 306 frontier rows, 101 resolved targets;
- original dirty checkout: 54 metadata-only paths, unchanged and contents unread;
- correction manifest: complete and replayed; and
- nine repository corruption/scope catch-proofs: passed.

## Scope and unchanged evidence

The only existing files changed are:

- `tests/test_hygiene_header.py`;
- `STRUCTURE_HYGIENE.md`;
- `LIVE.md`; and
- `CLAUDE.md`.

All 37 backlog documents, equations, scientific claims, status labels, `CANON.md`, registries,
scripts, data, fixed historical verification records, and frozen packages are unchanged.

## Banking gates

1. Preregistered: **YES**, commit `1b455fb`.
2. Full or bounded scope: **YES**, exact current hygiene-glob universe only.
3. Independently verified: **YES**, separate census plus actual-pytest mutations and fresh
   zero-context adversarial review.
4. Premises audited: **YES**, including the editable-test/code-review limitation and declared glob
   boundary.
