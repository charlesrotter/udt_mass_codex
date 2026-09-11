"""Read-only correspondence and scoped publication check; no scientific verification."""
from pathlib import Path
import datetime
import hashlib
import json
import subprocess

repo = Path(__file__).resolve().parents[1]
package = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=repo, text=True)


counts = {}
for name, base in [
    ("CANDIDATE_FREEZE.json", package),
    ("PRECOMPUTATION_FREEZE.json", repo),
    ("SOURCE_PINS.json", repo),
    ("review/REVIEW_RECEIPT.json", repo),
]:
    pins = json.loads((package / name).read_text())["sha256"]
    for path, digest in pins.items():
        assert sha(base / path) == digest, (name, path)
    counts[name] = len(pins)

head = git("rev-parse", "HEAD").strip()
origin = git("rev-parse", "origin/grok").strip()
branch = git("branch", "--show-current").strip()
assert branch == "grok"
assert head == origin == "1de84bf0e8b8781201ede8d0486489a22dbf7d07"
status = git("status", "--porcelain=v1", "--untracked-files=normal")
unrelated = "".join(
    line + "\n" for line in status.splitlines()
    if line.startswith("?? ") and not line.endswith(package.name + "/")
)
fingerprint = hashlib.sha256(unrelated.encode()).hexdigest()
assert fingerprint == "55e7c4508622f912730f9c068cc571c370b3977bc1110eb0a48a8218dbe024c2"
navigation = ["CURRENT_RESEARCH_PROGRAM.md", "HANDOFF.md", "INDEX.md", "LIVE.md", "UDT_RESEARCH_ROADMAP.md"]
assert sorted(git("diff", "--name-only").splitlines()) == navigation
assert not git("diff", "--cached", "--name-only").strip()
assert subprocess.check_output(
    ["git", "show", head + ":CURRENT_SCIENTIFIC_PREMISES.tsv"], cwd=repo
) == (repo / "CURRENT_SCIENTIFIC_PREMISES.tsv").read_bytes()
source_lines = (repo / "udt_ti1_banking_2026-09-11/SOURCE_EVIDENCE_SHA256SUMS").read_text().splitlines()
for line in source_lines:
    digest, path = line.split(None, 1)
    assert sha(repo / path.strip()) == digest, path
assert len(source_lines) == 103
print(json.dumps({
    "verified_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "verdict": "PASS", "branch": branch, "HEAD": head, "local_origin_grok": origin,
    "network_evidence": "banking push completion collected at13:47:22UTC; TI2 publication future",
    "verified_pin_counts": counts, "candidate_unchanged": True,
    "original_TI1_source_files_preserved": len(source_lines),
    "current396_registry_byte_identical_to_banked_HEAD": True,
    "original_unrelated_status_entry_count": len(unrelated.splitlines()),
    "original_unrelated_status_sha256": fingerprint,
    "exact_tracked_change_paths": navigation,
    "protected_payloads": "not inspected; status names only",
    "backup_completeness": "UNVERIFIED", "pre_reboot_unsaved_state": "UNVERIFIED",
}, indent=2))
