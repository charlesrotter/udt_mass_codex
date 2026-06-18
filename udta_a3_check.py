"""
udta_a3_check.py  --  trace EXACTLY which choices yield each candidate a.
Sign-careful enumeration. The inline tentative was a=-3 (weight e^{-2phi}).
DATA-BLIND.
"""
import sympy as sp
phi = sp.Symbol('phi', real=True)
c0, hbar, lam = sp.symbols('c0 hbar lam', positive=True)

# Building blocks (afar reading, ref at phi=0), all sign-checked from the metric:
clock = sp.exp(-phi)       # dtau/dt : proper time per coord time
ruler = sp.exp(+phi)       # dL/dr   : proper length per coord length
c_coord = c0*sp.exp(-2*phi)# (dr/dt)_coord
c_loc = c0                 # local measured c (Sense-1 invariant)

def expo(x):
    return sp.simplify(sp.log(sp.simplify(x))).coeff(phi)

# m = E/c^2 = (hbar f)/c^2 ; f = afar frequency = 1/(coord period)
# Two ways to read mass; mass has BOTH a time-face (E/c^2) and length-face (hbar/(c lam)).
print("Enumerate m_afar = hbar * f / c^2  and  m_afar = hbar/(c * lam):")
print()

# afar frequency from a LOCAL oscillator (period = proper period, fixed): f = clock * f_loc
f_clock = clock              # ~ e^{-phi}
# afar Compton length seen as coordinate extent:
lam_afar = lam*ruler/ruler*sp.exp(-phi)  # proper length lam -> coord dr = lam e^{-phi}
print(" face=ENERGY/c^2, c=LOCAL c0 :  m ~ f_clock/c0^2 ~ e^{-phi}  => a = -1  [clock, GR redshift]")
print(" face=ENERGY/c^2, c=COORD    :  m ~ f_clock/c_coord^2 ~ e^{-phi}/e^{-4phi} = e^{+3phi} => a=+3")
m = f_clock/c_coord**2
print("    check:", sp.powsimp(sp.simplify(m),force=True), " exponent", expo(m))
print()
print(" face=hbar/(c*lam), c=LOCAL c0:  m ~ 1/(c0 * lam e^{-phi}) ~ e^{+phi} => a = +1  [ruler]")
print(" face=hbar/(c*lam), c=COORD   :  m ~ 1/(c_coord * lam e^{-phi})")
m2 = 1/(c_coord*lam*sp.exp(-phi))
print("    check:", sp.powsimp(sp.simplify(m2),force=True), " exponent", expo(m2), " => a = +1??")
print()
# The tentative a=-3 / weight e^{-2phi}:  weight e^{(a+1)phi} = e^{-2phi} <=> a = -3.
print("TARGET a=-3  <=> source weight e^{(a+1)phi} = e^{-2phi}.")
print("Which build gives a=-3 (m~e^{-3phi})?")
# m ~ e^{-3phi}: e.g. f_clock/c^2 with c = c0 e^{+phi}?? but coord c is e^{-2phi}.
# Or energy redshifts as e^{-phi} (clock) AND divided by c_coord^2=e^{-4phi}? that's +3.
# To get -3 need: clock e^{-phi} * (extra e^{-2phi} from TWO more clock-like factors).
m3a = clock * sp.exp(-2*phi)   # clock energy further measured per (proper-volume e^{-?})
print("  e.g. clock-energy e^{-phi} times proper-3-volume factor e^{-2phi}:",
      sp.simplify(m3a), " exponent", expo(m3a), " (a=-3)")
print()
print("  The a=-3 reading: mass = energy density integrated over the PROPER SPATIAL")
print("  3-volume but read with the AFAR clock-energy, where the spatial 3-volume")
print("  e^{+3phi}*... -- NOTE this requires a SPECIFIC volume-vs-point choice.")
print()

# Map to the FIELD result: kinetic ~ e^{(a-1)phi}, angular ~ e^{(a+1)phi}.
# The committed source's DOMINANT deep-phi behavior: at large phi (deep core),
# e^{-2phi}=A->? deep core is phi -> -p (negative, large |phi|): e^{-2phi} BLOWS UP.
print("DEEP-CORE (phi -> large negative, the sub-nuclear extreme):")
print("  X=e^{-2phi}Tp^2 DOMINATES (e^{-2phi} large). So the KINETIC sector wins.")
print("  Kinetic scales as e^{(a-1)phi}. For the field's deep energy to track the")
print("  point mass m~e^{a phi}, need (a-1)=a => impossible, OR the point-mass")
print("  identification is with the kinetic invariant => observed exponent = a-1.")
print("  If a(point,clock)=-1 then kinetic-sector field exponent = -2  => weight")
print("  on the DEEP source ~ e^{(a+1)phi} with effective a+1 = -2 => a=-3 EMERGES")
print("  as the FIELD-SECTOR (deep, kinetic-dominated) effective exponent IF the")
print("  point value is the clock value -1. The e^{-2phi} weight = the kinetic")
print("  sector's extra g^{rr} contraction. THIS is the origin of the a=-3 guess.")
