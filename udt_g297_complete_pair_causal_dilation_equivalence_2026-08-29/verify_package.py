#!/usr/bin/env python3
"""No-write verifier for the local G297 evidence package."""

from hashlib import sha256
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
ROOT = Path(os.environ.get("G297_SOURCE_ROOT", str(HERE.parent))).resolve()


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def run(command, cwd):
    completed = subprocess.run(
        command,
        cwd=cwd,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return completed.stdout


def main():
    source_rows = []
    for raw in (HERE / "SOURCE_MANIFEST.tsv").read_text(encoding="utf-8").splitlines()[1:]:
        expected, relative = raw.split("\t", 1)
        path = ROOT / relative
        if not path.is_file():
            raise AssertionError(f"missing source: {relative}")
        if digest(path) != expected:
            raise AssertionError(f"source hash mismatch: {relative}")
        source_rows.append(relative)

    derivation = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    required_derivation_tokens = [
        "OWNER_CLARIFICATION_IS_SUBSTANTIVE_BUT_THE_TWO_LEG_COMPLETE_TRANSFER_REMAINS_UNDERDEFINED",
        "G297 does not supply these items",
        "scalar shortcut is exactly refuted",
        "OPEN_UNDERDEFINED",
        "W1 remains an evaluator",
    ]
    for token in required_derivation_tokens:
        if token not in derivation:
            raise AssertionError(f"missing derivation token: {token}")

    prereg = (HERE / "PREREGISTRATION.md").read_text(encoding="utf-8")
    if "No outcome-dependent landing may be invented." not in prereg:
        raise AssertionError("preregistration landing freeze missing")

    expected_production = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    expected_independent = json.loads(
        (HERE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8")
    )
    if not expected_production.get("all_pass") or expected_production.get("check_count") != 125:
        raise AssertionError("saved production envelope invalid")
    if expected_production.get("load_bearing_complete_transfer_verified") is not False:
        raise AssertionError("open transfer boundary missing")
    expected_landing = (
        "OWNER_CLARIFICATION_IS_SUBSTANTIVE_BUT_THE_TWO_LEG_COMPLETE_TRANSFER_REMAINS_UNDERDEFINED"
        "__NO_UNIQUE_NONIDENTITY_FORM_YET"
    )
    if expected_production.get("landing_candidate") != expected_landing:
        raise AssertionError("saved landing does not match frozen candidate 2")
    if not expected_independent.get("all_pass") or expected_independent.get("assertions") != 50002:
        raise AssertionError("saved independent envelope invalid")

    with tempfile.TemporaryDirectory(prefix="g297_verify_") as temp_name:
        runtime = Path(temp_name)
        for name in ("derive_causal_dilation_equivalence.py", "verify_causal_dilation_independent.py"):
            shutil.copy2(HERE / name, runtime / name)
        run([sys.executable, "-S", "derive_causal_dilation_equivalence.py"], runtime)
        run([sys.executable, "-S", "verify_causal_dilation_independent.py"], runtime)
        replay_production = json.loads((runtime / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
        replay_independent = json.loads(
            (runtime / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8")
        )
        if replay_production != expected_production:
            raise AssertionError("production replay differs from saved evidence")
        if replay_independent != expected_independent:
            raise AssertionError("independent replay differs from saved evidence")

    result = {
        "all_pass": True,
        "source_count": len(source_rows),
        "production_checks": expected_production["check_count"],
        "independent_cases": expected_independent["cases"],
        "independent_assertions": expected_independent["assertions"],
        "no_write_replay": True,
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
