import sympy as sp
t, r, th, ph, eps = sp.symbols('t r theta phi_coord epsilon', real=True)
coords=[t,r,th,ph]
phi0 = sp.Function('phi')(r)
h_tr  = sp.Function('h_tr')(r, th, ph)
h_tth = sp.Function('h_ttheta')(r, th, ph)
h_tph = sp.Function('h_tphi')(r, th, ph)

gbar = sp.diag(-sp.exp(-2*phi0), sp.exp(2*phi0), r**2, r**2*sp.sin(th)**2)
h = sp.zeros(4,4)
h[0,1]=h[1,0]=h_tr; h[0,2]=h[2,0]=h_tth; h[0,3]=h[3,0]=h_tph
g = gbar + eps*h
ginv = g.inv().applyfunc(lambda e: sp.series(e,eps,0,2).removeO())

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
G=christ(g,ginv)
Ric=sp.zeros(4,4)
for b in range(4):
    for c in range(4):
        term=0
        for a in range(4):
            term+=sp.diff(G[a][b][c],coords[a])-sp.diff(G[a][b][a],coords[c])
            for d in range(4):
                term+=G[a][a][d]*G[d][b][c]-G[a][c][d]*G[d][b][a]
        Ric[b,c]=sp.series(sp.expand(term),eps,0,2).removeO()
Rs=0
for a in range(4):
    for b in range(4):
        Rs+=ginv[a,b]*Ric[a,b]
Rs=sp.series(sp.expand(Rs),eps,0,2).removeO()
Glow=sp.zeros(4,4)
for a in range(4):
    for b in range(4):
        Glow[a,b]=sp.series(sp.expand(Ric[a,b]-sp.Rational(1,2)*g[a,b]*Rs),eps,0,2).removeO()

dG_tr = sp.simplify(sp.expand(Glow[0,1]).coeff(eps,1))
print("CLAIM 3: dG_tr contains e^{-2phi} prefactor and phi' decorations?")
print("   has exp(phi)?:", dG_tr.has(sp.exp(-2*phi0)) or dG_tr.has(sp.exp(2*phi0)))
print("   has phi':?", dG_tr.has(sp.Derivative(phi0,r)))

# CLAIM 4: pure radial h_tr mode -> is there a d_r^2 h_tr term? (elliptic) or not (algebraic)?
Htr=sp.Function('Htr')(r)
dG_tr_rad = sp.simplify(dG_tr.subs({h_tth:0,h_tph:0,h_tr:Htr}))
print("\ndG_tr on pure radial h_tr=Htr(r):", dG_tr_rad)
coeff_drr = sp.simplify(dG_tr_rad.coeff(sp.Derivative(Htr,r,r)))
print("coeff of d_r^2 Htr (radial h_tr) =", coeff_drr, " -> ALGEBRAIC if 0")

# Now h_ttheta transverse: d_r^2 present?
Hang=sp.Function('Hang')(r)
dG_tth = sp.simplify(sp.expand(Glow[0,2]).coeff(eps,1))
dG_tth_rad = sp.simplify(dG_tth.subs({h_tr:0,h_tph:0,h_tth:Hang}))
coeff_drr_ang = sp.simplify(dG_tth_rad.coeff(sp.Derivative(Hang,r,r)))
print("coeff of d_r^2 Hang (transverse h_ttheta) =", coeff_drr_ang, " -> ELLIPTIC if nonzero")
