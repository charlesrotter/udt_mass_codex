import sympy as sp

# Symbols
r, phi, phia, phib, w, c, lam = sp.symbols('r phi phi_a phi_b omega c lambda', positive=True, real=True)

# Radial equation: (1/r^2) d/dr( r^2 e^{-2phi} g') + (w^2/c^2) e^{2phi} g = 0
# Multiply by r^2:  d/dr( r^2 e^{-2phi} g') + (w^2/c^2) r^2 e^{2phi} g = 0
# SL form: (p g')' + lam W g = 0  with lam = w^2/c^2
# => p = r^2 e^{-2phi},  W = r^2 e^{2phi},  lam = w^2/c^2

p = r**2 * sp.exp(-2*phi)
W = r**2 * sp.exp(2*phi)
lam_val = w**2/c**2

# Local WKB wavenumber k = sqrt(lam W / p)
k = sp.sqrt(lam_val * W / p)
k = sp.simplify(k)
print("p   =", p)
print("W   =", W)
print("k   =", k)

# effective phase speed c_eff = w/k
c_eff = sp.simplify(w/k)
print("c_eff =", c_eff)

# Impedance Z = p*k
Z = sp.simplify(p*k)
print("Z = p*k =", Z)
print("Z depends on phi?", phi in Z.free_symbols)

# Reflection at a step in phi at fixed radius r: phi_a -> phi_b
ka = k.subs(phi, phia)
kb = k.subs(phi, phib)
pa = p.subs(phi, phia)
pb = p.subs(phi, phib)
Za = sp.simplify(pa*ka)
Zb = sp.simplify(pb*kb)
R = sp.simplify((Za - Zb)/(Za + Zb))
print("Za =", Za)
print("Zb =", Zb)
print("R (from p*k impedance) =", R)

# Alternative acoustic convention Z ~ 1/c_eff
c_eff_a = c_eff.subs(phi, phia)
c_eff_b = c_eff.subs(phi, phib)
R_acoustic = sp.simplify((c_eff_a - c_eff_b)/(c_eff_a + c_eff_b))
print("c_eff =", c_eff, " (c_eff = c e^{-2phi})")
print("R_acoustic (c_a-c_b)/(c_a+c_b) =", R_acoustic)
dphi = sp.symbols('Delta')
print("tanh(Delta phi) check:", sp.simplify(R_acoustic.rewrite(sp.tanh)) if False else "see numeric")

# numeric check of acoustic R vs tanh(dphi) with dphi=phib-phia
import math
pa_v, pb_v = 0.3, 0.9
ca = math.exp(-2*pa_v); cb = math.exp(-2*pb_v)
print("numeric acoustic R =", (ca-cb)/(ca+cb), " tanh(phib-phia)=", math.tanh(pb_v-pa_v))
