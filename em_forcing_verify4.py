"""Part 4: careful conservation identity nabla_mu T^{mu}_nu = -F_{nu a} J^a,
with the correct J^a = nabla_mu F^{mu a} = (1/sqrt-g) d_mu(sqrt-g F^{mu a}).
Test on a flat metric first (sanity), then UDT background.
Also test the SCALAR competitor's conservation."""
import sympy as sp

t,r,th,ph,c=sp.symbols('t r theta phi_ang c',real=True)
x=[t,r,th,ph]

def run(gg, label):
    gginv=gg.inv()
    sg=sp.sqrt(-gg.det())
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
    Fmix=sp.zeros(4,4)  # F_mu^{ al} = g^{al be} F_{mu be}
    for mu in range(4):
        for al in range(4):
            Fmix[mu,al]=sum(gginv[al,be]*F[mu,be] for be in range(4))
    F2=sum(F[a,b]*Fup[a,b] for a in range(4) for b in range(4))
    # christoffel
    def christ(a,b,cc):
        return sp.Rational(1,2)*sum(gginv[a,d]*(sp.diff(gg[d,b],x[cc])+sp.diff(gg[d,cc],x[b])-sp.diff(gg[b,cc],x[d])) for d in range(4))
    Gam=[[[christ(a,b,cc) for cc in range(4)] for b in range(4)] for a in range(4)]
    # T^mu_nu = F^{mu al} F_{nu al} - 1/4 delta^mu_nu F2
    def Tmix(mu,nu):
        s=sum(Fup[mu,al]*F[nu,al] for al in range(4))
        return s - sp.Rational(1,4)*(1 if mu==nu else 0)*F2
    Tm=[[sp.simplify(Tmix(mu,n)) for n in range(4)] for mu in range(4)]
    nu=0
    div=0
    for mu in range(4):
        div+=sp.diff(Tm[mu][nu],x[mu])
        for a in range(4):
            div+=Gam[mu][mu][a]*Tm[a][nu]
            div-=Gam[a][mu][nu]*Tm[mu][a]
    div=sp.simplify(div)
    # current J^a = (1/sqrt-g) d_mu(sqrt-g F^{mu a})  (= nabla_mu F^{mu a})
    J=[sp.simplify((1/sg)*sum(sp.diff(sg*Fup[mu,a],x[mu]) for mu in range(4))) for a in range(4)]
    # identity: nabla_mu T^mu_nu = F_{nu a} J^a  (sign depends on conventions); test both
    rhs1=sp.simplify(sum(F[nu,a]*J[a] for a in range(4)))
    print(f"[{label}] div - F_{{t a}}J^a =", sp.simplify(div-rhs1))
    print(f"[{label}] div + F_{{t a}}J^a =", sp.simplify(div+rhs1))

print("=== FLAT (sanity) ===")
run(sp.diag(-1,1,1,1),"flat-cart")

print("\n=== UDT bg, static phi(r,theta) ===")
phi=sp.Function('phi')(r,th)
run(sp.diag(-sp.exp(-2*phi)*c**2, sp.exp(2*phi), r**2, r**2*sp.sin(th)**2),"UDT")
