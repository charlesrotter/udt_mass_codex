"""
Agent CC sanity sympy check — Schwarz symmetry of mixed second variations
on §99 unified action-level L²(M, sqrt(-g) d⁴x) measure for the J0 Yukawa
coupling at CG §8.5.3a.

NOT a derivation; a sanity check that the action-Schwarz layer is automatic
by Clairaut's theorem for smooth functionals.
"""
import sympy as sp

# Coordinates and abstract fields on canonical UDT metric
t, r, th, ph = sp.symbols('t r theta phi_a', real=True, positive=False)
phi_bg = sp.Function('phi_bg')(r)  # background metric scalar (φ_bg(r))
chi = sp.Function('chi')(t, r, th, ph)  # matter scalar χ
# Use scalar bilinears to stand in for bar(Psi) Psi = G²-F² etc.
Psi_bil = sp.Function('B')(t, r, th, ph)  # = bar(Psi) Psi
alpha = sp.Symbol('alpha', positive=True)

# Volume element sqrt(-g) on canonical UDT metric — φ_bg-independent per CG §1.2
# sqrt(-g) = c r² sin θ ; for the symbolic Clairaut check we drop c, sinθ.
sqrt_g = r**2  # times c sinθ — Schwarz sym is trivially preserved on this factor

# J0 Yukawa coupling integrand at fixed background φ_bg
L_cross = alpha * sqrt_g * chi * Psi_bil

# δ²L/(δχ δB) — pointwise functional kernel at coincident points
# For pointwise multiplicative coupling: L = α sqrt(-g) χ B
# ∂L/∂χ = α sqrt(-g) B
# ∂²L/(∂χ ∂B) = α sqrt(-g)
ddL_chi_then_B = sp.diff(sp.diff(L_cross, chi), Psi_bil)
ddL_B_then_chi = sp.diff(sp.diff(L_cross, Psi_bil), chi)

print("Action-Schwarz residual on §99 unified action L²(M, sqrt(-g) d⁴x):")
print(f"  ∂²L/(∂χ ∂B) = {ddL_chi_then_B}")
print(f"  ∂²L/(∂B ∂χ) = {ddL_B_then_chi}")
print(f"  Schwarz residual = {sp.simplify(ddL_chi_then_B - ddL_B_then_chi)}")

# Check measure consistency: sqrt(-g) = N sqrt(h)
# N = e^(-φ) c, sqrt(h) = e^(φ) r² sin θ, so N sqrt(h) = c r² sin θ = sqrt(-g)
phi = sp.Function('phi_bg')(r)
N = sp.exp(-phi)  # times c, drop
sqrth = sp.exp(phi) * r**2  # times sin θ, drop
print()
print("ADM measure consistency check:")
print(f"  N × sqrt(h) = {sp.simplify(N * sqrth)}")
print(f"  sqrt(-g)    = {sp.simplify(r**2)}")
print(f"  residual    = {sp.simplify(N * sqrth - r**2)}")
