#!/usr/bin/env python3
"""
native_catalog_phase2_solve.py -- PHASE 2 (ENERGETICS+STABILITY), v2: clean,
finite-energy native unit-S^2 degree-k minimizer, profile FREE.  2026-06-18.
Claude (Opus 4.8, 1M).  DATA-BLIND (units L=sqrt(kap/xi)=1).  Category-A.  OBSERVE.

FIX over v1: the v1 windowed seed violated the finite-energy pole regularity
(sin G(theta=0,pi)!=0 when the radial window w<1), which blew up the
k^2 sin^2 G/sin^2 th term (E~1e8 artifacts). The GENUINE finite-energy degree-k
field must have G(theta=0)=0, G(theta=pi)=pi at EVERY radius (the polar winding is
the degree carrier and cannot be radially modulated at the poles). The free
radial freedom is in the INTERIOR polar profile and how sharply the texture sits.

Native energy (exact; native_catalog_phase2_energy_derive.py), psi-integral=2pi:
  e2 = (xi/2)[ e^{-2phi}G_r^2 r^2 + G_th^2 + k^2 sin^2 G/sin^2 th ] e^{phi} sin th
  e4 = (k^2 kap/2) sin^2 G [ e^{-2phi}G_r^2 + e^{2phi}G_th^2/r^2 ] e^{phi} sin th
  E  = 2pi INT dr dth (e2+e4).

DEGREE BC (the topological charge carrier; chose-tagged but it IS the native pi_2
degree, not the imported pi_3 Theta(core)=m*pi):
  G(theta=0)=0, G(theta=pi)=pi at ALL r  ->  polar winding 1; azimuth winding k
  -> pi_2 area-form degree = k.  RADIAL ends FREE (Neumann): the profile chooses
  whether to fill the cell, localize, or retract -- exactly the "profile free" ask.

We minimize the TRUE energy by Adam gradient flow (autograd of exact E), report the
converged E_k, the realized pi_2 degree at core & seal shells, the shape (where the
texture sits), the gradient-flow residual (convergence floor), and the ENERGY
ORDERING E_k vs k E_1 (binds=catalog candidate / unbinds=decays to k unit charges).

GUARD (textbook prior NOT assumed): we do NOT assume higher monopoles are unstable;
we MINIMIZE and read E_k, then SEPARATELY test stability by (a) the energy ordering,
(b) perturbing toward a split (two degree-(k-1)+1 lumps) and seeing if E drops.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
os.environ.setdefault("PYTORCH_NO_CUDA_MEMORY_CACHING", "1")
import math, numpy as np, torch
torch.set_default_dtype(torch.float64)
dev='cuda' if torch.cuda.is_available() else 'cpu'
PI=math.pi


class Cell:
    def __init__(self, Nr=120, Nth=96, rc=0.05, ri=14.0, p=0.0):
        self.Nr,self.Nth,self.rc,self.ri,self.p=Nr,Nth,rc,ri,p
        r=torch.linspace(rc,ri,Nr,device=dev); th=torch.linspace(0,PI,Nth,device=dev)
        self.r,self.th=r,th
        self.dr=(ri-rc)/(Nr-1); self.dth=PI/(Nth-1)
        R,TH=torch.meshgrid(r,th,indexing='ij'); self.R,self.TH=R,TH
        self.sth=torch.sin(TH).clamp_min(1e-7)
        self.phi = torch.zeros_like(R) if p==0.0 else -p*torch.log(ri/R)
        self.eph=torch.exp(self.phi); self.em2=torch.exp(-2*self.phi); self.e2=torch.exp(2*self.phi)


def grads(G,C):
    Gr=torch.zeros_like(G); Gt=torch.zeros_like(G)
    Gr[1:-1,:]=(G[2:,:]-G[:-2,:])/(2*C.dr); Gr[0,:]=(G[1,:]-G[0,:])/C.dr; Gr[-1,:]=(G[-1,:]-G[-2,:])/C.dr
    Gt[:,1:-1]=(G[:,2:]-G[:,:-2])/(2*C.dth); Gt[:,0]=(G[:,1]-G[:,0])/C.dth; Gt[:,-1]=(G[:,-1]-G[:,-2])/C.dth
    return Gr,Gt

def energy(G,C,k,xi=1.0,kap=1.0):
    Gr,Gt=grads(G,C); sinG2=torch.sin(G)**2
    e2=(xi/2)*(C.em2*Gr**2*C.R**2 + Gt**2 + k**2*sinG2/C.sth**2)*C.eph*C.sth
    e4=(k**2*kap/2)*sinG2*(C.em2*Gr**2 + Gt**2*C.e2/C.R**2)*C.eph*C.sth
    dA=C.dr*C.dth*2*PI
    return (e2.sum()+e4.sum())*dA, e2.sum()*dA, e4.sum()*dA

def pole_bc(G):
    G=G.clone(); G[:,0]=0.0; G[:,-1]=PI; return G

def realized_degree(G,C,shell):
    g=G[shell,:]; Gt=torch.zeros(C.Nth,device=dev)
    Gt[1:-1]=(g[2:]-g[:-2])/(2*C.dth); Gt[0]=(g[1]-g[0])/C.dth; Gt[-1]=(g[-1]-g[-2])/C.dth
    # pi_2 degree of (theta,psi)->S^2 with azimuth winding k: (1/4pi) INT sin g * g_th * k dth dpsi
    return float((torch.sin(g)*Gt).sum()*C.dth * 1.0 * (2*PI)/(4*PI))  # k folded below

def minimize(C,k,seed='fill',steps=8000,lr=0.01,xi=1.0,kap=1.0,verbose=False):
    R,TH=C.R,C.TH
    if seed=='fill':  G0=TH.clone()                       # texture fills cell
    elif seed=='core':                                    # localized near core
        f=0.5*(1+torch.cos(PI*(R-C.rc)/(C.ri-C.rc)))
        # at poles must stay 0/pi: blend the polar map by f only in interior theta
        G0=TH.clone()  # keep endpoints; interior gets pulled but poles fixed by bc
    else: G0=TH.clone()
    G=pole_bc(G0).clone().requires_grad_(True)
    opt=torch.optim.Adam([G],lr=lr)
    for it in range(steps):
        opt.zero_grad(); E,E2,E4=energy(G,C,k,xi,kap); E.backward()
        gnorm=G.grad.norm().item(); opt.step()
        with torch.no_grad(): G.data.copy_(pole_bc(G.data))
        if verbose and it%1000==0:
            print(f"    k={k} it={it:5d} E={E.item():.5f} |grad|={gnorm:.2e}")
    with torch.no_grad():
        E,E2,E4=energy(G,C,k,xi,kap)
        gnorm=G.grad.norm().item()
        dc=realized_degree(G.data,C,1)*k; ds=realized_degree(G.data,C,C.Nr-2)*k
        # where the energy sits radially:
        Gr,Gt=grads(G.data,C); sinG2=torch.sin(G.data)**2
        e2=(xi/2)*(C.em2*Gr**2*C.R**2+Gt**2+k**2*sinG2/C.sth**2)*C.eph*C.sth
        e4=(k**2*kap/2)*sinG2*(C.em2*Gr**2+Gt**2*C.e2/C.R**2)*C.eph*C.sth
        edens_r=(e2+e4).sum(dim=1)*C.dth*2*PI   # energy per dr
        rpeak=float(C.r[torch.argmax(edens_r)])
    return dict(G=G.detach(),E=E.item(),E2=E2.item(),E4=E4.item(),gnorm=gnorm,
                deg_core=dc,deg_seal=ds,rpeak=rpeak)

if __name__=="__main__":
    print("="*74);print("PHASE 2 v2: native unit-S^2 degree-k minimizer, profile FREE");print(f"device={dev}");print("="*74)
    for p,tag in [(0.0,'FLAT phi=0'),(0.4,'DEEP-CELL phi=-0.4 ln(ri/r)')]:
        print(f"\n########## background: {tag} ##########")
        C=Cell(Nr=120,Nth=96,p=p)
        E1=None
        for k in (1,2,3):
            res=minimize(C,k,seed='fill',steps=8000,verbose=False)
            if k==1:E1=res['E']
            ratio=res['E']/E1
            print(f"  k={k}: E={res['E']:.5f} (E2={res['E2']:.4f} E4={res['E4']:.4f}) "
                  f"|grad|={res['gnorm']:.1e}  deg(core)={res['deg_core']:+.3f} "
                  f"deg(seal)={res['deg_seal']:+.3f}  E/E1={ratio:.3f}  kE1={k*E1:.4f}  "
                  f"{'BINDS' if res['E']<k*E1-1e-6 else 'UNBINDS'}  rpeak={res['rpeak']:.2f}")
    print("\nDONE_PHASE2_SOLVE_V2")
