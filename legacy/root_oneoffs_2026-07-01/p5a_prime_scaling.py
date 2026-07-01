#!/usr/bin/env python3
"""Step 5: light SCALING PROBE for P5a' -- JFNK cost (Krylov-iters x JVP) vs the
dense Jacobian BUILD, at 2 grid sizes.  Confirms the scalability win (the reason JFNK
matters: the dense jacrev build dominates and scales worse).  JFNK-only => caching
allocator (no no-cache flag).  We time, per grid: (a) ONE matrix-free JVP, (b) ONE
JFNK Newton step (its LSMR Krylov iters x JVP), (c) ONE dense reposed Jacobian build
(jacrev) -- run in a SEPARATE no-cache subprocess so the timings are apples-to-apples
for each method's native allocator.  Branch p5a-prime-repose.  2026-06-20.  DATA-BLIND."""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK","0")
import time, math, subprocess, sys
import torch
sys.path.insert(0,'/home/udt-admin/udt_mass_codex')
torch.set_default_dtype(torch.float64)
from full3d_spectral import Grid3D, attach_coord_weight
from full3d_solver import round_seed
import p5a_prime_repose as RP

def jvp_time(G, rp, ub, kap8, nrep=20):
    F0,JT,JV = RP.make_reposed_ops(ub, rp, None, kap8)
    v = torch.randn_like(ub)
    torch.cuda.synchronize() if torch.cuda.is_available() else None
    t=time.time()
    for _ in range(nrep):
        _=JV(v); _=JT(F0)
    torch.cuda.synchronize() if torch.cuda.is_available() else None
    return (time.time()-t)/nrep

for (Nr,Nth,Nps) in [(12,6,8),(16,8,8)]:
    G=Grid3D(Nr,Nth,Nps,rc=0.05,cell=14.0); G=attach_coord_weight(G)
    u0,sol=round_seed(G,p=0.4,kap8=0.05)
    rp=RP.Repose(G,p=0.4,m=1,edge_mode='hold',fit_deg=4); rp.set_edge_hold(u0); ub0=rp.extract(u0)
    nB=rp.nB
    tjvp=jvp_time(G,rp,ub0,0.05)
    # one JFNK Newton step (LSMR cap 400)
    t=time.time()
    ubj,hj,its,wt=RP.reposed_jfnk_solve(ub0,rp,u0,0.05,maxit=1,lam0=1e-4,tol=0.0,
                                        pc='none',lsmr_maxit=400,lsmr_tol=1e-11,verbose=False)
    tstep=time.time()-t; krylov=its[0] if its else 0
    print(f"grid ({Nr},{Nth},{Nps}) nB={nB}: JVP/JT pair={tjvp*1e3:.1f} ms ; JFNK Newton step={tstep:.1f}s (krylov={krylov})",flush=True)

# dense jacrev build timing in a no-cache subprocess (its native allocator)
sub = r'''
import os
os.environ["PYTORCH_NVML_BASED_CUDA_CHECK"]="0"; os.environ["PYTORCH_NO_CUDA_MEMORY_CACHING"]="1"
import time, torch, sys; sys.path.insert(0,"/home/udt-admin/udt_mass_codex")
torch.set_default_dtype(torch.float64)
from full3d_spectral import Grid3D, attach_coord_weight
from full3d_solver import round_seed
import p5a_prime_repose as RP
for (Nr,Nth,Nps) in [(12,6,8),(16,8,8)]:
    G=Grid3D(Nr,Nth,Nps,rc=0.05,cell=14.0); G=attach_coord_weight(G)
    u0,sol=round_seed(G,p=0.4,kap8=0.05)
    rp=RP.Repose(G,p=0.4,m=1,edge_mode="hold",fit_deg=4); rp.set_edge_hold(u0); ub0=rp.extract(u0)
    _=RP.reposed_jacobian_jacrev(ub0,rp,0.05)  # warm
    t=time.time(); J,F=RP.reposed_jacobian_jacrev(ub0,rp,0.05); dt=time.time()-t
    print(f"grid ({Nr},{Nth},{Nps}): dense jacrev BUILD={dt:.1f}s  J shape={tuple(J.shape)}",flush=True)
'''
print("--- dense jacrev build (no-cache subprocess) ---",flush=True)
subprocess.run([sys.executable,"-u","-c",sub])
print("=== SCALING DONE ===",flush=True)
