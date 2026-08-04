#!/usr/bin/env python3
"""Fail-closed verifier for the extension-bundle globalization audit."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PACKAGE_PREFIX = HERE.name + "/"

FAMILY_IDS = {f"F{i:02d}" for i in range(1, 8)}
OBSTRUCTION_IDS = {f"B{i:02d}" for i in range(1, 15)}
ARCHITECTURE_IDS = {f"A{i:02d}" for i in range(1, 4)}
VARIATION_IDS = {f"V{i:02d}" for i in range(1, 19)}
IDENTITY_IDS = {f"I{i:02d}" for i in range(1, 16)}
REPAIR_IDS = {f"R{i:02d}" for i in range(1, 7)}
VARIATION_ROLES = {
    "PRESENTATION_GAUGE",
    "LOCAL_CONFIGURATION_TANGENT",
    "RECIPROCAL_ASSIGNMENT_TANGENT_OPEN",
    "TRANSITION_OR_GLOBAL_MODULUS_TANGENT",
    "BOUNDARY_CONFIGURATION_TANGENT",
    "DISCRETE_SECTOR_CHANGE_NOT_TANGENT",
    "OBSERVER_QUERY_NOT_FIELD_VARIATION",
    "CONDITIONAL_ACTION_VARIATION_ONLY",
    "BLOCKED_UNTYPED",
}


def table(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob(path: str) -> str:
    return subprocess.check_output(["git", "rev-parse", f"HEAD:{path}"], cwd=ROOT, text=True).strip()


def unique_exact(rows: list[dict[str, str]], field: str, expected: set[str]) -> None:
    values = [row[field] for row in rows]
    assert len(values) == len(set(values)), f"duplicate {field}"
    assert set(values) == expected, f"{field} coverage mismatch"


def validate_sources(rows: list[dict[str, str]], field: str, manifest_paths: set[str]) -> None:
    for row in rows:
        source = row[field]
        assert (ROOT / source).is_file(), f"missing source: {source}"
        if not source.startswith(PACKAGE_PREFIX):
            assert source in manifest_paths, f"unmanifested external source: {source}"


def validate_families(rows, manifest_paths):
    unique_exact(rows, "family_id", FAMILY_IDS)
    validate_sources(rows, "controlling_source", manifest_paths)
    by = {row["family_id"]: row for row in rows}
    assert by["F01"]["status"] == "OPEN_RETAINED_CLASS"
    assert by["F02"]["status"] == "QUERY_BUNDLE_DERIVED__FIELD_SECTION_OPEN"
    assert by["F02"]["section_required"] == "query container no; realized field yes"
    assert by["F03"]["status"] == "ABSTRACT_Z2_GRADED_COCYCLE_DERIVED__PHYSICAL_METRIC_LIFT_CONDITIONAL"
    assert "noncontractible loop monodromy may be odd" in by["F03"]["transition_rule"]
    assert by["F04"]["status"] == "GLOBAL_SCREEN_METRIC_AND_MIXING_SECTIONS_AVAILABLE__GLOBAL_SCREEN_FRAME_NOT_REQUIRED"
    assert "sigma_j=Q_ij sigma_i P_ij_minus1" in by["F04"]["transition_rule"]
    assert by["F05"]["status"] == "DERIVED_EXISTENCE_WITNESS_NOT_PARENT_REQUIREMENT"
    assert by["F06"]["status"] == "CONDITIONAL_EXTRA_RESTRICTION_NOT_REQUIRED_FOR_BUNDLE"
    assert by["F07"]["status"] == "OPEN_RETAINED_OUTSIDE_SMOOTH_BUNDLE_TILE"


def validate_obstructions(rows, manifest_paths):
    unique_exact(rows, "obstruction_id", OBSTRUCTION_IDS)
    validate_sources(rows, "controlling_source", manifest_paths)
    by = {row["obstruction_id"]: row for row in rows}
    assert by["B02"]["status"] == "OPEN_TOPOLOGICAL_AND_PHYSICAL_REDUCTION"
    assert by["B03"]["status"] == "DERIVED_CONTRACTIBLE_LOCAL_FIBER"
    assert by["B04"]["status"] == "DERIVED_NO_ADDITIONAL_EXISTENCE_OBSTRUCTION"
    assert by["B04"]["what_is_not_required"] == "a global screen frame"
    assert by["B05"]["status"] == "DERIVED_NO_ADDITIONAL_EXISTENCE_OBSTRUCTION"
    assert by["B05"]["object_or_join"] == "mixing bundle Hom(N,Q)"
    assert by["B05"]["what_is_not_required"] == "physical zero mixing or a preferred nonzero section"
    assert by["B06"]["status"] == "LOCAL_REPRESENTATIVE_ONLY"
    assert by["B07"]["status"] == "CONDITIONAL_STRONG_WITNESS"
    assert by["B08"]["status"] == "OPEN_ASSIGNMENT"
    assert by["B10"]["status"] == "CONDITIONAL_PHYSICAL_LIFT"
    assert by["B11"]["status"] == "NOT_REQUIRED__BRANCH_CONDITIONAL"
    assert by["B12"]["status"] == "OPEN_GLOBAL_COMPLETION"
    assert by["B13"]["status"] == "OPEN_ONTOLOGY_FORK"
    assert by["B14"]["status"] == "OPEN_UNCHANGED"


def validate_architectures(rows, manifest_paths):
    unique_exact(rows, "architecture_id", ARCHITECTURE_IDS)
    validate_sources(rows, "controlling_source", manifest_paths)
    by = {row["architecture_id"]: row for row in rows}
    assert by["A01"]["status"] == "AVAILABLE_TYPE_CORRECT_NOT_SELECTED"
    assert "not field variations" in by["A01"]["variation_domain"]
    assert by["A02"]["status"] == "CONDITIONAL_GLOBAL_SECTION_AND_OWNERSHIP_OPEN"
    assert by["A03"]["status"] == "AVAILABLE_ON_BOUNDED_BRANCHES_NOT_UNIVERSAL"


def validate_variations(rows, manifest_paths):
    unique_exact(rows, "variation_id", VARIATION_IDS)
    validate_sources(rows, "controlling_source", manifest_paths)
    assert {row["role"] for row in rows} <= VARIATION_ROLES
    by = {row["variation_id"]: row for row in rows}
    assert by["V03"]["role"] == "PRESENTATION_GAUGE"
    assert by["V04"]["role"] == by["V05"]["role"] == "LOCAL_CONFIGURATION_TANGENT"
    assert by["V04"]["gauge_or_physical_note"] == "not three propagating modes"
    assert by["V05"]["gauge_or_physical_note"] == "not four propagating modes"
    assert by["V06"]["status"] == "OPEN_PHYSICAL_ASSIGNMENT"
    assert by["V07"]["role"] == "OBSERVER_QUERY_NOT_FIELD_VARIATION"
    assert by["V08"]["status"] == "CONDITIONAL_UNTYPED_PHYSICAL"
    assert by["V12"]["role"] == "DISCRETE_SECTOR_CHANGE_NOT_TANGENT"
    assert by["V13"]["role"] == "BOUNDARY_CONFIGURATION_TANGENT"
    assert by["V15"]["status"] == "CONDITIONAL_NOT_NATIVE"
    assert by["V16"]["status"] == "CONDITIONAL_CARRIER_BRANCH"
    assert by["V17"]["status"] == "AMBIENT_TANGENT__NOT_FIXED_RANK_TILE_TANGENT"
    assert by["V18"]["status"] == "OPEN_NOT_ACTIVATED"


def validate_identities(rows, manifest_paths):
    unique_exact(rows, "identity_id", IDENTITY_IDS)
    validate_sources(rows, "controlling_source", manifest_paths)
    by = {row["identity_id"]: row for row in rows}
    assert by["I01"]["identity"] == "E_j=L_ij E_i R_ij_inverse"
    assert by["I02"]["status"] == "DERIVED_ALGEBRAIC"
    assert by["I03"]["status"] == "DERIVED_EXACT"
    assert by["I04"]["identity"] == "e_j=ell_ij+Ad(L_ij)e_i-Ad(E_j)r_ij"
    assert by["I05"]["status"] == by["I06"]["status"] == "DERIVED_EXACT"
    assert by["I08"]["what_it_does_not_supply"] == "ordinary Lorentz transport or physical seam"
    assert by["I09"]["identity"] == "reciprocal_transition_product_required_to_equal_identity_has_even_F_parity_while_noncontractible_loop_monodromy_may_be_odd"
    assert by["I11"]["status"] == "DERIVED_STANDARD_BUNDLE_FACT"
    assert by["I12"]["status"] == "DERIVED_STANDARD_BUNDLE_FACT"
    assert by["I12"]["identity"] == "zero_is_a_global_section_of_Hom_N_Q"
    assert by["I13"]["identity"] == "dphi_to_minus_dphi_leaves_s_phi_and_P_phi_invariant"
    assert by["I15"]["status"] == "DERIVED_NEGATIVE_SCOPE"


def validate_current_premises(rows):
    by = {row["premise_id"]: row for row in rows}
    assert by["G01"]["current_status"] == "DERIVED_ADDITIVE_LOG_DEPTH_OF_RECIPROCAL_PAIR"
    assert by["G04"]["current_status"] == "CHALLENGED_OWNER_POSTULATE_NOT_DERIVED"
    assert by["G04"]["active_use"] == "INACTIVE_UNLESS_CHARLES_EXPLICITLY_REAUTHORIZES"
    assert by["G09"]["current_status"] == "POSIT"
    assert by["G16"]["current_status"] == "OPEN"


def validate_manifest() -> set[str]:
    rows = table(HERE / "SOURCE_MANIFEST.tsv")
    listed = [line.strip() for line in (HERE / "SOURCE_PATHS.txt").read_text().splitlines() if line.strip()]
    assert len(listed) == len(set(listed)) == 24
    assert [row["path"] for row in rows] == listed
    for row in rows:
        path = ROOT / row["path"]
        assert path.is_file()
        assert str(path.stat().st_size) == row["bytes"]
        assert sha(path) == row["sha256"]
        assert git_blob(row["path"]) == row["git_blob"]
    return set(listed)


def validate_algebra_results():
    production = json.loads((HERE / "TRANSITION_VARIATION_RESULT.json").read_text())
    independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text())
    pin = (HERE / "requirements.txt").read_text().strip().split("==", 1)[1]
    assert production["status"] == "PASS" and production["check_count"] == 26
    assert len(production["checks"]) == 26 and set(production["checks"].values()) == {"PASS"}
    assert production["sympy_version"] == pin
    assert independent["status"] == "PASS" and independent["check_count"] == 16
    assert len(independent["checks"]) == 16 and set(independent["checks"].values()) == {"PASS"}
    assert independent["production_imported"] is False and independent["third_party_packages"] == []


def validate_review_gate(review_text: str, repairs, replay_text: str | None, final: bool):
    verdict = next((line.strip() for line in review_text.splitlines() if line.strip()), "")
    assert verdict in {"ACCEPT", "ACCEPT_WITH_REQUIRED_REPAIRS"}, f"invalid review verdict: {verdict}"
    unique_exact(repairs, "repair_id", REPAIR_IDS)
    if verdict == "ACCEPT_WITH_REQUIRED_REPAIRS":
        if final:
            assert {row["status"] for row in repairs} == {"CLOSED"}
            assert replay_text is not None
            replay_verdict = next((line.strip() for line in replay_text.splitlines() if line.strip()), "")
            assert replay_verdict == "REPAIRS_ACCEPTED"
        else:
            assert {row["status"] for row in repairs} <= {"APPLIED_PENDING_REPLAY", "CLOSED"}


def catch_proofs(families, obstructions, architectures, variations, identities, premises, repairs, review_text, manifest_paths):
    result = {}

    def must_fail(name, fn):
        try:
            fn()
        except (AssertionError, KeyError, ValueError):
            result[name] = "PASS"
        else:
            raise AssertionError(f"catch proof did not fail: {name}")

    must_fail("missing_transition_family", lambda: validate_families(families[:-1], manifest_paths))
    bad = [dict(row) for row in families]
    next(row for row in bad if row["family_id"] == "F05")["status"] = "PARENT_REQUIREMENT"
    must_fail("hidden_global_coframe", lambda: validate_families(bad, manifest_paths))
    bad = [dict(row) for row in obstructions]
    next(row for row in bad if row["obstruction_id"] == "B05")["what_is_not_required"] = "nonzero mixing"
    must_fail("forced_zero_mixing", lambda: validate_obstructions(bad, manifest_paths))
    bad = [dict(row) for row in identities]
    next(row for row in bad if row["identity_id"] == "I13")["identity"] = "dphi_sign_changes_projector"
    must_fail("channel_reversal_sign_failure", lambda: validate_identities(bad, manifest_paths))
    bad = [dict(row) for row in identities]
    next(row for row in bad if row["identity_id"] == "I02")["status"] = "OPEN"
    must_fail("cocycle_failure", lambda: validate_identities(bad, manifest_paths))
    bad = [dict(row) for row in variations]
    next(row for row in bad if row["variation_id"] == "V03")["role"] = "LOCAL_CONFIGURATION_TANGENT"
    must_fail("gauge_counted_physical", lambda: validate_variations(bad, manifest_paths))
    bad = [dict(row) for row in variations]
    next(row for row in bad if row["variation_id"] == "V12")["role"] = "LOCAL_CONFIGURATION_TANGENT"
    must_fail("topology_change_treated_as_tangent", lambda: validate_variations(bad, manifest_paths))
    bad = [dict(row) for row in variations]
    next(row for row in bad if row["variation_id"] == "V15")["status"] = "NATIVE_DERIVED"
    must_fail("conditional_action_promoted", lambda: validate_variations(bad, manifest_paths))
    bad = [dict(row) for row in obstructions]
    next(row for row in bad if row["obstruction_id"] == "B02")["status"] = "DERIVED_GLOBAL_FIELD"
    must_fail("invented_global_reciprocal_section", lambda: validate_obstructions(bad, manifest_paths))
    bad = [dict(row) for row in variations]
    next(row for row in bad if row["variation_id"] == "V07")["role"] = "LOCAL_CONFIGURATION_TANGENT"
    must_fail("query_direction_promoted_to_field", lambda: validate_variations(bad, manifest_paths))
    bad = [dict(row) for row in families]
    next(row for row in bad if row["family_id"] == "F07")["status"] = "REJECTED"
    must_fail("rank_changing_stratum_discarded", lambda: validate_families(bad, manifest_paths))
    bad = [dict(row) for row in obstructions]
    next(row for row in bad if row["obstruction_id"] == "B08")["status"] = "DERIVED_GLOBAL_SCALAR"
    must_fail("global_phi_invented", lambda: validate_obstructions(bad, manifest_paths))
    bad = [dict(row) for row in variations]
    next(row for row in bad if row["variation_id"] == "V04")["gauge_or_physical_note"] = "three propagating modes"
    must_fail("chart_tangents_promoted_to_modes", lambda: validate_variations(bad, manifest_paths))
    bad = [dict(row) for row in premises]
    next(row for row in bad if row["premise_id"] == "G04")["active_use"] = "ACTIVE"
    must_fail("strong_CSN_reactivated", lambda: validate_current_premises(bad))
    bad = [dict(row) for row in premises]
    next(row for row in bad if row["premise_id"] == "G09")["current_status"] = "DERIVED"
    must_fail("S2_carrier_promoted", lambda: validate_current_premises(bad))
    must_fail(
        "review_verdict_substring_false_accept",
        lambda: validate_review_gate("REJECT\nThe word ACCEPT appears only in discussion.\n", repairs, None, False),
    )
    bad_repairs = [dict(row) for row in repairs]
    bad_repairs[0]["status"] = "APPLIED_PENDING_REPLAY"
    must_fail(
        "required_repairs_not_closed",
        lambda: validate_review_gate(review_text, bad_repairs, "REPAIRS_ACCEPTED\n", True),
    )
    must_fail(
        "missing_repair_row",
        lambda: validate_review_gate(review_text, repairs[:-1], None, False),
    )
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pre-review", action="store_true")
    args = parser.parse_args()

    required = [
        "PREREGISTRATION.md", "EXACT_DERIVATION.md", "GLOBALIZATION_ARCHITECTURE.md",
        "COMPLETENESS_MAP.md", "AUDIT_REPORT.md", "TRANSITION_FAMILY_LEDGER.tsv",
        "BUNDLE_OBSTRUCTION_LEDGER.tsv", "ONTOLOGY_FORK.tsv", "VARIATION_DOMAIN_LEDGER.tsv",
        "COCYCLE_AND_VARIATION_IDENTITIES.tsv", "SOURCE_MANIFEST.tsv",
        "TRANSITION_VARIATION_RESULT.json", "INDEPENDENT_RESULT.json", "REVIEW_DISPATCH.md",
        "REPOSITORY_GATES.json", "REPOSITORY_TEST_STDOUT.txt", "UNRELATED_UNTRACKED_METADATA.tsv",
        "RUN_ENVIRONMENT.json", "COMMANDS.txt",
        "FRESH_ADVERSARIAL_REVIEW.md", "REVIEW_REPAIR_CLOSURE.tsv",
        "ADVERSARIAL_REVIEW_CORRECTION.md",
        "FRESH_ADVERSARIAL_REVIEW_RAW.md", "REPAIR_REPLAY_RAW.md",
        "SOURCE_PATHS.txt", "requirements.txt", "build_source_manifest.py",
        "derive_transition_variation.py", "verify_transition_variation_independent.py",
        "record_environment.py", "verify_repository_gates.py", "verify_audit.py",
    ]
    if not args.pre_review:
        required.append("REPAIR_REPLAY.md")
    for name in required:
        assert (HERE / name).is_file(), f"missing deliverable: {name}"

    report = (HERE / "AUDIT_REPORT.md").read_text()
    review_text = (HERE / "FRESH_ADVERSARIAL_REVIEW.md").read_text()
    repairs = table(HERE / "REVIEW_REPAIR_CLOSURE.tsv")
    if args.pre_review:
        assert "PRELIMINARY_REPAIRS_PENDING_REPLAY" in report
        validate_review_gate(review_text, repairs, None, False)
    else:
        assert "PRELIMINARY_REPAIRS_PENDING_REPLAY" not in report
        validate_review_gate(review_text, repairs, (HERE / "REPAIR_REPLAY.md").read_text(), True)

    manifest_paths = validate_manifest()
    families = table(HERE / "TRANSITION_FAMILY_LEDGER.tsv")
    obstructions = table(HERE / "BUNDLE_OBSTRUCTION_LEDGER.tsv")
    architectures = table(HERE / "ONTOLOGY_FORK.tsv")
    variations = table(HERE / "VARIATION_DOMAIN_LEDGER.tsv")
    identities = table(HERE / "COCYCLE_AND_VARIATION_IDENTITIES.tsv")
    premises = table(ROOT / "CURRENT_SCIENTIFIC_PREMISES.tsv")
    validate_families(families, manifest_paths)
    validate_obstructions(obstructions, manifest_paths)
    validate_architectures(architectures, manifest_paths)
    validate_variations(variations, manifest_paths)
    validate_identities(identities, manifest_paths)
    validate_current_premises(premises)
    validate_algebra_results()
    catches = catch_proofs(families, obstructions, architectures, variations, identities, premises, repairs, review_text, manifest_paths)

    result = {
        "schema": "udt-extension-bundle-globalization-verification-1.0",
        "status": "PASS_PRE_REVIEW" if args.pre_review else "PASS",
        "transition_families": len(families),
        "obstruction_rows": len(obstructions),
        "ontology_architectures": len(architectures),
        "variation_rows": len(variations),
        "identity_rows": len(identities),
        "source_manifest_rows": len(manifest_paths),
        "production_symbolic_checks": 26,
        "independent_rational_checks": 16,
        "catch_proofs": catches,
        "deliverable_sha256": {name: sha(HERE / name) for name in required},
        "maximum_conclusion": "BOUNDED_EQUIVARIANT_EXTENSION_BUNDLE_AND_VARIATION_TYPE_CLASSIFICATION_ONLY",
    }
    output = "PRE_REVIEW_VERIFICATION_RESULT.json" if args.pre_review else "VERIFICATION_RESULT.json"
    (HERE / output).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
