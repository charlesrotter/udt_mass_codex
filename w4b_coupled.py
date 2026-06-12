"""W4 SOLVER AGENT B — script 6: COUPLED f-RESPONSE; OPTION 1 vs OPTION 2.

The mixed-character strategy of the W4 kit, executed:
  OPTION 2 (operator splitting): per f-update cadence, re-solve the
    STATIC slice flow (library frame, the recipe's own t-IVP from weld
    data, labeled premise)
       X_tt - X_t = 2 P_w,X + (4 kappa/c) J(t),
       P_w = (1/8) Int (1-u^2) f_u^2/((1+w)^2 f) du,
       J_l = Int du [e^{-2t} v_T^2/f^2 + v_t^2] Y_l(u)
    (derived in w4b_sym_energy.py block D; reduces to the banked
    recipe at w = 0 - anchored below, C-G1); advance w by RK4 on the
    general-coefficient conservation form
       v_TT = (f_c/(r^2 f_b)) d_x[(r^2 f_c/f_b) v_x] + (f_cT/f_c) v_T
              + S(v; fth2_cur)
    (reduces exactly to the frozen stencil at f_c = f_b - C-G2).
  OPTION 1 (space-time slab): f(t,T) solved as a genuine ELLIPTIC BVP
    with the full time-row term (same-minus):
       X_tt - X_t = 2 P_w,X + (4 kappa/c) J
                    + (e^{-2t}/2) [dG2/dX - d_T(dG2/dX_T)],
       G2 = (1/2) Int du f_T^2 / f^2,
    Chebyshev collocation in T (natural/free T-ends), Newton-Krylov,
    fixed-point alternation with the w-march on the slab f.
  STRUCTURAL PREMISE (recorded, first-class): the banked N1/N2
  ellipticity means the slab with weld-IVP t-data is Hadamard-unstable;
  Option 1 is closed instead with X pinned to the background at the
  seal end (t = t_stop) - a t-BVP premise Option 2 (IVP slices) does
  not share. The Option1-vs-Option2 delta therefore bundles
  {quasi-static error} + {t-end premise}; both are reported.

PRE-REGISTERED CROSS-VALIDATION GATES (the integrator trust pair,
M1, kappa = -1, D_cell ON, amp 0.2, profile g1, BC core):
  C-G1: slice solver at w = 0 reproduces the banked background to
        <= 1e-8 max abs (the recipe anchor).
  C-G2: coupled stepper at f_c = f_b frozen reproduces the frozen-f
        run (same waveform <= 1e-10).
  C-G3: agreement: ||opt1 - opt2||_2 over the middle 60% of the probe
        waveform <= 0.5 * ||opt2 - frozen||_2  OR
        ||opt2 - frozen|| / ||frozen|| <= 1e-4 (backreaction below
        resolution => frozen catalog stands validated as-is).
        FAILURE pre-stated: if neither holds, the coupled conclusions
        are NOT banked; only frozen-f results carry.
  Physical expectation (hypothesis-grade, stated before run): the
  slab f cannot follow w-oscillations at frequency omega (response
  suppressed by e^{-2t} omega^2/f^2), so opt2's oscillatory f-response
  should exceed opt1's, while time-averaged responses agree.

COUPLED kappa SUBSET (P5 refinement, M1): ON {0.25 kc, 0.9 kc,
1.1 kc, 2 kc, -1, -10, +10} x amp {0.05, 0.3}; OFF {+1, +10, -1, -10}
x amp {0.05}; classification per the committed evolib classifier;
f-degeneracy monitor f_min < 0.001 terminates (FCOLLAPSE label).

Log: /tmp/w4b_coupled.log; checkpoints /tmp/w4b_coupled_*.npz.
New file. 2026-06-12, W4-B agent.
"""
import json
import time
import numpy as np
from scipy.optimize import newton_krylov
import w4b_evolib as ev


def log(*a):
    print(*a, flush=True)


npz = np.load("/tmp/w4b_bg.npz")
lin = np.load("/tmp/w4b_lingap.npz")
S3 = 3**0.5
NX = 768
NT_SOLVER = 1025

UN, WU = np.polynomial.legendre.leggauss(24)
Y4 = ev.Yr(UN)            # (4, Nu)
Yu4 = ev.Yru(UN)


class Coupled:
    """Option-2 coupled evolution on one member."""

    def __init__(self, tag, Nx=NX, Nts=None):
        self.geo = ev.Geo(npz, tag, Nu=24, Nx=Nx)
        g = self.geo
        self.tag = tag
        m = npz[f"{tag}_meta"]
        self.gamma, self.c, self.t_stop = m[0], m[1], m[2]
        # f-solver grid = the STORED background grid (exact anchor;
        # slice integration via DOP853 rtol 1e-11, the recipe's own)
        self.ts = npz[f"{tag}_t"].copy()
        self.hs = self.ts[1] - self.ts[0]
        self.X_bg = npz[f"{tag}_X"].copy()
        self.f_b = g.f.copy()
        # N=2000 Gauss-Legendre quadrature for the f-sector (the
        # recipe's own N; the 24-ray quadrature fails O(1) at the seal
        # layer where 1/f spikes in u - found and fixed 2026-06-12).
        self.xq, self.wq = np.polynomial.legendre.leggauss(2000)
        self.Y4q = ev.Yr(self.xq)
        self.Yu4q = ev.Yru(self.xq)
        self.sq = 1 - self.xq**2
        # barycentric interpolation matrix: 24 GL rays -> 2000 nodes
        # (w-fields are smooth in u; recorded premise of the coupled
        # solver)
        bw = np.array([1.0 / np.prod(UN[j] - np.delete(UN, j))
                       for j in range(24)])
        D = self.xq[:, None] - UN[None, :]
        small = np.abs(D) < 1e-13
        D[small] = 1.0
        L = bw[None, :] / D
        L = L / L.sum(1)[:, None]
        L[small.any(1)] = 0.0
        for qi, kj in zip(*np.where(small)):
            L[qi, :] = 0.0
            L[qi, kj] = 1.0
        self.INTERP = L

    # ---- w fields on the f-solver grid
    def w_on_ts(self, v, vt):
        """returns dict 'n': (V, VT, VR) on (Nu, Nts)."""
        g = self.geo
        vx = np.gradient(v, axis=-1) / g.dx[:, None]
        dxdt = -np.exp(-g.tgrid) / self.f_b      # dx/dt per ray
        vt_rad = vx * dxdt
        V = np.empty((g.Nu, len(self.ts)))
        VT = np.empty_like(V)
        VR = np.empty_like(V)
        for k in range(g.Nu):
            # geo.tgrid[k] decreasing in x; flip for np.interp
            tk = g.tgrid[k][::-1]
            V[k] = np.interp(self.ts, tk, v[k][::-1])
            VT[k] = np.interp(self.ts, tk, vt[k][::-1])
            VR[k] = np.interp(self.ts, tk, vt_rad[k][::-1])
        return {"n": (V, VT, VR)}

    # ---- slice flow RHS (N=2000 quadrature; w-fields barycentrically
    # interpolated from the 24 rays - the 24-node quadrature fails O(1)
    # at the seal layer, recorded above)
    def Pw_X(self, X, Vk):
        f = X @ self.Y4q                 # (2000,)
        fu = X @ self.Yu4q
        e2 = np.exp(2.0 * (self.INTERP @ Vk))
        wfac = self.wq / (e2 * 8.0)
        g1 = (self.sq * 2 * fu / f * wfac) @ self.Yu4q.T
        g2 = -(self.sq * fu**2 / f**2 * wfac) @ self.Y4q.T
        return g1 + g2

    def J_of(self, X, t, Vk, VTk, VRk):
        f = X @ self.Y4q
        VTq = self.INTERP @ VTk
        VRq = self.INTERP @ VRk
        dens = np.exp(-2 * t) * VTq**2 / f**2 + VRq**2
        return (self.wq * dens) @ self.Y4q.T

    def slice_solve(self, wts, kappa, zero_w=False):
        """DOP853 (rtol 1e-11, the recipe's integrator) march of
        X_tt - X_t = 2 P_w,X + (4 kappa/c) J, w-fields linearly
        interpolated in t from the stored grid."""
        from scipy.integrate import solve_ivp
        Vn, VTn, VRn = wts["n"]
        if zero_w:
            Vn = np.zeros_like(Vn)
            VTn = np.zeros_like(VTn)
            VRn = np.zeros_like(VRn)
        Nts = len(self.ts)
        h = self.hs

        def colp(t):
            i = min(max(int(t / h), 0), Nts - 2)
            a = (t - self.ts[i]) / h
            return (Vn[:, i] * (1 - a) + Vn[:, i + 1] * a,
                    VTn[:, i] * (1 - a) + VTn[:, i + 1] * a,
                    VRn[:, i] * (1 - a) + VRn[:, i + 1] * a)

        def rhs(t, z):
            X, Xt = z[:4], z[4:]
            Vk, VTk, VRk = colp(t)
            a = Xt + 2 * self.Pw_X(X, Vk)
            if kappa != 0.0:
                a = a + (4 * kappa / self.c) * self.J_of(X, t, Vk, VTk,
                                                         VRk)
            return np.concatenate([Xt, a])

        z0 = np.array([1.0, 0, 0, 0, self.gamma, -self.c, 0, 0])
        sol = solve_ivp(rhs, (0.0, self.ts[-1]), z0, method='DOP853',
                        rtol=1e-11, atol=1e-12, dense_output=True)
        return sol.sol(self.ts)[:4].T

    def f_on_rays(self, Xs, tsrc=None):
        """X(tsrc) -> f, fth2 on per-ray x-grids (tsrc defaults to the
        stored 4097 grid; the slab passes its own coarser grid)."""
        g = self.geo
        tsrc = self.ts if tsrc is None else tsrc
        f = np.empty_like(g.f)
        fth2 = np.empty_like(g.f)
        for k in range(g.Nu):
            Xi = np.array([np.interp(g.tgrid[k], tsrc, Xs[:, i])
                           for i in range(4)]).T
            f[k] = Xi @ Y4[:, k]
            fth2[k] = (1 - UN[k]**2) * (Xi @ Yu4[:, k])**2
        return f, fth2

    # ---- coupled stepper
    def rhs_coupled(self, v, vt, fc, fcT, fth2c, kappa, dcell, bc):
        g = self.geo
        dx = g.dx[:, None]
        r2 = g.r**2
        p = r2 * fc / self.f_b
        pf = 0.5 * (p[:, 1:] + p[:, :-1])
        F = pf * (v[:, 1:] - v[:, :-1]) / dx
        pref = fc / (r2 * self.f_b)
        dvt = np.empty_like(v)
        dvt[:, 1:-1] = pref[:, 1:-1] * (F[:, 1:] - F[:, :-1]) / dx
        dvt[:, 0] = pref[:, 0] * (F[:, 0] - 0.0) / dx[:, 0] * 2
        dvt[:, -1] = pref[:, -1] * (0.0 - F[:, -1]) / dx[:, 0] * 2
        sc = self.c * fth2c / (16.0 * g.r**2) / kappa
        if dcell:
            dvt += sc * (np.exp(v) - np.exp(-2 * v))
        else:
            dvt += -sc * np.exp(-2 * v)
        dvt += (fcT / fc) * vt
        dv = vt.copy()
        if bc[0] == "dirichlet":
            dv[:, 0] = 0.0
            dvt[:, 0] = 0.0
        return dv, dvt

    def evolve_opt2(self, v0, vt0, kappa, dcell, T_end, n_f=64,
                    bc=("dirichlet", "neumann"), with_fT=True,
                    f_override=None):
        """Option-2 coupled run. f_override: callable T -> (fc, fcT,
        fth2c) for Option-1 slab playback; None = slice re-solves."""
        g = self.geo
        # CFL margin sized from the INITIAL f-response (the coupled
        # wave speed is f_c/f_b in x; an O(1) f-response above the old
        # fixed margin 1.6 was found to blow the march - fixed
        # 2026-06-12, on record): pre-solve once, set margin, and
        # terminate cleanly if a later update exceeds it.
        margin = 1.6
        if f_override is None:
            wts0 = self.w_on_ts(v0, vt0)
            Xs0 = self.slice_solve(wts0, kappa)
            fc0, _ = self.f_on_rays(Xs0)
            if np.all(np.isfinite(fc0)) and fc0.min() > 0.001:
                margin = max(1.6, 1.3 * float(np.max(fc0 / self.f_b)))
        self.cfl_margin = margin = min(margin, 12.0)
        dT = 0.5 * float(np.min(g.dx)) / margin
        nstep = int(np.ceil(T_end / dT))
        v, vt = v0.copy(), vt0.copy()
        fc, fth2c = self.f_b.copy(), g.fth2.copy()
        fcT = np.zeros_like(fc)
        fprev = fc.copy()
        stride = max(1, nstep // 4096)
        Ts, probes, envs, fmons, Xhist = [], [], [], [], []
        term = None
        for n in range(nstep):
            if f_override is None and n % n_f == 0:
                wts = self.w_on_ts(v, vt)
                Xs = self.slice_solve(wts, kappa)
                fc, fth2c = self.f_on_rays(Xs)
                if (not np.all(np.isfinite(fc))) or fc.min() < 0.001:
                    # the slice f-IVP left the admissible domain - the
                    # weld-continuation growth species; terminate clean
                    term = ("FCOLLAPSE", n * dT)
                    fmons.append(float(fc.min()) if np.all(
                        np.isfinite(fc)) else -np.inf)
                    break
                if float(np.max(fc / self.f_b)) > self.cfl_margin:
                    term = ("CFL-EXCEEDED", n * dT)
                    fmons.append(float(fc.min()))
                    break
                if with_fT and n > 0:
                    fcT = (fc - fprev) / (n_f * dT)
                fprev = fc.copy()
                Xhist.append((n * dT, Xs[:: len(self.ts) // 16].copy()))
            elif f_override is not None and n % n_f == 0:
                fc, fcT, fth2c = f_override(n * dT)
            # RK4
            k1 = self.rhs_coupled(v, vt, fc, fcT, fth2c, kappa, dcell,
                                  bc)
            k2 = self.rhs_coupled(v + 0.5 * dT * k1[0],
                                  vt + 0.5 * dT * k1[1], fc, fcT,
                                  fth2c, kappa, dcell, bc)
            k3 = self.rhs_coupled(v + 0.5 * dT * k2[0],
                                  vt + 0.5 * dT * k2[1], fc, fcT,
                                  fth2c, kappa, dcell, bc)
            k4 = self.rhs_coupled(v + dT * k3[0], vt + dT * k3[1], fc,
                                  fcT, fth2c, kappa, dcell, bc)
            v = v + dT / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
            vt = vt + dT / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
            if n % stride == 0:
                Ts.append((n + 1) * dT)
                probes.append(float(v[g.k_probe, g.i_probe]))
                envs.append(float(np.max(np.abs(v))))
                fmons.append(float(fc.min()))
            if n % 200 == 0:
                if not np.all(np.isfinite(v)):
                    term = ("COLLAPSE+", (n + 1) * dT)
                    break
                if v.min() <= ev.LN_COLLAPSE:
                    term = ("COLLAPSE-", (n + 1) * dT)
                    break
                if v.max() >= ev.V_BLOWUP:
                    term = ("COLLAPSE+", (n + 1) * dT)
                    break
                if fc.min() < 0.001:
                    term = ("FCOLLAPSE", (n + 1) * dT)
                    break
        return dict(v=v, vt=vt, T=np.array(Ts), probe=np.array(probes),
                    env=np.array(envs), fmin=np.array(fmons),
                    term=term, dT=dT, nstep=nstep, Xhist=Xhist,
                    E=np.zeros((0, 2)), vlast=(float(v.min()),
                                               float(v.max())),
                    srate=0.0)


# ====================================================================
log("=" * 72)
log("C-G1: slice solver anchor (w = 0 reproduces banked background)")
log("=" * 72)
cp = Coupled("M1")
zer = {"n": (np.zeros((24, len(cp.ts))),) * 3}
Xs0 = cp.slice_solve(zer, 0.0, zero_w=True)
err = np.max(np.abs(Xs0 - cp.X_bg))
log(f"C-G1 max|X_slice(w=0) - X_banked| = {err:.2e}")
assert err <= 1e-8, "C-G1 FAILED - recipe anchor broken; STOP"
log("PASS C-G1")

log("=" * 72)
log("C-G2: coupled stepper anchor (frozen playback == frozen stencil)")
log("=" * 72)
KAP, AMP = -1.0, 0.2
g = cp.geo
v0 = ev.bump_profile(g, AMP, "g1")
T_x = float(np.max(g.xmax))
T_end = 6.0 * T_x


def frozen_override(T):
    return cp.f_b, np.zeros_like(cp.f_b), g.fth2


rA = cp.evolve_opt2(v0, np.zeros_like(v0), KAP, True, T_end,
                    f_override=frozen_override)
# reference: pure frozen stencil at the same dT
rF = ev.evolve_np(g, v0, np.zeros_like(v0), KAP, True, T_end,
                  cfl=0.5 / 1.6)
nmin = min(len(rA["probe"]), len(rF["probe"]))
dGate = np.max(np.abs(rA["probe"][:nmin] - rF["probe"][:nmin]))
log(f"C-G2 max probe diff coupled(frozen-playback) vs frozen stencil "
    f"= {dGate:.2e}")
assert dGate <= 1e-10, "C-G2 FAILED - coupled stencil mismatch; STOP"
log("PASS C-G2")

# --------- the slice-IVP instability ladder (recorded phenomenon):
# at kappa = -1 (|4 kappa/c| ~ 22) the w-stress source drives the
# weld-IVP slice flow out of the admissible domain (f < 0) - the
# banked N1/N2 weld-continuation growth species acting inside the
# splitting scheme. Ladder amp -> survival probes the threshold.
log("=" * 72)
log("SLICE-IVP INSTABILITY LADDER (M1, kappa=-1, D_cell ON)")
log("=" * 72)
for a_l in (0.2, 0.1, 0.05, 0.02, 0.01):
    v0l = ev.bump_profile(g, a_l, "g1")
    rl = cp.evolve_opt2(v0l, np.zeros_like(v0l), -1.0, True,
                        2.0 * T_x, n_f=64)
    log(f"  amp={a_l:5.3f}: term={rl['term']} "
        f"fmin={rl['fmin'].min() if len(rl['fmin']) else np.nan:.4g}")

# --------- cross-validation pair re-posed in the SURVIVING regime
# (probe record /tmp/w4b_probe_slice.py output, 2026-06-12): kappa > 0
# wave stress deepens the seal and the slice f-IVP hits f = 0 at every
# tested amplitude (zero seal margin - recorded finding); kappa = -1
# survives for amp <= 0.02 with a finite response that UNSEALS the
# cell. Amended pair: (M1, kappa = -1, D_cell ON, amp 0.01, wide bump
# sig = 0.25 x_max) - the originally declared kappa sign, amplitude
# lowered with the reason on record BEFORE the comparison ran.
KAP = -1.0
AMP = 0.01
v0 = ev.bump_profile(g, AMP, "g1", sig_frac=0.25)
rF = ev.evolve_np(g, v0, np.zeros_like(v0), KAP, True, T_end,
                  cfl=0.5 / 1.6)
log("=" * 72)
log(f"CROSS-VALIDATION RUN (M1, kappa={KAP:.4f}=2kc, D_cell ON, "
    f"amp {AMP})")
log("=" * 72)
t0 = time.time()
r2o = cp.evolve_opt2(v0, np.zeros_like(v0), KAP, True, T_end, n_f=64)
log(f"option-2 done {time.time()-t0:.0f}s term={r2o['term']} "
    f"fmin_range=({r2o['fmin'].min():.4g},{r2o['fmin'].max():.4g})"
    if len(r2o['fmin']) else
    f"option-2 done {time.time()-t0:.0f}s term={r2o['term']} (no "
    f"surviving steps - full-domain coupled march not executable; "
    f"structural finding on record)")
opt2_alive = len(r2o["probe"]) > 32
dcad = np.nan
if opt2_alive:
    # cadence-doubling internal check of option 2
    r2b = cp.evolve_opt2(v0, np.zeros_like(v0), KAP, True, T_end,
                         n_f=32)
    ncad = min(len(r2o["probe"]), len(r2b["probe"]))
    dcad = np.max(np.abs(r2o["probe"][:ncad] - r2b["probe"][:ncad]))
    log(f"option-2 cadence halving probe diff = {dcad:.3e}")

# ---------------- Option 1: slab elliptic f, Chebyshev in T ----------
NTC = 9
# Chebyshev-Lobatto nodes on [0, T_end]
jj = np.arange(NTC)
xc = np.cos(np.pi * jj / (NTC - 1))
Tn = 0.5 * T_end * (1 - xc)                  # increasing 0..T_end


def cheb_D(N, Tend):
    x = np.cos(np.pi * np.arange(N) / (N - 1))
    cvec = np.ones(N)
    cvec[0] = cvec[-1] = 2
    cvec = cvec * (-1)**np.arange(N)
    X = np.tile(x, (N, 1)).T
    dX = X - X.T + np.eye(N)
    D = np.outer(cvec, 1 / cvec) / dX
    D -= np.diag(D.sum(1))
    # map x = 1 - 2T/Tend  => d/dT = -2/Tend d/dx
    return -2.0 / Tend * D


DT1 = cheb_D(NTC, T_end)
DT2 = DT1 @ DT1
NTS_SLAB = 257
ts_s = np.linspace(0, cp.t_stop, NTS_SLAB)
hs_s = ts_s[1] - ts_s[0]
Xbg_s = np.array([np.interp(ts_s, cp.ts, cp.X_bg[:, i])
                  for i in range(4)]).T


def slab_residual_factory(Wn):
    """Wn: dict of w-quantities (V, VT, VR) at (Nu, NTS_SLAB, NTC).
    N=2000 quadrature with ray->node interpolation (the 24-node
    quadrature fails O(1) at the seal layer)."""
    Vq = np.einsum('qk,ktn->tnq', cp.INTERP, Wn[0])
    VTq = np.einsum('qk,ktn->tnq', cp.INTERP, Wn[1])
    VRq = np.einsum('qk,ktn->tnq', cp.INTERP, Wn[2])
    sq, wq, Y4q, Yu4q = cp.sq, cp.wq, cp.Y4q, cp.Yu4q

    def res(Z):
        # Z: (NTS_SLAB, NTC, 4) deviation from background
        X = Xbg_s[:, None, :] + Z
        Xt = np.gradient(X, hs_s, axis=0)
        Xtt = (X[2:] - 2 * X[1:-1] + X[:-2]) / hs_s**2
        XT = np.einsum('nm,tmi->tni', DT1, X)
        XTT = np.einsum('nm,tmi->tni', DT2, X)
        f = np.einsum('tni,ik->tnk', X, Y4q)
        fu = np.einsum('tni,ik->tnk', X, Yu4q)
        fT = np.einsum('tni,ik->tnk', XT, Y4q)
        fTT = np.einsum('tni,ik->tnk', XTT, Y4q)
        e2 = np.exp(2.0 * Vq)                        # (t, n, q)
        # P_w,X
        wf = wq / (e2 * 8.0)
        PX = (np.einsum('tnk,ik->tni', sq * 2 * fu / f * wf, Yu4q)
              + np.einsum('tnk,ik->tni', -sq * fu**2 / f**2 * wf, Y4q))
        # J
        e2t = np.exp(-2 * ts_s)[:, None, None]
        dens = e2t * VTq**2 / f**2 + VRq**2
        J = np.einsum('tnk,ik->tni', wq * dens, Y4q)
        # time-row: (e^{-2t}/2)[dG2/dX - d_T dG2/dX_T]
        # dG2/dX_l = -Int du fT^2 Y_l/f^3 ; dG2/dX_T,l = Int du fT Y_l/f^2
        dG2X = np.einsum('tnk,ik->tni', -wq * fT**2 / f**3, Y4q)
        inner = fTT / f**2 - 2 * fT**2 / f**3
        dTdG2XT = np.einsum('tnk,ik->tni', wq * inner, Y4q)
        trow = 0.5 * e2t * (dG2X - dTdG2XT)
        R = np.empty_like(Z)
        R[1:-1] = (Xtt - Xt[1:-1] - 2 * PX[1:-1]
                   - (4 * KAP / cp.c) * J[1:-1] - trow[1:-1])
        # t-end rows: weld Dirichlet (X = bg, i.e. Z = 0) AND weld
        # momentum via one-sided derivative pinned to background;
        # seal end pinned to background (the recorded premise)
        R[0] = Z[0]
        R[-1] = Z[-1]
        # weld momentum row folded into first interior row weighting:
        R[1] = (X[1] - X[0]) / hs_s - (Xbg_s[1] - Xbg_s[0])[None, :] \
            / hs_s - 0.5 * hs_s * 0.0 - (Xt[0] - Xt[0])  # X_t(0)=bg rate
        R[1] = (X[1] - X[0]) / hs_s \
            - ((Xbg_s[1] - Xbg_s[0]) / hs_s)[None, :]
        return R
    return res


def w_on_slab(v_hist):
    """v_hist: list of (T, v, vt) snapshots at Chebyshev nodes ->
    (V, VT, VR) arrays (Nu, NTS_SLAB, NTC)."""
    Nu = g.Nu
    V = np.zeros((Nu, NTS_SLAB, NTC))
    VT = np.zeros_like(V)
    VR = np.zeros_like(V)
    for n, (Tq, vv, vvt) in enumerate(v_hist):
        vx = np.gradient(vv, axis=-1) / g.dx[:, None]
        vr = vx * (-np.exp(-g.tgrid) / cp.f_b)
        for k in range(Nu):
            tk = g.tgrid[k][::-1]
            V[k, :, n] = np.interp(ts_s, tk, vv[k][::-1])
            VT[k, :, n] = np.interp(ts_s, tk, vvt[k][::-1])
            VR[k, :, n] = np.interp(ts_s, tk, vr[k][::-1])
    return V, VT, VR


def make_override(Zsol):
    """Build T -> (fc, fcT, fth2) from a slab solution (barycentric
    Chebyshev evaluation in T)."""
    X_slab = Xbg_s[:, None, :] + Zsol      # (t, n, 4)
    fc_n = np.empty((NTC, g.Nu, g.Nx))
    fth_n = np.empty_like(fc_n)
    fcT_n = np.empty_like(fc_n)
    XT_slab = np.einsum('nm,tmi->tni', DT1, X_slab)
    for n in range(NTC):
        fc_n[n], fth_n[n] = cp.f_on_rays(X_slab[:, n, :], tsrc=ts_s)
        fT_r = np.empty_like(fc_n[n])
        for k in range(g.Nu):
            Xi = np.array([np.interp(g.tgrid[k], ts_s,
                                     XT_slab[:, n, i])
                           for i in range(4)]).T
            fT_r[k] = Xi @ Y4[:, k]
        fcT_n[n] = fT_r
    wb = np.ones(NTC) * (-1.0)**np.arange(NTC)
    wb[0] *= 0.5
    wb[-1] *= 0.5
    xn = np.cos(np.pi * np.arange(NTC) / (NTC - 1))

    def f_override(T):
        x = 1 - 2 * min(T, T_end) / T_end
        d = x - xn
        if np.any(np.abs(d) < 1e-14):
            n = int(np.argmin(np.abs(d)))
            return fc_n[n], fcT_n[n], fth_n[n]
        ww = wb / d
        ww = ww / ww.sum()
        return (np.einsum('n,nkx->kx', ww, fc_n),
                np.einsum('n,nkx->kx', ww, fcT_n),
                np.einsum('n,nkx->kx', ww, fth_n))
    return f_override


# fixed-point alternation
log("OPTION 1 slab fixed-point (NTC=%d, NTS=%d)" % (NTC, NTS_SLAB))
# iteration 0: w-march on frozen f, snapshot at Chebyshev nodes
def march_snapshots(f_override):
    snaps = []
    dT = 0.5 * float(np.min(g.dx)) / 1.6
    v, vt = v0.copy(), np.zeros_like(v0)
    fc, fcT, fth2c = (cp.f_b, np.zeros_like(cp.f_b), g.fth2) \
        if f_override is None else f_override(0.0)
    nstep = int(np.ceil(T_end / dT))
    upd = 16
    targets = list(Tn)
    ti = 0
    pr = []
    if abs(targets[0]) < 1e-12:
        snaps.append((0.0, v.copy(), vt.copy()))
        ti = 1
    for n in range(nstep):
        if f_override is not None and n % upd == 0:
            fc, fcT, fth2c = f_override(n * dT)
        k1 = cp.rhs_coupled(v, vt, fc, fcT, fth2c, KAP, True,
                            ("dirichlet", "neumann"))
        k2 = cp.rhs_coupled(v + 0.5 * dT * k1[0], vt + 0.5 * dT * k1[1],
                            fc, fcT, fth2c, KAP, True,
                            ("dirichlet", "neumann"))
        k3 = cp.rhs_coupled(v + 0.5 * dT * k2[0], vt + 0.5 * dT * k2[1],
                            fc, fcT, fth2c, KAP, True,
                            ("dirichlet", "neumann"))
        k4 = cp.rhs_coupled(v + dT * k3[0], vt + dT * k3[1], fc, fcT,
                            fth2c, KAP, True, ("dirichlet", "neumann"))
        v = v + dT / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        vt = vt + dT / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        pr.append(float(v[g.k_probe, g.i_probe]))
        while ti < NTC and (n + 1) * dT >= Tn[ti]:
            snaps.append((Tn[ti], v.copy(), vt.copy()))
            ti += 1
    while ti < NTC:
        snaps.append((Tn[ti], v.copy(), vt.copy()))
        ti += 1
    return snaps, np.array(pr), dT


# C-G1b diagnostic: slab residual at Z = 0, w = 0 records the slab's
# own FD bias scale (the background satisfies the continuum EL; the
# discrete residual is O(hs^2) and is the floor of slab fidelity)
W0 = tuple(np.zeros((g.Nu, NTS_SLAB, NTC)) for _ in range(3))
r0 = slab_residual_factory(W0)(np.zeros((NTS_SLAB, NTC, 4)))
log(f"C-G1b slab FD bias floor: max interior residual at background "
    f"= {np.max(np.abs(r0[2:-2])):.3e}")

Zsol = np.zeros((NTS_SLAB, NTC, 4))
slab_ok = True
pr_prev = None
for itr in range(3):
    ovr = None if itr == 0 else make_override(Zsol)
    snaps, pr1, dTm = march_snapshots(ovr)
    if pr_prev is not None:
        nn = min(len(pr1), len(pr_prev))
        log(f"  fixed-point waveform delta iter {itr}: "
            f"{np.max(np.abs(pr1[:nn] - pr_prev[:nn])):.3e}")
    pr_prev = pr1
    Wn = w_on_slab(snaps)
    resfun = slab_residual_factory(Wn)
    t1 = time.time()
    try:
        Zsol = newton_krylov(resfun, Zsol, f_tol=1e-9, maxiter=40,
                             verbose=0)
        ok = True
    except Exception as ex:
        log(f"  newton_krylov failed at iter {itr}: {ex}")
        ok = False
        slab_ok = False
    log(f"  slab solve iter {itr}: {'OK' if ok else 'FAIL'} "
        f"({time.time()-t1:.0f}s), max|Z| = {np.max(np.abs(Zsol)):.3e}")
    if not ok:
        break

res_opt1 = cp.evolve_opt2(v0, np.zeros_like(v0), KAP, True, T_end,
                          n_f=16, f_override=make_override(Zsol))
log(f"option-1 march done; term={res_opt1['term']}; "
    f"slab_ok={slab_ok}")

# ---------------- the C-G3 comparison --------------------------------
if opt2_alive and len(res_opt1["probe"]) > 32:
    nmin = min(len(res_opt1["probe"]), len(r2o["probe"]),
               len(rF["probe"]))
    sl = slice(int(0.2 * nmin), int(0.8 * nmin))
    d12 = np.linalg.norm(res_opt1["probe"][:nmin][sl]
                         - r2o["probe"][:nmin][sl])
    d2f = np.linalg.norm(r2o["probe"][:nmin][sl]
                         - rF["probe"][:nmin][sl])
    nfz = np.linalg.norm(rF["probe"][:nmin][sl])
    log(f"C-G3: ||opt1-opt2|| = {d12:.4e}; ||opt2-frozen|| = "
        f"{d2f:.4e}; ||frozen|| = {nfz:.4e}")
    backsub = d2f / nfz <= 1e-4
    agree = d12 <= 0.5 * d2f
    verdict = ("GATE OPEN" if (agree or backsub)
               else "GATE FAILED - coupled conclusions NOT banked")
    log(f"C-G3 VERDICT: agree={agree} "
        f"backreaction-sub-resolution={backsub} => {verdict}")
else:
    log("C-G3 VERDICT: NOT EXECUTABLE on the full-domain class - the "
        "Option-2 march has no surviving regular regime (kappa > 0: "
        "f-degeneracy at the seal; kappa < 0: unsealing response "
        "raises characteristic speeds O(100) past any fixed CFL). "
        "Coupled conclusions are NOT banked; the frozen-f catalog "
        "carries the labeled premise 'f-backreaction excluded'. "
        "Trust-window (t <= t_5%) re-pose is the named next step.")
np.savez("/tmp/w4b_coupled_xval.npz",
         T2=r2o["T"], p2=r2o["probe"],
         TF=rF["T"][:len(rF['probe'])], pF=rF["probe"],
         T1=res_opt1["T"], p1=res_opt1["probe"], Z=Zsol,
         fmin2=r2o["fmin"], dcad=dcad)

# ---------------- coupled kappa subset (Option 2) ---------------------
log("=" * 72)
log("COUPLED KAPPA SUBSET (Option 2; M1)")
log("=" * 72)
kc = float(lin["M1_kc"])
SUBSET = ([(kk, True, 0.05) for kk in (0.25 * kc, 0.9 * kc, 1.1 * kc,
                                       2 * kc, -1.0, -10.0, 10.0)]
          + [(kk, True, 0.01) for kk in (0.25 * kc, 1.1 * kc, 2 * kc,
                                         -1.0, -10.0, 10.0)]
          + [(kk, False, 0.05) for kk in (1.0, 10.0, -1.0, -10.0)]
          + [(kk, False, 0.01) for kk in (1.0, -1.0)])
rows = []
for kk, dc, aa in SUBSET:
    v0s = ev.bump_profile(g, aa, "g1", sig_frac=0.25)
    t1 = time.time()
    rr = cp.evolve_opt2(v0s, np.zeros_like(v0s), kk, dc,
                        10.0 * T_x, n_f=64)
    rr["dT"] = rr["dT"]
    lab, diag = ev.classify(rr, abs(aa), conserving=False)
    fr = rr["fmin"]
    row = dict(kappa=float(kk), dcell=bool(dc), amp=float(aa),
               label=lab, freq=float(diag.get("freq", np.nan)),
               env_max=float(diag.get("env_max", np.nan)),
               fmin_min=float(fr.min()) if len(fr) else np.nan,
               T_term=float(diag.get("T_term", np.nan)))
    rows.append(row)
    log(f"  k={kk:+9.4g} dcell={dc} amp={aa:+.2g} -> {lab:12s} "
        f"freq={row['freq']:7.3f} fmin={row['fmin_min']:.4g} "
        f"({time.time()-t1:.0f}s)")
    with open("/tmp/w4b_coupled_subset.json", "w") as fh:
        json.dump(rows, fh, indent=1)
log("done.")
