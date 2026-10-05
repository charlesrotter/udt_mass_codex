"""Frozen independent original-metric checks; imports no parent package code."""
import json, math, platform, time
from pathlib import Path
import numpy as np
import scipy
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq
import sympy as sp

OUT=Path(__file__).parent
started=time.time()
u,r,t,p=sp.symbols('u r theta phi', real=True)
m,H=sp.symbols('m H',positive=True)
xx=[u,r,t,p]
f=1-2*m/r-H**2*r**2
g=sp.Matrix([[-f,-1,0,0],[-1,0,0,0],[0,0,r*r,0],[0,0,0,r*r*sp.sin(t)**2]])
gi=g.inv()
gamma={}
dgamma={}
for i in range(4):
 for j in range(4):
  for k in range(4):
   z=sp.simplify(sum(gi[i,l]*(sp.diff(g[l,k],xx[j])+sp.diff(g[l,j],xx[k])-sp.diff(g[j,k],xx[l])) for l in range(4))/2)
   if z!=0:
    gamma[i,j,k]=sp.lambdify((r,t,m,H),z,'numpy')
    for q in [1,2]:
     dz=sp.diff(z,xx[q])
     if dz!=0: dgamma[i,j,k,q]=sp.lambdify((r,t,m,H),dz,'numpy')

def metric(x,mm,hh):
 rr=x[1]; ff=1-2*mm/rr-hh*hh*rr*rr
 return np.array([[-ff,-1,0,0],[-1,0,0,0],[0,0,rr*rr,0],[0,0,0,rr*rr*np.sin(x[2])**2]])

def rhs(l,y,mm,hh,jac):
 x=y[:4]; k=y[4:8]; ga=np.zeros((4,4,4))
 for ix,fun in gamma.items(): ga[ix]=fun(x[1],x[2],mm,hh)
 dy=np.zeros_like(y); dy[:4]=k; dy[4:8]=-np.einsum('ijk,j,k->i',ga,k,k)
 if jac:
  jj=y[8:16].reshape(4,2); vv=y[16:24].reshape(4,2)
  grad=np.zeros((4,4))
  for (i,j,z,q),fun in dgamma.items(): grad[i,q]+=fun(x[1],x[2],mm,hh)*k[j]*k[z]
  dy[8:16]=vv.ravel()
  dy[16:24]=(-2*np.einsum('ijk,j,kn->in',ga,k,vv)-grad@jj).ravel()
 return dy

def integrate(y,a,R,mm,hh,jac,tight):
 def endpoint(l,y): return y[1]-a
 endpoint.terminal=True
 sol=solve_ivp(lambda l,y:rhs(l,y,mm,hh,jac),(0,-10*R),y,method='DOP853',
               rtol=2e-12 if tight else 2e-10,atol=2e-13 if tight else 2e-11,events=endpoint)
 if not sol.success or len(sol.t_events[0])!=1: raise RuntimeError(sol.message)
 return sol

def optical_case(mm,hh,a,E,R,b):
 ff=lambda rr:1-2*mm/rr-hh*hh*rr*rr
 ss=lambda rr:math.sqrt(1-ff(rr)*b*b/(rr*rr))
 sR=ss(R); sa=ss(a); v=math.sqrt(E*E-ff(R))
 A=1/(E+v)+v*b*b/(R*R*(1+sR))
 xo=np.array([0.,R,math.pi/2,0.])
 ko=np.array([b*b/(R*R*(1+sR)),sR,0.,b/(R*R)])
 U=np.array([1/(E+v),v,0.,0.]); met=metric(xo,mm,hh)
 eb=np.array([[b/(R*sR),0],[0,0],[0,1/R],[1/(R*sR),0]])
 physical=eb+np.outer(ko,(U@met@eb)/A)
 n=ko/A-U
 I=quad(lambda rr:1/(rr*rr*ss(rr)**3),a,R,epsabs=2e-13,epsrel=2e-13,limit=400)[0]
 P=quad(lambda rr:b/(rr*rr*ss(rr)),a,R,epsabs=2e-13,epsrel=2e-13,limit=400)[0]
 Bpar=a*R*sa*sR*I
 Bper=a*R*math.sin(P)/b if b else R-a
 expected=-A*np.diag([Bpar,Bper])
 report={'parameters':[mm,hh,a,E,R,b],'P':P,'A':A,'B':[Bpar,Bper],'D_A':A*math.sqrt(abs(Bpar*Bper)),'expected':expected.tolist(),'jacobi':[],'neighbor':[]}
 final=None
 for tight in [False,True]:
  yy=np.concatenate((xo,ko,np.zeros(8),(A*physical).ravel()))
  sol=integrate(yy,a,R,mm,hh,True,tight); final=sol.y[:,-1]
  xe=final[:4]; ke=final[4:8]; ge=metric(xe,mm,hh)
  ee=np.array([[b/(a*sa),0],[0,0],[0,1/a],[1/(a*sa),0]])
  actual=ee.T@ge@final[8:16].reshape(4,2)
  err=float(np.max(np.abs(actual-expected))/max(1,np.max(np.abs(expected))))
  norms=[]; energies=[]
  for j in range(sol.y.shape[1]):
   x=sol.y[:4,j]; k=sol.y[4:8,j]; gm=metric(x,mm,hh)
   norms.append(abs(float(k@gm@k))/max(1,float(np.sum(abs(k*(gm@k))))))
   energies.append(abs(float(-(gm@k)[0])-1))
  report['jacobi'].append({'tight':tight,'map':actual.tolist(),'relative_error':err,'max_null_scaled':max(norms),'max_energy_error':max(energies),'steps':len(sol.t),'lambda_end':float(sol.t[-1])})
  assert err<=2e-6 and max(norms)<=2e-7 and max(energies)<=2e-7
 errors=[]
 for eps in [1e-6,5e-7]:
  center=[]
  for axis in range(2):
   endpoints=[]
   for sign in [-1,1]:
    knew=A*(U+math.cos(eps)*n+sign*math.sin(eps)*physical[:,axis])
    sol=integrate(np.r_[xo,knew],a,R,mm,hh,False,True)
    endpoints.append(sol.y[:4,-1])
   center.append((endpoints[1]-endpoints[0])/(2*eps))
  actual=ee.T@ge@np.array(center).T
  err=float(np.max(np.abs(actual-expected))/max(1,np.max(np.abs(expected))))
  report['neighbor'].append({'angle':eps,'map':actual.tolist(),'relative_error':err})
  errors.append(err)
 (OUT/'LAST_OPTICAL_CASE.json').write_text(json.dumps(report,indent=2)+'\n')
 assert errors[-1]<=2e-5 and (errors[-1]<errors[0] or errors[-1]<=2e-7)
 L=quad(lambda rr:1/ss(rr),a,R,epsabs=1e-11,epsrel=2e-13,limit=400)[0]
 report['D_affine']=A*L
 report['angular_affine_ratio']=report['D_A']/(A*L)
 return report

def incidence(R):
 mm=1.;hh=.02;a=6.;E=1.; om=math.sqrt(mm/a**3-hh*hh); h=1-3*mm/a
 ff=lambda rr:1-2*mm/rr-hh*hh*rr*rr
 # Compact inverse-radius quadratures avoid infinity and very long intervals.
 def vscaled(x): return math.sqrt(hh*hh+(E*E-1)*x*x+2*mm*x**3)
 d=quad(lambda x:1/(vscaled(x)*(E*x+vscaled(x))),0,1/R,epsabs=2e-13,epsrel=2e-13)[0]
 def values(b):
  ss=lambda x:math.sqrt(1+hh*hh*b*b-b*b*x*x+2*mm*b*b*x**3)
  P=quad(lambda x:b/ss(x),1/R,1/a,epsabs=2e-13,epsrel=2e-13)[0]
  UU=quad(lambda x:b*b/(ss(x)*(1+ss(x))),1/R,1/a,epsabs=2e-13,epsrel=2e-13)[0]
  return P,UU,ss
 def equation(b):
  P,UU,ss=values(b);return P-om*UU-om*d
 bmax=a/math.sqrt(ff(a)); b=brentq(equation,0,.999*bmax,xtol=1e-13,rtol=1e-14)
 P,UU,ss=values(b)
 I=quad(lambda x:1/ss(x)**3,1/R,1/a,epsabs=2e-13,epsrel=2e-13)[0]
 v=math.sqrt(E*E-ff(R));A=1/(E+v)+v*b*b/(R*R*(1+ss(1/R)))
 bp=a*R*ss(1/a)*ss(1/R)*I;bt=a*R*math.sin(P)/b
 DA=A*math.sqrt(bp*bt);Z=(1-om*b)/(math.sqrt(h)*A)
 target=(a+E/hh)/math.sqrt(h);product=Z*(1/hh-DA)
 residual=abs(equation(b));err=abs(product/target-1)
 assert residual<=1e-10
 return {'R':R,'b':b,'t_e':-d-UU,'P':P,'B':[bp,bt],'A':A,'D_A':DA,'Z':Z,'pole_product':product,'target':target,'pole_relative_error':err,'incidence_residual':residual}

results={'versions':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,'sympy':sp.__version__},'cases':[],'incidences':[],'finite_case_count':0}
def save():
 results['elapsed_seconds']=time.time()-started
 (OUT/'RESULT.json').write_text(json.dumps(results,indent=2)+'\n')
try:
 ca=3.001;ch=.18;cb=.999*ca/math.sqrt(1-2/ca-ch*ch*ca*ca)
 for case in [(1,ch,ca,1,30,cb)]:
  results['cases'].append(optical_case(*case));results['finite_case_count']+=10;save()
  print('optical',case,'PASS',flush=True)
 for R in [1e3,1e4,1e5,1e6]:
  results['incidences'].append(incidence(R));results['finite_case_count']+=1;save()
  print('incidence',R,'PASS',flush=True)
 errs=[x['pole_relative_error'] for x in results['incidences']]
 assert errs[-1]<.01 and all(y<x for x,y in zip(errs,errs[1:]))
 results['status']='PASS';save();print('ALL PASS',flush=True)
except Exception as exc:
 results['status']='FAIL';results['failure']=repr(exc);save();raise
