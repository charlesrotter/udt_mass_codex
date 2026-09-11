"""Seal the reviewed TI2 checkpoint before publication; not a scientific check."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import subprocess

repo = Path(__file__).resolve().parents[1]
package = Path(__file__).resolve().parent
baseline = "1de84bf0e8b8781201ede8d0486489a22dbf7d07"
navigation = ["CURRENT_RESEARCH_PROGRAM.md", "HANDOFF.md", "INDEX.md", "LIVE.md", "UDT_RESEARCH_ROADMAP.md"]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=repo, text=True)


def write_json(name, value):
    (package / name).write_text(json.dumps(value, indent=2) + "\n")


assert not (package / "PREPUBLICATION_RECEIPT.json").exists(), "Preserve any prior seal; do not overwrite"
assert git("branch", "--show-current").strip() == "grok"
assert git("rev-parse", "HEAD").strip() == baseline
assert git("rev-parse", "origin/grok").strip() == baseline
assert sorted(git("diff", "--name-only").splitlines()) == navigation
assert not git("diff", "--cached", "--name-only").strip()
final = json.loads((package / "review/FINAL_FIDELITY_RECEIPT.json").read_text())
assert final["scientific_repairs_required"] == 0
assert "TI2_CONDITIONAL_UNPROMOTED" in final["disposition"]
for name, digest in final["sha256"].items():
    assert sha(repo / name) == digest, name
for record, base in [("CANDIDATE_FREEZE.json", package), ("SOURCE_PINS.json", repo)]:
    for name, digest in json.loads((package / record).read_text())["sha256"].items():
        assert sha(base / name) == digest, name
status = git("status", "--porcelain=v1", "--untracked-files=normal")
unrelated = "".join(line + "\n" for line in status.splitlines()
                    if line.startswith("?? ") and not line.endswith(package.name + "/"))
fingerprint = hashlib.sha256(unrelated.encode()).hexdigest()
assert fingerprint == "55e7c4508622f912730f9c068cc571c370b3977bc1110eb0a48a8218dbe024c2"
now = datetime.datetime.now(datetime.timezone.utc)
assert now < datetime.datetime(2026, 9, 11, 16, 0, 50, tzinfo=datetime.timezone.utc)
write_json("COMPLETION_SEAL.json", {
    "sealed_utc": now.isoformat(), "combined_launch_utc": "2026-09-11T13:00:50Z",
    "hard_return_utc": "2026-09-11T16:00:50Z", "science_and_review": "COMPLETE",
    "TI1": "G413_BANKED", "TI2": "VERIFIED-WITH-CAVEATS_CONDITIONAL_UNPROMOTED",
    "scientific_repairs_after_candidate_freeze": 0,
    "actual_new_context_count": 2,
    "allocations": [
        {"context": "/root/ti1_banking_review", "first_observed_utc": "2026-09-11T13:04:34Z",
         "final_seal_utc": "2026-09-11T13:43:25.874357Z", "status": "COMPLETED",
         "overlap": "parent banking integration"},
        {"context": final["context"], "allocation_bracket_utc": ["2026-09-11T13:47:22Z", "2026-09-11T13:47:55Z"],
         "first_observed_utc": final["first_observed_utc"], "final_seal_utc": final["completed_utc"],
         "status": "COMPLETED", "overlap": "parent construction/checking/closeout; no overlap with banking reviewer"},
    ],
    "capacity": "only actual allocations established; restored/general capacity UNVERIFIED; no limit recurred",
    "configured_parent": "gpt-6-astra/xhigh observed earlier; no override",
    "runtime_model_version": "UNATTESTED",
    "final_fidelity_receipt_sha256": sha(package / "review/FINAL_FIDELITY_RECEIPT.json"),
    "final_fidelity_pins_verified": len(final["sha256"]),
    "full396": "ACTUAL_PASS_402.836033429s_at_banked_snapshot",
    "later_navigation": "ACTUAL_539_PASS_1_DUPLICATE_FULL_WRAPPER_DESELECTED",
    "original46_name_status_sha256": fingerprint,
    "next_study": "PROPOSED_NOT_AUTHORIZED; stop for lay discussion",
    "backup_completeness": "UNVERIFIED", "pre_reboot_unsaved_state": "UNVERIFIED",
    "publication": "FUTURE_AT_SEAL; staging, commit and push require actual collection",
})
exclude = {"ARTIFACT_SHA256SUMS", "PREPUBLICATION_RECEIPT.json"}
paths = set(navigation)
for directory, dirs, names in os.walk(package):
    dirs[:] = [d for d in dirs if d not in {"__pycache__", ".pytest_cache"}]
    for name in names:
        path = Path(directory) / name
        assert not path.is_symlink(), path
        if path.parent == package and name in exclude:
            continue
        paths.add(str(path.relative_to(repo)))
scope_path = str((package / "PUBLICATION_SCOPE.json").relative_to(repo))
paths.add(scope_path)
write_json("PUBLICATION_SCOPE.json", {
    "baseline_head": baseline, "manifest_paths": sorted(paths),
    "additional_seal_paths": [str((package / name).relative_to(repo)) for name in sorted(exclude)],
    "stage_command": ["git", "add", "-f", "--", "EACH_EXPLICIT_PATH_IN_THIS_RECORD"],
    "root_scope": navigation, "new_science_grade": "TI2_UNPROMOTED",
})
manifest = "".join(sha(repo / name) + "  " + name + "\n" for name in sorted(paths))
(package / "ARTIFACT_SHA256SUMS").write_text(manifest)
write_json("PREPUBLICATION_RECEIPT.json", {
    "sealed_utc": now.isoformat(), "command": ["python3", str(Path(__file__).relative_to(repo))],
    "branch": "grok", "baseline_head": baseline, "manifest_entries": len(paths),
    "manifest_sha256": sha(package / "ARTIFACT_SHA256SUMS"),
    "reviewed_final_pins_unchanged": len(final["sha256"]),
    "candidate_and_source_pins_unchanged": True, "original46_name_status_sha256": fingerprint,
    "TI2": "UNPROMOTED", "publication": "FUTURE_AT_SEAL; do not infer commit/push success",
    "outcome_metadata_review": "parent-owned after final fidelity, no scientific/doc mutation",
})
print(json.dumps({"verdict": "SEALED", "manifest_entries": len(paths),
                  "staging_expected_paths": len(paths) + 2, "final_review_pins": len(final["sha256"]),
                  "manifest_sha256": sha(package / "ARTIFACT_SHA256SUMS")}, indent=2))
