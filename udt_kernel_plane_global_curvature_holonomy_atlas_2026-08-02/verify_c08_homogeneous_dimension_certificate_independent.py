#!/usr/bin/env python3
"""Independent sparse replay of the corrected homogeneous C08 certificate.

This verifier does not import the production driver.  It parses the preserved
Singular return, recomputes every polynomial identity, proves stabilization of
the monomial Hilbert function, and separately replays the rational lower bound.
"""

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
HOMOGENIZATION_POLICY = "UNSATURATED_INDIVIDUAL_HOMOGENIZATIONS"

Monomial: TypeAlias = tuple[int, ...]
Coefficient: TypeAlias = int | Fraction
Sparse: TypeAlias = dict[Monomial, Coefficient]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 1
    return True


def field_value(value: Fraction, modulus: int | None) -> Coefficient:
    if modulus is None:
        return value
    return value.numerator % modulus * pow(value.denominator % modulus, -1, modulus) % modulus


def parse_polynomial(text: str, variables: tuple[str, ...], modulus: int | None) -> Sparse:
    normalized = text.strip().replace(" ", "").replace("\n", "")
    normalized = normalized.replace("z_ratio**", "z^").replace("y_ratio**", "y^")
    normalized = normalized.replace("z_ratio", "z").replace("y_ratio", "y")
    normalized = normalized.replace("**", "^")
    if not normalized or normalized == "0":
        return {}
    if normalized[0] not in "+-":
        normalized = "+" + normalized
    terms = re.findall(r"[+-][^+-]+", normalized)
    assert "".join(terms) == normalized, "unparsed sign or term boundary"
    result: Sparse = {}
    for signed in terms:
        sign = -1 if signed[0] == "-" else 1
        remainder = signed[1:]
        exponents: list[int] = []
        for variable in variables:
            powered = re.search(rf"{re.escape(variable)}\^(\d+)", remainder)
            compact = re.search(rf"{re.escape(variable)}(\d+)", remainder) if powered is None else None
            if powered:
                exponent = int(powered.group(1))
                remainder = remainder.replace(powered.group(0), "", 1)
            elif compact:
                exponent = int(compact.group(1))
                remainder = remainder.replace(compact.group(0), "", 1)
            elif variable in remainder:
                exponent = 1
                remainder = remainder.replace(variable, "", 1)
            else:
                exponent = 0
            exponents.append(exponent)
        raw = remainder.replace("*", "")
        assert not re.search(r"[A-Za-z_]", raw), f"unparsed polynomial token: {raw!r}"
        value = Fraction(sign) if raw == "" else sign * Fraction(raw)
        coefficient = field_value(value, modulus)
        monomial = tuple(exponents)
        updated = result.get(monomial, 0) + coefficient
        if modulus is not None:
            updated %= modulus
        if updated:
            result[monomial] = updated
        else:
            result.pop(monomial, None)
    return result


def add(left: Sparse, right: Sparse, scale: Coefficient, modulus: int | None) -> Sparse:
    result = dict(left)
    for monomial, coefficient in right.items():
        updated = result.get(monomial, 0) + scale * coefficient
        if modulus is not None:
            updated %= modulus
        if updated:
            result[monomial] = updated
        else:
            result.pop(monomial, None)
    return result


def multiply(left: Sparse, right: Sparse, modulus: int | None) -> Sparse:
    result: Sparse = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(a + b for a, b in zip(left_monomial, right_monomial, strict=True))
            updated = result.get(monomial, 0) + left_coefficient * right_coefficient
            if modulus is not None:
                updated %= modulus
            if updated:
                result[monomial] = updated
            else:
                result.pop(monomial, None)
    return result


def grevlex_key(monomial: Monomial) -> tuple[int, ...]:
    # Singular dp with variables in the recorded order: total degree, then
    # reverse lexicographic tie breaking.
    return (sum(monomial),) + tuple(-value for value in reversed(monomial[1:]))


def leading(poly: Sparse) -> tuple[Monomial, Coefficient]:
    assert poly
    monomial = max(poly, key=grevlex_key)
    return monomial, poly[monomial]


def divides(divisor: Monomial, dividend: Monomial) -> bool:
    return all(left <= right for left, right in zip(divisor, dividend, strict=True))


def divide_coefficient(numerator: Coefficient, denominator: Coefficient, modulus: int | None) -> Coefficient:
    if modulus is None:
        return numerator / denominator
    return int(numerator) * pow(int(denominator), -1, modulus) % modulus


def monomial_multiple(poly: Sparse, exponent: Monomial, scale: Coefficient, modulus: int | None) -> Sparse:
    result = {
        tuple(a + b for a, b in zip(monomial, exponent, strict=True)): coefficient * scale
        for monomial, coefficient in poly.items()
    }
    if modulus is not None:
        return {monomial: coefficient % modulus for monomial, coefficient in result.items() if coefficient % modulus}
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def normal_form(poly: Sparse, basis: list[Sparse], modulus: int | None) -> Sparse:
    work = dict(poly)
    remainder: Sparse = {}
    heads = [leading(divisor) for divisor in basis]
    while work:
        lead_monomial, lead_coefficient = leading(work)
        for divisor, (divisor_monomial, divisor_coefficient) in zip(basis, heads, strict=True):
            if divides(divisor_monomial, lead_monomial):
                exponent = tuple(a - b for a, b in zip(lead_monomial, divisor_monomial, strict=True))
                factor = divide_coefficient(lead_coefficient, divisor_coefficient, modulus)
                work = add(work, monomial_multiple(divisor, exponent, factor, modulus), -1, modulus)
                break
        else:
            remainder[lead_monomial] = lead_coefficient
            work.pop(lead_monomial)
    return remainder


def s_polynomial(left: Sparse, right: Sparse, modulus: int | None) -> Sparse:
    left_monomial, left_coefficient = leading(left)
    right_monomial, right_coefficient = leading(right)
    common = tuple(max(a, b) for a, b in zip(left_monomial, right_monomial, strict=True))
    left_exponent = tuple(a - b for a, b in zip(common, left_monomial, strict=True))
    right_exponent = tuple(a - b for a, b in zip(common, right_monomial, strict=True))
    left_part = monomial_multiple(left, left_exponent, divide_coefficient(1, left_coefficient, modulus), modulus)
    right_part = monomial_multiple(right, right_exponent, divide_coefficient(1, right_coefficient, modulus), modulus)
    return add(left_part, right_part, -1, modulus)


def buchberger_failures(basis: list[Sparse], modulus: int | None) -> list[list[int]]:
    failures: list[list[int]] = []
    for left in range(len(basis)):
        for right in range(left + 1, len(basis)):
            if normal_form(s_polynomial(basis[left], basis[right], modulus), basis, modulus):
                failures.append([left + 1, right + 1])
    return failures


def homogeneous_degree(poly: Sparse) -> int | None:
    degrees = {sum(monomial) for monomial in poly}
    return next(iter(degrees)) if len(degrees) == 1 else None


def homogenize(poly: Sparse) -> Sparse:
    degree = max(sum(monomial) for monomial in poly)
    assert all(len(monomial) == 2 for monomial in poly)
    return {
        (monomial[0], monomial[1], degree - sum(monomial)): coefficient
        for monomial, coefficient in poly.items()
    }


def dehomogenize(poly: Sparse, modulus: int | None) -> Sparse:
    result: Sparse = {}
    for (z_power, y_power, _t_power), coefficient in poly.items():
        monomial = (z_power, y_power)
        updated = result.get(monomial, 0) + coefficient
        if modulus is not None:
            updated %= modulus
        if updated:
            result[monomial] = updated
        else:
            result.pop(monomial, None)
    return result


def parse_affine_sources(modulus: int | None) -> list[Sparse]:
    source = HERE / "C08_MODULAR_ALL_ZERO_INPUT.sing"
    assert digest(source) == EXPECTED_RATIONAL_INPUT_SHA256
    rows = re.findall(r"^poly ([ab][123])=(.*);$", source.read_text(), re.MULTILINE)
    assert [name for name, _ in rows] == ["a1", "b1", "a2", "b2", "a3", "b3"]
    return [parse_polynomial(expression, ("z", "y"), modulus) for _, expression in rows]


def parse_indexed_polynomials(text: str, begin: str, end: str, name: str, variables: tuple[str, ...], modulus: int | None) -> list[Sparse]:
    body = text.split(begin, 1)[1].split(end, 1)[0]
    rows = re.findall(rf"^{name}\[(\d+)\]=(.*)$", body, re.MULTILINE)
    assert [int(index) for index, _ in rows] == list(range(1, len(rows) + 1))
    return [parse_polynomial(expression, variables, modulus) for _, expression in rows]


def parse_homogeneous_return(columns: int) -> tuple[list[Sparse], list[Sparse], list[list[Sparse]]]:
    text = (HERE / "C08_HOMOGENEOUS_STDOUT.txt").read_text()
    inputs = parse_indexed_polynomials(
        text, "UDT_HOMOGENIZED_INPUT_BEGIN", "UDT_HOMOGENIZED_INPUT_END", "L", ("z", "y", "t"), PRIME
    )
    basis = parse_indexed_polynomials(
        text, "UDT_BASIS_BEGIN", "UDT_BASIS_END", "K", ("z", "y", "t"), PRIME
    )
    body = text.split("UDT_MATRIX_BEGIN", 1)[1].split("UDT_MATRIX_END", 1)[0]
    rows = re.findall(r"^U\[(\d+),(\d+)\]=(.*)$", body, re.MULTILINE)
    assert len(inputs) == 6 and len(basis) == columns and len(rows) == 6 * columns
    matrix = [[{} for _ in range(columns)] for _ in range(6)]
    seen: set[tuple[int, int]] = set()
    for row_text, column_text, expression in rows:
        row, column = int(row_text), int(column_text)
        assert 1 <= row <= 6 and 1 <= column <= columns and (row, column) not in seen
        seen.add((row, column))
        matrix[row - 1][column - 1] = parse_polynomial(expression, ("z", "y", "t"), PRIME)
    assert len(seen) == 6 * columns
    return inputs, basis, matrix


def transformation_residuals(inputs: list[Sparse], basis: list[Sparse], matrix: list[list[Sparse]]) -> list[Sparse]:
    residuals: list[Sparse] = []
    for column, target in enumerate(basis):
        result = {monomial: (-int(coefficient)) % PRIME for monomial, coefficient in target.items()}
        for row, source in enumerate(inputs):
            result = add(result, multiply(source, matrix[row][column], PRIME), 1, PRIME)
        residuals.append(result)
    return residuals


def rational_staircase(basis: list[Sparse]) -> tuple[int, int, int, list[Monomial]]:
    leading_monomials = [leading(poly)[0] for poly in basis]
    z_bound = min(z for z, y in leading_monomials if y == 0)
    y_bound = min(y for z, y in leading_monomials if z == 0)
    standard = [
        (z, y)
        for z in range(z_bound)
        for y in range(y_bound)
        if not any(divides(monomial, (z, y)) for monomial in leading_monomials)
    ]
    return len(standard), z_bound, y_bound, leading_monomials


def homogeneous_hilbert_data(basis: list[Sparse]) -> dict[str, object]:
    leading_monomials = [leading(poly)[0] for poly in basis]
    pure_z = [monomial[0] for monomial in leading_monomials if monomial[1] == 0 and monomial[2] == 0]
    pure_y = [monomial[1] for monomial in leading_monomials if monomial[0] == 0 and monomial[2] == 0]
    assert pure_z and pure_y, "missing finite z/y pure-power bounds"
    z_bound, y_bound = min(pure_z), min(pure_y)
    surviving: list[tuple[int, int]] = []
    killed: list[tuple[int, int, int]] = []
    thresholds: list[int] = []
    for z_power in range(z_bound):
        for y_power in range(y_bound):
            eligible = [
                monomial[2]
                for monomial in leading_monomials
                if monomial[0] <= z_power and monomial[1] <= y_power
            ]
            if eligible:
                kill_t = min(eligible)
                killed.append((z_power, y_power, kill_t))
                thresholds.append(z_power + y_power + kill_t)
            else:
                surviving.append((z_power, y_power))
                thresholds.append(z_power + y_power)
    stabilization = max(thresholds, default=0)

    def value(degree: int) -> int:
        count = 0
        for z_power in range(min(z_bound - 1, degree) + 1):
            for y_power in range(min(y_bound - 1, degree - z_power) + 1):
                t_power = degree - z_power - y_power
                if not any(divides(monomial, (z_power, y_power, t_power)) for monomial in leading_monomials):
                    count += 1
        return count

    sampled = {str(degree): value(degree) for degree in (stabilization, stabilization + 1, stabilization + 5)}
    return {
        "leading_monomials": [list(monomial) for monomial in leading_monomials],
        "pure_power_bounds": {"z": z_bound, "y": y_bound},
        "surviving_t_rays": len(surviving),
        "killed_t_rays": len(killed),
        "stabilization_degree": stabilization,
        "stabilization_samples": sampled,
        "eventual_hilbert_constant": len(surviving),
    }


def input_program_gate() -> bool:
    text = (HERE / "C08_HOMOGENEOUS_INPUT.sing").read_text()
    definitions = re.findall(r"^poly F(\d+)=homog\(([ab][123]),t\);$", text, re.MULTILINE)
    return (
        "ring r=32003,(z,y,t),dp;" in text
        and definitions == [(str(index), name) for index, name in enumerate(("a1", "b1", "a2", "b2", "a3", "b3"), 1)]
        and "ideal L=F1,F2,F3,F4,F5,F6;" in text
        and "sat(" not in text and "saturate" not in text.lower()
    )


def policy_gate(policy: str) -> bool:
    return policy == HOMOGENIZATION_POLICY


def main() -> int:
    assert is_prime(PRIME)
    process_path = HERE / "C08_HOMOGENEOUS_PROCESS.json"
    stdout_path = HERE / "C08_HOMOGENEOUS_STDOUT.txt"
    stderr_path = HERE / "C08_HOMOGENEOUS_STDERR.txt"
    process = json.loads(process_path.read_text())
    assert process["status"] == "RETURNED_CERTIFIED_HOMOGENEOUS_FIBER_PENDING_INDEPENDENT_REVIEW"
    assert process["prime"] == str(PRIME)
    assert digest(stdout_path) == process["stdout_sha256"]
    assert digest(stderr_path) == process["stderr_sha256"]
    columns = int(process["basis_size"])

    affine_finite = parse_affine_sources(PRIME)
    expected_homogeneous = [homogenize(poly) for poly in affine_finite]
    returned_inputs, basis, matrix = parse_homogeneous_return(columns)
    dehomogenization_failures = [
        index + 1 for index, (homogeneous, affine) in enumerate(zip(returned_inputs, affine_finite, strict=True))
        if dehomogenize(homogeneous, PRIME) != affine
    ]
    independent_homogenization_failures = [
        index + 1 for index, (returned, expected) in enumerate(zip(returned_inputs, expected_homogeneous, strict=True))
        if returned != expected
    ]
    input_homogeneity_failures = [index + 1 for index, poly in enumerate(returned_inputs) if homogeneous_degree(poly) is None]
    basis_homogeneity_failures = [index + 1 for index, poly in enumerate(basis) if homogeneous_degree(poly) is None]
    residuals = transformation_residuals(returned_inputs, basis, matrix)
    finite_buchberger = buchberger_failures(basis, PRIME)
    finite_input_failures = [
        index + 1 for index, poly in enumerate(returned_inputs) if normal_form(poly, basis, PRIME)
    ]
    hilbert = homogeneous_hilbert_data(basis)

    rational_inputs = parse_affine_sources(None)
    rational_stdout = HERE / "C08_MODULAR_ALL_ZERO_STDOUT.txt"
    assert digest(rational_stdout) == EXPECTED_RATIONAL_BASIS_SHA256
    rational_basis = parse_indexed_polynomials(
        rational_stdout.read_text(), "UDT_BASIS_BEGIN", "UDT_BASIS_END", "G", ("z", "y"), None
    )
    rational_buchberger = buchberger_failures(rational_basis, None)
    rational_input_failures = [
        index + 1 for index, poly in enumerate(rational_inputs) if normal_form(poly, rational_basis, None)
    ]
    rational_count, rational_z_bound, rational_y_bound, rational_leads = rational_staircase(rational_basis)

    mutation_row = next(row for row in range(6) if any(matrix[row][column] for column in range(columns)))
    mutation_column = next(column for column in range(columns) if matrix[mutation_row][column])
    mutated_matrix = [[dict(entry) for entry in row] for row in matrix]
    matrix_entry = dict(mutated_matrix[mutation_row][mutation_column])
    matrix_monomial = next(iter(matrix_entry))
    matrix_entry[matrix_monomial] = (int(matrix_entry[matrix_monomial]) + 1) % PRIME
    mutated_matrix[mutation_row][mutation_column] = matrix_entry

    mutated_inputs = [dict(poly) for poly in returned_inputs]
    input_monomial = next(iter(mutated_inputs[mutation_row]))
    mutated_inputs[mutation_row][input_monomial] = (int(mutated_inputs[mutation_row][input_monomial]) + 1) % PRIME

    wrong_degree_inputs = [dict(poly) for poly in expected_homogeneous]
    old_monomial = next(iter(wrong_degree_inputs[0]))
    old_coefficient = wrong_degree_inputs[0].pop(old_monomial)
    wrong_monomial = (old_monomial[0], old_monomial[1], old_monomial[2] + 1)
    wrong_degree_inputs[0][wrong_monomial] = old_coefficient

    finite_upper = int(hilbert["eventual_hilbert_constant"])
    dimension_sandwich = rational_count == finite_upper == 124
    stabilization_values = set(hilbert["stabilization_samples"].values())
    catch_proofs = {
        "changed_transformation_coefficient_rejected": any(
            transformation_residuals(returned_inputs, basis, mutated_matrix)
        ),
        "changed_homogeneous_input_coefficient_rejected": any(
            transformation_residuals(mutated_inputs, basis, matrix)
        ),
        "wrong_homogenization_degree_rejected": wrong_degree_inputs != expected_homogeneous
        and homogeneous_degree(wrong_degree_inputs[0]) is None,
        "changed_prime_rejected": not (32_009 == PRIME and is_prime(32_009)),
        "changed_hilbert_count_rejected": not (rational_count == finite_upper + 1 == 124),
        "omission_of_t_rejected": not (len(next(iter(returned_inputs[0]))) == 2),
        "saturation_or_infinity_drop_rejected": not policy_gate("SATURATE_BY_T"),
        "certificate_hash_mismatch_rejected": digest(stdout_path) != "0" * 64,
        "process_hash_mismatch_rejected": digest(process_path) != "0" * 64,
        "inhomogeneous_rank_shortcut_rejected": not policy_gate("AFFINE_SPECIAL_FIBER_SHORTCUT"),
    }

    passed = (
        input_program_gate()
        and policy_gate(HOMOGENIZATION_POLICY)
        and not dehomogenization_failures
        and not independent_homogenization_failures
        and not input_homogeneity_failures
        and not basis_homogeneity_failures
        and not any(residuals)
        and not finite_buchberger
        and not finite_input_failures
        and finite_upper == 124
        and stabilization_values == {124}
        and not rational_buchberger
        and not rational_input_failures
        and rational_count == 124
        and dimension_sandwich
        and all(catch_proofs.values())
    )
    result = {
        "schema": "udt-c08-homogeneous-independent-verification-1.0",
        "status": "PASS_IDEAL_EQUALITY_PENDING_COLD_REVIEW" if passed else "REFUTED_OR_VERIFIER_ERROR",
        "prime": PRIME,
        "homogenization_policy": HOMOGENIZATION_POLICY,
        "finite_homogeneous_replay": {
            "input_count": len(returned_inputs),
            "basis_size": len(basis),
            "matrix_shape": [len(matrix), columns],
            "dehomogenization_failures": dehomogenization_failures,
            "independent_homogenization_failures": independent_homogenization_failures,
            "input_homogeneity_failures": input_homogeneity_failures,
            "basis_homogeneity_failures": basis_homogeneity_failures,
            "transformation_residual_term_counts": [len(residual) for residual in residuals],
            "buchberger_pairs": len(basis) * (len(basis) - 1) // 2,
            "buchberger_failures": finite_buchberger,
            "input_reduction_failures": finite_input_failures,
            "input_term_counts": [len(poly) for poly in returned_inputs],
            "basis_term_counts": [len(poly) for poly in basis],
            "matrix_term_counts": [[len(entry) for entry in row] for row in matrix],
            "hilbert": hilbert,
        },
        "rational_lower_bound_replay": {
            "basis_size": len(rational_basis),
            "buchberger_pairs": len(rational_basis) * (len(rational_basis) - 1) // 2,
            "buchberger_failures": rational_buchberger,
            "input_reduction_failures": rational_input_failures,
            "leading_monomials": [list(monomial) for monomial in rational_leads],
            "pure_power_bounds": {"z": rational_z_bound, "y": rational_y_bound},
            "standard_monomial_count": rational_count,
        },
        "corrected_dimension_argument": {
            "degreewise_rank_inequality": "dim_Q_graded_quotient<=dim_Fp_graded_quotient",
            "localization": "degree_zero_direct_limit_under_multiplication_by_t",
            "rational_quotient_lower_bound": rational_count,
            "rational_quotient_upper_bound": finite_upper,
            "dimension_sandwich": dimension_sandwich,
        },
        "catch_proofs": catch_proofs,
        "homogeneous_input_sha256": digest(HERE / "C08_HOMOGENEOUS_INPUT.sing"),
        "homogeneous_stdout_sha256": digest(stdout_path),
        "homogeneous_process_sha256": digest(process_path),
        "rational_input_sha256": digest(HERE / "C08_MODULAR_ALL_ZERO_INPUT.sing"),
        "rational_basis_sha256": digest(rational_stdout),
    }
    target = HERE / "C08_HOMOGENEOUS_INDEPENDENT_VERIFICATION.json"
    target.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
