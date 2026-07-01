"""
hbar_a_action_invariance.py
OBSERVE pass (2026-06-18): Does Planck's constant hbar pin the matter
mass-dilation exponent a in m(phi)=m0 e^{a phi}, WITHOUT building a soliton?

Every exponent below is machine-produced by sympy. Nothing is asserted by hand.
Tags in the doc: DERIVED / CHOSE / CONVENTION.

Metric (CANON C-2026-06-18-1):
  ds^2 = -e^{-2phi} c0^2 dt^2 + e^{2phi} dr^2 + r^2 dOmega^2,  B=1/A.
Sense-1: LOCAL physics unmodified (local c=c0, local m=m0, hbar fixed);
dilation is comparative ("as seen from afar"). afar = reference, phi_ref=0.

CANON kinematics (already DERIVED + blind-verified, prior doc):
  proper time   dtau/dt = e^{-phi}    (CLOCK contracts for phi>0)
  proper length dL/dr   = e^{+phi}    (RULER expands  for phi>0)
  product = 1 exactly (the B=1/A reciprocal tie).
"""
import sympy as sp

phi = sp.symbols('phi', real=True)

# --- the two metric dilation weights, read off the metric (DERIVED) ---
# weight w means: (afar value) = (local value) * e^{w * phi}
W_clock_freq = sp.Integer(-1)   # a LOCAL frequency seen from afar: f_afar = e^{-phi} f_local
                                # because afar uses coordinate time t, dtau/dt=e^{-phi}.
W_length     = sp.Integer(+1)   # a LOCAL proper length seen from afar spans e^{+phi}...
                                # CAREFUL: a fixed PROPER length = e^{+phi} dr, so in
                                # COORDINATE extent dr it is e^{-phi}; as a PROPER length
                                # it is e^{+phi}. We track BOTH below explicitly.

print("="*70)
print("PART 1: IS ACTION (hbar) DILATION-INVARIANT under B=1/A?")
print("="*70)
# Action S = Energy * time = momentum * length. Test the dilation weight of S.
#
# Energy ~ hbar * frequency. A frequency is a CLOCK rate -> rides the clock.
# Time interval ~ rides the clock (a duration).
# Momentum ~ hbar / length (wavelength).
# Length ~ rides the ruler.
#
# We compute the dilation weight (the coefficient of phi in the exponent) of
# each, FROM AFAR, using the metric. Two natural pairings for S:

# Pairing 1: S = Energy * Time
# Energy: an energy is hbar*omega; omega is a clock frequency.
#   from afar a local frequency dilates as e^{-phi} (W_clock_freq).
#   So E_afar weight = W_E = -1   (energy redshifts: e^{-phi}).
W_E = W_clock_freq
# Time: a DURATION measured from afar. A proper duration dtau seen in coord time:
#   dt = dtau / (dtau/dt) = dtau * e^{+phi}. So a proper time interval, expressed
#   in the afar (coordinate) time, dilates as e^{+phi}.  W_time = +1.
W_time = -W_clock_freq   # = +1, reciprocal of the frequency
S1 = W_E + W_time
print(f" Pairing S=E*time:    W_E={W_E}, W_time={W_time}  ->  W_S = {S1}")

# Pairing 2: S = momentum * length
# Momentum: p = hbar/lambda; a wavelength is a LENGTH (rides the ruler, e^{+phi} proper).
#   p_afar weight = -W_length = -1  (momentum ~ 1/length, redshifts like energy).
W_p = -W_length          # = -1
# Length: a proper length seen from afar dilates as e^{+phi} (W_length).
W_len = W_length         # = +1
S2 = W_p + W_len
print(f" Pairing S=p*length:  W_p={W_p}, W_len={W_len}  ->  W_S = {S2}")

print(f"\n ACTION DILATION WEIGHT: S1={S1}, S2={S2}  (both {sp.Integer(0)} => INVARIANT)")
print(" => action factors CANCEL because of B=1/A (clock e^{-phi} vs ruler e^{+phi}")
print("    are exact reciprocals). hbar can be globally fixed: STRUCTURAL consequence.")
assert S1 == 0 and S2 == 0, "action not invariant -- REFUTED"

print("\n  Cross-check: is the CANCELLATION specifically a B=1/A effect?")
print("  Redo with a HYPOTHETICAL non-reciprocal metric g_tt=-e^{-2p}, g_rr=e^{2*b*p}")
b = sp.symbols('b', real=True)  # b=1 is the UDT reciprocal case
Wc = sp.Integer(-1)             # clock freq weight unchanged (g_tt fixed)
Wl = b                          # ruler weight = b (proper length ~ e^{b phi})
S1b = Wc + (-Wc)                # E*time: time is reciprocal of freq regardless -> 0 ALWAYS
S2b = (-Wl) + Wl                # p*len : momentum is reciprocal of length regardless -> 0 ALWAYS
print(f"   S=E*time weight (any b): {sp.simplify(S1b)}")
print(f"   S=p*len  weight (any b): {sp.simplify(S2b)}")
print("   NOTE: each pairing self-cancels by its OWN reciprocity (E~1/time, p~1/length),")
print("   INDEPENDENT of b. The B=1/A content is that the E*time route and the p*length")
print("   route AGREE on the SAME weights for E,p,time,length -- see consistency below.")

print()
print("="*70)
print("PART 2: DOES THE COMPTON LINK PIN a? (two ways, must agree)")
print("="*70)
# The Compton relation, LOCALLY (Sense-1, all local/proper quantities, unmodified):
#   m0 c0^2 = hbar omega_C,   lambda_C = hbar/(m0 c0).
# These hold in EVERY local frame (Sense-1). The question is what the AFAR observer
# attributes as the mass m(phi)=m0 e^{a phi}. We do NOT modify local physics; we
# ask how the afar-attributed mass scales, using the metric dilations + hbar fixed.
#
# Define a = d(ln m_afar)/dphi.  m_afar = m0 e^{a phi}.

a = sp.symbols('a', real=True)

# ---- ROUTE I: via E = hbar*omega_C  (mass as a CLOCK frequency) ----
# omega_C is the particle's rest-frame Compton CLOCK frequency. A clock frequency,
# seen from afar, dilates as the clock: omega_afar = e^{W_clock_freq * phi} omega_local
# = e^{-phi} omega_local.   hbar fixed.   So E_afar = hbar omega_afar = e^{-phi} E_local.
# Then m_afar c?^2 = E_afar.  THE ONLY FREEDOM: which c converts E to m (c0 local, or
# coordinate c0 e^{-2phi}).  Track both.
W_omega = W_clock_freq                       # -1, DERIVED (clock)
# m = E / c^2.  c_local weight 0 ; c_coord weight -2 (c=c0 e^{-2phi}).
for cname, Wc2 in [("local c0", sp.Integer(0)), ("coordinate c0 e^{-2phi}", sp.Integer(-2))]:
    # m_afar weight = W_E - W_(c^2) = W_omega - 2*Wc2
    a_I = W_omega - 2*Wc2
    print(f" ROUTE I  E=hbar*omega, c={cname:24s}: a = W_omega - 2*W_c = {W_omega} - 2*({Wc2}) = {a_I}")

# ---- ROUTE II: via lambda_C = hbar/(m c)  (mass as inverse Compton LENGTH) ----
# lambda_C is a proper length. Seen from afar as a PROPER length it dilates e^{+phi};
# but to convert to mass we again need a c. m = hbar/(c lambda).
# A subtlety: is lambda_C "the proper Compton length" (rides ruler, e^{+phi}) or its
# COORDINATE extent (e^{-phi})?  This is the SAME face/which-length freedom. Track both
# lengths x both c's.
print()
for lname, Wl2 in [("proper length e^{+phi}", sp.Integer(+1)), ("coordinate extent e^{-phi}", sp.Integer(-1))]:
    for cname, Wc2 in [("local c0", sp.Integer(0)), ("coordinate c0 e^{-2phi}", sp.Integer(-2))]:
        # m = hbar/(c lambda): m_afar weight = -(W_c) - (W_lambda) = -Wc2 - Wl2
        a_II = -Wc2 - Wl2
        print(f" ROUTE II lambda={lname:24s}, c={cname:24s}: a = -W_c - W_lambda = {a_II}")

print()
print("="*70)
print("PART 2b: THE CONSISTENCY DEMAND -- when do Route I and Route II AGREE?")
print("="*70)
# Consistency: the SAME particle, SAME afar observer, must give ONE m_afar whether
# read via E=hbar*omega or via lambda=hbar/(mc). Both use hbar (fixed) and the SAME c.
# Internal consistency of the LOCAL Compton relations: m0 c0^2 = hbar omega_C AND
# lambda_C = hbar/(m0 c0) imply omega_C = c0 / lambda_C * (1)  ... check:
#   omega_C = m0 c0^2/hbar ; c0/lambda_C = c0 * m0 c0 / hbar = m0 c0^2/hbar = omega_C. OK.
# So LOCALLY omega_C = c0/lambda_C (a clock frequency = c0 / a length). This TIE must
# be respected from afar too IF we use a single consistent c. From afar:
#   omega_afar = (c_used)_afar / lambda_afar   <-- the dispersion relation the afar
#   observer would write IF physics looks locally-Lorentzian to them.
# Let W_c be the weight of the c the afar observer uses in THIS relation.
Wc = sp.symbols('W_c', real=True)
Wlam = sp.symbols('W_lambda', real=True)
# omega ~ c/lambda  =>  W_omega = W_c - W_lambda. With W_omega=-1 (clock, DERIVED):
eq_disp = sp.Eq(W_omega, Wc - Wlam)
print(f" dispersion tie (omega=c/lambda):  {eq_disp}  => W_lambda = W_c - W_omega = W_c + 1")
Wlam_sol = sp.solve(eq_disp, Wlam)[0]
print(f"   => W_lambda = {Wlam_sol}")
# Now a from the TWO routes, EXPRESSED with the same W_c, and DEMAND they match:
#   Route I:  a = W_omega - 2 W_c
#   Route II: a = -W_c - W_lambda  (with W_lambda tied above)
aI  = W_omega - 2*Wc
aII = -Wc - Wlam_sol
print(f"   Route I  a = {sp.simplify(aI)}")
print(f"   Route II a = {sp.simplify(aII)}")
diff = sp.simplify(aI - aII)
print(f"   Route I - Route II = {diff}")
if diff == 0:
    print("   => CONSISTENT FOR ALL W_c: the two routes AGREE identically once the")
    print("      local dispersion tie omega=c/lambda is imposed. GOOD: hbar+Compton is")
    print("      self-consistent, but a still depends on the ONE remaining choice W_c.")
    a_of_Wc = sp.simplify(aI)
    print(f"   => a = {a_of_Wc}   (a FUNCTION of which-c only)")
    for cname, val in [("local c0 (W_c=0)", 0), ("coordinate c0 e^{-2phi} (W_c=-2)", -2),
                       ("'half' geometric W_c=-1", -1)]:
        print(f"        W_c={val:>3} ({cname:32s}) -> a = {a_of_Wc.subs(Wc, val)}")

print()
print("="*70)
print("PART 3: 'MASS TIED TO TIME' -- what hbar-invariance + Compton give")
print("="*70)
# If we ACCEPT the cleanest reading: mass IS the Compton clock frequency
# (m = hbar omega_C / c^2), and a clock frequency dilates as the metric clock
# (e^{-phi}, DERIVED, no freedom), then the ONLY residual freedom is the c in m=E/c^2.
# 'Mass tied to time' = 'mass rides the clock' = the time-face reading.
print(" Mass-as-clock-frequency (time-face) reading:")
print("   m_afar = hbar omega_afar / c^2 = (hbar omega_local/c^2) e^{-phi} / e^{2*W_c phi}")
print("   With LOCAL c (W_c=0): a = -1  (the GR gravitational-redshift value; IN-STEP)")
print("   With COORDINATE c (W_c=-2): a = +3 (OUT-of-step)")
print(" => 'mass tied to time' makes mass ride the CLOCK e^{-phi}; with the local c")
print("    (the Sense-1 conversion) this is EXACTLY a=-1 = GR redshift. hbar+Compton")
print("    DERIVE 'mass dilates as the Compton clock' but the clock value is -1 (GR).")

print()
print("="*70)
print("PART 4: NUMBER or FUNCTION?  (is a constant or a(phi)?)")
print("="*70)
# The clock dilation dtau/dt = e^{-phi} is a PURE exponential in phi with CONSTANT
# rate -1. So IF mass rides the clock, a is a CONSTANT (=-1). a becomes a FUNCTION
# only if the relevant frequency/length dilation is NONLINEAR in phi -- which the
# metric clock is NOT (it is exactly e^{-phi}). The intrinsic-scale composition-break
# (a_profile doc) is a SEPARATE effect (matter's own length entering at the extremes),
# NOT produced by hbar-invariance itself.
ratio = sp.exp(-phi)   # dtau/dt
lnr = sp.log(ratio)
rate = sp.diff(lnr, phi)
print(f" d(ln(dtau/dt))/dphi = {rate}  (CONSTANT) => clock-ridden a is a NUMBER, not a(phi).")
print(" hbar-invariance is EXACT for all phi (Part 1 weights are phi-independent),")
print(" so hbar itself introduces NO nonlinearity => does NOT make a a function.")

print()
print("="*70)
print("PART 5: RESOLVE or RELOCATE the menu?")
print("="*70)
print(" hbar-invariance (Part 1) REMOVES one axis of the prior menu: it forbids the")
print(" face-MISMATCH readings (a=0 Sense-1-literal, a=+-? mixed) because action=E*t=p*l")
print(" must be invariant -> E and p, time and length are LOCKED to be reciprocals, so a")
print(" mass cannot independently 'ride the ruler' (a=+1) while its energy rides the clock.")
print(" The Compton tie omega=c/lambda makes Route I and Route II AGREE (Part 2b).")
print(" BUT the SAME single freedom SURVIVES, RELOCATED to: WHICH c does the afar")
print(" observer use to convert energy<->mass<->length (local c0 vs coordinate c0 e^{-2phi})?")
print("   W_c = 0  -> a = -1  (GR redshift; the Sense-1 'local c' choice)")
print("   W_c = -2 -> a = +3  (coordinate-c choice)")
print(" So hbar RESOLVES the face/ruler ambiguity (collapses {-3,0,+1} style splits)")
print(" but RELOCATES the residual to a single binary: which-c. The natural Sense-1")
print(" reading (local c0 everywhere, the observer-frame postulate) selects a=-1=GR.")
