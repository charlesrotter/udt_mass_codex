#!/usr/bin/env python3
"""BLIND VERIFIER independent re-derivation (agent: blind verifier,
same-session-spawned; date 2026-07-28). Own construction, NOT a copy of
derive_routeB_stage1.py. Adjudicates the load-bearing claims of
udt_p4_routeB_extension_selection_2026-07-28 and hunts counterexamples.

Includes an ADVERSARIAL counter-test (V-C4): the package claims the finite
residual chart symmetry of the registered class is Z2 = {I, R_pi}. The
verifier tests whether the pi-rotations in the (ruler,screen) planes,
R12(pi) = diag(1,-1,-1,1) and R13(pi) = diag(1,-1,1,-1), ALSO preserve the
registered class (they are in SO+(1,3) and fix X0). If they do, the claimed
residual is INCOMPLETE (at least Klein Z2 x Z2), an amendment.

Exact SymPy only. Exit 0 iff all verifier checks pass AND the counter-test
does NOT overturn a load-bearing survival verdict (the residual finding is
reported as an amendment flag, not a crash).
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
phi, phi1, phi2, phi3 = sp.symbols("phi phi1 phi2 phi3", real=True)
a, d, k, lamv = sp.symbols("a d k lamv", real=True)

# ---------------------------------------------------------------- (2a) plane
# My own construction: E07 generator per the banked 07-25 ledger is the
# derivative at phi=0 of diag(e^-phi, e^phi, e^-k phi, e^k phi):
E07_frame = sp.diag(sp.exp(-phi), sp.exp(phi), sp.exp(-k * phi), sp.exp(k * phi))
X_E07 = sp.diff(E07_frame, phi).subs(phi, 0)
vcheck("V2a_E07_generator_is_diag(-1,1,-k,k)", X_E07 == sp.diag(-1, 1, -k, k))
# det-one line in the (a,d) plane: tr(full X) = -1+1+a+d = a+d
Xad = sp.diag(-1, 1, a, d)
vcheck("V2a_E07_on_detone_line", sp.simplify(sp.trace(X_E07)) == 0)
# lambda=(a+d)/2 axis (isotropic a=d) vs kmod=(d-a)/2 axis (a=-d):
# intersection of {a=d} and {a=-d} is only (0,0):
inter = sp.solve([a - d, a + d], [a, d], dict=True)
vcheck("V2a_axes_meet_only_at_origin", inter == [{a: 0, d: 0}])
# Adjudicate the MAP correction: E07 member == isotropic member
# diag(-1,1,lam,lam) iff lam=-k and lam=k iff k=lam=0 (spectator only):
eq_sol = sp.solve([sp.Eq(-k, lamv), sp.Eq(k, lamv)], [k, lamv], dict=True)
vcheck("V2a_E07k_equals_lambda_only_at_spectator", eq_sol == [{k: 0, lamv: 0}])
# => the package's "MAP seat equation FALSE at matrix level" is CORRECT.

# ------------------------------------------------------- (2b) volume loci
# One-parameter frame from the diagonal generator, built by ME via matrix exp
M_ad = sp.exp(sp.Matrix(sp.diag(-1, 1, a, d)) * phi)  # sympy matrix exponential
vcheck("V2b_frame_is_componentwise_exp",
       sp.simplify(M_ad - sp.diag(sp.exp(-phi), sp.exp(phi), sp.exp(a * phi), sp.exp(d * phi))) == sp.zeros(4))
det4 = sp.simplify(M_ad.det())
# 4D volume blind <=> det4 independent of phi <=> a+d=0
vcheck("V2b_4D_blind_iff_a_plus_d_0",
       sp.simplify(det4 - sp.exp((a + d) * phi)) == 0
       and sp.solve(sp.Eq(sp.diff(det4, phi), 0), a) == [-d])
# spatial triad (slots 1,2,3): product of those diagonal factors
tri = sp.simplify(M_ad[1, 1] * M_ad[2, 2] * M_ad[3, 3])
vcheck("V2b_triad_blind_iff_1_plus_a_plus_d_0",
       sp.solve(sp.Eq(sp.diff(tri, phi), 0), a) == [-d - 1])
# on the isotropic axis a=d=lam: 1+2lam=0 <=> lam=-1/2
vcheck("V2b_isotropic_triad_point_lam_minus_half",
       sp.solve(sp.Eq(sp.diff(tri.subs({a: lamv, d: lamv}), phi), 0), lamv) == [sp.Rational(-1, 2)])
# and the 4D reading on the isotropic axis gives lam=0, NOT -1/2:
vcheck("V2b_isotropic_4D_point_lam_zero",
       sp.solve(sp.Eq(sp.diff(det4.subs({a: lamv, d: lamv}), phi), 0), lamv) == [0])
# witness slice volume (my own route: substitute independent monomials
# w=e^{2phi}, z=e^{4 lam phi}; phi-derivative must vanish for ALL w,z>0)
R_ = sp.symbols("R_", positive=True)
aw0 = sp.symbols("aw0", real=True)
detg3 = (R_**2 * sp.exp(2 * phi) - aw0**2 * sp.exp(-2 * phi)) * R_**4 * sp.exp(4 * lamv * phi)
dd = sp.expand(sp.diff(detg3, phi))
wv, zv = sp.symbols("wv zv", positive=True)
dd_wz = sp.expand(dd.subs({sp.exp(4 * lamv * phi): zv, sp.exp(2 * phi): wv,
                           sp.exp(-2 * phi): 1 / wv}))
c1 = sp.simplify(dd_wz.coeff(wv * zv))            # coefficient of w*z
c2 = sp.simplify(sp.expand(dd_wz - c1 * wv * zv) * wv / zv)  # coeff of z/w
vcheck("V2b_slice_coeffs_are_nontrivial", c1 != 0 and c2 != 0)
sol_slice2 = sp.solve([sp.Eq(c1, 0), sp.Eq(c2, 0)], [lamv, aw0], dict=True)
vcheck("V2b_slice_blind_iff_lam_minus_half_and_zero_shift",
       sol_slice2 == [{lamv: sp.Rational(-1, 2), aw0: 0}])
# with a nonzero shift no lambda works: c2=0 forces aw0=0 when lam=-1/2, and
# c1=0 alone pins lam=-1/2:
vcheck("V2b_slice_c1_pins_lam_minus_half",
       sp.solve(sp.Eq(c1, 0), lamv) == [sp.Rational(-1, 2)])
vcheck("V2b_slice_no_lambda_blind_with_nonzero_shift",
       sp.solve(sp.Eq(c2.subs(lamv, sp.Rational(-1, 2)), 0), aw0) == [0])
# CONVENTION-STAMP AUDIT (read separately): the package labels 4D vs triad as
# convention-dependent readings, not banked facts -> confirmed in the .md text.

# ------------------------------------------ (2c) stabilizer / residual / SO(2)
c00, c01, c10, c11, k00, k10, k11 = sp.symbols("vc00 vc01 vc10 vc11 vk00 vk10 vk11", real=True)
SY7 = (c00, c01, c10, c11, k00, k10, k11)
X0 = sp.diag(-1, 1, 0, 0)
XG = sp.Matrix([[-1, 0, 0, 0], [0, 1, 0, 0],
                [c00, c01, k00, 0], [c10, c11, k10, k11]])
# my own so(1,3) parametrization: B = eta * A with A antisymmetric
w = sp.symbols("w0:6", real=True)
A = sp.Matrix([[0, w[0], w[1], w[2]],
               [-w[0], 0, w[3], w[4]],
               [-w[1], -w[3], 0, w[5]],
               [-w[2], -w[4], -w[5], 0]])
B = eta * A
vcheck("V2c_B_is_so13", sp.simplify(B.T * eta + eta * B) == sp.zeros(4))


def class_tangent_violations(M, keep_23_constraint=True):
    """Entries of M that must vanish for M to lie in the class linear part."""
    out = [M[i, j] for i in range(2) for j in range(4)]
    if keep_23_constraint:
        out.append(M[2, 3])
    return out


def stab_dim(keep_23):
    com = B * XG - XG * B
    eqs = []
    for e in class_tangent_violations(com, keep_23):
        p = sp.Poly(sp.expand(e), *SY7)
        eqs.extend(p.coeffs())  # coefficients in the 7 class params AND constants
    Amat, _ = sp.linear_eq_to_matrix([sp.expand(q) for q in eqs], list(w))
    return 6 - Amat.rank(), Amat


dim_reg, _ = stab_dim(True)
vcheck("V2c_registered_connected_stabilizer_trivial", dim_reg == 0)
dim_blk, Ablk = stab_dim(False)
vcheck("V2c_blockform_connected_stabilizer_dim1", dim_blk == 1)
ns = Ablk.nullspace()
Bsol = B.subs({w[i]: ns[0][i] for i in range(6)})
# generator supported only on the screen (2,3) block, antisymmetric there:
vcheck("V2c_blockform_stabilizer_is_screen_rotation",
       Bsol[0:2, :] == sp.zeros(2, 4) and Bsol[:, 0:2] == sp.zeros(4, 2)
       and sp.simplify(Bsol[2, 3] + Bsol[3, 2]) == 0 and Bsol[2, 3] != 0)
# screen SO(2) action law (K,C)->(S K S^-1, S C):
th = sp.symbols("th", real=True)
S = sp.Matrix([[sp.cos(th), sp.sin(th)], [-sp.sin(th), sp.cos(th)]])
Lam = sp.diag(1, 1, 1, 1)
Lam[2:, 2:] = S
Kb = sp.Matrix([[k00, 0], [k10, k11]])
Cb = sp.Matrix([[c00, c01], [c10, c11]])
Xc = sp.simplify(Lam * XG * Lam.T)  # S orthogonal => inverse = transpose
vcheck("V2c_screen_SO2_action_law",
       sp.simplify(Xc[2:, 2:] - S * Kb * S.T) == sp.zeros(2)
       and sp.simplify(Xc[2:, :2] - S * Cb) == sp.zeros(2, 2)
       and sp.simplify(Xc[:2, :2] - sp.diag(-1, 1)) == sp.zeros(2))
# R_pi = diag(1,1,-1,-1): (K,C) -> (K,-C):
Rpi = sp.diag(1, 1, -1, -1)
Xp = Rpi * XG * Rpi
vcheck("V2c_Rpi_action_K_fixed_C_negated",
       Xp[2:, 2:] == Kb and Xp[2:, :2] == -Cb and Xp[:2, :2] == sp.diag(-1, 1))

# ---- ADVERSARIAL COUNTER-TEST V-C4: is the finite residual ONLY {I, R_pi}? --
extra = {"R12pi=diag(1,-1,-1,1)": sp.diag(1, -1, -1, 1),
         "R13pi=diag(1,-1,1,-1)": sp.diag(1, -1, 1, -1)}
residual_incomplete = False
for name, L in extra.items():
    in_lorentz = sp.simplify(L.T * eta * L - eta) == sp.zeros(4)
    proper_ortho = (L.det() == 1) and (L[0, 0] > 0)
    Xr = L * XG * L.inv()
    fixes_X0 = sp.simplify(L * X0 * L.inv() - X0) == sp.zeros(4)
    # stays in registered class: rows 0,1 match [H,0]; (2,3) entry zero:
    viol = class_tangent_violations(Xr - XG.subs({s: 0 for s in SY7}) - (Xr - Xr), True)
    top_ok = (Xr[:2, :2] == sp.diag(-1, 1)) and (Xr[:2, 2:] == sp.zeros(2, 2))
    tri_ok = sp.simplify(Xr[2, 3]) == 0
    stays = top_ok and tri_ok
    not_in_claimed_Z2 = (L != sp.eye(4)) and (L != Rpi)
    print(f"  counter-test {name}: lorentz={in_lorentz} SO+={proper_ortho} "
          f"fixes_X0={fixes_X0} stays_in_registered_class={stays} "
          f"outside_claimed_Z2={not_in_claimed_Z2}")
    if in_lorentz and proper_ortho and fixes_X0 and stays and not_in_claimed_Z2:
        residual_incomplete = True
        # its action on (K,C):
        print(f"    action: K -> {list(Xr[2:, 2:])}, C -> {list(Xr[2:, :2])}")
print(f"V-C4 RESIDUAL-INCOMPLETE FLAG: {residual_incomplete} "
      "(True => claimed Z2 residual is a proper subgroup of the true finite "
      "residual, which contains the Klein group of pi-rotations)")
# does the bigger group change the banked E08 modulus statement 's mod sign'?
s = sp.symbols("s", real=True)
E08g = XG.subs({c00: s, c01: 0, c10: 0, c11: 0, k00: 0, k10: 0, k11: 0})
acts = set()
for L in [sp.eye(4), Rpi] + list(extra.values()):
    acts.add(sp.simplify((L * E08g * L.inv())[2, 0]))
vcheck("V2c_E08_modulus_still_s_mod_sign_under_full_Klein_group",
       acts == {s, -s})
# strata conditions (trK, K=0, C=0) invariant under the Klein group too:
inv_ok = True
for L in list(extra.values()) + [Rpi]:
    Xr = L * XG * L.inv()
    if sp.simplify(sp.trace(Xr[2:, 2:]) - sp.trace(Kb)) != 0:
        inv_ok = False
vcheck("V2c_strata_conditions_invariant_under_Klein_group", inv_ok)

# ---------------------------------------------------------- (2d) E08 cocycle
# my own construction: E08 map from the matrix exponential itself
XE08 = sp.Matrix(sp.diag(-1, 1, 0, 0))
XE08[2, 0] = s
ME08 = sp.exp(XE08 * phi)
sig = lambda x: 1 - sp.exp(-x)
expect = sp.diag(sp.exp(-phi), sp.exp(phi), 1, 1)
expect[2, 0] = s * sig(phi)
vcheck("V2d_E08_exponential_matches_banked_form",
       sp.simplify(ME08 - expect) == sp.zeros(4))
s1, s2, s3, s12 = sp.symbols("s1 s2 s3 s12", real=True)


def Emap(ph, sv):
    M = sp.diag(sp.exp(-ph), sp.exp(ph), 1, 1)
    M[2, 0] = sv * sig(ph)
    return M


P = sp.simplify(Emap(phi2, s2) * Emap(phi1, s1))
s12_claimed = (s1 * sig(phi1) + s2 * sp.exp(-phi1) * sig(phi2)) / sig(phi1 + phi2)
vcheck("V2d_composition_law_matches_claim",
       sp.simplify(P - Emap(phi1 + phi2, s12_claimed)) == sp.zeros(4))
# associativity of the induced law on s (not just matrix associativity):
def comp(pA, sA, pB, sB):  # segment A then B
    return (sA * sig(pA) + sB * sp.exp(-pA) * sig(pB)) / sig(pA + pB)
left = comp(phi1 + phi2, comp(phi1, s1, phi2, s2), phi3, s3)
right = comp(phi1, s1, phi2 + phi3, comp(phi2, s2, phi3, s3))
vcheck("V2d_cocycle_associativity_on_s", sp.simplify(left - right) == 0)
vcheck("V2d_sigma_definition_matches_banked_E08",
       sp.simplify(s * sig(phi) - s * (1 - sp.exp(-phi))) == 0)

# ------------------------------------------------------ (2e) T5 table cells
def dim_of(eqs):
    if not eqs:
        return 7
    Amat, b = sp.linear_eq_to_matrix([sp.expand(e) for e in eqs], list(SY7))
    if Amat.rank() != Amat.row_join(b).rank():
        return None
    return 7 - Amat.rank()


# my own supplied-condition derivations:
# SO(3) holonomy = commutant with rotation algebra {L12,L13,L23}: solve directly
rot_gens = []
for (i, j) in [(1, 2), (1, 3), (2, 3)]:
    g = sp.zeros(4)
    g[i, j] = 1
    g[j, i] = -1
    rot_gens.append(g)
so3_eqs = [e for g in rot_gens for e in (XG * g - g * XG)]
sol_so3 = sp.solve([sp.Eq(e, 0) for e in so3_eqs], list(SY7), dict=True)
vcheck("V2e_SO3_commutant_forces_Xplus1",
       sol_so3 == [{c00: 0, c01: 0, c10: 0, c11: 0, k00: 1, k10: 0, k11: 1}])
# cell (E03, SO3): trace identity: E03 needs k00+k11=0 but SO(3) forces +2:
vcheck("V2e_cell_E03_SO3_EMPTY_via_trace",
       dim_of([k00 + k11, k00 - 1, k10, k11 - 1, c00, c01, c10, c11]) is None)
# cell (E05, SO12): SO+(1,2) = commutant with {L02,L03,L23}:
boost_gens = []
for (i, j) in [(0, 2), (0, 3)]:
    g = sp.zeros(4)
    g[i, j] = 1
    g[j, i] = 1  # boost: eta-antisymmetric
    boost_gens.append(g)
so12_eqs = [e for g in boost_gens + [rot_gens[2]] for e in (XG * g - g * XG)]
sol_so12 = sp.solve([sp.Eq(e, 0) for e in so12_eqs], list(SY7), dict=True)
vcheck("V2e_SO12_commutant_forces_Xminus1",
       sol_so12 == [{c00: 0, c01: 0, c10: 0, c11: 0, k00: -1, k10: 0, k11: -1}])
X_m1 = XG.subs(sol_so12[0])
vcheck("V2e_cell_E05_SO12_dim0_is_Xminus1",
       dim_of([c00, c01, c10, c11, k00 + 1, k10, k11 + 1]) == 0
       and X_m1 == sp.diag(-1, 1, -1, -1))
# cell (E08, swap F): F X F^-1 = -X with banked F = swap(0,1) + I2:
F = sp.Matrix([[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
swap_eqs = list(F * XG * F.inv() + XG)
sol_swap = sp.solve([sp.Eq(e, 0) for e in swap_eqs], list(SY7), dict=True)
vcheck("V2e_swap_full_class_solution",
       sol_swap == [{c00: -c01, c10: -c11, k00: 0, k10: 0, k11: 0}])
# E08 stratum = {c01=c10=c11=k00=k10=k11=0}; intersect with swap conditions:
vcheck("V2e_cell_E08_swap_dim0_s_forced_0",
       dim_of([c01, c10, c11, k00, k10, k11, c00 + c01, c10 + c11]) == 0)
# cell (E02, screen SO2 alone): commutant with L23 on full class -> dim 1:
L23 = sp.zeros(4)
L23[2, 3] = 1
L23[3, 2] = -1
sol_l23 = sp.solve([sp.Eq(e, 0) for e in (XG * L23 - L23 * XG)], list(SY7), dict=True)
vcheck("V2e_screenSO2_full_class_isotropic_axis",
       sol_l23 == [{c00: 0, c01: 0, c10: 0, c11: 0, k00: k11, k10: 0}])
vcheck("V2e_cell_E02_screenSO2_dim1",
       dim_of([c00, c01, c10, c11, k00 - k11, k10]) == 1)
# bonus rank fact used by T1 presentation-singleton claim (independent build):
def vec16(M):
    return sp.Matrix([M[i, j] for i in range(4) for j in range(4)])
Vbasis = []
for sy in SY7:
    Vbasis.append(sp.Matrix(4, 4, lambda i, j: sp.diff(XG[i, j], sy)))
lor6 = []
names6 = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
for (i, j) in names6:
    g = sp.zeros(4)
    g[i, j] = 1
    g[j, i] = -eta[i, i] / eta[j, j]
    lor6.append(g)
stack = sp.Matrix.hstack(*[vec16(M) for M in Vbasis + lor6])
vcheck("V_rank13_extension_plus_so13", stack.rank() == 13)

print()
print(f"VERIFIER SUMMARY: {('ALL PASS' if not FAIL else 'FAILURES: ' + str(FAIL))}")
print(f"RESIDUAL-INCOMPLETE AMENDMENT FLAG: {residual_incomplete}")
sys.exit(1 if FAIL else 0)
