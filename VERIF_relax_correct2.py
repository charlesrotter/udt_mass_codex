import numpy as np
from scipy.optimize import least_squares
import VERIF_relax_correct as M

G=M.Grid(24,4,rc=0.05,cell=14.0)
u0=M.round_seed(G)
def res(u,p=0.4,kap8=0.05): return M.residual(u,G,p,kap8)[0]
# gate
solg=least_squares(res,u0.copy(),method='lm',max_nfev=4000,xtol=1e-12,ftol=1e-12)
_,rfg=M.residual(solg.x,G,0.4,0.05)
print(f"GATE (correct EL): Phi={float(solg.fun@solg.fun):.3e} M_MS={M.M_MS(G,rfg,0.05):.5f} tvar={M.tvar(G,rfg):.3e}")
def legP(l,x):
    from numpy.polynomial.legendre import Legendre
    cc=np.zeros(l+1);cc[l]=1.0;return Legendre(cc)(x)
import sys
for kind in (sys.argv[1:] or ['l2']):
    a,b,c,d,Th=M.unpack(u0,G)
    rprof=np.exp(-((G.R-2.0)/1.5)**2)
    if kind.startswith('l'): Th=Th+0.30*rprof*legP(int(kind[1:]),G.CTH)
    elif kind=='ring': Th=Th+0.40*rprof*np.sin(G.THm)**2
    Th[0,:]=np.pi;Th[-1,:]=0.0
    us=M.pack(a,b,c,d,Th)
    _,rf0=M.residual(us,G,0.4,0.05)
    print(f"\nseed {kind}: seed_tvar={M.tvar(G,rf0):.4f} Phi0={float(res(us)@res(us)):.2e}")
    sol=least_squares(res,us,method='lm',max_nfev=6000,xtol=1e-13,ftol=1e-13)
    _,rf=M.residual(sol.x,G,0.4,0.05)
    print(f"  SOLVED: Phi={float(sol.fun@sol.fun):.3e} tvar={M.tvar(G,rf):.4e} M_MS={M.M_MS(G,rf,0.05):.5f}")
