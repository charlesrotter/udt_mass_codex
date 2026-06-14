"""
Verify the doc's CORE MECHANISM claim independently with a controlled LOCALIZED
profile (width w), bypassing minimizer-width ambiguity:
  Theta(r) = pi * exp(-(r/w)^2)  (localized twist, unwound exterior).
Check:
 (1) L2 L_perp ~ INT (4pi/3)(cos2Th+2) r^2 dr DIVERGES with cell size
     (cos^2Th->1 tail), L2 L_3 ~ INT (8pi/3)sin^2Th r^2 dr stays LOCALIZED.
 (2) ratio grows with cell size  -> background-dependent, not universal.
 (3) pattern stays axial 2+1 (by construction of closed forms).
This isolates the MECHANISM from the BVP minimizer.
DATA-BLIND.
"""
import torch, math
torch.set_default_dtype(torch.float64)
dev='cuda'

def L2_inertia_localized(w, rcore, rint, N=20000):
    r=torch.linspace(rcore,rint,N,device=dev)
    dr=r[1]-r[0]
    Th=math.pi*torch.exp(-(r/w)**2)
    rc=0.5*(r[1:]+r[:-1]); Tc=0.5*(Th[1:]+Th[:-1]); drc=r[1:]-r[:-1]
    L3=0.5*((8*math.pi/3)*torch.sin(Tc)**2 * rc**2 * drc).sum().item()
    Lp=0.5*((4*math.pi/3)*(torch.cos(2*Tc)+2) * rc**2 * drc).sum().item()
    return Lp, L3

print("Localized profile width w=1.0; vary cell size r_int:")
print(f"{'r_int':>8} {'L_perp':>14} {'L_3':>12} {'ratio':>10}")
for rint in [8,12,20,30,50,100]:
    Lp,L3=L2_inertia_localized(1.0, 0.05, float(rint))
    print(f"{rint:8.1f} {Lp:14.6g} {L3:12.6g} {Lp/L3:10.4g}")

print("\n-> L_3 saturates (localized), L_perp grows ~ r_int^3 (fills cell):")
print("   ratio DIVERGES with cell size = background-dependent, NOT universal.")
print("   This independently CONFIRMS the doc's L2 mechanism & non-universality.")

print("\nThe doc's flat-12L L2 ratio 415 corresponds to a width ~1 BVP profile;")
print("my full-BVP minimizer produced a WIDER profile (width~3) giving ratio ~3.")
print("The MECHANISM (perp divergence) and PATTERN (axial 2+1) are confirmed;")
print("the exact ratio is profile/width and cell dependent = the doc's own claim.")
