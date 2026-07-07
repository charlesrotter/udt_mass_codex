import sympy as sp

# ============================================================
# PART 1 — SYMBOLIC: native equations, Ricci scalar, homogeneity tests
# ============================================================
r, Z, k, L = sp.symbols('r Z k L', positive=True)
phi = sp.Function('phi')
rho = sp.Function('rho')

# Native geometry equation (Eq A) from cell_solver_universe_T3.py line 79:
#   phi'' = 4 e^{-2phi} rho'^2/(Z rho^2) - 2 phi' rho'/rho
# Claim Eq-A' :  (rho^2 phi')' = (4/Z) e^{-2phi} rho'^2
phi_r  = phi(r); rho_r = rho(r)
EqA   = sp.diff(phi_r,r,2) - (4*sp.exp(-2*phi_r)*sp.diff(rho_r,r)**2/(Z*rho_r**2) - 2*sp.diff(phi_r,r)*sp.diff(rho_r,r)/rho_r)
EqAp  = sp.diff(rho_r**2*sp.diff(phi_r,r),r) - (sp.Rational(4)/Z)*sp.exp(-2*phi_r)*sp.diff(rho_r,r)**2
# EqAp should equal rho^2 * EqA
print("Eq-A' == rho^2 * EqA ?  ", sp.simplify(EqAp - rho_r**2*EqA)==0)

# ---- Ricci scalar of ds^2 = -e^{-2phi} dt^2 + e^{2phi} dr^2 + rho^2 dOmega^2 ----
t,th,ps = sp.symbols('t theta psi')
coords=[t,r,th,ps]
A = sp.exp(-2*phi_r); B = sp.exp(2*phi_r); RR = rho_r**2
g = sp.diag(-A, B, RR, RR*sp.sin(th)**2)
gi = g.inv()
def christ(g,gi,coords):
    n=len(coords); Ga=[[[0]*n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                s=0
                for d in range(n):
                    s+=gi[a,d]*(sp.diff(g[d,b],coords[c])+sp.diff(g[d,c],coords[b])-sp.diff(g[b,c],coords[d]))
                Ga[a][b][c]=sp.simplify(s/2)
    return Ga
Ga=christ(g,gi,coords)
n=4
# Ricci tensor
Ric=sp.zeros(n)
for a in range(n):
    for b in range(n):
        s=0
        for c in range(n):
            s+=sp.diff(Ga[c][a][b],coords[c])-sp.diff(Ga[c][a][c],coords[b])
            for d in range(n):
                s+=Ga[c][c][d]*Ga[d][a][b]-Ga[c][b][d]*Ga[d][a][c]
        Ric[a,b]=sp.simplify(s)
Rscalar=sp.simplify(sum(gi[a,b]*Ric[a,b] for a in range(n) for b in range(n)))
print("\nRicci scalar R(phi,rho) =")
sp.pprint(sp.simplify(Rscalar))

# store R as a lambda in phi,phi',phi'',rho,rho',rho''
p,pp,ppp,rh,rhp,rhpp = sp.symbols("p pp ppp rh rhp rhpp")
Rsub=Rscalar.subs({sp.diff(phi_r,r,2):pp, sp.diff(phi_r,r):p, phi_r:p*0+sp.Symbol('P'),
                   sp.diff(rho_r,r,2):rhpp, sp.diff(rho_r,r):rhp, rho_r:rh})
# (leave symbolic; we'll just numerically evaluate R via lambdify of the full expr)

# ---- de Sitter test: areal gauge rho=r, phi=-1/2 ln(1-k r^2) ----
phidS = -sp.Rational(1,2)*sp.log(1-k*r**2)
subs_dS = {phi_r: phidS, sp.diff(phi_r,r): sp.diff(phidS,r), sp.diff(phi_r,r,2): sp.diff(phidS,r,2),
           rho_r: r, sp.diff(rho_r,r): 1, sp.diff(rho_r,r,2):0}
EqAp_dS = sp.simplify(EqAp.subs(subs_dS))
print("\n[de Sitter areal rho=r, phi=-1/2 ln(1-k r^2)]  Eq-A' residual =", EqAp_dS, " (0 => solves; nonzero => FAILS)")
R_dS = sp.simplify(Rscalar.subs(subs_dS))
print("   Ricci scalar R(de Sitter) =", R_dS, " (const => maximally symmetric metric)")

# ---- Minkowski: phi=0, rho=r ----
subs_M={phi_r:0,sp.diff(phi_r,r):0,sp.diff(phi_r,r,2):0,rho_r:r,sp.diff(rho_r,r):1,sp.diff(rho_r,r,2):0}
print("[Minkowski phi=0,rho=r] Eq-A' residual =", sp.simplify(EqAp.subs(subs_M)), " (should be 0 for a solution)")

# ---- general structural fact: RHS of Eq-A' is (4/Z) e^{-2phi} rho'^2 >= 0 ----
print("\nStructural: (rho^2 phi')' = (4/Z) e^{-2phi} rho'^2 >= 0, =0 only where rho'=0.")
print("=> rho^2 phi' is monotone NONDECREASING; phi CANNOT be constant unless rho'=0 (cylinder).")
