import sympy as sp
r=sp.symbols('r',positive=True); th=sp.symbols('theta')
a=sp.Function('a'); b=sp.Function('b'); A=a(r); B=b(r)
# control ELs from q3 (paste the exact expressions), stripped of common factors:
# ELa*e^{2a-2b}... use full ELa, ELb as functions; simplest: recompute compactly.
xs=[sp.Symbol('t'),r,th,sp.Symbol('ph')]
g=sp.diag(-sp.exp(2*A),sp.exp(2*B),r**2,r**2*sp.sin(th)**2); gi=g.inv()
def christ(g,gi,x):
    n=len(x);G=[[[0]*n for _ in range(n)] for _ in range(n)]
    for al in range(n):
        for be in range(n):
            for ga in range(n):
                s=0
                for de in range(n): s+=gi[al,de]*(sp.diff(g[de,be],x[ga])+sp.diff(g[de,ga],x[be])-sp.diff(g[be,ga],x[de]))
                G[al][be][ga]=s/2
    return G
Ga=christ(g,gi,xs);n=4
Ric=sp.zeros(n,n)
for be in range(n):
    for ga in range(n):
        s=0
        for al in range(n):
            s+=sp.diff(Ga[al][be][ga],xs[al])-sp.diff(Ga[al][be][al],xs[ga])
            for de in range(n): s+=Ga[al][al][de]*Ga[de][be][ga]-Ga[al][ga][de]*Ga[de][be][al]
        Ric[be,ga]=s
Rs=sp.simplify(sum(gi[i,j]*Ric[i,j] for i in range(n) for j in range(n)))
Ein=sp.simplify(gi*(Ric-sp.Rational(1,2)*g*Rs))
Gtt=sp.simplify(Ein[0,0]); Grr=sp.simplify(Ein[1,1])
print("=== G^t_t - G^r_r (two independent fns) ===")
diff=sp.simplify(Gtt-Grr)
print(diff)
print("=== under reciprocal lock a=-phi,b=phi ->  a'+b'=0 ===")
phi=sp.Function('phi')
print(sp.simplify(diff.subs({A:-phi(r),B:phi(r)}).doit()))
