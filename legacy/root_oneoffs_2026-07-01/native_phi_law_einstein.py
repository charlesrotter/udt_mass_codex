import sympy as sp

t, r, th, ph = sp.symbols('t r theta phi_ang', real=True)
phi = sp.Function('phi')(r)   # dilation field, slaved to metric
c0 = sp.symbols('c0', positive=True)

# CANON metric (CHOSE: static, spherical, diagonal, areal-r):
# ds^2 = -e^{-2phi} c0^2 dt^2 + e^{2phi} dr^2 + r^2 dOmega^2
g = sp.diag(-sp.exp(-2*phi)*c0**2, sp.exp(2*phi), r**2, r**2*sp.sin(th)**2)
ginv = g.inv()
coords = [t, r, th, ph]
n = 4

# Christoffel
def christoffel(g, ginv, coords):
    n=len(coords)
    Gamma=[[[0]*n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                s=0
                for d in range(n):
                    s+= ginv[a,d]*(sp.diff(g[d,b],coords[c])+sp.diff(g[d,c],coords[b])-sp.diff(g[b,c],coords[d]))
                Gamma[a][b][c]=sp.simplify(s/2)
    return Gamma
Gamma=christoffel(g,ginv,coords)

# Ricci
Ric=sp.zeros(n,n)
for b in range(n):
    for c in range(n):
        s=0
        for a in range(n):
            s+=sp.diff(Gamma[a][b][c],coords[a])-sp.diff(Gamma[a][b][a],coords[c])
            for d in range(n):
                s+=Gamma[a][a][d]*Gamma[d][b][c]-Gamma[a][c][d]*Gamma[d][b][a]
        Ric[b,c]=sp.simplify(s)
R=sp.simplify(sum(ginv[i,j]*Ric[i,j] for i in range(n) for j in range(n)))
# Einstein mixed G^mu_nu
G=sp.zeros(n,n)
for i in range(n):
    for j in range(n):
        s=0
        for k in range(n):
            s+=ginv[i,k]*(Ric[k,j]-sp.Rational(1,2)*g[k,j]*R)
        G[i,j]=sp.simplify(s)

print("=== Ricci scalar R ===")
print(sp.simplify(R))
print()
print("=== Einstein tensor G^mu_nu (mixed) ===")
labels=['t','r','th','ph']
for i in range(n):
    val=sp.simplify(G[i,i])
    print(f"G^{labels[i]}_{labels[i]} = {val}")
print()
# Box_g phi (covariant dalembertian of phi(r))
sqrtmg=sp.sqrt(-g.det())
boxphi=0
for mu in range(n):
    boxphi+=sp.diff(sqrtmg*sum(ginv[mu,nu]*sp.diff(phi,coords[nu]) for nu in range(n)),coords[mu])
boxphi=sp.simplify(boxphi/sqrtmg)
print("=== Box_g phi ===")
print(boxphi)
print()
print("=== Box_g phi + G^th_th  (test identity =0) ===")
print(sp.simplify(boxphi+G[2,2]))
