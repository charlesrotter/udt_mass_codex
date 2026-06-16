import os; os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK","0")
import numpy as np, sympy as sp, torch
torch.set_default_dtype(torch.float64)
from spectral_radial_soliton import solve as rsolve
from VERIF_indep_matter import EL_lam
import axisym_matter_el as ME

# Get a converged round soliton (spectral radial), high N.
out=rsolve(96, rc=0.05, cell=14.0, p=0.4, kap8=0.05, maxit=120)
r=out['r']; a=out['a']; b=out['b']; Th=out['Th']; D=out['D']
ap=D@a; bp=D@b; Thp=D@Th
app=D@ap; bpp=D@bp; Thpp=D@Thp
# c=d=0 round; theta=pi/2; all theta-derivs zero
body=(r>0.6)&(r<r[-1]-0.6)
z=np.zeros_like(r)
# independent EL on-shell (round)
mine=np.array([EL_lam(r[i],np.pi/2, a[i],ap[i],0.0,app[i],0.0,0.0,
                      b[i],bp[i],0.0,bpp[i],0.0,0.0,
                      0.,0.,0.,0.,0.,0.,
                      0.,0.,0.,0.,0.,0.,
                      Th[i],Thp[i],0.0,Thpp[i],0.0,0.0, 1.0,1.0) for i in range(r.size)])
comm=np.array([ME.matter_el_resid(r[i],np.pi/2, a[i],b[i],0.,0.,Th[i],
        ap[i],bp[i],0.,0.,Thp[i], 0.,0.,0.,0.,0.,
        app[i],bpp[i],0.,0.,Thpp[i], 0.,0.,0.,0.,0., 0.,0.,0.,0.,0., 1.0,1.0) for i in range(r.size)])
print("ON THE CONVERGED ROUND SOLITON (spectral N=96):")
print(f"  committed axisym EL  max|body| = {np.max(np.abs(comm[body])):.3e}")
print(f"  INDEPENDENT EL       max|body| = {np.max(np.abs(mine[body])):.3e}")
print(f"  radial-residual Fnorm                = {out['Fnorm']:.3e}")
# also: do indep and committed share zero set? ratio where both nonzero
