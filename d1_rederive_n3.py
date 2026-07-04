#!/usr/bin/env python3
"""D1 provenance audit — CAS checks for N=3 (carrier rank).

Direction D1 of ponder_emergence_directions_2026-07-04.md.
Allowed inputs: the CURRENT framework only (CANON C-2026-06-14-1 + refinement:
the native S^2 carrier n_a, omega_H1 = eps_abc n_a dn_b ^ dn_c, L2+L4).

Four independent checks on what forces (or fails to force) rank N=3:

  CHECK 1  dim Lambda^3(R^N) = C(N,3) = 1  iff N=3      [the legacy epsilon lock]
  CHECK 2  SO(N)-invariant antisymmetric 3-tensor exists iff N=3
           (computed: invariant subspace of Lambda^3(R^N) under so(N))
  CHECK 3  the generalized winding density on a rank-N unit carrier is an
           (N-1)-form; it is a 2-form (the canonized omega_H1 / the S^2-cell
           integrand) iff N=3.  Verified for N=3: omega pulled back by the
           degree-1 hedgehog = 2 x (S^2 area form), integral = 8*pi.
  CHECK 4  (cited, not computed) pi_2(S^{N-1}) != 0 iff N=3
           (pi_2(S^1)=0, pi_2(S^2)=Z, pi_2(S^m)=0 for m>=3 — Hurewicz/classical).

All symbolic, sympy. No solves. Single process.
"""
import itertools
import sympy as sp

print("=" * 70)
print("CHECK 1: C(N,3) = 1 iff N = 3 (unique antisymmetric triple)")
N = sp.symbols('N', positive=True, integer=True)
sols = sp.solve(sp.Eq(sp.binomial(N, 3), 1), N)
print("  solve C(N,3)=1 over positive integers:", sols)
scan = [(n, sp.binomial(n, 3)) for n in range(3, 10)]
print("  scan N=3..9:", scan)
assert sols == [3] and all(v == 1 if n == 3 else v > 1 for n, v in scan)
print("  PASS: N=3 is the unique rank with exactly one antisymmetric triple.")
print("  NOTE (circularity flag): demanding a 3-INDEX antisymmetric singlet")
print("  PRESUPPOSES the '3'; this lock is rigid GIVEN 3, it does not source it.")

print("=" * 70)
print("CHECK 2: SO(N)-invariant subspace of Lambda^3(R^N), N = 3,4,5")
# so(N) generators act on Lambda^3; invariants = joint kernel of the actions.
for n in (3, 4, 5):
    triples = list(itertools.combinations(range(n), 3))
    idx = {t: k for k, t in enumerate(triples)}
    dim = len(triples)

    def act(gen_ij, vec):
        """action of so(n) generator E_ij - E_ji on a Lambda^3 vector."""
        i, j = gen_ij
        out = [sp.S(0)] * dim
        for t, k in idx.items():
            c = vec[k]
            if c == 0:
                continue
            for pos in range(3):
                a = list(t)
                # generator: e_i -> e_j, e_j -> -e_i on slot `pos`
                for (src, dst, sgn) in ((i, j, 1), (j, i, -1)):
                    if a[pos] == src:
                        b = a.copy()
                        b[pos] = dst
                        if len(set(b)) < 3:
                            continue
                        srt = tuple(sorted(b))
                        perm_sign = sp.Matrix([[1 if srt[r] == b[c2] else 0
                                                for c2 in range(3)] for r in range(3)]).det()
                        out[idx[srt]] += sgn * perm_sign * c
        return out

    rows = []
    vec_syms = sp.symbols(f'v0:{dim}')
    for gen in itertools.combinations(range(n), 2):
        res = act(gen, list(vec_syms))
        for expr in res:
            row = [sp.diff(expr, v) for v in vec_syms]
            rows.append(row)
    M = sp.Matrix(rows)
    inv_dim = dim - M.rank()
    print(f"  N={n}: dim Lambda^3 = {dim}, invariant subspace dim = {inv_dim}")
    assert inv_dim == (1 if n == 3 else 0)
print("  PASS: an SO(N)-invariant antisymmetric 3-tensor exists iff N=3")
print("  (it is eps_abc; for N>3 the only invariant form is the top N-form).")

print("=" * 70)
print("CHECK 3: the winding density is an (N-1)-form; 2-form iff N=3;")
print("         hedgehog pullback for N=3 = 2 sin(theta) dtheta^dphi")
th, ph = sp.symbols('theta phi', real=True)
nvec = sp.Matrix([sp.sin(th) * sp.cos(ph), sp.sin(th) * sp.sin(ph), sp.cos(th)])
dth = nvec.diff(th)
dph = nvec.diff(ph)
# omega_H1(d_theta, d_phi) = eps_abc n_a dn_b(th) dn_c(ph) antisymmetrized:
eps = sp.LeviCivita
comp = sp.S(0)
for a in range(3):
    for b in range(3):
        for c in range(3):
            comp += eps(a, b, c) * nvec[a] * (dth[b] * dph[c] - dph[b] * dth[c])
comp = sp.simplify(comp)
print("  omega_H1(e_theta, e_phi) =", comp)          # expect 2*sin(theta)
integral = sp.integrate(sp.integrate(comp, (ph, 0, 2 * sp.pi)), (th, 0, sp.pi))
print("  integral over S^2 =", integral, " (= 8*pi ⇒ deg-1 with normalization 1/(8*pi))")
assert sp.simplify(comp - 2 * sp.sin(th)) == 0 and sp.simplify(integral - 8 * sp.pi) == 0
print("  PASS: for N=3 the density is exactly 2x the S^2 area 2-form.")
print("  STRUCTURE: for rank N (target S^{N-1}) the unique invariant winding")
print("  density eps_{a1..aN} n dn^...^dn has degree N-1.  A 2-FORM (the object")
print("  the canonized L4 = -(kappa/4)|omega_H1|^2_g takes the norm of, and the")
print("  only degree integrable over the spatial S^2 cell surface) forces N-1=2,")
print("  i.e. N=3.  The '3' is sourced by the TWO-dimensionality of the cell")
print("  surface (+1), not by the epsilon lock.")

print("=" * 70)
print("CHECK 4 (cited): pi_2(S^{N-1}) = Z iff N=3; trivial for all other N")
print("  pi_2(S^1)=0, pi_2(S^2)=Z (Hurewicz), pi_2(S^m)=0 for m>=3 (classical).")
print("  So a rank-N unit carrier supports a topological point-defect charge on")
print("  a 2-sphere iff N=3 — the native-defect discovery re-selects N=3.")
print("=" * 70)
print("ALL CHECKS PASS")
