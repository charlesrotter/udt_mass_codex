#!/usr/bin/env python3
"""Independent spot-check: evaluate G_tr, G_ttheta at a concrete metric.
(1) STATIONARY nonzero arm => G_tr,G_ttheta nonzero?  (2) STATIC (arm=0) => 0?
(3) TIME-DEPENDENT arm => extra A_t,B_t contribution present?
Built from scratch (does NOT reuse the symbolic expr) to be a true cross-check.
"""
import sympy as sp
t,r,th,ph,c = sp.symbols('t r theta phi_ang c', positive=True)
X=[t,r,th,ph]
def einstein_trow(phi_f, A_f, B_f):
    e_m=sp.exp(-2*phi_f); e_p=sp.exp(2*phi_f)
    g=sp.Matrix([[-e_m*c**2,A_f,B_f,0],[A_f,e_p,0,0],[B_f,0,r**2,0],[0,0,0,r**2*sp.sin(th)**2]])
    gi=g.inv(); n=4
    d=lambda e,i: sp.diff(e,X[i])
    Gam=[[[sp.S(0)]*n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for ccc in range(n):
                s=sum(gi[a,dd]*(d(g[dd,b],ccc)+d(g[dd,ccc],b)-d(g[b,ccc],dd)) for dd in range(n))
                Gam[a][b][ccc]=sp.cancel(s/2)
    def ric(b,dd):
        s=sum(d(Gam[a][b][dd],a)-d(Gam[a][b][a],dd) for a in range(n))
        for a in range(n):
            for e in range(n):
                s+=Gam[a][a][e]*Gam[e][b][dd]-Gam[a][dd][e]*Gam[e][b][a]
        return sp.cancel(s)
    Ric=sp.zeros(n)
    for b in range(n):
        for dd in range(b,n):
            Ric[b,dd]=ric(b,dd); Ric[dd,b]=Ric[b,dd]
    Rs=sum(gi[a,b]*Ric[a,b] for a in range(n) for b in range(n))
    Gtr =sp.cancel(Ric[0,1]-sp.Rational(1,2)*g[0,1]*Rs)
    Gtth=sp.cancel(Ric[0,2]-sp.Rational(1,2)*g[0,2]*Rs)
    return Gtr,Gtth

# numeric nonzero test: substitute concrete numbers for r,theta,t and any funcs
def nz(expr):
    val=expr.subs({r:sp.Rational(7,5),th:sp.Rational(3,5),t:sp.Rational(2,5),
                   c:1, ph:sp.Rational(1,4)})
    return sp.nsimplify(val)!=0, float(val)

phi_c = sp.Rational(1,3)*sp.cos(th)*(r)   # simple polynomial-ish static phi

print("--- (2) STATIC: arm = 0 ---")
g1,g2=einstein_trow(phi_c, sp.S(0), sp.S(0))
print("G_tr=",sp.simplify(g1),"  G_ttheta=",sp.simplify(g2))

print("\n--- (1) STATIONARY nonzero arm A=A(r,theta),B=B(r,theta) ---")
A_st=sp.Rational(1,5)*r*sp.sin(th); B_st=sp.Rational(1,7)*r**2*sp.cos(th)
g1,g2=einstein_trow(phi_c, A_st, B_st)
print("G_tr nonzero:", nz(g1), "  G_ttheta nonzero:", nz(g2))

print("\n--- (3) TIME-DEPENDENT arm A=sin(t)*..., B=cos(t)*... ---")
A_td=sp.sin(t)*sp.Rational(1,5)*r*sp.sin(th); B_td=sp.cos(t)*sp.Rational(1,7)*r**2*sp.cos(th)
g1,g2=einstein_trow(phi_c, A_td, B_td)
print("G_tr nonzero:", nz(g1), "  G_ttheta nonzero:", nz(g2))
print("G_tr has cos(t) (=A_t signature):", g1.has(sp.cos(t)))
print("DONE_SPOT")
