#!/usr/bin/env python3
"""Mechanical verifier for the bounded G280 package."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load(name: str) -> dict[str, object]:
    with (PACKAGE / name).open() as handle:
        return json.load(handle)


def frozen_source_bytes(relative: str, expected_size: int, expected_sha256: str) -> bytes:
    """Read the exact frozen source from the worktree or immutable Git history."""

    live = ROOT / relative
    if live.is_file():
        payload = live.read_bytes()
        if len(payload) == expected_size and hashlib.sha256(payload).hexdigest() == expected_sha256:
            return payload
    revisions = subprocess.run(
        ["git", "log", "--format=%H", "--", relative],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.splitlines()
    for revision in revisions:
        frozen = subprocess.run(
            ["git", "show", f"{revision}:{relative}"],
            cwd=ROOT,
            capture_output=True,
            check=False,
        )
        if (
            frozen.returncode == 0
            and len(frozen.stdout) == expected_size
            and hashlib.sha256(frozen.stdout).hexdigest() == expected_sha256
        ):
            return frozen.stdout
    raise AssertionError(f"frozen source unavailable: {relative}")


def main() -> None:
    required = {
        "MAP.md",
        "PREREGISTRATION.md",
        "PREMISE_LEDGER.tsv",
        "SOURCE_SCOPE.tsv",
        "SOURCE_MANIFEST.tsv",
        "COMMANDS.md",
        "EXACT_DERIVATION.md",
        "AUDIT_REPORT.md",
        "LAY_REPORT.md",
        "STATUS_LEDGER.tsv",
        "EVIDENCE_GATES.md",
        "EXTERNAL_REVIEW_REQUEST.md",
        "EXTERNAL_REVIEW_GPT54.md",
        "TRANSMISSION_RECORD.md",
        "REPAIR_PREREGISTRATION.md",
        "REPAIR_FOLLOWUP_REQUEST.md",
        "EXTERNAL_REPAIR_FOLLOWUP.md",
        "DERIVATION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "CATCH_PROOF_RESULT.json",
        "derive_projective_optical_bridge.py",
        "verify_projective_optical_bridge_independent.py",
        "run_catch_proofs.py",
        "freeze_source_manifest.py",
        "verify_package.py",
        "build_review_intake.py",
    }
    missing = sorted(name for name in required if not (PACKAGE / name).is_file())
    assert not missing, missing

    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="") as handle:
        sources = list(csv.DictReader(handle, delimiter="\t"))
    assert len(sources) == 12
    for row in sources:
        frozen_source_bytes(row["path"], int(row["bytes"]), row["sha256"])
        lowered = row["path"].lower()
        assert "onshell_timelive_reset" not in lowered
        assert "regime_flow_reciprocal_orchestra" not in lowered
        assert "sne_xmax_g88" not in lowered
        assert "curvature_holonomy_atlas" not in lowered

    derivation = load("DERIVATION_RESULT.json")
    independent = load("INDEPENDENT_VERIFICATION.json")
    catches = load("CATCH_PROOF_RESULT.json")
    assert derivation["status"] == "PASS"
    assert derivation["selected_alternative"] == "B"
    assert derivation["cases"]["assertions"] == 36883
    assert derivation["cases"]["projective"] == 4096
    assert derivation["cases"]["regular_precaustic_area"] == 4096
    assert derivation["cases"]["primary_radial"] == 4096
    assert derivation["fitted_coefficients"] == 0
    assert derivation["observational_outcomes_used"] == 0
    assert independent["status"] == "PASS"
    assert independent["cases"] == 4096
    assert independent["assertions"] == 40960
    assert independent["production_module_imported"] is False
    assert independent["production_result_read"] is False
    assert independent["different_native_screen_area"] is True
    assert independent["different_primary_radial_areal_radius"] is True
    assert catches["status"] == "PASS"
    assert catches["caught"] == catches["expected"] == 8
    assert catches["executable_mutations"] == 4
    assert catches["provenance_guards"] == 4
    assert catches["repair_fail_closed_mutations"]["caught"] == 10
    assert catches["repair_fail_closed_mutations"]["expected"] == 10
    assert sum(item["check_kind"] == "executable_mutation" for item in catches["checks"]) == 4
    assert sum(item["check_kind"] == "provenance_guard" for item in catches["checks"]) == 4
    center = next(
        item
        for item in catches["checks"]
        if item["name"] == "equating_areal_radius_to_projective_position_forces_nonsmooth_center_profile"
    )
    assert center["evidence"]["forced_center_slope"] == 1
    assert center["evidence"]["smooth_center_control_slope"] == 0

    report = (PACKAGE / "AUDIT_REPORT.md").read_text()
    assert "SAME_COMPLETE_PROJECTIVE_PAIR_STATE_ADMITS_DIFFERENT_NATIVE_JACOBI_AREA" in report
    assert "Source-bounded metric geometry only" in report
    assert "EXTERNAL_REPAIR_ACCEPTED__BOUNDED_LANDING_UNCHANGED" in report
    followup = (PACKAGE / "EXTERNAL_REPAIR_FOLLOWUP.md").read_text()
    assert followup.startswith("REPAIRS_ACCEPTED__BOUNDED_LANDING_UNCHANGED")
    assert "Remaining scoped defect: none." in followup
    print(
        "PASS: 12 frozen sources; 36883 symbolic/production assertions; "
        "40960 independent assertions; 4 executable mutations; 4 provenance guards; "
        "10 repair fail-closed mutations; G280 alternative B"
    )


if __name__ == "__main__":
    main()
