import os
for v in ("OMP_NUM_THREADS","MKL_NUM_THREADS","OPENBLAS_NUM_THREADS","NUMEXPR_NUM_THREADS"):
    os.environ[v]="1"
import numpy as np, sys
sys.path.insert(0,'.')
from lean import xdot,xcr
from lean_rayleigh import BG, omega2, mode_isorot_z
from lean import nhat

# the three iso-rotation generators about target x,y,z axes -> exact zero modes
def isorot_axis(B, axis):
    out=[]
    for i in range(B.Nr):
        n0=B.flds[i]; d=np.empty_like(n0)
        a=axis
        d[...,0]=a[1]*n0[...,2]-a[2]*n0[...,1]
        d[...,1]=a[2]*n0[...,0]-a[0]*n0[...,2]
        d[...,2]=a[0]*n0[...,1]-a[1]*n0[...,0]
        d=d-xdot(d,n0)[...,None]*n0
        out.append(d)
    return out

if __name__=='__main__':
    for p in (0,1,2):
        B=BG(p)
        print(f"p={p} iso-rotation zero modes:")
        for nm,ax in [('x',[1,0,0]),('y',[0,1,0]),('z',[0,0,1])]:
            o,d2S,d2T=omega2(B,isorot_axis(B,ax))
            print(f"   axis {nm}: omega^2={o:.6e}  d2S={d2S:.3e} d2T={d2T:.3e}")
