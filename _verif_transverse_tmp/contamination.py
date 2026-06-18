"""
Demonstrate the contamination mechanism: on a NON-stationary background the
second-variation stiffness can go negative (spurious), while on the stationary
background it is positive-definite. We take the unit field with a DELIBERATELY
non-extremal profile (e.g. the corpus profile scaled, or a slightly-wrong profile)
and show the l=1 stiffness sign flips, reproducing the prior -0.3-type lead, then
confirm the stationary profile removes it.
We use bg profile but multiply F by a factor c to detune stationarity.
"""
import os
for v in ("OMP_NUM_THREADS","MKL_NUM_THREADS","OPENBLAS_NUM_THREADS","NUMEXPR_NUM_THREADS"):
    os.environ[v]="1"
import numpy as np, sys
sys.path.insert(0,'.')
import bg, lean2 as L
from lean2 import nhat,angderiv,xdot,xcr,SINT,TG,PG,DTH,DPH,geomgrid,dr_nonuniform
from scipy.linalg import eigvalsh

def stiff_l1(Ffunc,p=0,R=18.0,r_core=0.05,Nr=70,r_int=1.0,eps=2e-4):
    rg=geomgrid(r_core,R,Nr); F=Ffunc(rg); phia=p*np.log(rg/r_int)
    flds=[nhat(F[i]) for i in range(Nr)]
    Yf=lambda T,P:np.sin(T)*np.cos(P)
    def angtan(Fv):
        n0=nhat(Fv); h=1e-6; d=(nhat(Fv+h)-nhat(Fv-h))/(2*h); d=d-xdot(d,n0)[...,None]*n0
        return Yf(TG,PG)[...,None]*xcr(n0,d/np.sqrt(xdot(d,d))[...,None])
    tang=[angtan(F[i]) for i in range(Nr)]
    def Spert(psi,sign):
        pert=[(flds[i]+sign*eps*psi[i]*tang[i]) for i in range(Nr)]
        pert=[w/np.sqrt(xdot(w,w))[...,None] for w in pert]
        return np.trapezoid([L.shell_energy(pert[i],dr_nonuniform(pert,rg,i),phia[i],rg[i]) for i in range(Nr)],rg)
    def Q(psi): return (Spert(psi,1)-2*Spert(psi,0)+Spert(psi,-1))/eps**2
    H=np.zeros((Nr,Nr)); Qi=np.zeros(Nr)
    for i in range(Nr):
        e=np.zeros(Nr); e[i]=1; Qi[i]=Q(e); H[i,i]=Qi[i]
    for i in range(Nr-1):
        e=np.zeros(Nr); e[i]=1;e[i+1]=1; H[i,i+1]=H[i+1,i]=0.5*(Q(e)-Qi[i]-Qi[i+1])
    idx=np.arange(1,Nr-1); return eigvalsh(0.5*(H+H.T)[np.ix_(idx,idx)])[0]

if __name__=='__main__':
    sol=bg.solve_profile(0)
    Fbvp=lambda rg: sol.sol(rg)[0]
    print("stationary (BVP) profile        : l=1 min stiffness =", f"{stiff_l1(Fbvp):.4e}")
    for c in (0.7,0.85,1.15,1.3):
        Fc=lambda rg,c=c: np.clip(c*sol.sol(rg)[0],0,np.pi)
        print(f"detuned profile F*{c:<4}        : l=1 min stiffness =", f"{stiff_l1(Fc):.4e}")
