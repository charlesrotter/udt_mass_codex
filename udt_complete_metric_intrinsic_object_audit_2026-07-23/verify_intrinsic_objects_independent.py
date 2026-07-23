#!/usr/bin/env python3
"""Independent standard-library verifier for the intrinsic-object audit.

This implementation does not import SymPy or the production derivation.
"""

from __future__ import annotations

import copy
import csv
import hashlib
import itertools
import json
import platform
from collections import Counter
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PAIR_BASIS = ((0, 1), (0, 2), (0, 3), (2, 3), (3, 1), (1, 2))


def zeros(rows: int, columns: int) -> list[list[F]]:
    return [[F(0) for _ in range(columns)] for _ in range(rows)]


def identity(size: int) -> list[list[F]]:
    result = zeros(size, size)
    for index in range(size):
        result[index][index] = F(1)
    return result


def transpose(matrix: list[list[F]]) -> list[list[F]]:
    return [list(column) for column in zip(*matrix)]


def matmul(left: list[list[F]], right: list[list[F]]) -> list[list[F]]:
    return [
        [sum(left[i][k] * right[k][j] for k in range(len(right))) for j in range(len(right[0]))]
        for i in range(len(left))
    ]


def add(left: list[list[F]], right: list[list[F]], sign: int = 1) -> list[list[F]]:
    return [
        [left[i][j] + sign * right[i][j] for j in range(len(left[0]))]
        for i in range(len(left))
    ]


def scalar_mul(value: F, matrix: list[list[F]]) -> list[list[F]]:
    return [[value * item for item in row] for row in matrix]


def flatten(matrix: list[list[F]]) -> list[F]:
    return [item for row in matrix for item in row]


def rank(matrix: list[list[F]]) -> int:
    work = [row[:] for row in matrix]
    if not work:
        return 0
    rows = len(work)
    columns = len(work[0])
    pivot_row = 0
    for column in range(columns):
        pivot = next((row for row in range(pivot_row, rows) if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [item / value for item in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                work[row][index] - factor * work[pivot_row][index]
                for index in range(columns)
            ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def matrix_equal(left: list[list[F]], right: list[list[F]]) -> bool:
    return left == right


def metric_generators() -> tuple[list[list[F]], list[list[list[F]]]]:
    eta = zeros(4, 4)
    for index, value in enumerate((-1, 1, 1, 1)):
        eta[index][index] = F(value)
    generators: list[list[list[F]]] = []
    for spatial in (1, 2, 3):
        boost = zeros(4, 4)
        boost[0][spatial] = boost[spatial][0] = F(1)
        generators.append(boost)
    for left, right in ((1, 2), (1, 3), (2, 3)):
        rotation = zeros(4, 4)
        rotation[left][right] = F(-1)
        rotation[right][left] = F(1)
        generators.append(rotation)
    return eta, generators


def linear_action_matrix(
    input_rows: int,
    input_columns: int,
    output,
) -> list[list[F]]:
    columns: list[list[F]] = []
    for variable in range(input_rows * input_columns):
        basis = zeros(input_rows, input_columns)
        basis[variable // input_columns][variable % input_columns] = F(1)
        columns.append(flatten(output(basis)))
    return [list(row) for row in zip(*columns)]


def commutant_dimension(generators: list[list[list[F]]]) -> int:
    size = len(generators[0])
    blocks = []
    for generator in generators:
        blocks.extend(
            linear_action_matrix(
                size,
                size,
                lambda candidate, generator=generator: add(
                    matmul(candidate, generator),
                    matmul(generator, candidate),
                    sign=-1,
                ),
            )
        )
    return size * size - rank(blocks)


def form_matrix(vector: list[F]) -> list[list[F]]:
    result = zeros(4, 4)
    for coefficient, (left, right) in zip(vector, PAIR_BASIS):
        result[left][right] = coefficient
        result[right][left] = -coefficient
    return result


def form_vector(matrix: list[list[F]]) -> list[F]:
    return [matrix[left][right] for left, right in PAIR_BASIS]


def induced_form_generator(generator: list[list[F]]) -> list[list[F]]:
    columns = []
    for index in range(6):
        basis = [F(0)] * 6
        basis[index] = F(1)
        form = form_matrix(basis)
        variation = scalar_mul(
            F(-1),
            add(matmul(transpose(generator), form), matmul(form, generator)),
        )
        columns.append(form_vector(variation))
    return [list(row) for row in zip(*columns)]


def induced_form_group_action(group_element: list[list[F]]) -> list[list[F]]:
    columns = []
    for index in range(6):
        basis = [F(0)] * 6
        basis[index] = F(1)
        form = form_matrix(basis)
        transformed = matmul(matmul(transpose(group_element), form), group_element)
        columns.append(form_vector(transformed))
    return [list(row) for row in zip(*columns)]


def induced_form_projector(projector: list[list[F]]) -> list[list[F]]:
    columns = []
    for index in range(6):
        basis = [F(0)] * 6
        basis[index] = F(1)
        form = form_matrix(basis)
        projected = add(
            matmul(transpose(projector), form),
            matmul(form, projector),
        )
        columns.append(form_vector(projected))
    return [list(row) for row in zip(*columns)]


def line_projector(metric: list[list[F]], covector: list[F]) -> list[list[F]]:
    # The audit metric is its own inverse.
    raised = [sum(metric[i][j] * covector[j] for j in range(4)) for i in range(4)]
    norm = sum(covector[i] * raised[i] for i in range(4))
    if norm == 0:
        raise ZeroDivisionError("null covector")
    return [[raised[i] * covector[j] / norm for j in range(4)] for i in range(4)]


def permutation_sign(values: tuple[int, int, int, int]) -> int:
    if len(set(values)) < 4:
        return 0
    inversions = sum(
        values[left] > values[right]
        for left in range(4)
        for right in range(left + 1, 4)
    )
    return -1 if inversions % 2 else 1


def hodge_star() -> list[list[F]]:
    inverse = zeros(4, 4)
    for index, value in enumerate((-1, 1, 1, 1)):
        inverse[index][index] = F(value)
    columns = []
    for index in range(6):
        basis = [F(0)] * 6
        basis[index] = F(1)
        covariant = form_matrix(basis)
        contravariant = matmul(matmul(inverse, covariant), inverse)
        dual = zeros(4, 4)
        for a in range(4):
            for b in range(4):
                dual[a][b] = F(1, 2) * sum(
                    F(permutation_sign((a, b, c, d))) * contravariant[c][d]
                    for c in range(4)
                    for d in range(4)
                )
        columns.append(form_vector(dual))
    return [list(row) for row in zip(*columns)]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


EXPECTED_RULINGS = {
    "O02": "BUNDLE_EXISTS_SECTION_AND_HOPF_CLASS_OPEN",
    "O05": "STAR_SQUARED_MINUS_I_NO_REAL_PLUS_MINUS_REDUCTION",
    "O06": "EXACT_INTRINSIC_COMPLEX_RECIPROCAL_CANDIDATE_FAILS_REALITY_AND_SUPPLIES_NO_HOPF_SECTION",
    "O11": "INTRINSIC_LINE_NOT_RECIPROCAL_PLANE_OR_HOPF_SECTION",
    "O12": "CONDITIONAL_LOCAL_SECTION_NOT_UNIVERSAL_OR_HOPF_BEARING",
    "O16": "FAILS_LOCAL_LORENTZ_DESCENT",
    "O20": "INTRINSIC_ON_SUPPLIED_COMPLETION_NOT_FOUNDATION_SELECTOR",
    "O22": "GENUINE_GLOBAL_INVARIANTS_BUT_NOT_RECIPROCAL_HOPF_CARRIER",
    "O24": "EXACT_CONDITIONAL_HOPF_BUNDLE_NOT_NATIVE_SELECTION",
    "O25": "NOT_A_PHYSICAL_BUNDLE_INVARIANT",
    "O29": "FIELD_ASSISTED_REAL_RECIPROCAL_REDUCTION_EXISTS_ONLY_ON_NONNULL_DPHI_STRATA__NO_GLOBAL_HOPF_SECTION_OR_SELECTED_BUNDLE_INVARIANT",
    "O30": "EXACT_FIELD_ASSISTED_REAL_RECIPROCAL_3PLUS3_REDUCTION_ON_NONNULL_STRATA__NOT_GLOBAL_OR_HOPF_BEARING",
}


def validate_payload(
    result: dict,
    rows: list[dict[str, str]],
    source_lines: list[str],
    frozen_replay: dict[str, object],
) -> None:
    if result.get("status") != "PASS":
        raise AssertionError("result status")
    counts = result.get("counts", {})
    expected_counts = {
        "object_candidates": 30,
        "exact_checks": 37,
        "tangent_commutant_dimension": 1,
        "invariant_tangent_vector_dimension": 0,
        "invariant_real_two_form_dimension": 0,
        "two_form_commutant_dimension": 2,
        "full_orientation_reversing_Lorentz_two_form_commutant_dimension": 1,
        "spatial_rotation_fixed_vector_dimension": 0,
        "registered_configurations": 6144,
        "registered_metric_active_full_irreducible": 5376,
        "registered_flat_ambiguous": 768,
        "registered_isolated_real_simple_curvature_eigenplanes": 0,
        "registered_global_completion_families": 12,
        "native_selected_reciprocal_Hopf_objects": 0,
        "intrinsic_complex_reciprocal_candidates": 1,
        "intrinsic_real_reciprocal_local_stratum_candidates": 1,
        "intrinsic_real_reciprocal_Hopf_objects": 0,
        "conditional_exact_toric_Hopf_objects": 1,
    }
    for key, value in expected_counts.items():
        if counts.get(key) != value:
            raise AssertionError(f"count {key}")
    if counts.get("seal_invariant_projector_ranks") != [0, 1, 3, 4]:
        raise AssertionError("seal ranks")
    if counts.get("registered_dphi_causal_classes") != {
        "SPACELIKE": 2304,
        "TIMELIKE": 768,
        "ZERO": 3072,
    }:
        raise AssertionError("dphi causal census")
    if frozen_replay != {
        "configurations": 6144,
        "metric_active_full_irreducible": 5376,
        "flat_ambiguous": 768,
        "isolated_real_simple_curvature_eigenplanes": 0,
        "global_completion_families": 12,
        "selected_global_quotient_classes": [],
        "dphi_causal_classes": {
            "SPACELIKE": 2304,
            "TIMELIKE": 768,
            "ZERO": 3072,
        },
    }:
        raise AssertionError("frozen evidence replay")
    if len(rows) != 30 or len({row["id"] for row in rows}) != 30:
        raise AssertionError("row coverage")
    by_id = {row["id"]: row for row in rows}
    for identity, ruling in EXPECTED_RULINGS.items():
        if by_id.get(identity, {}).get("ruling") != ruling:
            raise AssertionError(f"ruling {identity}")
    if by_id["O24"]["foundation_selection"] != "GLOBAL_INPUTS_NOT_SELECTED":
        raise AssertionError("conditional toric selection")
    if by_id["O02"]["Hopf_content"] != "S2_FIBER_ONLY":
        raise AssertionError("fiber/section distinction")
    if by_id["O20"]["definition_domain"] != "SUPPLIED_COMPLETE_METRIC_AND_LOOPS":
        raise AssertionError("holonomy domain")
    if by_id["O29"]["foundation_selection"] != "NO_NATIVE_JOIN_FOUND":
        raise AssertionError("whole-foundation selection")
    maximum = result.get("maximum_conclusion", "")
    if maximum != (
        "EXACT_FRAME_INDEPENDENT_FIELD_ASSISTED_REAL_RECIPROCAL_3PLUS3_TWO_FORM_"
        "REDUCTION_IDENTIFIED_ON_NONNULL_DPHI_STRATA__HODGE_EXCHANGES_THE_SECTORS__"
        "GLOBAL_EXTENSION_PHYSICAL_OWNERSHIP_AND_HOPF_SECTION_REMAIN_OPEN"
    ):
        raise AssertionError("maximum conclusion")
    scope = result.get("scope", "")
    if "NOT_ARBITRARY_FUTURE_HIGHER_JET_OR_NONLOCAL_UDT_LAWS" not in scope:
        raise AssertionError("bounded scope")
    if len(source_lines) != 60 or len(set(source_lines)) != 60:
        raise AssertionError("source manifest coverage")
    for line in source_lines:
        digest, relative = line.split("  ", 1)
        if sha256(ROOT / relative) != digest:
            raise AssertionError(f"source hash {relative}")


def main() -> None:
    eta, generators = metric_generators()
    metric_skew = all(
        matrix_equal(
            add(matmul(transpose(generator), eta), matmul(eta, generator)),
            zeros(4, 4),
        )
        for generator in generators
    )
    tangent_commutant_dimension = commutant_dimension(generators)
    invariant_vector_rank = rank([row for generator in generators for row in generator])
    invariant_vector_dimension = 4 - invariant_vector_rank

    form_action_rows = []
    for generator in generators:
        form_action_rows.extend(
            linear_action_matrix(
                6,
                1,
                lambda vector_matrix, generator=generator: [
                    [item]
                    for item in form_vector(
                        add(
                            matmul(transpose(generator), form_matrix(flatten(vector_matrix))),
                            matmul(form_matrix(flatten(vector_matrix)), generator),
                        )
                    )
                ],
            )
        )
    invariant_two_form_dimension = 6 - rank(form_action_rows)

    induced = [induced_form_generator(generator) for generator in generators]
    two_form_commutant_dimension = commutant_dimension(induced)
    orientation_reversal = identity(4)
    orientation_reversal[1][1] = F(-1)
    orientation_reversal_on_forms = induced_form_group_action(orientation_reversal)
    full_lorentz_commutant_dimension = commutant_dimension(
        [*induced, orientation_reversal_on_forms]
    )
    star = hodge_star()
    identity_star_span_rank = rank(
        [
            [flatten(identity(6))[row], flatten(star)[row]]
            for row in range(36)
        ]
    )
    star_square = matmul(star, star)
    star_commutes = all(
        matrix_equal(matmul(star, generator), matmul(generator, star))
        for generator in induced
    )
    star_anticommutes_with_orientation_reversal = matrix_equal(
        matmul(star, orientation_reversal_on_forms),
        scalar_mul(
            F(-1), matmul(orientation_reversal_on_forms, star)
        ),
    )
    star_trace = sum(star[index][index] for index in range(6))
    star_first_basis = [star[row][0] for row in range(6)]
    # Formal exact complexification: K=i* has K^2=I because i^2=-1 and
    # *^2=-I.  P_\pm=(I+/-K)/2 are idempotent with trace/rank three.
    # D_t=((t+t^-1)/2)I+i((t-t^-1)/2)* has a nonzero imaginary part
    # on the first real basis form for t=2, hence fails real descent.
    complex_Hodge_projector_rank = 3 if star_trace == 0 else -1
    reciprocal_reality_imaginary_coefficient = F(3, 4)
    complex_reciprocal_fails_real_descent = any(
        reciprocal_reality_imaginary_coefficient * item != 0
        for item in star_first_basis
    )
    timelike_line = line_projector(eta, [F(2), F(1), F(0), F(0)])
    conformally_scaled_inverse_metric = scalar_mul(F(1, 4), eta)
    conformally_scaled_timelike_line = line_projector(
        conformally_scaled_inverse_metric,
        [F(2), F(1), F(0), F(0)],
    )
    timelike_plus = induced_form_projector(timelike_line)
    timelike_minus = add(identity(6), timelike_plus, sign=-1)
    timelike_involution = add(scalar_mul(F(2), timelike_plus), identity(6), sign=-1)
    reciprocal_two = add(
        scalar_mul(F(2), timelike_plus),
        scalar_mul(F(1, 2), timelike_minus),
    )
    reciprocal_two_inverse = add(
        scalar_mul(F(1, 2), timelike_plus),
        scalar_mul(F(2), timelike_minus),
    )
    conformally_scaled_timelike_plus = induced_form_projector(
        conformally_scaled_timelike_line
    )
    conformally_scaled_timelike_minus = add(
        identity(6), conformally_scaled_timelike_plus, sign=-1
    )
    conformally_scaled_reciprocal_two = add(
        scalar_mul(F(2), conformally_scaled_timelike_plus),
        scalar_mul(F(1, 2), conformally_scaled_timelike_minus),
    )
    hodge_inverse = scalar_mul(F(-1), star)
    spacelike_line = line_projector(eta, [F(1), F(2), F(0), F(0)])
    spacelike_plus = induced_form_projector(spacelike_line)
    null_covector = [F(1), F(1), F(0), F(0)]
    null_raised = [
        sum(eta[i][j] * null_covector[j] for j in range(4)) for i in range(4)
    ]
    null_endomorphism = [
        [null_raised[i] * null_covector[j] for j in range(4)] for i in range(4)
    ]
    null_two_form_endomorphism = induced_form_projector(null_endomorphism)

    spatial_blocks = [
        [row[1:4] for row in generator[1:4]]
        for generator in generators[3:]
    ]
    spatial_fixed_dimension = 3 - rank([row for block in spatial_blocks for row in block])

    boost = [
        [F(5, 4), F(3, 4), F(0), F(0)],
        [F(3, 4), F(5, 4), F(0), F(0)],
        [F(0), F(0), F(1), F(0)],
        [F(0), F(0), F(0), F(1)],
    ]
    boost_metric = matmul(matmul(transpose(boost), eta), boost)
    named_leg_vector = [F(1), F(0), F(0), F(0)]
    moved_leg_vector = [sum(boost[i][j] * named_leg_vector[j] for j in range(4)) for i in range(4)]

    seal_generators = [generators[1], generators[2], generators[5]]
    seal_commutant_dimension = commutant_dimension(seal_generators)
    normal_projector = zeros(4, 4)
    normal_projector[1][1] = F(1)
    tangent_projector = add(identity(4), normal_projector, sign=-1)
    seal_basis_commutes = all(
        matrix_equal(
            matmul(projector, generator), matmul(generator, projector)
        )
        for projector in (normal_projector, tangent_projector)
        for generator in seal_generators
    )

    exact = {
        "lorentz_generators_metric_skew": metric_skew,
        "tangent_commutant_dimension": tangent_commutant_dimension == 1,
        "invariant_vector_dimension": invariant_vector_dimension == 0,
        "invariant_two_form_dimension": invariant_two_form_dimension == 0,
        "connected_orientation_preserving_two_form_commutant_dimension": (
            two_form_commutant_dimension == 2
        ),
        "connected_orientation_preserving_two_form_commutant_spanned_by_I_and_star": two_form_commutant_dimension == 2
        and identity_star_span_rank == 2,
        "full_orientation_reversing_Lorentz_two_form_commutant_is_scalar": (
            full_lorentz_commutant_dimension == 1
        ),
        "hodge_square_minus_identity": matrix_equal(
            star_square, scalar_mul(F(-1), identity(6))
        ),
        "hodge_commutes": star_commutes,
        "hodge_anticommutes_with_orientation_reversal": (
            star_anticommutes_with_orientation_reversal
        ),
        "formal_i_hodge_involution": matrix_equal(
            star_square, scalar_mul(F(-1), identity(6))
        ),
        "formal_complex_projector_ranks": complex_Hodge_projector_rank == 3,
        "complex_reciprocal_fails_real_descent": complex_reciprocal_fails_real_descent,
        "real_equivariant_two_form_maps_no_real_reciprocal_split": (
            two_form_commutant_dimension == 2
            and identity_star_span_rank == 2
            and matrix_equal(star_square, scalar_mul(F(-1), identity(6)))
        ),
        "nonnull_gradient_rank3_plus_rank3": rank(timelike_plus) == 3
        and matrix_equal(matmul(timelike_plus, timelike_plus), timelike_plus)
        and rank(timelike_minus) == 3
        and matrix_equal(matmul(timelike_minus, timelike_minus), timelike_minus),
        "nonnull_gradient_Hodge_exchange": matrix_equal(
            matmul(matmul(star, timelike_plus), hodge_inverse),
            timelike_minus,
        ),
        "nonnull_gradient_real_involution": matrix_equal(
            matmul(timelike_involution, timelike_involution), identity(6)
        ),
        "Hodge_exchange_conjugates_reciprocal_to_inverse": matrix_equal(
            matmul(matmul(star, reciprocal_two), hodge_inverse),
            reciprocal_two_inverse,
        )
        and matrix_equal(
            matmul(reciprocal_two, reciprocal_two_inverse), identity(6)
        ),
        "gradient_projector_CSN_invariant": matrix_equal(
            conformally_scaled_timelike_line, timelike_line
        ),
        "full_gradient_reciprocal_operator_CSN_invariant": matrix_equal(
            conformally_scaled_reciprocal_two, reciprocal_two
        ),
        "spacelike_gradient_same_Hodge_pair": rank(spacelike_plus) == 3
        and matrix_equal(matmul(spacelike_plus, spacelike_plus), spacelike_plus)
        and matrix_equal(
            matmul(matmul(star, spacelike_plus), hodge_inverse),
            add(identity(6), spacelike_plus, sign=-1),
        ),
        "null_gradient_is_nonzero_nilpotent_not_projector": rank(null_endomorphism) == 1
        and matrix_equal(matmul(null_endomorphism, null_endomorphism), zeros(4, 4)),
        "null_gradient_induced_two_form_map_is_rank2_nilpotent": (
            rank(null_two_form_endomorphism) == 2
            and any(flatten(null_two_form_endomorphism))
            and matrix_equal(
                matmul(null_two_form_endomorphism, null_two_form_endomorphism),
                zeros(6, 6),
            )
        ),
        "spatial_fixed_dimension": spatial_fixed_dimension == 0,
        "same_metric_boost": matrix_equal(boost_metric, eta),
        "boost_moves_named_leg": moved_leg_vector != named_leg_vector,
        "seal_commutant_dimension": seal_commutant_dimension == 2,
        "seal_projector_basis_commutes": seal_basis_commutes,
        "seal_projector_rank_pattern": rank(normal_projector) == 1
        and rank(tangent_projector) == 3,
    }
    failed = [name for name, status in exact.items() if not status]
    if failed:
        raise AssertionError(f"independent exact failures: {failed}")

    result = json.loads((HERE / "RESULT.json").read_text(encoding="utf-8"))
    rows = read_rows(HERE / "INTRINSIC_OBJECT_CENSUS.tsv")
    source_lines = [
        line
        for line in (HERE / "SOURCE_MANIFEST.sha256").read_text(encoding="utf-8").splitlines()
        if line
    ]
    local_atlas = json.loads(
        (
            ROOT
            / "udt_local_selector_holonomy_closure_2026-07-22/ATLAS_RESULT.json"
        ).read_text(encoding="utf-8")
    )
    joint_atlas = json.loads(
        (
            ROOT
            / "udt_joint_invariant_subspace_atlas_2026-07-21/ATLAS_RESULT.json"
        ).read_text(encoding="utf-8")
    )
    global_atlas = json.loads(
        (
            ROOT
            / "udt_global_metric_assembly_atlas_2026-07-22/ATLAS_RESULT.json"
        ).read_text(encoding="utf-8")
    )
    dphi_rows = read_rows(
        ROOT
        / "udt_structural_ensemble_metric_atlas_2026-07-21/CONFIGURATION_OBSERVATIONS.tsv"
    )
    dphi_causal_classes = Counter(row["dphi_class"] for row in dphi_rows)
    frozen_replay = {
        "configurations": local_atlas["q02"]["configurations"],
        "metric_active_full_irreducible": local_atlas["q02"][
            "final_class_counts"
        ]["BASE_CURVATURE_FULL_IRREDUCIBLE__HIGHER_JETS_MONOTONE"],
        "flat_ambiguous": local_atlas["q02"]["final_class_counts"][
            "EXACT_CONSTANT_METRIC_FLAT__ALL_SUBSPACES_AMBIGUOUS"
        ],
        "isolated_real_simple_curvature_eigenplanes": joint_atlas[
            "bivector_eigenplane_rows"
        ],
        "global_completion_families": global_atlas["completion_class_count"],
        "selected_global_quotient_classes": global_atlas[
            "selected_global_quotient_classes"
        ],
        "dphi_causal_classes": dict(sorted(dphi_causal_classes.items())),
    }
    validate_payload(result, rows, source_lines, frozen_replay)

    catches: list[dict[str, str]] = []

    def catch(identity: str, mutation: str, mutate) -> None:
        mutated_result = copy.deepcopy(result)
        mutated_rows = copy.deepcopy(rows)
        mutated_sources = list(source_lines)
        mutate(mutated_result, mutated_rows, mutated_sources)
        caught = False
        try:
            validate_payload(
                mutated_result, mutated_rows, mutated_sources, frozen_replay
            )
        except Exception:
            caught = True
        if not caught:
            raise AssertionError(f"mutation escaped: {identity}")
        catches.append({"id": identity, "mutation": mutation, "status": "CAUGHT"})

    catch("C01", "remove_object_row", lambda _r, rows_, _s: rows_.pop())
    catch("C02", "duplicate_object_identity", lambda _r, rows_, _s: rows_.append(copy.deepcopy(rows_[0])))
    catch("C03", "promote_celestial_bundle_to_selected_section", lambda _r, rows_, _s: rows_[1].update(ruling="SELECTED_SECTION"))
    catch("C04", "promote_Hodge_star_to_real_rank2_split", lambda _r, rows_, _s: rows_[4].update(ruling="REAL_RANK2_SPLIT"))
    catch("C19", "promote_complex_Hodge_candidate_to_real", lambda _r, rows_, _s: rows_[5].update(ruling="REAL_RECIPROCAL_REDUCTION"))
    catch("C05", "promote_dphi_line_to_Hopf_section", lambda _r, rows_, _s: rows_[10].update(ruling="HOPF_SECTION"))
    catch("C06", "promote_null_dphi_stratum_to_universal", lambda _r, rows_, _s: rows_[11].update(ruling="UNIVERSAL_SECTION"))
    catch("C07", "declare_named_coframe_plane_intrinsic", lambda _r, rows_, _s: rows_[15].update(ruling="INTRINSIC"))
    catch("C08", "turn_per_metric_holonomy_into_foundation_selector", lambda _r, rows_, _s: rows_[19].update(ruling="FOUNDATION_SELECTOR"))
    catch("C09", "equate_primary_characteristic_class_with_Hopf_charge", lambda _r, rows_, _s: rows_[21].update(ruling="HOPF_CHARGE"))
    catch("C10", "promote_conditional_toric_bundle_to_native", lambda _r, rows_, _s: rows_[23].update(foundation_selection="NATIVE_SELECTED"))
    catch("C11", "declare_component_Hopf_charge_invariant", lambda _r, rows_, _s: rows_[24].update(ruling="FRAME_INVARIANT"))
    catch("C12", "promote_combined_foundation", lambda _r, rows_, _s: rows_[28].update(foundation_selection="NATIVE_OBJECT_FOUND"))
    catch("C13", "alter_registered_full_irreducible_count", lambda r, _rows, _s: r["counts"].update(registered_metric_active_full_irreducible=5375))
    catch("C14", "drop_bounded_scope", lambda r, _rows, _s: r.update(scope="ARBITRARY_METRICS"))
    catch("C15", "corrupt_source_digest", lambda _r, _rows, sources: sources.__setitem__(0, "0" * 64 + sources[0][64:]))
    catch("C16", "claim_native_selected_object", lambda r, _rows, _s: r["counts"].update(native_selected_reciprocal_Hopf_objects=1))
    catch("C17", "lose_fiber_section_distinction", lambda _r, rows_, _s: rows_[1].update(Hopf_content="SELECTED_HOPF_MAP"))
    catch("C18", "lose_holonomy_loop_dependency", lambda _r, rows_, _s: rows_[19].update(definition_domain="POINTWISE_METRIC"))
    catch("C20", "promote_nonnull_dphi_reduction_to_global_Hopf_object", lambda _r, rows_, _s: rows_[29].update(ruling="GLOBAL_HOPF_OBJECT"))

    def operator_catch(identity: str, mutation: str, mutated_check) -> None:
        caught = False
        try:
            if not mutated_check():
                raise AssertionError(mutation)
        except AssertionError:
            caught = True
        if not caught:
            raise AssertionError(f"operator mutation escaped: {identity}")
        catches.append({"id": identity, "mutation": mutation, "status": "CAUGHT"})

    doubled_line = scalar_mul(F(2), timelike_line)
    doubled_plus = induced_form_projector(doubled_line)
    operator_catch(
        "C21",
        "drop_projector_normalization",
        lambda: matrix_equal(matmul(doubled_plus, doubled_plus), doubled_plus),
    )
    corrupted_star = copy.deepcopy(star)
    corrupted_star[0][0] += F(1)
    operator_catch(
        "C22",
        "corrupt_Hodge_exchange_operator",
        lambda: matrix_equal(
            matmul(matmul(corrupted_star, timelike_plus), hodge_inverse),
            timelike_minus,
        ),
    )
    incorrectly_scaled_plus = induced_form_projector(
        scalar_mul(F(1, 4), timelike_line)
    )
    incorrectly_scaled_reciprocal = add(
        scalar_mul(F(2), incorrectly_scaled_plus),
        scalar_mul(
            F(1, 2), add(identity(6), incorrectly_scaled_plus, sign=-1)
        ),
    )
    operator_catch(
        "C23",
        "scale_projector_numerator_without_normalizing_denominator",
        lambda: matrix_equal(incorrectly_scaled_reciprocal, reciprocal_two),
    )
    operator_catch(
        "C24",
        "erase_complex_real_descent_obstruction_by_setting_reciprocal_weights_equal",
        lambda: any(F(0) * item != 0 for item in star_first_basis),
    )
    corrupted_null_two_form = add(null_two_form_endomorphism, identity(6))
    operator_catch(
        "C25",
        "replace_null_rank2_nilpotent_by_identity_shift",
        lambda: rank(corrupted_null_two_form) == 2
        and matrix_equal(
            matmul(corrupted_null_two_form, corrupted_null_two_form),
            zeros(6, 6),
        ),
    )

    with (HERE / "CATCH_PROOFS.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            delimiter="\t",
            fieldnames=["id", "mutation", "status"],
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(catches)

    verification = {
        "schema": "udt-complete-metric-intrinsic-object-independent-verification-1.0",
        "status": "PASS",
        "python_version": platform.python_version(),
        "implementation": (
            "stdlib_Fraction_no_production_import_no_SymPy__local_linear_algebra_"
            "independently_recomputed__frozen_atlas_taxonomies_directly_parsed_"
            "and_hash_checked_not_rederived"
        ),
        "exact_checks": exact,
        "counts": {
            "independent_exact_checks": len(exact),
            "object_rows": len(rows),
            "source_files": len(source_lines),
            "mutation_catches": len(catches),
            "tangent_commutant_dimension": tangent_commutant_dimension,
            "invariant_vector_dimension": invariant_vector_dimension,
            "invariant_two_form_dimension": invariant_two_form_dimension,
            "two_form_commutant_dimension": two_form_commutant_dimension,
            "full_orientation_reversing_Lorentz_two_form_commutant_dimension": (
                full_lorentz_commutant_dimension
            ),
            "spatial_fixed_dimension": spatial_fixed_dimension,
            "seal_commutant_dimension": seal_commutant_dimension,
            "frozen_dphi_causal_classes": dict(
                sorted(dphi_causal_classes.items())
            ),
        },
        "frozen_evidence_replay": frozen_replay,
        "result_sha256": sha256(HERE / "RESULT.json"),
        "object_census_sha256": sha256(HERE / "INTRINSIC_OBJECT_CENSUS.tsv"),
        "source_manifest_sha256": sha256(HERE / "SOURCE_MANIFEST.sha256"),
    }
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(verification, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(verification, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
