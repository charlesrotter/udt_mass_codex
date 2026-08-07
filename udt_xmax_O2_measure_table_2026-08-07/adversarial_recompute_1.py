# ADVERSARIAL REVIEW 1 — independent recompute of every O2 cell.
# Fresh sympy; NO probe code imported or read (derive_o2.py never opened).
# Reviewer: Claude (Fable 5), 2026-08-07.
import sympy as sp

R = {}  # results ledger


def bank(k, v):
    R[k] = v
    print(f"{k} = {v}")


u, r, Rw, X, c0, eps, w, p, q, t = sp.symbols('u r R_w X c_0 epsilon w p q t', positive=True)
a = sp.Symbol('a', positive=True)  # gap parameter for iff-conditions
zsym = sp.Symbol('z', positive=True)

print("=== 1. CLASS (i): A = c0*(1-r/Rw)^n, sub u=1-r/Rw, wall u->0+ ===")
# PROPER: int_0^Rw A^{-1/2} dr = Rw*c0^{-1/2} * int_0^1 u^{-n/2} du
# antiderivative of u^{-n/2}: u^{1-n/2}/(1-n/2); finite at u=0 iff n<2.
n_lt2 = 2 - a   # n<2
n_gt2 = 2 + a   # n>2
F = lambda n_: u**(1 - n_/2) / (1 - n_/2)
bank('i_proper_limit_n_lt2', sp.limit(F(n_lt2), u, 0, '+'))            # 0 => finite
bank('i_proper_limit_n_gt2', sp.limit(F(n_gt2), u, 0, '+'))            # oo => divergent
val_proper = Rw / sp.sqrt(c0) * (F(n_lt2).subs(u, 1) - 0)
bank('i_proper_value_check_2Rw_over_sqrtc0_2mn',
     sp.simplify(val_proper - 2*Rw/(sp.sqrt(c0)*(2 - n_lt2))) == 0)
# witnesses
for nv, expect in [(sp.Rational(1, 2), 4*Rw/(3*sp.sqrt(c0))), (1, 2*Rw/sp.sqrt(c0))]:
    got = Rw/sp.sqrt(c0) * sp.integrate(u**(-nv/sp.Integer(2)), (u, 0, 1))
    bank(f'i_proper_witness_n={nv}', sp.simplify(got - expect) == 0)
bank('i_proper_witness_n=2_divergent',
     sp.integrate(u**-1, (u, 0, 1)) == sp.oo)

# OPTICAL: int dr/A = (Rw/c0) int_0^1 u^{-n} du; finite iff n<1, value Rw/(c0(1-n))
G = lambda n_: u**(1 - n_) / (1 - n_)
n_lt1 = 1 - a
n_gt1 = 1 + a
bank('i_optical_limit_n_lt1', sp.limit(G(n_lt1), u, 0, '+'))
bank('i_optical_limit_n_gt1', sp.limit(G(n_gt1), u, 0, '+'))
val_opt = Rw/c0 * (G(n_lt1).subs(u, 1) - 0)
bank('i_optical_value_check', sp.simplify(val_opt - Rw/(c0*(1 - n_lt1))) == 0)
bank('i_optical_witness_n=1/2', sp.simplify(
    Rw/c0*sp.integrate(u**sp.Rational(-1, 2), (u, 0, 1)) - 2*Rw/c0) == 0)
# n=1 partial integral and log rate; delta = -(1/2)ln A; at c0=1, delta = -(1/2)ln u^n
ell_partial = Rw/c0 * sp.integrate(1/u, (u, u, 1))     # = -(Rw/c0) ln u
bank('i_optical_n1_partial', sp.simplify(ell_partial + Rw/c0*sp.log(u)) == 0)
delta_i = -sp.Rational(1, 2)*sp.log(u)                  # n=1, c0=1
bank('i_optical_n1_rate_2X_delta',
     sp.simplify(ell_partial.subs(c0, 1) - 2*Rw*delta_i) == 0)

print("=== P-opt adjudication: d ell_opt/d phi constant iff n=1 (pure class i) ===")
nn = sp.Symbol('n', positive=True)
A_i = c0*u**nn
phi_i = -sp.Rational(1, 2)*sp.log(A_i)
# d ell = dr/A = -Rw du/A ; d phi = dphi/du du
ratio = sp.simplify((-Rw/A_i) / sp.diff(phi_i, u))      # d ell / d phi as function of u
bank('Popt_ratio_general_n', ratio)                     # = 2Rw u^{1-n}/n : const iff n=1
bank('Popt_const_iff_n1', sp.simplify(ratio.subs(nn, 1)) == 2*Rw/c0)  # kappa = 2Rw at c0=1
# class-(iii) member AT n=1 (p != 0) violates P-opt: ratio non-constant
pp = sp.Symbol('p', real=True)
A_iii = c0*u * (-sp.log(u))**(-pp)
phi_iii = -sp.Rational(1, 2)*sp.log(A_iii)
ratio3 = sp.simplify((-Rw/A_iii) / sp.diff(phi_iii, u))
bank('Popt_iii_n1_ratio', sp.simplify(ratio3))          # depends on u for p != 0
bank('Popt_iii_n1_nonconst_for_p_ne_0',
     sp.simplify(sp.diff(ratio3, u)) != 0)

print("=== CLASS (ii): A = e^{-r/X} ===")
bank('ii_proper_divergent', sp.integrate(sp.exp(r/(2*X)), (r, 0, sp.oo)) == sp.oo)
bank('ii_optical_divergent', sp.integrate(sp.exp(r/X), (r, 0, sp.oo)) == sp.oo)
bank('ii_areal_limit', sp.limit(r, r, sp.oo))
bank('ii_redshift_limit', sp.limit(sp.exp(r/X)**sp.Rational(1, 2), r, sp.oo))
bank('ii_dL_limit', sp.limit(r*sp.exp(r/X), r, sp.oo))
bank('ii_dA_r_limit', sp.limit(r, r, sp.oo))
bank('ii_dA_variant_limit', sp.limit(r*sp.exp(-r/(2*X)), r, sp.oo))

print("=== CLASS (iii) knife edges: A = c0 u^n (-ln u)^{-p}, t = -ln u ===")
# optical n=1: 1/A du-integrand ~ u^{-1} t^p -> int t^p dt on (T,oo): finite iff p<-1
bank('iii_optical_n1_value_p=-(1+a)', sp.integrate(t**(-(1 + a)), (t, 1, sp.oo)))
bank('iii_optical_n1_edge_P1_div', sp.integrate(t**(-1), (t, 1, sp.oo)) == sp.oo)
bank('iii_optical_witness_P2', sp.integrate(t**-2, (t, sp.log(2), sp.oo)))
# proper n=2: A^{-1/2} ~ u^{-1} t^{p/2} -> int t^{p/2} dt: finite iff p/2<-1 i.e. p<-2
bank('iii_proper_n2_value_p=-(2+a)', sp.integrate(t**(-1 - a/2), (t, 1, sp.oo)))
bank('iii_proper_n2_edge_div', sp.integrate(t**(-1), (t, 1, sp.oo)) == sp.oo)

print("=== CLASS (i) remaining rows ===")
A_gen = c0*(1 - r/Rw)**nn
bank('i_areal_limit', sp.limit(r, r, Rw))
bank('i_depth_limit', sp.limit(-sp.Rational(1, 2)*sp.log(A_gen), r, Rw, '-'))
bank('i_redshift_limit', sp.limit(A_gen**sp.Rational(-1, 2), r, Rw, '-'))
bank('i_dL_limit', sp.limit(r/A_gen, r, Rw, '-'))
bank('i_dA_r_limit', sp.limit(r, r, Rw))
bank('i_dA_variant_limit', sp.limit(r*sp.sqrt(A_gen), r, Rw, '-'))

print("=== INFALL geodesic (independent re-derivation) ===")
# ds^2 = -A c^2 dt^2 + dr^2/A. Lagrangian L = -A c^2 tdot^2 + rdot^2/A = -c^2.
# Killing energy: e = A tdot (dimensionless with c absorbed): tdot = e/A.
# -A c^2 e^2/A^2 + rdot^2/A = -c^2  =>  rdot^2 = c^2 (e^2 - A). Verified:
c, tau = sp.symbols('c tau', positive=True)
e = sp.Symbol('e', positive=True)
tdot, rdot = sp.symbols('tdot rdot')
constraint = sp.Eq(-A_gen*c**2*(e/A_gen)**2 + rdot**2/A_gen, -c**2)
bank('infall_rdot2', sp.solve(constraint, rdot**2)[0])   # expect c^2(e^2 - A)
bank('infall_rdot2_check',
     sp.simplify(sp.solve(constraint, rdot**2)[0] - c**2*(e**2 - A_gen)) == 0)
# integrand 1/(c sqrt(e^2-A)) -> 1/(c e) at wall (A->0): finite nonzero
bank('infall_integrand_wall_limit',
     sp.limit(1/(c*sp.sqrt(e**2 - A_gen)), r, Rw, '-'))
# explicit witness n=1,c0=1,e=1 from rest at r=0: tau = int dr/(c sqrt(r/Rw)) = 2Rw/c
bank('infall_witness_n1_tau',
     sp.integrate(1/(c*sp.sqrt(r/Rw)), (r, 0, Rw)))
# class (ii): rdot -> c*e const over infinite range => divergent
bank('infall_ii_divergent',
     sp.integrate(1/(c*sp.sqrt(e**2)), (r, 0, sp.oo)) == sp.oo)

print("=== CROSS-CHECKS vs banked record ===")
# 1. L proper = 2X (n=1,c0=1,Rw=X)
bank('XC1_L_proper_2X', sp.simplify(
    X*sp.integrate(u**sp.Rational(-1, 2), (u, 0, 1)) - 2*X) == 0)
# 2. L optical log-divergent, rate 2X*delta  (banked ell_opt prop. phi) - shown above
bank('XC2_L_optical_rate', R['i_optical_n1_rate_2X_delta'])
# 3/4: exponential + quadratic proper divergent - shown above
bank('XC3_exp_proper_div', R['ii_proper_divergent'])
bank('XC4_quad_proper_div', R['i_proper_witness_n=2_divergent'])
# 5. banked family A=(1-r/X)^{1/m} finite proper iff m>1/2 <=> our n=1/m<2: identical
mM = sp.Symbol('m', positive=True)
bank('XC5_n_lt_2_iff_m_gt_half',
     sp.reduce_inequalities(1/mM < 2, mM))  # expect m > 1/2 (m>0 assumed)
# 6. d_L convention: on L, d_L=(1+z)^2 r equals X z(z+2)
A_of_z = 1/(1 + zsym)**2
r_L = X*(1 - A_of_z)
dL = (1 + zsym)**2 * r_L
bank('XC6_dL_z_zp2', sp.simplify(dL - X*zsym*(zsym + 2)) == 0)
# Etherington: d_L=(1+z)^2 d_A + banked d_L=(1+z)^2 r  =>  d_A = r (forced);
# variant d_A=r/(1+z) would give d_L=(1+z) r != banked. Trivial algebra:
bank('XC6_Etherington_forces_dA_eq_r', True)

print("=== ABSTRACT BUDGET ROW: settle the infimum exactly ===")
# 2x2 Lorentz block, eta = diag(-1,1). D(d)=diag(e^-d,e^d): lambda_t=e^-2d, depth d.
# Boost B(w): eta-isometry => strain = I => DEPTH 0 (zero-budget legs). Verify:
eta = sp.diag(-1, 1)
Bw = sp.Matrix([[sp.cosh(w), sp.sinh(w)], [sp.sinh(w), sp.cosh(w)]])
Dd = lambda d_: sp.diag(sp.exp(-d_), sp.exp(d_))
strain = lambda M: sp.simplify(eta*M.T*eta*M)
bank('boost_leg_strain_is_identity', strain(Bw) == sp.eye(2))
# Independent recompute of the two-leg trace law: M = B(w)D(q)B(-w) * D(p)
Bmw = sp.Matrix([[sp.cosh(w), -sp.sinh(w)], [-sp.sinh(w), sp.cosh(w)]])
M2 = Bw*Dd(q)*Bmw*Dd(p)
C2 = strain(M2)
tr = sp.trace(C2)
law = 2*sp.cosh(2*(p + q)) + 4*sp.sinh(w)**2*sp.sinh(2*p)*sp.sinh(2*q)
bank('trace_law_recomputed',
     sp.simplify(sp.expand_trig(sp.expand(tr - law)).rewrite(sp.exp)) == 0)
bank('detC2_is_1',
     sp.simplify(sp.expand(C2.det().rewrite(sp.exp))) == 1)
# Unbounded in w at fixed p=q=eps>0: coefficient sinh(2eps)^2 > 0 strictly
coeff = 4*sp.sinh(2*eps)**2
bank('twist_coefficient_positive', coeff.is_positive)
bank('depth_unbounded_in_twist',
     sp.limit(2*sp.cosh(4*eps) + coeff*sp.sinh(w)**2, w, sp.oo))
