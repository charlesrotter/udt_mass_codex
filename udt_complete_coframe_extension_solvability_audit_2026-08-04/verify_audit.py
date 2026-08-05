#!/usr/bin/env python3
"""Fail-closed verifier and exercised catch-proofs for the extension/solvability audit."""

from __future__ import annotations

import copy
import argparse
import csv
import hashlib
import json
import subprocess
from pathlib import Path


PKG = Path(__file__).resolve().parent
ROOT = PKG.parent
BASE = "3af4d32718f08ddf83f760eda3faee243a7937ab"
OUTCOME = (
    "DERIVED_EXTENSION_EXISTENCE_AND_CARTAN_RECONSTRUCTION_ARE_NONSELECTING__"
    "CONDITIONAL_HOLONOMY_OBSTRUCTIONS_REQUIRE_EXTRA_PARALLELISM__"
    "NATIVE_INTERIOR_RETURN_REMAINS_OPEN"
)
OPERATION_STATUSES = {
    "E01": "KINEMATIC_DESCENT_NONSELECTION",
    "E02": "DERIVED_EXISTENCE_NONSELECTION",
    "E03": "CONDITIONAL_STRONG_WITNESS_NOT_REQUIRED",
    "E04": "CONDITIONAL_EXTRA_INTEGRABILITY_NOT_FRAME_NATURAL",
    "E05": "DERIVED_RECONSTRUCTION_NONSELECTION",
    "E06": "DERIVED_IDENTITY_NONSELECTION",
    "E07": "CONDITIONAL_PARALLELISM_SELECTOR",
    "E08": "CIRCULAR_PARENT_LAW_REQUIRED",
    "E09": "CIRCULAR_PARENT_BULK_AND_BOUNDARY_REQUIRED",
    "E10": "OPEN_OUTSIDE_FIXED_RANK_TILE",
}
HYPOTHESIS_RULINGS = {
    "H1": "REFUTED_IN_BOUNDED_SMOOTH_TILE",
    "H2": "SUPPORTED_DERIVED_BOUNDED",
    "H3": "SUPPORTED_CONDITIONAL_ONLY",
    "H4": "REFUTED_IN_POINTWISE_RECONSTRUCTION_AND_IDENTITY_CLASS",
    "H5": "TYPE_BLOCKED_CIRCULAR",
}


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def git_blob(path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{BASE}:{path}"], cwd=ROOT)


def validate(
    result: dict,
    independent: dict,
    operation_rows: list[dict[str, str]],
    hypothesis_rows: list[dict[str, str]],
    premise_rows: list[dict[str, str]],
    source_rows: list[dict[str, str]],
    operation_universe_rows: list[dict[str, str]],
) -> list[str]:
    checks = []

    assert result["outcome"] == OUTCOME, "outcome mismatch"
    checks.append("outcome_exact")
    assert result["sympy_version"] == "1.13.1", "SymPy version drift"
    checks.append("sympy_1_13_1")

    extension = result["extension_descent"]
    assert extension["seed_extension_dimension"] == 7, "seed extension dimension changed"
    assert extension["descent_map_rank"] == 7, "descent rank changed"
    assert extension["surviving_extension_dimension"] == 7, "surviving extension dimension changed"
    assert extension["selection_rank_from_descent"] == 0, "descent promoted to selector"
    assert extension["cocycle_h_exact"] and extension["cocycle_sigma_exact"], "cocycle broken"
    assert extension["positive_metric_preserved_all_charts"], "positive metric preservation failed"
    checks.append("extension_descent_exact_and_nonselecting")

    cartan = result["cartan_reconstruction"]
    assert cartan["connection_unknowns"] == 24 and cartan["torsion_equations"] == 24, "Cartan size drift"
    assert cartan["coefficient_rank"] == 24 and cartan["coefficient_nullity"] == 0, "Cartan rank drift"
    assert cartan["arbitrary_anholonomy_rhs_solvable"], "Cartan reconstruction lost"
    assert cartan["coframe_constraints_from_reconstruction"] == 0, "Cartan promoted to coframe equation"
    checks.append("cartan_reconstruction_full_rank_nonselection")

    coordinate = result["coordinate_integrability"]
    assert coordinate["metric_preserved_exact"], "frame rotation stopped preserving metric"
    assert coordinate["rotated_exterior_coefficients_at_x0"] == [1, 0], "frame-gauge witness changed"
    assert coordinate["rotated_coframe_not_closed"], "anholonomic witness lost"
    assert not coordinate["coordinate_integrability_is_frame_gauge_invariant"], "coordinate closure promoted"
    checks.append("coordinate_integrability_not_frame_invariant")

    monodromy = result["monodromy"]
    assert monodromy["matrix_count"] == 8, "monodromy count changed"
    assert monodromy["all_endpoint_graphs_dimension_two"], "endpoint graph dimension changed"
    assert monodromy["all_frozen_fixed_dimensions_match"], "fixed dimensions mismatch"
    assert monodromy["fixed_parallel_dimension_histogram"] == {"0": 4, "1": 3, "2": 1}, "fixed histogram changed"
    assert all(row["endpoint_graph_dimension"] == 2 for row in monodromy["rows"]), "endpoint/fixed conflation"
    checks.append("endpoint_matching_distinct_from_parallel_fixed_space")

    assert independent["extension_descent"]["descent_map_rank"] == extension["descent_map_rank"], "independent descent mismatch"
    assert independent["cartan_reconstruction"]["coefficient_rank"] == cartan["coefficient_rank"], "independent Cartan mismatch"
    assert independent["coordinate_integrability"] == coordinate, "independent coordinate witness mismatch"
    assert independent["monodromy"] == monodromy, "independent monodromy mismatch"
    checks.append("independent_replay_matches")

    operations = result["operations"]
    assert operations["operation_count"] == 10, "operation count changed"
    assert operations["native_complete_return_passes"] == 0, "native return silently promoted"
    assert operations["circular_parent_law_operations"] == 2, "circular dependency count changed"
    assert operations["conditional_extra_premise_operations"] == 3, "extra premise count changed"
    result_statuses = {row["operation_id"]: row["status"] for row in operations["records"]}
    assert result_statuses == OPERATION_STATUSES, "result operation statuses changed"
    assert not any(row["native_complete_return_pass"] for row in operations["records"]), "operation promoted"
    checks.append("operation_result_exact_no_native_pass")

    assert len(operation_rows) == 10, "operation ledger count changed"
    ledger_statuses = {row["operation_id"]: row["physical_ruling"] for row in operation_rows}
    assert ledger_statuses == OPERATION_STATUSES, "operation ledger status drift"
    by_id = {row["operation_id"]: row for row in operation_rows}
    assert by_id["E07"]["metric_native_status"] == "CONDITIONAL_EXTRA_PREMISE", "parallelism promoted"
    assert by_id["E08"]["parent_law_required"] == "YES", "bulk parent dependency deleted"
    assert by_id["E09"]["parent_law_required"] == "YES", "boundary parent dependency deleted"
    assert by_id["E10"]["physical_ruling"] == "OPEN_OUTSIDE_FIXED_RANK_TILE", "stratified class erased"
    checks.append("operation_ledger_semantic_guards")

    assert len(operation_universe_rows) == 10, "operation universe count changed"
    assert [row["operation_id"] for row in operation_universe_rows] == [f"E{i:02d}" for i in range(1, 11)], "operation universe IDs changed"
    universe_names = {row["operation_id"]: row["operation"] for row in operation_universe_rows}
    ledger_names = {row["operation_id"]: row["operation"] for row in operation_rows}
    assert universe_names == ledger_names, "operation universe/ledger mismatch"
    checks.append("operation_universe_10_exact")

    assert len(hypothesis_rows) == 5, "hypothesis count changed"
    assert {row["hypothesis_id"]: row["ruling"] for row in hypothesis_rows} == HYPOTHESIS_RULINGS, "hypothesis ruling drift"
    checks.append("hypothesis_rulings_exact")

    assert len(premise_rows) == 20, "premise count changed"
    premise = {row["premise_id"]: row["status"] for row in premise_rows}
    assert premise["P10"] == "CONDITIONAL_STRONG_WITNESS", "global coframe promoted"
    assert premise["P11"] == "NOT_FOUNDATIONAL", "coordinate coframe promoted"
    assert premise["P13"] == "CONDITIONAL_EXTRA_PREMISE", "parallelism premise promoted"
    assert premise["P14"] == "OPEN", "response/action promoted"
    assert premise["P16"] == "OPEN_OUTSIDE_SMOOTH_TILE", "rank-changing scope erased"
    assert premise["P18"] == "INACTIVE", "strong CSN reactivated"
    assert premise["P19"] == "POSIT_UNUSED", "carrier promoted"
    checks.append("premise_guards_exact")

    assert len(source_rows) == 27, "source count changed"
    assert [row["source_id"] for row in source_rows] == [f"S{i:02d}" for i in range(1, 28)], "source IDs changed"
    for row in source_rows:
        actual = hashlib.sha256(git_blob(row["path"])).hexdigest()
        assert actual == row["sha256"], f"source hash mismatch: {row['path']}"
    checks.append("base_source_hashes_27_exact")

    text = "\n".join(
        (PKG / name).read_text(encoding="utf-8")
        for name in ["EXACT_DERIVATION.md", "COMPLETENESS_MAP.md", "LAY_REPORT.md"]
    )
    for forbidden in [
        "NATIVE_ACTION_DERIVED",
        "NATIVE_SOURCE_DERIVED",
        "CARRIER_DERIVED",
        "PHYSICAL_BRANCH_SELECTED",
        "RANK_CHANGING_REJECTED",
        "STRONG_CSN_ACTIVE",
    ]:
        assert forbidden not in text, f"forbidden promotion: {forbidden}"
    checks.append("semantic_scope_guards")

    return checks


def expect_caught(mutation_id, description, mutate, baseline):
    args = copy.deepcopy(baseline)
    mutate(*args)
    try:
        validate(*args)
    except (AssertionError, KeyError) as exc:
        return {"mutation_id": mutation_id, "description": description, "status": "CAUGHT", "reason": str(exc)}
    raise AssertionError(f"mutation escaped: {mutation_id} {description}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true", help="verify without changing VERIFICATION_RESULT.json")
    args = parser.parse_args()
    result = json.loads((PKG / "RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((PKG / "INDEPENDENT_RESULT.json").read_text(encoding="utf-8"))
    fresh_result = json.loads(
        subprocess.check_output(
            ["python3", str(PKG / "derive_extension_solvability.py"), "--no-write"],
            cwd=ROOT,
            text=True,
        )
    )
    fresh_independent = json.loads(
        subprocess.check_output(
            ["python3", str(PKG / "independent_extension_solvability.py"), "--no-write"],
            cwd=ROOT,
            text=True,
        )
    )
    assert fresh_result == result, "fresh production replay mismatch"
    assert fresh_independent == independent, "fresh independent replay mismatch"
    operation_rows = read_tsv(PKG / "OPERATION_LEDGER.tsv")
    hypothesis_rows = read_tsv(PKG / "HYPOTHESIS_LEDGER.tsv")
    premise_rows = read_tsv(PKG / "PREMISE_LEDGER.tsv")
    source_rows = read_tsv(PKG / "SOURCE_ADJUDICATION.tsv")
    operation_universe_rows = read_tsv(PKG / "OPERATION_UNIVERSE.tsv")
    baseline = (result, independent, operation_rows, hypothesis_rows, premise_rows, source_rows, operation_universe_rows)
    checks = validate(*baseline)
    checks.append("fresh_primary_and_independent_replays_match_saved_artifacts")

    mutations = [
        ("M01", "wrong outcome", lambda r, *_: r.update(outcome="CLOSED")),
        ("M02", "descent rank reduced", lambda r, *_: r["extension_descent"].update(descent_map_rank=6)),
        ("M03", "cocycle broken", lambda r, *_: r["extension_descent"].update(cocycle_h_exact=False)),
        ("M04", "Cartan rank reduced", lambda r, *_: r["cartan_reconstruction"].update(coefficient_rank=23)),
        ("M05", "Cartan promoted to coframe equation", lambda r, *_: r["cartan_reconstruction"].update(coframe_constraints_from_reconstruction=1)),
        ("M06", "coordinate integrability promoted", lambda r, *_: r["coordinate_integrability"].update(coordinate_integrability_is_frame_gauge_invariant=True)),
        ("M07", "endpoint graph conflated with fixed space", lambda r, *_: r["monodromy"]["rows"][1].update(endpoint_graph_dimension=0)),
        ("M08", "native return silently added", lambda r, *_: r["operations"].update(native_complete_return_passes=1)),
        ("M09", "parallelism promoted", lambda r, i, o, h, p, s, u: next(row for row in o if row["operation_id"] == "E07").update(metric_native_status="DERIVED")),
        ("M10", "bulk parent dependency deleted", lambda r, i, o, h, p, s, u: next(row for row in o if row["operation_id"] == "E08").update(parent_law_required="NO")),
        ("M11", "boundary parent dependency deleted", lambda r, i, o, h, p, s, u: next(row for row in o if row["operation_id"] == "E09").update(parent_law_required="NO")),
        ("M12", "rank-changing class closed", lambda r, i, o, h, p, s, u: next(row for row in o if row["operation_id"] == "E10").update(physical_ruling="DERIVED_RETURN")),
        ("M13", "global coframe promoted", lambda r, i, o, h, p, s, u: next(row for row in p if row["premise_id"] == "P10").update(status="DERIVED")),
        ("M14", "strong CSN reactivated", lambda r, i, o, h, p, s, u: next(row for row in p if row["premise_id"] == "P18").update(status="ACTIVE")),
        ("M15", "conditional holonomy made unconditional", lambda r, i, o, h, p, s, u: next(row for row in h if row["hypothesis_id"] == "H3").update(ruling="SUPPORTED_DERIVED_UNCONDITIONAL")),
        ("M16", "source hash corrupted", lambda r, i, o, h, p, s, u: s[0].update(sha256="0" * 64)),
        ("M17", "operation universe member deleted", lambda r, i, o, h, p, s, u: u.pop()),
    ]
    catches = [expect_caught(mid, description, mutate, baseline) for mid, description, mutate in mutations]
    verification = {
        "schema": "udt.complete_coframe_extension_solvability.verification.v1",
        "status": "PASS",
        "checks_passed": len(checks),
        "checks": checks,
        "mutations_caught": len(catches),
        "catch_proofs": catches,
        "source_adjudication_sha256": hashlib.sha256((PKG / "SOURCE_ADJUDICATION.tsv").read_bytes()).hexdigest(),
    }
    if not args.no_write:
        (PKG / "VERIFICATION_RESULT.json").write_text(json.dumps(verification, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(verification, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
