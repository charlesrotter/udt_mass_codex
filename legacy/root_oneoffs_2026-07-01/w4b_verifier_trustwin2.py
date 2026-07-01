"""W4-B BLIND VERIFIER — attack E: the seal-margin mechanism's
falsifiable prediction.

Claim 4 (W4-B): the full-domain coupled (f,w) solve is NOT executable
BECAUSE the background seal margin is zero (f_min = 0.002): kappa > 0
wave stress deepens the seal -> f crosses 0; kappa < 0 unseals ->
speeds O(100). If that mechanism reading is right, the SAME coupled
machinery on the TRUST-WINDOW domain t <= t_5% (M1: t5 = 2.2357,
where f_min(t5) is finite) must march regularly. If it still
collapses there, the instability is intrinsic to the coupled system
(weld-IVP species), not a seal-margin artifact, and the mechanism
claim is wrong.

Own machinery throughout (verifier flow + own truncated geometry +
own slice ODE + own coupled stepper in the agent's stated
general-coefficient form). Slice ODE: X_tt - X_t = 2 P_w,X +
(4 kappa/c) J,  P_w = (1/8) Int s f_u^2 e^{-2v}/f du,
J_l = Int du [e^{-2t} v_T^2/f^2 + v_t^2] Y_l  (w4b_sym block D).
2000-pt Gauss quadrature; barycentric 24-ray -> node interp.

Runs (M1, D_cell ON, the amplitudes that FCOLLAPSED full-domain):
  kappa = 2 kc = +0.14124, amp 0.05;  kappa = -1, amp 0.05;
  plus amp 0.01 each; T_end = 6 x~max(trust); n_f = 64.
Pre-stated reading: REGULAR march for both signs => mechanism reading
UPGRADED (frozen-f premise is a domain artifact); collapse => claim 4
mechanism WRONG. Log: /tmp/w4b_verifier_trustwin.log.
New file. 2026-06-12, verifier.
"""
import sys
import time
import numpy as np
from scipy.integrate import solve_ivp
sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
import w4b_verifier_lib as vl


def log(*a):
    print(*a, flush=True)


T5_M1 = 2.2357
GAMMA, C = 1.0, 0.18413678
t0 = time.time()
mem = vl.Member(GAMMA, C, Nu=24, Nt=8000)
log(f"member regenerated ({time.time()-t0:.0f}s) t_stop={mem.t_stop:.4f}")

# ---- truncated geometry on t <= t5
sel = mem.tg <= T5_M1
tg = mem.tg[sel]
Nu = mem.Nu
UN, WU = mem.u, mem.wu
Y4, Yu4 = vl.Yr(UN), vl.Yru(UN)
Xbg = mem.X[sel]
f_t = mem.f[sel]                      # (Ntw, Nu)
fmin_t5 = float(np.min(f_t[-1]))
log(f"trust window t<={T5_M1}: f at window edge min over u = "
    f"{fmin_t5:.4f} (background seal margin now finite)")

Nx = 512
et = np.exp(-tg)[:, None]
integ = et / f_t
h = tg[1] - tg[0]
cs = np.concatenate([np.zeros((1, Nu)),
                     np.cumsum(0.5 * (integ[1:] + integ[:-1]), 0) * h])
x_of_t = cs[-1][None, :] - cs         # x=0 at t5 end, xmax at weld
xmax = x_of_t[0].copy()
xg = np.linspace(0, 1, Nx)[None, :] * xmax[:, None]
dx = xg[:, 1] - xg[:, 0]
t_of_x = np.empty((Nu, Nx))
f_b = np.empty((Nu, Nx))
fth2_b = np.empty((Nu, Nx))
for k in range(Nu):
    xs = x_of_t[::-1, k]
    ts = tg[::-1]
    t_of_x[k] = np.interp(xg[k], xs, ts)
    f_b[k] = np.interp(t_of_x[k], tg, f_t[:, k])
    fu_k = np.interp(t_of_x[k], tg, (mem.X[sel] @ Yu4[:, k]))
    fth2_b[k] = (1 - UN[k]**2) * fu_k**2
r = np.exp(-t_of_x)
r2 = r**2
k_probe = int(np.argmax(fth2_b.sum(1)))
i_probe = int(0.55 * Nx)
xm = float(np.max(xmax))
log(f"trust-window xmax={xm:.4f} (full-domain was ~0.60); Nx={Nx}")

# ---- 2000-pt quadrature + barycentric interp 24 rays -> nodes
xq, wq = np.polynomial.legendre.leggauss(2000)
Y4q, Yu4q = vl.Yr(xq), vl.Yru(xq)
sq = 1 - xq**2
bw = np.array([1.0 / np.prod(UN[j] - np.delete(UN, j))
               for j in range(24)])
D = xq[:, None] - UN[None, :]
small = np.abs(D) < 1e-13
D[small] = 1.0
L = bw[None, :] / D
L = L / L.sum(1)[:, None]
INTERP = L


def w_on_t(v, vt):
    vx = np.gradient(v, axis=-1) / dx[:, None]
    vtr = vx * (-np.exp(-t_of_x) / f_b)       # dv/dt along flow var
    V = np.empty((Nu, len(tg)))
    VT = np.empty_like(V)
    VR = np.empty_like(V)
    for k in range(Nu):
        tk = t_of_x[k][::-1]
        V[k] = np.interp(tg, tk, v[k][::-1])
        VT[k] = np.interp(tg, tk, vt[k][::-1])
        VR[k] = np.interp(tg, tk, vtr[k][::-1])
    return V, VT, VR


def slice_solve(V, VT, VR, kappa):
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
        e2v = np.exp(2.0 * (INTERP @ Vk))
        wf = wq / (e2v * 8.0)
        PX = (sq * 2 * fuq / fq * wf) @ Yu4q.T \
            - (sq * fuq**2 / fq**2 * wf) @ Y4q.T
        VTq = INTERP @ VTk
        VRq = INTERP @ VRk
        J = (wq * (np.exp(-2 * t) * VTq**2 / fq**2 + VRq**2)) @ Y4q.T
        return np.concatenate([Xt, Xt + 2 * PX + (4 * kappa / C) * J])

    z0 = np.array([1.0, 0, 0, 0, GAMMA, -C, 0, 0])
    s = solve_ivp(rhs, (0.0, tg[-1]), z0, method='DOP853', rtol=1e-8,
                  atol=1e-10, dense_output=True)
    if not s.success:
        return None
    return s.sol(tg)[:4].T


def f_on_rays(Xs):
    fc = np.empty_like(f_b)
    fthc = np.empty_like(f_b)
    for k in range(Nu):
        Xi = np.array([np.interp(t_of_x[k], tg, Xs[:, i])
                       for i in range(4)]).T
        fc[k] = Xi @ Y4[:, k]
        fthc[k] = (1 - UN[k]**2) * (Xi @ Yu4[:, k])**2
    return fc, fthc


# anchor: slice at w = 0 must reproduce the background
Z0 = slice_solve(np.zeros((Nu, len(tg))), np.zeros((Nu, len(tg))),
                 np.zeros((Nu, len(tg))), 0.0)
err = np.max(np.abs(Z0 - Xbg))
log(f"ANCHOR slice(w=0) vs background on trust window: max|dX| = "
    f"{err:.2e}")
assert err < 1e-7


def rhs_coupled(v, vt, fc, fcT, fthc, kappa, dcell=True):
    p = r2 * fc / f_b
    pf = 0.5 * (p[:, 1:] + p[:, :-1])
    F = pf * (v[:, 1:] - v[:, :-1]) / dx[:, None]
    pref = fc / (r2 * f_b)
    dvt = np.empty_like(v)
    dvt[:, 1:-1] = pref[:, 1:-1] * (F[:, 1:] - F[:, :-1]) / dx[:, None]
    dvt[:, 0] = 0.0
    dvt[:, -1] = pref[:, -1] * (0.0 - F[:, -1]) / dx * 2
    s = C * fthc / (16 * r2) / kappa
    dvt[:, 1:] += (s * (np.exp(v) - np.exp(-2 * v)))[:, 1:] if dcell \
        else (-s * np.exp(-2 * v))[:, 1:]
    dvt += (fcT / np.maximum(fc, 1e-6)) * vt
    dv = vt.copy()
    dv[:, 0] = 0.0
    dvt[:, 0] = 0.0
    return dv, dvt


def coupled_run(kappa, amp, T_end, n_f=96, tag=""):
    g_ = 1 - UN**2
    g_ = g_ / g_.max()
    w0 = amp * g_[:, None] * np.exp(-((xg - 0.55 * xmax[:, None])
                                      / (0.25 * xmax[:, None]))**2)
    v = np.log1p(w0)
    vt = np.zeros_like(v)
    dT = 0.4 * float(np.min(dx)) / 1.6
    n = int(np.ceil(T_end / dT))
    fc, fthc = f_b.copy(), fth2_b.copy()
    fcT = np.zeros_like(fc)
    fprev = fc.copy()
    fmins, ratmax, Ts, envs = [], [], [], []
    term = None
    for i in range(n):
        if i % n_f == 0:
            if (i // n_f) % 20 == 0:
                log(f"    [{tag} k={kappa:+.4f}] cadence {i//n_f} "
                    f"T={i* dT:.3f} fmin={fc.min():.4f} "
                    f"maxratio={float(np.max(fc/f_b)):.3f} "
                    f"env={float(np.max(np.abs(v))):.4g}")
            V, VT, VR = w_on_t(v, vt)
            Xs = slice_solve(V, VT, VR, kappa)
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
            fmins.append(float(fc.min()))
            ratmax.append(rat)
        k1 = rhs_coupled(v, vt, fc, fcT, fthc, kappa)
        k2 = rhs_coupled(v + 0.5 * dT * k1[0], vt + 0.5 * dT * k1[1],
                         fc, fcT, fthc, kappa)
        k3 = rhs_coupled(v + 0.5 * dT * k2[0], vt + 0.5 * dT * k2[1],
                         fc, fcT, fthc, kappa)
        k4 = rhs_coupled(v + dT * k3[0], vt + dT * k3[1], fc, fcT,
                         fthc, kappa)
        v = v + dT / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        vt = vt + dT / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        if i % 50 == 0:
            Ts.append((i + 1) * dT)
            envs.append(float(np.max(np.abs(v))))
            if not np.all(np.isfinite(v)) or v.max() > 8 \
                    or v.min() < np.log(0.05):
                term = ("W-COLLAPSE", (i + 1) * dT)
                break
    fmins = np.array(fmins)
    envs = np.array(envs)
    log(f"[{tag}] kappa={kappa:+.5f} amp={amp}: "
        f"term={term} steps={i+1}/{n} "
        f"fmin range=({fmins.min() if len(fmins) else np.nan:.4f},"
        f"{fmins.max() if len(fmins) else np.nan:.4f}) "
        f"max f/fb={max(ratmax) if ratmax else np.nan:.3f} "
        f"env final={envs[-1] if len(envs) else np.nan:.4g} "
        f"env max={envs.max() if len(envs) else np.nan:.4g}")
    return term, fmins, envs


KC = 0.070620
log("=" * 72)
log("TRUST-WINDOW COUPLED RUNS (M1, D_cell ON)")
log("=" * 72)
for kappa, amp in ((2 * KC, 0.05), (-1.0, 0.05), (2 * KC, 0.01),
                   (-1.0, 0.01)):
    t1 = time.time()
    coupled_run(kappa, amp, 3.0 * xm, tag=f"TW")
    log(f"   ({time.time()-t1:.0f}s)")
log("done.")
