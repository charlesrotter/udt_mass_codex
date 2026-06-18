"""
LEAN, low-memory pipeline (commit-charge constrained env).
- Never hold 4D arrays. Per radial shell use small 2D (Nth,Nph) float64 arrays, freed.
- (1) Build reduced 1D energy functional of the UNIT field via numeric angular quadrature.
- (2) Solve stationary profile F(r) (1D BVP from the tabulated reduced Lagrangian).
- (3) Transverse l>=1 operator: per channel, compute radial densities P,Q,R,W by the
      eps-second-variation, angular integral by quadrature, tiny arrays.
All cross products done componentwise. Threads pinned to 1.
"""
import os
for v in ("OMP_NUM_THREADS","MKL_NUM_THREADS","OPENBLAS_NUM_THREADS","NUMEXPR_NUM_THREADS"):
    os.environ[v]="1"
import numpy as np

Nth=64; Nph=12
TH=np.linspace(1e-3,np.pi-1e-3,Nth); DTH=TH[1]-TH[0]
PH=np.linspace(0,2*np.pi,Nph,endpoint=False); DPH=2*np.pi/Nph
TG,PG=np.meshgrid(TH,PH,indexing='ij')        # (Nth,Nph)
SINT=np.sin(TG); COST=np.cos(TG); COSP=np.cos(PG); SINP=np.sin(PG)

def nhat(F):
    """unit field at scalar F over angular grid -> (Nth,Nph,3)"""
    a=np.sin(F)*SINT*COSP; b=np.sin(F)*SINT*SINP; c=np.cos(F)*np.ones_like(SINT)
    n=np.empty((Nth,Nph,3))
    norm=np.sqrt(a*a+b*b+c*c)
    n[...,0]=a/norm; n[...,1]=b/norm; n[...,2]=c/norm
    return n

def dn_dF(F,h=1e-6):
    return (nhat(F+h)-nhat(F-h))/(2*h)

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

def energy_density_shell(fld, dnr, phd, r):
    """(L2+L4)*sqrtg integrated over the sphere for one shell. fld,dnr:(Nth,Nph,3)."""
    dnt,dnp=angderiv(fld)
    grr=np.exp(-2*phd); gtt=1/r**2; gpp=1/(r**2*SINT**2)
    g2=grr*xdot(dnr,dnr)+gtt*xdot(dnt,dnt)+gpp*xdot(dnp,dnp)
    e2=0.5*g2
    Srt=xcr(dnr,dnt); Srp=xcr(dnr,dnp); Stp=xcr(dnt,dnp)
    L4s=2*(grr*gtt*xdot(Srt,Srt)+grr*gpp*xdot(Srp,Srp)+gtt*gpp*xdot(Stp,Stp))
    e4=0.25*L4s
    sqrtg=np.exp(phd)*r**2*SINT
    return np.sum((e2+e4)*sqrtg)*DTH*DPH

def total_energy(rgrid, Farr, phiarr):
    Nr=len(rgrid); dr=rgrid[1]-rgrid[0]
    # need dn/dr: use F neighbors
    densr=np.empty(Nr)
    flds=[nhat(Farr[i]) for i in range(Nr)]
    for i in range(Nr):
        if i==0: dnr=(flds[1]-flds[0])/dr
        elif i==Nr-1: dnr=(flds[-1]-flds[-2])/dr
        else: dnr=(flds[i+1]-flds[i-1])/(2*dr)
        densr[i]=energy_density_shell(flds[i],dnr,phiarr[i],rgrid[i])
    return np.trapezoid(densr,rgrid)

if __name__=='__main__':
    # sanity: energy of corpus-like linear profile, p=0
    r_core=0.05; R=18.0; Nr=60
    rg=np.linspace(r_core,r_core+R,Nr)
    F=np.pi*np.exp(-(rg-r_core)/2.0); F[-1]=0
    phia=np.zeros(Nr)
    print("sample total energy (unit field, init profile):", total_energy(rg,F,phia))
    print("mem-safe core OK")
