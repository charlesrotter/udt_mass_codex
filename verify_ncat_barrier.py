#!/usr/bin/env python3
"""verify_ncat_barrier.py -- AXIS B (load-bearing): energy along degree-1 -> degree-0
unwinding. Uses CORRECTED L4. Two settings:
 (1) seal degree FREE (radial Neumann): does the cell spontaneously shed degree-1
     (energy monotone down to vacuum => BC-held, no barrier)?
 (2) seal degree HELD at 1, interior unwinds via global retraction param s: trace E(s)
     to see if a metastable minimum (barrier) exists at finite degree.
Also: relax from degree-1 free seed and watch the realized degree + energy."""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK","0")
import math, torch
torch.set_default_dtype(torch.float64)
dev='cuda' if torch.cuda.is_available() else 'cpu'
PI=math.pi

class Cell:
    def __init__(self,Nr=100,Nth=140,rc=0.05,ri=14.0,p=0.4):
        r=torch.linspace(rc,ri,Nr,device=dev);th=torch.linspace(0,PI,Nth,device=dev)
        self.Nr,self.Nth,self.rc,self.ri=Nr,Nth,rc,ri
        self.r,self.th=r,th;self.dr=(ri-rc)/(Nr-1);self.dth=PI/(Nth-1)
        R,TH=torch.meshgrid(r,th,indexing='ij');self.R,self.TH=R,TH
        self.sth=torch.sin(TH).clamp_min(1e-7)
        self.phi=torch.zeros_like(R) if p==0 else -p*torch.log(ri/R)
        self.eph=torch.exp(self.phi);self.em2=torch.exp(-2*self.phi);self.e2=torch.exp(2*self.phi)

def grads(G,C):
    Gr=torch.zeros_like(G);Gt=torch.zeros_like(G)
    Gr[1:-1,:]=(G[2:,:]-G[:-2,:])/(2*C.dr);Gr[0,:]=(G[1,:]-G[0,:])/C.dr;Gr[-1,:]=(G[-1,:]-G[-2,:])/C.dr
    Gt[:,1:-1]=(G[:,2:]-G[:,:-2])/(2*C.dth);Gt[:,0]=(G[:,1]-G[:,0])/C.dth;Gt[:,-1]=(G[:,-1]-G[:,-2])/C.dth
    return Gr,Gt

def energy(G,C,k=1,xi=1.,kap=1.):
    Gr,Gt=grads(G,C);sg2=torch.sin(G)**2
    e2=(xi/2)*(C.em2*Gr**2*C.R**2+Gt**2+k**2*sg2/C.sth**2)*C.eph*C.sth
    e4=(k**2*kap/2)*sg2*(C.em2*Gr**2*C.R**2+Gt**2*C.e2)*C.eph/(C.R**2*C.sth)  # CORRECTED
    dA=C.dr*C.dth*2*PI
    return (e2.sum()+e4.sum())*dA

def realized_deg(G,C,shell,k=1):
    g=G[shell,:];Gt=torch.zeros(C.Nth,device=dev)
    Gt[1:-1]=(g[2:]-g[:-2])/(2*C.dth);Gt[0]=(g[1]-g[0])/C.dth;Gt[-1]=(g[-1]-g[-2])/C.dth
    return float((torch.sin(g)*Gt).sum()*C.dth*k*(2*PI)/(4*PI))

C=Cell()
# (2) BARRIER scan: parametrize field by global retraction s in [0,1]: G = s*theta
#     (s=1 full degree-1, s=0 vacuum north pole). Poles: at s<1, G(pi)=s*pi != pi,
#     so sinG(pole)!=0 -> the k^2 sin^2G/sin^2th pole term. Evaluate E(s).
print("[B-2] Energy along GLOBAL retraction G=s*theta (s:1->0), seal NOT held, deep-cell:")
print("   s     E(s)      deg(seal)")
for s in [1.0,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,0.0]:
    G=s*C.TH
    E=energy(G,C).item();dg=realized_deg(G,C,C.Nr-2)
    print(f"  {s:.2f}  {E:9.4f}   {dg:+.3f}")

# (1) FREE relax from degree-1 seed, ALL radial ends Neumann (only poles fixed 0/pi):
print("\n[B-1] FREE relax (poles fixed 0/pi; radial ends FREE) from degree-1 seed:")
def pole_only(G):
    G=G.clone();G[:,0]=0.0;G[:,-1]=PI;return G
G=pole_only(C.TH.clone()).requires_grad_(True)
opt=torch.optim.Adam([G],lr=0.01)
for it in range(6000):
    opt.zero_grad();E=energy(G,C);E.backward();opt.step()
    with torch.no_grad():G.data.copy_(pole_only(G.data))
with torch.no_grad():
    print(f"   final E={energy(G,C).item():.4f}  deg(core)={realized_deg(G.data,C,1):+.3f}  deg(seal)={realized_deg(G.data,C,C.Nr-2):+.3f}")
    print("   (poles fixed forces a polar winding at every r -> degree stays ~1 even with radial free;")
    print("    the polar BC G(0)=0,G(pi)=pi IS the degree carrier.)")

# (1b) TRULY free: release the poles too (clamp only |n|=1 implicitly via G real). 
print("\n[B-1b] FULLY free (NO pole BC, NO radial BC) from degree-1 seed:")
G=C.TH.clone().requires_grad_(True)
opt=torch.optim.Adam([G],lr=0.01)
for it in range(8000):
    opt.zero_grad();E=energy(G,C);E.backward();opt.step()
with torch.no_grad():
    print(f"   final E={energy(G,C).item():.4f}  deg(core)={realized_deg(G.data,C,1):+.3f}  deg(seal)={realized_deg(G.data,C,C.Nr-2):+.3f}")
    print(f"   G range: [{G.data.min().item():.3f},{G.data.max().item():.3f}]  (->0 everywhere means unwound to vacuum)")
