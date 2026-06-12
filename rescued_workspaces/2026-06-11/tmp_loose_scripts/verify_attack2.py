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
def Gam(a,b,c):
    s=0
    for d in range(4):
        s+=ginv[a,d]*(sp.diff(g[d,b],coords[c])+sp.diff(g[d,c],coords[b])-sp.diff(g[b,c],coords[d]))
    return sp.series(sp.Rational(1,2)*s,eps,0,2).removeO()
Gth_tr=sp.simplify(sp.diff(Gam(2,0,1),eps).subs(eps,0))

# transverse accel cross term a^theta_new = -2 Gamma^th_tr tdot rdot, tdot=e^{2phi}, rdot=1
tdot=sp.exp(2*phi)
a_new = sp.simplify(-2*Gth_tr*tdot)
print("a_theta_new_cross =", a_new)
# coeff of d_theta h_tr (the claimed kernel e^{2phi}/r^2)
coeff = sp.simplify(sp.diff(a_new, sp.Derivative(h_tr,th)))
print("coeff of d_theta h_tr =", coeff)

# KEY ATTACK: a_new also contains h_ttheta and d_r h_ttheta terms (PURE transverse off-diag).
# The h_tr piece is ONLY -d_theta h_tr. So the "phase carrier" via h_tr is the d_theta h_tr term.
# But note Phase A found h_tr (longitudinal/radial) is a CONSTRAINT field (d_r^2 coeff = 0),
# while h_ttheta is the elliptic-propagating transverse field. 
# Phase C identifies h_tr proportional to d_r delta_phi. Let's check: is h_tr even sourced
# by the RADIAL current J_r = T^{tr}? In Einstein eq, T^{tr} sources delta_G_tr.
# Phase A delta_G_tr radial-isolated operator (h_ttheta=h_tph=0, h_tr=Htr(r)):
Htr=sp.Function('Htr')(r)
# reuse delta_G_tr from full calc:
# Build Einstein tensor delta_G_tr quickly via Phase A's structure is expensive; instead
# test Phase A's stated result: radial d_r^2 h_tr coeff = 0.  Verify from delta_G_tr json:
# json delta_G_tr has NO Derivative(h_tr,(r,2)) term. Confirm by inspection of structure:
print()
print("Phase A reported Q1_radial_second_deriv_coeff_tr = 0 (h_tr radial is CONSTRAINT, not elliptic)")
print("=> the 'phase-preserving elliptic Green function' argument applies to h_ttheta, NOT h_tr.")
