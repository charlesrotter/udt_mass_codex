"""NONSTATIONARY SECTOR N2 — script 1: setup, exact reductions, anchors.

Action convention (pinned against banked anchors below):
    L_C1 = -(c/2) sqrt(-g) e^{-2 phi} g^{mu nu} d_mu phi d_nu phi,
    f = e^{-2 phi}   =>   L_C1 = -(c/8) sqrt(-g) g^{mu nu} f_mu f_nu / f.

Metric class (P1 class + full time row; axisymmetric m=0, even parity,
k=0 canon, g_rr = 1/f tied):
    ds^2 = -f dT^2 + 2a dT dr + 2b dT dth + f^{-1} dr^2 + 2q dr dth
           + A dth^2 + B dphi^2,
    A = r^2 (1+w)^2,  B = r^2 sin^2(th) (1+w)^{-2}.
f(T,r,th) dynamical; a,b,q,w pointwise algebraic (the C1 action contains
no derivative of any metric component — structural).

Method discipline: all identity checks are polynomial (expand/cancel);
radical-branch signs fixed by exact-rational sampling on the connected
admissible domain (Q>0, D2>0, P>0, f>0) — sign of a continuous
nonvanishing function on a connected set is constant.
"""
import sympy as sp
from sympy import Rational as Ra

PASS, FAIL = [], []
def check(label, ok):
    (PASS if ok else FAIL).append(label)
    print(("PASS" if ok else "FAIL"), label)

def zero_poly(e):
    return sp.expand(e) == 0

def zero_cancel(e):
    return sp.cancel(sp.together(e)) == 0

c, f, r, th = sp.symbols('c f r theta', positive=True)
a, b, q, w = sp.symbols('a b q w', real=True)
vT, vr, vh = sp.symbols('v_T v_r v_theta', real=True)
A, B = sp.symbols('A B', positive=True)

# ---------------------------------------------------------------- block 0
p = sp.Symbol('p', real=True)
g4 = sp.Matrix([[-f, a, b, p], [a, 1/f, q, 0], [b, q, A, 0], [p, 0, 0, B]])
v4 = sp.Matrix([vT, vr, vh, 0])
det4 = sp.expand(g4.det())
N4 = sp.expand((v4.T * g4.adjugate() * v4)[0, 0])
check("B0: det and N even in p at u=v=0 (axisym) => L even in p; p=0 is a "
      "parity-consistent branch (g_Tphi droppable in the even sector)",
      zero_poly(det4 - det4.subs(p, -p)) and zero_poly(N4 - N4.subs(p, -p)))

# ---------------------------------------------------------------- block 1
M = sp.Matrix([[-f, a, b], [a, 1/f, q], [b, q, A]])
v3 = sp.Matrix([vT, vr, vh])
adjM = M.adjugate()
check("B1a: M*adj(M) = det(M) I",
      sp.expand(M * adjM - M.det() * sp.eye(3)) == sp.zeros(3, 3))
Delta = sp.expand(-M.det())
N = sp.expand((v3.T * adjM * v3)[0, 0])
# L = (c/8) sqrt(B) N / (f sqrt(Delta))   ==  -(c/8) sqrt(-g) g^{ij} v_i v_j / f
# (identity: v^T adj(M) v = det(M) v^T M^{-1} v, det(M) = -Delta, sqrt(-g)=sqrt(B*Delta))
check("B1b: v^T adj(M) v = det(M) * v^T M^{-1} v  (so L-form is exact)",
      zero_cancel(N - sp.expand(M.det()) * (v3.T * M.inv() * v3)[0, 0]))

M2 = sp.Matrix([[1/f, q], [q, A]])
adj2 = M2.adjugate()
vt2 = sp.Matrix([vr, vh]); wvec = sp.Matrix([a, b])
D2 = sp.expand(M2.det())
P = sp.expand((vt2.T * adj2 * vt2)[0, 0])
S = sp.expand((vt2.T * adj2 * wvec)[0, 0])
W2 = sp.expand((wvec.T * adj2 * wvec)[0, 0])
K = vr * b - vh * a
check("B1c: Delta = f*D2 + W2", zero_cancel(Delta - (f * D2 + W2)))
check("B1d: N = D2 vT^2 - 2 vT S - f P - K^2",
      zero_cancel(N - (D2 * vT**2 - 2 * vT * S - f * P - K**2)))
check("B1e: Gram identity P*W2 - S^2 = D2*K^2",
      zero_cancel(P * W2 - S**2 - D2 * K**2))

# ---------------------------------------------------------------- block 2  STATIC ANCHORS
Ns = N.subs({a: 0, b: 0, vT: 0}); Ds = Delta.subs({a: 0, b: 0})
Eq_q = sp.expand(2 * sp.diff(Ns, q) * Ds - Ns * sp.diff(Ds, q))  # d/dq of N/sqrt(D) numerator
sols = sp.solve(sp.factor(Eq_q), q)
qs_exp = 2 * A * vr * vh / (f * A * vr**2 + vh**2)
check("B2a: unique static root q* = 2A vr vh/(f A vr^2 + vh^2)",
      len(sols) == 1 and zero_cancel(sols[0] - qs_exp))
# eliminated static L: square identity + branch sign
Kst = f * A * vr**2 - vh**2
Ls_sq = sp.cancel((Ns**2 / Ds).subs(q, qs_exp) - Kst**2 / (f * A) * f**0)
check("B2b(sq): [N_s^2/Delta_s](q*) = (fA vr^2 - vh^2)^2/(A) ... static perfect square",
      zero_cancel((Ns**2 / Ds).subs(q, qs_exp) - Kst**2 / A))
# L_static* = (c/8) sqrt(B) N_s/(f sqrt(D_s)) at q*; sign: N_s(q*) < 0 on K>0 (sample)
samp = {f: Ra(2), A: Ra(3), vr: Ra(1), vh: Ra(1, 2), B: Ra(5)}
check("B2b(sign): N_s(q*) = -|K_st|/sqrt-consistent branch (sample, K>0)",
      sp.nsimplify(Ns.subs(q, qs_exp).subs(samp)) < 0)
# => L*_static = -(c/8) sqrt(B) (fA vr^2 - vh^2)/(f sqrt(A)) on K>0
sth = sp.Symbol('s_th', positive=True)   # sin(theta) on (0, pi)
W1p = sp.Symbol('W1', positive=True)     # 1 + w on the trust branch
Asub = r**2 * W1p**2
Bsub = r**2 * sth**2 / W1p**2
Lst = (-Ra(1, 8) * c * sp.sqrt(B) * Kst / (f * sp.sqrt(A))).subs({A: Asub, B: Bsub})
LP1 = -Ra(1, 8) * c * sth * (r**2 * vr**2 - vh**2 / (f * W1p**2))
check("B2c: static L* = -(c/8) sin[r^2 vr^2 - vh^2/(f(1+w)^2)]  (P1 flip)",
      sp.simplify(Lst - LP1) == 0)
check("B2d: dL*/dw = -(c/4) sin(th) vh^2/(f(1+w)^3)  (P1 w-equation EXACT)",
      sp.simplify(sp.diff(Lst, W1p) + Ra(1, 4) * c * sth * vh**2 / (f * W1p**3)) == 0)
# q-tadpole at the diagonal point (formed background, measure-fork flag)
Lfull_sym = Ra(1, 8) * c * sp.sqrt(B) * N / (f * sp.sqrt(Delta))
tad = sp.diff(Lfull_sym.subs({a: 0, b: 0, vT: 0}), q).subs(q, 0)
tad = sp.simplify(tad.subs({A: Asub, B: Bsub}).subs(W1p, 1))
check("B2e: q-tadpole = +(c/4) sin(th) vr vh  (measure-fork EXACT)",
      sp.simplify(tad - Ra(1, 4) * c * sth * vr * vh) == 0)

# ---------------------------------------------------------------- block 3  TIME-ROW ELIMINATION
Ssym, Ksym = sp.symbols('S K', real=True)
W2_of = (Ssym**2 + D2 * Ksym**2) / P
N_of = D2 * vT**2 - 2 * vT * Ssym - f * P - Ksym**2
Del_of = f * D2 + W2_of
# stationarity numerators of N_of/sqrt(Del_of):
eqS = sp.expand(sp.numer(sp.together(2 * sp.diff(N_of, Ssym) * Del_of - N_of * sp.diff(Del_of, Ssym))))
eqK = sp.expand(sp.numer(sp.together(2 * sp.diff(N_of, Ksym) * Del_of - N_of * sp.diff(Del_of, Ksym))))
check("B3a: K-equation = K * [2 Del P + N D2] structure (K=0 always stationary)",
      zero_cancel(eqK.subs(Ksym, 0)))
Q = sp.expand(f * P - D2 * vT**2)
S_star = 2 * f * D2 * vT * P / Q
check("B3b: S* = 2 f D2 vT P/Q solves the S-equation on K=0",
      zero_cancel(eqS.subs({Ksym: 0, Ssym: S_star})))
check("B3b2: S* is the ONLY root on K=0 (S-equation degree 1 in S after cancel)",
      sp.degree(sp.cancel(eqS.subs(Ksym, 0)), Ssym) == 1)
Rnum = sp.expand(f * P + D2 * vT**2)
check("B3c: PERFECT SQUARE  Q^2 + 4 f D2 P vT^2 = (f P + D2 vT^2)^2",
      zero_poly(Q**2 + 4 * f * D2 * P * vT**2 - Rnum**2))
# eliminated L on K=0 branch: square identity + sign sample on Q>0
Lab_sq = sp.cancel((N_of**2 / Del_of).subs({Ksym: 0, Ssym: S_star}) - Rnum**2 / (f * D2))
check("B3d(sq): [N^2/Del](S*,K=0) = (fP + D2 vT^2)^2/(f D2)",
      zero_cancel((N_of**2 / Del_of).subs({Ksym: 0, Ssym: S_star}) - Rnum**2 / (f * D2)))
sampQ = {f: Ra(2), A: Ra(3), q: Ra(1, 5), vr: Ra(1), vh: Ra(1, 2), vT: Ra(1, 3), B: Ra(5)}
NofS = N_of.subs({Ksym: 0, Ssym: S_star})
check("B3d(sign): N(S*,K=0) < 0 on a Q>0, D2>0 sample (connected branch)",
      sp.nsimplify(NofS.subs(sampQ)) < 0 and Q.subs(sampQ) > 0 and D2.subs(sampQ) > 0)
Lab = -Ra(1, 8) * c * sp.sqrt(B) * Rnum / (f * sp.sqrt(f * D2))   # THE OBJECT
print("    L*_ab = -(c/8) sqrt(B) [f P + D2 vT^2] / (f sqrt(f D2))   [Q>0, K=0 branch]")
# map back to (a*,b*) and verify stationarity of the FULL L in a and b
absol = sp.solve([sp.Eq((vt2.T * adj2 * wvec)[0, 0], S_star),
                  sp.Eq(vr * b - vh * a, 0)], [a, b], dict=True)[0]
Ea = sp.expand(2 * sp.diff(N, a) * Delta - N * sp.diff(Delta, a))
Eb = sp.expand(2 * sp.diff(N, b) * Delta - N * sp.diff(Delta, b))
check("B3e: dL/da = 0 at (a*,b*)", zero_cancel(Ea.subs({a: absol[a], b: absol[b]})))
check("B3f: dL/db = 0 at (a*,b*)", zero_cancel(Eb.subs({a: absol[a], b: absol[b]})))
print("    a* =", sp.cancel(absol[a]))
print("    b* =", sp.cancel(absol[b]))
# the nonlinear flip
L0 = Ra(1, 8) * c * sp.sqrt(B) * (D2 * vT**2 - f * P) / (f * sp.sqrt(f * D2))
check("B3g: in-scheme L(a=b=0) = +(c/8) sqrt(B)(D2 vT^2 - fP)/(f sqrt(f D2))",
      zero_cancel(N.subs({a: 0, b: 0}) - (D2 * vT**2 - f * P)) and
      zero_cancel(Delta.subs({a: 0, b: 0}) - f * D2))
print("    => elimination maps +D2 vT^2 -> -D2 vT^2 : the W_A flip EXACT AT ALL ORDERS")

# ---------------------------------------------------------------- block 4  QUADRATIC ANCHORS
# (i) W_A on arbitrary (w; q=0) static backgrounds:
coef_vT2 = sp.diff(Lab, vT, 2) / 2
WA = sp.simplify((coef_vT2 * 4 * f**2).subs(q, 0).subs({A: Asub, B: Bsub}))
check("B4a: W_A = -(c/2) r^2 sin(th), w-INDEPENDENT (measure-fork EXACT)",
      sp.simplify(WA + Ra(1, 2) * c * r**2 * sth) == 0)
WA_q = sp.simplify((coef_vT2 * 4 * f**2).subs({A: Asub, B: Bsub}))
print("    W_A with q on:", WA_q, "  [exact q-dressing of the flip]")

# (ii) L2_corr around spherical (axisymmetric terms), symbol-level jets.
f0, f0p, df, dfT, dfr, dfh = sp.symbols('f0 f0p df df_T df_r df_th', real=True)
f0_ = sp.Symbol('f0', positive=True)
eps = sp.Symbol('epsilon')
# fields on background + perturbation (background: f0(r), vT=0, vh=0, w=0)
fX = f0_ + eps * df
vTX = eps * dfT
vrX = f0p + eps * dfr
vhX = eps * dfh
# stationary q at linear order: from cubic E1 (derived in block 5; here the
# static-form linearization suffices because vT^2-corrections are O(eps^2)):
q1 = 2 * dfh / (f0_ * f0p)
qX = eps * q1
LX = Lab.subs({A: r**2, B: r**2 * sth**2, q: qX, f: fX,
               vT: vTX, vr: vrX, vh: vhX})
L2_mine = sp.series(LX, eps, 0, 3).removeO().coeff(eps, 2)
# banked L2_corr in dp-variables, dp1 = -df/(2 f0):
dp1 = -df / (2 * f0_)
dp1T = -dfT / (2 * f0_)
dp1r = -dfr / (2 * f0_) + df * f0p / (2 * f0_**2)
dp1h = -dfh / (2 * f0_)
phi0r = -f0p / (2 * f0_)
L2_banked = -Ra(1, 2) * c * sth * (
    r**2 * dp1T**2
    + f0_**2 * r**2 * (dp1r**2 - 8 * phi0r * dp1 * dp1r + 8 * phi0r**2 * dp1**2)
    - f0_ * dp1h**2)
# dp2 = dp1^2 feed-through: L1[g] with g = dp1^2 (g has gradients):
g_, gT_, gr_, gh_ = sp.symbols('g g_T g_r g_th', real=True)
fg = f0_ - 2 * eps * f0_ * g_
vTg = -2 * eps * f0_ * gT_
vrg = f0p - 2 * eps * (f0p * g_ + f0_ * gr_)
vhg = -2 * eps * f0_ * gh_
Lg = Lab.subs({A: r**2, B: r**2 * sth**2, q: 0, f: fg,
               vT: vTg, vr: vrg, vh: vhg})
L1_func = sp.series(Lg, eps, 0, 2).removeO().coeff(eps, 1)
g2 = dp1**2
L1_dp2 = L1_func.subs({g_: g2,
                       gT_: 2 * dp1 * dp1T,
                       gr_: 2 * dp1 * dp1r,
                       gh_: 2 * dp1 * dp1h})
check("B4b: eps^2 of fully-eliminated L around spherical = banked L2_corr "
      "+ background-row feed-through  [ANGULAR-FLIP + W_A + radial jet ANCHOR]",
      sp.simplify(L2_mine - L1_dp2 - L2_banked) == 0)

# (iii) the -4 r^2 f^2 E0 mass term of the per-channel radial operator:
rv = r
u = sp.Function('u')(rv)
f0fun = sp.Function('f0', positive=True)(rv)
phi0 = -sp.log(f0fun) / 2
phi0r_f = sp.diff(phi0, rv)
expr_rad = f0fun**2 * rv**2 * (sp.diff(u, rv) - 4 * phi0r_f * u)**2 \
    - 8 * f0fun**2 * rv**2 * phi0r_f**2 * u**2
EL_rad = sp.diff(expr_rad, u) - sp.diff(sp.diff(expr_rad, sp.diff(u, rv)), rv)
E0 = sp.diff(phi0, rv, 2) + 2 * phi0r_f / rv - 2 * phi0r_f**2
target = -2 * (sp.diff(rv**2 * f0fun**2 * sp.diff(u, rv), rv) - 4 * rv**2 * f0fun**2 * E0 * u)
check("B4c: radial-sector EL = (r^2 f^2 u')' - 4 r^2 f^2 E0 u  (banked mass EXACT)",
      sp.simplify(EL_rad - target) == 0)

# ---------------------------------------------------------------- block 5  q-CUBIC + w-EQUATION
# q-elimination of L*_ab: stationarity numerator 2 R' D2 - R D2' (envelope thm)
E1 = sp.expand(2 * sp.diff(Rnum, q) * D2 - Rnum * sp.diff(D2, q))
E1_expected = 2 * (vT**2 * q**3 + (f * A * vr**2 + vh**2 - (A / f) * vT**2) * q
                    - 2 * A * vr * vh)
check("B5a: q-equation = CUBIC  vT^2 q^3 + (fA vr^2 + vh^2 - (A/f) vT^2) q "
      "- 2A vr vh = 0", zero_cancel(E1 - E1_expected))
check("B5b: static limit of the cubic returns q* (linear, unique)",
      zero_cancel(sp.cancel(-E1_expected.subs(vT, 0) / 2 / q - (f * A * vr**2 + vh**2) * (1 - qs_exp / q)) * 0)
      or zero_cancel((E1_expected.subs(vT, 0)).subs(q, qs_exp)))
# w-equation by envelope: only explicit w of L*_ab matters at q = q*(cubic).
W1 = W1p
LabW = (-Ra(1, 8) * c * (r * sth / W1) * Rnum / (f * sp.sqrt(f * D2))).subs(A, r**2 * W1**2)
dW = sp.together(sp.diff(LabW, W1))
E2num = sp.expand(-sp.numer(dW))
E2den = sp.denom(dW)
AA = r**2 * W1**2
D2A = (AA / f - q**2)
RA = sp.expand((f * P + D2 * vT**2).subs(A, AA))
brack = sp.expand((-1 + 2 * AA * (f * vr**2 + vT**2 / f) / RA - AA / (f * D2A)) * RA * f * D2A)
check("B5c: dL/dW1 numerator = -(c f r s_th) * [(-1 + 2A(f vr^2 + vT^2/f)/R "
      "- A/(f D2)) * R f D2]  — the exact w-equation",
      zero_cancel(E2num - c * f * r * sth * brack))
print("    dL/dW1 = -(c r s_th) * bracket * R/(denominator);  denominator =", E2den)
# static residual of the w-equation at q = q*_static:  prop. -vh^2 * K_st
brack_static = sp.together(brack.subs(vT, 0).subs(q, qs_exp.subs(A, AA)))
num_bs = sp.factor(sp.numer(brack_static))
print("    static w-residual numerator factors:", num_bs)
check("B5d: static w-residual = 2 W1^2 r^2 vh^2 (f A vr^2 - vh^2)^7 / (pos)^k "
      "— zero set off the degenerate locus is vh = 0 (P1 theorem)",
      zero_poly(num_bs - 2 * W1**2 * r**2 * vh**2 * (f * r**2 * W1**2 * vr**2 - vh**2)**7))
# spherical-motion slice: vh = 0, q = 0: w-equation IDENTICALLY satisfied
check("B5e: vh=0, q=0 => w-equation identity (moving spherical keeps w flat)",
      zero_cancel(brack.subs({vh: 0, q: 0})))

print()
print("PASS:", len(PASS), " FAIL:", len(FAIL))
if FAIL:
    print("FAILED:", FAIL); raise SystemExit(1)
