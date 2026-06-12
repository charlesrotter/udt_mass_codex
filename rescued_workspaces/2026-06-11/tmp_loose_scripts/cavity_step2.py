"""EXTERIOR-SOURCED CAVITY, step 2 (scratch):
D_+(omega,lambda) of the mirrored universe-side medium and the window map.

Exterior background (derived step 1): phi0 = (q/2)ln(r/R) for r>R,
f = (R/r)^q < 1, E0 = s/r^2, screened response n_ext in [0.993,1).
Exterior fluctuation eq (R=1 units, x = ln r > 0):
  u_xx + (1-2q) u_x = [lam e^{qx} + m + w2 e^{(2+2q)x}] u,
  m = (4-2n)s  (screened: m -> ~0+, nu -> 3).
D_+ := -u_x(0+)/u(0) of the decaying branch.
Static closed form: u = e^{-(1-2q)x/2} K_nu(tau), tau = tau0 e^{qx/2},
  D_+(0) = (1-2q)/2 - (q tau0/2) K'_nu(tau0)/K_nu(tau0).
Checks: closed form vs independent inward shooting; omega-monotonicity;
realness of the exterior branch at w2>0 (no leakage channel); the
bracket question; interior L_int(w2) monotone; total mode mismatch
M(w2) = L_int + D_+ - gamma_eff sign-definite for every shell reading.
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import kv, iv

PASS = 0; FAIL = 0
def check(label, ok):
    global PASS, FAIL
    print(f"[{'PASS' if ok else 'FAIL'}] {label}")
    if ok: PASS += 1
    else: FAIL += 1

q = 1.0/3.0; s = q*(1-q)/2

def Dplus_closed(nu, lam):
    t0 = 2*np.sqrt(lam)/q
    kp = -0.5*(kv(nu-1, t0) + kv(nu+1, t0))
    return (1-2*q)/2 - (q*t0/2)*kp/kv(nu, t0)

def Dplus_shoot(m, lam, w2, xmax=None):
    """Independent inward shooting on the exterior x>0; start at xmax
    on the decaying WKB branch; return -u_x(0+)/u(0)."""
    if xmax is None:
        xmax = 6.0 if w2 > 0 else 9.0
    def Vx(x):
        return lam*np.exp(q*x) + m + w2*np.exp((2+2*q)*x)
    # WKB start: u' / u = -(1-2q)/2 - sqrt(V + ((1-2q)/2)^2)
    g0 = -(1-2*q)/2 - np.sqrt(Vx(xmax) + ((1-2*q)/2)**2)
    def rhs(x, y):
        u, up = y
        return [up, -(1-2*q)*up + Vx(x)*u]
    sol = solve_ivp(rhs, [xmax, 0.0], [1.0, g0], rtol=1e-12, atol=1e-300)
    u, up = sol.y[0, -1], sol.y[1, -1]
    return -up/u

# ---- static D_+ : closed form vs shooting, screened (nu=3) ----
for lam in (2.0, 6.0):
    nu = 3.0; m = 0.0   # full screening; band handled below
    a = Dplus_closed(nu, lam); b = Dplus_shoot(m, lam, 0.0)
    b2 = Dplus_shoot(m, lam, 0.0, xmax=12.0)
    check(f"D_+(0,lam={lam:g}) closed form {a:.8f} = shooting {b:.8f} "
          f"(xmax-doubling stable {abs(b-b2):.1e})",
          abs(a-b) < 1e-7 and abs(b-b2) < 1e-8)

# unscreened-exterior control (n_ext=0, nu=sqrt17) for the record
for lam in (2.0,):
    nu = np.sqrt(17.0); m = 4*s
    a = Dplus_closed(nu, lam); b = Dplus_shoot(m, lam, 0.0)
    check(f"control n_ext=0: D_+(0,lam=2,nu=sqrt17) = {a:.8f} matches "
          f"shooting ({abs(a-b):.1e})", abs(a-b) < 1e-7)

D2 = Dplus_closed(3.0, 2.0); D6 = Dplus_closed(3.0, 6.0)
D2u = Dplus_closed(np.sqrt(17.0), 2.0); D6u = Dplus_closed(np.sqrt(17.0), 6.0)
print(f"   D_+(0): lam=2 screened {D2:.6f} (unscr {D2u:.6f}); "
      f"lam=6 screened {D6:.6f} (unscr {D6u:.6f})")

# ---- the bracket question 2(a) ----
check("BRACKET: D_+(0,lam=2) = %.6f sits INSIDE the banked BC bracket "
      "(no-flux 0 < D_+ < ell+1 = 2 reservoir): the medium interpolates,"
      " it does NOT supply a negative direction" % D2,
      0 < D2 < 2)
check("BRACKET lam=6: 0 < D_+ = %.6f < ell+1 = 3" % D6, 0 < D6 < 3)

# ---- omega-dependence and realness ----
w2grid = [0.0, 0.5, 1.0, 2.0, 5.0, 10.0, 25.0, 50.0]
Dv = [Dplus_shoot(0.0, 2.0, w2) for w2 in w2grid]
print("   D_+(w2,lam=2,scr):", " ".join(f"{d:.4f}" for d in Dv))
check("D_+(omega^2) is REAL and MONOTONE INCREASING on w2 in [0,50] "
      "(medium exterior has NO propagating channel at w2>0: any mode "
      "would be a genuine bound state, no leakage — and the exterior "
      "only gets MORE confining with frequency)",
      all(Dv[i] < Dv[i+1] for i in range(len(Dv)-1)) and Dv[0] > 0)

# dressing adds positive mass at w2>0 (resolved sign, step 3): exterior
# with m(w2) = m_scr + P_eff*w2/(w0^2+w2) >= m_scr -> D_+ only rises:
Dm = Dplus_shoot(0.1, 2.0, 1.0)
check("mass-monotonicity: D_+ increases with the exterior mass m "
      f"({Dplus_shoot(0.0,2.0,1.0):.6f} -> {Dm:.6f} at m: 0 -> 0.1): "
      "the repulsive dressing only worsens the exterior cost",
      Dm > Dplus_shoot(0.0, 2.0, 1.0))

# ---- interior L_int(w2), Friedrichs branch (from the banked script) ----
def aplus(qv, sv):
    return (-(1-2*qv) + np.sqrt((1-2*qv)**2 + 16*sv))/2

def L_int(m, lam, w2, x0=-50.0):
    """interior x<0: u_xx + (1-2q)u_x = [lam e^{qx} + m + w2 e^{(2+2q)x}]u
    regular branch; returns u_x(0-)/u(0).  m = (4-2n)s."""
    a = (-(1-2*q) + np.sqrt((1-2*q)**2 + 4*m))/2
    den = (a+q)**2 + (1-2*q)*(a+q) - m
    c = lam/den
    e0 = np.exp(q*x0)
    def rhs(x, y):
        u, up = y
        return [up, -(1-2*q)*up
                + (lam*np.exp(q*x) + m + w2*np.exp((2+2*q)*x))*u]
    sol = solve_ivp(rhs, [x0, 0.0], [1+c*e0, a + c*(a+q)*e0],
                    rtol=1e-12, atol=1e-300)
    return sol.y[1, -1]/sol.y[0, -1]

# cross-check vs closed forms: L_int(m=2s? no: m=(4-2n)s) ;
# n=0: m=4s -> L0 banked; n=1: m=2s?? no: m=(4-2*1)*s=2s -> D_3+q
L00 = L_int(4*s, 2.0, 0.0)
L01 = L_int(2*s, 2.0, 0.0)
check(f"interior shooting reproduces banked L0(2) = {L00:.8f} "
      "(1.33835009) at n=0 and the screened D_3+q = "
      f"{L01:.8f} (1.25841686) at n=1 — NOTE m(n=1) = 2s gives nu=3: "
      "x-form mass (4-2n)s",
      abs(L00 - 1.33835009) < 1e-6 and abs(L01 - 1.25841686) < 1e-6)

Lv = [L_int(2*s, 2.0, w2) for w2 in w2grid]
check("L_int(omega^2) monotone increasing on [0,50] (interior cost "
      "rises with frequency)", all(Lv[i] < Lv[i+1] for i in range(7)))

# ---- THE WINDOW MAP: mismatch M(w2) = L_int + D_+ - gamma_eff ----
print("\n   mode condition: L_int(w2) - gamma_eff = u'/u(0+) = -D_+(w2)")
readings = [
    ("medium ext, screened both sides, gamma_eff=0 (mirror)", 2*s, 0.0, 0.0),
    ("medium ext, UNSCREENED both sides (n=0 control), gamma_eff=0",
     4*s, 4*s, 0.0),
]
for lab, m_in, m_ex, g in readings:
    M = [L_int(m_in, 2.0, w2) + Dplus_shoot(m_ex, 2.0, w2) - g
         for w2 in w2grid]
    print(f"   {lab}: M(w2) = " + " ".join(f"{v:.4f}" for v in M))
    check(f"NO real-omega root, lam=2 [{lab}]: M(w2) >= {min(M):.4f} > 0 "
          "and increasing — window SHUT",
          min(M) > 0 and all(M[i] < M[i+1] for i in range(len(M)-1)))

# shortfall numbers (static, the closest approach)
for lam, ell in ((2.0, 1), (6.0, 2)):
    sf = L_int(2*s, lam, 0.0) + Dplus_closed(3.0, lam)
    sfu = L_int(4*s, lam, 0.0) + Dplus_closed(np.sqrt(17.0), lam)
    print(f"   lam={lam:g}: EXACT static shortfall (gamma_eff=0): "
          f"screened {sf:.6f}, unscreened control {sfu:.6f}  "
          f"[old vacuum-ext deficits: no-flux {L_int(4*s,lam,0.0)-2*q:.6f},"
          f" reservoir {L_int(4*s,lam,0.0)+ell+1-2*q:.6f}]")

# hybrid forks for honesty: medium exterior but shell retained at 2q or q
for g, lab in ((2*q, "gamma=2q (if a kink survived canon-adjudication)"),
               (q, "gamma=q (wholesale-screened kink)")):
    M0 = L_int(2*s, 2.0, 0.0) + Dplus_closed(3.0, 2.0) - g
    print(f"   hybrid fork [{lab}]: static margin needed <0, is {M0:+.6f}")
    check(f"hybrid fork [{lab}] also SHUT (margin {M0:+.4f} > 0)", M0 > 0)

print(f"\nSTEP2: {PASS} PASS / {FAIL} FAIL")
import sys; sys.exit(1 if FAIL else 0)
