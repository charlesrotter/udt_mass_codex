#!/usr/bin/env python3
"""Hostile mutation checks for the G297 package verifier."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def verifier_rejects(mutator):
    with tempfile.TemporaryDirectory(prefix="g297_catch_") as temp_name:
        package = Path(temp_name) / HERE.name
        shutil.copytree(HERE, package, ignore=shutil.ignore_patterns("__pycache__"))
        mutator(package)
        env = dict(os.environ)
        env["G297_SOURCE_ROOT"] = str(ROOT)
        completed = subprocess.run(
            [sys.executable, "-S", "verify_package.py"],
            cwd=package,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return completed.returncode != 0


def mutate_source_hash(package):
    path = package / "SOURCE_MANIFEST.tsv"
    text = path.read_text(encoding="utf-8")
    path.write_text(text.replace("b4b0d9", "04b0d9", 1), encoding="utf-8")


def mutate_production_result(package):
    path = package / "DERIVATION_RESULT.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["check_count"] = 124
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def mutate_independent_result(package):
    path = package / "INDEPENDENT_VERIFICATION.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["assertions"] = 50001
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def mutate_landing(package):
    path = package / "EXACT_DERIVATION.md"
    text = path.read_text(encoding="utf-8")
    path.write_text(
        text.replace(
            "OWNER_CLARIFICATION_IS_SUBSTANTIVE_BUT_THE_TWO_LEG_COMPLETE_TRANSFER_REMAINS_UNDERDEFINED",
            "BROKEN_LANDING",
            1,
        ),
        encoding="utf-8",
    )


def mutate_production_code(package):
    path = package / "derive_causal_dilation_equivalence.py"
    text = path.read_text(encoding="utf-8")
    path.write_text(text.replace('"check_count": len(checks)', '"check_count": len(checks) - 1', 1), encoding="utf-8")


def main():
    mutations = {
        "source_hash": mutate_source_hash,
        "production_result": mutate_production_result,
        "independent_result": mutate_independent_result,
        "landing_token": mutate_landing,
        "production_code": mutate_production_code,
    }
    caught = {name: verifier_rejects(mutator) for name, mutator in mutations.items()}
    if not all(caught.values()):
        raise AssertionError(caught)
    result = {"all_pass": True, "caught": caught, "count": len(caught)}
    (HERE / "CATCH_PROOF_RESULT.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
