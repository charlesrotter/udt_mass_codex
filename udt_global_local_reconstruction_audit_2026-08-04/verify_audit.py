#!/usr/bin/env python3
"""Fail-closed verifier for the global/local reconstruction audit."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
OUTCOME = (
    "DERIVED_PARTIAL_KINEMATIC_ADMISSIBILITY_CORRESPONDENCE__"
    "WORKING_POSIT_REQUIRES_BUT_DOES_NOT_DERIVE_COMPLETE_RETURN"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def run_json(path: Path) -> dict[str, object]:
    completed = subprocess.run(
        ["python3", str(path)], cwd=REPO, check=True, capture_output=True, text=True
    )
    if completed.stderr:
        raise AssertionError(f"unexpected stderr from {path.name}: {completed.stderr}")
    return json.loads(completed.stdout)


def validate(package: Path) -> list[str]:
    checks: list[str] = []

    result = json.loads((package / "RESULT.json").read_text(encoding="utf-8"))
    independent_saved = json.loads((package / "INDEPENDENT_RESULT.json").read_text(encoding="utf-8"))
    if result["outcome"] != OUTCOME:
        raise AssertionError("outcome mismatch")
    checks.append("result_outcome_exact")
    if result["status"] not in {"PASS_PENDING_SEMANTIC_REVIEW", "PASS_WITH_CAVEATS"}:
        raise AssertionError("invalid result status")
    checks.append("result_status_bounded")

    production = run_json(package / "derive_reconstruction.py")
    independent = run_json(package / "independent_reconstruction.py")
    if production["outcome"] != OUTCOME:
        raise AssertionError("production outcome mismatch")
    checks.append("production_outcome_exact")
    if production["sympy_version"] != "1.13.1":
        raise AssertionError("unpinned SymPy version")
    checks.append("sympy_1_13_1")

    prod_cover = production["cover_reconstruction"]
    ind_cover = independent["cover_reconstruction"]
    for key in (
        "cover_a_descent_dimension",
        "cover_b_descent_dimension",
        "descent_plus_readout_graph_rank",
        "descent_plus_readout_graph_nullity",
        "global_configuration_dimension",
        "refinement_reconstructs_same_global_data",
    ):
        if prod_cover[key] != ind_cover[key]:
            raise AssertionError(f"cover disagreement: {key}")
    if [prod_cover[key] for key in ("cover_a_descent_dimension", "cover_b_descent_dimension", "descent_plus_readout_graph_nullity", "global_configuration_dimension")] != [4, 4, 4, 4]:
        raise AssertionError("cover dimension control changed")
    checks.extend(["cover_independent_replay", "cover_dimensions_preserve_full_space"])

    prod_completion = production["completion_fibers"]
    ind_completion = independent["completion_fibers"]
    for key in (
        "distinct_graph_pairs",
        "pairwise_intersection_dimension_histogram",
        "pairs_with_nonzero_ambiguous_endpoint_line",
        "zero_endpoint_pair_belongs_to_all_graphs",
    ):
        if prod_completion[key] != ind_completion[key]:
            raise AssertionError(f"completion disagreement: {key}")
    if prod_completion["distinct_graph_pairs"] != 28:
        raise AssertionError("monodromy graph pair count changed")
    if prod_completion["pairwise_intersection_dimension_histogram"] != {"0": 16, "1": 12}:
        raise AssertionError("intersection histogram changed")
    checks.extend(["completion_independent_replay", "completion_ambiguity_exact"])

    prod_corr = production["admissibility_correspondence"]
    ind_corr = independent["admissibility_correspondence"]
    expected_survivors = {
        "A_product": 2,
        "A_quadratic": 4,
        "A_reconstruction_identity": 16,
    }
    if prod_corr["witness_survivor_counts"] != expected_survivors:
        raise AssertionError("production correspondence survivors changed")
    if ind_corr["witness_survivor_counts"] != expected_survivors:
        raise AssertionError("independent correspondence survivors changed")
    if not prod_corr["same_readout_and_frame_symmetry_allow_inequivalent_nontrivial_relations"]:
        raise AssertionError("nonuniqueness control lost")
    checks.extend(["correspondence_independent_replay", "inequivalent_relations_discriminate"])

    if result["cover_reconstruction"]["descent_plus_readout_graph_nullity"] != 4:
        raise AssertionError("saved result graph nullity changed")
    if result["completion_fibers"]["distinct_graph_pairs"] != 28:
        raise AssertionError("saved result completion count changed")
    if result["completion_fibers"]["pairs_with_nonzero_ambiguous_endpoint_line"] != 12:
        raise AssertionError("saved result ambiguity count changed")
    if result["admissibility_correspondence"]["witness_survivor_counts"] != expected_survivors:
        raise AssertionError("saved result correspondence counts changed")
    checks.append("saved_result_matches_replay")

    if independent_saved["completion_fibers"]["all_matrices_are_GL2Z"] is not True:
        raise AssertionError("independent GL2Z check missing")
    if independent_saved["completion_fibers"]["pairwise_intersection_dimension_histogram"] != {"0": 16, "1": 12}:
        raise AssertionError("saved independent histogram changed")
    checks.append("saved_independent_result_matches")

    operations = rows(package / "OPERATION_LEDGER.tsv")
    if len(operations) != 9 or {row["operation_id"] for row in operations} != {f"O{i:02d}" for i in range(1, 10)}:
        raise AssertionError("operation universe incomplete or duplicated")
    if any(row["selects_complete_physical_configurations"] != "NO" for row in operations):
        raise AssertionError("physical selection promotion")
    expected_operation_results = {
        "O01": "DERIVED_IDENTITY_ON_ADMITTED_GEOMETRIES",
        "O05": "DERIVED_PARTIAL_KINEMATIC_ADMISSIBILITY_CORRESPONDENCE",
        "O09": "WORKING_POSIT_DETERMINES_CORRESPONDENCE_TYPE_AND_NONTAUTOLOGY_REQUIREMENT",
    }
    for operation_id, expected in expected_operation_results.items():
        actual = next(row["current_result"] for row in operations if row["operation_id"] == operation_id)
        if actual != expected:
            raise AssertionError(f"operation promotion/regression: {operation_id}")
    checks.extend(["operation_universe_9_exact", "no_operation_selects_physics"])

    requirements = rows(package / "ADMISSIBILITY_REQUIREMENTS.tsv")
    if len(requirements) != 13 or {row["requirement_id"] for row in requirements} != {f"A{i:02d}" for i in range(1, 14)}:
        raise AssertionError("admissibility requirement universe incomplete or duplicated")
    requirement_map = {row["requirement_id"]: row for row in requirements}
    if requirement_map["A10"]["status"] != "NOT_REQUIRED_BY_POSIT":
        raise AssertionError("scalar optimizer silently promoted")
    if requirement_map["A13"]["status"] != "OPEN_SMALLEST_MISSING_OPERATION":
        raise AssertionError("complete relation silently closed")
    if requirement_map["A03"]["status"] != "WORKING_POSIT_FALSIFIABILITY_REQUIREMENT":
        raise AssertionError("nonidentity requirement lost")
    checks.extend(["admissibility_requirements_13_exact", "optimizer_not_assumed", "complete_relation_open"])

    premises = rows(package / "PREMISE_LEDGER.tsv")
    if len(premises) != 14 or {row["premise_id"] for row in premises} != {f"P{i:02d}" for i in range(1, 15)}:
        raise AssertionError("premise universe incomplete or duplicated")
    premise_map = {row["premise_id"]: row for row in premises}
    if premise_map["P07"]["status"] != "WORKING_POSIT_OWNER_AUTHORIZED":
        raise AssertionError("working posit provenance changed")
    if premise_map["P09"]["status"] != "CHALLENGED_INACTIVE":
        raise AssertionError("strong CSN reactivated")
    if premise_map["P11"]["status"] != "POSIT":
        raise AssertionError("carrier promoted")
    if premise_map["P14"]["status"] != "OPEN":
        raise AssertionError("physics closure promoted")
    checks.extend(["premises_14_exact", "premise_promotions_rejected"])

    sources = rows(package / "SOURCE_ADJUDICATION.tsv")
    if len(sources) != 26 or len({row["path"] for row in sources}) != 26:
        raise AssertionError("source universe incomplete or duplicated")
    for row in sources:
        source = REPO / row["path"]
        if not source.is_file():
            raise AssertionError(f"missing source: {row['path']}")
        if sha256(source) != row["sha256"]:
            raise AssertionError(f"source hash mismatch: {row['path']}")
    checks.append("source_hashes_26_exact")

    report = (package / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    architecture = (package / "RECONSTRUCTION_ARCHITECTURE.md").read_text(encoding="utf-8")
    exact = (package / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    combined_text = report + architecture + exact
    for required in (
        OUTCOME,
        "partial kinematic",
        "does not yet derive",
        "multiple branches",
        "not proposed UDT laws",
    ):
        if required not in combined_text:
            raise AssertionError(f"required scope wording missing: {required}")
    forbidden = (
        "native action is derived",
        "matter emergence is derived",
        "unique universe is selected",
        "bootstrap law is complete",
    )
    if any(token in combined_text.lower() for token in forbidden):
        raise AssertionError("forbidden promotion wording")
    checks.append("semantic_scope_guards")
    return checks


def mutation_catches() -> list[dict[str, str]]:
    mutations = [
        ("M01", "wrong outcome", "RESULT.json", OUTCOME, "DERIVED_COMPLETE_BOOTSTRAP_LAW"),
        ("M02", "wrong graph-pair count", "RESULT.json", '"distinct_graph_pairs": 28', '"distinct_graph_pairs": 27'),
        ("M03", "wrong ambiguity count", "RESULT.json", '"pairs_with_nonzero_ambiguous_endpoint_line": 12', '"pairs_with_nonzero_ambiguous_endpoint_line": 11'),
        ("M04", "wrong graph nullity", "RESULT.json", '"descent_plus_readout_graph_nullity": 4', '"descent_plus_readout_graph_nullity": 3'),
        ("M05", "physical selection promotion", "OPERATION_LEDGER.tsv", "O05\tmonodromy_seam_cap_fibers\tDERIVED_PARTIAL_KINEMATIC_ADMISSIBILITY_CORRESPONDENCE\tNO", "O05\tmonodromy_seam_cap_fibers\tDERIVED_PARTIAL_KINEMATIC_ADMISSIBILITY_CORRESPONDENCE\tYES"),
        ("M06", "working posit promoted", "OPERATION_LEDGER.tsv", "O09\tglobal_local_mutual_admissibility\tWORKING_POSIT_DETERMINES_CORRESPONDENCE_TYPE_AND_NONTAUTOLOGY_REQUIREMENT", "O09\tglobal_local_mutual_admissibility\tDERIVED_COMPLETE_RETURN"),
        ("M07", "nonidentity requirement deleted", "ADMISSIBILITY_REQUIREMENTS.tsv", "A03\tnonidentity_admissibility\tWORKING_POSIT_FALSIFIABILITY_REQUIREMENT", "A03\tnonidentity_admissibility\tOPEN"),
        ("M08", "optimizer silently required", "ADMISSIBILITY_REQUIREMENTS.tsv", "A10\tscalar_objective_or_optimizer\tNOT_REQUIRED_BY_POSIT", "A10\tscalar_objective_or_optimizer\tDERIVED_REQUIRED"),
        ("M09", "complete relation promoted", "ADMISSIBILITY_REQUIREMENTS.tsv", "A13\tmetric_native_complete_relation_K\tOPEN_SMALLEST_MISSING_OPERATION", "A13\tmetric_native_complete_relation_K\tDERIVED"),
        ("M10", "strong CSN reactivated", "PREMISE_LEDGER.tsv", "P09\tstrong_local_CSN\tCHALLENGED_INACTIVE", "P09\tstrong_local_CSN\tACTIVE_DERIVED"),
        ("M11", "carrier promoted", "PREMISE_LEDGER.tsv", "P11\tS2_carrier\tPOSIT", "P11\tS2_carrier\tDERIVED"),
        ("M12", "source hash corruption", "SOURCE_ADJUDICATION.tsv", "04cb1621c0bb2616fb1260ae0775b46f1da02e081e30baa5b29f24606109a5d3", "00cb1621c0bb2616fb1260ae0775b46f1da02e081e30baa5b29f24606109a5d3"),
    ]
    caught: list[dict[str, str]] = []
    with tempfile.TemporaryDirectory(prefix="udt_reconstruction_verify_") as temporary:
        base = Path(temporary) / "package"
        shutil.copytree(PACKAGE, base)
        for mutation_id, description, relative, old, new in mutations:
            mutated = Path(temporary) / mutation_id
            shutil.copytree(base, mutated)
            target = mutated / relative
            text = target.read_text(encoding="utf-8")
            if old not in text:
                raise AssertionError(f"mutation target absent: {mutation_id}")
            target.write_text(text.replace(old, new, 1), encoding="utf-8")
            try:
                validate(mutated)
            except AssertionError as error:
                caught.append({"mutation_id": mutation_id, "description": description, "status": "CAUGHT", "reason": str(error)})
            else:
                raise AssertionError(f"mutation escaped: {mutation_id}")
    return caught


def main() -> None:
    checks = validate(PACKAGE)
    catches = mutation_catches()
    result = {
        "schema": "udt.global_local_reconstruction.verification.v1",
        "status": "PASS",
        "checks_passed": len(checks),
        "checks": checks,
        "mutations_caught": len(catches),
        "catch_proofs": catches,
        "source_adjudication_sha256": sha256(PACKAGE / "SOURCE_ADJUDICATION.tsv"),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
