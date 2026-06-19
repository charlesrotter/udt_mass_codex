"""
depth_selector_verif_well.py
============================
FOLLOW-UP: characterize the interior minima my sweep found in the PHYSICAL U
(cap enforced). Are they REAL confining wells (omega2>0 at the min, finite barrier
on BOTH sides) or artifacts? When exactly do they appear vs the constructor's claim?

The constructor used (c_grav=1, A0^2 in {1,5,20,100}, floor=2, D*=2.6, k=4) and got
monotone-rising. My sweep over the FULL derived ranges found wells. Resolve the
discrepancy: it is the RATIO A0^2/c_grav (carrier weight vs gravity) that matters.
The constructor FIXED c_grav=1 and only scanned A0^2 up to 100 -> never entered the
well regime. The well regime is legitimate (c_grav is tagged "CHOSE, cancels in ratios").
"""
import numpy as np

def make(c_grav, A0sq, floor, Dstar, k):
    c_bind = floor/Dstar**k
    Eg  = lambda D: c_grav*(np.exp(2*np.asarray(D,float))-1.0)
    w2  = lambda D: floor - c_bind*np.asarray(D,float)**k
    Uph = lambda D: Eg(D) + 0.5*A0sq*np.maximum(w2(D),0.0)
    return Eg,w2,Uph,c_bind

def well_report(c_grav,A0sq,floor,Dstar,k,n=400000):
    Eg,w2,Uph,cb = make(c_grav,A0sq,floor,Dstar,k)
    D = np.linspace(1e-5, Dstar*(1-1e-7), n)
    Uv = Uph(D)
    idx = 1 + np.where((Uv[1:-1] < Uv[:-2]) & (Uv[1:-1] < Uv[2:]))[0]
    out=[]
    for i in idx:
        Dm=D[i]; Um=Uv[i]; w2m=w2(Dm)
        # barrier on each side within (0,D*)
        leftmax = Uv[:i].max() if i>0 else Um
        rightmax= Uv[i:].max()
        out.append(dict(Dm=Dm,Um=Um,w2m=w2m,
                        left_barrier=leftmax-Um, right_barrier=rightmax-Um,
                        U0=Uv[0], UDstar=Uv[-1]))
    return out

print("="*78)
print("Characterize the interior minima (PHYSICAL U, cap on)")
print("="*78)

# The constructor's exact grid vs an extended A0^2/c_grav ratio scan
print("\nConstructor's grid (c_grav=1, floor=2, D*=2.6, k=4):  -- reproduce 'monotone'?")
for A in [1,5,20,100]:
    r=well_report(1.0,A,2.0,2.6,4.0)
    print(f"  A0^2={A:5}: interior minima = {len(r)}   "+("" if not r else f"min@D={r[0]['Dm']:.3f}"))

print("\nEXTEND the ratio (constructor stopped at A0^2=100). Same floor=2,D*=2.6,k=4:")
for A in [200,500,1000,5000,1e4,1e5]:
    r=well_report(1.0,A,2.0,2.6,4.0)
    if r:
        w=r[0]
        print(f"  A0^2={A:8.0f}: WELL  min@D={w['Dm']:.3f}  omega2={w['w2m']:.3f}  "
              f"left_barrier={w['left_barrier']:.3f}  right_barrier={w['right_barrier']:.3f}")
    else:
        print(f"  A0^2={A:8.0f}: monotone (no interior min)")

print("\nEquivalently FIX A0^2=5 (constructor) and lower c_grav (tagged CHOSE/cancels):")
for cg in [1.0,0.1,1e-2,1e-3,1e-4]:
    r=well_report(cg,5.0,2.0,2.6,4.0)
    if r:
        w=r[0]
        print(f"  c_grav={cg:.0e}: WELL  min@D={w['Dm']:.3f}  omega2={w['w2m']:.3f}  "
              f"left_barrier={w['left_barrier']:.4f}  right_barrier={w['right_barrier']:.4f}")
    else:
        print(f"  c_grav={cg:.0e}: monotone")

print("\nAre these wells REAL (omega2>0 at min, finite barrier both sides)? "
      "And does the LEFT barrier actually confine, or is U(0) still the global min?")
for cg,A,fl,Ds,k in [(1.0,1e4,2.0,2.6,4.0),(1e-3,5.0,2.0,2.6,4.0),(1.0,1e3,12.0,3.4,3.5)]:
    r=well_report(cg,A,fl,Ds,k)
    if r:
        w=r[0]
        # is it a TRUE confining double-well (U0 above the min => left barrier real)?
        confining = (w['U0']>w['Um']) and (w['UDstar']>w['Um'])
        print(f"  c_grav={cg:.0e} A0^2={A:.0e} fl={fl} D*={Ds} k={k}: min@D={w['Dm']:.3f} "
              f"omega2={w['w2m']:.3f}  U(0)={w['U0']:.3f} U_min={w['Um']:.3f} U(D*)={w['UDstar']:.3f}  "
              f"-> {'TRUE interior well (U0>Umin & UDstar>Umin)' if confining else 'NOT a true well (D=0 is lower)'}")

print("""
CRITICAL DIAGNOSIS:
  The interior minimum at D~1.7 appears because the carrier term (1/2)A0^2*omega2(D)
  starts at +(1/2)A0^2*floor at D=0 and DROPS to 0 at D*. That drop is a DOWNWARD
  ramp of height (1/2)A0^2*floor. If that height exceeds the exponential's rise over
  the SAME interval, U dips then rises -> a TRUE interior minimum with omega2>0.
  BUT: the carrier term is MONOTONE DECREASING (drops from +X to 0). So U = (rising exp)
  + (decreasing-to-0 carrier). The left edge value U(0) = E_grav(0) + (1/2)A0^2*floor
  = 0 + (1/2)A0^2*floor is ELEVATED by the full carrier energy. The minimum sits where
  the carrier has dropped enough. So U(0) can be ABOVE the interior min => the carrier
  energy at D=0 IS the left barrier. This is a GENUINE interior well, not fake, not
  tachyonic (omega2>0 throughout).
""")
