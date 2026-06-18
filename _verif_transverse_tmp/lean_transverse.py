import os
for v in ("OMP_NUM_THREADS","MKL_NUM_THREADS","OPENBLAS_NUM_THREADS","NUMEXPR_NUM_THREADS"):
    os.environ[v]="1"
import numpy as np, sys
sys.path.insert(0,'.')
import lean
from lean import nhat,angderiv,xdot,xcr,SINT,COST,DTH,DPH,Nth,Nph,TG,PG
from lean_rayleigh import BG, S_total, Tweight, mode_isorot_z
from scipy.linalg import eigh

"""
Transverse l-channel operator. Mode field:
   delta(r,th,ph) = psi(r) * [ f_lm(th,ph) e1(th,ph;F(r)) + g_lm(th,ph) e2(...) ]
e1 = (dn0/dF)/|.| (polar tangent), e2 = n0 x e1 (azimuthal tangent).
We assemble the radial generalized eigenproblem H_ab = delta^2 S[psi_a,psi_b],
M_ab = delta^2 T[...], in a finite-element-like radial basis (hat functions on rgrid).
delta^2 S is a symmetric bilinear form; we get it from
   delta^2 S[d] = (1/2) d2/deps2 S[normalize(n0+eps d)]  (a quadratic form Q(d,d))
and polarization: Q(da,db) = (Q(da+db)-Q(da)-Q(db))/... but cheaper: build the
Hessian via second mixed differences. For an eigenproblem we use the basis of
single-shell radial bumps times the angular tangent harmonic; H,M are Nr x Nr.

We compute H[a,b] and M[a,b] via:
   H[a,b] = (1/2)[ Q(e_a+e_b) - Q(e_a) - Q(e_b) ] + diag adjust, where Q(d)=d2S[d].
To keep it cheap and robust we instead directly evaluate the bilinear second
variation using FOUR-point stencil:
   d2S(da,db) = [S(eps da+eps db)-S(eps da)-S(eps db)+S(0)]/eps^2   (mixed second diff)
This is O(Nr^2) S-evaluations -> too many. Instead we use the fact that delta^2 S is
LOCAL in r up to nearest-neighbor (only dn/dr couples shells). So H is TRIDIAGONAL in
the shell basis. We exploit that: compute H[i,i],H[i,i+1] only.
"""

def angular_tangent(F, fang, gang):
    """tangent vector field f*e1+g*e2 over angular grid for scalar F."""
    n0=nhat(F)
    h=1e-6
    d=(nhat(F+h)-nhat(F-h))/(2*h)
    d=d-xdot(d,n0)[...,None]*n0
    nrm=np.sqrt(xdot(d,d))[...,None]
    e1=d/nrm
    e2=xcr(n0,e1)
    f=fang(TG,PG)[...,None]; g=gang(TG,PG)[...,None]
    return f*e1+g*e2

def build_modefield(B, psi, fang, gang):
    """delta[i] = psi[i]*tangent(F[i])"""
    return [psi[i]*angular_tangent(B.F[i], fang, gang) for i in range(B.Nr)]

def channel_operator(B, fang, gang, eps=2e-4):
    """Build tridiagonal H and M (Nr-2 interior shells, Dirichlet) for the channel."""
    Nr=B.Nr; dr=B.dr
    # precompute angular tangent at each shell (unit-amplitude psi=1)
    tang=[angular_tangent(B.F[i],fang,gang) for i in range(Nr)]
    # S as function of a full psi vector (modefield), reuse S_total via deltas list
    def Sfun(psi):
        deltas=[psi[i]*tang[i] for i in range(Nr)]
        return S_total(B,deltas,1.0,+1)  # eps absorbed into psi; use sign+1, eps=1
    # but normalize() is nonlinear; need small amplitude. Use scaled psi.
    # We want the QUADRATIC form. Evaluate S at amplitude a and -a, subtract S0.
    def Q(psi):
        a=eps
        Sp=S_total(B,[psi[i]*tang[i] for i in range(Nr)],a,+1)
        Sm=S_total(B,[psi[i]*tang[i] for i in range(Nr)],a,-1)
        S0=S_total(B,[psi[i]*tang[i] for i in range(Nr)],a,0)
        return (Sp-2*S0+Sm)/a**2
    def Mq(psi):
        deltas=[psi[i]*tang[i] for i in range(Nr)]
        return 2*Tweight(B,deltas)
    # H tridiagonal: H_ii from unit bump e_i; H_i,i+1 from polarization.
    H=np.zeros((Nr,Nr)); M=np.zeros((Nr,Nr))
    Qi=np.zeros(Nr); Mi=np.zeros(Nr)
    for i in range(Nr):
        e=np.zeros(Nr); e[i]=1.0
        Qi[i]=Q(e); Mi[i]=Mq(e)
        H[i,i]=Qi[i]; M[i,i]=Mi[i]
    for i in range(Nr-1):
        e=np.zeros(Nr); e[i]=1.0; e[i+1]=1.0
        Qsum=Q(e); Msum=Mq(e)
        H[i,i+1]=H[i+1,i]=0.5*(Qsum-Qi[i]-Qi[i+1])
        M[i,i+1]=M[i+1,i]=0.5*(Msum-Mi[i]-Mi[i+1])
    return H,M

def solve_channel(B,fang,gang,bc='dirichlet'):
    H,M=channel_operator(B,fang,gang)
    Nr=B.Nr
    if bc=='dirichlet': idx=np.arange(1,Nr-1)
    else: idx=np.arange(Nr)
    Hs=H[np.ix_(idx,idx)]; Ms=M[np.ix_(idx,idx)]
    Ms=0.5*(Ms+Ms.T)+1e-12*np.eye(len(idx)); Hs=0.5*(Hs+Hs.T)
    ev,evec=eigh(Hs,Ms)
    return ev,evec,idx,H,M

# angular harmonics
def Y(l,m):
    if l==1:
        if m==0:  return lambda T,P: np.cos(T)
        if m==1:  return lambda T,P: np.sin(T)*np.cos(P)
        if m==-1: return lambda T,P: np.sin(T)*np.sin(P)
    if l==2:
        if m==0:  return lambda T,P: 3*np.cos(T)**2-1
        if m==1:  return lambda T,P: np.sin(T)*np.cos(T)*np.cos(P)
        if m==-1: return lambda T,P: np.sin(T)*np.cos(T)*np.sin(P)
        if m==2:  return lambda T,P: np.sin(T)**2*np.cos(2*P)
        if m==-2: return lambda T,P: np.sin(T)**2*np.sin(2*P)
    raise ValueError
ZERO=lambda T,P: np.zeros_like(T)

if __name__=='__main__':
    p=0; B=BG(p)
    print("=== l=1 channels, p=0, R=18 ===")
    for name,(f,g) in [('e1*Y10',(Y(1,0),ZERO)),('e2*Y10',(ZERO,Y(1,0))),
                       ('e1*Y11',(Y(1,1),ZERO)),('e2*Y11',(ZERO,Y(1,1)))]:
        ev,*_=solve_channel(B,f,g)
        print(f"  {name}: lowest 5 omega^2 =",np.round(ev[:5],5))
