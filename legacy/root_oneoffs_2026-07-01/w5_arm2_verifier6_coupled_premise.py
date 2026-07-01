#!/usr/bin/env python3
"""W5 ARM-2 BLIND VERIFIER — SCRIPT 6: the coupled-premise adjudication.

Date: 2026-06-12.  Verifier agent.

THE PREMISE UNDER ADJUDICATION (claim 6 carries it; claimant flagged
it): the coupled runs operationalize the species' w-content as the
BARE density D_alg = -(1/2) sin f_th^2/(f^2(1+w)^2).  My symbolic
verifier (VW5A2-III2..4) proved: the species' ACTUAL w-content (the
w-DEPENDENT part, Arm-1's Delta_w with E_f == 0 at w = 0) is the
SUBTRACTED density D_sub = D_alg(w) - D_alg(0), and the difference is
a w-INDEPENDENT f-force E_f[D_alg(0)] of O(kappa) — pure
operationalization, not species content.  Both choices give the SAME
w-equation; they differ ONLY in the f-channel.

TEST: rerun the claimant's coupled machinery (same GeoW5, same
stencils, same slice IVP, same cadence) with the A-term replaced by
its subtracted form
  A_sub = -(1/4) Int du s f_u^2 (e^{-2v} - 1)/f^2
(gradient changes accordingly).  At v = 0: A_sub == 0 and grad == 0,
so the static cell is NOT renormalized — the claimed O(kappa)
"cell renormalization" (max f/f_b = 1.44..2.35) and the kappa < 0
weld-IVP divergence are predicted to be artifacts of the bare-D_alg
choice if they vanish/soften here.

Runs (M1, t5 window, D_cell ON, amp 0.05, T_end = 6 x_max, n_f = 64,
identical to the claimant's):
  R1 kappa = +1 with A_sub  -> report max f/f_b (claimant bare: 1.679)
  R2 kappa = -1 with A_sub  -> does the FCOLLAPSE-at-step-1 disappear?
  R3 kappa = +3 with A_sub  -> max f/f_b (claimant bare: 2.353)
Log: /tmp/w5_arm2_verifier6_coupled.log.  New file.
"""
import sys, time
import numpy as np
from scipy.integrate import solve_ivp
sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
import w4b_verifier_lib as vl
import w5_arm2_lib as w5

t0 = time.time()
def log(*a):
    print(*a, flush=True)

GAMMA, CM, CC, T5 = 1.0, 0.18413678, 2.0, 2.2357
mem = vl.Member(GAMMA, CM, Nu=24, Nt=8000)
g = w5.GeoW5(mem, t_b=T5, Nt=2000, Nx=768)
Nu = g.Nu
UN = mem.u
Y4, Yu4 = vl.Yr(UN), vl.Yru(UN)
tg = g.tg
h = tg[1] - tg[0]
Xbg = g.X
f_b = g.f
fth2_b = g.fth2
xm = float(np.max(g.xmax))
log(f"M1 t5 window: xmax={xm:.4f} Nx={g.Nx} f_b range "
    f"({f_b.min():.4f}, {f_b.max():.4f})")

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


def slice_rhs_factory(V, VT, VR, kappa, subtracted):
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
            # D_alg f-force: bare e^{-2v} (claimant) vs SUBTRACTED
            # (e^{-2v} - 1) (the species' actual w-content):
            wgt = (e2v - 1.0) if subtracted else e2v
            wfa = wq * sq * wgt
            AX = -0.25 * ((wfa * 2 * fuq / fq ** 2) @ Yu4q.T
                          + (wfa * fuq ** 2 * (-2) / fq ** 3) @ Y4q.T)
            acc = acc + 2 * kappa * AX
        return np.concatenate([Xt, acc])
    return rhs


def slice_solve(V, VT, VR, kappa, subtracted, method="rk4grid"):
    rhs = slice_rhs_factory(V, VT, VR, kappa, subtracted)
    z0 = np.array([1.0, 0, 0, 0, GAMMA, -CM, 0, 0])
    if method == "dop853":
        s = solve_ivp(rhs, (0.0, tg[-1]), z0, method='DOP853',
                      rtol=1e-9, atol=1e-12, dense_output=True)
        return s.sol(tg)[:4].T if s.success else None
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


def rhs_coupled(v, vt, fc, fcT, fthc, kappa, dcell):
    p = g.r ** 2 * fc / f_b
    pf = 0.5 * (p[:, 1:] + p[:, :-1])
    F = pf * (v[:, 1:] - v[:, :-1]) / g.dx[:, None]
    pref = fc / (g.r ** 2 * f_b)
    dvt = np.empty_like(v)
    dvt[:, 1:-1] = pref[:, 1:-1] * (F[:, 1:] - F[:, :-1]) / g.dx[:, None]
    dvt[:, 0] = 0.0
    dvt[:, -1] = pref[:, -1] * (0.0 - F[:, -1]) / g.dx * 2
    s = CC * fthc / (16 * g.r ** 2) / kappa
    fac = 1.0 - 2.0 * kappa / fc
    if dcell:
        dvt[:, 1:] += (s * (np.exp(v) - fac * np.exp(-2 * v)))[:, 1:]
    else:
        dvt[:, 1:] += (-s * fac * np.exp(-2 * v))[:, 1:]
    dvt += (fcT / np.maximum(fc, 1e-6)) * vt
    dv = vt.copy()
    dv[:, 0] = 0.0
    dvt[:, 0] = 0.0
    return dv, dvt


log("=" * 72)
log("P0: v = 0 slice dressing, bare vs subtracted (the artifact test)")
log("=" * 72)
Z = np.zeros((Nu, len(tg)))
for kap in (1.0, -1.0, 3.0, -3.0):
    out = {}
    for lbl, subf in (("bare", False), ("sub", True)):
        Xk = slice_solve(Z, Z, Z, kap, subf, method="dop853")
        if Xk is None or not np.all(np.isfinite(Xk)):
            out[lbl] = "DIVERGES"
            continue
        fck, _ = f_on_rays(Xk)
        out[lbl] = f"max|f_c/f_b-1|={np.max(np.abs(fck/f_b-1)):.3e}"
    log(f"  kappa={kap:+.1f}: bare-D_alg: {out['bare']}   |   "
        f"subtracted: {out['sub']}")


def coupled_run(kappa, amp, dcell, T_end, subtracted, n_f=64, tag=""):
    ts = time.time()
    v = w5.bump_profile(g, amp, sig_frac=0.25)
    vt = np.zeros_like(v)
    dT = 0.4 * float(np.min(g.dx)) / 1.6
    n = int(np.ceil(T_end / dT))
    fc, fthc = f_b.copy(), fth2_b.copy()
    fcT = np.zeros_like(fc)
    fprev = fc.copy()
    ratmax, envs, pin = [], [], []
    band = np.abs(f_b - 2 * kappa) < 0.3 * abs(2 * kappa)
    nband = int(band.sum())
    term = None
    for i in range(n):
        if i % n_f == 0:
            V, VT, VR = w_on_t(v, vt)
            Xs = slice_solve(V, VT, VR, kappa, subtracted)
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
            ratmax.append(rat)
            if nband:
                pin.append(float(np.median(
                    np.abs(fc[band] / (2 * kappa) - 1.0))))
        k1 = rhs_coupled(v, vt, fc, fcT, fthc, kappa, dcell)
        k2 = rhs_coupled(v + .5 * dT * k1[0], vt + .5 * dT * k1[1],
                         fc, fcT, fthc, kappa, dcell)
        k3 = rhs_coupled(v + .5 * dT * k2[0], vt + .5 * dT * k2[1],
                         fc, fcT, fthc, kappa, dcell)
        k4 = rhs_coupled(v + dT * k3[0], vt + dT * k3[1], fc, fcT,
                         fthc, kappa, dcell)
        v = v + dT / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        vt = vt + dT / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        if i % 50 == 0:
            envs.append(float(np.max(np.abs(v))))
            if not np.all(np.isfinite(v)) or v.max() > 8 \
                    or v.min() < np.log(0.05):
                term = ("W-COLLAPSE", (i + 1) * dT)
                break
    msg = (f"[{tag}] k={kappa:+.2f} dcell={dcell} amp={amp} "
           f"({'SUBTRACTED' if subtracted else 'bare'}): term={term} "
           f"steps={i+1}/{n} max f/fb="
           f"{max(ratmax) if ratmax else np.nan:.4f} env fin/max="
           f"{envs[-1] if envs else np.nan:.4g}/"
           f"{max(envs) if envs else np.nan:.4g}")
    if nband and pin:
        msg += f" | PIN {pin[0]:.4f} -> {pin[len(pin)//2]:.4f} -> {pin[-1]:.4f}"
    log(msg + f"  ({time.time()-ts:.0f}s)")
    return term


log("=" * 72)
log("R1-R3: coupled runs with the SUBTRACTED species f-force")
log("=" * 72)
coupled_run(1.0, 0.05, True, 6.0 * xm, subtracted=True, tag="R1")
coupled_run(-1.0, 0.05, True, 6.0 * xm, subtracted=True, tag="R2")
coupled_run(3.0, 0.05, True, 6.0 * xm, subtracted=True, tag="R3")
log(f"done ({time.time()-t0:.0f}s)")
