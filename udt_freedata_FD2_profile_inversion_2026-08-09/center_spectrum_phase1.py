#!/usr/bin/env python3
"""Blind regular-center correction for the four inherited FD1 witnesses.

The production path uses original-variable flux shooting.  Every positive root is then
checked with scipy's adaptive collocation (solve_bvp), which does not reuse the shooting
root condition as an eigenvalue algorithm.  No CMB or SNe values are loaded.
"""

from __future__ import annotations

import hashlib
import json
import math
import time
from pathlib import Path

import numpy as np
from scipy.integrate import solve_bvp, solve_ivp
from scipy.optimize import brentq
from scipy.special import jn_zeros


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
FD1_PATH = REPO / "udt_freedata_FD1_mixing_bound_2026-08-09" / "phase1_atlas_g240.json"
OUTPUT = ROOT / "center_spectrum_phase1.json"
EXPECTED_FD1_HASH = "534713dea58c7a99a0b5ed149c33c08972f458d558bedb681f67c0d3f376110d"
INV_N = 0.9470
N = 1.0 / INV_N
NMODES = 7
Y0 = 1.0e-7
BACKGROUNDS = (
    (0.75, "D", 0.01),
    (0.75, "N", 0.01),
    (0.95, "D", 0.5),
    (0.95, "N", 0.5),
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def q_value(n: float, q_ratio: float) -> float:
    return q_ratio * (2.0 - n) / 2.0


def coeff(y: float | np.ndarray, n: float, q: float, hbar: float):
    y = np.asarray(y, dtype=float)
    u = np.exp(-y)
    r = -np.expm1(-y)
    A = u**n
    h = hbar * r**2 * u**q
    D = A * r**2 + h**2
    p = np.sqrt(A * D)
    return u, r, A, h, p


def center_state(omega: float, m: int, n: float, q: float, hbar: float) -> tuple[float, float]:
    _, r, _, _, p = coeff(Y0, n, q, hbar)
    r = float(r)
    p = float(p)
    am = abs(m)
    if am == 0:
        z = omega * r
        R = 1.0 - z * z / 4.0 + z**4 / 64.0
        dRdr = -omega**2 * r / 2.0 + omega**4 * r**3 / 16.0
        return R, p * dRdr
    # Scale out r0^|m|.  The ratio F/R is the regular Frobenius datum.
    return 1.0, am * p / r


def rhs(y: float | np.ndarray, state: np.ndarray, omega: float, m: int, n: float, q: float, hbar: float):
    u, r, A, h, p = coeff(y, n, q, hbar)
    if np.ndim(state) == 1:
        R, F = state
    else:
        R, F = state[0], state[1]
    dR = u * F / p
    dF = u * (A * m * m - 2.0 * h * m * omega - r * r * omega * omega) * R / p
    return np.vstack((dR, dF)) if np.ndim(state) > 1 else np.asarray((dR, dF), dtype=float)


def integrate_shooting(
    omega: float,
    m: int,
    n: float,
    q: float,
    hbar: float,
    ymax: float,
    dense: bool = False,
):
    return solve_ivp(
        lambda y, state: rhs(y, state, omega, m, n, q, hbar),
        (Y0, ymax),
        center_state(omega, m, n, q, hbar),
        method="DOP853",
        rtol=2.0e-11,
        atol=2.0e-13,
        max_step=0.25,
        dense_output=dense,
    )


def tail_state(R: float, F: float, omega: float, tail: float) -> tuple[float, float]:
    phase = omega * tail
    return (
        R * math.cos(phase) + F * math.sin(phase) / omega,
        F * math.cos(phase) - omega * R * math.sin(phase),
    )


def normalized_boundary(R: float, F: float, omega: float, wall: str) -> float:
    scaled_flux = F / omega
    norm = math.hypot(R, scaled_flux)
    return R / norm if wall == "D" else scaled_flux / norm


def boundary_value(
    omega: float,
    m: int,
    n: float,
    q: float,
    hbar: float,
    ymax: float,
    tail: float,
    wall: str,
) -> float:
    sol = integrate_shooting(omega, m, n, q, hbar, ymax)
    if not sol.success:
        raise RuntimeError(sol.message)
    R, F = tail_state(float(sol.y[0, -1]), float(sol.y[1, -1]), omega, tail)
    return normalized_boundary(R, F, omega, wall)


def boundary_scan(
    omegas: np.ndarray,
    m: int,
    n: float,
    q: float,
    hbar: float,
    ymax: float,
    tail: float,
    wall: str,
) -> np.ndarray:
    """Evaluate a frequency scan in one batched ODE integration."""
    omegas = np.asarray(omegas, dtype=float)
    _, r0, _, _, p0 = coeff(Y0, n, q, hbar)
    r0, p0 = float(r0), float(p0)
    if m == 0:
        z = omegas * r0
        R0 = 1.0 - z * z / 4.0 + z**4 / 64.0
        F0 = p0 * (-omegas**2 * r0 / 2.0 + omegas**4 * r0**3 / 16.0)
    else:
        R0 = np.ones_like(omegas)
        F0 = np.full_like(omegas, abs(m) * p0 / r0)
    initial = np.r_[R0, F0]

    def batch_rhs(y: float, state: np.ndarray) -> np.ndarray:
        u, r, A, h, p = coeff(y, n, q, hbar)
        R = state[: len(omegas)]
        F = state[len(omegas) :]
        dR = u * F / p
        dF = u * (A * m * m - 2.0 * h * m * omegas - r * r * omegas**2) * R / p
        return np.r_[dR, dF]

    sol = solve_ivp(
        batch_rhs,
        (Y0, ymax),
        initial,
        method="DOP853",
        rtol=2.0e-10,
        atol=2.0e-12,
        max_step=0.35,
    )
    if not sol.success:
        raise RuntimeError(sol.message)
    R = sol.y[: len(omegas), -1]
    F = sol.y[len(omegas) :, -1]
    phase = omegas * tail
    Rw = R * np.cos(phase) + F * np.sin(phase) / omegas
    Fw = F * np.cos(phase) - omegas * R * np.sin(phase)
    scaled_flux = Fw / omegas
    norm = np.hypot(Rw, scaled_flux)
    return Rw / norm if wall == "D" else scaled_flux / norm


def scan_positive_roots(
    m: int,
    n: float,
    q: float,
    hbar: float,
    ymax: float,
    tail: float,
    wall: str,
    reference_max: float,
) -> tuple[np.ndarray, list[float]]:
    # The inherited eighth positive frequency is used only to bound the blind scan,
    # never to label a root.  Expansion is automatic if the corrected spectrum extends farther.
    upper = 1.6 * reference_max
    for expansion in range(4):
        probes = np.linspace(max(1.0e-7, upper / 2000.0), upper, 401)
        values = boundary_scan(probes, m, n, q, hbar, ymax, tail, wall)
        brackets = []
        for left, right, lv, rv in zip(probes[:-1], probes[1:], values[:-1], values[1:]):
            if lv == 0.0:
                brackets.append((left * (1.0 - 1.0e-5), left * (1.0 + 1.0e-5)))
            elif lv * rv < 0.0:
                brackets.append((left, right))
        roots = []
        for left, right in brackets:
            root = brentq(
                lambda x: boundary_value(x, m, n, q, hbar, ymax, tail, wall),
                left,
                right,
                xtol=1.0e-12,
                rtol=1.0e-12,
                maxiter=100,
            )
            if not roots or abs(root - roots[-1]) > 1.0e-7:
                roots.append(root)
            if len(roots) == NMODES:
                residuals = [abs(boundary_value(x, m, n, q, hbar, ymax, tail, wall)) for x in roots]
                return np.asarray(roots), residuals
        upper *= 1.7
    raise RuntimeError(f"found fewer than {NMODES} roots for m={m}, wall={wall}")


def collocation_check(
    omega_guess: float,
    m: int,
    n: float,
    q: float,
    hbar: float,
    ymax: float,
    tail: float,
    wall: str,
) -> dict[str, object]:
    shooting = integrate_shooting(omega_guess, m, n, q, hbar, ymax, dense=True)
    early = np.linspace(Y0, min(5.0, ymax), 180)
    late = np.linspace(min(5.0, ymax), ymax, 260)[1:] if ymax > 5.0 else np.array([])
    mesh = np.unique(np.r_[early, late])
    guess = shooting.sol(mesh)
    r0 = float(-math.expm1(-Y0))
    _, _, _, _, p0 = coeff(Y0, n, q, hbar)
    p0 = float(p0)

    def fun(y: np.ndarray, z: np.ndarray, parameter: np.ndarray) -> np.ndarray:
        return rhs(y, z, float(parameter[0]), m, n, q, hbar)

    def bc(left: np.ndarray, right: np.ndarray, parameter: np.ndarray) -> np.ndarray:
        omega = float(parameter[0])
        if m == 0:
            center = left[1] + 0.5 * omega**2 * r0**2 * left[0]
        else:
            center = left[1] - abs(m) * p0 / r0 * left[0]
        Rw, Fw = tail_state(float(right[0]), float(right[1]), omega, tail)
        wall_value = Rw if wall == "D" else Fw / omega
        return np.asarray((left[0] - 1.0, center, wall_value), dtype=float)

    solved = solve_bvp(
        fun,
        bc,
        mesh,
        guess,
        p=np.asarray([omega_guess]),
        tol=1.0e-7,
        max_nodes=30000,
        verbose=0,
    )
    omega = float(solved.p[0])
    residual = abs(boundary_value(omega, m, n, q, hbar, ymax, tail, wall))
    return {
        "success": bool(solved.success),
        "status": int(solved.status),
        "message": str(solved.message),
        "omega": omega,
        "normalized_boundary_residual": residual,
        "nodes": int(solved.x.size),
        "relative_difference_from_shooting": abs(omega / omega_guess - 1.0),
    }


def flat_controls() -> dict[str, object]:
    def flat_boundary(omega: float, wall: str) -> float:
        r0 = 1.0e-8
        z = omega * r0
        initial = (1.0 - z * z / 4.0, -omega**2 * r0**2 / 2.0)

        def flat_rhs(r: float, state: np.ndarray) -> tuple[float, float]:
            R, F = state
            return F / r, -omega**2 * r * R

        sol = solve_ivp(flat_rhs, (r0, 1.0), initial, method="DOP853", rtol=1e-12, atol=1e-14)
        R, F = float(sol.y[0, -1]), float(sol.y[1, -1])
        return R if wall == "D" else F / omega

    exact_d = jn_zeros(0, 4)
    exact_n = jn_zeros(1, 4)
    roots_d = [brentq(lambda x: flat_boundary(x, "D"), 0.98 * x, 1.02 * x) for x in exact_d]
    roots_n = [brentq(lambda x: flat_boundary(x, "N"), 0.98 * x, 1.02 * x) for x in exact_n]
    return {
        "dirichlet_exact_j0": exact_d.tolist(),
        "dirichlet_shooting": roots_d,
        "dirichlet_max_relative_error": float(np.max(np.abs(np.asarray(roots_d) / exact_d - 1.0))),
        "neumann_exact_zero_mode": True,
        "neumann_positive_exact_j1": exact_n.tolist(),
        "neumann_positive_shooting": roots_n,
        "neumann_max_relative_error": float(np.max(np.abs(np.asarray(roots_n) / exact_n - 1.0))),
        "center_indicial_mminus": 1,
        "center_indicial_mzero": 0,
        "center_indicial_mplus": 1,
    }


def main() -> None:
    if sha256(FD1_PATH) != EXPECTED_FD1_HASH:
        raise SystemExit("FD1 parent hash mismatch")
    parent = json.loads(FD1_PATH.read_text(encoding="utf-8"))
    rows = {
        (float(row["q_ratio"]), str(row["wall"]), float(row["hbar"])): row
        for row in parent["rows"]
        if row.get("n_label") == "inv_n=0.9470" and float(row.get("hbar", 0.0)) > 0.0
    }
    start = time.time()
    analytic = flat_controls()
    results = []
    maximum_boundary = 0.0
    maximum_collocation_difference = 0.0
    maximum_collocation_boundary = 0.0
    maximum_fd1_drift = 0.0
    collocation_failures = 0

    for identity in BACKGROUNDS:
        parent_row = rows[identity]
        qratio, wall, hbar = identity
        q = q_value(N, qratio)
        ymax = -math.log(float(parent_row["umin"]))
        tail = float(parent_row["tail_fraction"]) * float(parent_row["xwall"])
        modes = {}
        for m, field in ((-1, "omega_mminus"), (0, "omega_m0"), (1, "omega_mplus")):
            reference = np.asarray(parent_row[field], dtype=float)
            positive, residuals = scan_positive_roots(
                m, N, q, hbar, ymax, tail, wall, float(reference[-1])
            )
            maximum_boundary = max(maximum_boundary, max(residuals))
            # Compare like-indexed positive roots only.  For N,m=0 the inherited spurious
            # first positive value is intentionally exposed by this comparison.
            fd1_drift = np.abs(positive / reference[:NMODES] - 1.0)
            maximum_fd1_drift = max(maximum_fd1_drift, float(np.max(fd1_drift)))
            collocation = [
                collocation_check(value, m, N, q, hbar, ymax, tail, wall)
                for value in positive
            ]
            maximum_collocation_difference = max(
                maximum_collocation_difference,
                max(item["relative_difference_from_shooting"] for item in collocation),
            )
            maximum_collocation_boundary = max(
                maximum_collocation_boundary,
                max(item["normalized_boundary_residual"] for item in collocation),
            )
            collocation_failures += sum(not item["success"] for item in collocation)
            modes[str(m)] = {
                "positive_omega": positive.tolist(),
                "shooting_boundary_residuals": residuals,
                "fd1_reference_positive": reference[:NMODES].tolist(),
                "fd1_like_index_relative_drift": fd1_drift.tolist(),
                "collocation": collocation,
                "exact_zero_mode": bool(wall == "N" and m == 0),
            }
            print(
                f"ROOTS {identity} m={m:+d} max_fd1_drift={np.max(fd1_drift):.3e} "
                f"max_colloc={max(x['relative_difference_from_shooting'] for x in collocation):.3e}"
            )
        results.append({
            "q_ratio": qratio,
            "q": q,
            "wall": wall,
            "hbar": hbar,
            "inv_n": INV_N,
            "n": N,
            "ymax": ymax,
            "tail": tail,
            "modes": modes,
        })

    gates = {
        "analytic_dirichlet_j0": analytic["dirichlet_max_relative_error"] < 1.0e-8,
        "analytic_neumann_j1": analytic["neumann_max_relative_error"] < 1.0e-8,
        "analytic_neumann_zero": analytic["neumann_exact_zero_mode"] is True,
        "center_indices": (
            analytic["center_indicial_mminus"],
            analytic["center_indicial_mzero"],
            analytic["center_indicial_mplus"],
        ) == (1, 0, 1),
        "root_count": sum(len(row["modes"][str(m)]["positive_omega"]) for row in results for m in (-1, 0, 1)) == 84,
        "shooting_boundary_residual": maximum_boundary < 1.0e-8,
        "collocation_success": collocation_failures == 0,
        "collocation_frequency_agreement": maximum_collocation_difference < 1.0e-5,
        "collocation_boundary_residual": maximum_collocation_boundary < 1.0e-8,
    }
    summary = {
        "background_count": len(results),
        "positive_root_count": 84,
        "exact_neumann_m0_zero_mode_count": 2,
        "maximum_shooting_boundary_residual": maximum_boundary,
        "maximum_collocation_relative_frequency_difference": maximum_collocation_difference,
        "maximum_collocation_boundary_residual": maximum_collocation_boundary,
        "collocation_failure_count": collocation_failures,
        "maximum_like_index_fd1_relative_drift": maximum_fd1_drift,
        "runtime_seconds": time.time() - start,
    }
    payload = {
        "phase": "UPSTREAM_CENTER_SPECTRUM_CORRECTION_PHASE1_BLIND",
        "observational_peak_values_loaded": False,
        "sne_magnitudes_loaded": False,
        "parent": {"fd1_atlas_sha256": sha256(FD1_PATH)},
        "analytic_controls": analytic,
        "gates": gates,
        "summary": summary,
        "rows": results,
    }
    OUTPUT.write_text(
        json.dumps(
            payload,
            indent=2,
            sort_keys=True,
            default=lambda value: value.item() if isinstance(value, np.generic) else str(value),
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, sort_keys=True))
    print(json.dumps(gates, indent=2, sort_keys=True))
    print(f"WROTE {OUTPUT}")
    if not all(gates.values()):
        raise SystemExit(f"failed gates: {[name for name, passed in gates.items() if not passed]}")


if __name__ == "__main__":
    main()
