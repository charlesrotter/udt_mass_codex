#!/usr/bin/env python3
"""Stage 2: FAST matrix-free JFNK GATE B (PC-independence) + GATE C (#60 beat).
JFNK-ONLY => caching allocator (no-cache flag NOT set) => ~2x faster.  Loads the
reposed DENSE reference from /tmp/dense_refs.pt (Stage 1).  Branch p5a-prime-repose.
Driver: Claude Opus 4.8.  2026-06-20.  DATA-BLIND.  NEW FILE."""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK","0")
# deliberately NOT setting PYTORCH_NO_CUDA_MEMORY_CACHING (JFNK matrix-free needs no vmap)
import time, math
import numpy as np, torch
import sys; sys.path.insert(0,'/home/udt-admin/udt_mass_codex')
torch.set_default_dtype(torch.float64)
from full3d_spectral import Grid3D, attach_coord_weight, residuals, diagnostics
from full3d_solver import residual_vector, round_seed, unpack, lm_solve
import p5a_prime_repose as RP

NR,NTH,NPS=12,6,8; P,KAP8=0.4,0.05; LCAP=1000
G=Grid3D(NR,NTH,NPS,rc=0.05,cell=14.0); G=attach_coord_weight(G)
u0,sol=round_seed(G,p=P,kap8=KAP8); Nr=G.Nr; dev=u0.device
refs=torch.load('/tmp/dense_refs.pt',weights_only=True)
ubd1=refs['ubd1'].to(dev); ua=refs['ua'].to(dev)
fields=['a','b','c','d','Th']
def phys(u,tag):
    F=residual_vector(u,G,P,KAP8); Phi=float((F*F).sum())
    d=diagnostics(G,residuals(G,unpack(u,G),P,KAP8),KAP8)
    print(f"  [{tag}] Phi={Phi:.3e} M_MS={d['M_MS']:.6f} tvar={d['tvar']:.4e}",flush=True); return Phi,d

print("=== GATE B (fast JFNK, LCAP=%d): round + PC-independence ==="%LCAP,flush=True)
rp=RP.Repose(G,p=P,m=1,edge_mode='hold',fit_deg=4); rp.set_edge_hold(u0); ub0=rp.extract(u0)
print(f"  dense reference (Stage 1): reposed-Phi={float(((RP.reposed_residual(ubd1,rp,u0,KAP8))**2).sum()):.3e}",flush=True)
res={}
for pc in ['none','fieldblock']:
    t=time.time()
    ubj,hj,its,wt=RP.reposed_jfnk_solve(ub0,rp,u0,KAP8,maxit=70,lam0=1e-4,tol=1e-12,
                                        pc=pc,lsmr_maxit=LCAP,lsmr_tol=1e-11,verbose=True)
    # field-by-field on body DOF vs dense reference
    db=(ubj-ubd1).reshape(5,Nr-6,NTH,NPS).abs()
    fb=" ".join(f"{fields[f]}={db[f].max().item():.2e}" for f in range(5))
    print(f"  JFNK[{pc}] reposed-Phi={hj[-1]:.3e} newton={len(hj)-1} lsmr_avg={np.mean(its) if its else 0:.0f} time={wt:.0f}s",flush=True)
    print(f"     field-by-field max|JFNK-dense| (BODY): {fb}",flush=True)
    res[pc]=ubj
print(f"  GATE B PC-independence: max|none - fieldblock| = {(res['none']-res['fieldblock']).abs().max().item():.3e}",flush=True)

print("=== GATE C (fast JFNK): beat the #60 axisym-l2 stall ===",flush=True)
useed=RP.axi_l2_seed(G,u0,amp=0.25,m=1); phys(useed,"seed")
# old Jacobi-PCG control (the documented #60 stall) -- matrix-free, no jacrev, fast
t=time.time(); uc,hc=lm_solve(useed,G,P,KAP8,maxit=40,lam0=1e-3,verbose=False,tol=1e-11)
print(f"  #60 control (Jacobi-PCG LM) final committed-Phi={hc[-1]:.3e} iters={len(hc)-1} time={time.time()-t:.0f}s",flush=True); phys(uc,"control")
rpC=RP.Repose(G,p=P,m=1,edge_mode='hold',fit_deg=4); rpC.set_edge_hold(useed); ubc0=rpC.extract(useed)
t=time.time()
ubcj,hjc,itsc,wtc=RP.reposed_jfnk_solve(ubc0,rpC,useed,KAP8,maxit=90,lam0=1e-4,tol=1e-12,
                                         pc='none',lsmr_maxit=LCAP,lsmr_tol=1e-11,verbose=True)
print(f"  GATE C JFNK reposed-Phi={hjc[-1]:.3e} newton={len(hjc)-1} lsmr_avg={np.mean(itsc) if itsc else 0:.0f} time={wtc:.0f}s",flush=True)
print(f"  GATE C residual history: {['%.2e'%x for x in hjc]}",flush=True)
phys(rpC.embed_vsafe(ubcj),"GATE-C->committed")
v='PASS' if hjc[-1]<=1e-9 else ('PARTIAL' if hjc[-1]<hc[-1]/10 else 'FAIL')
print(f"  GATE C VERDICT: control stalled ~{hc[-1]:.1e}; JFNK reached {hjc[-1]:.1e} -> {v}",flush=True)
torch.save({'none':res['none'].cpu(),'fieldblock':res['fieldblock'].cpu(),'ubcj':ubcj.cpu()},'/tmp/jfnk_fast.pt')
print("=== JFNK FAST DONE ===",flush=True)
