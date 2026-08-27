#!/usr/bin/env python3
"""Mechanical consistency verifier for the G278 evidence package."""

from __future__ import annotations

import csv
import hashlib
import json
import os
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
DES_ROOT = Path(os.environ["G236_DES_ROOT"]).resolve()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    external = {
        "external_data/DES-Dovekie_HD.csv": DES_ROOT / "DES-Dovekie_HD.csv",
        "external_data/STAT+SYS.npz": DES_ROOT / "STAT+SYS.npz",
    }
    source_checks = {}
    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            path = external.get(row["path"], ROOT / row["path"])
            source_checks[row["path"]] = path.is_file() and sha256(path) == row["sha256"]

    result = json.load((PACKAGE / "DERIVATION_RESULT.json").open())
    independent = json.load((PACKAGE / "INDEPENDENT_VERIFICATION.json").open())
    catch = json.load((PACKAGE / "CATCH_PROOF_RESULT.json").open())
    followup = json.load((PACKAGE / "RESOLUTION_FOLLOWUP_RESULT.json").open())
    required = [
        "MAP.md", "PREREGISTRATION.md", "PREMISE_LEDGER.tsv", "SOURCE_MANIFEST.tsv",
        "COMMANDS.md", "derive_scale_and_holdout.py", "DERIVATION_RESULT.json",
        "SCALE_RESULTS.tsv", "CALIBRATOR_SUBSET_CONTROLS.tsv", "DES_HOLDOUT_RESULTS.tsv",
        "PRODUCTION_RUN_LOG.txt", "verify_independent.py", "INDEPENDENT_VERIFICATION.json",
        "INDEPENDENT_RUN_LOG.txt", "run_catch_proofs.py", "CATCH_PROOF_RESULT.json",
        "CATCH_PROOF_RUN_LOG.txt", "AUDIT_REPORT.md", "LAY_REPORT.md", "EVIDENCE_GATES.md",
        "RESOLUTION_FOLLOWUP_PREREGISTRATION.md", "diagnose_resolution_sensitivity.py",
        "RESOLUTION_FOLLOWUP_RESULT.json", "RESOLUTION_CURVE_COMPARISON.tsv",
        "RESOLUTION_FOLLOWUP_RUN_LOG.txt", "RESOLUTION_FOLLOWUP_REPORT.md",
        "EXTERNAL_REVIEW.md", "EXTERNAL_REVIEW_TRANSMISSION.md",
        "EXTERNAL_REPAIR_PREREGISTRATION.md", "EXTERNAL_REPAIR_FOLLOWUP_REVIEW.md",
        "REPAIR_RESULT.md",
    ]
    checks = {
        "all_sources_match": bool(source_checks and all(source_checks.values())),
        "all_required_files_present": all((PACKAGE / name).is_file() for name in required),
        "landing_exact": result["landing"] == "SCALE_ATTACHMENT_RESOLUTION_OR_SUBSET_SENSITIVE",
        "only_resolution_gate_failed": bool(
            result["gates"]["g236_reproduction_pass"]
            and result["gates"]["primary_calibration_pass"]
            and not result["gates"]["resolution_pass"]
            and result["gates"]["subset_pass"]
            and result["gates"]["serialization_pass"]
            and result["gates"]["primary_DES_pass"]
        ),
        "independent_checks_pass": all(independent["checks"].values()),
        "catch_proofs_pass": all(catch["checks"].values()),
        "followup_landing_exact": followup["landing"] == "PHYSICAL_CURVE_RESOLUTION_SENSITIVITY_PERSISTS",
        "followup_retains_original": bool(
            followup["cannot_regrade_original"]
            and followup["original_landing"] == result["landing"]
            and not any(followup["forbidden_actions"].values())
        ),
        "no_scaffolding_or_retuning": bool(
            not result["frozen"]["kernel_retuned"]
            and not result["frozen"]["state_shape_retuned_by_calibrators"]
            and result["frozen"]["DES_parameters_fitted"] == 0
            and not result["frozen"]["P1_used"]
            and result["frozen"]["angular_coefficients_fitted"] == 0
            and not result["frozen"]["Xmax_used"]
        ),
        "followup_cannot_regrade_original": "not regrade this landing" in (PACKAGE / "AUDIT_REPORT.md").read_text(),
        "external_repairs_recorded": bool(
            "ACCEPT-WITH-REPAIRS" in (PACKAGE / "EXTERNAL_REVIEW.md").read_text()
            and "R1_R2_R3_EXTERNALLY_ACCEPTED" in (PACKAGE / "REPAIR_RESULT.md").read_text()
            and "Verdict: `ACCEPT`" in (PACKAGE / "EXTERNAL_REPAIR_FOLLOWUP_REVIEW.md").read_text()
        ),
        "sealed_command_surface_exact": bool(
            "G236_DES_ROOT=\"$PWD/external_data\"" in (PACKAGE / "COMMANDS.md").read_text()
            and "python3 verify_current_scientific_premises.py" not in (PACKAGE / "COMMANDS.md").read_text()
        ),
    }
    if not all(checks.values()):
        raise AssertionError({"checks": checks, "source_checks": source_checks})
    output = {
        "audit": "G278_PACKAGE_VERIFICATION",
        "checks": checks,
        "source_checks": source_checks,
        "durable_output_hashes": {
            name: sha256(PACKAGE / name)
            for name in required
            if name not in {"RESOLUTION_FOLLOWUP_PREREGISTRATION.md"}
        },
    }
    with (PACKAGE / "PACKAGE_VERIFICATION.json").open("w") as handle:
        json.dump(output, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
