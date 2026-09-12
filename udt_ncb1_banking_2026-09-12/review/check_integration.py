#!/usr/bin/env python3
"""Independent byte-boundary attacks; input mutations are in-memory only."""
from pathlib import Path
import ast
import csv
import datetime
import hashlib
import io
import json
import subprocess
import sys
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import ncb1_banking_guard as new
import ti1_banking_guard as ti1
import ti2_banking_guard as ti2
import verify_current_scientific_premises as old

BASE = "fd6a28e6c9ee72b1d6e19e0c2e8d03c645e9a8e1"
BANK = ROOT / "udt_ncb1_banking_2026-09-12"
REG = ROOT / "CURRENT_SCIENTIFIC_PREMISES.tsv"
raw = REG.read_bytes()
baseline = subprocess.check_output(["git", "show", f"{BASE}:CURRENT_SCIENTIFIC_PREMISES.tsv"], cwd=ROOT)
lines = raw.splitlines(keepends=True)
selected = [line for line in lines if line.split(b"\t", 1)[0] == b"G415"]
assert len(selected) == 1
row = selected[0]
assert b"".join(line for line in lines if line is not row) == baseline
assert lines[1] == row and len(lines) == 399
freeze = json.loads((BANK / "ACCEPTANCE_FREEZE.json").read_text())
for name, expected in freeze.items():
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == expected
parsed = list(csv.DictReader(raw.decode().splitlines(), delimiter="\t"))
claim = json.loads((BANK / "BANKED_CLAIM.json").read_text())
assert parsed[0] == claim["claim"]
assert set(claim["required_registry_ids"]) == {"G394", "G220", "G348", "G312"}
assert claim["controls_and_source_credit"] == ["G342"]

open_original = Path.open
events = []

def exercise(label, fn, payloads, *, target=REG, fail=None, reads=1):
    observed = []
    def opened(path, mode="r", *args, **kwargs):
        if path == target:
            n = len(observed)
            observed.append(str(path))
            data = payloads[min(n, len(payloads)-1)]
            return io.BytesIO(data) if "b" in mode else io.StringIO(data.decode(kwargs.get("encoding") or "utf-8"))
        return open_original(path, mode, *args, **kwargs)
    error = None
    with patch.object(Path, "open", opened):
        try:
            fn()
        except SystemExit as exc:
            error = str(exc)
    assert len(observed) == reads, (label, observed)
    assert (error is None) if fail is None else (error is not None and fail in error), (label, error)
    events.append({"case": label, "reads": len(observed), "rejection": error})

historical_names = [
    "validate_conditional_banking", "validate_shared_constraint_banking",
    "validate_persistence_banking", "validate_restrictiveness_banking",
    "validate_source_metric_banking", "validate_reconstruction_banking",
    "validate_coupled_banking", "validate_vacuum_scale_banking",
    "validate_berger_banking", "validate_closed_fibre_banking",
    "validate_neighboring_tidal_banking", "validate_reviewed_backlog_banking",
    "validate_ti1_banking", "validate_ti2_banking",
]
calls = {name: lambda name=name: getattr(old, name)(ROOT, authenticate_sources=False) for name in historical_names}
calls["validate_ncb1_banking"] = lambda: new.validate_ncb1_banking(ROOT, authenticate_sources=False)
calls["historical_banking_snapshot"] = lambda: old.historical_banking_snapshot(ROOT)
calls["registry_bytes_for_historical_banking"] = lambda: old.registry_bytes_for_historical_banking(ROOT)
badrow = row.replace(b"NOT_PHYSICAL_ADOPTION", b"PHYSICAL_ADOPTION")
poison = raw.replace(row, badrow)
duplicate = raw.replace(row, row + row)
for name, fn in calls.items():
    exercise(name + ": valid then poison", fn, [raw, poison])
    exercise(name + ": poison then valid", fn, [poison, raw], fail="NCB1 exact row/scope changed")
    exercise(name + ": duplicate then valid", fn, [duplicate, raw], fail="NCB1 current row missing/duplicate")
    exercise(name + ": historical absence", fn, [baseline],
             fail="NCB1 current row missing/duplicate" if name == "validate_ncb1_banking" else None)

for field in range(9):
    fields = row.rstrip(b"\n").split(b"\t")
    fields[field] += b" CORRUPTED"
    altered = raw.replace(row, b"\t".join(fields) + b"\n")
    exercise(f"new row field {field}", calls["validate_ncb1_banking"], [altered], fail="NCB1")
old_poison = raw.replace(b"G394\t", b"G394_POISON\t", 1)
exercise("unrelated original row remains rejected", calls["validate_ncb1_banking"], [old_poison],
         fail="NCB1 changed an original397 registry byte")
assert b"G394_POISON\t" in new.without_ncb1(old_poison)

new.validate_ncb1_banking(ROOT)
source_entries = [line.split("  ", 1) for line in (BANK/"SOURCE_EVIDENCE_SHA256SUMS").read_text().splitlines()]
for _, name in source_entries:
    target = ROOT/name
    exercise("source poison:" + name, lambda: new.validate_ncb1_banking(ROOT),
             [target.read_bytes() + b"\nSOURCE_CORRUPTION\n"], target=target,
             fail="NCB1 original source evidence changed")
for name in new.NCB1_GUARD_FILES:
    target = ROOT/name
    exercise("acceptance poison:" + name, lambda: new.validate_ncb1_banking(ROOT),
             [target.read_bytes() + b"\nUNCONDITIONAL\n"], target=target, fail="NCB1 guard file changed")
authority = ROOT/claim["authority_source"]
exercise("authority poison", lambda: new.validate_ncb1_banking(ROOT),
         [authority.read_bytes() + b"\nSTRONGER_GR_INPUT\n"], target=authority,
         fail="NCB1 authority source changed")

# Catch proof: remove only authentication while preserving the projection.
# The same hostile input must then create a false pass in a historical guard.
def unsafe_projection(data, *, required=False):
    return b"".join(line for line in data.splitlines(keepends=True) if not line.startswith(b"G415\t"))
catch_proofs = []
for module, fn in [(old, calls["validate_conditional_banking"]),
                   (ti1, calls["validate_ti1_banking"]),
                   (ti2, calls["validate_ti2_banking"])]:
    with patch.object(module, "without_ncb1", unsafe_projection):
        try:
            exercise("disabled auth catches:" + module.__name__, fn, [poison],
                     fail="NCB1 exact row/scope changed")
        except AssertionError:
            catch_proofs.append(module.__name__)
        else:
            raise AssertionError("The hostile probe failed to turn red under removed authentication")
assert len(catch_proofs) == 3

# Existing guards/tests are compared at AST level as well as visually diffed.
# The only permitted inherited assert changes are mechanical current counts.
assert_preservation = {}
for name in ["ti1_banking_guard.py", "ti2_banking_guard.py", "tests/test_ti1_banking.py", "tests/test_ti2_banking.py"]:
    previous = subprocess.check_output(["git", "show", f"{BASE}:{name}"], cwd=ROOT).decode()
    current = (ROOT/name).read_text()
    def assertions(source):
        return [ast.dump(n, include_attributes=False) for n in ast.walk(ast.parse(source))
                if isinstance(n, ast.Assert) or (isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "require")]
    assert assertions(previous) == assertions(current), name
    assert_preservation[name] = len(assertions(current))

print(json.dumps({
    "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "verdict": "PASS_BYTE_AUTHENTICATION_AND_HOSTILE_BOUNDARIES",
    "original397_byte_identity": True,
    "acceptance_freeze_authenticated": freeze,
    "guards_and_helpers": len(calls),
    "hostile_and_preserving_cases": events,
    "removed_authentication_catchproof_red_modules": catch_proofs,
    "inherited_assertions_exactly_preserved": assert_preservation,
    "source_files_each_actually_poisoned": len(source_entries),
    "mutation_method": "Path.open in-memory streams cover read_bytes/read_text/read_tsv without source writes",
    "science_reruns": 0, "guard_route": "independent input-harness, shared guarded implementations"
}, indent=2))
