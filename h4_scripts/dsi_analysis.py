import sympy as sp

print("="*70)
print("PART C CAS ANALYSIS: running ambient vs frozen-coefficient DSI")
print("="*70)

r, s, Zf, W0, C = sp.symbols('r s Z_phi W0 C', positive=True)
u = sp.Function('u')   # phi_amb(r)
dphi = sp.Function('dphi')

# ---- 1. Confirm frozen indicial roots ----
print("\n[1] FROZEN operator  Z_phi (r^2 dphi')' + 8 W0 dphi = 0, try dphi=r^s")
expr = Zf*( (r**2*(s*(s-1)*r**(s-2))) + 2*r*(s*r**(s-1)) ) + 8*W0*r**s
expr = sp.simplify(expr/r**s)
print("   indicial polynomial / r^s :", sp.expand(expr))
roots = sp.solve(sp.Eq(Zf*(s**2+s)+8*W0,0), s)
print("   roots s =", [sp.simplify(rt) for rt in roots])
Wcrit = sp.solve(sp.Eq(1-32*W0/Zf,0),W0)[0]
print("   discriminant 1-32 W0/Z_phi -> complex when W0 >", Wcrit)
print("   critical depth phi_crit = -1/2 ln(W_crit) =",
      sp.simplify(-sp.Rational(1,2)*sp.log(Wcrit)),
      " ; at Z=1:", float(-sp.Rational(1,2)*sp.log(Wcrit).subs(Zf,1)),
      " at Z=8:", float(-sp.Rational(1,2)*sp.log(Wcrit).subs(Zf,8)))

# ---- 2. The true ambient ODE. autonomous form in t=ln r ----
print("\n[2] TRUE ambient ODE  Z_phi (r^2 u')' = 4 e^{-2u}")
t = sp.symbols('t', real=True)
ut = sp.Function('u')
# in t: (r^2 u')' = u_tt + u_t
print("   in t=ln r (autonomous):  Z_phi (u_tt + u_t) = 4 e^{-2u}")

# try closed form
try:
    sol = sp.dsolve(sp.Eq(Zf*(ut(t).diff(t,2)+ut(t).diff(t)), 4*sp.exp(-2*ut(t))), ut(t))
    print("   dsolve ->", sol)
except Exception as e:
    print("   dsolve FAILED (no elementary closed form):", type(e).__name__, str(e)[:80])

# ---- 3. test candidate asymptotic forms ----
print("\n[3] Dominant-balance asymptotic test (t->inf, u->+inf)")
a,b = sp.symbols('a b')
# (a) linear u = a t + b
uu = a*t+b
res = Zf*(uu.diff(t,2)+uu.diff(t)) - 4*sp.exp(-2*uu)
print("   linear u=a t+b : LHS-RHS =", sp.simplify(res), " (const vs r^{-2a}: no balance unless a=0)")
# (b) u = 1/2 ln( (8/Z) t + C )  -> drop u_tt, balance Z u_t = 4 e^{-2u}
uu = sp.Rational(1,2)*sp.log((8/Zf)*t + C)
lhs_drop = Zf*uu.diff(t)          # keep only damping
rhs = 4*sp.exp(-2*uu)
print("   log-log ansatz u=1/2 ln((8/Z)t+C):")
print("     Z*u_t  =", sp.simplify(lhs_drop))
print("     4e^-2u =", sp.simplify(rhs), "  -> EQUAL:", sp.simplify(lhs_drop-rhs)==0)
utt = uu.diff(t,2); ut1 = uu.diff(t)
print("     u_tt/u_t =", sp.simplify(utt/ut1), " -> 0 as t->inf (dropping u_tt self-consistent)")
