import os
for v in ("OMP_NUM_THREADS","MKL_NUM_THREADS","OPENBLAS_NUM_THREADS","NUMEXPR_NUM_THREADS"):
    os.environ[v]="1"
import numpy as np, sys
sys.path.insert(0,'.')
import lean
from scipy.optimize import minimize

def solve_profile(p, R=18.0, r_core=0.05, Nr=60, r_int=1.0):
    rg=np.linspace(r_core,r_core+R,Nr)
    phia=p*np.log(rg/r_int)
    F0=np.pi*np.exp(-(rg-r_core)/max(0.3,2.0/(1+p))); F0[-1]=0
    def pack(x):
        F=np.empty(Nr); F[0]=np.pi; F[-1]=0.0; F[1:-1]=x; return F
    def obj(x):
        return lean.total_energy(rg,pack(x),phia)
    res=minimize(obj,F0[1:-1],method='L-BFGS-B',
                 options={'maxiter':500,'ftol':1e-11,'gtol':1e-8,'maxfun':100000})
    return rg,pack(res.x),phia,res

if __name__=='__main__':
    import time
    for p in (0,1,2):
        t=time.time()
        rg,F,phia,res=solve_profile(p)
        print(f"p={p}: E0={res.fun:.4f} conv={res.success} nit={res.nit} t={time.time()-t:.1f}s")
        np.save(f'leanprof_p{p}.npy',np.vstack([rg,F,phia]))
