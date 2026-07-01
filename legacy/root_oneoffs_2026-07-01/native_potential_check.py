"""
native_potential_check.py -- TASK 4. Is there a NATIVE potential V(n)?

Candidate: the seal action density eta = q/6 = 1/18, tied to the transgression
Xi = dTheta (h1_types_results.md). Test: does eta enter as a BULK potential in
the Theta Euler-Lagrange equation, or is it STRICTLY a boundary/seal object?

Key derived fact (h1_types): Xi = dTheta is EXACT (global primitive Theta=(ln f)
omega_H1). A bulk Lagrangian piece that is a total derivative (d of something)
contributes ZERO to the bulk Euler-Lagrange equation -- by Stokes its ENTIRE
content is the boundary (seal) value. We verify symbolically that the
transgression density is a total derivative in r, hence boundary-only.
"""
import sympy as sp
r, q = sp.symbols('r q', positive=True)
lnf = sp.Function('lnf')   # ln f(r)

# transgression content per the derived object: Xi = d(ln f) ^ omega_H1, and
# INT_{IxS2} Xi = 4pi (ln f)_seal - 4pi (ln f)_phi0  -- a pure boundary value.
# As a radial density its integrand is d/dr[ 4pi ln f(r) ] = total derivative.
density = sp.Derivative(4*sp.pi*lnf(r), r)
print("Transgression radial density =", density,
      " (a total r-derivative => Stokes => boundary-only).")

# A bulk Euler-Lagrange test: take L_extra = d/dr[G(Theta,r)] (total derivative).
Th = sp.Function('Theta')
G = sp.Function('G')
L_extra = sp.diff(G(Th(r), r), r)   # any total derivative in r
# Euler-Lagrange operator for Theta: dL/dTheta - d/dr(dL/dTheta')
Thp = sp.Derivative(Th(r), r)
EL = sp.diff(L_extra, Th(r)) - sp.diff(sp.diff(L_extra, Thp), r)
print("EL[ total-derivative term ] =", sp.simplify(EL),
      " => contributes 0 to the bulk EOM.")

print("""
VERDICT (Task 4): eta = q/6 = 1/18 is the SEAL/transgression action density.
Xi = dTheta is EXACT (derived, h1_types): its content is PURELY the boundary
(seal) value D = 4pi(ln f)_seal. A total-derivative term has identically zero
bulk Euler-Lagrange contribution. Therefore eta does NOT supply a bulk potential
V(n) that pins the hedgehog orientation -- it is STRICTLY a boundary/seal object
(a junction/closure action), NOT a Derrick-style stabilizing bulk potential.

=> NATIVE POTENTIAL: NO (none falls out as a bulk term). The native stabilizer
   is the Skyrme/winding-current term (Task 1), NOT a potential. eta governs the
   seal closure, a separate (boundary) role. No metric-derived bulk V(n) found.
""")
