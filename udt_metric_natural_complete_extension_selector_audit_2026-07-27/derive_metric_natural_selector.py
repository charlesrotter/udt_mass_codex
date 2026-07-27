#!/usr/bin/env python3
"""Exact controls and complete frozen-candidate selector classification."""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def read_tsv(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(name: str, rows: list[dict[str, object]], fields: list[str]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def symmetric_entries(matrix: sp.Matrix) -> list[sp.Expr]:
    return [sp.expand(matrix[i, j]) for i in range(matrix.rows) for j in range(i, matrix.cols)]


def coefficient_rank(expressions: list[sp.Expr], variables: list[sp.Symbol]) -> int:
    rows = [[sp.expand(expr).coeff(var) for var in variables] for expr in expressions]
    return int(sp.Matrix(rows).rank())


def lorentz_generators(eta: sp.Matrix) -> dict[str, sp.Matrix]:
    result: dict[str, sp.Matrix] = {}
    for a in range(4):
        for b in range(a + 1, 4):
            generator = sp.zeros(4)
            generator[a, b] = 1
            generator[b, a] = -eta[a, a] / eta[b, b]
            assert generator.T * eta + eta * generator == sp.zeros(4)
            result[f"L{a}{b}"] = generator
    return result


def solve_zero_parameter(matrix: sp.Matrix, parameter: sp.Symbol) -> list[str]:
    equations = [sp.factor(value) for value in matrix if value != 0]
    if not equations:
        return ["ALL"]
    solution = sp.solve(equations, [parameter], dict=True)
    return [str(item[parameter]) for item in solution if parameter in item]


def solve_linear_tuple(expressions: list[sp.Expr], variables: list[sp.Symbol]) -> list[list[str]]:
    """Return a stable exact representation of a linear solution set."""
    solution = sp.linsolve(expressions, variables)
    if solution is sp.EmptySet:
        return []
    return [[str(sp.simplify(value)) for value in item] for item in solution]


def primitive_unoriented(vector: tuple[int, int]) -> tuple[int, int]:
    p, q = vector
    if p < 0 or (p == 0 and q < 0):
        p, q = -p, -q
    return p, q


def shortest_forms(form, bound: int = 3) -> list[tuple[int, int]]:
    values: dict[tuple[int, int], sp.Expr] = {}
    for p in range(-bound, bound + 1):
        for q in range(-bound, bound + 1):
            if (p, q) == (0, 0) or sp.gcd(p, q) != 1:
                continue
            w = primitive_unoriented((p, q))
            values[w] = sp.simplify(form(*w))
    minimum = min(values.values(), key=lambda value: float(value))
    return sorted(w for w, value in values.items() if sp.simplify(value - minimum) == 0)


def exact_controls() -> dict[str, object]:
    eta = sp.diag(-1, 1, 1, 1)
    c00, c01, c10, c11, k00, k10, k11 = sp.symbols("c00 c01 c10 c11 k00 k10 k11")
    variables = [c00, c01, c10, c11, k00, k10, k11]
    X = sp.Matrix(
        [
            [-1, 0, 0, 0],
            [0, 1, 0, 0],
            [c00, c01, k00, 0],
            [c10, c11, k10, k11],
        ]
    )
    metric_tangent = X.T * eta + eta * X
    physical_rank = coefficient_rank(symmetric_entries(metric_tangent), variables)
    determinant_rank = coefficient_rank([sp.trace(X)], variables)
    transverse = X[2:4, 2:4]
    transverse_rank = coefficient_rank(symmetric_entries(transverse.T + transverse), variables)
    mixing_rank = coefficient_rank(list(X[2:4, 0:2]), variables)
    both_rank = coefficient_rank(
        symmetric_entries(transverse.T + transverse) + list(X[2:4, 0:2]), variables
    )

    generators = lorentz_generators(eta)
    mvars = sp.symbols("m0:16")
    M = sp.Matrix(4, 4, mvars)
    commutator_expressions: list[sp.Expr] = []
    for generator in generators.values():
        commutator_expressions.extend(list(M * generator - generator * M))
    commutant_rank = coefficient_rank(commutator_expressions, list(mvars))
    commutant_dimension = 16 - commutant_rank

    lam = sp.symbols("lambda", real=True)
    Xlam = sp.diag(-1, 1, lam, lam)
    holonomy_solutions = {
        "screen_rotation_L23": solve_zero_parameter(Xlam * generators["L23"] - generators["L23"] * Xlam, lam),
        "spatial_mix_L12": solve_zero_parameter(Xlam * generators["L12"] - generators["L12"] * Xlam, lam),
        "spatial_mix_L13": solve_zero_parameter(Xlam * generators["L13"] - generators["L13"] * Xlam, lam),
        "boost_mix_L02": solve_zero_parameter(Xlam * generators["L02"] - generators["L02"] * Xlam, lam),
        "boost_mix_L03": solve_zero_parameter(Xlam * generators["L03"] - generators["L03"] * Xlam, lam),
        "base_boost_L01": solve_zero_parameter(Xlam * generators["L01"] - generators["L01"] * Xlam, lam),
    }
    swap = sp.Matrix([[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    odd_solutions = solve_zero_parameter(swap * Xlam * swap.inv() + Xlam, lam)

    def commutator_constraints(names: list[str]) -> list[list[str]]:
        expressions = []
        for name in names:
            expressions.extend(list(X * generators[name] - generators[name] * X))
        return solve_linear_tuple(expressions, variables)

    full_extension_holonomy = {
        "screen_SO2_L23": commutator_constraints(["L23"]),
        "spatial_SO3_L12_L13_L23": commutator_constraints(["L12", "L13", "L23"]),
        "lorentz_SOplus12_L02_L03_L23": commutator_constraints(["L02", "L03", "L23"]),
        "base_boost_L01": commutator_constraints(["L01"]),
        "full_lorentz": commutator_constraints(list(generators)),
        "twisted_reciprocal_swap_odd": solve_linear_tuple(list(swap * X * swap.inv() + X), variables),
    }
    swap_is_lorentz = swap.T * eta * swap == eta

    timelike = sp.Matrix([1, 0, 0, 0])
    spacelike = sp.Matrix([0, 1, 0, 0])
    null = sp.Matrix([1, 1, 0, 0])

    def projector(vector: sp.Matrix):
        norm = (vector.T * eta * vector)[0]
        if norm == 0:
            return norm, None
        covector = vector.T * eta
        value = sp.simplify(vector * covector / norm)
        return norm, value

    time_norm, time_projector = projector(timelike)
    space_norm, space_projector = projector(spacelike)
    null_norm, null_projector = projector(null)

    simple_ricci_pairings = 3
    ricci_degenerate_pairings = "UNSELECTED_CONTINUUM"
    ricci_complex_control = sp.Matrix(
        [[0, 1, 0, 0], [-1, 0, 0, 0], [0, 0, 2, 0], [0, 0, 0, 3]]
    )
    ricci_complex_is_eta_self_adjoint = ricci_complex_control.T * eta == eta * ricci_complex_control
    ricci_complex_charpoly = sp.factor(ricci_complex_control.charpoly().as_expr())
    ricci_complex_eigenvalues = sorted(
        (str(value) for value in ricci_complex_control.eigenvals()), key=str
    )
    zero_bivector_eigenspace_dimension = 6
    angular_round_shortest = shortest_forms(lambda p, q: p * p + q * q)
    angular_hex_shortest = shortest_forms(lambda p, q: p * p - p * q + q * q)
    seal_generator_independence = sp.exp(0 * X) == sp.eye(4)

    assert physical_rank == 7
    assert determinant_rank == 1
    assert transverse_rank == 3
    assert mixing_rank == 4
    assert both_rank == 7
    assert commutant_rank == 15 and commutant_dimension == 1
    assert holonomy_solutions["screen_rotation_L23"] == ["ALL"]
    assert holonomy_solutions["spatial_mix_L12"] == ["1"]
    assert holonomy_solutions["spatial_mix_L13"] == ["1"]
    assert holonomy_solutions["boost_mix_L02"] == ["-1"]
    assert holonomy_solutions["boost_mix_L03"] == ["-1"]
    assert holonomy_solutions["base_boost_L01"] == []
    assert odd_solutions == ["0"]
    assert full_extension_holonomy["screen_SO2_L23"] == [["0", "0", "0", "0", "k11", "0", "k11"]]
    assert full_extension_holonomy["spatial_SO3_L12_L13_L23"] == [["0", "0", "0", "0", "1", "0", "1"]]
    assert full_extension_holonomy["lorentz_SOplus12_L02_L03_L23"] == [["0", "0", "0", "0", "-1", "0", "-1"]]
    assert full_extension_holonomy["base_boost_L01"] == []
    assert full_extension_holonomy["full_lorentz"] == []
    assert full_extension_holonomy["twisted_reciprocal_swap_odd"] == [["-c01", "c01", "-c11", "c11", "0", "0", "0"]]
    assert not swap_is_lorentz
    assert time_norm == -1 and time_projector * time_projector == time_projector
    assert space_norm == 1 and space_projector * space_projector == space_projector
    assert null_norm == 0 and null_projector is None
    assert len(angular_round_shortest) == 2
    assert len(angular_hex_shortest) == 3
    assert seal_generator_independence
    assert ricci_complex_is_eta_self_adjoint
    assert ricci_complex_charpoly == (sp.Symbol("lambda") - 3) * (sp.Symbol("lambda") - 2) * (sp.Symbol("lambda") ** 2 + 1)

    return {
        "extension_physical_tangent_rank": physical_rank,
        "determinant_one_constraint_rank": determinant_rank,
        "transverse_metric_constraint_rank": transverse_rank,
        "no_mixing_constraint_rank": mixing_rank,
        "joint_spectator_constraint_rank": both_rank,
        "full_lorentz_commutant_constraint_rank": commutant_rank,
        "full_lorentz_commutant_dimension": commutant_dimension,
        "holonomy_lambda_solutions": holonomy_solutions,
        "reciprocal_swap_odd_lambda_solutions": odd_solutions,
        "full_extension_variable_order": [str(value) for value in variables],
        "full_extension_holonomy_solutions": full_extension_holonomy,
        "reciprocal_swap_is_lorentz": swap_is_lorentz,
        "nonnull_projector_idempotent": True,
        "null_projector_undefined": True,
        "simple_ricci_clock_spatial_pairings_on_real_Segre_1_111_stratum": simple_ricci_pairings,
        "ricci_complex_control_is_eta_self_adjoint": ricci_complex_is_eta_self_adjoint,
        "ricci_complex_control_charpoly": str(ricci_complex_charpoly),
        "ricci_complex_control_eigenvalues": ricci_complex_eigenvalues,
        "repeated_ricci_pairing_status": ricci_degenerate_pairings,
        "zero_weyl_or_riemann_bivector_eigenspace_dimension": zero_bivector_eigenspace_dimension,
        "round_torus_shortest_unoriented_lines": [list(item) for item in angular_round_shortest],
        "hexagonal_torus_shortest_unoriented_lines": [list(item) for item in angular_hex_shortest],
        "seal_exp_zero_is_identity_for_all_extensions": True,
    }


G = {
    "C01": ["PASS", "PASS", "PARTIAL_PAIR_ONLY", "FAIL_INCOMPLETE_BASE", "PASS_BASE", "PASS_BASE", "PASS", "FAIL_SEVEN_PARAMETERS_OPEN", "NOT_APPLICABLE", "NOT_APPLICABLE", "FAIL_NO_COMPLETE_DESCENT", "FAIL_NO_COMPLETE_TRANSITION", "FAIL_NO_COMPLETION", "PASS", "PASS_BASE_ONLY", "OPEN_SEPARATE_GATE"],
    "C02": ["PASS", "PASS", "FAIL_NO_ACTIVE_AUTHORITY", "FAIL_LINE_NOT_EXTENSION", "PASS_SETWISE", "PASS_SETWISE", "FAIL_RULER_AND_EXTENSION_UNSELECTED", "PASS_SCOPED_UNIQUE_K_LINE", "FAIL_SYMMETRY_ENHANCEMENT", "NOT_APPLICABLE", "FAIL_GENERIC_HOLONOMY", "OPEN", "FAIL_NOT_ALL_COMPLETIONS", "PARTIAL", "PASS_SCOPED_NO_SPLICE", "OPEN_SEPARATE_GATE"],
    "C03": ["PASS", "PASS_CONDITIONAL_ON_REALIZED_DPHI", "FAIL_NO_ACTIVE_AUTHORITY", "FAIL_LINE_SPLIT_NOT_ORDERED_PAIR", "PASS_NONNULL_STRATA", "PASS_NONNULL_STRATA", "FAIL_COMPLEMENT_CHARACTER_CHOSEN", "PASS_NONNULL_LINE_ONLY", "FAIL_ZERO_STRATUM", "FAIL_NULL_ZERO_TYPE_CHANGE", "OPEN", "OPEN", "FAIL_NOT_ALL_COMPLETIONS", "PARTIAL", "PASS_SCOPED_NO_SPLICE", "OPEN_SEPARATE_GATE"],
    "C04": ["PASS", "PASS", "FAIL_NO_ACTIVE_AUTHORITY", "FAIL_EIGENLINES_NOT_EXTENSION", "PASS_SETWISE_ON_REAL_DIAGONALIZABLE_STRATUM", "PASS_SETWISE_ON_REAL_DIAGONALIZABLE_STRATUM", "FAIL_PAIRING_PRIORITY_UNSELECTED", "FAIL_THREE_PAIRINGS_ONLY_ON_REAL_SEGRE_1_111_STRATUM", "FAIL_COMPLEX_REPEATED_AND_EINSTEIN_STRATA", "OPEN_TYPE_CHANGE", "OPEN", "OPEN", "FAIL_NOT_ALL_COMPLETIONS", "PARTIAL", "PASS_SCOPED_NO_SPLICE", "OPEN_SEPARATE_GATE"],
    "C05": ["PASS", "PASS", "FAIL_NO_ACTIVE_AUTHORITY", "FAIL_BIVECTOR_PLANES_NOT_EXTENSION", "PASS_SETWISE", "PASS_SETWISE", "FAIL_PRINCIPAL_MEMBER_AND_ROLE_UNSELECTED", "PARTIAL_ALGEBRAICALLY_GENERAL_ONLY", "FAIL_REPEATED_OR_CONFORMALLY_FLAT", "OPEN_TYPE_CHANGE", "OPEN", "OPEN", "FAIL_NOT_ALL_COMPLETIONS", "PARTIAL", "PASS_SCOPED_NO_SPLICE", "OPEN_SEPARATE_GATE"],
    "C06": ["PASS", "PASS", "FAIL_NO_ACTIVE_AUTHORITY", "FAIL_BIVECTOR_OPERATOR_NOT_EXTENSION", "PASS_SETWISE", "PASS_SETWISE", "FAIL_REDUCTION_PRIORITY_UNSELECTED", "PARTIAL_SIMPLE_OPERATOR_ONLY", "FAIL_DEGENERATE_OR_FLAT", "OPEN_TYPE_CHANGE", "FAIL_FULL_HOLONOMY_CONTROL", "OPEN", "FAIL_NOT_ALL_COMPLETIONS", "PARTIAL", "PASS_SCOPED_NO_SPLICE", "OPEN_SEPARATE_GATE"],
    "C07": ["PASS", "PARTIAL_SUPPLIED_ANGULAR_SPLIT", "FAIL_NO_ACTIVE_AUTHORITY", "FAIL_AXES_NOT_COMPLETE_EXTENSION", "PARTIAL_SPLIT_DEPENDENT", "PARTIAL_SPLIT_DEPENDENT", "FAIL_BASE_SCREEN_SPLIT_AND_ORIENTATION_UNSELECTED", "PASS_SIMPLE_SPECTRUM_AXES_ONLY", "FAIL_ROUND_TIE_AND_WALL", "NOT_APPLICABLE", "FAIL_MONODROMY_CAN_EXCHANGE_AXES", "PARTIAL", "FAIL_NOT_ALL_COMPLETIONS", "PARTIAL", "PASS_SCOPED_NO_SPLICE", "OPEN_SEPARATE_GATE"],
    "C08": ["PASS", "PASS_CONDITIONAL_ON_SOLDERED_PAIR_OR_NONNULL_DPHI", "FAIL_NO_ACTIVE_AUTHORITY", "FAIL_PROJECTOR_NOT_COMPLETE_EXTENSION", "PASS_WHERE_DEFINED", "PASS_WHERE_DEFINED", "FAIL_INPUT_PROJECTOR_OR_SOLDER_ALREADY_CHOSEN", "PARTIAL_LINE_OR_PLANE_ONLY", "FAIL_ZERO_OR_TIE", "FAIL_NULL_ZERO_TYPE_CHANGE", "OPEN", "OPEN", "FAIL_NOT_ALL_COMPLETIONS", "PASS_BASE", "PASS_SCOPED_NO_SPLICE", "OPEN_SEPARATE_GATE"],
    "C09": ["PASS", "PARTIAL_REQUIRES_INTEGRAL_TORUS_LATTICE", "FAIL_NO_ACTIVE_AUTHORITY", "FAIL_CHARACTER_SET_NOT_EXTENSION", "PARTIAL_ANGULAR_LOCAL_SYSTEM", "PASS_GL2Z_SETWISE", "FAIL_TORUS_LATTICE_SIGN_AND_PHASE_UNSELECTED", "PASS_TIE_FREE_LINE_ONLY", "FAIL_TWO_AND_THREE_WAY_TIES", "NOT_APPLICABLE", "PARTIAL_MONODROMY_SETWISE", "PASS_SETWISE_ONLY", "FAIL_MULTIPLE_COMPLETION_GATES", "PARTIAL", "PASS_SCOPED_NO_SPLICE", "OPEN_SEPARATE_GATE"],
    "C10": ["PASS", "PASS", "FAIL_NO_ACTIVE_HOLONOMY_OR_ONTOLOGY_SELECTION", "PASS_CONDITIONAL_POINTWISE_FULL_PLUS_MINUS_MEMBERS_TWISTED_ZERO_PARTIAL", "PASS_FOR_SUPPLIED_LORENTZ_HOLONOMY", "PASS_FOR_SUPPLIED_COCYCLE", "PASS_CONDITIONAL_ON_ACTUAL_HOLONOMY", "PASS_PLUS_MINUS_ONLY_TWISTED_ZERO_NOT_UNIQUE_FULL_CLASS", "FAIL_FULL_OR_NULL_HOLONOMY", "OPEN_SINGULAR_COMPLEMENT", "PASS_CONDITIONAL_REDUCED_HOLONOMY", "PARTIAL_TWIST_IS_EXTERNAL_NOT_LORENTZ_HOLONOMY", "FAIL_NO_SELECTED_COMPLETE_BRANCH", "PASS", "FAIL_POSITIVE_VALUES_OCCUR_ON_DIFFERENT_BRANCHES", "OPEN_SEPARATE_GATE"],
    "C11": ["PASS", "PARTIAL_FINITE_CELL_DATA_UNSELECTED", "FAIL_NO_ACTIVE_BOUNDARY_SELECTOR", "FAIL_SEAL_IDENTITY_HAS_ZERO_EXTENSION_RANK", "OPEN_LIFT_DEPENDENT", "OPEN_LIFT_DEPENDENT", "FAIL_NORMAL_LIFT_OR_ISOTROPY_CHOSEN", "FAIL_ALL_EXTENSIONS_IDENTITY_AT_PHI_ZERO", "FAIL_MULTIPLE_FIXED_SET_TYPES", "OPEN_CAUSAL_SURFACE_TYPE", "OPEN", "OPEN", "FAIL_COMPLETION_NOT_SELECTED", "PASS_AT_SEAL_ONLY", "PASS_SCOPED_NO_SPLICE", "OPEN_SEPARATE_GATE"],
    "C12": ["PASS", "PARTIAL_COMPLETION_DATA_SUPPLIED", "FAIL_NO_ACTIVE_COMPLETION_SELECTION", "PARTIAL_CONSTRAINS_NOT_SELECTS_EXTENSION", "PARTIAL_TRANSITION_DEPENDENT", "PASS_WHEN_COCYCLE_SUPPLIED", "FAIL_CAP_QUOTIENT_OR_GLUE_IS_INPUT", "FAIL_FAMILY_DEPENDENT", "FAIL_STRATIFIED_AND_SINGULAR_REMAINDERS", "OPEN_TYPE_CHANGE_AND_RANK_LOSS", "PARTIAL", "PASS_CONDITIONAL_ON_SUPPLIED_COCYCLE", "FAIL_NO_ONE_RULE_ACROSS_ALL_COMPLETIONS", "PARTIAL", "PASS_SCOPED_NO_SPLICE", "OPEN_SEPARATE_GATE"],
}

OUTCOMES = {
    "C01": ("PARTIAL_CONSTRAINT", "founded_pair_fixes_only_the_two_channel_projection"),
    "C02": ("AVAILABLE_CONDITIONAL", "unique_Killing_line_exists_on_some_complete_witnesses_but_not_a_complete_extension"),
    "C03": ("AVAILABLE_CONDITIONAL", "nonnull_dphi_selects_a_line_split_but_not_the_ordered_pair_and_fails_null_zero_type_change"),
    "C04": ("SET_VALUED_ONLY", "three_pairings_exist_only_on_the_real_Segre_1_111_stratum_while_complex_repeated_and_Einstein_strata_do_not_supply_a_complete_section"),
    "C05": ("SET_VALUED_ONLY", "principal_bivector_data_does_not_supply_a_complete_founded_extension_and_degenerates"),
    "C06": ("SET_VALUED_ONLY", "curvature_operator_reductions_are_not_complete_sections_and_full_holonomy_obstructs_descent"),
    "C07": ("AVAILABLE_CONDITIONAL", "angular_axes_require_a_supplied_split_and_fail_round_ties_wall_crossing_and_monodromy"),
    "C08": ("AVAILABLE_CONDITIONAL", "projectors_presuppose_the_solder_or_nonnull_direction_they_would_need_to_select"),
    "C09": ("SET_VALUED_ONLY", "dual_systole_is_globally_set_covariant_but_has_exact_two_and_three_way_ties"),
    "C10": ("AVAILABLE_CONDITIONAL", "supplied_SO3_or_SOplus12_centralizer_conditions_force_pointwise_full_chart_plus_or_minus_members_but_the_non_Lorentz_twisted_zero_leaves_two_full_class_mixing_freedoms_and_no_global_branch_is_selected"),
    "C11": ("PARTIAL_CONSTRAINT", "phi_zero_makes_every_extension_identity_and_supplies_zero_selector_rank"),
    "C12": ("AVAILABLE_CONDITIONAL", "supplied_completion_cocycles_constrain_descent_but_neither_completion_nor_section_is selected"),
}


def verify_source_claims() -> dict[str, bool]:
    manifest = {row["source_id"]: row["path"] for row in read_tsv("SOURCE_MANIFEST.tsv")}
    claims = {
        "active_selector_rank_zero": ("S04", "\t0\t"),
        "nonnull_dphi_conditional": ("S05", "COVARIANT_LINE_SPLIT_NOT_ORDERED_PAIR"),
        "explicit_unbounded_remainder": ("S05", "EXPLICIT_UNBOUNDED_REMAINDER"),
        "holonomy_conditional_values": ("S06", "UNIQUE_CONDITIONAL"),
        "unique_killing_witness": ("S10", "EXISTS_COMPLETE_FULL_KILLING_ALGEBRA_ONE_DIMENSIONAL"),
        "systole_ties": ("S13", "TWO_WAY_TIE_AT_PHI_ZERO"),
        "finite_cell_nonselection": ("S12", "NOT_EVALUABLE"),
    }
    result = {}
    for key, (source_id, token) in claims.items():
        result[key] = token in (ROOT / manifest[source_id]).read_text(encoding="utf-8")
        assert result[key], f"missing registered source claim: {key}"
    return result


def main() -> None:
    candidates = read_tsv("CANDIDATE_UNIVERSE.tsv")
    gates = read_tsv("GATE_SCHEMA.tsv")
    assert [row["candidate_id"] for row in candidates] == [f"C{i:02d}" for i in range(1, 13)]
    assert [row["gate_id"] for row in gates] == [f"G{i:02d}" for i in range(1, 17)]
    assert set(G) == {row["candidate_id"] for row in candidates}
    assert all(len(statuses) == 16 for statuses in G.values())

    controls = exact_controls()
    source_claims = verify_source_claims()
    matrix_rows = []
    for candidate in candidates:
        cid = candidate["candidate_id"]
        for gate, status in zip(gates, G[cid]):
            matrix_rows.append(
                {
                    "candidate_id": cid,
                    "candidate_family": candidate["candidate_family"],
                    "gate_id": gate["gate_id"],
                    "gate": gate["gate"],
                    "status": status,
                }
            )
    write_tsv(
        "SELECTOR_GATE_MATRIX.tsv",
        matrix_rows,
        ["candidate_id", "candidate_family", "gate_id", "gate", "status"],
    )

    outcome_rows = []
    for candidate in candidates:
        cid = candidate["candidate_id"]
        outcome, reason = OUTCOMES[cid]
        selected = outcome == "SELECTED_DERIVED"
        outcome_rows.append(
            {
                "candidate_id": cid,
                "candidate_family": candidate["candidate_family"],
                "outcome": outcome,
                "native_section_selected": "YES" if selected else "NO",
                "reason": reason,
                "variation_domain": "OPEN_SEPARATE_GATE",
            }
        )
    write_tsv(
        "SELECTOR_OUTCOMES.tsv",
        outcome_rows,
        ["candidate_id", "candidate_family", "outcome", "native_section_selected", "reason", "variation_domain"],
    )

    status_counts = Counter(row["status"] for row in matrix_rows)
    outcome_counts = Counter(row["outcome"] for row in outcome_rows)
    exact_path = HERE / "EXACT_ALGEBRA.json"
    exact_path.write_text(json.dumps(controls, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    result = {
        "candidate_count": len(candidates),
        "gate_count": len(gates),
        "matrix_cell_count": len(matrix_rows),
        "native_selected_count": sum(row["native_section_selected"] == "YES" for row in outcome_rows),
        "outcome_counts": dict(sorted(outcome_counts.items())),
        "status_counts": dict(sorted(status_counts.items())),
        "source_claims": source_claims,
        "exact_algebra_sha256": hashlib.sha256(exact_path.read_bytes()).hexdigest(),
        "maximum_conclusion": "TWELVE_PREREGISTERED_CANDIDATE_FAMILY_BOUNDARY;NO_ACTIVE_UDT_AUTHORITATIVE_LOCAL_LORENTZ_EQUIVARIANT_COMPLETE_EXTENSION_SECTION_EVIDENCED;SUPPLIED_REDUCED_HOLONOMY_CONDITIONALLY_FORCES_POINTWISE_FULL_CHART_PLUS_OR_MINUS_MEMBER;NON_LORENTZ_TWISTED_ZERO_REMAINS_PARTIAL_IN_FULL_CLASS;GLOBAL_BUNDLE_TRANSITION_LAW_ADMISSIBLE_SECTIONS_AND_PHYSICAL_VARIATION_DOMAIN_REMAIN_OPEN",
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
