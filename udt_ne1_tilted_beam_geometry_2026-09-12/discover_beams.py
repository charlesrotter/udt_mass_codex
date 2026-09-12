#!/usr/bin/env python3
"""Full supplied-metric ray derivative; finite floating-point diagnostics only."""
import argparse,itertools,json,math,platform,sys,warnings
import numpy as np
import scipy
from scipy.integrate import solve_ivp,quad
from scipy.special import jv,yv

# SUPPLIED G394 constants and initial normalization, not physical selections.
K=0.75
AA=-3*math.pi*yv(0,K)/4
BB=3*math.pi*jv(0,K)/4

def fields(t,x,eps):
    f=AA*jv(0,K*t)+BB*yv(0,K*t)
    fp=-K*(AA*jv(1,K*t)+BB*yv(1,K*t))
    co,si=np.cos(K*x),np.sin(K*x)
    P=eps*f*co; Pt=eps*fp*co; Px=-eps*K*f*si
    Pxx=-K*K*P; Ptx=-eps*K*fp*si
    ell=eps*eps*(t*t*(fp*fp+K*K*f*f)/2+t*f*fp/2-9/8+t*f*fp*np.cos(2*K*x)/2)
    a=np.log(0.75)-np.log(t)/4+ell/4
    ax=t*Pt*Px/2; axx=t*(Ptx*Px+Pt*Pxx)/2
    lengths=np.array([np.exp(a),np.sqrt(t)*np.exp(P/2),np.sqrt(t)*np.exp(-P/2)])
    A=np.array([1.,np.exp(2*a-P)/t,np.exp(2*a+P)/t])
    lx=np.array([0.,2*ax-Px,2*ax+Px]); lxx=np.array([0.,2*axx-Pxx,2*axx+Pxx])
    return lengths,A,A*lx,A*(lx*lx+lxx)

def flow(t,state,eps,variation=True,mutate=None):
    x=state[:3]; p=state[3:6]
    lengths,A,Ax,Axx=fields(t,x[0],eps)
    h=np.sqrt(np.dot(A,p*p)); q=A*p
    Sx=np.dot(Ax,p*p); Sxx=np.dot(Axx,p*p)
    rhs=np.concatenate((q/h,np.array([-Sx/(2*h),0.,0.])))
    if not variation:return rhs
    Hpp=np.diag(A)/h-np.outer(q,q)/h**3
    Hxp=np.zeros((3,3)); Hxp[0]=Ax*p/h-q*Sx/(2*h**3)
    Hxx=np.zeros((3,3)); Hxx[0,0]=Sxx/(2*h)-Sx*Sx/(4*h**3)
    if mutate=='drop_spatial_hessian':Hxp[:]=0;Hxx[:]=0
    L=np.block([[Hxp.T,Hpp],[-Hxx,-Hxp]])
    return np.concatenate((rhs,(L@state[6:].reshape(6,6)).ravel()))

def screen(s):
    s=np.asarray(s,dtype=float); s=s/np.linalg.norm(s)
    seed=np.eye(3)[np.argmin(np.abs(s))]
    e=seed-s*np.dot(s,seed);e/=np.linalg.norm(e)
    return np.column_stack((e,np.cross(s,e)))

def initial(eps,mu,psi,xe):
    rho=math.sqrt(max(0,1-mu*mu)); s=np.array([mu,rho*math.cos(psi),rho*math.sin(psi)])
    lengths=fields(1.,xe,eps)[0]; p=lengths*s
    return np.r_[xe,0.,0.,p,np.eye(6).ravel()],s,screen(s)

def solve(eps,mu,psi,xe,to=40.,rtol=2e-10,atol=2e-12,step=0.2,mutate=None):
    state,s,E=initial(eps,mu,psi,xe)
    sol=solve_ivp(lambda t,y:flow(t,y,eps,True,mutate),(1.,to),state,method='DOP853',
                  rtol=rtol,atol=atol,max_step=step,dense_output=True)
    if not sol.success:raise RuntimeError(sol.message)
    return sol,s,E

def readout(t,state,eps,E):
    le=fields(1.,0.,eps)[0]; lo=fields(t,state[0],eps)[0]
    p=state[3:6]; w=np.linalg.norm(p/lo); s=p/lo/w
    M=state[6:].reshape(6,6)
    X=lo[:,None]*(M[:3,3:]@(le[:,None]*E))
    D=screen(s).T@X
    signed=float(np.dot(s,np.cross(X[:,0],X[:,1])))
    sym=np.block([[np.zeros((3,3)),np.eye(3)],[-np.eye(3),np.zeros((3,3))]])
    sr=np.linalg.norm(M.T@sym@M-sym,ord=np.inf)
    return {'t':t,'frequency':float(w),'clock_ratio':float(1/w),'signed_area':signed,
            'area':abs(signed),'singular_values':np.linalg.svd(D,compute_uv=False).tolist(),
            'screen_map':D.tolist(),'screen_orthogonality_abs':float(np.max(np.abs(s@X))),
            'screen_orthogonality_scaled':float(np.max(np.abs(s@X))/(1+np.linalg.norm(X))),
            'symplectic_abs':float(sr),'symplectic_scaled':float(sr/(1+np.linalg.norm(M,ord=np.inf)**2)),
            'state':state.tolist()}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--mutate',choices=['drop_spatial_hessian'])
    args=parser.parse_args();records=[];failure=None
    try:
        with warnings.catch_warnings(record=True) as warns:
            warnings.simplefilter('always')
            cases=list(itertools.product((0.,.5,1.),(-.8,0.,.8),(0.,math.pi/4,math.pi/2),(0.,.7)))
            cases+=list(itertools.product((0.,.5),(-1.,1.),(0.,),(.7,)))
            for eps,mu,psi,xe in cases:
                sol,s,E=solve(eps,mu,psi,xe,mutate=args.mutate)
                samples=[readout(t,sol.sol(t),eps,E) for t in (2.,8.,20.,40.)]
                item={'epsilon':eps,'mu':mu,'psi':psi,'source_xi':xe,'nfev':sol.nfev,'samples':samples}
                records.append(item)
                for row in samples:
                    assert row['screen_orthogonality_scaled']<=2e-7,('screen_orthogonality',row['screen_orthogonality_scaled'],item)
                    assert row['symplectic_scaled']<=2e-7,('symplectic',row['symplectic_scaled'])
                if abs(mu)==1:
                    for row in samples:
                        t=row['t'];lo=fields(t,xe+mu*(t-1),eps)[0]
                        expected=[lo[i]/.75*quad(lambda u:fields(u,xe+mu*(u-1),eps)[1][i],1,t,epsabs=1e-10,epsrel=1e-10)[0] for i in (1,2)]
                        err=max(abs(a-b)/(1+abs(b)) for a,b in zip(sorted(row['singular_values']),sorted(expected)))
                        row['axial_width_scaled_error']=err
                        assert err<=2e-6,('axial_width',err)
        status='PASS';warning_text=[str(w.message) for w in warns]
    except Exception as exc:
        status='FAIL';failure=repr(exc);warning_text=[]
    output={'status':status,'scope':'Finite floating-point discovery; no interval certification or whole-sky/no-conjugacy theorem.',
            'versions':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__},
            'dtype':'float64','method':'DOP853','rtol':2e-10,'atol':2e-12,'max_step':.2,'mutation':args.mutate,
            'records':records,'warnings':warning_text,'failure':failure}
    print(json.dumps(output,indent=2,allow_nan=False));return 0 if status=='PASS' else 1
if __name__=='__main__':sys.exit(main())
