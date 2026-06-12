"""Resolve the Method-1 vs Method-2 discrepancy for the a- extension.
(a) Scan Lminus(W) finely: distinguish genuine roots (Lm = gamma with u(0)
    away from 0) from poles (Dirichlet eigenvalues, u(0) -> 0).
(b) Stability of roots under x0 and rtol variation.
(c) Chebyshev: dump ALL finite eigenvalues in (-5, 10) for the minus BC at
    shorter x0 (where the BC row is less degenerate), N convergence.
(d) Independent variational sanity: for the a- extension the form is
    UNBOUNDED below? No -- check second eigenvalue structure instead.
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.special import kv
from scipy.linalg import eig

q = 1/3; s = q*(1-q)/2
mu = np.sqrt(1+4*q*(1-q))/2
nu = 2*mu/q
GAM = 2*q

def shoot(W, lam, x0=-12.0, rtol=1e-12):
    tau0 = (2*np.sqrt(lam)/q)*np.exp(q*x0/2)
    K = kv(nu, tau0); Kp = -(kv(nu-1, tau0)+kv(nu+1, tau0))/2
    pref = np.exp(-(1-2*q)*x0/2)
    u0 = pref*K
    up0 = pref*(-(1-2*q)/2*K + Kp*tau0*q/2)
    def rhs(x, y):
        return [y[1], -(1-2*q)*y[1] + (lam*np.exp(q*x)+4*s
                                       + W*np.exp((2+2*q)*x))*y[0]]
    sol = solve_ivp(rhs, [x0, 0.0], [u0, up0], rtol=rtol, atol=1e-300,
                    method='DOP853')
    return sol.y[0,-1], sol.y[1,-1]

for lam in (2.0, 6.0):
    print(f"--- lam = {lam:g}: fine scan of Lm(W), u(0), on (0, 8] ---")
    Ws = np.linspace(0.001, 8.0, 33)
    prev = None
    for W in Ws:
        u0, up0 = shoot(W, lam)
        L = up0/u0
        print(f"  W={W:7.3f}  u(0)={u0:+.3e}  Lm={L:+10.4f}")

print()
print("root stability (BC-c root, Lm(W)=2/3):")
for lam in (2.0, 6.0):
    for x0, rt in ((-12.0,1e-12), (-10.0,1e-12), (-14.0,1e-12), (-12.0,1e-10)):
        # bracket near previously found root
        lo, hi = (0.5, 2.0) if lam == 2.0 else (1e-4, 0.5)
        try:
            f = lambda W: shoot(W, lam, x0=x0, rtol=rt)[1]/shoot(W, lam, x0=x0, rtol=rt)[0] - GAM
            # find sign change on a fine grid in [lo,hi]
            g = np.linspace(lo, hi, 60); v=[f(w) for w in g]; root=None
            for i in range(59):
                if np.sign(v[i]) != np.sign(v[i+1]):
                    root = brentq(f, g[i], g[i+1], xtol=1e-11); break
            print(f"  lam={lam:g} x0={x0:6.1f} rtol={rt:.0e}: root = "
                  f"{'%.8f' % root if root else 'none'}")
        except Exception as e:
            print("  err", e)

print()
print("Chebyshev minus-branch, all eigenvalues in (-6, 10):")
def cheb(N):
    xi = np.cos(np.pi*np.arange(N+1)/N)
    c = np.hstack([2., np.ones(N-1), 2.])*(-1)**np.arange(N+1)
    X = np.tile(xi, (N+1,1)).T
    dX = X - X.T
    D = np.outer(c, 1./c)/(dX + np.eye(N+1))
    D -= np.diag(D.sum(axis=1))
    return D, xi

def eigs_minus(lam, gamma, x0, N):
    D, xi = cheb(N)
    x = x0 + (xi+1)/2*(0.0-x0)
    Dx = (2.0/(0.0-x0))*D
    A = Dx@Dx - np.diag(lam*np.exp(q*x) + mu**2)
    B = np.diag(np.exp((2+2*q)*x))
    c1 = lam/(q**2 - 2*mu*q)
    mcore = -mu + c1*q*np.exp(q*x0)/(1+c1*np.exp(q*x0))
    A[N,:] = Dx[N,:]; A[N,N] -= mcore; B[N,:] = 0
    A[0,:] = Dx[0,:]; A[0,0] -= (gamma + (1-2*q)/2); B[0,:] = 0
    w = eig(A, B, right=False)
    w = w[np.isfinite(w)]
    w = w[np.abs(w.imag) < 1e-8*np.maximum(1,np.abs(w.real))].real
    return np.sort(w[(w > -6) & (w < 10)])

for lam in (2.0,):
    for x0, N in ((-6.0, 160), (-8.0, 200), (-10.0, 240), (-12.0, 280)):
        print(f"  lam={lam:g} x0={x0:5.1f} N={N}: {np.round(eigs_minus(lam, GAM, x0, N), 6)}")
        # NOTE: with short x0 the a- core BC series correction is larger;
        # c1 e^{qx0} at x0=-6: |c1|*e^{-2} ~ 0.78 -- series marginal there,
        # so watch the trend, not the absolute value.
