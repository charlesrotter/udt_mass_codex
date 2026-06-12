"""Attack D+E: throat threshold V(infinity); does ANY J!=0 member lift it?
Plus curvature identity of the throat metric."""
import sympy as sp

r = sp.Symbol("r", positive=True)
al, ga, J, lam, b0 = sp.symbols("alpha gamma J lambda b_0", positive=True)
f = sp.Function("f", positive=True)(r)
rho = sp.Function("rho", positive=True)(r)

def EL(L, v):
    return sp.simplify((L.diff(v) - sp.diff(L.diff(v.diff(r)), r)).doit())

V = f*lam/rho**2 + f*sp.diff(f*rho.diff(r), r)/rho

print("== D1: exhibited throat (beta = b0 rho^2) ==")
rho_t = sp.sqrt(J + r**2)
f_t = (al*r + ga)/rho_t
V_t = sp.simplify(V.subs([(f, f_t), (rho, rho_t)]).doit())
print("V(oo) =", sp.limit(V_t, r, sp.oo))
print("f(oo) =", sp.limit(f_t, r, sp.oo), "; rho(oo) = oo;  f' sign:",
      sp.simplify(sp.diff(f_t, r)))
print("phi(oo) = -(1/2)ln alpha (finite):",
      sp.simplify(sp.limit(-sp.log(f_t)/2, r, sp.oo)))
dphids = sp.simplify((-sp.diff(f_t, r)/(2*sp.sqrt(f_t))))
print("dphi/ds = -f'/(2 sqrt f) =", sp.simplify(dphids),
      "  -> >0 iff gamma*r > alpha*J ... sign flips at r = alpha*J/gamma" )

print("\n== D2: engineered cylinder-end member (alpha = 0) ==")
# target solution: rho = rho_oo - exp(-r), f = gamma/rho  (u = f rho = gamma const)
# required beta from first integral: beta = J/(1 - rho'^2), rho' = e^{-r} = rho_oo - rho
# => beta(rho) = J/(1 - (rho_oo - rho)^2)
rho_oo = sp.Symbol("rho_oo", positive=True)
rho_c = rho_oo - sp.exp(-r)
f_c = ga/rho_c
beta_expr = J/(1 - (rho_oo - rho)**2)
L_c = sp.Rational(1, 4)*sp.diff(f*rho, r)**2 + beta_expr*(1 + rho.diff(r)**2)
ELf_c = EL(L_c, f)
ELr_c = EL(L_c, rho)
print("EL_f on member:", sp.simplify(ELf_c.subs([(f, f_c), (rho, rho_c)]).doit()))
print("EL_rho on member:", sp.simplify(ELr_c.subs([(f, f_c), (rho, rho_c)]).doit()))
print("first integral check beta(1-rho'^2) =",
      sp.simplify(beta_expr.subs(rho, rho_c)*(1 - sp.diff(rho_c, r)**2)))
V_c = sp.simplify(V.subs([(f, f_c), (rho, rho_c)]).doit())
print("V(oo) =", sp.simplify(sp.limit(V_c, r, sp.oo)), "  (= gamma*lam/rho_oo^3 > 0 ?)")
print("f(oo) =", sp.limit(f_c, r, sp.oo), "> 0; f positive and monotone:",
      sp.simplify(sp.diff(f_c, r)))
print("phi(oo) finite:", sp.simplify(sp.limit(-sp.log(f_c)/2, r, sp.oo)))
print("beta at the end: beta(rho_oo) =", beta_expr.subs(rho, rho_oo),
      "; beta'(rho_oo) =", sp.simplify(sp.diff(beta_expr, rho).subs(rho, rho_oo)),
      "; beta''(rho_oo) =", sp.simplify(sp.diff(beta_expr, rho, 2).subs(rho, rho_oo)))
# domain sanity: need rho>0 and 1-(rho_oo-rho)^2 > 0 i.e. e^{-2r}<1: r>0. OK.

print("\n== D3: can alpha != 0 lift? (confining check) ==")
# with alpha != 0 on a cylinder end, f ~ alpha*r/rho_oo -> oo and V -> oo (confining)
f_lin = (al*r + ga)/rho_c
V_lin = sp.simplify(V.subs([(f, f_lin), (rho, rho_c)]).doit())
print("V(oo) with alpha != 0 on cylinder end:", sp.limit(V_lin, r, sp.oo))
