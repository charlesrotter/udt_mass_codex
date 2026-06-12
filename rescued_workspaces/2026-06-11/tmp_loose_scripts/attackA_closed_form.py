"""ATTACK A: independent closed-form re-derivation of L0(q,lam) and the
threshold map, using mpmath modified Bessel functions (the target script
only ever SHOOTS for L0; this is an exact closed form it never uses).

Derivation (independent):
 interior mode eq at omega^2=0, rho=r/R, x=ln rho:
   u_xx + (1-2q) u_x - (lam e^{qx} + 4s) u = 0,  s=q(1-q)/2
 u = e^{-(1-2q)x/2} psi  =>  psi_xx = (lam e^{qx} + mu^2) psi,
   mu = sqrt((1-2q)^2/4 + 4s) = sqrt(1+4q(1-q))/2
 tau = (2 sqrt(lam)/q) e^{qx/2}  =>  modified Bessel, order nu = 2 mu/q.
 Friedrichs branch u ~ rho^{a+}: a+ = mu - (1-2q)/2, I_nu(tau) ~ tau^nu
   gives u ~ e^{(q nu/2 - (1-2q)/2)x} = e^{a+ x}.  OK.
 L0 = u_x/u at x=0 = -(1-2q)/2 + (q tau0/2) I_nu'(tau0)/I_nu(tau0),
   tau0 = 2 sqrt(lam)/q.
 Non-Friedrichs (pure a-) branch: K_nu(tau) ~ tau^{-nu} => u ~ e^{a- x}:
 L0_minus = -(1-2q)/2 + (q tau0/2) K_nu'(tau0)/K_nu(tau0).
"""
import mpmath as mp
mp.mp.dps = 30

q = mp.mpf(1)/3
s = q*(1-q)/2
mu = mp.sqrt(1+4*q*(1-q))/2
nu = 2*mu/q
ap = mu - (1-2*q)/2
am = -mu - (1-2*q)/2
print("q=1/3  s=", s, " nu=", nu, " (= sqrt(17):", mp.sqrt(17), ")")
print("a+ =", ap, "  a- =", am)

def L0_I(lam, q=q):
    tau0 = 2*mp.sqrt(lam)/q
    Ip = (mp.besseli(nu-1, tau0) + mp.besseli(nu+1, tau0))/2
    return -(1-2*q)/2 + (q*tau0/2) * Ip/mp.besseli(nu, tau0)

def L0_K(lam, q=q):
    tau0 = 2*mp.sqrt(lam)/q
    Kp = -(mp.besselk(nu-1, tau0) + mp.besselk(nu+1, tau0))/2
    return -(1-2*q)/2 + (q*tau0/2) * Kp/mp.besselk(nu, tau0)

print()
print("CLOSED-FORM L0 (Friedrichs) vs script claims:")
claims = {2: mp.mpf("1.33835009"), 6: mp.mpf("2.29931870"),
          12: mp.mpf("3.28396540")}
for lam in (2, 6, 12):
    v = L0_I(lam)
    print(f"  lam={lam:2d}: L0 = {mp.nstr(v, 15)}   claim {mp.nstr(claims[lam],10)}"
          f"   diff = {mp.nstr(v - claims[lam], 3)}")

print()
print("Threshold map checks (gamma_phys = 2q = 2/3):")
g = 2*q
# gamma_c BC-c = L0; BC-a = L0 + (ell+1)
for lam, ell in ((2,1),(6,2),(12,3)):
    v = L0_I(lam)
    print(f"  lam={lam:2d}: gamma_c(BC-c)={mp.nstr(v,12)}  deficit={mp.nstr(v-g,10)}"
          f"  gamma_c(BC-a)={mp.nstr(v+ell+1,12)}  deficit={mp.nstr(v+ell+1-g,10)}")

print()
# ATTACK D: lam_c where L0(lam) = 2/3
lam_c = mp.findroot(lambda la: L0_I(la) - g, mp.mpf("0.27"))
print("ATTACK D: lam_c (L0=2/3, BC-c, q=1/3) =", mp.nstr(lam_c, 12),
      "  claim 0.267787")
# monotonicity scan of L0 in lam
prev = None
mono = True
import numpy as np
for la in [1e-6, 0.01, 0.05, 0.1, 0.2677, 0.5, 1, 2, 4, 6, 9, 12, 20, 50]:
    v = L0_I(mp.mpf(la))
    if prev is not None and v <= prev: mono = False
    prev = v
print("L0 monotone increasing in lam over scan:", mono)
print("L0(lam->0) ->", mp.nstr(L0_I(mp.mpf("1e-12")), 10), " vs a+ =", mp.nstr(ap,10))

print()
# ATTACK E: high-precision L0(2) vs 4/3 and ratio vs 2
v2 = L0_I(2)
print("ATTACK E: L0(lam=2) =", mp.nstr(v2, 20))
print("  L0 - 4/3 =", mp.nstr(v2 - mp.mpf(4)/3, 10),
      " rel =", mp.nstr((v2 - mp.mpf(4)/3)/(mp.mpf(4)/3), 6))
print("  gamma_c/gamma = L0/(2/3) =", mp.nstr(v2/g, 20),
      "  minus 2 =", mp.nstr(v2/g - 2, 8))

print()
# ATTACK C support: non-Friedrichs (pure a- core) zero-energy log-derivative
for lam in (2, 6):
    print(f"  L0_minus(lam={lam}) [pure a- core, K_nu] =", mp.nstr(L0_K(lam), 12))
print("  (if L0_minus < 2/3 and the log-derivative is increasing in omega^2,")
print("   the a- extension WOULD have an omega^2>0 BC-c mode -> numeric test next)")

# exterior zero-energy form cost check (BC-a offset): integral computed exactly
import sympy as sp
rho, ell_s = sp.symbols('rho ell', positive=True)
u = rho**(-(ell_s+1))
cost = sp.integrate(rho**2*sp.diff(u,rho)**2 + ell_s*(ell_s+1)*u**2,
                    (rho,1,sp.oo), conds='none')
print()
print("BC-a exterior zero-energy cost (independent sympy):",
      sp.simplify(cost), " (claim: ell+1)")
# and the marginal-matching route: ext decaying log-deriv at omega^2->0+ is
# -(ell+1) (u~rho^{-(ell+1)}); jump matching L0 - gamma = -(ell+1) =>
# gamma_c = L0 + (ell+1). Same answer by two independent routes.
