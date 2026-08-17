#!/usr/bin/env python3
"""Independent stdlib/Fraction replay of G145 load-bearing finite claims."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def rank(matrix: list[list[F]]) -> int:
    work = [row[:] for row in matrix]
    rows = len(work)
    columns = len(work[0])
    pivot_row = 0
    for column in range(columns):
        pivot = next((i for i in range(pivot_row, rows) if work[i][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [value / scale for value in work[pivot_row]]
        for i in range(rows):
            if i == pivot_row or not work[i][column]:
                continue
            factor = work[i][column]
            work[i] = [left - factor * right for left, right in zip(work[i], work[pivot_row])]
        pivot_row += 1
    return pivot_row


def transpose(matrix: list[list[F]]) -> list[list[F]]:
    return [list(row) for row in zip(*matrix)]


def multiply(left: list[list[F]], right: list[list[F]]) -> list[list[F]]:
    return [
        [sum((left[i][k] * right[k][j] for k in range(len(right))), F(0)) for j in range(len(right[0]))]
        for i in range(len(left))
    ]


def equal(left: list[list[F]], right: list[list[F]]) -> bool:
    return left == right


Jet = dict[tuple[int, int], F]
ZERO: Jet = {}
ONE: Jet = {(0, 0): F(1)}


def jclean(value: Jet) -> Jet:
    return {power: coefficient for power, coefficient in value.items() if coefficient and sum(power) <= 3}


def jadd(left: Jet, right: Jet) -> Jet:
    out = dict(left)
    for power, coefficient in right.items():
        out[power] = out.get(power, F(0)) + coefficient
    return jclean(out)


def jscale(scale: F, value: Jet) -> Jet:
    return jclean({power: scale * coefficient for power, coefficient in value.items()})


def jmul(left: Jet, right: Jet) -> Jet:
    out: Jet = {}
    for (i, j), a in left.items():
        for (k, ell), b in right.items():
            power = (i + k, j + ell)
            if sum(power) <= 3:
                out[power] = out.get(power, F(0)) + a * b
    return jclean(out)


def jpow(value: Jet, exponent: int) -> Jet:
    out = ONE
    for _ in range(exponent):
        out = jmul(out, value)
    return out


def jexp(value: Jet) -> Jet:
    if value.get((0, 0), F(0)):
        raise AssertionError("jet exponential expects zero constant term")
    out = ONE
    factorial = 1
    for exponent in range(1, 4):
        factorial *= exponent
        out = jadd(out, jscale(F(1, factorial), jpow(value, exponent)))
    return out


def jmatmul(left: list[list[Jet]], right: list[list[Jet]]) -> list[list[Jet]]:
    return [
        [
            _jsum(jmul(left[i][k], right[k][j]) for k in range(len(right)))
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def _jsum(values) -> Jet:
    out = ZERO
    for value in values:
        out = jadd(out, value)
    return out


def jtranspose(matrix: list[list[Jet]]) -> list[list[Jet]]:
    return [list(row) for row in zip(*matrix)]


def complete_metric_jet(amplitudes: dict[str, F]) -> list[list[Jet]]:
    t: Jet = {(1, 0): F(1)}
    r: Jet = {(0, 1): F(1)}
    t_plus_r = jadd(t, r)
    t_minus_2r = jadd(t, jscale(F(-2), r))
    t_minus_r = jadd(t, jscale(F(-1), r))
    cubic = lambda amp, value: jscale(amp, jpow(value, 3))

    kappa = cubic(amplitudes.get("kappa", F(0)), t_plus_r)
    shift = cubic(amplitudes.get("shift", F(0)), t_minus_2r)
    base_t = jexp(jadd(kappa, jscale(F(-1), r)))
    base_l = jexp(jadd(kappa, r))
    bmat = [[base_t, jmul(base_t, shift)], [ZERO, base_l]]
    q = [
        [jadd(ONE, cubic(amplitudes.get("q00", F(0)), t)), cubic(amplitudes.get("q01", F(0)), r)],
        [ZERO, jadd(ONE, cubic(amplitudes.get("q11", F(0)), t_plus_r))],
    ]
    s = [
        [cubic(amplitudes.get("s00", F(0)), t), cubic(amplitudes.get("s01", F(0)), r)],
        [cubic(amplitudes.get("s10", F(0)), t_plus_r), cubic(amplitudes.get("s11", F(0)), t_minus_r)],
    ]
    qs = jmatmul(q, s)
    e = [
        [bmat[0][0], bmat[0][1], ZERO, ZERO],
        [bmat[1][0], bmat[1][1], ZERO, ZERO],
        [qs[0][0], qs[0][1], q[0][0], q[0][1]],
        [qs[1][0], qs[1][1], q[1][0], q[1][1]],
    ]
    eta_e = [[jscale(F(-1) if i == 0 else F(1), e[i][j]) for j in range(4)] for i in range(4)]
    return jmatmul(jtranspose(e), eta_e)


def scalar_curvature_at_origin(phi_prime: F, phi_second: F) -> F:
    """Direct pointwise Christoffel/Ricci contraction for the 4D witness, c_E=1."""
    n = 4
    g = [[F(0) for _ in range(n)] for _ in range(n)]
    g_inv = [[F(0) for _ in range(n)] for _ in range(n)]
    for i, value in enumerate((F(-1), F(1), F(1), F(1))):
        g[i][i] = value
        g_inv[i][i] = 1 / value
    dg = [[ [F(0) for _ in range(n)] for _ in range(n)] for _ in range(n)]
    ddg = [[[[F(0) for _ in range(n)] for _ in range(n)] for _ in range(n)] for _ in range(n)]
    dg[1][0][0] = 2 * phi_prime
    dg[1][1][1] = 2 * phi_prime
    ddg[1][1][0][0] = 2 * phi_second - 4 * phi_prime * phi_prime
    ddg[1][1][1][1] = 2 * phi_second + 4 * phi_prime * phi_prime

    d_inv = [[ [F(0) for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for derivative in range(n):
        for i in range(n):
            for j in range(n):
                d_inv[derivative][i][j] = -sum(
                    (g_inv[i][a] * dg[derivative][a][b] * g_inv[b][j]
                     for a in range(n) for b in range(n)), F(0)
                )

    gamma = [[ [F(0) for _ in range(n)] for _ in range(n)] for _ in range(n)]
    d_gamma = [[[[F(0) for _ in range(n)] for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for upper in range(n):
        for left in range(n):
            for right in range(n):
                bracket = [
                    dg[left][k][right] + dg[right][k][left] - dg[k][left][right]
                    for k in range(n)
                ]
                gamma[upper][left][right] = F(1, 2) * sum(
                    (g_inv[upper][k] * bracket[k] for k in range(n)), F(0)
                )
                for derivative in range(n):
                    inverse_term = sum(
                        (d_inv[derivative][upper][k] * bracket[k] for k in range(n)), F(0)
                    )
                    metric_term = sum(
                        (
                            g_inv[upper][k]
                            * (ddg[derivative][left][k][right]
                               + ddg[derivative][right][k][left]
                               - ddg[derivative][k][left][right])
                            for k in range(n)
                        ), F(0)
                    )
                    d_gamma[derivative][upper][left][right] = F(1, 2) * (inverse_term + metric_term)

    ricci = [[F(0) for _ in range(n)] for _ in range(n)]
    for left in range(n):
        for right in range(n):
            value = F(0)
            for k in range(n):
                quadratic = sum(
                    (gamma[k][k][ell] * gamma[ell][left][right]
                     - gamma[k][right][ell] * gamma[ell][left][k]
                     for ell in range(n)), F(0)
                )
                value += d_gamma[k][k][left][right] - d_gamma[right][k][left][k] + quadratic
            ricci[left][right] = value
    return sum((g_inv[i][j] * ricci[i][j] for i in range(n) for j in range(n)), F(0))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true", help="recompute without replacing saved evidence")
    args = parser.parse_args()
    checks: list[str] = []
    basis = (
        (0, 0), (0, 1), (0, 2), (0, 3),
        (1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (3, 3),
    )
    directions = (
        (1, 0, 0), (0, 1, 0), (0, 0, 1),
        (1, 1, 0), (1, 0, 1), (0, 1, 1),
    )
    design: list[list[F]] = []
    e0 = (1, 0, 0, 0)
    for direction in directions:
        ruler = (0, *direction)
        for left, right in ((e0, e0), (e0, ruler), (ruler, ruler)):
            row: list[F] = []
            for i, j in basis:
                value = F(left[i] * right[j])
                if i != j:
                    value += F(left[j] * right[i])
                row.append(value)
            design.append(row)
    if rank(design) != 10:
        raise AssertionError("independent six-plane rank")
    checks.append("independent_six_plane_rank_ten")

    j_ba = [[F(2), F(1)], [F(1), F(1)]]
    j_cb = [[F(1), F(1)], [F(1), F(2)]]
    j_ca = multiply(j_cb, j_ba)
    h_c = [[F(-5), F(1)], [F(1), F(2)]]
    h_b = multiply(multiply(transpose(j_cb), h_c), j_cb)
    h_a = multiply(multiply(transpose(j_ba), h_b), j_ba)
    direct = multiply(multiply(transpose(j_ca), h_c), j_ca)
    if not equal(h_a, direct):
        raise AssertionError("independent overlap descent")
    checks.extend(("independent_overlap_cocycle", "independent_pullback_descent"))

    base_j_ba = [
        [F(1), F(1), F(0), F(0)], [F(0), F(1), F(1), F(0)],
        [F(0), F(0), F(1), F(1)], [F(0), F(0), F(0), F(1)],
    ]
    base_j_cb = [
        [F(1), F(0), F(0), F(1)], [F(0), F(1), F(0), F(0)],
        [F(0), F(1), F(1), F(0)], [F(0), F(0), F(0), F(1)],
    ]
    base_j_ca = multiply(base_j_cb, base_j_ba)
    base_g_c = [
        [F(-7), F(0), F(0), F(0)], [F(0), F(2), F(0), F(0)],
        [F(0), F(0), F(3), F(0)], [F(0), F(0), F(0), F(5)],
    ]
    base_g_b = multiply(multiply(transpose(base_j_cb), base_g_c), base_j_cb)
    base_g_a = multiply(multiply(transpose(base_j_ba), base_g_b), base_j_ba)
    base_direct = multiply(multiply(transpose(base_j_ca), base_g_c), base_j_ca)
    if base_g_a != base_direct:
        raise AssertionError("independent four-dimensional base descent")
    checks.extend(("independent_four_dimensional_base_chart_cocycle",
                   "independent_four_dimensional_base_metric_descent"))

    endpoint_q = {"A": F(9, 4), "B": F(4, 1), "C": F(25, 4)}

    def edge_q(source: str, target: str) -> F:
        return endpoint_q[target] / endpoint_q[source]

    q_ba, q_cb, q_ca = edge_q("A", "B"), edge_q("B", "C"), edge_q("A", "C")
    if q_cb * q_ba != q_ca or edge_q("B", "A") != 1 / q_ba:
        raise AssertionError("independent reciprocal composition")
    checks.extend(("independent_q_composition", "independent_q_reversal"))

    def xi(q_value: F) -> F:
        return (1 - q_value) / (1 + q_value)

    xi_ba, xi_cb, xi_ca = xi(q_ba), xi(q_cb), xi(q_ca)
    mobius = (xi_ba + xi_cb) / (1 + xi_ba * xi_cb)
    if mobius != xi_ca:
        raise AssertionError("independent Mobius position")
    checks.append("independent_signed_position_mobius_composition")

    # Reconstruct the curvature from metric first/second derivatives through Christoffel and Ricci
    # tensors; do not substitute into the production route's claimed closed scalar formula.
    r_minus = scalar_curvature_at_origin(F(1), F(0))
    r_plus = scalar_curvature_at_origin(F(1), F(4))
    if not (r_minus == F(-4) and r_plus == F(4) and r_plus - r_minus == F(8)):
        raise AssertionError("independent marked curvature separation")
    checks.extend(("independent_linear_profile_negative_curvature", "independent_quadratic_profile_positive_curvature"))

    amplitudes = {
        "kappa": F(11, 19), "shift": F(-13, 23),
        "q00": F(1, 7), "q01": F(3, 11), "q11": F(-2, 9),
        "s00": F(2, 5), "s01": F(-3, 7), "s10": F(5, 13), "s11": F(-7, 17),
    }
    baseline_jet = complete_metric_jet({})
    complete_jet = complete_metric_jet(amplitudes)
    for i in range(4):
        for j in range(4):
            difference = jadd(complete_jet[i][j], jscale(F(-1), baseline_jet[i][j]))
            if any(coefficient for power, coefficient in difference.items() if sum(power) <= 2):
                raise AssertionError("active complete coframe alters marked metric two-jet")
    for name, amplitude in amplitudes.items():
        if not amplitude:
            raise AssertionError(f"zero independent amplitude: {name}")
        one_field_jet = complete_metric_jet({name: amplitude})
        differences = [
            jadd(one_field_jet[i][j], jscale(F(-1), baseline_jet[i][j]))
            for i in range(4) for j in range(4)
        ]
        if not any(any(coefficient for power, coefficient in delta.items() if sum(power) == 3)
                   for delta in differences):
            raise AssertionError(f"independent metric is insensitive to live field: {name}")
    checks.append("independent_active_orchestra_preserves_marked_two_jet")

    # Dimensions are ordered (length, mass, time). Solve mass/time first.
    # c_E^alpha G^beta has mass exponent -beta and time exponent -alpha-2beta.
    beta_power = F(0)
    alpha_power = -2 * beta_power
    resulting_length_power = alpha_power + 3 * beta_power
    if resulting_length_power == 1:
        raise AssertionError("independent dimensional length unexpectedly exists")
    checks.append("independent_cE_G_no_length_monomial")

    source_count = 0
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            digest = hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest()
            if digest != row["sha256"]:
                raise AssertionError(f"source hash mismatch: {row['path']}")
            source_count += 1
            checks.append(f"independent_source_hash_{Path(row['path']).parent.name}")

    result = {
        "status": "PASS",
        "checks_passed": len(checks),
        "checks_total": len(checks),
        "checks": checks,
        "source_count": source_count,
        "witness_curvatures": {"linear": str(r_minus), "quadratic": str(r_plus)},
        "curvature_method": "direct_fraction_christoffel_ricci_contraction",
        "independently_live_complete_coframe_fields": len(amplitudes),
    }
    if not args.no_write:
        (HERE / "INDEPENDENT_VERIFICATION.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
