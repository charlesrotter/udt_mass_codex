# Post-review binding correction

The first parent binding helper stopped before writing REVIEW_RECORD.json: it
incorrectly required the literal FINAL_IMMUTABLE in each prose report, although
the mathematical reviewer supplied that status in the signed-by-context JSON
attestation and explicit final message. The reports themselves were already
final and their recorded hashes matched. No scientific or frozen source changed.

The inadvertently following checks/final_normal run consequently failed with
REVIEW_REQUIRED on CURRENT_RESEARCH_PROGRAM.md, exactly as an unbound edition
should. Its output/receipt remain preserved; it is not counted as a successful
normal check. The corrected helper validates FINAL_IMMUTABLE in the actual
attestation, the common accepted map, each actual freeze field name, and report
hash, then writes the parent review binding. The two attestations use equivalent
freeze_sha256 and integration_freeze_sha256 field names; the helper respects
both without modifying either reviewer record.

checks/final_normal_bound is the required subsequent normal verification. The
banking manifest requires that successful receipt, maintenance and full406 before
staging. This is a parent packaging correction, not a scientific repair or new
review verdict; no result, premise, accepted-map byte or final report is changed.
