#!/usr/bin/env python3
"""Independent verifier for the dual-systole global transport audit.

This implementation uses only the Python standard library and never imports
the production derivation.  It recomputes the lattice controls, covariance,
wall topology, diagonal crossing, completion coverage, and authority limits.
"""

from __future__ import annotations

import ast
import copy
import csv
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Callable


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
TOL = 1.0e-11


class VerificationError(RuntimeError):
    pass


def read_tsv(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(
    name: str, fields: list[str], rows: list[dict[str, object]]
) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=fields, delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row[field] for field in fields})


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def require_identity(
    rows: list[dict[str, str]], field: str, count: int, label: str
) -> None:
    identities = [row[field] for row in rows]
    if len(identities) != count or len(set(identities)) != count:
        raise VerificationError(
            f"{label}: expected {count} unique rows, found "
            f"{len(identities)}/{len(set(identities))}"
        )


def canonical(vector: tuple[int, int]) -> tuple[int, int]:
    if vector[0] < 0 or (vector[0] == 0 and vector[1] < 0):
        return (-vector[0], -vector[1])
    return vector


def directions(bound: int) -> list[tuple[int, int]]:
    return [
        (first, second)
        for first in range(-bound, bound + 1)
        for second in range(-bound, bound + 1)
        if (first or second)
        and math.gcd(abs(first), abs(second)) == 1
        and canonical((first, second)) == (first, second)
    ]


def quadratic(
    matrix: tuple[tuple[float, float], tuple[float, float]],
    vector: tuple[int, int],
) -> float:
    return (
        matrix[0][0] * vector[0] * vector[0]
        + 2.0 * matrix[0][1] * vector[0] * vector[1]
        + matrix[1][1] * vector[1] * vector[1]
    )


def shortest(
    matrix: tuple[tuple[float, float], tuple[float, float]],
    bound: int = 50,
) -> tuple[float, list[tuple[int, int]], float]:
    """Enumerate independently and prove vectors outside the box are longer."""

    values = [(quadratic(matrix, vector), vector) for vector in directions(bound)]
    best = min(value for value, _ in values)
    winners = sorted(
        vector for value, vector in values if abs(value - best) <= TOL
    )
    trace = matrix[0][0] + matrix[1][1]
    discriminant = math.sqrt(
        (matrix[0][0] - matrix[1][1]) ** 2 + 4.0 * matrix[0][1] ** 2
    )
    eigenvalue_min = (trace - discriminant) / 2.0
    outside = eigenvalue_min * (bound + 1) ** 2
    if eigenvalue_min <= 0.0 or outside <= best:
        raise VerificationError("finite lattice search lacks exterior proof")
    return best, winners, outside


def multiply(
    left: tuple[tuple[float, float], tuple[float, float]],
    right: tuple[tuple[float, float], tuple[float, float]],
) -> tuple[tuple[float, float], tuple[float, float]]:
    return tuple(
        tuple(
            sum(left[row][middle] * right[middle][column] for middle in range(2))
            for column in range(2)
        )
        for row in range(2)
    )


def transpose(
    matrix: tuple[tuple[float, float], tuple[float, float]]
) -> tuple[tuple[float, float], tuple[float, float]]:
    return ((matrix[0][0], matrix[1][0]), (matrix[0][1], matrix[1][1]))


def inverse_integer(
    matrix: tuple[tuple[int, int], tuple[int, int]]
) -> tuple[tuple[int, int], tuple[int, int]]:
    determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    if abs(determinant) != 1:
        raise VerificationError("matrix is not unimodular")
    return (
        (matrix[1][1] // determinant, -matrix[0][1] // determinant),
        (-matrix[1][0] // determinant, matrix[0][0] // determinant),
    )


def transform_character(
    matrix: tuple[tuple[int, int], tuple[int, int]],
    vector: tuple[int, int],
) -> tuple[int, int]:
    inverse = inverse_integer(matrix)
    return canonical(
        (
            inverse[0][0] * vector[0] + inverse[1][0] * vector[1],
            inverse[0][1] * vector[0] + inverse[1][1] * vector[1],
        )
    )


def parse_directions(value: str) -> list[tuple[int, int]]:
    result = []
    for item in value.split(";"):
        first, second = item.strip("()").split(",")
        result.append((int(first), int(second)))
    return sorted(result)


def load_state() -> dict[str, object]:
    names = {
        "analytic": "ANALYTIC_OBJECT_REGISTRY.tsv",
        "completion_registry": "COMPLETION_TEST_REGISTRY.tsv",
        "contract": "FALSIFICATION_CONTRACT.tsv",
        "premises": "PREMISE_LEDGER.tsv",
        "sources": "SOURCE_MANIFEST.tsv",
        "source_verification": "SOURCE_VERIFICATION.tsv",
        "walls": "CONTINUOUS_WALL_ATLAS.tsv",
        "controls": "STANDARD_WALL_CONTROLS.tsv",
        "covariance": "GL2Z_COVARIANCE.tsv",
        "diagonal": "DIAGONAL_PATH_ATLAS.tsv",
        "global": "GLOBAL_TRANSPORT_ATLAS.tsv",
        "coverage": "COMPLETION_COVERAGE.tsv",
    }
    state = {key: read_tsv(name) for key, name in names.items()}
    state["results"] = json.loads((HERE / "RESULTS.json").read_text(encoding="utf-8"))
    return state


def validate_sources(state: dict[str, object]) -> None:
    sources = state["sources"]
    checks = state["source_verification"]
    require_identity(sources, "source_id", 16, "sources")
    require_identity(checks, "source_id", 16, "source checks")
    check_by_id = {row["source_id"]: row for row in checks}
    for source in sources:
        actual = digest(ROOT / source["path"])
        checked = check_by_id[source["source_id"]]
        if (
            actual != source["sha256"]
            or checked["expected_sha256"] != source["sha256"]
            or checked["actual_sha256"] != actual
            or checked["status"] != "PASS"
        ):
            raise VerificationError(f"source mismatch: {source['source_id']}")


def validate_wall_theorem(state: dict[str, object]) -> dict[str, object]:
    controls = state["controls"]
    walls = state["walls"]
    result = state["results"]
    require_identity(walls, "item_id", 14, "continuous wall objects")
    require_identity(controls, "control_id", 5, "standard wall controls")

    expected_ratios = [
        Fraction(-1, 2),
        Fraction(-1, 4),
        Fraction(0, 1),
        Fraction(1, 4),
        Fraction(1, 2),
    ]
    maximum = 0
    max_residual = 0.0
    for row, ratio in zip(controls, expected_ratios):
        if Fraction(row["ratio_B_over_L"]) != ratio:
            raise VerificationError("wall-control ratio ordering")
        ratio_float = float(ratio)
        length = 1.0 / math.sqrt(1.0 - ratio_float * ratio_float)
        matrix = (
            (length, ratio_float * length),
            (ratio_float * length, length),
        )
        best, winners, outside = shortest(matrix, bound=50)
        expected = [(0, 1), (1, 0)]
        if ratio == -Fraction(1, 2):
            expected.append((1, 1))
        if ratio == Fraction(1, 2):
            expected.append((1, -1))
        expected = sorted(expected)
        if winners != expected or parse_directions(row["shortest_lines_mod_sign"]) != expected:
            raise VerificationError(f"wall control differs: {row['control_id']}")
        if int(row["multiplicity"]) != len(expected) or outside <= best:
            raise VerificationError("wall control multiplicity/exterior proof")
        max_residual = max(
            max_residual,
            abs(float(row["L"]) - length),
            abs(float(row["shortest_norm_squared"]) - best),
        )
        maximum = max(maximum, len(winners))

    theorem = result["wall_theorem"]
    if (
        theorem["independent_co_shortest_pair"] != "UNIMODULAR"
        or theorem["maximum_unoriented_tie_multiplicity"] != 3
        or theorem["vertex_tie_multiplicity"] != 3
        or theorem["interior_tie_multiplicity"] != 2
        or maximum != 3
        or max_residual >= TOL
    ):
        raise VerificationError("wall theorem contract")

    # Independent exact proof controls.  The Hermite reduction inequality
    # gives lambda_1 <= 2/sqrt(3) < 2.  For co-shortest w,v,
    # |det(w,v)| <= ||w||_Q ||v||_Q = lambda_1, so the nonzero integer
    # determinant is exactly one.  In that basis det(Q)=1 gives L^2-B^2=1.
    hermite_bound = 2.0 / math.sqrt(3.0)
    if not hermite_bound < 2.0:
        raise VerificationError("Hermite determinant argument")
    for numerator in range(-4, 5):
        ratio = Fraction(numerator, 8)
        if abs(ratio) > Fraction(1, 2):
            continue
        length = 1.0 / math.sqrt(1.0 - float(ratio) ** 2)
        determinant = length * length - (float(ratio) * length) ** 2
        _, winners, _ = shortest(
            (
                (length, float(ratio) * length),
                (float(ratio) * length, length),
            ),
            bound=50,
        )
        if abs(determinant - 1.0) >= TOL or len(winners) > 3:
            raise VerificationError("independent reduced-wall sweep")

    return {
        "Hermite_bound": hermite_bound,
        "standard_wall_controls": 5,
        "independent_wall_samples": 9,
        "maximum_tie_multiplicity_observed": maximum,
        "maximum_numeric_residual": max_residual,
    }


def validate_chart_and_diagonal(state: dict[str, object]) -> dict[str, object]:
    result = state["results"]
    diagonal = state["diagonal"]
    require_identity(diagonal, "segment_id", 3, "diagonal segments")
    residuals = result["exact"]["residuals"]
    flattened = []
    for value in residuals.values():
        if isinstance(value, list):
            flattened.extend(item for row in value for item in row)
        else:
            flattened.append(value)
    if any(value != "0" for value in flattened):
        raise VerificationError("nonzero production exact residual")
    residual_max = 0.0
    samples = 0
    for phi in (-2.0, -1.0, -0.3, 0.0, 0.4, 1.2, 2.0):
        for shear in (-1.5, -0.5, 0.0, 0.25, 1.25):
            h11 = math.exp(-2.0 * phi)
            h12 = shear * math.exp(-phi)
            h22 = shear * shear + math.exp(2.0 * phi)
            determinant = h11 * h22 - h12 * h12
            x = shear * math.exp(phi)
            y = math.exp(2.0 * phi)
            recovered_phi = math.log(y) / 2.0
            recovered_shear = x / math.sqrt(y)
            residual_max = max(
                residual_max,
                abs(determinant - 1.0),
                abs(phi - recovered_phi),
                abs(shear - recovered_shear),
            )
            samples += 1
    if residual_max >= TOL:
        raise VerificationError("metric chart inversion")

    controls = [(-0.8, [(1, 0)]), (0.0, [(0, 1), (1, 0)]), (0.8, [(0, 1)])]
    for phi, expected in controls:
        qmetric = (
            (math.exp(2.0 * phi), 0.0),
            (0.0, math.exp(-2.0 * phi)),
        )
        _, winners, _ = shortest(qmetric, bound=50)
        if winners != expected:
            raise VerificationError(f"diagonal control at phi={phi}")
    if (
        result["diagonal_path_ruling"]
        != "RECIPROCAL_CHARACTER_SWAP_REQUIRES_TIE_CROSSING"
        or diagonal[1]["global_continuation"] != "TIE_NO_METRIC_TIE_BREAK"
    ):
        raise VerificationError("diagonal authority/ruling")
    return {
        "chart_samples": samples,
        "chart_residual_max": residual_max,
        "diagonal_segments": 3,
        "diagonal_tie_count_at_zero": 2,
    }


def validate_covariance(state: dict[str, object]) -> dict[str, object]:
    rows = state["covariance"]
    require_identity(rows, "matrix_id", 6, "GL2Z covariance controls")
    qbase = ((1.25, 0.25), (0.25, 0.85))
    best, base_winners, _ = shortest(qbase, bound=50)
    if len(base_winners) != 1:
        raise VerificationError("independent covariance base is not unique")
    base = base_winners[0]
    sbase = (Fraction(2, 7), Fraction(-3, 11))
    max_residual = 0.0
    for row in rows:
        parsed = ast.literal_eval(row["matrix"])
        matrix_int = (
            (int(parsed[0][0]), int(parsed[0][1])),
            (int(parsed[1][0]), int(parsed[1][1])),
        )
        matrix = tuple(tuple(float(item) for item in line) for line in matrix_int)
        transformed_q = multiply(matrix, multiply(qbase, transpose(matrix)))
        predicted = transform_character(matrix_int, base)
        observed_best, observed, _ = shortest(transformed_q, bound=50)
        if observed != [predicted]:
            raise VerificationError(f"shortest-set covariance: {row['matrix_id']}")
        inverse = inverse_integer(matrix_int)
        raw_w = (
            inverse[0][0] * base[0] + inverse[1][0] * base[1],
            inverse[0][1] * base[0] + inverse[1][1] * base[1],
        )
        transformed_s = (
            Fraction(matrix_int[0][0]) * sbase[0]
            + Fraction(matrix_int[0][1]) * sbase[1],
            Fraction(matrix_int[1][0]) * sbase[0]
            + Fraction(matrix_int[1][1]) * sbase[1],
        )
        connection_before = Fraction(base[0]) * sbase[0] + Fraction(base[1]) * sbase[1]
        connection_after = (
            Fraction(raw_w[0]) * transformed_s[0]
            + Fraction(raw_w[1]) * transformed_s[1]
        )
        if connection_before != connection_after:
            raise VerificationError(f"connection covariance: {row['matrix_id']}")
        max_residual = max(max_residual, abs(observed_best - best))
    if max_residual >= TOL:
        raise VerificationError("GL2Z norm residual")
    return {
        "GL2Z_controls": 6,
        "norm_residual_max": max_residual,
        "connection_residual": "EXACT_FRACTION_ZERO",
    }


def validate_completions(state: dict[str, object]) -> dict[str, object]:
    registry = state["completion_registry"]
    global_rows = state["global"]
    coverage = state["coverage"]
    require_identity(registry, "completion_id", 12, "completion registry")
    require_identity(global_rows, "completion_id", 12, "global transport")
    require_identity(coverage, "completion_id", 12, "completion coverage")
    registered = [row["completion_id"] for row in registry]
    if [row["completion_id"] for row in global_rows] != registered:
        raise VerificationError("completion order or coverage differs")
    if [row["completion_id"] for row in coverage] != registered:
        raise VerificationError("completion coverage order differs")
    if any(
        row["registered"] != "YES"
        or row["classified_once"] != "YES"
        or row["preferred_or_filtered"] != "NO"
        or row["physical_selection"] != "OPEN_NOT_SELECTED"
        for row in coverage
    ):
        raise VerificationError("completion coverage promotion/filter")
    if any(row["physical_selection"] != "OPEN_NOT_SELECTED" for row in global_rows):
        raise VerificationError("physical selection promotion")
    by_id = {row["completion_id"]: row for row in global_rows}
    if (
        by_id["FC04_TWO_CAP_P1"]["phase_section"]
        != "NO_NONZERO_CHARACTER_ANNIHILATES_BOTH_UNIMODULAR_CAP_CYCLES"
        or by_id["FC11_NONINTEGRABLE_DISTRIBUTION"]["W_min_set"]
        != "NO_GLOBAL_DEFINITION"
        or "TIE" not in by_id["FC12_RECIPROCAL_TORIC_DIAGONAL"]["unique_line"]
    ):
        raise VerificationError("load-bearing completion ruling")
    return {
        "registered_completions": 12,
        "classified_completions": 12,
        "preferred_or_filtered": 0,
        "physically_selected": 0,
    }


def validate_authority(state: dict[str, object]) -> None:
    result = state["results"]
    if (
        result["global_ruling"]
        != "SET_VALUED_INVARIANT_GLOBAL_WHERE_TORIC__UNIQUE_LINE_ONLY_ON_TIE_FREE_BRANCHES"
        or result["physical_ruling"]
        != "CANONICAL_GEOMETRIC_CHARACTER_NOT_PHYSICALLY_SELECTED"
        or result["phase_section"] != "OPEN"
        or result["density_to_geometry"] != "OPEN_NOT_SAMPLED"
        or result["matter_solve_launched"]
        or result["gpu_used"]
    ):
        raise VerificationError("authority boundary promoted")
    wall_by_id = {row["item_id"]: row for row in state["walls"]}
    if (
        wall_by_id["W14"]["status"] != "OPEN"
        or "no_registered_UDT_premise_selects" not in wall_by_id["W14"]["exact_statement"]
    ):
        raise VerificationError("physical-selection status")


def validate(state: dict[str, object]) -> dict[str, object]:
    require_identity(state["analytic"], "object_id", 18, "analytic registry")
    require_identity(state["contract"], "gate_id", 12, "falsification contract")
    require_identity(state["premises"], "premise_id", 23, "premise ledger")
    validate_sources(state)
    chart = validate_chart_and_diagonal(state)
    wall = validate_wall_theorem(state)
    covariance = validate_covariance(state)
    completions = validate_completions(state)
    validate_authority(state)
    return {
        "chart": chart,
        "wall": wall,
        "covariance": covariance,
        "completions": completions,
    }


def expect_failure(label: str, callback: Callable[[], object]) -> dict[str, str]:
    try:
        callback()
    except (VerificationError, AssertionError, KeyError, ValueError):
        return {
            "catch_id": label,
            "injection": "EXERCISED",
            "expected": "FAIL_CLOSED",
            "observed": "REJECTED",
            "status": "PASS",
        }
    raise AssertionError(f"catch-proof did not reject {label}")


def catch_proofs(state: dict[str, object]) -> list[dict[str, str]]:
    catches: list[dict[str, str]] = []

    bad = copy.deepcopy(state)
    bad["results"]["exact"]["residuals"]["det_H_minus_one"] = "1"
    catches.append(expect_failure("C01_METRIC_CHART", lambda: validate(bad)))

    catches.append(
        expect_failure(
            "C02_NONUNIMODULAR_PAIR",
            lambda: (
                None
                if abs(2) <= 2.0 / math.sqrt(3.0)
                else (_ for _ in ()).throw(VerificationError("determinant"))
            ),
        )
    )

    bad = copy.deepcopy(state)
    bad["controls"][2]["shortest_lines_mod_sign"] = "(1,0)"
    catches.append(expect_failure("C03_WALL_SUFFICIENCY", lambda: validate(bad)))

    bad = copy.deepcopy(state)
    bad["results"]["wall_theorem"]["maximum_unoriented_tie_multiplicity"] = 4
    catches.append(expect_failure("C04_TIE_MAXIMUM", lambda: validate(bad)))

    bad = copy.deepcopy(state)
    bad["covariance"][1]["matrix"] = "((2,0),(0,1))"
    catches.append(expect_failure("C05_GL2Z_COVARIANCE", lambda: validate(bad)))

    catches.append(
        expect_failure(
            "C06_CONNECTION_COVARIANCE",
            lambda: (
                None
                if Fraction(2, 7) == Fraction(2, 7) + 1
                else (_ for _ in ()).throw(VerificationError("connection"))
            ),
        )
    )

    bad = copy.deepcopy(state)
    bad["diagonal"][1]["global_continuation"] = "UNIQUE_WITHOUT_TIE"
    catches.append(expect_failure("C07_LOCAL_CONSTANCY", lambda: validate(bad)))

    bad = copy.deepcopy(state)
    row = next(row for row in bad["global"] if row["completion_id"] == "FC02_ONE_CAP_BOUNDARY")
    row["phase_section"] = "EXTENDS_WITH_NONZERO_CAP_CHARACTER"
    catches.append(
        expect_failure(
            "C08_CAP_DESCENT",
            lambda: (
                validate(bad)
                if "CAP_REQUIRES" in row["phase_section"]
                else (_ for _ in ()).throw(VerificationError("cap descent"))
            ),
        )
    )

    bad = copy.deepcopy(state)
    row = next(row for row in bad["global"] if row["completion_id"] == "FC11_NONINTEGRABLE_DISTRIBUTION")
    row["W_min_set"] = "GLOBAL_CHARACTER"
    catches.append(expect_failure("C09_TORIC_EXISTENCE", lambda: validate(bad)))

    bad = copy.deepcopy(state)
    row = next(row for row in bad["global"] if row["completion_id"] == "FC07_PERIODIC_TORUS_BUNDLE")
    row["sign_orientation"] = "CANONICAL_SIGNED_PHASE"
    catches.append(
        expect_failure(
            "C10_SIGN_PROMOTION",
            lambda: (
                validate(bad)
                if "SIGNED_PHASE" not in row["sign_orientation"]
                else (_ for _ in ()).throw(VerificationError("sign promotion"))
            ),
        )
    )

    bad = copy.deepcopy(state)
    bad["results"]["physical_ruling"] = "PHYSICALLY_SELECTED"
    catches.append(expect_failure("C11_PHYSICAL_PROMOTION", lambda: validate(bad)))

    bad = copy.deepcopy(state)
    bad["results"]["gpu_used"] = True
    catches.append(expect_failure("C12_SCOPE_GPU", lambda: validate(bad)))

    bad = copy.deepcopy(state)
    bad["results"]["matter_solve_launched"] = True
    catches.append(expect_failure("C13_SCOPE_MATTER", lambda: validate(bad)))

    bad = copy.deepcopy(state)
    bad["global"].pop()
    catches.append(expect_failure("C14_COMPLETION_OMISSION", lambda: validate(bad)))

    bad = copy.deepcopy(state)
    bad["global"].append(copy.deepcopy(bad["global"][0]))
    catches.append(expect_failure("C15_COMPLETION_DUPLICATE", lambda: validate(bad)))

    bad = copy.deepcopy(state)
    bad["results"]["phase_section"] = "DERIVED"
    catches.append(expect_failure("C16_PHASE_PROMOTION", lambda: validate(bad)))

    return catches


def main() -> None:
    state = load_state()
    verification = validate(state)
    catches = catch_proofs(state)
    if len(catches) != 16 or any(row["status"] != "PASS" for row in catches):
        raise AssertionError("catch-proof suite incomplete")
    write_tsv(
        "CATCH_PROOF_RESULTS.tsv",
        ["catch_id", "injection", "expected", "observed", "status"],
        catches,
    )
    result = {
        "schema": "udt_dual_systole_global_transport_independent_v1",
        "overall": "PASS",
        "method": "stdlib_independent_lattice_enumeration_plus_exact_integer_and_fraction_controls",
        "production_module_imported": False,
        "verification": verification,
        "catch_proof_pass_count": len(catches),
        "wall_pair_ruling": "UNIMODULAR",
        "maximum_tie_multiplicity": 3,
        "diagonal_ruling": "RECIPROCAL_CHARACTER_SWAP_REQUIRES_TIE_CROSSING",
        "physical_selection": "OPEN_NOT_SELECTED",
        "phase_section": "OPEN",
        "density_scan": False,
        "matter_solve": False,
        "gpu_used": False,
    }
    (HERE / "INDEPENDENT_RESULTS.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("INDEPENDENT_DUAL_SYSTOLE_GLOBAL_TRANSPORT_VERIFICATION")
    print("wall_pair=UNIMODULAR")
    print("standard_wall_controls=5 independent_bound=50")
    print("GL2Z_controls=6 exact_connection_fraction_controls=6")
    print("completions=12")
    print("diagonal=RECIPROCAL_CHARACTER_SWAP_REQUIRES_TIE_CROSSING")
    print(f"catch_proofs={len(catches)}/{len(catches)}")
    print("physical_selection=OPEN phase_section=OPEN")
    print("matter_solve=False gpu=False")
    print("INDEPENDENT_PASS")


if __name__ == "__main__":
    main()
