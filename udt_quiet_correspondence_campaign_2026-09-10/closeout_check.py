"""Read-only correspondence/preservation checks, not scientific proof."""

import hashlib
import json
import subprocess

BASELINE = "2a3e64befd72b801cdd54e528d9a7c68362cdd7b"
PACKAGE = "udt_quiet_correspondence_campaign_2026-09-10/"
ALLOWED = {
    "LIVE.md", "HANDOFF.md", "CURRENT_RESEARCH_PROGRAM.md",
    "CURRENT_SCIENTIFIC_PREMISES.md", "INDEX.md", "MEMORY.md",
    "UDT_RESEARCH_ROADMAP.md",
}


def git(*args):
    return subprocess.check_output(
        ["git", "-c", "index.threads=1", "-c", "core.preloadIndex=false", *args],
        text=True,
    )


assert git("branch", "--show-current").strip() == "grok"
changed = git("diff", "--name-only", BASELINE).splitlines()
assert all(p in ALLOWED or p.startswith(PACKAGE) for p in changed), changed
git("diff", "--check", BASELINE)
status = git("status", "--short").splitlines()
unrelated = sorted(s for s in status if s.startswith("?? ") and not s[3:].startswith(PACKAGE))
fingerprint = hashlib.sha256("\n".join(unrelated).encode()).hexdigest()
assert len(unrelated) == 46, len(unrelated)
assert fingerprint == "d65d71d63a56b95aabfd61f33317b1f1f2b2a62a85ded8258c525b99a5e156ea", fingerprint

for step in ("step_01", "step_02"):
    for manifest in ("SOURCE_SHA256SUMS", "CANDIDATE_SHA256SUMS", "review/REVIEW_SHA256SUMS"):
        subprocess.run(["sha256sum", "-c", PACKAGE + step + "/" + manifest], check=True)

print(json.dumps({
    "status": "PASS; byte correspondence and scoped Git/status checks only",
    "baseline": BASELINE,
    "head": git("rev-parse", "HEAD").strip(),
    "branch": "grok",
    "changed_tracked_paths": changed,
    "unrelated_untracked_count": len(unrelated),
    "unrelated_status_names_sha256": fingerprint,
    "protected_payloads": "not opened or hashed; status-name preservation only",
    "source_candidate_review_manifest_entries": 47,
    "full365": "separate actual run FAILED G325; not waived or rerun here",
    "backup_and_pre_reboot_unsaved_state": "UNVERIFIED",
}, indent=2, sort_keys=True))
