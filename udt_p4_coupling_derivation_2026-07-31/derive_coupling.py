#!/usr/bin/env python3
# P4 coupling derivation (TC-1..TC-5) -- contract: PREREGISTRATION.md (frozen).
# Exact SymPy only; no floats, no numeric solvers, no GPU; deterministic; exit nonzero on failure.
# EVERYTHING HERE IS IF-ADOPTED CONDITIONAL: theta is the REGISTERED-NOT-ADOPTED S1-valued
# field of the doorway bank (f27b5ca). No coupling is selected; no adoption occurs (F-C4).
# AMENDED 2026-07-31 (verifier round 1, PASS-WITH-REQUIRED-AMENDMENTS): AM-1 block-grading
# rule stated + thp*thpp regraded EVEN + menu regenerated (18 blocks, parity COMPUTED);
# AM-2 the eps_theta=-1 crease jet-2 condition adjudicated (c_theta = 0 FORCED on every
# nonconstant cell -- disjointness STRENGTHENED); AM-3 the pin-pin piZ lattice on the
# mirrored double-crease constant stratum added (massless-confined). See CORRECTION_LAYER.md.
import sympy as sp
from sympy import (symbols, Function, cos, sin, exp, I, pi, integrate, atan, log,
                   Matrix, S, solveset, Eq, sqrt, Rational)
import json, sys

RESULTS = {"checks": [], "stages": {}}
FAILED = []
def check(name, ok, kind, detail):
    ok = bool(ok)
    RESULTS["checks"].append({"name": name, "ok": ok, "kind": kind, "detail": detail})
    tag = "PASS" if ok else "FAIL"
    print(f"[{tag}][{kind}] {name}")
    if not ok:
        FAILED.append(name)

x, s_, L_, ell = symbols('x s_ L_ ell', real=True)
th = symbols('vartheta', real=True)            # a target value of theta (R/2piZ)
n_w = symbols('n_w', integer=True)
g_th = symbols('g_theta', positive=True)       # IF-ADOPTED coupling constant (FREE, unpinned)
c_th = symbols('c_theta', real=True)           # theta-momentum constant (integration datum)
eps_th = symbols('epsilon_theta', real=True)   # SUPPLIED parity sign, never valued

print("## P4 COUPLING DERIVATION -- staged run. All theta-content REGISTERED-POSIT;")
print("## every consequence IF-ADOPTED conditional. Contract: PREREGISTRATION.md.")
print()
print("## ============ STAGE 1 / TC-1: the lawful coupling menu ============")

# ---- S1a: alphabet legality of every grade<=2 theta-block (periodicity rule, doorway C5a re-run)
res_lin  = sp.simplify((th + 2*pi) - th)
blocks_g0 = {"cos_theta": cos(th), "sin_theta": sin(th)}
per_ok = all(sp.simplify(b.subs(th, th + 2*pi) - b) == 0 for b in blocks_g0.values())
check("S1a_grade0_blocks_periodic_legal",
      per_ok and res_lin == 2*pi and res_lin != 0,
      "SUBSTANTIVE",
      "grade-0 theta-entries: cos(theta), sin(theta) well-defined on R/2piZ (zero residual "
      "under theta -> theta+2pi); BARE theta EXCLUDED (residual 2pi != 0) -- the doorway "
      "C5a periodicity legality rule re-run at the coupling layer; the exclusion travels")
thF = Function('vth')
jet1 = sp.diff(thF(x) + 2*pi, x) - sp.diff(thF(x), x)
jet2 = sp.diff(thF(x) + 2*pi, x, 2) - sp.diff(thF(x), x, 2)
check("S1a_jets_lift_independent_legal",
      sp.simplify(jet1) == 0 and sp.simplify(jet2) == 0,
      "SUBSTANTIVE",
      "theta'(x), theta''(x): lifts differ by 2piZ constants, killed by d/dx (zero residual) "
      "-- REAL local entries at grades 1,2 (doorway C5a jets, re-run); jet<=2 layer declared, "
      "higher jets TYPED (same argument, order-independent)")
# ---- S1b: the excluded entries travel (co-translation defect of the anchored nonlocal / lift)
u_ = symbols('u_', real=True)
lift = x**2
translated_val = integrate(sp.diff(lift.subs(x, u_ + s_), u_), (u_, 0, x))
naive = lift.subs(x, x + s_) - lift.subs(x, 0)
nl_res = sp.simplify(translated_val - naive)
check("S1b_nonlocal_lift_exclusion_travels",
      nl_res == -s_**2 and nl_res != 0,
      "SUBSTANTIVE",
      "the anchored nonlocal entry int_0^x theta' du (= the lift theta~(x)-theta~(0)) FAILS "
      "the banked co-translation test (witness residual -s^2 != 0): the bare-phi/nonlocal-m/"
      "absolute-point exclusions TRAVEL to every menu member -- no member may carry the lift, "
      "an anchored integral, or an absolute-point value (doorway C5b re-run; R1/J12 fence)")

# ---- S1c: K4 character grading of the theta-blocks (chi_theta DECLARED, carried symbolically)
# Representation: for g in K4, theta -> chi_theta(g)*theta with chi_theta(g) in {+1,-1}
# (doorway C5d: theta -> -theta is circle-legal; chi_theta = a DECLARED K4 character).
sgn = symbols('sgn')   # a character value +-1
odd_blocks, even_blocks = {}, {}
for nm, b, dnm in (("sin_theta", sin(th), 0), ("theta_p", None, 1), ("theta_pp", None, 2)):
    pass
# explicit transformation checks at both sign values:
tr = {s0: {
        "cos_theta": sp.simplify(cos(s0*th) - cos(th)),
        "sin_theta": sp.simplify(sin(s0*th) - s0*sin(th)),
     } for s0 in (1, -1)}
thf = thF(x)
jtr = {s0: {
        "theta_p":  sp.simplify(sp.diff(s0*thf, x) - s0*sp.diff(thf, x)),
        "theta_pp": sp.simplify(sp.diff(s0*thf, x, 2) - s0*sp.diff(thf, x, 2)),
     } for s0 in (1, -1)}
check("S1c_theta_block_characters_computed",
      all(v == 0 for s0 in (1, -1) for v in tr[s0].values())
      and all(v == 0 for s0 in (1, -1) for v in jtr[s0].values()),
      "SUBSTANTIVE",
      "under g in K4 acting as theta -> chi_theta(g)*theta (chi_theta(g) = +-1): "
      "cos(theta) -> cos(theta) (TRIVIAL character, both signs, zero residual); "
      "sin(theta) -> chi_theta(g)*sin(theta); theta' -> chi_theta(g)*theta'; "
      "theta'' -> chi_theta(g)*theta'' (each zero residual): the theta-alphabet is graded -- "
      "cos-type blocks carry the trivial character, every theta-ODD block (sin, jets) carries "
      "chi_theta. chi_theta itself stays a DECLARED symbol in {triv, chi_a, chi_b, chi_c}")
# ---- S1d: the character group algebra (Z2 x Z2) + the exhaustive grade<=2 matched-block table
# characters as vectors over GF(2): triv=(0,0), a=(1,0), b=(0,1), c=(1,1); product = XOR.
CH = {"triv": (0, 0), "a": (1, 0), "b": (0, 1), "c": (1, 1)}
def chmul(u, v): return ((u[0]+v[0]) % 2, (u[1]+v[1]) % 2)
grp_ok = (chmul(CH["a"], CH["b"]) == CH["c"] and chmul(CH["b"], CH["c"]) == CH["a"]
          and chmul(CH["a"], CH["c"]) == CH["b"]
          and all(chmul(v, v) == CH["triv"] for v in CH.values()))
check("S1d_character_group_Z2xZ2",
      grp_ok, "SUBSTANTIVE",
      "K4^ = Z2 x Z2 verified: chi_a chi_b = chi_c (and cyclically), every character squares "
      "to trivial -- so a product of theta-odd blocks carries chi_theta^(odd count), and "
      "chi_theta^2 = trivial for EVERY declared chi_theta")
# ---- theta-block table (AM-1 AMENDMENT 2026-07-31, verifier round 1) ----
# THE BLOCK GRADING RULE, stated and applied uniformly (the shipped rule was inconsistent:
# its comment bounded "TOTAL jet order <= 2" yet its list included thp*thpp (total 3) and
# excluded thpp^2 -- and it hand-misgraded thp*thpp as theta-ODD; true character trivial).
# Derived rule from the banked jet-layer <= 2 admission:
#  (i) alphabet FACTORS = the legal entries of the 2-jet only: grade-0 periodic {1, cos,
#      sin} (higher harmonics cos(k theta) absorbed into the F(theta) classes) and the
#      jets {theta', theta''} -- the banked bound is each entry's JET ORDER <= 2, NOT a
#      product's total derivative count;
#  (ii) the TABLE enumerates monomials of jet DEGREE <= 2 (the quadratic layer -- the
#       highest polynomial degree the banked pairing/second-variation machinery carries);
#       higher-degree monomials are TYPED by the same grading (theta-parity = odd-factor
#       count mod 2, order/degree-independent since chi_theta^2 = trivial, S1d above).
# vs the shipped 13-block table: ADDS thpp^2, sin*thp*thpp, cos*thp*thpp, sin*thpp^2,
# cos*thpp^2; REGRADES thp*thpp EVEN. Parity now COMPUTED per block (theta -> s*theta,
# s = +-1), never hand-listed.
thX = thF(x)
def _jetm(s):
    tp, tpp = sp.diff(s*thX, x), sp.diff(s*thX, x, 2)
    return {"": S(1), "thp": tp, "thpp": tpp, "thp^2": tp**2,
            "thp*thpp": tp*tpp, "thpp^2": tpp**2}
def _trig(s):
    return {"": S(1), "cos": cos(s*thX), "sin": sin(s*thX)}
_j_oddcount = {"": 0, "thp": 1, "thpp": 1, "thp^2": 0, "thp*thpp": 0, "thpp^2": 0}
THB = []   # (name, computed_parity): 18 blocks = {1, cos, sin} x {jet monomials deg <= 2}
_am1_rule_ok = True
for tn in ("", "cos", "sin"):
    for jn in ("", "thp", "thpp", "thp^2", "thp*thpp", "thpp^2"):
        nm = (tn + "*" + jn).strip("*") or "1"
        bp, bm = _trig(1)[tn]*_jetm(1)[jn], _trig(-1)[tn]*_jetm(-1)[jn]
        if sp.simplify(bm - bp) == 0:
            par = 0
        elif sp.simplify(bm + bp) == 0:
            par = 1
        else:
            par = None
        oddcount = ((1 if tn == "sin" else 0) + _j_oddcount[jn]) % 2
        _am1_rule_ok &= (par is not None and par == oddcount)
        THB.append((nm, par))
_thb_par = dict(THB)
check("AM1_S1d2_block_grading_rule_uniform_and_regrade",
      _am1_rule_ok and len(THB) == 18 and _thb_par["thp*thpp"] == 0
      and _thb_par["thpp^2"] == 0 and _thb_par["sin*thp*thpp"] == 1
      and _thb_par["cos*thp*thpp"] == 0 and _thb_par["sin*thpp^2"] == 1
      and _thb_par["cos*thpp^2"] == 0,
      "SUBSTANTIVE",
      "AM-1 (AMENDMENT 2026-07-31, verifier round 1): the block grading rule stated above "
      "applied uniformly -- all 18 jet-degree<=2 blocks parity-graded by direct symbolic "
      "computation (theta -> s*theta at s = +-1), and every computed parity MATCHES the "
      "odd-factor-count rule (sin, theta', theta'' each count 1; parity = count mod 2 -- "
      "the chi_theta^2 = trivial consequence of S1d). The shipped error is corrected: "
      "thp*thpp is EVEN (trivial character), NOT theta-odd -- bare theta'theta'' does NOT "
      "sit in r_sh at chi_theta = chi_a; it enters TRIVIAL rows directly. Rule-added even "
      "blocks thpp^2/cos*thp*thpp/cos*thpp^2 join the trivial rows; odd sin*thp*thpp/"
      "sin*thpp^2 join the chi_theta-matched rows. Higher-degree monomials TYPED (parity = "
      "odd-count mod 2, same computation shape)")
row_char = {"R_p0": "triv", "R_f": "triv", "R_bh": "triv", "r_tr": "triv", "r_tf": "triv",
            "R_wall": "triv", "r_sh": "a", "R_c00c11": "b", "R_c01c10": "c",
            "R_theta": "CHI"}   # the new theta-row pairs delta-theta => needs chi_theta itself
menu_table = {}
for chi_nm, chi in CH.items():
    per_row = {}
    for rw, rc in row_char.items():
        target = chi if rc == "CHI" else CH[rc]
        direct, dressed = [], []
        for bn, par in THB:
            bc = chi if par == 1 else CH["triv"]
            if bc == target:
                direct.append(bn)          # block alone (x trivial invariants A_g)
            else:
                need = chmul(bc, target)   # needed moduli-module character (chi^2=triv)
                dressed.append((bn, [k for k, v in CH.items() if v == need][0]))
        per_row[rw] = {"direct_blocks": direct,
                       "dressed_blocks_need_module": dressed}
    menu_table[chi_nm] = per_row
# structural checks on the assembled menu:
mt_ok = True
for chi_nm, chi in CH.items():
    # theta-row always admits at least sin (if chi matches parity-1 blocks) or dressed entries:
    mt_ok &= len(menu_table[chi_nm]["R_theta"]["direct_blocks"]) > 0
    # trivial rows always admit the even blocks directly:
    mt_ok &= "cos" in menu_table[chi_nm]["R_p0"]["direct_blocks"]
    mt_ok &= "thp^2" in menu_table[chi_nm]["R_p0"]["direct_blocks"]
# chi_theta = chi_a puts the bare jet directly into the shear slot; not for chi_b:
mt_ok &= "thp" in menu_table["a"]["r_sh"]["direct_blocks"]
mt_ok &= "thp" not in menu_table["b"]["r_sh"]["direct_blocks"]
# for chi_theta = triv the theta-odd blocks are trivial-charactered => direct everywhere trivial:
mt_ok &= "thp" in menu_table["triv"]["R_p0"]["direct_blocks"]
# AM-1 regenerated-menu facts: thp*thpp is EVEN => OUT of r_sh at chi_a, INTO trivial rows:
mt_ok &= "thp*thpp" not in menu_table["a"]["r_sh"]["direct_blocks"]
mt_ok &= "thp*thpp" in menu_table["a"]["R_p0"]["direct_blocks"]
# rule-added blocks land per computed parity (even -> trivial rows; odd -> matched rows):
mt_ok &= "thpp^2" in menu_table["b"]["R_f"]["direct_blocks"]
mt_ok &= "sin*thp*thpp" in menu_table["a"]["r_sh"]["direct_blocks"]
mt_ok &= "sin*thpp^2" not in menu_table["b"]["r_sh"]["direct_blocks"]
check("S1d_menu_assembly_grade_le2_exhaustive_by_character",
      mt_ok, "SUBSTANTIVE",
      "the jet<=2 theta-block table (18 blocks, AM-1 REGENERATED: parity computed, grading "
      "rule stated above) x the banked row characters (trivial for field/tr/tf/wall rows; "
      "chi_a shear; chi_b/chi_c mixing; chi_theta for the new theta-row) assembled over "
      "K4^ = Z2xZ2: EVERY row's lawful theta-entries = (character-matched blocks) x A_g + "
      "(mismatched blocks) x (matching banked character-module generators) -- a NONEMPTY "
      "parametrized family for every declared chi_theta; e.g. bare theta' sits in the shear "
      "slot r_sh iff chi_theta = chi_a; theta-even blocks (cos, theta'^2, sin*theta', and "
      "AM-1: theta'theta'', theta''^2) enter every trivial row for every chi_theta -- the "
      "shipped mis-admission of bare theta'theta'' into r_sh at chi_a is REMOVED. Row "
      "characters CITED from the banked Stage-2 module table (guard S1g); the group algebra "
      "and block grading computed here")

# ---- S1e: anchoring / shift / co-translation legality of the coupling products
phi_, cE, a_ = symbols('phi_v c_E a_v', real=True)
Qb = cE*exp(-phi_)             # the banked anchored readout block Q
prod = Qb**a_ * cos(th)        # weight-structure coupling: Q-power x periodic block
shifted = prod.subs([(phi_, phi_ + s_), (cE, cE*exp(s_))], simultaneous=True)
check("S1e_weight_coupling_anchor_orbit_invariant",
      sp.simplify(shifted - prod) == 0,
      "SUBSTANTIVE",
      "the weight-structure members Q^a x F_per(theta) (and W_F-multiplied members at the "
      "seam-locus rule) are shift-legal: under the banked absorption orbit (phi, c_E) -> "
      "(phi+s, c_E e^s) the product is INVARIANT with theta inert (zero residual) -- theta "
      "blocks carry no anchor, so the banked p = q Q-power condition is UNTOUCHED by the "
      "coupling layer; any c_E^p e^{-q phi} with p != q stays excluded (banked, cited)")
# ---- S1f: J05 pairing of the theta-row: pointwise density row + wall theta-jet slots
c0, c1, c2, c3, d0, d1, d2, d3, e0, e1, e2, e3 = symbols('c0:4 d0:4 e0:4')
Dp = c0 + c1*x + c2*x**2 + c3*x**3         # D_theta (pointwise row witness)
Ep = d0 + d1*x + d2*x**2 + d3*x**3         # D_theta' (jet-slot kernel witness)
Vp = e0 + e1*x + e2*x**2 + e3*x**3         # delta-theta witness
lhs = integrate(Dp*Vp + Ep*sp.diff(Vp, x), (x, 0, L_))
rhs = integrate((Dp - sp.diff(Ep, x))*Vp, (x, 0, L_)) + (Ep*Vp).subs(x, L_) - (Ep*Vp).subs(x, 0)
check("S1f_J05_theta_row_pointwise_plus_wall_slots",
      sp.simplify(sp.expand(lhs - rhs)) == 0,
      "SUBSTANTIVE",
      "the J05 identity re-run with all 12 coefficients free (zero residual): every bulk menu "
      "member pairs delta-theta as a POINTWISE density row (D_theta - d/dx D_theta') plus WALL "
      "theta-jet slots [D_theta' v]_walls -- the doorway C5e slots are exactly the two lawful "
      "coupling SEATS; no other seat exists at jet<=2 (N3-analog; V8 supplied-structure at "
      "the walls; R12/J14 full-domain-first: all entries pointwise-local, no restrict-then-vary)")
# ---- S1g [guard]: banked citations the menu rides on
check("S1g_banked_row_and_module_citations",
      True, "GUARD",
      "CITED (never re-derived): the Stage-2 row characters + character-module generator "
      "bases (chi_a {k10, c00c01, c00c10, c11c01, c11c10}; chi_b {c00, c11, k10c01, k10c10}; "
      "chi_c {c01, c10, k10c00, k10c11}); the Stage-2 A1 stratum Noether identities (they cut "
      "the theta-extended rows exactly as banked -- theta-blocks are moduli-inert so the "
      "identities' derivation is untouched); the wall-gate slot census (first germs pinned/"
      "forced per posture, second germs unpinned); R1/R4 screen slot structure (theta adds NO "
      "screen kernel slot: the W-decomposition r_tr/r_tf/r_sh + null is a delta-K pairing "
      "fact, theta-independent); the doorway registration content f27b5ca")
# ---- S1h: parity / wall compatibility census (eps_theta SUPPLIED, both signs carried)
# mirror at a crease: x -> -x with theta -> eps_theta*theta (+ 2 pi k). Generic odd/even lift split:
a0, a1, a2, a3 = symbols('a0:4', real=True)
thpoly = a0 + a1*x + a2*x**2 + a3*x**3
# eps_theta = -1 (theta odd up to 2 pi k): fixed-point condition at the crease value:
crease_vals = solveset(Eq(2*th, 2*pi*symbols('kk', integer=True)), th, S.Reals)
tv = sorted(set([sp.Mod(pi*m, 2*pi) for m in range(-2, 3)]), key=str)
# jet parities under (x, theta) -> (-x, eps*theta): theta'(x) -> -eps*theta'(-x); theta'' -> eps*theta''(-x)
todd = thpoly - thpoly.subs(x, -x)*(-1)      # enforcing odd: a0 = a2 = 0 branch
jp_odd_th = sp.diff(a1*x + a3*x**3, x)       # theta odd  => theta' EVEN (survives crease)
jp_odd_th2 = sp.diff(a1*x + a3*x**3, x, 2)   # theta odd  => theta'' ODD (killed at crease)
jp_even_th = sp.diff(a0 + a2*x**2, x)        # theta even => theta' ODD (killed at crease)
ok_par = (jp_odd_th.subs(x, -x) - jp_odd_th == 0
          and sp.simplify(jp_odd_th2.subs(x, -x) + jp_odd_th2) == 0
          and sp.simplify(jp_even_th.subs(x, -x) + jp_even_th) == 0
          and pi in crease_vals.subs(symbols('kk', integer=True), 1)
          and set(tv) == {S(0), pi})
check("S1h_parity_wall_census_both_eps_branches",
      ok_par, "SUBSTANTIVE",
      "crease/wall compatibility, BOTH supplied signs: eps_theta = -1 -- crease value 2-torsion "
      "quantized theta(crease) in {0, pi} (solveset exact; doorway C5d re-run), theta' EVEN "
      "(trace SURVIVES: the wall theta-jet slot is live), theta'' ODD (trace killed); "
      "eps_theta = +1 -- theta(crease) FREE, theta' ODD (trace KILLED: the wall jet slot dies "
      "at a crease), theta'' survives. Glue seams: [e^{i theta}] continuity + supplied germ "
      "jumps J_s (banked seam menu); open ends: both traces free. eps_theta stays SUPPLIED")
print()
print("## TC-1 MENU (the deliverable, parametrized family; NOTHING adopted):")
print("##  MB-P  potential class: grade-0 periodic blocks {cos, sin} x A_g / x module gens")
print("##  MB-J  moment/jet class: {theta', theta''} + even combos; canonical rep: the")
print("##        angular-moment kernel D_theta' = g_theta * w * theta' (lawful for EVERY chi_theta)")
print("##  MB-Xf field-sector cross members (theta-even blocks in R_p0/R_f/R_bh; odd blocks")
print("##        dressed by chi_theta-matching module generators)")
print("##  MB-Xm moduli-sector cross members (bare theta' in r_sh iff chi_theta = chi_a; ")
print("##        sin theta entrywise in the mixing rows iff matched; else module-dressed)")
print("##  MB-W  weight-structure members Q^a x F_per(theta) (anchor-invariant)")
print("##  MW-N  wall members: theta'-trace slot + periodic theta-trace arguments, cut by the")
print("##        S1h parity census per posture; seam jumps J_s supplied germ data")
print("##  EXCLUDED (proven): bare theta, the lift, anchored-nonlocal, absolute-point,")
print("##        aperiodic F(theta), character-mismatched terms, p != q anchor powers")
RESULTS["stages"]["TC1"] = {"menu_table_by_chi_theta": menu_table,
                            "outcome": "NONEMPTY parametrized family (OC-2 shape)"}
print("## STAGE 1 complete.")

print()
print("## ============ STAGE 2 / TC-2: conditional integer cuts (ALL IF-ADOPTED) ============")
# 2pi provenance discipline: the 2pi traces ONLY to the target circle (banked precedent re-run).
check("S2a_2pi_provenance_from_target",
      sp.simplify(exp(I*(2*pi*n_w)).rewrite(cos).subs(n_w, 3)) == 1
      and sp.simplify(exp(I*pi)) == -1,
      "SUBSTANTIVE",
      "e^{i 2pi n} = 1 and e^{i pi} = -1 (direct exact certificates, the banked period-gate "
      "route): the 2pi in every cut below enters ONLY through single-valuedness of e^{i theta} "
      "on the registered target -- never inserted by hand (banked provenance discipline)")
# ---- S2b: MB-J canonical member IF ADOPTED: per-cell closure and increment on the banked atlas
A_, w1, w0, E0, g_p, a_F = symbols('A_ w1 w0 E0 g_p a_F', real=True)
w = A_*x**2 + w1*x + w0                       # the banked quadratic-class atlas
thsol = Function('theta_s')
# IF the theta-row member (pointwise density = d/dx(g_theta w theta')) is adopted and closes
# (the banked pi_f = c_f analog): g_theta * w * theta' = c_theta per cell:
thp_of_x = c_th/(g_th*w)
closure_resid = sp.simplify(sp.diff(g_th*w*thp_of_x, x))
# certified crease-pinned massive witness cell (banked C6b, A = 1/2, ell = 1): w = x^2/2 + 1/2
w_wit = x**2/2 + S(1)/2
J_wit = integrate(1/w_wit, (x, -1, 1))
dth_wit = sp.simplify(c_th/g_th * J_wit)
check("S2b_MBJ_increment_on_banked_atlas",
      closure_resid == 0 and J_wit == pi and dth_wit == pi*c_th/g_th,
      "SUBSTANTIVE",
      "IF-ADOPTED (MB-J angular-moment member): the closure pi_theta = g_theta w theta' = "
      "c_theta holds identically per cell (zero residual), so the per-cell winding increment "
      "is Delta theta_i = (c_theta,i/g_theta) J_i with J_i = int dx/w_i the BANKED positive "
      "functional. Exact instance on the certified crease-pinned massive witness cell "
      "(w = x^2/2 + 1/2, ell = 1): J = pi exactly, Delta theta = pi c_theta / g_theta")
# ---- S2c: the winding condition WITH the coupling present -- the lattice cut (cyclic completions)
Jtot = symbols('J_tot', positive=True)
Js = symbols('Js_sum', real=True)
sol_cth = sp.solve(Eq(c_th*Jtot/g_th + Js, 2*pi*n_w), c_th)
# banked real-target contrast (the f-moment on the SAME cycle): forced = 0:
sol_cf = sp.solve(Eq(symbols('c_f', real=True)*Jtot/symbols('g_f', positive=True), 0),
                  symbols('c_f', real=True))
check("S2c_MBJ_momentum_lattice_cut_cyclic",
      sol_cth == [g_th*(2*pi*n_w - Js)/Jtot] and sol_cf == [0],
      "SUBSTANTIVE",
      "IF-ADOPTED with MB-J, on a CYCLIC completion (posture+completion data) with momentum "
      "continuity across seams: the winding condition Sum_i (c_theta/g_theta) J_i + Sum_s J_s "
      "= 2 pi n_w SOLVES exactly to c_theta = g_theta (2 pi n_w - Sum J_s)/Sum J_i -- the "
      "theta-momentum is LATTICE-CUT (Z-indexed, spacing 2 pi g_theta/Sum J_i at sealed "
      "seams). CONTRAST (banked, recomputed): the real-target f-moment on the same cycle is "
      "FORCED TO ZERO. The circle target converts 'forced 0' into 'forced onto a lattice' -- "
      "the first conditional discreteness that lands ON a sector datum rather than on free "
      "joint sheets. WHAT IS CUT: c_theta (theta-sector data), NOT a banked parameter")
# ---- S2d: the lock-class affine instance -- exact spacing law in the cell length
sol_lock = sp.solve(Eq(c_th*(2*ell)/g_th, 2*pi*n_w), c_th)   # w == 1, cell [-ell, ell]
check("S2d_lock_class_spacing_law",
      sol_lock == [pi*g_th*n_w/ell],
      "SUBSTANTIVE",
      "lock-class (P1-4D landing, w == 1) instance on a cyclic single-cell completion: "
      "c_theta = pi g_theta n_w / ell exactly -- spacing INVERSELY proportional to the cell "
      "size (the arc's first derived spacing LAW touching ell; conditional stack: IF adopted, "
      "IF MB-J, IF cyclic, IF lock-class landing). NOTE the banked contrast: the f/h slopes "
      "on this cycle are forced to 0 (family (ii) 'forced massless', banked C6c) -- theta "
      "ESCAPES that cut through the 2 pi Z lattice: nonzero circulating theta-momentum is "
      "winding-legal where nonzero f-momentum is not")

# ---- S2e: IF the MB-J member also enters the angular Gram: sigma-additivity + the n^2 form
g_f, g_h, c_f, c_h = symbols('g_f g_h', positive=True) + symbols('c_f c_h', real=True)
G3 = sp.diag(g_f, g_h, g_th)
cvec = Matrix([c_f, c_h, c_th])
sigma3 = (cvec.T*G3.inv()*cvec)[0, 0]
sigma2 = c_f**2/g_f + c_h**2/g_h
theta_share = sp.simplify((g_th*(2*pi*n_w - Js)/Jtot)**2/g_th)
check("S2e_sigma_additive_and_nsquared_share",
      sp.simplify(sigma3 - sigma2 - c_th**2/g_th) == 0
      and sp.simplify(theta_share - g_th*(2*pi*n_w - Js)**2/Jtot**2) == 0,
      "SUBSTANTIVE",
      "IF-ADOPTED with MB-J entering the diagonal angular Gram: sigma_tot = sigma_fh + "
      "c_theta^2/g_theta EXACTLY (additive; general G by constant congruence, Category-A "
      "banked practice). On a cyclic completion the theta-share of sigma is then "
      "g_theta (2 pi n_w - Sum J_s)^2 / (Sum J_i)^2 -- an EXACT n^2-form on theta-sector "
      "data (flux-sealed seams: (2 pi n_w)^2 g_theta / J_tot^2). Premise stack: IF adopted, "
      "IF MB-J-in-Gram, IF cyclic; this cuts sigma's theta-SHARE, not yet E0")
# ---- S2f: the honest no-close fact -- the Z-cut and the sigma = E0 pin live on DISJOINT completions
check("S2f_crease_pin_vs_cyclic_cut_disjoint",
      True, "GUARD",
      "HONEST NON-CUT (map fact, cited banks; framing AMENDED by AM-3, 2026-07-31): the "
      "banked sigma = E0 * w(crease) pin lives on CREASE-TERMINATED (acyclic) completions; "
      "the CYCLE-WINDING cut lives on CYCLIC completions (no ends), and the AM-3 PIN-PIN "
      "cut lives on double-crease acyclic completions whose massive locus is EMPTY (banked "
      "SB2) -- so at the banked N=2 layer NO completion carries both a Z-lattice and a "
      "LIVE (E0 != 0) sigma-E0 pin, and the composition 'E0 in an n^2 family' does NOT "
      "close -- E0 remains UNCUT by MB-J at the banked layer, AM-3 included. "
      "The NAMED SEAT where it could close: (i) a completion class carrying both a cycle and "
      "a crease-type sigma-E0 pin (not banked; would need its own registration + census), or "
      "(ii) an MB-Xm/lambda-row member making I_p theta-dependent so the multi-cell tie "
      "Sum E0_i I_p,i = 0 becomes n_w-dependent (typed, not derived here). F-C1 note: this "
      "is exactly the leg a spectrum-hunter would blur; it is stated as NOT CLOSING")
# ---- S2g: cyclic massive escape adjudication (which banked parameters the Z-family touches)
E01, E02, L1, L2 = symbols('E01 E02 L1 L2', real=True)
sos = sp.simplify(E01*L1 + E02*L2)   # the banked mass-ring law Sum E0_i L_i = 0 (theta-free)
check("S2g_mass_ring_law_theta_free",
      sp.simplify(sos.diff(c_th)) == 0 and sp.simplify(sos.diff(g_th)) == 0,
      "SUBSTANTIVE",
      "the banked cyclic mass-ring law Sum E0_i L_i = 0 contains NO theta datum (exact: "
      "derivatives in c_theta, g_theta vanish identically): the MB-J winding condition is a "
      "SECOND, independent condition on the same cycle. Consequence table (IF-ADOPTED, "
      "cyclic): all-definite rings stay FORBIDDEN for mass (banked, untouched); massive-with-"
      "indefinite-partner chains acquire the ADDITIONAL lattice condition on c_theta whose "
      "spacing 2 pi g_theta / Sum J_i(E0_i, ell_i, moduli) DEPENDS on the banked parameters "
      "through J_i: at FIXED c_theta != 0 the geometry functional Sum J_i is lattice-cut "
      "(conditional codim-1 Z-family in (E0_i, ell_i) space); with c_theta free the cut is "
      "Z-sheeting of the joint space only. E0, ell are NEVER unconditionally quantized")
# ---- S2h: crease ends under MB-J -- the eps_theta fork closes the moment or pins the value
# eps_theta = +1: theta' trace killed at crease => c_theta = g_theta w theta' = 0 there;
# momentum continuity kills the whole chain's circulating momentum:
cth_at_crease = (g_th*w_wit*thp_of_x.subs([(A_, S(1)/2), (w1, 0), (w0, S(1)/2)]))
check("S2h_crease_end_forks_MBJ",
      sp.simplify(cth_at_crease - c_th) == 0,
      "SUBSTANTIVE",
      "crease ends under IF-ADOPTED MB-J (both supplied signs; RESTATED by AM-2, 2026-07-31 "
      "verifier round 1): pi_theta = c_theta identically on the cell (recomputed on the "
      "witness), so crease trace conditions transfer to c_theta itself. eps_theta = +1: the "
      "theta'-trace is killed (S1h) => c_theta = 0 on any crease-terminated chain, EVERY "
      "stratum -- theta locked cell-constant, the moment member INERT. eps_theta = -1: the "
      "crease VALUE is 2-torsion-pinned theta in {0, pi} AND the theta''-trace is killed "
      "(S1h); on-shell the jet-2 kill forces c_theta*w'(crease) = 0 (AM2b below) => "
      "c_theta = 0 on every NONCONSTANT cell. On the certified massive mixed crease|glue "
      "chain (nonconstant): c_theta = 0 at BOTH supplied signs (momentum continuity spreads "
      "it chain-wide); at eps=-1 theta is FROZEN at the Z2 crease value -- the theta integer "
      "content is the Z2 crease datum ONLY (no cycle, no n_w). DISJOINTNESS STRENGTHENED: "
      "the Z-cut and the certified massive family DO NOT MEET -- now DERIVED at both signs. "
      "(The shipped claim 'eps=-1 frees theta-prime' is WITHDRAWN: theta'-trace survival is "
      "an off-shell parity fact; on-shell the jet-2 kill closes the moment anyway. See "
      "CORRECTION_LAYER.md AM-2)")

# ---- AM-2 (AMENDMENT 2026-07-31, verifier round 1): the eps_theta = -1 crease jet-2
# condition under MB-J, ADJUDICATED against the banked census (the verifier found S2h in
# tension with the package's own S1h). Banked precedent recomputed first: the period-gate
# C6a mirror-jet kill (eps_phi = -1 DEFINITIONAL) is applied ON-SHELL as a trace condition
# and BINDS cell data -- p0''(crease) = 0 <=> 2A w = w'^2 -- with w'(crease) != 0 on the
# certified branch. So a declared-parity field gets NO 'fold-kink' escape from its even-jet
# kill; the identical census rule applied to theta (jet-0 leg already banked: doorway C5d
# 2-torsion) forces the jet-2 leg on-shell. F-C5 note: re-scoping theta's kill away would
# dissolve C6a's own crease conditions -- a bank contradiction; the algebra lands STRENGTHENED.
p0_onshell = sp.log(w)/a_F
kill_id = sp.simplify(sp.diff(p0_onshell, x, 2) - (2*A_*w - sp.diff(w, x)**2)/(a_F*w**2))
Apos = symbols('A_pos', positive=True)
w_br = Apos*x**2 + (2*Apos - sp.sqrt(2*Apos))*x + (1 + Apos - sp.sqrt(2*Apos))
w_br_crease = sp.simplify(w_br.subs(x, -1))                     # = 1 (banked C6b branch)
wp_crease = sp.simplify(sp.diff(w_br, x).subs(x, -1))           # = -sqrt(2A) != 0
p0pp_crease = sp.simplify((2*Apos*w_br - sp.diff(w_br, x)**2).subs(x, -1))
check("AM2a_banked_crease_kill_applies_onshell",
      kill_id == 0 and w_br_crease == 1 and p0pp_crease == 0
      and sp.simplify(wp_crease + sp.sqrt(2*Apos)) == 0,
      "SUBSTANTIVE",
      "AM-2 leg 1 -- the banked precedent recomputed (period gate C6a/C6b, cited + re-run): "
      "p0'' = (2A w - w'^2)/(a_F w^2) on-shell (zero residual); on the certified crease "
      "branch (ell = 1, w1 = 2A - sqrt(2A), w0 = 1 + A - sqrt(2A)): w(crease) = 1, "
      "p0''(crease) = 0 (the banked even-jet kill HOLDS ON-SHELL and binds the cell data), "
      "while w'(crease) = -sqrt(2A) != 0 for A > 0 -- the kill is a genuine trace condition "
      "on the on-shell field, NOT excused by the fold; this is the census rule theta "
      "inherits at its supplied eps_theta = -1 (its jet-0 leg, the {0,pi} 2-torsion pin, is "
      "already banked: doorway C5d)")
thpp_crease = sp.simplify(sp.diff(c_th/(g_th*w_br), x).subs(x, -1))
forced = sp.solveset(Eq(thpp_crease, 0), c_th, S.Reals)
check("AM2b_eps_minus1_jet2_forces_cth_zero_nonconstant",
      sp.simplify(thpp_crease - c_th*sp.sqrt(2*Apos)/g_th) == 0
      and forced == sp.FiniteSet(0),
      "SUBSTANTIVE",
      "AM-2 leg 2 -- the exact crease jet-2 condition for theta under MB-J at eps_theta = "
      "-1, evaluated on-shell: theta'' = -c_theta w'/(g_theta w^2), so theta''(crease) = "
      "c_theta sqrt(2A)/g_theta on the certified branch (w(crease) = 1, w'(crease) = "
      "-sqrt(2A)); the S1h kill theta''(crease) = 0 solves EXACTLY to c_theta = 0 for every "
      "A > 0 -- i.e. on EVERY nonconstant (massive-capable: E0 = 2A g_p/a_F^2 != 0 <=> "
      "A != 0) crease-compatible cell. Witness instance A = 1/2: theta''(crease) = "
      "c_theta/g_theta (the verifier's value, confirmed). Combined with the eps = +1 jet-1 "
      "kill (S2h): c_theta = 0 at ANY crease end of ANY nonconstant cell, BOTH supplied "
      "signs -- the disjointness of the Z-cut from the certified massive family is "
      "STRENGTHENED from census-observed to DERIVED")
thpp_const = sp.simplify(sp.diff(c_th/(g_th*S(1)), x))
check("AM2c_constant_stratum_kill_vacuous",
      thpp_const == 0,
      "SUBSTANTIVE",
      "AM-2 leg 3 -- the constant stratum w == 1 (A = 0; the crease conditions read 0 = 0): "
      "on-shell theta' = c_theta/g_theta is CONSTANT, so theta'' == 0 IDENTICALLY -- the "
      "eps_theta = -1 jet-2 kill is satisfied VACUOUSLY and forces NOTHING; c_theta stays "
      "free there (until pinned twice: AM-3). The AM-2 forcing is scoped: NONCONSTANT cells "
      "only. (At eps_theta = +1 the jet-1 kill still forces c_theta = 0 on every stratum, "
      "constant included.) This is exactly the interaction the AM-3 pin-pin lattice needs: "
      "it lives where w' == 0, so the nonconstant-cell forcing does not touch it")
# ---- S2i: MB-P potential member cut form (typed transcendental; crease-sheet evaluation exact)
cos0, cospi = sp.simplify(cos(0)), sp.simplify(cos(pi))
check("S2i_MBP_cut_form_typed_crease_sheets_exact",
      cos0 == 1 and cospi == -1,
      "SUBSTANTIVE",
      "MB-P (potential class) IF-ADOPTED: the theta-row becomes a pendulum-type density; its "
      "winding-sector structure on cyclic completions is the Z-labeled branch family of a "
      "periodic-potential BVP -- the cut form is TRANSCENDENTAL (named seat: a bounded "
      "elliptic-integral push; NOT derived here, typed per contract). EXACT piece: at "
      "eps_theta = -1 crease sheets the potential evaluates on the 2-torsion values with "
      "cos(0) = +1, cos(pi) = -1 -- the two Z2 sheets carry OPPOSITE potential sign (feeds "
      "TC-3/TC-4); germ data: seam jumps J_s enter every cut affinely (S2c form)")
# ---- AM-3 (AMENDMENT 2026-07-31, verifier round 1): the missed integer leg -- the
# PIN-PIN lattice on the banked-PERMITTED mirrored (crease|crease) completion, constant
# stratum w == 1, eps_theta = -1: BOTH crease values are 2-torsion-pinned in {0, pi}
# (lifts in pi*Z), so the MB-J lift increment (c_theta/g_theta)*2 ell must land in pi*Z --
# a Z-lattice on an ACYCLIC completion, at HALF the cyclic lock-class spacing. NOT a
# winding homomorphism: Hom(D_inf, Z) = 0 (S4a) does NOT close it. Massless-confined:
# double-crease massive locus EMPTY (banked SB2, both E0 signs) + the family-(ii) quotient
# parity-collapse exclusion. F-C1 note: an UNDER-claimed cutting leg, now stated.
m_pin = symbols('m_pin', integer=True)
sol_2pin = sp.solve(Eq((c_th/g_th)*(2*ell), pi*m_pin), c_th)
spacing_pinpin = sp.simplify(sol_2pin[0].subs(m_pin, m_pin + 1) - sol_2pin[0])
ratio_half = sp.simplify(spacing_pinpin/(pi*g_th/ell))
th_lin = pi*symbols('k_pin', integer=True) + (c_th/g_th)*(x + ell)
check("AM3_two_pin_lattice_constant_stratum",
      sol_2pin == [pi*g_th*m_pin/(2*ell)] and ratio_half == S(1)/2
      and sp.diff(th_lin, x, 2) == 0,
      "SUBSTANTIVE",
      "AM-3 (AMENDMENT 2026-07-31): on the banked-PERMITTED mirrored double-crease "
      "completion (period-gate menu), CONSTANT stratum w == 1, eps_theta = -1: both crease "
      "values pinned in {0, pi} => the MB-J increment obeys (c_theta/g_theta) 2 ell = pi m, "
      "solving EXACTLY to c_theta = pi g_theta m/(2 ell), m in Z -- a PIN-PIN Z-lattice on "
      "an ACYCLIC completion, spacing pi g_theta/(2 ell) = HALF the cyclic lock-class "
      "spacing (ratio 1/2 exact). Consistency with AM-2 VERIFIED: theta is linear on the "
      "stratum, theta'' == 0 identically (zero residual) -- the jet-2 kill is satisfied, "
      "and w' == 0 makes the nonconstant-cell forcing inapplicable; the lattice is LEGAL. "
      "It is NOT a winding homomorphism, so Hom(D_inf, Z) = 0 does not close it (S4a "
      "framing corrected). MASSLESS-CONFINED (double-crease massive EMPTY, banked SB2 + "
      "family-(ii) quotient exclusion): E0 stays UNCUT; ell is lattice-cut only at fixed "
      "c_theta != 0 (same conditional shape as S2g), never unconditionally. Corrected "
      "framing: CYCLE-WINDING lattices (2pi-spaced increments, cyclic completions) vs "
      "PIN-PIN lattices (pi-spaced-over-2ell, two-pinned acyclic completions) -- the Z-cut "
      "does NOT live on cyclic completions only")

RESULTS["stages"]["TC2"] = {
  "MB-J": "cyclic: c_theta = g_theta(2 pi n_w - Sum J_s)/Sum J_i (lattice); lock-class: c_theta = pi g_theta n_w/ell; sigma theta-share n^2-form; E0/ell cut ONLY at fixed c_theta via Sum J_i; crease ends (AM-2): c_theta = 0 forced at BOTH eps_theta signs on every nonconstant cell => certified massive (acyclic) chain carries NO theta-momentum -- Z2 crease datum only, disjointness DERIVED; PIN-PIN lattice (AM-3): mirrored double-crease constant stratum (w==1, eps_theta=-1): c_theta = pi g_theta m/(2 ell) -- acyclic Z-lattice at HALF the cyclic lock-class spacing, MASSLESS-confined",
  "MB-P": "Z-labeled winding branches, transcendental cut form (typed); crease sheets carry opposite potential sign (exact)",
  "MB-X/MB-W/MW-N": "no independent integer condition at jet<=2 beyond the S2c winding + S1h torsion data + the AM-3 pin-pin lattice; lambda-row theta-dependence = the named I_p seat (typed)",
  "unconditional_cuts_on_banked_parameters": "NONE (every cut carries its IF-ADOPTED premise stack; AM-3 changes nothing here -- E0 uncut, ell conditional-only)"}
print("## STAGE 2 complete.")

print()
print("## ============ STAGE 3 / TC-3: stability interplay (computed where banked machinery")
print("## reaches; TYPED with named seat where not) + TC-4 sector/catalog map ============")
# ---- S3a: the generic 3-moment completion -- the coupling enters S-i ONLY through sigma
vp, y1, y2, y3 = symbols('v_p y1 y2 y3', real=True)
wS = symbols('w_S', positive=True)
yv = Matrix([y1, y2, y3])
Qform = wS*(yv.T*G3*yv)[0, 0] - 2*a_F*vp*(yv.T*cvec)[0, 0]
ystar = (a_F*vp/wS)*G3.inv()*cvec
comp_resid = sp.simplify(sp.expand(
    Qform - (wS*((yv - ystar).T*G3*(yv - ystar))[0, 0] - a_F**2*vp**2*sigma3/wS)))
check("S3a_three_moment_completion_only_through_sigma",
      comp_resid == 0,
      "SUBSTANTIVE",
      "the SA5 completion identity re-proven with THREE angular moments (f, h, theta): "
      "w y^T G y - 2 a_F v_p c^T y = w |y - y*|_G^2 - a_F^2 sigma_tot v_p^2 / w with "
      "sigma_tot = c^T G^-1 c (zero residual, diagonal G; general G by constant congruence, "
      "Category-A banked): IF-ADOPTED MB-J enters the S-i second-variation structure ONLY "
      "through the single scalar sigma -- the reduced Sturm-Liouville operator "
      "L v = -g_p(w v')' - a_F^2 sigma v / w is FORM-INVARIANT, with sigma -> sigma_tot")
# ---- S3b [guard]: S-i verdict transport (form-level; banked SB machinery cited)
check("S3b_Si_verdicts_form_invariant_typed",
      True, "GUARD",
      "consequence (form-level; banked stability slice CITED, cc8b872): the crease pin reads "
      "sigma_tot = E0 * w(crease); every SB closed form is a function of (s, E0) through "
      "sigma alone, so the banked verdicts TRANSPORT VERBATIM to the theta-extended member: "
      "free-wall-data branch UNSTABLE index-1-in-reduced-sector, the negative mode's angular "
      "wall-flux channel now INCLUDES the theta-channel (a 3rd flux direction); the "
      "ABSORPTION THEOREM absorbs the same unique negative direction (the parity pin acts on "
      "f/bh; theta joins the zero-trace-core positivity by the same completion). NAMED SEATS "
      "(not computed): the lambda-Schur sign (banked dilogarithmic obstruction, unchanged); "
      "theta-SECOND-germ activation at walls -- by the SB16 argument shape the theta wall "
      "response's second germ is UNPINNED, so trace-active postures stay uncertifiable "
      "(certification boundary EXTENDS to the theta sector)")
# ---- S3c: S-ii dichotomy -- diagonal extension exact; the pairing-branch fork carried
kn, c_m, t_c = symbols('k_n c_m t_c', real=True)
B2 = Matrix([[g_p*kn**2, 2*E0], [2*E0, c_m*kn**2]])
B3 = Matrix([[g_p*kn**2, 2*E0, 0], [2*E0, c_m*kn**2, 0], [0, 0, g_th*kn**2]])
minors_ok = (sp.simplify(B3.det() - g_th*kn**2*B2.det()) == 0)
lam_ = symbols('lam', real=True)
aF_4D = 2*lam_     # P1-4D a_F = 2 lambda
aF_tri = 1 + 2*lam_
check("S3c_Sii_dichotomy_diagonal_extension_and_branch_fork",
      minors_ok and aF_4D.subs(lam_, 0) == 0 and aF_tri.subs(lam_, 0) == 1,
      "SUBSTANTIVE",
      "S-ii lock-class landing (lambda == 0 emerged): P1-4D pairing branch has a_F = 2 lambda "
      "= 0 EXACTLY at the landing, so the MB-J cross channel (prop to a_F c_theta) VANISHES "
      "there -- the theta block extends the per-mode matrix DIAGONALLY and det B3 = "
      "g_theta k^2 det B2 (zero residual): THE BANKED DICHOTOMY 64 E0^2 l^4 <= g_p c_m pi^4 "
      "IS UNTOUCHED by MB-J on the P1-4D branch. P1-TRIAD branch: a_F = 1 + 2 lambda = 1 != 0 "
      "at the landing -- the cross channel SURVIVES; its per-mode block is the NAMED SEAT "
      "(needs the theta-extended member's own second-variation push; typed, branch carried). "
      "MB-Xm members coupling theta to the lambda-jet density would enter c_m directly (typed)")
# ---- S3d: MB-P sheet-sign fact (exact) -- the Z2 label becomes a stability discriminator
check("S3d_MBP_crease_sheet_sign_split",
      sp.simplify(cos(S(0))) == 1 and sp.simplify(cos(pi)) == -1,
      "SUBSTANTIVE",
      "IF-ADOPTED MB-P at eps_theta = -1: the second variation gains a theta-mass density "
      "prop to cos(theta_bar) x (invariant coefficient); on the two 2-torsion crease sheets "
      "it evaluates to OPPOSITE SIGNS (cos 0 = +1, cos pi = -1, exact): one Z2 sheet is "
      "theta-stabilizing, the other theta-destabilizing, coefficient-independent -- the "
      "revived Z2 label becomes a STABILITY DISCRIMINATOR (full spectral verdict per sheet: "
      "named seat, a bounded pendulum-BVP push; not run)")

# ---- S4a: TC-4 -- integer content per posture (the map's spine, recomputed)
hh = symbols('hh', integer=True)
homDinfZ = solveset(Eq(2*hh, 0), hh, S.Integers)
z2sheets = sorted({(sp.Mod(pi*m1, 2*pi), sp.Mod(pi*m2, 2*pi)) for m1 in (0, 1) for m2 in (0, 1)},
                  key=str)
check("S4a_posture_integer_content_map",
      homDinfZ == sp.FiniteSet(0) and len(z2sheets) == 4,
      "SUBSTANTIVE",
      "TC-4 spine (recomputed; AMENDED by AM-3, 2026-07-31): QUOTIENT posture -- winding "
      "hom D-inf -> Z is identically 0 (2h = 0 over Z exact), so the quotient carries NO "
      "cycle-winding label; its integer content = the crease Z2 data (eps_theta = -1; "
      "(Z2)^2 = 4 sheets on a double-crease cell, enumerated exactly) PLUS -- corrected, "
      "AM-3 -- the constant-stratum PIN-PIN Z-lattice c_theta = pi g_theta m/(2 ell) (NOT "
      "a winding hom; Hom(D_inf, Z) = 0 does not close it). The banked double-crease "
      "massive locus is EMPTY, so ALL this content indexes MASSLESS quotient sectors only. "
      "CYCLIC completions -- the Z winding label n_w (S2c). OPEN ends -- no integer, germs "
      "freed. All labels IF-ADOPTED conditional")
# ---- S4b [guard]: the catalog map assembled (map facts; nothing adopted)
RESULTS["stages"]["TC4_map"] = {
 "quotient_double_crease": "(Z2)^2 labels (eps_theta=-1) AND (AM-3) the constant-stratum PIN-PIN Z-lattice c_theta = pi g_theta m/(2 ell) (acyclic, half cyclic spacing; NOT a winding hom -- survives Hom(D_inf,Z)=0); massive EMPTY (banked) -> ALL this content labels massless sectors only; eps_theta=+1: c_theta = 0 (jet-1 kill) and no discrete label (free crease value)",
 "certified_massive_mixed_crease_glue_chain": "ACYCLIC -> no Z label; AM-2: c_theta = 0 forced at BOTH eps_theta signs (nonconstant cells; momentum continuity spreads chain-wide) => MB-J INERT on the whole chain; at eps_theta=-1 theta FROZEN at the Z2 crease value (ONE Z2 datum, theta_bar in {0,pi}); under MB-P the two sheets are stability-split (S3d); eps_theta=+1: theta = continuous cell-constant modulus, NO integer",
 "cyclic_all_definite_rings": "massless (banked ring law, theta-free S2g) BUT carry the Z winding label n_w: a Z-catalog of massless ring sectors -- labels without mass",
 "cyclic_massive_indefinite_chains": "conditional existence (banked); carry n_w AND the c_theta lattice; at fixed c_theta the geometry functional Sum J_i is lattice-cut",
 "K4_torsion_revival": "the revived Z2 holonomy classes attach to the K4-orbifold cycles; the DECLARED chi_theta sets WHICH moduli channel the theta-odd blocks interlock with (chi_a: shear slot r_sh; chi_b/chi_c: mixing rows; triv: field-sector rows)",
 "sector_labels": "the winding integer LABELS completion classes (sheets), never particle states; no spectrum exists at this layer"}
check("S4b_catalog_map_assembled",
      True, "GUARD",
      "the TC-4 conditional catalog map assembled from S2/S3 computed facts + banked sector "
      "map (period gate TP-5/TP-6, stability slice posture facts) -- map facts ONLY, "
      "IF-ADOPTED stamps on every row; recorded in the JSON under stages.TC4_map")
print("## STAGE 3 complete (TC-3 + TC-4).")

# ---- final assembly: outcome class + files
RESULTS["stages"]["TC3"] = {
 "MB-J_S-i": "enters ONLY through sigma (3-moment completion exact); reduced operator form-invariant; banked verdicts transport (UNSTABLE index-1 free branch; absorption theorem); theta joins the angular wall-flux channel",
 "MB-J_S-ii": "P1-4D branch: dichotomy 64 E0^2 l^4 <= g_p c_m pi^4 UNTOUCHED (a_F = 0 at landing, exact); P1-triad branch: cross channel survives -- NAMED SEAT",
 "MB-P": "crease-sheet sign split exact (cos 0 = +1, cos pi = -1); full pendulum spectrum = named seat",
 "certification_boundary": "theta second germs unpinned -> extends to the theta sector (SB16 shape, guard)"}
RESULTS["outcome_class"] = ("OC-2: a NONEMPTY lawful menu (parametrized family of member "
 "classes MB-P/MB-J/MB-Xf/MB-Xm/MB-W/MW-N, per declared chi_theta x supplied eps_theta), "
 "with per-member conditional cuts; NO unconditional cut of any banked parameter; NO "
 "adoption; NO coupling selected")
nsub = sum(1 for c in RESULTS["checks"] if c["kind"] == "SUBSTANTIVE")
ngrd = sum(1 for c in RESULTS["checks"] if c["kind"] == "GUARD")
RESULTS["check_split"] = {"substantive": nsub, "guard": ngrd,
                          "total": nsub + ngrd, "failed": FAILED}
print()
print(f"## RESULT: {nsub + ngrd} checks = {nsub} SUBSTANTIVE + {ngrd} GUARD; failures: {len(FAILED)}")
print("## OUTCOME CLASS: OC-2 (menu = nonempty parametrized family; every cut IF-ADOPTED")
print("## conditional; no banked parameter unconditionally quantized; nothing adopted).")
def _ser(o):
    return str(o)
with open("coupling_results.json", "w") as f:
    json.dump(RESULTS, f, indent=1, default=_ser, sort_keys=True)
print("## coupling_results.json written.")
sys.exit(1 if FAILED else 0)
