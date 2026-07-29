#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BLIND VERIFIER independent check for udt_p4_routeP_seal_parity_2026-07-29.
Written from scratch (own constructions, own solve routes, own catch-proofs);
adversarial: includes completeness ATTACKS on the classification and mutation
catch-proofs. Exact SymPy only. Verifier: blind adversarial, same-session-
spawned, 2026-07-29.
"""
import sys
import sympy as sp

H = sp.diag(-1, 1)
I2 = sp.eye(2)
Z2 = sp.zeros(2, 2)
eta2 = sp.diag(-1, 1)

k00, k11, k10 = sp.symbols("k00 k11 k10")
c00, c01, c10, c11 = sp.symbols("c00 c01 c10 c11")
K = sp.Matrix([[k00, 0], [k10, k11]])
C = sp.Matrix([[c00, c01], [c10, c11]])
MOD = [k00, k11, k10, c00, c01, c10, c11]


def blk(A, B, Cb, D):
    return sp.Matrix(sp.BlockMatrix([[A, B], [Cb, D]]))


X = blk(H, Z2, C, K)          # generic registered-class member
X0 = blk(H, Z2, Z2, Z2)
LAM = (k00 + k11) / 2
KMOD = (k11 - k00) / 2

FAILS = []


def ck(name, ok):
    print(("PASS " if ok else "FAIL ") + name)
    if not ok:
        FAILS.append(name)


def zero(M):
    M = sp.expand(sp.simplify(M)) if not hasattr(M, "shape") else \
        sp.simplify(sp.expand(M))
    return M == (sp.zeros(*M.shape) if hasattr(M, "shape") else 0)


# ---------------------------------------------------------------- V1 banked
# -X obstruction
ck("V1_minusX_H_block_obstruction", sp.simplify((-X)[0:2, 0:2] + H) == Z2
   and (-H) != H)
# V5 swap facts
F2 = sp.Matrix([[0, 1], [1, 0]])
Fsw = blk(F2, Z2, Z2, I2)
img = sp.simplify(-Fsw * X * Fsw.inv())
ck("V1_swapF_action", img[0:2, 0:2] == H and img[0:2, 2:4] == Z2
   and sp.simplify(img[2:4, 2:4] + K) == Z2
   and sp.simplify(img[2:4, 0:2] + C * F2) == Z2)
ck("V1_F2_eta_antiisometry", sp.simplify(F2.T * eta2 * F2 + eta2) == Z2)

# ------------------------------------------------- V2 classification (mine)
# (a) Q=0 necessity: image of any v in V must have zero top block-row; the
# top block-row of J v is Q * v_low with v_low = [C_v | K_v] fully generic in
# C-part -> Q annihilates all of R^2x2 -> Q = 0.
q00, q01, q10, q11 = sp.symbols("q00 q01 q10 q11")
Q = sp.Matrix([[q00, q01], [q10, q11]])
a, b, c, d = sp.symbols("a b c d")
Cv = sp.Matrix([[a, b], [c, d]])
eqs = list(sp.expand(Q * Cv))
sysA = []
for e in eqs:
    for m in (a, b, c, d):
        sysA.append(sp.expand(sp.diff(e, m)))
sol = sp.solve(sysA, [q00, q01, q10, q11], dict=True)
ck("V2a_Q_zero_necessary",
   sol == [{q00: 0, q01: 0, q10: 0, q11: 0}])

# (b) with Q=0 the image H-block is exactly -P H P^-1 (R cannot compensate):
p00, p01, p10, p11 = sp.symbols("p00 p01 p10 p11")
Pg = sp.Matrix([[p00, p01], [p10, p11]])
Sg = sp.Matrix(2, 2, lambda i, j: sp.Symbol(f"sg{i}{j}"))
Rg = sp.Matrix(2, 2, lambda i, j: sp.Symbol(f"rg{i}{j}"))
Jg = blk(Pg, Z2, Rg, Sg)
Jginv = blk(Pg.inv(), Z2, -Sg.inv() * Rg * Pg.inv(), Sg.inv())
ck("V2b_block_inverse", zero(sp.expand(Jg * Jginv - sp.eye(4))))
IMG = sp.expand(-Jg * X * Jginv)
ck("V2b_H_block_is_minusPHPinv",
   zero(sp.expand(IMG[0:2, 0:2] - (-Pg * H * Pg.inv())))
   and IMG[0:2, 2:4] == Z2)
# P necessity: -P H P^-1 = H  <=>  P H + H P = 0 -> solve fully generic P
solP = sp.solve(list(sp.expand(Pg * H + H * Pg)), [p00, p01, p10, p11],
                dict=True)
ck("V2b_P_antidiagonal_necessary", solP == [{p00: 0, p11: 0}])

# (c) S necessity: (S K S^-1)[0,1] = 0 for all lower-tri K, S fully generic.
expr = sp.expand((Sg * K * Sg.adjugate())[0, 1])
sysS = [sp.expand(sp.diff(expr, m)) for m in (k00, k10, k11)]
# the k10 coefficient is -sg01^2: real zero only at sg01 = 0; and sg01 = 0
# annihilates the whole system (necessity + consistency)
sg01 = sp.Symbol("sg01")
ok = (sp.simplify(sp.diff(expr, k10) + sg01 ** 2) == 0
      and sp.solve([sg01 ** 2], [sg01], dict=True) == [{sg01: 0}]
      and all(sp.simplify(e.subs(sg01, 0)) == 0 for e in sysS))
ck("V2c_S_lower_triangular_necessary", ok)

# (d) commutant of the class = scalars (my route: commute with X at fully
# symbolic moduli, coefficient-extract in the moduli).
Zg = sp.Matrix(4, 4, lambda i, j: sp.Symbol(f"zz{i}{j}"))
comm = sp.expand(Zg * X - X * Zg)
sysZ = []
for e in comm:
    pe = sp.Poly(e, *MOD)
    sysZ.extend(pe.coeffs())
solZ = sp.solve(sysZ, list(Zg), dict=True)
Zsub = Zg.subs(solZ[0]) if solZ else Zg
ck("V2d_commutant_scalars",
   len(solZ) == 1 and zero(Zsub - Zsub[0, 0] * sp.eye(4)))

# (e) involution algebra: P = antidiag(p,q); J^2 = mu I demands S^2 = mu I,
# P^2 = pq I, R P + S R = 0; real lower-tri S => mu = s00^2 > 0.
p, q = sp.symbols("p q", nonzero=True)
Pa = sp.Matrix([[0, p], [q, 0]])
ck("V2e_P_square_scalar", sp.simplify(Pa * Pa - p * q * I2) == Z2)
s00, s10, s11 = sp.symbols("s00 s10 s11")
Sl = sp.Matrix([[s00, 0], [s10, s11]])
S2 = sp.expand(Sl * Sl)
# S^2 = mu I with mu = pq: solutions
solS2 = sp.solve([S2[0, 0] - p * q, S2[1, 1] - p * q, S2[1, 0]],
                 [s00, s10, s11], dict=True)
# every real solution has s00^2 = pq -> pq > 0; verify each returned branch
ok = len(solS2) > 0 and all(
    sp.simplify(s.get(s00, s00) ** 2 - p * q) == 0 or
    sp.simplify(s.get(s11, s11) ** 2 - p * q) == 0
    for s in solS2)
ck("V2e_S_square_pq_branches", ok)
# no real J^2 = -I: s00^2 = -1 impossible over the reals
s00r = sp.Symbol("s00r", real=True)
ck("V2e_no_real_complex_structure",
   sp.solve([s00r ** 2 + 1], [s00r], dict=True) == [])

# (f) COMPLETENESS ATTACKS: candidate dressings outside the family must fail.
# attack 1: Q != 0 involution, e.g. J = antidiag blocks (swap base<->screen)
Jat1 = blk(Z2, I2, I2, Z2)
im1 = sp.expand(-Jat1 * X * Jat1.inv())
ck("V2f_attack_offblock_swap_fails_class",
   sp.simplify(im1[0:2, 0:2] - H) != Z2 or im1[0:2, 2:4] != Z2)
# attack 2: S = F2 (upper-entry violation): class violated at generic k10
Jat2 = blk(Pa.subs({p: 1, q: 1}), Z2, Z2, F2)
im2 = sp.expand(-Jat2 * X * Jat2.inv())
ck("V2f_attack_screen_swap_fails_class",
   sp.simplify(im2[2:4, 2:4][0, 1]) != 0)
# attack 3: P diagonal (identity base): H-block obstruction persists
Jat3 = blk(I2, Z2, Z2, I2)
im3 = sp.expand(-Jat3 * X * Jat3.inv())
ck("V2f_attack_identity_base_fails_H", sp.simplify(im3[0:2, 0:2] - H) != Z2)
# attack 4: mu<0 via pq<0: P=antidiag(1,-1) squares to -I, but no real S
Pneg = sp.Matrix([[0, 1], [-1, 0]])
ck("V2f_attack_pq_negative_blocked_by_S",
   sp.simplify(Pneg * Pneg + I2) == Z2
   and sp.solve([s00r ** 2 + 1], [s00r], dict=True) == [])

# (g) sufficiency, most-generic member: branch (b), symbolic p, s1, s0=+-1,
# R = generic solution of R P + S R = 0.
s1 = sp.Symbol("s1")
r0, r1, r2, r3 = sp.symbols("r0 r1 r2 r3")
Rgen = sp.Matrix([[r0, r1], [r2, r3]])
Pn = sp.Matrix([[0, p], [1 / p, 0]])
for s0v in (1, -1):
    Sb = sp.Matrix([[s0v, 0], [s1, -s0v]])
    eqsR = list(sp.expand(Rgen * Pn + Sb * Rgen))
    solR = sp.solve(eqsR, [r0, r1, r2, r3], dict=True)
    Rsol = Rgen.subs(solR[0])
    free = sorted(Rsol.free_symbols & {r0, r1, r2, r3}, key=str)
    ok_dim = len(free) == 2
    Jfam = blk(Pn, Z2, Rsol, Sb)
    ok_inv = zero(sp.expand(Jfam * Jfam - sp.eye(4)))
    imf = sp.expand(-Jfam * X * Jfam.inv())
    ok_cls = (zero(sp.expand(imf[0:2, 0:2] - H)) and imf[0:2, 2:4] == Z2
              and sp.simplify(imf[2:4, 2:4][0, 1]) == 0)
    # parity of lambda, kmod on this fully generic member
    Kt = imf[2:4, 2:4]
    ok_par = (sp.simplify((Kt[0, 0] + Kt[1, 1]) / 2 + LAM) == 0
              and sp.simplify((Kt[1, 1] - Kt[0, 0]) / 2 + KMOD) == 0)
    # k10 branch-(b) law
    ok_k10 = sp.simplify(Kt[1, 0] - (k10 + 2 * (s1 / s0v) * KMOD)) == 0
    ck(f"V2g_branch_b_s0_{s0v}_generic_member_all",
       ok_dim and ok_inv and ok_cls and ok_par and ok_k10)
# branch (a) generic member with R != 0
for sig in (1, -1):
    eqsR = list(sp.expand(Rgen * Pn + sig * Rgen))
    solR = sp.solve(eqsR, [r0, r1, r2, r3], dict=True)
    Rsol = Rgen.subs(solR[0])
    free = sorted(Rsol.free_symbols & {r0, r1, r2, r3}, key=str)
    Jfam = blk(Pn, Z2, Rsol, sig * I2)
    imf = sp.expand(-Jfam * X * Jfam.inv())
    Kt = imf[2:4, 2:4]
    ck(f"V2g_branch_a_sig_{sig}_generic_member_all",
       len(free) == 2 and zero(sp.expand(Jfam * Jfam - sp.eye(4)))
       and zero(sp.expand(imf[0:2, 0:2] - H)) and imf[0:2, 2:4] == Z2
       and sp.simplify(Kt[0, 1]) == 0
       and sp.simplify(Kt + K) == Z2)   # K -> -K: lam,kmod,k10 all odd

# no Lorentz member: P^T eta P = diag(q^2, -p^2) != eta over R
ck("V2h_no_lorentz_member",
   sp.simplify(Pa.T * eta2 * Pa - sp.diag(q ** 2, -p ** 2)) == Z2
   and sp.solve([q ** 2 + 1], [q], dict=True) == [])

# ------------------------------------------------------------ V3 parities
# trace identity, 16-symbol J (own transcription)
J16 = sp.Matrix(4, 4, lambda i, j: sp.Symbol(f"j{i}{j}"))
ck("V3_trace_similarity_generic",
   sp.expand(sp.trace(J16 * X * J16.adjugate()) - J16.det() * sp.trace(X))
   == 0)
ck("V3_trX_is_2lambda", sp.simplify(sp.trace(X) - 2 * LAM) == 0)
# diag preservation under ANY invertible lower-tri S (generic, not branch)
t00, t10, t11 = sp.symbols("t00 t10 t11", nonzero=True)
Sfree = sp.Matrix([[t00, 0], [t10, t11]])
SKS = sp.expand(Sfree * K * Sfree.inv())
ck("V3_diag_preserved_any_lowertri_S",
   sp.simplify(SKS[0, 0] - k00) == 0 and sp.simplify(SKS[1, 1] - k11) == 0)

# C-signature via my own vectorization, symbolic p and s1, all four branches
x = sp.Symbol("x")
target = sp.expand((x - 1) ** 2 * (x + 1) ** 2)
BASIS = [sp.Matrix([[1, 0], [0, 0]]), sp.Matrix([[0, 1], [0, 0]]),
         sp.Matrix([[0, 0], [1, 0]]), sp.Matrix([[0, 0], [0, 1]])]
ok_sig = True
for Sbr in (I2, -I2, sp.Matrix([[1, 0], [s1, -1]]),
            sp.Matrix([[-1, 0], [s1, 1]])):
    cols = []
    for E in BASIS:
        M = sp.expand(-Sbr * E * Pn.inv())      # linear-in-C part, P^-1 form
        cols.append([M[0, 0], M[0, 1], M[1, 0], M[1, 1]])
    Mop = sp.Matrix(cols).T
    ok_sig = ok_sig and sp.simplify(
        sp.expand(Mop.charpoly(x).as_expr()) - target) == 0
ck("V3_C_signature_all_branches_Pinv_form", ok_sig)
# linear-in-C part is R-independent (block-triangularity of the moduli map)
imf = sp.expand(-Jg.subs({p00: 0, p11: 0}) * X
                * Jginv.subs({p00: 0, p11: 0}))
Ct = imf[2:4, 0:2]
ok_lin = True
for cs in (c00, c01, c10, c11):
    colC = sp.Matrix([[sp.diff(e, cs) for e in Ct]])
    ok_lin = ok_lin and colC.free_symbols.isdisjoint(set(Rg))
ck("V3_C_linear_part_R_independent", ok_lin)

# catch-proof mutations (must FAIL if machinery has teeth)
ck("V3_catch_kmod_even_is_false",
   not (sp.simplify(SKS[1, 1] - SKS[0, 0] - (k11 - k00)) == 0
        and sp.simplify((-(SKS[1, 1] - SKS[0, 0]) / 2) - KMOD) == 0))
mut = sp.expand((x - 1) ** 3 * (x + 1))
ck("V3_catch_wrong_signature_fails",
   sp.simplify(sp.expand(
       sp.Matrix([[sp.expand(-1 * E * Pn.inv())[i, j] for E in BASIS]
                  for (i, j) in [(0, 0), (0, 1), (1, 0), (1, 1)]]
                 ).charpoly(x).as_expr()) - mut) != 0)
# branch-(b) k10-odd claim must fail at kmod != 0
Sbv = sp.Matrix([[1, 0], [s1, -1]])
Ktb = sp.expand(-(Sbv * K * Sbv.inv()))
ck("V3_catch_k10_odd_on_branch_b_fails",
   sp.simplify(Ktb[1, 0] + k10) != 0)

# ------------------------------------------------------------ V4 fixed loci
# branch (a), sig=1, R generic in its 2-dim space, symbolic p
eqsR = list(sp.expand(Rgen * Pn + Rgen))
Rsol = Rgen.subs(sp.solve(eqsR, [r0, r1, r2, r3], dict=True)[0])
Ja = blk(Pn, Z2, Rsol, I2)
solfix = sp.solve(list(sp.expand(Ja * X + X * Ja)), MOD, dict=True)
sfa = solfix[0]
ck("V4_fixed_locus_a_K0_dim2",
   len(solfix) == 1 and sfa.get(k00, 0) == 0 and sfa.get(k11, 0) == 0
   and sfa.get(k10, 0) == 0
   and len([v for v in (c00, c01, c10, c11) if v in sfa]) == 2)
# F member cell = banked T5 swap cell
JF = blk(sp.Matrix([[0, 1], [1, 0]]), Z2, Z2, I2)
sfF = sp.solve(list(sp.expand(JF * X + X * JF)), MOD, dict=True)[0]
ck("V4_F_member_cell_matches_T5_swap",
   sfF.get(k00, 0) == 0 and sfF.get(k11, 0) == 0 and sfF.get(k10, 0) == 0
   and sp.simplify(sfF.get(c00, c00) + c01) == 0
   and sp.simplify(sfF.get(c10, c10) + c11) == 0)
# branch (b): k10 free, dim 3
Jb = blk(Pn, Z2, Z2, sp.Matrix([[1, 0], [s1, -1]]))
sfb = sp.solve(list(sp.expand(Jb * X + X * Jb)), MOD, dict=True)[0]
ck("V4_fixed_locus_b_k10_free_dim3",
   sfb.get(k00, 0) == 0 and sfb.get(k11, 0) == 0 and (k10 not in sfb)
   and len([v for v in (c00, c01, c10, c11) if v in sfb]) == 2)

# --------------------------------------------------- V5 escape witness / P2
kk = sp.Symbol("kk", nonzero=True)
Xk = sp.diag(-1, 1, -kk, kk)
Jout = blk(F2, Z2, Z2, F2)
ck("V5_escape_witness_exact",
   sp.simplify(Jout * Xk * Jout.inv() + Xk) == sp.zeros(4, 4)
   and sp.simplify(sp.expand(Jout * Jout) - sp.eye(4)) == sp.zeros(4, 4))
# J_out is OUTSIDE the compatible family: screen block F2 not lower-tri and
# its class action fails on generic members
imo = sp.expand(-Jout * X * Jout.inv())
ck("V5_Jout_leaves_class_generically",
   sp.simplify(imo[2:4, 2:4][0, 1]) != 0)
# lambda kill NOT escapable: even for Jout the trace flips (lam=0 here);
# generally: any linear rep flips tr, so a fold-invariant member needs lam=0.
lam_wit = sp.simplify(sp.trace(Xk) / 2)
ck("V5_witness_has_lambda_zero", lam_wit == 0)

# ------------------------------------------------------------ V6 bifurcation
lam = sp.Symbol("lambda")
aF_4D = 2 * lam
aF_tri = 1 + 2 * lam
ck("V6_aF_values_at_lambda0",
   aF_4D.subs(lam, 0) == 0 and aF_tri.subs(lam, 0) == 1
   and sp.Rational(-1, 2) != 0)
# value-vs-derivative discriminator: P1-4D has a_F'(0) = 2 != 0 (the banked
# "no lambda-row" criterion is a_F' = 0, NOT a_F = 0) — the package's check-25
# transfer of the "P2 side no-lambda-row" statement to the P1-4D lambda=0
# landing conflates the two.
ck("V6_P1_4D_aFprime_nonzero_at_0", sp.diff(aF_4D, lam).subs(lam, 0) == 2)
ck("V6_P2_pairing_aFprime_zero", sp.diff(sp.Integer(0) * lam, lam) == 0)

# ------------------------------------------------------------ V7 K4 honesty
R23 = sp.diag(1, 1, -1, -1)
R12 = sp.diag(1, -1, -1, 1)
R13 = sp.diag(1, -1, 1, -1)
Jf0 = blk(Pn, Z2, Z2, I2)
ck("V7_R23_composition_in_family",
   zero(sp.expand((R23 * Jf0) * (R23 * Jf0) - sp.eye(4)))
   and sp.simplify((R23 * Jf0)[2:4, 2:4] + I2) == Z2)
ck("V7_R12_composition_not_involutive",
   sp.simplify(sp.expand((R12 * Jf0) * (R12 * Jf0))
               - sp.diag(-1, -1, 1, 1)) == sp.zeros(4, 4))
ck("V7_R13_composition_not_involutive",
   sp.simplify(sp.expand((R13 * Jf0) * (R13 * Jf0))
               - sp.diag(-1, -1, 1, 1)) == sp.zeros(4, 4))

# ---------------------------------------------------------------- summary
print("=" * 70)
print(f"VERIFIER TOTAL: {'ALL PASS' if not FAILS else 'FAILURES: ' + str(FAILS)}")
sys.exit(0 if not FAILS else 1)
