#!/usr/bin/env python3
"""W6 ARM-1 — SCRIPT A: THE UNREDUCED 3-FIELD FLUCTUATION OPERATOR.

Date: 2026-06-12.  Driver: W6 Arm-1 agent.  Declaration: W6 section of
w_stiffness_push_declaration.md (binding).  METRIC-LED: every block is
a second derivative of the derived density S = C1 + kappa Delta_w
+ beta D_cell on the q-on time-on class (w6_arm1_lib.py header).

DELIVERABLE: the exact (H, B, C) blocks of the quadratic fluctuation
form in (delta-f, delta-q, delta-w) about a GENERAL background
(f, q, w)(T, r, theta) — every entry's exact derivative content —
posed UNREDUCED (no q-elimination; the elimination breaks down on
Delta_w).

PRE-STATED FAILURE CRITERIA (hypothesis discipline; any FAIL = the
operator is mis-derived, STOP, nothing downstream is valid):
  GA-1  L_total must be FIRST-ORDER in all three fields' jets.
  GA-2  sqrt(-g) and the Gamma-Gamma split identity
        sqrt(-g) R = LGG + div V must hold exactly (provenance).
  GA-3  C1 convention locks: static literature form (V2-05) and the
        time-row f_T^2 coefficient -(1/4) sqrt(-g)/f^2 (V1-03,
        q-on/w-on generalization; VA4 invariant reading).
  GA-4  the time-on w-channel second-jet row of MY E_w must equal
        kappa x the VW5-1 twelve-entry row (V2-15) exactly,
        including c[q_TT] = 2 r q sin/((1+w)^2 sqrt(D)).
  GA-5  the static (w,q)-second-jet inventory of the kappa-part must
        reproduce the VW5-1 13-zero set + closed forms (V2-01/02),
        in particular c[w_thth] == 0 in all three rows at all q.
  GA-6  kappa = 0 cross blocks must reproduce VW2/V1-25:
        C_qw = sin f_r f_th (beta-free), C_qq = the C1 q-Hessian.
  GA-7  at q = 0 the species' w-EL content must equal
        EL_w[W_wave + D_alg] identically (the W5 surrogate; this is
        what certifies the W4/W5 pencil limits as corollaries).
  GA-8  HARD GATE — the VW5-1 f-row door as the q*-elimination
        corollary of MY operator blocks: the member assembly
        -(dE_q[Dw]/dw_th + dE_q[Dw]/dq_th * dq*/dw)/L_qq
        * dE_f[C1]/dq_th must equal the four-way-verified closed form
        c_f[w_thth] = -8 f r^3 f_r^3 f_th^2 (2f + r f_r) sin
        / (Delta_w^2 P) at exact rational subsonic branch points.

Log: /tmp/w6_arm1_a.log     Checkpoint: /tmp/w6_arm1_blocks.srepr
"""
import random
import sys
import time

import sympy as sp
from sympy import Rational as Ra

from w6_arm1_lib import (T, r, th, ph, kap, beta, COORDS, TAGS, CC,
                         geom, gg_split, Jets, build_fields,
                         build_metric, build_LC1, build_Dcell,
                         build_all_jets, FIELDS, jet_syms, blocks,
                         save_blocks, tan_half, qstar_expr)

random.seed(660660)
t0 = time.time()
PASS, FAIL = [], []


def check(tag, cond, note=""):
    ok = bool(cond)
    (PASS if ok else FAIL).append(tag)
    print(f"W6A-{tag}: {'PASS' if ok else 'FAIL'}  {note}", flush=True)


print("=" * 72)
print("PART 0 — build the density stack (q-on, time-on, exact)")
print("=" * 72)
J, dens, raw = build_all_jets()
f, q, w, g4, Dfield, sq = raw[0], raw[1], raw[2], raw[3], raw[4], raw[5]
V4 = raw[6]
u, j1 = jet_syms(J)
fj, qj, wj = u['f'], u['q'], u['w']
fT, fr_, fh = j1[('f', 0)], j1[('f', 1)], j1[('f', 2)]
qT, qr_, qh = j1[('q', 0)], j1[('q', 1)], j1[('q', 2)]
wT, wr_, wh = j1[('w', 0)], j1[('w', 1)], j1[('w', 2)]
SD = sp.sqrt(r ** 2 * (1 + wj) ** 2 - fj * qj ** 2)
print(f"   [densities built, {time.time()-t0:.0f}s]", flush=True)

check("00", sp.cancel(sp.together(-g4.det() - sq ** 2)) == 0,
      "-det g == (r sin sqrt(D)/(1+w))^2 (own determinant)")

# GA-1: first-order check
all_second = [J.sym(nm, (i, jx)) for nm in FIELDS
              for i in range(3) for jx in range(i, 3)]
check("01", all(not dens['L'].has(s) for s in all_second),
      "GA-1: L = C1 + kappa Delta_w + beta D_cell is FIRST-ORDER in "
      "all jets of all three fields (no second-jet symbol appears)")

# GA-2: split identity sqrt(-g) R = LGG + div V (provenance anchor)
print("   [Ricci scalar for the split identity (heavy) ...]",
      flush=True)
_, _, _, Rsc = geom(g4, [T, r, th, ph])
divV = sum(sp.diff(V4[a], [T, r, th, ph][a]) for a in range(4))
split_res = sp.simplify(sp.together(sq * Rsc - (J  # noqa: F841
                        and 0) - divV) - sp.together(0))
# (compute in field form, then compare)
LGG_field = sp.together(sq * Rsc - divV)
LGG_built = sp.together(dens['LGG'])
# convert field form to jets for the comparison:
LGG_field_j = J.to_jets(sp.expand(LGG_field))
diff_split = sp.cancel(sp.together(sp.expand(LGG_field_j - LGG_built)))
check("02", diff_split == 0,
      "GA-2: sqrt(-g) R == LGG + sum_a D_a V^a EXACTLY on the q-on "
      "time-on class (the species representative's provenance)")

# GA-3: C1 locks
LC1_static = dens['LC1'].subs({fT: 0, qT: 0, wT: 0})
L_C1_lit = (Ra(1, 4) * r * sp.sin(th)
            * (fj * r ** 2 * (1 + wj) ** 2 * fr_ ** 2
               - 2 * fj * qj * fr_ * fh + fh ** 2)
            / ((1 + wj) * fj * SD))
check("03a", sp.cancel(sp.together(sp.radsimp(LC1_static - L_C1_lit)))
      == 0,
      "GA-3: static C1 == literature form (V2-05) on the q-on w-on "
      "class")
cfT2 = sp.cancel(sp.together(sp.diff(dens['LC1'], fT, 2) / 2))
check("03b", sp.cancel(sp.together(
    cfT2 + r * sp.sin(th) * SD / (4 * fj ** 2 * (1 + wj)))) == 0,
      "GA-3: C1 f_T^2 coefficient = -(1/4) sqrt(-g)/f^2 = "
      "-r sin sqrt(D)/(4 f^2 (1+w)): STRICTLY NEGATIVE at all "
      "(q, w) — the VA4 invariant reading generalizes to the full "
      "class")

# ====================================================================
print()
print("=" * 72)
print("PART 1 — THE BLOCKS (H, B, C) of the quadratic fluctuation form")
print("=" * 72)
H, B, C = blocks(J, dens['L'])
print(f"   [blocks done, {time.time()-t0:.0f}s]", flush=True)
keys = [(nm, i) for nm in FIELDS for i in range(3)]


def cname(k):
    return f"{k[0]}_{TAGS[k[1]]}"


nzH = {(a, b): v for (a, b), v in H.items() if v != 0}
print(f"   nonzero H entries (of 45 independent): "
      f"{len({tuple(sorted((cname(a), cname(b)))) for a, b in nzH})}")
for a in keys:
    for b in keys:
        if keys.index(b) < keys.index(a):
            continue
        v = H[(a, b)]
        if v != 0:
            print(f"     H[{cname(a)},{cname(b)}] = {v}")
print()
for nm in FIELDS:
    for b in keys:
        v = B[(nm, b)]
        if v != 0:
            print(f"     B[{nm},{cname(b)}] = {v}")
print()
for a in FIELDS:
    for b in FIELDS:
        if FIELDS.index(b) < FIELDS.index(a):
            continue
        v = C[(a, b)]
        if v != 0:
            print(f"     C[{a},{b}] = {sp.factor(v)}")
print(flush=True)

# second-jet coefficient extraction from H:


def sj_coeff(rowX, Y, m, n):
    """coefficient of Y_{mn} (m<=n) in row X of the EL system."""
    if m == n:
        return -H[((rowX, m), (Y, m))]
    return -(H[((rowX, m), (Y, n))] + H[((rowX, n), (Y, m))])


# GA-4: time-on w-row == kappa x V2-15 (twelve entries)
tgt_row3 = {
    ('w', 0, 0): -4 * r ** 3 * sp.sin(th) / ((1 + wj) * fj * SD),
    ('w', 0, 1): 0, ('w', 0, 2): 0,
    ('w', 1, 1): 4 * r ** 3 * fj * sp.sin(th) / ((1 + wj) * SD),
    ('w', 1, 2): 0, ('w', 2, 2): 0,
    ('q', 0, 0): 2 * r * qj * sp.sin(th) / ((1 + wj) ** 2 * SD),
    ('q', 0, 1): 0, ('q', 0, 2): 0, ('q', 1, 1): 0,
    ('q', 1, 2): -2 * r * fj * sp.sin(th) / ((1 + wj) ** 2 * SD),
    ('q', 2, 2): 0}
ok4 = True
for (Y, m, n), tv in tgt_row3.items():
    mine = sj_coeff('w', Y, m, n)
    res = sp.cancel(sp.together(sp.radsimp(mine - kap * tv)))
    if res != 0:
        ok4 = False
        print(f"   GA-4 MISMATCH at ({Y},{m},{n}): {res}")
check("04", ok4,
      "GA-4: my E_w second-jet row == kappa x VW5-1 V2-15 EXACTLY "
      "(time-on, q-on, general w): c[w_TT], c[w_rr] (cone -1/f^2 at "
      "all q), c[q_TT] = 2 kappa r q sin/((1+w)^2 sqrt(D)) "
      "(the dynamical delta-q door), c[q_rth], and the SIX zeros "
      "incl. c[w_thth] = 0")

# GA-5: static inventory of the kappa part vs VW5-1 V2-01/02.
# RUN-1 RECORD (hypothesis discipline; kept, not erased): the first
# version of this gate demanded the V2-01/02 closed forms VERBATIM
# for all five nonzero entries and FAILED — the V2 inventory belongs
# to the UNSUBTRACTED species channels E[sqrt(-g)R], while the
# declared W6 system carries the banked representative
# Delta_w = LGG - LGG|_{w-content=0} (V2-13/V2-18: the subtraction is
# NOT EL-invisible in the f- and q-rows; it is what makes the species
# vanish identically on w == 0, i.e. the macro gate).  The correct
# decomposition gate: all w-PAIRING entries (subtraction-blind) match
# V2 verbatim; the f-row q-pairing carries EXACTLY the w-free
# reference shift  -r sin/sqrt(D0), D0 = r^2 - f q^2.
stat0 = {fT: 0, qT: 0, wT: 0}
SD0 = sp.sqrt(r ** 2 - fj * qj ** 2)
expected_zero = {('w', 'w_rth'), ('w', 'w_thth'), ('w', 'q_rr'),
                 ('w', 'q_thth'), ('q', 'w_rr'), ('q', 'w_thth'),
                 ('q', 'q_rr'), ('q', 'q_rth'), ('q', 'q_thth'),
                 ('f', 'w_rr'), ('f', 'w_thth'), ('f', 'q_rr'),
                 ('f', 'q_thth')}
namepairs = {'w_rr': ('w', 1, 1), 'w_rth': ('w', 1, 2),
             'w_thth': ('w', 2, 2), 'q_rr': ('q', 1, 1),
             'q_rth': ('q', 1, 2), 'q_thth': ('q', 2, 2)}
inv = {}
for chX in FIELDS:
    for nm2, (Y, m, n) in namepairs.items():
        e = sj_coeff(chX, Y, m, n).subs(stat0)
        e = sp.cancel(sp.together(sp.diff(e, kap)))  # kappa part
        inv[(chX, nm2)] = e
zs = {k for k, v in inv.items() if v == 0}
tgt5 = {('w', 'w_rr'): 4 * fj * r ** 3 * sp.sin(th) / ((1 + wj) * SD),
        ('w', 'q_rth'): -2 * fj * r * sp.sin(th) / ((1 + wj) ** 2 * SD),
        ('q', 'w_rth'): -2 * fj * r * sp.sin(th) / ((1 + wj) ** 2 * SD),
        ('f', 'w_rth'): -2 * qj * r * sp.sin(th) / ((1 + wj) ** 2 * SD)}
ok5a = (zs == expected_zero) and all(
    sp.cancel(sp.together(sp.radsimp(inv[k] - v))) == 0
    for k, v in tgt5.items())
check("05a", ok5a,
      "GA-5a: the 13 V2-01 zeros hold for the W6 system's kappa part "
      "(c[w_thth] == 0 in ALL rows at all q — no pure angular "
      "operator anywhere), and all four w-PAIRING closed forms match "
      "V2-02 verbatim (the subtraction is w-blind)")
shift5 = sp.cancel(sp.together(sp.radsimp(
    inv[('f', 'q_rth')]
    - (r * sp.sin(th) / ((1 + wj) * SD) - r * sp.sin(th) / SD0))))
check("05b", shift5 == 0,
      "GA-5b: c_f[q_rth] of the kappa part == r sin [1/((1+w) "
      "sqrt(D)) - 1/sqrt(D0)] — the V2-02 unsubtracted value MINUS "
      "its exact w == 0 reference (the representative's subtraction "
      "carried in the f-row, as VW5-1 V2-18 requires; vanishes "
      "identically at w = 0: the macro/undressed gate is exact)")

# the split of c[q_rth] in E_w (the angular-character raw datum):
print("   THE SPLIT (new structure, no banked target):")
print(f"     H[(w,r),(q,th)] = {H[(('w',1),('q',2))]}")
print(f"     H[(w,th),(q,r)] = {H[(('w',2),('q',1))]}")
print(f"     H[(f,r),(w,th)] = {H[(('f',1),('w',2))]}")
print(f"     H[(f,th),(w,r)] = {H[(('f',2),('w',1))]}")
print(f"     H[(w,th),(w,th)] = {H[(('w',2),('w',2))]}")
print(f"     H[(f,th),(w,th)] = {H[(('f',2),('w',2))]}")
print(f"     H[(q,th),(w,th)] = {H[(('q',2),('w',2))]}", flush=True)

# GA-6: kappa = 0 static cross blocks (V1-25 targets, independent
# literature-form rebuild):
Cqw0 = sp.cancel(sp.together(
    C[('q', 'w')].subs(stat0).subs(kap, 0).subs({qj: 0, wj: 0})))
Cqq0 = sp.cancel(sp.together(
    C[('q', 'q')].subs(stat0).subs(kap, 0).subs({qj: 0, wj: 0})))
check("06", sp.simplify(Cqw0 - sp.sin(th) * fr_ * fh) == 0
      and sp.simplify(Cqq0 - Ra(1, 4) * sp.sin(th)
                      * (fj * r ** 2 * fr_ ** 2 + fh ** 2)
                      / r ** 2) == 0
      and not Cqw0.has(beta),
      "GA-6: kappa = 0 cross blocks at q = w = 0 reproduce VW2/V1-25: "
      "C_qw = sin f_r f_th (beta-free), C_qq = (1/4) sin "
      "(f r^2 f_r^2 + f_th^2)/r^2 > 0")

# ====================================================================
print()
print("=" * 72)
print("PART 2 — GA-7: q = 0 species w-EL == EL_w[W_wave + D_alg]")
print("=" * 72)
print("   [EL2 of Delta_w (heavy) ...]", flush=True)
Ew_Dw = J.EL2(dens['Dw'], 'w')
q0_all = {qj: 0, qT: 0, qr_: 0, qh: 0}
for i in range(3):
    for jx in range(i, 3):
        q0_all[J.sym('q', (i, jx))] = 0
Ew_Dw_q0 = Ew_Dw.subs(q0_all)
# de-root sqrt(r^2 (1+w)^2) on the polar convention:
from w6_arm1_lib import derad  # noqa: E402
Ew_Dw_q0 = Ew_Dw_q0.replace(sp.Abs, lambda x_: x_)
Ew_Dw_q0 = derad(Ew_Dw_q0, r ** 2 * (1 + wj) ** 2, r * (1 + wj))
W_wave_j = 2 * r ** 2 * sp.sin(th) / (1 + wj) ** 2 \
    * (wT ** 2 / fj - fj * wr_ ** 2)
D_alg_j = -sp.sin(th) * fh ** 2 / (2 * fj ** 2 * (1 + wj) ** 2)
Ew_WD = J.EL2(W_wave_j + D_alg_j, 'w')
res7 = sp.cancel(sp.together(sp.expand(Ew_Dw_q0 - Ew_WD)))
check("07", res7 == 0,
      "GA-7: E_w[Delta_w]|_{q=0} == EL_w[W_wave + D_alg] IDENTICALLY "
      "in all (f,w) jets — the W6 declaration's '(W_wave + D_alg)' is "
      "exactly this object's q = 0 face; the W4/W5 pencils and the "
      "(1 - 2 kappa/f) factor structure are corollaries of THIS "
      "operator at q-bar = 0 frozen channels")

# ====================================================================
print()
print("=" * 72)
print("PART 3 — GA-8: THE HARD GATE (the VW5-1 door as MY corollary)")
print("=" * 72)
print("   [EL2 rows for the member assembly (heavy) ...]", flush=True)
Eq_Dw = J.EL2(dens['Dw'], 'q')
Ef_C1 = J.EL2(dens['LC1'], 'f')
L_qq_C1 = sp.diff(dens['LC1'], qj, 2)
# static restriction of everything (T-jets of all fields -> 0):
statall = dict(stat0)
for nm in FIELDS:
    for i in range(3):
        for jx in range(i, 3):
            if 0 in (i, jx):
                statall[J.sym(nm, (i, jx))] = 0
Eq_Dw_s = Eq_Dw.subs(statall)
Ef_C1_s = Ef_C1.subs(statall)
L_qq_s = L_qq_C1.subs(stat0)
c_qwth = sp.diff(Eq_Dw_s, wh)     # dE_q[Dw]/dw_th  (my q-row entry)
c_qqth = sp.diff(Eq_Dw_s, qh)     # dE_q[Dw]/dq_th  (my q-row entry)
A_mem = sp.diff(Ef_C1_s, qh)      # dE_f[C1]/dq_th  (my f-row entry)
Q0 = qstar_expr(fj, fr_, fh, wj)
dQ0dw = sp.diff(Q0, wj)
Q0_r, Q0_h = J.D(Q0, 1), J.D(Q0, 2)
pred_mem = -(c_qwth + c_qqth * dQ0dw) / L_qq_s * A_mem
P_j = fj * r ** 2 * fr_ ** 2 + fh ** 2
Dw0_j = fj * r ** 2 * fr_ ** 2 - fh ** 2
cf_closed = (-8 * fj * r ** 3 * fr_ ** 3 * fh ** 2
             * (2 * fj + r * fr_) * sp.sin(th) / (Dw0_j ** 2 * P_j))
tp_ = sp.Symbol('t_par', real=True)
pm_t = tan_half(pred_mem, tp_)
cl_t = tan_half(cf_closed, tp_)
Q0_t, Q0r_t, Q0h_t = [tan_half(x, tp_) for x in (Q0, Q0_r, Q0_h)]
done, ok8 = 0, True
while done < 6:
    sub = {r: Ra(random.randint(2, 7), random.randint(1, 3)),
           tp_: Ra(random.randint(1, 8), random.randint(2, 9)),
           fj: Ra(random.randint(1, 8), random.randint(1, 4)),
           fr_: Ra(random.randint(-7, 7), random.randint(1, 5)),
           fh: Ra(random.randint(-7, 7), random.randint(1, 5)),
           wj: 0, wr_: 0, wh: 0}
    for nm in FIELDS:
        for i in range(1, 3):
            for jx in range(i, 3):
                s = J.sym(nm, (i, jx))
                if s not in sub:
                    sub[s] = (0 if nm == 'w'
                              else Ra(random.randint(-6, 6),
                                      random.randint(1, 4)))
    if sub[fr_] == 0 or sub[fh] == 0:
        continue
    if sub[fj] * sub[r] ** 2 * sub[fr_] ** 2 - sub[fh] ** 2 <= 0:
        continue                       # subsonic branch points only
    base = dict(sub)
    sub[qj] = Q0_t.subs(base)
    sub[qr_] = Q0r_t.subs(base)
    sub[qh] = Q0h_t.subs(base)
    v1 = sp.cancel(pm_t.subs(sub))
    v2 = sp.cancel(cl_t.subs(sub))
    if sp.simplify(v1 - v2) != 0:
        ok8 = False
        print(f"   GA-8 MISMATCH: {v1} vs {v2}")
    done += 1
check("08", ok8,
      "GA-8 HARD GATE: the four-way-verified VW5-1 door "
      "c_f[w_thth] = -8 f r^3 f_r^3 f_th^2 (2f + r f_r) sin/"
      "(Delta_w^2 P) is the q*-elimination corollary of MY operator "
      "blocks [-(dE_q[Dw]/dw_th + dE_q[Dw]/dq_th dq*/dw)/L_qq "
      "x dE_f[C1]/dq_th] at 6 exact rational subsonic branch points "
      "(w = 0)")

# ====================================================================
print()
print("=" * 72)
print("PART 4 — checkpoint the blocks for scripts B/C")
print("=" * 72)
extra = {'Eq_Dw_static': Eq_Dw_s, 'Ef_C1_static': Ef_C1_s,
         'L_qq_C1_static': L_qq_s}
save_blocks('/tmp/w6_arm1_blocks.srepr', J, H, B, C, extra)
print("   wrote /tmp/w6_arm1_blocks.srepr")

print(f"\nW6 ARM-1 SCRIPT A: {len(PASS)} PASS / {len(FAIL)} FAIL "
      f"({time.time()-t0:.0f}s)")
for x in FAIL:
    print("FAILED:", x)
sys.exit(0 if not FAIL else 1)
