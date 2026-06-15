"""Part 3: numeric simultaneous match (Maxwell & Proca), parity check,
covariant conservation of Maxwell stress vs Bianchi (claim 4 consistency)."""
import sympy as sp

t, r, th, ph, c = sp.symbols('t r theta phi_ang c', real=True)
m = sp.symbols('m', real=True)
x = [t, r, th, ph]

# concrete phi(t,r,theta)=0.3 cos(theta) r  (as in doc), concrete A
phi = sp.Rational(3,10)*sp.cos(th)*r
g = sp.diag(-sp.exp(-2*phi)*c**2, sp.exp(2*phi), r**2, r**2*sp.sin(th)**2)
ginv = g.inv()

# doc config: A_t=cos t /r, A_r= sin t cos th, A_th= sin t * r
At = sp.cos(t)/r
Ar = sp.sin(t)*sp.cos(th)
Ath = sp.sin(t)*r
A=[At,Ar,Ath,sp.Integer(0)]

F=sp.zeros(4,4)
for mu in range(4):
    for nu in range(4):
        F[mu,nu]=sp.diff(A[nu],x[mu])-sp.diff(A[mu],x[nu])
Fup=sp.zeros(4,4)
for a in range(4):
    for b in range(4):
        Fup[a,b]=sum(ginv[a,mu]*ginv[b,nu]*F[mu,nu] for mu in range(4) for nu in range(4))
Fmixed=sp.zeros(4,4)
for mu in range(4):
    for al in range(4):
        Fmixed[mu,al]=sum(ginv[al,be]*F[mu,be] for be in range(4))
F2=sum(F[a,b]*Fup[a,b] for a in range(4) for b in range(4))
Aup=[sum(ginv[a,mu]*A[mu] for mu in range(4)) for a in range(4)]
A2=sum(A[mu]*Aup[mu] for mu in range(4))
def Tmax(mu,nu):
    return sum(Fmixed[mu,al]*F[nu,al] for al in range(4)) - sp.Rational(1,4)*g[mu,nu]*F2
def Tproca(mu,nu,mval):
    return Tmax(mu,nu)+mval**2*(A[mu]*A[nu]-sp.Rational(1,2)*g[mu,nu]*A2)

pt={t:sp.Rational(4,10), r:sp.Rational(14,10), th:sp.Rational(6,10), c:sp.Integer(1)}
print("=== NUMERIC SIMULTANEOUS MATCH (sign-convention: T = +F F -1/4 g F^2) ===")
print("Maxwell T_tr     =", float(Tmax(0,1).subs(pt)))
print("Maxwell T_ttheta =", float(Tmax(0,2).subs(pt)))
print("Proca(m=0.5) T_tr     =", float(Tproca(0,1,sp.Rational(1,2)).subs(pt)))
print("Proca(m=0.5) T_ttheta =", float(Tproca(0,2,sp.Rational(1,2)).subs(pt)))

print("\n=== PARITY under sigma: t -> -t ===")
# T_ti should be sigma-ODD. Build symbolic T_tr with general A and apply t->-t
At2=sp.Function('A_t')(t,r,th); Ar2=sp.Function('A_r')(t,r,th); Ath2=sp.Function('A_th')(t,r,th)
Ag=[At2,Ar2,Ath2,sp.Integer(0)]
phig=sp.Function('phi')(r,th)  # phi even in t (static-ish); doesn't affect parity argument
gg=sp.diag(-sp.exp(-2*phig)*c**2,sp.exp(2*phig),r**2,r**2*sp.sin(th)**2)
gginv=gg.inv()
Fg=sp.zeros(4,4)
for mu in range(4):
    for nu in range(4):
        Fg[mu,nu]=sp.diff(Ag[nu],x[mu])-sp.diff(Ag[mu],x[nu])
Fgmix=sp.zeros(4,4)
for mu in range(4):
    for al in range(4):
        Fgmix[mu,al]=sum(gginv[al,be]*Fg[mu,be] for be in range(4))
Fgup=sp.zeros(4,4)
for a in range(4):
    for b in range(4):
        Fgup[a,b]=sum(gginv[a,mu]*gginv[b,nu]*Fg[mu,nu] for mu in range(4) for nu in range(4))
F2g=sum(Fg[a,b]*Fgup[a,b] for a in range(4) for b in range(4))
Ttr_g=sp.simplify(sum(Fgmix[0,al]*Fg[1,al] for al in range(4))-sp.Rational(1,4)*gg[0,1]*F2g)
# parity op: t->-t, A_t even, A_r/A_th odd  => A_t(-t)=A_t, A_r(-t)=-A_r ... implement by sign flips on functions & d_t flips
# Easiest: substitute t->-t in expression treating A_t even, A_r,A_th odd.
# We'll do operational: replace each function by its parity image and t-derivs pick up signs automatically via chain.
# Construct sigma-imaged potentials as functions of (-t):
ta=sp.Symbol('ta')
At_s=sp.Function('A_t')(-t,r,th)        # even: A_t(-t)= +A_t(-t,..) (value), but we declare even so equal pattern
# Simpler conceptual check: under t->-t with A_t even, A_r,A_th odd,
# F_{tr}=d_t A_r - d_r A_t -> (-)(-A_r)'... do it termwise on the explicit concrete config below.
print("(checking on concrete config: parity of T_tr, T_ttheta under t->-t with A_t even, A_r,A_th odd)")
# concrete with declared parity: A_t=cos t /r (even in t: cos(-t)=cos t OK),
# A_r= sin t cos th (odd: sin(-t)=-sin t OK), A_th= sin t r (odd OK). phi=0.3cos(th) r (even).
Ttr_c=Tmax(0,1); Ttth_c=Tmax(0,2)
Ttr_sig=Ttr_c.subs(t,-t); Ttth_sig=Ttth_c.subs(t,-t)
print("T_tr(sigma)/T_tr     :", sp.simplify(Ttr_sig+Ttr_c)==0, "(True => ODD)")
print("T_ttheta(sigma)/T_tth:", sp.simplify(Ttth_sig+Ttth_c)==0, "(True => ODD)")

print("\n=== CONSERVATION: nabla_mu T^{mu}_{ t} for Maxwell on diagonal bg ===")
# Use general A, general static phi(r,th); compute covariant divergence of Maxwell stress.
# Christoffels
gG=gg; gGinv=gginv
def christ(a,b,cc):
    return sp.Rational(1,2)*sum(gGinv[a,d]*(sp.diff(gG[d,b],x[cc])+sp.diff(gG[d,cc],x[b])-sp.diff(gG[b,cc],x[d])) for d in range(4))
Gam=[[[sp.simplify(christ(a,b,cc)) for cc in range(4)] for b in range(4)] for a in range(4)]
# Maxwell T^{mu}_{nu}
F2gg=F2g
def Tud(mu,nu):
    Tmn=sum(Fgmix[mu,al]*Fg[nu,al] for al in range(4))-sp.Rational(1,4)*gg[mu,nu]*F2gg
    return Tmn
# raise first index: T^{mu}_{nu}=g^{mu a} T_{a nu}
def Tmixed(mu,nu):
    return sum(gginv[mu,a]*Tud(a,nu) for a in range(4))
# nabla_mu T^{mu}_{nu} = d_mu T^{mu}_nu + Gam^mu_{mu a} T^{a}_nu - Gam^a_{mu nu} T^{mu}_a
nu=0
div=0
Tm=[[sp.simplify(Tmixed(mu,n)) for n in range(4)] for mu in range(4)]
for mu in range(4):
    div+=sp.diff(Tm[mu][nu],x[mu])
    for a in range(4):
        div+=Gam[mu][mu][a]*Tm[a][nu]
        div-=Gam[a][mu][nu]*Tm[mu][a]
div=sp.simplify(div)
# On-shell: Maxwell eq d_mu(sqrt-g F^{mu nu})=0 with no current => div should vanish.
# Off-shell (no field eq imposed) div = -F_{nu a} J^a where J^a = (1/sqrt-g) d_mu(sqrt-g F^{mu a}).
# Compute J and check div + F_{nu a} J^a == 0 (the identity nabla_mu T^{mu}_nu = -F_{nu a} J^a).
sg=sp.sqrt(-gg.det())
J=[sp.simplify((1/sg)*sum(sp.diff(sg*Fgup[mu,a],x[mu]) for mu in range(4))) for a in range(4)]
identity=sp.simplify(div + sum(Fg[nu,a]*J[a] for a in range(4)))
print("nabla_mu T^mu_t + F_{t a} J^a == 0  (conservation identity):", identity==0)
print("  (=> on-shell J=0 forces nabla_mu T^mu_t = 0; stress is a conserved source)")
