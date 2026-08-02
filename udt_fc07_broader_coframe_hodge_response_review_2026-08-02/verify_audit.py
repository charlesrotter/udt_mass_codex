#!/usr/bin/env python3
"""Fail-closed verification of the append-only correction layer."""

from __future__ import annotations

import ast
import csv
import hashlib
import json
import subprocess
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
PARENT = ROOT / "udt_fc07_broader_coframe_hodge_response_audit_2026-08-02"


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def table(name: str) -> list[dict[str, str]]:
    with (PACKAGE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> int:
    required = table("REQUIRED_CORRECTIONS.tsv")
    overlay = table("STATUS_OVERLAY.tsv")
    catches = table("CATCH_PROOFS.tsv")
    sources = table("SOURCE_MANIFEST.tsv")
    result = json.loads((PACKAGE / "CORRECTION_RESULT.json").read_text(encoding="utf-8"))

    assert [row["id"] for row in required] == [f"C{i:02d}" for i in range(1, 8)]
    assert len(overlay) == 12
    assert len(catches) == 15 and all(row["status"] == "PASS" for row in catches)
    assert result["outcome"] == "COLD_REVIEW_PASS_AFTER_REQUIRED_CORRECTIONS"
    assert result["checks_passed"] == result["checks_total"] == 33
    assert result["semantic_catches_passed"] == result["semantic_catches_total"] == 15
    assert result["parent_package_entries"] == 51 and result["parent_package_valid"] is True
    assert result["parent_source_blobs"] == 15 and result["parent_source_blobs_valid"] is True
    assert result["current_source_matches"] == 14
    assert result["current_source_divergences"] == ["LIVE.md"]
    assert result["law_selected"] is False and result["density_scan_authorized"] is False

    # Parent package remains exactly frozen.
    assert digest(PARENT / "PACKAGE_MANIFEST.sha256") == (
        "5f9cbe9eeae15b82e9d79d290cbc0e8d056b8d8cd7af20c2b1818070c164ae36"
    )
    parent_entries = 0
    for line in (PARENT / "PACKAGE_MANIFEST.sha256").read_text(encoding="utf-8").splitlines():
        expected, name = line.split(None, 1)
        path = PARENT / name.strip()
        assert path.is_file() and digest(path) == expected
        parent_entries += 1
    assert parent_entries == 51

    # Correction source freeze also replays immutable recorded Git blobs.
    assert len(sources) == len({row["path"] for row in sources}) == 10
    for row in sources:
        data = subprocess.check_output(["git", "cat-file", "blob", row["git_blob"]], cwd=ROOT)
        assert digest_bytes(data) == row["sha256"]
        assert len(data) == int(row["bytes"])
    recorded = (PACKAGE / "SOURCE_MANIFEST.sha256").read_text(encoding="utf-8").split()[0]
    assert digest(PACKAGE / "SOURCE_MANIFEST.tsv") == recorded

    review = (PACKAGE / "COLD_REVIEW_RETURN.md").read_text(encoding="utf-8")
    correction = (PACKAGE / "CORRECTION_LAYER.md").read_text(encoding="utf-8")
    assert "PASS_AFTER_REQUIRED_CORRECTIONS" in review
    assert "not a configuration-uniform quotient dimension" in review
    assert "not individually global one-forms" in review
    assert "outside the registered\npositive-triangular" in review
    assert "formal/free affine two-scalar coefficient class" in correction
    assert "sigma=2 phi" in correction
    assert "priority phrase" in correction
    assert "No connection or curvature" in correction

    tree = ast.parse((PACKAGE / "verify_correction.py").read_text(encoding="utf-8"))
    imports = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    from_imports = {
        node.module or ""
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
    }
    assert "sympy" not in imports
    assert not any("derive_broader_response" in name for name in from_imports)

    verification = {
        "status": "PASS",
        "outcome": result["outcome"],
        "required_corrections": len(required),
        "status_overlay_rows": len(overlay),
        "correction_checks": result["checks_total"],
        "semantic_catches": len(catches),
        "parent_package_entries": parent_entries,
        "parent_source_blobs": result["parent_source_blobs"],
        "correction_source_blobs": len(sources),
        "law_selected": False,
        "density_scan_authorized": False,
    }
    (PACKAGE / "VERIFICATION_RESULT.json").write_text(
        json.dumps(verification, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(verification, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
