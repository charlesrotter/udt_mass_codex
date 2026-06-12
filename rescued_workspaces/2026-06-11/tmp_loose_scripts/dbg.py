import numpy as np
from scipy.linalg import eigvalsh_tridiagonal, eigh_tridiagonal

def build_mesh(rmin, R, rmax, n_int, n_ext):
    g_int = np.exp(np.linspace(np.log(rmin), np.log(R), n_int))
    g_int[-1] = R
    if rmax > R:
        g_ext = np.linspace(R, rmax, n_ext + 1)[1:]
        return np.concatenate([g_int, g_ext]), n_int - 1
    return g_int, n_int - 1

q, s, lam, R = 1/3, 1/9, 2.0, 1.0
r, im = build_mesh(1e-5, 1.0, 1.0, 1000, 0)
print("im", im, "r[im]", r[im], "N", len(r))
h = np.diff(r); rm = 0.5*(r[:-1]+r[1:])
f = (R/rm)**q
Pm = rm**2*f**2
Qm = lam*f + 4*f**2*s
Wm = rm**2
N = len(r)
Qn = np.zeros(N); Wn = np.zeros(N)
Qn[:-1] += Qm*h/2; Qn[1:] += Qm*h/2
Wn[:-1] += Wm*h/2; Wn[1:] += Wm*h/2
for gamma in (0.0, 2/3, 2.0):
    Qn2 = Qn.copy(); Qn2[im] -= gamma
    cp = Pm/h
    d = np.zeros(N); d[:-1] += cp; d[1:] += cp
    idx = np.arange(1, N)   # BC-c: Robin natural at last node
    diag = d[idx] + Qn2[idx]
    off = -cp[idx[:-1]+0]   # conductance between idx[j], idx[j+1] = cp[idx[j]]
    sw = 1.0/np.sqrt(Wn[idx])
    dt = diag*sw**2; et = off*sw[:-1]*sw[1:]
    vals = eigvalsh_tridiagonal(dt, et, select='i', select_range=(0, 2))
    print(f"gamma={gamma}: theta_min {vals[:3]}, omega2_top={-vals[0]:.6f}")
