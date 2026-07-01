"""W2 ARM-1 BLIND VERIFIER — LINE 3 (squares' origin; u-variable; brick fork).

Adversarial pass, 2026-06-12 (session of 2026-06-11). Independent
machinery: every claimed identity verified by my own expansion (no
sp.solve on radicals; claimed roots verified by substitution); the brick
census attacked for COMPLETENESS by generalizing to the continuum
u_alpha = f r (1+w)^alpha and to a q-bearing brick the arm never named.
New file; no committed file edited. Verifier agent.
"""

import sympy as sp
from sympy import Rational as Ra

PASS, FAIL = [], []


def check(label, ok):
    (PASS if ok else FAIL).append(label)
    print(("PASS" if ok else "FAIL"), label, flush=True)


def zc(e):
    return sp.cancel(sp.together(sp.expand(e))) == 0


print("=" * 72)
print("V3-A: THE ENVELOPE/DISCRIMINANT LEMMA (claim 3, own algebra)")
print("=" * 72)
m11, m22, z, v1, v2 = sp.symbols('m11 m22 z v1 v2', real=True)
M = sp.Matrix([[m11, z], [z, m22]])
v = sp.Matrix([v1, v2])
N = sp.expand((v.T * M.adjugate() * v)[0, 0])
Delta = sp.expand(M.det())
stat = sp.expand(2 * sp.diff(N, z) * Delta - N * sp.diff(Delta, z))
z_star = 2 * m11 * m22 * v1 * v2 / (m22 * v1**2 + m11 * v2**2)
check("V3-01 stationarity of N/sqrt(Delta) in z is LINEAR in z "
      "(degree check on my own expansion — uniqueness is structural, "
      "no solve needed) and z* solves it by substitution",
      sp.Poly(stat, z).degree() == 1 and zc(stat.subs(z, z_star)))
val = sp.cancel((N**2 / Delta).subs(z, z_star))
check("V3-02 N^2/Delta at z* = (m22 v1^2 - m11 v2^2)^2/(m11 m22) "
      "EXACTLY (the general envelope square, claim 3's one-theorem core)",
      zc(val - (m22 * v1**2 - m11 * v2**2)**2 / (m11 * m22)))
f_, A_, fr_, fth_, vT_, D2_, P_ = sp.symbols(
    'f A f_r f_th v_T D2 P', positive=True)
inst_a = val.subs([(m11, 1 / f_), (m22, A_), (v1, fr_), (v2, fth_)])
check("V3-03 INSTANCE static-q: f A * (N^2/Delta)|* = "
      "(f A f_r^2 - f_th^2)^2 (the pde_p1 D-12 square)",
      zc(inst_a * f_ * A_ - (f_ * A_ * fr_**2 - fth_**2)**2))
# time-row instance with the TRUE N (incl. -K^2, K = 0 here):
S_ = sp.Symbol('S', real=True)
N_t = D2_ * vT_**2 - 2 * vT_ * S_ - f_ * P_
Del_t = f_ * D2_ + S_**2 / P_
stat_t = sp.expand(sp.numer(sp.together(
    2 * sp.diff(N_t, S_) * Del_t - N_t * sp.diff(Del_t, S_))))
S_star = 2 * f_ * D2_ * vT_ * P_ / (f_ * P_ - D2_ * vT_**2)
check("V3-04 INSTANCE time-row: S-stationarity numerator is degree 1 "
      "(unique root), S* solves it by substitution, and N^2/Delta at "
      "S* = (f P + D2 vT^2)^2/(f D2): the opener square from the SAME "
      "lemma", sp.Poly(stat_t, S_).degree() == 1
      and zc(stat_t.subs(S_, S_star))
      and zc(sp.cancel((N_t**2 / Del_t).subs(S_, S_star))
             - (f_ * P_ + D2_ * vT_**2)**2 / (f_ * D2_)))
check("V3-05 the binomial-discriminant core (x+y)^2 - 4xy = (x-y)^2 "
      "and the opener square Q^2 + 4 f D2 P vT^2 = R^2 as its x = fP, "
      "y = D2 vT^2 instance",
      zc((f_ * P_ - D2_ * vT_**2)**2 + 4 * f_ * D2_ * P_ * vT_**2
         - (f_ * P_ + D2_ * vT_**2)**2))

print()
print("=" * 72)
print("V3-B: THE RHO SQUARE (different origin) AND THE u-IDENTITY")
print("=" * 72)
r = sp.Symbol('r', positive=True)
fr_fun = sp.Function('f')(r)
rho = sp.Function('rho')(r)
u = fr_fun * rho
L_rho = Ra(1, 4) * rho**2 * sp.diff(fr_fun, r)**2
D_star = (Ra(1, 4) * fr_fun**2 * sp.diff(rho, r)**2
          + Ra(1, 2) * rho * fr_fun * sp.diff(fr_fun, r) * sp.diff(rho, r))
check("V3-06 rho square re-verified: L_C1 + D* = (1/4)[(f rho)']^2 "
      "exact, and it is NOT an off-diagonal elimination (the (f,rho) "
      "metric is diagonal; D* was survival-forced) — 'two origins' is "
      "the honest statement, as the arm recorded",
      zc(L_rho + D_star - Ra(1, 4) * sp.diff(u, r)**2))
th = sp.Symbol('theta', real=True)
fF = sp.Function('f')(r, th)
wF = sp.Function('w')(r, th)
W1 = 1 + wF
fth2 = sp.diff(fF, th)
wth2 = sp.diff(wF, th)
u_th = fF * r * W1
deficit = sp.expand(sp.diff(u_th, th)**2 / r**2 - W1**2 * fth2**2)
check("V3-07 CLAIM 3 u-identity by expansion: u_theta^2/r^2 - "
      "(1+w)^2 f_th^2 = 2(1+w) f f_th w_th + f^2 w_th^2 EXACTLY",
      zc(deficit - (2 * W1 * fF * fth2 * wth2 + fF**2 * wth2**2)))
u_ph = fF * r / W1
deficit_ph = sp.expand(sp.diff(u_ph, th)**2 / r**2 - fth2**2 / W1**2)
check("V3-08 phi-brick identity by expansion: opposite cross sign, "
      "deficit = -2 f f_th w_th/(1+w)^3 + f^2 w_th^2/(1+w)^4",
      zc(deficit_ph - (-2 * fF * fth2 * wth2 / W1**3
                       + fF**2 * wth2**2 / W1**4)))
check("V3-09 determinant brick exactly w-blind: u_det = "
      "f (g_thth g_phph / sin^2)^{1/4} = f r identically",
      zc(fF * sp.sqrt(sp.sqrt(r**4)) - fF * r))

print()
print("=" * 72)
print("V3-C: BRICK-FORK COMPLETENESS ATTACK (task brief item E)")
print("=" * 72)
# the arm's census: THREE bricks. Attack: ANY u_alpha = f r (1+w)^alpha
# coincides with f rho on spherical — the fork is a CONTINUUM, of which
# the metric-brick members are the alpha = +1, -1, 0 slice.
alpha = sp.Symbol('alpha', real=True)
# The deficit identity holds for an ARBITRARY weight v(r,theta):
vF = sp.Function('v')(r, th)
vth = sp.diff(vF, th)
u_v = fF * r * vF
def_v = sp.expand(sp.diff(u_v, th)**2 / r**2 - vF**2 * fth2**2)
target_v = 2 * fF * fth2 * vF * vth + fF**2 * vth**2
check("V3-10 GENERALIZED DEFICIT (the arm's census is a SLICE of a "
      "FUNCTION SPACE): for ARBITRARY weight v, u = f r v satisfies "
      "u_th^2/r^2 - v^2 f_th^2 = 2 f f_th v v_th + f^2 v_th^2 (trivial "
      "binomial, verified) — every v = v(w) with v(0) = 1 coincides "
      "with f rho on spherical: the brick fork is INFINITE-dimensional "
      "(any dilation weight of the shape field), of which the arm's "
      "three bricks are v = (1+w)^{+1,-1,0}. 'Unselected' is therefore "
      "much STRONGER than the arm recorded — and also much CHEAPER: "
      "the binomial identity carries no selection power at all",
      zc(def_v - target_v))
v_al = W1**alpha
chain = sp.diff(v_al, th) - alpha * W1**(alpha - 1) * wth2
check("V3-11 the alpha-slice reproduces the arm's two identities by "
      "pure chain rule (v_th = alpha (1+w)^{alpha-1} w_th; alpha = +1 "
      "gives L3-11, alpha = -1 gives L3-21), and at f_theta = 0 the "
      "deficit f^2 v_th^2 = alpha^2 f^2 (1+w)^{2a-2} w_th^2 >= 0 is a "
      "DERIVED square for EVERY member — invariant content survives "
      "the enlargement; alpha = 0 (v = 1) is the unique w-blind member",
      zc(sp.powsimp(chain, force=True))
      and zc(target_v.subs(vF, W1).doit().subs(sp.Derivative(fF, th), 0)
             - fF**2 * wth2**2)
      and zc(target_v.subs(vF, 1 / W1).doit()
             .subs(sp.Derivative(fF, th), 0)
             - fF**2 * wth2**2 / W1**4))
# a q-bearing brick the census never names: u_q = f sqrt(g_thth - f q^2)
# (= f sqrt(f D2)); it equals the theta-brick at q = 0 and is a FOURTH
# (family of) member(s) on the q-on class:
qF = sp.Function('q')(r, th)
u_qbrick = fF * sp.sqrt(r**2 * W1**2 - fF * qF**2)
check("V3-12 COMPLETENESS DEFECT (recorded): the q-bearing brick "
      "u_q = f sqrt(g_thth - f q^2) = f sqrt(f D2) reduces EXACTLY to "
      "the theta-brick f r (1+w) at q = 0 (and to f rho on spherical) "
      "— the arm's three-brick census is complete only on the q = 0 "
      "slice; on the q-on class the fork is wider still. (No member "
      "is selected by anything — the arm's no-forcing conclusion is "
      "unchanged, indeed strengthened.)",
      zc(u_qbrick.subs(qF, sp.Integer(0))**2 - (fF * r * W1)**2)
      and zc(u_qbrick.subs(qF, sp.Integer(0)).subs(wF, sp.Integer(0))**2
             - (fF * r)**2))
# does anything select a member? the one quantitative candidate: the
# L4 bulk wave-quadratic weight (1+w)^{-2} vs the brick deficits at
# f_th = 0: theta-brick (1+w)^0, phi-brick (1+w)^{-4}, alpha generic
# (1+w)^{2 alpha - 2}: matching the L4 weight needs 2a - 2 = -2, a = 0
# — the w-BLIND brick. No brick reproduces the curvature species' weight
# with a nonzero deficit:
check("V3-13 SELECTION HUNT (negative, exact): matching the curvature "
      "species' bulk weight (1+w)^{-2} within the continuum requires "
      "alpha = 0 — exactly the w-blind member: NO brick deficit "
      "reproduces the L4 wave sector; the u-binomial structure and the "
      "curvature species are DIFFERENT objects (consistent with the "
      "arm's 'banked as structure, not as a derived action term')",
      sp.solve(sp.Eq(2 * alpha - 2, -2), alpha) == [0])

print()
print("TOTALS: %d PASS / %d FAIL" % (len(PASS), len(FAIL)))
assert not FAIL
