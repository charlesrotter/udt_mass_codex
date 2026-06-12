"""
VERIFIER v2: spherical anchors of the flipped operator.

(1) symbolic: derive the channel-reduced EL of the FLIPPED quadratic
    functional from MY v1 jets (independent assembly) and check it is
      -(r^2 f^2 u')' + [4 r^2 f^2 E0 + lam f] u = omega^2 r^2 u,
      E0 = phi0'' + 2 phi0'/r - 2 phi0'^2     (banked weld operator)
(2) numeric: MY OWN self-adjoint FD discretization (not fem_general):
    reproduce the verifier counterexample omega^2 = +7.53 on
    phi0 = -3(r-3/2)^2, [1,2], ell=2 Dirichlet, and the vacuum control
    top omega^2 = -12.6.
"""
import numpy as np
import sympy as sp
from scipy.linalg import eigh_tridiagonal

PASS = []
def check(name, ok, detail=""):
    PASS.append((name, bool(ok)))
    print(f"V2 {name}: {'PASS' if ok else 'FAIL'} {detail}", flush=True)

# ---------- (1) symbolic EL ----------
R = sp.symbols('r', positive=True)
lam, om, cc = sp.symbols('lambda omega c', positive=True)
ph = sp.Function('phi0')(R)
u = sp.Function('u')(R)
F = sp.exp(-2*ph)
# static quadratic density per channel (from v1 E1, spherical, dp=u(R)Y,
# sphere-reduced; angular gradient of dp gives lam f u^2):
# stat2 = -(c/2)[ e^{-4phi}r^2 (dpr^2 - 8 phi' u dpr + 8 phi'^2 u^2)
#                 + lam f u^2 / r^2 * r^2 ]  ... derive exactly:
eps, dpsym = sp.symbols('eps dps')
ee = sp.exp(-2*(ph + eps*u))
dens = -(cc/2)*(ee**2*(sp.diff(ph, R) + eps*sp.diff(u, R))**2*R**2
                + ee*lam*eps**2*u**2)          # angular part: lam f u^2
stat2 = sp.diff(dens, eps, 2).subs(eps, 0)/2
# flipped time term: W = -(c/2) r^2 (d_T dp)^2 -> mode u cos(om T),
# T-avg 2x: contributes -(c/2) r^2 (-om^2) ... quadratic form
# Q[u] = -stat2 - (c/2) om^2 r^2 u^2 (sign: flipped kinetic ADDS
# -(c/2) r^2 om^2 u^2 to the action; modes where total form vanishes)
Q = sp.expand(-2/cc*stat2 - om**2*R**2*u**2)   # scaled by -2/c
EL = sp.expand(sp.diff(Q, u) - sp.diff(sp.diff(Q, sp.diff(u, R)), R))
E0 = sp.diff(ph, R, 2) + 2*sp.diff(ph, R)/R - 2*sp.diff(ph, R)**2
banked = sp.expand(2*(-sp.diff(R**2*F**2*sp.diff(u, R), R)
                      + (4*R**2*F**2*E0 + lam*F)*u - om**2*R**2*u))
check("S1 my flipped-functional EL == banked operator "
      "-(r^2 f^2 u')' + [4 r^2 f^2 E0 + lam f] u - om^2 r^2 u (x2)",
      sp.simplify(EL - banked) == 0)

# ---------- (2) my own FD eigensolver ----------
def solve_op(Pf, Qf, Rf, x0, x1, N):
    """-(P u')' + Q u = sigma R u, Dirichlet; self-adjoint FD;
    returns lowest sigmas."""
    x = np.linspace(x0, x1, N + 2)
    h = x[1] - x[0]
    xi = x[1:-1]
    Ph = Pf((x[:-1] + x[1:])/2)        # P at half nodes, len N+1
    Qd = Qf(xi); Rd = Rf(xi)
    diag = (Ph[:-1] + Ph[1:])/h**2 + Qd
    off = -Ph[1:-1]/h**2
    s = np.sqrt(Rd)
    d2 = diag/Rd
    e2 = off/(s[:-1]*s[1:])
    w = eigh_tridiagonal(d2, e2, select='i', select_range=(0, 3))[0]
    return w

ph0 = lambda r: -3.0*(r - 1.5)**2
dph = lambda r: -6.0*(r - 1.5)
F2 = lambda r: np.exp(-4*ph0(r))
E0f = lambda r: -6.0 + 2*dph(r)/r - 2*dph(r)**2
lam = 6.0
sig = solve_op(lambda r: r**2*F2(r),
               lambda r: 4*r**2*F2(r)*E0f(r) + lam*np.exp(-2*ph0(r)),
               lambda r: r**2, 1.0, 2.0, 12000)
om2 = -sig[0]
check("S2 sourced cell (E0<0): lowest sigma -> omega^2 = +7.53 banked",
      abs(om2 - 7.53) < 0.02, f"omega^2 = {om2:+.4f}")
sigv = solve_op(lambda r: r**2, lambda r: lam + 0*r, lambda r: r**2,
                1.0, 2.0, 12000)
check("S3 vacuum control: top omega^2 = -12.6 banked",
      abs(-sigv[0] + 12.6) < 0.1, f"omega^2 = {-sigv[0]:+.4f}")
# convergence sanity (doubling)
sig2 = solve_op(lambda r: r**2*F2(r),
                lambda r: 4*r**2*F2(r)*E0f(r) + lam*np.exp(-2*ph0(r)),
                lambda r: r**2, 1.0, 2.0, 24000)
check("S4 FD converged (doubling moves sigma_0 < 1e-4)",
      abs(sig2[0] - sig[0]) < 1e-4, f"delta {abs(sig2[0]-sig[0]):.1e}")

n = sum(1 for _, ok in PASS if ok)
print(f"\nV2 TOTAL: {n}/{len(PASS)} PASS")
