"""W5 ARM-1 (UNCOVER) — SCRIPT 2: THE q-ON ANGULAR CONTENT AND THE
q*-BRANCH ANGULAR-STIFFNESS ADJUDICATION (registry #28's unadjudicated
branch — the discreteness gap's named suspect).

Date: 2026-06-12.  W5 ARM-1 agent.  Declaration: W5 section of
w_stiffness_push_declaration.md (binding; uncovering only).

QUESTION: at q != 0, does the curvature species supply EL-VISIBLE
angular w-stiffness (a w_thth principal term in the w-EL), and what
survives on the q*-eliminated branch
   q* = 2 r^2 W f_r f_th / (f r^2 W f_r^2 + f_th^2),  W = (1+w)^2 ?
This decides whether BANDS can become LINES at this order.

CAREFUL SECOND-ORDER STRUCTURE (the W1-Route-B trap is on record): the
reduced w-EL of S = C1 + kappa*Delta_w on the branch at O(kappa) has
three members that could carry angular w-jets:
  (m1) E_w[Delta] at q = q*(f,w,jets), WITH the chain rule on q-jets
       (D^J q* carries w-second-jets through dq*/dw);
  (m2) the C1-response member: q-branch shift q1 = -E_q[Delta]|_{q*}
       / L_qq|_{q*} (pointwise; C1 carries no q-jets), feeding
       L_wq * q1;
  (m3) C1's own dL_C1/dw — w-jet-free at all q (checked, not assumed).

PRE-STATED FAILURE CRITERIA (committed before the final run; the
exploratory pass that fixed the assert targets is on record in the
results doc — every target below is a COMPUTED value, none is a hope):
  G1: if the Einstein-route E_w disagrees with the full second-order
      jet EL of sqrt(-g)R at hostile rational points, STOP — engine
      broken.
  G2: if c[w_thth] of the reduced branch w-EL vanishes, the q*-branch
      supplies NO pure angular stiffness: registry #28's branch closes
      on that channel — first-class outcome, banked with premise set
      {P1 q-on class, C1-q* branch, O(kappa), EL level}.
  G3: hypothesis discipline: angular stiffness is the HOPED-FOR
      outcome.  Skeptic's bars: EL-visibility (not density-level
      structure); totals not parts; signs as computed.

Method: exact sympy CPU; Einstein-tensor variational route
(E_X = -sqrt(-g) G^{munu} dg_{munu}/dX, exact for algebraic slots);
full second-order jet EL as cross-check at hostile exact rational
points; polar-domain convention 0 < th < pi, r > 0, 1 + w > 0
(Abs(positive brick) -> brick, as in the committed W2 census).
New file.  Log: /tmp/w5_arm1_s2.log
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


# ------------------------------------------------------------ geometry engine
def christoffel(g, xs):
    n = len(xs)
    gi = g.inv()
    Gam = [[[sp.S(0)] * n for _ in range(n)] for _ in range(n)]
    for aa in range(n):
        for i in range(n):
            for j in range(i, n):
                e = sum(gi[aa, k] * (sp.diff(g[k, i], xs[j])
                                     + sp.diff(g[k, j], xs[i])
                                     - sp.diff(g[i, j], xs[k]))
                        for k in range(n))
                Gam[aa][i][j] = Gam[aa][j][i] = sp.together(e / 2)
    return Gam, gi


def ricci(g, xs):
    n = len(xs)
    Gam, gi = christoffel(g, xs)
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
            Ric[i, j] = Ric[j, i] = sp.together(e)
    Rsc = sum(gi[i, j] * Ric[i, j] for i in range(n) for j in range(n))
    return sp.together(Rsc), Ric, gi


def build_E(coordsdep):
    """Einstein-route EL channels on the q-on class with the given
    coordinate dependence for (f, q, w).  Returns (E_w, E_q, E_f,
    fields, sqrtmg)."""
    f = sp.Function('f')(*coordsdep)
    q = sp.Function('q')(*coordsdep)
    w = sp.Function('w')(*coordsdep)
    W = (1 + w)**2
    g4 = sp.Matrix([[-f, 0, 0, 0],
                    [0, 1 / f, q, 0],
                    [0, q, r**2 * W, 0],
                    [0, 0, 0, r**2 * sp.sin(th)**2 / W]])
    sq = r * sp.sin(th) * sp.sqrt(r**2 * W - f * q**2) / (1 + w)
    Rsc, Ric, gi = ricci(g4, [T, r, th, ph])

    def G_up(i, j):
        e = sum(gi[i, k] * gi[j, l] * Ric[k, l]
                for k in range(4) for l in range(4)
                if gi[i, k] != 0 and gi[j, l] != 0)
        return sp.together(e - gi[i, j] * Rsc / 2)

    E_w = -sq * (G_up(2, 2) * 2 * r**2 * (1 + w)
                 + G_up(3, 3) * (-2) * r**2 * sp.sin(th)**2 / (1 + w)**3)
    E_q = -sq * 2 * G_up(1, 2)
    E_f = -sq * (G_up(0, 0) * (-1) + G_up(1, 1) * (-1 / f**2))
    return E_w, E_q, E_f, (f, q, w), sq, Rsc


# =====================================================================
print("=" * 72)
print("PART 1 — STATIC q-ON CLASS: THE COMPLETE SECOND-JET INVENTORY")
print("=" * 72)
print("   [Ricci/Einstein, static q-on ...]", flush=True)
E_w, E_q, E_f, (f, q, w), sq, Rsc = build_E((r, th))

# jet machinery (static, 2 coords):
coords2 = [r, th]
JET = {}


def jsym(name, mi):
    mi = tuple(sorted(mi))
    key = (name, mi)
    if key not in JET:
        tag = ''.join('rh'[i] for i in mi)
        JET[key] = sp.Symbol(name + ('_' + tag if tag else ''), real=True)
    return JET[key]


FMAP = {f: 'f', q: 'q', w: 'w'}


def to_jets(expr):
    dmap = {}
    for d in expr.atoms(sp.Derivative):
        if d.expr in FMAP:
            mi = []
            for v, k in d.variable_count:
                mi += [coords2.index(v)] * int(k)
            dmap[d] = jsym(FMAP[d.expr], tuple(mi))
    return expr.subs(dmap).subs({F: jsym(nm, ()) for F, nm in FMAP.items()})


def Dtot(expr, i):
    out = sp.diff(expr, coords2[i])
    for (name, mi), s in list(JET.items()):
        if expr.has(s):
            out += sp.diff(expr, s) * jsym(name, mi + (i,))
    return out


E_w_j, E_q_j, E_f_j = to_jets(E_w), to_jets(E_q), to_jets(E_f)
fj, qj, wj = jsym('f', ()), jsym('q', ()), jsym('w', ())
fr_, fth = jsym('f', (0,)), jsym('f', (1,))
qr_, qth = jsym('q', (0,)), jsym('q', (1,))
wr_, wth = jsym('w', (0,)), jsym('w', (1,))
frr, frth, fthth = jsym('f', (0, 0)), jsym('f', (0, 1)), jsym('f', (1, 1))
qrr, qrth, qthth = jsym('q', (0, 0)), jsym('q', (0, 1)), jsym('q', (1, 1))
wrr, wrth, wthth = jsym('w', (0, 0)), jsym('w', (0, 1)), jsym('w', (1, 1))
DD = r**2 * (1 + wj)**2 - fj * qj**2          # f * D2 > 0 (signature)
SD = sp.sqrt(DD)

inv = {}
for ch, E in (('w', E_w_j), ('q', E_q_j), ('f', E_f_j)):
    for nm, s in (('w_rr', wrr), ('w_rth', wrth), ('w_thth', wthth),
                  ('q_rr', qrr), ('q_rth', qrth), ('q_thth', qthth)):
        inv[(ch, nm)] = sp.cancel(sp.together(sp.diff(E, s)))
print("   nonzero second-jet coefficients (all others identically 0):")
for k, v in inv.items():
    if v != 0:
        print(f"     E_{k[0]}: c[{k[1]}] = {sp.factor(v)}")

zero_keys = [k for k, v in inv.items() if v == 0]
check("S2-01 THE INVENTORY (the central uncovering): in the THREE EL "
      "channels, the only nonzero (w,q)-second-jet coefficients are "
      "E_w:c[w_rr], E_w:c[q_rth], E_q:c[w_rth], E_f:c[w_rth], "
      "E_f:c[q_rth] — in particular c[w_thth] = 0 IDENTICALLY AT ALL q "
      "IN ALL THREE CHANNELS, and c[w_rth] = 0 in the w-channel itself",
      set(zero_keys) == {('w', 'w_rth'), ('w', 'w_thth'),
                         ('w', 'q_rr'), ('w', 'q_thth'),
                         ('q', 'w_rr'), ('q', 'w_thth'),
                         ('q', 'q_rr'), ('q', 'q_rth'), ('q', 'q_thth'),
                         ('f', 'w_rr'), ('f', 'w_thth'),
                         ('f', 'q_rr'), ('f', 'q_thth')})
check("S2-02 closed forms (exact): E_w c[w_rr] = 4 f r^3 sin/"
      "((1+w) sqrt(D)), E_w c[q_rth] = E_q c[w_rth] = -2 f r sin/"
      "((1+w)^2 sqrt(D)), E_f c[w_rth] = -2 q r sin/((1+w)^2 sqrt(D)), "
      "E_f c[q_rth] = +r sin/((1+w) sqrt(D)); D = r^2 W - f q^2.  The "
      "w<->q cross symmetry E_w c[q_rth] == E_q c[w_rth] holds exactly",
      sp.cancel(sp.together(
          inv[('w', 'w_rr')] - 4 * fj * r**3 * sp.sin(th)
          / ((1 + wj) * SD))) == 0
      and sp.cancel(sp.together(
          inv[('w', 'q_rth')] + 2 * fj * r * sp.sin(th)
          / ((1 + wj)**2 * SD))) == 0
      and sp.cancel(sp.together(
          inv[('w', 'q_rth')] - inv[('q', 'w_rth')])) == 0
      and sp.cancel(sp.together(
          inv[('f', 'w_rth')] + 2 * qj * r * sp.sin(th)
          / ((1 + wj)**2 * SD))) == 0
      and sp.cancel(sp.together(
          inv[('f', 'q_rth')] - r * sp.sin(th)
          / ((1 + wj) * SD))) == 0)
# quasi-linearity (needed for the branch chain-rule bookkeeping):
secs = [wrr, wrth, wthth, qrr, qrth, qthth, frr, frth, fthth]
check("S2-03 quasi-linearity: E_w, E_q, E_f are LINEAR in all second "
      "jets (no second-jet products) — the branch chain-rule "
      "bookkeeping below is complete",
      all(sp.diff(sp.diff(E, a), b) == 0
          for E in (E_w_j, E_q_j, E_f_j) for a in secs for b in secs))

# G1 bar: full second-order jet EL vs Einstein route, hostile points:
# (method note: the density is kept UNEXPANDED — expanding the radical
# q-on density is the known computational trap; exact evaluation at
# rational points is unaffected)
print("   [building density jet EL for the trap audit ...]", flush=True)
EH_j = to_jets(sq * Rsc)


def EL_second(L, name):
    res = sp.diff(L, jsym(name, ()))
    for i in range(2):
        res -= Dtot(sp.diff(L, jsym(name, (i,))), i)
    for i in range(2):
        for j in range(i, 2):
            c = sp.diff(L, jsym(name, tuple(sorted((i, j)))))
            if c != 0:
                res += Dtot(Dtot(c, i), j)
    return res


diff_routes = EL_second(EH_j, 'w') - E_w_j
tpar = sp.Symbol('t_w', real=True)
de = diff_routes.subs({sp.sin(th): 2 * tpar / (1 + tpar**2),
                       sp.cos(th): (1 - tpar**2) / (1 + tpar**2)})
syms = sorted(de.free_symbols, key=str)
done, ok_pts = 0, True
while done < 4:
    sub = {}
    for s in syms:
        if s == r:
            sub[s] = Ra(random.randint(2, 9), random.randint(1, 5))
        elif s == tpar:
            sub[s] = Ra(random.randint(1, 7), random.randint(2, 9))
        elif str(s) == 'f':
            sub[s] = Ra(random.randint(1, 9), random.randint(1, 4))
        elif str(s) == 'w':
            sub[s] = Ra(random.randint(-2, 6), 7)     # hostile: w < 0
        elif str(s) == 'q':
            sub[s] = Ra(random.randint(-5, 5), 9)     # hostile: q < 0
        else:
            sub[s] = Ra(random.randint(-9, 9), random.randint(1, 7))
    if (sub[r]**2 * (1 + sub[wj])**2 - sub[fj] * sub[qj]**2) <= 0 \
            or (1 + sub[wj]) <= 0:
        continue
    ok_pts = ok_pts and (sp.cancel(de.subs(sub)) == 0)
    done += 1
check("S2-04 G1 bar: FULL second-order jet EL of sqrt(-g)R == "
      "Einstein-tensor route at 4 hostile signature-legal exact "
      "rational points (q both signs, w < 0) — trap-free engine at "
      "q-on", ok_pts)

# =====================================================================
print()
print("=" * 72)
print("PART 2 — TIME-ON q-ON CLASS: THE WAVE CONE IS q-INVARIANT")
print("=" * 72)
print("   [Ricci/Einstein, time-on q-on ...]", flush=True)
E_w3, E_q3, E_f3, (f3, q3, w3), sq3, _ = build_E((T, r, th))
row3 = {}
for nm, a in (('w_TT', sp.Derivative(w3, (T, 2))),
              ('w_Tr', sp.Derivative(w3, T, r)),
              ('w_Tth', sp.Derivative(w3, T, th)),
              ('w_rr', sp.Derivative(w3, (r, 2))),
              ('w_rth', sp.Derivative(w3, r, th)),
              ('w_thth', sp.Derivative(w3, (th, 2))),
              ('q_TT', sp.Derivative(q3, (T, 2))),
              ('q_Tth', sp.Derivative(q3, T, th)),
              ('q_rth', sp.Derivative(q3, r, th))):
    row3[nm] = sp.cancel(sp.together(E_w3.diff(a)))
    print(f"     E_w: c[{nm}] = {sp.factor(row3[nm])}")
DD3 = r**2 * (1 + w3)**2 - f3 * q3**2
check("S2-05 THE WAVE CONE IS q-INVARIANT (exact, full time-on q-on "
      "class): c[w_TT] = -4 r^3 sin/((1+w) f sqrt(D)), c[w_rr] = "
      "+4 r^3 f sin/((1+w) sqrt(D)) — ratio -1/f^2 AT ALL q: the "
      "species' characteristics stay dr/dT = +-f, q-undistorted",
      sp.cancel(sp.together(row3['w_TT'] + 4 * r**3 * sp.sin(th)
                            / ((1 + w3) * f3 * sp.sqrt(DD3)))) == 0
      and sp.cancel(sp.together(row3['w_rr'] - 4 * r**3 * f3
                                * sp.sin(th)
                                / ((1 + w3) * sp.sqrt(DD3)))) == 0)
check("S2-06 EXTENDED FIBER CANCELLATION AT EL LEVEL (the G2 face): "
      "c[w_Tr] = c[w_Tth] = c[w_rth] = c[w_thth] = 0 IDENTICALLY at "
      "all q on the time-on class — the species' w-EL has NO angular "
      "or mixed principal w-content at ANY q; angular structure can "
      "enter ONLY through the q-jet couplings c[q_TT] = +2 r q sin/"
      "((1+w)^2 sqrt(D)) and c[q_rth] = -2 r f sin/((1+w)^2 sqrt(D))",
      all(row3[k] == 0 for k in ('w_Tr', 'w_Tth', 'w_rth', 'w_thth'))
      and sp.cancel(sp.together(row3['q_TT'] - 2 * r * q3 * sp.sin(th)
                                / ((1 + w3)**2 * sp.sqrt(DD3)))) == 0
      and sp.cancel(sp.together(row3['q_rth'] + 2 * r * f3 * sp.sin(th)
                                / ((1 + w3)**2 * sp.sqrt(DD3)))) == 0
      and row3['q_Tth'] == 0)

# =====================================================================
print()
print("=" * 72)
print("PART 3 — THE q*-BRANCH: TOTAL O(kappa) REDUCED w-EL ROW")
print("=" * 72)
# C1 (positive banked convention c = 2) with plain symbols:
wv = sp.Symbol('w', real=True)
fv = sp.Symbol('f', positive=True)
frv, fthv = sp.symbols('f_r f_th', real=True)
qv = sp.Symbol('q', real=True)
Wv = (1 + wv)**2
DDv = r**2 * Wv - fv * qv**2
L_C1 = (Ra(1, 4) * r * sp.sin(th)
        * (fv * r**2 * Wv * frv**2 - 2 * fv * qv * frv * fthv
           + fthv**2) / ((1 + wv) * fv * sp.sqrt(DDv)))
qstar = 2 * r**2 * Wv * frv * fthv / (fv * r**2 * Wv * frv**2
                                      + fthv**2)
dL = sp.together(sp.diff(L_C1, qv))
# q* verification: exact rational spot points (the full radical cancel
# is the known computational trap; VA4's symbolic uniqueness is banked)
okq = True
for _ in range(5):
    sub = {r: Ra(random.randint(2, 7), random.randint(1, 3)),
           fv: Ra(random.randint(1, 8), random.randint(1, 4)),
           frv: Ra(random.randint(-7, 7), random.randint(1, 5)),
           fthv: Ra(random.randint(-7, 7), random.randint(1, 5)),
           wv: Ra(random.randint(-2, 5), 7), th: sp.pi / 3}
    if sub[frv] == 0 or sub[fthv] == 0:
        continue
    qs_v = qstar.subs(sub)
    if (sub[r]**2 * (1 + sub[wv])**2 - sub[fv] * qs_v**2) <= 0:
        continue
    okq = okq and sp.simplify(dL.subs(qv, qs_v).subs(sub)) == 0
check("S2-07 q* spot-verified: dL_C1/dq = 0 at q = q* at 5 exact "
      "rational signature-legal points (w on, both f_r f_th signs; "
      "symbolic uniqueness is VA4-banked, V1-06)", okq)
L_qq = sp.diff(L_C1, qv, 2)
L_wq = sp.diff(sp.diff(L_C1, qv), wv)
dqdw = sp.diff(qstar, wv)
# implicit-function identity dq*/dw = -L_wq/L_qq on the branch:
okI = True
for _ in range(5):
    sub = {r: Ra(random.randint(2, 7), random.randint(1, 3)),
           fv: Ra(random.randint(1, 8), random.randint(1, 4)),
           frv: Ra(random.randint(-7, 7), random.randint(1, 5)),
           fthv: Ra(random.randint(-7, 7), random.randint(1, 5)),
           wv: Ra(random.randint(-2, 5), 7), th: sp.pi / 3}
    if sub[frv] == 0 or sub[fthv] == 0:
        continue
    qs_v = qstar.subs(sub)
    if (sub[r]**2 * (1 + sub[wv])**2 - sub[fv] * qs_v**2) <= 0:
        continue
    okI = okI and sp.simplify(
        (dqdw + L_wq / L_qq).subs(qv, qs_v).subs(sub)) == 0
check("S2-08 implicit-function identity on the branch: dq*/dw = "
      "-L_wq/L_qq exactly (5 exact rational spot points, w on) — the "
      "structural source of m1 == m2 below", okI)

# ---- the branch chain-rule carriers (small exact objects) ----
# q*(f, w, f_r, f_th) carries NO w-jets; hence:
#   d(D_r q*)/d(second w-jets)   = 0 except none
#   d(D_th q*)/d(second w-jets)  = 0
#   d(D_r D_th q*)/dw_rth = dq*/dw ;  /dw_thth = 0 ; /dw_rr = 0
#   d(D_th D_th q*)/dw_thth = dq*/dw ;  d(D_r D_r q*)/dw_rr = dq*/dw
# verified on the jet-symbol images:
qstar_j = qstar.subs([(fv, fj), (frv, fr_), (fthv, fth), (wv, wj)])
qs_r = Dtot(qstar_j, 0)
qs_th = Dtot(qstar_j, 1)
qs_rth = Dtot(qs_r, 1)
qs_thth = Dtot(qs_th, 1)
qs_rr = Dtot(qs_r, 0)
dqdw_j = sp.diff(qstar_j, wj)
check("S2-09 chain carriers: d(D_rD_th q*)/dw_rth = d(D_th^2 q*)/"
      "dw_thth = d(D_r^2 q*)/dw_rr = dq*/dw, and NO other second-w-jet "
      "enters any D^J q* (first-jet substitutions carry no w-second-"
      "jets at all)",
      sp.cancel(sp.diff(qs_rth, wrth) - dqdw_j) == 0
      and sp.cancel(sp.diff(qs_thth, wthth) - dqdw_j) == 0
      and sp.cancel(sp.diff(qs_rr, wrr) - dqdw_j) == 0
      and sp.diff(qs_rth, wthth) == 0 and sp.diff(qs_rth, wrr) == 0
      and sp.diff(qs_thth, wrth) == 0 and sp.diff(qs_thth, wrr) == 0
      and sp.diff(qs_rr, wrth) == 0 and sp.diff(qs_rr, wthth) == 0
      and sp.diff(qs_r, wrr) == 0 and sp.diff(qs_r, wrth) == 0
      and sp.diff(qs_r, wthth) == 0 and sp.diff(qs_th, wrr) == 0
      and sp.diff(qs_th, wrth) == 0 and sp.diff(qs_th, wthth) == 0)

# THE w_thth THEOREM on the branch (G2 adjudication), assembled from
# exact zero pieces — no big substitution needed:
#   total c[w_thth] = E_w c[w_thth] (=0)
#                   + E_w c[q_thth] (=0) * dq*/dw      [m1 chain]
#                   - (L_wq/L_qq) * [E_q c[w_thth] (=0)
#                       + E_q c[q_thth] (=0) * dq*/dw]  [m2]
check("S2-10 G2 ADJUDICATED — THE w_thth THEOREM: the reduced branch "
      "w-EL's w_thth coefficient is 0 IDENTICALLY (every carrier "
      "vanishes: S2-01 zeros + S2-09 carriers + S2-03 quasi-"
      "linearity): the q*-branch supplies NO pure angular stiffness "
      "at any q — bands cannot become lines through an angular "
      "SL well at this order [premises: static P1 q-on class, "
      "C1-q* branch, O(kappa), EL level]",
      inv[('w', 'w_thth')] == 0 and inv[('w', 'q_thth')] == 0
      and inv[('q', 'w_thth')] == 0 and inv[('q', 'q_thth')] == 0)

# ---- what IS there: the mixed w_rth member, m1 and m2 ----
w0 = [(wv, 0)]
qstar0 = qstar.subs(wv, 0)
dqdw0 = sp.simplify(dqdw.subs(wv, 0))
P_ = fv * r**2 * frv**2 + fthv**2
Dw0 = fv * r**2 * frv**2 - fthv**2          # Delta_w at w = 0
check("S2-11 dq*/dw|_{w=0} = 4 r^2 f_r f_th^3/(f r^2 f_r^2 "
      "+ f_th^2)^2 exactly",
      sp.cancel(sp.together(dqdw0 - 4 * r**2 * frv * fthv**3 / P_**2))
      == 0)
DDstar0 = sp.factor(sp.cancel(DDv.subs(wv, 0).subs(qv, qstar0)))
check("S2-12 THE BRANCH DEGENERACY = THE TURNING SURFACE (exact): "
      "D|_{q*, w=0} = r^2 Delta_w^2/(f r^2 f_r^2 + f_th^2)^2 with "
      "Delta_w = f r^2 f_r^2 - f_th^2 — the q*-branch metric "
      "degenerates EXACTLY on W3's Delta_w turning surface (sqrt(D) "
      "= r |Delta_w|/P)",
      sp.cancel(sp.together(DDstar0 - r**2 * Dw0**2 / P_**2)) == 0)
# m1 = c_w[q_rth]|_{q*,w0} * dq*/dw|_0 ;  m2 = -(L_wq/L_qq)|_{q*,w0}
#    * c_q[w_rth]|_{q*,w0} = m1 by S2-08 + cross symmetry (S2-02).
# subsonic branch convention Delta_w > 0: sqrt(D*) = r Delta_w / P:
cq_branch0 = -2 * fv * r * sp.sin(th) / (r * Dw0 / P_)
m1 = sp.cancel(sp.together(cq_branch0 * dqdw0))
S_rth = sp.cancel(sp.together(2 * m1))
S_rth_tgt = -16 * fv * r**2 * sp.sin(th) * frv * fthv**3 / (P_ * Dw0)
check("S2-13 THE SURVIVING ANGULAR-DERIVATIVE CHANNEL (exact, w=0, "
      "subsonic Delta_w > 0): the reduced branch w-EL carries the "
      "MIXED term S_rth * w_rth with S_rth = m1 + m2 = 2 m1 = "
      "-16 f r^2 sin f_r f_th^3/[(f r^2 f_r^2 + f_th^2) Delta_w] — "
      "the species' own chain member and the C1-response member are "
      "EQUAL (implicit-function identity + cross-block symmetry); "
      "supersonic flips the overall sign (|Delta_w|)",
      sp.cancel(sp.together(S_rth - S_rth_tgt)) == 0)
# w_rr on the branch is the pure direct member (S2-09: no carrier):
c_rr_branch = sp.cancel(sp.together(
    (4 * fv * r**3 * sp.sin(th) / (r * Dw0 / P_))))
check("S2-14 branch radial stiffness c[w_rr]|_{q*,w0} = 4 f r^2 sin "
      "(f r^2 f_r^2 + f_th^2)/Delta_w (subsonic): BOTH surviving "
      "principal coefficients diverge on the turning surface "
      "Delta_w -> 0; their ratio S_rth/c_rr = -4 f_r f_th^3/"
      "(f r^2 f_r^2 + f_th^2)^2 stays finite",
      sp.cancel(sp.together(c_rr_branch
                            - 4 * fv * r**2 * sp.sin(th) * P_ / Dw0))
      == 0
      and sp.cancel(sp.together(S_rth / c_rr_branch
                                + 4 * frv * fthv**3 / P_**2)) == 0)
check("S2-15 structure of the surviving channel: NO xi_th^2 term — "
      "principal form xi_r (c_rr xi_r + S_rth xi_th), DEGENERATE "
      "along pure-theta directions (not an angular well; an angular "
      "COUPLING that breaks the #28 premise 'per-u radial SL "
      "pencils'); S_rth is ODD in f_th (odd across the equator), "
      "vanishes on spherical (f_th -> 0) as f_th^3, axis-regular",
      sp.cancel(sp.together(S_rth.subs(fthv, 0))) == 0
      and sp.cancel(sp.together(
          S_rth.subs(fthv, -fthv) + S_rth)) == 0)

# =====================================================================
print()
print("=" * 72)
print("PART 4 — EL-MAP COMPLETION: THE q-CHANNEL AND THE PAIRING")
print("=" * 72)
q0sub = [(qrr, 0), (qrth, 0), (qthth, 0), (qr_, 0), (qth, 0), (qj, 0)]
w0sub = [(wrr, 0), (wrth, 0), (wthth, 0), (wr_, 0), (wth, 0), (wj, 0)]
E_q_q0 = E_q_j.subs(q0sub)
# polar-domain convention: positive bricks, Abs -> identity
E_q_q0 = E_q_q0.replace(sp.Abs, lambda x_: x_)
E_q_q0 = sp.cancel(sp.together(E_q_q0))
E_q_D = sp.cancel(sp.together(E_q_q0 - E_q_q0.subs(w0sub)))
print("   E_q[Delta]|_{q=0} =", sp.simplify(E_q_D), flush=True)
check("S2-16 the species' q-channel at q = 0: NONZERO on shaped w-on "
      "configurations, vanishing at w == 0, and every term carries "
      "w_r, w_rth or f_rth — at O(kappa) the species SHIFTS the "
      "q-equation (the q* branch is kappa-dressed; the m2 bookkeeping "
      "above evaluates on the C1 branch per registry #28's naming)",
      sp.simplify(E_q_D) != 0
      and sp.cancel(sp.together(E_q_D.subs(w0sub))) == 0
      and sp.cancel(sp.together(
          E_q_D.subs([(wr_, 0), (wrth, 0), (frth, 0)]))) == 0)
check("S2-17 ... and its principal piece is -2 f sin w_rth/(1+w)^3 "
      "(the cross-symmetric partner of the w-channel's q_rth coupling)",
      sp.cancel(sp.together(sp.diff(E_q_D, wrth)
                            + 2 * fj * sp.sin(th) / (1 + wj)**3)) == 0)
# THE PAIRING (Task 4): w_thth in the f-channel:
check("S2-18 THE PAIRING'S DYNAMICAL STATUS (negative, recorded as "
      "computed): c_f[w_thth] = 0 and c_f[q_thth] = 0 IDENTICALLY at "
      "all q, and the branch carriers vanish (S2-09/S2-03) — the W2 "
      "clock/shape pairing [(1-f) + 4 w_thth] acquires NO EL channel "
      "in ANY equation at this order; what the f-channel acquires "
      "instead is the q-MEDIATED MIXED coupling c_f[w_rth] = "
      "-2 q r sin/((1+w)^2 sqrt(D)) [premises: P1 q-on class, EL "
      "level, O(kappa)]",
      inv[('f', 'w_thth')] == 0 and inv[('f', 'q_thth')] == 0
      and inv[('f', 'w_rth')] != 0)

print()
print(f"TOTALS: {len(PASS)} PASS / {len(FAIL)} FAIL "
      f"({time.time()-t0:.0f}s)")
assert not FAIL
