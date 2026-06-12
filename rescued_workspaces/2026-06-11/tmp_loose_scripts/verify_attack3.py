import sympy as sp
t,r,th,ph,eps = sp.symbols('t r theta phi_coord epsilon', real=True)
phi = sp.Function('phi')(r)
h_tr = sp.Function('h_tr')(r,th,ph)
h_tth = sp.Function('h_ttheta')(r,th,ph)
h_tph = sp.Function('h_tphi')(r,th,ph)
coords=[t,r,th,ph]
gbar = sp.diag(-sp.exp(-2*phi), sp.exp(2*phi), r**2, r**2*sp.sin(th)**2)
h=sp.zeros(4,4)
h[0,1]=h[1,0]=h_tr; h[0,2]=h[2,0]=h_tth; h[0,3]=h[3,0]=h_tph
g=gbar+eps*h
ginv=g.inv().applyfunc(lambda e: sp.series(e,eps,0,2).removeO())
def christ(gm,gi):
    G=[[[0]*4 for _ in range(4)] for _ in range(4)]
    for a in range(4):
        for b in range(4):
            for c in range(4):
                s=0
                for d in range(4):
                    s+=gi[a,d]*(sp.diff(gm[d,b],coords[c])+sp.diff(gm[d,c],coords[b])-sp.diff(gm[b,c],coords[d]))
                G[a][b][c]=sp.series(sp.expand(sp.Rational(1,2)*s),eps,0,2).removeO()
    return G
Gam=christ(g,ginv)
Ric=sp.zeros(4,4)
for b in range(4):
    for c in range(4):
        term=0
        for a in range(4):
            term+=sp.diff(Gam[a][b][c],coords[a])-sp.diff(Gam[a][b][a],coords[c])
            for d in range(4):
                term+=Gam[a][a][d]*Gam[d][b][c]-Gam[a][c][d]*Gam[d][b][a]
        Ric[b,c]=sp.series(sp.expand(term),eps,0,2).removeO()
Rs=0
for a in range(4):
    for b in range(4):
        Rs+=ginv[a,b]*Ric[a,b]
Rs=sp.series(sp.expand(Rs),eps,0,2).removeO()
Gtr=sp.series(sp.expand(Ric[0,1]-sp.Rational(1,2)*g[0,1]*Rs),eps,0,2).removeO()
dGtr=sp.simplify(sp.expand(Gtr).coeff(eps,1))
# radial isolation: h_ttheta=h_tph=0, h_tr=Htr(r)
Htr=sp.Function('Htr')(r)
dGtr_rad=sp.simplify(dGtr.subs({h_tth:0,h_tph:0,h_tr:Htr}))
print("delta_G_tr radial (h_tr=Htr(r) only):", dGtr_rad)
print()
print("coeff of d_r^2 Htr:", sp.simplify(dGtr_rad.coeff(sp.Derivative(Htr,r,r))))
print("coeff of d_r Htr:", sp.simplify(dGtr_rad.coeff(sp.Derivative(Htr,r))))
print("coeff of Htr:", sp.simplify(dGtr_rad.coeff(Htr)))
