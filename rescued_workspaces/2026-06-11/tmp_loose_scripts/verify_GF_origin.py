import sympy as sp
r = sp.symbols('r', positive=True)
kappa, m, E = sp.symbols('kappa m E', real=True)
phi = sp.Function('phi')(r)
dphi = sp.Function('dphi')(r)
G = sp.Function('G')(r); F = sp.Function('F')(r)

# The script's "e2phi_source_magnitude" construction (lines 82-85):
e2_eq1_G = -2*E*sp.exp(2*phi)*F*dphi * G    # the E-piece of dR1, times G
e2_eq2_F = +2*E*sp.exp(2*phi)*G*dphi * F    # the E-piece of dR2, times F
print("eq1 piece (E-channel of dR1 * G):", sp.expand(e2_eq1_G))
print("eq2 piece (E-channel of dR2 * F):", sp.expand(e2_eq2_F))
print("SUM (conserving):", sp.simplify(e2_eq1_G + e2_eq2_F))
print("script 'magnitude' = -e2_eq1_G + e2_eq2_F:", sp.expand(-e2_eq1_G + e2_eq2_F))
print("  ... note: -(-2E e2 GF) + (2E e2 GF) = 4E e2 GF, then /2 'per equation' = 2E e2 GF")
