#!/usr/bin/env python3
"""Bounded common-query pair-immersion reconstruction.

This is a metric-geometry calculation.  It does not solve a field equation and
does not select a physical observer query.  The two queries and every numerical
control are frozen in PREREGISTRATION.md and PREMISE_LEDGER.tsv.
"""

from __future__ import annotations

import csv
import json
import platform
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import numpy as np
import scipy
from scipy.integrate import solve_ivp
from scipy.linalg import expm


HERE = Path(__file__).resolve().parent
ETA = np.diag([-1.0, 1.0, 1.0, 1.0])
CS_H = 1.0e-30
RTOL = 1.0e-11
ATOL = 1.0e-13
MAX_STEP = 2.5e-3
SURFACE_D = 2.0e-5
SCALES = (4.0e-3, 2.0e-3, 1.0e-3)
LOOP_HALF_WIDTHS = (4.0e-2, 2.0e-2, 1.0e-2)


@dataclass(frozen=True)
class Witness:
    query_id: str
    geometry: str
    lam: float
    eps: float
    twist: float = 0.4


R17 = Witness("Q1_R17_LEAF", "R17_GLOBAL", 1.0, 0.12)
TL = Witness("Q2_TL_FERMI", "TIMELIVE_LOCAL", 0.0, 0.15)


def r17_phi(x: np.ndarray, eps: float):
    _, th, va, ps = x
    x1 = np.cos(th / 2) * np.cos((ps + va) / 2)
    x2 = np.cos(th / 2) * np.sin((ps + va) / 2)
    x3 = np.sin(th / 2) * np.cos((ps - va) / 2)
    x4 = np.sin(th / 2) * np.sin((ps - va) / 2)
    return 0.12 * x1 + 0.08 * x2 * x3 - 0.05 * (x4 * x4 - x3 * x3) + eps * (0.11 * x4 + 0.07 * x1 * x2)


def r17_coframe(x: np.ndarray, witness: Witness) -> np.ndarray:
    _, th, _, ps = x
    phi = r17_phi(x, witness.eps)
    u = np.exp(phi)
    v = np.exp(witness.lam * phi)
    s1 = 0.5 * np.array([0, np.cos(ps), np.sin(ps) * np.sin(th), 0], dtype=x.dtype)
    s2 = 0.5 * np.array([0, -np.sin(ps), np.cos(ps) * np.sin(th), 0], dtype=x.dtype)
    s3 = 0.5 * np.array([0, 0, np.cos(th), 1], dtype=x.dtype)
    dt = np.array([1, 0, 0, 0], dtype=x.dtype)
    return np.vstack(((dt + witness.twist * s3) / u, u * s3, v * s1, v * s2))


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


def timelive_coframe(x: np.ndarray, witness: Witness) -> np.ndarray:
    kappa, phi, beta, gamma, q1, q2, shear, S = timelive_fields(x, witness.eps)
    T = np.exp(kappa - phi)
    L = np.exp(kappa + phi)
    B = np.array([[T, T * beta], [0, L]], dtype=x.dtype)
    rot = np.array([[np.cos(gamma), -np.sin(gamma)], [np.sin(gamma), np.cos(gamma)]], dtype=x.dtype)
    upper = np.array([[np.exp(q1), shear], [0, np.exp(q2)]], dtype=x.dtype)
    Q = rot @ upper
    E = np.zeros((4, 4), dtype=x.dtype)
    E[:2, :2] = B
    E[2:, :2] = Q @ S
    E[2:, 2:] = Q
    return E


def coframe(x: np.ndarray, witness: Witness) -> np.ndarray:
    return r17_coframe(x, witness) if witness.geometry == "R17_GLOBAL" else timelive_coframe(x, witness)


def metric(x: np.ndarray, witness: Witness) -> np.ndarray:
    E = coframe(x, witness)
    return E.T @ ETA @ E


def metric_derivatives(x: np.ndarray, witness: Witness) -> np.ndarray:
    out = np.empty((4, 4, 4), dtype=float)
    xc = np.asarray(x, dtype=complex)
    for k in range(4):
        z = xc.copy()
        z[k] += 1j * CS_H
        out[k] = np.imag(metric(z, witness)) / CS_H
    return out


def christoffel(x: np.ndarray, witness: Witness) -> np.ndarray:
    g = np.asarray(metric(np.asarray(x), witness), dtype=float)
    gi = np.linalg.inv(g)
    dg = metric_derivatives(np.asarray(x, dtype=float), witness)
    G = np.zeros((4, 4, 4), dtype=float)
    for a in range(4):
        for b in range(4):
            for c in range(4):
                G[a, b, c] = 0.5 * sum(gi[a, d] * (dg[b, d, c] + dg[c, d, b] - dg[d, b, c]) for d in range(4))
    return G


def ambient_riemann(x: np.ndarray, witness: Witness, step: float) -> np.ndarray:
    G = christoffel(x, witness)
    dG = np.empty((4, 4, 4, 4), dtype=float)
    for k in range(4):
        dx = np.zeros(4)
        dx[k] = step
        dG[k] = (christoffel(x + dx, witness) - christoffel(x - dx, witness)) / (2 * step)
    R = np.zeros((4, 4, 4, 4), dtype=float)
    # R[a,b,c,d] are components of R(partial_c,partial_d) partial_b.
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    R[a, b, c, d] = dG[c, a, d, b] - dG[d, a, c, b]
                    R[a, b, c, d] += sum(G[a, c, e] * G[e, d, b] - G[a, d, e] * G[e, c, b] for e in range(4))
    return R


def integrate_state(rhs, span: tuple[float, float], y0: np.ndarray) -> np.ndarray:
    if span[0] == span[1]:
        return y0.copy()
    sol = solve_ivp(rhs, span, y0, method="DOP853", rtol=RTOL, atol=ATOL, max_step=MAX_STEP)
    if not sol.success:
        raise RuntimeError(sol.message)
    return sol.y[:, -1]


class PairSurface:
    witness: Witness

    def __init__(self) -> None:
        self._base_cache: dict[tuple[float, float], dict] = {}
        self._light_cache: dict[tuple[float, float], dict] = {}

    def point(self, y: float, s: float) -> np.ndarray:
        raise NotImplementedError

    def exact_tangents(self, y: float, s: float) -> np.ndarray | None:
        return None

    def tangent(self, q: np.ndarray, axis: int, d: float = SURFACE_D) -> np.ndarray:
        exact = self.exact_tangents(float(q[0]), float(q[1]))
        if exact is not None:
            return exact[:, axis]
        dq = np.zeros(2)
        dq[axis] = d
        return (self.point(*(q + dq)) - self.point(*(q - dq))) / (2 * d)


class R17LeafSurface(PairSurface):
    witness = R17

    def __init__(self) -> None:
        super().__init__()

    @lru_cache(maxsize=None)
    def point(self, y: float, s: float) -> np.ndarray:
        return np.array([0.07 + y, 1.08, 0.31, 0.44 + 2.0 * s], dtype=float)

    def exact_tangents(self, y: float, s: float) -> np.ndarray:
        del y, s
        return np.array([[1.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 2.0]])


class TimeLiveFermiSurface(PairSurface):
    witness = TL

    def __init__(self) -> None:
        super().__init__()
        self.x0 = np.array([0.12, -0.18, 0.23, -0.14], dtype=float)
        frame = np.linalg.inv(coframe(self.x0, self.witness))
        self.u0 = np.asarray(frame[:, 0], dtype=float)
        self.n0 = np.asarray(frame[:, 1], dtype=float)
        g0 = metric(self.x0, self.witness)
        if abs(self.u0 @ g0 @ self.u0 + 1) > 1e-12 or abs(self.n0 @ g0 @ self.n0 - 1) > 1e-12 or abs(self.u0 @ g0 @ self.n0) > 1e-12:
            raise RuntimeError("initial complete-coframe flag is not orthonormal")

        state0 = np.concatenate((self.x0, self.u0, self.n0))

        def rhs(_, state):
            x, u, n = state[:4], state[4:8], state[8:12]
            G = christoffel(x, self.witness)
            du = -np.einsum("abc,b,c->a", G, u, u)
            dn = -np.einsum("abc,b,c->a", G, u, n)
            return np.concatenate((u, du, dn))

        self._observer_pos = solve_ivp(rhs, (0.0, 0.065), state0, method="DOP853", rtol=RTOL, atol=ATOL, max_step=MAX_STEP, dense_output=True)
        self._observer_neg = solve_ivp(rhs, (0.0, -0.065), state0, method="DOP853", rtol=RTOL, atol=ATOL, max_step=MAX_STEP, dense_output=True)
        if not self._observer_pos.success or not self._observer_neg.success:
            raise RuntimeError("observer dense-output integration failed")

    @lru_cache(maxsize=None)
    def observer_state(self, y: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        if abs(y) > 0.065:
            raise ValueError("query y lies outside preregistered dense observer tile")
        sol = self._observer_pos if y >= 0 else self._observer_neg
        state = np.asarray(sol.sol(y), dtype=float)
        return state[:4], state[4:8], state[8:12]

    @lru_cache(maxsize=None)
    def point(self, y: float, s: float) -> np.ndarray:
        x, _, n = self.observer_state(y)
        state0 = np.concatenate((x, n))

        def rhs(_, state):
            xx, v = state[:4], state[4:8]
            G = christoffel(xx, self.witness)
            dv = -np.einsum("abc,b,c->a", G, v, v)
            return np.concatenate((v, dv))

        return integrate_state(rhs, (0.0, s), state0)[:4]


def surface_point(surface: PairSurface, q: np.ndarray) -> np.ndarray:
    return surface.point(float(q[0]), float(q[1]))


def surface_tangents(surface: PairSurface, q: np.ndarray) -> np.ndarray:
    return np.column_stack((surface.tangent(q, 0), surface.tangent(q, 1)))


def surface_second(surface: PairSurface, q: np.ndarray, d: float = SURFACE_D) -> np.ndarray:
    F0 = surface_point(surface, q)
    out = np.empty((4, 2, 2), dtype=float)
    for i in range(2):
        dq = np.zeros(2); dq[i] = d
        out[:, i, i] = (surface_point(surface, q + dq) - 2 * F0 + surface_point(surface, q - dq)) / d**2
    d0 = np.array([d, 0.0]); d1 = np.array([0.0, d])
    mixed = (surface_point(surface, q + d0 + d1) - surface_point(surface, q + d0 - d1) - surface_point(surface, q - d0 + d1) + surface_point(surface, q - d0 - d1)) / (4 * d**2)
    out[:, 0, 1] = mixed
    out[:, 1, 0] = mixed
    return out


def normal_frame(x: np.ndarray, J: np.ndarray, g: np.ndarray, witness: Witness) -> tuple[np.ndarray, np.ndarray]:
    h = J.T @ g @ J
    hi = np.linalg.inv(h)
    PT = J @ hi @ J.T @ g
    PN = np.eye(4) - PT
    frame = np.linalg.inv(coframe(x, witness))
    n0 = PN @ frame[:, 2]
    n0 /= np.sqrt(n0 @ g @ n0)
    n1 = PN @ frame[:, 3]
    n1 -= n0 * (n0 @ g @ n1)
    n1 /= np.sqrt(n1 @ g @ n1)
    N = np.column_stack((n0, n1))
    return N, PN


def base_geometry(surface: PairSurface, q: np.ndarray) -> dict:
    key = (round(float(q[0]), 14), round(float(q[1]), 14))
    if key in surface._base_cache:
        return surface._base_cache[key]
    x = surface_point(surface, q)
    witness = surface.witness
    g = metric(x, witness)
    J = surface_tangents(surface, q)
    h = J.T @ g @ J
    F2 = surface_second(surface, q)
    G = christoffel(x, witness)
    cov2 = np.empty_like(F2)
    for i in range(2):
        for j in range(2):
            cov2[:, i, j] = F2[:, i, j] + np.einsum("abc,b,c->a", G, J[:, i], J[:, j])
    N, PN = normal_frame(x, J, g, witness)
    IIvec = np.einsum("ab,bij->aij", PN, cov2)
    ii = np.einsum("aij,ab,bA->Aij", IIvec, g, N)
    result = {"x": x, "g": g, "J": J, "h": h, "G": G, "N": N, "PN": PN, "cov2": cov2, "IIvec": IIvec, "ii": ii}
    surface._base_cache[key] = result
    return result


def light_geometry(surface: PairSurface, q: np.ndarray) -> dict:
    """First-jet-only geometry used by finite loop transport."""
    key = (round(float(q[0]), 14), round(float(q[1]), 14))
    if key in surface._light_cache:
        return surface._light_cache[key]
    x = surface_point(surface, q)
    g = metric(x, surface.witness)
    J = surface_tangents(surface, q)
    h = J.T @ g @ J
    N, _ = normal_frame(x, J, g, surface.witness)
    result = {"x": x, "g": g, "J": J, "h": h, "N": N, "G": christoffel(x, surface.witness)}
    surface._light_cache[key] = result
    return result


def h_at(surface: PairSurface, q: np.ndarray) -> np.ndarray:
    return base_geometry(surface, q)["h"]


def surface_christoffel(surface: PairSurface, q: np.ndarray, d: float) -> np.ndarray:
    h = h_at(surface, q)
    hi = np.linalg.inv(h)
    dh = np.empty((2, 2, 2), dtype=float)
    for k in range(2):
        dq = np.zeros(2); dq[k] = d
        dh[k] = (h_at(surface, q + dq) - h_at(surface, q - dq)) / (2 * d)
    G = np.zeros((2, 2, 2), dtype=float)
    for a in range(2):
        for b in range(2):
            for c in range(2):
                G[a, b, c] = 0.5 * sum(hi[a, ell] * (dh[b, ell, c] + dh[c, ell, b] - dh[ell, b, c]) for ell in range(2))
    return G


def intrinsic_riemann(surface: PairSurface, q: np.ndarray, d: float) -> np.ndarray:
    inner = d / 2
    G = surface_christoffel(surface, q, inner)
    dG = np.empty((2, 2, 2, 2), dtype=float)
    for k in range(2):
        dq = np.zeros(2); dq[k] = d
        dG[k] = (surface_christoffel(surface, q + dq, inner) - surface_christoffel(surface, q - dq, inner)) / (2 * d)
    R = np.zeros((2, 2, 2, 2), dtype=float)
    for a in range(2):
        for b in range(2):
            for c in range(2):
                for e in range(2):
                    R[a, b, c, e] = dG[c, a, e, b] - dG[e, a, c, b]
                    R[a, b, c, e] += sum(G[a, c, m] * G[m, e, b] - G[a, e, m] * G[m, c, b] for m in range(2))
    return R


def normal_connection(surface: PairSurface, q: np.ndarray, d: float) -> np.ndarray:
    geom = base_geometry(surface, q)
    x, g, J, G, N = geom["x"], geom["g"], geom["J"], geom["G"], geom["N"]
    omega = np.empty((2, 2, 2), dtype=float)
    for i in range(2):
        dq = np.zeros(2); dq[i] = d
        Np = base_geometry(surface, q + dq)["N"]
        Nm = base_geometry(surface, q - dq)["N"]
        dN = (Np - Nm) / (2 * d)
        for A in range(2):
            for B in range(2):
                cov = dN[:, B] + np.einsum("abc,b,c->a", G, J[:, i], N[:, B])
                omega[i, A, B] = N[:, A] @ g @ cov
    return omega


def evaluate_scale(surface: PairSurface, d: float) -> dict:
    q = np.zeros(2)
    geom = base_geometry(surface, q)
    x, g, J, h, ii, N = geom["x"], geom["g"], geom["J"], geom["h"], geom["ii"], geom["N"]
    det_h = float(np.linalg.det(h))
    regular = bool(h[0, 0] < 0 and det_h < 0 and np.linalg.matrix_rank(J) == 2)
    T2 = -h[0, 0]
    beta = h[0, 1] / h[0, 0]
    L2 = h[1, 1] - h[0, 1] ** 2 / h[0, 0]
    hrec = np.array([[-T2, -T2 * beta], [-T2 * beta, -T2 * beta**2 + L2]])
    kappa = 0.25 * np.log(-det_h) if regular else np.nan
    phi = 0.25 * np.log((-det_h) / h[0, 0] ** 2) if regular else np.nan

    ambR = ambient_riemann(x, surface.witness, d / 2)
    intR = intrinsic_riemann(surface, q, d)
    RM = np.einsum("abcd,b,c,d->a", ambR, J[:, 1], J[:, 0], J[:, 1])
    amb_gauss = float(J[:, 0] @ g @ RM)
    int_gauss = float(sum(h[0, a] * intR[a, 1, 0, 1] for a in range(2)))
    extrinsic = float(np.dot(ii[:, 0, 0], ii[:, 1, 1]) - np.dot(ii[:, 0, 1], ii[:, 1, 0]))
    gauss_res = amb_gauss - int_gauss - extrinsic

    surfG = surface_christoffel(surface, q, d / 2)
    omega = normal_connection(surface, q, d / 4)
    dii = np.empty((2, 2, 2, 2), dtype=float)
    for axis in range(2):
        dq = np.zeros(2); dq[axis] = d
        dii[axis] = (base_geometry(surface, q + dq)["ii"] - base_geometry(surface, q - dq)["ii"]) / (2 * d)
    Dii = np.empty_like(dii)
    for axis in range(2):
        for A in range(2):
            for j in range(2):
                for k in range(2):
                    val = dii[axis, A, j, k] + sum(omega[axis, A, B] * ii[B, j, k] for B in range(2))
                    val -= sum(surfG[m, axis, j] * ii[A, m, k] + surfG[m, axis, k] * ii[A, j, m] for m in range(2))
                    Dii[axis, A, j, k] = val
    codazzi = np.empty((2, 2), dtype=float)
    for A in range(2):
        for k in range(2):
            lhs = Dii[0, A, 1, k] - Dii[1, A, 0, k]
            Rvec = np.einsum("abcd,b,c,d->a", ambR, J[:, k], J[:, 0], J[:, 1])
            rhs = N[:, A] @ g @ Rvec
            codazzi[A, k] = lhs - rhs

    domega = np.empty((2, 2, 2, 2), dtype=float)
    for axis in range(2):
        dq = np.zeros(2); dq[axis] = d
        domega[axis] = (normal_connection(surface, q + dq, d / 4) - normal_connection(surface, q - dq, d / 4)) / (2 * d)
    Rperp = domega[0, 1] - domega[1, 0] + omega[0] @ omega[1] - omega[1] @ omega[0]
    hi = np.linalg.inv(h)
    shape = np.array([hi @ ii[A] for A in range(2)])
    ricci = np.empty((2, 2), dtype=float)
    for A in range(2):
        for B in range(2):
            Rvec = np.einsum("abcd,b,c,d->a", ambR, N[:, B], J[:, 0], J[:, 1])
            amb = N[:, A] @ g @ Rvec
            comm = shape[B] @ shape[A] - shape[A] @ shape[B]
            comm_term = h[1, :] @ comm[:, 0]
            ricci[A, B] = Rperp[A, B] - amb - comm_term

    acceleration_s = np.linalg.norm(geom["cov2"][:, 1, 1])
    if surface.witness.geometry == "TIMELIVE_LOCAL":
        dq = np.array([0.0, d])
        Kp = base_geometry(surface, q + dq)["cov2"][:, 0, 1]
        Km = base_geometry(surface, q - dq)["cov2"][:, 0, 1]
        dK = (Kp - Km) / (2 * d)
        K = geom["cov2"][:, 0, 1]
        covK = dK + np.einsum("abc,b,c->a", geom["G"], J[:, 1], K)
        Rjvv = np.einsum("abcd,b,c,d->a", ambR, J[:, 0], J[:, 1], J[:, 1])
        jacobi_res = np.linalg.norm(covK + Rjvv)
        jacobi_status = "QUERY_OWNED_GEODESIC_VARIATION"
    else:
        jacobi_res = np.nan
        jacobi_status = "NOT_OWNED_BY_QUERY"

    return {
        "query_id": surface.witness.query_id,
        "scale": d,
        "regular": regular,
        "det_h": det_h,
        "h00": float(h[0, 0]),
        "kappa_pair": float(kappa),
        "phi_pair": float(phi),
        "beta_pair": float(beta),
        "h_reconstruction_residual": float(np.linalg.norm(hrec - h)),
        "ii_norm": float(np.linalg.norm(ii)),
        "s_ruling_acceleration_norm": float(acceleration_s),
        "gauss_residual": float(abs(gauss_res)),
        "codazzi_residual": float(np.linalg.norm(codazzi)),
        "ricci_residual": float(np.linalg.norm(ricci)),
        "jacobi_status": jacobi_status,
        "jacobi_residual": None if np.isnan(jacobi_res) else float(jacobi_res),
        "ambient_gauss": amb_gauss,
        "intrinsic_gauss": int_gauss,
        "extrinsic_gauss": extrinsic,
    }


def orthogonal_polar(matrix: np.ndarray) -> np.ndarray:
    u, _, vt = np.linalg.svd(matrix)
    out = u @ vt
    if np.linalg.det(out) < 0:
        u[:, -1] *= -1
        out = u @ vt
    return out


def integrate_surface_loop(surface: PairSurface, halfwidth: float, subdivisions: int) -> tuple[np.ndarray, np.ndarray, float]:
    corners = [
        np.array([-halfwidth, -halfwidth]),
        np.array([halfwidth, -halfwidth]),
        np.array([halfwidth, halfwidth]),
        np.array([-halfwidth, halfwidth]),
        np.array([-halfwidth, -halfwidth]),
    ]
    P = np.eye(4)
    PN = np.eye(2)
    for qa, qb in zip(corners[:-1], corners[1:]):
        for index in range(subdivisions):
            q0 = qa + (qb - qa) * (index / subdivisions)
            q1 = qa + (qb - qa) * ((index + 1) / subdivisions)
            qm = 0.5 * (q0 + q1)
            geom_m = light_geometry(surface, qm)
            x0 = surface_point(surface, q0)
            x1 = surface_point(surface, q1)
            dx = x1 - x0
            W = np.einsum("abc,b->ac", geom_m["G"], dx)
            U = expm(-W)
            P = U @ P

            geom0 = light_geometry(surface, q0)
            geom1 = light_geometry(surface, q1)
            carried = U @ geom0["N"]
            overlap = geom1["N"].T @ geom1["g"] @ carried
            PN = orthogonal_polar(overlap) @ PN
    xbase = surface_point(surface, corners[0])
    gbase = metric(xbase, surface.witness)
    metric_defect = float(np.linalg.norm(P.T @ gbase @ P - gbase))
    return P, PN, metric_defect


def evaluate_loop(surface: PairSurface, halfwidth: float) -> dict:
    q = np.zeros(2)
    geom = base_geometry(surface, q)
    d = halfwidth / 8
    ambR = ambient_riemann(geom["x"], surface.witness, d)
    Rop = np.einsum("abcd,c,d->ab", ambR, geom["J"][:, 0], geom["J"][:, 1])
    omega = normal_connection(surface, q, d)
    domega = np.empty((2, 2, 2, 2), dtype=float)
    for axis in range(2):
        dq = np.zeros(2); dq[axis] = d
        domega[axis] = (normal_connection(surface, q + dq, d / 2) - normal_connection(surface, q - dq, d / 2)) / (2 * d)
    Rperp = domega[0, 1] - domega[1, 0] + omega[0] @ omega[1] - omega[1] @ omega[0]
    area = (2 * halfwidth) ** 2
    runs = {}
    for subdivisions in (8, 16, 32):
        runs[subdivisions] = integrate_surface_loop(surface, halfwidth, subdivisions)
    P, PN, metric_defect = runs[32]
    ambient_quad_8_16 = float(np.linalg.norm(runs[16][0] - runs[8][0]))
    ambient_quad_16_32 = float(np.linalg.norm(runs[32][0] - runs[16][0]))
    normal_quad_8_16 = float(np.linalg.norm(runs[16][1] - runs[8][1]))
    normal_quad_16_32 = float(np.linalg.norm(runs[32][1] - runs[16][1]))
    return {
        "query_id": surface.witness.query_id,
        "halfwidth": halfwidth,
        "area": area,
        "ambient_holonomy_norm": float(np.linalg.norm(P - np.eye(4))),
        "ambient_metric_defect": metric_defect,
        "ambient_curvature_residual": float(np.linalg.norm((P - np.eye(4)) / area + Rop)),
        "ambient_quadrature_8_16": ambient_quad_8_16,
        "ambient_quadrature_16_32": ambient_quad_16_32,
        "normal_holonomy_norm": float(np.linalg.norm(PN - np.eye(2))),
        "normal_curvature_residual": float(np.linalg.norm((PN - np.eye(2)) / area + Rperp)),
        "normal_quadrature_8_16": normal_quad_8_16,
        "normal_quadrature_16_32": normal_quad_16_32,
    }


def write_tsv(path: Path, rows: list[dict]) -> None:
    if not rows:
        raise RuntimeError(f"empty output {path}")
    fields = list(rows[0])
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: ("NA" if v is None else v) for k, v in row.items()})


def source_liveness() -> dict:
    x = np.array([0.12, -0.18, 0.23, -0.14])
    base = timelive_fields(x, TL.eps)
    gradients = []
    for axis in range(4):
        dx = np.zeros(4); dx[axis] = 1.0e-5
        plus = timelive_fields(x + dx, TL.eps)
        minus = timelive_fields(x - dx, TL.eps)
        flat_plus = np.concatenate(([float(v) for v in plus[:-1]], plus[-1].ravel()))
        flat_minus = np.concatenate(([float(v) for v in minus[:-1]], minus[-1].ravel()))
        gradients.append((flat_plus - flat_minus) / (2.0e-5))
    grad = np.asarray(gradients).T
    return {
        "field_count": int(grad.shape[0]),
        "coordinate_count": int(grad.shape[1]),
        "nonzero_gradient_fields": int(np.sum(np.linalg.norm(grad, axis=1) > 1.0e-10)),
        "gradient_norms": [float(v) for v in np.linalg.norm(grad, axis=1)],
    }


def main() -> None:
    surfaces: list[PairSurface] = [R17LeafSurface(), TimeLiveFermiSurface()]
    scale_rows = []
    loop_rows = []
    for surface in surfaces:
        for d in SCALES:
            print(f"SCALE {surface.witness.query_id} {d}", flush=True)
            scale_rows.append(evaluate_scale(surface, d))
        for width in LOOP_HALF_WIDTHS:
            print(f"LOOP {surface.witness.query_id} {width}", flush=True)
            loop_rows.append(evaluate_loop(surface, width))
    write_tsv(HERE / "SCALE_DIAGNOSTICS.tsv", scale_rows)
    write_tsv(HERE / "LOOP_DIAGNOSTICS.tsv", loop_rows)
    result = {
        "schema": "UDT_COMMON_QUERY_PAIR_IMMERSION_V1",
        "status": "PRODUCTION_COMPLETE_INDEPENDENT_PENDING",
        "scope": "two_query_bounded_metric_geometry",
        "queries": [R17.query_id, TL.query_id],
        "scales": list(SCALES),
        "loop_halfwidths": list(LOOP_HALF_WIDTHS),
        "source_liveness": source_liveness(),
        "counts": {"scale_rows": len(scale_rows), "loop_rows": len(loop_rows)},
        "versions": {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__},
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
