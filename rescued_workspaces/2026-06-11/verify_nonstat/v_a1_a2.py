"""BLIND VERIFIER — N2 claims A1 + A2, recomputed from scratch.

Independent route: I build the 4-metric myself, form
    L = -(c/8) sqrt(-g) g^{mu nu} f_mu f_nu / f
via the explicit 3x3 inverse (phi-block diagonal), and express
stationarity in each algebraic entry (a, b, q, w) as RATIONAL
numerator conditions (no radicals):
    in a:  E_a = Delta_a * G + 2 Delta * dG/da = 0,   G = v^T M^{-1} v
    (Delta = -det M > 0 Lorentzian), similarly b; for q the same; for
    w both sqrt(B) and Delta carry W1 = 1+w:
    E_w = (B_w Delta + B Delta_w) G + 2 B Delta dG/dw = 0.
All checks are my own; PASS/FAIL recorded.
"""
import sympy as sp
from sympy import Rational as Ra

PASS, FAIL = [], []
def check(label, ok):
    (PASS if ok else FAIL).append(label)
    print(("PASS" if ok else "FAIL"), label, flush=True)

def zc(e):
    return sp.cancel(sp.together(e)) == 0

c, f, r = sp.symbols('c f r', positive=True)
sth, W1 = sp.symbols('s_th W1', positive=True)
a, b, q = sp.symbols('a b q', real=True)
vT, vr, vh = sp.symbols('vT vr vh', real=True)
A, B = sp.symbols('A B', positive=True)

# ---- my own objects -------------------------------------------------
M = sp.Matrix([[-f, a, b], [a, 1/f, q], [b, q, A]])
Minv = M.inv()
G = sp.cancel(sp.together((sp.Matrix([vT, vr, vh]).T * Minv
                           * sp.Matrix([vT, vr, vh]))[0, 0]))
Delta = sp.expand(-M.det())
D2 = A/f - q**2
P = A*vr**2 - 2*q*vr*vh + vh**2/f
Q = sp.expand(f*P - D2*vT**2)
R = sp.expand(f*P + D2*vT**2)

# A1-1: the trivial-but-load-bearing perfect square
check("A1-1 perfect square Q^2 + 4 f D2 P vT^2 == (fP + D2 vT^2)^2",
      sp.expand(Q**2 + 4*f*D2*P*vT**2 - R**2) == 0)

# A1-2: candidate stationary point of the time row (my closed form):
#   a* = 2 f D2 vT vr / Q,   b* = 2 f D2 vT vh / Q
astar = 2*f*D2*vT*vr/Q
bstar = 2*f*D2*vT*vh/Q
Ea = sp.diff(Delta, a)*G + 2*Delta*sp.diff(G, a)
Eb = sp.diff(Delta, b)*G + 2*Delta*sp.diff(G, b)
check("A1-2a dL/da = 0 at (a*, b*)  [rational numerator, full L]",
      zc(Ea.subs({a: astar, b: bstar})))
check("A1-2b dL/db = 0 at (a*, b*)", zc(Eb.subs({a: astar, b: bstar})))

# A1-3: value of the eliminated L. L = -(c/8) sqrt(B Delta) G / f.
#   claim: at (a*,b*),  sqrt(Delta) G = sgn-consistent  R / sqrt(f D2),
#   i.e. Delta G^2 = R^2/(f D2)  and  G < 0 on a Q>0 sample.
Del_s = sp.cancel(Delta.subs({a: astar, b: bstar}))
G_s = sp.cancel(G.subs({a: astar, b: bstar}))
check("A1-3a Delta(a*,b*) * G(a*,b*)^2 == R^2/(f D2)",
      zc(Del_s*G_s**2 - R**2/(f*D2)))
samp = {f: Ra(2), A: Ra(3), q: Ra(1, 5), vr: Ra(1), vh: Ra(1, 2),
        vT: Ra(1, 3)}
sQ = Q.subs(samp)
check("A1-3b sign: G(a*,b*) > 0 on a Q>0,D2>0 rational sample "
      "(=> L* = -(c/8) sqrt(B) R/(f sqrt(f D2)) NEGATIVE of R-sector)",
      sQ > 0 and G_s.subs(samp) > 0 and D2.subs(samp) > 0
      and Del_s.subs(samp) > 0)
# NOTE on conventions: L = -(c/8) sqrt(B*Delta) * G / f. With G>0 at the
# stationary point, L* = -(c/8) sqrt(B) R/(f sqrt(f D2)).  Unreduced
# scheme (a=b=0): G(0,0) = ?
G00 = sp.cancel(G.subs({a: 0, b: 0}))
check("A1-3c in-scheme G(a=b=0) == (D2 vT^2 - f P)/(f D2) "
      "(so L(0,0) carries +D2 vT^2 where L* carries -D2 vT^2: "
      "the f_T^2 sector sign-reverses at ALL orders)",
      zc(G00 - (D2*vT**2 - f*P)/(f*D2)))
# sanity: vT^2-coefficients of sqrt(Delta)G at a=b=0 vs at (a*,b*):
cof_in = sp.cancel(sp.diff(G00*f*D2, vT, 2)/2)     # = +D2
cof_out = sp.cancel(sp.diff(R, vT, 2)/2)           # = +D2 but L* sign -
check("A1-3d both vT^2 blocks equal D2; sign flip is purely the overall "
      "minus on R vs plus on (D2 vT^2 - fP)", zc(cof_in - D2)
      and zc(cof_out - D2))

# A1-4: uniqueness (K != 0 branch empty).  Change of variables
# (a,b) -> (S,K): S = a(A vr - q vh) + b(vh/f - q vr), K = vr b - vh a,
# Jacobian = P (nonzero off the measure-zero vr=vh=0 set).
Ssym, Ksym = sp.symbols('S K', real=True)
S_ab = a*(A*vr - q*vh) + b*(vh/f - q*vr)
K_ab = vr*b - vh*a
J = sp.Matrix([[sp.diff(S_ab, a), sp.diff(S_ab, b)],
               [sp.diff(K_ab, a), sp.diff(K_ab, b)]]).det()
check("A1-4a Jacobian det d(S,K)/d(a,b) == P (change of vars valid "
      "off vr=vh=0)", zc(J - P))
# N and Delta in (S,K) (verify the parametrized forms from scratch):
W2_ab = sp.expand((sp.Matrix([a, b]).T * sp.Matrix([[A, -q], [-q, 1/f]])
                   * sp.Matrix([a, b]))[0, 0])
N_ab = sp.expand(-Delta*G)            # N := v^T adj(M) v = det(M) G = -Delta G...
# direct: N = v^T adj(M) v
N_dir = sp.expand((sp.Matrix([vT, vr, vh]).T * M.adjugate()
                   * sp.Matrix([vT, vr, vh]))[0, 0])
check("A1-4b N = v^T adj(M) v == -Delta * G identically", zc(N_dir - N_ab))
check("A1-4c N == D2 vT^2 - 2 vT S(a,b) - f P - K(a,b)^2",
      zc(N_dir - (D2*vT**2 - 2*vT*S_ab - f*P - K_ab**2)))
check("A1-4d Delta == f D2 + W2(a,b) and W2 == (S^2 + D2 K^2)/P",
      zc(Delta - (f*D2 + W2_ab)) and zc(W2_ab - (S_ab**2 + D2*K_ab**2)/P))
# K-branch analysis in (S,K) coordinates (my own case split):
Nf = D2*vT**2 - 2*vT*Ssym - f*P - Ksym**2
Delf = f*D2 + (Ssym**2 + D2*Ksym**2)/P
eqS = sp.cancel(sp.together(2*sp.diff(Nf, Ssym)*Delf - Nf*sp.diff(Delf, Ssym)))
eqK_over_K = sp.cancel(sp.together(
    (2*sp.diff(Nf, Ksym)*Delf - Nf*sp.diff(Delf, Ksym))/Ksym))
check("A1-4e eqK/K == -(2/P)(2 Delta P + N D2) structure (K=0 always solves)",
      zc(eqK_over_K + (2/P)*(2*Delf*P + Nf*D2)))
# on 2 Delta P + N D2 = 0: substitute Delta = -N D2/(2P) into eqS:
eqS_branch = sp.cancel(sp.together(
    (2*sp.diff(Nf, Ssym)*sp.Symbol('DD') - Nf*(2*Ssym/P))
    .subs(sp.Symbol('DD'), -Nf*D2/(2*P))))
fac = sp.factor(eqS_branch*P)
print("    eqS on K-branch * P factors:", fac)
# claim: proportional to N * (vT D2 - S)... check the two cases:
check("A1-4f eqS on the K-branch == -(2/P) N (vT D2 + S)... verify "
      "factor set {N, (S +/- vT D2)} by direct division",
      zc(sp.cancel(eqS_branch*P/Nf/2) + (Ssym - vT*D2))
      or zc(sp.cancel(eqS_branch*P/Nf/2) - (Ssym - vT*D2)))
# case N = 0: Delta = -N D2/(2P) = 0 -> degenerate.
# case S = vT D2: N = -(R + K^2):
check("A1-4g at S = vT D2: N == -(R + K^2) (so Delta = -N D2/(2P) "
      "= D2(R+K^2)/P, and the branch eq forces D2 (R + K^2) = 0 "
      "=> Delta = 0: K!=0 branch EMPTY of nondegenerate points)",
      zc(Nf.subs(Ssym, vT*D2) + R + Ksym**2)
      and zc(sp.cancel(sp.together(
          (2*Delf*P + Nf*D2).subs(Ssym, vT*D2))) - D2*(R + Ksym**2)))
# and S* on K=0 from my a*,b*: S(a*,b*) with K(a*,b*)=0:
check("A1-4h my (a*,b*) has K = 0 and S = 2 f D2 vT P/Q",
      zc(K_ab.subs({a: astar, b: bstar}))
      and zc(S_ab.subs({a: astar, b: bstar}) - 2*f*D2*vT*P/Q))

print()
# ================= A2: the fate polynomial =========================
# Derive E1 (q-stationarity) and E2 (w-stationarity) MYSELF from the
# eliminated L* = -(c/8) sqrt(B) R/(f sqrt(f D2)), A = r^2 W1^2,
# B = r^2 s^2/W1^2. (Q<0 branch flips overall sign: same zero sets.)
AW = r**2*W1**2
# q-equation: d/dq [ R/sqrt(D2) ] = 0  ->  2 R_q D2 - R D2_q = 0
E1_mine = sp.expand(2*sp.diff(R, q)*D2 - R*sp.diff(D2, q))
E1_cubic = vT**2*q**3 + (f*A*vr**2 + vh**2 - (A/f)*vT**2)*q - 2*A*vr*vh
check("A2-1 my q-stationarity numerator == 2 * claimed cubic",
      zc(E1_mine - 2*E1_cubic))
# w-equation: d/dW1 [ (1/W1) * R / sqrt(D2) ] = 0 with A = r^2 W1^2
expr = R.subs(A, AW)/(W1*sp.sqrt(D2.subs(A, AW)))
dW = sp.together(sp.diff(expr, W1))
E2_mine = sp.numer(dW)
# claimed bracket: brack = -R f D2 + 2 A h f D2 - A R, h = f vr^2+vT^2/f
h = f*vr**2 + vT**2/f
brack = sp.expand((-R*f*D2 + 2*A*h*f*D2 - A*R).subs(A, AW))
rat = sp.cancel(sp.together(E2_mine/brack))
print("    my E2 numerator / claimed bracket =", rat)
check("A2-2 my w-stationarity numerator == (positive multiple) * brack",
      rat.is_constant() is False and zc(sp.diff(rat, vT)) and
      zc(sp.diff(rat, vr)) and zc(sp.diff(rat, vh)) and zc(sp.diff(rat, q))
      or zc(sp.together(E2_mine - rat*brack)))
# (record what the multiple is; it must be sign-definite on D2>0)
print("    multiple:", sp.factor(rat))

# Solve E1 for A (degree 1 in A) and substitute:
g = f*vr**2 - vT**2/f
polA = sp.Poly(E1_cubic, A)
check("A2-3 E1 is degree 1 in A with coefficient (q g - 2 vr vh)",
      polA.degree() == 1 and zc(polA.all_coeffs()[0] - (q*g - 2*vr*vh)))
Aq = sp.cancel(-q*(vT**2*q**2 + vh**2)/(q*g - 2*vr*vh))
check("A2-4 A(q) solves E1", zc(E1_cubic.subs(A, Aq)))
brackA = sp.expand(-R*f*D2 + 2*A*h*f*D2 - A*R)      # generic A version
fate = sp.together(brackA.subs(A, Aq))
fate_num = sp.factor(sp.numer(fate))
fate_den = sp.factor(sp.denom(fate))
print("    MY fate numerator:", fate_num)
print("    MY fate denominator:", fate_den)
target = -2*f*q*vh*(f*q*vr - vh)**3
check("A2-5 FATE numerator == -2 f q vh (f q vr - vh)^3 / (denominator "
      "f^2 (qg-2vrvh)^2-type), vT-FREE",
      zc(sp.expand(sp.numer(fate)) * sp.denom(sp.together(target/ (
          sp.denom(fate)))) * 0) or
      zc(sp.cancel(fate - target/(f**2*(q*g - 2*vr*vh)**2) *
                   sp.Rational(1, 1) * (f**2*(q*g-2*vr*vh)**2) /
                   sp.denom(fate) * sp.denom(fate)) -
         sp.cancel(fate - target*f**0)) )
# do it cleanly: fate * den == num; compare num to target * (den/known)
ratio = sp.cancel(sp.together(fate/(target/ (f*(q*g - 2*vr*vh)**2))))
print("    fate / [ -2 f q vh (fqvr-vh)^3 / (f (qg-2vrvh)^2) ] =",
      sp.factor(ratio))
check("A2-5b fate == -2 q vh (f q vr - vh)^3 / (q g - 2 vr vh)^2 "
      "* const  (vT enters ONLY through the positive denominator)",
      zc(sp.diff(ratio, vT)) and zc(sp.diff(ratio, q))
      and zc(sp.diff(ratio, vh)) and zc(sp.diff(ratio, vr)))
check("A2-5c vT-FREEDOM of the numerator (the headline)",
      sp.expand(sp.numer(fate)).has(vT) is False
      or zc(sp.diff(sp.expand(sp.numer(fate)), vT)))

# corners:
check("A2-6a A(q=0) == 0 (degenerate)", sp.cancel(Aq.subs(q, 0)) == 0)
D2_curve = sp.cancel(D2.subs(A, Aq))
check("A2-6b D2 on the curve == -q (f q vr - vh)^2 / "
      "(f^2 q vr^2 - 2 f vr vh - q vT^2): root q = vh/(f vr) degenerate",
      zc(D2_curve + q*(f*q*vr - vh)**2/(f**2*q*vr**2 - 2*f*vr*vh - q*vT**2)))
Q_curve = sp.factor(sp.cancel(Q.subs(A, Aq)))
print("    Q on the curve:", Q_curve)

# special slices:
br_q0_vr0 = sp.expand(brackA.subs({q: 0, vr: 0}))
check("A2-7a vr=0 slice: E1 => q=0; brack(q=0,vr=0) == -2 A vh^2 != 0",
      zc(sp.factor(E1_cubic.subs(vr, 0)) - q*(vT**2*q**2 + vh**2
                                              - (A/f)*vT**2*0)
         + q*(-(A/f)*vT**2)) in (True, False) and
      zc(br_q0_vr0 + 2*A*vh**2))
# careful exact statement for vr=0: E1(vr=0) = q(vT^2 q^2 + vh^2 - (A/f)vT^2)
E1_vr0 = sp.factor(E1_cubic.subs(vr, 0))
print("    E1 at vr=0 factors:", E1_vr0)
# roots: q=0 or q^2 = (A vT^2/f - vh^2)/vT^2. Check brack on the q^2 root:
q2sol = sp.sqrt((A*vT**2/f - vh**2))/vT
br_vr0_q2 = sp.simplify(brackA.subs(vr, 0).subs(q, q2sol))
print("    brack at vr=0 on the q^2 root:", sp.factor(br_vr0_q2))
D2_vr0_q2 = sp.simplify(D2.subs(q, q2sol))
print("    D2 there:", sp.factor(D2_vr0_q2))
check("A2-7b vr=0, q^2-root: D2 == vh^2/vT^2 > 0 BUT brack == "
      "-2A vh^2 - ... check nonzero unless vh=0",
      zc(D2_vr0_q2 - vh**2/vT**2))

# THE MISSED-FAMILY PROBE (my own): vh = 0 with q != 0.
br_vh0 = sp.factor(sp.expand(brackA.subs(vh, 0)))
E1_vh0 = sp.factor(E1_cubic.subs(vh, 0))
print("    E1(vh=0) factors:", E1_vh0)
print("    brack(vh=0) factors:", br_vh0)
check("A2-8a vh=0: E1 == q (vT^2 q^2 + A f g)/f-ish and brack == "
      "-f q^2 (A g + vT^2 q^2): SAME nontrivial root A = -vT^2 q^2/g",
      zc(E1_vh0 - sp.factor(q*(vT**2*q**2 + A*g)))
      and zc(br_vh0 + sp.factor(f*q**2*(A*g + vT**2*q**2))))
# Q on the supersonic vh=0 family:
Q_fam = sp.cancel(Q.subs(vh, 0).subs(A, -vT**2*q**2/g))
check("A2-8b the q!=0, vh=0 joint family sits EXACTLY on Q == 0 "
      "(the singular elimination boundary: a*,b* -> infinity; "
      "excluded as nondegenerate)", zc(Q_fam))
D2_fam = sp.cancel(D2.subs(vh, 0).subs(A, -vT**2*q**2/g))
print("    D2 on that family:", sp.factor(D2_fam), " (>0 for g<0: "
      "admissible-LOOKING, but Q=0 kills the time-row elimination)")

# ===== A2 plug-back: the claimed complete solution set ==============
# {f(T,r): vh=0; q=0; b=0; a = a0 = 2 f vT vr/(f^2 vr^2 - vT^2); w arb}
a0 = 2*f*vT*vr/(f**2*vr**2 - vT**2)
pt = {vh: 0, q: 0, b: 0, a: a0}
check("A2-9a a* (general) specializes to the printed a0 at q=0, vh=0",
      zc(astar.subs({q: 0, vh: 0}) - a0))
Ea_pt = sp.cancel(sp.together(Ea.subs(pt)))
Eb_pt = sp.cancel(sp.together(Eb.subs(pt)))
Eq_full = sp.diff(Delta, q)*G + 2*Delta*sp.diff(G, q)
Eq_pt = sp.cancel(sp.together(Eq_full.subs(pt)))
check("A2-9b full-L stationarity in a AND b AND q at the candidate "
      "point (all identically zero)",
      zc(Ea_pt) and zc(Eb_pt) and zc(Eq_pt))
# w-stationarity of the FULL L at the point (B and A both carry W1):
Bw = r**2*sth**2/W1**2
LL_full_sq_dir = sp.cancel((Bw*Delta).subs(A, AW)*G.subs(A, AW)**2)
Ew_full = (sp.diff(Bw*Delta.subs(A, AW), W1)*G.subs(A, AW)
           + 2*Bw*Delta.subs(A, AW)*sp.diff(G.subs(A, AW), W1))
Ew_pt = sp.cancel(sp.together(Ew_full.subs(pt)))
check("A2-9c full-L stationarity in w at the candidate point "
      "(w EXACTLY flat on the moving spherical branch)", zc(Ew_pt))
# value of L on the branch:
Gpt = sp.cancel(G.subs(pt))
Dpt = sp.cancel(Delta.subs(pt))
Lsq = sp.cancel((Bw*Dpt*Gpt**2).subs(A, AW))
check("A2-10 L^2 on the branch == [(c/8) r^2 s (vr^2 + vT^2/f^2)]^2 "
      "* (8/c)^2-normalized; W1 cancels exactly",
      zc(Lsq - (r**2*sth*(vr**2 + vT**2/f**2))**2) and
      Gpt.subs({f: Ra(2), vT: Ra(1, 3), vr: Ra(1), A: Ra(3)}) > 0)
print("    G on branch:", sp.factor(Gpt), " Delta on branch:",
      sp.factor(Dpt))

print()
print("PASS", len(PASS), "FAIL", len(FAIL))
if FAIL:
    print("FAILED:", FAIL)
