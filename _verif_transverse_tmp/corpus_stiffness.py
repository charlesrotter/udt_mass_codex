"""
Decisive cross-check: stiffness (second-variation) sign on the WELL-RESOLVED corpus
BVP profile (bg.solve_bvp -> the E0~50,52 deep-phi solitons), with background field =
normalize(candidate-A). Stability = sign of the stiffness quadratic form H (independent
of the time-kinetic weight). If H is positive-definite for l=1,l=2 at all p, there is
no unstable transverse direction -- regardless of background-stationarity subtleties,
because a negative omega^2 REQUIRES a negative stiffness direction.

We also report the lowest GENERALIZED eigenvalue (vs the weight) for completeness.
Resolution: BVP profile sampled on a geometric grid with Nr nodes; deep phi resolved.
"""
import os
for v in ("OMP_NUM_THREADS","MKL_NUM_THREADS","OPENBLAS_NUM_THREADS","NUMEXPR_NUM_THREADS"):
    os.environ[v]="1"
import numpy as np, sys, time
sys.path.insert(0,'.')
import bg, lean2 as L
from lean2 import nhat,angderiv,xdot,xcr,SINT,COST,TG,PG,DTH,DPH,geomgrid,dr_nonuniform
from scipy.linalg import eigh, eigvalsh

class Bc:
    def __init__(self,p,R=18.0,r_core=0.05,Nr=90,r_int=1.0):
        sol=bg.solve_profile(p,r_core=r_core,R=R,r_int=r_int)
        self.rg=geomgrid(r_core,R,Nr); self.Nr=Nr; self.p=p; self.R=R
        self.F=sol.sol(self.rg)[0]; self.phi=p*np.log(self.rg/r_int)
        self.flds=[nhat(self.F[i]) for i in range(Nr)]
        self.success=sol.success
    def dnr(self,i): return dr_nonuniform(self.flds,self.rg,i)

def S_pert(Bo,deltas,eps,sign):
    Nr=Bo.Nr; pert=[]
    for i in range(Nr):
        w=Bo.flds[i]+sign*eps*deltas[i]; pert.append(w/np.sqrt(xdot(w,w))[...,None])
    densr=np.array([L.shell_energy(pert[i],dr_nonuniform(pert,Bo.rg,i),Bo.phi[i],Bo.rg[i]) for i in range(Nr)])
    return np.trapezoid(densr,Bo.rg)

def Tw(Bo,deltas):
    Nr=Bo.Nr; densr=np.empty(Nr)
    for i in range(Nr):
        r=Bo.rg[i]; phd=Bo.phi[i]; n0=Bo.flds[i]; d=deltas[i]; d=d-xdot(d,n0)[...,None]*n0
        dnr=Bo.dnr(i); dnt,dnp=angderiv(n0)
        grr=np.exp(-2*phd); gtt=1/r**2; gpp=1/(r**2*SINT**2); e2phi=np.exp(2*phd)
        w2=e2phi*xdot(d,d); cxr=xcr(d,dnr); cxt=xcr(d,dnt); cxp=xcr(d,dnp)
        w4=e2phi*(grr*xdot(cxr,cxr)+gtt*xdot(cxt,cxt)+gpp*xdot(cxp,cxp))
        densr[i]=np.sum((w2+w4)*np.exp(phd)*r**2*SINT)*DTH*DPH
    return np.trapezoid(densr,Bo.rg)

def angtan(F,fang,gang):
    n0=nhat(F); h=1e-6; d=(nhat(F+h)-nhat(F-h))/(2*h); d=d-xdot(d,n0)[...,None]*n0
    e1=d/np.sqrt(xdot(d,d))[...,None]; e2=xcr(n0,e1)
    return fang(TG,PG)[...,None]*e1+gang(TG,PG)[...,None]*e2

def chanop(Bo,fang,gang,eps=2e-4):
    Nr=Bo.Nr; tang=[angtan(Bo.F[i],fang,gang) for i in range(Nr)]
    def Q(psi):
        d=[psi[i]*tang[i] for i in range(Nr)]
        return (S_pert(Bo,d,eps,1)-2*S_pert(Bo,d,eps,0)+S_pert(Bo,d,eps,-1))/eps**2
    def Mq(psi): return 2*Tw(Bo,[psi[i]*tang[i] for i in range(Nr)])
    H=np.zeros((Nr,Nr)); M=np.zeros((Nr,Nr)); Qi=np.zeros(Nr); Mi=np.zeros(Nr)
    for i in range(Nr):
        e=np.zeros(Nr); e[i]=1; Qi[i]=Q(e); Mi[i]=Mq(e); H[i,i]=Qi[i]; M[i,i]=Mi[i]
    for i in range(Nr-1):
        e=np.zeros(Nr); e[i]=1; e[i+1]=1
        H[i,i+1]=H[i+1,i]=0.5*(Q(e)-Qi[i]-Qi[i+1]); M[i,i+1]=M[i+1,i]=0.5*(Mq(e)-Mi[i]-Mi[i+1])
    return H,M

def Y(l,m):
    if l==1: return {0:lambda T,P:np.cos(T),1:lambda T,P:np.sin(T)*np.cos(P),-1:lambda T,P:np.sin(T)*np.sin(P)}[m]
    if l==2: return {0:lambda T,P:3*np.cos(T)**2-1,1:lambda T,P:np.sin(T)*np.cos(T)*np.cos(P),
            -1:lambda T,P:np.sin(T)*np.cos(T)*np.sin(P),2:lambda T,P:np.sin(T)**2*np.cos(2*P),
            -2:lambda T,P:np.sin(T)**2*np.sin(2*P)}[m]
ZERO=lambda T,P:np.zeros_like(T)

def channel(Bo,l):
    best=np.inf; smin=np.inf; rows=[]
    for m in range(-l,l+1):
        for tag,(f,g) in [('e1',(Y(l,m),ZERO)),('e2',(ZERO,Y(l,m)))]:
            H,M=chanop(Bo,f,g); Nr=Bo.Nr; idx=np.arange(1,Nr-1)
            Hs=0.5*(H+H.T)[np.ix_(idx,idx)]; Ms=0.5*(M+M.T)[np.ix_(idx,idx)]+1e-12*np.eye(len(idx))
            gev=eigh(Hs,Ms,eigvals_only=True); sw=eigvalsh(Hs)
            rows.append((m,tag,gev[0],sw[0])); best=min(best,gev[0]); smin=min(smin,sw[0])
    return best,smin,rows

if __name__=='__main__':
    print("### CORPUS BVP profile (well-resolved), normalize(A) background ###")
    for p in (0,1,2):
        t=time.time(); b=Bc(p)
        mono=np.all(np.diff(b.F)<=1e-3)
        l1,s1,_=channel(b,1); l2,s2,_=channel(b,2)
        verdict="POS-DEF (stable)" if min(s1,s2)>0 else "NEG (UNSTABLE)"
        print(f"p={p}: bvp_ok={b.success} monotone={mono} | "
              f"l=1 stiff_min={s1:.4e} l=2 stiff_min={s2:.4e} -> {verdict}")
        print(f"      l=1 lowest weighted omega^2={l1:.4e}  l=2={l2:.4e}  (t={time.time()-t:.0f}s)")
