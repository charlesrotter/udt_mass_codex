import numpy as np
from scipy.integrate import solve_bvp
def solve_deep(p, xi=1.0, kappa=1.0, rint=1.0, ratio=240.0, N=6000):
    rc=rint/ratio
    def ephi(r): return np.exp(-p*np.log(rint/r))
    def a(r,T): return (0.5*xi*r**2+kappa*np.sin(T)**2)/ephi(r)
    def aT(r,T): return (kappa*2*np.sin(T)*np.cos(T))/ephi(r)
    def ar(r,T): return (p/r)/ephi(r)*(0.5*xi*r**2+kappa*np.sin(T)**2)+ (xi*r)/ephi(r)
    def bT(r,T): return ephi(r)*(xi*2*np.sin(T)*np.cos(T)+kappa*4*np.sin(T)**3*np.cos(T)/(2*r**2))
    def rhs(r,y):
        T,Tp=y
        Tpp=(aT(r,T)*Tp**2+bT(r,T)-2*ar(r,T)*Tp-2*aT(r,T)*Tp*Tp)/(2*a(r,T))
        return np.vstack([Tp,Tpp])
    def bc(ya,yb): return np.array([ya[0]-np.pi, yb[0]-0.0])
    r=np.linspace(rc,rint,N)
    Tg=np.pi*(1-(r-rc)/(rint-rc)); Tpg=np.full_like(r,-np.pi/(rint-rc))
    sol=solve_bvp(rhs,bc,r,np.vstack([Tg,Tpg]),max_nodes=400000,tol=1e-7)
    rs=np.linspace(rc,rint,40000); Ts=sol.sol(rs)[0]
    w=rs[np.argmin(np.abs(Ts-np.pi/2))]; L=np.sqrt(kappa/xi)
    return sol.success,(w-rc)/L,(sol.rms_residuals.max() if sol.success else -1)
for p in [0.0,0.5,1,2,3,4]:
    ok,wL,res=solve_deep(p)
    print(f'p={p}: success={ok}  (w-rc)/L={wL:.3f}  resid={res:.1e}')
