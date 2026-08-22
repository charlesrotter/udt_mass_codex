#!/usr/bin/env python3
"""Byte-stable no-write core replay for G211 before external review."""

from __future__ import annotations

import csv
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


PACKAGE = Path(__file__).resolve().parent
OUT = PACKAGE / "CORE_VERIFICATION_RESULT.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def run_json(script: str) -> dict:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["UDT_NO_WRITE"] = "1"
    completed = subprocess.run(
        [sys.executable, str(PACKAGE / script)],
        cwd=PACKAGE,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def main() -> None:
    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    assert len(rows) == 8
    for row in rows:
        assert len(row["sha256"]) == 64
        int(row["sha256"], 16)
        assert row["path"] and not Path(row["path"]).is_absolute()

    result_paths = (
        PACKAGE / "PRODUCTION_RESULT.json",
        PACKAGE / "INDEPENDENT_VERIFICATION.json",
        PACKAGE / "RADIAL_CONTROLS.json",
        PACKAGE / "CATCH_PROOF_RESULT.json",
        PACKAGE / "SOURCE_PROVENANCE_VERIFICATION.json",
    )
    before = {path.name: sha256(path) for path in result_paths}
    replay = (
        run_json("derive_diagonal_scalar_basis.py"),
        run_json("verify_diagonal_scalar_independent.py"),
        run_json("run_radial_controls.py"),
        run_json("run_catch_proofs.py"),
        run_json("verify_source_manifest_repository.py"),
    )
    after = {path.name: sha256(path) for path in result_paths}
    assert before == after
    saved = tuple(json.loads(path.read_text(encoding="utf-8")) for path in result_paths)
    assert replay == saved
    production, independent, controls, catches, provenance = saved
    assert production["assertion_count"] == 29
    assert independent["status"] == "PASS"
    assert independent["distinct_exact_cases"] == 10_000
    assert independent["assertion_count"] == 280_003
    assert independent["production_imported"] is False
    assert controls["status"] == "PASS" and controls["precision_digits"] == 120
    assert controls["profile_count"] == 4
    assert catches["status"] == "PASS" and catches["catch_count"] == 31
    assert provenance["status"] == "PASS"
    assert provenance["checked_in_live_repository_context"] == 8
    assert provenance["package_replay_dependency"] is False

    exact = " ".join((PACKAGE / "EXACT_DERIVATION.md").read_text(encoding="utf-8").split())
    report = " ".join((PACKAGE / "AUDIT_REPORT.md").read_text(encoding="utf-8").split())
    for token in (
        "COMPLETE_LOCAL_DIAGONAL_SCALAR_SECTOR_HAS_RANK_TWO_AFTER_SUPPLIED_1PLUS3_REFERENCE",
        "COMMON_SCALE_AND_RELATIVE_SPATIAL_VOLUME_FORM_AN_EXACT_BASIS",
        "LAPSE_ONLY_IS_NOT_A_THIRD_TILE",
        "CAUSAL_CONES_DEPEND_ONLY_ON_RELATIVE_MODE_WHILE_NULL_AFFINE_AND_COMPLETED_DEPTH_HEAR_COMMON_SCALE",
        "NO_PHYSICAL_SCALAR_HISTORY_OR_XMAX_SELECTION",
    ):
        assert token in exact and token in report
    execution = " ".join(
        (PACKAGE / "PREREGISTRATION_EXECUTION_NOTE.md").read_text(encoding="utf-8").split()
    )
    assert "7220e71f" in execution
    assert "passed all 31 registered catches" in execution
    assert "do not independently mechanize the analytic global causal-transfer" in execution

    result = {
        "status": "PASS",
        "provenance_manifest_rows": len(rows),
        "production_assertions": production["assertion_count"],
        "independent_assertions": independent["assertion_count"],
        "independent_cases": independent["distinct_exact_cases"],
        "radial_precision_digits": controls["precision_digits"],
        "radial_profiles": controls["profile_count"],
        "mutation_catches": catches["catch_count"],
        "no_write_replay": True,
        "external_review": "PENDING_SEPARATE_GATE",
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if os.environ.get("UDT_NO_WRITE") != "1":
        OUT.write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
