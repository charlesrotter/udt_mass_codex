#!/usr/bin/env python3
"""FD1 Phase 1: blind geometry atlas for the m=0,+1,-1 scalar-probe modes.

No CMB peak/trough datum is present or loaded.  The calculation remains on the scoped
RA1/RA2 equatorial stationary metric and records every frozen parameter point.
"""

from __future__ import annotations

import argparse
import json
import math
import time
from pathlib import Path

import numpy as np
import sympy as sp
from scipy import linalg as sla
from scipy.integrate import cumulative_trapezoid, quad


ROOT = Path(__file__).resolve().parent
INV_N_VALUES = (0.9658, 0.9470, 0.9284)
Q_RATIOS = (-2.0, -1.0, 0.0, 0.25, 0.50, 0.75, 0.95)
HBARS = (0.0, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0)
WALLS = ("D", "N")
NMODES = 8
ASYMPTOTIC_RATIO_MAX = 1.0e-6
KEYS: dict[str, bool] = {}


def key(name: str, condition: bool) -> None:
    KEYS[name] = bool(condition)
    print(f"KEY {name}: {KEYS[name]}")


def symbolic_layer() -> None:
    r = sp.symbols("r", positive=True)
    A = sp.Function("A", positive=True)(r)
    h = sp.Function("h", real=True)(r)
    omega, m = sp.symbols("omega m", real=True)
    D = A * r**2 + h**2
    p = sp.sqrt(A * D)
    weight = r**2 / sp.sqrt(A * D)
    cross = 2 * h * m / sp.sqrt(A * D)
    key("FD1_S1_pw_r2", sp.simplify(p * weight - r**2) == 0)
    key("FD1_S2_C_over_M", sp.simplify(cross / weight - 2 * m * h / r**2) == 0)

    lam, hbar = sp.symbols("lambda hbar", positive=True)
    root_plus = -hbar + sp.sqrt(hbar**2 + lam)
    root_minus = hbar + sp.sqrt(hbar**2 + lam)
    key("FD1_S3_q0_exact_split", sp.simplify(root_minus - root_plus - 2 * hbar) == 0)
    eta = (root_minus - root_plus) / ((root_minus + root_plus) / 2)
    key("FD1_S4_q0_eta", sp.simplify(eta - 2 * hbar / sp.sqrt(hbar**2 + lam)) == 0)

    n, q = sp.symbols("n q", real=True)
    sigma = (n + 2 * q) / 2
    qcrit = (2 - n) / 2
    key("FD1_S5_lc_boundary", sp.simplify(sigma.subs(q, qcrit) - 1) == 0)


def q_value(n: float, q_ratio: float) -> float:
    return 0.0 if q_ratio == 0.0 else q_ratio * (2.0 - n) / 2.0


def crossover_u(n: float, q: float, hbar: float) -> float:
    if hbar <= 0.0:
        return 0.0
    exponent = n - 2.0 * q
    return math.exp(2.0 * math.log(hbar) / exponent)


def family_umin(n: float, q: float) -> float:
    candidates = []
    exponent = n - 2.0 * q
    for hbar in HBARS:
        if hbar <= 0.0:
            continue
        log_uc = 2.0 * math.log(hbar) / exponent
        log_target = log_uc + math.log(ASYMPTOTIC_RATIO_MAX) / exponent
        candidates.append(min(1.0e-6, math.exp(max(log_target, math.log(1.0e-300)))))
    return max(1.0e-120, min(candidates))


def make_x_geometry(n: float, q: float, hbar: float, umin: float, size: int) -> dict[str, object]:
    """Build the metric-derived Liouville coordinate and midpoint coefficients.

    The asymptotic tail is included analytically, so the final node is the finite
    limit-circle wall rather than a coordinate cutoff masquerading as the wall.
    """
    sigma = (n + 2.0 * q) / 2.0
    smax = -math.log(umin)

    def scalar_integrand(s: float) -> float:
        if s == 0.0:
            return 1.0
        uu = math.exp(-s)
        rr = -math.expm1(-s)
        A = uu**n
        h = hbar * rr**2 * uu**q
        return rr * uu / math.sqrt(A * (A * rr**2 + h**2))

    samples = max(4000, int(math.ceil(200.0 * smax)))
    sgrid = np.linspace(0.0, smax, samples)
    ugrid = np.exp(-sgrid)
    rgrid = -np.expm1(-sgrid)
    Agrid = ugrid**n
    hgrid = hbar * rgrid**2 * ugrid**q
    denominator = np.sqrt(Agrid * (Agrid * rgrid**2 + hgrid**2))
    integrand = np.empty_like(sgrid)
    integrand[0] = 1.0
    integrand[1:] = rgrid[1:] * ugrid[1:] / denominator[1:]
    cumulative = cumulative_trapezoid(integrand, sgrid, initial=0.0)
    body, _ = quad(scalar_integrand, 0.0, smax, epsabs=1.0e-10, epsrel=2.0e-10, limit=600)
    cumulative *= body / cumulative[-1]
    tail = umin ** (1.0 - sigma) / (hbar * (1.0 - sigma))
    asymptotic_ratio = math.exp((n - 2.0 * q) * math.log(umin) - 2.0 * math.log(hbar))
    xwall = body + tail
    xnodes = np.linspace(0.0, xwall, size)
    xmid = 0.5 * (xnodes[:-1] + xnodes[1:])
    smid = np.empty_like(xmid)
    in_body = xmid <= body
    smid[in_body] = np.interp(xmid[in_body], cumulative, sgrid)
    remaining = xwall - xmid[~in_body]
    umid_tail = (hbar * (1.0 - sigma) * remaining) ** (1.0 / (1.0 - sigma))
    smid[~in_body] = -np.log(umid_tail)
    umid = np.exp(-smid)
    rmid = -np.expm1(-smid)
    Amid = umid**n
    hmid = hbar * rmid**2 * umid**q
    Dmid = Amid * rmid**2 + hmid**2
    connection = np.sqrt(Amid * Dmid) / (2.0 * rmid**2)
    return {
        "xnodes": xnodes,
        "rmid": rmid,
        "Amid": Amid,
        "hmid": hmid,
        "connection": connection,
        "xwall": xwall,
        "tail": tail,
        "asymptotic_ratio": asymptotic_ratio,
        "umin": umin,
    }


def assemble(
    geometry: dict[str, object],
    m: int,
    wall: str,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    xnodes = np.asarray(geometry["xnodes"])
    rmid = np.asarray(geometry["rmid"])
    Amid = np.asarray(geometry["Amid"])
    hmid = np.asarray(geometry["hmid"])
    connection = np.asarray(geometry["connection"])
    nn = len(xnodes)
    K = np.zeros((nn, nn))
    M = np.zeros((nn, nn))
    C = np.zeros((nn, nn))
    base_mass = np.array([[2.0, 1.0], [1.0, 2.0]]) / 6.0
    base_stiffness = np.array([[1.0, -1.0], [-1.0, 1.0]])
    for i, width in enumerate(np.diff(xnodes)):
        mass = width * base_mass
        a = connection[i]
        covariant = base_stiffness / width + np.array([[a, 0.0], [0.0, -a]]) + a * a * mass
        angular = (m * m) * Amid[i] / (rmid[i] ** 2)
        dragging = 2.0 * m * hmid[i] / (rmid[i] ** 2)
        sl = slice(i, i + 2)
        K[sl, sl] += covariant + angular * mass
        M[sl, sl] += mass
        C[sl, sl] += dragging * mass
    keep = np.ones(nn, dtype=bool)
    keep[0] = False
    if wall == "D":
        keep[-1] = False
    idx = np.flatnonzero(keep)
    K = K[np.ix_(idx, idx)]
    M = M[np.ix_(idx, idx)]
    C = C[np.ix_(idx, idx)]
    return K, M, C, idx


def solve_modes(
    geometry: dict[str, object],
    m: int,
    wall: str,
    candidates: int = 14,
) -> dict[str, object]:
    K, M, C, _ = assemble(geometry, m, wall)
    if m == 0:
        values, vectors = sla.eigh(K, M, check_finite=False)
        mask = values > 1.0e-12
        omega = np.sqrt(values[mask])[:candidates]
        vectors = vectors[:, mask][:, :candidates]
        residuals = [
            float(np.linalg.norm(K @ vectors[:, j] - omega[j] ** 2 * M @ vectors[:, j]) /
                  (np.linalg.norm(K @ vectors[:, j])
                   + omega[j] ** 2 * np.linalg.norm(M @ vectors[:, j])))
            for j in range(len(omega))
        ]
        return {
            "omega": omega,
            "vectors": vectors,
            "node_counts": [count_nodes(vectors[:, j]) for j in range(vectors.shape[1])],
            "raw_backward_residuals": residuals,
            "complex_count": 0,
            "near_real_count": int(len(omega)),
        }

    nn = K.shape[0]
    eye = np.eye(nn)
    zero = np.zeros_like(K)
    companion_a = np.block([[zero, eye], [K, -C]])
    companion_b = np.block([[eye, zero], [zero, M]])
    values, vectors = sla.eig(companion_a, companion_b, check_finite=False)
    tolerance = 2.0e-7 * np.maximum(1.0, np.abs(values.real))
    real_mask = np.abs(values.imag) <= tolerance
    positive = np.flatnonzero(real_mask & (values.real > 1.0e-9))
    positive = positive[np.argsort(values.real[positive])]
    positive = positive[:candidates]
    omega = values.real[positive]
    radial = vectors[:nn, positive].real
    norms = np.linalg.norm(radial, axis=0)
    radial = radial / norms
    residuals = []
    for j, frequency in enumerate(omega):
        vector = radial[:, j]
        raw = K @ vector - frequency * C @ vector - frequency**2 * M @ vector
        denominator = (
            np.linalg.norm(K @ vector)
            + abs(frequency) * np.linalg.norm(C @ vector)
            + frequency**2 * np.linalg.norm(M @ vector)
        )
        residuals.append(float(np.linalg.norm(raw) / denominator))
    return {
        "omega": omega,
        "vectors": radial,
        "node_counts": [count_nodes(radial[:, j]) for j in range(radial.shape[1])],
        "raw_backward_residuals": residuals,
        "complex_count": int(np.count_nonzero(~real_mask)),
        "near_real_count": int(np.count_nonzero(real_mask)),
    }


def count_nodes(vector: np.ndarray) -> int:
    """Count resolved sign changes; whitening preserves the radial function's signs."""
    vector = np.asarray(vector)
    threshold = 1.0e-8 * float(np.max(np.abs(vector)))
    signs = np.sign(vector[np.abs(vector) > threshold])
    return int(np.count_nonzero(signs[1:] != signs[:-1]))


def track(previous: np.ndarray | None, solved: dict[str, object]) -> tuple[np.ndarray, np.ndarray, float, list[int]]:
    """Use the ordered Sturm branch; overlap and resolved nodes remain diagnostics."""
    omega = np.asarray(solved["omega"])
    vectors = np.asarray(solved["vectors"])
    nodes = list(solved["node_counts"])
    if len(omega) < NMODES or not np.all(np.diff(omega[:NMODES]) > 0.0):
        raise RuntimeError("positive Sturm branch is incomplete or unordered")
    indices = list(range(NMODES))
    omega = omega[indices]
    vectors = vectors[:, indices]
    if previous is None:
        return omega, vectors, 1.0, nodes[:NMODES]
    overlap = np.abs(np.sum(previous * vectors, axis=0))
    signs = np.sign(np.sum(previous * vectors, axis=0))
    signs[signs == 0.0] = 1.0
    vectors *= signs
    return omega, vectors, float(np.min(overlap)), nodes[:NMODES]


def family_rows(n_label: str, n: float, q_ratio: float, wall: str, grid_size: int) -> list[dict[str, object]]:
    q = q_value(n, q_ratio)
    qcrit = (2.0 - n) / 2.0
    umin = family_umin(n, q)
    previous: dict[int, np.ndarray | None] = {-1: None, 0: None, 1: None}
    rows: list[dict[str, object]] = []
    for hbar in HBARS:
        if hbar == 0.0:
            rows.append({
                "n_label": n_label,
                "n": n,
                "q_ratio": q_ratio,
                "q": q,
                "qcrit": qcrit,
                "hbar": hbar,
                "wall": wall,
                "classification": "MU_OFF_LIMIT_POINT_CONTINUUM",
                "umin": umin,
            })
            continue
        geometry = make_x_geometry(n, q, hbar, umin, grid_size)
        modes: dict[int, np.ndarray] = {}
        match_scores: dict[int, float] = {}
        complex_counts: dict[int, int] = {}
        node_labels: dict[int, list[int]] = {}
        backward_residuals: dict[int, float] = {}
        for m in (-1, 0, 1):
            solved = solve_modes(geometry, m, wall)
            omega, vectors, score, nodes = track(previous[m], solved)
            previous[m] = vectors
            modes[m] = omega
            match_scores[m] = score
            complex_counts[m] = int(solved["complex_count"])
            node_labels[m] = nodes
            backward_residuals[m] = float(max(solved["raw_backward_residuals"][:NMODES]))
        mean_pair = 0.5 * (modes[1] + modes[-1])
        eta = np.abs(modes[1] - modes[-1]) / mean_pair
        displacement = np.maximum(np.abs(modes[1] - modes[0]), np.abs(modes[-1] - modes[0])) / modes[0]
        xwall = float(geometry["xwall"])
        xtail = float(geometry["tail"])
        q0_error = None
        if q_ratio == 0.0:
            q0_error = float(np.max(np.abs(np.abs(modes[1] - modes[-1]) - 2.0 * hbar)))
        rows.append({
            "n_label": n_label,
            "n": n,
            "q_ratio": q_ratio,
            "q": q,
            "qcrit": qcrit,
            "hbar": hbar,
            "wall": wall,
            "classification": "MIXING_CREATED_LIMIT_CIRCLE_LADDER",
            "umin": umin,
            "xwall": xwall,
            "tail_fraction": xtail / xwall,
            "tail_asymptotic_ratio": float(geometry["asymptotic_ratio"]),
            "omega_mminus": modes[-1].tolist(),
            "omega_m0": modes[0].tolist(),
            "omega_mplus": modes[1].tolist(),
            "eta_split": eta.tolist(),
            "full_displacement": displacement.tolist(),
            "min_tracking_overlap": min(match_scores.values()),
            "complex_counts": {str(k): v for k, v in complex_counts.items()},
            "resolved_node_counts": {str(k): v for k, v in node_labels.items()},
            "sturm_mode_labels": list(range(NMODES)),
            "max_raw_backward_residual": {str(k): v for k, v in backward_residuals.items()},
            "q0_split_max_abs_error": q0_error,
        })
    print(
        f"FAMILY n={n:.8f} q/qcrit={q_ratio:+.2f} wall={wall} "
        f"umin={umin:.1e} rows={len(rows)}"
    )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--grid", type=int, default=240)
    parser.add_argument("--output", default="phase1_atlas.json")
    parser.add_argument(
        "--max-families",
        type=int,
        default=0,
        help="conditioning smoke only: run the first N families; 0 runs the frozen full atlas",
    )
    args = parser.parse_args()
    start = time.time()
    symbolic_layer()
    families: list[tuple[str, float, float, str]] = []
    for inv_n in INV_N_VALUES:
        n = 1.0 / inv_n
        label = f"inv_n={inv_n:.4f}"
        for ratio in Q_RATIOS:
            for wall in WALLS:
                families.append((label, n, ratio, wall))
    production_complete = args.max_families == 0
    if args.max_families < 0:
        raise SystemExit("--max-families must be nonnegative")
    if args.max_families:
        families = families[: args.max_families]
        print("PARTIAL CONDITIONING RUN: this output cannot certify the Phase-I atlas")
    rows: list[dict[str, object]] = []
    for label, n, ratio, wall in families:
        rows.extend(family_rows(label, n, ratio, wall, args.grid))
    q0_errors = [row["q0_split_max_abs_error"] for row in rows if row.get("q0_split_max_abs_error") is not None]
    overlaps = [row["min_tracking_overlap"] for row in rows if "min_tracking_overlap" in row]
    tail_fractions = [row["tail_fraction"] for row in rows if "tail_fraction" in row]
    tail_asymptotic_ratios = [row["tail_asymptotic_ratio"] for row in rows if "tail_asymptotic_ratio" in row]
    complex_total = sum(sum(row.get("complex_counts", {}).values()) for row in rows)
    sturm_ordered = all(
        np.all(np.diff(np.asarray(row[key_name])) > 0.0)
        for row in rows
        if "omega_m0" in row
        for key_name in ("omega_mminus", "omega_m0", "omega_mplus")
    )
    max_backward_residual = max(
        value
        for row in rows
        for value in row.get("max_raw_backward_residual", {}).values()
    )
    key("FD1_N1_row_count", len(rows) == len(families) * len(HBARS))
    if q0_errors:
        key("FD1_N2_q0_exact_anchor", max(q0_errors) < 2.0e-6)
    else:
        print("CHECK FD1_N2_q0_exact_anchor: NOT_EVALUATED_IN_PARTIAL_RUN")
    key("FD1_N3_sturm_ordered", sturm_ordered)
    key("FD1_N4_tail_asymptotic_control", max(tail_asymptotic_ratios) <= 1.01 * ASYMPTOTIC_RATIO_MAX)
    key("FD1_N5_real_spectrum", complex_total == 0)
    key("FD1_N6_raw_backward_residual", max_backward_residual < 1.0e-8)
    payload = {
        "phase": "PHASE1_BLIND_GEOMETRY",
        "run_scope": "FROZEN_FULL_ATLAS" if production_complete else "PARTIAL_CONDITIONING_ONLY",
        "production_complete": production_complete,
        "observational_width_values_loaded": False,
        "config": {
            "inv_n_values": INV_N_VALUES,
            "q_ratios": Q_RATIOS,
            "hbars": HBARS,
            "walls": WALLS,
            "grid": args.grid,
            "nmodes": NMODES,
            "tail_asymptotic_ratio_max": ASYMPTOTIC_RATIO_MAX,
            "families_run": len(families),
            "families_frozen_total": len(INV_N_VALUES) * len(Q_RATIOS) * len(WALLS),
        },
        "keys": KEYS,
        "summary": {
            "rows": len(rows),
            "q0_max_abs_error": max(q0_errors) if q0_errors else None,
            "minimum_tracking_overlap": min(overlaps),
            "maximum_tail_fraction": max(tail_fractions),
            "maximum_tail_asymptotic_ratio": max(tail_asymptotic_ratios),
            "complex_eigenvalue_count": complex_total,
            "maximum_raw_backward_residual": max_backward_residual,
            "runtime_seconds": time.time() - start,
        },
        "rows": rows,
    }
    output = ROOT / args.output
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    print(f"WROTE {output}")
    print(f"TOTAL KEYS {sum(KEYS.values())}/{len(KEYS)}")
    if production_complete and not all(KEYS.values()):
        raise SystemExit(f"failed keys: {[name for name, passed in KEYS.items() if not passed]}")


if __name__ == "__main__":
    main()
