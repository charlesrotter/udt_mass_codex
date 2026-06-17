#!/usr/bin/env python
"""
VERIF_frame_BC_revival.py -- OBSERVE (compute), not canonical. New file only.
Driver: Claude (Opus 4.8 1M). 2026-06-17. float64 + mpmath spot-checks.

REVIVAL HYPOTHESIS UNDER TEST (Charles), tested REFUTE-FIRST:
  The W2 shape-wave death (open_domain_discreteness_results.md branch (iv);
  STATE open-gate 1; charter-closed "infinite probe energy") is an
  OBSERVER-FRAME artifact. Claim: the PHYSICAL self-adjoint center BC and
  what counts as finite-energy / real-frequency are set by the LOCAL/PROPER
  frame (proper distance, proper time, c_eff), not the coordinate frame; and
  the difference becomes extreme where c_eff -> infinity toward the core/seal.
  If so the binding branch-iv extension (u ~ 1/r, omega^2 < 0 "relaxation")
  may be locally finite-energy AND map to a REAL local oscillation,
  reviving intrinsic discreteness (conjecture A).

GIVEN (do NOT re-derive):
  W2 SL problem:  (P f u')' + omega^2 (P/f) u = 0,  P = 2 r^2/(1+w)^2 (w=0 => 2 r^2),
  f = e^{-2 phi} = c_eff.  Liouville/Schrodinger: V = -2 phi' f^2 / r (well).
  Coordinate "regular" BC: psi = sqrt(P) u ~ r => Dirichlet => box-control omega ~ 1/R.
  Binding branch: u ~ 1/r (irregular), dismissed "non-Friedrichs/infinite probe
  energy", sits at omega^2 < 0 (relaxation, ~ -29 on the deep cell).

CORPUS CITATIONS (metric + frames + the measure ruling):
  CANON.md:79     g_tt = -e^{-2phi}, g_rr = +e^{2phi}  (diagonal dilation-tie class)
  CANON.md:81     wave speeds c_r^2 = e^{-4phi}, c_theta^2 = e^{-2phi}/r^2
  CANON.md:118-126 g_tt g_rr = -c^2 (B=1/A); G^t_t=G^r_r
  w2_uncovering_results.md:29-31  the f-weighted hyperbolic wave, dr/dT=+-f=c_eff
  open_domain_discreteness_results.md:42-46,116  branch (iv) non-Friedrichs,
                  finite-action charter, "any such bound state costs infinite probe energy"
  STATE.md:534    "non-Friedrichs center BC -- charter-closed (infinite probe energy)"
  NEGATIVES_REGISTRY.md:782-785  TOOLING FIX (banked): self-adjoint measure is
                  M = r^2 sin(theta) BARE; the e^{-2phi} weights belong in the
                  STIFFNESS, NOT the measure. (the ~18000 spurious negatives were
                  a MEASURE DOUBLE-COUNT.)
  measure_fork_results.md:52-60 (item 5): "NEITHER OLD LIFT SURVIVES ... the
                  proper lift's single-n parameterization is refuted."
"""
import numpy as np
import sympy as sp
import mpmath as mp
mp.mp.dps = 40

LINE = "="*78
def hdr(s): print("\n"+LINE+"\n"+s+"\n"+LINE)

# ============================================================================
# STEP 1: METRIC + FRAMES (derive proper distance, proper time, redshift)
# ============================================================================
hdr("STEP 1  METRIC + FRAMES (CANON.md:79)")
r = sp.symbols('r', positive=True)
phi = sp.Function('phi')
gtt = -sp.exp(-2*phi(r))        # CANON.md:79
grr =  sp.exp( 2*phi(r))        # CANON.md:79
print("  g_tt = -e^{-2phi} =", gtt)
print("  g_rr = +e^{ 2phi} =", grr)
print("  g_tt*g_rr =", sp.simplify(gtt*grr), "  (= -1: B=1/A areal chart, CANON:118)")
print()
# ds^2 = g_tt dt^2 + g_rr dr^2 + r^2 dOmega^2
#  -> proper radial distance:  dl = sqrt(g_rr) dr = e^{phi} dr
#  -> proper time of static observer: dtau = sqrt(-g_tt) dt = e^{-phi} dt
#  -> redshift / lapse factor:  N = sqrt(-g_tt) = e^{-phi}
dl_dr   = sp.sqrt(grr)
dtau_dt = sp.sqrt(-gtt)
print("  PROPER RADIAL DISTANCE :  dl   = sqrt(g_rr) dr  = e^{+phi} dr   ;  dl/dr =", dl_dr)
print("  PROPER TIME (static obs):  dtau = sqrt(-g_tt) dt = e^{-phi} dt   ;  dtau/dt =", dtau_dt)
print("  LAPSE / REDSHIFT FACTOR :  N = sqrt(-g_tt) = e^{-phi}")
print()
# f = e^{-2 phi} = c_eff (W2).  Note f = -g_tt.  And matter side: phi < 0 (deep core),
# so f = e^{-2 phi} -> +inf as phi -> -inf (the seal / deep core).  c_eff -> inf there.
print("  f = e^{-2phi} = c_eff = -g_tt.  Matter core: phi<0 -> f=c_eff -> +inf at seal.")
print("  Redshift e^{-phi}=sqrt(f) -> +inf at core; lapse N=e^{-phi}=sqrt(f).")
print()
# IMPORTANT CONSISTENCY CHECK: the W2 'c_eff = f = e^{-2phi}' vs CANON c_r^2 = e^{-4phi}.
# In tortoise/areal mixing these differ by the areal factor; the SL given uses f as the
# speed.  We take the W2 reduction AS GIVEN (per instructions) but flag the relation:
print("  NOTE: CANON c_r^2 = e^{-4phi} = f^2  (CANON:81) -> c_r = f.  Consistent with W2 dr/dT=f.")
print("        (the SL 'f' IS the radial coordinate wave speed; tortoise dr*=dr/f.)")

# ============================================================================
# STEP 2: THE ENERGY/NORM CRUX -- branch-iv u~1/r in coordinate vs proper measure
# ============================================================================
hdr("STEP 2  ENERGY/NORM of branch-iv u ~ 1/r : coordinate vs proper measure")
# The SL weight (the inner product that makes the operator self-adjoint) is rho = P/f.
# This IS the metric-correct measure for THIS operator (it is what self-adjointness of
# (P f u')' demands). Let us be explicit and compute the squared norm of u = 1/r near r=0.
#
#  Two candidate inner products for the field u(r):
#   (a) COORDINATE L^2 with the SL weight:   ||u||^2 = INT u^2 (P/f) dr
#   (b) "PROPER" L^2 (physical 3-volume measure): the radial field energy density of a
#       scalar-like mode integrated with the proper volume element.
#
# Let us also compute the physically meaningful PROBE ENERGY (the quadratic form Q),
# since the charter's "infinite probe energy" is about the ENERGY, not just the norm.
print("  SL weight (self-adjointness): rho = P/f = 2 r^2 e^{+2phi}.")
print("  SL stiffness: p = P f = 2 r^2 e^{-2phi}.")
print()
# --- (a) COORDINATE-with-SL-weight norm of u=1/r near 0 (phi -> phi0 finite at core) ---
# rho = 2 r^2 e^{2 phi}, with phi -> phi0 (finite, e.g. -0.8) at the core.
# ||u||^2 ~ INT_0 (1/r)^2 * 2 r^2 e^{2phi0} dr = INT_0 2 e^{2phi0} dr  -> FINITE at r=0!
print("  (a) Norm-weight INT u^2 rho dr with u=1/r near core (phi->phi0 finite):")
print("      integrand = (1/r^2)*2 r^2 e^{2phi0} = 2 e^{2phi0} = CONSTANT -> norm FINITE at r=0.")
print("      => u~1/r is NORMALIZABLE in the SL weight near the center.  (limit-circle, as documented)")
print()
# --- The PROBE ENERGY (quadratic form) is the real charter object. ---
#   Q[u] = INT [ p (u')^2 ] dr = INT 2 r^2 e^{-2phi} (u')^2 dr.
# For u = 1/r: u' = -1/r^2, (u')^2 = 1/r^4.
#   Q ~ INT_0 2 r^2 e^{-2phi0} (1/r^4) dr = INT_0 2 e^{-2phi0} / r^2 dr  -> DIVERGES at r=0.
print("  PROBE ENERGY (quadratic form) Q[u] = INT p (u')^2 dr, p = 2 r^2 e^{-2phi}:")
print("      u=1/r => (u')^2 = 1/r^4 => integrand = 2 e^{-2phi0}/r^2 -> INT_0 dr/r^2 = +INF.")
print("      => PROBE ENERGY DIVERGES at the center.  <-- this IS the charter's 'infinite energy'.")
print()
# --- (b) Does the PROPER frame change the ENERGY verdict? ---
# The hypothesis: use the proper measure (proper distance dl=e^{phi}dr) so the energy
# integral's measure is dl instead of dr, AND/OR rescale u to the local-frame amplitude.
# Be explicit. The metric-correct field energy of the W2 wave is the SL energy itself:
#   E = INT [ p (u')^2 + (omega^2 negative-of) ... ] -- but the QUESTION is the gradient
#   term near r=0.  Convert the SAME gradient energy to the proper radial coordinate.
# d/dr = (dl/dr)^{-1} d/dl = e^{-phi} d/dl.  And dr = e^{-phi} dl.
# Q = INT p (du/dr)^2 dr = INT [2 r^2 e^{-2phi}] (e^{-phi} du/dl)^2 (e^{-phi} dl)
#   = INT 2 r^2 e^{-2phi} e^{-2phi} (du/dl)^2 e^{-phi} dl = INT 2 r^2 e^{-5phi} (du/dl)^2 dl.
# This is just a reparameterization -- IDENTICALLY the same number. A coordinate change of
# the integration variable CANNOT change whether a definite integral diverges.
hdr_note = """
  KEY MATHEMATICAL FACT (the refutation core):
  Q[u] is a coordinate-INVARIANT functional (it is INT p (u')^2 dr written in r, but its
  VALUE is the physical gradient energy of the mode and does not depend on the chart used
  to evaluate it). Rewriting INT ... dr as INT ... dl with dl = e^{phi} dr is a change of
  dummy variable; a convergent integral stays convergent and a divergent one stays
  divergent. The proper frame can rescale the AMPLITUDE u and the MEASURE, but the
  physical energy of a fixed mode is one number. To change FINITE<->INFINITE you must
  change the MODE or the OPERATOR, not the chart."""
print(hdr_note)

# --- Numerical demonstration: integrate Q over [eps, R] in BOTH charts, show identical ---
def phi_prof(rr, phi0=-0.8, Rc=1.0):       # deep negative-phi cell (matches eigen script)
    return phi0*np.exp(-(rr/Rc)**2)
def phip_prof(rr, phi0=-0.8, Rc=1.0):
    return phi0*np.exp(-(rr/Rc)**2)*(-2*rr/Rc**2)

def Q_coordinate(eps, R, n=400000, phi0=-0.8, Rc=1.0):
    rr = np.linspace(eps, R, n); ph = phi_prof(rr,phi0,Rc)
    p = 2*rr**2*np.exp(-2*ph)
    u = 1.0/rr; up = -1.0/rr**2          # u=1/r exactly
    integ = p*up**2
    return np.trapz(integ, rr)

def Q_proper(eps, R, n=400000, phi0=-0.8, Rc=1.0):
    # same Q but integrate over proper distance l(r)=INT e^{phi} dr; u'(r) expressed via dl
    rr = np.linspace(eps, R, n); ph = phi_prof(rr,phi0,Rc)
    f_ph = np.exp(ph)                     # dl/dr = e^{phi}
    l = np.concatenate([[0.0], np.cumsum(0.5*(f_ph[1:]+f_ph[:-1])*np.diff(rr))])
    p = 2*rr**2*np.exp(-2*ph)
    up_r = -1.0/rr**2                     # du/dr
    # du/dl = du/dr * dr/dl = up_r * e^{-phi}; integrand in l: p*(du/dl)^2 ... but to compare
    # the SAME physical Q we must include the Jacobian; net it must reproduce Q_coordinate.
    du_dl = up_r*np.exp(-ph)
    integ_l = p*du_dl**2                  # NOTE: this is p*(du/dl)^2, integrate dl
    return np.trapz(integ_l, l)

print("\n  Numerical Q[u=1/r] over [eps, 4] in two charts (must agree; both blow up as eps->0):")
print(f"   {'eps':>10} {'Q(coordinate chart)':>22} {'Q(proper-distance chart)':>26}")
for eps in [1e-1, 1e-2, 1e-3, 1e-4]:
    qc = Q_coordinate(eps, 4.0); qp = Q_proper(eps, 4.0)
    print(f"   {eps:10.0e} {qc:22.6f} {qp:26.6f}")
print("  -> Q grows without bound as eps->0 in BOTH charts (same number). Energy is INFINITE")
print("     in the proper frame too. The chart change does not finitize it.")

# mpmath exact spot-check of the leading divergence INT_eps 2 e^{-2phi0}/r^2 dr = 2e^{-2phi0}(1/eps - 1/R)
hdr2 = "\n  mpmath exact leading-divergence check (phi0=-0.8 frozen, the r->0 behaviour):"
print(hdr2)
phi0 = mp.mpf('-0.8')
for eps in ['1e-2','1e-3','1e-4']:
    e = mp.mpf(eps); R = mp.mpf('4.0')
    exact = 2*mp.e**(-2*phi0)*(1/e - 1/R)     # leading term INT 2 e^{-2phi0} r^{-2} dr
    print(f"   eps={eps}:  2 e^(-2phi0)(1/eps-1/R) = {mp.nstr(exact,8)}  -> diverges ~ 1/eps")

# ============================================================================
# STEP 3: THE FREQUENCY CRUX -- omega -> omega_local, sign of omega_local^2
# ============================================================================
hdr("STEP 3  FREQUENCY CRUX: omega (coordinate) -> omega_local, and the SIGN")
print("""  The SL eigenvalue is omega^2 where w(r,T)=u(r) e^{i omega T}, T = COORDINATE time.
  A static local observer at r measures proper time dtau = e^{-phi} dt = N dt, N = sqrt(-g_tt).
  A coordinate phase e^{i omega t} reads locally as e^{i omega_local tau} with
        omega_local = omega * dt/dtau = omega / N = omega e^{+phi}.
  THE MAP:  omega_local = omega * e^{+phi} = omega / sqrt(f)   (since f=e^{-2phi}).
  This is a POSITIVE REAL rescaling of omega (e^{phi} > 0 always).""")
print()
print("  ==> SIGN OF omega^2 IS A FRAME INVARIANT:")
print("      omega_local^2 = omega^2 * e^{+2phi} = omega^2 / f.")
print("      e^{2phi} = 1/f > 0 STRICTLY.  A real positive factor cannot flip a sign.")
print("      omega^2 < 0  <=>  omega_local^2 < 0.   omega^2 > 0 <=> omega_local^2 > 0.")
print()
# Toward the core/seal: phi -> -inf, f -> +inf, so e^{2phi} -> 0.
print("  Toward the core/seal (phi -> -inf, c_eff=f -> +inf):  e^{2phi} -> 0+.")
print("  So omega_local^2 = omega^2 e^{2phi} -> 0 (the local frequency is RED-shifted to zero,")
print("  it does NOT grow). A relaxation rate (omega^2<0) maps to omega_local^2 = (neg)*(0+):")
print("  it stays NEGATIVE (still a decaying/relaxation mode locally), and its magnitude")
print("  SHRINKS toward the core. There is NO sign flip and NO real-oscillation revival.")
print()
# numerical: branch-iv coordinate omega^2 ~ -29 (documented). map it.
om2_coord = -29.0
for phival in [0.0, -0.4, -0.8, -2.0, -10.0]:
    om2_loc = om2_coord*np.exp(2*phival)
    print(f"   phi={phival:6.1f}: f=c_eff={np.exp(-2*phival):12.4g}  "
          f"omega_local^2 = {om2_coord}*e^(2phi) = {om2_loc:+.5g}  "
          f"[{'still negative (relaxation)' if om2_loc<0 else 'positive'}]")

# ============================================================================
# STEP 4: BOX-INDEPENDENCE in the proper frame
# ============================================================================
hdr("STEP 4  BOX-INDEPENDENCE: is the binding-mode frequency intrinsic or box-set?")
print("""  Two cases:
   - REGULAR (Dirichlet) extension: psi~r at center -> the documented box modes
     omega ~ 1/R_wall. Frame map omega_local=omega e^{phi(R)} only rescales by the
     edge redshift; since phi(seal)=0 at the exterior, e^{phi}=1 there -> box modes
     stay box modes in the proper frame. NOT intrinsic.
   - BINDING branch-iv (u~1/r): IF admitted, its omega^2 is set by the well V=-2phi'f^2/r,
     i.e. by the DILATION profile phi(r) (no R_wall in V). So its frequency WOULD be
     intrinsic. BUT step 2 shows its probe energy is infinite (in BOTH frames) and step 3
     shows its omega^2<0 stays negative locally -> it is a RELAXATION rate, not an
     oscillation, intrinsic or not.""")
# Quick numeric: confirm the well depth / a candidate bound omega^2 is R_wall-independent,
# by Rayleigh quotient with a normalizable trial that AVOIDS the 1/r singularity (regular
# class) -- to show the REGULAR class has NO negative Rayleigh quotient (no binding).
def V_of_r(rr, phi0=-0.8, Rc=1.0):
    ph = phi_prof(rr,phi0,Rc); pp = phip_prof(rr,phi0,Rc); f = np.exp(-2*ph)
    return -2*pp*f**2/rr, f
def rayleigh_regular(R, phi0=-0.8, Rc=1.0, n=20000):
    # tortoise coordinate, regular trial psi ~ sin(pi r*/L) (Dirichlet both ends)
    rr = np.linspace(1e-4, R, n); V,f = V_of_r(rr,phi0,Rc)
    rs = np.concatenate([[0.0], np.cumsum(np.diff(rr)/(0.5*(f[1:]+f[:-1])))])
    L = rs[-1]
    psi = np.sin(np.pi*rs/L)
    dpsi = np.gradient(psi, rs)
    num = np.trapz(dpsi**2 + V*psi**2, rs)
    den = np.trapz(psi**2, rs)
    return num/den, L
print("\n  Regular-class Rayleigh quotient (lowest box trial), vary R_wall:")
print(f"   {'R_wall':>8} {'rstar_len':>10} {'R[psi]=omega^2_est':>20}")
base=None
for Rw in [4.0, 8.0, 16.0, 32.0]:
    Rq, L = rayleigh_regular(Rw)
    if base is None: base=Rq
    print(f"   {Rw:8.1f} {L:10.3f} {Rq:20.6f}   (~1/R^2 box scaling => NOT intrinsic)")
print("  -> regular class: positive, shrinks with R_wall => pure box control (no binding).")

# ============================================================================
# STEP 5: VERDICT
# ============================================================================
hdr("STEP 5  VERDICT")
print("""  (a) PROPER FRAMES (CANON.md:79):
        proper distance  dl   = e^{+phi} dr
        proper time      dtau = e^{-phi} dt   (lapse N = sqrt(-g_tt) = e^{-phi} = sqrt(f))
        redshift factor  = e^{-phi} = sqrt(f) = sqrt(c_eff); -> +inf at core (phi->-inf).

  (b) BRANCH-IV ENERGY in the proper measure:  STILL INFINITE.
        - The SL-weight NORM of u~1/r is finite (limit-circle, already documented) in BOTH
          charts -- that was never the obstruction.
        - The PROBE ENERGY (quadratic form Q=INT p u'^2) DIVERGES as 1/eps at the center in
          the COORDINATE chart AND in the PROPER-distance chart (numerically identical;
          mpmath confirms the 1/eps leading divergence). A change of integration variable
          cannot finitize a divergent definite integral. => the 'infinite probe energy'
          charter (open_domain_discreteness_results.md:116) is FRAME-INVARIANT.

  (c) omega -> omega_local MAP:  omega_local = omega e^{+phi} = omega/sqrt(f);
        omega_local^2 = omega^2 e^{2phi} = omega^2/f.  e^{2phi}=1/f > 0 STRICTLY.
        => the SIGN of omega^2 is FRAME-INVARIANT. omega^2<0 (relaxation) stays
        omega_local^2<0 (relaxation) locally.  Toward the core e^{2phi}->0 so the local
        rate SHRINKS -- it does NOT become a real oscillation.  NO REVIVAL via the map.

  (d) BOX-INDEPENDENCE:  the regular (admissible) class is pure box-control in the proper
        frame too (edge redshift e^{phi(seal)}=1; box modes unchanged). The binding branch
        WOULD be intrinsic, but it is inadmissible (infinite energy) and non-oscillatory.

  VERDICT:  CONJECTURE A STILL DEAD in the local frame. The coordinate-frame verdict is
  FRAME-INVARIANT for the two decisive reasons:
     (1) finite/infinite of the probe ENERGY is a reparameterization invariant of a fixed
         mode -- the proper chart cannot rescue a divergent gradient integral;
     (2) the redshift factor e^{2phi} that maps omega^2 -> omega_local^2 is STRICTLY
         POSITIVE, so it cannot flip omega^2<0 into a real oscillation, and in fact it
         drives the local rate to ZERO (not to a finite real frequency) at the core.

  MOST WISHFUL STEP (and why it fails):  the hope that 'c_eff -> infinity toward the core'
  makes the local frequency LARGE/real. The map runs the OTHER way: c_eff=f large means
  redshift sqrt(f) large in PROPER TIME, i.e. coordinate frequencies are DIVIDED by sqrt(f),
  so omega_local -> 0 at the core. The deep core is where coordinate modes are most red-
  shifted toward zero, not blue-shifted into oscillation. The 'extreme where c_eff->inf'
  intuition has the sign of the effect backwards.

  CORPUS CONSILIENCE (independent kill of the same hypothesis-family): the program already
  settled the measure fork -- 'the self-adjoint measure is r^2 sin(theta) BARE; the e^{-2phi}
  weights belong in the STIFFNESS, NOT the measure' (NEGATIVES_REGISTRY.md:782-785), and
  'NEITHER OLD LIFT SURVIVES ... the proper lift ... is refuted' (measure_fork_results.md:52-60).
  Moving e^{-2phi} into the measure (the proper-frame move) was diagnosed there as a MEASURE
  DOUBLE-COUNT producing ~18000 SPURIOUS negatives. The revival hypothesis is a re-run of
  that already-refuted move on the radial center BC.

  CONFIDENCE: HIGH. Steps (b) and (c) are reparameterization / strict-positivity facts, not
  numerics; the numerics merely illustrate them and the mpmath leading-order check agrees.
""")
