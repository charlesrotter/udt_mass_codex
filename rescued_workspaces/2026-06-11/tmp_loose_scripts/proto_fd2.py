import numpy as np
import scipy.sparse as sps
from scipy.sparse.linalg import eigsh

def assemble(q, s, lam, R=1.0, rmin=1e-5, rmax=None, n_int=4000,
             n_ext=4000, bc='a', gamma=None):
    if gamma is None:
        gamma = 2*q   # dimensionless (R=1) — generalize later
    g_int = np.exp(np.linspace(np.log(rmin), np.log(R), n_int)); g_int[-1] = R
    if bc == 'a':
        g_ext = np.linspace(R, rmax, n_ext + 1)[1:]
        r = np.concatenate([g_int, g_ext]); im = n_int - 1
    else:
        r = g_int; im = n_int - 1
    h = np.diff(r); rm = 0.5*(r[:-1] + r[1:])
    f = np.where(rm <= R, (R/rm)**q, 1.0)
    E0 = np.where(rm <= R, s/rm**2, 0.0)
    Pm = rm**2*f**2
    Qm = lam*f + 4*rm**2*f**2*E0
    Wm = rm**2
    N = len(r)
    Qn = np.zeros(N); Wn = np.zeros(N)
    Qn[:-1] += Qm*h/2; Qn[1:] += Qm*h/2
    Wn[:-1] += Wm*h/2; Wn[1:] += Wm*h/2
    if bc != 'b':
        Qn[im] -= gamma * R**2 / R  # = gamma (R=1); delta term -(2q/R)*R^2*f^2... see notes
    cp = Pm/h
    d = np.zeros(N); d[:-1] += cp; d[1:] += cp
    idx = np.arange(1, N) if bc == 'c' else np.arange(1, N-1)
    Kdiag = d[idx] + Qn[idx]
    Koff = -cp[1:1+len(idx)-1]
    A = -sps.diags([Koff, Kdiag, Koff], [-1, 0, 1], format='csc')
    W = sps.diags(Wn[idx], 0, format='csc')
    return A, W

def top_eigs(*args, k=4, sigma=50.0, **kw):
    A, W = assemble(*args, **kw)
    vals = eigsh(A, k=k, M=W, sigma=sigma, which='LM',
                 return_eigenvectors=False)
    return np.sort(vals)[::-1]

q, s = 1/3, 1/9
for lam in (2.0, 6.0):
    a  = top_eigs(q, s, lam, rmax=20.0, bc='a')
    a2 = top_eigs(q, s, lam, rmax=40.0, bc='a')
    b  = top_eigs(q, s, lam, bc='b')
    c  = top_eigs(q, s, lam, bc='c')
    a0 = top_eigs(q, s, lam, rmax=20.0, bc='a', gamma=0.0)
    print(f"lam={lam}: BC-a top {a[0]:+.6f} (rmax20) {a2[0]:+.6f} (rmax40)"
          f" no-delta {a0[0]:+.6f}")
    print(f"          BC-b top {b[0]:+.8f}  BC-c top {c[0]:+.8f}")

print()
gcc = 1.338350085465  # L0(1/3,1/9,2)
for fac in (0.95, 1.05, 1.5):
    c = top_eigs(q, s, 2.0, bc='c', gamma=fac*gcc)
    print(f"BC-c lam=2 gamma={fac:>4}*gamma_c: top {c[0]:+.8f}")
gca = gcc + 2.0
for fac in (0.95, 1.2):
    a  = top_eigs(q, s, 2.0, rmax=20.0, bc='a', gamma=fac*gca)
    a2 = top_eigs(q, s, 2.0, rmax=40.0, bc='a', gamma=fac*gca)
    print(f"BC-a lam=2 gamma={fac:>4}*gamma_c: top {a[0]:+.8f} (20) {a2[0]:+.8f} (40)")
