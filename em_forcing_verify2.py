"""Part 2: electric-only zero, Proca extra, scalar competitor, parity,
static Coulomb, dF=0, conservation."""
import sympy as sp

t, r, th, ph, c = sp.symbols('t r theta phi_ang c', real=True)
phi = sp.Function('phi')(t, r, th)
m = sp.symbols('m', real=True)
x = [t, r, th, ph]

g = sp.diag(-sp.exp(-2*phi)*c**2, sp.exp(2*phi), r**2, r**2*sp.sin(th)**2)
ginv = g.inv()
detg = g.det()
sqrtmg = sp.sqrt(-detg)

At = sp.Function('A_t')(t, r, th)
Ar = sp.Function('A_r')(t, r, th)
Ath = sp.Function('A_th')(t, r, th)
A = [At, Ar, Ath, sp.Integer(0)]

F = sp.zeros(4,4)
for mu in range(4):
    for nu in range(4):
        F[mu,nu] = sp.diff(A[nu],x[mu]) - sp.diff(A[mu],x[nu])
Fup = sp.zeros(4,4)
for a in range(4):
    for b in range(4):
        Fup[a,b] = sum(ginv[a,mu]*ginv[b,nu]*F[mu,nu] for mu in range(4) for nu in range(4))
Fmixed = sp.zeros(4,4)
for mu in range(4):
    for al in range(4):
        Fmixed[mu,al] = sum(ginv[al,be]*F[mu,be] for be in range(4))
F2 = sum(F[a,b]*Fup[a,b] for a in range(4) for b in range(4))

# Proca: add mass term to Lagrangian L = -1/4 F^2 - 1/2 m^2 A^2 (A^2 = A_mu A^mu)
Aup = [sum(ginv[a,mu]*A[mu] for mu in range(4)) for a in range(4)]
A2 = sum(A[mu]*Aup[mu] for mu in range(4))

def maxwell_T(mu,nu):
    s = sum(Fmixed[mu,al]*F[nu,al] for al in range(4))
    return sp.simplify(s - sp.Rational(1,4)*g[mu,nu]*F2)

# Proca stress: T_{mn} = Maxwell + m^2 ( A_mu A_nu - 1/2 g_{mn} A^2 )
def proca_extra(mu,nu):
    return sp.simplify(m**2*(A[mu]*A[nu] - sp.Rational(1,2)*g[mu,nu]*A2))

print("=== ELECTRIC-ONLY (A_t=f(r,t,th), A_r=A_th=0) time row ===")
subE = {Ar: 0, Ath: 0}
# must substitute the functions AND their derivatives -> easier: rebuild with A_r=A_th=0
Are=sp.Integer(0); Athe=sp.Integer(0)
Ae=[At,Are,Athe,sp.Integer(0)]
Fe=sp.zeros(4,4)
for mu in range(4):
    for nu in range(4):
        Fe[mu,nu]=sp.diff(Ae[nu],x[mu])-sp.diff(Ae[mu],x[nu])
Fupe=sp.zeros(4,4)
for a in range(4):
    for b in range(4):
        Fupe[a,b]=sum(ginv[a,mu]*ginv[b,nu]*Fe[mu,nu] for mu in range(4) for nu in range(4))
Fmixe=sp.zeros(4,4)
for mu in range(4):
    for al in range(4):
        Fmixe[mu,al]=sum(ginv[al,be]*Fe[mu,be] for be in range(4))
F2e=sum(Fe[a,b]*Fupe[a,b] for a in range(4) for b in range(4))
def TE(mu,nu):
    s=sum(Fmixe[mu,al]*Fe[nu,al] for al in range(4))
    return sp.simplify(s-sp.Rational(1,4)*g[mu,nu]*F2e)
print("T_tr (electric only)     =", TE(0,1))
print("T_ttheta (electric only) =", TE(0,2))

print("\n=== PROCA EXTRA pieces (mass term) ===")
print("dT_tr     =", proca_extra(0,1))
print("dT_ttheta =", proca_extra(0,2))

print("\n=== SCALAR COMPETITOR: T_{mn}[S] = d_m S d_n S - 1/2 g_mn (dS)^2 ===")
S = sp.Function('S')(t,r,th)
dS=[sp.diff(S,x[i]) for i in range(4)]
dS2=sum(ginv[a,b]*dS[a]*dS[b] for a in range(4) for b in range(4))
def TS(mu,nu):
    return sp.simplify(dS[mu]*dS[nu]-sp.Rational(1,2)*g[mu,nu]*dS2)
print("T_tr[S]     =", TS(0,1))
print("T_ttheta[S] =", TS(0,2))

print("\n=== dF = 0 (Bianchi, F=dA closed) ===")
# (dF)_{abc} = d_a F_{bc} + d_b F_{ca} + d_c F_{ab}
maxabs=0
for a in range(4):
    for b in range(4):
        for cc in range(4):
            val=sp.simplify(sp.diff(F[b,cc],x[a])+sp.diff(F[cc,a],x[b])+sp.diff(F[a,b],x[cc]))
            if val!=0:
                maxabs=val
print("dF identically zero:", maxabs==0)

print("\n=== STATIC SOURCE-FREE MAXWELL: A_t=f(r), A_r=A_th=0 ===")
f=sp.Function('f')(r)
Astat=[f,sp.Integer(0),sp.Integer(0),sp.Integer(0)]
# phi static phi(r)
phis=sp.Function('phi')(r)
gs=sp.diag(-sp.exp(-2*phis)*c**2, sp.exp(2*phis), r**2, r**2*sp.sin(th)**2)
gsinv=gs.inv()
sqrtmgs=sp.sqrt(-gs.det())
Fst=sp.zeros(4,4)
for mu in range(4):
    for nu in range(4):
        Fst[mu,nu]=sp.diff(Astat[nu],x[mu])-sp.diff(Astat[mu],x[nu])
Fupst=sp.zeros(4,4)
for a in range(4):
    for b in range(4):
        Fupst[a,b]=sum(gsinv[a,mu]*gsinv[b,nu]*Fst[mu,nu] for mu in range(4) for nu in range(4))
print("sqrt(-g) F^{rt} =", sp.simplify(sqrtmgs*Fupst[1,0]))
# Maxwell eq: d_mu( sqrt(-g) F^{mu nu} ) = 0 ; nu=t component
eq=sp.simplify(sp.diff(sqrtmgs*Fupst[1,0], r))
eq=sp.simplify(eq/ (sp.Abs(c*sp.sin(th))) )  # strip constant factor
print("Maxwell-t eq (=0):", sp.simplify(eq))
sol=sp.dsolve(sp.Eq(sp.simplify(sp.diff(sqrtmgs*Fupst[1,0],r)),0), f)
print("solution:", sol)
