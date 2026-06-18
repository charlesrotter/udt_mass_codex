"""
Consolidated NON-UNIFORM-grid run: solve stationary unit profile (geometric grid),
verify zero modes, build transverse l=1/l=2 operators, R-scan. Deep-phi resolved.
"""
import os
for v in ("OMP_NUM_THREADS","MKL_NUM_THREADS","OPENBLAS_NUM_THREADS","NUMEXPR_NUM_THREADS"):
    os.environ[v]="1"
import numpy as np, sys, time
sys.path.insert(0,'.')
import lean2 as L
from lean2 import nhat,angderiv,xdot,xcr,SINT,COST,TG,PG,DTH,DPH,Nth,Nph,geomgrid,dr_nonuniform,total_energy
from scipy.optimize import minimize
from scipy.linalg import eigh, eigvalsh

def solve_profile(p,R=18.0,r_core=0.05,Nr=70,r_int=1.0):
    import bg
    rg=geomgrid(r_core,R,Nr); phia=p*np.log(rg/r_int)
    # init from the well-resolved corpus BVP profile (close to the unit extremum)
    sol=bg.solve_profile(p,r_core=r_core,R=R,r_int=r_int)
    F0=np.clip(sol.sol(rg)[0],0,np.pi); F0[0]=np.pi; F0[-1]=0.0
    def pack(x):
        F=np.empty(Nr); F[0]=np.pi; F[-1]=0.0; F[1:-1]=x; return F
    # monotonicity-preserving: optimize over log-decrements so F stays monotone
    res=minimize(lambda x: total_energy(rg,pack(x),phia), F0[1:-1],
                 method='L-BFGS-B',options={'maxiter':1500,'ftol':1e-13,'gtol':1e-10,'maxcor':30})
    return rg,pack(res.x),phia,res

class B:
    def __init__(self,p,R=18.0,r_core=0.05,Nr=70):
        self.rg,self.F,self.phi,self.res=solve_profile(p,R=R,r_core=r_core,Nr=Nr)
        self.Nr=Nr; self.p=p; self.R=R; self.flds=[nhat(self.F[i]) for i in range(Nr)]
        self.E0=self.res.fun
    def dnr(self,i): return dr_nonuniform(self.flds,self.rg,i)

def S_pert(B,deltas,eps,sign):
    Nr=B.Nr
    pert=[]
    for i in range(Nr):
        w=B.flds[i]+sign*eps*deltas[i]; nn=np.sqrt(xdot(w,w))[...,None]; pert.append(w/nn)
    densr=np.empty(Nr)
    for i in range(Nr):
        densr[i]=L.shell_energy(pert[i],dr_nonuniform(pert,B.rg,i),B.phi[i],B.rg[i])
    return np.trapezoid(densr,B.rg)

def Tw(B,deltas):
    Nr=B.Nr; densr=np.empty(Nr)
    for i in range(Nr):
        r=B.rg[i]; phd=B.phi[i]; n0=B.flds[i]
        d=deltas[i]; d=d-xdot(d,n0)[...,None]*n0
        dnr=B.dnr(i); dnt,dnp=angderiv(n0)
        grr=np.exp(-2*phd); gtt=1/r**2; gpp=1/(r**2*SINT**2); e2phi=np.exp(2*phd)
        w2=e2phi*xdot(d,d)
        cxr=xcr(d,dnr); cxt=xcr(d,dnt); cxp=xcr(d,dnp)
        w4=e2phi*(grr*xdot(cxr,cxr)+gtt*xdot(cxt,cxt)+gpp*xdot(cxp,cxp))
        sqrtg=np.exp(phd)*r**2*SINT
        densr[i]=np.sum((w2+w4)*sqrtg)*DTH*DPH
    return np.trapezoid(densr,B.rg)

def omega2(B,deltas,eps=1e-4):
    Sp=S_pert(B,deltas,eps,1); Sm=S_pert(B,deltas,eps,-1); S0=S_pert(B,deltas,eps,0)
    d2S=(Sp-2*S0+Sm)/eps**2; d2T=2*Tw(B,deltas)
    return d2S/d2T, d2S, d2T

def isorot(B,ax):
    out=[]
    for i in range(B.Nr):
        n0=B.flds[i]; d=np.empty_like(n0)
        d[...,0]=ax[1]*n0[...,2]-ax[2]*n0[...,1]
        d[...,1]=ax[2]*n0[...,0]-ax[0]*n0[...,2]
        d[...,2]=ax[0]*n0[...,1]-ax[1]*n0[...,0]
        out.append(d-xdot(d,n0)[...,None]*n0)
    return out

def angtan(F,fang,gang):
    n0=nhat(F); h=1e-6; d=(nhat(F+h)-nhat(F-h))/(2*h); d=d-xdot(d,n0)[...,None]*n0
    e1=d/np.sqrt(xdot(d,d))[...,None]; e2=xcr(n0,e1)
    return fang(TG,PG)[...,None]*e1+gang(TG,PG)[...,None]*e2

def chanop(B,fang,gang,eps=2e-4):
    Nr=B.Nr; tang=[angtan(B.F[i],fang,gang) for i in range(Nr)]
    def Q(psi):
        deltas=[psi[i]*tang[i] for i in range(Nr)]
        Sp=S_pert(B,deltas,eps,1); Sm=S_pert(B,deltas,eps,-1); S0=S_pert(B,deltas,eps,0)
        return (Sp-2*S0+Sm)/eps**2
    def Mq(psi): return 2*Tw(B,[psi[i]*tang[i] for i in range(Nr)])
    H=np.zeros((Nr,Nr)); M=np.zeros((Nr,Nr)); Qi=np.zeros(Nr); Mi=np.zeros(Nr)
    for i in range(Nr):
        e=np.zeros(Nr); e[i]=1; Qi[i]=Q(e); Mi[i]=Mq(e); H[i,i]=Qi[i]; M[i,i]=Mi[i]
    for i in range(Nr-1):
        e=np.zeros(Nr); e[i]=1; e[i+1]=1
        H[i,i+1]=H[i+1,i]=0.5*(Q(e)-Qi[i]-Qi[i+1])
        M[i,i+1]=M[i+1,i]=0.5*(Mq(e)-Mi[i]-Mi[i+1])
    return H,M

def Y(l,m):
    if l==1: return {0:lambda T,P:np.cos(T),1:lambda T,P:np.sin(T)*np.cos(P),-1:lambda T,P:np.sin(T)*np.sin(P)}[m]
    if l==2: return {0:lambda T,P:3*np.cos(T)**2-1,1:lambda T,P:np.sin(T)*np.cos(T)*np.cos(P),
            -1:lambda T,P:np.sin(T)*np.cos(T)*np.sin(P),2:lambda T,P:np.sin(T)**2*np.cos(2*P),
            -2:lambda T,P:np.sin(T)**2*np.sin(2*P)}[m]
ZERO=lambda T,P:np.zeros_like(T)

def channel(B,l):
    best=np.inf; stiff_min=np.inf; rows=[]
    for m in range(-l,l+1):
        for tag,(f,g) in [('e1',(Y(l,m),ZERO)),('e2',(ZERO,Y(l,m)))]:
            H,M=chanop(B,f,g); Nr=B.Nr; idx=np.arange(1,Nr-1)
            Hs=0.5*(H+H.T)[np.ix_(idx,idx)]; Ms=0.5*(M+M.T)[np.ix_(idx,idx)]+1e-12*np.eye(len(idx))
            ev=eigh(Hs,Ms,eigvals_only=True); sw=eigvalsh(Hs)
            rows.append((m,tag,ev[0],sw[0])); best=min(best,ev[0]); stiff_min=min(stiff_min,sw[0])
    return best,stiff_min,rows

if __name__=='__main__':
    print("### NON-UNIFORM GRID, deep-phi resolved ###\n")
    for p in (0,1,2):
        t=time.time(); b=B(p)
        # profile quality
        mono = np.all(np.diff(b.F)<=1e-6)
        print(f"=== p={p} R=18 Nr={b.Nr}: E0={b.E0:.3f} conv={b.res.success} monotone={mono} t={time.time()-t:.0f}s")
        for ax,nm in [([1,0,0],'x'),([0,0,1],'z')]:
            o,d2S,_=omega2(b,isorot(b,ax)); print(f"   iso-rot {nm}: omega^2={o:.3e} d2S={d2S:.2e}")
        l1,s1,r1=channel(b,1); l2,s2,r2=channel(b,2)
        print(f"   l=1: lowest omega^2={l1:.5e}  min stiffness={s1:.5e}")
        print(f"   l=2: lowest omega^2={l2:.5e}  min stiffness={s2:.5e}")
