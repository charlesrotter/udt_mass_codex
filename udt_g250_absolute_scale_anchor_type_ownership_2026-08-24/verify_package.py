#!/usr/bin/env python3
"""No-write verifier for the bounded G250 package."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent.parent
PKG = Path(__file__).resolve().parent
LANDING = (
    "ONE_MATCHED_NONZERO_HOMOTHETY_WEIGHT_ANCHOR_CONDITIONALLY_FIXES_THE_SINGLE_G249_SCALE"
    "__ADDITIONAL_INDEPENDENT_ANCHORS_TEST_THE_SUPPLIED_DIMENSIONLESS_HISTORY_RATHER_THAN_ADD_SCALE_PARAMETERS"
    "__CE_GOBS_RECIPROCAL_REDSHIFT_AND_RELATIVE_SNE_STATE_DO_NOT_FIX_ABSOLUTE_SCALE"
    "__MASS_DENSITY_ENERGY_COMPOSITES_ARE_DIMENSIONAL_CANDIDATES_ONLY_UNTIL_A_METRIC_ATTACHMENT_LAW_IS_SUPPLIED"
    "__G99_XEFF_REMAINS_HISTORICAL_TRANSFER_CONDITIONAL_NOT_NATIVE_G249_INPUT"
    "__NO_ANCHOR_VALUE_HISTORY_PROFILE_OR_OUTCOME_SELECTED"
)
HOSTILE_KEYS = frozenset({
    "anchor_selects_branch_rejected",
    "anchor_selects_history_rejected",
    "area_linear_recovery_rejected",
    "area_square_root_recovery_control",
    "attachment_free_density_scale_rejected",
    "attachment_free_mass_scale_rejected",
    "ce_called_interval_rejected",
    "ce_gobs_mass_neutrality_rejects_length",
    "curvature_direct_ratio_recovery_rejected",
    "curvature_inverse_square_recovery_control",
    "g248_probability_promotion_rejected",
    "g99_native_promotion_rejected",
    "inconsistent_second_anchor_rejected",
    "linear_length_recovery_control",
    "relative_sne_absolute_owner_rejected",
    "same_object_gate_erasure_rejected",
    "second_anchor_consistency_control",
    "weight_zero_scale_owner_rejected",
    "xmax_anchor_promotion_rejected",
    "zero_curvature_anchor_rejected",
})


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def source_matches(path: Path, expected: str, relative: str) -> bool:
    if sha256(path) == expected:
        return True
    if relative != "CURRENT_SCIENTIFIC_PREMISES.tsv":
        return False
    lines = path.read_bytes().splitlines(keepends=True)
    g250_rows = [index for index, line in enumerate(lines) if line.startswith(b"G250\t")]
    if len(g250_rows) != 1:
        return False
    historical = b"".join(line for index, line in enumerate(lines) if index != g250_rows[0])
    return hashlib.sha256(historical).hexdigest() == expected


def replay(script: str, *arguments: str) -> dict:
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        [sys.executable, str(PKG / script), *arguments],
        cwd=ROOT,
        env=environment,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def hostile_valid(result: dict) -> bool:
    mutations = result.get("mutations", {})
    return (
        result.get("status") == "PASS"
        and result.get("implementation") == "formula_and_type_level_mutations_no_phrase_search"
        and result.get("caught") == 20
        and result.get("total") == 20
        and result.get("missed") == []
        and frozenset(mutations) == HOSTILE_KEYS
        and all(mutations.values())
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    required = [
        "MAP.md", "PREMISE_LEDGER.tsv", "PREREGISTRATION.md",
        "PREREGISTRATION_COMMIT.md", "PREREGISTRATION_EXECUTION_NOTE.md",
        "SOURCE_MANIFEST.tsv", "EXACT_DERIVATION.md", "AUDIT_REPORT.md", "LAY_REPORT.md",
        "STATUS_LEDGER.tsv", "EVIDENCE_GATES.md", "COMMANDS.md", "REVIEW_REQUEST.md",
        "DERIVATION_RESULT.json", "INDEPENDENT_VERIFICATION.json", "CATCH_PROOF_RESULT.json",
        "CANDIDATE_CLASSIFICATION.tsv", "derive_absolute_scale_anchor_types.py",
        "verify_absolute_scale_anchor_types_independent.py", "run_catch_proofs.py",
        "verify_package.py", "build_review_intake.py",
    ]
    missing = [name for name in required if not (PKG / name).is_file()]
    if missing:
        raise SystemExit(f"missing package files: {missing}")

    with (PKG / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        sources = list(csv.DictReader(stream, delimiter="\t"))
    source_checks = []
    for row in sources:
        path = ROOT / row["path"]
        source_checks.append(path.is_file() and source_matches(path, row["sha256"], row["path"]))

    with (PKG / "CANDIDATE_CLASSIFICATION.tsv").open(newline="", encoding="utf-8") as stream:
        candidates = list(csv.DictReader(stream, delimiter="\t"))
    classifications = {row["candidate"]: row["classification"] for row in candidates}

    saved_production = json.loads((PKG / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    saved_independent = json.loads((PKG / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    saved_catches = json.loads((PKG / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    live_production = replay("derive_absolute_scale_anchor_types.py", "--cases", "4096")
    live_independent = replay("verify_absolute_scale_anchor_types_independent.py", "--cases", "12000")
    live_catches = replay("run_catch_proofs.py")

    deleted_catches = dict(saved_catches)
    deleted_mutations = dict(saved_catches.get("mutations", {}))
    deleted_mutations.pop("same_object_gate_erasure_rejected", None)
    deleted_catches["mutations"] = deleted_mutations
    deleted_catches["caught"] = len(deleted_mutations)
    deleted_catches["total"] = len(deleted_mutations)

    checks = {
        "required_files": not missing,
        "source_manifest_nine_exact": len(sources) == 9 and all(source_checks),
        "production_saved_pass": saved_production.get("status") == "PASS",
        "independent_saved_pass": saved_independent.get("status") == "PASS",
        "catch_saved_pass": saved_catches.get("status") == "PASS",
        "production_landing": saved_production.get("landing") == LANDING,
        "independent_landing": saved_independent.get("expected_landing") == LANDING,
        "production_replay_exact": live_production == saved_production,
        "independent_replay_exact": live_independent == saved_independent,
        "catch_replay_exact": live_catches == saved_catches,
        "production_case_floor": saved_production.get("sampled", {}).get("cases", 0) >= 4096,
        "independent_case_floor": saved_independent.get("cases", 0) >= 12000,
        "independent_implementation": saved_independent.get("implementation") == "standard_library_fraction_no_production_import_or_output_read",
        "candidate_count_exact": len(candidates) == 18 and saved_production.get("candidate_count") == 18,
        "direct_area_class": classifications.get("matched_screen_or_orbit_area") == "CONDITIONALLY_SUFFICIENT_DIRECT",
        "ce_gobs_class": classifications.get("c_E_plus_G_obs") == "INSUFFICIENT_NO_LENGTH_MONOMIAL",
        "mass_bridge_class": classifications.get("G_obs_M_over_c_E_squared") == "DIMENSIONALLY_ELIGIBLE_NEEDS_ATTACHMENT",
        "relative_sne_class": classifications.get("G236_G237_relative_SNe_state") == "INSUFFICIENT_ABSOLUTE_ZERO_POINT_REMOVED",
        "g99_class": classifications.get("G99_M_B_conditional_X_eff") == "CONDITIONAL_EXTERNAL_CROSSCHECK_NOT_NATIVE_INPUT",
        "hostile_exact_ledger": hostile_valid(saved_catches),
        "hostile_deleted_entry_rejected": not hostile_valid(deleted_catches),
        "outcomes_unused": saved_production.get("observational_values_used") == 0 and saved_independent.get("observational_values_used") == 0,
        "zero_fitted_coefficients": saved_production.get("fitted_coefficients") == 0 and saved_independent.get("fitted_coefficients") == 0,
        "blinding_limit_disclosed": "Strict reviewer blinding was not preserved" in (PKG / "PREREGISTRATION_EXECUTION_NOTE.md").read_text(encoding="utf-8"),
    }
    failed = [name for name, value in checks.items() if not value]
    result = {"checks": checks, "failed": failed, "status": "PASS" if not failed else "FAIL"}
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
