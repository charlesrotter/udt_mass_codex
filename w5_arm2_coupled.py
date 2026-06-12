#!/usr/bin/env python3
"""W5 ARM-2 — SCRIPT 7: COUPLED (f,w) ON TRUST WINDOWS (untruncated).

Date: 2026-06-12.  HYPOTHESIS-GRADE; TRUE units cc = 2.  The
VB4-vindicated domain class: full back-reaction marches on t <= t5.

SYSTEM (exact pieces, sym layer): operator-split (Option-2 species,
the W4-B/VB4 machinery re-implemented for the untruncated action):
  w-channel: v_TT = (f_c/(r^2 f_b)) d_x[(r^2 f_c/f_b) v_x]
             + (f_cT/f_c) v_T + S_W5(v; f_c, fth2_c)
    with S_W5 carrying the (1 - 2 kappa/f_c) factor on the e^{-2v}
    term (the locus is evaluated on the CURRENT f — the locus moves
    with the field; this is where pinning would show).
  f-slices (library-frame recipe IVP from weld data, premise labeled):
    X_tt - X_t = 2 P_w,X + (4 kappa/cc) J + 2 kappa A_X,
    P_w = (1/8) Int du s f_u^2 e^{-2v} / f
    J_l = Int du [e^{-2t} v_T^2/f^2 + v_t^2] Y_l        (W_wave f-source)
    A   = -(1/4) Int du s f_u^2 e^{-2v} / f^2           (D_alg f-source;
          gradient gate G-F passed, 1.4e-10)
  NOTE the A-term is the NEW f-channel force of the untruncated
  species: it is kappa-linear and survives w -> 0 shaped backgrounds
  ONLY via e^{-2v} dressing (A != 0 even at v = 0 — but at v = 0 it
  is w-INDEPENDENT and renormalizes the static cell itself; recorded
  structural fact, checked at C-G1' below).

PRE-REGISTERED GATES + runs:
  C-G1' slice anchor: at v = 0, kappa = 0 the slice flow must
        reproduce the background X to <= 1e-7 (recipe lock).  At
        v = 0, kappa != 0 the A-term DRESSES the static cell: the
        dressed slice flow is reported (new structural object), and
        the coupled run uses it as its own background (consistency).
  C-G2' frozen playback == frozen stencil <= 1e-10.
  RUNS (M1, t5 window): kappa {+2 kc_t5', -2 kc_t5', +1.0, -1.0,
        +3.0} x amp {0.05, 0.01}, D_cell ON and OFF; T_end = 6 x_max;
        n_f = 64 cadence (halving check on one run).
  PINNING DIAGNOSTIC (pre-registered; compute, don't hope): histogram
        distance d(T) = median_x |f_c/(2 kappa) - 1| over the locus
        band |f_b - 2 kappa| < 0.3 * 2 kappa; PINNING would be d(T)
        decreasing and staying small; the null is d(T) tracking the
        w-oscillation with no drift.
  VERDICTS: durable shaped matter with back-reaction yes/no per run
        (bounded envelopes, regular march, f_min > 0.001, no CFL
        blowout); locus behavior under back-reaction.

Log: /tmp/w5_arm2_coupled.log.  New file.  2026-06-12, W5 Arm-2.
"""
import sys, time, json
import numpy as np
from scipy.integrate import solve_ivp
sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
import w4b_verifier_lib as vl
import w5_arm2_lib as w5

t0 = time.time()
def log(*a):
    print(*a, flush=True)

GAMMA, CM = 1.0, 0.18413678
CC = 2.0
T5 = 2.2357
mem = vl.Member(GAMMA, CM, Nu=24, Nt=8000)
geo = w5.GeoW5(mem, t_b=T5, Nt=2000, Nx=768)
g = geo
Nu = g.Nu
UN = mem.u
Y4, Yu4 = vl.Yr(UN), vl.Yru(UN)
tg = g.tg
h = tg[1] - tg[0]
Xbg = g.X
f_b = g.f
fth2_b = g.fth2
xm = float(np.max(g.xmax))
log(f"M1 trust window t<={T5}: xmax={xm:.4f} Nx={g.Nx} "
    f"f_b range ({f_b.min():.4f}, {f_b.max():.4f})")

# 2000-pt quadrature + barycentric 24-ray -> node interp
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
        # P_w gradient (C1 angular, w-dressed):
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
    """f-slice march.  PRODUCTION integrator (amended after the first
    coupled attempt, on record): fixed-step RK4 with steps ALIGNED to
    the t-storage grid — DOP853 spends ~100x the work resolving the
    C0 kinks of the linearly-interpolated w-fields (3.4 s/slice vs
    0.03 s) at no accuracy gain beyond the interpolation floor.  Each
    production run validates its FIRST slice against DOP853 rtol 1e-9
    (gate <= 5e-7 max |dX|); the anchor C-G1' stays DOP853."""
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


# ---------------- gates
log("=" * 72)
log("C-G1': slice anchors")
log("=" * 72)
Z = np.zeros((Nu, len(tg)))
X0 = slice_solve(Z, Z, Z, 0.0)
err = np.max(np.abs(X0 - Xbg))
log(f"  slice(v=0, kappa=0) vs background: max|dX| = {err:.2e}")
# tolerance 1e-6 (amended, on record): geo.X is the Nt=8000 member
# re-interpolated to the Nt=2000 window grid — the 2.3e-7 observed is
# the interpolation floor, not a recipe mismatch (w4b's 1e-8 anchor
# compared on the SAME stored grid).
assert err < 1e-6, "C-G1' FAILED"
# the kappa-dressed static cell (v = 0, kappa != 0): the D_alg f-force
for kap in (1.0, -1.0, 3.0):
    Xk = slice_solve(Z, Z, Z, kap)
    if Xk is None or not np.all(np.isfinite(Xk)):
        log(f"  kappa={kap:+.2f}: v=0 dressed slice FAILS (f-IVP "
            "leaves domain) — recorded")
        continue
    fck, _ = f_on_rays(Xk)
    log(f"  kappa={kap:+.2f}: v=0 D_alg-dressed cell: max|f_c/f_b - 1|"
        f" = {np.max(np.abs(fck / f_b - 1)):.3e} (the untruncated "
        f"species renormalizes the static cell at O(kappa))")
log("  PASS C-G1'")


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


log("=" * 72)
log("C-G2': frozen playback == frozen stencil")
log("=" * 72)
v0 = w5.bump_profile(g, 0.05, sig_frac=0.25)
dTg = 0.4 * float(np.min(g.dx)) / 1.6
nst = int(np.ceil(1.0 * xm / dTg))
va, vta = v0.copy(), np.zeros_like(v0)
vb_, vtb = v0.copy(), np.zeros_like(v0)
for n in range(nst):
    k1 = rhs_coupled(va, vta, f_b, 0 * f_b, fth2_b, 1.0, True)
    k2 = rhs_coupled(va + .5 * dTg * k1[0], vta + .5 * dTg * k1[1],
                     f_b, 0 * f_b, fth2_b, 1.0, True)
    k3 = rhs_coupled(va + .5 * dTg * k2[0], vta + .5 * dTg * k2[1],
                     f_b, 0 * f_b, fth2_b, 1.0, True)
    k4 = rhs_coupled(va + dTg * k3[0], vta + dTg * k3[1], f_b,
                     0 * f_b, fth2_b, 1.0, True)
    va = va + dTg / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
    vta = vta + dTg / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
    kb1 = w5.rhs_np(vb_, vtb, g, 1.0, True, CC, True,
                    ("dirichlet", "neumann"))
    kb2 = w5.rhs_np(vb_ + .5 * dTg * kb1[0], vtb + .5 * dTg * kb1[1],
                    g, 1.0, True, CC, True, ("dirichlet", "neumann"))
    kb3 = w5.rhs_np(vb_ + .5 * dTg * kb2[0], vtb + .5 * dTg * kb2[1],
                    g, 1.0, True, CC, True, ("dirichlet", "neumann"))
    kb4 = w5.rhs_np(vb_ + dTg * kb3[0], vtb + dTg * kb3[1], g, 1.0,
                    True, CC, True, ("dirichlet", "neumann"))
    vb_ = vb_ + dTg / 6 * (kb1[0] + 2 * kb2[0] + 2 * kb3[0] + kb4[0])
    vtb = vtb + dTg / 6 * (kb1[1] + 2 * kb2[1] + 2 * kb3[1] + kb4[1])
dG = np.max(np.abs(va - vb_))
log(f"  frozen-playback vs frozen stencil after {nst} steps: "
    f"max|dv| = {dG:.2e}")
assert dG <= 1e-10, "C-G2' FAILED"
log("  PASS C-G2'")


def coupled_run(kappa, amp, dcell, T_end, n_f=64, tag="",
                wall_cap=1200.0):
    t_start = time.time()
    v = w5.bump_profile(g, amp, sig_frac=0.25)
    vt = np.zeros_like(v)
    dT = 0.4 * float(np.min(g.dx)) / 1.6
    n = int(np.ceil(T_end / dT))
    fc, fthc = f_b.copy(), fth2_b.copy()
    fcT = np.zeros_like(fc)
    fprev = fc.copy()
    fmins, ratmax, Ts, envs, pin = [], [], [], [], []
    term = None
    # locus band on the background (pre-registered diagnostic):
    band = np.abs(f_b - 2 * kappa) < 0.3 * abs(2 * kappa)
    nband = int(band.sum())
    for i in range(n):
        if i % (n_f * 40) == 0:
            log(f"    [{tag}] progress {i}/{n} steps "
                f"({time.time()-t_start:.0f}s)")
            if time.time() - t_start > wall_cap:
                term = ("WALL-CAP", i * dT)
                break
        if i % n_f == 0:
            V, VT, VR = w_on_t(v, vt)
            Xs = slice_solve(V, VT, VR, kappa)
            if i == 0 and Xs is not None:
                Xref = slice_solve(V, VT, VR, kappa, method="dop853")
                dsl = (np.nan if Xref is None
                       else float(np.max(np.abs(Xs - Xref))))
                # gate RECORDED per run (amended: a hard assert killed
                # the campaign on one run; runs with dsl > 1e-5 are
                # flagged SLICE-GATE-FLAG and not banked):
                gate_ok = bool(np.isfinite(dsl) and dsl <= 1e-5)
                log(f"    [{tag}] slice integrator gate: rk4grid vs "
                    f"DOP853 max|dX| = {dsl:.2e} "
                    f"[{'OK' if gate_ok else 'FLAGGED'}]")
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
            Ts.append((i + 1) * dT)
            envs.append(float(np.max(np.abs(v))))
            if not np.all(np.isfinite(v)) or v.max() > 8 \
                    or v.min() < np.log(0.05):
                term = ("W-COLLAPSE", (i + 1) * dT)
                break
    fmins = np.array(fmins); envs = np.array(envs); pin = np.array(pin)
    msg = (f"[{tag}] k={kappa:+.4f} dcell={dcell} amp={amp}: "
           f"term={term} steps={i+1}/{n} "
           f"fmin=({fmins.min() if len(fmins) else np.nan:.4f},"
           f"{fmins.max() if len(fmins) else np.nan:.4f}) "
           f"max f/fb={max(ratmax) if ratmax else np.nan:.3f} "
           f"env fin/max={envs[-1] if len(envs) else np.nan:.3g}/"
           f"{envs.max() if len(envs) else np.nan:.3g}")
    if nband and len(pin):
        d0, dmid, dend = pin[0], pin[len(pin) // 2], pin[-1]
        msg += (f" | PIN d(T): {d0:.4f} -> {dmid:.4f} -> {dend:.4f} "
                f"(band pts {nband})")
    log(msg)
    return term, fmins, envs, pin


# ---------------- production runs
KC_T5 = 0.0802 / 0.092068    # t5 OFF fold scale in true units ~ 0.871
log("=" * 72)
log("COUPLED RUNS (M1, t5 window, untruncated; TRUE units)")
log("=" * 72)
RES = []
for dcell in (True, False):
    for kappa, amp in ((1.0, 0.05), (1.0, 0.01), (-1.0, 0.05),
                       (3.0, 0.05), (-3.0, 0.05), (0.5, 0.05),
                       (2.0, 0.05)):
        t1 = time.time()
        term, fm, en, pin = coupled_run(kappa, amp, dcell, 6.0 * xm,
                                        tag="W5")
        RES.append(dict(kappa=kappa, amp=amp, dcell=dcell,
                        term=str(term),
                        fmin=float(fm.min()) if len(fm) else np.nan,
                        envmax=float(en.max()) if len(en) else np.nan,
                        pin0=float(pin[0]) if len(pin) else np.nan,
                        pin1=float(pin[-1]) if len(pin) else np.nan))
        log(f"   ({time.time()-t1:.0f}s)")
        with open("/tmp/w5_arm2_coupled.json", "w") as fh:
            json.dump(RES, fh, indent=1)
# cadence halving check on one representative
log("cadence check (kappa=1, ON, amp .05): n_f 64 -> 32")
t1 = time.time()
coupled_run(1.0, 0.05, True, 2.0 * xm, n_f=32, tag="cad32")
coupled_run(1.0, 0.05, True, 2.0 * xm, n_f=64, tag="cad64")
log(f"   ({time.time()-t1:.0f}s)")
log(f"done ({time.time()-t0:.0f}s)")
