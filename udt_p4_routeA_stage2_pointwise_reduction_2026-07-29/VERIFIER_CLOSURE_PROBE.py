#!/usr/bin/env python3
"""Closure adjudication probes — independent attack on the A1 extensions."""
import itertools
import sympy as sp
from sympy import Matrix, Rational, symbols, eye, zeros, simplify

eta = sp.diag(-1, 1, 1, 1)

def gen(a, b):
    L = zeros(4, 4)
    L[a, b] = 1
    L[b, a] = -Rational(eta[a, a], eta[b, b])
    return L

PAIRS = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
GENS = [gen(a, b) for a, b in PAIRS]
k00, k10, k11 = symbols("k00 k10 k11")
c00, c01, c10, c11 = symbols("c00 c01 c10 c11")
H2 = sp.diag(-1, 1)
Kb = Matrix([[k00, 0], [k10, k11]])
Cb = Matrix([[c00, c01], [c10, c11]])
X = zeros(4, 4)
X[0:2, 0:2] = H2
X[2:4, 0:2] = Cb
X[2:4, 2:4] = Kb
FORB = [(0, 0), (0, 1), (1, 0), (1, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
bcoef = symbols("beta0:6")
B = zeros(4, 4)
for i, L in enumerate(GENS):
    B = B + bcoef[i] * L
Cm = B * X - X * B
A_pt, _ = sp.linear_eq_to_matrix([Cm[i, j] for i, j in FORB], list(bcoef))

# P1: independent minor divisibility (my own: rem() by k00-k11 in poly ring)
minors = []
for rsel in itertools.combinations(range(9), 6):
    d = sp.expand(A_pt[list(rsel), :].det())
    if d != 0:
        minors.append(d)
div_ok = all(sp.rem(sp.Poly(d, k00, k10, k11, c00, c01, c10, c11),
                    sp.Poly(k00 - k11, k00, k10, k11, c00, c01, c10, c11)).is_zero
             for d in minors)
print("P1 minors:", len(minors), "all divisible by (k00-k11):", div_ok)

# P2: independent Groebner ideal membership of the confinement polynomial
gb = sp.groebner(minors, k00, k10, k11, c00, c01, c10, c11, order="grevlex")
conf = sp.expand((k00 - 1) * (k00 + 1) * (k00 - k11) * (k11 - 1) * (k11 + 1))
print("P2 confinement poly in minor ideal:", sp.expand(gb.reduce(conf)[1]) == 0)
# and adversarial: is the STRONGER product without a factor also in the ideal?
conf_weak = sp.expand((k00 - k11))
print("P2b (attack) bare (k00-k11) in ideal (should be False, else k_mod=0 would be the whole story):",
      sp.expand(gb.reduce(conf_weak)[1]) == 0)

# P3: does a C!=0, k_mod!=0 rank-drop point EXIST? (the 'ONLY genuine cut' stress test)
# On k00=-1 substitute and hunt: rank of A_pt(k00=-1) as function of remaining moduli.
A_res = A_pt.subs(k00, -1)
pts = [
    {k11: 5, k10: 3, c00: 0, c01: 0, c10: 13, c11: 17},
    {k11: 5, k10: 3, c00: 7, c01: 11, c10: 13, c11: 17},
    {k11: 5, k10: 0, c00: 7, c01: 11, c10: 13, c11: 17},
    {k11: 5, k10: 0, c00: 0, c01: 0, c10: 13, c11: 17},
    {k11: 5, k10: 3, c00: 7, c01: 0, c10: 13, c11: 0},
    {k11: 5, k10: 3, c00: 0, c01: 11, c10: 0, c11: 17},
]
for p in pts:
    r = A_res.subs(p).rank()
    print("P3 rank at k00=-1,", {str(k): v for k, v in p.items()}, "->", r)

# P3b: symbolic — which C's give rank<6 at k00=-1, k_mod!=0? Compute the minor ideal
# of A_res and eliminate: find the variety's C-support. Cheap probe: nullspace
# requires all 6x6 minors of A_res to vanish; collect their GCD-free content on C.
minors_res = []
for rsel in itertools.combinations(range(9), 6):
    d = sp.expand(A_res[list(rsel), :].det())
    if d != 0:
        minors_res.append(d)
gb_res = sp.groebner(minors_res, k10, k11, c00, c01, c10, c11, order="grevlex")
# does the ideal force C=0 OR k11 in {-1,1,(k00=)-1}? test membership of candidates:
for cand in [c00, c01, c10, c11]:
    pass
# instead: check whether (k11+1)(k11-1)(k11+1? ) ... simpler: is the product
# c00*c01*c10*c11*(k11^2-1)*(k11+1) ... adversarial existence: solve directly for a
# point with C != 0, k11 generic. Use nullspace condition: rank(A_res)<6 as equations.
sols = sp.solve([m for m in gb_res.exprs], [k10, k11, c00, c01, c10, c11], dict=True)
print("P3b solution branches of the k00=-1 rank-drop variety (first 10):")
for s in sols[:10]:
    print("   ", {str(k): sp.simplify(v) for k, v in s.items()})
print("P3b total branches:", len(sols))

# P4: the corrected witness (r_tf, m00) = (c01 c10, 2 k10 c01) — independent recheck
r_tf, m00 = symbols("r_tf m00")
ident = -2 * k10 * r_tf + m00 * c10  # only these terms active for this witness
val = ident.subs({r_tf: c01 * c10, m00: 2 * k10 * c01})
print("P4 witness satisfies identity identically:", sp.expand(val) == 0)
# character: c01*c10 under R12 (k10,c00,c11 flip): invariant? under R13 (k10,c01,c10 flip): (+)(+)... c01->-c01, c10->-c10 => product invariant. OK trivial.
sR12 = {k10: -k10, c00: -c00, c11: -c11}
sR13 = {k10: -k10, c01: -c01, c10: -c10}
def char(e):
    return (sp.simplify(e.subs(sR12, simultaneous=True) / e),
            sp.simplify(e.subs(sR13, simultaneous=True) / e))
print("P4 char(r_tf=c01c10):", char(c01 * c10), "(want (1,1)); char(m00=k10c01):",
      char(k10 * c01), "(want chi_b = (-1,1))")
print("P4 R_kmod = 2c01c10 nonzero generically:", sp.expand(2 * c01 * c10) != 0)

# ---------------------------------------------------------------------------
# P5 (the NEW-DEFECT counter-computation): identity on the C != 0 resonance
# sub-stratum {k00 = -1, c00 = c01 = 0} and its violation by class members.
sub = {k00: -1, c00: 0, c01: 0}
Xs = X.subs(sub)
A_s, _ = sp.linear_eq_to_matrix([(B * Xs - Xs * B)[i, j] for i, j in FORB], list(bcoef))
ns = A_s.nullspace()
assert len(ns) == 1
Bn = zeros(4, 4)
for i in range(6):
    Bn = Bn + sp.simplify(ns[0][i]) * GENS[i]
W_s = sp.simplify(Bn * Xs - Xs * Bn)
assert all(sp.simplify(W_s[i, j]) == 0 for i, j in FORB)
r_tr, r_tf, r_sh, r_nl = symbols("r_tr r_tf r_sh r_nl")
m00v, m01v, m10v, m11v = symbols("m00 m01 m10 m11")
Wk = r_tr * eye(2) + r_tf * sp.diag(-1, 1) + r_sh * Matrix([[0, 0], [1, 0]]) + r_nl * Matrix([[0, 1], [0, 0]])
Mk = Matrix([[m00v, m01v], [m10v, m11v]])
ident_s = sp.expand(sp.trace(Wk.T * W_s[2:4, 2:4]) + sp.trace(Mk.T * W_s[2:4, 0:2]))
print("P5 stratum {k00=-1, c00=c01=0} identity:", sp.simplify(ident_s), "= 0")
viol_member = ident_s.subs({m10v: c10, m00v: 0, m01v: 0, m11v: 0,
                            r_tr: 0, r_tf: 0, r_sh: 0, r_nl: 0})
viol_omega = ident_s.subs({r_sh: k10, r_tr: 0, r_tf: 0, r_nl: 0,
                           m00v: 0, m01v: 0, m10v: 0, m11v: 0})
print("P5 member R_c10 = c10 pairs to:", sp.simplify(viol_member), "(genuine cut, NOT auto-satisfied)")
print("P5 omega-shape (r_sh = k10) pairs to:", sp.simplify(viol_omega), "(violates on this sub-stratum)")
print("P5 => the claim 'the ONLY genuine new cut is the k_mod = 0 identity' is REFUTED;")
print("      correct: k_mod = 0 is the only CODIMENSION-1 cut; C != 0 resonance sub-loci carry further cuts.")
