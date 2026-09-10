# Runtime-provenance replay maintenance

Authorization: Charles, “Maintenance repair authorized.” Baseline:
`51f189679d4029d750e375be949f41e2f15420fa`, synchronized `grok`.
Tracked tree initially clean; 46 unrelated untracked status entries preserved.

## Frozen scope and diagnostic plan

Repair the G325 replay comparison, not its mathematics: require exact agreement
of every result field, while recording saved and replayed Python build strings
separately. Only explicitly named top-level runtime metadata may differ.
Missing/malformed metadata, extra/missing result fields, changed values, and
type changes must not pass. Preserve all original result JSONs and sources.
Report full-record equality separately from scientific-record equality.

Run real package replays, hostile comparison tests (including reintroducing the
old whole-record comparison), the full 365-row audit, and relevant startup tests.
Fresh separate-context adversarial review is required before closure. Review
is checker/reproducibility review, not a new review or promotion of the science.
One focused same-scope repair/re-review is allowed if required.

Budget: two hours active work, CPU only, no GPU or scientific solve. Begin with
G325; at most two immediately encountered identical metadata-only comparator
defects may also be repaired if diagnosed by real replay. Any substantive result
disagreement or different failure stops that extension and stays an actual gate.
No infrastructure redesign, physical adoption, registry change, canon/manuscript
edit, protected payload inspection, archive access, or observational work.

The solver-first/no-shortcuts/verifier-before-record protocols require preserving
the initial failure and adversarial catch proofs; they do not supply science.
Backup completeness/pre-reboot unsaved state stay UNVERIFIED; ScratchDisk remains
archive-only. GOCE stays PARKED/OPEN/UNSENT; paused research stays paused.

## Baseline observation

The initial unrestricted startup audit, retained in the session tool output but
not captured as a standalone file, exited 1 at G325
`replay_exact:DERIVATION_RESULT.json`; later gates were unreached. The earlier
read-only production replay differed only in `python_version`: Python 3.10.12,
June 22 versus August 31 build, both GCC 11.4.0. All 36 production checks and
all non-runtime fields matched. That observation alone did not certify the
independent/catch artifacts or the full registry. Preserved command outputs and
the final reviewed maintenance outcome follow in this directory.

## Intermediate diagnosis

G325 repaired replay passes: 41 aggregate gates, all scientific fields equal;
both Python provenance strings retained, full-record equality correctly false.
Unrestricted full audit then reaches and fails G326's identical whole-record
comparison. Direct G326 diagnostic replays all three artifacts: only the
production and independent `python_version` strings differ; catch output is
identical. Apply the same narrow maintenance to G326, retaining its source pins
and canned-emitter rejection checks. No other checker expansion is presumed.

The first two captured full-audit attempts (`baseline_full` and
`full_after_g325`) used the existing capture utility's 512 MiB address-space
cap. Both fail earlier during Git source-history access, so neither represents
the unrestricted full-audit outcome. They remain preserved, not relabeled.
`full_after_g325_unrestricted.json` captures the actual G326 failure with a
300-second wall timeout and without that artificial memory cap. Package-only
captures remain bounded by the existing utility's 60 seconds / 512 MiB.
The separate reviewer also restores each exact baseline package verifier in a
temporary copy and preserves its original failure; those are package-level
reproductions, not a retroactively reconstructed baseline full365 transcript.

## Reviewed outcome and actual remaining gate

The G325/G326 comparator repair is VERIFIED-WITH-CAVEATS for maintenance only:
`review/REVIEW.md` controls. Fresh separate context; model UNKNOWN, no different-
model claim. The reviewer uses an independently implemented recursive typed
comparison oracle; the scientific producer replays still reuse original code.
All original scientific evidence/reviews and conditional limits remain unchanged.

Author checks: nine grouped unittest tests passed, with hostile subcases and
actual copied-package failures. Reviewer checks: 661 comparison probes, 20
hostile aggregate mutations, exact baseline failure reproductions, all six
producer replays, optimization refusal, and registered G326 output checks passed.
G325 retains 41 aggregate checks; G326 retains 57, including original source pins
and canned-emitter controls. Both report scientific equality true and full-record
equality false, preserving both runtime strings. Original aggregate JSONs remain
historical v1 records; new stdout is explicitly v2, not a rewritten old receipt.

The full unmodified registry verifier completed in 273.13 seconds with exit 1,
not a timeout. It passed the former G325/G326 stopping points and stopped at
G349's no-write package gate. `full_after_g325_g326.json` retains stdout/stderr.
Direct no-write diagnosis (`g349_diagnostic.*`) found 20/21 gates true; the sole
false gate is `geometric_not_physical_union_scope`. That checker requires the
literal phrase `geometric endpoint image-union` in CURRENT_RESEARCH_PROGRAM.md;
the current sentence is `G349 finite sheet area is not endpoint image-union;
that needs supplied global preimages.` The scientific replays, source hashes,
scope checks, and no-write checks in that package pass. This is a distinct
documentation synchronization defect, not evidence of a failed area theorem.
G349 code/results and the scientific sentence have NOT been changed by this task.

Per the declared different-failure stop, no further guard repair is included.
Full365 remains NOT_PASSED; later full-audit gates are unreached. Current startup
pages and roadmap now name the actual blocker instead of the repaired one. The
next maintenance action would be a source-faithful wording/guard alignment,
with its catch proof and complete rerun; no scientific solve is indicated.
No new scientific banking, premise adoption, campaign or canon change occurs.

PRESERVATION.json compares 76 original files against baseline: all unchanged,
including original package evidence, exact registry, canon, manuscript/coverage,
and root full-audit checker. Unrelated untracked status: 46 entries, unchanged
fingerprint `d65d71d63a56b95aabfd61f33317b1f1f2b2a62a85ded8258c525b99a5e156ea`.
Protected payload contents were not inspected. Hashes establish correspondence,
not independent scientific truth or backup completeness.

Initial focused startup regression: 353 passed, one explicitly deselected full-
audit test; it is run separately above and fails as disclosed. Final startup
checks, status fidelity review, publication and hashes are recorded alongside.

The first post-status-edit startup run (`startup_checks_final.json`) caught a
one-word overflow of the research-program orientation limit: 1101 versus 1100.
Only the newly edited status sentence was shortened; that failure is retained.
The subsequent startup result is `startup_checks_repaired.json`.
