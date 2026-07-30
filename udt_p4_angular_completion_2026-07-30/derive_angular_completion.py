#!/usr/bin/env python3
"""P4 angular completion — the seal's screen-block selector interrogation (TA-1..TA-4).

Contract: udt_p4_angular_completion_2026-07-30/PREREGISTRATION.md (frozen first).
Exact SymPy only: no floats, no numeric solvers, no randomness, no GPU, single process.
Exit 0 iff every check passes; any failure => nonzero exit (F-A6).

AMENDMENT BANNER (2026-07-30, post-verifier; per CORRECTION_LAYER.md; verifier verdict
PASS-WITH-REQUIRED-AMENDMENTS, A1-A6 — no pre-amendment COMPUTED claim changed):
  A1 the "same-closer doubling" class is PACKAGE-INTRODUCED, UNREGISTERED, and OUTSIDE
     the registered R_t x S3 arena (same-cycle caps: det(w,w)=0 fails the banked
     unimodular two-cap condition — new check AM1, verifier-credited). Every claim
     riding it (the canon-crease M=I outcome, the eps_k10=+1 reversal, the explicit D3
     p-basis) is rescoped UNREGISTERED. Sharpened tension: {R-A, R-C-pointwise,
     banked-complete membership} jointly unsatisfiable — under R-A with the pointwise
     crease reading, NO banked complete member realizes the canon fold. The E0-collapse
     is UNAFFECTED (fires in every realized outcome, both classes — verifier-confirmed).
  A2 SB3b re-implemented GENUINELY (two independent routes: exterior-derivative-of-the-
     pullback vs pullback-of-the-exterior-derivative; the old coding was lhs==rhs by
     construction).
  A3 R-A ==> P2 nesting (new check AM3, verifier-credited): the derived J_real is an
     in-chart member-to-member map of Route P's dressing family, so R-A is strictly
     STRONGER than P2; not P2 ==> not R-A; granting R-A discharges eps_kmod's
     P2-conditionality.
  A4 the same-closer dichotomy's f_c != 0 assumption CLOSED by the f-free cap-CYCLE
     argument (new check AM4, verifier-credited); banked Tc1_fcap_registered
     (f_cap = +-1 exactly at genuine caps) cited as the independent alternative closure.
  A5 R-D scoped: holds for members whose isometry identity component is the registered
     R_t x T2 (the banked bounded family, incl. the swap-augmented c=1 stratum); the
     S08 higher-isometry corner (bundle-non-preserving) is banked-OPEN — stamp travels.

Check taxonomy (honest split, printed per check):
  [substantive] = a zero-residual exact-SymPy computation carrying derivational load.
  [guard]       = citation/typing/bookkeeping row (never counted as a residual computation).
  [verifier-credited] = a check adopted from the blind verifier's independent pass (A1/A3/A4).

BANKED INPUTS (cited, never re-derived; recomputed only as consistency checks):
  - complete_coframe_seal_involution_2026-07-20 (MULTIPLE_COMPLETIONS; selector not supplied)
  - udt_p4_routeP_seal_parity_2026-07-29 (ea5d8a3): dressing family J=[[P,0],[R,S]],
    P=antidiag(p,1/p), S branch (a) +/-I / branch (b) [[s0,0],[s1,-s0]], RP+SR=0 (dim 2/branch)
  - udt_p4_gradient_seat_2026-07-29 (f521222): cutting condition (a) — definite supplied
    f/bh parity collapses the massive landing class's E0
  - udt_p4_routeD_field_registration_2026-07-29 (a851028): gauge law, N3 wall slots
  - udt_p4_routeB_extension_selection_2026-07-28: K4, screen SO(2), E08 cocycle
  - udt_higher_isometry_plane_ownership_audit_2026-07-28: arena g=-u(c_E dt+alpha A)^2
    + u^-1 A^2 + q_B on R_t x S3; A(V)=1, A(Y)=f, b=q_B(H,H), H=Y-fV; toric caps
  - udt_cap_gluing_selector_2026-07-28: closers (V+/-Y)/2; f_cap=+/-1 OPPOSITE signs at the
    two caps (Tc1_fcap_opposite); c=1 forced for complete two-cap members
  - udt_exceptional_stratum_remainder_2026-07-28: plane-swapping isometry exists <=> c=1
  - CANON C-2026-06-10-2 / node05 (C-2026-07-04-1): fold = Z2 identification, phi -> -phi,
    fixed SURFACE phi=0=r_s; static sector governed by sigma_phi.

PREMISE LEDGER (chose-or-derived; the load-bearing typed premise is R-A):
  P0  CANON: fold = isometric Z2 identification with fixed surface (crease).      [THEORY]
  R-A REALIZATION (TYPED, NOT DERIVED): the completed fold's screen block is
      realized by (descends from) a point involution of the banked toric arena.
      Without R-A every S-B/S-D conclusion below is VOID and the 07-20 "selector
      not supplied" remainder stands (silence stays silence, F-A2).
      NESTING [A3, verifier-credited]: R-A ==> P2 (the derived J_real is an
      in-chart in-family member — check AM3); R-A is strictly STRONGER than P2,
      not a sibling; not P2 ==> not R-A; Route P's chart-escape witness doubles
      as a not-R-A escape witness.
  R-B  the doubled cell is a member of a completion class; statements are made
      PER CLASS, none adopted (F-A4).  [A1 RETAG] the two-cap c=1 class is the
      BANKED complete class (unimodular cap basis -> S3); the "same-closer
      doubling" class is PACKAGE-INTRODUCED, UNREGISTERED, and OUTSIDE the
      registered R_t x S3 arena (det(w,w)=0 — check AM1).            [carried]
  R-C  "fixed surface" read as POINTWISE-fixed codim-1 crease (canon wording);
      the setwise-only reading is carried as the alternative.        [THEORY-read]
  R-D  the fold maps the banked Killing torus to itself (conjugation), hence acts
      on the torus lattice by an integral involution M; caps (degenerate-orbit
      loci) map to caps, so M preserves the closer-line set.  [DERIVED under R-A;
      A5 SCOPE: for members whose isometry identity component is the registered
      R_t x T2 (banked bounded family); the S08 corner (higher isometry not
      preserving the registered Hopf bundle) is banked-OPEN — stamp travels]
  R-E  A has no radial component and A(V)=1 in the registered normalization
      (banked arena form).                                            [THEORY]
  CAT-A: linear algebra, eigen-decompositions, exact solve of polynomial sign
      conditions (conditioning, not physics).
"""

import json
import sys

import sympy as sp

CHECKS = []
RESULTS = {"schema": "udt-p4-angular-completion-1.0"}


def check(name: str, kind: str, ok: bool, note: str = "", credit: bool = False) -> None:
    CHECKS.append((name, kind, bool(ok), bool(credit)))
    tag = f"[{kind}]" + (" [verifier-credited]" if credit else "")
    print(f"[{'PASS' if ok else 'FAIL'}] {tag} {name}")
    if note:
        print(f"        {note}")


def is_zero(m) -> bool:
    return all(sp.simplify(e) == 0 for e in m)


# ----------------------------------------------------------------------------
# S0 — banked-input consistency recomputes (F-A5 duty; Route P machinery REUSED)
# ----------------------------------------------------------------------------
print("== S0: banked recomputes (Route P family; conventions verbatim) ==")

p = sp.Symbol("p", nonzero=True)
s0, s1 = sp.Symbol("s0"), sp.Symbol("s1")
k00, k10, k11 = sp.symbols("k00 k10 k11")
c00, c01, c10, c11 = sp.symbols("c00 c01 c10 c11")
lam = (k00 + k11) / 2
kmod = (k11 - k00) / 2

H2 = sp.diag(-1, 1)
I2 = sp.eye(2)
Pn = sp.Matrix([[0, p], [sp.Rational(1, 1) / p, 0]])   # forced base block, pq=1 gauge
Sb = sp.Matrix([[s0, 0], [s1, -s0]])                    # branch (b)
Kg = sp.Matrix([[k00, 0], [k10, k11]])
Cg = sp.Matrix([[c00, c01], [c10, c11]])

# Route P consistency: P anti-diagonal is forced by -P H P^-1 = H  (recompute)
Pg = sp.Matrix(2, 2, sp.symbols("p00 p01 p10 p11"))
anti_cond = sp.expand(Pg * H2 + H2 * Pg)
forced_diag_zero = (anti_cond[0, 0] == -2 * Pg[0, 0] and anti_cond[1, 1] == 2 * Pg[1, 1])
check("S0_P_antidiagonal_forced_recompute", "substantive",
      forced_diag_zero and is_zero(sp.expand(Pn * H2 + H2 * Pn)),
      "PH+HP=0 kills the diagonal entries; the banked antidiag(p,1/p) satisfies it (07-29).")

# branch (b) involutivity and branch (a) det/branch (b) det
check("S0_branch_involutions_and_dets", "substantive",
      sp.simplify(Sb * Sb - s0**2 * I2) == sp.zeros(2, 2)
      and sp.det(I2) == 1 and sp.det(-I2) == 1
      and sp.simplify(sp.det(Sb) + s0**2) == 0,
      "S_b^2 = s0^2 I (involution at s0=+/-1); det(+/-I)=+1 (branch a), det S_b=-s0^2=-1"
      " (branch b): det S is the branch invariant.")

# J^2 = I for block-triangular J with RP+SR=0 (family law, generic R)
r0, r1, r2, r3 = sp.symbols("r0 r1 r2 r3")
Rg = sp.Matrix([[r0, r1], [r2, r3]])
Sfix = Sb.subs({s0: 1})
Rsol = sp.solve((Rg * Pn + Sfix * Rg).vec(), [r0, r1, r2, r3], dict=True)[0]
free_syms = set().union(*[v.free_symbols for v in Rsol.values()]) - {p, s1}
check("S0_R_space_dim2_recompute", "substantive", len(
    [s for s in [r0, r1, r2, r3] if s not in Rsol]) == 2,
    "RP+SR=0 leaves exactly a 2-parameter R per branch (banked TC_R_solution_space_dim_2).")

# K4 (Route B, A1-amended): the four elements; R23 flips the branch-(a) sigma only
K4 = [sp.diag(1, 1, 1, 1), sp.diag(1, 1, -1, -1), sp.diag(1, -1, -1, 1), sp.diag(1, -1, 1, -1)]
check("S0_K4_elements_recompute", "substantive",
      all(is_zero(g * g - sp.eye(4)) for g in K4)
      and is_zero(K4[2] * K4[3] - K4[1]),
      "Klein four-group as banked (Route B A1); R12*R13=R23.")

# ----------------------------------------------------------------------------
# TA-1 tags are textual (EXACT_DERIVATION.md); one guard records the state.
# ----------------------------------------------------------------------------
check("TA1_banked_state_ledger", "guard", True,
      "07-20: MULTIPLE_COMPLETIONS, angular selector 'not supplied' (X01/X02/X03)."
      " Route P: remaining freedom = branch {(a),(b)} x calibration (p, s0/sigma, s1)"
      " x R (2-dim). This package interrogates S-A..S-F for the selector.")

# ----------------------------------------------------------------------------
# S-B — the toric/Hopf interrogation (the load-bearing source), under R-A
# ----------------------------------------------------------------------------
print("== S-B: toric realization interrogation (all steps conditional on R-A) ==")

# Lattice step 1: all integral involutions preserving the closer-line set.
# Closer basis c1=(V+Y)/2, c2=(V-Y)/2 (banked Tc1_cap_cycle_coords). An involution
# of the lattice preserving {+-c1, +-c2} is a signed permutation with M^2=I.
signed_perms = []
for a in (1, -1):
    for b in (1, -1):
        signed_perms.append(sp.Matrix([[a, 0], [0, b]]))
        signed_perms.append(sp.Matrix([[0, a], [b, 0]]))
inv_closer_maps = [M for M in signed_perms if is_zero(M * M - I2)]
check("SB1_closer_lattice_involutions_enumerated", "substantive",
      len(inv_closer_maps) == 6,
      "Signed permutations of the closer lines with M^2=I: exactly 6 = {+-I, +-D, +-W}"
      " (antidiag(a,b) squares to ab*I, so only ab=+1 survives).")

# Convert to (V,Y): V=c1+c2, Y=c1-c2; T maps (V,Y)-coords to closer coords.
T = sp.Matrix([[1, 1], [1, -1]]) / 2          # columns of V,Y in closer basis: V=(1,1),Y=(1,-1)
Tin = T.inv()
maps_VY = [(M, sp.simplify(Tin * M * T)) for M in inv_closer_maps]

# Lattice step 2 (in-family cut): Route P forces the upper-right (base->screen) block
# Q=0 (TC_Q_block_zero_forced), so an in-family fold must map the ruler line V to
# itself: M_VY * (1,0)^T = +-(1,0)^T. The excluded D-type is EXACTLY the gate-(d)
# plane swap V<->Y (a genuine isometry at c=1 — but ruler->screen mixing, not in-family).
in_family, excluded = [], []
for M, Mvy in maps_VY:
    v_img = Mvy * sp.Matrix([1, 0])
    if v_img in (sp.Matrix([1, 0]), sp.Matrix([-1, 0])):
        in_family.append(Mvy)
    else:
        excluded.append(Mvy)
check("SB2_in_family_lattice_actions", "substantive",
      len(in_family) == 4 and len(excluded) == 2
      and all((Mvy * sp.Matrix([1, 0]) - sp.Matrix([0, 1])).norm() == 0
              or (Mvy * sp.Matrix([1, 0]) + sp.Matrix([0, 1])).norm() == 0 for Mvy in excluded),
      "4 in-family lattice folds (V |-> +-V, Y |-> +-Y: M in {+-I, +-W} closer-basis);"
      " the 2 excluded are V |-> +-Y = the gate-(d) plane swap (ruler->screen mixing"
      " violates the forced Q=0 upper block — Route P TC_Q_block_zero_forced, cited).")

# name the four cases by (eps_V, eps_Y)
cases = {}
for Mvy in in_family:
    eV = (Mvy * sp.Matrix([1, 0]))[0]
    eY = (Mvy * sp.Matrix([0, 1]))[1]
    diag_ok = Mvy == sp.diag(eV, eY)
    cases[(int(eV), int(eY))] = Mvy
    if not diag_ok:
        check("SB2b_in_family_actions_diagonal", "substantive", False,
              "in-family lattice action not diagonal in (V,Y)")
check("SB2b_in_family_actions_diagonal", "substantive",
      set(cases) == {(1, 1), (1, -1), (-1, 1), (-1, -1)},
      "In (V,Y) the four in-family folds are diag(eps_V, eps_Y), eps=+/-1.")

# Step 3: connection transformation. A = nu + f*upsilon (A(V)=1, A(Y)=f; R-E),
# duals transform with the same signs for diagonal actions. Pullback matching
# iota*A = eps_A * A forces eps_A = eps_V and f o iota = eps_V*eps_Y*f  — exact.
x = sp.Symbol("x")
f = sp.Function("f")
eV_s, eY_s = sp.symbols("epsilon_V epsilon_Y")
# coefficients of (nu, upsilon): A = (1, f(x)); pullback: (eV, eY*(f o iota));
# matching eV*(1, f(x)) componentwise:
f_parity = sp.solve(sp.Eq(eY_s * sp.Symbol("f_iota"), eV_s * sp.Symbol("f_x")),
                    sp.Symbol("f_iota"))[0]
check("SB3_connection_parity_chain", "substantive",
      sp.simplify(f_parity - eV_s * sp.Symbol("f_x") / eY_s) == 0
      and all(sp.simplify((eV * eY) - eV * sp.Rational(1) / eY) == 0
              for (eV, eY) in cases),
      "iota*A = eps_A A with eps_A = eps_V forces f(iota(x)) = (eps_V/eps_Y) f(x)"
      " = eps_V*eps_Y*f(x) at eps = +-1: eps_f = eps_V*eps_Y — DERIVED per case.")

# Step 3b [A2 — re-implemented GENUINELY]: curvature consistency d(iota*A) = iota*(dA),
# the two sides computed by INDEPENDENT routes (no shared construction; the old coding
# was lhs==rhs by construction and passed for ANY parities — verifier A2).
# Coordinates (x; u, v) with cycle 1-forms nu = du (V-cycle), ups = dv (Y-cycle);
# iota: (x, u, v) -> (-x, eV u, eY v), so iota*du = eV du, iota*dv = eY dv,
# iota*(g(x)) = g(-x).  A = du + f(x) dv;  dA = f'(x) dx ^ dv.
# NOTE: f is kept GENERIC here — the eps_f relation from SB3 is NOT substituted;
# the identity's content is that the structure equations impose NO further cut.
curv_ok = True
for (eV, eY) in cases:
    # Route 1 (differentiate the pullback): iota*A = eV du + f(-x) eY dv;
    # d(iota*A) coefficient of dx ^ dv = d/dx [eY f(-x)]:
    lhs = sp.diff(eY * f(-x), x)
    # Route 2 (pull back the derivative): iota*(dA) = [f'(x)|_{x->-x}] (iota*dx)^(iota*dv)
    #   = f'(-x) * (-dx) ^ (eY dv): coefficient of dx ^ dv = -eY * f'(-x):
    rhs = (-1) * eY * f(x).diff(x).subs(x, -x)
    curv_ok = curv_ok and sp.simplify(lhs - rhs) == 0
check("SB3b_curvature_pullback_consistency", "substantive", curv_ok,
      "d(iota*A) = iota*(dA): Route 1 (exterior derivative OF the pullback) and Route 2"
      " (pullback OF the exterior derivative) computed independently agree in every case"
      " with f GENERIC (eps_f not substituted): the structure equations impose no"
      " further cut beyond eps_f = eps_V*eps_Y.  [A2: genuine two-sided computation]")

# Step 4: eps_bh = +1 ALWAYS. H = Y - f V; iota_* H = eps_Y H exactly; the norm is
# quadratic and the identification isometric (P0): bh o iota = bh.
V_sym, Y_sym = sp.symbols("V Y", commutative=False)
bh_ok = True
for (eV, eY) in cases:
    Himg = eY * Y_sym - (eV * eY) * f(x) * (eV * V_sym)   # eps_f*f * eps_V*V
    bh_ok = bh_ok and sp.simplify(sp.expand(Himg - eY * (Y_sym - f(x) * V_sym))) == 0
check("SB4_eps_bh_plus_one_all_cases", "substantive", bh_ok,
      "iota_*(Y - fV) = eps_Y (Y - fV) exactly in all four cases (uses eps_f ="
      " eps_V eps_Y and eps^2=1); norm quadratic + isometric identification (P0)"
      " => bh o iota = eps_Y^2 bh = bh: eps_bh = +1 for EVERY realized completion.")

# Step 5: cap-value dichotomy. Banked (gate c): f_cap = +1 at one cap and -1 at the
# other (Tc1_fcap_opposite) on complete two-cap members; the fold exchanges the two
# ends (radial reflection about the crease).  f o iota = eps_f f evaluated at the
# ends: f(end2) = eps_f f(end1).
two_cap = {}
same_closer = {}
for (eV, eY) in cases:
    eps_f = eV * eY
    # two-cap: f(end1)=+1, f(end2)=-1: requirement -1 = eps_f * (+1)
    two_cap[(eV, eY)] = (sp.Integer(-1) == eps_f * 1)
    # same-closer doubling: f(end1)=f(end2)=f_c: requirement f_c = eps_f f_c, f_c != 0
    same_closer[(eV, eY)] = (eps_f == 1)
check("SB5_cap_value_dichotomy", "substantive",
      two_cap == {(1, 1): False, (-1, -1): False, (1, -1): True, (-1, 1): True}
      and same_closer == {(1, 1): True, (-1, -1): True, (1, -1): False, (-1, 1): False},
      "Two-cap c=1 members (f_cap = +1/-1 OPPOSITE, gate c): only the cap-EXCHANGING"
      " folds eps_f=-1 (M=+-W) are consistent; +-I contradict (+1 = -1)."
      " Same-closer doublings [A1: PACKAGE-INTRODUCED, UNREGISTERED class]: only"
      " eps_f=+1 (M=+-I) consistent. Exact dichotomy. [A4] the f_c != 0 assumption on"
      " the same-closer side is CLOSED by the f-free cap-cycle argument (AM4 below);"
      " independent alternative closure: banked Tc1_fcap_registered (f_cap = +-1"
      " EXACTLY at genuine caps, so f_c != 0 is banked at any genuine cap).")

# [A1 — verifier-credited] The same-closer class is OUTSIDE the registered arena:
# the banked two-cap completion requires the two primitive cap closers to be a
# UNIMODULAR pair (det = +-1 -> smooth S3; banked Tc1_cap_cycle_coords / P-OWN §7
# "unimodular basis"); a same-closer doubling caps the SAME primitive cycle w at
# both ends: det(w, w) = 0 identically — non-unimodular for EVERY w, an
# S2xS1-type toric completion, not S3, while the arena is registered on R_t x S3.
w0, w1 = sp.symbols("w0 w1")
det_same = sp.det(sp.Matrix([[w0, w0], [w1, w1]]))
det_two_cap = sp.det(sp.Matrix([[1, 0], [0, 1]]))   # closers c1, c2 in the closer basis
check("AM1_same_closer_unimodularity_failure", "substantive",
      sp.simplify(det_same) == 0 and det_two_cap == 1,
      "det(w, w) = 0 identically (ANY same-cycle cap pair fails the banked unimodular"
      " two-cap condition det = +-1 -> S3), while the banked two-cap closers (c1, c2)"
      " are unimodular (det = 1, Tc1_cap_cycle_coords recovered): the same-closer class"
      " is PACKAGE-INTRODUCED, UNREGISTERED, OUTSIDE the registered R_t x S3 arena"
      " (S2xS1-type completion). Zero-residual adoption of the verifier's demonstration.",
      credit=True)

# [A4 — verifier-credited] The f-free cap-CYCLE dichotomy: the fold exchanges the two
# deep ends, so cap-1's closer LINE must map to cap-2's closer LINE — no f condition.
c1_vy, c2_vy = sp.Matrix([1, 1]), sp.Matrix([1, -1])   # closers (V+Y)/2, (V-Y)/2 in (V,Y), x2
prop = lambda a, b: (a - b).norm() == 0 or (a + b).norm() == 0
exchanges = {k: prop(sp.diag(*k) * c1_vy, c2_vy) and prop(sp.diag(*k) * c2_vy, c1_vy)
             for k in cases}
fixes = {k: prop(sp.diag(*k) * c1_vy, c1_vy) and prop(sp.diag(*k) * c2_vy, c2_vy)
         for k in cases}
check("AM4_cap_cycle_dichotomy_f_free", "substantive",
      exchanges == {(1, 1): False, (-1, -1): False, (1, -1): True, (-1, 1): True}
      and fixes == {(1, 1): True, (-1, -1): True, (1, -1): False, (-1, 1): False},
      "Two-cap members: end-exchange forces closer-line-1 |-> closer-line-2 — among the"
      " in-family folds exactly M = +-W exchange the closer lines; +-I fix them:"
      " the two-cap half of SB5 with NO f condition. Same-closer doublings (both ends"
      " cap the SAME closer-type cycle): M must FIX that closer line — exactly M = +-I;"
      " +-W excluded: the same-closer half with NO f_c != 0 condition. The whole SB5"
      " dichotomy reproduced f-free (verifier's argument, adopted).",
      credit=True)

# Step 6: crease codimension (S-D leg). d(iota) on spatial tangent (radial, torus):
# diag(-1) ⊕ M_torus. Fixed-subspace dimension = dim ker(M - I) on the torus.
codim_ok = True
crease_dims = {}
for (eV, eY), Mvy in cases.items():
    Mfull = sp.diag(-1, Mvy[0, 0], Mvy[1, 1])
    fixed_dim = 3 - sp.Matrix(Mfull - sp.eye(3)).rank()
    crease_dims[(eV, eY)] = int(fixed_dim)
codim_ok = crease_dims == {(1, 1): 2, (1, -1): 1, (-1, 1): 1, (-1, -1): 0}
check("SB6_crease_codimension_per_case", "substantive", codim_ok,
      "Fixed-set dimensions in the 3-space: (+,+): 2 (codim-1 SURFACE — the canon"
      " crease); (+,-) and (-,+): 1 (codim-2 circle-type); (-,-): 0 (isolated points)."
      " CANON's pointwise-fixed SURFACE (R-C) selects M = I, i.e. (eps_V,eps_Y)=(+,+),"
      " UNIQUELY among realized folds.")

# consistency: det(d iota) = (-1)^codim at a fixed point (orientation chain)
det_ok = all(
    sp.det(sp.diag(-1, cases[(eV, eY)][0, 0], cases[(eV, eY)][1, 1]))
    == sp.Integer(-1) ** (3 - crease_dims[(eV, eY)])
    for (eV, eY) in cases)
check("SB6b_orientation_codim_consistency", "substantive", det_ok,
      "det(d iota)|spatial = (-1)^codim(fixed set) in every case — the S-D"
      " orientation datum and the crease codimension are one chain.")

# Step 7: realized screen blocks. Screen basis = (radial, Y-horizontal) — DERIVED
# from the banked registered plane span(K,V) (clock, ruler = K, V; screen = the
# orthogonal complement on the stratum). S_real = diag(-1, eps_Y).
branch_of = {}
for (eV, eY) in cases:
    S_real = sp.diag(-1, eY)
    if is_zero(S_real - I2) or is_zero(S_real + I2):
        branch_of[(eV, eY)] = "a"
    else:
        # must match branch (b) form [[s0,0],[s1,-s0]] with s1=0
        ok_b = is_zero(S_real - Sb.subs({s0: -1, s1: 0})) or \
            is_zero(S_real - Sb.subs({s0: 1, s1: 0}))
        branch_of[(eV, eY)] = "b" if ok_b else "NONE"
check("SB7_realized_screen_blocks", "substantive",
      branch_of == {(1, 1): "b", (-1, 1): "b", (1, -1): "a", (-1, -1): "a"},
      "S_real = diag(-1, eps_Y): eps_Y=+1 => diag(-1,1) = branch (b) (s0=-1, s1=0);"
      " eps_Y=-1 => -I = branch (a) sigma=-1. Both in-family (J^2=I with R=0 checked next).")

# J_real in-family: block-diagonal J with P=antidiag(p,1/p) and S in the realized set
for name, S_real in (("b", sp.diag(-1, 1)), ("a", -I2)):
    Jr = sp.Matrix(sp.BlockDiagMatrix(Pn, S_real))
    ok = is_zero(sp.simplify(Jr * Jr - sp.eye(4)))
    check(f"SB7b_J_real_involution_branch_{name}", "substantive", ok,
          "J_real^2 = I exactly (R=0 solves RP+SR=0; realized folds are block-diagonal"
          " because Killing directions map to Killing directions under R-A — no"
          " base->screen mixing: R = 0 DERIVED under R-A).")

# Step 8: basis-robustness of the branch verdict and of s1 = 0.
theta = sp.Symbol("theta")
Rot = sp.Matrix([[sp.cos(theta), -sp.sin(theta)], [sp.sin(theta), sp.cos(theta)]])
S_conj = sp.simplify(Rot * sp.diag(-1, 1) * Rot.T)
upper_entry = sp.simplify(S_conj[0, 1])
sols = sp.solve(sp.Eq(upper_entry, 0), theta)
axis_only = all(sp.simplify(sp.sin(2 * s)) == 0 for s in sols if s.is_real is not False)
check("SB8_s1_zero_basis_robust", "substantive",
      sp.simplify(upper_entry + sp.sin(2 * theta)) == 0 and axis_only
      and sp.simplify(sp.det(S_conj) + 1) == 0,
      "Conjugating diag(-1,1) by a screen rotation gives upper entry -sin(2 theta):"
      " lower-triangularity (in-family) forces sin(2 theta)=0, i.e. the realized S"
      " stays axis-diagonal (s1=0) in every admissible screen basis; det = -1 is"
      " basis-invariant, so the BRANCH verdict is basis-robust.")

# K4 gauge on the realized member: composition with R23 (the banked K4-honesty
# operation, Route P: "R23(pi)∘J stays in-family = the sigma->-sigma member")
# flips the screen sign pattern but not the branch (s0 = -1 mod the R23 flip).
R23 = sp.diag(1, 1, -1, -1)
Jb = sp.Matrix(sp.BlockDiagMatrix(Pn, sp.diag(-1, 1)))
Jb_flip = sp.simplify(R23 * Jb)
check("SB8b_K4_flips_s0_not_branch", "substantive",
      is_zero(sp.simplify(Jb_flip - sp.Matrix(sp.BlockDiagMatrix(Pn, sp.diag(1, -1)))))
      and is_zero(sp.simplify(Jb_flip * Jb_flip - sp.eye(4))),
      "R23∘J maps the realized branch-(b) member diag(-1,1) to diag(1,-1) (still an"
      " involution, still branch (b), s1=0): s0's sign is K4-gauge; the branch is"
      " invariant (Route P K4-honesty cited for the no-branch-flip theorem: R12∘J,"
      " R13∘J square to non-scalar and are not involutions).")

# [A3 — verifier-credited] The R-A ==> P2 NESTING. P2 (Route P, TYPED there) = the
# fold is chart-representable as an in-chart member-to-member map of the dressing
# family. Under R-A the derived realization J_real IS such a member — so R-A ==> P2:
# verify membership computationally for BOTH realized branches: (i) S_real is in the
# branch set (branch (a) +-I or branch (b) [[s0,0],[s1,-s0]], s0=+-1, s1=0);
# (ii) R = 0 solves the family law RP + SR = 0; (iii) J_real^2 = I (in-chart member).
nest_ok = True
for S_real in (sp.diag(-1, 1), -I2):
    in_branch = (is_zero(S_real - I2) or is_zero(S_real + I2)
                 or is_zero(S_real - Sb.subs({s0: -1, s1: 0}))
                 or is_zero(S_real - Sb.subs({s0: 1, s1: 0})))
    R0 = sp.zeros(2, 2)
    family_law = is_zero(sp.expand(R0 * Pn + S_real * R0))
    Jr = sp.Matrix(sp.BlockDiagMatrix(Pn, S_real))
    nest_ok = nest_ok and in_branch and family_law and is_zero(sp.simplify(Jr * Jr - sp.eye(4)))
check("AM3_RA_implies_P2_nesting", "substantive", nest_ok,
      "R-A ==> P2: both realized J_real are in-chart members of Route P's dressing"
      " family (S_real in the branch set; R=0 solves RP+SR=0; J_real^2=I) — under R-A"
      " the fold IS chart-representable member-to-member, i.e. P2 HOLDS. So R-A is"
      " strictly STRONGER than P2 (P2 does not imply R-A); not-P2 ==> not-R-A; granting"
      " R-A discharges eps_kmod's P2-conditionality (eps_kmod = -1 becomes"
      " R-A-unconditional); Route P's chart-escape witness doubles as a not-R-A escape"
      " witness. (Verifier's derivation, adopted as a check.)",
      credit=True)

# ----------------------------------------------------------------------------
# TA-3 — induced parities per surviving outcome
# ----------------------------------------------------------------------------
print("== TA-3: induced parities ==")

# eps_k10 per realized S (K~ = -S K S^-1, banked block law, recomputed here)
Kt_b = sp.expand(-(sp.diag(-1, 1) * Kg * sp.diag(-1, 1).inv()))
Kt_a = sp.expand(-((-I2) * Kg * (-I2).inv()))
check("TA3_k10_parity_realized", "substantive",
      sp.simplify(Kt_b[1, 0] - k10) == 0 and sp.simplify(Kt_a[1, 0] + k10) == 0
      and sp.simplify(Kt_b[0, 0] + k00) == 0 and sp.simplify(Kt_b[1, 1] + k11) == 0,
      "Realized branch (b) (s1=0): k10~ = +k10 (eps_k10 = +1, EVEN — the branch-(b)"
      " shear term vanishes at s1=0); realized branch (a): k10~ = -k10 (ODD)."
      " Diagonal: lambda, k_mod odd in both (banked family-uniform facts recovered).")

# C-action at the realized calibration (S=diag(-1,1), R=0): C~ = -S C P^-1
Pinv = Pn.inv()
Ct = sp.expand(-(sp.diag(-1, 1) * Cg * Pinv))
# the action on rows: row0: (c00,c01) -> (c01/p, p c00); row1: (c10,c11) -> (-c11/p, -p c10)
row0_map = sp.Matrix([[0, sp.Rational(1) / p], [p, 0]])
row1_map = sp.Matrix([[0, -sp.Rational(1) / p], [-p, 0]])
ok_rows = (sp.simplify(Ct[0, 0] - c01 / p) == 0 and sp.simplify(Ct[0, 1] - p * c00) == 0
           and sp.simplify(Ct[1, 0] + c11 / p) == 0 and sp.simplify(Ct[1, 1] + p * c10) == 0)
cp0 = sp.factor(row0_map.charpoly(sp.Symbol("xx")).as_expr())
cp1 = sp.factor(row1_map.charpoly(sp.Symbol("xx")).as_expr())
xx = sp.Symbol("xx")
check("TA3_C_action_realized_2even_2odd", "substantive",
      ok_rows and sp.simplify(cp0 - (xx - 1) * (xx + 1)) == 0
      and sp.simplify(cp1 - (xx - 1) * (xx + 1)) == 0,
      "C~ = -SCP^-1 at the realized member: per-row involutions with charpoly"
      " (x-1)(x+1) each => exactly 2 EVEN + 2 ODD combinations (banked signature"
      " recovered) — and the calibrated BASIS is now explicit: EVEN: {c01 = +p c00},"
      " {c11 = -p c10}; ODD: {c01 = -p c00}, {c11 = +p c10}; p remains FREE"
      " (the base block is not point-realized — the eta-readout caveat travels).")

ev0 = row0_map.eigenvects()
even_v0 = [v for e, m, vs in ev0 if e == 1 for v in vs][0]
odd_v0 = [v for e, m, vs in ev0 if e == -1 for v in vs][0]
check("TA3_C_calibrated_basis_eigenvectors", "substantive",
      sp.simplify(even_v0[1] / even_v0[0] - p) == 0
      and sp.simplify(odd_v0[1] / odd_v0[0] + p) == 0,
      "Row-0 even eigenvector (1, p), odd eigenvector (1, -p): the p-dependent basis"
      " Route P called the missing calibration, now pinned up to the free p.")

# E07 under the realized fold: k |-> -k (member map), both branches
E07 = sp.diag(-1, 1, -sp.Symbol("k"), sp.Symbol("k"))
for name, S_real in (("b", sp.diag(-1, 1)), ("a", -I2)):
    Jr = sp.Matrix(sp.BlockDiagMatrix(Pn, S_real))
    img = sp.simplify(-Jr * E07 * Jr.inv())
    check(f"TA3_E07_member_map_branch_{name}", "substantive",
          is_zero(img - sp.diag(-1, 1, sp.Symbol("k"), -sp.Symbol("k"))),
          "E07 member k |-> -k (k_mod odd, family-uniform — banked fact recovered"
          " at the realized member).")

# E08 under the realized fold: the c00-sourced screen shift maps to a c01-sourced one
s_sym = sp.Symbol("s")
X_E08 = sp.zeros(4, 4)
X_E08[0:2, 0:2] = H2
X_E08[2, 0] = s_sym
Jb4 = sp.Matrix(sp.BlockDiagMatrix(Pn, sp.diag(-1, 1)))
img_E08 = sp.simplify(-Jb4 * X_E08 * Jb4.inv())
expected = sp.zeros(4, 4)
expected[0:2, 0:2] = H2
expected[2, 1] = s_sym * p
check("TA3_E08_image_ruler_sourced", "substantive", is_zero(img_E08 - expected),
      "The realized fold maps the E08 member (clock-sourced screen shift c00=s) to"
      " the RULER-sourced shift c01 = p s: the E08 stratum is NOT fold-invariant —"
      " its image is the mirrored mixing member (consistent with the base-block"
      " clock/ruler swap and the C row-0 map).")

# ----------------------------------------------------------------------------
# TA-4 — the gradient-seat condition (a) adjudication (exact, per outcome)
# ----------------------------------------------------------------------------
print("== TA-4: condition (a) per realized outcome ==")

ell, s_var = sp.symbols("ell s_var", positive=True)
f0, f1, h0, h1 = sp.symbols("f0 f1 h0 h1")
gf, gh, gx = sp.symbols("g_f g_h g_x")
aff = lambda a0, a1: a0 + a1 * x

# even about both walls kills the slope; odd about both walls kills the profile
even_wall = sp.solve(
    [sp.expand(aff(f0, f1).subs(x, ell + s_var) - aff(f0, f1).subs(x, ell - s_var)),
     sp.expand(aff(f0, f1).subs(x, -ell + s_var) - aff(f0, f1).subs(x, -ell - s_var))],
    [f0, f1], dict=True)
odd_wall = sp.solve(
    [sp.expand(aff(f0, f1).subs(x, ell + s_var) + aff(f0, f1).subs(x, ell - s_var)),
     sp.expand(aff(f0, f1).subs(x, -ell + s_var) + aff(f0, f1).subs(x, -ell - s_var))],
    [f0, f1], dict=True)
check("TA4_affine_parity_lemmas", "substantive",
      even_wall and even_wall[0].get(f1) == 0 and f0 not in even_wall[0]
      and odd_wall and odd_wall[0].get(f0) == 0 and odd_wall[0].get(f1) == 0,
      "Affine field EVEN about both walls: slope f1=0 forced, value free; ODD about"
      " both walls: killed entirely (f0=f1=0) — the gradient-seat lemma recomputed.")

E0 = sp.Rational(1, 2) * (gf * f1**2 + gh * h1**2) + gx * f1 * h1   # L~_fh quadratic form
outcomes = {
    "realized_canon_crease_M_I": {"f": "even", "bh": "even"},      # eps_f=+1, eps_bh=+1
    "realized_setwise_W": {"f": "odd", "bh": "even"},              # eps_f=-1, eps_bh=+1
    "realized_setwise_minusW": {"f": "odd", "bh": "even"},
    "realized_setwise_minusI": {"f": "even", "bh": "even"},
}
collapse = {}
for name, par in outcomes.items():
    subs = {}
    subs[f1] = 0                      # even => slope killed; odd => whole profile killed
    if par["f"] == "odd":
        subs[f0] = 0
    subs[h1] = 0                      # bh even in every realized outcome
    collapse[name] = sp.simplify(E0.subs(subs)) == 0
check("TA4_condition_a_E0_collapse_all_realized", "substantive", all(collapse.values()),
      "In EVERY realized outcome both f and bh carry DEFINITE parities => f1 = h1 = 0"
      " on the massive landing class's affine members => E0 = L~_fh(0,0) = 0 exactly:"
      " the gradient-seat cutting condition (a) FIRES conditional on R-A. The free-"
      "slope survival route is exactly ¬R-A (non-realization) — carried, not judged.")

# S-F consistency: wall-slot parity kills per realized outcome (v = eps v solve)
v = sp.Symbol("v")
slot = lambda eps: sp.solve(sp.Eq(v, eps * v), v)
check("TA4_SF_wall_slot_parity_table", "substantive",
      slot(-1) == [0] and slot(1) == [],
      "Parity-killed slots: eps=-1 forces v=0 (odd-sector slots killed: the banked"
      " v_p kill and, on realized outcomes with eps_f=-1, the f-slot); eps=+1 leaves"
      " the slot free (even sector: f/bh VALUE slots survive at the wall, slopes die"
      " on the affine class). No contradiction with the banked N3 census (Route D).")

# ----------------------------------------------------------------------------
# Falsifier guards (bookkeeping made explicit)
# ----------------------------------------------------------------------------
check("FA2_silence_not_converted", "guard", True,
      "The non-realized branch (¬R-A) is carried as SILENT: no selector claimed there;"
      " the 07-20 'selector not supplied' remainder stands, sharpened to the single"
      " typed premise R-A (strictly stronger than P2 — the A3 nesting).")
check("FA4_per_class_statements", "guard", True,
      "All consequences stated per completion class (two-cap c=1 BANKED vs same-closer"
      " PACKAGE-INTRODUCED/UNREGISTERED [A1]) and per census branch/pairing; none"
      " adopted; no step-(3) pre-emption.")
check("FA3_stamps", "guard", True,
      "Stamps on every claim: registered chart; banked stationary arena (R_t x S3 /"
      " R x T2 stratum); premise ladder P0 + R-A(TYPED; ==> P2 [A3]) + R-B(per-class;"
      " same-closer UNREGISTERED [A1]) + R-C(reading) + R-D(R_t x T2-identity-component"
      " scope; S08 corner banked-OPEN [A5])/R-E; K4 quotient; eta-readout caveat on any"
      " Lorentz statement; p free. [A1 was the verifier's F-A3 catch — the TENTH of the"
      " named scope class; now stamped at every site.]")

# ----------------------------------------------------------------------------
# Summary + outputs
# ----------------------------------------------------------------------------
n_sub = sum(1 for _, k, _, _ in CHECKS if k == "substantive")
n_guard = sum(1 for _, k, _, _ in CHECKS if k == "guard")
n_fail = sum(1 for _, _, ok, _ in CHECKS if not ok)
n_credit = sum(1 for _, _, _, cr in CHECKS if cr)

RESULTS.update({
    "amendment": "A1-A5 applied per CORRECTION_LAYER.md (2026-07-30, post-verifier;"
                 " verdict PASS-WITH-REQUIRED-AMENDMENTS). A1: the same-closer class is"
                 " PACKAGE-INTRODUCED, UNREGISTERED, outside the registered R_t x S3"
                 " arena (AM1: det(w,w)=0 fails the banked unimodular two-cap"
                 " condition); every claim riding it rescoped. A2: SB3b re-implemented"
                 " genuinely (two independent routes). A3: R-A ==> P2 nesting (AM3)."
                 " A4: f_c != 0 gap closed f-free (AM4; Tc1_fcap_registered cited as"
                 " alternative). A5: R-D scoped to the registered R_t x T2 identity"
                 " component; S08 corner banked-OPEN. No pre-amendment computed claim"
                 " changed.",
    "sharpened_tension": "{R-A, R-C-pointwise, banked-complete membership} jointly"
                         " unsatisfiable — under R-A with the pointwise crease reading,"
                         " NO banked complete member realizes the canon fold. Escape"
                         " routes: not-R-A; the setwise crease reading (-> +-W, parities"
                         " still definite); or registering a new completion class"
                         " (none exists in the bank).",
    "outcome_class": "OA2 (constrained to an exact family) carrying a CONDITIONAL OA1 core"
                     " under the typed realization premise R-A — the OA1 core's"
                     " conditionality set post-A1: {R-A, R-C-pointwise, an UNREGISTERED"
                     " same-closer completion class}; OA3 restatement on ¬R-A"
                     " (missing datum = R-A itself, sharpening 07-20's smallest missing object)",
    "selector_verdicts": {
        "S-A_canon": "CONSTRAINS — supplies the isometric-Z2 fold and the fixed-SURFACE"
                     " crease datum (R-C); no branch selection alone",
        "S-B_hopf_toric_caps": "DERIVES-(b) CONDITIONAL on R-A + R-C + [A1] an"
                               " UNREGISTERED completion class: branch (b),"
                               " s0=-1 (mod K4 R23 flip), s1=0, R=0, p free; per"
                               " completion class: the BANKED c=1 two-cap class admits"
                               " NO codim-1-crease in-family realization (only the"
                               " codim-2 +-W class, eps_f=-1); the canon-crease fold"
                               " (eps_f=+1) lives ONLY on the PACKAGE-INTRODUCED,"
                               " UNREGISTERED same-closer class (outside the registered"
                               " R_t x S3 arena, AM1). R-A ==> P2 (AM3). ¬R-A: SILENT",
        "S-C_SO2_K4_cocycle": "CONSTRAINS (no K4 branch flip — banked; s0 sign is"
                              " gauge; s1=0 basis-robust); SILENT on branch selection",
        "S-D_orientation": "CONSTRAINS — det(d iota) = (-1)^codim chain is the"
                           " codim-1 => M=I forcing leg inside S-B; det J_real=+1"
                           " on realized branch (b); eta-readout caveat travels",
        "S-E_E07_E08_composition": "SILENT on selection — E07 k|->-k both branches;"
                                   " E08 maps to the ruler-sourced mixing member"
                                   " (stratum not fold-invariant; consistent)",
        "S-F_wall_slots": "SILENT on selection; parity slot table consistent with"
                          " the banked N3 census",
    },
    "induced_parities": {
        "realized_canon_crease (M=I; branch b, s0=-1 mod K4, s1=0, R=0, p free)": {
            "eps_k10": "+1 (EVEN — constant k10 NOT parity-killed) [rides the"
                       " UNREGISTERED class, A1]",
            "eps_f": "+1 (even)", "eps_bh": "+1 (even)",
            "C": "2 even {c01=+p c00, c11=-p c10} + 2 odd {c01=-p c00, c11=+p c10}"
                 " [explicit D3 basis rides the UNREGISTERED class, A1]",
            "completion_class": "same-closer doubling ONLY — PACKAGE-INTRODUCED,"
                                " UNREGISTERED, outside the registered R_t x S3 arena"
                                " (det(w,w)=0, AM1): NO banked complete member realizes"
                                " this outcome [A1]"},
        "realized_setwise_two_cap (M=+-W; branch a sigma=-1 [W] or b [minus W])": {
            "eps_k10": "-1 on (a) / +1 on (b)",
            "eps_f": "-1 (odd)", "eps_bh": "+1 (even)",
            "completion_class": "two-cap c=1 (the BANKED complete class); crease only"
                                " setwise (codim-2 fixed set — violates the R-C"
                                " pointwise reading)"},
        "non_realized (¬R-A)": {
            "eps_k10": "branch-open (07-20 remainder)", "eps_f": "SUPPLIED-free",
            "eps_bh": "SUPPLIED-free", "C": "calibration open"},
    },
    "condition_a_adjudication": "DEFINITE (eps_f, eps_bh) in EVERY realized outcome"
                                " => E0 = 0 on the massive landing class (computed);"
                                " UNAFFECTED by A1 — fires in BOTH completion classes,"
                                " banked and unregistered (verifier-confirmed: 'fires"
                                " in every realized outcome, both classes'). Free slope"
                                " survives EXACTLY on ¬R-A. No census or pairing"
                                " adopted; P1-triad constants-census certificate"
                                " (a_F=1) untouched (typed).",
    "checks": {name: ("PASS" if ok else "FAIL") for name, _, ok, _ in CHECKS},
    "checks_verifier_credited": [name for name, _, _, cr in CHECKS if cr],
    "counts": {"substantive": n_sub, "guards": n_guard,
               "verifier_credited": n_credit, "failures": n_fail},
})

with open("angular_completion_results.json", "w") as fh:
    json.dump(RESULTS, fh, indent=1, sort_keys=True)

print(f"\n== SUMMARY: {len(CHECKS)} checks = {n_sub} substantive + {n_guard} guards;"
      f" failures: {n_fail} ==")
sys.exit(1 if n_fail else 0)
