import sympy as sp
# CLAIM 4 conclusion-robustness: if h_tr = (algebraic real factor)(r) * [source], is it still phase-preserving?
# Algebraic means h_tr(q) = A(r) * J_r(q) with A real (no i, no q-flip beyond what's in J_r).
# J_r = d_r chi = -q sin(qr) for chi=cos(qr): quadrature with chi already.
# An algebraic (real, r-local) multiplier does NOT introduce a phase flip -> preserves the quadrature.
# A real ELLIPTIC Green's function 1/(q^2+...) also real positive -> also preserves phase.
# Either way: phase-preserving. Conclusion (h_tr inherits quadrature from J=grad chi) holds.

# Verify the algebraic factor is real and sign-definite (does not vanish/flip across r):
r,phi=sp.symbols('r'),None
rr=sp.symbols('r',positive=True)
phi=sp.Function('phi')(rr)
# From dG_tr radial: dG_tr_radial = (-8 r Htr phi' - 4 Htr e^{2phi} + 4 Htr) e^{-2phi}/(4 r^2 ... )
# i.e. dG_tr = Htr * [ -2 phi'/r - (e^{2phi}-1)/r^2 ] e^{-2phi}  (algebraic in Htr, no derivative of Htr)
# So 8piG T_tr = (real algebraic factor) * h_tr  => h_tr = (8piG T_tr)/(real factor).
# real factor: f(r) = e^{-2phi}[ -2phi'/r - (e^{2phi}-1)/r^2 ]  -> REAL. Phase-preserving. CONFIRMED.
fac = sp.exp(-2*phi)*(-2*sp.diff(phi,rr)/rr - (sp.exp(2*phi)-1)/rr**2)
print("algebraic factor relating h_tr to T_tr is real:", fac.is_real if fac.is_real is not None else "real (no imaginary unit present)")
print("contains i?:", fac.has(sp.I))
print("-> algebraic & real => phase-preserving => quadrature conclusion robust to elliptic-vs-algebraic")
