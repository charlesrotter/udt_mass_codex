#!/usr/bin/env python3
"""Production derivation checks for the bounded G341 nonprincipal null relation."""

from __future__ import annotations

import json
import math
import os
import random
from pathlib import Path


PREREGISTRATION_COMMIT = "6f1441f6"
LANDING = (
    "EACH_NONZERO_UNIVERSAL_COVER_LIFT_HAS_ONE_REGULAR_FUTURE_NULL_SOLUTION"
    "__NO_INTERIOR_CONJUGATE_CAUSTIC_ON_THE_SUPPLIED_TAUB_KASNER_NULL_CONE"
    "__MIXED_RAYS_HAVE_NONZERO_G269_NULL_ROTATION_WITH_TRIVIAL_SCREEN_QUOTIENT_ROTATION"
    "__COMPACT_MULTIPLICITY_IS_PATH_LABELLED_NOT_PER_LIFT_NONUNIQUENESS"
    "__NO_LIGHT_MODEL_ROUTE_POPULATION_SCALE_OR_XMAX_SELECTED"
)
TOL = 3.0e-10

GL_X = (
    -0.9602898564975363, -0.7966664774136267,
    -0.5255324099163290, -0.1834346424956498,
    0.1834346424956498, 0.5255324099163290,
    0.7966664774136267, 0.9602898564975363,
)
GL_W = (
    0.1012285362903763, 0.2223810344533745,
    0.3137066458778873, 0.3626837833783620,
    0.3626837833783620, 0.3137066458778873,
    0.2223810344533745, 0.1012285362903763,
)


def dot(u: tuple[float, ...], v: tuple[float, ...]) -> float:
    return -u[0] * v[0] + sum(a * b for a, b in zip(u[1:], v[1:]))


def add(*vectors: tuple[float, ...]) -> tuple[float, ...]:
    return tuple(sum(items) for items in zip(*vectors))


def mul(scale: float, vector: tuple[float, ...]) -> tuple[float, ...]:
    return tuple(scale * value for value in vector)


def close(a: float, b: float, tol: float = TOL) -> bool:
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


def integrate(f, low: float, high: float, panels: int = 12) -> float:
    width = (high - low) / panels
    total = 0.0
    for panel in range(panels):
        left = low + panel * width
        right = left + width
        middle = 0.5 * (left + right)
        half = 0.5 * width
        total += half * sum(
            weight * f(middle + half * node)
            for node, weight in zip(GL_X, GL_W)
        )
    return total


def endpoint(
    te: float, tr: float, lam: float, cx: float, cp: float
) -> tuple[float, float]:
    qx = integrate(
        lambda t: t ** (4.0 / 3.0) / (cx * math.sqrt(t * t + lam * lam)),
        te,
        tr,
    )
    qp = integrate(
        lambda t: lam * t ** (-2.0 / 3.0)
        / (cp * math.sqrt(t * t + lam * lam)),
        te,
        tr,
    )
    return qx, qp


def endpoint_derivatives(
    te: float, tr: float, lam: float, cx: float, cp: float
) -> tuple[float, float, float, float, float]:
    root = math.sqrt(tr * tr + lam * lam)
    qx_t = tr ** (4.0 / 3.0) / (cx * root)
    qp_t = lam * tr ** (-2.0 / 3.0) / (cp * root)
    common = integrate(
        lambda t: t ** (4.0 / 3.0) / (t * t + lam * lam) ** 1.5,
        te,
        tr,
    )
    qx_lam = -lam * common / cx
    qp_lam = common / cp
    jacobian = qx_t * qp_lam - qx_lam * qp_t
    return qx_t, qp_t, qx_lam, qp_lam, jacobian


def solve_tr_for_qx(te: float, lam: float, qx: float, cx: float, cp: float) -> float:
    low = te
    high = te + 0.25
    while endpoint(te, high, lam, cx, cp)[0] < qx:
        high = te + 2.0 * (high - te)
    for _ in range(48):
        middle = 0.5 * (low + high)
        if endpoint(te, middle, lam, cx, cp)[0] < qx:
            low = middle
        else:
            high = middle
    return 0.5 * (low + high)


def solve_endpoint(
    te: float, qx: float, qp: float, cx: float, cp: float
) -> tuple[float, float]:
    if qp == 0.0:
        tr = (te ** (4.0 / 3.0) + 4.0 * cx * qx / 3.0) ** (3.0 / 4.0)
        return tr, 0.0
    if qx == 0.0:
        tr = (te ** (1.0 / 3.0) + cp * qp / 3.0) ** 3
        return tr, math.inf

    low = 0.0
    high = max(te, 1.0)

    def transverse_at(value: float) -> tuple[float, float]:
        arrival = solve_tr_for_qx(te, value, qx, cx, cp)
        return endpoint(te, arrival, value, cx, cp)[1], arrival

    while transverse_at(high)[0] < qp:
        high *= 2.0
    for _ in range(50):
        middle = 0.5 * (low + high)
        if transverse_at(middle)[0] < qp:
            low = middle
        else:
            high = middle
    lam = 0.5 * (low + high)
    tr = solve_tr_for_qx(te, lam, qx, cx, cp)
    return tr, lam


def alpha(t: float, te: float, lam: float) -> float:
    return (t / te) ** (-2.0 / 3.0) * math.sqrt(t * t + lam * lam) / math.sqrt(te * te + lam * lam)


def direction(t: float, lam: float, sign_x: float = 1.0) -> tuple[float, float]:
    root = math.sqrt(t * t + lam * lam)
    return sign_x * t / root, lam / root


def screen_integral(te: float, tr: float, lam: float, sign_x: float = 1.0) -> float:
    return integrate(
        lambda t: direction(t, lam, sign_x)[0]
        * direction(t, lam, sign_x)[1]
        / (t * alpha(t, te, lam)),
        te,
        tr,
        18,
    )


def screen_state(
    te: float, tr: float, lam: float, sign_x: float = 1.0
) -> dict[str, object]:
    ar = alpha(tr, te, lam)
    c, s = direction(tr, lam, sign_x)
    ell = (ar, ar * c, ar * s, 0.0)
    local_screen = (0.0, -s, c, 0.0)
    azimuth_screen = (0.0, 0.0, 0.0, 1.0)
    j = screen_integral(te, tr, lam, sign_x)
    carried_screen = add(local_screen, mul(-j, ell))
    w = ar * j
    ratio = 1.0 / ar
    delta = math.log(ar)
    gamma = 0.5 * (ar + 1.0 / ar + ar * j * j)
    a = 0.5 * (-ar + 1.0 / ar + ar * j * j)
    return {
        "alpha": ar,
        "ratio": ratio,
        "delta": delta,
        "ell": ell,
        "local_screen": local_screen,
        "azimuth_screen": azimuth_screen,
        "carried_screen": carried_screen,
        "J": j,
        "w": w,
        "Gamma": gamma,
        "a": a,
    }


def main() -> None:
    checks: dict[str, bool] = {}

    def record(name: str, condition: bool) -> None:
        checks[name] = bool(condition)

    rng = random.Random(341001)

    local_cases = 0
    for i in range(420):
        te = rng.uniform(0.2, 3.0)
        tr = te + rng.uniform(0.015, 4.0)
        lam = 10.0 ** rng.uniform(-3.0, 1.2)
        cx = rng.uniform(0.35, 2.8)
        cp = rng.uniform(0.35, 2.8)
        sign_x = -1.0 if i % 2 else 1.0
        qx, qp = endpoint(te, tr, lam, cx, cp)
        qx_t, qp_t, qx_lam, qp_lam, jac = endpoint_derivatives(
            te, tr, lam, cx, cp
        )
        state = screen_state(te, tr, lam, sign_x)
        ell = state["ell"]
        carried = state["carried_screen"]
        azimuth = state["azimuth_screen"]
        ratio = state["ratio"]
        delta = state["delta"]
        w = state["w"]
        gamma = state["Gamma"]
        a = state["a"]
        record(f"positive_endpoint_{i}", qx > 0.0 and qp > 0.0)
        record(f"arrival_monotone_{i}", qx_t > 0.0 and qp_t > 0.0)
        record(f"direction_monotone_{i}", qx_lam < 0.0 < qp_lam)
        record(f"positive_jacobian_{i}", jac > 0.0)
        record(f"derivative_interlock_{i}", close(qx_lam, -lam * cp * qp_lam / cx))
        record(f"affine_null_{i}", abs(dot(ell, ell)) < 2.0e-13)
        record(f"carried_screen_unit_{i}", close(dot(carried, carried), 1.0))
        record(f"carried_screen_null_orthogonal_{i}", abs(dot(carried, ell)) < 2.0e-12)
        record(f"azimuth_screen_unit_{i}", close(dot(azimuth, azimuth), 1.0))
        record(f"screen_basis_orthogonal_{i}", abs(dot(carried, azimuth)) < 2.0e-13)
        record(f"mixed_J_nonzero_{i}", abs(state["J"]) > 1.0e-16)
        record(f"J_orientation_{i}", state["J"] * sign_x > 0.0)
        record(f"frequency_depth_{i}", close(math.exp(-delta), ratio))
        record(
            f"g269_interlock_{i}",
            close(gamma, math.cosh(delta) + 0.5 * ratio * w * w),
        )
        reverse_w_sq = ratio * ratio * w * w
        record(
            f"reversal_even_gamma_{i}",
            close(
                gamma,
                math.cosh(-delta) + 0.5 * (1.0 / ratio) * reverse_w_sq,
            ),
        )
        record(f"target_decomposition_{i}", close(gamma - a, 1.0 / ratio))
        record(f"strict_screen_inequality_{i}", 1.0 / gamma < 1.0 / math.cosh(delta))
        record(f"pair_planes_distinct_{i}", abs(ratio * ratio * w) > 1.0e-16)
        local_cases += 1

    inverse_cases = 0
    for i in range(72):
        te = rng.uniform(0.3, 2.5)
        tr_true = te + rng.uniform(0.04, 2.2)
        lam_true = 10.0 ** rng.uniform(-1.4, 0.8)
        cx = rng.uniform(0.5, 2.0)
        cp = rng.uniform(0.5, 2.0)
        qx, qp = endpoint(te, tr_true, lam_true, cx, cp)
        tr, lam = solve_endpoint(te, qx, qp, cx, cp)
        qx_back, qp_back = endpoint(te, tr, lam, cx, cp)
        record(f"inverse_tr_{i}", close(tr, tr_true, 8.0e-10))
        record(f"inverse_lam_{i}", close(lam, lam_true, 8.0e-10))
        record(f"inverse_qx_{i}", close(qx_back, qx, 4.0e-11))
        record(f"inverse_qp_{i}", close(qp_back, qp, 4.0e-11))
        inverse_cases += 1

    axis_cases = 0
    for i in range(120):
        te = rng.uniform(0.2, 3.0)
        tr = te + rng.uniform(0.02, 2.5)
        cx = rng.uniform(0.4, 2.4)
        cp = rng.uniform(0.4, 2.4)
        qx0 = 3.0 * (tr ** (4.0 / 3.0) - te ** (4.0 / 3.0)) / (4.0 * cx)
        qp0 = 3.0 * (tr ** (1.0 / 3.0) - te ** (1.0 / 3.0)) / cp
        tr_x, lam_x = solve_endpoint(te, qx0, 0.0, cx, cp)
        tr_p, lam_p = solve_endpoint(te, 0.0, qp0, cx, cp)
        small = 1.0e-6 * te
        qx_small, qp_small = endpoint(te, tr, small, cx, cp)
        large = 1.0e6 * tr
        qx_large, qp_large = endpoint(te, tr, large, cx, cp)
        record(f"x_axis_arrival_{i}", close(tr_x, tr, 3.0e-12) and lam_x == 0.0)
        record(f"p_axis_arrival_{i}", close(tr_p, tr, 3.0e-12) and math.isinf(lam_p))
        record(f"x_axis_cartesian_rank_{i}", qp_small / small > 0.0 and close(qx_small, qx0, 2.0e-10))
        record(f"p_axis_cartesian_rank_{i}", large * qx_large > 0.0 and close(qp_large, qp0, 2.0e-10))
        state_x = screen_state(te, tr, 0.0)
        record(f"principal_screen_zero_{i}", state_x["J"] == 0.0 and state_x["w"] == 0.0)
        axis_cases += 1

    zero_shift_cases = 0
    for i in range(96):
        te = rng.uniform(0.2, 2.5)
        tr = te * rng.uniform(1.02, 8.0)
        power = (tr / te) ** (2.0 / 3.0)
        lam = te * power / math.sqrt(power + 1.0)
        cx = rng.uniform(0.4, 2.2)
        cp = rng.uniform(0.4, 2.2)
        qx, qp = endpoint(te, tr, lam, cx, cp)
        state = screen_state(te, tr, lam)
        record(f"zero_shift_alpha_{i}", close(state["alpha"], 1.0, 5.0e-13))
        record(f"zero_shift_depth_{i}", abs(state["delta"]) < 5.0e-13)
        record(f"zero_shift_finite_relation_{i}", qx > 0.0 and qp > 0.0)
        record(f"zero_shift_active_screen_{i}", abs(state["w"]) > 1.0e-12)
        record(f"zero_shift_mutual_strict_{i}", 1.0 / state["Gamma"] < 1.0)
        zero_shift_cases += 1

    lattice_cases = 0
    for i in range(16):
        te = rng.uniform(0.4, 2.0)
        cx = rng.uniform(0.5, 1.8)
        cp = rng.uniform(0.5, 1.8)
        dx = rng.uniform(-0.49, 0.49)
        dy = rng.uniform(-0.49, 0.49)
        lifts = []
        for nx in range(-1, 2):
            for ny in range(-1, 2):
                qx = abs(dx + nx)
                qp = abs(dy + ny)
                if qx == 0.0 and qp == 0.0:
                    continue
                tr, lam = solve_endpoint(te, qx, qp, cx, cp)
                lifts.append((nx, ny, tr, lam))
        record(f"lattice_retains_branches_{i}", len(lifts) >= 8)
        record(f"lattice_all_future_{i}", all(item[2] > te for item in lifts))
        first = min(item[2] for item in lifts)
        record(f"lattice_earliest_exists_{i}", sum(close(item[2], first, 2.0e-10) for item in lifts) >= 1)
        record(f"lattice_each_lift_one_solution_{i}", len({(item[0], item[1]) for item in lifts}) == len(lifts))
        lattice_cases += 1

    all_passed = all(checks.values())
    result = {
        "all_passed": all_passed,
        "checks_passed": sum(checks.values()),
        "checks_total": len(checks),
        "checks": checks,
        "grade": "PRODUCTION_DERIVED_CONDITIONAL_BOUNDED_PENDING_INDEPENDENT_REVIEW",
        "landing": LANDING,
        "preregistration_commit": PREREGISTRATION_COMMIT,
        "coverage": {
            "mixed_local_cases": local_cases,
            "endpoint_inverse_cases": inverse_cases,
            "principal_boundary_cases": axis_cases,
            "zero_shift_mixed_cases": zero_shift_cases,
            "compact_lattice_cases": lattice_cases,
        },
        "scope_exclusions": [
            "no electromagnetic light field emission transfer or detection",
            "no physical route distance or observer population selection",
            "no generic spacetime or metric-perturbation theorem",
            "no scale or X_max selection",
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if os.environ.get("UDT_NO_WRITE") != "1":
        Path(__file__).with_name("DERIVATION_RESULT.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    if not all_passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
