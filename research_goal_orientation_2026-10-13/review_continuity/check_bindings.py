#!/usr/bin/env python3
"""Reviewer-owned byte/inheritance check; no scientific interpretation."""
import hashlib
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AREA = Path(__file__).resolve().parent
PROTECTED = (
    "udt_native_onshell_timelive_reset_owner_audit_2026-08-10/",
    "udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12/",
    "udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12/",
    "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/",
)
EXPECTED_CHANGED = {
    "AGENTS.md", "CLAUDE.md", "HANDOFF.md", "LIVE.md",
    "UDT_RESEARCH_OPERATING_PLAN.md", "UDT_RESEARCH_ROADMAP.md",
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def safe(path, unrelated):
    p = Path(path)
    assert not p.is_absolute() and ".." not in p.parts
    assert not path.startswith((".git/", *PROTECTED))
    assert path not in unrelated
    q = ROOT / p
    resolved = q.resolve().relative_to(ROOT).as_posix()
    assert not resolved.startswith((".git/", *PROTECTED))
    assert resolved not in unrelated and q.is_file()
    return q


def main():
    freeze_path, expected_hash, receipt_name = sys.argv[1:]
    assert Path(receipt_name).name == receipt_name
    freeze_bytes = (ROOT / freeze_path).read_bytes()
    assert sha(freeze_bytes) == expected_hash
    freeze = json.loads(freeze_bytes)
    base = json.loads((ROOT / "research_goal_orientation_2026-10-13/BASELINE.json").read_bytes())
    unrelated = set(base["existing_untracked_names_only"])
    accepted = freeze["accepted_sha256"]
    # Screen every name/resolved path before reading any accepted payload.
    safe_paths = {p: safe(p, unrelated) for p in accepted}
    prior_bytes = safe_paths[freeze["prior_review_record"]].read_bytes()
    assert sha(prior_bytes) == freeze["prior_review_record_sha256"]
    assert prior_bytes == git("show", base["head"] + ":development_reconstruction_2026-09-29/REVIEW_RECORD.json")
    prior = json.loads(prior_bytes)["accepted_sha256"]
    changed = sorted(p for p in accepted.keys() & prior.keys() if accepted[p] != prior[p])
    added = sorted(accepted.keys() - prior.keys())
    removed = sorted(prior.keys() - accepted.keys())
    unchanged = sum(accepted[p] == prior[p] for p in accepted.keys() & prior.keys())
    assert changed == sorted(freeze["inherited_changed"]) == sorted(EXPECTED_CHANGED)
    assert added == sorted(freeze["added"])
    assert removed == sorted(freeze["removed"]) == []
    assert unchanged == freeze["inherited_unchanged_count"] == 14624
    mismatches = []
    total = 0
    for p, q in safe_paths.items():
        digest = hashlib.sha256()
        with q.open("rb") as stream:
            while chunk := stream.read(1024 * 1024):
                total += len(chunk)
                digest.update(chunk)
        if digest.hexdigest() != accepted[p]:
            mismatches.append(p)
    tracked_diff = git("diff", "--name-only", base["head"]).decode().splitlines()
    assert set(tracked_diff) == EXPECTED_CHANGED
    current_untracked = set(git("ls-files", "--others", "--exclude-standard", "-z").decode().rstrip("\0").split("\0"))
    missing_unrelated = sorted(unrelated - current_untracked)
    assert not mismatches and not missing_unrelated
    receipt = {
        "utc": datetime.now(timezone.utc).isoformat(),
        "context": "/root/goal_method_continuity",
        "python": platform.python_version(),
        "git_version": git("--version").decode().strip(),
        "status": "PASS",
        "command": "python3 " + str(Path(__file__).relative_to(ROOT)) + " " + " ".join(sys.argv[1:]),
        "freeze_path": freeze_path,
        "freeze_sha256": expected_hash,
        "head": git("rev-parse", "HEAD").decode().strip(),
        "branch": git("branch", "--show-current").decode().strip(),
        "accepted_count": len(accepted),
        "inherited_unchanged_count": unchanged,
        "inherited_changed": changed,
        "added": added,
        "removed": removed,
        "prior_record_matches_baseline_git_bytes": True,
        "protected_and_unrelated_screened_before_payload_hashing": True,
        "unrelated_names_preserved": len(unrelated),
        "accepted_bytes_hashed": total,
        "byte_mismatches": mismatches,
        "changed_document_sha256": {p: accepted[p] for p in sorted(EXPECTED_CHANGED)},
        "limits": "Byte correspondence and inherited map consistency only; not reproof, semantic completeness, chronology, current remote freshness, or independent scientific implementation.",
    }
    (AREA / receipt_name).write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
