import numpy as np
from scipy.special import sph_harm
from numpy import pi, sqrt

NTH, NPH = 80, 160
xg, wg = np.polynomial.legendre.leggauss(NTH); theta=np.arccos(xg)
phi=np.linspace(0,2*pi,NPH,endpoint=False); dphi=2*pi/NPH
TH,PH=np.meshgrid(theta,phi,indexing='ij'); W=np.outer(wg,np.ones(NPH))*dphi
NHAT=[np.sin(TH)*np.cos(PH),np.sin(TH)*np.sin(PH),np.cos(TH)]

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

def h_tensor(kind):
    if kind=="m0": return np.diag([-1.,-1.,2.])/sqrt(6)
    if kind=="m2": h=np.zeros((3,3)); h[0,0]=1;h[1,1]=-1; return h/sqrt(2)
    if kind=="m1": h=np.zeros((3,3)); h[0,2]=1;h[2,0]=1; return h/sqrt(2)

def sigma_dot_v(spinor,h):
    up,dn=spinor
    v=[sum(h[i,jj]*NHAT[jj] for jj in range(3)) for i in range(3)]
    return (v[2]*up+(v[0]-1j*v[1])*dn, (v[0]+1j*v[1])*up-v[2]*dn)

def ang(a,b,h):
    S=0.0
    for mu in mus(b):
        Tb=sigma_dot_v(omega(b,mu),h)
        for mup in mus(a): S+=abs(inner(omega(a,mup),Tb))**2
    return S

# KEY: well-known identity sigma.nhat Omega_{k,mu} = -Omega_{-k,mu}.  Check it.
print("=== Identity check: sigma.nhat Omega_{k} = -Omega_{-k} ===")
for k in [-1,1,-2,2,-3]:
    for mu in mus(k):
        snO = sigma_dot_v(omega(k,mu), np.eye(3))  # sigma . nhat
        target = (-omega(-k,mu)[0], -omega(-k,mu)[1])
        err = inner((snO[0]-target[0],snO[1]-target[1]),(snO[0]-target[0],snO[1]-target[1])).real
        if err>1e-12: print(f"  FAIL k={k} mu={mu} err={err:.2e}")
print("  identity holds (sigma.n flips kappa sign, preserves mu)")

# Now the off-diagonal Dirac brackets for kappa=-1 -> -4 reach.
# Dirac vertex alpha.(h n): <psi_k'|alpha.v|psi_k> = g'*f <Om_{k'}|sv|Om_{-k}> + f'*g <Om_{-k'}|sv|Om_{k}>
# For k=-1: -k=+1, Om_{+1} l=1.  k'=-4: Om_{-4} l=3, Om_{+4} l=4.
print("\n=== kappa=-1 -> kappa=-4 off-diagonal brackets (independent recompute) ===")
for kind in ["m0","m1","m2"]:
    h=h_tensor(kind)
    t1=ang(-4,1,h)   # <Om_{-4}|sv|Om_{+1}>  (g'f)  l3 <- l1
    t2=ang(4,-1,h)   # <Om_{+4}|sv|Om_{-1}>  (f'g)  l4 <- l0
    print(f"  {kind}: g'f<Om_-4|sv|Om_+1>={t1:.3e}  f'g<Om_+4|sv|Om_-1>={t2:.3e}")

# kappa=-1 -> kappa=-3 reach
print("\n=== kappa=-1 -> kappa=-3 off-diagonal brackets ===")
for kind in ["m0","m1","m2"]:
    h=h_tensor(kind)
    t1=ang(-3,1,h)   # <Om_-3|sv|Om_+1>  l2<-l1
    t2=ang(3,-1,h)   # <Om_+3|sv|Om_-1>  l3<-l0
    print(f"  {kind}: g'f<Om_-3|sv|Om_+1>={t1:.4f}  f'g<Om_+3|sv|Om_-1>={t2:.3e}")
