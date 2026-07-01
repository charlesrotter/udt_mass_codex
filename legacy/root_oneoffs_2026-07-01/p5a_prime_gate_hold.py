#!/usr/bin/env python3
"""GATE A (full-rank + physics-invariance) + GATE B (JFNK + PC-independence) for the
'hold' re-pose.  Branch p5a-prime-repose.  Driver: Claude Opus 4.8.  2026-06-20.
DATA-BLIND.  NEW FILE.

The 'hold' re-pose: unknowns = BODY radial rows [3:Nr-3] (full-rank).  The 6 excised
edge rows per field are HELD fixed at a smooth/regular gauge (the round-seed edge
rows), endpoints pinned by the analytic BC values.  This is the verifier's literal
prescription ("drop the excised-edge columns; solve only body DOF").

GATE A:
  A1 full-rank: reposed-J kappa ~1e4-1e6, ~0 near-zero (vs full-space ~1e18/216).
  A2 floor: hold-dense reaches floor on the committed residual.
  A3 PHYSICS-INVARIANCE: solve hold with TWO different regular edge gauges; compare
     M_MS/tvar.  If the physics is gauge-invariant, the re-pose preserves physics
     (the edge DOF are spurious gauge).  Compare also to the full-space anchor.
GATE B: hold-JFNK == hold-dense fixed point (~floor, field-by-field) + PC-independence.
"""
import os, time, math
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK","0")
os.environ.setdefault("PYTORCH_NO_CUDA_MEMORY_CACHING","1")
import numpy as np, torch
torch.set_default_dtype(torch.float64)
from full3d_spectral import Grid3D, attach_coord_weight, residuals, diagnostics
from full3d_solver import residual_vector, round_seed, unpack, pack
import full3d_newton as NW
import p5a_prime_repose as RP

NR,NTH,NPS = 12,6,8
P,KAP8 = 0.4,0.05
G = Grid3D(NR,NTH,NPS,rc=0.05,cell=14.0); G=attach_coord_weight(G)
u0,sol = round_seed(G,p=P,kap8=KAP8)
Nr=G.Nr; dev=u0.device
fields=['a','b','c','d','Th']

def phys(u,tag):
    F=residual_vector(u,G,P,KAP8); Phi=float((F*F).sum())
    out=residuals(G,unpack(u,G),P,KAP8); d=diagnostics(G,out,KAP8)
    print(f"  [{tag}] committed-Phi={Phi:.3e} M_MS={d['M_MS']:.6f} tvar={d['tvar']:.4e} psivar={d['psivar']:.4e}",flush=True)
    return Phi,d

# full-space anchor for physics reference
print("=== full-space dense ANCHOR (physics reference) ===",flush=True)
ua,ha = NW.newton_solve(u0,G,P,KAP8,maxit=30,lam0=1e-4,tol=1e-12,verbose=False)
print(f"  anchor Phi={ha[-1]:.3e} iters={len(ha)-1}",flush=True)
_,danc=phys(ua,"anchor")

# gauge 1: round-seed edges ; gauge 2: anchor edges (a different regular gauge)
def make_rp(edge_ref):
    rp=RP.Repose(G,p=P,m=1,edge_mode='hold',fit_deg=4)
    rp.set_edge_hold(edge_ref)
    return rp

print("=== GATE A2/A3: hold-dense, gauge G1 (round-seed edges) ===",flush=True)
rp1=make_rp(u0); ub0=rp1.extract(u0)
t=time.time()
ubd1,hd1=RP.reposed_dense_solve_fast(ub0,rp1,KAP8,maxit=30,lam0=1e-4,tol=1e-13,verbose=True)
print(f"  G1 hold-dense reposed-Phi={hd1[-1]:.3e} iters={len(hd1)-1} time={time.time()-t:.0f}s",flush=True)
ud1=rp1.embed_vsafe(ubd1); _,d1=phys(ud1,"hold-dense-G1->committed")
Jb,_=RP.reposed_jacobian_jacrev(ubd1,rp1,KAP8); S=torch.linalg.svdvals(Jb)
print(f"  A1 reposed-J@sol(G1): kappa={float(S[0]/S[-1]):.3e} near-zero={int((S<1e-8*S[0]).sum())}",flush=True)

print("=== GATE A3: hold-dense, gauge G2 (anchor edges) -- physics invariance ===",flush=True)
rp2=make_rp(ua)
ubd2,hd2=RP.reposed_dense_solve_fast(rp2.extract(u0),rp2,KAP8,maxit=30,lam0=1e-4,tol=1e-13,verbose=True)
print(f"  G2 hold-dense reposed-Phi={hd2[-1]:.3e} iters={len(hd2)-1}",flush=True)
ud2=rp2.embed_vsafe(ubd2); _,d2=phys(ud2,"hold-dense-G2->committed")
print(f"  >>> PHYSICS-INVARIANCE G1 vs G2: dM_MS={abs(d1['M_MS']-d2['M_MS']):.3e} dtvar={abs(d1['tvar']-d2['tvar']):.3e}",flush=True)
print(f"  >>> vs ANCHOR: G1 dM_MS={abs(d1['M_MS']-danc['M_MS']):.3e} dtvar={abs(d1['tvar']-danc['tvar']):.3e} ; G2 dM_MS={abs(d2['M_MS']-danc['M_MS']):.3e} dtvar={abs(d2['tvar']-danc['tvar']):.3e}",flush=True)

print("=== GATE B: hold-JFNK (LSMR) on gauge G1, PC-independence ===",flush=True)
res={}
for pc in ['none','fieldblock']:
    t=time.time()
    ubj,hj,its,wt=RP.reposed_jfnk_solve(ub0,rp1,u0,KAP8,maxit=50,lam0=1e-4,tol=1e-13,
                                        pc=pc,lsmr_maxit=1000,lsmr_tol=1e-12,verbose=True)
    diff=(ubj-ubd1).abs().max().item()
    print(f"  JFNK[pc={pc}] reposed-Phi={hj[-1]:.3e} iters={len(hj)-1} lsmr_avg={np.mean(its) if its else 0:.0f} time={wt:.0f}s max|diff vs hold-dense|={diff:.3e}",flush=True)
    phys(rp1.embed_vsafe(ubj),f"JFNK[{pc}]->committed")
    res[pc]=ubj
print(f"  GATE B PC-independence: max|none-fieldblock|={(res['none']-res['fieldblock']).abs().max().item():.3e}",flush=True)
torch.save({'ubd1':ubd1.cpu(),'ua':ua.cpu(),'none':res['none'].cpu(),'fieldblock':res['fieldblock'].cpu(),'rp1_edge':rp1.edge_hold.cpu()},'/tmp/repose_hold.pt')
print("=== GATE HOLD DONE ===",flush=True)
