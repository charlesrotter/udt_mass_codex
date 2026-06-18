"""Angular-resolution convergence of the l=1 stiffness sign on the BVP profile, p=0.
Confirms the positive stiffness isn't a coarse-grid artifact. Re-imports lean2 with
overridden Nth,Nph by monkey-patching is messy; instead reimplement minimal stiffness
on a parametric (Nth,Nph)."""
import os
for v in ("OMP_NUM_THREADS","MKL_NUM_THREADS","OPENBLAS_NUM_THREADS","NUMEXPR_NUM_THREADS"):
    os.environ[v]="1"
import numpy as np, sys
sys.path.insert(0,'.')
import bg
from scipy.linalg import eigvalsh

def run(Nth,Nph,p=0,R=18.0,r_core=0.05,Nr=70,r_int=1.0,l=1,m=1,eps=2e-4):
    TH=np.linspace(1e-3,np.pi-1e-3,Nth); DTH=TH[1]-TH[0]
    PH=np.linspace(0,2*np.pi,Nph,endpoint=False); DPH=2*np.pi/Nph
    TG,PG=np.meshgrid(TH,PH,indexing='ij'); SINT=np.sin(TG); COSP=np.cos(PG); SINP=np.sin(PG)
    def nhat(F):
        a=np.sin(F)*SINT*COSP; b=np.sin(F)*SINT*SINP; c=np.cos(F)*np.ones_like(SINT)
        nr=np.sqrt(a*a+b*b+c*c); n=np.empty((Nth,Nph,3)); n[...,0]=a/nr;n[...,1]=b/nr;n[...,2]=c/nr; return n
    def xdot(a,b): return a[...,0]*b[...,0]+a[...,1]*b[...,1]+a[...,2]*b[...,2]
    def xcr(a,b):
        c=np.empty_like(a); c[...,0]=a[...,1]*b[...,2]-a[...,2]*b[...,1]
        c[...,1]=a[...,2]*b[...,0]-a[...,0]*b[...,2]; c[...,2]=a[...,0]*b[...,1]-a[...,1]*b[...,0]; return c
    def angderiv(arr):
        dt=np.empty_like(arr); dt[1:-1]=(arr[2:]-arr[:-2])/(2*DTH); dt[0]=(arr[1]-arr[0])/DTH; dt[-1]=(arr[-1]-arr[-2])/DTH
        dp=(np.roll(arr,-1,axis=1)-np.roll(arr,1,axis=1))/(2*DPH); return dt,dp
    sol=bg.solve_profile(p,r_core=r_core,R=R,r_int=r_int)
    rg=np.geomspace(r_core,r_core+R,Nr); F=sol.sol(rg)[0]; phia=p*np.log(rg/r_int)
    flds=[nhat(F[i]) for i in range(Nr)]
    Yf=(lambda T,P:np.sin(T)*np.cos(P)) if l==1 else (lambda T,P:np.sin(T)*np.cos(T)*np.cos(P))
    def angtan(Fv):
        n0=nhat(Fv); h=1e-6; d=(nhat(Fv+h)-nhat(Fv-h))/(2*h); d=d-xdot(d,n0)[...,None]*n0
        e2=xcr(n0,d/np.sqrt(xdot(d,d))[...,None]); return Yf(TG,PG)[...,None]*e2
    tang=[angtan(F[i]) for i in range(Nr)]
    def drn(fl,i):
        if i==0: return (fl[1]-fl[0])/(rg[1]-rg[0])
        if i==Nr-1: return (fl[-1]-fl[-2])/(rg[-1]-rg[-2])
        h1=rg[i]-rg[i-1]; h2=rg[i+1]-rg[i]; return (fl[i+1]*h1**2-fl[i-1]*h2**2+fl[i]*(h2**2-h1**2))/(h1*h2*(h1+h2))
    def shellE(fld,dnr,phd,r):
        dnt,dnp=angderiv(fld); grr=np.exp(-2*phd); gtt=1/r**2; gpp=1/(r**2*SINT**2)
        e2=0.5*(grr*xdot(dnr,dnr)+gtt*xdot(dnt,dnt)+gpp*xdot(dnp,dnp))
        Srt=xcr(dnr,dnt);Srp=xcr(dnr,dnp);Stp=xcr(dnt,dnp)
        e4=0.25*2*(grr*gtt*xdot(Srt,Srt)+grr*gpp*xdot(Srp,Srp)+gtt*gpp*xdot(Stp,Stp))
        return np.sum((e2+e4)*np.exp(phd)*r**2*SINT)*DTH*DPH
    def Spert(psi,sign):
        pert=[(flds[i]+sign*eps*psi[i]*tang[i]) for i in range(Nr)]
        pert=[w/np.sqrt(xdot(w,w))[...,None] for w in pert]
        return np.trapezoid([shellE(pert[i],drn(pert,i),phia[i],rg[i]) for i in range(Nr)],rg)
    def Q(psi): return (Spert(psi,1)-2*Spert(psi,0)+Spert(psi,-1))/eps**2
    H=np.zeros((Nr,Nr)); Qi=np.zeros(Nr)
    for i in range(Nr):
        e=np.zeros(Nr); e[i]=1; Qi[i]=Q(e); H[i,i]=Qi[i]
    for i in range(Nr-1):
        e=np.zeros(Nr); e[i]=1;e[i+1]=1; H[i,i+1]=H[i+1,i]=0.5*(Q(e)-Qi[i]-Qi[i+1])
    idx=np.arange(1,Nr-1); return eigvalsh(0.5*(H+H.T)[np.ix_(idx,idx)])[0]

if __name__=='__main__':
    for (Nth,Nph) in [(48,8),(64,12),(96,16),(128,24)]:
        s=run(Nth,Nph)
        print(f"Nth={Nth} Nph={Nph}: l=1 min stiffness eigenvalue = {s:.5e}")
