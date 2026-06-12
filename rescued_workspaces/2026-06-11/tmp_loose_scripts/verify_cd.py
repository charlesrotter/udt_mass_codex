"""Attack C (algebraic -> f-equation, sign anchoring) and D (bound numerics,
k-classification), all independent of the target scripts."""
import sympy as sp
import mpmath as mp

r = sp.symbols("r", positive=True)
K, a, lamS, c, kS = sp.symbols("K a lam c k", positive=True)
f = sp.Function("f", positive=True)(r)
rho = sp.Function("rho", positive=True)(r)
fp = sp.diff(f, r)

print("== C: algebraic equation -> f-equation ==")
# d/dr [rho^4 f'^2 - 4K] = 2 rho^3 f' * [2 rho' f' + rho f''] = (2 rho f') * (rho^2 f')'/... check:
expr = sp.diff(rho**4*fp**2, r)
factored = 2*rho**2*fp*sp.diff(rho**2*fp, r)
print("C1 d/dr[rho^4 f'^2] == 2 (rho^2 f') (rho^2 f')':",
      sp.simplify(expr - factored) == 0)
# so on rho^4 f'^2 = 4K>0, f' != 0 everywhere => (rho^2 f')' = 0. Constant-sign of f'
# follows from continuity of f' and f' != 0. Then rho^2 f' = const = -a, a^2 = 4K.

print()
print("== C2: sign anchoring ==")
# the f-equation cannot see the flux piece: dL_flux/df = dL_flux/df' = 0
Lflux = K/rho**2
print("C2a flux piece blind to f (so banked rho=r f-equations CANNOT anchor its sign):",
      sp.simplify(Lflux.diff(f)) == 0 and sp.simplify(Lflux.diff(fp)) == 0)
# alternative sign: L = (1/4)rho^2 f'^2 - K/rho^2 -> rho-eq (1/2)rho f'^2 + 2K/rho^3 = 0
alt = sp.Rational(1,2)*rho*fp**2 + 2*K/rho**3
print("C2b alternative sign rho-equation is sum of positives (no solution): each term >= / > 0:",
      "yes (rho>0, K>0)")
# RN-like banked diagnostic: f = 1 + a/r + q^2/r^2 with rho=r needs (r^2 f')' = 2q^2/r^2 != 0
qS = sp.symbols("q", positive=True)
fRN = 1 + a/r + qS**2/r**2
print("C2c (r^2 fRN')' =", sp.simplify(sp.diff(r**2*sp.diff(fRN, r), r)),
      " (NOT 0: the native flux theory does NOT produce an RN q^2/r^2 term in f)")
# extremal RN comparison: f = (1 - Q/r)^2 has a = -2Q i.e. |a| = 2|Q|
Q = sp.symbols("Q", positive=True)
fext = (1 - Q/r)**2
print("C2d extremal RN f=(1-Q/r)^2 expanded:", sp.expand(fext), " tail coeff a=-2Q -> |a| = 2|Q|")
print("    but fext has a q^2/r^2 term, so fext does NOT satisfy (r^2 f')'=0:",
      sp.simplify(sp.diff(r**2*sp.diff(fext, r), r)))

print()
print("== D: re-derive + numerically test the L1 bound ==")
# Bound re-derivation (analytic, summarized):
# int_R^inf |lam/r^2 + f'/r| dr <= lam/R + [int r^2 f'^2]^{1/2} [int dr/r^4]^{1/2}
#   = lam/R + sqrt(4 S_tail) * sqrt(1/(3R^3)) = lam/R + 2 sqrt(S_tail)/sqrt(3 R^3).
S_check = sp.integrate(1/r**4, (r, sp.Symbol("R", positive=True), sp.oo))
print("D0 int_R^inf dr/r^4 = 1/(3R^3):", sp.simplify(S_check - 1/(3*sp.Symbol("R", positive=True)**3)) == 0)

mp.mp.dps = 30
def test_profile(name, ffun, ffp, R0, lam_v):
    LHS = mp.quad(lambda rr: abs(lam_v/rr**2 + ffp(rr)/rr), [R0, mp.inf])
    Stail = mp.mpf(1)/4 * mp.quad(lambda rr: rr**2*ffp(rr)**2, [R0, mp.inf])
    RHS = lam_v/R0 + 2*mp.sqrt(Stail)/mp.sqrt(3*R0**3)
    print(f"  {name}: LHS=int|V|dr* = {mp.nstr(LHS,8)}  RHS bound = {mp.nstr(RHS,8)}  "
          f"S_tail={mp.nstr(Stail,8)}  bound holds: {LHS <= RHS}")
    # also Cauchy-Schwarz convergence bound |f(b)-f(a)|^2 <= 4 S_tail(a)/a
    aa = R0 + 1
    St_a = mp.mpf(1)/4 * mp.quad(lambda rr: rr**2*ffp(rr)**2, [aa, mp.inf])
    ok = True
    for bb in [aa+0.5, aa+2, aa+10, aa+100, aa+10000]:
        dfab = abs(ffun(bb) - ffun(aa))
        ok = ok and (dfab**2 <= 4*St_a/aa + mp.mpf("1e-25"))
    print(f"      C-S bound |f(b)-f(a)|^2 <= 4 S_tail(a)/a for several b: {ok}")

test_profile("f = 1 + 1/r  (lam=2, R=1)", lambda rr: 1+1/rr, lambda rr: -1/rr**2, 1, 2)
test_profile("f = 2 + 3/r  (lam=2, R=1)", lambda rr: 2+3/rr, lambda rr: -3/rr**2, 1, 2)
test_profile("f = 1 + sin(r)/r^2 (oscillatory, lam=6, R=2)",
             lambda rr: 1+mp.sin(rr)/rr**2,
             lambda rr: mp.cos(rr)/rr**2 - 2*mp.sin(rr)/rr**3, 2, 6)
# exact check of script's worked example value 5/6
val = sp.integrate(sp.Abs(2/r**2 - 3/r**3), (r, 1, sp.oo))
print("  exact worked example f=2+3/r, lam=2: int|V|dr* =", sp.nsimplify(val), "(script claims 5/6)")

print()
print("== D2: k-classification, independent ==")
V = f*(lamS/r**2 + fp/r)
Vk = sp.simplify(V.subs(f, c*r**kS).doit())
print("V(f=c r^k) =", sp.expand(Vk))
for kv, expect in [(sp.Rational(-3,2),0),(0,0),(sp.Rational(1,2),0),(sp.Rational(9,10),0),
                   (1,c**2),(sp.Rational(11,10),sp.oo),(2,sp.oo),(5,sp.oo)]:
    L = sp.limit(Vk.subs(kS, kv), r, sp.oo)
    print(f"  k={kv}: V(inf)={L}  expected {expect}  ok={sp.simplify(L-expect)==0 if expect is not sp.oo else L==sp.oo}")
# endpoint strength g(k) for k>1, independent derivation:
s = sp.symbols("s", positive=True)
kk = 1 + s
dist = sp.integrate(1/(c*r**kk), (r, sp.Symbol("rr", positive=True), sp.oo))  # x_inf - x(r)
dist = sp.simplify(dist)
print("x_inf - x(r) =", dist)
g_lim = sp.limit(sp.simplify(Vk.subs(kS, kk)) * dist.subs(sp.Symbol("rr", positive=True), r)**2, r, sp.oo)
print("V*(x_inf-x)^2 ->", sp.simplify(g_lim), " vs k/(k-1)^2 =", sp.simplify(kk/(kk-1)**2),
      " equal:", sp.simplify(g_lim - kk/(kk-1)**2) == 0)
# limit-point window
sol = sp.solve(3*sp.Symbol("k")**2 - 10*sp.Symbol("k") + 3, sp.Symbol("k"))
print("g(k) >= 3/4 boundary roots:", sol)
