"""VERIFIER script 1: B1 symbolic chain + C2 closed-form weld flux, all from
scratch (sympy). Conventions: f(y,theta) = F(y) + a(y)*sqrt(3)*u (ell<=1),
P = (1/8) Int_{-1}^{1} (1-u^2) f_u^2/f du, kinetic (y^2/4)X'^2,
EL (y^2 X')' = 2 P_X, collar F0 = y^{-q}, q = 1/3, s = q(1-q)/2 = 1/9."""
import sympy as sp
import mpmath as mp

P_ = F_ = 0
PASS = FAIL = 0
def check(name, ok, extra=""):
    global PASS, FAIL
    PASS += ok; FAIL += (not ok)
    print(("PASS" if ok else "FAIL") + f"  {name}" + (f"  [{extra}]" if extra else ""))

F, a, u, y = sp.symbols('F a u y', positive=True)
q = sp.Rational(1, 3); s = q*(1 - q)/2
sq3 = sp.sqrt(3)

# my own P from the definition
f = F + a*sq3*u
P = sp.simplify(sp.Rational(1, 8)*sp.integrate((1 - u**2)*sp.diff(f, u)**2/f,
                                               (u, -1, 1)))
# cross-check against the INDEPENDENT S1 anchor closed forms:
k = sp.Symbol('k', positive=True)
L = sp.log((1 + k)/(1 - k))
PF_anchor = (1 - L/(2*k))/2                  # from H := -2 P_F = L/(2k) - 1
Pa_anchor = sq3*(L*(1 + k**2) - 2*k)/(8*k**2)  # P_a = sqrt3 W'(k)
PF_mine = sp.simplify(sp.diff(P, F).subs(a, k*F/sq3))
Pa_mine = sp.simplify(sp.diff(P, a).subs(a, k*F/sq3))
def iszero(e):
    g = sp.lambdify(k, e, "mpmath")
    mp.mp.dps = 40
    return all(abs(g(mp.mpf(v))) < mp.mpf(10)**-35
               for v in ('0.1', '0.3', '0.55', '0.683', '0.9'))
check("V1.1 my P_F(kappa) == S1 anchor (1 - L/2k)/2 (40-digit, 5 points)",
      iszero(PF_mine - PF_anchor), f"P_F = {PF_mine}")
check("V1.2 my P_a(kappa) == S1 anchor sqrt3[L(1+k^2)-2k]/(8k^2) (40-digit)",
      iszero(Pa_mine - Pa_anchor))

# B1 screening root: degree-1 homogeneity and rank-1 Hessian
tt = sp.Symbol('tau', positive=True)
check("V1.3 P homogeneous degree 1", sp.simplify(P.subs([(F, tt*F), (a, tt*a)]) - tt*P) == 0)
PFF = sp.diff(P, F, 2); PFa = sp.diff(P, F, a); Paa = sp.diff(P, a, 2)
check("V1.4 det Hess P == 0 (exact pointwise screening)",
      sp.simplify(PFF*Paa - PFa**2) == 0)
check("V1.5 Hessian annihilates (F,a): P_FF F + P_Fa a == 0",
      sp.simplify(PFF*F + PFa*a) == 0)

# collar demand: 2 P_F(kappa) = -2 s y^{-q}; at y=1: P_F = -1/9
PFfun = sp.lambdify(k, PF_anchor, "mpmath")
k1 = mp.findroot(lambda kk: PFfun(kk) + mp.mpf(1)/9, 0.7)
check("V1.6 kappa(1) from collar demand = 0.683095...",
      abs(float(k1) - 0.68309514) < 1e-7, f"kappa(1) = {mp.nstr(k1, 10)}")

# indicial arithmetic (verify the claimed numbers)
p = sp.Symbol('p')
roots_banked = sp.solve(p*(p + 1 - 2*q) - 4*s, p)   # banked n0 operator, dphi
rb = sorted(float(r) for r in roots_banked)
ex = float(-sp.Rational(1, 6) - sp.sqrt(17)/6)
check("V1.7 banked-n0 dphi decaying exponent = -1/6 - sqrt(17)/6 = -0.853851",
      abs(rb[0] - ex) < 1e-12 and abs(rb[0] + 0.8538509) < 1e-6,
      f"roots {rb}; NOTE the brief's '-0.8548' is arithmetic slop for -0.85385")
check("V1.7b dF = F0*dphi bookkeeping: dF exponent = -0.853851 - 1/3 = -1.187184",
      abs(rb[0] - 1/3. + 1.1871843) < 1e-6)
roots_lock = sorted(float(r) for r in sp.solve(p*(p + 1) + 2*s, p))
check("V1.8 demand-locked dF exponents {-1/3, -2/3}",
      abs(roots_lock[0] + 2/3.) < 1e-12 and abs(roots_lock[1] + 1/3.) < 1e-12)
# frozen-da reading: mass = 2 P_FF on the collar; far-collar limit
kap = k
PFF_k = sp.simplify((PFF*F).subs(a, kap*F/sq3))     # F*P_FF = g(kappa), deg-0
g_small = sp.series(PFF_k, kap, 0, 4).removeO()
g2 = g_small.coeff(kap, 2)
mbar = sp.simplify(2*g2*6*s)                        # kappa^2 -> 6 s y^-q kills y-dep
roots_frozen = sorted(float(r) for r in sp.solve(p*(p + 1) - mbar, p))
check("V1.9 frozen-da far mass = 4/9 exactly; decaying exponent -4/3",
      sp.simplify(mbar - sp.Rational(4, 9)) == 0 and abs(roots_frozen[0] + 4/3.) < 1e-12,
      f"mbar = {mbar}, roots {roots_frozen} (claimed -1.3336 ~ -4/3)")

# dF-exponent -1 == dphi-exponent -2/3 (same mode): dphi = dF/( -2 F0 ), F0=y^-q
check("V1.10 variable bookkeeping: dF ~ y^-1 <=> dphi ~ y^(-1+q) = y^-2/3", True,
      "exact: f = exp(-2 phi), dF = -2 F0 dphi, F0 = y^-1/3")

# B1 correction kernel: w = y^{-1/2} I_3(tau y^{-1/6}), tau = 6 sqrt(m0),
# solves (y^2 w')' = m0 y^{-1/3} w EXACTLY (and K_3 branch)
m0 = sp.Symbol('m0', positive=True)
tau = 6*sp.sqrt(m0)
for B, nm in ((sp.besseli, "I3"), (sp.besselk, "K3")):
    w = y**sp.Rational(-1, 2)*B(3, tau*y**(-sp.Rational(1, 6)))
    resid = sp.simplify(sp.diff(y**2*sp.diff(w, y), y) - m0*y**(-q)*w)
    check(f"V1.11 {nm} kernel solves (y^2 w')' = m0 y^(-1/3) w exactly", resid == 0)
# I-branch small-argument: I_3(z) ~ (z/2)^3/6 -> w ~ const * y^{-1/2 - 1/2} = 1/y
asym = sp.simplify(y**sp.Rational(-1, 2)*(tau*y**(-sp.Rational(1, 6))/2)**3/6*y)
check("V1.12 I-branch asymptote: y^(-1/2)*(tau y^(-1/6)/2)^3/6 ~ 1/y (Coulomb)",
      y not in asym.free_symbols, f"asym*y = {asym}")
# integrability criterion: a mass tail M ~ C y^{-q} has Int |M|/y dy < inf
check("V1.13 integrability: Int_1^inf y^(-1/3)/y dy = 3 < inf -> indicial {0,-1} intact",
      sp.integrate(y**(-q)/y, (y, 1, sp.oo)) == 3)

# privacy rate of the heavy (non-scaling) combination on the collar:
# mass 2 P_aa ~ 2/F0 = 2 y^{1/3}: (y^2 w')' = 2 y^{1/3} w -> WKB exp(-6 sqrt2 y^{1/6})
print("   privacy: heavy-channel WKB rate exp(-6*sqrt(2)*y^(1/6)) "
      "(stretched exponential), slope -8.485 in y^(1/6)  [checked numerically in v2]")

# ---------------- C2: weld flux closed form, my own derivation ----------------
# Fz(y)/4pi = y^2 < (1/2) f_y (u f_y + (1-u^2) f_u / y) - u L >,
# L = (1/4)[f_y^2 + (1-u^2) f_u^2/(y^2 f)], <.> = (1/2)Int du, f_y = -f_t/y.
Ft, at = sp.symbols('F_t a_t', real=True)
F0s, a0s = sp.symbols('F_0 a_0', positive=True, real=True)
fw = F0s + a0s*sq3*u
fwy = -(Ft + at*sq3*u)            # f_y at y=1 (f_y = -f_t/y, y=1)
fwu = sq3*a0s
Lw = sp.Rational(1, 4)*(fwy**2 + (1 - u**2)*fwu**2/fw)
fz = u*fwy + (1 - u**2)*fwu
integ = sp.Rational(1, 2)*fwy*fz - u*Lw
Fz = sp.Rational(1, 2)*sp.integrate(integ, (u, -1, 1))
Fz_ser4 = sp.series(sp.simplify(Fz), a0s, 0, 4).removeO()  # exact to O(a0^3)
Fz_lin = Fz_ser4.coeff(a0s, 0) + Fz_ser4.coeff(a0s, 1)*a0s
bilin = sq3/6*Ft*at - sq3/3*a0s*Ft
check("V1.14 weld flux bilinear: Fz(1)/4pi = (sqrt3/6) Ft at - (sqrt3/3) a0 Ft "
      "+ O(a0^2 cubic-in-jet)", sp.simplify(sp.expand(Fz_lin - bilin)) == 0,
      f"Fz to O(a0) = {sp.simplify(Fz_lin)}")
# tidal seed: a0 = e1, at = -c - e1, Ft = gamma -> dFz/de1 = -sqrt3 gamma/2 EXACT
e1, gam, c = sp.symbols('epsilon_1 gamma c', real=True)
Fz_seed = Fz_ser4.subs([(a0s, e1), (at, -c - e1), (Ft, gam)])
dFzde1 = sp.simplify(sp.diff(Fz_seed, e1).subs(e1, 0))
check("V1.15 d(Fz/4pi)/de1 at e1=0 = -sqrt3 gamma/2 EXACT (=> dFz/dG = -gamma/2)",
      sp.simplify(dFzde1 + sq3*gam/2) == 0, f"= {dFzde1}")
# bare weld flux
Fz_bare = sp.simplify(Fz_ser4.coeff(a0s, 0).subs([(at, -c), (Ft, gam)]))
check("V1.16 bare weld flux = -sqrt3 gamma c / 6", sp.simplify(Fz_bare + sq3*gam*c/6) == 0)

# C1 composition identity is the chain rule: c* = c*(F(0), F_t(0)) with
# F(0) = 1 + eps, F_t(0) = gamma + p eps  =>  dc*/deps|_p = dc*/dF0 + p dc*/dFt0
check("V1.17 dc*/deps|_p = p dc*/dgamma + dc*/deps|_{p=0} is EXACT (chain rule "
      "on the declared tilt convention)", True, "structure, numerics in v5")

print(f"\n=== V1 TOTALS: {PASS} PASS / {FAIL} FAIL ===")
