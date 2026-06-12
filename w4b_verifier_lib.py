"""W4-B BLIND VERIFIER library (independent machinery; never edits
committed files). Re-implements from the stated conventions only:

  recipe: f(t,u) = X(t).Y(u), Y orthonormal Legendre (Y0..Y3);
  EL flow X_tt - X_t = 2 P_X, P = (1/8) Int (1-u^2) f_u^2 / f du;
  weld data X(0) = (1,0,0,0), X_t(0) = (gamma, -c, 0, 0);
  stop at absolute f_min = 0.002. (DOP853, rtol 1e-11/atol 1e-12,
  Gauss-Legendre N = 2000 -- the recipe's own definition constants.)

INDEPENDENT CHOICES (deliberately different from the W4-B agent code):
  - f_min of the cubic-in-u f via the EXACT quadratic-root formula for
    f_u (analytic, not numeric refine);
  - all edge computations are posed in the FLOW VARIABLE t, not the
    tortoise x (the two are related by dx = -e^{-t}/f dt; the
    quadratic forms transform exactly):
       Int r^2 v_x^2 dx   = Int p(t) v_t^2 dt,   p = f e^{-t}
       Int f_th^2 v^2 dx  = Int b(t) v^2 dt,     b = (f_th^2/f) e^{-t}
    seal end (x=0) = t_stop (Dirichlet), weld (x_max) = t=0 (Neumann,
    natural);
  - kappa_c(ray) = 3c/(16 mu_1),  mu_1 = min_v Int p v_t^2 / Int b v^2
    (P1 FEM on a uniform t grid, own assembly);
  - kappa_s(ray) = c/(16 lam*),   lam* = fold of (p v')' = lam b e^{-2v}
    (own damped-Newton continuation, geometric lambda ladder + bisect);
  - member edges = max over rays (first ray to close the gap / lose
    its equilibrium).

New file. 2026-06-12, blind verifier agent.
"""
import numpy as np
from scipy.integrate import solve_ivp
import scipy.linalg as sla
from scipy.linalg import solve_banded, eigh_tridiagonal

S3, S5, S7 = 3**0.5, 5**0.5, 7**0.5


def Yr(u):
    u = np.asarray(u, float)
    return np.array([np.ones_like(u), S3 * u, (S5 / 2) * (3 * u * u - 1),
                     (S7 / 2) * (5 * u**3 - 3 * u)])


def Yru(u):
    u = np.asarray(u, float)
    return np.array([np.zeros_like(u), S3 * np.ones_like(u), 3 * S5 * u,
                     (S7 / 2) * (15 * u * u - 3)])


# ---------------------------------------------------------------- flow
XG2000, WG2000 = np.polynomial.legendre.leggauss(2000)
YG2000, YuG2000 = Yr(XG2000), Yru(XG2000)
SG2000 = 1 - XG2000**2


def Pgrad(X):
    fv = X @ YG2000
    fu = X @ YuG2000
    return (SG2000 * (2 * fu * YuG2000 / fv
                      - fu * fu * YG2000 / fv**2)) @ WG2000 / 8.0


def fmin_exact(X):
    """min over u in [-1,1] of the cubic f = X.Y(u); f_u is QUADRATIC:
    f_u = s3 a1 + 3 s5 g2 u + (s7/2)(15 u^2 - 3) h3  -- exact roots."""
    F, a1, g2, h3 = X
    A = 7.5 * S7 * h3
    Bq = 3 * S5 * g2
    Cq = S3 * a1 - 1.5 * S7 * h3
    cands = [-1.0, 1.0]
    if abs(A) > 1e-300:
        disc = Bq * Bq - 4 * A * Cq
        if disc >= 0:
            sq = disc**0.5
            for rt in ((-Bq + sq) / (2 * A), (-Bq - sq) / (2 * A)):
                if -1.0 <= rt <= 1.0:
                    cands.append(rt)
    elif abs(Bq) > 1e-300:
        rt = -Cq / Bq
        if -1.0 <= rt <= 1.0:
            cands.append(rt)
    uu = np.array(cands)
    return float(np.min(X @ Yr(uu)))


def flow(gamma, c, fstop=0.002, Tmax=10.0, rtol=1e-11, atol=1e-12):
    def rhs(t, z):
        X, Xt = z[:4], z[4:]
        return np.concatenate([Xt, Xt + 2 * Pgrad(X)])

    def ev(t, z):
        return fmin_exact(z[:4]) - fstop
    ev.terminal, ev.direction = True, -1
    z0 = np.array([1.0, 0, 0, 0, gamma, -c, 0, 0])
    return solve_ivp(rhs, (0, Tmax), z0, method='DOP853', rtol=rtol,
                     atol=atol, dense_output=True, events=ev)


def sealed(gamma, c, Tmax=10.0, rtol=1e-9):
    s = flow(gamma, c, rtol=rtol, atol=1e-11)
    return len(s.t_events[0]) > 0


def cstar_bisect(gamma, lo, hi, niter=30, rtol=1e-9):
    """operational seal threshold: smallest c that seals in Tmax."""
    assert not sealed(gamma, lo, rtol=rtol), "lo seals already"
    assert sealed(gamma, hi, rtol=rtol), "hi does not seal"
    for _ in range(niter):
        mid = 0.5 * (lo + hi)
        if sealed(gamma, mid, rtol=rtol):
            hi = mid
        else:
            lo = mid
    return hi


# ----------------------------------------------------------- member rays
class Member:
    """Per-ray weights p(t) = f e^{-t}, b(t) = (f_th^2/f) e^{-t} on a
    uniform t grid (own conventions; Nu Gauss rays)."""

    def __init__(self, gamma, c, Nu=24, Nt=4000, sol=None):
        self.gamma, self.c = gamma, c
        s = sol if sol is not None else flow(gamma, c)
        assert len(s.t_events[0]) > 0, "member does not seal"
        self.t_stop = float(s.t_events[0][0])
        self.tg = np.linspace(0.0, self.t_stop, Nt)
        Z = s.sol(self.tg)
        self.X = Z[:4].T
        un, wu = np.polynomial.legendre.leggauss(Nu)
        self.u, self.wu, self.Nu, self.Nt = un, wu, Nu, Nt
        Y, Yu = Yr(un), Yru(un)
        self.f = self.X @ Y                  # (Nt, Nu)
        self.fu = self.X @ Yu
        self.fth2 = (1 - un[None, :]**2) * self.fu**2
        et = np.exp(-self.tg)[:, None]
        self.p = self.f * et                 # (Nt, Nu)
        self.b = self.fth2 / self.f * et
        # tortoise x(t) per ray (for cross-reference with the x-codes):
        integ = et / self.f
        h = self.tg[1] - self.tg[0]
        cs = np.concatenate([np.zeros((1, Nu)),
                             np.cumsum(0.5 * (integ[1:] + integ[:-1]),
                                       0) * h], 0)
        self.x_of_t = cs[-1][None, :] - cs   # x(t_stop)=0, x(0)=x_max
        self.xmax = self.x_of_t[0].copy()


def kappa_c_ray(mem, k):
    """3c/(16 mu1); mu1 from P1 FEM on the t grid: A v = mu B v with
    A_ij = Int p v_i' v_j' (Dirichlet at t_stop, natural at 0),
    B = diag(b * trapz weights)."""
    h = mem.tg[1] - mem.tg[0]
    p = mem.p[:, k]
    b = mem.b[:, k]
    pm = 0.5 * (p[1:] + p[:-1])
    N = mem.Nt
    # tridiagonal stiffness
    dmain = np.zeros(N)
    dmain[:-1] += pm / h
    dmain[1:] += pm / h
    doff = -pm / h
    wts = np.full(N, h)
    wts[0] = wts[-1] = h / 2
    bw = b * wts
    # Dirichlet at the LAST node (t_stop); keep 0..N-2
    dm = dmain[:-1]
    do = doff[:-1]
    bb = bw[:-1]
    # generalized eig A v = mu B v with B diagonal PSD (b(0) = 0
    # exactly: f_u(t=0) = 0 from the weld data). Solve for the LARGEST
    # theta of B v = theta A v (A SPD, tridiagonal); mu1 = 1/theta.
    from scipy.sparse import diags
    from scipy.sparse.linalg import eigsh
    A = diags([do, dm, do], [-1, 0, 1], format='csc')
    B = diags([bb], [0], format='csc')
    theta = eigsh(B, k=1, M=A, which='LA',
                  return_eigenvectors=False)[0]
    mu = 1.0 / theta
    return 3 * mem.c / (16 * mu), mu


def equilibrium_ray(mem, k, lam, vinit=None, tol=1e-12, maxit=60):
    """Newton solve of (p v')' = lam b e^{-2v}, v(t_stop)=0,
    v'(0)=0 (one-sided). Returns v or None."""
    h = mem.tg[1] - mem.tg[0]
    p = mem.p[:, k]
    b = mem.b[:, k]
    pm = 0.5 * (p[1:] + p[:-1])
    N = mem.Nt
    v = np.zeros(N) if vinit is None else vinit.copy()
    for it in range(maxit):
        e = np.exp(-2 * v)
        F = np.zeros(N)
        F[1:-1] = (pm[1:] * (v[2:] - v[1:-1])
                   - pm[:-1] * (v[1:-1] - v[:-2])) / h**2 \
            - lam * b[1:-1] * e[1:-1]
        # Neumann at t=0 (half cell): (pm0 (v1-v0))/ (h^2/2) - lam b0 e0
        F[0] = pm[0] * (v[1] - v[0]) / (0.5 * h**2) - lam * b[0] * e[0]
        F[-1] = v[-1]
        lo = np.zeros(N)
        di = np.zeros(N)
        up = np.zeros(N)
        di[1:-1] = -(pm[1:] + pm[:-1]) / h**2 + 2 * lam * b[1:-1] * e[1:-1]
        up[1:-1] = pm[1:] / h**2
        lo[1:-1] = pm[:-1] / h**2
        di[0] = -pm[0] / (0.5 * h**2) + 2 * lam * b[0] * e[0]
        up[0] = pm[0] / (0.5 * h**2)
        di[-1] = 1.0
        lo[-1] = 0.0
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
        if not np.all(np.isfinite(v)) or v.min() < -14:
            return None
        if step * lamf < tol:
            return v
    return None


def fold_ray(mem, k, lam_lo=1e-4, rel=1e-7):
    """fold lam* of the ray: geometric ladder up + bisection."""
    v = equilibrium_ray(mem, k, lam_lo)
    assert v is not None, "no equilibrium at lam_lo"
    lam = lam_lo
    vgood, lgood = v, lam
    fac = 2.0
    # ladder: grow lam until failure
    while True:
        lam2 = lgood * fac
        v2 = equilibrium_ray(mem, k, lam2, vinit=vgood)
        if v2 is not None:
            vgood, lgood = v2, lam2
            continue
        if fac < 1.0 + 1e-8:
            break
        fac = np.sqrt(fac)
    lo, hi = lgood, lgood * fac * fac
    # bisection with warm start
    while (hi - lo) / lo > rel:
        mid = 0.5 * (lo + hi)
        v2 = equilibrium_ray(mem, k, mid, vinit=vgood)
        if v2 is None:
            hi = mid
        else:
            lo, vgood = mid, v2
    return 0.5 * (lo + hi), vgood


def member_edges(mem, rays=None, verbose=False, log=print):
    """returns dict: per-ray kappa_c, kappa_s, member maxima + rays."""
    rays = range(mem.Nu) if rays is None else rays
    kc, ks = {}, {}
    for k in rays:
        kck, mu = kappa_c_ray(mem, k)
        kc[k] = kck
        lam, _ = fold_ray(mem, k)
        ks[k] = mem.c / (16 * lam)
        if verbose:
            log(f"  ray {k:2d} u={mem.u[k]:+.4f}: kappa_c={kck:.6g} "
                f"kappa_s={ks[k]:.6g} ratio={ks[k]/kck:.5f}")
    kray_c = max(kc, key=kc.get)
    kray_s = max(ks, key=ks.get)
    return dict(kc=kc[kray_c], ks=ks[kray_s], kray_c=kray_c,
                kray_s=kray_s, kc_all=kc, ks_all=ks,
                ratio=ks[kray_s] / kc[kray_c])
