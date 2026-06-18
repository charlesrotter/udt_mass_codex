"""
Deliverable #2: transverse radial operator coefficients P_t (kinetic, psi'^2),
V_t (potential, psi^2), W_t (time weight) for l=1 and l=2, on the stationary unit
background (p=0). Extracted from the second-variation densities per shell.
P_t(r) = coeff of psi'^2 ; V_t(r) = coeff of psi^2 ; W_t(r) = time-kinetic weight.
We isolate them by the (s,sp) FD machinery applied SHELL-LOCALLY.
"""
import os
for v in ("OMP_NUM_THREADS","MKL_NUM_THREADS","OPENBLAS_NUM_THREADS","NUMEXPR_NUM_THREADS"):
    os.environ[v]="1"
import numpy as np, sys
sys.path.insert(0,'.')
import lean2 as L
from lean2 import nhat,angderiv,xdot,xcr,SINT,COST,TG,PG,DTH,DPH,geomgrid,dr_nonuniform
import bg

def angtan(F,fang,gang):
    n0=nhat(F); h=1e-6; d=(nhat(F+h)-nhat(F-h))/(2*h); d=d-xdot(d,n0)[...,None]*n0
    e1=d/np.sqrt(xdot(d,d))[...,None]; e2=xcr(n0,e1)
    return fang(TG,PG)[...,None]*e1+gang(TG,PG)[...,None]*e2

def coeffs(p,l,m,tag,R=18.0,r_core=0.05,Nr=70,r_int=1.0,ds=2e-4):
    sol=bg.solve_profile(p,r_core=r_core,R=R,r_int=r_int)
    rg=geomgrid(r_core,R,Nr); F=sol.sol(rg)[0]; phia=p*np.log(rg/r_int)
    if l==1: Yf={0:lambda T,P:np.cos(T),1:lambda T,P:np.sin(T)*np.cos(P),-1:lambda T,P:np.sin(T)*np.sin(P)}[m]
    if l==2: Yf={0:lambda T,P:3*np.cos(T)**2-1,1:lambda T,P:np.sin(T)*np.cos(T)*np.cos(P),
        -1:lambda T,P:np.sin(T)*np.cos(T)*np.sin(P)}[m]
    ZERO=lambda T,P:np.zeros_like(T)
    if tag=='e1': fang,gang=Yf,ZERO
    else: fang,gang=ZERO,Yf
    flds=[nhat(F[i]) for i in range(Nr)]
    tang=[angtan(F[i],fang,gang) for i in range(Nr)]
    P=np.zeros(Nr); V=np.zeros(Nr); W=np.zeros(Nr)
    for i in range(Nr):
        r=rg[i]; phd=phia[i]; n0=flds[i]; T=tang[i]
        # local field with s (value) and sp (radial slope) of the mode amplitude:
        # build a 3-shell stencil where psi = s0 + sp0*(r-r_i)
        def dens(s0,sp0):
            # field at i-1,i,i+1 with psi linear; but only shell i density needs dn/dr
            hi=rg[i]-rg[i-1] if i>0 else rg[1]-rg[0]
            hp=rg[i+1]-rg[i] if i<Nr-1 else rg[-1]-rg[-2]
            def fld_at(j,rj):
                psi=s0+sp0*(rj-r)
                w=flds[j]+psi*tang[j] if j==i else nhat(F[j])+ (s0+sp0*(rj-r))*angtan(F[j],fang,gang)
                return w/np.sqrt(xdot(w,w))[...,None]
            fi=fld_at(i,r)
            jm=max(i-1,0); jp=min(i+1,Nr-1)
            fim=fld_at(jm,rg[jm]); fip=fld_at(jp,rg[jp])
            # dn/dr central nonuniform at i
            if i==0: dnr=(fip-fi)/(rg[1]-rg[0])
            elif i==Nr-1: dnr=(fi-fim)/(rg[-1]-rg[-2])
            else:
                h1=rg[i]-rg[i-1]; h2=rg[i+1]-rg[i]
                dnr=(fip*h1**2 - fim*h2**2 + fi*(h2**2-h1**2))/(h1*h2*(h1+h2))
            return L.shell_energy(fi,dnr,phd,r)
        d=ds
        A00=dens(0,0)
        app=dens(d,0); amm=dens(-d,0); V[i]=(app-2*A00+amm)/(2*d**2)
        bpp=dens(0,d); bmm=dens(0,-d); P[i]=(bpp-2*A00+bmm)/(2*d**2)
        # weight
        dd=d*T  # not used; compute W directly
        dt=T-xdot(T,n0)[...,None]*n0
        dnr=dr_nonuniform(flds,rg,i); dnt,dnp=angderiv(n0)
        grr=np.exp(-2*phd); gtt=1/r**2; gpp=1/(r**2*SINT**2); e2phi=np.exp(2*phd)
        w2=e2phi*xdot(dt,dt); cxr=xcr(dt,dnr); cxt=xcr(dt,dnt); cxp=xcr(dt,dnp)
        w4=e2phi*(grr*xdot(cxr,cxr)+gtt*xdot(cxt,cxt)+gpp*xdot(cxp,cxp))
        W[i]=np.sum((w2+w4)*np.exp(phd)*r**2*SINT)*DTH*DPH
    return rg,P,V,W

if __name__=='__main__':
    for l in (1,2):
        rg,P,V,W=coeffs(0,l,1,'e2')
        print(f"\n=== l={l} m=1 e2 channel, p=0 (sampled radial coefficients) ===")
        print(" r        P_t(kin)     V_t(pot)     W_t(weight)")
        for j in range(0,len(rg),10):
            print(f" {rg[j]:6.3f}  {P[j]:11.4e}  {V[j]:11.4e}  {W[j]:11.4e}")
        print(f" sum V_t (sign of net potential): {np.trapezoid(V,rg):.4f}  (>0 => no tachyon well)")
