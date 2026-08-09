#!/usr/bin/env python3
"""Independent FD1 Phase-I audit.

This verifier does not import derive_phase1.py.  It checks the saved atlases, then
rebuilds selected operators using solve_ivp for the metric coordinate and solves
the quadratic pencil as scalar nonlinear symmetric eigenvalue problems rather
than using the production companion linearization.
"""

from __future__ import annotations

import copy
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy import linalg as sla
from scipy.integrate import solve_ivp
from scipy.optimize import brentq


ROOT = Path(__file__).resolve().parent
PRIMARY = ROOT / "phase1_atlas_g240.json"
COARSE = ROOT / "phase1_atlas_g180.json"
FAILED = ROOT / "phase1_atlas_failed_tail_g240.json"
OUT = ROOT / "phase1_verification.json"
NMODES = 8
HBARS = (0.0, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0)
ASYMPTOTIC_RATIO_MAX = 1.0e-6
KEYS: dict[str, bool] = {}


def key(name: str, condition: bool) -> None:
    KEYS[name] = bool(condition)
    print(f"KEY {name}: {KEYS[name]}")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def identity(row: dict[str, object]) -> tuple[object, ...]:
    return row["n_label"], row["q_ratio"], row["wall"], row["hbar"]


def atlas_errors(payload: dict[str, object]) -> list[str]:
    errors: list[str] = []
    rows = payload.get("rows", [])
    if payload.get("phase") != "PHASE1_BLIND_GEOMETRY":
        errors.append("wrong phase")
    if payload.get("observational_width_values_loaded") is not False:
        errors.append("observational data disclosure")
    if payload.get("production_complete") is not True:
        errors.append("partial run")
    if len(rows) != 462:
        errors.append("row count")
    ids = [identity(row) for row in rows]
    if len(set(ids)) != len(ids):
        errors.append("duplicate identity")
    if not all(payload.get("keys", {}).values()):
        errors.append("failed internal key")
    for row in rows:
        hbar = float(row["hbar"])
        if hbar == 0.0:
            if any(name in row for name in ("omega_mminus", "omega_m0", "omega_mplus")):
                errors.append("mu-off spectrum claimed")
            continue
        for name in ("omega_mminus", "omega_m0", "omega_mplus", "eta_split", "full_displacement"):
            if name not in row or len(row[name]) != NMODES:
                errors.append(f"missing {name}")
                continue
            values = np.asarray(row[name], dtype=float)
            if not np.all(np.isfinite(values)):
                errors.append(f"nonfinite {name}")
            if name.startswith("omega_") and not np.all(np.diff(values) > 0.0):
                errors.append(f"unordered {name}")
        if float(row["q_ratio"]) == 0.0 and all(name in row for name in ("omega_mminus", "omega_mplus")):
            split_error = np.max(
                np.abs(np.abs(np.asarray(row["omega_mplus"]) - np.asarray(row["omega_mminus"])) - 2.0 * hbar)
            )
            if split_error >= 2.0e-6:
                errors.append("q0 exact split")
    return errors


def family_umin(n: float, q: float) -> float:
    exponent = n - 2.0 * q
    candidates = []
    for hbar in HBARS[1:]:
        log_target = (
            2.0 * math.log(hbar) / exponent
            + math.log(ASYMPTOTIC_RATIO_MAX) / exponent
        )
        candidates.append(min(1.0e-6, math.exp(max(log_target, math.log(1.0e-300)))))
    return max(1.0e-120, min(candidates))


def alternate_geometry(n: float, q: float, hbar: float, umin: float, size: int) -> dict[str, np.ndarray | float]:
    sigma = 0.5 * (n + 2.0 * q)
    smax = -math.log(umin)

    def rate(s: float) -> float:
        if abs(s) < 1.0e-14:
            return 1.0
        u = math.exp(-s)
        r = -math.expm1(-s)
        A = u**n
        h = hbar * r * r * u**q
        return r * u / math.sqrt(A * (A * r * r + h * h))

    solution = solve_ivp(
        lambda s, _: [rate(float(s))],
        (0.0, smax),
        [0.0],
        rtol=2.0e-10,
        atol=2.0e-12,
        max_step=max(0.01, smax / 8000.0),
        dense_output=True,
    )
    if not solution.success:
        raise RuntimeError(solution.message)
    body = float(solution.y[0, -1])
    tail = umin ** (1.0 - sigma) / (hbar * (1.0 - sigma))
    xwall = body + tail
    xnodes = np.linspace(0.0, xwall, size)
    xmid = 0.5 * (xnodes[:-1] + xnodes[1:])
    sprobe = np.linspace(0.0, smax, max(12000, int(80.0 * smax)))
    xprobe = solution.sol(sprobe)[0]
    smid = np.empty_like(xmid)
    body_mask = xmid <= body
    smid[body_mask] = np.interp(xmid[body_mask], xprobe, sprobe)
    remainder = xwall - xmid[~body_mask]
    utail = (hbar * (1.0 - sigma) * remainder) ** (1.0 / (1.0 - sigma))
    smid[~body_mask] = -np.log(utail)
    u = np.exp(-smid)
    r = -np.expm1(-smid)
    A = u**n
    h = hbar * r * r * u**q
    D = A * r * r + h * h
    connection = np.sqrt(A * D) / (2.0 * r * r)
    return {"xnodes": xnodes, "r": r, "A": A, "h": h, "connection": connection, "xwall": xwall}


def alternate_matrices(geometry: dict[str, np.ndarray | float], m: int, wall: str) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    xnodes = np.asarray(geometry["xnodes"])
    r = np.asarray(geometry["r"])
    A = np.asarray(geometry["A"])
    h = np.asarray(geometry["h"])
    connection = np.asarray(geometry["connection"])
    count = len(xnodes)
    K = np.zeros((count, count))
    M = np.zeros((count, count))
    C = np.zeros((count, count))
    mass_template = np.array([[2.0, 1.0], [1.0, 2.0]]) / 6.0
    stiffness_template = np.array([[1.0, -1.0], [-1.0, 1.0]])
    for i, dx in enumerate(np.diff(xnodes)):
        mass = dx * mass_template
        a = connection[i]
        covariant = stiffness_template / dx + np.array([[a, 0.0], [0.0, -a]]) + a * a * mass
        potential = (m * m) * A[i] / (r[i] * r[i])
        drag = 2.0 * m * h[i] / (r[i] * r[i])
        K[i:i + 2, i:i + 2] += covariant + potential * mass
        M[i:i + 2, i:i + 2] += mass
        C[i:i + 2, i:i + 2] += drag * mass
    keep = np.ones(count, dtype=bool)
    keep[0] = False
    if wall == "D":
        keep[-1] = False
    indices = np.flatnonzero(keep)
    return K[np.ix_(indices, indices)], M[np.ix_(indices, indices)], C[np.ix_(indices, indices)]


def nonlinear_frequency(K: np.ndarray, M: np.ndarray, C: np.ndarray, m: int, mode: int, reference: float) -> tuple[float, float]:
    if m == 0:
        value, vector = sla.eigh(K, M, subset_by_index=[mode, mode], check_finite=False)
        omega = math.sqrt(float(value[0]))
        vec = vector[:, 0]
    else:
        def branch(omega: float) -> float:
            value = sla.eigvalsh(K - omega * C, M, subset_by_index=[mode, mode], check_finite=False)[0]
            return float(value - omega * omega)

        upper = max(1.0, 2.0 * reference)
        while branch(upper) > 0.0 and upper < 1.0e6 * max(1.0, reference):
            upper *= 2.0
        omega = brentq(branch, 0.0, upper, xtol=2.0e-11, rtol=2.0e-11, maxiter=100)
        _, vector = sla.eigh(K - omega * C, M, subset_by_index=[mode, mode], check_finite=False)
        vec = vector[:, 0]
    raw = K @ vec - omega * C @ vec - omega * omega * M @ vec
    denominator = (
        np.linalg.norm(K @ vec)
        + abs(omega) * np.linalg.norm(C @ vec)
        + omega * omega * np.linalg.norm(M @ vec)
    )
    return omega, float(np.linalg.norm(raw) / denominator)


def main() -> None:
    primary = json.loads(PRIMARY.read_text(encoding="utf-8"))
    coarse = json.loads(COARSE.read_text(encoding="utf-8"))
    failed = json.loads(FAILED.read_text(encoding="utf-8"))
    key("FD1_V1_primary_schema", not atlas_errors(primary))
    key("FD1_V2_coarse_schema", not atlas_errors(coarse))
    key("FD1_V3_failed_run_rejected", bool(atlas_errors(failed)))

    primary_rows = {identity(row): row for row in primary["rows"]}
    coarse_rows = {identity(row): row for row in coarse["rows"]}
    grid_drifts = []
    for row_id, prow in primary_rows.items():
        if float(prow["hbar"]) == 0.0:
            continue
        crow = coarse_rows[row_id]
        for name in ("omega_mminus", "omega_m0", "omega_mplus"):
            pv = np.asarray(prow[name])
            cv = np.asarray(crow[name])
            grid_drifts.append(float(np.max(np.abs(cv / pv - 1.0))))
    max_grid_drift = max(grid_drifts)
    key("FD1_V4_full_grid_convergence", max_grid_drift < 0.025)

    witnesses = [
        ("inv_n=0.9658", -2.0, "N", 1.0),
        ("inv_n=0.9658", 0.0, "D", 0.1),
        ("inv_n=0.9658", 0.95, "D", 0.001),
        ("inv_n=0.9470", 0.50, "N", 0.02),
        ("inv_n=0.9284", -1.0, "D", 0.1),
        ("inv_n=0.9284", 0.95, "N", 1.0),
    ]
    independent_rows = []
    max_independent_drift = 0.0
    max_independent_residual = 0.0
    for row_id in witnesses:
        row = primary_rows[row_id]
        n = float(row["n"])
        q = float(row["q"])
        hbar = float(row["hbar"])
        wall = str(row["wall"])
        umin = float(row["umin"])
        geometry = alternate_geometry(n, q, hbar, umin, 300)
        for m, field in ((-1, "omega_mminus"), (0, "omega_m0"), (1, "omega_mplus")):
            K, M, C = alternate_matrices(geometry, m, wall)
            for mode in (0, 3, 7):
                reference = float(row[field][mode])
                omega, residual = nonlinear_frequency(K, M, C, m, mode, reference)
                drift = abs(omega / reference - 1.0)
                max_independent_drift = max(max_independent_drift, drift)
                max_independent_residual = max(max_independent_residual, residual)
                independent_rows.append({
                    "identity": row_id,
                    "m": m,
                    "mode": mode,
                    "primary_omega": reference,
                    "independent_omega": omega,
                    "relative_drift": drift,
                    "raw_backward_residual": residual,
                })
    key("FD1_V5_independent_nonlinear_solver", max_independent_drift < 0.03)
    key("FD1_V6_independent_raw_residual", max_independent_residual < 1.0e-8)

    cutoff_witnesses = [
        ("inv_n=0.9658", 0.95, "D", 0.001),
        ("inv_n=0.9284", -2.0, "N", 1.0),
    ]
    cutoff_rows = []
    max_cutoff_drift = 0.0
    for row_id in cutoff_witnesses:
        row = primary_rows[row_id]
        n, q, hbar = float(row["n"]), float(row["q"]), float(row["hbar"])
        wall, base_umin = str(row["wall"]), float(row["umin"])
        reference_geometry = alternate_geometry(n, q, hbar, base_umin, 300)
        for m, field in ((-1, "omega_mminus"), (0, "omega_m0"), (1, "omega_mplus")):
            K0, M0, C0 = alternate_matrices(reference_geometry, m, wall)
            for mode in (0, 7):
                atlas_reference = float(row[field][mode])
                base_frequency, _ = nonlinear_frequency(K0, M0, C0, m, mode, atlas_reference)
                for factor in (0.1, 0.01):
                    geometry = alternate_geometry(n, q, hbar, base_umin * factor, 300)
                    K, M, C = alternate_matrices(geometry, m, wall)
                    frequency, residual = nonlinear_frequency(K, M, C, m, mode, base_frequency)
                    drift = abs(frequency / base_frequency - 1.0)
                    max_cutoff_drift = max(max_cutoff_drift, drift)
                    cutoff_rows.append({
                        "identity": row_id,
                        "m": m,
                        "mode": mode,
                        "cutoff_factor": factor,
                        "relative_drift": drift,
                        "raw_backward_residual": residual,
                    })
    key("FD1_V7_cutoff_10x_100x", max_cutoff_drift < 0.005)

    mutations = []
    duplicate = copy.deepcopy(primary)
    duplicate["rows"].append(copy.deepcopy(duplicate["rows"][0]))
    mutations.append(("duplicate_identity", bool(atlas_errors(duplicate))))
    disclosure = copy.deepcopy(primary)
    disclosure["observational_width_values_loaded"] = True
    mutations.append(("observational_disclosure", bool(atlas_errors(disclosure))))
    missing = copy.deepcopy(primary)
    live = next(row for row in missing["rows"] if float(row["hbar"]) > 0.0)
    del live["omega_mplus"]
    mutations.append(("missing_multiplet_member", bool(atlas_errors(missing))))
    split = copy.deepcopy(primary)
    q0 = next(row for row in split["rows"] if float(row["q_ratio"]) == 0.0 and float(row["hbar"]) > 0.0)
    q0["omega_mplus"][0] += 0.01
    mutations.append(("broken_q0_exact_split", bool(atlas_errors(split))))
    key("FD1_V8_catch_proofs", all(passed for _, passed in mutations))

    result = {
        "phase": "FD1_PHASE1_INDEPENDENT_VERIFICATION",
        "keys": KEYS,
        "hashes": {path.name: digest(path) for path in (PRIMARY, COARSE, FAILED)},
        "summary": {
            "maximum_g180_g240_frequency_drift": max_grid_drift,
            "maximum_independent_frequency_drift": max_independent_drift,
            "maximum_independent_raw_backward_residual": max_independent_residual,
            "maximum_10x_100x_cutoff_drift": max_cutoff_drift,
            "independent_points": len(independent_rows),
            "cutoff_points": len(cutoff_rows),
        },
        "independent_rows": independent_rows,
        "cutoff_rows": cutoff_rows,
        "catch_proofs": [{"name": name, "rejected": passed} for name, passed in mutations],
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"], indent=2, sort_keys=True))
    print(f"WROTE {OUT}")
    print(f"TOTAL KEYS {sum(KEYS.values())}/{len(KEYS)}")
    if not all(KEYS.values()):
        raise SystemExit(f"failed keys: {[name for name, passed in KEYS.items() if not passed]}")


if __name__ == "__main__":
    main()
