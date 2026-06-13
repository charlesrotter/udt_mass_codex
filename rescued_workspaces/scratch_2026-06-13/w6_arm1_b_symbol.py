#!/usr/bin/env python3
"""W6 ARM-1 — SCRIPT B: THE ANGULAR CHARACTER OF THE COUPLED OPERATOR
(the push deliverable: bands-vs-lines at the operator level).

Date: 2026-06-12.  Declaration: W6 section of
w_stiffness_push_declaration.md.  Self-contained (blocks rebuilt from
scratch; no cache trusted).

THE QUESTION (verbatim from the push): after coupling, does the
system's characteristic variety acquire theta-dependence in the
w-sector — is there any channel combination along which angular
derivatives of delta-w enter at second order (locally)?  If all
angular structure enters only through delta-f's own angular operator
coupled algebraically, compute the Schur complement onto the
w-channel and decide whether the induced w-w angular kernel has a
LOCAL second-derivative part (genuine angular stiffness) or is purely
nonlocal/smoothing (bands robust).

PRE-STATED VERDICT CRITERIA (hypothesis discipline — LINES is the
hoped outcome; committed BEFORE the computation below runs):
  NO-ANGULAR-STIFFNESS (bands stand at the coupled level) iff ALL of:
    (a) H[(Y,n),(w,th)] == 0 for every channel Y and direction n
        (no second-order pairing of d_th delta-w anywhere in the
        unreduced operator), AND
    (b) after the EXACT LOCAL delta-q elimination (legal because the
        q-q block is algebraic — checked, not assumed) the reduced
        static w-row carries NO delta-w term with >= 1 theta
        derivative at total derivative order >= 2 with coefficient
        nonzero on shaped (f_th != 0) backgrounds, AND
    (c) the symbol-level Schur complement onto delta-w carries no
        k_th-dependence at its leading local order beyond what (b)
        already accounts for.
  If ANY of (a)-(c) fails with a coefficient nonzero on shaped
  backgrounds, the angular-derivative door into the w-sector is OPEN
  at the coupled level, and the exact kernel below is the object Arm
  2 discretizes.  Either verdict is recorded as found; a negative is
  first-class (premise set: this metric class, this density stack,
  general static background, away from O_qq = 0).

CONVENTIONS: w6_arm1_lib.py header (binding).  All exact sympy;
rational spot evaluation where radicals obstruct symbolic closure.
Log: /tmp/w6_arm1_b.log
"""
import random
import sys
import time

import sympy as sp
from sympy import Rational as Ra

from w6_arm1_lib import (T, r, th, kap, beta, TAGS, Jets,
                         build_all_jets, FIELDS, jet_syms, blocks,
                         tan_half, qstar_expr, derad)

random.seed(661661)
t0 = time.time()
PASS, FAIL = [], []


def check(tag, cond, note=""):
    ok = bool(cond)
    (PASS if ok else FAIL).append(tag)
    print(f"W6B-{tag}: {'PASS' if ok else 'FAIL'}  {note}", flush=True)


def pshow(name, expr, cap=1800):
    e = sp.cancel(sp.together(expr))
    try:
        ef = sp.factor(e)
    except Exception:
        ef = e
    s = str(ef)
    if len(s) > cap:
        s = s[:cap] + f" ... [{len(s)} chars]"
    print(f"     {name} = {s}", flush=True)
    return e


print("=" * 72)
print("PART 0 — rebuild blocks (self-contained)")
print("=" * 72)
J, dens, raw = build_all_jets()
u, j1 = jet_syms(J)
fj, qj, wj = u['f'], u['q'], u['w']
fT, fr_, fh = j1[('f', 0)], j1[('f', 1)], j1[('f', 2)]
qT, qr_, qh = j1[('q', 0)], j1[('q', 1)], j1[('q', 2)]
wT, wr_, wh = j1[('w', 0)], j1[('w', 1)], j1[('w', 2)]
SD = sp.sqrt(r ** 2 * (1 + wj) ** 2 - fj * qj ** 2)
HT, BT, CT = blocks(J, dens['L'])       # time-on blocks (kept)
keys = [(nm, i) for nm in FIELDS for i in range(3)]
print(f"   [blocks done, {time.time()-t0:.0f}s]", flush=True)

# ====================================================================
print()
print("=" * 72)
print("PART 1 — criterion (a): the d_th delta-w pairing census")
print("=" * 72)
wthcol = {ka: HT[(ka, ('w', 2))] for ka in keys}
nzk = [f"{ka[0]}_{TAGS[ka[1]]}" for ka, v in wthcol.items() if v != 0]
print("   H[(Y,n),(w,th)] census (time-on, q-on, general w):")
for ka, v in wthcol.items():
    print(f"     H[{ka[0]}_{TAGS[ka[1]]}, w_th] = {v}")
crit_a = (len(nzk) == 0)
msg_a = "NONE - criterion (a) HOLDS" if crit_a else \
    "criterion (a) FAILS - the door is open already unreduced"
check("01", True,
      f"criterion (a) DATUM: nonzero d_th-delta-w pairings = {nzk} "
      f"({msg_a})")

print("   the c[q_rth]|E_w split (raw angular-character datum):")
pshow("H[(w,r),(q,th)]", HT[(('w', 1), ('q', 2))])
pshow("H[(w,th),(q,r)]", HT[(('w', 2), ('q', 1))])
print("   the c[w_rth]|E_f split:")
pshow("H[(f,r),(w,th)]", HT[(('f', 1), ('w', 2))])
pshow("H[(f,th),(w,r)]", HT[(('f', 2), ('w', 1))])
print("   the c[q_rth]|E_f split:")
pshow("H[(f,r),(q,th)]", HT[(('f', 1), ('q', 2))])
pshow("H[(f,th),(q,r)]", HT[(('f', 2), ('q', 1))])

# ====================================================================
print()
print("=" * 72)
print("PART 2 — q-q block locality (the elimination's legality)")
print("=" * 72)
Hqq_stat = [HT[(('q', m), ('q', n))] for m in (1, 2)
            for n in (1, 2)]
check("02", all(v == 0 for v in Hqq_stat),
      "H[(q,m),(q,n)] == 0 for ALL STATIC direction pairs (computed, "
      "not assumed): the STATIC q-q block is ALGEBRAIC — the static "
      "delta-q elimination is LOCAL (multiplication-operator "
      "inverse), valid wherever O_qq != 0")
Kqq = HT[(('q', 0), ('q', 0))]
Kqq_q0 = sp.cancel(sp.together(Kqq.subs({qj: 0, qT: 0, qr_: 0,
                                         qh: 0})))
# polar convention 1 + w > 0: resolve sqrt((1+w)^2 r^2) radicals
Kqq_q0 = Kqq_q0.replace(sp.Abs, lambda x_: x_)
Kqq_q0 = derad(Kqq_q0, r ** 2 * (1 + wj) ** 2, r * (1 + wj))
Kqq_q0 = sp.cancel(sp.together(Kqq_q0))
check("02b", Kqq != 0
      and sp.simplify(Kqq_q0 + kap * sp.sin(th) * wj * (2 + wj)
                      / (1 + wj) ** 2) == 0,
      "FINDING (time-on): H[q_T,q_T] != 0 — delta-q has SELF "
      "time-kinetic content; at q-bar = 0 it is "
      "K_qq = -kappa sin(th) w(2+w)/(1+w)^2: ZERO on undressed "
      "(w = 0) backgrounds but NONZERO on every dressed cell "
      "(W5: all shaped cells self-dress) — the delta-q channel is "
      "dynamical through its OWN kinetic term there, not only "
      "through the K_wq pairing")
print(f"   H[q_T,q_T] (time-on q-q) = {sp.cancel(sp.together(Kqq))}")
print(f"   B[q,(q,m)] = {[BT[('q', ('q', m))] for m in range(3)]}")

# ====================================================================
print()
print("=" * 72)
print("PART 3 — linearized rows as linear forms (exact engine) + gate")
print("=" * 72)
stat0 = {fT: 0, qT: 0, wT: 0}
H = {k: v.subs(stat0) for k, v in HT.items()}
B = {k: v.subs(stat0) for k, v in BT.items()}
C = {k: v.subs(stat0) for k, v in CT.items()}

FJ = {}


def fsym(nm, mi):
    mi = tuple(sorted(mi))
    k = (nm, mi)
    if k not in FJ:
        suff = ''.join(TAGS[i] for i in mi)
        FJ[k] = sp.Symbol(nm + ('_' + suff if suff else ''), real=True)
    return FJ[k]


FNAME = {'f': 'df', 'q': 'dq', 'w': 'dw'}
DIRS_S = [1, 2]


def lin_row(X):
    row = {}

    def add(key, val):
        if val == 0:
            return
        row[key] = row.get(key, 0) + val

    for Y in FIELDS:
        dY = FNAME[Y]
        add((dY, ()), C[(X, Y)])
        for m in DIRS_S:
            add((dY, ()), -J.D(B[(Y, (X, m))], m))
        for n in DIRS_S:
            add((dY, (n,)), B[(X, (Y, n))] - B[(Y, (X, n))])
            for m in DIRS_S:
                add((dY, (n,)), -J.D(H[((X, m), (Y, n))], m))
                add((dY, tuple(sorted((m, n)))), -H[((X, m), (Y, n))])
    out = {}
    for k, v in row.items():
        v = sp.cancel(sp.together(v))
        if v != 0:
            out[k] = v
    return out


rows = {X: lin_row(X) for X in FIELDS}
print(f"   [static linearized rows built, {time.time()-t0:.0f}s]",
      flush=True)

# gate: independent epsilon-second-variation route for the w-row
print("   [gate: w-row vs direct second variation ...]", flush=True)
eps = sp.Symbol('epsilon')
fb = sp.Function('fb')(r, th)
qb = sp.Function('qb')(r, th)
wb = sp.Function('wb')(r, th)
pf = sp.Function('pf')(r, th)
pq = sp.Function('pq')(r, th)
pw = sp.Function('pw')(r, th)
subfun = {}
for nm, Fb, Fp in (('f', fb, pf), ('q', qb, pq), ('w', wb, pw)):
    subfun[J.sym(nm, ())] = Fb + eps * Fp
    subfun[J.sym(nm, (0,))] = 0
    subfun[J.sym(nm, (1,))] = sp.diff(Fb, r) + eps * sp.diff(Fp, r)
    subfun[J.sym(nm, (2,))] = sp.diff(Fb, th) + eps * sp.diff(Fp, th)
Leps = dens['L'].subs(subfun, simultaneous=True)
Q2 = sp.diff(Leps, eps, 2) / 2
el_pw = (sp.diff(Q2, pw)
         - sp.diff(sp.diff(Q2, sp.diff(pw, r)), r)
         - sp.diff(sp.diff(Q2, sp.diff(pw, th)), th)).subs(eps, 0)
J2 = Jets({fb: 'f', qb: 'q', wb: 'w', pf: 'df', pq: 'dq', pw: 'dw'},
          [T, r, th], TAGS)
el_pw_j = J2.to_jets(el_pw)
mine_w = sum(cf * fsym(nm, mi) for (nm, mi), cf in rows['w'].items())
resg = sp.cancel(sp.together(sp.expand(el_pw_j - mine_w)))
if resg != 0:
    tp_ = sp.Symbol('t_par', real=True)
    e = tan_half(resg, tp_)
    okp, done, tries = True, 0, 0
    while done < 4 and tries < 200:
        tries += 1
        sub = {}
        for s in sorted(e.free_symbols, key=str):
            nm = str(s)
            if s == r:
                sub[s] = Ra(random.randint(2, 7), random.randint(1, 3))
            elif s == tp_:
                sub[s] = Ra(random.randint(1, 8), random.randint(2, 9))
            elif nm == 'f':
                sub[s] = Ra(random.randint(1, 8), random.randint(1, 4))
            elif nm == 'w':
                sub[s] = Ra(random.randint(-2, 5), 8)
            elif nm == 'q':
                sub[s] = Ra(random.randint(-5, 5), 7)
            elif nm in ('kappa', 'beta'):
                sub[s] = Ra(random.randint(-3, 3), 2)
            else:
                sub[s] = Ra(random.randint(-9, 9),
                            random.randint(1, 7))
        wv0 = sub.get(wj, 0)
        qv0 = sub.get(qj, 0)
        fv0 = sub.get(fj, 1)
        if (1 + wv0) <= 0 or sub[r]**2*(1+wv0)**2 - fv0*qv0**2 <= 0:
            continue
        if sp.cancel(e.subs(sub)) != 0:
            okp = False
        done += 1
    if okp and done == 4:
        resg = 0
check("03", resg == 0,
      "GATE: my linear-form w-row == independent "
      "epsilon-second-variation EL route (symbolic, or 4 exact "
      "rational points)")

# ====================================================================
print()
print("=" * 72)
print("PART 4 — EXACT LOCAL delta-q ELIMINATION (static, general bg)")
print("=" * 72)
rq = rows['q']
oqq = rq.get(('dq', ()), 0)
no_dq_jets = all(k[0] != 'dq' or k[1] == () for k in rq)
check("04", no_dq_jets and oqq != 0,
      "the static linearized q-row contains delta-q ALGEBRAICALLY "
      "ONLY (the dq-jet D-term cancellation realized in the engine): "
      "q-row = O_qq dq + [df, dw derivative terms]")
oqq = pshow("O_qq", oqq)
dqsol = {k: sp.cancel(sp.together(-v / oqq)) for k, v in rq.items()
         if k[0] != 'dq'}
print("   dq_sol fluctuation-jet content:")
for k in sorted(dqsol, key=str):
    print(f"     {fsym(*k)}: {'NONZERO' if dqsol[k] != 0 else '0'}")


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
print(f"   [dq_sol prolonged, {time.time()-t0:.0f}s]", flush=True)


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
print(f"   [rows reduced, {time.time()-t0:.0f}s]", flush=True)

# ====================================================================
print()
print("=" * 72)
print("PART 5 — REDUCED STATIC w-ROW: ANGULAR CONTENT (criterion b)")
print("=" * 72)
TARGETS = [('dw', (2, 2)), ('dw', (1, 2)), ('dw', (1, 1)),
           ('dw', (1, 1, 2)), ('dw', (1, 2, 2)), ('dw', (2, 2, 2)),
           ('dw', (1, 1, 1)), ('dw', (1, 1, 1, 2)),
           ('dw', (1, 1, 2, 2)), ('dw', (1, 2, 2, 2)),
           ('dw', (2, 2, 2, 2)), ('dw', (1, 1, 1, 1))]
wrow_ang = {}
print("   reduced w-row delta-w jet content (general static bg):")
for kk in TARGETS:
    cf = sp.cancel(sp.together(red['w'].get(kk, 0)))
    wrow_ang[kk] = cf
    print(f"     coeff[{fsym(*kk)}] "
          f"{'NONZERO' if cf != 0 else '== 0'}", flush=True)
c_whh = wrow_ang[('dw', (2, 2))]
print("\n   THE PURE ANGULAR DOOR (reduced w-row):")
pshow("coeff[dw_hh]", c_whh, cap=4000)
print("\n   the quartic mixed stiffness:")
pshow("coeff[dw_rrhh]", wrow_ang[('dw', (1, 1, 2, 2))], cap=4000)

# symbol cross-check of the quartic content:
kr, kh = sp.symbols('k_r k_h', real=True)
sig = {}
for X in FIELDS:
    for Y in FIELDS:
        sig[(X, Y)] = sp.cancel(sp.together(
            sum(H[((X, m), (Y, n))]
                * (kr if m == 1 else kh) * (kr if n == 1 else kh)
                for m in (1, 2) for n in (1, 2))))
quart_sym = sp.cancel(sp.together(sig[('w', 'q')] * sig[('q', 'w')]
                                  / oqq))
qs_kk = sp.expand(quart_sym).coeff(kr ** 2 * kh ** 2)
res5 = sp.cancel(sp.together(qs_kk - wrow_ang[('dw', (1, 1, 2, 2))]))
check("05", res5 == 0,
      "CROSS-CHECK: exact composed coeff[dw_rrhh] == the k_r^2 k_h^2 "
      "coefficient of sigma_wq sigma_qw / O_qq — composition engine "
      "and symbol calculus agree")

ang_open = [str(fsym(*kk)) for kk in TARGETS
            if wrow_ang[kk] != 0 and 2 in kk[1]]
check("06", True,
      f"criterion (b) DATUM: reduced static w-row angular-derivative "
      f"delta-w terms with NONZERO coefficient: {ang_open}")
# full key inventory of both reduced rows (for the Arm-2 spec):
for X in ('w', 'f'):
    nzkeys = sorted((str(fsym(*k)) for k, v in red[X].items()
                     if sp.cancel(sp.together(v)) != 0))
    print(f"   reduced {X}-row NONZERO fluctuation-jet content: "
          f"{nzkeys}", flush=True)
# checkpoint the exact reduced rows for Arm 2:
with open('/tmp/w6_arm1_reduced_rows.srepr', 'w') as fh:
    for X in ('w', 'f'):
        for k, v in red[X].items():
            vv = sp.cancel(sp.together(v))
            if vv != 0:
                fh.write(f"{X}|{k[0]}|{','.join(map(str, k[1]))}|"
                         f"{sp.srepr(vv)}\n")
print("   [wrote /tmp/w6_arm1_reduced_rows.srepr]")

# shaped-background nonvanishing at exact rational points:
print("\n   shaped-background evaluation (exact rational points):")
tp_ = sp.Symbol('t_par', real=True)
Q0 = qstar_expr(fj, fr_, fh, wj)
QP = {(): Q0}
for mi in [(1,), (2,), (1, 1), (1, 2), (2, 2),
           (1, 1, 1), (1, 1, 2), (1, 2, 2), (2, 2, 2)]:
    QP[mi] = J.D(QP[mi[:-1]], mi[-1])
QP_t = {k: tan_half(v, tp_) for k, v in QP.items()}
print(f"   [q* prolonged to 3rd order, {time.time()-t0:.0f}s]",
      flush=True)


def at_points(expr, qmode, npts=4, wsel=0):
    e = tan_half(expr, tp_)
    need = set(e.free_symbols)
    if qmode == 'star':
        for v in QP_t.values():
            need |= v.free_symbols
    need = sorted(need, key=str)
    out = []
    tries = 0
    while len(out) < npts and tries < 500:
        tries += 1
        sub = {r: Ra(random.randint(2, 7), random.randint(1, 3)),
               tp_: Ra(random.randint(1, 8), random.randint(2, 9)),
               fj: Ra(random.randint(1, 8), random.randint(1, 4)),
               fr_: Ra(random.randint(-7, 7), random.randint(1, 5)),
               fh: Ra(random.randint(-7, 7), random.randint(1, 5))}
        if sub[fr_] == 0 or sub[fh] == 0:
            continue
        # f-jets to 4th order random; w-jets identically 0 (the
        # w-bar = wsel constant slice); q-jets per qmode:
        for s in need:
            nm = str(s)
            if s in sub or s in (kap, beta):
                continue
            if nm == 'w':
                sub[s] = wsel
            elif nm.startswith('w_'):
                sub[s] = 0
            elif nm.startswith('f_') or nm == 'f':
                sub[s] = Ra(random.randint(-6, 6),
                            random.randint(1, 4))
        base = dict(sub)
        qsyms = [s for s in need if str(s) == 'q'
                 or str(s).startswith('q_')]
        if qmode == 'zero':
            for s in qsyms:
                sub[s] = 0
        elif qmode == 'star':
            for s in qsyms:
                nm = str(s)
                suff = nm[2:] if nm.startswith('q_') else ''
                mi = tuple(sorted(1 if cch == 'r' else 2
                                  for cch in suff))
                if mi not in QP_t:
                    sub[s] = 0      # (no T-jets statically)
                else:
                    sub[s] = QP_t[mi].subs(base)
        else:
            for s in qsyms:
                sub[s] = Ra(random.randint(-4, 4), 7)
        Dv = sub[r] ** 2 * (1 + wsel) ** 2 \
            - sub[fj] * sub.get(qj, 0) ** 2
        if Dv <= 0:
            continue
        out.append(sp.cancel(sp.together(e.subs(sub))))
    return out


for kk in [('dw', (2, 2)), ('dw', (1, 2)), ('dw', (1, 1, 2, 2))]:
    if wrow_ang[kk] == 0:
        continue
    for qmode in ('zero', 'star', 'free'):
        vals = at_points(wrow_ang[kk], qmode, 3)
        nzv = sum(1 for v in vals if sp.simplify(v) != 0)
        print(f"     coeff[{fsym(*kk)}] at q-bar = {qmode}: "
              f"{nzv}/{len(vals)} nonzero", flush=True)

# ====================================================================
print()
print("=" * 72)
print("PART 6 — THE REDUCED f-ROW DOOR (hard gate + q-bar = 0 datum)")
print("=" * 72)
c_fhh = sp.cancel(sp.together(red['f'].get(('dw', (2, 2)), 0)))
print(f"   coeff[dw_hh] in reduced f-row: "
      f"{'NONZERO' if c_fhh != 0 else '== 0'}")
P_j = fj * r ** 2 * fr_ ** 2 + fh ** 2
Dw0_j = fj * r ** 2 * fr_ ** 2 - fh ** 2
cf_closed = (-8 * fj * r ** 3 * fr_ ** 3 * fh ** 2
             * (2 * fj + r * fr_) * sp.sin(th)
             / (Dw0_j ** 2 * P_j))
c_fhh_k = sp.diff(c_fhh.subs(beta, 0), kap).subs(kap, 0)
vals = at_points(c_fhh_k - cf_closed, 'star', 5)
check("07", len(vals) >= 4 and all(sp.simplify(v) == 0 for v in vals),
      "HARD GATE (fluctuation-level Schur, independent of Script A's "
      "member assembly): O(kappa) coeff[dw_hh] of MY reduced f-row "
      "at q-bar = q*, w-bar = 0, beta = 0 == the four-way-verified "
      "VW5-1 door at exact rational subsonic branch points — "
      "linearize-then-eliminate == eliminate-then-linearize, proved "
      "at the operator level")
vals0 = at_points(c_fhh, 'zero', 4)
nz0 = sum(1 for v in vals0 if sp.simplify(v) != 0)
check("08", True,
      f"DATUM: the f-row dw_hh door at q-bar = 0 is "
      f"{'NONZERO' if nz0 else 'ZERO'} ({nz0}/{len(vals0)} points)")
if nz0:
    print(f"     sample value: {vals0[0]}")

# ====================================================================
print()
print("=" * 72)
print("PART 7 — SYMBOL-LEVEL SCHUR ONTO delta-w (criterion c)")
print("=" * 72)
sig_red = {}
for X in ('f', 'w'):
    for Y in ('f', 'w'):
        sig_red[(X, Y)] = sp.cancel(sp.together(
            sig[(X, Y)] - sig[(X, 'q')] * sig[('q', Y)] / oqq))
        d = sp.total_degree(sp.expand(sp.numer(sig_red[(X, Y)])),
                            kr, kh)
        print(f"   sigma_red[{X}{Y}]: k-degree {d}; "
              f"k_h-dependence: "
              f"{'yes' if sig_red[(X, Y)].has(kh) else 'no'}")
sig_w_eff = sp.together(
    sig_red[('w', 'w')] - sig_red[('w', 'f')] * sig_red[('f', 'w')]
    / sig_red[('f', 'f')])
sw_pure = sp.cancel(sp.together(sig_w_eff.subs(kr, 0)))
print("   pure-angular direction (k_r = 0):")
sw_pure = pshow("sigma_w_eff(0, k_h)", sw_pure, cap=4000)
# leading homogeneous directional character: k = lam (1, s):
lam, s_ = sp.symbols('lambda s', positive=True)
sw_dir = sig_w_eff.subs({kr: lam, kh: lam * s_})
sw_dir = sp.cancel(sp.together(sw_dir))
numd, dend = sp.fraction(sw_dir)
pn = sp.Poly(sp.expand(numd), lam)
pd = sp.Poly(sp.expand(dend), lam)
lead = sp.cancel(pn.LC() / pd.LC() * lam ** (pn.degree()
                                             - pd.degree()))
print(f"   leading high-frequency symbol along (1, s): degree "
      f"{pn.degree() - pd.degree()} in lambda")
lead_s = sp.cancel(sp.together(pn.LC() / pd.LC()))
sdep = lead_s.has(s_)
check("09", True,
      f"criterion (c) DATUM: sigma_w_eff(0,k_h) "
      f"{'== 0' if sw_pure == 0 else 'NONZERO'}; leading directional "
      f"symbol {'DEPENDS on the angular direction s' if sdep else 'is angular-direction-blind'}")
if sw_pure != 0:
    # is the pure-angular symbol a square root of definite sign?
    print("   [sign analysis of sigma_w_eff(0,k_h) deferred to "
          "script C tables]")

# ====================================================================
print()
print("=" * 72)
print("PART 8 — TIME-ON: kinetic matrix + characteristic cones")
print("=" * 72)
om = sp.Symbol('omega', real=True)
kvec = {0: om, 1: kr, 2: kh}
sig3 = {}
for X in FIELDS:
    for Y in FIELDS:
        sig3[(X, Y)] = sp.cancel(sp.together(
            sum(HT[((X, m), (Y, n))] * kvec[m] * kvec[n]
                for m in range(3) for n in range(3))))
print("   time-kinetic matrix K[X_T, Y_T] (time-on blocks):")
Kmat = sp.zeros(3, 3)
for i, X in enumerate(FIELDS):
    for jx, Y in enumerate(FIELDS):
        Kmat[i, jx] = HT[((X, 0), (Y, 0))]
        if jx >= i and Kmat[i, jx] != 0:
            pshow(f"K[{X},{Y}]", Kmat[i, jx])
check("10", Kmat[1, 1] != 0 and Kmat[0, 1] == 0 and Kmat[0, 2] == 0,
      "kinetic matrix structure: K_fq = K_fw = 0 (delta-f's time row "
      "decouples kinetically); K_qq != 0 (finding 02b); the (w,q) "
      "kinetic sub-block [[K_ww, K_wq],[K_wq, K_qq]] is the "
      "dynamical pairing — signature tabled in script C")
M = sp.Matrix(3, 3, lambda i, jx: sig3[(FIELDS[i], FIELDS[jx])])
oqq_t = CT[('q', 'q')]
print("   [characteristic-variety convention: the q-q slot carries "
      "the ALGEBRAIC block C_qq (the D-term corrections are "
      "subprincipal); V = det of the DN-weighted symbol]")
Mq = M.copy()
Mq[1, 1] = oqq_t
Vk0 = sp.cancel(sp.together(Mq.det().subs(kh, 0)))
num0 = sp.numer(Vk0)
cone_res = sp.cancel(sp.together(num0.subs(om ** 2,
                                           fj ** 2 * kr ** 2)))
cone_factor = (cone_res == 0)
print("   V(omega, k_r, 0) numerator factored:")
pshow("V|_{k_h=0}", num0, cap=3000)
check("11", True,
      f"DATUM: the wave cone omega^2 = f^2 k_r^2 "
      f"{'IS a factor of V at k_h = 0 (survives coupling)' if cone_factor else 'is NOT a factor of V at k_h = 0 (coupling shifts the cones)'}")
print(f"   [done, {time.time()-t0:.0f}s]")

print(f"\nW6 ARM-1 SCRIPT B: {len(PASS)} PASS / {len(FAIL)} FAIL")
for x in FAIL:
    print("FAILED:", x)
sys.exit(0 if not FAIL else 1)
