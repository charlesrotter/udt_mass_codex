import sympy as sp

r = sp.symbols('r', real=True)
# Functions of r
G = sp.Function('G')(r)
F = sp.Function('F')(r)
phi = sp.Function('phi')(r)
m, E, kappa = sp.symbols('m E kappa', real=True)

# Form-T residuals (set to zero on-shell):
# R1 = G' + (kappa/r - phi')G - (m e^phi + E e^{2phi})F
# R2 = F' + (-kappa/r - phi')F - (m e^phi - E e^{2phi})G
ephi = sp.exp(phi)
e2phi = sp.exp(2*phi)

R1 = sp.diff(G,r) + (kappa/r - sp.diff(phi,r))*G - (m*ephi + E*e2phi)*F
R2 = sp.diff(F,r) + (-kappa/r - sp.diff(phi,r))*F - (m*ephi - E*e2phi)*G

# Now vary phi -> phi + dphi, holding G,F,E,m fixed. dphi is an independent function.
eps = sp.symbols('epsilon')
dphi = sp.Function('dphi')(r)

phi_pert = phi + eps*dphi
ephi_p = sp.exp(phi_pert)
e2phi_p = sp.exp(2*phi_pert)

R1p = sp.diff(G,r) + (kappa/r - sp.diff(phi_pert,r))*G - (m*ephi_p + E*e2phi_p)*F
R2p = sp.diff(F,r) + (-kappa/r - sp.diff(phi_pert,r))*F - (m*ephi_p - E*e2phi_p)*G

# first-order variation
dR1 = sp.diff(R1p, eps).subs(eps,0)
dR2 = sp.diff(R2p, eps).subs(eps,0)

print("dR1 =", sp.simplify(dR1))
print("dR2 =", sp.simplify(dR2))

# Diagonal contraction: -(G*dR1 + F*dR2)
expr = -(G*dR1 + F*dR2)
expr = sp.expand(expr)
print()
print("-(G*dR1 + F*dR2) =", sp.simplify(expr))

# Compare to claimed: dphi'*(G^2+F^2) + 2 m e^phi dphi G F
claimed = sp.diff(dphi,r)*(G**2+F**2) + 2*m*ephi*dphi*G*F
print()
print("claimed - actual =", sp.simplify(expr - claimed))
