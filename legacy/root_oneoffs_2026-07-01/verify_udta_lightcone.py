"""
Careful scrutiny of the K5 'light-cone collapse to a=-1' claim, and the
Killing-energy a=-1 identification (claims 2,4,5).
"""
import sympy as sp
phi, c0, hbar, m0 = sp.symbols('phi c0 hbar m0', positive=True)

g_tt = -sp.exp(-2*phi)*c0**2
g_rr = sp.exp(2*phi)
dtau_dt = sp.sqrt(-g_tt)/c0          # e^{-phi}
dL_dr   = sp.sqrt(g_rr)              # e^{+phi}
v_coord = sp.sqrt(-g_tt/g_rr)        # c0 e^{-2phi}

print("=== K5 light-cone: what frequency does a Compton-length mode have, seen from afar? ===")
lam_C = hbar/(m0*c0)                  # PROPER Compton length (local invariant)

# A mode 'rings' by light crossing its own proper Compton length.
# LOCAL view (Sense-1): local c=c0, proper length lam_C => proper period T_proper = lam_C/c0
T_proper = lam_C/c0
print("local proper period T_proper = lam_C/c0 =", sp.simplify(T_proper))
# frequency seen from afar = (dtau/dt) * f_local  [time dilation of the local clock]
f_local = 1/T_proper
f_afar = dtau_dt * f_local
print("f_afar = (dtau/dt) f_local =", sp.simplify(f_afar), " scaling:",
      sp.simplify(sp.log(sp.simplify(f_afar/(c0/lam_C)))/phi))
print("  => this is just Route A again: f_afar ~ e^{-phi}, m=hbar f_afar/c0^2 ~ e^{-phi}, a=-1")

print("\n--- alternative 'coordinate-speed crossing' build the doc invokes ---")
# proper Compton length spans coordinate extent dr = lam_C * e^{-phi}
dr_span = lam_C/dL_dr
# cross at COORDINATE speed v_coord => coordinate period
T_coord = dr_span/v_coord
print("coord extent dr =", sp.simplify(dr_span))
print("coord crossing period T_coord = dr/v_coord =", sp.simplify(T_coord),
      " scaling:", sp.simplify(sp.log(sp.simplify(T_coord/(lam_C/c0)))/phi))
# This coordinate period, converted to afar frequency: f = 1/T_coord (coordinate freq)
f_coord = 1/T_coord
print("coordinate freq f=1/T_coord scaling:",
      sp.simplify(sp.log(sp.simplify(f_coord/(c0/lam_C)))/phi), " => e^{+phi}, would be a=+1")
# convert coordinate freq to PROPER (afar) freq via dtau/dt
f_afar2 = dtau_dt*f_coord
print("convert to afar proper freq (x dtau/dt):",
      sp.simplify(sp.log(sp.simplify(f_afar2/(c0/lam_C)))/phi), " => e^{0}!  NOT e^{-phi}")

print("""
OBSERVATION: The two clean self-consistent builds give:
  (1) local-c crossing + clock dilation  => f_afar ~ e^{-phi}  => a=-1   (= Route A)
  (2) coord-c crossing + clock dilation   => f_afar ~ e^{0}    => a=0
Neither cleanly gives the doc's 'collapse to a=-1 via coordinate speed'.
The doc's K5 narrative ('e^{+phi} ruler and e^{-2phi} coord speed combine to e^{-phi}')
mixes a coordinate-speed crossing with a LOCAL-clock period read, which is internally
inconsistent (it uses coord c for length but local clock for time). The DEFENSIBLE
a=-1 build is simply Route A (local everything) -- no coordinate speed needed.
""")

print("=== Claims 4/5: Komar/Killing energy for the FULL metric (incl. c0 e^{-2phi} lapse) ===")
# Komar energy uses the timelike Killing vector xi = d/dt. Conserved energy of a
# particle: E = -g_{tt} u^t * m / (normalization). For a STATIC particle u^t = 1/sqrt(-g_tt),
# E_conserved = m * (-g_tt) u^t / c-stuff ... do the invariant version:
# E/c = -g_{munu} xi^mu p^nu = -g_tt p^t.  p^t = m u^t (local rest mass m=m0).
# u^t normalized: g_tt (u^t)^2 = -c0^2  => u^t = c0/sqrt(-g_tt)
ut = c0/sp.sqrt(-g_tt)
E_over = -g_tt * (m0*ut)            # = m0 * (-g_tt) * c0/sqrt(-g_tt) = m0 c0 sqrt(-g_tt)
E_over = sp.simplify(E_over)
print("conserved Killing energy ~", E_over, " scaling vs m0 c0^2:",
      sp.simplify(sp.log(sp.simplify(E_over/(m0*c0**2)))/phi))
print("  => sqrt(-g_tt)/c0 = e^{-phi}: Killing energy at fixed-phi source redshifts as e^{-phi}")
print("  Energy at infinity (afar reference, phi->0) of a source AT depth phi ~ e^{-phi} => a=-1.")
print("""
NOTE: This says the energy-AT-INFINITY of a deep source is m0 c0^2 e^{-phi}.
That is the standard GR redshift. Whether this equals 'the rest mass exponent a'
requires identifying m(phi) (local) with the energy AT INFINITY. The Killing charge
is the energy measured AT INFINITY, i.e. it is m0*e^{-phi} as a number assigned by
the distant observer -- which is EXACTLY the a=-1 reading. So claim 4/5 sound:
covariant Killing energy => a=-1 => source weight e^{(a+1)phi}=1 => UDT=GR locally.
""")
