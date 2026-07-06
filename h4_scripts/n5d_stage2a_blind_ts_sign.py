"""
Blind independent symbolic derivation of the UDT metric-shear source relation.
Derives:
  (1) delta S_m / delta s      (direct algebraic s-derivative of sqrt(g) L_m)
  (2) Hilbert stress T^A_A = 2 h_AA dL/dh_AA + L, and T_s = T^th_th - T^ps_ps
  (3) the sign relation between them
  (4) explicit T_s
  (5) L2-only rigid check at s=0, f=theta, N=1
Derived only from the primitives supplied in the task prompt.
"""
import sympy as sp

# --- symbols (positive reals where physical) ---
rho, s, fr, ft, N, xi, kappa = sp.symbols('rho s f_r f_theta N xi kappa',
                                          positive=True, real=True)
theta = sp.symbols('theta', real=True)
f = sp.symbols('f', real=True)                 # f value (sin f appears)
# on the physical domain theta in (0,pi), sin(theta) > 0; use a positive symbol
sinth = sp.symbols('sin_theta', positive=True, real=True)
sinf = sp.sin(f)

# transverse 2-metric components as INDEPENDENT symbols a, b
a, b = sp.symbols('a b', positive=True, real=True)   # a=h_thth, b=h_psps

# radial metric
g_rr = sp.Integer(1)
g_rrinv = 1/g_rr

# inverse transverse
g_thth = 1/a
g_psps = 1/b

# --- matter Lagrangian in terms of a,b (independent) ---
# L2 = (xi/2)[ g^rr fr^2 + g^thth ft^2 + g^psps N^2 sin^2 f ]
L2 = (xi/2)*( g_rrinv*fr**2 + g_thth*ft**2 + g_psps*N**2*sinf**2 )

# F_{r psi} = N sin f f_r ; F_{theta psi} = N sin f f_theta
F_rps  = N*sinf*fr
F_thps = N*sinf*ft
# L4 = (kappa/2)[ F_rps^2 g^rr g^psps + F_thps^2 g^thth g^psps ]
L4 = (kappa/2)*( F_rps**2 * g_rrinv*g_psps + F_thps**2 * g_thth*g_psps )

L_m = L2 + L4

# sqrt(g) = sqrt(g_rr a b)  (with metric subst = rho^2 sin theta, s-independent)
sqrtg_ab = sp.sqrt(g_rr*a*b)

# metric substitution: a = rho^2 e^s, b = rho^2 e^{-s} sin^2 theta
subs_metric = {a: rho**2*sp.exp(s), b: rho**2*sp.exp(-s)*sinth**2}

# ============================================================
# (1) delta S_m/delta s = d(sqrt(g) L_m)/ds directly
#     substitute metric FIRST (so a,b depend on s), then d/ds
# ============================================================
action_density = (sqrtg_ab*L_m).subs(subs_metric)
dSm_ds = sp.simplify(sp.diff(action_density, s))
print("=== (1) delta S_m/delta s (direct d/ds of sqrt(g) L_m) ===")
print(sp.simplify(dSm_ds))
print()

# ============================================================
# (2) Hilbert mixed stress: T^A_A = 2 h_AA dL/dh_AA + L
# ============================================================
Tth = 2*a*sp.diff(L_m, a) + L_m       # T^theta_theta
Tps = 2*b*sp.diff(L_m, b) + L_m       # T^psi_psi
Ts_ab = sp.simplify(Tth - Tps)
Ts = sp.simplify(Ts_ab.subs(subs_metric))
print("=== (4)/(A) T_s = T^th_th - T^ps_ps (metric substituted) ===")
print(sp.simplify(Ts))
print()

# separate L2 and L4 parts of T_s
Tth_L2 = 2*a*sp.diff(L2, a) + L2
Tps_L2 = 2*b*sp.diff(L2, b) + L2
Ts_L2 = sp.simplify((Tth_L2 - Tps_L2).subs(subs_metric))
Tth_L4 = 2*a*sp.diff(L4, a) + L4
Tps_L4 = 2*b*sp.diff(L4, b) + L4
Ts_L4 = sp.simplify((Tth_L4 - Tps_L4).subs(subs_metric))
print("   T_s L2-part:", sp.simplify(Ts_L2))
print("   T_s L4-part:", sp.simplify(Ts_L4))
print()

# ============================================================
# (3) sign relation: dSm_ds  -  (rho^2 sin/2) * T_s
# ============================================================
rhs = (rho**2*sinth/2)*Ts
diff_plus = sp.simplify(dSm_ds - rhs)
diff_minus = sp.simplify(dSm_ds - (-rhs))
print("=== (3)/(B) sign relation ===")
print("dSm_ds - (+ rho^2 sin/2 T_s) =", diff_plus)
print("dSm_ds - (- rho^2 sin/2 T_s) =", diff_minus)
if diff_plus == 0:
    print("RELATION: delta S_m/delta s = +(rho^2 sin/2)(T^th_th - T^ps_ps)  [PLUS]")
elif diff_minus == 0:
    print("RELATION: delta S_m/delta s = -(rho^2 sin/2)(T^th_th - T^ps_ps)  [MINUS]")
else:
    print("RELATION: neither exact; check factor:",
          sp.simplify(dSm_ds/rhs))
print()

# ============================================================
# (5)/(C) L2-only rigid check at s=0, f=theta (=> f_theta=1), N=1
# ============================================================
# f=theta => sin f = sin theta = sinth (our positive symbol)
Ts_L2_check = Ts_L2.subs({s: 0, N: 1, sinf: sinth, ft: 1, fr: fr})
Ts_L2_check = sp.simplify(Ts_L2_check)
print("=== (5)/(C) L2-only T_s at s=0, f=theta, f_theta=1, N=1 ===")
print("T_s(L2) =", Ts_L2_check)
# also show the general L2 T_s at s=0 for context
print("   (general L2 T_s at s=0):",
      sp.simplify(Ts_L2.subs(s, 0)))
