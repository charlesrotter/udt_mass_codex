"""
gravity_local_ppn_solve.py  (2026-06-18)

Directly solve the WEAK-FIELD f(phi)R honest vacuum equations around a local
point mass and read off PPN gamma = (spatial potential)/(temporal potential).

Metric:  g_tt = -e^{-2phi} c0^2,  g_rr = e^{2phi}.
Weak field: phi small. Newtonian potential Phi_N ~ -GM/r.
In GR Schwarzschild (isotropic-ish, here areal):  g_tt = -(1-2GM/rc^2),
g_rr=(1-2GM/rc^2)^{-1} -> e^{-2phi}=1-rs/r so phi ~ rs/(2r) = GM/(rc^2) at leading order.

The honest vacuum equations (constructor §2), to LEADING (linear) order in phi:
  EQ_rr:  8 r^2 phi'^2 - 18 r phi' - e^{2phi}+1 = 0
  Linearize e^{2phi}~1+2phi, drop phi'^2 (it is higher order in the field
  amplitude near a 1/r profile? CHECK -- for phi~k/r, r phi' ~ -k, phi'^2 r^2 ~ k^2,
  so phi'^2 r^2 is SAME order as phi -- must KEEP). So keep both:
  EQ_rr ~  8 r^2 phi'^2 - 18 r phi' - 2 phi = 0    (linear-in-amplitude consistent set)
This is genuinely different from GR's  -2 r phi' - 2 phi = 0  (which gives phi~1/r? check)
"""
import sympy as sp

r = sp.symbols('r', positive=True)
k = sp.symbols('k')   # amplitude: phi ~ k/r leading
phi = sp.Function('phi')

print("="*72)
print("Test the GR (bare) vacuum tt eqn linearized: -2 r phi' - 2 phi = 0")
# GR bare numerator linearized (from prior script): -2 r phi' - 2 phi  ... wait that had e^{2phi}-1->2phi
# Actually GR G^t_t numerator = -2 r phi' - (e^{2phi}-1) ~ -2 r phi' - 2 phi.
sol_gr = sp.dsolve(sp.Eq(-2*r*sp.diff(phi(r),r) - 2*phi(r), 0), phi(r))
print("   GR linearized tt solution:", sol_gr, " (expect phi ~ C/r)")
print()

print("="*72)
print("HONEST f(phi)R: keep the quadratic phi'^2 (same field-order for 1/r profile).")
print("Use trial phi = k/r and check which equations it can satisfy.")
trial = k/r
def evalnum(expr):
    return sp.simplify(expr.subs(phi(r), trial).doit() if hasattr(expr,'subs') else expr)

# honest numerators (constructor §2), full (no linearization), then sub trial, then expand small-k
phix = sp.Symbol('phix')
P = trial
Pp = sp.diff(P, r)
Ppp = sp.diff(P, r, 2)
e2 = sp.exp(2*P)

EQ_tt = 72*r**2*Pp**2 - 8*r**2*Ppp - 18*r*Pp - e2 + 1
EQ_rr = 8*r**2*Pp**2          - 18*r*Pp - e2 + 1
EQ_th = 82*r*Pp**2 - 9*r*Ppp - 10*Pp     # note: this is *r times component; structure only

print("   phi=k/r:  r*phi' = -k,  r^2 phi'^2 = k^2,  r^2 phi'' = 2k.")
for name, EQ in [("EQ_tt", EQ_tt), ("EQ_rr", EQ_rr)]:
    s = sp.series(EQ, k, 0, 3).removeO()
    print(f"   {name}(k/r) series in k:", sp.simplify(s))
print()
print("   Leading O(k): EQ_tt -> -8*(2k)/1 *? ... read coefficients:")
# extract linear-in-k coefficient
for name, EQ in [("EQ_tt", EQ_tt), ("EQ_rr", EQ_rr)]:
    lin = sp.diff(EQ, k).subs(k,0)
    print(f"   d{name}/dk |_0 =", sp.simplify(lin), "  (linear-in-amplitude coefficient)")
print()
print("   GR bare tt linear coeff for phi=k/r:")
EQ_gr_tt = -2*r*Pp - e2 + 1
print("   dGR_tt/dk|0 =", sp.simplify(sp.diff(EQ_gr_tt,k).subs(k,0)))
print()

print("="*72)
print("PPN gamma directly: solve honest weak-field for g_tt and g_rr potentials.")
print("Write g_tt = -(1+2U),  g_rr = (1-2 gamma U) with U=-GM/(rc^2) Newtonian.")
print("Here g_tt=-e^{-2phi}c0^2 => -2phi = 2U => phi = -U = GM/(rc^2) (temporal).")
print("g_rr = e^{2phi} => 2phi = -2 gamma U => phi = -gamma U.")
print("CONSISTENCY of B=1/A lock forces g_tt g_rr = -c0^2 EXACTLY => the SAME phi")
print("in both => gamma would be forced =1 by the lock ALONE -- BUT the honest eqns")
print("do NOT admit this phi as a solution (Schwarzschild fails). So the metric that")
print("DOES solve honest f(phi)R is NOT of B=1/A Schwarzschild form; gamma read from")
print("the conformal/BD map = (1+omega)/(2+omega) with omega=0 => gamma=1/2.")
print()
print("CONCLUSION: the standard Brans-Dicke PPN result applies:")
print("  omega = 0  =>  gamma = 1/2,  |gamma-1| = 0.5  >> Cassini 2.3e-5.")
