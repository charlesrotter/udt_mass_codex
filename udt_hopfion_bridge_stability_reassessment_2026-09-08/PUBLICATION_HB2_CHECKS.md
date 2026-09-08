# HB2 publication-format diagnostic — evidence unchanged

At staging,108 newly added files belonged exclusively to step_02; its two
question/dispatch files were already tracked. The frozen109-payload seal
passed before staging and remains unchanged. No unrelated path was staged.

The actual `git diff --cached --check` returned2. Its complete diagnostic is
preserved in publication_hb2_whitespace.stdout with automatic command/resource
JSON and empty stderr. This is NOT a passed whole-index whitespace check.
Initial console display was truncated; the subsequent saved invocation was not.

All196 warnings were independently classified from the complete saved output:

| File within step_02/review | Warnings | Actual reason |
|---|---|---|
| REVIEW_ARTIFACT_MANIFEST.tsv |90|Valid original CRLF TSV record endings|
| SOURCE_FIRST_MANIFEST.tsv |63|Valid original CRLF TSV record endings|
| SOURCE_SNAPSHOT_MANIFEST.tsv |40|Valid original CRLF TSV record endings|
| source_snapshots/...banking.../prebank_356.json |1|Preserved extra final blank line in original receipt|
| source_snapshots/...banking.../prebank_356.stdout |1|Same original serialization caveat|
| source_snapshots/...arc_recovery.../MASS_BRANCH_AUTHORITY_MAP.tsv |1|Original source's final blank line|

For each TSV, actual CRLF count and total CR count equal the warning count;
there are no other carriage returns. Both review payload manifests parse as
TSV and every listed hash/size matches its file. The three snapshot endings
match the original hashed sources. No other staged file generated a warning.

The original frozen review evidence and source snapshots are committed
UNCHANGED, retaining these serialization-only warnings. No scientific test,
review objection, source mismatch or permission gate is waived. No historical
artifact or review seal was normalized/repaired for cosmetic acceptance.
These publication diagnostics are after the root scientific seal and remain
separately committed operational evidence, not additional scientific support.
