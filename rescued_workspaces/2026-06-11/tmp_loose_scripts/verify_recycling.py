import sympy as sp

r = sp.symbols('r', positive=True)
kappa, m, E, eps = sp.symbols('kappa m E eps', real=True)
phi = sp.Function('phi')(r)
dphi = sp.Function('dphi')(r)
G = sp.Function('G')(r)
F = sp.Function('F')(r)
phip = sp.diff(phi, r)

# Form-T residuals
R1 = sp.diff(G, r) + ( kappa/r - phip)*G - (m*sp.exp(phi) + E*sp.exp(2*phi))*F
R2 = sp.diff(F, r) + (-kappa/r - phip)*F - (m*sp.exp(phi) - E*sp.exp(2*phi))*G

def vary(R):
    Rp = R.subs(phi, phi + eps*dphi).doit()
    return sp.simplify(sp.diff(Rp, eps).subs(eps, 0))

dR1 = vary(R1)
dR2 = vary(R2)
print("dR1 =", dR1)
print("dR2 =", dR2)

# Diagonal contraction
diag = sp.expand(sp.simplify(-(G*dR1 + F*dR2)))
print("\n-(G dR1 + F dR2) =", diag)
dphip = sp.diff(dphi, r)
print("coeff dphi':", sp.simplify(diag.coeff(dphip)))
print("remainder:", sp.simplify(diag - diag.coeff(dphip)*dphip))

# Off-diagonal contraction
offdiag = sp.expand(sp.simplify(F*dR1 - G*dR2))
print("\nF dR1 - G dR2 =", offdiag)

# E-channel pieces (the e^{2phi} terms only)
# In dR1 the E-channel contribution; isolate by setting m=0 and looking at E parts
dR1_E = dR1.subs(m,0)
dR2_E = dR2.subs(m,0)
print("\ndR1 (m=0):", sp.simplify(dR1_E))
print("dR2 (m=0):", sp.simplify(dR2_E))

# The claimed E-channel diagonal contraction with m=0
diag_m0 = sp.expand(sp.simplify(-(G*dR1_E + F*dR2_E)))
print("\ndiagonal (m=0) -(G dR1+F dR2):", diag_m0)
