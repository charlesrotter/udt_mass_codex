#!/usr/bin/env python3
"""
mass_cost_ladder.py  --  FREQUENCY-VS-COST split test (STRUCTURE-FIRST, DATA-BLIND)
================================================================================
Combine two banked results:
  (1) quantized_carrier_structure_results.md : postulate-A quantization gives an
      INTRINSIC discrete well, but the eigen-FREQUENCY binding is POWER-LAW in
      depth D (V_eff sees only log-derivatives of v0, linear in D).
  (2) B1_mass_dilation_cost_results.md : the MASS is the dilation COST,
      m(r)=(c^2 r/2G)(1-e^{-2phi}), EXACT native functional, EXPONENTIAL in depth.

HYPOTHESIS (frequency-vs-cost split): the discrete LADDER comes from quantization,
the MASS of each quantized state is its dilation COST (B1), not hbar*omega. Since
cost is undifferentiated e^{phi} (exp in D) while frequency is its log-derivative
(power-law in D), the exponential hierarchy may live in mass-as-COST.

Agent: claude-opus-4-8[1m]. Date: 2026-06-19. NOT canon. No git commit.
DATA-BLIND: no lepton/mass/ratio/wall numbers anywhere (contract 26fc757).
Anti-numerology: no rational promoted to evidence; we test FORM, not values.

We do NOT fit an exponential to manufacture one. We DERIVE the cost functional
exactly (sympy) and SHOW its analytic D-dependence, then numerically corroborate.
We HONESTLY test whether postulate A selects discrete DEPTHS D_n (the load-bearing
question), or whether "quantized depths" is a smuggled mechanism.
"""
import sympy as sp
import numpy as np
from scipy.linalg import eigh_tridiagonal

def hr(s): print("\n"+"="*78+"\n"+s+"\n"+"="*78)

# ============================================================================
hr("PART 1 -- EXACT mass-as-COST functional (B1's MS mass), symbolic")
# ============================================================================
# Native dilation profile (same native-like family as the quantization doc):
#   v0(r) = -D f(r),  phi == v0  (dilation depth; deep negative core -> 0 exterior).
# B1's Misner-Sharp dilation cost (EXACT native form, B1 script [4]):
#   m(r) = (c^2 r / 2G)(1 - e^{-2 phi(r)})
# Here phi = v0 = -D f(r) is NEGATIVE in the core (a WELL / time-dilation deficit),
# so e^{-2phi} = e^{+2 D f} grows EXPONENTIALLY as D deepens. (1 - e^{-2phi}) is the
# dilation deficit-from-unity = the cost.
r, D, a, c2G = sp.symbols('r D a c2G', positive=True)
f = sp.exp(-(r/a)**2)                 # generic native-like core shape f(r): 1 at r=0 -> 0 exterior
phi = -D*f                            # phi = v0 = -D f   (depth D; NEGATIVE core)
m_cost = (c2G * r / 2) * (1 - sp.exp(-2*phi))   # MS dilation cost, EXACT
m_cost = sp.simplify(m_cost)
print(" phi(r) = v0(r) = -D*f(r),  f(r)=exp(-(r/a)^2)   [native-like core, depth D]")
print(" MS dilation COST  m(r) = (c^2 r/2G)(1 - e^{-2 phi}) :")
sp.pprint(m_cost)

# The "cost of the state at depth D" = a depth-characteristic of the WHOLE profile,
# not a single r. Two natural scalar cost measures (we report BOTH, neither chosen
# to favor the hypothesis):
#  (A) peak cost amplitude: the cost at the core, leading exponential in D:
#        as r->0, phi->-D, (1-e^{-2phi}) = (1 - e^{2D})  ~  -e^{2D}  for large D.
#  (B) integrated cost weight INT (1 - e^{-2phi}) dr  (the B1 "INT(1-e^{-2phi})" measure
#        flagged in the quantization doc as exp-in-depth).
hr("PART 1b -- the COST amplitude vs the FREQUENCY potential: WHY one is exp, one is power")
# Frequency route (quantization doc): V_eff built from V_L = (1/2)s' - (1/4)s^2, s=2 v0'.
v0 = phi
s = 2*sp.diff(v0, r)
V_L = sp.Rational(1,2)*sp.diff(s, r) - sp.Rational(1,4)*s**2
V_L = sp.simplify(V_L)
print(" FREQUENCY route potential  V_L = (1/2)s' - (1/4)s^2,  s=2 v0' :")
sp.pprint(V_L)
print("\n  -> V_L is built from s = 2 v0' = 2*(-D f') = -2D f'(r): LINEAR in D in the (1/2)s'")
print("     term, QUADRATIC in D in the -(1/4)s^2 term. POLYNOMIAL in D. (power-law).")
print("\n COST route amplitude  (1 - e^{-2 phi}) = (1 - e^{+2 D f}) :")
sp.pprint(sp.simplify(1 - sp.exp(-2*phi)))
print("  -> contains e^{2 D f}: EXPONENTIAL in D (the depth amplitude UNDIFFERENTIATED).")
print("""
 STRUCTURAL DERIVATION OF THE SPLIT (the load-bearing point):
   The dilation amplitude is  e^{phi} = e^{-D f}  (exp in D).
   * The eigen-FREQUENCY sees phi only through V_L, which depends on v0' (a derivative).
     d/dr of (-D f) = -D f'  -> the D comes DOWN as a multiplicative POLYNOMIAL factor;
     the exponential that survives is e^{-D f} only inside, but the BINDING SCALE that
     sets omega^2 is the COEFFICIENT ~ D^2 (from s^2). Differentiation converts the
     'D in the exponent' into 'D as a polynomial coefficient' -> POWER-LAW in D.
   * The COST sees phi through e^{-2 phi}=e^{+2 D f} DIRECTLY (no derivative). The D stays
     IN THE EXPONENT -> EXPONENTIAL in D.
   => cost restores exactly the exponential that frequency differentiated away. CONFIRMED
      analytically, not fitted.""")

# ============================================================================
hr("PART 2 -- THE LADDER AXIS: what indexes the family? (honest, not assumed)")
# ============================================================================
print("""
 Candidates for the ladder index (from the two docs):
   - radial n : SHALLOW (1 stable level then tachyon; quantization doc Finding 2). NOT it.
   - angular l : the CHARGE axis (already banked: N=3, q=1/3). Charge diversity, not a
       same-charge generation family. NOT the generation axis.
   - depth D  : the state's location in the dilation well. The candidate.
   - composite l x n : limited by the shallow n.

 THE LOAD-BEARING QUESTION (must not be smuggled): does POSTULATE A actually select
 DISCRETE DEPTHS D_n, or is 'quantized depths' an invented mechanism?

 Postulate A = Bohr-Sommerfeld on the RADIAL wavefunction in a FIXED V_eff(D): it
 quantizes the radial node number n AT A GIVEN DEPTH D. It does NOT, by itself, produce
 a TOWER of depths D_n. The depth D is a CONTINUOUS profile parameter (how deep the well
 is), set by the matter/amplitude of the state -- NOT a quantum number handed out by
 oint p dq over r. So 'the same charge-1 object quantized to sit at discrete depths D_n'
 is NOT delivered by postulate A as stated. We FLAG this and test what WOULD discretize D.""")

# ============================================================================
hr("PART 3 -- IF depths were discrete: structure of mass_n = cost(D_n) (form, data-blind)")
# ============================================================================
# We do NOT assume a spacing of D_n (that would be a smuggled value). We instead ask:
# GIVEN any increasing sequence of depths D_n, what is the STRUCTURE of the cost?
# Report the analytic cost(D) and its ratio structure; the D_n spacing is left OPEN.
Dn = sp.symbols('D_n', positive=True)
# peak/core cost amplitude (r->0): cost_core(D) = (c2G * r_core/2)(1 - e^{2D})  [r_core fixed scale]
# integrated cost weight:
Dval_sym = sp.symbols('Dv', positive=True)
print(" cost-amplitude(D) ~ (1 - e^{+2D f_core})  -> for deep D, ~ -e^{2D} (magnitude e^{2D}).")
print(" RATIO of cost amplitudes at two depths (core, leading):")
ratio = sp.exp(2*Dn)/sp.exp(2*sp.Symbol('D_m'))
print("   |cost(D_n)| / |cost(D_m)|  ~  e^{2(D_n - D_m)}   (leading, deep).")
print("   => SCALE-FREE: c^2/2G, r_core, a ALL CANCEL in the ratio. Only the depth")
print("      DIFFERENCE (D_n - D_m) survives -> a clean dimensionless exponential in")
print("      depth-spacing. (This is the B1 'exponential in depth' restored.)")
print("""
 So IF the depths are an increasing sequence D_n, mass_n-as-COST is:
   * EXPONENTIAL in depth (analytic, not fitted): |m_n| ~ e^{2 D_n} (leading, deep core),
     vs the frequency route's m_n^2 = l(l+1) - D_n^k (power-law). CONFIRMED the split.
   * SCALE-FREE in ratios: m_n/m_0 ~ e^{2(D_n - D_0)}, all dimensionful prefactors cancel.
   * the ladder VALUES depend entirely on the (unknown, NOT-chosen) depth spacing {D_n}.""")

# ============================================================================
hr("PART 4 -- NUMERICAL corroboration (exp vs power), DATA-BLIND, profile-robust")
# ============================================================================
# For a SCAN of depths D (treated as a continuous parameter, NO spacing chosen), compute:
#  (i)  FREQUENCY binding (V_inf - E_0) from the eigensolve  -> expect POWER-LAW in D
#  (ii) COST amplitude   |1 - e^{-2 phi_core}| and INT|1-e^{-2phi}|dr -> expect EXP in D
# Then fit exp-in-D vs power-in-D to EACH and report which wins (form, not value).

def Veff(rr, Dval, aval, l):
    t = (rr/aval)**2
    et = np.exp(-t); e2t = np.exp(-2*t)
    VL = (2*Dval/aval**2)*et*(1-2*t) - (4*Dval**2*t/aval**2)*e2t
    return l*(l+1) + VL

def freq_binding(Dval, aval=1.0, l=1, R=20., h=0.004, r_core=0.02):
    N = int((R-r_core)/h); rr = r_core + h*np.arange(1,N+1)
    V = Veff(rr,Dval,aval,l); main = 2.0/h**2 + V; off = -1.0/h**2*np.ones(N-1)
    E = eigh_tridiagonal(main, off, select='i', select_range=(0,4), eigvals_only=True)
    return l*(l+1) - np.sort(E)[0]   # V_inf - E_0

def cost_measures(Dval, aval=1.0, R=20., h=0.004, r_core=0.02):
    rr = np.arange(r_core, R, h)
    phi = -Dval*np.exp(-(rr/aval)**2)        # v0
    cost_density = (1 - np.exp(-2*phi))      # 1 - e^{-2phi}, exp in D (e^{+2D f})
    core_amp = abs(1 - np.exp(2*Dval*np.exp(-(r_core/aval)**2)))   # |cost| at core
    integ = np.trapz(np.abs(cost_density), rr)                     # integrated cost weight
    return core_amp, integ

Ds = np.arange(0.6, 3.41, 0.2)   # stay below tachyon D* for the FREQUENCY comparison
fb=[]; ca=[]; ci=[]
for Dv in Ds:
    fb.append(freq_binding(Dv)); c,i = cost_measures(Dv); ca.append(c); ci.append(i)
fb=np.array(fb); ca=np.array(ca); ci=np.array(ci)

def form_test(x, y, label):
    g = y>0
    se = np.polyfit(x[g], np.log(y[g]),1); re = np.std(np.log(y[g])-np.polyval(se,x[g]))
    sp_ = np.polyfit(np.log(x[g]), np.log(y[g]),1); rp = np.std(np.log(y[g])-np.polyval(sp_,np.log(x[g])))
    verdict = "EXPONENTIAL e^{%.2f D}"%se[0] if re<rp else "POWER-LAW D^%.2f"%sp_[0]
    print(f"  {label:34s}: exp-resid={re:.2e}  pow-resid={rp:.2e}  -> {verdict}")
    return 'exp' if re<rp else 'pow'

print(" Fit each quantity to exp-in-D vs power-in-D (smaller residual wins). DATA-BLIND.\n")
form_test(Ds, fb, "FREQUENCY binding (V_inf - E_0)")
form_test(Ds, ca, "COST core amplitude |1-e^{-2phi}|")
form_test(Ds, ci, "COST integrated weight INT|.|dr")
print("\n  D scan      =", np.round(Ds,2))
print("  freq binding=", np.round(fb,3))
print("  cost core   =", np.round(ca,3))
print("  cost integ  =", np.round(ci,3))

# ============================================================================
hr("PART 5 -- INTRINSIC-vs-BOX test for the COST (R-dependence)")
# ============================================================================
print(" Is the cost amplitude/ratio R-(box)-dependent? Core amplitude is r-LOCAL (R-indep)")
print(" by construction; the INTEGRATED weight could pick up the box. Test both vs R.\n")
for Dv in [1.0, 2.0, 3.0]:
    row=[]
    for R in [8.,16.,32.,64.]:
        c,i = cost_measures(Dv, R=R); row.append((R,c,i))
    print(f"  D={Dv}:")
    for R,c,i in row:
        print(f"    R={R:5.1f}: core_amp={c:12.5f}  integ_weight={i:12.5f}")
print("""
 READ: the CORE cost amplitude is exactly R-independent (local to the core; e^{2D} fixed
 by D, not by the cell). The INTEGRATED weight saturates (f->0 exterior, integrand->0),
 so it is also R-independent once R >> a. => the COST ladder is INTRINSIC, not box-controlled,
 for BOTH measures -- the box is irrelevant to the dilation cost (unlike the frequency
 continuum). The exponential lives in a box-free quantity.""")

# ============================================================================
hr("PART 6 -- # of stable rungs: does the cost route escape the tachyon cap?")
# ============================================================================
print("""
 The FREQUENCY route caps stable rungs at ~1 because omega^2=E>0 is REQUIRED (a real
 standing wave); past D* ~ 2.6 the ground omega^2 < 0 (tachyon). Does mass-as-COST escape?

 KEY DISTINCTION (honest): the cost is defined for ANY depth D (it is a geometric mass
 aspect, always real and positive-magnitude). BUT a PHYSICAL state still must be a valid
 standing-wave carrier solution: omega^2 = E > 0. The cost does NOT relax that constraint
 -- it only changes WHAT WE CALL THE MASS of a state that already exists. So:

   * if the states are the RADIAL levels at fixed D: still ~1 stable (tachyon cap UNCHANGED;
     cost relabels its mass but does not add rungs). NO multi-rung family this way.
   * if the states are at DIFFERENT depths D_n: each D_n must independently host a STABLE
     (omega^2>0) carrier. The tachyon cap D* bounds the DEEPEST admissible D_n. So the
     number of rungs = number of admissible discrete depths in (0, D*) -- which requires a
     DEPTH-SELECTOR (Part 2's open question) AND all D_n < D*.""")
# how many depths below D* -- but D* itself, and any spacing, are NOT ours to choose.
print(" => # stable rungs is GATED by (a) the missing depth-selector and (b) the D* cap.")
print("    The cost functional ITSELF imposes no upper limit on rungs; the CARRIER STABILITY")
print("    constraint (omega^2>0, depth<D*) does. Cost does NOT by itself lift the tachyon cap.")

print("\nDONE.")
