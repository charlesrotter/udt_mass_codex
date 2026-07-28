#!/usr/bin/env python3
"""Independent fail-closed checks for the post-verdict legacy comparison."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parent
EXPECTED_FAMILIES = {
    "F01_GR_S2_COUPLED": 3,
    "F02_LEGACY_SCALAR_SOURCE": 5,
    "F03_S2_STRESS_PROBE": 1,
    "F04_NONROUND_SL_PROXY": 5,
    "F05_W_CHANNEL_ACTION": 2,
    "F06_SIMPLE_L_SPECTRUM": 1,
    "F07_C2_EH_FLUX": 2,
    "F08_SPHERICAL_AREAL_KINEMATICS": 2,
}


def git(*args: str) -> str:
    return subprocess.check_output(("git", *args), cwd=REPO, text=True).strip()


def read_rows() -> list[dict[str, str]]:
    with (HERE / "LEGACY_TIME_SYSTEMS.tsv").open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def validate(rows: list[dict[str, str]]) -> list[str]:
    errors = []
    paths = [row["path"] for row in rows]
    if len(rows) != 21 or len(paths) != len(set(paths)):
        errors.append("coverage_or_duplicate")
    if Counter(row["family"] for row in rows) != Counter(EXPECTED_FAMILIES):
        errors.append("family_counts")
    if any(row["current_background_solve_authorized"] != "NO" for row in rows):
        errors.append("background_promotion")
    retained = [row for row in rows if row["current_disposition"].startswith("RETAINED_")]
    if len(retained) != 5:
        errors.append("retained_count")
    historical = [row for row in rows if not row["current_disposition"].startswith("RETAINED_")]
    if len(historical) != 16:
        errors.append("historical_count")
    if sum(row["first_date"][:10] < "2026-07-01" for row in rows) != 16:
        errors.append("pre_firewall_count")
    if sum(row["first_date"][:10] >= "2026-07-01" for row in rows) != 5:
        errors.append("post_firewall_count")

    by_family = {}
    for row in rows:
        by_family.setdefault(row["family"], []).append(row)
        path = REPO / row["path"]
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != row["sha256"]:
            errors.append(f"sha:{row['path']}")
        if git("rev-parse", f"HEAD:{row['path']}") != row["git_blob"]:
            errors.append(f"blob:{row['path']}")

    if any(row["operator_provenance"] != "IMPORTED_GR_EINSTEIN_EOM_PLUS_POSIT_S2_L2L4_ACTION" for row in by_family.get("F01_GR_S2_COUPLED", [])):
        errors.append("F01_provenance")
    if any("INDEPENDENT_SCALAR" not in row["operator_provenance"] for row in by_family.get("F02_LEGACY_SCALAR_SOURCE", [])):
        errors.append("F02_provenance")
    if any("POSIT_S2" not in row["operator_provenance"] for row in by_family.get("F03_S2_STRESS_PROBE", [])):
        errors.append("F03_provenance")
    if any("STURM_LIOUVILLE_PROXY" not in row["operator_provenance"] for row in by_family.get("F04_NONROUND_SL_PROXY", [])):
        errors.append("F04_provenance")
    if any("SUPPLIED_W_CHANNEL_ACTION" not in row["operator_provenance"] for row in by_family.get("F05_W_CHANNEL_ACTION", [])):
        errors.append("F05_provenance")
    if any("SPECTRAL_OPERATOR" not in row["operator_provenance"] for row in by_family.get("F06_SIMPLE_L_SPECTRUM", [])):
        errors.append("F06_provenance")
    if any(row["current_disposition"] != "RETAINED_CONDITIONAL_OPERATOR_COMPARISON_NOT_SELECTED_DYNAMICS" for row in by_family.get("F07_C2_EH_FLUX", [])):
        errors.append("F07_scope")
    if any(row["current_disposition"] != "RETAINED_CONDITIONAL_KINEMATICS_NOT_BACKGROUND_DYNAMICS" for row in by_family.get("F08_SPHERICAL_AREAL_KINEMATICS", [])):
        errors.append("F08_scope")
    return errors


def catches(rows: list[dict[str, str]]) -> dict[str, bool]:
    out = {}
    x = copy.deepcopy(rows); x[0]["current_background_solve_authorized"] = "YES"; out["background_promotion_rejected"] = bool(validate(x))
    x = copy.deepcopy(rows); x = x[:-1]; out["missing_path_rejected"] = bool(validate(x))
    x = copy.deepcopy(rows); x.append(copy.deepcopy(x[0])); out["duplicate_path_rejected"] = bool(validate(x))
    x = copy.deepcopy(rows); x[0]["sha256"] = "0" * 64; out["hash_mutation_rejected"] = bool(validate(x))
    x = copy.deepcopy(rows); next(r for r in x if r["family"] == "F07_C2_EH_FLUX")["current_disposition"] = "SELECTED_NATIVE_DYNAMICS"; out["conditional_action_promotion_rejected"] = bool(validate(x))
    x = copy.deepcopy(rows); next(r for r in x if r["family"] == "F08_SPHERICAL_AREAL_KINEMATICS")["current_disposition"] = "NATIVE_BACKGROUND_EVOLUTION"; out["kinematic_promotion_rejected"] = bool(validate(x))
    return out


def main() -> None:
    rows = read_rows()
    errors = validate(rows)
    catch = catches(rows)
    if not git("merge-base", "--is-ancestor", "6c89b7a", "HEAD") == "":
        errors.append("cleanroom_commit_not_ancestor")
    clean_blob = git("rev-parse", "6c89b7a:udt_cleanroom_metric_reduction_readiness_audit_2026-07-27/DERIVATION_RESULT.json")
    current_blob = git("rev-parse", "HEAD:udt_cleanroom_metric_reduction_readiness_audit_2026-07-27/DERIVATION_RESULT.json")
    if clean_blob != current_blob:
        errors.append("cleanroom_result_changed_after_legacy_inspection")
    if not all(catch.values()):
        errors.append("catch_failure")
    summary = json.loads((HERE / "LEGACY_PROVENANCE_RESULT.json").read_text())
    if summary.get("scripts") != 21 or summary.get("background_solve_authorized") != 0:
        errors.append("summary_mismatch")
    result = {
        "schema": "udt-cleanroom-legacy-provenance-verification-1.0",
        "result": "PASS" if not errors else "FAIL",
        "errors": errors,
        "scripts": 21,
        "family_counts": EXPECTED_FAMILIES,
        "pre_july_scripts": 16,
        "post_july_scripts": 5,
        "retained_conditional_nonbackground_scripts": 5,
        "historical_or_blocked_scripts": 16,
        "background_solve_authorized": 0,
        "cleanroom_result_blob_unchanged": clean_blob == current_blob,
        "catch_proofs": catch,
        "ledger_sha256": hashlib.sha256((HERE / "LEGACY_TIME_SYSTEMS.tsv").read_bytes()).hexdigest(),
    }
    (HERE / "LEGACY_VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))
    raise SystemExit(0 if not errors else 1)


if __name__ == "__main__":
    main()
