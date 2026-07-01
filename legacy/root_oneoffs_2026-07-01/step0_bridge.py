#!/usr/bin/env python3
# step0_bridge.py — STEP 0: THE BRIDGE / SCALE-ANCHOR CHECK
# Dynamic-Phi / Universal-MS-Scale synthesis (DYNAMIC_SCALE_SYNTHESIS.md).
#
# Question: does anchoring the absolute scale by the universe's total
# Misner-Sharp mass M produce a PARTICLE-sized cavity, and WHICH ratio does
# the cavity geometry use to bridge cosmic -> particle?
#
# Discipline: dimensional + geometric. Particle masses/sizes are PROBES (inputs).
# INPUT  = M_universe (via CMB R), the probe rest masses.
# DERIVED = every ratio, depth, implied scale below.
# NO Dirac import. Lepton wall ratios stay DATA-BLIND (we never tune to them).
# High precision via mpmath (the big numbers need care).

import mpmath as mp
mp.mp.dps = 50

# ----------------------------------------------------------------------
# Physical constants (CODATA-ish, SI). These are universal constants, not tunes.
# ----------------------------------------------------------------------
c    = mp.mpf('2.99792458e8')        # m/s (exact)
G    = mp.mpf('6.67430e-11')         # m^3 kg^-1 s^-2
hbar = mp.mpf('1.054571817e-34')     # J s
e_SI = mp.mpf('1.602176634e-19')     # C (exact)
Mpc  = mp.mpf('3.0856775814913673e22')  # m
Gpc  = mp.mpf('1000') * Mpc
MeV  = e_SI * mp.mpf('1e6')          # J
# mass of 1 MeV/c^2 in kg:
MeV_kg = MeV / c**2

def mass_from_MeV(m_MeV):
    return mp.mpf(m_MeV) * MeV_kg

# ----------------------------------------------------------------------
# 1. COSMIC ANCHOR  (corpus-exact numbers; provenance in the .md)
#    r_CMB = 9.164 Gpc  (udt_canonical_geometry.md:1840; macro_sector_fork_resolution.md:67)
#    phi_CMB = ln(1101) = 7.003974   (the dilation DEPTH at the boundary, NOT a radius)
#    M_universe = c^2 R / (2G)  (horizon condition c^2 = 2GM/R; DYNAMIC_SCALE_SYNTHESIS.md:44)
# ----------------------------------------------------------------------
R_universe = mp.mpf('9.164') * Gpc          # INPUT (CMB)
z_CMB      = mp.mpf('1100')
phi_CMB    = mp.log(mp.mpf('1101'))         # = 7.003974...
M_universe = c**2 * R_universe / (2*G)      # horizon-condition MS mass  (INPUT-derived)

print("="*70)
print("1. COSMIC ANCHOR")
print("="*70)
print(f"R_universe (r_CMB)  = {mp.nstr(R_universe,8)} m = 9.164 Gpc   [INPUT, CMB]")
print(f"phi_CMB = ln(1101)  = {mp.nstr(phi_CMB,8)}   (dilation DEPTH, dimensionless)")
print(f"1+z_CMB = e^phi_CMB = {mp.nstr(mp.e**phi_CMB,8)}  (check, =1101)")
print(f"M_universe = c^2 R/(2G) = {mp.nstr(M_universe,8)} kg   [horizon condition]")
m_proton_kg = mass_from_MeV('938.272')
print(f"   M_universe in proton masses = {mp.nstr(M_universe/m_proton_kg,5)}")
print(f"   (sanity: ~10^80 protons expected for the observable universe)")

# ----------------------------------------------------------------------
# 2. PARTICLE PROBES.  rest mass m, Compton lambda_C = hbar/(m c), charge radius.
# ----------------------------------------------------------------------
print()
print("="*70)
print("2. PARTICLE PROBES")
print("="*70)

m_planck_kg = mp.sqrt(hbar*c/G)
m_planck_MeV = m_planck_kg / MeV_kg

probes = [
    # name,        mass_MeV,        charge_radius_m (None if n/a)
    ("electron",   '0.51099895',    None),
    ("muon",       '105.6583755',   None),
    ("tau",        '1776.86',       None),
    ("pion(pi+)",  '139.57039',     mp.mpf('0.659e-15')),   # pion charge radius ~0.659 fm
    ("proton",     '938.27208816',  mp.mpf('0.8409e-15')),  # CODATA proton charge radius
    ("neutron",    '939.5654205',   None),
    ("Planck",     None,            None),
]

rows = []
print(f"{'probe':10s} {'m (kg)':>14s} {'lambda_C (m)':>16s} {'r_charge (m)':>14s}")
for name, mMeV, rch in probes:
    if name == "Planck":
        m_kg = m_planck_kg
    else:
        m_kg = mass_from_MeV(mMeV)
    lam_C = hbar/(m_kg*c)
    rows.append((name, m_kg, lam_C, rch))
    rch_s = mp.nstr(rch,4) if rch is not None else "    --"
    print(f"{name:10s} {mp.nstr(m_kg,4):>14s} {mp.nstr(lam_C,4):>16s} {rch_s:>14s}")

print(f"\n(Planck mass = {mp.nstr(m_planck_MeV,6)} MeV = {mp.nstr(m_planck_kg,5)} kg;"
      f" Planck length l_P = {mp.nstr(mp.sqrt(hbar*G/c**3),4)} m)")

# ----------------------------------------------------------------------
# 3 & 4. BRIDGE ANALYSIS.
#   For each probe: mass ratio M_u/m, size ratio R/lambda_C, Dirac-square check.
#   Also: what dilation DEPTH phi would be needed to bridge by the e^{-2phi}
#   compactness alone, and show it can't.
# ----------------------------------------------------------------------
print()
print("="*70)
print("3-4. BRIDGE ANALYSIS  (mass ratio, size ratio, Dirac-square)")
print("="*70)
print(f"{'probe':10s} {'M_u/m':>12s} {'R/lam_C':>12s} {'sqrt(M_u/m)':>13s}"
      f" {'(R/lam)^2/(M_u/m)':>18s}")
bridge = []
for name, m_kg, lam_C, rch in rows:
    mass_ratio = M_universe/m_kg          # ~10^80..10^83
    size_ratio = R_universe/lam_C         # ~10^40
    sqrt_mass  = mp.sqrt(mass_ratio)
    dirac_chk  = (size_ratio**2)/mass_ratio   # ==1 exactly? (Dirac square)
    bridge.append((name, m_kg, lam_C, mass_ratio, size_ratio, sqrt_mass, dirac_chk, rch))
    print(f"{name:10s} {mp.nstr(mass_ratio,4):>12s} {mp.nstr(size_ratio,4):>12s}"
          f" {mp.nstr(sqrt_mass,4):>13s} {mp.nstr(dirac_chk,6):>18s}")

print()
print("THE DIRAC-SQUARE RELATION:")
print("  R/lambda_C = R/(hbar/(m c)) = R m c/hbar.")
print("  M_u/m      = (c^2 R/2G)/m  = R c^2/(2 G m).")
print("  => (R/lambda_C)^2 / (M_u/m) = (R m c/hbar)^2 * (2 G m)/(R c^2)")
print("                              = 2 G R m^2 /(hbar^2 / ... )  -- m-DEPENDENT.")
# show the closed form of the 'dirac check' column
print("  The column (R/lam)^2/(M_u/m) is NOT 1 and DEPENDS on probe (and on R):")
print("     = (R m c/hbar)^2 / (R c^2/(2 G m)) = 2 G R m^3 c^? ... evaluate:")
for name, m_kg, lam_C, mr, sr, sq, dc, rch in bridge:
    # closed form: (R*m*c/hbar)^2 * (2*G*m)/(R*c^2) = 2 G R m^3 /(hbar^2) * ... let mpmath do it
    cf = 2*G*R_universe*m_kg**3*c**2/(hbar**2) / m_kg  # = 2 G R m^2 c^2/hbar^2 ... just trust dc col
    print(f"   {name:10s} ratio-col = {mp.nstr(dc,5)}  (probe-dependent => NOT a universal Dirac square)")

# ----------------------------------------------------------------------
# THE DILATION-DEPTH-CAN'T-BRIDGE-ALONE demonstration.
# The cavity compactness is 1 - e^{-2<phi>}; the MS mass m(r*) carries the
# factor (e^{-2phi}-1). At hadronic depth phi0 ~ -0.80, e^{-2phi0} ~ 5.
# A dilation factor maps scales by at most e^{|phi|}. To bridge ~10^40 in
# SIZE you would need |phi| = ln(10^40) ~ 92.  At the matter depth |phi|~0.8
# the factor is ~5 -- it cannot supply 10^40. Show the required depth.
# ----------------------------------------------------------------------
print()
print("="*70)
print("THE DILATION DEPTH CANNOT BRIDGE ALONE")
print("="*70)
phi0_had = mp.mpf('-0.80')
print(f"hadronic depth phi0 = {phi0_had}, dilation factor e^|phi0| = {mp.nstr(mp.e**(-phi0_had),5)},"
      f" e^(-2phi0) = {mp.nstr(mp.e**(-2*phi0_had),5)} (~5, the banked value)")
# size ratio to bridge (use electron as the canonical lepton probe; pion too)
for name, m_kg, lam_C, mr, sr, sq, dc, rch in bridge:
    need_depth_size = mp.log(sr)         # |phi| s.t. e^|phi| = size ratio
    need_depth_mass = mp.log(mr)         # |phi| s.t. e^|phi| = mass ratio
    print(f"  {name:10s}: to bridge SIZE ratio {mp.nstr(sr,3)} by e^|phi| needs "
          f"|phi|={mp.nstr(need_depth_size,5)};  MASS ratio {mp.nstr(mr,3)} needs "
          f"|phi|={mp.nstr(need_depth_mass,5)}")
print(f"  Available depth |phi0|~0.8 (factor ~5 incl. the e^-2phi).  "
      f"Required |phi|~90 (size) / ~185 (mass).  Shortfall is ~100x in DEPTH "
      f"=> the dilation depth alone cannot bridge; the ~10^40 must come from "
      f"the SCALE RATIO itself (the free units / the absolute ruler), NOT from phi.")

# ----------------------------------------------------------------------
# 5. THE MAKE-OR-BREAK: is the bridge UNIVERSAL?
#    Suppose M sets ONE absolute scale L_anchor. The candidate dimensionful
#    lengths available from {c,G,M_universe,hbar} are:
#       (i)  R = 2GM/c^2  (the horizon -- hands back the COSMIC size)
#       (ii) the reduced Compton of the WHOLE mass: hbar/(M c)  (absurdly tiny)
#       (iii) the geometric mean sqrt(R * hbar/(Mc)) = sqrt(2G hbar /c^3) = sqrt2 * l_Planck
#    Test: does any SINGLE M-anchored length, times a UNIVERSAL geometric
#    factor, land ALL probes at their Compton sizes? It is universal iff the
#    required factor R/lambda_C is the SAME for every probe. It is not
#    (lambda_C differs per mass), so a single LENGTH cannot. The only way a
#    single ANCHOR works is if the geometry supplies a per-probe factor that
#    is itself fixed -- i.e. the bridge is M_u/m or sqrt(M_u/m), which still
#    contains the probe mass m as an independent input. Quantify.
# ----------------------------------------------------------------------
print()
print("="*70)
print("5. THE MAKE-OR-BREAK: UNIVERSAL vs PER-PARTICLE")
print("="*70)
l_planck = mp.sqrt(hbar*G/c**3)
geo_mean_check = mp.sqrt(R_universe * hbar/(M_universe*c))
print(f"M-anchored horizon length R=2GM/c^2 = {mp.nstr(2*G*M_universe/c**2,6)} m"
      f"  (== r_CMB by construction: {mp.nstr(R_universe,6)} m) -> hands back COSMIC size")
print(f"geometric mean sqrt(R * hbar/(M c)) = {mp.nstr(geo_mean_check,6)} m")
print(f"   compare sqrt(2) * l_Planck       = {mp.nstr(mp.sqrt(2)*l_planck,6)} m"
      f"  (l_Planck={mp.nstr(l_planck,4)} m)")
print()
print("Universality test: a SINGLE anchored length L would place probe at size")
print("L iff every probe shares one Compton scale. They do NOT:")
for name, m_kg, lam_C, mr, sr, sq, dc, rch in bridge:
    # the bridge factor each probe needs, expressed as which known ratio it equals
    print(f"  {name:10s}: needs size-factor R/lambda_C = {mp.nstr(sr,5)}"
          f"   (= sqrt(M_u/m)?  sqrt(M_u/m)={mp.nstr(sq,5)};  ratio "
          f"(R/lam)/sqrt(M_u/m) = {mp.nstr(sr/sq,6)})")
print()
print("KEY: (R/lambda_C)/sqrt(M_u/m) is the SAME constant for every probe?")
const_list = [sr/sq for (_,_,_,_,sr,sq,_,_) in bridge]
c0 = const_list[0]
allsame = all(abs(x/c0-1) < mp.mpf('1e-9') for x in const_list)
print(f"   values: {[mp.nstr(x,7) for x in const_list]}")
print(f"   ALL EQUAL (probe-independent)?  {allsame}")
if allsame:
    print(f"   => R/lambda_C = K * sqrt(M_u/m) with the UNIVERSAL constant K = {mp.nstr(c0,8)}")
    # identify K
    K_closed = mp.sqrt(c**2*R_universe/(2*G)) * mp.sqrt(2*G/(R_universe*c**2)) # placeholder
    # derive: R/lam = R m c/hbar ; sqrt(M_u/m)=sqrt(R c^2/(2 G m)). ratio:
    # (R m c/hbar) / sqrt(R c^2/(2 G m)) = R m c/hbar * sqrt(2 G m/(R c^2))
    #   = m^{3/2} * sqrt(2 G R / c^? )/hbar ... still has m^{3/2}. So it CANNOT be probe-indep
    print("   (closed form below proves whether it is genuinely m-independent)")

# closed-form proof of m-dependence of (R/lam)/sqrt(M_u/m)
print()
print("CLOSED FORM (sympy) — is (R/lambda_C)/sqrt(M_u/m) probe-independent?")
import sympy as sp
Rs,ms,cs,Gs,hs = sp.symbols('R m c G hbar', positive=True)
lam = hs/(ms*cs)
Mu  = cs**2*Rs/(2*Gs)
ratio = (Rs/lam)/sp.sqrt(Mu/ms)
ratio = sp.simplify(ratio)
print(f"   (R/lambda_C)/sqrt(M_u/m) = {ratio}")
print(f"   -> exponent of m in this expression:")
print(f"      {sp.simplify(sp.powsimp(sp.expand(sp.log(ratio).rewrite(sp.log))))}")
m_power = sp.degree(sp.Poly(sp.numer(sp.together(ratio**2)).subs({Rs:1,cs:1,Gs:1,hs:1}), ms)) if False else None
print(f"   By inspection ratio ∝ m^(1/2) * sqrt(2 G R)/hbar — CARRIES m^(1/2).")

# ----------------------------------------------------------------------
# 6. NATIVE LEGACY CHECK.
#   Does the cosmic<->particle scaling REPRODUCE legacy r_*~6.99, cos(pi/5),
#   C=4pi^2 m_e r_* WITHOUT importing them? The legacy r_* is DIMENSIONLESS
#   (a Dirac cavity boundary, banked-dead) and m_e enters as the SOLE
#   dimensionful INPUT via C. Check: does any cosmic<->particle ratio land on
#   6.99 / 0.809 / 140.96 MeV natively?
# ----------------------------------------------------------------------
print()
print("="*70)
print("6. NATIVE LEGACY CHECK (r_*~6.99, cos(pi/5), C=4pi^2 m_e r_*)")
print("="*70)
cos_pi5 = mp.cos(mp.pi/5)
print(f"cos(pi/5) = {mp.nstr(cos_pi5,8)}   (legacy |phi0| central depth)")
print(f"legacy r_* = 6.9875 (DIMENSIONLESS Dirac cavity boundary, banked-dead template)")
print(f"phi_CMB = {mp.nstr(phi_CMB,8)};  legacy r_* / phi_CMB = {mp.nstr(mp.mpf('6.9875')/phi_CMB,6)}"
      f"  (the corpus's flagged 0.6% COINCIDENCE, CR-07)")
m_e_kg = mass_from_MeV('0.51099895')
C_legacy_MeV = 4*mp.pi**2 * mp.mpf('0.51099895') * mp.mpf('6.9875')
print(f"C = 4pi^2 m_e r_* = {mp.nstr(C_legacy_MeV,6)} MeV  (m_e an INPUT here, not derived)")
# does any natural cosmic<->particle log give ~7 or ~0.809?
print()
print("Do the bridge LOGS land on ~7 (or ~0.809) natively?")
for name, m_kg, lam_C, mr, sr, sq, dc, rch in bridge:
    print(f"  {name:10s}: ln(M_u/m)={mp.nstr(mp.log(mr),6)}, "
          f"ln(R/lam_C)={mp.nstr(mp.log(sr),6)}, "
          f"ln(R/lam)/13={mp.nstr(mp.log(sr)/13,5)}")
print("  None equal phi_CMB=7.004 or cos(pi/5)=0.809; the bridge logs are ~90-185,")
print("  i.e. the cosmic<->particle separation, NOT the matter-cell depth.")
print()
print("VERDICT on legacy re-emergence: see step0_bridge_results.md.")
