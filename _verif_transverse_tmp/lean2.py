"""
Lean core v2: NON-UNIFORM radial grid (geometric near core) for deep-phi resolution.
Same angular machinery; radial derivatives & integration use the actual node spacing.
Low memory (2D angular arrays only).
"""
import os
for v in ("OMP_NUM_THREADS","MKL_NUM_THREADS","OPENBLAS_NUM_THREADS","NUMEXPR_NUM_THREADS"):
    os.environ[v]="1"
import numpy as np

Nth=64; Nph=12
TH=np.linspace(1e-3,np.pi-1e-3,Nth); DTH=TH[1]-TH[0]
PH=np.linspace(0,2*np.pi,Nph,endpoint=False); DPH=2*np.pi/Nph
TG,PG=np.meshgrid(TH,PH,indexing='ij')
SINT=np.sin(TG); COST=np.cos(TG); COSP=np.cos(PG); SINP=np.sin(PG)

def nhat(F):
    a=np.sin(F)*SINT*COSP; b=np.sin(F)*SINT*SINP; c=np.cos(F)*np.ones_like(SINT)
    norm=np.sqrt(a*a+b*b+c*c)
    n=np.empty((Nth,Nph,3)); n[...,0]=a/norm; n[...,1]=b/norm; n[...,2]=c/norm
    return n
def angderiv(arr):
    dt=np.empty_like(arr)
    dt[1:-1]=(arr[2:]-arr[:-2])/(2*DTH); dt[0]=(arr[1]-arr[0])/DTH; dt[-1]=(arr[-1]-arr[-2])/DTH
    dp=(np.roll(arr,-1,axis=1)-np.roll(arr,1,axis=1))/(2*DPH)
    return dt,dp
def xdot(a,b): return a[...,0]*b[...,0]+a[...,1]*b[...,1]+a[...,2]*b[...,2]
def xcr(a,b):
    c=np.empty_like(a)
    c[...,0]=a[...,1]*b[...,2]-a[...,2]*b[...,1]
    c[...,1]=a[...,2]*b[...,0]-a[...,0]*b[...,2]
    c[...,2]=a[...,0]*b[...,1]-a[...,1]*b[...,0]
    return c

def geomgrid(r_core,R,Nr):
    return np.geomspace(r_core, r_core+R, Nr)

def dr_nonuniform(flds,rg,i):
    Nr=len(rg)
    if i==0: return (flds[1]-flds[0])/(rg[1]-rg[0])
    if i==Nr-1: return (flds[-1]-flds[-2])/(rg[-1]-rg[-2])
    # central, non-uniform
    h1=rg[i]-rg[i-1]; h2=rg[i+1]-rg[i]
    return (flds[i+1]*h1**2 - flds[i-1]*h2**2 + flds[i]*(h2**2-h1**2))/(h1*h2*(h1+h2))

def shell_energy(fld,dnr,phd,r):
    dnt,dnp=angderiv(fld)
    grr=np.exp(-2*phd); gtt=1/r**2; gpp=1/(r**2*SINT**2)
    g2=grr*xdot(dnr,dnr)+gtt*xdot(dnt,dnt)+gpp*xdot(dnp,dnp); e2=0.5*g2
    Srt=xcr(dnr,dnt); Srp=xcr(dnr,dnp); Stp=xcr(dnt,dnp)
    L4s=2*(grr*gtt*xdot(Srt,Srt)+grr*gpp*xdot(Srp,Srp)+gtt*gpp*xdot(Stp,Stp)); e4=0.25*L4s
    sqrtg=np.exp(phd)*r**2*SINT
    return np.sum((e2+e4)*sqrtg)*DTH*DPH

def total_energy(rg,Farr,phia):
    Nr=len(rg); flds=[nhat(Farr[i]) for i in range(Nr)]
    densr=np.array([shell_energy(flds[i],dr_nonuniform(flds,rg,i),phia[i],rg[i]) for i in range(Nr)])
    return np.trapezoid(densr,rg)
