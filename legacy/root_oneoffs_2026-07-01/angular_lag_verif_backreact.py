import sympy as sp
t,r,th,ph,c,xi,kap8 = sp.symbols('t r theta phi c xi kappa8', positive=True)
phi=sp.Function('phi')(r)
g=sp.diag(-sp.exp(-2*phi)*c**2, sp.exp(2*phi), r**2, r**2*sp.sin(th)**2)
ginv=g.inv(); coords=[t,r,th,ph]
# Christoffels
def christ():
    G=[[[0]*4 for _ in range(4)] for _ in range(4)]
    for a in range(4):
        for b in range(4):
            for cc in range(4):
                s=0
                for d in range(4):
                    s+=ginv[a,d]*(sp.diff(g[d,b],coords[cc])+sp.diff(g[d,cc],coords[b])-sp.diff(g[b,cc],coords[d]))
                G[a][b][cc]=sp.simplify(s/2)
    return G
Ga=christ()
# Ricci
def ricci():
    R=sp.zeros(4,4)
    for b in range(4):
        for d in range(4):
            s=0
            for a in range(4):
                s+=sp.diff(Ga[a][b][d],coords[a])-sp.diff(Ga[a][b][a],coords[d])
                for e in range(4):
                    s+=Ga[a][a][e]*Ga[e][b][d]-Ga[a][d][e]*Ga[e][b][a]
            R[b,d]=sp.simplify(s)
    return R
Ric=ricci()
Rs=sp.simplify(sum(ginv[i,j]*Ric[i,j] for i in range(4) for j in range(4)))
G_dd=Ric-sp.Rational(1,2)*g*Rs
G_ud=sp.simplify(ginv*G_dd)
print("G^t_t =",sp.simplify(G_ud[0,0]))
print("G^r_r =",sp.simplify(G_ud[1,1]))
print("G^t_t - G^r_r (expect 0):", sp.simplify(G_ud[0,0]-G_ud[1,1]))
print("G^th_th =",sp.simplify(G_ud[2,2]))
