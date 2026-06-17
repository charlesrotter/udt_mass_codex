"""
CLEAN final solver. Solve the SL form DIRECTLY in r (no tortoise interpolation),
generalized eigenproblem with proper consistent FE, robust banded generalized eig.
  -(p u')' = E (P/f) u ,  p = P f = 2r^2 e^{-2phi}, weight rho = P/f = 2r^2 e^{2phi}
  regular core (natural BC), Dirichlet wall.
Use scipy.linalg.eigh with banded? Use eig of generalized via Cholesky of consistent
SPD mass (banded). We use scipy.linalg.eigh on banded via 'eigvals' with b.
To stay fast & correct: build sparse, use eigsh shift-invert with sigma slightly
below 0 ... but that was slow. Instead: Cholesky-banded reduce by hand is messy.

Simplest reliable: moderate N=3000 dense generalized eigh (consistent mass).
This matched mpmath earlier (0.2862 vs 0.28616). Trust it. Scan R_wall.
"""
import numpy as np
from scipy.linalg import eigh

def SL_dense(phi_fun, R_wall, N=2500, r0=1e-6):
    r = np.linspace(r0, R_wall, N)
    h = r[1]-r[0]
    f = np.exp(-2*phi_fun(r))
    p = 2*r**2*f
    rho = 2*r**2/f
    rh = 0.5*(r[:-1]+r[1:]); ph = np.interp(rh, r, p); rhoh = np.interp(rh, r, rho)
    Kmain=np.zeros(N); Koff=np.zeros(N-1); Mmain=np.zeros(N); Moff=np.zeros(N-1)
    for el in range(N-1):
        ke=ph[el]/h; Kmain[el]+=ke; Kmain[el+1]+=ke; Koff[el]-=ke
        me=rhoh[el]*h; Mmain[el]+=me/3; Mmain[el+1]+=me/3; Moff[el]+=me/6
    K=np.diag(Kmain)+np.diag(Koff,1)+np.diag(Koff,-1)
    M=np.diag(Mmain)+np.diag(Moff,1)+np.diag(Moff,-1)
    K=K[:-1,:-1]; M=M[:-1,:-1]   # Dirichlet wall; regular core natural
    w=eigh(K,M,eigvals_only=True, subset_by_index=[0,3])
    return np.sort(w)

def make_tanh_well(phi0,R0,sharp):
    def phi(r): return phi0*0.5*(1-np.tanh((r-R0)/sharp));
    return phi
def make_gaussian(phi0,width):
    def phi(r): return phi0*np.exp(-(r/width)**2)
    return phi
def make_hedgehog(phi0):
    def phi(r): return phi0*np.exp(-(r/0.7)**2)+0.25*abs(phi0)*np.exp(-((r-1.3)/0.4)**2)
    return phi

print("CLEAN SL generalized eig (consistent mass, N=2500). E0=omega0^2.")
print("Pure box <=> E0*R_wall^2 ~ const.  Bound state <=> E0 -> positive const.\n")
profs = {
 "gauss phi0=-0.8": make_gaussian(-0.8,1.0),
 "gauss phi0=-3.0": make_gaussian(-3.0,1.0),
 "tanh phi0=-3.0":  make_tanh_well(-3.0,1.0,0.3),
 "tanh phi0=-5.0":  make_tanh_well(-5.0,1.0,0.3),
 "hedgehog phi0=-0.8": make_hedgehog(-0.8),
}
for name,phi in profs.items():
    print(f"--- {name} ---")
    print(f"{'R_wall':>7} {'E0':>14} {'E0*Rw^2':>12} {'E1':>13}")
    for Rw in [4.,8.,16.,32.]:
        w=SL_dense(phi,Rw)
        print(f"{Rw:7.1f} {w[0]:14.6e} {w[0]*Rw**2:12.4f} {w[1]:13.5e}")
    print()
