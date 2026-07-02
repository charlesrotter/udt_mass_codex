"""LEMMA D — the UNIVERSAL bottom-connection ODE (derived this dispatch) and its test.

Exact slow background INCLUDING x_c (CAS below):  with v = e^{-phi/2},
    v' = -kappa sqrt(1 - x_c v^2)   =>   e^{-phi/2} = (1/sqrt{x_c}) cos(kappa sqrt{x_c} r)
    (IC phi(0)=phi_c). Phase coord:  zeta = int_0^r k dr = z_c tan(tau),  tau = kappa sqrt{x_c} r,
    z_c = sqrt(|s1| x_c)/kappa = Theta_tot sqrt(x_c) (up to O(x_c)).
O(eps) u-equation on this background, dt-source only [TRUNC: drops the -(Z/4)phi'^2 source
piece, relative O(Z kappa^2/|s1|) ~ 1%], in g = (u - dt/|s1|)/(dt/|s1|):
    g_zz - [2 zeta/(zeta^2+z_c^2)] g_z + g = 0 ,   g(0) = -1, g_z(0) = 0.
ONE parameter: z_c. Large-zeta basis: u_J = sin z - z cos z, u_Y = cos z + z sin z:
    g -> alpha(z_c) u_J + beta(z_c) u_Y
=> LAUNCH FACTOR  F(z_c) = sqrt(alpha^2+beta^2),  MIXTURE PHASE  z* = atan2(-beta, alpha) mod pi.
TEST: at z_c = 0.8825 (stageB N=8) the measured mixture was (A,B) |s1|/dt = (1.379, -0.966).
"""
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

ok = lambda name, expr: print(f"  [{'PASS' if expr else 'FAIL'}] {name}")
XC = 1.0 / 1101.0

# ---------------- CAS: exact slow background with x_c, and the universal reduction
print("CAS checks:")
r, kap, xc, s1, dt, zc = sp.symbols('r kappa x_c s1 dt z_c', positive=True)
# parametrize by w = kap sqrt(xc) r in (0, pi/2) so sqrt(1-cos^2 w) = sin w unambiguously
w = sp.Symbol('w', positive=True)   # 0 < w < pi/2 on the cell
v_w = sp.cos(w)/sp.sqrt(xc)         # v = e^{-phi/2}
# v' (in r) = dv/dw * kap sqrt(xc) = -kap sin(w); and -kap sqrt(1-xc v^2) = -kap |sin w|
lhs_bg = v_w.diff(w)*kap*sp.sqrt(xc)
rhs_bg = -kap*sp.sqrt(1 - xc*v_w**2)
ok("background: e^{-phi/2}=cos(kap sqrt(xc) r)/sqrt(xc) solves v' = -kap sqrt(1-xc v^2)  (0<w<pi/2)",
   sp.simplify(lhs_bg + kap*sp.sin(w)) == 0 and
   sp.simplify(rhs_bg**2 - (kap*sp.sin(w))**2) == 0)   # square kills the |.|; sign fixed by range
# slow law: Phi = Z phi' (rho~1: O(a) TRUNC) with Phi^2 = 4 Z C^2 sqrt|s1| (e^phi - x_c),
# kappa = C |s1|^{1/4}/sqrt Z:
C_, Z_ = sp.symbols('C Z', positive=True)
phi_w = -2*sp.log(v_w)
phip_w = phi_w.diff(w)*kap*sp.sqrt(xc)      # d/dr = kap sqrt(xc) d/dw
Phi2 = ((Z_*phip_w)**2).subs(kap, C_*s1**sp.Rational(1, 4)/sp.sqrt(Z_))
ok("Phi^2 = 4 Z C^2 sqrt|s1| (e^phi - x_c) on this background (rho~1)",
   sp.simplify(sp.expand_log(sp.expand(Phi2 - 4*Z_*C_**2*sp.sqrt(s1)*(sp.exp(phi_w) - xc)), force=True)) == 0)
# universal ODE: transform u'' - 2 phi' u' + e^{2phi} s1 u = e^{2phi} dt to zeta
tau = sp.Symbol('tau')
g = sp.Function('g')(tau)
u_of_g = dt/s1*(1 + g)
phi_t = -2*sp.log(sp.cos(tau)/sp.sqrt(xc))           # phi(tau)
k2 = sp.exp(2*phi_t)*s1                              # (Z/4)phi'^2 term dropped: TRUNC O(Zk^2/s1)
lhs = ((kap*sp.sqrt(xc))**2*u_of_g.diff(tau, 2)
       - 2*(2*sp.tan(tau)*kap*sp.sqrt(xc))*(kap*sp.sqrt(xc))*u_of_g.diff(tau)
       + k2*u_of_g - sp.exp(2*phi_t)*dt)
lhs = sp.simplify(lhs/(kap**2*xc)/(dt/s1))
target = g.diff(tau, 2) - 4*sp.tan(tau)*g.diff(tau) + (s1*xc/kap**2)*sp.sec(tau)**4*g
ok("tau-form: g_tt - 4 tan(tau) g_t + z_c^2 sec^4(tau) g = 0  (z_c^2 = s1 xc/kap^2)",
   sp.simplify(lhs - target) == 0)
# zeta-form
zeta = sp.Symbol('zeta', positive=True)
G = sp.Function('g')(zeta)
# chain rule: zeta = z_c tan tau -> d/dtau = z_c sec^2 tau d/dzeta; verified:
# chain rule: g_tau = G' * zc sec^2, g_tautau = G'' (zc sec^2)^2 + G' * 2 zc sec^2 tan
tan_t = zeta/zc
sec2 = 1 + tan_t**2
expr = ((zc*sec2)**2*G.diff(zeta, 2) + (2*zc*sec2*tan_t)*G.diff(zeta)
        - 4*tan_t*(zc*sec2)*G.diff(zeta) + zc**2*sec2**2*G)
expr = sp.simplify(expr/(zc**2*sec2**2))
ok("zeta-form: g'' - [2 zeta/(zeta^2+z_c^2)] g' + g = 0",
   sp.simplify(expr - (G.diff(zeta, 2) - 2*zeta/(zeta**2 + zc**2)*G.diff(zeta) + G)) == 0)
# z_c identity: z_c = Theta sqrt(xc) with Theta = z_s sqrt(1-x_c)... report form used:
print("    z_c = sqrt(s1 x_c)/kappa;  kappa = C |s1|^{1/4}/sqrt Z;  C = sqrt(Z)|s1|^{1/4}sqrt(1-xc)/Theta")
print("    => z_c = Theta sqrt(x_c)/sqrt(1-x_c)   [family and Z cancel: z_c = z_c(Theta, x_c) ONLY]")

# ---------------- universal injection coefficients alpha(z_c), beta(z_c)
def inject(z_c, zeta_max=60.0):
    def f(z, y):
        g, gp = y
        return [gp, 2*z/(z*z + z_c*z_c)*gp - g]
    s = solve_ivp(f, (0.0, zeta_max), [-1.0, 0.0], rtol=1e-11, atol=1e-13, dense_output=True)
    z = zeta_max
    g, gp = s.y[:, -1]
    uJ, uY = np.sin(z) - z*np.cos(z), np.cos(z) + z*np.sin(z)
    uJp, uYp = z*np.sin(z), z*np.cos(z)
    W = uJ*uYp - uY*uJp           # = -z^2
    alpha = (g*uYp - gp*uY)/W
    beta = (gp*uJ - g*uJp)/W
    return alpha, beta

print("\nUniversal injection (alpha, beta), launch factor F, mixture phase z*:")
print(f"{'z_c':>8}{'alpha':>10}{'beta':>10}{'F=|.|':>10}{'z*/pi':>8}")
for z_c in (0.05, 0.2, 0.4, 0.6, 0.7, 0.8, 0.8825, 0.95, 1.1, 1.3, 1.6, 2.0):
    a, b = inject(z_c)
    F = np.hypot(a, b)
    zstar = np.mod(np.arctan2(-b, a), np.pi)
    print(f"{z_c:>8.4f}{a:>10.4f}{b:>10.4f}{F:>10.4f}{zstar/np.pi:>8.4f}")

print("\nTEST vs measured mixture on the re-shot stageB N=8 trajectory (lemD_bessel.py):")
a, b = inject(0.8825)
print(f"    predicted (alpha, beta) = ({a:.4f}, {b:.4f})   measured (A,B)|s1|/dt = (1.379, -0.966)")
print(f"    predicted F = {np.hypot(a,b):.4f}  vs measured 1.684")
print(f"    predicted seal-node phase z*/pi = {np.mod(np.arctan2(-b,a),np.pi)/np.pi:.4f}"
      f"  vs measured z_s mod pi = {1.0166/np.pi:.4f} pi ... (z_s=29.2909)")
print("    check beta -> -1 as z_c -> 0 (pure-Y core matching):", inject(0.02)[1])
