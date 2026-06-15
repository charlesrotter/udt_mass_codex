#!/usr/bin/env python3
"""Final nail: res_rr = res_tt - k8(p_r+rho) EXACTLY (since G^t_t=G^r_r identically).
So the (r,r) residual = (t,t) FD error  +  the analytic EOS gap -k8(p_r+rho).
As FD->exact, res_tt->0 and res_rr -> -k8(p_r+rho) which is NONZERO in the body.
That is the genuine inconsistency.  Driver: Claude verifier 2026-06-15."""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import numpy as np, torch
import complete_metric_batched as cm
torch.set_default_dtype(torch.float64)
DEV = "cuda" if torch.cuda.is_available() else "cpu"
xi=kap=1.0; rc=0.05; ri=rc+14.0; P=0.4; K8=0.05

print("Identity check  res_rr - res_tt == -k8(p_r+rho)  [from G^t_t=G^r_r exactly]")
print("and convergence of res_tt->0 (so res_rr -> -k8(p_r+rho) != 0 in body):\n")
import sys
for N in [700,1400,2800]:
    rg=torch.linspace(rc,ri,N,device=DEV).unsqueeze(0)
    o=cm.selfconsistent_batched(rg,xi,kap,p=P,kap8=K8,iters=160,relax=0.4,tol=1e-11)
    r=o['r'][0].cpu().numpy();Th=o['Th'][0].cpu().numpy();phi=o['phi'][0].cpu().numpy()
    Thp=o['Thp'][0].cpu().numpy();phip=np.gradient(phi,r)
    X=np.exp(-2*phi)*Thp**2;Y=np.sin(Th)**2/r**2
    rho=(xi/2)*(X+2*Y)+(kap/2)*(2*X*Y+Y**2)
    pr=(xi/2)*(X-2*Y)+(kap/2)*(2*X*Y-Y**2)
    G=(-2*phip*r-np.exp(2*phi)+1)*np.exp(-2*phi)/r**2   # G^t_t=G^r_r
    res_tt=G-K8*(-rho); res_rr=G-K8*pr
    # smooth body away from core spike and edges
    b=(np.abs(Thp)>1e-2*np.max(np.abs(Thp)))&(r>rc+1.0)&(np.arange(N)>5)&(np.arange(N)<N-6)
    ident=np.max(np.abs((res_rr-res_tt)-(-K8*(pr+rho))))   # should be ~machine zero (algebraic)
    eos=-K8*(pr+rho)
    print(f"  N={N:5d}: |res_rr-res_tt+k8(p_r+rho)|_max={ident:.2e} (algebraic id)  "
          f"body: max|res_tt|={np.max(np.abs(res_tt[b])):.3e}  "
          f"mean|k8(p_r+rho)|={np.mean(np.abs(eos[b])):.3e}  max|k8(p_r+rho)|={np.max(np.abs(eos[b])):.3e}"); sys.stdout.flush()
print("""
=> The algebraic identity holds to machine zero: res_rr = res_tt - k8(p_r+rho).
   res_tt is pure FD truncation (shrinks as N grows in the smooth body).
   -k8(p_r+rho) is the ANALYTIC EOS gap: NONZERO and resolution-independent in the body,
   zero in the exterior.  THIS is the irreducible (r,r) violation.  REAL, not artifact.
""")
