import sympy as sp

r = sp.symbols('r', positive=True)
th = sp.symbols('theta', positive=True)
A = sp.Function('A')(r)
B = sp.Function('B')(r)
cc = sp.symbols('c', positive=True)   # reference light speed c_E

# ---- FACTS (general A(r),B(r)) ----
g = sp.diag(-A*cc**2, B, r**2, r**2*sp.sin(th)**2)
detg = g.det()
sqrtmg = sp.sqrt(-detg)
print("sqrt(-g) =", sp.simplify(sqrtmg))          # expect cc*sqrt(A*B)*r^2*|sin th|

# coordinate light speed^2 = -g_tt/g_xx
c_eff2 = sp.simplify(-g[0,0]/g[1,1])
print("c_eff^2 =", c_eff2)                          # A c^2 / B

print("volume-blind (sqrt(-g) r-dep) needs A*B = const:", "A*B" )
print("="*50)

# ---- FORMALIZATION 1: clock x ruler = 1 ----
# proper time rate ~ sqrt(A), proper length rate ~ sqrt(B); product =1
Af, Bf = sp.symbols('A B', positive=True)  # local symbols
f1 = sp.Eq(sp.sqrt(Af)*sp.sqrt(Bf), 1)
AB1 = sp.solve(f1, Af*Bf)  # A*B from sqrt(A)sqrt(B)=1 -> AB=1
print("F1 clock*ruler=1 -> A*B =", sp.solve(sp.Eq(sp.sqrt(Af*Bf),1), Af*Bf))
print("  A*B = 1  => CONST => BLIND (control, matches frozen)")
print("="*50)
