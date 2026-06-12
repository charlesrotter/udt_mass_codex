import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.linalg import eigvalsh_tridiagonal
from scipy.special import kv, kvp

# ---------------- interior shooting in x = ln(r/R) ----------------
def aplus(q, s):
    return (-(1-2*q) + np.sqrt((1-2*q)**2 + 16*s))/2.0

def interior_shoot(q, s, lam, w2, x0=None, rtol=1e-12):
    """Integrate u_xx + (1-2q)u_x = [lam e^{qx} + 4s + w2 e^{(2+2q)x}] u
    from x0 (Friedrichs branch, two-term start) to x=0.
    Returns (u(0), u_x(0))."""
    if x0 is None:
        x0 = -max(40.0, 8.0/max(q, 1e-6))
    a = aplus(q, s)
    den = (a+q)**2 + (1-2*q)*(a+q) - 4*s
    c = lam/den
    e0 = np.exp(q*x0)
    u0 = 1.0 + c*e0
    up0 = a + c*(a+q)*e0
    def rhs(x, y):
        u, up = y
        return [up, -(1-2*q)*up + (lam*np.exp(q*x) + 4*s
                                   + w2*np.exp((2+2*q)*x))*u]
    sol = solve_ivp(rhs, [x0, 0.0], [u0, up0], rtol=rtol, atol=1e-14,
                    method='RK45', dense_output=False)
    return sol.y[0, -1], sol.y[1, -1]

def L0(q, s, lam):
    u, up = interior_shoot(q, s, lam, 0.0)
    return up/u

for lam in (2.0, 6.0, 12.0):
    print("lam", lam, "q=1/3 s=1/9 L0 =", L0(1/3, 1/9, lam),
          " a+ =", aplus(1/3, 1/9))

# threshold map BC-c: 2q = L0(q,lam), s=q(1-q)/2
for lam in (2.0, 6.0, 12.0):
    qs = np.linspace(0.02, 0.49, 25)
    g = [2*q - L0(q, q*(1-q)/2, lam) for q in qs]
    print("lam", lam, "max over q of 2q - L0:", max(g),
          "at q=", qs[int(np.argmax(g))])

# BC-a deficit: L0 + (l+1) - 2q  (binding iff < 0)
for lam, ell in ((2.0, 1), (6.0, 2), (12.0, 3)):
    q = 1/3
    v = L0(q, 1/9, lam) + (ell+1) - 2*q
    print("BC-a lam", lam, "deficit (must be <0 to bind):", v)
