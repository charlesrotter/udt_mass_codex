"""W4 SOLVER AGENT B — script 3: EVOLUTION LIBRARY (imported by runs).

Implements the production solver for the w-channel of
S = C1 + kappa W_wave on frozen / quasi-statically coupled library
backgrounds, in the EXACT variables derived in w4b_sym_energy.py
(23/23):
  v = ln(1+w)  (wave sector exactly free in v; 1+w > 0 automatic)
  per-ray tortoise x: dr/dx = f  (x = 0 at the SEAL end, x_max at the
  weld; unit characteristic speed)
  v_TT = v_xx + 2 (f/r) v_x + S(v; x)            [frozen f]
  S_off(primary) = -(c/(16 kappa)) (f_th^2/r^2) e^{-2v}
  S_on (primary) = +(c/(16 kappa)) (f_th^2/r^2) (e^{v} - e^{-2v})
  S_off(diagonal q=0 frame, labeled variant) = + (c/(16 kappa)) ... e^{-2v}
  E = Sum_k wu_k Int dx [ 2 kappa r^2 (v_T^2 + v_x^2) + V(v; x) ]
  V_off = -(c/8) f_th^2 (e^{-2v} - 1),
  V_on  = -(c/8) f_th^2 (e^{-2v} + 2 e^v - 3)
  dE/dT = [4 kappa r^2 v_x v_T] boundary  (zero for Dirichlet/Neumann)

Integrators: RK4 method-of-lines (PRODUCTION; secular energy drift
< 1e-6 achievable) and leapfrog (independent cross-check integrator).
GPU: torch float64 batched over (kappa, amplitude, ...) with per-batch
CPU asserts (CLAUDE.md pitfalls binding; no batched solve_triangular
with broadcast Cholesky is used anywhere - no Cholesky at all in the
hot path).

PRE-REGISTERED OUTCOME CLASSIFIER (fixed before any production run;
priority order COLLAPSE > GROW > BREATHER > RING > DISPERSE > QUIET):
  COLLAPSE-: terminated with min v <= ln(0.05) ~ -3.0  (1+w -> 0,
             metric degeneracy approach)
  COLLAPSE+: terminated with max v >= +8 (blow-up direction) or nonfinite
  GROW:  not terminated, env(T_end)/env(T_end/2) > 3 and final-quarter
         log-envelope slope > +0.02 / x_max-crossing
  BREATHER: max envelope grew > 3x initial but final-30% envelope slope
         |lam| < 0.005 per crossing (saturated, bounded)
  RING:  bounded in [0.2, 3] x initial envelope over the final 60% with
         >= 3 sign changes of (v_probe - mean) in the final 60%
  DISPERSE: env(T_end) < 0.1 env(0)
  QUIET: none of the above (reported raw)
  UNRESOLVED-STIFF (override, pre-registered before production): a
  nonfinite/blow-up termination with min v > -2 at the last monitor AND
  source stiffness sqrt(max|dS/dv|) * dT > 1 is an INTEGRATOR failure,
  not a physical outcome - reported as UNRESOLVED-STIFF, never banked.
For D_cell-OFF runs the same classifier is applied to (v - v_eq) when a
static equilibrium v_eq exists (computed by Newton in this module), and
the equilibrium displacement is reported separately.

PRE-REGISTERED RUN-VALIDITY GATES:
  G1 (energy): for flux-conserving BC variants the secular drift
     |median(E last 5%) - median(E first 5%)| / max|E| <= 1e-6, else
     the run is INVALID and excluded (counted, reported).
  G2 (resolution): a run-cell is banked only if its classification is
     identical under grid doubling (checked on representatives).
  G3 (GPU trust): torch batch must match the numpy reference stepper
     on >= 2 batch members for 50 steps to <= 1e-11 max abs.

New file. 2026-06-12, W4-B agent.
"""
import numpy as np

S3, S5, S7 = 3**0.5, 5**0.5, 7**0.5
LN_COLLAPSE = float(np.log(0.05))
V_BLOWUP = 8.0


def Yr(u):
    u = np.asarray(u, float)
    return np.array([np.ones_like(u), S3 * u, (S5 / 2) * (3 * u * u - 1),
                     (S7 / 2) * (5 * u**3 - 3 * u)])


def Yru(u):
    u = np.asarray(u, float)
    return np.array([np.zeros_like(u), S3 * np.ones_like(u), 3 * S5 * u,
                     (S7 / 2) * (15 * u * u - 3)])


# ----------------------------------------------------------- geometry
class Geo:
    """Per-member frozen geometry on per-ray tortoise grids.

    Arrays shaped (Nu, Nx): r, f, fth2 (= (1-u^2) f_u^2), tgrid (t of x).
    x-grid per ray is uniform with the SAME Nx; dx differs per ray.
    """

    def __init__(self, npz, tag, Nu=24, Nx=2048):
        t = npz[f"{tag}_t"]
        X = npz[f"{tag}_X"]
        meta = npz[f"{tag}_meta"]
        self.gamma, self.c, self.t_stop, self.t1, self.t5, self.tseal = meta
        self.tag, self.Nu, self.Nx = tag, Nu, Nx
        un, wu = np.polynomial.legendre.leggauss(Nu)
        self.u, self.wu = un, wu
        Y, Yu = Yr(un), Yru(un)             # (4, Nu)
        f_tu = X @ Y                        # (Nt, Nu)
        fu_tu = X @ Yu
        rt = np.exp(-t)
        # tortoise per ray: x(t) = int_t^{t_stop} e^{-t'}/f dt'
        integ = rt[:, None] / f_tu          # (Nt, Nu)
        # cumulative from the seal end (trapezoid on the dense t grid)
        xt = np.zeros_like(integ)
        dts = np.diff(t)
        seg = 0.5 * (integ[1:] + integ[:-1]) * dts[:, None]
        cs = np.concatenate([np.zeros((1, len(un))), np.cumsum(seg, 0)], 0)
        xt = cs[-1][None, :] - cs           # x(t): x(t_stop)=0, x(0)=x_max
        self.xmax = xt[0].copy()            # (Nu,)
        self.xg = np.linspace(0.0, 1.0, Nx)[None, :] * self.xmax[:, None]
        self.dx = self.xg[:, 1] - self.xg[:, 0]            # (Nu,)
        # invert map per ray (xt decreasing in t)
        self.tgrid = np.empty((Nu, Nx))
        for k in range(Nu):
            self.tgrid[k] = np.interp(self.xg[k], xt[::-1, k], t[::-1])
        self.r = np.exp(-self.tgrid)
        self.f = np.empty((Nu, Nx))
        self.fth2 = np.empty((Nu, Nx))
        for k in range(Nu):
            self.f[k] = np.interp(self.tgrid[k], t, f_tu[:, k])
            fu_k = np.interp(self.tgrid[k], t, fu_tu[:, k])
            self.fth2[k] = (1 - un[k]**2) * fu_k**2
        self.a1 = 2.0 * self.f / self.r     # first-order coefficient
        self.sc = self.c * self.fth2 / (16.0 * self.r**2)  # source coeff
        # probe: ray with max integrated fth2, mid-bump point
        self.k_probe = int(np.argmax(self.fth2.sum(1)))
        self.i_probe = int(0.55 * Nx)
        # trapezoid weights in x per ray
        self.wx = np.full((Nu, Nx), 1.0) * self.dx[:, None]
        self.wx[:, 0] *= 0.5
        self.wx[:, -1] *= 0.5


def bump_profile(geo, amp, gshape, x0frac=0.55, sig_frac=0.10):
    """Initial w = amp * g(u) * gaussian(x); returns v0 (Nu, Nx)."""
    u = geo.u
    if gshape == "g1":
        g = (1 - u**2)
    elif gshape == "g2":
        g = u * (1 - u**2) * (3 * S3 / 2) / 1.0
    elif gshape == "g3":
        g = (5 * u**2 - 1) * (1 - u**2)
    else:
        raise ValueError(gshape)
    g = g / np.max(np.abs(g))
    x0 = x0frac * geo.xmax[:, None]
    sig = sig_frac * geo.xmax[:, None]
    bump = np.exp(-((geo.xg - x0) / sig)**2)
    w0 = amp * g[:, None] * bump
    assert np.min(1 + w0) > 0.02, "initial data crosses degeneracy"
    return np.log1p(w0)


# ----------------------------------------------------------- sources
def source(v, geo, kappa, dcell, frame="primary"):
    """S(v; x) of the v-equation. kappa signed. frame: primary|diagonal."""
    sc = geo.sc / kappa
    if dcell:
        assert frame == "primary", "D_cell is defined in the primary frame"
        return sc * (np.exp(v) - np.exp(-2 * v))
    em2 = np.exp(-2 * v)
    return (sc * em2) if frame == "diagonal" else (-sc * em2)


def potential_density(v, geo, dcell, frame="primary"):
    """V(v;x) with V(0)=0 (energy bookkeeping; frame sign carried)."""
    cf = geo.c * geo.fth2 / 8.0
    if dcell:
        return -cf * (np.exp(-2 * v) + 2 * np.exp(v) - 3)
    Voff = -cf * (np.exp(-2 * v) - 1)
    return -Voff if frame == "diagonal" else Voff


def energy(v, vt, geo, kappa, dcell, frame="primary"):
    """Semi-discrete energy of the conservation-form stencil: kinetic +
    potential on nodes (trapezoid), gradient on faces (midpoint r^2).
    Conserved EXACTLY by the spatial discretization for Dirichlet /
    Neumann / Robin ends (Robin adds the boundary term); RK4 time error
    only. Matches Int dx [2 kappa r^2 (v_T^2 + v_x^2) + V] at O(dx^2).
    """
    dx = geo.dx[:, None]
    vxf = (v[:, 1:] - v[:, :-1]) / dx                      # faces
    r2f = 0.5 * (geo.r[:, 1:]**2 + geo.r[:, :-1]**2)
    kin = np.einsum('k,kx,kx->', geo.wu, geo.wx,
                    2 * kappa * geo.r**2 * vt**2
                    + potential_density(v, geo, dcell, frame))
    grad = np.einsum('k,kx,kx->', geo.wu,
                     np.broadcast_to(dx, vxf.shape),
                     2 * kappa * r2f * vxf**2)
    extra = 0.0
    if getattr(geo, "robin_inner", False):
        # boundary energy of the Robin (v_x = h v, h=1) seal end
        extra = float(np.einsum('k,k->', geo.wu,
                                2 * kappa * geo.r[:, 0]**2 * v[:, 0]**2))
    return float(kin + grad + extra)


# ----------------------------------------------------------- stepper (numpy)
def rhs_np(v, vt, geo, kappa, dcell, frame, bc):
    """Returns (dv, dvt). CONSERVATION FORM: the exact identity
    v_xx + 2(f/r) v_x = (1/r^2) d/dx (r^2 v_x)  (r_x = f) is
    discretized as flux differences on faces => the semi-discrete
    energy is exactly conserved (closed BCs). bc = (inner, outer):
    inner in {dirichlet, robin1, neumann}; outer in {neumann,
    dirichlet, outgoing}."""
    Nu, Nx = v.shape
    dx = geo.dx[:, None]
    r2 = geo.r**2
    r2f = 0.5 * (r2[:, 1:] + r2[:, :-1])
    F = r2f * (v[:, 1:] - v[:, :-1]) / dx                  # interior faces
    dvt = np.empty_like(v)
    dvt[:, 1:-1] = (F[:, 1:] - F[:, :-1]) / (dx * r2[:, 1:-1])
    # boundary faces: zero flux default (Neumann); Robin adds h v term
    Fl = np.zeros(Nu)                                      # inner face flux
    if bc[0] == "robin1":
        geo.robin_inner = True
        Fl = r2[:, 0] * 1.0 * v[:, 0]       # p v_x|_0 = r^2 h v (h = 1)
    dvt[:, 0] = (F[:, 0] - Fl) / (dx[:, 0] * r2[:, 0]) * 2  # half-cell
    dvt[:, -1] = (0.0 - F[:, -1]) / (dx[:, 0] * r2[:, -1]) * 2
    dvt += source(v, geo, kappa, dcell, frame)
    dv = vt.copy()
    if bc[0] == "dirichlet":
        dv[:, 0] = 0.0
        dvt[:, 0] = 0.0
    if bc[1] == "dirichlet":
        dv[:, -1] = 0.0
        dvt[:, -1] = 0.0
    if bc[1] == "outgoing":
        # first-order absorbing: v_T = -v_x (one-sided), penalty form
        vx_b = (3 * v[:, -1] - 4 * v[:, -2] + v[:, -3]) / (2 * dx[:, 0])
        dv[:, -1] = -vx_b
        dvt[:, -1] = (-vx_b - vt[:, -1]) / (2 * geo.dt_pen)
    return dv, dvt


def rk4_step(v, vt, dT, geo, kappa, dcell, frame, bc):
    k1v, k1t = rhs_np(v, vt, geo, kappa, dcell, frame, bc)
    k2v, k2t = rhs_np(v + 0.5 * dT * k1v, vt + 0.5 * dT * k1t, geo, kappa,
                      dcell, frame, bc)
    k3v, k3t = rhs_np(v + 0.5 * dT * k2v, vt + 0.5 * dT * k2t, geo, kappa,
                      dcell, frame, bc)
    k4v, k4t = rhs_np(v + dT * k3v, vt + dT * k3t, geo, kappa, dcell,
                      frame, bc)
    return (v + dT / 6 * (k1v + 2 * k2v + 2 * k3v + k4v),
            vt + dT / 6 * (k1t + 2 * k2t + 2 * k3t + k4t))


def stiff_rate(v, geo, kappa, dcell, frame="primary"):
    """sqrt(max |dS/dv|) — source stiffness monitor."""
    sc = np.abs(geo.sc / kappa)
    if dcell:
        d = sc * (np.exp(v) + 2 * np.exp(-2 * v))
    else:
        d = 2 * sc * np.exp(-2 * v)
    return float(np.sqrt(np.max(d)))


def evolve_np(geo, v0, vt0, kappa, dcell, T_end, frame="primary",
              bc=("dirichlet", "neumann"), cfl=0.5, n_mon=200,
              integrator="rk4", store_stride=None, vref=None):
    """CPU reference evolution. Returns dict with monitors + outcome.
    vref: reference field subtracted in probe/env monitors (e.g. a
    static equilibrium); termination monitors stay on absolute v."""
    dT = cfl * float(np.min(geo.dx))
    geo.dt_pen = dT
    nstep = int(np.ceil(T_end / dT))
    v, vt = v0.copy(), vt0.copy()
    vr = np.zeros_like(v) if vref is None else vref
    if integrator == "leapfrog":
        dv, dvt = rhs_np(v, vt, geo, kappa, dcell, frame, bc)
        vm = v - dT * vt + 0.5 * dT**2 * dvt   # Taylor start
    stride = store_stride or max(1, nstep // 4096)
    Ts, probes, envs, Es = [], [], [], []
    term = None
    vlast = (0.0, 0.0)
    for n in range(nstep):
        if integrator == "rk4":
            v, vt = rk4_step(v, vt, dT, geo, kappa, dcell, frame, bc)
        else:
            # leapfrog (conserving BCs only; vt argument unused by dvt)
            dv, dvt = rhs_np(v, vt, geo, kappa, dcell, frame, bc)
            vnew = 2 * v - vm + dT**2 * dvt
            if bc[0] == "dirichlet":
                vnew[:, 0] = 0.0
            if bc[1] == "dirichlet":
                vnew[:, -1] = 0.0
            vt = (vnew - vm) / (2 * dT)   # centered monitor velocity
            vm, v = v, vnew
        if n % stride == 0:
            Ts.append((n + 1) * dT)
            probes.append(float((v - vr)[geo.k_probe, geo.i_probe]))
            envs.append(float(np.max(np.abs(v - vr))))
        if n % n_mon == 0:
            fin = np.all(np.isfinite(v))
            if fin:
                vlast = (float(v.min()), float(v.max()))
            if not fin:
                term = ("COLLAPSE+", (n + 1) * dT)
                break
            mn, mx = vlast
            if mn <= LN_COLLAPSE:
                term = ("COLLAPSE-", (n + 1) * dT)
                break
            if mx >= V_BLOWUP:
                term = ("COLLAPSE+", (n + 1) * dT)
                break
            Es.append(((n + 1) * dT,
                       energy(v, vt, geo, kappa, dcell, frame)))
    sr = stiff_rate(np.clip(v, -10, 10) if np.all(np.isfinite(v))
                    else np.full_like(v, vlast[0]), geo, kappa, dcell,
                    frame)
    return dict(v=v, vt=vt, T=np.array(Ts), probe=np.array(probes),
                env=np.array(envs), E=np.array(Es), term=term, dT=dT,
                nstep=nstep, vlast=vlast, srate=sr)


# ----------------------------------------------------------- classifier
def classify(res, amp0, conserving=True):
    """Pre-registered classifier (header). Returns (label, diag)."""
    diag = {}
    Earr = np.asarray(res["E"])
    if Earr.size:
        # drift over the FINITE prefix only (post-collapse entries are
        # meaningless; conservation is checked while the run lived)
        fin = np.isfinite(Earr[:, 1])
        Earr = Earr[fin]
    if len(Earr) > 10 and conserving:
        E = Earr[:, 1]
        n5 = max(1, len(E) // 20)
        scale = max(np.max(np.abs(E)), 1e-300)
        drift = abs(np.median(E[-n5:]) - np.median(E[:n5])) / scale
        diag["edrift"] = drift
        diag["valid"] = drift <= 1e-6
    else:
        diag["edrift"] = np.nan
        diag["valid"] = True
    env, T = res["env"], res["T"]
    if res["term"]:
        diag["T_term"] = res["term"][1]
        lab = res["term"][0]
        # pre-registered stiffness override (header)
        if (lab == "COLLAPSE+" and res.get("vlast", (0., 0.))[0] > -2
                and res.get("srate", 0.0) * res["dT"] > 1.0):
            return "UNRESOLVED-STIFF", diag
        return lab, diag
    if len(env) < 8:
        return "QUIET", diag
    n = len(env)
    e0 = max(env[0], 1e-300)
    diag["env_final"] = env[-1]
    diag["env_max"] = float(np.max(env))
    # log-envelope slope, final quarter (per x_max-crossing time unit)
    i4 = 3 * n // 4
    sl = np.polyfit(T[i4:], np.log(np.maximum(env[i4:], 1e-300)), 1)[0]
    diag["rate_final"] = sl
    grew = env[-1] / max(env[n // 2], 1e-300) > 3
    if grew and sl > 0.02:
        return "GROW", diag
    if np.max(env) > 3 * e0:
        i3 = int(0.7 * n)
        sl3 = np.polyfit(T[i3:], np.log(np.maximum(env[i3:], 1e-300)),
                         1)[0]
        if abs(sl3) < 0.005:
            return "BREATHER", diag
        if sl3 > 0:
            return "GROW", diag
    i6 = int(0.4 * n)
    tail = env[i6:]
    pr = res["probe"][i6:]
    nz = int(np.sum(np.diff(np.sign(pr - pr.mean())) != 0))
    diag["zero_crossings"] = nz
    if np.all(tail >= 0.2 * e0) and np.all(tail <= 3 * e0) and nz >= 3:
        # ringing frequency from FFT of probe series
        d = pr - pr.mean()
        F = np.abs(np.fft.rfft(d * np.hanning(len(d))))
        fr = np.fft.rfftfreq(len(d), d=(T[i6 + 1] - T[i6]))
        diag["freq"] = float(fr[np.argmax(F[1:]) + 1] * 2 * np.pi)
        return "RING", diag
    if env[-1] < 0.1 * e0:
        return "DISPERSE", diag
    return "QUIET", diag


# ----------------------------------------------------------- equilibrium
def equilibrium_newton(geo, kappa, frame="primary",
                       bc=("dirichlet", "neumann"), tol=1e-12, vinit=None):
    """Static v_eq per ray (D_cell OFF): v_xx + a1 v_x + S(v) = 0.
    Tridiagonal Newton. Returns v_eq (Nu,Nx) or None if any ray fails
    (existence threshold diagnostics in 'info')."""
    Nu, Nx = geo.f.shape
    veq = np.zeros((Nu, Nx)) if vinit is None else vinit.copy()
    info = dict(fail_rays=[])
    sgn = -1.0 if frame == "primary" else +1.0
    for k in range(Nu):
        dx = geo.dx[k]
        vk = veq[k].copy()
        ok = False
        for it in range(80):
            em2 = np.exp(-2 * vk)
            S = sgn * geo.sc[k] / kappa * em2
            Sp = -2 * S
            F = np.zeros(Nx)
            F[1:-1] = (vk[2:] - 2 * vk[1:-1] + vk[:-2]) / dx**2 \
                + geo.a1[k, 1:-1] * (vk[2:] - vk[:-2]) / (2 * dx) \
                + S[1:-1]
            lo = np.full(Nx, 1 / dx**2) - geo.a1[k, :] / (2 * dx)
            di = np.full(Nx, -2 / dx**2) + Sp
            up = np.full(Nx, 1 / dx**2) + geo.a1[k, :] / (2 * dx)
            # BCs: inner dirichlet v=0; outer neumann v[N-1]=v[N-2]
            # banded (3, Nx) layout for solve_banded
            ab = np.zeros((3, Nx))
            ab[0, 2:] = up[1:-1]
            ab[1, 1:-1] = di[1:-1]
            ab[2, :-2] = lo[1:-1]
            ab[1, 0] = 1.0
            ab[0, 1] = 0.0
            F[0] = vk[0] if bc[0] == "dirichlet" else 0.0
            ab[1, -1] = 1.0
            ab[2, -2] = -1.0
            F[-1] = vk[-1] - vk[-2]
            from scipy.linalg import solve_banded
            try:
                dvk = solve_banded((1, 1), ab, -F)
            except Exception:
                break
            lam = 1.0
            if np.max(np.abs(dvk)) > 0.5:
                lam = 0.5 / np.max(np.abs(dvk))
            vk += lam * dvk
            if not np.all(np.isfinite(vk)) or vk.min() < -12:
                break
            if np.max(np.abs(dvk)) * lam < tol:
                ok = True
                break
        if ok:
            veq[k] = vk
        else:
            info["fail_rays"].append(k)
    if info["fail_rays"]:
        return None, info
    return veq, info


# ----------------------------------------------------------- torch batch
def evolve_torch(geo, v0b, vt0b, kappas, dcell, T_end, frame="primary",
                 bc=("dirichlet", "neumann"), cfl=0.5, n_mon=200,
                 device="cuda", cpu_assert=True, log=print, vrefb=None):
    """Batched RK4 evolution. v0b (NB,Nu,Nx); kappas (NB,). Returns
    per-batch monitor dict. GPU trust gate G3 enforced when cpu_assert.
    """
    import torch
    NB, Nu, Nx = v0b.shape
    dev = torch.device(device)
    dx = torch.tensor(geo.dx[:, None], dtype=torch.float64, device=dev)
    a1 = torch.tensor(geo.a1, dtype=torch.float64, device=dev)
    sc = torch.tensor(geo.sc, dtype=torch.float64, device=dev)
    r2 = torch.tensor(geo.r**2, dtype=torch.float64, device=dev)
    cf = torch.tensor(geo.c * geo.fth2 / 8.0, dtype=torch.float64,
                      device=dev)
    wq = torch.tensor(geo.wu[:, None] * geo.wx, dtype=torch.float64,
                      device=dev)
    kap = torch.tensor(kappas, dtype=torch.float64,
                       device=dev)[:, None, None]
    v = torch.tensor(v0b, dtype=torch.float64, device=dev)
    vt = torch.tensor(vt0b, dtype=torch.float64, device=dev)
    dT = cfl * float(np.min(geo.dx))
    nstep = int(np.ceil(T_end / dT))

    def src(vv):
        if dcell:
            return sc / kap * (torch.exp(vv) - torch.exp(-2 * vv))
        e = sc / kap * torch.exp(-2 * vv)
        return e if frame == "diagonal" else -e

    r2f = 0.5 * (r2[:, 1:] + r2[:, :-1])
    wxf = torch.tensor(np.broadcast_to(geo.dx[:, None],
                                       (Nu, Nx - 1)).copy(),
                       dtype=torch.float64, device=dev)
    wuf = torch.tensor(geo.wu[:, None], dtype=torch.float64, device=dev)

    def rhs(vv, vvt):
        # conservation form (mirrors rhs_np exactly)
        F = r2f * (vv[..., 1:] - vv[..., :-1]) / dx
        dvt = torch.empty_like(vv)
        dvt[..., 1:-1] = (F[..., 1:] - F[..., :-1]) / (dx * r2[:, 1:-1])
        Fl = torch.zeros((vv.shape[0], Nu), dtype=torch.float64,
                         device=dev)
        if bc[0] == "robin1":
            Fl = r2[:, 0] * vv[..., 0]
        dvt[..., 0] = (F[..., 0] - Fl) / (dx[:, 0] * r2[:, 0]) * 2
        dvt[..., -1] = (0.0 - F[..., -1]) / (dx[:, 0] * r2[:, -1]) * 2
        dvt = dvt + src(vv)
        dv = vvt.clone()
        if bc[0] == "dirichlet":
            dv[..., 0] = 0
            dvt[..., 0] = 0
        if bc[1] == "dirichlet":
            dv[..., -1] = 0
            dvt[..., -1] = 0
        if bc[1] == "outgoing":
            vxb = (3 * vv[..., -1] - 4 * vv[..., -2]
                   + vv[..., -3]) / (2 * dx[:, 0])
            dv[..., -1] = -vxb
            dvt[..., -1] = (-vxb - vvt[..., -1]) / (2 * dT)
        return dv, dvt

    def energyb(vv, vvt):
        if dcell:
            V = -cf * (torch.exp(-2 * vv) + 2 * torch.exp(vv) - 3)
        else:
            V = -cf * (torch.exp(-2 * vv) - 1)
            if frame == "diagonal":
                V = -V
        E = torch.einsum('kx,bkx->b', wq, 2 * kap * r2 * vvt**2 + V)
        vxf = (vv[..., 1:] - vv[..., :-1]) / dx
        E = E + torch.einsum('kx,bkx->b', wuf * wxf,
                             2 * kap * r2f * vxf**2)
        if bc[0] == "robin1":
            E = E + torch.einsum('k,bk->b', wuf[:, 0],
                                 2 * kap[:, 0, 0, None]
                                 * r2[:, 0] * vv[..., 0]**2)
        return E

    # ---- G3 GPU trust gate: 50 steps vs numpy on 2 batch members.
    # Members chosen as the two LARGEST |kappa| (least-stiff source;
    # stiff members can legitimately blow up inside the 50-step window
    # and NaN==NaN is uncheckable - the gate tests GPU-vs-CPU
    # agreement, which any member witnesses).
    if cpu_assert:
        order = np.argsort(-np.abs(np.asarray(kappas)))
        for bidx in (int(order[0]), int(order[1] if NB > 1 else order[0])):
            vn, vtn = v0b[bidx].copy(), vt0b[bidx].copy()
            geo.dt_pen = dT
            for _ in range(50):
                vn, vtn = rk4_step(vn, vtn, dT, geo, kappas[bidx], dcell,
                                   frame, bc)
            vg, vtg = v[bidx:bidx + 1].clone(), vt[bidx:bidx + 1].clone()
            kk = kap[bidx:bidx + 1]

            def rhs1(vv, vvt, kk=kk):
                nonlocal kap
                ksave = kap
                kap = kk
                out = rhs(vv, vvt)
                kap = ksave
                return out
            for _ in range(50):
                k1v, k1t = rhs1(vg, vtg)
                k2v, k2t = rhs1(vg + 0.5 * dT * k1v, vtg + 0.5 * dT * k1t)
                k3v, k3t = rhs1(vg + 0.5 * dT * k2v, vtg + 0.5 * dT * k2t)
                k4v, k4t = rhs1(vg + dT * k3v, vtg + dT * k3t)
                vg = vg + dT / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
                vtg = vtg + dT / 6 * (k1t + 2 * k2t + 2 * k3t + k4t)
            err = max(float(torch.max(torch.abs(
                vg[0] - torch.tensor(vn, device=dev)))),
                float(torch.max(torch.abs(
                    vtg[0] - torch.tensor(vtn, device=dev)))))
            assert err <= 1e-11, f"G3 GPU trust gate FAILED: {err:.2e}"
        log(f"    G3 GPU trust gate PASS (<=1e-11), dT={dT:.3e}, "
            f"nstep={nstep}")

    stride = max(1, nstep // 4096)
    alive = torch.ones(NB, dtype=torch.bool, device=dev)
    vrf = (torch.zeros_like(v) if vrefb is None else
           torch.tensor(vrefb, dtype=torch.float64, device=dev))
    term_lab = [None] * NB
    term_T = [np.nan] * NB
    vmin_last = np.zeros(NB)
    vmax_last = np.zeros(NB)
    Ts, probes, envs, Es, ETs = [], [], [], [], []
    for n in range(nstep):
        k1v, k1t = rhs(v, vt)
        k2v, k2t = rhs(v + 0.5 * dT * k1v, vt + 0.5 * dT * k1t)
        k3v, k3t = rhs(v + 0.5 * dT * k2v, vt + 0.5 * dT * k2t)
        k4v, k4t = rhs(v + dT * k3v, vt + dT * k3t)
        vN = v + dT / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
        vtN = vt + dT / 6 * (k1t + 2 * k2t + 2 * k3t + k4t)
        # freeze terminated members
        m = alive[:, None, None]
        v = torch.where(m, vN, v)
        vt = torch.where(m, vtN, vt)
        if n % stride == 0:
            Ts.append((n + 1) * dT)
            probes.append((v - vrf)[:, geo.k_probe,
                                    geo.i_probe].cpu().numpy())
            envs.append(torch.amax(torch.abs(v - vrf),
                                   dim=(1, 2)).cpu().numpy())
        if n % n_mon == 0:
            mn = torch.amin(v, dim=(1, 2))
            mx = torch.amax(v, dim=(1, 2))
            fin = torch.isfinite(mx) & torch.isfinite(mn)
            fa = (fin & alive).cpu().numpy()
            vmin_last[fa] = mn.cpu().numpy()[fa]
            vmax_last[fa] = mx.cpu().numpy()[fa]
            cm = (mn <= LN_COLLAPSE) & alive
            cp = ((mx >= V_BLOWUP) | ~fin) & alive
            for arr, labl in ((cm, "COLLAPSE-"), (cp, "COLLAPSE+")):
                idxs = torch.nonzero(arr).flatten().tolist()
                for i in idxs:
                    term_lab[i] = labl
                    term_T[i] = (n + 1) * dT
                    alive[i] = False
            Es.append(energyb(v, vt).cpu().numpy())
            ETs.append((n + 1) * dT)
    vcpu = v.cpu().numpy()
    srates = np.array([
        stiff_rate(np.clip(vcpu[b], -10, 10) if np.all(np.isfinite(
            vcpu[b])) else np.full_like(vcpu[b], vmin_last[b]),
            geo, kappas[b], dcell, frame) for b in range(NB)])
    return dict(T=np.array(Ts), probe=np.array(probes).T,
                env=np.array(envs).T, E=np.array(Es).T,
                ET=np.array(ETs), term_lab=term_lab,
                term_T=term_T, dT=dT, nstep=nstep,
                v=vcpu, vt=vt.cpu().numpy(),
                vmin_last=vmin_last, vmax_last=vmax_last, srate=srates)


def classify_batch(resb, b, amp0, conserving=True):
    res = dict(T=resb["T"], probe=resb["probe"][b], env=resb["env"][b],
               E=np.column_stack([resb["ET"], resb["E"][b]]),
               term=(None if resb["term_lab"][b] is None
                     else (resb["term_lab"][b], resb["term_T"][b])),
               vlast=(resb["vmin_last"][b], resb["vmax_last"][b]),
               srate=resb["srate"][b], dT=resb["dT"])
    return classify(res, amp0, conserving)
