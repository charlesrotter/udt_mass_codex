import numpy as np
from spectral_radial_soliton import solve as rsolve
from axisym_matter_el_CORRECT import matter_el_resid_CORRECT as ELc
import axisym_matter_el as ME
out=rsolve(96,rc=0.05,cell=14.0,p=0.4,kap8=0.05,maxit=120)
r=out['r'];a=out['a'];b=out['b'];Th=out['Th'];D=out['D']
ap=D@a;bp=D@b;app=D@ap;bpp=D@bp;Thp=D@Th;Thpp=D@Thp
body=(r>0.6)&(r<r[-1]-0.6)
Z=0.0
correct=np.array([ELc(r[i],np.pi/2, a[i],ap[i],Z,app[i],Z,Z, b[i],bp[i],Z,bpp[i],Z,Z,
                      Z,Z,Z,Z,Z,Z, Z,Z,Z,Z,Z,Z, Th[i],Thp[i],Z,Thpp[i],Z,Z, 1.0,1.0) for i in range(r.size)])
print("CORRECT axisym EL on round soliton, body max-abs:", np.max(np.abs(correct[body])))
