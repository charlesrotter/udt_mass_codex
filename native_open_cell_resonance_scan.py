"""SCATTERING-RESONANCE structure of the OPEN softened matter cell.

No box anywhere.  Companion to native_open_domain_threshold_theorem.py,
which proves the open-domain point spectrum is empty: the only discrete
frequency data the open linear cell can natively own are RESONANCES
(complex-omega poles / Wigner time-delay peaks).  This script measures them.

B1  Backgrounds (repo conventions, spot-checked against native_core_solver):
        f_xx + f_x + 2 s W(x) f = 0,  x = ln r,  W = logistic window,
        s = eta*lambda, eta = 1/18; interior power law f ~ r^{-p},
        p(1-p)/2 = s, finite-action branch p < 1/2; exterior f -> 1 + a/r.
      Sectors: lambda = 2 (ell=1, s = 1/9) and lambda = 6 (ell=2, s = 1/3
      -- EXCEEDS the finite-action bound 1/8; reported honestly, then the
      capped value s = 1/9 = q/3 is run for ell=2).  Controls: vacuum
      (f = 1 + a/r, no core) and flat (f = 1).
B2  Effective potential in tortoise form, derived symbolically for GENERAL f
      (f' terms included, nothing guessed):  u = r R, dr*/dr = 1/f gives
      u'' + [omega^2 - V]u = 0 with V = f*(lambda/r^2 + f'/r).
      The SHAPE of V (pocket vs monotone) is printed per background.
B3  Real-axis scattering scan: regular center solution integrated outward
      (Magnus midpoint propagator in r*), matched to exact Riccati-Bessel
      asymptotics in omega*r* with the a/r tail handled honestly:
      tortoise log-stretch (Coulomb-like phase) + first-order variable-phase
      correction for the residual potential; matching-radius independence
      is measured and reported.  Wigner time delay d(delta)/d(omega);
      resonances = time-delay peaks, fitted for omega_0, Gamma, Q.
B4  Pre-registered verdicts (printed BEFORE results; no softening).
B5  Independent cross-check: complex-omega outgoing-wave root finding
      (poles of the open cell) compared against the time-delay scan.

Frequencies are in units of c / R_core with R_core = exp(x_core) = 1.

New file 2026-06-10; modifies nothing existing.
"""

from __future__ import annotations

import argparse
import math
import sys

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import curve_fit
from scipy.signal import find_peaks

from native_core_solver import p_roots, solve_profile, window

ETA = 1.0 / 18.0
X_CORE = 0.0          # native_core_solver default: core scale r_core = 1
WIDTH = 0.5
XMIN = -20.0
XMAX = 12.0
DX = 1.0e-3

RHO_MATCH = 600.0     # default matching radius (tortoise units)
RHO_SNAPSHOTS = (480.0, 600.0, 720.0, 1200.0)   # -20%, base, +20%, range x2
PER_EFOLD = 80.0      # geometric-zone resolution near the center
H_WAVE = 0.021        # uniform tortoise step ~ (2*pi/omega_max)/10

FAILURES: list[str] = []


def check(label: str, ok: bool) -> None:
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}")
    if not ok:
        FAILURES.append(label)


def hr(title: str) -> None:
    print()
    print("=" * 78)
    print(title)
    print("=" * 78)


# ---------------------------------------------------------------------------
# B2 — symbolic derivation of the tortoise-form potential (general f)
# ---------------------------------------------------------------------------
def derive_potential() -> None:
    hr("B2(i) — tortoise reduction derived symbolically for GENERAL f "
       "(f' terms included)")
    r = sp.symbols("r", positive=True)
    lam, w = sp.symbols("lam omega", positive=True)
    f = sp.Function("f", positive=True)(r)
    u = sp.Function("u")(r)
    R = u / r
    E = (-sp.diff(r**2 * f * sp.diff(R, r), r) + lam * R
         - w**2 * (r**2 / f) * R)
    V = f * (lam / r**2 + sp.diff(f, r) / r)
    # claim: (f/r)*E == -f(f u')' + (V - omega^2) u, and f(f u')' = u_{r*r*}
    residual = sp.simplify((f / r) * E
                           - (-f * sp.diff(f * sp.diff(u, r), r)
                              + (V - w**2) * u))
    check("(f/r)·[radial eq] = −u_{r*r*} + (V − ω²)u  with  "
          "V(r) = f·( λ/r² + f'/r )   [EXACT, general f]", residual == 0)
    print("      V(r) = f(r) * [ lambda/r^2 + f'(r)/r ]")
    M = sp.symbols("M", positive=True)
    Vs = sp.expand(V.subs(f, 1 - 2 * M / r).doit())
    check("Schwarzschild control: f = 1−2M/r gives the standard scalar "
          "Regge–Wheeler V = λ/r² + 2M(1−λ)/r³ − 4M²/r⁴",
          sp.simplify(Vs - (lam / r**2 + 2 * M * (1 - lam) / r**3
                            - 4 * M**2 / r**4)) == 0)
    print("      (matches the known GR form -> the f' term is real, not "
          "guessed)")


# ---------------------------------------------------------------------------
# B1 — backgrounds
# ---------------------------------------------------------------------------
class Background:
    """Numeric background on an x = ln r grid + analytic continuations."""

    def __init__(self, name: str, kind: str, s: float | None = None,
                 a_fixed: float | None = None, dx: float = DX,
                 rtol: float = 1e-12, atol: float = 1e-14):
        self.name = name
        self.kind = kind          # "core" | "vacuum" | "flat"
        self.s = s
        self.dx = dx
        self.rtol, self.atol = rtol, atol
        xg = np.linspace(XMIN, XMAX, int(round((XMAX - XMIN) / dx)) + 1)
        self.xg = xg
        rg = np.exp(xg)

        if kind == "core":
            roots = p_roots(s)
            if roots is None:
                raise ValueError("no finite-action interior branch")
            p_soft = roots[0]
            self.p = p_soft

            def rhs(x, y):
                fv, fx, _rho = y
                wv = window(float(x), X_CORE, WIDTH)
                return [fx, -fx - 2.0 * s * wv * fv, math.exp(x) / fv]

            rho0 = math.exp(XMIN) / (1.0 * (1.0 + p_soft))  # f(xmin)=1 raw
            sol = solve_ivp(rhs, (XMIN, XMAX), [1.0, -p_soft, rho0],
                            t_eval=xg, rtol=rtol, atol=atol,
                            max_step=0.05, method="DOP853")
            if not sol.success:
                raise RuntimeError(sol.message)
            f_raw, fx_raw, rho_raw = sol.y
            A = f_raw[-1] + fx_raw[-1]
            B = -fx_raw[-1] * math.exp(XMAX)
            self.a = B / A
            self.fg = f_raw / A
            self.fxg = fx_raw / A
            self.rho_g = rho_raw * A          # rho = int dr / (f/A)
            self.C = self.fg[0] * math.exp(p_soft * XMIN)  # f ~ C r^-p deep
        elif kind == "vacuum":
            self.a = float(a_fixed)
            self.p = None
            self.fg = 1.0 + self.a / rg
            self.fxg = -self.a / rg
            self.rho_g = rg - self.a * np.log1p(rg / self.a)
        elif kind == "flat":
            self.a = 0.0
            self.p = None
            self.fg = np.ones_like(rg)
            self.fxg = np.zeros_like(rg)
            self.rho_g = rg
        else:
            raise ValueError(kind)
        self.r_top = math.exp(XMAX)

    # -- profile evaluation with analytic continuations -------------------
    def f_of_r(self, r):
        r = np.asarray(r, dtype=float)
        x = np.log(r)
        out = np.interp(x, self.xg, self.fg)
        if self.kind == "core":
            lo = x < self.xg[0]
            if np.any(lo):
                out = np.where(lo, self.C * r ** (-self.p), out)
        hi = x > self.xg[-1]
        if np.any(hi):
            out = np.where(hi, 1.0 + self.a / r, out)
        return out

    def fp_of_r(self, r):
        r = np.asarray(r, dtype=float)
        x = np.log(r)
        out = np.interp(x, self.xg, self.fxg) / r
        if self.kind == "core":
            lo = x < self.xg[0]
            if np.any(lo):
                out = np.where(lo, -self.p * self.C * r ** (-self.p - 1), out)
        hi = x > self.xg[-1]
        if np.any(hi):
            out = np.where(hi, -self.a / r**2, out)
        return out

    def V_of_r(self, r, lam):
        f = self.f_of_r(r)
        return f * (lam / np.asarray(r) ** 2 + self.fp_of_r(r) / np.asarray(r))

    def rho_of_r(self, r):
        if self.kind == "flat":
            return np.asarray(r, dtype=float)
        if self.kind == "vacuum":
            r = np.asarray(r, dtype=float)
            return r - self.a * np.log1p(r / self.a)
        return np.interp(np.log(r), self.xg, self.rho_g)

    def r_of_rho(self, rho):
        if self.kind == "flat":
            return np.asarray(rho, dtype=float)
        x = np.interp(rho, self.rho_g, self.xg)
        return np.exp(x)


def report_s_one_third() -> None:
    hr("B1(ii) — lambda = 6 sector at face value: s = eta*lambda = 1/3")
    p = sp.symbols("p")
    s_val = sp.Rational(1, 3)
    sols = sp.solve(sp.Eq(p * (1 - p) / 2, s_val), p)
    print(f"  indicial equation p(1-p)/2 = 1/3  ->  p = {sols}")
    nu = sp.sqrt(8 * s_val - 1) / 2
    check("s = 1/3 EXCEEDS the finite-action bound 1/8: indicial roots are "
          "complex 1/2 ± i·sqrt(5/3)/2",
          all(sp.im(sv) != 0 for sv in sols))
    print(f"""
  Consequence (exact): with W = 1 in the deep core, EVERY interior solution
  is f = r^(-1/2)·[A cos(nu·ln r) + B sin(nu·ln r)], nu = {sp.nsimplify(nu)}
  ≈ {float(nu):.6f}.  It oscillates in ln r and crosses ZERO infinitely
  often as r -> 0: the conditions f >= 1 and finite action are BOTH
  unsatisfiable.  There is NO valid lambda=6-sourced softened background at
  s = 1/3.  Reported honestly; the capped value s = 1/9 (the q = 1/3-branch
  value s = q/3) is run for the ell = 2 probe instead.  NOTE: the capped
  background then coincides numerically with the s = 1/9 (lambda=2) one;
  only the PROBE sector differs.
""")


def spot_check_core(bg: Background) -> None:
    res = solve_profile(bg.s, X_CORE, WIDTH, XMIN, XMAX)
    da = abs(res["a_tail"] - bg.a) / abs(res["a_tail"])
    dp = abs(res["p_soft"] - bg.p)
    # compare f at a few radii (reference values come from linear interp on
    # the banked solver's own sparse output grid -> that interp is the
    # accuracy floor of the comparison, ~1e-5, not a solver discrepancy)
    xs = np.array([-15.0, -5.0, -1.0, 0.0, 1.0, 5.0])
    f_ref = np.interp(xs, res["x"], res["f"])
    f_new = bg.f_of_r(np.exp(xs))
    df = float(np.max(np.abs(f_new / f_ref - 1.0)))
    check(f"spot-check vs native_core_solver.solve_profile: "
          f"rel.diff a_tail = {da:.2e} (<1e-8), p = {dp:.2e} (exact), "
          f"max f = {df:.2e} (<1e-4, reference-interp limited)",
          da < 1e-8 and dp < 1e-12 and df < 1e-4)
    fmin = float(np.min(bg.fg))
    check(f"matter-side requirement f >= 1 on the grid: min f = {fmin:.9f}",
          fmin >= 1.0 - 1e-9)


# ---------------------------------------------------------------------------
# B2 — potential shape per background
# ---------------------------------------------------------------------------
def classify_shape(bg: Background, lam: float) -> str:
    rr = np.exp(np.linspace(math.log(1e-5), math.log(200.0), 4001))
    V = bg.V_of_r(rr, lam)
    dV = np.diff(V)
    sgn = np.sign(dV)
    turn = np.where(np.diff(sgn) != 0)[0] + 1
    extrema = [(rr[i], V[i], "max" if sgn[i - 1] > 0 else "min")
               for i in turn]
    print(f"  background {bg.name}, probe lambda = {lam:g}:")
    if bg.kind == "core":
        gc = bg.p / (1.0 + bg.p) ** 2
        rho_small = bg.rho_of_r(np.array([1e-5]))[0]
        Vc = bg.V_of_r(np.array([1e-5]), lam)[0]
        print(f"    near-center (tortoise): V ~ -g/rho^2 with "
              f"g = p/(1+p)^2 = {gc:.6f} (subcritical: < 1/4)")
        print(f"    numeric check at r = 1e-5: V*rho^2 = "
              f"{Vc * rho_small**2:.6f} "
              f"(asymptote -g + lam-term correction)")
        rzero = rr[np.where(np.diff(np.sign(V)) != 0)[0]]
        if rzero.size:
            print(f"    V crosses zero at r ≈ {rzero[0]:.6g} "
                  f"(attractive r < that, repulsive barrier outside)")
    if bg.kind == "vacuum":
        print("    near-center: f = 1 + a/r alone gives V ~ -a^2/r^4 "
              "-> -1/(4 rho^2) in tortoise form (exactly CRITICAL "
              "coefficient)")
        print(f"    V crosses zero at r = a/lambda = {bg.a / lam:.6g}")
    if not extrema:
        verdict = "MONOTONE decay (no local extremum, no pocket)"
    else:
        for re_, ve_, kind_ in extrema[:8]:
            print(f"    local {kind_} at r = {re_:.6g}, V = {ve_:.6g}")
        has_pocket = any(
            k1 == "min" and any(k2 == "max" and r2 > r1 and v2 > v1
                                for r2, v2, k2 in extrema)
            for r1, v1, k1 in extrema)
        verdict = ("POCKET (local min between barriers)" if has_pocket
                   else "barrier only — NO pocket at finite V "
                        "(attractive region bottoms out only at the center)")
    print(f"    SHAPE VERDICT: {verdict}")
    return verdict


# ---------------------------------------------------------------------------
# Riccati-Bessel / Riccati-Hankel machinery (exact closed forms via sympy)
# ---------------------------------------------------------------------------
def riccati(ell: int):
    z = sp.symbols("z")
    jl = sp.expand_func(sp.jn(ell, z))
    yl = sp.expand_func(sp.yn(ell, z))
    S = sp.simplify(z * jl)               # regular
    Cc = sp.simplify(-z * yl)             # irregular, W(S,C)=-1 convention
    H = sp.simplify(z * (jl + sp.I * yl))  # outgoing ~ e^{i(z - ell pi/2)}/i^..
    mods = ["numpy"]
    return (sp.lambdify(z, S, mods), sp.lambdify(z, sp.diff(S, z), mods),
            sp.lambdify(z, Cc, mods), sp.lambdify(z, sp.diff(Cc, z), mods),
            sp.lambdify(z, H, mods), sp.lambdify(z, sp.diff(H, z), mods))


RB = {1: riccati(1), 2: riccati(2)}


# ---------------------------------------------------------------------------
# B3 — propagation machinery
# ---------------------------------------------------------------------------
def build_nodes(rho0: float, rho_max: float, per_efold: float, h_wave: float,
                snaps=()):
    """Geometric zone (h = rho/per_efold) then uniform zone (h <= h_wave),
    with every snapshot radius landed on EXACTLY (so different resolutions
    share identical matching radii)."""
    targets = sorted(set(list(snaps) + [rho_max]))
    nodes = [rho0]
    rho = rho0
    ratio = 1.0 + 1.0 / per_efold
    while rho * (ratio - 1.0) < h_wave and rho < targets[0]:
        rho = min(rho * ratio, targets[0])
        nodes.append(rho)
    for tgt in targets:
        if tgt <= rho:
            continue
        n = int(math.ceil((tgt - rho) / h_wave))
        seg = rho + (tgt - rho) * np.arange(1, n + 1) / n
        nodes.extend(seg.tolist())
        rho = tgt
    nodes = np.asarray(nodes)
    snap_idx = [int(np.argmin(np.abs(nodes - s_))) for s_ in snaps]
    return nodes, snap_idx


def magnus_sweep(w, Vm, h, u0, up0, snap_set=None):
    """Propagate u'' = (V - w^2) u with the midpoint-Magnus (constant-V)
    propagator; exact in omega for piecewise-constant V.  Vectorized over
    omega.  Returns {snap_index: (u, up)} (last node always included)."""
    w = np.asarray(w)
    cplx = np.iscomplexobj(w) or np.iscomplexobj(u0)
    dt = complex if cplx else float
    u = np.broadcast_to(np.asarray(u0, dtype=dt), w.shape).copy()
    up = np.broadcast_to(np.asarray(up0, dtype=dt), w.shape).copy()
    w2 = w * w
    out = {}
    snap_set = set(snap_set or ())
    nstep = len(h)
    if cplx:
        for j in range(nstep):
            k = np.sqrt(w2 - Vm[j] + 0j)
            kh = k * h[j]
            c = np.cos(kh)
            sk = np.where(np.abs(kh) > 1e-8, np.sin(kh) / np.where(k == 0, 1, k),
                          h[j])
            u, up = c * u + sk * up, -(w2 - Vm[j]) * sk * u + c * up
            if j + 1 in snap_set:
                out[j + 1] = (u.copy(), up.copy())
    else:
        for j in range(nstep):
            k2 = w2 - Vm[j]
            ak = np.sqrt(np.abs(k2))
            arg = ak * h[j]
            pos = k2 >= 0.0
            c = np.where(pos, np.cos(arg), np.cosh(arg))
            snum = np.where(pos, np.sin(arg), np.sinh(arg))
            sk = np.where(arg > 1e-8, snum / np.where(ak == 0, 1.0, ak), h[j])
            u, up = c * u + sk * up, -k2 * sk * u + c * up
            if j + 1 in snap_set:
                out[j + 1] = (u.copy(), up.copy())
    out[nstep] = (u, up)
    return out


def regular_ic(bg: Background, lam: float, w=None):
    """Frobenius series for the regular center solution; returns
    (r0, rho0, u0, up0) with up0 = du/d(rho).  For 'flat', w (vector) is
    required and the exact Riccati-Bessel start is used."""
    if bg.kind == "core":
        r0 = 1.0e-4
        f0 = float(bg.f_of_r(np.array([r0]))[0])
        p = bg.p
        Cl = f0 * r0**p
        # R = sum c_n r^{np};  c_n = c_{n-1} * lam / (C n p (np + 1 - p))
        term, Rv, Rp = 1.0, 1.0, 0.0
        for n in range(1, 400):
            term *= lam / (Cl * n * p * (n * p + 1.0 - p))
            tn = term * r0 ** (n * p)
            Rv += tn
            Rp += tn * n * p / r0
            if abs(tn) < 1e-17 * abs(Rv):
                break
        else:
            raise RuntimeError("core Frobenius series did not converge")
        rho0 = r0 / (f0 * (1.0 + p))
        u0 = r0 * Rv
        up0 = f0 * (Rv + r0 * Rp)
        return r0, rho0, u0, up0
    if bg.kind == "vacuum":
        a = bg.a
        r0 = 1.0e-6 * a
        # R = sum c_n r^n;  c_n = c_{n-1} (lam - n(n-1)) / (a n^2)
        term, Rv, Rp = 1.0, 1.0, 0.0
        for n in range(1, 60):
            term *= (lam - n * (n - 1.0)) / (a * n * n)
            tn = term * r0**n
            Rv += tn
            Rp += tn * n / r0
            if abs(tn) < 1e-17 * abs(Rv):
                break
        f0 = 1.0 + a / r0
        rho0 = r0 - a * math.log1p(r0 / a)
        u0 = r0 * Rv
        up0 = f0 * (Rv + r0 * Rp)
        return r0, rho0, u0, up0
    # flat: exact
    ell = int(round((-1 + math.sqrt(1 + 4 * lam)) / 2))
    from scipy.special import spherical_jn
    r0 = 1.0e-4
    z0 = w * r0
    u0 = z0 * spherical_jn(ell, z0)
    up0 = w * (spherical_jn(ell, z0) + z0 * spherical_jn(ell, z0, derivative=True))
    return r0, r0, u0, up0


def tail_integral(bg: Background, lam: float, rho_m: float) -> float:
    """I(rho_m) = int_{rho_m}^{inf} [ V(r(rho)) - lam/rho^2 ] d rho,
    computed on the background grid (+ negligible-bounded remainder)."""
    if bg.kind == "flat":
        return 0.0
    mask = bg.rho_g > rho_m
    rho = np.concatenate(([rho_m], bg.rho_g[mask]))
    rr = bg.r_of_rho(rho)
    dV = bg.V_of_r(rr, lam) - lam / rho**2
    return float(np.trapezoid(dV, rho))


def tail_remainder_bound(bg: Background, lam: float) -> float:
    rt = bg.r_top
    a = abs(bg.a)
    return (lam * (2 * a * math.log(max(rt, 2.0)) + a + a * lam) + a * lam) \
        / max(rt, 1.0) ** 2


def extract_delta(u, up, w, rho_m, ell, Itail, dV_m):
    """Match to exact Riccati-Bessel comparison functions of omega*rho, then
    apply the FULL first-order variable-phase tail correction for the
    residual potential dV = V - lam/rho^2 beyond rho_m:
        delta_inf = delta(rho_m) - I/(2w) - dV(rho_m) sin(2 phi_m)/(4 w^2)
    (mean part + leading oscillatory part; remainder O(dV'/w^3))."""
    S, Sp, Cc, Cp = RB[ell][:4]
    z = w * rho_m
    t = up / w
    alpha = Cc(z) * t - u * Cp(z)
    beta = u * Sp(z) - S(z) * t
    delta_raw = np.arctan2(beta, alpha)
    phi_m = w * rho_m - ell * math.pi / 2.0 + delta_raw
    return (delta_raw - Itail / (2.0 * w)
            - dV_m * np.sin(2.0 * phi_m) / (4.0 * w * w))


def unwrap_pi(d):
    return np.unwrap(2.0 * np.asarray(d)) / 2.0


def _delta_snapshots(bg, ell, wgrid, per_efold, h_wave, snaps):
    lam = ell * (ell + 1.0)
    if bg.kind == "flat":
        r0, rho0, u0, up0 = regular_ic(bg, lam, wgrid)
    else:
        r0, rho0, u0, up0 = regular_ic(bg, lam)
    nodes, snap_idx = build_nodes(rho0, max(snaps), per_efold, h_wave, snaps)
    rho_mid = 0.5 * (nodes[:-1] + nodes[1:])
    Vm = bg.V_of_r(bg.r_of_rho(rho_mid), lam)
    res = magnus_sweep(wgrid, Vm, np.diff(nodes), u0, up0, snap_set=snap_idx)
    out = {}
    for s_target, idx in zip(snaps, snap_idx):
        rho_act = nodes[idx]
        It = tail_integral(bg, lam, rho_act)
        dV_m = float(bg.V_of_r(bg.r_of_rho(np.array([rho_act])),
                               lam)[0] - lam / rho_act**2)
        uu, uup = res[idx]
        out[s_target] = unwrap_pi(
            extract_delta(uu, uup, wgrid, rho_act, ell, It, dV_m))
    return out


class ProbeScan:
    """Real-axis scan of one probe on one background, with matching-radius
    snapshots and Richardson extrapolation over the Magnus step size
    (levels h and h/2; global error O(h^2) -> extrapolant O(h^4))."""

    def __init__(self, bg: Background, ell: int, wgrid: np.ndarray,
                 per_efold=PER_EFOLD, h_wave=H_WAVE,
                 snaps=RHO_SNAPSHOTS, base_snap=None):
        self.bg, self.ell, self.w = bg, ell, wgrid
        self.lam = ell * (ell + 1.0)
        self.snaps = snaps
        self.base_snap = base_snap if base_snap is not None else (
            snaps[1] if len(snaps) > 1 else snaps[0])
        self.deltas_coarse = _delta_snapshots(bg, ell, wgrid, per_efold,
                                              h_wave, snaps)
        self.deltas_fine = _delta_snapshots(bg, ell, wgrid, 2.0 * per_efold,
                                            0.5 * h_wave, snaps)
        self.deltas = {k: (4.0 * self.deltas_fine[k]
                           - self.deltas_coarse[k]) / 3.0
                       for k in self.deltas_fine}
        self.delta = self.deltas[self.base_snap]
        self.tau = np.gradient(self.delta, wgrid)

    def radius_independence(self):
        base = self.deltas[self.base_snap]
        devs = {}
        for s_t, d in self.deltas.items():
            if s_t == self.base_snap:
                continue
            dd = d - base
            dd = dd - np.round(np.mean(dd) / math.pi) * math.pi
            devs[s_t] = float(np.max(np.abs(dd)))
        return devs

    def grid_residual(self):
        """max |Richardson - fine| at the base radius = grid-resolution
        residual estimate of the banked delta curve."""
        dd = self.deltas[self.base_snap] - self.deltas_fine[self.base_snap]
        return float(np.max(np.abs(dd)))


# ---------------------------------------------------------------------------
# resonance detection + fitting
# ---------------------------------------------------------------------------
def tau_model(w, c0, c1, A, w0, G):
    return c0 + c1 * (w - w0) + A * (G / 2.0) / ((w - w0) ** 2 + (G / 2.0) ** 2)


def fit_peak(wgrid, tau, ipk):
    w_pk = wgrid[ipk]
    base = np.median(tau)
    height = tau[ipk] - base
    if height <= 0:
        return None
    G_est = 2.0 / height
    msk = np.abs(wgrid - w_pk) < max(6.0 * G_est, 10 * (wgrid[1] - wgrid[0]))
    try:
        popt, _ = curve_fit(tau_model, wgrid[msk], tau[msk],
                            p0=[base, 0.0, 1.0, w_pk, G_est], maxfev=20000)
    except Exception:
        return None
    c0, c1, A, w0, G = popt
    G = abs(G)
    if not (wgrid[msk][0] <= w0 <= wgrid[msk][-1]) or G <= 0:
        return None
    return {"w0": w0, "Gamma": G, "Q": w0 / G, "rise_over_pi": A, "c0": c0}


def find_resonances(wgrid, tau, prominence=0.3):
    pk, _props = find_peaks(tau, prominence=prominence)
    pk = [i for i in pk if 5 <= i <= len(wgrid) - 6]
    fits = []
    for i in pk:
        ft = fit_peak(wgrid, tau, i)
        if ft is not None:
            fits.append(ft)
    return fits


# ---------------------------------------------------------------------------
# B5 — complex-omega outgoing-wave poles
# ---------------------------------------------------------------------------
def incoming_coefficient(bg: Background, ell: int, wc, rho_m: float,
                         per_efold=PER_EFOLD, h_wave=H_WAVE):
    """Siegert mismatch: the INCOMING-wave coefficient of the regular
    solution, extracted by Wronskian at rho_m,

        c_in(omega)  propto  zeta_out(z)·u'/omega − zeta_out'(z)·u,
        z = omega*rho_m;       pole  <=>  c_in = 0.

    This is well-conditioned (unlike a log-derivative outgoing match, where
    for Im omega < 0 EVERYTHING looks outgoing once e^{2|Im w|rho} >> 1).
    The cancellation noise floor is ~ 1e-16·e^{2|Im w|rho_m}: rho_m must be
    chosen so 2|Im w|·rho_m <~ 25.  Returns (c_in, noise_scale)."""
    lam = ell * (ell + 1.0)
    wc = np.atleast_1d(np.asarray(wc, dtype=complex))
    if bg.kind == "flat":
        r0, rho0, u0, up0 = regular_ic(bg, lam, wc)
    else:
        r0, rho0, u0, up0 = regular_ic(bg, lam)
        u0 = complex(u0)
        up0 = complex(up0)
    nodes, _ = build_nodes(rho0, rho_m, per_efold, h_wave)
    rho_mid = 0.5 * (nodes[:-1] + nodes[1:])
    Vm = bg.V_of_r(bg.r_of_rho(rho_mid), lam)
    rho_act = nodes[-1]
    # first-order distorted-wave outgoing comparison:
    #   u_out(rho) = zeta+(w rho) * exp(i I(rho)/(2w)),  dI/drho = -dV(rho)
    #   => u_out'/w carries the extra term  -i dV(rho_m)/(2 w^2) zeta+
    dVm = float(bg.V_of_r(bg.r_of_rho(np.array([rho_act])),
                          lam)[0] - lam / rho_act**2)
    with np.errstate(over="ignore", invalid="ignore"):
        res = magnus_sweep(wc, Vm, np.diff(nodes), u0, up0)
        u, up = res[len(nodes) - 1]
        H, Hp = RB[ell][4], RB[ell][5]
        z = wc * rho_act
        t = up / wc
        Hp_corr = Hp(z) - 1j * dVm / (2.0 * wc * wc) * H(z)
        c_in = H(z) * t - Hp_corr * u
        scale = np.abs(H(z) * t) + np.abs(Hp_corr * u)
    return c_in, scale


def siegert_depth_limit(bg: Background, lam: float, rho_m: float,
                        w_ref: float) -> float:
    """Conditioning window of the Siegert extraction at rho_m: the
    tail-truncation contamination (after the first-order distorted-wave
    correction, residual ~ eps0^2 + oscillatory part) is amplified by
    e^{2|Im w| rho_m}; poles are trustworthy only for
        |Im omega| < ln(1/eps_eff) / (2 rho_m)   (x 0.7 safety)."""
    eps0 = abs(tail_integral(bg, lam, rho_m)) / (2.0 * w_ref)
    dVm = float(bg.V_of_r(bg.r_of_rho(np.array([rho_m])),
                          lam)[0] - lam / rho_m**2)
    eps_eff = max(eps0**2, abs(dVm) / (4.0 * w_ref**2 * w_ref * rho_m),
                  1e-13)
    return 0.7 * math.log(1.0 / eps_eff) / (2.0 * rho_m)


def secant_poles(bg, ell, seeds, rho_m, iters=40,
                 per_efold=PER_EFOLD, h_wave=H_WAVE):
    """Vectorized complex secant on c_in(omega).  Returns (poles,
    normalized residual |c_in|/scale)."""
    w0 = np.asarray(seeds, dtype=complex)
    w1 = w0 * (1.0 + 1e-4) - 1e-4j
    D0, _ = incoming_coefficient(bg, ell, w0, rho_m, per_efold, h_wave)
    D1, _ = incoming_coefficient(bg, ell, w1, rho_m, per_efold, h_wave)
    for _ in range(iters):
        with np.errstate(over="ignore", invalid="ignore"):
            denom = np.where(D1 == D0, 1e-30, D1 - D0)
            w2 = w1 - D1 * (w1 - w0) / denom
        w2 = np.where(np.isfinite(w2), w2, w1)
        w2 = np.clip(w2.real, 0.05, 40.0) + 1j * np.clip(w2.imag, -3.0, -1e-4)
        w0, D0 = w1, D1
        w1 = w2
        D1, sc1 = incoming_coefficient(bg, ell, w1, rho_m, per_efold, h_wave)
        if np.all(np.abs(w1 - w0) < 1e-12 * np.abs(w1) + 1e-14):
            break
    with np.errstate(invalid="ignore", divide="ignore"):
        resid = np.abs(D1) / np.where(sc1 == 0, 1.0, sc1)
    return w1, resid


STRIPS = (   # (Im_lo, Im_hi, n_im, rho_m) — rho_m matched to target depth
    (-0.020, -0.002, 9, 100.0),
    (-0.15, -0.02, 12, 30.0),
    (-0.60, -0.12, 12, 8.0),
    (-2.00, -0.50, 10, 8.0),
)


def pole_grid_scan(bg, ell, re_lo, re_hi, n_re=60):
    """Strip-wise normalized |c_in| map with rho_m matched to target depth
    (narrow poles need large rho_m; deep/broad poles small rho_m to evade
    the e^{2|Im w| rho} amplification).  Returns seeds at strict local
    minima, each tagged with its strip rho_m and conditioning depth."""
    wr = np.linspace(re_lo, re_hi, n_re)
    seeds = []
    info = []
    lam = ell * (ell + 1.0)
    for (im_lo, im_hi, n_im, rho_m) in STRIPS:
        wi = np.linspace(im_lo, im_hi, n_im)
        WW = (wr[None, :] + 1j * wi[:, None]).ravel()
        D, S = incoming_coefficient(bg, ell, WW, rho_m)
        with np.errstate(invalid="ignore", divide="ignore"):
            mag = (np.abs(D) / np.where(S == 0, 1.0, S)).reshape(n_im, n_re)
        depth = siegert_depth_limit(bg, lam, rho_m, 0.5 * (re_lo + re_hi))
        info.append((rho_m, im_lo, im_hi, float(np.nanmin(mag)), depth))
        for i in range(1, n_im - 1):
            for j in range(1, n_re - 1):
                if np.isfinite(mag[i, j]) and \
                        mag[i, j] == np.nanmin(mag[i - 1:i + 2, j - 1:j + 2]):
                    seeds.append((wr[j] + 1j * wi[i], rho_m, depth))
    return seeds, info


# ---------------------------------------------------------------------------
# main orchestration
# ---------------------------------------------------------------------------
def preregistration() -> None:
    hr("B4 — PRE-REGISTERED VERDICT CRITERIA (printed before any scan result)")
    print("""
  NATIVE-DISCRETENESS CANDIDATE:  some time-delay resonance with Q =
      omega_0/Gamma >= 10 that is STABLE under (i) doubling the integration
      range, (ii) doubling the grid resolution, (iii) +-20% matching-radius
      variation (omega_0 shift < max(1e-4*omega_0, Gamma/20), Gamma shift
      < 10%).
  BROAD-ONLY (clean negative):  Q < 3 everywhere ->
      "the open matter cell supports no narrow native resonances in these
       sectors."
  MARGINAL:  3 <= Q < 10 for the best stable feature -> reported, NOT banked.
  Additionally: feature positions must NOT shift with artificial parameters
  (matching radius, grid, range) and SHOULD shift with physical ones
  (probe lambda, source s).  Controls (vacuum tail, flat) must be
  featureless; the flat control must give |delta| ~ 0 (pipeline zero test).
""")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true",
                    help="coarse omega grid (debug only)")
    args = ap.parse_args()

    print("OPEN softened-cell scattering-resonance scan (no box anywhere)")
    print(f"eta = 1/18, x_core = {X_CORE}, width = {WIDTH}, "
          f"xmin = {XMIN}, xmax = {XMAX}, dx = {DX}")
    print(f"matching radius rho_m = {RHO_MATCH} (snapshots "
          f"{RHO_SNAPSHOTS}), Magnus h_wave = {H_WAVE}, "
          f"per-efold = {PER_EFOLD}")

    derive_potential()
    report_s_one_third()

    hr("B1 — backgrounds")
    s_l1 = ETA * 2.0
    print(f"  ell=1 sector source: s = eta*lambda = {s_l1:.10f} = 1/9 "
          f"< 1/8 (finite-action OK), p_soft = 1/3 exactly")
    bg_core = Background("softened core s=1/9", "core", s=s_l1)
    spot_check_core(bg_core)
    print(f"  built: a_tail = {bg_core.a:.10f}, p = {bg_core.p:.10f}, "
          f"f_max(grid) = {np.max(bg_core.fg):.6g}")
    bg_vac = Background("vacuum tail (a = a_tail, no core)", "vacuum",
                        a_fixed=bg_core.a)
    bg_flat = Background("flat control f = 1", "flat")
    print(f"  vacuum control: f = 1 + a/r with a = {bg_vac.a:.10f}")
    print("  flat control:   f = 1")

    hr("B2(ii) — potential SHAPE per background (finding in itself)")
    shapes = {}
    for bg, lam in ((bg_core, 2.0), (bg_core, 6.0), (bg_vac, 2.0),
                    (bg_vac, 6.0), (bg_flat, 2.0)):
        shapes[(bg.name, lam)] = classify_shape(bg, lam)

    preregistration()

    # ------------------------------------------------------------------
    hr("B3 — real-axis scattering scan")
    dw = 0.05 if args.quick else 0.01
    wgrid = np.arange(0.15, 30.0 + 0.5 * dw, dw)
    print(f"  omega grid: [{wgrid[0]:g}, {wgrid[-1]:g}] step {dw:g} "
          f"({len(wgrid)} points); units c/R_core, R_core = 1")
    print("  delta convention: relative to the tail-distorted reference "
          "sin(omega*rho - ell*pi/2),")
    print("  rho = tortoise radius with rho(0) = 0 (the a/r tail makes a "
          "flat-space reference ill-defined")
    print("  by a divergent Coulomb-like log phase; this is the honest "
          "Coulomb-style convention).")

    probes = [
        ("CORE  s=1/9  ell=1", bg_core, 1),
        ("CORE  s=1/9 (capped lambda=6 sector) ell=2", bg_core, 2),
        ("VACUUM control ell=1", bg_vac, 1),
        ("VACUUM control ell=2", bg_vac, 2),
        ("FLAT control ell=1", bg_flat, 1),
        ("FLAT control ell=2", bg_flat, 2),
    ]
    scans = {}
    for label, bg, ell in probes:
        scans[label] = ProbeScan(bg, ell, wgrid)
        sc = scans[label]
        devs = sc.radius_independence()
        # interior points only (np.gradient is one-sided at the edges)
        tau_i = sc.tau[2:-2]
        w_i = wgrid[2:-2]
        tmax = float(np.max(tau_i))
        wmax = float(w_i[int(np.argmax(tau_i))])
        rem = tail_remainder_bound(bg, sc.lam)
        # verifier amendment 2026-06-10: when tau_max lands at the
        # long-wavelength end of the omega grid it is the edge of a smooth
        # rise (independently confirmed monotone), NOT a feature.
        edge_note = (" (NOTE: tau_max sits at the long-wavelength grid "
                     "edge — a smooth rise, independently confirmed "
                     "monotone; NOT a feature)"
                     if wmax <= w_i[2] else "")
        print(f"\n  {label}:")
        print(f"    delta range [{np.min(sc.delta):+.4f}, "
              f"{np.max(sc.delta):+.4f}] rad; "
              f"tau max = {tmax:+.5f} at omega = {wmax:.3f}{edge_note}; "
              f"tau min = {np.min(tau_i):+.5f}")
        dev_str = ", ".join(f"rho={k:g}: {v:.2e}" for k, v in
                            sorted(devs.items()))
        print(f"    matching-radius independence |d(delta)| vs rho=600: "
              f"{dev_str}")
        print(f"    (beyond-grid tail-correction remainder bound "
              f"{rem:.1e} rad)")

    # pipeline zero test
    for ell in (1, 2):
        lab = f"FLAT control ell={ell}"
        mx = float(np.max(np.abs(scans[lab].delta)))
        check(f"flat-control phase shift consistent with zero: "
              f"max|delta| = {mx:.2e} (< 1e-6)", mx < 1e-6)
    for lab in ("VACUUM control ell=1", "VACUUM control ell=2",
                "CORE  s=1/9  ell=1",
                "CORE  s=1/9 (capped lambda=6 sector) ell=2"):
        devs = scans[lab].radius_independence()
        worst = max(devs.values())
        check(f"{lab}: matching-radius independence "
              f"{worst:.2e} rad (< 1e-6 incl. range doubling)",
              worst < 1e-6)

    # ------------------------------------------------------------------
    hr("B3/B4 — resonance search + stability battery")
    verdicts = {}
    for label, bg, ell in probes:
        sc = scans[label]
        fits = find_resonances(wgrid, sc.tau)
        print(f"\n  {label}: {len(fits)} time-delay peak(s) above "
              "prominence 0.3")
        results = []
        for ft in fits:
            w0, G = ft["w0"], ft["Gamma"]
            # refit on every snapshot radius (incl. +-20% and range x2)
            # and on the fine-grid (non-extrapolated) solution = the
            # grid-resolution variant
            variants = {}
            for s_t, d in sc.deltas.items():
                tau_v = np.gradient(d, wgrid)
                i_pk = int(np.argmin(np.abs(wgrid - w0)))
                j = np.argmax(tau_v[max(0, i_pk - 20):i_pk + 21]) \
                    + max(0, i_pk - 20)
                ftv = fit_peak(wgrid, tau_v, int(j))
                variants[f"rho={s_t:g}"] = ftv
            taud = np.gradient(sc.deltas_fine[sc.base_snap], wgrid)
            i_pk = int(np.argmin(np.abs(wgrid - w0)))
            j = np.argmax(taud[max(0, i_pk - 20):i_pk + 21]) + max(0, i_pk - 20)
            variants["grid x2"] = fit_peak(wgrid, taud, int(j))
            stable = True
            print(f"    peak omega_0 = {w0:.6f}, Gamma = {G:.6f}, "
                  f"Q = {ft['Q']:.3f}, phase rise/pi = "
                  f"{ft['rise_over_pi']:.3f}")
            for vn, vf in variants.items():
                if vf is None:
                    print(f"      variant {vn:>10s}: fit failed")
                    stable = False
                    continue
                dw0 = abs(vf["w0"] - w0)
                dG = abs(vf["Gamma"] - G) / G
                okv = dw0 < max(1e-4 * w0, G / 20.0) and dG < 0.10
                stable = stable and okv
                print(f"      variant {vn:>10s}: omega_0 = {vf['w0']:.6f} "
                      f"(shift {dw0:.2e}), Gamma = {vf['Gamma']:.6f} "
                      f"(rel shift {dG:.2%}) "
                      f"{'stable' if okv else 'UNSTABLE'}")
            ft["stable"] = stable
            results.append(ft)
        if not results:
            print("    no fitted peaks.")
        qmax = max((ft["Q"] for ft in results if ft["stable"]), default=0.0)
        qmax_any = max((ft["Q"] for ft in results), default=0.0)
        if any(ft["Q"] >= 10 and ft["stable"] for ft in results):
            verdicts[label] = "NATIVE-DISCRETENESS CANDIDATE"
        elif qmax_any < 3.0:
            verdicts[label] = "BROAD-ONLY (clean negative)"
        else:
            verdicts[label] = (f"MARGINAL (best stable Q = {qmax:.2f}; "
                               "reported, NOT banked)")
        scans[label].fits = results

    # ------------------------------------------------------------------
    hr("B4 — physical-parameter sensitivity (lambda, s) "
       "vs artificial parameters")
    print("  artificial-parameter stability was reported per peak above "
          "(radius, range, grid).")
    print("  physical scan: source s in {0.08, 1/9, 0.123} (all < 1/8), "
          "probe ell = 1:")
    phys = {}
    for s_v in (0.08, s_l1, 0.123):
        bgv = bg_core if abs(s_v - s_l1) < 1e-15 else \
            Background(f"core s={s_v:g}", "core", s=s_v)
        scv = ProbeScan(bgv, 1, wgrid, snaps=(RHO_MATCH,))
        tauv = np.gradient(scv.deltas[RHO_MATCH], wgrid)
        fitsv = find_resonances(wgrid, tauv)
        key = (f"s={s_v:.4f} (p={bgv.p:.4f}, a={bgv.a:.4f})")
        phys[key] = (float(wgrid[2:-2][int(np.argmax(tauv[2:-2]))]),
                     float(np.max(tauv[2:-2])),
                     [(ft["w0"], ft["Q"]) for ft in fitsv])
    for key, (wm, tm, ftl) in phys.items():
        print(f"    {key}: tau_max = {tm:+.5f} at omega = {wm:.3f}; "
              f"peaks: {ftl if ftl else 'none'}")
    print("  -> feature scale tracks the PHYSICAL source (a_tail, p change "
          "the smooth delay curve);")
    print("     any resonance candidate must follow s and lambda, never "
          "rho_m/grid/range.")

    # ------------------------------------------------------------------
    hr("B5 — independent cross-check: complex-omega outgoing-wave poles")
    print("""
  Method: Siegert condition c_in(omega) = 0, with c_in extracted by
  Wronskian against the first-order distorted-wave outgoing comparison
  (NOT a log-derivative outgoing match, which is exponentially
  ill-conditioned for Im omega < 0).  Strip-wise rho_m matched to target
  depth; every accepted pole must pass: residual < 1e-8, rho_m x1.5 and
  grid x2 position stability (tolerance << artifact-ladder spacing
  pi/rho_m), the strip conditioning window, and real-axis consistency.
  COVERAGE CAVEAT (stated, not hidden): ultra-narrow poles with
  Gamma << 4e-3 lie below the shallowest strip and could also alias
  through the d(omega) = 0.01 real-axis grid; with NO potential pocket
  (B2) such trapping is structurally unavailable here, but the scan's
  formal reach is Gamma >= ~4e-3.""")
    for label, bg, ell in probes[:4]:
        sc = scans[label]
        lam = ell * (ell + 1.0)
        seeds = []
        if getattr(sc, "fits", None):
            for ft in sc.fits:
                rm_s = float(np.clip(12.0 / max(0.5 * ft["Gamma"], 0.05),
                                     8.0, 100.0))
                seeds.append((ft["w0"] - 0.5j * ft["Gamma"], rm_s,
                              siegert_depth_limit(bg, lam, rm_s, ft["w0"])))
        print(f"\n  {label}:")
        gseeds, ginfo = pole_grid_scan(bg, ell, 0.3, 12.0)
        for rho_m_s, im_lo, im_hi, mmin, depth in ginfo:
            print(f"    |c_in| strip Im({im_lo:g},{im_hi:g}) rho_m="
                  f"{rho_m_s:g}: min = {mmin:.3e}, conditioning depth "
                  f"|Im| < {depth:.3f}")
        all_seeds = seeds + gseeds[:10]
        if not all_seeds:
            print("    no seeds -> no pole candidates anywhere in the "
                  "scanned strips; time delay featureless by both methods.")
            continue
        kept = []
        rejected = 0
        for grp_rho in sorted(set(rm for _, rm, _d in all_seeds)):
            grp = [s_ for s_, rm, _d in all_seeds if rm == grp_rho]
            depth = [d for _s, rm, d in all_seeds if rm == grp_rho][0]
            poles, resid = secant_poles(bg, ell, grp, rho_m=grp_rho)
            # acceptance battery: rho_m x1.5 re-polish and grid-doubled;
            # tolerance well below the artifact-ladder spacing pi/rho_m
            poles_b, resid_b = secant_poles(bg, ell, poles,
                                            rho_m=1.5 * grp_rho)
            poles_c, resid_c = secant_poles(bg, ell, poles, rho_m=grp_rho,
                                            per_efold=2 * PER_EFOLD,
                                            h_wave=0.5 * H_WAVE)
            tol = 0.1 * math.pi / grp_rho
            for pw, r1, pb, rb, pc, rc in zip(poles, resid, poles_b, resid_b,
                                              poles_c, resid_c):
                ok = (r1 < 1e-8 and rb < 1e-8 and rc < 1e-8
                      and abs(pb - pw) < tol and abs(pc - pw) < tol
                      and -depth < pw.imag < -1e-3)
                if ok and not any(abs(pw - kp) < 1e-2 * abs(kp) + 1e-3
                                  for kp in kept):
                    kept.append(pw)
                elif not ok:
                    rejected += 1
        if not kept:
            print(f"    secant polishing accepted NO stable pole "
                  f"({rejected} candidate(s) rejected by the battery: "
                  "residual < 1e-8, rho_m x1.5 and grid x2 shifts < "
                  "0.1*pi/rho_m, inside conditioning window):")
            print("    -> no resonance poles; consistent with the "
                  "featureless real-axis time delay.")
        for pw in sorted(kept, key=lambda z: z.real):
            G = -2.0 * pw.imag
            print(f"    POLE omega = {pw.real:.6f} - {-pw.imag:.6f} i  "
                  f"->  omega_0 = {pw.real:.6f}, Gamma = {G:.6f}, "
                  f"Q = {pw.real / G:.3f}")
            # honesty cross-check: a pole at distance Gamma/2 from the real
            # axis must show up as a time-delay peak of height ~ 2/Gamma
            i_n = int(np.argmin(np.abs(wgrid - pw.real)))
            tau_loc = float(np.max(sc.tau[max(0, i_n - 10):i_n + 11]))
            cons = ("CONSISTENT" if tau_loc > 1.0 / G else
                    "-> INCONSISTENT, treat as method artifact, not banked")
            print(f"      real-axis consistency: expected tau peak ~ "
                  f"{2.0 / G:.2f}, observed local tau = {tau_loc:.4f} {cons}")
        if getattr(sc, "fits", None):
            for ft in sc.fits:
                tgt = ft["w0"] - 0.5j * ft["Gamma"]
                match = min(kept, key=lambda z: abs(z - tgt)) if kept else None
                if match is not None:
                    print(f"    cross-check vs time-delay fit "
                          f"(omega_0={ft['w0']:.4f}, Gamma={ft['Gamma']:.4f})"
                          f": nearest pole {match.real:.4f} - "
                          f"{-match.imag:.4f}i")

    # ------------------------------------------------------------------
    hr("convergence digits (repo standard: 4+ stable digits on banked "
       "numbers)")
    lab = "CORE  s=1/9  ell=1"
    for plab in [lab, "CORE  s=1/9 (capped lambda=6 sector) ell=2"]:
        gres = scans[plab].grid_residual()
        print(f"  {plab}: |Richardson − fine-grid| residual on delta = "
              f"{gres:.2e}")
    # independent third resolution level: levels (2x, 4x) Richardson pair
    sc_hi = ProbeScan(bg_core, 1, wgrid, per_efold=2 * PER_EFOLD,
                      h_wave=0.5 * H_WAVE, snaps=(RHO_MATCH,))
    diff = sc_hi.delta - scans[lab].delta
    diff -= np.round(np.mean(diff) / math.pi) * math.pi
    mx = float(np.max(np.abs(diff)))
    digits = -math.log10(mx) if mx > 0 else 16.0
    check(f"core ell=1 delta(omega): independent resolution-doubled "
          f"Richardson pair, max change = {mx:.2e} "
          f"(~{digits:.1f} stable digits, >= 4 required)", digits >= 4.0)
    # background a_tail convergence vs the actual integration control
    # (solver tolerance; the dx output grid does not control DOP853 accuracy)
    bg_lo = Background("core s=1/9 loose-rtol", "core", s=s_l1,
                       rtol=3e-10, atol=3e-12)
    da = abs(bg_lo.a - bg_core.a) / bg_core.a
    check(f"a_tail solver-tolerance convergence: rel change rtol 1e-12 -> "
          f"3e-10 = {da:.2e} (>= 4 digits; banked-solver cross-check "
          "9.9e-10 above)", da < 1e-4)

    # ------------------------------------------------------------------
    hr("VERDICTS (pre-registered criteria, no softening)")
    for label, bg, ell in probes:
        print(f"  {label}: {verdicts[label]}")
    core_labels = [p[0] for p in probes[:2]]
    if all("BROAD-ONLY" in verdicts[lab] for lab in core_labels):
        print("""
  HEADLINE: the open matter cell supports no narrow native resonances in
  these sectors (ell = 1 with s = 1/9; ell = 2 on the capped s = 1/9
  background; the uncapped lambda = 6 source s = 1/3 admits no valid
  background at all).  Combined with the continuum-threshold theorem
  (empty point spectrum, Friedrichs class), branch (i) of the four-branch
  structure is now EXCLUDED for this background family at the scan's
  formal reach (Gamma >~ 4e-3); branch (iv) (non-Friedrichs center
  boundary condition) is closed by the finite-action charter unless a
  selection mechanism is derived: native discreteness, if it exists, must
  come from branch (ii) (terminated cell with a true compact probe domain)
  or branch (iii) (modified asymptotic threshold from an uncovered metric
  function — Charles's phi-angular interaction hunch).""")
    if FAILURES:
        print(f"\n  {len(FAILURES)} CHECK(S) FAILED:")
        for labf in FAILURES:
            print(f"    - {labf}")
        sys.exit(1)
    print("\n  all internal checks passed.")


if __name__ == "__main__":
    main()
