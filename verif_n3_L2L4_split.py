"""
Run down the ratio discrepancy: decompose L2-only vs L4-only inertia for the
flat 12L cell, and inspect the profile tail. The doc claims L2-only ratio ~415
(perp divergent via cos^2Theta tail), L4-only ratio ~1.17. Verify which dominates
and whether the profile has the long unwound tail.
DATA-BLIND.
"""
import torch, math
torch.set_default_dtype(torch.float64)
dev='cuda' if torch.cuda.is_available() else 'cpu'
from verif_n3_gpu_3d import solve_bvp_profile, inertia_tensor

r,Th,phi=solve_bvp_profile(0.05,12.0,1.0,1.0,0.0,N=4000)
# profile tail inspection
import numpy as np
rn=r.cpu().numpy(); Tn=Th.cpu().numpy()
print("Profile Theta(r) samples (flat 12L):")
for frac in [0.0,0.02,0.05,0.1,0.2,0.4,0.6,0.8,1.0]:
    i=int(frac*(len(rn)-1))
    print(f"  r={rn[i]:7.3f}  Theta={Tn[i]:.4f}  cos^2={math.cos(Tn[i])**2:.4f}")

print("\nL2-only (kappa=0):")
L2=inertia_tensor(r,Th,phi,0.0,1.0,200,200)
d2=torch.diag(L2).cpu().numpy()
print(f"  L_perp={0.5*(d2[0]+d2[1]):.6g} L_3={d2[2]:.6g} ratio={0.5*(d2[0]+d2[1])/d2[2]:.4g}")

print("L4-only (xi=0):")
L4=inertia_tensor(r,Th,phi,1.0,0.0,200,200)
d4=torch.diag(L4).cpu().numpy()
print(f"  L_perp={0.5*(d4[0]+d4[1]):.6g} L_3={d4[2]:.6g} ratio={0.5*(d4[0]+d4[1])/d4[2]:.4g}")

print("\nFull (xi=kappa=1):")
Lf=inertia_tensor(r,Th,phi,1.0,1.0,200,200)
df=torch.diag(Lf).cpu().numpy()
print(f"  L_perp={0.5*(df[0]+df[1]):.6g} L_3={df[2]:.6g} ratio={0.5*(df[0]+df[1])/df[2]:.4g}")

# Cross-check L2 perp/along-3 against pure analytic radial integral of the
# closed forms (8pi/3)sin^2 and (4pi/3)(cos2Th+2), with measure e^{phi}r^2:
print("\nAnalytic radial integral of closed forms (flat, e^{phi}=1):")
dr=r[1:]-r[:-1]; rc=0.5*(r[1:]+r[:-1]); Tc=0.5*(Th[1:]+Th[:-1])
A3=(0.5*1.0)*( (8*math.pi/3)*torch.sin(Tc)**2 * rc**2 * dr).sum().item()
Ap=(0.5*1.0)*( (4*math.pi/3)*(torch.cos(2*Tc)+2) * rc**2 * dr).sum().item()
print(f"  L2 analytic: L_perp={Ap:.6g} L_3={A3:.6g} ratio={Ap/A3:.4g}")
print("  (this is the doc's claimed L2 mechanism; compare to GPU L2 above)")
