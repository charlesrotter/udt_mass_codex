#!/usr/bin/env python3
"""Full nonlinear finite-path G128 geodesic/screen/Jacobi propagation."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
import sympy as sp


HERE = Path(__file__).resolve().parent
LAM_END = 0.8
SAMPLES = np.linspace(0.0, LAM_END, 161)
ANGLES = (0.0, math.pi / 12, math.pi / 6, math.pi / 4)


def json_default(value):
    if isinstance(value, np.generic):
        return value.item()
    raise TypeError(f"not JSON serializable: {type(value).__name__}")


def build_symbolic_geometry():
    T, R, th, ps = sp.symbols("T R theta psi", real=True)
    kap = sp.Function("kappa")(T, R)
    phi = sp.Function("phi")(T, R)
    beta = sp.Function("beta")(T, R)
    coords = (T, R, th, ps)

    N = sp.exp(kap - phi)
    L = sp.exp(kap + phi)
    g = sp.Matrix(
        [
            [-N**2 + L**2 * beta**2, L**2 * beta, 0, 0],
            [L**2 * beta, L**2, 0, 0],
            [0, 0, R**2, 0],
            [0, 0, 0, R**2 * sp.sin(th) ** 2],
        ]
    )
    gi = sp.simplify(g.inv())

    Gamma = np.empty((4, 4, 4), dtype=object)
    for a in range(4):
        for b in range(4):
            for c in range(4):
                Gamma[a, b, c] = sp.simplify(
                    sum(
                        gi[a, d]
                        * (
                            sp.diff(g[d, c], coords[b])
                            + sp.diff(g[d, b], coords[c])
                            - sp.diff(g[b, c], coords[d])
                        )
                        for d in range(4)
                    )
                    / 2
                )

    Rup = np.empty((4, 4, 4, 4), dtype=object)
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    Rup[a, b, c, d] = sp.simplify(
                        sp.diff(Gamma[a, d, b], coords[c])
                        - sp.diff(Gamma[a, c, b], coords[d])
                        + sum(
                            Gamma[a, c, e] * Gamma[e, d, b]
                            - Gamma[a, d, e] * Gamma[e, c, b]
                            for e in range(4)
                        )
                    )

    Rlow = np.empty((4, 4, 4, 4), dtype=object)
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    Rlow[a, b, c, d] = sp.simplify(
                        sum(g[a, e] * Rup[e, b, c, d] for e in range(4))
                    )

    jet_exprs = (
        kap,
        phi,
        beta,
        sp.diff(kap, T),
        sp.diff(kap, R),
        sp.diff(phi, T),
        sp.diff(phi, R),
        sp.diff(beta, T),
        sp.diff(beta, R),
        sp.diff(kap, T, 2),
        sp.diff(kap, T, R),
        sp.diff(kap, R, 2),
        sp.diff(phi, T, 2),
        sp.diff(phi, T, R),
        sp.diff(phi, R, 2),
        sp.diff(beta, T, 2),
        sp.diff(beta, T, R),
        sp.diff(beta, R, 2),
    )
    jet_symbols = sp.symbols(
        "kap phi beta kap_T kap_R phi_T phi_R beta_T beta_R "
        "kap_TT kap_TR kap_RR phi_TT phi_TR phi_RR beta_TT beta_TR beta_RR",
        real=True,
    )
    replace = dict(zip(jet_exprs, jet_symbols))

    def lower(expr):
        return sp.simplify(expr.xreplace(replace))

    g_flat = [lower(g[a, b]) for a in range(4) for b in range(4)]
    gamma_entries = []
    for index in np.ndindex(4, 4, 4):
        expr = lower(Gamma[index])
        if expr != 0:
            gamma_entries.append((index, expr))
    rlow_entries = []
    for index in np.ndindex(4, 4, 4, 4):
        expr = lower(Rlow[index])
        if expr != 0:
            rlow_entries.append((index, expr))

    args = (R, th, *jet_symbols)
    g_fn = sp.lambdify(args, g_flat, modules="numpy", cse=True)
    gamma_fn = sp.lambdify(args, [x[1] for x in gamma_entries], modules="numpy", cse=True)
    rlow_fn = sp.lambdify(args, [x[1] for x in rlow_entries], modules="numpy", cse=True)

    # SymPy's general ``simplify``/``trigsimp`` path is both expensive and, for
    # these large expressions, can enter a fragile multivariate factorization.
    # The only coordinate trigonometry in this chart is spherical theta.  Audit
    # it exactly through the rational half-angle substitution instead.  All
    # remaining quantities are treated as algebraically independent jet data.
    half_tan = sp.symbols("half_tan", real=True)
    zero_cache = {}

    def exact_zero(expr):
        if expr == 0:
            return True
        if expr in zero_cache:
            return zero_cache[expr]
        candidate = sp.expand_trig(expr)
        candidate = candidate.subs(
            {
                sp.tan(th): sp.sin(th) / sp.cos(th),
                sp.cot(th): sp.cos(th) / sp.sin(th),
                sp.sec(th): 1 / sp.cos(th),
                sp.csc(th): 1 / sp.sin(th),
            },
            simultaneous=True,
        )
        candidate = candidate.subs(
            {
                sp.sin(th): 2 * half_tan / (1 + half_tan**2),
                sp.cos(th): (1 - half_tan**2) / (1 + half_tan**2),
            },
            simultaneous=True,
        )
        is_zero = sp.cancel(candidate) == 0
        zero_cache[expr] = is_zero
        return is_zero

    symmetry_debug = {}

    def audit_symmetry(label, sign, permutation):
        for a, b, c, d in np.ndindex(4, 4, 4, 4):
            residual = Rlow[a, b, c, d] + sign * permutation(a, b, c, d)
            if not exact_zero(residual):
                symmetry_debug[label] = {
                    "index": (a, b, c, d),
                    "residual": str(sp.factor(sp.together(residual))),
                }
                return False
        return True

    # Exact algebraic checks on the generic symbolic geometry.
    exact_checks = {
        "metric_inverse": all(
            sp.simplify((g * gi - sp.eye(4))[a, b]) == 0
            for a in range(4)
            for b in range(4)
        ),
        "connection_lower_symmetry": all(
            sp.simplify(Gamma[a, b, c] - Gamma[a, c, b]) == 0
            for a in range(4)
            for b in range(4)
            for c in range(4)
        ),
        "riemann_last_pair_antisymmetry": audit_symmetry(
            "last", 1, lambda a, b, c, d: Rlow[a, b, d, c]
        ),
        "riemann_first_pair_antisymmetry": audit_symmetry(
            "first", 1, lambda a, b, c, d: Rlow[b, a, c, d]
        ),
        "riemann_pair_exchange": audit_symmetry(
            "pair", -1, lambda a, b, c, d: Rlow[c, d, a, b]
        ),
    }

    # Generic frame normalization, including the complete spherical shift.
    alpha = sp.symbols("alpha", real=True)
    e0 = sp.Matrix([1 / N, -beta / N, 0, 0])
    e1 = sp.Matrix([0, 1 / L, 0, 0])
    e2 = sp.Matrix([0, 0, 1 / R, 0])
    e3 = sp.Matrix([0, 0, 0, 1 / (R * sp.sin(th))])
    kval = e0 + sp.cos(alpha) * e1 + sp.sin(alpha) * e2
    s1 = -sp.sin(alpha) * e1 + sp.cos(alpha) * e2
    s2 = e3
    inner = lambda x, y: sp.trigsimp(sp.simplify((x.T * g * y)[0]))
    exact_checks["generic_null_and_normalized"] = (
        inner(kval, kval) == 0 and inner(kval, e0) == -1
    )
    exact_checks["generic_screen_orthonormal"] = (
        inner(s1, s1) == 1
        and inner(s2, s2) == 1
        and inner(s1, s2) == 0
        and inner(kval, s1) == 0
        and inner(kval, s2) == 0
    )

    # Recover the exact G127 static reciprocal curvature scalars.
    static_sub = {
        jet_symbols[0]: 0,
        jet_symbols[2]: 0,
        jet_symbols[3]: 0,
        jet_symbols[4]: 0,
        jet_symbols[5]: 0,
        jet_symbols[7]: 0,
        jet_symbols[8]: 0,
        jet_symbols[9]: 0,
        jet_symbols[10]: 0,
        jet_symbols[11]: 0,
        jet_symbols[12]: 0,
        jet_symbols[13]: 0,
        jet_symbols[15]: 0,
        jet_symbols[16]: 0,
        jet_symbols[17]: 0,
        th: sp.pi / 2,
    }
    ph, phr, phrr = jet_symbols[1], jet_symbols[6], jet_symbols[14]
    g_low = np.empty((4, 4, 4, 4), dtype=object)
    for index in np.ndindex(4, 4, 4, 4):
        g_low[index] = lower(Rlow[index]).subs(static_sub)
    et = sp.Matrix([sp.exp(ph), 0, 0, 0])
    er = sp.Matrix([0, sp.exp(-ph), 0, 0])
    eth = sp.Matrix([0, 0, 1 / R, 0])
    eps = sp.Matrix([0, 0, 0, 1 / R])

    def contract(x, y, z, w):
        value = sp.S.Zero
        for a in range(4):
            if w[a] == 0:
                continue
            for b in range(4):
                if z[b] == 0:
                    continue
                for c in range(4):
                    if x[c] == 0:
                        continue
                    for d in range(4):
                        if y[d] != 0:
                            value += w[a] * z[b] * x[c] * y[d] * g_low[a, b, c, d]
        return sp.simplify(value)

    Tcurv = contract(er, et, et, er)
    Ucurv = contract(eth, et, et, eth)
    Vcurv = contract(eth, er, er, eth)
    Wcurv = contract(eps, eth, eth, eps)
    exact_checks.update(
        {
            "G127_static_T": sp.simplify(
                Tcurv - sp.exp(-2 * ph) * (2 * phr**2 - phrr)
            )
            == 0,
            "G127_static_U": sp.simplify(
                Ucurv + sp.exp(-2 * ph) * phr / R
            )
            == 0,
            "G127_static_V": sp.simplify(
                Vcurv - sp.exp(-2 * ph) * phr / R
            )
            == 0,
            "G127_static_W": sp.simplify(
                Wcurv - (1 - sp.exp(-2 * ph)) / R**2
            )
            == 0,
        }
    )

    return {
        "symbols": (T, R),
        "jet_exprs": jet_exprs,
        "jet_symbols": jet_symbols,
        "g_fn": g_fn,
        "gamma_fn": gamma_fn,
        "rlow_fn": rlow_fn,
        "gamma_indices": [x[0] for x in gamma_entries],
        "rlow_indices": [x[0] for x in rlow_entries],
        "exact_checks": exact_checks,
        "static_curvature_expressions": {
            "T": str(sp.factor(Tcurv)),
            "U": str(sp.factor(Ucurv)),
            "V": str(sp.factor(Vcurv)),
            "W": str(sp.factor(Wcurv)),
        },
        "nonzero_gamma": len(gamma_entries),
        "nonzero_rlow": len(rlow_entries),
        "symmetry_debug": symmetry_debug,
    }


def build_histories(T, R, jet_exprs):
    qtime = (1 + sp.Rational(2, 5) * sp.sin(T)) / 4
    phi_static = sp.log(1 + R**2 / 4) / 2
    phi_live = sp.log(1 + qtime * R**2) / 2
    histories = {
        "H0_flat": (sp.S.Zero, sp.S.Zero, sp.S.Zero),
        "H1_static_reciprocal": (sp.S.Zero, phi_static, sp.S.Zero),
        "H2_timelive_reciprocal": (sp.S.Zero, phi_live, sp.S.Zero),
        "H3_timelive_full_spherical_base": (
            R**2 * sp.cos(T / 2) / (20 * (1 + R**2)),
            phi_live,
            R * sp.exp(-R**2) * (1 + sp.sin(T / 2)) / 12,
        ),
    }
    funcs = {}
    for name, (kap, phi, beta) in histories.items():
        replacements = {
            sp.Function("kappa")(T, R): kap,
            sp.Function("phi")(T, R): phi,
            sp.Function("beta")(T, R): beta,
        }
        values = [sp.simplify(expr.subs(replacements).doit()) for expr in jet_exprs]
        funcs[name] = {
            "expressions": tuple(str(value) for value in values[:3]),
            "fn": sp.lambdify((T, R), values, modules="numpy", cse=True),
        }
    return funcs


class Geometry:
    def __init__(self, symbolic, histories):
        self.s = symbolic
        self.histories = histories

    def args(self, name, x):
        T, R, th, _ = x
        jets = self.histories[name]["fn"](T, R)
        return (R, th, *[float(value) for value in jets])

    def metric(self, name, x):
        return np.asarray(self.s["g_fn"](*self.args(name, x)), dtype=float).reshape(4, 4)

    def connection(self, name, x):
        out = np.zeros((4, 4, 4), dtype=float)
        values = np.atleast_1d(self.s["gamma_fn"](*self.args(name, x))).astype(float)
        for index, value in zip(self.s["gamma_indices"], values):
            out[index] = value
        return out

    def curvature(self, name, x):
        out = np.zeros((4, 4, 4, 4), dtype=float)
        values = np.atleast_1d(self.s["rlow_fn"](*self.args(name, x))).astype(float)
        for index, value in zip(self.s["rlow_indices"], values):
            out[index] = value
        return out


def initial_frame(geo, history, alpha):
    x = np.array([0.0, 0.4, math.pi / 2, 0.0])
    jets = geo.histories[history]["fn"](x[0], x[1])
    kap, phi, beta = map(float, jets[:3])
    N = math.exp(kap - phi)
    L = math.exp(kap + phi)
    e0 = np.array([1 / N, -beta / N, 0.0, 0.0])
    e1 = np.array([0.0, 1 / L, 0.0, 0.0])
    e2 = np.array([0.0, 0.0, 1 / x[1], 0.0])
    e3 = np.array([0.0, 0.0, 0.0, 1 / x[1]])
    v = math.cos(alpha) * e1 + math.sin(alpha) * e2
    s1 = -math.sin(alpha) * e1 + math.cos(alpha) * e2
    s2 = e3
    k = e0 + v
    return x, e0, v, k, s1, s2


def tidal(rlow, k, screens):
    out = np.empty((2, 2), dtype=float)
    for A in range(2):
        for B in range(2):
            out[A, B] = np.einsum(
                "c,d,b,a,abcd->", screens[A], k, k, screens[B], rlow
            )
    return out


def full_rhs(geo, history):
    def rhs(_lam, y):
        x = y[0:4]
        k = y[4:8]
        screens = y[8:16].reshape(2, 4)
        D = y[16:20].reshape(2, 2)
        P = y[20:24].reshape(2, 2)
        gamma = geo.connection(history, x)
        rlow = geo.curvature(history, x)
        acceleration = -np.einsum("abc,b,c->a", gamma, k, k)
        screen_dot = -np.einsum("abc,b,Ac->Aa", gamma, k, screens)
        rperp = tidal(rlow, k, screens)
        return np.concatenate(
            (k, acceleration, screen_dot.ravel(), P.ravel(), (-rperp @ D).ravel())
        )

    return rhs


def geodesic_rhs(geo, history):
    def rhs(_lam, y):
        x, k = y[:4], y[4:]
        gamma = geo.connection(history, x)
        return np.concatenate((k, -np.einsum("abc,b,c->a", gamma, k, k)))

    return rhs


def solve_full(geo, history, alpha, strict=False):
    x, _e0, _v, k, s1, s2 = initial_frame(geo, history, alpha)
    y0 = np.concatenate((x, k, s1, s2, np.zeros(4), np.eye(2).ravel()))
    settings = (
        {"rtol": 2.5e-12, "atol": 2.5e-14, "max_step": 0.005}
        if strict
        else {"rtol": 1e-10, "atol": 1e-12, "max_step": 0.01}
    )
    sol = solve_ivp(
        full_rhs(geo, history),
        (0.0, LAM_END),
        y0,
        method="DOP853",
        t_eval=SAMPLES,
        dense_output=True,
        **settings,
    )
    if not sol.success or sol.t[-1] < LAM_END:
        raise RuntimeError(f"branch failed: {history} alpha={alpha}: {sol.message}")
    return sol


def solve_geodesic_endpoint(geo, history, alpha, axis, delta):
    x, e0, v, _k, s1, s2 = initial_frame(geo, history, alpha)
    direction = math.cos(delta) * v + math.sin(delta) * (s1, s2)[axis]
    y0 = np.concatenate((x, e0 + direction))
    sol = solve_ivp(
        geodesic_rhs(geo, history),
        (0.0, LAM_END),
        y0,
        method="DOP853",
        rtol=2.5e-12,
        atol=2.5e-14,
        max_step=0.005,
    )
    if not sol.success:
        raise RuntimeError(f"neighbor ray failed: {history} {alpha} {axis} {delta}")
    return sol.y[:4, -1]


def five_point_jacobi(geo, history, alpha, base_sol):
    h = 2e-4
    Dfd = np.zeros((2, 2))
    endpoint = base_sol.y[:4, -1]
    screens = base_sol.y[8:16, -1].reshape(2, 4)
    g = geo.metric(history, endpoint)
    for axis in range(2):
        points = {
            multiple: solve_geodesic_endpoint(geo, history, alpha, axis, multiple * h)
            for multiple in (-2, -1, 1, 2)
        }
        J = (-points[2] + 8 * points[1] - 8 * points[-1] + points[-2]) / (12 * h)
        for row in range(2):
            Dfd[row, axis] = screens[row] @ g @ J
    return Dfd


def diagnose(geo, history, alpha, sol):
    null_drift = 0.0
    screen_drift = 0.0
    screen_ray_drift = 0.0
    tidal_symmetry = 0.0
    max_tidal_contrast = 0.0
    max_shear = 0.0
    radial_singular_difference = 0.0
    radial_shear = 0.0
    det_min = float("inf")
    shear_series = []
    singular_series = []
    tidal_series = []
    det_series = []

    for i in range(sol.y.shape[1]):
        x = sol.y[0:4, i]
        k = sol.y[4:8, i]
        screens = sol.y[8:16, i].reshape(2, 4)
        D = sol.y[16:20, i].reshape(2, 2)
        P = sol.y[20:24, i].reshape(2, 2)
        g = geo.metric(history, x)
        rperp = tidal(geo.curvature(history, x), k, screens)
        null_drift = max(null_drift, abs(k @ g @ k))
        screen_drift = max(screen_drift, np.max(np.abs(screens @ g @ screens.T - np.eye(2))))
        screen_ray_drift = max(screen_ray_drift, np.max(np.abs(screens @ g @ k)))
        tidal_symmetry = max(tidal_symmetry, np.max(np.abs(rperp - rperp.T)))
        contrast = float(rperp[0, 0] - rperp[1, 1])
        max_tidal_contrast = max(max_tidal_contrast, abs(contrast))
        tidal_series.append(contrast)
        singular = np.linalg.svd(D, compute_uv=False)
        singular_series.append(singular)
        radial_singular_difference = max(radial_singular_difference, abs(singular[0] - singular[1]))
        det = float(np.linalg.det(D))
        det_series.append(det)
        if i > 0:
            det_min = min(det_min, abs(det))
            if abs(det) > 1e-10:
                B = P @ np.linalg.inv(D)
                Btf = (B + B.T) / 2 - np.trace(B) * np.eye(2) / 2
                shear = float(np.linalg.norm(Btf, ord="fro"))
                max_shear = max(max_shear, shear)
                radial_shear = max(radial_shear, shear)
                shear_series.append(shear)
            else:
                shear_series.append(float("nan"))
        else:
            shear_series.append(0.0)

    # Raw affine and screen-transport residuals from a five-point derivative of the dense solve.
    affine_residual = 0.0
    parallel_residual = 0.0
    hfd = 1e-4
    for lam in np.linspace(5e-4, LAM_END - 5e-4, 21):
        ym2, ym1, yp1, yp2 = (
            sol.sol(lam - 2 * hfd),
            sol.sol(lam - hfd),
            sol.sol(lam + hfd),
            sol.sol(lam + 2 * hfd),
        )
        derivative = (-yp2 + 8 * yp1 - 8 * ym1 + ym2) / (12 * hfd)
        y = sol.sol(lam)
        x, k = y[0:4], y[4:8]
        screens = y[8:16].reshape(2, 4)
        gamma = geo.connection(history, x)
        affine = derivative[4:8] + np.einsum("abc,b,c->a", gamma, k, k)
        parallel = derivative[8:16].reshape(2, 4) + np.einsum(
            "abc,b,Ac->Aa", gamma, k, screens
        )
        affine_residual = max(affine_residual, np.max(np.abs(affine)))
        parallel_residual = max(parallel_residual, np.max(np.abs(parallel)))

    Dend = sol.y[16:20, -1].reshape(2, 2)
    Pend = sol.y[20:24, -1].reshape(2, 2)
    Dfd = five_point_jacobi(geo, history, alpha, sol)
    fd_abs = float(np.max(np.abs(Dend - Dfd)))
    fd_rel = float(np.linalg.norm(Dend - Dfd) / max(np.linalg.norm(Dend), 1e-30))

    return {
        "null_drift": null_drift,
        "screen_metric_drift": screen_drift,
        "screen_ray_drift": screen_ray_drift,
        "tidal_symmetry_drift": tidal_symmetry,
        "affine_residual": affine_residual,
        "parallel_residual": parallel_residual,
        "max_tidal_contrast": max_tidal_contrast,
        "max_optical_shear": max_shear,
        "radial_singular_difference": radial_singular_difference,
        "radial_shear": radial_shear,
        "min_abs_det_after_vertex": det_min,
        "D_endpoint": Dend.tolist(),
        "P_endpoint": Pend.tolist(),
        "D_fd_endpoint": Dfd.tolist(),
        "fd_abs": fd_abs,
        "fd_rel": fd_rel,
        "tidal_contrast_series": tidal_series,
        "shear_series": shear_series,
        "singular_series": np.asarray(singular_series).tolist(),
        "det_series": det_series,
    }


def main():
    symbolic = build_symbolic_geometry()
    T, R = symbolic["symbols"]
    histories = build_histories(T, R, symbolic["jet_exprs"])
    geo = Geometry(symbolic, histories)

    exact_checks = dict(symbolic["exact_checks"])
    branch_data = {}
    sample_payload = {}
    rows = []
    convergence_geo = 0.0
    convergence_phase = 0.0

    for history in histories:
        for alpha in ANGLES:
            key = f"{history}__alpha_{alpha:.12f}"
            sol = solve_full(geo, history, alpha, strict=False)
            strict = solve_full(geo, history, alpha, strict=True)
            convergence_geo = max(
                convergence_geo, float(np.max(np.abs(sol.y[:16, -1] - strict.y[:16, -1])))
            )
            convergence_phase = max(
                convergence_phase, float(np.max(np.abs(sol.y[16:, -1] - strict.y[16:, -1])))
            )
            diag = diagnose(geo, history, alpha, sol)
            branch_data[key] = diag
            sample_payload[f"{key}__lambda"] = sol.t
            sample_payload[f"{key}__state"] = sol.y
            sample_payload[f"{key}__tidal_contrast"] = np.asarray(diag["tidal_contrast_series"])
            sample_payload[f"{key}__shear"] = np.asarray(diag["shear_series"])
            rows.append(
                {
                    "history": history,
                    "alpha": f"{alpha:.16g}",
                    "max_tidal_contrast": f"{diag['max_tidal_contrast']:.17g}",
                    "max_optical_shear": f"{diag['max_optical_shear']:.17g}",
                    "fd_abs": f"{diag['fd_abs']:.17g}",
                    "fd_rel": f"{diag['fd_rel']:.17g}",
                    "null_drift": f"{diag['null_drift']:.17g}",
                    "affine_residual": f"{diag['affine_residual']:.17g}",
                    "screen_metric_drift": f"{diag['screen_metric_drift']:.17g}",
                    "min_abs_det_after_vertex": f"{diag['min_abs_det_after_vertex']:.17g}",
                }
            )

    # One exact-symmetry numerical reversal control on a genuinely time-live history.
    reverse_plus = solve_full(geo, "H2_timelive_reciprocal", math.pi / 6)
    reverse_minus = solve_full(geo, "H2_timelive_reciprocal", -math.pi / 6)
    plus_diag = branch_data[
        f"H2_timelive_reciprocal__alpha_{math.pi / 6:.12f}"
    ]
    minus_diag = diagnose(geo, "H2_timelive_reciprocal", -math.pi / 6, reverse_minus)
    reversal_singular = float(
        np.max(
            np.abs(
                np.asarray(plus_diag["singular_series"])
                - np.asarray(minus_diag["singular_series"])
            )
        )
    )
    reversal_shear = float(
        np.nanmax(
            np.abs(
                np.asarray(plus_diag["shear_series"])
                - np.asarray(minus_diag["shear_series"])
            )
        )
    )

    all_diags = list(branch_data.values())
    radial_diags = [
        branch_data[f"{name}__alpha_{0.0:.12f}"] for name in histories
    ]
    nonflat_names = [name for name in histories if name != "H0_flat"]
    nonflat_presence = {}
    for name in nonflat_names:
        tilted = [
            branch_data[f"{name}__alpha_{alpha:.12f}"]
            for alpha in ANGLES
            if alpha != 0
        ]
        nonflat_presence[name] = any(
            d["max_tidal_contrast"] > 1e-7 and d["max_optical_shear"] > 1e-7
            for d in tilted
        )

    flat = [branch_data[f"H0_flat__alpha_{alpha:.12f}"] for alpha in ANGLES]
    flat_D_error = max(
        np.max(
            np.abs(
                np.asarray(d["D_endpoint"])
                - LAM_END * np.eye(2)
            )
        )
        for d in flat
    )

    checks = {
        **exact_checks,
        "all_branches_completed": len(branch_data) == len(histories) * len(ANGLES),
        "raw_null_drift": max(d["null_drift"] for d in all_diags) < 2e-9,
        "raw_affine_residual": max(d["affine_residual"] for d in all_diags) < 2e-9,
        "raw_parallel_residual": max(d["parallel_residual"] for d in all_diags) < 2e-9,
        "screen_metric_drift": max(d["screen_metric_drift"] for d in all_diags) < 2e-9,
        "screen_ray_drift": max(d["screen_ray_drift"] for d in all_diags) < 2e-9,
        "tidal_symmetry": max(d["tidal_symmetry_drift"] for d in all_diags) < 2e-9,
        "strict_replay_geodesic_screen": convergence_geo < 2e-8,
        "strict_replay_jacobi_phase": convergence_phase < 5e-8,
        "neighbor_ray_absolute": max(d["fd_abs"] for d in all_diags) < 2e-5,
        "neighbor_ray_relative": max(d["fd_rel"] for d in all_diags) < 2e-5,
        "flat_D_equals_lambda_I": flat_D_error < 2e-9,
        "flat_zero_shear": max(d["max_optical_shear"] for d in flat) < 2e-9,
        "radial_singular_values_equal": max(
            d["radial_singular_difference"] for d in radial_diags
        )
        < 2e-8,
        "radial_zero_shear": max(d["radial_shear"] for d in radial_diags) < 2e-8,
        "nonflat_tilted_response_exists": any(nonflat_presence.values()),
        "tilt_reversal_singular_values": reversal_singular < 2e-8,
        "tilt_reversal_shear_norm": reversal_shear < 2e-8,
    }

    if not all(checks.values()):
        landing = "NUMERICAL_OR_TYPE_FAILURE"
    elif all(nonflat_presence.values()):
        landing = "FINITE_PATH_SAME_HISTORY_EMERGENCE_OBSERVED"
    elif any(nonflat_presence.values()):
        landing = "FINITE_PATH_EMERGENCE_HISTORY_DEPENDENT"
    else:
        landing = "LOCAL_ONLY_IN_DECLARED_ATLAS"

    maxima = {
        "null_drift": max(d["null_drift"] for d in all_diags),
        "affine_residual": max(d["affine_residual"] for d in all_diags),
        "parallel_residual": max(d["parallel_residual"] for d in all_diags),
        "screen_metric_drift": max(d["screen_metric_drift"] for d in all_diags),
        "screen_ray_drift": max(d["screen_ray_drift"] for d in all_diags),
        "tidal_symmetry_drift": max(d["tidal_symmetry_drift"] for d in all_diags),
        "convergence_geodesic_screen": convergence_geo,
        "convergence_jacobi_phase": convergence_phase,
        "neighbor_ray_abs": max(d["fd_abs"] for d in all_diags),
        "neighbor_ray_rel": max(d["fd_rel"] for d in all_diags),
        "flat_D_error": float(flat_D_error),
        "radial_singular_difference": max(
            d["radial_singular_difference"] for d in radial_diags
        ),
        "radial_shear": max(d["radial_shear"] for d in radial_diags),
        "tilt_reversal_singular": reversal_singular,
        "tilt_reversal_shear": reversal_shear,
    }

    result = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "landing": landing,
        "checks": checks,
        "symbolic_nonzero_counts": {
            "Gamma": symbolic["nonzero_gamma"],
            "Rlow": symbolic["nonzero_rlow"],
        },
        "histories": {name: data["expressions"] for name, data in histories.items()},
        "angles": list(ANGLES),
        "branch_count": len(branch_data),
        "nonflat_family_response": nonflat_presence,
        "maxima": maxima,
        "branches": branch_data,
        "maximum_conclusion": (
            "branchwise finite-path behavior on four supplied spherical histories only; no "
            "physical history, universal query, nonspherical completion, observation, source, "
            "transfer, X_max, bootstrap, action, matter, mass, or signalling claim"
        ),
    }

    with (HERE / "FINITE_PATH_ATLAS.tsv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    np.savez_compressed(HERE / "FINITE_PATH_SAMPLES.npz", **sample_payload)
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True, default=json_default) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                k: result[k]
                for k in (
                    "status",
                    "landing",
                    "checks",
                    "maxima",
                    "nonflat_family_response",
                )
            },
            indent=2,
            sort_keys=True,
            default=json_default,
        )
    )
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
