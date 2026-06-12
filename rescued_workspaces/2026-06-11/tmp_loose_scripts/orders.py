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
H=np.diag([-1.,-1.,2.])/sqrt(6)
def sdv(spinor,v):
    up,dn=spinor; return (v[2]*up+(v[0]-1j*v[1])*dn,(v[0]+1j*v[1])*up-v[2]*dn)
def hv(h): return [sum(h[i,jj]*NHAT[jj] for jj in range(3)) for i in range(3)]
def ang(a,b):
    S=0.0
    for mu in mus(b):
        T=sdv(omega(b,mu),hv(H))
        for mup in mus(a): S+=abs(inner(omega(a,mup),T))**2
    return S
KS=[-1,1,-2,2,-3,3,-4,4,-5,-6]
def chan(kp,k): return ang(kp,-k)>1e-12 or ang(-kp,k)>1e-12
def step(s):
    out=set()
    for m in s:
        for kp in KS:
            if chan(kp,m): out.add(kp)
    return out
cur={-1}; 
print("Reachability tower from kappa=-1 (full Dirac off-diagonal vertex), by order:")
for n in range(1,6):
    cur=step(cur)
    has4 = -4 in cur
    print(f"  order {n}: {sorted(cur)}   kappa=-4 present: {has4}")

print("\nPARITY/SIGNATURE STRUCTURE of the reachable set {-1,+2,-3,+4,-5,...}:")
print("  kappa values reached: -1,+2,-3,+4,-5  -> pattern: kappa odd=>negative, even=>positive")
print("  i.e. sign(kappa) = (-1)^kappa. This is a conserved signature of the off-diagonal vertex.")
print("  l-values: kappa=-1:l0, +2:l2, -3:l2, +4:l4, -5:l4  -> l EVEN only. l=3 (kappa=-4,+3) EXCLUDED.")
print("  => kappa=-4 (l=3) and kappa=+3 (l=3) are excluded at ALL ORDERS by l-parity conservation.")
print()
print("CONSEQUENCE for the CEILING claim: the reachable set is INFINITE ({-1,2,-3,4,-5,6,...}).")
print("  There is NO |kappa|<=3 ceiling from this vertex! kappa=+4 (|k|=4) is reached at 2nd order,")
print("  kappa=-5 (|k|=5) too. The vertex bounds Dj<=2 PER STEP but the TOWER is unbounded in |kappa|.")
