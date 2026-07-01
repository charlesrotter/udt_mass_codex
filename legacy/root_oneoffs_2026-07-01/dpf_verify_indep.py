#!/usr/bin/env python3
"""
INDEPENDENT blind adversarial verifier for the Delta_p_F claim.
Agent: blind-verifier (own machinery). Date 2026-06-14.
DATA-BLIND: no lepton wall numbers loaded; contract 26fc757 NOT opened.

Own machinery (own sympy). Tests the SIX kill-shots A-F.
The strategy: this is a PRIOR-CONFIRMING positive (a clean forced ratio
from the cohomological sector) -- per hypothesis discipline, attack HARDEST,
default skeptical, hunt for ASSEMBLY (the {3,5,7} failure mode).
"""
import sympy as sp

P=[0]; F=[0]
def ck(name, cond):
    if cond: P[0]+=1; print(f"  PASS  {name}")
    else: F[0]+=1; print(f"  FAIL  {name}")

q   = sp.Rational(1,3)
eta = q/6
gamma, c, f, m = sp.symbols('gamma c f m', positive=True)

print("="*72)
print("KILL-SHOT A : Does the genuine O(c^2) charge correction FACTORIZE")
print("              as -p_F * W * (c^2/gamma^2) * exp(-eta/2 d)?")
print("="*72)
# The banked charge functional is p_F = y dM0/dy - M0 (mass_audit:52), with
# m(y,u)=(y/2)(1-f) (mass_audit:50).  The OFF-BARE angular correction is
# named P_F, 100% angular-sourced, "P_F vanishes on spherical flows"
# (mass_audit:103-104).  CRUCIAL FINDING: NO explicit P_F[c] functional is
# banked ANYWHERE (grep of spectrum + mass_audit: only the SCALAR
# 'Delta_p_F ~ -2.5% at gamma=1, c=0=>0').  So the multiplicative form
# CANNOT be checked against a closed functional -- it is ASSEMBLED from
# four separately-banked scalars.  We test what CAN be tested:
#  (A1) does the assembled product reproduce the ONE banked scalar anchor
#       (sign<0, c=0 vanish, O(c^2), ~few-% at gamma=1)?
#  (A2) is the *ORDER* of multiplication (W outside the atten, c^2/gamma^2
#       a plain prefactor) forced by anything, or a free choice?

# Reconstruct the challenger's assembled object with MY OWN symbols:
W = {'trace':sp.Rational(1,12),'A3':sp.Rational(1,4),'S5':sp.Rational(5,12)}
depth = {'trace':0,'A3':2,'S5':4}   # the claimed d=2L
def dpf(sec):
    return -(gamma/2)*W[sec]*(c**2/gamma**2)*sp.exp(-eta/2*depth[sec])

# A1: the banked-anchor reproduction
for sec in ['trace','A3','S5']:
    ck(f"A1 c->0 vanish [{sec}]", sp.simplify(dpf(sec).subs(c,0))==0)
    ck(f"A1 sign<0 [{sec}] (for c,gamma>0)", sp.simplify(dpf(sec)).subs({gamma:1,c:sp.Rational(1,2)})<0)
# Order O(c^2): leading c-power
for sec in ['A3']:
    ser = sp.series(dpf(sec), c, 0, 3).removeO()
    ck(f"A1 leading power is c^2 (no c^1) [{sec}]",
       sp.simplify(ser - dpf(sec))==0 and sp.limit(sp.diff(dpf(sec),c).subs(c,0),c,0)==0)

# A2: the assembly-ORDER ambiguity test.  Build ALTERNATIVE equally-"natural"
# assemblies that ALSO vanish at c=0, are O(c^2), negative, and respect the
# SAME banked factors -- but multiply in a DIFFERENT order / placement.
print("""
  A2: assembly-order ambiguity -- alternative orderings that obey the SAME
      banked anchors (c=0 vanish, O(c^2), sign<0) but give DIFFERENT ratios:""")
def alt_W_inside_atten(sec):  # put W inside the exponent's weighting
    return -(gamma/2)*(c**2/gamma**2)*W[sec]*sp.exp(-eta/2*depth[sec]*W[sec]*12)
def alt_atten_on_W(sec):      # attenuate the WEIGHT not the whole product
    return -(gamma/2)*(W[sec]*sp.exp(-eta/2*depth[sec]))*(c**2/gamma**2)  # same as orig
def alt_depth_dim(sec):       # d=dim (the REJECTED reading) instead of 2L
    dim={'trace':1,'A3':3,'S5':5}
    return -(gamma/2)*W[sec]*(c**2/gamma**2)*sp.exp(-eta/2*dim[sec])
def alt_depth_L(sec):         # d=L instead of 2L
    L={'trace':0,'A3':1,'S5':2}
    return -(gamma/2)*W[sec]*(c**2/gamma**2)*sp.exp(-eta/2*L[sec])

orig_ratio = sp.simplify(dpf('S5')/dpf('A3'))
print("    ORIGINAL  S5/A3 =", orig_ratio, "=", sp.nsimplify(orig_ratio,[sp.E]))
for nm,fn in [('d=dim (rejected)',alt_depth_dim),('d=L',alt_depth_L),
              ('W inside atten',alt_W_inside_atten)]:
    r = sp.simplify(fn('S5')/fn('A3'))
    print(f"    {nm:18s} S5/A3 =", sp.nsimplify(r,[sp.E]),
          " (numeric", float(r),")")
print("""    => ALL obey the same banked anchors. The RATIO depends entirely on
       the (unforced) depth-count and assembly placement. The product
       structure is NOT pinned by the banked anchors alone.""")

print()
print("="*72)
print("KILL-SHOT B : the d = 2L junction count -- forced or a 'reading'?")
print("="*72)
# Claim: an SO(3) order-L mode adds d=2L Dirichlet/parity constraints across
# the D=0 crease, because |m|=1..L gives L doublets (+-m) = 2L.  Independent
# count of REAL same-minus mirror-fold junction conditions for a spin-L field
# crossing a Z2 fixed surface:
print("""  A real-analytic same-minus (Z2) mirror fold imposes ONE parity
  condition per independent field component at the fixed surface:
  either the component or its normal derivative vanishes (even/odd).
  For an SO(3) order-L harmonic the multiplicity of independent angular
  components is 2L+1 (m=-L..L), NOT 2L.  The '2L' drops the m=0 member.""")
for L in [0,1,2]:
    dim=2*L+1
    print(f"    L={L}: irrep dim 2L+1 = {dim};  2L = {2*L};  L = {L}")
print("""  The challenger's '2L = number of (+-m) PAIRS, |m|=1..L' is ONE reading
  (count signed doublets, drop m=0).  Equally defensible counts:
    - 2L+1 (all components get a parity BC at a Z2 surface) -> the dim count
    - L+1  (count |m|=0..L distinct magnitudes)
    - 2L+1 - (parity-even count) ...
  NONE is derived from an actual junction-condition computation; the doc
  ITSELF flags d=2L as HYPOTHESIS-GRADE (dpf_results lines 168-173, 220-226).
  The {3,5,7} verifier rejected 'depth=dim'; 'depth=2L=dim-1' is the SAME
  class of unforced reading, merely shifted by one.  It is NOT forced.""")
# show the e^{-1/18} factor is ENTIRELY a function of (d_S5 - d_A3):
dd = sp.symbols('Delta_d')
print("  inter-sector exp factor = exp(-eta/2 * Delta_d), eta/2=1/36:")
for label,val in [('Delta_d=2 (2L)',2),('Delta_d=2 (dim:5-3)',2),
                  ('Delta_d=1 (L:2-1)',1)]:
    print(f"    {label}: exp(-{val}/36) =", sp.nsimplify(sp.exp(-sp.Rational(val,36)),[sp.E]),
          float(sp.exp(-sp.Rational(val,36))))
print("""  NOTE: d=2L and d=dim give the SAME Delta_d=2 here (both differ by 2
  between A3 and S5), so the e^{-1/18} is robust to that particular swap --
  but d=L gives Delta_d=1 => e^{-1/36}, a DIFFERENT number.  So the ratio's
  exponential IS reading-dependent (L vs 2L).""")

print()
print("="*72)
print("KILL-SHOT C : the floor c^2/gamma^2 and the weight W(P)=Tr(P)/12")
print("="*72)
# floor: from |X_t(0)|^2 = gamma^2 + c^2 (mass_audit:48 banked exact).
jet_norm = gamma**2 + (-c)**2
ck("C floor: |X_t|^2 = gamma^2 + c^2 (banked, reproduced)", sp.simplify(jet_norm-(gamma**2+c**2))==0)
ck("C floor ratio a_ang/a_mono = c^2/gamma^2", sp.simplify((c**2/4)/(gamma**2/4)-c**2/gamma**2)==0)
print("""  C weight: W(P)=Tr(P)/12 is, per the spectrum doc (sec 17), a CANDIDATE
  rule ('suggests', 'candidate') defined from (1/36)BB^T=(1/12)P_T8 on the
  TRACELESS T8=A3+S5 part only.  Tr(P_A3)=3, Tr(P_S5)=5 give W=1/4, 5/12 --
  FORCED *as a readout of T8*.  BUT W(trace)=1/12 EXTRAPOLATES the rule to
  the trace direction, which is NOT in T8 (T8 is by definition traceless).
  W(trace) is an extension, not the banked rule.  For the S5/A3 RATIO the
  trace weight is irrelevant, so W_S5/W_A3 = 5/3 is forced GIVEN the
  candidate readout.  The readout rule itself is candidate-grade upstream.""")
ck("C W_S5/W_A3 = 5/3", sp.simplify(W['S5']/W['A3']-sp.Rational(5,3))==0)

print()
print("="*72)
print("KILL-SHOT D : seal placement -- odd/Dirichlet boundary, not bulk?")
print("="*72)
# rho = b - f q a, b*=-c, a*=gamma.  rho sigma-odd; c is the odd insertion.
a_star, b_star = gamma, -c
rho = b_star - f*q*a_star
rho_sig = (-b_star) - f*q*(-a_star)
ck("D rho is sigma-ODD (rho -> -rho)", sp.simplify(rho_sig+rho)==0)
ck("D c-insertion is the odd part of rho", sp.simplify((rho - rho.subs(c,0)) - (-c))==0)
print("""  The parity dichotomy (sigma-odd -> Dirichlet) and Xi=dTheta EXACT (Stokes
  delivers the angular content at the seal) are BANKED (w6/w7, h1_types).
  So the c-channel genuinely lands in the odd/Dirichlet seal sector -- this
  placement is FORCED (sign of b*=-c is odd; det g4 ~ rho^2).  *** BUT ***
  this licenses 'a boundary charge correction exists, O(c^2), at the seal';
  it does NOT by itself dictate that the correction EQUALS the assembled
  product p_F*W*(c^2/g^2)*atten.  Placement is solid; the FORMULA is the gap.""")

print()
print("="*72)
print("KILL-SHOT E : ratio data-blind / no tuning")
print("="*72)
ratio = sp.simplify(dpf('S5')/dpf('A3'))
ck("E ratio = (5/3) e^{-1/18}", sp.simplify(ratio - sp.Rational(5,3)*sp.exp(-sp.Rational(1,18)))==0)
ck("E m and gamma cancel in the ratio (no per-cell datum)",
   sp.simplify(sp.diff(ratio,gamma))==0 and len((dpf('S5')/dpf('A3')).free_symbols & {m})==0)
print("  numeric (5/3)e^{-1/18} =", float(sp.Rational(5,3)*sp.exp(-sp.Rational(1,18))))
print("""  GIVEN the assembled form + d=2L, m and gamma DO cancel: the ratio is a
  pure number, data-blind (no wall number entered the construction; I did
  not open the contract).  HOWEVER 'data-blind' != 'forced': the number is
  forced ONLY conditional on (a) the multiplicative assembly and (b) d=2L,
  both of which are reading-grade (kill-shots A2, B).  Change either and the
  ratio changes (e.g. d=L -> (5/3)e^{-1/36}).  No wall leak; but the
  forced-ness is conditional on unforced choices.""")

print()
print("="*72)
print(f"INDEPENDENT VERIFIER TOTALS  PASS={P[0]}  FAIL={F[0]}")
print("="*72)
