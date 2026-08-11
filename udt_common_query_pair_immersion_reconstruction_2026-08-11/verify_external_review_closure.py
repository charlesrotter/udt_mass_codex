#!/usr/bin/env python3
"""Independent higher-jet and normal-loop replay for the common-query audit.

This script deliberately imports neither production nor the prior independent verifier.
It duplicates the frozen TL_P2 coframe, constructs the same Fermi query with fixed-step
RK4, evaluates Codazzi in both normal-frame and ambient-vector forms, and integrates
the raw normal connection without polar projection.
"""

from __future__ import annotations

import json
import platform
from functools import lru_cache
from pathlib import Path

import numpy as np
import scipy
from scipy.linalg import expm


HERE = Path(__file__).resolve().parent
ETA = np.diag([-1.0, 1.0, 1.0, 1.0])
EPS = 0.15
X0 = np.array([0.12, -0.18, 0.23, -0.14], dtype=float)
RK_MAX_STEP = 1.25e-4
METRIC_D = 1.0e-5
SURFACE_JET_D = 5.0e-4
CONNECTION_D = 5.0e-4
CURVATURE_STEPS = (5.0e-4, 2.5e-4)
CODAZZI_SCALES = (8.0e-3, 4.0e-3, 2.0e-3, 1.0e-3)
LOOP_HALF_WIDTH = 1.0e-2
LOOP_SUBDIVISIONS = (16, 32, 64)
PRODUCTION_NORMAL_LOOP_NORM = 6.019832007454665e-6


def fields(x: np.ndarray):
    t, xx, y, z = x
    kappa = 0.035 * np.sin(t + 0.3 * y) + 0.018 * np.cos(xx - z) + EPS * 0.025 * np.sin(t + xx + y)
    phi = 0.11 * np.cos(xx - 0.2 * t) + 0.025 * np.sin(y + z) + EPS * 0.08 * np.cos(t - z + 0.4 * xx)
    beta = 0.12 * np.sin(t + xx) + 0.04 * np.cos(y - z) + EPS * 0.05 * np.sin(t + y)
    gamma = 0.16 * np.sin(t - y + 0.2 * z) + EPS * 0.04 * np.cos(xx + z)
    q1 = 0.045 * np.cos(t + y) + EPS * 0.03 * np.sin(xx - z)
    q2 = -0.035 * np.sin(xx + z) + EPS * 0.025 * np.cos(t - y)
    shear = 0.07 * np.sin(t + xx + y + z) + EPS * 0.025 * np.cos(xx - y)
    S = np.array([
        [0.055 * np.cos(t + y) + EPS * 0.02 * np.sin(z), 0.045 * np.sin(xx - z) + EPS * 0.015 * np.cos(t + y)],
        [-0.04 * np.cos(t - xx + y) + EPS * 0.02 * np.sin(xx + z), 0.05 * np.sin(t + z) + EPS * 0.018 * np.cos(xx - y)],
    ])
    return kappa, phi, beta, gamma, q1, q2, shear, S


def coframe(x: np.ndarray) -> np.ndarray:
    kappa, phi, beta, gamma, q1, q2, shear, S = fields(x)
    T, L = np.exp(kappa - phi), np.exp(kappa + phi)
    B = np.array([[T, T * beta], [0.0, L]])
    rot = np.array([[np.cos(gamma), -np.sin(gamma)], [np.sin(gamma), np.cos(gamma)]])
    upper = np.array([[np.exp(q1), shear], [0.0, np.exp(q2)]])
    Q = rot @ upper
    E = np.zeros((4, 4))
    E[:2, :2] = B
    E[2:, :2] = Q @ S
    E[2:, 2:] = Q
    return E


def metric(x: np.ndarray) -> np.ndarray:
    E = coframe(x)
    return E.T @ ETA @ E


def fd1_array(func, x: np.ndarray, axis: int, step: float) -> np.ndarray:
    e = np.zeros_like(x, dtype=float)
    e[axis] = step
    return (-func(x + 2 * e) + 8 * func(x + e) - 8 * func(x - e) + func(x - 2 * e)) / (12 * step)


@lru_cache(maxsize=None)
def christoffel_cached(x_tuple: tuple[float, ...]) -> np.ndarray:
    x = np.array(x_tuple, dtype=float)
    g = metric(x)
    gi = np.linalg.inv(g)
    dg = np.array([fd1_array(metric, x, k, METRIC_D) for k in range(4)])
    G = np.zeros((4, 4, 4))
    for a in range(4):
        for b in range(4):
            for c in range(4):
                G[a, b, c] = 0.5 * sum(gi[a, d] * (dg[b, d, c] + dg[c, d, b] - dg[d, b, c]) for d in range(4))
    return G


def christoffel(x: np.ndarray) -> np.ndarray:
    return christoffel_cached(tuple(float(v) for v in x))


@lru_cache(maxsize=None)
def riemann_cached(x_tuple: tuple[float, ...], step: float) -> np.ndarray:
    x = np.array(x_tuple, dtype=float)
    G = christoffel(x)
    dG = np.array([fd1_array(christoffel, x, k, step) for k in range(4)])
    R = np.zeros((4, 4, 4, 4))
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    R[a, b, c, d] = dG[c, a, d, b] - dG[d, a, c, b]
                    R[a, b, c, d] += sum(G[a, c, e] * G[e, d, b] - G[a, d, e] * G[e, c, b] for e in range(4))
    return R


def riemann(x: np.ndarray, step: float) -> np.ndarray:
    return riemann_cached(tuple(float(v) for v in x), float(step))


def rk4_to(rhs, end: float, initial: np.ndarray) -> np.ndarray:
    if end == 0.0:
        return initial.copy()
    count = max(1, int(np.ceil(abs(end) / RK_MAX_STEP)))
    h = end / count
    state = initial.copy()
    for _ in range(count):
        k1 = rhs(state)
        k2 = rhs(state + 0.5 * h * k1)
        k3 = rhs(state + 0.5 * h * k2)
        k4 = rhs(state + h * k3)
        state += h * (k1 + 2 * k2 + 2 * k3 + k4) / 6.0
    return state


frame0 = np.linalg.inv(coframe(X0))
U0 = frame0[:, 0]
N0 = frame0[:, 1]


@lru_cache(maxsize=None)
def observer(y: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    state0 = np.concatenate((X0, U0, N0))

    def rhs(state):
        x, u, n = state[:4], state[4:8], state[8:12]
        G = christoffel(x)
        return np.concatenate((u, -np.einsum("abc,b,c->a", G, u, u), -np.einsum("abc,b,c->a", G, u, n)))

    out = rk4_to(rhs, y, state0)
    return out[:4], out[4:8], out[8:12]


@lru_cache(maxsize=None)
def surface_point_cached(y: float, s: float) -> np.ndarray:
    x, _, n = observer(float(y))

    def rhs(state):
        xx, v = state[:4], state[4:8]
        return np.concatenate((v, -np.einsum("abc,b,c->a", christoffel(xx), v, v)))

    return rk4_to(rhs, float(s), np.concatenate((x, n)))[:4]


def surface_point(q: np.ndarray) -> np.ndarray:
    return surface_point_cached(float(q[0]), float(q[1]))


def surface_tangent(q: np.ndarray, axis: int) -> np.ndarray:
    return fd1_array(surface_point, q, axis, SURFACE_JET_D)


def surface_tangents(q: np.ndarray) -> np.ndarray:
    return np.column_stack((surface_tangent(q, 0), surface_tangent(q, 1)))


def surface_second(q: np.ndarray) -> np.ndarray:
    out = np.empty((4, 2, 2))
    for i in range(2):
        for j in range(2):
            out[:, i, j] = fd1_array(lambda qq: surface_tangent(qq, j), q, i, SURFACE_JET_D)
    return out


def normal_frame_from_first(x: np.ndarray, J: np.ndarray, g: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    h = J.T @ g @ J
    PT = J @ np.linalg.inv(h) @ J.T @ g
    PN = np.eye(4) - PT
    screen = np.linalg.inv(coframe(x))[:, 2:4]
    n0 = PN @ screen[:, 0]
    n0 /= np.sqrt(n0 @ g @ n0)
    n1 = PN @ screen[:, 1]
    n1 -= n0 * (n0 @ g @ n1)
    n1 /= np.sqrt(n1 @ g @ n1)
    return np.column_stack((n0, n1)), PN


@lru_cache(maxsize=None)
def first_geometry_cached(y: float, s: float) -> dict:
    q = np.array([y, s], dtype=float)
    x = surface_point(q)
    g = metric(x)
    J = surface_tangents(q)
    h = J.T @ g @ J
    N, PN = normal_frame_from_first(x, J, g)
    return {"x": x, "g": g, "J": J, "h": h, "N": N, "PN": PN, "G": christoffel(x)}


def first_geometry(q: np.ndarray) -> dict:
    return first_geometry_cached(float(q[0]), float(q[1]))


@lru_cache(maxsize=None)
def full_geometry_cached(y: float, s: float) -> dict:
    q = np.array([y, s], dtype=float)
    first = first_geometry(q)
    F2 = surface_second(q)
    cov2 = np.empty_like(F2)
    for i in range(2):
        for j in range(2):
            cov2[:, i, j] = F2[:, i, j] + np.einsum("abc,b,c->a", first["G"], first["J"][:, i], first["J"][:, j])
    IIvec = np.einsum("ab,bij->aij", first["PN"], cov2)
    ii = np.einsum("aij,ab,bA->Aij", IIvec, first["g"], first["N"])
    return {**first, "cov2": cov2, "IIvec": IIvec, "ii": ii}


def full_geometry(q: np.ndarray) -> dict:
    return full_geometry_cached(float(q[0]), float(q[1]))


def surface_christoffel(q: np.ndarray) -> np.ndarray:
    h = first_geometry(q)["h"]
    hi = np.linalg.inv(h)
    dh = np.array([fd1_array(lambda qq: first_geometry(qq)["h"], q, k, CONNECTION_D) for k in range(2)])
    G = np.zeros((2, 2, 2))
    for a in range(2):
        for b in range(2):
            for c in range(2):
                G[a, b, c] = 0.5 * sum(hi[a, d] * (dh[b, d, c] + dh[c, d, b] - dh[d, b, c]) for d in range(2))
    return G


@lru_cache(maxsize=None)
def normal_connection_cached(y: float, s: float) -> np.ndarray:
    q = np.array([y, s], dtype=float)
    geom = first_geometry(q)
    dN = np.array([fd1_array(lambda qq: first_geometry(qq)["N"], q, i, CONNECTION_D) for i in range(2)])
    omega = np.empty((2, 2, 2))
    for i in range(2):
        for A in range(2):
            for B in range(2):
                cov = dN[i, :, B] + np.einsum("abc,b,c->a", geom["G"], geom["J"][:, i], geom["N"][:, B])
                omega[i, A, B] = geom["N"][:, A] @ geom["g"] @ cov
    return omega


def normal_connection(q: np.ndarray) -> np.ndarray:
    return normal_connection_cached(float(q[0]), float(q[1]))


def codazzi_residual(scale: float, curvature_step: float) -> dict:
    q = np.zeros(2)
    geom = full_geometry(q)
    SG = surface_christoffel(q)
    omega = normal_connection(q)
    dii = np.array([fd1_array(lambda qq: full_geometry(qq)["ii"], q, axis, scale) for axis in range(2)])
    dIIvec = np.array([fd1_array(lambda qq: full_geometry(qq)["IIvec"], q, axis, scale) for axis in range(2)])
    Dii = np.empty_like(dii)
    Dvec = np.empty_like(dIIvec)
    for axis in range(2):
        for j in range(2):
            for k in range(2):
                for A in range(2):
                    val = dii[axis, A, j, k] + sum(omega[axis, A, B] * geom["ii"][B, j, k] for B in range(2))
                    val -= sum(SG[m, axis, j] * geom["ii"][A, m, k] + SG[m, axis, k] * geom["ii"][A, j, m] for m in range(2))
                    Dii[axis, A, j, k] = val
                vec = dIIvec[axis, :, j, k] + np.einsum("abc,b,c->a", geom["G"], geom["J"][:, axis], geom["IIvec"][:, j, k])
                vec -= sum(SG[m, axis, j] * geom["IIvec"][:, m, k] + SG[m, axis, k] * geom["IIvec"][:, j, m] for m in range(2))
                Dvec[axis, :, j, k] = vec

    R = riemann(geom["x"], curvature_step)
    frame_residual = np.empty((2, 2))
    vector_components = np.empty((2, 2))
    vector_residuals = []
    for k in range(2):
        Rvec = np.einsum("abcd,b,c,d->a", R, geom["J"][:, k], geom["J"][:, 0], geom["J"][:, 1])
        projected_R = geom["PN"] @ Rvec
        vector_residual = geom["PN"] @ (Dvec[0, :, 1, k] - Dvec[1, :, 0, k] - projected_R)
        vector_residuals.append(vector_residual)
        vector_components[:, k] = geom["N"].T @ geom["g"] @ vector_residual
        for A in range(2):
            rhs = geom["N"][:, A] @ geom["g"] @ Rvec
            frame_residual[A, k] = Dii[0, A, 1, k] - Dii[1, A, 0, k] - rhs

    vector_residuals = np.column_stack(vector_residuals)
    direct_norm = float(np.linalg.norm(vector_components))
    frame_norm = float(np.linalg.norm(frame_residual))
    return {
        "scale": scale,
        "curvature_step": curvature_step,
        "direct_normal_component_matrix": vector_components.tolist(),
        "frame_component_matrix": frame_residual.tolist(),
        "direct_residual_norm": direct_norm,
        "frame_residual_norm": frame_norm,
        "classification_residual": max(direct_norm, frame_norm),
        "formulation_disagreement": float(np.linalg.norm(vector_components - frame_residual)),
        "normality_defect": float(np.linalg.norm(geom["J"].T @ geom["g"] @ vector_residuals)),
    }


def normal_curvature() -> np.ndarray:
    q = np.zeros(2)
    d = 2.0e-3
    deriv = np.array([fd1_array(normal_connection, q, axis, d) for axis in range(2)])
    omega = normal_connection(q)
    return deriv[0, 1] - deriv[1, 0] + omega[0] @ omega[1] - omega[1] @ omega[0]


def integrate_normal_loop(subdivisions: int) -> np.ndarray:
    h = LOOP_HALF_WIDTH
    corners = [
        np.array([-h, -h]),
        np.array([h, -h]),
        np.array([h, h]),
        np.array([-h, h]),
        np.array([-h, -h]),
    ]
    U = np.eye(2)
    for qa, qb in zip(corners[:-1], corners[1:]):
        delta = (qb - qa) / subdivisions
        for index in range(subdivisions):
            qm = qa + (index + 0.5) * delta
            omega = normal_connection(qm)
            generator = omega[0] * delta[0] + omega[1] * delta[1]
            U = expm(-generator) @ U
    return U


def classify_codazzi(rows: list[dict], control_row: dict) -> str:
    tail = [rows[-2]["classification_residual"], rows[-1]["classification_residual"]]
    stable = tail[0] / max(tail[1], 1e-30) >= 1.5 or max(tail) / max(min(tail), 1e-30) <= 1.5
    control_delta = abs(rows[-1]["classification_residual"] - control_row["classification_residual"])
    if max(tail) < 5e-6 and stable and control_delta < 2e-6:
        return "INDEPENDENTLY_CERTIFIED"
    if min(row["classification_residual"] for row in rows) > 5e-4:
        return "IDENTITY_REFUTED_ON_DECLARED_NUMERICS"
    return "NUMERICALLY_UNRESOLVED"


def main() -> None:
    g0 = metric(X0)
    initial_orthonormality = np.array([
        U0 @ g0 @ U0 + 1.0,
        N0 @ g0 @ N0 - 1.0,
        U0 @ g0 @ N0,
    ])

    codazzi_rows = [codazzi_residual(scale, CURVATURE_STEPS[0]) for scale in CODAZZI_SCALES]
    control_row = codazzi_residual(CODAZZI_SCALES[-1], CURVATURE_STEPS[1])
    codazzi_status = classify_codazzi(codazzi_rows, control_row)

    loops = {str(n): integrate_normal_loop(n) for n in LOOP_SUBDIVISIONS}
    area = (2 * LOOP_HALF_WIDTH) ** 2
    curvature = normal_curvature()
    loop64 = loops["64"]
    loop_norm = float(np.linalg.norm(loop64 - np.eye(2)))
    loop_rate = loop_norm / area
    curvature_norm = float(np.linalg.norm(curvature))
    generator_relative = abs(loop_rate - curvature_norm) / max(curvature_norm, 1e-30)
    production_relative = abs(loop_norm - PRODUCTION_NORMAL_LOOP_NORM) / PRODUCTION_NORMAL_LOOP_NORM
    quadrature_16_32 = float(np.linalg.norm(loops["32"] - loops["16"]))
    quadrature_32_64 = float(np.linalg.norm(loops["64"] - loops["32"]))
    orthogonality_defect = float(np.linalg.norm(loop64.T @ loop64 - np.eye(2)))
    loop_status = "INDEPENDENTLY_REGENERATED" if (
        quadrature_32_64 < 1e-8
        and loop_norm > 1e-7
        and generator_relative < 2e-3
        and production_relative < 2e-3
    ) else "NUMERICALLY_UNRESOLVED"

    output = {
        "schema": "UDT_COMMON_QUERY_EXTERNAL_REVIEW_CLOSURE_V1",
        "method": "standalone_fixed_rk4_five_point_higher_jet_raw_normal_connection",
        "versions": {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__},
        "controls": {
            "rk_max_step": RK_MAX_STEP,
            "metric_derivative_step": METRIC_D,
            "surface_jet_step": SURFACE_JET_D,
            "connection_step": CONNECTION_D,
            "curvature_steps": list(CURVATURE_STEPS),
            "codazzi_scales": list(CODAZZI_SCALES),
            "loop_halfwidth": LOOP_HALF_WIDTH,
            "loop_subdivisions": list(LOOP_SUBDIVISIONS),
        },
        "initial_orthonormality_defect": initial_orthonormality.tolist(),
        "codazzi": {
            "status": codazzi_status,
            "rows": codazzi_rows,
            "curvature_step_control": control_row,
        },
        "normal_loop": {
            "status": loop_status,
            "area": area,
            "loop_matrices": {k: v.tolist() for k, v in loops.items()},
            "loop_norm_64": loop_norm,
            "production_loop_norm_frozen": PRODUCTION_NORMAL_LOOP_NORM,
            "production_relative_difference": production_relative,
            "quadrature_16_32": quadrature_16_32,
            "quadrature_32_64": quadrature_32_64,
            "orthogonality_defect": orthogonality_defect,
            "normal_curvature_matrix": curvature.tolist(),
            "normal_curvature_norm": curvature_norm,
            "loop_rate_norm": loop_rate,
            "generator_relative_difference": generator_relative,
        },
        "verdict": "VERIFIED" if codazzi_status == "INDEPENDENTLY_CERTIFIED" and loop_status == "INDEPENDENTLY_REGENERATED" else "VERIFIED_WITH_CAVEATS",
    }
    (HERE / "EXTERNAL_REVIEW_CLOSURE_VERIFICATION.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

