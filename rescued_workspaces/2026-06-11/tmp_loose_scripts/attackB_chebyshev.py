"""ATTACK B: independent re-computation of the claimed eigenvalues with a
COMPLETELY different scheme: Chebyshev spectral collocation, in the
x = ln(r/R) variable, on the Liouville-transformed psi-equation
   psi'' = (lam e^{qx} + mu^2 + W e^{(2+2q)x}) psi,   W = omega^2 R^2,
   u = e^{-(1-2q)x/2} psi,  mu = sqrt(1+4q(1-q))/2.
(The target script uses a log-mesh 2nd-order FD on u in r plus RK shooting;
nothing here shares its discretization, variable, or BC implementation.)

BCs:
  core x0:  psi'/psi = mu + c1 q e^{q x0}/(1 + c1 e^{q x0}),
            c1 = lam/(q^2 + 2 mu q)   [Friedrichs branch series]
  x=0 BC-c: u'/u = gamma  =>  psi'/psi = gamma + (1-2q)/2
  x=0 BC-b: psi(0) = 0
Targets: BC-c lam=2 gamma=2/3: -3.4667814 ; lam=6: -10.376405
         BC-b lam=2: -27.334956 ; lam=6: -41.213694
         boosted BC-c gamma=1.5*L0(2)=2.0075251: +4.0701100
"""
import numpy as np
from scipy.linalg import eig

q = 1.0/3.0
mu = np.sqrt(1+4*q*(1-q))/2

def cheb(N):
    if N == 0:
        return np.zeros((1,1)), np.array([1.0])
    xi = np.cos(np.pi*np.arange(N+1)/N)
    c = np.hstack([2., np.ones(N-1), 2.])*(-1)**np.arange(N+1)
    X = np.tile(xi, (N+1,1)).T
    dX = X - X.T
    D = np.outer(c, 1./c)/(dX + np.eye(N+1))
    D -= np.diag(D.sum(axis=1))
    return D, xi

def top_eig(lam, gamma, bc, x0=-25.0, N=300):
    D, xi = cheb(N)
    sc = 2.0/(0.0 - x0)              # x = x0 + (xi+1)/sc' ... affine
    x = x0 + (xi+1)/2*(0.0-x0)       # xi=1 -> x=0, xi=-1 -> x=x0
    Dx = sc*D
    A = Dx@Dx - np.diag(lam*np.exp(q*x) + mu**2)
    B = np.diag(np.exp((2+2*q)*x))
    # BC rows: index 0 is x=0 (xi=1), index N is x=x0
    c1 = lam/(q**2 + 2*mu*q)
    mcore = mu + c1*q*np.exp(q*x0)/(1+c1*np.exp(q*x0))
    A[N,:] = Dx[N,:]; A[N,N] -= mcore; B[N,:] = 0
    if bc == 'c':
        A[0,:] = Dx[0,:]; A[0,0] -= (gamma + (1-2*q)/2); B[0,:] = 0
    else:  # 'b' Dirichlet
        A[0,:] = 0; A[0,0] = 1.0; B[0,:] = 0
    w = eig(A, B, right=False)
    w = w[np.isfinite(w)]
    w = w[np.abs(w.imag) < 1e-6*np.maximum(1, np.abs(w.real))].real
    w = w[w < 1e6]
    return np.sort(w)[::-1]

print("ATTACK B: Chebyshev collocation (independent scheme)")
print(f"{'case':34s} {'N=240,x0=-20':>14s} {'N=300,x0=-25':>14s} "
      f"{'N=360,x0=-30':>14s}   claim")
cases = [
    ("BC-c lam=2 gamma=2/3 (top)", 2.0, 2.0/3.0, 'c', -3.4667814),
    ("BC-c lam=6 gamma=2/3 (top)", 6.0, 2.0/3.0, 'c', -10.376405),
    ("BC-b lam=2 (top)",           2.0, 0.0,     'b', -27.334956),
    ("BC-b lam=6 (top)",           6.0, 0.0,     'b', -41.213694),
    ("BC-c lam=2 gamma=1.5*L0",    2.0, 1.5*1.3383500854650566, 'c', +4.0701100),
]
for name, lam, g, bc, claim in cases:
    vals = [top_eig(lam, g, bc, x0=x0, N=N)[0]
            for x0, N in ((-20.0,240), (-25.0,300), (-30.0,360))]
    print(f"{name:34s} {vals[0]:+14.7f} {vals[1]:+14.7f} {vals[2]:+14.7f}"
          f"   {claim:+.7f}")

# second eigenvalues too (BC-c lam=2), as extra structure check
v = top_eig(2.0, 2/3, 'c', x0=-25.0, N=300)
print("\nBC-c lam=2 top three eigenvalues:", np.round(v[:3], 5))

# threshold bracket independent: gamma scan around L0
L0 = 1.3383500854650566
for fac in (0.97, 0.99, 1.0, 1.01, 1.03):
    t = top_eig(2.0, fac*L0, 'c', x0=-25.0, N=300)[0]
    print(f"  gamma = {fac:4.2f}*L0: top W = {t:+.6e}")
