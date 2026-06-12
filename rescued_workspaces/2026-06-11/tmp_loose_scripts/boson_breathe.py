import numpy as np
from scipy.linalg import eigh_tridiagonal
# Breathing SL: -((2+r)^2 u')' = w^2 r^2 u  on (eps, L), u'(0)~0 regular, u(L)=0 box.
# Discretize generalized eig A u = w^2 B u, A=stiffness from -(p u')', p=(2+r)^2, B=diag(r^2).
def solve(L, N=6000, eps=1e-3):
    r = np.linspace(eps, L, N); h = r[1]-r[0]
    p = (2+r)**2
    ph = (2+(r+h/2))**2            # p at half points
    plo = (2+(r-h/2))**2
    # -(p u')' ~ [ -plo u_{i-1} + (plo+phi) u_i - phi u_{i+1} ] / h^2
    diag = (plo+ph)/h**2
    off  = -ph[:-1]/h**2
    w2 = r**2
    # generalized symmetric tridiagonal: divide by sqrt(w2) on both sides -> standard
    # A x = lam B x ; B=diag(w2). Symmetrize: C = B^{-1/2} A B^{-1/2}
    s = np.sqrt(w2)
    d = diag/w2
    e = off/(s[:-1]*s[1:])
    vals = eigh_tridiagonal(d, e, select='i', select_range=(0,8))[0]
    return vals
print("Breathing eigenvalues w^2 vs BOX SIZE L (continuum -> all scale ~1/L^2; bound -> lowest box-independent):")
print(f"  {'L':>5}  {'lowest 6 w^2':>50}")
for L in [20, 40, 80, 160]:
    v = solve(L)
    print(f"  {L:5.0f}  "+", ".join(f"{x:.5f}" for x in v[:6]))
print("\n  ALSO: w^2 * L^2 (if ~constant down a column -> these are BOX modes = continuum, no gap):")
for L in [20,40,80,160]:
    v=solve(L)
    print(f"  L={L:4.0f}: w^2*L^2 = "+", ".join(f"{x*L*L:.2f}" for x in v[:5]))
# gap check: is there a lowest w^2 that stays put as L grows (a bound mode) or does everything -> 0?
print("\n  lowest w^2 vs L (does it -> 0 [continuum] or plateau [bound mode]?):")
for L in [20,40,80,160,320]:
    print(f"    L={L:4.0f}: w0^2={solve(L)[0]:.6f}")
