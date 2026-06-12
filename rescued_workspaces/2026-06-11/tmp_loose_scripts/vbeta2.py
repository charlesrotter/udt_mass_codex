"""Vβ-2: envelope subtraction + WKB momentum.

U = X e^{-2 phi}, V = Y e^{-2 phi}, W = Z e^{-2 phi}.
At m=0:
  U' = X' e^{-2 phi} - 2 phi' X e^{-2 phi}
     = (2 phi' X + (2 kappa/r) Y) e^{-2 phi} - 2 phi' X e^{-2 phi}
     = (2 kappa/r) V                                              ✓
  V' = Y' e^{-2 phi} - 2 phi' Y e^{-2 phi}
     = ((2 kappa/r) X + 2 phi' Y - 4 E e^{2 phi} Z) e^{-2 phi} - 2 phi' Y e^{-2 phi}
     = (2 kappa/r) U - 4 E W
  W' = Z' e^{-2 phi} - 2 phi' Z e^{-2 phi}
     = (2 phi' Z + E e^{2 phi} Y) e^{-2 phi} - 2 phi' Z e^{-2 phi}  [at m=0; need to verify Z' at m=0]
     ...
But wait — let's check Z' at m=0.
"""
import sympy as sp
r, kappa, m, E = sp.symbols("r kappa m E", real=True)
phi = sp.Function("phi")(r)
G = sp.Function("G")(r)
F = sp.Function("F")(r)
phip = sp.diff(phi, r)

# At m=0
Gprime = (-kappa/r + phip)*G + E*sp.exp(2*phi)*F
Fprime = (+kappa/r + phip)*F - E*sp.exp(2*phi)*G

Z = G*F
Zp = Gprime*F + G*Fprime
Zp_target_canonical_m0 = 2*phip*Z + E*sp.exp(2*phi)*(F**2 - G**2)
print(f"Z' at m=0 (canonical) - target 2phi' Z + E e^{{2phi}} Y: {sp.simplify(sp.expand(Zp - Zp_target_canonical_m0))}")
# At m=0, agent's C reduces to E e^{2 phi}; agent says Z' = 2 phi' Z + C Y = 2 phi' Z + E e^{2 phi} Y. Match.

print()
print("Vβ-2: envelope subtraction at m=0")
X = G**2 + F**2
Y_expr = F**2 - G**2
U = X * sp.exp(-2*phi)
V_ = Y_expr * sp.exp(-2*phi)
W_ = Z * sp.exp(-2*phi)
Up = sp.diff(U, r)
# substitute G', F'
Up_sub = Up.subs([(sp.Derivative(G, r), Gprime), (sp.Derivative(F, r), Fprime)])
Up_sub = sp.simplify(sp.expand(Up_sub))
target_Up = (2*kappa/r) * V_
print(f"U' - (2 kappa/r) V = {sp.simplify(sp.expand(Up_sub - target_Up))}")

Vp = sp.diff(V_, r)
Vp_sub = Vp.subs([(sp.Derivative(G, r), Gprime), (sp.Derivative(F, r), Fprime)])
target_Vp = (2*kappa/r)*U - 4*E*sp.exp(2*phi)*W_   # at m=0, C = E e^{2phi}; agent's V' = (2k/r)U - 4 C W
print(f"V' - ((2 kappa/r) U - 4 E e^{{2 phi}} W) = {sp.simplify(sp.expand(Vp_sub - target_Vp))}")

Wp = sp.diff(W_, r)
Wp_sub = Wp.subs([(sp.Derivative(G, r), Gprime), (sp.Derivative(F, r), Fprime)])
target_Wp = E*sp.exp(2*phi)*V_  # at m=0, C V
print(f"W' - (E e^{{2 phi}} V) = {sp.simplify(sp.expand(Wp_sub - target_Wp))}")

# WKB momentum check.
# Matrix on (V, W) at m=0:  V' = (2k/r) U - 4 E e^{2phi} W,  W' = E e^{2phi} V
# Ignoring slow U source, M = [[0, -4 E e^{2phi}], [E e^{2phi}, 0]]
# det(lam I - M) = lam^2 + 4 E^2 e^{4 phi}. lam = +- 2i E e^{2 phi}.
# So k(r) = 2 E e^{2 phi} at m=0.  At C = E e^{2phi} (m=0), agent says k = 2C = 2 E e^{2 phi}.  PASS.
print()
print("WKB momentum at m=0: k(r) = 2 E e^{2 phi} = 2 C(r). PASS")

# Compare to canonical Form-T second-order SL momentum at m=0
# Eliminated G satisfies -(e^{-4 phi} G')' + Q_G G = E^2 G
# Asymptotic momentum p satisfies p^2 ~ E^2 e^{4 phi} - Q_G effective
# p ~ E e^{2 phi}
# So agent's k = 2 p at m=0. Factor-of-2 vs second-order SL momentum.
# This is consistent with k being the (V,W) rotation frequency on quadratic amplitudes (which is twice the underlying (G,F) rotation).
print()
print("Sanity check: second-order SL on G gives p ~ E e^{2 phi}; agent's k = 2 p.")
print("Factor-of-2 expected — V, W are quadratic in (G, F), so rotate at twice the (G,F) frequency. PASS")
