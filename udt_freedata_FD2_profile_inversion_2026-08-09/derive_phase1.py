#!/usr/bin/env python3
"""FD2 Phase I: blind localized-profile response atlas.

This program deliberately contains no CMB peak/trough values and loads no SNe magnitudes.
It computes the m=0 scalar-probe frequency response of the frozen FD2 motif census.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import time
from pathlib import Path

import numpy as np
from scipy import linalg as sla
from scipy.integrate import cumulative_trapezoid, quad


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
FD1_DIR = REPO / "udt_freedata_FD1_mixing_bound_2026-08-09"
INV_N = 0.9470
N = 1.0 / INV_N
DELTA = 1.0e-4
NMODES = 7
BACKGROUNDS = (
    {"q_ratio": 0.75, "wall": "D", "hbar": 0.01},
    {"q_ratio": 0.75, "wall": "N", "hbar": 0.01},
    {"q_ratio": 0.95, "wall": "D", "hbar": 0.5},
    {"q_ratio": 0.95, "wall": "N", "hbar": 0.5},
)
SUPPORTS = (
    *((0.025, round(0.05 * i, 3)) for i in range(1, 20)),
    *((0.05, round(0.10 * i, 3)) for i in range(1, 10)),
    *((0.10, round(0.10 * i, 3)) for i in range(2, 9)),
    *((0.20, round(0.10 * i, 3)) for i in range(3, 8)),
)
MOTIF_CLASSES = ("BUMP", "DIPOLE")
EXPECTED_PARENT_HASHES = {
    "derive_phase1.py": "f0249178721016d990f3cd6a6b89b2b14e91d0f003a90f62c47f92faa717060c",
    "phase1_atlas_g180.json": "a7412a6e382df91cb6552c8a81b56c1cd57f6eec484a1e67036edc64e19ee5b5",
    "phase1_atlas_g240.json": "534713dea58c7a99a0b5ed149c33c08972f458d558bedb681f67c0d3f376110d",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def motif_id(kind: str, center: float, halfwidth: float) -> str:
    return f"{kind}_c{center:.3f}_w{halfwidth:.3f}"


def compact_core(xi: np.ndarray) -> np.ndarray:
    xi = np.asarray(xi, dtype=float)
    out = np.zeros_like(xi)
    inside = np.abs(xi) < 1.0
    out[inside] = np.exp(1.0 - 1.0 / (1.0 - xi[inside] ** 2))
    return out


def motif_value(s: np.ndarray, kind: str, center: float, halfwidth: float) -> np.ndarray:
    xi = (np.asarray(s, dtype=float) - center) / halfwidth
    core = compact_core(xi)
    if kind == "BUMP":
        return core
    if kind == "DIPOLE":
        raw = xi * core
        # The analytic maximum of |xi exp(1-1/(1-xi^2))| is fixed, but numerical
        # normalization on a dense reference grid is simpler and deterministic.
        ref = np.linspace(-1.0, 1.0, 20001)
        norm = float(np.max(np.abs(ref * compact_core(ref))))
        return raw / norm
    raise ValueError(kind)


def q_value(n: float, q_ratio: float) -> float:
    return q_ratio * (2.0 - n) / 2.0


def fd1_rows(grid: int) -> tuple[dict[str, object], dict[tuple[float, str, float], dict[str, object]]]:
    path = FD1_DIR / f"phase1_atlas_g{grid}.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    rows = {}
    for row in payload["rows"]:
        if row.get("n_label") != "inv_n=0.9470" or float(row.get("hbar", 0.0)) <= 0.0:
            continue
        key = (float(row["q_ratio"]), str(row["wall"]), float(row["hbar"]))
        rows[key] = row
    return payload, rows


def make_geometry(
    n: float,
    q: float,
    hbar: float,
    umin: float,
    size: int,
    kind: str,
    center: float,
    halfwidth: float,
    coefficient: float,
) -> dict[str, object]:
    """Metric-derived Liouville coordinate for A=u^n exp(c B)."""
    sigma = (n + 2.0 * q) / 2.0
    smax = -math.log(umin)

    def scalar_integrand(y: float) -> float:
        if y == 0.0:
            return 1.0
        u = math.exp(-y)
        r = -math.expm1(-y)
        b = float(motif_value(np.array([r]), kind, center, halfwidth)[0])
        A = math.exp(n * math.log(u) + coefficient * b)
        h = hbar * r * r * u**q
        return r * u / math.sqrt(A * (A * r * r + h * h))

    samples = max(4000, int(math.ceil(200.0 * smax)))
    ygrid = np.linspace(0.0, smax, samples)
    ugrid = np.exp(-ygrid)
    rgrid = -np.expm1(-ygrid)
    bgrid = motif_value(rgrid, kind, center, halfwidth)
    Agrid = np.exp(n * np.log(ugrid) + coefficient * bgrid)
    hgrid = hbar * rgrid**2 * ugrid**q
    denominator = np.sqrt(Agrid * (Agrid * rgrid**2 + hgrid**2))
    integrand = np.empty_like(ygrid)
    integrand[0] = 1.0
    integrand[1:] = rgrid[1:] * ugrid[1:] / denominator[1:]
    cumulative = cumulative_trapezoid(integrand, ygrid, initial=0.0)
    body, _ = quad(scalar_integrand, 0.0, smax, epsabs=1.0e-10, epsrel=2.0e-10, limit=600)
    cumulative *= body / cumulative[-1]

    # Every registered motif vanishes before the asymptotic tail, so the FD1 tail is exact.
    tail = umin ** (1.0 - sigma) / (hbar * (1.0 - sigma))
    xwall = body + tail
    xnodes = np.linspace(0.0, xwall, size)
    xmid = 0.5 * (xnodes[:-1] + xnodes[1:])
    ymid = np.empty_like(xmid)
    in_body = xmid <= body
    ymid[in_body] = np.interp(xmid[in_body], cumulative, ygrid)
    remaining = xwall - xmid[~in_body]
    umid_tail = (hbar * (1.0 - sigma) * remaining) ** (1.0 / (1.0 - sigma))
    ymid[~in_body] = -np.log(umid_tail)
    umid = np.exp(-ymid)
    rmid = -np.expm1(-ymid)
    bmid = motif_value(rmid, kind, center, halfwidth)
    Amid = np.exp(n * np.log(umid) + coefficient * bmid)
    hmid = hbar * rmid**2 * umid**q
    Dmid = Amid * rmid**2 + hmid**2
    connection = np.sqrt(Amid * Dmid) / (2.0 * rmid**2)
    return {
        "xnodes": xnodes,
        "connection": connection,
        "xwall": float(xwall),
        "tail": float(tail),
    }


def assemble_m0(geometry: dict[str, object], wall: str) -> tuple[np.ndarray, np.ndarray]:
    xnodes = np.asarray(geometry["xnodes"], dtype=float)
    connection = np.asarray(geometry["connection"], dtype=float)
    nn = len(xnodes)
    K = np.zeros((nn, nn))
    M = np.zeros((nn, nn))
    base_mass = np.array([[2.0, 1.0], [1.0, 2.0]]) / 6.0
    base_stiffness = np.array([[1.0, -1.0], [-1.0, 1.0]])
    for i, width in enumerate(np.diff(xnodes)):
        mass = width * base_mass
        a = connection[i]
        covariant = base_stiffness / width + np.array([[a, 0.0], [0.0, -a]]) + a * a * mass
        sl = slice(i, i + 2)
        K[sl, sl] += covariant
        M[sl, sl] += mass
    keep = np.ones(nn, dtype=bool)
    keep[0] = False
    if wall == "D":
        keep[-1] = False
    idx = np.flatnonzero(keep)
    return K[np.ix_(idx, idx)], M[np.ix_(idx, idx)]


def solve_m0(geometry: dict[str, object], wall: str) -> tuple[np.ndarray, float]:
    K, M = assemble_m0(geometry, wall)
    values, vectors = sla.eigh(
        K,
        M,
        subset_by_index=(0, min(K.shape[0] - 1, NMODES + 4)),
        check_finite=False,
        driver="gvx",
    )
    mask = values > 1.0e-12
    values = values[mask][:NMODES]
    vectors = vectors[:, mask][:, :NMODES]
    if len(values) != NMODES:
        raise RuntimeError("insufficient positive modes")
    omega = np.sqrt(values)
    residuals = []
    for j, frequency in enumerate(omega):
        v = vectors[:, j]
        raw = K @ v - frequency**2 * M @ v
        denominator = np.linalg.norm(K @ v) + frequency**2 * np.linalg.norm(M @ v)
        residuals.append(float(np.linalg.norm(raw) / denominator))
    return omega, max(residuals)


def response_row(
    background: dict[str, object],
    parent: dict[str, object],
    grid: int,
    kind: str,
    center: float,
    halfwidth: float,
    omega0: np.ndarray,
    residual0: float,
) -> dict[str, object]:
    q = q_value(N, float(background["q_ratio"]))
    umin = float(parent["umin"])
    solves: dict[str, np.ndarray] = {"zero": omega0}
    residuals = [residual0]
    for label, coefficient in (
        ("plus", DELTA),
        ("minus", -DELTA),
        ("half_plus", DELTA / 2.0),
        ("half_minus", -DELTA / 2.0),
    ):
        geometry = make_geometry(
            N,
            q,
            float(background["hbar"]),
            umin,
            grid,
            kind,
            center,
            halfwidth,
            coefficient,
        )
        solves[label], residual = solve_m0(geometry, str(background["wall"]))
        residuals.append(residual)
    j_full = (solves["plus"] - solves["minus"]) / (2.0 * DELTA)
    j_half = (solves["half_plus"] - solves["half_minus"]) / DELTA
    step_drift = float(np.linalg.norm(j_full - j_half) / max(np.linalg.norm(j_half), 1.0e-14))
    return {
        "identity": motif_id(kind, center, halfwidth),
        "motif_class": kind,
        "center": center,
        "halfwidth": halfwidth,
        "q_ratio": float(background["q_ratio"]),
        "q": q,
        "wall": str(background["wall"]),
        "hbar": float(background["hbar"]),
        "inv_n": INV_N,
        "n": N,
        "umin": umin,
        "omega0": omega0.tolist(),
        "response_delta": j_full.tolist(),
        "response_half_delta": j_half.tolist(),
        "halfstep_relative_norm_drift": step_drift,
        "maximum_raw_backward_residual": max(residuals),
        "positive_ordered": bool(np.all(np.diff(omega0) > 0.0)),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--grid", type=int, choices=(180, 240), required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--max-rows", type=int, default=0, help="conditioning smoke only")
    args = parser.parse_args()

    parent_path = FD1_DIR / f"phase1_atlas_g{args.grid}.json"
    expected = EXPECTED_PARENT_HASHES[parent_path.name]
    if sha256(parent_path) != expected:
        raise SystemExit(f"parent atlas hash mismatch: {parent_path}")
    if sha256(FD1_DIR / "derive_phase1.py") != EXPECTED_PARENT_HASHES["derive_phase1.py"]:
        raise SystemExit("FD1 production script hash mismatch")
    parent_payload, parent_rows = fd1_rows(args.grid)

    frozen = []
    for background in BACKGROUNDS:
        for halfwidth, center in SUPPORTS:
            for kind in MOTIF_CLASSES:
                frozen.append((background, kind, center, halfwidth))
    production_complete = args.max_rows == 0
    if args.max_rows:
        frozen = frozen[: args.max_rows]
        print("PARTIAL CONDITIONING RUN: cannot certify the frozen atlas")

    start = time.time()
    base_cache: dict[tuple[float, str, float], tuple[np.ndarray, float]] = {}
    rows = []
    for index, (background, kind, center, halfwidth) in enumerate(frozen, 1):
        background_key = (
            float(background["q_ratio"]),
            str(background["wall"]),
            float(background["hbar"]),
        )
        parent = parent_rows[background_key]
        if background_key not in base_cache:
            geometry0 = make_geometry(
                N,
                q_value(N, background_key[0]),
                background_key[2],
                float(parent["umin"]),
                args.grid,
                "BUMP",
                0.5,
                0.1,
                0.0,
            )
            base_cache[background_key] = solve_m0(geometry0, background_key[1])
        omega0, residual0 = base_cache[background_key]
        rows.append(
            response_row(background, parent, args.grid, kind, center, halfwidth, omega0, residual0)
        )
        if index % 20 == 0 or index == len(frozen):
            print(f"ROW {index}/{len(frozen)} elapsed={time.time()-start:.1f}s")

    baseline_drifts = []
    for background_key, (omega0, _) in base_cache.items():
        parent = parent_rows[background_key]
        reference = np.asarray(parent["omega_m0"][:NMODES], dtype=float)
        baseline_drifts.append(float(np.max(np.abs(omega0 / reference - 1.0))))

    unique = {
        (row["identity"], row["q_ratio"], row["wall"], row["hbar"])
        for row in rows
    }
    summary = {
        "row_count": len(rows),
        "unique_row_count": len(unique),
        "expected_production_rows": 320,
        "maximum_baseline_relative_drift_from_fd1": max(baseline_drifts),
        "maximum_raw_backward_residual": max(row["maximum_raw_backward_residual"] for row in rows),
        "maximum_halfstep_relative_norm_drift": max(row["halfstep_relative_norm_drift"] for row in rows),
        "halfstep_unresolved_row_count": sum(row["halfstep_relative_norm_drift"] > 0.02 for row in rows),
        "all_positive_ordered": all(row["positive_ordered"] for row in rows),
        "all_finite": all(
            np.all(np.isfinite(np.asarray(row[field], dtype=float)))
            for row in rows
            for field in ("omega0", "response_delta", "response_half_delta")
        ),
        "runtime_seconds": time.time() - start,
    }
    gates = {
        "row_count": (not production_complete) or len(rows) == 320,
        "identity_unique": len(unique) == len(rows),
        "positive_ordered": summary["all_positive_ordered"],
        "finite": summary["all_finite"],
        "raw_backward_residual": summary["maximum_raw_backward_residual"] < 1.0e-8,
        "fd1_baseline_reproduction": summary["maximum_baseline_relative_drift_from_fd1"] < 5.0e-4,
    }
    payload = {
        "phase": "FD2_PHASE1_BLIND_PROFILE_RESPONSE",
        "observational_peak_values_loaded": False,
        "sne_magnitudes_loaded": False,
        "production_complete": production_complete,
        "config": {
            "grid": args.grid,
            "inv_n": INV_N,
            "n": N,
            "delta": DELTA,
            "nmodes": NMODES,
            "backgrounds": BACKGROUNDS,
            "supports": [{"halfwidth": w, "center": c} for w, c in SUPPORTS],
            "motif_classes": MOTIF_CLASSES,
        },
        "parent": {
            "fd1_atlas": str(parent_path.relative_to(REPO)),
            "fd1_atlas_sha256": sha256(parent_path),
            "fd1_all_internal_gates": all(parent_payload["keys"].values()),
        },
        "gates": gates,
        "summary": summary,
        "rows": rows,
    }
    output = ROOT / args.output
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    print(json.dumps(gates, indent=2, sort_keys=True))
    print(f"WROTE {output}")
    if production_complete and not all(gates.values()):
        raise SystemExit(f"failed gates: {[name for name, passed in gates.items() if not passed]}")


if __name__ == "__main__":
    main()
