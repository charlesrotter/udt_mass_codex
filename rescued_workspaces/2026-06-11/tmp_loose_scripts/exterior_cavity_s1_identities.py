#!/usr/bin/env python3
"""Exterior-sourced cavity push — Script 1: exact identities.
Convention: per-solid-angle action S = int dy [(y^2/4)(F'^2+a'^2) + P(F,a)],
f = F(1+kappa cos th), a = F kappa/sqrt3 (orthonormal Y1 = sqrt3 cos th).
EL: (y^2 F')' = 2 P_F ; (y^2 a')' = 2 P_a.
"""
import sympy as sp
import mpmath as mp

mp.mp.dps = 30
PASS = FAIL = 0
def check(name, ok, detail=""):
    global PASS, FAIL
    if ok: PASS += 1; print(f"PASS  {name} {detail}")
    else:  FAIL += 1; print(f"FAIL  {name} {detail}")

# ---------- symbols ----------
F, a, y, k, q, n, s = sp.symbols('F a y kappa q n s', positive=True)
L = sp.log((1+k)/(1-k))
G1 = (2*k + (k**2-1)*L)/k**3
kap = sp.sqrt(3)*a/F
P = (3*a**2/(8*F)) * G1.subs(k, kap)

# ---------- 1. quadrature check of P (incl. F<1 universe side) ----------
def P_quad(Fv, kv):
    # per-solid-angle: (1/4pi) int dOmega (1/4)|grad_Om f|^2/f ; f = F(1+k c)
    g = lambda c: Fv*kv**2*(1-c**2)/(1+kv*c)   # |grad f|^2/f with grad^2 = F^2 k^2 sin^2
    return float(mp.quad(lambda c: 0.25*0.5*g(c), [-1, 1]))
for (Fv, kv) in [(1.0, 0.3), (2.5, 0.7), (0.4, 0.9), (0.05, 0.5)]:
    av = Fv*kv/mp.sqrt(3)
    Pcl = float(P.subs({F: Fv, a: av}))
    Pq = P_quad(Fv, kv)
    check(f"P closed form vs sphere quadrature F={Fv} k={kv}",
          abs(Pcl-Pq) < 1e-12*max(1, abs(Pq)), f"{Pcl:.15f} vs {Pq:.15f}")

# ---------- 2. H(kappa) = L/(2k) - 1 and P_F = -H/2 ----------
H_def = (k**2/4)*sp.diff(k*G1, k)
H_closed = L/(2*k) - 1
check("H = (k^2/4) d(kG1)/dk == L/(2k)-1", sp.simplify(H_def - H_closed) == 0)

PF = sp.diff(P, F)
check("P_F == -H(kappa)/2 (F-independent, deg-0)",
      sp.simplify(PF + sp.Rational(1,2)*H_closed.subs(k, kap)) == 0)

W = k**2*G1/8
Wp = sp.diff(W, k)
Wp_closed = (L*(1+k**2) - 2*k)/(8*k**2)
check("W' == [L(1+k^2)-2k]/(8k^2)", sp.simplify(Wp - Wp_closed) == 0)
Pa = sp.diff(P, a)
check("P_a == sqrt3 W'(kappa)", sp.simplify(Pa - sp.sqrt(3)*Wp_closed.subs(k, kap)) == 0)

# ---------- 3. Euler homogeneity + rank-1 Hessian + pointwise screening ----------
check("Euler: F P_F + a P_a == P", sp.simplify(F*PF + a*Pa - P) == 0)
PFF, PFa, Paa = sp.diff(P, F, 2), sp.diff(P, F, a), sp.diff(P, a, 2)
check("rank-1: P_FF P_aa - P_Fa^2 == 0", sp.simplify(PFF*Paa - PFa**2) == 0)
check("screening: P_FF - P_Fa^2/P_aa == 0 (exact pointwise)",
      sp.simplify(PFF - PFa**2/Paa) == 0)

# ---------- 4. demanded interface amplitude: H(k1) = 2s = q(1-q) ----------
# collar F0=y^-q: (y^2F0')' = -q(1-q)y^-q = 2P_F = -H  =>  H(k(y)) = q(1-q) y^-q
# closed form: L/(2k) - 1 = q(1-q) y^-q ; at y=1: L = 2k(1+q(1-q)) = 22k/9 (q=1/3)
f_dem = lambda kk: mp.log((1+kk)/(1-kk)) - mp.mpf(22)/9*kk
k1 = mp.findroot(f_dem, 0.68)
check("demanded kappa(1): L=22k/9 root == banked 0.683095",
      abs(k1 - mp.mpf('0.683095')) < 5e-7, f"k1 = {mp.nstr(k1,12)}")
# slipped variant (the caught 4pi slip): H = 2s/(4pi)
f_slip = lambda kk: mp.log((1+kk)/(1-kk))/(2*kk) - 1 - mp.mpf(2)/9/(4*mp.pi)
k1s = mp.findroot(f_slip, 0.23)
check("slipped 4pi variant reproduces 0.230329 (provenance of the slip)",
      abs(k1s - mp.mpf('0.230329')) < 5e-7, f"k1_slip = {mp.nstr(k1s,12)}")

# ---------- 5. fixed-sigma completion second jet: mu = (1-n) q(1-q) ----------
# S_src = int c_n(y) F^n dy, criticality: 2 n c_n F0^{n-1} = -q(1-q) y^-q at F0=y^-q
F0 = y**(-q)
c_n = sp.solve(sp.Eq(2*n*sp.Symbol('cn')*F0**(n-1), -q*(1-q)*y**(-q)), sp.Symbol('cn'))[0]
mu_fixed = sp.simplify(2*sp.diff(c_n*F**n, F, 2).subs(F, F0))
check("fixed-sigma jet2 mass mu == (1-n) q(1-q)  [banked invariant family]",
      sp.simplify(mu_fixed - (1-n)*q*(1-q)) == 0, f"mu = {sp.simplify(mu_fixed)}")

# ---------- 6. interface pointwise rate: d f_min/dt|_0 = gamma - sqrt3 c ----------
# f_min = F(1-kappa); data F=1,F'=-gamma,a=0,a'=-c at y=1; t=-ln y
g_, c_ = sp.symbols('gamma c', positive=True)
eps = sp.Symbol('epsilon', positive=True)  # 1-y
Fy = 1 + g_*eps     # F to first order inward
ay = c_*eps         # a to first order inward
fmin = Fy*(1 - sp.sqrt(3)*ay/Fy)
check("d f_min/d(1-y) at interface == gamma - sqrt3 c",
      sp.simplify(sp.diff(fmin, eps).subs(eps, 0) - (g_ - sp.sqrt(3)*c_)) == 0)

# ---------- 7. vacuum mode action: f=A+B/y costs B^2/(4y^2) ----------
A_, B_ = sp.symbols('A B', positive=True)
dens = (y**2/4)*sp.diff(A_+B_/y, y)**2
check("vacuum B/y action density == B^2/(4y^2) (non-integrable at 0)",
      sp.simplify(dens - B_**2/(4*y**2)) == 0)

# ---------- 8. demanded collar is OFF-SHELL in the a-channel (residual) ----------
# kappa_d(y): L/(2k)-1 = (2/9) y^(-1/3);  a_d = y^(-1/3) kappa_d /sqrt3
def kd(yv):
    rhs = mp.mpf(2)/9 * yv**(-mp.mpf(1)/3)
    return mp.findroot(lambda kk: mp.log((1+kk)/(1-kk))/(2*kk) - 1 - rhs,
                       min(0.95, mp.sqrt(3*rhs)))
def ad(yv): return yv**(-mp.mpf(1)/3)*kd(yv)/mp.sqrt(3)
def resid_a(yv):
    h = mp.mpf('1e-6')
    app = (ad(yv+h) - 2*ad(yv) + ad(yv-h))/h**2
    ap  = (ad(yv+h) - ad(yv-h))/(2*h)
    kk = kd(yv)
    Wp_v = (mp.log((1+kk)/(1-kk))*(1+kk**2) - 2*kk)/(8*kk**2)
    return yv**2*app + 2*yv*ap - 2*mp.sqrt(3)*Wp_v
r1 = resid_a(mp.mpf(1)); rhalf = resid_a(mp.mpf('0.5'))
# compare against the term size 2 sqrt3 W'
kk1 = kd(mp.mpf(1))
sz = 2*mp.sqrt(3)*(mp.log((1+kk1)/(1-kk1))*(1+kk1**2)-2*kk1)/(8*kk1**2)
check("demanded collar a-channel residual NONZERO (over-determined; collar = demand curve, not exact source-free solution)",
      abs(r1) > 1e-3*abs(sz), f"R_a(1) = {mp.nstr(r1,6)} vs term size {mp.nstr(sz,6)}; R_a(0.5)={mp.nstr(rhalf,6)}")

# ---------- 9. demanded-profile slope at interface (for flow reproduction) ----------
Hp = lambda kk: 1/(kk*(1-kk**2)) - mp.log((1+kk)/(1-kk))/(2*kk**2)
k1p = -(mp.mpf(2)/27)/Hp(k1)            # dk_d/dy at 1: H'(k) k' = -(2/9)(1/3) y^{-4/3}
a1d = k1/mp.sqrt(3)
a1pd = (-(mp.mpf(1)/3)*k1 + k1p)/mp.sqrt(3)
print(f"INFO  demanded interface jet: kappa(1)={mp.nstr(k1,10)}, a(1)={mp.nstr(a1d,10)}, "
      f"a'(1)={mp.nstr(a1pd,10)}, kappa'(1)={mp.nstr(k1p,10)}")

print(f"\nSCRIPT1 TOTALS: {PASS} PASS / {FAIL} FAIL")
