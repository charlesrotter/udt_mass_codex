"""
BLIND VERIFIER — CLAIM 3: standing-wave spectrum = intrinsic centrifugal FLOOR + box-controlled CONTINUUM.
INDEPENDENT eigensolver. Two discretizations:
  (1) dense symmetric FD on the SL operator -(P U')' + [l(l+1)W + Q] U  (Liouville-transformed to symmetric tridiag)
  (2) a second-derivative-matrix check via different node spacing.
The dressed SL eigenproblem:  -(P U')' + [l(l+1) W + Q] U = omega^2 U  on (0,R], P=W=e^{2 v0(r)}.
Native-like default: v0(r) = -0.4 e^{-r}  (deep negative core -> 0 exterior, W_inf = e^0 = 1).
We do NOT assume the constructor's M; the eigenvalue is omega^2 directly (M=1 weight here as a clean proxy).

Attacks:
 (a) lowest omega^2(l=1) R-independent across R=8..512 ?
 (b) with Q=0, floor == l(l+1)*W_inf exactly ?
 (c) level spacing above floor -> 0 as R grows ?
 (d) ratios omega_l/omega_1 ~ sqrt(l(l+1)/2) ?
 KEY ATTACK: is R-independence an artifact of (i) Q proxy [Q=0], (ii) W_inf modeled exterior
             [non-asymptoting v0], (iii) BC [Dirichlet vs Neumann]?
"""
import numpy as np

def build_SL(R, N, l, v0func, Qfunc=None, seal='dirichlet', rmin=None):
    """
    Symmetric eigensolve of  L U = -(P U')' + [l(l+1)W + Q] U = lam U  on (rmin, R].
    P = W = exp(2 v0(r)).  Inner BC Dirichlet (regularity node, l>=1). seal at r=R.
    Uses a self-adjoint finite-volume discretization: matrix is symmetric in the standard L2 metric
    because the principal part -(P U')' with P at half-nodes is symmetric.
    """
    if rmin is None:
        rmin = R/ (N*1.0) * 1.0   # small inner offset ~ one cell, avoids r=0 singularity of l(l+1)/... (none here, W bounded)
        rmin = max(rmin, 1e-3)
    r = np.linspace(rmin, R, N)
    h = r[1]-r[0]
    P = np.exp(2*v0func(r))
    W = np.exp(2*v0func(r))
    Q = np.zeros_like(r) if Qfunc is None else Qfunc(r)
    pot = l*(l+1)*W + Q
    # interior nodes 1..N-2 (Dirichlet inner at index 0). Seal at index N-1.
    # Half-node P: P_{i+1/2} = 0.5*(P_i+P_{i+1})
    Phalf = 0.5*(P[:-1]+P[1:])   # length N-1, Phalf[i] between node i and i+1
    # Assemble symmetric tridiagonal for -(P U')' :  row i: [-Phalf[i-1], Phalf[i-1]+Phalf[i], -Phalf[i]]/h^2
    if seal == 'dirichlet':
        idx = np.arange(1, N-1)        # interior, both ends Dirichlet
    elif seal == 'neumann':
        idx = np.arange(1, N)          # include seal node r=R with Neumann (ghost reflection)
    n = len(idx)
    A = np.zeros((n, n))
    for a, i in enumerate(idx):
        # Neumann at seal node i=N-1: no outward flux (Phalf[i] absent) -> only inward flux Phalf[i-1]
        if seal == 'neumann' and i == N-1:
            A[a, a] = Phalf[i-1]/h**2 + pot[i]
            A[a, a-1] = -Phalf[i-1]/h**2
            continue
        diagK = (Phalf[i-1] + Phalf[i])/h**2
        A[a, a] = diagK + pot[i]
        if a-1 >= 0:
            A[a, a-1] = -Phalf[i-1]/h**2
        if a+1 < n:
            A[a, a+1] = -Phalf[i]/h**2
    A = 0.5*(A + A.T)   # enforce symmetry
    ev = np.linalg.eigvalsh(A)
    return np.sort(ev)

# ---- default native-like profile: asymptotes to constant exterior (W_inf = 1) ----
def v0_default(r): return -0.4*np.exp(-r)
def v0_deepcore(r): return -1.0*np.exp(-r)          # variant, deeper core
# ---- non-asymptoting exterior (KEY ATTACK ii): v0 grows logarithmically, W has no flat exterior ----
def v0_nonflat(r): return -0.4*np.exp(-r) + 0.05*np.log(1+r)   # exterior keeps drifting up

print("="*72)
print("CLAIM 3 (a)+(b): floor R-independence and floor == l(l+1) W_inf  (Q=0, Dirichlet)")
print("="*72)
N = 4000
for l in [1,2,3]:
    print(f"\n l={l}:  W_inf = e^(2*v0(inf)) = {np.exp(2*v0_default(1e6)):.4f}, l(l+1)W_inf = {l*(l+1)*np.exp(2*v0_default(1e6)):.4f}")
    print("   R      omega^2_floor   (Q=0)")
    for R in [8, 32, 128, 512]:
        ev = build_SL(R, N, l, v0_default, Qfunc=None, seal='dirichlet')
        print(f"   {R:4d}    {ev[0]:.5f}")

print()
print("="*72)
print("CLAIM 3 (c): level spacing above the floor -> 0 as R grows (l=1, Q=0)")
print("="*72)
print("   R      omega^2_1     omega^2_2     gap")
for R in [16, 32, 64, 128, 256]:
    ev = build_SL(R, N, 1, v0_default, seal='dirichlet')
    print(f"   {R:4d}   {ev[0]:.5f}     {ev[1]:.5f}     {ev[1]-ev[0]:.5f}")

print()
print("="*72)
print("CLAIM 3 (d): angular ratios omega_l/omega_1 ~ sqrt(l(l+1)/2)  (R=256, Q=0)")
print("="*72)
R = 256
floors = {}
for l in [1,2,3,4]:
    ev = build_SL(R, N, l, v0_default, seal='dirichlet')
    floors[l] = np.sqrt(ev[0])
for l in [1,2,3,4]:
    print(f"   l={l}: omega_l/omega_1 = {floors[l]/floors[1]:.4f}   vs sqrt(l(l+1)/2) = {np.sqrt(l*(l+1)/2):.4f}")

print()
print("="*72)
print("KEY ATTACK (ii): NON-ASYMPTOTING exterior v0 (W has no flat exterior) — does R-INDEPENDENCE survive?")
print("="*72)
print("   v0_nonflat = -0.4 e^{-r} + 0.05 ln(1+r)  (exterior keeps drifting; no W_inf)")
print("   l=1:  R      omega^2_floor")
for R in [8, 32, 128, 512]:
    ev = build_SL(R, N, 1, v0_nonflat, seal='dirichlet')
    print(f"          {R:4d}    {ev[0]:.5f}")
print("   => If R-independence DIES here, the constructor's 'intrinsic floor' was a flat-exterior artifact.")
print("   => If floor MOVES but stays R-stable-ish, it is the local potential floor (constructor's claim).")

print()
print("="*72)
print("KEY ATTACK (iii): Dirichlet vs Neumann seal (l=1, Q=0)")
print("="*72)
print("   R      Dirichlet      Neumann")
for R in [32, 128, 512]:
    evd = build_SL(R, N, 1, v0_default, seal='dirichlet')
    evn = build_SL(R, N, 1, v0_default, seal='neumann')
    print(f"   {R:4d}   {evd[0]:.5f}      {evn[0]:.5f}")

print()
print("="*72)
print("KEY ATTACK (i): nonzero bounded Q>=0 proxy vs Q=0 — does floor stay R-independent?")
print("="*72)
def Qproxy(r): return 0.5*np.exp(-r)   # bounded >=0 source proxy
print("   l=1, Q=0.5 e^{-r}:  R      omega^2_floor")
for R in [8, 32, 128, 512]:
    ev = build_SL(R, N, 1, v0_default, Qfunc=Qproxy, seal='dirichlet')
    print(f"                       {R:4d}    {ev[0]:.5f}")

print()
print("="*72)
print("SECOND DISCRETIZATION CHECK: different N (grid-independence of the floor), R=128, l=1, Q=0")
print("="*72)
for N2 in [1000, 2000, 4000, 8000]:
    ev = build_SL(128, N2, 1, v0_default, seal='dirichlet')
    print(f"   N={N2:5d}:  omega^2_floor = {ev[0]:.6f}")
