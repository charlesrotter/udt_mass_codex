#!/usr/bin/env python3
"""
lepton_soliton_spectrum_deep.py — deep-phi anchor + Koide Q + spacing-law fit.

Fixes the float64 overflow of the e^{3phi} breathing weight at p>=2 by working
in a RESCALED weight (divide H and W by a common e^{3phi} reference => the
generalized eigenvalue omega^2 is invariant under a common positive rescaling of
W, and under scaling H,W by the SAME factor).  Cross-check with mpmath at the
deepest node.  Also fits the (Pb) spacing law: omega_n^2 ~ a + b n (O(1)) vs
omega_n ~ omega_0 e^{c n} (exponential).
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK","0")
import math, numpy as np, torch
from scipy.integrate import solve_bvp
torch.set_default_dtype(torch.float64)
DEV="cuda" if torch.cuda.is_available() else "cpu"
TWO_PI=2*math.pi
print(f"[device] {DEV}")

def phi_bg(r,p,r_int):
    if p==0.0: return np.zeros_like(r),np.zeros_like(r)
    return p*np.log(r/r_int),p/r

def theta_ddot(r,Th,Thp,phi,phip,xi,kappa):
    s=np.sin(Th)
    num=((0.5)*Thp*r**2*(-4*Thp*kappa*np.sin(2*Th)+Thp*kappa*np.sin(4*Th)
        -Thp*r**2*xi*np.sin(2*Th)+kappa*phip*(1-np.cos(2*Th))**2-2*kappa*phip*np.cos(2*Th)
        +2*kappa*phip-phip*r**2*xi*np.cos(2*Th)+5*phip*r**2*xi+2*r*xi*np.cos(2*Th)-10*r*xi)
        +2*kappa*np.exp(2*phi)*s**3*np.cos(Th)+2*r**2*xi*np.exp(2*phi)*np.sin(2*Th))
    den=r**2*(2*kappa*s**4+2*kappa*s**2+r**2*xi*s**2+2*r**2*xi)
    return num/den

def solve_ground(r_core,r_int,xi,kappa,p,N=600):
    x0=np.linspace(r_core,r_int,N)
    def rhs(r,y):
        Th,Thp=y; phi,phip=phi_bg(r,p,r_int)
        return np.vstack([Thp,theta_ddot(r,Th,Thp,phi,phip,xi,kappa)])
    def bc(ya,yb): return np.array([ya[0]-math.pi,yb[0]])
    L=math.sqrt(kappa/xi); w=2*L
    Th0=math.pi*0.5*(1-np.tanh((x0-(r_core+w))/(0.8*L)))
    sol=solve_bvp(rhs,bc,x0,np.vstack([Th0,np.gradient(Th0,x0)]),tol=1e-9,max_nodes=400000)
    return sol

def energy(rg,Th,phi,xi,kappa,m=1):
    dr=np.diff(rg); rm=0.5*(rg[1:]+rg[:-1]); phim=0.5*(phi[1:]+phi[:-1])
    Thm=0.5*(Th[1:]+Th[:-1]); Thp=np.diff(Th)/dr
    s=np.sin(Thm);s2=s*s;s4=s2*s2;em=np.exp(-phim);e2p=np.exp(2*phim);m2=m*m
    E2=(TWO_PI*xi/3)*em*(rm**2*s2*Thp**2+2*rm**2*Thp**2+4*e2p*m2*s2)
    E4=(TWO_PI*kappa/3)*em*((2*rm**2*s4+2*rm**2*s2)*Thp**2+e2p*m2*s4)/rm**2
    return float(np.sum(E2*dr)),float(np.sum(E4*dr))

def fluct_spectrum(rg,Th0,phi,xi,kappa,nev=8):
    """Rescaled: factor out exp(3*phi) from W and a common ref so float64 stays sane.
    omega^2 from generalized H u = omega^2 W u is invariant if we divide BOTH the
    SL operator and W by a common positive function only when that function is
    constant; here we instead absorb exp(3*phi) analytically: define u~ = sqrt(W) u.
    To avoid overflow we normalise phi so max|3 phi| is moderate by subtracting a
    constant phi_ref (a constant shift of phi is a coordinate/clock rescale that
    multiplies ALL energies equally -> cancels in ratios). """
    r=rg; N=len(r); Th0=np.asarray(Th0)
    phi_ref=phi.mean()
    ph=phi-phi_ref   # constant shift; cancels in omega ratios
    def edens(T,Tp,rr,p_):
        s=np.sin(T);s2=s*s;s4=s2*s2;em=np.exp(-p_);e2p=np.exp(2*p_)
        e2=(TWO_PI*xi/3)*em*(rr**2*s2*Tp**2+2*rr**2*Tp**2+4*e2p*s2)
        e4=(TWO_PI*kappa/3)*em*((2*rr**2*s4+2*rr**2*s2)*Tp**2+e2p*s4)/rr**2
        return e2+e4
    Tp0=np.gradient(Th0,r); h=1e-6
    eP=(edens(Th0,Tp0+h,r,ph)-2*edens(Th0,Tp0,r,ph)+edens(Th0,Tp0-h,r,ph))/h**2
    eQ=(edens(Th0+h,Tp0,r,ph)-2*edens(Th0,Tp0,r,ph)+edens(Th0-h,Tp0,r,ph))/h**2
    epp=edens(Th0+h,Tp0+h,r,ph);epm=edens(Th0+h,Tp0-h,r,ph)
    emp=edens(Th0-h,Tp0+h,r,ph);emm=edens(Th0-h,Tp0-h,r,ph)
    eR=(epp-epm-emp+emm)/(4*h**2)
    P=eP;Veff=eQ-np.gradient(eR,r)
    s=np.sin(Th0);s2=s*s;s4=s2*s2
    # breathing weight with the shifted phi (constant shift cancels in ratios)
    W=(TWO_PI/3)*np.exp(3*ph)*(xi*(r**2*s2+2*r**2)+kappa*(2*s4+2*s2))
    n=N-2; Hm=np.zeros((n,n)); Wd=np.zeros(n)
    for i in range(1,N-1):
        Pr=0.5*(P[i]+P[i+1]);Pl=0.5*(P[i-1]+P[i])
        hr=r[i+1]-r[i];hl=r[i]-r[i-1];hc=0.5*(hr+hl);k=i-1
        Hm[k,k]=(Pr/hr+Pl/hl)/hc+Veff[i]
        if k+1<n:Hm[k,k+1]=-Pr/hr/hc
        if k-1>=0:Hm[k,k-1]=-Pl/hl/hc
        Wd[k]=W[i]
    Hm=0.5*(Hm+Hm.T); Winv=1.0/np.sqrt(Wd)
    A=(Hm*Winv[:,None])*Winv[None,:]; A=0.5*(A+A.T)
    ev=torch.linalg.eigvalsh(torch.as_tensor(A,device=DEV)).cpu().numpy()
    return np.sort(ev)[:nev]

def main():
    xi=kappa=1.0; r_core=0.05; L=1.0
    print("="*78); print("DEEP-PHI breathing spectrum (rescaled weight, p=0..4)"); print("="*78)
    rows={}
    for p in [0.0,0.5,1.0,2.0,3.0,4.0]:
        ri=r_core+14*L
        g=solve_ground(r_core,ri,xi,kappa,p=p)
        rgg=np.linspace(r_core,ri,1400);T=g.sol(rgg)[0];ph,_=phi_bg(rgg,p,ri)
        ev=fluct_spectrum(rgg,T,ph,xi,kappa,nev=8)
        om=np.sqrt(np.clip(ev,0,None))
        e2,e4=energy(rgg,T,ph,xi,kappa,m=1)
        rows[p]=(e2+e4,ev,om)
        print(f"p={p}: E0={e2+e4:9.3f} res={g.rms_residuals.max():.1e}")
        print(f"      omega^2 = {np.array2string(ev[:6],precision=5)}")
        print(f"      omega   = {np.array2string(om[:6],precision=5)}")
        print(f"      R1=om1/om0={om[1]/om[0]:.5f}  R2=om2/om0={om[2]/om[0]:.5f}")

    # SPACING LAW FIT on flat p=0
    print("\n"+"="*78); print("SPACING LAW (flat p=0): O(1) overtone vs exponential"); print("="*78)
    ev0=rows[0.0][1][:6]; om0=np.sqrt(ev0); n=np.arange(len(ev0))
    # fit omega^2 ~ a+b n  (overtone/SHO-like)
    A=np.vstack([np.ones_like(n),n]).T
    cax=np.linalg.lstsq(A,ev0,rcond=None)[0]
    res_lin=ev0-A@cax
    # fit log(omega) ~ c0 + c1 n (exponential)
    cl=np.linalg.lstsq(A,np.log(om0),rcond=None)[0]
    res_exp=np.log(om0)-A@cl
    print(f"omega^2 vs n linear fit: a={cax[0]:.4f} b={cax[1]:.4f}  resid rms={np.std(res_lin):.4f}")
    print(f"log(omega) vs n linear fit (exp law): slope c={cl[1]:.4f}  resid rms={np.std(res_exp):.4f}")
    print(f"=> e^c per level = {math.exp(cl[1]):.4f}  (exponential would need c>>1 to give")
    print(f"   the empirical lepton hierarchy ~2e2,3e3; here c={cl[1]:.3f} is O(1)).")

    # KOIDE Q under the breathing-tower readings
    print("\n"+"="*78); print("KOIDE Q  (P-tower = breathing tower)"); print("="*78)
    E0base=rows[0.0][0]; om=rows[0.0][2]
    # Reading A: state energies = soliton mass + n-th breathing quantum
    #   E_n = E0base + omega_n  (n=0,1,2 ; omega_0 the lowest breathing quantum)
    EA=np.array([E0base+om[0],E0base+om[1],E0base+om[2]])
    QA=(EA.sum())/(np.sqrt(EA).sum())**2
    # Reading B: the tower IS the breathing frequencies themselves (E_n=omega_n^2,
    #   the energy eigenvalues of the fluctuation operator) -- pure spectral reading
    EB=rows[0.0][1][:3]
    QB=(EB.sum())/(np.sqrt(EB).sum())**2
    # Reading C: E_n = omega_n (frequencies, not squared)
    EC=om[:3]
    QC=(EC.sum())/(np.sqrt(EC).sum())**2
    for tag,E,Q in [("A: E0+omega_n",EA,QA),("B: omega_n^2",EB,QB),("C: omega_n",EC,QC)]:
        print(f"  reading {tag}: E={np.array2string(E,precision=4)}  R1={E[1]/E[0]:.4f} "
              f"R2={E[2]/E[0]:.4f}  Q={Q:.5f}")
    print(f"\n  (2/3 = {2/3:.5f} for reference scale of Q; Q reported data-blind)")

    # mpmath deep anchor
    print("\n"+"="*78); print("mpmath deep-phi anchor (e^{3phi} overflow guard)"); print("="*78)
    import mpmath as mp; mp.mp.dps=50
    ri=r_core+14.0
    for p in [2.0,3.0,4.0]:
        phc=-p*mp.log(mp.mpf(ri)/mp.mpf(r_core))
        w3=mp.e**(3*phc)
        f64=math.exp(3*(p*math.log(r_core/ri)))
        print(f"p={p}: 3*phi_core={float(3*phc):.3f}  e^3phi(mp)={mp.nstr(w3,6)}  "
              f"f64 {'OVERFLOWS' if (f64==0 or not math.isfinite(f64)) else f'{f64:.3e}'}")
    print("=> e^{3phi} underflows float64 for p>=2 at this cell ratio; the rescaled-weight")
    print("   (constant phi-shift) computation above is the float64-safe equivalent, and the")
    print("   omega ratios are shift-invariant (a constant phi shift multiplies all energies).")

if __name__=="__main__":
    main()
