import numpy as np
from scipy.linalg import eigvalsh_tridiagonal
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.special import kv, kvp

def aplus(q, s):
    return (-(1-2*q) + np.sqrt((1-2*q)**2 + 16*s))/2.0

def build_mesh(rmin, R, rmax, n_int, n_ext):
    g_int = np.exp(np.linspace(np.log(rmin), np.log(R), n_int))
    g_int[-1] = R
    if rmax > R:
        g_ext = np.linspace(R, rmax, n_ext + 1)[1:]
        return np.concatenate([g_int, g_ext]), n_int - 1  # index of R
    return g_int, n_int - 1

def P_of(r, q, R):
    f = np.where(r <= R, (R/r)**q, 1.0)
    return r**2 * f**2

def Qbulk_of(r, q, s, R, lam):
    f = np.where(r <= R, (R/r)**q, 1.0)
    E0 = np.where(r <= R, s/r**2, 0.0)
    return lam*f + 4*r**2*f**2*E0

def top_eigs(q, s, lam, R=1.0, rmin=1e-5, rmax=None, n_int=4000,
             n_ext=4000, bc='a', gamma=None, k=4):
    """Top-k omega^2 of (P u')' - Q u + gamma*delta_R u = w2 r^2 u.
    bc: 'a' exterior-matching (Dirichlet at rmax), 'b' Dirichlet at R,
    'c' Robin-natural at R (interior only). gamma: delta strength
    (default 2q/R); set 0 for no-delta control."""
    if gamma is None:
        gamma = 2*q/R
    if bc == 'a':
        assert rmax is not None and rmax > R
        r, im = build_mesh(rmin, R, rmax, n_int, n_ext)
    else:
        r, im = build_mesh(rmin, R, R, n_int, 0)
    h = np.diff(r)
    rm = 0.5*(r[:-1] + r[1:])
    # avoid midpoint straddling: interior cells have rm<R, ok by mesh
    Pm = P_of(rm, q, R)
    Qm = Qbulk_of(rm, q, s, R, lam)
    Wm = rm**2
    N = len(r)
    # node-based lumped Q and W: cell contributions split half-half
    Qn = np.zeros(N); Wn = np.zeros(N)
    Qn[:-1] += Qm*h/2; Qn[1:] += Qm*h/2
    Wn[:-1] += Wm*h/2; Wn[1:] += Wm*h/2
    Qn[im] -= gamma * (1.0 if bc != 'b' else 0.0)  # delta (does no work for b)
    # unknowns: Dirichlet at node 0 always; at last node for bc 'a','b';
    # last node free (natural) for bc 'c'
    if bc == 'c':
        idx = np.arange(1, N)
    else:
        idx = np.arange(1, N-1)
    cp = Pm/h  # cell conductances
    d = np.zeros(N); 
    d[:-1] += cp; d[1:] += cp
    diag = (d[idx] + Qn[idx])
    off = -cp[idx[:-1]]
    # generalized -> standard via W^{-1/2}
    s_w = 1.0/np.sqrt(Wn[idx])
    dt = diag*s_w**2
    et = off*s_w[:-1]*s_w[1:]
    nn = len(idx)
    vals = eigvalsh_tridiagonal(dt, et, select='i',
                                select_range=(0, k-1))
    return -vals  # omega^2 = -theta

q, s = 1/3, 1/9
for lam in (2.0, 6.0):
    a = top_eigs(q, s, lam, rmax=20.0, bc='a')
    a2 = top_eigs(q, s, lam, rmax=40.0, bc='a')
    b = top_eigs(q, s, lam, bc='b')
    c = top_eigs(q, s, lam, bc='c')
    a0 = top_eigs(q, s, lam, rmax=20.0, bc='a', gamma=0.0)
    print(f"lam={lam}: BC-a top {a[0]:.6e} (rmax 20) {a2[0]:.6e} (rmax 40)"
          f" no-delta {a0[0]:.6e}")
    print(f"         BC-b top {b[0]:.8f}  BC-c top {c[0]:.8f}")

# boosted-gamma control (decoupled): gamma above gamma_c must bind (BC-c)
print()
gc_c = 1.338350085  # L0(q=1/3,lam=2)
for fac in (0.95, 1.05, 1.5):
    c = top_eigs(q, s, 2.0, bc='c', gamma=fac*gc_c)
    print(f"BC-c lam=2 gamma={fac}*gamma_c: top {c[0]:+.8f}")
# boosted BC-a
gc_a = 1.338350085 + 2.0
for fac in (0.95, 1.2):
    a = top_eigs(q, s, 2.0, rmax=20.0, bc='a', gamma=fac*gc_a)
    a2 = top_eigs(q, s, 2.0, rmax=40.0, bc='a', gamma=fac*gc_a)
    print(f"BC-a lam=2 gamma={fac}*gamma_c: top {a[0]:+.8f} (20) {a2[0]:+.8f} (40)")
