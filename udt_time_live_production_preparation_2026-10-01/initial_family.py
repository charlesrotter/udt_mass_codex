"""Supplied TT families in the unchanged conditional conformal CMC arena.

The positive Newton-CG solve is adapted from the fixed TDS1 initial_data.py;
only the explicitly supplied TT mode list is generalized. No physics selector.
"""
import argparse, io, json, sys
from pathlib import Path
import numpy as np
from scipy.sparse.linalg import LinearOperator, cg

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'udt_three_spatial_smoke_2026-10-01'))
from initial_data import frequencies, gradient, exact_control

def tt_tensor(k, matrix):
    k=np.asarray(k,dtype=float);s=np.asarray(matrix,dtype=float)
    if k.shape!=(3,) or s.shape!=(3,3) or not np.isfinite(k).all() or not np.isfinite(s).all() or np.dot(k,k)==0:
        raise ValueError('INVALID_TT_INPUT')
    if not np.array_equal(k,np.rint(k)) or not np.allclose(s,s.T,rtol=0,atol=1e-14):raise ValueError('INVALID_MODE')
    p=np.eye(3)-np.outer(k,k)/np.dot(k,k);t=p@s@p;t-=np.trace(t)*p/2
    norm=np.linalg.norm(t)
    if norm<1e-12:raise ValueError('DEGENERATE_POLARIZATION')
    return t*np.sqrt(2)/norm

def construct(n, modes, period=2*np.pi, tau=-1.):
    if type(n)!=int or n<8 or n>64 or n%2:raise ValueError('INVALID_GRID')
    if not np.isfinite(period) or period<=0 or not np.isfinite(tau) or tau==0:raise ValueError('INVALID_CMC_DOMAIN')
    x=np.meshgrid(*([np.arange(n)*period/n]*3),indexing='ij')
    seed=np.broadcast_to(np.diag([2/3,-1/3,-1/3]),(n,n,n,3,3)).copy()
    for mode in modes:
        k=np.asarray(mode['k']);a=float(mode['amplitude']);phase=float(mode['phase'])
        tensor=tt_tensor(k,mode['matrix'])
        if np.max(abs(k))>=n/2 or not np.isfinite(a) or not np.isfinite(phase):raise ValueError('UNRESOLVED_OR_INVALID_MODE')
        angle=2*np.pi*sum(k[i]*x[i] for i in range(3))/period+phase
        seed+=a*np.cos(angle)[...,None,None]*tensor
    a2=np.einsum('...ij,...ij->...',seed,seed);freq=frequencies(n,period);k2=sum(k*k for k in freq)
    def lap(a):return np.fft.ifftn(-k2*np.fft.fftn(a)).real
    def residual(p):return -8*lap(p)-a2*p**(-7)+(2/3)*tau*tau*p**5
    psi=np.full((n,n,n),(a2.mean()/((2/3)*tau*tau))**(1/12));history=[]
    for iteration in range(25):
        r=residual(psi);err=float(np.max(np.abs(r)));history.append(err)
        if err<1e-11:break
        potential=7*a2*psi**(-8)+(10/3)*tau*tau*psi**4
        op=LinearOperator((n**3,n**3),matvec=lambda z:(-8*lap(z.reshape(psi.shape))+potential*z.reshape(psi.shape)).ravel(),dtype=float)
        pre=LinearOperator(op.shape,matvec=lambda z:np.fft.ifftn(np.fft.fftn(z.reshape(psi.shape))/(8*k2+potential.mean())).real.ravel(),dtype=float)
        delta,info=cg(op,-r.ravel(),M=pre,rtol=1e-12,atol=1e-14,maxiter=250)
        if info:raise RuntimeError(('CONSTRAINT_LINEAR_SOLVE',info))
        scale=1.
        for backtrack in range(20):
            trial=psi+scale*delta.reshape(psi.shape)
            if trial.min()>0 and np.max(np.abs(residual(trial)))<err:break
            scale*=.5
        else:raise RuntimeError('CONSTRAINT_LINE_SEARCH')
        psi=trial
    else:raise RuntimeError(('CONSTRAINT_NONCONVERGENCE',history))
    gamma=psi[...,None,None]**4*np.eye(3);extrinsic=psi[...,None,None]**(-2)*seed+(tau/3)*gamma
    g=np.zeros((n,n,n,4,4));v=np.zeros_like(g);g[...,0,0]=-1.;g[...,1:,1:]=gamma;v[...,1:,1:]=-2*extrinsic;v[...,0,0]=2*tau
    for i,d in enumerate(gradient(np.log(psi),freq)):v[...,0,i+1]=v[...,i+1,0]=-2*d
    return dict(g=g,v=v,gamma=gamma,K=extrinsic,psi=psi,seed=seed,period=np.array(period),tau=np.array(tau),modes_json=np.array(json.dumps(modes,sort_keys=True)),constraint_history=np.array(history))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('family');ap.add_argument('output');ap.add_argument('--n',type=int,required=True);args=ap.parse_args()
    family=json.loads(Path(args.family).read_text())
    if family.get('control')=='kasner':
        g,v,_=exact_control('kasner',args.n,0);data=dict(g=g,v=v,period=np.array(2*np.pi),control=np.array('kasner'))
    else:data=construct(args.n,family['modes'])
    buf=io.BytesIO();np.savez_compressed(buf,**data)
    with Path(args.output).open('xb') as f:f.write(buf.getvalue())
    print(json.dumps({'n':args.n,'output':args.output,'family':family,'residual_history':data.get('constraint_history',np.array([])).tolist()}))
