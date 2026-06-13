#!/usr/bin/env python3
"""W6 ARM-1 — SCRIPT B2: CLOSED FORMS OF THE REDUCED STATIC w-ROW AT
THE q-bar == 0 CLASS (light companion to w6_arm1_b_symbol.py).

Date: 2026-06-12.  Loads the Script-A block checkpoint
(/tmp/w6_arm1_blocks.srepr; regenerate with w6_arm1_a_operator.py)
and specializes the background to q-bar == 0 (all q-jets zero) BEFORE
row assembly — legal because restricting q-jets to zero commutes with
the total derivative (no term can resurrect a q-jet).  Everything
here is a SPECIALIZATION cross-check target for the general-background
engine of w6_arm1_b_symbol.py; the q-bar = 0 class is off-shell in q
on shaped cells (E_q != 0 there) — labeled, exactly as the banked
frozen-spectra readouts were.

Deliverable: exact closed forms of O_qq, dq_sol, and the angular
delta-w content of the reduced w-row and f-row at q-bar = 0.
Log: /tmp/w6_arm1_b2.log
"""
import sys
import time

import sympy as sp

from w6_arm1_lib import (T, r, th, kap, beta, TAGS, Jets, FIELDS,
                         load_blocks)

t0 = time.time()
PASS, FAIL = [], []


def check(tag, cond, note=""):
    ok = bool(cond)
    (PASS if ok else FAIL).append(tag)
    print(f"W6B2-{tag}: {'PASS' if ok else 'FAIL'}  {note}", flush=True)


H, B, C, X = load_blocks('/tmp/w6_arm1_blocks.srepr')
J = Jets({}, [T, r, th], TAGS)
# re-register jets by name so J.D raises correctly:
for nm in FIELDS:
    J.sym(nm, ())
    for i in range(3):
        J.sym(nm, (i,))
        for jx in range(i, 3):
            J.sym(nm, (i, jx))
            for kx in range(jx, 3):
                J.sym(nm, (i, jx, kx))
fj, wj = J.sym('f', ()), J.sym('w', ())
fT, fr_, fh = (J.sym('f', (0,)), J.sym('f', (1,)), J.sym('f', (2,)))
wT, wr_, wh = (J.sym('w', (0,)), J.sym('w', (1,)), J.sym('w', (2,)))
W1 = 1 + wj

# static + q-bar == 0 specialization of the blocks:
q0 = {J.sym('q', mi): 0 for mi in
      [(), (0,), (1,), (2,)]}
q0.update({fT: 0, wT: 0})
Hs = {k: v.subs(q0) for k, v in H.items()}
Bs = {k: v.subs(q0) for k, v in B.items()}
Cs = {k: v.subs(q0) for k, v in C.items()}
print(f"   [blocks specialized, {time.time()-t0:.0f}s]", flush=True)

FJ = {}


def fsym(nm, mi):
    mi = tuple(sorted(mi))
    k = (nm, mi)
    if k not in FJ:
        suff = ''.join(TAGS[i] for i in mi)
        FJ[k] = sp.Symbol(nm + ('_' + suff if suff else ''),
                          real=True)
    return FJ[k]


FNAME = {'f': 'df', 'q': 'dq', 'w': 'dw'}


def lin_row(Xn):
    row = {}

    def add(key, val):
        if val == 0:
            return
        row[key] = row.get(key, 0) + val

    for Y in FIELDS:
        dY = FNAME[Y]
        add((dY, ()), Cs[(Xn, Y)])
        for m in (1, 2):
            add((dY, ()), -J.D(Bs[(Y, (Xn, m))], m))
        for n in (1, 2):
            add((dY, (n,)), Bs[(Xn, (Y, n))] - Bs[(Y, (Xn, n))])
            for m in (1, 2):
                add((dY, (n,)), -J.D(Hs[((Xn, m), (Y, n))], m))
                add((dY, tuple(sorted((m, n)))),
                    -Hs[((Xn, m), (Y, n))])
    out = {}
    for k, v in row.items():
        # kill background q-jets raised by J.D (q-bar == 0 globally):
        v = v.subs({J.sym('q', mi): 0
                    for mi in [(0, 0), (0, 1), (0, 2), (1, 1),
                               (1, 2), (2, 2)]})
        v = sp.cancel(sp.together(v))
        if v != 0:
            out[k] = v
    return out


rows = {Xn: lin_row(Xn) for Xn in FIELDS}
print(f"   [rows built, {time.time()-t0:.0f}s]", flush=True)

print("=" * 72)
print("THE q-bar = 0 STATIC LINEARIZED q-ROW (exact, all w)")
print("=" * 72)
rq = rows['q']
oqq = rq.get(('dq', ()), 0)
check("01", all(k[0] != 'dq' or k[1] == () for k in rq) and oqq != 0,
      "q-row: delta-q enters algebraically only at q-bar = 0 too")
for k in sorted(rq, key=str):
    print(f"   q-row coeff[{fsym(*k)}] = "
          f"{sp.factor(sp.cancel(sp.together(rq[k])))}", flush=True)
dqsol = {k: sp.cancel(sp.together(-v / oqq)) for k, v in rq.items()
         if k[0] != 'dq'}


def prolong(soldict, m):
    out = {}
    for (nm, mi), cf in soldict.items():
        df_ = J.D(cf, m).subs({J.sym('q', mi2): 0 for mi2 in
                               [(0, 0), (0, 1), (0, 2), (1, 1),
                                (1, 2), (2, 2)]})
        out[(nm, mi)] = out.get((nm, mi), 0) + df_
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


red = {Xn: reduce_row(rows[Xn]) for Xn in ('f', 'w')}
print(f"   [reduced, {time.time()-t0:.0f}s]", flush=True)

print()
print("=" * 72)
print("REDUCED STATIC w-ROW AT q-bar = 0: delta-w content")
print("(on the DRESSED RADIAL CELL slice w-bar = w(r): w_h = 0 — the")
print(" W5 physical class; general-w forms retained in script B)")
print("=" * 72)
# the dressed radial slice (polar convention 1 + w > 0):
slice_wh = {J.sym('w', (2,)): 0, J.sym('w', (1, 2)): 0,
            J.sym('w', (2, 2)): 0, J.sym('w', (1, 1, 2)): 0,
            J.sym('w', (1, 2, 2)): 0, J.sym('w', (2, 2, 2)): 0}


def clean(v):
    v = v.subs(slice_wh)
    v = v.replace(sp.Abs, lambda x_: x_)
    v = v.replace(
        lambda e: e.is_Pow and getattr(e.exp, 'is_Rational', False)
        and e.exp.q == 2 and sp.simplify(e.base - (1 + wj) ** 2) == 0,
        lambda e: (1 + wj) ** (2 * e.exp))
    v = v.subs(sp.sqrt(wj ** 2 + 2 * wj + 1), 1 + wj)
    return sp.cancel(sp.together(v))


for rown in ('w', 'f'):
    print(f"\nREDUCED STATIC {rown}-ROW AT q-bar = 0, w_h = 0: "
          "delta-w content (exact)")
    for kk in sorted((k for k in red[rown] if k[0] == 'dw'), key=str):
        v = clean(red[rown][kk])
        if v != 0:
            try:
                vf = sp.factor(v)
            except Exception:
                vf = v
            s = str(vf)
            if len(s) > 2200:
                s = s[:2200] + f" ...[{len(s)} chars]"
            print(f"   coeff[{fsym(*kk)}] = {s}", flush=True)

# headline checks (dressed radial slice): pure angular door + quartic
c_whh = clean(red['w'].get(('dw', (2, 2)), 0))
c_wrrhh = clean(red['w'].get(('dw', (1, 1, 2, 2)), 0))
Hwrqh = clean(Hs[(('w', 1), ('q', 2))])
tgt_q = clean(-Hwrqh ** 2 / clean(oqq))
check("02", sp.cancel(sp.together(c_wrrhh - tgt_q)) == 0,
      "coeff[dw_rrhh]|_{q-bar=0, w_h=0} == -H[w_r,q_th]^2/O_qq "
      "exactly (the induced quartic is the square of the single "
      "nonzero angular pairing over the algebraic q-q block)")
check("03", True,
      f"DATUM: coeff[dw_hh]|q-bar=0, w_h=0 is "
      f"{'NONZERO' if c_whh != 0 else '== 0'} "
      f"(the pure angular door on the dressed radial cell class)")
print(f"\nW6 ARM-1 SCRIPT B2: {len(PASS)} PASS / {len(FAIL)} FAIL "
      f"({time.time()-t0:.0f}s)")
for x in FAIL:
    print("FAILED:", x)
sys.exit(0 if not FAIL else 1)
