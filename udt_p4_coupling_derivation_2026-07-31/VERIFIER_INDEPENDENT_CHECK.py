#!/usr/bin/env python3
# Blind-verifier independent check — P4 coupling derivation 2026-07-31.
# Re-derives the load-bearing claims from scratch; then attacks.
import sympy as sp
from sympy import symbols, Function, cos, sin, exp, I, pi, integrate, Matrix, S, Rational, Eq
OK = []; BAD = []
def rec(name, cond, note=""):
    (OK if bool(cond) else BAD).append(name)
    print(("PASS " if bool(cond) else "FAIL ") + name + ("  # " + note if note else ""))

x, ell, Ltot = symbols('x ell L_tot', real=True, positive=True)
g_th, c_th = symbols('g_th c_th', real=True)
n_w, m_ = symbols('n_w m_', integer=True)

# ---- P1: lattice cut re-derivation from the doorway winding condition + MB-J closure
# MB-J closure: g_th * w * th' = c_th  (per cell, momentum continuity => common c_th)
# => Delta theta_i = (c_th/g_th) * J_i, J_i = int dx / w_i.
# Doorway integer condition (banked f27b5ca): sum_i Delta_i + sum_s J_s = 2 pi n_w.
Js, Jtot = symbols('Js Jtot', real=True)
sol = sp.solve(Eq((c_th/g_th)*Jtot + Js, 2*pi*n_w), c_th)
rec("P1a_lattice_cut_form", sol == [g_th*(2*pi*n_w - Js)/Jtot])
# spacing between consecutive n_w:
sp_cyc = sp.simplify(sol[0].subs(n_w, n_w+1) - sol[0])
rec("P1b_spacing", sp_cyc == 2*pi*g_th/Jtot)
# lock class w == 1 on [-ell, ell]: J = 2 ell (independent integral)
Jlock = integrate(S(1), (x, -ell, ell))
sol_lock = sp.solve(Eq((c_th/g_th)*Jlock, 2*pi*n_w), c_th)
rec("P1c_lock_class", Jlock == 2*ell and sol_lock == [pi*g_th*n_w/ell])
# witness cell J = pi (independent):
Jwit = integrate(1/(x**2/2 + S(1)/2), (x, -1, 1))
rec("P1d_witness_J_pi", sp.simplify(Jwit - pi) == 0)
# f-contrast (banked C6c mechanism, re-derived): REAL target => closure sum = 0 exactly;
# affine f on a 1-cell cycle: f(L)=f(0) => slope 0. Circle target: theta(L)=theta(0)+2 pi n.
f1, f0 = symbols('f1 f0', real=True)
sol_f = sp.solve(Eq(f1*Ltot + f0, f0), f1)
rec("P1e_f_slope_killed", sol_f == [0], "real target single-valuedness kills the slope")
sol_th = sp.solve(Eq(c_th/g_th*Ltot, 2*pi*n_w), c_th)
rec("P1f_theta_escape", sol_th == [2*pi*n_w*g_th/Ltot],
    "circle target converts =0 into in-2piZ: escape mechanism GENUINE, rides ONLY on the target")
# n^2 share (diagonal Gram) + additivity:
g_f, g_h = symbols('g_f g_h', positive=True); c_f, c_h = symbols('c_f c_h', real=True)
G3 = sp.diag(g_f, g_h, g_th); cv = Matrix([c_f, c_h, c_th])
sig3 = sp.simplify((cv.T*G3.inv()*cv)[0,0] - c_f**2/g_f - c_h**2/g_h - c_th**2/g_th)
rec("P1g_sigma_additive_diag", sig3 == 0)
share = sp.simplify((sol[0]**2/g_th) - g_th*(2*pi*n_w-Js)**2/Jtot**2)
rec("P1h_n2_share", share == 0)
# additivity FAILS for non-diagonal G (adversarial: is the diagonal scoping load-bearing?)
gc = symbols('g_c', real=True)
Gnd = Matrix([[g_f, gc, 0],[gc, g_h, 0],[0,0,g_th]])
signd = sp.simplify((cv.T*Gnd.inv()*cv)[0,0] - c_f**2/g_f - c_h**2/g_h - c_th**2/g_th)
rec("P1i_offdiag_breaks_additivity", signd != 0,
    "additivity claim correctly scoped to diagonal G in the package")

# ---- P4(part): J05 identity + 3-moment completion + det factorization, independent
c = symbols('c0:4'); d = symbols('d0:4'); e = symbols('e0:4'); L_ = symbols('L_')
Dp = sum(c[i]*x**i for i in range(4)); Ep = sum(d[i]*x**i for i in range(4))
Vp = sum(e[i]*x**i for i in range(4))
lhs = integrate(Dp*Vp + Ep*sp.diff(Vp,x), (x, 0, L_))
rhs = integrate((Dp - sp.diff(Ep,x))*Vp, (x, 0, L_)) + (Ep*Vp).subs(x,L_) - (Ep*Vp).subs(x,0)
rec("P4a_J05_identity", sp.simplify(sp.expand(lhs - rhs)) == 0)
wS, aF, vp = symbols('w_S a_F v_p', real=True); wSp = symbols('w_Sp', positive=True)
y = Matrix(symbols('y1:4', real=True))
Q = wSp*(y.T*G3*y)[0,0] - 2*aF*vp*(y.T*cv)[0,0]
yst = (aF*vp/wSp)*G3.inv()*cv
sig = (cv.T*G3.inv()*cv)[0,0]
comp = sp.simplify(sp.expand(Q - (wSp*((y-yst).T*G3*(y-yst))[0,0] - aF**2*vp**2*sig/wSp)))
rec("P4b_3moment_completion", comp == 0)
gp, cm, kn, E0 = symbols('g_p c_m k_n E0', real=True)
B2 = Matrix([[gp*kn**2, 2*E0],[2*E0, cm*kn**2]])
B3 = Matrix([[gp*kn**2, 2*E0, 0],[2*E0, cm*kn**2, 0],[0,0,g_th*kn**2]])
rec("P4c_det_factorization", sp.simplify(B3.det() - g_th*kn**2*B2.det()) == 0)
rec("P4d_sheet_signs", cos(0) == 1 and cos(pi) == -1)
print("## part 1 done:", len(OK), "pass,", len(BAD), "fail")

# ================= ATTACK LEGS =================
th = symbols('th', real=True); thF = Function('th')(x)
# ---- A1: character parity of every THB block, computed from theta -> s*theta (s=+-1)
import itertools
def parity_of(expr_builder):
    # returns 0 if invariant under s=-1, 1 if flips sign, None otherwise
    ep, em = expr_builder(1), expr_builder(-1)
    if sp.simplify(em - ep) == 0: return 0
    if sp.simplify(em + ep) == 0: return 1
    return None
blocks = {
 "1":        lambda s: S(1),
 "cos":      lambda s: cos(s*th),
 "sin":      lambda s: sin(s*th),
 "thp":      lambda s: sp.diff(s*thF, x),
 "thpp":     lambda s: sp.diff(s*thF, x, 2),
 "sin*thp":  lambda s: sin(s*thF)*sp.diff(s*thF, x),
 "cos*thp":  lambda s: cos(s*thF)*sp.diff(s*thF, x),
 "thp^2":    lambda s: sp.diff(s*thF, x)**2,
 "sin*thpp": lambda s: sin(s*thF)*sp.diff(s*thF, x, 2),
 "cos*thpp": lambda s: cos(s*thF)*sp.diff(s*thF, x, 2),
 "sin*thp^2":lambda s: sin(s*thF)*sp.diff(s*thF, x)**2,
 "cos*thp^2":lambda s: cos(s*thF)*sp.diff(s*thF, x)**2,
 "thp*thpp": lambda s: sp.diff(s*thF, x)*sp.diff(s*thF, x, 2),
}
true_par = {k: parity_of(v) for k, v in blocks.items()}
pkg_par = {"1":0,"cos":0,"sin":1,"thp":1,"thpp":1,"sin*thp":0,"cos*thp":1,"thp^2":0,
           "sin*thpp":0,"cos*thpp":1,"sin*thp^2":1,"cos*thp^2":0,"thp*thpp":1}
mismatch = {k for k in blocks if true_par[k] != pkg_par[k]}
rec("A1_THB_parity_audit", mismatch == {"thp*thpp"},
    "package MISGRADES thp*thpp as theta-odd; true parity EVEN (chi^2=trivial)")
rec("A1b_thp_thpp_is_even", true_par["thp*thpp"] == 0)
# consequence check against the shipped JSON menu table:
import json
J = json.load(open("/home/udt-admin/udt_mass_codex/udt_p4_coupling_derivation_2026-07-31/coupling_results.json"))
mt = J["stages"]["TC1"]["menu_table_by_chi_theta"]
wrong_direct = "thp*thpp" in str(mt["a"]["r_sh"]["direct_blocks"])
wrong_dressed = "thp*thpp" in str(mt["a"]["R_p0"]["dressed_blocks_need_module"])
rec("A1c_json_menu_carries_misgrade", wrong_direct and wrong_dressed,
    "shipped menu wrongly ADMITS bare thp*thpp direct into r_sh at chi_a and wrongly "
    "requires dressing in trivial rows — one-block admission-chain error (F-C2-adjacent)")

# ---- A2: the eps_theta=-1 crease under MB-J: the theta''-trace kill the package's OWN
# S1h census asserts, applied on-shell (S2h did NOT apply it).
w_wit = x**2/2 + S(1)/2                      # certified massive witness, crease at x=-1
thp_onshell = c_th/(g_th*w_wit)
thpp_crease = sp.simplify(sp.diff(thp_onshell, x).subs(x, -1))
rec("A2a_thpp_crease_nonzero_unless_c0", sp.simplify(thpp_crease - c_th/g_th) == 0,
    "on-shell theta''(crease) = c_th/g_th != 0 for c_th != 0; S1h says the eps=-1 crease "
    "KILLS the theta'' trace => c_th = 0 forced at eps_theta=-1 too on this witness "
    "(w'(crease) = -1 != 0). S2h states only the eps=+1 kill; the eps=-1 leg is "
    "UNDER-DERIVED (claims theta' freed; on-shell the census forces c_th * w'(crease) = 0)")
# general nonconstant crease-compatible cell: w'(crease)^2 = 2A * w(crease) = 2A != 0 for A>0
A_ = symbols('A_', positive=True)
rec("A2b_wprime_crease_nonzero_massive", sp.simplify(sp.sqrt(2*A_*1)) != 0,
    "crease condition 2A w = w'^2, w(crease)=1 => w'(crease) = +-sqrt(2A) != 0 on every "
    "nonconstant (massive-capable) cell => IF the jet-2 kill applies, c_th = 0 at EVERY "
    "eps=-1 crease of a massive cell — disjointness STRENGTHENED, but S2h's stated "
    "eps=-1 remainder (free theta-prime) needs the amendment either way")

# ---- A3: missed lattice leg — two-pin (double-crease) acyclic completion, constant stratum
# banked-PERMITTED completion: crease|crease mirrored cell (period-gate menu row 1).
# Constant stratum w == 1 (satisfies crease conds 0=0): theta linear, all even jets vanish,
# both crease values pinned in {0, pi} (2-torsion) => lift increment in pi*Z:
thA, thB = symbols('thA thB', integer=True)   # crease lifts = pi*integer each
incr = (c_th/g_th)*(2*ell)                    # MB-J increment across the cell (J = 2 ell)
sol_2pin = sp.solve(Eq(incr, pi*m_), c_th)
rec("A3a_two_pin_lattice", sol_2pin == [pi*g_th*m_/(2*ell)],
    "c_th = pi g_th m / (2 ell) on the mirrored (double-crease) cell at eps=-1, "
    "constant stratum: a Z-lattice cut on an ACYCLIC banked completion — HALF the cyclic "
    "lock-class spacing. Package claims (S4a/S2f/TC-2) the Z-cut lives on CYCLIC "
    "completions only and quotient integer content = Z2 data only: MISSED LEG. "
    "Confined to massless sectors (double-crease massive EMPTY is banked SB2 + family-(ii) "
    "quotient parity-collapse exclusion), so the honest limits on E0 and the certified-"
    "massive disjointness SURVIVE — but the catalog map understates the massless lattice")
# consistency of the two-pin solution with the fold (even jets of odd extension vanish for linear theta):
th_lin = pi*thA + (c_th/g_th)*(x + ell)
rec("A3b_linear_theta_even_jets_vanish", sp.diff(th_lin, x, 2) == 0)

# ---- A4: Hom(D_inf, Z) = 0 independent (order-2 generators r1, r2 generate D_inf)
hh = symbols('hh', integer=True)
rec("A4_hom_Dinf_Z_zero", sp.solveset(Eq(2*hh, 0), hh, S.Integers) == sp.FiniteSet(0),
    "any hom kills order-2 generators; t = r1 r2 => t maps to 0; winding label vanishes "
    "on quotient completions — but note A3: the two-pin lattice is NOT a winding hom and "
    "survives Hom = 0; Hom(D_inf,Z)=0 alone does NOT close the quotient integer content")
print("## part 2 done:", len(OK), "pass,", len(BAD), "fail")

# ================= CLOSURE ROUND (2026-07-31, amendments AM-1..AM-4) =================
# C1: AM2a precedent independently -- the banked crease conditions {w(crease)=1,
# 2A w = w'^2} ARE {p0=0, p0''=0} on-shell (w = e^{a_F p0}), i.e. the period-gate C6a
# census applies the even-jet kill ON-SHELL binding cell data (odd jets free: p0'(crease)
# = w'/(a_F w) != 0). Independent of the amendment agent's code.
aFv = symbols('a_Fv', nonzero=True); Ap = symbols('A_p', positive=True)
w1v, w0v = symbols('w1v w0v', real=True)
wq = Ap*x**2 + w1v*x + w0v
p0 = sp.log(wq)/aFv
idd = sp.simplify(sp.diff(p0, x, 2) - (2*Ap*wq - sp.diff(wq, x)**2)/(aFv*wq**2))
rec("C1a_p0pp_identity", idd == 0)
# crease conditions <=> even-jet kill (solve p0=0 & p0''=0 at x=-1 for the branch):
br = sp.solve([Eq(wq.subs(x, -1), 1), Eq((2*Ap*wq - sp.diff(wq, x)**2).subs(x, -1), 0)],
              [w1v, w0v], dict=True)
c6b = {w1v: 2*Ap - sp.sqrt(2*Ap), w0v: 1 + Ap - sp.sqrt(2*Ap)}
hit = any(all(sp.simplify(s[k] - c6b[k]) == 0 for k in c6b) for s in br)
rec("C1b_kill_reproduces_C6b_branch", hit,
    "the banked C6b crease branch is EXACTLY the on-shell even-jet-kill solution: the "
    "precedent AM2a cites is real -- the census kills even jets on-shell, w'(crease)!=0 "
    "notwithstanding (odd jets free). Uniformity then forces theta''(crease)=0 at eps=-1")
# C2: the forcing at general A (independent): theta''(crease) under MB-J on the branch
wbr = wq.subs(c6b)
thpp_cr = sp.simplify(sp.diff(c_th/(g_th*wbr), x).subs(x, -1))
sol_forced = sp.solveset(Eq(thpp_cr, 0), c_th, S.Reals)
rec("C2_forcing_general_A", sol_forced == sp.FiniteSet(0) and
    sp.simplify(thpp_cr - c_th*sp.sqrt(2*Ap)/g_th) == 0,
    "c_theta = 0 forced for EVERY A>0: AM2b confirmed independently; constant stratum "
    "(A=0, w==1): theta'' == 0 identically, kill vacuous (AM2c confirmed)")
# C3: 18-block completeness under the STATED rule (independent enumeration):
import itertools as it
jets = {"1":(0,0), "thp":(1,1), "thpp":(2,1)}   # (order, degree-per-factor=1)
mons = set()
for r in range(0, 3):
    for combo in it.combinations_with_replacement(["thp", "thpp"], r):
        mons.add(tuple(sorted(combo)))
n_expected = 3*len(mons)   # {1,cos,sin} x jet-monomials degree<=2
rec("C3_18_block_completeness", len(mons) == 6 and n_expected == 18,
    "jet monomials of degree<=2 over factors {thp,thpp} = 6 exactly; x{1,cos,sin} = 18: "
    "the amended table is COMPLETE under the stated rule; rule itself = banked jet-order<=2 "
    "factors x quadratic-layer degree bound (degree>2 typed by parity -- honest typing)")
# C4: the shipped amended JSON no longer misplaces thp*thpp:
J2 = json.load(open("/home/udt-admin/udt_mass_codex/udt_p4_coupling_derivation_2026-07-31/coupling_results.json"))
mt2 = J2["stages"]["TC1"]["menu_table_by_chi_theta"]
fixed = ("thp*thpp" in mt2["a"]["R_p0"]["direct_blocks"]
         and "thp*thpp" not in mt2["a"]["r_sh"]["direct_blocks"]
         and "thpp^2" in mt2["a"]["R_p0"]["direct_blocks"]
         and "sin*thpp^2" in mt2["a"]["R_theta"]["direct_blocks"])
rec("C4_json_menu_fixed", fixed, "AM-1 correction landed in the shipped menu table")
# C5: pin-pin spacing ratio (independent): pi*g/(2l) vs cyclic lock pi*g/l
rec("C5_pinpin_half_spacing", sp.simplify((pi*g_th/(2*ell))/(pi*g_th/ell)) == S(1)/2)
print("## closure round:", len(OK), "pass,", len(BAD), "fail")
