# Evidence-seal scope

EVIDENCE_SHA256SUMS seals the six reviewed current pages and every audit
payload present at the evidence freeze. Paths are relative to the repository
root. It excludes itself, PUBLICATION.md and publication_* capture files:
those are self-referential or later operational commit/push/replay receipts,
not added scientific evidence. Their actual versions are preserved in Git.

All original reviewer seals and stdout/stderr are included, including the
explicitly post-hoc reconstructed initial warning. Source pins distinguish
the fixed baseline from changed current pages. A later authorized current
page edit does not rewrite this snapshot; authenticate its historical bytes
at the recorded evidence commit. Hashes show correspondence, not scientific
truth, independence or externally trusted chronology. No full-registry PASS
or scientific promotion is implied by sealing or publication.
