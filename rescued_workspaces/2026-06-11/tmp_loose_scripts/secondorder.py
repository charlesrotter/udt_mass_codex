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
def ang(a,b):  # <Om_a|sv|Om_b>^2 summed
    S=0.0
    for mu in mus(b):
        T=sdv(omega(b,mu),hv(H))
        for mup in mus(a): S+=abs(inner(omega(a,mup),T))**2
    return S
# Full Dirac off-diagonal channel rule: k->k' open if ang(k',-k) or ang(-k',k) nonzero.
def chan(kp,k): return ang(kp,-k)>1e-12 or ang(-kp,k)>1e-12
# Second order: k=-1 -> intermediate m -> -4. Enumerate reachable m, then m->-4.
KS=[-1,1,-2,2,-3,3,-4,4,-5]
inter=[m for m in KS if chan(m,-1)]
print("First-order reach from kappa=-1:", inter)
to4=[m for m in inter if chan(-4,m)]
print("Of those, which reach kappa=-4 at the SECOND step:", to4)
print(f"=> kappa=-4 reachable at SECOND order via {to4}: {'YES' if to4 else 'NO'}")

print("\nWhere do the first-order intermediates reach (full Dirac rule)?")
for m in inter:
    rr=[kp for kp in KS if chan(kp,m)]
    print(f"  kappa={m:+d} -> {rr}")
print("\nNOTE on the author's da_discharge_i.py CHECK(3): it used the DIAGONAL sigma.v twice")
print("(not the off-diagonal Dirac vertex) and reported kappa=-4 S2=2.1e-33 = ZERO too.")
print("So NEITHER script actually demonstrates a 2nd-order kappa=-4 leak. The claim's framing")
print("'a SECOND insertion reaches kappa=-4 (=assumption ii)' is NOT supported by the evidence.")
