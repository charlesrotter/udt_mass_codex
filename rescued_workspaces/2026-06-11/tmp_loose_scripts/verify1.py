import sympy as sp
from fractions import Fraction as Fr
from math import comb

N = sp.symbols('N', positive=True)

# (a) LOCK-FLOW: (N-1)/(2N^2) = 1/N^2
print("LOCK-FLOW solve:", sp.solve(sp.Eq((N-1)/(2*N**2), 1/N**2), N))
# LOCK-2F: C(N^2,2) = 4N^2 i.e. N^2(N^2-1)/2 = 4N^2
print("LOCK-2F solve:", sp.solve(sp.Eq(N**2*(N**2-1)/2, 4*N**2), N))
# integer scans
print("flow hits:", [n for n in range(2,2001) if Fr(n-1,2*n*n)==Fr(1,n*n)])
print("2F hits:", [n for n in range(2,2001) if comb(n*n,2)==4*n*n])

# alternative branch from rank-one activation law s=q/N: q=(N-2)/N
q_alt = (N-2)/N
print("ALT M1 lock (q=(N-2)/N == 1/N):", sp.solve(sp.Eq(q_alt, 1/N), N))
print("ALT M2 lock (s=q/N == 1/N^2):", sp.solve(sp.Eq(q_alt/N, 1/N**2), N))
e2_alt = (q_alt/2)/N/2
print("ALT 2F lock (eta/2 == 1/C(N^2,2)):",
      [r for r in sp.solve(sp.Eq(e2_alt, 2/(N**2*(N**2-1))), N) if r.is_real])

# (b) section 15: eta/2 * N == S_C1/R identically in N -> q=1/3
q = sp.symbols('q', positive=True)
e2 = (q/2)/N/2
sc1 = q**2/(4*(1-2*q))
sols = sp.solve(sp.Eq(e2*N, sc1), q)
print("(b) eta/2*N == S_C1/R -> q =", sols, "; N-free:",
      all(sp.simplify(s).free_symbols == set() for s in sols))

# (c) B2 at N=2 and general
print("(c) N=2:", Fr(4-1,12), Fr(4-3,4), Fr(4-1,12)==Fr(4-3,4))
print("(c) poly roots:", sp.solve(sp.Eq((N**2-1)/12, (N**2-3)/N**2), N))
# verify the Lambda^3 fraction formula C(M-1,3)/C(M,3)=(M-3)/M
M = sp.symbols('M', positive=True)
print("(c) C(M-1,3)/C(M,3) == (M-3)/M:",
      sp.simplify(sp.binomial(M-1,3)/sp.binomial(M,3) - (M-3)/M)==0)

# (d) overlap identity
expr = 2*(N*(N-1)/2) + (N*(N+1)/2 - 1) - (N**2-1) - N*(N-1)/2
print("(d) overlap - C(N,2) simplifies to:", sp.simplify(expr))
