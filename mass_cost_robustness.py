#!/usr/bin/env python3
"""
mass_cost_robustness.py  -- profile-robustness of the COST exponential + the
depth-selector honesty check.  STRUCTURE-FIRST, DATA-BLIND. NOT canon.
Agent: claude-opus-4-8[1m]. 2026-06-19.

(A) Repeat the exp-vs-power form test for the COST amplitude across the SAME four
    native-like profiles the quantization doc used (gaussian/lorentzian/expcore/sech2),
    to certify the exponential is profile-robust (not a gaussian artifact).
(B) Honest depth-selector probe: is there ANY native quantity whose DISCRETENESS would
    hand out discrete depths D_n? Enumerate candidates and mark native/import/unaudited.
"""
import numpy as np
def hr(s): print("\n"+"="*78+"\n"+s+"\n"+"="*78)

# four native-like core shapes f(r): 1 at r=0 -> 0 exterior. phi=v0=-D f(r).
def f_gauss(r,a): return np.exp(-(r/a)**2)
def f_lorentz(r,a): return 1.0/(1.0+(r/a)**2)
def f_expcore(r,a): return np.exp(-np.abs(r)/a)
def f_sech2(r,a): return 1.0/np.cosh(r/a)**2
profiles = {'gaussian':f_gauss,'lorentzian':f_lorentz,'expcore':f_expcore,'sech2':f_sech2}

def cost_core(Dval, fcore):
    # core (r->0) cost magnitude |1 - e^{-2 phi}| with phi=-D f, f(0)=1 -> |1 - e^{2D}|
    return abs(1 - np.exp(2*Dval*fcore))   # fcore = f(r_core) ~ 1

def cost_integ(Dval, ffun, a=1.0, R=30., h=0.004, r_core=0.02):
    rr = np.arange(r_core,R,h); phi=-Dval*ffun(rr,a)
    return np.trapezoid(np.abs(1-np.exp(-2*phi)), rr)

def form_test(x,y):
    g=y>0
    se=np.polyfit(x[g],np.log(y[g]),1); re=np.std(np.log(y[g])-np.polyval(se,x[g]))
    sp_=np.polyfit(np.log(x[g]),np.log(y[g]),1); rp=np.std(np.log(y[g])-np.polyval(sp_,np.log(x[g])))
    if re<rp: return f"EXP e^{{{se[0]:.2f} D}}  (exp-resid={re:.1e} < pow-resid={rp:.1e})"
    return f"POWER D^{sp_[0]:.2f}  (pow-resid={rp:.1e} < exp-resid={re:.1e})"

hr("(A) COST exponential -- profile-robustness across 4 native-like cores")
Ds = np.arange(0.6,3.41,0.2)
print(" core cost amplitude |1-e^{-2phi}| (r->0):")
for name,ffun in profiles.items():
    fcore = ffun(0.02,1.0)
    y = np.array([cost_core(Dv,fcore) for Dv in Ds])
    print(f"   {name:11s}: {form_test(Ds,y)}")
print("\n integrated cost weight INT|1-e^{-2phi}|dr:")
for name,ffun in profiles.items():
    y = np.array([cost_integ(Dv,ffun) for Dv in Ds])
    print(f"   {name:11s}: {form_test(Ds,y)}")
print("""
 READ: the COST is EXPONENTIAL in depth for ALL FOUR native-like cores (the e^{-2phi}
 amplitude carries the depth undifferentiated). Profile-robust, exactly mirroring how the
 quantization doc found the FREQUENCY power-law profile-robust. The split is structural,
 not a profile artifact: same four profiles, frequency=power, cost=exp.""")

hr("(B) THE DEPTH-SELECTOR -- honest enumeration (the load-bearing obstruction)")
print("""
 mass_n=cost(D_n) needs a SEQUENCE of discrete depths {D_n}. Where could it come from?
 Each candidate tagged NATIVE / POSTULATE-A / IMPORT / UNAUDITED:

  C1. Radial Bohr-Sommerfeld over r (postulate A as applied in the quantization doc):
      quantizes the RADIAL NODE n at FIXED depth D. Does NOT discretize D.   -> POSTULATE-A,
      but WRONG VARIABLE: it indexes n, not D. Gives ~1 stable rung (tachyon). NOT a depth tower.

  C2. Bohr-Sommerfeld over the DEPTH/amplitude DOF itself (oint p_D dD = (n+1/2)hbar):
      would quantize the well DEPTH as a collective coordinate. This requires the AMPLITUDE
      to be a genuine canonical DOF with its own conjugate momentum and an effective potential
      U(D) with a confining shape -- i.e. the NONLINEAR BREATHER back-reaction omega(A). That
      object is UNBUILT (flagged in the quantization doc + timelive). -> UNAUDITED / NOT-YET-NATIVE.
      It is the RIGHT shape for the candidate, but it is NOT delivered by postulate A as scoped
      (postulate A is hbar+spin+statistics; applying Bohr-Sommerfeld to the depth coordinate is
      LEGAL under it, but needs the breather potential U(D), which must be DERIVED, not posited).

  C3. Topological/winding selecting depth: B1 says charge axis (l, N=3) is the discrete
      topological structure; it is CHARGE diversity, not a same-charge depth family.   -> NATIVE
      but WRONG AXIS (charge, not generation).

  C4. Closed-time / non-stationary selector (#57, single-cell-spectrum memory's lead): a
      periodic-time condition could discretize the depth via a temporal Bohr-Sommerfeld.
      -> UNAUDITED (the time-live carrier exists; the closed-time quantization is NOT built).

  C5. Imposing a depth spacing by hand (e.g. evenly/log spaced D_n): -> IMPORT / SMUGGLED VALUE.
      FORBIDDEN (chose-a-value). We do NOT do this. Any specific spacing would be a fit.

 VERDICT: postulate A (radial) gives n, NOT D (C1). The depth-tower candidate that WOULD give
 mass_n=cost(D_n) needs C2 (depth/breather Bohr-Sommerfeld with a DERIVED U(D)) or C4
 (closed-time) -- BOTH UNBUILT. So mass-as-cost RESTORES THE EXPONENTIAL FORM and the
 SCALE-FREE RATIO and the INTRINSIC (box-free) character, but the DISCRETE LADDER OF DEPTHS
 -- the thing that makes it a multi-rung family -- is NOT yet closed natively. The exponential
 is real; the rungs are not yet selected.""")
print("DONE.")
