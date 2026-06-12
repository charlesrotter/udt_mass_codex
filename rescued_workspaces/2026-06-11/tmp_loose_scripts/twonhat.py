import numpy as np
from scipy.special import sph_harm
from numpy import pi, sqrt
NTH, NPH = 96, 192
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
    up,dn=spinor
    return (v[2]*up+(v[0]-1j*v[1])*dn, (v[0]+1j*v[1])*up-v[2]*dn)
def hv(h): return [sum(h[i,jj]*NHAT[jj] for jj in range(3)) for i in range(3)]

# THE genuinely rank-3 worst case: operator with TWO explicit nhats x H, e.g.
#   nhat_a nhat_b H_{ab} * (sigma.v) or nhat_a H_{ab} sigma_b * (nhat.something).
# Such a term has orbital content up to (nhat nhat) = l in {0,2}. From small comp l=1 this reaches l=3!
# Does ANY first-order gravity vertex actually produce TWO nhats? For h=f(r)H, ONE derivative = ONE nhat.
# The vierbein vertex h_ij alpha^i p^j: p^j can ALSO hit the radial profile -> p^j ~ nhat_j d/dr,
# giving h_ij nhat^j = (h.nhat)_i = v_i : still ONE nhat. p hitting angular part gives angular-momentum
# (no extra nhat as a multiplicative tensor; it's a derivative). So at FIRST ORDER in h there is exactly
# ONE power of h hence at most the nhat's inside h's derivative + the p. Max two orbital units ONLY if
# p ALSO contributes a multiplicative nhat AND h contributes one. Let's test the literal worst case:
H=Hm0()
def op_two_nhat_A(spinor,h):  # (nhat.H.nhat) * (sigma.v)  -- two nhats from H plus v's nhat = THREE? 
    v=hv(h); nHn=sum(NHAT[i]*h[i,j]*NHAT[j] for i in range(3) for j in range(3))
    r=sdv(spinor,v); return (nHn*r[0], nHn*r[1])
def op_two_nhat_B(spinor,h):  # sigma.(H.nhat) with an EXTRA nhat.sigma applied = product two sigmas/two nhats
    r=sdv(spinor,NHAT); return sdv(r,hv(h))
targets=[-1,1,-2,2,-3,3,-4,4,-5]
def reach(op):
    out={}
    for kp in targets:
        Ss=0.0
        for mu in mus(-1):
            T=op(omega(-1,mu),H)
            for mup in mus(kp): Ss+=abs(inner(omega(kp,mup),T))**2
        out[kp]=Ss
    return out
for name,op in [("(n.H.n)(sig.v) [3 nhat]",op_two_nhat_A),("(n.sig)(sig.v) [2 nhat]",op_two_nhat_B)]:
    r=reach(op)
    print(f"{name}: kappa=-4 S={r[-4]:.3e} {'LEAK!' if r[-4]>1e-10 else 'no leak'} ; reach={[k for k in targets if r[k]>1e-12]}")

# And the CRITICAL one: build a literal rank-3 spherical-tensor operator and confirm IT does leak,
# proving the test is sensitive (not a false-negative bug). T^(3) ~ {nhat nhat nhat}_traceless . (stuff)
def op_Y3(spinor,h):  # multiply by a real l=3 harmonic -> MUST reach kappa=-4 from kappa=-1
    f=(Y(3,0)).real
    return (f*spinor[0], f*spinor[1])
r=reach(op_Y3)
print(f"SENSITIVITY: Y_30 scalar (rank-3 orbital): kappa=-4 S={r[-4]:.4f} {'reaches -4 (test IS sensitive)' if r[-4]>1e-6 else 'FALSE NEGATIVE BUG!'}")
