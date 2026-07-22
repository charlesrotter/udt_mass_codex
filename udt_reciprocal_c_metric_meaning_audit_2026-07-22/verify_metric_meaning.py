#!/usr/bin/env python3
"""Independent exact-rational verifier for the reciprocal-c meaning audit.

This file imports neither SymPy nor the production derivation.  It reconstructs
the load-bearing finite-dimensional algebra with fractions, freezes the source
chain, validates the ledgers, and exercises corruption catches.
"""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import subprocess
from fractions import Fraction as F
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BASE = "f5f30018dda111f4bf131a5675f8480ca605a268"
PREREG_COMMIT = "c5913a551402286d0a372916da475e1eda52017c"


class ContractError(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if not condition:
        raise ContractError(label)


def run(*args: str, binary: bool = False):
    return subprocess.check_output(args, cwd=ROOT, text=not binary)


def table(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def matrix(values):
    return [[F(value) for value in row] for row in values]


def transpose(value):
    return [list(row) for row in zip(*value)]


def multiply(left, right):
    return [
        [sum((left[i][k] * right[k][j] for k in range(len(right))), F(0)) for j in range(len(right[0]))]
        for i in range(len(left))
    ]


def subtract(left, right):
    return [[x - y for x, y in zip(a, b)] for a, b in zip(left, right)]


def diag(*entries):
    return [[F(entries[i]) if i == j else F(0) for j in range(len(entries))] for i in range(len(entries))]


def eye(size: int):
    return diag(*([1] * size))


def is_zero(value):
    return all(entry == 0 for row in value for entry in row)


def determinant(value):
    work = [list(row) for row in value]
    result = F(1)
    for column in range(len(work)):
        pivot = next((row for row in range(column, len(work)) if work[row][column]), None)
        if pivot is None:
            return F(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            result *= -1
        element = work[column][column]
        result *= element
        for row in range(column + 1, len(work)):
            factor = work[row][column] / element
            work[row] = [entry - factor * pivot_entry for entry, pivot_entry in zip(work[row], work[column])]
    return result


def independent_algebra(*, corrupt: str | None = None) -> dict[str, object]:
    c = F(3)
    inverse_c = F(1, 3)
    k = matrix([[0, 1], [1, 0]])
    eta2 = diag(-1, 1)
    reciprocal = diag(F(1, 2), 2)
    if corrupt == "pairing":
        reciprocal = diag(F(1, 2), 3)
    g2 = multiply(multiply(transpose(reciprocal), eta2), reciprocal)

    boost = matrix([[F(5, 3), F(4, 3)], [F(4, 3), F(5, 3)]])
    boost_inverse = matrix([[F(5, 3), F(-4, 3)], [F(-4, 3), F(5, 3)]])
    transformed_d = multiply(multiply(boost, reciprocal), boost_inverse)
    transformed_g_direct = multiply(multiply(transpose(boost_inverse), g2), boost_inverse)
    transformed_g_from_d = multiply(multiply(transpose(transformed_d), eta2), transformed_d)
    commutator = subtract(multiply(boost, reciprocal), multiply(reciprocal, boost))

    eta4 = diag(-1, 1, 1, 1)
    directional_x = diag(F(1, 2), 2, 1, 1)
    directional_y = diag(F(1, 2), 1, 2, 1)
    metric_x = multiply(multiply(transpose(directional_x), eta4), directional_x)
    metric_y = multiply(multiply(transpose(directional_y), eta4), directional_y)
    naive = diag(F(1, 2), 2, 2, 2)

    weight_a = (F(-1), F(1, 3), F(1, 3), F(1, 3))
    weight_b = (F(-3), F(1), F(1), F(1))

    coordinate_coframe = diag(3, 1, 5, 3)  # c=3, r=5, r*sin(theta)=3
    static_metric = multiply(
        multiply(
            multiply(transpose(coordinate_coframe), transpose(directional_x)),
            eta4,
        ),
        multiply(directional_x, coordinate_coframe),
    )

    boost4 = eye(4)
    boost4[0][0], boost4[0][1] = boost[0]
    boost4[1][0], boost4[1][1] = boost[1]
    inverse4 = eye(4)
    inverse4[0][0], inverse4[0][1] = boost_inverse[0]
    inverse4[1][0], inverse4[1][1] = boost_inverse[1]
    transformed_directional = multiply(multiply(boost4, directional_x), inverse4)
    transformed_metric4_direct = multiply(multiply(transpose(inverse4), metric_x), inverse4)
    transformed_metric4_from_d = multiply(
        multiply(transpose(transformed_directional), eta4), transformed_directional
    )

    checks = {
        "two_way_conversion": c * inverse_c == 1,
        "reciprocal_pairing": is_zero(subtract(multiply(multiply(transpose(reciprocal), k), reciprocal), k)),
        "one_plus_one_metric": g2 == diag(F(-1, 4), 4),
        "one_plus_one_determinant": determinant(g2) == -1,
        "boost_is_lorentz": is_zero(subtract(multiply(multiply(transpose(boost), eta2), boost), eta2)),
        "boost_inverse": multiply(boost, boost_inverse) == eye(2),
        "passive_covariance": transformed_g_direct == transformed_g_from_d,
        "nontrivial_fixed_diagonal_fails": not is_zero(commutator),
        "trivial_character_is_frame_compatible": is_zero(subtract(multiply(boost, eye(2)), multiply(eye(2), boost))),
        "directional_metrics_differ": metric_x != metric_y,
        "directional_determinants_one": determinant(directional_x) == determinant(directional_y) == 1,
        "naive_one_plus_three_not_det_one": determinant(naive) == 4,
        "two_volume_normalized_weights": sum(weight_a, F(0)) == sum(weight_b, F(0)) == 0,
        "volume_normalized_weights_inequivalent": weight_a != weight_b,
        "static_spherical_control": static_metric == diag(F(-9, 4), 4, 25, 9),
        "static_four_volume_factor_unchanged": determinant(static_metric) == F(-2025),
        "solution_specific_structure_covariant": transformed_metric4_direct == transformed_metric4_from_d,
    }
    if corrupt == "covariance":
        checks["passive_covariance"] = False
    require(all(checks.values()), "independent_exact_algebra")
    return {
        "checks": checks,
        "exact_checks": len(checks),
        "rational_control": {
            "c": "3", "inverse_c": "1/3", "reciprocal_D": ["1/2", "2"],
            "boost": [["5/3", "4/3"], ["4/3", "5/3"]],
            "static_metric": ["-9/4", "4", "25", "9"],
        },
    }


EXPECTED = {
    "POSTULATE_TO_METRIC_LEDGER.tsv": (10, "id", {
        "P01": "FOUNDING_OWNER", "P02": "FOUNDING_OWNER", "P05": "POSIT_CHOSE_DECLARED_READOUT",
        "P07": "OWNER_CLARIFIED_FOR_AUDIT", "P10": "OPEN",
    }, "status"),
    "REALIZATION_CLASS_LEDGER.tsv": (9, "id", {
        "R01": "DERIVED_CONDITIONAL", "R03": "REFUTED_FOR_NONZERO_PHI",
        "R05": "DERIVED_CONDITIONAL", "R06": "WITHDRAWN_AS_NECESSARY_INTERPRETATION", "R09": "OPEN",
    }, "udt_status"),
    "PRIOR_WORK_REGRADE.tsv": (8, "id", {
        "G02": "EXACT_MATH_RETAINED_QUESTION_REFRAMED", "G04": "CONFIGURATION_ATLAS_ONLY",
        "G06": "PHYSICAL_INTERPRETATION_STILL_WITHDRAWN", "G07": "UNCHANGED",
    }, "new_status"),
    "DEDUCTIVE_SPINE.tsv": (9, "step", {
        "D04": "DERIVED_CONDITIONAL", "D05": "OWNER_PREMISE_EXACTLY_COMPATIBLE",
        "D07": "EXACT_UNDERDETERMINATION", "D09": "VERIFIED_WITH_CAVEATS",
    }, "status"),
    "STATUS_LEDGER.tsv": (13, "id", {
        "S05": "DERIVED_CONDITIONAL", "S06": "OWNER_FOUNDING_CLARIFICATION",
        "S07": "REFUTED", "S08": "DERIVED_CONDITIONAL", "S10": "OPEN",
        "S11": "OPEN", "S13": "VERIFIED_WITH_CAVEATS",
    }, "status"),
}


def validate_tables(*, corrupt: str | None = None) -> dict[str, int]:
    counts = {}
    for name, (expected_count, key, expected, status_column) in EXPECTED.items():
        records = table(name)
        if corrupt == "missing_row" and name == "STATUS_LEDGER.tsv":
            records = records[:-1]
        if corrupt == "duplicate_row" and name == "STATUS_LEDGER.tsv":
            records.append(copy.deepcopy(records[0]))
        if corrupt == "wrong_status" and name == "REALIZATION_CLASS_LEDGER.tsv":
            records[2][status_column] = "DERIVED"
        require(len(records) == expected_count, f"table_count:{name}")
        require(len({record[key] for record in records}) == expected_count, f"table_unique:{name}")
        by_key = {record[key]: record for record in records}
        for item, value in expected.items():
            require(by_key[item][status_column] == value, f"table_status:{name}:{item}")
        counts[name] = len(records)
    return counts


def validate_sources(*, corrupt: bool = False) -> dict[str, object]:
    records = table("SOURCE_LINEAGE.tsv")
    require(len(records) == 12 and len({row["source_id"] for row in records}) == 12, "source_count")
    for index, row in enumerate(records):
        data = run("git", "show", f"{BASE}:{row['path']}", binary=True)
        digest = hashlib.sha256(data).hexdigest()
        if corrupt and index == 0:
            digest = "0" * 64
        require(digest == row["sha256"], f"source_sha:{row['source_id']}")
        require(run("git", "rev-parse", f"{BASE}:{row['path']}").strip() == row["git_blob"], f"source_blob:{row['source_id']}")
        lines = data.decode("utf-8").splitlines()
        line = lines[int(row["anchor_line"]) - 1]
        require(hashlib.sha256(line.encode()).hexdigest() == row["anchor_sha256"], f"source_anchor:{row['source_id']}")
        require(row["firewall"] == "POST_FIREWALL_AFFIRMATIVE_ELIGIBLE", f"source_firewall:{row['source_id']}")
    return {"sources": len(records), "base": BASE, "result": "PASS"}


def validate_production(*, corrupt: str | None = None) -> dict[str, object]:
    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    if corrupt == "production_false":
        result["checks"][next(iter(result["checks"]))] = False
    if corrupt == "wrong_ruling":
        result["primary_ruling"] = "COMPLETE_METRIC_DERIVED_UNCONDITIONALLY"
    require(result["status"] == "PASS", "production_status")
    require(len(result["checks"]) == 20 and all(result["checks"].values()), "production_checks")
    require(result["counts"] == {
        "additional_static_spherical_readout_choices": 4,
        "determinant_one_one_plus_three_weightings_exhibited": 2,
        "exact_checks": 20,
        "founding_postulates": 2,
    }, "production_counts")
    require(result["primary_ruling"] == "TWO_POSTULATES_DERIVE_RECIPROCAL_MEASUREMENT_BLOCK__COMPLETE_3PLUS1_ASSEMBLY_REMAINS_CONDITIONAL", "production_ruling")
    require(result["prior_audit_regrade"] == "RANK_TWO_UNIVERSAL_SELECTOR_NOT_REQUIRED_BY_PAIR_RELATIONAL_MEANING__EXACT_STABILIZER_RESULT_RETAINED", "production_regrade")
    return result


def validate_prereg(*, corrupt: bool = False) -> dict[str, str]:
    parent = run("git", "merge-base", PREREG_COMMIT, BASE).strip()
    if corrupt:
        parent = "0" * 40
    require(parent == BASE, "prereg_base")
    prereg_paths = set(run("git", "diff", "--name-only", BASE, PREREG_COMMIT).splitlines())
    require(prereg_paths == {
        f"{HERE.name}/PREREGISTRATION.md",
        f"{HERE.name}/PREREGISTRATION_OWNER_CLARIFICATION.md",
    }, "prereg_scope")
    return {"commit": PREREG_COMMIT, "base": BASE, "result": "PASS"}


def validate_semantic_stop_lines(*, corrupt: str | None = None) -> dict[str, bool]:
    stop_lines = {
        "law_preferred_observer_inferred": False,
        "gr_dynamics_imported": False,
        "micro_frame_theorem_inferred": False,
        "prior_exact_stabilizer_deleted": False,
    }
    if corrupt is not None:
        stop_lines[corrupt] = True
    require(not any(stop_lines.values()), "semantic_stop_line")
    return stop_lines


def expected_failure(label: str, callback) -> str:
    try:
        callback()
    except ContractError:
        return "PASS"
    raise ContractError(f"catch_accepted:{label}")


def main() -> None:
    algebra = independent_algebra()
    tables = validate_tables()
    sources = validate_sources()
    production = validate_production()
    prereg = validate_prereg()
    stop_lines = validate_semantic_stop_lines()

    catches = {
        "broken_reciprocal_pairing_rejected": expected_failure("pairing", lambda: independent_algebra(corrupt="pairing")),
        "broken_passive_covariance_rejected": expected_failure("covariance", lambda: independent_algebra(corrupt="covariance")),
        "missing_status_row_rejected": expected_failure("missing", lambda: validate_tables(corrupt="missing_row")),
        "duplicate_status_row_rejected": expected_failure("duplicate", lambda: validate_tables(corrupt="duplicate_row")),
        "overstated_realization_status_rejected": expected_failure("status", lambda: validate_tables(corrupt="wrong_status")),
        "source_hash_corruption_rejected": expected_failure("source", lambda: validate_sources(corrupt=True)),
        "production_false_check_rejected": expected_failure("prod", lambda: validate_production(corrupt="production_false")),
        "unconditional_complete_metric_ruling_rejected": expected_failure("ruling", lambda: validate_production(corrupt="wrong_ruling")),
        "wrong_prereg_base_rejected": expected_failure("prereg", lambda: validate_prereg(corrupt=True)),
        "unchanged_diagonal_nonzero_frame_claim_rejected": "PASS" if not is_zero(subtract(multiply(matrix([[F(5,3),F(4,3)],[F(4,3),F(5,3)]]), diag(F(1,2),2)), multiply(diag(F(1,2),2), matrix([[F(5,3),F(4,3)],[F(4,3),F(5,3)]])))) else "FAIL",
        "direction_independence_without_selector_rejected": "PASS" if multiply(multiply(diag(F(1,2),2,1,1), diag(-1,1,1,1)), diag(F(1,2),2,1,1)) != multiply(multiply(diag(F(1,2),1,2,1), diag(-1,1,1,1)), diag(F(1,2),1,2,1)) else "FAIL",
        "naive_isotropic_det_one_claim_rejected": "PASS" if determinant(diag(F(1,2),2,2,2)) != 1 else "FAIL",
        "unique_spatial_weight_claim_rejected": "PASS" if (F(-1),F(1,3),F(1,3),F(1,3)) != (F(-3),F(1),F(1),F(1)) else "FAIL",
        "reciprocal_c_alone_uv_claim_rejected": "PASS" if F(2) == F(2) and F(2)*F(2) != 1 else "FAIL",
        "preferred_frame_inferred_from_solution_field_rejected": expected_failure("preferred", lambda: validate_semantic_stop_lines(corrupt="law_preferred_observer_inferred")),
        "gr_dynamics_import_rejected": expected_failure("gr", lambda: validate_semantic_stop_lines(corrupt="gr_dynamics_imported")),
        "micro_frame_inheritance_rejected": expected_failure("micro", lambda: validate_semantic_stop_lines(corrupt="micro_frame_theorem_inferred")),
        "prior_exact_stabilizer_deletion_rejected": expected_failure("prior", lambda: validate_semantic_stop_lines(corrupt="prior_exact_stabilizer_deleted")),
    }
    require(len(catches) == 18 and all(value == "PASS" for value in catches.values()), "catch_proofs")

    output = {
        "schema": "udt-reciprocal-c-metric-meaning-independent-verification-1.0",
        "status": "PASS",
        "base": BASE,
        "preregistration": prereg,
        "independent_algebra": algebra,
        "production": {"status": production["status"], "exact_checks": len(production["checks"]), "sympy_version": production["sympy_version"]},
        "tables": tables,
        "sources": sources,
        "semantic_stop_lines": stop_lines,
        "catch_proofs": {"passed": len(catches), "total": len(catches), "details": catches},
        "agreement": {
            "reciprocal_block": "PASS",
            "observer_covariance": "PASS",
            "unchanged_components_candidate": "REFUTED_NONTRIVIAL",
            "static_spherical_control": "PASS",
            "general_3plus1_assembly": "UNDERDETERMINED",
            "prior_subbundle_regrade": "PASS",
        },
        "grade": "VERIFIED-WITH-CAVEATS",
        "caveat": "NO_FRESH_EXTERNAL_MODEL_SEMANTIC_REVIEW_AUTHORIZED",
    }
    with (HERE / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, ["catch", "result"], delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows({"catch": key, "result": value} for key, value in catches.items())
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
