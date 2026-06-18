"""
Fast self-consistent UNIT-field soliton via full vectorization (r,th,ph all at once),
minimizing the exact discretized 3D (L2+L4) energy. Returns stationary profile F(r).
"""
import os
for v in ("OMP_NUM_THREADS","MKL_NUM_THREADS","OPENBLAS_NUM_THREADS","NUMEXPR_NUM_THREADS"):
    os.environ[v]="1"
import numpy as np
from scipy.optimize import minimize

def xprod(a,b):
    # cross product of (...,3) arrays without np.cross (avoids big-array alloc bug)
    return np.stack([a[...,1]*b[...,2]-a[...,2]*b[...,1],
                     a[...,2]*b[...,0]-a[...,0]*b[...,2],
                     a[...,0]*b[...,1]-a[...,1]*b[...,0]],axis=-1)

class UnitEnergy:
    def __init__(self,p,R=18.0,r_core=0.05,Nr=80,Nth=80,Nph=16,r_int=1.0):
        self.p=p; self.r_int=r_int
        self.r=np.linspace(r_core,r_core+R,Nr); self.dr=self.r[1]-self.r[0]; self.Nr=Nr
        th=np.linspace(1e-3,np.pi-1e-3,Nth); self.dth=th[1]-th[0]; self.Nth=Nth
        ph=np.linspace(0,2*np.pi,Nph,endpoint=False); self.dph=2*np.pi/Nph; self.Nph=Nph
        TH,PH=np.meshgrid(th,ph,indexing='ij')
        self.sinth=TH*0+np.sin(TH); self.cosP=np.cos(PH); self.sinP=np.sin(PH)
        # broadcast shapes: (Nr,Nth,Nph)
        self.SINTH=self.sinth[None]; self.COSP=self.cosP[None]; self.SINP=self.sinP[None]
        self.phi=(p*np.log(self.r/r_int))[:,None,None]
        self.rr=self.r[:,None,None]
        self.r_core=r_core; self.R=R
    def nhat(self,F):
        # F shape (Nr,) -> broadcast
        Fb=F[:,None,None]
        a=np.sin(Fb)*self.SINTH*self.COSP; b=np.sin(Fb)*self.SINTH*self.SINP
        c=np.cos(Fb)*np.ones_like(self.SINTH)
        v=np.stack([a,b,c],axis=-1)  # (Nr,Nth,Nph,3)
        return v/np.linalg.norm(v,axis=-1,keepdims=True)
    def energy(self,F):
        fld=self.nhat(F)  # (Nr,Nth,Nph,3)
        # dn/dr
        dnr=np.empty_like(fld)
        dnr[1:-1]=(fld[2:]-fld[:-2])/(2*self.dr); dnr[0]=(fld[1]-fld[0])/self.dr; dnr[-1]=(fld[-1]-fld[-2])/self.dr
        # dn/dth (axis1)
        dnt=np.empty_like(fld)
        dnt[:,1:-1]=(fld[:,2:]-fld[:,:-2])/(2*self.dth); dnt[:,0]=(fld[:,1]-fld[:,0])/self.dth; dnt[:,-1]=(fld[:,-1]-fld[:,-2])/self.dth
        # dn/dph (axis2 periodic)
        dnp=(np.roll(fld,-1,axis=2)-np.roll(fld,1,axis=2))/(2*self.dph)
        grr=np.exp(-2*self.phi); gtt=1/self.rr**2; gpp=1/(self.rr**2*self.SINTH**2)
        g2=grr*np.sum(dnr*dnr,-1)+gtt*np.sum(dnt*dnt,-1)+gpp*np.sum(dnp*dnp,-1)
        e2=0.5*g2
        Srt=xprod(dnr,dnt); Srp=xprod(dnr,dnp); Stp=xprod(dnt,dnp)
        L4s=2*(grr*gtt*np.sum(Srt*Srt,-1)+grr*gpp*np.sum(Srp*Srp,-1)+gtt*gpp*np.sum(Stp*Stp,-1))
        e4=0.25*L4s
        sqrtg=np.exp(self.phi)*self.rr**2*self.SINTH
        densr=np.sum((e2+e4)*sqrtg,axis=(1,2))*self.dth*self.dph
        return np.trapezoid(densr,self.r)

def solve(p,**kw):
    U=UnitEnergy(p,**kw)
    F0=np.pi*np.exp(-(U.r-U.r_core)/max(0.3,2.0/(1+p))); F0[-1]=0
    def pack(x):
        F=np.empty(U.Nr); F[0]=np.pi; F[-1]=0.0; F[1:-1]=x; return F
    obj=lambda x: U.energy(pack(x))
    res=minimize(obj,F0[1:-1],method='L-BFGS-B',options={'maxiter':600,'ftol':1e-11,'gtol':1e-8})
    return U,pack(res.x),res

if __name__=='__main__':
    import time
    for p in (0,1,2):
        t=time.time(); U,F,res=solve(p,Nr=80,Nth=80,Nph=16)
        print(f"p={p}: E0={res.fun:.4f} conv={res.success} nit={res.nit} t={time.time()-t:.1f}s")
        np.save(f'unitprof_p{p}.npy',np.vstack([U.r,F]))
