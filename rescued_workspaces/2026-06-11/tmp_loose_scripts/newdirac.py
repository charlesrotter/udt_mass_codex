#!/usr/bin/env python3
"""
da_discharge_i_dirac.py — CORRECTED discharge of (i): use the REAL Dirac vertex structure.

The fermion-graviton vertex is  H_int = h_ij alpha^i p^j  (alpha = Dirac, OFF-DIAGONAL in
large/small components).  alpha^i = [[0, sigma^i],[sigma^i, 0]] connects UPPER(channel k') to
LOWER(channel k) and vice versa.  Dirac spinor:  psi_k = ( g(r) Omega_{+k} ; i f(r) Omega_{-k} ).
So  <psi_{k'}| alpha.(h.nhat) |psi_k>  ∝  g'* f <Omega_{k'}|sigma.v|Omega_{-k}>
                                        + f'* g <Omega_{-k'}|sigma.v|Omega_{+k}>,   v = h.nhat.

A CHANNEL coupling k->k' is OPEN iff EITHER angular bracket is nonzero (generic radial weights).
This is the single-particle operator test of (i): does a FIRST-ORDER intrinsic-spin-2 vertex take
the GROUND channel k=-1 to |k|=3 (Dj=2), and is k=-4 (Dj=3) forbidden?  NO two-body addition.
"""
import numpy as np
from scipy.special import sph_harm
from numpy import pi, sqrt

NTH, NPH = 64, 128
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

def ang(a,b,h):   # sum_mu |<Omega_a| sigma.v |Omega_b>|^2  over matching mu
    S=0.0
    for mu in mus(b):
        Tb=sigma_dot_v(omega(b,mu),h)
        for mup in mus(a): S+=abs(inner(omega(a,mup),Tb))**2
    return S

def dirac_channel(kp,k,h):
    """OPEN if either Dirac off-diagonal angular bracket is nonzero."""
    t1=ang(kp,-k,h)     # <Omega_{k'} | sv | Omega_{-k}>   (g'* f)
    t2=ang(-kp,k,h)     # <Omega_{-k'}| sv | Omega_{+k}>   (f'* g)
    return t1,t2

if __name__ == "__main__":
    print("="*78)
    print("CORRECTED (i): FIRST-ORDER intrinsic-spin-2 Dirac vertex, channel selection rule")
    print("  psi_k=(g Om_{+k}; i f Om_{-k});  vertex alpha.(h.nhat);  OPEN if g'f or f'g term nonzero")
    print("="*78)
    KS=[-1,1,-2,2,-3,3,-4,4,-5]
    for kind in ["m0","m2","m1"]:
        h=h_tensor(kind)
        print(f"\n--- h='{kind}' --- from GROUND channel kappa=-1 (j=1/2):")
        for kp in KS:
            t1,t2=dirac_channel(kp,-1,h)
            open_ = abs(t1)>1e-12 or abs(t2)>1e-12
            dj=j_of(kp)-0.5
            tag=""
            if kp==-4: tag="  <== kappa=-4 (Dj=3) LEAK TEST"
            if open_ or kp==-4:
                via=[]
                if abs(t1)>1e-12: via.append(f"g'f:<{kp}|sv|{-(-1)}>={t1:.3f}")
                if abs(t2)>1e-12: via.append(f"f'g:<{-kp}|sv|{-1}>={t2:.3f}")
                state="OPEN " if open_ else "CLOSED"
                print(f"    kappa=-1 -> {kp:+d} (j={j_of(kp)},Dj={dj:+.0f}): {state} {'; '.join(via) if via else '(both zero)'}{tag}")
    
    print("\n"+"="*78)
    print("FULL first-order channel map (which kappa' each kappa reaches):")
    print("="*78)
    h=h_tensor("m0")
    for k0 in [-1,1,-2,2,-3,-4]:
        reach=[kp for kp in KS if (lambda t:abs(t[0])>1e-12 or abs(t[1])>1e-12)(dirac_channel(kp,k0,h))]
        djs=[j_of(kp)-j_of(k0) for kp in reach]
        djmax=max(abs(d) for d in djs) if reach else 0
        print(f"  kappa={k0:+d} (j={j_of(k0)}) -> {reach}   max|Dj|={djmax:.0f}")
    
    print("\n"+"="*78)
    print("VERDICT")
    print("="*78)
    t1,t2=dirac_channel(-3,-1,h); reach3 = abs(t1)>1e-12 or abs(t2)>1e-12
    l1,l2=dirac_channel(-4,-1,h); leak4 = abs(l1)>1e-12 or abs(l2)>1e-12
    print(f"  kappa=-1 -> kappa=-3 (Dj=2) at FIRST ORDER: {'OPEN (reaches |k|=3)' if reach3 else 'CLOSED'}")
    print(f"  kappa=-1 -> kappa=-4 (Dj=3) at FIRST ORDER: {'OPEN -- LEAK!' if leak4 else 'FORBIDDEN (no leak)'}")
    print(f"  => assumption (i) {'HOLDS' if (reach3 and not leak4) else 'FAILS'} for the ground channel at first order.")
