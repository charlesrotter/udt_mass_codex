# Hygiene-Baseline Correction Preregistration

Date: 2026-07-23

Base: `9373c1563378665f2585359bf16e2f019398abc3`

Mode: repository process maintenance; no physics

## Observed defect

`tests/test_hygiene_header.py::test_covered_results_have_hygiene_header` is a permanently expected
failure. At the base it covers 70 documents: 33 comply and 37 do not. The 37 fixed identities have
88 exact missing requirements. Every affected file was introduced after the hygiene test's
`b5622bd847a3f37f134125a0bf734eeb57133159` commit on 2026-07-09.

The test therefore caught a real process lapse. Deleting or weakening it is forbidden. Keeping a
permanently red test is also unsafe because a new regression can hide inside the accepted failure.

## Frozen candidate universe

`HYGIENE_LEGACY_BACKLOG.tsv` freezes:

- exactly 37 repository-root Markdown paths;
- each current SHA-256;
- all 88 exact missing requirements;
- introducing commit and timestamp; and
- the fixed R1C frozen/manifest classification.

The 37 documents are evidence inputs. They must remain byte-identical in this correction. Fixed
R0-R1H snapshots, scientific packages, manifests, and historical test records must not be edited.

## Authorized mutation

Only the following current process surfaces may change after this preregistration is committed:

- `tests/test_hygiene_header.py`;
- `STRUCTURE_HYGIENE.md`;
- current baseline wording in `LIVE.md` and `CLAUDE.md`;
- new files inside `hygiene_baseline_correction_2026-07-23/`.

No equation, claim, status, result, evidence document, scientific script, data file, historical
verification record, or current artifact registry may change.

## Required behavior

The corrected test must:

1. independently rescan every covered document;
2. accept only the exact path/hash/omission triples frozen in the backlog;
3. require every covered document outside that backlog to be fully compliant;
4. reject a missing or duplicate backlog row;
5. reject a changed backlog document;
6. reject a new unregistered noncompliant document;
7. reject a silently enlarged backlog; and
8. require an intentionally corrected backlog document to be removed or re-adjudicated rather than
   silently leaving a stale exception.

## Falsification and verification contract

An independent implementation must reproduce 70 covered, 33 compliant, 37 registered backlog
documents, and 88 omissions. It must exercise at least these four red-path mutations:

- unregistered noncompliant document;
- changed registered-document bytes;
- duplicate backlog row;
- enlarged backlog.

The full suite must exit zero with 70 passed and one existing expected xfail. The six hard-frozen
manifests, 85 prior scientific-package manifests, 1,114 current paths, 306 frontier rows, and the
original 54-path dirty-checkout metadata must remain unchanged.

Maximum conclusion:

`CURRENT_TEST_BASELINE_GREEN_WITH_EXACT_HASHED_LEGACY_HYGIENE_BACKLOG`

This does not upgrade, retrograde, or reinterpret any scientific artifact.
