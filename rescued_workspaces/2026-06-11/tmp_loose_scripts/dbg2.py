import numpy as np
from scipy.linalg import eigvalsh_tridiagonal, eigh

def assemble(rmin, n_int, gamma, q=1/3, s=1/9, lam=2.0):
    r = np.exp(np.linspace(np.log(rmin), 0.0, n_int)); r[-1] = 1.0
    h = np.diff(r); rm = 0.5*(r[:-1]+r[1:])
    f = rm**(-q)
    Pm = rm**2*f**2; Qm = lam*f + 4*f**2*s; Wm = rm**2
    N = len(r)
    Qn = np.zeros(N); Wn = np.zeros(N)
    Qn[:-1] += Qm*h/2; Qn[1:] += Qm*h/2
    Wn[:-1] += Wm*h/2; Wn[1:] += Wm*h/2
    Qn[-1] -= gamma
    cp = Pm/h
    d = np.zeros(N); d[:-1] += cp; d[1:] += cp
    idx = np.arange(1, N)
    diag = d[idx] + Qn[idx]
    off = -cp[1:]  # cp[j] couples nodes j,j+1; for idx nodes 1..N-1: cp[1..N-2]
    return diag, off, Wn[idx], r

diag, off, W, r = assemble(1e-5, 300, 2.0)
# dense generalized check
n = len(diag)
K = np.diag(diag) + np.diag(off, 1) + np.diag(off, -1)
vals = eigh(K, np.diag(W), eigvals_only=True)
print("dense gen eig: min 3:", vals[:3])
# tridiag reduction
sw = 1/np.sqrt(W)
dt = diag*sw**2; et = off*sw[:-1]*sw[1:]
v2 = eigvalsh_tridiagonal(dt, et, select='i', select_range=(0,2))
print("tridiag reduction:", v2)
v3 = eigvalsh_tridiagonal(dt, et)  # all
print("all, min 3:", np.sort(v3)[:3])
# Rayleigh of continuum-informed trial: zero-energy interior solution approx rho^L0
u = r[1:]**1.3383
num = np.sum((np.diff(np.r_[0.0, u]) if False else 0))
# compute form directly
uu = np.r_[0.0, u]  # include dirichlet node
hh = np.diff(r); rm = 0.5*(r[:-1]+r[1:]); f = rm**(-1/3)
Pm = rm**2*f**2; Qm = 2.0*f + 4*f**2/9
B = np.sum(Pm*np.diff(uu)**2/hh) + np.sum(Qm*(0.5*(uu[:-1]**2+uu[1:]**2))*hh) - 2.0*uu[-1]**2
Wq = np.sum(rm**2*0.5*(uu[:-1]**2+uu[1:]**2)*hh)
print("trial Rayleigh:", B/Wq)
