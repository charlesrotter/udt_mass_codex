"""BLIND VERIFIER — N2 claim A4: kernel anchors with MY OWN solver +
MY OWN time integrator; plus the linearized-a* = banked-weld identity.

Collar background (structural, banked): r <= 1, f = r^{-q}, q = 1/3,
E0 = s/r^2, s = 1/9. Operator (relaxation reading):
   (r^2 f^2 u')' - [lam f + 4 r^2 f^2 E0] u = omega^2 r^2 u
x = ln r:  u_xx + b u_x - (lam e^{qx} + 4 s) u = omega^2 e^{(2+2q)x} u,
b = 1 - 2q. Core: Friedrichs branch u ~ e^{a+ x}, a+ = (sqrt17-1)/6.
Outer Robin at x=0: u_x(0) = gamma u(0).
Anchors: gamma = 2/3 -> omega^2 = -3.4667814; gamma = 1.5 L0(2)
-> omega^2 = +4.0701100, L0(2) = 1.33835009.
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
import sympy as sp

PASS, FAIL = [], []
def check(label, ok):
    (PASS if ok else FAIL).append(label)
    print(("PASS" if ok else "FAIL"), label, flush=True)

QB = 1.0/3.0
SB = 1.0/9.0
BX = 1.0 - 2*QB
AP = (np.sqrt(17.0) - 1.0)/6.0

# indicial check (my own): u ~ e^{ax}: a^2 + b a - 4s = 0
a_ind = (-BX + np.sqrt(BX**2 + 16*SB))/2
check("A4-0 indicial root a+ == (sqrt(17)-1)/6", abs(a_ind - AP) < 1e-14)

# ---- my own shooting eigensolver (different x0, tolerances) ----
def logderiv_at0(w2, lam, gamma, x0=-35.0):
    def rhs(x, y):
        u, up = y
        return [up, -BX*up + (lam*np.exp(QB*x) + 4*SB
                              + w2*np.exp((2 + 2*QB)*x))*u]
    # w2 < 0 convention: omega^2 enters with MINUS? strong form:
    # u_xx + b u_x - (V)u = w2 e^{..}u  ->  u_xx = -b u_x + V u + w2 e u
    sol = solve_ivp(rhs, (x0, 0.0), [1.0, a_ind], rtol=3e-12, atol=1e-280,
                    max_step=0.02)
    return sol.y[1, -1]/sol.y[0, -1] - gamma

def rhs_make(w2, lam):
    def rhs(x, y):
        u, up = y
        return [up, -BX*up + (lam*np.exp(QB*x) + 4*SB
                              - w2*np.exp((2 + 2*QB)*x))*u]
    return rhs

# careful with sign: (r^2f^2u')' - [..]u = omega^2 r^2 u
# x-form: d_x(e^{bx}u_x) - e^x V u = omega^2 e^{3x} u  with e^x V =
# e^{(1-b)x}... => u_xx + b u_x - (lam e^{qx}+4s) u - omega^2
# e^{(2+2q)x} u = 0   i.e. u_xx = -b u_x + (V + omega^2 e^{(2+2q)x}) u
def shoot(w2, lam, gamma, x0=-35.0):
    sol = solve_ivp(rhs_make(-w2, lam), (x0, 0.0), [1.0, a_ind],
                    rtol=3e-12, atol=1e-280, max_step=0.02)
    return sol.y[1, -1]/sol.y[0, -1] - gamma

def rhs2(w2, lam):
    def rhs(x, y):
        u, up = y
        return [up, -BX*up + (lam*np.exp(QB*x) + 4*SB
                              + w2*np.exp((2 + 2*QB)*x))*u]
    return rhs

def shoot2(w2, lam, gamma, x0=-35.0):
    sol = solve_ivp(rhs2(w2, lam), (x0, 0.0), [1.0, a_ind],
                    rtol=3e-12, atol=1e-280, max_step=0.02)
    return sol.y[1, -1]/sol.y[0, -1] - gamma

L0 = shoot2(0.0, 2.0, 0.0) + 0.0   # log-derivative at omega^2 = 0
print(f"    L0(lam=2) = {L0:.8f}  (banked 1.33835009)")
check("A4-1 L0(2) == 1.33835009 (my shooting)", abs(L0 - 1.33835009) < 1e-6)
L06 = shoot2(0.0, 6.0, 0.0)
print(f"    L0(lam=6) = {L06:.8f}  (banked 2.29931870)")
check("A4-1b L0(6) == 2.29931870", abs(L06 - 2.29931870) < 1e-6)

w_rel = brentq(lambda w: shoot2(w, 2.0, 2*QB), -3.6, -3.3, xtol=1e-10)
print(f"    omega^2 (lam=2, gamma=2/3) = {w_rel:.7f}  (banked -3.4667814)")
check("A4-2 banked relaxation anchor -3.4667814 (my shooting)",
      abs(w_rel + 3.4667814) < 2e-5)
gboost = 1.5*L0
w_b = brentq(lambda w: shoot2(w, 2.0, gboost), 3.5, 4.5, xtol=1e-10)
print(f"    omega^2 (lam=2, gamma=1.5 L0) = {w_b:.7f}  (banked +4.0701100)")
check("A4-3 boosted anchor +4.0701100 (my shooting)",
      abs(w_b - 4.0701100) < 2e-5)

# ---- MY OWN FD assembly + MY OWN backward-Euler relaxation flow ----
def assemble_mine(lam, gamma, x0=-14.0, n=4000):
    """flux FD of d_x(e^{bx}u_x) - e^x V(x) u with weight e^{3x};
    Robin closures: left flux = e^{b x0} Lcore u, right flux = gamma u."""
    x = np.linspace(x0, 0.0, n)
    h = x[1] - x[0]
    xm = 0.5*(x[:-1] + x[1:])
    k = np.exp(BX*xm)/h
    V = lam*np.exp(QB*x) + 4*SB     # e^x V with e^x absorbed: e^{x}*(lam e^{-qx}+4s e^{-2qx}) = lam e^{(1-q)x}+4s e^{(1-2q)x}
    pot = lam*np.exp((1 - QB)*x) + 4*SB*np.exp((1 - 2*QB)*x)
    diag = -pot*h
    diag[0] = -pot[0]*h/2
    diag[-1] = -pot[-1]*h/2
    diag[1:-1] -= (k[:-1] + k[1:])
    diag[0] -= k[0]
    diag[-1] -= k[-1]
    # core log-derivative from my shooting of the zero-energy solution
    def core_ld():
        sol = solve_ivp(rhs2(0.0, lam), (-40.0, x0), [1.0, a_ind],
                        rtol=1e-12, atol=1e-280, max_step=0.05)
        return sol.y[1, -1]/sol.y[0, -1]
    diag[0] += np.exp(BX*x0)*core_ld()
    diag[-1] += gamma
    wgt = np.exp(3*x)*h
    wgt[0] *= 0.5; wgt[-1] *= 0.5
    return diag, k, wgt

def top_eig_mine(lam, gamma, x0=-14.0, n=4000):
    from scipy.linalg import eigh_tridiagonal
    diag, k, wgt = assemble_mine(lam, gamma, x0, n)
    s = 1.0/np.sqrt(wgt)
    d2 = diag*s*s
    e2 = k*s[:-1]*s[1:]
    vals = eigh_tridiagonal(d2, e2, select='v',
                            select_range=(-60.0, 50.0))[0]
    return np.sort(vals)[::-1]

ev = top_eig_mine(2.0, 2*QB)
evb = top_eig_mine(2.0, gboost)
print(f"    my-FD top omega^2: relax {ev[0]:.6f}, boosted {evb[0]:.6f}")
check("A4-4 my own FD spectrum reproduces both anchors (3+ digits)",
      abs(ev[0] + 3.4667814) < 5e-3 and abs(evb[0] - 4.0701100) < 5e-3)

def relax_mine(lam, gamma, T_end=8.0, dt=2e-4, x0=-12.0, n=2500, seed=42):
    """MY integrator: pure backward Euler (theta=1) on W u_T = L u."""
    from scipy.linalg import solveh_banded
    diag, k, wgt = assemble_mine(lam, gamma, x0, n)
    ab = np.zeros((2, n))
    ab[1] = wgt - dt*diag
    ab[0, 1:] = -dt*k
    rng = np.random.default_rng(seed)
    u = rng.normal(size=n)
    nst = int(T_end/dt)
    logn = np.zeros(nst)
    acc = 0.0
    for i in range(nst):
        rhs = wgt*u
        u = solveh_banded(ab, rhs)
        nr = np.sqrt(np.sum(wgt*u*u))
        acc += np.log(nr)
        logn[i] = acc
        u /= nr
    tg = dt*np.arange(1, nst + 1)
    i0 = int(0.7*nst)
    return np.polyfit(tg[i0:], logn[i0:], 1)[0]

r1 = relax_mine(2.0, 2*QB)
r2 = relax_mine(2.0, gboost)
print(f"    my backward-Euler relaxation rates: {r1:.5f} (target "
      f"-3.46678), {r2:.5f} (target +4.07011)")
# backward Euler rate bias ~ +0.5*lambda^2*dt
check("A4-5 MY integrator: generic-data late-time relaxation rate == "
      "banked -3.4668 within integrator bias (~lam^2 dt/2 ~ 1e-3)",
      abs(r1 + 3.4667814) < 5e-3)
check("A4-6 MY integrator: boosted rate == +4.0701 within bias",
      abs(r2 - 4.0701100) < 5e-3)

# ---- Hadamard demo with my own power iteration --------------------
def mesh_rate(n, x0=-4.0, lam=2.0, gamma=2*QB):
    diag, k, wgt = assemble_mine(lam, gamma, x0, n)
    def Au(v):
        out = diag*v
        out[:-1] += k*v[1:]
        out[1:] += k*v[:-1]
        return out/wgt
    v = np.random.default_rng(1).normal(size=n)
    for _ in range(300):
        v = Au(v); v /= np.linalg.norm(v)
    lam_ex = v @ Au(v)
    return np.sqrt(abs(lam_ex))

m1, m2 = mesh_rate(300), mesh_rate(600)
print(f"    second-order T-march mesh rates: n=300 {m1:.3e}, n=600 "
      f"{m2:.3e} (ratio {m2/m1:.2f}; physical ~1.86)")
check("A4-7 Hadamard: T-march growth rate is mesh-divergent (rate >> "
      "physical, ~doubles with mesh)", m1 > 50*1.86 and 1.5 < m2/m1 < 2.5)

# ---- linearized a* == banked algebraic weld ------------------------
f0, f0p, dfT, eps = sp.symbols('f0 f0p dfT epsilon', positive=True)
a_star = 2*f0*(eps*dfT)*f0p/(f0**2*f0p**2 - (eps*dfT)**2)
a_lin = sp.series(a_star, eps, 0, 2).removeO().coeff(eps, 1)
check("A4-8 linearized a* == 2 dfT/(f0 f0') == -4 d_T(dphi)/f0' "
      "(banked algebraic weld H1)",
      sp.simplify(a_lin - 2*dfT/(f0*f0p)) == 0)

print()
print("PASS", len(PASS), "FAIL", len(FAIL))
if FAIL:
    print("FAILED:", FAIL)
