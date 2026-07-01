"""
B2-1 GAUGE TEST part 2: solve the gauge constraints to see if a time-dependent
diagonal-only l=2 warp can be PURE GAUGE.

Author warp: h_tt=h_tr=h_rr=0, h_tth=0, h_rth=0 (purely diagonal angular),
             h_thth = r^2 h(t,r) P2 with h time-dependent (carries d_t^2).

From gauge form, require simultaneously:
 (1) h_tt=0:  d_t T = 0           -> T=T(r)
 (2) h_rr=0:  d_r R = 0           -> R=R(t)
 (3) h_tr=0:  d_t R + d_r T = 0
 (4) h_tth=0: T + d_t Th = 0
 (5) h_rth=0: r(R + d_r Th) - 2 Th = 0
Then ask: is the resulting h_thth necessarily TIME-INDEPENDENT? If yes, a
time-dependent diagonal l=2 warp is NOT pure gauge -> physical (carries
gauge-invariant content). That is the radiative DOF.
"""
import sympy as sp

t, r = sp.symbols('t r', real=True)
T = sp.Function('T')(t, r)
R = sp.Function('R')(t, r)
Th = sp.Function('Th')(t, r)

# (1) T = T(r); (2) R = R(t)
Tr = sp.Function('T')(r)
Rt = sp.Function('R')(t)

# (3) dR/dt + dT/dr = 0  => Rt'(t) = -Tr'(r). LHS depends on t only, RHS on r only
#     => both equal a constant k.  Rt = k t + c1 ;  Tr = -k r + c2
k, c1, c2 = sp.symbols('k c1 c2', real=True)
Rt_sol = k*t + c1
Tr_sol = -k*r + c2

# (4) h_tth=0:  T + d_t Th = 0  => d_t Th = -T = -Tr_sol  (function of r only)
#     => Th = -Tr_sol * t + f(r) = (k r - c2) t + f(r)
fr = sp.Function('f')(r)
Th_sol = (k*r - c2)*t + fr

# (5) h_rth=0:  r(R + d_r Th) - 2 Th = 0
expr5 = r*(Rt_sol + sp.diff(Th_sol, r)) - 2*Th_sol
expr5 = sp.expand(sp.simplify(expr5))
print("Constraint (5) residual =", expr5)
# group by t and 1:
poly_t = sp.Poly(expr5, t)
print("  coeff of t^1:", sp.simplify(poly_t.coeff_monomial(t)))
print("  coeff of t^0:", sp.simplify(poly_t.coeff_monomial(1)))

# Now h_thth (diagonal angular trace piece). From gauge run:
# h_thth = 3 r R cos^2 - r R - 12 Th cos^2 + 6 Th  (full theta structure)
# The P2 piece coefficient ~ (3R r ... - 12 Th ...). Time dependence enters via R(t),Th(t,r).
# Build the actual h_thth and test if it can be time-dependent under (1)-(5).
