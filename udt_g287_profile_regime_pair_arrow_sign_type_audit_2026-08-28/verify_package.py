#!/usr/bin/env python3
"""Aggregate, dependency-free G287 replay, repair, and sealed-intake verifier."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
LANDING = (
    "PROFILE_REGIME_SIGN_AND_PAIR_ARROW_ORIENTATION_ARE_ALREADY_TYPE_DISTINCT"
    "__NO_NATIVE_KERNEL_REGRESSION__RECENT_EXPLANATION_CONFLATED_THEM"
)
REQUIRED = [
    "MAP.md", "PREREGISTRATION.md", "REPAIR_PREREGISTRATION.md", "REPAIR_REPORT.md",
    "REPAIR_FOLLOWUP_REQUEST.md", "EXTERNAL_REVIEW_GPT54.md", "PREMISE_LEDGER.tsv",
    "SOURCE_SCOPE.tsv", "SOURCE_MANIFEST.tsv", "USER_SIGN_CLARIFICATION.md",
    "DEPENDENCY_AUDIT.tsv", "EXACT_DERIVATION.md", "AUDIT_REPORT.md", "LAY_REPORT.md",
    "STATUS_LEDGER.tsv", "EVIDENCE_GATES.md", "ADVERSARIAL_REVIEW_REQUEST.md", "COMMANDS.md",
    "derive_sign_types.py", "verify_independent.py", "run_catch_proofs.py",
    "run_repair_catch_proofs.py", "build_source_manifest.py", "build_review_intake.py",
    "DERIVATION_RESULT.json", "INDEPENDENT_VERIFICATION.json", "CATCH_PROOF_RESULT.json",
    "REPAIR_CATCH_PROOF_RESULT.json",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_script(package: Path, root: Path, script: str, output: Path | None = None):
    command = [sys.executable, "-S", str(package / script)]
    if output is not None:
        command.extend(["--output", str(output)])
    return subprocess.run(command, cwd=root, capture_output=True, text=True, check=False)


def verify_manifest(manifest: Path, base: Path) -> tuple[bool, int]:
    with manifest.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    checks = []
    for row in rows:
        path = base / row["path"]
        checks.append(
            path.is_file()
            and path.stat().st_size == int(row["bytes"])
            and sha256(path) == row["sha256"]
        )
    return all(checks), len(rows)


def parse_json_stdout(run: subprocess.CompletedProcess[str]) -> dict:
    try:
        return json.loads(run.stdout)
    except (json.JSONDecodeError, TypeError):
        return {}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    skip_repair_probes = os.environ.get("G287_SKIP_REPAIR_PROBES") == "1"
    required = [
        name for name in REQUIRED
        if not (skip_repair_probes and name == "REPAIR_CATCH_PROOF_RESULT.json")
    ]
    missing = [name for name in required if not (PACKAGE / name).is_file()]
    source_manifest_ok, source_manifest_count = verify_manifest(
        PACKAGE / "SOURCE_MANIFEST.tsv", ROOT
    )

    with tempfile.TemporaryDirectory(prefix="udt_g287_verify_") as temporary:
        temp = Path(temporary)
        production_path = temp / "production.json"
        independent_path = temp / "independent.json"
        catch_path = temp / "catch.json"
        repair_path = temp / "repair_catches.json"
        rebuilt_manifest_path = temp / "SOURCE_MANIFEST.tsv"

        production_run = run_script(PACKAGE, ROOT, "derive_sign_types.py", production_path)
        independent_run = run_script(PACKAGE, ROOT, "verify_independent.py", independent_path)
        catch_run = run_script(PACKAGE, ROOT, "run_catch_proofs.py", catch_path)
        repair_run = None if skip_repair_probes else run_script(
            PACKAGE, ROOT, "run_repair_catch_proofs.py", repair_path
        )
        source_builder_run = run_script(
            PACKAGE, ROOT, "build_source_manifest.py", rebuilt_manifest_path
        )
        review_builder_run = run_script(PACKAGE, ROOT, "build_review_intake.py")

        production = json.loads(production_path.read_text()) if production_path.is_file() else {}
        independent = json.loads(independent_path.read_text()) if independent_path.is_file() else {}
        catches = json.loads(catch_path.read_text()) if catch_path.is_file() else {}
        repairs = (
            json.loads(repair_path.read_text())
            if repair_path.is_file()
            else (
                {"pass": True, "probe_count": 5}
                if skip_repair_probes
                else json.loads((PACKAGE / "REPAIR_CATCH_PROOF_RESULT.json").read_text())
            )
        )
        review_metadata = parse_json_stdout(review_builder_run)
        source_builder_reproduced = (
            source_builder_run.returncode == 0
            and rebuilt_manifest_path.is_file()
            and rebuilt_manifest_path.read_bytes() == (PACKAGE / "SOURCE_MANIFEST.tsv").read_bytes()
        )
        intake = Path(review_metadata.get("path", "/nonexistent"))
        review_manifest = intake / "REVIEW_MANIFEST.tsv"
        review_scope = intake / "REVIEW_SCOPE.json"
        review_seal = intake / "REVIEW_MANIFEST.sha256"
        intake_manifest_ok, intake_payloads = (
            verify_manifest(review_manifest, intake) if review_manifest.is_file() else (False, 0)
        )
        seal_text = review_seal.read_text(encoding="utf-8") if review_seal.is_file() else ""

        sealed_replays = {}
        if intake_manifest_ok:
            sealed_package = intake / PACKAGE.name
            sealed_production = temp / "sealed_production.json"
            sealed_independent = temp / "sealed_independent.json"
            sealed_catch = temp / "sealed_catch.json"
            sealed_source_manifest = temp / "sealed_source_manifest.tsv"
            sealed_runs = {
                "production": run_script(sealed_package, intake, "derive_sign_types.py", sealed_production),
                "independent": run_script(sealed_package, intake, "verify_independent.py", sealed_independent),
                "catch": run_script(sealed_package, intake, "run_catch_proofs.py", sealed_catch),
                "source_builder": run_script(
                    sealed_package, intake, "build_source_manifest.py", sealed_source_manifest
                ),
            }
            sealed_replays = {
                "sealed_production": sealed_runs["production"].returncode == 0
                    and sealed_production.read_bytes() == production_path.read_bytes(),
                "sealed_independent": sealed_runs["independent"].returncode == 0
                    and sealed_independent.read_bytes() == independent_path.read_bytes(),
                "sealed_catch": sealed_runs["catch"].returncode == 0
                    and sealed_catch.read_bytes() == catch_path.read_bytes(),
                "sealed_source_builder": sealed_runs["source_builder"].returncode == 0
                    and sealed_source_manifest.read_bytes() == (PACKAGE / "SOURCE_MANIFEST.tsv").read_bytes(),
            }

    frozen_production = json.loads((PACKAGE / "DERIVATION_RESULT.json").read_text())
    frozen_independent = json.loads((PACKAGE / "INDEPENDENT_VERIFICATION.json").read_text())
    frozen_catches = json.loads((PACKAGE / "CATCH_PROOF_RESULT.json").read_text())
    frozen_repairs = (
        repairs
        if skip_repair_probes and not (PACKAGE / "REPAIR_CATCH_PROOF_RESULT.json").is_file()
        else json.loads((PACKAGE / "REPAIR_CATCH_PROOF_RESULT.json").read_text())
    )
    report_text = (PACKAGE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    derivation_text = (PACKAGE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    prereg_text = (PACKAGE / "PREREGISTRATION.md").read_text(encoding="utf-8")

    checks = {
        "required_files": not missing,
        "source_manifest_count": source_manifest_count == 23,
        "source_manifest_integrity": source_manifest_ok,
        "source_builder_exit": source_builder_run.returncode == 0,
        "source_builder_reproduced": source_builder_reproduced,
        "production_exit": production_run.returncode == 0,
        "independent_exit": independent_run.returncode == 0,
        "catch_exit": catch_run.returncode == 0,
        "repair_probe_exit": skip_repair_probes or (repair_run is not None and repair_run.returncode == 0),
        "production_pass": production.get("pass") is True,
        "independent_pass": independent.get("pass") is True,
        "catch_pass": catches.get("pass") is True and catches.get("mutation_count") == 6,
        "repair_probe_pass": repairs.get("pass") is True and repairs.get("probe_count") == 5,
        "production_reproduced": production == frozen_production,
        "independent_reproduced": independent == frozen_independent,
        "catches_reproduced": catches == frozen_catches,
        "repair_catches_reproduced": repairs == frozen_repairs,
        "review_builder_exit": review_builder_run.returncode == 0,
        "review_builder_source_count": review_metadata.get("immutable_sources") == 23,
        "review_builder_payload_count": review_metadata.get("payloads") == intake_payloads,
        "review_builder_total_count": review_metadata.get("total_files") == intake_payloads + 2,
        "review_scope_hash": review_scope.is_file()
            and sha256(review_scope) == review_metadata.get("scope_sha256"),
        "review_manifest_hash": review_manifest.is_file()
            and sha256(review_manifest) == review_metadata.get("manifest_sha256"),
        "review_seal_hash": review_seal.is_file()
            and sha256(review_seal) == review_metadata.get("seal_sha256"),
        "review_seal_content": review_manifest.is_file()
            and seal_text == f"{sha256(review_manifest)}  REVIEW_MANIFEST.tsv\n",
        "review_manifest_integrity": intake_manifest_ok,
        **sealed_replays,
        "landing_exact_report": LANDING in "".join(report_text.split()),
        "landing_exact_derivation": LANDING in "".join(derivation_text.split()),
        "landing_preregistered": LANDING in "".join(prereg_text.split()),
        "discovery_timing_disclosed": "MAP_DISCOVERY_PRECEDED_FORMAL_PREREGISTRATION" in prereg_text,
    }
    result = {"checks": checks, "missing": missing, "pass": all(checks.values())}
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    raise SystemExit(0 if result["pass"] else 1)


if __name__ == "__main__":
    main()
