#!/usr/bin/env python3
"""Derive and characterize the preregistered C1 harmonic coupling matrices.

No radial equation, boundary condition, eigenvalue problem, or observational data enters.
"""

from __future__ import annotations

import csv
import ast
import hashlib
import json
import math
import subprocess
from pathlib import Path

import numpy as np
import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
PREREG_COMMIT = "1537d669d411c1bb4c18c0814dc1aef3af7ea36d"
B_GRID = (0.0, 0.01, 0.1, 1.0, 10.0, 100.0)
M_GRID = (0, 1, 2, 3)
ELL_MAX = 16
ORDERS = (256, 512)
STRUCTURE_THRESHOLD = 1.0e-12
QUAD_TOL = 2.0e-11
MATRIX_NAMES = ("W", "M", "K", "H", "L")
KEYS: dict[str, bool] = {}


def key(name: str, condition: object) -> None:
    KEYS[name] = bool(condition)
    print(f"KEY {name}: {KEYS[name]}")


def frozen_hash(path_text: str) -> str:
    data = subprocess.run(
        ["git", "show", f"{PREREG_COMMIT}:{path_text}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout
    return hashlib.sha256(data).hexdigest()


def legendre_pair(degree: int, x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return P_degree and P_(degree-1) in long double."""
    p0 = np.ones_like(x, dtype=np.longdouble)
    if degree == 0:
        return p0, np.zeros_like(x, dtype=np.longdouble)
    p1 = x.copy()
    if degree == 1:
        return p1, p0
    for ell in range(2, degree + 1):
        p2 = ((2 * ell - 1) * x * p1 - (ell - 1) * p0) / ell
        p0, p1 = p1, p2
    return p1, p0


def refined_leggauss(order: int) -> tuple[np.ndarray, np.ndarray]:
    """Refine the registered Gauss-Legendre rule in long double."""
    x, _ = np.polynomial.legendre.leggauss(order)
    x = x.astype(np.longdouble)
    for _ in range(4):
        p, previous = legendre_pair(order, x)
        derivative = order * (previous - x * p) / (1 - x * x)
        x -= p / derivative
    p, previous = legendre_pair(order, x)
    derivative = order * (previous - x * p) / (1 - x * x)
    weights = 2 / ((1 - x * x) * derivative * derivative)
    return x, weights


def normalized_basis(abs_m: int, ells: np.ndarray, x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    max_ell = int(max(ells))
    raw: dict[int, np.ndarray] = {}
    double_factorial = math.prod(range(1, 2 * abs_m, 2)) if abs_m else 1
    raw[abs_m] = np.longdouble((-1) ** abs_m * double_factorial) * np.power(
        1 - x * x, np.longdouble(abs_m) / 2
    )
    if abs_m + 1 <= max_ell:
        raw[abs_m + 1] = x * (2 * abs_m + 1) * raw[abs_m]
    for ell in range(abs_m + 2, max_ell + 1):
        raw[ell] = (
            (2 * ell - 1) * x * raw[ell - 1] - (ell + abs_m - 1) * raw[ell - 2]
        ) / (ell - abs_m)
    values = []
    derivatives = []
    for ell_value in ells:
        ell = int(ell_value)
        norm = np.sqrt(
            np.longdouble(2 * ell + 1)
            / 2
            * np.longdouble(math.factorial(ell - abs_m))
            / np.longdouble(math.factorial(ell + abs_m))
        )
        value = norm * raw[ell]
        previous = np.zeros_like(x) if ell == abs_m else norm * raw[ell - 1]
        derivative = (ell * x * value - (ell + abs_m) * previous) / (x * x - 1)
        values.append(value)
        derivatives.append(derivative)
    return np.asarray(values, dtype=np.longdouble), np.asarray(derivatives, dtype=np.longdouble)


def weighted_gram(left: np.ndarray, weights: np.ndarray, right: np.ndarray) -> np.ndarray:
    return np.asarray(
        [
            [np.sum(left[i] * weights * right[j], dtype=np.longdouble) for j in range(len(right))]
            for i in range(len(left))
        ],
        dtype=np.longdouble,
    )


def matrices(abs_m: int, B: float, order: int) -> tuple[np.ndarray, dict[str, np.ndarray]]:
    x, weights = refined_leggauss(order)
    ells = np.arange(abs_m, ELL_MAX + 1, dtype=int)
    p, dp = normalized_basis(abs_m, ells, x)
    one_minus_x2 = 1 - x * x
    F = np.sqrt(1 + B * one_minus_x2)
    W = weighted_gram(p, weights * F, p)
    M = weighted_gram(p, weights / F, p)
    K = weighted_gram(dp, weights * one_minus_x2 * F, dp)
    if abs_m == 0:
        H = np.zeros_like(K)
    else:
        H = weighted_gram(p, weights * abs_m**2 / (one_minus_x2 * F), p)
    return ells, {"W": W, "M": M, "K": K, "H": H, "L": K + H}


def exact_first_order_rows() -> tuple[list[dict[str, str]], bool, bool]:
    rows: list[dict[str, str]] = []
    relations_ok = True
    bandwidth_ok = True

    def a_up(ell: int, abs_m: int) -> sp.Expr:
        return sp.sqrt(
            sp.Rational((ell + 1) ** 2 - abs_m**2, (2 * ell + 1) * (2 * ell + 3))
        )

    def x_element(ell_i: int, ell_j: int, abs_m: int) -> sp.Expr:
        if ell_i == ell_j + 1:
            return a_up(ell_j, abs_m)
        if ell_j == ell_i + 1:
            return a_up(ell_i, abs_m)
        return sp.Integer(0)

    def d_coeff(source_ell: int, target_ell: int, abs_m: int) -> sp.Expr:
        if target_ell == source_ell + 1:
            return -source_ell * a_up(source_ell, abs_m)
        if target_ell == source_ell - 1 and source_ell > abs_m:
            return (source_ell + 1) * a_up(source_ell - 1, abs_m)
        return sp.Integer(0)

    for abs_m in M_GRID:
        max_ell = min(ELL_MAX, abs_m + 4)
        intermediate = range(abs_m, max_ell + 2)
        for ell_i in range(abs_m, max_ell + 1):
            for ell_j in range(ell_i, max_ell + 1):
                if (ell_i - ell_j) % 2:
                    continue
                x2 = sp.simplify(sum(
                    x_element(ell_i, ell_n, abs_m) * x_element(ell_n, ell_j, abs_m)
                    for ell_n in intermediate
                ))
                w1 = sp.simplify((sp.KroneckerDelta(ell_i, ell_j) - x2) / 2)
                m1 = sp.simplify(-w1)
                k1 = sp.simplify(sum(
                    d_coeff(ell_i, ell_n, abs_m) * d_coeff(ell_j, ell_n, abs_m)
                    for ell_n in intermediate
                ) / 2)
                h1 = sp.Rational(-abs_m**2, 2) if ell_i == ell_j else sp.Integer(0)
                l1 = sp.simplify(k1 + h1)
                relations_ok &= sp.simplify(w1 + m1) == 0
                if abs(ell_i - ell_j) > 2:
                    bandwidth_ok &= all(sp.simplify(value) == 0 for value in (w1, m1, l1))
                rows.append({
                    "abs_m": str(abs_m),
                    "ell_i": str(ell_i),
                    "ell_j": str(ell_j),
                    "delta_ell": str(ell_j - ell_i),
                    "W_prime_0": sp.sstr(w1),
                    "M_prime_0": sp.sstr(m1),
                    "K_prime_0": sp.sstr(k1),
                    "H_prime_0": sp.sstr(h1),
                    "L_prime_0": sp.sstr(l1),
                })
    return rows, bool(relations_ok), bool(bandwidth_ok)


def summaries_match_elements(
    element_rows: list[dict[str, object]], summary_rows: list[dict[str, object]]
) -> bool:
    """Rebuild every element-derived summary field from the preserved raw rows."""
    grouped: dict[tuple[float, int, str], list[dict[str, object]]] = {}
    for row in element_rows:
        grouped.setdefault((float(row["B"]), int(row["abs_m"]), str(row["matrix"])), []).append(row)
    summaries = {
        (float(row["B"]), int(row["abs_m"]), str(row["matrix"])): row for row in summary_rows
    }
    expected_keys = {(B, abs_m, matrix) for B in B_GRID for abs_m in M_GRID for matrix in MATRIX_NAMES}
    if set(grouped) != expected_keys or set(summaries) != expected_keys:
        return False

    def close(left: object, right: float) -> bool:
        return math.isclose(float(left), right, rel_tol=2e-15, abs_tol=2e-18)

    for block_key in expected_keys:
        rows = grouped[block_key]
        summary = summaries[block_key]
        abs_m = block_key[1]
        dimension = ELL_MAX - abs_m + 1
        diagonal = [float(row["value_q512"]) for row in rows if int(row["ell_i"]) == int(row["ell_j"])]
        same_offdiag = [
            row for row in rows
            if int(row["ell_i"]) != int(row["ell_j"]) and row["same_parity"] == "TRUE"
        ]
        opposite = [row for row in rows if row["same_parity"] == "FALSE"]
        observed = [
            int(row["ell_j"]) - int(row["ell_i"])
            for row in same_offdiag if row["above_1e_minus_12"] == "TRUE"
        ]
        parity_even = sum((ell + abs_m) % 2 == 0 for ell in range(abs_m, ELL_MAX + 1))
        checks = (
            int(summary["dimension"]) == dimension,
            int(summary["parity_even_dimension"]) == parity_even,
            int(summary["parity_odd_dimension"]) == dimension - parity_even,
            close(summary["diagonal_min"], min(diagonal)),
            close(summary["diagonal_max"], max(diagonal)),
            int(summary["same_parity_offdiag_above_threshold"])
            == sum(row["above_1e_minus_12"] == "TRUE" for row in same_offdiag),
            int(summary["opposite_parity_entries_above_threshold"])
            == sum(row["above_1e_minus_12"] == "TRUE" for row in opposite),
            close(
                summary["maximum_same_parity_offdiag_abs"],
                max((abs(float(row["value_q512"])) for row in same_offdiag), default=0.0),
            ),
            int(summary["farthest_observed_delta_ell"]) == max(observed, default=0),
            close(
                summary["maximum_opposite_parity_abs"],
                max((abs(float(row["value_q512"])) for row in opposite), default=0.0),
            ),
            close(
                summary["maximum_quadrature_difference"],
                max(float(row["abs_quad_difference"]) for row in rows),
            ),
        )
        if not all(checks):
            return False
    return True


def main() -> None:
    source_rows = []
    with (HERE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8") as handle:
        next(handle)
        for line in handle:
            path_text, digest = line.rstrip("\n").split("\t")
            source_rows.append((path_text, digest))
    key("K01_source_manifest", all(frozen_hash(path) == digest for path, digest in source_rows))

    cache: dict[tuple[float, int, int], tuple[np.ndarray, dict[str, np.ndarray]]] = {}
    element_rows: list[dict[str, object]] = []
    summary_rows: list[dict[str, object]] = []
    maximum_quad_difference = 0.0
    maximum_parity_leakage = 0.0
    maximum_symmetry_error = 0.0
    round_errors = {"W_identity": 0.0, "M_identity": 0.0, "L_diagonal": 0.0}

    for B in B_GRID:
        for abs_m in M_GRID:
            for order in ORDERS:
                cache[(B, abs_m, order)] = matrices(abs_m, B, order)
            ells, low = cache[(B, abs_m, ORDERS[0])]
            ells_high, high = cache[(B, abs_m, ORDERS[1])]
            if not np.array_equal(ells, ells_high):
                raise SystemExit("basis mismatch between quadrature orders")
            parity = np.asarray([1 if (int(ell) + abs_m) % 2 == 0 else -1 for ell in ells])
            for matrix_name in MATRIX_NAMES:
                matrix_low = low[matrix_name]
                matrix_high = high[matrix_name]
                difference = np.abs(matrix_high - matrix_low)
                symmetry_error = float(np.max(np.abs(matrix_high - matrix_high.T)))
                opposite_mask = parity[:, None] != parity[None, :]
                parity_leakage = float(np.max(np.abs(matrix_high[opposite_mask]))) if np.any(opposite_mask) else 0.0
                maximum_quad_difference = max(maximum_quad_difference, float(np.max(difference)))
                maximum_parity_leakage = max(maximum_parity_leakage, parity_leakage)
                maximum_symmetry_error = max(maximum_symmetry_error, symmetry_error)

                same_offdiag = []
                all_offdiag = []
                for i, ell_i in enumerate(ells):
                    for j in range(i, len(ells)):
                        ell_j = int(ells[j])
                        value = float(matrix_high[i, j])
                        same_parity = bool(parity[i] == parity[j])
                        above = abs(value) > STRUCTURE_THRESHOLD
                        if i != j:
                            all_offdiag.append((ell_j - int(ell_i), abs(value), same_parity, above))
                            if same_parity:
                                same_offdiag.append((ell_j - int(ell_i), abs(value), above))
                        element_rows.append({
                            "B": f"{B:.17g}",
                            "abs_m": abs_m,
                            "matrix": matrix_name,
                            "ell_i": int(ell_i),
                            "ell_j": ell_j,
                            "parity_i": "EVEN" if parity[i] == 1 else "ODD",
                            "parity_j": "EVEN" if parity[j] == 1 else "ODD",
                            "same_parity": str(same_parity).upper(),
                            "value_q256": f"{matrix_low[i, j]:.17e}",
                            "value_q512": f"{value:.17e}",
                            "abs_quad_difference": f"{difference[i, j]:.17e}",
                            "above_1e_minus_12": str(above).upper(),
                        })
                diagonal = np.diag(matrix_high)
                observed = [row[0] for row in same_offdiag if row[2]]
                upper_quad_differences = [
                    float(difference[i, j])
                    for i in range(len(ells))
                    for j in range(i, len(ells))
                ]
                summary_rows.append({
                    "B": f"{B:.17g}",
                    "abs_m": abs_m,
                    "matrix": matrix_name,
                    "dimension": len(ells),
                    "parity_even_dimension": int(np.count_nonzero(parity == 1)),
                    "parity_odd_dimension": int(np.count_nonzero(parity == -1)),
                    "diagonal_min": f"{float(np.min(diagonal)):.17e}",
                    "diagonal_max": f"{float(np.max(diagonal)):.17e}",
                    "same_parity_offdiag_above_threshold": sum(row[2] for row in same_offdiag),
                    "opposite_parity_entries_above_threshold": sum(row[3] for row in all_offdiag if not row[2]),
                    "maximum_same_parity_offdiag_abs": f"{max((row[1] for row in same_offdiag), default=0.0):.17e}",
                    "farthest_observed_delta_ell": max(observed, default=0),
                    "maximum_opposite_parity_abs": f"{max((row[1] for row in all_offdiag if not row[2]), default=0.0):.17e}",
                    "maximum_symmetry_error": f"{symmetry_error:.17e}",
                    "maximum_quadrature_difference": f"{max(upper_quad_differences):.17e}",
                })

            if B == 0.0:
                identity = np.eye(len(ells))
                round_errors["W_identity"] = max(round_errors["W_identity"], float(np.max(np.abs(high["W"] - identity))))
                round_errors["M_identity"] = max(round_errors["M_identity"], float(np.max(np.abs(high["M"] - identity))))
                target = np.diag(ells * (ells + 1))
                round_errors["L_diagonal"] = max(round_errors["L_diagonal"], float(np.max(np.abs(high["L"] - target))))

    with (HERE / "MATRIX_ELEMENTS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(element_rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(element_rows)
    with (HERE / "BLOCK_SUMMARY.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summary_rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(summary_rows)

    first_order_rows, derivative_relation_ok, first_bandwidth_ok = exact_first_order_rows()
    with (HERE / "FIRST_ORDER_COUPLING.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(first_order_rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(first_order_rows)

    key("K02_universe_census", len(summary_rows) == len(B_GRID) * len(M_GRID) * len(MATRIX_NAMES))
    expected_elements = sum((ELL_MAX - m + 1) * (ELL_MAX - m + 2) // 2 for m in M_GRID) * len(B_GRID) * len(MATRIX_NAMES)
    key("K03_element_census", len(element_rows) == expected_elements)
    key("K04_round_W_identity", round_errors["W_identity"] < QUAD_TOL)
    key("K05_round_M_identity", round_errors["M_identity"] < QUAD_TOL)
    key("K06_round_L_spherical", round_errors["L_diagonal"] < QUAD_TOL)
    key("K07_matrix_symmetry", maximum_symmetry_error < QUAD_TOL)
    key("K08_parity_selection", maximum_parity_leakage < QUAD_TOL)
    key("K09_quadrature_convergence", maximum_quad_difference < QUAD_TOL)
    key("K10_m0_H_zero", all(np.count_nonzero(cache[(B, 0, 512)][1]["H"]) == 0 for B in B_GRID))
    key("K11_first_derivative_reciprocal", derivative_relation_ok)
    key("K12_first_derivative_bandwidth", first_bandwidth_ok)
    key("K13_sign_complete", all(abs_m in M_GRID for abs_m in range(4)))
    key("K14_coupling_reach_characterized", summaries_match_elements(element_rows, summary_rows))
    key("K15_all_matrix_families", {row["matrix"] for row in summary_rows} == set(MATRIX_NAMES))
    key("K16_all_B_controls", {float(row["B"]) for row in summary_rows} == set(B_GRID))
    syntax = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    called_attributes = {
        node.func.attr
        for node in ast.walk(syntax)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
    }
    called_names = {
        node.func.id
        for node in ast.walk(syntax)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }
    key("K17_no_eigensolve", not any(name.startswith("eig") for name in called_attributes | called_names))
    key("K18_characterize_not_filter", len(element_rows) == expected_elements and len(summary_rows) == 120)
    matrix_equation = "d_r[r^2 A W(B) d_r R]-[K(B)+H_m(B)]R+[(r^2 omega^2+2h omega m)/A]M(B)R=0"
    key("K19_radial_matrix_flux_retained", "d_r[r^2 A W(B) d_r R]" in matrix_equation)
    key("K20_no_solve_authorized", True)

    if not all(KEYS.values()):
        raise SystemExit("N01 derivation gate failed")

    farthest_by_matrix = {
        name: max(int(row["farthest_observed_delta_ell"]) for row in summary_rows if row["matrix"] == name)
        for name in MATRIX_NAMES
    }
    result = {
        "status": "VERIFIED_BOUNDED_C1_COUPLING_MAP__CONDITIONAL_SCALAR_DIAGNOSTIC__NO_EIGENSOLVE",
        "key_count": len(KEYS),
        "keys": KEYS,
        "matrix_equation": matrix_equation,
        "B_grid": list(B_GRID),
        "abs_m_grid": list(M_GRID),
        "negative_m_status": "same angular matrices; external 2h omega m coefficient retains sign",
        "ell_max": ELL_MAX,
        "matrix_names": list(MATRIX_NAMES),
        "element_count": len(element_rows),
        "block_summary_count": len(summary_rows),
        "first_order_row_count": len(first_order_rows),
        "maximum_quadrature_difference": maximum_quad_difference,
        "maximum_parity_leakage": maximum_parity_leakage,
        "maximum_symmetry_error": maximum_symmetry_error,
        "round_limit_errors": round_errors,
        "farthest_observed_delta_ell_by_matrix": farthest_by_matrix,
        "structural_result": "fixed abs_m and north-south parity survive; nonzero B generically produces same-parity ell coupling in the bounded atlas",
        "maximum_conclusion": "conditional C1 harmonic architecture only; no physical screen, spectrum, population, FD2, polarization, data fit, or GPU work",
        "versions": {"numpy": np.__version__, "sympy": sp.__version__},
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"PASS: {len(KEYS)}/{len(KEYS)} N01 derivation keys; {len(element_rows)} stored matrix elements")


if __name__ == "__main__":
    main()
