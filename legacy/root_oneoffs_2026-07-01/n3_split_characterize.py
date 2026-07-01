#!/usr/bin/env python3
"""
n3_split_characterize.py — characterize the SPLIT found in Lambda_ab.

ESTABLISHED (n3_isotropy_check.py):
 - Pure hedgehog Theta=theta: Lambda_ab ISOTROPIC (spread -> 0 as 1/n^2; the exact
   SO(3) symmetry).  Confirms the integrator is correct.
 - PROFILE hedgehog n=(sinTheta(r) sinth cosph, sinTheta(r) sinth sinph, cosTheta(r)):
   Lambda_ab SPLITS, resolution-INDEPENDENTLY, into 2 equal + 1 different
   (Lambda_11=Lambda_22 >> Lambda_33).  spread 1.491, off-diag ~ machine zero.

WHY: the SETTLED native ansatz (native_stabilizer_results.md) is the EASY-AXIS
baby-Skyrme hedgehog: n3 = cosTheta(r) depends only on r, while n1,n2 carry the
spatial (th,ph) winding.  This ansatz NATIVELY distinguishes target-axis 3 (the
"easy axis" along which the profile interpolates pi->0).  Iso-rotations about
axes 1,2 tilt the easy axis (cost ~ winding gradient energy); the iso-rotation
about axis 3 only spins the phase of the (n1,n2) winding (a different, smaller
cost).  So the split is a NATIVE consequence of the soliton ansatz that the
settled L2+L4 model already uses — NOT a coordinate artifact.

This script:
 1. Confirms resolution independence of the split (the amplitude is real).
 2. Extracts the PURE-NUMBER split ratio Lambda_perp/Lambda_3 (= Lambda_11/Lambda_33),
    and its xi/kappa, cell-size, and deep-phi dependence (does it stay ~constant
    => a clean native number, or drift => background-dependent?).
 3. Reports the PATTERN: (2 equal + 1) axial, NOT cyclic Z3.  off-diagonal=0.
 4. Splits the ratio into L2 and L4 contributions.
 5. THE sqrt QUESTION: Lambda_ab is the inertia of dot-n dot-n => it is
   QUADRATIC in the field velocity (energy ~ Lambda omega^2).  The natural
   "amplitude" is omega (or the collective coordinate), and energy ~ amplitude^2.
   We report whether a sqrt(energy) amplitude is the native primitive here.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK","0")
import math, numpy as np, torch
from scipy.integrate import solve_bvp
torch.set_default_dtype(torch.float64)
DEV="cuda" if torch.cuda.is_available() else "cpu"
print(f"[device] {DEV}")

def theta_ddot(r,Th,Thp,phi,phip,xi,kappa):
    s=np.sin(Th)
    num=((0.5)*Thp*r**2*(-4*Thp*kappa*np.sin(2*Th)+Thp*kappa*np.sin(4*Th)
        -Thp*r**2*xi*np.sin(2*Th)+kappa*phip*(1-np.cos(2*Th))**2
        -2*kappa*phip*np.cos(2*Th)+2*kappa*phip-phip*r**2*xi*np.cos(2*Th)
        +5*phip*r**2*xi+2*r*xi*np.cos(2*Th)-10*r*xi)
        +2*kappa*np.exp(2*phi)*s**3*np.cos(Th)+2*r**2*xi*np.exp(2*phi)*np.sin(2*Th))
    den=r**2*(2*kappa*s**4+2*kappa*s**2+r**2*xi*s**2+2*r**2*xi)
    return num/den

def phi_bg(r,p,r_int):
    if p==0.0: return np.zeros_like(r),np.zeros_like(r)
    return p*np.log(r/r_int), p/r

def solve_profile(r_core,r_int,xi,kappa,p,N=500):
    x0=np.linspace(r_core,r_int,N); L=math.sqrt(kappa/xi)
    def rhs(r,y):
        phi,phip=phi_bg(r,p,r_int); return np.vstack([y[1],theta_ddot(r,y[0],y[1],phi,phip,xi,kappa)])
    def bc(ya,yb): return np.array([ya[0]-math.pi,yb[0]-0.0])
    Th0=math.pi*0.5*(1-np.tanh((x0-(r_core+2*L))/(0.8*L)))
    return solve_bvp(rhs,bc,x0,np.vstack([Th0,np.gradient(Th0,x0)]),tol=1e-8,max_nodes=200000)

def lambda_tensor(r_np,Theta_np,phi_np,xi,kappa,nth,nph):
    """Lambda_ab (total, and L2/L4 split) for profile Theta(r). midpoint rule."""
    r=torch.as_tensor(r_np,device=DEV); phi=torch.as_tensor(phi_np,device=DEV)
    Th=torch.as_tensor(Theta_np,device=DEV); Thp=torch.as_tensor(np.gradient(Theta_np,r_np),device=DEV)
    th=torch.linspace(0.0,math.pi,nth,device=DEV); ph=torch.linspace(0.0,2*math.pi,nph,device=DEV)
    dr=r[1:]-r[:-1]; rm=0.5*(r[1:]+r[:-1]); phim=0.5*(phi[1:]+phi[:-1])
    Thm=0.5*(Th[1:]+Th[:-1]); Thpm=0.5*(Thp[1:]+Thp[:-1]); Nr=rm.shape[0]
    thm=0.5*(th[1:]+th[:-1]); phm=0.5*(ph[1:]+ph[:-1]); dth=th[1:]-th[:-1]; dph=ph[1:]-ph[:-1]
    nt=thm.shape[0]; npp=phm.shape[0]
    R=rm.view(Nr,1,1); PHI=phim.view(Nr,1,1); STH=torch.sin(Thm).view(Nr,1,1)
    CTH=torch.cos(Thm).view(Nr,1,1); THP=Thpm.view(Nr,1,1)
    TT=thm.view(1,nt,1); PP=phm.view(1,1,npp); DR=dr.view(Nr,1,1); DTH=dth.view(1,nt,1); DPH=dph.view(1,1,npp)
    ONE=torch.ones((Nr,nt,npp),device=DEV)
    sTh=STH*ONE; cTh=CTH*ONE; st=torch.sin(TT)*ONE; ct=torch.cos(TT)*ONE; sp=torch.sin(PP)*ONE; cp=torch.cos(PP)*ONE
    n1=sTh*st*cp; n2=sTh*st*sp; n3=cTh
    drn=(cTh*st*cp*THP, cTh*st*sp*THP, -sTh*THP)
    dt=(sTh*ct*cp, sTh*ct*sp, torch.zeros_like(n1)); dp=(-sTh*st*sp, sTh*st*cp, torch.zeros_like(n1))
    grr=torch.exp(-2*PHI); gthth=1.0/R**2; gphph=1.0/(R**2*st**2)
    def d2(A): return A[0]**2+A[1]**2+A[2]**2
    grad2=grr*d2(drn)+gthth*d2(dt)+gphph*d2(dp)
    measure=torch.exp(PHI)*R**2*st*torch.exp(2*PHI)
    v=[(torch.zeros_like(n1),-n3,n2),(n3,torch.zeros_like(n1),-n1),(-n2,n1,torch.zeros_like(n1))]
    def dot(A,B): return A[0]*B[0]+A[1]*B[1]+A[2]*B[2]
    vol=DR*DTH*DPH; L2=np.zeros((3,3)); L4=np.zeros((3,3))
    for a in range(3):
        for b in range(3):
            vavb=dot(v[a],v[b])
            cross=grr*dot(v[a],drn)*dot(v[b],drn)+gthth*dot(v[a],dt)*dot(v[b],dt)+gphph*dot(v[a],dp)*dot(v[b],dp)
            L2[a,b]=float((measure*(xi/2.0)*vavb*vol).sum())
            L4[a,b]=float((measure*(kappa/2.0)*(vavb*grad2-cross)*vol).sum())
    return L2,L4,L2+L4

def main():
    xi=1.0; r_core=0.05
    print("="*78); print("1) RESOLUTION INDEPENDENCE of the split (kappa=1, flat, cell=12L)"); print("="*78)
    r_int=r_core+12.0; sol=solve_profile(r_core,r_int,xi,1.0,0.0)
    rg=np.linspace(r_core,r_int,800); Th=sol.sol(rg)[0]
    print(f"{'nth=nph':>8} {'Lam_perp(11=22)':>16} {'Lam_3(33)':>12} {'ratio perp/3':>13} {'offmax':>10}")
    for n in [120,240,360]:
        _,_,Lam=lambda_tensor(rg,Th,np.zeros_like(rg),xi,1.0,n,n)
        d=np.diag(Lam); off=np.max(np.abs(Lam-np.diag(d)))
        print(f"{n:8d} {0.5*(d[0]+d[1]):16.5f} {d[2]:12.5f} {(0.5*(d[0]+d[1]))/d[2]:13.6f} {off:10.2e}")

    print("\n"+"="*78); print("2) PATTERN: is it (2 equal + 1) axial, or cyclic Z3? eigvals + eigvecs"); print("="*78)
    _,_,Lam=lambda_tensor(rg,Th,np.zeros_like(rg),xi,1.0,300,300)
    ev,evec=np.linalg.eigh(Lam)
    print("Lambda_ab =\n",np.array2string(Lam,precision=5,suppress_small=True))
    print("eigenvalues:",ev)
    print("=> two equal (perp), one distinct (along target-3) => AXIAL (2+1), NOT cyclic.")

    print("\n"+"="*78); print("3) L2 vs L4 contribution to the split"); print("="*78)
    L2,L4,Lam=lambda_tensor(rg,Th,np.zeros_like(rg),xi,1.0,300,300)
    for nm,M in [("L2",L2),("L4",L4),("total",Lam)]:
        d=np.diag(M); print(f"  {nm:5}: perp={0.5*(d[0]+d[1]):11.4f} along3={d[2]:11.4f} ratio={0.5*(d[0]+d[1])/d[2]:.6f}")

    print("\n"+"="*78); print("4) DEPENDENCE of the ratio on kappa/xi, cell size, deep-phi"); print("="*78)
    print(f"{'case':>28} {'perp':>12} {'along3':>12} {'ratio perp/3':>13}")
    # kappa scan (flat)
    for kappa in [0.25,1.0,4.0,9.0]:
        L=math.sqrt(kappa/xi); r_int=r_core+12.0*L
        sol=solve_profile(r_core,r_int,xi,kappa,0.0); rg=np.linspace(r_core,r_int,800); Th=sol.sol(rg)[0]
        _,_,Lam=lambda_tensor(rg,Th,np.zeros_like(rg),xi,kappa,260,260); d=np.diag(Lam)
        print(f"{'flat kappa=%.2f'%kappa:>28} {0.5*(d[0]+d[1]):12.4f} {d[2]:12.4f} {0.5*(d[0]+d[1])/d[2]:13.6f}")
    # cell size scan
    kappa=1.0
    for mult in [8.0,12.0,20.0,30.0]:
        r_int=r_core+mult; sol=solve_profile(r_core,r_int,xi,kappa,0.0); rg=np.linspace(r_core,r_int,1000); Th=sol.sol(rg)[0]
        _,_,Lam=lambda_tensor(rg,Th,np.zeros_like(rg),xi,kappa,260,260); d=np.diag(Lam)
        print(f"{'flat cell=%.0fL'%mult:>28} {0.5*(d[0]+d[1]):12.4f} {d[2]:12.4f} {0.5*(d[0]+d[1])/d[2]:13.6f}")
    # deep-phi scan
    r_int=r_core+12.0
    for p in [0.0,0.5,1.0,2.0]:
        sol=solve_profile(r_core,r_int,xi,kappa,p); rg=np.linspace(r_core,r_int,1000); Th=sol.sol(rg)[0]
        phi,_=phi_bg(rg,p,r_int); _,_,Lam=lambda_tensor(rg,Th,phi,xi,kappa,260,260); d=np.diag(Lam)
        print(f"{'deep p=%.1f'%p:>28} {0.5*(d[0]+d[1]):12.4f} {d[2]:12.4f} {0.5*(d[0]+d[1])/d[2]:13.6f}")

    print("\n"+"="*78); print("5) sqrt STRUCTURE: every Lambda_ab is mass/energy-dimensioned (inertia).")
    print("   Energy of iso-rotation = (1/2)Lambda omega^2: QUADRATIC in the velocity.")
    print("   The native primitive amplitude is the angular velocity / collective")
    print("   coordinate omega; energy ~ omega^2.  Report verdict in the .md.")
    print("="*78)

if __name__=="__main__":
    main()
