"""
BLIND ADVERSARIAL VERIFIER — depth-monodromy of the L2+L4 S^2 soliton.
Independent re-derivation. Does NOT run the constructor scripts.

THE HARDEST TEST (Task 3): does back-reaction (sourced phi) or the seal force
an INTERNAL-LONGITUDE profile psi(r) on the target S^2 (a second internal twist
beyond the single polar profile Theta(r)) that would REVIVE a depth-dependent
Berry phase / monodromy?

Build the GENERALIZED hedgehog that ALLOWS an internal azimuthal twist psi(r).
Internal azimuth = ph + Psi(r). Psi=const => pure meridian/hedgehog.
Derive L2+L4 energy on the back-reacted UDT cell EXACTLY, get the radial
functional, then the Euler-Lagrange equation for Psi(r).
"""
import sympy as sp

print("="*70)
print("GENERALIZED ANSATZ WITH INTERNAL LONGITUDE TWIST Psi(r)")
print("="*70)

r, th, ph = sp.symbols('r theta phi', real=True, positive=True)
Th = sp.Function('Theta')(r)
Ps = sp.Function('Psi')(r)
phi = sp.Function('phi')(r)
xi, kappa, c = sp.symbols('xi kappa c', real=True, positive=True)

# internal polar = Theta(r); internal azimuth = ph + Psi(r)
A = Th
B = ph + Ps
n1 = sp.sin(A)*sp.cos(B)
n2 = sp.sin(A)*sp.sin(B)
n3 = sp.cos(A)
n = sp.Matrix([n1, n2, n3])
print("|n|^2 - 1 =", sp.simplify(n.dot(n) - 1))

grr_inv  = sp.exp(-2*phi)
gthth_inv= 1/r**2
gphph_inv= 1/(r**2*sp.sin(th)**2)
sqrtg = sp.exp(phi)*r**2*sp.sin(th)

coords = [r, th, ph]
ginv = [grr_inv, gthth_inv, gphph_inv]
dn = [sp.diff(n, x) for x in coords]

def cross(a, b):
    return sp.Matrix([a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]])

# L2 density
L2 = sum(ginv[i]*dn[i].dot(dn[i]) for i in range(3))
L2 = sp.Rational(1,2)*xi*L2

# L4 density
L4 = 0
for i in range(3):
    for j in range(3):
        Sij = cross(dn[i], dn[j])
        L4 += ginv[i]*ginv[j]*Sij.dot(Sij)
L4 = sp.Rational(1,4)*kappa*L4

integrand = sp.expand_trig(sp.simplify(sqrtg*(L2 + L4)))

# Manual angular integration: integrate ph in [0,2pi] then th in [0,pi].
# All ph-dependence cancels (axial symmetry) -> integrate ph trivially.
integ_ph = sp.integrate(integrand, (ph, 0, 2*sp.pi))
integ_ph = sp.simplify(integ_ph)
# Now th-integral: substitute u=cos th to make it a polynomial-in-trig integral.
# Use known integrals; do it directly but guard the sin(th) factors.
integ_ph = sp.simplify(sp.powsimp(integ_ph, force=True))
print("\nAfter ph-integration, th-integrand:")
print(integ_ph)

# integrate over th. Expand into a sum and integrate term by term.
expr = sp.expand(integ_ph)
Efull = 0
for term in expr.as_ordered_terms():
    Efull += sp.integrate(term, (th, 0, sp.pi))
Efull = sp.simplify(Efull)
print("\n" + "="*70)
print("RADIAL ENERGY FUNCTIONAL E[Theta(r), Psi(r), phi(r)] (integrand in r):")
print("="*70)
print(Efull)
sp.srepr  # keep
# Save for reuse
import pickle
with open('/tmp/verif_Efull.pkl','wb') as f:
    pickle.dump(sp.srepr(Efull), f)
print("\n(saved)")
