#!/usr/bin/env python3
"""Read-only authentication of the original NCB1 evidence and historical pins."""
from pathlib import Path
import csv
import datetime
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parents[2]
BASE = "fd6a28e6c9ee72b1d6e19e0c2e8d03c645e9a8e1"
SOURCE = "udt_ne1_clock_beam_geometry_2026-09-12"
BANK = "udt_ncb1_banking_2026-09-12"

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)

def blob(commit, path):
    return git("show", f"{commit}:{path}")

def manifest(raw):
    pairs = [line.split("  ", 1) for line in raw.decode().splitlines() if line]
    assert len({path for _, path in pairs}) == len(pairs)
    return pairs

head = git("rev-parse", "HEAD").decode().strip()
branch = git("branch", "--show-current").decode().strip()
assert head == BASE and branch == "grok"
source_manifest = (ROOT/BANK/"SOURCE_EVIDENCE_SHA256SUMS").read_bytes()
pairs = manifest(source_manifest)
tracked = set(git("ls-tree", "-r", "--name-only", BASE, "--", SOURCE).decode().splitlines())
assert set(p for _, p in pairs) == tracked and len(pairs) == 87
for expected, path in pairs:
    current = (ROOT/path).read_bytes()
    assert sha(current) == expected and current == blob(BASE, path), path

source_pins = list(csv.DictReader((ROOT/SOURCE/"SOURCE_PINS.tsv").read_text().splitlines(), delimiter="\t"))
assert len(source_pins) == 22
for pin in source_pins:
    assert sha(blob(BASE, pin["path"])) == pin["sha256"], pin["path"]

freeze = json.loads((ROOT/SOURCE/"INITIAL_FREEZE.json").read_text())
for name, expected in freeze["sha256"].items():
    assert sha((ROOT/SOURCE/name).read_bytes()) == expected, name
assert freeze["sha256"]["INITIAL_CANDIDATE.md"] == "8f58d15f3e24bf8878fca2af5c24c95cb7c68dec49bfb2fa175fbe945b54879f"

edits = json.loads((ROOT/SOURCE/"EDITORIAL_CLARIFICATION.json").read_text())
texts = {change["path"]: (ROOT/SOURCE/change["path"]).read_text() for change in edits["changes"]}
for change in reversed(edits["changes"]):
    current = texts[change["path"]]
    assert sha(current.encode()) == change["after_sha256"]
    assert current.count(change["new"]) == 1
    previous = current.replace(change["new"], change["old"], 1)
    assert sha(previous.encode()) == change["before_sha256"]
    texts[change["path"]] = previous
assert len(edits["changes"]) == 3 and edits["scientific_repairs"] == 0

publication = json.loads((ROOT/SOURCE/"PUBLICATION.json").read_text())
evidence_commit = publication["evidence_commit"]["head"]
original_manifest = manifest((ROOT/SOURCE/"SHA256SUMS").read_bytes())
for expected, path in original_manifest:
    assert sha(blob(evidence_commit, path)) == expected, path
assert len(original_manifest) == 91
assert publication["evidence_commit"]["returncode"] == publication["evidence_push"]["returncode"] == 0

receipt = json.loads((ROOT/SOURCE/"checks/current_full397.json").read_text())
stdout = (ROOT/SOURCE/"checks/current_full397.stdout").read_bytes()
assert receipt["command"] == ["python3", "verify_current_scientific_premises.py"]
assert receipt["started_utc"] == "2026-09-12T17:25:43.776954+00:00"
assert receipt["returncode"] == 0 and receipt["timeout"] is False
assert receipt["duration_seconds"] == 404.72793896193616
assert b"PASS: 397-row premise registry" in stdout and b"G414/TI2" in stdout
assert (ROOT/SOURCE/"checks/current_full397.stderr").read_bytes() == b""
registry = blob(BASE, "CURRENT_SCIENTIFIC_PREMISES.tsv")
assert sha(registry) == "2c27fa4b8931672c44b4d778aab0f2a2631c04a5c586358340db1dc763b74f7e"
assert len(registry.splitlines()) == 398
rows = list(csv.DictReader(registry.decode().splitlines(), delimiter="\t"))
required = {r["premise_id"]: sha((json.dumps(r, sort_keys=True)+"\n").encode()) for r in rows if r["premise_id"] in {"G220", "G312", "G342", "G348", "G394"}}
assert len(required) == 5
print(json.dumps({
    "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "reviewer": "/root/ncb1_banking_review", "branch": branch, "head": head,
    "verdict": "PASS_SOURCE_CORRESPONDENCE_NOT_SCIENTIFIC_REPROOF",
    "parent_startup": "Attributed WORK_ORDER/LAUNCH; no duplicate top-level startup/sync/audit",
    "source_package_files": len(pairs), "source_manifest_sha256": sha(source_manifest),
    "source_package_all_match_baseline": True,
    "historical_source_pins_authenticated_at_baseline": len(source_pins),
    "initial_freeze_unchanged": True, "editorial_reverse_hash_chain_changes": 3,
    "original_manifest_historical_commit": evidence_commit,
    "original_manifest_entries_authenticated": len(original_manifest),
    "prebank_full397_receipt": receipt, "prebank_stdout_sha256": sha(stdout),
    "original397_sha256": sha(registry), "required_row_structured_sha256": required,
    "runtime_model_version": "UNATTESTED", "general_capacity": "UNVERIFIED",
    "protected_payloads": "NOT read or hashed", "science_programs_rerun": 0,
    "new_parent_claim_or_guard_exposure": "NONE before direct invitation"
}, indent=2))
