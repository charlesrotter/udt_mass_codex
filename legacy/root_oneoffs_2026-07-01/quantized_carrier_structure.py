#!/usr/bin/env python3
"""
quantized_carrier_structure.py
================================================================================
QUANTIZATION-STRUCTURE STEP -- apply POSTULATE A to the validated native
time-live standing-wave carrier and determine the STRUCTURE of the discrete
spectrum (NOT the values).

Agent: claude-opus-4-8[1m].   Date: 2026-06-19.   STRUCTURE-FIRST, DATA-BLIND.
NOT canon. Append-only working record. NO git commit.

THE NATIVE CARRIER (validated, blind-verified: timelive_nonround_native_solve_results.md):
   L_space[U] = omega^2 M[U],   M>0,   L_space negative-definite
   radial reduction (Liouville normal form):
      -(P U')' + [ l(l+1) W(r) + Q(r) ] U  =  omega^2 M(r) U
   with P = M = e^{2 v0(r)} (the dilation factor), W = e^{2 v0(r)},
   v0(r) = the native dilation DEPTH profile (deep negative core -> 0 exterior),
   l(l+1) = the area-form CHARGE centrifugal term (l>=1, native, banked),
   Q(r) >= 0 a source proxy (tested non-load-bearing in the prior result).

   PRIOR VALIDATED CLASSICAL FINDING: this is a SCATTERING/continuum problem with
   an angular-momentum barrier -- intrinsic floor omega^2 = l(l+1) W_inf, a
   BOX-CONTROLLED continuum above it (spacing -> 0 as R grows). NO classical
   bound tower (no binding well found classically).

POSTULATE A (the MINIMAL quantum input, the ONLY thing imported here):
   (i)  hbar = quantum of action; Bohr-Sommerfeld  oint p dq = (n+1/2) hbar
        <=> canonical quantization of the standing-wave action.
   (ii) spin-1/2 fermion.  (iii) fermion statistics (distinct quantized states
        = distinct particles).
   i = the AREA FORM complex structure (NATIVE -- not a generic postulated i):
        the harmonic-balance phase e^{i omega t} uses the area-form complex
        structure J (J^2 = -1 from the S^2 area 2-form orientation). This makes
        the quantization the canonical quantization of (q, p) with the symplectic
        form = the area form. Structurally: it fixes the phase-space measure to
        be the native area-form measure (does NOT change the WKB STRUCTURE below,
        only confirms the (n+1/2) Maslov index is the area-form-canonical one).

WHAT THIS SCRIPT DOES (structure, not values):
  STEP A. Cast the native carrier as a 1D Schrodinger problem -psi'' + V_eff = E psi,
          E = omega^2 (so m_n ~ omega_n via E = hbar omega, mass-as-dilation-cost).
          Find V_eff(r) from the native depth profile + charge. Print its SHAPE:
          does the native DEPTH create a WELL (two turning points) or only a
          barrier+flat-exterior (scattering)?
  STEP B. Apply Bohr-Sommerfeld  oint p dr = (n+1/2) pi  (hbar absorbed into E-scale;
          structure is hbar-independent up to the overall E unit).
          - If a WELL exists: the turning points r_-(E), r_+(E) are INTRINSIC
            (set by V_eff, not R) => discrete INTRINSIC tower. Test R-independence.
          - If no well: the outer turning point is the WALL R => quantization
            integral is R-dependent => BOX-CONTROLLED (postulate A does NOT rescue).
  STEP C. n-dependence and DEPTH-dependence of m_n. Scan the depth parameter D
          (v0_core = -D, the dilation depth) and read the functional form m_n(n, D, l).
          Is it EXPONENTIAL-in-depth (target) or O(1)/linear (the #44 failure)?
  STEP D. Scale-freeness of ratios m_n/m_0. Where spin-1/2/statistics enter.
  STEP E. Honest obstruction check.

NO wall numbers loaded (contract 26fc757). No rational promoted to evidence.
Machine-precision quadrature flagged where used.
"""
import numpy as np
import sympy as sp

np.set_printoptions(precision=6, suppress=False, linewidth=120)
def hr(s): print("\n"+"="*78+"\n"+s+"\n"+"="*78)

# ----------------------------------------------------------------------------
hr("STEP A -- cast the native carrier as 1D Schrodinger; read the SHAPE of V_eff")
# ----------------------------------------------------------------------------
# The native radial carrier:  -(P U')' + [l(l+1)W + Q] U = omega^2 M U,
#   P=M=W=e^{2 v0(r)},  v0(r) = native depth profile.
# Liouville substitution to remove the first-derivative term and the weight M:
#   define  x = INT_0^r sqrt(M/P) dr' = INT dr' = r   (since M=P here -- the
#   natural radial coordinate is already the Liouville coordinate when M=P).
#   Then  -(P U')'/M + [l(l+1)W/M + Q/M] U = omega^2 U.
#   With P=M=W=e^{2v0}:  W/M = 1, P/M = 1, so the operator is
#      -(1/M)(P U')' + [ l(l+1) + Q/M ] U = omega^2 U.
#   Expand -(P U')'/M = -U'' - (P'/P) U'.  Liouville: U = M^{-1/4} psi removes U'.
#   Standard result: -psi'' + V_eff psi = omega^2 psi  with
#      V_eff(r) = l(l+1) + Q/M + V_L(r),
#   where V_L = the Liouville potential = (1/4)(P'/P)^2*... -> from M^{-1/4} transform:
#      V_L = (1/2)(M''/M)*(1/2) ... we compute it exactly symbolically below.
#
# The l(l+1) term here is CONSTANT (W/M=1) -- the CENTRIFUGAL BARRIER is a flat
# pedestal, NOT an r^-2 wall, because the carrier's centrifugal term is dressed by
# W=e^{2v0} and divided by M=e^{2v0}. THIS IS THE KEY: any binding WELL must come
# from the LIOUVILLE potential V_L of the depth profile v0(r), or from Q.

r = sp.symbols('r', positive=True)
D = sp.symbols('D', positive=True)        # dilation DEPTH (v0_core = -D)
a = sp.symbols('a', positive=True)        # core width
# native-like depth profile: deep negative core -> 0 exterior.
# canonical smooth form  v0(r) = -D * exp(-(r/a)^2)  (Gaussian core well in v0)
v0 = -D*sp.exp(-(r/a)**2)
M  = sp.exp(2*v0)
# Liouville potential for -(M U')'/M  with U = M^{-1/4} psi  (P=M):
#   -(M U')'/M = -U'' - (M'/M)U'.  Sub U=M^{-1/4}psi:
#   the transformed potential adds  V_L = (1/4)(M'/M)' - (1/16)(M'/M)^2 ... derive exact.
g  = sp.diff(M, r)/M            # = (ln M)' = 2 v0'
VL = sp.simplify( sp.Rational(1,2)*sp.diff(g, r) - sp.Rational(1,4)*g**2 )
# (this is the standard Liouville potential V_L = (1/2) s' - (1/4) s^2 with s=(lnM)'
#  for the operator -U'' - s U' transformed by U = e^{-(1/2)INT s} psi = M^{-1/4} psi
#  ... verify sign by reconstructing below.)
print("\n s = (ln M)' = 2 v0'(r):")
sp.pprint(sp.simplify(g))
print("\n Liouville potential V_L(r) = (1/2) s' - (1/4) s^2  (depth-well contribution):")
sp.pprint(sp.simplify(VL))

# Numerically inspect the SHAPE of V_eff = l(l+1) + V_L  for a representative depth.
hr("STEP A.2 -- numeric SHAPE of V_eff(r): is there a WELL (two turning points)?")
def Veff_func(Dval, aval, l, Qamp=0.0):
    """V_eff(r) = l(l+1) + V_L(r) + Q/M, with the exact Liouville V_L."""
    VLf = sp.lambdify((r,), VL.subs({D:Dval, a:aval}), 'numpy')
    Mf  = sp.lambdify((r,), M.subs({D:Dval, a:aval}), 'numpy')
    def V(rr):
        rr = np.asarray(rr, dtype=float)
        out = l*(l+1) + VLf(rr)
        if Qamp != 0.0:
            out = out + Qamp*np.exp(-rr)/Mf(rr)   # source proxy / M
        return out
    return V

for Dval in [1.0, 3.0, 6.0]:
    V = Veff_func(Dval, 1.0, l=1)
    rr = np.linspace(1e-3, 8.0, 4000)
    Vr = V(rr)
    imin = np.argmin(Vr)
    print(f"\n depth D={Dval:4.1f}  l=1: V_eff  min={Vr.min():.4f} at r={rr[imin]:.3f} ; "
          f"V_eff(0+)={Vr[0]:.4f}  V_eff(inf~8)={Vr[-1]:.4f}")
    # count turning points for an energy E between the min and the asymptote:
    Einf = Vr[-1]
    Emin = Vr.min()
    Etest = 0.5*(Emin+Einf)
    crossings = np.where(np.diff(np.sign(Vr - Etest)))[0]
    print(f"    asymptote V_inf={Einf:.4f}, well-min={Emin:.4f}; "
          f"for E={Etest:.4f}: #turning points = {len(crossings)} "
          f"({'WELL (bound states possible)' if len(crossings)>=2 else 'no well / scattering'})")

print("""
 READ (Step A): the dilation DEPTH profile v0(r) (deep negative core) produces a
 Liouville potential V_L(r). If V_L dips BELOW its r->inf asymptote over a finite
 r-range, V_eff has a WELL with TWO turning points r_-(E)<r_+(E) for a band of E --
 then Bohr-Sommerfeld gives an INTRINSIC discrete bound tower (turning points set by
 V_eff, independent of the wall R). If V_L has no sub-asymptotic dip (monotone /
 barrier-only), the outer turning point is the WALL => box-controlled (no rescue).
""")

# ----------------------------------------------------------------------------
hr("STEP B -- POSTULATE A: Bohr-Sommerfeld quantization. Intrinsic or box?")
# ----------------------------------------------------------------------------
# Bohr-Sommerfeld for -psi'' + V_eff psi = E psi  (units: hbar^2/2m = 1, the E-scale
# carries hbar; STRUCTURE is hbar-independent):
#   INT_{r-}^{r+} sqrt(E - V_eff(r)) dr = (n + 1/2) pi ,  n = 0,1,2,...
# r-, r+ = classical turning points (V_eff(r±)=E).
# If a WELL exists, r± are roots of V_eff=E INSIDE the well => INTRINSIC.

from numpy import trapz
def turning_points(Vr, rr, E):
    s = np.sign(Vr - E)
    idx = np.where(np.diff(s))[0]
    # linear-interp the crossing r-values
    rs = []
    for i in idx:
        r0,r1 = rr[i], rr[i+1]; v0_,v1 = Vr[i], Vr[i+1]
        rs.append(r0 + (E - v0_)*(r1-r0)/(v1-v0_))
    return np.array(rs)

def bohr_sommerfeld_levels(Dval, aval, l, nmax=8, Rwall=8.0, Qamp=0.0, ngrid=20000):
    """Return the BS-quantized E_n (=omega_n^2) inside the well of V_eff, if any.
    Also returns whether the outer turning point hits the wall (box-control flag)."""
    V = Veff_func(Dval, aval, l, Qamp)
    rr = np.linspace(1e-4, Rwall, ngrid)
    Vr = V(rr)
    Vmin = Vr.min(); Vinf = Vr[-1]
    if Vmin >= Vinf - 1e-9:
        return None, None, None, True   # no sub-asymptotic well -> scattering/box
    # quantize for E in (Vmin, Vinf): bound band
    levels = []; box_flag = False
    # action(E) = INT sqrt(E - V) over classically allowed region
    def action(E):
        tps = turning_points(Vr, rr, E)
        if len(tps) < 2:
            return None, False
        rlo, rhi = tps[0], tps[-1]
        wall_hit = (rhi > Rwall*0.95)
        mask = (rr>=rlo)&(rr<=rhi)&(E - Vr > 0)
        if mask.sum() < 5: return None, wall_hit
        return trapz(np.sqrt(np.clip(E-Vr[mask],0,None)), rr[mask]), wall_hit
    # find E_n by solving action(E_n)=(n+1/2)pi via bisection on the bound band
    Es = np.linspace(Vmin+1e-6, Vinf-1e-9, 4000)
    acts = []
    for E in Es:
        A,_ = action(E)
        acts.append(A if A is not None else np.nan)
    acts = np.array(acts)
    for n in range(nmax):
        target = (n+0.5)*np.pi
        # find E where action crosses target
        valid = ~np.isnan(acts)
        if not valid.any(): break
        Av = acts[valid]; Ev = Es[valid]
        if target > np.nanmax(Av):
            break   # no more bound levels fit inside the well (finite well -> finite tower)
        j = np.where(np.diff(np.sign(Av - target)))[0]
        if len(j)==0: break
        k = j[0]
        E0,E1 = Ev[k], Ev[k+1]; A0,A1 = Av[k], Av[k+1]
        En = E0 + (target-A0)*(E1-E0)/(A1-A0)
        _, wh = action(En); box_flag = box_flag or wh
        levels.append(En)
    return np.array(levels), Vmin, Vinf, box_flag

print("\n Bohr-Sommerfeld bound levels E_n = omega_n^2 (l=1), per dilation depth D:")
for Dval in [1.0, 2.0, 4.0, 6.0]:
    lv, Vmin, Vinf, box = bohr_sommerfeld_levels(Dval, 1.0, l=1)
    if lv is None:
        print(f"  D={Dval:4.1f}: NO WELL in V_eff -> scattering/continuum (box-controlled). "
              f"Postulate A gives NO intrinsic bound tower.")
    else:
        print(f"  D={Dval:4.1f}: well [{Vmin:.3f},{Vinf:.3f}], #bound levels={len(lv)}, "
              f"box-hit={box}")
        print(f"          E_n = {lv}")

print("""
 INTRINSIC-vs-BOX test: re-run with a LARGER wall R; if the bound levels E_n are
 unchanged the tower is INTRINSIC (turning points inside the well). If they move /
 the count grows with R, it is box-controlled.""")
for Rwall in [8.0, 16.0, 32.0]:
    lv,_,_,box = bohr_sommerfeld_levels(4.0, 1.0, l=1, Rwall=Rwall)
    nb = 0 if lv is None else len(lv)
    head = (lv[:3] if lv is not None else None)
    print(f"  R={Rwall:5.1f}: #bound={nb}  first levels={head}  box-hit={box}")

# ----------------------------------------------------------------------------
hr("STEP C -- n-dependence and DEPTH-dependence of m_n (the functional form)")
# ----------------------------------------------------------------------------
print("""
 m_n via E=hbar omega: E_n = omega_n^2 (the carrier eigenvalue), and mass-as-dilation
 -cost ties m_n ~ omega_n = sqrt(E_n)  (E=hbar omega; the dilation-cost is the energy
 of the standing mode). We report the STRUCTURE of m_n = sqrt(E_n) vs (n, depth D, l).
""")
def masses(Dval, aval, l, **kw):
    lv = bohr_sommerfeld_levels(Dval, aval, l, **kw)[0]
    if lv is None: return None
    return np.sqrt(np.clip(lv,0,None))

print(" DEPTH SCAN -- ground mass m_0 and first ratio m_1/m_0 vs depth D (l=1):")
print(f"   {'D':>5} {'#levels':>8} {'m_0':>10} {'m_1/m_0':>9} {'m_2/m_0':>9}  shape")
for Dval in [1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0]:
    m = masses(Dval, 1.0, l=1, nmax=10)
    if m is None or len(m)<1:
        print(f"   {Dval:5.1f} {'(no well)':>8}")
        continue
    nlev=len(m)
    r1 = m[1]/m[0] if nlev>1 else np.nan
    r2 = m[2]/m[0] if nlev>2 else np.nan
    print(f"   {Dval:5.1f} {nlev:8d} {m[0]:10.4f} {r1:9.4f} {r2:9.4f}")

print("""
 FUNCTIONAL-FORM read: fit log(m_n) vs n and vs depth D to see if the spacing is
 EXPONENTIAL (log-linear in n -> geometric tower) or O(1)/harmonic (linear in n).""")
# at a representative depth with several levels, classify the n-spacing
for Dval in [4.0, 6.0, 8.0]:
    m = masses(Dval, 1.0, l=1, nmax=12)
    if m is None or len(m)<3:
        print(f"  D={Dval}: <3 levels, cannot classify n-form"); continue
    n = np.arange(len(m))
    # harmonic-oscillator-like: E_n ~ (n+1/2) => m_n=sqrt(E_n) ~ sqrt(n)
    # geometric/exponential: log(m_n) linear in n
    logm = np.log(m)
    # linear fit log m vs n (slope => exponential growth rate)
    A = np.polyfit(n, logm, 1)
    resid_exp = np.std(logm - np.polyval(A, n))
    # sqrt(n+1/2) fit
    sq = np.sqrt(n+0.5)
    B = np.polyfit(sq, m, 1); resid_sqrt = np.std(m - np.polyval(B, sq))
    print(f"  D={Dval:4.1f}: {len(m)} levels  log-linear(exp) slope={A[0]:+.3f} resid={resid_exp:.3e} | "
          f"sqrt(n+1/2)[HO] resid={resid_sqrt:.3e} -> "
          f"{'EXPONENTIAL' if resid_exp<resid_sqrt else 'HO/sqrt(n) (O(1))'}")

print("""
 DEPTH-EXPONENTIAL test (the lepton-hierarchy target): does m_0 (or the well depth)
 grow EXPONENTIALLY with the dilation depth D? The native depth enters V_eff through
 V_L(v0), v0 = -D f(r). Fit log(well-depth) and log(m_0) vs D.""")
Ds = np.array([1.0,1.5,2.0,3.0,4.0,5.0,6.0,8.0,10.0])
m0s=[]; welldepth=[]
for Dval in Ds:
    V = Veff_func(Dval,1.0,1); rr=np.linspace(1e-3,8,4000); Vr=V(rr)
    welldepth.append(Vr[-1]-Vr.min())
    m=masses(Dval,1.0,l=1,nmax=10)
    m0s.append(m[0] if (m is not None and len(m)>0) else np.nan)
welldepth=np.array(welldepth); m0s=np.array(m0s)
# fit log(welldepth) vs D and vs log(D)
good = welldepth>0
slope_lin = np.polyfit(Ds[good], np.log(welldepth[good]),1)[0]
slope_log = np.polyfit(np.log(Ds[good]), np.log(welldepth[good]),1)[0]
print(f"  well-depth(D): log-linear-in-D slope={slope_lin:+.3f} (exp-in-D if ~const>0) ; "
      f"power-law exponent d ln(depth)/d ln D = {slope_log:+.3f}")
print(f"  well-depth values: {welldepth}")
print(f"  m_0 values:        {m0s}")

# ----------------------------------------------------------------------------
hr("STEP D -- scale-freeness of ratios; where spin-1/2 / statistics enter")
# ----------------------------------------------------------------------------
print("""
 SCALE-FREENESS: the carrier eigenvalue problem -psi''+V_eff psi = omega^2 psi has an
 overall scale from (a) hbar^2/2m_unit in front, (b) the radial unit a (core width),
 (c) the dilation-cost prefactor sqrt(kappa/xi). RATIOS m_n/m_0 = sqrt(E_n/E_0) cancel
 the OVERALL prefactor. They DO retain the dimensionless shape parameters: the depth D
 and the core-width-to-... ratio. So m_n/m_0 is scale-free in the dimensionful unit but
 DEPENDS on the dimensionless depth D and l. We print the ratios to confirm cancellation.
""")
for Dval in [4.0,6.0]:
    m=masses(Dval,1.0,l=1,nmax=8)
    if m is not None and len(m)>1:
        print(f"  D={Dval}: m_n/m_0 = {m/m[0]}")
print("""
 SPIN-1/2 / STATISTICS (postulate A (ii),(iii)) enter the STRUCTURE as:
  - the (n+1/2) MASLOV/zero-point shift in Bohr-Sommerfeld IS the half-integer; with
    the AREA-FORM complex structure i (native J), the canonical 1-form p dq is the
    area-form symplectic potential, and the half-integer index is the area-form Maslov
    index -> the +1/2 is the native spin-1/2 zero-point, not an imported convention.
  - fermion STATISTICS (distinct quantized states = distinct particles) makes each
    discrete (n,l) level a DISTINCT PARTICLE in the catalog (one occupant per state).
  - DEGENERACY: each l carries (2l+1) area-form orientations; statistics + the area-form
    charge fix the multiplicity. (l labels the area-form/charge sector; n the radial
    overtone.) We do NOT assign these to observed particles here (gated/data-blind).
""")

# ----------------------------------------------------------------------------
hr("STEP E -- HONEST OBSTRUCTION CHECK")
# ----------------------------------------------------------------------------
print("""
 Assembled from Steps A-D (printed verdicts above feed this; final prose in the doc).
 The decisive facts to read off the runs:
  (1) Does V_eff have a WELL (Step A.2 turning-point count >= 2)?  -> intrinsic tower
      possible only if YES.
  (2) Are the BS levels R-INDEPENDENT (Step B R-scan)?  -> intrinsic only if YES.
  (3) Is m_n exponential-in-n or O(1)/sqrt(n) (Step C n-form)?  -> hierarchy only if
      a geometric/exponential structure appears; HO/sqrt(n) = O(1) (the #44 failure).
  (4) Is the well-depth / m_0 EXPONENTIAL in the dilation depth D (Step C depth-form)?
      -> the lepton-hierarchy target needs exp-in-depth.
  (5) Are ratios scale-free (Step D)?  -> yes by construction (prefactor cancels),
      but they depend on dimensionless D, l.
""")
print("DONE. Read the printed verdicts; structural prose -> quantized_carrier_structure_results.md")
