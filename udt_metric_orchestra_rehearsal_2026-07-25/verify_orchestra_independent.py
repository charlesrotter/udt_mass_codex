#!/usr/bin/env python3
"""Independent high-precision finite-difference reconstruction of the atlas."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from fractions import Fraction
from pathlib import Path

import mpmath as mp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FIELDS = ("phi", "sigma", "alpha", "k", "S10", "S11", "S20", "S21")
RATES = tuple(f"d{direction}_{field}" for direction in ("0", "1") for field in FIELDS)
RICCI_COMPONENTS = ((0, 0), (0, 1), (0, 2), (0, 3), (1, 1),
                    (1, 2), (1, 3), (2, 2), (2, 3), (3, 3))
RICCI_NAMES = tuple(f"R{mu}{nu}" for mu, nu in RICCI_COMPONENTS)


def require(name: str, condition: bool, checks: dict[str, str]) -> None:
    if not condition:
        raise AssertionError(name)
    checks[name] = "PASS"


def coframe(field: list[mp.mpf]) -> mp.matrix:
    phi, sigma, alpha, k, s10, s11, s20, s21 = field
    r = mp.exp(sigma / 2 - alpha)
    q = mp.exp(sigma / 2 + alpha)
    return mp.matrix([
        [mp.exp(-phi), 0, 0, 0],
        [0, mp.exp(phi), 0, 0],
        [r * (s10 + k * s20), r * (s11 + k * s21), r, k * r],
        [q * s20, q * s21, 0, q],
    ])


ETA = mp.matrix([[-1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])


def metric_from_field(field: list[mp.mpf]) -> mp.matrix:
    E = coframe(field)
    return E.T * ETA * E


def metric_for_rates(rates: list[mp.mpf], x0: mp.mpf, x1: mp.mpf) -> mp.matrix:
    field = [rates[i] * x0 + rates[8 + i] * x1 for i in range(8)]
    return metric_from_field(field)


def metric_for_second(index: int, kind: str, x0: mp.mpf, x1: mp.mpf) -> mp.matrix:
    field = [mp.mpf("0") for _ in range(8)]
    if kind == "d00":
        field[index] = x0**2 / 2
    elif kind == "d01":
        field[index] = x0 * x1
    else:
        field[index] = x1**2 / 2
    return metric_from_field(field)


def combine(terms: list[tuple[mp.mpf, mp.matrix]]) -> mp.matrix:
    result = mp.zeros(4)
    for coefficient, matrix in terms:
        result += coefficient * matrix
    return result


def numerical_metric_jets(function, h: mp.mpf):
    zero = mp.mpf("0")
    cache: dict[tuple[int, int], mp.matrix] = {}

    def value(i: int, j: int) -> mp.matrix:
        key = (i, j)
        if key not in cache:
            cache[key] = function(i * h, j * h)
        return cache[key]

    g0 = value(0, 0)
    dg = [mp.zeros(4) for _ in range(4)]
    dg[0] = combine([
        (1, value(-2, 0)), (-8, value(-1, 0)),
        (8, value(1, 0)), (-1, value(2, 0)),
    ]) / (12 * h)
    dg[1] = combine([
        (1, value(0, -2)), (-8, value(0, -1)),
        (8, value(0, 1)), (-1, value(0, 2)),
    ]) / (12 * h)

    ddg = [[mp.zeros(4) for _ in range(4)] for _ in range(4)]
    ddg[0][0] = combine([
        (-1, value(2, 0)), (16, value(1, 0)), (-30, g0),
        (16, value(-1, 0)), (-1, value(-2, 0)),
    ]) / (12 * h**2)
    ddg[1][1] = combine([
        (-1, value(0, 2)), (16, value(0, 1)), (-30, g0),
        (16, value(0, -1)), (-1, value(0, -2)),
    ]) / (12 * h**2)
    mixed = combine([
        (1, value(1, 1)), (-1, value(1, -1)),
        (-1, value(-1, 1)), (1, value(-1, -1)),
    ]) / (4 * h**2)
    ddg[0][1] = mixed
    ddg[1][0] = mixed
    return g0, dg, ddg


def curvature_from_jets(g0: mp.matrix, dg: list[mp.matrix], ddg: list[list[mp.matrix]]):
    inv = g0**-1
    dinv = [-inv * item * inv for item in dg]
    gamma = [[[
        sum(inv[rho, s] * (dg[nu][s, mu] + dg[mu][s, nu] - dg[s][mu, nu])
            for s in range(4)) / 2
        for nu in range(4)] for mu in range(4)] for rho in range(4)]
    dgamma = [[[[(
        sum(
            dinv[lam][rho, s] * (dg[nu][s, mu] + dg[mu][s, nu] - dg[s][mu, nu])
            + inv[rho, s] * (
                ddg[lam][nu][s, mu] + ddg[lam][mu][s, nu] - ddg[lam][s][mu, nu]
            ) for s in range(4)
        ) / 2
    ) for nu in range(4)] for mu in range(4)] for rho in range(4)] for lam in range(4)]
    ricci = mp.zeros(4)
    for mu in range(4):
        for nu in range(4):
            for rho in range(4):
                ricci[mu, nu] += dgamma[rho][rho][mu][nu] - dgamma[nu][rho][mu][rho]
                for lam in range(4):
                    ricci[mu, nu] += gamma[rho][rho][lam] * gamma[lam][mu][nu]
                    ricci[mu, nu] -= gamma[rho][nu][lam] * gamma[lam][mu][rho]
    scalar = sum(inv[mu, nu] * ricci[mu, nu]
                 for mu in range(4) for nu in range(4))
    return ricci, scalar


def rate_curvature(rates: list[mp.mpf], h: mp.mpf):
    return curvature_from_jets(*numerical_metric_jets(
        lambda x0, x1: metric_for_rates(rates, x0, x1), h
    ))


def reconstruct_hessians(h: mp.mpf):
    size = 16
    zero = mp.mpf("0")
    one = mp.mpf("1")
    basis_values = []
    for i in range(size):
        vector = [zero for _ in range(size)]
        vector[i] = one
        basis_values.append(rate_curvature(vector, h))
    scalar_hessian = [[zero for _ in range(size)] for _ in range(size)]
    ricci_hessians = [[[zero for _ in range(size)] for _ in range(size)]
                      for _ in RICCI_COMPONENTS]
    for i in range(size):
        basis_ricci, basis_scalar = basis_values[i]
        scalar_hessian[i][i] = 2 * basis_scalar
        for component, (mu, nu) in enumerate(RICCI_COMPONENTS):
            ricci_hessians[component][i][i] = 2 * basis_ricci[mu, nu]
        for j in range(i + 1, size):
            vector = [zero for _ in range(size)]
            vector[i] = one
            vector[j] = one
            cross_ricci, cross_scalar = rate_curvature(vector, h)
            ricci_i, scalar_i = basis_values[i]
            ricci_j, scalar_j = basis_values[j]
            scalar_cross = cross_scalar - scalar_i - scalar_j
            scalar_hessian[i][j] = scalar_hessian[j][i] = scalar_cross
            for component, (mu, nu) in enumerate(RICCI_COMPONENTS):
                ricci_cross = cross_ricci[mu, nu] - ricci_i[mu, nu] - ricci_j[mu, nu]
                ricci_hessians[component][i][j] = ricci_cross
                ricci_hessians[component][j][i] = ricci_cross
    return ricci_hessians, scalar_hessian


def parse_fraction(value: str) -> mp.mpf:
    fraction = Fraction(value)
    return mp.mpf(fraction.numerator) / fraction.denominator


def maximum_matrix_error(left, right) -> mp.mpf:
    return max(abs(left[i][j] - right[i][j])
               for i in range(len(left)) for j in range(len(left[i])))


def maximum_tensor_error(left, right) -> mp.mpf:
    return max(maximum_matrix_error(left[k], right[k]) for k in range(len(left)))


def main() -> None:
    mp.mp.dps = 70
    checks: dict[str, str] = {}
    with (HERE / "CURVATURE_RATE_HESSIAN.tsv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    expected_hessian = [[parse_fraction(row[name]) for name in RATES] for row in rows]
    require("I01_hessian_shape", len(rows) == 16 and all(row["rate"] == RATES[i]
                                                         for i, row in enumerate(rows)), checks)

    coarse_h = mp.mpf("0.002")
    fine_h = coarse_h / 2
    coarse_ricci, coarse = reconstruct_hessians(coarse_h)
    fine_ricci, fine = reconstruct_hessians(fine_h)
    coarse_error = maximum_matrix_error(coarse, expected_hessian)
    fine_error = maximum_matrix_error(fine, expected_hessian)
    require("I02_numeric_hessian_coarse", coarse_error < mp.mpf("2e-4"), checks)
    require("I03_numeric_hessian_refined", fine_error < mp.mpf("5e-5"), checks)
    require("I04_numeric_hessian_refines", fine_error < coarse_error / 3, checks)

    expected_ricci = [[[mp.mpf("0") for _ in RATES] for _ in RATES]
                      for _ in RICCI_COMPONENTS]
    with (HERE / "RICCI_RATE_COUPLINGS.tsv").open(newline="", encoding="utf-8") as handle:
        ricci_rows = list(csv.DictReader(handle, delimiter="\t"))
    for row in ricci_rows:
        i = RATES.index(row["left_rate"])
        j = RATES.index(row["right_rate"])
        for component, name in enumerate(RICCI_NAMES):
            value = parse_fraction(row[name])
            expected_ricci[component][i][j] = value
            expected_ricci[component][j][i] = value
    ricci_coarse_error = maximum_tensor_error(coarse_ricci, expected_ricci)
    ricci_fine_error = maximum_tensor_error(fine_ricci, expected_ricci)
    require("I05_ricci_hessian_59_nonzero_pairs", len(ricci_rows) == 59, checks)
    require("I06_numeric_ricci_hessians_coarse", ricci_coarse_error < mp.mpf("2e-4"), checks)
    require("I07_numeric_ricci_hessians_refined", ricci_fine_error < mp.mpf("5e-5"), checks)
    require("I08_numeric_ricci_hessians_refine", ricci_fine_error < ricci_coarse_error / 3, checks)

    with (HERE / "CURVATURE_SECOND_JET_RESPONSE.tsv").open(newline="", encoding="utf-8") as handle:
        second_rows = list(csv.DictReader(handle, delimiter="\t"))
    second_coarse_errors = []
    second_fine_errors = []
    ricci_second_coarse_errors = []
    ricci_second_fine_errors = []
    with (HERE / "RICCI_SECOND_JET_RESPONSE.tsv").open(newline="", encoding="utf-8") as handle:
        ricci_second_rows = list(csv.DictReader(handle, delimiter="\t"))
    ricci_second_by_key = {
        (row["instrument"], row["second_jet"]): row for row in ricci_second_rows
    }
    for row in second_rows:
        index = FIELDS.index(row["instrument"])
        expected = parse_fraction(row["curvature_response"])
        ricci_row = ricci_second_by_key[(row["instrument"], row["second_jet"])]
        for h, errors, ricci_errors in (
            (coarse_h, second_coarse_errors, ricci_second_coarse_errors),
            (fine_h, second_fine_errors, ricci_second_fine_errors),
        ):
            observed_ricci, observed = curvature_from_jets(*numerical_metric_jets(
                lambda x0, x1, i=index, kind=row["second_jet"]: metric_for_second(i, kind, x0, x1), h
            ))
            errors.append(abs(observed - expected))
            for name, (mu, nu) in zip(RICCI_NAMES, RICCI_COMPONENTS):
                ricci_errors.append(abs(observed_ricci[mu, nu] - parse_fraction(ricci_row[name])))
    second_coarse = max(second_coarse_errors)
    second_fine = max(second_fine_errors)
    ricci_second_coarse = max(ricci_second_coarse_errors)
    ricci_second_fine = max(ricci_second_fine_errors)
    require("I09_all_24_second_jets", len(second_rows) == 24 and len(ricci_second_rows) == 24, checks)
    require("I10_numeric_second_jets_coarse", second_coarse < mp.mpf("2e-4"), checks)
    require("I11_numeric_second_jets_refined", second_fine < mp.mpf("5e-5"), checks)
    require("I12_numeric_second_jets_refine", second_fine < second_coarse / 3, checks)
    require("I13_numeric_ricci_second_jets_coarse", ricci_second_coarse < mp.mpf("2e-4"), checks)
    require("I14_numeric_ricci_second_jets_refined", ricci_second_fine < mp.mpf("5e-5"), checks)
    require("I15_numeric_ricci_second_jets_refine", ricci_second_fine < ricci_second_coarse / 3, checks)

    sample = [mp.mpf(value) for value in ("0.2", "-0.3", "0.4", "0.1", "0.2", "-0.1", "0.3", "0.25")]
    E = coframe(sample)
    g = E.T * ETA * E
    require("I16_metric_determinant", abs(mp.det(E) - mp.exp(sample[1])) < mp.mpf("1e-60")
            and abs(mp.det(g) + mp.exp(2 * sample[1])) < mp.mpf("1e-60"), checks)
    pure_gauge = [mp.mpf("0") for _ in range(16)]
    pure_gauge[5] = 1  # d0 S11
    pure_gauge[12] = 1  # d1 S10
    pure_gauge_ricci, pure_gauge_scalar = rate_curvature(pure_gauge, fine_h)
    require("I17_pure_gauge_connection_zero_curvature",
            abs(pure_gauge_scalar) < mp.mpf("5e-5")
            and max(abs(pure_gauge_ricci[i, j]) for i in range(4) for j in range(4)) < mp.mpf("5e-5"), checks)
    field_strength = [mp.mpf("0") for _ in range(16)]
    field_strength[5] = 1
    _, field_strength_scalar = rate_curvature(field_strength, fine_h)
    require("I18_connection_field_strength_half_square",
            abs(field_strength_scalar - mp.mpf("0.5")) < mp.mpf("5e-5"), checks)

    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        sources = list(csv.DictReader(handle, delimiter="\t"))
    source_ok = len(sources) == 10
    for row in sources:
        path = ROOT / row["path"]
        blob = subprocess.run(["git", "rev-parse", f"HEAD:{row['path']}"], cwd=ROOT,
                              check=True, text=True, capture_output=True).stdout.strip()
        source_ok &= hashlib.sha256(path.read_bytes()).hexdigest() == row["sha256"]
        source_ok &= blob == row["git_blob"]
    require("I19_source_identities", source_ok, checks)

    algebra = json.loads((HERE / "ALGEBRA_RESULT.json").read_text(encoding="utf-8"))
    require("I20_production_integrity", algebra["sympy_version"] == "1.14.0"
            and algebra["check_count"] == 22
            and set(algebra["checks"].values()) == {"PASS"}, checks)
    result = {
        "schema": "udt-metric-orchestra-independent-1.0",
        "method": "mpmath_70_digit_direct_coframe_finite_difference_metric_jets_no_production_import",
        "mpmath_version": mp.__version__,
        "check_count": len(checks), "checks": checks,
        "curvature_hessian_reconstruction": {
            "entries": 256, "coarse_h": str(coarse_h), "fine_h": str(fine_h),
            "coarse_max_abs_error": mp.nstr(coarse_error, 16),
            "fine_max_abs_error": mp.nstr(fine_error, 16),
        },
        "ricci_hessian_reconstruction": {
            "components": 10, "entries": 2560, "nonzero_upper_triangle_pairs": 59,
            "coarse_max_abs_error": mp.nstr(ricci_coarse_error, 16),
            "fine_max_abs_error": mp.nstr(ricci_fine_error, 16),
        },
        "second_jet_reconstruction": {
            "controls": 24,
            "coarse_max_abs_error": mp.nstr(second_coarse, 16),
            "fine_max_abs_error": mp.nstr(second_fine, 16),
        },
        "ricci_second_jet_reconstruction": {
            "components": 10, "entries": 240,
            "coarse_max_abs_error": mp.nstr(ricci_second_coarse, 16),
            "fine_max_abs_error": mp.nstr(ricci_second_fine, 16),
        },
        "scientific_checks": 18,
        "artifact_integrity_checks": 2,
        "result": "PASS",
    }
    (HERE / "INDEPENDENT_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
