import sympy as sp

# Variables
r, kappa, E, m, PHI, PHIp, lam = sp.symbols('r kappa E m PHI PHIp lambda', real=True)
G, F = sp.symbols('G F')

# The first-order system (freeze coefficients = WKB / local analysis):
#  G' = (PHI' - kappa/r) G + (E e^{2PHI} + m e^{PHI}) F
#  F' = (PHI' + kappa/r) F - (E e^{2PHI} - m e^{PHI}) G
# Define coefficients
a = PHIp - kappa/r          # coeff of G in G'
bp = E*sp.exp(2*PHI) + m*sp.exp(PHI)   # coeff of F in G'   (A+ style)
d = PHIp + kappa/r          # coeff of F in F'
bm = E*sp.exp(2*PHI) - m*sp.exp(PHI)   # coeff of G in F' (with minus sign)

# Matrix form  (G,F)' = M (G,F),  M = [[a, bp],[-bm, d]]
M = sp.Matrix([[a, bp],[-bm, d]])
# eigenvalues lambda: solutions ~ e^{lambda r} locally
eig = M.eigenvals()
print("Eigenvalues of frozen system M:")
for k,v in eig.items():
    print("  ", sp.simplify(k))

# trace and det
tr = sp.simplify(M.trace())
det = sp.simplify(M.det())
print("trace =", tr)
print("det   =", det)
# lambda = tr/2 +/- sqrt(tr^2/4 - det). Oscillatory when (tr^2/4 - det) < 0.
disc = sp.simplify(tr**2/4 - det)
print("discriminant tr^2/4 - det =", sp.expand(disc))

# A+ A- product:
ApAm = sp.simplify(bp*bm)
print("A+ A- = (E e^{2PHI}+m e^{PHI})(E e^{2PHI}-m e^{PHI}) =", sp.expand(ApAm))
