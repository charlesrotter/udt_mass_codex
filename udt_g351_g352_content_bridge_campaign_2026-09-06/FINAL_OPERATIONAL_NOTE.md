# Final read-only lookup diagnostic

At20:55:58 UTC the parent attempted to locate the pending closure note with
an unnecessarily broad filename-only command:

    rg --files --hidden --no-ignore /tmp -g '*CLOSURE_FIDELITY.md' -g '*closure*' -g '!udt_kernel*' -g '!udt_native*' -g '!udt_pair*' -g '!udt_sne*'

It returned exit2, reporting Permission denied for systemd/snap private temporary
directories and listing filenames from unrelated temporary trees. The tool
returned truncated output (reported4294 original tokens, output budget1000);
this note does not claim an untruncated independent capture. The original tool
event remains in the conversation record. No file payload was opened by this
lookup and no filesystem/Git state changed. No result from those unrelated
trees was used as scientific evidence or as preservation proof.

The broad lookup was stopped, not retried with higher permission. Subsequent
receipt uses only the exact fresh closure directory supplied by its reviewer.
This was a scope/operational mistake in filename discovery, not a mathematical
failure or an actual blocker. It establishes nothing about backups or the
disposition of pre-reboot unsaved work; both remain UNVERIFIED.

A later read-only display used the abbreviated, nonexistent filename
step_04/FROZEN_SHA256SUMS. sed reported "No such file or directory"; the
surrounding display command's final exit was 0 and is NOT treated as proof
that this individual read succeeded. Scoped filename discovery located the
actual FROZEN_CANDIDATE_SHA256SUMS. Final checks use that exact path. No data
was changed by the failed display.

An extra check of Step2 review's STAGE_A_SOURCE_SHA256SUMS returned exit1:
its 28 other entries matched, but its historical CAMPAIGN_LOG.md exposure
hash did not match the later maintained log. FINAL_METADATA.json explicitly
labels that hash historical exposure, not a current-status lock. Git at
9fb783cb reproduces the recorded log hash exactly. FINAL_SCOPE_AUDIT.json
preserves the actual repeated mismatch, historical comparison and final
source/freeze/archive checks; it does not convert the current-log mismatch
into a pass. The initial orchestration stopped at the extra check before
saving its accumulated records, so the final audit is a disclosed actual rerun.
While locating that metadata, an rg request also named a nonexistent
STAGE_A_SOURCE_METADATA.json; scoped filename discovery located the actual
FINAL_METADATA.json. The missing-path diagnostic changed no state or evidence.
