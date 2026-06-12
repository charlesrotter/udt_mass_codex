import sympy as sp

# Independent re-derivation of Gamma^theta_{tr} on the canonical metric with off-diagonal h_{ti}.
t, r, th, ph, eps = sp.symbols('t r theta phi_coord epsilon', real=True)
coords = [t, r, th, ph]
phi0 = sp.Function('phi0')(r)
h_tr  = sp.Function('h_tr')(r, th, ph)
h_tth = sp.Function('h_tth')(r, th, ph)
h_tph = sp.Function('h_tph')(r, th, ph)

g = sp.zeros(4,4)
g[0,0] = -sp.exp(-2*phi0)
g[1,1] =  sp.exp(2*phi0)
g[2,2] =  r**2
g[3,3] =  r**2*sp.sin(th)**2
g[0,1]=g[1,0]=eps*h_tr
g[0,2]=g[2,0]=eps*h_tth
g[0,3]=g[3,0]=eps*h_tph

# first-order inverse
gbar = g.subs(eps,0)
gbar_inv = gbar.inv()
dg = sp.expand(g - gbar)
ginv = sp.expand(gbar_inv - gbar_inv*dg*gbar_inv)
ginv = ginv.applyfunc(lambda e: sp.series(e, eps, 0, 2).removeO())

def Gamma(a,b,c):
    s = 0
    for d in range(4):
        s += ginv[a,d]*(sp.diff(g[d,b],coords[c]) + sp.diff(g[d,c],coords[b]) - sp.diff(g[b,c],coords[d]))
    return sp.Rational(1,2)*s

# Gamma^theta_{tr}: a=2(theta), b=0(t), c=1(r)
Gth_tr = Gamma(2,0,1)
Gth_tr_1 = sp.simplify(sp.diff(sp.series(Gth_tr,eps,0,2).removeO(), eps).subs(eps,0))
print("MY Gamma^theta_{tr} O(eps) =", Gth_tr_1)

# Claimed: (1/2r^2)(2 h_tth phi0' - d_theta h_tr + d_r h_tth)
claimed = (2*h_tth*sp.diff(phi0,r) - sp.diff(h_tr,th) + sp.diff(h_tth,r))/(2*r**2)
print("CLAIM 1 residual (mine - claimed):", sp.simplify(Gth_tr_1 - claimed))

# CLAIM 2: transverse deflection. Null radial ray: tdot = e^{2phi0} rdot, rdot=1.
# d2theta/dl2 = -Gamma^th_{mu nu} xdot^mu xdot^nu ; cross term = -2 Gamma^th_{tr} tdot rdot
tdot = sp.exp(2*phi0); rdot = 1
new_term = sp.simplify(-2*Gth_tr_1*tdot*rdot)
print("MY new transverse deflection term =", new_term)
claimed2 = (sp.exp(2*phi0)/r**2)*(sp.diff(h_tr,th) - 2*h_tth*sp.diff(phi0,r) - sp.diff(h_tth,r))
print("CLAIM 2 residual (mine - claimed):", sp.simplify(new_term - claimed2))

# coefficient of d_theta h_tr
co = sp.simplify(new_term.coeff(sp.diff(h_tr,th)))
print("coeff of d_theta h_tr in deflection =", co)
print("compare e^{2phi0}/r^2 =", sp.simplify(sp.exp(2*phi0)/r**2))
print("match coeff?:", sp.simplify(co - sp.exp(2*phi0)/r**2)==0)

# Canonical scalar deflection per §12.15.2: 2 e^{2phi0} d_theta dphi / r^2 -> coeff 2 e^{2phi0}/r^2
# So h_tr coefficient is HALF the scalar coefficient (1x vs 2x). Note the structural claim.
print("scalar coeff 2 e^{2phi0}/r^2 =", sp.simplify(2*sp.exp(2*phi0)/r**2))
