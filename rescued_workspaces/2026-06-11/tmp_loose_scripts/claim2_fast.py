import numpy as np
from scipy.integrate import solve_ivp, simpson
from scipy.optimize import brentq

# Fast & clean: take a mode at scale 1, rescale it analytically (r->s r, m->m/s, c=s^-1/2),
# verify the FULL sourced RHS lambda*e^{4phi}(T^r-T^t) maps to (1/s^2)*RHS, AND that the
# eigenvalue E found in the rescaled problem equals E0/s (so E/m invariant).
A0,r0,w=0.5,3.0,1.2
PHI=lambda r:A0*np.exp(-((r-r0)/w)**2)
PHIp=lambda r:A0*np.exp(-((r-r0)/w)**2)*(-2*(r-r0)/w**2)
m,k=0.5,-1
rg=np.linspace(0.03,22,9000)
def solve(PHIf,PHIpf,mm,kk,grid):
    def shoot(E):
        def rhs(r,y):
            G,F=y;p=PHIf(r);pp=PHIpf(r);e2=np.exp(2*p);e1=np.exp(p)
            return [(pp-kk/r)*G+(E*e2+mm*e1)*F,(pp+kk/r)*F-(E*e2-mm*e1)*G]
        return solve_ivp(rhs,[grid[0],grid[-1]],[grid[0]**abs(kk),1e-3],t_eval=grid,rtol=1e-11,atol=1e-14)
    def res(E):return shoot(E).y[0][-1]
    Es=np.linspace(0.05*mm,0.999*mm,500);rr=[res(E) for E in Es];br=None
    for i in range(len(rr)-1):
        if rr[i]*rr[i+1]<0:br=(Es[i],Es[i+1]);break
    E=brentq(res,*br,xtol=1e-13);sol=shoot(E);G,F=sol.y
    nrm=simpson(G**2+F**2,grid);return E,G/np.sqrt(nrm),F/np.sqrt(nrm)

E0,G0,F0=solve(PHI,PHIp,m,k,rg)
print("scale 1: E0=",E0," E0/m=",E0/m)
# now rescaled problem: s=3, PHI_s(r)=PHI(r/s), m_s=m/s. Solve from scratch.
s=3.0
rgs=rg*s
Es,Gs,Fs=solve(lambda r:PHI(r/s),lambda r:PHIp(r/s)/s,m/s,k,rgs)
print(f"scale s={s}: Es={Es}  Es/(m/s)={Es/(m/s)}")
print(f"E0/m invariant? rel.diff={abs(E0/m-Es/(m/s))/(E0/m):.3e}")
print(f"Es vs E0/s: {Es:.6f} vs {E0/s:.6f}  rel={abs(Es-E0/s)/(E0/s):.3e}")

# verify the source maps as 1/s^2 with the analytically-rescaled mode (c=s^-1/2):
sigma=-1
def source(G,F,p,pp,mm,grid):
    return -2*sigma*(k*(F**2-G**2)/grid+pp*(F**2+F**2)*0+pp*(F**2+G**2)+mm*np.exp(p)*G*F)
src0=source(G0,F0,PHI(rg),PHIp(rg),m,rg)
# analytic rescale of the scale-1 mode:
Gana=np.interp(rgs/s,rg,G0)/np.sqrt(s); Fana=np.interp(rgs/s,rg,F0)/np.sqrt(s)
srcana=source(Gana,Fana,PHI(rgs/s),PHIp(rgs/s)/s,m/s,rgs)
# compare srcana(s*r) to src0(r)/s^2
src0_interp=np.interp(rgs/s,rg,src0)
ratio=srcana/(src0_interp/s**2)
print("source ratio srcana(sr)/(src0(r)/s^2) median:",np.median(ratio[np.abs(src0_interp)>1e-4*np.max(np.abs(src0_interp))]))
