"""
B2-1 GAUGE TEST part 3: with c2=0 and f solving r f' - 2 f = -c1 r,
compute the gauge h_thth and test whether it can be TIME-DEPENDENT
while keeping h_tt=h_tr=h_rr=h_tth=h_rth=0 (the author's diagonal warp).
"""
import sympy as sp

t, r, th = sp.symbols('t r theta', real=True)
k, c1 = sp.symbols('k c1', real=True)

# Solve r f' - 2 f + c1 r = 0  (first-order linear ODE)
f = sp.Function('f')
sol = sp.dsolve(sp.Eq(r*sp.Derivative(f(r), r) - 2*f(r) + c1*r, 0), f(r))
print("f(r) =", sol.rhs)
fr = sol.rhs   # general solution with constant C1

# c2=0:
Tr = -k*r
Rt = k*t + c1
Th = k*r*t + fr

# h_thth (full) from gauge run: 3 r R cos^2 - r R - 12 Th cos^2 + 6 Th
ct2 = sp.cos(th)**2
h_thth = 3*r*Rt*ct2 - r*Rt - 12*Th*ct2 + 6*Th
h_thth = sp.expand(sp.simplify(h_thth))
print("\nh_thth (pure-gauge, constraints applied) =", h_thth)
# Coefficient of t:
poly = sp.Poly(h_thth, t)
print("\n  d(h_thth)/dt =", sp.simplify(sp.diff(h_thth, t)))
print("  d^2(h_thth)/dt^2 =", sp.simplify(sp.diff(h_thth, t, 2)))
print("\nINTERPRETATION:")
print("  The gauge h_thth at most LINEAR in t (d_t^2 = 0). A pure-gauge l=2")
print("  diagonal warp CANNOT carry d_t^2 content. The author's warp DOES")
print("  (coeff r^2 P2/2 != 0). => the d_t^2 mode is GAUGE-INVARIANT / PHYSICAL.")
