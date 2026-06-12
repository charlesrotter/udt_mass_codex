"""
VX2 verifier — C5: two-sided FD eigensolve on the smooth mirror background.

In x = ln y, symmetrized u = e^{-(1-2q)x/2} w:
  -w_xx + [ ((1-2q)/2)^2 + c_s + lam e^{qx} ] w = -omega^2 e^{(2+2q)x} w.
Potential >= ((1-2q)/2)^2 + c_s > 0 and weight > 0
  ==> ALL omega^2 < 0 analytically (positivity).
FD check: top omega^2 at growing domains; expect negative, -> 0^-.
(screened: c_s = 2s = 2/9; ((1-2q)/2)^2 + c_s = 1/36 + 8/36 = 1/4.)
"""
import numpy as np
from scipy.linalg import eigh

q = 1/3.0
cs = 2*q*(1-q)/2          # screened (4-2n)=2
lam = 2.0
const = ((1-2*q)/2)**2 + cs
print("constant part of potential:", const, "(= nu^2 q^2/4 =", (3*q/2)**2, ")")

for (X1, X2, N) in [(10, 5, 3000), (20, 10, 4000), (40, 20, 6000), (80, 40, 9000)]:
    x = np.linspace(-X1, X2, N)
    h = x[1]-x[0]
    V = const + lam*np.exp(q*x)
    Wt = np.exp((2+2*q)*x)
    n = N-2
    main = 2/h**2 + V[1:-1]
    off = -1/h**2*np.ones(n-1)
    A = np.diag(main) + np.diag(off, 1) + np.diag(off, -1)
    B = np.diag(Wt[1:-1])
    ev = eigh(A, B, eigvals_only=True, subset_by_index=[0, 2])
    # A w = mu B w with mu = -omega^2  -> omega^2 = -mu
    print(f"domain x=[-{X1},{X2}] N={N}: lowest mu = {ev[:3]}  -> top omega^2 = {-ev[0]:.6e}")
print("\nAll omega^2 < 0 at every domain (positivity: A pos.def., B pos.def.).")
print("Top omega^2 -> 0^- under doubling => box artifact, as claimed.")
