"""
depth_selector_verif_confine.py
================================
BLIND ADVERSARIAL VERIFIER — ATTACK 1 & 2: confinement + smuggling.

I do NOT trust the constructor. I re-derive U(D) from the two stated native pieces
and HUNT HARD for an interior minimum (a confining well) below the tachyon cap D*,
sweeping the FULL derived parameter ranges:
    k in [3.5, 4.9], D* in [2.4, 3.4], floor=l(l+1) for l in {1,2,3} -> {2,6,12},
    c_grav (the gravitational prefactor, "CHOSE, cancels in ratios"), A0^2 (any positive).

Native form (from docs):
    E_grav(D)  = c_grav*(e^{2D}-1)            (B1 MS dilation cost; EXPONENTIAL)
    omega2(D)  = floor - c_bind*D^k           (native carrier freq; c_bind from omega2(D*)=0)
    U(D)       = E_grav(D) + (1/2)*A0sq*max(omega2(D),0)   [PHYSICAL: tachyon cap enforced]
    U_naive(D) = E_grav(D) + (1/2)*A0sq*omega2(D)          [lets omega2<0: the FAKE-well audit]

KEY ADVERSARIAL QUESTIONS:
 (Q1) Is the tachyon cap max(.,0) the thing killing the well? -> if I REMOVE it
      (U_naive), does a real *smooth* interior min appear BELOW D* (i.e. omega2 still >0)?
      A well that needs omega2<0 to exist is FAKE. A well at omega2>0 would be REAL.
 (Q2) Can c_grav be pushed small enough that the bounded carrier drop out-pulls the
      exponential rise INSIDE (0,D*) -> a real interior min? (c_grav is "CHOSE".)
 (Q3) Left wall as D->0: does U rise as D->0 (a left barrier) or is it flat/open?
"""
import numpy as np

def omega2(D, floor, c_bind, k):
    return floor - c_bind*np.asarray(D,float)**k

def make(c_grav, A0sq, floor, Dstar, k):
    c_bind = floor/Dstar**k          # omega2(D*)=0  -> c_bind = floor/D*^k
    Eg  = lambda D: c_grav*(np.exp(2*np.asarray(D,float))-1.0)
    w2  = lambda D: omega2(D, floor, c_bind, k)
    Uph = lambda D: Eg(D) + 0.5*A0sq*np.maximum(w2(D),0.0)
    Una = lambda D: Eg(D) + 0.5*A0sq*w2(D)
    return Eg, w2, Uph, Una, c_bind

def interior_min_info(U, Dstar, n=200000):
    """Find interior local minima on (eps, D*). Return list of (D_min, depth-below-right)."""
    D = np.linspace(1e-4, Dstar*(1-1e-6), n)
    Uv = U(D)
    # strict interior local minima
    idx = 1 + np.where((Uv[1:-1] < Uv[:-2]) & (Uv[1:-1] < Uv[2:]))[0]
    mins = [(D[i], Uv[i]) for i in idx]
    return mins, D, Uv

print("="*78)
print("VERIFIER ATTACK 1/2 — hunt for a confining interior minimum below D*")
print("="*78)

# ---- (Q2) BRUTE SWEEP for an interior minimum in the PHYSICAL U (cap enforced) ----
print("\n[Q2] PHYSICAL U (tachyon cap on): sweep full derived ranges for ANY interior min")
ks      = [3.5, 4.0, 4.5, 4.9]
Dstars  = [2.4, 2.6, 3.0, 3.4]
floors  = [2.0, 6.0, 12.0]            # l=1,2,3
cgravs  = [1e-6, 1e-3, 1e-2, 0.1, 1.0, 10.0, 100.0]   # push SMALL to favor a well
A0sqs   = [0.1, 1.0, 10.0, 100.0, 1e3, 1e4, 1e6]      # push BIG to favor a well
found_phys = 0
worst_case = None  # smallest dU/dD min (closest to a well)
import itertools
min_slope_global = np.inf
for k,Ds,fl,cg,A in itertools.product(ks,Dstars,floors,cgravs,A0sqs):
    Eg,w2,Uph,Una,cb = make(cg,A,fl,Ds,k)
    mins,D,Uv = interior_min_info(Uph, Ds, n=40000)
    # also track the minimum slope (most-negative dU/dD) to see how close to a turn
    dU = np.gradient(Uv,D)
    ms = dU.min()
    if ms < min_slope_global:
        min_slope_global = ms
        worst_case = (k,Ds,fl,cg,A,ms,len(mins))
    if mins:
        found_phys += 1
        if found_phys <= 5:
            print(f"   WELL? k={k} D*={Ds} floor={fl} c_grav={cg:.0e} A0^2={A:.0e}: "
                  f"interior mins at D={[round(m[0],3) for m in mins]}")
print(f"   PHYSICAL-U interior minima found across {len(ks)*len(Dstars)*len(floors)*len(cgravs)*len(A0sqs)} combos: {found_phys}")
print(f"   closest-to-a-well (most negative dU/dD on (0,D*)): "
      f"k={worst_case[0]} D*={worst_case[1]} floor={worst_case[2]} c_grav={worst_case[3]:.0e} "
      f"A0^2={worst_case[4]:.0e}  min(dU/dD)={worst_case[5]:.4g}  (>=0 => monotone rising)")

# ---- (Q1) SMUGGLING / FAKE-WELL audit: does removing the cap create a well, and is it FAKE? ----
print("\n[Q1] FAKE-WELL audit: U_naive (cap OFF). If a min appears, is it at omega2>0 (REAL)")
print("     or only because omega2 went NEGATIVE (FAKE)?")
for cg,A,fl,Ds,k in [(1.0,5.0,2.0,2.6,4.0),(1e-3,1e4,2.0,2.6,4.0),(0.1,100.0,12.0,3.4,3.5)]:
    Eg,w2,Uph,Una,cb = make(cg,A,fl,Ds,k)
    mins,D,Uv = interior_min_info(Una, Ds, n=200000)
    if mins:
        for Dm,Um in mins:
            w2m = w2(Dm)
            tag = "REAL (omega2>0)" if w2m>0 else "FAKE (omega2<0 -> tachyon, not binding)"
            print(f"   c_grav={cg:.0e} A0^2={A:.0e} floor={fl} D*={Ds} k={k}: "
                  f"naive min at D={Dm:.3f}, omega2={w2m:.3f} -> {tag}")
    else:
        print(f"   c_grav={cg:.0e} A0^2={A:.0e} floor={fl} D*={Ds} k={k}: no interior min even WITHOUT cap")

# ---- (Q1b) THE DEEPER QUESTION: could a SMOOTH well exist WITHOUT going tachyonic? ----
# A genuine confining well below D* needs dU/dD = 0 at some D_w < D* with omega2(D_w) > 0.
# dU/dD = 2 c_grav e^{2D} - (1/2) A0^2 c_bind k D^{k-1}.  Set =0:
#   2 c_grav e^{2D} = (1/2) A0^2 c_bind k D^{k-1}
# The LHS rises like e^{2D} (>= 2 c_grav at D=0, and 2 c_grav*e^{2D}). The RHS is bounded by
# its value over [0,D*]. For an interior STATIONARY point you need the falling carrier slope to
# EXCEED the rising grav slope somewhere -> U decreasing -> then a min. Test the slope crossing.
print("\n[Q1b] Can the carrier's downward slope EXCEED gravity's upward slope below D* (=> dip)?")
print("     (this is the ONLY way a real interior min can form with the cap on)")
for cg,A,fl,Ds,k in [(1e-3,1e6,2.0,2.6,4.0),(1e-6,1e6,2.0,2.4,4.9),(1.0,5.0,2.0,2.6,4.0),(1e-2,1e4,12.0,3.4,3.5)]:
    Eg,w2,Uph,Una,cb = make(cg,A,fl,Ds,k)
    D = np.linspace(1e-4, Ds*(1-1e-6), 400000)
    grav_slope = 2*cg*np.exp(2*D)
    # carrier slope only where omega2>0 (physical); d/dD[ (1/2)A0^2 omega2 ] = -(1/2)A0^2 c_bind k D^{k-1}
    carr_down = 0.5*A*cb*k*D**(k-1)   # magnitude of downward pull
    phys = w2(D) > 0
    # net downward region: carrier downward pull > gravity upward push AND omega2>0
    dip = phys & (carr_down > grav_slope)
    if dip.any():
        Dd = D[dip]
        print(f"   c_grav={cg:.0e} A0^2={A:.0e} floor={fl} D*={Ds} k={k}: "
              f"DIP region exists at D in [{Dd.min():.3f},{Dd.max():.3f}] (omega2>0) -> a REAL well COULD form")
    else:
        print(f"   c_grav={cg:.0e} A0^2={A:.0e} floor={fl} D*={Ds} k={k}: "
              f"NO physical (omega2>0) region where carrier out-pulls gravity -> monotone rising")

# ---- (Q3) LEFT WALL as D->0 ----
print("\n[Q3] Left wall as D->0: is U(D) increasing or decreasing toward D=0?")
for cg,A,fl,Ds,k in [(1.0,5.0,2.0,2.6,4.0)]:
    Eg,w2,Uph,Una,cb = make(cg,A,fl,Ds,k)
    Dsmall = np.array([1e-4,1e-3,1e-2,0.05,0.1,0.2,0.5])
    print("   D     :", np.array2string(Dsmall,precision=4))
    print("   U_phys:", np.array2string(Uph(Dsmall),precision=5))
    print("   dU/dD at D->0 = 2c_grav + 0 (carrier slope ~ D^{k-1}->0). =",2*cg,
          "  => U RISES from D=0 (no 1/D^2 barrier, but also no leftward pull): a flat-ish RISING left edge")
print("\n   The l(l+1) carrier term's D-slope ~ D^{k-1} -> 0 as D->0, so NO 1/D^2 left wall;")
print("   gravity slope -> 2c_grav>0, so U is RISING (gently) from D=0. Half-well, open-ish left, confirmed.")
