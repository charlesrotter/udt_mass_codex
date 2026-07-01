"""
udta_symmetric_resolution.py
The owner's argument says mass rides NEITHER the clock NOR the ruler alone,
because they diverge. What is the SYMMETRIC / invariant build that does not
privilege one sector? Test candidates rigorously, sign-careful. DATA-BLIND.
"""
import sympy as sp
phi = sp.Symbol('phi', real=True)
c0, hbar, m0, lam = sp.symbols('c0 hbar m0 lam', positive=True)

print("Candidate resolutions for a, given clock~e^{-phi}, ruler~e^{+phi}:")
print()

# Candidate 1: proper 4-VOLUME / invariant action element.
# The invariant proper measure: sqrt(-g) d^4x.
# sqrt(-g) for diag(-e^{-2phi}c0^2, e^{2phi}, r^2, r^2 sin^2): 
g = sp.diag(-sp.exp(-2*phi)*c0**2, sp.exp(2*phi), sp.Symbol('r')**2, 1)
# only the t,r block carries phi:
sqrtg_tr = sp.sqrt(sp.exp(-2*phi)*c0**2 * sp.exp(2*phi))
print("C1 sqrt(-g) t-r block =", sp.simplify(sqrtg_tr), 
      " -> phi CANCELS (e^{-phi}*e^{+phi}=1). The proper 4-volume is phi-INVARIANT.")
print("    => an action/energy tied to proper 4-volume sees NO net phi-scaling there;")
print("    the B=1/A cancellation is exactly why the metric DETERMINANT is flat.")
print()

# Candidate 2: mass as rest ENERGY/c^2 where energy = action/proper-time, and the
# action is the dimensionless invariant (phase, in units of hbar, is an INVARIANT count).
# Phase  S/hbar = INT m c^2 dtau / hbar  is a pure number (invariant, Sense-1 hbar fixed).
# A FIXED phase accumulated over a FIXED number of proper ticks:
#   m c0^2 dtau = hbar * (fixed phase)  =>  m = hbar*phase/(c0^2 dtau_proper)
# proper tick dtau_proper is LOCAL = fixed (Sense 1). So m_LOCAL = m0 fixed. (trivial: a acts on AFAR reading.)
print("C2: the action/phase is an invariant count; LOCAL m=m0 always (Sense-1). a")
print("    governs only the AFAR ATTRIBUTION, so we must build the afar reading.")
print()

# Candidate 3 (the geometric mean / 'no privileged sector'):
# afar mass = geometric mean of clock-route (e^{-phi}) and ruler-route (e^{+phi}):
gm = sp.sqrt(sp.exp(-phi)*sp.exp(+phi))
print("C3 geometric mean of clock & ruler routes =", sp.simplify(gm), 
      " = e^{0} => a=0 (mass phi-INDEPENDENT as seen from afar).")
print("    This is the 'rides neither' literal reading: the divergent factors cancel.")
print()

# Candidate 4: mass = E/c^2 with E from afar-frequency AND c the LOCAL c0 (Sense1),
# but the afar energy built from the full proper-4-volume-normalized mode.
# A localized mode's afar energy = hbar * (afar frequency). Afar frequency we found
# = e^{-phi} f_local (Route A, robust: frequency is inverse coordinate time, the
# clock factor, period). That gives a=-1 UNAMBIGUOUSLY for ENERGY-as-frequency.
# The ruler route gave a=+1 for MASS-as-inverse-Compton-length.
# Reconcile via E=mc^2 with c=LOCAL c0: if E~e^{-phi} and m=E/c0^2 then m~e^{-phi} (a=-1).
# The a=+1 came from using m=hbar/(c lambda): consistent ONLY if c there is the
# COORDINATE c=c0 e^{-2phi}:  m = hbar/(c_coord * lambda_afar)
phi_s=phi
c_coord = c0*sp.exp(-2*phi_s)
lam_afar = lam*sp.exp(-phi_s)   # proper length lam seen as coord extent
m_B_coordc = hbar/(c_coord*lam_afar)
print("C4 RECONCILE the ruler route using the COORDINATE c (= c0 e^{-2phi}):")
print("   m = hbar/(c_coord * lam_afar) =", sp.simplify(m_B_coordc/(hbar/(c0*lam))),
      "* (hbar/c0 lam)")
expo = sp.simplify(sp.log(m_B_coordc) - sp.log(hbar/(c0*lam)))
print("   exponent in phi =", expo, "  => a = +1 still? check:")
print("   ", sp.simplify(m_B_coordc), " => e^{+phi+2phi}=e^{3phi}?? sign of c_coord power")
# explicit:
print("   m_B_coordc simplified:", sp.powsimp(sp.simplify(m_B_coordc), force=True))
