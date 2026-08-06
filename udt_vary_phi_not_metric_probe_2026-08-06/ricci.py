import sympy as sp
r,th,cc = sp.symbols('r theta c', positive=True)
x=[sp.symbols('t'),r,th,sp.symbols('ph')]

def ricci_scalar(A,B):
    g=sp.diag(-A*cc**2,B,r**2,r**2*sp.sin(th)**2)
    gi=g.inv()
    n=4
    Gam=[[[sum(gi[l,m]*(sp.diff(g[m,i],x[j])+sp.diff(g[m,j],x[i])-sp.diff(g[i,j],x[m]))
        for m in range(n))/2 for j in range(n)] for i in range(n)] for l in range(n)]
    def Ric(i,j):
        return sp.simplify(sum(sp.diff(Gam[l][i][j],x[l]) for l in range(n))
            -sum(sp.diff(Gam[l][i][l],x[j]) for l in range(n))
            +sum(Gam[l][l][m]*Gam[m][i][j] for l in range(n) for m in range(n))
            -sum(Gam[l][j][m]*Gam[m][i][l] for l in range(n) for m in range(n)))
    Rs=sum(gi[i,i]*Ric(i,i) for i in range(n))  # diagonal metric
    return sp.simplify(Rs),g

def single_field_EL(Afun,Bfun,u):
    # u = u(r) the ONE field; Afun,Bfun functions of u
    A=Afun; B=Bfun
    Rs,g=ricci_scalar(A,B)
    sqrtmg=sp.sqrt(-g.det())               # = c*sqrt(AB)*r^2*|sin|
    L=sp.simplify(Rs*sqrtmg/(cc*sp.Abs(sp.sin(th))))   # drop c,|sin|; keep r^2 sqrt(AB)
    up=sp.diff(u,r); upp=sp.diff(up,r)
    # Euler-Lagrange for L(u,u',u'') via substitution to independent symbols
    return Rs,L

# field u(r); un-blind case 4c: A=u^2, B=1
u=sp.Function('u')(r)
Rs_4c,L_4c=single_field_EL(u**2,sp.Integer(1),u)
print("4c A=u^2,B=1: R =",Rs_4c)
print("   L=R*r^2*sqrt(AB) =",sp.simplify(L_4c))

def EL_of_L(L,u,r):
    # exact Euler-Lagrange up to 2nd deriv: replace u,u',u'' by symbols
    U,U1,U2,U3,U4=sp.symbols('U U1 U2 U3 U4')
    up=sp.diff(u,r); upp=sp.diff(up,r)
    Ls=L.subs({upp:U2,up:U1,u:U}).doit()
    dLdu=sp.diff(Ls,U); dLdu1=sp.diff(Ls,U1); dLdu2=sp.diff(Ls,U2)
    def tot(expr):
        e=expr.subs({U:u,U1:up,U2:upp})
        return sp.diff(e,r)
    E=dLdu.subs({U:u,U1:up,U2:upp}) - tot(dLdu1) + sp.diff(dLdu2.subs({U:u,U1:up,U2:upp}),r,2)
    return sp.simplify(E)

print("EL[4c] =",EL_of_L(L_4c,u,r))

# 4d A=1,B=1/u^2
Rs_4d,L_4d=single_field_EL(sp.Integer(1),1/u**2,u)
print("4d A=1,B=1/u^2: L =",sp.simplify(L_4d))
print("EL[4d] =",EL_of_L(sp.simplify(L_4d),u,r))

# generic non-blind NON-reciprocal control: A=u^2, B=u  (AB=u^3 function, A/B=u so c_eff^2=c^2 u)
Rs_g,L_g=single_field_EL(u**2,u,u)
print("ctrl A=u^2,B=u: L =",sp.simplify(L_g))
print("EL[ctrl] =",EL_of_L(sp.simplify(L_g),u,r))

print("\n--- interpret EL zeros ---")
uu=sp.symbols('u_', positive=True)
print("EL[4d] as fn(u) = 2(u^2-1)/u^2 -> =0 iff u=1 (flat, c_eff=c). NONVACUOUS-ALGEBRAIC.")
print("EL[ctrl]= 3(u-1)/sqrt(u) -> =0 iff u=1. NONVACUOUS-ALGEBRAIC.")

# PROFILE admission: u = 1 - r/X  (c_eff=c_E(1-r/X))
X=sp.symbols('X',positive=True)
prof=1-r/X
for tag,EL in [("4c",EL_of_L(L_4c,u,r)),("4d",EL_of_L(sp.simplify(L_4d),u,r))]:
    val=sp.simplify(EL.subs(u,prof).doit()) if EL!=0 else sp.Integer(0)
    # substitute function u(r)->prof
    val=sp.simplify(EL.subs({sp.Derivative(u,(r,2)):sp.diff(prof,r,2),
                             sp.Derivative(u,r):sp.diff(prof,r),u:prof}))
    print(f"EL[{tag}] on profile u=1-r/X : {val}  -> admits? {val==0}")

# effective source: Einstein tensor G^t_t for un-blind 4c metric on profile
def Gtt(A,B):
    Rs,g=ricci_scalar(A,B); gi=g.inv(); n=4
    Gam=[[[sum(gi[l,m]*(sp.diff(g[m,i],x[j])+sp.diff(g[m,j],x[i])-sp.diff(g[i,j],x[m]))
        for m in range(n))/2 for j in range(n)] for i in range(n)] for l in range(n)]
    def Ric(i,j):
        return sum(sp.diff(Gam[l][i][j],x[l]) for l in range(n))-sum(sp.diff(Gam[l][i][l],x[j]) for l in range(n))\
            +sum(Gam[l][l][m]*Gam[m][i][j] for l in range(n) for m in range(n))\
            -sum(Gam[l][j][m]*Gam[m][i][l] for l in range(n) for m in range(n))
    Rt=Ric(0,0); Gdown=Rt-sp.Rational(1,2)*g[0,0]*Rs
    return sp.simplify(gi[0,0]*Gdown)   # G^t_t
G4c=Gtt(u**2,sp.Integer(1))
print("\n4c G^t_t[u] =",sp.simplify(G4c))
print("4c G^t_t on profile =",sp.simplify(G4c.subs({sp.Derivative(u,(r,2)):sp.diff(prof,r,2),
    sp.Derivative(u,r):sp.diff(prof,r),u:prof})))

G4d=Gtt(sp.Integer(1),1/u**2)
print("4d G^t_t[u] =",sp.simplify(G4d))
print("4d G^t_t on profile u=1-r/X =",sp.simplify(G4d.subs({sp.Derivative(u,(r,2)):sp.diff(prof,r,2),
    sp.Derivative(u,r):sp.diff(prof,r),u:prof})))
