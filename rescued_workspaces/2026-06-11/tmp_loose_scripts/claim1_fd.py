import numpy as np
from scipy.integrate import solve_ivp

# We test the SOURCE FORMULA via the variational identity it must satisfy:
#   dS_Dirac/dphi(r)  =  -sqrt(-g) (T^r_r - T^t_t)   [collapse, verified symbolically]
# and the claim:
#   T^r_r - T^t_t = -2 sigma [ kappa(F^2-G^2)/r + PHI'(F^2+G^2) + m e^{PHI} GF ]
# with PHI = -phi (sigma=-1).
#
# To make this checkable WITHOUT the full spin-connection Dirac action, we use the
# Form-T action whose Euler-Lagrange equations ARE the given G',F' system, and vary it wrt phi.
#
# The first-order Dirac radial system can be derived from a Lagrangian density (per unit r,
# already angular-integrated). A standard first-order action giving
#   G' = (PHI'-k/r)G + (E e^{2PHI}+ m e^{PHI})F
#   F' = (PHI'+k/r)F - (E e^{2PHI}- m e^{PHI})G
# is
#   L = G F' - F G' + (2k/r) GF - 2 PHI' GF  ... we must reverse-engineer it.
# Instead, do the cleaner thing: take the EXACT formula for (T^r_r - T^t_t) as the source S(r),
# and independently verify it is the variational derivative of the Dirac energy functional
# wrt a LOCAL change phi(r)->phi(r)+eps*delta(r), via the Feynman-Hellmann theorem applied to
# the radial Hamiltonian. That ties the source to the operator the claim itself defines.

# Radial Dirac as eigenproblem H psi = E psi.  Write the system as
#   G' = (PHI' - k/r)G + (E e^{2PHI} + m e^{PHI}) F
#   F' = (PHI' + k/r)F - (E e^{2PHI} - m e^{PHI}) G
# Solve for E as eigenvalue with bound-state BCs in a fixed background phi(r).
# Then Feynman-Hellmann: dE/d(param) = <d H/d param>.
# If we perturb phi at radius r by phi->phi+eps h(r), the change in E (at fixed normalization
# INT(G^2+F^2)dr =1) equals INT h(r) * [functional derivative]. We compare that derivative
# to the claimed (T^r_r - T^t_t) shape.

# Build H so that (G,F)'=A(r)(G,F). Multiply eqs to isolate. Cast as generalized eigenproblem:
# It's a first-order Dirac op. Use a smooth localized background and shoot for E.

def make_background(kind='tanhwell', A=0.6, r0=3.0, w=1.0):
    # PHI(r) = A * something localized, PHI=-phi
    def PHI(r):  return A*np.exp(-((r-r0)/w)**2)
    def PHIp(r): return A*np.exp(-((r-r0)/w)**2)*(-2*(r-r0)/w**2)
    return PHI, PHIp

def solve_mode(E, m, k, PHI, PHIp, rgrid):
    def rhs(r, y):
        G,F = y
        p = PHI(r); pp = PHIp(r)
        e2 = np.exp(2*p); e1 = np.exp(p)
        Gp = (pp - k/r)*G + (E*e2 + m*e1)*F
        Fp = (pp + k/r)*F - (E*e2 - m*e1)*G
        return [Gp, Fp]
    # start near r=rmin with small-r behavior G~r^{|k|}, pick a seed
    r0 = rgrid[0]
    if k<0:
        y0=[r0**(abs(k)), 1e-3]
    else:
        y0=[1e-3, r0**(abs(k))]
    sol = solve_ivp(rhs, [rgrid[0],rgrid[-1]], y0, t_eval=rgrid, rtol=1e-9, atol=1e-12, dense_output=True)
    return sol

# Eigenvalue via shooting: bound state => F (or G) ->0 at large r. Match by requiring decay.
def shoot_residual(E, m, k, PHI, PHIp, rgrid):
    sol = solve_mode(E,m,k,PHI,PHIp,rgrid)
    G,F = sol.y
    return G[-1]  # want -> 0 for bound large-r decay (heuristic)

from scipy.optimize import brentq
PHI,PHIp = make_background(A=0.6)
rgrid=np.linspace(0.05, 20, 6000)
m=0.5; k=-1
# scan for sign change of residual
Es=np.linspace(0.01*m, 0.999*m, 200)
res=[shoot_residual(E,m,k,PHI,PHIp,rgrid) for E in Es]
res=np.array(res)
sign=np.where(np.diff(np.sign(res)))[0]
print("candidate E brackets:", [(Es[i],Es[i+1]) for i in sign][:5])
