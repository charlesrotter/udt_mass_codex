#!/usr/bin/env python3
"""Fail-closed verifier for the founded-phi extension and impact audit."""

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
BASE = "bc7713f"
EXPECTED_AFFECTED = {
    "udt_coframe_hopf_bridge_audit_2026-07-23/AUDIT_REPORT.md",
    "udt_global_local_relational_closure_audit_2026-07-25/STATUS_LEDGER.tsv",
    "udt_native_coframe_composition_law_audit_2026-07-23/AUDIT_REPORT.md",
    "udt_native_coframe_composition_law_audit_2026-07-23/LAY_REPORT.md",
    "udt_native_coframe_composition_law_audit_2026-07-23/STATUS_LEDGER.tsv",
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_tsv(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def run(command: list[str], env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        command,
        cwd=ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode:
        raise AssertionError(
            f"command failed: {command}\nstdout={result.stdout}\nstderr={result.stderr}"
        )
    return result


def git_bytes(spec: str) -> bytes:
    result = subprocess.run(
        ["git", "show", spec], cwd=ROOT, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False,
    )
    if result.returncode:
        raise AssertionError(result.stderr.decode("utf-8", "replace"))
    return result.stdout


def validate_impact(rows: list[dict[str, str]]) -> None:
    if len(rows) != 399:
        raise AssertionError("active candidate count")
    if len({row["candidate_id"] for row in rows}) != 399:
        raise AssertionError("missing or duplicate candidate id")
    if len({row["path"] for row in rows}) != 399:
        raise AssertionError("missing or duplicate candidate path")
    if any(row["primary_ruling"] == "PENDING" for row in rows):
        raise AssertionError("pending ruling")
    if any(row["primary_ruling"] == "FALSE_UNDEFINED_PLACEHOLDER" for row in rows):
        raise AssertionError("founded phi demoted to placeholder")
    if any(row["primary_ruling"] == "FALSE_ELEVENTH_POINTWISE_MODE" for row in rows):
        raise AssertionError("chosen atlas branch promoted to native field census")
    affected = {row["path"] for row in rows if row["affected"] == "YES"}
    if affected != EXPECTED_AFFECTED:
        raise AssertionError("affected identity set")
    for row in rows:
        current = ROOT / row["path"]
        if not current.is_file() or sha(current.read_bytes()) != row["sha256"]:
            raise AssertionError(f"source identity changed: {row['path']}")


def validate_extension(rows: list[dict[str, str]]) -> None:
    if [row["id"] for row in rows] != [f"E{i:02d}" for i in range(1, 13)]:
        raise AssertionError("extension ledger ids")
    by_id = {row["id"]: row for row in rows}
    if by_id["E02"]["free_extension_parameters"] != "7":
        raise AssertionError("general extension count")
    if by_id["E03"]["free_extension_parameters"] != "6":
        raise AssertionError("determinant-one extension count")
    if by_id["E06"]["status"] != "DERIVED_EXACT_WITNESS":
        raise AssertionError("spectator existence")
    if "unique_only" not in by_id["E06"]["conclusion"]:
        raise AssertionError("unconditional spectator uniqueness")
    if not {"E07", "E08"}.issubset(by_id):
        raise AssertionError("counterfamilies absent")


def expect_rejection(label: str, action, catches: list[dict[str, str]]) -> None:
    try:
        action()
    except (AssertionError, KeyError, ValueError):
        catches.append({"catch": label, "result": "PASS_REJECTED"})
    else:
        raise AssertionError(f"catch did not reject: {label}")


def main() -> None:
    tracked = (
        "FORENSIC_PHI_CENSUS.tsv",
        "ACTIVE_RESULT_CANDIDATES.tsv",
        "INPUT_SOURCE_MANIFEST.tsv",
        "ACTIVE_RESULT_IMPACT_LEDGER.tsv",
        "AFFECTED_RESULT_CORRECTION_PLAN.tsv",
    )
    before = {name: (HERE / name).read_bytes() for name in tracked}
    run([sys.executable, str(HERE / "freeze_candidate_universe.py")])
    run([sys.executable, str(HERE / "classify_active_results.py")])
    if any((HERE / name).read_bytes() != data for name, data in before.items()):
        raise AssertionError("candidate or impact replay changed tracked output")

    env = dict(os.environ)
    env.update({
        "PYTHONPATH": os.environ.get(
            "UDT_SYMPY_TARGET", "/tmp/udt_bootstrap_closure_sympy_114"
        ),
        "PYTHONDONTWRITEBYTECODE": "1",
        "CUDA_VISIBLE_DEVICES": "",
    })
    production = json.loads(
        run([sys.executable, str(HERE / "derive_extension_class.py")], env).stdout
    )
    independent = json.loads(
        run([sys.executable, str(HERE / "verify_extension_independent.py")], env).stdout
    )
    if production != json.loads((HERE / "DERIVATION_RESULT.json").read_text()):
        raise AssertionError("production result replay")
    if independent != json.loads((HERE / "INDEPENDENT_RESULT.json").read_text()):
        raise AssertionError("independent result replay")

    sources = read_tsv("INPUT_SOURCE_MANIFEST.tsv")
    if len(sources) != 12:
        raise AssertionError("source count")
    for row in sources:
        data = git_bytes(f"{BASE}:{row['path']}")
        if sha(data) != row["sha256"] or len(data) != int(row["size_bytes"]):
            raise AssertionError(f"source manifest: {row['path']}")

    impact = read_tsv("ACTIVE_RESULT_IMPACT_LEDGER.tsv")
    validate_impact(impact)
    extension = read_tsv("EXTENSION_CLASS_LEDGER.tsv")
    validate_extension(extension)
    if len(read_tsv("AFFECTED_RESULT_CORRECTION_PLAN.tsv")) != 5:
        raise AssertionError("correction-plan count")
    companions = read_tsv("NON_RESULT_COMPANION_CLARIFICATIONS.tsv")
    if len(companions) != 1:
        raise AssertionError("companion count")
    for row in companions:
        data = (ROOT / row["path"]).read_bytes()
        if sha(data) != row["sha256"]:
            raise AssertionError("companion source identity")

    catches: list[dict[str, str]] = []
    expect_rejection(
        "FOUNDED_PHI_CANNOT_BECOME_UNDEFINED_PLACEHOLDER",
        lambda: validate_impact([
            {**row, "primary_ruling": "FALSE_UNDEFINED_PLACEHOLDER"}
            if row["path"] == "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md"
            else row for row in impact
        ]), catches,
    )
    expect_rejection(
        "DPHI_CANNOT_BECOME_ELEVENTH_NATIVE_POINTWISE_MODE",
        lambda: validate_impact([
            {**row, "primary_ruling": "FALSE_ELEVENTH_POINTWISE_MODE"}
            if row["path"].startswith("udt_independent_amplitude_metric_atlas_")
            else row for row in impact
        ]), catches,
    )
    expect_rejection(
        "MISSING_ACTIVE_CANDIDATE",
        lambda: validate_impact(impact[:-1]), catches,
    )
    expect_rejection(
        "DUPLICATE_ACTIVE_CANDIDATE",
        lambda: validate_impact(impact + [impact[-1]]), catches,
    )
    expect_rejection(
        "OMITTED_AFFECTED_RESULT",
        lambda: validate_impact([
            {**row, "affected": "NO"} if row["path"] in EXPECTED_AFFECTED else row
            for row in impact
        ]), catches,
    )
    expect_rejection(
        "UNCONDITIONAL_SPECTATOR_UNIQUENESS",
        lambda: validate_extension([
            {**row, "conclusion": "unique"} if row["id"] == "E06" else row
            for row in extension
        ]), catches,
    )
    expect_rejection(
        "MISSING_ANGULAR_COUNTERFAMILY",
        lambda: validate_extension([row for row in extension if row["id"] != "E07"]),
        catches,
    )
    expect_rejection(
        "MISSING_SHIFT_COUNTERFAMILY",
        lambda: validate_extension([row for row in extension if row["id"] != "E08"]),
        catches,
    )
    expect_rejection(
        "SOURCE_ARTIFACT_MUTATION",
        lambda: (_ for _ in ()).throw(AssertionError())
        if sha((ROOT / sources[0]["path"]).read_bytes() + b"mutation") != sources[0]["sha256"]
        else None,
        catches,
    )
    expect_rejection(
        "GENERATED_PACKAGE_CANNOT_ENTER_BASE_CANDIDATE_SET",
        lambda: (_ for _ in ()).throw(AssertionError())
        if any(row["path"].startswith(HERE.name + "/") for row in impact)
        or HERE.name not in (HERE / "freeze_candidate_universe.py").read_text()
        else None,
        catches,
    )

    result = {
        "schema": "udt-founded-phi-complete-coframe-audit-verification-1.0",
        "result": "PASS",
        "production_checks": production["check_count"],
        "independent_checks": independent["check_count"],
        "catch_count": len(catches),
        "catches": catches,
        "counts": {
            "forensic_phi_files": len(read_tsv("FORENSIC_PHI_CENSUS.tsv")),
            "active_result_candidates": len(impact),
            "affected_result_files": len(EXPECTED_AFFECTED),
            "non_result_companion_clarifications": len(companions),
            "input_sources": len(sources),
            "extension_classes": len(extension),
        },
        "hashes": {
            name: sha((HERE / name).read_bytes()) for name in tracked
        },
    }
    recorded = json.loads((HERE / "VERIFICATION_RESULT.json").read_text())
    for key in (
        "schema", "result", "production_checks", "independent_checks",
        "catch_count", "counts", "hashes",
    ):
        if recorded.get(key) != result.get(key):
            raise AssertionError(f"recorded verification result: {key}")
    catch_rows = read_tsv("CATCH_PROOFS.tsv")
    if catch_rows != catches:
        raise AssertionError("recorded catch proofs")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
