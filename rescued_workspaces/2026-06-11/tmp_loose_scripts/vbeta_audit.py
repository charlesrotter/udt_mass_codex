"""Independent verification of S67-004 transport equations at m=0.
Canonical Form-T from CG §4.4:
  G' = (-kappa/r + phi') G + (m e^phi + E e^{2 phi}) F
  F' = (+kappa/r + phi') F + (m e^phi - E e^{2 phi}) G

At m=0:
  G' = (-kappa/r + phi') G + E e^{2 phi} F
  F' = (+kappa/r + phi') F - E e^{2 phi} G

Derive X' = (G^2+F^2)', Y' = (F^2-G^2)', Z' = (GF)' from canonical at m=0.
Compare to agent's claim.
"""
import sympy as sp

r, kappa, m, E = sp.symbols("r kappa m E", real=True)
phi = sp.Function("phi")(r)
G = sp.Function("G")(r)
F = sp.Function("F")(r)

# Canonical Form-T (CG §4.4 verbatim, m=0 limit)
Gprime_canonical_m0 = (-kappa/r + sp.diff(phi, r))*G + E*sp.exp(2*phi)*F
Fprime_canonical_m0 = (+kappa/r + sp.diff(phi, r))*F - E*sp.exp(2*phi)*G

# Agent's Form-T (sympy script line 63-64) at m=0
C_m0 = E*sp.exp(2*phi)
Gprime_agent_m0 = (-kappa/r + sp.diff(phi, r))*G + C_m0*F
Fprime_agent_m0 = (+kappa/r + sp.diff(phi, r))*F - C_m0*G

# At m=0 these should agree
print("=" * 60)
print("Vβ-1: substrate at m=0 comparison")
print("=" * 60)
print(f"G' canonical - G' agent (m=0): {sp.simplify(Gprime_canonical_m0 - Gprime_agent_m0)}")
print(f"F' canonical - F' agent (m=0): {sp.simplify(Fprime_canonical_m0 - Fprime_agent_m0)}")

# Now derive X', Y', Z' from canonical at m=0
X = G**2 + F**2
Y = F**2 - G**2
Z = G*F

Xp_from_canon = 2*G*Gprime_canonical_m0 + 2*F*Fprime_canonical_m0
Yp_from_canon = 2*F*Fprime_canonical_m0 - 2*G*Gprime_canonical_m0
Zp_from_canon = Gprime_canonical_m0*F + G*Fprime_canonical_m0

# Agent's targets at m=0
phip = sp.diff(phi, r)
C_check = E*sp.exp(2*phi)  # = C at m=0

Xp_agent_target = 2*phip*X + (2*kappa/r)*Y
Yp_agent_target = (2*kappa/r)*X + 2*phip*Y - 4*C_check*Z
Zp_agent_target = 2*phip*Z + C_check*Y

print()
print(f"X' from canonical - agent's target (m=0): {sp.simplify(sp.expand(Xp_from_canon) - sp.expand(Xp_agent_target))}")
print(f"Y' from canonical - agent's target (m=0): {sp.simplify(sp.expand(Yp_from_canon) - sp.expand(Yp_agent_target))}")
print(f"Z' from canonical - agent's target (m=0): {sp.simplify(sp.expand(Zp_from_canon) - sp.expand(Zp_agent_target))}")

# Now derive WHAT canonical gives at m != 0
print()
print("=" * 60)
print("Vβ-5a: canonical transport at m != 0 (independent re-derivation)")
print("=" * 60)
Gprime_canon = (-kappa/r + phip)*G + (m*sp.exp(phi) + E*sp.exp(2*phi))*F
Fprime_canon = (+kappa/r + phip)*F + (m*sp.exp(phi) - E*sp.exp(2*phi))*G  # NOTE: + (me^phi - Ee^{2phi})

Xp_canon = sp.expand(2*G*Gprime_canon + 2*F*Fprime_canon)
Yp_canon = sp.expand(2*F*Fprime_canon - 2*G*Gprime_canon)
Zp_canon = sp.expand(Gprime_canon*F + G*Fprime_canon)

# Try matching to 2 phi' X + (2 kappa/r) Y + (mass piece?)
diff_X = sp.simplify(Xp_canon - (2*phip*X + (2*kappa/r)*Y))
diff_Y = sp.simplify(Yp_canon - ((2*kappa/r)*X + 2*phip*Y))
diff_Z = sp.simplify(Zp_canon - (2*phip*Z))
print(f"X' canonical - (2 phi' X + (2 kappa/r) Y) = {diff_X}")
print(f"Y' canonical - ((2 kappa/r) X + 2 phi' Y) = {diff_Y}")
print(f"Z' canonical - 2 phi' Z = {diff_Z}")

# What is the actual structure at m != 0?
# Try: X' = 2 phi' X + (2 kappa/r) Y + A * Z  
# where A is to be determined
A_X = sp.simplify(diff_X / Z) if Z != 0 else None
print(f"\nA_X (coefficient of Z in X' beyond 2 phi' X + (2 kappa/r) Y): {sp.simplify(A_X)}")

# Now compare to agent's S61-005 claim: X' = 2 phi' X + (2 kappa/r) Y (no Z term)
# CG §4.7 line 525: "(G^2+F^2)' = 2 phi'(G^2+F^2) + (2 kappa/r)(F^2-G^2) + 4 m e^phi GF"
# So at m != 0, the canonical X' has +4m e^phi GF = +4m e^phi Z term!
print()
print("CG §4.7 line 525 says X' = 2 phi' X + (2 kappa/r) Y + 4 m e^phi Z")
print(f"Match? Diff = {sp.simplify(diff_X - 4*m*sp.exp(phi)*Z)}")

# Check Y'
diff_Y2 = sp.simplify(Yp_canon - ((2*kappa/r)*X + 2*phip*Y))
print(f"\nY' canonical - ((2 kappa/r) X + 2 phi' Y) = {diff_Y2}")
# Should the residue equal a Z coupling?
# Y' = (2 kappa/r) X + 2 phi' Y + B Z
B_Y = sp.simplify(diff_Y2 / Z)
print(f"B_Y coefficient of Z: {sp.simplify(B_Y)}")

# Z'
diff_Z2 = sp.simplify(Zp_canon - 2*phip*Z)
print(f"\nZ' canonical - 2 phi' Z = {diff_Z2}")
# Try C_Y_y + D_X_x
# match to D_canon * Y + C_canon X 
