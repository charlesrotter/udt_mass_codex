#!/usr/bin/env python3
"""
n3_isotropy_check.py — CRITICAL self-audit before recording.

The pure hedgehog n = x/|x| (Theta=theta) is EXACTLY SO(3)-covariant: an iso-
rotation about target axis a EQUALS a spatial rotation about axis a.  Therefore
the iso-moment-of-inertia tensor Lambda_ab MUST be isotropic (∝ delta_ab) for the
pure hedgehog by an exact symmetry argument.  Any anisotropy in the numeric
Lambda_ab from the FULL profile run is then either (i) a real effect of the
radial profile Theta(r) breaking Theta=theta, or (ii) a GRID ARTIFACT of the
theta-grid (which singles out the z-axis: v_3 = e_3 x n vanishes on the z-axis
and the polar coordinate under-resolves it).

This script ISOLATES the cause:
 A) Compute Lambda_ab for the PURE hedgehog Theta(r)=theta (a fixed map, NO radial
    profile) at increasing theta/phi resolution.  By the exact symmetry it must
    -> isotropic; watch the spread shrink with resolution => the split in the
    main run is a GRID ARTIFACT, not physics.
 B) Confirm analytically: for the pure hedgehog the L2 density v_a.v_b integrates
    to (8pi/3) delta_ab * INT dr (...).  Check the three diagonal entries converge
    to equal and off-diagonal -> 0.

If even the PURE hedgehog (which is provably isotropic) shows the 2:1 z-split,
the split is a coordinate artifact and the HONEST answer is DEGENERATE.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import math, numpy as np, torch
torch.set_default_dtype(torch.float64)
DEV = "cuda" if torch.cuda.is_available() else "cpu"
print(f"[device] {DEV}")


def lambda_pure_hedgehog(r_np, phi_np, xi, kappa, nth, nph):
    """Lambda_ab for the EXACT hedgehog Theta=theta (so sinTheta=sin th, etc.)."""
    r = torch.as_tensor(r_np, device=DEV)
    phi = torch.as_tensor(phi_np, device=DEV)
    th = torch.linspace(0.0, math.pi, nth, device=DEV)         # include poles
    ph = torch.linspace(0.0, 2*math.pi, nph, device=DEV)
    dr = r[1:]-r[:-1]; rm = 0.5*(r[1:]+r[:-1]); phim = 0.5*(phi[1:]+phi[:-1])
    Nr = rm.shape[0]
    # midpoints in theta, phi (proper midpoint rule, avoids pole double-count)
    thm = 0.5*(th[1:]+th[:-1]); phm = 0.5*(ph[1:]+ph[:-1])
    dth = th[1:]-th[:-1]; dph = ph[1:]-ph[:-1]
    nt = thm.shape[0]; npp = phm.shape[0]
    R = rm.view(Nr,1,1); PHI = phim.view(Nr,1,1)
    TT = thm.view(1,nt,1); PP = phm.view(1,1,npp)
    DTH = dth.view(1,nt,1); DPH = dph.view(1,1,npp); DR = dr.view(Nr,1,1)

    # pure hedgehog: Theta=theta => sinTheta=sin th, Theta'(r)=0 (no radial profile)
    st = torch.sin(TT); ct = torch.cos(TT); sp = torch.sin(PP); cp = torch.cos(PP)
    ONE = torch.ones((Nr,nt,npp), device=DEV)
    st=st*ONE; ct=ct*ONE; sp=sp*ONE; cp=cp*ONE
    n1 = st*cp; n2 = st*sp; n3 = ct
    # d_r n = 0 (Theta'=0).  d_th n = (ct cp, ct sp, -st); d_ph n=(-st sp, st cp,0)
    dt = (ct*cp, ct*sp, -st); dp = (-st*sp, st*cp, torch.zeros_like(n1))
    em2phi = torch.exp(-2*PHI)
    gthth = 1.0/R**2; gphph = 1.0/(R**2*st**2)
    def d2(A): return A[0]**2+A[1]**2+A[2]**2
    grad2 = gthth*d2(dt) + gphph*d2(dp)   # (d_r=0)
    sqrtg = torch.exp(PHI)*R**2*st
    measure = sqrtg*torch.exp(2*PHI)
    v = [(torch.zeros_like(n1),-n3,n2),(n3,torch.zeros_like(n1),-n1),(-n2,n1,torch.zeros_like(n1))]
    def dot(A,B): return A[0]*B[0]+A[1]*B[1]+A[2]*B[2]
    vol = DR*DTH*DPH
    Lam = np.zeros((3,3))
    for a in range(3):
        for b in range(3):
            vavb = dot(v[a],v[b])
            cross = gthth*dot(v[a],dt)*dot(v[b],dt) + gphph*dot(v[a],dp)*dot(v[b],dp)
            dens = (xi/2.0)*vavb + (kappa/2.0)*(vavb*grad2 - cross)
            Lam[a,b] = float((measure*dens*vol).sum())
    return Lam


def lambda_profile(r_np, Theta_np, phi_np, xi, kappa, nth, nph):
    """Lambda_ab for the BVP profile Theta(r), proper midpoint rule (incl. d_r n)."""
    r=torch.as_tensor(r_np,device=DEV); phi=torch.as_tensor(phi_np,device=DEV)
    Th=torch.as_tensor(Theta_np,device=DEV)
    Thp=torch.as_tensor(np.gradient(Theta_np,r_np),device=DEV)
    th=torch.linspace(0.0,math.pi,nth,device=DEV); ph=torch.linspace(0.0,2*math.pi,nph,device=DEV)
    dr=r[1:]-r[:-1]; rm=0.5*(r[1:]+r[:-1]); phim=0.5*(phi[1:]+phi[:-1])
    Thm=0.5*(Th[1:]+Th[:-1]); Thpm=0.5*(Thp[1:]+Thp[:-1]); Nr=rm.shape[0]
    thm=0.5*(th[1:]+th[:-1]); phm=0.5*(ph[1:]+ph[:-1])
    dth=th[1:]-th[:-1]; dph=ph[1:]-ph[:-1]; nt=thm.shape[0]; npp=phm.shape[0]
    R=rm.view(Nr,1,1); PHI=phim.view(Nr,1,1); STH=torch.sin(Thm).view(Nr,1,1)
    CTH=torch.cos(Thm).view(Nr,1,1); THP=Thpm.view(Nr,1,1)
    TT=thm.view(1,nt,1); PP=phm.view(1,1,npp)
    DR=dr.view(Nr,1,1); DTH=dth.view(1,nt,1); DPH=dph.view(1,1,npp)
    ONE=torch.ones((Nr,nt,npp),device=DEV)
    sTh=STH*ONE; cTh=CTH*ONE; st=torch.sin(TT)*ONE; ct=torch.cos(TT)*ONE
    sp=torch.sin(PP)*ONE; cp=torch.cos(PP)*ONE
    n1=sTh*st*cp; n2=sTh*st*sp; n3=cTh
    drn=(cTh*st*cp*THP, cTh*st*sp*THP, -sTh*THP)
    dt=(sTh*ct*cp, sTh*ct*sp, torch.zeros_like(n1)); dp=(-sTh*st*sp, sTh*st*cp, torch.zeros_like(n1))
    em2phi=torch.exp(-2*PHI); grr=em2phi; gthth=1.0/R**2; gphph=1.0/(R**2*st**2)
    def d2(A): return A[0]**2+A[1]**2+A[2]**2
    grad2=grr*d2(drn)+gthth*d2(dt)+gphph*d2(dp)
    sqrtg=torch.exp(PHI)*R**2*st; measure=sqrtg*torch.exp(2*PHI)
    v=[(torch.zeros_like(n1),-n3,n2),(n3,torch.zeros_like(n1),-n1),(-n2,n1,torch.zeros_like(n1))]
    def dot(A,B): return A[0]*B[0]+A[1]*B[1]+A[2]*B[2]
    vol=DR*DTH*DPH; Lam=np.zeros((3,3))
    for a in range(3):
        for b in range(3):
            vavb=dot(v[a],v[b])
            cross=grr*dot(v[a],drn)*dot(v[b],drn)+gthth*dot(v[a],dt)*dot(v[b],dt)+gphph*dot(v[a],dp)*dot(v[b],dp)
            dens=(xi/2.0)*vavb+(kappa/2.0)*(vavb*grad2-cross)
            Lam[a,b]=float((measure*dens*vol).sum())
    return Lam


def main():
    xi=1.0; kappa=1.0; r_core=0.05; r_int=r_core+12.0
    rg = np.linspace(r_core, r_int, 400); phi0=np.zeros_like(rg)
    print("="*72)
    print("PURE HEDGEHOG Theta=theta (provably SO(3)-isotropic): grid convergence")
    print("If the z-axis (Lambda_33) split SHRINKS with resolution => the main-run")
    print("split is a polar-grid artifact, and the true answer is DEGENERATE.")
    print("="*72)
    print(f"{'nth=nph':>8} {'Lam_11':>12} {'Lam_22':>12} {'Lam_33':>12} "
          f"{'spread':>10} {'offmax':>10}")
    for n in [60, 120, 240, 480]:
        Lam = lambda_pure_hedgehog(rg, phi0, xi, kappa, n, n)
        ev = np.linalg.eigvalsh(Lam)
        d = np.diag(Lam); offmax = np.max(np.abs(Lam-np.diag(d)))
        spread = (ev.max()-ev.min())/ev.mean()
        print(f"{n:8d} {d[0]:12.4f} {d[1]:12.4f} {d[2]:12.4f} {spread:10.3e} {offmax:10.3e}")

    print("\n" + "="*72)
    print("FULL PROFILE Theta(r) (BVP soliton), same midpoint integrator:")
    print("Theta(r) still gives n = (sinTheta(r) sinth cosph,...), STILL exactly")
    print("SO(3) iso-covariant => MUST also be isotropic.  Convergence test:")
    print("="*72)
    from scipy.integrate import solve_bvp
    def theta_ddot(r,Th,Thp,phi,phip,xi,kappa):
        s=np.sin(Th)
        num=((0.5)*Thp*r**2*(-4*Thp*kappa*np.sin(2*Th)+Thp*kappa*np.sin(4*Th)
            -Thp*r**2*xi*np.sin(2*Th)+kappa*phip*(1-np.cos(2*Th))**2
            -2*kappa*phip*np.cos(2*Th)+2*kappa*phip-phip*r**2*xi*np.cos(2*Th)
            +5*phip*r**2*xi+2*r*xi*np.cos(2*Th)-10*r*xi)
            +2*kappa*np.exp(2*phi)*s**3*np.cos(Th)+2*r**2*xi*np.exp(2*phi)*np.sin(2*Th))
        den=r**2*(2*kappa*s**4+2*kappa*s**2+r**2*xi*s**2+2*r**2*xi)
        return num/den
    x0=np.linspace(r_core,r_int,400)
    def rhs(r,y): return np.vstack([y[1],theta_ddot(r,y[0],y[1],0*r,0*r,xi,kappa)])
    def bc(ya,yb): return np.array([ya[0]-math.pi,yb[0]-0.0])
    L=1.0; Th0=math.pi*0.5*(1-np.tanh((x0-(r_core+2*L))/(0.8*L)))
    sol=solve_bvp(rhs,bc,x0,np.vstack([Th0,np.gradient(Th0,x0)]),tol=1e-8,max_nodes=200000)
    rg2=np.linspace(r_core,r_int,800); Thr=sol.sol(rg2)[0]
    print(f"{'nth=nph':>8} {'Lam_11':>12} {'Lam_22':>12} {'Lam_33':>12} {'spread':>10} {'offmax':>10}")
    for n in [120,240,480]:
        Lam=lambda_profile(rg2,Thr,np.zeros_like(rg2),xi,kappa,n,n)
        ev=np.linalg.eigvalsh(Lam); d=np.diag(Lam); offmax=np.max(np.abs(Lam-np.diag(d)))
        print(f"{n:8d} {d[0]:12.4f} {d[1]:12.4f} {d[2]:12.4f} {(ev.max()-ev.min())/ev.mean():10.3e} {offmax:10.3e}")

    print("\nAnalytic check (pure hedgehog, L2 only, flat phi):")
    print("  Lambda^{L2}_ab = (xi/2) INT sqrt(g) (v_a.v_b) dV.")
    print("  v_a.v_b for n on unit sphere integrates to (8pi/3) delta_ab per shell,")
    print("  so the three diagonal entries MUST be exactly equal, off-diag=0.")
    # exact: INT_S2 (v_a.v_b) dOmega = (8pi/3) delta_ab ; times (xi/2) INT r^2 dr (flat)
    shell = (xi/2.0)*(8*math.pi/3.0)*( (r_int**3 - r_core**3)/3.0 )
    print(f"  exact Lambda^L2_aa (flat) = (xi/2)(8pi/3) INT r^2 dr = {shell:.4f} (all three equal)")


if __name__=="__main__":
    main()
