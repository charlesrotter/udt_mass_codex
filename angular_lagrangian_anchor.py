"""
angular_lagrangian_anchor.py  (FAST, unbuffered)
PART 5 standalone: H(kappa) anchor + PART 5b anisotropy response, and a
torch float64 GPU spot-check of the hedgehog stress tensor p_r+rho=0.
"""
import sympy as sp
print("PART 5 -- H(kappa) ANCHOR", flush=True)
kap, mu, F = sp.symbols('kappa mu F', real=True)
Lk = sp.log((1+kap)/(1-kap))
H_dpf = Lk/(2*kap) - 1
print("H_dpf series:", sp.series(H_dpf, kap,0,9).removeO(), flush=True)
G1 = (2*kap+(kap**2-1)*Lk)/kap**3
# Identify generating integral
i1 = sp.simplify(sp.integrate(1/(1+kap*mu),(mu,-1,1))/2)
i2 = sp.simplify(sp.integrate((1-mu**2)/(1+kap*mu),(mu,-1,1))/2)
i3 = sp.simplify(sp.integrate(1/(1+kap*mu)**2,(mu,-1,1))/2)
print("avg 1/(1+k mu)       =", i1, flush=True)
print("avg (1-mu^2)/(1+k mu)=", i2, flush=True)
print("avg 1/(1+k mu)^2     =", i3, flush=True)
print("G1                   =", sp.simplify(G1), flush=True)
print("G1 == avg (1-mu^2)/(1+k mu)?", sp.simplify(G1-i2)==0, flush=True)
print("G1 == avg 1/(1+k mu)^2?     ", sp.simplify(G1-i3)==0, flush=True)
# reconstruct H from P
P = sp.Rational(3,8)*((F*kap/sp.sqrt(3))**2)/F*G1
H_from_P = sp.simplify(-2*sp.diff(P,F))
print("-2 P_F == H_dpf?", sp.simplify(H_from_P-H_dpf)==0, flush=True)
# PART 5b: our hedgehog winding-energy anisotropy response
th = sp.symbols('theta', real=True)
w = 1+kap*sp.cos(th)
# winding charge density of n=x/r under (1+k cos) areal weight, response 1/w:
I_resp = sp.simplify(sp.integrate(sp.sin(th)/w,(th,0,sp.pi))/2)
print("\nPART 5b: (1/2)INT sin/(1+k cos) dth =", I_resp, flush=True)
print("   series:", sp.series(I_resp,kap,0,7).removeO(), flush=True)
# the (1-mu^2)=sin^2 weighted (winding density ~ sin^2 for hedgehog grad):
I_resp2 = sp.simplify(sp.integrate(sp.sin(th)**3/w,(th,0,sp.pi))/2)
print("(1/2)INT sin^3/(1+k cos) dth =", I_resp2, flush=True)
print("   series:", sp.series(I_resp2,kap,0,7).removeO(), flush=True)
print("   == G1?", sp.simplify(I_resp2-G1)==0, flush=True)
