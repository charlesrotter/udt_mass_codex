"""
PART 2: THE BC CRUX.  Is regularity => Dirichlet on psi at r=0 correct?

SL form (re-derived, frozen w=0):  (P f u')' + omega^2 (P/f) u = 0, P = 2 r^2.
Liouville: psi = sqrt(P) u, coord x=r* (dr*=dr/f), -psi_xx + V psi = omega^2 psi.
"""
import sympy as sp

r = sp.symbols('r', positive=True)
a2, phi0 = sp.symbols('a2 phi0', real=True)
phi = phi0 + a2*r**2          # smooth even core: phi'(0)=0
f = sp.exp(-2*phi)
P = 2*r**2
om = sp.symbols('omega', positive=True)

print("=== Indicial analysis of SL operator at r=0 ===")
for sval in [0, -1, 1, -2]:
    u0 = r**sval
    res = sp.diff(P*f*sp.diff(u0, r), r) + om**2*(P/f)*u0
    res = sp.simplify(res)
    # leading power as r->0
    lead = sp.simplify(res / r**(sval)) if sval != 0 else res
    val0 = sp.limit(res*r**(-sval) if sval<0 else res, r, 0)
    print(f"  u = r^{sval}:  residual leading behavior, lim (res/r^max(s,?)) ...")
    print(f"     res = {res}")

print()
print("Dominant balance (kinetic term (P f u')' for u=r^s, P f ~ 2 e^{-2phi0} r^2):")
print("   P f u' = 2 e^{-2phi0} s r^{s+1};  d/dr = 2 e^{-2phi0} s(s+1) r^s")
print("   om^2 (P/f) u = O(r^{s+2}) subdominant")
print("   => INDICIAL: s(s+1) = 0  ->  s = 0  or  s = -1")
print()
print("  s = 0 : u ~ const  (REGULAR core, even field)  -> psi = sqrt(2) r u ~ r  => psi(0)=0  (DIRICHLET)")
print("  s =-1 : u ~ 1/r     (SINGULAR core)            -> psi ~ const           => psi(0)!=0 (NEUMANN)")
print()

# ---- ENERGY NORM check: which branch is normalizable / finite-energy?
# Physical L2 norm uses the SL WEIGHT rho = P/f = 2 r^2 e^{2phi0}.
#   ||u||^2 = int rho |u|^2 dr = int 2 r^2 e^{2phi0} |u|^2 dr near 0.
# Energy (gradient) norm uses p = P f = 2 r^2 e^{-2phi0}:
#   E ~ int p |u'|^2 dr = int 2 r^2 e^{-2phi0} |u'|^2 dr.
print("=== Normalizability near r=0 (which branch is admissible) ===")
e2 = sp.exp(2*phi0); em2 = sp.exp(-2*phi0)
for sval, lbl in [(0,'regular u~const'), (-1,'singular u~1/r')]:
    u0 = r**sval
    rho = 2*r**2*e2
    p = 2*r**2*em2
    nrm = sp.integrate(rho*u0**2, (r, 0, sp.Rational(1,1000)))
    egr = sp.integrate(p*sp.diff(u0,r)**2, (r, 0, sp.Rational(1,1000)))
    print(f"  {lbl}: int rho u^2 dr (mass) finite? -> {sp.simplify(nrm)} ;",
          f"int p u'^2 dr (energy) -> {sp.simplify(egr)}")

print()
print("INTERPRETATION:")
print(" - regular u~const: mass-norm int r^2 dr ~ finite, energy int r^2 *0 ~ finite. ADMISSIBLE.")
print(" - singular u~1/r : mass int r^2 (1/r^2) dr = int dr finite at 0 (!!), ")
print("     BUT energy int r^2 (1/r^2)^2 *... wait u'=-1/r^2 -> p u'^2 = 2r^2 e^{-2phi0}/r^4 = 2e^{-2phi0}/r^2")
print("     int_0 dr/r^2 = DIVERGES => INFINITE ENERGY.  This matches the claim: u~1/r is infinite-energy.")
print()
print(">>> BC CRUX VERDICT: The mapping  regular(u finite) <-> Dirichlet(psi~r->0)  is CORRECT.")
print(">>> The u~1/r (psi~const, Neumann) branch has DIVERGENT energy norm at r=0.")
print(">>> So the claim's load-bearing BC step is SOUND -- regular core forces Dirichlet on psi.")
