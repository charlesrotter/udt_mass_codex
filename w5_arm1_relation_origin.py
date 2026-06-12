"""W5 ARM-1 (UNCOVER) — SCRIPT 1: THE -2/f RELATION, ITS ORIGIN, AND THE
FULL q=0 EL MAP OF THE SPECIES.

Date: 2026-06-12.  W5 ARM-1 agent.  Declaration: W5 section of
w_stiffness_push_declaration.md (binding; uncovering verbs only).

CONTEXT (VA4, two routes, q=0 class):
    E_w[sqrt(-g) R] = EL_w[W_wave] + sin(th) f_th^2/((1+w)^3 f^2)
                    = EL_w[W_wave] - (2/f) dL_C1/dw          (exact)

TASKS HERE:
  T1a. THIRD independent route to the relation (neither of VA4's two):
       Gamma-Gamma split + first-order EL on the BULK L_GG, with the
       EL-invisibility of div V checked separately.  VA4 route 1 was
       the Einstein-tensor variational identity on the full density;
       VA4 route 2 was sympy euler_equations on the full density.
       This route never touches the full density's EL.
  T1b. ORIGIN: localize the species' algebraic w-content slot-by-slot
       (which f-jet quadratic carries it); test the WEIGHT-STRIPPING
       reading (the species' algebraic w-channel = C1's angular density
       with the postulate weight e^{-2phi} replaced by the curvature's
       native weight -2 e^{0}; ratio = -2 e^{2phi} = -2/f); then probe
       what the "-2" tracks by DEFORMING THE TIE: g_TT = -f^a,
       g_rr = f^b (postulate point a=1, b=-1) and extracting the exact
       tadpole polynomial P(a,b).
  T1c. FULL EL MAP of the species' w-content on the q=0 class:
       E_f[Delta_w species] exactly (macro gate at fluctuation order;
       the exact second-order sources the species feeds the
       spherical/macro sector; w_thth content or its absence; the
       (1-f)/w_thth pairing question in the f-channel at q=0).

PRE-STATED FAILURE CRITERIA (committed before computation):
  F1: if the third route does NOT reproduce VA4's relation exactly,
      the W5 premise is broken — STOP, report, nothing downstream.
  F2: if the species' algebraic w-content does NOT localize in the
      f_th^2 slot (spreads over f_r^2 / f_r f_th / jet-free slots),
      the weight-stripping origin DIES — record the death; the -2/f
      stays an unexplained ratio.
  F3: if the tie-deformation polynomial P(a,b) has no structural
      reading (not a small-rational combination in which the
      postulate point is distinguished), the "postulate-structural"
      origin reading is NOT banked (negative, scoped to this probe
      family: power-law tie deformations g_TT=-f^a, g_rr=f^b).
  F4: if E_f[Delta_w] fails to vanish identically at w == 0, the P4
      macro gate is broken for the UNTRUNCATED system — first-class
      negative, report immediately.

Method: exact sympy on CPU; no linearization; jet-symbol EL machinery
(own implementation, modeled on w2_arm1_verifier_l4.py's — the full-EL
trap is on record); exact rational spot checks (Weierstrass-
rationalized theta) wherever full symbolic cancel is too heavy, with
the method note recorded.  New file.  Log: /tmp/w5_arm1_s1.log
"""
import random
import time
import sympy as sp
from sympy import Rational as Ra

random.seed(20260612)
t0 = time.time()
PASS, FAIL = [], []


def check(label, ok):
    ok = bool(ok)
    (PASS if ok else FAIL).append(label)
    print(("PASS" if ok else "FAIL"), label, flush=True)
    assert ok, "FAILED: " + label


T, r, th, ph = sp.symbols('T r theta varphi', real=True)
coords3 = [T, r, th]

f = sp.Function('f')(T, r, th)
w = sp.Function('w')(T, r, th)


# ------------------------------------------------------------ geometry engine
def christoffel(g, xs):
    n = len(xs)
    ginv = g.inv()
    Gam = [[[sp.S(0)] * n for _ in range(n)] for _ in range(n)]
    for aa in range(n):
        for i in range(n):
            for j in range(i, n):
                e = sp.S(0)
                for k in range(n):
                    e += ginv[aa, k] * (sp.diff(g[k, i], xs[j])
                                        + sp.diff(g[k, j], xs[i])
                                        - sp.diff(g[i, j], xs[k]))
                Gam[aa][i][j] = Gam[aa][j][i] = sp.together(e / 2)
    return Gam, ginv


def ricci(g, xs):
    n = len(xs)
    Gam, ginv = christoffel(g, xs)
    Ric = sp.zeros(n, n)
    for i in range(n):
        for j in range(i, n):
            e = sp.S(0)
            for aa in range(n):
                e += sp.diff(Gam[aa][i][j], xs[aa])
                e -= sp.diff(Gam[aa][i][aa], xs[j])
                for bb in range(n):
                    e += Gam[aa][aa][bb] * Gam[bb][i][j]
                    e -= Gam[aa][j][bb] * Gam[bb][i][aa]
            Ric[i, j] = Ric[j, i] = e
    Rsc = sp.S(0)
    for i in range(n):
        for j in range(n):
            Rsc += ginv[i, j] * Ric[i, j]
    return Rsc, Ric, ginv, Gam


def gammagamma_split(g, xs, sq):
    n = len(xs)
    Gam, ginv = christoffel(g, xs)
    V = []
    for cc in range(n):
        e = sp.S(0)
        for aa in range(n):
            for bb in range(n):
                e += ginv[aa, bb] * Gam[cc][aa][bb]
                e -= ginv[cc, bb] * Gam[aa][aa][bb]
        V.append(sq * e)
    LGG = sp.S(0)
    for aa in range(n):
        for bb in range(n):
            for cc in range(n):
                for dd in range(n):
                    LGG += ginv[aa, bb] * (
                        Gam[cc][aa][dd] * Gam[dd][bb][cc]
                        - Gam[cc][aa][bb] * Gam[dd][dd][cc])
    return sq * LGG, V


# ------------------------------------------------------ jet-symbol machinery
JET = {}


def jsym(name, mi):
    mi = tuple(sorted(mi))
    key = (name, mi)
    if key not in JET:
        tag = ''.join('Trh'[i] for i in mi)
        JET[key] = sp.Symbol(name + ('_' + tag if tag else ''), real=True)
    return JET[key]


FMAP = {f: 'f', w: 'w'}


def to_jets(expr):
    dmap = {}
    for d in expr.atoms(sp.Derivative):
        if d.expr in FMAP:
            mi = []
            for v, k in d.variable_count:
                mi += [coords3.index(v)] * int(k)
            dmap[d] = jsym(FMAP[d.expr], tuple(mi))
    fmap = {F: jsym(nm, ()) for F, nm in FMAP.items()}
    return expr.subs(dmap).subs(fmap)


def Dtot(expr, i):
    out = sp.diff(expr, coords3[i])
    for (name, mi), s in list(JET.items()):
        if expr.has(s):
            out += sp.diff(expr, s) * jsym(name, mi + (i,))
    return out


def EL_first(L, name):
    """EL of a FIRST-jet density (L_GG is first-jet in every field)."""
    res = sp.diff(L, jsym(name, ()))
    for i in range(3):
        res -= Dtot(sp.diff(L, jsym(name, (i,))), i)
    return res


tpar = sp.Symbol('t_w', real=True)


def rational_points(expr, npts=5):
    e = expr.subs({sp.sin(th): 2 * tpar / (1 + tpar**2),
                   sp.cos(th): (1 - tpar**2) / (1 + tpar**2)})
    syms = sorted(e.free_symbols, key=str)
    vals = []
    for _ in range(npts):
        sub = {}
        for s in syms:
            if s == r:
                sub[s] = Ra(random.randint(2, 9), random.randint(1, 5))
            elif s == tpar:
                sub[s] = Ra(random.randint(1, 7), random.randint(2, 9))
            elif str(s) == 'f':
                sub[s] = Ra(random.randint(1, 9), random.randint(1, 4))
            elif str(s) == 'w':
                sub[s] = Ra(random.randint(-2, 6), 7)  # hostile: w < 0
            else:
                sub[s] = Ra(random.randint(-9, 9), random.randint(1, 7))
        vals.append(sp.cancel(e.subs(sub)))
    return vals


def is_zero_rp(expr, npts=5):
    return all(v == 0 for v in rational_points(expr, npts))


# =====================================================================
print("=" * 72)
print("PART 0 — ENGINE SANITY")
print("=" * 72)
m_ = sp.Symbol('m', positive=True)
gS = sp.diag(-(1 - 2 * m_ / r), 1 / (1 - 2 * m_ / r), r**2,
             r**2 * sp.sin(th)**2)
RS, RicS, _, _ = ricci(gS, [T, r, th, ph])
check("S1-00 engine sanity: Schwarzschild R == 0 and Ricci == 0 "
      "(own Christoffel/Ricci)",
      sp.simplify(RS) == 0
      and all(sp.simplify(RicS[i, j]) == 0
              for i in range(4) for j in range(4)))

# =====================================================================
print()
print("=" * 72)
print("PART 1 — T1a: THIRD ROUTE TO THE RELATION (Gamma-Gamma bulk EL)")
print("=" * 72)
A = r**2 * (1 + w)**2
B = r**2 * sp.sin(th)**2 / (1 + w)**2
g4 = sp.diag(-f, 1 / f, A, B)
sq = r**2 * sp.sin(th)          # sqrt(-g) = r^2 sin th exactly at q=0
check("S1-01 sqrt(-g) on the q=0 class is r^2 sin th exactly "
      "(w-free, f-free)",
      sp.cancel(-g4.det() - (r**2 * sp.sin(th))**2) == 0)

print("   [building Gamma-Gamma split on the full time-on q=0 class...]",
      flush=True)
LGG, V = gammagamma_split(g4, [T, r, th, ph], sq)
LGGj = to_jets(sp.expand(LGG))

# my own EL of the bulk (first-jet density -> first-order EL is the
# FULL EL; no Route-B trap possible here, and the trap-audit is the
# div-V invisibility check below):
ELw_bulk = EL_first(LGGj, 'w')

# targets, built independently from the banked closed forms:
fj, wj = jsym('f', ()), jsym('w', ())
fT, fr_, fth = jsym('f', (0,)), jsym('f', (1,)), jsym('f', (2,))
wT, wr, wth = jsym('w', (0,)), jsym('w', (1,)), jsym('w', (2,))
L_Wwave = (2 * r**2 * sp.sin(th) / (1 + wj)**2) * (wT**2 / fj
                                                   - fj * wr**2)
ELw_Wwave = EL_first(L_Wwave, 'w')
# C1 (positive banked convention c = 2), q=0 time-on class:
L_C1 = (Ra(1, 4) * sp.sin(th) * (r**2 * fr_**2
                                 + fth**2 / (fj * (1 + wj)**2))
        - Ra(1, 4) * r**2 * sp.sin(th) * fT**2 / fj**2)
dLC1_dw = sp.diff(L_C1, wj)
check("S1-02 C1 w-tadpole (banked): dL_C1/dw = "
      "-(1/2) sin f_th^2/(f(1+w)^3), w-jet-free",
      sp.cancel(dLC1_dw + Ra(1, 2) * sp.sin(th) * fth**2
                / (fj * (1 + wj)**3)) == 0)

rel_resid = sp.expand(ELw_bulk - (ELw_Wwave - (2 / fj) * dLC1_dw))
rel_resid_c = sp.cancel(sp.together(rel_resid))
check("S1-03 THIRD ROUTE (F1 bar): EL_w[L_GG] = EL_w[W_wave] "
      "- (2/f) dL_C1/dw IDENTICALLY on the full q=0 time-on class "
      "(symbolic cancellation; route: Gamma-Gamma bulk + first-order "
      "EL — neither of VA4's two routes)",
      rel_resid_c == 0)

# EL-invisibility of div V under the w-EL (completes the route):
divV = sum(sp.diff(V[i], x) for i, x in enumerate([T, r, th, ph]))
divVj = to_jets(sp.expand(divV))
# divV is second-jet; full second-order EL needed for the invisibility:
def EL_second(L, name):
    res = sp.diff(L, jsym(name, ()))
    for i in range(3):
        res -= Dtot(sp.diff(L, jsym(name, (i,))), i)
    for i in range(3):
        for j in range(i, 3):
            c = sp.diff(L, jsym(name, tuple(sorted((i, j)))))
            if c != 0:
                res += Dtot(Dtot(c, i), j)
    return res


ELw_divV = EL_second(divVj, 'w')
check("S1-04 EL_w[div V] == 0 under the FULL second-order EL operator "
      "(exact rational identity test, 5 hostile points incl. w<0): "
      "the bulk EL in S1-03 IS the species' w-EL",
      is_zero_rp(ELw_divV, 5))

# =====================================================================
print()
print("=" * 72)
print("PART 2 — T1b ORIGIN (i): SLOT LOCALIZATION")
print("=" * 72)
# the bulk at zero w-jets: which f-jet quadratic slots carry w?
LGG_alg = LGGj.subs({wT: 0, wr: 0, wth: 0})
slots = {
    'f_T^2': sp.cancel(sp.diff(LGG_alg, fT, 2) / 2),
    'f_r^2': sp.cancel(sp.diff(LGG_alg, fr_, 2) / 2),
    'f_th^2': sp.cancel(sp.diff(LGG_alg, fth, 2) / 2),
    'f_T f_r': sp.cancel(sp.diff(sp.diff(LGG_alg, fT), fr_)),
    'f_T f_th': sp.cancel(sp.diff(sp.diff(LGG_alg, fT), fth)),
    'f_r f_th': sp.cancel(sp.diff(sp.diff(LGG_alg, fr_), fth)),
    'f_T lin': sp.cancel(sp.diff(LGG_alg, fT).subs(
        {fT: 0, fr_: 0, fth: 0})),
    'f_r lin': sp.cancel(sp.diff(LGG_alg, fr_).subs(
        {fT: 0, fr_: 0, fth: 0})),
    'f_th lin': sp.cancel(sp.diff(LGG_alg, fth).subs(
        {fT: 0, fr_: 0, fth: 0})),
    'jet-free': sp.cancel(LGG_alg.subs({fT: 0, fr_: 0, fth: 0})),
}
print("   bulk algebraic slots (zero w-jets) and their w-derivatives:")
wdeps = {}
for k, v in slots.items():
    dv = sp.cancel(sp.diff(v, wj))
    wdeps[k] = dv
    print(f"     d/dw coeff[{k}] = {sp.simplify(dv)}")
others_dead = all(wdeps[k] == 0 for k in wdeps if k != 'f_th^2')
check("S1-05 LOCALIZATION (F2 bar): the species' algebraic w-content "
      "lives ENTIRELY in the f_th^2 slot — d/dw of every other slot "
      "(f_T^2, f_r^2, all crosses, all linears, jet-free) vanishes "
      "identically", others_dead and wdeps['f_th^2'] != 0)
check("S1-06 the f_th^2 slot's exact value: coeff[f_th^2] of the bulk "
      "at zero w-jets = -sin(th)/(2 f^2 (1+w)^2) + w-free? — computed: "
      "its w-DEPENDENT part is exactly -sin/(2f^2)(1/(1+w)^2 - 1)",
      sp.cancel(slots['f_th^2'] - slots['f_th^2'].subs(wj, 0)
                + sp.sin(th) / (2 * fj**2)
                * (1 / (1 + wj)**2 - 1)) == 0)

print()
print("=" * 72)
print("PART 2 — T1b ORIGIN (ii): WEIGHT-STRIPPING IDENTITY")
print("=" * 72)
# C1's angular density piece (postulate weight e^{-2phi} = f):
L_C1_ang = Ra(1, 4) * sp.sin(th) * fth**2 / (fj * (1 + wj)**2)
# the claim: species' algebraic w-channel = -2 e^{2phi} x C1's, i.e.
#   LGG_alg(w) - LGG_alg(0) = -(2/f) [L_C1_ang(w) - L_C1_ang(0)]
lhs = sp.cancel(LGG_alg - LGG_alg.subs(wj, 0))
rhs = sp.cancel(-(2 / fj) * (L_C1_ang - L_C1_ang.subs(wj, 0)))
check("S1-07 WEIGHT-STRIPPING (exact, all w): LGG_alg(w) - LGG_alg(0) "
      "= -(2/f)[L_C1_ang(w) - L_C1_ang(0)] — the species' algebraic "
      "w-channel IS C1's angular density times -2 e^{2phi}: the "
      "postulate weight e^{-2phi} stripped, replaced by the curvature "
      "scalar's native weight -2 e^{0}",
      sp.cancel(lhs - rhs) == 0)
# the -2 (nabla phi)^2 reading: -2 sqrt(-g) g^{thth} phi_th^2 has
# exactly the species slot's w-dependent f_th^2 coefficient:
phi_th = -fth / (2 * fj)
term = -2 * sq * (1 / (r**2 * (1 + wj)**2)) * phi_th**2
check("S1-08 the -2(grad phi)^2 reading: -2 sqrt(-g) g^{thth} phi_th^2 "
      "= -sin f_th^2/(2 f^2 (1+w)^2), whose w-dependent part equals the "
      "species' algebraic w-content EXACTLY; C1's same slot is "
      "+e^{-2phi} sqrt(-g) g^{thth} phi_th^2 — RATIO = -2 e^{2phi} "
      "= -2/f at every point",
      sp.cancel(term + sp.sin(th) * fth**2 / (2 * fj**2 * (1 + wj)**2))
      == 0
      and sp.cancel((term - term.subs(wj, 0)) - lhs) == 0
      and sp.cancel(term / (fj * sq * (1 / (r**2 * (1 + wj)**2))
                            * phi_th**2) + 2 / fj) == 0)

# =====================================================================
print()
print("=" * 72)
print("PART 3 — T1b ORIGIN (iii): TIE DEFORMATION g_TT=-f^a, g_rr=f^b")
print("=" * 72)
# STATIC class (the tadpole carries no f_T); exponents symbolic.
a_, b_ = sp.symbols('a b', real=True)
fs = sp.Function('f')(r, th)
ws = sp.Function('w')(r, th)
g_def = sp.diag(-fs**a_, fs**b_, r**2 * (1 + ws)**2,
                r**2 * sp.sin(th)**2 / (1 + ws)**2)
print("   [Ricci on the deformed-tie static class (symbolic a, b)...]",
      flush=True)
R_def, Ric_def, gi_def, _ = ricci(g_def, [T, r, th, ph])
sq_def = fs**((a_ + b_) / 2) * r**2 * sp.sin(th)
check("S1-09 deformed-tie determinant: sqrt(-g) = f^{(a+b)/2} r^2 sin",
      sp.simplify(sp.powsimp(-g_def.det() - sq_def**2,
                             force=True)) == 0)
# Einstein-tensor variational route for E_w (algebraic part):
Rup22 = sum(gi_def[2, k] * gi_def[2, l] * Ric_def[k, l]
            for k in range(4) for l in range(4))
Rup33 = sum(gi_def[3, k] * gi_def[3, l] * Ric_def[k, l]
            for k in range(4) for l in range(4))
G22 = Rup22 - gi_def[2, 2] * R_def / 2
G33 = Rup33 - gi_def[3, 3] * R_def / 2
dg22 = 2 * r**2 * (1 + ws)
dg33 = -2 * r**2 * sp.sin(th)**2 / (1 + ws)**3
Ew_def = -sq_def * (G22 * dg22 + G33 * dg33)
# algebraic part: kill all w-jets:
Ew_alg = Ew_def
for d in (sp.Derivative(ws, (r, 2)), sp.Derivative(ws, (th, 2)),
          sp.Derivative(ws, r, th), sp.Derivative(ws, r),
          sp.Derivative(ws, th)):
    Ew_alg = Ew_alg.subs(d, 0)
Ew_alg = sp.expand(sp.cancel(sp.together(Ew_alg)))
# the tadpole is the f_th^2-sourced part; extract coefficient structure.
fth_d = sp.Derivative(fs, th)
fr_d = sp.Derivative(fs, r)
fthth_d = sp.Derivative(fs, (th, 2))
frr_d = sp.Derivative(fs, (r, 2))
frth_d = sp.Derivative(fs, r, th)
c_fth2 = sp.cancel(sp.diff(Ew_alg, fth_d, 2) / 2)
# all OTHER slots of the algebraic w-EL must vanish (they do at a=1,
# b=-1 by VA4; here we LOOK at general (a,b)):
others = {
    'f_r^2': sp.cancel(sp.diff(Ew_alg, fr_d, 2) / 2),
    'f_r f_th': sp.cancel(sp.diff(sp.diff(Ew_alg, fr_d), fth_d)),
    'f_thth': sp.cancel(sp.diff(Ew_alg, fthth_d)),
    'f_rr': sp.cancel(sp.diff(Ew_alg, frr_d)),
    'f_rth': sp.cancel(sp.diff(Ew_alg, frth_d)),
    'jet-free': sp.cancel(Ew_alg.subs([(fth_d, 0), (fr_d, 0),
                                       (fthth_d, 0), (frr_d, 0),
                                       (frth_d, 0)])),
}
print("   deformed-tie algebraic w-EL, slot census:")
for k, v in others.items():
    vs = sp.simplify(v)
    print(f"     [{k}] = {vs}")
print(f"     [f_th^2] = {sp.simplify(c_fth2)}", flush=True)
# P(a,b): normalize by the a=1,b=-1 value's structure:
#   c_fth2 = sin/( (1+w)^3 ) * f^{(a+b)/2 - 2} * P(a,b) ?  EXTRACT:
P_ab = sp.cancel(sp.simplify(
    c_fth2 / (sp.sin(th) * fs**((a_ + b_) / 2 - 2) / (1 + ws)**3)))
print("   P(a,b) =", sp.simplify(sp.expand(P_ab)), flush=True)
P_post = sp.simplify(P_ab.subs([(a_, 1), (b_, -1)]))
check("S1-10 deformed-tie tadpole: at the postulate point (a,b)=(1,-1) "
      "the f_th^2 slot reproduces the species tadpole "
      "+sin f_th^2/((1+w)^3 f^2) exactly  [P(1,-1) = 1]",
      sp.simplify(P_post - 1) == 0)
# structural reading test (F3 bar): is P(a,b) a small-rational
# polynomial?  print it; the adjudication is recorded in the verdict.
P_poly = sp.Poly(sp.expand(P_ab), a_, b_) \
    if sp.expand(P_ab).is_polynomial(a_, b_) else None
check("S1-11 P(a,b) is a POLYNOMIAL in the tie exponents (degree <= 2) "
      "— printed above for the origin adjudication; w-independence of "
      "P also checked",
      P_poly is not None and sp.total_degree(P_poly.as_expr(), a_, b_) <= 2
      and ws not in P_ab.free_symbols)
# does the localization itself survive deformation? (the other slots
# need not vanish off the postulate point — report what is there):
others_at_post = {k: sp.simplify(v.subs([(a_, 1), (b_, -1)]))
                  for k, v in others.items()}
check("S1-12 at the postulate point every non-f_th^2 slot of the "
      "algebraic w-EL vanishes (re-derives VA4's tadpole shape on the "
      "deformed engine — engine cross-check)",
      all(v == 0 for v in others_at_post.values()))
off_alive = any(sp.simplify(v) != 0 for v in others.values())
print(f"   off-postulate slots alive: {off_alive}  (reported, "
      "adjudicated in verdict)")

# =====================================================================
print()
print("=" * 72)
print("PART 4 — T1c: FULL EL MAP — E_f[species w-content] at q=0")
print("=" * 72)
# Delta_w species (EL-grade representative): the bulk's w-content
Delta = sp.expand(LGGj - LGGj.subs({wT: 0, wr: 0, wth: 0, wj: 0}))
ELf_D = EL_first(Delta, 'f')
ELf_D = sp.expand(ELf_D)
# F4 bar: vanish identically at w == 0 (all w-jets and w zero):
ELf_D_w0 = ELf_D
for s_ in [jsym('w', mi) for (nm, mi) in list(JET.keys()) if nm == 'w']:
    ELf_D_w0 = ELf_D_w0.subs(s_, 0)
check("S1-13 MACRO GATE, untruncated (F4 bar): E_f[Delta_w species] "
      "== 0 IDENTICALLY at w == 0 (any f, both signs of nothing — "
      "symbolic): the full species cannot touch the spherical/macro "
      "sector at fluctuation order zero or one",
      sp.simplify(ELf_D_w0) == 0)
# the exact structure: linear-in-w part (the species' first-order
# back-reaction channel into the f-equation):
lin_w = sp.expand(sp.diff(ELf_D, wj).subs(
    {wj: 0, wT: 0, wr: 0, wth: 0,
     jsym('w', (0, 0)): 0, jsym('w', (1, 1)): 0, jsym('w', (2, 2)): 0,
     jsym('w', (0, 1)): 0, jsym('w', (0, 2)): 0, jsym('w', (1, 2)): 0}))
lin_w = sp.cancel(sp.together(lin_w))
print("   d E_f[Delta]/dw at w=0 (the O(w) f-source) =")
print("     ", sp.simplify(lin_w), flush=True)
# w-jet-linear parts:
lin_jets = {}
for nm, s_ in (('w_T', wT), ('w_r', wr), ('w_th', wth),
               ('w_TT', jsym('w', (0, 0))), ('w_rr', jsym('w', (1, 1))),
               ('w_thth', jsym('w', (2, 2))),
               ('w_Tr', jsym('w', (0, 1))), ('w_Tth', jsym('w', (0, 2))),
               ('w_rth', jsym('w', (1, 2)))):
    v = sp.diff(ELf_D, s_)
    for s2 in [jsym('w', mi) for (n2, mi) in list(JET.keys())
               if n2 == 'w']:
        v = v.subs(s2, 0)
    lin_jets[nm] = sp.cancel(sp.together(v))
for nm, v in lin_jets.items():
    print(f"   d E_f[Delta]/d{nm} at w=0 = {sp.simplify(v)}")
check("S1-14 E_f MAP: at q=0 the species feeds the f-equation NO w "
      "second jets at linearized order (coeff[w_TT] = coeff[w_rr] = "
      "coeff[w_thth] = crosses = 0 at w=0) — the f-channel cannot see "
      "w_thth at q=0: the W2 pairing [(1-f)+4 w_thth] has NO q=0 "
      "dynamical channel through the f-equation at first order",
      all(lin_jets[k] == 0 for k in
          ('w_TT', 'w_rr', 'w_thth', 'w_Tr', 'w_Tth', 'w_rth')))
# the exact O(w) source content (algebraic w x f-jets):
tgt_linw = (sp.sin(th) / fj**2
            * (2 * fj * jsym('f', (2, 2)) - 3 * fth**2)
            + sp.sin(th) * sp.cos(th) * 2 * fth / fj) / 1
# do not guess: just record nonzeroness and f_th^2-proportionality
check("S1-15 the species' O(w) f-source is NONZERO and shaped-only "
      "(every term carries f_th, f_thth or w-jets; it vanishes "
      "identically when f_th == f_thth == 0): second-order "
      "back-reaction touches ONLY shaped cells",
      sp.simplify(lin_w) != 0
      and sp.simplify(lin_w.subs([(fth, 0), (jsym('f', (2, 2)), 0),
                                  (jsym('f', (0, 2)), 0),
                                  (jsym('f', (1, 2)), 0)])) == 0)
# spherical-f restriction of the FULL E_f[Delta] (all w on): the wave
# stress terms (what a ringing w does to a spherical macro f):
sph_sub = [(fth, 0), (jsym('f', (2, 2)), 0), (jsym('f', (0, 2)), 0),
           (jsym('f', (1, 2)), 0)]
ELf_sph = sp.cancel(sp.together(ELf_D.subs(sph_sub)))
print("   E_f[Delta] on spherical f (full w):")
print("     ", sp.simplify(ELf_sph), flush=True)
# the W4-known wave stress is dL_Wwave/df (L_Wwave is f-jet-free, so
# its E_f is the bare partial); on spherical f the species must add
# nothing beyond it (the algebraic channel is f_th^2-locked):
tgt_sph = sp.diff(L_Wwave, fj)
check("S1-16 on spherical f the species' E_f content is EXACTLY "
      "dL_Wwave/df = -2 r^2 sin [w_r^2 + w_T^2/f^2]/(1+w)^2 — the "
      "UNTRUNCATED species adds NO new spherical-f source beyond the "
      "W4-known wave stress (the algebraic species channel is "
      "f_th^2-locked in the f-equation too)",
      sp.cancel(sp.together(ELf_sph - tgt_sph)) == 0)

print()
print(f"TOTALS: {len(PASS)} PASS / {len(FAIL)} FAIL "
      f"({time.time()-t0:.0f}s)")
assert not FAIL
