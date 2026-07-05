import sympy as sp
r,t,th,ps = sp.symbols('r t theta psi', real=True)
phi = sp.Function('phi')(r)
c,lam,N,om = sp.symbols('c lambda N omega', positive=True)
Th = sp.Function('Theta')(r)

# canonical constrained metric  ds^2 = -e^{-2phi}c^2 dt^2 + e^{2phi} dr^2 + r^2(dth^2 + sin^2 th dps^2)
g = sp.diag(-sp.exp(-2*phi)*c**2, sp.exp(2*phi), r**2, r**2*sp.sin(th)**2)
coords=[t,r,th,ps]
ginv = g.inv()
detg = g.det()
sqrt_mg = sp.sqrt(-sp.simplify(detg))
print("sqrt(-g) =", sp.simplify(sqrt_mg), " (phi-free?)")
print("g^tt =", sp.simplify(ginv[0,0]))
print("g^rr =", sp.simplify(ginv[1,1]))
print("g^psipsi =", sp.simplify(ginv[3,3]))

# hedgehog:  unit 3-vector n = (sinTheta cos chi, sinTheta sin chi, cosTheta),  chi = N psi + om t
chi = N*ps + om*t
n = sp.Matrix([sp.sin(Th)*sp.cos(chi), sp.sin(Th)*sp.sin(chi), sp.cos(Th)])
def dmu(mu): return sp.Matrix([sp.diff(comp, coords[mu]) for comp in n])
G = sp.Matrix(4,4, lambda a,b: sp.simplify(dmu(a).dot(dmu(b))))
# X = g^{mn} G_mn
X = sp.simplify(sum(ginv[a,a]*G[a,a] for a in range(4)))
print("\nG_rr =", sp.simplify(G[1,1]))
print("G_psipsi =", sp.simplify(G[3,3]))
print("G_tt =", sp.simplify(G[0,0]))
print("X = g^{mn}G_mn =", X)

# static piece (om=0):
Xstat = sp.simplify(X.subs(om,0))
print("\nX(om=0) =", Xstat)
# the time-channel addition:
print("X - X(om=0) =", sp.simplify(X - Xstat))

# shift weights: phi -> phi + lam
def weight(expr):
    e2 = expr.subs(phi, phi+lam)
    return sp.simplify(e2/expr)
print("\nshift factor of g^tt:", weight(ginv[0,0]))
print("shift factor of g^rr:", weight(ginv[1,1]))
print("shift factor of e^{-2phi}Th'^2 (radial term):", weight(sp.exp(-2*phi)*sp.Derivative(Th,r)**2))
print("shift factor of e^{+2phi} term (time term):", weight(sp.exp(2*phi)))
