"""
BLIND adversarial re-derivation of the mass-dilation exponent `a`.
Independent sympy work; NO author script reused. Data-blind.
Metric: g_tt = -e^{-2phi} c0^2, g_rr = e^{2phi}  (CANON C-2026-06-18-1, B=1/A).
"""
import sympy as sp

phi, c0, hbar, m0, t, r = sp.symbols('phi c0 hbar m0 t r', real=True, positive=True)

# ---------------------------------------------------------------
# CLAIM 1: sign-careful kinematics off the metric
# ---------------------------------------------------------------
g_tt = -sp.exp(-2*phi)*c0**2
g_rr = sp.exp(2*phi)

# Static clock: proper time per coordinate time = sqrt(-g_tt)/c0
dtau_dt = sp.sqrt(-g_tt)/c0
dtau_dt = sp.simplify(dtau_dt)
# Static ruler: proper length per coordinate length = sqrt(g_rr)
dL_dr = sp.sqrt(g_rr)
dL_dr = sp.simplify(dL_dr)
print("K1  dtau/dt =", dtau_dt, "   (expect e^{-phi})")
print("K1  dL/dr   =", dL_dr, "   (expect e^{+phi})")
print("    product clock*ruler =", sp.simplify(dtau_dt*dL_dr), " (reciprocal => 1)")

# coordinate null speed
v_coord = sp.sqrt(-g_tt/g_rr)
print("    coord null speed dr/dt =", sp.simplify(v_coord), " (expect c0 e^{-2phi})")

# ---------------------------------------------------------------
# CLAIM 1/2: Route A (clock/energy redshift) and Route B (ruler/Compton)
# Sense-1: local c=c0, local m=m0, hbar fixed.
# ---------------------------------------------------------------
print("\n--- Route A: clock/energy redshift ---")
# local oscillator freq f_local; afar frequency uses dtau/dt
f_local = sp.symbols('f_local', positive=True)
f_afar = dtau_dt * f_local          # e^{-phi} f_local
E_afar = hbar*f_afar
# mass via local c0:  m = E/c0^2,  m0 := hbar f_local/c0^2
m_afar_A = E_afar/c0**2
m_afar_A = m_afar_A.subs(hbar*f_local/c0**2, m0)
m_afar_A = sp.simplify(hbar*f_local/c0**2 * dtau_dt)
print("  m_afar(A) = (hbar f_local/c0^2) *", dtau_dt, "  => exponent a =",
      sp.simplify(sp.log(dtau_dt)/phi))

print("\n--- Route B: ruler/Compton length ---")
# proper Compton length lambda_C = hbar/(m0 c0) is a fixed LOCAL invariant.
lam_C = hbar/(m0*c0)
# Seen from afar: a fixed PROPER length spans coordinate extent dr = lam_C / (dL/dr)
#   because dL = (dL/dr) dr  =>  dr = dL/(dL/dr) = lam_C * e^{-phi}
dr_span = lam_C / dL_dr
# Re-read as the distant observer's own proper length (ref, phi=0 => factor 1) and invert
# m = hbar/(c0 * lambda) with local c0
m_afar_B = hbar/(c0*dr_span)
m_afar_B = sp.simplify(m_afar_B)
print("  coord extent of Compton length =", sp.simplify(dr_span))
print("  m_afar(B) =", m_afar_B, "  => exponent a =",
      sp.simplify(sp.log(m_afar_B/m0)/phi))

print("\n  gap m_afar(B)/m_afar(A):",
      sp.simplify((m_afar_B)/(hbar*f_local/c0**2*dtau_dt).subs(hbar*f_local/c0**2, m0)))

# ---------------------------------------------------------------
# CLAIM 1: enumerate the menu (face) x (which c)
# face = clock (e^{-phi} freq) or ruler (e^{+phi} proper length)
# which c for length<->mass conversion: local c0, or coordinate c0 e^{-2phi}
# ---------------------------------------------------------------
print("\n--- menu enumeration ---")
c_local = c0
c_coord = c0*sp.exp(-2*phi)

# Build mass from clock energy E=hbar f_afar, m = E/c^2
for cname, cc in [("local c0", c_local), ("coord c0 e^{-2phi}", c_coord)]:
    m_clk = hbar*f_afar/cc**2
    a_val = sp.simplify(sp.log(sp.simplify(m_clk/(hbar*f_local/c0**2)))/phi)
    print(f"  clock-energy / ({cname})^2 : a = {a_val}")

# Build mass from Compton ruler m = hbar/(c * lambda_coord), lambda_coord = lam_C e^{-phi}
lam_coord = lam_C*sp.exp(-phi)
for cname, cc in [("local c0", c_local), ("coord c0 e^{-2phi}", c_coord)]:
    m_rul = hbar/(cc*lam_coord)
    a_val = sp.simplify(sp.log(sp.simplify(m_rul/m0))/phi)
    print(f"  hbar/({cname} * lambda_coord) : a = {a_val}")

# clock-energy times proper 3-volume e^{-2phi}? (the inline -3 guess)
m_vol = (hbar*f_afar/c0**2)*sp.exp(-2*phi)
print("  clock-energy * proper-3-vol e^{-2phi}: a =",
      sp.simplify(sp.log(sp.simplify(m_vol/(hbar*f_local/c0**2)))/phi))
# geometric mean of clock & ruler
gm = sp.sqrt(dtau_dt*dL_dr)
print("  geometric mean of clock & ruler: factor =", sp.simplify(gm), " a = 0")

# ---------------------------------------------------------------
# CLAIM 1/2: light-cone collapse - cross Compton length at COORDINATE speed
# ---------------------------------------------------------------
print("\n--- light-cone build (cross proper Compton length at coord speed) ---")
# proper Compton length lam_C; its coordinate extent dr = lam_C e^{-phi}
# period = dr / v_coord ; freq seen afar?
period_coord = dr_span / v_coord
print("  coord crossing period =", sp.simplify(period_coord))
# proper period = period_coord * dtau/dt
period_proper = period_coord*dtau_dt
print("  proper period scales as", sp.simplify(period_proper/(lam_C/c0)),
      "=> freq ~", sp.simplify((lam_C/c0)/period_proper))
f_lc = 1/period_proper
m_lc = hbar*sp.simplify(f_lc/(lam_C/c0))/c0**2  # crude check of scaling
print("  light-cone freq exponent in e^{?phi}:",
      sp.simplify(sp.log(sp.simplify(f_lc/(c0/lam_C)))/phi))

# ---------------------------------------------------------------
# CLAIM 3: field kinetic vs angular phi-scaling under weight e^{(a+1)phi}
# rho = (xi/2)(X+2Y) + (kap/2)(2XY+Y^2),  X=e^{-2phi}Theta'^2, Y=sin^2 T / r^2
# ---------------------------------------------------------------
print("\n--- CLAIM 3: field sector scaling ---")
a = sp.symbols('a', real=True)
p = sp.symbols('p', real=True)  # uniform depth
# isolate phi-scaling: X carries e^{-2phi}, Y carries e^0
X_scale = sp.exp(-2*p)
Y_scale = sp.exp(0*p)
weight = sp.exp((a+1)*p)
kin_scale = sp.simplify(weight*X_scale)      # e^{(a-1)p}
ang_scale = sp.simplify(weight*Y_scale)      # e^{(a+1)p}
print("  kinetic (X-built) under weight: ", kin_scale, " exponent:", sp.simplify(sp.log(kin_scale)/p))
print("  angular (Y-built) under weight: ", ang_scale, " exponent:", sp.simplify(sp.log(ang_scale)/p))
print("  ratio kinetic/angular =", sp.simplify(kin_scale/ang_scale), " (expect e^{-2p})")
print("  with a=-1: kinetic exponent", sp.simplify(sp.log(kin_scale.subs(a,-1))/p),
      " => a_eff = -3 weight e^{-2phi}")

# ---------------------------------------------------------------
# CLAIM 4/5: Killing/Komar energy at infinity scaling
# Conserved energy of timelike Killing vector for static metric:
# E = -p_t = -m g_tt u^t ... for a static particle, energy at infinity
# E_inf = m_local * sqrt(-g_tt)/c0  (the redshift of rest energy)
# ---------------------------------------------------------------
print("\n--- CLAIM 4: Killing energy scaling (static particle) ---")
# A static particle at phi has local rest energy m0 c0^2. Conserved Killing energy
# E = m0 c0^2 * sqrt(-g_tt)/c0  (Wald: E = -g_tt u^t for normalized u; redshift factor)
# sqrt(-g_tt)/c0 = e^{-phi}
E_killing_factor = sp.simplify(sp.sqrt(-g_tt)/c0)
print("  Killing redshift factor sqrt(-g_tt)/c0 =", E_killing_factor,
      " => energy-at-infinity ~ e^{-phi}, a=-1")
