"""Vβ-5a: m != 0 extension — does the agent's IBP bound carry over?

CG §4.7 line 525 explicitly states the canonical X' at m != 0:
  X' = 2 phi' X + (2 kappa/r) Y + 4 m e^phi Z

Therefore at m != 0, U' is NOT simply (2 kappa/r) V.  Re-derive:
  U' = X' e^{-2 phi} - 2 phi' X e^{-2 phi}
     = (2 kappa/r) V + 4 m e^phi W

So at m != 0, U has TWO oscillatory drivers (V and W), not just V.
The agent's IBP bound:
  d/dr log U = (2 kappa/r) cos Theta (at m=0)
is replaced at m != 0 by:
  d/dr log U = (2 kappa/r) V/U + 4 m e^phi W/U
             = g(r) cos Theta + (4 m e^phi)/(2)(R/U) sin Theta   [using V=R cos, W=(R/2) sin]
             = g(r) cos Theta + h(r) sin Theta   with h(r) = 2 m e^phi (R/U)
"""
print("At m != 0 the agent's transport DOES extend, but with an ADDITIONAL")
print("oscillatory driver:")
print("  d/dr log U = g(r) cos Theta + h(r) sin Theta")
print("  g(r) = 2 kappa/r,  h(r) = 2 m e^phi")
print()
print("(using R = U slow envelope per ansatz, V = U cos Theta, W = (U/2) sin Theta)")
print()
print("IBP on h(r) sin Theta with sin Theta = -(1/k) d/dr cos Theta:")
print("  int h sin Theta dr = -[h cos Theta / k]_{r0}^r + int cos Theta (h/k)' dr")
print("  |int h sin Theta dr| <= 2 max|h/k| + int |(h/k)'| dr")
print()
print("So the m != 0 bound is:")
print("  |log U(r) - log U(r0)| <=")
print("    2 max|g/k| + int |(g/k)'| dr  +  2 max|h/k| + int |(h/k)'| dr")
print()
print("With h = 2 m e^phi and k = 2(m e^phi + E e^{2 phi}):")
print("  h/k = m e^phi / (m e^phi + E e^{2 phi})")
print("      = 1 / (1 + (E/m) e^phi)")
print()
print("At canonical Branch-M sub-barrier electron mode (E ~ m at typical phi ~ -0.5):")
print("  E/m ~ 1,  e^phi ~ 0.6,  (E/m) e^phi ~ 0.6")
print("  h/k ~ 1/(1.6) ~ 0.625")
print()
print("At high-spectrum modes (E >> m e^{-phi}): h/k -> 0, m piece negligible.")
print()
print("SUBSTANTIVE FINDING: at canonical Branch-M sub-barrier electron mode (m e^phi ~ E e^{2 phi}):")
print("  h/k ~ O(1), NOT << 1.  IBP bound DOES NOT TIGHTEN — boundary term ~ 1!")
print("  The bound essentially says |log U swing| <= 4 + small integral terms.")
print("  But |log U|_typical = O(1) anyway -- the bound becomes vacuous at m e^phi ~ E e^{2 phi}.")
print()
print("This is the structural obstruction: at canonical Branch-M with m = m_e and E = E_1 = 2 sqrt(2)/3,")
print("the m e^phi piece is COMPARABLE to E e^{2 phi}, the WKB rotation involves BOTH mass and energy,")
print("and the h(r) = 2 m e^phi driver of d/dr log U is NOT small relative to k(r).")
print("The IBP bound exists structurally but is NOT TIGHT — it does not establish |alpha - 2| << 1.")
