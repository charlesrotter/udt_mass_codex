#!/usr/bin/env python3
"""Fail closed on package identity and decisive authority fields."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


entries = []
for line in (HERE / "PACKAGE_MANIFEST.sha256").read_text(encoding="utf-8").splitlines():
    expected, name = line.split(None, 1)
    target = HERE / name.strip()
    assert target.is_file() and digest(target) == expected
    entries.append(name.strip())
assert len(entries) == len(set(entries))
result = json.loads((HERE / "ADJUDICATION_RESULT.json").read_text(encoding="utf-8"))
gates = json.loads((HERE / "REPOSITORY_GATES.json").read_text(encoding="utf-8"))
assert result["status"] == "PASS_VERIFIED_FRESH_COLD_REVIEW"
assert result["abstract_pair"] == "DERIVED"
assert result["local_alignment"] == "DERIVED_CONDITIONAL_ON_RECORDED_READOUT"
assert result["branch_reductions"] == "DERIVED_BOUNDED_EXISTENCE"
assert result["universal_reduction"] == "OPEN"
assert result["q_squared"] == "DERIVED_GIVEN_REGISTERED_REDUCTION"
assert result["q_squared_metric_only"] == "NOT_DERIVED"
assert result["catch_proofs"] == 8 and result["fresh_zero_context_review"] is True
assert gates["status"] == "PASS"
verification = {
    "status": result["status"],
    "entries": len(entries),
    "package_manifest_sha256": digest(HERE / "PACKAGE_MANIFEST.sha256"),
    "source_manifest_sha256": digest(HERE / "SOURCE_MANIFEST.tsv"),
    "headline": result["headline"],
}
(HERE / "PACKAGE_VERIFICATION.json").write_text(
    json.dumps(verification, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
print(json.dumps(verification, sort_keys=True))
