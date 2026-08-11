#!/usr/bin/env python3
"""Independent fixed-RK4/real-difference verifier for the common-query audit.

This file intentionally duplicates the two coframe formulas and does not import
the production evaluator.
"""

from __future__ import annotations

import csv
import json
from functools import lru_cache
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ETA = np.diag([-1.0, 1.0, 1.0, 1.0])
METRIC_D = 2.0e-5
SURFACE_D = 5.0e-4
CURV_D = 1.0e-3
RK_STEP = 5.0e-4


def fields_tl(x: np.ndarray, eps: float = 0.15):
    t, xx, y, z = x
    kappa = 0.035 * np.sin(t + 0.3 * y) + 0.018 * np.cos(xx - z) + eps * 0.025 * np.sin(t + xx + y)
    phi = 0.11 * np.cos(xx - 0.2 * t) + 0.025 * np.sin(y + z) + eps * 0.08 * np.cos(t - z + 0.4 * xx)
    beta = 0.12 * np.sin(t + xx) + 0.04 * np.cos(y - z) + eps * 0.05 * np.sin(t + y)
    gamma = 0.16 * np.sin(t - y + 0.2 * z) + eps * 0.04 * np.cos(xx + z)
    q1 = 0.045 * np.cos(t + y) + eps * 0.03 * np.sin(xx - z)
    q2 = -0.035 * np.sin(xx + z) + eps * 0.025 * np.cos(t - y)
    shear = 0.07 * np.sin(t + xx + y + z) + eps * 0.025 * np.cos(xx - y)
    S = np.array([
        [0.055 * np.cos(t + y) + eps * 0.02 * np.sin(z), 0.045 * np.sin(xx - z) + eps * 0.015 * np.cos(t + y)],
        [-0.04 * np.cos(t - xx + y) + eps * 0.02 * np.sin(xx + z), 0.05 * np.sin(t + z) + eps * 0.018 * np.cos(xx - y)],
    ])
    return kappa, phi, beta, gamma, q1, q2, shear, S


def coframe_tl(x: np.ndarray) -> np.ndarray:
    kappa, phi, beta, gamma, q1, q2, shear, S = fields_tl(x)
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


def phi_r17(x: np.ndarray, eps: float = 0.12) -> float:
    _, th, va, ps = x
    x1 = np.cos(th / 2) * np.cos((ps + va) / 2)
    x2 = np.cos(th / 2) * np.sin((ps + va) / 2)
    x3 = np.sin(th / 2) * np.cos((ps - va) / 2)
    x4 = np.sin(th / 2) * np.sin((ps - va) / 2)
    return float(0.12 * x1 + 0.08 * x2 * x3 - 0.05 * (x4 * x4 - x3 * x3) + eps * (0.11 * x4 + 0.07 * x1 * x2))


def coframe_r17(x: np.ndarray) -> np.ndarray:
    _, th, _, ps = x
    phi = phi_r17(x)
    u = np.exp(phi)
    v = np.exp(phi)
    s1 = 0.5 * np.array([0.0, np.cos(ps), np.sin(ps) * np.sin(th), 0.0])
    s2 = 0.5 * np.array([0.0, -np.sin(ps), np.cos(ps) * np.sin(th), 0.0])
    s3 = 0.5 * np.array([0.0, 0.0, np.cos(th), 1.0])
    dt = np.array([1.0, 0.0, 0.0, 0.0])
    return np.vstack(((dt + 0.4 * s3) / u, u * s3, v * s1, v * s2))


def coframe(x: np.ndarray, family: str) -> np.ndarray:
    return coframe_r17(x) if family == "R17" else coframe_tl(x)


def metric(x: np.ndarray, family: str) -> np.ndarray:
    E = coframe(x, family)
    return E.T @ ETA @ E


def gamma(x: np.ndarray, family: str) -> np.ndarray:
    g = metric(x, family)
    gi = np.linalg.inv(g)
    dg = np.empty((4, 4, 4))
    for k in range(4):
        dx = np.zeros(4); dx[k] = METRIC_D
        dg[k] = (metric(x + dx, family) - metric(x - dx, family)) / (2 * METRIC_D)
    G = np.zeros((4, 4, 4))
    for a in range(4):
        for b in range(4):
            for c in range(4):
                G[a, b, c] = 0.5 * sum(gi[a, d] * (dg[b, d, c] + dg[c, d, b] - dg[d, b, c]) for d in range(4))
    return G


def riemann(x: np.ndarray, family: str) -> np.ndarray:
    G = gamma(x, family)
    dG = np.empty((4, 4, 4, 4))
    for k in range(4):
        dx = np.zeros(4); dx[k] = CURV_D
        dG[k] = (gamma(x + dx, family) - gamma(x - dx, family)) / (2 * CURV_D)
    R = np.zeros((4, 4, 4, 4))
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    R[a, b, c, d] = dG[c, a, d, b] - dG[d, a, c, b]
                    R[a, b, c, d] += sum(G[a, c, e] * G[e, d, b] - G[a, d, e] * G[e, c, b] for e in range(4))
    return R


def rk4(rhs, end: float, state: np.ndarray) -> np.ndarray:
    if end == 0:
        return state.copy()
    steps = max(1, int(np.ceil(abs(end) / RK_STEP)))
    h = end / steps
    y = state.copy()
    t = 0.0
    for _ in range(steps):
        k1 = rhs(t, y)
        k2 = rhs(t + h / 2, y + h * k1 / 2)
        k3 = rhs(t + h / 2, y + h * k2 / 2)
        k4 = rhs(t + h, y + h * k3)
        y += h * (k1 + 2 * k2 + 2 * k3 + k4) / 6
        t += h
    return y


class Surface:
    family: str

    @lru_cache(maxsize=None)
    def point(self, y: float, s: float) -> np.ndarray:
        raise NotImplementedError

    def tangents(self, q: np.ndarray) -> np.ndarray:
        cols = []
        for axis in range(2):
            dq = np.zeros(2); dq[axis] = SURFACE_D
            cols.append((self.point(*(q + dq)) - self.point(*(q - dq))) / (2 * SURFACE_D))
        return np.column_stack(cols)


class R17Surface(Surface):
    family = "R17"

    @lru_cache(maxsize=None)
    def point(self, y: float, s: float) -> np.ndarray:
        return np.array([0.07 + y, 1.08, 0.31, 0.44 + 2 * s])

    def tangents(self, q: np.ndarray) -> np.ndarray:
        del q
        return np.array([[1.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 2.0]])


class TLSurface(Surface):
    family = "TL"

    def __init__(self) -> None:
        self.x0 = np.array([0.12, -0.18, 0.23, -0.14])
        frame = np.linalg.inv(coframe_tl(self.x0))
        self.u0, self.n0 = frame[:, 0], frame[:, 1]

    @lru_cache(maxsize=None)
    def observer(self, y: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        state0 = np.concatenate((self.x0, self.u0, self.n0))

        def rhs(_, state):
            x, u, n = state[:4], state[4:8], state[8:12]
            G = gamma(x, "TL")
            return np.concatenate((u, -np.einsum("abc,b,c->a", G, u, u), -np.einsum("abc,b,c->a", G, u, n)))

        out = rk4(rhs, y, state0)
        return out[:4], out[4:8], out[8:12]

    @lru_cache(maxsize=None)
    def point(self, y: float, s: float) -> np.ndarray:
        x, _, n = self.observer(y)

        def rhs(_, state):
            xx, v = state[:4], state[4:8]
            G = gamma(xx, "TL")
            return np.concatenate((v, -np.einsum("abc,b,c->a", G, v, v)))

        return rk4(rhs, s, np.concatenate((x, n)))[:4]


def normal_frame(x: np.ndarray, J: np.ndarray, g: np.ndarray, family: str) -> tuple[np.ndarray, np.ndarray]:
    h = J.T @ g @ J
    PN = np.eye(4) - J @ np.linalg.inv(h) @ J.T @ g
    frame = np.linalg.inv(coframe(x, family))
    n0 = PN @ frame[:, 2]; n0 /= np.sqrt(n0 @ g @ n0)
    n1 = PN @ frame[:, 3]; n1 -= n0 * (n0 @ g @ n1); n1 /= np.sqrt(n1 @ g @ n1)
    return np.column_stack((n0, n1)), PN


def geometry(surface: Surface, q: np.ndarray) -> dict:
    x = surface.point(*q)
    g = metric(x, surface.family)
    J = surface.tangents(q)
    h = J.T @ g @ J
    F0 = x
    F2 = np.empty((4, 2, 2))
    for i in range(2):
        dq = np.zeros(2); dq[i] = SURFACE_D
        F2[:, i, i] = (surface.point(*(q + dq)) - 2 * F0 + surface.point(*(q - dq))) / SURFACE_D**2
    d0 = np.array([SURFACE_D, 0.0]); d1 = np.array([0.0, SURFACE_D])
    mixed = (surface.point(*(q + d0 + d1)) - surface.point(*(q + d0 - d1)) - surface.point(*(q - d0 + d1)) + surface.point(*(q - d0 - d1))) / (4 * SURFACE_D**2)
    F2[:, 0, 1] = mixed; F2[:, 1, 0] = mixed
    G = gamma(x, surface.family)
    cov2 = np.empty_like(F2)
    for i in range(2):
        for j in range(2):
            cov2[:, i, j] = F2[:, i, j] + np.einsum("abc,b,c->a", G, J[:, i], J[:, j])
    N, PN = normal_frame(x, J, g, surface.family)
    IIvec = np.einsum("ab,bij->aij", PN, cov2)
    ii = np.einsum("aij,ab,bA->Aij", IIvec, g, N)
    return {"x": x, "g": g, "J": J, "h": h, "G": G, "N": N, "PN": PN, "cov2": cov2, "ii": ii}


def intrinsic_christoffel(surface: Surface, q: np.ndarray, d: float) -> np.ndarray:
    h = geometry(surface, q)["h"]
    hi = np.linalg.inv(h)
    dh = np.empty((2, 2, 2))
    for k in range(2):
        dq = np.zeros(2); dq[k] = d
        dh[k] = (geometry(surface, q + dq)["h"] - geometry(surface, q - dq)["h"]) / (2 * d)
    G = np.zeros((2, 2, 2))
    for a in range(2):
        for b in range(2):
            for c in range(2):
                G[a, b, c] = 0.5 * sum(hi[a, e] * (dh[b, e, c] + dh[c, e, b] - dh[e, b, c]) for e in range(2))
    return G


def gauss_residual(surface: Surface, d: float = 4e-3) -> tuple[float, dict]:
    q = np.zeros(2)
    geom = geometry(surface, q)
    h, J, g, ii = geom["h"], geom["J"], geom["g"], geom["ii"]
    RA = riemann(geom["x"], surface.family)
    G = intrinsic_christoffel(surface, q, d / 2)
    dG = np.empty((2, 2, 2, 2))
    for k in range(2):
        dq = np.zeros(2); dq[k] = d
        dG[k] = (intrinsic_christoffel(surface, q + dq, d / 2) - intrinsic_christoffel(surface, q - dq, d / 2)) / (2 * d)
    RI = np.zeros((2, 2, 2, 2))
    for a in range(2):
        for b in range(2):
            for c in range(2):
                for e in range(2):
                    RI[a, b, c, e] = dG[c, a, e, b] - dG[e, a, c, b] + sum(G[a, c, m] * G[m, e, b] - G[a, e, m] * G[m, c, b] for m in range(2))
    Rvec = np.einsum("abcd,b,c,d->a", RA, J[:, 1], J[:, 0], J[:, 1])
    ambient = J[:, 0] @ g @ Rvec
    intrinsic = sum(h[0, a] * RI[a, 1, 0, 1] for a in range(2))
    extrinsic = np.dot(ii[:, 0, 0], ii[:, 1, 1]) - np.dot(ii[:, 0, 1], ii[:, 1, 0])
    return float(abs(ambient - intrinsic + extrinsic)), geom


def normal_connection(surface: Surface, q: np.ndarray, d: float = 1e-3) -> np.ndarray:
    geom = geometry(surface, q)
    omega = np.empty((2, 2, 2))
    for i in range(2):
        dq = np.zeros(2); dq[i] = d
        dN = (geometry(surface, q + dq)["N"] - geometry(surface, q - dq)["N"]) / (2 * d)
        for A in range(2):
            for B in range(2):
                cov = dN[:, B] + np.einsum("abc,b,c->a", geom["G"], geom["J"][:, i], geom["N"][:, B])
                omega[i, A, B] = geom["N"][:, A] @ geom["g"] @ cov
    return omega


def normal_curvature(surface: Surface, d: float = 2e-3) -> np.ndarray:
    q = np.zeros(2)
    omega = normal_connection(surface, q)
    deriv = []
    for axis in range(2):
        dq = np.zeros(2); dq[axis] = d
        deriv.append((normal_connection(surface, q + dq) - normal_connection(surface, q - dq)) / (2 * d))
    return deriv[0][1] - deriv[1][0] + omega[0] @ omega[1] - omega[1] @ omega[0]


def jacobi_balance(surface: TLSurface, d: float = 2e-3) -> tuple[float, float, float]:
    def J_at(s: float) -> np.ndarray:
        return surface.tangents(np.array([0.0, s]))[:, 0]

    def v_at(s: float) -> np.ndarray:
        return surface.tangents(np.array([0.0, s]))[:, 1]

    def DJ_at(s: float) -> np.ndarray:
        q = np.array([0.0, s])
        x = surface.point(*q)
        return (J_at(s + d) - J_at(s - d)) / (2 * d) + np.einsum("abc,b,c->a", gamma(x, "TL"), v_at(s), J_at(s))

    x0 = surface.point(0.0, 0.0)
    v0, J0 = v_at(0.0), J_at(0.0)
    cov2 = (DJ_at(d) - DJ_at(-d)) / (2 * d) + np.einsum("abc,b,c->a", gamma(x0, "TL"), v0, DJ_at(0.0))
    Rjvv = np.einsum("abcd,b,c,d->a", riemann(x0, "TL"), v0, J0, v0)
    residual = np.linalg.norm(cov2 + Rjvv)
    scale = max(np.linalg.norm(cov2), np.linalg.norm(Rjvv))
    return float(residual), float(scale), float(residual / scale)


def read_smallest_loops() -> dict[str, dict[str, float]]:
    rows = list(csv.DictReader((HERE / "LOOP_DIAGNOSTICS.tsv").open(), delimiter="\t"))
    out = {}
    for query in ("Q1_R17_LEAF", "Q2_TL_FERMI"):
        row = min((r for r in rows if r["query_id"] == query), key=lambda r: float(r["halfwidth"]))
        out[query] = {k: float(row[k]) for k in ("area", "ambient_holonomy_norm", "normal_holonomy_norm")}
    return out


def plane_cylinder_control() -> tuple[float, float, float]:
    s, radius = 0.37, 1.7
    hp = np.diag([-1.0, 1.0])
    J = np.column_stack((np.array([1.0, 0.0, 0.0, 0.0]), np.array([0.0, -np.sin(s / radius), np.cos(s / radius), 0.0])))
    hc = J.T @ ETA @ J
    ii = -1 / radius
    return float(np.linalg.norm(hp - hc)), 0.0, float(ii)


def main() -> None:
    r17, tl = R17Surface(), TLSurface()
    loops = read_smallest_loops()
    results = {}
    passed = []
    for surface, query in ((r17, "Q1_R17_LEAF"), (tl, "Q2_TL_FERMI")):
        gauss, geom = gauss_residual(surface)
        h = geom["h"]
        det = np.linalg.det(h)
        T2 = -h[0, 0]; beta = h[0, 1] / h[0, 0]; L2 = h[1, 1] - h[0, 1] ** 2 / h[0, 0]
        hrec = np.array([[-T2, -T2 * beta], [-T2 * beta, -T2 * beta**2 + L2]])
        phi_pair = 0.25 * np.log((-det) / h[0, 0] ** 2)
        acceleration = np.linalg.norm(geom["cov2"][:, 1, 1])
        RA = riemann(geom["x"], surface.family)
        Rop = np.einsum("abcd,c,d->ab", RA, geom["J"][:, 0], geom["J"][:, 1])
        Rperp = normal_curvature(surface)
        loop = loops[query]
        ambient_rate = loop["ambient_holonomy_norm"] / loop["area"]
        normal_rate = loop["normal_holonomy_norm"] / loop["area"]
        amb_rel = abs(ambient_rate - np.linalg.norm(Rop)) / max(np.linalg.norm(Rop), 1e-15)
        normal_rel = abs(normal_rate - np.linalg.norm(Rperp)) / max(np.linalg.norm(Rperp), 1e-15)
        row = {
            "regular": bool(h[0, 0] < 0 and det < 0 and np.linalg.matrix_rank(geom["J"]) == 2),
            "det_h": float(det),
            "phi_pair": float(phi_pair),
            "h_reconstruction_residual": float(np.linalg.norm(hrec - h)),
            "s_ruling_acceleration_norm": float(acceleration),
            "gauss_residual": gauss,
            "ambient_generator_norm": float(np.linalg.norm(Rop)),
            "ambient_loop_rate": float(ambient_rate),
            "ambient_loop_relative_error": float(amb_rel),
            "normal_generator_norm": float(np.linalg.norm(Rperp)),
            "normal_loop_rate": float(normal_rate),
            "normal_loop_relative_error": float(normal_rel),
        }
        if query == "Q1_R17_LEAF":
            row["r17_phi_identity_defect"] = float(abs(phi_pair - phi_r17(geom["x"])))
            passed += [row["r17_phi_identity_defect"] < 1e-7, acceleration > 1e-4]
        else:
            jr, js, jrel = jacobi_balance(tl)
            row.update({"jacobi_residual": jr, "jacobi_term_scale": js, "jacobi_relative_residual": jrel})
            passed += [acceleration < 1e-5, jrel < 5e-3]
        passed += [row["regular"], row["h_reconstruction_residual"] < 1e-7, gauss < 5e-4, amb_rel < 0.15, normal_rel < 0.15]
        results[query] = row

    equal_h, plane_ii, cylinder_ii = plane_cylinder_control()
    control = {"equal_h_residual": equal_h, "plane_ii": plane_ii, "cylinder_ii": cylinder_ii}
    passed += [equal_h < 1e-12, abs(plane_ii - cylinder_ii) > 1e-3]
    verdict = "VERIFIED_WITH_CAVEATS" if all(passed) else "REFUTED_OR_UNRESOLVED"
    output = {
        "schema": "UDT_COMMON_QUERY_INDEPENDENT_V1",
        "method": "fixed_RK4_real_finite_difference_no_production_import",
        "verdict": verdict,
        "passed_gate_count": int(sum(bool(x) for x in passed)),
        "total_gate_count": len(passed),
        "queries": results,
        "plane_cylinder_control": control,
        "caveat": "Q2 Codazzi convergence is not certified by this verifier",
    }
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps(output, indent=2, sort_keys=True))
    if verdict != "VERIFIED_WITH_CAVEATS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
