#!/usr/bin/env python3
"""Verify both G334 sealed products and no-bytecode in-place replay."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot(root):
    return {
        path.relative_to(root).as_posix(): digest(path)
        for path in root.rglob("*")
        if path.is_file()
    }


def run(command, cwd):
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="REPAIR_VERIFICATION_RESULT.json")
    args = parser.parse_args()
    checks = []

    def require(condition, name):
        if not condition:
            raise AssertionError(name)
        checks.append(name)

    def exercise(builder, expected_count, label):
        built = run(["python3", "-B", "-S", str(ROOT / builder)], ROOT)
        require(built.returncode == 0, f"{label}_builder_pass")
        metadata = json.loads(built.stdout)
        intake = Path(metadata["intake"])
        before = snapshot(intake)
        require(metadata["file_count"] == expected_count, f"{label}_declared_count_exact")
        require(len(before) == expected_count, f"{label}_actual_count_exact")
        require(not any("__pycache__" in path or path.endswith(".pyc") for path in before),
                f"{label}_has_no_bytecode")

        intake_check = run(
            ["python3", "-B", "-S", str(intake / "package" / "verify_review_intake.py"),
             str(intake)], intake
        )
        require(intake_check.returncode == 0, f"{label}_intake_verifier_pass")

        package_check = run(
            ["python3", "-B", "-S", str(intake / "package" / "verify_package.py")], intake
        )
        require(package_check.returncode == 0, f"{label}_package_replay_pass")
        require("103 aggregate gates" in package_check.stdout,
                f"{label}_scientific_103_retained")
        after = snapshot(intake)
        require(after == before, f"{label}_replay_byte_exact_and_no_extra")

        with tempfile.TemporaryDirectory(prefix=f"g334_{label}_hostile_extra_") as temporary:
            hostile = Path(temporary) / "intake"
            shutil.copytree(intake, hostile)
            (hostile / "UNMANIFESTED_SENTINEL.txt").write_text(
                "hostile extra file\n", encoding="utf-8"
            )
            hostile_check = run(
                ["python3", "-B", "-S",
                 str(hostile / "package" / "verify_review_intake.py"), str(hostile)], hostile
            )
            require(hostile_check.returncode != 0, f"{label}_hostile_extra_rejected")
            require("sealed file-set mismatch" in (hostile_check.stderr + hostile_check.stdout),
                    f"{label}_hostile_extra_rejection_reason")

    exercise("build_review_intake.py", 43, "fresh_review")
    exercise("build_repair_followup_intake.py", 46, "repair_followup")

    payload = {
        "package": "G334",
        "verdict": "PASS",
        "landing": (
            "G334_SEALED_FILE_SET_AND_NO_BYTECODE_REPLAY_REPAIRED"
            "__SCIENTIFIC_LANDING_UNCHANGED"
        ),
        "r3_landing": (
            "G334_FRESH_AND_REPAIR_FOLLOWUP_SEALED_PRODUCTS_EXPLICITLY_SEPARATED"
            "__R1_R2_BEHAVIOR_RETAINED__SCIENTIFIC_LANDING_UNCHANGED"
        ),
        "checks_passed": len(checks),
        "checks": checks,
        "fresh_review_file_count": 43,
        "repair_followup_file_count": 46,
        "result_is_digest_independent": True,
        "scientific_landing_changed": False,
    }
    Path(args.output).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"checks_passed": len(checks), "verdict": "PASS"}, sort_keys=True))


if __name__ == "__main__":
    main()
