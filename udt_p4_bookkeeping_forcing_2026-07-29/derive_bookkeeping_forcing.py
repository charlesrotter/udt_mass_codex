#!/usr/bin/env python3
# P4 BOOKKEEPING-FORCING derivation script (TF1-TF4 computational legs).
# Contract: udt_p4_bookkeeping_forcing_2026-07-29/PREREGISTRATION.md (frozen first).
# Exact SymPy only: no floats, no numeric solvers, no randomness, no network, no GPU.
# Honest split: SUBSTANTIVE = zero-residual symbolic computation carrying load;
# GUARD = definitional-unpacking / citation / typing bookkeeping of banked facts.
# Deterministic; exit nonzero on any failure (F-K6: failures recorded as-is).
#
# AMENDMENT PASS (2026-07-29, post-verifier; VERIFIER_REPORT.md verdict
# PASS-WITH-REQUIRED-AMENDMENTS; record = CORRECTION_LAYER.md): A1 (required) = the
# TF4 field-census massless statement now carries the no-moduli-jet-alphabet clause
# (check TF4_stakes_map_fact_restatement detail; echoed in EXACT_DERIVATION sec.4 and
# RESIDUAL_DECISION_SURFACE.md); A2 (recommended, implemented) = the S1 guard
# adjudicates the upstream 07-25 registration phrase "exactly seven pointwise
# extension parameters" (an at-a-point count; decides neither census branch); plus
# TWO verifier checks ADOPTED as credited in-package checks (the continuously
# x-dependent Duhamel-transport cocycle leg; the Route-P swap-dressing parity
# candidate — a CANDIDATE INPUT, explicitly NOT banked as a parity derivation).
# No computed claim changed; honest split becomes 13 substantive + 8 guards = 21.
#
# Standing scope stamps (travel with every check): registered positive triangular
# chart; registered stationary one-parameter presentation; jet <= 2; enumerated
# anchored pairing family (P1-4D, P1-triad, P2, P3-bulk*) with W_M = e^{a_M p0}
# (P1 per-slot moduli weights SUPPLIED open structure, banked Stage-3 premise;
# P2 = a_M = 0); off-shell typing computations unless stamped otherwise; BASE
# (constant-moduli) vs BR-M (field-moduli) census branches BOTH carried, NEITHER
# adopted (F-K4). Coordinate measure dx = Category-A conditioning (banked).

import json
import sys

import sympy as sp

CHECKS = []


def check(name, kind, ok, detail):
    CHECKS.append({"name": name, "kind": kind, "passed": bool(ok), "detail": detail})
    print("[%s] [%s] %s :: %s" % ("PASS" if ok else "FAIL", kind, name, detail))


x, t = sp.symbols("x t", real=True)
aM = sp.Symbol("a_M", real=True, nonzero=True)   # supplied moduli-slot weight exponent
aF = sp.Symbol("a_F", real=True)                 # field-slot weight exponent
dm = sp.Symbol("dm", real=True)                  # a constant moduli variation

# ----------------------------------------------------------------------------
# TF1 — the pairing-form theorem
# ----------------------------------------------------------------------------

# [1] GUARD: constant-fork row is the integrated scalar (definitional unpacking of
# the banked enumerated pairing on a one-dimensional tangent direction; re-states
# Slice-2 `T0_base_branch_integrated_row` [guard]). Instance: constant pulls out.
g_dens = 1 + x + x**2                       # arbitrary sample density
W_poly = 1 + x**2                           # e^{a_M p0} at a_M=1, p0=log(1+x^2): a
                                            # legal off-shell configuration instance
lhs = sp.integrate(W_poly * g_dens * dm, (x, -1, 1))
rhs = dm * sp.integrate(W_poly * g_dens, (x, -1, 1))
check(
    "TF1_constant_fork_integrated_row_definitional", "guard",
    sp.simplify(lhs - rhs) == 0,
    "constant delta-m pulls out of the enumerated pairing: <R, dm> = dm * Int(W_M R_mu dx);"
    " one scalar row per modulus per cell (7 rows on the moduli block). Cites banked"
    " Slice-2 T0_base_branch_integrated_row; W_M provenance = Stage-3 anchored-weight"
    " premise (P1 per-slot weights SUPPLIED; P2 a_M=0).",
)

# [2] SUBSTANTIVE: separation witness — an alphabet-legal density whose integrated
# row vanishes for EVERY weight of the anchored family while the density is
# pointwise nonzero. Configuration p0 = x^2 (even), density = f1 with f = x^2,
# i.e. f1 = 2x (grade-1, trivial K4 character: legal for R_lambda / R_kmod slots;
# with chi prefactors k10*2x^3 etc. the same odd-kill covers the character rows).
p0_even = x**2
Wm = sp.exp(aM * p0_even)
d1 = 2 * x            # f1 of f = x^2
d3 = 2 * x**3         # f0*f1 of f = x^2 (invariant-multiplied forms same parity)
I1 = sp.integrate(Wm * d1, (x, -1, 1))
I3 = sp.integrate(Wm * d3, (x, -1, 1))
I1_P2 = sp.integrate(d1, (x, -1, 1))   # a_M = 0 (P2) leg, exact polynomial
I3_P2 = sp.integrate(d3, (x, -1, 1))
pw = d1.subs(x, sp.Rational(1, 2))
ok2 = (
    sp.simplify(I1) == 0 and sp.simplify(I3) == 0
    and I1_P2 == 0 and I3_P2 == 0 and pw == 1
)
check(
    "TF1_separation_witness_odd_density_all_weights", "substantive", ok2,
    "Int_{-1}^{1} e^{a_M x^2} * (2x) dx = 0 and * (2x^3) dx = 0 EXACTLY at symbolic"
    " nonzero a_M (and at a_M=0 = P2), while the density = 1 != 0 at x=1/2: the"
    " integrated row vanishes on the WHOLE enumerated weight family with the pointwise"
    " row nonzero. Pointwise R_mu = 0 is strictly stronger than the constant-fork"
    " pairing condition.",
)

# [3] SUBSTANTIVE: a declared-class FIELD direction detects the pointwise content the
# constant fork misses. Interior-supported variation v = x(1-x^2)^3 (vanishes with
# v' and v'' at both walls x = +-1 — the Stage-3 TC1_P3 interior-supported class).
v = x * (1 - x**2) ** 3
orders_kill = all(
    sp.simplify(sp.diff(v, x, j).subs(x, s)) == 0
    for j in (0, 1, 2) for s in (1, -1)
)
integrand = sp.expand(d1 * v)                      # = 2 x^2 (1-x^2)^3
fact_ok = sp.simplify(integrand - 2 * x**2 * (1 - x) ** 3 * (1 + x) ** 3) == 0
I_P2 = sp.integrate(integrand, (x, -1, 1))         # exact rational, P2 weight
ok3 = orders_kill and fact_ok and I_P2 > 0
check(
    "TF1_field_direction_detects_pointwise_content", "substantive", ok3,
    "v = x(1-x^2)^3 has v=v'=v''=0 at both walls (interior-supported, banked declared-"
    "class precedent TC1_P3_interior_defect_wall_immune); <R, v> at P2 = Int 2x^2(1-x^2)^3"
    " dx = %s > 0 EXACT; factorization 2x^2(1-x)^3(1+x)^3 (zero residual) gives integrand"
    " >= 0 on the cell, and W_M > 0 (banked T0), so the pairing is nonzero on EVERY"
    " anchored branch (integral positivity, named Category-A — banked Slice-2 precedent)."
    " The SAME density that annihilates all constant directions fails to annihilate a"
    " declared-class field direction." % I_P2,
)

# [4] GUARD: the F-K2 discharge record for the field-fork pointwise reduction.
check(
    "TF1_declared_class_localization_footing", "guard", True,
    "Field-fork pointwise rows derived from banked footing, NOT textbook habit: (a) the"
    " tangent definition POSED sec.1.4 gives delta-m(x) arbitrary in the declared class"
    " on the field fork vs ONE direction per modulus on the constant fork (the load-"
    "bearing distinction is the banked tangent-space dimension); (b) interior-supported"
    " variations are IN the banked declared class (Stage-3 used them: TC1_P3_interior_"
    "defect_wall_immune); (c) W_M invertible/positive (banked T0_weight_invertibility);"
    " (d) the localization closure (continuous g with Int g*v = 0 for all interior-"
    "supported v implies g == 0) is a NAMED Category-A calculus step (continuity + bump"
    " density), same lane as Slice-2's log-monotonicity/integral-positivity citations."
    " No 'fundamental lemma' imported bare.",
)

# [5] SUBSTANTIVE: generated-tuple rows are CENSUS-SLAVED (TC1 H4 machinery reused).
# Banked alphabet carries NO moduli jets (BASE): the field-fork Euler operator in m
# of D = W_F(m) * Ltil(p0, p1, m) is exactly the partial derivative; the constant-
# fork coefficient is its weighted integral. GEN-QUAD instance: d/dlam (e^{2 lam p0}
# L0) = 2 p0 e^{2 lam p0} L0 (the banked lambda-slot / anchored-log structure).
mfun = sp.Function("m")(x)
pfun = sp.Function("p")(x)
Lt = sp.Function("Ltil")(pfun, sp.Derivative(pfun, x), mfun)
aFf = sp.Function("a_F")(mfun)
D5 = sp.exp(aFf * pfun) * Lt
dDdmprime = sp.diff(D5, sp.Derivative(mfun, x))
euler_m = sp.diff(D5, mfun) - sp.diff(dDdmprime, x)
res5a = sp.simplify(euler_m - sp.diff(D5, mfun))
lam = sp.Symbol("lambda", real=True)
p1s, f1s, h1s, p0s = sp.symbols("p1 f1 h1 p0", real=True)
L0 = (p1s**2 + f1s**2 + h1s**2) / 2
res5b = sp.simplify(sp.diff(sp.exp(2 * lam * p0s) * L0, lam) - 2 * p0s * sp.exp(2 * lam * p0s) * L0)
check(
    "TF1_generated_rows_census_slaved", "substantive",
    dDdmprime == 0 and res5a == 0 and res5b == 0,
    "Banked alphabet has no m-jets (BASE): Euler_m(W_F Ltil) = partial_m(W_F Ltil)"
    " exactly (field fork = pointwise density), and the constant fork pairs the SAME"
    " density integrated (check 1). GEN-QUAD lambda-slot instance re-derived:"
    " d/dlam(e^{2 lam p0} L0) = 2 p0 W_F L0 (zero residual; the banked TD2 lambda-row"
    " integrand). The generating functional's variation w.r.t. m REPRODUCES whichever"
    " row form the census status of m dictates — it does not independently force one.",
)

# [6] SUBSTANTIVE: two members with IDENTICAL integrated moduli rows (all 7 slots,
# every anchored weight) that differ pointwise — the constant-fork condition set has
# codimension <= 7 and cannot determine pointwise content.
delta = {"lam": 2 * x, "kmod": 2 * x**3, "k10": 2 * x, "c00": 2 * x**3,
         "c01": 2 * x, "c10": 2 * x**3, "c11": 2 * x}
diffs_int = [sp.simplify(sp.integrate(Wm * d, (x, -1, 1))) for d in delta.values()]
all_int_zero = all(dv == 0 for dv in diffs_int)
some_pw_nonzero = all(d.subs(x, sp.Rational(1, 2)) != 0 for d in delta.values())
check(
    "TF1_two_members_same_integrated_rows_differ_pointwise", "substantive",
    all_int_zero and some_pw_nonzero,
    "R' = R + (odd densities on all 7 moduli slots): every integrated-row difference"
    " Int e^{a_M x^2} * odd dx = 0 EXACTLY at symbolic a_M, yet every slot differs"
    " pointwise at x=1/2. The constant fork supplies EXACTLY 7 scalar conditions per"
    " cell (one per banked tangent direction, POSED sec.1.4); pointwise R_mu = 0 is"
    " an EXTRA condition the pairing does not supply on that fork. (Character legality:"
    " odd factors realized as f1 / f0*f1 alphabet entries times chi-prefactors.)",
)

# ----------------------------------------------------------------------------
# TF2 — the census interrogation (per candidate forcing source)
# ----------------------------------------------------------------------------

# [7] GUARD: the E02 record's own typing (source i).
check(
    "TF2_E02_record_constant_generator_typing", "guard", True,
    "Route B T1(a) scope: presentation orbits computed for CONSTANT generators X"
    " ('Two constant generators X, X-prime present the same anchored family...');"
    " census rows 11-14 fork (ii) verbatim: field lambda(x) means 'the pointwise E02"
    " class is EXTENDED (X no longer a constant generator — a class extension beyond"
    " the banked footing, typed only)'. VERDICT: the banked footing types the moduli"
    " AS CONSTANTS of the registered class; the field branch is a TYPED, UNREGISTERED"
    " extension (BR-M NOT-EXHAUSTED) — not forbidden, not derived. Provenance-grade"
    " asymmetry, not an in-principle prohibition. A2 ADJUDICATION (verifier-"
    "recommended, adopted): the upstream 07-25 registration phrase 'exactly seven"
    " pointwise extension parameters' (udt_founded_phi_complete_coframe_extension_"
    "audit_2026-07-25 AUDIT_REPORT) and the MAP G08 echo ('7 pointwise params') are"
    " AT-A-POINT parameter counts — how many free entries the extension has at a"
    " point — and decide NEITHER census branch (an at-a-point count neither forces"
    " cell-constancy nor x-dependence). The S1 constant-footing verdict rests on"
    " Route B's constant-generator derivations and the census fork wording; the one"
    " banked phrase a field-branch advocate could cite is named and disposed here.",
)

# [8] SUBSTANTIVE: the two-sided twisted cocycle law is the block-lower-triangular
# composition identity itself — member-constancy-independent (source ii).
r1b = sp.Matrix(2, 2, lambda i, j: sp.Symbol("r1_%d%d" % (i, j)))
q1b = sp.Matrix(2, 2, lambda i, j: sp.Symbol("q1_%d%d" % (i, j)))
l1b = sp.Matrix(2, 2, lambda i, j: sp.Symbol("l1_%d%d" % (i, j)))
r2b = sp.Matrix(2, 2, lambda i, j: sp.Symbol("r2_%d%d" % (i, j)))
q2b = sp.Matrix(2, 2, lambda i, j: sp.Symbol("q2_%d%d" % (i, j)))
l2b = sp.Matrix(2, 2, lambda i, j: sp.Symbol("l2_%d%d" % (i, j)))
Z2 = sp.zeros(2, 2)
M1 = sp.Matrix(sp.BlockMatrix([[r1b, Z2], [l1b, q1b]]))
M2 = sp.Matrix(sp.BlockMatrix([[r2b, Z2], [l2b, q2b]]))
prod = M2 * M1
ll = prod[2:4, 0:2]
res8 = sp.simplify(ll - (q2b * l1b + l2b * r1b))
ur = sp.simplify(prod[0:2, 2:4])
check(
    "TF2_blocktriangular_composition_is_twosided_cocycle", "substantive",
    res8 == sp.zeros(2, 2) and ur == sp.zeros(2, 2),
    "For ANY block-lower-triangular transports M_i = [[rho_i,0],[L_i,Q_i]] (constant-"
    "member OR x-dependent-generator solutions of M' = X(phi)M with fixed H — the"
    " zero upper-right block is preserved: U' = H U, U(0)=0 gives U == 0, Picard"
    " Category-A), composition gives L_12 = Q_2 L_1 + L_2 rho_1 IDENTICALLY (zero"
    " residual, generic blocks). The banked T3 law is the composition identity of the"
    " transport class, NOT a constancy property: promotion m -> m(x) cannot break it.",
)

# [9] SUBSTANTIVE: E04 cross-member composition recomputed — the banked law already
# ABSORBS x-dependent effective members (member drift) (source ii).
ph1, ph2 = sp.symbols("phi1 phi2", real=True)
H2 = sp.diag(-1, 1)
hvals = (-1, 1)
C1m = sp.Matrix(2, 2, lambda i, j: sp.Symbol("C1_%d%d" % (i, j)))
C2m = sp.Matrix(2, 2, lambda i, j: sp.Symbol("C2_%d%d" % (i, j)))
I2 = sp.eye(2)


def expH(phi):
    return sp.diag(sp.exp(-phi), sp.exp(phi))


def ME04(phi, C):
    return sp.Matrix(sp.BlockMatrix([[expH(phi), Z2], [C * H2 * (expH(phi) - I2), I2]]))


C3m = sp.Matrix(2, 2, lambda i, j: (
    (C2m[i, j] * (sp.exp(ph2 * hvals[j]) - 1) * sp.exp(ph1 * hvals[j])
     + C1m[i, j] * (sp.exp(ph1 * hvals[j]) - 1))
    / (sp.exp((ph1 + ph2) * hvals[j]) - 1)
))
res9 = sp.simplify(ME04(ph2, C2m) * ME04(ph1, C1m) - ME04(ph1 + ph2, C3m))
# two-sided law instance on E04 (Q = I since K = 0): L12 = L1 + L2 rho1
L1e = C1m * H2 * (expH(ph1) - I2)
L2e = C2m * H2 * (expH(ph2) - I2)
L12e = (ME04(ph2, C2m) * ME04(ph1, C1m))[2:4, 0:2]
res9b = sp.simplify(L12e - (L1e + L2e * expH(ph1)))
# same-member closure: C3 == C1 when C2 == C1
subs_same = {C2m[i, j]: C1m[i, j] for i in range(2) for j in range(2)}
res9c = sp.simplify(C3m.subs(subs_same) - C1m)
# drift: C3 - C1 is NOT identically zero for distinct members (witness entry)
drift_entry = sp.simplify((C3m - C1m)[0, 0])
check(
    "TF2_E04_crossmember_drift_absorbed_by_law", "substantive",
    res9 == sp.zeros(4, 4) and res9b == sp.zeros(2, 2)
    and res9c == sp.zeros(2, 2) and drift_entry != 0,
    "Banked E04 cross-member law recomputed zero-residual: M(phi2;C2)M(phi1;C1) ="
    " M(phi1+phi2;C3) with the banked C3, C3==C1 iff same member, C3 drifts otherwise;"
    " two-sided law L12 = Q2 L1 + L2 rho1 holds on the composite (Q=I on E04). The"
    " composite of distinct constant members IS an x-dependent effective generator,"
    " and the banked transition-data machinery (J07/T3) was DERIVED to absorb exactly"
    " that: the cocycle source PERMITS x-dependence; it does not force constancy.",
)

# [10] SUBSTANTIVE: the mirror-parity lever (source iii) — exact conditional
# structure; the parity assignment itself is SUPPLIED, not banked-derived.
eps = sp.Symbol("epsilon")
a0, a1, a2, a3 = sp.symbols("a0 a1 a2 a3", real=True)
u_poly = a0 + a1 * t + a2 * t**2 + a3 * t**3      # jet of m about the wall
mirror_eq = sp.expand(u_poly - eps * u_poly.subs(t, -t))
coeffs = [mirror_eq.coeff(t, j) for j in range(4)]
# epsilon = -1 (odd): even jets killed -> m(wall) = 0; a constant is its own 0-jet
kill_odd = [sp.simplify(c.subs(eps, -1)) for c in coeffs]
odd_kills_even_jets = (kill_odd[0] == 2 * a0 and kill_odd[2] == 2 * a2
                       and kill_odd[1] == 0 and kill_odd[3] == 0)
const_forced_zero = sp.solve(sp.Eq(2 * a0, 0), a0) == [0]
# epsilon = +1 (even): 0-jet survives (constants unconstrained)
kill_even = [sp.simplify(c.subs(eps, 1)) for c in coeffs]
even_keeps_0jet = (kill_even[0] == 0 and kill_even[2] == 0
                   and kill_even[1] == 2 * a1 and kill_even[3] == 2 * a3)
# the depth mirror does not act inside the class: -X has H-block -H != H
res10H = sp.simplify(-H2 - H2)
H_exit = res10H != sp.zeros(2, 2)
check(
    "TF2_parity_jet_kill_and_constant_lever", "substantive",
    odd_kills_even_jets and const_forced_zero and even_keeps_0jet and H_exit,
    "TC3 parity-jet kill re-derived on the m-jet: m(w+t) = eps*m(w-t) kills jets with"
    " (-1)^j eps = -1. IF a promoted modulus is assigned eps_m = -1: its 0-jet dies at"
    " the wall, so a CONSTANT modulus is forced to 0 (2a0=0) and fields must be odd;"
    " IF eps_m = +1: constants pass, fields must be even. AND: -X has H-block -H != H"
    " (residual -2H != 0), so the depth mirror phi -> -phi is NOT represented inside"
    " the registered class by generator negation — the mirror's action on moduli is"
    " SUPPLIED seal structure (banked derives only eps_phi = -1; f/bh/moduli parities"
    " tagged SUPPLIED). VERDICT: an exact CONDITIONAL lever, not a banked forcing.",
)

# [11] SUBSTANTIVE: K4 acts pointwise on promoted moduli; characters and jet-
# characters extend verbatim (sources iv/v).
c00f, c01f, c10f, c11f, k10f = [sp.Function(n)(x) for n in ("c00", "c01", "c10", "c11", "k10")]
k00f, k11f = [sp.Function(n)(x) for n in ("k00", "k11")]
Cx = sp.Matrix([[c00f, c01f], [c10f, c11f]])
Kx = sp.Matrix([[k00f, 0], [k10f, k11f]])
Xx = sp.Matrix(sp.BlockMatrix([[H2, Z2], [Cx, Kx]]))
g23 = sp.diag(1, 1, -1, -1)
g12 = sp.diag(1, -1, -1, 1)
g13 = sp.diag(1, -1, 1, -1)
conj = lambda g: g * Xx * g.inv()
X23, X12, X13 = conj(g23), conj(g12), conj(g13)
ok_R23 = (sp.simplify(X23[2:4, 0:2] + Cx) == sp.zeros(2, 2)
          and sp.simplify(X23[2:4, 2:4] - Kx) == sp.zeros(2, 2))
ok_R12 = (sp.simplify(X12[3, 2] + k10f) == 0
          and sp.simplify(X12[2, 0] + c00f) == 0 and sp.simplify(X12[3, 1] + c11f) == 0
          and sp.simplify(X12[2, 1] - c01f) == 0 and sp.simplify(X12[3, 0] - c10f) == 0)
ok_R13 = (sp.simplify(X13[3, 2] + k10f) == 0
          and sp.simplify(X13[2, 1] + c01f) == 0 and sp.simplify(X13[3, 0] + c10f) == 0
          and sp.simplify(X13[2, 0] - c00f) == 0 and sp.simplify(X13[3, 1] - c11f) == 0)
# jet characters: d/dx commutes with the (constant-matrix) action
ok_jets = sp.simplify(sp.diff(-c00f, x) + sp.diff(c00f, x)) == 0
# chi_a prefactors transform with the k10 sign under every element (pointwise)
prefactors = [k10f, c00f * c01f, c00f * c10f, c11f * c01f, c11f * c10f]
signs = {"R23": (1, {c00f: -c00f, c01f: -c01f, c10f: -c10f, c11f: -c11f, k10f: k10f}),
         "R12": (-1, {c00f: -c00f, c11f: -c11f, c01f: c01f, c10f: c10f, k10f: -k10f}),
         "R13": (-1, {c01f: -c01f, c10f: -c10f, c00f: c00f, c11f: c11f, k10f: -k10f})}
ok_chars = True
for _gname, (chi_a, sub) in sorted(signs.items()):
    for pref in prefactors:
        if sp.simplify(pref.subs(sub, simultaneous=True) - chi_a * pref) != 0:
            ok_chars = False
check(
    "TF2_K4_pointwise_action_and_jet_characters", "substantive",
    ok_R23 and ok_R12 and ok_R13 and ok_jets and ok_chars,
    "K4 conjugation computed on an x-DEPENDENT generator (Function-valued entries):"
    " the banked signed flips (R23: C -> -C, K fixed; R12: k10,c00,c11 flip; R13:"
    " k10,c01,c10 flip) hold POINTWISE, zero residual; d/dx commutes with the constant-"
    "matrix action so moduli JETS carry the same characters (the Stage-2 BR-M typing"
    " recomputed); all 5 chi_a prefactors transform with the k10 sign under all"
    " elements pointwise. VERDICT: the K4 quotient/character rule PERMITS promotion"
    " unchanged — no forcing either way.",
)

# [12] GUARD: R10/R1 footing (source iv, provenance half).
check(
    "TF2_R10_footing_field_branch_unregistered", "guard", True,
    "R10: the response is DEFINED on the E02 footing (coframe extension selected"
    " FIRST). The census itself stamps the field branch 'a class extension beyond the"
    " banked footing, typed only' and Stage-2 stamps BR-M TYPED-NOT-EXHAUSTED."
    " Therefore at the CURRENT bank the constant branch is the only branch on which"
    " the response object is DERIVED to be defined; entering the field branch requires"
    " a NEW extension registration (a Route-B-analog derivation for x-dependent"
    " generators). PROVENANCE/HONESTY statement only — no merit, no prohibition;"
    " checks 8/9/11 show the computed legs of that extension are form-stable.",
)

# [13] GUARD: J05 (full tangent) and J06 (determined-vs-retained) are fork-neutral.
check(
    "TF2_J05_J06_row_completeness_neutral", "guard", True,
    "J05 verbatim: 'pair action is integrated on every coframe slot' — it forbids"
    " DELETED slots, and both census branches satisfy it (constant fork: all 7 moduli"
    " directions paired by 7 integrated rows; field fork: all delta-m(x) paired by"
    " pointwise rows). J05 does not enlarge the tangent space, hence cannot convert"
    " integrated rows to pointwise. J06's determined-vs-retained branches concern"
    " whether rows DETERMINE moduli, orthogonal to row FORM (banked Slice-2 gate-2"
    " record shows both branches under integrated rows). VERDICT both: PERMITS-BOTH.",
)

# [14] SUBSTANTIVE: the stratum Noether identities DESCEND to the integrated rows
# on the constant fork (one row dependency, exactly as banked TC2 counts) —
# and apply pointwise on the field fork; no fork conversion either way (source viii).
k10c, c00c, c01c, c10c, c11c = sp.symbols("k10 c00 c01 c10 c11", real=True, nonzero=True)
Rc00, Rc01, Rc10, Rc11 = x**2, 1 + x, x**4, sp.Integer(2)   # sample densities
Rkmod = (c10c * Rc00 + c11c * Rc01 - c00c * Rc10 - c01c * Rc11) / k10c  # kmod=0 identity solved
Iw = lambda d: sp.integrate(W_poly * d, (x, -1, 1))
res14a = sp.simplify(-k10c * Iw(Rkmod) + c10c * Iw(Rc00) + c11c * Iw(Rc01)
                     - c00c * Iw(Rc10) - c01c * Iw(Rc11))
# RES-CNEQ0 banked shear-identity example: -c10*R_k10 - k10*R_c10 = 0 on
# {lam-k_mod=-1, c00=c01=0} (cited example; deeper stratification CENSUS-REQUIRED)
Rk10s = -k10c * Rc10 / c10c
res14b = sp.simplify(-c10c * Iw(Rk10s) - k10c * Iw(Rc10))
check(
    "TF2_stratum_identities_descend_to_integrated_rows", "substantive",
    res14a == 0 and res14b == 0,
    "With CONSTANT moduli the coefficients (k10, C) pull out of the weighted integrals,"
    " so the banked pointwise k_mod=0 Noether identity among densities integrates to"
    " EXACTLY the same one linear dependency among the integrated rows (zero residual,"
    " sample densities + symbolic constants) — matching the banked TC2 row-dependency"
    " count; same for the cited RES-CNEQ0 shear-identity example (deeper stratification"
    " CENSUS-REQUIRED upstream, inherited). On the field fork the identities apply"
    " pointwise as banked. VERDICT: stratum structure PERMITS-BOTH — it reshapes row"
    " COUNTING per branch, never the branch itself.",
)

# [15] GUARD: field-branch stratum-crossing obligations (source viii, descent side).
check(
    "TF2_field_branch_stratum_crossing_typed", "guard", True,
    "Under promotion the stratum label becomes x-dependent (e.g. k_mod(x) may vanish"
    " on a locus): the banked k_mod=0 identity then binds ON that locus, a J09-type"
    " continuation/exclusion obligation (banked node-locus precedent TE4_J09). An"
    " obligation TYPE added to the field branch, not a prohibition and not a forcing;"
    " descent/completion forks (L4/J08) are discrete and orthogonal to BR-M. VERDICT:"
    " PERMITS-BOTH with typed extra obligations on the field branch.",
)

# [16] SUBSTANTIVE: restrict-vs-vary correspondence — the census fork IS the
# vary/restrict order question at DOMAIN level; the constant fork = pullback of the
# field-fork one-form to the constant-section submanifold (source ix).
g16 = 1 + x + x**3
pullback = sp.integrate(W_poly * g16 * dm, (x, -1, 1))     # field pairing on delta-m = const
constant_row = dm * sp.integrate(W_poly * g16, (x, -1, 1))  # constant-fork row
res16 = sp.simplify(pullback - constant_row)
check(
    "TF2_restrict_vs_vary_pullback_correspondence", "substantive",
    res16 == 0,
    "The field-fork pairing evaluated on constant directions equals the constant-fork"
    " row EXACTLY (pullback of the one-form to the constant-section submanifold =="
    " the integrated rows), and by checks 2/6 vanishing of the pullback is STRICTLY"
    " weaker than pointwise vanishing: INTEGRATED vs POINTWISE = restrict-then-vary"
    " vs vary-then-restrict of the SAME structure — i.e. the R2 fork is a DOMAIN-"
    "DEFINITION question (what 'the moduli directions of D' ARE), exactly the census"
    " fork. R12 binds moduli STRATA inside the typed domain, not the census fork"
    " itself (the census types both ways at domain level; F-K4 protected).",
)

# [17] SUBSTANTIVE: BR-M-extended typing instance — with moduli JETS present the two
# branch row-sets differ by a wall term even after integrating the pointwise row.
m0, m1c, m2c, m3c = sp.symbols("m0 m1 m2 m3", real=True)
mpoly = m0 + m1c * x + m2c * x**2 + m3c * x**3
Ppoly = sp.Symbol("P0") + sp.Symbol("P1") * x
D17 = sp.diff(mpoly, x) ** 2 / 2 + mpoly * Ppoly       # BR-M-extended sample density
# Euler row in m computed explicitly: E_m(D17) = dD/dm - Dx(dD/dm') = P - m''
field_row = sp.simplify(Ppoly - sp.diff(sp.diff(mpoly, x), x))
int_field_row = sp.integrate(field_row, (x, -1, 1))
const_row17 = sp.integrate(sp.expand(Ppoly), (x, -1, 1))     # Int dD/dm dx (m const: jets absent)
wall_term = (sp.diff(mpoly, x).subs(x, 1) - sp.diff(mpoly, x).subs(x, -1))
res17 = sp.simplify(int_field_row - (const_row17 - wall_term))
check(
    "TF2_mjet_extension_row_difference_wall_term", "substantive",
    res17 == 0,
    "BR-M-EXTENDED typing instance (moduli jets in the density, typed-only upstream):"
    " for D = m'^2/2 + m*P the pointwise row is P - m'' and Int(pointwise row) ="
    " Int(partial_m D) - [m']_walls EXACTLY (zero residual): even the INTEGRAL of the"
    " field-fork row differs from the constant-fork row by a wall term once m-jets"
    " exist — the two branch row-sets are genuinely different objects (P3 wall typing"
    " inherits this). Typing computation only; BR-M stays NOT-EXHAUSTED.",
)

# ----------------------------------------------------------------------------
# ADOPTED verifier strengthenings (amendment pass; credited — original legs in
# VERIFIER_INDEPENDENT_CHECK.py, preserved in-package)
# ----------------------------------------------------------------------------

# [18] SUBSTANTIVE (ADOPTED, credited: verifier V4_two_sided_cocycle_under_promotion):
# a GENUINELY CONTINUOUSLY x-dependent generator — X(t) = [[H,0],[C(t),0]] with
# C(t) = C0 + C1*t (K = 0) — whose transport is built from its Duhamel integral
# L(p) = Int_0^p C(u) expH(u) du; the two-sided cocycle law holds EXACTLY over
# concatenated segments. Stronger S2 grounding than the generic-block + piecewise
# (E04 cross-member) legs alone: a continuous promotion instance, zero residual.
u_var = sp.Symbol("u", real=True)
CA0 = sp.Matrix(2, 2, lambda i, j: sp.Symbol("p%d%d" % (i, j)))
CA1 = sp.Matrix(2, 2, lambda i, j: sp.Symbol("q%d%d" % (i, j)))
LpA = sp.integrate((CA0 + CA1 * u_var) * expH(u_var), (u_var, 0, t))


def fullA(p):
    return sp.Matrix(sp.BlockMatrix([[expH(p), Z2], [LpA.subs(t, p), I2]]))


XtA = sp.Matrix(sp.BlockMatrix([[H2, Z2], [CA0 + CA1 * t, Z2]]))
ode_ok18 = sp.simplify(sp.diff(fullA(t), t) - XtA * fullA(t)) == sp.zeros(4, 4)
T1A = fullA(ph1)
T2A = sp.simplify(fullA(ph1 + ph2) * fullA(ph1).inv())
totA = fullA(ph1 + ph2)
LA_g1 = T1A[2:4, 0:2]
LA_g2 = T2A[2:4, 0:2]
rhoA_g1 = T1A[0:2, 0:2]
QA_g2 = T2A[2:4, 2:4]
cocycle_ok18 = (
    sp.simplify(totA[2:4, 0:2] - (QA_g2 * LA_g1 + LA_g2 * rhoA_g1)) == sp.zeros(2, 2)
    and sp.simplify(QA_g2 - I2) == sp.zeros(2, 2)
)
check(
    "ADOPTED_xdep_duhamel_two_sided_cocycle", "substantive",
    ode_ok18 and cocycle_ok18,
    "ADOPTED from the blind verifier (credited: V4_two_sided_cocycle_under_promotion,"
    " VERIFIER_INDEPENDENT_CHECK.py): X(t) = [[H,0],[C(t),0]] with C(t) = C0 + C1*t"
    " genuinely CONTINUOUSLY x-dependent; the Duhamel transport (L(p) = Int_0^p C(u)"
    " expH(u) du) solves M' = X(t)M EXACTLY (zero residual), and its segment"
    " transports satisfy the two-sided law L(g2.g1) = Q(g2)L(g1) + L(g2)rho(g1)"
    " EXACTLY over concatenated segments. The banked T3/J07 law is composition-"
    "structural: promotion m -> m(x) cannot break it — S2 PERMITS-BOTH now grounded"
    " on a continuous promotion instance, beyond checks 8/9.",
)

# [19] SUBSTANTIVE (ADOPTED, credited: verifier V5_swap_dressing_candidate_computed):
# the Route-P CANDIDATE computation — a conditional input, explicitly NOT banked as
# a parity derivation (the seal-dressing premise is unestablished).
F2s = sp.Matrix([[0, 1], [1, 0]])
Fb = sp.Matrix(sp.BlockMatrix([[F2s, Z2], [Z2, I2]]))
KlA = sp.Matrix([[sp.Symbol("kA00"), 0], [sp.Symbol("kA10"), sp.Symbol("kA11")]])
CgA = sp.Matrix(2, 2, lambda i, j: sp.Symbol("cgA%d%d" % (i, j)))
XgA = sp.Matrix(sp.BlockMatrix([[H2, Z2], [CgA, KlA]]))
XmA = sp.simplify(-(Fb * XgA * Fb.inv()))
eta2 = sp.diag(-1, 1)
swap_ok19 = (
    sp.simplify(XmA[0:2, 0:2] - H2) == Z2
    and sp.simplify(XmA[2:4, 2:4] + KlA) == Z2
    and sp.simplify(XmA[2:4, 0:2] + CgA * F2s) == Z2
    and sp.simplify(F2s.T * eta2 * F2s - eta2) != Z2
)
check(
    "ADOPTED_swap_dressing_parity_candidate", "substantive",
    swap_ok19,
    "VERIFIER-COMPUTED CANDIDATE INPUT for Route P (adopted, credited:"
    " V5_swap_dressing_candidate_computed, VERIFIER_INDEPENDENT_CHECK.py): IF the"
    " seal dressing were the banked non-Lorentz swap F = diag(F2, I2) (F2 ="
    " antidiag(1,1)), then -F X F^-1 IS in the registered class with DERIVED"
    " parities: H-block FIXED (-F2 H F2^-1 = H, zero residual), K -> -K (lambda,"
    " k_mod, k10 all ODD), C -> -C.F2 (zero residual). AND F2^T eta F2 != eta —"
    " F is NOT a Lorentz map, so adopting F as the seal dressing is itself SUPPLIED"
    " seal structure: this check is NOT banked as a parity derivation (the premise"
    " is unestablished); it is recorded on the Route-P entry of"
    " RESIDUAL_DECISION_SURFACE.md as a candidate input only (F-K4 protected).",
)

# ----------------------------------------------------------------------------
# TF3 / TF4 — assembly guards
# ----------------------------------------------------------------------------

check(
    "TF3_composite_verdict_assembly", "guard", True,
    "TF1 verdict: CRUX PROVEN — the enumerated pairing supplies EXACTLY the integrated"
    " rows (7 scalars/cell) on the constant fork and EXACTLY the pointwise rows on the"
    " field fork (declared-class localization); pointwise is strictly stronger (checks"
    " 2/3/6). R2 REDUCES to the census fork (BR-M). TF2 verdict: NO banked source"
    " forces the census fork — E02 record + R10 provenance give FORCES-CONSTANT-ON-"
    "BANKED-FOOTING (field = typed unregistered extension); cocycle/K4/characters/"
    "generated-rows/stratum-identities all form-stable = PERMITS-BOTH; parity = exact"
    " CONDITIONAL lever on supplied eps_m. Composite per sector ((lam,k_mod) trivial-"
    "char; (k10,C) chi-graded; KMOD0/RES-CNEQ0 combos): REDUCED(census: OPEN) with the"
    " stated provenance asymmetry. Stamps: all sectors x {LE,NV} x {GENERIC, KMOD0;"
    " RES-CNEQ0 example-only} x enumerated anchored branches x jet<=2 stationary"
    " presentation x {BASE=constant, BR-M=field} both carried. OUTCOME CLASS OF3.",
)

check(
    "TF4_stakes_map_fact_restatement", "guard", True,
    "MAP FACT (no promotion): by TF1, Slice-2b's INTEGRATED column IS the constant-"
    "moduli census branch and its POINTWISE column IS the field-moduli census reading"
    " on the BASE arena. Banked theorem restated under the reduction: on the"
    " fiberwise-quadratic p-unmixed LE class, P1-side pairings, jet<=2, stationary"
    " presentation, definite sub-class: constant-census survivors = {E0=0} u {I_p=0"
    " massive locus, nonempty}; field-census survivors = {E0=0} = massless under all"
    " four labeled mass branches at the banked no-moduli-jet response alphabet"
    " (§1.2); a registered BR-M response could carry moduli-jet row content (check"
    " 17) and the massless statement would need re-derivation there (A1 clause;"
    " indefinite sub-class: nonconstant E0=0 members exist — banked). The massive/"
    "massless divergence therefore ATTACHES TO THE CENSUS FORK, which is OPEN (TF5"
    " surface). No branch adopted (F-K4).",
)

# ----------------------------------------------------------------------------
# Report
# ----------------------------------------------------------------------------
n_sub = sum(1 for c in CHECKS if c["kind"] == "substantive")
n_grd = sum(1 for c in CHECKS if c["kind"] == "guard")
n_pass = sum(1 for c in CHECKS if c["passed"])
summary = {
    "package": "udt_p4_bookkeeping_forcing_2026-07-29",
    "contract": "PREREGISTRATION.md (frozen before derivation)",
    "checks_total": len(CHECKS),
    "checks_passed": n_pass,
    "substantive": n_sub,
    "guards": n_grd,
    "TF1_verdict": "CRUX PROVEN: R2 reduces to the census fork (constant -> integrated"
                   " rows exactly; field -> pointwise rows exactly; pointwise strictly"
                   " stronger; witnesses exhibited)",
    "TF2_verdict": "census fork NOT forced by any banked source; E02-record/R10 ="
                   " forces-constant-on-banked-footing (field = typed unregistered"
                   " extension); parity = conditional lever (eps_m SUPPLIED);"
                   " cocycle/K4/characters/generated-rows/strata = permits-both",
    "TF3_outcome_class": "OF3 (REDUCED; census OPEN; exact residual freedom to Charles)",
    "checks": CHECKS,
}
with open("bookkeeping_forcing_results.json", "w") as fh:
    json.dump(summary, fh, indent=1, sort_keys=True)
print()
print("TOTAL: %d/%d passed (%d substantive + %d guards); outcome class OF3"
      % (n_pass, len(CHECKS), n_sub, n_grd))
sys.exit(0 if n_pass == len(CHECKS) else 1)
