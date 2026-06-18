"""
The decisive question (claim 2, both directions):
 (A) Is a=-1 genuinely an ADMISSIBLE self-consistent reading? (if not -> under-det REFUTED)
 (B) Is the menu genuinely a MENU, or is it actually MORE determined than claimed
     (i.e. does a covariant argument single out ONE value, collapsing the under-det
      from the other side)?
"""
import sympy as sp
phi, c0, hbar, m0 = sp.symbols('phi c0 hbar m0', positive=True)
g_tt = -sp.exp(-2*phi)*c0**2
g_rr = sp.exp(2*phi)
dtau_dt = sp.sqrt(-g_tt)/c0  # e^{-phi}

print("""
KEY DISTINCTION the doc trades on:
  Route A asks: what mass-NUMBER does the AFAR observer assign to a deep source?  -> e^{-phi}
  Route B asks: what is the source's LOCAL rest mass as a function of its position?
The two 'faces' answer DIFFERENT questions. The exponent `a` in m(phi)=m0 e^{a phi}
is, per the field-eqn doc, the LOCAL rest mass as a function of local position phi
(the new SOURCE effect entering T_munu locally). It is NOT the afar-assigned number.
""")

print("--- Is a=-1 admissible as the LOCAL law? ---")
print("""
Sense-1 (owner-confirmed, K10): LOCAL physics is UNMODIFIED. Local rest mass = m0,
held FIXED everywhere as a universal constant. Taken literally, Sense-1 says the
LOCAL rest mass does NOT vary with position at all -> the local m(phi)=m0 -> a=0 (!).
The thing that varies is the AFAR-ASSIGNED mass number, which redshifts as e^{-phi}
(a=-1 as an afar bookkeeping exponent).

So there is a genuine tension in the FRAME of the question:
 - If `a` = local rest-mass slope: Sense-1 forces a=0 (local mass is a constant).
 - If `a` = afar-assigned energy slope: Killing energy forces a=-1.
 - The field-eqn doc's source weight e^{(a+1)phi} needs the LOCAL coupling exponent,
   which is the slope of the mass that sits IN the local T_munu.
""")

print("--- Does Sense-1 (local mass fixed) actually EXCLUDE a!=-1? ---")
print("""
The field-eqn doc (P1) explicitly says 'MASS dilates with position' = the NEW source
effect, NOT present in GR. That CONTRADICTS a literal Sense-1 'local mass = m0 const'.
=> The two committed postulates (Sense-1 local-mass-fixed vs P1 mass-dilates) are in
   tension. The exponent `a` is precisely the dial that interpolates:
     a=0  : local mass truly constant (strict Sense-1) -- but then NOT 'mass dilates'
     a=-1 : local mass tracks the clock (metric-locked) -> source weight 1 -> UDT=GR
     a!=-1: mass dilates out of step -> genuine modification
""")

# Check: the menu values and whether any covariant principle removes the freedom.
print("--- Covariant pin attempt: extremize test-particle action m(phi) int dtau ---")
# action S = -int m(phi) c^2 dtau ; for a static config the 'energy' conjugate to t.
# Lagrangian for radial motion: L = -m(phi) c0^2 dtau/dt. Conserved energy:
m = m0*sp.exp(sp.Symbol('a')*phi)
a = sp.Symbol('a')
# static particle: energy = m(phi) c0^2 dtau/dt = m0 e^{a phi} c0^2 e^{-phi}
E_static = m0*sp.exp(a*phi)*c0**2*dtau_dt
print("test-particle conserved energy E(phi) = m(phi)c0^2 (dtau/dt) ~",
      sp.simplify(E_static/(m0*c0**2)), " exponent:", sp.simplify(sp.log(sp.simplify(E_static/(m0*c0**2)))/phi))
print("""
For E to be the position-INDEPENDENT conserved Killing energy (so a free static
particle has no net force / sits in equilibrium agnostic of depth), need exponent 0:
   a - 1 = 0  => a = +1  (!!)
i.e. demanding the test-mass action's conserved energy be phi-independent picks a=+1,
NOT a=-1. Demanding instead that the AFAR energy redshift be the standard e^{-phi}
picks the reading a=-1. These are DIFFERENT covariant-looking demands giving DIFFERENT
values. => the menu is REAL; no single covariant principle is uniquely forced.
""")

print("--- Verdict on determinacy ---")
print("""
* a=-1 IS admissible (Killing/afar-energy reading). Under-det NOT refuted from that side.
* a=+1 is ALSO admissible (conserved test-particle energy / ruler reading).
* a=0 is admissible (strict Sense-1 local-mass-constant).
=> Genuinely under-determined. The doc's menu {-3,-1,0,+1,+3} is sound; if anything
   the doc UNDERSTATES the tension by privileging a=-1 in its prose (K5, missing-input).
""")
