#!/usr/bin/env python3
"""Verify G128 sources and replay production and independent implementations."""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import math
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


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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

    production_module = load_module(HERE / "derive_finite_path.py", "g128_production_guards")
    independent_module = load_module(
        HERE / "verify_finite_path_independent.py", "g128_independent_guards"
    )
    production_events = production_module.boundary_events()
    independent_events = independent_module.boundary_events()
    radius_state = np.zeros(24)
    radius_state[1] = 0.08
    radius_state[2] = math.pi / 2
    pole_state = radius_state.copy()
    pole_state[1] = 0.4
    pole_state[2] = math.asin(0.2)
    checks["production_runtime_boundary_events"] = (
        len(production_events) == 2
        and all(event.terminal for event in production_events)
        and abs(production_events[0](0.0, radius_state)) < 1e-15
        and abs(production_events[1](0.0, pole_state)) < 1e-15
    )
    checks["independent_runtime_boundary_events"] = (
        len(independent_events) == 2
        and all(event.terminal for event in independent_events)
        and abs(independent_events[0](0.0, radius_state)) < 1e-15
        and abs(independent_events[1](0.0, pole_state)) < 1e-15
    )
    fake_geo = type(
        "FakeGeometry",
        (),
        {"histories": {"safe": {"fn": lambda _t, _r: np.zeros(18)}}},
    )()
    production_module.validate_metric_state(fake_geo, "safe", radius_state)
    independent_module.validate_metric_state("H0_flat", radius_state[:8])
    rejected = []
    for validator, args in (
        (production_module.validate_metric_state, (fake_geo, "safe", np.full(24, np.nan))),
        (independent_module.validate_metric_state, ("H0_flat", np.full(8, np.nan))),
    ):
        try:
            validator(*args)
        except FloatingPointError:
            rejected.append(True)
        else:
            rejected.append(False)
    checks["runtime_nonfinite_rejection"] = all(rejected)

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
        "EXTERNAL_REVIEW_RAW.md",
        "EXTERNAL_REVIEW_ADJUDICATION.md",
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
