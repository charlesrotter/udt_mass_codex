"""
depth_selector_verif_truewell.py
================================
RESOLVE: is there a TRUE interior local minimum (dU/dD: + -> - -> +, strictly inside
(0,D*), with omega2>0 at the min AND a positive barrier on BOTH sides), or does the
carrier drop always pull the global min to the cap D* (omega2->0)?

dU/dD = c_grav[2 e^{2D}] - (1/2)A0^2 c_bind k D^{k-1}.  Divide by c_grav, R=A0^2/c_grav:
   g(D) = 2 e^{2D} - (1/2) R cb k D^{k-1},   cb=floor/D*^k.
A true interior MIN needs g(D)=0 with g'<0->... i.e. g goes + (small D) -> - -> + ?
Actually g(0+)=2>0 (since D^{k-1}->0 for k>1). For an interior MIN of U we need g to cross
0 downward (U slope + to -) at some D1, then cross 0 upward (- to +) at D2>D1, both <D*.
The MIN is at D1 (first downward crossing) -- wait, U'=g: U decreasing where g<0. So:
  U rises (g>0) on (0,D1), falls (g<0) on (D1,D2), rises (g>0) on (D2,D*).
  => D1 is a local MAX, D2 is a local MIN.  The interior MINIMUM is at D2.
For D2 to be a real interior min with omega2>0 we need D2<D* AND omega2(D2)>0.
Count sign changes of g on (0,D*) at high precision.
"""
import numpy as np

def g_roots(R,floor,Dstar,k,n=4_000_000):
    cb=floor/Dstar**k
    D=np.linspace(1e-7,Dstar,n)
    g=2*np.exp(2*D)-0.5*R*cb*k*D**(k-1)
    s=np.sign(g)
    cross=np.where(np.diff(s)!=0)[0]
    roots=D[cross]
    return roots,D,g,cb

def classify(R,floor,Dstar,k):
    roots,D,g,cb=g_roots(R,floor,Dstar,k)
    # sign of g just left of each root tells +->- (local max of U) or -->+ (local min of U)
    info=[]
    for r in roots:
        i=np.searchsorted(D,r)
        left=g[max(i-3,0)]; right=g[min(i+3,len(g)-1)]
        kind='Umax' if (left>0 and right<0) else ('Umin' if (left<0 and right>0) else 'flat')
        w2=floor-cb*r**k
        info.append((r,kind,w2))
    return info

print("="*78)
print("Search for a TRUE interior local MIN of U (g: +->-->+) with omega2>0, below D*")
print("="*78)
floor,Dstar,k=2.0,2.6,4.0
print(f"\nfloor={floor} D*={Dstar} k={k}: scan R=A0^2/c_grav")
for R in [100,136,140,150,170,200,250,300,400,600,1000,3000]:
    info=classify(R,floor,Dstar,k)
    mins=[(r,w2) for (r,kind,w2) in info if kind=='Umin']
    maxs=[(r,w2) for (r,kind,w2) in info if kind=='Umax']
    if mins:
        rm,w2m=mins[0]
        print(f"  R={R:5}: interior Umin at D={rm:.3f} (omega2={w2m:.3f}); Umax at "
              f"{[round(x[0],3) for x in maxs]}  -> TRUE double-well? {rm<Dstar-1e-3 and w2m>1e-3}")
    else:
        # monotone-ish or min pinned at D*
        print(f"  R={R:5}: no interior Umin (g crossings: {[(round(r,3),kind) for r,kind,_ in info]}) "
              f"-> min at boundary (D=0 or D*)")

# The decisive structural fact: as R grows, the local Umin D2 -> D* (pinned to cap) because
# the carrier downpull (1/2)R cb k D^{k-1} only crosses 2e^{2D} once it is large, near D*.
# Print the Umin location vs D* as R grows to show it RIDES the cap, not a free interior well.
print("\nDoes the interior Umin (when it exists) ride the cap D* as R grows?")
for R in [136,138,141,145,150,160,180,220,300,500,1000,5000]:
    info=classify(R,floor,Dstar,k)
    mins=[(r,w2) for (r,kind,w2) in info if kind=='Umin']
    if mins:
        rm,w2m=mins[0]
        print(f"  R={R:5}: Umin@D={rm:.4f}  (D*-Dmin={Dstar-rm:.4f})  omega2={w2m:.4f}")
    else:
        print(f"  R={R:5}: no interior Umin")
print(f"\n  D*={Dstar}.  If Umin stays a FIXED finite distance below D* with omega2 bounded away")
print("  from 0 -> a genuine free interior well (RESCUE). If D*-Dmin shrinks / omega2->0 as R")
print("  grows -> the well only exists in a narrow R sliver pinned to the cap (NON-CLOSURE survives).")
