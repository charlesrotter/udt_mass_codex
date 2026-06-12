import sympy as sp
r = sp.symbols('r', positive=True)
kappa, m, E = sp.symbols('kappa m E', real=True)
phi = sp.Function('phi')(r); G=sp.Function('G')(r); F=sp.Function('F')(r); dphi=sp.Function('dphi')(r)
e2=sp.exp(2*phi)

# The two E e^{2phi} pieces in the variation:
# dR1 contains -2E e^{2phi} F dphi (from varying E e^{2phi} F term)
# dR2 contains +2E e^{2phi} G dphi (from varying -E e^{2phi} G term, sign flip)
# In diagonal contraction -(G dR1 + F dR2):
piece_from_eq1 = -G*(-2*E*e2*F*dphi)   # = +2E e^{2phi} GF dphi
piece_from_eq2 = -F*(+2*E*e2*G*dphi)   # = -2E e^{2phi} GF dphi
print("eq1 E-piece in diagonal:", sp.expand(piece_from_eq1))
print("eq2 E-piece in diagonal:", sp.expand(piece_from_eq2))
print("equal-and-opposite? sum =", sp.simplify(piece_from_eq1+piece_from_eq2))
print("magnitude of each = 2E e^{2phi} GF? ", sp.simplify(piece_from_eq1 - 2*E*e2*G*F*dphi)==0)

# Confirm CG 4.5b boxed identity m!=0 form:  2 phi'(G^2+F^2) + (2k/r)(F^2-G^2) + 4 m e^phi GF
phip=sp.diff(phi,r)
target = 2*phip*(G**2+F**2) + (2*kappa/r)*(F**2-G**2) + 4*m*sp.exp(phi)*G*F
Gp = (phip - kappa/r)*G + (m*sp.exp(phi)+E*e2)*F
Fp = (phip + kappa/r)*F + (m*sp.exp(phi)-E*e2)*G
lhs = 2*G*Gp+2*F*Fp
print("\nd/dr(G^2+F^2) == CG4.5b m!=0 boxed form?", sp.simplify(lhs-target)==0)
