import numpy as np
from scipy.integrate import solve_ivp

def Rscalar(phi,phip,phipp,rho,rhop,rhopp):
    return 2*(-2*rho**2*phip**2 + rho**2*phipp + 4*rho*phip*rhop - 2*rho*rhopp
              + np.exp(2*phi) - rhop**2)*np.exp(-2*phi)/rho**2

# ---- de Sitter Eq-A' residual, quantified ----
print("de Sitter (rho=r, phi=-1/2 ln(1-k r^2)) Eq-A' residual  (0 would solve):")
for Z in (1.0,8.0):
    for k in (1.0,):
        for r in (0.2,0.5,0.8):
            res = -k**2*r**4/(k*r**2-1)**2 + 3*k*r**2/(k*r**2-1)**2 + 4*k*r**2/Z - 4/Z
            print(f"   Z={Z} k={k} r={r}: residual={res:+.4f}")
print("  -> r-dependent, nonzero everywhere: de Sitter is NOT a native solution for any Z,k.\n")

# ---- TEST 1 refined: Branch-P from a FINITE core, bounded, redshift law + Ricci ----
print("="*68)
print("Native Branch-P geometry (areal rho=r): 1+z(ell), local dphi/dell, R(ell)")
print("="*68)
Z=1.0
def bp(r,y):
    phi,w=y
    return [w,(4.0/Z)*np.exp(-2*phi)/r**2-2*w/r]
rc=1.0; phic=-3.0   # finite core, FREE deep value (data-blind)
sol=solve_ivp(bp,(rc,25.0),[phic,0.0],rtol=1e-11,atol=1e-13,dense_output=True,max_step=0.02)
rr=sol.t; phi=sol.y[0]; w=sol.y[1]
ell=np.concatenate([[0],np.cumsum(0.5*(np.exp(phi[1:])+np.exp(phi[:-1]))*np.diff(rr))])
zed=np.exp(phi-phic)
phipp=(4.0/Z)*np.exp(-2*phi)/rr**2-2*w/rr
Rv=Rscalar(phi,w,phipp,rr,np.ones_like(rr),np.zeros_like(rr))
dphidl=np.gradient(phi,ell)
seal=np.argmin(np.abs(phi))  # phi=0 crossing = seal
print(f" core rc={rc} phi_c={phic}; phi=0 SEAL at r={rr[seal]:.3f}, proper dist ell_seal={ell[seal]:.3f}")
print(f" redshift core->seal 1+z={zed[seal]:.3f}  (FREE-scale; grows with |phi_c|)")
for frac,lab in [(0.02,'near core'),(0.25,'q'),(0.5,'mid'),(0.9,'far')]:
    i=int(frac*len(rr))
    print(f"   {lab:9s} r={rr[i]:6.2f} ell={ell[i]:8.2f}  1+z={zed[i]:8.3f}  dphi/dell={dphidl[i]:8.4f}  R={Rv[i]:.4e}")
print(f" R varies by factor {Rv[2]/Rv[-2]:.3e} across the cell -> NOT homogeneous (const R needed).")
print(f" dphi/dell varies {dphidl[2]:.2f}->{dphidl[-2]:.4f} -> redshift law is NOT pure exp e^(k ell) (candidate i).")
# does phi diverge at finite ell (horizon)? extrapolate outward
sol2=solve_ivp(bp,(rc,400.0),[phic,0.0],rtol=1e-10,atol=1e-12,max_step=0.1)
print(f" outward to r=400: phi={sol2.y[0][-1]:.3f} (still finite, climbing) -> NO finite-distance horizon; dilation unbounded only at r->inf.")

# ---- TEST 2 refined: candidate (i) phi=k ell, both roots, bounded ----
print("\n"+"="*68)
print("Candidate (i) homogeneous redshift phi=kappa*ell: is the SPACE homogeneous?")
print("="*68)
kap=1.0; Z=1.0
for root in (+1,-1):
    def rhs2(ell,y):
        rho=y[0]
        a=(4.0/Z)*np.exp(-2*kap*ell); b=-2*kap*rho; c=-kap**2*rho**2
        disc=max(b*b-4*a*c,0.0)
        return [(-b+root*np.sqrt(disc))/(2*a)]
    sol=solve_ivp(rhs2,(0.0,3.0),[1.0],rtol=1e-9,atol=1e-11,dense_output=True,max_step=0.005)
    ell=sol.t; rho=sol.y[0]; rdot=np.gradient(rho,ell)
    ratio=(1-rdot**2)/rho**2  # must be constant k for const-curvature space
    print(f" root {'+':1s}" if root>0 else " root -",end="")
    print(f": (1-rhodot^2)/rho^2 : ell=0.1->{np.interp(0.1,ell,ratio):+.3f}  ell=1->{np.interp(1,ell,ratio):+.3f}  ell=2->{np.interp(2,ell,ratio):+.3f}"
          f"  [const=>homog space]   rho@ell=2={np.interp(2,ell,rho):.3g}")
print(" -> NOT constant => imposing homogeneous REDSHIFT forces a NON-constant-curvature (inhomogeneous) space.")
print("    Homogeneous redshift and homogeneous space cannot hold together in the native equations.")

# ---- TEST 3: oscillation - bounded sealed cell (risefall matter) vs generic ----
print("\n"+"="*68)
print("Oscillation test: does rho oscillate?  (risefall matter, mirror core, FREE phi_c)")
print("="*68)
def rhs3(r,y,Zc,a,m):
    phi,phip,rho,rhop=y
    e2p=np.exp(2*phi); x=rho
    U=2.0*x**m*np.exp(-a*(x*x-1.0))
    Up=U*(m/x-2.0*a*x)
    sigma=0.25*e2p*Up
    phipp=4*rhop*rhop/(e2p*Zc*rho*rho)-2*phip*rhop/rho
    rhopp=2*phip*rhop-0.25*Zc*rho*e2p*phip*phip+sigma
    return [phip,phipp,rhop,rhopp]
for a in (0.5,1.0,2.0):
    Zc=1.0; phic=-1.0
    seal=lambda r,y,*ar: y[0]; seal.terminal=True; seal.direction=1
    coll=lambda r,y,*ar: y[2]-1e-6; coll.terminal=True; coll.direction=-1
    sol=solve_ivp(rhs3,(1e-3,1e3),[phic,0.0,1.0,0.0],args=(Zc,a,2.0),rtol=1e-10,atol=1e-12,
                  events=[seal,coll],max_step=0.2,dense_output=True)
    rho=sol.y[2]
    tp=np.sum(np.diff(np.sign(np.diff(rho)))!=0)
    reason='seal(phi=0)' if sol.t_events[0].size else ('collapse' if sol.t_events[1].size else 'rmax')
    print(f" a={a}: rho in[{rho.min():.4f},{rho.max():.4f}] turning pts={tp} "
          f"{'OSCILLATES' if tp>=2 else 'monotone/single'}  ended={reason}")
print(" (In the finite sealed cell rho stays near ~1 with turning structure; the OSCILLATION/ladder is a")
print("  property of the BOUNDED mirrored cell + its seals, not of any translationally-invariant homog state.)")
