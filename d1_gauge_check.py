import os
os.environ.setdefault('PYTORCH_NVML_BASED_CUDA_CHECK', '0')
import torch, numpy as np
torch.set_default_dtype(torch.float64)
import p1_residual_general_einstein as P1
import free_s2_matter as S2M, whole_metric_3d_matter as MAT
from full3d_spectral import attach_coord_weight, Grid3D, build_metric, T, R as RR, TH, PS
from full3d_newton import inv4x4
from torch.func import jacrev
G = attach_coord_weight(Grid3D(Nr=8, Nth=6, Nps=8, rc=0.1, cell=8.0))
d = torch.load('galerkin_floored_X1.pt', map_location='cpu', weights_only=False)
u = d['u'].to(G.Dr.device); X=-1.0

def observe(u):
    a,b,c,dd,n1,n2,n3,phi,ert,erp,etp = P1.unpack11(u,G)
    n=torch.stack([n1,n2,n3],-1); dn=S2M.field_dn_components_exact(G,n)
    g=build_metric(G,a,b,c,dd,e_rt=ert,e_rp=erp,e_tp=etp); gi=inv4x4(g)
    rho=-torch.einsum('...ma,...an->...mn',gi,MAT.stress_tensor(g,gi,dn,1.0,1.0)[0])[...,T,T]
    nrm=torch.sqrt(torch.clamp((n**2).sum(-1),min=1e-300)); wth=G.wmu/G.sth; dpl=wth[None,:,None]*G.wps[None,None,:]
    crs=torch.cross(dn[...,TH,:],dn[...,PS,:],dim=-1); Q=((n/nrm[...,None]*crs).sum(-1)*dpl).sum((1,2))/(4*np.pi)
    return dict(Q=float(Q[2:-2].mean()), rho_max=float(rho[G.body].abs().max()),
                lapse_min=float(torch.exp(a)[G.body].min()),
                warp=max(float(x.abs().max()) for x in (a,b,c,dd)), phi_absmax=float(phi.abs().max()))

ob=observe(u)
print(f"=== RE-GRADE on galerkin-floored field (Phi={d['Phi']:.3e}, X=-1) ===", flush=True)
print(f"  {ob}", flush=True)
print(f"  OLD X=-1 crawl-floor (Phi=2e-3): Q=1.000 rho_max=0.0097 lapse_min=0.55 warp=2.57 phi_absmax=0.90", flush=True)
f=lambda uu: P1.residual_vector_p1(uu,G,1.0,1.0,X=X,branch='G',determined=True)
F=f(u); J=jacrev(f,chunk_size=128)(u).double()
U,S,Vh=torch.linalg.svd(J,full_matrices=False); sv=S.cpu().numpy()
c=(U.transpose(-1,-2)@F).cpu().numpy()                       # residual per singular direction
Phi=float((F*F).sum()); red=float((c*c).sum())
gauge = sv < 1e-3                                            # benign gauge band (smin~8.5e-5)
print(f"\n  Phi={Phi:.3e}  reducible(in range J)={red:.3e} ({100*red/Phi:.1f}%)", flush=True)
print(f"  reducible residual in GAUGE band (SV<1e-3, n={int(gauge.sum())}): {float((c[gauge]**2).sum()):.3e} "
      f"({100*float((c[gauge]**2).sum())/red:.1f}% of reducible)", flush=True)
print(f"  reducible residual in PHYSICAL band (SV>=1e-3):                 {float((c[~gauge]**2).sum()):.3e} "
      f"({100*float((c[~gauge]**2).sum())/red:.1f}% of reducible)", flush=True)
print("INTERPRET: if the reducible residual is mostly in the GAUGE band -> reducing it needs huge gauge-direction"
      " steps (the crawl) and the PHYSICS is floored (observables trustworthy). If mostly PHYSICAL -> under-converged.", flush=True)
