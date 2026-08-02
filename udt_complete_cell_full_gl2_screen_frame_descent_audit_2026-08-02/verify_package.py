#!/usr/bin/env python3
"""Fail closed on the final package identity and decisive fields."""

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
result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text(encoding="utf-8"))
semantic = json.loads((HERE / "VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
gates = json.loads((HERE / "REPOSITORY_GATES.json").read_text(encoding="utf-8"))
assert result["headline"] == "SPLIT_RELATIVE_ONLY__NO_COMPLETE_FRAME_DESCENT"
assert result["curvature_rows"] == 36 and result["nonzero_lower_curvature_blocks"] == 6
assert result["independent_closure_equations"] == 5
assert result["contact_reduction"]["complete_frame_descent"] is False
assert independent["curvature_rows_matched"] == 36
assert independent["scalar_curvature_matched_by_ricci_contraction"] is True
assert semantic["catch_proofs"] == 14
assert gates["status"] == "PASS"
verification = {
    "status": "PASS_VERIFIED_WITH_CAVEATS_NO_FRESH_BLIND_REVIEW",
    "entries": len(entries),
    "package_manifest_sha256": digest(HERE / "PACKAGE_MANIFEST.sha256"),
    "source_manifest_sha256": digest(HERE / "SOURCE_MANIFEST.tsv"),
    "headline": result["headline"],
}
(HERE / "PACKAGE_VERIFICATION.json").write_text(
    json.dumps(verification, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
print(json.dumps(verification, sort_keys=True))
