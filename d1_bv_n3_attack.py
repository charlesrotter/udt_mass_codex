#!/usr/bin/env python3
"""BLIND VERIFIER attack on d1_rederive_n3.py (N=3 claims).

Independent re-derivations, DIFFERENT methods from the audit script:

A1. SO(N)-invariant subspace of Lambda^k(R^N) for ALL k, N=2..6 — via the
    so(N) action built from matrix exponent-free generator action on basis
    k-vectors (independent implementation). Expectation from theory: the
    ONLY invariant is the top form (k=N), dim 1; so a 3-index invariant
    exists iff N=3. This also DIRECTLY tests the audit's implicit claim
    that the unique invariant winding density is the N-index epsilon
    (=> degree N-1 after inserting n once).

A2. The cleaner, non-circular form of Forcing A: an SO(N)-invariant 2-FORM
    on the target S^{N-1} corresponds to an SO(N-1)-invariant element of
    Lambda^2(R^{N-1}) (isotropy rep at a pole). Compute dim for
    m=N-1=1..5. Theory: dim 1 iff m=2 (N=3). This tests whether ANY
    invariant 2-form (not just the epsilon-winding) could serve a rank-N
    carrier: if 0 for N!=3, no invariant 2-form density exists AT ALL for
    other ranks — Forcing A is then not merely "the epsilon one is a
    2-form only at N=3" but "there is no invariant 2-form to norm, period".

A3. Degree count: the winding density eps_{a1..aN} n^{a1} dn^{a2}^...^dn^{aN}
    is an (N-1)-form BY CONSTRUCTION (N-1 dn slots). Verify nontriviality:
    pull back by the standard embedding/hedgehog for N=2 (S^1: 1-form dtheta,
    integral 2pi) and N=4 (S^3: 3-form, integral 2*pi^2 * (N-1)! factor?) —
    compute exactly, confirm the density is the (N-1)-sphere volume form up
    to constant, i.e. the construction generalizes and the DEGREE really is
    N-1 (so "2-form iff N=3" is arithmetic, not smuggle).

A4. pi_2(S^m): cite-check via Hurewicz logic only (no computation possible
    in CAS): documented in output for the record with the m=1 subtlety
    (pi_2(S^1)=0 because universal cover R is contractible).

CIRCULARITY probe: does anything below use '3' before concluding it? The
only inputs are: (i) the carrier class = unit vector in R^N (N symbolic/
scanned), (ii) the CELL SURFACE dimension = 2 (spatial 3D cell boundary /
finite-cell canon) — flagged where used.
"""
import itertools
import sympy as sp
from sympy.combinatorics import Permutation

# ---------------------------------------------------------------- A1
print("="*72)
print("A1: dim of SO(N)-invariant subspace of Lambda^k(R^N), all k, N=2..6")
print("    (independent implementation: generator action on basis k-forms)")

def inv_dim_lambda(n, k):
    basis = list(itertools.combinations(range(n), k))
    idx = {b: i for i, b in enumerate(basis)}
    d = len(basis)
    if d == 0:
        return 0
    rows = []
    for (i, j) in itertools.combinations(range(n), 2):
        # generator L_ij: e_i -> e_j, e_j -> -e_i (acts as derivation)
        M = sp.zeros(d, d)
        for b, col in idx.items():
            for pos in range(k):
                for src, dst, sgn in ((i, j, 1), (j, i, -1)):
                    if b[pos] == src:
                        nb = list(b)
                        nb[pos] = dst
                        if len(set(nb)) < k:
                            continue
                        srt = tuple(sorted(nb))
                        # sign of sorting permutation
                        perm = sorted(range(k), key=lambda t: nb[t])
                        psign = Permutation(perm).signature()
                        M[idx[srt], col] += sgn * psign
        rows.append(M)
    big = sp.Matrix.vstack(*rows)
    return d - big.rank()

table = {}
for n in range(2, 7):
    for k in range(1, n + 1):
        table[(n, k)] = inv_dim_lambda(n, k)
for n in range(2, 7):
    print(f"  N={n}: " + "  ".join(f"k={k}:{table[(n,k)]}" for k in range(1, n+1)))
# Theory: invariant iff k==n (the top epsilon), dim 1.
for (n, k), v in table.items():
    assert v == (1 if k == n else 0), (n, k, v)
print("  PASS: unique SO(N) invariant = the top N-form epsilon, for every N.")
print("  => a 3-INDEX invariant exists iff N=3 (audit CHECK 2 confirmed,")
print("     independent code); and the ONLY invariant winding density for a")
print("     rank-N carrier is the N-index epsilon => degree N-1 forms.")

# ---------------------------------------------------------------- A2
print("="*72)
print("A2: SO(m)-invariant 2-forms on S^m (isotropy rep Lambda^2(R^m)), m=1..5")
for m in range(1, 6):
    v = inv_dim_lambda(m, 2) if m >= 2 else 0
    print(f"  m={m} (target S^{m}, rank N={m+1}): dim invariant Lambda^2 = {v}")
    assert v == (1 if m == 2 else 0)
print("  PASS: an invariant 2-form density on the target exists iff N-1=2,")
print("  i.e. N=3 — INDEPENDENT of the epsilon construction. Forcing A is")
print("  therefore not circular via the epsilon: NO invariant 2-form of ANY")
print("  kind exists for other ranks. (The '2' input = cell-surface dim,")
print("  from 3 spatial dims / finite-cell canon — flagged, not from N.)")

# ---------------------------------------------------------------- A3
print("="*72)
print("A3: degree really is N-1 — explicit pullbacks for N=2 and N=4")
# N=2: n=(cos t, sin t); winding density eps_ab n_a dn_b = 1-form
t = sp.symbols('t', real=True)
n2 = sp.Matrix([sp.cos(t), sp.sin(t)])
dn2 = n2.diff(t)
comp2 = sum(sp.LeviCivita(a, b) * n2[a] * dn2[b] for a in range(2) for b in range(2))
comp2 = sp.simplify(comp2)
I2 = sp.integrate(comp2, (t, 0, 2*sp.pi))
print(f"  N=2: eps_ab n_a dn_b = {comp2} dt  (a 1-FORM), integral over S^1 = {I2}")
assert comp2 == 1 and I2 == 2*sp.pi
# N=4: hedgehog on S^3, hyperspherical (chi, th, ph)
chi, th, ph = sp.symbols('chi theta phi', real=True)
n4 = sp.Matrix([sp.sin(chi)*sp.sin(th)*sp.cos(ph),
                sp.sin(chi)*sp.sin(th)*sp.sin(ph),
                sp.sin(chi)*sp.cos(th),
                sp.cos(chi)])
coords = (chi, th, ph)
d = [n4.diff(c) for c in coords]
# 3-form component eps_{abcd} n_a dn_b^dn_c^dn_d on (chi,th,ph):
comp4 = sp.S(0)
for perm in itertools.permutations(range(4)):
    a, b, c, e = perm
    sgn = Permutation(list(perm)).signature()
    # antisymmetrize the three dn slots over coordinate order (chi,th,ph)
    for cp in itertools.permutations(range(3)):
        csgn = Permutation(list(cp)).signature()
        comp4 += sgn * csgn * n4[a] * d[cp[0]][b] * d[cp[1]][c] * d[cp[2]][e] / 6
comp4 = sp.simplify(sp.trigsimp(comp4))
vol_s3 = sp.sin(chi)**2 * sp.sin(th)   # standard S^3 volume element
ratio = sp.simplify(comp4 / vol_s3)
I4 = sp.integrate(sp.integrate(sp.integrate(comp4, (ph, 0, 2*sp.pi)),
                               (th, 0, sp.pi)), (chi, 0, sp.pi))
print(f"  N=4: density / (sin^2 chi sin th) = {ratio}  (a 3-FORM on S^3)")
print(f"       integral over S^3 = {I4}  (= 3! x Vol(S^3)/... nonzero const x 2 pi^2)")
assert ratio.is_constant() and ratio != 0
print("  PASS: the construction generalizes; degree = N-1 exactly (1-form at")
print("  N=2, 2-form at N=3, 3-form at N=4). '2-form iff N=3' is arithmetic.")

# ---------------------------------------------------------------- A4
print("="*72)
print("A4 (record): pi_2(S^1)=0 (universal cover R^1 contractible: pi_2 lifts);")
print("  pi_2(S^2)=Z (Hurewicz: S^2 simply connected, first nonzero homotopy =")
print("  first nonzero homology = H_2 = Z); pi_2(S^m)=0 for m>=3 (Hurewicz:")
print("  pi_k(S^m)=0 for k<m). Also N=1: S^0 disconnected points, pi_2=0.")
print("  => pi_2(S^{N-1}) != 0 iff N=3, over ALL N>=1. Audit CHECK 4 stands.")
print("="*72)
print("ALL VERIFIER ATTACKS ON N=3: the mathematics HOLDS.")
