import sympy as sp
r = sp.symbols('r', positive=True)
G, F, phi, dphi, m, E = sp.symbols('G F phi dphi m E', real=True)
Gp, Fp, phip, dphip = sp.symbols("G' F' phi' dphi'", real=True)
kappa = sp.symbols('kappa', real=True)
ephi  = sp.exp(phi)
e2phi = sp.exp(2*phi)

# Form-T residuals (CG §4.4):
# G' + (kappa/r - phi') G - (m e^phi + E e^2phi) F = 0
# F' + (-kappa/r - phi') F - (m e^phi - E e^2phi) G = 0
R1 = Gp + (kappa/r - phip)*G - (m*ephi + E*e2phi)*F
R2 = Fp + (-kappa/r - phip)*F - (m*ephi - E*e2phi)*G

# Vary phi -> phi + eps*dphi  (G,F,E fixed; phi' -> phi' + eps*dphi')
eps = sp.symbols('eps')
phi_v  = phi + eps*dphi
phip_v = phip + eps*dphip
def vary(expr):
    e = expr.subs({phi: phi_v, phip: phip_v}, simultaneous=True)
    return sp.diff(e, eps).subs(eps, 0)
dR1 = vary(R1)
dR2 = vary(R2)

# diagonal contraction  -(G dR1 + F dR2)
coupling = sp.expand(-(G*dR1 + F*dR2))
print("coupling -(G dR1 + F dR2) =")
sp.pprint(sp.collect(coupling, [dphip, dphi]))

# isolate coefficients
c_dphip = coupling.coeff(dphip)
c_dphi  = coupling.coeff(dphi)
print("\ncoeff of dphi'  :", sp.simplify(c_dphip))   # expect G^2+F^2
print("coeff of dphi   :", sp.simplify(c_dphi))      # expect 2 m e^phi G F (E-term cancels)
