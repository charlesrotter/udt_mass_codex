"""EXTERIOR-SOURCED CAVITY, step 2b (corrected step 2):
- screened exterior/interior x-form mass m = (4-2n)s -> 2s at n=1 (nu=3)
- exterior D_+ via Riccati g' = -(1-2q)g + V - g^2 inward (no overflow)
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import kv

PASS = 0; FAIL = 0
def check(label, ok):
    global PASS, FAIL
    print(f"[{'PASS' if ok else 'FAIL'}] {label}")
    if ok: PASS += 1
    else: FAIL += 1

q = 1.0/3.0; s = q*(1-q)/2
M_SCR = 2*s    # n=1
M_UNS = 4*s    # n=0

def nu_of_m(m):
    return np.sqrt((1-2*q)**2 + 4*m)/q

def Dplus_closed(m, lam):
    nu = nu_of_m(m)
    t0 = 2*np.sqrt(lam)/q
    kp = -0.5*(kv(nu-1, t0) + kv(nu+1, t0))
    return (1-2*q)/2 - (q*t0/2)*kp/kv(nu, t0)

def Dplus(m, lam, w2, xmax=14.0):
    """D_+ = -g(0), g = u_x/u of the decaying branch, Riccati inward."""
    def V(x):
        return lam*np.exp(q*x) + m + w2*np.exp((2+2*q)*x)
    g0 = -(1-2*q)/2 - np.sqrt(V(xmax) + ((1-2*q)/2)**2)
    def rhs(x, y):
        g = y[0]
        return [-(1-2*q)*g + V(x) - g*g]
    sol = solve_ivp(rhs, [xmax, 0.0], [g0], rtol=1e-12, atol=1e-12,
                    method='LSODA')
    return -sol.y[0, -1]

# ---- closed form vs Riccati, static ----
for lam in (2.0, 6.0):
    for m, tag in ((M_SCR, "screened n=1, nu=3"),
                   (M_UNS, "unscreened n=0, nu=sqrt17")):
        a = Dplus_closed(m, lam)
        b = Dplus(m, lam, 0.0)
        b2 = Dplus(m, lam, 0.0, xmax=20.0)
        check(f"D_+(0,lam={lam:g}) [{tag}]: closed {a:.8f} = Riccati "
              f"{b:.8f} (xmax stable {abs(b-b2):.1e})",
              abs(a-b) < 1e-6 and abs(b-b2) < 1e-7)

D2s = Dplus_closed(M_SCR, 2.0); D6s = Dplus_closed(M_SCR, 6.0)
D2u = Dplus_closed(M_UNS, 2.0); D6u = Dplus_closed(M_UNS, 6.0)
print(f"   D_+(0) screened: lam=2 {D2s:.6f}, lam=6 {D6s:.6f}; "
      f"unscreened: {D2u:.6f}, {D6u:.6f}")

# ---- bracket question ----
check(f"BRACKET lam=2: 0 < D_+ = {D2s:.6f} < ell+1 = 2 (interpolates; "
      "NO negative direction)", 0 < D2s < 2)
check(f"BRACKET lam=6: 0 < D_+ = {D6s:.6f} < ell+1 = 3", 0 < D6s < 3)

# ---- omega dependence: real + monotone ----
w2grid = [0.0, 0.25, 0.5, 1.0, 2.0, 5.0, 10.0, 25.0, 50.0]
Dv = [Dplus(M_SCR, 2.0, w2) for w2 in w2grid]
print("   D_+(w2): " + " ".join(f"{d:.4f}" for d in Dv))
check("D_+(w2) REAL, finite, MONOTONE INCREASING on [0,50] (no "
      "propagating exterior channel at w2>0: any mode would be genuinely "
      "bound — and the medium gets MORE confining with frequency)",
      all(np.isfinite(Dv)) and
      all(Dv[i] < Dv[i+1] for i in range(len(Dv)-1)) and Dv[0] > 0)
Dm = Dplus(M_SCR+0.1, 2.0, 1.0); D0 = Dplus(M_SCR, 2.0, 1.0)
check(f"repulsive dressing direction: D_+ rises with exterior mass "
      f"({D0:.6f} -> {Dm:.6f} at m += 0.1)", Dm > D0)

# ---- interior ----
def L_int(m, lam, w2, x0=-50.0):
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

L00 = L_int(M_UNS, 2.0, 0.0); L01 = L_int(M_SCR, 2.0, 0.0)
check(f"interior: L0(2,n=0) = {L00:.8f} (banked 1.33835009); "
      f"L0(2,n=1) = {L01:.8f} (= D_3+q = 1.25841686)",
      abs(L00-1.33835009) < 1e-6 and abs(L01-1.25841686) < 1e-6)
Lv = [L_int(M_SCR, 2.0, w2) for w2 in w2grid]
check("L_int(w2) monotone increasing",
      all(Lv[i] < Lv[i+1] for i in range(len(Lv)-1)))

# ---- WINDOW MAP ----
print("\n   mode condition (medium ext): L_int(w2) - gamma_eff = -D_+(w2)")
for lab, m_in, m_ex, g in (
        ("screened both sides, gamma_eff=0", M_SCR, M_SCR, 0.0),
        ("unscreened n=0 control, gamma_eff=0", M_UNS, M_UNS, 0.0)):
    M = [L_int(m_in, 2.0, w2) + Dplus(m_ex, 2.0, w2) - g for w2 in w2grid]
    print(f"   {lab}: M = " + " ".join(f"{v:.4f}" for v in M))
    check(f"NO real-omega root lam=2 [{lab}]: min M = {min(M):.4f} > 0, "
          "increasing — window SHUT",
          min(M) > 0 and all(M[i] < M[i+1] for i in range(len(M)-1)))

for lam, ell in ((2.0, 1), (6.0, 2)):
    sf = L_int(M_SCR, lam, 0.0) + Dplus_closed(M_SCR, lam)
    sfu = L_int(M_UNS, lam, 0.0) + Dplus_closed(M_UNS, lam)
    print(f"   lam={lam:g}: static shortfall (gamma_eff=0): screened "
          f"{sf:.6f}, unscreened {sfu:.6f} "
          f"[vacuum-ext deficits were: no-flux "
          f"{L_int(M_UNS,lam,0.0)-2*q:.6f}, reservoir "
          f"{L_int(M_UNS,lam,0.0)+ell+1-2*q:.6f}]")

# hybrid forks
for g, lab in ((2*q, "kink gamma=2q retained"), (q, "screened kink gamma=q")):
    M0 = L_int(M_SCR, 2.0, 0.0) + Dplus_closed(M_SCR, 2.0) - g
    check(f"hybrid fork [{lab}]: static margin {M0:+.6f} > 0 — SHUT",
          M0 > 0)

# what gamma WOULD be needed (record): gamma_need = L_int(0)+D_+(0)
gn2 = L_int(M_SCR, 2.0, 0.0) + Dplus_closed(M_SCR, 2.0)
print(f"\n   gamma needed at lam=2 (medium ext, screened): {gn2:.6f} "
      f"= {gn2/(2*q):.4f} x the banked 2q; the mirror supplies 0")

print(f"\nSTEP2b: {PASS} PASS / {FAIL} FAIL")
import sys; sys.exit(1 if FAIL else 0)
