# CES1 review-binding setup failure and bounded repair

Both real final attestations accepted the identical integration freeze and128
hash map. The parent assembler additionally expected a `freeze_sha256` metadata
key in each attestation. The fidelity attestation instead uses the equally
explicit `integration_freeze_sha256` key. At 2026-09-30T14:54 UTC the assembler
raised `KeyError: 'freeze_sha256'` before writing REVIEW_RECORD.json. No reviewed
source or review verdict was changed.

The orchestration incorrectly continued after that command failure. Consequently
checks/development_final.* records exit1 with REVIEW_REQUIRED under the old
review record, and a full-audit attempt using checks/premise_final was launched
prematurely. It was interrupted through its exact tool session (30876), which
returned exit130. Its existing capture provenance is preserved; it has no
successful completion receipt and supplies no audit acceptance. This interrupted
attempt is not a scientific failure or a completed failed full406 audit.

The bounded repair is to validate each actual attestation's stated freeze-hash
key, check identical accepted maps and report hashes, then bind the unchanged
actual reviews. No attestation is rewritten and no candidate hash is refreshed.
The repaired binder is executed separately; only its successful result permits
the normal guard. A successful normal guard then permits a new full audit under
a distinct capture prefix, preserving the failed/interrupted artifacts. This
repairs execution ordering and metadata handling, not mathematics or physics.
