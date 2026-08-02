#!/usr/bin/env python3
"""Fail closed on package identity and decisive all-gate fields."""

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
assert digest(HERE / "derive_invariant_certificate.py") == "fbef0067b506b865e8bcb22db07534cd1146712b0d7869b30bd6c9a6915d75ea"
assert digest(HERE / "INVARIANT_CERTIFICATE.json") == "876b00e7d94e249b148846d59612b4cef373430bb1b8fb2f34a1f8ee55160d67"
review = HERE / "independent_review"
assert digest(review / "independent_torch_curvature.py") == "c182f90aaf32ab6ecb40e394f52a7e8e720206011c9d8ecfc62de99e3e7009dc"
assert digest(review / "independent_torch_curvature.stdout.json") == "e6edb2085af4553e1a3159289581152e3c66e9a7c024d47a8983f02f284c9443"
assert digest(review / "independent_torch_curvature.additional.stdout.json") == "e44394fef0695331a634f14607caac0fb3a2593e0eb762b22cdc48230cabf6de"
assert digest(review / "independent_torch_curvature.environment.txt") == "d797465a9a4177f0e1ee2b43d2c6757e6323b65d412bf47022f16d451e816b17"
result = json.loads((HERE / "ADJUDICATION_RESULT.json").read_text(encoding="utf-8"))
certificate = json.loads((HERE / "INVARIANT_CERTIFICATE.json").read_text(encoding="utf-8"))
gates = json.loads((HERE / "REPOSITORY_GATES.json").read_text(encoding="utf-8"))
assert result["status"] == "PASS_VERIFIED_FRESH_COLD_REVIEW"
assert result["eligible_exact_nonzero_candidates"] == ["C01", "C02", "C03", "C04", "C05"]
assert result["full_killing_algebra"] == "ONE_DIMENSIONAL_EXACT_BOUNDED_WITNESS"
assert result["rank2_reduction"] == "DERIVED_SMOOTH_EQUIVARIANT_ON_EXPLICIT_WITNESS"
assert result["universal_family_selection"] == result["on_shell_selection"] == "OPEN_NOT_CLAIMED"
assert result["catch_count"] == 20 and result["gate_count"] == 13
assert result["profile_selected"] is result["lambda_selected"] is result["physics_promoted"] is False
assert certificate["exact_nonzero_witness_exists"] is True
assert gates["status"] == "PASS"
verification = {
    "status": result["status"],
    "entries": len(entries),
    "package_manifest_sha256": digest(HERE / "PACKAGE_MANIFEST.sha256"),
    "source_manifest_sha256": digest(HERE / "SOURCE_MANIFEST.tsv"),
    "invariant_certificate_sha256": digest(HERE / "INVARIANT_CERTIFICATE.json"),
    "headline": result["headline"],
}
(HERE / "PACKAGE_VERIFICATION.json").write_text(json.dumps(verification, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(verification, sort_keys=True))
