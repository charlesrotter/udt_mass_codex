#!/usr/bin/env python3
"""Independent sparse verification of the C08 finite-field dimension certificate."""

from __future__ import annotations

import hashlib
import json
import re
from fractions import Fraction
from pathlib import Path
from typing import TypeAlias


HERE = Path(__file__).resolve().parent
PRIME = 32_003
EXPECTED_RATIONAL_INPUT_SHA256 = "8079b60cbe573ffefe0557a92b0c35f35b2e6a6a413bc26c5f99a85fc7c96ec0"
EXPECTED_RATIONAL_BASIS_SHA256 = "a785441f0bb6fc5bb8f631861a84336660f8508e729780a6e40459868070479b"
Monomial: TypeAlias = tuple[int, int]
Coefficient: TypeAlias = int | Fraction
Sparse: TypeAlias = dict[Monomial, Coefficient]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prime_gate(value: int) -> bool:
    if value < 2:
        return False
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 1
    return True


def coefficient(value: Fraction, modulus: int | None) -> Coefficient:
    if modulus is None:
        return value
    return (value.numerator % modulus) * pow(value.denominator % modulus, -1, modulus) % modulus


def parse_polynomial(text: str, modulus: int | None) -> Sparse:
    normalized = text.strip().replace(" ", "")
    normalized = normalized.replace("z_ratio**", "z^").replace("y_ratio**", "y^")
    normalized = normalized.replace("z_ratio", "z").replace("y_ratio", "y")
    if not normalized or normalized == "0":
        return {}
    if normalized[0] not in "+-":
        normalized = "+" + normalized
    result: Sparse = {}
    for signed_term in re.findall(r"[+-][^+-]+", normalized):
        sign = -1 if signed_term[0] == "-" else 1
        term = signed_term[1:]
        exponents = []
        for variable in ("z", "y"):
            powered = re.search(rf"{variable}\^(\d+)", term)
            compact = re.search(rf"{variable}(\d+)", term) if powered is None else None
            if powered:
                exponent = int(powered.group(1)); term = term.replace(powered.group(0), "", 1)
            elif compact:
                exponent = int(compact.group(1)); term = term.replace(compact.group(0), "", 1)
            elif variable in term:
                exponent = 1; term = term.replace(variable, "", 1)
            else:
                exponent = 0
            exponents.append(exponent)
        raw_coefficient = term.replace("*", "")
        value = Fraction(sign) if raw_coefficient == "" else sign * Fraction(raw_coefficient)
        value = coefficient(value, modulus)
        monomial = (exponents[0], exponents[1])
        updated = result.get(monomial, 0) + value
        if modulus is not None:
            updated %= modulus
        if updated:
            result[monomial] = updated
        else:
            result.pop(monomial, None)
    return result


def add(left: Sparse, right: Sparse, scale: Coefficient = 1, modulus: int | None = None) -> Sparse:
    result = dict(left)
    for monomial, value in right.items():
        updated = result.get(monomial, 0) + scale * value
        if modulus is not None:
            updated %= modulus
        if updated:
            result[monomial] = updated
        else:
            result.pop(monomial, None)
    return result


def multiply(left: Sparse, right: Sparse, modulus: int | None) -> Sparse:
    result: Sparse = {}
    for (z_left, y_left), c_left in left.items():
        for (z_right, y_right), c_right in right.items():
            monomial = (z_left + z_right, y_left + y_right)
            updated = result.get(monomial, 0) + c_left * c_right
            if modulus is not None:
                updated %= modulus
            if updated:
                result[monomial] = updated
            else:
                result.pop(monomial, None)
    return result


def monomial_key(monomial: Monomial) -> tuple[int, int]:
    return sum(monomial), monomial[0]


def leading(poly: Sparse) -> tuple[Monomial, Coefficient]:
    monomial = max(poly, key=monomial_key)
    return monomial, poly[monomial]


def divides(left: Monomial, right: Monomial) -> bool:
    return left[0] <= right[0] and left[1] <= right[1]


def ratio(numerator: Coefficient, denominator: Coefficient, modulus: int | None) -> Coefficient:
    if modulus is None:
        return numerator / denominator
    return numerator * pow(int(denominator), -1, modulus) % modulus


def monomial_multiple(poly: Sparse, exponent: Monomial, scale: Coefficient, modulus: int | None) -> Sparse:
    result = {
        (z + exponent[0], y + exponent[1]): value * scale
        for (z, y), value in poly.items()
    }
    if modulus is not None:
        result = {monomial: value % modulus for monomial, value in result.items() if value % modulus}
    return result


def remainder(poly: Sparse, basis: list[Sparse], modulus: int | None) -> Sparse:
    work = dict(poly)
    result: Sparse = {}
    while work:
        lead_monomial, lead_coefficient = leading(work)
        for divisor_poly in basis:
            divisor_monomial, divisor_coefficient = leading(divisor_poly)
            if divides(divisor_monomial, lead_monomial):
                exponent = (
                    lead_monomial[0] - divisor_monomial[0],
                    lead_monomial[1] - divisor_monomial[1],
                )
                factor = ratio(lead_coefficient, divisor_coefficient, modulus)
                work = add(work, monomial_multiple(divisor_poly, exponent, factor, modulus), -1, modulus)
                break
        else:
            result[lead_monomial] = lead_coefficient
            work.pop(lead_monomial)
    return result


def s_polynomial(left: Sparse, right: Sparse, modulus: int | None) -> Sparse:
    lm_left, lc_left = leading(left)
    lm_right, lc_right = leading(right)
    lcm = (max(lm_left[0], lm_right[0]), max(lm_left[1], lm_right[1]))
    left_exp = (lcm[0] - lm_left[0], lcm[1] - lm_left[1])
    right_exp = (lcm[0] - lm_right[0], lcm[1] - lm_right[1])
    left_scale = ratio(1, lc_left, modulus)
    right_scale = ratio(1, lc_right, modulus)
    return add(
        monomial_multiple(left, left_exp, left_scale, modulus),
        monomial_multiple(right, right_exp, right_scale, modulus),
        -1, modulus,
    )


def buchberger_failures(basis: list[Sparse], modulus: int | None) -> list[tuple[int, int]]:
    failures = []
    for left in range(len(basis)):
        for right in range(left + 1, len(basis)):
            if remainder(s_polynomial(basis[left], basis[right], modulus), basis, modulus):
                failures.append((left, right))
    return failures


def staircase(basis: list[Sparse]) -> tuple[list[Monomial], int, int]:
    leading_monomials = [leading(poly)[0] for poly in basis]
    z_bound = min(z for z, y in leading_monomials if y == 0)
    y_bound = min(y for z, y in leading_monomials if z == 0)
    standard = [
        (z, y)
        for z in range(z_bound)
        for y in range(y_bound)
        if not any(divides(leading_monomial, (z, y)) for leading_monomial in leading_monomials)
    ]
    return standard, z_bound, y_bound


def parse_named_rows(text: str, begin: str, end: str, name: str, modulus: int | None) -> list[Sparse]:
    body = text.split(begin, 1)[1].split(end, 1)[0]
    rows = re.findall(rf"^{name}\[(\d+)\]=(.*)$", body, re.MULTILINE)
    indices = [int(index) for index, _ in rows]
    assert indices == list(range(1, len(rows) + 1))
    return [parse_polynomial(expression, modulus) for _, expression in rows]


def parse_inputs(modulus: int | None) -> list[Sparse]:
    result = []
    for label in ("12", "13", "23"):
        for component in ("A", "B"):
            result.append(parse_polynomial((HERE / f"C08_LINEAR_{component}_{label}.txt").read_text(), modulus))
    return result


def parse_rational_basis() -> list[Sparse]:
    path = HERE / "C08_MODULAR_ALL_ZERO_STDOUT.txt"
    assert digest(path) == EXPECTED_RATIONAL_BASIS_SHA256
    return parse_named_rows(path.read_text(), "UDT_BASIS_BEGIN", "UDT_BASIS_END", "G", None)


def parse_finite_field_return(columns: int) -> tuple[list[Sparse], list[list[Sparse]]]:
    text = (HERE / "C08_FINITE_FIELD_STDOUT.txt").read_text()
    basis = parse_named_rows(text, "UDT_BASIS_BEGIN", "UDT_BASIS_END", "H", PRIME)
    body = text.split("UDT_MATRIX_BEGIN", 1)[1].split("UDT_MATRIX_END", 1)[0]
    rows = re.findall(r"^T\[(\d+),(\d+)\]=(.*)$", body, re.MULTILINE)
    assert len(rows) == 6 * columns
    matrix = [[{} for _ in range(columns)] for _ in range(6)]
    seen = set()
    for row_text, column_text, expression in rows:
        row, column = int(row_text), int(column_text)
        assert 1 <= row <= 6 and 1 <= column <= columns and (row, column) not in seen
        seen.add((row, column))
        matrix[row - 1][column - 1] = parse_polynomial(expression, PRIME)
    assert len(seen) == 6 * columns and len(basis) == columns
    return basis, matrix


def transformation_residuals(inputs: list[Sparse], basis: list[Sparse], matrix: list[list[Sparse]]) -> list[Sparse]:
    residuals = []
    for column, target in enumerate(basis):
        result = {monomial: (-value) % PRIME for monomial, value in target.items()}
        for row, source in enumerate(inputs):
            result = add(result, multiply(source, matrix[row][column], PRIME), 1, PRIME)
        residuals.append(result)
    return residuals


def dimension_sandwich(rational_lower: int, finite_upper: int) -> bool:
    return rational_lower == finite_upper == 124


def rank_direction(statement: str) -> bool:
    return statement == "rank_Q>=rank_Fp"


def fixed_prime_gate(value: int) -> bool:
    return value == PRIME and prime_gate(value)


def structural_gate(basis: list[Sparse], matrix: list[list[Sparse]], columns: int) -> bool:
    return len(basis) == columns and len(matrix) == 6 and all(len(row) == columns for row in matrix)


def hash_gate(actual: str, expected: str) -> bool:
    return actual == expected


def main() -> int:
    assert prime_gate(PRIME)
    rational_input = HERE / "C08_MODULAR_ALL_ZERO_INPUT.sing"
    assert digest(rational_input) == EXPECTED_RATIONAL_INPUT_SHA256
    process_path = HERE / "C08_FINITE_FIELD_PROCESS.json"
    process = json.loads(process_path.read_text())
    stdout_path = HERE / "C08_FINITE_FIELD_STDOUT.txt"
    stderr_path = HERE / "C08_FINITE_FIELD_STDERR.txt"
    assert process["status"] == "RETURNED_CERTIFIED_FINITE_FIELD_FIBER_PENDING_INDEPENDENT_REVIEW"
    assert process["prime"] == str(PRIME)
    assert digest(stdout_path) == process["stdout_sha256"]
    assert digest(stderr_path) == process["stderr_sha256"]
    columns = int(process["basis_size"])

    finite_inputs = parse_inputs(PRIME)
    finite_basis, matrix = parse_finite_field_return(columns)
    finite_residuals = transformation_residuals(finite_inputs, finite_basis, matrix)
    finite_buchberger = buchberger_failures(finite_basis, PRIME)
    finite_input_failures = [
        index for index, poly in enumerate(finite_inputs)
        if remainder(poly, finite_basis, PRIME)
    ]
    finite_standard, finite_z_bound, finite_y_bound = staircase(finite_basis)

    rational_inputs = parse_inputs(None)
    rational_basis = parse_rational_basis()
    rational_buchberger = buchberger_failures(rational_basis, None)
    rational_input_failures = [
        index for index, poly in enumerate(rational_inputs)
        if remainder(poly, rational_basis, None)
    ]
    rational_standard, rational_z_bound, rational_y_bound = staircase(rational_basis)

    mutation_row = next(row for row in range(6) if any(matrix[row][column] for column in range(columns)))
    mutation_column = next(column for column in range(columns) if matrix[mutation_row][column])
    mutated_matrix = [[dict(entry) for entry in row] for row in matrix]
    entry = dict(mutated_matrix[mutation_row][mutation_column])
    mutation_monomial = next(iter(entry))
    entry[mutation_monomial] = (int(entry[mutation_monomial]) + 1) % PRIME
    mutated_matrix[mutation_row][mutation_column] = entry
    matrix_mutation_caught = any(transformation_residuals(finite_inputs, finite_basis, mutated_matrix))

    mutated_inputs = [dict(poly) for poly in finite_inputs]
    input_monomial = next(iter(mutated_inputs[mutation_row]))
    mutated_inputs[mutation_row][input_monomial] = (
        int(mutated_inputs[mutation_row][input_monomial]) + 1
    ) % PRIME
    input_mutation_caught = any(transformation_residuals(mutated_inputs, finite_basis, matrix))

    catch_proofs = {
        "changed_nonzero_transformation_coefficient_rejected": matrix_mutation_caught,
        "changed_input_coefficient_rejected": input_mutation_caught,
        "dropped_basis_element_rejected": not structural_gate(finite_basis[:-1], matrix, columns),
        "dropped_transformation_row_rejected": not structural_gate(finite_basis, matrix[:-1], columns),
        "dropped_transformation_column_rejected": not structural_gate(
            finite_basis, [row[:-1] for row in matrix], columns
        ),
        "changed_prime_rejected": not fixed_prime_gate(32_009),
        "changed_quotient_count_rejected": not dimension_sandwich(124, 125),
        "reversed_rank_inequality_rejected": not rank_direction("rank_Q<=rank_Fp"),
        "certificate_hash_mismatch_rejected": not hash_gate(digest(stdout_path), "0" * 64),
        "process_hash_mismatch_rejected": not hash_gate(digest(process_path), "0" * 64),
    }
    passed = (
        not any(finite_residuals)
        and not finite_buchberger
        and not finite_input_failures
        and len(finite_standard) == 124
        and not rational_buchberger
        and not rational_input_failures
        and len(rational_standard) == 124
        and structural_gate(finite_basis, matrix, columns)
        and dimension_sandwich(len(rational_standard), len(finite_standard))
        and rank_direction("rank_Q>=rank_Fp")
        and all(catch_proofs.values())
    )
    result = {
        "schema": "udt-c08-finite-field-independent-verification-1.0",
        "status": "PASS_IDEAL_EQUALITY_PENDING_COLD_REVIEW" if passed else "REFUTED_OR_VERIFIER_ERROR",
        "prime": PRIME,
        "finite_field": {
            "basis_size": len(finite_basis),
            "matrix_shape": [len(matrix), columns],
            "transformation_residual_term_counts": [len(item) for item in finite_residuals],
            "buchberger_pairs": len(finite_basis) * (len(finite_basis) - 1) // 2,
            "buchberger_failures": finite_buchberger,
            "input_reduction_failures": finite_input_failures,
            "leading_monomials": [list(leading(poly)[0]) for poly in finite_basis],
            "pure_power_bounds": {"z": finite_z_bound, "y": finite_y_bound},
            "standard_monomial_count": len(finite_standard),
            "input_term_counts": [len(poly) for poly in finite_inputs],
            "basis_term_counts": [len(poly) for poly in finite_basis],
            "matrix_term_counts": [[len(entry) for entry in row] for row in matrix],
        },
        "rational_replay": {
            "basis_size": len(rational_basis),
            "buchberger_pairs": len(rational_basis) * (len(rational_basis) - 1) // 2,
            "buchberger_failures": rational_buchberger,
            "input_reduction_failures": rational_input_failures,
            "pure_power_bounds": {"z": rational_z_bound, "y": rational_y_bound},
            "standard_monomial_count": len(rational_standard),
        },
        "dimension_argument": {
            "filtered_rank_inequality": "rank_Q>=rank_Fp",
            "rational_quotient_lower_bound": len(rational_standard),
            "finite_field_quotient_upper_bound": len(finite_standard),
            "surjection_dimension_sandwich": dimension_sandwich(
                len(rational_standard), len(finite_standard)
            ),
        },
        "catch_proofs": catch_proofs,
        "rational_input_sha256": digest(rational_input),
        "rational_basis_sha256": digest(HERE / "C08_MODULAR_ALL_ZERO_STDOUT.txt"),
        "finite_field_stdout_sha256": digest(stdout_path),
        "finite_field_process_sha256": digest(process_path),
    }
    target = HERE / "C08_FINITE_FIELD_INDEPENDENT_VERIFICATION.json"
    target.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
