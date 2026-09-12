#!/usr/bin/env python3
"""Authenticate actual final artifacts and seal final fidelity before publication."""
from pathlib import Path
import ast
import datetime
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parents[2]
BANK = ROOT/"udt_ncb1_banking_2026-09-12"
BASE = "fd6a28e6c9ee72b1d6e19e0c2e8d03c645e9a8e1"
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)
def load(path):
    return json.loads(path.read_text())

freeze = load(BANK/"AUDIT_INPUT_FREEZE.json")
assert len(freeze["sha256"]) == 142
assert all(sha(ROOT/path) == expected for path, expected in freeze["sha256"].items())
audit = load(BANK/"checks/full398.json")
completion = load(BANK/"AUDIT_COMPLETION.json")
assert completion["audit_result"] == audit
assert audit["command"] == ["python3", "verify_current_scientific_premises.py"]
assert audit["cwd"] == str(ROOT)
assert audit["started_utc"] == "2026-09-12T19:37:50.444950+00:00"
assert audit["duration_seconds"] == 403.5759908319451
assert audit["returncode"] == 0 and audit["timeout"] is False
assert audit["cpu_seconds"] == 900 and audit["address_space_bytes"] == 2048*1024**2
assert (BANK/"checks/full398.stderr").read_bytes() == b""
out = (BANK/"checks/full398.stdout").read_bytes()
assert b"PASS: 398-row premise registry" in out and b"PASS: G415/NCB1" in out
assert sha(BANK/"checks/full398.stdout") == completion["full398_stdout_sha256"]
provenance = load(BANK/"checks/full398.capture_provenance.json")
assert provenance["command"] == audit["command"]
assert provenance["thread_environment"] == {k: "1" for k in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"]}
assert sha(ROOT/provenance["source"]) == provenance["source_sha256"]
assert sha(ROOT/"udt_reviewed_backlog_banking_2026-09-10/capture_existing.py") == provenance["wrapper_sha256"]
assert datetime.datetime.fromisoformat(freeze["utc"]) < datetime.datetime.fromisoformat(audit["started_utc"])

input_checks = {}
for name in ["running_input_authentication", "completed_input_authentication"]:
    receipt = load(BANK/f"review/checks/{name}.json")
    evidence = load(BANK/f"review/checks/{name}.stdout")
    assert receipt["returncode"] == 0 and not receipt["timeout"]
    assert evidence["freeze_sha256"] == sha(BANK/"AUDIT_INPUT_FREEZE.json")
    assert evidence["declared_audit_inputs"] == 142
    input_checks[name] = receipt

raw = (ROOT/"CURRENT_SCIENTIFIC_PREMISES.tsv").read_bytes()
original = b"".join(line for line in raw.splitlines(keepends=True) if line.split(b"\t", 1)[0] != b"G415")
assert original == git("show", f"{BASE}:CURRENT_SCIENTIFIC_PREMISES.tsv")
assert len(original.splitlines()) == 398 and len(raw.splitlines()) == 399
sources = [line.split("  ", 1) for line in (BANK/"SOURCE_EVIDENCE_SHA256SUMS").read_text().splitlines()]
assert len(sources) == 87 and all(sha(ROOT/path) == expected for expected, path in sources)
launch = load(BANK/"LAUNCH.json")
status = git("status", "--short").decode().splitlines()
assert set(launch["original_untracked_status"]) <= set(status)
assert git("rev-parse", "HEAD").decode().strip() == BASE
assert git("branch", "--show-current").strip() == b"grok"
tracked = [line for line in status if not line.startswith("??")]
assert tracked == freeze["tracked_status"]
direct = load(BANK/"review/REVIEW_RECEIPT.json")
guard = (ROOT/"ncb1_banking_guard.py").read_text()
assignment = next(n for n in ast.parse(guard).body if isinstance(n, ast.Assign)
                  and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "NCB1_PINS")
pins = ast.literal_eval(assignment.value)
for name in ["REVIEW.md", "REVIEW_RECEIPT.json"]:
    key = str((BANK/"review"/name).relative_to(ROOT))
    assert pins[key] == sha(ROOT/key)
    guard = guard.replace(", " + repr(key) + ": " + repr(pins[key]), "", 1)
assert hashlib.sha256(guard.encode()).hexdigest() == direct["reviewed_sha256"]["ncb1_banking_guard.py"]

now = datetime.datetime.now(datetime.timezone.utc)
conservative_start = datetime.datetime(2026, 9, 12, 19, 25, tzinfo=datetime.timezone.utc)
wall_upper_minutes = (now-conservative_start).total_seconds()/60
assert wall_upper_minutes < 40
assert now < datetime.datetime(2026, 9, 12, 20, 25, tzinfo=datetime.timezone.utc)
paths = set(freeze["sha256"])
for name in ["CLOSEOUT.md", "LAY_PROMOTION.md", "AUDIT_COMPLETION.json", "AUDIT_INPUT_FREEZE.json",
             "INTEGRATION_HISTORY.md", "INDEX_CLARIFICATION.json", "LAUNCH.json",
             "checks/full398.json", "checks/full398.stdout", "checks/full398.stderr", "checks/full398.capture_provenance.json"]:
    paths.add(str((BANK/name).relative_to(ROOT)))
for path in (BANK/"review").rglob("*"):
    if path.is_file() and path.suffix != ".pyc" and path.name != "FINAL_FIDELITY_RECEIPT.json" and not path.name.startswith("final_seal"):
        paths.add(str(path.relative_to(ROOT)))
record = {
    "utc": now.isoformat(), "reviewer": "/root/ncb1_banking_review", "head": BASE, "branch": "grok",
    "verdict": "FIDELITY_REVIEWED__VERIFIED_WITH_CAVEATS__EXACT_CONDITIONAL_G415_ACCEPTANCE",
    "unresolved_objections": [], "scientific_repairs": 0,
    "final_sha256": {path: sha(ROOT/path) for path in sorted(paths)},
    "actual_current398_receipt": audit,
    "full398_stdout_sha256": sha(BANK/"checks/full398.stdout"),
    "input_freeze_sha256": sha(BANK/"AUDIT_INPUT_FREEZE.json"),
    "frozen_inputs_authenticated_at_final_seal": 142,
    "independent_running_and_completed_input_captures": input_checks,
    "direct_guard_change": "exactly two review pins; prior bytes reconstructed to direct hash; remaining AST identical in both input checks",
    "original_registry_rows_byte_preserved": 397, "original_source_files_byte_preserved": 87,
    "original_untracked_status_entries_present": 46,
    "new_scientific_programs_or_full_audits_run_by_reviewer": 0,
    "chronology_editorial_correction": "CLOSEOUT direct seal follows inspection of earlier INDEX repair; no frozen input or science changed",
    "review_timing": {"conservative_earliest_allocation_bound_utc": conservative_start.isoformat(),
                      "bound_source": "work-order launch known to precede allocation; not exact spawn timestamp",
                      "completion_utc": now.isoformat(), "whole_elapsed_upper_bound_minutes": wall_upper_minutes,
                      "aggregate_active_limit_minutes": 40, "whole_elapsed_bound_includes_waiting": True,
                      "exact_cpu_active_duration": "NOT separately measured",
                      "observed_overlap": "source-stage review while parent prepared integration; independent running-input check at19:41:15 while full398 ran19:37:50 onward"},
    "runtime_model_version": "UNATTESTED", "different_model_library_human_formal_interval": "UNTESTED",
    "parent_startup": "attributed; no top-level duplication", "general_capacity": "UNVERIFIED",
    "atomic_snapshot_or_signed_chronology": False,
    "protected_payloads": "NOT read/hashed", "reviewer_git_mutations": 0,
    "publication": "Subsequent mechanical manifest/staging/sync/commit/push/receipt gate; not preclaimed complete",
    "maximum_conclusion": "Complete original NCB1 equations1-14 at exact reviewed conditional scope accepted as G415 after authorized banking checks; no physical adoption, successor or canon"
}
with (BANK/"review/FINAL_FIDELITY_RECEIPT.json").open("x") as f:
    json.dump(record, f, indent=2); f.write("\n")
print(json.dumps({"verdict": record["verdict"], "frozen_input_files": 142,
                  "sealed_paths": len(paths), "elapsed_upper_bound_minutes": wall_upper_minutes,
                  "receipt_sha256": sha(BANK/"review/FINAL_FIDELITY_RECEIPT.json")}, indent=2))
