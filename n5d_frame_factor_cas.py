"""n5d_frame_factor_cas.py -- CAS check of the source frame factor for E_s + T_s = 0.
DECIDES whether coded E_s (EAB_shear_row) is the DENSITY (delta L_geo/delta s)/sin(th) [carries the
sqrt(h)=rho^2 measure weight => matter source needs a rho^2 factor] OR the bare mixed component
E^th_th - E^ps_ps [no weight => stored orthonormal sh2 is already the correct T_s].  Category-A.
"""
import sympy as sp

r, th = sp.symbols('r theta', positive=True)
S = sp.sin(th)
rho = sp.Function('rho')(r)
phi = sp.Function('phi')(r)
s = sp.Function('s')(r)                       # traceless shear DOF s(r); angular P2 handled separately
w0 = sp.exp(-2*phi)
a = rho**2 * sp.exp(s)                         # h_thth
bt = rho**2 * sp.exp(-s)                       # h_psps / sin^2

# geometric shear action density (op_derive2):  L_geo = w0 * ell , ell = -1/2 sin a' bt'/sqrt(ab)
ap = sp.diff(a, r); bp = sp.diff(bt, r)
ell = -sp.Rational(1, 2) * S * ap * bp / sp.sqrt(a*bt)
L_geo = w0 * ell

# Euler-Lagrange density  delta L_geo / delta s  (s, s' appear; also s'' after the d/dr)
s1 = sp.diff(s, r)
EL_s = sp.diff(L_geo, s) - sp.diff(sp.diff(L_geo, s1), r)

# ---- manual linearization about s=0 (replace s,s',s'' by independent symbols, keep O(s^1)) ----
S0, S1, S2 = sp.symbols('S0 S1 S2')
subs_sym = {sp.diff(s, r, 2): S2, sp.diff(s, r): S1, s: S0}
EL_poly = EL_s.subs(subs_sym)
const = sp.simplify(EL_poly.subs({S0: 0, S1: 0, S2: 0}))
c0 = sp.simplify(sp.diff(EL_poly, S0).subs({S0: 0, S1: 0, S2: 0}))
c1 = sp.simplify(sp.diff(EL_poly, S1).subs({S0: 0, S1: 0, S2: 0}))
c2 = sp.simplify(sp.diff(EL_poly, S2).subs({S0: 0, S1: 0, S2: 0}))
print("round (s-independent) part of delta L_geo/delta s [expect 0 for the traceless row]:", const)
s0 = sp.Function('s0')(r)                      # linear shear shape
s0p = sp.diff(s0, r); s0pp = sp.diff(s0, r, 2)
EL_lin = sp.simplify(c0*s0 + c1*s0p + c2*s0pp)
print("\ndelta L_geo/delta s (linearized) =")
sp.pprint(EL_lin)

# coded E_s^sans (n5d_shear.EAB_shear_row), linear in s:
rhop = sp.diff(rho, r); phip = sp.diff(phi, r)
E_s_coded = -w0 * (rho**2 * s0pp + (2*rho*rhop - 2*phip*rho**2) * s0p)
print("\ncoded E_s^sans (linear) =")
sp.pprint(sp.simplify(E_s_coded))

ratio = sp.simplify(EL_lin / (S * E_s_coded))
print("\n===== RATIO  (delta L_geo/delta s) / (sin(th) * E_s_coded) =====")
sp.pprint(ratio)
print()
print("If ratio == 1        => coded E_s IS the density (carries the rho^2/2 measure weight)")
print("   => the matter source must carry the SAME weight: correct source = (rho^2/2) * sh2 .")
print("If ratio == rho^2/2  => coded E_s is the bare mixed component E^th_th-E^ps_ps (no weight)")
print("   => stored sh2 (also mixed/orthonormal component) is ALREADY correct; NO rho^2 factor.")

# required multiplier on stored sh2 so the matter density matches the coded E_s normalization:
#   matter density delta L_m/delta s = (sqrt(h)/2)(T^th_th-T^ps_ps) = (rho^2 sin/2) * sh2
#   coded source sits at the E_s_coded level; correct multiplier = [(rho^2/2)/ratio]
mult = sp.simplify((rho**2/2) / ratio)
print("\n===== REQUIRED multiplier on stored sh2 (correct_source = mult * sh2) =====")
sp.pprint(mult)
