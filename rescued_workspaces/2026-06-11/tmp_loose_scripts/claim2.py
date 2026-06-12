import numpy as np
from scipy.linalg import eigh_tridiagonal

# Build 1D Hamiltonian u'' + (lam - V)u = 0  ->  -u'' + V u = lam u
# FD on [0,L] with Dirichlet u(0)=0 always (the LEFT hard node).
def solve(V_func, L, N, right='dirichlet'):
    # interior grid points x_1..x_{N} with spacing h; node at x=0 (index 0) enforced.
    h = L/(N+1)
    x = np.arange(1,N+1)*h
    V = V_func(x)
    diag = 2.0/h**2 + V
    off = -1.0/h**2*np.ones(N-1)
    if right=='neumann':
        # Neumann at x=L: u'(L)=0. Use ghost-point: last diagonal modified.
        # standard: -u''(x_N) with u_{N+1}=u_N (zero derivative) -> diag adjustment
        diag = diag.copy()
        diag[-1] = 1.0/h**2 + V[-1]
    w, v = eigh_tridiagonal(diag, off)
    return w, x, h

# --- Triangular well: V = s*x, left node u(0)=0, soft turning point at x_tp=lam/s ---
s = 1.0
L = 60.0
N = 6000
w,_,_ = solve(lambda x: s*x, L, N)
print("Triangular well (node + soft turning point), expect delta=3/4:")
for n in range(8):
    lam = w[n]
    xtp = lam/s
    phase = (2.0/3.0)*lam**1.5/s   # integral_0^xtp sqrt(lam - s x) dx = (2/3) lam^{3/2}/s
    delta = phase/np.pi - n
    print(f"  n={n} lam={lam:.5f} x_tp={xtp:.3f} phase/pi={phase/np.pi:.5f} -> n+delta, delta={delta:.4f}")

# Compare to exact: triangular well eigenvalues = s^{2/3} * (-a_n) where a_n are Airy zeros
from scipy.special import ai_zeros
a, ap, aiz, aipz = ai_zeros(8)
print("\n  exact lam_n (Airy zeros, s=1):", [f"{-a[n]:.5f}" for n in range(5)])

# --- Flat well, Dirichlet both ends: V=0 on [0,L], expect delta=0 ---
print("\nFlat well Dirichlet-Dirichlet (expect delta=0):")
Lf=10.0; Nf=8000
w0,_,_ = solve(lambda x: 0*x, Lf, Nf, right='dirichlet')
for n in range(5):
    lam=w0[n]; k=np.sqrt(lam)
    phase=k*Lf  # int_0^L k dx
    delta=phase/np.pi-(n+1)   # n+1 because lowest DD mode is half-wave (n starts 0 -> 1 antinode)
    print(f"  n={n} lam={lam:.5f} k*L/pi={phase/np.pi:.5f} delta(vs n+1)={delta:.5f}")

# --- Flat well, Dirichlet-Neumann: V=0, left node right antinode, expect delta=1/2 ---
print("\nFlat well Dirichlet-Neumann (expect delta=1/2):")
wn,_,_ = solve(lambda x: 0*x, Lf, Nf, right='neumann')
for n in range(5):
    lam=wn[n]; k=np.sqrt(lam)
    phase=k*Lf
    delta=phase/np.pi-n
    print(f"  n={n} lam={lam:.5f} k*L/pi={phase/np.pi:.5f} delta={delta:.5f}  (expect 0.5)")
