#!/usr/bin/env python3
"""Verifier's own flow library — written fresh from the verified reduction.
Galerkin in orthonormal-Legendre (du/2), Gauss-Legendre N=3000 (P1 used 2000),
dense f_min grid 8001 with endpoint recursion (P1 clipped + patched poles).
X_tt - X_t = sign * 2 P_X,  P = (1/8) Int (1-u^2) f_u^2 / f du.
Weld data: X = e0, V = (gamma, -c, 0, ...). Seal: f_min <= 0.002 (absolute).
"""
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.integrate import solve_ivp


def legY(L, u):
    """Orthonormal-(du/2) Legendre values at u (any points incl +-1)."""
    P = [np.ones_like(u), u.astype(float).copy()]
    for l in range(1, L + 1):
        P.append(((2*l + 1)*u*P[l] - l*P[l - 1])/(l + 1))
    n = np.sqrt(2*np.arange(L + 1) + 1)
    return n[:, None]*np.array(P[:L + 1])


class Ang:
    def __init__(self, L, N=3000):
        self.L = L
        u, wq = leggauss(N)
        self.u, self.wq = u, wq
        self.Y = legY(L, u)
        # derivative: (1-u^2) P_l' = l (P_{l-1} - u P_l)  (interior nodes)
        P = self.Y / np.sqrt(2*np.arange(L + 1) + 1)[:, None]
        Pp = np.zeros_like(P)
        for l in range(1, L + 1):
            Pp[l] = l*(P[l - 1] - u*P[l])/(1 - u**2)
        self.Yp = np.sqrt(2*np.arange(L + 1) + 1)[:, None]*Pp
        self.m = 1 - u**2
        self.ud = np.linspace(-1, 1, 8001)
        self.Yd = legY(L, self.ud)

    def gradP(self, X):
        f = X @ self.Y
        fu = X @ self.Yp
        a = (self.m*fu/(4*f))*self.wq
        b = (-self.m*fu**2/(8*f**2))*self.wq
        return self.Yp @ a + self.Y @ b

    def P(self, X):
        f = X @ self.Y
        fu = X @ self.Yp
        return float((self.m*fu**2/(8*f)) @ self.wq)

    def fmin(self, X):
        fd = X @ self.Yd
        i = int(np.argmin(fd))
        return fd[i], self.ud[i]


def flow(ang, gamma, c, sign, t_max=60.0, cutoff=0.002, rtol=1e-11, atol=1e-13):
    L = ang.L
    X0 = np.zeros(L + 1); X0[0] = 1.0
    V0 = np.zeros(L + 1); V0[0] = gamma
    if L >= 1:
        V0[1] = -c

    def rhs(t, s):
        X, V = s[:L + 1], s[L + 1:]
        return np.concatenate([V, V + sign*2.0*ang.gradP(X)])

    def ev(t, s):
        return ang.fmin(s[:L + 1])[0] - cutoff
    ev.terminal, ev.direction = True, -1
    sol = solve_ivp(rhs, (0.0, t_max), np.concatenate([X0, V0]), method='DOP853',
                    rtol=rtol, atol=atol, dense_output=True, events=[ev],
                    max_step=0.05)
    res = dict(sol=sol, ang=ang, sealed=len(sol.t_events[0]) > 0,
               t_stop=sol.t[-1])
    if res['sealed']:
        ts = sol.t_events[0][0]
        X = sol.sol(ts)[:L + 1]
        fmin, umin = ang.fmin(X)
        h = 1e-6
        f2 = ang.fmin(sol.sol(ts - h)[:L + 1])[0]
        slope = (fmin - f2)/h
        res['t_seal'] = ts + (fmin/(-slope) if slope < 0 else 0.0)
        res['y_seal'] = float(np.exp(-res['t_seal']))
        res['u_min'] = umin
    return res


def state(res, t):
    L = res['ang'].L
    s = res['sol'].sol(np.atleast_1d(t))
    return s[:L + 1].T, s[L + 1:].T


def bisect_cstar(ang, gamma, sign, lo, hi, tol=2e-6, t_max=60.0):
    def sealed(c):
        return flow(ang, gamma, c, sign, t_max=t_max, rtol=1e-10,
                    atol=1e-12)['sealed']
    slo, shi = sealed(lo), sealed(hi)
    if slo or not shi:
        return None, (slo, shi)
    while hi - lo > tol:
        mid = 0.5*(lo + hi)
        if sealed(mid):
            hi = mid
        else:
            lo = mid
    return 0.5*(lo + hi), (slo, shi)


# ---------------- independent discretization: finite-volume MOL ----------
def fv_classB(gamma, c, M=400, t_max=4.0, rtol=1e-9):
    """Class B PDE by finite volume in u (cell-centered), NO Galerkin.
    f_tt - f_t = +d_u[(1-u^2) f_u/f] + (1-u^2) f_u^2/(2 f^2)."""
    h = 2.0/M
    uc = -1 + (np.arange(M) + 0.5)*h           # centers
    uf = -1 + np.arange(M + 1)*h               # faces
    mf = 1 - uf**2                              # vanishes at u = +-1: zero flux
    mc = 1 - uc**2

    def rhs(t, s):
        f, ft = s[:M], s[M:]
        df = np.diff(f)/h                       # f_u at interior faces
        ff = 0.5*(f[1:] + f[:-1])               # f at interior faces
        G = np.zeros(M + 1)
        G[1:-1] = mf[1:-1]*df/ff
        divG = np.diff(G)/h
        fuc = np.gradient(f, h)                 # f_u at centers (2nd order)
        return np.concatenate([ft, ft + divG + mc*fuc**2/(2*f**2)])

    f0 = np.ones(M)
    ft0 = gamma - c*np.sqrt(3.0)*uc
    sol = solve_ivp(rhs, (0, t_max), np.concatenate([f0, ft0]), method='DOP853',
                    rtol=rtol, atol=1e-11, dense_output=True, max_step=0.02)
    def moments(t):
        f = sol.sol(t)[:M]
        F = 0.5*np.sum(f)*h
        a1 = (np.sqrt(3)/2)*np.sum(f*uc)*h
        return F, a1
    return sol, moments
