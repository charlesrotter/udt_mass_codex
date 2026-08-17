#!/usr/bin/env python3
"""Verify G128 sources and replay production and independent implementations."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def main():
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    checks = {"source_count_five": len(rows) == 5}
    for row in rows:
        source = ROOT / row["path"]
        checks[f"source::{row['path']}"] = source.is_file() and digest(source) == row["sha256"]

    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text())
    checks["production_29_of_29"] = (
        production.get("status") == "PASS"
        and production.get("landing") == "FINITE_PATH_SAME_HISTORY_EMERGENCE_OBSERVED"
        and len(production.get("checks", {})) == 29
        and all(production.get("checks", {}).values())
    )
    checks["independent_7_of_7"] = (
        independent.get("status") == "PASS"
        and len(independent.get("checks", {})) == 7
        and all(independent.get("checks", {}).values())
    )

    with tempfile.TemporaryDirectory(prefix="udt_g128_replay_") as temp_name:
        temp = Path(temp_name)
        for name in ("derive_finite_path.py", "verify_finite_path_independent.py"):
            shutil.copy2(HERE / name, temp / name)

        prod_run = subprocess.run(
            [sys.executable, str(temp / "derive_finite_path.py")],
            cwd=temp,
            text=True,
            capture_output=True,
            check=False,
        )
        checks["fresh_production_exit"] = prod_run.returncode == 0
        if prod_run.returncode == 0:
            checks["fresh_production_json_identical"] = (
                (temp / "DERIVATION_RESULT.json").read_bytes()
                == (HERE / "DERIVATION_RESULT.json").read_bytes()
            )
            checks["fresh_atlas_tsv_identical"] = (
                (temp / "FINITE_PATH_ATLAS.tsv").read_bytes()
                == (HERE / "FINITE_PATH_ATLAS.tsv").read_bytes()
            )
            fresh_npz = np.load(temp / "FINITE_PATH_SAMPLES.npz")
            banked_npz = np.load(HERE / "FINITE_PATH_SAMPLES.npz")
            checks["fresh_sample_keys_identical"] = set(fresh_npz.files) == set(banked_npz.files)
            checks["fresh_sample_arrays_identical"] = checks["fresh_sample_keys_identical"] and all(
                np.array_equal(fresh_npz[key], banked_npz[key], equal_nan=True)
                for key in fresh_npz.files
            )
        else:
            checks.update(
                {
                    "fresh_production_json_identical": False,
                    "fresh_atlas_tsv_identical": False,
                    "fresh_sample_keys_identical": False,
                    "fresh_sample_arrays_identical": False,
                }
            )

        independent_run = subprocess.run(
            [sys.executable, str(temp / "verify_finite_path_independent.py")],
            cwd=temp,
            text=True,
            capture_output=True,
            check=False,
        )
        checks["fresh_independent_exit"] = independent_run.returncode == 0
        checks["fresh_independent_json_identical"] = (
            independent_run.returncode == 0
            and (temp / "INDEPENDENT_VERIFICATION.json").read_bytes()
            == (HERE / "INDEPENDENT_VERIFICATION.json").read_bytes()
        )

    for name in (
        "PREREGISTRATION.md",
        "PREMISE_LEDGER.tsv",
        "EXACT_DERIVATION.md",
        "LAY_REPORT.md",
        "EVIDENCE_GATES.md",
        "REVIEW_REQUEST.md",
        "AUDIT_REPORT.md",
        "STATUS.md",
    ):
        checks[f"present::{name}"] = (HERE / name).is_file()

    result = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "verification_kind": "source_manifest_plus_fresh_isolated_production_and_independent_replay",
        "source_count": len(rows),
        "checks": checks,
    }
    (HERE / "PACKAGE_VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
