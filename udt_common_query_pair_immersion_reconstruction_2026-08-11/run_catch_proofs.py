#!/usr/bin/env python3
"""Exercise fail-closed package mutations against verify_package.py."""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parent


def run(package: Path) -> bool:
    proc = subprocess.run(
        ["python3", str(HERE / "verify_package.py"), "--repo-root", str(REPO), "--package-dir", str(package)],
        capture_output=True,
        text=True,
    )
    return proc.returncode != 0


def mutate_remove_scale(package: Path) -> None:
    path = package / "SCALE_DIAGNOSTICS.tsv"
    lines = path.read_text().splitlines()
    path.write_text("\n".join(lines[:-1]) + "\n")


def mutate_source_hash(package: Path) -> None:
    path = package / "SOURCE_MANIFEST.tsv"
    text = path.read_text()
    path.write_text(text.replace("454edcf9", "00000000", 1))


def mutate_independent_verdict(package: Path) -> None:
    path = package / "INDEPENDENT_VERIFICATION.json"
    data = json.loads(path.read_text())
    data["verdict"] = "VERIFIED"
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def mutate_codazzi_promotion(package: Path) -> None:
    path = package / "AUDIT_REPORT.md"
    path.write_text(path.read_text().replace("NUMERICALLY_UNRESOLVED", "CERTIFIED", 1))


def mutate_shared_import(package: Path) -> None:
    path = package / "verify_common_query_independent.py"
    path.write_text("from solve_common_query import metric\n" + path.read_text())


def mutate_remove_history(package: Path) -> None:
    (package / "FIRST_PRODUCTION_SCALE_DIAGNOSTICS.tsv").unlink()


def mutate_query_identity(package: Path) -> None:
    path = package / "SCALE_DIAGNOSTICS.tsv"
    path.write_text(path.read_text().replace("Q2_TL_FERMI", "Q2_RENAMED", 1))


def main() -> None:
    mutations = [
        ("missing_scale_row", mutate_remove_scale),
        ("source_hash_change", mutate_source_hash),
        ("independent_verdict_promotion", mutate_independent_verdict),
        ("codazzi_promotion", mutate_codazzi_promotion),
        ("shared_production_import", mutate_shared_import),
        ("first_return_removed", mutate_remove_history),
        ("query_identity_changed", mutate_query_identity),
    ]
    rows = []
    with tempfile.TemporaryDirectory(prefix="udt_common_query_catches_") as tmp:
        for name, mutation in mutations:
            target = Path(tmp) / name
            shutil.copytree(HERE, target)
            mutation(target)
            rejected = run(target)
            rows.append({"catch": name, "result": "PASS_REJECTED" if rejected else "FAIL_ACCEPTED"})
    output = {"schema": "UDT_COMMON_QUERY_CATCHES_V1", "counts": {"passed": sum(r["result"] == "PASS_REJECTED" for r in rows), "total": len(rows)}, "rows": rows}
    (HERE / "CATCH_PROOF_RESULTS.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps(output, indent=2, sort_keys=True))
    if output["counts"]["passed"] != output["counts"]["total"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
