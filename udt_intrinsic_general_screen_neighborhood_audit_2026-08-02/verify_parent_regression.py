#!/usr/bin/env python3
"""Prove the three parent p1 certificates reproduce the frozen parent output exactly."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OLD = ROOT / "udt_twisted_s3_all_gate_reciprocal_reduction_audit_2026-08-02/INVARIANT_CERTIFICATE.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


old = json.loads(OLD.read_text(encoding="utf-8"))
rows = []
for index, candidate_id in enumerate(("C01", "C02", "C03")):
    prior = old["candidate_results"][index]
    current_path = HERE / "invariant_points" / f"{candidate_id}_p1.json"
    current = json.loads(current_path.read_text(encoding="utf-8"))
    fields = ("invariants_at_point", "jacobian", "jacobian_determinant", "jacobian_nonzero")
    assert all(current[field] == prior[field] for field in fields)
    rows.append({
        "candidate_id": candidate_id,
        "fields_identical": list(fields),
        "current_point_sha256": digest(current_path),
    })
result = {
    "schema": "udt-general-screen-parent-regression-1.0",
    "status": "PASS_EXACT",
    "parent_candidates": 3,
    "prior_certificate_sha256": digest(OLD),
    "rows": rows,
}
(HERE / "PARENT_REGRESSION.json").write_text(
    json.dumps(result, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)
print(json.dumps({"status": result["status"], "parent_candidates": 3}, sort_keys=True))
