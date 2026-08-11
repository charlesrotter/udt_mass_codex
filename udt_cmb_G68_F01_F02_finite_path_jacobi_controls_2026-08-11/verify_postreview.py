#!/usr/bin/env python3
"""Verify G68 reviewed history, immutable payload, and final adjudication state."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path

from verify_package import verify_files


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REVIEWED_COMMIT = "0ea2200e"
ALLOWED_POSTREVIEW_CHANGES = {
    f"{HERE.name}/AUDIT_REPORT.md",
    f"{HERE.name}/CATCH_PROOF_RESULTS.json",
    f"{HERE.name}/CATCH_PROOF_STDOUT.txt",
    f"{HERE.name}/EXACT_DERIVATION.md",
    f"{HERE.name}/run_catch_proofs.py",
    f"{HERE.name}/verify_package.py",
}


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def committed_bytes(path: str) -> bytes:
    result = subprocess.run(
        ["git", "show", f"{REVIEWED_COMMIT}:{path}"],
        cwd=ROOT,
        capture_output=True,
        check=True,
    )
    return result.stdout


def main() -> None:
    review_rows = tsv(HERE / "REVIEW_MANIFEST.tsv")
    assert len(review_rows) == 37
    historical_mismatches = []
    current_immutable_mismatches = []
    for row in review_rows:
        if digest_bytes(committed_bytes(row["path"])) != row["sha256"]:
            historical_mismatches.append(row["path"])
        if row["path"] not in ALLOWED_POSTREVIEW_CHANGES and digest(ROOT / row["path"]) != row["sha256"]:
            current_immutable_mismatches.append(row["path"])
    assert not historical_mismatches, historical_mismatches
    assert not current_immutable_mismatches, current_immutable_mismatches

    assert digest(HERE / "REVIEW_MANIFEST.tsv") == "38f8bd1bda0289de91bd74243b28a88e70ac4aa370b0c715367ee671b051bc3d"
    assert digest(HERE / "EXTERNAL_REVIEW_RAW.md") == "450065fed7324aecf6aa4764f97037944876271d5d7f74b708c7b6cbc968eb20"
    assert "VERIFIED_WITH_CAVEATS" in (HERE / "EXTERNAL_REVIEW_RAW.md").read_text(encoding="utf-8")
    assert "VERIFIED_WITH_CAVEATS" in (HERE / "EXTERNAL_REVIEW_ADJUDICATION.md").read_text(encoding="utf-8")

    package = verify_files()
    assert package["passed"] == package["total"] == 18
    catches = json.loads((HERE / "CATCH_PROOF_RESULTS.json").read_text(encoding="utf-8"))
    assert catches["passed"] == catches["total"] == 21

    postreview_rows = tsv(HERE / "POSTREVIEW_MANIFEST.tsv")
    assert len(postreview_rows) == len({row["path"] for row in postreview_rows})
    mismatches = [row["path"] for row in postreview_rows if digest(HERE / row["path"]) != row["sha256"]]
    assert not mismatches, mismatches

    result = {
        "schema": "udt-cmb-g68-postreview-v1",
        "status": "PASS",
        "review_manifest_rows": len(review_rows),
        "review_manifest_sha256": digest(HERE / "REVIEW_MANIFEST.tsv"),
        "raw_review_sha256": digest(HERE / "EXTERNAL_REVIEW_RAW.md"),
        "historical_reviewed_mismatches": historical_mismatches,
        "current_immutable_mismatches": current_immutable_mismatches,
        "allowed_postreview_changes": sorted(ALLOWED_POSTREVIEW_CHANGES),
        "package_checks": package["passed"],
        "catch_proofs": catches["passed"],
        "postreview_manifest_rows": len(postreview_rows),
    }
    (HERE / "POSTREVIEW_VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
