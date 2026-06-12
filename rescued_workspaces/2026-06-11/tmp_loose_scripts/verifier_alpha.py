import sympy as sp

# ===== Independent re-derivation, VERIFIER ALPHA =====
# Canonical Form-T (CG sec 4.4):
#   R1: G' + (kappa/r - phi') G - (m e^phi + E e^{2phi}) F = 0
#   R2: F' + (-kappa/r - phi') F - (m e^phi - E e^{2phi}) G = 0
r = sp.symbols('r', positive=True)
kappa, m, E, eps = sp.symbols('kappa m E eps', real=True)
phi = sp.Function('phi')(r)
G = sp.Function('G')(r)
F = sp.Function('F')(r)
dphi = sp.Function('dphi')(r)
phip = sp.diff(phi, r)

R1 = sp.diff(G, r) + (kappa/r - phip)*G - (m*sp.exp(phi) + E*sp.exp(2*phi))*F
R2 = sp.diff(F, r) + (-kappa/r - phip)*F - (m*sp.exp(phi) - E*sp.exp(2*phi))*G

# phi -> phi + eps*dphi ; G,F,E held fixed
R1p = R1.subs(phi, phi + eps*dphi).doit()
R2p = R2.subs(phi, phi + eps*dphi).doit()
dR1 = sp.simplify(sp.diff(R1p, eps).subs(eps, 0))
dR2 = sp.simplify(sp.diff(R2p, eps).subs(eps, 0))
print("dR1 =", dR1)
print("dR2 =", dR2)

# ===== CLAIM 1: coeff of dphi' in -(G dR1 + F dR2) is exactly (G^2+F^2) =====
diag = sp.expand(-(G*dR1 + F*dR2))
dphip = sp.diff(dphi, r)
c_dphip = sp.simplify(diag.coeff(dphip))
print("\n[CLAIM 1] -(G dR1 + F dR2) =", diag)
print("[CLAIM 1] coeff of dphi' =", c_dphip, " ==(G^2+F^2)?",
      sp.simplify(c_dphip - (G**2+F**2)) == 0)

# remainder (the dphi algebraic coupling)
rem = sp.simplify(diag - c_dphip*dphip)
print("[CLAIM 1] remainder (dphi terms) =", rem)

# ===== CLAIM 2: the 2E e^{2phi} GF pieces cancel; surviving diagonal GF is mass 2m e^phi GF =====
# isolate the E-channel and m-channel contributions explicitly
# E-channel piece of dR1 contracted with G, and dR2 contracted with F:
# dR1 contains a -2E e^{2phi} F dphi e^... let's pull pieces by coeff in E and m
print("\n[CLAIM 2] full diagonal remainder coeff of dphi:", sp.simplify(rem.coeff(dphi)))
# break into E-part and m-part
rem_coeff = sp.simplify(rem.coeff(dphi))
E_part = sp.simplify(rem_coeff.coeff(E))
m_part = sp.simplify(rem_coeff - E_part*E)
print("[CLAIM 2] E-dependent part of diagonal dphi coeff:", E_part)
print("[CLAIM 2] m-dependent part of diagonal dphi coeff:", m_part)

# ===== CLAIM 4 / 4.5b: cross-coupling cancellation in d/dr(G^2+F^2) =====
# Use Form-T solved for G',F' (m!=0 full form)
Gp = (phip - kappa/r)*G + (m*sp.exp(phi) + E*sp.exp(2*phi))*F
Fp = (phip + kappa/r)*F + (m*sp.exp(phi) - E*sp.exp(2*phi))*G
ddr = sp.expand(2*G*Gp + 2*F*Fp)
print("\n[CLAIM 4/4.5b] d/dr(G^2+F^2) =", sp.simplify(ddr))
# coefficient of E (should vanish => E e^{2phi} GF cancels)
print("[CLAIM 4] coeff of E in d/dr(G^2+F^2):", sp.simplify(ddr.coeff(E)))
# coefficient of m
print("[CLAIM 4] coeff of m in d/dr(G^2+F^2):", sp.simplify(ddr.coeff(m)))
