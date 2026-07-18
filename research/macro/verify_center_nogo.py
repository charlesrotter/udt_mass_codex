"""
Independent adversarial verification of the CENTER NO-GO claim.
Metric: ds^2 = -A dt^2 + (1/A) dr^2 + r^2 (dth^2 + sin^2 th dph^2), A=A(r).
Compute R (Ricci scalar) and K (Kretschmann) FROM THE METRIC via Christoffels/Riemann,
no imported formulas. Then evaluate on A=1-r/X and the family (1-r/X)^alpha.
Also test A'(0) and hunt for a center-regular re-centering member.
"""
import sympy as sp

t, r, th, ph, X, alpha = sp.symbols('t r theta phi X alpha', real=True, positive=True)
A = sp.Function('A')(r)

coords = [t, r, th, ph]
g = sp.diag(-A, 1/A, r**2, r**2*sp.sin(th)**2)
ginv = g.inv()
n = 4

# Christoffel symbols Gamma^a_bc
def christoffel(g, ginv, coords):
    n = len(coords)
    Gamma = [[[0]*n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                s = 0
                for d in range(n):
                    s += ginv[a,d]*(sp.diff(g[d,b],coords[c]) + sp.diff(g[d,c],coords[b]) - sp.diff(g[b,c],coords[d]))
                Gamma[a][b][c] = sp.simplify(s/2)
    return Gamma

Gamma = christoffel(g, ginv, coords)

# Riemann R^a_bcd = d_c Gamma^a_bd - d_d Gamma^a_bc + Gamma^a_ce Gamma^e_bd - Gamma^a_de Gamma^e_bc
Riem = [[[[0]*n for _ in range(n)] for _ in range(n)] for _ in range(n)]
for a in range(n):
    for b in range(n):
        for c in range(n):
            for d in range(n):
                term = sp.diff(Gamma[a][b][d], coords[c]) - sp.diff(Gamma[a][b][c], coords[d])
                for e in range(n):
                    term += Gamma[a][c][e]*Gamma[e][b][d] - Gamma[a][d][e]*Gamma[e][b][c]
                Riem[a][b][c][d] = sp.simplify(term)

# Ricci R_bd = R^a_bad
Ric = sp.zeros(n)
for b in range(n):
    for d in range(n):
        s = 0
        for a in range(n):
            s += Riem[a][b][a][d]
        Ric[b,d] = sp.simplify(s)

# Ricci scalar R = g^bd R_bd
Rscalar = sp.simplify(sum(ginv[b,d]*Ric[b,d] for b in range(n) for d in range(n)))

# Kretschmann K = R_{abcd} R^{abcd}
# lower first index: R_{abcd} = g_ae R^e_bcd
Riem_low = [[[[0]*n for _ in range(n)] for _ in range(n)] for _ in range(n)]
for a in range(n):
    for b in range(n):
        for c in range(n):
            for d in range(n):
                Riem_low[a][b][c][d] = sp.simplify(sum(g[a,e]*Riem[e][b][c][d] for e in range(n)))

# raise all indices of R_{abcd} to get R^{abcd}
Riem_up = [[[[0]*n for _ in range(n)] for _ in range(n)] for _ in range(n)]
for a in range(n):
    for b in range(n):
        for c in range(n):
            for d in range(n):
                s = 0
                for e in range(n):
                    for f in range(n):
                        for gg in range(n):
                            for h in range(n):
                                s += ginv[a,e]*ginv[b,f]*ginv[c,gg]*ginv[d,h]*Riem_low[e][f][gg][h]
                Riem_up[a][b][c][d] = s

K = 0
for a in range(n):
    for b in range(n):
        for c in range(n):
            for d in range(n):
                K += Riem_low[a][b][c][d]*Riem_up[a][b][c][d]
K = sp.simplify(K)

print("=== General A(r) invariants ===")
print("R  =", Rscalar)
print("K  =", K)

# ---- Evaluate on L: A = 1 - r/X ----
AL = 1 - r/X
subsL = {A: AL, sp.diff(A,r): sp.diff(AL,r), sp.diff(A,r,2): sp.diff(AL,r,2)}
# substitute derivatives: replace Derivative first, then function
def apply_A(expr, Aexpr):
    expr = expr.subs(sp.Derivative(A, r, 2), sp.diff(Aexpr, r, 2))
    expr = expr.subs(sp.Derivative(A, r), sp.diff(Aexpr, r))
    expr = expr.subs(A, Aexpr)
    return sp.simplify(expr)

RL = apply_A(Rscalar, AL)
KL = apply_A(K, AL)
print("\n=== On L (A=1-r/X) ===")
print("R_L =", RL)
print("K_L =", KL)
print("leading R_L as r->0:", sp.series(RL, r, 0, 1))
print("leading K_L as r->0:", sp.series(KL, r, 0, 1))
print("lim r*R_L :", sp.limit(r*RL, r, 0))
print("lim r^2*K_L :", sp.limit(r**2*KL, r, 0))

# ---- family (1-r/X)^alpha ----
Af = (1 - r/X)**alpha
Rf = apply_A(Rscalar, Af)
Kf = apply_A(K, Af)
print("\n=== On family (1-r/X)^alpha ===")
print("lim r*R_f  :", sp.simplify(sp.limit(r*Rf, r, 0)))
print("lim r^2*K_f:", sp.simplify(sp.limit(r**2*Kf, r, 0)))
print("A'(0) family =", sp.diff(Af, r).subs(r,0))
print("A'(0) L      =", sp.diff(AL, r))

# ---- Center regularity: general A=1+a1 r + a2 r^2 ----
a1, a2, a3 = sp.symbols('a1 a2 a3', real=True)
Ag = 1 + a1*r + a2*r**2 + a3*r**3
Rg = apply_A(Rscalar, Ag)
Kg = apply_A(K, Ag)
print("\n=== General Taylor center A=1+a1 r+a2 r^2+... ===")
print("R series:", sp.series(Rg, r, 0, 2))
print("K series:", sp.series(Kg, r, 0, 2))
print("R finite at 0 requires a1=0? R|a1=0:", sp.limit(Rg.subs(a1,0), r, 0))
print("K finite at 0 requires a1=0? K|a1=0:", sp.limit(Kg.subs(a1,0), r, 0))
