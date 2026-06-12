"""ATTACK C: core treatment.
(1) Independent indicial-equation check (sympy, from scratch).
(2) THE ROBUSTNESS QUESTION: admit the non-Friedrichs core branch
    u ~ rho^{a-} (the other limit-circle extension, kappa = c+/c- = 0... i.e.
    pure a- leading behavior) and ask whether omega^2 > 0 BC-c / BC-a modes
    appear at the PHYSICAL gamma = 2/3.
Method 1: Chebyshev BVP eigensolve with the a- core Robin condition.
Method 2: shooting with EXACT W=0 closed-form (K_nu) start at x0 = -12
    (the W-term there is e^{-32}-suppressed, so the W=0 closed form is the
    true solution to ~1e-14), then brentq on u'(0)/u(0) - gamma.
"""
import numpy as np
import sympy as sp
from scipy.linalg import eig
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.special import kv

# ---------- (1) indicial equation from scratch ----------
r, R, qs, ss, a = sp.symbols('r R q s a', positive=True)
f = (R/r)**qs
u = r**a
expr = sp.expand(sp.diff(r**2*f**2*sp.diff(u, r), r) - 4*r**2*f**2*(ss/r**2)*u)
lead = sp.simplify(expr / (R**(2*qs) * r**(a - 2*qs) * r**(1-1)))
print("indicial check: (r^2 f^2 u')' - 4 r^2 f^2 (s/r^2) u for u=r^a, f=(R/r)^q:")
print("   =", sp.simplify(expr/(R**(2*qs)*r**(a-2*qs))), " * R^{2q} r^{a-2q}")
poly = sp.simplify(expr/(R**(2*qs)*r**(a-2*qs)))
print("   indicial polynomial:", sp.expand(poly), "  (claim: a^2+(1-2q)a-4s)")
print("   match:", sp.simplify(poly - (a**2+(1-2*qs)*a-4*ss)) == 0)
rts = sp.solve(sp.Eq(a**2 + (1-sp.Rational(2,3))*a - sp.Rational(4,9), 0), a)
print("   q=1/3, s=1/9 roots:", rts, "=", [float(x) for x in rts])
print("   (sqrt(17)-1)/6 =", float((sp.sqrt(17)-1)/6))
# limit point/circle: weight-L2 needs a > -3/2 (int r^2 r^{2a}); both qualify
# form energy: int r^{2-2q} u'^2 ~ r^{2a-2q} needs a > q-1/2 = -1/6: only a+.
print()

# ---------- shared setup ----------
q = 1.0/3.0; s = q*(1-q)/2
mu = np.sqrt(1+4*q*(1-q))/2
nu = 2*mu/q  # sqrt(17)
am = -mu - (1-2*q)/2
ap = mu - (1-2*q)/2
GAM = 2*q

def cheb(N):
    xi = np.cos(np.pi*np.arange(N+1)/N)
    c = np.hstack([2., np.ones(N-1), 2.])*(-1)**np.arange(N+1)
    X = np.tile(xi, (N+1,1)).T
    dX = X - X.T
    D = np.outer(c, 1./c)/(dX + np.eye(N+1))
    D -= np.diag(D.sum(axis=1))
    return D, xi

def top_eig_branch(lam, gamma, x0=-25.0, N=300, branch='minus', k=3):
    D, xi = cheb(N)
    x = x0 + (xi+1)/2*(0.0-x0)
    Dx = (2.0/(0.0-x0))*D
    A = Dx@Dx - np.diag(lam*np.exp(q*x) + mu**2)
    B = np.diag(np.exp((2+2*q)*x))
    if branch == 'minus':
        c1 = lam/(q**2 - 2*mu*q)   # psi ~ e^{-mu x}(1 + c1 e^{qx})
        mcore = -mu + c1*q*np.exp(q*x0)/(1+c1*np.exp(q*x0))
    else:
        c1 = lam/(q**2 + 2*mu*q)
        mcore = mu + c1*q*np.exp(q*x0)/(1+c1*np.exp(q*x0))
    A[N,:] = Dx[N,:]; A[N,N] -= mcore; B[N,:] = 0
    A[0,:] = Dx[0,:]; A[0,0] -= (gamma + (1-2*q)/2); B[0,:] = 0
    w = eig(A, B, right=False)
    w = w[np.isfinite(w)]
    w = w[np.abs(w.imag) < 1e-6*np.maximum(1, np.abs(w.real))].real
    w = w[w < 1e6]
    return np.sort(w)[::-1][:k]

# ---------- Method 2: exact-start shooting on the a- branch ----------
def Lminus(W, lam, x0=-12.0, rtol=1e-12):
    tau0 = (2*np.sqrt(lam)/q)*np.exp(q*x0/2)
    K = kv(nu, tau0); Kp = -(kv(nu-1, tau0)+kv(nu+1, tau0))/2
    pref = np.exp(-(1-2*q)*x0/2)
    psi0 = K; dpsi0 = Kp*tau0*q/2
    u0 = pref*psi0
    up0 = pref*(-(1-2*q)/2*psi0 + dpsi0)
    def rhs(x, y):
        u, up = y
        return [up, -(1-2*q)*up + (lam*np.exp(q*x) + 4*s
                                   + W*np.exp((2+2*q)*x))*u]
    sol = solve_ivp(rhs, [x0, 0.0], [u0, up0], rtol=rtol, atol=1e-300,
                    method='DOP853')
    return sol.y[1,-1]/sol.y[0,-1]

print("ATTACK C(2): pure-a- (non-Friedrichs) extension, BC-c, gamma = 2/3")
print("  zero-energy log-derivative L0_minus(lam=2):")
print("    closed form K_nu:        -1.80622024269")
print("    shooting x0=-12:        ", f"{Lminus(0.0, 2.0):+.8f}")
print("    shooting x0=-10:        ", f"{Lminus(0.0, 2.0, x0=-10.0):+.8f}")
print()
for lam in (2.0, 6.0):
    # Chebyshev eigensolve, a- core BC
    e1 = top_eig_branch(lam, GAM, x0=-20.0, N=280)
    e2 = top_eig_branch(lam, GAM, x0=-25.0, N=340)
    # shooting root of Lminus(W) = gamma
    Ws = np.linspace(0.01, 60.0, 80)
    vals = [Lminus(w, lam) - GAM for w in Ws]
    root = None
    for i in range(len(Ws)-1):
        if np.sign(vals[i]) != np.sign(vals[i+1]):
            root = brentq(lambda w: Lminus(w, lam) - GAM, Ws[i], Ws[i+1],
                          xtol=1e-10)
            break
    print(f"  lam={lam:g}: Cheb top eigs (x0=-20): {np.round(e1,6)}")
    print(f"           Cheb top eigs (x0=-25): {np.round(e2,6)}")
    print(f"           shooting root of Lm(W)=2/3 in (0,60): "
          f"{'%.6f' % root if root is not None else 'none'}")
print()
print("  BC-a with a- core (exterior K-Bessel matching), lam=2, ell=1:")
def D_ext(w, ell):
    nu_e = ell + 0.5
    kp = -0.5*(kv(nu_e-1, w) + kv(nu_e+1, w))
    return -0.5 + w*kp/kv(nu_e, w)
def Fa_minus(W):
    return Lminus(W, 2.0) - GAM - D_ext(np.sqrt(W), 1)
Ws = np.linspace(1e-3, 30.0, 60)
va = [Fa_minus(w) for w in Ws]
roota = None
for i in range(len(Ws)-1):
    if np.sign(va[i]) != np.sign(va[i+1]):
        roota = brentq(Fa_minus, Ws[i], Ws[i+1], xtol=1e-10); break
print(f"    root of Lm(W)-2/3 = D_ext: "
      f"{'%.6f' % roota if roota is not None else 'NONE in (0,30]'};"
      f"  endpoint values F(0+)={va[0]:+.4f}, F(30)={va[-1]:+.4f}")
