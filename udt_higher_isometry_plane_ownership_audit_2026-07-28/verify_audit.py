#!/usr/bin/env python3
"""Fail-closed replay and mutation catches for the bounded audit."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def require(name: str, condition: bool, checks: list[str] | None = None) -> None:
    if not condition:
        raise AssertionError(name)
    if checks is not None:
        checks.append(name)


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env.update({"CUDA_VISIBLE_DEVICES": "", "PYTHONDONTWRITEBYTECODE": "1"})
    return subprocess.run(command, cwd=ROOT, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)


def keyed(rows: list[dict[str, str]], key: str) -> dict[str, dict[str, str]]:
    return {row[key]: row for row in rows}


def validate(
    production: dict[str, object],
    independent: dict[str, object],
    status_rows: list[dict[str, str]],
    strata_rows: list[dict[str, str]],
    circle_rows: list[dict[str, str]],
    outcomes: list[dict[str, str]],
) -> None:
    require("production_check_count", production["check_count"] == 135)
    require("production_symbolic", production["symbolic_check_count"] == 31)
    require("production_toric", production["toric_cap_pair_count"] == 104)
    require("primary", production["primary_classification"] == "UNIVERSAL_SELECTION_REFUTED__FAMILY_IDENTITY_ROBUSTNESS_DERIVED__GENERIC_FIXED_METRIC_SELECTION_OPEN")
    require("universal_refuted", production["universal_registered_plane_selection"] == "REFUTED_WITHIN_BOUNDED_FAMILY")
    require("generic_open", production["generic_registered_plane_selection"] == "OPEN_QUANTIFIER_CORRECTION_REQUIRED_FIXED_PROFILE_CLASSIFICATION")
    require("family_identity", production["family_identity_registered_plane_robustness"] == "DERIVED_UNDER_INDEPENDENT_CONFIGURATION_FAMILY_VARIATION")
    require("fixed_metric_open", production["plane_scan"]["generic_fixed_metric_unique_constant_area_plane"] == "OPEN")
    require("full_response_distinction", production["full_response"]["important_distinction"] == "full_orbit_D_eigenplane_is_not_the_restricted_two_plane_scan")
    require("full_plus", production["full_response"]["plus_2chi_eigenvalue_when_chi_df_nonzero"] is False)
    require("topology_count", production["topology"]["smooth_S3_unimodular_caps_free_unoriented_circle_count"] == 2)
    require("topology_no_select", production["topology"]["topology_selects_registered_V"] is False)
    require("counter_alpha", production["countercontrol"]["alpha"] == 0)
    require("counter_nonconstant", production["countercontrol"]["phi_nonconstant"] is True)
    require("counter_planes", production["countercontrol"]["reciprocal_planes"] == ["span(K,V)", "span(K,Y)"])
    require("macro_open", production["macro_micro_assignment"] == "OPEN_NOT_TESTED")
    require("independent_status", independent["status"] == "PASS")
    require("independent_checks", independent["checks_passed"] == 292)
    require("independent_caps", independent["independent_cap_pair_count"] == 232)
    require("independent_histogram", independent["free_line_histogram"] == {"2": 232})

    status = keyed(status_rows, "claim_id")
    require("status_rows", len(status) == 11)
    require("R07", status["R07"]["status"] == "REFUTED_BOUNDED")
    require("R01_scope", status["R01"]["scope"] == "stationary_descended_block_screen_principal_orbits_b_positive")
    require("R02_scope", "b_positive" in status["R02"]["scope"])
    require("R03", status["R03"]["status"] == "DERIVED_IDENTITY_LEVEL_ONLY")
    require("R04", status["R04"]["status"] == "DERIVED_IDENTITY_LEVEL_ONLY")
    require("R08", status["R08"]["status"] == "OPEN")
    require("R09", status["R09"]["status"] == "REFUTED_WHERE_df_NONZERO_ON_PRINCIPAL_ORBITS")
    require("R10", status["R10"]["status"] == "OPEN")
    require("R11", status["R11"]["status"] == "OPEN")

    strata = keyed(strata_rows, "id")
    require("strata_rows", len(strata) == 8)
    require("S02", strata["S02"]["classification"] == "FAMILY_IDENTITY_RESULT__FIXED_METRIC_UNIQUENESS_OPEN")
    require("S03", strata["S03"]["classification"] == "MULTIPLE_EQUIVALENT_RECIPROCAL_PLANES")
    require("S04", strata["S04"]["classification"] == "REGISTERED_PAIR_RATE_DISTINGUISHED_IN_THIS_WITNESS")
    require("S06", strata["S06"]["classification"] == "UNVERIFIED_ILLUSTRATION_NOT_EVIDENCE")
    require("S07", strata["S07"]["classification"] == "UNVERIFIED_ILLUSTRATION_NOT_EVIDENCE")
    require("S08", strata["S08"]["classification"] == "OPEN_OUTSIDE_BOUNDED_FAMILY")
    require("circles", len(circle_rows) == 4 and sum(row["free_at_both_caps"] == "YES" for row in circle_rows) == 4)
    outcome = keyed(outcomes, "id")
    require("outcomes", len(outcomes) == 8)
    require("F04_downgraded", outcome["F04"]["status"] == "REFUTED_AND_DOWNGRADED_OPEN")
    require("other_outcomes", all(row["status"] == "PASS" for row in outcomes if row["id"] != "F04"))


def main() -> None:
    checks: list[str] = []
    replay = run([sys.executable, str(HERE / "run_and_capture.py")])
    require("run_and_capture", replay.returncode == 0, checks)
    environment = json.loads((HERE / "RUN_ENVIRONMENT.json").read_text(encoding="utf-8"))
    expected_stream_hashes = {
        "production_stdout_sha256": "1d65b56d5e9511bc349a9ae8bb1e1d54f9ab52349e4fca3b0d38b889bd72d30d",
        "production_stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "independent_stdout_sha256": "a3808e1a41a27c6a3235c8d0b919f9714219d04b46f44691c63e383b787d580b",
        "independent_stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    }
    require("raw_stream_hashes", all(environment[key] == value for key, value in expected_stream_hashes.items()), checks)
    premise = run([sys.executable, "verify_current_scientific_premises.py"])
    require("premise_replay", premise.returncode == 0, checks)

    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text(encoding="utf-8"))
    status_rows = list(csv.DictReader((HERE / "STATUS_LEDGER.tsv").open(encoding="utf-8"), delimiter="\t"))
    strata_rows = list(csv.DictReader((HERE / "HIGHER_ISOMETRY_STRATA.tsv").open(encoding="utf-8"), delimiter="\t"))
    circle_rows = list(csv.DictReader((HERE / "FREE_CIRCLE_CLASSES.tsv").open(encoding="utf-8"), delimiter="\t"))
    outcomes = list(csv.DictReader((HERE / "FALSIFICATION_OUTCOMES.tsv").open(encoding="utf-8"), delimiter="\t"))
    validate(production, independent, status_rows, strata_rows, circle_rows, outcomes)
    checks.append("artifact_validation")

    mutations: list[tuple[str, str, object]] = [
        ("production", "check_count", 134),
        ("production", "primary_classification", "GENERIC_SELECTION_WITH_EXACT_EXCEPTIONAL_MULTIPLE_PLANE_STRATA"),
        ("production", "universal_registered_plane_selection", "DERIVED"),
        ("production", "generic_registered_plane_selection", "DERIVED_FOR_OPEN_INDEPENDENT_FIRST_JET_STRATUM_BY_RESTRICTED_PLANE_SCAN"),
        ("production", "family_identity_registered_plane_robustness", "GENERIC_FIXED_METRIC_THEOREM"),
        ("production.plane_scan", "generic_fixed_metric_unique_constant_area_plane", "span(K,V)"),
        ("production", "macro_micro_assignment", "DERIVED"),
        ("production.full_response", "important_distinction", "SAME_OPERATION"),
        ("production.full_response", "plus_2chi_eigenvalue_when_chi_df_nonzero", True),
        ("production.topology", "smooth_S3_unimodular_caps_free_unoriented_circle_count", 1),
        ("production.topology", "topology_selects_registered_V", True),
        ("production.countercontrol", "alpha", 1),
        ("production.countercontrol", "phi_nonconstant", False),
        ("production.countercontrol", "reciprocal_planes", ["span(K,V)"]),
        ("independent", "status", "FAIL"),
        ("independent", "checks_passed", 291),
        ("independent", "independent_cap_pair_count", 104),
        ("status.R07", "status", "DERIVED"),
        ("status.R01", "scope", "stationary_descended_block_screen"),
        ("status.R03", "status", "DERIVED_GENERIC"),
        ("status.R04", "status", "DERIVED_GENERIC"),
        ("status.R08", "status", "DERIVED_WITH_EXCEPTIONAL_LOCI"),
        ("status.R09", "status", "REFUTED_GENERIC_WHERE_df_NONZERO"),
        ("status.R10", "status", "DERIVED"),
        ("strata.S02", "classification", "SELECTED_BY_RESTRICTED_PLANE_SCAN_NOT_FULL_D_EIGENPLANE"),
        ("strata.S03", "classification", "UNIQUE"),
        ("strata.S04", "classification", "UNIVERSAL"),
        ("strata.S06", "classification", "PLANE_GROUP_SELECTED_CLOCK_OPEN_OR_MISMATCH"),
        ("strata.S07", "classification", "MULTIPLE_EQUIVALENT_PLANES"),
        ("strata.S08", "classification", "CLOSED"),
        ("outcome.F02", "status", "FAIL"),
        ("outcome.F04", "status", "PASS"),
    ]
    catch_rows: list[dict[str, str]] = []
    for index, (target, field, value) in enumerate(mutations, 1):
        p = copy.deepcopy(production)
        i = copy.deepcopy(independent)
        sr = copy.deepcopy(status_rows)
        tr = copy.deepcopy(strata_rows)
        cr = copy.deepcopy(circle_rows)
        oc = copy.deepcopy(outcomes)
        if target == "production":
            p[field] = value
        elif target.startswith("production."):
            p[target.split(".", 1)[1]][field] = value
        elif target == "independent":
            i[field] = value
        elif target.startswith("status."):
            keyed(sr, "claim_id")[target.split(".", 1)[1]][field] = value
        elif target.startswith("strata."):
            keyed(tr, "id")[target.split(".", 1)[1]][field] = value
        elif target.startswith("outcome."):
            keyed(oc, "id")[target.split(".", 1)[1]][field] = value
        else:
            raise AssertionError(target)
        caught = False
        try:
            validate(p, i, sr, tr, cr, oc)
        except AssertionError:
            caught = True
        require(f"catch_{index:02d}", caught)
        catch_rows.append({"id": f"C{index:02d}", "mutation": f"{target}.{field}={value}", "expected": "VERIFY_FAIL", "observed": "VERIFY_FAIL", "status": "PASS"})
    with (HERE / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(catch_rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(catch_rows)

    manifest = list(csv.DictReader((HERE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8"), delimiter="\t"))
    identity = "\n".join(f"{r['path']}\t{r['blob']}\t{r['sha256']}\t{r['bytes']}" for r in manifest) + "\n"
    source_identity = hashlib.sha256(identity.encode()).hexdigest()
    require("source_count", len(manifest) == 26, checks)

    initial_hashes = {
        "INITIAL_REFUTED_DERIVATION_RESULT.json": "f8ad7c7c339b71ec6e86c19c8a638e7f6aef236ff91477dbce3a9d8b0957f44b",
        "INITIAL_REFUTED_DERIVATION_STDOUT.txt": "f8ad7c7c339b71ec6e86c19c8a638e7f6aef236ff91477dbce3a9d8b0957f44b",
        "INITIAL_REFUTED_STATUS_LEDGER.tsv": "1bb2f1a12f4c78ec976f5d1caa9c2ffdcf28b97eda22f6fd16159b37c0bc5e2e",
        "INITIAL_REFUTED_HIGHER_ISOMETRY_STRATA.tsv": "53bd8afae60dc72bba52337d8c73e1c469b57099c060ef1e07dcc4485ee4c8de",
        "INITIAL_REFUTED_AUDIT_REPORT.md": "8776f263a096d17bd0ca8ce7a47c13b9ba27662a1d3953e4b92166a22fb672cd",
        "INITIAL_REFUTED_EXACT_DERIVATION.md": "29564e8edcfce0ee55cd7c52d31f7fd72947885edd49047561ce0d4f6e5db503",
        "FRESH_ADVERSARIAL_REVIEW.md": "21e99ac850291d189aaf578a47c238094e08d866dfa7c5c785e04408b25102cc",
    }
    for name, expected in initial_hashes.items():
        require(f"preserved_{name}", hashlib.sha256((HERE / name).read_bytes()).hexdigest() == expected, checks)

    review = HERE / "FRESH_ADVERSARIAL_REVIEW.md"
    require("fresh_review_exists", review.is_file(), checks)
    review_text = review.read_text(encoding="utf-8")
    require("initial_refutation_preserved", review_text.splitlines()[0].strip("`") == "REFUTED", checks)
    require("correction_layer", (HERE / "CORRECTION_LAYER.md").is_file(), checks)
    corrected_review = HERE / "CORRECTED_ADVERSARIAL_REVIEW.md"
    require("corrected_review_exists", corrected_review.is_file(), checks)
    corrected_review_text = corrected_review.read_text(encoding="utf-8")
    corrected_verdict = corrected_review_text.splitlines()[0].strip("`")
    require("corrected_review_verdict", corrected_verdict in {"PASS", "PASS_WITH_CAVEATS"}, checks)

    result = {
        "schema": "udt-higher-isometry-plane-ownership-verification-1.0",
        "status": "PASS",
        "checks_passed": len(checks),
        "production_checks": production["check_count"],
        "independent_checks": independent["checks_passed"],
        "catch_proofs": len(catch_rows),
        "source_count": len(manifest),
        "source_identity_sha256": source_identity,
        "initial_review_verdict": review_text.splitlines()[0].strip("`"),
        "corrected_review_verdict": corrected_verdict,
        "raw_stream_hashes": expected_stream_hashes,
        "maximum_conclusion": production["maximum_conclusion"],
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
