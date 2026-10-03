"""Actual PSW clock observations in supplied flat-spatial homogeneous metrics.

This module never supplies curvature to the estimator. Rotational/translational
isometries reduce the number of distinct forward solves; duplicated labels are
explicitly marked. All geometry/parameter values are FREE diagnostic controls.
"""
import math
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from numpy.polynomial.legendre import leggauss

class Geometry:
    def __init__(self, kind, fine=False):
        self.kind=kind; self.fine=fine; self.calls=0
        self.rtol=3e-14 if fine else 2e-12
        self.atol=3e-16 if fine else 2e-14
        self.nodes,self.weights=leggauss(32 if fine else 16)
        self.domain=(-1.5,1.5)
        if kind=='quadratic':
            # CONDITIONAL ERC1 equation, alpha=1,Lambda=0,P0=.3; no scale calibration.
            def rhs(t,y):
                H,R,P,a=y
                return [R/6-2*H*H,P,-3*H*P-R/6,a*H]
            self.sol=[]
            for end in [-1.5,1.5]:
                s=solve_ivp(rhs,(0.,end),[0.,0.,.3,1.],method='DOP853',
                    rtol=self.rtol,atol=self.atol,max_step=.01 if fine else .02,dense_output=True)
                if not s.success:raise RuntimeError(s.message)
                self.sol.append(s.sol)
    def state(self,t):
        q=np.asarray(t); assert np.all(q>=self.domain[0]) and np.all(q<=self.domain[1])
        if self.kind=='quadratic':
            if q.ndim==0:return self.sol[int(q>=0)](q)
            out=np.empty((4,)+q.shape)
            for side in [0,1]:
                mask=(q>=0) if side else (q<0)
                if np.any(mask):out[:,mask]=self.sol[side](q[mask])
            return out
        if self.kind=='flat':a=np.ones_like(q);H=np.zeros_like(q);R=H;P=H
        elif self.kind=='scalar_false_pass':
            a=np.sqrt(1+.4*q);H=.2/(1+.4*q);R=np.zeros_like(q);P=R
        elif self.kind=='cubic_control':
            a=1+.03*q**3;H=.09*q*q/a;R=6*(.18*q/a+H*H);P=np.zeros_like(q)
        else:raise ValueError(self.kind)
        return np.array([H,R,P,a])
    def ah(self,t):
        y=self.state(t)
        return y[3],y[0]
    def integral(self,fun,lo,hi):
        mid=(lo+hi)/2;half=(hi-lo)/2
        return half*np.dot(self.weights,fun(mid+half*self.nodes))
    def prep(self,t0,L,v,direction):
        """Exp(L N), transporting U along that same unit spacelike geodesic."""
        a0=float(self.ah(t0)[0]);gamma=1/math.sqrt(1-v*v)
        U=np.array([gamma,gamma*v/a0,0.,0.])
        N=np.array([gamma*v,gamma/a0,0.,0.]) if direction==0 else np.array([0.,0.,1/a0,0.])
        init=np.r_[t0,np.zeros(3),N,U]
        def rhs(s,y):
            t=y[0];V=y[4:8];u=y[8:12];a,H=self.ah(t)
            return np.r_[V,-a*a*H*np.dot(V[1:],V[1:]),-2*H*V[0]*V[1:],
                          -a*a*H*np.dot(V[1:],u[1:]),-H*(V[0]*u[1:]+u[0]*V[1:])]
        sol=solve_ivp(rhs,(0.,L),init,method='DOP853',rtol=self.rtol,atol=self.atol,max_step=L/4)
        if not sol.success:raise RuntimeError(sol.message)
        y=sol.y[:,-1];a=float(self.ah(y[0])[0]);dot=lambda V,W:-V[0]*W[0]+a*a*np.dot(V[1:],W[1:])
        errs=[abs(dot(y[4:8],y[4:8])-1),abs(dot(y[8:12],y[8:12])+1),abs(dot(y[4:8],y[8:12]))]
        if max(errs)>2e-10:raise RuntimeError(('PREPARATION_NORM',errs))
        return y,errs
    def moving(self,t,tstart,xstart,K):
        k2=float(np.dot(K,K))
        dist=self.integral(lambda q:1/(self.ah(q)[0]**2*np.sqrt(1+k2/self.ah(q)[0]**2)),tstart,t)
        a=float(self.ah(t)[0]);u=np.r_[math.sqrt(1+k2/a**2),K/a**2]
        return xstart+K*dist,u
    def observe(self,t0,L,v,direction,emission_offset=0.):
        self.calls+=1
        if self.calls>100000:raise RuntimeError('FINITE_QUERY_BUDGET')
        y,errs=self.prep(t0,L,v,direction)
        tb0=float(y[0]);xb0=y[1:4];ab0=float(self.ah(tb0)[0]);Kb=ab0*ab0*y[9:12]
        a0=float(self.ah(t0)[0]);gamma=1/math.sqrt(1-v*v);Ka=np.array([a0*gamma*v,0.,0.])
        # Optional emitter coordinate-time offset for an exposed nearby-emission check.
        te=t0+emission_offset;xe,ue=self.moving(te,t0,np.zeros(3),Ka)
        def incidence(t):
            xb,ub=self.moving(t,tb0,xb0,Kb)
            return self.integral(lambda q:1/self.ah(q)[0],te,t)-np.linalg.norm(xb-xe)
        lo=te;hi=te+4*L*(1+v)/(1-v)
        if hi>=self.domain[1]:raise RuntimeError('CLOCK_DOMAIN')
        if not incidence(lo)<0<incidence(hi):raise RuntimeError('NO_REGULAR_BRACKET')
        tr=brentq(incidence,lo,hi,xtol=5e-15 if self.fine else 5e-14,rtol=1e-14,maxiter=100)
        if tr<=tb0:raise RuntimeError('RECEIVER_BEFORE_PREPARATION')
        xr,ur=self.moving(tr,tb0,xb0,Kb);n=(xr-xe)/np.linalg.norm(xr-xe)
        ae=float(self.ah(te)[0]);ar=float(self.ah(tr)[0])
        we=ue[0]/ae-n@ue[1:];wr=ur[0]/ar-n@ur[1:]
        if min(we,wr)<=0:raise RuntimeError('FREQUENCY_SIGN')
        # log1p reduces subtraction error at tiny shifts.
        logp=math.log1p((we-wr)/wr)
        resid=abs(incidence(tr))
        if resid>2e-11:raise RuntimeError(('NULL_RESIDUAL',resid))
        return dict(log_p=logp,arrival=tr,emission=te,prep_time=tb0,
                    norm_error=max(errs),null_residual=resid,
                    receiver_K=Kb.tolist(),receiver_initial_x=xb0.tolist(),
                    unique_forward_kind='rest' if v==0 else ('boost_long' if direction==0 else 'boost_trans'))
    def spatial_site_time(self,t0,h):
        # A comoving spatial geodesic has equal final time for +/- every axis.
        return float(self.prep(t0,h,0.,0)[0][0])

def clock_triplet(g,t,L,v):
    return [g.observe(t,L,0.,0),g.observe(t,L,v,0),g.observe(t,L,v,1)]

def expand_frames(values):
    """21 ideal records represented by 3 unique solves using exact isometries."""
    out=[]
    for frame in range(7):
        for direction in range(3):
            k=0 if frame==0 else (1 if direction==0 else 2)
            out.append({'frame':frame,'direction':direction,**values[k]})
    return out
