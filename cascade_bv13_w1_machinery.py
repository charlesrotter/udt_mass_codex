"""bv13 W1 chunk 0: validate the moving-endpoint second-variation FORMULA on an exact toy.

Claimed general formula (my own derivation, to be validated exactly here):
  S(eps) = int_{a(eps)}^{b(eps)} L(y(r,eps), y_r(r,eps)) dr,  y possibly vector.
  S''(0) = B_b - B_a + INT2 + EL2
    B_b = L'(b) b1^2 + 2 (L_y.u + L_{y'}.u')|_b b1 + L(b) b2 + p(b).w(b)
    (same at a with a1,a2), where
      b1=b'(0), b2=b''(0), u=y_eps|_0, w=y_epseps|_0, p=L_{y'},
      L'(b) = total d/dr of L along the eps=0 field at r=b,
    INT2 = int_a^b [L_yy u^2 + 2 L_yy' u u' + L_y'y' u'^2] dr  (all pairings, vector),
    EL2  = int_a^b EL(y0).w dr   (vanishes on-shell; kept here since toy y0 need not be on-shell?
           -- NO: we test with y0 NOT on shell to be maximally strict, so keep EL2 AND also the
           first-order-in-w boundary term is already in p.w; the identity below is exact for ANY family.)
Exactness test: pick concrete polynomial L, y(r,eps) (2 components), a(eps), b(eps);
compute S(eps) in closed form; compare series coefficient of eps^2 with the formula.
"""
import sympy as sp

r, e = sp.symbols('r epsilon')

# concrete but generic-ish polynomial family (2 components), moving endpoints
y1 = 1 + r + sp.Rational(1,3)*r**2 + e*(2 - r + r**3) + e**2*(sp.Rational(1,2) + r**2)
y2 = 2 - r**2 + e*(1 + r - 2*r**2) + e**2*(r - sp.Rational(1,4)*r**3)
a  = sp.Rational(1,10) + e*sp.Rational(1,3) + e**2*sp.Rational(1,7)
b  = 2 + e*sp.Rational(1,2) - e**2*sp.Rational(1,5)

q1, q2, q1p, q2p = sp.symbols('q1 q2 q1p q2p')
L = q1p**2/2 - 3*q2p**2/2 + q1p*q2 + q1*q2p*q2 + q1**2*q2 - q1*q2**2 + q2**3/3 + q1p*q2p*q1

def Lat(rv, ev):
    return L.subs({q1: y1, q2: y2, q1p: sp.diff(y1, r), q2p: sp.diff(y2, r)}, simultaneous=True)

Lfield = L.subs({q1: y1, q2: y2, q1p: sp.diff(y1, r), q2p: sp.diff(y2, r)}, simultaneous=True)
S = sp.integrate(Lfield, (r, a, b))          # polynomial -> exact
S2_exact = sp.diff(S, e, 2).subs(e, 0)
S2_exact = sp.simplify(S2_exact)

# ---- formula side ----
ys  = [y1, y2]
qs  = [q1, q2]; qps = [q1p, q2p]
y0  = [yy.subs(e, 0) for yy in ys]
u   = [sp.diff(yy, e).subs(e, 0) for yy in ys]
w   = [sp.diff(yy, e, 2).subs(e, 0) for yy in ys]
a0, a1, a2 = a.subs(e,0), sp.diff(a,e).subs(e,0), sp.diff(a,e,2).subs(e,0)
b0, b1, b2 = b.subs(e,0), sp.diff(b,e).subs(e,0), sp.diff(b,e,2).subs(e,0)

subs0 = {q1: y0[0], q2: y0[1], q1p: sp.diff(y0[0], r), q2p: sp.diff(y0[1], r)}
L0    = L.subs(subs0, simultaneous=True)
Lp0   = sp.diff(L0, r)                                   # total r-derivative along eps=0 field
Ly    = [sp.diff(L, q).subs(subs0, simultaneous=True) for q in qs]
Lyp   = [sp.diff(L, qp).subs(subs0, simultaneous=True) for qp in qps]
# EL of the eps=0 field (toy is NOT on-shell; formula must include EL2)
EL = [sp.diff(L, qs[i]).subs(subs0, simultaneous=True)
      - sp.diff(sp.diff(L, qps[i]).subs(subs0, simultaneous=True), r) for i in range(2)]

def Bterm(pt, c1, c2):
    lin = sum(Ly[i]*u[i] + Lyp[i]*sp.diff(u[i], r) for i in range(2))
    sec = sum(Lyp[i]*w[i] for i in range(2))
    return (Lp0*c1**2 + 2*lin*c1 + L0*c2 + sec).subs(r, pt)

# quadratic integrand: full second differential of L in (u, u')
d2L = 0
vars_ = qs + qps
du   = u + [sp.diff(uu, r) for uu in u]
for i in range(4):
    for j in range(4):
        d2L += sp.diff(L, vars_[i], vars_[j]).subs(subs0, simultaneous=True)*du[i]*du[j]
INT2 = sp.integrate(d2L, (r, a0, b0))
EL2  = sp.integrate(sum(EL[i]*w[i] for i in range(2)), (r, a0, b0))
# off-shell also the FIRST-variation boundary term p.w was included in Bterm; and off-shell the
# integral of (Ly.w + Lyp.w') = [p.w] + int EL.w  -- consistent with Bterm containing p.w + EL2 kept.

S2_formula = sp.simplify(Bterm(b0, b1, b2) - Bterm(a0, a1, a2) + INT2 + EL2)
diff = sp.simplify(S2_exact - S2_formula)
print("chunk0 machinery: S''(0) exact - formula =", diff)
print("chunk0 verdict:", "PASS" if diff == 0 else "FAIL")
