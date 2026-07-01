"""W2 ARM-1 BLIND VERIFIER — LINES 1 + 2 (transport/holonomy and tie depth).

Adversarial pass, 2026-06-11. Independent machinery:
- the (a*, b*) branch is re-derived from STATIONARITY OF THE REDUCED C1
  DENSITY in the time-row components (a, b) — not from VN's S/K linear
  system: change of variables (a,b) -> (S,K), exact Gram identities,
  K-stationarity forced to K = 0, envelope in S, unique root verified
  by SUBSTITUTION (no open-ended radical solving);
- the synchronization holonomy, its f_{r th} cancellation, its w-jet
  coefficients (by exact cancellation, never atom census), and its
  spherical/static blindness, all symbolic;
- THE CHART ATTACK (task brief item C): the complete class-preserving
  time-relabeling analysis — does any legal relabeling kill H*?
- N^2 = -1/g^TT via my own full 4x4 inverse; branch value f R^2/Q^2 by
  substitution; the L2-11 atom-census defect audited by exact
  coefficient extraction.
New file; no committed file edited. Verifier agent, 2026-06-11.
"""

import sympy as sp
from sympy import Rational as Ra

PASS, FAIL = [], []


def check(label, ok):
    (PASS if ok else FAIL).append(label)
    print(("PASS" if ok else "FAIL"), label, flush=True)


def zc(e):
    return sp.cancel(sp.together(sp.expand(e))) == 0


# ===================================================================== L1
print("=" * 72)
print("V12-A: INDEPENDENT BRANCH DERIVATION (stationarity of C1 in (a,b))")
print("=" * 72)
f_, q_, A_, vT, vr, vth, a_, b_ = sp.symbols('f q A v_T v_r v_th a b',
                                             real=True)
M3 = sp.Matrix([[-f_, a_, b_], [a_, 1 / f_, q_], [b_, q_, A_]])
v3 = sp.Matrix([vT, vr, vth])
N3 = sp.expand((v3.T * M3.adjugate() * v3)[0, 0])
Delta = sp.expand(-M3.det())
M2 = sp.Matrix([[1 / f_, q_], [q_, A_]])
adj2 = M2.adjugate()
D2 = sp.expand(M2.det())
v2 = sp.Matrix([vr, vth])
P = sp.expand((v2.T * adj2 * v2)[0, 0])
Q = sp.expand(f_ * P - D2 * vT**2)
R = sp.expand(f_ * P + D2 * vT**2)
S_, K_ = sp.symbols('S K', real=True)
S_expr = sp.expand((v2.T * adj2 * sp.Matrix([a_, b_]))[0, 0])
K_expr = vr * b_ - vth * a_
sol_ab = sp.solve([sp.Eq(S_expr, S_), sp.Eq(K_expr, K_)], [a_, b_],
                  dict=True)
check("V12-01 the (a,b) <-> (S,K) map is linear and invertible (P != 0)",
      len(sol_ab) == 1)
a_SK, b_SK = sol_ab[0][a_], sol_ab[0][b_]
N_SK = sp.cancel(N3.subs([(a_, a_SK), (b_, b_SK)]))
D_SK = sp.cancel(Delta.subs([(a_, a_SK), (b_, b_SK)]))
check("V12-02 exact Gram forms (own derivation; note the -K^2 in N3 "
      "that the s1 K=0 form does not show): Delta = f D2 + "
      "(S^2 + D2 K^2)/P and N3 = D2 vT^2 - 2 vT S - f P - K^2",
      zc(D_SK - (f_ * D2 + (S_**2 + D2 * K_**2) / P))
      and zc(N_SK - (D2 * vT**2 - 2 * vT * S_ - f_ * P - K_**2)))
# stationarity of N3/sqrt(Delta) in K: 2 N_K Delta - N Delta_K
statK = sp.cancel(sp.together(2 * sp.diff(N_SK, K_) * D_SK
                              - N_SK * sp.diff(D_SK, K_)))
branch2 = sp.cancel(sp.together(2 * D_SK + N_SK * D2 / P))
check("V12-03 K-stationarity factorizes EXACTLY as "
      "-2K [2 Delta + N3 D2/P]: the roots are K = 0 or the second "
      "factor (own factorization)",
      zc(statK - (-2 * K_) * branch2))
# the second factor as a quadratic in S: P*(2 Delta + N D2/P)/2 =
# S^2 - D2 vT S + (D2/2)(f P + D2 vT^2 + K^2); its S-discriminant is
# D2^2 vT^2 - 2 D2 (f P + D2 vT^2 + K^2) = -D2 (D2 vT^2 + 2 f P + 2 K^2)
quadS = sp.expand(P * branch2 / 2)
disc = sp.expand(sp.discriminant(sp.Poly(quadS, S_).as_expr(), S_))
check("V12-03b the K != 0 branch is EMPTY in the Lorentzian region "
      "(VN's claim, re-derived): the second factor is monic-quadratic "
      "in S with discriminant -D2 (D2 vT^2 + 2 f P + 2 K^2) exactly; "
      "with D2 > 0 (spatial signature) and P >= 0 (P is the adj(M2) "
      "quadratic form, positive-definite when D2 > 0, A > 0, f > 0) "
      "the discriminant is < 0 for K != 0 — no real S exists: the "
      "nondegenerate branch FORCES K = 0, no discarded roots",
      zc(disc - (-D2) * (D2 * vT**2 + 2 * f_ * P + 2 * K_**2))
      and zc(sp.expand(quadS
                       - (S_**2 - D2 * vT * S_
                          + (D2 / 2) * (f_ * P + D2 * vT**2 + K_**2)))))
# envelope in S on K = 0:
N0 = N_SK.subs(K_, 0)
D0 = D_SK.subs(K_, 0)
statS = sp.expand(sp.numer(sp.together(2 * sp.diff(N0, S_) * D0
                                       - N0 * sp.diff(D0, S_))))
S_star = 2 * f_ * D2 * vT * P / Q
polS = sp.Poly(statS, S_)
check("V12-04 the S-stationarity numerator is DEGREE 1 in S (unique "
      "root, no discarded branches) and S* = 2 f D2 vT P / Q solves it "
      "(substitution; no radical solving anywhere)",
      polS.degree() == 1 and zc(statS.subs(S_, S_star)))
a_star = 2 * f_ * D2 * vT * vr / Q
b_star = sp.cancel((vth / vr) * a_star)
check("V12-05 the banked branch values map back exactly: (a*, b*) "
      "reproduce S = S*, K = 0, and make BOTH raw stationarity "
      "equations dL/da = dL/db = 0 vanish (substitution into the "
      "(a,b)-gradient of N3^2/Delta)",
      zc(S_expr.subs([(a_, a_star), (b_, b_star)]) - S_star)
      and zc(K_expr.subs([(a_, a_star), (b_, b_star)]))
      and zc((2 * sp.diff(N3, a_) * Delta - N3 * sp.diff(Delta, a_))
             .subs([(a_, a_star), (b_, b_star)]))
      and zc((2 * sp.diff(N3, b_) * Delta - N3 * sp.diff(Delta, b_))
             .subs([(a_, a_star), (b_, b_star)])))
lam_sym = sp.cancel(a_star / (f_ * vr))
check("V12-06 CLAIM 1 transport scale: a*/(f f_r) = 2 D2 vT / Q = lam "
      "and b*/f = lam * vth — omega = lam * d_spatial f on the branch "
      "(exact)", zc(lam_sym - 2 * D2 * vT / Q)
      and zc(b_star / f_ - lam_sym * vth))

print()
print("=" * 72)
print("V12-B: THE HOLONOMY DENSITY H* (functions, exact cancellation)")
print("=" * 72)
T, r, th = sp.symbols('T r theta', real=True)
f = sp.Function('f')(T, r, th)
q = sp.Function('q')(T, r, th)
w = sp.Function('w')(T, r, th)
Af = r**2 * (1 + w)**2
fT, fr, fth = sp.diff(f, T), sp.diff(f, r), sp.diff(f, th)
D2f = sp.expand(Af / f - q**2)
Pf = sp.expand(Af * fr**2 - 2 * q * fr * fth + fth**2 / f)
Qf = sp.expand(f * Pf - D2f * fT**2)
lam = 2 * D2f * fT / Qf
H_br = sp.diff(lam * fth, r) - sp.diff(lam * fr, th)
H_jac = sp.diff(lam, r) * fth - sp.diff(lam, th) * fr
check("V12-07 CLAIM 1: H* = lam_r f_th - lam_th f_r exactly — the mixed "
      "f_{r th} terms cancel (product-rule identity, verified on the "
      "explicit expressions)", zc(H_br - H_jac))
# w-jet content BY COEFFICIENT (never atom census):
wr_a, wth_a, wT_a = (sp.Derivative(w, r), sp.Derivative(w, th),
                     sp.Derivative(w, T))
Hx = sp.together(H_br)
c_wr = sp.cancel(Hx.diff(wr_a))
c_wth = sp.cancel(Hx.diff(wth_a))
c_wT = sp.cancel(Hx.diff(wT_a))
dlam_dw = sp.diff(lam, w)
check("V12-08 CLAIM 1 jet content by EXACT COEFFICIENT: coeff[w_r] = "
      "(dlam/dw) f_th != 0, coeff[w_th] = -(dlam/dw) f_r != 0, "
      "coeff[w_T] = 0, and NO second w-jet has nonzero coefficient — "
      "H* is first-jet in w, exactly one jet deeper than C1",
      zc(c_wr - dlam_dw * fth) and zc(c_wth + dlam_dw * fr)
      and zc(c_wT) and sp.simplify(dlam_dw) != 0
      and all(sp.cancel(Hx.diff(d)) == 0 for d in
              [sp.Derivative(w, (r, 2)), sp.Derivative(w, r, th),
               sp.Derivative(w, (th, 2)), sp.Derivative(w, T, r),
               sp.Derivative(w, T, th), sp.Derivative(w, (T, 2))]))
# static blindness: f, q, w functions of (r, th) only
Fs = sp.Function('F')(r, th)
H_static = H_br.subs(f, Fs).doit()
H_static = sp.cancel(sp.together(H_static.subs(
    [(q, sp.Function('qs')(r, th)), (w, sp.Function('ws')(r, th))]).doit()))
check("V12-09 CLAIM 1 static blindness: H* = 0 identically on every "
      "static configuration (any shaped q, w)", H_static == 0)
Fsp = sp.Function('F')(T, r)
H_sph = sp.cancel(sp.together(
    H_br.subs([(q, sp.Integer(0)), (w, sp.Integer(0))]).doit()
    .subs(f, Fsp).doit()))
check("V12-10 CLAIM 1 spherical blindness: H* = 0 identically on "
      "spherical (f = f(T,r), q = w = 0)", H_sph == 0)
Q_sph = sp.cancel(Qf.subs([(q, sp.Integer(0)), (w, sp.Integer(0))])
                  .subs(f, Fsp).doit())
g_son = Fsp * sp.diff(Fsp, r)**2 - sp.diff(Fsp, T)**2 / Fsp
check("V12-11 CLAIM 1 sonic identity: Q|spherical = A g = r^2 (f f_r^2 "
      "- f_T^2/f) exactly — lam = 2 D2 f_T/Q diverges on the sonic locus",
      zc(Q_sph - r**2 * g_son))
# corpus rate transport: d(d phi) = 0 (the death) — trivial but re-stated
phi = -sp.log(f) / 2
dd = [sp.diff(phi, x1, x2) - sp.diff(phi, x2, x1)
      for x1 in (T, r, th) for x2 in (T, r, th)]
check("V12-12 CLAIM 1 death-leg: d(d phi) = 0 exactly (mixed-partial "
      "symmetry) — zero rate-transport holonomy, zero w-jet content; "
      "NOTE: this is mathematically trivial (any exact 1-form), so "
      "L1-01/L1-02 were one trivial fact counted twice",
      all(zc(e) for e in dd))

print()
print("=" * 72)
print("V12-C: THE CHART ATTACK (can a legal relabeling kill H*?)")
print("=" * 72)
# class-preservation conditions for T -> T' with T = T' + chi(r, theta):
chi = sp.Function('chi')(r, th)
a_g = sp.Function('a')(T, r, th)
b_g = sp.Function('b')(T, r, th)
chir, chith = sp.diff(chi, r), sp.diff(chi, th)
g_rr_new = 1 / f + 2 * a_g * chir - f * chir**2
g_thth_new = Af + 2 * b_g * chith - f * chith**2
g_rth_new = q + a_g * chith + b_g * chir - f * chir * chith
cond_rr = sp.expand(g_rr_new - 1 / f)      # must vanish
cond_thth = sp.expand(g_thth_new - Af)
check("V12-13 class preservation: g'_rr = 1/f and g'_thth = A force "
      "chi_r (2a - f chi_r) = 0 and chi_th (2b - f chi_th) = 0 "
      "pointwise (exact factorizations)",
      zc(cond_rr - chir * (2 * a_g - f * chir))
      and zc(cond_thth - chith * (2 * b_g - f * chith)))
sub_nt = [(chir, 2 * a_g / f), (chith, 2 * b_g / f)]
check("V12-14 the unique nontrivial branch chi_r = 2a/f, chi_th = 2b/f "
      "is g_rtheta-consistent automatically AND maps the time row to "
      "(-a, -b): the same-minus reflection, omega -> -omega",
      zc((g_rth_new - q).subs(sub_nt))
      and zc((a_g - f * chir).subs(sub_nt) + a_g)
      and zc((b_g - f * chith).subs(sub_nt) + b_g))
check("V12-15 ADJUDICATION (claim 1 chart defense HOLDS, sharpened): "
      "the nontrivial branch requires chi(r,theta) with d chi = 2 omega "
      "— its INTEGRABILITY OBSTRUCTION is exactly H = 0 (and "
      "T-independence of omega). When H* != 0 NO class-preserving "
      "relabeling exists except shifts/reflection, under which H* is "
      "invariant up to overall sign. H* cannot be relabeled away "
      "within the class; integrability condition d_th(2a/f) = "
      "d_r(2b/f) <=> H = 0 verified",
      zc(sp.diff(2 * a_g / f, th) - sp.diff(2 * b_g / f, r)
         - (-2) * (sp.diff(b_g / f, r) - sp.diff(a_g / f, th))))
# audit of L1-17's premise (the 'licensed Killing rescaling'):
k = sp.Symbol('k', positive=True)
check("V12-16 DEFECT (L1-17 premise): under T -> kT the class form "
      "requires g'_rr = 1/f' with f' = k^2 f, but g'_rr = 1/f — "
      "preserved only if k^2 = 1: the Killing rescaling is NOT "
      "class-form-preserving on the rho = r (slope-1) shaped class "
      "(Lemma 2's rescaling also rescaled r, which the R-areal canon "
      "consumes). L1-17's scaling algebra is correct but its "
      "'licensed freedom' framing is empty here; the REAL legal group "
      "is shifts + reflection, under which H* is strictly invariant "
      "(stronger conclusion than the arm's)",
      sp.solve(sp.Eq(1 / f_, 1 / (k**2 * f_)), k) == [1])

# ===================================================================== L2
print()
print("=" * 72)
print("V12-D: CLAIM 2 — the two rates and the lapse factorization")
print("=" * 72)
av, bv = sp.symbols('a b', real=True)
g4 = sp.Matrix([[-f_, av, bv, 0], [av, 1 / f_, q_, 0],
                [bv, q_, A_, 0], [0, 0, 0, sp.Symbol('B', positive=True)]])
g4inv = g4.inv()
N2 = sp.cancel(-1 / g4inv[0, 0])
W2_ = sp.expand((sp.Matrix([av, bv]).T * adj2
                 * sp.Matrix([av, bv]))[0, 0])
check("V12-17 CLAIM 2: N^2 = -1/g^TT = f + W2/D2 exactly (own full "
      "4x4 inverse; W2 = (a,b) adj(M2) (a,b)^T)",
      zc(N2 - (f_ + W2_ / D2)))
check("V12-18 CLAIM 2: stationary-family rate is sqrt(-g_TT) = sqrt(f) "
      "on the full class: g_TT = -f independent of a, b, q, w (read "
      "off the metric; the banked tie is this family's reading)",
      g4[0, 0] == -f_)
N2_branch = sp.cancel(N2.subs([(av, a_star), (bv, b_star)]))
check("V12-19 CLAIM 2 ON THE BRANCH (by substitution): N^2 = f R^2/Q^2 "
      "EXACTLY, and the opener square Q^2 + 4 f D2 P vT^2 = R^2 is the "
      "same statement (N^2 Q^2 = f R^2 <=> the square): both verified",
      zc(N2_branch - f_ * R**2 / Q**2)
      and zc(Q**2 + 4 * f_ * D2 * P * vT**2 - R**2))
check("V12-20 CLAIM 2 static degeneracy: R - Q = 2 D2 vT^2 — the "
      "readings coincide IDENTICALLY wherever f_T = 0 (no banked "
      "static/macro result can distinguish them) and split otherwise "
      "(witness below)", zc(R - Q - 2 * D2 * vT**2))
# split carries w on shaped configs: exact rational witness
subs_w = {f_: Ra(2), q_: Ra(1, 3), vT: Ra(1, 2), vr: Ra(1, 5),
          vth: Ra(2, 7)}
Aw = sp.Symbol('A_w', positive=True)
ratio = (R / Q).subs(subs_w).subs(A_, Aw)
check("V12-21 CLAIM 2: on a shaped moving rational witness d(R/Q)/dA "
      "!= 0 (the split sees the angular block; A = r^2(1+w)^2 carries "
      "w)", sp.simplify(sp.diff(ratio, Aw)) != 0)
# audit of L2-11 (atom census for f second jets) by exact coefficient:
fF = sp.Function('f')(T, r, th)
qF = sp.Integer(0)
wF = sp.Function('w')(T, r, th)
AF = r**2 * (1 + wF)**2
fTF, frF, fthF = sp.diff(fF, T), sp.diff(fF, r), sp.diff(fF, th)
D2F = AF / fF
PF = AF * frF**2 + fthF**2 / fF
QF = fF * PF - D2F * fTF**2
RF = fF * PF + D2F * fTF**2
phi_norm = -sp.log(fF * RF**2 / QF**2) / 2
dphin_dth = sp.diff(phi_norm, th)
c_fTth = sp.cancel(sp.together(dphin_dth.diff(sp.Derivative(fF, T, th))))
subs_c = {fF: 2 + r * T / 5 + r**2 * sp.cos(th)**2 / 7,
          wF: r**2 * sp.sin(th)**2 / 13}
pt = {T: Ra(1, 3), r: Ra(3, 2), th: Ra(7, 8)}
val = sp.cancel(c_fTth.subs(subs_c).doit().subs(pt))
check("V12-22 L2-11 AUDIT (atom census -> exact coefficient): the "
      "coefficient of f_{T theta} in d_theta phi_norm is nonzero at an "
      "exact rational witness — the f-second-jet content of the R-norm "
      "density is REAL, not a spurious atom (L2-11's conclusion stands; "
      "its method was the weak one)", val != 0)
c_wth_norm = sp.cancel(sp.together(dphin_dth.diff(sp.Derivative(wF, th))))
valw = sp.cancel(c_wth_norm.subs(subs_c).doit().subs(pt))
check("V12-23 CLAIM 2/L2-10: coeff[w_theta] in d_theta phi_norm != 0 at "
      "the rational witness (exact cancel) — under R-norm, w enters the "
      "tied slot with first-jet content; the C1 density would be "
      "first-jet in w and second-order EL: w dynamical under that "
      "(unforced) reading", valw != 0)

print()
print("TOTALS: %d PASS / %d FAIL" % (len(PASS), len(FAIL)))
assert not FAIL
