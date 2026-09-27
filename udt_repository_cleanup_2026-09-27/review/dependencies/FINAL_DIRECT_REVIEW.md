# Final direct dependency and construction review

**Verdict: VERIFIED-WITH-CAVEATS for the constructed maintenance change at the input hashes in `final/REVIEWED_FINAL_INPUTS.tsv`.** No remaining defect was found in this bounded direct review. Parent-owned integrated tests, fresh-reader review, final publication scope/seal checks, commit and remote verification are separate completion gates; this report does not claim them passed.

Same separate reviewer context: `/root/cleanup_dependency_review`. The first source review, exposure/coordination disclosures and limitations remain in `DEPENDENCY_ADJUDICATION.md` and `INITIAL_REVIEW_SEAL.json`. The original initial results and seal are preserved; final outputs are in `final/`. HEAD was independently rechecked as `8aac11e13a2311347771e11f507f4f2042ea02a2` on `grok` before publication. No scientific test, GPU operation, numerical campaign or protected-content read was performed in this continuation.

## Direct result

- All **34 archive files / 223,085 bytes** match their exact baseline Git blobs. The independent comparison uses `git cat-file blob <oid>` and separately derives each Git blob ID and SHA-256 from the archived bytes; it does not reuse construction or production-checker code.
- All destinations are regular files, with no symlinks. **32 files are `0664`, two are `0644`**; all correspond to Git mode `100644` and remain non-executable. Every old root path is absent, including absence of a dangling symlink.
- Archive manifest, final inventory and dependency clearance agree on every source and destination. All 34 also match a unique full-read `ARCHIVE_ELIGIBLE` row in the surface review or its declared three-file transfer supplement, including the original Git blob and SHA-256. This checks correspondence; the surface review's own context record establishes the actual prose reads.
- The independent inventory audit again passes **33,380 baseline paths, 1,147 baseline root rows and 799 groups**, now with 34 archive dispositions. Its 13 corruption controls are all rejected. These are baseline census counts; 34 originals have moved from root.
- Tracked changes are exactly the 34 original-path removals and five permitted navigation edits: README, INDEX, LIVE, HANDOFF and `research/_registry/README.md`. All **52 pre-existing unrelated untracked status entries** remain identical. No other tracked source, script, fixed historical table or package changed, as checked by the exact Git diff inventory.
- Fifteen named authority/manuscript/fixed-history files were independently compared byte-for-byte with baseline blobs. They include AGENTS, CLAUDE, CANON, founding, both scientific-premise files, current program, unchanged manuscript **and coverage TSV**, the old relocation ledger, maintained scientific verifier/startup test, and all three fixed root rehearsal records.
- All **49 Markdown links** in the five edited navigation files, the new packet README/repository map and the archive README resolve. Every moved file has an explicit archive-README link. The unchanged manuscript's old observer-pair-review basename is explicitly resolved through the new archive guide and manifest; original historical references were not rewritten.

The current production publication checker was also run directly and passed. It measured 29,793,545 maintenance-packet bytes at that run, below the 50 MiB limit. Later additions require the parent's final size/scope check; this number is deliberately a recorded measurement, not a permanent bound.

## Implementation review and exercised repairs

`prepare_archive.py` intersects actual full-read surface eligibility with dependency clearance, checks the original baseline blob/hash against the review record, requires exactly one unchanged original-or-destination regular file, rehearses byte-preserving restoration in scratch, writes the explicit manifest/overrides, and then renames. It performs all source validation before the first relocation. A partial relocation would remain identifiable in the manifest and the same-byte original/destination checks permit bounded recovery. I inspected this implementation and reviewed its concrete output; I did not rerun the mutating constructor.

The first construction attempt incorrectly required filesystem mode `0644`. The saved stderr shows failure at that source-validation assertion, before the move loop. Accepting the measured existing `0664` and `0644` modes repairs that assumption while preserving regular-file and non-executable requirements. The initial failure and repaired pass remain in `checks/ARCHIVE_CONSTRUCTION*`; neither was hidden or counted as scientific evidence.

`verify_cleanup.py` now checks the inventory's destination against the archive manifest, rejects archive symlinks, rejects executable modes, detects dangling symlinks at old root paths, preserves retained destinations and enforces the packet-size ceiling. These address the earlier review objections without weakening content, provenance or scientific guards.

`check_publication_guards.py` executes the **actual** `run()` with isolated synthetic Git/table metadata and synthetic file bytes. Real filesystem and hash branches run. Valid regular-file cases pass for both `0664` and `0644`. Twelve corruptions are rejected: inventory destination mismatch, same-byte archive symlink, dangling old-root symlink, executable archive mode, changed bytes, changed hash, changed size, changed blob ID, duplicate archive row, moved retained destination, unrelated tracked edit and changed unrelated status. No authoritative source was mutated. These finite tests cover the reported repairs and representative invariants; they do not prove universal fault coverage.

## Navigation and remaining scope

The five navigation diffs direct readers to the cleanup lookup and later archive maps while preserving LIVE and the exact scientific registry as owners. INDEX's added task-triggered skill phrase restores the already-authoritative startup instruction rather than introducing a new method. Its removed old maintenance-pass breadcrumb is historical and remains recoverable; no scientific route was removed. README retains the fixed manuscript snapshot and its grade/authority limits. The old relocation ledger itself is unchanged.

Historical dispatches retain their original instructions and claims as bytes. Their new guide explicitly denies current execution authority, preserves criticism/failure records and explains baseline-Git restoration. Moving a receipt does not invalidate its evidence, and retaining a scientific interface does not promote its status. The dependency review remains a bounded static/consumer audit; no claim of whole-repository dynamic completeness or scientific re-verification is made.

## Reproduction

```sh
python3 udt_repository_cleanup_2026-09-27/review/dependencies/verify_final_constructed.py
python3 udt_repository_cleanup_2026-09-27/review/dependencies/check_publication_guards.py
python3 udt_repository_cleanup_2026-09-27/verify_cleanup.py
```

The unchanged independent inventory script was imported with only its output directory redirected to `review/dependencies/final/`, then `main()` was run. This preserved the prior initial results. Exact stdout/stderr and JSON are saved under `final/`; no production classifier is imported by the independent inventory or archive-byte auditors.
