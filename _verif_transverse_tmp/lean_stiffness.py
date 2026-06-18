import os
for v in ("OMP_NUM_THREADS","MKL_NUM_THREADS","OPENBLAS_NUM_THREADS","NUMEXPR_NUM_THREADS"):
    os.environ[v]="1"
import numpy as np, sys
sys.path.insert(0,'.')
from lean_rayleigh import BG
from lean_full import channel_op, Y, ZERO
from scipy.linalg import eigh, eigvalsh

def stiffness_min(B,l):
    """min eigenvalue of the STIFFNESS form H alone (Dirichlet), over m and e1/e2.
    H>0 => no unstable direction, independent of the mass weight."""
    best=np.inf
    for m in range(-l,l+1):
        for f,g in [(Y(l,m),ZERO),(ZERO,Y(l,m))]:
            H,M=channel_op(B,f,g); Nr=B.Nr; idx=np.arange(1,Nr-1)
            Hs=0.5*(H+H.T)[np.ix_(idx,idx)]
            w=eigvalsh(Hs)
            best=min(best,w[0])
    return best

if __name__=='__main__':
    for p in (0,1,2):
        B=BG(p)
        s1=stiffness_min(B,1); s2=stiffness_min(B,2)
        print(f"p={p}: min stiffness eigenvalue  l=1: {s1:.5e}   l=2: {s2:.5e}  "
              f"{'(POSITIVE-DEFINITE: no unstable direction)' if min(s1,s2)>0 else '(NEGATIVE: unstable dir!)'}")
