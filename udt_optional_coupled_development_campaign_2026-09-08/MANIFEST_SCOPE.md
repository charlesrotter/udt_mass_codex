# Evidence-manifest scope

EVIDENCE_SHA256SUMS, generated only after numerical/audit processes finish,
uses repository-root-relative paths. It covers every file in this owned
campaign package at the final evidence freeze EXCEPT itself and the mutable
COMPLETION_RECORD.md. The latter records actual post-freeze commit/push
receipts and is preserved/versioned by git rather than self-hashed.

The manifest includes original and review code, raw stdout/stderr, structured
capture records, questions/work order, both scientific review histories,
false-pass evidence, reviewed wrappers/decision brief, the compact log and
source/dependency/initial manifests. Ignored stdout must be staged explicitly.
The five maintained current-status files are outside this package manifest;
their exact reviewed versions are pinned in step_02/FINAL_FIDELITY_REVIEW.md
and the delivery commit. No protected payload belongs to this inventory.

Correspondence is not truth, independence, chronology, acceptance or canon.
The initial scientific manifests are never regenerated to hide a change.
No additional candidate/review file may be silently omitted from this final
inventory. Any later scientific edit requires its own visible review history.
