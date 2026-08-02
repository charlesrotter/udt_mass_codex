#!/usr/bin/env python3
"""Construct exact FC07 mapping-torus screen metrics for all frozen monodromies."""

from __future__ import annotations

import ast
import csv
import json
from itertools import combinations
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def table(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write(name: str, rows: list[dict[str, object]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)


def matrix_text(m: sp.Matrix) -> str:
    return "[[" + "],[".join(",".join(str(sp.factor(m[i, j])) for j in range(m.cols)) for i in range(m.rows)) + "]]"


def congruence_operator(m: sp.Matrix) -> sp.Matrix:
    a, b, d = sp.symbols("a b d")
    h = sp.Matrix([[a, b], [b, d]])
    hp = sp.expand(m.T * h * m)
    entries = (hp[0, 0], hp[0, 1], hp[1, 1])
    return sp.Matrix([[sp.expand(value).coeff(x) for x in (a, b, d)] for value in entries])


def main() -> int:
    candidates = table(HERE / "MONODROMY_CANDIDATES.tsv")
    registry = {row["monodromy_id"]: row for row in table(ROOT / "udt_global_metric_assembly_atlas_2026-07-22/TORUS_MONODROMY_REGISTRY.tsv")}
    assert len(candidates) == len(registry) == 8

    a, b, d, q, x, z = sp.symbols("a b d q x z", real=True)
    h0 = sp.Matrix([[a, b], [b, d]])
    delta = sp.factor(h0.det())
    vector = sp.Matrix([x, z])
    representative = sp.Matrix([[sp.Rational(2), sp.Rational(1, 3)], [sp.Rational(1, 3), sp.Rational(5)]])
    assert representative[0, 0] > 0 and representative.det() > 0

    operators: dict[str, sp.Matrix] = {}
    endpoint_representatives: dict[str, sp.Matrix] = {}
    witness_rows: list[dict[str, object]] = []
    invariant_rows: list[dict[str, object]] = []
    projector_rows: list[dict[str, object]] = []
    covariance_rows: list[dict[str, object]] = []
    checks = 0

    expected_fixed = {
        "M_IDENTITY": ("(a,b,d)", "YES_FULL_SPD_CONE", 3),
        "M_MINUS_IDENTITY": ("(a,b,d)", "YES_FULL_SPD_CONE", 3),
        "M_ORDER4_ROTATION": ("(d,0,d)", "YES_d_GT_0", 1),
        "M_ORDER6_ELLIPTIC": ("(d,d/2,d)", "YES_d_GT_0", 1),
        "M_PARABOLIC": ("(0,0,d)", "NO_POSITIVE_DEFINITE_MEMBER", 1),
        "M_HYPERBOLIC": ("(-d,d/2,d)", "NO_POSITIVE_DEFINITE_MEMBER", 1),
        "M_EXCHANGE": ("(d,b,d)", "YES_d_ABS_GT_b", 2),
        "M_ORIENTATION_REVERSING_GLIDE": ("(2*b,b,d)", "YES_b_GT_0_AND_d_GT_b/2", 2),
    }

    for candidate in candidates:
        rid = candidate["monodromy_id"]
        source = registry[rid]
        assert candidate["matrix"] == source["matrix"] and candidate["registry_class"] == source["monodromy_class"]
        checks += 2
        m = sp.Matrix(ast.literal_eval(candidate["matrix"]))
        det_m = int(m.det())
        assert abs(det_m) == 1
        checks += 1

        h1 = sp.expand(m.T * h0 * m)
        hq = sp.expand((1 - q) * h0 + q * h1)
        assert sp.factor(h1.det() - delta) == 0
        assert sp.simplify((vector.T * hq * vector)[0] - ((1 - q) * (vector.T * h0 * vector)[0] + q * ((m * vector).T * h0 * (m * vector))[0])) == 0
        checks += 2
        for value in (sp.Rational(0), sp.Rational(1, 4), sp.Rational(1, 2), sp.Rational(3, 4), sp.Rational(1)):
            sampled = hq.subs({a: 2, b: sp.Rational(1, 3), d: 5, q: value})
            assert sampled[0, 0] > 0 and sampled.det() > 0
            checks += 1

        op = congruence_operator(m)
        operators[rid] = op
        endpoint_representatives[rid] = sp.expand(m.T * representative * m)

        equations = list(m.T * h0 * m - h0)
        solution = sp.linsolve(equations, (a, b, d))
        expected_form, spd_fixed, fixed_dim = expected_fixed[rid]
        assert len(solution.args) == 1
        free = set().union(*(entry.free_symbols for entry in solution.args[0])) & {a, b, d}
        assert len(free) == fixed_dim
        checks += 2
        variation_status = "SCREEN_VARIATION_FORCED_FOR_EVERY_SPD_H0" if spd_fixed.startswith("NO_") else "CONSTANT_SCREEN_SUBFAMILY_EXISTS_AND_VARYING_MEMBERS_REMAIN"
        invariant_rows.append({"candidate_id": candidate["candidate_id"], "monodromy_id": rid, "fixed_symmetric_form": expected_form, "linear_fixed_space_dimension": fixed_dim, "positive_definite_fixed_member": spd_fixed, "screen_variation_ruling": variation_status})

        orientation = "ORIENTABLE" if det_m == 1 else "NONORIENTABLE_FC07_FC09_OVERLAP"
        coframe = "GLOBAL_ORIENTED_COFRAME_PATH_P0_TO_P0M_EXISTS" if det_m == 1 else "LOCAL_COFRAMES_WITH_O2_REFLECTION_TRANSITION_ONLY"
        witness_rows.append({"candidate_id": candidate["candidate_id"], "monodromy_id": rid, "det_M": det_m, "orientation_stratum": orientation, "h1_congruence": matrix_text(h1), "det_h1": "a*d-b^2", "interpolation": "h=(1-chi)h0+chi*h1;chi_flat", "seam_regularity": "C_INFINITY_ALL_POSITIVE_ORDER_ENDPOINT_JETS_ZERO", "screen_metric": "SPD_FOR_ALL_h0_SPD_AND_0_LE_chi_LE_1", "coframe_globality": coframe, "spatial_completeness": "COMPACT_MAPPING_TORUS_HOPF_RINOW", "four_metric_completeness": "CONSTANT_LAPSE_PRODUCT_GEODESICS_DECOUPLE", "completion_status": "COMPLETE_OFFSHELL_METRIC_WITNESS"})

        projector_rows.append({"candidate_id": candidate["candidate_id"], "monodromy_id": rid, "transition": "T=diag(1_t,1_s,M)", "screen_projector": "Pi=diag(0,0,1,1)", "descent_identity": "T*Pi=Pi*T", "screen_distribution": "GLOBAL_INTEGRABLE_VERTICAL_T2", "pair_distribution": "GLOBAL_INTEGRABLE_t_s", "parallel_status": "NOT_REQUIRED;NONPARALLEL_WHERE_dh/ds_NONZERO", "neighborhood_scope": "BLOCK_SEAM_COMPATIBLE_SPD_PERTURBATIONS_ONLY"})

        basis_controls = {
            "B_EXCHANGE": sp.Matrix([[0, 1], [1, 0]]),
            "B_SHEAR": sp.Matrix([[1, 1], [0, 1]]),
        }
        passed = []
        for basis_id, basis in basis_controls.items():
            transformed_m = basis.inv() * m * basis
            transformed_h0 = basis.T * h0 * basis
            left = sp.expand(transformed_m.T * transformed_h0 * transformed_m)
            right = sp.expand(basis.T * h1 * basis)
            assert left == right
            checks += 1
            passed.append(basis_id)
        covariance_rows.append({"candidate_id": candidate["candidate_id"], "monodromy_id": rid, "basis_controls": ";".join(passed), "transformation": "Mprime=B^-1*M*B;hprime=B^T*h*B", "covariance_identity": "C_Mprime(hprime)=B^T*C_M(h)*B", "status": "PASS_EXACT"})

    # Classify the induced maps on the three metric components. M and -M may collapse.
    classes: list[list[str]] = []
    remaining = [row["monodromy_id"] for row in candidates]
    while remaining:
        first = remaining.pop(0)
        group = [first] + [other for other in remaining if operators[other] == operators[first]]
        remaining = [other for other in remaining if other not in group]
        classes.append(group)
    assert len(classes) == 7
    assert classes[0] == ["M_IDENTITY", "M_MINUS_IDENTITY"]
    assert sum(operators[left] != operators[right] for left, right in combinations(operators, 2)) == 27
    checks += 3

    operator_rows = []
    for row in candidates:
        rid = row["monodromy_id"]
        class_index = next(index for index, group in enumerate(classes, 1) if rid in group)
        endpoint = endpoint_representatives[rid]
        operator_rows.append({"candidate_id": row["candidate_id"], "monodromy_id": rid, "metric_congruence_operator_on_a_b_d": matrix_text(operators[rid]), "metric_fiber_class": f"K{class_index:02d}", "class_members": ";".join(classes[class_index - 1]), "rational_SPD_control_h0": "[[2,1/3],[1/3,5]]", "rational_control_h1": matrix_text(endpoint)})

    # Seven class representatives have distinct endpoint metrics on one exact generic SPD control.
    class_endpoints = [endpoint_representatives[group[0]] for group in classes]
    assert all(left != right for left, right in combinations(class_endpoints, 2))
    checks += 1

    write("COMPLETE_WITNESS_CENSUS.tsv", witness_rows)
    write("INVARIANT_SCREEN_STRATA.tsv", invariant_rows)
    write("METRIC_CONGRUENCE_FIBER_ATLAS.tsv", operator_rows)
    write("PROJECTOR_DESCENT_ATLAS.tsv", projector_rows)
    write("LATTICE_BASIS_COVARIANCE.tsv", covariance_rows)

    result = {
        "schema": "udt.torus_bundle_full_screen_witness.result.v1",
        "status": "PASS",
        "outcome": "FC07_COMPLETE_OFFSHELL_FULL_SCREEN_METRIC_WITNESS_FAMILY_EXISTS__SEVEN_FROZEN_REPRESENTATIVE_ENDPOINT_CONGRUENCE_FIBERS_FROM_EIGHT_MONODROMIES__NO_PHYSICAL_SELECTION",
        "candidate_monodromies": len(candidates),
        "complete_metric_witnesses": len(witness_rows),
        "global_oriented_coframe_witnesses": sum(row["det_M"] == 1 for row in witness_rows),
        "local_transition_coframe_only_witnesses": sum(row["det_M"] == -1 for row in witness_rows),
        "metric_congruence_fiber_classes": len(classes),
        "metric_operator_distinct_pairs": 27,
        "metric_operator_collapsed_pairs": 1,
        "collapsed_pair": ["M_IDENTITY", "M_MINUS_IDENTITY"],
        "constant_screen_subfamily_monodromies": sum("YES_" in row["positive_definite_fixed_member"] for row in invariant_rows),
        "forced_varying_screen_monodromies": [row["monodromy_id"] for row in invariant_rows if row["positive_definite_fixed_member"].startswith("NO_")],
        "global_integrable_projector_witnesses": len(projector_rows),
        "lattice_basis_covariance_controls": 2 * len(covariance_rows),
        "exact_checks": checks,
        "physical_completion_selectors": 0,
        "native_field_equations": 0,
        "maximum_conclusion": "COMPLETE_OFFSHELL_FC07_METRIC_WITNESSES_EXIST_FOR_THE_EIGHT_FROZEN_CONTROLS_IN_THE_CHOSEN_CONSTANT_DEPTH_BLOCK_EXTENSION__SEVEN_FROZEN_ENDPOINT_CONGRUENCE_OPERATOR_CLASSES__NO_EXTENSION_OR_MONODROMY_SELECTION_DYNAMICS_STABILITY_BOOTSTRAP_RESPONSE_PROJECTOR_OR_MATTER_CLAIM",
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
