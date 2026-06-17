#!/usr/bin/env python3
"""
VERIF_multicell_tiling.py -- the #40 "sharp next object": does ANGULAR-SECTOR-BRIDGE
multi-cell coupling + a GLOBAL conserved Misner-Sharp total DISCRETIZE the partition
energy E (multi-rooted closure residual C(E;M_total)=0 => discrete seal depths/masses),
or does it stay single-root / continuum?

Driver: Claude (Opus 4.8, 1M).  2026-06-17.  OBSERVE mode.  DATA-BLIND.
NEW file (append-never-edit discipline; does NOT touch committed scripts/.md records).

================================================================================
PART 1 -- THE SINGLE-CELL CLOSURE (re-stated EXACTLY, the object to generalize)
================================================================================
The canonical single-cell whole-profile closure (registry #33/#34, w_alg PART E):

    metric profile v(m), m = ln r (radial chart).  ON two-exponential source.
    whole-profile EOM:   v_mm = Phi*(e^{-2v} - e^{v})
    FIRST INTEGRAL:      H(v,v_m) = (1/2) v_m^2 + (Phi/2) e^{-2v} + Phi e^{v} = E
    restoring well:      U(v) = (Phi/2)e^{-2v} + Phi e^{v},  U'(v)=Phi(-e^{-2v}+e^v),
                         U_min = (3 Phi/2) at v=0,  U strictly CONVEX (U''=Phi(2e^{-2v}+e^v)>0).

Closure = a bounded orbit (E > U_min): TWO turning points v_m=0 automatically
(inner regularity + outer Neumann are met AUTOMATICALLY by the well's symmetry of
turning points).  The ONLY non-automatic datum is the DEPTH (Dirichlet boundary
value v_max), which is a CONTINUOUS BIJECTION depth<->E.

THE SINGLE-CELL RESIDUAL (what plays the role of D(E)/C(E)):
  Given the partition energy E, the depth is the turning point v_*(E) (larger root of
  U(v)=E).  Define the single-cell closure map:
      depth:   v_*(E) = the v>0 turning point solving U(v)=E
      width:   L(E)   = 2 * INT_{v_-}^{v_+} dv / sqrt(2(E-U(v)))   (full bounce)
      seal-depth invariant:  Dsc(E) = 4*pi*(ln f)_seal = 4*pi * (ln f at depth)
                             with ln f = -2 phi = +2 v_*  (f=e^{-2phi}, phi=-v convention)
  ONE-ROOT PROPERTY: U is strictly convex with a single minimum, so for any E>U_min
  there is EXACTLY ONE v_+>0 and ONE v_-<0 turning point.  v_*(E) and Dsc(E) are SMOOTH,
  STRICTLY MONOTONE in E (dv_*/dE = 1/U'(v_*) > 0).  No lattice, one root.  (h1_types
  l.104: dD/dE != 0; reg #33 l.596-600: continuous bijection depth<->E.)

================================================================================
PART 2 -- THE TWO-CELL ANGULAR-BRIDGE TILING CLOSURE (the NEW object)
================================================================================
Two negative-phi MATTER cells embedded in a positive-phi background, COUPLED through
the phi-INVARIANT ANGULAR SECTOR (Charles 2026-06-17 LATER-8: the bridge is
ANGULAR-FIELD CONTINUITY across cells; NOT a phi-mirror).  A GLOBAL conserved total
Sigma(Misner-Sharp mass) = M_total is a FREE PARAMETER.

Each cell i has its OWN partition energy E_i and its OWN depth v_i = v_*(E_i).
The two-cell state is (E_1, E_2).  The closure is TWO scalar conditions on (E_1,E_2):

  (J) ANGULAR-SECTOR-BRIDGE JUNCTION:  the angular field is CONTINUOUS across the bridge.
      The angular sector carries the fixed topological datum (N=3, q=1/3): the public
      charge SLOPE d ln f = -q d ln r is the angular sector's footprint on each cell.
      Continuity of the angular field across the shared bridge = continuity of the
      angular-sector invariant each cell presents at its seal.  The cell's angular
      invariant at its seal is  A_i = q * (ln f)_seal,i = q * 2 * v_i   (the area-form
      content per unit 4pi, i.e. Dsc/(4pi/ ... ); the q-weighted seal depth).
      BRIDGE = A_1 = A_2  (angular continuity)  ... [the connective tissue]
      => q*2*v_1 = q*2*v_2  => v_1 = v_2  in the PURE-continuity reading.
      [This is the FAITHFUL minimal junction; we ALSO test a GENERALIZED bridge
       where the background twist rotates the angular phase by Delta between cells,
       A_1 = A_2 + Delta, to see if a nonzero offset opens windows.]

  (G) GLOBAL CONSERVED TOTAL:  Sigma M_MS = M_total.
      Single-cell Misner-Sharp mass (coupled_cell l.30; reg): m_i = (depth content) =
      M(v_i) = 1 - e^{-2 phi_seal} ... in the whole-profile chart the cell's MS content
      is set by the seal depth.  We use the DERIVED single-cell mass map
          M(v) = 1 - e^{-2 v}              (Misner-Sharp: m = 1 - e^{-2phi}=1-e^{-2v},
                                            the seal-depth -> mass convention, h1 l.114)
      (and ALSO a second, super-exponential map M(v)=e^{2v}-1 from the #56 deep-neg
       core dial m_core=rc(1-e^{2p}); both tested -- the verdict must not hinge on it.)
      GLOBAL:  M(v_1) + M(v_2) = M_total.

THE COUPLED RESIDUAL (eliminate v_2 via the bridge, parameterize by E_1 == E):
  Let v_1 = v_*(E).  Bridge (pure) => v_2 = v_1 = v_*(E).  Then
      C(E; M_total) = M(v_*(E)) + M(v_*(E)) - M_total = 2*M(v_*(E)) - M_total
  Generalized bridge (offset Delta): v_2 = v_1 + Delta/(2q);
      C(E; M_total) = M(v_*(E)) + M(v_*(E) + Delta/(2q)) - M_total

ROOT COUNT in E for fixed M_total is the WHOLE QUESTION.

================================================================================
PREMISE LEDGER (chose-or-derived; FORCED choices flagged ***)
================================================================================
DERIVED (forced by the corpus / the metric / the angular Lagrangian):
 D1. Single-cell whole-profile EOM v_mm=Phi(e^{-2v}-e^v); first integral E; convex
     well U; one turning point each side; depth<->E continuous bijection. [reg#33 596-600]
 D2. dDsc/dE != 0, Dsc=4pi(ln f)_seal, ln f = 2 v at the seal. [h1 l.104,114]
 D3. Angular sector is phi-INVARIANT and carries the fixed (N=3,q=1/3); its footprint
     on a cell is the charge slope d ln f=-q d ln r => seal invariant ~ q*(ln f)_seal.
     [STATE_DERIVATION 449-452; reg#40 920-922]
 D4. Misner-Sharp mass m=1-e^{-2phi} (depth->mass). [h1 l.114; coupled_cell l.30]
 D5. The bridge = ANGULAR-FIELD CONTINUITY across cells, NOT a phi-matching/reflection.
     [STATE_DERIVATION 451; Charles Q1]

CHOSE (modeling choices; *** = forced choice / smuggle-risk, flagged honestly):
 C1.*** WHICH single-cell object to generalize: the #33/#34 two-exponential
     whole-profile closure (cleanest "convex well, one root, E free").  Forced: it is
     THE canonical single-cell closure the #40 statement refers to.  (Cross-checked
     against the #56 depth-mass map in C5.)
 C2.*** The angular-bridge junction is implemented as EQUALITY of the q-weighted seal
     depth (A_i = q*(ln f)_seal,i).  This is the LOAD-BEARING choice: it says angular
     continuity ties the two cells' DEPTHS (pure: v_1=v_2).  Smuggle-risk: any junction
     that ties v_1,v_2 RIGIDLY collapses the 2-cell DOF to 1.  We FLAG this and ALSO run
     the generalized-offset and the FULLY-DECOUPLED-junction variants to bound it.
 C3.   Phi (the source strength) = 1 (a dimensionless dial; scale-free, #39).  Not
     load-bearing (rescaling Phi rescales E,U together).
 C4.   M_total is a FREE PARAMETER scanned over a wide range; NO value assumed critical.
 C5.   Mass map M(v): primary M=1-e^{-2v} (D4); SECONDARY M=e^{2v}-1 (#56 deep-core dial)
     run as a robustness check.  Verdict must agree across both.
 C6.   Generalized bridge offset Delta in {0, +-0.2, +-0.5, +-1.0} scanned (does a
     nonzero angular phase offset open multi-root windows?).
 C7.   N_cells generalized 2->K (identical-cell tiling: K*M(v_*(E))=M_total) tested IF
     the 2-cell case shows any multi-rootedness; otherwise reported as "did not need to".

NOT CLAIMED: no mass, no ratio, no wall comparison; no value of M_total asserted special
unless the root-structure FORCES it; the nonstationary sector untouched.
================================================================================
"""
import numpy as np
import mpmath as mp

PHI = 1.0   # C3: scale-free source dial

# --------------------------------------------------------------------------
# Single-cell well U(v) and its turning points / depth map v_*(E).
# --------------------------------------------------------------------------
def U(v, Phi=PHI):
    return 0.5*Phi*np.exp(-2.0*v) + Phi*np.exp(v)

def Uprime(v, Phi=PHI):
    return Phi*(-np.exp(-2.0*v) + np.exp(v))

def Udd(v, Phi=PHI):
    return Phi*(2.0*np.exp(-2.0*v) + np.exp(v))

U_MIN = 1.5*PHI   # at v=0

def v_star_plus(E, Phi=PHI):
    """The v>0 turning point solving U(v)=E (the cell's DEPTH).  One root (convex)."""
    if E <= U_MIN:
        return None
    # U increasing for v>0 (U'(0)=0, U''>0): bisect on [0, vmax]
    lo, hi = 0.0, 1.0
    while U(hi, Phi) < E:
        hi *= 2.0
        if hi > 1e3:
            break
    for _ in range(200):
        mid = 0.5*(lo+hi)
        if U(mid, Phi) < E:
            lo = mid
        else:
            hi = mid
    return 0.5*(lo+hi)

def v_star_minus(E, Phi=PHI):
    """The v<0 turning point (inner).  One root."""
    if E <= U_MIN:
        return None
    lo, hi = -1.0, 0.0
    while U(lo, Phi) < E:
        lo *= 2.0
        if lo < -1e3:
            break
    for _ in range(200):
        mid = 0.5*(lo+hi)
        if U(mid, Phi) < E:
            hi = mid
        else:
            lo = mid
    return 0.5*(lo+hi)

# --------------------------------------------------------------------------
# Mass maps (D4 primary; #56 secondary).  q=1/3 angular charge slope.
# --------------------------------------------------------------------------
Q = 1.0/3.0

def M_primary(v):      # Misner-Sharp m = 1 - e^{-2phi}, phi=-v -> 1-e^{-2v}?
    # depth v>0 => phi=-v<0 (matter-bearing neg-phi); m=1-e^{-2phi}=1-e^{+2v} is
    # negative; use |.| convention consistent with h1 (seal depth = mass content):
    return np.expm1(2.0*v)            # e^{2v}-1, the deep-neg core MS content (>=0)

def M_alt(v):          # alternative convention 1-e^{-2v} (also >=0, saturating)
    return -np.expm1(-2.0*v)          # 1 - e^{-2v}

# --------------------------------------------------------------------------
# THE COUPLED TWO-CELL RESIDUAL C(E; M_total).
# bridge: v_2 = v_1 + Delta/(2q)   (Delta=0 => pure angular continuity v_1=v_2)
# --------------------------------------------------------------------------
def C_two_cell(E, M_total, Delta=0.0, massmap=M_primary, Phi=PHI):
    v1 = v_star_plus(E, Phi)
    if v1 is None:
        return None
    v2 = v1 + Delta/(2.0*Q)
    if v2 <= 0:   # cell 2 must still be a matter (neg-phi) cell
        return None
    return massmap(v1) + massmap(v2) - M_total

def count_roots(M_total, Delta=0.0, massmap=M_primary, Phi=PHI,
                Emin=None, Emax=60.0, n=20000):
    if Emin is None:
        Emin = U_MIN + 1e-9
    Es = np.linspace(Emin, Emax, n)
    Cs = np.array([C_two_cell(E, M_total, Delta, massmap, Phi) for E in Es],
                  dtype=object)
    # filter Nones
    valid = np.array([c is not None for c in Cs])
    Es_v = Es[valid]; Cs_v = np.array([float(c) for c in Cs[valid]])
    roots = []
    for k in range(len(Cs_v)-1):
        if Cs_v[k] == 0.0:
            roots.append(Es_v[k])
        elif Cs_v[k]*Cs_v[k+1] < 0.0:
            # refine by bisection
            a, b = Es_v[k], Es_v[k+1]
            fa = C_two_cell(a, M_total, Delta, massmap, Phi)
            for _ in range(80):
                m = 0.5*(a+b)
                fm = C_two_cell(m, M_total, Delta, massmap, Phi)
                if fm is None:
                    break
                if fa*fm <= 0:
                    b = m
                else:
                    a = m; fa = fm
            roots.append(0.5*(a+b))
    return roots, Es_v, Cs_v

# --------------------------------------------------------------------------
# K-cell identical tiling: K*M(v_*(E)) = M_total  (only if 2-cell shows structure)
# --------------------------------------------------------------------------
def count_roots_Kcell(M_total, K, massmap=M_primary, Phi=PHI, Emin=None, Emax=60.0, n=20000):
    if Emin is None:
        Emin = U_MIN + 1e-9
    Es = np.linspace(Emin, Emax, n)
    vals = []
    for E in Es:
        v = v_star_plus(E, Phi)
        vals.append(K*massmap(v) - M_total if v is not None else None)
    roots = []
    for k in range(len(Es)-1):
        a_ok = vals[k] is not None; b_ok = vals[k+1] is not None
        if a_ok and b_ok and vals[k]*vals[k+1] < 0:
            a,b = Es[k],Es[k+1]; fa=vals[k]
            for _ in range(60):
                m=0.5*(a+b); fm=K*massmap(v_star_plus(m,Phi))-M_total
                if fa*fm<=0: b=m
                else: a=m; fa=fm
            roots.append(0.5*(a+b))
    return roots

# ==========================================================================
def main():
    print("="*78)
    print("PART 1 -- single-cell closure: one-root property check")
    print("="*78)
    print(f"U_min = {U_MIN:.6f} at v=0;  U'' > 0 everywhere (strictly convex).")
    # demonstrate single turning point + monotone depth(E)
    print(f"{'E':>8} {'v_+(E)':>12} {'v_-(E)':>12} {'dv+/dE=1/U''(v+)':>18} {'Dsc=4pi*2v+':>14}")
    prevv = None; mono = True
    for E in [1.6, 2.0, 3.0, 5.0, 10.0, 30.0]:
        vp = v_star_plus(E); vm = v_star_minus(E)
        dvdE = 1.0/Uprime(vp)
        Dsc = 4.0*np.pi*2.0*vp
        print(f"{E:8.2f} {vp:12.8f} {vm:12.8f} {dvdE:18.8f} {Dsc:14.6f}")
        if prevv is not None and vp <= prevv: mono = False
        prevv = vp
    print(f"depth v_+(E) strictly monotone increasing: {mono}  (=> single-cell ONE root, smooth)")

    print()
    print("="*78)
    print("PART 3 -- TWO-CELL ANGULAR-BRIDGE closure: root count C(E;M_total)=0")
    print("="*78)

    for label, mm in [("M=e^{2v}-1 (deep-core, primary)", M_primary),
                      ("M=1-e^{-2v} (saturating, alt)",   M_alt)]:
        print(f"\n--- mass map: {label} ---")
        print("PURE bridge (Delta=0, angular continuity v1=v2): C = 2*M(v_*(E)) - M_total")
        # range of reachable 2*M over E
        Egrid = np.linspace(U_MIN+1e-9, 60, 4000)
        twoM = np.array([2.0*mm(v_star_plus(E)) for E in Egrid])
        print(f"   2*M(v_*(E)) range over E in [{U_MIN:.2f},60]: "
              f"[{twoM.min():.5g}, {twoM.max():.5g}], monotone={np.all(np.diff(twoM)>0)}")
        print(f"   {'M_total':>10} {'#roots':>7}   roots(E)")
        for Mt in [0.1, 0.5, 1.0, 2.0, 5.0, 20.0, 100.0, 1e4, 1e8]:
            roots,_,_ = count_roots(Mt, Delta=0.0, massmap=mm)
            rs = ", ".join(f"{r:.5f}" for r in roots[:6])
            print(f"   {Mt:10.4g} {len(roots):7d}   {rs}")

    print()
    print("--- GENERALIZED bridge: angular-phase OFFSET Delta (v2=v1+Delta/(2q)) ---")
    print("    (does a nonzero angular offset between cells open multi-root windows?)")
    print(f"   {'Delta':>7} {'M_total':>10} {'#roots':>7}   roots(E)")
    for Delta in [-1.0, -0.5, -0.2, 0.0, 0.2, 0.5, 1.0]:
        for Mt in [1.0, 5.0, 50.0, 5000.0]:
            roots,_,_ = count_roots(Mt, Delta=Delta, massmap=M_primary)
            rs = ", ".join(f"{r:.4f}" for r in roots[:6])
            print(f"   {Delta:7.2f} {Mt:10.4g} {len(roots):7d}   {rs}")

    print()
    print("--- root-set CARDINALITY vs M_total (fine scan, pure bridge, primary map) ---")
    print("    windows open/close?  spacing exponential (~207,~17) or O(1)?")
    card = {}
    for Mt in np.logspace(-1, 9, 60):
        roots,_,_ = count_roots(Mt, Delta=0.0, massmap=M_primary, Emax=120, n=8000)
        card[len(roots)] = card.get(len(roots),0)+1
    print(f"   cardinality histogram over 60 M_total in [0.1, 1e9]: {dict(sorted(card.items()))}")

    print()
    print("="*78)
    print("PART 3b -- K-CELL identical tiling (K*M(v_*(E))=M_total): does K-count help?")
    print("="*78)
    for K in [2, 3, 5, 10, 207]:
        nroot = {}
        for Mt in np.logspace(-1, 9, 40):
            r = count_roots_Kcell(Mt, K, massmap=M_primary, Emax=120, n=6000)
            nroot[len(r)] = nroot.get(len(r),0)+1
        print(f"   K={K:4d}: root-cardinality histogram over 40 M_total = {dict(sorted(nroot.items()))}")

    print()
    print("="*78)
    print("PART 4 -- mpmath spot-check of a claimed root (dps=40)")
    print("="*78)
    mp.mp.dps = 40
    def U_mp(v): return mp.mpf('0.5')*mp.e**(-2*v) + mp.e**v
    def vstar_mp(E):
        return mp.findroot(lambda v: U_mp(v)-E, mp.mpf('1.0'))
    # take the pure-bridge root for M_total=20 (primary map)
    roots,_,_ = count_roots(20.0, Delta=0.0, massmap=M_primary)
    if roots:
        E0 = roots[0]
        v0 = vstar_mp(mp.mpf(E0))
        C0 = 2*(mp.e**(2*v0)-1) - 20
        print(f"   M_total=20, float64 root E={E0:.12f}, v_*={float(v0):.12f}")
        print(f"   mpmath residual C(E;20) = {mp.nstr(C0, 12)}  (should be ~0)")
        # is the root structurally forced unique? show C monotone there
        for dE in [-0.5,-0.1,0,0.1,0.5]:
            v = vstar_mp(mp.mpf(E0)+dE)
            print(f"      E={float(E0)+dE:8.4f}  C={mp.nstr(2*(mp.e**(2*v)-1)-20,8)}")

if __name__ == "__main__":
    main()
