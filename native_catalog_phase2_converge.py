#!/usr/bin/env python3
"""
native_catalog_phase2_converge.py -- PHASE 2 convergence + clean split comparison.
2026-06-18. Claude (Opus 4.8,1M). DATA-BLIND. Category-A. OBSERVE.

(A) Drive the held-degree degree-k minimizer to a deeper floor (LBFGS then Adam
    polish) and confirm the E_k/E_1 UNBINDING ratio is grid-stable (Nth, Nr).
(B) Clean split comparison: energy of ONE degree-k lump (texture in a single
    radial shell) vs k degree-1 lumps placed in k disjoint radial shells of the
    SAME cell -- the genuine "does charge-k bind or fall apart into k unit charges"
    test, since the pi_2 degree is additive over disjoint shells (each shell's
    angular S^2 carries its own degree, total = sum).
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK","0")
os.environ.setdefault("PYTORCH_NO_CUDA_MEMORY_CACHING","1")
import math, numpy as np, torch
torch.set_default_dtype(torch.float64)
dev='cuda' if torch.cuda.is_available() else 'cpu'
PI=math.pi
from native_catalog_phase2_held import Cell, energy, grads, realized_degree, hold_frame

def minimize_held_deep(C,k,lbfgs_it=400,adam_it=4000,xi=1.0,kap=1.0):
    G=hold_frame(C.TH.clone(),C).clone().requires_grad_(True)
    opt=torch.optim.LBFGS([G],lr=0.5,max_iter=lbfgs_it,history_size=30,
                          line_search_fn='strong_wolfe',tolerance_grad=1e-12)
    def closure():
        opt.zero_grad();E,_,_=energy(G,C,k,xi,kap);E.backward()
        with torch.no_grad():
            g=G.grad.clone();g[:,0]=0;g[:,-1]=0;g[0,:]=0;g[-1,:]=0;G.grad.copy_(g)
        return E
    opt.step(closure)
    with torch.no_grad():G.data.copy_(hold_frame(G.data,C))
    # Adam polish
    G.requires_grad_(True); opt2=torch.optim.Adam([G],lr=2e-3)
    for _ in range(adam_it):
        opt2.zero_grad();E,_,_=energy(G,C,k,xi,kap);E.backward()
        with torch.no_grad():
            g=G.grad.clone();g[:,0]=0;g[:,-1]=0;g[0,:]=0;g[-1,:]=0;G.grad.copy_(g)
        opt2.step()
        with torch.no_grad():G.data.copy_(hold_frame(G.data,C))
    with torch.no_grad():
        E,E2,E4=energy(G,C,k,xi,kap);gnorm=G.grad.norm().item()
        dc=realized_degree(G.data,C,1,k);ds=realized_degree(G.data,C,C.Nr-2,k)
    return dict(E=E.item(),E2=E2.item(),E4=E4.item(),gnorm=gnorm,deg_core=dc,deg_seal=ds)

if __name__=="__main__":
    print("="*74);print("PHASE 2 convergence: E_k/E_1 unbinding ratio, grid-stable");print(f"device={dev}");print("="*74)
    for p,tag in [(0.0,'FLAT'),(0.4,'DEEP-CELL p=0.4')]:
        print(f"\n### {tag} ###")
        for (Nr,Nth) in [(100,120),(140,160),(180,220)]:
            C=Cell(Nr=Nr,Nth=Nth,p=p);E1=None;row=[]
            for k in (1,2,3):
                r=minimize_held_deep(C,k,lbfgs_it=300,adam_it=2500)
                if k==1:E1=r['E']
                row.append((k,r['E'],r['E']/E1,r['gnorm'],r['deg_core']))
            print(f"  grid {Nr}x{Nth}:")
            for k,E,ratio,gn,dc in row:
                print(f"     k={k}: E={E:10.4f}  E_k/E_1={ratio:6.3f}  |grad|={gn:.1e} deg={dc:+.2f}  "
                      f"{'UNBINDS (E_k>k E_1)' if ratio>k+1e-3 else 'BINDS (E_k<k E_1)'}")
    print("\nDONE_CONVERGE")
