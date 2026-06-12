"""W5 ARM-2 — SCRIPT 2: NUMERIC LIBRARY (untruncated species solvers).

Date: 2026-06-12.  New file; REUSES (by import, never edit) the
committed validated machinery: w4b_verifier_lib (member flow, per-ray
t-chart weights p = f e^{-t}, b = (f_th^2/f) e^{-t}; VB4's own
independent engine) and w4b_evolib.classify (the pre-registered W4
outcome classifier, applied unchanged).

THE SOURCES (exact, from w5_arm2_sym.py — checks C3/C4/E1/D1):
  v-equation per ray (frozen f), v = ln(1+w):
    v_TT = Lin[v] + S,
    S_off = -(cc/(16 k)) (fth^2/r^2) e^{-2v} (1 - 2k/f)        [beta=0]
    S_on  = +(cc/(16 k)) (fth^2/r^2) [e^v - (1 - 2k/f) e^{-2v}] [beta=1]
  static t-chart:   (p v')' = -m * S,   m = e^{-3t}/f
  dressed pencil:   -(p psi')' - [(cc/(8k))(1-2k/f) e^{-2vb}
                    + beta (cc/(16k)) e^{vb}] b psi = omega^2 m psi
  energy (T,x):     E = Int dx [2 k r^2 (v_T^2 + v_x^2) + V],
    V_off = -(cc/8) fth^2 (1-2k/f) (e^{-2v}-1),
    V_on  = V_off - (cc/4) fth^2 (e^v - 1)
  dE/dT = boundary flux exactly (sym check D1).

SWITCHES (the continuity gates live on these):
  cc        : source convention constant.  TRUE value = 2 (sym check
              G1).  cc = member-c reproduces the W4-B banked unit
              (geo.c conflation, on record).
  species   : True = untruncated (W5); False = W4 truncation
              (factor (1-2k/f) -> 1 and the ON e^v term unchanged).
  t_b       : inner cut (t_stop full domain == W4 class; t5 / t1
              trust windows == VB4-vindicated primary class).

GPU per CLAUDE.md: batched torch float64 evolutions (elementwise only;
no solve_triangular anywhere); batched torch.linalg.eigvalsh for
pencil sweeps with DIAGONAL mass reduction (no Cholesky); per-batch
CPU asserts.  2026-06-12, W5 Arm-2 agent.
"""
import numpy as np
import scipy.linalg as sla
from scipy.linalg import solve_banded
import sys
sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
import w4b_verifier_lib as vl
import w4b_evolib as ev4

CC_TRUE = 2.0
LN_COLLAPSE = float(np.log(0.05))
V_BLOWUP = 8.0


# ------------------------------------------------------------ geometry
class GeoW5:
    """Per-ray geometry of a member on [0, t_b], both charts.

    t-chart arrays (Nt, Nu): f, fth2, p, b, m  (verifier-lib species).
    x-chart arrays (Nu, Nx): r, f, fth2, locus factor (1 - 2k/f) built
    per kappa at run time.  x = 0 at the INNER CUT t_b, x_max at weld.
    """

    def __init__(self, mem, t_b=None, Nt=4000, Nx=1024):
        self.mem = mem
        self.t_b = float(mem.t_stop if t_b is None else t_b)
        self.Nu = mem.Nu
        self.u, self.wu = mem.u, mem.wu
        self.tg = np.linspace(0.0, self.t_b, Nt)
        Z = mem.X  # (Ntm, 4) on mem.tg
        self.X = np.array([np.interp(self.tg, mem.tg, Z[:, i])
                           for i in range(4)]).T
        Y, Yu = vl.Yr(mem.u), vl.Yru(mem.u)
        self.f_t = self.X @ Y                       # (Nt, Nu)
        fu_t = self.X @ Yu
        self.fth2_t = (1 - mem.u[None, :] ** 2) * fu_t ** 2
        et = np.exp(-self.tg)[:, None]
        self.p_t = self.f_t * et
        self.b_t = self.fth2_t / self.f_t * et
        self.m_t = np.exp(-3 * self.tg)[:, None] / self.f_t
        # x-chart (per-ray tortoise from the cut end)
        integ = et / self.f_t
        h = self.tg[1] - self.tg[0]
        cs = np.concatenate([np.zeros((1, self.Nu)),
                             np.cumsum(0.5 * (integ[1:] + integ[:-1]),
                                       0) * h])
        x_of_t = cs[-1][None, :] - cs               # x(t_b)=0, x(0)=xmax
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
            self.f[k] = np.interp(self.t_of_x[k], self.tg, self.f_t[:, k])
            self.fth2[k] = np.interp(self.t_of_x[k], self.tg,
                                     self.fth2_t[:, k])
        self.r = np.exp(-self.t_of_x)
        self.k_probe = int(np.argmax(self.fth2.sum(1)))
        self.i_probe = int(0.55 * Nx)
        self.wx = np.full((self.Nu, Nx), 1.0) * self.dx[:, None]
        self.wx[:, 0] *= 0.5
        self.wx[:, -1] *= 0.5
        # x-position of the locus f = 2k per ray is computed at run time

    def locus_t(self, kappa):
        """per-ray t where f(t) = 2 kappa (first crossing from weld);
        nan if absent on [0, t_b]."""
        out = np.full(self.Nu, np.nan)
        for k in range(self.Nu):
            d = self.f_t[:, k] - 2 * kappa
            sgn = np.sign(d)
            idx = np.where(np.diff(sgn) != 0)[0]
            if len(idx):
                i = idx[0]
                a = d[i] / (d[i] - d[i + 1])
                out[k] = self.tg[i] + a * (self.tg[i + 1] - self.tg[i])
        return out


# ------------------------------------------------------------- sources
def factor(geo_f, kappa, species):
    return (1.0 - 2.0 * kappa / geo_f) if species else 1.0


def source_x(v, geo, kappa, dcell, cc=CC_TRUE, species=True):
    """S(v;x) of the v-equation (x-chart arrays)."""
    sc = cc * geo.fth2 / (16.0 * geo.r ** 2) / kappa
    fac = factor(geo.f, kappa, species)
    if dcell:
        return sc * (np.exp(v) - fac * np.exp(-2 * v))
    return -sc * fac * np.exp(-2 * v)


def dsource_x(v, geo, kappa, dcell, cc=CC_TRUE, species=True):
    sc = cc * geo.fth2 / (16.0 * geo.r ** 2) / kappa
    fac = factor(geo.f, kappa, species)
    if dcell:
        return sc * (np.exp(v) + 2 * fac * np.exp(-2 * v))
    return 2 * sc * fac * np.exp(-2 * v)


def potential_density(v, geo, kappa, dcell, cc=CC_TRUE, species=True):
    """V(v;x), V(0) = 0 (energy bookkeeping; sym check D1)."""
    fac = factor(geo.f, kappa, species)
    V = -(cc / 8.0) * geo.fth2 * fac * (np.exp(-2 * v) - 1)
    if dcell:
        V = V - (cc / 4.0) * geo.fth2 * (np.exp(v) - 1)
    return V


# ------------------------------------------------- static equilibria (t)
def equilibrium_ray_t(geo, k, kappa, dcell, cc=CC_TRUE, species=True,
                      vinit=None, tol=1e-12, maxit=80):
    """Newton solve of (p v')' = -m S(v) on the t-grid of ray k.
    BCs: Neumann at the weld t=0 (natural), Dirichlet v=0 at t_b.
    Returns v(t) or None."""
    tg = geo.tg
    h = tg[1] - tg[0]
    p = geo.p_t[:, k]
    b = geo.b_t[:, k]
    f = geo.f_t[:, k]
    N = len(tg)
    pm = 0.5 * (p[1:] + p[:-1])
    fac = (1.0 - 2.0 * kappa / f) if species else np.ones(N)
    lam = cc / (16.0 * kappa)

    def S_t(v):
        # -m*S expressed in t-weights:  (p v')' = RHS(v)
        if dcell:
            return lam * b * (fac * np.exp(-2 * v) - np.exp(v))
        return lam * b * fac * np.exp(-2 * v)

    def Sp_t(v):
        if dcell:
            return lam * b * (-2 * fac * np.exp(-2 * v) - np.exp(v))
        return -2 * lam * b * fac * np.exp(-2 * v)

    v = np.zeros(N) if vinit is None else vinit.copy()
    for it in range(maxit):
        R = S_t(v)
        F = np.zeros(N)
        F[1:-1] = (pm[1:] * (v[2:] - v[1:-1])
                   - pm[:-1] * (v[1:-1] - v[:-2])) / h ** 2 - R[1:-1]
        F[0] = pm[0] * (v[1] - v[0]) / (0.5 * h ** 2) - R[0]
        F[-1] = v[-1]
        Sp = Sp_t(v)
        lo = np.zeros(N); di = np.zeros(N); up = np.zeros(N)
        di[1:-1] = -(pm[1:] + pm[:-1]) / h ** 2 - Sp[1:-1]
        up[1:-1] = pm[1:] / h ** 2
        lo[1:-1] = pm[:-1] / h ** 2
        di[0] = -pm[0] / (0.5 * h ** 2) - Sp[0]
        up[0] = pm[0] / (0.5 * h ** 2)
        di[-1] = 1.0
        ab = np.zeros((3, N))
        ab[0, 1:] = up[:-1]
        ab[1, :] = di
        ab[2, :-1] = lo[1:]
        try:
            dv = solve_banded((1, 1), ab, -F)
        except Exception:
            return None
        if not np.all(np.isfinite(dv)):
            return None
        step = np.max(np.abs(dv))
        lamf = 1.0 if step < 0.5 else 0.5 / step
        v = v + lamf * dv
        if not np.all(np.isfinite(v)) or v.min() < -14 or v.max() > 30:
            return None
        if step * lamf < tol:
            return v
    return None


def equilibrium_member(geo, kappa, dcell, cc=CC_TRUE, species=True,
                       vinit=None):
    """All-ray equilibrium; returns (Nu, Nt) or None + failed rays."""
    out = np.zeros((geo.Nu, len(geo.tg)))
    fails = []
    for k in range(geo.Nu):
        vi = None if vinit is None else vinit[k]
        v = equilibrium_ray_t(geo, k, kappa, dcell, cc, species, vinit=vi)
        if v is None:
            fails.append(k)
        else:
            out[k] = v
    return (None if fails else out), fails


# --------------------------------------------------- pencil (t-chart FD)
def pencil_ray(geo, k, kappa, dcell, cc=CC_TRUE, species=True,
               vbar=None, nev=4, bc_weld='N'):
    """-(p psi')' + q psi = w2 m psi on ray k; Dirichlet at t_b,
    Neumann (natural) or Dirichlet at the weld.  vbar = dressed
    background (None = frozen v=0, labeled FROZEN).  Dense sym eigh.
    Returns (w2[nev], vecs, tgrid_kept)."""
    tg = geo.tg
    h = tg[1] - tg[0]
    p = geo.p_t[:, k]
    b = geo.b_t[:, k]
    m = geo.m_t[:, k]
    f = geo.f_t[:, k]
    N = len(tg)
    vb = np.zeros(N) if vbar is None else vbar
    fac = (1.0 - 2.0 * kappa / f) if species else np.ones(N)
    q = -(cc / (8.0 * kappa)) * fac * np.exp(-2 * vb) * b
    if dcell:
        q = q - (cc / (16.0 * kappa)) * np.exp(vb) * b
    pm = 0.5 * (p[1:] + p[:-1])
    wts = np.full(N, h); wts[0] = wts[-1] = h / 2
    dmain = np.zeros(N)
    dmain[:-1] += pm / h
    dmain[1:] += pm / h
    dmain += q * wts
    doff = -pm / h
    M = m * wts
    keep = np.arange(N - 1)          # Dirichlet at t_b (last node)
    if bc_weld == 'D':
        keep = keep[1:]
    Mi = 1.0 / np.sqrt(M[keep])
    # symmetric diagonal congruence keeps tridiagonal structure:
    dmK = dmain[keep] * Mi ** 2
    # off-diagonal entries between kept nodes i,i+1:
    off = doff[keep[0]:keep[0] + len(keep) - 1] * Mi[:-1] * Mi[1:]
    w2, V = sla.eigh_tridiagonal(dmK, off, select='i',
                                 select_range=(0, nev - 1))
    return w2, (Mi[:, None] * V), tg[keep]


def pencil_member_gpu(geo, kappas, dcell, cc=CC_TRUE, species=True,
                      vbars=None, nev=4, Ncoarse=600, cpu_spots=3):
    """Batched frozen/dressed pencil over (kappa x ray) on the GPU.
    Coarsened t-grid (Ncoarse) for the dense batch; CPU eigh asserts.
    vbars: dict kappa -> (Nu, Nt) dressed background or None.
    Returns w2 array (nk, Nu, nev)."""
    import torch
    dev = 'cuda' if torch.cuda.is_available() else 'cpu'
    tg = geo.tg
    idx = np.linspace(0, len(tg) - 1, Ncoarse).astype(int)
    tgc = tg[idx]
    h = tgc[1] - tgc[0]
    nk, Nu = len(kappas), geo.Nu
    N = Ncoarse
    A = np.zeros((nk, Nu, N - 1, N - 1))
    for ik, kap in enumerate(kappas):
        for k in range(Nu):
            p = geo.p_t[idx, k]; b = geo.b_t[idx, k]
            m = geo.m_t[idx, k]; f = geo.f_t[idx, k]
            vb = (np.zeros(N) if (vbars is None or vbars.get(kap) is None)
                  else vbars[kap][k][idx])
            fac = (1.0 - 2.0 * kap / f) if species else np.ones(N)
            q = -(cc / (8.0 * kap)) * fac * np.exp(-2 * vb) * b
            if dcell:
                q = q - (cc / (16.0 * kap)) * np.exp(vb) * b
            pm = 0.5 * (p[1:] + p[:-1])
            wts = np.full(N, h); wts[0] = wts[-1] = h / 2
            dmain = np.zeros(N)
            dmain[:-1] += pm / h
            dmain[1:] += pm / h
            Ak = np.diag(dmain + q * wts) + np.diag(-pm / h, 1) \
                + np.diag(-pm / h, -1)
            Mi = 1.0 / np.sqrt(m * wts)
            As = (Mi[:, None] * Ak * Mi[None, :])[:-1, :-1]
            A[ik, k] = 0.5 * (As + As.T)
    At = torch.tensor(A.reshape(nk * Nu, N - 1, N - 1), device=dev)
    w2 = torch.linalg.eigvalsh(At)[:, :nev].cpu().numpy()
    w2 = w2.reshape(nk, Nu, nev)
    # CPU spot asserts (pitfall discipline)
    rng = np.random.default_rng(5)
    for _ in range(cpu_spots):
        ik = int(rng.integers(nk)); k = int(rng.integers(Nu))
        evc = sla.eigh(A[ik, k], eigvals_only=True,
                       subset_by_index=[0, nev - 1])
        dev_ = np.max(np.abs(evc - w2[ik, k])
                      / np.maximum(np.abs(evc), 1.0))
        # tolerance 1e-5 RELATIVE (amended twice, on record): at
        # |kappa| ~ 1e-3 the potential term and the e^{-3t}/f mass
        # scaling push matrix entries to ~1e9-1e10; the float64
        # eigensolve floor at that conditioning is ~1e-6 relative
        # (observed 1.4e-6 torch-vs-scipy on identical matrices; same
        # species as the W4-A 1e-7 amendment, w4a_p2_spectra.py:229).
        # The band-relevant eigenvalues (|w2| <~ 1e2 at |kappa| >~
        # 0.05) carry absolute agreement far below any reported digit.
        assert dev_ < 1e-5, f"GPU/CPU eigensolve mismatch {dev_:.1e}"
    return w2


# ----------------------------------------------- evolution (x-chart)
def rhs_np(v, vt, geo, kappa, dcell, cc, species, bc):
    """Conservation form (identical stencil to the W4 evolib; only the
    source differs).  bc = (inner@x=0/cut, outer@weld)."""
    dx = geo.dx[:, None]
    r2 = geo.r ** 2
    r2f = 0.5 * (r2[:, 1:] + r2[:, :-1])
    F = r2f * (v[:, 1:] - v[:, :-1]) / dx
    dvt = np.empty_like(v)
    dvt[:, 1:-1] = (F[:, 1:] - F[:, :-1]) / (dx * r2[:, 1:-1])
    dvt[:, 0] = (F[:, 0] - 0.0) / (dx[:, 0] * r2[:, 0]) * 2
    dvt[:, -1] = (0.0 - F[:, -1]) / (dx[:, 0] * r2[:, -1]) * 2
    dvt += source_x(v, geo, kappa, dcell, cc, species)
    dv = vt.copy()
    if bc[0] == "dirichlet":
        dv[:, 0] = 0.0
        dvt[:, 0] = 0.0
    if bc[1] == "dirichlet":
        dv[:, -1] = 0.0
        dvt[:, -1] = 0.0
    return dv, dvt


def rk4_step(v, vt, dT, geo, kappa, dcell, cc, species, bc):
    k1 = rhs_np(v, vt, geo, kappa, dcell, cc, species, bc)
    k2 = rhs_np(v + .5 * dT * k1[0], vt + .5 * dT * k1[1], geo, kappa,
                dcell, cc, species, bc)
    k3 = rhs_np(v + .5 * dT * k2[0], vt + .5 * dT * k2[1], geo, kappa,
                dcell, cc, species, bc)
    k4 = rhs_np(v + dT * k3[0], vt + dT * k3[1], geo, kappa, dcell, cc,
                species, bc)
    return (v + dT / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]),
            vt + dT / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]))


def energy_np(v, vt, geo, kappa, dcell, cc, species):
    dx = geo.dx[:, None]
    vxf = (v[:, 1:] - v[:, :-1]) / dx
    r2f = 0.5 * (geo.r[:, 1:] ** 2 + geo.r[:, :-1] ** 2)
    kin = np.einsum('k,kx,kx->', geo.mem.wu, geo.wx,
                    2 * kappa * geo.r ** 2 * vt ** 2
                    + potential_density(v, geo, kappa, dcell, cc, species))
    grad = np.einsum('k,kx,kx->', geo.mem.wu,
                     np.broadcast_to(dx, vxf.shape),
                     2 * kappa * r2f * vxf ** 2)
    return float(kin + grad)


def evolve_np(geo, v0, vt0, kappa, dcell, T_end, cc=CC_TRUE,
              species=True, bc=("dirichlet", "neumann"), cfl=0.5,
              n_mon=200, vref=None):
    dT = cfl * float(np.min(geo.dx))
    nstep = int(np.ceil(T_end / dT))
    v, vt = v0.copy(), vt0.copy()
    vr = np.zeros_like(v) if vref is None else vref
    stride = max(1, nstep // 4096)
    Ts, probes, envs, Es = [], [], [], []
    term = None
    vlast = (0.0, 0.0)
    for n in range(nstep):
        v, vt = rk4_step(v, vt, dT, geo, kappa, dcell, cc, species, bc)
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
            if vlast[0] <= LN_COLLAPSE:
                term = ("COLLAPSE-", (n + 1) * dT)
                break
            if vlast[1] >= V_BLOWUP:
                term = ("COLLAPSE+", (n + 1) * dT)
                break
            Es.append(((n + 1) * dT,
                       energy_np(v, vt, geo, kappa, dcell, cc, species)))
    sr = float(np.sqrt(np.max(np.abs(dsource_x(
        np.clip(v, -10, 10) if np.all(np.isfinite(v))
        else np.full_like(v, vlast[0]), geo, kappa, dcell, cc,
        species)))))
    return dict(v=v, vt=vt, T=np.array(Ts), probe=np.array(probes),
                env=np.array(envs), E=np.array(Es), term=term, dT=dT,
                nstep=nstep, vlast=vlast, srate=sr)


def evolve_torch(geo, v0b, vt0b, kappas, dcell, T_end, cc=CC_TRUE,
                 species=True, bc=("dirichlet", "neumann"), cfl=0.5,
                 n_mon=200, device="cuda", cpu_assert=True, log=print,
                 vrefb=None):
    """Batched RK4 over kappa (mirrors w4b_evolib.evolve_torch; new
    source; G3 GPU-trust gate enforced)."""
    import torch
    NB, Nu, Nx = v0b.shape
    dev = torch.device(device if torch.cuda.is_available() else "cpu")
    dx = torch.tensor(geo.dx[:, None], dtype=torch.float64, device=dev)
    r2 = torch.tensor(geo.r ** 2, dtype=torch.float64, device=dev)
    fT = torch.tensor(geo.f, dtype=torch.float64, device=dev)
    scb = torch.tensor(cc * geo.fth2 / (16.0 * geo.r ** 2),
                       dtype=torch.float64, device=dev)
    cf = torch.tensor(geo.fth2, dtype=torch.float64, device=dev)
    wq = torch.tensor(geo.mem.wu[:, None] * geo.wx, dtype=torch.float64,
                      device=dev)
    kap = torch.tensor(np.asarray(kappas, float),
                       device=dev)[:, None, None]
    fac = (1.0 - 2.0 * kap / fT) if species else torch.ones_like(
        kap * fT)
    v = torch.tensor(v0b, dtype=torch.float64, device=dev)
    vt = torch.tensor(vt0b, dtype=torch.float64, device=dev)
    dT = cfl * float(np.min(geo.dx))
    nstep = int(np.ceil(T_end / dT))
    r2f = 0.5 * (r2[:, 1:] + r2[:, :-1])
    wxf = torch.tensor(np.broadcast_to(geo.dx[:, None],
                                       (Nu, Nx - 1)).copy(),
                       dtype=torch.float64, device=dev)
    wuf = torch.tensor(geo.mem.wu[:, None], dtype=torch.float64,
                       device=dev)

    def src(vv):
        if dcell:
            return scb / kap * (torch.exp(vv) - fac * torch.exp(-2 * vv))
        return -scb / kap * fac * torch.exp(-2 * vv)

    def rhs(vv, vvt):
        F = r2f * (vv[..., 1:] - vv[..., :-1]) / dx
        dvt = torch.empty_like(vv)
        dvt[..., 1:-1] = (F[..., 1:] - F[..., :-1]) / (dx * r2[:, 1:-1])
        dvt[..., 0] = F[..., 0] / (dx[:, 0] * r2[:, 0]) * 2
        dvt[..., -1] = (0.0 - F[..., -1]) / (dx[:, 0] * r2[:, -1]) * 2
        dvt = dvt + src(vv)
        dv = vvt.clone()
        if bc[0] == "dirichlet":
            dv[..., 0] = 0
            dvt[..., 0] = 0
        if bc[1] == "dirichlet":
            dv[..., -1] = 0
            dvt[..., -1] = 0
        return dv, dvt

    def energyb(vv, vvt):
        V = -(cc / 8.0) * cf * fac * (torch.exp(-2 * vv) - 1)
        if dcell:
            V = V - (cc / 4.0) * cf * (torch.exp(vv) - 1)
        E = torch.einsum('kx,bkx->b', wq, 2 * kap * r2 * vvt ** 2 + V)
        vxf = (vv[..., 1:] - vv[..., :-1]) / dx
        E = E + torch.einsum('kx,bkx->b', wuf * wxf,
                             2 * kap * r2f * vxf ** 2)
        return E

    if cpu_assert:
        # G3 members = the two LARGEST |kappa| (least-stiff source) —
        # the committed w4b_evolib convention: stiff members can
        # legitimately blow up inside the 50-step window and NaN==NaN
        # is uncheckable; the gate tests GPU-vs-CPU agreement, which
        # any member witnesses.
        order = np.argsort(-np.abs(np.asarray(kappas)))
        for bidx in {int(order[0]), int(order[1] if NB > 1 else order[0])}:
            vn, vtn = v0b[bidx].copy(), vt0b[bidx].copy()
            for _ in range(50):
                vn, vtn = rk4_step(vn, vtn, dT, geo, kappas[bidx],
                                   dcell, cc, species, bc)
            vg = v[bidx:bidx + 1].clone()
            vtg = vt[bidx:bidx + 1].clone()
            kk = kap[bidx:bidx + 1]
            fck = fac[bidx:bidx + 1] if species else fac[:1]

            def rhs1(vv, vvt):
                F = r2f * (vv[..., 1:] - vv[..., :-1]) / dx
                dvt = torch.empty_like(vv)
                dvt[..., 1:-1] = (F[..., 1:] - F[..., :-1]) \
                    / (dx * r2[:, 1:-1])
                dvt[..., 0] = F[..., 0] / (dx[:, 0] * r2[:, 0]) * 2
                dvt[..., -1] = -F[..., -1] / (dx[:, 0] * r2[:, -1]) * 2
                if dcell:
                    dvt = dvt + scb / kk * (torch.exp(vv)
                                            - fck * torch.exp(-2 * vv))
                else:
                    dvt = dvt - scb / kk * fck * torch.exp(-2 * vv)
                dv = vvt.clone()
                if bc[0] == "dirichlet":
                    dv[..., 0] = 0
                    dvt[..., 0] = 0
                if bc[1] == "dirichlet":
                    dv[..., -1] = 0
                    dvt[..., -1] = 0
                return dv, dvt
            for _ in range(50):
                k1v, k1t = rhs1(vg, vtg)
                k2v, k2t = rhs1(vg + .5 * dT * k1v, vtg + .5 * dT * k1t)
                k3v, k3t = rhs1(vg + .5 * dT * k2v, vtg + .5 * dT * k2t)
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
        k2v, k2t = rhs(v + .5 * dT * k1v, vt + .5 * dT * k1t)
        k3v, k3t = rhs(v + .5 * dT * k2v, vt + .5 * dT * k2t)
        k4v, k4t = rhs(v + dT * k3v, vt + dT * k3t)
        vN = v + dT / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
        vtN = vt + dT / 6 * (k1t + 2 * k2t + 2 * k3t + k4t)
        m_ = alive[:, None, None]
        v = torch.where(m_, vN, v)
        vt = torch.where(m_, vtN, vt)
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
                for i in torch.nonzero(arr).flatten().tolist():
                    term_lab[i] = labl
                    term_T[i] = (n + 1) * dT
                    alive[i] = False
            Es.append(energyb(v, vt).cpu().numpy())
            ETs.append((n + 1) * dT)
    vcpu = v.cpu().numpy()
    srates = np.array([float(np.sqrt(np.max(np.abs(dsource_x(
        np.clip(vcpu[bb], -10, 10) if np.all(np.isfinite(vcpu[bb]))
        else np.full_like(vcpu[bb], vmin_last[bb]), geo, kappas[bb],
        dcell, cc, species))))) for bb in range(NB)])
    return dict(T=np.array(Ts), probe=np.array(probes).T,
                env=np.array(envs).T, E=np.array(Es).T,
                ET=np.array(ETs), term_lab=term_lab, term_T=term_T,
                dT=dT, nstep=nstep, v=vcpu, vt=vt.cpu().numpy(),
                vmin_last=vmin_last, vmax_last=vmax_last, srate=srates)


def classify_batch(resb, b, amp0, conserving=True):
    res = dict(T=resb["T"], probe=resb["probe"][b], env=resb["env"][b],
               E=np.column_stack([resb["ET"], resb["E"][b]]),
               term=(None if resb["term_lab"][b] is None
                     else (resb["term_lab"][b], resb["term_T"][b])),
               vlast=(resb["vmin_last"][b], resb["vmax_last"][b]),
               srate=resb["srate"][b], dT=resb["dT"])
    return ev4.classify(res, amp0, conserving)


def bump_profile(geo, amp, x0frac=0.55, sig_frac=0.10):
    u = geo.mem.u
    g = (1 - u ** 2)
    g = g / np.max(np.abs(g))
    x0 = x0frac * geo.xmax[:, None]
    sig = sig_frac * geo.xmax[:, None]
    w0 = amp * g[:, None] * np.exp(-((geo.xg - x0) / sig) ** 2)
    assert np.min(1 + w0) > 0.02
    return np.log1p(w0)


# -------------------------------------------------------- edge finders
def kappa_c_member(geo, dcell, cc=CC_TRUE, species=True, dressed=True,
                   klo=1e-4, khi=50.0, nbis=40, sign=+1):
    """gap edge: largest kappa (sign branch) where the lowest dressed
    (or frozen) pencil eigenvalue is negative; log-bisection on
    omega^2_min(kappa) sign with warm-started equilibria."""
    cache = {}

    def w2min(kap):
        kk = sign * kap
        vb = None
        if dressed:
            vb, fails = equilibrium_member(geo, kk, dcell, cc, species)
            if vb is None:
                return None     # no static background: not in band
        w2s = [pencil_ray(geo, k, kk, dcell, cc, species,
                          vbar=None if vb is None else vb[k],
                          nev=1)[0][0] for k in range(geo.Nu)]
        return min(w2s)

    lo, hi = klo, khi
    wlo = w2min(lo)
    whi = w2min(hi)
    info = dict(wlo=wlo, whi=whi)
    if wlo is None or whi is None or not (wlo < 0 <= whi):
        return None, info
    for _ in range(nbis):
        mid = np.sqrt(lo * hi)
        wm = w2min(mid)
        if wm is None or wm < 0:
            lo = mid
        else:
            hi = mid
    return np.sqrt(lo * hi), info


def kappa_s_member(geo, dcell, cc=CC_TRUE, species=True, sign=+1,
                   klo=1e-4, khi=200.0, nbis=44):
    """static-existence edge by direct kappa-continuation (warm
    starts from the existing side).  Orientation-agnostic: the W4
    OFF-branch fold has existence at LARGE |kappa| and failure at
    small (source ~ 1/kappa); the untruncated source is NOT a
    one-lambda Bratu family, so no scaling shortcut is used.
    Returns (edge, status):  edge = the existence boundary in (klo,
    khi); np.inf = exists everywhere in range; None = nowhere."""
    def exists(kap, vinit=None):
        v, fails = equilibrium_member(geo, sign * kap, dcell, cc,
                                      species, vinit=vinit)
        return v

    vlo = exists(klo)
    vhi = exists(khi)
    if vlo is not None and vhi is not None:
        return np.inf, "exists at both ends (no fold in range)"
    if vlo is None and vhi is None:
        return None, "no equilibrium at either end"
    upper_exists = vhi is not None
    lo, hi = klo, khi
    vgood = vhi if upper_exists else vlo
    for _ in range(nbis):
        mid = np.sqrt(lo * hi)
        v2 = exists(mid, vgood)
        if v2 is None:
            if upper_exists:
                lo = mid
            else:
                hi = mid
        else:
            vgood = v2
            if upper_exists:
                hi = mid
            else:
                lo = mid
    return np.sqrt(lo * hi), ("edge: exists %s" %
                              ("above" if upper_exists else "below"))
