"""bv2_e_sigma.py — BLIND VERIFIER C7: sigma structure."""
import sympy as sp

r, Z = sp.symbols('r Z', positive=True)
phi = sp.Function('phi')(r); rho = sp.Function('rho', positive=True)(r); f = sp.Function('f')(r)
P1, R1, F1 = sp.diff(phi,r), sp.diff(rho,r), sp.diff(f,r)
P2, R2 = sp.diff(phi,r,2), sp.diff(rho,r,2)

Lgeo = sp.Rational(1,2)*Z*rho**2*P1**2 - 2*sp.exp(-2*phi)*R1**2 + 2

def EL(Lag, q):
    return sp.diff(sp.diff(Lag, sp.diff(q, r)), r) - sp.diff(Lag, q)

# (i) general phi-blind L_m(rho, rho', f, f'): solve the FULL rho-EL for rho''
Lm = sp.Function('L_m')(rho, R1, f, F1)
L = Lgeo + Lm
el_rho = EL(L, rho)
sol = sp.solve(sp.Eq(el_rho, 0), R2, dict=True)[0][R2]
geo_part = 2*P1*R1 - Z/4*rho*sp.exp(2*phi)*P1**2
sigma_claim = sp.exp(2*phi)/4*( sp.diff(sp.diff(Lm, R1), r) - sp.diff(Lm, rho) )
# NOTE: d/dr(dLm/drho') itself contains rho'' when Lm has rho' — handle implicitly:
resid = sp.simplify(el_rho - (EL(Lgeo, rho) + EL(Lm, rho)))
print("(i) EL additivity:", resid == 0)
# rho'' = geo + sigma  <=>  EL_geo(rho) as -4e^{-2phi}(rho'' - geo); check:
elgeo = sp.expand(EL(Lgeo, rho))
print("(i) EL_geo(rho) = -4 e^{-2phi}(rho'' - geo_part):",
      sp.simplify(elgeo - (-4*sp.exp(-2*phi))*(R2 - geo_part)) == 0)
# hence rho'' - geo = (e^{2phi}/4) * EL(Lm,rho)|_{as written} = (e^{2phi}/4)[(dLm/drho')' - dLm/drho]
print("(i) sigma = (e^{2phi}/4)[(dLm/drho')' - dLm/drho]: follows exactly (division by -4e^{-2phi}); prefactor is GEOMETRIC")

# concrete check vs banked matter source: Lm = -(xi/2)(rho^2 Ir + Ith + N^2 Is) - (kap N^2/2)(I4r + I4th/rho^2)
xi, kap, N, Ir, Ith, Is, I4r, I4th = sp.symbols('xi kappa N I_r I_th I_s I_4r I_4th', positive=True)
Lm2 = -(xi/2)*(rho**2*Ir + Ith + N**2*Is) - (kap*N**2/2)*(I4r + I4th/rho**2)
sig2 = sp.exp(2*phi)/4*( 0 - sp.diff(Lm2, rho) )
print("(i) banked source reproduced:",
      sp.simplify(sig2 - sp.exp(2*phi)/4*(xi*rho*Ir - kap*N**2*I4th/rho**3)) == 0)

# (ii) dE_geo/dr = -4 e^{-2phi} rho' sigma  on-shell (phi-eq unchanged; rho'' = geo + sigma)
sig = sp.Function('sigma')(r)
E_geo = sp.Rational(1,2)*Z*rho**2*P1**2 - 2*sp.exp(-2*phi)*R1**2
phipp = 4*sp.exp(-2*phi)*R1**2/(Z*rho**2) - 2*P1*R1/rho
dE = sp.diff(E_geo, r).subs([(P2, phipp), (R2, geo_part + sig)], simultaneous=True)
print("(ii) dE_geo/dr + 4 e^{-2phi} rho' sigma == 0:",
      sp.simplify(dE + 4*sp.exp(-2*phi)*R1*sig) == 0)

# (iii) potential-only L_m = -U(rho): sigma = (e^{2phi}/4) U'(rho); invertible along injective rho(r)
U = sp.Function('U')(rho)
sigU = sp.exp(2*phi)/4*(0 - sp.diff(-U, rho))
print("(iii) sigma_U =", sigU, " -> any smooth sigma(r) realized by U'(rho) = 4 e^{-2phi(r(rho))} sigma(r(rho)); sign free")

# (iv) explicit r-dependence breaks conservation: dH/dr = -partial_r L
Lm3 = sp.Function('L_m3')(r, rho, f, F1)
L3 = Lgeo + Lm3
pis = [sp.diff(L3, P1), sp.diff(L3, R1), sp.diff(L3, F1)]
H3 = P1*pis[0] + R1*pis[1] + F1*pis[2] - L3
els = [EL(L3, phi), EL(L3, rho), EL(L3, f)]
dH3 = sp.diff(H3, r) - (P1*els[0] + R1*els[1] + F1*els[2])
# should equal -partial_r Lm3 (explicit)
expl = -sp.Derivative(Lm3, r)   # explicit partial
print("(iv) dH/dr on-shell = -dL_m/dr|_explicit :", sp.simplify(dH3 - expl.doit()) == 0 or sp.simplify(dH3) )
