"""Parent-owned outcome seal after final banking fidelity; no new scientific claim."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import subprocess
import sys

repo = Path(__file__).resolve().parents[1]
package = Path(__file__).resolve().parent
sys.path.insert(0, str(repo))
import ti2_banking_guard as guard

baseline = "b95ace99315b816b9a53abe8102b478d1e1cd188"
roots = ["AGENTS.md", "CURRENT_RESEARCH_PROGRAM.md", "CURRENT_SCIENTIFIC_PREMISES.md",
         "CURRENT_SCIENTIFIC_PREMISES.tsv", "HANDOFF.md", "INDEX.md", "LIVE.md", "MEMORY.md",
         "UDT_RESEARCH_ROADMAP.md", "tests/test_startup_surface.py", "tests/test_ti1_banking.py",
         "tests/test_ti2_banking.py", "ti1_banking_guard.py", "ti2_banking_guard.py",
         "verify_current_scientific_premises.py"]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=repo, text=True)


def write(name, value):
    (package / name).write_text(json.dumps(value, indent=2) + "\n")


assert not (package / "PREPUBLICATION_RECEIPT.json").exists(), "Preserve prior seals"
assert git("branch", "--show-current").strip() == "grok"
assert git("rev-parse", "HEAD").strip() == git("rev-parse", "origin/grok").strip() == baseline
review_path = package / "review/FINAL_FIDELITY_RECEIPT.json"
review = json.loads(review_path.read_text())
for path, digest in review["sha256"].items():
    assert sha(repo / path) == digest, path
guard.validate_ti2_banking(repo)
full = json.loads((package / "checks/full397.json").read_text())
nav = json.loads((package / "checks/final_navigation.json").read_text())
assert full["returncode"] == nav["returncode"] == 0
assert not full["timeout"] and not nav["timeout"]
assert "PASS: 397-row premise registry" in (package / "checks/full397.stdout").read_text()
assert "592 passed, 1 deselected" in (package / "checks/final_navigation.stdout").read_text()
assert not (package / "checks/full397.stderr").read_bytes()
assert not (package / "checks/final_navigation.stderr").read_bytes()
status = git("status", "--porcelain=v1", "--untracked-files=normal")
unrelated = "".join(line + "\n" for line in status.splitlines()
                    if line.startswith("?? ") and not line[3:].startswith(package.name + "/")
                    and line[3:] not in {"ti2_banking_guard.py", "tests/test_ti2_banking.py"})
fingerprint = hashlib.sha256(unrelated.encode()).hexdigest()
assert fingerprint == "55e7c4508622f912730f9c068cc571c370b3977bc1110eb0a48a8218dbe024c2"
now = datetime.datetime.now(datetime.timezone.utc)
assert now < datetime.datetime(2026, 9, 11, 19, 36, 7, tzinfo=datetime.timezone.utc)
write("ALLOCATION_CLOSE.json", {
    "recorded_utc": now.isoformat(), "banking_context": "/root/ti2_banking_fidelity",
    "first_observed_utc": "2026-09-11T18:54:40Z",
    "final_fidelity_seal_utc": review.get("sealed_utc", review.get("completed_utc")),
    "status": "COMPLETED", "overlap": "parent banking construction/integration/closeout",
    "actual_new_contexts_so_far": 1, "later_TI3_reviewer": "NOT_YET_ALLOCATED",
    "old_contexts": "retained and unused", "runtime_model_version": "UNATTESTED",
    "capacity": "actual allocation only; restored/general capacity UNVERIFIED",
    "TI3": "AUTHORIZED_NOT_STARTED; actual start after banking publication",
})
exclude = {"ARTIFACT_SHA256SUMS", "PREPUBLICATION_RECEIPT.json"}
paths = set(roots)
for directory, dirs, names in os.walk(package):
    dirs[:] = [name for name in dirs if name not in {"__pycache__", ".pytest_cache"}]
    for name in names:
        path = Path(directory) / name
        assert not path.is_symlink(), path
        if path.parent == package and name in exclude:
            continue
        paths.add(str(path.relative_to(repo)))
paths.add(str((package / "PUBLICATION_SCOPE.json").relative_to(repo)))
write("PUBLICATION_SCOPE.json", {
    "baseline_head": baseline, "root_paths": roots, "manifest_paths": sorted(paths),
    "additional_seal_paths": [str((package / name).relative_to(repo)) for name in sorted(exclude)],
    "TI2": "G414_ACCEPTED_AT_ENTIRE_REVIEWED_CONDITIONAL_SCOPE", "TI3": "EXCLUDED_FROM_THIS_COMMIT",
})
(package / "ARTIFACT_SHA256SUMS").write_text(
    "".join(sha(repo / path) + "  " + path + "\n" for path in sorted(paths)))
write("PREPUBLICATION_RECEIPT.json", {
    "sealed_utc": now.isoformat(), "command": ["python3", str(Path(__file__).relative_to(repo))],
    "baseline_head": baseline, "manifest_entries": len(paths),
    "manifest_sha256": sha(package / "ARTIFACT_SHA256SUMS"),
    "final_fidelity_receipt_sha256": sha(review_path), "final_fidelity_pins_verified": len(review["sha256"]),
    "full397_seconds": full["duration_seconds"], "final_navigation_seconds": nav["duration_seconds"],
    "final_navigation": "ACTUAL592_PASS_1_DUPLICATE_FULL_WRAPPER_DESELECTED",
    "original46_status_sha256": fingerprint, "source120_and_original396": "AUTHENTICATED",
    "publication": "FUTURE_AT_SEAL; observe actual staging/commit/push completion",
    "backup_completeness": "UNVERIFIED", "pre_reboot_unsaved_state": "UNVERIFIED",
})
print(json.dumps({"verdict": "SEALED", "manifest_entries": len(paths),
                  "staging_expected_paths": len(paths) + 2,
                  "manifest_sha256": sha(package / "ARTIFACT_SHA256SUMS")}, indent=2))
