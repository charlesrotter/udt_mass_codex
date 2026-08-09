#!/usr/bin/env python3
"""FD2 Phase-I continuum shooting and variational profile response.

No Planck peak/trough values and no SNe magnitudes are loaded here.  This is the
preregistered refinement after the low-order FEM derivative convergence failure.
"""

from __future__ import annotations

import hashlib
import json
import math
import time
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

import derive_phase1 as fem


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
FD1 = REPO / "udt_freedata_FD1_mixing_bound_2026-08-09" / "phase1_atlas_g240.json"
OUTPUT = ROOT / "phase1_response_continuum.json"
Y0 = 1.0e-8
QUADRATURE_SIZES = (8001, 16001)
DIRECT_DELTA = 0.01
EXPECTED_FD1_HASH = "534713dea58c7a99a0b5ed149c33c08972f458d558bedb681f67c0d3f376110d"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def background_key(background: dict[str, object]) -> tuple[float, str, float]:
    return float(background["q_ratio"]), str(background["wall"]), float(background["hbar"])


def coefficients(
    y: float | np.ndarray,
    n: float,
    q: float,
    hbar: float,
    motif: tuple[str, float, float] | None = None,
    coefficient: float = 0.0,
) -> tuple[np.ndarray, ...]:
    y = np.asarray(y, dtype=float)
    u = np.exp(-y)
    r = -np.expm1(-y)
    b = np.zeros_like(r)
    if motif is not None and coefficient != 0.0:
        kind, center, halfwidth = motif
        b = fem.motif_value(r, kind, center, halfwidth)
    A = np.exp(n * np.log(u) + coefficient * b)
    h = hbar * r**2 * u**q
    D = A * r**2 + h**2
    p = np.sqrt(A * D)
    w = r**2 / p
    return u, r, A, h, D, p, w


def tail_propagate(R: float, F: float, omega: float, tail: float) -> tuple[float, float]:
    phase = omega * tail
    cosine = math.cos(phase)
    sine = math.sin(phase)
    return (
        R * cosine + (F / omega) * sine,
        F * cosine - omega * R * sine,
    )


def integrate(
    omega: float,
    n: float,
    q: float,
    hbar: float,
    ymax: float,
    motif: tuple[str, float, float] | None = None,
    coefficient: float = 0.0,
    dense: bool = False,
):
    r0 = -math.expm1(-Y0)
    _, _, _, _, _, p0, _ = coefficients(Y0, n, q, hbar, motif, coefficient)
    z = omega * r0
    R0 = 1.0 - z * z / 4.0 + z**4 / 64.0
    dRdr0 = -omega * omega * r0 / 2.0 + omega**4 * r0**3 / 16.0
    F0 = float(p0) * dRdr0

    def rhs(y: float, state: np.ndarray) -> tuple[float, float]:
        u, _, _, _, _, p, w = coefficients(y, n, q, hbar, motif, coefficient)
        R, F = state
        return float(u * F / p), float(-u * omega * omega * w * R)

    return solve_ivp(
        rhs,
        (Y0, ymax),
        (R0, F0),
        method="DOP853",
        rtol=1.0e-11,
        atol=1.0e-13,
        dense_output=dense,
        max_step=0.10,
    )


def boundary_value(
    omega: float,
    n: float,
    q: float,
    hbar: float,
    ymax: float,
    tail: float,
    wall: str,
    motif: tuple[str, float, float] | None = None,
    coefficient: float = 0.0,
) -> float:
    sol = integrate(omega, n, q, hbar, ymax, motif, coefficient, dense=False)
    if not sol.success:
        raise RuntimeError(sol.message)
    Rw, Fw = tail_propagate(float(sol.y[0, -1]), float(sol.y[1, -1]), omega, tail)
    return Rw if wall == "D" else Fw / omega


def find_roots(
    references: np.ndarray,
    n: float,
    q: float,
    hbar: float,
    ymax: float,
    tail: float,
    wall: str,
    motif: tuple[str, float, float] | None = None,
    coefficient: float = 0.0,
) -> tuple[np.ndarray, list[float]]:
    references = np.asarray(references, dtype=float)
    roots = []
    residuals = []
    for index in range(fem.NMODES):
        center = references[index]
        lower = 0.5 * center if index == 0 else 0.5 * (references[index - 1] + center)
        upper = (
            0.5 * (center + references[index + 1])
            if index + 1 < len(references)
            else center + 0.5 * (center - references[index - 1])
        )
        f = lambda omega: boundary_value(
            omega, n, q, hbar, ymax, tail, wall, motif, coefficient
        )
        fl, fu = f(lower), f(upper)
        if fl * fu > 0.0:
            # Deterministic local scan retained only as a bracketing fallback.
            trial = np.linspace(max(1.0e-10, 0.7 * center), 1.3 * center, 81)
            values = [f(value) for value in trial]
            bracket = None
            for left, right, lv, rv in zip(trial[:-1], trial[1:], values[:-1], values[1:]):
                if lv == 0.0 or lv * rv < 0.0:
                    bracket = (left, right)
                    break
            if bracket is None:
                raise RuntimeError(f"could not bracket mode {index} near {center}")
            lower, upper = bracket
        root = brentq(f, lower, upper, xtol=1.0e-13, rtol=1.0e-13, maxiter=100)
        roots.append(root)
        residuals.append(abs(f(root)))
    return np.asarray(roots), residuals


def tail_norm(R: float, F: float, omega: float, tail: float) -> float:
    phase = omega * tail
    a = R
    b = F / omega
    return (
        a * a * (tail / 2.0 + math.sin(2.0 * phase) / (4.0 * omega))
        + b * b * (tail / 2.0 - math.sin(2.0 * phase) / (4.0 * omega))
        + a * b * math.sin(phase) ** 2 / omega
    )


def mode_kernel(
    omega: float,
    n: float,
    q: float,
    hbar: float,
    ymax: float,
    tail: float,
    points: int,
) -> tuple[np.ndarray, np.ndarray, float]:
    sol = integrate(omega, n, q, hbar, ymax, dense=True)
    if not sol.success or sol.sol is None:
        raise RuntimeError(sol.message)
    y = np.linspace(Y0, ymax, points)
    R, F = sol.sol(y)
    u, r, A, _, D, p, w = coefficients(y, n, q, hbar)
    body_norm = float(np.trapezoid(u * w * R**2, y))
    norm = body_norm + tail_norm(float(R[-1]), float(F[-1]), omega, tail)
    profile_factor = 0.5 * (1.0 + A * r**2 / D)
    energy = u * (F**2 / p + omega**2 * w * R**2)
    kernel = energy * profile_factor / (2.0 * omega * norm)
    return y, r, kernel


def motif_response(
    r: np.ndarray,
    y: np.ndarray,
    kernels: list[np.ndarray],
    kind: str,
    center: float,
    halfwidth: float,
) -> np.ndarray:
    b = fem.motif_value(r, kind, center, halfwidth)
    return np.asarray([float(np.trapezoid(kernel * b, y)) for kernel in kernels])


def direct_check_identities() -> set[tuple[str, float, float]]:
    selected = set()
    for kind in fem.MOTIF_CLASSES:
        motifs = sorted((fem.motif_id(kind, c, w), c, w) for w, c in fem.SUPPORTS)
        for _, center, halfwidth in (motifs[0], motifs[-1]):
            selected.add((kind, center, halfwidth))
    return selected


def main() -> None:
    if sha256(FD1) != EXPECTED_FD1_HASH:
        raise SystemExit("FD1 atlas hash mismatch")
    parent = json.loads(FD1.read_text(encoding="utf-8"))
    parent_rows = {}
    for row in parent["rows"]:
        if row.get("n_label") == "inv_n=0.9470" and float(row.get("hbar", 0.0)) > 0.0:
            parent_rows[(float(row["q_ratio"]), str(row["wall"]), float(row["hbar"]))] = row

    start = time.time()
    baseline = {}
    max_boundary_residual = 0.0
    max_fd1_drift = 0.0
    for background in fem.BACKGROUNDS:
        key = background_key(background)
        row = parent_rows[key]
        n = fem.N
        q = fem.q_value(n, key[0])
        ymax = -math.log(float(row["umin"]))
        tail = float(row["tail_fraction"]) * float(row["xwall"])
        references = np.asarray(row["omega_m0"][: fem.NMODES + 1], dtype=float)
        omega, residuals = find_roots(references, n, q, key[2], ymax, tail, key[1])
        max_boundary_residual = max(max_boundary_residual, max(residuals))
        max_fd1_drift = max(max_fd1_drift, float(np.max(np.abs(omega / references[: fem.NMODES] - 1.0))))
        baseline[key] = {
            "omega": omega,
            "boundary_residuals": residuals,
            "ymax": ymax,
            "tail": tail,
            "q": q,
        }
        print(f"BASELINE {key} drift={np.max(np.abs(omega/references[:fem.NMODES]-1)):.3e}")

    rows = []
    direct_selected = direct_check_identities()
    direct_checks = []
    for background in fem.BACKGROUNDS:
        key = background_key(background)
        base = baseline[key]
        kernels_by_size = {}
        r_by_size = {}
        y_by_size = {}
        for points in QUADRATURE_SIZES:
            mode_data = [
                mode_kernel(
                    float(omega), fem.N, float(base["q"]), key[2],
                    float(base["ymax"]), float(base["tail"]), points
                )
                for omega in np.asarray(base["omega"])
            ]
            y_by_size[points] = mode_data[0][0]
            r_by_size[points] = mode_data[0][1]
            kernels_by_size[points] = [item[2] for item in mode_data]

        for halfwidth, center in fem.SUPPORTS:
            for kind in fem.MOTIF_CLASSES:
                response = {}
                for points in QUADRATURE_SIZES:
                    response[points] = motif_response(
                        r_by_size[points], y_by_size[points], kernels_by_size[points],
                        kind, center, halfwidth
                    )
                coarse = response[QUADRATURE_SIZES[0]]
                fine = response[QUADRATURE_SIZES[1]]
                norm = float(np.linalg.norm(fine))
                absolute_drift = float(np.linalg.norm(fine - coarse))
                relative_drift = absolute_drift / max(norm, 1.0e-14)
                resolved = absolute_drift < 1.0e-10 if norm < 1.0e-10 else relative_drift < 0.02
                record = {
                    "identity": fem.motif_id(kind, center, halfwidth),
                    "motif_class": kind,
                    "center": center,
                    "halfwidth": halfwidth,
                    "q_ratio": key[0],
                    "q": float(base["q"]),
                    "wall": key[1],
                    "hbar": key[2],
                    "inv_n": fem.INV_N,
                    "n": fem.N,
                    "omega0": np.asarray(base["omega"]).tolist(),
                    "response_8001": coarse.tolist(),
                    "response_16001": fine.tolist(),
                    "response_norm": norm,
                    "quadrature_absolute_norm_drift": absolute_drift,
                    "quadrature_relative_norm_drift": relative_drift,
                    "numerically_resolved": bool(resolved),
                }
                rows.append(record)

                if (kind, center, halfwidth) in direct_selected:
                    motif = (kind, center, halfwidth)
                    direct = []
                    for coefficient in (DIRECT_DELTA, -DIRECT_DELTA):
                        roots, residuals = find_roots(
                            np.r_[np.asarray(base["omega"]), np.asarray(base["omega"])[-1] * 1.2],
                            fem.N,
                            float(base["q"]),
                            key[2],
                            float(base["ymax"]),
                            float(base["tail"]),
                            key[1],
                            motif,
                            coefficient,
                        )
                        direct.append(roots)
                        max_boundary_residual = max(max_boundary_residual, max(residuals))
                    direct_response = (direct[0] - direct[1]) / (2.0 * DIRECT_DELTA)
                    disagreement = float(np.linalg.norm(direct_response - fine))
                    relative = disagreement / max(norm, 1.0e-14)
                    direct_checks.append({
                        "identity": [record["identity"], key[0], key[1], key[2]],
                        "variational_response": fine.tolist(),
                        "direct_response": direct_response.tolist(),
                        "absolute_norm_disagreement": disagreement,
                        "relative_norm_disagreement": relative,
                        "passed": bool(disagreement < 1.0e-8 if norm < 1.0e-8 else relative < 0.02),
                    })

    unique = {(row["identity"], row["q_ratio"], row["wall"], row["hbar"]) for row in rows}
    gates = {
        "baseline_root_count": sum(len(item["omega"]) for item in baseline.values()) == 28,
        "baseline_positive_ordered": all(
            np.all(np.asarray(item["omega"]) > 0.0) and np.all(np.diff(np.asarray(item["omega"])) > 0.0)
            for item in baseline.values()
        ),
        "boundary_residual": max_boundary_residual < 1.0e-8,
        "fd1_frequency_drift": max_fd1_drift < 0.01,
        "row_count": len(rows) == len(unique) == 320,
        "quadrature_response": all(row["numerically_resolved"] for row in rows),
        "direct_check_count": len(direct_checks) == 16,
        "direct_nonlinear_checks": all(row["passed"] for row in direct_checks),
    }
    summary = {
        "baseline_root_count": 28,
        "row_count": len(rows),
        "maximum_boundary_residual": max_boundary_residual,
        "maximum_fd1_frequency_relative_drift": max_fd1_drift,
        "maximum_quadrature_relative_response_drift": max(row["quadrature_relative_norm_drift"] for row in rows),
        "maximum_quadrature_absolute_response_drift": max(row["quadrature_absolute_norm_drift"] for row in rows),
        "unresolved_response_rows": sum(not row["numerically_resolved"] for row in rows),
        "maximum_direct_relative_response_disagreement": max(row["relative_norm_disagreement"] for row in direct_checks),
        "failed_direct_checks": sum(not row["passed"] for row in direct_checks),
        "runtime_seconds": time.time() - start,
    }
    payload = {
        "phase": "FD2_PHASE1_CONTINUUM_VARIATIONAL_RESPONSE",
        "observational_peak_values_loaded": False,
        "sne_magnitudes_loaded": False,
        "parent": {"fd1_atlas_sha256": sha256(FD1)},
        "config": {
            "quadrature_sizes": QUADRATURE_SIZES,
            "direct_delta": DIRECT_DELTA,
            "ode_method": "DOP853",
            "rtol": 1.0e-11,
            "atol": 1.0e-13,
        },
        "gates": gates,
        "summary": summary,
        "baselines": {str(key): {**value, "omega": np.asarray(value["omega"]).tolist()} for key, value in baseline.items()},
        "direct_checks": direct_checks,
        "rows": rows,
    }
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    print(json.dumps(gates, indent=2, sort_keys=True))
    print(f"WROTE {OUTPUT}")
    if not all(gates.values()):
        raise SystemExit(f"failed gates: {[name for name, passed in gates.items() if not passed]}")


if __name__ == "__main__":
    main()
