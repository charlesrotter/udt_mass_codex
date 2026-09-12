#!/usr/bin/env python3
"""Source-first original-Christoffel ray offsets; imports no parent science code."""
import json
import platform
import sys
import numpy as np
import scipy
from scipy.integrate import solve_ivp, quad
from scipy.special import jv, yv

k=.75  # PINNED G394
A=-(3*np.pi/4)*yv(0,k)
B=(3*np.pi/4)*jv(0,k)
def ff(t):
    return A*jv(0,k*t)+B*yv(0,k*t),-k*(A*jv(1,k*t)+B*yv(1,k*t))

def metric(t,x,e):
    f,fp=ff(t)
    P=e*f*np.cos(k*x)
    Pt=e*fp*np.cos(k*x)
    Px=-e*k*f*np.sin(k*x)
    L=t*t*(fp*fp+k*k*f*f)/2+t*f*fp/2-9/8
    lam=4*np.log(.75)+e*e*(L+t*f*fp*np.cos(2*k*x)/2)
    a=lam/4-np.log(t)/4
    at=-1/(4*t)+t*(Pt*Pt+Px*Px)/4
    ax=t*Pt*Px/2
    q=np.array([a,a,(np.log(t)+P)/2,(np.log(t)-P)/2])
    qt=np.array([at,at,(1/t+Pt)/2,(1/t-Pt)/2])
    qx=np.array([ax,ax,Px/2,-Px/2])
    return q,qt,qx

def rhs(t,u,e):
    q,qt,qx=metric(t,u[0],e)
    w=np.r_[1.,u[3:6]]
    metric_ratio=np.array([-1.,1.,np.exp(2*(q[2]-q[0])),np.exp(2*(q[3]-q[0]))])
    connection=2*w*(qt+w[1]*qx)
    connection[0]+=np.dot(metric_ratio*w*w,qt)
    connection[1]-=np.dot(metric_ratio*w*w,qx)
    acc=-connection[1:]+w[1:]*connection[0]
    return np.r_[u[3:6],acc,qt[0]+w[1]*qx[0]-connection[0]]

def ray(e,x,s,T):
    initial=np.r_[x,0.,0.,s*np.array([1,.75,.75]),0.]
    sol=solve_ivp(lambda t,u:rhs(t,u,e),(1,T),initial,method='DOP853',
                  rtol=2e-11,atol=2e-13,max_step=.05,dense_output=True)
    assert sol.success,sol.message
    sample=sol.sol(np.linspace(1,T,41)).T
    null=[]
    for t,u in zip(np.linspace(1,T,41),sample):
        q,_,_=metric(t,u[0],e)
        null.append(abs(np.sum(np.exp(2*(q[1:]-q[0])))*0 + np.dot(np.exp(2*(q[1:]-q[0])),u[3:6]**2)-1))
    assert max(null)<2e-8,('null',max(null))
    return sol.y[:,-1],max(null)

def scalar(e,T):
    def f(t,u):
        F,Fp=ff(t)
        rt=-3/(4*t)+e*e*t*Fp*Fp/4-e*Fp/2
        rxx=k*k*e*F*(1-e*t*Fp)/2
        return [u[1],-rt*u[1]-rxx*u[0]]
    sol=solve_ivp(f,(1,T),(0,1),method='DOP853',rtol=2e-12,atol=2e-14,max_step=.025)
    assert sol.success
    return sol.y[0,-1]

def run(case):
    e,x,mu,psi,T=case
    rho=np.sqrt(max(0,1-mu*mu))
    s=np.array([mu,rho*np.cos(psi),rho*np.sin(psi)])
    ref=np.eye(3)[np.argmin(np.abs(s))]
    ea=np.cross(s,ref);ea/=np.linalg.norm(ea)
    eb=np.cross(s,ea)
    source=np.column_stack([ea,eb])
    u,null=ray(e,x,s,T)
    q,_,_=metric(T,u[0],e)
    b=np.exp(q[1:]);n=b*u[3:6]/np.exp(q[0])
    estimates=[]
    for h in [1e-3,5e-4,2.5e-4]:
        columns=[]
        for a in [ea,eb]:
            up,_=ray(e,x,np.cos(h)*s+np.sin(h)*a,T)
            um,_=ray(e,x,np.cos(h)*s-np.sin(h)*a,T)
            columns.append(b*(up[:3]-um[:3])/(2*h))
        estimates.append(np.column_stack(columns))
    extrap=(4*estimates[-1]-estimates[-2])/3
    error=np.linalg.norm(extrap-estimates[-1])/max(1,np.linalg.norm(extrap))
    orth=np.linalg.norm(n@estimates[-1])/max(1,np.linalg.norm(estimates[-1]))
    assert error<2e-5,('derivative',case,error)
    assert orth<2e-5,('orthogonality',case,orth)
    signed=np.linalg.det(np.column_stack([n,extrap]))
    singular=np.linalg.svd(extrap,compute_uv=False)
    result=dict(case=case,sky=s.tolist(),source_basis=source.tolist(),endpoint=u.tolist(),
                physical_variations=extrap.tolist(),h_estimates=[v.tolist() for v in estimates],
                area=abs(signed),signed_area=signed,singular_values=singular.tolist(),
                frequency=np.exp(u[-1]),derivative_error=error,orthogonality=orth,nullness=null)
    if abs(mu)==1:
        widths=[]
        for i in [2,3]:
            integ=quad(lambda t:np.exp(2*(metric(t,x+mu*(t-1),e)[0][0]-metric(t,x+mu*(t-1),e)[0][i])),1,T,epsabs=2e-11,epsrel=2e-11)[0]
            widths.append(np.exp(q[i])*integ/.75)
        result['axial_expected_widths']=widths
        assert np.max(np.abs(np.sort(widths)-np.sort(singular))/np.maximum(1,np.sort(widths)))<2e-5
    if x==0 and mu==0 and (psi==0 or psi==np.pi/2):
        expected=np.exp(q[0])*scalar(e if psi==0 else -e,T)
        # xi source tangent may be first or second basis vector; norm gives invariant component.
        computed=np.linalg.norm(extrap[0,:])
        result['invariant_xi_expected']=expected
        result['invariant_xi_computed']=computed
        assert abs(expected-computed)/max(1,abs(expected))<2e-5
    if e==0:
        freq=np.sqrt(mu*mu*np.sqrt(T)+(1-mu*mu)/T)
        result['background_frequency']=freq
        assert abs(result['frequency']-freq)<2e-8
        # Constant covariant momenta give an independent endpoint Jacobian integral.
        p=s*np.array([.75,1.,1.]);dp=source*np.array([.75,1.,1.])[:,None]
        def derivative(t,j,a):
            N=.75*t**(-.25)
            inv=np.array([1/(N*N),1/t,1/t])
            omega=np.sqrt(np.dot(p*p,inv))
            dom=np.dot(p*inv,dp[:,a])/omega
            return N*inv[j]*(dp[j,a]/omega-p[j]*dom/omega**2)
        independent=np.array([[b[j]*quad(lambda t:derivative(t,j,a),1,T,epsabs=2e-11,epsrel=2e-11)[0] for a in range(2)] for j in range(3)])
        result['background_variations']=independent.tolist()
        assert np.linalg.norm(independent-extrap)/max(1,np.linalg.norm(independent))<2e-5
    return result

cases=[(1/6,.3,.6,0,12),(1/6,.3,-.6,np.pi/2,12),(.5,.7,.6,.7,12),
       (.5,.7,-.6,.7,12),(1,.4,.2,1.1,8),(-.5,.9,-.3,.4,12),
       (.5,0,0,0,12),(.5,0,0,np.pi/2,12),(.5,.3,1,0,12),
       (.5,.3,-1,0,12),(0,.7,.6,.7,12)]
results=[]
for c in cases:
    result=run(c);results.append(result)
    print(json.dumps({'case_completed':c,'area':result['area']}),file=sys.stderr,flush=True)
print(json.dumps(dict(versions=dict(python=sys.version,numpy=np.__version__,scipy=scipy.__version__,platform=platform.platform()),cases=results),indent=2))
