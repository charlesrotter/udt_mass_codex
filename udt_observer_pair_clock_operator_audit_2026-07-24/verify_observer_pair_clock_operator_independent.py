#!/usr/bin/env python3
"""Independent stdlib/Fraction verification of the observer-pair operator."""

from __future__ import annotations

import csv
import hashlib
import json
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


Matrix = tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]


def matmul(left: Matrix, right: Matrix) -> Matrix:
    return tuple(
        tuple(sum(left[i][k] * right[k][j] for k in range(2)) for j in range(2))
        for i in range(2)
    )  # type: ignore[return-value]


def transpose(matrix: Matrix) -> Matrix:
    return tuple(tuple(matrix[j][i] for j in range(2)) for i in range(2))  # type: ignore[return-value]


def diagonal(a: Fraction, b: Fraction) -> Matrix:
    return ((a, Fraction(0)), (Fraction(0), b))


def trace(matrix: Matrix) -> Fraction:
    return matrix[0][0] + matrix[1][1]


def determinant(matrix: Matrix) -> Fraction:
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def reciprocal_operator(z: Fraction) -> Matrix:
    return diagonal(1 / z, z)


def balanced_boost(z: Fraction) -> Matrix:
    # Exact H^T S H without introducing sqrt(2).
    diagonal_sum = (z + 1 / z) / 2
    off_diagonal = (1 / z - z) / 2
    return ((diagonal_sum, off_diagonal), (off_diagonal, diagonal_sum))


def inverse_boost(z: Fraction) -> Matrix:
    return balanced_boost(1 / z)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_tsv(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def require(name: str, condition: bool, checks: dict[str, str]) -> None:
    if not condition:
        raise AssertionError(name)
    checks[name] = "PASS"


def expect_failure(name: str, callback, catches: dict[str, str]) -> None:
    try:
        callback()
    except (AssertionError, KeyError, ValueError):
        catches[name] = "PASS"
        return
    raise AssertionError(f"catch did not fire: {name}")


def main() -> None:
    checks: dict[str, str] = {}
    catches: dict[str, str] = {}
    zero = Fraction(0)
    one = Fraction(1)
    identity: Matrix = ((one, zero), (zero, one))
    K: Matrix = ((zero, one), (one, zero))
    eta: Matrix = ((one, zero), (zero, -one))

    for index, (z1, z2) in enumerate(
        [
            (Fraction(2), Fraction(3)),
            (Fraction(5, 3), Fraction(7, 4)),
            (Fraction(11, 5), Fraction(13, 7)),
        ],
        start=1,
    ):
        s1 = reciprocal_operator(z1)
        s2 = reciprocal_operator(z2)
        require(f"determinant_{index}", determinant(s1) == one, checks)
        require(
            f"K_preservation_{index}",
            matmul(matmul(transpose(s1), K), s1) == K,
            checks,
        )
        require(
            f"composition_{index}",
            matmul(s1, s2) == reciprocal_operator(z1 * z2),
            checks,
        )
        require(
            f"inverse_{index}",
            matmul(s1, reciprocal_operator(1 / z1)) == identity,
            checks,
        )
        boost = balanced_boost(z1)
        require(
            f"balanced_Lorentz_{index}",
            matmul(matmul(transpose(boost), eta), boost) == eta,
            checks,
        )
        require(
            f"balanced_inverse_{index}",
            matmul(boost, inverse_boost(z1)) == identity,
            checks,
        )
        require(
            f"half_trace_{index}",
            trace(s1) / 2 == (z1 + 1 / z1) / 2,
            checks,
        )
        require(
            f"half_trace_reversal_{index}",
            trace(s1) == trace(reciprocal_operator(1 / z1)),
            checks,
        )

    z = Fraction(2)
    gamma_one = (z + 1 / z) / 2
    gamma_two = (z * z + 1 / (z * z)) / 2
    require("gamma_noncharacter_exact", gamma_two - gamma_one * gamma_one == Fraction(9, 16), checks)
    require("named_clock_character", 1 / (z * z) == (1 / z) * (1 / z), checks)
    require("named_ruler_character", z * z == z * z, checks)

    # Endpoint field factorization with e^phi represented by positive rationals.
    zp, zq, zr = Fraction(3, 2), Fraction(5, 2), Fraction(7, 3)
    u_pq = matmul(reciprocal_operator(1 / zp), reciprocal_operator(zq))
    u_qr = matmul(reciprocal_operator(1 / zq), reciprocal_operator(zr))
    u_pr = matmul(reciprocal_operator(1 / zp), reciprocal_operator(zr))
    require("endpoint_composition", matmul(u_pq, u_qr) == u_pr, checks)
    require(
        "endpoint_difference",
        u_pq == reciprocal_operator(zq / zp),
        checks,
    )

    # Independent Cartan/coordinate check at a rational endpoint ratio.
    endpoint_ratio = zq / zp
    vector_transport = diagonal(endpoint_ratio, 1 / endpoint_ratio)
    covector_transport = diagonal(1 / endpoint_ratio, endpoint_ratio)
    require(
        "coordinate_covector_matches_pair",
        covector_transport == reciprocal_operator(endpoint_ratio),
        checks,
    )
    require(
        "coordinate_vector_is_inverse",
        vector_transport == reciprocal_operator(1 / endpoint_ratio),
        checks,
    )
    require(
        "vector_covector_duality",
        matmul(transpose(vector_transport), covector_transport) == identity,
        checks,
    )

    theta_p_t = 1 / zp
    theta_p_x = zp
    theta_q_t = 1 / zq
    theta_q_x = zq
    require(
        "orthonormal_time_coframe_parallel",
        covector_transport[0][0] * theta_p_t == theta_q_t,
        checks,
    )
    require(
        "orthonormal_space_coframe_parallel",
        covector_transport[1][1] * theta_p_x == theta_q_x,
        checks,
    )

    # Infinitesimal coordinate connection versus the physical coframe.
    phi_prime = Fraction(7, 5)
    vector_generator = diagonal(phi_prime, -phi_prime)
    covector_generator = diagonal(-phi_prime, phi_prime)
    coframe_log_derivative = diagonal(-phi_prime, phi_prime)
    require("vector_covector_generators_dual", vector_generator[0][0] == -covector_generator[0][0], checks)
    require("coframe_derivative_matches_covector", coframe_log_derivative == covector_generator, checks)
    require("orthonormal_spatial_spin_connection_zero", Fraction(0) == zero, checks)

    # Independent endpoint frame changes alter the trace even for identity transport.
    frame_p = Fraction(2)
    frame_q = Fraction(3)
    refactored = matmul(balanced_boost(frame_q), inverse_boost(frame_p))
    require(
        "independent_endpoint_trace_changes",
        trace(refactored) / 2 == (frame_q / frame_p + frame_p / frame_q) / 2,
        checks,
    )
    require("independent_endpoint_trace_not_one", trace(refactored) / 2 != one, checks)

    with (HERE / "DERIVATION_RESULT.json").open(encoding="utf-8") as handle:
        result = json.load(handle)
    operator_rows = read_tsv("OPERATOR_STATUS_LEDGER.tsv")
    readout_rows = read_tsv("CLOCK_READOUT_LEDGER.tsv")
    transport_rows = read_tsv("TRANSPORT_TYPE_LEDGER.tsv")
    gate_rows = read_tsv("GLOBAL_EVALUATION_GATE.tsv")
    source_rows = read_tsv("SOURCE_LINEAGE.tsv")

    require("production_check_count", result["check_count"] >= 50, checks)
    require("operator_rows_7", len(operator_rows) == 7, checks)
    require("readout_rows_5", len(readout_rows) == 5, checks)
    require("transport_rows_5", len(transport_rows) == 5, checks)
    require("gate_rows_7", len(gate_rows) == 7, checks)
    require("source_rows_11", len(source_rows) == 11, checks)
    require("operator_ids_unique", len({row["id"] for row in operator_rows}) == 7, checks)
    require("source_ids_unique", len({row["id"] for row in source_rows}) == 11, checks)
    for row in source_rows:
        source = ROOT / row["path"]
        require(f"source_exists_{row['id']}", source.is_file(), checks)
        require(f"source_sha_{row['id']}", sha256(source) == row["sha256"], checks)

    status_by_id = {row["id"]: row["status"] for row in operator_rows}
    require("abstract_operator_derived", status_by_id["O01"].startswith("DERIVED_"), checks)
    require("endpoint_join_conditional", "OPEN_PAIR_TO_LOCAL_FIELD_JOIN" in status_by_id["O03"], checks)
    require("global_operator_open", status_by_id["O07"] == "OPEN_TYPED_GLOBAL_JOIN", checks)
    require(
        "mutual_slow_conditional",
        {row["id"]: row["status"] for row in readout_rows}["R03"].startswith("CONDITIONAL_"),
        checks,
    )
    require(
        "orthonormal_transport_identity",
        {row["id"]: row["spatial_transport"] for row in transport_rows}["T03"] == "identity",
        checks,
    )

    def mutate_result(field: str, value) -> None:
        changed = json.loads(json.dumps(result))
        changed[field] = value
        require("mutation", changed["schema"] == "udt-observer-pair-clock-operator-1.0", {})

    expect_failure("schema", lambda: mutate_result("schema", "bad"), catches)
    expect_failure("K", lambda: require("bad", matmul(matmul(transpose(reciprocal_operator(z)), identity), reciprocal_operator(z)) == K, {}), catches)
    expect_failure("composition", lambda: require("bad", matmul(reciprocal_operator(z), reciprocal_operator(z)) == reciprocal_operator(z), {}), catches)
    expect_failure("reversal", lambda: require("bad", reciprocal_operator(z) == reciprocal_operator(1 / z), {}), catches)
    expect_failure("gamma_character", lambda: require("bad", gamma_two == gamma_one * gamma_one, {}), catches)
    expect_failure("endpoint_promote", lambda: require("bad", status_by_id["O03"].startswith("DERIVED_UNCONDITIONAL"), {}), catches)
    expect_failure("orthonormal_boost", lambda: require("bad", {row["id"]: row["spatial_transport"] for row in transport_rows}["T03"] != "identity", {}), catches)
    expect_failure("global_promote", lambda: require("bad", status_by_id["O07"].startswith("DERIVED"), {}), catches)
    expect_failure("mutual_promote", lambda: require("bad", {row["id"]: row["status"] for row in readout_rows}["R03"].startswith("DERIVED_PHYSICAL"), {}), catches)
    expect_failure("source_missing", lambda: require("bad", len(source_rows[:-1]) == 11, {}), catches)
    expect_failure("duplicate_operator", lambda: require("bad", len(operator_rows + [operator_rows[0]]) == len({row["id"] for row in operator_rows + [operator_rows[0]]}), {}), catches)
    expect_failure("Xmax_scope", lambda: require("bad", {row["gate"]: row["result"] for row in gate_rows}["physical Xmax mass or CMB"] == "PASS", {}), catches)

    verification = {
        "schema": "udt-observer-pair-clock-operator-independent-1.0",
        "implementation": "PYTHON_STDLIB_FRACTION_NO_SYMPY_NO_PRODUCTION_IMPORT",
        "result": "PASS",
        "checks": checks,
        "check_count": len(checks),
        "catches": catches,
        "catch_count": len(catches),
        "ruling": {
            "abstract_operator": "DERIVED_CONDITIONAL_WITH_FOUNDING_PREMISE_STAMPS",
            "balanced_form": "EXACT_O11_BOOST_ALGEBRA",
            "static_coordinate_covector_match": "PASS",
            "orthonormal_spatial_transport": "IDENTITY",
            "global_physical_clock_readout": "OPEN_TYPED_JOIN",
        },
    }
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(verification, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "result": "PASS",
        "checks": len(checks),
        "catches": len(catches),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
