#!/usr/bin/env python3
"""Independent numerical and structural verification of the blind corrected atlas."""

from __future__ import annotations

import copy
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.special import jn_zeros, jnp_zeros


ROOT = Path(__file__).resolve().parent
ATLAS = ROOT / "corrected_full_atlas_certified.json"
STRICT = ROOT / "corrected_full_atlas_strict.json"
EXPECTED_ATLAS = "042138fb73cc9f3bef4faf97fc0357f2a2f079daced5e39d6532c4a6f770dfbb"
EXPECTED_STRICT = "46e8aeda120f6c51fbfc000cf56e5db5a78fe2092ae12b06b20523bc468ec1d5"
INV_N = (0.9658, 0.9470, 0.9284)
Q_RATIOS = (-2.0, -1.0, 0.0, 0.25, 0.50, 0.75, 0.95)
HBAR_CHECK = (0.001, 0.05, 1.0)
KEYS: dict[str, bool] = {}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def key(name: str, value: bool) -> None:
    KEYS[name] = bool(value)
    print(f"KEY {name}: {KEYS[name]}")


def endpoint_power(z: float, exponent: float, compact: float) -> float:
    power = exponent / compact - 1.0
    if abs(power) < 2.0e-13:
        return 1.0
    return 0.0 if z <= 0.0 else z**power


def independent_endpoint(
    frequency: float,
    angular: int,
    n: float,
    q: float,
    hbar: float,
    *,
    split: float = 1.0,
    center: float = 1.0e-7,
) -> tuple[float, float]:
    """Separately coded two-chart flux propagation at tighter tolerances."""
    y0 = -math.log1p(-center)
    k2 = frequency**2 + 2.0 * hbar * angular * frequency
    u0, r0 = math.exp(-y0), -math.expm1(-y0)
    A0, h0 = u0**n, hbar * r0 * r0 * u0**q
    p0 = math.sqrt(A0 * (A0 * r0 * r0 + h0 * h0))
    if angular == 0:
        initial_R = 1.0 - k2 * center**2 / 4.0 + k2**2 * center**4 / 64.0
        initial_F = p0 * (-k2 * center / 2.0 + k2**2 * center**3 / 16.0)
    else:
        initial_R = 1.0 - k2 * center**2 / 8.0 + k2**2 * center**4 / 192.0
        initial_F = (p0 / center) * (
            1.0 - 3.0 * k2 * center**2 / 8.0 + 5.0 * k2**2 * center**4 / 192.0
        )

    def body_rhs(y: float, state: np.ndarray) -> np.ndarray:
        u, r = math.exp(-y), -math.expm1(-y)
        A, h = u**n, hbar * r * r * u**q
        p = math.sqrt(A * (A * r * r + h * h))
        R, F = state
        return np.asarray((u * F / p, u * (A * angular**2 - 2.0 * h * angular * frequency - r**2 * frequency**2) * R / p))

    body = solve_ivp(
        body_rhs, (y0, split), (initial_R, initial_F), method="DOP853",
        rtol=2.0e-12, atol=2.0e-14, max_step=0.055,
    )
    if not body.success:
        raise RuntimeError(body.message)
    sigma = 0.5 * (n + 2.0 * q)
    aa, bb, gg = 1.0 - sigma, 1.0 - n / 2.0, 1.0 + n - sigma
    compact = min(aa, bb)
    z0 = math.exp(-compact * split)

    def tail_rhs(z: float, state: np.ndarray) -> np.ndarray:
        u = 0.0 if z <= 0.0 else z ** (1.0 / compact)
        r = 1.0 - u
        ratio = 0.0 if z <= 0.0 else z ** ((n - 2.0 * q) / compact) / (hbar**2 * r**2)
        norm = math.sqrt(1.0 + ratio)
        ca, cb, cg = (endpoint_power(z, exponent, compact) for exponent in (aa, bb, gg))
        R, F = state
        dR = -ca * F / (compact * hbar * r**2 * norm)
        dF = (
            -angular**2 * cg / (compact * hbar * r**2 * norm)
            + 2.0 * angular * frequency * cb / (compact * norm)
            + frequency**2 * ca / (compact * hbar * norm)
        ) * R
        return np.asarray((dR, dF))

    tail = solve_ivp(
        tail_rhs, (z0, 0.0), body.y[:, -1], method="DOP853",
        rtol=2.0e-12, atol=2.0e-14, max_step=min(0.017, z0 / 28.0),
    )
    if not tail.success:
        raise RuntimeError(tail.message)
    return float(tail.y[0, -1]), float(tail.y[1, -1])


def independent_root(
    saved: float, step: float, angular: int, row: dict[str, object], *, split: float = 1.0, center: float = 1.0e-7
) -> tuple[float, float]:
    wall = str(row["wall"])

    def value(frequency: float) -> float:
        R, F = independent_endpoint(
            frequency, angular, float(row["n"]), float(row["q"]), float(row["hbar"]),
            split=split, center=center,
        )
        scale = math.hypot(R, F)
        return (R if wall == "D" else F) / scale

    left, right = max(1.0e-14, saved - 0.75 * step), saved + 0.75 * step
    if value(left) * value(right) >= 0.0:
        raise RuntimeError("independent local bracket failure")
    root = brentq(value, left, right, xtol=1.0e-18, rtol=1.0e-14, maxiter=200)
    return float(root), abs(value(root))


def flat_endpoint(frequency: float, angular: int) -> tuple[float, float]:
    radius = 1.0e-7
    k2 = frequency**2
    if angular == 0:
        R0 = 1.0 - k2 * radius**2 / 4.0 + k2**2 * radius**4 / 64.0
        V0 = -k2 * radius / 2.0 + k2**2 * radius**3 / 16.0
    else:
        R0 = 1.0 - k2 * radius**2 / 8.0 + k2**2 * radius**4 / 192.0
        V0 = (1.0 / radius) * (
            1.0 - 3.0 * k2 * radius**2 / 8.0 + 5.0 * k2**2 * radius**4 / 192.0
        )

    def rhs(r: float, state: np.ndarray) -> np.ndarray:
        R, V = state
        return np.asarray((V, -V / r - (frequency**2 - angular**2 / r**2) * R))

    solve = solve_ivp(rhs, (radius, 1.0), (R0, V0), method="DOP853", rtol=2.0e-12, atol=2.0e-14)
    if not solve.success:
        raise RuntimeError(solve.message)
    return float(solve.y[0, -1]), float(solve.y[1, -1])


def flat_controls() -> float:
    errors: list[float] = []
    analytic = {
        (0, "D"): jn_zeros(0, 8),
        (0, "N"): jn_zeros(1, 8),
        (1, "D"): jn_zeros(1, 8),
        (1, "N"): jnp_zeros(1, 8),
    }
    for (angular, wall), exact in analytic.items():
        for target in exact:
            def value(frequency: float) -> float:
                R, V = flat_endpoint(frequency, angular)
                return R if wall == "D" else V
            root = brentq(value, target - 0.18, target + 0.18, xtol=1.0e-13, rtol=1.0e-13)
            errors.append(abs(root / target - 1.0))
    return max(errors)


def identity(row: dict[str, object]) -> tuple[object, ...]:
    return (float(row["inv_n"]), float(row["q_ratio"]), float(row["hbar"]), str(row["wall"]))


def structural_errors(payload: dict[str, object]) -> list[str]:
    errors: list[str] = []
    rows = payload.get("rows", [])
    identities = [identity(row) for row in rows]
    if len(rows) != 462 or len(set(identities)) != 462:
        errors.append("row census")
    spectral = [row for row in rows if float(row["hbar"]) > 0.0]
    if len(spectral) != 420 or len(rows) - len(spectral) != 42:
        errors.append("spectral/control census")
    for row in spectral:
        for name in ("omega_mminus", "omega_m0", "omega_mplus"):
            values = np.asarray(row.get(name, []), dtype=float)
            if len(values) != 8 or not np.all(values > 0.0) or not np.all(np.diff(values) > 0.0):
                errors.append(f"root order {identity(row)} {name}")
        if row["wall"] == "N" and row.get("neumann_m0_exact_zero_mode") is not True:
            errors.append("Neumann zero mode")
        if max(row["max_normalized_wall_residual"].values()) >= 2.0e-8:
            errors.append("stored residual")
        if float(row["q_ratio"]) == 0.0:
            minus, plus = np.asarray(row["omega_mminus"]), np.asarray(row["omega_mplus"])
            if np.max(np.abs(np.abs(plus - minus) - 2.0 * float(row["hbar"]))) >= 2.0e-8:
                errors.append("q0 split")
    if payload.get("observational_peak_or_trough_values_loaded") is not False:
        errors.append("blindness flag")
    if int(payload.get("summary", {}).get("corrected_positive_root_count", -1)) != 10080:
        errors.append("positive-root count")
    return errors


def main() -> None:
    key("CFA_V1_certified_hash", digest(ATLAS) == EXPECTED_ATLAS)
    key("CFA_V2_strict_parent_hash", digest(STRICT) == EXPECTED_STRICT)
    payload = json.loads(ATLAS.read_text())
    strict = json.loads(STRICT.read_text())
    base_errors = structural_errors(payload)
    key("CFA_V3_structural_census", not base_errors)
    max_bessel_error = flat_controls()
    key("CFA_V4_flat_bessel_controls", max_bessel_error < 2.0e-9)

    atlas_rows = {identity(row): row for row in payload["rows"]}
    independent_drift: list[float] = []
    independent_residual: list[float] = []
    split_drift: list[float] = []
    center_drift: list[float] = []
    subset: list[dict[str, object]] = []
    fields = {-1: "omega_mminus", 0: "omega_m0", 1: "omega_mplus"}
    for i in range(21):
        inv_n = INV_N[i % 3]
        ratio = Q_RATIOS[i % 7]
        hbar = HBAR_CHECK[i // 7]
        wall = ("D", "N")[i % 2]
        angular = (-1, 0, 1)[i % 3]
        row = atlas_rows[(inv_n, ratio, hbar, wall)]
        step = float(row["scan"][str(angular)]["scan_step"])
        for radial in (0, 3, 7):
            saved = float(row[fields[angular]][radial])
            baseline, residual = independent_root(saved, step, angular, row)
            alternatives = [
                independent_root(saved, step, angular, row, split=0.7)[0],
                independent_root(saved, step, angular, row, split=1.4)[0],
            ]
            centers = [
                independent_root(saved, step, angular, row, center=1.0e-6)[0],
                independent_root(saved, step, angular, row, center=1.0e-8)[0],
            ]
            independent_drift.append(abs(baseline / saved - 1.0))
            independent_residual.append(residual)
            split_drift.extend(abs(value / baseline - 1.0) for value in alternatives)
            center_drift.extend(abs(value / baseline - 1.0) for value in centers)
            subset.append(
                {
                    "i": i,
                    "inv_n": inv_n,
                    "q_ratio": ratio,
                    "hbar": hbar,
                    "wall": wall,
                    "m": angular,
                    "radial_index": radial,
                    "saved": saved,
                    "independent": baseline,
                    "normalized_residual": residual,
                }
            )
    key("CFA_V5_independent_63_roots", max(independent_drift) < 2.0e-7)
    key("CFA_V6_independent_residuals", max(independent_residual) < 2.0e-7)
    key("CFA_V7_split_robustness", max(split_drift) < 2.0e-8)
    key("CFA_V8_center_robustness", max(center_drift) < 2.0e-8)

    strict_rows = {identity(row): row for row in strict["rows"]}
    changed_roots: list[tuple[object, ...]] = []
    for row_id, row in atlas_rows.items():
        old = strict_rows[row_id]
        for angular, field in fields.items():
            for radial, (before, after) in enumerate(zip(old.get(field, []), row.get(field, []))):
                if before != after:
                    changed_roots.append((*row_id, angular, radial))
    target_prefix = (0.9284, 0.95, 0.001, "D")
    key(
        "CFA_V9_only_preregistered_roots_changed",
        0 < len(changed_roots) <= 24 and all(item[:4] == target_prefix for item in changed_roots),
    )

    mutations: list[tuple[str, dict[str, object]]] = []
    missing = copy.deepcopy(payload); missing["rows"].pop(); mutations.append(("missing", missing))
    duplicate = copy.deepcopy(payload); duplicate["rows"][-1] = copy.deepcopy(duplicate["rows"][0]); mutations.append(("duplicate", duplicate))
    root_bad = copy.deepcopy(payload); next(r for r in root_bad["rows"] if r["hbar"])["omega_m0"][0] = -1.0; mutations.append(("root", root_bad))
    zero_bad = copy.deepcopy(payload); next(r for r in zero_bad["rows"] if r.get("neumann_m0_exact_zero_mode"))["neumann_m0_exact_zero_mode"] = False; mutations.append(("zero", zero_bad))
    q0_bad = copy.deepcopy(payload); qrow = next(r for r in q0_bad["rows"] if r["hbar"] and r["q_ratio"] == 0.0); qrow["omega_mplus"][0] += 0.1; mutations.append(("q0", q0_bad))
    count_bad = copy.deepcopy(payload); count_bad["summary"]["corrected_positive_root_count"] = 5040; mutations.append(("count", count_bad))
    blind_bad = copy.deepcopy(payload); blind_bad["observational_peak_or_trough_values_loaded"] = True; mutations.append(("blind", blind_bad))
    caught = {name: bool(structural_errors(mutated)) for name, mutated in mutations}
    key("CFA_V10_all_mutation_catches", all(caught.values()) and len(caught) == 7)

    result = {
        "keys": KEYS,
        "summary": {
            "flat_bessel_max_relative_error": max_bessel_error,
            "independent_roots": len(subset),
            "independent_max_relative_frequency_drift": max(independent_drift),
            "independent_max_normalized_residual": max(independent_residual),
            "split_max_relative_drift": max(split_drift),
            "center_max_relative_drift": max(center_drift),
            "strict_to_certified_changed_root_values": len(changed_roots),
            "mutation_catches": caught,
            "structural_errors": base_errors,
        },
        "independent_subset": subset,
    }
    output = ROOT / "verification_result.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result["summary"], sort_keys=True))
    print(f"WROTE {output} SHA256 {digest(output)}")
    if not all(KEYS.values()):
        raise SystemExit("independent verification failed")


if __name__ == "__main__":
    main()
