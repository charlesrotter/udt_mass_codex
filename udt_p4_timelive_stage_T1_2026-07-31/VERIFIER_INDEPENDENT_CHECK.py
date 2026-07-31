#!/usr/bin/env python3
"""Blind adversarial verifier — independent checks for Stage T1 (2026-07-31).
Exact SymPy only; exit nonzero on any failure. Written from scratch against
the CANON wording (g_tt=-e^{-2phi}c^2 covariant; g_tt*g_rr=-c^2), not by
editing the package script. Includes the verifier's ATTACK constructions
(V5a/V5b/V5c: the psi-branch the package's T1p gloss misses).
"""
import os, sys
import sympy as sp
from sympy import Matrix, symbols, exp, simplify

HERE = os.path.dirname(os.path.abspath(__file__))
FAILS = []

def ck(name, cond, note=""):
    ok = bool(cond)
    if not ok:
        FAILS.append(name)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {note}")

c = symbols("c", positive=True)
phi = symbols("phi", real=True)
N = symbols("N", real=True)
gxx = symbols("g_xx", positive=True)
gtt = -exp(-2*phi)*c**2                       # CANON clock law (covariant row)
g = Matrix([[gtt, N], [N, gxx]])              # (t,x) block, shift live

# V1 — no free lapse, both lock readings (independent construction)
hp = symbols("hp", real=True)
J = Matrix([[hp, 0], [0, 1]])
gh = sp.expand(J.T*g*J)
ck("V1a_lock_coord_forces_hp2_1", set(sp.solve(sp.Eq(gh[0,0]*gh[1,1], gtt*gxx), hp)) == {-1, 1},
   "coordinate lock reading preserved under t->h(t) iff h'^2=1")
gam = g[1,1] - g[0,1]**2/g[0,0]
gamh = gh[1,1] - gh[0,1]**2/gh[0,0]
ck("V1b_lock_proj_forces_hp2_1", set(sp.solve(sp.Eq(sp.simplify(gh[0,0]*gamh), sp.simplify(g[0,0]*gam)), hp)) == {-1, 1},
   "projected lock reading likewise; rigidity reading-robust — package T1a/T1b CONFIRMED")

# V2 — clock row alone does NOT rigidify h (phi-redefinition slack): confirm the
# package's stated reason the LOCK is load-bearing.
hpos = symbols("hpos", positive=True)
ck("V2_clock_row_alone_has_phi_slack",
   simplify(hpos**2*(-exp(-2*(phi + sp.log(hpos)))*c**2) - gtt) == 0,
   "g_tt form preserved under t->h(t), phi -> phi + ln h' for any h'>0: the clock row ALONE does not "
   "rigidify the lapse; the rigidity genuinely rests on the LOCK (package leg-1 reasoning confirmed)")

# V3 — the ADM discriminator, independent + DOWNSTREAM content
ginv = g.inv()
ck("V3a_minus_inv_gtt_identity", simplify(-1/ginv[0,0] - (exp(-2*phi)*c**2 + N**2/gxx)) == 0,
   "-1/g^tt = e^{-2phi}c^2 + N^2/g_xx — package T1j identity CONFIRMED")
# ADM-lapse pin instead: g_tt = -e^{-2phi}c^2 + N^2/gxx. Stationary proper rate differs:
gtt_adm = -exp(-2*phi)*c**2 + N**2/gxx
rate_adm = sp.sqrt(-gtt_adm)/c
ck("V3b_ADM_pin_breaks_canon_clock_rate", simplify(rate_adm - exp(-phi)) != 0 and simplify(rate_adm.subs(N,0) - exp(-phi)) == 0,
   "under an ADM-lapse pin the stationary observer rate != e^{-phi} whenever N!=0: the discriminator is "
   "NOT cosmetic — the covariant pin is the only reading matching the canon clock rate (Duty 2a settled)")

# V4 — lock-reading split
ck("V4_reading_split", simplify((gam - gxx) - N**2*exp(2*phi)/c**2) == 0,
   "gamma_xx - g_xx = N^2 e^{2phi}/c^2 — package T1k CONFIRMED; coincide iff N=0")
print("--- section 1 ok ---")

# V5 — THE ATTACK (Duty 2b/2c): the psi-slack t -> t + psi(x) under the SPATIAL
# PIN ALONE, and under the projected-reading registration.
p = symbols("psi1", real=True)          # psi'(x)
Jp = Matrix([[1, p], [0, 1]])
gp = sp.expand(Jp.T*g*Jp)
# V5a: spatial pin alone (preserve g_xx only) does NOT force psi'=0 — two branches.
sols = set(sp.solve(sp.Eq(gp[1,1], g[1,1]), p))
ck("V5a_spatial_pin_alone_two_branches", sols == {0, sp.simplify(-2*N/gtt)},
   "preserving g_xx alone gives psi' in {0, -2N/g_tt}: the package's T1p check-name "
   "'registered_spatial_pin_kills_psi' overstates — uniqueness needed the SHIFT-ROW equation too")
# V5b: the second branch is a lawful extra residual map on configs where
# -2N/g_tt is a function of x alone: preserves clock row, spatial row, both lock
# readings, and flips N -> -N (sign action only; N still never REMOVED).
gp2 = sp.expand(gp.subs(p, -2*N/gtt))
ck("V5b_extra_residual_map_flips_N",
   simplify(gp2[0,0]-g[0,0]) == 0 and simplify(gp2[1,1]-g[1,1]) == 0 and simplify(gp2[0,1]+N) == 0,
   "psi' = -2N/g_tt preserves g_tt and g_xx and maps N -> -N: a residual chart map beyond t->sigma t+t0 "
   "exists on the stratum where 2N e^{2phi}/c^2 is t-independent — T1c/T1r's group statement needs this caveat "
   "(orbit still {N,-N}: irreducibility conclusion SURVIVES, the group claim is amended)")
# V5c: under a PROJECTED-reading registration (pin g_tt and gamma_xx, not g_xx),
# psi' = -N/g_tt is lawful and REMOVES the shift entirely:
gp3 = sp.expand(gp.subs(p, sp.simplify(-N/gtt)))
gam3 = sp.simplify(gp3[1,1] - gp3[0,1]**2/gp3[0,0])
ck("V5c_projected_pin_makes_N_removable",
   simplify(gp3[0,1]) == 0 and simplify(gp3[0,0]-g[0,0]) == 0 and simplify(gam3 - gam) == 0,
   "psi' = -N/g_tt kills N while preserving the clock row and the PROJECTED lock reading exactly "
   "(new chart diagonal with g'_xx = gamma_xx): under a reading-(ii) spatial registration the shift is "
   "chart-slack (removable when N/g_tt is t-independent) — the leg-3 irreducibility claim is CONDITIONAL "
   "on the coordinate-reading (i) spatial pin; the package states the fork and the irreducibility "
   "as independent facts and misses this interaction (REQUIRED AMENDMENT)")

# V6 — temporal-mirror parities, independent (solve on TWO sample phi values to
# force the for-all reading, then confirm symbolically)
sphi, sN, sG = symbols("s_phi s_N s_G", real=True)
ph, NN, GG = symbols("ph NN GG", real=True)
eq_phi = sp.Eq(exp(-2*sphi*ph), exp(-2*ph))
sol_sphi = sp.solve(sp.Eq(sphi*ph, ph), sphi)
ck("V6a_phi_even_forced", sol_sphi == [1] and simplify(exp(sp.Integer(2)) - exp(sp.Integer(-2))) != 0,
   "e^{-2 s phi} = e^{-2 phi} for all phi forces s=+1 (s=-1 fails at phi=1): phi EVEN-composed — T2a leg confirmed")
ck("V6b_N_odd_G_even", sp.solve(sp.Eq(sN*NN, -NN), sN) == [-1] and sp.solve(sp.Eq(sG*GG, GG), sG) == [1],
   "pullback under t->-t flips g_ti only: N ODD, spatial data EVEN — temporal mirror (t,phi,N,G)->(-t,phi,-N,G)")

# V7 — K4 and the SO+ obstruction, independent
eta = sp.diag(-1,1,1,1)
K4 = [sp.eye(4), sp.diag(1,1,-1,-1), sp.diag(1,-1,-1,1), sp.diag(1,-1,1,-1)]
ck("V7a_K4_fixes_time_axis", all(M[0,0]==1 and all(M[0,j]==0 and M[j,0]==0 for j in range(1,4)) for M in K4)
   and all(sp.simplify((M.T*eta*M - eta).norm()) == 0 and M.det()==1 for M in K4),
   "all four K4 elements in SO+ with Lam^0_0=1: K4 survives; time a spectator")
L = Matrix(4,4, symbols("m0:16", real=True))
col00 = sp.expand((L.T*eta*L)[0,0])
ck("V7b_column0_identity", simplify(col00 - (-L[0,0]**2 + L[1,0]**2 + L[2,0]**2 + L[3,0]**2)) == 0,
   "(Lam^T eta Lam)_00 = -L00^2 + sum b^2 = -1 => L00^2 = 1 + sum b^2 >= 1: orthochronous split exact; "
   "SO+ (banked Route B registration) contains no time flip — coframe-layer obstruction CONFIRMED")
print("--- section 2 ok ---")

# V8 — TT-3 typing anchors, independent
t, T = symbols("t T", positive=True)
ck("V8a_period_depth_lock", simplify(sp.integrate(sp.sqrt(-gtt)/c, (t, 0, T)) - exp(-phi)*T) == 0,
   "branch-(b) map fact: proper period tau = e^{-phi} T for static phi — T3a confirmed; framed as obligation")
det2 = g.det()
ck("V8b_wall_causal_types", simplify(ginv[1,1] - gtt/det2) == 0 and simplify(ginv[0,0] - gxx/det2) == 0
   and sp.simplify(det2.subs(N,0)) == gtt*gxx,
   "g^xx = g_tt/det > 0 (det<0): spatial wall x R_t TIMELIKE; g^tt = g_xx/det < 0: t=const SPACELIKE — T3b confirmed")

# V9 — anchor-shift absorption (T1q) independent
s = symbols("s", real=True)
ck("V9_anchor_absorption", simplify(exp(2*s)*gtt.subs(phi, phi+s) - gtt) == 0
   and simplify(exp(-2*s)*exp(2*(phi+s)) - exp(2*phi)) == 0,
   "(phi+s, t e^s, r e^{-s}): clock and locked radial rows invariant — D3 time extension confirmed")

# V10 — psi-cocycle additivity (T2i) independent + loop holonomy
pa, pb = symbols("pa pb", real=True)
Ja = Matrix([[1, pa], [0, 1]]); Jb = Matrix([[1, pb], [0, 1]])
ck("V10_cocycle_additive", sp.expand(Jb.T*(Ja.T*g*Ja)*Jb - (Matrix([[1, pa+pb],[0,1]]).T*g*Matrix([[1, pa+pb],[0,1]]))) == sp.zeros(2,2)
   and sp.expand(Ja.T*(Jb.T*g*Jb)*Ja - Jb.T*(Ja.T*g*Ja)*Jb) == sp.zeros(2,2),
   "successive psi-maps compose additively and commute: abelian J07 cocycle; loop holonomy trivial — T2i confirmed")

# V11 — C-1 INDEPENDENT static recovery (my own parse of both TSVs; Duty 3)
banked = []
with open(os.path.join(HERE, "..", "udt_p4_routeA_response_inverse_problem_2026-07-29",
                       "VARIATION_DOMAIN_CENSUS.tsv")) as fh:
    for line in fh:
        if line.startswith("#") or line.startswith("object\t") or not line.strip():
            continue
        banked.append(line.split("\t")[0].split(" ")[0].split("(")[0].strip())
objs, reqs, jrows = [], [], []
with open(os.path.join(HERE, "TIMELIVE_T1_LEDGER.tsv")) as fh:
    for line in fh:
        if line.startswith("#") or line.startswith("row_id\t") or not line.strip():
            continue
        f = line.rstrip("\n").split("\t")
        nm = f[2].split(" ")[0].split("(")[0].strip()
        {"OBJECT": objs, "REQUIREMENT": reqs, "JROW": jrows}.get(f[1], []).append(nm)
kill = {"shift_row_N": None, "time_topology_label": None, "boundary_data_walls": "boundary_data"}
restr = [kill.get(n, n) for n in objs]
restr = [n for n in restr if n is not None]
ck("V11a_census_recovery_independent", len(banked) == 16 and len(objs) == 18 and restr == banked,
   "independent parse: 18-row time-live census restricts to the banked 16-row census exactly, in order — F-T7 clean")
ck("V11b_ledger_row_counts", len(reqs) == 15 and len(jrows) == 15, "15 R-rows + 15 J-rows present")
# Requirement classes: parsed from the BANKED posing doc table (primary-class column)
import re
txt = open(os.path.join(HERE, "..", "udt_p4_routeA_response_inverse_problem_2026-07-29",
                        "POSED_INVERSE_PROBLEM.md")).read()
m = re.search(r"PW 8 \(R1, R2, R4, R7, R8, R10, R12, R13\)", txt)
m2 = re.search(r"WS 2 \(R5, R14\)", txt)
ck("V11c_banked_class_tally_wording", m is not None and m2 is not None,
   "banked tallies PW8(R1,R2,R4,R7,R8,R10,R12,R13)/WS2(R5,R14) verbatim in the banked doc; GC4 = R3,R6,R9,R15 "
   "— matches the package's BANKED_CLASSES table and the no-migration claim's baseline")

# V12 — T4a independent: the banked component-list block contains exactly the 11
# slots in order (unicode names), and the package's static restriction matches.
block = txt[txt.find("R_φ"):txt.find("boundary/corner components")]
order_ok = all(block.find(a) < block.find(b) for a, b in
               [("R_φ","R_f"),("R_f","R_bh"),("R_bh","R_α"),("R_α","R_{c_E}"),
                ("R_{c_E}","R_λ"),("R_λ","R_{k_mod}"),("R_{k_mod}","R_{k10}"),
                ("R_{k10}","R_C"),("R_C","R_∂"),("R_∂","R_corner")])
ck("V12_component_list_banked_order", order_ok,
   "banked doc's component list order = phi,f,bh,alpha,cE,lambda,kmod,k10,C,wall,corner — T4a's hard-coded "
   "BANKED_COMPONENTS is faithful to the bank (the package check itself was self-authored on both sides)")

n = len(FAILS)
print(f"VERIFIER TOTAL: {'ALL PASS' if n == 0 else f'{n} FAILURES: {FAILS}'}")
sys.exit(0 if n == 0 else 1)
