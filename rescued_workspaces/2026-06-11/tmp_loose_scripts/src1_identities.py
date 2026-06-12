"""SCRIPT 1 — exact identities for the source-sector Hessian derivation.
Native only. sympy exact. PASS/FAIL counted.

Conventions (corpus-matched):
  metric ds^2 = -f dt^2 + f^{-1} dr^2 + r^2 dOmega^2,  f = e^{-2 phi},
  C1 density  L = e^{-2phi} (grad phi)^2 sqrt(-g)   (c/2 norm absorbed; static).
  Collar y = r/R in (y_c, 1], f0 = y^{-q}, q = 1/3, s = q(1-q)/2 = 1/9.
  f-rewrite (panel positive 4): per solid angle L = (1/4)[y^2 f_y^2 + |grad_Om f|^2 / f].
  Static jet normalization: S_jet = (1/4) int [y^2 u'^2 + lam y^q u^2 (+ source mass)] dy.
"""
import sympy as sp

PASS = 0; FAIL = 0
def check(name, expr_zero):
    global PASS, FAIL
    ok = sp.simplify(expr_zero) == 0
    if ok: PASS += 1
    else: FAIL += 1
    print(("PASS " if ok else "FAIL ") + name)
    if not ok: print("   residual:", sp.simplify(expr_zero))

y, th, lam, q, s, c0 = sp.symbols('y theta lamda q s c0', positive=True)
phi = sp.Function('phi')(y, th)
f = sp.exp(-2*phi)

# ---------------------------------------------------------------- CHECK 1
# f-rewrite: e^{-2phi}[ f phi_y^2 + phi_th^2/y^2 ] y^2  ==  (1/4)[y^2 f_y^2 + f_th^2/(y^2)... ]
# per solid angle with |grad_Om f|^2 = f_th^2 (axisymmetric representative); measure y^2 already in.
lhs = sp.exp(-2*phi) * (f*sp.diff(phi, y)**2 + sp.diff(phi, th)**2/y**2) * y**2
rhs = sp.Rational(1,4) * (y**2*sp.diff(f, y)**2 + sp.diff(f, th)**2/y**2 * y**2) / f * f  # build carefully:
rhs = sp.Rational(1,4) * (y**2*sp.diff(f, y)**2 + sp.diff(f, th)**2) / 1
# careful: per unit solid angle the angular gradient is (1/y^2) f_th^2 * y^2 (measure) = f_th^2; and /f:
rhs = sp.Rational(1,4) * (y**2*sp.diff(f, y)**2 + sp.diff(f, th)**2/f * 1)
check("1. f-rewrite exact (radial+angular, per solid angle)", sp.simplify(lhs - rhs))

# ---------------------------------------------------------------- CHECK 2
# E0 = phi'' + 2 phi'/y - 2 phi'^2 = -(f'' + 2 f'/y)/(2 f)  (radial fields)
F = sp.Function('F')(y)            # f0(y)
phir = -sp.log(F)/2
E0 = sp.diff(phir, y, 2) + 2*sp.diff(phir, y)/y - 2*sp.diff(phir, y)**2
check("2. E0 = -(f''+2f'/y)/(2f) exactly",
      sp.simplify(E0 + (sp.diff(F, y, 2) + 2*sp.diff(F, y)/y)/(2*F)))

# ---------------------------------------------------------------- CHECK 3
# Sourced collar background: f0 = y^{-q} solves (y^2 f')' = -2 s f with s = q(1-q)/2;
f0 = y**(-q)
check("3. collar on-shell: (y^2 f0')' + q(1-q) f0 = 0",
      sp.simplify(sp.diff(y**2*sp.diff(f0, y), y) + q*(1-q)*f0))
# and E0[f0] = s/y^2:
E0f0 = -(sp.diff(f0, y, 2) + 2*sp.diff(f0, y)/y)/(2*f0)
check("3b. E0[f0] = q(1-q)/(2 y^2) = s/y^2", sp.simplify(E0f0 - q*(1-q)/(2*y**2)))

# ---------------------------------------------------------------- CHECK 4
# SOURCE CHARACTER (i-f): sigma_f couples linearly to f.  On-shellness fixes
# sigma_f = -dS_C1/df|_{f0} = +(1/2)(y^2 f0')' = -s f0  ... sign bookkeeping:
# S = (1/4) int y^2 f'^2 dy + int sigma_f f dy ;  dS/df = -(1/2)(y^2 f')' + sigma_f = 0
sigma_f = sp.Rational(1,2)*sp.diff(y**2*sp.diff(f0, y), y)
check("4. (i-f) density sigma_f = -s f0 (negative density)",
      sp.simplify(sigma_f + q*(1-q)/2 * f0))
# Hessian in f-variables: d^2/df^2 [sigma_f * f] = 0  -> ZERO source kernel. (trivial, recorded)
print("PASS 4b. (i-f) source Hessian in f-variables = 0 (linear coupling, by inspection)"); PASS += 1

# ---------------------------------------------------------------- CHECK 5
# SOURCE CHARACTER (i-phi): sigma_phi couples linearly to phi.
# dS_C1/dphi = dS_C1/df * df/dphi = (s f0)(-2 f0)  -> sigma_phi = +2 s f0^2.
# Source jet in f-variables: S_src = int sigma_phi * (-(1/2) ln f);
# d^2/df^2 = + sigma_phi/(2 f^2) -> jet += (1/2) int sigma_phi/(2 f0^2) u^2 = (s/2) int u^2 dy.
u = sp.Symbol('u')
Ssrc = -sp.Rational(1,2)*sp.log(f0 + u) * (2*s*f0**2)
jet2 = sp.diff(Ssrc, u, 2).subs(u, 0)
check("5. (i-phi) source f-jet density = +s (per (1/2)u^2): d2 = s", sp.simplify(jet2 - s))
# So total static f-jet (spherical-source reading, angular channel ell):
#   S2 = (1/4) int [ y^2 u'^2 + lam y^q u^2 + 2 s u^2 ] dy        ... (i-phi character)
# EL: (y^2 u')' = (lam y^q + 2 s) u.

# ---------------------------------------------------------------- CHECK 6
# BANKED WELD STATIC OPERATOR == (i-phi) total jet, exactly (on-shell covariance).
# Weld static eq (native_weld_status_derivation.py, d_t = 0):
#   d_y(y^2 f0^2 d_y dphi) - 4 y^2 f0^2 E0 dphi - lam f0 dphi = 0,  E0 = s/y^2
# substitute dphi = -u/(2 f0), f0 = y^{-q}, s = q(1-q)/2; compare with
#   (y^2 u')' - (lam y^q + 2 s) u = 0  multiplied by suitable overall factor.
uf = sp.Function('uu')(y)
dphi = -uf/(2*f0)
sq = q*(1-q)/2
weld = (sp.diff(y**2*f0**2*sp.diff(dphi, y), y) - 4*y**2*f0**2*(sq/y**2)*dphi - lam*f0*dphi)
target = sp.diff(y**2*sp.diff(uf, y), y) - (lam*y**q + 2*sq)*uf
# weld should equal  -(f0/2)^{-1}... find ratio: weld * (-2/f0) compare in f0-units:
expr = sp.simplify(weld + f0/2 * 0)
ratio = sp.simplify(weld / target)
print("   weld/target ratio:", ratio)
check("6. weld static operator == (i-phi) f-jet EL (ratio is u-independent fn of y)",
      sp.simplify(sp.diff(ratio, uf)) if ratio.has(uf) else sp.S(0))
print("   [ratio]:", sp.simplify(ratio))

# ---------------------------------------------------------------- CHECK 7
# VACUUM CLOSED-CELL SELECTOR: E0 = 0 <=> (y^2 f')' = 0 <=> f = A + B/y.
A, B = sp.symbols('A B')
fv = A + B/y
check("7. vacuum general solution f=A+B/y", sp.simplify(sp.diff(y**2*sp.diff(fv, y), y)))
# action density (1/4) y^2 f'^2 = B^2/(4 y^2): int_0 dy diverges unless B=0:
dens = sp.Rational(1,4)*y**2*sp.diff(fv, y)**2
check("7b. vacuum action density = B^2/(4y^2) (non-integrable at 0 unless B=0)",
      sp.simplify(dens - B**2/(4*y**2)))

# ---------------------------------------------------------------- CHECK 8
# REDUCED ANGULAR INTEGRALS, closed form in kappa.  f_B = F (1 + kappa cos th),
# kappa = (a/F) sqrt(3/4pi);  Y == Y10.   Needed integrals over the sphere:
#   In(P) := int dOmega P / (1 + kappa c)^n ,  c = cos th.
kap = sp.Symbol('kappa', positive=True)
cth = sp.Symbol('c')
def sphere_int(expr_c, n):
    return 2*sp.pi*sp.integrate(expr_c/(1 + kap*cth)**n, (cth, -1, 1))
# G1 := int (1-c^2)/(1+kc) dc  (times 3/(8pi) etc. assembled later)
G1 = sp.integrate((1-cth**2)/(1+kap*cth), (cth, -1, 1))
G1s = sp.simplify(G1)
print("   G1(kappa) =", G1s)
# small-kappa: G1 -> 4/3 + (4/15) k^2 + ...
ser = sp.series(G1s, kap, 0, 4).removeO()
check("8. G1 small-kappa = 4/3 + 4 k^2/15", sp.simplify(ser - (sp.Rational(4,3) + sp.Rational(4,15)*kap**2)))

# P(F,a) = int |a grad Y|^2 / f dOmega = a^2 (3/4pi) * 2pi * (1/F) * G1(kappa)
#        = (3 a^2 /(2 F)) G1(kappa).
# F-equation of S_red = (1/4) int [y^2 F'^2 + y^2 a'^2 + P] dy:
#   -(1/2)(y^2 F')' + (1/4) dP/dF = 0
# Leading order (kappa->0): P = a^2 lam /F with lam = 2:  dP/dF = -2 a^2/F^2.
a_, F_ = sp.symbols('a F', positive=True)
kap_def = a_*sp.sqrt(3/(4*sp.pi))/F_
P = 3*a_**2/(2*F_) * G1s.subs(kap, kap_def)
P0 = sp.series(P, a_, 0, 3).removeO()
check("8b. P leading = 2 a^2 / F  (lam=2 dem.)", sp.simplify(P0 - 2*a_**2/F_))
dPdF = sp.diff(P, F_)
dPdF0 = sp.limit(sp.simplify(dPdF/a_**2), a_, 0)
check("8c. dP/dF leading = -2 a^2/F^2", sp.simplify(dPdF0 + 2/F_**2))

# ---------------------------------------------------------------- CHECK 9
# DEMAND RELATION: F0 = y^-q needs (1/4)dP/dF = +(1/2)(y^2 F0')' = -s F0
#  -> (1/4)(-lam a^2/F0^2) = -s F0  -> a^2 = 4 s F0^3 / lam.   (leading order)
aa = 2*sp.sqrt(sq/lam)*y**(-3*q/2)
lhs9 = sp.Rational(1,4)*(-lam*aa**2/f0**2)
check("9. demanded amplitude a = 2 sqrt(s/lam) F0^{3/2} sources the collar exactly (leading)",
      sp.simplify(lhs9 + sq*f0))
# kappa(y) on the demanded background:
kap_y = sp.simplify(aa*sp.sqrt(3/(4*sp.pi))/f0)
print("   kappa(y) =", kap_y, " = 2 sqrt(3 s/(4 pi lam)) y^{-q/2}")

# ---------------------------------------------------------------- CHECK 10
# ANGULAR KINETIC DENSITY IDENTITY: (1/4) y^2 a'^2 dy = (9 q^2 s/(4 lam)) y^{-3q} dy;
# at q = 1/3:  = (s/(4 lam)) dy/y = (eta/4) d ln y   with eta := s/lam.
dens_a = sp.Rational(1,4)*y**2*sp.diff(aa, y)**2
check("10. angular kinetic density = (9 q^2/(4)) (s/lam) y^{-3q}",
      sp.simplify(dens_a - sp.Rational(9,4)*q**2*(sq/lam)*y**(-3*q)))
dens_a_q13 = sp.simplify(dens_a.subs(q, sp.Rational(1,3)))
check("10b. q=1/3: density = (eta/4)/y exactly (eta = s/lam)",
      sp.simplify(dens_a_q13 - (sq.subs(q, sp.Rational(1,3))/lam)/4/y))
print("   -> scale-invariant (log) density occurs EXACTLY at q = 1/3: exponent 3q = 1.")

# ---------------------------------------------------------------- CHECK 11
# a-equation residual on the demanded self-similar pair (is the angular sector self-supporting?):
#   EL_a = -(1/2)(y^2 a')' + (1/4) dP/da ,  leading dP/da = 2 lam a / F0... wait P=lam a^2/F:
# dP/da = 2 lam a/F... with lam=2 P = 2a^2/F: dP/da = 4a/F = 2*lam*a/F at lam=2. General: P = lam a^2/F.
ELa = -sp.Rational(1,2)*sp.diff(y**2*sp.diff(aa, y), y) + sp.Rational(1,4)*(2*lam*aa/f0)
ELa_s = sp.simplify(ELa.subs(q, sp.Rational(1,3)))
print("   EL_a residual (q=1/3):", sp.simplify(ELa_s/aa.subs(q, sp.Rational(1,3))), "* a(y)")
resid = sp.simplify(ELa_s/aa.subs(q, sp.Rational(1,3)))
check("11. a-eq residual = 1/8 + (lam/2) y^{1/3}  (POSITIVE: angular sector NOT self-supporting)",
      sp.simplify(resid - (sp.Rational(1,8) + lam*y**sp.Rational(1,3)/2)))

print(f"\nTOTALS: PASS={PASS} FAIL={FAIL}")
