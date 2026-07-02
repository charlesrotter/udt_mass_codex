"""LEMMA D — the EXACT interior solution of the O(eps) oscillation equation on the
averaged background (stronger than WKB; derived this dispatch).

Averaged slow background (S5, x_c-term dropped: valid e^phi >> x_c):
    Phi^2 = 4 Z C^2 sqrt|s1| e^phi  =>  phi' = (2 C |s1|^{1/4}/sqrt Z) e^{phi/2}
    =>  e^{-phi/2} = kappa (r_v - r),  kappa = C |s1|^{1/4}/sqrt(Z)     [EXACT solution]
    =>  phi' = 2/s, phi'' = 2/s^2  (s = r_v - r),  k = e^phi sqrt|s1| = lam/s^2,
        lam = sqrt|s1|/kappa^2.
w-equation (S2, exact): w'' + (k^2 + phi'' - phi'^2) w = e^{phi}[dt - (Z/4)phi'^2]:
    w_ss + (lam^2/s^4 - 2/s^2) w = dt/(kappa^2 s^2) - Z/(kappa^2 s^4)
CLAIMS (CAS-verified below):
  B1  homogeneous solutions  w = sqrt(s) J_{±3/2}(lam/s); in u = e^phi w variables,
      with z = lam/s = (sqrt|s1|/kappa) e^{phi/2}:
        u_J = sin z - z cos z          (-> z^3/3, core side)
        u_Y = cos z + z sin z          (-> 1,     core side)
      and  du_J/dz = z sin z,  du_Y/dz = z cos z   (elementary!)
  B2  exact particular solution: u_p = dt/|s1| - (Z/|s1|)/s^2 - 2 Z kappa^4 s^2 *(e^phi)/|s1|^2...
      verified in w-form:  w_p = (dt kappa^2/|s1|) s^2 - (Z kappa^2/|s1|)(1 + 2 kappa^4 s^2/|s1|)
      NOTE (Z/|s1|)/s^2 = (Z/4)phi'^2/|s1| -- the adiabatic offset, EXACT here up to the
      constant -2 Z kappa^6 s^2 e^{phi}... term (small, O(kappa^4/|s1|)).
  B3  fit-free trajectory test: match (A, B) at ONE interior point (the 2 legitimate
      integration constants), predict the ENTIRE oscillation zone; report mismatch.
  B4  the seal-phase structure: u_h'(z) = z(A sin z + B cos z) => nodes of rho' spaced
      EXACTLY pi in z; theta_0 = mixture angle arctan structure (bottom-region input).
Budget: 1 IVP shot.
"""
import sys
import numpy as np
import sympy as sp
sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
from cell_solver_universe_T3 import rhs, PHI_C, make_risefall_slice
from scipy.integrate import solve_ivp

ok = lambda name, expr: print(f"  [{'PASS' if expr else 'FAIL'}] {name}")
XC = 1.0 / 1101.0

# ---------------------------------------------------------------- CAS: B1, B2
print("B1/B2 CAS:")
s, lam, kap, Z_, dt_, s1_ = sp.symbols('s lambda kappa Z dt s1', positive=True)
z = lam / s
for name, uz in (("u_J = sin z - z cos z", sp.sin(z) - z*sp.cos(z)),
                 ("u_Y = cos z + z sin z", sp.cos(z) + z*sp.sin(z))):
    w = s**2 * kap**2 * uz / lam**0  # u = e^phi w, e^phi = 1/(kap^2 s^2) => w = kap^2 s^2 u
    w = s**2 * uz                    # overall const irrelevant (linear, homogeneous)
    resid = sp.simplify(w.diff(s, 2) + (lam**2/s**4 - 2/s**2)*w)
    ok(f"homogeneous: {name}", resid == 0)
zz = sp.Symbol('z', positive=True)
ok("du_J/dz = z sin z", sp.simplify(sp.diff(sp.sin(zz) - zz*sp.cos(zz), zz) - zz*sp.sin(zz)) == 0)
ok("du_Y/dz = z cos z", sp.simplify(sp.diff(sp.cos(zz) + zz*sp.sin(zz), zz) - zz*sp.cos(zz)) == 0)
# particular: lam^2 = s1/kap^4
lam2 = s1_ / kap**4
wp = (dt_*kap**2/s1_)*s**2 - (Z_*kap**2/s1_)*(1 + 2*kap**4*s**2/s1_)
resid_p = sp.simplify(wp.diff(s, 2) + (lam2/s**4 - 2/s**2)*wp
                      - (dt_/(kap**2*s**2) - Z_/(kap**2*s**4)))
ok("particular w_p (exact)", resid_p == 0)
up_expr = sp.simplify(wp / (kap**2 * s**2))   # u_p = e^phi w_p
print("    u_p =", sp.expand(up_expr), "  [= dt/|s1| - (Z/4)phi'^2/|s1| - 2 Z kap^4/s1^2 ... exact]")

# ---------------------------------------------------------------- B3: trajectory test (1 shot)
print("\nB3: fit-free overlay on stageB N=8 (Z=8, A1 m=3, a*=1.4941240) — 1 shot")
Z, m, a_param, N = 8.0, 3.0, 1.4941240, 8
U, Up, lab = make_risefall_slice(a_param, m=m)
seal = lambda r, y, *a: y[0]; seal.terminal, seal.direction = True, +1
sol = solve_ivp(rhs, (0.0, 5e7), [PHI_C, 0.0, 1.0, 0.0], args=(Z, Up), method="LSODA",
                rtol=1e-10, atol=1e-12, events=[seal], dense_output=True)
r_s = sol.t_events[0][0]
rr = np.linspace(0.0, r_s, 400001)
phi, phip, rho, rhop = sol.sol(rr)
h = 1e-6
dt = Up(1.0)/4.0
s1 = -(Up(1.0+h) - Up(1.0-h))/(2*h)/4.0
Q = 0.25*Z*phip**2 + s1
k = np.exp(phi)*np.sqrt(Q)
Theta = np.trapezoid(k, rr)
C = np.sqrt(Z)*s1**0.25*np.sqrt(1-XC)/Theta      # S6 (verified = flux/envelope C to ~1%)
kappa = C*s1**0.25/np.sqrt(Z)
zg = np.sqrt(s1)/kappa*np.exp(phi/2.0)           # Bessel argument along the trajectory
up_off = (dt - 0.25*Z*phip**2)/Q                 # adiabatic offset (B2, exact on background)
osc = rho - 1.0 - up_off
uJ = np.sin(zg) - zg*np.cos(zg)
uY = np.cos(zg) + zg*np.sin(zg)
# match A,B at one interior point: z ~ 0.55 z_s (mid oscillation zone), using value + slope
i0 = np.argmin(np.abs(zg - 0.55*zg[-1]))
i1 = i0 + 400                                     # second nearby point for the 2x2 solve
Mm = np.array([[uJ[i0], uY[i0]], [uJ[i1], uY[i1]]])
A, B = np.linalg.solve(Mm, [osc[i0], osc[i1]])
pred = A*uJ + B*uY
zone = zg > 3.0                                   # oscillation zone (past onset)
err = pred[zone] - osc[zone]
amp = np.max(np.abs(osc[zone]))
print(f"    matched at z={zg[i0]:.2f}, z_s={zg[-1]:.3f} (Theta={Theta:.3f});  A={A:.5e}  B={B:.5e}")
print(f"    mixture angle: atan2(B,A) = {np.degrees(np.arctan2(B, A)):.2f} deg;"
      f"  amp = sqrt(A^2+B^2) = {np.hypot(A, B):.5e}  vs dt/|s1| = {dt/s1:.5e}"
      f"  (pure-Y bottom matching would give B=-dt/|s1|={-dt/s1:.3e}, A=0)")
print(f"    OVERLAY (z>3): rms(pred-osc)/max|osc| = {np.sqrt(np.mean(err**2))/amp:.4f}"
      f"   max|pred-osc|/max|osc| = {np.max(np.abs(err))/amp:.4f}")
# core-side limit of the matched solution vs -dt/|s1| (what pure-Y matching assumes)
print(f"    core-side limit A*0 + B*1 = B = {B:.4e}  vs  -dt/|s1| = {-dt/s1:.4e}"
      f"   (ratio {B/(-dt/s1):.3f}) -> bottom region injects a NON-pure-Y mixture: the underived piece")
# seal phase structure: last few rho'-nodes spacing in z (B4: exactly pi apart)
sgn = np.sign(rhop[1:-1]); flips = np.where(sgn[1:]*sgn[:-1] < 0)[0]
zn = zg[1:-1][flips]
print(f"    B4 rho'-node spacings in z (should -> pi): {np.diff(zn)[-6:]}")
print(f"    seal lands at z_s = {zg[-1]:.4f};  z_s mod pi = {np.mod(zg[-1], np.pi):.4f}"
      f"  (node phase: tan z_s = -B/A -> z* = {np.mod(np.arctan2(-B, A), np.pi):.4f})")
