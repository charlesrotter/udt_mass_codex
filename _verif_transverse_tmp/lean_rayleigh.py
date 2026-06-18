import os
for v in ("OMP_NUM_THREADS","MKL_NUM_THREADS","OPENBLAS_NUM_THREADS","NUMEXPR_NUM_THREADS"):
    os.environ[v]="1"
import numpy as np, sys
sys.path.insert(0,'.')
import lean
from lean import nhat,dn_dF,angderiv,xdot,xcr,SINT,COST,DTH,DPH,Nth,Nph,TG,PG

class BG:
    def __init__(self,p):
        d=np.load(f'leanprof_p{p}.npy'); self.r=d[0]; self.F=d[1]; self.phi=d[2]
        self.Nr=len(self.r); self.dr=self.r[1]-self.r[0]; self.p=p
        self.flds=[nhat(self.F[i]) for i in range(self.Nr)]
    def dnr_bg(self,i):
        if i==0: return (self.flds[1]-self.flds[0])/self.dr
        if i==self.Nr-1: return (self.flds[-1]-self.flds[-2])/self.dr
        return (self.flds[i+1]-self.flds[i-1])/(2*self.dr)

def S_total(BGo, deltas, eps, sign):
    """energy of normalize(n0+sign*eps*delta) summed over shells."""
    Nr=BGo.Nr; dr=BGo.dr
    pert=[]
    for i in range(Nr):
        w=BGo.flds[i]+sign*eps*deltas[i]
        nn=np.sqrt(xdot(w,w))[...,None]
        pert.append(w/nn)
    densr=np.empty(Nr)
    for i in range(Nr):
        if i==0: dnr=(pert[1]-pert[0])/dr
        elif i==Nr-1: dnr=(pert[-1]-pert[-2])/dr
        else: dnr=(pert[i+1]-pert[i-1])/(2*dr)
        densr[i]=lean.energy_density_shell(pert[i],dnr,BGo.phi[i],BGo.r[i])
    return np.trapezoid(densr,BGo.r)

def Tweight(BGo, deltas):
    """time-kinetic weight (coeff of (1/2) epsdot^2). delta projected tangent."""
    Nr=BGo.Nr; densr=np.empty(Nr)
    for i in range(Nr):
        r=BGo.r[i]; phd=BGo.phi[i]; n0=BGo.flds[i]
        d=deltas[i]; d=d-xdot(d,n0)[...,None]*n0
        dnr=BGo.dnr_bg(i); dnt,dnp=angderiv(n0)
        grr=np.exp(-2*phd); gtt=1/r**2; gpp=1/(r**2*SINT**2); e2phi=np.exp(2*phd)
        w2=e2phi*xdot(d,d)
        cxr=xcr(d,dnr); cxt=xcr(d,dnt); cxp=xcr(d,dnp)
        w4=e2phi*(grr*xdot(cxr,cxr)+gtt*xdot(cxt,cxt)+gpp*xdot(cxp,cxp))
        sqrtg=np.exp(phd)*r**2*SINT
        densr[i]=np.sum((w2+w4)*sqrtg)*DTH*DPH
    return np.trapezoid(densr,BGo.r)

def omega2(BGo, deltas, eps=1e-4):
    Sp=S_total(BGo,deltas,eps,+1); Sm=S_total(BGo,deltas,eps,-1); S0=S_total(BGo,deltas,eps,0)
    d2S=(Sp-2*S0+Sm)/eps**2
    d2T=2*Tweight(BGo,deltas)
    return d2S/d2T, d2S, d2T

# ---- analytic symmetry modes ----
def mode_translation_z(BGo):
    out=[]
    for i in range(BGo.Nr):
        r=BGo.r[i]; n0=BGo.flds[i]; dnr=BGo.dnr_bg(i); dnt,_=angderiv(n0)
        dz=COST[...,None]*dnr-(SINT[...,None]/r)*dnt
        d=-dz; d=d-xdot(d,n0)[...,None]*n0
        out.append(d)
    return out

def mode_isorot_z(BGo):
    z=np.array([0,0,1.0]); out=[]
    for i in range(BGo.Nr):
        n0=BGo.flds[i]
        d=np.empty_like(n0)
        d[...,0]=z[1]*n0[...,2]-z[2]*n0[...,1]
        d[...,1]=z[2]*n0[...,0]-z[0]*n0[...,2]
        d[...,2]=z[0]*n0[...,1]-z[1]*n0[...,0]
        d=d-xdot(d,n0)[...,None]*n0
        out.append(d)
    return out

if __name__=='__main__':
    for p in (0,1,2):
        B=BG(p)
        o_t,d2S_t,d2T_t=omega2(B,mode_translation_z(B))
        o_i,d2S_i,d2T_i=omega2(B,mode_isorot_z(B))
        print(f"p={p}: translation omega^2={o_t:.5f} (d2S={d2S_t:.3f},d2T={d2T_t:.3f}) | "
              f"isorot omega^2={o_i:.5f} (d2S={d2S_i:.3f})")
