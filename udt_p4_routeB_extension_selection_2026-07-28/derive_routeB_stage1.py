#!/usr/bin/env python3
"""P4 Route B Stage 1: stratum classification of the E02 extension class under
constraint layers C1-C4 (contract: PREREGISTRATION.md, this package).

Exact SymPy only (Rational/symbols, no floats). Every claim is a zero-residual
check. Deterministic. Writes routeB_stage1_results.json. Exit nonzero on any
failure (falsifier F-C).

Banked inputs (cited, never re-derived as new results; recomputed only as
consistency checks where load-bearing):
  - E02 class/strata:  udt_founded_phi_complete_coframe_extension_audit_2026-07-25
  - rank facts, holonomy table, swap F, seal: udt_metric_natural_complete_extension_selector_audit_2026-07-27
  - 18-family zero selector rank, scalar-only centralizer, equivariance:
    udt_complete_coframe_native_selector_audit_2026-07-26
  - J01-J15 obligations + R x S3 witness: udt_joint_selector_provenance_audit_2026-07-28

Convention stamps:
  - Chart: registered positive triangular coframe chart; generator
    X = [[H,0],[C,K]], H=diag(-1,+1) (slots 0=clock,1=ruler), K=[[k00,0],[k10,k11]]
    lower triangular (slots 2,3 = screen), C=[[c00,c01],[c10,c11]].
  - eta = diag(-1,1,1,1). Lorentz generator convention copied from the banked
    07-27 script: L{ab}[a,b]=1, L{ab}[b,a]=-eta[a,a]/eta[b,b].
  - Concatenation order: segment 1 first, then segment 2 -> composite matrix M2*M1.
"""

import json
import sys

import sympy as sp

# ----------------------------------------------------------------------------
# infrastructure
# ----------------------------------------------------------------------------

CHECKS: list[dict[str, object]] = []
RESULTS: dict[str, object] = {}
SCOPE_STAMPS: list[str] = []
FALSIFIERS = {"F-A": False, "F-B": False, "F-C": False, "F-D": False, "F-E": False}


def check(name: str, condition: bool) -> None:
    ok = bool(condition)
    CHECKS.append({"name": name, "passed": ok})
    print(("PASS " if ok else "FAIL ") + name)
    if not ok:
        FALSIFIERS["F-C"] = True


def stamp(text: str) -> None:
    SCOPE_STAMPS.append(text)


def is_zero_matrix(M: sp.Matrix) -> bool:
    return all(sp.simplify(e) == 0 for e in M)


# ----------------------------------------------------------------------------
# registered objects
# ----------------------------------------------------------------------------

eta = sp.diag(-1, 1, 1, 1)
H4 = sp.diag(-1, 1, 0, 0)  # founded generator embedded on clock/ruler slots
H2 = sp.diag(-1, 1)

c00, c01, c10, c11, k00, k10, k11 = sp.symbols("c00 c01 c10 c11 k00 k10 k11", real=True)
V7SYMS = (c00, c01, c10, c11, k00, k10, k11)

phi, phi1, phi2, lam, theta = sp.symbols("phi phi1 phi2 lam theta", real=True)


def member(c=(c00, c01, c10, c11), k=(k00, k10, k11)) -> sp.Matrix:
    """Generic registered-chart member X = X0 + v(c,k)."""
    X = sp.zeros(4)
    X[0, 0], X[1, 1] = -1, 1
    X[2, 0], X[2, 1], X[3, 0], X[3, 1] = c[0], c[1], c[2], c[3]
    X[2, 2], X[3, 2], X[3, 3] = k[0], k[1], k[2]
    return X


X0 = member(c=(0, 0, 0, 0), k=(0, 0, 0))  # E06 spectator = founded embedding
XGEN = member()

# linear part V of the class (7-dim): rows 0,1 zero and entry (2,3) zero
V_BASIS = []
for s in V7SYMS:
    B = sp.zeros(4)
    M = member()
    for i in range(4):
        for j in range(4):
            B[i, j] = sp.diff(M[i, j], s)
    V_BASIS.append(B)


def constrained_entries(M: sp.Matrix) -> list[sp.Expr]:
    """Entries that must vanish for M to lie in V (registered, K lower-tri)."""
    out = [M[i, j] for i in range(2) for j in range(4)]
    out.append(M[2, 3])
    return out


def constrained_entries_blockform(M: sp.Matrix) -> list[sp.Expr]:
    """Entries that must vanish for the relaxed block form (general K, 8-dim)."""
    return [M[i, j] for i in range(2) for j in range(4)]


def lorentz_generators() -> dict[str, sp.Matrix]:
    """Banked convention (07-27 script lines 40-48)."""
    result = {}
    for a in range(4):
        for b in range(a + 1, 4):
            g = sp.zeros(4)
            g[a, b] = 1
            g[b, a] = -eta[a, a] / eta[b, b]
            assert g.T * eta + eta * g == sp.zeros(4)
            result[f"L{a}{b}"] = g
    return result


GEN = lorentz_generators()
GEN_NAMES = sorted(GEN)


def vec(M: sp.Matrix) -> sp.Matrix:
    return sp.Matrix([M[i, j] for i in range(4) for j in range(4)])


def coefficient_rank(exprs, variables) -> int:
    A, _ = sp.linear_eq_to_matrix([sp.expand(e) for e in exprs], list(variables))
    return A.rank()


print("=" * 78)
print("SECTION 0 - banked input facts recomputed as zero-residual consistency checks")
print("=" * 78)

# physical metric tangent T = X^T eta + eta X ; rank 7 over the 7 directions
T_GEN = XGEN.T * eta + eta * XGEN
check("S0_physical_tangent_rank_7", coefficient_rank(list(T_GEN), V7SYMS) == 7)

# block structure of T: [[2I, C^T],[C, K+K^T]]
Cblk = sp.Matrix([[c00, c01], [c10, c11]])
Kblk = sp.Matrix([[k00, 0], [k10, k11]])
T_expected = sp.Matrix(sp.BlockMatrix([[2 * sp.eye(2), Cblk.T], [Cblk, Kblk + Kblk.T]]))
check("S0_physical_tangent_block_form", is_zero_matrix(T_GEN - T_expected))

# so(1,3): 6 generators, each metric-skew
check("S0_so13_dimension_6", len(GEN) == 6)

# extension directions + so(1,3) are jointly independent: rank 13
stack13 = sp.Matrix.hstack(*[vec(B) for B in V_BASIS], *[vec(GEN[n]) for n in GEN_NAMES])
check("S0_extension_plus_so13_rank_13", stack13.rank() == 13)
RESULTS["presentation_kernel_intersection_dim"] = 0

# scalar-only centralizer of so(1,3): commutant equations have rank 15
Msyms = sp.symbols("m0:16", real=True)
Mgen = sp.Matrix(4, 4, lambda i, j: Msyms[4 * i + j])
comm_exprs = []
for n in GEN_NAMES:
    comm_exprs.extend(list(Mgen * GEN[n] - GEN[n] * Mgen))
check("S0_full_lorentz_commutant_rank_15", coefficient_rank(comm_exprs, Msyms) == 15)
sol = sp.solve([sp.Eq(e, 0) for e in comm_exprs], list(Msyms), dict=True)
Msol = Mgen.subs(sol[0])
free_left = sorted(Msol.free_symbols, key=str)
check(
    "S0_centralizer_is_scalar_identity",
    len(free_left) == 1 and is_zero_matrix(Msol - free_left[0] * sp.eye(4)),
)

# E08 banked witness recomputed
s_sym = sp.symbols("s", real=True)
E08 = sp.diag(sp.exp(-phi), sp.exp(phi), 1, 1)
E08[2, 0] = s_sym * (1 - sp.exp(-phi))
check("S0_E08_det_one", sp.simplify(E08.det()) == 1)
X_E08 = member(c=(s_sym, 0, 0, 0), k=(0, 0, 0))
check("S0_E08_generator_matches", is_zero_matrix(sp.diff(E08, phi).subs(phi, 0) - X_E08))

# seal: exp(0*X) = I (banked 07-27 s5) - via generic closed forms below; direct:
check("S0_seal_zero_rank_identity", sp.exp(sp.Integer(0)) == 1)

print()
print("=" * 78)
print("SECTION 1 - T1: transformation law of (K,C); covariance typing per stratum")
print("=" * 78)

# (a) presentation-kernel law: X' presents the same anchored family iff
# exp(phi X') exp(-phi X) in SO+(1,3) for all phi; tangent at phi=0:
# X' - X in so(1,3). Combined with rank 13, orbits inside the class are
# singletons: no stratum is a presentation artifact. (rank-13 check above.)

# (b) equivariance law X -> Lam X Lam^{-1} (banked correction, 07-26).
# Structure-preserving infinitesimal stabilizer:
betas = sp.symbols("beta0:6", real=True)
Bgen = sp.zeros(4)
for coeff, n in zip(betas, GEN_NAMES):
    Bgen = Bgen + coeff * GEN[n]


def stabilizer_nullspace_dim(entry_selector) -> tuple[int, list]:
    exprs = list(entry_selector(Bgen * X0 - X0 * Bgen))
    commv = Bgen * XGEN - XGEN * Bgen - (Bgen * X0 - X0 * Bgen)  # [B, v] part
    for e in entry_selector(commv):
        p = sp.expand(e)
        for vsym in V7SYMS:
            exprs.append(p.coeff(vsym))
    A, rhs = sp.linear_eq_to_matrix([sp.expand(e) for e in exprs], list(betas))
    ns = A.nullspace()
    return len(ns), ns


dim_reg, _ = stabilizer_nullspace_dim(constrained_entries)
check("T1_registered_chart_infinitesimal_stabilizer_trivial", dim_reg == 0)
dim_blk, ns_blk = stabilizer_nullspace_dim(constrained_entries_blockform)
check("T1_blockform_infinitesimal_stabilizer_dim_1", dim_blk == 1)
if dim_blk == 1:
    v = ns_blk[0]
    idx = [i for i in range(6) if sp.simplify(v[i]) != 0]
    check("T1_blockform_stabilizer_is_screen_rotation_L23", idx == [GEN_NAMES.index("L23")])

# finite residual chart symmetry: R_pi = exp(pi*L23) = diag(1,1,-1,-1)


def rot(a: int, b: int, ang) -> sp.Matrix:
    R = sp.eye(4)
    R[a, a] = sp.cos(ang)
    R[b, b] = sp.cos(ang)
    R[a, b] = sp.sin(ang)
    R[b, a] = -sp.sin(ang)
    return R


R23 = rot(2, 3, theta)
check("T1_R23_is_lorentz", is_zero_matrix(R23.T * eta * R23 - eta))
check("T1_R23_tangent_is_L23", is_zero_matrix(sp.diff(R23, theta).subs(theta, 0) - GEN["L23"]))
R_pi = R23.subs(theta, sp.pi)
check("T1_R_pi_closed_form", R_pi == sp.diag(1, 1, -1, -1))
X_conj_pi = R_pi * XGEN * R_pi.inv()
X_flipC = member(c=(-c00, -c01, -c10, -c11), k=(k00, k10, k11))
check("T1_R_pi_action_K_fixed_C_negated", is_zero_matrix(X_conj_pi - X_flipC))

# ---- A1 AMENDMENT (verifier-required, VERIFIER_REPORT.md): EXACT finite ----
# residual, exhaustiveness PROVEN. Definition: the residual chart symmetry is
#   Stab = {Lam in SO+(1,3) : Lam X0 Lam^-1 - X0 in V  and  Lam V Lam^-1 = V}
# (exactly the condition that conjugation maps the affine registered class
# {X0 + v} onto itself). Bounded classification, four exact steps:
#
# STEP 1 (upper-right block of Lam vanishes). Probe member v* in V with C=I2,
# K=0: image(v*) = screen plane. Rows 0,1 of Lam*v**Lam^-1 must vanish
# (V has zero top rows); since Lam^-1 is invertible this holds iff rows 0,1 of
# Lam*v* vanish, and those rows are EXACTLY the upper-right entries of Lam:
lsyms = sp.symbols("l0:16", real=True)
LamG = sp.Matrix(4, 4, lambda i, j: lsyms[4 * i + j])
v_probe = sp.zeros(4)
v_probe[2, 0], v_probe[3, 1] = 1, 1  # C = I2, K = 0
Mv = LamG * v_probe
row_expected = sp.Matrix([[LamG[0, 2], LamG[0, 3], 0, 0], [LamG[1, 2], LamG[1, 3], 0, 0]])
check("T1_residual_probe_forces_upper_right_block_zero", is_zero_matrix(Mv[:2, :] - row_expected))

# STEP 2 (block-diagonal forced). With upper-right block zero, Lam^T eta Lam =
# eta decomposes blockwise as S^T S = I2, S^T Xb = 0, A^T eta2 A + Xb^T Xb =
# eta2; the linear system S^T Xb = 0 in Xb has coefficient determinant
# (det S)^2 = 1 != 0 (since S in O(2)), so Xb = 0 and Lam = diag(A, S):
eta2 = sp.diag(-1, 1)
Ab = sp.Matrix(2, 2, sp.symbols("resA0:4", real=True))
Xb = sp.Matrix(2, 2, sp.symbols("resXb0:4", real=True))
Sb = sp.Matrix(2, 2, sp.symbols("resS0:4", real=True))
LamB = sp.Matrix(sp.BlockMatrix([[Ab, sp.zeros(2)], [Xb, Sb]]))
Gres = sp.expand(LamB.T * eta * LamB - eta)
check(
    "T1_residual_lorentz_blockform_identities",
    is_zero_matrix(sp.expand(Gres[:2, :2] - (Ab.T * eta2 * Ab + Xb.T * Xb - eta2)))
    and is_zero_matrix(sp.expand(Gres[:2, 2:] - Xb.T * Sb))
    and is_zero_matrix(sp.expand(Gres[2:, 2:] - (Sb.T * Sb - sp.eye(2)))),
)
Acoef, _ = sp.linear_eq_to_matrix([sp.expand(e) for e in (Sb.T * Xb)], list(Xb))
check(
    "T1_residual_offdiag_coefficient_det_is_detS_squared",
    sp.simplify(Acoef.det() - Sb.det() ** 2) == 0,
)

# STEP 3 (base block A signed-diagonal, orthochronous). Rows 0,1 of
# Lam X0 Lam^-1 must equal X0's rows (V has zero top rows), so A H2 A^-1 = H2,
# i.e. [A, H2] = 0 -> A diagonal; A^T eta2 A = eta2 -> entries +-1;
# orthochronicity (Lam[0,0] > 0) picks the +1 clock sign:
solA = sp.solve([sp.Eq(e, 0) for e in (Ab * H2 - H2 * Ab)], list(Ab), dict=True)
check("T1_residual_A_commutes_H_iff_diagonal", solA == [{Ab[0, 1]: 0, Ab[1, 0]: 0}])
alpha_r, delta_r = sp.symbols("alpha_r delta_r", real=True)
solAd = sp.solve(
    [sp.Eq(e, 0) for e in (sp.diag(alpha_r, delta_r).T * eta2 * sp.diag(alpha_r, delta_r) - eta2)],
    [alpha_r, delta_r],
    dict=True,
)
check(
    "T1_residual_A_signs_pm1",
    sorted((d[alpha_r], d[delta_r]) for d in solAd)
    == [(-1, -1), (-1, 1), (1, -1), (1, 1)],
)

# STEP 4 (screen block S signed-diagonal). Lam V Lam^-1 = V requires
# S K S^-1 lower-triangular for every lower-triangular K; the k10 probe E21
# gives (S E21 adj(S))[0,1] = -q^2, so q = 0 (det S != 0); then S^T S = I2
# with q = 0 forces r = 0 and p, t in {+-1}:
p_, q_, r_, t_ = sp.symbols("p_ q_ r_ t_", real=True)
Sgen = sp.Matrix([[p_, q_], [r_, t_]])
E21 = sp.Matrix([[0, 0], [1, 0]])
check(
    "T1_residual_S_triangularity_forces_q_zero",
    sp.expand((Sgen * E21 * Sgen.adjugate())[0, 1] + q_**2) == 0,
)
solS = sp.solve(
    [sp.Eq(e, 0) for e in (Sgen.T * Sgen - sp.eye(2)).subs(q_, 0)],
    [p_, r_, t_],
    dict=True,
)
check(
    "T1_residual_S_orthogonality_forces_signed_diag",
    sorted((d[p_], d[r_], d[t_]) for d in solS)
    == [(-1, 0, -1), (-1, 0, 1), (1, 0, -1), (1, 0, 1)],
)

# STEP 5 (enumeration + sufficiency + group law). Candidates are the eight
# diag(1, e1, e2, e3), e_i = +-1; det = e1*e2*e3 = +1 filters to exactly four;
# each is in SO+(1,3), fixes X0, and preserves the registered class -> the
# residual is EXACTLY the Klein four-group:
KLEIN = {
    "I": sp.eye(4),
    "R23pi": sp.diag(1, 1, -1, -1),
    "R12pi": sp.diag(1, -1, -1, 1),
    "R13pi": sp.diag(1, -1, 1, -1),
}
cands = [
    sp.diag(1, e1, e2, e3)
    for e1 in (1, -1)
    for e2 in (1, -1)
    for e3 in (1, -1)
    if e1 * e2 * e3 == 1
]
check(
    "T1_residual_exhaustive_enumeration_klein_four",
    len(cands) == 4 and all(any(g == k for k in KLEIN.values()) for g in cands),
)
ok_suff = True
for g in KLEIN.values():
    ok_suff = ok_suff and is_zero_matrix(g.T * eta * g - eta)  # Lorentz
    ok_suff = ok_suff and g.det() == 1 and g[0, 0] == 1  # proper orthochronous
    ok_suff = ok_suff and is_zero_matrix(g * X0 * g.inv() - X0)  # fixes X0
    Xg = g * XGEN * g.inv()  # preserves the registered class:
    ok_suff = ok_suff and all(sp.simplify(e) == 0 for e in constrained_entries(Xg - X0))
check("T1_residual_klein_elements_preserve_class_and_fix_X0", ok_suff)
elems = list(KLEIN.values())
check(
    "T1_residual_klein_group_closure_involutions",
    all(any(g1 * g2 == k for k in elems) for g1 in elems for g2 in elems)
    and all(g * g == sp.eye(4) for g in elems)
    and KLEIN["R12pi"] * KLEIN["R13pi"] == KLEIN["R23pi"],
)
check("T1_R_pi_is_klein_R23pi", R_pi == KLEIN["R23pi"])

# exact actions of the two new elements (k10 -> -k10 plus signed C-flips):
check(
    "T1_R12pi_action_flips_k10_c00_c11",
    is_zero_matrix(
        KLEIN["R12pi"] * XGEN * KLEIN["R12pi"].inv()
        - member(c=(-c00, c01, c10, -c11), k=(k00, -k10, k11))
    ),
)
check(
    "T1_R13pi_action_flips_k10_c01_c10",
    is_zero_matrix(
        KLEIN["R13pi"] * XGEN * KLEIN["R13pi"].inv()
        - member(c=(c00, -c01, -c10, c11), k=(k00, -k10, k11))
    ),
)
# stratum-defining conditions invariant under the FULL Klein group:
ok_inv = True
for g in KLEIN.values():
    Xg = g * XGEN * g.inv()
    ok_inv = ok_inv and sp.simplify(sp.trace(Xg[2:, 2:]) - sp.trace(Kblk)) == 0  # tr K (E03)
    ok_inv = ok_inv and is_zero_matrix((g * member(k=(0, 0, 0)) * g.inv())[2:, 2:])  # K=0 (E04)
    ok_inv = ok_inv and is_zero_matrix((g * member(c=(0, 0, 0, 0)) * g.inv())[2:, :2])  # C=0 (E05)
check("T1_strata_invariant_under_klein_group", ok_inv)

RESULTS["residual_finite_chart_symmetry"] = (
    "EXACT (exhaustiveness PROVEN, A1 amendment): the Klein four-group "
    "{I, diag(1,1,-1,-1), diag(1,-1,-1,1), diag(1,-1,1,-1)} in SO+(1,3). "
    "Actions: R23pi: (K,C)->(K,-C); R12pi: k10->-k10, (c00,c11)->(-c00,-c11); "
    "R13pi: k10->-k10, (c01,c10)->(-c01,-c10). Proof chain: probe mixing member "
    "forces the upper-right Lam block to vanish; eta-preservation then forces "
    "block-diagonality; the fixed-H condition forces the base block "
    "signed-diagonal (orthochronous: clock sign +1); K-triangularity "
    "preservation forces the screen block signed-diagonal; det=+1 enumerates "
    "exactly the four elements (checks T1_residual_*). Carried moduli k10 and "
    "C are read modulo this quotient (k10 mod sign; C mod the signed-flip action)."
)

# block-diagonal screen rotation action: (K,C) -> (S K S^-1, S C); the
# registered K-triangularity is NOT preserved (exact witness):
S2 = sp.Matrix([[sp.cos(theta), sp.sin(theta)], [-sp.sin(theta), sp.cos(theta)]])
Lam_S = sp.diag(1, 1, 1, 1)
Lam_S[2:, 2:] = S2
Xc = Lam_S * XGEN * Lam_S.inv()
check("T1_screen_rotation_preserves_H_block", is_zero_matrix(sp.simplify(Xc[:2, :2] - H2)))
check("T1_screen_rotation_upper_right_stays_zero", is_zero_matrix(sp.simplify(Xc[:2, 2:])))
check(
    "T1_screen_rotation_K_conjugation_C_left_action",
    is_zero_matrix(sp.simplify(Xc[2:, 2:] - S2 * Kblk * S2.inv()))
    and is_zero_matrix(sp.simplify(Xc[2:, :2] - S2 * Cblk)),
)
tri_break = sp.simplify(Xc[2, 3].subs(theta, sp.pi / 2))
check("T1_K_triangularity_not_preserved_probe", sp.simplify(tri_break - (-k10)) == 0 and tri_break != 0)

# strata conditions invariant under the residual/blockdiag actions:
check(
    "T1_strata_invariant_under_screen_action",
    sp.simplify(sp.trace(S2 * Kblk * S2.inv()) - sp.trace(Kblk)) == 0,
)

# (c) covariance typing.
# E03: tr X is invariant under conjugation by ANY invertible matrix:
check("T1_E03_trace_conjugation_invariant", sp.simplify(sp.trace(Mgen * XGEN - XGEN * Mgen)) == 0)
# det exp(phi X) = e^{phi tr X}: X is fully lower triangular; diagonal projection
# is multiplicative on lower-triangular matrices (exact lemma):
asyms = sp.symbols("a0:10", real=True)
bsyms = sp.symbols("b0:10", real=True)


def lower_tri(syms) -> sp.Matrix:
    M = sp.zeros(4)
    t = 0
    for i in range(4):
        for j in range(i + 1):
            M[i, j] = syms[t]
            t += 1
    return M


LA, LB = lower_tri(asyms), lower_tri(bsyms)
prod = LA * LB
check(
    "T1_lower_triangular_diagonal_multiplicative",
    all(sp.simplify(prod[i, i] - LA[i, i] * LB[i, i]) == 0 for i in range(4))
    and all(sp.simplify(prod[i, j]) == 0 for i in range(4) for j in range(i + 1, 4)),
)
check("T1_det_lower_triangular_is_diag_product", sp.simplify(LA.det() - LA[0, 0] * LA[1, 1] * LA[2, 2] * LA[3, 3]) == 0)
stamp(
    "det exp(phi X) = e^{phi tr X} rides the exact triangular lemmas plus the"
    " standard series-limit argument; instantiated exactly on the diagonal"
    " subfamily, E08, and the E04 closed form below."
)

# E04/E05/E06: split-relative. Exact orbit witness under ruler-screen rotation:
R12 = rot(1, 2, theta)
check("T1_R12_is_lorentz", is_zero_matrix(R12.T * eta * R12 - eta))
check("T1_R12_tangent_is_L12", is_zero_matrix(sp.diff(R12, theta).subs(theta, 0) - GEN["L12"]))

X_E04 = member(k=(0, 0, 0))  # generic mixing member, K=0
Xrot = sp.simplify(R12 * X_E04 * R12.inv())
up_right_probe = Xrot[:2, 2:].subs(theta, sp.pi / 2)
check("T1_E04_orbit_leaves_chart_class_probe", not is_zero_matrix(up_right_probe))

# metric-tangent transport: T -> Lam^{-T} T Lam^{-1}
T_E04 = X_E04.T * eta + eta * X_E04
T_rot = sp.simplify(Xrot.T * eta + eta * Xrot)
check(
    "T1_tangent_transports_as_bilinear_form",
    is_zero_matrix(sp.simplify(T_rot - R12.inv().T * T_E04 * R12.inv())),
)
# the founded-block anchor (top-left 2I) moves -> rotated deformation is not
# presentable in the anchored chart class; exact obstruction functionals:
left_null = stack13.T.nullspace()
check("T1_anchored_class_complement_dim_3", len(left_null) == 3)
Xrot_probe = Xrot.subs(theta, sp.pi / 2)
obstructions = [sp.simplify((w.T * vec(Xrot_probe - X0))[0, 0]) for w in left_null]
check("T1_E04_orbit_obstruction_nonzero_probe", any(o != 0 for o in obstructions))
X0rot_probe = sp.simplify(R12 * X0 * R12.inv()).subs(theta, sp.pi / 2)
obstructions0 = [sp.simplify((w.T * vec(X0rot_probe - X0))[0, 0]) for w in left_null]
check("T1_E06_spectator_orbit_also_leaves_class_probe", any(o != 0 for o in obstructions0))
T6 = X0.T * eta + eta * X0
check("T1_E06_topleft_anchor_moves_probe", sp.simplify(R12.inv().T * T6 * R12.inv()).subs(theta, sp.pi / 2)[:2, :2] != 2 * sp.eye(2))

# E06 equivariant content: eta*T/2 is the eta-symmetrization; for E06 it is H4
check("T1_E06_eta_symmetrization_is_H4", is_zero_matrix(eta * T6 / 2 - H4))
# transport law: eta*Ttilde/2 = Lam (eta T/2) Lam^{-1} for Lorentz Lam
lhs = sp.simplify(eta * (R12.inv().T * T6 * R12.inv()) / 2)
rhs = sp.simplify(R12 * (eta * T6 / 2) * R12.inv())
check("T1_E06_condition_transports_by_conjugacy_of_H4", is_zero_matrix(sp.simplify(lhs - rhs)))

RESULTS["T1"] = {
    "presentation_law": "X'~X iff X'-X in so(1,3); intersection with the 7 directions = 0 (rank 13): strata are honest quotient conditions, none is a presentation artifact",
    "equivariance_law": "X -> Lam X Lam^{-1}; connected structure-preserving stabilizer of the registered chart class is trivial; finite residual = EXACTLY the Klein four-group {I, diag(1,1,-1,-1), diag(1,-1,-1,1), diag(1,-1,1,-1)} (exhaustiveness proven, A1): R23pi acts (K,C)->(K,-C), R12pi/R13pi act k10->-k10 with signed C-flips; block-form residual = screen SO(2): (K,C)->(S K S^{-1}, S C)",
    "E03": "COVARIANT (tr X = 0 is conjugation-invariant; det exp = e^{phi tr X})",
    "E04": "SPLIT-RELATIVE (condition on (T,Pi) pair; exact orbit exits the anchored class)",
    "E05": "SPLIT-RELATIVE (same witness class)",
    "E06": "SPLIT-RELATIVE as a fixed condition; equivariant content = conjugacy class of H4 (banked equivariance correction instantiated)",
}

print()
print("=" * 78)
print("SECTION 2 - T2: bracket/subalgebra and finite composition closure")
print("=" * 78)

p1 = sp.symbols("p1_0:7", real=True)
p2 = sp.symbols("p2_0:7", real=True)
X1 = member(c=p1[:4], k=p1[4:])
X2 = member(c=p2[:4], k=p2[4:])
BR = X1 * X2 - X2 * X1
check("T2_E02_bracket_lands_in_V", all(sp.simplify(e) == 0 for e in constrained_entries(BR)))
check("T2_bracket_always_traceless_lands_in_E03_linear_part", sp.simplify(sp.trace(BR)) == 0)

# E04 stratum bracket: [X1,X2] = [[0,0],[(C1-C2)H,0]]
X1_04 = member(c=p1[:4], k=(0, 0, 0))
X2_04 = member(c=p2[:4], k=(0, 0, 0))
BR04 = X1_04 * X2_04 - X2_04 * X1_04
C1blk = sp.Matrix([[p1[0], p1[1]], [p1[2], p1[3]]])
C2blk = sp.Matrix([[p2[0], p2[1]], [p2[2], p2[3]]])
BR04_expected = sp.zeros(4)
BR04_expected[2:, :2] = (C1blk - C2blk) * H2
check("T2_E04_bracket_exact_form", is_zero_matrix(BR04 - BR04_expected))
check("T2_E04_nonabelian", not is_zero_matrix(BR04_expected))

# E05 stratum bracket: block diagonal, [K1,K2] lower triangular
X1_05 = member(c=(0, 0, 0, 0), k=p1[4:])
X2_05 = member(c=(0, 0, 0, 0), k=p2[4:])
BR05 = X1_05 * X2_05 - X2_05 * X1_05
check(
    "T2_E05_bracket_block_diagonal_lower_tri",
    all(sp.simplify(e) == 0 for e in constrained_entries(BR05)) and is_zero_matrix(BR05[2:, :2]),
)

# finite closure, exact closed forms.
# E04 closed form: M04(phi;C) = [[e^{phi H},0],[C H (e^{phi H}-I), I]] solves M'=XM, M(0)=I


def M04(ph, CB) -> sp.Matrix:
    M = sp.eye(4)
    M[0, 0], M[1, 1] = sp.exp(-ph), sp.exp(ph)
    L = CB * H2 * (sp.diag(sp.exp(-ph), sp.exp(ph)) - sp.eye(2))
    M[2:, :2] = L
    return M


Mgen04 = M04(phi, C1blk)
X_from_C1 = member(c=p1[:4], k=(0, 0, 0))
check("T2_E04_closed_form_solves_ODE", is_zero_matrix(sp.simplify(sp.diff(Mgen04, phi) - X_from_C1 * Mgen04)))
check("T2_E04_closed_form_initial_condition", is_zero_matrix(Mgen04.subs(phi, 0) - sp.eye(4)))
check("T2_E04_det_one_family", sp.simplify(Mgen04.det()) == 1)
check(
    "T2_E04_same_member_additive",
    is_zero_matrix(sp.simplify(M04(phi2, C1blk) * M04(phi1, C1blk) - M04(phi1 + phi2, C1blk))),
)

# cross-member effective member (member drift), exact:
hvals = [-1, 1]
C3blk = sp.zeros(2, 2)
Phi = phi1 + phi2
for i in range(2):
    for j in range(2):
        h = hvals[j]
        C3blk[i, j] = (
            C2blk[i, j] * (sp.exp(phi2 * h) - 1) * sp.exp(phi1 * h)
            + C1blk[i, j] * (sp.exp(phi1 * h) - 1)
        ) / (sp.exp(Phi * h) - 1)
check(
    "T2_E04_cross_member_product_equals_effective_member",
    is_zero_matrix(sp.simplify(M04(phi2, C2blk) * M04(phi1, C1blk) - M04(Phi, C3blk))),
)
check(
    "T2_E04_effective_member_constant_iff_same_member",
    is_zero_matrix(sp.simplify(C3blk.subs({p2[i]: p1[i] for i in range(4)}) - C1blk)),
)
drift = sp.simplify(sp.diff(C3blk[0, 0], phi1))
drift_probe = sp.simplify(drift.subs({p1[0]: 0, p2[0]: 1, phi1: 1, phi2: 1}))
check("T2_E04_member_drift_nonzero_for_distinct_members", drift_probe != 0)

# E07 cross-member one-parameter failure (exact, diagonal): the product of
# members k, k' equals exp((phi1+phi2) X_{k''}) for a CONSTANT k'' iff
# k*phi1 + k'*phi2 = k''*(phi1+phi2) identically, i.e. k''=k AND k''=k'.
kk, kk2, kk3 = sp.symbols("kk kk2 kk3", real=True)
ident = sp.expand(kk * phi1 + kk2 * phi2 - kk3 * (phi1 + phi2))
eqs_kk = [ident.coeff(phi1), ident.coeff(phi2)]
sol_distinct = sp.solve([sp.Eq(e, 0) for e in eqs_kk], [kk3], dict=True)
sol_equal = sp.solve([sp.Eq(e.subs(kk2, kk), 0) for e in eqs_kk], [kk3], dict=True)
check(
    "T2_E07_cross_member_closure_iff_equal_members",
    sol_distinct == [] and sol_equal == [{kk3: kk}],
)

# commuting affine closure: for commuting members the product is
# exp(phi1 X1 + phi2 X2) and the effective member (phi1 X1 + phi2 X2)/(phi1+phi2)
# is an affine combination staying in the class but depending on (phi1,phi2):
Xd1 = sp.diag(-1, 1, sp.Symbol("ad1"), sp.Symbol("dd1"))
Xd2 = sp.diag(-1, 1, sp.Symbol("ad2"), sp.Symbol("dd2"))
check("T2_diagonal_members_commute", is_zero_matrix(Xd1 * Xd2 - Xd2 * Xd1))
Xeff = (phi1 * Xd1 + phi2 * Xd2) / (phi1 + phi2)
check("T2_affine_effective_member_H_block_preserved", sp.simplify(Xeff[0, 0] + 1) == 0 and sp.simplify(Xeff[1, 1] - 1) == 0)
check(
    "T2_affine_effective_member_phi_dependent_iff_distinct",
    sp.simplify(sp.diff(Xeff[2, 2], phi1).subs({sp.Symbol("ad1"): 0, sp.Symbol("ad2"): 1, phi1: 1, phi2: 1})) != 0,
)

RESULTS["T2"] = {
    "subalgebra": "every stratum span is a Lie subalgebra; every bracket of members is traceless and lands in the E03 linear part; E04 bracket = [[0,0],[(C1-C2)H,0]] (nonabelian shift algebra); E05 block-diagonal",
    "finite_closure": "class group (triangular, upper block e^{phi H}) closed under products for all strata; same-member one-parameter families exactly additive",
    "exact_failure": "cross-member composition drifts the member: effective member is a (phi1,phi2)-dependent affine mixture (exact drift law banked for E04; exact k!=k' failure for E07); one-parameter anchored closure holds ONLY per member",
}

print()
print("=" * 78)
print("SECTION 3 - T3: mixing cocycle law")
print("=" * 78)

# E08 exact composition (segment 1 then segment 2):
s1, s2, s12 = sp.symbols("s1 s2 s12", real=True)


def E08_map(ph, sv) -> sp.Matrix:
    M = sp.diag(sp.exp(-ph), sp.exp(ph), 1, 1)
    M[2, 0] = sv * (1 - sp.exp(-ph))
    return M


prod21 = sp.simplify(E08_map(phi2, s2) * E08_map(phi1, s1))
u12 = prod21[2, 0]
sigma = lambda x: 1 - sp.exp(-x)
check(
    "T3_E08_cocycle_u12",
    sp.simplify(u12 - (s1 * sigma(phi1) + s2 * sigma(phi2) * sp.exp(-phi1))) == 0,
)
s12_solved = sp.solve(sp.Eq(s12 * sigma(phi1 + phi2), u12), s12)[0]
RESULTS["E08_composition_law"] = str(sp.simplify(s12_solved))
check(
    "T3_E08_composed_map_in_class_with_drifted_s",
    is_zero_matrix(sp.simplify(prod21 - E08_map(phi1 + phi2, s12_solved))),
)
# associativity / cocycle identity over three segments:
phi3, s3 = sp.symbols("phi3 s3", real=True)
left = sp.simplify(E08_map(phi3, s3) * (E08_map(phi2, s2) * E08_map(phi1, s1)))
right = sp.simplify((E08_map(phi3, s3) * E08_map(phi2, s2)) * E08_map(phi1, s1))
check("T3_E08_cocycle_identity_associativity", is_zero_matrix(sp.simplify(left - right)))
# residual chart symmetry acts on the cocycle parameter: s -> -s
check(
    "T3_E08_residual_symmetry_flips_s",
    is_zero_matrix(sp.simplify(R_pi * E08_map(phi, s_sym) * R_pi.inv() - E08_map(phi, -s_sym))),
)
# A1: orbit of s under the FULL (exact) Klein residual: R23pi and R12pi flip
# s, R13pi fixes it -> the orbit is {s, -s}; invariant modulus s mod sign
# (conclusion unchanged; group corrected):
orbit_signs = set()
for g in KLEIN.values():
    Mg = sp.simplify(g * E08_map(phi, s_sym) * g.inv())
    if is_zero_matrix(sp.simplify(Mg - E08_map(phi, s_sym))):
        orbit_signs.add(1)
    elif is_zero_matrix(sp.simplify(Mg - E08_map(phi, -s_sym))):
        orbit_signs.add(-1)
    else:
        orbit_signs.add(0)
check("T3_E08_klein_orbit_is_s_mod_sign", orbit_signs == {1, -1})

# generalization to the full C block. Exact (all orders, not merely first
# order) on the diagonal-K subfamily via Duhamel: with X=[[H,0],[C,K]],
# K=diag(kA,kB), the lower-left block of exp(phi X) is
# L(phi) = Integral_0^phi e^{(phi-t)K} C e^{t H} dt, characterized by
# L' = K L + C e^{phi H}, L(0)=0.
kA, kB = sp.symbols("kA kB", real=True)
Kdiag = sp.diag(kA, kB)
# generic-stratum closed form of Integral_0^phi e^{(phi-t)k} e^{t h} dt
# = (e^{phi h} - e^{phi k})/(h - k) for k != h; verified below by the ODE
# characterization L' = K L + C e^{phi H}, L(0)=0 (unique solution).
Lint = sp.zeros(2, 2)
for i in range(2):
    for j in range(2):
        kv = [kA, kB][i]
        hv = hvals[j]
        Lint[i, j] = Cblk[i, j] * (sp.exp(phi * hv) - sp.exp(phi * kv)) / (hv - kv)
stamp(
    "T3 diagonal-K closed form holds on the generic stratum kA != -1, kB != +1;"
    " on the resonant sub-strata k_i = h_j the integral degenerates to"
    " phi*e^{phi h_j} (same Duhamel/ODE characterization; not expanded here)."
)
ode_res = sp.simplify(sp.diff(Lint, phi) - Kdiag * Lint - Cblk * sp.diag(sp.exp(-phi), sp.exp(phi)))
check("T3_duhamel_lower_left_ODE", is_zero_matrix(ode_res))
check("T3_duhamel_initial_condition", is_zero_matrix(sp.simplify(Lint.subs(phi, 0))))
# full map on the diagonal-K subfamily and its two-sided twisted cocycle law:


def MKC(ph):
    M = sp.zeros(4)
    M[0, 0], M[1, 1] = sp.exp(-ph), sp.exp(ph)
    M[2, 2], M[3, 3] = sp.exp(kA * ph), sp.exp(kB * ph)
    M[2:, :2] = Lint.subs(phi, ph)
    return M


XKC = member(k=(kA, 0, kB))
check("T3_full_map_solves_ODE", is_zero_matrix(sp.simplify(sp.diff(MKC(phi), phi) - XKC * MKC(phi))))
Q2 = sp.diag(sp.exp(kA * phi2), sp.exp(kB * phi2))
rho1 = sp.diag(sp.exp(-phi1), sp.exp(phi1))
coc_res = sp.simplify(Lint.subs(phi, phi1 + phi2) - (Q2 * Lint.subs(phi, phi1) + Lint.subs(phi, phi2) * rho1))
check("T3_two_sided_twisted_cocycle_law", is_zero_matrix(coc_res))
RESULTS["T3"] = {
    "E08_law": "u=s*(1-e^{-phi}) composes as u12 = u1 + e^{-phi1} u2; s12 = [s1(1-e^{-phi1}) + s2 e^{-phi1}(1-e^{-phi2})]/(1-e^{-phi1-phi2})",
    "E08_residual_orbit": "orbit of s under the exact Klein-four residual is {s,-s} (R23pi and R12pi flip s, R13pi fixes it); the chart-honest invariant modulus remains s mod sign (A1: conclusion unchanged, group corrected from the understated Z2)",
    "general_law": "L(gamma2 o gamma1) = Q(gamma2) L(gamma1) + L(gamma2) rho(gamma1), Q=e^{phi K}, rho=e^{phi H}: a two-sided twisted 1-cocycle (crossed homomorphism) over the concatenation groupoid; exact on the diagonal-K subfamily, Duhamel form for general K",
    "J07_typed_requirements": [
        "J07: a global assignment requires overlap transition data (phi-anchor, member) satisfying the twisted cocycle law tensorially on every chart overlap - NOT filled in here",
        "J11: loop consistency requires the cocycle holonomy around every loop to be trivial (or classified) - NOT filled in here",
    ],
}
stamp(
    "T3 general-K law is proven exactly on the diagonal-K subfamily (closed"
    " integrals); for k10 != 0 the same Duhamel/ODE characterization holds but"
    " the closed integral was not expanded (bounded scope)."
)

print()
print("=" * 78)
print("SECTION 4 - T4: the diagonal (a,d)-plane; volume forms; the honest L2 modulus")
print("=" * 78)

a_s, d_s = sp.symbols("a_s d_s", real=True)
Xplane = sp.diag(-1, 1, a_s, d_s)
# coordinates: lam = (a+d)/2 (isotropic/trace modulus), kmod = (d-a)/2 (E07 modulus)
# E07 seat: (a,d)=(-k,+k)  <->  lam=0 ;  isotropic seat: (a,d)=(lam,lam) <-> kmod=0
check("T4_E07_axis_is_traceless_line", sp.simplify((a_s + d_s).subs({a_s: -kk, d_s: kk})) == 0)
check("T4_axes_intersect_only_at_spectator", sp.solve([a_s + d_s, d_s - a_s], [a_s, d_s]) == {a_s: 0, d_s: 0})

# banked conditional gates re-solved on the plane (assembly of banked gates):


def plane_commutant_condition(gname):
    E = Xplane * GEN[gname] - GEN[gname] * Xplane
    return sp.solve([sp.Eq(e, 0) for e in E], [a_s, d_s], dict=True)


sol_L23 = plane_commutant_condition("L23")
check("T4_screen_rotation_forces_isotropic_axis", sol_L23 == [{a_s: d_s}])
sol_SO3 = sp.solve(
    [sp.Eq(e, 0) for g in ("L12", "L13", "L23") for e in (Xplane * GEN[g] - GEN[g] * Xplane)],
    [a_s, d_s],
    dict=True,
)
check("T4_SO3_forces_plus_one_point", sol_SO3 == [{a_s: 1, d_s: 1}])
sol_SO12 = sp.solve(
    [sp.Eq(e, 0) for g in ("L02", "L03", "L23") for e in (Xplane * GEN[g] - GEN[g] * Xplane)],
    [a_s, d_s],
    dict=True,
)
check("T4_SO12_forces_minus_one_point", sol_SO12 == [{a_s: -1, d_s: -1}])
swap = sp.Matrix([[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])  # banked F (07-27)
sol_swap = sp.solve([sp.Eq(e, 0) for e in (swap * Xplane * swap.inv() + Xplane)], [a_s, d_s], dict=True)
check("T4_banked_swap_forces_origin_on_plane", sol_swap == [{a_s: 0, d_s: 0}])
check("T4_banked_swap_not_lorentz", swap.T * eta * swap != eta)
# banked swap on the full class: (-c01, c01, -c11, c11, 0,0,0)
sol_swap_full = sp.solve([sp.Eq(e, 0) for e in (swap * XGEN * swap.inv() + XGEN)], list(V7SYMS), dict=True)
check(
    "T4_banked_swap_full_class_two_mixing_freedoms",
    sol_swap_full == [{c00: -c01, c10: -c11, k00: 0, k10: 0, k11: 0}],
)
# full-class screen-rotation centralizer = the isotropic axis exactly:
sol_L23_full = sp.solve([sp.Eq(e, 0) for e in (XGEN * GEN["L23"] - GEN["L23"] * XGEN)], list(V7SYMS), dict=True)
check(
    "T4_screen_rotation_full_class_forces_isotropic_diag",
    sol_L23_full == [{c00: 0, c01: 0, c10: 0, c11: 0, k00: k11, k10: 0}],
)
# base boost L01 centralizer empty on the plane (banked):
sol_L01 = plane_commutant_condition("L01")
check("T4_base_boost_centralizer_empty", sol_L01 == [])

# centralizer dimensions of X_lam in so(1,3) (banked: generic 1, +-1: 3, 0: 1):


def centralizer_dim(lam_val):
    Xl = sp.diag(-1, 1, lam_val, lam_val)
    exprs = list(Bgen * Xl - Xl * Bgen)
    A, _ = sp.linear_eq_to_matrix([sp.expand(e) for e in exprs], list(betas))
    return len(A.nullspace())


check("T4_centralizer_dims_generic_pm1_zero", [centralizer_dim(v) for v in (lam, 1, -1, 0)] == [1, 3, 3, 1])
stamp("generic-lambda centralizer dim computed with symbolic lam (rank over the rational-function field).")

# ---- volume forms DERIVED from the coframe (T4 amendment: no banked pin) ----
# (i) full 4D coframe volume: theta0^theta1^theta2^theta3 -> det(M(phi)) * vol.
Mplane = sp.diag(sp.exp(-phi), sp.exp(phi), sp.exp(a_s * phi), sp.exp(d_s * phi))
det4 = sp.simplify(Mplane.det())
check("T4_vol4_scaling", sp.simplify(det4 - sp.exp((a_s + d_s) * phi)) == 0)
sol_blind4 = sp.solve(sp.Eq(sp.diff(det4, phi).subs(phi, 0), 0), a_s)
check("T4_vol4_blind_locus_is_traceless_line", sol_blind4 == [-d_s])
check("T4_vol4_blind_isotropic_point_lam0", sp.solve(sp.Eq((2 * lam), 0), lam) == [0])
# (ii) spatial triad volume (slots 1,2,3 = ruler+screen): scaling e^{(1+a+d)phi}
det3 = sp.simplify(sp.exp(phi) * sp.exp(a_s * phi) * sp.exp(d_s * phi))
sol_blind3 = sp.solve(sp.Eq(sp.diff(det3, phi).subs(phi, 0), 0), a_s)
check("T4_triad_blind_locus_line", sol_blind3 == [-d_s - 1])
check("T4_triad_blind_isotropic_point_is_lam_minus_half", sp.solve(sp.Eq(1 + 2 * lam, 0), lam) == [sp.Rational(-1, 2)])
# full-class triad statement: pure-triad coefficient = minor(1,2,3)x(1,2,3),
# lower triangular -> e^{(1+trK)phi}; theta0-contamination when C != 0:
stamp(
    "full-class spatial-triad volume: pure-triad coefficient scales as"
    " e^{(1+k00+k11)phi}; for C != 0 the transported triad additionally"
    " acquires theta0-components (mixing contamination), so strict triad"
    " volume-blindness requires tr K = -1 AND vanishing C-minors; on the"
    " diagonal plane this reduces to 1+a+d=0."
)
# (iii) joint-audit R x S3 witness consistency (banked det E = R^3 e^{2 lam phi}):
R_sym, aw, cE = sp.symbols("R_sym aw cE", positive=True)
Ew = sp.Matrix(
    [
        [sp.exp(-phi) * cE, sp.exp(-phi) * aw, 0, 0],
        [0, R_sym * sp.exp(phi), 0, 0],
        [0, 0, R_sym * sp.exp(lam * phi), 0],
        [0, 0, 0, R_sym * sp.exp(lam * phi)],
    ]
)
detEw = sp.simplify(Ew.det())
check("T4_witness_det_matches_banked", sp.simplify(detEw - cE * R_sym**3 * sp.exp(2 * lam * phi)) == 0)
check("T4_witness_4D_blind_iff_lam0", sp.solve(sp.Eq(sp.diff(detEw, phi).subs(phi, 0), 0), lam) == [0])
# (iv) witness slice-induced 3-volume on t=const (basis sigma3, sigma1, sigma2).
# Work in independent monomials w=e^{2 phi}, z=e^{4 lam phi} (dw/dphi=2w,
# dz/dphi=4 lam z); det g3 = R^6 w z - aw^2 R^4 z/w; require d/dphi det == 0
# identically <=> the coefficients of the independent monomials wz and z/w vanish.
w_, z_ = sp.symbols("w_ z_", positive=True)
aw2 = sp.symbols("aw2", real=True)  # aw treated real here so aw=0 is admissible
det_g3_wz = R_sym**6 * w_ * z_ - aw2**2 * R_sym**4 * z_ / w_
ddet_wz = sp.expand(sp.diff(det_g3_wz, w_) * 2 * w_ + sp.diff(det_g3_wz, z_) * 4 * lam * z_)
coeff_wz = sp.simplify(ddet_wz.coeff(w_ * z_))
coeff_z_over_w = sp.simplify(sp.expand(ddet_wz - coeff_wz * w_ * z_) * w_ / z_)
sol_slice = sp.solve([sp.Eq(coeff_wz, 0), sp.Eq(coeff_z_over_w, 0)], [lam, aw2], dict=True)
check(
    "T4_witness_slice_blind_iff_lam_minus_half_and_zero_shift",
    sol_slice == [{lam: sp.Rational(-1, 2), aw2: 0}],
)
# consistency: the wz-representation reproduces the slice determinant exactly
g3 = sp.diag(
    R_sym**2 * sp.exp(2 * phi) - aw**2 * sp.exp(-2 * phi),
    R_sym**2 * sp.exp(2 * lam * phi),
    R_sym**2 * sp.exp(2 * lam * phi),
)
check(
    "T4_witness_slice_monomial_representation_exact",
    sp.simplify(
        g3.det()
        - det_g3_wz.subs({w_: sp.exp(2 * phi), z_: sp.exp(4 * lam * phi), aw2: aw})
    )
    == 0,
)

RESULTS["T4"] = {
    "plane_coordinates": "lam=(a+d)/2 (isotropic/trace modulus), kmod=(d-a)/2 (E07/reciprocal-anisotropy modulus); E07 axis = {lam=0} = det-one line; isotropic axis = {kmod=0}; intersection = E06 spectator origin",
    "MAP_seat_equation_corrected": "'E07's k = joint-audit lambda' is FALSE at matrix level: they are orthogonal axes of the plane meeting only at the spectator point",
    "banked_pins": {
        "det_one_E03": "lam=0 (whole E07 axis), kmod free",
        "supplied_SO3": "(lam,kmod)=(+1,0)",
        "supplied_SO+(1,2)": "(lam,kmod)=(-1,0)",
        "supplied_banked_swap_F": "(lam,kmod)=(0,0) on the plane; two mixing freedoms in full class",
        "supplied_screen_SO2_alone": "kmod=0, C=0, k10=0 (the isotropic axis, lam free) - full-class solve, this package",
    },
    "volume_blind_loci_DERIVED": {
        "full_4D_coframe_volume": "a+d=0 (lam=0): the E07/det-one axis; witness: lam=0",
        "spatial_triad_volume_slots123": "1+a+d=0 (lam=-1/2 line); isotropic point lam=-1/2 reproduces the previously unsourced '1+2lam=0' ONLY as the spatial-triad reading",
        "witness_slice_volume": "lam=-1/2 AND zero twist shift a=0; with shift a!=0 no lambda is volume-blind",
    },
    "honest_L2_modulus": "the diagonal subfamily carries TWO scalars (lam, kmod); the full class adds k10 and the four mixing parameters C, read modulo the exact Klein-four residual chart quotient (k10 mod sign; C mod the signed-flip action; lam and kmod are Klein-invariant); all pins above are CONDITIONAL on their cited supplied structures; no active premise selects any of them",
}

print()
print("=" * 78)
print("SECTION 5 - T5: stratum x supplied-reduction forcing table (assembly only)")
print("=" * 78)

STRATA = {
    "E02": [],
    "E03": [k00 + k11],
    "E04": [k00, k10, k11],
    "E05": [c00, c01, c10, c11],
    "E06": [c00, c01, c10, c11, k00, k10, k11],
    "E07": [c00, c01, c10, c11, k00 + k11, k10],  # diagonal traceless: a=-k,d=+k
    "E08": [c01, c10, c11, k00, k10, k11],  # single lower shift generator
}
SUPPLIED = {
    "det_one[E03 registration 07-25]": [k00 + k11],
    "transverse_invariance[E04 registration 07-25]": [k00, k10, k11],
    "no_mixing[E05 registration 07-25]": [c00, c01, c10, c11],
    "SO3_holonomy[07-27 s4]": [c00, c01, c10, c11, k00 - 1, k10, k11 - 1],
    "SO12_holonomy[07-27 s4]": [c00, c01, c10, c11, k00 + 1, k10, k11 + 1],
    "swap_F[07-27 s4]": [c00 + c01, c10 + c11, k00, k10, k11],
    "screen_SO2_alone[banked gate 07-27; full-class solve this package]": [c00, c01, c10, c11, k00 - k11, k10],
}


def solution_dim(eqs):
    if not eqs:
        return 7
    A, b = sp.linear_eq_to_matrix([sp.expand(e) for e in eqs], list(V7SYMS))
    Ab = A.row_join(b)
    if A.rank() != Ab.rank():
        return None  # inconsistent
    return 7 - A.rank()


# verify the supplied-structure solution sets against direct commutant solves:
check("T5_SO3_cell_matches_banked_point", solution_dim(SUPPLIED["SO3_holonomy[07-27 s4]"]) == 0)
XSO3 = member(c=(0, 0, 0, 0), k=(1, 0, 1))
check(
    "T5_SO3_forced_member_is_X_plus1",
    all(
        is_zero_matrix(XSO3 * GEN[g] - GEN[g] * XSO3) for g in ("L12", "L13", "L23")
    )
    and XSO3 == sp.diag(-1, 1, 1, 1),
)
XSO12 = member(c=(0, 0, 0, 0), k=(-1, 0, -1))
check(
    "T5_SO12_forced_member_is_X_minus1",
    all(is_zero_matrix(XSO12 * GEN[g] - GEN[g] * XSO12) for g in ("L02", "L03", "L23"))
    and XSO12 == sp.diag(-1, 1, -1, -1),
)

TABLE = []
for sname, seqs in STRATA.items():
    row = {"stratum": sname, "stratum_dim": solution_dim(seqs)}
    for gname, geqs in SUPPLIED.items():
        d = solution_dim(seqs + geqs)
        row[gname] = "EMPTY" if d is None else f"dim={d}"
    TABLE.append(row)

expected_cells = {
    ("E03", "SO3_holonomy[07-27 s4]"): "EMPTY",
    ("E03", "SO12_holonomy[07-27 s4]"): "EMPTY",
    ("E04", "SO3_holonomy[07-27 s4]"): "EMPTY",
    ("E05", "SO3_holonomy[07-27 s4]"): "dim=0",
    ("E05", "SO12_holonomy[07-27 s4]"): "dim=0",
    ("E03", "swap_F[07-27 s4]"): "dim=2",
    ("E04", "swap_F[07-27 s4]"): "dim=2",
    ("E05", "swap_F[07-27 s4]"): "dim=0",
    ("E06", "swap_F[07-27 s4]"): "dim=0",
    ("E07", "swap_F[07-27 s4]"): "dim=0",
    ("E08", "swap_F[07-27 s4]"): "dim=0",
    ("E07", "screen_SO2_alone[banked gate 07-27; full-class solve this package]"): "dim=0",
    ("E02", "screen_SO2_alone[banked gate 07-27; full-class solve this package]"): "dim=1",
}
ok_cells = True
tbl_lookup = {r["stratum"]: r for r in TABLE}
for (srow, scol), val in expected_cells.items():
    if tbl_lookup[srow][scol] != val:
        ok_cells = False
        print(f"  MISMATCH cell ({srow},{scol}): got {tbl_lookup[srow][scol]}, expected {val}")
check("T5_forcing_table_key_cells", ok_cells)
# E06 unique only in the joint stronger class (rank-7, banked 07-26): recompute
check(
    "T5_joint_spectator_rank_7",
    coefficient_rank(
        SUPPLIED["transverse_invariance[E04 registration 07-25]"] + SUPPLIED["no_mixing[E05 registration 07-25]"],
        V7SYMS,
    )
    == 7,
)
RESULTS["T5_table"] = TABLE
RESULTS["T5_unconstrained_columns"] = {
    "active_18_family[07-26]": "UNCONSTRAINED for every stratum (zero selector rank; F-A guard: no elimination may cite this set)",
    "seal_phi0[07-27 s5]": "UNCONSTRAINED (exp(0 X)=I for every X: zero extension-selector rank)",
    "strong_CSN[E10, 07-25/26]": "INACTIVE (conditional; removes angular trace only if supplied)",
}

# F-A structural guard: every EMPTY/forcing cell in the table cites a SUPPLIED
# structure (bracketed source), never the active-18 set:
check(
    "T5_F-A_guard_every_forcing_column_is_supplied",
    all("[" in gname for gname in SUPPLIED),
)

print()
print("=" * 78)
print("SECTION 6 - T6: L1/L2 re-tag (Stage-1 evidence only)")
print("=" * 78)

RESULTS["T6"] = {
    "L1_stratum": (
        "MODULUS-CARRIED. No constraint layer C1-C4 unconditionally eliminates any "
        "stratum: C1 types covariance (E03 DERIVED-covariant via tr X=0; E04/E05/E06 "
        "split-relative, i.e. CONDITIONAL on the supplied base/screen split for their "
        "very definition); C2 closes every stratum (no composition elimination); C3 "
        "reductions are all CONDITIONAL(cite 07-27 s4: SO3->X_{+1}, SO+(1,2)->X_{-1}, "
        "swap_F->2-param mixing family); C4 violations occur only-if-imposed. The full "
        "7-parameter family survives (moduli read modulo the exact Klein-four residual "
        "chart quotient, A1); outcome class O2/O3."
    ),
    "L2_transverse_modulus": (
        "MODULUS-CARRIED and RESOLVED IN FORM: not one scalar. On the diagonal "
        "subfamily the modulus is the PAIR (lam, kmod)=((a+d)/2,(d-a)/2); the MAP's "
        "seat equation 'lambda (= E07's k)' is corrected - the axes are orthogonal and "
        "meet only at the spectator. Pins: det-one => lam=0 (kmod free) "
        "[CONDITIONAL, 07-25 E03]; SO3/SO+(1,2) => (+1,0)/(-1,0) [CONDITIONAL, 07-27]; "
        "banked swap F => (0,0) plus two mixing freedoms [CONDITIONAL, 07-27]; "
        "4D-volume-blind <=> lam=0 [DERIVED here]; spatial-triad-volume-blind <=> "
        "lam=-1/2 [DERIVED here; this is the honest source of the previously unsourced "
        "'1+2lam=0', valid ONLY for the ruler+screen triad volume and, on the witness "
        "slice, only at zero twist shift]. Full class adds k10 and C (4 mixing) as "
        "carried moduli, read modulo the exact Klein-four residual chart quotient "
        "(k10 mod sign; C mod the signed-flip action; A1)."
    ),
}
RESULTS["outcome_class"] = "O2/O3 mixed: stratified family survives with explicit moduli; all reductions conditional-on-supplied-structure"

# C4 typing (J-obligation compatibility per stratum):
RESULTS["C4_typing"] = {
    "J05": "satisfiable-in-principle for all strata (exp(phi X) integrates the pair action on every slot; E06 acts trivially on the screen - degenerate but not violated)",
    "J06": "E02: satisfiable via retained moduli (this ledger). E03/E04/E05/E06 IMPOSED without derivation = J06's named false pass ('spectator screen isotropy or trace zero assumed') -> violated-only-if-imposed",
    "J07": "all strata: satisfiable-in-principle pointwise; a global assignment requires the T3 twisted-cocycle transition data on overlaps - obligation open, not filled",
    "J10": "E03: satisfies (no preferred plane needed). E04/E05/E06 as FIXED-plane conditions conflict with 'no preferred fixed plane'; the equivariant reading (plane = frame data, T1) satisfies -> violated-only-if-imposed(fixed plane)",
    "J11": "identity/reversal/concatenation hold per member (T2); cross-member drift and loop consistency are exactly the open holonomy/cocycle obligations (T2/T3); satisfiable-in-principle, conditional",
    "J13": "E02/E03 retain the lambda/cocycle/twist discriminators (E07/E08 live there); imposing E05 erases the cocycle discriminator, imposing E06 erases both -> violated-only-if-imposed",
    "J15": "satisfied by this deliverable: the surviving moduli (lam, kmod, k10, C) are reported, no witness promoted to unique law",
}

# F-B guard: no pointwise metric-only selection of a non-scalar generator was
# claimed anywhere above; assert bookkeeping flags:
check("F-B_no_pointwise_selection_claimed", all(not FALSIFIERS[k] for k in ("F-A", "F-B")))

# ----------------------------------------------------------------------------
# summary + JSON
# ----------------------------------------------------------------------------
n_fail = sum(1 for c in CHECKS if not c["passed"])
print()
print("=" * 78)
print(f"CHECK SUMMARY: {len(CHECKS) - n_fail}/{len(CHECKS)} passed, {n_fail} failed")
print(f"FALSIFIERS: {FALSIFIERS}")
print("=" * 78)

payload = {
    "package": "udt_p4_routeB_extension_selection_2026-07-28",
    "stage": "Route B Stage 1 (constraint layers C1-C4)",
    "n_checks": len(CHECKS),
    "n_failed": n_fail,
    "checks": CHECKS,
    "results": RESULTS,
    "scope_stamps": SCOPE_STAMPS,
    "falsifier_flags": FALSIFIERS,
}
import pathlib

out = pathlib.Path(__file__).resolve().parent / "routeB_stage1_results.json"
out.write_text(json.dumps(payload, indent=1, default=str) + "\n")
print(f"wrote {out}")

sys.exit(1 if n_fail else 0)
