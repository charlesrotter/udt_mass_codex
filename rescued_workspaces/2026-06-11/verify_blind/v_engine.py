"""BLIND VERIFIER independent flow engine. Written from the banked
context only (conventions matched to the library headers so results are
comparable):
  f(u,t) = sum_{l=0}^{lmax} X_l(t) Y_l(u),  Y_l = sqrt(2l+1) P_l(u)
  P = (1/8) Int_{-1}^1 (1-u^2) f_u^2 / f du
  EL:  X_tt - X_t = 2 dP/dX_l ;  weld X=(1,0,...), X_t=(gamma,-c,0,...)
  classifier ABS: seal iff min_u f < fstop before Tmax
  classifier REL: seal iff min_u f / F < frac before Tmax
Implementation choices deliberately different from S1: generic lmax via
Legendre recurrence, numpy.polynomial for f_min (eigen-companion roots),
LSODA/DOP853 with my own tolerances, GL orders 1000 (flow) / 4000 (audit).
"""
import numpy as np
from numpy.polynomial import legendre as npleg
from scipy.integrate import solve_ivp
from scipy.optimize import brentq


def Ymat(u, lmax):
    """rows l=0..lmax of sqrt(2l+1) P_l(u) and derivative."""
    u = np.asarray(u, float)
    P = np.zeros((lmax + 1, u.size)); dP = np.zeros_like(P)
    P[0] = 1.0
    if lmax >= 1:
        P[1] = u; dP[1] = 1.0
    for l in range(1, lmax):
        P[l + 1] = ((2*l + 1)*u*P[l] - l*P[l - 1])/(l + 1)
        dP[l + 1] = dP[l - 1] + (2*l + 1)*P[l]
    nrm = np.sqrt(2*np.arange(lmax + 1) + 1.0)[:, None]
    return nrm*P, nrm*dP


class GL:
    def __init__(self, N, lmax):
        x, w = np.polynomial.legendre.leggauss(N)
        self.x, self.w = x, w
        self.Y, self.dY = Ymat(x, lmax)
        self.s = 1.0 - x**2


def gradP(X, q):
    f = X @ q.Y
    fu = X @ q.dY
    return (q.s*(2.0*fu*q.dY/f - (fu*fu)*q.Y/(f*f))) @ q.w / 8.0


def Pval(X, q):
    f = X @ q.Y; fu = X @ q.dY
    return (q.w @ (q.s*fu*fu/f))/8.0


def hessP(X, q):
    f = X @ q.Y; fu = X @ q.dY
    n = X.size
    H = np.empty((n, n))
    for i in range(n):
        for j in range(i, n):
            integ = q.s*(2*q.dY[i]*q.dY[j]/f
                         - 2*fu*(q.dY[i]*q.Y[j] + q.dY[j]*q.Y[i])/f**2
                         + 2*fu**2*q.Y[i]*q.Y[j]/f**3)
            H[i, j] = H[j, i] = (q.w @ integ)/8.0
    return H


def fmin_exact(X):
    """exact min over u in [-1,1] of the degree-(lmax) polynomial f.
    Build Legendre-series coeffs, convert to power basis, find real
    critical points via roots."""
    lmax = X.size - 1
    nrm = np.sqrt(2*np.arange(lmax + 1) + 1.0)
    c = npleg.leg2poly(X*nrm)            # power-basis coeffs of f(u)
    dc = np.polynomial.polynomial.polyder(c)
    cands = [-1.0, 1.0]
    if len(dc) > 1 and np.any(np.abs(dc[1:]) > 1e-14*max(1, abs(dc[0]))):
        r = np.polynomial.polynomial.polyroots(dc)
        cands += [float(z.real) for z in r
                  if abs(z.imag) < 1e-10 and -1 < z.real < 1]
    vals = np.polynomial.polynomial.polyval(np.array(cands), c)
    i = int(np.argmin(vals))
    return float(vals[i]), float(cands[i])


def integrate(gamma, c, lmax, fstop=0.02, Tmax=120.0, Nq=1000,
              rel=None, dense=False, rtol=1e-10, atol=1e-12):
    """rel=None: absolute classifier event at f_min=fstop.
    rel=frac: relative classifier event at f_min/F = frac."""
    q = GL(Nq, lmax)
    n = lmax + 1
    def rhs(t, z):
        X, V = z[:n], z[n:]
        g = gradP(X, q)
        return np.concatenate([V, V + 2*g])
    if rel is None:
        def ev(t, z): return fmin_exact(z[:n])[0] - fstop
    else:
        def ev(t, z): return fmin_exact(z[:n])[0]/z[0] - rel
    ev.terminal, ev.direction = True, -1
    z0 = np.zeros(2*n); z0[0] = 1.0; z0[n] = gamma; z0[n + 1] = -c
    sol = solve_ivp(rhs, (0.0, Tmax), z0, method='DOP853', rtol=rtol,
                    atol=atol, events=ev, dense_output=dense, max_step=0.1)
    return sol, len(sol.t_events[0]) > 0, q


def cstar(gamma, lmax, lo, hi, fstop=0.02, Tmax=120.0, Nq=1000, rel=None,
          xtol=1e-5):
    f = lambda c: 1.0 if integrate(gamma, c, lmax, fstop, Tmax, Nq,
                                   rel=rel)[1] else -1.0
    assert f(lo) < 0 < f(hi), "bracket"
    return brentq(f, lo, hi, xtol=xtol)
