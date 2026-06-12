import numpy as np
from scipy.special import sph_harm
from numpy import pi, sqrt
NTH, NPH = 80, 160
xg, wg = np.polynomial.legendre.leggauss(NTH); theta=np.arccos(xg)
phi=np.linspace(0,2*pi,NPH,endpoint=False); dphi=2*pi/NPH
TH,PH=np.meshgrid(theta,phi,indexing='ij'); W=np.outer(wg,np.ones(NPH))*dphi
nx,ny,nz=np.sin(TH)*np.cos(PH),np.sin(TH)*np.sin(PH),np.cos(TH); NHAT=[nx,ny,nz]
def Y(l,m):
    if l<0 or abs(m)>l: return np.zeros_like(TH,dtype=complex)
    return sph_harm(m,l,PH,TH)
def l_of(k): return k if k>0 else -k-1
def j_of(k): return abs(k)-0.5
def omega(k,mu):
    l=l_of(k); j=j_of(k)
    if abs(mu)>j: z=np.zeros_like(TH,dtype=complex); return (z,z)
    if k<0: a=sqrt((l+mu+0.5)/(2*l+1)); b=sqrt((l-mu+0.5)/(2*l+1))
    else:   a=-sqrt((l-mu+0.5)/(2*l+1)); b=sqrt((l+mu+0.5)/(2*l+1))
    return (a*Y(l,int(mu-0.5)), b*Y(l,int(mu+0.5)))
def mus(k):
    j=j_of(k); return [(-2*j+2*t)/2 for t in range(int(2*j)+1)]
def inner(A,B): return np.sum(np.conj(A[0])*B[0]*W)+np.sum(np.conj(A[1])*B[1]*W)
def Hm0(): return np.diag([-1.,-1.,2.])/sqrt(6)
def sdv(spinor,v):
    up,dn=spinor; return (v[2]*up+(v[0]-1j*v[1])*dn,(v[0]+1j*v[1])*up-v[2]*dn)
def hv(h): return [sum(h[i,jj]*NHAT[jj] for jj in range(3)) for i in range(3)]
H=Hm0()

# ATTACK #4: second insertion of the FULL Dirac vertex -> does kappa=-4 appear?
# vertex maps psi_k -> involves alpha (off-diag). Model: apply sdv twice with intermediate
# small/large swap. Simplest faithful: angular operator (sigma.v) applied twice reaches l up to +2.
def reach2(k0):
    out={}
    for kp in [-1,-2,-3,-4,-5]:
        Ss=0.0
        for mu in mus(k0):
            T=sdv(sdv(omega(k0,mu),hv(H)),hv(H))
            for mup in mus(kp): Ss+=abs(inner(omega(kp,mup),T))**2
        out[kp]=Ss
    return out
r2=reach2(-1)
print("ATTACK #4: TWO insertions of sigma.v from kappa=-1:")
for k in [-1,-2,-3,-4,-5]:
    print(f"  kappa=-1 -> {k:+d}: S2={r2[k]:.4e} {'  <== kappa=-4 REACHED at 2nd order' if k==-4 and r2[k]>1e-8 else ''}")

# ATTACK #3: distinguishability. Compare intrinsic-spin-2 (const H, L=0) vs scalar orbital-L=2.
def scal(k0,kp,Lh,Mh=0):
    YLM=Y(Lh,Mh); S=0.0
    for mu in mus(k0):
        u,d=omega(k0,mu); Tu,Td=YLM*u,YLM*d
        for mup in mus(kp): S+=abs(inner(omega(kp,mup),(Tu,Td)))**2
    return S
print("\nATTACK #3: scalar orbital-L distinguishability from intrinsic spin-2:")
print(f"  scalar L=2: reach -3 S={scal(-1,-3,2):.4f}, -4 S={scal(-1,-4,2):.2e}  -> {'NO -4' if scal(-1,-4,2)<1e-8 else '-4 LEAK'}")
print(f"  scalar L=3: reach -3 S={scal(-1,-3,3):.4f}, -4 S={scal(-1,-4,3):.4f}  -> {'-4 LEAK' if scal(-1,-4,3)>1e-8 else 'no'}")
print("  NOTE: scalar L=2 ALSO gives -3 with no -4. So 'no -4 at first order' is NOT unique to spin-2;")
print("  it is shared by ANY operator whose orbital content is capped at L=2. The spin-2-vs-L=2")
print("  distinction is doing NO work for the no-leak; the cap is purely 'operator rank <= 2 in l'.")

# ATTACK #5: relativistic dependence. The -3 reach uses g'f bracket (small component f).
# In the FULL Dirac vertex the kappa=-3 reach came ONLY from the g'*f term (small comp of source,
# large of target via Om_+1 l=1 -> Om_-3 l=2). If f->0 (non-relativistic), that bracket's PREFACTOR f->0.
print("\nATTACK #5: the kappa=-3 reach is via g'*f <Om_-3|sv|Om_+1> ONLY (the f'g path was zero).")
print("  -> coupling strength ∝ f (small component). For non-relativistic fermion f~(v/c)g -> SUPPRESSED.")
print("  -> the Dj=2 reach to kappa=-3 is O(f); it is O(1) ONLY for relativistic modes (f~g).")
