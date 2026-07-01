#!/usr/bin/env python3
"""GATE A + GATE B harness for P5a' (re-pose + JFNK).  Branch p5a-prime-repose.
Driver: Claude Opus 4.8.  2026-06-20.  DATA-BLIND.  NEW FILE.

GATE A: the re-pose is FULL-RANK and preserves the physics.
  A1: reposed J is full-rank (kappa~1e4-1e6, ~0 near-zero) -- vs full-space ~1e18/216.
  A2: reposed DENSE solve reaches floor on the COMMITTED residual when embedded.
  A3: the reposed solution's physical observables (M_MS, tvar, psivar) match the
      full-space dense anchor -- the re-pose removed only spurious/unconstrained
      (gauge, ~95% edge-supported) DOF, not physics.  We ALSO project the anchor
      into the spectral gauge and compare the BODY DOF field-by-field.
GATE B: reposed JFNK (matrix-free LSMR) reaches the SAME reposed fixed point as the
        reposed dense solve (~floor, field-by-field) + PC-independence (none vs
        fieldblock -> same solution).
"""
import os, time, math
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK","0")
os.environ.setdefault("PYTORCH_NO_CUDA_MEMORY_CACHING","1")
import numpy as np, torch
torch.set_default_dtype(torch.float64)
from full3d_spectral import Grid3D, attach_coord_weight, residuals, diagnostics
from full3d_solver import residual_vector, round_seed, unpack
import full3d_newton as NW
import p5a_prime_repose as RP

NR,NTH,NPS = 12,6,8
P,KAP8 = 0.4,0.05
G = Grid3D(NR,NTH,NPS,rc=0.05,cell=14.0); G=attach_coord_weight(G)
u0,sol = round_seed(G,p=P,kap8=KAP8)
Nr=G.Nr; n=G.Nr*G.Nth*G.Nps; dev=u0.device
rp = RP.Repose(G,p=P,m=1,edge_mode='spectral',fit_deg=4)
ub0 = rp.extract(u0)
fields=['a','b','c','d','Th']

def phys(u,tag):
    F=residual_vector(u,G,P,KAP8); Phi=float((F*F).sum())
    out=residuals(G,unpack(u,G),P,KAP8); d=diagnostics(G,out,KAP8)
    print(f"  [{tag}] committed-Phi={Phi:.3e} M_MS={d['M_MS']:.6f} tvar={d['tvar']:.4e} psivar={d['psivar']:.4e}",flush=True)
    return Phi,d

def body_fields(u):
    u5=u.reshape(5,Nr,NTH,NPS); return u5[:,3:Nr-3]

print("=== full-space dense ANCHOR ===",flush=True)
t=time.time()
ua,ha = NW.newton_solve(u0,G,P,KAP8,maxit=30,lam0=1e-4,tol=1e-12,verbose=False)
print(f"  anchor Phi={ha[-1]:.3e} iters={len(ha)-1} time={time.time()-t:.0f}s",flush=True)
phys(ua,"anchor")

print("=== GATE A: reposed DENSE (spectral gauge, jacrev) ===",flush=True)
t=time.time()
ubd,hd = RP.reposed_dense_solve_fast(ub0,rp,KAP8,maxit=40,lam0=1e-4,tol=1e-13,verbose=True)
print(f"  reposed-dense reposed-Phi={hd[-1]:.3e} iters={len(hd)-1} time={time.time()-t:.0f}s",flush=True)
ud_full = rp.embed_vsafe(ubd)
phys(ud_full,"reposed-dense->committed")
Jb,_=RP.reposed_jacobian_jacrev(ubd,rp,KAP8)
S=torch.linalg.svdvals(Jb)
print(f"  A1 reposed-J@sol: kappa={float(S[0]/S[-1]):.3e} near-zero(<1e-8)={int((S<1e-8*S[0]).sum())} smallest3={[f'{x:.2e}' for x in S[-3:].tolist()]}",flush=True)
print("  A3 body field-by-field max|reposed-dense - anchor| (BODY DOF):",flush=True)
bd=(body_fields(ud_full)-body_fields(ua)).abs()
for f in range(5):
    print(f"     {fields[f]}: {bd[f].max().item():.3e}",flush=True)

print("=== GATE B: reposed JFNK (LSMR), PC-independence ===",flush=True)
res={}
for pc in ['none','fieldblock']:
    t=time.time()
    ubj,hj,its,wt = RP.reposed_jfnk_solve(ub0,rp,u0,KAP8,maxit=50,lam0=1e-4,tol=1e-13,
                                          pc=pc,lsmr_maxit=1000,lsmr_tol=1e-12,verbose=True)
    diff=(ubj-ubd).abs().max().item()
    print(f"  JFNK[pc={pc}] reposed-Phi={hj[-1]:.3e} iters={len(hj)-1} lsmr_avg={np.mean(its) if its else 0:.0f} time={wt:.0f}s max|diff vs reposed-dense|={diff:.3e}",flush=True)
    phys(rp.embed_vsafe(ubj),f"JFNK[{pc}]->committed")
    res[pc]=ubj
pcind=(res['none']-res['fieldblock']).abs().max().item()
print(f"  GATE B PC-independence: max|none - fieldblock| = {pcind:.3e}",flush=True)

torch.save({'ubd':ubd.cpu(),'ua':ua.cpu(),'none':res['none'].cpu(),'fieldblock':res['fieldblock'].cpu()},'/tmp/repose_gateAB.pt')
print("=== GATE A/B DONE ===",flush=True)
