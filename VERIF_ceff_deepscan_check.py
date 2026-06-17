"""
PART 3b: AGGRESSIVE deep-well scan with FAST robust solvers.

Two independent discretizations:
 (A) Schrodinger/Liouville-normal form: -psi'' + V psi = E psi on tortoise x,
     V = -2 phi' f^2/r, Dirichlet both ends -> symmetric TRIDIAGONAL -> eigh_tridiagonal.
 (B) SL form (P f u')' + E (P/f) u = 0 via mass-orthonormalization:
     lumped diagonal mass M (SPD) -> solve standard eig of M^{-1/2} K M^{-1/2} (tridiag).

If a true intrinsic bound state exists, E0 = omega0^2 -> POSITIVE constant as R_wall->inf.
Pure box: E0 ~ const/R_wall^2 -> 0.
"""
import numpy as np
from scipy.linalg import eigh_tridiagonal

def schro(phi_fun, phip_fun, R_wall, N=20000):
    r = np.linspace(1e-7, R_wall, N)
    dr = r[1]-r[0]
    f = np.exp(-2*phi_fun(r))
    x = np.concatenate([[0.0], np.cumsum(0.5*(1/f[1:]+1/f[:-1])*dr)])
    V = -2*phip_fun(r)*f**2/r
    xu = np.linspace(x[0], x[-1], N)
    Vu = np.interp(xu, x, V)
    hx = xu[1]-xu[0]
    d = 2/hx**2 + Vu[1:-1]
    e = -1/hx**2*np.ones(len(d)-1)
    w = eigh_tridiagonal(d, e, select='i', select_range=(0,3))[0]
    return np.sort(w)

def SL_lumped(phi_fun, R_wall, N=20000):
    # nodes 0..N-1, Dirichlet at last node, regular (natural) at node 0.
    r = np.linspace(1e-7, R_wall, N)
    h = r[1]-r[0]
    f = np.exp(-2*phi_fun(r))
    p = 2*r**2*f
    rh = 0.5*(r[:-1]+r[1:]); ph = np.interp(rh, r, p)
    rho = 2*r**2/f
    n = N-1   # drop wall node
    # stiffness tridiagonal
    Kmain = np.zeros(n); Koff = np.zeros(n-1)
    for e_ in range(n):   # elements among kept nodes; element e_ connects e_, e_+1
        if e_ < n: pass
    # build properly: elements 0..N-2; kept nodes 0..n-1 (=N-2). element e connects e,e+1
    Kmain = np.zeros(N); Koff = np.zeros(N-1)
    for el in range(N-1):
        ke = ph[el]/h
        Kmain[el]+=ke; Kmain[el+1]+=ke; Koff[el]-=ke
    # lumped mass at nodes
    Mdiag = rho*h
    Mdiag[0]*=0.5; Mdiag[-1]*=0.5
    # drop wall node (last)
    Kmain=Kmain[:-1]; Koff=Koff[:-1]; Mdiag=Mdiag[:-1]
    # standard tridiag: A = D^{-1/2} K D^{-1/2}
    s = 1/np.sqrt(Mdiag)
    d = Kmain*s*s
    off = Koff*s[:-1]*s[1:]
    w = eigh_tridiagonal(d, off, select='i', select_range=(0,3))[0]
    return np.sort(w)   # do NOT filter -- a negative E0 would itself be a finding

def make_tanh_well(phi0, R0, sharp):
    def phi(r): return phi0*0.5*(1-np.tanh((r-R0)/sharp))
    def phip(r): return phi0*0.5*(-(1/sharp)/np.cosh((r-R0)/sharp)**2)
    return phi, phip
def make_gaussian(phi0, width):
    def phi(r): return phi0*np.exp(-(r/width)**2)
    def phip(r): return phi0*np.exp(-(r/width)**2)*(-2*r/width**2)
    return phi, phip

print("DEEP WELL aggressive scan, N=20000, R_wall up to 48 (8x)")
for name,(phi,phip) in [("tanh phi0=-3.0",make_tanh_well(-3.0,1.0,0.3)),
                        ("tanh phi0=-5.0",make_tanh_well(-5.0,1.0,0.3)),
                        ("gauss phi0=-3.0",make_gaussian(-3.0,1.0)),
                        ("gauss phi0=-0.8",make_gaussian(-0.8,1.0))]:
    print(f"\n--- {name} ---")
    print(f"{'R_wall':>7} {'E0(SL)':>14} {'E0*Rw^2':>12} {'E0(Schr)':>14} {'E0(Schr)*Rw^2':>14}")
    for Rw in [6.,12.,24.,48.]:
        sl = SL_lumped(phi, Rw)
        sc = schro(phi, phip, Rw)
        print(f"{Rw:7.1f} {sl[0]:14.6e} {sl[0]*Rw**2:12.3e} {sc[0]:14.6e} {sc[0]*Rw**2:14.3e}")
