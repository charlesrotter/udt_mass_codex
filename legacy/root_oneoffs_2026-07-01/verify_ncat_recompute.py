#!/usr/bin/env python3
"""verify_ncat_recompute.py -- recompute E_k/E_1 with CORRECTED L4 (the I4 from the
exact derive script) vs the solver's buggy e4. Held-degree global-monopole frame,
matching phase2_held.py setup. Adversarial verifier (Opus). DATA-BLIND."""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK","0")
os.environ.setdefault("PYTORCH_NO_CUDA_MEMORY_CACHING","1")
import math, torch
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

def energy(G,C,k,mode,xi=1.0,kap=1.0):
    Gr,Gt=grads(G,C);sinG2=torch.sin(G)**2
    # L2 (same for both; correct):
    e2=(xi/2)*(C.em2*Gr**2*C.R**2+Gt**2+k**2*sinG2/C.sth**2)*C.eph*C.sth
    if mode=='buggy':
        e4=(k**2*kap/2)*sinG2*(C.em2*Gr**2+Gt**2*C.e2/C.R**2)*C.eph*C.sth
    elif mode=='correct':
        # I4 = Gr^2 k^2 kap e^{-phi} sin^2G/(2 sinth) + Gt^2 k^2 kap e^{phi} sin^2G/(2 r^2 sinth)
        e4=(k**2*kap/2)*sinG2*(C.em2*Gr**2*C.R**2+Gt**2*C.e2)*C.eph/(C.R**2*C.sth)
    dA=C.dr*C.dth*2*PI
    return (e2.sum()+e4.sum())*dA,e2.sum()*dA,e4.sum()*dA

def hold_frame(G,C):
    G=G.clone();G[:,0]=0.0;G[:,-1]=PI;G[0,:]=C.th;G[-1,:]=C.th;return G

def minimize_held(C,k,mode,steps=400,xi=1.0,kap=1.0):
    G0=C.TH.clone()
    G=hold_frame(G0,C).clone().requires_grad_(True)
    opt=torch.optim.LBFGS([G],lr=0.5,max_iter=steps,history_size=20,
                          line_search_fn='strong_wolfe',tolerance_grad=1e-10)
    def closure():
        opt.zero_grad();E,_,_=energy(G,C,k,mode,xi,kap);E.backward()
        with torch.no_grad():
            grad=G.grad.clone();grad[:,0]=0;grad[:,-1]=0;grad[0,:]=0;grad[-1,:]=0
            G.grad.copy_(grad)
        return E
    opt.step(closure)
    with torch.no_grad():
        G.data.copy_(hold_frame(G.data,C))
        E,E2,E4=energy(G,C,k,mode,xi,kap)
        gn=G.grad.norm().item() if G.grad is not None else float('nan')
    return E.item(),E2.item(),E4.item(),gn

if __name__=="__main__":
    print("RECOMPUTE E_k/E_1: buggy-solver vs corrected-L4");print(f"device={dev}")
    for p,tag in [(0.4,'DEEP-CELL p=0.4'),(0.0,'FLAT p=0')]:
        print(f"\n##### {tag} #####")
        for mode in ('buggy','correct'):
            print(f"  mode={mode}")
            for Nth in (120,160,220):
                C=Cell(Nr=100,Nth=Nth,p=p)
                E1=None;row=[]
                for k in (1,2,3):
                    E,E2,E4,gn=minimize_held(C,k,mode)
                    if k==1:E1=E
                    row.append((k,E/E1,E,gn))
                s=" ".join(f"E{k}/E1={rt:6.3f}" for k,rt,E,gn in row)
                gmax=max(gn for *_,gn in row)
                print(f"    Nth={Nth}: {s}  (|grad|max={gmax:.1e})")
