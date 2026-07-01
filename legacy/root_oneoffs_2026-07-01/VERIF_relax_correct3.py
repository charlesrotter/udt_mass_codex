import numpy as np
from scipy.optimize import least_squares
import VERIF_relax_correct as M
import sys
Nr=int(sys.argv[1]); Nth=int(sys.argv[2])
G=M.Grid(Nr,Nth,rc=0.05,cell=14.0)
u0=M.round_seed(G)
def res(u): return M.residual(u,G,0.4,0.05)[0]
def report(tag,u):
    F,rf=M.residual(u,G,0.4,0.05)
    a,b,c,d,Th=M.unpack(u,G)
    comps=M.einstein(G,a,b,c,d); Tm=rf['Tm']
    body=(G.R>0.8)&(G.R<G.ri-0.8)
    def mx(k): return np.max(np.abs((comps.get(k,0*a)-0.05*Tm[...,k[0],k[1]])[body]))
    REL=M.el_correct(G,a,b,c,d,Th)
    print(f"  {tag}: Phi={float(F@F):.3e} tvar={M.tvar(G,rf):.4e} M_MS={M.M_MS(G,rf,0.05):.5f}")
    print(f"       res_tt={mx((0,0)):.2e} res_thth={mx((2,2)):.2e} res_rth={mx((1,2)):.2e} EL_body={np.max(np.abs(REL[body])):.2e} cdmax={np.max(np.abs(c[body]))+np.max(np.abs(d[body])):.2e}")
solg=least_squares(res,u0.copy(),method='lm',max_nfev=8000,xtol=1e-13,ftol=1e-13)
print(f"=== Nr={Nr} Nth={Nth} CORRECT EL ===")
report("GATE round",solg.x)
def legP(l,x):
    from numpy.polynomial.legendre import Legendre
    cc=np.zeros(l+1);cc[l]=1.0;return Legendre(cc)(x)
a,b,c,d,Th=M.unpack(u0,G)
Th=Th+0.30*np.exp(-((G.R-2.0)/1.5)**2)*legP(2,G.CTH); Th[0,:]=np.pi;Th[-1,:]=0
us=M.pack(a,b,c,d,Th)
sol=least_squares(res,us,method='lm',max_nfev=10000,xtol=1e-14,ftol=1e-14)
report("l=2 solved",sol.x)
