import os
for v in ("OMP_NUM_THREADS","MKL_NUM_THREADS","OPENBLAS_NUM_THREADS","NUMEXPR_NUM_THREADS"):
    os.environ[v]="1"
import numpy as np, sys
sys.path.insert(0,'.')
import lean
from lean import nhat,xdot,xcr,TG,PG
from lean_solve import solve_profile
import lean_rayleigh as LR
from lean_full import channel_op, lowest, Y, ZERO, angular_tangent
from scipy.linalg import eigh

class BGr:
    """stationary unit background solved at arbitrary R."""
    def __init__(self,p,R,Nr=60,r_core=0.05):
        rg,F,phia,res=solve_profile(p,R=R,r_core=r_core,Nr=Nr)
        self.r=rg; self.F=F; self.phi=phia; self.Nr=Nr; self.dr=rg[1]-rg[0]; self.p=p; self.R=R
        self.flds=[nhat(F[i]) for i in range(Nr)]
        self.E0=res.fun
    def dnr_bg(self,i):
        if i==0: return (self.flds[1]-self.flds[0])/self.dr
        if i==self.Nr-1: return (self.flds[-1]-self.flds[-2])/self.dr
        return (self.flds[i+1]-self.flds[i-1])/(2*self.dr)

def lowest_l1(B):
    best=np.inf
    for m in (-1,0,1):
        for f,g in [(Y(1,m),ZERO),(ZERO,Y(1,m))]:
            ev=lowest(B,f,g); best=min(best,ev[0])
    return best

if __name__=='__main__':
    print("=== R-scan: lowest non-Goldstone l=1 omega^2 ===")
    print("intrinsic => omega^2 ~ const (omega^2*R^2 grows ~R^2); box => omega^2 ~ 1/R^2 (omega^2*R^2 ~ const)\n")
    for p in (0,1):
        print(f"--- p={p} ---")
        Rs=[10,18,30] if p==0 else [8,16,32,64]
        for R in Rs:
            B=BGr(p,R)
            o=lowest_l1(B)
            print(f"  R={R:>3}: E0={B.E0:7.2f}  omega^2={o:.6e}  omega^2*R^2={o*R*R:.4f}")
