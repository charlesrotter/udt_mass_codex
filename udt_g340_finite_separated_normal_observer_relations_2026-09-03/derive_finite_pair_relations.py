#!/usr/bin/env python3
"""Production checks for the bounded G340 finite-separated pair classification."""

from __future__ import annotations

import json
import math
import os
import random
from pathlib import Path


PREREGISTRATION_COMMIT = "d2b68663"
LANDING = (
    "METRIC_NULL_GEOMETRY_CLOSES_A_PATH_LABELLED_FINITE_NORMAL_PAIR_FAMILY"
    "__NO_PHENOMENOLOGICAL_LIGHT_MODEL_REQUIRED"
    "__SLICE_DISTANCE_NULL_EXCHANGE_RADAR_AND_PROJECTIVE_READOUT_ARE_RELATED_NOT_IDENTICAL"
    "__COMPACT_WINDINGS_REMAIN_DISTINCT_BRANCHES"
    "__NO_PHYSICAL_PROTOCOL_POPULATION_SCALE_OR_XMAX_SELECTED"
)
TOL = 2.0e-11


def scale_x(t: float, cx: float) -> float:
    return cx * t ** (-1.0 / 3.0)


def scale_p(t: float, cp: float) -> float:
    return cp * t ** (2.0 / 3.0)


def omega(t: float, px: float, py: float, pz: float, cx: float, cp: float) -> float:
    return math.sqrt(
        px * px * t ** (2.0 / 3.0) / (cx * cx)
        + (py * py + pz * pz) * t ** (-4.0 / 3.0) / (cp * cp)
    )


def null_velocity(
    t: float, px: float, py: float, pz: float, cx: float, cp: float
) -> tuple[float, float, float]:
    w = omega(t, px, py, pz, cx, cp)
    return (
        px * t ** (2.0 / 3.0) / (cx * cx * w),
        py * t ** (-4.0 / 3.0) / (cp * cp * w),
        pz * t ** (-4.0 / 3.0) / (cp * cp * w),
    )


def arrival_x(te: float, q: float, cx: float) -> float:
    return (te ** (4.0 / 3.0) + 4.0 * cx * q / 3.0) ** (3.0 / 4.0)


def arrival_p(te: float, q: float, cp: float) -> float:
    return (te ** (1.0 / 3.0) + cp * q / 3.0) ** 3


def lift_x(te: float, tr: float, cx: float) -> float:
    return 3.0 * (tr ** (4.0 / 3.0) - te ** (4.0 / 3.0)) / (4.0 * cx)


def lift_p(te: float, tr: float, cp: float) -> float:
    return 3.0 * (tr ** (1.0 / 3.0) - te ** (1.0 / 3.0)) / cp


def ratio_depth_projective(axis: str, te: float, tr: float) -> tuple[float, float, float, float]:
    if axis == "x":
        ratio = (te / tr) ** (1.0 / 3.0)
    else:
        ratio = (tr / te) ** (2.0 / 3.0)
    delta = -math.log(ratio)
    chi = math.tanh(delta)
    mutual = 1.0 / math.cosh(delta)
    return ratio, delta, chi, mutual


def slice_length(axis: str, t: float, q: float, cx: float, cp: float) -> float:
    return (scale_x(t, cx) if axis == "x" else scale_p(t, cp)) * q


def radar_events(
    axis: str,
    tb: float,
    q_out: float,
    q_return: float,
    cx: float,
    cp: float,
) -> tuple[float, float]:
    if axis == "x":
        base = tb ** (4.0 / 3.0)
        tm = (base - 4.0 * cx * q_out / 3.0) ** (3.0 / 4.0)
        tp = (base + 4.0 * cx * q_return / 3.0) ** (3.0 / 4.0)
    else:
        base = tb ** (1.0 / 3.0)
        tm = (base - cp * q_out / 3.0) ** 3
        tp = (base + cp * q_return / 3.0) ** 3
    return tm, tp


def radar_rate(axis: str, tm: float, tb: float, tp: float) -> float:
    if axis == "x":
        return 2.0 / ((tb / tm) ** (1.0 / 3.0) + (tb / tp) ** (1.0 / 3.0))
    return 2.0 / ((tm / tb) ** (2.0 / 3.0) + (tp / tb) ** (2.0 / 3.0))


def simpson(f, a: float, b: float, panels: int = 4096) -> float:
    if panels % 2:
        panels += 1
    h = (b - a) / panels
    total = f(a) + f(b)
    for i in range(1, panels):
        total += (4.0 if i % 2 else 2.0) * f(a + i * h)
    return total * h / 3.0


def close(a: float, b: float, tol: float = TOL) -> bool:
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


def main() -> None:
    checks: dict[str, bool] = {}

    def record(name: str, condition: bool) -> None:
        checks[name] = bool(condition)

    case = 0
    for cx in (0.7, 1.3, 2.2):
        for cp in (0.8, 1.7):
            for te in (0.4, 1.0, 2.5):
                for q in (0.03, 0.2, 0.9):
                    for axis in ("x", "p"):
                        tr = arrival_x(te, q, cx) if axis == "x" else arrival_p(te, q, cp)
                        recovered = lift_x(te, tr, cx) if axis == "x" else lift_p(te, tr, cp)
                        record(f"arrival_inverse_{case}", close(q, recovered))
                        record(f"future_arrival_{case}", tr > te > 0.0)
                        px, py = ((1.4, 0.0) if axis == "x" else (0.0, 1.4))
                        w_e = omega(te, px, py, 0.0, cx, cp)
                        w_r = omega(tr, px, py, 0.0, cx, cp)
                        ratio, delta, chi, mutual = ratio_depth_projective(axis, te, tr)
                        record(f"frequency_ratio_{case}", close(ratio, w_e / w_r))
                        record(f"depth_ratio_{case}", close(math.exp(-delta), ratio))
                        record(f"projective_ratio_{case}", close(chi, (1.0 - ratio * ratio) / (1.0 + ratio * ratio)))
                        record(f"mutual_ratio_{case}", close(mutual, 2.0 * ratio / (1.0 + ratio * ratio)))
                        vx, vy, vz = null_velocity(te, px, py, 0.0, cx, cp)
                        null_residual = -1.0 + scale_x(te, cx) ** 2 * vx * vx + scale_p(te, cp) ** 2 * (vy * vy + vz * vz)
                        record(f"null_velocity_{case}", abs(null_residual) <= TOL)
                        integrand = (
                            (lambda t: null_velocity(t, px, py, 0.0, cx, cp)[0])
                            if axis == "x"
                            else (lambda t: null_velocity(t, px, py, 0.0, cx, cp)[1])
                        )
                        numeric_q = abs(simpson(integrand, te, tr, 1024))
                        record(f"null_quadrature_{case}", close(numeric_q, q, 3.0e-12))
                        record(f"slice_positive_{case}", slice_length(axis, te, q, cx, cp) > 0.0)
                        case += 1

    radar_case = 0
    for axis in ("x", "p"):
        for cx, cp in ((0.8, 1.1), (1.3, 0.7), (2.0, 1.8)):
            for tb in (0.8, 1.7, 3.4):
                if axis == "x":
                    q_max = 0.5 * 3.0 * tb ** (4.0 / 3.0) / (4.0 * cx)
                else:
                    q_max = 0.5 * 3.0 * tb ** (1.0 / 3.0) / cp
                for out_fraction in (0.08, 0.21, 0.43):
                    for return_fraction in (0.11, 0.27):
                        q_out = out_fraction * q_max
                        q_return = return_fraction * q_max
                        tm, tp = radar_events(axis, tb, q_out, q_return, cx, cp)
                        record(f"radar_order_{radar_case}", 0.0 < tm < tb < tp)
                        q_out_back = lift_x(tm, tb, cx) if axis == "x" else lift_p(tm, tb, cp)
                        q_ret_back = lift_x(tb, tp, cx) if axis == "x" else lift_p(tb, tp, cp)
                        record(f"radar_outgoing_{radar_case}", close(q_out, q_out_back))
                        record(f"radar_return_{radar_case}", close(q_return, q_ret_back))
                        midpoint = 0.5 * (tm + tp)
                        radar_range = 0.5 * (tp - tm)
                        record(f"radar_positive_{radar_case}", radar_range > 0.0 and midpoint > 0.0)
                        eps = tb * 1.0e-6
                        tm_lo, tp_lo = radar_events(axis, tb - eps, q_out, q_return, cx, cp)
                        tm_hi, tp_hi = radar_events(axis, tb + eps, q_out, q_return, cx, cp)
                        derivative_mid = ((tm_hi + tp_hi) - (tm_lo + tp_lo)) / (4.0 * eps)
                        numerical_rate = 1.0 / derivative_mid
                        record(f"radar_rate_{radar_case}", close(numerical_rate, radar_rate(axis, tm, tb, tp), 3.0e-10))
                        # c_E converts each clock interval and cancels from the geometric radar length.
                        for c_e in (0.3, 1.0, 299792458.0):
                            tau_m, tau_p = tm / c_e, tp / c_e
                            recovered_length = 0.5 * c_e * (tau_p - tau_m)
                            record(f"ce_conversion_{radar_case}_{c_e}", close(recovered_length, radar_range, 2.0e-10))
                        radar_case += 1

    symmetric_case = 0
    for axis in ("x", "p"):
        for tb in (0.7, 1.2, 2.8):
            cx, cp = 1.2, 0.9
            q = 0.07 * (3.0 * tb ** (4.0 / 3.0) / (4.0 * cx) if axis == "x" else 3.0 * tb ** (1.0 / 3.0) / cp)
            tm, tp = radar_events(axis, tb, q, q, cx, cp)
            if axis == "x":
                relation = 0.5 * (tm ** (4.0 / 3.0) + tp ** (4.0 / 3.0))
                target = tb ** (4.0 / 3.0)
            else:
                relation = 0.5 * (tm ** (1.0 / 3.0) + tp ** (1.0 / 3.0))
                target = tb ** (1.0 / 3.0)
            record(f"symmetric_power_midpoint_{symmetric_case}", close(relation, target))
            record(f"arithmetic_midpoint_not_reflection_{symmetric_case}", not close(0.5 * (tm + tp), tb, 1.0e-8))
            d_slice = slice_length(axis, tb, q, cx, cp)
            d_radar = 0.5 * (tp - tm)
            record(f"slice_not_radar_{symmetric_case}", not close(d_slice, d_radar, 1.0e-8))
            symmetric_case += 1

    # Every winding is retained; the shortest lift gives the earliest principal arrival.
    winding_case = 0
    for axis in ("x", "p"):
        for delta in (0.13, 0.37, 0.5):
            period = 1.0
            lifts = [(n, abs(delta + n * period)) for n in range(-4, 5)]
            arrivals = [
                (n, arrival_x(1.1, q, 1.3) if axis == "x" else arrival_p(1.1, q, 0.8))
                for n, q in lifts
            ]
            q_min = min(q for _, q in lifts)
            t_min = min(t for _, t in arrivals)
            record(f"winding_earliest_{winding_case}", all((t == t_min) == close(q, q_min) for (n, q), (_, t) in zip(lifts, arrivals)))
            record(f"winding_branches_retained_{winding_case}", len({round(t, 13) for _, t in arrivals}) >= 5)
            if delta == 0.5:
                record(f"cut_locus_tie_{winding_case}", sum(close(q, q_min) for _, q in lifts) == 2)
            winding_case += 1

    # General nonprincipal null Hamiltonian and quadrature checks.
    rng = random.Random(340031)
    for i in range(400):
        cx = rng.uniform(0.4, 2.5)
        cp = rng.uniform(0.4, 2.5)
        te = rng.uniform(0.25, 2.5)
        tr = te + rng.uniform(0.03, 2.0)
        px, py, pz = (rng.uniform(-2.0, 2.0) for _ in range(3))
        if px * px + py * py + pz * pz < 0.05:
            px += 0.7
        t = rng.uniform(te, tr)
        w = omega(t, px, py, pz, cx, cp)
        vx, vy, vz = null_velocity(t, px, py, pz, cx, cp)
        residual = -1.0 + scale_x(t, cx) ** 2 * vx * vx + scale_p(t, cp) ** 2 * (vy * vy + vz * vz)
        record(f"general_null_{i}", abs(residual) <= TOL)
        factor = rng.uniform(0.2, 4.0)
        v_scaled = null_velocity(t, factor * px, factor * py, factor * pz, cx, cp)
        record(f"momentum_scale_gauge_{i}", all(close(a, b) for a, b in zip((vx, vy, vz), v_scaled)))
        displacements = tuple(
            simpson(lambda tt, j=j: null_velocity(tt, px, py, pz, cx, cp)[j], te, tr, 512)
            for j in range(3)
        )
        record(f"general_quadrature_finite_{i}", all(math.isfinite(v) for v in displacements))
        # Transverse rotations leave frequency and transverse displacement norm unchanged.
        angle = rng.uniform(-math.pi, math.pi)
        py2 = math.cos(angle) * py - math.sin(angle) * pz
        pz2 = math.sin(angle) * py + math.cos(angle) * pz
        disp_rot = tuple(
            simpson(lambda tt, j=j: null_velocity(tt, px, py2, pz2, cx, cp)[j], te, tr, 512)
            for j in range(3)
        )
        record(f"transverse_frequency_rotation_{i}", close(omega(t, px, py, pz, cx, cp), omega(t, px, py2, pz2, cx, cp)))
        record(f"transverse_displacement_rotation_{i}", close(math.hypot(displacements[1], displacements[2]), math.hypot(disp_rot[1], disp_rot[2]), 4.0e-11))

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
            "principal_one_way_cases": case,
            "radar_cases": radar_case,
            "symmetric_radar_cases": symmetric_case,
            "winding_cases": winding_case,
            "general_null_cases": 400,
        },
        "scope_exclusions": [
            "no electromagnetic light field or luminosity transfer",
            "no physical radar distance or route selection",
            "no observer population or occupancy selection",
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
