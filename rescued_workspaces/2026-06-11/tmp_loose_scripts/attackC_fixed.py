"""Attack C, corrected numerics for the pure-a- (non-Friedrichs) extension.
Shallow exact-K start (x0=-8): W-term on (-inf,x0] is e^{-21.3}W-suppressed,
so K_nu data is exact to ~1e-9 for W=O(1); dynamic-range contamination
~1e-13*64*900 ~ 6e-9. Validate at W=0 vs closed form, then root-find
Lm(W)=gamma (BC-c) and Lm(W)-gamma=D_ext (BC-a).
Cross-validate with Chebyshev minus-BC using the exact K log-derivative as
core BC at SHORT x0 (-5..-8), where the BC row retains sensitivity.
"""
import numpy as np
import mpmath as mp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.special import kv
from scipy.linalg import eig

mp.mp.dps = 30
q = 1/3; s = q*(1-q)/2
mu = np.sqrt(1+4*q*(1-q))/2
nu = 2*mu/q
GAM = 2/3

def K_data(lam, x0):
    """exact (u, u_x) of the a- branch at x0, and log-derivative."""
    tau0 = (2*np.sqrt(lam)/q)*np.exp(q*x0/2)
    K = float(mp.besselk(mp.sqrt(17), tau0))
    Kp = float(-(mp.besselk(mp.sqrt(17)-1, tau0)
                 + mp.besselk(mp.sqrt(17)+1, tau0))/2)
    pref = np.exp(-(1-2*q)*x0/2)
    u0 = pref*K
    up0 = pref*(-(1-2*q)/2*K + Kp*tau0*q/2)
    return u0, up0

def Lm(W, lam, x0=-8.0, rtol=1e-13):
    u0, up0 = K_data(lam, x0)
    def rhs(x, y):
        return [y[1], -(1-2*q)*y[1] + (lam*np.exp(q*x)+4*s
                                       + W*np.exp((2+2*q)*x))*y[0]]
    sol = solve_ivp(rhs, [x0, 0.0], [u0, up0], rtol=rtol, atol=1e-300,
                    method='DOP853')
    return sol.y[1,-1]/sol.y[0,-1], sol.y[0,-1]

# closed-form anchors
def L0m_exact(lam):
    tau0 = 2*mp.sqrt(lam)/mp.mpf(q)
    n = mp.sqrt(17)
    Kp = -(mp.besselk(n-1,tau0)+mp.besselk(n+1,tau0))/2
    return float(-(1-2*mp.mpf(q))/2 + (mp.mpf(q)*tau0/2)*Kp/mp.besselk(n,tau0))

print("W=0 validation (shooting vs closed form):")
for lam in (2.0, 6.0):
    for x0 in (-6.0, -8.0):
        v, _ = Lm(0.0, lam, x0=x0)
        print(f"  lam={lam:g} x0={x0}: {v:+.9f}   exact {L0m_exact(lam):+.9f}")

print()
print("Lm(W) scan, lam=6, corrected (x0=-8, rtol=1e-13):")
for W in (0.001, 0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0, 30.0):
    v, u0 = Lm(W, 6.0)
    print(f"  W={W:7.3f}: Lm={v:+10.5f}  u(0)={u0:+.3e}")

print()
print("BC-c roots Lm(W)=2/3 (corrected):")
roots = {}
for lam in (2.0, 6.0):
    f = lambda W: Lm(W, lam)[0] - GAM
    g = np.geomspace(1e-3, 60, 120); vv = [f(w) for w in g]; rt=[]
    for i in range(len(g)-1):
        if np.sign(vv[i]) != np.sign(vv[i+1]):
            rt.append(brentq(f, g[i], g[i+1], xtol=1e-11))
    roots[lam] = rt
    # stability: x0 variation
    rs = []
    for x0 in (-6.0, -8.0, -10.0):
        f2 = lambda W: Lm(W, lam, x0=x0)[0] - GAM
        if rt:
            rs.append(brentq(f2, 0.5*rt[0], 2*rt[0]+0.5, xtol=1e-11))
    print(f"  lam={lam:g}: roots {['%.7f' % x for x in rt]}; "
          f"x0-stability {['%.7f' % x for x in rs]}")

print()
print("BC-a root (lam=2, ell=1), corrected:")
def D_ext(w, ell):
    n_ = ell + 0.5
    kp = -0.5*(kv(n_-1, w) + kv(n_+1, w))
    return -0.5 + w*kp/kv(n_, w)
fA = lambda W: Lm(W, 2.0)[0] - GAM - D_ext(np.sqrt(W), 1)
g = np.geomspace(1e-3, 30, 80); vv=[fA(w) for w in g]; rtA=[]
for i in range(len(g)-1):
    if np.sign(vv[i]) != np.sign(vv[i+1]):
        rtA.append(brentq(fA, g[i], g[i+1], xtol=1e-11))
print(f"  roots: {['%.7f' % x for x in rtA]}")

print()
print("Chebyshev minus-BC with EXACT K core log-derivative, short x0:")
def cheb(N):
    xi = np.cos(np.pi*np.arange(N+1)/N)
    c = np.hstack([2., np.ones(N-1), 2.])*(-1)**np.arange(N+1)
    X = np.tile(xi, (N+1,1)).T
    dX = X - X.T
    D = np.outer(c, 1./c)/(dX + np.eye(N+1))
    D -= np.diag(D.sum(axis=1))
    return D, xi

def eigs_minus_exact(lam, gamma, x0, N, lo=-6, hi=10):
    D, xi = cheb(N)
    x = x0 + (xi+1)/2*(0.0-x0)
    Dx = (2.0/(0.0-x0))*D
    A = Dx@Dx - np.diag(lam*np.exp(q*x) + mu**2)
    B = np.diag(np.exp((2+2*q)*x))
    u0, up0 = K_data(lam, x0)
    m_u = up0/u0                       # u-log-derivative, exact
    mcore = m_u + (1-2*q)/2            # psi-log-derivative
    A[N,:] = Dx[N,:]; A[N,N] -= mcore; B[N,:] = 0
    A[0,:] = Dx[0,:]; A[0,0] -= (gamma + (1-2*q)/2); B[0,:] = 0
    w = eig(A, B, right=False)
    w = w[np.isfinite(w)]
    w = w[np.abs(w.imag) < 1e-7*np.maximum(1,np.abs(w.real))].real
    return np.sort(w[(w > lo) & (w < hi)])

for lam in (2.0, 6.0):
    for x0, N in ((-5.0, 140), (-6.0, 160), (-7.0, 180), (-8.0, 200)):
        ev = eigs_minus_exact(lam, GAM, x0, N)
        print(f"  lam={lam:g} x0={x0:5.1f}: {np.round(ev, 6)}")
