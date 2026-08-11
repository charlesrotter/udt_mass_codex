#!/usr/bin/env python3
"""Bounded solved-geometry atlas for two preregistered UDT metric families.

This is a geometry solver, not a field-equation or stability solver.  It integrates
metric-owned geodesics and Levi-Civita transport, evaluates the R17 normal
connection, and records every preregistered witness without outcome filtering.
"""

from __future__ import annotations

import csv
import hashlib
import json
import platform
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import scipy
from scipy.integrate import solve_ivp


HERE = Path(__file__).resolve().parent
ETA = np.diag([-1.0, 1.0, 1.0, 1.0])
RTOL = 1.0e-10
ATOL = 1.0e-12
MAX_STEP = 1.0e-2
CS_H = 1.0e-30
DEXP_H = 1.0e-6
AFFINE_END = 0.40


@dataclass(frozen=True)
class Sample:
    sample_id: str
    geometry: str
    lam: float = 0.0
    eps: float = 0.0
    twist: float = 0.4


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def load_samples() -> list[Sample]:
    rows = list(csv.DictReader((HERE / "NUMERICAL_SAMPLE_UNIVERSE.tsv").open(), delimiter="\t"))
    out: list[Sample] = []
    for row in rows:
        p = {x.split("=", 1)[0]: x.split("=", 1)[1] for x in (row["parameter_1"], row["parameter_2"]) if "=" in x}
        out.append(
            Sample(
                sample_id=row["sample_id"],
                geometry=row["geometry"],
                lam=float(p.get("lambda", 0.0)),
                eps=float(p.get("epsilon", 0.0)),
            )
        )
    if len(out) != 14 or len({s.sample_id for s in out}) != 14:
        raise RuntimeError("preregistered sample universe is not the exact 14-row universe")
    return out


def r17_phi(x: np.ndarray, eps: float):
    _, th, va, ps = x
    x1 = np.cos(th / 2) * np.cos((ps + va) / 2)
    x2 = np.cos(th / 2) * np.sin((ps + va) / 2)
    x3 = np.sin(th / 2) * np.cos((ps - va) / 2)
    x4 = np.sin(th / 2) * np.sin((ps - va) / 2)
    return 0.12 * x1 + 0.08 * x2 * x3 - 0.05 * (x4 * x4 - x3 * x3) + eps * (0.11 * x4 + 0.07 * x1 * x2)


def r17_coframe(x: np.ndarray, sample: Sample) -> np.ndarray:
    _, th, _, ps = x
    phi = r17_phi(x, sample.eps)
    u = np.exp(phi)
    v = np.exp(sample.lam * phi)
    # Half-scaled SU(2) forms: d sigma_i = -2 epsilon_ijk sigma_j wedge sigma_k.
    s1 = 0.5 * np.array([0, np.cos(ps), np.sin(ps) * np.sin(th), 0], dtype=x.dtype)
    s2 = 0.5 * np.array([0, -np.sin(ps), np.cos(ps) * np.sin(th), 0], dtype=x.dtype)
    s3 = 0.5 * np.array([0, 0, np.cos(th), 1], dtype=x.dtype)
    dt = np.array([1, 0, 0, 0], dtype=x.dtype)
    return np.vstack(((dt + sample.twist * s3) / u, u * s3, v * s1, v * s2))


def timelive_fields(x: np.ndarray, eps: float):
    t, xx, y, z = x
    kappa = 0.035 * np.sin(t + 0.3 * y) + 0.018 * np.cos(xx - z) + eps * 0.025 * np.sin(t + xx + y)
    phi = 0.11 * np.cos(xx - 0.2 * t) + 0.025 * np.sin(y + z) + eps * 0.08 * np.cos(t - z + 0.4 * xx)
    beta = 0.12 * np.sin(t + xx) + 0.04 * np.cos(y - z) + eps * 0.05 * np.sin(t + y)
    gamma = 0.16 * np.sin(t - y + 0.2 * z) + eps * 0.04 * np.cos(xx + z)
    q1 = 0.045 * np.cos(t + y) + eps * 0.03 * np.sin(xx - z)
    q2 = -0.035 * np.sin(xx + z) + eps * 0.025 * np.cos(t - y)
    shear = 0.07 * np.sin(t + xx + y + z) + eps * 0.025 * np.cos(xx - y)
    s00 = 0.055 * np.cos(t + y) + eps * 0.02 * np.sin(z)
    s01 = 0.045 * np.sin(xx - z) + eps * 0.015 * np.cos(t + y)
    s10 = -0.04 * np.cos(t - xx + y) + eps * 0.02 * np.sin(xx + z)
    s11 = 0.05 * np.sin(t + z) + eps * 0.018 * np.cos(xx - y)
    return kappa, phi, beta, gamma, q1, q2, shear, np.array([[s00, s01], [s10, s11]], dtype=x.dtype)


def timelive_coframe(x: np.ndarray, sample: Sample) -> np.ndarray:
    kappa, phi, beta, gamma, q1, q2, shear, S = timelive_fields(x, sample.eps)
    T = np.exp(kappa - phi)
    L = np.exp(kappa + phi)
    B = np.array([[T, T * beta], [0, L]], dtype=x.dtype)
    R = np.array([[np.cos(gamma), -np.sin(gamma)], [np.sin(gamma), np.cos(gamma)]], dtype=x.dtype)
    U = np.array([[np.exp(q1), shear], [0, np.exp(q2)]], dtype=x.dtype)
    Q = R @ U
    E = np.zeros((4, 4), dtype=x.dtype)
    E[:2, :2] = B
    E[2:, :2] = Q @ S
    E[2:, 2:] = Q
    return E


def coframe(x: np.ndarray, sample: Sample) -> np.ndarray:
    return r17_coframe(x, sample) if sample.geometry == "R17_GLOBAL" else timelive_coframe(x, sample)


def metric(x: np.ndarray, sample: Sample) -> np.ndarray:
    E = coframe(x, sample)
    return E.T @ ETA @ E


def metric_derivatives(x: np.ndarray, sample: Sample) -> np.ndarray:
    out = np.empty((4, 4, 4), dtype=float)
    xc = np.asarray(x, dtype=complex)
    for k in range(4):
        z = xc.copy()
        z[k] += 1j * CS_H
        out[k] = np.imag(metric(z, sample)) / CS_H
    return out


def christoffel(x: np.ndarray, sample: Sample) -> np.ndarray:
    g = np.asarray(metric(np.asarray(x), sample), dtype=float)
    gi = np.linalg.inv(g)
    dg = metric_derivatives(np.asarray(x, dtype=float), sample)
    G = np.zeros((4, 4, 4), dtype=float)
    for a in range(4):
        for b in range(4):
            for c in range(4):
                G[a, b, c] = 0.5 * sum(gi[a, d] * (dg[b, d, c] + dg[c, d, b] - dg[d, b, c]) for d in range(4))
    return G


def initial_point(sample: Sample) -> np.ndarray:
    if sample.geometry == "R17_GLOBAL":
        return np.array([0.07, 1.08, 0.31, 0.44])
    return np.array([0.12, -0.18, 0.23, -0.14])


def initial_velocity(x0: np.ndarray, sample: Sample, causal: str) -> np.ndarray:
    frame = np.linalg.inv(coframe(x0, sample))
    if causal == "TIMELIKE":
        return np.asarray(frame[:, 0] + 0.18 * frame[:, 2], dtype=float) / np.sqrt(1.0 - 0.18**2)
    return np.asarray(frame[:, 1] + 0.22 * frame[:, 3], dtype=float) / np.sqrt(1.0 + 0.22**2)


def geodesic_rhs(_, y: np.ndarray, sample: Sample, with_transport: bool) -> np.ndarray:
    x = y[:4]
    v = y[4:8]
    G = christoffel(x, sample)
    acc = -np.einsum("abc,b,c->a", G, v, v)
    if not with_transport:
        return np.concatenate((v, acc))
    P = y[8:].reshape(4, 4)
    W = np.einsum("abc,b->ac", G, v)
    return np.concatenate((v, acc, (-W @ P).ravel()))


def solve_geodesic(sample: Sample, causal: str, dv: np.ndarray | None = None, with_transport: bool = False):
    x0 = initial_point(sample)
    v0 = initial_velocity(x0, sample, causal)
    if dv is not None:
        v0 = v0 + dv
    y0 = np.concatenate((x0, v0, np.eye(4).ravel())) if with_transport else np.concatenate((x0, v0))
    sol = solve_ivp(
        lambda s, y: geodesic_rhs(s, y, sample, with_transport),
        (0.0, AFFINE_END),
        y0,
        method="DOP853",
        rtol=RTOL,
        atol=ATOL,
        max_step=MAX_STEP,
    )
    if not sol.success:
        raise RuntimeError(f"geodesic failure {sample.sample_id} {causal}: {sol.message}")
    return sol.y[:, -1], len(sol.t)


def dexp_singular_values(sample: Sample, causal: str) -> np.ndarray:
    cols = []
    for j in range(4):
        dv = np.zeros(4)
        dv[j] = DEXP_H
        yp, _ = solve_geodesic(sample, causal, dv=dv)
        ym, _ = solve_geodesic(sample, causal, dv=-dv)
        cols.append((yp[:4] - ym[:4]) / (2 * DEXP_H))
    return np.linalg.svd(np.column_stack(cols), compute_uv=False)


def pair_readout(x: np.ndarray, sample: Sample):
    g = metric(x, sample)
    J = np.zeros((4, 2))
    J[0, 0] = 1.0
    J[3, 1] = 2.0 if sample.geometry == "R17_GLOBAL" else 0.0
    J[1, 1] = 0.0 if sample.geometry == "R17_GLOBAL" else 1.0
    h = J.T @ g @ J
    ev = np.linalg.eigvalsh(h)
    det = np.linalg.det(h)
    regular = h[0, 0] < 0 and det < 0 and np.sum(ev < 0) == 1
    phi_pair = float(0.25 * np.log((-det) / (h[0, 0] ** 2))) if regular else np.nan
    return h, ev, regular, phi_pair


def endpoint_atlas_defect(sample: Sample):
    p = initial_point(sample)
    q = p + (np.array([0.08, 0.035, -0.04, 0.06]) if sample.geometry == "R17_GLOBAL" else np.array([0.07, -0.05, 0.04, 0.03]))
    r = p + (np.array([0.13, -0.025, 0.07, 0.11]) if sample.geometry == "R17_GLOBAL" else np.array([0.14, 0.025, -0.06, 0.08]))
    Ep, Eq, Er = coframe(p, sample), coframe(q, sample), coframe(r, sample)
    Apq = np.linalg.solve(Eq, Ep)
    Aqr = np.linalg.solve(Er, Eq)
    Apr = np.linalg.solve(Er, Ep)
    return float(np.linalg.norm(Aqr @ Apq - Apr)), p, q


def path_segments(sample: Sample, name: str):
    x0 = initial_point(sample)
    if sample.geometry == "R17_GLOBAL":
        if name == "HOPF_FIBER":
            def path(s):
                x = x0.copy(); x[3] += 4 * np.pi * s
                dx = np.array([0.0, 0.0, 0.0, 4 * np.pi])
                return x, dx
            return [(path, 0.0, 1.0)]
        dth, dva = 0.17, 0.19
        dirs = [(1, dth), (2, dva), (1, -dth), (2, -dva)]
    else:
        axes = (0, 1) if name == "TX_RECTANGLE" else (2, 3)
        dirs = [(axes[0], 0.16), (axes[1], 0.18), (axes[0], -0.16), (axes[1], -0.18)]
    segments = []
    current = x0.copy()
    for axis, amount in dirs:
        start = current.copy()
        def path(s, start=start, axis=axis, amount=amount):
            x = start.copy(); x[axis] += amount * s
            dx = np.zeros(4); dx[axis] = amount
            return x, dx
        segments.append((path, 0.0, 1.0))
        current[axis] += amount
    return segments


def normal_connection_coord(x: np.ndarray, sample: Sample) -> np.ndarray:
    if sample.geometry != "R17_GLOBAL":
        return np.zeros(4)
    E = r17_coframe(x, sample)
    frame = np.linalg.inv(E)
    grad = np.empty(4)
    xc = np.asarray(x, dtype=complex)
    for k in range(4):
        z = xc.copy(); z[k] += 1j * CS_H
        grad[k] = np.imag(r17_phi(z, sample.eps)) / CS_H
    p = frame.T @ grad
    phi = r17_phi(x, sample.eps)
    u, v = np.exp(phi), np.exp(sample.lam * phi)
    Avec = np.array([
        sample.twist / (u * v * v),
        2.0 / u - u / (v * v),
        -sample.lam * p[3] / v,
        sample.lam * p[2] / v,
    ])
    return Avec @ E


def integrate_loop(sample: Sample, name: str):
    P = np.eye(4)
    normal_angle = 0.0
    nsteps = 0
    for path, lo, hi in path_segments(sample, name):
        def rhs(s, y):
            x, dx = path(s)
            G = christoffel(x, sample)
            W = np.einsum("abc,b->ac", G, dx)
            dP = -W @ y[:16].reshape(4, 4)
            dangle = float(normal_connection_coord(x, sample) @ dx)
            return np.concatenate((dP.ravel(), [dangle]))
        y0 = np.concatenate((P.ravel(), [normal_angle]))
        sol = solve_ivp(rhs, (lo, hi), y0, method="DOP853", rtol=RTOL, atol=ATOL, max_step=MAX_STEP)
        if not sol.success:
            raise RuntimeError(f"loop failure {sample.sample_id} {name}: {sol.message}")
        P = sol.y[:16, -1].reshape(4, 4)
        normal_angle = float(sol.y[16, -1])
        nsteps += len(sol.t)
    x0 = initial_point(sample)
    metric_defect = float(np.linalg.norm(P.T @ metric(x0, sample) @ P - metric(x0, sample)))
    return P, normal_angle, metric_defect, nsteps


def classify_holonomy(P: np.ndarray) -> str:
    return "NONIDENTITY" if np.linalg.norm(P - np.eye(4)) > 1.0e-5 else "IDENTITY_WITHIN_TOLERANCE"


def write_tsv(path: Path, rows: list[dict]):
    if not rows:
        raise RuntimeError(f"refusing empty output {path}")
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        w.writeheader(); w.writerows(rows)


def main():
    atlas_rows, geodesic_rows, path_rows = [], [], []
    for sample in load_samples():
        defect, p, q = endpoint_atlas_defect(sample)
        hp, evp, regp, phip = pair_readout(p, sample)
        hq, evq, regq, phiq = pair_readout(q, sample)
        if sample.geometry == "R17_GLOBAL":
            field_delta = float(r17_phi(q, sample.eps) - r17_phi(p, sample.eps))
            pair_delta_defect = abs((phiq - phip) - field_delta)
            paths = ("HOPF_FIBER", "LOCAL_RECTANGLE")
            completion = "GLOBAL_RxS3_SOURCE_OWNED"
        else:
            field_delta = np.nan
            pair_delta_defect = np.nan
            paths = ("TX_RECTANGLE", "YZ_RECTANGLE")
            completion = "LOCAL_OFFSHELL_ONLY"
        min_abs = float(min(np.min(np.abs(evp)), np.min(np.abs(evq)), abs(np.linalg.det(hp)), abs(np.linalg.det(hq))))
        atlas_rows.append({
            "sample_id": sample.sample_id,
            "geometry": sample.geometry,
            "lambda": f"{sample.lam:.8g}",
            "epsilon": f"{sample.eps:.8g}",
            "completion_scope": completion,
            "endpoint_atlas_defect": f"{defect:.17g}",
            "pair_regular_p": str(regp).upper(),
            "pair_regular_q": str(regq).upper(),
            "pair_min_abs_invariant": f"{min_abs:.17g}",
            "phi_pair_delta": f"{(phiq-phip):.17g}",
            "field_phi_delta": "NA" if np.isnan(field_delta) else f"{field_delta:.17g}",
            "r17_phi_identity_defect": "NA" if np.isnan(pair_delta_defect) else f"{pair_delta_defect:.17g}",
            "endpoint_family": "REGULAR" if regp and regq and defect <= 5e-10 else "NUMERIC_UNRESOLVED",
        })

        for causal in ("TIMELIKE", "SPACELIKE"):
            yend, steps = solve_geodesic(sample, causal, with_transport=True)
            x0 = initial_point(sample); v0 = initial_velocity(x0, sample, causal)
            x1, v1, P = yend[:4], yend[4:8], yend[8:].reshape(4, 4)
            n0 = float(v0 @ metric(x0, sample) @ v0)
            n1 = float(v1 @ metric(x1, sample) @ v1)
            metric_defect = float(np.linalg.norm(P.T @ metric(x1, sample) @ P - metric(x0, sample)))
            sv = dexp_singular_values(sample, causal)
            numeric_ok = abs(n1-n0) <= 5e-8 and metric_defect <= 5e-8
            geodesic_rows.append({
                "sample_id": sample.sample_id,
                "causal_class": causal,
                "affine_end": f"{AFFINE_END:.8g}",
                "solver_steps": str(steps),
                "initial_norm": f"{n0:.17g}",
                "final_norm": f"{n1:.17g}",
                "norm_drift": f"{abs(n1-n0):.17g}",
                "transport_metric_defect": f"{metric_defect:.17g}",
                "dexp_min_singular": f"{sv[-1]:.17g}",
                "dexp_max_singular": f"{sv[0]:.17g}",
                "endpoint_x": ";".join(f"{z:.17g}" for z in x1),
                "classification": "NEAR_CONJUGATE_OR_NUMERICALLY_UNRESOLVED" if sv[-1] < 1e-5 else ("REGULAR_PROPAGATOR" if numeric_ok else "NUMERIC_UNRESOLVED"),
            })

        for name in paths:
            P, angle, metric_defect, steps = integrate_loop(sample, name)
            path_rows.append({
                "sample_id": sample.sample_id,
                "path": name,
                "solver_steps": str(steps),
                "lc_holonomy_norm": f"{np.linalg.norm(P-np.eye(4)):.17g}",
                "lc_metric_defect": f"{metric_defect:.17g}",
                "normal_connection_angle": f"{angle:.17g}" if sample.geometry == "R17_GLOBAL" else "NA",
                "holonomy_matrix": ";".join(f"{z:.17g}" for z in P.ravel()),
                "classification": classify_holonomy(P) if metric_defect <= 5e-8 else "NUMERIC_UNRESOLVED",
            })

    write_tsv(HERE / "SOLVED_GEOMETRY_ATLAS.tsv", atlas_rows)
    write_tsv(HERE / "GEODESIC_DIAGNOSTICS.tsv", geodesic_rows)
    write_tsv(HERE / "PATH_DIAGNOSTICS.tsv", path_rows)
    result = {
        "schema": "UDT_SOLVED_GEOMETRY_SURVIVOR_ATLAS_V1",
        "status": "PRODUCTION_COMPLETE_INDEPENDENT_PENDING",
        "scope": "bounded_metric_geometry_not_physical_stability",
        "counts": {"samples": len(atlas_rows), "geodesics": len(geodesic_rows), "paths": len(path_rows)},
        "threshold_counts": {
            "endpoint_regular": sum(r["endpoint_family"] == "REGULAR" for r in atlas_rows),
            "regular_propagators": sum(r["classification"] == "REGULAR_PROPAGATOR" for r in geodesic_rows),
            "nonidentity_loops": sum(r["classification"] == "NONIDENTITY" for r in path_rows),
            "numeric_unresolved": sum("UNRESOLVED" in r["classification"] for r in geodesic_rows + path_rows),
        },
        "versions": {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__},
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    output_hashes = {p.name: sha256(p) for p in (HERE / "SOLVED_GEOMETRY_ATLAS.tsv", HERE / "GEODESIC_DIAGNOSTICS.tsv", HERE / "PATH_DIAGNOSTICS.tsv", HERE / "DERIVATION_RESULT.json")}
    print(json.dumps({"result": result, "sha256": output_hashes}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
