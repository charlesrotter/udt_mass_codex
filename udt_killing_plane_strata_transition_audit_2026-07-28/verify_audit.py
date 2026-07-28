#!/usr/bin/env python3
"""Fail-closed replay of the bounded Killing-plane audit."""

from __future__ import annotations

import csv
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SOURCE_IDENTITY = "f68c93d740c3b5e337237bebc196810c1c537564109793507e30f53967e1ac0a"


def require(name: str, condition: bool, checks: list[str]) -> None:
    if not condition:
        raise AssertionError(name)
    checks.append(name)


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env.update({"CUDA_VISIBLE_DEVICES": "", "PYTHONDONTWRITEBYTECODE": "1"})
    return subprocess.run(
        command, cwd=ROOT, env=env, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False,
    )


def main() -> None:
    checks: list[str] = []
    replay = run([sys.executable, str(HERE / "run_and_capture.py")])
    require("run_and_capture", replay.returncode == 0, checks)

    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text(encoding="utf-8"))
    require("production_31", production["check_count"] == 31, checks)
    require("independent_209", independent["checks_passed"] == 209, checks)
    require("catch_24", independent["catch_proofs"] == 24, checks)
    require("primary_mixed", production["primary_classification"] == "MIXED_PARAMETER_STRATA", checks)
    require("registered_plane", production["method_boundary"]["registered_K_V_plane_conditional"] is True, checks)
    require("higher_isometry_open", production["topology"]["higher_isometry_plane_selection"] == "OPEN", checks)
    require("full_twist_not_zero", production["twist"]["K_full_twist_generically_zero"] is False, checks)
    require("flat_control", production["twist"]["constant_depth_kappa_zero"] == "ALL_CONSTANT_KILLING_DIRECTIONS_TWIST_FREE", checks)
    require("repository_tests", independent["repository_gates"]["tests"]["passed"] == 70 and independent["repository_gates"]["tests"]["xfailed"] == 1, checks)
    require("frozen", independent["repository_gates"]["frozen"]["entries"] == 127 and independent["repository_gates"]["frozen"]["tracked_paths"] == 133, checks)
    require("navigation", independent["repository_gates"]["navigation"]["current_paths"] == 1114 and independent["repository_gates"]["navigation"]["frontier_targets"] == 101, checks)

    manifest = list(csv.DictReader((HERE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8"), delimiter="\t"))
    identity = "\n".join(f"{r['path']}\t{r['blob']}\t{r['sha256']}\t{r['bytes']}" for r in manifest) + "\n"
    require("source_identity", len(manifest) == 20 and hashlib.sha256(identity.encode()).hexdigest() == SOURCE_IDENTITY, checks)

    catches = list(csv.DictReader((HERE / "CATCH_PROOFS.tsv").open(encoding="utf-8"), delimiter="\t"))
    require("all_catches", len(catches) == 24 and all(row["status"] == "PASS" for row in catches), checks)
    contract = list(csv.DictReader((HERE / "FALSIFICATION_CONTRACT.tsv").open(encoding="utf-8"), delimiter="\t"))
    require("contract", len(contract) == 15 and all(row["status"] == "PASS" for row in contract), checks)

    review_files = [
        "FRESH_ADVERSARIAL_REVIEW.md",
        "FRESH_ADVERSARIAL_REVIEW_CORRECTED.md",
        "FRESH_ADVERSARIAL_REVIEW_FINAL.md",
    ]
    require("review_files", all((HERE / name).is_file() for name in review_files), checks)
    verdicts = [(HERE / name).read_text(encoding="utf-8").splitlines()[0].strip("`") for name in review_files]
    require("review_verdicts", verdicts == ["PASS_WITH_REQUIRED_CORRECTIONS"] * 3, checks)
    require(
        "final_self_output_path_closed",
        "Preserve this review under that name" in (HERE / review_files[-1]).read_text(encoding="utf-8")
        and (HERE / review_files[-1]).exists(),
        checks,
    )

    result = {
        "schema": "udt-killing-plane-strata-transition-verification-1.0",
        "status": "PASS",
        "checks_passed": len(checks),
        "production_checks": production["check_count"],
        "independent_checks": independent["checks_passed"],
        "catch_proofs": independent["catch_proofs"],
        "fresh_reviews": verdicts,
        "final_review_resolution": "SOLE_MISSING_SELF_OUTPUT_PATH_EXISTS_AND_NAVIGATION_REPLAY_PASSES",
        "source_identity_sha256": SOURCE_IDENTITY,
        "maximum_conclusion": production["maximum_conclusion"],
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
