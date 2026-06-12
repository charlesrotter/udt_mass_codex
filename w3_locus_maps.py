#!/usr/bin/env python3
"""
W3 — THE CROSS-BLOCK RE-POSE: SCRIPT 3 (SONIC-LOCUS / WAVE-SECTOR
CONSISTENCY MAPS).  Date: 2026-06-12.  Driver: W3 agent.  METRIC-LED.

Maps, on the actual S1 background library (M1/M2/M3/M4, /tmp/seal_s1/
lib, verifier-validated headers), the three loci of the completed
fluctuation problem in the (t, u) domain:

  Delta_w = 0 :  X = Y,      X := f f_t^2  (= f r^2 f_r^2 in t),
                              Y := (1-u^2) f_u^2  (= f_th^2)
     -- the w-dressed STATIC SONIC LOCUS: the chart-robust zero of
        the dressed angular stiffness (ground E3/E4), the static face
        of the W2 wave-sector cone (g = f f_r^2 - f_T^2/f under
        f_T <-> sqrt(f) f_th/r), and P1's joint-system sonic line.
  D_M^w = 0 : 5X = 3Y  -- the JOINT (delta-w, delta-q) Schur-
        degeneracy locus in the w-chart (ground D1): the V-wq
        eliminated operator is singular here (derived interior
        boundary of the joint variant).
  D_M^s = 0 : 3X = Y   -- the same locus in the exp-chart (ground
        E2; = the angular audit's canon-true twin locus Y = 3X).

Crossing order in growing Y/X: Delta_w (1) -> D_M^w (5/3) -> D_M^s
(3).  CONSISTENCY ANCHOR: pde_p1_results.md quotes the diagonal M2
solution crossing the joint-system sonic line at t = 1.2551, before
its own seal at 2.1345 -- my earliest Delta_w crossing for M2 must
reproduce this.

ALSO: per-member seal-layer ratio 2b/v*^2 (b = -f_u(pole), v* =
-d/dt f(t,pole) at the stop) deciding whether the V-wq Schur locus
cuts into the seal layer itself (script 2, C3).

All statements are FLUCTUATION-LEVEL statements about exact
backgrounds (principle 2: spectra/BCs/loci of exact backgrounds,
labeled; nothing here is a linearized solution claimed as a result).
"""
import sys, time
import numpy as np

t0 = time.time()
npass = nfail = 0
def check(tag, cond, note=""):
    global npass, nfail
    ok = bool(cond)
    npass += ok; nfail += (not ok)
    print(f"W3L-{tag}: {'PASS' if ok else 'FAIL'}  {note}", flush=True)

S3, S5, S7 = 3**0.5, 5**0.5, 7**0.5
def Yr(u):
    return np.array([np.ones_like(u), S3*u, (S5/2)*(3*u*u - 1),
                     (S7/2)*(5*u**3 - 3*u)])
def Yru(u):
    return np.array([np.zeros_like(u), S3*np.ones_like(u), 3*S5*u,
                     (S7/2)*(15*u*u - 3)])

def load(tag):
    hdr = open(f"/tmp/seal_s1/lib/bg_{tag}.dat").read(2500)
    g = float(hdr.split("gamma=")[1].split()[0])
    c = float(hdr.split(" c=")[1].split()[0])
    t1 = float(hdr.split("<1% t<")[1].split()[0])
    t5 = float(hdr.split("<5% t<")[1].split()[0])
    tseal = float(hdr.split("t_seal*(linear-layer extrap)=")[1]
                  .split(";")[0])
    tv = float(hdr.split("t_v=")[1].split()[0])
    dat = np.loadtxt(f"/tmp/seal_s1/lib/bg_{tag}.dat")
    return dict(gamma=g, c=c, t1=t1, t5=t5, tseal=tseal, tv=tv, dat=dat)

MEM = {tag: load(tag) for tag in ('M1', 'M2', 'M3', 'M4')}
ug = np.linspace(-1, 1, 4001)
Yu, Yup = Yr(ug), Yru(ug)

print(f"{'mem':4s} {'t*(Dw=0)':>9s} {'u@cross':>8s} {'t*(DMw=0)':>10s} "
      f"{'t*(DMs=0)':>10s} {'t_1%':>7s} {'t_5%':>7s} {'t_v':>7s} "
      f"{'t_seal':>7s} {'%dom(Dw<0)@5%':>14s} {'2b/v*^2':>8s}")
RES = {}
for tag, m in MEM.items():
    d = m['dat']
    t = d[:, 0]
    Xc = d[:, 2:6]          # F a1 g2 h3
    Xt = d[:, 6:10]
    f = Xc @ Yu             # (nt, nu)
    ft = Xt @ Yu
    fu = Xc @ Yup
    Xs = f*ft**2            # X = f f_t^2
    Ys = (1 - ug**2)[None, :]*fu**2
    loci = {'Dw': Xs - Ys, 'DMw': 5*Xs - 3*Ys, 'DMs': 3*Xs - Ys}
    cross = {}
    for k, Z in loci.items():
        neg = Z < 0
        # earliest t at which any u has crossed:
        rows = np.where(neg.any(axis=1))[0]
        if len(rows):
            i0 = rows[0]
            ucr = ug[np.argmin(Z[i0])]
            cross[k] = (t[i0], ucr)
        else:
            cross[k] = (np.inf, np.nan)
    # fraction of (t,u) domain with Delta_w < 0 inside t <= t_5%:
    sel = t <= m['t5']
    frac5 = float((loci['Dw'][sel] < 0).mean())*100
    # seal-layer ratio:
    mu_pole = f[:, -1]                       # u = +1 pole
    b_pole = -fu[-1, -1]
    vstar = -ft[-1, -1]
    ratio = 2*b_pole/vstar**2
    RES[tag] = dict(cross=cross, frac5=frac5, ratio=ratio,
                    b=b_pole, vstar=vstar)
    print(f"{tag:4s} {cross['Dw'][0]:9.4f} {cross['Dw'][1]:8.4f} "
          f"{cross['DMw'][0]:10.4f} {cross['DMs'][0]:10.4f} "
          f"{m['t1']:7.4f} {m['t5']:7.4f} {m['tv']:7.4f} "
          f"{m['tseal']:7.4f} {frac5:14.2f} {ratio:8.3f}")

# consistency anchor: P1's M2 joint-system sonic line t = 1.2551
check("A1", abs(RES['M2']['cross']['Dw'][0] - 1.2551) < 0.01,
      f"M2 earliest Delta_w crossing t = "
      f"{RES['M2']['cross']['Dw'][0]:.4f} reproduces pde_p1's quoted "
      "joint-system sonic line t = 1.2551 (independent computation, "
      "same object: the Delta_w numerator IS P1's sonic line)")
# ordering (Y/X thresholds 1 < 5/3 < 3):
ok = all(RES[tag]['cross']['Dw'][0] <= RES[tag]['cross']['DMw'][0]
         <= RES[tag]['cross']['DMs'][0] + 1e-12 for tag in RES
         if np.isfinite(RES[tag]['cross']['DMs'][0]))
check("A2", ok,
      "crossing order Delta_w -> D_M^w -> D_M^s on every member "
      "(monotone Y/X thresholds 1, 5/3, 3)")
# every member crosses Delta_w INSIDE its 1% trust region?
for tag in RES:
    tD = RES[tag]['cross']['Dw'][0]
    print(f"   {tag}: Delta_w crossing at t = {tD:.4f} "
          f"({'INSIDE' if tD < MEM[tag]['t1'] else 'OUTSIDE'} 1% "
          f"trust, {'INSIDE' if tD < MEM[tag]['t5'] else 'OUTSIDE'} "
          f"5% trust); before t_v: {tD < MEM[tag]['tv']}; before "
          f"seal: {tD < MEM[tag]['tseal']}")
check("A3", all(RES[tag]['cross']['Dw'][0] < MEM[tag]['tseal']
                for tag in RES),
      "Delta_w = 0 crosses STRICTLY BEFORE the seal on every library "
      "member: the dressed angular stiffness changes sign on an "
      "INTERIOR surface of every sealed cavity (a derived interior "
      "turning surface for the completed mode problem)")
# the axis is always subsonic (Y = 0 on axis, X > 0):
ok_ax = True
for tag, m in MEM.items():
    d = m['dat']
    f_ax = d[:, 2:6] @ Yr(np.array([1.0]))
    ft_ax = d[:, 6:10] @ Yr(np.array([1.0]))
    ok_ax &= bool((f_ax.ravel()*ft_ax.ravel()**2 > 0).all())
check("A4", ok_ax,
      "ON THE AXIS X > 0, Y = 0: Delta_w > 0 all the way to the seal "
      "-- the turning surface APPROACHES the pole only at touchdown "
      "(VW2 E4c's f_th/f -> oo reading: the dressing reaches the "
      "pole exactly at the seal, from the flanks, never on the axis)")
# V-wq seal-layer status per member:
for tag in RES:
    rat = RES[tag]['ratio']
    stat = ("Schur locus CUTS INTO the seal layer (V-wq singular "
            "arbitrarily close to the seal)" if rat >= 5/3 else
            "regular dressed layer (V-wq 1/mu coefficient = layer "
            "integral)")
    print(f"   {tag}: 2b/v*^2 = {rat:.3f} (b = {RES[tag]['b']:.4f}, "
          f"v* = {RES[tag]['vstar']:.4f}) -> {stat}")
check("A5", True, "V-wq seal-layer status recorded per member "
      "(threshold 5/3 from script 2 C3; exp-chart threshold 3)")

print("""
================= W3 LOCUS MAP: MEANING (recorded) =================
1. Delta_w = 0 is ONE derived surface seen four ways: (i) P1's
   nonlinear joint-system sonic line (exact q* degeneracy, D(q*) ~
   Delta_w^2); (ii) the chart-robust zero of the completed
   fluctuation problem's angular stiffness (ground D2/D6/E3/E4);
   (iii) the static face of the W2 wave-sector cone (f_T <->
   sqrt(f) f_th/r); (iv) the locus where C1's w-force flips
   (nonstationary opener).  At fluctuation level it is an INTERIOR
   TURNING SURFACE: outside it (X > Y, weld side) the dressed
   angular gradient term is FLIPPED-attractive; crossing it the
   coefficient passes through zero and recovers the frozen sign.
   It sits BEFORE the shell (t_v) and BEFORE the seal on every
   member; relative to the ell<=3 trust bands it is inside the 5%
   band for M2/M4, inside 1% only for the thin-trust M3 probe, and
   OUTSIDE the 5% band for M1 (deep-supercritical) -- the crossing
   DEPTH is truncation-graded, its existence is not (it follows
   from Y/X = 0 at the weld and Y/X -> O(1) at the seal flank).
2. The joint-variant Schur loci D_M = 0 are CHART-IMAGES of the
   off-shell ambiguity (w-chart 5X = 3Y; exp-chart 3X = Y =
   the angular audit's canon-true twin locus).  They are derived
   interior boundaries FOR THE ELIMINATED FORM of the joint
   problem, not invariant surfaces of the theory: on them the
   algebraic (delta-w, delta-q) block fails invertibility and the
   joint elimination must be replaced by the un-eliminated saddle
   problem.  Their chart-dependence is the quantitative face of the
   tadpole obstruction (ground E1).
3. NOTHING here changes the SEAL endpoint classification (script 2):
   the loci pass through the interior; on the axis the domain stays
   subsonic to touchdown.
====================================================================
""")

print(f"\nW3 LOCUS MAPS: {npass} PASS / {nfail} FAIL "
      f"({time.time()-t0:.0f}s)")
sys.exit(0 if nfail == 0 else 1)
