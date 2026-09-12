#!/usr/bin/env python3
"""Authenticate the running audit's declared inputs and exact guard-pin-only edit."""
from pathlib import Path
import ast
import datetime
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parents[2]
BANK = ROOT/"udt_ncb1_banking_2026-09-12"
BASE = "fd6a28e6c9ee72b1d6e19e0c2e8d03c645e9a8e1"
def sha(raw):
    return hashlib.sha256(raw).hexdigest()

freeze_raw = (BANK/"AUDIT_INPUT_FREEZE.json").read_bytes()
freeze = json.loads(freeze_raw)
assert freeze["head"] == BASE
assert freeze["command"] == ["python3", "verify_current_scientific_premises.py"]
assert len(freeze["sha256"]) == 142
for name, expected in freeze["sha256"].items():
    assert sha((ROOT/name).read_bytes()) == expected, name
direct = json.loads((BANK/"review/REVIEW_RECEIPT.json").read_text())
guard = (ROOT/"ncb1_banking_guard.py").read_text()
node = next(n for n in ast.parse(guard).body if isinstance(n, ast.Assign)
            and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "NCB1_PINS")
pins = ast.literal_eval(node.value)
new_names = [str((BANK/"review"/name).relative_to(ROOT)) for name in ["REVIEW.md", "REVIEW_RECEIPT.json"]]
assert len(pins) == 7 and all(pins[name] == sha((ROOT/name).read_bytes()) for name in new_names)
for name in new_names:
    token = ", " + repr(name) + ": " + repr(pins[name])
    assert guard.count(token) == 1
    guard = guard.replace(token, "", 1)
assert sha(guard.encode()) == direct["reviewed_sha256"]["ncb1_banking_guard.py"]
# AST equality follows from reconstructing exact prior bytes, plus a direct
# semantic check that the only changed node is the two-entry pin mapping.
reconstructed = ast.parse(guard)
current = ast.parse((ROOT/"ncb1_banking_guard.py").read_text())
current_pin_node = next(n for n in current.body if isinstance(n, ast.Assign)
                       and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "NCB1_PINS")
prior_pin_node = next(n for n in reconstructed.body if isinstance(n, ast.Assign)
                     and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "NCB1_PINS")
current_pin_node.value = prior_pin_node.value
assert ast.dump(current, include_attributes=False) == ast.dump(reconstructed, include_attributes=False)
for name, expected in direct["reviewed_sha256"].items():
    if name != "ncb1_banking_guard.py":
        assert sha((ROOT/name).read_bytes()) == expected, name
receipt = json.loads((BANK/"checks/final_integration.json").read_text())
assert receipt["returncode"] == 0 and receipt["timeout"] is False
assert (BANK/"checks/final_integration.stderr").read_bytes() == b""
assert b"649 passed, 1 deselected" in (BANK/"checks/final_integration.stdout").read_bytes()
head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT).decode().strip()
assert head == BASE
print(json.dumps({
    "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "head": head, "verdict": "PASS_DECLARED_INPUT_CORRESPONDENCE",
    "declared_audit_inputs": len(freeze["sha256"]), "freeze_sha256": sha(freeze_raw),
    "guard_change": "exactly two review pins; prior bytes reconstructed to direct-reviewed SHA256; remaining AST identical",
    "guard_sha256": sha((ROOT/"ncb1_banking_guard.py").read_bytes()),
    "added_review_pins": {name: pins[name] for name in new_names},
    "direct_review_snapshot_preserved_except_declared_pin_edit": True,
    "final_integration_receipt": receipt,
    "full398_result": "NOT assessed by this input-only check",
    "atomic_snapshot_or_chronology_attestation": False
}, indent=2))
