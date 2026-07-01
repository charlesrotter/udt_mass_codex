"""Part 5: debug the conservation identity. The identity
nabla_mu T^mu_nu = F_{nu a} J^a  (J^a = nabla_mu F^{mu a})
MUST hold on ANY metric as an algebraic identity (no field eq needed).
Test on a NON-trivial diagonal metric with NO angular sin(theta) subtleties
to isolate whether my divergence code is correct, then add UDT.
Use NUMERIC substitution to avoid simplify timeouts/branches."""
import sympy as sp

t,r,th,ph,c=sp.symbols('t r theta phi_ang c',real=True)
x=[t,r,th,ph]

def residual(gg):
    gginv=gg.inv()
    At=sp.Function('A_t')(t,r,th); Ar=sp.Function('A_r')(t,r,th); Ath=sp.Function('A_th')(t,r,th)
    A=[At,Ar,Ath,sp.Integer(0)]
    F=sp.zeros(4,4)
    for mu in range(4):
        for nu in range(4):
            F[mu,nu]=sp.diff(A[nu],x[mu])-sp.diff(A[mu],x[nu])
    Fup=sp.zeros(4,4)
    for a in range(4):
        for b in range(4):
            Fup[a,b]=sum(gginv[a,mu]*gginv[b,nu]*F[mu,nu] for mu in range(4) for nu in range(4))
    F2=sum(F[a,b]*Fup[a,b] for a in range(4) for b in range(4))
    def christ(a,b,cc):
        return sp.Rational(1,2)*sum(gginv[a,d]*(sp.diff(gg[d,b],x[cc])+sp.diff(gg[d,cc],x[b])-sp.diff(gg[b,cc],x[d])) for d in range(4))
    Gam=[[[christ(a,b,cc) for cc in range(4)] for b in range(4)] for a in range(4)]
    def Tmix(mu,nu):  # T^mu_nu
        return sum(Fup[mu,al]*F[nu,al] for al in range(4)) - sp.Rational(1,4)*(1 if mu==nu else 0)*F2
    Tm=[[Tmix(mu,n) for n in range(4)] for mu in range(4)]
    nu=0
    div=0
    for mu in range(4):
        div+=sp.diff(Tm[mu][nu],x[mu])
        for a in range(4):
            div+=Gam[mu][mu][a]*Tm[a][nu]
            div-=Gam[a][mu][nu]*Tm[mu][a]
    sg=sp.sqrt(-gg.det())
    J=[(1/sg)*sum(sp.diff(sg*Fup[mu,a],x[mu]) for mu in range(4)) for a in range(4)]
    rhs=sum(F[nu,a]*J[a] for a in range(4))
    return div-rhs

# substitute random numeric values for the A-functions and their derivs to test identity numerically
import random
def numtest(gg,label):
    res=residual(gg)
    # build numeric substitution: replace each derivative/function appearing with random numbers
    funcs=res.atoms(sp.Function, sp.Derivative)
    subs={}
    random.seed(1)
    for fn in funcs:
        if fn.has(sp.Function('A_t')) or fn.has(sp.Function('A_r')) or fn.has(sp.Function('A_th')):
            subs[fn]=sp.Rational(random.randint(-9,9), random.randint(1,7))
    pt={t:sp.Rational(3,7),r:sp.Rational(11,9),th:sp.Rational(5,9),c:sp.Integer(1)}
    val=res.subs(subs).subs(pt)
    try:
        val=complex(val)
    except Exception:
        val=sp.N(res.subs(subs).subs(pt))
    print(f"[{label}] residual (should be 0):", val)

print("flat:")
numtest(sp.diag(-1,1,1,1),"flat")
print("flat spherical:")
numtest(sp.diag(-1,1,r**2,r**2*sp.sin(th)**2),"flat-sph")
print("UDT static phi(r,theta):")
phi=sp.Rational(3,10)*sp.cos(th)*r
numtest(sp.diag(-sp.exp(-2*phi)*c**2,sp.exp(2*phi),r**2,r**2*sp.sin(th)**2),"UDT")
