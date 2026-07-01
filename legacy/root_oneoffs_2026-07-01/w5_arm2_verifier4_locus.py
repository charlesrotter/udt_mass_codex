#!/usr/bin/env python3
"""W5 ARM-2 — VERIFIER 4 (ADVERSARIAL): the "locus nulls" (claim 5).

Date: 2026-06-12.  Blind adversarial verifier; NEW file, edits nothing.
Imports ONLY the committed w4b_verifier_lib (vl.Member, vl.Yr, vl.Yru,
vl.flow).  The claimant scripts w5_arm2_lib.py / w5_arm2_coupled.py
were READ to replicate setups; ALL analysis code below is my own.

ATTACK TARGETS (W5 Arm-2 claim 5, "locus nulls"):
 (a) no trapping / no new locus-localized pencil states; nneg 1 -> 0
     smoothly; localization CM stays away from the locus.
 (b) no f-pinning at f = 2 kappa in the coupled (f,w) system; the
     claimant's d(T) at kappa=3 (M1 t5, ON, amp .05) drifts AWAY
     (0.1917 -> 0.1953 -> 0.1971 over T_end = 6 xmax) and max f/f_b
     reaches 2.353.

MY PROBES:
 P1 Agmon-distance localization on the full-domain OFF dressed pencil
    (M1, kappa = 1.0 and 2.0, dominant-b ray + seal-adjacent ray):
    own FD assembly (Nt = 4000 + doubling check at Nt = 8000), lowest
    6 eigenpairs; Agmon weight rho_A(t) = |Int_{t_loc}^t
    sqrt(max(q - w2 m, 0)/p) ds| from the locus t_loc (f = 2 kappa,
    first crossing from the weld); test |psi| <= C e^{-rho_A} into the
    flipped cap f < 2 kappa, and the m-weighted mode mass fraction in
    the cap.  TRAPPED state = mass near t_loc + weak Agmon suppression.
 P2 eigenvalue-count anomaly scan kappa in (0.5, 0.767, 1.0, 1.45,
    2.0, 2.5): untruncated (W5) vs truncated species-OFF (W4) pencil
    spectra mode-by-mode (each about ITS OWN dressed equilibrium, the
    claimant's comparability convention), nneg counts, unmatched-level
    detector.
 P3 long-T coupled pinning: faithful reimplementation of the
    claimant's coupled machinery (M1 t5 window, Nt=2000/Nx=768 GeoW5-
    equivalent built here, operator-split (f,w), library-frame weld
    IVP f-slices, n_f = 64, RK4), kappa = +3.0, D_cell ON, amp 0.05,
    T_end = 12 xmax (DOUBLE the claimant's horizon).  Record d(T) at
    every f-update, PLUS sharpened diagnostics the claimant lacked:
    band on the CURRENT f_c, 10th-percentile and min distances, locus
    position drift, and the v=0 dressed-static-cell reference (is the
    f-renormalization just relaxation to the static D_alg-dressed
    cell, or secular?).

Log: /tmp/w5_arm2_verifier4_locus.log.  2026-06-12, verifier-4 agent.
"""
import sys, time
import numpy as np
import scipy.linalg as sla
from scipy.linalg import solve_banded, eigh_tridiagonal
from scipy.integrate import solve_ivp

sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
import w4b_verifier_lib as vl

t0 = time.time()
def log(*a):
    print(*a, flush=True)

GAMMA, CM = 1.0, 0.18413678
CC = 2.0                      # TRUE units
T5 = 2.2357

log("=" * 72)
log("VERIFIER 4 (locus nulls) — building M1 (single flow, two grids)")
log("=" * 72)
SOL = vl.flow(GAMMA, CM)
mem4 = vl.Member(GAMMA, CM, Nu=24, Nt=4000, sol=SOL)
mem8 = vl.Member(GAMMA, CM, Nu=24, Nt=8000, sol=SOL)
log(f"M1 t_stop = {mem4.t_stop:.6f} (claimed 3.598647) "
    f"[{time.time()-t0:.0f}s]")
assert abs(mem4.t_stop - 3.598647) < 5e-6


# ===================================================================
# PART 1 machinery — MY OWN static solver + FD pencil (t-chart)
# ===================================================================
def ray_arrays(mem, k):
    tg = mem.tg
    f = mem.f[:, k]
    p = mem.p[:, k]
    b = mem.b[:, k]
    m = np.exp(-3.0 * tg) / f
    return tg, f, p, b, m


def my_equilibrium(mem, k, kappa, species=True, vinit=None,
                   tol=1e-12, maxit=120):
    """Damped Newton for (p v')' = (1/(8 kappa)) b fac e^{-2v},
    fac = (1 - 2 kappa/f) if species else 1; v(t_stop)=0, v'(0)=0
    (natural).  My own FEM-weak-form assembly."""
    tg, f, p, b, m = ray_arrays(mem, k)
    h = tg[1] - tg[0]
    N = len(tg)
    pm = 0.5 * (p[1:] + p[:-1])
    fac = (1.0 - 2.0 * kappa / f) if species else np.ones(N)
    lam = 1.0 / (8.0 * kappa)
    w = np.full(N, h); w[0] = h / 2; w[-1] = h / 2
    v = np.zeros(N) if vinit is None else vinit.copy()
    for it in range(maxit):
        R = lam * b * fac * np.exp(-2.0 * v)
        F = np.zeros(N)
        F[1:-1] = (pm[1:] * (v[2:] - v[1:-1])
                   - pm[:-1] * (v[1:-1] - v[:-2])) / h - R[1:-1] * w[1:-1]
        F[0] = pm[0] * (v[1] - v[0]) / h - R[0] * w[0]
        F[-1] = v[-1]
        dR = -2.0 * R
        lo = np.zeros(N); di = np.zeros(N); up = np.zeros(N)
        di[1:-1] = -(pm[1:] + pm[:-1]) / h - dR[1:-1] * w[1:-1]
        up[1:-1] = pm[1:] / h
        lo[1:-1] = pm[:-1] / h
        di[0] = -pm[0] / h - dR[0] * w[0]
        up[0] = pm[0] / h
        di[-1] = 1.0
        ab = np.zeros((3, N))
        ab[0, 1:] = up[:-1]; ab[1] = di; ab[2, :-1] = lo[1:]
        try:
            dv = solve_banded((1, 1), ab, -F)
        except Exception:
            return None
        if not np.all(np.isfinite(dv)):
            return None
        s = np.max(np.abs(dv))
        damp = 1.0 if s < 0.5 else 0.5 / s
        v = v + damp * dv
        if not np.all(np.isfinite(v)) or v.min() < -14 or v.max() > 30:
            return None
        if s * damp < tol:
            return v
    return None


def my_pencil(mem, k, kappa, species=True, vbar=None, nev=8):
    """-(p psi')' + q psi = w2 m psi, q = -(1/(4 kappa)) fac e^{-2vb} b
    (OFF branch); Dirichlet at t_stop, natural Neumann at the weld.
    My own P1-FEM tridiagonal assembly + diagonal-mass congruence.
    Returns (w2, psi (N-1, nev), tk, q, m-weights)."""
    tg, f, p, b, m = ray_arrays(mem, k)
    h = tg[1] - tg[0]
    N = len(tg)
    vb = np.zeros(N) if vbar is None else vbar
    fac = (1.0 - 2.0 * kappa / f) if species else np.ones(N)
    q = -(1.0 / (4.0 * kappa)) * fac * np.exp(-2.0 * vb) * b
    pm = 0.5 * (p[1:] + p[:-1])
    w = np.full(N, h); w[0] = h / 2; w[-1] = h / 2
    dmain = np.zeros(N)
    dmain[:-1] += pm / h
    dmain[1:] += pm / h
    dmain += q * w
    doff = -pm / h
    Mw = m * w
    # Dirichlet at t_stop: drop last node
    dm = dmain[:-1]; do = doff[:-1][:-1]
    Mi = 1.0 / np.sqrt(Mw[:-1])
    dmK = dm * Mi ** 2
    offK = doff[:-1] * Mi[:-1] * Mi[1:]
    w2, V = eigh_tridiagonal(dmK, offK, select='i',
                             select_range=(0, nev - 1))
    psi = Mi[:, None] * V
    return w2, psi, tg[:-1], q[:-1], Mw[:-1]


def locus_t_ray(mem, k, kappa):
    """all crossings of f = 2 kappa along t (from weld)."""
    tg, f, p, b, m = ray_arrays(mem, k)
    d = f - 2.0 * kappa
    idx = np.where(np.diff(np.sign(d)) != 0)[0]
    out = []
    for i in idx:
        a = d[i] / (d[i] - d[i + 1])
        out.append(float(tg[i] + a * (tg[i + 1] - tg[i])))
    return out


def agmon_report(mem, k, kappa, nev=6, label="", vwarm=None):
    """Lowest-nev eigenpairs + Agmon localization vs the locus."""
    tg, f, p, b, m = ray_arrays(mem, k)
    veq = my_equilibrium(mem, k, kappa, species=True, vinit=vwarm)
    bg = "DRESSED" if veq is not None else "FROZEN(v=0; eq missing)"
    w2, psi, tk, q, Mw = my_pencil(mem, k, kappa, species=True,
                                   vbar=veq, nev=nev)
    cross = locus_t_ray(mem, k, kappa)
    pk = p[:-1]; mk = m[:-1]; fk = f[:-1]
    flip = fk < 2.0 * kappa
    log(f"  [{label}] kappa={kappa}: bg={bg}; locus crossings t = "
        f"{['%.4f' % c for c in cross]}; flipped-cap node frac "
        f"{flip.mean():.3f}")
    if not cross:
        log("    (no locus on this ray at this kappa)")
        return veq, w2
    tloc = cross[0]
    rows = []
    for n in range(nev):
        ps = psi[:, n]
        ps = ps / np.max(np.abs(ps))
        w2n = w2[n]
        # m-weighted localization
        dens = Mw * ps ** 2
        dens = dens / dens.sum()
        cm = float(np.sum(tk * dens))
        mflip = float(dens[flip].sum())
        mnear = float(dens[np.abs(tk - tloc) < 0.2].sum())
        # Agmon weight from t_loc into the weld-side cap (t < tloc)
        gA = np.sqrt(np.maximum(q - w2n * mk, 0.0) / pk)
        h = tk[1] - tk[0]
        iloc = int(np.searchsorted(tk, tloc))
        rho = np.zeros_like(tk)
        # integrate from iloc down to 0
        for i in range(iloc - 1, -1, -1):
            rho[i] = rho[i + 1] + 0.5 * (gA[i] + gA[i + 1]) * h
        capm = tk < tloc
        rhoW = rho[0]                      # total Agmon distance to weld
        psiW = abs(ps[0])
        # envelope-violation factor: max over cap of |psi| e^{rho}
        # normalized by |psi| at the locus node
        psiL = max(abs(ps[iloc]), 1e-300)
        viol = float(np.max(np.abs(ps[capm]) * np.exp(rho[capm])) / psiL) \
            if capm.any() else np.nan
        rows.append((n, w2n, cm, mflip, mnear, rhoW, psiW, viol))
    log("    n    w2            CM(t)   m-frac(f<2k)  m-frac(|t-tl|<.2)"
        "  rhoA(weld)  |psi(weld)|  Agmon-viol")
    for r in rows:
        log("    %d  %+.6e  %.4f   %.3e     %.3e        %8.3f    "
            "%.3e    %.3e" % r)
    return veq, w2


# ===================================================================
# PART 1a: Agmon localization, kappa = 1.0 and 2.0, full domain, OFF
# ===================================================================
log("=" * 72)
log("P1: AGMON LOCALIZATION (M1 full domain, OFF, untruncated, "
    "dressed)")
log("=" * 72)
k_dom = int(np.argmax(mem4.b.sum(0)))
k_seal = int(np.argmin(mem4.f.min(0)))
log(f"dominant-b ray k={k_dom} (u={mem4.u[k_dom]:+.4f}); "
    f"seal-adjacent ray k={k_seal} (u={mem4.u[k_seal]:+.4f})")
log(f"f ranges: dom ({mem4.f[:, k_dom].min():.4f}, "
    f"{mem4.f[:, k_dom].max():.4f}); seal ({mem4.f[:, k_seal].min():.4f},"
    f" {mem4.f[:, k_seal].max():.4f})")

W2STORE = {}
for kray, lbl in ((k_dom, "dom"), (k_seal, "seal")):
    vwarm = None
    for kap in (2.0, 1.0):                # descending: warm starts
        veq, w2 = agmon_report(mem4, kray, kap, nev=6,
                               label=f"{lbl} Nt=4000", vwarm=vwarm)
        vwarm = veq
        W2STORE[(lbl, kap, 4000)] = w2
        # doubling check (Nt = 8000), eigenvalues only
        veq8 = my_equilibrium(mem8, kray, kap, species=True,
                              vinit=None if veq is None else
                              np.interp(mem8.tg, mem4.tg, veq))
        w28, _, _, _, _ = my_pencil(mem8, kray, kap, species=True,
                                    vbar=veq8, nev=6)
        W2STORE[(lbl, kap, 8000)] = w28
        scale = np.maximum(np.abs(w2), 1e-3)
        drift = np.max(np.abs(w28 - w2) / scale)
        log(f"    doubling Nt 4000->8000: max rel drift (6 modes) = "
            f"{drift:.2e}")
log(f"[{time.time()-t0:.0f}s]")

# ===================================================================
# PART 1b: eigenvalue-count anomaly scan (W5 vs species-OFF W4 pencil)
# ===================================================================
log("=" * 72)
log("P2: EIGENVALUE-COUNT SCAN kappa in (0.5,...,2.5): W5(untrunc) "
    "vs W4(trunc) — each about its OWN dressed equilibrium")
log("=" * 72)
KSCAN = (2.5, 2.0, 1.45, 1.0, 0.767, 0.5)   # descending (warm starts)
for kray, lbl in ((k_dom, "dom"), (k_seal, "seal")):
    vw5 = None; vw4 = None
    for kap in KSCAN:
        v5 = my_equilibrium(mem4, kray, kap, species=True, vinit=vw5)
        v4 = my_equilibrium(mem4, kray, kap, species=False, vinit=vw4)
        vw5, vw4 = v5, v4
        w25, _, _, _, _ = my_pencil(mem4, kray, kap, species=True,
                                    vbar=v5, nev=8)
        w24, _, _, _, _ = my_pencil(mem4, kray, kap, species=False,
                                    vbar=v4, nev=8)
        nn5 = int((w25 < 0).sum()); nn4 = int((w24 < 0).sum())
        # unmatched-level detector: greedy nearest pairing, gap units
        sp = np.median(np.diff(w24))
        unmatched = 0.0
        for x in w25[:6]:
            unmatched = max(unmatched,
                            float(np.min(np.abs(w24 - x)) / sp))
        b5 = "DR" if v5 is not None else "FR"
        b4 = "DR" if v4 is not None else "FR"
        log(f"  [{lbl}] kappa={kap:5.3f}  nneg W5={nn5} W4={nn4}  "
            f"bg(W5,W4)=({b5},{b4})  max unmatched (gap units) = "
            f"{unmatched:.3f}")
        log(f"      W5 w2[:6]: " + " ".join(f"{x:+.5e}" for x in w25[:6]))
        log(f"      W4 w2[:6]: " + " ".join(f"{x:+.5e}" for x in w24[:6]))
log(f"[{time.time()-t0:.0f}s]")

# ===================================================================
# PART 2: COUPLED (f,w) LONG-T PINNING — faithful reimplementation
# ===================================================================
log("=" * 72)
log("P3: COUPLED LONG-T (kappa=3, ON, amp .05, T_end = 12 xmax)")
log("=" * 72)


class GeoLite:
    """GeoW5-equivalent geometry, built from the claimant's stated
    formulas (read, then re-coded)."""

    def __init__(self, mem, t_b, Nt=2000, Nx=768):
        self.Nu = mem.Nu
        self.u, self.wu = mem.u, mem.wu
        self.tg = np.linspace(0.0, float(t_b), Nt)
        self.X = np.array([np.interp(self.tg, mem.tg, mem.X[:, i])
                           for i in range(4)]).T
        Y, Yu = vl.Yr(mem.u), vl.Yru(mem.u)
        self.f_t = self.X @ Y
        fu_t = self.X @ Yu
        self.fth2_t = (1 - mem.u[None, :] ** 2) * fu_t ** 2
        et = np.exp(-self.tg)[:, None]
        integ = et / self.f_t
        h = self.tg[1] - self.tg[0]
        cs = np.concatenate([np.zeros((1, self.Nu)),
                             np.cumsum(0.5 * (integ[1:] + integ[:-1]),
                                       0) * h])
        x_of_t = cs[-1][None, :] - cs
        self.xmax = x_of_t[0].copy()
        self.Nx = Nx
        self.xg = np.linspace(0, 1, Nx)[None, :] * self.xmax[:, None]
        self.dx = self.xg[:, 1] - self.xg[:, 0]
        self.t_of_x = np.empty((self.Nu, Nx))
        self.f = np.empty((self.Nu, Nx))
        self.fth2 = np.empty((self.Nu, Nx))
        for k in range(self.Nu):
            xs = x_of_t[::-1, k]
            ts = self.tg[::-1]
            self.t_of_x[k] = np.interp(self.xg[k], xs, ts)
            self.f[k] = np.interp(self.t_of_x[k], self.tg,
                                  self.f_t[:, k])
            self.fth2[k] = np.interp(self.t_of_x[k], self.tg,
                                     self.fth2_t[:, k])
        self.r = np.exp(-self.t_of_x)


g = GeoLite(mem8, T5, Nt=2000, Nx=768)
Nu = g.Nu
UN = mem8.u
Y4, Yu4 = vl.Yr(UN), vl.Yru(UN)
tg = g.tg
h = tg[1] - tg[0]
Xbg = g.X
f_b = g.f
fth2_b = g.fth2
xm = float(np.max(g.xmax))
log(f"GeoLite: xmax={xm:.4f} Nx={g.Nx} f_b range "
    f"({f_b.min():.4f}, {f_b.max():.4f})  [claimant: 0.5753, "
    f"(1.0000, 13.4811)]")

# 2000-pt quadrature + barycentric 24-ray -> quad-node interp
xq, wq = np.polynomial.legendre.leggauss(2000)
Y4q, Yu4q = vl.Yr(xq), vl.Yru(xq)
sq = 1 - xq ** 2
bw = np.array([1.0 / np.prod(UN[j] - np.delete(UN, j))
               for j in range(24)])
D = xq[:, None] - UN[None, :]
D[np.abs(D) < 1e-13] = 1.0
L = bw[None, :] / D
INTERP = L / L.sum(1)[:, None]


def w_on_t(v, vt):
    vx = np.gradient(v, axis=-1) / g.dx[:, None]
    vtr = vx * (-np.exp(-g.t_of_x) / f_b)
    V = np.empty((Nu, len(tg)))
    VT = np.empty_like(V)
    VR = np.empty_like(V)
    for k in range(Nu):
        tk = g.t_of_x[k][::-1]
        V[k] = np.interp(tg, tk, v[k][::-1])
        VT[k] = np.interp(tg, tk, vt[k][::-1])
        VR[k] = np.interp(tg, tk, vtr[k][::-1])
    return V, VT, VR


def slice_rhs_factory(V, VT, VR, kappa, species=True):
    Ntw = len(tg)

    def colp(t):
        i = min(max(int(t / h), 0), Ntw - 2)
        a = (t - tg[i]) / h
        return (V[:, i] * (1 - a) + V[:, i + 1] * a,
                VT[:, i] * (1 - a) + VT[:, i + 1] * a,
                VR[:, i] * (1 - a) + VR[:, i + 1] * a)

    def rhs(t, z):
        X, Xt = z[:4], z[4:]
        Vk, VTk, VRk = colp(t)
        fq = X @ Y4q
        fuq = X @ Yu4q
        e2v = np.exp(-2.0 * (INTERP @ Vk))
        wf = wq * e2v / 8.0
        PX = (sq * 2 * fuq / fq * wf) @ Yu4q.T \
            - (sq * fuq ** 2 / fq ** 2 * wf) @ Y4q.T
        acc = Xt + 2 * PX
        if kappa != 0.0:
            VTq = INTERP @ VTk
            VRq = INTERP @ VRk
            J = (wq * (np.exp(-2 * t) * VTq ** 2 / fq ** 2
                       + VRq ** 2)) @ Y4q.T
            acc = acc + (4 * kappa / CC) * J
            if species:
                wfa = wq * sq * e2v
                AX = -0.25 * ((wfa * 2 * fuq / fq ** 2) @ Yu4q.T
                              + (wfa * fuq ** 2 * (-2) / fq ** 3)
                              @ Y4q.T)
                acc = acc + 2 * kappa * AX
        return np.concatenate([Xt, acc])
    return rhs


def slice_solve(V, VT, VR, kappa, species=True, method="rk4grid"):
    rhs = slice_rhs_factory(V, VT, VR, kappa, species)
    z0 = np.array([1.0, 0, 0, 0, GAMMA, -CM, 0, 0])
    if method == "dop853":
        s = solve_ivp(rhs, (0.0, tg[-1]), z0, method='DOP853',
                      rtol=1e-9, atol=1e-12, dense_output=True)
        if not s.success:
            return None
        return s.sol(tg)[:4].T
    Z = np.empty((len(tg), 8))
    z = z0.copy()
    Z[0] = z
    for i in range(len(tg) - 1):
        t = tg[i]
        k1 = rhs(t, z)
        k2 = rhs(t + h / 2, z + h / 2 * k1)
        k3 = rhs(t + h / 2, z + h / 2 * k2)
        k4 = rhs(t + h, z + h * k3)
        z = z + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        if not np.all(np.isfinite(z)):
            return None
        Z[i + 1] = z
    return Z[:, :4]


def f_on_rays(Xs):
    fc = np.empty_like(f_b)
    fthc = np.empty_like(f_b)
    for k in range(Nu):
        Xi = np.array([np.interp(g.t_of_x[k], tg, Xs[:, i])
                       for i in range(4)]).T
        fc[k] = Xi @ Y4[:, k]
        fthc[k] = (1 - UN[k] ** 2) * (Xi @ Yu4[:, k]) ** 2
    return fc, fthc


def rhs_coupled(v, vt, fc, fcT, fthc, kappa, dcell, species=True):
    p = g.r ** 2 * fc / f_b
    pf = 0.5 * (p[:, 1:] + p[:, :-1])
    F = pf * (v[:, 1:] - v[:, :-1]) / g.dx[:, None]
    pref = fc / (g.r ** 2 * f_b)
    dvt = np.empty_like(v)
    dvt[:, 1:-1] = pref[:, 1:-1] * (F[:, 1:] - F[:, :-1]) / g.dx[:, None]
    dvt[:, 0] = 0.0
    dvt[:, -1] = pref[:, -1] * (0.0 - F[:, -1]) / g.dx * 2
    s = CC * fthc / (16 * g.r ** 2) / kappa
    fac = (1.0 - 2.0 * kappa / fc) if species else 1.0
    if dcell:
        dvt[:, 1:] += (s * (np.exp(v) - fac * np.exp(-2 * v)))[:, 1:]
    else:
        dvt[:, 1:] += (-s * fac * np.exp(-2 * v))[:, 1:]
    dvt += (fcT / np.maximum(fc, 1e-6)) * vt
    dv = vt.copy()
    dv[:, 0] = 0.0
    dvt[:, 0] = 0.0
    return dv, dvt


def bump_profile(amp, x0frac=0.55, sig_frac=0.25):
    uu = g.u
    gg = (1 - uu ** 2)
    gg = gg / np.max(np.abs(gg))
    x0 = x0frac * g.xmax[:, None]
    sig = sig_frac * g.xmax[:, None]
    w0 = amp * gg[:, None] * np.exp(-((g.xg - x0) / sig) ** 2)
    assert np.min(1 + w0) > 0.02
    return np.log1p(w0)


def locus_pos_stats(fc, kappa):
    """per-ray locus t-position on the CURRENT f (first crossing from
    the weld side, i.e. largest-x crossing on the x-grid)."""
    ts = []
    for k in range(Nu):
        d = fc[k] - 2.0 * kappa
        idx = np.where(np.diff(np.sign(d)) != 0)[0]
        if len(idx):
            i = idx[-1]            # largest x = closest to weld
            a = d[i] / (d[i] - d[i + 1])
            tt = g.t_of_x[k, i] + a * (g.t_of_x[k, i + 1]
                                       - g.t_of_x[k, i])
            ts.append(tt)
    return (len(ts), float(np.median(ts)) if ts else np.nan)


KAPPA, AMP, DCELL = 3.0, 0.05, True
TWO_K = 2.0 * KAPPA
band_b = np.abs(f_b - TWO_K) < 0.3 * TWO_K
log(f"background band pts = {int(band_b.sum())} (claimant: 646); "
    f"static band median |f_b/2k - 1| = "
    f"{np.median(np.abs(f_b[band_b] / TWO_K - 1)):.4f}")

# v=0 dressed-static-cell reference (the D_alg renormalization target)
Zr = np.zeros((Nu, len(tg)))
Xst = slice_solve(Zr, Zr, Zr, KAPPA)
fst, _ = f_on_rays(Xst)
log(f"v=0 D_alg-dressed static cell at kappa=3: max f_st/f_b = "
    f"{np.max(fst / f_b):.4f}; d_static(bg band) = "
    f"{np.median(np.abs(fst[band_b] / TWO_K - 1)):.4f}; "
    f"d_static(current band) = "
    f"{np.median(np.abs(fst[np.abs(fst - TWO_K) < 0.3 * TWO_K] / TWO_K - 1)):.4f}")

T_end = 12.0 * xm
n_f = 64
v = bump_profile(AMP)
vt = np.zeros_like(v)
dT = 0.4 * float(np.min(g.dx)) / 1.6
nst = int(np.ceil(T_end / dT))
log(f"T_end = 12 xmax = {T_end:.4f}, dT = {dT:.3e}, steps = {nst}")

fc, fthc = f_b.copy(), fth2_b.copy()
fcT = np.zeros_like(fc)
fprev = fc.copy()
REC = dict(T=[], pin_b=[], pin_c=[], q10_b=[], minall=[], rat=[],
           nb_c=[], nray=[], tloc=[], dst=[])
term = None
i = 0
for i in range(nst):
    if i % 2560 == 0:
        log(f"    progress {i}/{nst} ({time.time()-t0:.0f}s)")
    if i % n_f == 0:
        V, VT, VR = w_on_t(v, vt)
        Xs = slice_solve(V, VT, VR, KAPPA)
        if i == 0 and Xs is not None:
            Xref = slice_solve(V, VT, VR, KAPPA, method="dop853")
            dsl = (np.nan if Xref is None
                   else float(np.max(np.abs(Xs - Xref))))
            log(f"    slice gate rk4grid vs DOP853: max|dX| = "
                f"{dsl:.2e} [{'OK' if dsl <= 1e-5 else 'FLAGGED'}]")
        if Xs is None or not np.all(np.isfinite(Xs)):
            term = ("SLICE-FAIL", i * dT)
            break
        fc, fthc = f_on_rays(Xs)
        if fc.min() < 0.001:
            term = ("FCOLLAPSE", i * dT, float(fc.min()))
            break
        rat = float(np.max(fc / f_b))
        if rat > 4.0:
            term = ("CFL-EXCEEDED", i * dT, rat)
            break
        if i > 0:
            fcT = (fc - fprev) / (n_f * dT)
        fprev = fc.copy()
        dist = np.abs(fc / TWO_K - 1.0)
        band_c = np.abs(fc - TWO_K) < 0.3 * TWO_K
        nrayl, tlocm = locus_pos_stats(fc, KAPPA)
        REC["T"].append(i * dT)
        REC["pin_b"].append(float(np.median(dist[band_b])))
        REC["pin_c"].append(float(np.median(dist[band_c]))
                            if band_c.any() else np.nan)
        REC["q10_b"].append(float(np.quantile(dist[band_b], 0.10)))
        REC["minall"].append(float(dist.min()))
        REC["rat"].append(rat)
        REC["nb_c"].append(int(band_c.sum()))
        REC["nray"].append(nrayl)
        REC["tloc"].append(tlocm)
        REC["dst"].append(float(np.max(np.abs(fc - fst))))
    k1 = rhs_coupled(v, vt, fc, fcT, fthc, KAPPA, DCELL)
    k2 = rhs_coupled(v + .5 * dT * k1[0], vt + .5 * dT * k1[1],
                     fc, fcT, fthc, KAPPA, DCELL)
    k3 = rhs_coupled(v + .5 * dT * k2[0], vt + .5 * dT * k2[1],
                     fc, fcT, fthc, KAPPA, DCELL)
    k4 = rhs_coupled(v + dT * k3[0], vt + dT * k3[1], fc, fcT,
                     fthc, KAPPA, DCELL)
    v = v + dT / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
    vt = vt + dT / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
    if i % 50 == 0:
        if not np.all(np.isfinite(v)) or v.max() > 8 \
                or v.min() < np.log(0.05):
            term = ("W-COLLAPSE", (i + 1) * dT)
            break

nrec = len(REC["T"])
log(f"run done: term={term}, steps={i+1}/{nst}, f-updates={nrec} "
    f"[{time.time()-t0:.0f}s]")
if nrec:
    idxs = [0, nrec // 4, nrec // 2, (3 * nrec) // 4, nrec - 1]
    log("  j      T        d_bgband   d_curband  q10_bg    min_all   "
        "max f/fb  nb_c  nrayloc  med t_loc  max|fc-f_static|")
    for j in idxs:
        log("  %5d  %7.3f  %.5f    %.5f    %.5f   %.5f   %.4f    "
            "%4d  %4d     %.4f     %.4e"
            % (j, REC["T"][j], REC["pin_b"][j], REC["pin_c"][j],
               REC["q10_b"][j], REC["minall"][j], REC["rat"][j],
               REC["nb_c"][j], REC["nray"][j], REC["tloc"][j],
               REC["dst"][j]))
    # claimant-window cross-check: value at T = 6 xmax
    jh = int(np.searchsorted(REC["T"], 6.0 * xm)) - 1
    log(f"  cross-check at T ~ 6 xmax (claimant horizon): d_bgband = "
        f"{REC['pin_b'][jh]:.4f} (claimant end 0.1971), max f/fb = "
        f"{REC['rat'][jh]:.3f} (claimant 2.353)")
    # secular test: linear fit of rat and pin_b on last half
    Ta = np.array(REC["T"]); ra = np.array(REC["rat"])
    pa = np.array(REC["pin_b"])
    half = Ta > Ta[-1] / 2
    cr = np.polyfit(Ta[half], ra[half], 1)
    cp = np.polyfit(Ta[half], pa[half], 1)
    log(f"  last-half linear rates: d(max f/fb)/dT = {cr[0]:+.3e}, "
        f"d(d_bg)/dT = {cp[0]:+.3e}")
    np.savez("/tmp/w5_arm2_verifier4_pinning.npz",
             **{k_: np.array(v_) for k_, v_ in REC.items()})
log(f"ALL DONE [{time.time()-t0:.0f}s]")
