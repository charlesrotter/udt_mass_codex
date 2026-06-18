#!/usr/bin/env python3
"""
native_catalog_phase2_held.py -- PHASE 2 controlled: native unit-S^2 degree-k with
the degree HELD by the full angular Dirichlet frame (global-monopole setup), to
(a) confirm a finite-energy degree-k configuration EXISTS and converges, (b) read
the clean ENERGY ORDERING E_k vs k E_1, (c) test the SPLIT instability directly.
2026-06-18.  Claude (Opus 4.8,1M).  DATA-BLIND.  Category-A.  OBSERVE.

WHY HELD: Phase 1 established the pi_2 degree is a BOUNDARY (seal/pole) charge on a
regular finite cell (case ii), not bulk-protected. So "does a degree-k soliton
exist/stable" is the GLOBAL-MONOPOLE question: hold the degree at the boundary and
ask if the interior energy is finite, what shape, and whether higher k binds.
We hold the STANDARD harmonic degree-k map on the WHOLE boundary frame of the
(r,theta) rectangle EXCEPT we leave the SEAL radial end's interior free to test
retraction; the poles carry the polar winding (G=0 at th=0, pi at th=pi).

Convergence: L-BFGS on the exact native energy (better floor than Adam here),
report |grad|.  Energy ordering: E_k vs k E_1.  Split test: seed a "two-lump"
degree-k field (degree concentrated in two theta-caps) and see if E drops below the
single-lump degree-k (=> the charge-k object splits = unbinds).
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK","0")
os.environ.setdefault("PYTORCH_NO_CUDA_MEMORY_CACHING","1")
import math, numpy as np, torch
torch.set_default_dtype(torch.float64)
dev='cuda' if torch.cuda.is_available() else 'cpu'
PI=math.pi

class Cell:
    def __init__(self,Nr=100,Nth=120,rc=0.05,ri=14.0,p=0.0):
        self.Nr,self.Nth,self.rc,self.ri,self.p=Nr,Nth,rc,ri,p
        r=torch.linspace(rc,ri,Nr,device=dev);th=torch.linspace(0,PI,Nth,device=dev)
        self.r,self.th=r,th;self.dr=(ri-rc)/(Nr-1);self.dth=PI/(Nth-1)
        R,TH=torch.meshgrid(r,th,indexing='ij');self.R,self.TH=R,TH
        self.sth=torch.sin(TH).clamp_min(1e-7)
        self.phi=torch.zeros_like(R) if p==0.0 else -p*torch.log(ri/R)
        self.eph=torch.exp(self.phi);self.em2=torch.exp(-2*self.phi);self.e2=torch.exp(2*self.phi)

def grads(G,C):
    Gr=torch.zeros_like(G);Gt=torch.zeros_like(G)
    Gr[1:-1,:]=(G[2:,:]-G[:-2,:])/(2*C.dr);Gr[0,:]=(G[1,:]-G[0,:])/C.dr;Gr[-1,:]=(G[-1,:]-G[-2,:])/C.dr
    Gt[:,1:-1]=(G[:,2:]-G[:,:-2])/(2*C.dth);Gt[:,0]=(G[:,1]-G[:,0])/C.dth;Gt[:,-1]=(G[:,-1]-G[:,-2])/C.dth
    return Gr,Gt

def energy(G,C,k,xi=1.0,kap=1.0):
    Gr,Gt=grads(G,C);sinG2=torch.sin(G)**2
    e2=(xi/2)*(C.em2*Gr**2*C.R**2+Gt**2+k**2*sinG2/C.sth**2)*C.eph*C.sth
    e4=(k**2*kap/2)*sinG2*(C.em2*Gr**2+Gt**2*C.e2/C.R**2)*C.eph*C.sth
    dA=C.dr*C.dth*2*PI
    return (e2.sum()+e4.sum())*dA,e2.sum()*dA,e4.sum()*dA

def realized_degree(G,C,shell,k):
    g=G[shell,:];Gt=torch.zeros(C.Nth,device=dev)
    Gt[1:-1]=(g[2:]-g[:-2])/(2*C.dth);Gt[0]=(g[1]-g[0])/C.dth;Gt[-1]=(g[-1]-g[-2])/C.dth
    return float((torch.sin(g)*Gt).sum()*C.dth*k*(2*PI)/(4*PI))

def hold_frame(G,C,mode='monopole'):
    """Hold the degree at the WHOLE boundary frame (Dirichlet box) with the standard
    degree map G=theta -> global monopole with degree pinned everywhere on bdry.
    Interior fully free.  Poles always 0/pi."""
    G=G.clone()
    G[:,0]=0.0;G[:,-1]=PI                  # poles (polar winding)
    G[0,:]=C.th                            # core r-end: full degree map
    G[-1,:]=C.th                           # seal r-end: full degree map (HELD)
    return G

def minimize_held(C,k,steps=300,xi=1.0,kap=1.0,seed_split=False,verbose=False):
    G0=C.TH.clone()
    if seed_split:
        # concentrate the polar sweep into TWO caps (texture split into 2 lumps in r)
        # G as function of r: sweep 0->pi twice across r? No—degree is angular. Instead
        # perturb interior to break axial symmetry toward splitting: add a localized
        # bump that, if it lowers E, indicates the single lump is unstable to splitting.
        bump=0.6*torch.sin(PI*(C.R-C.rc)/(C.ri-C.rc))*torch.sin(2*C.TH)
        G0=G0+bump
    G=hold_frame(G0,C).clone().requires_grad_(True)
    opt=torch.optim.LBFGS([G],lr=0.5,max_iter=steps,history_size=20,
                          line_search_fn='strong_wolfe',tolerance_grad=1e-10)
    def closure():
        opt.zero_grad();E,_,_=energy(G,C,k,xi,kap);E.backward()
        with torch.no_grad():
            grad=G.grad.clone()
            # project out the held boundary frame from the gradient (Dirichlet)
            grad[:,0]=0;grad[:,-1]=0;grad[0,:]=0;grad[-1,:]=0
            G.grad.copy_(grad)
        return E
    opt.step(closure)
    with torch.no_grad():
        G.data.copy_(hold_frame(G.data,C))
        E,E2,E4=energy(G,C,k,xi,kap)
        gnorm=G.grad.norm().item() if G.grad is not None else float('nan')
        dc=realized_degree(G.data,C,1,k);dm=realized_degree(G.data,C,C.Nr//2,k);ds=realized_degree(G.data,C,C.Nr-2,k)
    return dict(G=G.detach(),E=E.item(),E2=E2.item(),E4=E4.item(),gnorm=gnorm,
                deg_core=dc,deg_mid=dm,deg_seal=ds)

if __name__=="__main__":
    print("="*74);print("PHASE 2 HELD: native unit-S^2 degree-k, degree pinned at boundary frame");print(f"device={dev}");print("="*74)
    for p,tag in [(0.0,'FLAT phi=0'),(0.4,'DEEP-CELL phi=-0.4 ln(ri/r)')]:
        print(f"\n########## background: {tag} ##########")
        for Nth in (120,180):
            C=Cell(Nr=100,Nth=Nth,p=p)
            print(f"  --- grid Nr=100 Nth={Nth} ---")
            E1=None
            for k in (1,2,3):
                res=minimize_held(C,k)
                if k==1:E1=res['E']
                print(f"    k={k}: E={res['E']:.5f} (E2={res['E2']:.4f} E4={res['E4']:.4f}) "
                      f"|grad|={res['gnorm']:.1e} deg(c/m/s)={res['deg_core']:+.2f}/{res['deg_mid']:+.2f}/{res['deg_seal']:+.2f} "
                      f"E/E1={res['E']/E1:6.3f} kE1={k*E1:.4f} {'BINDS' if res['E']<k*E1-1e-6 else 'UNBINDS'}")
    print("\n########## SPLIT instability test (FLAT phi=0, Nth=180) ##########")
    C=Cell(Nr=100,Nth=180,p=0.0)
    for k in (2,3):
        single=minimize_held(C,k,seed_split=False)
        split=minimize_held(C,k,seed_split=True)
        print(f"  k={k}: single-lump E={single['E']:.5f}  split-seed E={split['E']:.5f}  "
              f"{'SPLITS (split lower)' if split['E']<single['E']-1e-4 else 'no split (single lower/equal)'}")
    print("\nDONE_HELD")
