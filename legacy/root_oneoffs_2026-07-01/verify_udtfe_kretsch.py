import sympy as sp

t, r, th, ph = sp.symbols('t r theta phi_a', real=True)
c0 = sp.symbols('c0', positive=True)

def kretschmann(g, coords):
    n=len(coords); ginv=g.inv()
    Gamma=[[[0]*n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for cc in range(n):
                s=0
                for d in range(n):
                    s+=ginv[a,d]*(sp.diff(g[d,b],coords[cc])+sp.diff(g[d,cc],coords[b])-sp.diff(g[b,cc],coords[d]))
                Gamma[a][b][cc]=sp.simplify(s/2)
    # Riemann R^a_{bcd}
    R=[[[[0]*n for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for cc in range(n):
                for d in range(n):
                    term=sp.diff(Gamma[a][b][d],coords[cc])-sp.diff(Gamma[a][b][cc],coords[d])
                    for e in range(n):
                        term+=Gamma[a][cc][e]*Gamma[e][b][d]-Gamma[a][d][e]*Gamma[e][b][cc]
                    R[a][b][cc][d]=sp.simplify(term)
    # lower: R_{abcd}
    Rl=[[[[0]*n for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for cc in range(n):
                for d in range(n):
                    Rl[a][b][cc][d]=sp.simplify(sum(g[a,e]*R[e][b][cc][d] for e in range(n)))
    # raise all: R^{abcd}
    K=0
    for a in range(n):
        for b in range(n):
            for cc in range(n):
                for d in range(n):
                    Rup=0
                    for i in range(n):
                        for j in range(n):
                            for k in range(n):
                                for l in range(n):
                                    Rup+=ginv[a,i]*ginv[b,j]*ginv[cc,k]*ginv[d,l]*Rl[i][j][k][l]
                    K+=Rl[a][b][cc][d]*Rup
    return sp.simplify(K)

coords=[t,r,th,ph]
phi=sp.Function('phi')(r); cl=sp.Function('cl')(r)

# metric A: g_tt = -e^{-2phi} cl^2, g_rr=e^{2phi}
gA=sp.diag(-sp.exp(-2*phi)*cl**2, sp.exp(2*phi), r**2, r**2*sp.sin(th)**2)
# metric B: absorb cl into phi-tilde in the LAPSE keeping g_rr fixed
# define phit such that e^{-2phit} = e^{-2phi} cl^2  => phit = phi - ln(cl)
phit = phi - sp.log(cl)
gB=sp.diag(-sp.exp(-2*phit)*c0**2, sp.exp(2*phi), r**2, r**2*sp.sin(th)**2)
KA=kretschmann(gA,coords)
KB=kretschmann(gB,coords)
print("Kretschmann A - B (lapse-absorption, g_rr fixed) =", sp.simplify(KA-KB))
print("  -> NOTE: this is the VERIFIER CAVEAT case (g_rr held fixed leaves B=1/A family)")

# Honest absorption: a true diffeo/relabel. The claim that cl carries no invariant
# content is tested by: is there ANY phi-tilde making the FULL metric identical?
# g_tt only differs; with g_rr fixed the two metrics are literally different unless
# we also rescale. Test pure relabel phi->phit in BOTH slots is NOT what doc claims.
# Doc claim (L4): cl folds into the LAPSE. Lapse = sqrt(-g_tt). Indeed sqrt(-g_tt)=e^{-phi}cl
# = e^{-phit}c0 with phit=phi-ln(cl/c0). That is a DEFINITION of the lapse potential,
# tautologically true. The Ricci/Kretschmann EQUALITY above tests invariance of geometry.
