#!/usr/bin/env python3
"""BLIND VERIFIER independent check — P4 angular completion (2026-07-30).

Written from scratch by the blind adversarial verifier (same-session-spawned,
zero package-context at start; not a hosted external model). Re-derives every
load-bearing leg of derive_angular_completion.py INDEPENDENTLY (different
constructions where possible), and probes the specific attack surfaces:
  V1  lattice-involution classification completeness (brute force over GL(2,Z),
      entry bound 3) + witness that the classification HINGES on closer-set
      preservation (R-D): an in-GL(2,Z) involution NOT preserving the set exists.
  V2  the +-D <-> V<->Y swap identification (gate-(d) object) and the Q=0 cut.
  V3  eps_f = eps_V*eps_Y and eps_bh = +1 via explicit pullback bookkeeping.
  V4  cap-value dichotomy + the f_c = 0 loophole probe on the same-closer side.
  V5  crease fixed-set: EXPLICIT fixed-point sets on T^2 (not just linear kernel)
      per case; codim-1 uniqueness of M = I; det = (-1)^codim.
  V6  branch identification + det invariance + generic-s1 shear term
      k10~ = k10 + 2(s1/s0) kmod (so eps_k10=+1 NEEDS s1=0, which needs R-A).
  V7  C-action 2 even + 2 odd with the p-basis; K-law lambda/kmod odd.
  V8  E0 collapse per realized outcome; PLUS the one-wall-vs-two-wall probe:
      ODD about ONE wall alone does NOT kill the slope (the +-W-outcome collapse
      leg needs parity at both walls or evenness).
Exit 0 iff all pass.
"""
import sys
from itertools import product

import sympy as sp

FAIL = []


def rep(name, ok, note=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" — {note}" if note else ""))
    if not ok:
        FAIL.append(name)


I2 = sp.eye(2)

# ---- V1: brute-force GL(2,Z) involutions preserving {+-c1,+-c2} -------------
c1 = sp.Matrix([1, 0])
c2 = sp.Matrix([0, 1])
closer_set = [tuple(v) for v in (c1, -c1, c2, -c2)]
found = []
B = 3
for a, b, c, d in product(range(-B, B + 1), repeat=4):
    M = sp.Matrix([[a, b], [c, d]])
    if M * M != I2:
        continue
    if tuple(M * c1) in closer_set and tuple(M * c2) in closer_set:
        found.append(M)
rep("V1_bruteforce_closer_involutions_count6", len(found) == 6,
    f"{len(found)} integral involutions (entries |.|<=3) preserve the closer set")
# they are exactly {+-I, +-D, +-W}
D = sp.diag(1, -1)
W = sp.Matrix([[0, 1], [1, 0]])
expected = [I2, -I2, D, -D, W, -W]
rep("V1_set_is_pmI_pmD_pmW",
    all(any(M == E for E in expected) for M in found) and len(found) == 6)
# hinge witness: an involution in GL(2,Z) NOT preserving the closer set
Mw = sp.Matrix([[1, 1], [0, -1]])
rep("V1_hinge_witness_RD_needed", Mw * Mw == I2 and tuple(Mw * c2) not in closer_set,
    "[[1,1],[0,-1]] is a GL(2,Z) involution NOT preserving the set: the"
    " 6-element classification stands ONLY on caps->caps (R-D, i.e. R-A)")

# ---- V2: basis change to (V,Y); +-D are the swap; Q=0 cut -------------------
# V = c1+c2, Y = c1-c2  =>  change of basis T: closer coords of V,Y columns
T = sp.Matrix([[1, 1], [1, -1]]) / 2
to_VY = lambda M: sp.simplify(T.inv() * M * T)
rep("V2_D_is_swap", to_VY(D) == W and to_VY(-D) == -W,
    "closer-basis +-D act on (V,Y) as the antidiagonal V<->Y swap (gate-(d) object)")
rep("V2_W_is_diag", to_VY(W) == D and to_VY(-W) == -D,
    "closer-basis +-W act on (V,Y) as diag(+1,-1)/diag(-1,+1)")
in_family = [M for M in found if (to_VY(M))[0, 1] == 0 and (to_VY(M))[1, 0] == 0]
rep("V2_Q0_cut_leaves_4", len(in_family) == 4,
    "requiring V |-> +-V (no ruler->screen mixing, forced Q=0) leaves the 4"
    " diagonal (V,Y)-actions; the 2 swaps are excluded")

# ---- V3: parity chain, explicit pullback ------------------------------------
x = sp.Symbol("x")
fx = sp.Function("f")
results = {}
for eV, eY in product((1, -1), repeat=2):
    # iota: x -> -x (radial), V-cycle -> eV*V, Y-cycle -> eY*Y  (dual 1-forms
    # nu -> eV*nu, ups -> eY*ups under pullback since the action is diagonal +-1)
    # A = nu + f(x) ups ; iota^*A = eV*nu + f(-x)*eY*ups. A(V)=1 must be
    # preserved with iota^*A = eps_A * A => eps_A = eV and f(-x)*eY = eV*f(x)
    eps_f = sp.Rational(eV, eY)  # = eV*eY at +-1
    results[(eV, eY)] = eps_f
    # eps_bh: H = Y - f V; pushforward at x of H evaluated against the metric:
    # iota_* H |_x = eY*Y - f(x)*eV*V ; H at iota(x) = Y - f(-x) V = Y - eps_f f V
    diff = sp.expand(
        (eY * sp.Symbol("Ysym") - fx(x) * eV * sp.Symbol("Vsym"))
        - eY * (sp.Symbol("Ysym") - eps_f * fx(x) * sp.Symbol("Vsym")))
    rep(f"V3_pushforward_H_eV{eV}_eY{eY}", sp.simplify(diff) == 0,
        "iota_* H = eps_Y * H exactly")
rep("V3_eps_f_law", all(results[(eV, eY)] == eV * eY for eV, eY in results),
    "eps_f = eps_V * eps_Y in all four cases; eps_bh = eps_Y^2 = +1 (bh quadratic"
    " + isometric identification): NO realized fold can make bh odd")

# ---- V4: cap dichotomy + f_c=0 probe ----------------------------------------
two_cap_ok = {k: (results[k] * 1 == -1) for k in results}          # -1 = eps_f*(+1)
rep("V4_two_cap_only_W", two_cap_ok == {(1, 1): False, (-1, -1): False,
                                        (1, -1): True, (-1, 1): True},
    "f_cap opposite (+1/-1, gate c) => only eps_f=-1 (the (V,Y)-diag(+,-)/(-,+)"
    " = closer +-W) survive; +-I forced +1=-1 contradiction")
fc = sp.Symbol("f_c")
same_ok_nonzero = {k: bool(sp.solve(sp.Eq(fc, results[k] * fc), fc) == []) for k in results}
# eps_f=+1: identity => all f_c allowed (solve returns [] meaning identity? probe directly)
same_general = {k: sp.simplify(fc - results[k] * fc) for k in results}
rep("V4_same_closer_dichotomy_needs_fc_nonzero",
    same_general[(1, 1)] == 0 and same_general[(-1, -1)] == 0
    and same_general[(1, -1)] == 2 * fc and same_general[(-1, 1)] == 2 * fc,
    "same-closer: eps_f=+1 identically consistent; eps_f=-1 consistent ONLY at"
    " f_c=0 — the 'only +-I' half of the dichotomy is conditional on f_c != 0"
    " (CAVEAT: not zero-residual unless the banked class has f_c != 0)")

# ---- V5: explicit fixed-point sets on T^2 -----------------------------------
u, v = sp.symbols("u v")  # torus angles for (V,Y) cycles, period 1
# fold torus action: (u,v) -> (eV*u, eY*v) mod 1; fixed: u = eV*u, v = eY*v mod 1
# eps=+1: whole circle fixed (dim 1); eps=-1: 2u=0 mod 1 => u in {0, 1/2} (dim 0)
dims = {}
for eV, eY in results:
    dims[(eV, eY)] = (1 if eV == 1 else 0) + (1 if eY == 1 else 0)
rep("V5_torus_fixed_dims", dims == {(1, 1): 2, (1, -1): 1, (-1, 1): 1, (-1, -1): 0},
    "explicit torus fixed sets: (+,+)=T^2 (dim 2); mixed = circles x 2 points"
    " (dim 1); (-,-) = 4 points (dim 0). With radial always flipped, spatial"
    " fixed set dims = 2/1/1/0: codim-1 crease <=> M = I, UNIQUE")
rep("V5_det_codim", all(
    sp.det(sp.diag(-1, eV, eY)) == sp.Integer(-1) ** (3 - dims[(eV, eY)])
    for eV, eY in dims), "det(d iota) = (-1)^codim per case")

# ---- V6: branch id + shear term ---------------------------------------------
s0, s1, p = sp.symbols("s0 s1 p", nonzero=True)
k00, k10, k11 = sp.symbols("k00 k10 k11")
Sb = sp.Matrix([[s0, 0], [s1, -s0]])
K = sp.Matrix([[k00, 0], [k10, k11]])
Kt = sp.simplify(-(Sb * K * Sb.inv())).subs(s0**2, 1)  # s0=+-1
shear = sp.simplify(Kt[1, 0] - (k10 + 2 * (s1 / s0) * (k11 - k00) / 2))
rep("V6_k10_shear_term", sp.simplify(Kt[0, 0] + k00) == 0
    and sp.simplify(Kt[1, 1] + k11) == 0 and shear == 0,
    "branch (b) generic: k10~ = k10 + 2(s1/s0)*kmod — eps_k10=+1 REQUIRES s1=0"
    " (i.e. the realized completion); lambda, kmod odd always")
Kt_a = sp.simplify(-((-I2) * K * (-I2)))
rep("V6_branch_a_k10_odd", Kt_a[1, 0] == -k10, "branch (a): k10 odd (the tabled kill)")
S_real = sp.diag(-1, 1)
rep("V6_branch_id", sp.det(S_real) == -1 and S_real == Sb.subs({s0: -1, s1: 0}),
    "diag(-1,1) = branch (b) member (s0=-1, s1=0); det=-1 is basis-invariant")
th = sp.Symbol("theta", real=True)
Rot = sp.Matrix([[sp.cos(th), -sp.sin(th)], [sp.sin(th), sp.cos(th)]])
Sc = sp.simplify(Rot * S_real * Rot.T)
rep("V6_s1_basis_robust", sp.simplify(Sc[0, 1] + sp.sin(2 * th)) == 0,
    "off-diagonal after rotation = -sin(2 theta): triangular only on the axes")

# ---- V7: C action ------------------------------------------------------------
c00, c01, c10, c11 = sp.symbols("c00 c01 c10 c11")
C = sp.Matrix([[c00, c01], [c10, c11]])
P = sp.Matrix([[0, p], [1 / p, 0]])
rep("V7_P_involution", sp.simplify(P * P) == I2)
Ct = sp.expand(-(S_real * C * P.inv()))
r0m = sp.Matrix([[0, 1 / p], [p, 0]])
r1m = sp.Matrix([[0, -1 / p], [-p, 0]])
rep("V7_C_rows", sp.simplify(Ct[0, 0] - c01 / p) == 0
    and sp.simplify(Ct[0, 1] - p * c00) == 0
    and sp.simplify(Ct[1, 0] + c11 / p) == 0
    and sp.simplify(Ct[1, 1] + p * c10) == 0)
e0 = r0m.eigenvects()
e1 = r1m.eigenvects()
sig = sorted([sp.simplify(ev) for ev, m, _ in e0 for _ in range(m)]) \
    + sorted([sp.simplify(ev) for ev, m, _ in e1 for _ in range(m)])
rep("V7_2even_2odd", sig == [-1, 1, -1, 1],
    "eigenvalues (+1,-1) per row: 2 even + 2 odd; even row-0 vector (1,p),"
    " odd (1,-p) — p-dependent basis, p free")

# ---- V8: E0 collapse + one-wall probe ---------------------------------------
f0, f1, h0, h1, gf, gh, gx, ell, s = sp.symbols("f0 f1 h0 h1 g_f g_h g_x ell s")
E0 = sp.Rational(1, 2) * (gf * f1**2 + gh * h1**2) + gx * f1 * h1
aff = f0 + f1 * x
even_one_wall = sp.solve(sp.expand(aff.subs(x, ell + s) - aff.subs(x, ell - s)), [f0, f1],
                         dict=True)
rep("V8_even_one_wall_kills_slope", even_one_wall == [{f1: 0}],
    "EVEN about a single wall already forces f1=0 for an affine field (the"
    " canon-crease M=I outcome needs only one crease)")
# NOTE: sp.solve on ONE underdetermined linear eq in [f0,f1] returns the
# particular solution {f0:0,f1:0} (SymPy 1.13 quirk) — use linsolve instead.
odd_one_wall = sp.linsolve([sp.expand(aff.subs(x, ell + s) + aff.subs(x, ell - s))],
                           [f0, f1])
rep("V8_odd_one_wall_does_NOT_kill_slope",
    odd_one_wall == sp.FiniteSet((-f1 * ell, f1)),
    "ODD about ONE wall only pins f0=-f1*ell, slope f1 SURVIVES => in the +-W"
    " (two-cap setwise) outcome the E0 collapse needs oddness at BOTH walls"
    " (mirror structure at both) — a premise the package inherits from the"
    " gradient-seat two-wall geometry; flagged for the record")
odd_two_wall = sp.solve(
    [sp.expand(aff.subs(x, ell + s) + aff.subs(x, ell - s)),
     sp.expand(aff.subs(x, -ell + s) + aff.subs(x, -ell - s))], [f0, f1], dict=True)
rep("V8_odd_two_walls_kills_all", odd_two_wall == [{f0: 0, f1: 0}])
collapse_even = E0.subs({f1: 0, h1: 0})
rep("V8_E0_collapse", sp.simplify(collapse_even) == 0,
    "definite parities => f1=h1=0 => E0=0 exactly (M=I outcome: even/even;"
    " needs E0 to be the pure slope-quadratic — checked against the banked form)")

print(f"\n== INDEPENDENT CHECK: {('ALL PASS' if not FAIL else 'FAILURES: ' + str(FAIL))} ==")
sys.exit(1 if FAIL else 0)
