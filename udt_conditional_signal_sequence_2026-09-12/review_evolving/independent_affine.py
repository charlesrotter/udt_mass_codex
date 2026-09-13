#!/usr/bin/env python3
"""Independent full affine metric Hamilton equations; no project science imports."""
import json, sys, time, platform
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.optimize import root, brentq
from scipy.special import jv, yv
import scipy

K=.75
AK=-(3*np.pi/4)*yv(0,K)
BK=(3*np.pi/4)*jv(0,K)
A=np.array([.7,0.,0.]); B=np.array([1.7,1.2,.7])
TMAX=12.

def field(t,x,eps):
    f=AK*jv(0,K*t)+BK*yv(0,K*t)
    fp=-K*(AK*jv(1,K*t)+BK*yv(1,K*t))
    P=eps*f*np.cos(K*x)
    Pt=eps*fp*np.cos(K*x); Px=-eps*K*f*np.sin(K*x)
    LL=.5*t*t*(fp*fp+K*K*f*f)+.5*t*f*fp-9/8
    lam=4*np.log(.75)+eps*eps*(LL+.5*t*f*fp*np.cos(2*K*x))
    N=np.exp(.25*lam)*t**(-.25)
    at=-.25/t+.25*t*(Pt*Pt+Px*Px); ax=.5*t*Pt*Px
    lens=np.array([N,np.sqrt(t*np.exp(P)),np.sqrt(t*np.exp(-P))])
    gi=np.array([-N**-2,N**-2,np.exp(-P)/t,np.exp(P)/t])
    gt=gi*np.array([-2*at,-2*at,-1/t-Pt,-1/t+Pt])
    gx=gi*np.array([-2*ax,-2*ax,-Px,Px])
    return N,lens,gi,gt,gx

def rhs(lam,v,eps):
    _,_,gi,gt,gx=field(v[0],v[1],eps)
    pp=v[4:]**2
    return np.r_[gi*v[4:],-.5*np.dot(gt,pp),-.5*np.dot(gx,pp),0.,0.]

def sky_angles(th,ph):
    return np.array([np.cos(th),np.sin(th)*np.cos(ph),np.sin(th)*np.sin(ph)])

def basis(s):
    a=np.eye(3)[np.argmin(np.abs(s))]
    e=a-s*np.dot(a,s); e=e/np.linalg.norm(e)
    return np.column_stack((e,np.cross(s,e)))

def ray(te,s,to,eps,tol=2e-10,scale=1.):
    N,lens,*_=field(te,A[0],eps)
    y0=np.r_[te,A,scale*np.r_[-N,lens*s]]
    def event(l,v):return v[0]-to
    event.terminal=True; event.direction=1
    sol=solve_ivp(lambda l,v:rhs(l,v,eps),(0.,200./scale),y0,rtol=tol,atol=tol*.01,
                  method='DOP853',events=event)
    if not sol.success or len(sol.t_events[0])!=1: raise RuntimeError('event failure '+sol.message)
    vals=[]
    for v in sol.y.T:
        gi=field(v[0],v[1],eps)[2]; terms=gi*v[4:]**2
        vals.append(abs(np.sum(terms))/np.sum(abs(terms)))
    return sol.y[:,-1],max(vals),float(sol.t[-1]),sol.nfev

def clock(t,x,eps):return quad(lambda u:field(u,x,eps)[0],1.,t,epsabs=2e-12,epsrel=2e-12)[0]
def emission(tau,eps):return 1. if tau==0 else brentq(lambda t:clock(t,A[0],eps)-tau,1.,TMAX,xtol=2e-13)

def endpoint(tau,eps,tol=2e-10,guess=None):
    te=emission(tau,eps)
    if guess is None:
        _,ll,*_=field(te,A[0],eps); d=ll*(B-A); ss=d/np.linalg.norm(d)
        guess=[np.arccos(ss[0]),np.arctan2(ss[2],ss[1]),te+np.linalg.norm(d)/ll[0]]
    def residual(z):
        if not te<z[2]<TMAX: return np.ones(3)*1e3+(z[2]-te)
        return ray(te,sky_angles(*z[:2]),z[2],eps,tol)[0][1:4]-B
    rr=root(residual,guess,tol=1e-9)
    s=sky_angles(*rr.x[:2]); out,cons,span,nfev=ray(te,s,rr.x[2],eps,tol)
    err=float(np.linalg.norm(out[1:4]-B))
    if err>2e-8:raise RuntimeError('endpoint failure '+str((eps,tau,rr.success,rr.message,err)))
    N,ll,*_=field(out[0],out[1],eps); omega=-out[4]/N
    return {'eps':eps,'tau_e':tau,'t_e':te,'t_o':float(out[0]),'tau_o':clock(out[0],B[0],eps),
      'sky_e':s.tolist(),'sky_o':(out[5:]/ll/omega).tolist(),'R':1/omega,
      'p_o':out[4:].tolist(),'endpoint_error':err,'null_constraint':cons,'affine_span':span,
      'root_success':bool(rr.success),'root_message':str(rr.message),'root_x':rr.x.tolist(),'nfev_last':nfev}

def beam(row,eta,tol=2e-10):
    te=row['t_e'];to=row['t_o'];eps=row['eps'];s=np.array(row['sky_e']);ee=basis(s)
    cols=[];res=[]
    for v in ee.T:
        p=s+eta*v;p/=np.linalg.norm(p)
        m=s-eta*v;m/=np.linalg.norm(m)
        yp,rp,*_=ray(te,p,to,eps,tol); ym,rm,*_=ray(te,m,to,eps,tol)
        cols.append((yp[1:4]-ym[1:4])/(2*eta));res.extend((rp,rm))
    N,ll,*_=field(to,B[0],eps)
    XX=ll[:,None]*np.column_stack(cols);so=np.array(row['sky_o']);eo=basis(so)
    DD=eo.T@XX
    return {'eta':eta,'D':DD.tolist(),'widths':np.linalg.svd(DD,compute_uv=False).tolist(),
      'area':float(abs(np.linalg.det(DD))),'transverse_residual':float(np.linalg.norm(so@XX)),
      'endpoint_det':float(abs(np.linalg.det(np.column_stack((np.column_stack(cols),N*so/ll))))),
      'det_from_beam':float(N*abs(np.linalg.det(DD))/np.prod(ll)),
      'null_constraint':max(res)}

def main():
    started=time.time(); rows=[]; checks=[]
    for eps in [-.5,0.,.5]:
        guess=None
        for tau in [0.,.4,.8,1.2]:
            row=endpoint(tau,eps,guess=guess); guess=np.array(row['root_x'])
            guess[2]+=.4/field(row['t_e'],A[0],eps)[0]
            # Every sampled endpoint is independently solved; sky is never kept fixed.
            fine=endpoint(tau,eps,tol=2e-12,guess=row['root_x'])
            row['fine']=fine
            b1=beam(fine,2e-4,tol=2e-12);b2=beam(fine,1e-4,tol=2e-12)
            row['beam_coarse_angle']=b1;row['beam_fine_angle']=b2
            row['beam_relative_difference']=abs(b1['area']/b2['area']-1)
            row['readout_relative_difference']=max(abs(row['R']/fine['R']-1),abs(row['t_o']/fine['t_o']-1))
            d=1e-4
            plus=endpoint(tau+d,eps,tol=2e-12,guess=row['root_x'])
            minus=endpoint(tau-d,eps,tol=2e-12,guess=row['root_x']) if tau>0 else None
            if minus:
                slope=(plus['tau_o']-minus['tau_o'])/(2*d)
            else:
                pp=endpoint(tau+2*d,eps,tol=2e-12,guess=plus['root_x'])
                slope=(-3*fine['tau_o']+4*plus['tau_o']-pp['tau_o'])/(2*d)
            row['clock_finite_difference']=slope
            row['clock_derivative_error']=abs(slope/fine['R']-1)
            # Common affine rescale provides an actual change of parameter, not a rescaled formula.
            rv,rc,_,_=ray(fine['t_e'],np.array(fine['sky_e']),fine['t_o'],eps,tol=2e-12,scale=2.3)
            om=-rv[4]/field(rv[0],rv[1],eps)[0]
            row['affine_scale_R_error']=abs((2.3/om)/fine['R']-1)
            row['affine_scale_endpoint_error']=float(np.linalg.norm(rv[1:4]-B))
            row['pass']=bool(row['beam_relative_difference']<2e-6 and row['clock_derivative_error']<2e-6 and
                            row['readout_relative_difference']<2e-7 and row['null_constraint']<2e-8 and
                            row['endpoint_error']<2e-8 and row['affine_scale_R_error']<2e-8)
            rows.append(row)
            print(json.dumps({'kind':'sample','row':row}),flush=True)
    print(json.dumps({'kind':'summary','all_pass':all(r['pass'] for r in rows),'count':len(rows),
      'elapsed_seconds':time.time()-started,'python':platform.python_version(),'numpy':np.__version__,
      'scipy':scipy.__version__,'equations':'full affine8 canonical geodesic Hamiltonian with analytic original metric first derivatives',
      'no_project_science_imports':True}),flush=True)
    if not all(r['pass'] for r in rows):sys.exit(1)
if __name__=='__main__':main()
