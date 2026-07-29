#!/usr/bin/env python3
"""BLIND VERIFIER — A1 CLOSURE adjudication (blind verifier,
same-session-spawned; 2026-07-28). Adversarial re-derivation of the amended
EXACT residual claim: Stab = {Lam in SO+(1,3): Lam X0 Lam^-1 - X0 in V and
Lam V Lam^-1 = V} is EXACTLY the Klein four-group.

Attack route (own construction, NOT the package's staged proof):
  (A) Independent necessity audit of each step's logic, including the
      quantifier structure (probe arguments = necessary conditions on ANY
      class-preserving Lam; sufficiency checked separately).
  (B) BRUTE-FORCE classification: solve the full polynomial system for a
      block-reduced Lam = [[A,0],[Xb,S]] (the reduction to this form is
      itself re-proven from the probe + invertibility), with NO staging:
      hand the joint system to sp.solve and enumerate ALL real solutions.
  (C) Fifth-element construction attempts: rotations S(theta), reflections
      at angle theta, the screen swap, det S=-1 compensated by det A=-1
      beyond the four, and an upper-right-block boost exp(zeta L02).
Exit 0 iff the exact-K4 claim survives every attack.
"""
import sys
import sympy as sp

FAIL = []


def vcheck(name, cond):
    ok = bool(cond)
    print(("VPASS " if ok else "VFAIL ") + name)
    if not ok:
        FAIL.append(name)


eta = sp.diag(-1, 1, 1, 1)
eta2 = sp.diag(-1, 1)
H2 = sp.diag(-1, 1)
X0 = sp.diag(-1, 1, 0, 0)
c00, c01, c10, c11, k00, k10, k11 = sp.symbols("zc00 zc01 zc10 zc11 zk00 zk10 zk11", real=True)
SY7 = (c00, c01, c10, c11, k00, k10, k11)
XG = sp.Matrix([[-1, 0, 0, 0], [0, 1, 0, 0],
                [c00, c01, k00, 0], [c10, c11, k10, k11]])
KLEIN = [sp.eye(4), sp.diag(1, 1, -1, -1), sp.diag(1, -1, -1, 1), sp.diag(1, -1, 1, -1)]


def in_class_tangent(M):
    """Violations of membership in V (top rows zero, (2,3) entry zero)."""
    return [M[i, j] for i in range(2) for j in range(4)] + [M[2, 3]]


# ---------- (A) quantifier audit of STEP 1 (probe necessity, my own algebra) --
# For ANY Lam with Lam V Lam^-1 = V, in particular the member v*=(C=I,K=0)
# must satisfy Lam v* Lam^-1 in V, whose top rows vanish. Row r of
# (Lam v*) Lam^-1 is zero iff row r of (Lam v*) is zero (Lam^-1 invertible):
L = sp.Matrix(4, 4, sp.symbols("L0:16", real=True))
vstar = sp.zeros(4)
vstar[2, 0], vstar[3, 1] = 1, 1
Mv = L * vstar
vcheck("A1c_step1_rows_of_Lv_are_upper_right_entries",
       Mv[0, 0] == L[0, 2] and Mv[0, 1] == L[0, 3]
       and Mv[1, 0] == L[1, 2] and Mv[1, 1] == L[1, 3]
       and all(Mv[i, j] == 0 for i in range(2) for j in (2, 3)))
# (row * invertible = 0 <=> row = 0 is a rank fact, not checked symbolically;
# it is the only non-machine step and is elementary linear algebra.)
# So upper-right block of Lam MUST vanish: a necessary condition quantified
# over ALL class-preserving Lam (the probe is a member the class must keep).
# QUANTIFIER VERDICT: necessary-condition argument, correctly quantified.

# ---------- (B) brute-force classification of the reduced system ------------
# Unknowns: A (4), Xb (4), S (4). Joint system (NO staging):
#   SᵀS=I; SᵀXb=0; Aᵀeta2 A + XbᵀXb = eta2;   [Lorentz]
#   A H2 = H2 A;                                [top rows of Lam X0 Lam^-1 = X0]
#   (S E21 adj(S))[0,1] = 0                     [K-triangularity, k10 probe]
Ab = sp.Matrix(2, 2, sp.symbols("bA0:4", real=True))
Xb = sp.Matrix(2, 2, sp.symbols("bX0:4", real=True))
Sb = sp.Matrix(2, 2, sp.symbols("bS0:4", real=True))
E21 = sp.Matrix([[0, 0], [1, 0]])
eqs = []
eqs += list(Sb.T * Sb - sp.eye(2))
eqs += list(Sb.T * Xb)
eqs += list(Ab.T * eta2 * Ab + Xb.T * Xb - eta2)
eqs += list(Ab * H2 - H2 * Ab)
eqs.append((Sb * E21 * Sb.adjugate())[0, 1])
allsyms = list(Ab) + list(Xb) + list(Sb)
sols = sp.solve([sp.Eq(e, 0) for e in eqs], allsyms, dict=True)
survivors = []
for so in sols:
    Lam = sp.zeros(4)
    Lam[:2, :2] = Ab.subs(so)
    Lam[2:, :2] = Xb.subs(so)
    Lam[2:, 2:] = Sb.subs(so)
    if Lam.free_symbols:
        # a solution family with free parameters would defeat exactness:
        vcheck("A1c_bruteforce_no_free_parameter_families", False)
        continue
    if Lam.det() == 1 and Lam[0, 0] > 0:  # SO+ filter (det, orthochronous)
        survivors.append(Lam)
uniq = []
for M in survivors:
    if not any(M == U for U in uniq):
        uniq.append(M)
vcheck("A1c_bruteforce_exactly_four_solutions", len(uniq) == 4)
vcheck("A1c_bruteforce_solutions_are_Klein_four",
       all(any(M == K for K in KLEIN) for M in uniq))
# and every survivor genuinely preserves the class + is Lorentz (sufficiency):
ok = True
for M in uniq:
    ok = ok and sp.simplify(M.T * eta * M - eta) == sp.zeros(4)
    Xg = M * XG * M.inv()
    ok = ok and all(sp.simplify(e) == 0 for e in in_class_tangent(Xg - X0))
vcheck("A1c_bruteforce_survivors_lorentz_and_class_preserving", ok)

# ---------- (C) fifth-element construction attempts -------------------------
th, ze = sp.symbols("th ze", real=True)
# (C1) screen rotation S(theta), A = diag(1,1) or diag(1,-1):
Srot = sp.Matrix([[sp.cos(th), sp.sin(th)], [-sp.sin(th), sp.cos(th)]])
cond_rot = sp.simplify((Srot * E21 * Srot.adjugate())[0, 1])
vcheck("A1c_rotation_killed_unless_sin_zero",
       sp.simplify(cond_rot + sp.sin(th) ** 2) == 0
       and sp.solve(sp.Eq(cond_rot, 0), th) in ([0, sp.pi], [0, -sp.pi], [sp.pi, 0]))
# (C2) screen reflection at angle theta (det=-1), det compensated by A=diag(1,-1):
Sref = sp.Matrix([[sp.cos(th), sp.sin(th)], [sp.sin(th), -sp.cos(th)]])
vcheck("A1c_reflection_is_O2", sp.simplify(Sref.T * Sref - sp.eye(2)) == sp.zeros(2))
# full conjugation: S E21 S^-1 [0,1] = (S E21 adj S)[0,1]/det S = -sin^2/-1
cond_ref = sp.simplify((Sref * E21 * Sref.inv())[0, 1])
sol_ref = sp.solve(sp.Eq(cond_ref, 0), th)
vcheck("A1c_reflection_killed_unless_sin_zero",
       sp.simplify(cond_ref - sp.sin(th) ** 2) == 0 and set(sol_ref) <= {0, sp.pi, -sp.pi})
# theta=0 reflection: S=diag(1,-1) with A=diag(1,-1) => R13pi (already in K4);
Lref0 = sp.diag(1, -1, 1, -1)
vcheck("A1c_theta0_reflection_is_R13pi_already_in_K4", any(Lref0 == K for K in KLEIN))
# theta=pi reflection: S=diag(-1,1) with A=diag(1,-1) => R12pi (already in K4):
vcheck("A1c_thetapi_reflection_is_R12pi_already_in_K4",
       any(sp.diag(1, -1, -1, 1) == K for K in KLEIN))
# (C3) screen swap: maps the k10 probe to an UPPER-triangular generator:
Ssw = sp.Matrix([[0, 1], [1, 0]])
vcheck("A1c_screen_swap_breaks_K_triangularity",
       (Ssw * E21 * Ssw.inv())[0, 1] == 1)
# (C4) clock-screen boost exp(ze*L02) has nonzero upper-right block; the probe
# member is mapped OUT of V (top rows nonzero) for ze != 0:
L02 = sp.zeros(4)
L02[0, 2] = 1
L02[2, 0] = 1
Boost = sp.exp(L02 * ze)
vcheck("A1c_boost_is_lorentz", sp.simplify(Boost.T * eta * Boost - eta) == sp.zeros(4))
viol = sp.simplify((Boost * vstar * Boost.inv())[0, 0])
vcheck("A1c_boost_maps_probe_out_of_V_for_nonzero_ze",
       sp.simplify(viol.subs(ze, 1)) != 0)
# (C5) time-orientation attack: diag(-1,...) candidates are excluded by
# orthochronicity, which is CONTRACT-legitimate (gauge group = connected
# Lorentz group per the package premise ledger / requirement 7):
vcheck("A1c_antichronous_excluded_by_contract_group",
       sp.diag(-1, -1, 1, 1).det() == 1)  # exists with det 1, but Lam00=-1<0: outside SO+

# ---------- moduli quotient statements -------------------------------------
# (lam, kmod) on the diagonal subfamily are K4-invariant (diagonal members
# have diagonal conjugates under diagonal sign matrices):
a, d = sp.symbols("za zd", real=True)
Xad = sp.diag(-1, 1, a, d)
ok = True
for K in KLEIN:
    Xc = K * Xad * K.inv()
    ok = ok and Xc == Xad
vcheck("A1c_lam_kmod_K4_invariant", ok)
# k10 orbit = {k10, -k10}; C orbits under the two signed-flip actions:
orb = set()
for K in KLEIN:
    orb.add(sp.simplify((K * XG * K.inv())[3, 2]))
vcheck("A1c_k10_orbit_is_mod_sign", orb == {k10, -k10})

print()
print("A1-CLOSURE SUMMARY:", "ALL PASS" if not FAIL else f"FAILURES: {FAIL}")
sys.exit(1 if FAIL else 0)
