import os
for v in ("OMP_NUM_THREADS","MKL_NUM_THREADS","OPENBLAS_NUM_THREADS","NUMEXPR_NUM_THREADS"):
    os.environ[v]="1"
import numpy as np, sys
sys.path.insert(0,'.')
import lean
from lean import nhat,angderiv,xdot,xcr,SINT,COST,TG,PG,DTH,DPH
from lean_rayleigh import BG, S_total, Tweight
from lean_solve import solve_profile
from scipy.linalg import eigh

def angular_tangent(F, fang, gang):
    n0=nhat(F); h=1e-6
    d=(nhat(F+h)-nhat(F-h))/(2*h); d=d-xdot(d,n0)[...,None]*n0
    e1=d/np.sqrt(xdot(d,d))[...,None]; e2=xcr(n0,e1)
    return fang(TG,PG)[...,None]*e1 + gang(TG,PG)[...,None]*e2

def channel_op(B, fang, gang, eps=2e-4):
    Nr=B.Nr
    tang=[angular_tangent(B.F[i],fang,gang) for i in range(Nr)]
    def Q(psi):
        deltas=[psi[i]*tang[i] for i in range(Nr)]
        Sp=S_total(B,deltas,eps,+1); Sm=S_total(B,deltas,eps,-1); S0=S_total(B,deltas,eps,0)
        return (Sp-2*S0+Sm)/eps**2
    def Mq(psi):
        return 2*Tweight(B,[psi[i]*tang[i] for i in range(Nr)])
    H=np.zeros((Nr,Nr)); M=np.zeros((Nr,Nr)); Qi=np.zeros(Nr); Mi=np.zeros(Nr)
    for i in range(Nr):
        e=np.zeros(Nr); e[i]=1.0; Qi[i]=Q(e); Mi[i]=Mq(e); H[i,i]=Qi[i]; M[i,i]=Mi[i]
    for i in range(Nr-1):
        e=np.zeros(Nr); e[i]=1.0; e[i+1]=1.0
        H[i,i+1]=H[i+1,i]=0.5*(Q(e)-Qi[i]-Qi[i+1])
        M[i,i+1]=M[i+1,i]=0.5*(Mq(e)-Mi[i]-Mi[i+1])
    return H,M

def lowest(B,fang,gang,bc='dirichlet'):
    H,M=channel_op(B,fang,gang); Nr=B.Nr
    idx=np.arange(1,Nr-1) if bc=='dirichlet' else np.arange(Nr)
    Hs=0.5*(H+H.T)[np.ix_(idx,idx)]; Ms=0.5*(M+M.T)[np.ix_(idx,idx)]+1e-12*np.eye(len(idx))
    ev,_=eigh(Hs,Ms); return ev

def Y(l,m):
    if l==1:
        return {0:lambda T,P:np.cos(T),1:lambda T,P:np.sin(T)*np.cos(P),
                -1:lambda T,P:np.sin(T)*np.sin(P)}[m]
    if l==2:
        return {0:lambda T,P:3*np.cos(T)**2-1,1:lambda T,P:np.sin(T)*np.cos(T)*np.cos(P),
                -1:lambda T,P:np.sin(T)*np.cos(T)*np.sin(P),2:lambda T,P:np.sin(T)**2*np.cos(2*P),
                -2:lambda T,P:np.sin(T)**2*np.sin(2*P)}[m]
ZERO=lambda T,P:np.zeros_like(T)

def channel_min(B,l):
    """min over m and over e1/e2 tangent of the lowest Dirichlet eigenvalue."""
    ms=range(-l,l+1); best=np.inf; rows=[]
    for m in ms:
        for tag,(f,g) in [('e1',(Y(l,m),ZERO)),('e2',(ZERO,Y(l,m)))]:
            ev=lowest(B,f,g); rows.append((m,tag,ev[0]))
            best=min(best,ev[0])
    return best,rows

if __name__=='__main__':
    import json
    out={}
    for p in (0,1,2):
        B=BG(p)
        l1,rows1=channel_min(B,1)
        l2,rows2=channel_min(B,2)
        print(f"\np={p} R=18:")
        print(f"  l=1 lowest non-Goldstone omega^2 = {l1:.5f}")
        for m,tag,e in rows1: print(f"      m={m:+d} {tag}: {e:.5f}")
        print(f"  l=2 lowest non-Goldstone omega^2 = {l2:.5f}")
        for m,tag,e in rows2: print(f"      m={m:+d} {tag}: {e:.5f}")
        out[p]={'l1':l1,'l2':l2}
    print("\nSUMMARY", json.dumps({str(k):v for k,v in out.items()}))
