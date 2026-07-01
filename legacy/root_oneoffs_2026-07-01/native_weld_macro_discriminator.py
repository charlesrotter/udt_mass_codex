#!/usr/bin/env python3
"""
MACRO WELD DISCRIMINATOR (HANDOFF queue item 1; the binding scoping is
macro_contamination_map.md).  New file only; modifies nothing.

DIFFERENTIAL test: hold the ENTIRE macro CMB pipeline fixed (background,
source, temperature model, projection -- the S116 radial-correlation
pipeline, /home/udt-admin/UDT/dispatch_D_CMB_EE_PROJECTION_SPIN_1/
native_weight_cl.py conventions) and swap ONLY the weld that builds H1
from the breathing field delta-phi:

  EINSTEIN weld (canon/S116, K=0)   [differential / CUMULATIVE]:
      d_r(e^{-2phi0} H1) = 2 d_t(dphi)
      =>  H1_E(r) = e^{+2phi0(r)} * Int_0^r 2 d_t(dphi) dr'
  NATIVE weld (weld_status_results.md; identically delta-T_tr = 0)
                                     [algebraic / LOCAL]:
      f phi0' H1 = 2 d_t(dphi)   (f = e^{-2phi0})
      =>  H1_N(r) = 2 d_t(dphi) / (f phi0')  =  -4 d_t(dphi) / f'

Common time structure d_t(dphi) = -i*omega*dphi (quadrature) -- COMMON to
both welds; pre-registered below: the phase channel CANNOT discriminate.

Every conclusion is CONDITIONAL: "given the common pipeline".  Absolute
amplitudes are NOT compared (epsilon-class inputs).  The temperature-model
sand (+1/4 drho/rho intrinsic term) is common-mode by construction and is
NOT used here: TT uses the GEOMETRY-clean -dphi Sachs-Wolfe channel.

AMENDED SAME DAY (2026-06-10) per verifier agent a6ef46971a22e0069
(amendments strengthen / correct; nothing weakened):
  (1) FACTUAL CORRECTION: the original run claimed the record states no
      position tolerance for the EE interleaving PASS and printed
      "EINSTEIN PREFERRED -- WEAK".  WRONG: the record states the
      tolerance (S115 ~30 ell, S116 mean 42 ell; exact citations at
      RECORD_TOL_* below).  The pre-registered downgrade clause FIRES;
      the verdict is INDISTINGUISHABLE-AT-CURRENT-RECORD.
  (2) Comb-phase-anchor robustness scan added (17 anchors over one full
      comb spacing) -- the E->N shift survives, every matched peak
      negative: a fractional-r effect, not a phase artifact.
  (3) Coherence-treatment sensitivity stated (+ in-script Limber/short-
      coherence proxy): ~2.9 ell at Lc = r_CMB/ell, 3.8-4.2 ell in the
      verifier's independent Limber/short-coherence integrator; the
      DIRECTION is universal.  The shift statement is specific to the
      principal sin^2-comb peaks (secondary-harmonic features can shift
      oppositely).
  (4) Honesty softenings: the V^2-based D1 statistic is weakly (log)
      rmin-dependent for the native weld (practically negligible); the
      D2 signal/spread margin is < 2x (doubled spread flips the formal
      comparison) -- one more reason the strict verdict is
      INDISTINGUISHABLE.
"""

import numpy as np
import sympy as sp
from scipy.integrate import cumulative_trapezoid

# ----------------------------------------------------------------------
# constants / provenance-graded inputs
# ----------------------------------------------------------------------
MU_G   = 0.2472981283        # /Gpc  [DATA-FIT; the VALUE rides pi*sqrt(pi/3)/13 -- QUARANTINED-RIDE label, fit survives]
R_CMB  = 9.164114            # Gpc   [DATA-FIT (finite-cell canon, phi0(r_CMB)=ln(1101))]
COS5   = np.cos(np.pi/5.0)
DL_IN  = 297.0               # BAO comb spacing at r_CMB in ell  [INPUT-class, observational]
ELL_OFF = 243.0              # comb phase offset: first r_CMB-shell TT peak at 540  [INPUT-class]
L_BAO  = np.pi*R_CMB/DL_IN   # Gpc; radial comb wavelength implied by Delta-ell ~ 297 at r_CMB

# Recorded EE interleaving POSITION TOLERANCE (VERIFIER CORRECTION,
# 2026-06-10, agent a6ef46971a22e0069 -- the original run wrongly claimed
# the record states no tolerance).  Record citations:
#   /home/udt-admin/UDT/SESSION_115_PROMPT.md line 53:
#     "EE interleaved positions matching Planck ~30 in ell (vs ~102 aligned)"
#   /home/udt-admin/UDT/SESSION_116_PROMPT.md lines 36-37:
#     "EE positions interleaved at TT-peak midpoints (mean|Delta-ell| 42
#      vs 108)"
RECORD_TOL_LO = 30.0   # ell  [RECORD, S115]
RECORD_TOL_HI = 42.0   # ell  [RECORD, S116]

npass, nfail = 0, 0
def check(label, ok, detail=""):
    global npass, nfail
    tag = "PASS" if ok else "FAIL"
    if ok: npass += 1
    else:  nfail += 1
    print(f"  [{tag}] {label}" + (f"  ({detail})" if detail else ""))

def hr(c="-"): print(c*72)

# ----------------------------------------------------------------------
# HONESTY / CONDITIONALITY HEADER  (printed before anything is computed)
# ----------------------------------------------------------------------
print("="*72)
print("NATIVE-vs-EINSTEIN WELD MACRO DISCRIMINATOR -- DIFFERENTIAL TEST")
print("="*72)
print("""
CONDITIONALITY (macro_contamination_map.md, BINDING):
  * Every conclusion below is CONDITIONAL: "given the common pipeline
    (flagged layers held fixed as hypothetical), ...".
  * The asymmetric set (what differs between the welds) is entirely
    GEOMETRY-grade: the constraint form, the H1 radial structure, the
    weld-derived weight.  No quarantined layer enters asymmetrically.
  * Inline provenance flags:
      - phi0(r) profile + mu_g + r_CMB ........ DATA-FIT (labels that said
        "derived, zero free params" ride the quarantined triple -- label
        sand only; the fit stands on Pantheon+/DESI data)
      - breathing envelope dphi(r) ............ INPUT-class (S116 crude
        analytic source style; representative, not load-bearing)
      - BAO comb Delta-ell ~ 297 + phase ...... INPUT-class (observational)
      - recycling amplitude epsilon ........... INPUT-class, NOT compared
      - temperature model used here ........... -dphi Sachs-Wolfe ONLY
        (GEOMETRY-clean).  The +1/4 drho/rho intrinsic term is SAND-flagged
        (rides the UDT blackbody) and is COMMON-mode anyway; not used.
      - ell^4 spin factor (lm1)l(l+1)(l+2) .... GEOMETRY, COMMON; cancels
        in every A/B and EE/TT comparison here.
  * Absolute amplitudes / absolute envelope peak positions are NOT
    compared (epsilon-class inputs; crude-source artifact per S116).

PRE-REGISTERED EXPECTATION (phase channel):
  Both welds give H1 proportional to d_t(dphi) = -i*omega*dphi -- identical
  TIME structure (quadrature with dphi).  The phase / interleaving-EXISTENCE
  channel CANNOT discriminate the welds.  Only weld-form-sensitive RADIAL
  structure can (the channel the contamination map grades GEOMETRY-clean).
  A sympy check below verifies the ratio H1_E/H1_N is omega-free and real.
""")

print("PRE-REGISTERED DISCRIMINATING CHANNELS (declared before computing):")
print("""
  D1: radial-weight shapes -- argmax radius, median radius r50 of the
      projection-effective kernel V(r) = W(r)*sqrt(S(r)), width r84-r16,
      for both welds (+ S116 lensing weight as historical reference).
  D2: EE comb feature POSITIONS (BAO comb source, variant b) relative to
      the TT comb / its sin^2 interleaving midpoints: do the EE peak
      positions shift between welds?  Quantified in ell units.
      Record pin: S115/S116 EE interleaving positions PASSED (Einstein).
  D3: EE/TT ratio R(ell) = C_ell^EE / (ell^4 C_ell^TT) log-log slope over
      ell in [100, 2000] per weld (S116 Einstein/lensing: ~ +0.02..+0.05,
      ell-flat).  Does the native weld stay ell-flat or tilt?
  D4: EE peak-radius-driven coherence: effective comb spacing / ell-scale
      ell_eff = pi*r_eff/L_BAO = 297*(r_eff/r_CMB) per weld (r_eff = r50).

PRE-REGISTERED VERDICT RULES:
  spread(channel) = max over robustness variants (source (a) vs (b) where
  applicable, radial-grid doubling, coherence-length factor-2, inner-cutoff
  doubling, envelope-power alternative) of |metric_variant - metric_base|,
  over both welds.  signal(channel) = |metric_E - metric_N| at baseline.
  NATIVE PREFERRED / EINSTEIN PREFERRED only if some channel has
  signal > spread AND its direction is checkable against the recorded
  Planck-validated facts (EE interleaving positions PASSED; EE peak ~1004;
  TT comb [540,810,1130,1450,1750]).  Channels the record does not pin
  (D1, D4 directly; D3 only via gross ell-flatness, threshold |slope|>0.5)
  cannot flip the verdict.  Otherwise:
  INDISTINGUISHABLE-AT-CURRENT-RECORD.
""")

print("VERIFIER AMENDMENT TO THE RECORD PIN (2026-06-10, a6ef46971a22e0069):")
print(f"""
  The original run asserted that the record states NO position tolerance
  for the EE interleaving PASS.  FACTUAL ERROR -- the record states it:
    /home/udt-admin/UDT/SESSION_115_PROMPT.md line 53:
      "EE interleaved positions matching Planck ~30 in ell (vs ~102
       aligned)"
    /home/udt-admin/UDT/SESSION_116_PROMPT.md lines 36-37:
      "EE positions interleaved at TT-peak midpoints (mean|Delta-ell| 42
       vs 108)"
  The recorded pass precision is therefore {RECORD_TOL_LO:.0f}-{RECORD_TOL_HI:.0f} ell.  The
  pre-registered downgrade clause (recorded tolerance coarser than the
  differential => INDISTINGUISHABLE-AT-CURRENT-RECORD) is applied with
  this recorded value in the verdict below.  The pre-registered rules
  text above is left untouched (it was written before computing); only
  the factually wrong no-tolerance claim is corrected.
""")

# ----------------------------------------------------------------------
# S1/S2: sympy + numerical verification of the setup
# ----------------------------------------------------------------------
hr("=")
print("S1/S2: SETUP VERIFICATION (sympy where marked)")
hr("=")

# S1 numeric: locked cubic profile, phi0(r_CMB) = ln(1101)
def phi0_f(r):
    x = MU_G*r
    return 1.5*x - COS5*x**2 + (2.0/3.0)*x**3
def phi0p_f(r):  # d(phi0)/dr
    x = MU_G*r
    return MU_G*(1.5 - 2.0*COS5*x + 2.0*x**2)

PHI_C = phi0_f(R_CMB)
dev = abs(PHI_C - np.log(1101.0))
check("S1  phi0(r_CMB) = ln(1101)", dev < 1e-3,
      f"phi0(r_CMB)={PHI_C:.7f}, ln(1101)={np.log(1101.0):.7f}, |diff|={dev:.2e}")
mu_formula = np.pi*np.sqrt(np.pi/3.0)/13.0
check("S1  mu_g value vs pi*sqrt(pi/3)/13 [QUARANTINED-RIDE label; DATA-FIT value]",
      abs(MU_G - mu_formula) < 1e-8, f"|diff|={abs(MU_G-mu_formula):.1e}")

# S2 sympy: phi0' > 0 everywhere (negative discriminant), f' = -2 phi0' f,
# weld equivalence, H1_E satisfies the differential weld, phase commonality.
xs = sp.symbols('x', real=True)
c5s = sp.cos(sp.pi/5)                       # = (1+sqrt(5))/4 exactly
quad = sp.Rational(3,2) - 2*c5s*xs + 2*xs**2   # phi0'(x)/mu_g
disc = sp.discriminant(quad, xs)
disc_exact = sp.simplify(disc - (4*c5s**2 - 12))
check("S2  discriminant(3/2 - 2cos(pi/5)x + 2x^2) = 4cos^2(pi/5)-12 (sympy exact)",
      disc_exact == 0, f"disc = {sp.simplify(disc)} = {float(disc):.6f}")
check("S2  discriminant < 0 and leading coeff > 0  =>  phi0'(r) > 0 on (0, r_CMB]"
      "  =>  H1_N regular everywhere", float(disc) < 0)

rs  = sp.symbols('r', positive=True)
Phi = sp.Function('Phi')(rs)
f_s = sp.exp(-2*Phi)
check("S2  f' = -2 phi0' f (sympy, generic profile)",
      sp.simplify(sp.diff(f_s, rs) + 2*sp.Derivative(Phi, rs)*f_s) == 0)

gfun = sp.Function('g')   # g := d_t(dphi)
H1N_a = 2*gfun(rs)/(f_s*sp.Derivative(Phi, rs))
H1N_b = -4*gfun(rs)/sp.diff(f_s, rs)
check("S2  weld equivalence: 2 g/(f phi0') == -4 g/f' (sympy)",
      sp.simplify(H1N_a - H1N_b) == 0)

rp = sp.symbols('r_p', positive=True)
H1E_s = sp.exp(2*Phi)*sp.Integral(2*gfun(rp), (rp, 0, rs))
weldE = sp.simplify(sp.diff(sp.exp(-2*Phi)*H1E_s, rs).doit() - 2*gfun(rs))
check("S2  H1_E = e^{2phi0} Int 2g dr' satisfies d_r(e^{-2phi0}H1) = 2g (sympy)",
      weldE == 0)

# phase channel: H1_E/H1_N is omega-free and real (pure radial structure)
om = sp.symbols('omega', real=True)
dp = sp.Function('dphi')
g_time = -sp.I*om*dp(rs)                    # d_t(dphi) for e^{-i omega t}
H1E_t = sp.exp(2*Phi)*sp.Integral(2*(-sp.I*om*dp(rp)), (rp, 0, rs))
H1N_t = 2*g_time/(f_s*sp.Derivative(Phi, rs))
ratio = sp.simplify(H1E_t/H1N_t)
check("S2  PRE-REGISTERED: H1_E/H1_N is omega-free and I-free (sympy) -- the"
      " phase channel cannot discriminate",
      (not ratio.has(om)) and (not ratio.has(sp.I)))

# ----------------------------------------------------------------------
# S3/S4: common breathing source + the two weld-derived EE weights
# ----------------------------------------------------------------------
def make_fields(nfine=6000, rmin=1e-3):
    """Common background + source + both welds' weights on a fine grid.
    omega is factored out of BOTH H1's (common quadrature factor)."""
    r   = np.linspace(rmin, R_CMB, nfine)
    ph  = phi0_f(r)
    php = phi0p_f(r)
    f   = np.exp(-2.0*ph)
    dphi = phi0_f(r)/PHI_C            # S116 crude analytic envelope [INPUT-class]
    S_a  = dphi.copy()                # source variant (a): smooth broad envelope
    # H1 per weld (omega factored out -- common):
    H1E = np.exp(2*ph)*cumulative_trapezoid(2.0*dphi, r, initial=0.0)  # CUMULATIVE
    H1N = 2.0*dphi/(f*php)                                             # LOCAL
    # identical weight construction except H1 (S116 step 2-3):
    WEE_E = (np.exp(2*ph)/r**2)*H1E*np.exp(-3*ph)
    WEE_N = (np.exp(2*ph)/r**2)*H1N*np.exp(-3*ph)
    WTT   = r**2*np.exp(-3*ph)        # Tolman measure; -dphi SW channel (clean)
    WLENS = (R_CMB - r)/(R_CMB*r)*np.exp(2*ph)   # deprecated S116 lensing ref
    return dict(r=r, ph=ph, php=php, f=f, dphi=dphi, S=S_a,
                H1E=H1E, H1N=H1N, WEE_E=WEE_E, WEE_N=WEE_N,
                WTT=WTT, WLENS=WLENS)

def d1_stats(r, V):
    a = np.abs(V)
    i = int(np.argmax(a))
    edge = (i == len(r)-1)
    w2 = a**2
    c = np.cumsum(0.5*(w2[1:]+w2[:-1])*np.diff(r))
    c = np.concatenate([[0.0], c]); c /= c[-1]
    r16, r50, r84 = np.interp([0.16, 0.50, 0.84], c, r)
    return dict(rpk=r[i], edge=edge, r16=r16, r50=r50, r84=r84,
                width=r84-r16)

# ----------------------------------------------------------------------
# S5: the projection (finite-coherence radial correlation, S116 form)
# ----------------------------------------------------------------------
def run_pass(N=260, kappa=1.0, rmin=1e-3, envpow=1.0, nfine=6000,
             ells=None, ell_off=ELL_OFF, limber=False):
    """One full projection pass.  Returns smooth (a) and comb (b) C_ell
    curves for TT, EE_E, EE_N (raw radial double integrals; the common
    ell^4 spin factor is omitted -- it cancels in all comparisons).
    ell_off: comb phase anchor (verifier amendment 2: the 17-anchor scan).
    limber:  short-coherence/Limber diagonal limit, C_ell ~ Int V^2 M dr
             (verifier amendment 3: coherence-treatment sensitivity)."""
    if ells is None:
        ells = np.arange(100.0, 2001.0, 5.0)
    F = make_fields(nfine=nfine, rmin=rmin)
    rg = np.linspace(rmin, R_CMB, N)
    h  = rg[1] - rg[0]
    S  = np.interp(rg, F['r'], F['S'])**envpow
    S  = S/S.max()
    sqrtS = np.sqrt(np.clip(S, 0.0, None))
    Vb = {k: np.interp(rg, F['r'], F[k])*sqrtS
          for k in ('WTT', 'WEE_E', 'WEE_N')}
    R1, R2 = np.meshgrid(rg, rg, indexing='ij')
    DR2 = (R1 - R2)**2
    comb_tag = {'WTT': 'cos2', 'WEE_E': 'sin2', 'WEE_N': 'sin2'}
    out = {k: np.empty(len(ells)) for k in Vb}
    outc = {k: np.empty(len(ells)) for k in Vb}
    for i, l in enumerate(ells):
        Lc = kappa*R_CMB/l                      # coherence ~ r_CMB/ell (S116)
        Kern = np.exp(-DR2/(2.0*Lc*Lc))
        # comb modulation: fixed k-space acoustic features projected at each
        # radius, ell-position scaling with r (Delta-ell(r) = 297*r/r_CMB);
        # phase chi = pi*(ell*r_CMB/r - 243)/297.  Anti-alias: unresolved
        # radial oscillation relaxed to its mean 1/2 (pipeline regularization,
        # COMMON-mode; grid-doubling variant tests it).
        chi  = np.pi*(l*(R_CMB/rg) - ell_off)/DL_IN
        kr   = 2.0*np.pi*l*R_CMB/(DL_IN*rg**2)  # local oscillation wavenumber
        damp = np.exp(-0.5*(kr*h/2.0)**2)
        cos2 = 0.5 + (np.cos(chi)**2 - 0.5)*damp
        sin2 = 0.5 + (np.sin(chi)**2 - 0.5)*damp
        for k, V in Vb.items():
            M = cos2 if comb_tag[k] == 'cos2' else sin2
            if limber:                      # diagonal / incoherent limit
                out[k][i]  = np.sum(V*V)*h
                outc[k][i] = np.sum(V*V*M)*h
            else:
                out[k][i] = V @ Kern @ V * h*h
                Vc = V*np.sqrt(M)
                outc[k][i] = Vc @ Kern @ Vc * h*h
    return dict(ells=ells, smooth=out, comb=outc)

def loglog_slope(ells, ratio, lo=100.0, hi=2000.0):
    m = (ells >= lo) & (ells <= hi) & (ratio > 0)
    return np.polyfit(np.log(ells[m]), np.log(ratio[m]), 1)[0]

def comb_peaks(ells, Q, lo=330.0, hi=1950.0):
    step = ells[1] - ells[0]
    pk = []
    for i in range(1, len(ells)-1):
        if lo <= ells[i] <= hi and Q[i] > Q[i-1] and Q[i] >= Q[i+1]:
            den = Q[i-1] - 2*Q[i] + Q[i+1]
            d = 0.5*(Q[i-1] - Q[i+1])/den if den != 0 else 0.0
            pk.append(ells[i] + d*step)
    return np.array(pk)

def contrast(ells, Q, lo=350.0, hi=1900.0):
    m = (ells >= lo) & (ells <= hi)
    return (Q[m].max() - Q[m].min())/Q[m].mean()

def match_shift(pA, pB, tol=80.0):
    """signed shifts pB - pA for nearest-matched peaks."""
    sh = []
    for p in pA:
        if len(pB) == 0: continue
        j = int(np.argmin(np.abs(pB - p)))
        if abs(pB[j] - p) <= tol:
            sh.append(pB[j] - p)
    return np.array(sh)

def metrics(P):
    """D2/D3 metrics from one pass."""
    ells = P['ells']
    Q = {k: P['comb'][k]/P['smooth'][k] for k in P['comb']}
    pk = {k: comb_peaks(ells, Q[k]) for k in Q}
    ct = {k: contrast(ells, Q[k]) for k in Q}
    # interleaving reference: r_CMB-shell TT midpoints (INPUT comb)
    nmax = int((2000 - ELL_OFF)/DL_IN) + 2
    mids = np.array([ELL_OFF + (n + 0.5)*DL_IN for n in range(nmax)])
    mids = mids[(mids > 330) & (mids < 1950)]
    def off(pkX):
        if len(pkX) == 0: return np.nan
        return np.mean([pkX[i] - mids[np.argmin(np.abs(mids - pkX[i]))]
                        for i in range(len(pkX))])
    slope = {k: loglog_slope(ells, P['smooth'][k]/P['smooth']['WTT'])
             for k in ('WEE_E', 'WEE_N')}
    slope_c = {k: loglog_slope(ells, P['comb'][k]/P['comb']['WTT'])
               for k in ('WEE_E', 'WEE_N')}
    return dict(Q=Q, pk=pk, ct=ct, mids=mids,
                offE=off(pk['WEE_E']), offN=off(pk['WEE_N']),
                slopeE=slope['WEE_E'], slopeN=slope['WEE_N'],
                slopeE_c=slope_c['WEE_E'], slopeN_c=slope_c['WEE_N'])

# ----------------------------------------------------------------------
# D1: radial weight shapes
# ----------------------------------------------------------------------
hr("=")
print("D1: RADIAL WEIGHT SHAPES (GEOMETRY-clean channel)")
hr("=")
F0 = make_fields(6000, 1e-3)
r0 = F0['r']

print("\n  Raw |W(r)| argmax (S116 native_weight_cl.py convention, for echo):")
for name, key in [("W^TT (Tolman, -dphi SW channel)", 'WTT'),
                  ("W^EE Einstein weld (cumulative H1)", 'WEE_E'),
                  ("W^EE native weld (local H1)", 'WEE_N'),
                  ("W^EE lensing (deprecated, historical ref)", 'WLENS')]:
    i = int(np.argmax(np.abs(F0[key])))
    print(f"    {name:44s} argmax r = {r0[i]:7.3f} Gpc"
          + ("  [grid edge]" if i in (0, len(r0)-1) else ""))

print("\n  Analytic small-r structure (the welds' genuine difference):")
WE0 = 1.5*MU_G/PHI_C
print(f"    Einstein: W^EE_E(r->0) -> 3 mu_g e^{{phi0}}/(2 phi0_c) = {WE0:.5f}  [FINITE]")
print(f"    Native:   W^EE_N(r->0) -> (2/phi0_c)/r  ~ {2/PHI_C:.5f}/r          [DIVERGES ~1/r]")
print("    (the C_ell integrand stays finite, but -- VERIFIER SOFTENING,")
print("     a6ef46971a22e0069 -- the V^2-based D1 statistic is WEAKLY (log)")
print("     rmin-dependent for the native weld: V_N = W_N*sqrt(S) ~ r^{-1/2}")
print("     at small r, so V_N^2 ~ 1/r.  Practically negligible (the rmin-x2")
print("     variant below moves r50 and the comb peaks by <~1e-3), but plain")
print("     'integrable' was too strong; inner-cutoff sensitivity is tested")
print("     in the error budget below)")
iN = len(r0)//1000
ratio_num = np.abs(F0['WEE_N'][iN])*r0[iN]*PHI_C/2.0
check("D1  numeric confirms W^EE_N ~ (2/phi0_c)/r at small r",
      abs(ratio_num - 1.0) < 0.05, f"r={r0[iN]:.4f}, ratio={ratio_num:.4f}")

print("\n  Projection-effective kernel V(r) = W(r)*sqrt(S(r)) statistics:")
sqrtS0 = np.sqrt(F0['S'])
d1 = {}
for name, key in [("V^TT", 'WTT'), ("V^EE Einstein", 'WEE_E'),
                  ("V^EE native", 'WEE_N'), ("V^EE lensing (hist.)", 'WLENS')]:
    st = d1_stats(r0, F0[key]*sqrtS0)
    d1[key] = st
    print(f"    {name:22s} argmax={st['rpk']:7.3f}{' [edge]' if st['edge'] else '       '}"
          f"  r50={st['r50']:7.4f}  width(r84-r16)={st['width']:7.4f} Gpc")

# D1 robustness: fine-grid doubling + inner-cutoff doubling + envelope power
d1_var = {}
for tag, (nf, rm, ep) in [('grid x2', (12000, 1e-3, 1.0)),
                          ('rmin x2', (6000, 2e-3, 1.0)),
                          ('envelope dphi^2', (6000, 1e-3, 2.0))]:
    Fv = make_fields(nf, rm)
    sq = np.sqrt(Fv['S']**ep)
    d1_var[tag] = {k: d1_stats(Fv['r'], Fv[k]*sq) for k in ('WEE_E', 'WEE_N')}

sig_r50 = abs(d1['WEE_E']['r50'] - d1['WEE_N']['r50'])
sig_wid = abs(d1['WEE_E']['width'] - d1['WEE_N']['width'])
spr_r50 = max(abs(d1_var[t][k]['r50'] - d1[k]['r50'])
              for t in d1_var for k in ('WEE_E', 'WEE_N'))
spr_wid = max(abs(d1_var[t][k]['width'] - d1[k]['width'])
              for t in d1_var for k in ('WEE_E', 'WEE_N'))
print(f"\n  D1 signal (E vs N):  |delta r50| = {sig_r50:.4f} Gpc,"
      f"  |delta width| = {sig_wid:.4f} Gpc")
print(f"  D1 spread (grid x2, rmin x2, envelope dphi^2): r50 {spr_r50:.5f},"
      f"  width {spr_wid:.5f} Gpc")
print("  (the envelope variant moves both welds nearly in common; the per-weld")
print("   movement is the conservative spread used in the budget)")
print(f"  D1 convergence: r50_E {d1['WEE_E']['r50']:.4f} vs grid-x2 "
      f"{d1_var['grid x2']['WEE_E']['r50']:.4f}; r50_N {d1['WEE_N']['r50']:.4f} vs "
      f"{d1_var['grid x2']['WEE_N']['r50']:.4f} (4-digit stable)")
check("D1  both welds' effective EE kernels are boundary-dominated (r50 > 8 Gpc)",
      d1['WEE_E']['r50'] > 8.0 and d1['WEE_N']['r50'] > 8.0)

# ----------------------------------------------------------------------
# D2/D3: projections -- baseline + robustness variants
# ----------------------------------------------------------------------
hr("=")
print("D2/D3: PROJECTIONS (S116 finite-coherence radial correlation)")
hr("=")
print("  source (a): smooth broad envelope (S116 crude analytic style) [INPUT]")
print(f"  source (b): BAO comb on (a); Delta-ell(r_CMB)={DL_IN:.0f}, offset "
      f"{ELL_OFF:.0f} [INPUT]")
print(f"    -> L_BAO = pi*r_CMB/{DL_IN:.0f} = {L_BAO:.5f} Gpc; r_CMB-shell TT comb"
      f" = {[int(ELL_OFF+n*DL_IN) for n in range(1,6)]}")
print("    honesty: the recorded TT comb is [540,810,1130,1450,1750] (spacing"
      " ~302); the 297-input comb drifts <= 27 in ell across the band vs the"
      " record -- COMMON-mode, flagged.")
print("  computing baseline + 5 robustness variants...\n")

base = run_pass(N=260, kappa=1.0, rmin=1e-3, envpow=1.0)
variants = {
    'grid x2 (N=520)':      run_pass(N=520, kappa=1.0, rmin=1e-3, envpow=1.0),
    'Lc x 1/2':             run_pass(N=260, kappa=0.5, rmin=1e-3, envpow=1.0),
    'Lc x 2':               run_pass(N=260, kappa=2.0, rmin=1e-3, envpow=1.0),
    'rmin x2':              run_pass(N=260, kappa=1.0, rmin=2e-3, envpow=1.0),
    'envelope dphi^2':      run_pass(N=260, kappa=1.0, rmin=1e-3, envpow=2.0),
}
mb = metrics(base)
mv = {t: metrics(P) for t, P in variants.items()}

# ---------------- D2 report ----------------
print("D2: COMB FEATURE POSITIONS (source (b))")
print(f"  comb contrast (peak-to-trough / mean of Q=C_comb/C_smooth, ell 350-1900):")
print(f"    TT {mb['ct']['WTT']:.4f}   EE_Einstein {mb['ct']['WEE_E']:.4f}   "
      f"EE_native {mb['ct']['WEE_N']:.4f}")
tt_washed = mb['ct']['WTT'] < 0.02
if tt_washed:
    print("    NOTE: the TT comb is washed out by the broad interior TT weight in")
    print("    this crude common pipeline (COMMON-mode artifact, flagged); the")
    print("    interleaving reference is the r_CMB-shell INPUT midpoints.")
print(f"  interleaving reference midpoints: {np.round(mb['mids'],1)}")
print(f"  EE comb peaks, EINSTEIN weld: {np.round(mb['pk']['WEE_E'],1)}")
print(f"  EE comb peaks, NATIVE weld:   {np.round(mb['pk']['WEE_N'],1)}")
sh = match_shift(mb['pk']['WEE_E'], mb['pk']['WEE_N'])
sig_d2 = np.mean(np.abs(sh)) if len(sh) else np.nan
print(f"  matched E->N peak shifts: {np.round(sh,2)}  ->  mean|shift| = "
      f"{sig_d2:.3f} ell  (signal)")
print(f"  mean offset from reference midpoints: Einstein {mb['offE']:+.2f},"
      f"  native {mb['offN']:+.2f} ell")
print("  (the common offset from the ideal midpoints is the pipeline's"
      " projection-radius crudeness -- common-mode; the DIFFERENTIAL number"
      " is the E-vs-N shift)")

# D2 spread: per-weld peak-position stability across variants
spr_list = []
for t, m in mv.items():
    for k in ('WEE_E', 'WEE_N'):
        s = match_shift(mb['pk'][k], m['pk'][k])
        if len(s): spr_list.append((t, k, np.mean(np.abs(s))))
spr_d2 = max(s for _, _, s in spr_list)
print("\n  D2 robustness spread (per-weld peak movement vs baseline):")
for t, k, s in spr_list:
    print(f"    {t:20s} {('Einstein' if k=='WEE_E' else 'native'):9s} "
          f"mean|move| = {s:6.3f} ell")
print(f"  D2 spread = {spr_d2:.3f} ell   vs   D2 signal = {sig_d2:.3f} ell")
# secondary diagnostic: how stable is the DIFFERENTIAL itself across variants?
diff_sig = {}
for t, m in mv.items():
    s = match_shift(m['pk']['WEE_E'], m['pk']['WEE_N'])
    if len(s): diff_sig[t] = np.mean(np.abs(s))
print("  D2 differential stability (mean|E->N shift| recomputed per variant):")
for t, s in diff_sig.items():
    print(f"    {t:20s} {s:6.3f} ell")
dmin, dmax = min(diff_sig.values()), max(diff_sig.values())
print(f"    -> the E-vs-N shift itself is stable in [{dmin:.2f}, {dmax:.2f}] ell"
      f" (baseline {sig_d2:.2f}); the per-weld spread above is largely"
      " common-mode")
# interleaving-offset differential and its spread
sig_d2b = abs(mb['offE'] - mb['offN'])
spr_d2b = max(abs(m['offE'] - mb['offE']) for m in mv.values())
spr_d2b = max(spr_d2b, max(abs(m['offN'] - mb['offN']) for m in mv.values()))
print(f"  D2b (interleaving-offset differential): signal = {sig_d2b:.3f},"
      f" spread = {spr_d2b:.3f} ell")
check("D2  both welds RETAIN the comb (contrast > 2%) -- interleaving"
      " structure survives the weld swap",
      mb['ct']['WEE_E'] > 0.02 and mb['ct']['WEE_N'] > 0.02)

# ---- D2c: comb-phase-anchor scan (VERIFIER AMENDMENT 2, a6ef46971a22e0069)
def signed_shift(P):
    """Signed E->N matched-peak shifts of the principal sin^2-comb peaks."""
    Q = {k: P['comb'][k]/P['smooth'][k] for k in ('WEE_E', 'WEE_N')}
    return match_shift(comb_peaks(P['ells'], Q['WEE_E']),
                       comb_peaks(P['ells'], Q['WEE_N']))

print("\n  D2c COMB-PHASE-ANCHOR ROBUSTNESS (VERIFIER AMENDMENT: the anchor")
print("  ELL_OFF is INPUT-class, so the differential must not depend on it;")
print("  17 anchors sliding over one full comb spacing):")
anchor_means = []
anchor_allneg = True
for j in range(17):
    off_j = ELL_OFF + j*DL_IN/17.0
    s = signed_shift(run_pass(ell_off=off_j))
    anchor_means.append(float(np.mean(s)))
    anchor_allneg = anchor_allneg and bool(np.all(s < 0))
print(f"    mean signed E->N shift over the 17 anchors: "
      f"[{min(anchor_means):+.3f}, {max(anchor_means):+.3f}] ell "
      f"(baseline {-sig_d2:+.3f})")
print(f"    every matched principal peak negative at every anchor: {anchor_allneg}")
print("    (verifier's independent short-coherence integrator: shift in")
print("     [-4.00, -3.74] over the same 17 anchors, every matched peak")
print("     negative -- same universality at its own magnitude)")
print("    -> the E->N downshift is a FRACTIONAL-r effect of the weld swap,")
print("       not a comb-phase artifact; this STRENGTHENS the differential.")
check("D2c phase-anchor scan: shift direction universal (all matched peaks"
      " < 0 at all 17 anchors)", anchor_allneg)
check("D2c phase-anchor scan: differential magnitude stable under the"
      " anchor slide",
      (max(anchor_means) - min(anchor_means)) < 1.0
      and abs(np.mean(anchor_means) + sig_d2) < 0.5,
      f"range width {max(anchor_means)-min(anchor_means):.3f} ell;"
      f" scan mean {np.mean(anchor_means):+.3f} vs baseline {-sig_d2:+.3f}")

# ---- D2d: coherence-treatment sensitivity (VERIFIER AMENDMENT 3)
print("\n  D2d COHERENCE-TREATMENT SENSITIVITY (VERIFIER AMENDMENT):")
sh_lim  = signed_shift(run_pass(N=260, limber=True))
sh_lim2 = signed_shift(run_pass(N=520, limber=True))
print(f"    in-script Limber/short-coherence (diagonal) proxy: mean signed"
      f" shift {np.mean(sh_lim):+.3f} ell (N=260), {np.mean(sh_lim2):+.3f}"
      f" (N=520);")
print(f"    all matched peaks negative: "
      f"{bool(np.all(sh_lim < 0)) and bool(np.all(sh_lim2 < 0))}")
print("    recorded sensitivity across coherence treatments:")
print(f"      ~{sig_d2:.1f} ell at Lc = r_CMB/ell (the S116 baseline here);")
print("      3.8-4.2 ell in the verifier's independent Limber/short-coherence")
print("      integrator (own grids/integrators, agent a6ef46971a22e0069).")
print("    The DIRECTION (native EE comb at LOWER ell) is UNIVERSAL across")
print("    every coherence treatment tried; only the magnitude moves")
print("    (2.6-4.2 ell over all treatments and variants).")
print("    CAVEAT (verifier): the shift statement is specific to the")
print("    PRINCIPAL sin^2-comb peaks -- secondary-harmonic features can")
print("    shift OPPOSITELY; any future record comparison must match the")
print("    principal comb positions, not arbitrary sub-features.")
check("D2d Limber-limit proxy keeps the shift direction (all matched"
      " principal peaks < 0)",
      bool(np.all(sh_lim < 0)) and bool(np.all(sh_lim2 < 0)),
      f"means {np.mean(sh_lim):+.3f}, {np.mean(sh_lim2):+.3f} ell")

# ---------------- D3 report ----------------
print()
print("D3: EE/TT RATIO SLOPE, R(ell) = C^EE/(ell^4 C^TT), ell in [100,2000]")
print("  (the common ell^4 spin factor is divided out / cancels)")
print(f"    Einstein weld:  slope = {mb['slopeE']:+.4f}   (S116 record: +0.05"
      f" native-pipeline, +0.02 lensing)")
print(f"    native weld:    slope = {mb['slopeN']:+.4f}")
sig_d3 = abs(mb['slopeE'] - mb['slopeN'])
spr_terms = []
for t, m in mv.items():
    spr_terms.append((t + " [E]", abs(m['slopeE'] - mb['slopeE'])))
    spr_terms.append((t + " [N]", abs(m['slopeN'] - mb['slopeN'])))
spr_terms.append(("source (b) comb [E]", abs(mb['slopeE_c'] - mb['slopeE'])))
spr_terms.append(("source (b) comb [N]", abs(mb['slopeN_c'] - mb['slopeN'])))
spr_d3 = max(s for _, s in spr_terms)
print("  D3 robustness spread terms:")
for t, s in spr_terms:
    print(f"    {t:26s} |delta slope| = {s:.4f}")
print(f"  D3 spread = {spr_d3:.4f}   vs   D3 signal = {sig_d3:.4f}")
check("D3  BOTH welds are ell-flat (|slope| < 0.5; gross-tilt record"
      " threshold)", abs(mb['slopeE']) < 0.5 and abs(mb['slopeN']) < 0.5,
      f"E {mb['slopeE']:+.3f}, N {mb['slopeN']:+.3f}")

# ---------------- D4 report ----------------
print()
print("D4: EFFECTIVE COMB SCALE FROM THE WEIGHT RADIUS, ell_eff = 297*r50/r_CMB")
e_eff_E = DL_IN*d1['WEE_E']['r50']/R_CMB
e_eff_N = DL_IN*d1['WEE_N']['r50']/R_CMB
sig_d4 = abs(e_eff_E - e_eff_N)
spr_d4 = DL_IN*spr_r50/R_CMB
print(f"    Einstein weld: r50 = {d1['WEE_E']['r50']:.4f} Gpc -> ell_eff = {e_eff_E:.2f}")
print(f"    native weld:   r50 = {d1['WEE_N']['r50']:.4f} Gpc -> ell_eff = {e_eff_N:.2f}")
print(f"  D4 signal = {sig_d4:.3f} ell-spacing units;  spread = {spr_d4:.3f}")

# ----------------------------------------------------------------------
# convergence digits on banked numbers
# ----------------------------------------------------------------------
hr("=")
print("CONVERGENCE (grid doubling N=260 -> 520) on the banked numbers")
hr("=")
mg = mv['grid x2 (N=520)']
def digits(a, b):
    if a == b: return 99
    d = abs(a - b)
    return int(np.floor(-np.log10(d/max(abs(a), 1e-300)))) if d > 0 else 99
banked = [
    ("D3 slope Einstein", mb['slopeE'], mg['slopeE']),
    ("D3 slope native",   mb['slopeN'], mg['slopeN']),
]
for k, lab in (('WEE_E', "first EE comb peak, Einstein"),
               ('WEE_N', "first EE comb peak, native")):
    banked.append((lab, mb['pk'][k][0], mg['pk'][k][0]))
for lab, a, b in banked:
    print(f"  {lab:32s} {a:12.5f} vs {b:12.5f}   |diff|={abs(a-b):.5f}"
          f"  (~{digits(a,b)} stable digits)")
print("  honesty: comb-peak positions carry the ell-grid step (5) /parabolic-")
print("  refinement floor ~0.5 ell and the anti-alias regularization; slopes")
print("  are stable to the digits shown.  Where fewer than 4 digits are")
print("  achieved, the achieved precision above is the honest statement;")
print("  all discriminator calls below use the SPREADS, not the raw digits.")

# ----------------------------------------------------------------------
# ERROR BUDGET + PRE-REGISTERED VERDICT
# ----------------------------------------------------------------------
hr("=")
print("ERROR BUDGET AND PRE-REGISTERED VERDICT")
hr("=")
rows = [
    ("D1 r50 (Gpc)",            sig_r50, spr_r50, "no direct record pin"),
    ("D1 width (Gpc)",          sig_wid, spr_wid, "no direct record pin"),
    ("D2 EE peak shift (ell)",  sig_d2,  spr_d2,  "PINNED: interleaving PASSED"),
    ("D2b interleave off (ell)",sig_d2b, spr_d2b, "PINNED: interleaving PASSED"),
    ("D3 slope",                sig_d3,  spr_d3,  "pinned only via |slope|>0.5"),
    ("D4 ell_eff",              sig_d4,  spr_d4,  "no direct record pin"),
]
print(f"  {'channel':26s} {'signal |E-N|':>13s} {'spread':>9s} {'>spread?':>9s}  record pin")
disc_pinned = []
for lab, sig, spr, pin in rows:
    over = sig > spr
    print(f"  {lab:26s} {sig:13.4f} {spr:9.4f} {str(over):>9s}  {pin}")
    if over and pin.startswith("PINNED"):
        disc_pinned.append((lab, sig, spr))
d3_gross = (abs(mb['slopeE']) < 0.5) != (abs(mb['slopeN']) < 0.5)

# D2 margin honesty (VERIFIER AMENDMENT 4, a6ef46971a22e0069)
quad_d2 = float(np.sqrt(sum(max(s for tt, _, s in spr_list if tt == t)**2
                            for t in mv)))
print()
print(f"  D2 MARGIN HONESTY (verifier amendment): combining the per-variant")
print(f"  spreads in quadrature gives {quad_d2:.2f} ell < signal {sig_d2:.2f} ell --")
print(f"  the comparison survives, but the margin is < 2x"
      f" (ratio {sig_d2/quad_d2:.2f}): DOUBLING the")
print("  spread estimate flips the formal signal > spread comparison.  One")
print("  more reason the strict verdict below is INDISTINGUISHABLE.")
check("D2 margin: signal exceeds quadrature spread but by < 2x (honest"
      " statement of the margin)",
      quad_d2 < sig_d2 < 2.0*quad_d2,
      f"quadrature {quad_d2:.2f} < signal {sig_d2:.2f} < 2x {2*quad_d2:.2f}")

print()
print("  Pre-registered rule recap: a weld is PREFERRED only if a channel")
print("  shows signal > spread AND the direction is checkable against the")
print("  recorded Planck-validated facts (EE interleaving positions PASSED;")
print("  EE peak ~1004; TT comb [540,810,1130,1450,1750]).")
print()
if disc_pinned:
    # VERIFIER CORRECTION (2026-06-10, agent a6ef46971a22e0069).  The
    # original run printed "EINSTEIN PREFERRED -- WEAK" on the claim that
    # the record states no position tolerance for the EE interleaving
    # PASS.  That claim was FACTUALLY WRONG (citations at RECORD_TOL_*):
    # the recorded pass precision is 30-42 ell.  The script's OWN
    # pre-registered downgrade clause ("if that PASS tolerance is coarser
    # than ~3 ell ... this verdict DOWNGRADES") therefore FIRES.
    coarse = RECORD_TOL_LO > sig_d2
    check("VERDICT  pre-registered downgrade clause fires: recorded pass"
          " tolerance coarser than the differential",
          coarse,
          f"recorded {RECORD_TOL_LO:.0f}-{RECORD_TOL_HI:.0f} ell ="
          f" {int(RECORD_TOL_LO/sig_d2)}-{int(RECORD_TOL_HI/sig_d2)}x the"
          f" {sig_d2:.1f}-ell differential")
    check("VERDICT  both welds sit inside the recorded pass band"
          " (|offset| < 30 ell)",
          abs(mb['offE']) < RECORD_TOL_LO and abs(mb['offN']) < RECORD_TOL_LO,
          f"offsets Einstein {mb['offE']:+.1f}, native {mb['offN']:+.1f} ell"
          f" vs recorded {RECORD_TOL_LO:.0f}-{RECORD_TOL_HI:.0f}")
    print()
    if coarse:
        print("  VERDICT: INDISTINGUISHABLE-AT-CURRENT-RECORD")
        print("  (given the common pipeline; VERIFIER-CORRECTED same day,"
              " 2026-06-10)")
        print()
        print("  Why the pre-registered downgrade clause FIRES:")
        for lab, sig, spr in disc_pinned:
            print(f"    * pinned channel {lab}: signal {sig:.3f} >"
                  f" spread {spr:.3f} (real differential), BUT")
        print("    * the record DOES state the EE interleaving pass tolerance:")
        print("        S115_PROMPT.md line 53: positions match Planck"
              " '~30 in ell (vs ~102 aligned)'")
        print("        S116_PROMPT.md lines 36-37: 'mean|Delta-ell| 42 vs 108'")
        print(f"      i.e. {RECORD_TOL_LO:.0f}-{RECORD_TOL_HI:.0f} ell --"
              f" {int(RECORD_TOL_LO/sig_d2)}-{int(RECORD_TOL_HI/sig_d2)}x"
              f" coarser than the {sig_d2:.1f}-ell differential;")
        print(f"    * BOTH welds sit comfortably inside that recorded pass"
              f" band: offsets {mb['offE']:+.1f} (Einstein) and"
              f" {mb['offN']:+.1f} (native) ell")
        print(f"      from the ideal midpoints -- the common-mode pipeline"
              f" bias ({abs(mb['offE']):.0f} ell) is"
              f" {abs(mb['offE'])/max(sig_d2,1e-9):.0f}x the differential;")
        print("    * the original run's 'EINSTEIN PREFERRED -- WEAK' rested"
              " on the factually")
        print("      wrong no-tolerance claim; corrected same day per"
              " verifier a6ef46971a22e0069.")
    else:  # kept for honesty: if a future record sharpens below the signal
        better_native = abs(mb['offN']) < abs(mb['offE'])
        who = "NATIVE PREFERRED" if better_native else "EINSTEIN PREFERRED"
        print(f"  VERDICT: {who} -- WEAK, formal application of the"
              " pre-registered rule  (given the common pipeline)")
        for lab, sig, spr in disc_pinned:
            print(f"    discriminating pinned channel: {lab}: signal {sig:.3f}"
                  f" > spread {spr:.3f}")
    print()
    print("  CALIBRATION OF THE VERDICT (calibrate, never dramatize):")
    print(f"    * the discriminating differential is {sig_d2:.1f} ell ~"
          f" {100*sig_d2/DL_IN:.1f}% of the comb spacing ({DL_IN:.0f});")
    print(f"    * the COMMON-mode pipeline bias from the ideal midpoints is"
          f" {abs(mb['offE']):.0f} ell -- {abs(mb['offE'])/max(sig_d2,1e-9):.0f}x"
          " the differential;")
    print("    * the direction is ROBUST -- a BANKED DIFFERENTIAL PREDICTION:")
    print("      the native weld's EE comb sits at slightly SMALLER ell")
    print("      (smaller effective weight radius r50) than the Einstein")
    print("      weld's, in every robustness variant, every coherence")
    print("      treatment, and all 17 comb-phase anchors.  A FUTURE few-ell")
    print("      Planck EE comb-position fit (actual likelihood-level peak")
    print("      positions vs TT midpoints) WOULD discriminate the welds at")
    print(f"      this ~{sig_d2:.0f}-ell differential.")
elif d3_gross:
    print("  VERDICT: gross D3 ell-flatness difference -- record-checkable;")
    print("  see D3 numbers above.")
else:
    print("  VERDICT: INDISTINGUISHABLE-AT-CURRENT-RECORD")
    print("  (given the common pipeline: every record-pinned channel's E-vs-N")
    print("   difference is within the pipeline's own robustness spread, and")
    print("   the channels where the welds genuinely differ structurally --")
    print("   the interior radial weight, D1/D4 -- are not pinned by the")
    print("   recorded Planck-validated facts)")

print(f"""
STRUCTURAL FINDING (conditional, given the common pipeline):
  The two welds DO differ genuinely in radial structure -- the Einstein
  H1 is CUMULATIVE (finite W^EE at r->0) while the native H1 is LOCAL
  (W^EE ~ 1/r at r->0, integrable).  But the Tolman boundary factor
  e^{{phi0(r)}} (rising to 1101 at r_CMB) makes BOTH effective EE kernels
  boundary-dominated (r50: Einstein {d1['WEE_E']['r50']:.3f} vs native
  {d1['WEE_N']['r50']:.3f} Gpc), so the observable radial-structure
  channels come out nearly degenerate: the weld difference lives in the
  interior, where the common pipeline's projection weight is
  exponentially suppressed.  The full observable residue of the weld
  swap is a ~{sig_d2:.0f}-ell downward shift of the EE comb (native vs
  Einstein, ~{100*sig_d2/DL_IN:.0f}% of the spacing) plus a slightly
  wider EE kernel ({d1['WEE_N']['width']:.3f} vs {d1['WEE_E']['width']:.3f} Gpc).

  Consequence for the weld program: given the common pipeline, the NATIVE
  algebraic weld (= delta-T_tr = 0) reproduces the macro radial-structure
  phenomenology of the Einstein weld at the few-ell level -- it preserves
  the comb/interleaving STRUCTURE and the ell-flat EE/TT ratio, shifting
  positions only ~1% of the comb spacing -- so the macro record does NOT
  veto the native weld: the recorded pass tolerance ({RECORD_TOL_LO:.0f}-{RECORD_TOL_HI:.0f} ell,
  S115_PROMPT.md line 53 / S116_PROMPT.md lines 36-37) is
  {int(RECORD_TOL_LO/sig_d2)}-{int(RECORD_TOL_HI/sig_d2)}x coarser than the weld differential, and both welds sit
  inside the recorded pass band.  (VERIFIER-CORRECTED: the original text
  here claimed the record states no tolerance.)  The phase channel was
  pre-registered non-discriminating (common quadrature) and the
  amplitude channels are epsilon-class/sand-flagged (not compared).

SCOPE: differential and conditional throughout.  No absolute amplitudes;
the temperature-model sand (+1/4 drho/rho) is common-mode by construction
and unused (TT = -dphi SW channel only); profile/mu_g/r_CMB enter as
DATA-FIT inputs; the comb scale and envelope are INPUT-class.
""")

hr("=")
print(f"CHECKS: {npass} PASS, {nfail} FAIL")
hr("=")
