#!/usr/bin/env python3
"""Independent full null-geodesic finite-difference route; no parent imports."""
import json, math, platform
import numpy as np
import scipy
from scipy.special import jv,yv,jvp,yvp
from scipy.integrate import quad,solve_ivp

kap=0.75 # supplied G394 normalization
aa=-3*math.pi/4*yv(0,kap); bb=3*math.pi/4*jv(0,kap)

def metric(t,x,eps):
    f=aa*jv(0,kap*t)+bb*yv(0,kap*t)
    fp=kap*(aa*jvp(0,kap*t)+bb*yvp(0,kap*t))
    p=eps*f*math.cos(kap*x)
    pt=eps*fp*math.cos(kap*x); px=-eps*kap*f*math.sin(kap*x)
    lag=4*math.log(0.75)+eps**2*(t*t*(fp*fp+kap*kap*f*f)/2+t*f*fp/2-9/8+t*f*fp*math.cos(2*kap*x)/2)
    n2=math.exp(lag/2)/math.sqrt(t)
    gt=np.array([-n2,n2,t*math.exp(p),t*math.exp(-p)])
    # These first derivatives are NE1's exact constraints, verified by G394;
    # the connection below is rebuilt from the metric, not a Jacobi tide.
    nt=(t*(pt*pt+px*px)-1/t)/2; nx=t*pt*px
    dg=np.zeros((4,4))
    dg[0]=gt*np.array([nt,nt,1/t+pt,1/t-pt])
    dg[1]=gt*np.array([nx,nx,px,-px])
    return gt,dg

def connection(gt,dg):
    G=np.zeros((4,4,4))
    for i in range(4):
        for j in range(4):
            for k in range(4):
                G[i,j,k]=((dg[j,i] if i==k else 0)+(dg[k,i] if i==j else 0)-(dg[i,j] if j==k else 0))/(2*gt[i])
    return G

cases=[(0,.4,.3,1,.6),(1/6,.4,.3,-1,.6),(-.5,1.4,-.7,1,1.1),(1.2,1.4,.2,-1,.8),(.5,2,.7,-1,2),(-1/6,3,-1.2,1,.9)]
records=[];maxnull=0.;maxcenter=0.;maxclock=0.;maxfine=0.
for eps,te,xe,sgn,leg in cases:
    tr=te+leg; xr=xe+sgn*leg
    ge,_=metric(te,xe,eps);gr,_=metric(tr,xr,eps)
    ne=math.sqrt(-ge[0]);nr=math.sqrt(-gr[0])
    def central(u):return metric(u,xe+sgn*(u-te),eps)[0]
    affine=quad(lambda u:-central(u)[0]/ne,te,tr,epsabs=2e-12,epsrel=2e-12)[0]
    expected=np.array([math.sqrt(ge[i]*gr[i])/ne*quad(lambda u:-central(u)[0]/central(u)[i],te,tr,epsabs=2e-12,epsrel=2e-12)[0] for i in (2,3)])
    def rhs(v,Y):
        gt,dg=metric(Y[0],Y[1],eps);G=connection(gt,dg)
        return np.concatenate((Y[4:],-np.einsum('ijk,j,k->i',G,Y[4:],Y[4:])))
    def integrate(axis,angle):
        K=np.array([1/ne,sgn*math.cos(angle)/ne,0.,0.])
        if axis is not None:K[axis]=math.sin(angle)/math.sqrt(ge[axis])
        ini=np.concatenate(([te,xe,0.,0.],K))
        sol=solve_ivp(rhs,(0,affine),ini,method='DOP853',rtol=2e-12,atol=2e-13)
        assert sol.success,sol.message
        end=sol.y[:,-1]; gt,_=metric(end[0],end[1],eps)
        null=abs(np.dot(gt,end[4:]**2))/max(1.,np.dot(abs(gt),end[4:]**2))
        assert null<2e-9,('null residual',null)
        return end,null
    center,cn=integrate(None,0.)
    cerr=max(abs(center[0]-tr)/max(1.,abs(tr)),abs(center[1]-xr)/max(1.,abs(xr)))
    assert cerr<2e-10,('central endpoint',cerr)
    errors=[]
    for delta in (.002,.001,.0005):
        vals=[]
        for j,axis in enumerate((2,3)):
            end,nu=integrate(axis,delta);maxnull=max(maxnull,nu)
            vals.append(math.sqrt(gr[axis])*end[axis]/delta)
        error=max(abs(np.array(vals)-expected)/np.maximum(1.,abs(expected)))
        errors.append(float(error))
    assert errors[-1]<2e-6,('full geodesic differential',errors)
    if errors[0]>1e-8:assert errors[0]/errors[-1]>8,('second order sky difference',errors)
    dt=1e-5
    clock_n=quad(lambda u:math.sqrt(-metric(u,xr,eps)[0][0]),tr-dt,tr+dt,epsabs=1e-15,epsrel=2e-12)[0]
    clock_d=quad(lambda u:math.sqrt(-metric(u,xe,eps)[0][0]),te-dt,te+dt,epsabs=1e-15,epsrel=2e-12)[0]
    clock=clock_n/clock_d
    clkerr=abs(clock-nr/ne)/max(1.,abs(nr/ne))
    assert clkerr<2e-9,('proper-time clock differential',clkerr)
    maxcenter=max(maxcenter,cerr);maxclock=max(maxclock,clkerr);maxfine=max(maxfine,errors[-1])
    records.append({'case':{'epsilon':eps,'te':te,'xe':xe,'sign':sgn,'length':leg},'affine_endpoint':affine,'quadrature_screen_map':expected.tolist(),'full_geodesic_differential_errors':errors,'coarse_to_fine_reduction':errors[0]/errors[-1],'clock_from_proper_intervals':clock,'clock_from_endpoints':nr/ne,'clock_scaled_error':clkerr,'central_endpoint_error':cerr})
print(json.dumps({'verdict':'PASS','method':'full 8D perturbed null geodesics vs screen quadrature; proper-time interval ratio vs clock endpoint formula','python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,'shape':{'cases':len(cases),'screen_axes':2,'angle_offsets':3,'geodesic_state_dimension':8},'max_null_scaled_residual':maxnull,'max_central_endpoint_error':maxcenter,'max_clock_scaled_error':maxclock,'max_finest_screen_scaled_error':maxfine,'records':records},indent=2,sort_keys=True))
