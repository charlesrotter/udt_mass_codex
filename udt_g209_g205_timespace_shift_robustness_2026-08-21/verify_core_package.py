#!/usr/bin/env python3
"""Byte-stable no-write core replay for G209 before external review."""

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
        PACKAGE / "BOUNDARY_DIAGNOSTICS.json",
        PACKAGE / "CATCH_PROOF_RESULT.json",
        PACKAGE / "SOURCE_PROVENANCE_VERIFICATION.json",
    )
    before = {path.name: sha256(path) for path in result_paths}
    replay = (
        run_json("derive_timespace_shift.py"),
        run_json("verify_timespace_shift_independent.py"),
        run_json("run_boundary_diagnostics.py"),
        run_json("run_catch_proofs.py"),
    )
    after = {path.name: sha256(path) for path in result_paths}
    assert before == after
    saved = tuple(json.loads(path.read_text(encoding="utf-8")) for path in result_paths)
    assert replay == saved[:4]
    production, independent, diagnostics, catches, provenance = saved
    assert production["assertion_count"] == 21
    assert independent["status"] == "PASS"
    assert independent["distinct_exact_cases"] == 10_000
    assert independent["assertion_count"] == 100_001
    assert independent["production_imported"] is False
    assert diagnostics["status"] == "PASS" and diagnostics["precision_digits"] == 120
    assert diagnostics["profile_count"] == 4
    assert catches["status"] == "PASS" and catches["catch_count"] == 25
    assert provenance["status"] == "PASS"
    assert provenance["checked_in_live_repository_context"] == 8
    assert provenance["package_replay_dependency"] is False

    exact = " ".join((PACKAGE / "EXACT_DERIVATION.md").read_text(encoding="utf-8").split())
    report = " ".join((PACKAGE / "AUDIT_REPORT.md").read_text(encoding="utf-8").split())
    for token in (
        "FULL_LOCAL_TIMESPACE_SHIFT_IS_AN_EXACT_INDEPENDENT_METRIC_SECTOR",
        "IT_TRANSLATES_THE_CAUSAL_ELLIPSOID_WITHOUT_CHANGING_SIGNATURE_OR_AMBIENT_DETERMINANT",
        "GROWTH_CONTROLLED_AND_UNIFORMLY_SUBLUMINAL_G205_CLASSES_SURVIVE",
        "A_SMOOTH_BOUNDED_COORDINATE_SHIFT_CAN_PRESERVE_GLOBAL_HYPERBOLICITY_WHILE_DESTROYING_NULL_COMPLETENESS",
        "COMPLETED_PAIRS_HEAR_SHIFT_BEFORE_READOUT",
        "NO_PHYSICAL_SHIFT_HISTORY_OR_XMAX_SELECTION",
    ):
        assert token in exact and token in report
    for guard in (
        "does not select a shift or a physical UDT history",
        "Timelike and spacelike completeness",
        "or `X_max`",
    ):
        assert guard in exact or guard in report
    execution = " ".join((PACKAGE / "PREREGISTRATION_EXECUTION_NOTE.md").read_text(encoding="utf-8").split())
    assert "b5c40cc2" in execution
    assert "do not independently mechanize the global theorems" in execution

    result = {
        "status": "PASS",
        "provenance_manifest_rows": len(rows),
        "production_assertions": production["assertion_count"],
        "independent_assertions": independent["assertion_count"],
        "independent_cases": independent["distinct_exact_cases"],
        "diagnostic_precision_digits": diagnostics["precision_digits"],
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
