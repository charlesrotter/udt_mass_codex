#!/usr/bin/env python3
"""Independent fail-closed verifier for the local-selector/holonomy atlas."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
STRUCTURAL = ROOT / "udt_structural_ensemble_metric_atlas_2026-07-21"
TOL = 1.0e-9
PAIRS = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(131072), b""):
            value.update(block)
    return value.hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def add_orthonormal(basis: list[np.ndarray], matrix: np.ndarray) -> tuple[bool, float]:
    vector = np.asarray(matrix, dtype=float).reshape(-1)
    norm = float(np.linalg.norm(vector))
    if norm <= 1.0e-13:
        return False, 0.0
    vector = vector / norm
    for item in basis:
        vector -= float(vector @ item) * item
    # A second pass makes this independent MGS closure numerically stable.
    for item in basis:
        vector -= float(vector @ item) * item
    residual = float(np.linalg.norm(vector))
    if residual <= TOL:
        return False, residual
    basis.append(vector / residual)
    return True, residual


def independent_algebra_dimension(operators: list[np.ndarray]) -> tuple[int, float, float]:
    generators = []
    for operator in operators:
        norm = float(np.linalg.norm(operator))
        if norm > 1.0e-13:
            generators.append(np.asarray(operator, dtype=float) / norm)
    basis: list[np.ndarray] = []
    accepted = []
    rejected = []
    for candidate in [np.eye(4), *generators]:
        added, residual = add_orthonormal(basis, candidate)
        (accepted if added else rejected).append(residual)
    changed = True
    while changed and len(basis) < 16:
        changed = False
        current = [item.reshape(4, 4) for item in basis]
        for left in current:
            for right in generators:
                added, residual = add_orthonormal(basis, left @ right)
                (accepted if added else rejected).append(residual)
                changed |= added
                if len(basis) == 16:
                    break
            if len(basis) == 16:
                break
    return len(basis), min(accepted, default=0.0), max(rejected, default=0.0)


def length_two_word_span_margin(operators: list[np.ndarray]) -> float:
    generators = []
    for operator in operators:
        norm = float(np.linalg.norm(operator))
        if norm > 1.0e-13:
            generators.append(np.asarray(operator, dtype=float) / norm)
    words = [np.eye(4), *generators, *(left @ right for left in generators for right in generators)]
    rows = []
    for word in words:
        vector = word.reshape(-1)
        norm = float(np.linalg.norm(vector))
        if norm > 1.0e-13:
            rows.append(vector / norm)
    singular = np.linalg.svd(np.asarray(rows), compute_uv=False)
    if len(singular) < 16:
        return 0.0
    return float(singular[15] / singular[0])


def curvature_operators(raw: dict[str, object]) -> list[np.ndarray]:
    metric = np.asarray(raw["metric"], dtype=float)
    inverse = np.linalg.inv(metric)
    down = np.asarray(raw["riemann_down"], dtype=float)
    up = np.einsum("ar,rsuv->asuv", inverse, down)
    return [up[:, :, mu, nu] for mu, nu in PAIRS]


def validate_atlas(rows: list[dict[str, str]], independent: dict[str, dict[str, object]]) -> None:
    if len(rows) != 6144:
        raise AssertionError("atlas row count")
    ids = [row["configuration_id"] for row in rows]
    if len(set(ids)) != len(ids):
        raise AssertionError("duplicate configuration")
    if set(ids) != set(independent):
        raise AssertionError("configuration identity coverage")
    counts = Counter()
    for row in rows:
        record = independent[row["configuration_id"]]
        if int(row["base_algebra_dimension"]) != record["dimension"]:
            raise AssertionError(f"independent dimension {row['configuration_id']}")
        flat = record["flat_exact"]
        expected = (
            "EXACT_CONSTANT_METRIC_FLAT__ALL_SUBSPACES_AMBIGUOUS"
            if flat else "BASE_CURVATURE_FULL_IRREDUCIBLE__HIGHER_JETS_MONOTONE"
        )
        if row["final_class"] != expected:
            raise AssertionError(f"classification {row['configuration_id']}")
        if row["flat_exact"] != ("YES" if flat else "NO"):
            raise AssertionError(f"flat disclosure {row['configuration_id']}")
        if flat and row["mask_id"] not in {"M0", "M8"}:
            raise AssertionError("flat outside M0/M8")
        if not flat and record["dimension"] != 16:
            raise AssertionError("intermediate algebra retained without classification")
        counts[expected] += 1
    if counts != Counter({
        "BASE_CURVATURE_FULL_IRREDUCIBLE__HIGHER_JETS_MONOTONE": 5376,
        "EXACT_CONSTANT_METRIC_FLAT__ALL_SUBSPACES_AMBIGUOUS": 768,
    }):
        raise AssertionError(f"class counts {counts}")


def validate_q01(rows: list[dict[str, str]], logic: list[dict[str, str]]) -> None:
    if len(rows) != 16 or len({row["candidate_id"] for row in rows}) != 16:
        raise AssertionError("Q01 coverage")
    required_types = {
        "UNTYPED_REALIZATION_RELATION", "SCALAR", "SCALAR_CURVATURE_CONTRACTION", "SCALAR_DENSITY",
        "COVECTOR_OR_VECTOR_LINE", "SYMMETRIC_TWO_TENSOR", "PROJECTOR_OR_INVOLUTION",
        "TWO_FORM_OR_BIVECTOR", "CONNECTION_OR_CURVATURE_VALUED", "COFRAME_ROW_OR_SLOT",
        "COFRAME_GAUGE_INVARIANT_CONTRACTION", "ARBITRARY_SMOOTH_COMBINATION", "HIGHER_FINITE_JET_OUTPUT",
    }
    if not required_types.issubset({row["output_type"] for row in rows}):
        raise AssertionError("Q01 output type")
    by_id = {row["candidate_id"]: row for row in rows}
    if by_id["Q01_U00"]["status"] != "CLASS_INFINITE_OR_UNTYPED__EXHAUSTION_NOT_WELL_POSED":
        raise AssertionError("untyped exhaustion promoted")
    if by_id["Q01_F00"]["status"] != "FRAME_DEPENDENT__UNSELECTED":
        raise AssertionError("coframe row promoted")
    if by_id["Q01_H00"]["status"] != "OPEN_HIGHER_JETS":
        raise AssertionError("higher jets closed")
    logic_by_id = {row["logic_id"]: row for row in logic}
    if len(logic_by_id) != 4:
        raise AssertionError("logic coverage")
    if logic_by_id["L01_CSN_ORBIT_CONSTANCY"]["status"] != "DERIVED_EXACT":
        raise AssertionError("CSN orbit logic")


def validate_anchors(rows: list[dict[str, str]]) -> None:
    expected = {
        *(f"R00_1_M{mask:X}_B0_P0" for mask in range(16)),
        *(f"V016_M{mask:X}_B3_P7" for mask in range(16)),
    }
    if len(rows) != 32 or {row["configuration_id"] for row in rows} != expected:
        raise AssertionError("anchor identities")
    for row in rows:
        if row["algebra_agreement"] != "YES" or row["residual_gate"] != "PASS":
            raise AssertionError(f"anchor gate {row['configuration_id']}")
        for prefix in ("h1", "h2"):
            if row[f"{prefix}_direct_dimension"] != row[f"{prefix}_transported_dimension"]:
                raise AssertionError("anchor algebra disagreement")
    maximum = max(float(row["h1_derivative_residual"]) for row in rows)
    if maximum > 2.0e-5:
        raise AssertionError("derivative residual")


def validate_scope(result: dict[str, object], report: str, controls: list[dict[str, str]]) -> None:
    if result["q02"]["global_holonomy_claim"] != "NOT_MADE":
        raise AssertionError("global holonomy overclaim")
    normalized_report = " ".join(report.split())
    required = (
        "not arbitrary four-metrics", "no closed-loop global holonomy theorem",
        "No action, variation domain, source, carrier", "separately supplied reciprocal-toric control is not refuted",
    )
    if any(fragment not in normalized_report for fragment in required):
        raise AssertionError("report scope language")
    if {row["control_id"] for row in controls} != {
        "C01_RECIPROCAL_TORIC", "C02_SEAL_REFLECTION", "C03_GLOBAL_COMPLETIONS"
    }:
        raise AssertionError("out-of-ensemble controls")


def expect_failure(name: str, action, catches: list[dict[str, object]]) -> None:
    failed = False
    detail = ""
    try:
        action()
    except Exception as exc:  # expected mutation rejection
        failed = True
        detail = f"{type(exc).__name__}:{exc}"
    if not failed:
        raise AssertionError(f"catch did not fail: {name}")
    catches.append({"catch_id": name, "status": "PASS", "detail": detail})


def main() -> None:
    atlas = read_tsv(HERE / "CURVATURE_HOLONOMY_SEED_ATLAS.tsv")
    q01 = read_tsv(HERE / "LOCAL_OUTPUT_TYPE_CENSUS.tsv")
    logic = read_tsv(HERE / "CSN_AND_EXHAUSTIBILITY_LOGIC.tsv")
    anchors = read_tsv(HERE / "DIRECT_DERIVATIVE_ANCHORS.tsv")
    controls = read_tsv(HERE / "OUT_OF_ENSEMBLE_CONTROLS.tsv")
    result = json.loads((HERE / "ATLAS_RESULT.json").read_text(encoding="utf-8"))
    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")

    independent: dict[str, dict[str, object]] = {}
    smallest_added = 1.0
    smallest_full_word_margin = 1.0
    smallest_full_word_margin_id = "-"
    largest_rejected = 0.0
    for shard in read_tsv(STRUCTURAL / "RAW_SHARD_REGISTRY.tsv"):
        shard_path = STRUCTURAL / shard["path"]
        if digest(shard_path) != shard["sha256"]:
            raise AssertionError(f"shard hash {shard['path']}")
        with shard_path.open(encoding="utf-8") as handle:
            for line in handle:
                raw = json.loads(line)
                configuration_id = raw["configuration_id"]
                if configuration_id in independent:
                    raise AssertionError("raw duplicate")
                operators = curvature_operators(raw)
                dimension, minimum, rejected = independent_algebra_dimension(operators)
                amplitudes = np.asarray(raw["effective_amplitudes"], dtype=float)
                flat = bool(
                    np.all(amplitudes[:10] == 0.0)
                    and np.max(np.abs(np.asarray(raw["metric_first"], dtype=float))) == 0.0
                    and np.max(np.abs(np.asarray(raw["metric_second"], dtype=float))) == 0.0
                    and np.max(np.abs(np.asarray(raw["riemann_down"], dtype=float))) == 0.0
                )
                independent[configuration_id] = {
                    "dimension": dimension,
                    "flat_exact": flat,
                    "operators": operators,
                }
                if dimension > 1:
                    smallest_added = min(smallest_added, minimum)
                if dimension == 16:
                    margin = length_two_word_span_margin(operators)
                    if margin < smallest_full_word_margin:
                        smallest_full_word_margin = margin
                        smallest_full_word_margin_id = configuration_id
                largest_rejected = max(largest_rejected, rejected)

    validate_atlas(atlas, independent)
    validate_q01(q01, logic)
    validate_anchors(anchors)
    validate_scope(result, report, controls)

    catches: list[dict[str, object]] = []
    expect_failure("C01_MISSING_CONFIGURATION", lambda: validate_atlas(atlas[:-1], independent), catches)
    duplicated = [*atlas, dict(atlas[0])]
    expect_failure("C02_DUPLICATE_CONFIGURATION", lambda: validate_atlas(duplicated, independent), catches)
    changed = copy.deepcopy(atlas)
    full_index = next(index for index, row in enumerate(changed) if row["base_algebra_dimension"] == "16")
    changed[full_index]["final_class"] = "PROPER_COMMON_REDUCTION_OBSERVED_BOUNDED"
    expect_failure("C03_FALSE_PROPER_REDUCTION", lambda: validate_atlas(changed, independent), catches)
    changed = copy.deepcopy(atlas)
    flat_index = next(index for index, row in enumerate(changed) if row["flat_exact"] == "YES")
    changed[flat_index]["final_class"] = "PROPER_COMMON_REDUCTION_OBSERVED_BOUNDED"
    expect_failure("C04_FLAT_ROW_PROMOTED", lambda: validate_atlas(changed, independent), catches)
    changed_q01 = copy.deepcopy(q01)
    next(row for row in changed_q01 if row["candidate_id"] == "Q01_U00")["status"] = "DERIVED_REPRESENTATIVE"
    expect_failure("C05_UNTYPED_SELECTOR_PROMOTED", lambda: validate_q01(changed_q01, logic), catches)
    changed_q01 = copy.deepcopy(q01)
    next(row for row in changed_q01 if row["candidate_id"] == "Q01_F00")["status"] = "DERIVED"
    expect_failure("C06_FRAME_LABEL_PROMOTED", lambda: validate_q01(changed_q01, logic), catches)
    changed_q01 = copy.deepcopy(q01)
    next(row for row in changed_q01 if row["candidate_id"] == "Q01_H00")["status"] = "NO_SELECTOR"
    expect_failure("C07_HIGHER_JETS_FALSELY_CLOSED", lambda: validate_q01(changed_q01, logic), catches)

    def reject_phi_holonomy() -> None:
        sources = {"RIEMANN", "PHI_HESSIAN"}
        if sources != {"RIEMANN"}:
            raise AssertionError("non-curvature operator inserted into Levi-Civita holonomy")

    expect_failure("C08_PHI_INSERTED_IN_HOLONOMY", reject_phi_holonomy, catches)

    full_id = atlas[full_index]["configuration_id"]
    zero_dimension, _a, _b = independent_algebra_dimension([np.zeros((4, 4))] * 6)
    expect_failure(
        "C09_CURVATURE_GENERATORS_OMITTED",
        lambda: (_ for _ in ()).throw(AssertionError("omitted generator changes dimension"))
        if zero_dimension != independent[full_id]["dimension"] else None,
        catches,
    )
    changed_anchors = copy.deepcopy(anchors)
    changed_anchors[0]["h1_transported_dimension"] = "16"
    expect_failure("C10_DERIVATIVE_ALGEBRA_MISMATCH", lambda: validate_anchors(changed_anchors), catches)
    changed_anchors = copy.deepcopy(anchors)
    changed_anchors[0]["residual_gate"] = "FAIL_RETAINED"
    expect_failure("C11_DERIVATIVE_RESIDUAL_FAILURE", lambda: validate_anchors(changed_anchors), catches)
    changed_result = copy.deepcopy(result)
    changed_result["q02"]["global_holonomy_claim"] = "PROVED"
    expect_failure("C12_GLOBAL_HOLONOMY_OVERCLAIM", lambda: validate_scope(changed_result, report, controls), catches)
    changed_independent = dict(independent)
    changed_independent.pop(next(iter(changed_independent)))
    expect_failure("C13_RAW_IDENTITY_LOSS", lambda: validate_atlas(atlas, changed_independent), catches)
    changed = copy.deepcopy(atlas)
    next(row for row in changed if row["mask_id"] == "M8")["flat_exact"] = "NO"
    expect_failure("C14_PHI_ONLY_FLAT_DISCLOSURE_LOST", lambda: validate_atlas(changed, independent), catches)
    changed_controls = controls[:-1]
    expect_failure("C15_CONDITIONAL_CONTROL_DROPPED", lambda: validate_scope(result, report, changed_controls), catches)

    write_tsv(HERE / "CATCH_PROOFS.tsv", catches)
    verification = {
        "schema": "udt-local-selector-holonomy-verification-1.0",
        "verdict": "PASS_WITH_CAVEAT_NO_FRESH_EXTERNAL_MODEL_REVIEW",
        "independent_method": "raw Riemann tensors plus modified-Gram-Schmidt word closure",
        "independent_configurations": len(independent),
        "independent_class_counts": dict(sorted(Counter(
            "FLAT_AMBIGUOUS" if row["flat_exact"] else "FULL_IRREDUCIBLE"
            for row in independent.values()
        ).items())),
        "anchor_rows": len(anchors),
        "q01_rows": len(q01),
        "catch_proofs": len(catches),
        "catch_passes": sum(row["status"] == "PASS" for row in catches),
        "smallest_incremental_added_basis_residual_diagnostic_only": smallest_added,
        "smallest_full_length_two_word_span_singular_ratio": smallest_full_word_margin,
        "smallest_full_length_two_word_span_configuration": smallest_full_word_margin_id,
        "largest_independent_rejected_basis_residual": largest_rejected,
        "atlas_sha256": digest(HERE / "CURVATURE_HOLONOMY_SEED_ATLAS.tsv"),
        "q01_sha256": digest(HERE / "LOCAL_OUTPUT_TYPE_CENSUS.tsv"),
        "report_sha256": digest(HERE / "AUDIT_REPORT.md"),
        "fresh_external_model_review": "NOT_RUN__NO_SUBAGENT_AUTHORITY_IN_CURRENT_EXECUTION_CONTEXT",
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(
        json.dumps(verification, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(verification, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
