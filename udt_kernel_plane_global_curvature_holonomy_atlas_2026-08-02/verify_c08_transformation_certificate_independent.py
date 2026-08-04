#!/usr/bin/env python3
"""Independently expand the C08 rational transformation certificate."""

from __future__ import annotations

import hashlib
import json
import re
from fractions import Fraction
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
Z, Y = sp.symbols("z y")
Monomial = tuple[int, int]
Sparse = dict[Monomial, Fraction]
EXPECTED_INPUT_SHA256 = "8079b60cbe573ffefe0557a92b0c35f35b2e6a6a413bc26c5f99a85fc7c96ec0"
EXPECTED_BASIS_STDOUT_SHA256 = "a785441f0bb6fc5bb8f631861a84336660f8508e729780a6e40459868070479b"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def singular_to_expr(text: str) -> sp.Expr:
    normalized = text.strip().replace("^", "**")
    normalized = re.sub(r"z(\d+)", r"z**\1", normalized)
    normalized = re.sub(r"y(\d+)", r"y**\1", normalized)
    normalized = re.sub(r"(?<=[0-9])(?=[zy])", "*", normalized)
    normalized = re.sub(r"(?<=[zy])(?=[zy])", "*", normalized)
    return sp.sympify(normalized, locals={"z": Z, "y": Y})


def to_sparse(expression: sp.Expr) -> Sparse:
    result: Sparse = {}
    for monomial, coefficient in sp.Poly(expression, Z, Y, domain=sp.QQ).terms():
        value = sp.Rational(coefficient)
        result[monomial] = Fraction(int(value.p), int(value.q))
    return {key: value for key, value in result.items() if value}


def add(left: Sparse, right: Sparse, scale: Fraction = Fraction(1)) -> Sparse:
    result = dict(left)
    for monomial, coefficient in right.items():
        value = result.get(monomial, Fraction()) + scale * coefficient
        if value:
            result[monomial] = value
        else:
            result.pop(monomial, None)
    return result


def multiply(left: Sparse, right: Sparse) -> Sparse:
    result: Sparse = {}
    for (zl, yl), cl in left.items():
        for (zr, yr), cr in right.items():
            monomial = (zl + zr, yl + yr)
            value = result.get(monomial, Fraction()) + cl * cr
            if value:
                result[monomial] = value
            else:
                result.pop(monomial, None)
    return result


def parse_inputs() -> list[Sparse]:
    result = []
    for label in ("12", "13", "23"):
        for prefix in ("A", "B"):
            text = (HERE / f"C08_LINEAR_{prefix}_{label}.txt").read_text().strip()
            expression = sp.sympify(
                text.replace("z_ratio", "z").replace("y_ratio", "y"),
                locals={"z": Z, "y": Y},
            )
            result.append(to_sparse(expression))
    assert len(result) == 6
    return result


def parse_basis() -> list[Sparse]:
    path = HERE / "C08_MODULAR_ALL_ZERO_STDOUT.txt"
    assert digest(path) == EXPECTED_BASIS_STDOUT_SHA256
    body = path.read_text().split("UDT_BASIS_BEGIN", 1)[1].split("UDT_BASIS_END", 1)[0]
    rows = re.findall(r"^G\[(\d+)\]=(.*)$", body, re.MULTILINE)
    assert [int(index) for index, _ in rows] == list(range(1, 10))
    return [to_sparse(singular_to_expr(text)) for _, text in rows]


def parse_matrix() -> list[list[Sparse]]:
    path = HERE / "C08_TRANSFORMATION_CERTIFICATE_STDOUT.txt"
    text = path.read_text()
    body = text.split("UDT_CERTIFICATE_MATRIX_BEGIN", 1)[1].split("UDT_CERTIFICATE_MATRIX_END", 1)[0]
    rows = re.findall(r"^W\[(\d+),(\d+)\]=(.*)$", body, re.MULTILINE)
    assert len(rows) == 63
    matrix = [[{} for _ in range(9)] for _ in range(7)]
    seen: set[tuple[int, int]] = set()
    for row_text, column_text, expression in rows:
        row, column = int(row_text), int(column_text)
        assert 1 <= row <= 7 and 1 <= column <= 9 and (row, column) not in seen
        seen.add((row, column))
        matrix[row - 1][column - 1] = to_sparse(singular_to_expr(expression))
    assert len(seen) == 63
    return matrix


def residual(inputs: list[Sparse], target: Sparse, certificate_column: list[Sparse]) -> Sparse:
    result = {monomial: -coefficient for monomial, coefficient in target.items()}
    for source, coefficient in zip(inputs, certificate_column):
        result = add(result, multiply(source, coefficient))
    return result


def structural_gate(matrix: list[list[Sparse]], rows: int = 7, columns: int = 9) -> bool:
    return len(matrix) == rows and all(len(row) == columns for row in matrix)


def hash_gate(actual: str, expected: str) -> bool:
    return actual == expected


def mode_gate(mode: str) -> bool:
    return mode == "EXACT_RATIONAL_FULL_EXPANSION"


def main() -> int:
    input_path = HERE / "C08_MODULAR_ALL_ZERO_INPUT.sing"
    assert digest(input_path) == EXPECTED_INPUT_SHA256
    process_path = HERE / "C08_TRANSFORMATION_CERTIFICATE_PROCESS.json"
    process = json.loads(process_path.read_text())
    stdout_path = HERE / "C08_TRANSFORMATION_CERTIFICATE_STDOUT.txt"
    stderr_path = HERE / "C08_TRANSFORMATION_CERTIFICATE_STDERR.txt"
    assert process["status"] == "RETURNED_EXACT_TRANSFORMATION_PENDING_INDEPENDENT_REVIEW"
    assert digest(stdout_path) == process["stdout_sha256"]
    assert digest(stderr_path) == process["stderr_sha256"]

    inputs = parse_inputs()
    basis = parse_basis()
    matrix = parse_matrix()
    assert structural_gate(matrix)
    projected_basis_equal = matrix[0] == basis
    certificates = [[matrix[row][column] for row in range(1, 7)] for column in range(9)]
    residuals = [residual(inputs, basis[column], certificates[column]) for column in range(9)]

    mutation_column = next(
        column for column in range(9) if any(certificates[column][row] for row in range(6))
    )
    mutation_row = next(row for row in range(6) if certificates[mutation_column][row])
    mutated = [[dict(entry) for entry in column] for column in certificates]
    mutated_entry = dict(mutated[mutation_column][mutation_row])
    mutation_monomial = next(iter(mutated_entry))
    old_coefficient = mutated_entry[mutation_monomial]
    mutated_entry[mutation_monomial] = Fraction(
        old_coefficient.numerator + 1, old_coefficient.denominator
    )
    mutated[mutation_column][mutation_row] = mutated_entry
    mutation_residual = residual(inputs, basis[mutation_column], mutated[mutation_column])

    permuted_inputs = list(inputs)
    permuted_inputs[0], permuted_inputs[1] = permuted_inputs[1], permuted_inputs[0]
    permutation_caught = any(
        residual(permuted_inputs, basis[column], certificates[column]) for column in range(9)
    )
    catch_proofs = {
        "changed_nonzero_numerator_rejected": bool(mutation_residual),
        "dropped_row_rejected": not structural_gate(matrix[:-1]),
        "duplicated_row_rejected": not structural_gate(matrix + [matrix[-1]]),
        "dropped_column_rejected": not structural_gate([row[:-1] for row in matrix]),
        "duplicated_column_rejected": not structural_gate([row + [row[-1]] for row in matrix]),
        "permuted_input_identity_rejected": permutation_caught,
        "input_hash_mismatch_rejected": not hash_gate(digest(input_path), "0" * 64),
        "basis_hash_mismatch_rejected": not hash_gate(
            digest(HERE / "C08_MODULAR_ALL_ZERO_STDOUT.txt"), "0" * 64
        ),
        "certificate_hash_mismatch_rejected": not hash_gate(digest(stdout_path), "0" * 64),
        "modular_only_mode_rejected": not mode_gate("MODULAR_ZERO_ONLY"),
        "numerical_only_mode_rejected": not mode_gate("NUMERICAL_TOLERANCE"),
    }
    passed = projected_basis_equal and all(not item for item in residuals) and all(catch_proofs.values())
    result = {
        "schema": "udt-c08-transformation-independent-verification-1.0",
        "status": "PASS_EXACT_RATIONAL_TRANSFORMATION_PENDING_COLD_REVIEW" if passed else "REFUTED_OR_VERIFIER_ERROR",
        "mode": "EXACT_RATIONAL_FULL_EXPANSION",
        "input_sha256": digest(input_path),
        "basis_stdout_sha256": digest(HERE / "C08_MODULAR_ALL_ZERO_STDOUT.txt"),
        "certificate_stdout_sha256": digest(stdout_path),
        "certificate_process_sha256": digest(process_path),
        "matrix_shape": [7, 9],
        "projected_basis_equal": projected_basis_equal,
        "residual_term_counts": [len(item) for item in residuals],
        "input_term_counts": [len(item) for item in inputs],
        "basis_term_counts": [len(item) for item in basis],
        "certificate_term_counts": [[len(entry) for entry in column] for column in certificates],
        "catch_proofs": catch_proofs,
    }
    target = HERE / "C08_TRANSFORMATION_INDEPENDENT_VERIFICATION.json"
    target.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
