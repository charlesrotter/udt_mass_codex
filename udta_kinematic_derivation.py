"""
udta_kinematic_derivation.py
Sign-careful derivation of the mass-dilation exponent a in m(phi)=m0 e^{a phi}.
Category-A, DATA-BLIND. sympy CPU. Nothing committed touched.

Metric (CANON C-2026-06-18-1):
    g_tt = -e^{-2phi} c0^2 ,  g_rr = e^{2phi}  (B=1/A; g_tt g_rr = -c0^2).

Sense-1 (observer-frame): held FIXED everywhere = LOCAL invariants:
    local c = c0,  local rest mass = m0,  hbar.
phi defined up to a constant; "afar" = reference position phi_ref (take 0).
"""
import sympy as sp

phi, c0, hbar, m0, a = sp.symbols('phi c0 hbar m0 a', positive=True, real=True)
phi = sp.Symbol('phi', real=True)   # phi can be any sign

# ---- 1. Proper time and proper length read off the metric (SIGN-CAREFUL) ----
# Proper time of a STATIC clock at position phi: dtau = sqrt(-g_tt)/c0 * dt
#   sqrt(-g_tt) = sqrt(e^{-2phi} c0^2) = c0 e^{-phi}
# so  dtau/dt = e^{-phi}.   => proper-time TICK length ~ e^{-phi} (contracts as phi>0)
dtau_dt = sp.sqrt(sp.exp(-2*phi)*c0**2)/c0
dtau_dt = sp.simplify(dtau_dt)
print("dtau/dt =", dtau_dt, "  => proper time ~ e^{-phi}  (CONTRACTS for phi>0)")

# Proper radial length of a static ruler: dL = sqrt(g_rr) dr = e^{+phi} dr
dL_dr = sp.sqrt(sp.exp(2*phi))
print("dL/dr  =", sp.simplify(dL_dr), "  => proper length ~ e^{+phi} (EXPANDS for phi>0)")
print("RECIPROCAL DIVERGENCE confirmed: time e^{-phi}, length e^{+phi} (opposite). [B=1/A]")
print()

# ---- ROUTE A: dimensional build of mass from invariants ----
# Mass dimension: [m] = [E]/[c]^2 = ([action]/[time])/[c]^2 = [hbar]/([time][c]^2)
#   (since E = hbar * frequency = hbar / time;  m = E/c^2)
# Sense-1: hbar FIXED (invariant), local c = c0 FIXED.
# The ONLY thing that scales is the TIME that enters. Which time?
#
# "Mass as attributed FROM AFAR" = energy/frequency as the distant (reference)
# observer reckons it, divided by c^2. The distant observer reads the LOCAL
# proper period of the source's quantum clock, but TRANSPORTED to afar.
#
# A local oscillator has proper period dtau (proper time). Its frequency
# AS MEASURED LOCALLY is f_local = 1/dtau_local = fixed (Sense 1, local physics
# universal). The frequency AS SEEN FROM AFAR uses coordinate time dt:
#   f_afar = 1/dt = (dtau/dt) * f_local = e^{-phi} f_local.
# So the energy attributed from afar:  E_afar = hbar f_afar = hbar e^{-phi} f_local.
# Mass attributed from afar:  m_afar = E_afar / c0^2 = (hbar f_local/c0^2) e^{-phi}
#                                    = m0 e^{-phi}.
# => a = -1  by the NAIVE frequency-redshift route.
print("ROUTE A (naive frequency redshift, single clock):")
f_local = sp.Symbol('f_local', positive=True)
f_afar = dtau_dt * f_local
E_afar = hbar * f_afar
m_afar = E_afar / c0**2
print("  m_afar =", sp.simplify(m_afar), " => a = -1  (mass rides the CLOCK only)")
print()

# ---- ROUTE B: mass from the Compton length (RULER route), the cross-check ----
# A mass also defines a LENGTH: the Compton wavelength lambda_C = hbar/(m c).
# Locally lambda_C,local = hbar/(m0 c0) = fixed invariant (Sense 1).
# AS SEEN FROM AFAR, a proper length lambda_C,local occupies coordinate extent
#   dr = dL / sqrt(g_rr) = lambda_C,local * e^{-phi}   (a proper length e^{+phi} per dr
#   means a fixed proper length spans FEWER coordinate dr by e^{-phi}).
# The mass attributed from afar from this RULER:
#   m_afar^{ruler} = hbar/(c0 * lambda_C,afar-in-proper?) ...
# Careful: the distant observer reckons mass via m = hbar/(c0 * lambda_C) using
# the lambda_C he ATTRIBUTES. He attributes the source's proper Compton length
# but reads it through HIS rulers. A proper length L_proper seen from afar
# corresponds to coordinate dr = L_proper e^{-phi}; reconverting to the distant
# observer's OWN proper length (at phi_ref=0, where his ruler = coordinate):
#   L_afar = dr = lambda_C,local * e^{-phi}.
# Then  m_afar^{ruler} = hbar/(c0 L_afar) = hbar/(c0 lambda_C,local e^{-phi})
#                      = m0 e^{+phi}.
print("ROUTE B (Compton-length / ruler route):")
lamC_local = hbar/(m0*c0)
L_afar = lamC_local * sp.exp(-phi)     # proper length seen as coordinate extent at ref
m_afar_ruler = hbar/(c0*L_afar)
print("  m_afar^ruler =", sp.simplify(m_afar_ruler), " => a = +1  (mass rides the RULER only)")
print()

print("RECONCILIATION:")
print("  Route A (clock) gives a=-1; Route B (ruler) gives a=+1. They DISAGREE")
print("  precisely because clock e^{-phi} and ruler e^{+phi} DIVERGE (B=1/A).")
print("  This is the owner's argument made quantitative: there is NO single")
print("  metric rate to ride. A self-consistent mass cannot pick one sector.")
print()

# ---- The consistent build: mass uses BOTH (it has units of both) ----
# m = [hbar]/([time][c]^2)  carries 1 power of inverse-time (clock) and is also
# = [hbar]/([length][c]) via Compton (1 power of inverse-length, ruler).
# These are the SAME m only if c is the SAME in both - and locally c=c0 ties them:
#   E = hbar/dtau = m c^2   and   lambda = hbar/(m c)  =>  lambda = c dtau.
# The geometric (afar) relation between a proper time and proper length is the
# LOCAL light cone: c0 dtau = dL_proper (both proper). Transported to afar:
#   c0 (dtau/dt) dt_afar = ? ... the afar light cone uses COORDINATE speed
#   (dr/dt)_coord = c0 e^{-2phi}.  A local light-crossing of the Compton length:
#   proper:  lambda_C = c0 * (proper period) -> consistent locally.
#   afar:    the SAME light segment has coord extent dr=lambda e^{-phi} and coord
#            duration dt = dr/(c0 e^{-2phi}) = lambda e^{-phi}/(c0 e^{-2phi})
#                        = (lambda/c0) e^{+phi}.
#   So the afar PERIOD of the quantum clock = (lambda_local/c0) e^{+phi}
#      = (proper period) e^{+phi}... wait, cross-check vs dtau/dt below.
print("CONSISTENT BUILD (mass = hbar * (afar frequency) / c0^2, frequency from the")
print("light-crossing of the Compton length, the object that DEFINES the mass):")
lam_local = sp.Symbol('lam_local', positive=True)   # proper Compton length, fixed
# afar coordinate extent of that proper length:
dr_afar = lam_local*sp.exp(-phi)
# coordinate light speed:
cr_coord = c0*sp.exp(-2*phi)
# afar coordinate duration of one Compton light-crossing:
dt_cross = dr_afar/cr_coord
print("  afar light-crossing coord-time dt =", sp.simplify(dt_cross), " (= (lam/c0) e^{+phi})")
# afar frequency = 1/dt_cross
f_afar2 = 1/dt_cross
# mass from afar = hbar f_afar / c0^2  (E=hbar f, m=E/c0^2; c0 fixed Sense-1)
m_afar2 = hbar*f_afar2/c0**2
print("  m_afar (consistent) ~ hbar f/c0^2 =", sp.simplify(m_afar2))
print("  exponent in phi:", sp.simplify(sp.log(m_afar2/ (hbar/(c0**2)) * (lam_local) )))
# isolate exponent: m_afar2 = (hbar/(lam_local c0)) e^{-phi}  -> that's a=-1 again unless...
print()
print("  NOTE: this light-crossing build returns e^{-phi} (a=-1) because the SAME")
print("  e^{+phi} length and e^{-2phi} speed combine: -1-(-2)= +1 in the PERIOD,")
print("  hence -1 in the FREQUENCY -> a=-1. The clock and the coord-speed conspire")
print("  to reproduce the pure-clock answer.  So the light-crossing definition")
print("  COLLAPSES to Route A (a=-1). The a=+1 ruler route used the LOCAL c (not")
print("  the coordinate c) to convert ruler->mass; that is the Sense-1-consistent")
print("  conversion. The discrepancy is REAL and traces to which c converts the")
print("  ruler to a mass.")
