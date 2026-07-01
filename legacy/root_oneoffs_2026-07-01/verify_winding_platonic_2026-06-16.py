#!/usr/bin/env python3
"""Blind verifier: PROPER platonic-instability re-test on SH-EXACT grid,
amplitude-scaled, multiple seed shapes (cos2psi, cos3psi, tetrahedral combo).

For each sector m in {2,3}:
  1. Converge the axisym winding soliton on the SH-exact grid.
  2. For each platonic seed shape and amplitude:
       Th_seed = Th + amp*shape
       re-solve full coupled Newton on SH-exact grid.
       record psivar(seed) -> psivar(relaxed), M_MS round vs relaxed, Phi_after.
     If converged psivar stays ~ injected (or grows) AND M drops => lower non-axisym state.
     decay ratio = psivar_relaxed / psivar_seed.
"""
import os, sys, time, json
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK","0")
os.environ.setdefault("PYTORCH_NO_CUDA_MEMORY_CACHING","1")
import numpy as np, torch
torch.set_default_dtype(torch.float64)
sys.path.insert(0,'/home/udt-admin/udt_mass_codex')
from full3d_grid_shexact import make_grid_shexact
from full3d_spectral import build_metric, PI
from full3d_solver import pack, unpack
import full3d_newton as NEW
import winding_catalog_map as WC

def platonic_shapes(G):
    r=G.Rg; sth=G.STHg; cth=torch.cos(G.THg); ps=G.PSg
    rc,ri=G.rc,G.ri
    env=torch.sin(PI*(r-rc)/(ri-rc))
    return {
      'cos2psi': env*sth*torch.cos(2*ps),
      'cos3psi': env*sth*torch.cos(3*ps),
      # tetra/cubic-type: combine l=2,m=2-like + l=3,m=2-like angular content
      'tetra':   env*sth*( torch.cos(2*ps)*cth + 0.5*torch.cos(3*ps)*sth ),
    }

def run_sector(Nr,Nth,Nps,m,p=0.4,kap8=0.05,maxit=40,relax_maxit=30,
               amps=(0.03,0.08,0.15,0.30,0.6)):
    mmax=Nps//2
    G=make_grid_shexact(Nr,Nth,Nps,rc=0.05,cell=14.0,mmax=mmax)
    t0=time.time()
    # converge axisym base on SH-exact grid
    u0,rsol=WC.winding_seed(G,m,p=p,kap8=kap8)
    u,hist=NEW.newton_solve(u0,G,p,kap8,m=m,maxit=maxit,tol=1e-12,verbose=False)
    dg0,comp0=WC.full_diag(u,G,p,kap8,m)
    print(f"[m={m}] base SH-exact: Phi {hist[0]:.2e}->{hist[-1]:.2e} M={dg0['M_MS']:.5f} "
          f"psivar={dg0['psivar']:.2e} tvar={dg0['tvar']:.3e} maxres={max(comp0.values()):.2e}",flush=True)
    a,b,c,d,Th=unpack(u,G)
    shapes=platonic_shapes(G)
    recs=[]
    for nm,sh in shapes.items():
        for amp in amps:
            Th2=Th+amp*sh
            useed=pack(a.clone(),b.clone(),c.clone(),d.clone(),Th2)
            dgs,_=WC.full_diag(useed,G,p,kap8,m)
            ur,hr=NEW.newton_solve(useed,G,p,kap8,m=m,maxit=relax_maxit,tol=1e-12,verbose=False)
            dgr,compr=WC.full_diag(ur,G,p,kap8,m)
            decay=dgr['psivar']/max(dgs['psivar'],1e-30)
            dM=dgr['M_MS']-dg0['M_MS']
            rec=dict(m=m,shape=nm,amp=amp,
                     psivar_seed=dgs['psivar'],psivar_relaxed=dgr['psivar'],
                     decay=decay,M_base=dg0['M_MS'],M_relaxed=dgr['M_MS'],dM=dM,
                     Phi_after=hr[-1],maxres=max(compr.values()))
            recs.append(rec)
            flag="  *** LOWER+PSI ***" if (dM< -1e-4 and dgr['psivar']>1e-4) else ""
            print(f"  [m={m} {nm:8s} amp={amp:.2f}] psivar {dgs['psivar']:.2e}->{dgr['psivar']:.2e} "
                  f"(decay {decay:.2e}) dM={dM:+.4e} Phi={hr[-1]:.1e}{flag}",flush=True)
    return dict(m=m,base=dict(M=dg0['M_MS'],psivar=dg0['psivar'],tvar=dg0['tvar'],
                Phi=hist[-1],maxres=max(comp0.values())),probes=recs)

if __name__=="__main__":
    out=[]
    # m=2 first (floor-converged sector); modest grid for cost
    out.append(run_sector(18,8,8,2,maxit=40,relax_maxit=30))
    json.dump(out,open("/tmp/verify_platonic_m2.json","w"),indent=1)
    print("DONE_M2",flush=True)
    out.append(run_sector(18,8,8,3,maxit=40,relax_maxit=30))
    json.dump(out,open("/tmp/verify_platonic_out.json","w"),indent=1)
    print("DONE_PLATONIC",flush=True)
