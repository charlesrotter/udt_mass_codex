# Review execution and exposure record

Parent startup synchronization/full406 evidence was attributed, not rerun. Independent metadata at entry: `git status --short --branch`, `git rev-parse HEAD`, and `git ls-tree` at baseline8aac11e13a2311347771e11f507f4f2042ea02a2. The source-first reads and code locators are in DEPENDENCY_ADJUDICATION.md. Review does not claim a transcript of every read command.

Saved reproducible commands:

```sh
python3 udt_repository_cleanup_2026-09-27/review/dependencies/scan_dependencies.py > udt_repository_cleanup_2026-09-27/review/dependencies/scan.stdout 2> udt_repository_cleanup_2026-09-27/review/dependencies/scan.stderr
python3 udt_repository_cleanup_2026-09-27/review/dependencies/verify_inventory_independent.py > udt_repository_cleanup_2026-09-27/review/dependencies/inventory.stdout 2> udt_repository_cleanup_2026-09-27/review/dependencies/inventory.stderr
python3 udt_repository_cleanup_2026-09-27/review/dependencies/check_builder_guards.py > udt_repository_cleanup_2026-09-27/review/dependencies/builder_guards.stdout 2> udt_repository_cleanup_2026-09-27/review/dependencies/builder_guards.stderr
```

The search helper scans only tracked text matching declared suffix/hash-manifest patterns, explicitly excluding all four protected directories. It emits literal matches, not automatically classified dependencies. Manifest consumers and selected code contexts were then inspected. The initial 23-name scan was expanded to55 after candidate coordination with the surface reviewer. A later supplemental two-name probe is summarized in SUPPLEMENTAL_DEPENDENCY_CLASSIFICATION.tsv; it did not regenerate the large literal capture.

Initial scanner failure (preserved diagnostic, no output table had been written):

```text
scan_dependencies.py, main, source, number, text = line.split(":", 2)
ValueError: not enough values to unpack (expected 3, got 1)
```

Cause: `splitlines()` also splits Unicode paragraph separators embedded in source lines. Repair: split only on newline. Initial suffix omissions of .sha256 and extensionless hash manifests were corrected before clearance; resulting native-stability fixed-Git manifest and cold-start trial snapshot references were traced. No protected content was inspected.

Two exploratory path probes returned file-not-found: obsolete root test_startup_surface.py (actual path tests/test_startup_surface.py), and nonexistent relational_phi classify_active_results.py (review used actual verify_regrade.py and verify_regrade_independent.py). These were discovery misses, not passing checks or omitted dependency objections.

Inventory review initially found immutable-metadata override risk. Parent repaired it before archival work; actual builder guard checking passed one valid synthetic archive case and rejected15 malformed overrides. The independent inventory checker passed33380 baseline paths,1147 root rows and799 group rows, rejecting13 in-memory corruptions. Those are separate maintenance implementations, not independent scientific evidence. Synthetic fixtures are declared and never counted as true independent reviews.

No whole scientific package validator, numerical campaign, full premise verifier, or protected source parser was executed by this reviewer. Parent integrated checks and final construction remain separate evidence.
