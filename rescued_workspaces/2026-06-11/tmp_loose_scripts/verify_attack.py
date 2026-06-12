import sympy as sp

# ============ ATTACK 4 + Phase A radial-mode claim ============
# Phase A claims: for h_tr longitudinal radial mode, the d_r^2 coeff is ZERO (json: "0"),
# i.e. the radial h_tr is a CONSTRAINT, not an elliptic-propagating mode. The "elliptic"
# claim is then shunted to the TRANSVERSE h_ttheta sector. Let's verify both and check
# whether the phase-carrying field in Phase C (h_tr via Gamma^theta_tr) is the SAME field
# that Phase A's "elliptic Green's function preserves phase" argument applies to.

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

def Gam(a,b,c):
    s=0
    for d in range(4):
        s+=ginv[a,d]*(sp.diff(g[d,b],coords[c])+sp.diff(g[d,c],coords[b])-sp.diff(g[b,c],coords[d]))
    return sp.series(sp.Rational(1,2)*s,eps,0,2).removeO()

# Gamma^theta_{t r} first order  (the Phase C phase carrier)
Gth_tr=sp.simplify(sp.diff(Gam(2,0,1),eps).subs(eps,0))
print("Gamma^th_tr (1st order):", Gth_tr)
co_dth_htr = sp.simplify(Gth_tr.coeff(sp.diff(h_tr,th)))
print("  coeff of d_theta h_tr:", co_dth_htr)
co_hth = sp.simplify(Gth_tr.coeff(h_tth))
co_drhth = sp.simplify(Gth_tr.coeff(sp.diff(h_tth,r)))
print("  coeff of h_ttheta:", co_hth, " coeff of d_r h_ttheta:", co_drhth)
