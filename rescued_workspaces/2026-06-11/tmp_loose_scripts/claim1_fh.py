import numpy as np
from scipy.integrate import solve_ivp, simpson
from scipy.optimize import brentq

# Feynman-Hellmann test of the SOURCE formula.
# Operator (1st order, k=quantum number, PHI background):
#   G' = (PHI' - k/r)G + (E e^{2PHI} + m e^{PHI}) F
#   F' = (PHI' + k/r)F - (E e^{2PHI} - m e^{PHI}) G
#
# Recast as eigenproblem.  Move E to RHS:  define the "Dirac Hamiltonian" weakly.
# Multiply: from the two eqs, E e^{2PHI}(F,-G) appears. Let's write H[G,F]=E w(r)[G,F] form.
# Rearranged:
#   G' - (PHI'-k/r)G - m e^{PHI} F = E e^{2PHI} F
#   F' - (PHI'+k/r)F + m e^{PHI} G = -E e^{2PHI} G
# So defining operator on (G,F):
#   row1:  G' - (PHI'-k/r)G - m e^{PHI} F  = E e^{2PHI} F
#   row2: -[F' - (PHI'+k/r)F + m e^{PHI} G] = E e^{2PHI} G
# i.e.  L (G,F)^T = E e^{2PHI} (F,G)^T ... messy. Use FH numerically via direct dE/deps instead:
# Perturb PHI -> PHI + eps*h, recompute eigenvalue E(eps), get dE/deps numerically.
# Then compare to INT h * D(r) dr where D(r) is the FH kernel = -(dH/dphi) expectation.
#
# The variational/source claim: dE/d(phi-perturbation h) should be proportional to
#   the SAME combination (T^r_r - T^t_t) integrated against h (since the field eq source IS
#   delta S/delta phi). We test PROPORTIONALITY of dE/deps[h] to INT h*(T^r_r-T^t_t)-shape.

def solver(PHIfun, PHIpfun, m, k, rgrid):
    def shoot(E):
        def rhs(r,y):
            G,F=y; p=PHIfun(r); pp=PHIpfun(r)
            e2=np.exp(2*p); e1=np.exp(p)
            return [ (pp-k/r)*G+(E*e2+m*e1)*F, (pp+k/r)*F-(E*e2-m*e1)*G ]
        r0=rgrid[0]
        y0=[r0**abs(k),1e-3] if k<0 else [1e-3,r0**abs(k)]
        sol=solve_ivp(rhs,[rgrid[0],rgrid[-1]],y0,t_eval=rgrid,rtol=1e-10,atol=1e-13)
        return sol
    def resid(E):
        return solver_resid(E)
    return shoot

def find_E(PHIfun,PHIpfun,m,k,rgrid,Ebr):
    def shoot(E):
        def rhs(r,y):
            G,F=y; p=PHIfun(r); pp=PHIpfun(r)
            e2=np.exp(2*p); e1=np.exp(p)
            return [ (pp-k/r)*G+(E*e2+m*e1)*F, (pp+k/r)*F-(E*e2-m*e1)*G ]
        r0=rgrid[0]
        y0=[r0**abs(k),1e-3] if k<0 else [1e-3,r0**abs(k)]
        sol=solve_ivp(rhs,[rgrid[0],rgrid[-1]],y0,t_eval=rgrid,rtol=1e-11,atol=1e-14)
        return sol
    def res(E):
        return shoot(E).y[0][-1]
    E=brentq(res,Ebr[0],Ebr[1],xtol=1e-12)
    sol=shoot(E)
    G,F=sol.y
    norm=simpson(G**2+F**2,rgrid)
    G=G/np.sqrt(norm); F=F/np.sqrt(norm)
    return E,G,F

A0,r0,w=0.6,3.0,1.0
base=lambda r:A0*np.exp(-((r-r0)/w)**2)
basep=lambda r:A0*np.exp(-((r-r0)/w)**2)*(-2*(r-r0)/w**2)
m,k=0.5,-1
rgrid=np.linspace(0.05,20,8000)

# find baseline E (re-bracket robustly)
def res0(E):
    def rhs(r,y):
        G,F=y;p=base(r);pp=basep(r);e2=np.exp(2*p);e1=np.exp(p)
        return [(pp-k/r)*G+(E*e2+m*e1)*F,(pp+k/r)*F-(E*e2-m*e1)*G]
    r0_=rgrid[0]; y0=[r0_**abs(k),1e-3]
    return solve_ivp(rhs,[rgrid[0],rgrid[-1]],y0,t_eval=[rgrid[-1]],rtol=1e-11,atol=1e-14).y[0][-1]
Es=np.linspace(0.05*m,0.999*m,400); rr=[res0(E) for E in Es]
br=None
for i in range(len(rr)-1):
    if rr[i]*rr[i+1]<0: br=(Es[i],Es[i+1]); break
print("bracket",br)
E0,G0,F0=find_E(base,basep,m,k,rgrid,br)
print("E0=",E0, "norm check", simpson(G0**2+F0**2,rgrid))

# claimed source shape with sigma=-1, PHI=base, PHIp=basep:
def source_shape(G,F,PHIfun,PHIpfun,m,k,rgrid):
    p=PHIfun(rgrid); pp=PHIpfun(rgrid)
    sigma=-1
    Trr_Ttt = -2*sigma*( k*(F**2-G**2)/rgrid + pp*(F**2+G**2) + m*np.exp(p)*G*F )
    # source = -sqrt(-g)(T^r_r-T^t_t); sqrt(-g)=r^2 (angular integrated already absorbs sin)
    return Trr_Ttt

# FH numerical: perturb PHI by eps*h(r), several test profiles h, get dE/deps
def dE_deps(hfun,eps=1e-4):
    Ep,_,_=find_E(lambda r:base(r)+eps*hfun(r),
                  lambda r:basep(r)+eps*(hfun(r+1e-6)-hfun(r-1e-6))/2e-6,
                  m,k,rgrid,(E0-0.02,E0+0.02))
    Em,_,_=find_E(lambda r:base(r)-eps*hfun(r),
                  lambda r:basep(r)-eps*(hfun(r+1e-6)-hfun(r-1e-6))/2e-6,
                  m,k,rgrid,(E0-0.02,E0+0.02))
    return (Ep-Em)/(2*eps)

shape=source_shape(G0,F0,base,basep,m,k,rgrid)
profiles={
 'g1':lambda r:np.exp(-((r-2.5)/0.6)**2),
 'g2':lambda r:np.exp(-((r-3.5)/0.6)**2),
 'g3':lambda r:np.exp(-((r-4.5)/0.8)**2),
}
print("\nFH test: compare dE/deps[h]  vs  INT h*shape dr  (should be proportional, same ratio)")
ratios=[]
for nm,h in profiles.items():
    num=dE_deps(h)
    overlap=simpson(h(rgrid)*shape,rgrid)
    print(f"  {nm}: dE/deps={num:+.6e}  INT h*shape={overlap:+.6e}  ratio={num/overlap:+.4f}")
    ratios.append(num/overlap)
print("ratio spread (should be ~constant if shape correct):", np.std(ratios)/np.mean(ratios))
