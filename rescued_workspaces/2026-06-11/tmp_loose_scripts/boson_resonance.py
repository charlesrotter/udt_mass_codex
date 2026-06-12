import numpy as np
from scipy.integrate import solve_ivp, cumulative_trapezoid
m=1.0; r0=1e-3; RMAX=60.0
rg=np.linspace(r0,RMAX,40000); dr=rg[1]-rg[0]
phib=0.5*np.log(rg/(2+rg)); phibp=1.0/(rg*(2+rg))      # phi_bg (<0) and phi_bg'
PHI=-phib; PHIp=-phibp                                  # operator sees Phi=-phi>0 (binding)
# ---------- 1) fermion kappa=-1 ground on phi_bg (binding convention) ----------
kappa=-1
def dirac(E):
    def rhs(r,y):
        ph=0.5*np.log((2+r)/r); pp=-1.0/(r*(2+r)); e1=np.exp(ph); e2=np.exp(2*ph); g,f=y
        return [(pp-kappa/r)*g+(E*e2+m*e1)*f,(pp+kappa/r)*f-(E*e2-m*e1)*g]
    s=solve_ivp(rhs,[r0,RMAX],[r0**0.5,0.0],dense_output=True,rtol=1e-10,atol=1e-12,max_step=0.02)
    G,F=s.y[0,-1],s.y[1,-1]; q=np.sqrt(max(m*m-E*E,1e-12))
    return (G+(E+m)/q*F)/np.sqrt(G*G+F*F+1e-300), s
lo,hi=0.45,0.55
for _ in range(60):
    mid=0.5*(lo+hi)
    if dirac(lo)[0]*dirac(mid)[0]<0: hi=mid
    else: lo=mid
E=0.5*(lo+hi); _,s=dirac(E)
G=s.sol(rg)[0]; F=s.sol(rg)[1]
nrm=np.trapezoid(G*G+F*F,rg); G/=np.sqrt(nrm); F/=np.sqrt(nrm)
print(f"fermion kappa=-1 ground E={E:.5f}  (norm int(G^2+F^2)dr=1)")
# ---------- 2) source T = T^r_r - T^t_t = -2 sigma[kappa(F^2-G^2)/r + Phi'(F^2+G^2)+ m e^Phi GF], sigma=-1 ----
ePhi=np.exp(PHI)
T = -2*(-1)*( kappa*(F**2-G**2)/rg + PHIp*(F**2+G**2) + m*ePhi*G*F )
qsrc = np.exp(4*phib)*T                                  # RHS of sourced static eq (lambda=1 units)
# ---------- 3) linear response dphi: ((2+r)^2 dphi')' = (2+r)^2 * qsrc ; dphi(inf)=0, regular ----
p=(2+rg)**2
rhs_int = cumulative_trapezoid(p*qsrc, rg, initial=0.0)  # = (2+r)^2 dphi' (with const so dphi'->0 outside source)
dphip = rhs_int/p
# integrate dphi' inward-consistent: dphi = -int_r^inf dphi' dr (so dphi(inf)=0)
dphi = -(np.trapezoid(dphip,rg) - cumulative_trapezoid(dphip,rg,initial=0.0))
print(f"dimple dphi: min={dphi.min():+.4e} at r={rg[np.argmin(dphi)]:.2f}, max={dphi.max():+.4e}; "
      f"sign in core -> {'deepens phi (stiffness BUMP)' if dphi[np.argmax(np.abs(dphi))]<0 else 'raises phi (stiffness DIP)'}")
# ---------- 4) boson phase shift on dressed bg: -(p_d u')' = w^2 r^2 u, p_d=(2+r)^2 e^{-4 lam dphi} ----
def phase_shift(lam, w):
    pd = (2+rg)**2*np.exp(-4*lam*dphi)
    pd_f=lambda r: np.interp(r,rg,pd)
    def rhs(r,y):
        u,pu=y                      # pu = p_d u'
        return [pu/pd_f(r), -w*w*r*r*u]
    s=solve_ivp(rhs,[r0,RMAX],[1.0,0.0],dense_output=True,rtol=1e-9,atol=1e-12,max_step=0.02)
    Rm=RMAX*0.9; u=s.sol(Rm)[0]; pu=s.sol(Rm)[1]; up=pu/pd_f(Rm)
    ru=Rm*u; rup=u+Rm*up            # (r u)'
    d=np.arctan2(w*ru, rup) - w*Rm  # sin(wr+delta): tan(wr+delta)=w ru/(ru)'
    return ((d+np.pi)% np.pi)
ws=np.linspace(0.05,3.0,300)
print("\nboson scattering: Wigner time delay d(delta)/dw vs w; peaks = RESONANCES. (compare lambda)")
print(f"  {'w':>6}", *[f"lam={l:<5}" for l in [0.0,1.0,2.0,4.0]])
import numpy as np
prev={l:None for l in [0.0,1.0,2.0,4.0]}
delt={l:np.array([phase_shift(l,w) for w in ws]) for l in [0.0,1.0,2.0,4.0]}
for l in delt:  # unwrap
    delt[l]=np.unwrap(2*delt[l])/2
for l in [1.0,2.0,4.0]:
    dd=np.gradient(delt[l]-delt[0.0],ws)
    pk=np.argsort(dd)[-3:]
    print(f"  lambda={l}: top time-delay peaks at w = "+", ".join(f"{ws[i]:.3f}(dd={dd[i]:.2f})" for i in sorted(pk)))
# also: total extra phase across the band (Levinson-ish: jumps of pi ~ quasi-bound count)
for l in [1.0,2.0,4.0]:
    net=(delt[l]-delt[0.0])[-1]-(delt[l]-delt[0.0])[0]
    print(f"  lambda={l}: net extra phase across band = {net:+.3f} rad ({net/np.pi:+.2f} pi)")
