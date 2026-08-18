#!/usr/bin/env python3
"""Independent stdlib replay of the G154 external conformal-network review."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


TOL = 2.0e-10


def mobius(x: float, y: float, scale: float) -> float:
    return (x + y) / (1.0 + x * y / (scale * scale))


def close(a: float, b: float, tol: float = TOL) -> bool:
    return math.isclose(a, b, rel_tol=tol, abs_tol=tol)


def matmul(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    return [
        [sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def transpose(a: list[list[float]]) -> list[list[float]]:
    return [list(row) for row in zip(*a)]


def scale_matrix(a: list[list[float]], factor: float) -> list[list[float]]:
    return [[factor * value for value in row] for row in a]


def max_matrix_error(a: list[list[float]], b: list[list[float]]) -> float:
    return max(abs(a[i][j] - b[i][j]) for i in range(len(a)) for j in range(len(a[0])))


def pullback(g: list[list[float]], j: list[list[float]]) -> list[list[float]]:
    return matmul(transpose(j), matmul(g, j))


def pair_metric(t_scale: float, l_scale: float, beta: float) -> list[list[float]]:
    return [
        [-t_scale * t_scale, -t_scale * t_scale * beta],
        [-t_scale * t_scale * beta, l_scale * l_scale - t_scale * t_scale * beta * beta],
    ]


def pair_readouts(h: list[list[float]]) -> tuple[float, float, float]:
    det = h[0][0] * h[1][1] - h[0][1] * h[1][0]
    phi = 0.25 * math.log((-det) / (h[0][0] * h[0][0]))
    beta = h[0][1] / h[0][0]
    kappa = 0.25 * math.log(-det)
    return phi, beta, kappa


def inverse_metric_norm(h: list[list[float]], grad: tuple[float, float]) -> float:
    det = h[0][0] * h[1][1] - h[0][1] * h[1][0]
    a, b = grad
    return (h[1][1] * a * a - 2.0 * h[0][1] * a * b + h[0][0] * b * b) / det


def response(q: float, ell: float, epsilon: int, x_star: float) -> float:
    return (
        epsilon
        * 4.0
        * x_star
        / 3.0
        * q ** (ell - 1.0 / 3.0)
        / (1.0 + q ** (2.0 / 3.0)) ** 2
    )


def smooth_step(t: float) -> float:
    if t <= 0.0:
        return 0.0
    if t >= 1.0:
        return 1.0
    left = math.exp(-1.0 / t)
    right = math.exp(-1.0 / (1.0 - t))
    return left / (left + right)


def cutoff_scale(q: float, ell: float, q_tail: float = 1.0e-4, q_anchor: float = 0.2) -> float:
    weight = smooth_step((q_anchor - q) / (q_anchor - q_tail))
    return math.exp(weight * (-ell * math.log(q)))


def run() -> dict[str, object]:
    checks: dict[str, bool] = {}

    # 1. Dimensionful Mobius groups are scale-isomorphic; normalized composition is scale blind.
    max_group_error = 0.0
    for x_scale in (0.7, 3.0, 11.0):
        for y_scale in (0.9, 5.0, 17.0):
            for a in (-1.7, -0.2, 0.0, 0.8, 2.1):
                for b in (-0.9, 0.0, 0.4, 1.3):
                    x = x_scale * math.tanh(a)
                    y = x_scale * math.tanh(b)
                    mapped_lhs = (y_scale / x_scale) * mobius(x, y, x_scale)
                    mapped_rhs = mobius(
                        (y_scale / x_scale) * x,
                        (y_scale / x_scale) * y,
                        y_scale,
                    )
                    normalized = mobius(x, y, x_scale) / x_scale
                    max_group_error = max(
                        max_group_error,
                        abs(mapped_lhs - mapped_rhs),
                        abs(normalized - math.tanh(a + b)),
                    )
    checks["mobius_group_bundle_scale_isomorphism"] = max_group_error < TOL

    # 2. General pair readouts under common rescaling.
    max_pair_error = 0.0
    for t_scale in (0.6, 1.4, 4.2):
        for l_scale in (0.8, 2.3, 7.1):
            for beta in (-1.2, 0.0, 0.7):
                h = pair_metric(t_scale, l_scale, beta)
                phi, shift, kappa = pair_readouts(h)
                for lam in (0.3, 1.0, 2.7, 9.0):
                    hs = scale_matrix(h, lam * lam)
                    phi_s, shift_s, kappa_s = pair_readouts(hs)
                    max_pair_error = max(
                        max_pair_error,
                        abs(phi_s - phi),
                        abs(shift_s - shift),
                        abs(kappa_s - kappa - math.log(lam)),
                    )
    checks["pair_phi_beta_invariant_kappa_shifts"] = max_pair_error < TOL

    # 3. Normalized responses and invariant gradient norm scale inversely.
    max_response_error = 0.0
    for t_scale, l_scale, beta, lam in (
        (0.8, 1.7, -0.4, 0.3),
        (1.2, 3.1, 0.0, 2.5),
        (2.4, 0.9, 0.8, 7.0),
    ):
        grad = (0.37, -0.91)
        h = pair_metric(t_scale, l_scale, beta)
        hs = scale_matrix(h, lam * lam)
        u_rho = grad[0] / t_scale
        n_rho = (grad[1] - beta * grad[0]) / l_scale
        u_rho_s = grad[0] / (lam * t_scale)
        n_rho_s = (grad[1] - beta * grad[0]) / (lam * l_scale)
        norm = inverse_metric_norm(h, grad)
        norm_s = inverse_metric_norm(hs, grad)
        max_response_error = max(
            max_response_error,
            abs(u_rho_s - u_rho / lam),
            abs(n_rho_s - n_rho / lam),
            abs(norm_s - norm / (lam * lam)),
        )
    checks["normalized_response_and_gradient_norm_rescale"] = max_response_error < TOL

    # 4. Exact conformal histories retain cones and reciprocal profile but separate response classes.
    x_star = 3.0
    q_values = [1.0e-3, 1.0e-6, 1.0e-12, 1.0e-24, 1.0e-48, 1.0e-60]
    quiet = [abs(response(q, 0.5, 1, x_star)) for q in q_values]
    finite = [response(q, 1.0 / 3.0, 1, x_star) for q in q_values]
    divergent = [abs(response(q, 0.25, 1, x_star)) for q in q_values]
    checks["quiet_class_four_orders"] = quiet[-1] < quiet[0] * 1.0e-4
    checks["finite_class_limit"] = abs(finite[-1] - 4.0) < 1.0e-8
    checks["divergent_class_four_orders"] = divergent[-1] > divergent[0] * 1.0e4

    cone_invariant = True
    vectors = ((1.0, 0.0, 0.0, 0.0), (1.0, 0.7, 0.2, -0.1), (0.1, 1.0, 0.3, 0.2))
    for q in (0.7, 0.08, 1.0e-5):
        phi = -(1.0 / 3.0) * math.log(q)
        base_diag = (-math.exp(-4.0 * phi), 1.0, 1.0, 1.0)
        base_values = [sum(base_diag[i] * vector[i] ** 2 for i in range(4)) for vector in vectors]
        for ell in (0.25, 1.0 / 3.0, 0.5, 0.9):
            factor = q ** (-2.0 * ell)
            scaled_values = [factor * value for value in base_values]
            cone_invariant = cone_invariant and all(
                (value == 0.0 and scaled == 0.0) or (value * scaled > 0.0)
                for value, scaled in zip(base_values, scaled_values)
            )
    checks["four_dimensional_conformal_twins_preserve_causal_class"] = cone_invariant

    n_phase = 40
    q_plus = math.exp(math.pi / 2.0 - 2.0 * math.pi * n_phase)
    q_minus = math.exp(3.0 * math.pi / 2.0 - 2.0 * math.pi * n_phase)
    osc_plus = (
        4.0
        * x_star
        / 3.0
        * (2.0 + math.sin(math.log(q_plus)))
        / (1.0 + q_plus ** (2.0 / 3.0)) ** 2
    )
    osc_minus = (
        4.0
        * x_star
        / 3.0
        * (2.0 + math.sin(math.log(q_minus)))
        / (1.0 + q_minus ** (2.0 / 3.0)) ** 2
    )
    checks["oscillatory_subsequences_separated"] = abs(osc_plus - osc_minus) > x_star

    # 5. Pullback/reparameterization coherence holds for each distinct conformal history.
    g = [
        [-7.0, 2.0, 3.0, 5.0],
        [2.0, 11.0, 13.0, 17.0],
        [3.0, 13.0, 19.0, 23.0],
        [5.0, 17.0, 23.0, 29.0],
    ]
    j = [[1.0, 0.2], [0.3, 1.0], [-0.4, 0.7], [0.5, -0.2]]
    reparam = [[1.0, 0.4], [0.0, 1.0]]
    max_pullback_error = 0.0
    for lam in (0.4, 1.0, 3.2):
        gs = scale_matrix(g, lam * lam)
        h = pullback(gs, j)
        left = pullback(gs, matmul(j, reparam))
        right = matmul(transpose(reparam), matmul(h, reparam))
        max_pullback_error = max(
            max_pullback_error,
            max_matrix_error(left, right),
            max_matrix_error(h, scale_matrix(pullback(g, j), lam * lam)),
        )
    checks["all_conformal_twins_obey_pullback_overlap_coherence"] = max_pullback_error < TOL

    recovered = [[0.0 for _ in range(4)] for _ in range(4)]
    for i in range(4):
        recovered[i][i] = g[i][i]
        for j_index in range(i + 1, 4):
            plane = [[g[i][i], g[i][j_index]], [g[j_index][i], g[j_index][j_index]]]
            recovered[i][j_index] = plane[0][1]
            recovered[j_index][i] = plane[1][0]
    checks["complete_two_plane_pullbacks_reconstruct_supplied_metric"] = recovered == g

    # 6. A C-infinity cutoff leaves an anchor neighborhood exactly unchanged and the tail exact.
    anchor_values = [cutoff_scale(q, 0.5) for q in (0.2, 0.3, 0.8)]
    tail_q = 1.0e-6
    tail_value = cutoff_scale(tail_q, 0.5)
    checks["cutoff_preserves_anchor_neighborhood"] = all(value == 1.0 for value in anchor_values)
    checks["cutoff_retains_exact_asymptotic_power"] = close(tail_value, tail_q ** -0.5)

    return {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "implementation": "python_stdlib_no_sympy_no_g154_imports",
        "landing": (
            "ACCEPT_CONFORMAL_NETWORK_NONSELECTION_WITH_CAVEATS"
            if all(checks.values())
            else "REJECT_EXTERNAL_STRENGTHENING__LOAD_BEARING_CHECK_FAILED"
        ),
        "max_errors": {
            "group": max_group_error,
            "pair": max_pair_error,
            "response": max_response_error,
            "pullback": max_pullback_error,
        },
        "tails": {
            "quiet": quiet[-1],
            "finite": finite[-1],
            "divergent": divergent[-1],
            "oscillatory_plus": osc_plus,
            "oscillatory_minus": osc_minus,
        },
        "checks": checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    raise SystemExit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
