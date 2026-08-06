import sympy as sp

r = sp.symbols('r', positive=True)
th = sp.symbols('theta', positive=True)
phi = sp.Function('phi')(r)
# c set to 1 (premise: constant reference c_E; scales g_tt only, irrelevant to vacuum structure)
# metric: ds^2 = -e^{-2phi} dt^2 + e^{2phi} dr^2 + r^2 dOmega^2
x = [sp.Symbol('t'), r, th, sp.Symbol('ph')]
g = sp.diag(-sp.exp(-2*phi), sp.exp(2*phi), r**2, r**2*sp.sin(th)**2)
gi = g.inv()

def christ(g, gi, x):
    n = len(x)
    G = [[[0]*n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                s = 0
                for d in range(n):
                    s += gi[a,d]*(sp.diff(g[d,b],x[c])+sp.diff(g[d,c],x[b])-sp.diff(g[b,c],x[d]))
                G[a][b][c] = sp.simplify(s/2)
    return G

Gamma = christ(g, gi, x)
n = 4
# Ricci
Ric = sp.zeros(n,n)
for b in range(n):
    for c in range(n):
        s = 0
        for a in range(n):
            s += sp.diff(Gamma[a][b][c], x[a]) - sp.diff(Gamma[a][b][a], x[c])
            for d in range(n):
                s += Gamma[a][a][d]*Gamma[d][b][c] - Gamma[a][c][d]*Gamma[d][b][a]
        Ric[b,c] = sp.simplify(s)

Rs = sp.simplify(sum(gi[a,b]*Ric[a,b] for a in range(n) for b in range(n)))
Ein = sp.zeros(n,n)
for a in range(n):
    for b in range(n):
        Ein[a,b] = sp.simplify(Ric[a,b] - sp.Rational(1,2)*g[a,b]*Rs)

# mixed G^mu_nu (cleaner)
Gmix = sp.simplify(gi*Ein)
print("=== R scalar ===")
print(sp.simplify(Rs))
print("=== G^t_t ===")
print(sp.simplify(Gmix[0,0]))
print("=== G^r_r ===")
print(sp.simplify(Gmix[1,1]))
print("=== G^th_th ===")
print(sp.simplify(Gmix[2,2]))
print("=== G^ph_ph ===")
print(sp.simplify(Gmix[3,3]))
