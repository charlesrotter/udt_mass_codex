#!/usr/bin/env python3
"""D1 provenance audit — CAS checks for eta = 1/18 (angular-source/seal coupling).

Legacy routes to the VALUE:
  (A) eta = 1/(2 N^2), N=3  — the 1/N^2 from two triplet averages (each 1/N),
      the 1/2 POSTULATED as a 'quadratic action normalization'
      (NPG:2503-2518; verdict NPG:2522-2525 'not derived until the source-action
      factorization is derived').
  (B) eta = 2 / dim Lambda^2 End(H1) = 2/36 (LHSF:169-170); the functional
      selector 'show the C1 action actually projects through Lambda^2 End(H1)'
      left OPEN (LHSF:176-179, 199-204; DLNA:150,191-195 never discharged).

CHECK 1  value identities: 1/(2N^2) = 1/18 iff N=3;  2/C(N^2,2) = 1/18 iff N=3
CHECK 2  the LOCK-2F identity: 1/(4N^2) = 1/C(N^2,2)  <=>  N^2 - 1 = 8  <=> N=3
         (unique over positive integers) — rigid GIVEN N=3, chance-cheap per
         DLNA (small-rational coverage ~16-23%)
CHECK 3  dim chain: End(ell=1 carrier) = 3x3 = 9 = 1+3+5; dim Lambda^2(9) = 36
CHECK 4  the two routes are NOT independent evidence: route B == route A given
         the identity in CHECK 2 (they coincide exactly at N=3 and ONLY there,
         so a second route adds a lock, not a derivation)
CHECK 5  the missing 1/2: enumerate which single rational factor lambda in
         eta = lambda/N^2 reproduces 1/18 — lambda = 1/2 exactly; no current-
         framework object supplies lambda (the DERIVED seal condition set
         JC1/JC2/C1a-c/C2 + fold pins contains no coupling slot at all —
         doc citation, not CAS).
"""
import sympy as sp

N = sp.symbols('N', positive=True, integer=True)

print("=" * 70)
print("CHECK 1: value identities")
solA = sp.solve(sp.Eq(1 / (2 * N**2), sp.Rational(1, 18)), N)
solB = sp.solve(sp.Eq(2 / sp.binomial(N**2, 2), sp.Rational(1, 18)), N)
print("  1/(2N^2) = 1/18  ->  N =", solA)
print("  2/C(N^2,2) = 1/18  ->  N =", solB)
assert solA == [3] and solB == [3]
print("  PASS (both hit 1/18 only at N=3).")

print("=" * 70)
print("CHECK 2: LOCK-2F  1/(4N^2) = 1/C(N^2,2)")
lock = sp.solve(sp.Eq(sp.binomial(N**2, 2), 4 * N**2), N)
print("  C(N^2,2) = 4N^2  ->  N =", lock, "  [N^2(N^2-1)/2 = 4N^2 <=> N^2-1=8]")
assert lock == [3]
scan = [(n, sp.binomial(n**2, 2), 4 * n**2) for n in range(2, 8)]
print("  scan:", scan)
print("  PASS: unique at N=3. Rigid GIVEN N=3; evidential weight graded by")
print("  DLNA:118-142 (individually cheap matches; 'two locks at chance ~1/37').")

print("=" * 70)
print("CHECK 3: dimension chain")
dim_end = 3 * 3
print("  dim End(ell=1 carrier) =", dim_end, "= 1+3+5 =", 1 + 3 + 5)
dim_l2 = sp.binomial(9, 2)
print("  dim Lambda^2(End) = C(9,2) =", dim_l2)
assert dim_end == 9 and dim_l2 == 36
print("  eta = 2/36 = 1/18; eta/2 = 1/36.  PASS (identities only).")
print("  NOTE: 'H1' is NOT a cohomology group (h1_types: H^1(I x S^2) = 0);")
print("  it is the ell=1 eigenspace, dim 2l+1 = 3. 'End(H1)' = End(R^3).")

print("=" * 70)
print("CHECK 4: routes A and B coincide identically at N=3 and only there")
diff = sp.simplify(1 / (2 * N**2) - 2 / sp.binomial(N**2, 2))
coincide = sp.solve(sp.Eq(diff, 0), N)
print("  1/(2N^2) - 2/C(N^2,2) = 0  ->  N =", coincide)
assert coincide == [3]
print("  PASS: route B is a re-naming at N=3, not independent support for")
print("  the functional form (the selector obligation stays undischarged).")

print("=" * 70)
print("CHECK 5: the missing factor")
lam = sp.symbols('lambda_')
need = sp.solve(sp.Eq(lam / N**2, sp.Rational(1, 18)).subs(N, 3), lam)
print("  eta = lambda/N^2 with N=3 requires lambda =", need)
print("  The 1/2 is the POSTULATED piece (NPG:2513-2518: 'The angular average")
print("  alone gives 1/N or 1/N^2, not the extra 1/2'). No current-framework")
print("  object supplies it: the DERIVED seal set (JC1/JC2; E1 C1a,C1b,C1c,C2;")
print("  fold pins phi=0, rho'=0, H=0) contains NO boundary coupling slot")
print("  (microphysics_E1_composite_closure_results.md Sec 1;")
print("  universe_cell_fold_jc_sigma_results.md) — eta has no native home.")
print("=" * 70)
print("ALL CHECKS PASS")
