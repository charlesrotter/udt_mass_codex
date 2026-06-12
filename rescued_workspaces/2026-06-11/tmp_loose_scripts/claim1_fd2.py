import numpy as np
from scipy.integrate import solve_ivp, simpson
from scipy.optimize import brentq

# Finite-difference test: dS_D/dphi(r) at a point should equal -(T^r_r - T^t_t)(r) on a solved mode.
# S_D[G,F,PHI] = INT L dr with L the first-order Lagrangian (on-shell =0, but its phi-FUNCTIONAL DERIV
# is nonzero). We test the LOCAL functional derivative by perturbing PHI(r)->PHI(r)+eps*delta-like bump
# and measuring dS/d(bump-amplitude) vs INT bump * source.
# Solve a bound mode in fixed PHI background, then check.

A0,r0,w=0.5,3.0,1.2
PHI =lambda r:A0*np.exp(-((r-r0)/w)**2)
PHIp=lambda r:A0*np.exp(-((r-r0)/w)**2)*(-2*(r-r0)/w**2)
m,k=0.5,-1
rg=np.linspace(0.03,22,12000)

def shoot(E):
    def rhs(r,y):
        G,F=y;p=PHI(r);pp=PHIp(r);e2=np.exp(2*p);e1=np.exp(p)
        return [(pp-k/r)*G+(E*e2+m*e1)*F,(pp+k/r)*F-(E*e2-m*e1)*G]
    y0=[rg[0]**abs(k),1e-3]
    return solve_ivp(rhs,[rg[0],rg[-1]],y0,t_eval=rg,rtol=1e-11,atol=1e-14)
def res(E): return shoot(E).y[0][-1]
Es=np.linspace(0.05*m,0.999*m,600); rr=[res(E) for E in Es]
br=None
for i in range(len(rr)-1):
    if rr[i]*rr[i+1]<0: br=(Es[i],Es[i+1]);break
E0=brentq(res,*br,xtol=1e-13)
sol=shoot(E0); G,F=sol.y
nrm=simpson(G**2+F**2,rg); G/=np.sqrt(nrm); F/=np.sqrt(nrm)
print("E0=",E0)

# source (sigma=-1, PHI background):
p=PHI(rg); pp=PHIp(rg); sigma=-1
source = -2*sigma*( k*(F**2-G**2)/rg + pp*(F**2+G**2) + m*np.exp(p)*G*F )

# The first-order Lagrangian density L = G(G'-RHS_G)+F(F'-RHS_F). On-shell L=0 identically, but the
# HF source = explicit dL/dPHI - d/dr(dL/dPHI'). We instead test the EQUIVALENT statement:
# d/d(eps) of [ G,F held FIXED, PHI->PHI+eps*h ] of S_D  =  INT h * (dL/dPHI) - INT h' *(dL/dPHIp) dr... 
# Cleaner: directly evaluate the integrated source against the action's explicit phi-derivative.
# L_explicit(PHI) part (drop G',F' which are phi-independent):
def L_expl(Gv,Fv,pv,ppv):
    # = -G*RHS_G - F*RHS_F  (the kinetic GG'+FF' drop)
    RG=(ppv-k/rg)*Gv+(E0*np.exp(2*pv)+m*np.exp(pv))*Fv
    RF=(ppv+k/rg)*Fv-(E0*np.exp(2*pv)-m*np.exp(pv))*Gv
    return -Gv*RG - Fv*RF
def S_expl(amp,h,hp):
    pv=PHI(rg)+amp*h; ppv=PHIp(rg)+amp*hp
    return simpson(L_expl(G,F,pv,ppv),rg)

# test bumps; sigma=-1 means PHI=-phi, perturb phi: PHI -> PHI - eps*h_phi. dPHI=-eps*h.
# dS_D/dphi tested: pick h(r), compute dS/deps wrt phi-perturbation = -(dS/d(PHI-amp)).
for (rc,wc) in [(2.0,0.5),(3.0,0.5),(4.0,0.7)]:
    h =np.exp(-((rg-rc)/wc)**2)
    hp=np.exp(-((rg-rc)/wc)**2)*(-2*(rg-rc)/wc**2)
    eps=1e-5
    # phi perturbation: phi+eps*h => PHI=-phi => PHI-eps*h
    dSdphi=(S_expl(-eps,h,hp)-S_expl(eps,h,hp))/(2*eps)   # d/dphi (chain: PHI amp = -phi amp)
    # claim: dS_D/dphi = -(T^r_r-T^t_t) integrated => INT h*(-(source))? Actually collapse:
    # delta S_D/delta phi = -(T^r_r-T^t_t). So dS/deps[phi=eps h] = INT h*(-source).
    pred=simpson(h*(-source),rg)
    print(f"  bump r={rc}: dS_D/dphi={dSdphi:+.6e}  INT h*(-(T^r-T^t))={pred:+.6e}  rel.diff={abs(dSdphi-pred)/abs(pred):.2e}")
