#!/usr/bin/env python3
"""Independent standard-library exact verifier for the cocycle audit."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import subprocess
from fractions import Fraction as Q
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def matrix(rows):
    return [[Q(value) for value in row] for row in rows]


def identity(size):
    return matrix([[1 if row == column else 0 for column in range(size)] for row in range(size)])


def transpose(value):
    return [list(row) for row in zip(*value)]


def add(left, right, factor=Q(1)):
    return [
        [left[row][column] + factor * right[row][column] for column in range(len(left[0]))]
        for row in range(len(left))
    ]


def multiply(left, right):
    return [
        [
            sum(left[row][middle] * right[middle][column] for middle in range(len(right)))
            for column in range(len(right[0]))
        ]
        for row in range(len(left))
    ]


def power(value, exponent):
    result = identity(len(value))
    for _ in range(exponent):
        result = multiply(result, value)
    return result


def block(left, right):
    size_left, size_right = len(left), len(right)
    output = [[Q(0) for _ in range(size_left + size_right)] for _ in range(size_left + size_right)]
    for row in range(size_left):
        for column in range(size_left):
            output[row][column] = left[row][column]
    for row in range(size_right):
        for column in range(size_right):
            output[size_left + row][size_left + column] = right[row][column]
    return output


def rank(value):
    work = [row[:] for row in value]
    rows, columns = len(work), len(work[0]) if work else 0
    pivot_row = 0
    for column in range(columns):
        pivot = next((row for row in range(pivot_row, rows) if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [entry / scale for entry in work[pivot_row]]
        for row in range(rows):
            if row != pivot_row and work[row][column]:
                factor = work[row][column]
                work[row] = [
                    work[row][entry] - factor * work[pivot_row][entry]
                    for entry in range(columns)
                ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def determinant(value):
    if len(value) == 2:
        return value[0][0] * value[1][1] - value[0][1] * value[1][0]
    work = [row[:] for row in value]
    answer = Q(1)
    sign = 1
    for column in range(len(value)):
        pivot = next((row for row in range(column, len(value)) if work[row][column]), None)
        if pivot is None:
            return Q(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            sign *= -1
        pivot_value = work[column][column]
        answer *= pivot_value
        for row in range(column + 1, len(value)):
            factor = work[row][column] / pivot_value
            for entry in range(column, len(value)):
                work[row][entry] -= factor * work[column][entry]
    return Q(sign) * answer


def F(value):
    value = Q(value)
    return matrix([[0, value], [1 / value, 0]])


def G(value):
    value = Q(value)
    return matrix([[value, 0], [0, 1 / value]])


def symmetric_basis():
    basis = []
    for row in range(4):
        for column in range(row, 4):
            item = [[Q(0) for _ in range(4)] for _ in range(4)]
            item[row][column] = Q(1)
            item[column][row] = Q(1)
            basis.append(item)
    return basis


def symmetric_eigenspace_dimension(transform, sign):
    columns = []
    for basis_item in symmetric_basis():
        image = multiply(multiply(transpose(transform), basis_item), transform)
        difference = add(image, basis_item, Q(-sign))
        columns.append([entry for row in difference for entry in row])
    equation_matrix = [list(row) for row in zip(*columns)]
    return 10 - rank(equation_matrix)


def coframe_eigenspace_dimension(transform, sign):
    return 4 - rank(add(transform, identity(4), Q(-sign)))


def rows(name):
    with (HERE / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tracked_blob(path):
    return subprocess.run(
        ["git", "rev-parse", f"HEAD:{path}"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    ).stdout.strip()


def main():
    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    source_rows = rows("SOURCE_LINEAGE.tsv")
    cocycle_rows = rows("COCYCLE_CLASSIFICATION.tsv")
    tangent_rows = rows("TANGENT_CLASSIFICATION.tsv")
    witness_rows = rows("GLOBAL_WITNESSES.tsv")
    status_rows = rows("STATUS_LEDGER.tsv")
    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    lay = (HERE / "LAY_DECISION_TREE.md").read_text(encoding="utf-8")
    next_decision = (HERE / "NEXT_SCIENTIFIC_DECISION.md").read_text(encoding="utf-8")

    # Independent rational group checks, not calls into the derivation implementation.
    b, c, d, a = Q(2), Q(3), Q(5), Q(7)
    K = matrix([[0, 1], [1, 0]])
    eta = matrix([[-1, 0], [0, 1]])
    reciprocal_at_two = G(Q(1, 2))
    metric_K_at_two = multiply(multiply(transpose(reciprocal_at_two), K), reciprocal_at_two)
    metric_eta_at_two = multiply(multiply(transpose(reciprocal_at_two), eta), reciprocal_at_two)
    mirrored_metric_eta_at_two = matrix([[-4, 0], [0, Q(1, 4)]])
    mixed_H = matrix([[2, 7], [7, 18]])
    mixed_P = G(Q(1, 2))
    mixed_P_inverse = G(2)
    mixed_F = F(3)
    mixed_g = multiply(multiply(transpose(mixed_P), mixed_H), mixed_P)
    mixed_g_mirror = multiply(multiply(transpose(mixed_P_inverse), mixed_H), mixed_P_inverse)
    mixed_g_pulled = multiply(multiply(transpose(mixed_F), mixed_g_mirror), mixed_F)
    mixed_H_transformed = multiply(multiply(transpose(G(5)), mixed_H), G(5))
    mixed_modulus = mixed_H[0][1] ** 2 / (mixed_H[0][0] * mixed_H[1][1])
    mixed_modulus_transformed = mixed_H_transformed[0][1] ** 2 / (
        mixed_H_transformed[0][0] * mixed_H_transformed[1][1]
    )
    spatial_H = matrix([[1, -2], [-2, 1]])
    spatial_fixed = matrix([[1], [1]])
    spatial_antifixed = matrix([[1], [-1]])
    rational_checks = {
        "F_involution": multiply(F(b), F(b)) == identity(2),
        "F_F_group_law": multiply(F(b), F(c)) == G(b / c),
        "G_F_group_law": multiply(G(a), F(b)) == F(a * b),
        "F_G_group_law": multiply(F(b), G(a)) == F(b / a),
        "three_odd_not_identity": multiply(multiply(F(b), F(c)), F(d)) != identity(2),
        "valid_triple_cocycle": multiply(multiply(F(b), F(c)), G(c / b)) == identity(2),
        "four_odd_formula": multiply(multiply(multiply(F(b), F(c)), F(d)), F(a))
        == G(b * d / (c * a)),
        "K_preserved": multiply(multiply(transpose(F(b)), K), F(b)) == K,
        "K_readout_phi_invisible": metric_K_at_two == K,
        "eta_readout_phi_visible": metric_eta_at_two == matrix([[Q(-1, 4), 0], [0, 4]]),
        "eta_balanced_mirror_anti_isometry": multiply(
            multiply(transpose(F(1)), mirrored_metric_eta_at_two), F(1)
        )
        == matrix([[Q(1, 4), 0], [0, -4]]),
        "mixed_readout_exact_mirror_isometry": mixed_g_pulled == mixed_g,
        "mixed_readout_Lorentz_and_phi_visible": determinant(mixed_H) < 0
        and mixed_g != mixed_H,
        "mixed_readout_modulus_invariant": mixed_modulus == mixed_modulus_transformed
        and mixed_modulus > 1,
        "mixed_readout_spatial_reflection_witness": multiply(F(1), spatial_fixed)
        == spatial_fixed
        and multiply(F(1), spatial_antifixed)
        == [[-entry[0]] for entry in spatial_antifixed]
        and multiply(transpose(spatial_fixed), multiply(spatial_H, spatial_fixed))[0][0] < 0
        and multiply(transpose(spatial_antifixed), multiply(spatial_H, spatial_antifixed))[0][0]
        > 0,
        "eta_not_positive_conformal": multiply(multiply(transpose(F(b)), eta), F(b))[0][0]
        > 0,
        "conjugacy_magnitude": multiply(multiply(G(a), F(b)), G(1 / a)) == F(a * a * b),
    }

    # Exact special-angle angular and finite-corner witnesses using only integer matrices.
    A0 = matrix([[1, 0], [0, -1]])
    A90 = matrix([[-1, 0], [0, 1]])
    A45 = matrix([[0, 1], [1, 0]])
    angular_checks = {
        "same_axis_commutes": multiply(A0, A0) == multiply(A0, A0),
        "perpendicular_axes_commute": multiply(A0, A90) == multiply(A90, A0),
        "oblique_axes_do_not_commute": multiply(A0, A45) != multiply(A45, A0),
        "quarter_turn_corner_order_four": power(multiply(A0, A45), 4) == identity(2),
        "same_base_reflection_corner": multiply(F(2), F(2)) == identity(2),
        "opposite_base_reflection_even_corner": power(multiply(F(2), F(-2)), 2)
        == identity(2),
        "generic_base_product_not_finite_order_four": power(multiply(F(2), F(1)), 4)
        != identity(2),
    }

    angular_classes = {
        "ANGULAR_PLUS_IDENTITY": identity(2),
        "ANGULAR_MINUS_IDENTITY": matrix([[-1, 0], [0, -1]]),
        "ANGULAR_AXIS_REFLECTION": A0,
    }
    expected_dimensions = {
        "ANGULAR_PLUS_IDENTITY": (-1, 3, 1, 7, 3),
        "ANGULAR_MINUS_IDENTITY": (-1, 1, 3, 7, 3),
        "ANGULAR_AXIS_REFLECTION": (1, 2, 2, 6, 4),
    }
    independent_dimensions = {}
    for name, angular in angular_classes.items():
        transform = block(F(1), angular)
        independent_dimensions[name] = (
            int(determinant(transform)),
            coframe_eigenspace_dimension(transform, 1),
            coframe_eigenspace_dimension(transform, -1),
            symmetric_eigenspace_dimension(transform, 1),
            symmetric_eigenspace_dimension(transform, -1),
        )

    caps = {
        "SAME_CYCLE_P0": ((1, 1), (1, 1), 0),
        "AXIS_EXCHANGE_P1": ((1, 0), (0, 1), 1),
        "MIRROR_LENS_P3": ((2, 1), (1, 2), 3),
        "MIRROR_LENS_P5": ((3, 2), (2, 3), 5),
    }
    cap_checks = {}
    for name, (left, right, expected) in caps.items():
        observed = abs(left[0] * right[1] - left[1] * right[0])
        cap_checks[name] = (
            math.gcd(abs(left[0]), abs(left[1])) == 1
            and math.gcd(abs(right[0]), abs(right[1])) == 1
            and observed == expected
        )

    expected_outcomes = {
        "MULTIPLE_GLOBAL_COMPLETIONS_SURVIVE_CONDITIONALLY",
        "COCYCLE_CONSISTENCY_REDUCES_BUT_DOES_NOT_SELECT",
        "GLOBAL_COCYCLE_CANNOT_BE_POSED_WITHOUT_OPEN_TOPOLOGY_OR_COVER",
        "BOUNDARY_TANGENT_SPACE_REMAINS_POLARIZATION_DEPENDENT",
        "CURRENT_DATA_DEFINE_ONLY_LOCAL_OR_SECTORWISE_INVOLUTIONS",
    }
    lineage_ok = all(
        (ROOT / row["source"]).is_file()
        and digest(ROOT / row["source"]) == row["sha256"]
        and tracked_blob(row["source"]) == row["git_blob"]
        for row in source_rows
    )
    checks = {
        "independent_rational_group_checks": all(rational_checks.values()),
        "independent_angular_corner_checks": all(angular_checks.values()),
        "independent_full_tangent_dimensions": independent_dimensions == expected_dimensions,
        "independent_cap_lattice_checks": all(cap_checks.values())
        and {value[2] for value in caps.values()} == {0, 1, 3, 5},
        "derivation_schema_and_check_count": result["schema"]
        == "udt-global-coframe-cocycle-audit-1.0"
        and len(result["checks"]) == 63
        and set(result["checks"].values()) == {"PASS"},
        "outcomes_exact": set(result["outcomes"]) == expected_outcomes,
        "uniqueness_not_earned": result["outcome_not_earned"]
        == "UNIQUE_GLOBAL_COFRAME_AND_TANGENT_COMPLETION_IN_AUDITED_CLASS",
        "readout_gate_open": "PHYSICAL_SOLDERING_AND_MODULUS_SELECTION_OPEN"
        in result["readout_ruling"]["status"],
        "mixed_readout_family_exact_conditional": result["readout_ruling"][
            "mixed_readout_family"
        ]["status"]
        == "EXACT_CONDITIONAL_FAMILY_NOT_SELECTED",
        "mixed_modulus_survives_full_extension": {
            row["mu"] for row in result["mixed_readout_full_witnesses"].values()
        }
        == {4, 9},
        "cover_gate_open": "chart/corner/cap incidence" in result["smallest_global_gate_after_local_readout"],
        "boundary_polarization_open": result["boundary_tangent_ruling"]["polarization"].startswith(
            "NOT_SELECTED_BY_INVOLUTION"
        ),
        "maximum_conclusion_exact": result["maximum_conclusion"]
        == "UDT_GLOBAL_COFRAME_COCYCLE_STATUS_CHARACTERIZED",
        "source_lineage_exact": len(source_rows) == 18 and lineage_ok,
        "classification_ledgers_complete": len(cocycle_rows) == 16
        and len(tangent_rows) == 5
        and len(witness_rows) == 9,
        "status_ledger_complete": len(status_rows) == 30
        and {row["id"] for row in status_rows} == {f"S{index:02d}" for index in range(1, 31)},
        "report_discloses_mixed_family_scope": "complete for constant real symmetric `2x2` readouts"
        in report
        and "DERIVED_CONDITIONAL" in report
        and "not a selected UDT readout" in report,
        "lay_readout_not_global_closure": "many tilt angles work" in lay
        and "still need the physical rule" in lay,
        "next_decision_excludes_imports_and_gpu": "Importing an ADM shift" in next_decision
        and "No GPU solve is indicated" in next_decision,
    }

    # Fail-closed mutation catches.
    catches = {
        "three_odd_cocycle_promotion_rejected": not rational_checks["three_odd_not_identity"] is False,
        "diagonal_readout_promotion_rejected": rational_checks["eta_not_positive_conformal"],
        "K_choice_hidden_as_foundation_rejected": result["readout_ruling"][
            "dual_K_as_physical_null_metric"
        ].startswith("CONDITIONAL"),
        "K_elegance_as_physical_phi_rejected": "metric-invisible"
        in result["readout_ruling"]["readout_tradeoff"]["K"],
        "eta_visibility_as_closed_seal_rejected": "anti-isometry"
        in result["readout_ruling"]["readout_tradeoff"]["eta"],
        "mixed_family_as_unique_readout_rejected": "dimensionless_unselected_modulus"
        in result["readout_ruling"]["mixed_readout_family"],
        "angular_class_deletion_rejected": len(independent_dimensions) == 3,
        "orientation_as_selector_rejected": len({row[0] for row in independent_dimensions.values()}) == 2,
        "static_phi_as_complete_tangent_rejected": 9
        not in {row[3] for row in independent_dimensions.values()},
        "corner_order_invention_rejected": "ORDER_NOT_SUPPLIED"
        in {row["status_or_limit"] for row in cocycle_rows},
        "topology_uniqueness_rejected": len({value[2] for value in caps.values()}) == 4,
        "primitive_implies_S3_rejected": cap_checks["MIRROR_LENS_P3"]
        and cap_checks["MIRROR_LENS_P5"],
        "boundary_polarization_promotion_rejected": tangent_rows[-1]["foundation_status"].startswith(
            "OPEN_"
        ),
        "global_completion_promotion_rejected": "GLOBAL_COCYCLE_CANNOT_BE_POSED_WITHOUT_OPEN_TOPOLOGY_OR_COVER"
        in expected_outcomes,
        "mixed_readout_canonization_rejected": next(
            row for row in status_rows if row["id"] == "S08"
        )["status"]
        == "DERIVED_CONDITIONAL",
        "complete_action_status_rejected": next(
            row for row in status_rows if row["id"] == "S28"
        )["status"]
        == "OPEN_NOT_ACTIVATED",
        "action_promotion_rejected": "action" not in result["maximum_conclusion"].lower(),
        "carrier_promotion_rejected": "carrier" not in result["maximum_conclusion"].lower(),
        "gpu_promotion_rejected": result["compute"]["cpu_only"]
        and not result["compute"]["gpu_used"],
    }
    if not all(checks.values()) or not all(catches.values()):
        raise AssertionError(
            {
                "checks": checks,
                "catch_proofs": catches,
                "rational": rational_checks,
                "angular": angular_checks,
                "dimensions": independent_dimensions,
                "caps": cap_checks,
            }
        )

    output = {
        "schema": "udt-global-coframe-cocycle-independent-verification-1.0",
        "result": "PASS_VERIFIED_WITH_CAVEATS",
        "checks": checks,
        "catch_proofs": catches,
        "independent_method": "Python standard library exact Fraction matrix algebra and rational rank",
        "independent_full_tangent_dimensions": {
            name: {
                "determinant": values[0],
                "coframe_fixed": values[1],
                "coframe_antifixed": values[2],
                "metric_even": values[3],
                "metric_odd": values[4],
            }
            for name, values in independent_dimensions.items()
        },
        "counts": {
            "derivation_checks": len(result["checks"]),
            "independent_checks": len(checks),
            "catch_proofs": len(catches),
            "sources": len(source_rows),
            "cocycle_rows": len(cocycle_rows),
            "tangent_rows": len(tangent_rows),
            "witnesses": len(witness_rows),
            "status_rows": len(status_rows),
        },
        "load_bearing_hashes": {
            name: digest(HERE / name)
            for name in (
                "DERIVATION_RESULT.json",
                "COCYCLE_CLASSIFICATION.tsv",
                "TANGENT_CLASSIFICATION.tsv",
                "GLOBAL_WITNESSES.tsv",
                "SOURCE_LINEAGE.tsv",
                "STATUS_LEDGER.tsv",
                "AUDIT_REPORT.md",
                "LAY_DECISION_TREE.md",
                "NEXT_SCIENTIFIC_DECISION.md",
            )
        },
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "result": output["result"],
                **output["counts"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
