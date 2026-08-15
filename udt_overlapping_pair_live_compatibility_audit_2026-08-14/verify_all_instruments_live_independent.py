#!/usr/bin/env python3
"""Independent numerical rebuild of the G90 all-instruments-live correction."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "ALL_INSTRUMENTS_LIVE_INDEPENDENT_VERIFICATION.json"
ETA2 = np.diag([-1.0, 1.0])
ETA4 = np.diag([-1.0, 1.0, 1.0, 1.0])


def factors(x: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    sig = 1.0 + x / 31.0
    beta = x / 37.0
    B = np.array([[sig / x, sig * beta / x], [0.0, sig * x]])
    Q = np.array([[1.0 + x / 7.0, x / 11.0], [0.0, 1.0 + x / 13.0]])
    S = np.array([[x / 17.0, x**2 / 19.0], [x**3 / 23.0, x**4 / 29.0]])
    return B, Q, S


def columns(x: float, kind: str) -> tuple[np.ndarray, np.ndarray, float, float]:
    Tp = 1.0 / x
    r = 0.1
    if kind == "flat":
        Lp, s = x, 0.05
    elif kind == "monotone":
        Lp, s = x**2, 0.05
    elif kind == "quiet":
        w = (x - 0.5) * (1.5 - x)
        Lp = x / w**2
        s = 0.25 + 3.0 * (x - 1.0) ** 2
    else:
        raise ValueError(kind)
    U = np.diag([Tp * (1 + r * r) / (1 - r * r), Lp * (1 - s * s) / (1 + s * s)])
    A = np.diag([Tp * 2 * r / (1 - r * r), Lp * 2 * s / (1 + s * s)])
    return U, A, Tp, Lp


def assembled(x: float, kind: str) -> dict[str, np.ndarray | float]:
    B, Q, S = factors(x)
    U, A, Tp, Lp = columns(x, kind)
    Y = np.linalg.solve(B, U)
    Z = np.linalg.solve(Q, A) - S @ Y
    E = np.block([[B, np.zeros((2, 2))], [Q @ S, Q]])
    J = np.vstack([Y, Z])
    V = E @ J
    h = V.T @ ETA4 @ V
    W = Z @ np.linalg.inv(Y)
    C = S + W
    P = C.T @ Q.T @ Q @ C
    Pi = np.linalg.inv(B).T @ P @ np.linalg.inv(B)
    phi_pair = 0.25 * np.log((-np.linalg.det(h)) / h[0, 0] ** 2)
    return {
        "B": B,
        "Q": Q,
        "S": S,
        "Y": Y,
        "Z": Z,
        "E": E,
        "J": J,
        "V": V,
        "U": U,
        "A": A,
        "h": h,
        "target_h": np.diag([-Tp * Tp, Lp * Lp]),
        "g": E.T @ ETA4 @ E,
        "trace": float(np.trace(Pi)),
        "M": float(phi_pair - np.log(x)),
    }


def derivative(kind: str, key: str, x: float, eps: float) -> np.ndarray:
    return (np.asarray(assembled(x + eps, kind)[key]) - np.asarray(assembled(x - eps, kind)[key])) / (2 * eps)


def family_checks(kind: str) -> dict[str, bool]:
    x, eps = 1.0, 2.0e-6
    c = assembled(x, kind)
    d = {key: derivative(kind, key, x, eps) for key in ("B", "Q", "S", "Y", "Z", "h", "g")}
    U, A = np.asarray(c["U"]), np.asarray(c["A"])
    B, Q, S, Y, Z = (np.asarray(c[key]) for key in ("B", "Q", "S", "Y", "Z"))
    R = S @ Y + Z
    HB = (d["B"] @ Y).T @ ETA2 @ U + U.T @ ETA2 @ (d["B"] @ Y)
    HQ = (d["Q"] @ R).T @ A + A.T @ (d["Q"] @ R)
    HS = (Q @ d["S"] @ Y).T @ A + A.T @ (Q @ d["S"] @ Y)
    HY = (B @ d["Y"]).T @ ETA2 @ U + U.T @ ETA2 @ (B @ d["Y"])
    HY += (Q @ S @ d["Y"]).T @ A + A.T @ (Q @ S @ d["Y"])
    HZ = (Q @ d["Z"]).T @ A + A.T @ (Q @ d["Z"])
    contributions = (HB, HQ, HS, HY, HZ)
    checks = {
        "direct_uncompressed_target": np.allclose(c["h"], c["target_h"], rtol=2e-12, atol=2e-12),
        "regular": bool(c["h"][0, 0] < 0 and np.linalg.det(c["h"]) < 0),
        "all_blocks_numerically_live": all(np.linalg.norm(d[key]) > 1e-7 for key in ("B", "Q", "S", "Y", "Z")),
        "all_four_S_entries_live": bool(np.all(np.abs(d["S"]) > 1e-7)),
        "all_contributions_live": all(np.linalg.norm(H) > 1e-7 for H in contributions),
        "contribution_partition": np.allclose(d["h"], sum(contributions), rtol=3e-5, atol=3e-5),
        "ambient_metric_live": np.linalg.norm(d["g"]) > 1e-7,
        "both_screen_columns": all(np.linalg.norm(A[:, i]) > 1e-7 for i in range(2)),
        "both_base_columns": all(np.linalg.norm(U[:, i]) > 1e-7 for i in range(2)),
    }

    if kind == "flat":
        pts = (0.7, 1.0, 1.3)
        vals = [assembled(p, kind) for p in pts]
        checks["flat_M"] = max(abs(float(v["M"])) for v in vals) < 2e-12
        checks["flat_trace"] = np.ptp([float(v["trace"]) for v in vals]) < 2e-12
    elif kind == "monotone":
        pts = (0.7, 1.0, 1.3)
        vals = [assembled(p, kind) for p in pts]
        checks["monotone_M"] = bool(np.all(np.diff([float(v["M"]) for v in vals]) > 0))
        checks["flat_trace"] = np.ptp([float(v["trace"]) for v in vals]) < 2e-12
    else:
        pts = (0.51, 0.8, 1.0, 1.2, 1.49)
        vals = [assembled(p, kind) for p in pts]
        mvals = np.array([float(v["M"]) for v in vals])
        trvals = np.array([float(v["trace"]) for v in vals])
        checks["quiet_M"] = bool(mvals[2] < mvals[1] and mvals[2] < mvals[3])
        checks["loud_M_ends"] = bool(mvals[0] > mvals[1] and mvals[-1] > mvals[-2])
        checks["quiet_trace"] = bool(trvals[2] < trvals[1] and trvals[2] < trvals[3])
        checks["loud_trace_ends"] = bool(trvals[0] > trvals[1] and trvals[-1] > trvals[-2])

    # Independently verify one nonidentity chart relation at the control point.
    Rchart = np.array([[1.0, x], [0.0, 1.0]])
    Ja = np.asarray(c["J"]) @ Rchart
    checks["nonidentity_overlap"] = np.allclose(Ja.T @ np.asarray(c["g"]) @ Ja, Rchart.T @ np.asarray(c["h"]) @ Rchart)
    return checks


def main() -> None:
    checks: dict[str, bool] = {}
    for kind in ("flat", "monotone", "quiet"):
        for name, passed in family_checks(kind).items():
            checks[f"{kind}_{name}"] = bool(passed)
    result = {
        "schema": "udt.g90.all_instruments_live_independent.v1",
        "method": "independent NumPy direct assembly and centered finite-difference contribution audit",
        "checks": checks,
        "passed": all(checks.values()),
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
