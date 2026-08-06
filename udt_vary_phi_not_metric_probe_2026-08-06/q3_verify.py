import sympy as sp
r = sp.symbols('r', positive=True)
X = sp.symbols('X', positive=True)

# ---------- (a) is L a total derivative? ----------
f,f1,f2 = sp.symbols('f f1 f2')
L = 2*(-2*f1**2*r**2 + 4*f1*r + f2*r**2 + sp.exp(2*f) - 1)*sp.exp(-2*f)
# guess F(r,f,f1) with L = dF/dr = F_r + F_f f1 + F_f1 f2. Coeff of f2 in L is 2 r^2 e^{-2f}=F_f1.
Ff1 = 2*r**2*sp.exp(-2*f)
# then remaining L - Ff1*f2 must equal F_r + F_f f1
rem = sp.simplify(L - Ff1*f2)
print("=== L - d/dr-part(f2 term); remaining (must be F_r+F_f f1, no f2) ===")
print(rem)
# F such that F_f1 = 2r^2 e^{-2f}: F = 2 r^2 e^{-2f} f1 + h(r,f). Then dF/dr:
F = 2*r**2*sp.exp(-2*f)*f1
dF = sp.diff(F,r) + sp.diff(F,f)*f1 + sp.diff(F,f1)*f2
print("=== L - dF/dr  (residual to be matched by h(r,f)) ===")
res = sp.simplify(L - dF)
print(res)  # if this is a function of (r,f) with no f1,f2 and integrable => total derivative

# ---------- (c) CONTROL: two independent functions, no reciprocal lock ----------
th = sp.symbols('theta')
a = sp.Function('a'); b = sp.Function('b')
A = a(r); B = b(r)
xs=[sp.Symbol('t'),r,th,sp.Symbol('ph')]
g = sp.diag(-sp.exp(2*A), sp.exp(2*B), r**2, r**2*sp.sin(th)**2)
gi=g.inv()
def christ(g,gi,x):
    n=len(x); G=[[[0]*n for _ in range(n)] for _ in range(n)]
    for al in range(n):
        for be in range(n):
            for ga in range(n):
                s=0
                for de in range(n):
                    s+=gi[al,de]*(sp.diff(g[de,be],x[ga])+sp.diff(g[de,ga],x[be])-sp.diff(g[be,ga],x[de]))
                G[al][be][ga]=s/2
    return G
Ga=christ(g,gi,xs); n=4
Ric=sp.zeros(n,n)
for be in range(n):
    for ga in range(n):
        s=0
        for al in range(n):
            s+=sp.diff(Ga[al][be][ga],xs[al])-sp.diff(Ga[al][be][al],xs[ga])
            for de in range(n):
                s+=Ga[al][al][de]*Ga[de][be][ga]-Ga[al][ga][de]*Ga[de][be][al]
        Ric[be,ga]=s
Rs=sp.simplify(sum(gi[i,j]*Ric[i,j] for i in range(n) for j in range(n)))
sqrtg=r**2*sp.sin(th)
Lag=sp.simplify(Rs*sqrtg)  # full radial density (keep sin th const)
# EL wrt a and b (both up to 2nd deriv). Use placeholder substitution.
A1,A2,B1,B2=sp.symbols('A1 A2 B1 B2')
subs_pl={sp.Derivative(A,(r,2)):A2, sp.Derivative(A,r):A1, A:sp.Symbol('Av'),
         sp.Derivative(B,(r,2)):B2, sp.Derivative(B,r):B1, B:sp.Symbol('Bv')}
Lp=Lag.subs(subs_pl)
Av,Bv=sp.Symbol('Av'),sp.Symbol('Bv')
def EL(L,v0,v1,v2,back):
    d0=sp.diff(L,v0); d1=sp.diff(L,v1); d2=sp.diff(L,v2)
    d0f=d0.subs(back); d1f=d1.subs(back); d2f=d2.subs(back)
    return sp.simplify(d0f - sp.diff(d1f,r) + sp.diff(d2f,r,2))
back={Av:A,A1:sp.Derivative(A,r),A2:sp.Derivative(A,(r,2)),
      Bv:B,B1:sp.Derivative(B,r),B2:sp.Derivative(B,(r,2))}
ELa=EL(Lp,Av,A1,A2,back); ELb=EL(Lp,Bv,B1,B2,back)
print("=== CONTROL EL wrt a (independent) ===")
print(sp.simplify(ELa*sp.exp(2*A)/sp.sin(th)))
print("=== CONTROL EL wrt b (independent) ===")
print(sp.simplify(ELb*sp.exp(2*B)/sp.sin(th)))
print("=== now impose reciprocal lock a=-b: sum of the two ELs projected ===")
# reciprocal lock: A=-phi, B=+phi -> phi-variation = dL/dphi = -ELa+ELb style projection
