#!/usr/bin/env python3
"""
VERIF_phi_angular_resonance2.py  (NEW FILE -- corrected, rigorous resonance test)

WHY A SECOND SCRIPT (refute-first self-correction):
  v1's RUN(a)/(b) gave bre_growth ~ 1e+223 and a UNIFORM growth_rate ~ 1.3e-2 at
  EVERY (p,n) -- including off-resonance n=1,3,4 -- and FLAT across the entire
  detuning scan (RUN b'). A genuine Arnold/Mathieu tongue grows ONLY in a narrow
  detuning band and is ZERO outside it. Uniform nonzero "growth" independent of
  detuning is a NUMERICAL ARTIFACT (secular drift of a generic anharmonic system +
  a crude envelope fit), NOT parametric resonance. v1 ALSO let b run to ~1e50,
  violating the small-amplitude regime in which the harmonic breathing model is
  even defined.

  This script does the test PROPERLY:
   (1) FLOQUET analysis of the LINEARIZED breathing equation with the rotor as an
       exact periodic parametric drive. The drive is periodic because the rotor,
       once b is small, modulates omega_phi^2 sinusoidally. The Floquet multiplier
       |mu| > 1 <=> parametric instability <=> resonance. This is the unambiguous,
       detuning-SHARP signature. Scan the drive frequency to MAP the tongue.
   (2) A proper Mathieu reduction: the canonical resonance test. Build the Mathieu
       parameters (a, q) the native coupling actually produces and read the tongue
       structure from the exact stability chart.
   (3) Control: an EXACTLY decoupled run (zero coupling) to confirm the method
       reports NO growth when there is no coupling.

THE LINEARIZED COUPLED SYSTEM (small breathing b, rotor as drive):
  rotor (cyclic, J conserved): omega_ang(t) = J / (L3 (1+b)^2) ~ omega0 (1 - 2b).
  breathing EOM (from v1, linearized about b=0, keep O(b)):
     bddot = -om_phi^2 b + (L3/M_b)(1+b) chidot^2
           ~ -om_phi^2 b + (L3/M_b) chidot^2 (1 + b)
  with chidot^2 = omega_ang^2 = (J/L3)^2 (1+b)^{-4} ~ (J/L3)^2 (1 - 4 b).
  Equilibrium b* shifts (centrifugal stretch); expand b = b* + u:
     uddot = -[om_phi^2 + 3 (J^2/L3) (1+b*)^{-4} - ... ] u  + DRIVE.
  The TIME-DEPENDENCE (parametric drive) enters because the rotor angle chi(t)
  advances and any non-axisymmetric residual makes the effective stiffness
  oscillate at the rotor frequency Omega_d = omega_ang. We model the canonical
  parametric form:  uddot + [a + 2 q cos(Omega_d t)] u = 0  (Mathieu),
  with a = om_phi^2 (breathing stiffness), and q = parametric depth set by the
  rotor-breathing coupling strength (centrifugal modulation amplitude).

  q (DERIVED magnitude): the rotor energy J^2/(2 L3 (1+b)^2) modulates the breathing
  stiffness; its fractional modulation at the rotor period is
     q ~ (rotor energy) / (breathing stiffness scale) * (coupling) .
  We compute q from the native numbers and ALSO scan q to map where ANY tongue
  would sit, then ask whether the NATIVE q reaches it.
"""

import numpy as np
from scipy.integrate import solve_ivp
import mpmath as mp

P_GRID      = np.array([0.0, 1.0, 2.0, 3.0, 4.0])
OM2_BREATHE = np.array([0.196, 0.651, 1.575, 3.082, 5.144])
OMEGA_PHI   = np.sqrt(OM2_BREATHE)
LAM3_LO, LAM3_HI = 8.81, 134.11
def Lambda3_of_p(p): return LAM3_LO*(LAM3_HI/LAM3_LO)**(p/4.0)
def omega_phi_of_p(p): return float(np.interp(p, P_GRID, OMEGA_PHI))

# ---------------------------------------------------------------------------
# (1) EXACT FLOQUET of the Mathieu equation  u'' + [a + 2 q cos(Om t)] u = 0
#     |mu|>1 => parametric instability (resonance). Maps the Arnold tongues.
# ---------------------------------------------------------------------------
def floquet_max_multiplier(a, q, Om):
    """Return max|Floquet multiplier| over one drive period T=2pi/Om."""
    if Om <= 0: return 1.0
    T = 2*np.pi/Om
    def rhs(t, y):
        u, v = y
        return [v, -(a + 2*q*np.cos(Om*t))*u]
    # propagate the two fundamental solutions
    M = np.zeros((2,2))
    for j,(u0,v0) in enumerate([(1.0,0.0),(0.0,1.0)]):
        sol = solve_ivp(rhs, [0,T], [u0,v0], rtol=1e-11, atol=1e-13,
                        method="DOP853", max_step=T/200)
        M[:,j] = sol.y[:,-1]
    ev = np.linalg.eigvals(M)
    return float(np.max(np.abs(ev)))

# ---------------------------------------------------------------------------
# native q at each depth: fractional modulation of breathing stiffness by the
# rotor. From bddot = -om^2 b + (L3/M_b) chidot^2 (1+b), the b-linear coupling
# to the rotor centrifugal term gives an effective parametric coefficient.
# We take the rotor at a chosen rate omega_ang; the centrifugal term is
# C = (L3/M_b) omega_ang^2 ; its modulation when the rotor frequency varies as
# the breathing changes inertia gives q_native = 2 C / om^2  (the fractional
# stiffness change per unit b, times the drive amplitude). We compute it and
# ALSO scan q independently to find the tongue thresholds.
# ---------------------------------------------------------------------------
def native_q(p, omega_ang, M_b=1.0):
    L3 = Lambda3_of_p(p); om = omega_phi_of_p(p)
    C = (L3/M_b)*omega_ang**2          # centrifugal stiffness contribution
    return 2.0*C/om**2                 # fractional parametric depth

if __name__ == "__main__":
    print("="*78)
    print("VERIF_phi_angular_resonance2 -- rigorous Floquet/Mathieu resonance test")
    print("="*78)

    # ---- CONTROL: q=0 must give |mu|=1 (no growth) at every detuning ----
    print("\n--- CONTROL (q=0, no coupling): must report |mu|=1 (no resonance) ---")
    for Om in [0.5, 1.0, 1.5, 2.0]:
        mu = floquet_max_multiplier(a=1.0, q=0.0, Om=Om)
        print(f"  Om={Om:.2f}:  |mu|_max = {mu:.6f}  "
              f"({'OK no-growth' if abs(mu-1)<1e-4 else 'METHOD BUG'})")

    # ---- MAP the principal Mathieu tongue: a=om^2 fixed, scan Om at small q ----
    # principal parametric resonance: Om = 2 sqrt(a) (drive at twice nat. freq).
    print("\n--- Arnold-tongue map: a=1 (om=1), small q=0.1, scan drive Om ---")
    print("   the principal tongue MUST sit at Om = 2*sqrt(a) = 2.0, ZERO elsewhere")
    print(f"   {'Om':>6} {'|mu|_max':>10} {'in-tongue':>10}")
    for Om in np.linspace(1.4, 2.6, 13):
        mu = floquet_max_multiplier(a=1.0, q=0.1, Om=Om)
        print(f"   {Om:>6.3f} {mu:>10.5f} {'YES' if mu>1.0001 else 'no':>10}")

    # ---- NATIVE q: does the real coupling reach the tongue, at commensurability? ----
    print("\n--- NATIVE coupling depth q at commensurability omega_phi=n*omega_ang ---")
    print("   parametric drive freq = omega_ang (rotor). principal tongue needs")
    print("   omega_ang = 2*omega_phi (n=1/2) OR omega_phi=2*omega_ang (n=2).")
    print(f"   {'p':>4} {'n':>3} {'om_phi':>8} {'om_ang':>8} {'q_native':>10} "
          f"{'Om_d':>7} {'|mu|_max':>10} {'RES?':>6}")
    native_resonance_found = False
    for p in P_GRID:
        om = omega_phi_of_p(p)
        for n in (1, 2, 3):
            omega_ang = om/n
            q = native_q(p, omega_ang)
            a = om**2
            Om_d = omega_ang                       # rotor drives at its own freq
            mu = floquet_max_multiplier(a=a, q=q, Om=Om_d)
            res = mu > 1.0001
            native_resonance_found = native_resonance_found or res
            print(f"   {p:>4.1f} {n:>3d} {om:>8.4f} {omega_ang:>8.4f} {q:>10.3f} "
                  f"{Om_d:>7.4f} {mu:>10.5f} {'YES' if res else 'no':>6}")
    # also drive at 2*omega_ang (inertia modulated twice per rotor turn)
    print("\n   [same, but drive at 2*omega_ang (inertia ~ (1+b)^2 -> 2/turn)]")
    print(f"   {'p':>4} {'n':>3} {'om_phi':>8} {'om_ang':>8} {'q_native':>10} "
          f"{'Om_d':>7} {'|mu|_max':>10} {'RES?':>6}")
    for p in P_GRID:
        om = omega_phi_of_p(p)
        for n in (1, 2, 3):
            omega_ang = om/n
            q = native_q(p, omega_ang)
            a = om**2
            Om_d = 2*omega_ang
            mu = floquet_max_multiplier(a=a, q=q, Om=Om_d)
            res = mu > 1.0001
            native_resonance_found = native_resonance_found or res
            print(f"   {p:>4.1f} {n:>3d} {om:>8.4f} {omega_ang:>8.4f} {q:>10.3f} "
                  f"{Om_d:>7.4f} {mu:>10.5f} {'YES' if res else 'no':>6}")

    # ---- discreteness check: IF resonance, are the rungs exp or O(1)? ----
    print("\n--- discreteness/spacing (from v1 RUN c, recomputed cleanly) ---")
    omega_ang_fixed = omega_phi_of_p(0.0)
    pfine = np.linspace(0,4,8001); omf = np.array([omega_phi_of_p(x) for x in pfine])
    rungs=[]
    for n in (1,2,3,4,5):
        tgt=n*omega_ang_fixed
        if omf.min()<=tgt<=omf.max():
            pn=pfine[np.argmin(np.abs(omf-tgt))]; rungs.append((n,pn))
    soliton_mass = lambda pp: 45.607*np.exp(0)  # base; mass scale O(1) per corpus
    print("   commensurate depths p_n and Lambda_3 (mass-like) ratios:")
    L3vals=[Lambda3_of_p(pn) for _,pn in rungs]
    print("    p_n     =", [f"{pn:.3f}" for _,pn in rungs])
    print("    L3(p_n) =", [f"{v:.2f}" for v in L3vals])
    print("    ratios  =", [f"{L3vals[i+1]/L3vals[i]:.3f}" for i in range(len(L3vals)-1)])
    print("    (lepton target ratios would be ~207, ~17; O(1)~1.3-2 = NOT lepton)")

    print("\n" + "="*78)
    print("VERDICT LOGIC:")
    print(" - CONTROL q=0 -> |mu|=1 confirms the method has no false-positive.")
    print(" - tongue map -> nonzero growth ONLY near Om=2 confirms it detects real")
    print("   parametric resonance sharply (unlike v1's uniform artifact).")
    print(" - NATIVE q rows: if all |mu|~1 -> the real coupling is too weak / wrong")
    print("   frequency -> NO native parametric resonance -> hypothesis DEAD.")
    print(" - if some YES: read spacing (O(1) vs exp) for the final verdict.")
    print("="*78)
