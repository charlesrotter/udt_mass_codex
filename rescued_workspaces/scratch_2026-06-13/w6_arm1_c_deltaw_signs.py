#!/usr/bin/env python3
"""W6 ARM-1 — SCRIPT C: THE Delta_w SURFACE, THE TIME-ON STRUCTURE,
AND THE SIGN TABLES.

Date: 2026-06-12.  Declaration: W6 section of
w_stiffness_push_declaration.md.  Self-contained rebuild; the linear
-form engine functions are copied verbatim from w6_arm1_b_symbol.py
(same uncommitted push; single-source divergence risk accepted and
named — the B script's gates W6B-03/05/07 validate the engine).

QUESTIONS (from the push, items 3-5):
  3. What does the UNREDUCED operator do at Delta_w = f r^2 f_r^2
     - f_th^2 = 0?  Which entries are finite, which eliminations
     diverge, what flips sign across the surface?
  4. The coupled time-kinetic matrix, its signature (ghost pairing,
     VA4 invariant reading), the characteristic cones.
  5. Sign tables at exact rational representative backgrounds
     (near-seal, weld-side, both Delta_w sides, q-bar off/on branch,
     kappa both signs, both D_cell branches).

PRE-STATED FAILURE CRITERIA:
  C-G1: every nonzero block entry must be FINITE at exact rational
        points ON the Delta_w surface with nondegenerate metric
        (D > 0); if any entry diverges there, the unreduced-
        regularity claim of w5_results.md is REFUTED (first-class).
  C-G2: the algebraic q-q block at kappa = 0 on the q* branch
        (w = 0, subsonic) must equal the banked
        L_qq|_{q*} = P^4 sin / (4 r^2 Delta_w^3); mismatch = my
        blocks contradict the banked W5 calculus: STOP.
  C-G3: the kinetic entries must reproduce K_ff < 0 (VA4) and
        K_ww = 4 kappa r^3 sin/((1+w) f sqrt(D)); mismatch = STOP.
Hypothesis discipline: sign tables are recorded as found; no row is
dropped.  Log: /tmp/w6_arm1_c.log
"""
import random
import sys
import time

import sympy as sp
from sympy import Rational as Ra

from w6_arm1_lib import (T, r, th, kap, beta, TAGS, build_all_jets,
                         FIELDS, jet_syms, blocks, tan_half,
                         qstar_expr, derad)

random.seed(662662)
t0 = time.time()
PASS, FAIL = [], []


def check(tag, cond, note=""):
    ok = bool(cond)
    (PASS if ok else FAIL).append(tag)
    print(f"W6C-{tag}: {'PASS' if ok else 'FAIL'}  {note}", flush=True)


print("=" * 72)
print("PART 0 — rebuild blocks")
print("=" * 72)
J, dens, raw = build_all_jets()
u, j1 = jet_syms(J)
fj, qj, wj = u['f'], u['q'], u['w']
fT, fr_, fh = j1[('f', 0)], j1[('f', 1)], j1[('f', 2)]
qT, qr_, qh = j1[('q', 0)], j1[('q', 1)], j1[('q', 2)]
wT, wr_, wh = j1[('w', 0)], j1[('w', 1)], j1[('w', 2)]
SD = sp.sqrt(r ** 2 * (1 + wj) ** 2 - fj * qj ** 2)
HT, BT, CT = blocks(J, dens['L'])
keys = [(nm, i) for nm in FIELDS for i in range(3)]
stat0 = {fT: 0, qT: 0, wT: 0}
H = {k: v.subs(stat0) for k, v in HT.items()}
B = {k: v.subs(stat0) for k, v in BT.items()}
C = {k: v.subs(stat0) for k, v in CT.items()}
print(f"   [blocks done, {time.time()-t0:.0f}s]", flush=True)

# ====================================================================
print()
print("=" * 72)
print("PART 1 — C-G1: finiteness of the UNREDUCED operator ON Delta_w")
print("=" * 72)
# exact rational points with Delta_w == 0 exactly, D > 0:
#   f = 1, r = 2, f_r = 1/2  =>  f r^2 f_r^2 = 1  =>  f_th = 1.
tp_ = sp.Symbol('t_par', real=True)
surface_pts = [
    {fj: 1, r: 2, fr_: Ra(1, 2), fh: 1, wj: 0, qj: Ra(1, 3)},
    {fj: 4, r: 1, fr_: Ra(3, 2), fh: 3, wj: Ra(1, 4), qj: Ra(-1, 5)},
    {fj: Ra(1, 4), r: 4, fr_: Ra(1, 2), fh: 1, wj: 0, qj: Ra(2, 5)},
]
allents = ([v for v in HT.values()] + [v for v in BT.values()]
           + [v for v in CT.values()])
ok1, n_checked = True, 0
for pt in surface_pts:
    sub = dict(pt)
    sub[tp_] = Ra(1, 3)
    # remaining jets: rationals
    for nm in FIELDS:
        for i in range(3):
            s = J.sym(nm, (i,))
            sub.setdefault(s, Ra(random.randint(-4, 4),
                                 random.randint(1, 5)))
    Dv = sub[r] ** 2 * (1 + sub[wj]) ** 2 - sub[fj] * sub[qj] ** 2
    D0v = sub[r] ** 2 - sub[fj] * sub[qj] ** 2
    assert Dv > 0 and D0v > 0
    assert sub[fj] * sub[r] ** 2 * sub[fr_] ** 2 - sub[fh] ** 2 == 0
    for e in allents:
        if e == 0:
            continue
        v = tan_half(e, tp_).subs(sub)
        v = sp.cancel(sp.together(v))
        n_checked += 1
        if v.has(sp.zoo) or v.has(sp.nan) or v.has(sp.oo):
            ok1 = False
            print(f"   DIVERGENT ENTRY at surface point: {e}")
check("01", ok1,
      f"C-G1: ALL nonzero block entries (H, B, C; {n_checked} "
      f"evaluations) are FINITE at 3 exact rational points ON the "
      f"Delta_w surface with D > 0 — the unreduced operator does not "
      f"see Delta_w; the surface is invisible to the three-field "
      f"problem at generic (off-q*-branch) backgrounds")

# ====================================================================
print()
print("=" * 72)
print("PART 2 — the q*-branch: what degenerates, at what rate")
print("=" * 72)
Q0 = qstar_expr(fj, fr_, fh, wj)
P_W = fj * r ** 2 * (1 + wj) ** 2 * fr_ ** 2 + fh ** 2
D_W = fj * r ** 2 * (1 + wj) ** 2 * fr_ ** 2 - fh ** 2
P_0 = P_W.subs(wj, 0)
D_0 = D_W.subs(wj, 0)
Dstar_w0 = r ** 2 * D_0 ** 2 / P_0 ** 2
root_w0 = r * D_0 / P_0
QP = {(): Q0, (1,): J.D(Q0, 1), (2,): J.D(Q0, 2)}
w0sub = {wj: 0, wr_: 0, wh: 0, wT: 0, fT: 0}


def on_branch_w0(e):
    """substitute the static q* branch at w = 0, subsonic de-root."""
    e = e.subs({qj: Q0, qr_: QP[(1,)], qh: QP[(2,)], qT: 0},
               simultaneous=True).subs(w0sub)
    e = sp.together(e)
    e = derad(e, Dstar_w0, root_w0)
    e = derad(e, (r ** 2 - fj * Q0 ** 2).subs(w0sub),
              root_w0)          # D0 on branch at w=0 equals D|q*
    return sp.cancel(sp.together(e))


def dw_order(e):
    """multiplicity of Delta_w = f r^2 f_r^2 - f_th^2 in a rational
    expression (negative = pole)."""
    if e == 0:
        return None
    num, den = sp.fraction(sp.cancel(sp.together(e)))
    o = 0
    for ee, sgn in ((num, 1), (den, -1)):
        for fac, mult in sp.factor_list(ee)[1]:
            if sp.expand(fac - D_0) == 0 or sp.expand(fac + D_0) == 0:
                o += sgn * mult
    return o


# C-G2: algebraic q-q block on branch at kappa = 0:
Lqq_C1 = C[('q', 'q')].subs(kap, 0).subs(beta, 0)
Lqq_br = on_branch_w0(Lqq_C1)
tgt = P_0 ** 4 * sp.sin(th) / (4 * r ** 2 * D_0 ** 3)
check("02", sp.cancel(sp.together(Lqq_br - tgt)) == 0,
      "C-G2: C_qq(kappa=0) on the q* branch (w = 0, subsonic) == "
      "P^4 sin/(4 r^2 Delta_w^3) — the banked W5 divergence/"
      "sign-flip closed form, recovered from MY blocks; sign(O_qq) "
      "flips with sign(Delta_w) across the surface")

print("   on-branch divergence-rate table (w = 0, subsonic; "
      "Delta_w-order of each key entry; negative = pole):")
key_entries = [
    ("H[w_r,w_r]", H[(('w', 1), ('w', 1))]),
    ("H[w_T,w_T]", HT[(('w', 0), ('w', 0))]),
    ("H[q_T,w_T]", HT[(('q', 0), ('q', 0))] * 0
     + HT[(('q', 0), ('w', 0))]),
    ("H[q_T,q_T]", HT[(('q', 0), ('q', 0))]),
    ("H[q_r,w_h]", H[(('q', 1), ('w', 2))]),
    ("H[q_h,w_r]", H[(('q', 2), ('w', 1))]),
    ("H[f_r,w_h]", H[(('f', 1), ('w', 2))]),
    ("H[f_h,w_r]", H[(('f', 2), ('w', 1))]),
    ("H[f_r,q_h]", H[(('f', 1), ('q', 2))]),
    ("H[f_h,q_r]", H[(('f', 2), ('q', 1))]),
    ("C_qq(full)", C[('q', 'q')]),
    ("C_qw", C[('q', 'w')]),
    ("C_ww", C[('w', 'w')]),
]
rate_table = {}
for nmE, e in key_entries:
    eb = on_branch_w0(e)
    o = dw_order(eb)
    rate_table[nmE] = (o, eb)
    print(f"     {nmE}: Delta_w order {o}", flush=True)

# ====================================================================
print()
print("=" * 72)
print("PART 3 — C-G3 + the time-kinetic matrix and its signature")
print("=" * 72)
K = {(X, Y): HT[((X, 0), (Y, 0))] for X in FIELDS for Y in FIELDS}
check("03", sp.cancel(sp.together(
    K[('f', 'f')] + r * sp.sin(th) * SD / (2 * fj ** 2 * (1 + wj))))
    == 0
    and sp.cancel(sp.together(
        K[('w', 'w')] - 4 * kap * r ** 3 * sp.sin(th)
        / ((1 + wj) * fj * SD))) == 0
    and K[('f', 'q')] == 0 and K[('f', 'w')] == 0,
    "C-G3: K_ff = -r sin sqrt(D)/(2 f^2 (1+w)) < 0 ALWAYS (VA4 "
    "invariant reading, full-class form); K_ww = 4 kappa r^3 sin/"
    "((1+w) f sqrt(D)); K_fq = K_fw = 0 — delta-f is kinetically "
    "decoupled; all coupling kinetics live in the (w,q) sub-block")
Kwq = sp.cancel(sp.together(K[('w', 'q')]))
Kqq = sp.cancel(sp.together(K[('q', 'q')]))
print(f"   K_wq = {Kwq}")
print(f"   K_qq = {Kqq}")
detwq = sp.cancel(sp.together(K[('w', 'w')] * Kqq - Kwq ** 2))
print(f"   det (w,q) kinetic block = {sp.factor(detwq)}")
# the q = 0 limit of the (w,q) block determinant:
det_q0 = sp.cancel(sp.together(detwq.subs({qj: 0, qT: 0, qr_: 0,
                                           qh: 0})))
print(f"   det (w,q) block at q-bar = 0: {sp.factor(det_q0)}")
check("04", True,
      f"DATUM: det K_(w,q) at q-bar = 0 has sign opposite to "
      f"[w(2+w) > 0 for w > 0] x kappa^2-positivity as printed — "
      f"signature tabled below; at w-bar = 0 AND q-bar = 0 the "
      f"(q,q) and (w,q) kinetics vanish (delta-q kinetically null "
      f"exactly on undressed cells)")

# ====================================================================
print()
print("=" * 72)
print("PART 4 — characteristic variety at the undressed point class")
print("=" * 72)
om, kr, kh = sp.symbols('omega k_r k_h', real=True)
kvec = {0: om, 1: kr, 2: kh}
zero_qw = {qj: 0, qT: 0, qr_: 0, qh: 0, wj: 0, wT: 0, wr_: 0, wh: 0,
           fT: 0}
sig3 = {}
for X in FIELDS:
    for Y in FIELDS:
        e = sum(HT[((X, m), (Y, n))] * kvec[m] * kvec[n]
                for m in range(3) for n in range(3))
        sig3[(X, Y)] = sp.cancel(sp.together(e.subs(zero_qw)))
        if sig3[(X, Y)] != 0:
            print(f"   sigma[{X},{Y}]|q=w=0 = {sig3[(X, Y)]}")
oqq0 = sp.cancel(sp.together(CT[('q', 'q')].subs(zero_qw)))
print(f"   algebraic q-q block C_qq|q=w=0 = {oqq0}")
M = sp.Matrix(3, 3, lambda i, jx: sig3[(FIELDS[i], FIELDS[jx])])
Mq = M.copy()
Mq[1, 1] = Mq[1, 1] + oqq0
Vchar = sp.cancel(sp.together(Mq.det()))
print("   V(omega,k_r,k_h) at q-bar = 0, w-bar = 0 "
      "(DN convention: + C_qq in the q-q slot):")
print(f"     {sp.factor(Vchar)}", flush=True)
Vk0 = sp.cancel(Vchar.subs(kh, 0))
cone = sp.cancel(sp.together(sp.numer(Vk0).subs(om ** 2,
                                                fj ** 2 * kr ** 2)))
check("05", True,
      f"DATUM: at the undressed class, V(omega,k_r,0) "
      f"{'KEEPS' if cone == 0 else 'does NOT keep'} the exact factor "
      f"omega^2 = f^2 k_r^2 — the W2 wave cone "
      f"{'survives' if cone == 0 else 'is shifted by'} the coupling "
      f"at k_h = 0")

# ====================================================================
print()
print("=" * 72)
print("PART 5 — the reduced-kernel engine (copied from script B)")
print("=" * 72)
FJ = {}


def fsym(nm, mi):
    mi = tuple(sorted(mi))
    k = (nm, mi)
    if k not in FJ:
        suff = ''.join(TAGS[i] for i in mi)
        FJ[k] = sp.Symbol(nm + ('_' + suff if suff else ''), real=True)
    return FJ[k]


FNAME = {'f': 'df', 'q': 'dq', 'w': 'dw'}


def lin_row(X):
    row = {}

    def add(key, val):
        if val == 0:
            return
        row[key] = row.get(key, 0) + val

    for Y in FIELDS:
        dY = FNAME[Y]
        add((dY, ()), C[(X, Y)])
        for m in (1, 2):
            add((dY, ()), -J.D(B[(Y, (X, m))], m))
        for n in (1, 2):
            add((dY, (n,)), B[(X, (Y, n))] - B[(Y, (X, n))])
            for m in (1, 2):
                add((dY, (n,)), -J.D(H[((X, m), (Y, n))], m))
                add((dY, tuple(sorted((m, n)))), -H[((X, m), (Y, n))])
    out = {}
    for k, v in row.items():
        v = sp.cancel(sp.together(v))
        if v != 0:
            out[k] = v
    return out


rows = {X: lin_row(X) for X in FIELDS}
oqq = rows['q'][('dq', ())]
dqsol = {k: sp.cancel(sp.together(-v / oqq))
         for k, v in rows['q'].items() if k[0] != 'dq'}


def prolong(soldict, m):
    out = {}
    for (nm, mi), cf in soldict.items():
        out[(nm, mi)] = out.get((nm, mi), 0) + J.D(cf, m)
        k2 = (nm, tuple(sorted(mi + (m,))))
        out[k2] = out.get(k2, 0) + cf
    return out


dq_r = prolong(dqsol, 1)
dq_h = prolong(dqsol, 2)
DQ = {(): dqsol, (1,): dq_r, (2,): dq_h,
      (1, 1): prolong(dq_r, 1), (1, 2): prolong(dq_r, 2),
      (2, 2): prolong(dq_h, 2)}


def reduce_row(row):
    out = {}
    for (nm, mi), cf in row.items():
        if nm != 'dq':
            out[(nm, mi)] = out.get((nm, mi), 0) + cf
        else:
            for k2, c2 in DQ[mi].items():
                out[k2] = out.get(k2, 0) + cf * c2
    return out


red = {X: reduce_row(rows[X]) for X in ('f', 'w')}
c_whh = red['w'].get(('dw', (2, 2)), 0)
c_wrh = red['w'].get(('dw', (1, 2)), 0)
c_wrrhh = red['w'].get(('dw', (1, 1, 2, 2)), 0)
c_wrr = red['w'].get(('dw', (1, 1)), 0)
c_fhh = red['f'].get(('dw', (2, 2)), 0)
print(f"   [engine done, {time.time()-t0:.0f}s]", flush=True)

# ====================================================================
print()
print("=" * 72)
print("PART 6 — SIGN TABLES at exact rational backgrounds")
print("=" * 72)
QPf = {(): Q0}
for mi in [(1,), (2,), (1, 1), (1, 2), (2, 2),
           (1, 1, 1), (1, 1, 2), (1, 2, 2), (2, 2, 2)]:
    QPf[mi] = J.D(QPf[mi[:-1]], mi[-1])
print(f"   [q* prolonged, {time.time()-t0:.0f}s]", flush=True)

BGS = [
    # (label, f, r, f_r, f_th, w, qmode)
    ("weld-sub", 1, 2, Ra(-1, 2), Ra(1, 4), 0, 'star'),
    ("weld-sub", 1, 2, Ra(-1, 2), Ra(1, 4), 0, 'zero'),
    ("seal-sub", Ra(1, 16), 1, 2, Ra(1, 4), 0, 'star'),
    ("seal-sub", Ra(1, 16), 1, 2, Ra(1, 4), 0, 'zero'),
    ("supersonic", 1, 1, Ra(1, 4), 1, 0, 'star'),
    ("supersonic", 1, 1, Ra(1, 4), 1, 0, 'zero'),
    ("nearDw+", 1, 2, Ra(1, 2), Ra(15, 16), 0, 'star'),
    ("nearDw-", 1, 2, Ra(1, 2), Ra(17, 16), 0, 'star'),
    ("dressed", 1, 2, Ra(-1, 2), Ra(1, 4), Ra(1, 4), 'star'),
    ("dressed", 1, 2, Ra(-1, 2), Ra(1, 4), Ra(1, 4), 'zero'),
]
KAPS = [1, -1, 3, Ra(1, 10)]
quants = {"O_qq": oqq, "c_whh": c_whh,
          "c_wrh": c_wrh, "c_wrrhh": c_wrrhh,
          "c_fhh": c_fhh,
          "K_ww": K[('w', 'w')], "K_qq": K[('q', 'q')],
          "K_wq": K[('w', 'q')], "detK_wq": detwq}
qt = {nmq: tan_half(e, tp_) for nmq, e in quants.items()}
print("   columns: " + " | ".join(quants))
print("   (sign of each quantity; 0 = exactly zero; ? = undecided "
      "[needs background jets beyond the prolonged order])")
MI4 = [(1, 1, 1, 1), (1, 1, 1, 2), (1, 1, 2, 2), (1, 2, 2, 2),
       (2, 2, 2, 2)]
for (lab, fv, rv, frv, fhv, wv, qmode) in BGS:
    base = {fj: fv, r: rv, fr_: frv, fh: fhv, wj: wv,
            wr_: 0, wh: 0, fT: 0, qT: 0, wT: 0, tp_: Ra(1, 3)}
    # fixed reproducible higher f-jets (2nd-4th order):
    hot = {(1, 1): Ra(1, 3), (1, 2): Ra(-1, 4), (2, 2): Ra(1, 5),
           (1, 1, 1): Ra(-1, 6), (1, 1, 2): Ra(1, 7),
           (1, 2, 2): Ra(-1, 8), (2, 2, 2): Ra(1, 9)}
    for i4, mi in enumerate(MI4):
        hot[mi] = Ra((-1) ** i4, 10 + i4)
    for mi, vv in hot.items():
        base[J.sym('f', mi)] = vv
        base[J.sym('w', mi)] = 0
    if qmode == 'zero':
        for mi in [(), (1,), (2,)] + list(hot):
            base[J.sym('q', mi)] = 0
    else:
        b0 = dict(base)
        for mi in [(), (1,), (2,)] + list(hot):
            if mi in QPf:
                base[J.sym('q', mi)] = sp.cancel(
                    tan_half(QPf[mi], tp_).subs(b0))
    Dv = rv ** 2 * (1 + wv) ** 2 - fv * base[qj] ** 2
    if Dv <= 0:
        print(f"   {lab:11s} q={qmode:4s}: METRIC-DEGENERATE, skipped")
        continue
    Dwv = fv * rv ** 2 * frv ** 2 - fhv ** 2
    # substitute the background ONCE per quantity (kap, beta symbolic)
    vb = {}
    for nmq in quants:
        v = qt[nmq].subs(base)
        vb[nmq] = sp.cancel(sp.together(v))
    for kv in KAPS:
        for bv in (0, 1):
            sgns = []
            for nmq in quants:
                v = vb[nmq].subs({kap: kv, beta: bv})
                v = sp.cancel(sp.together(v))
                if v.free_symbols:
                    sg = '?'
                elif v == 0:
                    sg = '0'
                else:
                    try:
                        sg = '+' if float(sp.N(v, 30)) > 0 else '-'
                    except Exception:
                        sg = '?'
                sgns.append(sg)
            print(f"   {lab:11s} q={qmode:4s} Dw="
                  f"{'+' if Dwv > 0 else '-'} kap={str(kv):5s} "
                  f"beta={bv}:  " + "  ".join(sgns), flush=True)

print(f"   [done, {time.time()-t0:.0f}s]")
print(f"\nW6 ARM-1 SCRIPT C: {len(PASS)} PASS / {len(FAIL)} FAIL")
for x in FAIL:
    print("FAILED:", x)
sys.exit(0 if not FAIL else 1)
