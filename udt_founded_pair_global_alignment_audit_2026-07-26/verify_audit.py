#!/usr/bin/env python3
"""Fail-closed verifier for the founded-pair global-alignment audit."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def exact_ids(values: list[dict[str, str]], key: str, expected: set[str]) -> None:
    actual = [row[key] for row in values]
    if len(actual) != len(set(actual)) or set(actual) != expected:
        raise AssertionError(f"identity coverage: {key}")


def validate_sources(corrupt: bool = False) -> None:
    scope = rows("SOURCE_SCOPE.tsv")
    manifest = rows("SOURCE_MANIFEST.tsv")
    if [row["path"] for row in scope] != [row["path"] for row in manifest]:
        raise AssertionError("source order")
    for index, row in enumerate(manifest):
        expected_sha = "0" * 64 if corrupt and index == 0 else row["sha256"]
        path = ROOT / row["path"]
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected_sha:
            raise AssertionError("source sha")
        if path.stat().st_size != int(row["bytes"]):
            raise AssertionError("source size")


def validate_model(
    routes: list[dict[str, str]],
    classes: list[dict[str, str]],
    sources: list[dict[str, str]],
    status: list[dict[str, str]],
    production: dict,
    independent: dict,
) -> None:
    exact_ids(routes, "route_id", {f"R{i:02d}" for i in range(1, 11)})
    exact_ids(classes, "class_id", {f"E{i:02d}" for i in range(1, 13)})
    if len(sources) != 12 or len({row["source"] for row in sources}) != 12:
        raise AssertionError("source precedence coverage")
    if len(status) != 13 or len({row["object"] for row in status}) != 13:
        raise AssertionError("status coverage")

    route = {row["route_id"]: row for row in routes}
    extension = {row["class_id"]: row for row in classes}
    state = {row["object"]: row for row in status}

    if route["R01"]["outcome"] != "SUPPORTED" or state["Local_physical_clock_ruler_alignment"]["status"] != "DERIVED_CONDITIONAL":
        raise AssertionError("local alignment lost")
    if route["R02"]["outcome"] != "REJECTED_IN_CURRENT_PRECEDENCE":
        raise AssertionError("older source precedence restored")
    if not any(row["source"].startswith("udt_mixed_readout_anchor") and row["current_ruling"] == "SUPERSEDED_FOR_LOCAL_PAIR_STATUS" for row in sources):
        raise AssertionError("source precedence")
    if route["R03"]["outcome"] != "REJECTED" or route["R04"]["outcome"] != "SUPPORTED":
        raise AssertionError("basis and mixed pair conflated")
    if state["Mixed_fixed_operator_readout"]["status"] != "COUNTERFACTUAL_NOT_ACTIVE":
        raise AssertionError("mixed pair promoted")
    if extension["E04"]["status"] != "DERIVED_CLASSIFICATION" or "exact_pair_restriction" not in extension["E04"]["meaning"]:
        raise AssertionError("complete cross terms changed pair")
    if extension["E06"]["status"] != "DERIVED_CLASSIFICATION" or "H_direct_sum_D" not in extension["E06"]["exact_form"]:
        raise AssertionError("invariant pair extension mixed")
    if extension["E09"]["status"] != "DERIVED_COUNTERCLASS" or "pair_is_not_invariant" not in extension["E09"]["meaning"]:
        raise AssertionError("compression promoted")
    if extension["E10"]["status"] != "REQUIRES_C_ZERO_FOR_EXACT_PAIR_METRIC":
        raise AssertionError("lower shift promoted")
    if state["Global_pair_subbundle"]["status"] != "OPEN" or route["R08"]["outcome"] != "REJECTED":
        raise AssertionError("global promotion")
    if state["Screen_response"]["status"] != "OPEN" or route["R10"]["outcome"] != "REJECTED":
        raise AssertionError("screen selected")
    if state["Physical_reciprocal_line_exchange"]["status"] != "REJECTED_IN_ALIGNED_READOUT":
        raise AssertionError("causal exchange promoted")
    if state["Action_source_carrier_boundary_density_bootstrap_mass_dynamics"]["status"] != "OPEN":
        raise AssertionError("physics imported")

    required_production = {
        "metric_only_transform_changes_metric_operator_pair",
        "fixed_operator_self_adjoint_iff_pair_offdiagonal_zero",
        "invariant_self_adjoint_extension_is_block_diagonal",
        "pair_restriction_independent_of_lambda",
        "cross_witness_pair_restriction_still_exact",
        "causal_norm_preservation_obstructs_physical_line_exchange",
    }
    if production.get("result") != "PASS" or production.get("check_count") != 50:
        raise AssertionError("production result")
    if not required_production.issubset(production["checks"]) or set(production["checks"].values()) != {"PASS"}:
        raise AssertionError("production checks")
    counts = independent.get("counts", {})
    if independent.get("result") != "PASS" or independent.get("summary_check_count") != 18:
        raise AssertionError("independent result")
    if (counts.get("bounded_pair_self_adjoint_Lorentzian"), counts.get("bounded_pair_nonself_adjoint_Lorentzian")) != (18, 238):
        raise AssertionError("pair census")
    if (counts.get("lower_shift_blocks_tested"), counts.get("lower_shift_pair_metric_preserving")) != (81, 1):
        raise AssertionError("lower shift census")
    if (counts.get("self_adjoint_compression_blocks_tested"), counts.get("pair_invariant_compression_blocks")) != (81, 1):
        raise AssertionError("compression census")
    if (counts.get("small_symmetric_screen_responses_tested"), counts.get("screen_rotation_equivariant_responses")) != (27, 3):
        raise AssertionError("screen census")


def expect_failure(callback) -> str:
    try:
        callback()
    except (AssertionError, KeyError):
        return "PASS"
    raise AssertionError("catch accepted corruption")


def main() -> None:
    exact_ids(rows("ROUTE_UNIVERSE.tsv"), "route_id", {f"R{i:02d}" for i in range(1, 11)})
    routes = rows("ROUTE_OUTCOMES.tsv")
    classes = rows("EXTENSION_CLASSIFICATION.tsv")
    sources = rows("SOURCE_PRECEDENCE.tsv")
    status = rows("STATUS_LEDGER.tsv")
    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text())
    validate_model(routes, classes, sources, status, production, independent)
    validate_sources()

    def changed_row(table, key, identity, field, value):
        changed = copy.deepcopy(table)
        next(row for row in changed if row[key] == identity)[field] = value
        return changed

    catches: dict[str, str] = {}
    bad_sources = copy.deepcopy(sources)
    target = next(row for row in bad_sources if row["source"].startswith("udt_mixed_readout_anchor") and row["current_ruling"] == "SUPERSEDED_FOR_LOCAL_PAIR_STATUS")
    target["current_ruling"] = "CONTROLLING"
    catches["source_precedence"] = expect_failure(lambda: validate_model(routes, classes, bad_sources, status, production, independent))

    bad_production = copy.deepcopy(production)
    del bad_production["checks"]["metric_only_transform_changes_metric_operator_pair"]
    catches["metric_only_basis_change"] = expect_failure(lambda: validate_model(routes, classes, sources, status, bad_production, independent))

    bad_production = copy.deepcopy(production)
    del bad_production["checks"]["fixed_operator_self_adjoint_iff_pair_offdiagonal_zero"]
    catches["pair_offdiagonal"] = expect_failure(lambda: validate_model(routes, classes, sources, status, bad_production, independent))

    bad_classes = changed_row(classes, "class_id", "E09", "status", "DERIVED_INVARIANT_EXTENSION")
    catches["compression_as_invariance"] = expect_failure(lambda: validate_model(routes, bad_classes, sources, status, production, independent))

    bad_classes = changed_row(classes, "class_id", "E06", "exact_form", "H_with_nonzero_mixing")
    catches["invariant_pair_mixing"] = expect_failure(lambda: validate_model(routes, bad_classes, sources, status, production, independent))

    bad_production = copy.deepcopy(production)
    del bad_production["checks"]["invariant_self_adjoint_extension_is_block_diagonal"]
    catches["orthogonal_complement"] = expect_failure(lambda: validate_model(routes, classes, sources, status, bad_production, independent))

    bad_status = changed_row(status, "object", "Global_pair_subbundle", "status", "DERIVED")
    catches["global_promotion"] = expect_failure(lambda: validate_model(routes, classes, sources, bad_status, production, independent))

    bad_status = changed_row(status, "object", "Screen_response", "status", "DERIVED_LAMBDA_ZERO")
    catches["lambda_selection"] = expect_failure(lambda: validate_model(routes, classes, sources, bad_status, production, independent))

    bad_classes = changed_row(classes, "class_id", "E04", "meaning", "Cross_terms_change_intrinsic_pair_metric")
    catches["cross_term_pair_change"] = expect_failure(lambda: validate_model(routes, bad_classes, sources, status, production, independent))

    bad_status = changed_row(status, "object", "Physical_reciprocal_line_exchange", "status", "DERIVED_ISOMETRY")
    catches["causal_line_exchange"] = expect_failure(lambda: validate_model(routes, classes, sources, bad_status, production, independent))

    catches["missing_route"] = expect_failure(lambda: validate_model(routes[:-1], classes, sources, status, production, independent))
    catches["duplicate_class"] = expect_failure(lambda: validate_model(routes, classes + [copy.deepcopy(classes[0])], sources, status, production, independent))
    catches["source_identity"] = expect_failure(lambda: validate_sources(True))

    if len(catches) != 13 or set(catches.values()) != {"PASS"}:
        raise AssertionError("catch proof count")

    output = {
        "schema": "udt-founded-pair-global-alignment-verification-1.0",
        "result": "PASS",
        "grade": "VERIFIED_WITH_CAVEATS_BOUNDED_LOCAL_AUTHORITY_AND_EXTENSION_CLASS",
        "routes": len(routes),
        "extension_classes": len(classes),
        "source_precedence_rows": len(sources),
        "status_rows": len(status),
        "production_checks": production["check_count"],
        "independent_summary_checks": independent["summary_check_count"],
        "independent_counts": independent["counts"],
        "source_identities": len(rows("SOURCE_MANIFEST.tsv")),
        "catch_count": len(catches),
        "catch_proofs": catches,
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
