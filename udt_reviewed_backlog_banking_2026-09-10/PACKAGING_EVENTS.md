# Preserved packaging and review history

These are administrative/reproduction/integration events, not new scientific discoveries.
Original candidates, objections, false passes, repairs and lost-output caveats remain in their
unchanged source packages and the source assessment ledgers. Initial candidate files in
initial_draft/ are preserved, not overwritten to mimic the later acceptance record.

1. A registry query initially requested `id` instead of `premise_id` and failed with KeyError.
   The query was corrected. An attempted standalone W4 lookup failed: W4's accepted content
   belongs to G261, rather than an independent registry row. Parent dependency metadata was
   corrected before the final claim freeze; no missing theorem was invented.
2. A few guessed administrative filenames did not exist. Bounded directory/file queries located
   their actual receipts. These unsuccessful reads did not establish missing scientific evidence.
   One patch failed its expected anchor and made no changes; the corrected patch then applied.
3. The first output correspondence search covered only `.stdout` and missed `.stdout.json`,
   `.stdout.txt` and NCI1's named AUTHOR_CHECK_OUTPUT.txt. Exact source paths were then used;
   identity was claimed only after actual byte comparison. Source review correspondence ledgers
   distinguish Python-build/timestamp-only differences from byte-identical outputs.
4. The first banking draft was frozen before the older-geometry reviewer completed its review
   identity and HB lost-output metadata, including two additional source references. Its five
   draft files were moved intact into initial_draft/. The final claim/row freeze was regenerated
   from completed source assessments before registry integration. This was source-preserving
   metadata completion, not a new mathematical argument or source edit.
   Direct comparison found BASELINE_REGISTRY, BANKED_ROWS, BANKING_RECORD and DISPOSITIONS
   byte-identical at that regeneration. BANKED_CLAIMS changes were confined to G384/G385 history,
   artifacts and source-assessment pins, and G386--G394 updated source-assessment pins.
5. `checks/draft_startup_tests.*` exited4: unrelated repository conftest imported a Torch/CUDA
   shared library that could not map under512MiB, before the relevant tests collected. Inspection
   established that the startup/banking tests require none of those GPU fixtures. Scoped runs
   therefore use standard pytest `--noconftest`; this does not omit a needed fixture or science test.
6. `checks/draft_startup_isolated.*` recorded349 passes and5 failures. Two historical G312
   projection tests incorrectly included the30 newly prepended rows in an old365-row snapshot
   comparison. They now strip ONLY the30 new rows before that comparison and still check the
   exact authenticated G312-only transition and single-read property. No old registry byte/hash
   or G312 control was weakened. Startup word limits and the three-sentence next gate were also
   exceeded and repaired without raising ceilings. Finally the full-audit pytest wrapper was
   inappropriately nested inside the small512MiB/120s envelope; its child reported git-log128.
   The exact cause of that git failure was not established. Full audits are run separately with
   2GiB/900s, preserving the failed execution rather than labeling it a pass.
7. `checks/draft_startup_repaired.*` recorded352 passes,1 failure and1 deselection: LIVE was
   still905 words. A further five-word trim met the unchanged900-word ceiling. The later
   `checks/draft_banking_guards.*` actually passed490 tests with only the separately executed
   full-audit wrapper deselected.
8. The fresh integration reviewer found that the LIVE/HANDOFF headline called all30 additions
   mathematical, despite correctly differentiated adjacent categories. It was narrowed to
   `G383--G412 exact-scope banking`; G409 design, G411 benchmark and G412 finite-procedure
   distinctions remain explicit. This is a presentation correction, not a grade change.
9. `checks/integration_preservation.*` exited1 at Git status under512MiB. The helper initially
   retained only CalledProcessError; its original code is preserved as
   `checks/initial_preservation_check.py`. A stderr-reporting repair and one diagnostic rerun
   preserved Git's actual `fatal: unable to create threaded lstat: Resource temporarily unavailable`.
   The unchanged repaired check passed at2GiB in `checks/integration_preservation_2g.*`, including
   the original46 name/status fingerprint, original365 registry bytes and all2612 source pins.
   This bounded source-preservation check uses the larger memory allowance because the actual
   Git operation failed at the small allowance. No Git/runtime configuration file was changed.
   The independent reviewer separately reproduced the same diagnostic and used an invocation-only
   preload-index flag; its initial `-uall` versus baseline `-unormal` count mismatch is preserved
   in that review and was corrected without changing the baseline fingerprint.
10. `checks/integration_full395.*` ran at2GiB/900s and exited1 after408.145703146seconds:
    `LIVE next gate lacks bounded conditional banking status: G411=LC2`. The headline wording
    repair in item8 had moved the category labels out of the next-gate sentence while its old
    guard still required them there. The guard now requires `exact-scope banking` in the next
    gate and all three distinct G409/G411/G412 category labels in the full LIVE/HANDOFF frontier.
    The corresponding mutation test was updated and six category-removal tests added. The same
    headline correction was applied to CURRENT_RESEARCH_PROGRAM. No scientific row, source pin,
    old registry projection or mathematical check changed; the failed full run remains failed.

The source reviewers separately preserve their bounded launcher/adapter corrections, including
the response review's occurrence-count failure before any scientific program executed. Original
scientific implementations were never repaired or rewritten by this banking task.
