import sympy as sp

t,r,th,ps = sp.symbols('t r theta psi', real=True)
phi = sp.Function('phi')(r)
rho = sp.Function('rho')(r)      # areal radius
Th  = sp.Function('Theta')(r)    # winding profile
c   = sp.symbols('c', positive=True)
N   = sp.symbols('N', real=True)
om  = sp.symbols('omega', real=True)
xi,kap,Z = sp.symbols('xi kappa Z_phi', positive=True)
j   = sp.Function('j')(r)        # frame-drag potential g_tpsi = j(r) sin^2 theta

# ---- diagonal metric (canonical UDT, h_AB = rho^2 dOmega^2), plus small g_tpsi ----
gtpsi = j*sp.sin(th)**2
g = sp.Matrix([
 [-sp.exp(-2*phi)*c**2, 0, 0, gtpsi],
 [0, sp.exp(2*phi), 0, 0],
 [0, 0, rho**2, 0],
 [gtpsi, 0, 0, rho**2*sp.sin(th)**2]])
ginv = g.inv()
print("g^tt   =", sp.simplify(ginv[0,0]))
print("g^rr   =", sp.simplify(ginv[1,1]))
print("g^psps =", sp.simplify(ginv[3,3]))
print("g^tps  =", sp.simplify(ginv[0,3]))

# ---- diagonal-only limit (j=0): confirm signs ----
gd = g.subs(j,0); gdi = gd.inv()
print("\n[diagonal j=0]")
print("g^tt   =", sp.simplify(gdi[0,0]), "   (=-e^{2phi}/c^2 <0)")
print("g^psps =", sp.simplify(gdi[3,3]), "   (>0)")

# ---- n-field: hedgehog with winding profile Theta(r) and internal phase chi=N*psi+om*t ----
# n = (sinTh cos chi, sinTh sin chi, cosTh),  chi = N*psi + om*t
chi = N*ps + om*t
n = sp.Matrix([sp.sin(Th)*sp.cos(chi), sp.sin(Th)*sp.sin(chi), sp.cos(Th)])
coords = [t,r,th,ps]
# strain S_mn = d_m n . d_n n
def dn(mu): return sp.Matrix([sp.diff(n[i],coords[mu]) for i in range(3)])
S = sp.Matrix(4,4, lambda a,b: (dn(a).T*dn(b))[0])
# L2 density (no measure): X = g^{mn} S_mn  (use diagonal j=0)
X = sum(gdi[a,b]*S[a,b] for a in range(4) for b in range(4))
X = sp.simplify(X)
print("\nX = g^{mn} dn.dn =", X)
