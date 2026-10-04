import os
for name in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:
    os.environ[name]='1'
import resource
resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
import json,sys,hashlib
from pathlib import Path
import numpy as np
import scipy
from scipy.integrate import solve_ivp
from scipy.optimize import root

B=Path(__file__).resolve().parent
f=lambda r:1-2/r
fp=lambda r:2/r**2
def endpoint(params,details=False):
    lamend,tauend,b=params
    assert lamend>0 and tauend>0
    q0=np.sqrt(1-f(10.)*b*b/100.)
    def ray_rhs(lam,y):
        t,r,phi,v=y
        return [1/f(r),v,b/r**2,b*b*(r-3)/r**4]
    def obs_rhs(tau,y):
        t,r,v=y
        return [1/f(r),v,-fp(r)/2]
    ray=solve_ivp(ray_rhs,(0,lamend),[0,10.,-.2,q0],method='DOP853',atol=1e-12,rtol=1e-12)
    obs=solve_ivp(obs_rhs,(0,tauend),[0,50.,.2],method='DOP853',atol=1e-12,rtol=1e-12)
    assert ray.success and obs.success
    re,oe=ray.y[:,-1],obs.y[:,-1]
    residual=np.array([re[0]-oe[0],re[1]-oe[1],re[2]])
    return (residual,ray,obs) if details else residual
sol=root(endpoint,[55.,65.,2.4],tol=1e-10)
assert sol.success,sol.message
res,ray,obs=endpoint(sol.x,True)
lamend,tauend,b=sol.x
R=obs.y[1,-1];v=obs.y[2,-1];q=ray.y[3,-1]
ray_norm=np.max(np.abs(ray.y[3]**2-1+f(ray.y[1])*b*b/ray.y[1]**2))
obs_norm=np.max(np.abs(obs.y[2]**2+f(obs.y[1])-1))
assert np.max(np.abs(res))<1e-9 and ray_norm<1e-9 and obs_norm<1e-9
we=(1-b*np.sqrt(.001))/np.sqrt(.7)
wo=(1-v*q)/f(R)
Z=we/wo
nr=(q-v)/(1-v*q);nphi=f(R)*b/(R*(1-v*q))
assert abs(nr*nr+nphi*nphi-1)<1e-9
out={'status':'PASS_INDEPENDENT_ODE_ANCHOR','python':sys.version,
 'numpy':np.__version__,'scipy':scipy.__version__,'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'method':'direct affine-null and proper-receiver ODE shooting, float64 DOP853',
 'inputs':{'m':1,'Lambda':0,'a':10,'R0':50,'E':1,'phi0':-.2,'t_e':0},
 'root_nfev':sol.nfev,'ray_affine_length':lamend,'R':R,'b':b,'tau_o':tauend,
 'Z_endpoint':Z,'n_propagation':[nr,nphi],
 'endpoint_coordinate_residual':res.tolist(),'max_null_norm_residual':ray_norm,
 'max_receiver_norm_residual':obs_norm,'ray_rhs_evaluations_final':ray.nfev,
 'receiver_rhs_evaluations_final':obs.nfev}
dest=B/'ODE_RESULT.json'
dest.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
