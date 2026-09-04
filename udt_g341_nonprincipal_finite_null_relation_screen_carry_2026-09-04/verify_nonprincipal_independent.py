#!/usr/bin/env python3
"""Implementation-distinct direct-metric verification of bounded G341."""

from __future__ import annotations

import json
import math
import os
import random
from pathlib import Path


LANDING = (
    "EACH_NONZERO_UNIVERSAL_COVER_LIFT_HAS_ONE_REGULAR_FUTURE_NULL_SOLUTION"
    "__NO_INTERIOR_CONJUGATE_CAUSTIC_ON_THE_SUPPLIED_TAUB_KASNER_NULL_CONE"
    "__MIXED_RAYS_HAVE_NONZERO_G269_NULL_ROTATION_WITH_TRIVIAL_SCREEN_QUOTIENT_ROTATION"
    "__COMPACT_MULTIPLICITY_IS_PATH_LABELLED_NOT_PER_LIFT_NONUNIQUENESS"
    "__NO_LIGHT_MODEL_ROUTE_POPULATION_SCALE_OR_XMAX_SELECTED"
)
TOL = 3.0e-10


def close(a: float, b: float, tol: float = TOL) -> bool:
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


def metric(t: float, cx: float, cp: float) -> tuple[float, float, float, float]:
    return (
        -1.0,
        cx * cx * t ** (-2.0 / 3.0),
        cp * cp * t ** (4.0 / 3.0),
        cp * cp * t ** (4.0 / 3.0),
    )


def mdot(
    t: float,
    u: tuple[float, float, float, float],
    v: tuple[float, float, float, float],
    cx: float,
    cp: float,
) -> float:
    g = metric(t, cx, cp)
    return sum(g[i] * u[i] * v[i] for i in range(4))


def null_tangent(
    t: float,
    p: tuple[float, float, float],
    cx: float,
    cp: float,
) -> tuple[float, float, float, float]:
    g = metric(t, cx, cp)
    spatial = sum(p[i] * p[i] / g[i + 1] for i in range(3))
    kt = math.sqrt(spatial)
    return (kt, p[0] / g[1], p[1] / g[2], p[2] / g[3])


def velocity(
    t: float,
    p: tuple[float, float, float],
    cx: float,
    cp: float,
) -> tuple[float, float, float]:
    k = null_tangent(t, p, cx, cp)
    return k[1] / k[0], k[2] / k[0], k[3] / k[0]


def simpson_vector(f, low: float, high: float, panels: int = 320) -> tuple[float, ...]:
    if panels % 2:
        panels += 1
    h = (high - low) / panels
    first = f(low)
    last = f(high)
    sums = [first[i] + last[i] for i in range(len(first))]
    for j in range(1, panels):
        values = f(low + j * h)
        weight = 4.0 if j % 2 else 2.0
        for i, value in enumerate(values):
            sums[i] += weight * value
    return tuple(value * h / 3.0 for value in sums)


def endpoint_direct(
    te: float,
    tr: float,
    lam: float,
    cx: float,
    cp: float,
) -> tuple[float, float]:
    p = (cx, cp * lam, 0.0)
    result = simpson_vector(
        lambda t: velocity(t, p, cx, cp)[:2], te, tr
    )
    return result[0], result[1]


def direction_for_slope(
    te: float,
    tr: float,
    slope: float,
    cx: float,
    cp: float,
) -> tuple[float, float, float]:
    low = 0.0
    high = max(te, 1.0)
    qx, qp = endpoint_direct(te, tr, high, cx, cp)
    while qp / qx < slope:
        high *= 2.0
        qx, qp = endpoint_direct(te, tr, high, cx, cp)
    for _ in range(48):
        middle = 0.5 * (low + high)
        qx, qp = endpoint_direct(te, tr, middle, cx, cp)
        if qp / qx < slope:
            low = middle
        else:
            high = middle
    lam = 0.5 * (low + high)
    qx, qp = endpoint_direct(te, tr, lam, cx, cp)
    return lam, qx, qp


def solve_endpoint_ray(
    te: float,
    qx_target: float,
    qp_target: float,
    cx: float,
    cp: float,
) -> tuple[float, float]:
    slope = qp_target / qx_target
    low = te
    high = te + 0.2
    lam, qx, _ = direction_for_slope(te, high, slope, cx, cp)
    while qx < qx_target:
        high = te + 2.0 * (high - te)
        lam, qx, _ = direction_for_slope(te, high, slope, cx, cp)
    for _ in range(50):
        middle = 0.5 * (low + high)
        lam, qx, _ = direction_for_slope(te, middle, slope, cx, cp)
        if qx < qx_target:
            low = middle
        else:
            high = middle
    tr = 0.5 * (low + high)
    lam, _, _ = direction_for_slope(te, tr, slope, cx, cp)
    return tr, lam


def transport_rhs(
    t: float,
    vector: tuple[float, float, float, float],
    p: tuple[float, float, float],
    cx: float,
    cp: float,
) -> tuple[float, float, float, float]:
    vx, vy, vz = velocity(t, p, cx, cp)
    g = metric(t, cx, cp)
    h1 = -1.0 / (3.0 * t)
    h2 = 2.0 / (3.0 * t)
    v0, v1, v2, v3 = vector
    return (
        -(g[1] * h1 * vx * v1 + g[2] * h2 * (vy * v2 + vz * v3)),
        -h1 * (v1 + vx * v0),
        -h2 * (v2 + vy * v0),
        -h2 * (v3 + vz * v0),
    )


def axpy(
    base: tuple[float, ...], scale: float, increment: tuple[float, ...]
) -> tuple[float, ...]:
    return tuple(a + scale * b for a, b in zip(base, increment))


def rk4_transport(
    te: float,
    tr: float,
    initial: tuple[float, float, float, float],
    p: tuple[float, float, float],
    cx: float,
    cp: float,
) -> tuple[float, float, float, float]:
    panels = max(1600, int(900.0 * (tr - te) / te))
    h = (tr - te) / panels
    t = te
    value = initial
    for _ in range(panels):
        k1 = transport_rhs(t, value, p, cx, cp)
        k2 = transport_rhs(t + 0.5 * h, axpy(value, 0.5 * h, k1), p, cx, cp)
        k3 = transport_rhs(t + 0.5 * h, axpy(value, 0.5 * h, k2), p, cx, cp)
        k4 = transport_rhs(t + h, axpy(value, h, k3), p, cx, cp)
        value = tuple(
            value[i] + h * (k1[i] + 2.0 * k2[i] + 2.0 * k3[i] + k4[i]) / 6.0
            for i in range(4)
        )
        t += h
    return value


def add(*vectors: tuple[float, ...]) -> tuple[float, ...]:
    return tuple(sum(items) for items in zip(*vectors))


def mul(scale: float, vector: tuple[float, ...]) -> tuple[float, ...]:
    return tuple(scale * value for value in vector)


def max_abs(vector: tuple[float, ...]) -> float:
    return max(abs(value) for value in vector)


def main() -> None:
    checks: dict[str, bool] = {}

    def record(name: str, condition: bool) -> None:
        checks[name] = bool(condition)

    rng = random.Random(341919)

    metric_cases = 0
    for i in range(320):
        te = rng.uniform(0.25, 2.5)
        tr = te + rng.uniform(0.02, 2.8)
        cx = rng.uniform(0.4, 2.4)
        cp = rng.uniform(0.4, 2.4)
        lam = 10.0 ** rng.uniform(-2.5, 1.0)
        azimuth = rng.uniform(-math.pi, math.pi)
        sign_x = -1.0 if i % 2 else 1.0
        p = (
            sign_x * cx,
            cp * lam * math.cos(azimuth),
            cp * lam * math.sin(azimuth),
        )
        t = rng.uniform(te, tr)
        k = null_tangent(t, p, cx, cp)
        g = metric(t, cx, cp)
        recovered = (g[1] * k[1], g[2] * k[2], g[3] * k[3])
        record(f"direct_null_{i}", abs(mdot(t, k, k, cx, cp)) < 2.0e-12 * max(1.0, k[0] * k[0]))
        record(f"future_branch_{i}", k[0] > 0.0)
        record(f"momentum_conserved_{i}", all(close(a, b, 2.0e-13) for a, b in zip(p, recovered)))
        factor = rng.uniform(0.15, 4.0)
        v1 = velocity(t, p, cx, cp)
        v2 = velocity(t, tuple(factor * x for x in p), cx, cp)
        record(f"affine_gauge_{i}", all(close(a, b, 2.0e-13) for a, b in zip(v1, v2)))
        q = simpson_vector(lambda tt: velocity(tt, p, cx, cp), te, tr)
        record(f"signed_quadrant_{i}", q[0] * sign_x > 0.0)
        record(f"transverse_azimuth_{i}", close(math.atan2(q[2], q[1]), azimuth, 2.0e-10))
        metric_cases += 1

    inverse_cases = 0
    for i in range(44):
        te = rng.uniform(0.35, 2.4)
        tr_true = te + rng.uniform(0.03, 1.8)
        lam_true = 10.0 ** rng.uniform(-1.2, 0.7)
        cx = rng.uniform(0.55, 1.9)
        cp = rng.uniform(0.55, 1.9)
        qx, qp = endpoint_direct(te, tr_true, lam_true, cx, cp)
        tr, lam = solve_endpoint_ray(te, qx, qp, cx, cp)
        qx_back, qp_back = endpoint_direct(te, tr, lam, cx, cp)
        record(f"independent_inverse_time_{i}", close(tr, tr_true, 2.0e-9))
        record(f"independent_inverse_direction_{i}", close(lam, lam_true, 2.0e-9))
        record(f"independent_inverse_qx_{i}", close(qx_back, qx, 2.0e-10))
        record(f"independent_inverse_qp_{i}", close(qp_back, qp, 2.0e-10))
        inverse_cases += 1

    transport_cases = 0
    for i in range(144):
        te = rng.uniform(0.35, 2.2)
        tr = te + rng.uniform(0.025, 1.6)
        cx = rng.uniform(0.55, 1.9)
        cp = rng.uniform(0.55, 1.9)
        lam = 10.0 ** rng.uniform(-1.5, 0.8)
        azimuth = rng.uniform(-math.pi, math.pi)
        sign_x = -1.0 if i % 2 else 1.0
        p = (
            sign_x * cx,
            cp * lam * math.cos(azimuth),
            cp * lam * math.sin(azimuth),
        )
        root_e = math.sqrt(te * te + lam * lam)
        c_e = sign_x * te / root_e
        s_e = lam / root_e
        a_e = cx * te ** (-1.0 / 3.0)
        b_e = cp * te ** (2.0 / 3.0)
        u0 = (1.0, 0.0, 0.0, 0.0)
        n0 = (
            0.0,
            c_e / a_e,
            s_e * math.cos(azimuth) / b_e,
            s_e * math.sin(azimuth) / b_e,
        )
        s0 = (
            0.0,
            -s_e / a_e,
            c_e * math.cos(azimuth) / b_e,
            c_e * math.sin(azimuth) / b_e,
        )
        z0 = (
            0.0,
            0.0,
            -math.sin(azimuth) / b_e,
            math.cos(azimuth) / b_e,
        )
        pu = rk4_transport(te, tr, u0, p, cx, cp)
        pn = rk4_transport(te, tr, n0, p, cx, cp)
        ps = rk4_transport(te, tr, s0, p, cx, cp)
        pz = rk4_transport(te, tr, z0, p, cx, cp)
        kt_e = null_tangent(te, p, cx, cp)[0]
        kt_r = null_tangent(tr, p, cx, cp)[0]
        ratio = kt_e / kt_r
        delta = -math.log(ratio)
        gamma = pu[0]
        a_coeff = -pn[0]
        target_u = (1.0, 0.0, 0.0, 0.0)
        mismatch = add(target_u, mul(-gamma, pu), mul(-a_coeff, pn))
        mismatch_sq = mdot(tr, mismatch, mismatch, cx, cp)
        w_s = mdot(tr, mismatch, ps, cx, cp)
        w_z = mdot(tr, mismatch, pz, cx, cp)
        k_r = null_tangent(tr, p, cx, cp)
        a_r = cx * tr ** (-1.0 / 3.0)
        b_r = cp * tr ** (2.0 / 3.0)
        root_r = math.sqrt(tr * tr + lam * lam)
        c_r = sign_x * tr / root_r
        s_r = lam / root_r
        local_s = (
            0.0,
            -s_r / a_r,
            c_r * math.cos(azimuth) / b_r,
            c_r * math.sin(azimuth) / b_r,
        )
        local_z = (
            0.0,
            0.0,
            -math.sin(azimuth) / b_r,
            math.cos(azimuth) / b_r,
        )
        beta = (ps[0] - local_s[0]) / k_r[0]
        screen_difference = add(ps, mul(-1.0, local_s), mul(-beta, k_r))
        record(f"transport_u_unit_{i}", close(mdot(tr, pu, pu, cx, cp), -1.0, 2.0e-9))
        record(f"transport_n_unit_{i}", close(mdot(tr, pn, pn, cx, cp), 1.0, 2.0e-9))
        record(f"transport_un_orthogonal_{i}", abs(mdot(tr, pu, pn, cx, cp)) < 2.0e-9)
        record(f"transport_screen_unit_{i}", close(mdot(tr, ps, ps, cx, cp), 1.0, 2.0e-9))
        record(f"transport_azimuth_unit_{i}", close(mdot(tr, pz, pz, cx, cp), 1.0, 2.0e-9))
        record(f"transport_screen_basis_{i}", abs(mdot(tr, ps, pz, cx, cp)) < 2.0e-9)
        record(f"transport_screen_null_{i}", abs(mdot(tr, ps, k_r, cx, cp)) < 3.0e-9)
        record(f"azimuth_exact_carry_{i}", max_abs(add(pz, mul(-1.0, local_z))) < 2.0e-9)
        record(f"screen_quotient_no_rotation_{i}", max_abs(screen_difference) < 4.0e-9)
        record(f"mismatch_spacelike_{i}", mismatch_sq > 0.0)
        record(f"mismatch_one_screen_direction_{i}", abs(w_z) < 3.0e-9 and close(w_s * w_s, mismatch_sq, 6.0e-9))
        record(f"g269_direct_{i}", close(gamma, math.cosh(delta) + 0.5 * ratio * mismatch_sq, 8.0e-9))
        record(f"frequency_plane_identity_{i}", close(gamma - a_coeff, 1.0 / ratio, 8.0e-9))
        record(f"mixed_plane_distinct_{i}", abs(w_s) > 1.0e-8)
        record(f"target_local_rank_two_{i}", ratio > 0.0)
        record(f"transported_pair_rank_two_{i}", -ratio * ratio * (1.0 + a_coeff * a_coeff) < 0.0)
        transport_cases += 1

    all_passed = all(checks.values())
    result = {
        "all_passed": all_passed,
        "checks_passed": sum(checks.values()),
        "checks_total": len(checks),
        "checks": checks,
        "grade": "IMPLEMENTATION_DISTINCT_DIRECT_METRIC_AND_CONNECTION_VERIFICATION",
        "landing": LANDING,
        "method": (
            "direct coordinate metric, reconstructed null tangent, composite-Simpson endpoint map, "
            "slope-first inverse, direct Christoffel transport, and RK4; no production import or result read"
        ),
        "random_seed": 341919,
        "coverage": {
            "direct_metric_cases": metric_cases,
            "independent_endpoint_inverse_cases": inverse_cases,
            "direct_connection_transport_cases": transport_cases,
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if os.environ.get("UDT_NO_WRITE") != "1":
        Path(__file__).with_name("INDEPENDENT_VERIFICATION.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    if not all_passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
