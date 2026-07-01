"""
relrederiv_checks.py
Symbolic cross-checks for the relativity-only re-derivation of the bare UDT
metric structure. Category-A: derives from R1+R2+R3 only; imports nothing.
Nothing committed is changed. Run on CPU (sympy).
"""
import sympy as sp

print("="*70)
print("PART 1a: functional equation -> exponential clock-rate law")
print("="*70)

# Dilation factor between positions: f(phi) = sqrt(-g_tt/c^2).
# Observer at phi_A sees clock at phi_B run at ratio D(phi_A,phi_B).
# R1 (depends only on differences): D = D(phi_B - phi_A) =: g(delta).
# R2 (composition / transitivity across an intermediate phi_C):
#     g(phi_C-phi_A) * g(phi_B-phi_C) = g(phi_B-phi_A)
#  => g(x)*g(y) = g(x+y)   (Cauchy exponential functional equation)
# Regularity premise: g continuous (or monotone, or measurable) and g>0.
# Unique solution: g(x) = exp(k x). Verify the FE is satisfied and that
# g(0)=1 (identity dilation) is forced.
x, y, k = sp.symbols('x y k', real=True)
g = lambda t: sp.exp(k*t)
lhs = g(x)*g(y)
rhs = g(x+y)
print("Cauchy FE  g(x)g(y)-g(x+y) simplifies to:", sp.simplify(lhs - rhs))
print("g(0) =", g(0), " (identity dilation forced by composition)")

# Pin the convention from phi := -(1/2) ln(-g_tt/c^2).
# -g_tt/c^2 = f(phi)^2 = g(phi)^2 = exp(2 k phi).  Then
# phi := -(1/2) ln(exp(2 k phi)) = -k phi.  Consistency forces k = -1.
phi = sp.symbols('phi', real=True)
neg_gtt_over_c2 = sp.exp(2*k*phi)          # = f(phi)^2
phi_def = -sp.Rational(1,2)*sp.log(neg_gtt_over_c2)
print("phi defined back:", sp.simplify(phi_def), " => set equal to phi forces k:")
sol_k = sp.solve(sp.Eq(phi_def, phi), k)
print("   k =", sol_k, " (CONVENTION, fixes sign of phi; physics is in |k|=1 scaling absorbed into phi)")

print()
print("="*70)
print("PART 1b: reciprocity R3 -> structural identity g_tt g_rr = -c^2")
print("="*70)
# With k=-1: g_tt = -exp(-2 phi) c^2.
# Radial proper length element: dL = sqrt(g_rr) dr.
# A radial "ruler" / coordinate-distance dilation factor is h(phi)=sqrt(g_rr).
# R3 reciprocity (SR/GR analog): the map B-as-seen-by-A and A-as-seen-by-B
# are mutual inverses with neither preferred. The time-dilation factor
# observer A assigns to B equals the inverse of the spatial/length factor
# (reciprocal pairing of the two metric dials), i.e.
#     sqrt(-g_tt/c^2) * sqrt(g_rr) = 1   for all phi  (no preferred position).
# => g_rr = -c^2/g_tt  => g_tt g_rr = -c^2.
phi_s = sp.symbols('phi', real=True)
c = sp.symbols('c', positive=True)
g_tt = -sp.exp(-2*phi_s)*c**2
g_rr = sp.exp(2*phi_s)
print("g_tt =", g_tt)
print("g_rr =", g_rr)
print("g_tt * g_rr =", sp.simplify(g_tt*g_rr), "  (= -c^2  : the structural identity)")
recip = sp.sqrt(-g_tt/c**2)*sp.sqrt(g_rr)
print("reciprocity product sqrt(-g_tt/c^2)*sqrt(g_rr) =", sp.simplify(recip), " (=1, mutual, neither preferred)")

print()
print("="*70)
print("PART 3a: reproduce corpus form & Einstein-identity cross-check")
print("="*70)
# Corpus chain (S58-009) uses GR identity G^t_t - G^r_r = -(AB)'/(r A B^2)
# on SSS ansatz ds^2 = -A c^2 dt^2 + B dr^2 + r^2 dOmega^2.
# Confirm: with A = e^{-2phi(r)}, B = e^{+2phi(r)}, AB = 1 identically,
# so (AB)' = 0 and G^t_t = G^r_r WITHOUT any matter assumption.
r = sp.symbols('r', positive=True)
phif = sp.Function('phi')(r)
A = sp.exp(-2*phif)
B = sp.exp(2*phif)
AB = sp.simplify(A*B)
print("A*B =", AB, " => (AB)' =", sp.diff(A*B, r), " (identically zero: tie is automatic)")

# Build the metric and compute G^t_t - G^r_r explicitly to confirm it
# vanishes for the locked form (no source needed).
t, th, ph = sp.symbols('t theta phi_ang', real=True)
coords = [t, r, th, ph]
gmet = sp.diag(-A*c**2, B, r**2, r**2*sp.sin(th)**2)
ginv = gmet.inv()
def christoffel(g, gi, X):
    n=len(X)
    Gam=[[[0]*n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for cc in range(n):
                s=0
                for d in range(n):
                    s+=gi[a,d]*(sp.diff(g[d,b],X[cc])+sp.diff(g[d,cc],X[b])-sp.diff(g[b,cc],X[d]))
                Gam[a][b][cc]=sp.simplify(s/2)
    return Gam
Gam=christoffel(gmet,ginv,coords)
def ricci(Gam,X):
    n=len(X)
    Ric=sp.zeros(n,n)
    for b in range(n):
        for d in range(n):
            s=0
            for a in range(n):
                s+=sp.diff(Gam[a][b][d],X[a])-sp.diff(Gam[a][b][a],X[d])
                for e in range(n):
                    s+=Gam[a][a][e]*Gam[e][b][d]-Gam[a][d][e]*Gam[e][b][a]
            Ric[b,d]=sp.simplify(s)
    return Ric
Ric=ricci(Gam,coords)
Rs=sp.simplify(sum(ginv[i,j]*Ric[i,j] for i in range(4) for j in range(4)))
# Einstein mixed components
Gmix=sp.zeros(4,4)
for a in range(4):
    for b in range(4):
        val=sum(ginv[a,m]*(Ric[m,b]-sp.Rational(1,2)*gmet[m,b]*Rs) for m in range(4))
        Gmix[a,b]=sp.simplify(val)
diff_tt_rr=sp.simplify(Gmix[0,0]-Gmix[1,1])
print("G^t_t - G^r_r for the locked form =", diff_tt_rr, " (must be 0: source-free tie)")
print("G^theta_theta (the equation that fixes phi) =", sp.simplify(Gmix[2,2]))
