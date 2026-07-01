#!/usr/bin/env python3
"""
em_forcing2.py  (OBSERVE; the MATCH + UNIQUENESS/forcing tests)

Builds on em_forcing.py. Two questions:
 (M) MATCH: at a concrete point, can a vector field A_mu config produce
     NONZERO T_tr, T_ttheta (so it CAN supply the forced sigma-ODD source)?
     And does the structure (which components feed it) match G's structure?
 (U) UNIQUENESS/forcing: does the forced G_tr,G_ttheta SELECT a closed 2-form
     F=dA (gauge field) over (a) a generic vector (non-closed), (b) a scalar
     gradient d_mu S? Test via the conservation/Bianchi identity that the
     Einstein time-row obeys, and whether a scalar can supply T_tr,T_ttheta.
"""
import sympy as sp
t, r, th, ph = sp.symbols('t r theta phi_ang', real=True)
c, mA = sp.symbols('c m_A', positive=True)
X=[t,r,th,ph]; n=4
phi=sp.Function('phi')(r,th)
g=sp.diag(-sp.exp(-2*phi)*c**2, sp.exp(2*phi), r**2, r**2*sp.sin(th)**2)
ginv=g.inv()
def d(e,i): return sp.diff(e,X[i])

# ---------- (S) SCALAR competitor: T_mu_nu[S] = d_mu S d_nu S - 1/2 g (dS)^2 ----------
# sigma-ODD scalar S(t,r,theta), S odd under t->-t.
S=sp.Function('S')(t,r,th)
dS=[d(S,i) for i in range(n)]
dS2=sp.simplify(sum(ginv[a,b]*dS[a]*dS[b] for a in range(n) for b in range(n)))
def Tscalar(mu,nu): return sp.simplify(dS[mu]*dS[nu]-sp.Rational(1,2)*g[mu,nu]*dS2)
Str=Tscalar(0,1); Stth=Tscalar(0,2)
print("=== sigma-ODD SCALAR competitor time-row stress ===")
print("T_tr[S]     =", Str)
print("T_ttheta[S] =", Stth)
print("  (scalar T_tr = S_t S_r ; T_ttheta = S_t S_th -- a gradient PRODUCT, nonzero if S_t!=0)")

# ---------- (M) MAXWELL match at a concrete point ----------
At=sp.Function('A_t')(t,r,th); Ar=sp.Function('A_r')(t,r,th); Ath=sp.Function('A_th')(t,r,th)
Alow=[At,Ar,Ath,sp.S(0)]
F=sp.zeros(n)
for mu in range(n):
    for nu in range(n):
        F[mu,nu]=d(Alow[nu],mu)-d(Alow[mu],nu)
def Tmax(mu,nu):
    s=sum(F[mu,a]*ginv[a,b]*F[nu,b] for a in range(n) for b in range(n))
    F2=sum(F[a,b]*ginv[a2,a]*ginv[b2,b]*F[a2,b2] for a in range(n) for b in range(n) for a2 in range(n) for b2 in range(n))
    return sp.simplify(s-sp.Rational(1,4)*g[mu,nu]*F2)
Mtr=Tmax(0,1); Mtth=Tmax(0,2)

# concrete radiative config: A_th = a(t,r) (a TIME-VARYING magnetic-type potential),
# everything else simple. Pick functions; evaluate T_tr, T_ttheta numerically.
import sympy as S2
subs_num={phi:sp.Float(0.3)*sp.cos(th)*r}  # phi handled via lambdify below; use explicit form
# Use explicit phi(r,th)=0.3 cos(th) r so all derivs defined:
phi_expr=sp.Float(0.3)*sp.cos(th)*r
def realize(e):
    return e.subs(phi,phi_expr).doit()
# choose A_t=0, A_r=0, A_th = sin(t)*r  (time-varying, sigma-odd-capable)
ch={At:sp.S(0), Ar:sp.S(0), Ath:sp.sin(t)*r}
# need to substitute the FUNCTIONS with concrete exprs incl their derivatives:
def plug(e):
    e=e.subs(phi,phi_expr)
    # replace derivative atoms of A_th first
    rep={}
    a=sp.sin(t)*r
    for D in e.atoms(sp.Derivative):
        if D.expr==Ath:
            rep[D]=a
            for v,k in D.variable_count:
                rep[D]=sp.diff(a,v,k) if len(D.variable_count)==1 else rep[D]
    # robust: rebuild by substituting function then doit
    return e
# Simpler: define A_th as actual expr from the start for the numeric check
Ath_e=sp.sin(t)*r; At_e=sp.S(0); Ar_e=sp.S(0)
Alow_e=[At_e,Ar_e,Ath_e,sp.S(0)]
g_e=sp.diag(-sp.exp(-2*phi_expr)*c**2, sp.exp(2*phi_expr), r**2, r**2*sp.sin(th)**2)
ginv_e=g_e.inv()
F_e=sp.zeros(n)
for mu in range(n):
    for nu in range(n):
        F_e[mu,nu]=d(Alow_e[nu],mu)-d(Alow_e[mu],nu)
def Tmax_e(mu,nu):
    s=sum(F_e[mu,a]*ginv_e[a,b]*F_e[nu,b] for a in range(n) for b in range(n))
    F2=sum(F_e[a,b]*ginv_e[a2,a]*ginv_e[b2,b]*F_e[a2,b2] for a in range(n) for b in range(n) for a2 in range(n) for b2 in range(n))
    return sp.simplify(s-sp.Rational(1,4)*g_e[mu,nu]*F2)
pt={t:0.4,r:1.4,th:0.6,c:1.0}
print("\n=== MAXWELL T_tr,T_ttheta at a concrete radiative config (A_th=sin(t)*r) ===")
print("T_tr     =", float(Tmax_e(0,1).subs(pt)))
print("T_ttheta =", float(Tmax_e(0,2).subs(pt)))
print("  (nonzero => a time-varying magnetic-type vector CAN supply the forced sigma-odd source)")

# ---------- (U) Conservation/selection: nabla_mu T^{mu nu}=0 for Maxwell <=> Maxwell eqn ----------
# A gauge field's stress is conserved BY the field equation D_mu F^{mu nu}=J^nu (J=0 source-free).
# The Bianchi identity dF=0 is AUTOMATIC for F=dA. Test: does T_tr require F closed?
print("\n=== Bianchi: is F closed (dF=0) automatically for F=dA? ===")
# dF_{mu nu rho} cyclic
def dF(a,b,cc): return d(F[b,cc],a)-d(F[a,cc],b)+d(F[a,b],cc)
allzero=all(sp.simplify(dF(a,b,cc))==0 for a in range(n) for b in range(n) for cc in range(n))
print("dF=0 identically (F=dA):", allzero, " -> the gauge field's F is a CLOSED 2-form by construction")
print("\nDONE_EM2")
