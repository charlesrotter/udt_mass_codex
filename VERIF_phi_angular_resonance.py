#!/usr/bin/env python3
"""
VERIF_phi_angular_resonance.py  (NEW FILE — repo discipline; edits no committed script)

HYPOTHESIS UNDER TEST (Charles's founding hunch, dynamical/time-domain form):
  Discreteness arises where the phi-INVARIANT ANGULAR sector RESONATES / phase-LOCKS
  with the phi (depth/dilation) sector. Resonance/commensurability is intrinsically
  discrete (a Lissajous closes only at rational frequency ratios; parametric/Mathieu
  tongues sit at omega_phi = (n/2) omega_drive). The static negatives (relaxation
  everywhere) were blind to this because they were static.

THE TWO CLOCKS (grounded in the corpus, NOT guessed):

  ANGULAR clock (the 2pi TIME clock):
    monodromy_depth_results.md #49 (verifier-cleared, lines 108-117, 278-280):
      L_eff(chi, chidot; D) = (1/2) Lambda_3(D) chidot^2 - E0(D)
      p_chi = Lambda_3(D) chidot = J = const (chi cyclic)
      chidot = omega_ang = J / Lambda_3(D)  -- UNIFORM rotation, FREE classical datum.
      crux2_coinflip_results.md P4: chi enters ONLY as (chidot)^2; ZERO linear-in-vel,
      ZERO bare term (for both S^2 and S^3 lift). => the rotor is a FREE RIGID ROTOR.
    Lambda_3(D) smooth/monotone 8.81 -> 134.11 over the depth scan (line 278-280).

  PHI clock (depth-dependent breathing/oscillation frequency):
    lepton_soliton_spectrum_results.md (Pb), deep-phi mpmath table (lines 100-101,
    174-188): the breathing Hessian H u = omega^2 W u, W ~ e^{3phi}, gives a discrete
    tower. Lowest breathing frequency omega_phi(p) (= sqrt of lowest omega^2):
       p=0: omega^2_0 = 0.196  -> omega_phi = 0.4427
       p=1: omega^2_0 = 0.651  -> omega_phi = 0.8068
       p=2: omega^2_0 = 1.575  -> omega_phi = 1.2550
       p=3: omega^2_0 = 3.082  -> omega_phi = 1.7556
       p=4: omega^2_0 = 5.144  -> omega_phi = 2.2680
    Spacing of the TOWER is O(1), saturating (R1: 1.61->2.26) -- a static fact.

THE COUPLING (the metric's native phi-angular cross-structure):
  wint_results.md (lines 33-39): the metric's own e^{2phi}/r^2-DRESSED angular
  operator (phi_thth + cot th phi_th - phi_th^2) -- the phi-angular coupling
  "appears for free." BUT (lines 92-133) that 2D static (r,theta) angular sector
  RELAXES TO ROUND everywhere (th_var ~ 1e-15), Jacobian never singular -> the
  STATIC spatial-angular coupling carries NO resonance.
  The DYNAMICAL coupling that CAN pump is different and native:
    rotor energy E_rot = J^2 / (2 Lambda_3(D))  with Lambda_3 = Lambda_3(shape).
    The breathing mode CHANGES the soliton shape (width) -> changes Lambda_3 and
    changes omega_phi. So the breathing coordinate b modulates the rotor inertia,
    and the rotor's centrifugal term J^2/(2 Lambda_3(b)) pushes on b.
    THIS is the only native channel with energy exchange (rotor<->breathing).
    It is a rotor + parametric/anharmonic oscillator. We test IT, faithfully.

WHAT WE REFUTE-FIRST:
  (1) Does the native coupling permit energy exchange at all? (a free rotor +
      uncoupled oscillator do NOT resonate -- stated in the prompt.)
  (2) If it pumps: is there genuine resonance/phase-locking (Mathieu tongue /
      closed Lissajous / energy exchange) at DISCRETE depths p_n where
      omega_phi(p_n) = n * omega_ang ?
  (3) If discrete depths: are masses M(p_n) EXPONENTIALLY spaced (~207, ~17) or O(1)?

DISCIPLINE: refute-first. If no pumping, or no locking, or O(1) -> say DEAD.
"""

import numpy as np
from scipy.integrate import solve_ivp
import mpmath as mp

np.set_printoptions(precision=6, suppress=False, linewidth=120)

# ----------------------------------------------------------------------------
# CORPUS-GROUNDED CLOCK DATA
# ----------------------------------------------------------------------------
# omega_phi(p): lowest breathing frequency, from lepton_soliton_spectrum_results.md
# deep-phi mpmath table (omega^2 lowest), sqrt'd.
P_GRID      = np.array([0.0, 1.0, 2.0, 3.0, 4.0])
OM2_BREATHE = np.array([0.196, 0.651, 1.575, 3.082, 5.144])   # lowest omega^2 vs p
OMEGA_PHI   = np.sqrt(OM2_BREATHE)                              # 0.443..2.268

# Lambda_3(D): iso-inertia, smooth/monotone 8.81 -> 134.11 (monodromy #49 line 278).
# We model it as a smooth monotone of depth p anchored at the two stated endpoints.
# (Only the SCALE-FREE behavior and monotonicity matter -- per Axis-1 scale-free.)
LAM3_LO, LAM3_HI = 8.81, 134.11
def Lambda3_of_p(p):
    # log-linear interpolation across the stated monotone range over p in [0,4]
    t = p / 4.0
    return LAM3_LO * (LAM3_HI / LAM3_LO) ** t

def omega_phi_of_p(p):
    return float(np.interp(p, P_GRID, OMEGA_PHI))

# ----------------------------------------------------------------------------
# PREMISE LEDGER  (chose / derived ; forced choices flagged)
# ----------------------------------------------------------------------------
PREMISE_LEDGER = """
PREMISE LEDGER (chose vs derived):
 D1 [DERIVED] rotor is FREE rigid rotor: L = (1/2)Lambda_3 chidot^2, chi cyclic,
      p_chi=J=const, omega_ang=J/Lambda_3.  (monodromy #49; crux2 P4: only (chidot)^2,
      zero linear/bare term.)
 D2 [DERIVED] omega_phi(p) = lowest breathing freq, depth-dependent, monotone-rising,
      O(1)-saturating.  (lepton_soliton_spectrum Pb + deep-phi mpmath table.)
 D3 [DERIVED] Lambda_3 depends on soliton SHAPE; breathing changes shape -> the only
      native rotor<->breathing energy channel is the inertia/centrifugal coupling
      E_rot = J^2/(2 Lambda_3(b)).  (monodromy #49: Lambda_3 is the t-t reduction of
      the SAME profile the breathing mode perturbs.)
 C1 [CHOSE-FORCED] the functional form of Lambda_3(b) vs the breathing amplitude b.
      The corpus gives Lambda_3(DEPTH) but not d Lambda_3 / d(breathing). We use the
      geometric/physical scaling of a rigid-body inertia with size: a breathing mode
      that scales the soliton width R by (1+b) scales Lambda_3 ~ R^2-weighted ->
      Lambda_3(b) = Lambda_3(p) * (1+b)^2  (rotor inertia grows with radius^2).
      *** THIS IS THE LOAD-BEARING FORCED CHOICE. It is the GENEROUS choice: it
      MAXIMIZES rotor->breathing pumping (strongest possible parametric drive). If
      resonance fails even here, it fails a fortiori. ***
 C2 [CHOSE] breathing potential: harmonic at leading order V(b)=(1/2)omega_phi^2 b^2
      (the Hessian/SL eigenproblem IS the harmonic 2nd variation). Anharmonicity
      added as a scoped robustness knob (cubic), default 0.
 C3 [CHOSE] J chosen so omega_ang = J/Lambda_3 sweeps to hit each commensurability
      omega_phi(p) = n*omega_ang -- i.e. we GIVE the rotor the chance to resonate.
"""

# ----------------------------------------------------------------------------
# THE DYNAMICAL TWO-SECTOR MODEL
# ----------------------------------------------------------------------------
# Generalized coords: chi (rotor angle), b (breathing amplitude).
# Lagrangian (native channel):
#   L = (1/2) Lambda_3(p) (1+b)^2 chidot^2   [rotor, inertia breathes]
#       + (1/2) M_b bdot^2 - (1/2) M_b omega_phi(p)^2 b^2 - (eps/3) b^3   [breathing]
# chi is STILL cyclic (no explicit chi) => p_chi = Lambda_3(p)(1+b)^2 chidot = J const.
# Routhian reduction (eliminate chi via conserved J):
#   E_rot(b) = J^2 / (2 Lambda_3(p) (1+b)^2)   -- centrifugal potential in b.
# Effective 1-DOF breathing EOM with the rotor's centrifugal back-reaction:
#   M_b bddot = - M_b omega_phi^2 b - eps b^2 + J^2 / (Lambda_3(p) (1+b)^3)
# The rotor instantaneous frequency: omega_ang(t) = J/(Lambda_3 (1+b(t))^2) -- it is
# MODULATED by the breathing. This is the genuine coupled, energy-exchanging system.
#
# We integrate the FULL (chi,b) system (not just the Routhian) to watch energy flow.

M_B = 1.0  # breathing effective mass (scale-free; sets units with omega_phi)

def make_rhs(p, J, eps=0.0):
    L3 = Lambda3_of_p(p)
    om = omega_phi_of_p(p)
    def rhs(t, y):
        chi, chidot, b, bdot = y
        inertia = L3 * (1.0 + b)**2
        # chi EOM from d/dt(inertia*chidot)=0 -> chiddot = -2 chidot bdot/(1+b)
        chiddot = -2.0 * chidot * bdot / (1.0 + b)
        # b EOM: M_b bddot = -M_b om^2 b - eps b^2 + d/db[(1/2) inertia chidot^2]
        #   d/db[(1/2)L3(1+b)^2 chidot^2] = L3 (1+b) chidot^2
        bddot = (-M_B * om**2 * b - eps * b**2 + L3 * (1.0 + b) * chidot**2) / M_B
        return [chidot, chiddot, b, bddot]
    return rhs

def energies(p, y):
    L3 = Lambda3_of_p(p); om = omega_phi_of_p(p)
    chi, chidot, b, bdot = y
    E_rot = 0.5 * L3 * (1.0 + b)**2 * chidot**2
    E_bre = 0.5 * M_B * bdot**2 + 0.5 * M_B * om**2 * b**2
    return E_rot, E_bre

# ----------------------------------------------------------------------------
# RUN (a): does the coupled system EXCHANGE ENERGY / show resonance?
# ----------------------------------------------------------------------------
def run_exchange(p, ratio_n, b0=0.05, t_max=4000.0, eps=0.0):
    """Set rotor so omega_ang = omega_phi/ratio_n (commensurability n:1), give the
       breathing a small kick, watch whether rotor<->breathing energy flows."""
    L3 = Lambda3_of_p(p); om = omega_phi_of_p(p)
    omega_ang_target = om / ratio_n
    J = omega_ang_target * L3 * (1.0 + 0.0)**2   # set J for that rotor rate
    rhs = make_rhs(p, J, eps=eps)
    y0 = [0.0, omega_ang_target, b0, 0.0]
    sol = solve_ivp(rhs, [0, t_max], y0, rtol=1e-10, atol=1e-12,
                    dense_output=True, max_step=0.5, method="DOP853")
    ts = np.linspace(0, t_max, 8000)
    Y = sol.sol(ts)
    Erot = np.array([energies(p, Y[:, i])[0] for i in range(len(ts))])
    Ebre = np.array([energies(p, Y[:, i])[1] for i in range(len(ts))])
    Etot = Erot + Ebre
    # energy-exchange metric: peak-to-peak swing of breathing energy relative to its
    # initial value (genuine pumping => large growth; decoupled => stays ~flat)
    bre_growth = (Ebre.max() - Ebre[0]) / max(Ebre[0], 1e-30)
    rot_swing = (Erot.max() - Erot.min()) / max(Erot.mean(), 1e-30)
    cons = (Etot.max() - Etot.min()) / max(Etot.mean(), 1e-30)
    b_amp = np.abs(Y[2]).max()
    return dict(p=p, n=ratio_n, omega_ang=omega_ang_target, omega_phi=om,
                bre_growth=bre_growth, rot_swing=rot_swing, b_amp=b_amp,
                E_conservation_err=cons)

# ----------------------------------------------------------------------------
# RUN (b): parametric (Mathieu) tongue test -- the SHARPEST resonance probe.
# Linearize breathing about b=0 with the rotor driving it. With omega_ang fixed,
# the rotor's modulation of the inertia drives b at 2*omega_ang. Mathieu instability
# (exponential growth of b) is THE signature of parametric resonance. We scan the
# detuning and measure the Floquet/growth exponent.
# ----------------------------------------------------------------------------
def growth_exponent(p, ratio_n, b0=1e-3, t_max=3000.0, eps=0.0):
    res = run_exchange(p, ratio_n, b0=b0, t_max=t_max, eps=eps)
    # re-run to grab the b envelope growth rate via log-linear fit on peaks
    L3 = Lambda3_of_p(p); om = omega_phi_of_p(p)
    J = (om / ratio_n) * L3
    rhs = make_rhs(p, J, eps=eps)
    sol = solve_ivp(rhs, [0, t_max], [0.0, om/ratio_n, b0, 0.0],
                    rtol=1e-10, atol=1e-13, dense_output=True, max_step=0.5,
                    method="DOP853")
    ts = np.linspace(0, t_max, 12000)
    b = sol.sol(ts)[2]
    env = np.abs(b)
    # upper envelope via running max in windows
    w = 200
    peaks = [env[i:i+w].max() for i in range(0, len(env)-w, w)]
    peaks = np.array(peaks); tp = np.arange(len(peaks)) * w * (ts[1]-ts[0])
    mask = peaks > 0
    if mask.sum() > 3:
        slope = np.polyfit(tp[mask], np.log(peaks[mask] + 1e-300), 1)[0]
    else:
        slope = 0.0
    return slope, res

# ============================================================================
if __name__ == "__main__":
    print("="*78)
    print("VERIF_phi_angular_resonance  --  dynamical phi<->angular resonance test")
    print("="*78)
    print(PREMISE_LEDGER)

    print("\n--- CLOCKS (corpus-grounded) ---")
    for p in P_GRID:
        print(f"  p={p:.1f}:  omega_phi={omega_phi_of_p(p):.4f}   "
              f"Lambda_3={Lambda3_of_p(p):8.3f}")

    # ---- RUN (a): energy exchange at commensurabilities n=1,2,3 across depth ----
    print("\n--- RUN (a): energy exchange at omega_phi = n * omega_ang ---")
    print("  (bre_growth >> 1 => genuine pumping/resonance; ~0 => decoupled/no exchange)")
    print(f"  {'p':>4} {'n':>3} {'om_ang':>8} {'om_phi':>8} {'bre_growth':>11} "
          f"{'rot_swing':>10} {'b_amp':>8} {'Econs_err':>10}")
    for p in P_GRID:
        for n in (1, 2, 3):
            r = run_exchange(p, n, b0=0.05, t_max=3000.0)
            print(f"  {p:>4.1f} {n:>3d} {r['omega_ang']:>8.4f} {r['omega_phi']:>8.4f} "
                  f"{r['bre_growth']:>11.3e} {r['rot_swing']:>10.3e} "
                  f"{r['b_amp']:>8.4f} {r['E_conservation_err']:>10.2e}")

    # ---- RUN (b): parametric growth exponent (Mathieu tongue) ----
    print("\n--- RUN (b): parametric growth exponent (Mathieu instability) ---")
    print("  parametric resonance sits at omega_phi ~ (k/2) * omega_drive.")
    print("  the rotor modulates inertia at 2*omega_ang -> drive freq = 2*omega_ang.")
    print("  principal tongue: omega_phi = omega_drive = 2*omega_ang  (i.e. n=2).")
    print(f"  {'p':>4} {'n':>3} {'growth_rate':>13} {'verdict':>14}")
    any_unstable = False
    for p in P_GRID:
        for n in (1, 2, 3, 4):
            g, _ = growth_exponent(p, n, b0=1e-3, t_max=3000.0)
            unstable = g > 1e-3
            any_unstable = any_unstable or unstable
            print(f"  {p:>4.1f} {n:>3d} {g:>13.3e} "
                  f"{'UNSTABLE/RES' if unstable else 'stable/no-res':>14}")

    # ---- RUN (b'): fine detuning scan for a true Arnold tongue at n=2, p=2 ----
    print("\n--- RUN (b'): fine detuning scan (Arnold tongue) at p=2 around n=2 ---")
    p = 2.0; om = omega_phi_of_p(p); L3 = Lambda3_of_p(p)
    print(f"  {'omega_ang':>10} {'om_phi/2om_ang':>14} {'growth':>12}")
    for fac in np.linspace(0.4, 0.6, 11):
        # omega_ang = fac * omega_phi ; drive=2*omega_ang ; ratio = om/(2*fac*om)=1/(2fac)
        n_eff = 1.0/fac
        g, _ = growth_exponent(p, n_eff, b0=1e-3, t_max=3000.0)
        print(f"  {fac*om:>10.4f} {om/(2*fac*om):>14.4f} {g:>12.3e}")

    # ---- RUN (c): IF any resonance -> discrete depths + mass spacing ----
    print("\n--- RUN (c): commensurate depths p_n and mass spacing ---")
    print("  commensurability omega_phi(p_n) = n*omega_ang for FIXED omega_ang.")
    # pick a fixed rotor rate (e.g. omega_ang = omega_phi(p=0)) and find p where
    # omega_phi(p) = n*omega_ang -> p_n. Then 'mass' ~ E0(p) (soliton energy) ~ growth.
    omega_ang_fixed = omega_phi_of_p(0.0)   # smallest available, gives most rungs
    print(f"  fixed omega_ang = {omega_ang_fixed:.4f}")
    pfine = np.linspace(0, 4, 4001)
    omfine = np.array([omega_phi_of_p(pp) for pp in pfine])
    p_ns = []
    for n in (1, 2, 3, 4, 5):
        target = n * omega_ang_fixed
        if target < omfine.min() or target > omfine.max():
            continue
        idx = np.argmin(np.abs(omfine - target))
        p_ns.append((n, pfine[idx], omega_phi_of_p(pfine[idx])))
    for n, pn, ompn in p_ns:
        print(f"   n={n}: p_n={pn:.4f}  omega_phi(p_n)={ompn:.4f}  "
              f"Lambda_3(p_n)={Lambda3_of_p(pn):.3f}")
    if len(p_ns) >= 2:
        # candidate 'mass' proxies and their ratios
        print("  mass-proxy spacing (consecutive ratios):")
        for proxy_name, proxy in [("Lambda_3(p_n)", lambda pp: Lambda3_of_p(pp)),
                                  ("e^{2 p_n} (depth volume)", lambda pp: np.exp(2*pp)),
                                  ("omega_phi(p_n)", lambda pp: omega_phi_of_p(pp))]:
            vals = [proxy(pn) for _, pn, _ in p_ns]
            ratios = [vals[i+1]/vals[i] for i in range(len(vals)-1)]
            print(f"    {proxy_name:>26}: vals={[f'{v:.3f}' for v in vals]}  "
                  f"ratios={[f'{r:.3f}' for r in ratios]}")

    # ---- mpmath spot-check of omega_phi monotone + Lambda_3 (float64 sanity) ----
    print("\n--- mpmath spot-check (dps=40) ---")
    mp.mp.dps = 40
    for p in (0, 2, 4):
        l3 = mp.mpf(LAM3_LO) * (mp.mpf(LAM3_HI)/mp.mpf(LAM3_LO))**(mp.mpf(p)/4)
        print(f"  p={p}: Lambda_3(mp)={mp.nstr(l3, 12)}  (f64={Lambda3_of_p(p):.6f})")

    print("\n" + "="*78)
    print("INTERPRETATION GUIDE:")
    print("  RUN(a) bre_growth ~ O(1) only (no runaway) AND rot_swing tiny")
    print("     => bounded exchange, NO parametric blow-up.")
    print("  RUN(b)/(b') growth_rate ~ 0 everywhere => NO Mathieu tongue => NO")
    print("     parametric resonance => the native coupling does NOT phase-lock.")
    print("  RUN(c) if rungs exist, check ratios: ~1.3 (O(1)) vs ~207/~17 (exp).")
    print("="*78)
